# -*- coding: utf-8 -*-
"""Scan radially from center to find the exact ring boundaries."""
import numpy as np
import cv2

img = cv2.imread("bongs-logo.png")
rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
CX, CY = 1022, 814

print("Scanning straight LEFT from center (clean radial, no chicken):")
for r in range(540, 700, 5):
    x, y = CX - r, CY
    c = tuple(int(v) for v in rgb[y, x])
    print(f"  r={r:3d} ({x},{y}) rgb={c}")

print("\nScanning straight RIGHT from center (chicken side):")
for r in range(540, 700, 5):
    x, y = CX + r, CY
    c = tuple(int(v) for v in rgb[y, x])
    print(f"  r={r:3d} ({x},{y}) rgb={c}")

print("\nScanning straight DOWN (banner area):")
for r in range(540, 700, 5):
    x, y = CX, CY + r
    c = tuple(int(v) for v in rgb[y, x])
    print(f"  r={r:3d} ({x},{y}) rgb={c}")

print("\nScanning straight UP (BONG'S text area):")
for r in range(540, 700, 5):
    x, y = CX, CY - r
    c = tuple(int(v) for v in rgb[y, x])
    print(f"  r={r:3d} ({x},{y}) rgb={c}")
