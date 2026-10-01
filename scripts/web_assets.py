"""Imágenes para la web (versión definitiva). Nada se amplía ni se inventa: resolución nativa.
Uso: python scripts/web_assets.py
- Recorta cualquier marco uniforme (capturas con bordes grises o blancos).
- Fotos: blanco y negro con un virado cálido muy leve. Documentos: color de papel natural, algo desaturado.
- Prensa Libre: recorte de prensa bajo el titular (la marca de agua de la hemeroteca queda fuera).
- multitud (último folio): capa del sujeto y fondo rellenado para el paralaje, más fondo desenfocado.
- _t: miniaturas para la tira de película del título.
Salida: web/img/*.webp y web/img/medidas.json
"""
import json, pathlib
import numpy as np, cv2
from PIL import Image, ImageOps

root = pathlib.Path(__file__).resolve().parent.parent
O, X, P = root / 'assets' / 'originales', root / 'assets' / 'externas', root / 'assets' / 'procesadas'
out = root / 'web' / 'img'; out.mkdir(parents=True, exist_ok=True)
for f in out.glob('*'): f.unlink()

def trim(im, tol=7, maxf=.12):
    """Quita bordes uniformes (marcos de captura) por cada lado."""
    a = np.asarray(im.convert('L')).astype(np.float32); h, w = a.shape
    def uniform(line): return line.std() < tol
    t, b, l, r = 0, h, 0, w
    while t < h * maxf and uniform(a[t, l:r]): t += 1
    while b > h * (1 - maxf) and uniform(a[b - 1, l:r]): b -= 1
    while l < w * maxf and uniform(a[t:b, l]): l += 1
    while r > w * (1 - maxf) and uniform(a[t:b, r - 1]): r -= 1
    if (t, b, l, r) != (0, h, 0, w): t, b, l, r = t + 2, b - 2, l + 2, r - 2
    return im.crop((l, t, r, b))

def mono(im, cutoff=.3):
    g = ImageOps.autocontrast(im.convert('L'), cutoff=cutoff)
    l = np.asarray(g).astype(np.float32) / 255
    return (np.clip(np.stack([l, l * .978 + .004, l * .94 + .01], -1), 0, 1) * 255).astype(np.uint8)

def paper(im, sat=.55):
    a = np.asarray(im.convert('RGB')).astype(np.float32)
    g = a.mean(-1, keepdims=True); return np.clip(g + (a - g) * sat, 0, 255).astype(np.uint8)

def save(arr, name, q=92, alpha=None):
    im = Image.fromarray(arr) if alpha is None else Image.fromarray(np.dstack([arr, alpha]), 'RGBA')
    im.save(out / f'{name}.webp', 'WEBP', quality=q, method=6); return im.size

sizes = {}
def photo(name, src, crop=None, q=92):
    im = Image.open(src).convert('RGB')
    if crop: im = im.crop(crop)
    im = trim(im); sizes[name] = save(mono(im), name, q); return im

def doc(name, src, crop=None, sat=.55, q=92):
    im = Image.open(src).convert('RGB')
    if crop: im = im.crop(crop)
    im = trim(im); sizes[name] = save(paper(im, sat), name, q); return im

# --- fotografías ---
photo('desfile', O / 'original_desfile.jpeg')
photo('jeep', O / 'original_IMG_3326.webp')
photo('uniforme', O / 'original_uniforme.jpeg')
photo('castillo', X / 'castillo_oficial.jpg')
photo('ydigoras', X / 'ydigoras_oficial.png')
photo('protesta', O / 'original_IMG_3332.png')
photo('palacio', root / 'assets' / 'originales' / 'v2' / '3.jpg')
photo('casapres', root / 'assets' / 'originales' / 'v2' / '5.jpg')
photo('eisenhower', X / 'eisenhower_dulles.jpg')
photo('exilio', X / 'arbenz_exilio_1955.jpg')
photo('retrato', O / 'original_retrato.jpeg')
photo('posesion', X / 'arbenz_posesion.jpg')

# --- documentos ---
doc('poster', O / 'original_poster.jpeg', sat=.4)
doc('constitucion', O / 'original_IMG_3331.jpeg', sat=.5)
doc('guyamel', O / 'original_IMG_3327.jpeg', sat=.4)
doc('memo1', X / 'cia_foia_1.gif', sat=0)
doc('memo5', X / 'cia_foia_5.gif', sat=0)
# Prensa Libre: solo el periódico (sin los márgenes blancos) y hasta el titular principal
pl = Image.open(O / 'original_periodico.jpeg').convert('RGB')
sizes['prensa'] = save(paper(pl.crop((136, 4, 487, 166)), .6), 'prensa', 93)
# sello postal «Liberación 1954-55»: se recorta al sello y el fondo se hace transparente
st = Image.open(X / 'liberacion_1954.jpg').convert('RGB'); st = trim(st, tol=10)
a = np.asarray(st).astype(np.float32); bgc = np.median(np.concatenate([a[:6].reshape(-1, 3), a[-6:].reshape(-1, 3), a[:, :6].reshape(-1, 3), a[:, -6:].reshape(-1, 3)]), 0)
d = np.sqrt(((a - bgc) ** 2).sum(-1)); m = np.clip((d - 18) / 22, 0, 1)
m = cv2.morphologyEx((m * 255).astype(np.uint8), cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
sizes['sello'] = save(np.asarray(st), 'sello', 92, m)

# --- último folio: capas para el paralaje ---
mt = Image.open(O / 'original_IMG_3333.jpeg').convert('RGB'); rgb = mono(mt); sizes['multitud'] = save(rgb, 'multitud', 90)
dep = np.asarray(Image.open(P / 'multitud_depth.png').convert('RGB'))
msk = cv2.resize(dep[..., 1].astype(np.float32) / 255, mt.size, interpolation=cv2.INTER_CUBIC)
msk = cv2.GaussianBlur(np.clip((msk - .35) / .3, 0, 1), (0, 0), 1.2)
save(rgb, 'multitud_fg', 88, (msk * 255).astype(np.uint8))
hole = cv2.GaussianBlur(cv2.dilate((msk > .05).astype(np.uint8), np.ones((31, 31), np.uint8)).astype(np.float32), (0, 0), 6)
bg = cv2.inpaint(rgb, (hole > .5).astype(np.uint8) * 255, 9, cv2.INPAINT_TELEA).astype(np.float32)
bg = cv2.GaussianBlur(bg, (0, 0), 3) * hole[..., None] + rgb * (1 - hole[..., None])
save(np.clip(bg, 0, 255).astype(np.uint8), 'multitud_bg', 85)
small = cv2.resize(rgb.astype(np.float32), (240, 161), interpolation=cv2.INTER_AREA)
save(np.clip(cv2.GaussianBlur(small, (0, 0), 5) * .5, 0, 255).astype(np.uint8), 'multitud_blur', 70)

# --- miniaturas para la tira de película ---
for n in ['posesion', 'desfile', 'jeep', 'eisenhower', 'uniforme', 'castillo', 'poster', 'constitucion', 'casapres', 'ydigoras', 'protesta', 'multitud', 'exilio', 'palacio']:
    im = Image.open(out / f'{n}.webp').convert('RGB'); im = ImageOps.fit(im, (400, 300), centering=(.5, .35))
    im.save(out / f'{n}_t.webp', 'WEBP', quality=82, method=6)

(out / 'medidas.json').write_text(json.dumps(sizes))
for k, v in sizes.items(): print(f'{k:12s} {v}')
