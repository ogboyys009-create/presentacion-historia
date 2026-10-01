"""Imágenes para la web, sin IA generativa: se parte de los archivos originales de los alumnos.
Uso: python scripts/web_assets.py
- Escala de grises con contraste preservado y un virado de plata muy leve.
- Ampliación clásica (Lanczos, como máximo x1,6) y enfoque suave; nada inventa detalle.
- Documentos recortados a su borde real (sin márgenes blancos).
- Retratos y fotos de escena: capa del sujeto (_fg, con transparencia) y fondo con el hueco rellenado (_bg),
  a partir de la máscara de assets/procesadas/<nombre>_depth.png (canal G, ver scripts/capas.py).
- _blur: versión diminuta y oscura para el fondo lejano.
Salida: web/img/*.webp
"""
import pathlib
import numpy as np, cv2
from PIL import Image, ImageOps, ImageFilter

root = pathlib.Path(__file__).resolve().parent.parent
orig, proc, out = root / 'assets' / 'originales', root / 'assets' / 'procesadas', root / 'web' / 'img'
out.mkdir(parents=True, exist_ok=True)
for f in out.glob('*.webp'): f.unlink()

# nombre -> archivo original con el mismo encuadre (si no hay, se usa assets/procesadas)
SRC = {'castillo': 'original_IMG_3324.jpeg', 'ydigoras': 'original_IMG_3325.png', 'jeep': 'original_IMG_3326.webp',
       'guyamel': 'original_IMG_3327.jpeg', 'constitucion': 'original_IMG_3331.jpeg', 'protesta': 'original_IMG_3332.png',
       'multitud': 'original_IMG_3333.jpeg', 'desfile': 'original_desfile.jpeg', 'periodico': 'original_periodico.jpeg',
       'poster': 'original_poster.jpeg', 'retrato': 'original_retrato.jpeg', 'uniforme': 'original_uniforme.jpeg',
       'palacio2': 'original_IMG_3329.jpeg'}
LAYERS = ['desfile', 'jeep', 'uniforme', 'castillo', 'casapres', 'ydigoras', 'protesta', 'multitud']
DOCS = ['periodico', 'poster', 'constitucion', 'guyamel']
ALL = LAYERS + DOCS + ['retrato', 'palacio', 'palacio2']
BLUR = LAYERS + ['palacio', 'palacio2', 'poster', 'periodico', 'constitucion']

def load(n):
    p = orig / SRC[n] if n in SRC else proc / f'{n}.jpg'
    im = Image.open(p).convert('RGB').convert('L')
    return ImageOps.autocontrast(im, cutoff=.4)

def crop_doc(im):
    a = np.asarray(im); dark = a < 200
    rows = np.where(dark.mean(1) > .02)[0]; cols = np.where(dark.mean(0) > .02)[0]
    if len(rows) and len(cols):
        pad = 2; im = im.crop((max(0, cols[0] - pad), max(0, rows[0] - pad), min(a.shape[1], cols[-1] + pad), min(a.shape[0], rows[-1] + pad)))
    return im

def enlarge(im, cap=2000):
    k = min(1.6, cap / max(im.size))
    if k > 1: im = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
    return im.filter(ImageFilter.UnsharpMask(radius=1.4, percent=55, threshold=2))

def tint(g):
    """Plata muy levemente cálida; no toca el contraste."""
    l = np.asarray(g).astype(np.float32) / 255
    rgb = np.stack([l * 1.0, l * .975 + .004, l * .93 + .012], -1)
    return (np.clip(rgb, 0, 1) * 255).astype(np.uint8)

def webp(arr, name, q=90, alpha=None):
    im = Image.fromarray(arr) if alpha is None else Image.fromarray(np.dstack([arr, alpha]), 'RGBA')
    im.save(out / f'{name}.webp', 'WEBP', quality=q, method=6)

def guided(I, p, r, eps):
    m = lambda a: cv2.boxFilter(a, -1, (r, r))
    mI, mp = m(I), m(p); a = (m(I * p) - mI * mp) / (m(I * I) - mI * mI + eps); b = mp - a * mI
    return m(a) * I + m(b)

def pushpull(img, w):
    if min(img.shape[:2]) <= 2:
        s = w.sum(); return np.full_like(img, (img * w[..., None]).sum((0, 1)) / s if s else img.mean((0, 1)))
    sz = (img.shape[1] // 2, img.shape[0] // 2)
    sw = cv2.resize(w, sz, interpolation=cv2.INTER_AREA); si = cv2.resize(img * w[..., None], sz, interpolation=cv2.INTER_AREA)
    f = pushpull(np.where(sw[..., None] > 1e-4, si / np.maximum(sw[..., None], 1e-4), 0), np.clip(sw * 4, 0, 1))
    return img * w[..., None] + cv2.resize(f, img.shape[1::-1], interpolation=cv2.INTER_LINEAR) * (1 - w[..., None])

info = {}
for n in ALL:
    g = load(n)
    if n in DOCS: g = crop_doc(g)
    g = enlarge(g, 1400 if n == 'guyamel' else 2000)
    rgb = tint(g); webp(rgb, n, 90)
    info[n] = g.size
    if n in LAYERS:
        dep = np.asarray(Image.open(proc / f'{n}_depth.png').convert('RGB'))
        # la máscara se hizo sobre la versión procesada; si el original tiene otro tamaño, se reescala al cuadro
        m = cv2.resize(dep[..., 1].astype(np.float32) / 255, g.size, interpolation=cv2.INTER_CUBIC)
        m = np.clip((m - .35) / .3, 0, 1)
        I = np.asarray(g).astype(np.float32) / 255
        m = np.clip(guided(I, m, max(9, g.size[1] // 90) | 1, 1e-3), 0, 1)
        m = cv2.GaussianBlur(np.clip((m - .2) / .6, 0, 1), (0, 0), 1.1)
        webp(rgb, f'{n}_fg', 88, (m * 255).astype(np.uint8))
        hole = cv2.dilate((m > .05).astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (41, 41))).astype(np.float32)
        hole = cv2.GaussianBlur(hole, (0, 0), 6)
        bg = pushpull(rgb.astype(np.float32), 1 - hole)
        bg += np.random.default_rng(3).normal(0, 4, bg.shape[:2])[..., None] * hole[..., None]
        webp(np.clip(bg, 0, 255).astype(np.uint8), f'{n}_bg', 84)
    if n in BLUR:
        s = 240 / max(g.size); small = cv2.resize(rgb.astype(np.float32), (int(g.size[0] * s), int(g.size[1] * s)), interpolation=cv2.INTER_AREA)
        webp(np.clip(cv2.GaussianBlur(small, (0, 0), 5) * .5, 0, 255).astype(np.uint8), f'{n}_blur', 70)
    print(n, g.size, flush=True)
import json
(out / 'medidas.json').write_text(json.dumps(info))
