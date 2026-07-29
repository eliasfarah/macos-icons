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

def tile(body, top="#2a2a2e", bottom="#0e0e10", defs="", glow=None, filter_shadow=True):
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

    return f"""<svg width="64" height="64" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <filter id="d-shadow" x="-25%" y="-25%" width="150%" height="150%">
      <feDropShadow dx="0" dy="1.8" stdDeviation="1.9" flood-color="#000000" flood-opacity="0.55" />
    </filter>
    <linearGradient id="d-bg" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="{top}" />
      <stop offset="100%" stop-color="{bottom}" />
    </linearGradient>
    <linearGradient id="d-rim" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.26" />
      <stop offset="42%" stop-color="#ffffff" stop-opacity="0.07" />
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0.03" />
    </linearGradient>
    <clipPath id="d-clip">
      <rect width="56" height="56" x="4" y="4" rx="14" ry="14" />
    </clipPath>{glow_defs}{defs}
  </defs>

  <g filter="url(#d-shadow)">
    <rect width="56" height="56" x="4" y="4" rx="14" ry="14" fill="url(#d-bg)" />
  </g>

  <g clip-path="url(#d-clip)">
    {glow_body}
{body}
  </g>

  <rect width="55" height="55" x="4.5" y="4.5" rx="13.5" ry="13.5" fill="none" stroke="url(#d-rim)" stroke-width="1" />
</svg>"""


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


# --------------------------------------------------------------------------
# app store / software centre
# --------------------------------------------------------------------------

def dark_appstore_svg():
    """App Store: the blue card becomes a blue-black tile, the A stays white."""
    # userSpaceOnUse: the crossbar is a horizontal line, so an
    # objectBoundingBox gradient would collapse and never paint it.
    defs = """
    <linearGradient id="a-glyph" gradientUnits="userSpaceOnUse" x1="32" y1="18" x2="32" y2="46">
      <stop offset="0%" stop-color="#ffffff" />
      <stop offset="100%" stop-color="#cfd6e4" />
    </linearGradient>"""
    # The App Store "A", traced off the light icon: heavy round bars, legs
    # that cross high and narrow, and a crossbar far wider than the stance.
    body = """    <g stroke="url(#a-glyph)" stroke-width="6.2" stroke-linecap="round" fill="none">
      <path d="M 16.5 47 L 34.5 15" />
      <path d="M 46.5 47 L 28.5 15" />
      <path d="M 14.5 38.4 L 48.5 38.4" />
    </g>"""
    return tile(body, top="#1c2534", bottom="#080a10",
                defs=defs, glow=("#0a84ff", 0.16))


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
# settings gear (extension manager, system settings)
# --------------------------------------------------------------------------

def _gear_path(cx, cy, r_out, r_in, teeth=10, tooth=0.5):
    """Cog outline: `teeth` trapezoid teeth around a circle."""
    import math
    step = 2 * math.pi / teeth
    pts = []
    for i in range(teeth):
        a = i * step
        for radius, off in ((r_in, -step * 0.5), (r_in, -step * tooth * 0.72),
                            (r_out, -step * tooth * 0.46), (r_out, step * tooth * 0.46),
                            (r_in, step * tooth * 0.72), (r_in, step * 0.5)):
            pts.append((cx + radius * math.cos(a + off), cy + radius * math.sin(a + off)))
    return "M " + " L ".join(f"{x:.2f} {y:.2f}" for x, y in pts) + " Z"


def _wedge(cx, cy, r_in, r_out, a_mid, half):
    """One spoke of the rotor, as an annular sector."""
    import math
    a0, a1 = math.radians(a_mid - half), math.radians(a_mid + half)
    p = lambda r, a: (cx + r * math.cos(a), cy + r * math.sin(a))
    x0, y0 = p(r_in, a0)
    x1, y1 = p(r_out, a0)
    x2, y2 = p(r_out, a1)
    x3, y3 = p(r_in, a1)
    return (f"M {x0:.2f} {y0:.2f} L {x1:.2f} {y1:.2f} "
            f"A {r_out} {r_out} 0 0 1 {x2:.2f} {y2:.2f} L {x3:.2f} {y3:.2f} "
            f"A {r_in} {r_in} 0 0 0 {x0:.2f} {y0:.2f} Z")


def dark_gear_svg():
    """Brushed-steel cog on a graphite tile — same watch movement as light mode.

    The light icon's character is in the *count*: forty fine teeth and a thin
    three-spoke rotor with big openings.  Fewer, chunkier teeth turn the same
    drawing into a cartoon.
    """
    defs = """
    <linearGradient id="g-metal" x1="15%" y1="0%" x2="85%" y2="100%">
      <stop offset="0%" stop-color="#eef1f5" />
      <stop offset="45%" stop-color="#c2c9d3" />
      <stop offset="100%" stop-color="#8b929c" />
    </linearGradient>
    <linearGradient id="g-inner" x1="15%" y1="0%" x2="85%" y2="100%">
      <stop offset="0%" stop-color="#dfe4ea" />
      <stop offset="55%" stop-color="#aab2bd" />
      <stop offset="100%" stop-color="#767d87" />
    </linearGradient>"""
    holes = "".join(f'<path d="{_wedge(32, 32, 6.5, 17.2, a, 46)}" />'
                    for a in (90, 210, 330))
    body = f"""    <g>
      <path d="{_gear_path(32, 32, 27, 25, teeth=46, tooth=0.55)}" fill="url(#g-metal)" />
      <circle cx="32" cy="32" r="25" fill="url(#g-metal)" />
      <circle cx="32" cy="32" r="21.5" fill="#14171b" />
      <circle cx="32" cy="32" r="19.5" fill="url(#g-inner)" />
      <g fill="#14171b">{holes}</g>
      <circle cx="32" cy="32" r="2.2" fill="#14171b" />
      <path d="M 8 30 A 24 24 0 0 1 36 8.4 L 35 12.6 A 20 20 0 0 0 12 31 Z"
            fill="#ffffff" opacity="0.3" />
    </g>"""
    return tile(body, top="#2b2e33", bottom="#101215",
                defs=defs, glow=("#c3cad4", 0.09))


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
    """Extension puzzle piece — Apple green at full strength on near-black."""
    defs = """
    <linearGradient id="x-piece" x1="20%" y1="0%" x2="80%" y2="100%">
      <stop offset="0%" stop-color="#4cf07a" />
      <stop offset="100%" stop-color="#1faf4e" />
    </linearGradient>"""
    # Square body, a tab bulging out of the right edge and a socket cut into
    # the bottom one — the two halves of a joint, which is what an extension is.
    piece = ("M 19.5 17 L 24 17 A 5.5 5.5 0 0 1 35 17 L 40.5 17 A 3.5 3.5 0 0 1 44 20.5 L 44 26 "
             "A 6 6 0 0 1 44 38 L 44 41.5 A 3.5 3.5 0 0 1 40.5 45 L 38 45 "
             "A 6 6 0 0 0 26 45 L 19.5 45 A 3.5 3.5 0 0 1 16 41.5 L 16 20.5 "
             "A 3.5 3.5 0 0 1 19.5 17 Z")
    body = f"""    <g transform="translate(-1.5, 1)">
      <path d="{piece}" fill="url(#x-piece)" />
      <path d="M 24 17 A 5.5 5.5 0 0 1 35 17 L 40.5 17 A 3.5 3.5 0 0 1 44 20.5 L 44 22
               A 3.5 3.5 0 0 0 40.5 18.5 L 34.6 18.5 A 5.5 5.5 0 0 0 24.4 18.5
               L 19.5 18.5 A 3.5 3.5 0 0 0 16 22 L 16 20.5 A 3.5 3.5 0 0 1 19.5 17 Z"
            fill="#ffffff" opacity="0.42" />
    </g>"""
    return tile(body, top="#16281c", bottom="#070c08",
                defs=defs, glow=("#30d158", 0.18))


# --------------------------------------------------------------------------
# video player
# --------------------------------------------------------------------------

def _video_body(screen_top, screen_bottom, sheen):
    return f"""    <g>
      <rect x="10.5" y="16" width="43" height="32" rx="6.5" ry="6.5" fill="url(#v-screen)" />
      <rect x="10.5" y="16" width="43" height="32" rx="6.5" ry="6.5" fill="none"
            stroke="#ffffff" stroke-opacity="{sheen}" stroke-width="1" />
      <path d="M 28.2 25.4 L 41.5 32 L 28.2 38.6 Z" fill="#ffffff" />
      <rect x="24" y="51" width="16" height="2.6" rx="1.3" fill="#ffffff" opacity="0.30" />
    </g>"""


def dark_video_svg():
    """A video player is a screen with a play head — not a FaceTime camera."""
    defs = """
    <linearGradient id="v-screen" x1="10%" y1="0%" x2="90%" y2="100%">
      <stop offset="0%" stop-color="#3a3f7a" />
      <stop offset="55%" stop-color="#232647" />
      <stop offset="100%" stop-color="#14152a" />
    </linearGradient>"""
    return tile(_video_body(None, None, 0.16), top="#22232e", bottom="#0a0a0f",
                defs=defs, glow=("#6b74ff", 0.14))


def light_video_svg():
    """Light-mode counterpart, same drawing on the light glass card."""
    return """<svg width="64" height="64" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <filter id="glass-shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="2.5" stdDeviation="2.5" flood-color="#000000" flood-opacity="0.25" />
    </filter>
    <linearGradient id="card" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#fdfdff" />
      <stop offset="100%" stop-color="#e6e8ef" />
    </linearGradient>
    <linearGradient id="inner-bevel" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.75" />
      <stop offset="35%" stop-color="#ffffff" stop-opacity="0.12" />
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0.05" />
    </linearGradient>
    <linearGradient id="v-screen" x1="10%" y1="0%" x2="90%" y2="100%">
      <stop offset="0%" stop-color="#5b62d6" />
      <stop offset="55%" stop-color="#3b3f9c" />
      <stop offset="100%" stop-color="#252a63" />
    </linearGradient>
    <clipPath id="card-clip">
      <rect width="56" height="56" x="4" y="4" rx="14" ry="14" />
    </clipPath>
  </defs>

  <g filter="url(#glass-shadow)">
    <rect width="56" height="56" x="4" y="4" rx="14" ry="14" fill="url(#card)" />
  </g>

  <g clip-path="url(#card-clip)">
    <rect x="10.5" y="16" width="43" height="32" rx="6.5" ry="6.5" fill="url(#v-screen)" />
    <path d="M 28.2 25.4 L 41.5 32 L 28.2 38.6 Z" fill="#ffffff" />
    <rect x="24" y="51" width="16" height="2.6" rx="1.3" fill="#3b3f9c" opacity="0.35" />
  </g>

  <rect width="55" height="55" x="4.5" y="4.5" rx="13.5" ry="13.5" fill="none" stroke="url(#inner-bevel)" stroke-width="1" />
</svg>"""


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
# registry: light source file -> builder for its dark counterpart
# --------------------------------------------------------------------------

HANDDRAWN = {
    "google-chrome.svg": dark_chrome_svg,
    "softwarecenter.svg": dark_appstore_svg,
    "eog.svg": dark_image_viewer_svg,
    "desktop-environment-gnome.svg": dark_tour_svg,
    "applications-system.svg": dark_gear_svg,
    "extensions.svg": dark_extensions_svg,
    "org.gnome.Totem.svg": dark_video_svg,
    # GNOME's newer player; shipped the FaceTime camera as its artwork.
    "Showtime.svg": dark_video_svg,
    "addressbook.svg": dark_contacts_svg,
    "gnome-maps.svg": dark_maps_svg,
    "accessories-camera.svg": dark_camera_svg,
}

# Artwork that must survive into dark mode untouched — Apple ships one Finder
# icon, not two, and the face *is* the card, so there is nothing to cut away.
VERBATIM = ("finder.svg",)
