# Estado actual: v3 (leer junto a BRIEF.md; esto manda si hay contradicción)

Preview v3: https://claude.ai/artifact/1VEFhDZpJJ7xQvTPibF8pG
Kit: `kit-para-code.zip` (HTML v3, plantilla `scripts/template3.html`, 16 imágenes con sus mapas de profundidad, originales, script de profundidad, brief).

## Qué cambió respecto a la v2

- 12 escenas (antes 10). Nuevas: Castillo Armas con retrato propio, Constitución de 1956 como documento, crisis con la foto «Que renuncie Ydígoras», cierre con multitud. El orden real está en el array `SCENES` de la plantilla.
- Layout por pantalla: en PC/Mac/iPad horizontal (`.wide`) los retratos van enteros con marco de papel a la derecha y el texto a la izquierda; en vertical (`.narrow`) las fotos van a sangre y el texto abajo.
- Dos capas 3D por escena: foto principal con relieve (z=0) y foto de fondo en semitono grande y bicolor (z=-6). El paralaje entre capas es real.
- Cursor: la cámara orbita con el ratón, la luz del relieve sigue al cursor (normales calculadas del mapa de profundidad en el shader) y los textos se desplazan en sentido contrario. Cursor propio con forma de marca de registro.
- iPad/móvil: giroscopio. En iOS aparece un botón «Activar movimiento» porque Safari exige permiso.
- Retro moderno: cinta de noticias arriba, «Edición 01/12», marcas de registro en las esquinas, año gigante en contorno detrás del texto, titulares con sombra roja desplazada, letras que caen una a una, error de registro rojo durante transiciones y al mover el cursor rápido, la trama se agranda antes de quemarse, destello blanco al entrar al magnicidio.

## Imágenes nuevas y pies de foto

| Archivo | Nombre | Uso | Aviso |
|---|---|---|---|
| IMG_3324 | castillo | Escena 5 y tarjeta | |
| IMG_3325 | ydigoras | Escena 8 y tarjeta | |
| IMG_3326 | jeep | Fondo escenas 1 y 5 | Identidades sin confirmar; no se nombra a nadie |
| IMG_3327 | guyamel | Recorte en escena 4 | Es la Guyamel Fruit Co., no la United Fruit (la absorbió en 1929) |
| IMG_3328 | casapres | Escena 7 | Era una captura de pantalla; recortada |
| IMG_3329 / IMG_3330 | palacio2 / palacio | Fondos | Recortado el borde gris |
| IMG_3331 | constitucion | Escena 6 | |
| IMG_3332 | protesta | Escena 9 | Probablemente jornadas de 1962; pie «años sesenta» |
| IMG_3333 | multitud | Cierre y fondo de portada | Es de décadas después (cartel del Che); pie «décadas después» |

## Pendiente para Code

- Probar en el Mac, el iPad y el proyector reales (rendimiento con 240×240 vértices por foto).
- Sonido opcional: máquina de escribir, golpe de sello, imprenta.
- Modo presentador y fallback sin WebGL.
- Build que incruste assets y genere `index.html`; activar Pages (Settings → Pages → `main` / root).
