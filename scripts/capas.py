"""Profundidad de calidad y separación en capas para cada imagen procesada.
Uso: python scripts/capas.py [nombre ...]      (sin nombres: todas)
Por cada assets/procesadas/<nombre>.jpg genera:
  <nombre>_depth.png  R = profundidad (Depth Anything V2 base), G = máscara del sujeto (suave)
  <nombre>_bg.jpg     fondo sin el sujeto, con el hueco rellenado (inpainting)
El modelo se descarga en scripts/da_base.onnx (~390 MB) la primera vez; no va al repo.
"""
import sys, pathlib, urllib.request
import numpy as np, onnxruntime as ort, cv2
from PIL import Image

here = pathlib.Path(__file__).resolve().parent
proc = here.parent / 'assets' / 'procesadas'
model = here / 'da_base.onnx'
if not model.exists():
    urllib.request.urlretrieve('https://huggingface.co/onnx-community/depth-anything-v2-base/resolve/main/onnx/model.onnx', model)
sess = ort.InferenceSession(str(model), providers=['CPUExecutionProvider'])
inp = sess.get_inputs()[0].name

def depth(g):
    """Profundidad inversa normalizada 0..1 (1 = cerca), con prueba en dos escalas para más detalle."""
    h, w = g.shape; out = np.zeros((h, w), np.float32)
    for long in (518, 770):
        s = long / max(h, w); H = max(14, round(h * s / 14) * 14); W = max(14, round(w * s / 14) * 14)
        x = cv2.resize(np.stack([g] * 3, -1), (W, H), interpolation=cv2.INTER_CUBIC).astype(np.float32) / 255
        x = ((x - [0.485, 0.456, 0.406]) / [0.229, 0.224, 0.225]).transpose(2, 0, 1)[None].astype(np.float32)
        d = sess.run(None, {inp: x})[0].squeeze()
        d = (d - np.percentile(d, 1)) / (np.percentile(d, 99.5) - np.percentile(d, 1) + 1e-6)
        out += cv2.resize(np.clip(d, 0, 1).astype(np.float32), (w, h), interpolation=cv2.INTER_CUBIC)
    return np.clip(out / 2, 0, 1)

def subject_mask(d):
    d8 = (d * 255).astype(np.uint8)
    t, _ = cv2.threshold(cv2.GaussianBlur(d8, (0, 0), 3), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    m = (d8 > t).astype(np.uint8)
    k = max(3, int(min(d.shape) * .012)) | 1
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k)))
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k * 2 + 1, k * 2 + 1)))
    n, lab, st, _ = cv2.connectedComponentsWithStats(m)
    keep = np.zeros_like(m)
    for i in range(1, n):  # descarta manchas pequeñas
        if st[i, cv2.CC_STAT_AREA] > m.size * .01: keep[lab == i] = 1
    return keep

def pushpull(img, w):
    """Rellena donde w=0 con el promedio suave de lo que rodea (pirámide), sin rayas."""
    if min(img.shape) <= 2:
        s = w.sum(); return np.full_like(img, (img * w).sum() / s if s else img.mean())
    small_w = cv2.resize(w, (img.shape[1] // 2, img.shape[0] // 2), interpolation=cv2.INTER_AREA)
    small_i = cv2.resize(img * w, (img.shape[1] // 2, img.shape[0] // 2), interpolation=cv2.INTER_AREA)
    filled = pushpull(np.where(small_w > 1e-4, small_i / np.maximum(small_w, 1e-4), 0), np.clip(small_w * 4, 0, 1))
    up = cv2.resize(filled, img.shape[::-1], interpolation=cv2.INTER_LINEAR)
    return img * w + up * (1 - w)

names = sys.argv[1:] or sorted(p.stem for p in proc.glob('*.jpg') if not p.stem.endswith('_bg'))
for name in names:
    g = np.asarray(Image.open(proc / f'{name}.jpg').convert('L'))
    h, w = g.shape
    d = depth(g)
    # la profundidad sigue los bordes de la foto (filtro guiado casero con bilateral conjunto aproximado)
    d = cv2.bilateralFilter(d.astype(np.float32), 9, .08, 5)
    m = subject_mask(d)
    soft = cv2.GaussianBlur(m.astype(np.float32), (0, 0), max(1.5, min(h, w) * .004))
    # fondo: se tapa el sujeto (máscara dilatada) y se rellena
    k = max(5, int(min(h, w) * .03)) | 1
    hole = cv2.dilate(m, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k)))
    sc = 700 / max(h, w) if max(h, w) > 700 else 1
    gs = cv2.resize(g, (int(w * sc), int(h * sc)), interpolation=cv2.INTER_AREA)
    hs = cv2.resize(hole, gs.shape[::-1], interpolation=cv2.INTER_NEAREST)
    bg = pushpull(gs.astype(np.float32), 1 - hs.astype(np.float32))
    # textura: grano del original para que el relleno no se vea liso
    noise = (np.random.default_rng(1).normal(0, 5, bg.shape)).astype(np.float32)
    bg = np.clip(bg.astype(np.float32) + noise * cv2.GaussianBlur(hs.astype(np.float32), (0, 0), 3), 0, 255).astype(np.uint8)
    Image.fromarray(bg).save(proc / f'{name}_bg.jpg', quality=72, optimize=True)
    ds = 512 / max(h, w) if max(h, w) > 512 else 1
    size = (max(1, int(w * ds)), max(1, int(h * ds)))
    R = cv2.resize((d * 255).astype(np.uint8), size, interpolation=cv2.INTER_AREA)
    G = cv2.resize((soft * 255).astype(np.uint8), size, interpolation=cv2.INTER_AREA)
    Image.fromarray(np.stack([R, G, np.zeros_like(R)], -1)).save(proc / f'{name}_depth.png', optimize=True)
    print(f'{name:14s} sujeto {m.mean()*100:4.1f} %  fondo {bg.shape[1]}x{bg.shape[0]}')
