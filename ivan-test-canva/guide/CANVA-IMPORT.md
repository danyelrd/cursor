# Ivan Test — Editable templates for Canva

The AI PNG previews **cannot** become fully editable in Canva (text and layers are baked into one image).  
Use the files in this folder instead.

## What you got

| File | Best for Canva | Editable |
|------|----------------|----------|
| `pptx/*.pptx` | **Recommended** — Upload → edit text, move boxes | Text, shapes, placeholders |
| `svg/*.svg` | Upload → ungroup | Text (may need font swap) |

All designs are **1080×1080** (Instagram / Facebook square).

---

## Option A — PowerPoint import (easiest)

1. Open [Canva](https://www.canva.com) → **Create a design** → **Instagram Post** (1080×1080).
2. **Upload** the `.pptx` file from `pptx/` (or drag onto the canvas).
3. Canva will convert slides to elements. Click each text box to edit **Ivan Test** copy.
4. Gray/gold **placeholder boxes** = swap with your photos:
   - Upload your bottle / model / salon images.
   - Drag on top of the placeholder → **Send backward** or delete the placeholder.
5. Optional: **File → Download → PDF Print** from Canva when finished.

**Tip:** If Canva groups everything, right-click → **Ungroup** until you can select single text layers.

---

## Option B — SVG import

1. Upload `svg/01-ivan-test-cysteine.svg` (etc.) to Canva.
2. Click the design → **Ungroup** (may need 2–3 times).
3. Edit text directly; replace placeholder rectangles with your images.
4. If fonts look wrong, select headline text → change to **Playfair Display** or **Cormorant** (serif) and body to **Montserrat**.

---

## Brand colors (save in Canva Brand Kit)

| Name | Hex |
|------|-----|
| Ivan Test Gold | `#C9A227` |
| Cream | `#F5F0E8` |
| Brown text | `#3D2914` |
| FDA green | `#2E7D32` |

---

## Placeholder checklist per template

### 01 — Cysteine
- [ ] Hair strand macro (stock or photo)
- [ ] Gold droplet PNGs (Screen / Overlay in Canva: **Transparency** + **Duotone** gold)
- [ ] Ivan Test bottle cutout

### 02 — FDA Tagalog
- [ ] 4–5 bottle photos, same background
- [ ] Fix headline: keep **FDA notified** in green only

### 03 — Argan
- [ ] Model with shiny hair
- [ ] Bottle + soft shadow
- [ ] Optional: bokeh PNG, **Transparency** effect

### 04 — Salon proof
- [ ] Salon candid photo (full bleed)
- [ ] Dark gradient already on template — add **Gradient** element in Canva if needed
- [ ] Small product strip at bottom

---

## Canva effects cheat sheet (match the Luxliss look)

| Effect | Where in Canva |
|--------|----------------|
| Warm grade | **Edit image → Adjust → Warmth** + slight **Brightness** |
| Gold glow | **Elements → search "bokeh gold"** → blend with transparency |
| Soft shadow under bottle | Duplicate image → black → blur → behind bottle |
| Grain (human feel) | **Elements → "film grain" overlay** at ~10% |
| Text gold | Text color `#C9A227` or **Gradient** gold |

---

## What is NOT editable

- The old AI `.png` files: treat as **reference only**, not source files.
- To edit those PNGs you would need Photoshop (**text not recoverable**); rebuild using these templates instead.

---

## Files

```
ivan-test-canva/
├── pptx/          ← import these first
├── svg/           ← alternative import
├── guide/         ← this file
└── generate_templates.py
```
