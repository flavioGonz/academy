# Lección 20. IVR que solo anuncia

**Escuchá:** ivr-que-solo-anuncia.mp3 (2 min)

**La idea, en tres líneas**
- Un IVR que solo pasa la bienvenida y deriva no lleva teclas ni marcar internos (Dial Other Extensions): el destino de Timeout es el grupo y las dos repeticiones quedan en 1.
- "Lo siento, no lo entiendo" es el aviso de opción inválida: al IVR le llegó un dígito que no es tecla ni interno, y en una línea analógica puede ser un DTMF falso que nadie marcó.
- Si el firmware tiene Advanced Call Features > Announcement, ese audio no se puede saltear y pasa solo al destino: es la herramienta más directa para "bienvenida y al grupo".

**Impacto:** el que llama escucha el saludo una vez y en segundos le suena el grupo, sin avisos raros ni tres vueltas de menú.

**Quién lo dice:** 4 de 4 fuentes oficiales (los manuales del UCM630x y del UCM630xA, la guía de IVR de Grandstream y la documentación de Asterisk) coinciden en que el IVR repite el aviso y después va al destino de Timeout o de Invalid, o corta; 3 casos de foro muestran FXO que detectan dígitos de más o de menos; ninguna fuente dice qué hace la UCM con un dígito cuando el IVR no tiene teclas, así que eso sale del caso real.

**Laboratorio** · Foco · 20 min
En una UCM de banco con una interna para llamar (1001) y el Ring Group 6000 con otra interna (1002). Si tenés una línea por FXO, mejor todavía: apuntá su ruta entrante al 7000 (lección Hasta que suene).
1. Subí la bienvenida y un audio de silencio de un segundo en PBX Settings > Voice Prompt > Custom Prompt (WAV PCM de 16 bits, mono, 8000 Hz, o MP3). El silencio lo podés generar así:
```bash
ffmpeg -f lavfi -i anullsrc=r=8000:cl=mono -t 1 -c:a pcm_s16le silencio.wav
```
2. Armá el IVR con el error del caso:
```text
Basic Call Features > IVR > Add
Name: bienvenida   Extension: 7000   Prompt: (tu bienvenida)
Dialed Number > Dial Other Extensions: Extension, Ring Group
Response Timeout Prompt Repeats: 3   Invalid Input Prompt Repeats: 3
Key Pressing Events: ninguna tecla numerada
  Timeout: Ring Group 6000   Invalid: Ring Group 6000
```
3. Simulá el DTMF falso: llamá al 7000 desde la 1001 y marcá un 5 mientras suena la bienvenida. El IVR espera más dígitos (Digit Timeout, 3 s de fábrica), busca un interno 5, no existe y suena el aviso de opción inválida; con 3 repeticiones, vuelve todo. Colgá apenas suene la 1002.
4. Mirá esa llamada en CDR > CDR: Action Type IVR, y como colgaste apenas sonó el grupo, su Call Time es casi entero el tiempo que el que llamó pasó en el IVR.
5. Aplicá la receta en el mismo IVR:
```text
Dial Other Extensions: nada seleccionado
Response Timeout (s): 2        (de fábrica 10: es el silencio después del audio)
Response Timeout Prompt: silencio   Response Timeout Prompt Repeats: 1
Invalid Input Prompt Repeats: 1
Timeout: Ring Group 6000   Invalid: Ring Group 6000   (sin cambios)
```
Si en Key Pressing Events quedó una fila abierta sin destino (por ejemplo una tecla * con "Select an Option"), sacala con el ícono (-): una tecla sin destino no se guarda. En firmwares anteriores marcar internos eran casillas sueltas (como Dial Trunk, que hoy es Dial External Number dentro de Dial Other Extensions): apagalas todas.
6. Repetí la llamada sin marcar nada y colgá cuando suene la 1002: bienvenida completa, un momento de silencio y suena el grupo. Después repetila marcando el 5 y anotá qué hace tu firmware: lo ignora, o suena una vez el aviso y pasa al grupo por Invalid. Las dos dejan atrás las tres vueltas.
7. Compará en el CDR el Call Time de las dos llamadas: el de ahora tiene que ser la bienvenida, el Response Timeout y poco más.
8. Si tu firmware tiene Advanced Call Features > Announcement, armá el mismo recorrido (Name, Prompt, Default Destination: Ring Group 6000), apuntale una ruta entrante de prueba y medí igual en el CDR: el audio no se saltea y no espera teclas.

Si después piden opciones (1 ventas, 2 administración), van como teclas en Key Pressing Events y marcar internos sigue apagado: esa opción es para discar un interno directo. Si con todo esto el aviso de inválido sigue apareciendo en la línea real, el dígito falso viene de la línea: grabala con Maintenance > Signaling Troubleshooting > Analog Record Trace y revisá eco, impedancia y ganancias (lección Identificador y audio).
⚠️ En la central de un cliente, cambiá el IVR fuera de hora y probá con una llamada real antes de irte: un IVR mal guardado deja la línea principal sin atender.

**Regla para quedarse**
Un IVR sin teclas no deja marcar internos: el silencio va al grupo, las repeticiones quedan en 1 y ninguna tecla queda sin destino.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Campos del IVR, Announcement y CDR en el UCM630xA: https://documentation.grandstream.com/knowledge-base/ucm630x-audio-series-user-manual/
- Guía de IVR de Grandstream (Dial Other Extensions, repeticiones, prompts): https://documentation.grandstream.com/knowledge-base/how-to-use-ivr/
- Las extensiones i y t de Asterisk, el motor de la UCM: https://docs.asterisk.org/Configuration/Dialplan/Special-Dialplan-Extensions/
- Un IVR por FXO que recibía dígitos al azar: https://issues-archive.asterisk.org/ASTERISK-22433
- Falsing y talk-off: https://en.wikipedia.org/wiki/Falsing
