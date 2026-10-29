"""Genera /home/claude/ies-training/ilustraciones/grandstream/manifest-ivr-anuncio.json (IVR que solo anuncia, id 20).

No pisa los otros manifests: enriquecer.py combina todos los manifest*.json por campo, y este solo trae la 20.
Las anclas ("after") salen del laboratorio de class/20-ivr-que-solo-anuncia/card.md y de teoria_md de acá.
"""
import json
from pathlib import Path

OUT = Path("/home/claude/ies-training/ilustraciones/grandstream/manifest-ivr-anuncio.json")

teoria = """### Un poco de historia

El IVR nació con el teclado. Cuando Bell presentó el Touch-Tone al público, el 18 de noviembre de 1963, cada tecla pasó a sonar como dos tonos a la vez, uno de un grupo bajo (697 a 941 Hz) y otro de un grupo alto (1209 a 1633 Hz); la norma de hoy es la UIT-T Q.23. Como viajan por el mismo canal que la voz, la norma les pone límites estrictos de duración, espacio entre dígitos, desvío de frecuencia y diferencia de nivel entre los dos (el twist): son los filtros que usa el detector para no confundir una voz con una tecla.

Igual se equivoca. En telecomunicaciones se llama falsing a un decodificador que detecta una señal que nadie mandó, y talk-off al caso en que la voz pega justo en la frecuencia del detector. Con SIP casi desaparece: el teléfono manda la tecla como evento RFC 4733 (2006). En una línea analógica de Antel, en cambio, no hay eventos: el FXO de la UCM sigue escuchando tonos en el audio.

### Cómo funciona

La UCM está basada en Asterisk 16, y su IVR se parece al Background() de Asterisk: reproduce el Prompt y, mientras suena, escucha teclas. Si llega un dígito, lo busca: primero entre las teclas de Key Pressing Events y, si Dial Other Extensions está prendido, entre los internos y grupos permitidos, esperando el Digit Timeout (3 s de fábrica) por si vienen más. Lo que no encuentra va a i, el inválido: suena el Invalid Input Prompt y se repite hasta Invalid Input Prompt Repeats (3 de fábrica). Si no llega nada, después del Response Timeout (10 s de fábrica) va a t: suena el Response Timeout Prompt y se repite hasta su propio Repeats. Al terminar las vueltas, la llamada va al destino de Invalid o de Timeout; si no hay destino, corta.

En una línea analógica, el dígito puede no ser de nadie. El detector del FXO mira el audio que llega por el par, con el eco de la propia bienvenida y el ruido de la línea, y si algo pasa todos sus filtros entrega un 5 que nadie marcó. Con marcar internos prendido y ninguna tecla, ese 5 se vuelve "buscá el interno 5": no existe, aviso de inválido y otra vuelta.

Por eso la receta tiene dos partes. En el IVR: marcar internos apagado, Timeout al grupo, repeticiones en 1 y un Response Timeout corto, así la llamada no depende del detector. En la línea: impedancia, ganancias y eco, que es donde nace el dígito falso. Con Announcement, la bienvenida directamente no escucha teclas."""

m = {"20": {
    "fig": {"file": "20.svg",
            "alt": "Arriba, la línea de Antel por el FXO1 de una UCM6304A entra al IVR 7000, que solo pasa la bienvenida, y de ahí al Ring Group 6000 con las internas 1001 y 1002. Debajo, la línea de tiempo de la llamada: bienvenida completa, silencio del Response Timeout y suena el grupo. Abajo a la izquierda, la configuración del IVR en Basic Call Features > IVR: Dial Other Extensions sin nada seleccionado, Response Timeout de 2 segundos, Response Timeout Prompt un audio de silencio, Response Timeout Prompt Repeats e Invalid Input Prompt Repeats en 1, y Timeout e Invalid al Ring Group 6000. A la derecha, en rojo: Lo siento, no lo entiendo es el aviso de opción inválida, porque al IVR le llegó un dígito que no es tecla ni interno, a veces un DTMF falso de la línea analógica. Debajo, en azul: si el firmware tiene Advanced Call Features > Announcement, el audio no se saltea, pasa solo al destino y no espera teclas.",
            "caption": "Bienvenida, un momento de silencio y el grupo: sin teclas, sin marcar internos y con las repeticiones en 1."},
    "anims": [{"file": "20-r1.svg",
               "alt": "Animación en cuatro tiempos. Arriba, la línea de Antel por el FXO1, el IVR 7000 y el Ring Group 6000 con las internas 1001 y 1002; abajo, dos líneas de tiempo de 0 a 60 segundos de ejemplo, antes y después del arreglo. 1: antes, con Dial Other Extensions en Extension y Ring Group y ninguna tecla, suena la bienvenida de 12 segundos y el FXO toma ruido o eco de la línea por un 5. 2: el IVR espera más dígitos durante el Digit Timeout de 3 segundos, busca el interno 5, no existe y suena el aviso de opción inválida, Lo siento, no lo entiendo. 3: con Invalid Input Prompt Repeats en 3, saludo y aviso vuelven dos veces más y el grupo suena recién a los 54 segundos, por el destino Invalid. 4: después, con marcar internos apagado, Response Timeout de 2 segundos y repeticiones en 1, suena la bienvenida, 2 segundos de silencio y el grupo a los 14 segundos, por el destino de Timeout.",
               "caption": "Antes, un 5 falso y tres vueltas de aviso; después, bienvenida, silencio y grupo."}],
    "steps": [
        {"file": "20-paso2.svg", "step": 2, "after": "Armá el IVR con el error del caso",
         "alt": "A la izquierda, el IVR 7000 como estaba, en Basic Call Features > IVR: Dial Other Extensions en Extension y Ring Group, resaltado, Digit Timeout 3, Response Timeout 10, Response Timeout Prompt Repeats 3 e Invalid Input Prompt Repeats 3. A la derecha, Key Pressing Events en Standard Key Event: ninguna tecla de 0 a 9, una fila de tecla * con Select an Option, resaltada, y Timeout e Invalid al Ring Group 6000. Debajo, tres tarjetas en rojo: 1, marcar internos prendido, el IVR queda esperando que el que llama disque un número; 2, ninguna tecla numerada, un dígito solo puede ser un interno y si no existe es inválido; 3, repeticiones en 3, saludo y aviso pueden sonar hasta tres veces antes del grupo. Abajo, en ámbar: la fila * con Select an Option no estaba guardada, era una fila nueva abierta en el formulario; una tecla sin destino no se guarda y se quita con el ícono menos.",
         "caption": "Marcar internos prendido, ninguna tecla y repeticiones en 3: las tres cosas que se juntaron en el caso."},
        {"file": "20-l1.svg", "step": 3, "after": "Simulá el DTMF falso",
         "alt": "Animación en cuatro tiempos con tres columnas: la interna 1001 en el banco, el IVR 7000 y el FXO1 con la línea en la obra; a la derecha, lo que hace el IVR. 1: en el banco, marcás 5 en la 1001 durante la bienvenida y la tecla viaja como evento RFC 4733 hasta el IVR. 2: en la obra, el 5 lo inventa el detector del FXO: ruido o eco de la línea que parece la mezcla de 770 y 1336 hercios, los tonos de la tecla 5, y el FXO se lo pasa al IVR. 3: con Dial Other Extensions en Extension y Ring Group, el IVR guarda el 5 y espera más dígitos durante el Digit Timeout de 3 segundos. 4: busca el interno 5, no existe, y le manda a quien llama el Invalid Input Prompt, Lo siento, no lo entiendo; con repeticiones en 3, es la vuelta 1 de 3. Abajo: en el banco el 5 lo marcás vos y en la obra lo inventa la línea, pero el IVR no distingue uno del otro.",
         "caption": "Lo que pasa en este paso: el 5 que marcás hace lo mismo que el falso de la línea, Digit Timeout, interno que no existe y aviso de inválido."},
        {"file": "20-paso5.svg", "step": 5, "after": "Aplicá la receta en el mismo IVR",
         "alt": "Tabla con tres columnas, campo, antes y después, con la columna después resaltada en verde. Dial Other Extensions: de Extension y Ring Group a nada seleccionado. Response Timeout: de 10, el de fábrica, a 2 segundos. Response Timeout Prompt: del de fábrica a un audio de silencio subido en Custom Prompt. Response Timeout Prompt Repeats: de 3 a 1. Invalid Input Prompt Repeats: de 3 a 1. Timeout e Invalid: Ring Group 6000, igual. Tecla * sin destino: de fila abierta a quitada con el ícono menos. Abajo, en verde: más adelante, 1 ventas y 2 administración van como teclas en Key Pressing Events y marcar internos sigue apagado. A la derecha: marcar internos sirve para que el que llama disque un interno directo; si un día se prende, con lista blanca.",
         "caption": "La receta en una tabla: marcar internos apagado, silencio corto, repeticiones en 1 y ninguna tecla sin destino."},
        {"file": "20-l2.svg", "step": 7, "after": "Compará en el CDR el Call Time",
         "alt": "Animación en cuatro tiempos con dos registros del CDR de la UCM, con las columnas Status, Call From, Call To, Action Type, Start Time y Call Time, y debajo dos barras de 0 a 60 segundos de ejemplo. 1: la llamada de prueba con el error, de la 1001 al IVR 7000, en la que se cuelga apenas suena la 1002, queda en el CDR como Answered, Action Type IVR. 2: su Call Time es 00:00:56; la barra muestra de qué está hecho: tres vueltas de bienvenida de 12 segundos, 3 segundos de Digit Timeout y el aviso de inválido, y recién ahí suena el grupo. 3: con la receta aplicada, la misma prueba queda con Call Time 00:00:15. 4: la barra nueva es la bienvenida, 2 segundos de silencio por el Response Timeout y el timbre: 41 segundos menos de espera. Colgando apenas suena la 1002, el Call Time es casi entero el tiempo que pasó en el IVR; se busca en CDR > CDR filtrando por la 1001.",
         "caption": "Lo que pasa en este paso: colgando apenas suena el grupo, el Call Time del CDR mide cuánto esperó el que llamó en el IVR."},
        {"file": "20-paso8.svg", "step": 8, "after": "armá el mismo recorrido",
         "alt": "Dos tarjetas. A la izquierda, IVR 7000 en Basic Call Features > IVR: escucha teclas mientras suena la bienvenida, en ámbar; tiene Response Timeout, repeticiones, Timeout e Invalid; admite teclas por horario si después piden opciones; con la receta del paso 5 deriva limpio. A la derecha, en verde, Announcement en Advanced Call Features > Announcement: un audio que no se puede saltear; se configura con Name, Prompt y Default Destination; se elige como destino de una ruta entrante; no espera teclas, así que un DTMF falso no lo cambia. Abajo, el recorrido: ruta entrante de la troncal de la línea, Announcement con la bienvenida y Ring Group 6000 con las internas 1001 y 1002. Nota: Announcement figura en el manual del UCM630x y del UCM630xA vigentes; en firmwares viejos puede no estar.",
         "caption": "Para un saludo sin opciones, Announcement no escucha teclas; el IVR conviene si después vienen opciones."},
    ],
    "concepts": [
        {"name": "IVR sin menú",
         "para_que": "Mucho cliente no quiere un menú: quiere que el que llama escuche un saludo y que después suene el grupo. Un IVR sin teclas resuelve eso con lo que la UCM ya trae, y deja la puerta abierta para sumar opciones más adelante.",
         "como": "En Basic Call Features > IVR, el Prompt es la bienvenida y Key Pressing Events queda sin teclas numeradas. Lo que hace funcionar la derivación es el destino de Timeout: cuando termina el audio, el IVR espera el Response Timeout y, si nadie marcó nada, manda la llamada ahí. Con Response Timeout corto y repeticiones en 1, el que llama escucha el saludo una vez y le suena el grupo.",
         "ejemplo": "Una óptica en el Centro quiere que se escuche el horario y la dirección antes de atender. IVR 7000 con esa bienvenida, Response Timeout de 2 segundos, Timeout al Ring Group 6000 del mostrador y repeticiones en 1: el que llama escucha el audio entero y en un par de segundos suena el mostrador."},
        {"name": "Marcar internos desde el IVR",
         "para_que": "Dial Other Extensions existe para que el que conoce el interno lo marque directo, sin pasar por el menú. Es cómodo en una oficina con muchos internos, pero cambia cómo el IVR trata cualquier dígito que llega.",
         "como": "En la sección Dialed Number se eligen los destinos que el que llama puede discar (Extension, Ring Group, Call Queue y otros). Prendido, el IVR toma cada dígito como el comienzo de un número y espera el Digit Timeout, 3 segundos de fábrica, por si vienen más; si el número no existe, va a Invalid. Las teclas numeradas de Key Pressing Events funcionan con la opción apagada, y si se prende conviene la lista blanca (lección IVR con horario).",
         "ejemplo": "Un estudio contable en Pocitos tiene un IVR con 1 administración y 2 contadores. Nadie marca internos de memoria, así que Dial Other Extensions queda apagado: un dígito que no es 1 ni 2 cae en Invalid y no queda esperando un número que nadie va a terminar de marcar."},
        {"name": "DTMF falso en la línea analógica",
         "para_que": "En una línea de cobre no hay eventos de teclas: los tonos viajan dentro del audio y el FXO los tiene que reconocer. El detector filtra por frecuencia, duración y nivel para no confundir voz con teclas, pero con eco, ruido o niveles altos a veces entrega un dígito que nadie marcó.",
         "como": "El síntoma es un IVR que reacciona solo: aviso de inválido sin que nadie toque nada, o una opción que se elige sola. Primero se saca al IVR de la dependencia del detector (marcar internos apagado, repeticiones en 1, Announcement si se puede). Después se ataca la línea: grabarla con Maintenance > Signaling Troubleshooting > Analog Record Trace y revisar impedancia (ACIM), ganancias y cancelador de eco, como en la lección Identificador y audio.",
         "ejemplo": "En una panadería del Prado, el IVR de la línea analógica sonaba con el aviso de inválido al final de la bienvenida. La grabación del FXO mostraba el eco de la propia bienvenida volviendo fuerte por la línea; con la ganancia de recepción más baja y el IVR sin marcar internos, el aviso desapareció."},
        {"name": "Announcement",
         "para_que": "Es la función de la UCM pensada justo para \"bienvenida y al destino\": un audio que el que llama no puede saltear y que, al terminar, pasa la llamada sola. No escucha teclas, así que un dígito falso no le cambia nada.",
         "como": "En Advanced Call Features > Announcement se crea con Name, Prompt (un audio subido, uno existente o uno generado por texto) y Default Destination: extensión, grupo, cola, IVR, buzón o número externo, con Call Privileges si es externo. Después se elige como destino de la ruta entrante. No es lo mismo que Announcement Paging ni que Announcement Center.",
         "ejemplo": "Una farmacia en Paso Molino solo quiere que se escuche el aviso de turno y que suene el mostrador. Ruta entrante de la línea al Announcement \"turno\" y de ahí al Ring Group 6000: si un día piden opciones, se cambia el destino de la ruta a un IVR."},
    ],
    "teoria_md": teoria,
    "teoria_figs": [{"file": "20-t1.svg", "after": "entrega un 5 que nadie marcó",
                     "alt": "Animación en cuatro tiempos. A la izquierda, el teclado DTMF con las frecuencias de cada fila, 697, 770, 852 y 941 hercios, y de cada columna, 1209, 1336 y 1477; al medio, el detector DTMF del FXO con tres filtros: un tono de cada grupo, que dure lo suficiente y niveles parecidos, el twist; a la derecha, lo que le pasa al IVR 7000. 1: entra la tecla 5 de verdad, 770 y 1336 hercios a la vez; pasa los tres filtros y el IVR recibe un 5. 2: entra voz o música; tiene algo de 770 pero dura poco y falla un filtro: no hay dígito. 3: entra eco o ruido parecido al par de la tecla 5 y pasa todos los filtros: el IVR recibe un 5 que nadie marcó; eso es falsing, y talk-off cuando es la voz. 4: por SIP, la tecla llega como evento RFC 4733 dentro del RTP y no pasa por ningún detector: el evento ya dice qué tecla fue. En la línea analógica no hay eventos y el FXO decide con el audio.",
                     "caption": "El FXO busca el par de tonos en el audio: la tecla de verdad pasa, la voz casi nunca y a veces el ruido sí."}],
}}

# controles: anclas y largo de los alt
card = Path("/home/claude/claudemy/grandstream/class/20-ivr-que-solo-anuncia/card.md").read_text(encoding="utf-8")
lab = card.split("**Laboratorio**", 1)[1].split("**Regla para quedarse**", 1)[0]
plain, fence = [], False
for ln in lab.splitlines():
    if ln.strip().startswith("```"):
        fence = not fence
        continue
    if not fence:
        plain.append(ln)
plain = "\n".join(plain)
for st in m["20"]["steps"]:
    assert plain.count(st["after"]) == 1, st["after"]
    assert len(st["alt"]) <= 1000, (st["file"], len(st["alt"]))
for tf in m["20"]["teoria_figs"]:
    assert teoria.count(tf["after"]) == 1, tf["after"]
words = len(teoria.split())
assert 250 <= words <= 450, words
assert "—" not in json.dumps(m, ensure_ascii=False) and "–" not in json.dumps(m, ensure_ascii=False)
OUT.write_text(json.dumps(m, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"ok {OUT.name}: teoria {words} palabras, {len(m['20']['steps'])} pasos, {len(m['20']['concepts'])} conceptos")
