# Project Rules for macos-icons

## Repository Update Preference

- After completing and validating requested work in this project, commit the
  relevant changes and push them to `origin/main`, unless the user explicitly
  asks not to publish them.
- Never include unrelated pre-existing work in that commit.

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
`softwarecenter.svg` also covers `gnome-software.svg`, while
`system-software-install.svg` deliberately has its own package-and-controls
artwork. The ChatGPT entry covers the Chrome web-app shortcut
`chrome-cadlkienfkclaiaibeoongdcgmdikeeg-Default.svg`.

Currently hand-drawn: Calendar, text-editor notepad, Chrome, software store,
Web compass, image viewer, GNOME Tour, settings cog, applications grid, Extension Manager,
document scanner, red help buoy, video player, music library, audio player,
Maps, Camera, Contacts. Empty light-mode placeholders are repaired by exact
filename for Celeste, Inscryption, Papers Please, OpenRA D2K, OneShot,
Stardew Valley, Terraria, Undertale, SimpleX Chat, Clapgrep, Roblox and
Ricochlime; this must remain name-based because unrelated apps share identical
blank artwork hashes. ChatGPT is generated from its own artwork
(`dark_mono_glyph_svg`): the knot is pure black ink on a white card, so
reading the card's luminance as the mark's *alpha* re-inks it white with no
halo — a plain card-cut would leave grey fringing on every strand.

`HD.VERBATIM` lists artwork that must reach dark mode untouched. Finder is
not verbatim: its light artwork remains the exact original, while
`dark_handdrawn.dark_finder_svg` uses the compact sculpted blue face on a
graphite Liquid Glass tile, with asymmetric eyes and a blue-to-black smile.

GNOME Connections is also a coordinated light/dark pair. The light source is
the ice-glass globe, live route and sculpted cursor in
`apps/scalable/gnome-connections.svg`; its dark counterpart is registered in
`HD.HANDDRAWN` so aliases such as `org.gnome.Connections.svg` follow it by
artwork hash.

Do **not** blanket-exempt a whole name family from the pipeline (an earlier
`"chrom" in name` rule quietly kept 60-odd Chrome web-app icons, ChatGPT
among them, in full light mode).

### GNOME Extensions visual direction

The dark GNOME Extensions icon follows the restrained macOS system-icon
language: one sculpted ivory puzzle piece on deep emerald glass. Preserve the
single clear silhouette, subtle material depth, generous negative space and
legibility at 32–64 px. Do not add tools, circuit traces or other secondary
metaphors; they make the icon read as a repair utility instead of a premium
system control. The primary file is `extensions.svg`; these aliases resolve to
it and must continue to follow automatically:

- `67EF_addoninstaller.0.svg`
- `cs-extensions.svg`
- `gnome-shell-extension-prefs.svg`
- `org.gnome.Extensions.svg`
- `org.gnome.Shell.Extensions.svg`

### Extension Manager app visual direction

`com.mattjakeman.ExtensionManager.svg` is a distinct application and must not
resolve to the generic `preferences-plugin.svg` gear. Its identity is the
official blue puzzle piece divided into four tonal quadrants. The light icon
uses an ice-glass tile; the dark counterpart uses sapphire-black glass. Keep
the quadrant structure, blue palette, sculpted edge and clean dock-size
silhouette. Do not add a gear, wrench or circuit detail.

`org.gnome.Totem.svg` and `Showtime.svg` both shipped **FaceTime's green
camera** as the video player's artwork. Both now carry the same cinematic
screen, glass play control and progress timeline
(`dark_handdrawn.light_video_svg`). When an app looks wrong in dark mode,
check whether it is wrong in light mode too — and check *which* file the
desktop actually resolves, since GNOME's video player is Showtime now, not
Totem.
