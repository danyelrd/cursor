#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Export Bong's Fried Chicken House logo as separated layers for Canva.

Outputs:
  - elements/*.png            one transparent PNG per layer (same canvas size)
  - Bongs_Logo_Layers.pdf     multi-page PDF (one layer per page, Canva-friendly)
  - Bongs_Logo_Composite.pdf  single page with all layers stacked (reference)
  - Bongs_Logo_Layers.svg     vector master with named groups (best for Canva)

Usage:
  python3 scripts/bongs_logo_layer_export.py --input path/to/your-logo.png
  python3 scripts/bongs_logo_layer_export.py
"""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass
from pathlib import Path

import cv2
import fitz
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "DOWNLOAD-HERE" / "bongs-logo-separated"
ELEMENTS_DIR = OUT_DIR / "elements"
CANVAS = 2000
CENTER = CANVAS // 2


@dataclass
class Layer:
    layer_id: str
    title: str
    z_index: int


LAYERS = [
    Layer("01-background-inner", "Background (cream inner circle)", 0),
    Layer("02-sunburst", "Sunburst glow", 1),
    Layer("03-flames-large", "Large flames (behind mascot)", 2),
    Layer("04-circle-outer-ring", "Outer circle and maroon ring", 3),
    Layer("05-chicken-mascot", "Chicken mascot", 4),
    Layer("06-drumstick", "Fried drumstick and steam", 5),
    Layer("07-text-bongs", "Text: BONG'S", 6),
    Layer("08-text-fried-chicken-house", "Text: FRIED CHICKEN HOUSE", 7),
    Layer("09-flame-icons", "Small flame icons (left and right)", 8),
    Layer("10-crown-icon", "Crown icon (bottom center)", 9),
]


def _ensure_dirs() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ELEMENTS_DIR.mkdir(parents=True, exist_ok=True)


def _rgba_canvas() -> np.ndarray:
    return np.zeros((CANVAS, CANVAS, 4), dtype=np.uint8)


def _draw_circle_alpha(
    img: np.ndarray,
    center: tuple[int, int],
    radius: int,
    fill: tuple[int, int, int, int],
    width: int = 0,
    outline: tuple[int, int, int, int] | None = None,
) -> None:
    pil = Image.fromarray(img, mode="RGBA")
    draw = ImageDraw.Draw(pil)
    bbox = [
        center[0] - radius,
        center[1] - radius,
        center[0] + radius,
        center[1] + radius,
    ]
    if width > 0 and outline:
        draw.ellipse(bbox, fill=fill, outline=outline, width=width)
    else:
        draw.ellipse(bbox, fill=fill)
    img[:] = np.array(pil)


def _draw_ring_alpha(
    img: np.ndarray,
    center: tuple[int, int],
    outer_r: int,
    inner_r: int,
    fill: tuple[int, int, int, int],
) -> None:
    _draw_circle_alpha(img, center, outer_r, fill)
    _draw_circle_alpha(img, center, inner_r, (0, 0, 0, 0))


def _polar_mask(shape: tuple[int, int], r_in: float, r_out: float, a0: float, a1: float) -> np.ndarray:
    h, w = shape
    yy, xx = np.mgrid[0:h, 0:w]
    cx, cy = w / 2, h / 2
    dx = xx - cx
    dy = yy - cy
    r = np.sqrt(dx * dx + dy * dy) / (w / 2)
    ang = (np.degrees(np.arctan2(dy, dx)) + 360) % 360
    if a0 <= a1:
        ang_ok = (ang >= a0) & (ang <= a1)
    else:
        ang_ok = (ang >= a0) | (ang <= a1)
    return ((r >= r_in) & (r <= r_out) & ang_ok).astype(np.uint8)


def _color_mask_hsv(img_bgr: np.ndarray, ranges: list[tuple[tuple[int, int, int], tuple[int, int, int]]]) -> np.ndarray:
    hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
    mask = np.zeros(img_bgr.shape[:2], dtype=np.uint8)
    for lo, hi in ranges:
        mask |= cv2.inRange(hsv, np.array(lo), np.array(hi))
    return mask


def segment_raster_logo(bgr: np.ndarray) -> dict[str, np.ndarray]:
    """Split a circular raster logo into layer masks using color and geometry."""
    h, w = bgr.shape[:2]
    resized = cv2.resize(bgr, (CANVAS, CANVAS), interpolation=cv2.INTER_LANCZOS4)
    rgba = cv2.cvtColor(resized, cv2.COLOR_BGR2BGRA)

    circle = np.zeros((CANVAS, CANVAS), dtype=np.uint8)
    cv2.circle(circle, (CENTER, CENTER), int(CANVAS * 0.48), 255, -1)
    alpha = rgba[:, :, 3] if rgba[:, :, 3].max() > 10 else np.full((CANVAS, CANVAS), 255, dtype=np.uint8)
    if rgba[:, :, 3].max() <= 10:
        gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
        _, alpha = cv2.threshold(255 - gray, 20, 255, cv2.THRESH_BINARY)
    rgba[:, :, 3] = cv2.bitwise_and(alpha, circle)

    maroon = _color_mask_hsv(
        resized,
        [
            ((0, 80, 40), (12, 255, 140)),
            ((165, 80, 40), (180, 255, 140)),
        ],
    )
    red_text = _color_mask_hsv(resized, [((0, 120, 120), (10, 255, 255)), ((170, 120, 120), (180, 255, 255))])
    yellow = _color_mask_hsv(resized, [((18, 80, 120), (38, 255, 255))])
    orange = _color_mask_hsv(resized, [((8, 120, 120), (22, 255, 255))])
    cream = _color_mask_hsv(resized, [((15, 10, 200), (40, 80, 255))])
    brown = _color_mask_hsv(resized, [((8, 60, 40), (25, 200, 180))])

    ring_band = _polar_mask((CANVAS, CANVAS), 0.78, 0.98, 0, 360)
    top_text_band = _polar_mask((CANVAS, CANVAS), 0.35, 0.95, 200, 340)
    bottom_text_band = _polar_mask((CANVAS, CANVAS), 0.72, 0.95, 20, 160)
    center_band = _polar_mask((CANVAS, CANVAS), 0.0, 0.72, 0, 360)
    upper_center = _polar_mask((CANVAS, CANVAS), 0.0, 0.72, 180, 360)

    def extract(mask: np.ndarray) -> np.ndarray:
        out = rgba.copy()
        m = cv2.bitwise_and(mask, circle)
        out[:, :, 3] = cv2.bitwise_and(out[:, :, 3], m)
        return out

    layers: dict[str, np.ndarray] = {}
    layers["01-background-inner"] = extract(cv2.bitwise_and(cream, center_band))
    layers["02-sunburst"] = extract(cv2.bitwise_and(yellow, cv2.bitwise_and(center_band, upper_center)))
    layers["03-flames-large"] = extract(cv2.bitwise_or(orange, cv2.bitwise_and(yellow, upper_center)))
    layers["04-circle-outer-ring"] = extract(cv2.bitwise_and(maroon, ring_band))
    layers["05-chicken-mascot"] = extract(
        cv2.bitwise_and(brown, cv2.bitwise_and(center_band, cv2.bitwise_not(cv2.bitwise_or(maroon, yellow))))
    )
    layers["06-drumstick"] = extract(cv2.bitwise_and(yellow, cv2.bitwise_and(brown, center_band)))
    layers["07-text-bongs"] = extract(cv2.bitwise_and(red_text, top_text_band))
    layers["08-text-fried-chicken-house"] = extract(cv2.bitwise_and(yellow, bottom_text_band))
    layers["09-flame-icons"] = extract(cv2.bitwise_and(orange, ring_band))
    layers["10-crown-icon"] = extract(cv2.bitwise_and(yellow, _polar_mask((CANVAS, CANVAS), 0.88, 0.98, 260, 280)))

    assigned = np.zeros((CANVAS, CANVAS), dtype=np.uint8)
    for key, value in layers.items():
        if key != "05-chicken-mascot":
            assigned = cv2.bitwise_or(assigned, value[:, :, 3])
    remainder = cv2.bitwise_and(cv2.bitwise_not(assigned), rgba[:, :, 3])
    rem = rgba.copy()
    rem[:, :, 3] = cv2.bitwise_and(remainder, center_band * 255)
    layers["05-chicken-mascot"] = cv2.bitwise_or(layers["05-chicken-mascot"], rem)

    return layers


def render_vector_layers() -> dict[str, np.ndarray]:
    """Procedural fallback layers matching logo structure."""
    maroon = (120, 18, 28, 255)
    red = (210, 32, 38, 255)
    yellow = (255, 204, 46, 255)
    orange = (255, 140, 32, 255)
    cream = (252, 246, 232, 255)
    brown = (120, 72, 38, 255)
    white = (255, 255, 255, 255)
    black = (25, 18, 15, 255)

    layers: dict[str, np.ndarray] = {}

    bg = _rgba_canvas()
    _draw_circle_alpha(bg, (CENTER, CENTER), int(CANVAS * 0.36), cream)
    layers["01-background-inner"] = bg

    sun = _rgba_canvas()
    pil = Image.fromarray(sun, mode="RGBA")
    draw = ImageDraw.Draw(pil)
    for i in range(14):
        ang = math.radians(i * (360 / 14))
        x2 = CENTER + int(math.cos(ang) * CANVAS * 0.22)
        y2 = CENTER + int(math.sin(ang) * CANVAS * 0.22)
        draw.line([(CENTER, CENTER - 120), (x2, y2)], fill=(255, 220, 80, 90), width=6)
    sun[:] = np.array(pil)
    layers["02-sunburst"] = sun

    flames = _rgba_canvas()
    pil = Image.fromarray(flames, mode="RGBA")
    draw = ImageDraw.Draw(pil)
    for ox in (-120, 0, 120):
        draw.polygon(
            [
                (CENTER + ox, CENTER - 80),
                (CENTER + ox - 90, CENTER + 120),
                (CENTER + ox, CENTER + 200),
                (CENTER + ox + 90, CENTER + 120),
            ],
            fill=orange,
        )
        draw.polygon(
            [
                (CENTER + ox, CENTER - 40),
                (CENTER + ox - 50, CENTER + 100),
                (CENTER + ox, CENTER + 150),
                (CENTER + ox + 50, CENTER + 100),
            ],
            fill=yellow,
        )
    flames[:] = np.array(pil)
    layers["03-flames-large"] = flames

    ring = _rgba_canvas()
    _draw_ring_alpha(ring, (CENTER, CENTER), int(CANVAS * 0.48), int(CANVAS * 0.36), maroon)
    layers["04-circle-outer-ring"] = ring

    chicken = _rgba_canvas()
    pil = Image.fromarray(chicken, mode="RGBA")
    draw = ImageDraw.Draw(pil)
    cx, cy = CENTER, CENTER + 40
    draw.ellipse([cx - 200, cy - 220, cx + 200, cy + 180], fill=brown, outline=black, width=6)
    draw.polygon([(cx - 70, cy - 250), (cx, cy - 320), (cx + 70, cy - 250)], fill=red, outline=black)
    draw.ellipse([cx - 55, cy - 120, cx - 10, cy - 75], fill=white, outline=black, width=3)
    draw.ellipse([cx + 10, cy - 120, cx + 55, cy - 75], fill=white, outline=black, width=3)
    draw.ellipse([cx - 35, cy - 105, cx - 18, cy - 88], fill=black)
    draw.ellipse([cx + 18, cy - 105, cx + 35, cy - 88], fill=black)
    draw.polygon([(cx - 35, cy - 55), (cx, cy - 25), (cx + 35, cy - 55)], fill=orange, outline=black)
    draw.ellipse([cx - 150, cy - 300, cx + 150, cy - 170], fill=white, outline=black, width=5)
    draw.rectangle([cx - 150, cy - 210, cx + 150, cy - 185], fill=yellow, outline=black, width=3)
    draw.polygon([(cx - 120, cy + 20), (cx + 120, cy + 20), (cx + 90, cy + 200), (cx - 90, cy + 200)], fill=yellow, outline=black, width=4)
    chicken[:] = np.array(pil)
    layers["05-chicken-mascot"] = chicken

    drum = _rgba_canvas()
    pil = Image.fromarray(drum, mode="RGBA")
    draw = ImageDraw.Draw(pil)
    dx, dy = CENTER - 260, CENTER + 60
    draw.ellipse([dx - 70, dy - 90, dx + 70, dy + 70], fill=(210, 150, 70, 255), outline=black, width=4)
    draw.rectangle([dx - 18, dy + 60, dx + 18, dy + 130], fill=white, outline=black, width=3)
    for i, ox in enumerate((-20, 0, 20)):
        draw.line([(dx + ox, dy - 100 - i * 15), (dx + ox, dy - 140 - i * 15)], fill=white, width=4)
    drum[:] = np.array(pil)
    layers["06-drumstick"] = drum

    try:
        font_big = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 120)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 52)
    except OSError:
        font_big = ImageFont.load_default()
        font_small = ImageFont.load_default()

    tb = _rgba_canvas()
    pil = Image.fromarray(tb, mode="RGBA")
    draw = ImageDraw.Draw(pil)
    text = "BONG'S"
    bbox = draw.textbbox((0, 0), text, font=font_big)
    tw = bbox[2] - bbox[0]
    x, y = CENTER - tw // 2, int(CANVAS * 0.11)
    for ox, oy, c in [(-4, 4, maroon), (3, 3, yellow), (3, -3, yellow)]:
        draw.text((x + ox, y + oy), text, font=font_big, fill=c)
    draw.text((x, y), text, font=font_big, fill=red)
    tb[:] = np.array(pil)
    layers["07-text-bongs"] = tb

    tf = _rgba_canvas()
    pil = Image.fromarray(tf, mode="RGBA")
    draw = ImageDraw.Draw(pil)
    text2 = "FRIED CHICKEN HOUSE"
    bbox = draw.textbbox((0, 0), text2, font=font_small)
    tw = bbox[2] - bbox[0]
    draw.text((CENTER - tw // 2, int(CANVAS * 0.86)), text2, font=font_small, fill=yellow)
    tf[:] = np.array(pil)
    layers["08-text-fried-chicken-house"] = tf

    fi = _rgba_canvas()
    pil = Image.fromarray(fi, mode="RGBA")
    draw = ImageDraw.Draw(pil)
    for side in (-1, 1):
        fx = CENTER + side * int(CANVAS * 0.33)
        fy = int(CANVAS * 0.78)
        draw.polygon([(fx, fy - 40), (fx - 25, fy + 20), (fx, fy + 45), (fx + 25, fy + 20)], fill=orange, outline=black, width=2)
    fi[:] = np.array(pil)
    layers["09-flame-icons"] = fi

    crown = _rgba_canvas()
    pil = Image.fromarray(crown, mode="RGBA")
    draw = ImageDraw.Draw(pil)
    bx, by = CENTER, int(CANVAS * 0.945)
    draw.polygon(
        [(bx, by - 35), (bx - 28, by + 10), (bx - 10, by - 5), (bx, by + 18), (bx + 10, by - 5), (bx + 28, by + 10)],
        fill=yellow,
        outline=maroon,
        width=3,
    )
    crown[:] = np.array(pil)
    layers["10-crown-icon"] = crown

    return layers


def write_layer_pngs(layers: dict[str, np.ndarray]) -> list[Path]:
    paths: list[Path] = []
    for layer in LAYERS:
        arr = layers[layer.layer_id]
        path = ELEMENTS_DIR / f"{layer.layer_id}.png"
        Image.fromarray(arr, mode="RGBA").save(path, "PNG")
        paths.append(path)
    return paths


def write_svg_master() -> Path:
  svg_path = OUT_DIR / "Bongs_Logo_Layers.svg"
  lines = [
      '<?xml version="1.0" encoding="UTF-8"?>',
      f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"',
      f' width="{CANVAS}" height="{CANVAS}" viewBox="0 0 {CANVAS} {CANVAS}">',
  ]
  for layer in LAYERS:
      rel = f"elements/{layer.layer_id}.png"
      lines.append(f'  <g id="{layer.layer_id}" data-name="{layer.title}">')
      lines.append(f'    <image xlink:href="{rel}" x="0" y="0" width="{CANVAS}" height="{CANVAS}" />')
      lines.append("  </g>")
  lines.append("</svg>")
  svg_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
  return svg_path


def write_pdfs(layer_paths: list[Path]) -> tuple[Path, Path]:
    multi_path = OUT_DIR / "Bongs_Logo_Layers.pdf"
    composite_path = OUT_DIR / "Bongs_Logo_Composite.pdf"
    rect = fitz.Rect(0, 0, CANVAS, CANVAS)
    save_opts = dict(garbage=4, deflate=True, clean=True)

    multi = fitz.open()
    for png in layer_paths:
        page = multi.new_page(width=CANVAS, height=CANVAS)
        page.insert_image(rect, filename=str(png), keep_proportion=False)
    multi.save(multi_path, **save_opts)
    multi.close()

    comp = fitz.open()
    page = comp.new_page(width=CANVAS, height=CANVAS)
    for png in layer_paths:
        page.insert_image(rect, filename=str(png), keep_proportion=False, overlay=True)
    comp.save(composite_path, **save_opts)
    comp.close()

    return multi_path, composite_path


def write_readme(source: str) -> None:
    readme = OUT_DIR / "CANVA_IMPORT_GUIDE.txt"
    layer_lines = "\n".join(f"  {L.z_index + 1:2}. {L.title} ({L.layer_id})" for L in LAYERS)
    readme.write_text(
        "Bong's Fried Chicken House - Separated Logo Layers\n"
        "==================================================\n\n"
        "FILES\n"
        "-----\n"
        "Bongs_Logo_Layers.pdf       One layer per page (best for Canva)\n"
        "Bongs_Logo_Composite.pdf    All layers stacked on one page\n"
        "Bongs_Logo_Layers.svg       Groups stay editable in Canva\n"
        "elements/                   Individual transparent PNGs\n\n"
        "HOW TO USE IN CANVA\n"
        "-------------------\n"
        "Option A - PDF:\n"
        "  Upload Bongs_Logo_Layers.pdf. Each page is one part (circle, text,\n"
        "  chicken, flames, etc.). Stack pages aligned to rebuild the logo.\n\n"
        "Option B - SVG:\n"
        "  Upload Bongs_Logo_Layers.svg and ungroup to move each part.\n\n"
        "Option C - PNGs:\n"
        "  Upload all files from elements/ and stack in order 01 to 10.\n\n"
        "LAYER ORDER (bottom to top)\n"
        "---------------------------\n"
        f"{layer_lines}\n\n"
        f"SOURCE\n------\n{source}\n\n"
        "Re-export from your PNG:\n"
        "  python3 scripts/bongs_logo_layer_export.py --input your-logo.png\n",
        encoding="utf-8",
    )


def find_default_source() -> Path | None:
    for name in ("bongs-logo-source.png", "bongs-logo-source.jpg"):
        p = ROOT / name
        if p.is_file():
            return p
    return None


def main() -> None:
    parser = argparse.ArgumentParser(description="Export separated logo layers for Canva")
    parser.add_argument("--input", type=Path, help="Source logo image (PNG/JPG)")
    parser.add_argument("--vector-fallback", action="store_true", help="Force procedural render")
    args = parser.parse_args()

    _ensure_dirs()
    source_note = "Procedural layers (add bongs-logo-source.png at repo root for your file)"

    if args.input and args.input.is_file():
        bgr = cv2.imread(str(args.input))
        if bgr is None:
            raise SystemExit(f"Could not read image: {args.input}")
        layers = segment_raster_logo(bgr)
        source_note = f"Segmented from: {args.input}"
    elif not args.vector_fallback:
        default = find_default_source()
        if default:
            bgr = cv2.imread(str(default))
            layers = segment_raster_logo(bgr)
            source_note = f"Segmented from: {default}"
        else:
            layers = render_vector_layers()
    else:
        layers = render_vector_layers()

    paths = write_layer_pngs(layers)
    write_svg_master()
    multi, composite = write_pdfs(paths)
    write_readme(source_note)

    print(f"Exported {len(paths)} layers to {OUT_DIR}")
    print(f"  Multi-page PDF: {multi}")
    print(f"  Composite PDF:  {composite}")
    print(f"  SVG:            {OUT_DIR / 'Bongs_Logo_Layers.svg'}")


if __name__ == "__main__":
    main()
