# -*- coding: utf-8 -*-
"""
Separate the Bong's Fried Chicken House logo into 12 element layers.

Approach:
  * Background / inner fills / circle frame are clean GEOMETRIC reconstructions
    using verified hardcoded colors (sampled from the actual artwork via the
    radial scan in 05_radial_scan.py). This avoids JPEG color bleed between
    the frame, banner, BONG'S text, and inner red fill - they are all the
    SAME dark red, so pixel-based separation would leak.

  * Text, character, fire, drumstick, flame accents, and crown are extracted
    as REAL pixels from the source image via color + spatial masks.

Each output layer is a transparent-background RGBA PNG sized to the full
original canvas so positions are preserved when stacked / imported into Canva.
"""
import os
import numpy as np
import cv2
from PIL import Image

SRC = "bongs-logo.png"
OUT_DIR = "layers"
os.makedirs(OUT_DIR, exist_ok=True)

img_bgr = cv2.imread(SRC, cv2.IMREAD_COLOR)
H, W = img_bgr.shape[:2]
hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

# Geometry (measured) -------------------------------------------------------
CX, CY = 1022, 814
R_OUT       = 672              # outer edge of badge / dark red ring
R_RED_INNER = 625              # inner edge of dark red ring
R_YEL_OUTER = R_RED_INNER      # outer edge of yellow ring
R_YEL_INNER = 605              # inner edge of yellow ring (varies; bottom is wider)
R_INTERIOR  = R_YEL_INNER      # radius of interior content
SPLIT_Y     = CY + 120         # horizontal split: upper cream / lower red

# Verified colors (RGB) -----------------------------------------------------
COL_CREAM     = (250, 248, 236)
COL_DARK_RED  = (140, 25, 17)
COL_YELLOW    = (235, 172, 45)

yy, xx = np.indices((H, W))
dist = np.sqrt((xx - CX) ** 2 + (yy - CY) ** 2)


# Color masks ---------------------------------------------------------------
def mask_cream():
    return (hsv[..., 1] < 35) & (hsv[..., 2] > 220)

def mask_dark_red():
    return (
        ((hsv[..., 0] <= 10) | (hsv[..., 0] >= 168))
        & (hsv[..., 1] >= 130) & (hsv[..., 2] >= 60) & (hsv[..., 2] <= 200)
    )

def mask_yellow():
    return (
        (hsv[..., 0] >= 16) & (hsv[..., 0] <= 32)
        & (hsv[..., 1] >= 130) & (hsv[..., 2] >= 160)
    )

def mask_orange():
    return (
        (hsv[..., 0] >= 8) & (hsv[..., 0] <= 22)
        & (hsv[..., 1] >= 130) & (hsv[..., 2] >= 130)
    )

def mask_red_orange():
    # Tightened: requires V > 165 so the darker banner red (V~140) is excluded.
    # Fire tips and bright red details have V ~ 175-220.
    return (
        ((hsv[..., 0] <= 10) | (hsv[..., 0] >= 168))
        & (hsv[..., 1] >= 160) & (hsv[..., 2] >= 165)
    )

def mask_white():
    return (hsv[..., 1] < 45) & (hsv[..., 2] > 235)

def mask_grey():
    return (hsv[..., 1] < 40) & (hsv[..., 2] >= 195) & (hsv[..., 2] <= 235)

def mask_dark():
    return hsv[..., 2] < 80

m_cream      = mask_cream()
m_dark_red   = mask_dark_red()
m_yellow     = mask_yellow()
m_orange     = mask_orange()
m_red_orange = mask_red_orange()
m_white      = mask_white()
m_grey       = mask_grey()
m_dark       = mask_dark()

inside_badge = dist <= R_INTERIOR + 4


# Helpers -------------------------------------------------------------------
def save_rgba(name, rgba):
    Image.fromarray(rgba, "RGBA").save(os.path.join(OUT_DIR, name))
    a = rgba[..., 3]
    cov = (a > 0).sum() / a.size * 100
    print(f"  {name:35s}  coverage={cov:5.2f}%")

def rgba_solid(mask, rgb_color, antialias=True):
    out = np.zeros((H, W, 4), dtype=np.uint8)
    out[..., :3] = rgb_color
    a = mask.astype(np.uint8) * 255
    if antialias:
        a = cv2.GaussianBlur(a, (3, 3), 0)
    out[..., 3] = a
    return out

def rgba_from_pixels(mask, feather=0):
    out = np.zeros((H, W, 4), dtype=np.uint8)
    out[..., :3] = img_rgb
    a = mask.astype(np.uint8) * 255
    if feather > 0:
        a = cv2.GaussianBlur(a, (feather * 2 + 1, feather * 2 + 1), 0)
    out[..., 3] = a
    return out

def clean(mask, open_k=0, close_k=0):
    out = mask.astype(np.uint8)
    if open_k:
        k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (open_k, open_k))
        out = cv2.morphologyEx(out, cv2.MORPH_OPEN, k)
    if close_k:
        k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (close_k, close_k))
        out = cv2.morphologyEx(out, cv2.MORPH_CLOSE, k)
    return out.astype(bool)

def keep_largest(mask, n=1, min_area=0):
    num, lbl, stats, _ = cv2.connectedComponentsWithStats(mask.astype(np.uint8), 8)
    if num <= 1:
        return mask
    areas = stats[1:, cv2.CC_STAT_AREA]
    order = np.argsort(-areas)
    keep = []
    for i in order:
        if areas[i] < min_area:
            break
        keep.append(i + 1)
        if len(keep) >= n:
            break
    return np.isin(lbl, keep)

def dilate(mask, k=5, it=1):
    return cv2.dilate(mask.astype(np.uint8), np.ones((k, k), np.uint8), iterations=it).astype(bool)

def disc(r):
    return dist <= r

def annulus(r_in, r_out):
    return (dist >= r_in) & (dist <= r_out)


print("\n== Building element layers ==")

# ============================================================================
# 01 - Background cream (solid cream outside badge)
# ============================================================================
bg_mask = ~disc(R_OUT)
save_rgba("01_background_cream.png", rgba_solid(bg_mask, COL_CREAM))

# ============================================================================
# 02 - Circle frame (dark red outer ring + yellow inner ring)
# Composite both bands into one clean geometric layer.
# ============================================================================
red_ann = annulus(R_RED_INNER, R_OUT)
yel_ann = annulus(R_YEL_INNER, R_YEL_OUTER + 2)
frame = np.zeros((H, W, 4), dtype=np.uint8)
frame[..., :3][red_ann] = COL_DARK_RED
frame[..., :3][yel_ann] = COL_YELLOW
a = ((red_ann | yel_ann).astype(np.uint8)) * 255
a = cv2.GaussianBlur(a, (3, 3), 0)
frame[..., 3] = a
save_rgba("02_circle_frame.png", frame)

# ============================================================================
# 03 - Inner cream upper (upper half-disc of interior)
# ============================================================================
inner_upper = disc(R_INTERIOR) & (yy < SPLIT_Y)
save_rgba("03_inner_cream_upper.png", rgba_solid(inner_upper, COL_CREAM))

# ============================================================================
# 04 - Inner red lower (lower half-disc of interior)
# ============================================================================
inner_lower = disc(R_INTERIOR) & (yy >= SPLIT_Y)
save_rgba("04_inner_red_lower.png", rgba_solid(inner_lower, COL_DARK_RED))

# ============================================================================
# 05 - BONG'S text (dark red letters in upper cream area)
# ============================================================================
bongs = (
    m_dark_red
    & inside_badge
    & (yy < SPLIT_Y - 80)
    & (dist < R_YEL_INNER - 8)
    & (dist > R * 0.40 if False else (dist > 200))
)
# Exclude the chicken's red comb (small red dot on forehead, roughly under hat)
bongs = bongs & ~((xx > CX - 80) & (xx < CX + 80) & (yy > CY - 350) & (yy < CY - 180))
bongs = clean(bongs, open_k=3, close_k=11)
save_rgba("05_text_bongs.png", rgba_from_pixels(bongs))

# ============================================================================
# 06 - FRIED CHICKEN HOUSE text (yellow letters on red banner)
# ============================================================================
fch = (
    m_yellow
    & inside_badge
    & (dist < R_YEL_INNER - 10)
    & (yy > SPLIT_Y + 20)
)
# Exclude central yellow apron region (taller bbox to avoid apron leak)
fch = fch & ~((xx > CX - 280) & (xx < CX + 280) & (yy > SPLIT_Y - 50) & (yy < SPLIT_Y + 380))
fch = clean(fch, open_k=2, close_k=7)
save_rgba("06_text_fried_chicken_house.png", rgba_from_pixels(fch))

# ============================================================================
# 07/08 - Small flame accents flanking the banner (left + right)
# From the probe: left flame is around x ? [400, 580], y ? [1050, 1180]
#                 right flame is around x ? [1440, 1620], y ? [1050, 1180]
# Both contain orange/yellow/red shapes with small flame icons.
# Capture the WHOLE flame icon (color = orange or red-orange but NOT the
# background dark red banner color).
# ============================================================================
flame_color = (m_orange | m_yellow | m_red_orange) & ~m_dark_red

# Left flame accent (yellow stylized flame at upper-left end of banner)
left_box  = (xx >= 380) & (xx <= 540) & (yy >= 880) & (yy <= 1020)
left_acc  = flame_color & left_box & inside_badge
left_acc  = clean(left_acc, close_k=9, open_k=2)
left_acc_outline = m_dark & dilate(left_acc, k=5) & left_box & inside_badge
left_acc = clean(left_acc | left_acc_outline, close_k=7)
left_acc = keep_largest(left_acc, n=1, min_area=200)
save_rgba("07_flame_accent_left.png", rgba_from_pixels(left_acc))

# Right flame accent (yellow stylized flame at upper-right end of banner)
right_box = (xx >= 1510) & (xx <= 1680) & (yy >= 880) & (yy <= 1020)
right_acc = flame_color & right_box & inside_badge
right_acc = clean(right_acc, close_k=9, open_k=2)
right_acc_outline = m_dark & dilate(right_acc, k=5) & right_box & inside_badge
right_acc = clean(right_acc | right_acc_outline, close_k=7)
right_acc = keep_largest(right_acc, n=1, min_area=200)
save_rgba("08_flame_accent_right.png", rgba_from_pixels(right_acc))

# ============================================================================
# 09 - Crown (small orange/yellow shape at bottom of badge)
# From the probe scan: crown rows are at y=1430-1480, with alternating
# orange (~243,170,40) and dark red (~140,20,15) pixels. So the crown
# combines both colors.
# ============================================================================
crown_box = (xx > CX - 240) & (xx < CX + 240) & (yy > 1400) & (yy < 1510)
crown_mask = crown_box & (m_orange | m_yellow | m_red_orange) & ~m_dark_red
crown_mask = clean(crown_mask, close_k=15, open_k=2)
# Include dark outlines around the crown
crown_outline = m_dark & dilate(crown_mask, k=5) & crown_box & inside_badge
crown_mask = clean(crown_mask | crown_outline, close_k=7)
crown_mask = keep_largest(crown_mask, n=1, min_area=400)
save_rgba("09_crown.png", rgba_from_pixels(crown_mask))

# ============================================================================
# 10/11/12 - Main fire, drumstick, chicken
# Strategy:
#   - Define a "non-text non-frame" character color set (orange + yellow + white)
#     that explicitly excludes the dark red banner and BONG'S text colors.
#   - For each of chicken/drum/fire, take character pixels inside a tight bbox,
#     keep the largest connected component, then add the dark outline pixels
#     adjacent to that component (only within the same bbox).
# ============================================================================
char_interior = dist < R_INTERIOR - 4
labeled_exclusion = (
    dilate(bongs, k=5) | dilate(fch, k=5)
    | dilate(left_acc, k=5) | dilate(right_acc, k=5)
    | dilate(crown_mask, k=5)
)

# Character core color: orange / yellow / white / bright red-orange.
# Banner color (dark red V<160) is excluded by mask_red_orange's V>165 rule.
char_color = m_orange | m_yellow | m_white | m_red_orange
# To make character regions connect across dark outlines, also include dark
# pixels that lie immediately adjacent (within 9 px) to character-colored ones.
# This bridges the chef-hat (white) to the chicken head (orange) via their
# shared black outlines, etc.
char_with_outline = char_color | (m_dark & dilate(char_color, k=9))

# Bounding boxes ------------------------------------------------------------
# Order of extraction: drumstick -> fire -> chicken (chicken takes everything
# else, so it must be last).
drum_bbox    = (xx > CX - 440) & (xx < CX - 80)  & (yy > CY - 250) & (yy < CY + 280)
fire_bbox    = (xx > CX - 250) & (xx < CX - 30)  & (yy > CY - 400) & (yy < CY + 50)
chicken_bbox = (xx > CX - 280) & (xx < CX + 560) & (yy > CY - 420) & (yy < CY + 420)

# Drumstick ----------------------------------------------------------------
# The breading is a thick solid orange BLOB. Flames are thin orange wisps.
# Distance transform on orange pixels gives high values inside the blob and
# low values inside thin wisps -> threshold to isolate breading core.
drum_orange = m_orange & inside_badge & char_interior & drum_bbox & ~labeled_exclusion
drum_orange = clean(drum_orange, close_k=5)
dist_map = cv2.distanceTransform(drum_orange.astype(np.uint8), cv2.DIST_L2, 5)
breading_seed = dist_map > 9   # pixels at least 9 px from any non-orange edge
breading_seed = clean(breading_seed, open_k=3)
breading_full = dilate(breading_seed, k=11, it=3) & drum_orange
breading_full = clean(breading_full, close_k=13)
breading_full = keep_largest(breading_full, n=1, min_area=3000)

# Add white bone: white pixels in drum_bbox below the breading bottom.
# The bone is a curved white shape going down from below the breading.
# Search a wide vertical band immediately below the breading bbox.
breading_ys, breading_xs = np.where(breading_full)
if len(breading_ys) > 0:
    by_max = int(breading_ys.max())
    bx_min = int(breading_xs.min())
    bx_max = int(breading_xs.max())
else:
    by_max, bx_min, bx_max = CY - 80, CX - 380, CX - 130
bone_search = (
    (yy >= by_max - 20) & (yy <= by_max + 280)
    & (xx >= bx_min - 60) & (xx <= bx_max + 80)
    & inside_badge
)
bone_candidates = m_white & bone_search & ~labeled_exclusion
bone_candidates = clean(bone_candidates, close_k=11, open_k=2)
bone_region = keep_largest(bone_candidates, n=1, min_area=800)

drum_combined = breading_full | bone_region
# Add the orange handle/grip area between breading and bone (small orange CC
# adjacent to either)
remaining_orange = drum_orange & ~drum_combined
near_drum = dilate(drum_combined, k=11)
handle = remaining_orange & near_drum
drum_combined = drum_combined | handle
# Add internal dark outlines bordering drum (small dilation only)
drum_internal_dark = m_dark & dilate(drum_combined, k=3) & drum_bbox & inside_badge
drum_final = drum_combined | drum_internal_dark
drum_final = clean(drum_final, close_k=5)

# Fire (everything flame/smoke-shaped in fire bbox, not drum) -------------
fire_color = m_red_orange | m_grey | m_yellow | m_orange
fire_raw = fire_color & inside_badge & char_interior & fire_bbox
fire_raw = fire_raw & ~labeled_exclusion & ~drum_final
fire_with_outline = fire_raw | (m_dark & dilate(fire_raw, k=7) & fire_bbox & ~drum_final)
fire_with_outline = clean(fire_with_outline, close_k=9, open_k=2)
fire_final = keep_largest(fire_with_outline, n=4, min_area=300)

# Chicken (largest character mass in chicken bbox, excluding drum + fire) --
chicken_in = char_with_outline & inside_badge & char_interior & chicken_bbox
chicken_in = clean(chicken_in, close_k=11, open_k=2)
# Aggressive text exclusion: dilate text masks more so close-fill can't recover them
strong_exclusion = (
    dilate(bongs, k=15) | dilate(fch, k=11)
    | dilate(left_acc, k=7) | dilate(right_acc, k=7)
    | dilate(crown_mask, k=7)
)
chicken_in = chicken_in & ~strong_exclusion & ~drum_final & ~fire_final
# Also remove plain dark-red pixels (banner / BONG'S leak) but not the chicken's
# own red comb dot and tongue. The comb/tongue are small enclosed shapes in the
# head region (around CX, CY-100).
head_region = (xx > CX - 100) & (xx < CX + 150) & (yy > CY - 250) & (yy < CY - 30)
dark_red_to_remove = m_dark_red & ~head_region
chicken_in = chicken_in & ~dark_red_to_remove
chicken_main = keep_largest(chicken_in, n=1, min_area=20000)
chicken_main = clean(chicken_main, close_k=3)

# Final mutual exclusivity
drum_final   = drum_final & ~chicken_main
fire_final   = fire_final & ~chicken_main & ~drum_final

save_rgba("10_fire_main.png",  rgba_from_pixels(fire_final))
save_rgba("11_drumstick.png",  rgba_from_pixels(drum_final))
save_rgba("12_chicken.png",    rgba_from_pixels(chicken_main))

print("\nDone. Layers in:", OUT_DIR)

# Also keep R available (it's the badge radius for downstream scripts)
R = R_OUT
