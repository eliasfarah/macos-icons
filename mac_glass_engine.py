import os
import sys
import subprocess
import base64
import hashlib
from pathlib import Path
import shutil
import re
import tempfile

# Premium, soft pastel and neutral gradients for flat logos (Light Mode)
PREMIUM_GRADIENTS = [
    ("#fdfbfb", "#ebedee"), # Very light gray/white
    ("#e0c3fc", "#8ec5fc"), # Soft lavender to blue
    ("#e6e9f0", "#eef1f5"), # Steel gray
    ("#accbee", "#e7f0fd"), # Soft baby blue
    ("#c1dfc4", "#deecdd"), # Mint green
    ("#ffd194", "#70e1f5"), # Warm peach to sky blue
    ("#ffecd2", "#fcb69f"), # Peach fuzz
    ("#cfd9df", "#e2ebf0"), # Cloud gray
    ("#a1c4fd", "#c2e9fb"), # Ocean blue
    ("#ff9a9e", "#fecfef"), # Soft pink
    ("#f6d365", "#fda085"), # Sunrise
    ("#d4fc79", "#96e6a1"), # Fresh lime
    ("#84fab0", "#8fd3f4")  # Aqua
]

# Premium Dark Gradients for Dark Mode (Apple OLED style)
PREMIUM_DARK_GRADIENTS = [
    ("#1c1c1e", "#000000"), # Standard OLED Black
    ("#1e1f24", "#050505"), # Deep Dark
    ("#121212", "#000000"), # Pitch Black
    ("#222327", "#0a0a0c"), # Soft Midnight
    ("#191a21", "#08090b"), # Deep Blue Black
]

def is_chatgpt(filename):
    name = filename.lower()
    return 'chatgpt' in name

def is_gemini(filename):
    name = filename.lower()
    return name in ['gemini.svg', 'com.google.gemini.svg', 'google-gemini.svg', 'google-gemini-desktop.svg', 'gemini-cli.svg',
                    'gemini.png', 'com.google.gemini.png', 'google-gemini.png', 'google-gemini-desktop.png', 'gemini-cli.png']

def is_finder(filename):
    name = filename.lower()
    return name in ['finder.svg', 'apple-finder.svg', 'mac-finder.svg', 'finder-mac.svg',
                    'finder.png', 'apple-finder.png', 'mac-finder.png', 'finder-mac.png']

def is_chrome(filename):
    name = filename.lower()
    return 'chrom' in name

def get_alphas(filepath, is_png=False):
    if is_png:
        cmd = f"magick '{filepath}' -resize 64x64! -format '%[fx:u.p{{32,8}}.a] %[fx:u.p{{32,56}}.a] %[fx:u.p{{8,32}}.a] %[fx:u.p{{56,32}}.a] %[fx:u.p{{14,14}}.a] %[fx:u.p{{50,14}}.a] %[fx:u.p{{14,50}}.a] %[fx:u.p{{50,50}}.a]' info: 2>/dev/null"
    else:
        cmd = f"rsvg-convert -w 64 -h 64 '{filepath}' 2>/dev/null | magick - -format '%[fx:u.p{{32,8}}.a] %[fx:u.p{{32,56}}.a] %[fx:u.p{{8,32}}.a] %[fx:u.p{{56,32}}.a] %[fx:u.p{{14,14}}.a] %[fx:u.p{{50,14}}.a] %[fx:u.p{{14,50}}.a] %[fx:u.p{{50,50}}.a]' info: 2>/dev/null"
    try:
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        vals = res.stdout.strip().split()
        if len(vals) == 8:
            return [float(v) for v in vals]
    except Exception:
        pass
    return [0.0]*8

def get_gradient(filename, is_dark=False):
    if is_chatgpt(filename):
        return ("#ffffff", "#f5f5f7")
    if is_gemini(filename):
        return ("#1e1f24", "#0f1013")

    gradients = PREMIUM_DARK_GRADIENTS if is_dark else PREMIUM_GRADIENTS
    idx = int(hashlib.md5(filename.encode()).hexdigest(), 16) % len(gradients)
    return gradients[idx]

def apply_glassmorphism(filepath, bytes_data, is_png=False, is_dark=False, out_dir=None):
    filename = filepath.name
    
    if out_dir:
        target_svg_path = out_dir / (filepath.stem + '.svg')
    else:
        target_svg_path = filepath if filepath.suffix.lower() == '.svg' else filepath.with_suffix('.svg')

    if is_finder(filename) or is_chrome(filename):
        if is_png:
            b64_content = base64.b64encode(bytes_data).decode('utf-8')
            mime_type = "image/png"
            data_uri = f"data:{mime_type};base64,{b64_content}"
            raw_svg = f'<svg width="64" height="64" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"><image href="{data_uri}" x="0" y="0" width="64" height="64"/></svg>'
            target_svg_path.write_text(raw_svg, encoding='utf-8')
        else:
            if target_svg_path != filepath:
                target_svg_path.write_bytes(bytes_data)
        return target_svg_path, False

    ext = '.png' if is_png else '.svg'
    with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as tmp:
        tmp.write(bytes_data)
        tmp_path = tmp.name

    try:
        alphas = get_alphas(tmp_path, is_png=is_png)
        is_flat = any(a < 0.5 for a in alphas)
        
        is_effective_dark = is_dark
        if is_chatgpt(filename):
            is_effective_dark = False
        if is_gemini(filename):
            is_effective_dark = True

        needs_invert = False
        needs_smart_invert = False
        
        # Calculate edge brightness to detect white backgrounds
        edge_brightness = 0.0
        if not is_flat:
            if is_png:
                cmd_eb = f"magick '{tmp_path}' -resize 64x64! -colorspace gray -format '%[fx:u.p{{32,8}}] %[fx:u.p{{32,56}}] %[fx:u.p{{8,32}}] %[fx:u.p{{56,32}}]' info: 2>/dev/null"
            else:
                cmd_eb = f"rsvg-convert -w 64 -h 64 '{tmp_path}' 2>/dev/null | magick - -colorspace gray -format '%[fx:u.p{{32,8}}] %[fx:u.p{{32,56}}] %[fx:u.p{{8,32}}] %[fx:u.p{{56,32}}]' info: 2>/dev/null"
            try:
                res_eb = subprocess.run(cmd_eb, shell=True, capture_output=True, text=True)
                vals_eb = res_eb.stdout.strip().split()
                if len(vals_eb) == 4:
                    edge_brightness = sum(float(v) for v in vals_eb) / 4.0
            except Exception:
                pass

        if is_effective_dark:
            if is_flat:
                cmd = f"magick '{tmp_path}' -background black -flatten -colorspace gray -format '%[fx:mean]' info: 2>/dev/null"
                res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                out = res.stdout.strip()
                if out and float(out) < 0.2:
                    needs_invert = True
            else:
                if edge_brightness > 0.8:
                    needs_smart_invert = True
                    
        # ChatGPT rule: must be black logo on white bg. If logo is white, invert to black!
        if is_chatgpt(filename) and is_flat:
            cmd = f"magick '{tmp_path}' -background white -flatten -colorspace gray -format '%[fx:mean]' info: 2>/dev/null"
            res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            out = res.stdout.strip()
            if out and float(out) > 0.8:
                needs_invert = True
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
            
    b64_content = base64.b64encode(bytes_data).decode('utf-8')
    mime_type = "image/png" if is_png else "image/svg+xml"
    data_uri = f"data:{mime_type};base64,{b64_content}"
    
    color1, color2 = get_gradient(filename, is_dark)
    
    if is_effective_dark:
        bevel_top = "#ffffff"
        bevel_top_op = "0.4"
        bevel_bot = "#000000"
        bevel_bot_op = "0.8"
        shadow_op = "0.6"
    else:
        bevel_top = "#ffffff"
        bevel_top_op = "0.6"
        bevel_bot = "#000000"
        bevel_bot_op = "0.25"
        shadow_op = "0.25"
    
    svg_header = f'''<svg width="64" height="64" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <!-- Elegant Apple-style Drop Shadow -->
    <filter id="glass-shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="2.5" stdDeviation="2.5" flood-color="#000000" flood-opacity="{shadow_op}" />
    </filter>
    
    <!-- 3D Bevel/Glass Highlights -->
    <linearGradient id="inner-bevel" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="{bevel_top}" stop-opacity="{bevel_top_op}" />
      <stop offset="25%" stop-color="{bevel_top}" stop-opacity="0.0" />
      <stop offset="75%" stop-color="{bevel_bot}" stop-opacity="0.0" />
      <stop offset="100%" stop-color="{bevel_bot}" stop-opacity="{bevel_bot_op}" />
    </linearGradient>
    
    <!-- Premium Soft Background Gradient -->
    <linearGradient id="bg-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{color1}" />
      <stop offset="100%" stop-color="{color2}" />
    </linearGradient>

    <!-- Unified Squircle Mask -->
    <clipPath id="squircle-clip">
      <rect width="56" height="56" x="4" y="4" rx="14" ry="14" />
    </clipPath>
  </defs>'''

    # Apple iOS 18 Dark Mode filter: darken + desaturate the icon art
    dark_filter_defs = ''
    apply_dark_mode_filter = is_effective_dark and not is_flat and not needs_smart_invert
    if apply_dark_mode_filter:
        dark_filter_defs = '''
    <!-- Apple Dark Mode: Darken & Desaturate Icon Art -->
    <filter id="dark-mode" x="0%" y="0%" width="100%" height="100%" color-interpolation-filters="sRGB">
      <feColorMatrix type="saturate" values="1.0" />
      <feComponentTransfer>
        <feFuncR type="linear" slope="0.85" intercept="0.0"/>
        <feFuncG type="linear" slope="0.85" intercept="0.0"/>
        <feFuncB type="linear" slope="0.85" intercept="0.0"/>
      </feComponentTransfer>
    </filter>'''
        # Insert before </defs>
        svg_header = svg_header.replace('</defs>', dark_filter_defs + '\n  </defs>')

    glow_element = ''
    if is_effective_dark and is_flat:
        glow_element = '\n  <circle cx="32" cy="32" r="24" fill="#ffffff" filter="blur(12px)" opacity="0.25" />'

    filter_attr = ''
    if needs_invert:
        filter_attr = ' style="filter: invert(1) hue-rotate(180deg);"'
    elif needs_smart_invert:
        filter_attr = ' style="filter: invert(1) hue-rotate(180deg) brightness(1.2) saturate(1.2);"'

    # We scale slightly in dark mode if flat
    if is_flat:
        if is_effective_dark:
            body = f'''
  <!-- Background with Shadow -->
  <rect width="56" height="56" x="4" y="4" rx="14" ry="14" fill="url(#bg-grad)" filter="url(#glass-shadow)" />{glow_element}
  <!-- Centered Icon (Scaled Up for Dark Mode) -->
  <image{filter_attr} href="{data_uri}" x="10" y="10" width="44" height="44"/>
  
  <!-- Glass Bevel Overlay -->
  <rect width="56" height="56" x="4" y="4" rx="14" ry="14" fill="none" stroke="url(#inner-bevel)" stroke-width="1.5" />
</svg>'''
        else:
            body = f'''
  <!-- Background with Shadow -->
  <rect width="56" height="56" x="4" y="4" rx="14" ry="14" fill="url(#bg-grad)" filter="url(#glass-shadow)" />
  <!-- Centered Icon -->
  <image{filter_attr} href="{data_uri}" x="12" y="12" width="40" height="40"/>
  
  <!-- Glass Bevel Overlay -->
  <rect width="56" height="56" x="4" y="4" rx="14" ry="14" fill="none" stroke="url(#inner-bevel)" stroke-width="1.5" />
</svg>'''
    else:
        if is_effective_dark:
            filter_ref = ' filter="url(#dark-mode)"' if apply_dark_mode_filter else ''
            body = f'''
  <g filter="url(#glass-shadow)">
    <g clip-path="url(#squircle-clip)">
      <image{filter_attr}{filter_ref} href="{data_uri}" x="0" y="0" width="64" height="64" />
    </g>
  </g>
  
  <!-- Subtle dark vignette overlay -->
  <rect width="56" height="56" x="4" y="4" rx="14" ry="14" fill="#000000" opacity="0.15" clip-path="url(#squircle-clip)" />
  
  <!-- Glass Bevel Overlay matching the clip boundary exactly -->
  <rect width="56" height="56" x="4" y="4" rx="14" ry="14" fill="none" stroke="url(#inner-bevel)" stroke-width="1.5" />
</svg>'''
        else:
            body = f'''
  <g filter="url(#glass-shadow)">
    <g clip-path="url(#squircle-clip)">
      <image{filter_attr} href="{data_uri}" x="0" y="0" width="64" height="64" />
    </g>
  </g>
  
  <!-- Glass Bevel Overlay matching the clip boundary exactly -->
  <rect width="56" height="56" x="4" y="4" rx="14" ry="14" fill="none" stroke="url(#inner-bevel)" stroke-width="1.5" />
</svg>'''

    with open(target_svg_path, 'w', encoding='utf-8') as f:
        f.write(svg_header + body)
        
    return target_svg_path, is_flat

def process_directory(dir_path, is_dark=False):
    flat_count = 0
    clip_count = 0
    processed_count = 0
    
    if not dir_path.exists():
        return 0, 0, 0
        
    out_dir = None
    if is_dark:
        out_dir = Path("apps-dark/scalable")
        out_dir.mkdir(parents=True, exist_ok=True)
        
    for junk in dir_path.glob("._*"):
        try:
            junk.unlink()
        except Exception:
            pass
            
    for file_path in list(dir_path.glob("*")):
        if not file_path.is_file() or file_path.is_symlink() or file_path.name.startswith("._"):
            continue
            
        bytes_data = file_path.read_bytes()
        is_png = bytes_data.startswith(b'\x89PNG')
        
        target_svg_path = file_path if file_path.suffix.lower() == '.svg' else file_path.with_suffix('.svg')
        if target_svg_path.exists() and not (is_finder(file_path.name) or is_chrome(file_path.name)):
            try:
                svg_text = target_svg_path.read_text(encoding='utf-8', errors='ignore')
                if 'glass-shadow' in svg_text and 'inner-bevel' in svg_text:
                    if not is_dark:
                        continue
                    else:
                        match = re.search(r'<image[^>]*href="([^"]+)"', svg_text)
                        if match:
                            data_uri = match.group(1)
                            header, b64 = data_uri.split(',', 1)
                            bytes_data = base64.b64decode(b64)
                            is_png = 'image/png' in header
            except Exception:
                pass
                
        target_svg, is_flat = apply_glassmorphism(file_path, bytes_data, is_png=is_png, is_dark=is_dark, out_dir=out_dir)
        processed_count += 1
        if is_flat:
            flat_count += 1
        else:
            clip_count += 1
            
        if not is_dark and file_path.suffix.lower() == '.png':
            try:
                subprocess.run(f"rsvg-convert -w 64 -h 64 '{target_svg}' -o '{file_path}' 2>/dev/null", shell=True)
            except Exception:
                pass

    if out_dir:
        for file_path in dir_path.glob("*"):
            if file_path.is_symlink():
                try:
                    target = os.readlink(file_path)
                    new_link = out_dir / file_path.name
                    if not new_link.exists() and not new_link.is_symlink():
                        os.symlink(target, new_link)
                except Exception:
                    pass

    return processed_count, flat_count, clip_count

def main():
    if "--dark" in sys.argv:
        # Dark mode moved to its own engine, which rebuilds each icon as a
        # designed dark variant instead of filtering the light one.
        print("Modo escuro agora é gerado por mac_dark_engine.py — delegando...")
        os.execvp(sys.executable, [sys.executable,
                                   str(Path(__file__).parent / "mac_dark_engine.py")]
                  + [a for a in sys.argv[1:] if a != "--dark"])

    is_dark = False

    misnamed_builder = Path("apps/scalable/gnome-buildersvg")
    if misnamed_builder.exists():
        misnamed_builder.rename("apps/scalable/gnome-builder.svg")
        print("Renomeado gnome-buildersvg -> gnome-builder.svg")
        
    dirs_to_process = [
        Path("apps/scalable")
    ]
    
    for dir_path in dirs_to_process:
        print(f"Processando {dir_path} (Modo: {'Escuro' if is_dark else 'Claro'})...")
        total, flat, clip = process_directory(dir_path, is_dark=is_dark)
        out_msg = f"apps-dark/scalable" if is_dark else str(dir_path)
        print(f"{out_msg}: {total} ícones processados ({flat} planos, {clip} preenchidos)")
    
    if not is_dark:
        pixmaps_to_convert = [
            ("antigravity-ide.png", ["antigravity-ide.svg"]),
            ("bb_launcher.png", ["bb_launcher.svg", "bb-launcher.svg"])
        ]
        apps_dir = Path("apps/scalable")
        for src_name, dest_names in pixmaps_to_convert:
            src_path = Path("/usr/share/pixmaps") / src_name
            if src_path.exists():
                bytes_data = src_path.read_bytes()
                for dest_name in dest_names:
                    target_svg = apps_dir / dest_name
                    apply_glassmorphism(target_svg, bytes_data, is_png=True, is_dark=False)
                    print(f"Ícone {dest_name} gerado/atualizado com sucesso!")
            
    print("Atualizando cache do tema de ícones...")
    subprocess.run("touch .icon-theme.cache 2>/dev/null", shell=True)
    subprocess.run("gtk-update-icon-cache -f -t . 2>/dev/null", shell=True)
    
    if is_dark:
        if Path("macos-icons-dark").exists():
            subprocess.run("touch macos-icons-dark/.icon-theme.cache 2>/dev/null", shell=True)
            subprocess.run("gtk-update-icon-cache -f -t macos-icons-dark 2>/dev/null", shell=True)

if __name__ == "__main__":
    main()
