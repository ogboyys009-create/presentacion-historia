"""Genera dist/index.html (un solo archivo) incrustando imágenes, mapas de profundidad, fondos y el escritorio 3D.
Uso: python3 scripts/build.py
Cada imagen necesita assets/procesadas/<nombre>.jpg y <nombre>_depth.png (ver scripts/capas.py);
<nombre>_bg.jpg (fondo rellenado) es opcional. El escritorio sale de scripts/escritorio.py (Blender).
También escribe manifest.webmanifest e icono.png para abrirla a pantalla completa desde la pantalla de inicio.
"""
import base64, json, pathlib
from PIL import Image, ImageOps
root = pathlib.Path(__file__).resolve().parent.parent
proc = root / 'assets' / 'procesadas'
dist = root / 'dist'; dist.mkdir(exist_ok=True)
b64 = lambda p: base64.b64encode(p.read_bytes()).decode()
assets = {}
for jpg in sorted(proc.glob('*.jpg')):
    k = jpg.stem
    if k.endswith('_bg'): continue
    dep = proc / f'{k}_depth.png'
    if not dep.exists():
        print('falta mapa de profundidad:', k); continue
    w, h = Image.open(jpg).size
    assets[k] = {'img': 'data:image/jpeg;base64,' + b64(jpg), 'depth': 'data:image/png;base64,' + b64(dep), 'w': w, 'h': h}
    bg = proc / f'{k}_bg.jpg'
    if bg.exists(): assets[k]['bg'] = 'data:image/jpeg;base64,' + b64(bg)
glb = root / 'assets' / 'escritorio.glb'
desk = b64(glb) if glb.exists() else ''
tpl = (root / 'src' / 'template.html').read_text(encoding='utf-8')
out = tpl.replace('__ASSETS__', 'const ASSETS=' + json.dumps(assets) + ';const DESK="' + desk + '";')
(dist / 'index.html').write_text(out, encoding='utf-8', newline='\n')

icon = ImageOps.fit(Image.open(proc / 'desfile.jpg').convert('RGB'), (512, 512), centering=(.62, .3))
ImageOps.expand(ImageOps.expand(icon.resize((440, 440)), 6, fill=(165, 139, 87)), 30, fill=(16, 21, 28)).resize((512, 512)).save(dist / 'icono.png')
(dist / 'manifest.webmanifest').write_text(json.dumps({
    'name': 'Guatemala después de Árbenz (1954–1959)', 'short_name': 'Árbenz 1954',
    'start_url': './', 'display': 'fullscreen', 'orientation': 'any',
    'background_color': '#07090C', 'theme_color': '#07090C',
    'icons': [{'src': 'icono.png', 'sizes': '512x512', 'type': 'image/png'}]}, ensure_ascii=False), encoding='utf-8')
print(f'dist/index.html  {len(out)/1e6:.2f} MB  ({len(assets)} imágenes, escritorio {len(desk)*3//4//1024} KB)')
