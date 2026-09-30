"""Genera dist/index.html (un solo archivo) incrustando las imágenes y sus mapas de profundidad.
Uso: python3 scripts/build.py
Cada imagen necesita assets/procesadas/<nombre>.jpg y <nombre>_depth.png (ver scripts/depth.py).
"""
import base64, json, pathlib
from PIL import Image
root = pathlib.Path(__file__).resolve().parent.parent
proc = root / 'assets' / 'procesadas'
assets = {}
for jpg in sorted(proc.glob('*.jpg')):
    k = jpg.stem
    dep = proc / f'{k}_depth.png'
    if not dep.exists():
        print('falta mapa de profundidad:', k); continue
    w, h = Image.open(jpg).size
    assets[k] = {
        'img': 'data:image/jpeg;base64,' + base64.b64encode(jpg.read_bytes()).decode(),
        'depth': 'data:image/png;base64,' + base64.b64encode(dep.read_bytes()).decode(),
        'w': w, 'h': h}
tpl = (root / 'src' / 'template.html').read_text(encoding='utf-8')
out = tpl.replace('__ASSETS__', 'const ASSETS=' + json.dumps(assets) + ';')
(root / 'dist').mkdir(exist_ok=True)
(root / 'dist' / 'index.html').write_text(out, encoding='utf-8', newline='\n')
print(f'dist/index.html  {len(out)/1e6:.2f} MB  ({len(assets)} imágenes)')
