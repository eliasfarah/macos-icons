import re
import base64
from pathlib import Path

def test_full(filepath):
    svg_text = Path(filepath).read_text(encoding='utf-8')
    match = re.search(r'<image[^>]*href="([^"]+)"', svg_text)
    if match:
        data_uri = match.group(1)
        header, b64 = data_uri.split(',', 1)
        bytes_data = base64.b64decode(b64)
        is_png = 'image/png' in header
        print(f"File {filepath}: extracted length {len(bytes_data)}, is_png: {is_png}")

test_full('apps/scalable/github-desktop.svg')
test_full('apps/scalable/git.svg')
