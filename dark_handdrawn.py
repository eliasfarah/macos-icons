#!/usr/bin/env python3
"""
dark_handdrawn.py — hand-drawn dark variants.

The automatic pipeline in mac_dark_engine.py works by cutting the light card
away from the artwork.  That only works when the card and the artwork are
different things.  Where the card *is* the artwork (Finder's face, the App
Store "A", a full-bleed photo) the cut leaves a ragged hole, so those icons
get drawn here instead.

Every icon uses the same tile as light mode — 56x56 squircle at (4,4),
radius 14 — with a near-black gradient tinted by the icon's own hue, a
hairline top rim and an outer shadow.
"""

# --------------------------------------------------------------------------
# shared tile
# --------------------------------------------------------------------------

def tile(body, top="#2e2e33", bottom="#101013", defs="", glow=None, filter_shadow=True):
    """Wrap `body` (clipped to the tile) in the standard dark card.

    glow: (colour, opacity) for a soft radial bloom behind the artwork — the
    glyph reads as if it were lighting its own tile.
    """
    glow_defs = glow_body = ""
    if glow:
        colour, op = glow
        glow_defs = f"""
    <radialGradient id="d-glow" cx="50%" cy="44%" r="56%">
      <stop offset="0%" stop-color="{colour}" stop-opacity="{op}" />
      <stop offset="55%" stop-color="{colour}" stop-opacity="{op * 0.35:.4f}" />
      <stop offset="100%" stop-color="{colour}" stop-opacity="0" />
    </radialGradient>"""
        glow_body = '<rect width="56" height="56" x="4" y="4" fill="url(#d-glow)" />'
    glow_line = f"    {glow_body}" if glow_body else ""

    return f"""<svg width="64" height="64" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <filter id="d-shadow" x="-25%" y="-25%" width="150%" height="150%">
      <feDropShadow dx="0" dy="2.4" stdDeviation="2.8" flood-color="#000000" flood-opacity="0.38" />
      <feDropShadow dx="0" dy="1.0" stdDeviation="0.8" flood-color="#000000" flood-opacity="0.62" />
    </filter>
    <linearGradient id="d-bg" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="{top}" />
      <stop offset="100%" stop-color="{bottom}" />
    </linearGradient>
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
    <radialGradient id="d-sheen" cx="22%" cy="4%" r="82%" fx="22%" fy="4%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.105" />
      <stop offset="48%" stop-color="#ffffff" stop-opacity="0.022" />
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0" />
    </radialGradient>
    <clipPath id="d-clip">
      <rect width="56" height="56" x="4" y="4" rx="14" ry="14" />
    </clipPath>{glow_defs}{defs}
  </defs>

  <g filter="url(#d-shadow)">
    <rect width="56" height="56" x="4" y="4" rx="14" ry="14" fill="url(#d-bg)" />
  </g>

  <g clip-path="url(#d-clip)">
    <rect width="56" height="56" x="4" y="4" fill="url(#d-floor)" />
{glow_line}
    <rect width="56" height="56" x="4" y="4" fill="url(#d-sheen)" />
{body}
  </g>

  <rect width="55.5" height="55.5" x="4.25" y="4.25" rx="13.75" ry="13.75" fill="none" stroke="#000000" stroke-opacity="0.34" stroke-width="0.5" />
  <rect width="54.5" height="54.5" x="4.75" y="4.75" rx="13.25" ry="13.25" fill="none" stroke="url(#d-rim)" stroke-width="0.75" />
</svg>"""


def _light_image_href(filename):
    """Return the self-contained image data URI from a light source icon."""
    import re
    from pathlib import Path

    source = (Path(__file__).resolve().parent / "apps" / "scalable" / filename)
    content = source.read_text(encoding="utf-8")
    match = re.search(r'<image\b[^>]*\bhref="(data:image/[^\"]+)"', content)
    if not match:
        raise ValueError(f"no embedded image found in {source}")
    return match.group(1)


# --------------------------------------------------------------------------
# finder / remote connections
# --------------------------------------------------------------------------

def dark_finder_svg():
    """Finder: compact blue face floating over a graphite Liquid Glass tile."""
    defs = """
    <filter id="finder-face-shadow" x="-35%" y="-25%" width="180%" height="175%">
      <feDropShadow dx="0" dy="1.45" stdDeviation="1.35" flood-color="#05060a" flood-opacity="0.72" />
      <feDropShadow dx="0" dy="0" stdDeviation="0.42" flood-color="#248eff" flood-opacity="0.30" />
    </filter>
    <filter id="finder-eye-shadow" x="-90%" y="-40%" width="280%" height="190%">
      <feDropShadow dx="0" dy="0.55" stdDeviation="0.42" flood-color="#000000" flood-opacity="0.68" />
    </filter>
    <filter id="finder-smile-shadow" x="-20%" y="-65%" width="140%" height="230%">
      <feDropShadow dx="0" dy="0.65" stdDeviation="0.48" flood-color="#000000" flood-opacity="0.82" />
    </filter>
    <linearGradient id="finder-card" gradientUnits="userSpaceOnUse" x1="32" y1="4" x2="32" y2="60">
      <stop offset="0%" stop-color="#2c2c2e" />
      <stop offset="56%" stop-color="#242426" />
      <stop offset="100%" stop-color="#19191b" />
    </linearGradient>
    <radialGradient id="finder-card-sheen" cx="24%" cy="5%" r="86%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.075" />
      <stop offset="58%" stop-color="#ffffff" stop-opacity="0.012" />
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0" />
    </radialGradient>
    <linearGradient id="finder-face" gradientUnits="userSpaceOnUse" x1="38" y1="11" x2="38" y2="56">
      <stop offset="0%" stop-color="#24b9f1" />
      <stop offset="31%" stop-color="#3199ef" />
      <stop offset="65%" stop-color="#315fce" />
      <stop offset="100%" stop-color="#293f9f" />
    </linearGradient>
    <linearGradient id="finder-face-edge" gradientUnits="userSpaceOnUse" x1="36" y1="11" x2="42" y2="56">
      <stop offset="0%" stop-color="#7ce3ff" stop-opacity="0.72" />
      <stop offset="42%" stop-color="#2877df" stop-opacity="0.52" />
      <stop offset="100%" stop-color="#19296d" stop-opacity="0.88" />
    </linearGradient>
    <linearGradient id="finder-face-gloss" gradientUnits="userSpaceOnUse" x1="38" y1="12" x2="38" y2="34">
      <stop offset="0%" stop-color="#d9f9ff" stop-opacity="0.065" />
      <stop offset="48%" stop-color="#9feaff" stop-opacity="0.015" />
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0" />
    </linearGradient>
    <linearGradient id="finder-left-eye" gradientUnits="userSpaceOnUse" x1="17" y1="22" x2="19" y2="29">
      <stop offset="0%" stop-color="#37b8ff" />
      <stop offset="100%" stop-color="#2b68e0" />
    </linearGradient>
    <linearGradient id="finder-right-eye" gradientUnits="userSpaceOnUse" x1="40" y1="22" x2="42" y2="29">
      <stop offset="0%" stop-color="#17334e" />
      <stop offset="100%" stop-color="#08111e" />
    </linearGradient>
    <linearGradient id="finder-smile" gradientUnits="userSpaceOnUse" x1="14.4" y1="45" x2="44.7" y2="45">
      <stop offset="0%" stop-color="#329cff" />
      <stop offset="42%" stop-color="#376ce5" />
      <stop offset="55%" stop-color="#283f79" />
      <stop offset="68%" stop-color="#17243a" />
      <stop offset="100%" stop-color="#0b111a" />
    </linearGradient>"""
    body = """    <rect x="4" y="4" width="56" height="56" fill="url(#finder-card)" />
    <rect x="4" y="4" width="56" height="56" fill="url(#finder-card-sheen)" />
    <g filter="url(#finder-face-shadow)">
      <path d="M34.45 11.4 H45.55
               C49.82 11.4 52.35 14.26 52.35 18.72
               V47.05 C52.35 52.28 49.25 55.45 44.82 55.45
               H36.08 C32.82 55.45 30.62 53.38 30.62 50.18
               V36.6 H26.35
               C24.68 36.6 23.86 35.52 24.34 33.62
               L29.66 14.58 C30.2 12.47 31.7 11.4 34.45 11.4 Z"
            fill="url(#finder-face)" stroke="url(#finder-face-edge)"
            stroke-width="0.72" stroke-linejoin="round" />
      <path d="M34.35 12.18 H45.25 C49.2 12.18 51.58 14.72 51.72 18.25
               C44.55 15.9 37.05 16.2 28.92 19.48 L30.28 14.72
               C30.7 13.08 32.05 12.18 34.35 12.18 Z"
            fill="url(#finder-face-gloss)" />
      <path d="M30.92 36.88 V50.05 C30.92 52.92 32.82 54.73 36.02 54.73"
            fill="none" stroke="#16276c" stroke-width="0.62"
            stroke-linecap="round" opacity="0.47" />
      <path d="M34.38 11.92 H45.22 C49.25 11.92 51.75 14.48 52.02 18.15"
            fill="none" stroke="#c6f5ff" stroke-width="0.58"
            stroke-linecap="round" opacity="0.31" />
    </g>
    <g filter="url(#finder-eye-shadow)">
      <rect x="17.68" y="22.72" width="1.92" height="5.25" rx="0.96"
            fill="url(#finder-left-eye)" />
      <path d="M18.16 23.2 V27.12" stroke="#8dd9ff" stroke-width="0.32"
            stroke-linecap="round" opacity="0.48" />
      <rect x="40.22" y="22.7" width="1.92" height="5.28" rx="0.96"
            fill="url(#finder-right-eye)" />
      <path d="M40.65 23.3 V27.14" stroke="#33516c" stroke-width="0.3"
            stroke-linecap="round" opacity="0.58" />
    </g>
    <path d="M14.4 41.92
             C21.75 47.95 27.45 49.48 32.62 49.08
             C37.52 48.72 41.53 45.58 44.7 41.82"
          fill="none" stroke="#060a10" stroke-width="2.08"
          stroke-linecap="round" opacity="0.82"
          filter="url(#finder-smile-shadow)" />
    <path d="M14.4 41.92
             C21.75 47.95 27.45 49.48 32.62 49.08
             C37.52 48.72 41.53 45.58 44.7 41.82"
          fill="none" stroke="url(#finder-smile)" stroke-width="1.58"
          stroke-linecap="round" />
    <path d="M15.02 42.04 C19.95 46.03 24.2 47.72 28.18 48.35"
          fill="none" stroke="#83bcff" stroke-width="0.34"
          stroke-linecap="round" opacity="0.36" />"""
    return tile(body, top="#2b2b2d", bottom="#171719", defs=defs)


def dark_connections_svg():
    """Connections: a precise glass globe, live route and sculpted cursor."""
    defs = """
    <filter id="conn-orb-shadow" x="-35%" y="-35%" width="170%" height="185%">
      <feDropShadow dx="0" dy="2.1" stdDeviation="2.0" flood-color="#00040b" flood-opacity="0.74" />
      <feDropShadow dx="0" dy="0" stdDeviation="0.65" flood-color="#52d9ff" flood-opacity="0.20" />
    </filter>
    <filter id="conn-cursor-shadow" x="-40%" y="-35%" width="190%" height="200%">
      <feDropShadow dx="0.8" dy="2.1" stdDeviation="1.65" flood-color="#000000" flood-opacity="0.78" />
    </filter>
    <filter id="conn-node-glow" x="-120%" y="-120%" width="340%" height="340%">
      <feGaussianBlur stdDeviation="1.25" result="blur" />
      <feMerge><feMergeNode in="blur" /><feMergeNode in="SourceGraphic" /></feMerge>
    </filter>
    <radialGradient id="conn-orb" cx="31%" cy="22%" r="82%">
      <stop offset="0%" stop-color="#25c8f3" />
      <stop offset="39%" stop-color="#0b8fd3" />
      <stop offset="73%" stop-color="#0758ae" />
      <stop offset="100%" stop-color="#062e71" />
    </radialGradient>
    <linearGradient id="conn-orb-rim" x1="18%" y1="5%" x2="82%" y2="100%">
      <stop offset="0%" stop-color="#d5faff" />
      <stop offset="42%" stop-color="#5bdcff" />
      <stop offset="100%" stop-color="#0c4f9d" />
    </linearGradient>
    <linearGradient id="conn-cursor" gradientUnits="userSpaceOnUse" x1="34" y1="15" x2="48" y2="42">
      <stop offset="0%" stop-color="#ffffff" />
      <stop offset="55%" stop-color="#e9f6ff" />
      <stop offset="100%" stop-color="#9fc7df" />
    </linearGradient>
    <linearGradient id="conn-cursor-edge" gradientUnits="userSpaceOnUse" x1="35" y1="15" x2="48" y2="43">
      <stop offset="0%" stop-color="#e8fbff" />
      <stop offset="100%" stop-color="#47738f" />
    </linearGradient>
    <clipPath id="conn-orb-clip"><circle cx="29.5" cy="33" r="21.15" /></clipPath>"""
    body = """    <g filter="url(#conn-orb-shadow)">
      <circle cx="29.5" cy="33" r="22" fill="#020b17" opacity="0.78" />
      <circle cx="29.5" cy="33" r="21.45" fill="url(#conn-orb-rim)" />
      <circle cx="29.5" cy="33" r="20.65" fill="url(#conn-orb)" />
    </g>
    <g clip-path="url(#conn-orb-clip)" fill="none" stroke="#a9efff"
       stroke-width="0.72" opacity="0.24">
      <ellipse cx="29.5" cy="33" rx="9.2" ry="20.8" />
      <ellipse cx="29.5" cy="33" rx="16.4" ry="20.8" />
      <path d="M8.8 33 H50.2" />
      <path d="M10.7 24.3 C20.8 27.7 38.2 27.7 48.3 24.3" />
      <path d="M10.7 41.7 C20.8 38.3 38.2 38.3 48.3 41.7" />
    </g>
    <path d="M11.3 21.4 C18.6 14.1 33.9 10.3 44.7 18.3"
          fill="none" stroke="#ffffff" stroke-width="1.2"
          stroke-linecap="round" opacity="0.20" />
    <path d="M13.6 41.7 C18.5 47.8 26.2 50.15 33.3 48.9
             C39.55 47.8 44.65 44.2 47.75 38.7"
          fill="none" stroke="#7ee9ff" stroke-width="1.42"
          stroke-linecap="round" stroke-dasharray="1.1 3.15" opacity="0.88" />
    <g fill="#d9fbff" stroke="#5adfff" stroke-width="0.55"
       filter="url(#conn-node-glow)">
      <circle cx="13.7" cy="41.7" r="1.7" />
      <circle cx="31.8" cy="49.1" r="1.35" />
      <circle cx="47.7" cy="38.7" r="1.7" />
    </g>
    <g filter="url(#conn-cursor-shadow)">
      <path d="M33.6 14.35 L52.05 28.85 L43.15 30.55
               L49.25 40.55 L44.2 43.6 L38.1 33.45 L32.15 40.2 Z"
            fill="#07121d" stroke="#02070d" stroke-width="2.45"
            stroke-linejoin="round" />
      <path d="M33.6 14.35 L52.05 28.85 L43.15 30.55
               L49.25 40.55 L44.2 43.6 L38.1 33.45 L32.15 40.2 Z"
            fill="url(#conn-cursor)" stroke="url(#conn-cursor-edge)"
            stroke-width="0.65" stroke-linejoin="round" />
      <path d="M35.15 17.35 L48.95 28.15 L41.15 29.65"
            fill="none" stroke="#ffffff" stroke-width="0.72"
            stroke-linecap="round" opacity="0.72" />
    </g>"""
    return tile(body, top="#102a42", bottom="#050b13",
                defs=defs, glow=("#19bfff", 0.15))


# --------------------------------------------------------------------------
# browsers / web
# --------------------------------------------------------------------------

def dark_chrome_svg():
    """Chrome keeps its full-colour wheel; only the white card goes dark."""
    defs = """
    <linearGradient id="c-red" x1="10%" y1="100%" x2="80%" y2="0%">
      <stop offset="0%" stop-color="#d93025" />
      <stop offset="100%" stop-color="#ef5350" />
    </linearGradient>
    <linearGradient id="c-yellow" x1="0%" y1="0%" x2="60%" y2="100%">
      <stop offset="0%" stop-color="#ffcd42" />
      <stop offset="100%" stop-color="#f0a30a" />
    </linearGradient>
    <linearGradient id="c-green" x1="100%" y1="0%" x2="10%" y2="80%">
      <stop offset="0%" stop-color="#34a853" />
      <stop offset="100%" stop-color="#1e8e3e" />
    </linearGradient>
    <linearGradient id="c-blue" x1="20%" y1="0%" x2="80%" y2="100%">
      <stop offset="0%" stop-color="#65a2ff" />
      <stop offset="100%" stop-color="#1a73e8" />
    </linearGradient>"""
    # Three 120 degree sectors: red 180->300, yellow 300->60, green 60->180,
    # measured clockwise from 3 o'clock, which is how the wheel actually sits.
    body = """    <g>
      <path d="M 32 32 L 15 32 A 17 17 0 0 1 40.5 17.28 Z" fill="url(#c-red)" />
      <path d="M 32 32 L 40.5 17.28 A 17 17 0 0 1 40.5 46.72 Z" fill="url(#c-yellow)" />
      <path d="M 32 32 L 40.5 46.72 A 17 17 0 0 1 15 32 Z" fill="url(#c-green)" />
      <circle cx="32" cy="32" r="8.6" fill="#f4f5f7" />
      <circle cx="32" cy="32" r="7" fill="url(#c-blue)" />
      <path d="M 32 25 A 7 7 0 0 1 38.6 29.6 A 7 7 0 0 0 32 25 Z" fill="#ffffff" opacity="0.35" />
    </g>"""
    return tile(body, top="#252a31", bottom="#0b0d10",
                defs=defs, glow=("#4285f4", 0.10))


def dark_web_svg():
    """GNOME Web: luminous Safari-style compass made for the dark tile."""
    defs = """
    <filter id="web-shadow" x="-35%" y="-35%" width="170%" height="180%">
      <feDropShadow dx="0" dy="2" stdDeviation="2" flood-color="#000814" flood-opacity="0.72" />
    </filter>
    <linearGradient id="web-rim" x1="16%" y1="4%" x2="86%" y2="96%">
      <stop offset="0%" stop-color="#d9f7ff" />
      <stop offset="28%" stop-color="#72d8ff" />
      <stop offset="70%" stop-color="#238ed9" />
      <stop offset="100%" stop-color="#0a4d8c" />
    </linearGradient>
    <radialGradient id="web-dial" cx="34%" cy="25%" r="76%">
      <stop offset="0%" stop-color="#51d3ff" />
      <stop offset="48%" stop-color="#1aa7ec" />
      <stop offset="100%" stop-color="#0873c7" />
    </radialGradient>
    <linearGradient id="web-red" x1="20%" y1="100%" x2="80%" y2="0%">
      <stop offset="0%" stop-color="#e2293d" />
      <stop offset="100%" stop-color="#ff6658" />
    </linearGradient>
    <linearGradient id="web-pearl" x1="0%" y1="100%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#c9eaff" />
      <stop offset="62%" stop-color="#ffffff" />
      <stop offset="100%" stop-color="#e9f8ff" />
    </linearGradient>
    <g id="web-tick">
      <path d="M32 12.8V16.2" stroke="#f4fbff" stroke-width="1.35" stroke-linecap="round" />
    </g>"""
    ticks = "\n".join(
        f'      <use href="#web-tick" transform="rotate({angle} 32 32)" />'
        for angle in range(0, 360, 15)
    )
    body = f"""    <g filter="url(#web-shadow)">
      <circle cx="32" cy="32" r="23.1" fill="#071a2d" opacity="0.88" />
      <circle cx="32" cy="32" r="22.1" fill="url(#web-rim)" />
      <circle cx="32" cy="32" r="19.7" fill="url(#web-dial)" />
      <path d="M17.2 24.5A18.8 18.8 0 0 1 45.8 18.3"
            fill="none" stroke="#ffffff" stroke-width="1.5" opacity="0.35" />
      <g opacity="0.96">
{ticks}
      </g>
      <path d="M29.6 29.6L49.3 16.2L35 35Z" fill="url(#web-red)"
            stroke="#b4142a" stroke-width="0.35" stroke-linejoin="round" />
      <path d="M34.4 34.4L14.7 47.8L29 29Z" fill="url(#web-pearl)"
            stroke="#b9dbea" stroke-width="0.35" stroke-linejoin="round" />
      <circle cx="32" cy="32" r="2.7" fill="#edf9ff" opacity="0.95" />
      <circle cx="32" cy="32" r="1.45" fill="#163a58" />
    </g>"""
    return tile(body, top="#183149", bottom="#07111d",
                defs=defs, glow=("#31bfff", 0.16))


# --------------------------------------------------------------------------
# app store / software centre
# --------------------------------------------------------------------------

def dark_appstore_svg():
    """App Store: the official icy-white A on deep blue glass."""
    defs = """
    <filter id="store-glyph-shadow" x="-30%" y="-25%" width="160%" height="165%">
      <feDropShadow dx="0" dy="1.2" stdDeviation="1.05" flood-color="#000000" flood-opacity="0.78" />
      <feDropShadow dx="0" dy="0" stdDeviation="0.38" flood-color="#75c8ff" flood-opacity="0.34" />
    </filter>
    <linearGradient id="store-bar-edge" gradientUnits="userSpaceOnUse" x1="32" y1="15" x2="32" y2="49">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.94" />
      <stop offset="48%" stop-color="#7e9fbb" stop-opacity="0.84" />
      <stop offset="100%" stop-color="#466b91" stop-opacity="0.88" />
    </linearGradient>
    <linearGradient id="store-bar-horizontal" gradientUnits="userSpaceOnUse" x1="32" y1="35.4" x2="32" y2="41.1">
      <stop offset="0%" stop-color="#ffffff" />
      <stop offset="42%" stop-color="#e8f3f9" />
      <stop offset="100%" stop-color="#bfd3e4" />
    </linearGradient>
    <linearGradient id="store-bar-down" gradientUnits="userSpaceOnUse" x1="28.9" y1="17.4" x2="46.2" y2="46.5">
      <stop offset="0%" stop-color="#d9edf6" />
      <stop offset="30%" stop-color="#f4fbfe" />
      <stop offset="52%" stop-color="#bcd2e1" />
      <stop offset="72%" stop-color="#ffffff" />
      <stop offset="100%" stop-color="#cfdeeb" />
    </linearGradient>
    <linearGradient id="store-bar-up" gradientUnits="userSpaceOnUse" x1="17.8" y1="46.6" x2="35.1" y2="17.1">
      <stop offset="0%" stop-color="#d0deec" />
      <stop offset="34%" stop-color="#bdd2e2" />
      <stop offset="62%" stop-color="#ffffff" />
      <stop offset="100%" stop-color="#d9ebf4" />
    </linearGradient>"""
    body = """    <g filter="url(#store-glyph-shadow)" fill="none"
           stroke-linecap="round" stroke-linejoin="round">
      <g>
        <path d="M15.9 38.2H48.1" stroke="url(#store-bar-edge)" stroke-width="5.3" />
        <path d="M15.9 38.2H48.1" stroke="url(#store-bar-horizontal)" stroke-width="4.5" />
        <path d="M16.2 37.75H47.8" stroke="#ffffff" stroke-width="0.45" opacity="0.58" />
      </g>
      <g>
        <path d="M29.1 17.8L45.1 45.6" stroke="url(#store-bar-edge)" stroke-width="5.3" />
        <path d="M29.1 17.8L45.1 45.6" stroke="url(#store-bar-down)" stroke-width="4.5" />
        <path d="M28.82 18.15L44.82 45.25" stroke="#ffffff" stroke-width="0.44" opacity="0.46" />
      </g>
      <g>
        <path d="M35 17.8L18.9 45.6" stroke="url(#store-bar-edge)" stroke-width="5.3" />
        <path d="M35 17.8L18.9 45.6" stroke="url(#store-bar-up)" stroke-width="4.5" />
        <path d="M34.7 17.65L18.6 45.3" stroke="#ffffff" stroke-width="0.48" opacity="0.64" />
      </g>
    </g>"""
    return tile(body, top="#0d3470", bottom="#030816",
                defs=defs, glow=("#1687ff", 0.20))


# --------------------------------------------------------------------------
# add / remove software
# --------------------------------------------------------------------------

def dark_package_manager_svg():
    """A vivid software package with explicit add and remove controls."""
    defs = """
    <filter id="pkg-cube-shadow" x="-35%" y="-35%" width="170%" height="180%">
      <feDropShadow dx="0" dy="2.1" stdDeviation="2" flood-color="#000000" flood-opacity="0.56" />
    </filter>
    <filter id="pkg-badge-shadow" x="-45%" y="-45%" width="190%" height="195%">
      <feDropShadow dx="0" dy="1.5" stdDeviation="1.4" flood-color="#000000" flood-opacity="0.64" />
    </filter>
    <linearGradient id="pkg-top" x1="12%" y1="0%" x2="86%" y2="100%">
      <stop offset="0%" stop-color="#ca94ff" />
      <stop offset="100%" stop-color="#7059ee" />
    </linearGradient>
    <linearGradient id="pkg-left" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#68cdff" />
      <stop offset="100%" stop-color="#2775eb" />
    </linearGradient>
    <linearGradient id="pkg-right" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#9072ff" />
      <stop offset="100%" stop-color="#cf53dc" />
    </linearGradient>
    <linearGradient id="pkg-plus" x1="20%" y1="0%" x2="80%" y2="100%">
      <stop offset="0%" stop-color="#96f48a" />
      <stop offset="100%" stop-color="#24bd63" />
    </linearGradient>
    <linearGradient id="pkg-minus" x1="20%" y1="0%" x2="80%" y2="100%">
      <stop offset="0%" stop-color="#ffa08d" />
      <stop offset="100%" stop-color="#f05268" />
    </linearGradient>"""
    body = """    <g filter="url(#pkg-cube-shadow)" stroke="#ffffff"
           stroke-opacity="0.30" stroke-width="0.8" stroke-linejoin="round">
      <path d="M32 12L50 22L32 32L14 22Z" fill="url(#pkg-top)" />
      <path d="M14 22L32 32V52L14 42Z" fill="url(#pkg-left)" />
      <path d="M50 22L32 32V52L50 42Z" fill="url(#pkg-right)" />
      <path d="M25.5 15.6L43.5 25.6L38 28.7L20 18.7Z"
            fill="#ffffff" fill-opacity="0.30" stroke="none" />
      <path d="M27.4 34.3V43.9L21.6 40.7V31.1Z"
            fill="#ffffff" fill-opacity="0.84" stroke="none" />
      <path d="M35.7 34L45 28.8V32.6L35.7 37.8Z"
            fill="#ffffff" fill-opacity="0.24" stroke="none" />
    </g>
    <g filter="url(#pkg-badge-shadow)">
      <circle cx="48" cy="17.5" r="8.6" fill="url(#pkg-plus)" />
      <circle cx="48" cy="17.5" r="7.85" fill="none" stroke="#ffffff"
              stroke-opacity="0.62" stroke-width="0.8" />
      <path d="M48 13.4V21.6M43.9 17.5H52.1" stroke="#ffffff"
            stroke-width="2.5" stroke-linecap="round" />
    </g>
    <g filter="url(#pkg-badge-shadow)">
      <circle cx="16.5" cy="47" r="7.7" fill="url(#pkg-minus)" />
      <circle cx="16.5" cy="47" r="6.95" fill="none" stroke="#ffffff"
              stroke-opacity="0.60" stroke-width="0.8" />
      <path d="M12.7 47H20.3" stroke="#ffffff"
            stroke-width="2.5" stroke-linecap="round" />
    </g>"""
    return tile(body, top="#302447", bottom="#0b0910",
                defs=defs, glow=("#8a63ff", 0.20))


# --------------------------------------------------------------------------
# image viewer
# --------------------------------------------------------------------------

def dark_image_viewer_svg():
    """A framed photo at night, with the loupe kept in polished chrome."""
    defs = """
    <linearGradient id="iv-sky" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#1b3a63" />
      <stop offset="55%" stop-color="#2f6ea6" />
      <stop offset="100%" stop-color="#4f97c9" />
    </linearGradient>
    <linearGradient id="iv-sea" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#0f2d4a" />
      <stop offset="100%" stop-color="#071624" />
    </linearGradient>
    <linearGradient id="iv-ring" x1="0%" y1="0%" x2="30%" y2="100%">
      <stop offset="0%" stop-color="#f2f4f8" />
      <stop offset="45%" stop-color="#98a2b3" />
      <stop offset="100%" stop-color="#5b6472" />
    </linearGradient>
    <linearGradient id="iv-lens" x1="20%" y1="0%" x2="80%" y2="100%">
      <stop offset="0%" stop-color="#3d4a5c" />
      <stop offset="100%" stop-color="#161c26" />
    </linearGradient>
    <clipPath id="iv-photo">
      <rect x="11" y="14" width="42" height="31" rx="4" ry="4" />
    </clipPath>"""
    body = """    <g clip-path="url(#iv-photo)">
      <rect x="11" y="14" width="42" height="31" fill="url(#iv-sky)" />
      <circle cx="41" cy="22" r="3.4" fill="#ffe9b0" opacity="0.9" />
      <path d="M 11 33 L 21 25 L 30 33 L 37 28.5 L 53 38 L 53 45 L 11 45 Z" fill="#0d2138" />
      <rect x="11" y="36" width="42" height="9" fill="url(#iv-sea)" />
      <path d="M 11 36 L 53 36 L 53 38.5 L 11 38.5 Z" fill="#7fb4d8" opacity="0.35" />
    </g>
    <rect x="11" y="14" width="42" height="31" rx="4" ry="4" fill="none" stroke="#ffffff" stroke-opacity="0.16" stroke-width="1" />

    <g transform="translate(0.5, 1)">
      <path d="M 41.5 41.5 L 48.5 48.5" stroke="#6b7480" stroke-width="5.4" stroke-linecap="round" />
      <path d="M 41.5 41.5 L 48.5 48.5" stroke="#c7ced8" stroke-width="3" stroke-linecap="round" />
      <circle cx="33" cy="33" r="10.5" fill="url(#iv-ring)" />
      <circle cx="33" cy="33" r="8" fill="url(#iv-lens)" />
      <path d="M 27 29 A 8 8 0 0 1 36.5 26 A 9 9 0 0 0 27 29 Z" fill="#ffffff" opacity="0.55" />
    </g>"""
    return tile(body, top="#242a31", bottom="#0a0c0f",
                defs=defs, glow=("#4f97c9", 0.11))


# --------------------------------------------------------------------------
# loupe image viewer
# --------------------------------------------------------------------------

def dark_loupe_svg():
    """Loupe's eight-colour flower, preserved on a sapphire-black card."""
    defs = """
    <filter id="flower-shadow" x="-35%" y="-35%" width="170%" height="175%">
      <feDropShadow dx="0" dy="1.5" stdDeviation="1.5" flood-color="#000000" flood-opacity="0.48" />
    </filter>
    <linearGradient id="petal-orange" x1="18%" y1="0%" x2="78%" y2="100%">
      <stop offset="0%" stop-color="#ffb17a" />
      <stop offset="100%" stop-color="#ff6326" />
    </linearGradient>
    <linearGradient id="petal-yellow" x1="18%" y1="0%" x2="78%" y2="100%">
      <stop offset="0%" stop-color="#fff66e" />
      <stop offset="100%" stop-color="#f3c600" />
    </linearGradient>
    <linearGradient id="petal-green" x1="18%" y1="0%" x2="78%" y2="100%">
      <stop offset="0%" stop-color="#91f862" />
      <stop offset="100%" stop-color="#24c93a" />
    </linearGradient>
    <linearGradient id="petal-cyan" x1="18%" y1="0%" x2="78%" y2="100%">
      <stop offset="0%" stop-color="#51f0c8" />
      <stop offset="100%" stop-color="#00b7d8" />
    </linearGradient>
    <linearGradient id="petal-blue" x1="18%" y1="0%" x2="78%" y2="100%">
      <stop offset="0%" stop-color="#6fcbff" />
      <stop offset="100%" stop-color="#367ff1" />
    </linearGradient>
    <linearGradient id="petal-violet" x1="18%" y1="0%" x2="78%" y2="100%">
      <stop offset="0%" stop-color="#a17cff" />
      <stop offset="100%" stop-color="#6842e7" />
    </linearGradient>
    <linearGradient id="petal-magenta" x1="18%" y1="0%" x2="78%" y2="100%">
      <stop offset="0%" stop-color="#f176ff" />
      <stop offset="100%" stop-color="#c326da" />
    </linearGradient>
    <linearGradient id="petal-red" x1="18%" y1="0%" x2="78%" y2="100%">
      <stop offset="0%" stop-color="#ff7183" />
      <stop offset="100%" stop-color="#ee2949" />
    </linearGradient>
    <radialGradient id="loupe-heart" cx="35%" cy="28%" r="75%">
      <stop offset="0%" stop-color="#31558f" />
      <stop offset="100%" stop-color="#101a31" />
    </radialGradient>"""
    petal = ("M32 33C25.7 29 23.4 20.6 26.4 14.4"
             "C28.6 9.8 34.4 8.4 38.4 11.4C43 15 41.2 24.1 32 33Z")
    colours = (
        "petal-orange", "petal-yellow", "petal-green", "petal-cyan",
        "petal-blue", "petal-violet", "petal-magenta", "petal-red",
    )
    petals = "\n".join(
        f'      <path d="{petal}" fill="url(#{colour})"'
        + (f' transform="rotate({i * 45} 32 32)"' if i else "")
        + " />"
        for i, colour in enumerate(colours)
    )
    body = f"""    <g filter="url(#flower-shadow)">
{petals}
      <circle cx="32" cy="32" r="4.2" fill="url(#loupe-heart)" fill-opacity="0.88" />
      <ellipse cx="30.7" cy="30.7" rx="1.45" ry="1" fill="#ffffff" opacity="0.45"
               transform="rotate(-28 30.7 30.7)" />
    </g>"""
    return tile(body, top="#26304a", bottom="#090b12",
                defs=defs, glow=("#667cff", 0.16))


# --------------------------------------------------------------------------
# display manager settings / login screen
# --------------------------------------------------------------------------

def dark_login_svg():
    """A premium login panel with a compact settings badge for GDM tools."""
    defs = """
    <filter id="login-panel-shadow" x="-30%" y="-30%" width="160%" height="170%">
      <feDropShadow dx="0" dy="1.5" stdDeviation="1.7" flood-color="#000000" flood-opacity="0.48" />
    </filter>
    <filter id="login-badge-shadow" x="-45%" y="-45%" width="190%" height="195%">
      <feDropShadow dx="0" dy="1.4" stdDeviation="1.4" flood-color="#000000" flood-opacity="0.66" />
    </filter>
    <linearGradient id="login-frame" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#8ca8c8" />
      <stop offset="100%" stop-color="#40536d" />
    </linearGradient>
    <linearGradient id="login-screen" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#173f70" />
      <stop offset="100%" stop-color="#09192e" />
    </linearGradient>
    <linearGradient id="login-avatar" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#ffffff" />
      <stop offset="100%" stop-color="#cdd8e7" />
    </linearGradient>
    <linearGradient id="login-badge" x1="18%" y1="0%" x2="78%" y2="100%">
      <stop offset="0%" stop-color="#f6f9fd" />
      <stop offset="52%" stop-color="#bdc9d8" />
      <stop offset="100%" stop-color="#657287" />
    </linearGradient>"""
    body = """    <g filter="url(#login-panel-shadow)">
      <rect x="10.5" y="12.5" width="43" height="39" rx="9" fill="url(#login-frame)" />
      <rect x="12.5" y="14.5" width="39" height="35" rx="7.2" fill="url(#login-screen)" />
    </g>
    <rect x="13.2" y="15.2" width="37.6" height="33.6" rx="6.5" fill="none"
          stroke="#8ccaff" stroke-opacity="0.28" stroke-width="0.8" />
    <circle cx="29.5" cy="26.5" r="6.1" fill="url(#login-avatar)" />
    <path d="M18.2 39.1C19.4 33.6 23.6 30.6 29.5 30.6C35.4 30.6 39.6 33.6 40.8 39.1
             C41.1 40.4 40.1 41.5 38.8 41.5H20.2C18.9 41.5 17.9 40.4 18.2 39.1Z"
          fill="url(#login-avatar)" />
    <rect x="19.5" y="43.8" width="20" height="3.2" rx="1.6" fill="#000000" opacity="0.42" />
    <circle cx="24.8" cy="45.4" r="0.9" fill="#d7e8fa" />
    <circle cx="29.5" cy="45.4" r="0.9" fill="#d7e8fa" />
    <circle cx="34.2" cy="45.4" r="0.9" fill="#d7e8fa" />
    <g filter="url(#login-badge-shadow)">
      <circle cx="47.5" cy="46.5" r="10" fill="url(#login-badge)" />
      <circle cx="47.5" cy="46.5" r="9.25" fill="none" stroke="#ffffff"
              stroke-opacity="0.46" stroke-width="0.8" />
    </g>
    <g fill="none" stroke="#173860" stroke-width="2.25" stroke-linecap="round">
      <circle cx="47.5" cy="46.5" r="4.4" />
      <path d="M47.5 37.8V40M47.5 53V55.2M38.8 46.5H41M54 46.5H56.2
               M41.35 40.35L42.9 41.9M52.1 51.1L53.65 52.65
               M41.35 52.65L42.9 51.1M52.1 41.9L53.65 40.35" />
    </g>
    <circle cx="47.5" cy="46.5" r="1.75" fill="#173860" />"""
    return tile(body, top="#1b3e70", bottom="#080d19",
                defs=defs, glow=("#55b8ff", 0.14))


# --------------------------------------------------------------------------
# gnome tour / welcome
# --------------------------------------------------------------------------

def dark_tour_svg():
    """The welcome house: warm orange keeps burning, the card goes cold."""
    defs = """
    <linearGradient id="t-roof" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#ff9f45" />
      <stop offset="100%" stop-color="#f2712c" />
    </linearGradient>
    <linearGradient id="t-wall" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#ffc46b" />
      <stop offset="100%" stop-color="#f79a3c" />
    </linearGradient>
    <radialGradient id="t-lit" cx="50%" cy="60%" r="60%">
      <stop offset="0%" stop-color="#fffdf4" />
      <stop offset="100%" stop-color="#ffe6a8" />
    </radialGradient>"""
    body = """    <g>
      <path d="M 32 12.5 L 51 28.5 L 51 50 A 2.5 2.5 0 0 1 48.5 52.5 L 15.5 52.5 A 2.5 2.5 0 0 1 13 50 L 13 28.5 Z"
            fill="url(#t-roof)" />
      <path d="M 32 20 L 45.5 31.5 L 45.5 52.5 L 18.5 52.5 L 18.5 31.5 Z" fill="url(#t-wall)" />
      <path d="M 32 27.5 L 40.5 34.5 L 40.5 52.5 L 23.5 52.5 L 23.5 34.5 Z" fill="url(#t-lit)" />
      <path d="M 32 12.5 L 51 28.5 L 51 31 L 32 15 L 13 31 L 13 28.5 Z" fill="#ffffff" opacity="0.22" />
    </g>"""
    return tile(body, top="#2a2320", bottom="#100c0a",
                defs=defs, glow=("#ff9f45", 0.17))


# --------------------------------------------------------------------------
# settings gear (system settings)
# --------------------------------------------------------------------------

def dark_gear_svg():
    """The supplied Apple artwork, with only its neutral card remapped dark."""
    art = _light_image_href("settings.svg")
    return f"""<svg width="64" height="64" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <filter id="settings-dark" x="0" y="0" width="100%" height="100%"
            color-interpolation-filters="sRGB">
      <feComponentTransfer>
        <feFuncR type="table" tableValues=".02 .035 .055 .075 .095 .12 .85 1" />
        <feFuncG type="table" tableValues=".022 .038 .058 .078 .10 .125 .86 1" />
        <feFuncB type="table" tableValues=".026 .045 .068 .09 .115 .14 .90 1" />
      </feComponentTransfer>
    </filter>
  </defs>
  <image href="{art}" x="0" y="0" width="64" height="64" filter="url(#settings-dark)" />
</svg>"""


def dark_contacts_svg():
    """Address book: the tan card goes dark, the portrait stays warm."""
    defs = """
    <linearGradient id="ct-tan" x1="20%" y1="0%" x2="80%" y2="100%">
      <stop offset="0%" stop-color="#f6c184" />
      <stop offset="100%" stop-color="#d08a3f" />
    </linearGradient>
    <clipPath id="ct-round">
      <circle cx="32" cy="32" r="15.6" />
    </clipPath>"""
    body = """    <g>
      <circle cx="32" cy="32" r="17.2" fill="none" stroke="url(#ct-tan)" stroke-width="2.8" />
      <g clip-path="url(#ct-round)" fill="url(#ct-tan)">
        <circle cx="32" cy="26.5" r="6.4" />
        <path d="M 32 35.5 C 23.5 35.5 18 41.5 17 50 L 47 50 C 46 41.5 40.5 35.5 32 35.5 Z" />
      </g>
    </g>"""
    return tile(body, top="#2e2620", bottom="#100c08",
                defs=defs, glow=("#e0a55f", 0.15))


def dark_extensions_svg():
    """A single sculpted puzzle piece on deep emerald glass.

    Extension Manager is a system utility, not a repair workshop.  The icon
    therefore uses one calm, instantly recognisable symbol with the restrained
    material depth of a macOS system icon.  No secondary tool or micro-detail
    competes with the silhouette at dock sizes.
    """
    defs = """
    <linearGradient id="x-piece" gradientUnits="userSpaceOnUse"
                    x1="25" y1="11" x2="40" y2="51">
      <stop offset="0%" stop-color="#ffffff" />
      <stop offset="42%" stop-color="#f2faf5" />
      <stop offset="78%" stop-color="#d8e9df" />
      <stop offset="100%" stop-color="#b8cfc1" />
    </linearGradient>
    <linearGradient id="x-edge" gradientUnits="userSpaceOnUse"
                    x1="22" y1="12" x2="42" y2="51">
      <stop offset="0%" stop-color="#ffffff" />
      <stop offset="52%" stop-color="#dcece3" />
      <stop offset="100%" stop-color="#789586" />
    </linearGradient>
    <linearGradient id="x-sheen" gradientUnits="userSpaceOnUse"
                    x1="24" y1="13" x2="37" y2="39">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.72" />
      <stop offset="55%" stop-color="#ffffff" stop-opacity="0.10" />
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0" />
    </linearGradient>
    <clipPath id="x-piece-clip">
      <path d="M 19 17 H 26 V 15.5
               C 26 11.9 28.9 9 32.5 9
               C 36.1 9 39 11.9 39 15.5 V 17 H 45
               C 46.7 17 48 18.3 48 20 V 26 H 49.5
               C 53.1 26 56 28.9 56 32.5
               C 56 36.1 53.1 39 49.5 39 H 48 V 45
               C 48 46.7 46.7 48 45 48 H 39 V 46.5
               C 39 42.9 36.1 40 32.5 40
               C 28.9 40 26 42.9 26 46.5 V 48 H 19
               C 17.3 48 16 46.7 16 45 V 39 H 17.5
               C 21.1 39 24 36.1 24 32.5
               C 24 28.9 21.1 26 17.5 26 H 16 V 20
               C 16 18.3 17.3 17 19 17 Z" />
    </clipPath>
    <filter id="x-piece-shadow" x="-30%" y="-30%" width="170%" height="180%">
      <feDropShadow dx="0" dy="2.2" stdDeviation="2.1"
                    flood-color="#000000" flood-opacity="0.52" />
      <feDropShadow dx="0" dy="0.6" stdDeviation="0.45"
                    flood-color="#000000" flood-opacity="0.46" />
    </filter>"""
    piece = """M 19 17 H 26 V 15.5
               C 26 11.9 28.9 9 32.5 9
               C 36.1 9 39 11.9 39 15.5 V 17 H 45
               C 46.7 17 48 18.3 48 20 V 26 H 49.5
               C 53.1 26 56 28.9 56 32.5
               C 56 36.1 53.1 39 49.5 39 H 48 V 45
               C 48 46.7 46.7 48 45 48 H 39 V 46.5
               C 39 42.9 36.1 40 32.5 40
               C 28.9 40 26 42.9 26 46.5 V 48 H 19
               C 17.3 48 16 46.7 16 45 V 39 H 17.5
               C 21.1 39 24 36.1 24 32.5
               C 24 28.9 21.1 26 17.5 26 H 16 V 20
               C 16 18.3 17.3 17 19 17 Z"""
    body = f"""    <g filter="url(#x-piece-shadow)">
      <path d="{piece}" fill="#04100a" stroke="#06140d" stroke-width="2.8" opacity="0.66" />
      <path d="{piece}" fill="url(#x-piece)" stroke="url(#x-edge)" stroke-width="0.9"
            stroke-linejoin="round" />
      <g clip-path="url(#x-piece-clip)">
        <ellipse cx="26" cy="16" rx="24" ry="17" fill="url(#x-sheen)" />
        <path d="M 16.8 44.4 H 26.8 C 28.2 41.8 30.2 40.6 32.5 40.6
                 C 35.1 40.6 37.1 42 38.3 44.2 H 47.3 V 48.8 H 16.8 Z"
              fill="#688576" opacity="0.12" />
      </g>
      <path d="M 19.5 18 H 27 V 15.5 C 27 12.6 29.3 10.2 32.3 10.1"
            fill="none" stroke="#ffffff" stroke-width="0.85"
            stroke-linecap="round" stroke-linejoin="round" opacity="0.86" />
    </g>"""
    return tile(body, top="#18352b", bottom="#07110d",
                defs=defs, glow=("#40d98a", 0.13))


def dark_extension_manager_svg():
    """Extension Manager — the official blue quadrant puzzle, refined.

    The four blue fields preserve the app's recognisable identity and suggest
    a managed collection.  A sapphire glass tile and restrained optical depth
    distinguish it from the single ivory puzzle used by GNOME Extensions.
    """
    piece = """M 19 19 H 26 V 16
               C 26 12.1 29.1 9 33 9
               C 36.9 9 40 12.1 40 16 V 19 H 45
               C 47.2 19 49 20.8 49 23 V 26 H 49.5
               C 53.6 26 57 29.4 57 33.5
               C 57 37.6 53.6 41 49.5 41 H 49 V 46
               C 49 48.2 47.2 50 45 50 H 40 V 47.5
               C 40 43.6 36.9 40.5 33 40.5
               C 29.1 40.5 26 43.6 26 47.5 V 50 H 19
               C 16.8 50 15 48.2 15 46 V 41 H 18.5
               C 22.4 41 25.5 37.9 25.5 34
               C 25.5 30.1 22.4 27 18.5 27 H 15 V 23
               C 15 20.8 16.8 19 19 19 Z"""
    defs = f"""
    <linearGradient id="em-piece" gradientUnits="userSpaceOnUse"
                    x1="21" y1="10" x2="46" y2="51">
      <stop offset="0%" stop-color="#86d7ff" />
      <stop offset="40%" stop-color="#44a8ff" />
      <stop offset="76%" stop-color="#1778ef" />
      <stop offset="100%" stop-color="#0751bd" />
    </linearGradient>
    <linearGradient id="em-edge" gradientUnits="userSpaceOnUse"
                    x1="23" y1="9" x2="44" y2="52">
      <stop offset="0%" stop-color="#d9f6ff" />
      <stop offset="45%" stop-color="#58bcff" />
      <stop offset="100%" stop-color="#00317f" />
    </linearGradient>
    <clipPath id="em-piece-clip">
      <path d="{piece}" />
    </clipPath>
    <filter id="em-piece-shadow" x="-30%" y="-30%" width="170%" height="180%">
      <feDropShadow dx="0" dy="2.2" stdDeviation="2"
                    flood-color="#000000" flood-opacity="0.54" />
      <feDropShadow dx="0" dy="0.6" stdDeviation="0.5"
                    flood-color="#001a47" flood-opacity="0.66" />
    </filter>"""
    body = f"""    <g filter="url(#em-piece-shadow)">
      <path d="{piece}" fill="#020b19" stroke="#031226" stroke-width="2.6" opacity="0.62" />
      <path d="{piece}" fill="url(#em-piece)" stroke="url(#em-edge)" stroke-width="0.9"
            stroke-linejoin="round" />
      <g clip-path="url(#em-piece-clip)">
        <rect x="14" y="8" width="19" height="26" fill="#477fff" opacity="0.32" />
        <rect x="33" y="8" width="25" height="26" fill="#61d5ff" opacity="0.30" />
        <rect x="14" y="34" width="19" height="18" fill="#136cf3" opacity="0.28" />
        <rect x="33" y="34" width="25" height="18" fill="#0647bd" opacity="0.30" />
        <path d="M 16 22 C 16 20.9 17.2 20 19 20 H 27 V 16
                 C 27 12.8 29.5 10.3 32.7 10.2"
              fill="none" stroke="#ffffff" stroke-width="1"
              stroke-linecap="round" opacity="0.78" />
        <path d="M 15 47 H 26.5 C 27.8 43.2 30 41.5 33 41.5
                 C 36 41.5 38.2 43.2 39.5 47 H 49 V 51 H 15 Z"
              fill="#002b78" opacity="0.22" />
      </g>
    </g>"""
    return tile(body, top="#172a45", bottom="#070c16",
                defs=defs, glow=("#229cff", 0.17))


# --------------------------------------------------------------------------
# document scanner
# --------------------------------------------------------------------------

def dark_scanner_svg():
    """A physical scanner, visible document and cyan scanning beam."""
    defs = """
    <filter id="scan-paper-shadow" x="-35%" y="-35%" width="170%" height="180%">
      <feDropShadow dx="0" dy="1.8" stdDeviation="1.7" flood-color="#000000" flood-opacity="0.46" />
    </filter>
    <filter id="scan-device-shadow" x="-30%" y="-35%" width="160%" height="180%">
      <feDropShadow dx="0" dy="2" stdDeviation="1.8" flood-color="#000000" flood-opacity="0.62" />
    </filter>
    <filter id="scan-beam-glow" x="-20%" y="-250%" width="140%" height="600%">
      <feGaussianBlur stdDeviation="1.4" result="blur" />
      <feMerge><feMergeNode in="blur" /><feMergeNode in="SourceGraphic" /></feMerge>
    </filter>
    <linearGradient id="scan-paper" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ffffff" />
      <stop offset="100%" stop-color="#dce5ec" />
    </linearGradient>
    <linearGradient id="scan-fold" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#d7e2ea" />
      <stop offset="100%" stop-color="#9fb3c1" />
    </linearGradient>
    <linearGradient id="scan-deck" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#90a7b8" />
      <stop offset="100%" stop-color="#465d6e" />
    </linearGradient>
    <linearGradient id="scan-body" x1="8%" y1="0%" x2="90%" y2="100%">
      <stop offset="0%" stop-color="#365b74" />
      <stop offset="52%" stop-color="#203d52" />
      <stop offset="100%" stop-color="#0d1c28" />
    </linearGradient>
    <linearGradient id="scan-front" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1a3548" />
      <stop offset="100%" stop-color="#08141d" />
    </linearGradient>"""
    body = """    <g filter="url(#scan-paper-shadow)">
      <path d="M18 9.5H39.5L46 16V42H18Z" fill="url(#scan-paper)" />
      <path d="M39.5 9.5V16H46Z" fill="url(#scan-fold)" />
      <path d="M22.5 17H35.5" stroke="#4a8bc1" stroke-width="2.1" stroke-linecap="round" />
      <path d="M22.5 22H40.5M22.5 25.5H38" stroke="#8fa2b0" stroke-width="1.15" stroke-linecap="round" />
      <rect x="22.5" y="29" width="9.5" height="7.5" rx="1.2" fill="#64b9df" />
      <path d="M23.5 35.3L26.3 32.8L28 34.2L29.6 32.5L31.2 35.3Z" fill="#205f8b" />
      <circle cx="29.4" cy="30.9" r="0.9" fill="#fff0a0" />
      <path d="M35 29.7H41M35 33H40M35 36.3H39" stroke="#99aab6"
            stroke-width="1.05" stroke-linecap="round" />
    </g>
    <g filter="url(#scan-device-shadow)">
      <path d="M13 31.5H51L56 39.5H8Z" fill="url(#scan-deck)" stroke="#ffffff"
            stroke-opacity="0.27" stroke-width="0.8" stroke-linejoin="round" />
      <rect x="8" y="37.5" width="48" height="17" rx="5.5" fill="url(#scan-body)" />
      <rect x="11.5" y="40.5" width="41" height="10.5" rx="3.4" fill="url(#scan-front)" />
      <rect x="14" y="38" width="36" height="3" rx="1.5" fill="#050b10" />
      <path d="M12.5 39H51.5" stroke="#8ad9f3" stroke-opacity="0.26" stroke-width="0.8" />
      <circle cx="49" cy="47" r="1.8" fill="#68ef88" />
      <circle cx="49" cy="47" r="0.75" fill="#e9ffe9" />
      <path d="M15 50H37" stroke="#47677d" stroke-width="1" stroke-linecap="round" />
    </g>
    <g filter="url(#scan-beam-glow)">
      <path d="M12 34.5H52" stroke="#42e7ff" stroke-width="2.1" stroke-linecap="round" />
      <path d="M14 33.9H50" stroke="#e5fdff" stroke-width="0.65" stroke-linecap="round" />
    </g>"""
    return tile(body, top="#1d3543", bottom="#070b0f",
                defs=defs, glow=("#35d8ff", 0.15))


# --------------------------------------------------------------------------
# help
# --------------------------------------------------------------------------

def dark_help_svg():
    """Apple Tips bulb: exact silhouette, amber-black card in dark mode."""
    art = _light_image_href("help.svg")
    return f"""<svg width="64" height="64" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <filter id="tips-dark" x="0" y="0" width="100%" height="100%"
            color-interpolation-filters="sRGB">
      <feColorMatrix in="SourceGraphic" type="matrix"
        values=".10 0 0 0 .018  0 .07 0 0 .010  0 0 .025 0 .004  0 0 0 1 0"
        result="dark" />
      <feColorMatrix in="SourceGraphic" type="matrix"
        values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 2.8 0 -.65"
        result="bulb-mask" />
      <feComposite in="SourceGraphic" in2="bulb-mask" operator="in" result="lit-bulb" />
      <feBlend in="lit-bulb" in2="dark" mode="normal" />
    </filter>
  </defs>
  <image href="{art}" x="0" y="0" width="64" height="64" filter="url(#tips-dark)" />
</svg>"""


def dark_ludusavi_svg():
    """Keep Ludusavi's white glyph intact on clean, deep rose glass."""
    art = _light_image_href("com.github.mtkennerly.ludusavi.svg")
    return f"""<svg width="64" height="64" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <filter id="ludu-shadow" x="-25%" y="-25%" width="150%" height="150%">
      <feDropShadow dx="0" dy="2.4" stdDeviation="2.8" flood-color="#000000" flood-opacity="0.42" />
      <feDropShadow dx="0" dy="1" stdDeviation="0.8" flood-color="#000000" flood-opacity="0.58" />
    </filter>
    <filter id="ludu-dark" x="0" y="0" width="100%" height="100%"
            color-interpolation-filters="sRGB">
      <feColorMatrix in="SourceGraphic" type="matrix"
        values=".12 0 0 0 .018  0 .05 0 0 .006  0 0 .065 0 .010  0 0 0 1 0"
        result="dark" />
      <feColorMatrix in="SourceGraphic" type="matrix"
        values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 3.5 0 0 -2.5"
        result="mark-mask" />
      <feComposite in="SourceGraphic" in2="mark-mask" operator="in" result="white-mark" />
      <feBlend in="white-mark" in2="dark" mode="normal" />
    </filter>
    <linearGradient id="ludu-rim" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.34" />
      <stop offset="35%" stop-color="#ffffff" stop-opacity="0.08" />
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0.02" />
    </linearGradient>
  </defs>
  <rect x="4" y="4" width="56" height="56" rx="13" fill="#2a0c12"
        filter="url(#ludu-shadow)" />
  <image href="{art}" x="0" y="0" width="64" height="64" filter="url(#ludu-dark)" />
  <rect x="4.25" y="4.25" width="55.5" height="55.5" rx="13.75"
        fill="none" stroke="#000000" stroke-opacity="0.32" stroke-width="0.5" />
  <rect x="4.75" y="4.75" width="54.5" height="54.5" rx="13.25"
        fill="none" stroke="url(#ludu-rim)" stroke-width="0.75" />
</svg>"""


# --------------------------------------------------------------------------
# video player
# --------------------------------------------------------------------------

def _video_body():
    return """    <g filter="url(#v-screen-shadow)">
      <rect x="9.5" y="13.5" width="45" height="36" rx="8" fill="url(#v-frame)" />
      <rect x="11.5" y="15.5" width="41" height="32" rx="6.4" fill="url(#v-screen)" />
    </g>
    <g clip-path="url(#v-screen-clip)">
      <rect x="11.5" y="15.5" width="41" height="32" fill="url(#v-screen-glow)" />
      <path d="M10 16H39C35 25 26 30 10 31Z" fill="#ffffff" opacity="0.11" />
      <path d="M11 39C25 43 39 41 53 34V48H11Z" fill="#0c0a36" opacity="0.20" />
    </g>
    <rect x="12.2" y="16.2" width="39.6" height="30.6" rx="5.7" fill="none"
          stroke="#ffffff" stroke-opacity="0.18" stroke-width="0.8" />
    <g filter="url(#v-play-shadow)">
      <circle cx="32" cy="29.5" r="9.4" fill="url(#v-play-disc)"
              stroke="#ffffff" stroke-opacity="0.36" stroke-width="0.9" />
      <path d="M29.3 24.3L38.8 29.5L29.3 34.7Z" fill="#ffffff" />
      <path d="M30.2 25.4V33.6" stroke="#ffffff" stroke-opacity="0.46"
            stroke-width="0.65" stroke-linecap="round" />
    </g>
    <rect x="17" y="42.3" width="30" height="2.2" rx="1.1" fill="#ffffff" opacity="0.20" />
    <rect x="17" y="42.3" width="17.2" height="2.2" rx="1.1" fill="url(#v-progress)" />
    <circle cx="34.2" cy="43.4" r="1.65" fill="#fff4f8" stroke="#e95b9d" stroke-width="0.65" />
    <path d="M28 50H36L38.5 53H25.5Z" fill="url(#v-stand)" />
    <rect x="22.5" y="52.3" width="19" height="2.3" rx="1.15" fill="url(#v-stand)" />
    <path d="M23.5 52.8H40.5" stroke="#ffffff" stroke-opacity="0.20"
          stroke-width="0.6" stroke-linecap="round" />"""


def dark_video_svg():
    """A cinematic glass display with active play and progress controls."""
    defs = """
    <filter id="v-screen-shadow" x="-30%" y="-35%" width="160%" height="180%">
      <feDropShadow dx="0" dy="2" stdDeviation="1.8" flood-color="#000000" flood-opacity="0.62" />
    </filter>
    <filter id="v-play-shadow" x="-45%" y="-45%" width="190%" height="195%">
      <feDropShadow dx="0" dy="1.5" stdDeviation="1.5" flood-color="#0d092f" flood-opacity="0.65" />
    </filter>
    <linearGradient id="v-frame" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#6c7392" />
      <stop offset="100%" stop-color="#30334d" />
    </linearGradient>
    <linearGradient id="v-screen" x1="8%" y1="0%" x2="92%" y2="100%">
      <stop offset="0%" stop-color="#796bff" />
      <stop offset="47%" stop-color="#4d45b4" />
      <stop offset="100%" stop-color="#211c57" />
    </linearGradient>
    <radialGradient id="v-screen-glow" cx="78%" cy="18%" r="78%">
      <stop offset="0%" stop-color="#ff74ba" stop-opacity="0.38" />
      <stop offset="52%" stop-color="#7b6fff" stop-opacity="0.08" />
      <stop offset="100%" stop-color="#2f2c7b" stop-opacity="0" />
    </radialGradient>
    <linearGradient id="v-play-disc" x1="18%" y1="0%" x2="82%" y2="100%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.38" />
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0.10" />
    </linearGradient>
    <linearGradient id="v-progress" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#ff65ad" />
      <stop offset="100%" stop-color="#ffb55f" />
    </linearGradient>
    <linearGradient id="v-stand" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#616782" />
      <stop offset="100%" stop-color="#2d3045" />
    </linearGradient>
    <clipPath id="v-screen-clip">
      <rect x="11.5" y="15.5" width="41" height="32" rx="6.4" />
    </clipPath>"""
    return tile(_video_body(), top="#29263e", bottom="#08080d",
                defs=defs, glow=("#7166ff", 0.17))


def light_video_svg():
    """Light-mode counterpart, same drawing on the light glass card."""
    body = _video_body().replace('stroke-opacity="0.18"', 'stroke-opacity="0.20"')
    return f"""<svg width="64" height="64" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <filter id="glass-shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="2.5" stdDeviation="2.5" flood-color="#000000" flood-opacity="0.25" />
    </filter>
    <filter id="v-screen-shadow" x="-30%" y="-35%" width="160%" height="180%">
      <feDropShadow dx="0" dy="2" stdDeviation="1.8" flood-color="#1b174b" flood-opacity="0.42" />
    </filter>
    <filter id="v-play-shadow" x="-45%" y="-45%" width="190%" height="195%">
      <feDropShadow dx="0" dy="1.5" stdDeviation="1.5" flood-color="#120d42" flood-opacity="0.45" />
    </filter>
    <linearGradient id="card" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#fdfdff" />
      <stop offset="100%" stop-color="#d6dcea" />
    </linearGradient>
    <linearGradient id="inner-bevel" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.75" />
      <stop offset="35%" stop-color="#ffffff" stop-opacity="0.12" />
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0.05" />
    </linearGradient>
    <linearGradient id="v-frame" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#9da7c8" />
      <stop offset="100%" stop-color="#4a4e77" />
    </linearGradient>
    <linearGradient id="v-screen" x1="8%" y1="0%" x2="92%" y2="100%">
      <stop offset="0%" stop-color="#796bff" />
      <stop offset="47%" stop-color="#4d45b4" />
      <stop offset="100%" stop-color="#211c57" />
    </linearGradient>
    <radialGradient id="v-screen-glow" cx="78%" cy="18%" r="78%">
      <stop offset="0%" stop-color="#ff74ba" stop-opacity="0.38" />
      <stop offset="52%" stop-color="#7b6fff" stop-opacity="0.08" />
      <stop offset="100%" stop-color="#2f2c7b" stop-opacity="0" />
    </radialGradient>
    <linearGradient id="v-play-disc" x1="18%" y1="0%" x2="82%" y2="100%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.38" />
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0.10" />
    </linearGradient>
    <linearGradient id="v-progress" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#ff65ad" />
      <stop offset="100%" stop-color="#ffb55f" />
    </linearGradient>
    <linearGradient id="v-stand" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#72799a" />
      <stop offset="100%" stop-color="#3e425f" />
    </linearGradient>
    <clipPath id="card-clip">
      <rect width="56" height="56" x="4" y="4" rx="14" ry="14" />
    </clipPath>
    <clipPath id="v-screen-clip">
      <rect x="11.5" y="15.5" width="41" height="32" rx="6.4" />
    </clipPath>
  </defs>

  <g filter="url(#glass-shadow)">
    <rect width="56" height="56" x="4" y="4" rx="14" ry="14" fill="url(#card)" />
  </g>

  <g clip-path="url(#card-clip)">
{body}
  </g>

  <rect width="55" height="55" x="4.5" y="4.5" rx="13.5" ry="13.5" fill="none" stroke="url(#inner-bevel)" stroke-width="1" />
</svg>"""


# --------------------------------------------------------------------------
# music library
# --------------------------------------------------------------------------

def dark_music_library_svg():
    """GNOME Music as an album collection with sleeve and vinyl record."""
    defs = """
    <filter id="music-album-shadow" x="-35%" y="-35%" width="170%" height="180%">
      <feDropShadow dx="0" dy="2" stdDeviation="1.8" flood-color="#000000" flood-opacity="0.58" />
    </filter>
    <filter id="music-record-shadow" x="-35%" y="-35%" width="170%" height="180%">
      <feDropShadow dx="0" dy="2" stdDeviation="1.7" flood-color="#000000" flood-opacity="0.72" />
    </filter>
    <linearGradient id="music-sleeve" x1="12%" y1="0%" x2="88%" y2="100%">
      <stop offset="0%" stop-color="#ff77b7" />
      <stop offset="48%" stop-color="#d84fc0" />
      <stop offset="100%" stop-color="#6c49cc" />
    </linearGradient>
    <radialGradient id="music-sun" cx="40%" cy="35%" r="65%">
      <stop offset="0%" stop-color="#fff3a8" />
      <stop offset="100%" stop-color="#ff9a5a" />
    </radialGradient>
    <radialGradient id="music-vinyl" cx="34%" cy="27%" r="76%">
      <stop offset="0%" stop-color="#414060" />
      <stop offset="42%" stop-color="#1c1a31" />
      <stop offset="100%" stop-color="#050409" />
    </radialGradient>
    <radialGradient id="music-label" cx="35%" cy="28%" r="72%">
      <stop offset="0%" stop-color="#65e6ff" />
      <stop offset="52%" stop-color="#6f72ff" />
      <stop offset="100%" stop-color="#df4dbe" />
    </radialGradient>
    <clipPath id="music-cover-clip">
      <rect x="12" y="12" width="35" height="39" rx="6" />
    </clipPath>"""
    body = """    <g filter="url(#music-album-shadow)">
      <rect x="9.5" y="15" width="35" height="39" rx="6" fill="#603e68"
            opacity="0.78" transform="rotate(-5 27 34.5)" />
      <rect x="12" y="12" width="35" height="39" rx="6" fill="url(#music-sleeve)" />
      <g clip-path="url(#music-cover-clip)">
        <circle cx="29.5" cy="27" r="9.5" fill="url(#music-sun)" />
        <path d="M9 37C18 29 25 31 33 37C41 43 47 38 52 33V53H9Z"
              fill="#5d3daf" opacity="0.78" />
        <path d="M10 42C20 36 30 41 38 43C45 45 49 42 52 40V53H10Z"
              fill="#332975" opacity="0.66" />
        <path d="M15 17H29" stroke="#fff7df" stroke-width="2.1"
              stroke-linecap="round" opacity="0.86" />
        <path d="M15 21H24" stroke="#fff7df" stroke-width="1.1"
              stroke-linecap="round" opacity="0.54" />
      </g>
      <rect x="12.6" y="12.6" width="33.8" height="37.8" rx="5.4" fill="none"
            stroke="#ffffff" stroke-opacity="0.32" stroke-width="0.8" />
    </g>
    <g filter="url(#music-record-shadow)">
      <circle cx="42.5" cy="39" r="14.2" fill="url(#music-vinyl)" />
      <circle cx="42.5" cy="39" r="11.7" fill="none" stroke="#8c879e"
              stroke-opacity="0.28" stroke-width="0.65" />
      <circle cx="42.5" cy="39" r="9.5" fill="none" stroke="#8c879e"
              stroke-opacity="0.22" stroke-width="0.55" />
      <circle cx="42.5" cy="39" r="7.3" fill="none" stroke="#8c879e"
              stroke-opacity="0.20" stroke-width="0.5" />
      <circle cx="42.5" cy="39" r="5.2" fill="url(#music-label)" />
      <circle cx="42.5" cy="39" r="1.15" fill="#f8f4ff" />
      <path d="M34.5 30.2A12 12 0 0 1 44 27" fill="none" stroke="#ffffff"
            stroke-width="1" stroke-linecap="round" opacity="0.20" />
    </g>"""
    return tile(body, top="#3b2038", bottom="#0c080c",
                defs=defs, glow=("#e852b6", 0.16))


# --------------------------------------------------------------------------
# audio player
# --------------------------------------------------------------------------

def dark_audio_player_svg():
    """Decibels as active headphones wrapped around a colourful waveform."""
    defs = """
    <filter id="audio-player-shadow" x="-38%" y="-38%" width="176%" height="185%">
      <feDropShadow dx="0" dy="2" stdDeviation="1.8" flood-color="#000000" flood-opacity="0.66" />
    </filter>
    <radialGradient id="audio-disc" cx="35%" cy="28%" r="74%">
      <stop offset="0%" stop-color="#29466f" />
      <stop offset="58%" stop-color="#132541" />
      <stop offset="100%" stop-color="#070e1e" />
    </radialGradient>
    <linearGradient id="audio-metal" gradientUnits="userSpaceOnUse" x1="32" y1="17" x2="32" y2="49">
      <stop offset="0%" stop-color="#ffffff" />
      <stop offset="46%" stop-color="#d7e5f0" />
      <stop offset="100%" stop-color="#71899f" />
    </linearGradient>
    <linearGradient id="audio-ear" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#eaf5fc" />
      <stop offset="42%" stop-color="#8db4d1" />
      <stop offset="100%" stop-color="#365a82" />
    </linearGradient>
    <linearGradient id="audio-wave" x1="0%" y1="100%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#44e6ff" />
      <stop offset="52%" stop-color="#7d78ff" />
      <stop offset="100%" stop-color="#ff69b7" />
    </linearGradient>"""
    body = """    <g filter="url(#audio-player-shadow)">
      <circle cx="32" cy="34" r="13.2" fill="url(#audio-disc)" stroke="#ffffff"
              stroke-opacity="0.22" stroke-width="0.9" />
      <circle cx="32" cy="34" r="10.9" fill="none" stroke="#75a2c8"
              stroke-opacity="0.18" stroke-width="0.6" />
      <path d="M16.2 35V31.5C16.2 21.5 22.7 16.5 32 16.5C41.3 16.5 47.8 21.5 47.8 31.5V35"
            fill="none" stroke="url(#audio-metal)" stroke-width="5" stroke-linecap="round" />
      <rect x="11.8" y="32.5" width="9.3" height="15.5" rx="4.3" fill="url(#audio-ear)" />
      <rect x="42.9" y="32.5" width="9.3" height="15.5" rx="4.3" fill="url(#audio-ear)" />
      <path d="M15.2 35.8V44.6M48.8 35.8V44.6" stroke="#ffffff"
            stroke-width="1" stroke-linecap="round" opacity="0.34" />
      <g fill="url(#audio-wave)">
        <rect x="24.3" y="31" width="2.5" height="6" rx="1.25" />
        <rect x="28.2" y="27.5" width="2.5" height="13" rx="1.25" />
        <rect x="32.1" y="29.5" width="2.5" height="9" rx="1.25" />
        <rect x="36" y="25.5" width="2.5" height="17" rx="1.25" />
        <rect x="39.9" y="31.5" width="2.5" height="5" rx="1.25" />
      </g>
      <path d="M23.5 45H40.5" stroke="#7ca5c5" stroke-opacity="0.35"
            stroke-width="1.2" stroke-linecap="round" />
      <circle cx="34.5" cy="45" r="1.35" fill="#ff75b8" />
    </g>"""
    return tile(body, top="#19365b", bottom="#060a12",
                defs=defs, glow=("#4d8cff", 0.17))


# --------------------------------------------------------------------------
# applications grid
# --------------------------------------------------------------------------

def dark_app_grid_svg():
    """Search plus six colourful app tiles, following the supplied reference."""
    defs = """
    <filter id="apps-control-shadow" x="-35%" y="-35%" width="170%" height="180%">
      <feDropShadow dx="0" dy="1.4" stdDeviation="1.3" flood-color="#000000" flood-opacity="0.52" />
    </filter>
    <linearGradient id="apps-search" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#555b63" />
      <stop offset="52%" stop-color="#3d4249" />
      <stop offset="100%" stop-color="#443a41" />
    </linearGradient>
    <linearGradient id="apps-blue" x1="10%" y1="0%" x2="90%" y2="100%">
      <stop offset="0%" stop-color="#22c7ff" /><stop offset="100%" stop-color="#078ae7" />
    </linearGradient>
    <linearGradient id="apps-green" x1="10%" y1="0%" x2="90%" y2="100%">
      <stop offset="0%" stop-color="#4cec68" /><stop offset="100%" stop-color="#19bd3d" />
    </linearGradient>
    <linearGradient id="apps-pink" x1="10%" y1="0%" x2="90%" y2="100%">
      <stop offset="0%" stop-color="#ff5d87" /><stop offset="100%" stop-color="#f22b5e" />
    </linearGradient>
    <linearGradient id="apps-orange" x1="10%" y1="0%" x2="90%" y2="100%">
      <stop offset="0%" stop-color="#ffb33d" /><stop offset="100%" stop-color="#ff8611" />
    </linearGradient>
    <linearGradient id="apps-purple" x1="10%" y1="0%" x2="90%" y2="100%">
      <stop offset="0%" stop-color="#c169f0" /><stop offset="100%" stop-color="#9143ce" />
    </linearGradient>
    <linearGradient id="apps-gray" x1="10%" y1="0%" x2="90%" y2="100%">
      <stop offset="0%" stop-color="#b7b7b9" /><stop offset="100%" stop-color="#77797e" />
    </linearGradient>"""
    body = """    <g filter="url(#apps-control-shadow)">
      <rect x="11.5" y="12.5" width="41" height="11.5" rx="5.75" fill="url(#apps-search)" />
      <rect x="12.2" y="13.2" width="39.6" height="10.1" rx="5.05" fill="none"
            stroke="#ffffff" stroke-opacity="0.18" stroke-width="0.7" />
      <circle cx="18.2" cy="18" r="2.8" fill="none" stroke="#f5f7fa" stroke-width="1.4" />
      <path d="M20.3 20.1L22.8 22.6" stroke="#f5f7fa" stroke-width="1.4" stroke-linecap="round" />
    </g>
    <g filter="url(#apps-control-shadow)">
      <rect x="12.5" y="28" width="11" height="11" rx="3.1" fill="url(#apps-blue)" />
      <rect x="26.5" y="28" width="11" height="11" rx="3.1" fill="url(#apps-green)" />
      <rect x="40.5" y="28" width="11" height="11" rx="3.1" fill="url(#apps-pink)" />
      <rect x="12.5" y="42" width="11" height="11" rx="3.1" fill="url(#apps-orange)" />
      <rect x="26.5" y="42" width="11" height="11" rx="3.1" fill="url(#apps-purple)" />
      <rect x="40.5" y="42" width="11" height="11" rx="3.1" fill="url(#apps-gray)" />
      <path d="M14.5 29.3H21.5M28.5 29.3H35.5M42.5 29.3H49.5
               M14.5 43.3H21.5M28.5 43.3H35.5M42.5 43.3H49.5"
            stroke="#ffffff" stroke-width="0.75" stroke-linecap="round" opacity="0.40" />
    </g>"""
    return tile(body, top="#2c313a", bottom="#090b0e",
                defs=defs, glow=("#8297b4", 0.12))


# --------------------------------------------------------------------------
# maps
# --------------------------------------------------------------------------

def dark_maps_svg():
    """Apple Maps at night: dark land, lit roads, the blue heading arrow."""
    defs = """
    <linearGradient id="m-land" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#2b3038" />
      <stop offset="100%" stop-color="#171b21" />
    </linearGradient>
    <linearGradient id="m-park" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#2f6b45" />
      <stop offset="100%" stop-color="#1d4a2e" />
    </linearGradient>
    <linearGradient id="m-water" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1d4f8a" />
      <stop offset="100%" stop-color="#123258" />
    </linearGradient>
    <linearGradient id="m-badge" x1="20%" y1="0%" x2="80%" y2="100%">
      <stop offset="0%" stop-color="#4aa3ff" />
      <stop offset="100%" stop-color="#0a63d2" />
    </linearGradient>"""
    body = """    <g>
      <rect x="4" y="4" width="56" height="56" fill="url(#m-land)" />
      <path d="M 4 4 L 26 4 L 17 60 L 4 60 Z" fill="url(#m-park)" opacity="0.85" />
      <path d="M 44 4 L 60 4 L 60 24 Z" fill="url(#m-water)" />

      <g stroke="#525a66" stroke-width="4" fill="none" stroke-linecap="square">
        <path d="M 4 22 L 60 16" />
        <path d="M 4 46 L 60 52" />
        <path d="M 22 4 L 30 60" />
      </g>
      <g stroke="#8b95a4" stroke-width="1.2" fill="none" opacity="0.5">
        <path d="M 4 34 L 60 34" />
        <path d="M 44 4 L 48 60" />
      </g>
      <path d="M 4 22 L 60 16" stroke="#f0b429" stroke-width="1.4" fill="none" opacity="0.65" />

      <circle cx="32" cy="32" r="12" fill="#000000" opacity="0.35" />
      <circle cx="32" cy="32" r="11" fill="url(#m-badge)" />
      <circle cx="32" cy="32" r="11" fill="none" stroke="#ffffff" stroke-opacity="0.55" stroke-width="1.2" />
      <path d="M 32 24.5 L 38 39.5 L 32 36 L 26 39.5 Z" fill="#ffffff" />
    </g>"""
    return tile(body, top="#2b3038", bottom="#171b21",
                defs=defs, glow=None)


# --------------------------------------------------------------------------
# camera
# --------------------------------------------------------------------------

def dark_camera_svg():
    """Camera: graphite body, real glass in the lens."""
    defs = """
    <linearGradient id="cam-body" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#4a5058" />
      <stop offset="100%" stop-color="#23272d" />
    </linearGradient>
    <linearGradient id="cam-ring" x1="20%" y1="0%" x2="80%" y2="100%">
      <stop offset="0%" stop-color="#d6dbe2" />
      <stop offset="50%" stop-color="#868d97" />
      <stop offset="100%" stop-color="#4c525a" />
    </linearGradient>
    <radialGradient id="cam-glass" cx="38%" cy="32%" r="72%">
      <stop offset="0%" stop-color="#5fd0ff" />
      <stop offset="45%" stop-color="#1c5f9e" />
      <stop offset="100%" stop-color="#0a1420" />
    </radialGradient>"""
    body = """    <g>
      <path d="M 25.5 15.5 L 38.5 15.5 L 41 19.5 L 51 19.5 A 3.5 3.5 0 0 1 54.5 23 L 54.5 45
               A 3.5 3.5 0 0 1 51 48.5 L 13 48.5 A 3.5 3.5 0 0 1 9.5 45 L 9.5 23
               A 3.5 3.5 0 0 1 13 19.5 L 23 19.5 Z" fill="url(#cam-body)" />
      <path d="M 25.5 15.5 L 38.5 15.5 L 41 19.5 L 23 19.5 Z" fill="#ffffff" opacity="0.16" />
      <circle cx="32" cy="34" r="12" fill="url(#cam-ring)" />
      <circle cx="32" cy="34" r="9.6" fill="url(#cam-glass)" />
      <path d="M 25 30 A 9.6 9.6 0 0 1 35.5 26 A 10.5 10.5 0 0 0 25 30 Z" fill="#ffffff" opacity="0.55" />
      <circle cx="47.5" cy="26" r="2.1" fill="#ffd15c" />
      <rect x="12.5" y="24" width="6" height="3" rx="1.5" fill="#ffffff" opacity="0.2" />
    </g>"""
    return tile(body, top="#2c3037", bottom="#0d0f12",
                defs=defs, glow=("#5fd0ff", 0.10))


# --------------------------------------------------------------------------
# name-specific repairs for empty source artwork
# --------------------------------------------------------------------------

def dark_celeste_svg():
    """Celeste: a cold mountain, warm summit and the game's red berry."""
    defs = """
    <linearGradient id="ce-mountain" x1="20%" y1="0%" x2="80%" y2="100%">
      <stop offset="0%" stop-color="#9ed8ff" />
      <stop offset="55%" stop-color="#596bd4" />
      <stop offset="100%" stop-color="#30245f" />
    </linearGradient>
    <linearGradient id="ce-berry" x1="20%" y1="0%" x2="80%" y2="100%">
      <stop offset="0%" stop-color="#ff6b7d" />
      <stop offset="100%" stop-color="#d71952" />
    </linearGradient>"""
    body = """    <g>
      <path d="M 9 51 L 26.5 21 L 32 28 L 38 16 L 55 51 Z" fill="url(#ce-mountain)" />
      <path d="M 26.5 21 L 32 28 L 38 16 L 43 25 L 38 23.2 L 34 33 L 29.5 28 Z"
            fill="#f4f7ff" opacity="0.92" />
      <path d="M 9 51 L 22 39 L 29 44 L 36 35 L 55 51 Z" fill="#19162f" opacity="0.74" />
      <g transform="translate(43, 15)">
        <path d="M 0 2 C -5 -1 -9 2 -8 7 C -7 12 -2 15 0 17 C 2 15 7 12 8 7 C 9 2 5 -1 0 2 Z"
              fill="url(#ce-berry)" />
        <path d="M -4 1 L 0 -3 L 4 1 L 1.5 2.5 L 0 0.8 L -1.5 2.5 Z" fill="#73df73" />
        <circle cx="-3" cy="6" r="0.8" fill="#ffd37d" />
        <circle cx="2.7" cy="7.5" r="0.8" fill="#ffd37d" />
      </g>
    </g>"""
    return tile(body, top="#202a46", bottom="#0a0c19",
                defs=defs, glow=("#739dff", 0.17))


def dark_inscryption_svg():
    """Inscryption: an ember-lit card and the watching cabin eye."""
    defs = """
    <linearGradient id="in-card" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#6e3218" />
      <stop offset="100%" stop-color="#2a120b" />
    </linearGradient>
    <linearGradient id="in-ember" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ffb13b" />
      <stop offset="100%" stop-color="#e64b16" />
    </linearGradient>"""
    body = """    <g>
      <rect x="16" y="11" width="32" height="42" rx="4" fill="url(#in-card)"
            stroke="#d46a26" stroke-width="1.2" />
      <path d="M 20 17 L 24 13 M 44 13 L 48 17 M 20 47 L 24 51 M 44 51 L 48 47"
            stroke="#ff9f2f" stroke-opacity="0.52" stroke-width="1.2" />
      <path d="M 21 31 C 27 23 37 23 43 31 C 37 39 27 39 21 31 Z" fill="#130a08"
            stroke="url(#in-ember)" stroke-width="1.5" />
      <circle cx="32" cy="31" r="5.2" fill="url(#in-ember)" />
      <circle cx="32" cy="31" r="2.2" fill="#170b08" />
      <path d="M 26 43 L 30 39 L 32 43 L 34 39 L 38 43" fill="none"
            stroke="#e87027" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
    </g>"""
    return tile(body, top="#2b1812", bottom="#0b0706",
                defs=defs, glow=("#ff6b1a", 0.18))


def dark_papers_please_svg():
    """Papers, Please: the severe Arstotzkan eagle in red and olive."""
    body = """    <g>
      <g fill="#6f7d48" opacity="0.88">
        <rect x="10" y="25" width="14" height="3" />
        <rect x="8" y="31" width="16" height="3" />
        <rect x="10" y="37" width="14" height="3" />
        <rect x="40" y="25" width="14" height="3" />
        <rect x="40" y="31" width="16" height="3" />
        <rect x="40" y="37" width="14" height="3" />
      </g>
      <path d="M 32 13 L 36 21 L 46 18 L 40 27 L 47 31 L 39 34 L 41 46
               L 32 51 L 23 46 L 25 34 L 17 31 L 24 27 L 18 18 L 28 21 Z"
            fill="#d64a3d" />
      <path d="M 32 20 L 36.5 29 L 32 42 L 27.5 29 Z" fill="#822c2b" />
      <path d="M 27 31 L 32 26 L 37 31 L 35 39 L 29 39 Z" fill="#e9d9b0" />
      <path d="M 30 16 L 32 11 L 34 16 L 32 19 Z" fill="#f0d7a0" />
    </g>"""
    return tile(body, top="#28261d", bottom="#0d0d09",
                glow=("#d64a3d", 0.12))


def dark_openra_d2k_svg():
    """OpenRA Dune 2000: desert planet, twin moons and compact D2K mark."""
    defs = """
    <radialGradient id="d2k-planet" cx="38%" cy="30%" r="72%">
      <stop offset="0%" stop-color="#ffd27a" />
      <stop offset="55%" stop-color="#c77a27" />
      <stop offset="100%" stop-color="#633012" />
    </radialGradient>"""
    body = """    <g>
      <circle cx="32" cy="31" r="20" fill="url(#d2k-planet)" />
      <path d="M 13 35 C 23 28 33 39 51 28 C 43 45 27 52 17 42 Z"
            fill="#3a1c16" opacity="0.88" />
      <circle cx="44" cy="16" r="3.2" fill="#d6d4c6" />
      <circle cx="49" cy="22" r="1.7" fill="#9ba7ad" />
      <text x="32" y="38" font-family="DIN Condensed, Impact, sans-serif" font-size="15"
            font-weight="800" letter-spacing="-1" fill="#fff3c5" text-anchor="middle">D2K</text>
    </g>"""
    return tile(body, top="#302119", bottom="#100a07",
                defs=defs, glow=("#d48a31", 0.15))


def dark_oneshot_svg():
    """OneShot: its sun-like bulb with a heart filament and violet base."""
    defs = """
    <radialGradient id="os-bulb" cx="38%" cy="28%" r="70%">
      <stop offset="0%" stop-color="#fffbd1" />
      <stop offset="45%" stop-color="#ffd84e" />
      <stop offset="100%" stop-color="#e99212" />
    </radialGradient>
    <linearGradient id="os-base" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#8f65d6" />
      <stop offset="100%" stop-color="#453071" />
    </linearGradient>"""
    body = """    <g>
      <circle cx="32" cy="28" r="17" fill="url(#os-bulb)" />
      <path d="M 25 29 C 25 24 31 23 32 27 C 33 23 39 24 39 29
               C 39 33 35 35 32 38 C 29 35 25 33 25 29 Z"
            fill="none" stroke="#fffdf2" stroke-width="2.1" />
      <path d="M 23 42 L 41 42 L 38 52 L 26 52 Z" fill="url(#os-base)" />
      <path d="M 25 45 L 39 45 M 26 49 L 38 49" stroke="#d9c7ff" stroke-width="1.2" opacity="0.72" />
      <path d="M 22 20 A 17 17 0 0 1 35 11" fill="none" stroke="#ffffff"
            stroke-width="2" stroke-linecap="round" opacity="0.65" />
    </g>"""
    return tile(body, top="#29213a", bottom="#0e0a16",
                defs=defs, glow=("#ffd84e", 0.22))


def dark_stardew_svg():
    """Stardew Valley: a tiny pixel chicken under a midnight farm sky."""
    body = """    <g shape-rendering="crispEdges">
      <rect x="18" y="18" width="4" height="4" fill="#fff4cf" />
      <rect x="22" y="14" width="12" height="4" fill="#fff4cf" />
      <rect x="18" y="22" width="24" height="16" fill="#fff4cf" />
      <rect x="22" y="38" width="16" height="8" fill="#fff4cf" />
      <rect x="34" y="18" width="8" height="4" fill="#d9533f" />
      <rect x="38" y="22" width="8" height="4" fill="#f4b73f" />
      <rect x="22" y="26" width="4" height="4" fill="#4b2b28" />
      <rect x="18" y="34" width="4" height="4" fill="#d8bb83" />
      <rect x="24" y="46" width="4" height="4" fill="#f4b73f" />
      <rect x="34" y="46" width="4" height="4" fill="#f4b73f" />
      <rect x="12" y="14" width="2" height="2" fill="#fff4cf" />
      <rect x="49" y="20" width="2" height="2" fill="#fff4cf" />
      <rect x="46" y="11" width="3" height="3" fill="#f4d45c" />
    </g>"""
    return tile(body, top="#173354", bottom="#080f1c",
                glow=("#f4d45c", 0.11))


def dark_terraria_svg():
    """Terraria: the grass block and tree reduced to crisp pixel essentials."""
    body = """    <g shape-rendering="crispEdges">
      <rect x="13" y="39" width="38" height="13" fill="#7a3f21" />
      <rect x="13" y="36" width="38" height="6" fill="#6fc34a" />
      <rect x="15" y="42" width="5" height="4" fill="#a96735" />
      <rect x="28" y="45" width="5" height="4" fill="#a96735" />
      <rect x="41" y="41" width="5" height="4" fill="#a96735" />
      <rect x="29" y="23" width="6" height="17" fill="#8a4c2d" />
      <rect x="23" y="17" width="18" height="12" fill="#47ad49" />
      <rect x="19" y="21" width="8" height="8" fill="#47ad49" />
      <rect x="37" y="20" width="8" height="9" fill="#47ad49" />
      <rect x="27" y="13" width="10" height="8" fill="#66ce58" />
      <rect x="10" y="13" width="2" height="2" fill="#d9f6ff" />
      <rect x="49" y="10" width="2" height="2" fill="#d9f6ff" />
    </g>"""
    return tile(body, top="#173144", bottom="#091017",
                glow=("#62d25b", 0.12))


def dark_undertale_svg():
    """Undertale: the red SOUL, intentionally tiny and pixel-sharp."""
    body = """    <g shape-rendering="crispEdges">
      <rect x="24" y="24" width="6" height="6" fill="#ff2d37" />
      <rect x="34" y="24" width="6" height="6" fill="#ff2d37" />
      <rect x="21" y="28" width="22" height="8" fill="#ff2d37" />
      <rect x="24" y="36" width="16" height="5" fill="#ff2d37" />
      <rect x="28" y="41" width="8" height="5" fill="#ff2d37" />
      <rect x="31" y="46" width="2" height="2" fill="#ff2d37" />
      <rect x="14" y="17" width="2" height="2" fill="#f2f2f2" />
      <rect x="48" y="38" width="2" height="2" fill="#f2f2f2" />
      <rect x="44" y="15" width="3" height="3" fill="#f2f2f2" />
    </g>"""
    return tile(body, top="#242126", bottom="#09090a",
                glow=("#ff2d37", 0.19))


def dark_simplex_svg():
    """SimpleX Chat: three linked X marks, kept crisp at launcher size."""
    body = """    <g fill="none" stroke-linecap="round" stroke-linejoin="round" stroke-width="4.2">
      <path d="M 18 21 L 30 33 L 18 45 M 30 21 L 18 33 L 30 45" stroke="#4db8ff" />
      <path d="M 29 21 L 41 33 L 29 45 M 41 21 L 29 33 L 41 45" stroke="#1688d4" />
      <path d="M 40 21 L 51 33 L 40 45 M 51 21 L 40 33 L 51 45" stroke="#8be0ff" />
    </g>"""
    return tile(body, top="#182b3c", bottom="#081019",
                glow=("#46bfff", 0.16))


def dark_clapgrep_svg():
    """Clapgrep: document search, expressed without tiny unreadable detail."""
    defs = """
    <linearGradient id="cg-doc" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#edeff5" />
      <stop offset="100%" stop-color="#aeb8c8" />
    </linearGradient>
    <linearGradient id="cg-glass" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#66e0ff" />
      <stop offset="100%" stop-color="#198ad3" />
    </linearGradient>"""
    body = """    <g>
      <path d="M 16 13 H 39 L 47 21 V 47 H 16 Z" fill="url(#cg-doc)" />
      <path d="M 39 13 V 21 H 47" fill="#7f8a9b" />
      <path d="M 21 27 H 38 M 21 33 H 34 M 21 39 H 31" stroke="#526071"
            stroke-width="2" stroke-linecap="round" />
      <circle cx="39" cy="39" r="9" fill="#15202b" stroke="url(#cg-glass)" stroke-width="3" />
      <path d="M 45.5 45.5 L 51 51" stroke="#66e0ff" stroke-width="3.5" stroke-linecap="round" />
    </g>"""
    return tile(body, top="#1b2d38", bottom="#091016",
                defs=defs, glow=("#46cfff", 0.14))


def dark_roblox_svg():
    """Roblox: the current tilted square mark in cool machined metal."""
    defs = """
    <linearGradient id="rb-metal" x1="12%" y1="0%" x2="88%" y2="100%">
      <stop offset="0%" stop-color="#ffffff" />
      <stop offset="45%" stop-color="#d9dee8" />
      <stop offset="100%" stop-color="#8d98a8" />
    </linearGradient>"""
    body = """    <g transform="rotate(14 32 32)">
      <path d="M 15 15 H 49 V 49 H 15 Z M 27 27 V 37 H 37 V 27 Z"
            fill="url(#rb-metal)" fill-rule="evenodd" />
      <path d="M 16 16 H 48" stroke="#ffffff" stroke-width="1.2" opacity="0.55" />
    </g>"""
    return tile(body, top="#252a31", bottom="#0b0d10",
                defs=defs, glow=("#c7d8ef", 0.10))


def dark_ricochlime_svg():
    """Ricochlime: a lively slime plus the ricocheting projectile path."""
    defs = """
    <linearGradient id="rc-slime" x1="20%" y1="0%" x2="80%" y2="100%">
      <stop offset="0%" stop-color="#8cf45b" />
      <stop offset="100%" stop-color="#35b83e" />
    </linearGradient>"""
    body = """    <g>
      <path d="M 15 45 C 15 34 20 26 27 24 C 28 17 36 17 38 24
               C 46 27 50 35 49 45 Z" fill="url(#rc-slime)" />
      <circle cx="27" cy="34" r="2.2" fill="#12351c" />
      <circle cx="39" cy="34" r="2.2" fill="#12351c" />
      <path d="M 27 41 C 30 43 35 43 39 40" fill="none" stroke="#12351c"
            stroke-width="1.8" stroke-linecap="round" />
      <path d="M 12 18 L 22 13 L 29 19 L 41 12 L 51 18" fill="none"
            stroke="#dfffae" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
      <circle cx="12" cy="18" r="3" fill="#fff36b" />
      <circle cx="51" cy="18" r="2" fill="#fff36b" opacity="0.72" />
    </g>"""
    return tile(body, top="#17331f", bottom="#08120b",
                defs=defs, glow=("#71e650", 0.17))


def dark_shadps4_svg():
    """shadPS4: its official symbol family, rebuilt as sapphire Liquid Glass."""
    defs = """
    <filter id="shad-mark-shadow" x="-30%" y="-30%" width="160%" height="180%">
      <feDropShadow dx="0" dy="1.35" stdDeviation="1.05" flood-color="#00020e" flood-opacity="0.82" />
      <feDropShadow dx="0" dy="0" stdDeviation="0.48" flood-color="#b9dcff" flood-opacity="0.14" />
    </filter>
    <filter id="shad-symbol-glow" x="-55%" y="-55%" width="210%" height="220%">
      <feDropShadow dx="0" dy="0.75" stdDeviation="0.7" flood-color="#00020e" flood-opacity="0.82" />
      <feDropShadow dx="0" dy="0" stdDeviation="0.95" flood-color="#26d3ff" flood-opacity="0.42" />
    </filter>
    <linearGradient id="shad-symbol" gradientUnits="userSpaceOnUse" x1="13" y1="10" x2="52" y2="57">
      <stop offset="0%" stop-color="#8cf4ff" />
      <stop offset="45%" stop-color="#28d3ff" />
      <stop offset="100%" stop-color="#168eff" />
    </linearGradient>
    <linearGradient id="shad-four" gradientUnits="userSpaceOnUse" x1="20" y1="15" x2="39" y2="50">
      <stop offset="0%" stop-color="#ffffff" />
      <stop offset="50%" stop-color="#eef7ff" />
      <stop offset="100%" stop-color="#a9c8f4" />
    </linearGradient>
    <linearGradient id="shad-stripe" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#1b4fba" stop-opacity="0.02" />
      <stop offset="50%" stop-color="#2380ed" stop-opacity="0.17" />
      <stop offset="100%" stop-color="#2bbcff" stop-opacity="0.025" />
    </linearGradient>"""
    body = """    <path d="M4 21 C18 14.8 44 13.2 60 18.5 V27 C42 22.3 19 23.2 4 29 Z"
          fill="#6eb8ff" opacity="0.035" />
    <path d="M4 34.5 C20 30.7 44 30.2 60 34 V41.2 C43 38 21 38.8 4 43.2 Z"
          fill="url(#shad-stripe)" />

    <g fill="none" stroke-linecap="round" stroke-linejoin="round" filter="url(#shad-symbol-glow)">
      <g stroke="#01051d" stroke-opacity="0.80" stroke-width="4.5" transform="translate(0 0.75)">
        <circle cx="17.3" cy="18.7" r="6.35" />
        <path d="M46.8 10.6 L55.6 21.1 L43.2 24.2 Z" />
        <path d="M7.05 44.3 L18.4 48.25 L14.5 59.6 L3.15 55.65 Z" />
        <path d="M45.5 39.5 L54.4 51 M54.15 39.6 L45.25 50.9" />
      </g>
      <g stroke="url(#shad-symbol)" stroke-width="2.8">
        <circle cx="17.3" cy="18.7" r="6.35" />
        <path d="M46.8 10.6 L55.6 21.1 L43.2 24.2 Z" />
        <path d="M7.05 44.3 L18.4 48.25 L14.5 59.6 L3.15 55.65 Z" />
        <path d="M45.5 39.5 L54.4 51 M54.15 39.6 L45.25 50.9" />
      </g>
      <g stroke="#e4fcff" stroke-opacity="0.40" stroke-width="0.65" transform="translate(-0.28 -0.32)">
        <circle cx="17.3" cy="18.7" r="6.35" />
        <path d="M46.8 10.6 L55.6 21.1 L43.2 24.2 Z" />
        <path d="M7.05 44.3 L18.4 48.25 L14.5 59.6 L3.15 55.65 Z" />
        <path d="M45.5 39.5 L54.4 51 M54.15 39.6 L45.25 50.9" />
      </g>
    </g>

    <g fill="none" stroke-linecap="round" stroke-linejoin="round" filter="url(#shad-mark-shadow)">
      <g stroke="#010318" stroke-opacity="0.82" stroke-width="8.2" transform="translate(0 0.8)">
        <path d="M34.35 16.2 L16.55 38.7 H43.1" />
        <path d="M34.35 16.2 V49.2" />
      </g>
      <g stroke="url(#shad-four)" stroke-width="6.25">
        <path d="M34.35 16.2 L16.55 38.7 H43.1" />
        <path d="M34.35 16.2 V49.2" />
      </g>
      <g stroke="#ffffff" stroke-opacity="0.48" stroke-width="0.85" transform="translate(-0.42 -0.45)">
        <path d="M34.35 16.2 L16.55 38.7 H43.1" />
        <path d="M34.35 16.2 V49.2" />
      </g>
    </g>"""
    return tile(body, top="#1b2c63", bottom="#06081b",
                defs=defs, glow=("#1e79ff", 0.14))


# --------------------------------------------------------------------------
# system log viewer / Console
# --------------------------------------------------------------------------

_LOG_WARNING_PATH = """M17.852 23.43L18.992 28.602L20.102 28.602L21.523 20.148L20.383 20.148L19.93 23.398L19.477 26.883L19.398 26.883L18.336 22.086L17.289 22.086L16.227 26.883L16.148 26.883L15.695 23.398L15.242 20.148L14.102 20.148L15.508 28.602L16.633 28.602L17.773 23.43ZM27.285 28.602L28.582 28.602L25.91 20.148L24.551 20.148L21.879 28.602L23.113 28.602L23.801 26.273L26.613 26.273ZM25.176 21.492L25.223 21.492L26.316 25.273L24.082 25.273ZM32.875 25.305L34.422 28.602L35.797 28.602L34.078 25.07C35.031 24.742 35.641 23.836 35.641 22.727C35.641 21.133 34.562 20.148 32.844 20.148L29.938 20.148L29.938 28.602L31.141 28.602L31.141 25.305ZM31.141 21.18L32.719 21.18C33.781 21.18 34.406 21.758 34.406 22.758C34.406 23.742 33.781 24.32 32.672 24.32L31.141 24.32ZM38.293 28.602L38.293 22.258L38.371 22.258L41.793 28.602L42.918 28.602L42.918 20.148L41.84 20.148L41.84 26.461L41.746 26.461L38.34 20.148L37.199 20.148L37.199 28.602ZM49.82 28.602L49.82 27.539L48.086 27.539L48.086 21.211L49.82 21.211L49.82 20.148L45.148 20.148L45.148 21.211L46.867 21.211L46.867 27.539L45.148 27.539L45.148 28.602ZM53.129 28.602L53.129 22.258L53.207 22.258L56.629 28.602L57.754 28.602L57.754 20.148L56.676 20.148L56.676 26.461L56.582 26.461L53.176 20.148L52.035 20.148L52.035 28.602ZM64.188 25.961C64.188 27.008 63.531 27.664 62.453 27.664C61.188 27.664 60.516 26.805 60.516 25.148L60.516 23.586C60.516 21.945 61.188 21.086 62.453 21.086C63.453 21.086 64.156 21.789 64.203 22.836L65.438 22.836C65.391 21.055 64.266 19.977 62.469 19.977C60.453 19.977 59.297 21.305 59.297 23.586L59.297 25.148C59.297 27.445 60.453 28.773 62.469 28.773C64.234 28.773 65.438 27.664 65.438 26.039L65.438 24.242L62.359 24.242L62.359 25.227L64.188 25.227Z"""
_LOG_MAY_PATH = """M-3.414 41.875L-3.508 38.469L-3.43 38.469L-1.836 43.016L-0.945 43.016L0.648 38.469L0.727 38.469L0.633 41.875L0.633 45L1.695 45L1.695 36.547L0.367 36.547L-1.352 41.688L-1.43 41.688L-3.148 36.547L-4.477 36.547L-4.477 45L-3.414 45ZM8.082 45L9.379 45L6.707 36.547L5.348 36.547L2.676 45L3.91 45L4.598 42.672L7.41 42.672ZM5.973 37.891L6.02 37.891L7.113 41.672L4.879 41.672ZM14.047 45L14.047 41.609L16.844 36.547L15.5 36.547L13.484 40.344L13.406 40.344L11.391 36.547L10.047 36.547L12.828 41.609L12.828 45Z"""
_LOG_TIME_PATH = """M27.711 45L29.008 45L32.742 37.609L32.742 36.547L26.977 36.547L26.977 37.594L31.492 37.594L31.492 37.672ZM37.223 40.562C37.848 40.562 38.348 40.047 38.348 39.422C38.348 38.797 37.848 38.281 37.223 38.281C36.613 38.281 36.098 38.797 36.098 39.422C36.098 40.047 36.613 40.562 37.223 40.562ZM37.223 45.062C37.848 45.062 38.348 44.531 38.348 43.906C38.348 43.281 37.848 42.766 37.223 42.766C36.613 42.766 36.098 43.281 36.098 43.906C36.098 44.531 36.613 45.062 37.223 45.062ZM43.609 41.141L44.594 41.141C45.703 41.141 46.422 41.719 46.422 42.641C46.422 43.547 45.719 44.109 44.625 44.109C43.609 44.109 42.906 43.562 42.812 42.703L41.672 42.703C41.75 44.203 42.938 45.172 44.656 45.172C46.406 45.172 47.641 44.156 47.641 42.688C47.641 41.547 46.969 40.766 45.844 40.625L45.844 40.531C46.75 40.312 47.297 39.578 47.297 38.578C47.297 37.281 46.188 36.375 44.625 36.375C42.984 36.375 41.922 37.297 41.844 38.797L42.984 38.797C43.047 37.922 43.656 37.391 44.578 37.391C45.5 37.391 46.109 37.922 46.109 38.75C46.109 39.578 45.469 40.172 44.562 40.172L43.609 40.172ZM55.074 42.25C55.074 40.703 53.965 39.562 52.465 39.562C51.934 39.562 51.34 39.797 51.074 40.125L50.98 40.094C51.027 39.984 51.027 39.984 51.293 39.609L53.543 36.547L52.152 36.547C52.043 36.688 50.418 38.922 50.293 39.141C49.465 40.312 49.137 41.219 49.137 42.234C49.137 43.953 50.371 45.172 52.105 45.172C53.824 45.172 55.074 43.938 55.074 42.25ZM52.105 44.125C51.09 44.125 50.324 43.344 50.324 42.312C50.324 41.266 51.09 40.5 52.105 40.5C53.121 40.5 53.887 41.266 53.887 42.312C53.887 43.344 53.121 44.125 52.105 44.125Z"""


def dark_system_log_svg():
    """System log viewer: cropped amber log lines on near-black glass."""
    defs = """
    <filter id="log-gold-glow" x="-20%" y="-35%" width="140%" height="170%">
      <feDropShadow dx="0" dy="0" stdDeviation="1.15" flood-color="#ffd341" flood-opacity="0.58" />
      <feDropShadow dx="0" dy="0.35" stdDeviation="0.35" flood-color="#fff0a1" flood-opacity="0.30" />
    </filter>
    <linearGradient id="log-gold" gradientUnits="userSpaceOnUse" x1="32" y1="19" x2="32" y2="46">
      <stop offset="0%" stop-color="#ffdc59" />
      <stop offset="52%" stop-color="#ffd044" />
      <stop offset="100%" stop-color="#eeb31c" />
    </linearGradient>
    <linearGradient id="log-fade" gradientUnits="userSpaceOnUse" x1="51" y1="0" x2="60" y2="0">
      <stop offset="0%" stop-color="#080809" stop-opacity="0" />
      <stop offset="100%" stop-color="#080809" stop-opacity="0.98" />
    </linearGradient>"""
    body = f"""    <g fill="url(#log-gold)" filter="url(#log-gold-glow)">
      <path d="{_LOG_WARNING_PATH}" transform="translate(0 28.6) scale(1 1.12) translate(0 -28.6)" />
      <path d="{_LOG_MAY_PATH}" transform="translate(0 45) scale(1 1.12) translate(0 -45)" />
      <path d="{_LOG_TIME_PATH}" transform="translate(0 45) scale(1 1.12) translate(0 -45)" />
    </g>
    <rect x="51" y="17" width="9" height="14" fill="url(#log-fade)" />"""
    return tile(body, top="#1b1b1d", bottom="#050506",
                defs=defs, glow=("#ffc52f", 0.045))


# --------------------------------------------------------------------------
# registry: light source file -> builder for its dark counterpart
# --------------------------------------------------------------------------

HANDDRAWN = {
    "finder.svg": dark_finder_svg,
    "gnome-connections.svg": dark_connections_svg,
    "google-chrome.svg": dark_chrome_svg,
    "web-browser.svg": dark_web_svg,
    "softwarecenter.svg": dark_appstore_svg,
    "logview.svg": dark_system_log_svg,
    "system-software-install.svg": dark_package_manager_svg,
    "eog.svg": dark_image_viewer_svg,
    "org.gnome.Loupe.svg": dark_loupe_svg,
    "login.svg": dark_login_svg,
    "desktop-environment-gnome.svg": dark_tour_svg,
    "applications-system.svg": dark_app_grid_svg,
    "settings.svg": dark_gear_svg,
    "scanner.svg": dark_scanner_svg,
    "help.svg": dark_help_svg,
    "com.github.mtkennerly.ludusavi.svg": dark_ludusavi_svg,
    "extensions.svg": dark_extensions_svg,
    "com.mattjakeman.ExtensionManager.svg": dark_extension_manager_svg,
    "org.gnome.Totem.svg": dark_video_svg,
    # GNOME's newer player; shipped the FaceTime camera as its artwork.
    "Showtime.svg": dark_video_svg,
    "gnome-music.svg": dark_music_library_svg,
    "org.gnome.Decibels.svg": dark_audio_player_svg,
    "addressbook.svg": dark_contacts_svg,
    "gnome-maps.svg": dark_maps_svg,
    "accessories-camera.svg": dark_camera_svg,
    "net.shadps4.shadps4-qtlauncher.svg": dark_shadps4_svg,
}

# Artwork that must survive into dark mode untouched.
VERBATIM = ()


# These source files contain only an empty card.  Artwork-hash registration
# cannot repair them because several unrelated apps share the exact same blank
# placeholder, so these exceptions are deliberately keyed by resolved name.
NAME_HANDDRAWN = {
    "celeste.svg": dark_celeste_svg,
    "com.hunterwittenborn.Celeste.svg": dark_celeste_svg,
    "lutris_celeste.svg": dark_celeste_svg,
    "steam_icon_504230.svg": dark_celeste_svg,
    "inscryption.svg": dark_inscryption_svg,
    "papers-please.svg": dark_papers_please_svg,
    "net.openra.OpenRA-d2k.svg": dark_openra_d2k_svg,
    "net.openra.OpenRA.openra-d2k.svg": dark_openra_d2k_svg,
    "openra-d2k.svg": dark_openra_d2k_svg,
    "oneshot.svg": dark_oneshot_svg,
    "lutris_stardew-valley.svg": dark_stardew_svg,
    "stardew-valley.svg": dark_stardew_svg,
    "steam_icon_413150.svg": dark_stardew_svg,
    "lutris_terraria.svg": dark_terraria_svg,
    "steam_icon_105600.svg": dark_terraria_svg,
    "terraria.svg": dark_terraria_svg,
    "lutris_undertale.svg": dark_undertale_svg,
    "steam_icon_391540.svg": dark_undertale_svg,
    "undertale.svg": dark_undertale_svg,
    "chat.simplex.simplex.svg": dark_simplex_svg,
    "simplex-chat.svg": dark_simplex_svg,
    "clapgrep.svg": dark_clapgrep_svg,
    "de.leopoldluley.Clapgrep.svg": dark_clapgrep_svg,
    "roblox.svg": dark_roblox_svg,
    "ricochlime.svg": dark_ricochlime_svg,
}
