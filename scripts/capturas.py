"""Capturas de verificación (sirve dist/ por HTTP para que WebGL lea las imágenes como en GitHub Pages).
Uso: python cap11.py <carpeta dist|url> <salida> 1440x900[,390x844] chromium|webkit [escenas: all | 3,4,5] [extra: burn,fin]"""
import sys, pathlib, threading, functools, http.server, socketserver
from playwright.sync_api import sync_playwright
src, out, sizes, bn = sys.argv[1:5]
which = sys.argv[5] if len(sys.argv) > 5 else 'all'
extra = sys.argv[6].split(',') if len(sys.argv) > 6 else []
out = pathlib.Path(out); out.mkdir(parents=True, exist_ok=True); errs = []
if src.startswith('http'): url = src
else:
    class Q(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a): pass
    H = functools.partial(Q, directory=str(pathlib.Path(src).resolve()))
    srv = socketserver.ThreadingTCPServer(('127.0.0.1', 0), H); srv.daemon_threads = True
    threading.Thread(target=srv.serve_forever, daemon=True).start(); url = f'http://127.0.0.1:{srv.server_address[1]}/'
with sync_playwright() as p:
    b = getattr(p, bn).launch(args=['--use-angle=d3d11', '--enable-gpu', '--ignore-gpu-blocklist'] if bn == 'chromium' else [])
    for sz in sizes.split(','):
        w, h = map(int, sz.split('x')); mob = w < 1000 and h > w or w < 700
        ctx = b.new_context(viewport={'width': w, 'height': h}, has_touch=mob, is_mobile=(bn == 'chromium' and mob), device_scale_factor=2 if mob else 1)
        pg = ctx.new_page()
        pg.on('pageerror', lambda e: errs.append(f'{sz} pageerror {e}'))
        pg.on('console', lambda m: m.type in ('error', 'warning') and errs.append(f'{sz} {m.type} {m.text[:300]}'))
        pg.goto(url, wait_until='domcontentloaded'); pg.wait_for_selector('#loader.done', state='attached', timeout=60000); pg.wait_for_timeout(2500)
        if not mob: pg.mouse.move(w * .72, h * .38)
        n = int(pg.evaluate('document.querySelectorAll(".sc").length'))
        gls = []
        ids = range(n) if which == 'all' else [int(x) for x in which.split(',')]
        for i in ids:
            pg.evaluate(f'__go({i})'); pg.wait_for_timeout(2600); pg.screenshot(path=str(out / f'{bn}_{w}x{h}_{i+1:02d}.png'))
            gls.append(pg.evaluate('document.querySelectorAll(".ph>canvas").length'))
        if 'burn' in extra:
            pg.evaluate('__go(4)'); pg.wait_for_timeout(2500)
            for f in (.5, .62, .74, .86, .95):
                pg.evaluate(f'__go({4+f-.34},1)'); pg.wait_for_timeout(350 if bn == 'chromium' else 1200); pg.screenshot(path=str(out / f'{bn}_{w}x{h}_burn{int(f*100)}.png'))
        if 'trans' in extra:
            for i in (3, 9, 11):
                for f in (.6, .75, .9):
                    pg.evaluate(f'__go({i+f-.34},1)'); pg.wait_for_timeout(600); pg.screenshot(path=str(out / f'{bn}_{w}x{h}_t{i+1:02d}_{int(f*100)}.png'))
        if 'fin' in extra:
            pg.evaluate('__go(20)'); pg.wait_for_timeout(3000); pg.screenshot(path=str(out / f'{bn}_{w}x{h}_roll.png'))
            pg.keyboard.press('ArrowRight'); pg.wait_for_timeout(9000); pg.screenshot(path=str(out / f'{bn}_{w}x{h}_fin.png'))
        info = pg.evaluate('({gl:document.querySelectorAll(".ph>canvas").length, folio:document.querySelector("#count").textContent})')
        print(sz, info, 'gl por escena:', gls)
        ctx.close()
    b.close()
print('errores:', errs or 'ninguno')
