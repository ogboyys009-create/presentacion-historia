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

## Técnica actual (versión definitiva, 21 folios)

Historial corto: la v7 («juego de Poki») y la v8 (IA, bordes blancos) se rechazaron; la v9 se aprobó («ahora sí») y la definitiva parte de ella con estos pedidos del cliente: sin recortes de personas (solo capas en el último folio), sin censuras, bordes limpios, relieve 3D sutil en las fotos, papeles desclasificados que se queman al pasar, transiciones suaves (nada de «golpes»), fuentes de la información (no de imágenes) en créditos de película, FIN solo y centrado, toque en móvil/iPad y aire de **expediente**.

- Página: `web/index.html` (sin plantilla) + `web/img/*.webp` + `web/fonts/*.woff2` (fuentes OFL alojadas en la web: no depende de Google Fonts, que puede fallar en la red del colegio; la carga espera las fuentes como mucho 3 s). `scripts/build.py` copia `web/` a `dist/`, incrusta `__SIZES__` y añade manifest e icono. Unos 4,7 MB.
- Escenario: cada folio es un contexto 3D de CSS (`perspective:1000px`); `place()` compensa escala y posición de cada capa según su z. Objetos físicos enteros (copias fotográficas, documentos, recortes, sellos) con sombra, inclinación y brillo según el cursor. Maquetación medida en `layout()`: columna de texto y área de imágenes separadas, el texto se reduce (`--z`) si no cabe, pies de foto (máquina de escribir) debajo de las imágenes.
- Navegación discreta: una diapositiva por gesto (→/espacio/AvPág/Intro, clic, rueda con bloqueo de ráfagas, tocar = avanzar y tercio izquierdo = retroceder, deslizar, mando). Interpolación Hermite de 2,5 s que conserva la velocidad si se encadenan pulsaciones. Transición = fundido cruzado con la cámara acercándose despacio (sin destello).
- WebGL (opcional, con respaldo en `<img>`): grupo fijo de 4 contextos reutilizables (Safari tarda en liberar contextos; nunca crear uno por imagen). Relieve de fotos: mapa de profundidad (`*_d.webp`, Depth Anything V2 base) y desplazamiento por punto fijo, con cursor, deriva lenta y movimiento de cámara; encuadre `PZ=.955` igual al de la `<img>` escalada. Quemado de los memorandos de la CIA al avanzar desde el folio 5: frente de ruido + distancia, brasa, papel tostado, chispas/ceniza/humo en `#fx`; la siguiente escena se ve por los huecos. El sello DESCLASIFICADO se pinta también dentro de la textura para que arda con el papel.
- Portada: fotografías de la época que no salen en las diapositivas (`p_*`) flotando hacia el espectador; sello CONFIDENCIAL. Personajes: fichas con clip. Créditos: rodillo por tiempo con las fuentes por tema; → lo adelanta; al terminar, «Fin» solo y centrado con cierre de iris.
- Imágenes: `scripts/web_assets.py` sin IA ni ampliación: recorta marcos y líneas de escaneo del canto (`trim` + `edges`), B/N con virado cálido, documentos en color de papel, mapas de profundidad en caché (`assets/hd/`, fuera del repo).
- Medido: 60 FPS con GPU en 1440×900 y en móvil 3x (3 fotogramas >33 ms de ~4100, en reposo); sin GPU, 44 FPS en 1440×900. Sin errores de consola en Chromium y WebKit.

## Verificación antes de dar algo por terminado

1. Capturas con Playwright en 1440×900, 1180×820 (iPad horizontal), 820×1180 (iPad vertical) y 390×844, con Chromium y con WebKit, sirviendo `dist/` por HTTP (con `file://` WebGL no puede leer las imágenes). Scripts en la carpeta de trabajo: `cap11.py`, `ctl11.py` (controles), `perf11.py` (fluidez), `depth11.py` (relieve).
2. Cursor en al menos dos posiciones para confirmar que la lámpara y la profundidad se notan.
3. Sin errores de consola. Modo seguro funcionando.
4. Revisar cada captura con ojo de director de arte y corregir antes de enseñar nada al usuario.

## Herramientas verificadas

- Blender con el add-on MCP respondió desde el chat (escena por defecto abierta). Confirmar la conexión desde Claude Code antes de la fase 3.
- GitHub conectado: el repo existe y ya tiene commits (`BRIEF.md`, `ESTADO-V3.md`, `ESTADO-V4.md`).
