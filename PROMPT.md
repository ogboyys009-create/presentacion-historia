Eres el ingeniero principal y director de arte de este proyecto. Lee primero `CLAUDE.md` completo y abre `referencia/v6-actual.html` en un navegador (Playwright) para ver exactamente dónde estamos. Mira también las hojas de contacto de `referencia/estilo/`.

## Objetivo

Convertir la v6 en la versión definitiva de la presentación «Guatemala después de Árbenz (1954–1959)»: una experiencia 3D cinematográfica, trágica y dramática, con aire de investigación histórica seria, al nivel de los sitios 3D de las referencias. Entrega: un solo `index.html` publicado en GitHub Pages, que funcione perfecto en PC, Mac, iPad y móvil, y con teclado o mando en clase.

La dirección de arte, el contenido y el rigor histórico de `CLAUDE.md` no se negocian. Lo rechazado (estética de videojuego y la penumbra excesiva de la v5) no vuelve. Tono: serio, trágico y elegante, pero legible y con luz suficiente.

## Qué tienes a mano

- **GitHub:** repo `ogboyys009-create/presentacion-historia`. Ya tiene `BRIEF.md`, `ESTADO-V3.md` y `ESTADO-V4.md` en la raíz; muévelos a `docs/`.
- **Blender con su MCP.** Ya respondió desde el chat; comprueba la conexión antes de la fase 3.
- Python, ffmpeg y Playwright.

## Trabajo, por fases (enséñame capturas al final de cada fase)

**Fase 1. Base.** Clona el repo y copia esta carpeta dentro. Comprueba que `python3 scripts/build.py` genera `dist/index.html` idéntico en comportamiento a la v6. Añade `.gitignore` (excluye `scripts/da.onnx`). Crea un workflow de GitHub Actions que ejecute el build y publique `dist/` en Pages. Después dime exactamente qué clic tengo que dar en Settings → Pages; no lo asumas hecho.

**Fase 2. Profundidad de verdad.** Hoy cada foto es una sola malla desplazada, y al girar mucho se estira en los bordes del sujeto. Quiero parallax real sin estiramientos:
- mapas de profundidad de más calidad (Depth Anything V2 base o large);
- separar sujeto y fondo en capas con la profundidad y una máscara limpia;
- rellenar el hueco que deja el sujeto (inpainting);
- colocar las capas a distinta z.

El movimiento del cursor tiene que notarse claramente, pero siempre elegante.

**Fase 3. El archivo en Blender.** Modela en Blender, vía MCP, un despacho-archivo de los años cincuenta en penumbra: escritorio de madera oscura, lámpara de latón, carpetas de expediente, máquina de escribir, papeles. Iluminación dramática. Exporta a `.glb` optimizado (Draco o meshopt, texturas pequeñas) e incrústalo en el HTML. Úsalo como hilo conductor:
- la portada y el cierre ocurren sobre el escritorio;
- entre capítulos la cámara vuela por la mesa;
- los documentos (periódico, Constitución de 1956, grabado, expediente PBSUCCESS) son objetos físicos sobre la mesa;
- la lámpara del cursor es la lámpara real de la escena.

Presupuesto total del HTML: menos de 15 MB, y que cargue rápido en iPad.

**Fase 4. Dirección cinematográfica.** Conserva la transición de la hoja que se quema (la pidió el cliente) y hazla aún mejor: humo, pavesas que suben, papel que se curva al arder. Mejora el resto (movimientos de cámara continuos), el ritmo del texto y el momento del magnicidio. Sonido opcional y apagado por defecto (papel, máquina de escribir, sello), con un botón discreto para activarlo. Añade un modo presentador: cada folio se queda quieto hasta que pulso una tecla.

**Fase 5. Pulido y verificación.** Aplica la lista de verificación de `CLAUDE.md` con Chromium y WebKit en los cuatro tamaños. Mide los FPS en iPad (usa emulación si no hay otra forma) y baja calidad automáticamente si hace falta. Comprueba el modo seguro sin WebGL. Revisa ortografía y tildes de todos los textos.

## Reglas

- Antes de escribir código en cada fase, dime en pocas líneas qué vas a hacer.
- Si algo no se puede hacer con lo que tienes (una conexión, un permiso, un archivo), dímelo en el momento y dime exactamente qué necesitas. No lo simules ni lo des por hecho.
- Nunca des por buena una versión sin haber mirado tus propias capturas como director de arte exigente.
- No cambies hechos históricos ni pies de foto sin decírmelo. No inventes citas.
- Haz commits pequeños con mensajes claros en español y empuja a `main` al terminar cada fase.
- Al final dame la URL pública de GitHub Pages y un resumen de cómo presentar en clase.

Empieza por la Fase 1.
