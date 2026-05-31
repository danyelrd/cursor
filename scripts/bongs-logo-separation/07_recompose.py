# -*- coding: utf-8 -*-
"""Stack all layers in order to verify the logo reproduces correctly."""
import os, glob
from PIL import Image

layers = sorted(glob.glob("layers/[0-9][0-9]_*.png"))
print("Stacking", len(layers), "layers:")
for f in layers:
    print(" ", os.path.basename(f))

base = Image.open(layers[0]).convert("RGBA")
W, H = base.size
canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
for f in layers:
    im = Image.open(f).convert("RGBA")
    canvas.alpha_composite(im)
canvas.convert("RGB").save("recomposed.png")
print("\nWrote recomposed.png")
