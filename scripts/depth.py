"""Mapas de profundidad con Depth Anything V2 (ONNX, CPU).
Uso: python3 scripts/depth.py assets/originales/foto.jpg nombre
Crea assets/procesadas/nombre.jpg (gris, máx 1400 px, autocontraste) y nombre_depth.png (máx 360 px).
El modelo small (~99 MB) se descarga en scripts/da.onnx la primera vez. Para más calidad, probar base o large.
"""
import sys, pathlib, urllib.request
import numpy as np, onnxruntime as ort
from PIL import Image, ImageFilter, ImageOps
here = pathlib.Path(__file__).resolve().parent
model = here / 'da.onnx'
if not model.exists():
    urllib.request.urlretrieve('https://huggingface.co/onnx-community/depth-anything-v2-small/resolve/main/onnx/model.onnx', model)
src, name = sys.argv[1], sys.argv[2]
out = here.parent / 'assets' / 'procesadas'
im = Image.open(src).convert('RGB')
s = ort.InferenceSession(str(model), providers=['CPUExecutionProvider'])
x = np.asarray(im.resize((518, 518), Image.BICUBIC)).astype(np.float32) / 255
x = ((x - [0.485, 0.456, 0.406]) / [0.229, 0.224, 0.225]).transpose(2, 0, 1)[None].astype(np.float32)
d = s.run(None, {s.get_inputs()[0].name: x})[0].squeeze()
d = (d - d.min()) / (d.max() - d.min() + 1e-6)
dm = Image.fromarray((d * 255).astype(np.uint8)).resize(im.size, Image.BICUBIC).filter(ImageFilter.GaussianBlur(3))
g = ImageOps.autocontrast(im.convert('L'), cutoff=1); g.thumbnail((1400, 1400), Image.LANCZOS)
g.save(out / f'{name}.jpg', quality=80, optimize=True)
dm.thumbnail((360, 360), Image.LANCZOS); dm.save(out / f'{name}_depth.png', optimize=True)
print('ok', name, g.size)
