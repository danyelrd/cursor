# -*- coding: utf-8 -*-
"""Crop the flame accent / crown areas from the original to inspect."""
from PIL import Image

im = Image.open("bongs-logo.png")
# Left flame accent area
im.crop((350, 1000, 650, 1230)).save("crop_left_flame.png")
# Right flame accent area
im.crop((1400, 1000, 1700, 1230)).save("crop_right_flame.png")
# Crown area
im.crop((850, 1380, 1200, 1520)).save("crop_crown.png")
# FCH text area
im.crop((300, 1150, 1750, 1430)).save("crop_fch_text.png")
print("Saved crops.")
