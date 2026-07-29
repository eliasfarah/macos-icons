# Project Rules for macos-icons

## Glassmorphism Engine & Directory Scope Rules
- **Only process `apps/scalable`**: The glassmorphism engine (`mac_glass_engine.py`) must ONLY process icons inside `apps/scalable`.
- **DO NOT touch `places/scalable`**: Never modify or attempt to auto-glassmorph icons in `places/scalable` (folders, trash cans, places icons). Keep user's original places icons intact.

## Specific App Icon Requirements
- **ChatGPT Icon**: Must feature the official black OpenAI knot logo centered on a 3D Glassmorphic WHITE background card (`#ffffff` gradient) with Apple drop shadow and 3D glass bevel overlay.
- **Google Gemini Icon**: Must feature the official Google Gemini 4-point star/sparkle logo with blue/purple gradient on dark glass background (`#1e1f24` -> `#0f1013`).
- **Apple Finder Icon**: Must embed 100% exact original Finder artwork provided by user.

## Dark Mode (`mac_dark_engine.py` -> `apps-dark/scalable`)

Light mode (`apps/scalable`) is the source of truth. The dark engine reads the
original artwork back out of each light icon and rebuilds it; it never edits
light icons.

Design rules, in priority order:

1. **The canvas goes dark, the logo does not.** A white or coloured card becomes
   a near-black tile tinted with the icon's own hue. The artwork on it keeps its
   brand colours at full strength.
2. **Never invert artwork.** Inversion turns GIMP's brown Wilber blue and
   Thunderbird's blue bird cream. Brand identity is not negotiable.
3. **Never globally dim or desaturate.** A flat brightness multiply reads as a
   dirty icon, not a designed one.
4. **Lift artwork that would disappear.** A black wordmark on a black tile is
   invisible, so its *lightness* is flipped while hue and saturation stay.
5. **Same tile geometry as light mode** (56x56 squircle at 4,4, radius 14), so
   the two sets read as one family.
6. **Dark tiles need an edge**: a hairline top rim highlight plus an outer
   shadow, or the icon melts into a dark dock.

Icons that are already dark (terminals, IDEs, OBS, Antigravity, bb-launcher)
are detected by their own background luminance and passed through untouched.

### Hand-drawn dark icons (`dark_handdrawn.py`)

The automatic route cuts the light card away from the artwork, which only
works when the card and the artwork are two different things. Where the card
**is** the artwork — Finder's face, the App Store "A", a full-bleed photo —
the cut leaves a ragged hole, so the dark variant is drawn by hand in
`dark_handdrawn.py` and registered in its `HANDDRAWN` map.

Registration is by *light source filename*, but lookup is by **artwork hash**,
so every alias that embeds the same drawing follows along: one entry for
`softwarecenter.svg` also covers `gnome-software.svg` and
`system-software-install.svg`, and the ChatGPT entry covers the Chrome web-app
shortcut `chrome-cadlkienfkclaiaibeoongdcgmdikeeg-Default.svg`.

Currently hand-drawn: Calendar, text-editor notepad, Chrome, App Store,
image viewer, GNOME Tour, settings cog, extensions puzzle, video player,
Maps, Camera, Contacts. ChatGPT is generated from its own artwork
(`dark_mono_glyph_svg`): the knot is pure black ink on a white card, so
reading the card's luminance as the mark's *alpha* re-inks it white with no
halo — a plain card-cut would leave grey fringing on every strand.

`HD.VERBATIM` lists artwork that must reach dark mode untouched. Finder is
there because Apple ships one Finder icon, not two.

Do **not** blanket-exempt a whole name family from the pipeline (an earlier
`"chrom" in name` rule quietly kept 60-odd Chrome web-app icons, ChatGPT
among them, in full light mode).

The two light-mode edits made so far: `org.gnome.Totem.svg` and
`Showtime.svg` both shipped **FaceTime's green camera** as the video player's
artwork. Both now carry a screen-and-play-head drawing
(`dark_handdrawn.light_video_svg`). When an app looks wrong in dark mode,
check whether it is wrong in light mode too — and check *which* file the
desktop actually resolves, since GNOME's video player is Showtime now, not
Totem.
