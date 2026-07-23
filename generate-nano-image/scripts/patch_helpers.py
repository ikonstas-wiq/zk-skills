"""Deterministic pixel-patch primitives for the LAST-RESORT manual edit path.

Use ONLY when the API edit cannot land a change (typically a text typo the model
keeps reproducing) AND the target is text / a small overlay on a near-flat
background. Not for spatial edits, textured/photographic backgrounds, or fonts
Liberation Sans can't approximate.

The agent drives this with vision: zoom -> locate -> patch -> RE-READ the crop to
verify. Nothing here judges success; you must look at the result.

CLI helpers (run via `uv run python patch_helpers.py <cmd> ...`):

  zoom   IMG X0 Y0 X1 Y1 [scale] [grid] OUT   # save a magnified (optionally gridded) crop to inspect
  vprof  IMG X0 Y0 X1 Y1                       # per-column ink profile -> find letter x-spans
  hprof  IMG X0 Y0 X1 Y1                       # per-row ink profile -> find text line y-spans
  sample IMG X0 Y0 X1 Y1                       # median light (bg) + mean dark (ink) colour in box

For the actual patch, import and call patch_text() from a tiny inline script so you
control coordinates exactly.
"""

from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
import numpy as np

FONT_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"  # Arial metric clone


def _box(args, n=4):
    return tuple(int(a) for a in args[:n])


def zoom(img, x0, y0, x1, y1, scale=8, grid=True, out="zoom.png"):
    """Save a magnified crop; optional coordinate grid (red=x cols, blue=y rows)."""
    im = Image.open(img).convert("RGB")
    c = im.crop((x0, y0, x1, y1)).resize(((x1 - x0) * scale, (y1 - y0) * scale), Image.NEAREST)
    if grid:
        d = ImageDraw.Draw(c)
        for gx in range(x0, x1 + 1):
            if gx % 10 == 0:
                x = (gx - x0) * scale
                d.line([(x, 0), (x, c.height)], fill=(255, 0, 0), width=1)
                d.text((x + 1, 1), str(gx), fill=(255, 0, 0))
        for gy in range(y0, y1 + 1):
            if gy % 5 == 0:
                y = (gy - y0) * scale
                d.line([(0, y), (c.width, y)], fill=(0, 0, 255), width=1)
                d.text((1, y + 1), str(gy), fill=(0, 0, 255))
    c.save(out)
    print(f"saved {out}  (crop {x0},{y0},{x1},{y1} x{scale})")


def _mask(img, x0, y0, x1, y1, thresh=200):
    a = np.asarray(Image.open(img).convert("RGB"))[y0:y1, x0:x1]
    return a, (a.sum(2) < thresh)


def vprof(img, x0, y0, x1, y1):
    """Per-column ink counts — read off letter x-spans and the gaps (spaces) between them."""
    _, dark = _mask(img, x0, y0, x1, y1)
    cols = dark.sum(0)
    for i, v in enumerate(cols):
        if v > 0:
            print(x0 + i, "#" * int(v))


def hprof(img, x0, y0, x1, y1):
    """Per-row ink counts — read off text-line y-spans (cap top / baseline)."""
    _, dark = _mask(img, x0, y0, x1, y1)
    for i, v in enumerate(dark.sum(1)):
        if v > 0:
            print(y0 + i, "#" * int(v))


def sample(img, x0, y0, x1, y1):
    """Report median light pixel (use as erase/fill bg) and mean dark pixel (use as ink)."""
    a = np.asarray(Image.open(img).convert("RGB"))[y0:y1, x0:x1].reshape(-1, 3)
    light = a[a.sum(1) > 600]
    dark = a[a.sum(1).argsort()[:60]]
    bg = tuple(int(v) for v in (np.median(light, 0) if len(light) else [255, 255, 255]))
    ink = tuple(int(v) for v in dark.mean(0))
    print(f"bg(median light)={bg}  ink(mean dark)={ink}")


def patch_text(
    img_in,
    img_out,
    erase_box,            # (x0,y0,x1,y1) region to clear — cover the old glyph(s) + any halo
    bg,                   # fill colour (from sample(); use the *local* median light)
    lines,                # [(text, center_x, baseline_y), ...]
    ink=(0, 0, 0),
    cap_height=20,        # target cap height in px (match the surrounding text)
    font_path=FONT_BOLD,
):
    """Erase a region and re-render one or more centred text lines.

    Pick cap_height to match the existing text (measure with hprof). center_x /
    baseline_y come from vprof/hprof. Verify by zoom()-ing the result afterwards.
    """
    im = Image.open(img_in).convert("RGB")
    d = ImageDraw.Draw(im)
    d.rectangle(list(erase_box), fill=tuple(bg))
    fs = 8
    f = ImageFont.truetype(font_path, fs)
    while (f.getbbox("H")[3] - f.getbbox("H")[1]) < cap_height and fs < 200:
        fs += 1
        f = ImageFont.truetype(font_path, fs)
    for text, cx, by in lines:
        d.text((cx, by), text, font=f, fill=tuple(ink), anchor="ms")  # middle / baseline
    im.save(img_out)
    print(f"patched -> {img_out}  (font px {fs})")


_CLI = {"zoom": zoom, "vprof": vprof, "hprof": hprof, "sample": sample}

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in _CLI:
        print(__doc__)
        raise SystemExit(1)
    cmd, rest = sys.argv[1], sys.argv[2:]
    if cmd == "zoom":
        img = rest[0]
        coords = _box(rest[1:5])
        scale = int(rest[5]) if len(rest) > 5 and rest[5].isdigit() else 8
        out = rest[-1] if rest[-1].endswith(".png") else "zoom.png"
        zoom(img, *coords, scale=scale, out=out)
    else:
        _CLI[cmd](rest[0], *_box(rest[1:5]))
