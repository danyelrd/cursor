# -*- coding: utf-8 -*-
"""Build a grid review image: each separated layer composited onto a checker bg."""
import os, glob
import numpy as np
from PIL import Image

OUT_DIR = "layers"
files = sorted(glob.glob(os.path.join(OUT_DIR, "*.png")))
files = [f for f in files if not f.endswith("_raw.png")]

print("Reviewing layers:")
for f in files:
    print(" ", f)

def checker(w, h, sq=24):
    arr = np.zeros((h, w, 3), dtype=np.uint8)
    for y in range(0, h, sq):
        for x in range(0, w, sq):
            c = 200 if ((x // sq + y // sq) % 2 == 0) else 230
            arr[y:y+sq, x:x+sq] = c
    return arr

thumbs = []
THUMB_W = 480
for f in files:
    im = Image.open(f).convert("RGBA")
    w, h = im.size
    th = int(h * THUMB_W / w)
    im_small = im.resize((THUMB_W, th), Image.LANCZOS)
    bg = Image.fromarray(checker(THUMB_W, th), "RGB").convert("RGBA")
    bg.alpha_composite(im_small)
    label = os.path.basename(f)
    from PIL import ImageDraw
    d = ImageDraw.Draw(bg)
    d.rectangle([0, 0, THUMB_W, 28], fill=(0, 0, 0, 200))
    d.text((6, 6), label, fill="white")
    thumbs.append(bg.convert("RGB"))

cols = 3
rows = (len(thumbs) + cols - 1) // cols
tw, th = thumbs[0].size
grid = Image.new("RGB", (cols * tw, rows * th), "white")
for i, t in enumerate(thumbs):
    grid.paste(t, ((i % cols) * tw, (i // cols) * th))
grid.save("review.png")
print(f"\nWrote review.png ({grid.size})")
