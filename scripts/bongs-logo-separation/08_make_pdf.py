# -*- coding: utf-8 -*-
"""
Build the multi-page PDF: one element per page, each page sized to the
original canvas so elements retain their position when imported into Canva.

Two PDF variants:
  bongs-logo-elements.pdf          - 12 element pages + 1 reference page
  bongs-logo-elements-canva.pdf    - same, but each page has cream background
                                     (Canva sometimes flattens transparency;
                                     this version reads better in that case)
"""
import os, glob
from PIL import Image

OUT_DIR = "layers"
layers = sorted(glob.glob(os.path.join(OUT_DIR, "[0-9][0-9]_*.png")))
ref = Image.open("bongs-logo.png").convert("RGB")
recomposed = Image.open("recomposed.png").convert("RGB")
W, H = ref.size

PRETTY = {
    "01_background_cream": "1. Background (cream)",
    "02_circle_frame":     "2. Circle frame (red + yellow rings)",
    "03_inner_cream_upper":"3. Inner cream (upper half)",
    "04_inner_red_lower":  "4. Inner red banner (lower half)",
    "05_text_bongs":       "5. Text - BONG'S",
    "06_text_fried_chicken_house": "6. Text - FRIED CHICKEN HOUSE",
    "07_flame_accent_left":  "7. Flame accent (left)",
    "08_flame_accent_right": "8. Flame accent (right)",
    "09_crown":              "9. Crown",
    "10_fire_main":          "10. Fire / smoke (behind drumstick)",
    "11_drumstick":          "11. Drumstick (with bone)",
    "12_chicken":            "12. Chicken character",
}

def make_pages(bg_color):
    """Return list of RGB Image pages with given background color."""
    pages = []
    # Page 0: reference (the original logo)
    p0 = ref.copy()
    pages.append(p0)
    # Page 1: recomposed (all layers stacked) as a sanity check
    pages.append(recomposed.copy())
    # Pages 2..N: one per element
    for f in layers:
        bg = Image.new("RGBA", (W, H), bg_color)
        el = Image.open(f).convert("RGBA")
        bg.alpha_composite(el)
        pages.append(bg.convert("RGB"))
    return pages

def save_pdf(pages, path):
    pages[0].save(
        path, "PDF", resolution=150.0, save_all=True,
        append_images=pages[1:]
    )
    print(f"Wrote {path} ({os.path.getsize(path) / 1024:.1f} KB, {len(pages)} pages)")

cream = (250, 248, 236, 255)
transparent_white = (255, 255, 255, 255)

# Variant A: white background per page (Canva imports cleanly,
# elements appear "cut out")
save_pdf(make_pages(transparent_white), "bongs-logo-elements-canva.pdf")

# Variant B: cream background (closer to original)
save_pdf(make_pages(cream), "bongs-logo-elements.pdf")
