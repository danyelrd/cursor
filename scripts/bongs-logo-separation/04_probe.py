# -*- coding: utf-8 -*-
"""Probe specific regions for color sampling and flame/crown positions."""
import numpy as np
import cv2

img = cv2.imread("bongs-logo.png")
H, W = img.shape[:2]
rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
CX, CY, R = 1022, 814, 672

print("=== Robust color sampling (median over patches) ===")
def patch_median(x, y, k=12):
    p = rgb[max(0,y-k):y+k+1, max(0,x-k):x+k+1].reshape(-1, 3)
    return tuple(int(c) for c in np.median(p, axis=0))

# Multiple points around the dark red outer ring
ring_pts = [(CX, CY - 645), (CX + 645, CY), (CX, CY + 645), (CX - 645, CY),
            (CX + 460, CY - 460), (CX - 460, CY + 460)]
ring_colors = [patch_median(x, y, 6) for x, y in ring_pts]
print("dark red ring samples:", ring_colors)
print("dark red ring median:", tuple(int(c) for c in np.median(ring_colors, axis=0)))

# Yellow ring
yel_pts = [(CX, CY - 605), (CX + 605, CY), (CX, CY + 605), (CX - 605, CY)]
yel_colors = [patch_median(x, y, 5) for x, y in yel_pts]
print("yellow ring samples:", yel_colors)
print("yellow ring median:", tuple(int(c) for c in np.median(yel_colors, axis=0)))

# Cream background outside
print("cream bg far corner:", patch_median(30, 30, 15))

# Inner cream (between BONG'S text and yellow ring on the cream area, sample
# right at top middle which is on cream BUT careful not to land on BONG'S letter)
# Try a few points
for x, y in [(800, 350), (1200, 320), (CX, 250), (700, 600), (1350, 600)]:
    print(f"  inner-near-top @ ({x},{y}):", patch_median(x, y, 4))

# Inner red lower (the dark red banner) — sample several
for x, y in [(550, 1100), (1500, 1100), (CX, 1300)]:
    print(f"  inner-red-low @ ({x},{y}):", patch_median(x, y, 6))

# Crown area — sample multiple
print("\n=== Crown area scan ===")
for y in range(1430, 1560, 20):
    row = []
    for x in range(CX - 150, CX + 151, 30):
        c = patch_median(x, y, 3)
        row.append(f"({x},{y})={c}")
    print(" ".join(row))

# Flame accents location scan — look at lower band rim
print("\n=== Left flame accent area ===")
for y in range(1050, 1200, 25):
    for x in range(280, 600, 60):
        c = patch_median(x, y, 3)
        h = hsv[y, x]
        print(f"  ({x},{y}) rgb={c} hsv={tuple(int(v) for v in h)}")

print("\n=== Right flame accent area ===")
for y in range(1050, 1200, 25):
    for x in range(1440, 1780, 60):
        c = patch_median(x, y, 3)
        h = hsv[y, x]
        print(f"  ({x},{y}) rgb={c} hsv={tuple(int(v) for v in h)}")
