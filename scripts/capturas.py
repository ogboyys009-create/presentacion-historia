"""Capturas de verificación con Playwright. Uso: python scripts/capturas.py <html|url> <salida> 1440x900[,390x844] chromium|webkit [rest|trans|both]"""
import sys, pathlib
from playwright.sync_api import sync_playwright
src, out, sizes, bn = sys.argv[1:5]; mode = sys.argv[5] if len(sys.argv) > 5 else 'both'
url = src if src.startswith('http') else pathlib.Path(src).resolve().as_uri()
out = pathlib.Path(out); out.mkdir(parents=True, exist_ok=True); errs = []
with sync_playwright() as p:
    b = getattr(p, bn).launch(args=['--use-angle=d3d11', '--enable-gpu', '--ignore-gpu-blocklist'] if bn == 'chromium' else [])
    for sz in sizes.split(','):
        w, h = map(int, sz.split('x'))
        pg = b.new_page(viewport={'width': w, 'height': h}, has_touch=w < 1000, is_mobile=(bn == 'chromium' and w < 500))
        pg.on('pageerror', lambda e: errs.append(f'{sz} pageerror {e}'))
        pg.on('console', lambda m: m.type == 'error' and errs.append(f'{sz} {m.text[:200]}'))
        pg.goto(url); pg.wait_for_selector('#loader.done', state='attached', timeout=30000); pg.wait_for_timeout(3200)
        pg.mouse.move(w * .7, h * .35)
        for i in range(12):
            if mode in ('rest', 'both'):
                pg.evaluate(f'__go({i})'); pg.wait_for_timeout(1400); pg.screenshot(path=str(out / f'{bn}_{w}x{h}_{i+1:02d}.png'))
            if mode in ('trans', 'both') and i < 11:
                for f in (.78, .9, .97):
                    pg.evaluate(f'__go({i}+{f}-.34)'); pg.wait_for_timeout(700); pg.screenshot(path=str(out / f'{bn}_{w}x{h}_{i+1:02d}t{int(f*100)}.png'))
        pg.close()
    b.close()
print('errores:', errs or 'ninguno')
