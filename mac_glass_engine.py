import os
import subprocess
import base64
import hashlib
from pathlib import Path

# Premium, soft pastel and neutral gradients for flat logos
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

def get_gradient(filename):
    idx = int(hashlib.md5(filename.encode()).hexdigest(), 16) % len(PREMIUM_GRADIENTS)
    return PREMIUM_GRADIENTS[idx]

def apply_glassmorphism(filepath, bytes_data, is_png=False):
    filename = filepath.name
    alphas = get_alphas(str(filepath), is_png=is_png)
    
    b64_content = base64.b64encode(bytes_data).decode('utf-8')
    mime_type = "image/png" if is_png else "image/svg+xml"
    data_uri = f"data:{mime_type};base64,{b64_content}"
    
    is_flat = any(a < 0.5 for a in alphas)
    color1, color2 = get_gradient(filename)
    
    svg_header = f'''<svg width="64" height="64" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <!-- Elegant Apple-style Drop Shadow -->
    <filter id="glass-shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="2.5" stdDeviation="2.5" flood-color="#000000" flood-opacity="0.25" />
    </filter>
    
    <!-- 3D Bevel/Glass Highlights -->
    <linearGradient id="inner-bevel" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.6" />
      <stop offset="25%" stop-color="#ffffff" stop-opacity="0.0" />
      <stop offset="75%" stop-color="#000000" stop-opacity="0.0" />
      <stop offset="100%" stop-color="#000000" stop-opacity="0.25" />
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

    if is_flat:
        body = f'''
  <!-- Background with Shadow -->
  <rect width="56" height="56" x="4" y="4" rx="14" ry="14" fill="url(#bg-grad)" filter="url(#glass-shadow)" />
  
  <!-- Centered Icon -->
  <image href="{data_uri}" x="12" y="12" width="40" height="40"/>
  
  <!-- Glass Bevel Overlay -->
  <rect width="56" height="56" x="4" y="4" rx="14" ry="14" fill="none" stroke="url(#inner-bevel)" stroke-width="1.5" />
</svg>'''
    else:
        body = f'''
  <g filter="url(#glass-shadow)">
    <g clip-path="url(#squircle-clip)">
      <image href="{data_uri}" x="0" y="0" width="64" height="64" />
    </g>
  </g>
  
  <!-- Glass Bevel Overlay matching the clip boundary exactly -->
  <rect width="56" height="56" x="4" y="4" rx="14" ry="14" fill="none" stroke="url(#inner-bevel)" stroke-width="1.5" />
</svg>'''

    target_svg_path = filepath if filepath.suffix.lower() == '.svg' else filepath.with_suffix('.svg')
    with open(target_svg_path, 'w', encoding='utf-8') as f:
        f.write(svg_header + body)
        
    return target_svg_path, is_flat

def process_directory(dir_path):
    flat_count = 0
    clip_count = 0
    processed_count = 0
    
    if not dir_path.exists():
        return 0, 0, 0
        
    # 1. Clean up Apple sidecar files (._*)
    for junk in dir_path.glob("._*"):
        try:
            junk.unlink()
        except Exception:
            pass
            
    # 2. Iterate through files
    for file_path in list(dir_path.glob("*")):
        if not file_path.is_file() or file_path.is_symlink() or file_path.name.startswith("._"):
            continue
            
        bytes_data = file_path.read_bytes()
        is_png = bytes_data.startswith(b'\x89PNG')
        
        # Check if corresponding SVG already has glassmorphism
        target_svg_path = file_path if file_path.suffix.lower() == '.svg' else file_path.with_suffix('.svg')
        if target_svg_path.exists():
            try:
                svg_text = target_svg_path.read_text(encoding='utf-8', errors='ignore')
                if 'glass-shadow' in svg_text and 'inner-bevel' in svg_text:
                    continue
            except Exception:
                pass
                
        target_svg, is_flat = apply_glassmorphism(file_path, bytes_data, is_png=is_png)
        processed_count += 1
        if is_flat:
            flat_count += 1
        else:
            clip_count += 1
            
        # If original file was a .png file, render glassmorphic PNG fallback matching the SVG
        if file_path.suffix.lower() == '.png':
            try:
                subprocess.run(f"rsvg-convert -w 64 -h 64 '{target_svg}' -o '{file_path}' 2>/dev/null", shell=True)
            except Exception:
                pass

    return processed_count, flat_count, clip_count

def main():
    # Fix misnamed files if present
    misnamed_builder = Path("apps/scalable/gnome-buildersvg")
    if misnamed_builder.exists():
        misnamed_builder.rename("apps/scalable/gnome-builder.svg")
        print("Renomeado gnome-buildersvg -> gnome-builder.svg")
        
    dirs_to_process = [
        Path("apps/scalable")
    ]
    
    for dir_path in dirs_to_process:
        print(f"Processando {dir_path}...")
        total, flat, clip = process_directory(dir_path)
        print(f"{dir_path}: {total} ícones novos processados ({flat} planos, {clip} preenchidos)")
    
    # Custom/System Pixmap Icons (Antigravity IDE & BB Launcher)
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
                apply_glassmorphism(target_svg, bytes_data, is_png=True)
                print(f"Ícone {dest_name} gerado/atualizado com sucesso!")
        
    print("Atualizando cache do tema de ícones...")
    subprocess.run("touch .icon-theme.cache 2>/dev/null", shell=True)
    subprocess.run("gtk-update-icon-cache -f -t . 2>/dev/null", shell=True)

if __name__ == "__main__":
    main()
