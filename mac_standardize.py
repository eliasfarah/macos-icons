import os
import subprocess
import base64
from pathlib import Path

def get_alphas(filepath):
    # Render SVG at 64x64. Check Top, Bottom, Left, Right + 4 Corners (slightly inner)
    # If ANY of these 8 points is highly transparent (< 0.5), it's a flat logo or circle.
    # macOS standard demands backgrounds for these.
    cmd = f"rsvg-convert -w 64 -h 64 '{filepath}' 2>/dev/null | magick - -format '%[fx:u.p{{32,8}}.a] %[fx:u.p{{32,56}}.a] %[fx:u.p{{8,32}}.a] %[fx:u.p{{56,32}}.a] %[fx:u.p{{14,14}}.a] %[fx:u.p{{50,14}}.a] %[fx:u.p{{14,50}}.a] %[fx:u.p{{50,50}}.a]' info: 2>/dev/null"
    try:
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        vals = res.stdout.strip().split()
        if len(vals) == 8:
            return [float(v) for v in vals]
    except Exception:
        pass
    # If error parsing (e.g. broken SVG), assume it's flat so it gets a wrapper
    return [0.0]*8

def process_svg(filepath, content):
    alphas = get_alphas(str(filepath))
    b64_content = base64.b64encode(content.encode('utf-8')).decode('utf-8')
    data_uri = f"data:image/svg+xml;base64,{b64_content}"
    
    is_flat = any(a < 0.5 for a in alphas)
    
    if is_flat:
        # Wrap flat icons in a clean, elegant white squircle with a soft shadow
        new_svg = f'''<svg width="64" height="64" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
    <feDropShadow dx="0" dy="1.5" stdDeviation="1.5" flood-color="#000000" flood-opacity="0.15" />
  </filter>
  
  <rect width="56" height="56" x="4" y="4" rx="14" ry="14" fill="#ffffff" filter="url(#shadow)" />
  <image href="{data_uri}" x="12" y="12" width="40" height="40"/>
</svg>'''
    else:
        # Clip full-bleed icons perfectly to squircle
        new_svg = f'''<svg width="64" height="64" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <clipPath id="squircle-clip">
      <rect width="56" height="56" x="4" y="4" rx="14" ry="14" />
    </clipPath>
  </defs>
  <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
    <feDropShadow dx="0" dy="1.5" stdDeviation="1.5" flood-color="#000000" flood-opacity="0.15" />
  </filter>

  <g filter="url(#shadow)">
    <g clip-path="url(#squircle-clip)">
      <image href="{data_uri}" x="0" y="0" width="64" height="64" />
    </g>
  </g>
</svg>'''
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_svg)
        
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
                
            is_flat = process_svg(svg_file, content)
            if is_flat:
                flat_count += 1
            else:
                clip_count += 1
                
        except Exception as e:
            print(f"Erro em {svg_file}: {e}")
            
    print(f"Ícones Planos (Fundo Branco): {flat_count}")
    print(f"Ícones Preenchidos (Clipados): {clip_count}")

if __name__ == "__main__":
    main()
