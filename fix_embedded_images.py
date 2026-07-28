import os
import xml.etree.ElementTree as ET
from pathlib import Path

# Fix namespace issues
ET.register_namespace('', 'http://www.w3.org/2000/svg')
ET.register_namespace('xlink', 'http://www.w3.org/1999/xlink')
ns = {'svg': 'http://www.w3.org/2000/svg'}

def process_file(filepath):
    try:
        tree = ET.parse(filepath)
        root = tree.getroot()
        modified = False
        
        # Encontra todas as tags <image> no arquivo
        images = root.findall('.//svg:image', ns)
        for img in images:
            # Pega o atributo href ou xlink:href
            href = img.attrib.get('{http://www.w3.org/1999/xlink}href') or img.attrib.get('href')
            if href and 'data:image/png;base64' in href:
                parent_map = {c: p for p in tree.iter() for c in p}
                parent = parent_map.get(img)
                if parent is not None:
                    parent.remove(img)
                    modified = True
        
        if modified:
            tree.write(filepath)
            print(f"Modificado: {filepath}")
            
    except Exception as e:
        print(f"Erro ao processar {filepath}: {e}")

def main():
    target_dir = Path(__file__).parent.resolve() / "apps/scalable"
    for svg_file in target_dir.glob("*.svg"):
        if svg_file.is_file() and not svg_file.is_symlink():
            process_file(svg_file)

if __name__ == "__main__":
    main()
