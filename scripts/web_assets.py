"""Imágenes para la web. Nada se amplía ni se inventa: resolución nativa.
Uso: python scripts/web_assets.py
- Bordes: quita marcos uniformes (capturas con bordes grises o blancos) y las líneas finas que dejan los escaneos
  en el canto; después recorta un margen mínimo de seguridad para que ningún borde quede sucio.
- Fotos: blanco y negro con un virado cálido muy leve. Documentos: color de papel natural, algo desaturado.
- Profundidad (_d): mapa de Depth Anything V2 (scripts/da_base.onnx) suavizado, para el relieve sutil de las fotos.
- Prensa Libre: recorte de prensa bajo el titular (la marca de agua de la hemeroteca queda fuera).
- multitud (último folio): capa del sujeto y fondo rellenado para el paralaje, más fondo desenfocado.
- p_*: copias para el muro de archivo de la portada (imágenes que no salen en las diapositivas).
Salida: web/img/*.webp y web/img/medidas.json
"""
import json, pathlib, hashlib
import numpy as np, cv2
from PIL import Image, ImageOps, ImageFilter

root = pathlib.Path(__file__).resolve().parent.parent
O, X, P = root / 'assets' / 'originales', root / 'assets' / 'externas', root / 'assets' / 'procesadas'
V2 = O / 'v2'
cache = root / 'assets' / 'hd'; cache.mkdir(parents=True, exist_ok=True)
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
    return im.crop((l, t, r, b))

def edges(im, maxf=.045, jump=20, extra=.009):
    """Líneas y bandas en el canto (filo del papel, sombra del escáner): se corta tras el último salto brusco
    cerca del borde y luego un margen fijo pequeño."""
    a = np.asarray(im.convert('L')).astype(np.float32); h, w = a.shape
    def cut(prof):
        n = len(prof); lim = max(3, int(n * maxf)); c = 0
        for i in range(lim):
            if abs(prof[i] - prof[min(n - 1, i + 3)]) > jump: c = i + 3
        return c
    rows, cols = a[:, int(w * .1):int(w * .9)].mean(1), a[int(h * .1):int(h * .9), :].mean(0)
    t, b = cut(rows), cut(rows[::-1]); l, r = cut(cols), cut(cols[::-1])
    ex, ey = round(w * extra), round(h * extra)
    return im.crop((l + ex, t + ey, w - r - ex, h - b - ey))

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

# ---------- profundidad ----------
_sess = None
def depth_map(rgb, name):
    """Profundidad inversa 0..1 (1 = cerca), suavizada y ensanchada hacia delante para que el relieve no rasgue."""
    key = hashlib.md5(rgb.tobytes()).hexdigest()[:12]; cf = cache / f'{name}_{key}.npy'
    if cf.exists(): d = np.load(cf)
    else:
        global _sess
        if _sess is None:
            import onnxruntime as ort
            _sess = ort.InferenceSession(str(root / 'scripts' / 'da_base.onnx'), providers=['CPUExecutionProvider'])
        g = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY); h, w = g.shape; d = np.zeros((h, w), np.float32)
        for long in (518, 770):
            s = long / max(h, w); H = max(14, round(h * s / 14) * 14); W = max(14, round(w * s / 14) * 14)
            x = cv2.resize(np.stack([g] * 3, -1), (W, H), interpolation=cv2.INTER_AREA).astype(np.float32) / 255
            x = ((x - [0.485, 0.456, 0.406]) / [0.229, 0.224, 0.225]).transpose(2, 0, 1)[None].astype(np.float32)
            r = _sess.run(None, {_sess.get_inputs()[0].name: x})[0].squeeze()
            r = (r - np.percentile(r, 2)) / (np.percentile(r, 99) - np.percentile(r, 2) + 1e-6)
            d += cv2.resize(np.clip(r, 0, 1).astype(np.float32), (w, h), interpolation=cv2.INTER_CUBIC)
        d /= 2; np.save(cf, d)
    h, w = d.shape; s = 512 / max(h, w); size = (max(8, round(w * s)), max(8, round(h * s)))
    d = cv2.resize(d, size, interpolation=cv2.INTER_AREA)
    d = cv2.bilateralFilter(d.astype(np.float32), 9, .1, 6)
    k = max(3, round(min(size) * .018)) | 1
    d = cv2.dilate(d, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k)))   # el primer plano se ensancha un poco
    d = cv2.GaussianBlur(d, (0, 0), min(size) * .012)
    d = (d - d.min()) / (d.max() - d.min() + 1e-6)
    Image.fromarray((d * 255).astype(np.uint8)).save(out / f'{name}_d.webp', 'WEBP', quality=90, method=6)

sizes = {}
def photo(name, src, crop=None, q=88, depth=True, blur=0, maxside=None):
    im = Image.open(src).convert('RGB')
    if crop: im = im.crop(crop)
    im = edges(trim(im))
    if blur: im = im.filter(ImageFilter.GaussianBlur(blur))   # destramado leve de fotos impresas en semitono
    if maxside and max(im.size) > maxside: im.thumbnail((maxside, maxside), Image.LANCZOS)
    arr = mono(im); sizes[name] = save(arr, name, q)
    if depth: depth_map(arr, name)
    return im

def doc(name, src, crop=None, sat=.55, q=92, clean=True):
    im = Image.open(src).convert('RGB')
    if crop: im = im.crop(crop)
    im = trim(im)
    if clean: im = edges(im, extra=.004)
    sizes[name] = save(paper(im, sat), name, q); return im

# --- fotografías de las diapositivas (con relieve) ---
photo('jeep', O / 'original_IMG_3326.webp')
photo('castillo', X / 'castillo_oficial.jpg', blur=.6, maxside=1700)
photo('posesion', X / 'arbenz_posesion.jpg')        # Arévalo saluda a Árbenz en su toma de posesión, 1951
photo('discurso', X / 'castillo_discurso.png')      # fotograma de noticiero (Archivos Nacionales de EE. UU.)
photo('ydigoras', X / 'ydigoras_oficial.png')
photo('protesta', O / 'original_IMG_3332.png')
photo('palacio', V2 / '3.jpg')
photo('casapres', V2 / '5.jpg')
photo('eisenhower', X / 'eisenhower_dulles.jpg')
photo('exilio', X / 'arbenz_exilio_1955.jpg', maxside=1600)
photo('retrato', O / 'original_retrato.jpeg', depth=False)

# --- documentos ---
doc('poster', O / 'original_poster.jpeg', sat=.4)
doc('constitucion', V2 / '2.jpg', sat=.5)
doc('guyamel', O / 'original_IMG_3327.jpeg', sat=.4, clean=False)   # el filete decorativo es parte del anuncio
doc('memo1', X / 'cia_foia_1.gif', sat=0, clean=False)
doc('memo5', X / 'cia_foia_5.gif', sat=0, clean=False)
# «Gloriosa victoria» (Diego Rivera, 1954): reproducción a color, apenas apagada
gv = edges(trim(Image.open(X / 'gloriosa_victoria.jpg').convert('RGB')), extra=.004)
ga = paper(gv, .78); sizes['gloriosa'] = save(ga, 'gloriosa', 88); depth_map(ga, 'gloriosa')
# Prensa Libre: solo el periódico (sin los márgenes blancos) y hasta el titular principal
pl = Image.open(O / 'original_periodico.jpeg').convert('RGB')
sizes['prensa'] = save(paper(pl.crop((136, 4, 487, 166)), .6), 'prensa', 93)
# sello postal «Liberación 1954-55»: se recorta al sello y el fondo se hace transparente
st = Image.open(X / 'liberacion_1954.jpg').convert('RGB'); st = trim(st, tol=10)
a = np.asarray(st).astype(np.float32); bgc = np.median(np.concatenate([a[:6].reshape(-1, 3), a[-6:].reshape(-1, 3), a[:, :6].reshape(-1, 3), a[:, -6:].reshape(-1, 3)]), 0)
d = np.sqrt(((a - bgc) ** 2).sum(-1)); m = np.clip((d - 18) / 22, 0, 1)
m = cv2.morphologyEx((m * 255).astype(np.uint8), cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
st.thumbnail((700, 700), Image.LANCZOS); m = cv2.resize(m, st.size, interpolation=cv2.INTER_AREA)
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

# --- portada: muro de archivo con fotografías de la época que no salen en las diapositivas ---
WALL = [('p_junta', X / 'junta_1944.jpg'), ('p_arevalo', X / 'arevalo_pres.jpg'), ('p_arana', X / 'arana.jpg'), ('p_1944', X / 'arbenz_1944.jpg'),
        ('p_1945', X / 'arbenz_1945b.jpg'), ('p_uniforme', O / 'original_uniforme.jpeg'), ('p_militar', X / 'arbenz_uniforme_militar.jpg'),
        ('p_retrato', X / 'arbenz_retrato_pres.png'), ('p_portrait', X / 'arbenz_portrait.jpg'), ('p_sonrie', O / 'original_sonrie.jpeg'),
        ('p_banda', X / 'arbenz_1950.jpg'), ('p_ministros', X / 'posesion_ministros.jpg'), ('p_desfile', O / 'original_desfile.jpeg'),
        ('p_plana', X / 'plana_mayor.jpg'), ('p_reforma', X / 'reforma_1952.jpg'), ('p_estadio', X / 'estadio_revolucion.jpg'),
        ('p_vapor', X / 'ufco3.jpg'), ('p_ufco', X / 'ufco1.jpg'), ('p_palacio2', V2 / '10.jpg'), ('p_ydigoras50', X / 'ydigoras_1950.jpg'),
        ('p_arevalo2', X / 'arevalo_large.jpg'), ('p_cia2', X / 'cia_foia_2.gif'), ('p_cia3', X / 'cia_foia_3.gif'), ('p_cia4', X / 'cia_foia_4.gif')]
for name, src in WALL:
    im = Image.open(src).convert('RGB'); im = trim(im)
    isdoc = 'cia' in name
    if not isdoc: im = edges(im)
    im.thumbnail((640, 420), Image.LANCZOS)
    sizes[name] = save(paper(im, 0) if isdoc else mono(im, .5), name, 82)

(out / 'medidas.json').write_text(json.dumps(sizes))
for k, v in sizes.items(): print(f'{k:12s} {v}')
