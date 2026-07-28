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

def get_alphas(filepath):
    # Check inner boundary edges to detect if it's flat/circle vs full squircle
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
    # Deterministic gradient based on filename
    idx = int(hashlib.md5(filename.encode()).hexdigest(), 16) % len(PREMIUM_GRADIENTS)
    return PREMIUM_GRADIENTS[idx]

def apply_glassmorphism(filepath, content):
    filename = filepath.name
    alphas = get_alphas(str(filepath))
    b64_content = base64.b64encode(content.encode('utf-8')).decode('utf-8')
    data_uri = f"data:image/svg+xml;base64,{b64_content}"
    
    is_flat = any(a < 0.5 for a in alphas)
    color1, color2 = get_gradient(filename)
    
    # Base SVG envelope with 3D glass definitions
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
        # Puts the flat logo onto a premium 3D squircle base
        body = f'''
  <!-- Background with Shadow -->
  <rect width="56" height="56" x="4" y="4" rx="14" ry="14" fill="url(#bg-grad)" filter="url(#glass-shadow)" />
  
  <!-- Centered Icon -->
  <image href="{data_uri}" x="12" y="12" width="40" height="40"/>
  
  <!-- Glass Bevel Overlay -->
  <rect width="56" height="56" x="4" y="4" rx="14" ry="14" fill="none" stroke="url(#inner-bevel)" stroke-width="1.5" />
</svg>'''
    else:
        # Clips the full-bleed logo and injects the 3D glass borders over it
        body = f'''
  <g filter="url(#glass-shadow)">
    <g clip-path="url(#squircle-clip)">
      <image href="{data_uri}" x="0" y="0" width="64" height="64" />
    </g>
  </g>
  
  <!-- Glass Bevel Overlay matching the clip boundary exactly -->
  <rect width="56" height="56" x="4" y="4" rx="14" ry="14" fill="none" stroke="url(#inner-bevel)" stroke-width="1.5" />
</svg>'''

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(svg_header + body)
        
    return is_flat

def main():
    target_dir = Path("apps/scalable")
    flat_count = 0
    clip_count = 0
    
    for svg_file in target_dir.glob("*.svg"):
        if not svg_file.is_file() or svg_file.is_symlink():
            continue
            
        try:
            with open(svg_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            if 'data:image/svg+xml;base64' in content:
                continue
                
            is_flat = apply_glassmorphism(svg_file, content)
            if is_flat:
                flat_count += 1
            else:
                clip_count += 1
                
        except Exception as e:
            pass
            
    print(f"Ícones Planos (Glassmorphism Base): {flat_count}")
    print(f"Ícones Preenchidos (Glassmorphism Overlay): {clip_count}")

    # Generate Antigravity IDE icon with this engine!
    ag_png = Path("/usr/share/pixmaps/antigravity-ide.png")
    if ag_png.exists():
        with open(ag_png, 'rb') as f:
            b64 = base64.b64encode(f.read()).decode('utf-8')
        # Simulate a flat icon wrapping for it
        svg_header = f'''<svg width="64" height="64" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <filter id="glass-shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="2.5" stdDeviation="2.5" flood-color="#000000" flood-opacity="0.25" />
    </filter>
    <linearGradient id="inner-bevel" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.6" />
      <stop offset="25%" stop-color="#ffffff" stop-opacity="0.0" />
      <stop offset="75%" stop-color="#000000" stop-opacity="0.0" />
      <stop offset="100%" stop-color="#000000" stop-opacity="0.25" />
    </linearGradient>
    <linearGradient id="bg-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1a2a6c" />
      <stop offset="100%" stop-color="#b21f1f" />
    </linearGradient>
  </defs>'''
        body = f'''
  <rect width="56" height="56" x="4" y="4" rx="14" ry="14" fill="url(#bg-grad)" filter="url(#glass-shadow)" />
  <image href="data:image/png;base64,{b64}" x="12" y="12" width="40" height="40"/>
  <rect width="56" height="56" x="4" y="4" rx="14" ry="14" fill="none" stroke="url(#inner-bevel)" stroke-width="1.5" />
</svg>'''
        with open(target_dir / "antigravity-ide.svg", 'w') as f:
            f.write(svg_header + body)

if __name__ == "__main__":
    main()
