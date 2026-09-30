# Guatemala después de Árbenz (1954–1959)

Presentación web en 3D para la clase de Historia de 4.º Bachillerato, ZETH Centro Educativo.
Integrantes: Víctor Robles y Guillermo Cifuentes. Se expone en clase (teclado o mando) y se abre en PC, Mac, iPad y móvil.

- Repo: https://github.com/ogboyys009-create/presentacion-historia (público, para GitHub Pages).
- Versión de referencia aprobada: `referencia/v6-actual.html`. Todo lo nuevo parte de aquí y tiene que superarla.
- Entrega final: un solo `index.html` autocontenido publicado en GitHub Pages.

## Dirección de arte (decidida con el cliente; no negociable)

Tono: **trágico, dramático, histórico, serio, elegante, sobrio**. Debe parecer una investigación o un informe de Estado de los años cincuenta, presentado por alguien con autoridad. Nunca un videojuego.

Concepto: **un archivo en penumbra examinado con una lámpara**. El cursor (en iPad, el dedo o la inclinación) ilumina lo que se examina con luz lateral que revela el relieve de las fotos. La penumbra es moderada: la v5 quedó demasiado oscura y el cliente pidió más luz y más seriedad.

- Ritmo claro/oscuro: retratos y fotos de época en escenas oscuras; documentos (periódico, grabado de la reforma agraria, Constitución de 1956) sobre papel marfil.
- Transición firma, pedida expresamente: **la hoja que se quema**. La imagen saliente se chamusca, se carboniza y arde con un borde de brasa naranja, y descubre la siguiente. No sustituirla.
- Folio V (reforma agraria): sello **SUSPENDIDO / DECRETO 900 · 1954** grande, rojo sólido, con textura de goma, que golpea el grabado (el grabado tiembla en el impacto). Tiene que ser lo que más resalta de la escena.

- Colores: negro azulado `#07090C` / `#0B0E13`, marfil `#ECE6D8`, latón `#A58B57` (filetes, fechas, índice), granate `#6B1E1E` (solo sellos y lo trágico).
- Tipografía: Bodoni Moda (titulares y fechas), Libre Caslon Text (texto, fuentes, membrete en versalitas), Special Elite solo en el expediente PBSUCCESS.
- Membrete fijo «Informe de Historia · Guatemala» y «Folio IV de XII»; índice lateral en números romanos; franjas negras de cine en pantallas anchas.
- Fotos: copia en gelatina de plata (curva suave, viñeta, grano fino). Retratos en pantallas anchas: enteros, con paspartú marfil y filete de latón, a la derecha. En vertical: a sangre.
- Cada escena tiene dos capas 3D: foto principal con relieve por mapa de profundidad (z=0) y fondo desenfocado y oscuro (z=-7), más polvo en suspensión delante de la cámara.
- Entrada de cada folio: fundido desde negro. Salida: la hoja que se quema.
- Animaciones de texto: líneas que suben tras máscara con easing cúbico, fades cortos, sellos de goma que se asientan, barras de censura que se retiran.

### Rechazado (no volver a esto)

La v3 «retro moderna» se rechazó por parecer videojuego: cinta de noticias, cursor en forma de mira, sombras rojas desplazadas en titulares, año gigante en contorno, semitono de puntos gruesos, descuadre de color rojo, letras que giran, destellos. La v4 se aprobó en estilo pero le faltaba drama y el efecto de profundidad con el cursor se notaba poco. La v5 resolvió eso con la lámpara, pero quedó demasiado oscura. La v6 (actual) aclara la penumbra, devuelve los documentos al papel, recupera la hoja quemada de la primera versión y hace protagonista el sello SUSPENDIDO.

## Contenido (12 folios, textos aprobados en `src/template.html`)

| Folio | Tema | Imagen principal | Fondo |
|---|---|---|---|
| I | Portada | desfile (Árbenz de perfil) | desfile desenfocado |
| II | La «Liberación», junio 1954: expediente PBSUCCESS (CIA, Guerra Fría, derrocar a Árbenz, acusación de comunismo). Nota: «Recreación visual. No es un documento original.» | jeep | — |
| III | El exilio | periódico Prensa Libre (cae sobre la mesa) | palacio2 |
| IV | Fin de la primavera: ANULADA Constitución de 1945, DISUELTO Congreso, PROHIBIDAS organizaciones populares | uniforme (Árbenz) | uniforme |
| V | Contrarreforma agraria: Estatuto Agrario suspende el Decreto 900; tierras devueltas a antiguos dueños y a la United Fruit Company. Sello SUSPENDIDO y recorte Guyamel | poster (grabado de Ismael Aroche) | poster desenfocado |
| VI | Carlos Castillo Armas, 1954–1957 | castillo | jeep |
| VII | Un Estado anticomunista: Constitución de 1956 y Comité de Defensa Nacional contra el Comunismo | constitucion | palacio |
| VIII | Magnicidio, 26 de julio de 1957 (luz que parpadea) | casapres | palacio |
| IX | Transición e inestabilidad 1957–1960 (cronología) | ydigoras | protesta |
| X | Clima de crisis | protesta | — |
| XI | Personajes: Árbenz, Castillo Armas, Ydígoras (galería) | — | palacio2 |
| XII | De la primavera al conflicto. Gracias. | multitud | — |

### Rigor histórico (obligatorio)

- Castillo Armas murió en **un corredor de la Casa Presidencial** (no «en las gradas del Palacio Nacional», como decía el texto original de los alumnos). Fuente: crónicas de Prensa Libre.
- `guyamel`: es la **Guyamel Fruit Co.**, no la United Fruit; la United Fruit la absorbió en 1929. Pie de foto ya corregido.
- `protesta` («Que renuncie Ydígoras»): probablemente jornadas de 1962. Pie: «años sesenta».
- `multitud` (cartel del Che): décadas posteriores. Solo en el cierre, con pie «décadas después».
- `jeep`: identidades sin confirmar; no nombrar a nadie.
- No inventar citas ni documentos. Si algo se recrea, se dice.

## Archivos

- `src/template.html`: toda la lógica (Three.js r128 por cdnjs, shaders, escenas, textos). `__ASSETS__` se sustituye en el build.
- `assets/procesadas/`: `<nombre>.jpg` + `<nombre>_depth.png` (16 imágenes). `assets/originales/`: archivos tal como los pasaron los alumnos.
- `scripts/build.py`: genera `dist/index.html` incrustando todo.
- `scripts/depth.py <imagen> <nombre>`: genera imagen procesada y mapa de profundidad (Depth Anything V2, ONNX, CPU).
- `referencia/estilo/`: hojas de contacto y videos de las referencias (TikToks de sitios 3D cinematográficos). Extraer fotogramas con ffmpeg si hace falta.
- `docs/`: historial de decisiones.

## Técnica actual (v8, rehecha desde cero)

El cliente rechazó la v7 («parece juego de Poki», transiciones feas, va trabada) y pidió una web como las de sus videos de referencia (sitios 3D de scroll cinematográfico tipo Vela Armon): simple, seria, fluida.

- Sin WebGL. Cada escena es un contexto 3D de CSS (`perspective:1000px`) con capas de imagen a distinta z: fondo lejano desenfocado (`_blur`, z=-900), fondo de la foto con el hueco rellenado (`_bg`, z=-420) y sujeto recortado (`_fg`, z=0). `place()` compensa escala y posición para que en reposo encajen; la cámara es `translateZ` del contenedor más una inclinación con el cursor.
- Scroll suave (lerp) que mueve la cámara: la escena llega desde el fondo, avanza despacio mientras se lee y la cámara la atraviesa hacia su punto focal (`o`); cruce breve a oscuras y llega la siguiente. Flechas/espacio/AvPág saltan de escena con una interpolación de 1,1–2,2 s. F pantalla completa.
- Documentos (periódico, grabado, Constitución) son papeles que caen y se asientan en 3D; el sello SUSPENDIDO golpea el grabado. Personajes: tres fichas en abanico.
- Imágenes: `scripts/web_assets.py` amplía x4 con Real-ESRGAN (`scripts/esrgan.onnx`, caché en `assets/hd/`, ambos fuera del repo), aplica virado de plata cálido, refina la máscara del sujeto con filtro guiado y exporta WebP a `web/img/`. Las máscaras y profundidades salen de `scripts/capas.py`.
- `web/index.html` es la página (sin plantilla). `scripts/build.py` copia `web/` a `dist/` y añade manifest e icono. Unos 2,6 MB en total, carga progresiva.
- Medido: 60 FPS con GPU (1440×900, 2560×1440, iPad 2x) y 60 FPS sin GPU en tamaño móvil.
- Tipografía: Instrument Serif (titulares) e Inter (textos). Esto sustituye a la dirección de arte anterior (Bodoni, membrete, hoja quemada) por decisión del cliente.

## Verificación antes de dar algo por terminado

1. Capturas con Playwright en 1440×900, 1180×820 (iPad horizontal), 820×1180 (iPad vertical) y 390×844, con Chromium y con WebKit.
2. Cursor en al menos dos posiciones para confirmar que la lámpara y la profundidad se notan.
3. Sin errores de consola. Modo seguro funcionando.
4. Revisar cada captura con ojo de director de arte y corregir antes de enseñar nada al usuario.

## Herramientas verificadas

- Blender con el add-on MCP respondió desde el chat (escena por defecto abierta). Confirmar la conexión desde Claude Code antes de la fase 3.
- GitHub conectado: el repo existe y ya tiene commits (`BRIEF.md`, `ESTADO-V3.md`, `ESTADO-V4.md`).
