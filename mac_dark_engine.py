#!/usr/bin/env python3
"""
mac_dark_engine.py — Apple-style Dark Mode icon generator.

Design rules (how Apple actually builds a dark icon variant):

  1. The *canvas* goes dark, the *logo* does not.  A white or coloured card
     becomes a near-black tile tinted with the icon's own hue.  The artwork
     that sits on it keeps its brand colours at full strength.
  2. Never invert artwork.  Inverting turns GIMP's brown Wilber blue and
     Thunderbird's blue bird cream — it destroys brand identity.
  3. Never globally dim or desaturate.  A flat "multiply by 0.85" reads as
     a dirty icon, not a designed one.
  4. Lift artwork that would disappear.  A black wordmark on a black tile is
     invisible, so its *lightness* is flipped while hue and saturation stay.
  5. Same tile geometry as light mode, so the two sets feel like one family.
  6. Dark tiles need an edge.  A hairline top rim highlight plus an outer
     shadow keeps the icon from melting into a dark dock.

Requires: numpy, pillow, rsvg-convert.
"""

import argparse
import base64
import datetime
import hashlib
import io
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import dark_handdrawn as HD

try:
    import numpy as np
    from PIL import Image
except ImportError as e:
    sys.exit(f"{e}.\nInstale as dependências: pip install --user numpy pillow\n"
             "(ou use um venv). É preciso também o rsvg-convert (librsvg).")

RASTER = 512
LUM = np.array([0.2126, 0.7152, 0.0722], dtype=np.float32)

REPO = Path(__file__).parent.resolve()
LIGHT_DIR = REPO / "apps" / "scalable"
DARK_DIR = REPO / "apps-dark" / "scalable"


# --------------------------------------------------------------------------
# colour helpers
# --------------------------------------------------------------------------

def rgb_to_hsv(rgb):
    """rgb: (..., 3) float 0..1 -> hsv (..., 3), h in 0..1."""
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    mx = rgb.max(-1)
    mn = rgb.min(-1)
    d = mx - mn
    h = np.zeros_like(mx)
    safe = d > 1e-6
    with np.errstate(invalid="ignore", divide="ignore"):
        rm = (mx == r) & safe
        gm = (mx == g) & safe & ~rm
        bm = safe & ~rm & ~gm
        h = np.where(rm, ((g - b) / np.where(d == 0, 1, d)) % 6, h)
        h = np.where(gm, (b - r) / np.where(d == 0, 1, d) + 2, h)
        h = np.where(bm, (r - g) / np.where(d == 0, 1, d) + 4, h)
    h = (h / 6.0) % 1.0
    s = np.where(mx > 1e-6, d / np.where(mx == 0, 1, mx), 0.0)
    return np.stack([h, s, mx], axis=-1)


def hsv_to_rgb(hsv):
    h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    i = np.floor(h * 6.0)
    f = h * 6.0 - i
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    i = (i.astype(np.int32) % 6)
    r = np.select([i == 0, i == 1, i == 2, i == 3, i == 4, i == 5], [v, q, p, p, t, v])
    g = np.select([i == 0, i == 1, i == 2, i == 3, i == 4, i == 5], [t, v, v, q, p, p])
    b = np.select([i == 0, i == 1, i == 2, i == 3, i == 4, i == 5], [p, p, t, v, v, q])
    return np.stack([r, g, b], axis=-1)


def hexcolor(rgb):
    v = np.clip(np.asarray(rgb, dtype=np.float32), 0, 1)
    return "#%02x%02x%02x" % tuple(int(round(c * 255)) for c in v)


# --------------------------------------------------------------------------
# rasterising
# --------------------------------------------------------------------------

def rasterize(data, is_png, size=RASTER):
    """Render source art into a centred square RGBA float array, or None."""
    try:
        if is_png:
            im = Image.open(io.BytesIO(data)).convert("RGBA")
        else:
            with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as t:
                t.write(data)
                tmp = t.name
            try:
                r = subprocess.run(
                    ["rsvg-convert", "--keep-aspect-ratio", "-w", str(size), "-h", str(size), tmp],
                    capture_output=True,
                )
                if r.returncode != 0 or not r.stdout:
                    return None
                im = Image.open(io.BytesIO(r.stdout)).convert("RGBA")
            finally:
                os.unlink(tmp)
    except Exception:
        return None

    w, h = im.size
    if w == 0 or h == 0:
        return None
    if (w, h) != (size, size):
        sc = size / max(w, h)
        nw, nh = max(1, round(w * sc)), max(1, round(h * sc))
        im = im.resize((nw, nh), Image.LANCZOS)
        canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        canvas.paste(im, ((size - nw) // 2, (size - nh) // 2))
        im = canvas
    return np.asarray(im, dtype=np.float32) / 255.0


# --------------------------------------------------------------------------
# background analysis
# --------------------------------------------------------------------------

def ring_mask(size, inset, band=0.035):
    i0 = int(size * inset)
    i1 = i0 + max(3, int(size * band))
    i1 = min(i1, size // 2 - 1)
    m = np.zeros((size, size), dtype=bool)
    m[i0:i1, i0:size - i0] = True
    m[size - i1:size - i0, i0:size - i0] = True
    m[i0:size - i0, i0:i1] = True
    m[i0:size - i0, size - i1:size - i0] = True
    return m


# Outermost first: full-bleed art matches immediately; art already wrapped in a
# squircle (our hand-drawn icons) or a circular logo matches further in.
RING_INSETS = (0.05, 0.09, 0.14, 0.20)


def find_background_ring(alpha, size):
    for inset in RING_INSETS:
        m = ring_mask(size, inset)
        if alpha[m].mean() > 0.85:
            return m, inset
    return None, None


def fit_background(rgb, alpha, ring):
    """Least-squares quadratic model of the background colour field.

    Handles flat fills, linear gradients and (approximately) radial ones.
    Returns (predicted_field, residual, mean_bg_colour) or None.
    """
    size = rgb.shape[0]
    ys, xs = np.nonzero(ring & (alpha > 0.9))
    if len(ys) < 200:
        return None
    x = (xs / (size - 1)) * 2 - 1
    y = (ys / (size - 1)) * 2 - 1
    A = np.stack([np.ones_like(x), x, y, x * x, y * y, x * y], axis=1)
    vals = rgb[ys, xs]

    coef, *_ = np.linalg.lstsq(A, vals, rcond=None)
    err = np.abs(A @ coef - vals).max(axis=1)
    # Reject outliers: a logo touching the ring must not drag the fit.
    keep = err <= max(0.04, float(np.percentile(err, 75)))
    if keep.sum() < 150:
        keep = np.ones_like(err, dtype=bool)
    coef, *_ = np.linalg.lstsq(A[keep], vals[keep], rcond=None)
    residual = float(np.abs(A[keep] @ coef - vals[keep]).max(axis=1).mean())

    gy, gx = np.mgrid[0:size, 0:size]
    X = (gx / (size - 1)) * 2 - 1
    Y = (gy / (size - 1)) * 2 - 1
    field = (
        coef[0] + coef[1] * X[..., None] + coef[2] * Y[..., None]
        + coef[3] * (X * X)[..., None] + coef[4] * (Y * Y)[..., None]
        + coef[5] * (X * Y)[..., None]
    )
    return np.clip(field, 0, 1), residual, vals[keep].mean(axis=0)


def _dilate(m):
    out = m.copy()
    out[1:, :] |= m[:-1, :]
    out[:-1, :] |= m[1:, :]
    out[:, 1:] |= m[:, :-1]
    out[:, :-1] |= m[:, 1:]
    return out


def border_connected(mask, cap=400):
    """The part of `mask` reachable from the image border.

    Without this, a white phone handset punched into a white-carded WhatsApp
    logo gets erased along with the card.  Run at half resolution — an icon's
    background is never a one-pixel maze — to keep the flood cheap.
    """
    small = np.ascontiguousarray(mask[::2, ::2])
    cur = np.zeros_like(small)
    cur[0, :] |= small[0, :]
    cur[-1, :] |= small[-1, :]
    cur[:, 0] |= small[:, 0]
    cur[:, -1] |= small[:, -1]
    prev = -1
    for _ in range(cap):
        cur = _dilate(cur) & small
        n = int(cur.sum())
        if n == prev:
            break
        prev = n
    grown = np.repeat(np.repeat(cur, 2, axis=0), 2, axis=1)[:mask.shape[0], :mask.shape[1]]
    out = grown & mask
    for _ in range(3):
        out = _dilate(out) & mask
    return out


def label_components(mask, cap=1500):
    """Label 4-connected regions at half resolution, or None if unfinished.

    A label has to travel the whole length of its region, and a glyph like a
    letter "A" is a long thin path — too low a cap and the labelling silently
    gives up, taking the fragment cleanup with it.
    """
    small = np.ascontiguousarray(mask[::2, ::2])
    ids = ((np.arange(small.size, dtype=np.int32).reshape(small.shape) + 1) * small)
    for _ in range(cap):
        prev = int(ids.sum())
        for _ in range(2):          # two sweeps per round: labels travel faster
            m = ids.copy()
            np.maximum(m[1:, :], ids[:-1, :], out=m[1:, :])
            np.maximum(m[:, 1:], ids[:, :-1], out=m[:, 1:])
            np.maximum(m[:-1, :], m[1:, :], out=m[:-1, :])
            np.maximum(m[:, :-1], m[:, 1:], out=m[:, :-1])
            ids = m * small
        if int(ids.sum()) == prev:
            return ids
    return None                     # never guess from an unfinished labelling


def clean_fragments(rgba, dist, t0, min_frac=0.0026):
    """Drop the crumbs a cut-away card leaves behind.

    Two kinds of debris survive a colour cut: specks far too small to be
    artwork, and shapes that barely differ from the card they sat on — a
    bevel highlight, or 2048's empty white tile against its white board.  Left
    in, the contrast rescue then brightens them into the loudest thing on the
    tile.  Both are background by any honest reading, so both go.
    """
    a = rgba[..., 3]
    mask = a > 0.35
    if not mask.any():
        return rgba
    ids = label_components(mask)
    if ids is None:
        return rgba

    small_dist = dist[::2, ::2]
    counts = np.bincount(ids.ravel())
    counts[0] = 0
    min_area = max(4, int(min_frac * ids.size))

    big = np.nonzero(counts >= min_area)[0]
    if len(big) > 250:
        return rgba                      # too speckled to reason about

    keep_ids = []
    kept_area = 0
    for cid in big:
        sel = ids == cid
        area = int(counts[cid])
        if float(np.percentile(small_dist[sel], 75)) < 2.2 * t0:
            continue                     # indistinguishable from the card
        keep_ids.append(cid)
        kept_area += area

    total = int(counts.sum())
    if not keep_ids or kept_area < 0.25 * total:
        return rgba                      # cleaning would gut the icon; leave it

    keep = np.isin(ids, np.asarray(keep_ids))
    keep = np.repeat(np.repeat(keep, 2, axis=0), 2, axis=1)[:mask.shape[0], :mask.shape[1]]
    for _ in range(3):
        keep = _dilate(keep)
    out = rgba.copy()
    out[..., 3] = a * keep
    return out


def rounded_box_mask(size, inset, radius=0.22, feather=0.022):
    """Feathered squircle mask used to shave off a card's own bevel."""
    gy, gx = np.mgrid[0:size, 0:size].astype(np.float32)
    c = (size - 1) / 2.0
    m = inset * size
    r = radius * size
    half = c - m - r
    qx = np.abs(gx - c) - half
    qy = np.abs(gy - c) - half
    d = (np.sqrt(np.maximum(qx, 0) ** 2 + np.maximum(qy, 0) ** 2)
         + np.minimum(np.maximum(qx, qy), 0) - r)
    return np.clip(0.5 - d / (feather * size), 0, 1)


def strip_background(rgba, field, residual, inset):
    """Erase the background the model describes, softly and only where it is
    actually background — then un-composite the artwork's edges and shave the
    card's bevel, which our own tile replaces.
    """
    rgb, a = rgba[..., :3], rgba[..., 3]
    dist = np.abs(rgb - field).max(axis=-1)
    t0 = max(0.06, residual * 2.6)
    t1 = t0 * 3.0
    hard = (dist < t0) | (a < 0.5)
    region = border_connected(hard)
    # The counter of an "A" is the card showing through the letter, not part of
    # it — so background colour trapped inside the artwork goes too.  The
    # tighter threshold keeps it from eating a logo that merely sits close to
    # its card, like Wilber's cream fur on white.
    region |= (dist < 0.6 * t0) & (a >= 0.5)
    for _ in range(6):
        region = _dilate(region)          # reach into the antialiased fringe
    # Squared ramp: artwork sits far from its card, so anything only slightly
    # off-background is the card's own soft edge or shadow and should go
    # cleanly, instead of surviving as a bright haze around the logo.
    soft = np.clip((dist - t0) / max(1e-4, t1 - t0), 0, 1) ** 2.0

    out = rgba.copy()
    new_a = np.where(region, a * soft, a)

    # Matting: an antialiased edge pixel is part logo, part card.  Solve the
    # card back out of it, or every logo keeps a bright halo of its old
    # background — which is exactly what makes a naive cut-out look cheap.
    cov = np.clip(np.where(a > 1e-3, new_a / np.maximum(a, 1e-3), 0.0), 0, 1)
    edge = (cov > 0.15) & (cov < 0.996)      # below 0.15 the division only amplifies noise
    if edge.any():
        c = cov[..., None]
        recovered = (rgb - (1.0 - c) * field) / np.maximum(c, 0.15)
        out[..., :3] = np.where(edge[..., None], np.clip(recovered, 0, 1), rgb)

    # A card found further in has its own bevel further in too, so cut deeper.
    clean_inset = 0.075 if inset <= 0.055 else min(inset + 0.055, 0.15)
    out[..., 3] = new_a * rounded_box_mask(rgba.shape[0], clean_inset)
    return clean_fragments(out, dist, t0)


# --------------------------------------------------------------------------
# art treatments
# --------------------------------------------------------------------------

def flip_neutral_tones(rgba):
    """Turn a light sheet dark while keeping the marks on it legible.

    Only neutral tones flip — white paper goes dark, dark ink goes light.
    Anything with colour in it keeps its hue and roughly its weight, so brand
    marks survive the change of paper.  Crushing neutrals to black instead (the
    obvious move) erases the drawing along with the background.
    """
    hsv = rgb_to_hsv(rgba[..., :3])
    h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    w = np.clip((0.24 - s) / 0.24, 0, 1)          # 1 = neutral, 0 = saturated
    v_flip = 0.15 + 0.64 * (1.0 - v)
    v_col = v * (0.72 + 0.28 * np.clip(s, 0, 1))
    v2 = v_flip * w + v_col * (1 - w)
    out = rgba.copy()
    out[..., :3] = hsv_to_rgb(
        np.stack([h, np.clip(s * 1.1, 0, 1), np.clip(v2, 0, 1)], axis=-1))
    return out


def grade_complex_art(rgba):
    """Dark-mode treatment for illustrations we can't cleanly separate.

    Light-dominant artwork gets its neutrals flipped, which is what actually
    reads as a dark redesign.  Artwork that is already dark is left alone —
    darkening it further is how a set ends up full of black rectangles.
    """
    hsv = rgb_to_hsv(rgba[..., :3])
    v = hsv[..., 2]
    opaque = rgba[..., 3] > 0.5
    if opaque.sum() < 100:
        return rgba
    if float(np.median(v[opaque])) > 0.52:
        return flip_neutral_tones(rgba)

    out = rgba.copy()
    out[..., :3] = hsv_to_rgb(
        np.stack([hsv[..., 0], np.clip(hsv[..., 1] * 1.1, 0, 1), v], axis=-1))
    return out


def subject_stats(rgba):
    a = rgba[..., 3]
    m = a > 0.35
    if m.sum() < 40:
        return None
    hsv = rgb_to_hsv(rgba[..., :3])
    w = a[m]
    lums = rgba[..., :3][m] @ LUM
    # Brightness questions get asked of solid pixels only — a semi-transparent
    # edge carries whatever the renderer blended there, not the artwork's colour.
    solid = a > 0.75
    core = (rgba[..., :3][solid] @ LUM) if solid.sum() >= 40 else lums

    cols = np.nonzero(a.max(0) > 0.12)[0]
    rows = np.nonzero(a.max(1) > 0.12)[0]
    bbox = (len(cols) * len(rows)) if len(cols) and len(rows) else 0
    return {
        "v": float((hsv[..., 2][m] * w).sum() / w.sum()),
        "s": float((hsv[..., 1][m] * w).sum() / w.sum()),
        "lum": float((lums * w).sum() / w.sum()),
        # How bright is the *brightest* part?  Artwork whose highlights are
        # still dim will disappear against a dark tile.
        "hi": float(np.percentile(core, 88)),
        # Typical brightness of the artwork's body.  A median ignores both the
        # stray bright fleck and the stray dark one, so it answers "is this
        # thing dark?" far more honestly than a mean or a tail fraction.
        "med": float(np.median(core)),
        # Is there anything bright in here at all?
        "bright": float((core > 0.55).mean()),
        # How completely does the shape fill its own bounding box?  A slab
        # answers ~0.95, a circle ~0.79, a glyph far less.
        "fill": float(int(m.sum()) / bbox) if bbox else 0.0,
        "coverage": float(m.mean()),
    }


def lift_dark_subject(rgba, st):
    """Rescue artwork that would vanish on a dark tile."""
    hsv = rgb_to_hsv(rgba[..., :3])
    h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    if st["s"] < 0.22 and st["bright"] < 0.04:
        # Nothing but dark monochrome: flip lightness, keep whatever hue exists.
        v2 = 1.0 - v * 0.88
    else:
        # Coloured, or dark with something bright already in it: raise the
        # floor so the dark mass reads, without negating what already works.
        v2 = 0.42 + v * 0.58
    out = rgba.copy()
    out[..., :3] = hsv_to_rgb(np.stack([h, np.clip(s, 0, 1), np.clip(v2, 0, 1)], axis=-1))
    return out


def dominant_color(rgba, fallback=None):
    """Alpha-weighted mean of the icon's most colourful pixels."""
    a = rgba[..., 3]
    hsv = rgb_to_hsv(rgba[..., :3])
    m = (a > 0.5) & (hsv[..., 1] > 0.25) & (hsv[..., 2] > 0.20)
    if m.sum() < 60:
        m = (a > 0.5) & (hsv[..., 1] > 0.10)
    if m.sum() < 60:
        return fallback
    # Pick the dominant hue bucket so mixed-colour logos don't average to mud.
    hues = hsv[..., 0][m]
    hist, _ = np.histogram(hues, bins=24, range=(0, 1))
    peak = int(hist.argmax())
    lo, hi = peak / 24.0, (peak + 1) / 24.0
    sel = m & (hsv[..., 0] >= lo) & (hsv[..., 0] < hi)
    if sel.sum() < 40:
        sel = m
    w = a[sel]
    return (rgba[..., :3][sel] * w[:, None]).sum(0) / w.sum()


# --------------------------------------------------------------------------
# framing
# --------------------------------------------------------------------------

def reframe(rgba):
    """Normalise how much of the tile the artwork occupies.

    Full-bleed art is left alone.  Art that crowds the tile edge is eased in,
    and stray postage-stamp logos are brought up to a sensible size.
    """
    size = rgba.shape[0]
    a = rgba[..., 3]
    cols = np.nonzero(a.max(0) > 0.12)[0]
    rows = np.nonzero(a.max(1) > 0.12)[0]
    if len(cols) == 0 or len(rows) == 0:
        return rgba, 1.0
    x0, x1 = int(cols[0]), int(cols[-1]) + 1
    y0, y1 = int(rows[0]), int(rows[-1]) + 1
    span = max(x1 - x0, y1 - y0) / size
    if span > 0.94:
        target = 0.90
    elif 0.06 < span < 0.52:
        target = 0.60
    else:
        return rgba, 1.0

    scale = target / span
    im = Image.fromarray((np.clip(rgba, 0, 1) * 255).astype(np.uint8), "RGBA")
    crop = im.crop((x0, y0, x1, y1))
    nw = max(1, round(crop.width * scale))
    nh = max(1, round(crop.height * scale))
    crop = crop.resize((nw, nh), Image.LANCZOS)
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    canvas.paste(crop, ((size - nw) // 2, (size - nh) // 2))
    return np.asarray(canvas, dtype=np.float32) / 255.0, scale


# --------------------------------------------------------------------------
# tile composition
# --------------------------------------------------------------------------

def tile_colors(tint):
    """Near-black tile carrying a whisper of the icon's own hue."""
    if tint is None:
        return "#2e2e33", "#101013"
    h, s, v = rgb_to_hsv(np.asarray(tint, dtype=np.float32))
    if s < 0.10 or v < 0.06:
        return "#2e2e33", "#101013"
    # Dark Mode still needs a visible material surface.  Going all the way to
    # black makes otherwise excellent artwork look pasted into a hole in the
    # Dock; a slightly lifted shoulder preserves the icon silhouette while the
    # lower edge remains decisively dark.
    s_top = float(min(s * 0.68, 0.38))
    s_bot = float(min(s * 0.80, 0.46))
    top = hsv_to_rgb(np.array([h, s_top, 0.19], dtype=np.float32))
    bot = hsv_to_rgb(np.array([h, s_bot, 0.065], dtype=np.float32))
    return hexcolor(top), hexcolor(bot)


def glow_color(dom):
    if dom is None:
        return "#8e8e93"
    h, s, v = rgb_to_hsv(np.asarray(dom, dtype=np.float32))
    return hexcolor(hsv_to_rgb(np.array([h, min(s * 1.05, 0.9), max(v, 0.55)], dtype=np.float32)))


SVG_TMPL = """<svg width="64" height="64" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <!-- Two-scale Apple shadow: a soft lift plus a tight contact shadow -->
    <filter id="d-shadow" x="-25%" y="-25%" width="150%" height="150%">
      <feDropShadow dx="0" dy="2.4" stdDeviation="2.8" flood-color="#000000" flood-opacity="0.38" />
      <feDropShadow dx="0" dy="1.0" stdDeviation="0.8" flood-color="#000000" flood-opacity="0.62" />
    </filter>

    <!-- Dark canvas, tinted with the icon's own hue -->
    <linearGradient id="d-bg" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="{top}" />
      <stop offset="100%" stop-color="{bot}" />
    </linearGradient>

    <!-- The glyph appears to light its own tile, faintly -->
    <radialGradient id="d-glow" cx="50%" cy="42%" r="52%">
      <stop offset="0%" stop-color="{glow}" stop-opacity="{glow_op}" />
      <stop offset="55%" stop-color="{glow}" stop-opacity="{glow_mid}" />
      <stop offset="100%" stop-color="{glow}" stop-opacity="0" />
    </radialGradient>

    <!-- A broad, almost invisible glass reflection over the upper shoulder -->
    <radialGradient id="d-sheen" cx="22%" cy="4%" r="82%" fx="22%" fy="4%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.105" />
      <stop offset="48%" stop-color="#ffffff" stop-opacity="0.022" />
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0" />
    </radialGradient>

    <!-- Hairline rim: the top catches light while the bottom recedes -->
    <linearGradient id="d-rim" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.34" />
      <stop offset="34%" stop-color="#ffffff" stop-opacity="0.10" />
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0.025" />
    </linearGradient>

    <linearGradient id="d-floor" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#000000" stop-opacity="0" />
      <stop offset="58%" stop-color="#000000" stop-opacity="0" />
      <stop offset="100%" stop-color="#000000" stop-opacity="0.28" />
    </linearGradient>

    <clipPath id="d-clip">
      <rect width="56" height="56" x="4" y="4" rx="14" ry="14" />
    </clipPath>
  </defs>

  <g filter="url(#d-shadow)">
    <rect width="56" height="56" x="4" y="4" rx="14" ry="14" fill="url(#d-bg)" />
  </g>

  <g clip-path="url(#d-clip)">
    <!-- Surface lighting always stays behind the artwork.  Brand colours must
         never be dimmed by a generic overlay. -->
    <rect width="56" height="56" x="4" y="4" fill="url(#d-floor)" />
    <rect width="56" height="56" x="4" y="4" fill="url(#d-glow)" />
    <rect width="56" height="56" x="4" y="4" fill="url(#d-sheen)" />
    <image href="{href}" x="{ix}" y="{iy}" width="{iw}" height="{ih}" />
  </g>

  <rect width="55.5" height="55.5" x="4.25" y="4.25" rx="13.75" ry="13.75" fill="none" stroke="#000000" stroke-opacity="0.34" stroke-width="0.5" />
  <rect width="54.5" height="54.5" x="4.75" y="4.75" rx="13.25" ry="13.25" fill="none" stroke="url(#d-rim)" stroke-width="0.75" />
</svg>"""


def compose(href, tint, dom, glow_strength=1.0, box=(0, 0, 64, 64)):
    top, bot = tile_colors(tint)
    return SVG_TMPL.format(
        top=top,
        bot=bot,
        glow=glow_color(dom),
        glow_op="%.3f" % (0.11 * glow_strength),
        glow_mid="%.3f" % (0.040 * glow_strength),
        href=href,
        ix=box[0], iy=box[1], iw=box[2], ih=box[3],
    )


def png_href(rgba):
    im = Image.fromarray((np.clip(rgba, 0, 1) * 255 + 0.5).astype(np.uint8), "RGBA")
    buf = io.BytesIO()
    im.save(buf, format="PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


def wrap_png(data):
    """Minimal SVG around a PNG, for sources that carry an .svg name."""
    href = "data:image/png;base64," + base64.b64encode(data).decode()
    return ('<svg width="64" height="64" viewBox="0 0 64 64" '
            'xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">'
            f'<image href="{href}" x="0" y="0" width="64" height="64"/></svg>')


def raw_href(data, is_png):
    mime = "image/png" if is_png else "image/svg+xml"
    return f"data:{mime};base64," + base64.b64encode(data).decode()


# --------------------------------------------------------------------------
# main per-icon pipeline
# --------------------------------------------------------------------------

def build_dark(art, is_png, fallback=None, verbose=False):
    """Return (svg_text, mode) for one icon's source artwork.

    A few light icons embed artwork that will not render on its own; for those
    the already-composed light icon is rasterised instead.
    """
    rgba = rasterize(art, is_png)
    if (rgba is None or rgba[..., 3].max() < 0.05) and fallback is not None:
        alt = rasterize(fallback, False)
        if alt is not None and alt[..., 3].max() >= 0.05:
            rgba, art, is_png = alt, fallback, False
    if rgba is None:
        return None, "fail"

    size = rgba.shape[0]
    alpha = rgba[..., 3]
    if alpha.max() < 0.05:
        return None, "empty"

    ring, inset = find_background_ring(alpha, size)
    mode = "asis"
    tint = None
    stripped = None
    untouched = True

    if ring is not None:
        fit = fit_background(rgba[..., :3], alpha, ring)
        if fit is not None:
            field, residual, bg_mean = fit
            bg_lum = float(np.asarray(bg_mean) @ LUM)
            if residual >= 0.06:
                # We never understood the background, so don't pretend we did.
                mode = "grade"
            elif bg_lum < 0.28:
                mode = "already-dark"          # terminal, OBS, IDEs — leave alone
                tint = bg_mean
            else:
                cand = strip_background(rgba, field, residual, inset)
                before = float(alpha.mean())
                after = float(cand[..., 3].mean())
                removed = before - after
                if after > 0.025 and removed > 0.12 and after / max(before, 1e-6) < 0.90:
                    stripped = cand
                    mode = "strip"
                    tint = bg_mean
                    untouched = False
                else:
                    mode = "grade"

    work = stripped if stripped is not None else rgba
    if mode == "grade":
        work = grade_complex_art(rgba)
        untouched = False
        tint = dominant_color(work)

    st = subject_stats(work)
    if st is None:
        return None, "empty"

    # Cutting one card away sometimes just uncovers another one underneath: a
    # bright slab filling the tile, which reads as a light icon in a dark set.
    # Judged by shape, so a big round white logo is left as the logo it is.
    if mode == "strip" and st["fill"] > 0.80 and st["coverage"] > 0.42 and st["lum"] > 0.62:
        work = flip_neutral_tones(work)
        st = subject_stats(work)

    # Otherwise rescue artwork that would be invisible against a dark tile.
    elif mode in ("asis", "strip") and st["med"] < 0.42:
        work = lift_dark_subject(work, st)
        untouched = False
        st = subject_stats(work)

    dom = dominant_color(work, fallback=tint)
    if tint is None:
        tint = dom

    work, scale = reframe(work)
    if scale != 1.0:
        untouched = False

    # Glyph-on-a-card icons get a stronger halo; full-bleed art needs almost none.
    glow_strength = 1.0 if st["coverage"] < 0.55 else 0.45
    if mode == "already-dark":
        glow_strength = 0.35

    href = raw_href(art, is_png) if untouched else png_href(work)
    svg = compose(href, tint, dom, glow_strength=glow_strength)
    return svg, mode


# --------------------------------------------------------------------------
# hand-drawn dark icons
# --------------------------------------------------------------------------

def dark_calendar_svg(weekday, day):
    """Native dark Calendar — dark tile, Apple system red, white numeral."""
    body = f"""    <g>
    <text x="32" y="21.5" font-family="-apple-system, BlinkMacSystemFont, SF Pro Text, Inter, Roboto, sans-serif" font-weight="600" font-size="11.5" fill="#ff453a" text-anchor="middle">{weekday}</text>
    <text x="32" y="49" font-family="-apple-system, BlinkMacSystemFont, SF Pro Display, Inter, Roboto, sans-serif" font-weight="600" font-size="28" fill="#f2f2f7" text-anchor="middle">{day}</text>
    </g>"""
    return HD.tile(body, top="#303034", bottom="#111114",
                   glow=("#ff453a", 0.055))


def dark_text_editor_svg():
    """Native dark notepad — charcoal paper, amber header, pencil at full colour."""
    defs = """
    <linearGradient id="d-header" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#eab308" />
      <stop offset="100%" stop-color="#b8860b" />
    </linearGradient>"""
    body = """    <g>
    <rect width="56" height="12" x="4" y="4" fill="url(#d-header)" />

    <line x1="12" y1="22" x2="52" y2="22" stroke="#eab308" stroke-width="1" opacity="0.34" />
    <line x1="12" y1="29" x2="52" y2="29" stroke="#eab308" stroke-width="1" opacity="0.34" />
    <line x1="12" y1="36" x2="52" y2="36" stroke="#eab308" stroke-width="1" opacity="0.34" />
    <line x1="12" y1="43" x2="52" y2="43" stroke="#eab308" stroke-width="1" opacity="0.34" />
    <line x1="12" y1="50" x2="52" y2="50" stroke="#eab308" stroke-width="1" opacity="0.34" />

    <g transform="translate(18, 12) rotate(-35)">
      <rect x="0" y="0" width="6" height="30" rx="1" fill="#f97316" />
      <path d="M 0 30 L 3 36 L 6 30 Z" fill="#fde047" />
      <path d="M 2 34 L 3 36 L 4 34 Z" fill="#e2e8f0" />
      <rect x="0" y="-3" width="6" height="3" fill="#cbd5e1" />
      <rect x="0" y="-7" width="6" height="4" rx="1" fill="#f43f5e" />
    </g>
    </g>"""
    return HD.tile(body, top="#302b23", bottom="#12100c",
                   defs=defs, glow=("#eab308", 0.07))


def dark_mono_glyph_svg(art, is_png, top, bottom, glow):
    """Re-ink a black-on-white logo as a white one.

    Cutting the white card away leaves a grey halo on the mark's antialiased
    edges.  Reading the card's own luminance as the glyph's alpha instead
    gives a mark with no halo at all — the strands stay as crisp as the
    original, they just change colour.
    """
    rgba = rasterize(art, is_png)
    if rgba is None:
        return None
    lum = rgba[..., :3] @ LUM
    alpha = rgba[..., 3] * np.clip(1.0 - lum, 0.0, 1.0)
    alpha = np.clip((alpha - 0.10) / 0.80, 0.0, 1.0)

    glyph = np.zeros_like(rgba)
    glyph[..., :3] = 1.0
    glyph[..., 3] = alpha
    glyph, _ = reframe(glyph)

    # Inset to the tile itself, so the mark keeps a margin like a logo on a
    # card rather than running off the corners.
    body = f'    <image href="{png_href(glyph)}" x="9" y="9" width="46" height="46" />'
    return HD.tile(body, top=top, bottom=bottom, glow=glow)


CALENDAR_NAMES = {
    "calendar.svg", "org.gnome.Calendar.svg", "org.gnome.calendar.svg",
    "gnome-calendar.svg", "google-calendar.svg", "web-google-calendar.svg",
    "unity-webapps-google-calendar.svg", "office-calendar.svg", "stock_calendar.svg",
    "vcalendar.svg", "x-office-calendar.svg", "xfcalendar.svg", "dde-calendar.svg",
    "deepin-calendar.svg", "evolution-calendar.svg", "io.elementary.calendar.svg",
    "org.deepin.flatdeb.deepin-calendar.svg", "org.kde.plasma.calendar.svg",
    "preferences-calendar-and-tasks.svg", "solstice-microsoft-outlook-calendar.svg",
    "starcal2.svg", "ximian-evolution-calendar.svg", "calendar-blue-31.svg",
    "calendar-red-31.svg",
}


def is_finder(name):
    return name.lower() in {"finder.svg", "apple-finder.svg", "mac-finder.svg", "finder-mac.svg"}


def is_gemini(name):
    return name.lower() in {
        "gemini.svg", "com.google.gemini.svg", "google-gemini.svg",
        "google-gemini-desktop.svg", "gemini-cli.svg",
    }



# --------------------------------------------------------------------------
# source extraction
# --------------------------------------------------------------------------

def source_art(path):
    """Get the original artwork behind a light-mode icon.

    The light engine wraps the original inside a data URI; hand-drawn icons
    have no embedded image, in which case the file itself is the artwork.
    """
    data = path.read_bytes()
    if data.startswith(b"\x89PNG"):
        return data, True
    try:
        text = data.decode("utf-8", errors="ignore")
    except Exception:
        return data, False
    m = re.search(r'<image[^>]*?href="(data:[^"]+)"', text)
    if m:
        header, b64 = m.group(1).split(",", 1)
        try:
            return base64.b64decode(b64), "image/png" in header
        except Exception:
            pass
    return data, False


# --------------------------------------------------------------------------
# driver
# --------------------------------------------------------------------------

def process(names=None, out_dir=None, verbose=False):
    out_dir = Path(out_dir) if out_dir else DARK_DIR
    out_dir.mkdir(parents=True, exist_ok=True)

    now = datetime.datetime.now()
    cal_svg = dark_calendar_svg(now.strftime("%a"), str(now.day))

    # Icons whose card *is* their artwork get a hand-drawn dark counterpart
    # rather than an automatic one.  Keyed on artwork, so every alias that
    # embeds the same drawing (nautilus.svg, chatgpt-desktop.svg, …) picks it
    # up too.
    def art_key(path):
        art, _ = source_art(path)
        return hashlib.md5(art).hexdigest()

    handdrawn = {}
    builders = {"accessories-text-editor.svg": dark_text_editor_svg,
                "calendar.svg": lambda: cal_svg}
    builders.update(HD.HANDDRAWN)
    for src, build in builders.items():
        p = LIGHT_DIR / src
        if p.exists():
            handdrawn[art_key(p)] = build()

    # ChatGPT is drawn from its own artwork rather than by hand: the knot is
    # too intricate to redraw, but it is pure black ink and re-inks cleanly.
    p = LIGHT_DIR / "chatgpt.svg"
    if p.exists():
        art, is_png = source_art(p)
        svg = dark_mono_glyph_svg(art, is_png, "#26262b", "#0b0b0d", ("#ffffff", 0.06))
        if svg:
            handdrawn[art_key(p)] = svg

    # Artwork explicitly registered as verbatim reaches dark mode untouched.
    verbatim = set()
    for src in HD.VERBATIM:
        p = LIGHT_DIR / src
        if p.exists():
            verbatim.add(art_key(p))

    if names:
        files = []
        for n in names:
            p = LIGHT_DIR / (n if n.endswith((".svg", ".png")) else n + ".svg")
            if p.exists():
                files.append(p)
    else:
        files = sorted(p for p in LIGHT_DIR.iterdir() if p.is_file() and not p.is_symlink())

    stats = {}
    failed = []
    for p in files:
        name = p.name
        target = out_dir / (p.stem + ".svg")
        try:
            if name in CALENDAR_NAMES:
                target.write_text(cal_svg, encoding="utf-8")
                stats["calendar"] = stats.get("calendar", 0) + 1
                continue

            named_builder = HD.NAME_HANDDRAWN.get(name)
            if named_builder:
                target.write_text(named_builder(), encoding="utf-8")
                stats["name-repair"] = stats.get("name-repair", 0) + 1
                continue

            art, is_png = source_art(p)
            key = hashlib.md5(art).hexdigest()

            if key in verbatim or is_gemini(name):
                # Kept as-is: exact official artwork, or already dark by spec.
                # A couple of these are PNGs carrying an .svg name, so wrap
                # rather than copy — otherwise the file will not render at all.
                raw = p.read_bytes()
                if raw.startswith(b"\x89PNG"):
                    target.write_text(wrap_png(raw), encoding="utf-8")
                else:
                    target.write_bytes(raw)
                stats["verbatim"] = stats.get("verbatim", 0) + 1
                continue

            hand = handdrawn.get(key)
            if hand:
                target.write_text(hand, encoding="utf-8")
                stats["handdrawn"] = stats.get("handdrawn", 0) + 1
                continue

            light = p.read_bytes()
            svg, mode = build_dark(art, is_png,
                                   fallback=None if light is art else light,
                                   verbose=verbose)
            if svg is None:
                # Never leave a hole in the theme: fall back to the light icon.
                target.write_bytes(light)
                failed.append((name, mode))
                stats["fail"] = stats.get("fail", 0) + 1
                continue
            target.write_text(svg, encoding="utf-8")
            stats[mode] = stats.get(mode, 0) + 1
            if verbose:
                print(f"  {name:48s} {mode}")
        except Exception as e:
            failed.append((name, repr(e)))
            stats["fail"] = stats.get("fail", 0) + 1

    if not names:
        # Mirror the light theme's aliases so every app name still resolves.
        for p in LIGHT_DIR.iterdir():
            if not p.is_symlink():
                continue
            link = out_dir / p.name
            if link.exists() or link.is_symlink():
                continue
            try:
                os.symlink(os.readlink(p), link)
                stats["alias"] = stats.get("alias", 0) + 1
            except Exception:
                pass

    return stats, failed


def main():
    ap = argparse.ArgumentParser(description="Apple-style dark mode icon generator")
    ap.add_argument("--only", help="comma separated icon names to build")
    ap.add_argument("--out", help="output directory (default apps-dark/scalable)")
    ap.add_argument("-v", "--verbose", action="store_true")
    ap.add_argument("--no-cache", action="store_true", help="skip icon cache refresh")
    args = ap.parse_args()

    names = [n.strip() for n in args.only.split(",")] if args.only else None
    stats, failed = process(names=names, out_dir=args.out, verbose=args.verbose)

    print("\nDark icons built:")
    for k in sorted(stats):
        print(f"  {k:14s} {stats[k]}")
    if failed:
        print(f"\n{len(failed)} failed:")
        for n, why in failed[:20]:
            print(f"  {n}: {why}")

    if not args.out and not args.no_cache:
        subprocess.run("touch macos-icons-dark/.icon-theme.cache 2>/dev/null", shell=True, cwd=REPO)
        subprocess.run("gtk-update-icon-cache -f -t macos-icons-dark 2>/dev/null", shell=True, cwd=REPO)


if __name__ == "__main__":
    main()
