# Guía: enriquecer lecciones de IES Training (ilustraciones + reflexión de conceptos)

Nico (dueño de IES) pidió dos cosas para cada lección:
1. **Imágenes ilustrativas que ayuden a entender cada concepto y cada paso concreto.** Ejemplo textual de su pedido: "cuando dice *Conectá la notebook a ether2*, creá una ilustración que ayude al alumno a entender". O sea: dibujar lo que el técnico tiene que hacer o ver (qué cable va a qué puerto, qué menú abrir, qué pasa con el tráfico, qué borne va con cuál), no ilustraciones decorativas.
2. **Una reflexión de cada concepto: para qué se creó, cómo se usa, con ejemplos claros.** Cada concepto importante de la lección (Safe Mode, cadena input, address-list, relé NO/NC, DTMF, SIP, alta seguridad HTTP, etc.) se explica con: el problema que vino a resolver, cómo se usa en la práctica y un ejemplo concreto de obra o de soporte en Uruguay.

## Qué producir por lección

Carpeta de salida: `/home/claude/ies-training/ilustraciones/<slug>/` (slug: `akuvox`, `mikrotik`, …).

### Ilustraciones (SVG generados con la biblioteca)
- **Una ilustración principal** de la lección: `<id>.svg` (el concepto central, en una imagen). Va arriba de todo en la pestaña Resumen.
- **De 1 a 3 ilustraciones de pasos** del laboratorio: `<id>-paso<N>.svg`, donde N es el número del paso del laboratorio que ilustra (el número tiene que coincidir con el paso). Elegí los pasos donde una imagen ayuda de verdad: conexiones físicas (qué cable a qué puerto o borne), dónde está una opción en el menú, qué pasa en la red, antes y después. No ilustres "abrí la terminal".
- `<id>` es el id de la lección (para estos cursos, el número sin ceros: `1`, `13`, `41`).
- Escribí un script Python por lección en `/home/claude/ies-training/ilustraciones/<slug>/src/<id>.py` que use la biblioteca `ilus.py` y guarde los SVG. Así se pueden corregir y regenerar.
- Renderizá cada SVG y **miralo** antes de darlo por bueno:
  `python3 /home/claude/ies-training/tools/render_svg.py /home/claude/ies-training/ilustraciones/<slug>/<id>.svg ...`
  Deja un `.png` al lado del SVG: abrilo con Read y revisá textos cortados, superposiciones, flechas que no llegan, etiquetas tapadas, cosas fuera del lienzo. Corregí y volvé a renderizar hasta que esté limpio.
- Ejemplos de referencia (miralos primero, script + png): `/home/claude/ies-training/ilustraciones/_ejemplos/mikrotik-1-paso1.py` y `/home/claude/ies-training/ilustraciones/mikrotik/4.svg` (hecho a mano; también se puede escribir SVG a mano si el diagrama lo pide, con el mismo estilo).

### Reglas de contenido de las imágenes
- Exactitud técnica: todo lo que dibujás sale de la tarjeta de la lección (`card.md`) o de las notas de investigación del curso (`research/notes/*.md`, `raw/web/*`). Mismos nombres de puertos, menús, comandos, IPs de ejemplo, bornes. Nada inventado. Si dudás de un detalle (posición exacta de un borne en un modelo), dibujalo genérico y etiquetado ("borne del relé A") en vez de inventar.
- Español rioplatense, voseo, frases cortas. Título de la imagen: una acción o una pregunta clara (máximo ~55 caracteres para que entre en una línea).
- Nada de logos, marcas ni copias de fotos de productos. Equipos genéricos dibujados con la biblioteca; el modelo va como texto.
- Colores con significado: verde = correcto/permitido, ámbar = atención, rojo = peligro/bloqueado, siempre con texto que lo diga. Cables según la biblioteca (datos azul, alimentación rojo/negro, relé cian, lógico punteado).
- Legibilidad: texto mínimo 15 px, no más de ~6 elementos principales por imagen, aire entre bloques. Mejor dos imágenes simples que una recargada.
- IPs y datos de ejemplo: los mismos de la tarjeta; si no hay, usá rangos de documentación (192.168.88.x de fábrica MikroTik, 192.0.2.x, 203.0.113.x, 198.51.100.x).

### Reflexión de conceptos + metadatos: `manifest.json`
Un único `manifest.json` por curso en la carpeta del slug, con una entrada por lección que hayas trabajado (si el archivo ya existe porque otro agente trabaja en el mismo curso, **no lo pises**: escribí el tuyo como `manifest-<desde>-<hasta>.json`, ej. `manifest-13-28.json`).

```json
{
  "13": {
    "fig": {"file": "13.svg", "alt": "Descripción de lo que muestra la imagen para quien no la ve", "caption": "Una línea que dice qué mirar en la imagen."},
    "steps": [
      {"file": "13-paso4.svg", "step": 4, "alt": "...", "caption": "...", "after": "texto exacto, copiado de una línea del paso 4 del laboratorio en card.md"}
    ],
    "concepts": [
      {
        "name": "Open Relay via HTTP",
        "para_que": "Para qué se creó: el problema que resuelve, en 2 o 3 oraciones.",
        "como": "Cómo se usa en la práctica: dónde se activa, qué se configura, qué cuidar. 2 a 4 oraciones.",
        "ejemplo": "Un ejemplo concreto y claro de obra o soporte (edificio en Pocitos, barrera de un estacionamiento, NVR que abre al detectar una matrícula). Puede incluir un comando corto entre `backticks`."
      }
    ]
  }
}
```
- `teoria_md` (nuevo, pedido por Nico: "cada lección debe tener un poco de Historia / Teoría"): texto en Markdown, 250 a 450 palabras, con dos subtítulos exactos `### Un poco de historia` y `### Cómo funciona`. Historia: de dónde sale la tecnología, el estándar o la función (quién la creó, cuándo, qué problema había antes, cómo evolucionó hasta la versión actual), solo con fechas y datos que estén en las fuentes leídas o que sean conocimiento técnico estable y verificable (por ejemplo: SIP es RFC 3261 de 2002; 802.1Q de 1998; WireGuard entró al kernel Linux 5.6 en 2020; RouterOS 7 salió estable en 2021). Teoría: cómo funciona por dentro (el protocolo, el flujo, los estados), al nivel de un técnico que quiere entender el porqué de los pasos del laboratorio. Párrafos cortos, ejemplos concretos, `código` donde ayude. Nada inventado: si no tenés una fecha confiable, contá la historia sin fecha.
- `concepts`: de 2 a 4 por lección, los conceptos que un técnico nuevo necesita entender de verdad para hacer el laboratorio. No repitas la "idea en tres líneas": profundizá en el porqué y el cómo. Tono: un técnico con experiencia explicándole a uno nuevo, cálido y directo, sin exigencias ("conviene", "probá", no "tenés que"). Sin guiones largos (— –).
- `after`: el texto tiene que existir tal cual en una línea del laboratorio de `card.md` (la imagen se inserta justo después de ese paso). Copiá un fragmento de 15 a 40 caracteres que sea único en el laboratorio y que no esté dentro de un bloque de código.
- `caption` y `alt` en español, sin markdown.

## Qué NO tocar
- No edites `card.md`, `quiz.json`, `script.txt` ni `course.json`: el contenido nuevo va solo en `ilustraciones/`. El orquestador lo combina con la versión publicada del curso.
- No despliegues ni subas nada al servidor.

## Script para automatizar lo aprendido (cursos con terminal: MikroTik primero)
Pedido de Nico: "Al final de cada lección debemos tener un script para automatizar lo aprendido (crear usuario, crear bridge con IPs de forma segura, etc.), para pegarlo en la terminal de MikroTik y tener la configuración deseada".
En la entrada de cada lección del manifest agregá el campo `script_rsc`:
```json
"script_rsc": {
  "titulo": "Crear un usuario por técnico y deshabilitar admin",
  "descripcion": "Qué deja configurado el script, en 1 o 2 oraciones.",
  "variables": [
    {"nombre": "USUARIO", "valor": "tecnico1", "detalle": "Nombre del usuario nuevo"},
    {"nombre": "LAN_IP", "valor": "192.168.88.1/24", "detalle": "IP y máscara del router en la LAN"}
  ],
  "codigo": "# IES Training · MikroTik · <título>\n# Probalo primero en un equipo de banco y en Safe Mode (Ctrl+X).\n:local usuario \"{{USUARIO}}\"\n...",
  "notas": ["Qué revisar después de pegarlo", "Qué no hace el script"]
}
```
Reglas del script:
- RouterOS 7, sintaxis exacta de la versión vigente, comandos con la forma `/ip/address/add …` como en las lecciones. Solo lo que la lección enseña (no inventar funciones).
- **Variables**: arriba del script, como `{{NOMBRE}}` (el portal muestra un formulario para completarlas y reemplaza las marcas antes de copiar). Valores por defecto de laboratorio (192.168.88.x, rangos de documentación). Nada de claves reales: para contraseñas usá una variable `{{CLAVE}}` con valor de ejemplo claramente falso y una nota de cambiarla.
- **Idempotente y seguro**: que se pueda pegar dos veces sin duplicar (`:if ([:len [/interface/bridge/find name=$nombre]] = 0) do={ … }`, o `find` + `set`), con `comment="ies-<algo>"` en lo que crea para encontrarlo después, y sin cortar el acceso de quien lo pega (por ejemplo, no deshabilitar admin si no existe otro usuario full, no sacar del bridge el puerto por donde se entra sin avisar). Si un paso es riesgoso, que el script lo deje comentado con `#` y una explicación.
- Comentarios en español rioplatense, cortos. Al final, un `:put "Listo: …"` con lo que quedó hecho y un comando de verificación sugerido.
- 15 a 60 líneas. Si la lección es conceptual (por ejemplo elegir canal de actualización), el script puede ser de diagnóstico o verificación (imprimir estado, comparar versiones) en vez de configurar.

## Ilustraciones y animaciones de la Teoría (pedido de Nico, octubre 2026)
"La teoría también debe tener ilustraciones y animaciones." Cada lección lleva **1 o 2 figuras dentro de la pestaña Teoría**, insertadas después del párrafo que explican. Al menos una por lección es una **animación** cuando la teoría describe algo que pasa en el tiempo (un paquete que viaja, un intercambio de mensajes, un cambio de estado, un antes y después, una secuencia de pasos de un protocolo). Si el concepto es estructural (capas, una tabla, una jerarquía), una ilustración fija alcanza.

**Qué dibujar:** el mecanismo de "Cómo funciona", no una repetición de la ilustración principal ni de los pasos del laboratorio. Ejemplos: el intercambio INVITE → 100 → 180 → 200 → ACK de SIP; el DORA de DHCP; un paquete que entra por input o por forward; la RIB que elige y la FIB que reenvía; el DTMF por RFC 4733 contra SIP INFO; el relé que se energiza y la cerradura que libera; la cadena de NAT de ida y vuelta; el timeline de Safe Mode.

**Animaciones:** con la biblioteca `/home/claude/ies-training/tools/anim.py` (leé su docstring). Ejemplo completo y de referencia: `/home/claude/ies-training/ilustraciones/mikrotik/src/anim_27_rib_fib.py` y su resultado `site2/ilustraciones/mikrotik/27-rib-fib.svg`.
- SVG animado con CSS, sin scripts, fuentes embebidas (lo hace la biblioteca), ciclo de 12 a 30 s, 3 a 5 tiempos con la leyenda numerada (`a.steps(...)`), texto mínimo 15 px, mismos colores con significado.
- Se guarda directo en `/home/claude/ies-training/site2/ilustraciones/<slug>/<id>-t<N>.svg` (no pasa por render_svg). Script en `ilustraciones/<slug>/src/anim_<id>_<tema>.py`.
- Revisión obligatoria: `a.write(..., preview=[…porcentajes…])` deja un PNG por instante y el cuadro fijo (`-fijo.png`, el de "reducir movimiento"). Miralos todos con Read: nada superpuesto, nada cortado, el cuadro fijo tiene que entenderse solo. Borrá los PNG de vista previa del sitio si quedaron en `site2/` (deben quedar en `ilustraciones/<slug>/`).
- Peso: menos de 120 KB por animación.

**Ilustraciones fijas de teoría:** igual que las demás (ilus.py, render_svg.py), con nombre `<id>-t<N>.svg` → `site2/ilustraciones/<slug>/<id>-t<N>.webp`.

**En el manifest**, campo `teoria_figs` en la entrada de la lección:
```json
"teoria_figs": [
  {"file": "27-t1.svg", "after": "texto exacto de un párrafo de teoria_md", "alt": "descripción completa, incluido lo que pasa en cada tiempo", "caption": "Una línea: qué mirar en la animación."},
  {"file": "27-t2.webp", "after": "…", "alt": "…", "caption": "…"}
]
```
- `file`: el nombre tal cual está en `site2/ilustraciones/<slug>/` (`.svg` animada o `.webp` fija).
- `after`: un fragmento de 15 a 60 caracteres que exista una sola vez en `teoria_md` (de esa lección, en el manifest) y que esté dentro del párrafo después del cual va la figura. Nunca dentro de un título `###`.
- Si la entrada de la lección está en otro manifest, podés escribir el tuyo aparte (`manifest-teoria-<desde>-<hasta>.json`): los manifests se combinan por campo.

**Vista previa confiable (corrección del 27/10):** pausar las animaciones por JavaScript a veces deja pintado un cuadro viejo. `anim.py` ya saca cada cuadro fijando el instante por CSS en una página nueva. Para revisar animaciones ya generadas: `python3 /home/claude/ies-training/tools/anim_preview.py <svg> [más] --pct 10,35,60,85` (deja `_rev-<nombre>-<pct>.png` y `-fijo.png` en `ilustraciones/<slug>/`). Además, `a.group(...)` con solo movimiento ahora se ve mientras corre aunque `still=0`.
