# Bong's Fried Chicken House — Logo separation scripts

These scripts split the Bong's logo into 12 element layers and assemble a
multi-page PDF for Canva. Outputs live in `DOWNLOAD-HERE/bongs-logo-separated/`.

## Usage

```bash
# Place the source logo here (JPEG or PNG converted to PNG):
cp /path/to/bongs-logo.png .

pip install --user pillow numpy opencv-python-headless

python3 02_separate.py      # build 12 layer PNGs in layers/
python3 03_review.py        # build review.png grid for visual inspection
python3 07_recompose.py     # stack layers to verify they reproduce the logo
python3 08_make_pdf.py      # build the multi-page PDF for Canva import
```

## Scripts

| Script              | Purpose                                                 |
|---------------------|---------------------------------------------------------|
| `01_explore.py`     | Detect badge circle (center/radius), sample key colors  |
| `02_separate.py`    | **Main separator**: build the 12 element layer PNGs     |
| `03_review.py`      | Build a side-by-side grid review of all layers          |
| `04_probe.py`       | Probe specific regions for color sampling debugging     |
| `05_radial_scan.py` | Scan radially from center to find ring boundaries       |
| `06_crops.py`       | Crop areas of interest for manual inspection            |
| `07_recompose.py`   | Stack all layers back together to verify positions      |
| `08_make_pdf.py`    | Build the final 14-page PDF (reference + recomposed + 12 elements) |
