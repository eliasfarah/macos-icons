import os
import base64
from pathlib import Path
import random

def has_squircle(svg_content):
    # Procura grosseiramente por rx="13" ou width="56"
    return 'rx="13' in svg_content or 'ry="13' in svg_content or 'width="56"' in svg_content

def wrap_svg(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if has_squircle(content):
            return False
            
        # Encode original SVG to base64
        b64_content = base64.b64encode(content.encode('utf-8')).decode('utf-8')
        data_uri = f"data:image/svg+xml;base64,{b64_content}"
        
        # Cores aleatórias bonitas e neutras para o gradiente de fundo
        colors = [
            ("#2b5876", "#4e4376"),
            ("#3a1c71", "#d76d77"),
            ("#283c86", "#45a247"),
            ("#159957", "#155799"),
            ("#11998e", "#38ef7d"),
            ("#2c3e50", "#3498db"),
            ("#e52d27", "#b31217"),
            ("#4b6cb7", "#182848"),
            ("#304352", "#d7d2cc"),
            ("#414d0b", "#727a17")
        ]
        color1, color2 = random.choice(colors)
        grad_id = f"bg_grad_{random.randint(1000, 9999)}"
        
        new_svg = f'''<svg width="64" height="64" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="{grad_id}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{color1}"/>
      <stop offset="100%" stop-color="{color2}"/>
    </linearGradient>
  </defs>
  <rect width="56" height="56" x="4" y="4" rx="13" ry="13" fill="url(#{grad_id})"/>
  <image href="{data_uri}" x="12" y="12" width="40" height="40"/>
</svg>'''

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_svg)
            
        return True
    except Exception as e:
        return False

def main():
    target_dir = Path("/home/farah/Projects/AZ-OS-3D-Prime-Icons/apps/scalable")
    modified_count = 0
    for svg_file in target_dir.glob("*.svg"):
        if svg_file.is_file() and not svg_file.is_symlink():
            if wrap_svg(svg_file):
                modified_count += 1
                
    print(f"Total de ícones envelopados de forma segura: {modified_count}")

    # Também gerar o ícone do Antigravity IDE (copiando do /usr/share/pixmaps)
    antigravity_src = Path("/usr/share/pixmaps/antigravity-ide.png")
    antigravity_dest = target_dir / "antigravity-ide.svg"
    if antigravity_src.exists():
        with open(antigravity_src, 'rb') as f:
            img_data = f.read()
        b64_img = base64.b64encode(img_data).decode('utf-8')
        png_data_uri = f"data:image/png;base64,{b64_img}"
        
        ag_svg = f'''<svg width="64" height="64" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
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
    <clipPath id="squircle-clip">
      <rect width="56" height="56" x="4" y="4" rx="14" ry="14" />
    </clipPath>
  </defs>
  <g filter="url(#glass-shadow)">
    <g clip-path="url(#squircle-clip)">
      <image href="{png_data_uri}" x="0" y="0" width="64" height="64" />
    </g>
  </g>
  <rect width="56" height="56" x="4" y="4" rx="14" ry="14" fill="none" stroke="url(#inner-bevel)" stroke-width="1.5" />
</svg>'''
        with open(antigravity_dest, 'w', encoding='utf-8') as f:
            f.write(ag_svg)
        print("Ícone do Antigravity IDE gerado com sucesso!")

if __name__ == "__main__":
    main()
