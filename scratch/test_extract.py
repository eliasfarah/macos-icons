import re
from pathlib import Path

def test_extract(filepath):
    svg_text = Path(filepath).read_text(encoding='utf-8')
    if 'glass-shadow' in svg_text and 'squircle-clip' in svg_text:
        match = re.search(r'<image href="([^"]+)"', svg_text)
        if match:
            data_uri = match.group(1)
            print(f"{filepath}: Found data URI of length {len(data_uri)}")
            is_flat = 'width="40"' in svg_text
            print(f"  -> is_flat: {is_flat}")
        else:
            print(f"{filepath}: No image href found")

test_extract('apps/scalable/github-desktop.svg')
test_extract('apps/scalable/git.svg')
