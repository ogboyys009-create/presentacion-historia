"""Capturas de verificación con Playwright: un PNG por folio, tamaño y navegador.
Uso: python scripts/capturas.py <html> <carpeta_salida> [--sizes 1440x900,390x844] [--browsers chromium,webkit] [--trans 0.3,0.6]
     [--mouse 0.3,-0.2] [--query snap] [--folios 0-11]
Escribe también consola.txt con los errores de consola y de página.
"""
import argparse, pathlib, sys
from playwright.sync_api import sync_playwright

ap = argparse.ArgumentParser()
ap.add_argument('html'); ap.add_argument('out')
ap.add_argument('--sizes', default='1440x900,1180x820,820x1180,390x844')
ap.add_argument('--browsers', default='chromium,webkit')
ap.add_argument('--mouse', default='0.3,-0.2', help='posición del cursor en [-1,1], varias separadas por ;')
ap.add_argument('--query', default='snap')
ap.add_argument('--folios', default='0-11')
ap.add_argument('--wait', type=int, default=1800)
ap.add_argument('--trans', default='', help='capturar transiciones congeladas en estos avances, p. ej. 0.3,0.6')
a = ap.parse_args()

url = pathlib.Path(a.html).resolve().as_uri() + ('?' + a.query if a.query else '')
out = pathlib.Path(a.out); out.mkdir(parents=True, exist_ok=True)
f0, f1 = map(int, a.folios.split('-'))
mice = [tuple(map(float, m.split(','))) for m in a.mouse.split(';')]
log = []
with sync_playwright() as p:
    for bname in a.browsers.split(','):
        br = getattr(p, bname).launch()
        for size in a.sizes.split(','):
            w, h = map(int, size.split('x'))
            touch = w < 1000 or (w, h) == (1180, 820)
            ctx = br.new_context(viewport={'width': w, 'height': h}, device_scale_factor=1,
                                 has_touch=touch, is_mobile=(bname == 'chromium' and w < 500))
            pg = ctx.new_page()
            pg.on('console', lambda m, t=f'{bname} {size}': m.type in ('error', 'warning') and log.append(f'[{t}] {m.type}: {m.text}'))
            pg.on('pageerror', lambda e, t=f'{bname} {size}': log.append(f'[{t}] pageerror: {e}'))
            pg.goto(url, wait_until='load'); pg.wait_for_timeout(2500)
            for i in range(f0, f1 + 1):
                if a.trans:
                    if i == 0: continue
                    for pv in a.trans.split(','):
                        pg.evaluate(f'window.__freeze=null; __go({i-1},true)'); pg.wait_for_timeout(400)
                        pg.evaluate(f'window.__freeze={pv}; __go({i})'); pg.wait_for_timeout(a.wait)
                        pg.screenshot(path=str(out / f'{bname}_{w}x{h}_t{i+1:02d}_{pv}.png'))
                    pg.evaluate('window.__freeze=null'); continue
                pg.evaluate(f'window.__go ? __go({i},true) : scrollTo(0,({i}+.42)*1.3*innerHeight)')
                for j, (mx, my) in enumerate(mice):
                    pg.mouse.move((mx + 1) / 2 * w, (my + 1) / 2 * h)
                    pg.wait_for_timeout(a.wait)
                    suf = f'_m{j}' if len(mice) > 1 else ''
                    pg.screenshot(path=str(out / f'{bname}_{w}x{h}_f{i+1:02d}{suf}.png'))
            ctx.close()
        br.close()
(out / 'consola.txt').write_text('\n'.join(log) or 'sin errores', encoding='utf-8')
print(f'{len(log)} mensajes de consola ->', out / 'consola.txt')
