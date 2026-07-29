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
    Path('scratch/extracted_github' + ext).write_bytes(bytes_data)
