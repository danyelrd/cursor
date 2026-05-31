"""Explore the Bong's logo: detect badge circle, sample key colors."""
import numpy as np
import cv2
from PIL import Image

img_bgr = cv2.imread("bongs-logo.png", cv2.IMREAD_COLOR)
h, w = img_bgr.shape[:2]
print(f"Image: {w}x{h}")

gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (9, 9), 2)

circles = cv2.HoughCircles(
    blurred, cv2.HOUGH_GRADIENT, dp=1, minDist=h,
    param1=80, param2=60,
    minRadius=int(h * 0.30), maxRadius=int(h * 0.55),
)
if circles is not None:
    cx, cy, r = np.round(circles[0, 0]).astype(int)
    print(f"Outer circle: center=({cx},{cy}) radius={r}")
else:
    print("No outer circle detected via Hough; falling back to red-pixel bbox")
    hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
    red1 = cv2.inRange(hsv, (0, 80, 50), (10, 255, 255))
    red2 = cv2.inRange(hsv, (165, 80, 50), (179, 255, 255))
    redmask = red1 | red2
    ys, xs = np.where(redmask > 0)
    cx, cy = int(xs.mean()), int(ys.mean())
    r = int(max(xs.max() - xs.min(), ys.max() - ys.min()) / 2)
    print(f"Fallback bbox-derived: center=({cx},{cy}) radius={r}")

hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)

samples = {
    "background-cream":      (50, 50),
    "outer-red-ring":        (cx, cy - r + 30),
    "yellow-ring":           (cx, cy - r + 90),
    "inner-cream-upper":     (cx, cy - r + 200),
    "inner-red-lower":       (cx - 350, cy + 350),
    "BONGS-text":            (cx, cy - r + 250),
    "yellow-banner-text":    (cx - 200, cy + 470),
    "chicken-body-orange":   (cx + 100, cy + 100),
    "chicken-tail":          (cx + 400, cy + 100),
    "drumstick-orange":      (cx - 280, cy - 50),
    "fire-orange":           (cx - 60, cy - 100),
    "fire-red-tip":          (cx + 10, cy - 250),
    "apron-yellow":          (cx + 50, cy + 280),
    "chef-hat-white":        (cx + 80, cy - 380),
    "crown-orange":          (cx, cy + r + 50),
}

print("\nColor samples (BGR -> HSV):")
for name, (px, py) in samples.items():
    px = max(0, min(w - 1, px))
    py = max(0, min(h - 1, py))
    bgr = img_bgr[py, px].tolist()
    hsv_px = hsv[py, px].tolist()
    print(f"  {name:25s} @ ({px:4d},{py:4d})  BGR={bgr}  HSV={hsv_px}")

vis = img_bgr.copy()
cv2.circle(vis, (cx, cy), r, (0, 255, 0), 3)
for name, (px, py) in samples.items():
    px = max(0, min(w - 1, px))
    py = max(0, min(h - 1, py))
    cv2.circle(vis, (px, py), 12, (255, 0, 255), 2)
cv2.imwrite("debug_geometry.png", vis)
print("\nWrote debug_geometry.png")

with open("geometry.txt", "w") as f:
    f.write(f"{w} {h} {cx} {cy} {r}\n")
