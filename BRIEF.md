# Guatemala después de Árbenz (1954–1959): brief para Claude Code

ZETH Centro Educativo. Historia, 4.º Bachillerato.
Integrantes: Víctor Robles y Guillermo Cifuentes.

Repo: https://github.com/ogboyys009-create/presentacion-historia (público; hace falta para GitHub Pages gratis)
Preview v2 (fuente completa, un solo HTML): https://claude.ai/artifact/1VEFhDZpJJ7xQvTPibF8pG
Kit descargable: `kit-para-code.zip` (HTML v2, imágenes, mapas de profundidad, script de profundidad, este brief).

## 1. Objetivo

Presentación web animada, estilo "sitio cinematográfico" (referencias: TikToks de sitios 3D hechos con Claude), con aire histórico pero moderno. Se expone en clase: debe funcionar con teclado o mando (← → espacio) y también con scroll en móvil. Entrega: un solo `index.html` publicado en GitHub Pages.

## 2. Dirección visual (decidida en v2)

El lenguaje sale del propio material de 1954: grabado de Ismael Aroche, portada de Prensa Libre y expedientes de la Guerra Fría.

- Colores: papel `#E9E2D0`, tinta `#15130F`, rojo sello `#B3261E`, gris humo `#8C8577`.
- Tipos: Barlow Condensed 500/700/800 (titulares, como los carteles y periódicos de la época), Old Standard TT (texto, tipografía de libro antiguo), Special Elite (máquina de escribir, solo en el expediente).
- Todas las fotos pasan por un shader: duotono tinta/papel + trama de semitono de periódico a 45°. Así fotos de fuentes distintas se ven como una sola edición impresa.
- Transición firma: disolución de tinta con ruido fbm; el papel "se quema" con borde de tinta y un filo rojo, y descubre la escena siguiente.
- 2.5D: cada foto es un plano subdividido (220×220) desplazado por su mapa de profundidad (Depth Anything V2). La cámara nunca está quieta, así que el paralaje revela el relieve.
- Grano de película en overlay. Sellos rojos que "golpean" (ANULADA, DISUELTO, PROHIBIDAS, SUSPENDIDO). Barras de censura que se retiran en el expediente.

## 3. Estructura y textos (versión aprobada para v2)

| # | Escena | Fondo / imagen | Efecto clave | Texto |
|---|---|---|---|---|
| 0 | Portada | Grabado de Aroche (relieve) | Título en máscara | Guatemala después de Árbenz, 1954–1959, integrantes |
| 1 | 1954: La «Liberación» | Foto del desfile (Árbenz de perfil) | Expediente PBSUCCESS, censura que se retira, sello GUERRA FRÍA | Organiza la CIA; rivalidad EE. UU.–URSS; objetivo derrocar a Árbenz; acusación de comunismo por políticas nacionalistas. Nota: "Recreación visual. No es un documento original." |
| 2 | El exilio | Portada de Prensa Libre | El periódico cae y se asienta con curvatura de papel | Tras refugiarse en la embajada de México, Árbenz y otros dirigentes salen del país |
| 3 | Fin de la primavera | Árbenz en uniforme (oscuro) | Línea 1944–1954 que se quiebra; sellos | ANULADA Constitución de 1945; DISUELTO Congreso; PROHIBIDAS organizaciones populares |
| 4 | Contrarreforma agraria | Grabado de Aroche otra vez | Sello gigante SUSPENDIDO sobre el grabado | Estatuto Agrario suspende el Decreto 900; tierras devueltas a antiguos dueños y a la United Fruit Company |
| 5 | Castillo Armas en el poder (1954–57) | Sin foto aún (marco "pendiente") | Bloques con filete rojo | Constitución de 1956; Comité de Defensa Nacional contra el Comunismo |
| 6 | Magnicidio | Negro | Fecha 26·07·57 cae dígito a dígito en rojo | Muere baleado en un corredor de la Casa Presidencial; se señaló al soldado Romeo Vásquez Sánchez, hallado muerto poco después; disputa entre facciones militares |
| 7 | Inestabilidad (1957–60) | Papel | Cronología que se rellena en rojo | 1957 gobierno provisional; 1957 elecciones anuladas por fraude; marzo 1958 asume Ydígoras; 1958–60 protestas y Ejército dividido; 13 nov 1960 sublevación, germen del conflicto armado |
| 8 | Personajes | Papel | Tarjetas que giran en 3D | Árbenz, Castillo Armas, Ydígoras (una línea cada uno) |
| 9 | Cierre | Retrato formal de Árbenz | Relieve oscuro | De la primavera al conflicto. Gracias. |

## 4. Corrección de datos

- El texto original dice que Castillo Armas fue baleado "en las gradas del Palacio Nacional". Las crónicas de Prensa Libre lo sitúan en un corredor de la Casa Presidencial, cuando iba al comedor con su esposa Odilia Palomo. La v2 ya usa "corredor de la Casa Presidencial".
- Todo lo demás del texto de los alumnos se mantiene. Antes de exponer, revisar fechas con el profesor o el libro de texto.

## 5. Imágenes

Mapeo de archivos subidos:

| Archivo | Nombre en el proyecto | Contenido |
|---|---|---|
| IMG_0940 | poster | Grabado "¡Una realidad! Ley de Reforma Agraria", Ismael Aroche |
| IMG_0939 | desfile | Árbenz de perfil con gorra y gafas en un desfile |
| IMG_0938 | sonrie | Árbenz sonriendo con banda (tarjeta de personajes) |
| IMG_0937 | uniforme | Árbenz en uniforme militar |
| IMG_0936 | retrato | Retrato formal de Árbenz |
| IMG_0941 | periodico | Prensa Libre: "Arbenz, Díaz, Fortuny y otros más salieron anoche a México" |

Pedir a los alumnos (prioridad en orden):
1. Carlos Castillo Armas, retrato (escenas 5 y 8).
2. Miguel Ydígoras Fuentes, retrato (escenas 7 y 8).
3. Castillo Armas y el Ejército de Liberación entrando a la capital, 1954 (escena 1 o 5).
4. United Fruit Company: plantación, tren o barco bananero (escena 4).
5. Casa Presidencial / Palacio Nacional de Guatemala (escena 6).
6. Portada de la Constitución de 1956 (escena 5).
7. Protestas estudiantiles 1958–1960 (escena 7).
8. Sublevación del 13 de noviembre de 1960 (escena 7 o cierre).

Cada imagen nueva pasa por `depth.py` para generar su mapa de profundidad.

## 6. Pipeline técnico

- Profundidad: `depth.py` usa `onnx-community/depth-anything-v2-small` (ONNX, ~99 MB) con onnxruntime en CPU. Entrada 518×518, salida normalizada 0–1, suavizado gaussiano r=3. Funciona sin GPU.
- Assets: imágenes en escala de grises, máx. 1100 px, JPEG q80 + autocontraste; mapas de profundidad PNG máx. 320 px. Se incrustan como data URI. Peso actual del HTML: ~740 KB.
- Render: Three.js r128 (cdnjs). ShaderMaterial propio (desplazamiento por profundidad en vertex shader, duotono + semitono + disolución en fragment). `autoClear=false` y `clearDepth()` entre planos para que el relieve de una foto no atraviese la de delante.
- Scroll: cada escena mide 1,25 pantallas. `sf = scrollY / (1.25*innerHeight)`. La transición visual ocurre en el último 28 % de cada escena. Suavizado por lerp (0,09). `?snap` desactiva el suavizado para capturas automáticas.
- Navegación: ← → ↑ ↓ espacio, RePág/AvPág, Inicio/Fin; raíl lateral clicable; contador 01/10.
- Accesibilidad: `prefers-reduced-motion` quita deriva y grano; textos en DOM real (no en canvas).
- Revisión visual: Playwright + Chromium con SwiftShader, capturas en 390×844 y 1440×900.

## 7. Plan en Claude Code

1. Crear estructura del repo: `src/` (plantilla + escenas), `assets/` (originales y profundidad), `scripts/` (depth, build), `index.html` generado.
2. Script de build que incruste assets y genere el `index.html` único.
3. Subir, y el usuario activa Pages: Settings → Pages → Deploy from branch → `main` / root.
4. Mejoras visuales:
   - Separar sujeto y fondo con la profundidad para un "dolly zoom" (fondo y persona a distinta velocidad).
   - Fotos que se revelan como si se imprimieran (la trama aparece punto a punto).
   - Mapa de Guatemala en 3D (escena 1 o cierre) con el recorrido de la invasión de 1954 desde Honduras, dibujado como grabado.
   - Escena del magnicidio: silencio, un destello, la fecha.
   - Sonido opcional: tipeo de máquina, golpe de sello, imprenta.
   - Modo presentador: pausa en cada escena hasta pulsar tecla.
   - Transición de página de periódico que se pliega (vértices).
5. Rendimiento: probar en el iPad y el portátil de la exposición; pixelRatio máx. 2; fallback sin WebGL (fotos planas + CSS).
6. Opcional: clips de Higgsfield (si los alumnos los generan) integrados como secuencias de fotogramas controladas por scroll.

## 8. Problemas conocidos de la v2

- Escenas 5 y 8 tienen huecos de foto pendientes.
- En móvil el sello SUSPENDIDO tapa parte del grabado; recolocar.
- El encuadre del desfile en vertical depende de `fx` (0,04); revisar cuando haya más fotos.
- Las escenas sin foto (5, 6, 7) son solo tipográficas; ganarían con una imagen o elemento 3D.
