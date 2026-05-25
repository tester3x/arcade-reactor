"""
recolor_yellow_knight.py
Recolor the BLUE knight sprites to GOLD/YELLOW while preserving alpha transparency.

USAGE (from a Windows PowerShell or cmd in C:\dev\arcade-reactor):
    pip install pillow numpy
    python recolor_yellow_knight.py

Drop this script next to a folder called `blue_originals` containing your 5 blue
PNG files (ostrich.png, ostrichmove.png, ostrichbrake.png, fly.png, fly2.png).
The script writes recolored versions to `yellow_output/` next to it.

Backup your blue originals first; never let me touch them in place.
"""

from PIL import Image
import numpy as np
import os
import sys

# ---- CONFIG ----
INPUT_DIR  = "blue_originals"
OUTPUT_DIR = "yellow_output"
FILES = ["ostrich.png", "ostrichmove.png", "ostrichbrake.png", "fly.png", "fly2.png"]

# Hue ranges (0..1 scale, so 0.5 = 180 degrees on the color wheel)
BLUE_HUE_MIN = 0.45   # ~162°
BLUE_HUE_MAX = 0.72   # ~259°
GOLD_HUE     = 0.13   # ~47° (warm gold)
SAT_BOOST    = 1.35   # punch up saturation on recolored pixels
SAT_CAP      = 0.95

def recolor(src_path, dst_path):
    img = Image.open(src_path)
    print(f"  {os.path.basename(src_path)}: format={img.format}, mode={img.mode}, size={img.size}")

    # Force RGBA so we always have an alpha channel to preserve.
    img = img.convert("RGBA")
    arr = np.array(img).astype(np.float32) / 255.0
    rgb   = arr[..., :3]
    alpha = arr[..., 3]   # ← THIS is what gets preserved untouched

    # RGB -> HSV (vectorized)
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    maxc = np.max(rgb, axis=-1)
    minc = np.min(rgb, axis=-1)
    v = maxc
    s = np.where(maxc > 0, (maxc - minc) / np.where(maxc > 0, maxc, 1), 0)
    delta = maxc - minc
    delta_safe = np.where(delta == 0, 1, delta)
    rc = (maxc - r) / delta_safe
    gc = (maxc - g) / delta_safe
    bc = (maxc - b) / delta_safe
    hue = np.zeros_like(maxc)
    hue = np.where(r == maxc, bc - gc, hue)
    hue = np.where(g == maxc, 2.0 + rc - bc, hue)
    hue = np.where(b == maxc, 4.0 + gc - rc, hue)
    hue = (hue / 6.0) % 1.0
    hue = np.where(delta == 0, 0, hue)

    # Catch saturated blues + low-sat cyan-blue highlights
    blue_mask     = (hue >= BLUE_HUE_MIN) & (hue <= BLUE_HUE_MAX) & (s > 0.12)
    cyan_highlight = (hue >= 0.40) & (hue <= 0.70) & (s > 0.04) & (s <= 0.12) & (v > 0.55)
    recolor_mask = blue_mask | cyan_highlight

    hue_new = np.where(recolor_mask, GOLD_HUE, hue)
    s_new   = np.where(recolor_mask, np.minimum(s * SAT_BOOST, SAT_CAP), s)

    # HSV -> RGB
    h6 = hue_new * 6.0
    ii = np.floor(h6).astype(int) % 6
    f  = h6 - np.floor(h6)
    p  = v * (1 - s_new)
    q  = v * (1 - s_new * f)
    t  = v * (1 - s_new * (1 - f))
    rgb_out = np.zeros_like(rgb)
    for idx, (rr, gg, bb) in enumerate([(v,t,p),(q,v,p),(p,v,t),(p,q,v),(t,p,v),(v,p,q)]):
        m = (ii == idx)
        rgb_out[..., 0] = np.where(m, rr, rgb_out[..., 0])
        rgb_out[..., 1] = np.where(m, gg, rgb_out[..., 1])
        rgb_out[..., 2] = np.where(m, bb, rgb_out[..., 2])

    rgb_uint8   = (np.clip(rgb_out, 0, 1) * 255).astype(np.uint8)
    alpha_uint8 = (alpha * 255).astype(np.uint8)   # ← alpha PRESERVED, not regenerated
    rgba_out = np.dstack([rgb_uint8, alpha_uint8])

    Image.fromarray(rgba_out, mode="RGBA").save(dst_path, "PNG", optimize=True)
    print(f"    -> wrote {dst_path}")

def main():
    here = os.path.dirname(os.path.abspath(__file__))
    in_dir  = os.path.join(here, INPUT_DIR)
    out_dir = os.path.join(here, OUTPUT_DIR)
    if not os.path.isdir(in_dir):
        print(f"ERROR: put the blue PNGs in '{in_dir}' and re-run.")
        sys.exit(1)
    os.makedirs(out_dir, exist_ok=True)

    print(f"Reading from: {in_dir}")
    print(f"Writing to:   {out_dir}")
    print()
    for fname in FILES:
        src = os.path.join(in_dir, fname)
        if not os.path.exists(src):
            print(f"  SKIP {fname} (not found)")
            continue
        dst = os.path.join(out_dir, fname)
        recolor(src, dst)
    print("\nDone. Drop the files from yellow_output/ into assets/joust/")

if __name__ == "__main__":
    main()
