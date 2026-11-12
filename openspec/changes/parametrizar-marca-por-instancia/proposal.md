# Proposal

## Why

La misma base de código sirve dos instancias con distinta marca — IES
(entrenamientos.ies.com.uy) e Infratec (entrenamientos.infratec.com.uy) — pero
hoy la marca está *hardcodeada*: colores vía un override de `:root` en
`styles.css`, textos "IES"/"Infratec" repartidos en `index.html`, `assets/app.js`
y `api/*.php`, y los logos como archivos sueltos. Eso obliga a mantener dos ramas
que divergen: cada arreglo del motor hay que portarlo a mano y cada rebrand toca
decenas de archivos. Un cambio de contenido en una instancia no llega a la otra
sin cherry-pick, y es fácil que un string de la marca equivocada quede visible.

## What Changes

- Se introduce una **configuración de marca por instancia** (un único archivo de
  tema: nombre, wordmark/monograma, paleta, tipografías, dominios, textos legales)
  que el front y el back leen en tiempo de ejecución.
- La UI toma colores, nombre y logos del tema; se eliminan los valores de marca
  hardcodeados del CSS/JS/PHP a favor de variables y textos parametrizados.
- Una sola rama `main` sirve ambas instancias; la instancia se determina por su
  archivo de tema (no versionado con secretos, como `config.php`).

## Capabilities

### New Capabilities
- `theming`: resolución y aplicación de la identidad de marca (colores, tipografías,
  logos, nombre y textos) por instancia, en tiempo de ejecución, desde una única
  fuente de verdad.

## Impact

- Afecta: `site/index.html`, `site/assets/styles.css`, `site/assets/app.js`,
  `site/api/*.php` (textos de marca), nuevos `site/assets/theme.<instancia>.*`.
- Riesgo de regresión visual: se mitiga con capturas antes/después en ambas marcas.
- Beneficio: una sola rama, fin de los forks divergentes, rebrand en un archivo.
