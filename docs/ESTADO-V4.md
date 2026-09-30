# Estado actual: v4 (manda sobre BRIEF.md y ESTADO-V3.md)

Preview v4: https://claude.ai/artifact/1VEFhDZpJJ7xQvTPibF8pG
Plantilla: `scripts/template4.html` dentro de `kit-para-code.zip`.

## Decisión del cliente

La v3 (retro moderno: cinta de noticias, cursor de mira, sombras rojas, semitono grueso, descuadre de color) se rechazó por parecer videojuego. La v4 vuelve al enfoque de la v2 con tono de **informe de Estado de los años cincuenta**: histórico, profesional, serio, elegante, sobrio. Tiene que parecer una investigación, no un juego. No reintroducir efectos llamativos.

## Sistema visual v4

- Colores: azul marino casi negro `#121821` (fondo principal), marfil `#ECE6D8` (papel y texto), latón `#A58B57` (filetes, fechas, índice), granate `#6B1E1E` (solo sellos), piedra `#8A8577`.
- Tipos: Bodoni Moda (titulares, fechas; tipografía de imprenta oficial), Libre Caslon Text (texto, fuentes, membrete en versalitas), Special Elite solo en el expediente.
- Membrete fijo: «Informe de Historia · Guatemala» y «Folio III de XII»; índice lateral en números romanos.
- Fotos: copia en gelatina de plata (curva suave, viñeta, grano fino). Sin semitono salvo un toque en el periódico.
- Retratos en pantallas anchas: enteros, con paspartú marfil y filete de latón, a la derecha. En vertical, a sangre.
- Fondo de cada escena: la misma foto u otra relacionada, desenfocada (mipmaps con bias) y oscurecida, a z=-7. Da profundidad de campo real.
- Cursor: órbita de cámara contenida (±0,075 rad), la luz del relieve sigue al cursor, los textos se mueven 5 px. iPad: giroscopio con botón de permiso.
- Transición: fundido con bordes de humo (fbm), sin color.
- Animaciones: líneas que suben tras máscara con easing cúbico, fades cortos, sellos de goma que se asientan (sin giros bruscos), censura que se retira en el expediente, cronología con filete de latón.
- Desplazamiento por profundidad atenuado en los bordes (`uEdge`) para que el paspartú no se deforme.

## Pendiente para Code

- Probar en el Mac, el iPad y el proyector reales.
- Build que incruste assets y genere `index.html`; activar Pages.
- Opcional: sonido muy discreto (papel, máquina de escribir), modo presentador, fallback sin WebGL.
