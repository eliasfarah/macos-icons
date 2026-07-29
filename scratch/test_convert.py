import re
from pathlib import Path
import base64
import tempfile
import subprocess
import os

svg_text = Path('apps/scalable/github-desktop.svg').read_text(encoding='utf-8')
match = re.search(r'<image href="([^"]+)"', svg_text)
if match:
    data_uri = match.group(1)
    header, b64 = data_uri.split(',', 1)
    bytes_data = base64.b64decode(b64)
    ext = '.png' if 'image/png' in header else '.svg'
    
    with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as tmp:
        tmp.write(bytes_data)
        tmp_path = tmp.name
        
    print(f"Extracted inner image to {tmp_path}")
    
    # Check brightness using a black background flatten trick.
    # If a logo is black on transparent, flattening on black makes it all black (mean ~0).
    # If a logo is white on transparent, flattening on black leaves white (mean > 0).
    # Wait, if the logo is colored, it will also be > 0.
    # So if mean_black_bg < 0.1, the logo is very dark/black!
    
    cmd = f"magick '{tmp_path}' -background black -flatten -colorspace gray -format '%[fx:mean]' info: 2>/dev/null"
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    out = res.stdout.strip()
    print(f"Brightness of inner image on black background: {out}")
    if out and float(out) < 0.1:
        print("  -> Logo is dark! Applying invert filter.")
        # Apply filter
        replacement = r'<image style="filter: invert(1) hue-rotate(180deg) brightness(1.2);" href="\1"'
        svg_text = re.sub(r'<image href="([^"]+)"', replacement, svg_text)
    
    Path('scratch/out_github.svg').write_text(svg_text)
    os.remove(tmp_path)
    
