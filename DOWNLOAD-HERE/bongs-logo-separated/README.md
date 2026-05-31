# Bong's Fried Chicken House — Logo Separated by Element

The logo has been split into 12 individual layers so you can adjust each
piece independently in Canva.

## Files

- **bongs-logo-elements.pdf** — Multi-page PDF, **one element per page**, each page
  has the cream background of the original. Import this into Canva to get the
  layered logo: Page 1 is the original reference, Page 2 is the recomposed
  version (all layers stacked), then Pages 3–14 are the individual elements
  in order. Each page is the full 2048×1629 canvas, so elements stay in
  their correct positions.
- **bongs-logo-elements-canva.pdf** — Same as above but with a plain WHITE
  background on each page. Use this version if Canva doesn't pick up the
  cream cleanly.
- **layers/** — Each element as a transparent-background PNG at the full
  original canvas size. Drag any of these into Canva individually if you
  prefer working with PNGs over PDF pages.
- **source-bongs-logo.png** — The source logo I worked from.
- **recomposed-from-layers.png** — Visual proof that re-stacking all 12 layers
  reproduces the original logo (so you know the positions are correct).
- **all-layers-preview.png** — Grid showing all 12 layers side-by-side.

## The 12 elements

| #  | File                              | What it is                                     |
|----|-----------------------------------|------------------------------------------------|
| 01 | `01_background_cream.png`         | Cream background (outside the circle)          |
| 02 | `02_circle_frame.png`             | Dark red outer ring + yellow inner ring        |
| 03 | `03_inner_cream_upper.png`        | Cream interior, upper half of badge            |
| 04 | `04_inner_red_lower.png`          | Dark red interior, lower half (banner area)    |
| 05 | `05_text_bongs.png`               | "BONG'S" wordmark (red, top arc)               |
| 06 | `06_text_fried_chicken_house.png` | "FRIED CHICKEN HOUSE" wordmark (yellow, bottom)|
| 07 | `07_flame_accent_left.png`        | Small yellow flame icon, top-left of banner    |
| 08 | `08_flame_accent_right.png`       | Small yellow flame icon, top-right of banner   |
| 09 | `09_crown.png`                    | Small orange crown at bottom of banner         |
| 10 | `10_fire_main.png`                | Big flames + smoke wisps behind the drumstick  |
| 11 | `11_drumstick.png`                | Fried-chicken drumstick (breading + bone)      |
| 12 | `12_chicken.png`                  | The rooster (hat, head, body, apron, tail, arm)|

## What works well

- All 12 layers reproduce the logo position-for-position when stacked in
  numerical order.
- Each element is a real-pixel cutout from your actual file (except the
  background / ring / inner half-discs, which are clean geometric
  reconstructions in the exact sampled colors — those are flat color shapes
  in the original so a clean re-draw matches better than a noisy pixel
  cutout).

## What may need a small touch-up in Canva

This was an automated raster separation of a flat JPG (the source wasn't a
layered vector). A few seams are imperfect:

- The chicken layer has small white speckles where dark outline pixels were
  ambiguous between the chicken and adjacent elements. In Canva, use the
  Background Remover or "Erase" brush to clean these up if they bother you.
- The "FRIED CHICKEN HOUSE" text is partially obscured by the chicken's
  apron / drumstick in the original. The extracted text mask captures the
  visible letters but not the parts hidden behind the chicken. If you move
  the chicken, you'll see the gap — easiest fix is to re-type the text in
  Canva on top of the banner.
- The drumstick layer captures the breading + bone cleanly. The chicken's
  hand wrapping around the bone is in the chicken layer (not the drumstick),
  so moving the drumstick will reveal the empty hand.
- The fire / smoke layer captures the visible flame strands; some pieces
  that are heavily overlapped by the drumstick body were not separated.

For a perfectly clean per-element separation, the only real fix is to redo
the logo as a layered vector (Illustrator / Figma) — but for re-arranging
the existing elements in Canva, this set is ready to go.
