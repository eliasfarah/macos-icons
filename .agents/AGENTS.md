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

Hand-drawn icons get hand-drawn dark counterparts, not automatic ones —
currently the Calendar and the text-editor notepad, keyed on artwork hash so
every alias that embeds the same drawing picks it up too.
