"""Imágenes para la web: ampliación con IA, tono, capas de profundidad y WebP.
Uso: python scripts/web_assets.py [nombre ...]
Por cada assets/procesadas/<nombre>.jpg:
  1. Amplía x4 con Real-ESRGAN (scripts/esrgan.onnx, fuera del repo) y guarda assets/hd/<nombre>.jpg (caché).
  2. Refina la máscara del sujeto (de <nombre>_depth.png, canal G) con un filtro guiado sobre la imagen grande.
  3. Exporta a web/img/: <nombre>.webp (foto completa), <nombre>_fg.webp (sujeto con transparencia)
     y <nombre>_bg.webp (fondo sin el sujeto, hueco rellenado). Tono de copia en plata cálida.
"""
import sys, pathlib, urllib.request
import numpy as np, cv2, onnxruntime as ort
from PIL import Image

here = pathlib.Path(__file__).resolve().parent
root = here.parent
proc, hd, out = root / 'assets' / 'procesadas', root / 'assets' / 'hd', root / 'web' / 'img'
hd.mkdir(parents=True, exist_ok=True); out.mkdir(parents=True, exist_ok=True)
model = here / 'esrgan.onnx'
if not model.exists():
    urllib.request.urlretrieve('https://huggingface.co/imgdesignart/realesrgan-x4-onnx/resolve/main/onnx/model.onnx', model)
LAYERS = {'desfile', 'jeep', 'uniforme', 'castillo', 'casapres', 'ydigoras', 'protesta', 'multitud', 'retrato'}
MAXL = {'constitucion': 1600, 'periodico': 1800, 'poster': 1900, 'guyamel': 900, 'retrato': 1200, 'palacio': 1600, 'palacio2': 1600}

def upscale(g):
    sess = ort.InferenceSession(str(model), providers=['CPUExecutionProvider']); name = sess.get_inputs()[0].name
    x = np.stack([g] * 3, -1).astype(np.float32) / 255
    P, T, S = 8, 64, 48
    h, w = g.shape
    H = ((h + S - 1) // S) * S; W = ((w + S - 1) // S) * S
    xp = np.pad(x, ((P, H - h + P), (P, W - w + P), (0, 0)), mode='reflect')
    res = np.zeros((H * 4, W * 4, 3), np.float32)
    for y in range(0, H, S):
        for xx in range(0, W, S):
            t = xp[y:y + T, xx:xx + T].transpose(2, 0, 1)[None]
            o = sess.run(None, {name: t})[0][0].transpose(1, 2, 0)
            res[y * 4:(y + S) * 4, xx * 4:(xx + S) * 4] = o[P * 4:(P + S) * 4, P * 4:(P + S) * 4]
    r = np.clip(res[:h * 4, :w * 4].mean(-1), 0, 1)
    return (r * 255).astype(np.uint8)

def guided(I, p, r, eps):
    m = lambda a: cv2.boxFilter(a, -1, (r, r))
    mI, mp = m(I), m(p); a = (m(I * p) - mI * mp) / (m(I * I) - mI * mI + eps); b = mp - a * mI
    return m(a) * I + m(b)

def tone(g):
    """Copia en gelatina de plata: curva suave y virado cálido muy leve."""
    l = g.astype(np.float32) / 255
    l = np.clip((l - .03) / .95, 0, 1); l = l * l * (3 - 2 * l) * .35 + l * .65
    lo, hi = np.array([13, 12, 11], np.float32), np.array([240, 233, 220], np.float32)
    return (lo + (hi - lo) * l[..., None]).astype(np.uint8)

def pushpull(img, w):
    if min(img.shape[:2]) <= 2:
        s = w.sum(); return np.full_like(img, (img * w[..., None]).sum((0, 1)) / s if s else img.mean((0, 1)))
    sz = (img.shape[1] // 2, img.shape[0] // 2)
    sw = cv2.resize(w, sz, interpolation=cv2.INTER_AREA); si = cv2.resize(img * w[..., None], sz, interpolation=cv2.INTER_AREA)
    f = pushpull(np.where(sw[..., None] > 1e-4, si / np.maximum(sw[..., None], 1e-4), 0), np.clip(sw * 4, 0, 1))
    up = cv2.resize(f, img.shape[1::-1], interpolation=cv2.INTER_LINEAR)
    return img * w[..., None] + up * (1 - w[..., None])

def save(arr, path, q=80, alpha=None):
    im = Image.fromarray(arr)
    if alpha is not None: im = Image.fromarray(np.dstack([arr, alpha]), 'RGBA')
    im.save(path, 'WEBP', quality=q, method=6)

def blur(n):
    """Fondo lejano: versión diminuta, desenfocada y oscura (al ampliarse en pantalla queda difusa sin coste)."""
    im = np.asarray(Image.open(out / f'{n}.webp').convert('RGB')).astype(np.float32)
    s = 240 / max(im.shape[:2]); im = cv2.resize(im, (int(im.shape[1] * s), int(im.shape[0] * s)), interpolation=cv2.INTER_AREA)
    im = cv2.GaussianBlur(im, (0, 0), 5) * .55
    save(np.clip(im, 0, 255).astype(np.uint8), out / f'{n}_blur.webp', 70)

if sys.argv[1:2] == ['--blur']:
    for n in sys.argv[2:]: blur(n)
    sys.exit()

names = sys.argv[1:] or ['desfile', 'jeep', 'periodico', 'uniforme', 'poster', 'castillo', 'constitucion', 'casapres',
                         'ydigoras', 'protesta', 'retrato', 'multitud', 'palacio', 'palacio2', 'guyamel']
for n in names:
    cache = hd / f'{n}.jpg'
    if cache.exists(): big = np.asarray(Image.open(cache).convert('L'))
    else:
        big = upscale(np.asarray(Image.open(proc / f'{n}.jpg').convert('L')))
        Image.fromarray(big).save(cache, quality=92)
    L = MAXL.get(n, 2200); h, w = big.shape; s = min(1, L / max(h, w))
    g = cv2.resize(big, (int(w * s), int(h * s)), interpolation=cv2.INTER_AREA)
    rgb = tone(g); save(rgb, out / f'{n}.webp', 80)
    if n in LAYERS:
        dep = np.asarray(Image.open(proc / f'{n}_depth.png').convert('RGB'))
        m = cv2.resize(dep[..., 1].astype(np.float32) / 255, g.shape[::-1], interpolation=cv2.INTER_CUBIC)
        m = np.clip((m - .35) / .3, 0, 1)
        I = g.astype(np.float32) / 255
        m = np.clip(guided(I, m, max(9, g.shape[0] // 90) | 1, 1e-3), 0, 1)
        m = np.clip((m - .2) / .6, 0, 1); m = cv2.GaussianBlur(m, (0, 0), 1.2)
        save(rgb, out / f'{n}_fg.webp', 78, (m * 255).astype(np.uint8))
        hole = cv2.dilate((m > .05).astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (41, 41))).astype(np.float32)
        hole = cv2.GaussianBlur(hole, (0, 0), 6)
        bs = 1400 / max(g.shape); small = cv2.resize(rgb, (int(g.shape[1] * bs), int(g.shape[0] * bs)), interpolation=cv2.INTER_AREA).astype(np.float32)
        hs = cv2.resize(hole, small.shape[1::-1])
        bg = pushpull(small, 1 - hs)
        bg += np.random.default_rng(3).normal(0, 4, bg.shape[:2])[..., None] * hs[..., None]
        save(np.clip(bg, 0, 255).astype(np.uint8), out / f'{n}_bg.webp', 74)
    blur(n)
    print(n, g.shape[::-1], 'capas' if n in LAYERS else '', flush=True)
