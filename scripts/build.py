"""Genera dist/ para GitHub Pages: web/index.html + web/img/*.webp (ver scripts/web_assets.py),
más manifest.webmanifest e icono.png para abrirla a pantalla completa desde la pantalla de inicio.
Uso: python3 scripts/build.py
"""
import json, pathlib, shutil
from PIL import Image, ImageOps
root = pathlib.Path(__file__).resolve().parent.parent
web, dist = root / 'web', root / 'dist'
shutil.rmtree(dist, ignore_errors=True)
shutil.copytree(web, dist)
# las proporciones de las imágenes se incrustan en la página (así no hay que pedirlas aparte)
html = (dist / 'index.html').read_text(encoding='utf-8')
(dist / 'index.html').write_text(html.replace('__SIZES__', (web / 'img' / 'medidas.json').read_text(encoding='utf-8')), encoding='utf-8', newline='\n')
icon = ImageOps.fit(Image.open(root / 'assets' / 'originales' / 'original_desfile.jpeg').convert('RGB'), (512, 512), centering=(.62, .3))
ImageOps.expand(icon.resize((452, 452)), 30, fill=(11, 11, 10)).save(dist / 'icono.png')
(dist / 'manifest.webmanifest').write_text(json.dumps({
    'name': 'Guatemala después de Árbenz (1954–1959)', 'short_name': 'Árbenz 1954',
    'start_url': './', 'display': 'fullscreen', 'orientation': 'any',
    'background_color': '#0b0b0a', 'theme_color': '#0b0b0a',
    'icons': [{'src': 'icono.png', 'sizes': '512x512', 'type': 'image/png'}]}, ensure_ascii=False), encoding='utf-8')
size = sum(f.stat().st_size for f in dist.rglob('*') if f.is_file())
print(f'dist/  {size/1e6:.2f} MB  ({len(list((dist / "img").glob("*.webp")))} imágenes)')
