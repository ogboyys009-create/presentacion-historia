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

## Técnica actual (v7)

- Navegación por folios (no por scroll): cada folio se queda quieto hasta que se avanza con → ↓ espacio Enter AvPág, clic, rueda, deslizar el dedo, tocar la mitad derecha (izquierda: volver) o un mando (A/RB avanzar, B/LB volver). Inicio/Fin, 1–9, índice lateral. F pantalla completa, S sonido. `#n` en la URL abre el folio n.
- Portada de acceso «Abrir el expediente»: el clic pone la pantalla completa (en iPhone no existe; se indica «Añadir a pantalla de inicio», con manifest e icono).
- Transición de llegada distinta en cada folio (`TR` en la plantilla): II inmersión en la foto del escritorio, III y IX la hoja que se quema (con curvatura del papel, pavesas y humo), IV tinta que se corre, V diafragma de cámara que se cierra sobre el rostro, VI papel que se retira de la mesa, VII rollo de película, VIII corte a negro y luz que parpadea (magnicidio), X persianas de noticiero, XI desenfoque, XII regreso al escritorio. Al retroceder o saltar: fundido a negro.
- Escritorio 3D (I y XII): `scripts/escritorio.py` lo modela en Blender por código y exporta `assets/escritorio.glb` (~400 KB, sin Draco). En la web: luz de foco real desde la lámpara de latón que apunta a donde está el cursor, sombras, entorno tenue, polvo en el haz. Las copias fotográficas son planos con textura de lienzo.
- Profundidad: `scripts/capas.py` (Depth Anything V2 base, dos escalas) genera `_depth.png` (R profundidad, G máscara del sujeto) y `_bg.jpg` (fondo con el hueco rellenado por difusión). Retratos con `layers:true`: placa de fondo detrás (z = -0,07·alto) y sujeto delante con su máscara. El jeep no usa capas (el grupo no se separa bien).
- Sonido sintetizado con WebAudio (papel, máquina, sello, crepitar, proyector), apagado por defecto.
- Calidad automática: si el promedio pasa de 26 ms por fotograma baja la resolución, el polvo y las sombras.
- Modo seguro sin WebGL (`?nogl`), `?snap` para capturas; `window.__go(i,true)` salta a un folio y `window.__freeze=p` congela una transición (lo usa `scripts/capturas.py --trans`).

## Verificación antes de dar algo por terminado

1. Capturas con Playwright en 1440×900, 1180×820 (iPad horizontal), 820×1180 (iPad vertical) y 390×844, con Chromium y con WebKit.
2. Cursor en al menos dos posiciones para confirmar que la lámpara y la profundidad se notan.
3. Sin errores de consola. Modo seguro funcionando.
4. Revisar cada captura con ojo de director de arte y corregir antes de enseñar nada al usuario.

## Herramientas verificadas

- Blender con el add-on MCP respondió desde el chat (escena por defecto abierta). Confirmar la conexión desde Claude Code antes de la fase 3.
- GitHub conectado: el repo existe y ya tiene commits (`BRIEF.md`, `ESTADO-V3.md`, `ESTADO-V4.md`).
