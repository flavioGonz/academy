"""Genera /home/claude/ies-training/ilustraciones/grandstream/manifest-fxo.json (lecciones 13 a 18, líneas analógicas por FXO).

No pisa manifest.json ni manifest-teoria-1-12.json: enriquecer.py combina todos los manifest*.json por campo.
Al final verifica: cada 'after' de pasos existe una sola vez en el laboratorio de card.md (fuera de bloques de código),
cada 'after' de teoria_figs existe una sola vez en teoria_md, la teoría tiene 250 a 450 palabras con sus dos subtítulos,
cada archivo existe en site2/ilustraciones/grandstream/ y no hay guiones largos.
"""
import json
import re
from pathlib import Path

ROOT = Path("/home/claude/ies-training")
SITE = ROOT / "site2" / "ilustraciones" / "grandstream"
CLASS = Path("/home/claude/claudemy/grandstream/class")
M = {}

# =====================================================================================  13
M["13"] = {
    "fig": {"file": "13.svg",
            "alt": "A la izquierda, la central de Antel, que hace de FXS, unida por el par de cobre a la roseta RJ11; de la roseta, un cable RJ11 baja al FXO1 resaltado del UCM6304A, que tiene FXS 1 a 4, FXO 1 a 4, LAN y WAN y una leyenda: el FXO hace de teléfono, descuelga y cuelga. Del mismo par cuelgan en paralelo una alarma que reporta por la línea, un posnet que autoriza por la línea y un teléfono en otro ambiente. Arriba a la derecha, lo que da la línea: tensión en reposo, timbre cuando entra una llamada, tono de invitación a marcar al descolgar y el número del que llama si está contratado. Abajo, un aviso: Antel no publica tensiones ni frecuencias, se miden antes de enchufar.",
            "caption": "La línea de Antel da tensión, timbre y tono; el FXO de la UCM descuelga, y todo lo que cuelga del mismo par también."},
    "steps": [
        {"file": "13-paso1.svg", "step": 1, "after": "Anotá la tensión en reposo",
         "alt": "Frente de una ficha RJ11 con seis posiciones; las del medio, 3 y 4, en dorado y con las puntas roja y negra de un multímetro en V CC. A la derecha, dos tarjetas para anotar: reposo con todo colgado, con la referencia de las fuentes de 24 a 70 V y muchas líneas cerca de 48 V, y descolgado con el teléfono de prueba, que cae a entre 4 y 18 V según Sandman. Dos avisos: si en reposo ya da valores de descolgado, algo en paralelo tomó la línea; con la línea sonando hay unos 70 V de alterna.",
         "caption": "Se mide en los contactos 3 y 4, con la central desconectada: en reposo y con el teléfono de prueba descolgado."},
        {"file": "13-paso5.svg", "step": 5, "after": "Recorré el par y anotá todo",
         "alt": "La línea de Antel con cuatro equipos en paralelo resaltados en ámbar, cada uno con la etiqueta anotalo: panel de alarma que llama para reportar, posnet que autoriza por la línea, fax que puede atender solo y un teléfono olvidado en el depósito. Una nota dice que cualquiera puede tomar la línea sin avisar y otra, en verde, que para probar va una línea con un solo equipo.",
         "caption": "Alarma, posnet, fax y teléfonos en paralelo pueden tomar la línea: se anotan y, para probar, se desconectan."},
        {"file": "13-paso7.svg", "step": 7, "after": "Conectá la línea al FXO1 del UCM6304A",
         "alt": "La roseta de la línea 1 conectada con un cable RJ11 al FXO1 resaltado del UCM6304A. A la derecha, la web en System Status > Dashboard: en Interface Status el FXO 1 aparece gris, que quiere decir conectado y sin troncal, y los FXO 2 a 4 sin línea todavía. Abajo, una nota sobre el lifeline: con un corte de luz el FXS1 queda conectado al FXO1 y el FXS2 al FXO2.",
         "caption": "Con la línea enchufada y sin troncal, el FXO1 se ve gris en el Dashboard."},
    ],
    "concepts": [
        {"name": "FXS y FXO",
         "para_que": "Una línea analógica necesita un lado que alimente y otro que use. El FXS es el que da tensión, timbre y tono; el FXO es el que se comporta como un teléfono y solo descuelga y cuelga. Por eso se conectan siempre de a pares: FXS con FXO.",
         "como": "La línea que llega de Antel es un FXS, así que en la UCM va a un puerto FXO. Los FXS de la UCM son para teléfonos analógicos o un fax. Enchufar la línea de Antel en un FXS de la central no funciona y además enfrenta dos fuentes de tensión.",
         "ejemplo": "En una carnicería de La Teja hay dos líneas de Antel y un fax viejo: las dos líneas van al FXO1 y FXO2 del UCM6304A, y el fax a un FXS, con su propia extensión."},
        {"name": "Tensión en reposo y descolgado",
         "para_que": "La tensión del par dice en qué estado está la línea sin necesidad de la central: si hay tensión de reposo, la línea está libre; si cae a pocos voltios, alguien la tiene tomada. Es la forma más rápida de separar un problema de línea de uno de configuración.",
         "como": "Con el UCM desconectado, multímetro en continua sobre los contactos 3 y 4 de la ficha. Se anota el valor en reposo, se descuelga un teléfono de prueba y se anota el valor descolgado. Antel no publica cifras: las fuentes hablan de 24 a 70 V en reposo y de 4 a 18 V descolgado, según la distancia a la central.",
         "ejemplo": "La ficha de una línea en un comercio de Paso Molino dice reposo y descolgado con sus valores. Meses después el puerto aparece ocupado: medís, da valores de descolgado con la central desenchufada, y encontrás el posnet descolgado detrás del mostrador."},
        {"name": "Equipos en paralelo",
         "para_que": "En muchos comercios la misma línea de cobre alimenta la central, la alarma, el posnet y algún teléfono suelto. Cada uno de esos equipos puede descolgar por su cuenta, y la central no tiene forma de saberlo.",
         "como": "Antes de conectar, se recorre el par y se anota todo lo que cuelga de él. Para probar la línea se deja un solo equipo conectado. Sandman, que trabaja con alarmas, recomienda directamente no compartir la línea de un panel de incendio con la telefonía.",
         "ejemplo": "La alarma de un local en Cordón reporta a la empresa de monitoreo por la línea 2: cada vez que reporta, el FXO2 de la UCM ve la línea tomada y las llamadas de clientes dan ocupado."},
    ],
    "teoria_md": """### Un poco de historia

La telefonía analógica funciona igual desde hace décadas: dos hilos de cobre entre la central del proveedor y el teléfono del cliente, que llevan a la vez la alimentación, la señalización y la voz. La central mantiene tensión continua en el par; en los sistemas clásicos, negativa respecto de tierra, del orden de -48 V. Al descolgar, el teléfono cierra el lazo, circula corriente y la central sabe que alguien quiere marcar o atender.

Los nombres FXS y FXO vienen de "Foreign eXchange": el lado Subscriber (abonado) y el lado Office (central). Hoy los usan las centrales IP y los gateways para decir qué hace cada puerto. En Uruguay, Antel es la empresa estatal que todavía entrega muchas de estas líneas en cobre; desde agosto de 2010 los números del país tienen 8 cifras y no hay códigos de área.

### Cómo funciona

En reposo, el par tiene tensión continua y no circula corriente. Las fuentes dan valores distintos: Patton habla de unos 50 V, innovaphone de 24 a 70 V en la red pública y Sandman de unos 48 V. Antel no los publica, por eso se miden.

Cuando entra una llamada, la central suma una alterna para hacer sonar el timbre: unos 70 V, según innovaphone, en ráfagas. El FXO de la UCM detecta ese timbre como lo haría un teléfono.

Para atender, el FXO cierra el lazo: circula corriente y la tensión cae a pocos voltios, de 4 a 18 V según la distancia a la central (Sandman). Para hacer una llamada pasa lo mismo y la central responde con el tono de invitación a marcar, que en Uruguay es de 425 Hz continuo.

Todo lo que cuelga del mismo par ve lo mismo y puede hacer lo mismo. Una alarma que reporta, un posnet que autoriza o un teléfono descolgado cierran el lazo igual que la UCM, y para la central de Antel la línea queda ocupada.""",
    "teoria_figs": [
        {"file": "13-t1.svg", "after": "la tensión cae a pocos voltios, de 4 a 18 V",
         "alt": "Animación en cinco tiempos con la central de Antel, que hace de FXS, unida por el par de cobre al FXO1 de la UCM, y abajo un gráfico de la tensión en el par que se va dibujando. 1: en reposo, tensión continua. 2: entra una llamada y la central suma el timbre, una alterna de unos 70 V en ráfagas. 3: la UCM atiende, cierra el lazo, circula corriente y la tensión cae al nivel de descolgado. 4: al colgar, vuelve la tensión de reposo. 5: para salir, el FXO descuelga, la tensión cae y llega el tono de invitación a marcar de 425 Hz. Nota: Antel no publica sus valores; innovaphone habla de 24 a 70 V en reposo y Sandman de 4 a 18 V descolgado.",
         "caption": "Reposo, timbre, lazo cerrado, colgado y tono: lo que se ve en el par en cada momento."},
    ],
}

# =====================================================================================  14
M["14"] = {
    "fig": {"file": "14.svg",
            "alt": "Dos tarjetas. A la izquierda, en verde, una troncal por línea, para cuando cada línea entra a un lugar distinto: el FXO1 va a la troncal Antel_Linea1 y de ahí al grupo 6000 de atención; el FXO2 va a Antel_Linea2 y de ahí al fax, con su extensión; la ruta entrante se elige por troncal. A la derecha, varias FXO en una troncal, para líneas iguales: FXO1 en uso y FXO2 libre entran a Antel_Grupo; DAHDI Out Line Selection en Ascend toma la primera libre (de fábrica), Poll alterna 1, 2, 1, 2 y Descend arranca por la última; si el 1 está en uso, sale por el 2.",
            "caption": "Una troncal por línea si entran distinto; una troncal para varias FXO si son iguales y se quiere salir por la libre."},
    "steps": [
        {"file": "14-paso1.svg", "step": 1, "after": "Revisá el hardware analógico",
         "alt": "La web en PBX Settings > Interface Settings > Analog Hardware con FXO Opermode en el país de la línea, PCMA Override en PCMA (resaltado), Tone Region para los tonos del FXS y la detección de ACIM de los FXO, que se ve en la lección Identificador y audio. A la derecha, dos tarjetas: PCMA Override, según el manual PCMU para Norteamérica y PCMA para el resto del mundo, de fábrica PCMU; FXO Opermode, impedancia, umbral de timbre y corriente de lazo por país, de fábrica Estados Unidos. Abajo, un aviso: PCMA Override reinicia la central.",
         "caption": "Antes de las troncales: país de la línea en FXO Opermode y PCMA, con un reinicio coordinado."},
        {"file": "14-paso2.svg", "step": 2, "after": "Creá una troncal por línea",
         "alt": "Dos ventanas de Extension/Trunk > Analog Trunks > Create: una con FXO Port 1 y Trunk Name Antel_Linea1, la otra con FXO Port 2 y Antel_Linea2. A la derecha, un aviso de que el nombre sale en rutas, Dashboard, Active Calls y capturas, una nota verde de usar nombres sin el número real y otra de que, si las dos líneas van al mismo destino, alcanza una troncal con FXO 1 y 2 en Ascend.",
         "caption": "Una troncal por línea, con nombres que se pueden mostrar sin exponer el número."},
        {"file": "14-captura-dashboard.webp", "step": 3, "after": "Guardá y aplicá. En System Status",
         "alt": "Captura editada del Dashboard de un UCM6304A, recortada a Interface Status y Trunks. En Interface Status, USB, SD y WAN en gris, LAN en azul; FXS 1 a 4 en gris; FXO 1 en azul (libre), FXO 2 en naranja (en uso) y FXO 3 y 4 en gris. En Trunks, una troncal Antel_Linea1 con el punto azul de disponible, y el resumen Available 1, Busy 0, Abnormal 0.",
         "caption": "Captura editada de una UCM6304A: FXO1 libre en azul, FXO2 en uso en naranja, FXO3 y FXO4 grises."},
    ],
    "concepts": [
        {"name": "Troncal analógica",
         "para_que": "Las rutas de la UCM no hablan de puertos sino de troncales. La troncal analógica agrupa uno o más FXO bajo un nombre, y es lo que después eligen las rutas entrantes y salientes.",
         "como": "Se crea en Extension/Trunk > Analog Trunks, marcando los canales FXO y con un Trunk Name único. Conviene un nombre que se pueda mostrar en capturas (Antel_Linea1) y dejar el número real en la ficha de la línea. En Advanced Options quedan la detección, el identificador y las ganancias, que se ven en las lecciones siguientes.",
         "ejemplo": "En una ferretería del Cerro, las troncales Antel_Linea1 y Antel_Linea2 aparecen tal cual en el Dashboard y en las capturas que el técnico manda al soporte, sin exponer los números del cliente."},
        {"name": "DAHDI Out Line Selection",
         "para_que": "Cuando una troncal tiene varias líneas, la central necesita una regla para elegir por cuál sale cada llamada. Sin regla, dos llamadas podrían pelearse por el mismo puerto.",
         "como": "Ascend, el de fábrica, prueba siempre desde el puerto más bajo y toma el primero libre. Poll alterna entre puertos. Descend arranca por el último. Solo afecta a las salientes: para entrar, cada llamada llega por el puerto donde sonó.",
         "ejemplo": "Una inmobiliaria en Pocitos con dos líneas iguales usa Antel_Grupo en Ascend: todas las salidas usan la línea 1 y la 2 se usa solo cuando la 1 está ocupada, así la 2 queda casi siempre libre para entrar."},
        {"name": "Estados del FXO en el Dashboard",
         "para_que": "El Dashboard resume en colores qué ve la central en cada puerto, sin abrir la configuración. Es lo primero que se mira cuando un cliente dice que la línea no anda.",
         "como": "En Interface Status, gris es conectado pero sin configurar o sin línea, el color de libre indica que la troncal está lista (verde en la guía de Grandstream, azul en el firmware actual de la serie A) y naranja es en uso. En Trunks, cada troncal aparece como Available, Busy, Abnormal o Unmonitored.",
         "ejemplo": "Un FXO naranja sin ninguna llamada en Active Calls es una pista: algo tiene tomada la línea. La lección Diagnóstico de línea arranca justamente de ese caso."},
    ],
    "teoria_md": """### Un poco de historia

Las centrales con líneas analógicas resolvían dos problemas desde siempre: elegir por qué línea sale cada llamada y mostrar a los usuarios qué líneas están ocupadas. Los sistemas de teclas lo hacían con un botón con luz por línea; la UCM conserva esa idea en el modo SLA, que el manual describe como la forma de emular un sistema de teclas sencillo.

Por dentro, la UCM es un Asterisk (el manual del UCM630x dice versión 16), y las placas analógicas de Asterisk se manejan con DAHDI, la interfaz de hardware de Digium que antes se llamaba Zaptel. Por eso las llamadas analógicas aparecen en Active Calls como canales DAHDI y la opción de selección de línea se llama DAHDI Out Line Selection.

### Cómo funciona

Cada FXO es un canal físico. La troncal analógica agrupa uno o varios de esos canales bajo un nombre, y las rutas trabajan con ese nombre: la ruta saliente dice por qué troncal salir y la entrante dice qué hacer con lo que llega por una troncal.

Para salir, si la troncal tiene varias FXO, la regla la pone DAHDI Out Line Selection. Con Ascend, la de fábrica, la central prueba el puerto 1; si está ocupado, el 2; y así hasta encontrar uno libre. Con Poll alterna y con Descend arranca por el último. La guía de Grandstream lo explica con un UCM6302 de dos puertos, y la lógica es la misma con los cuatro del UCM6304A.

Para entrar, la regla cambia. Por una línea analógica no llega el número que marcó el que llama, así que la central no tiene un número para comparar: sabe solamente por qué troncal entró. Si dos líneas van a destinos distintos, cada una necesita su propia troncal y su propia ruta entrante.

El Dashboard refleja todo esto: el color de cada FXO (gris sin configurar, libre, naranja en uso) y el estado de cada troncal. Mirarlo antes y después de cada cambio es la forma más rápida de saber si la central ve lo que esperás.""",
    "teoria_figs": [
        {"file": "14-t1.svg", "after": "y así hasta encontrar uno libre",
         "alt": "Animación en cuatro tiempos con las internas 1001 a 1003, una troncal Antel_Grupo con los FXO 1 y 2 en Ascend y los cuatro FXO a la derecha, el 3 y el 4 sin línea. 1: sale la llamada A; la troncal prueba el FXO1, está libre y lo toma. 2: sale la B con el FXO1 ocupado y la troncal la manda por el FXO2. 3: corta la A y el FXO1 vuelve a libre. 4: sale la C y Ascend arranca otra vez por el FXO1. Notas: Ascend empieza por el 1, Poll alterna y Descend arranca por la última; para entrar, la ruta es por troncal.",
         "caption": "Con Ascend, cada salida prueba primero el FXO1 y pasa al siguiente solo si está ocupado."},
    ],
}

# =====================================================================================  15
M["15"] = {
    "fig": {"file": "15.svg",
            "alt": "Cuatro líneas de tiempo de 0 a 6 segundos, todas a 425 Hz: invitación a marcar continua en azul; llamada, 1 s sí y 4 s no, en verde; ocupado, 0,5 s sí y 0,5 s no, en ámbar; congestión, 0,25 s sí y 0,25 s no, en rojo. Abajo, una nota con la fuente, la lista de tonos nacionales de la UIT (Rec. E.180, situación al 1 de mayo de 2010), y un aviso: la UCM viene en Estados Unidos, con ocupado de 480 y 620 Hz, y con eso no reconoce el ocupado uruguayo.",
            "caption": "En Uruguay todos los tonos son de 425 Hz: lo que distingue ocupado, llamada y congestión es la cadencia."},
    "steps": [
        {"file": "15-paso1.svg", "step": 1, "after": "Abrí la troncal y cargá los tonos",
         "alt": "La web en Analog Trunks > Antel_Linea1 > Tone Settings con Busy Detection Yes, Busy Tone Count 4, Tone Country Custom, Busy Tone f1=425@-50,c=500/500 (resaltado) y Congestion Tone f1=425@-50,c=250/250. A la derecha, cómo se lee: f1=425 es la frecuencia en Hz, @-50 el nivel, igual al de fábrica, y c=500/500 los milisegundos encendido y apagado; si Uruguay aparece en Tone Country, se usa. Abajo, un aviso sobre Busy Tone Count: 4, 6 u 8 según el manual, más alto corta más tarde y muy alto puede no cortar.",
         "caption": "Custom con 425 Hz y las cadencias de la UIT, y Busy Tone Count en 4."},
        {"file": "15-paso2.svg", "step": 2, "after": "Corré la detección con la línea libre",
         "alt": "Dos tarjetas. Con una línea, Semi-auto Detect: la UCM, desde el FXO1 como Source Channel, llama a tu celular como destino; la web avisa cuándo atender y cuándo cortar, y mide ocupado, polaridad y corte. Con dos líneas, Auto Detect: el FXO1 llama al FXO2, con el número real de la línea 2 como Destination Number, y la UCM atiende y corta sola. Abajo, el resultado llena Busy Tone, Polarity Reversal y Current Disconnect, la polaridad se activa solo si la detección la encontró y la prueba ocupa la línea alrededor de un minuto.",
         "caption": "PSTN Detection hace una llamada real de un minuto: Semi-auto con una línea, Auto con dos."},
        {"file": "15-paso5.svg", "step": 5, "after": "grabá la línea y medí el tono",
         "alt": "Arriba, los pasos en la UCM: Maintenance > Signaling Troubleshooting > Analog Record Trace en el FXO1, Start, llamada, cortar del otro lado, esperar 10 s, Stop y Download; y en la notebook: Audacity > File > Import > Raw Data con Signed 16-bit PCM, 1 canal y 8000 Hz, y Analyze > Plot Spectrum para la frecuencia. Abajo, el dibujo del archivo: conversación, una línea roja de corte del otro lado y después ráfagas de tono con 500 ms de tono y 500 ms de silencio.",
         "caption": "La grabación muestra qué manda la línea al cortar: tono y silencio que se miden en milisegundos."},
    ],
    "concepts": [
        {"name": "Supervisión de corte",
         "para_que": "En SIP, colgar es un mensaje. En una línea analógica no hay mensajes: la central tiene que deducir que el otro cortó a partir de lo que pasa en el par. Si no se entera, la línea queda tomada.",
         "como": "La UCM entiende tres señales: tono de ocupado o congestión (Busy y Congestion Detection), inversión de polaridad (Enable Polarity Reversal) y caída breve de tensión (Current Disconnect). Wikipedia cuenta que en muchos países de Sudamérica se usa el tono. Cuál manda Antel en cada línea se averigua con PSTN Detection.",
         "ejemplo": "En una agencia de viajes del Centro, los clientes cortan durante el mensaje del IVR y la línea sigue tomada dos minutos: con los tonos de fábrica, la UCM nunca reconoció el ocupado de 425 Hz."},
        {"name": "Tonos de Uruguay",
         "para_que": "Cada país define sus tonos de progreso de llamada. La UIT los recopila en la lista de la Recomendación E.180 para que equipos y técnicos sepan qué esperar en cada red.",
         "como": "Para Uruguay, la lista (situación de 2010) da 425 Hz para casi todo: invitación a marcar continua, ocupado 0,5 s y 0,5 s, llamada 1 s y 4 s, congestión 0,25 y 0,25. En la UCM se cargan en Tone Settings: Tone Country con el país si aparece o Custom con f1=425@-50,c=500/500 para el ocupado.",
         "ejemplo": "Un técnico de Salto deja el ocupado en Custom con 425 Hz y cadencia 500/500, corre PSTN Detection para confirmarlo y anota en la ficha que la línea corta por tono."},
        {"name": "PSTN Detection",
         "para_que": "Adivinar cómo corta una línea lleva tiempo y falla. La UCM trae una herramienta que hace una llamada real, la corta y mide lo que la línea manda, para llenar la configuración con valores reales.",
         "como": "En Tone Settings > Detect. Con dos líneas libres, Auto Detect llama de un FXO al número real del otro y atiende sola. Con una, Semi-auto Detect llama a un celular y la web avisa cuándo atender y cuándo cortar. Dura alrededor de un minuto y llena Busy Tone, Polarity Reversal y Current Disconnect.",
         "ejemplo": "En la puesta en marcha de un consultorio en Maldonado, PSTN Detection encuentra ocupado de 425 Hz y no encuentra inversión de polaridad: el técnico deja la polaridad apagada y anota el resultado."},
        {"name": "Busy Tone Count",
         "para_que": "Un solo tono parecido al ocupado no alcanza para cortar: la voz o la música pueden engañar al detector. Por eso la central espera varios tonos seguidos antes de colgar.",
         "como": "Viene en 2. El manual sugiere 4, 6 u 8 para evitar cortes al azar, sabiendo que más alto corta más tarde. Yeastar avisa que un valor muy alto puede no detectar nunca, y en un foro de Asterisk la detección de ocupado llegó a cortar salientes buenas.",
         "ejemplo": "Con Busy Tone Count en 4 y ocupado de 500/500, la UCM corta unos cuatro segundos después de que el otro colgó."},
    ],
    "teoria_md": """### Un poco de historia

Las centrales telefónicas avisan con tonos qué está pasando: invitación a marcar, llamada, ocupado, congestión. Cada país eligió los suyos, y la UIT publica la lista de "Diferentes tonos utilizados en las redes nacionales" según la Recomendación E.180. La edición consultada, con la situación al 1 de mayo de 2010, trae a Uruguay con 425 Hz en casi todos sus tonos.

Para avisar que el otro colgó, las redes usaron distintas señales. Wikipedia resume que en Norteamérica es común un intervalo breve sin tensión y que en muchos países de Sudamérica se usa un tono de desconexión. También existe la inversión de polaridad, que usan algunas redes para marcar el inicio o el fin de una llamada. Muchas líneas actuales salen de equipos del proveedor que no mandan esa liberación, como cuenta innovaphone, y la central tiene que adivinar.

### Cómo funciona

Cuando el otro corta, la línea de Antel sigue conectada y empieza a mandar algo: tono de ocupado, una inversión de polaridad o una caída breve de tensión. La UCM tiene un detector para cada cosa.

El detector de tono compara lo que escucha con el Busy Tone configurado: frecuencia y cadencia. De fábrica espera el ocupado de Estados Unidos, 480 y 620 Hz con 500/500, y no reconoce el de Uruguay, 425 Hz con 500/500. Cuando cuenta los tonos que dice Busy Tone Count, cuelga el FXO.

El detector de polaridad, si está activo, toma una inversión durante la llamada como corte; Polarity on Answer Delay ignora la que llega en los primeros 600 ms después de atender. El de corriente mira cada 200 ms (Current Disconnect Threshold) si la tensión cayó.

Hay un cuarto tiempo que importa: Ring Timeout, de 8000 ms, es lo que espera la UCM sin timbre para dar por cortada una entrante que todavía no se atendió.

Como Antel no publica qué usa, PSTN Detection mide con una llamada real, y Analog Record Trace graba lo que llega para medirlo a mano en Audacity.""",
    "teoria_figs": [
        {"file": "15-t1.svg", "after": "Cuando cuenta los tonos que dice Busy Tone Count, cuelga el FXO",
         "alt": "Animación en cuatro tiempos con dos filas iguales: Antel conectada al FXO1 de una UCM; arriba con Tone Country en Custom y el ocupado de Uruguay, 425 Hz 500/500, abajo con los tonos de fábrica de Estados Unidos, 480 y 620 Hz. 1: hay una llamada en curso y el FXO1 está en uso. 2: el otro cuelga; en analógico no hay mensaje y llega el tono de ocupado de 425 Hz. 3: arriba, la UCM cuenta cuatro tonos y cuelga, el FXO1 pasa a libre. 4: abajo no lo reconoce y el FXO1 queda tomado; el próximo que llama da ocupado.",
         "caption": "Con los tonos de Uruguay la UCM corta; con los de fábrica, la línea queda tomada."},
    ],
}

# =====================================================================================  16
M["16"] = {
    "fig": {"file": "16.svg",
            "alt": "Cuatro líneas de tiempo. Bellcore/Telcordia, el de fábrica en la UCM: timbre 1, después un bloque FSK y después el timbre 2. ETSI-FSK During Ringing: igual, el FSK después del primer timbre. ETSI Prior to Ringing: un aviso (LR, DTAS o RP), después FSK o DTMF y recién ahí el timbre 1. ETSI-DTMF: el número en tonos de teclado y después el timbre. Abajo, un aviso: en Bellcore el número viaja entre el primer y el segundo timbre, si la central atiende antes no llega, y el esquema de Antel no está publicado.",
            "caption": "Cada esquema manda el número en otro momento: entre timbres, antes del timbre o como tonos de teclado."},
    "steps": [
        {"file": "16-paso4.svg", "step": 4, "after": "Si no aparece, probá de a uno",
         "alt": "Una lista con casillas en orden: Auto-Detect, probalo primero; Bellcore/Telcordia, el de fábrica; ETSI-FSK During Ringing; ETSI-DTMF During Ringing; ETSI-FSK Prior to Ringing with LR, también DTAS y RP; ETSI-DTMF Prior to Ringing with LR, también DTAS y RP. A la derecha, en cada prueba: llamar desde un celular, dejar sonar al menos dos timbres y mirar el número en CDR y en el teléfono. Un aviso: antes, un teléfono con pantalla en el par confirma si la línea tiene la facilidad de Antel.",
         "caption": "Un esquema por vez, con una llamada desde el celular y dos timbres, hasta que aparezca el número."},
        {"file": "16-paso6.svg", "step": 6, "after": "Hacé una llamada real y ajustá de a poco",
         "alt": "La línea de Antel, el que llama, conectada a la UCM en el FXO1 de Antel_Linea1, y la UCM a la interna 1001. Lo que entra de la línea pasa por RX Gain hacia la interna; lo que sale de la interna hacia la línea pasa por TX Gain. Van de -13,5 a +12 dB, 0 de fábrica. Notas: si vos escuchás bajo al que llama, subí RX de a poco; si al otro lado te escuchan bajo, TX; y con eco, ruido o volumen raro, primero la impedancia con ACIM y después las ganancias.",
         "caption": "RX es lo que entra de la línea; TX, lo que sale hacia ella."},
    ],
    "concepts": [
        {"name": "Identificación de número llamante",
         "para_que": "Es el servicio de Antel que manda por la línea el número del que llama. Sin él, por más que la UCM esté bien configurada, no llega ningún número.",
         "como": "Se contrata aparte, con tarifa mensual, en la página de servicios de telefonía fija de Antel. La forma más simple de saber si está activo es enchufar un teléfono con pantalla en la línea y llamar desde un celular.",
         "ejemplo": "Un estudio contable en Parque Batlle se queja de que la UCM no muestra quién llama. El teléfono con pantalla tampoco lo muestra: la línea nunca tuvo el servicio, y el arreglo es un pedido a Antel."},
        {"name": "Caller ID Scheme",
         "para_que": "No hay una sola forma de mandar el número por una línea analógica. La UCM tiene que leerlo con el mismo esquema que usa la red, o lo pierde.",
         "como": "En la troncal, Use CallerID en Yes y Caller ID Scheme: Bellcore/Telcordia de fábrica, variantes ETSI-FSK y ETSI-DTMF durante o antes del timbre (con aviso por LR, DTAS o RP), SIN 227-BT, NTT o Auto-Detect. Como Antel no publica el suyo, se prueba Auto-Detect y después uno por uno.",
         "ejemplo": "En la UCM de una barraca en Las Piedras, Auto-Detect no muestra nada y ETSI-FSK During Ringing sí: el técnico lo deja fijo y lo anota en la ficha."},
        {"name": "ACIM y ganancias",
         "para_que": "Una línea de cobre tiene una impedancia que depende del país, de la central y del cable. Si el FXO no la iguala, aparecen eco, ruido o volumen raro, y subir el volumen solo agranda el problema.",
         "como": "En PBX Settings > Interface Settings > Analog Hardware, en las opciones de cada FXO, Detect (ERL o Pr) calcula la impedancia con la línea libre y Update la aplica. Después, en la troncal, RX Gain y TX Gain van de -13,5 a +12 dB, de a poco y con llamadas reales.",
         "ejemplo": "En una línea larga de un tambo en Florida, la detección de ACIM baja el eco y después alcanza con subir un poco el RX para escuchar bien al que llama."},
    ],
    "teoria_md": """### Un poco de historia

La idea de mostrar el número del que llama tiene más de medio siglo: Wikipedia cuenta que en 1968 Theodore Paraskevakos empezó a desarrollar un sistema para identificar al que llama, y que en 1977 el brasileño Valdir Bravo Salinas presentó una patente de un equipo identificador que se otorgó en 1982.

Con el tiempo quedaron varios estándares. En Estados Unidos, el de Bellcore, que manda los datos con un módem FSK Bell 202 de 1200 bits por segundo entre el primer y el segundo timbre. En Europa, ETSI EN 300 659-1, con FSK V.23 después del timbre, FSK antes del timbre con una señal de aviso, o tonos DTMF. Wikipedia tiene una tabla por país donde Uruguay no aparece, y aclara que a veces dos proveedores del mismo país usan estándares distintos. Antel vende el servicio como identificación de número llamante, sin decir el esquema.

### Cómo funciona

Con Bellcore, la línea suena una vez, en el silencio que sigue viaja el número en FSK y después suena el segundo timbre. Si la central atiende antes de ese silencio, el número no llega y queda como desconocido.

Con los esquemas ETSI "antes del timbre", la red primero avisa: una inversión de línea (LR), un tono doble (DTAS) o un pulso corto de timbre (RP). Después manda el número, en FSK o en DTMF, y recién ahí suena. La UCM tiene una variante para cada combinación, más Auto-Detect.

Si el esquema no coincide, la UCM recibe algo que no entiende: en Asterisk aparece como "Failed to decode CallerID". Por eso el orden es confirmar el servicio con un teléfono con pantalla, probar Auto-Detect y después los esquemas de a uno.

El audio sigue otra lógica. La señal de la línea entra por el FXO, pasa por el cancelador de eco y por RX Gain hacia las internas; lo que sale pasa por TX Gain hacia la línea. Si la impedancia del FXO no coincide con la de la línea, parte de la voz rebota como eco: por eso primero ACIM y después ganancias.""",
    "teoria_figs": [
        {"file": "16-t1.svg", "after": "Si la central atiende antes de ese silencio, el número no llega",
         "alt": "Animación en cuatro tiempos con dos filas, cada una con una línea de tiempo y la pantalla de la UCM. 1: con Bellcore suena el primer timbre y la pantalla dice sin número todavía. 2: entre el primer y el segundo timbre el número viaja en FSK y la UCM muestra 2900 1007. 3: si la UCM atiende antes del segundo timbre, el FSK no llega y la pantalla muestra Undetected. 4: abajo, con ETSI-DTMF antes del timbre, el número llega como tonos de teclado, la UCM lo muestra y después suena. Notas: Antel no publica el esquema; el número es un ejemplo.",
         "caption": "Bellcore manda el número entre timbres; ETSI-DTMF, antes de que suene."},
    ],
}

# =====================================================================================  17
M["17"] = {
    "fig": {"file": "17.svg",
            "alt": "Tres filas de cajas con flechas. Primera: FXO1 de la línea 1, troncal Antel_Linea1, extensión s de arranque, ruta entrante con Pattern _. y dos destinos, IVR 7000 y grupo 6000, en horario y fuera de horario. Segunda: FXO2, Antel_Linea2, s, ruta entrante con Pattern _. y destino fax. Tercera, en rojo: FXO3 de una línea nueva, Antel_Linea3 sin ruta entrante, y la llamada se queda en s. Notas: si en Active Calls una llamada queda en s, lo más probable es que su troncal no tenga ruta entrante o que el patrón no coincida; toda llamada analógica entra a la extensión s y el destino lo pone la ruta.",
            "caption": "Toda llamada analógica arranca en s; la ruta entrante de su troncal le da destino."},
    "steps": [
        {"file": "17-paso1.svg", "step": 1, "after": "Ruta entrante de la línea 1",
         "alt": "La web en Extension/Trunk > Inbound Routes > Add con Trunks Antel_Linea1, Pattern _., Default Destination IVR 7000 (resaltado), Time Condition con Office Time al IVR 7000 y fuera de horario al Ring Group 6000. A la derecha, por qué _.: el punto acepta uno o más caracteres de cualquier tipo y por una línea analógica no llega número llamado; y una nota de que el IVR 7000 y el grupo 6000 son los de las lecciones IVR con horario y Grupo o cola. Abajo: repetir con Antel_Linea2 y verificar en Active Calls que el destino nunca sea s.",
         "caption": "Una ruta entrante por troncal, con patrón _. y un destino que ya existe."},
        {"file": "17-paso4.svg", "step": 4, "after": "Ruta saliente por las líneas",
         "alt": "La web en Extension/Trunk > Outbound Routes > Add con los patrones _2XXXXXXX, _4XXXXXXX, _09XXXXXXX y _911, Privilege Level National, Use Trunk Antel_Linea1 y Failover Trunk Antel_Linea2 (resaltado). A la derecha, qué marca cada patrón: fijos de 8 cifras que empiezan con 2 o 4, celulares de 9 cifras que empiezan con 09 y emergencias 911; y qué número ve el que recibe: el de la línea por la que salió, porque Outbound Route CID no aplica a troncales analógicas. Abajo, la alternativa de prefijo _9X. con Strip 1 y que el 911 no se usa para pruebas.",
         "caption": "Los patrones de Uruguay por la línea 1, con la línea 2 de failover; el que recibe ve el número de la línea."},
    ],
    "concepts": [
        {"name": "La extensión s",
         "para_que": "Una llamada analógica no trae número llamado, pero la central igual necesita un lugar donde arrancar a procesarla. Asterisk usa para eso la extensión s, de start.",
         "como": "Toda llamada que entra por un FXO arranca en s y desde ahí la ruta entrante de su troncal la lleva al destino. En Active Calls, una llamada que se queda en s es una pista: lo más probable es que su troncal no tenga ruta entrante o que el patrón no coincida.",
         "ejemplo": "Después de agregar la línea 2 en un comercio de Malvín, las llamadas por esa línea aparecen en Active Calls con destino s y nadie las atiende: faltaba la ruta entrante de Antel_Linea2."},
        {"name": "Ruta entrante por troncal",
         "para_que": "Si no hay número llamado, la única forma de decidir a dónde va una llamada es por dónde entró. La ruta entrante analógica es una regla por troncal.",
         "como": "En Extension/Trunk > Inbound Routes se elige la troncal, un patrón que acepte todo (_.) y el destino: extensión, grupo, cola, IVR o fax, con condición de horario si hace falta. Cada troncal con su ruta.",
         "ejemplo": "En una óptica de Punta Carretas, la línea 1 entra al IVR 7000 en horario y al grupo 6000 fuera de horario, y la línea 2, que era del fax, va directo a la extensión del fax."},
        {"name": "Salida por varias líneas",
         "para_que": "Con dos líneas, la central puede usar la segunda cuando la primera está ocupada o no responde, sin que el usuario elija nada.",
         "como": "Una ruta saliente con los patrones de Uruguay (_2XXXXXXX y _4XXXXXXX para fijos, _09XXXXXXX para celulares, _911), privilegio National, Antel_Linea1 como troncal y Antel_Linea2 como failover; o una troncal con las dos FXO en Ascend. El que recibe ve el número de la línea por la que salió.",
         "ejemplo": "La dueña de un local en Tres Cruces quiere que siempre aparezca el número principal: se le explica antes de entregar que, si la línea 1 está ocupada y la llamada sale por la 2, el cliente ve el número de la 2."},
    ],
    "teoria_md": """### Un poco de historia

En una troncal SIP o digital, el proveedor manda el número que marcó el que llama, y la central lo usa para elegir la interna: es el DID de la lección Cada DID. Las líneas analógicas comunes nunca trajeron ese dato. El número llamado se usó para elegir la línea en la central de Antel, y lo que llega al edificio es solo el timbre.

Asterisk resolvió esto con una convención simple: toda llamada analógica arranca en una extensión llamada s, de start. Su documentación lo dice así y aclara que s no es un comodín sino el punto de arranque. En la comunidad de Asterisk se repite la consecuencia: no hay DID en líneas analógicas. La UCM, que es un Asterisk, conserva esa lógica y la muestra en Active Calls.

Del lado de la salida, Uruguay simplificó las cosas en 2010, cuando todos los números pasaron a 8 cifras y desaparecieron los códigos de área: fijos que empiezan con 2 en Montevideo y con 4 en el resto del país, y celulares de 9 cifras que empiezan con 09.

### Cómo funciona

Cuando suena una línea, la UCM atiende por el FXO y crea la llamada en s, marcada con la troncal por la que entró. Ahí busca las rutas entrantes de esa troncal: si una coincide, la llamada va a su destino; si ninguna coincide o no hay ruta, la llamada se queda sin destino.

Por eso la ruta se arma con un patrón que acepte todo, _., donde el punto quiere decir uno o más caracteres de cualquier tipo. El destino puede ser cualquier cosa de la central: una interna, el grupo 6000, la cola, el IVR 7000 con su horario o el fax.

Para salir es al revés: la ruta saliente compara lo que marcó la interna con sus patrones y lo manda por la troncal elegida, o por la de failover si la primera no puede. La línea de Antel pone su propio número como identificador: el Outbound Route CID de la UCM no aplica a troncales analógicas.""",
    "teoria_figs": [
        {"file": "17-t1.svg", "after": "si ninguna coincide o no hay ruta, la llamada se queda sin destino",
         "alt": "Animación en cinco tiempos con la línea 2 de Antel, el FXO2 de la troncal Antel_Linea2, la extensión s, la ruta entrante con patrón _. y destino 6000, y las internas 1001 y 1002 del grupo 6000; abajo, lo que muestra Active Calls. 1: suena la línea 2 y la UCM atiende por el FXO2. 2: no llega número llamado y la llamada arranca en s; Active Calls muestra Antel_Linea2 hacia s. 3: la ruta entrante le da destino, el grupo 6000. 4: suenan las internas del grupo. 5: una línea cuya troncal, Antel_Linea3, no tiene ruta entrante se queda en s, sin destino.",
         "caption": "La llamada pasa por s y la ruta entrante de su troncal la lleva al grupo; sin ruta, se queda en s."},
    ],
}

# =====================================================================================  18
M["18"] = {
    "fig": {"file": "18.svg",
            "alt": "Seis tarjetas numeradas con flechas, en dos filas: 1, foto del estado en Dashboard, Active Calls y CDR antes de tocar nada; 2, medir el par en reposo y descolgado con el UCM desconectado; 3, teléfono de prueba con tono, timbre y número en pantalla; 4, sacar lo que cuelga del par, una línea con un equipo; 5, en verde, cambiar el par de puerto para ver si la falla sigue a la línea; 6, configuración y grabación: ruta entrante, detección, Analog Record Trace y syslog. Abajo, dos salidas: si la falla sigue a la línea, reclamo a Antel al 121 con número, síntoma, horario y mediciones; si se queda en el puerto, es la central.",
            "caption": "De la ficha a la configuración: seis pasos, y cambiar el par de puerto decide de qué lado está la falla."},
    "steps": [
        {"file": "18-captura-active-calls.webp", "step": 1, "after": "Sacá la foto del estado",
         "alt": "Captura editada de System Status > Active Calls de un UCM6304A con dos llamadas. La primera, de 9 segundos: canal DAHDI/o2, troncal Antel_Linea2 y destino s. La segunda, de 18 segundos: número 0000 Undetected, troncal Antel_Linea1 y destino 100 Recepción. Los nombres de troncal y de la extensión se reemplazaron para no mostrar datos del cliente.",
         "caption": "Captura editada del caso: la llamada por la línea 2 queda en s y la de la línea 1 llega sin número (Undetected)."},
        {"file": "18-paso5.svg", "step": 5, "after": "Cambiá los pares: la línea 2 al FXO1",
         "alt": "Antes: la línea 1, par A, al FXO1 libre y la línea 2, par B con la falla, al FXO2 en uso. Después de cruzar los pares: la línea 2 al FXO1 y la línea 1 al FXO2. Dos resultados: si la falla pasa al FXO1, sigue a la línea 2, es la línea o algo conectado en ella, se revisa el par y se reclama a Antel; si se queda en el FXO2, es la central: troncal, ruta, detección y después el hardware. Abajo: al terminar, cada par vuelve a su puerto porque las troncales están atadas al FXO1 y al FXO2.",
         "caption": "Si la falla sigue a la línea, es la línea; si se queda en el puerto, es la central."},
    ],
    "concepts": [
        {"name": "Cambiar el par de puerto",
         "para_que": "Cuando un puerto falla, hay dos sospechosos: la línea (o lo que cuelga de ella) y la central (el puerto o su configuración). Cruzar los pares entre dos FXO separa a los dos sospechosos en cinco minutos.",
         "como": "Con dos líneas, se pasa la línea con falla al otro FXO y la sana al de la falla. Si el síntoma se va con la línea, es la línea; si se queda en el puerto, es la UCM. Después cada par vuelve a su lugar, porque las troncales están atadas a cada FXO.",
         "ejemplo": "En el comercio del caso, cruzar los pares diría si el loop es de la línea 2 (entonces medir, desconectar lo que cuelga y reclamar) o del FXO2 (entonces troncal, ruta y detección de ese puerto)."},
        {"name": "Analog Record Trace",
         "para_que": "En analógico no hay mensajes para capturar como en SIP: lo que pasa está en el audio de la línea. La UCM puede grabar ese audio en el puerto para escuchar y medir qué llega.",
         "como": "En Maintenance > Signaling Troubleshooting > Analog Record Trace se elige el puerto, Start, se reproduce la falla, Stop y Download. El archivo se abre en Audacity como datos en bruto de 16 bits, mono, 8000 Hz. Para el caller ID o un loop, conviene grabar dos o tres ciclos.",
         "ejemplo": "La grabación del FXO2 de un local en el Prado muestra un timbre corto cada diez segundos sin nadie llamando: con eso el reclamo a Antel ya no es una sensación, es un archivo."},
        {"name": "Hipótesis del loop de 10 segundos",
         "para_que": "Un FXO que se ocupa y se libera solo tiene varias causas posibles. Ponerles nombre evita cambiar ajustes al azar.",
         "como": "Encaja con lo visto que la UCM tome algo por timbre (un timbre real, ruido o una inversión de polaridad), atienda, la llamada quede en s sin destino, no vuelva a sonar y, pasado el Ring Timeout de 8000 ms, la dé por cortada. FreePBX documentó entrantes fantasma por inversión de polaridad al colgar, y Asterisk muestra un FXO en uso cuando no ve la tensión correcta. Se confirma o se descarta midiendo, cruzando pares y grabando.",
         "ejemplo": "Si al cruzar los pares el loop se va con la línea y la grabación muestra un timbre corto, el reclamo a Antel lleva el número, el horario y el archivo."},
        {"name": "Reclamo a Antel con datos",
         "para_que": "Un reclamo que dice \"no anda la línea\" vuelve muchas veces con \"la línea está bien\". Uno con mediciones y pruebas de separación le da al servicio técnico lo que necesita para buscar.",
         "como": "Reclamos de telefonía fija al 121 desde un fijo o al *121 desde un móvil Antel, todos los días las 24 horas; empresas, atención técnica al 0800 2599. Se da el número, el síntoma, desde cuándo y en qué horarios, la tensión medida, el resultado con teléfono de prueba y que la falla siguió a la línea al cambiar de puerto.",
         "ejemplo": "\"Línea con loop cada 10 segundos desde ayer a la mañana; en reposo mide lo de siempre; con teléfono de prueba suena un timbre corto sin llamada; al cambiar de puerto la falla siguió a la línea.\""},
    ],
    "teoria_md": """### Un poco de historia

Antes de las centrales IP, el diagnóstico de una línea era trabajo de campo: multímetro, teléfono de prueba y recorrer el par. Esas herramientas siguen siendo las primeras, porque una línea analógica no deja registros: lo que pasa está en la tensión y en el audio.

Lo nuevo es lo que agrega la central. En Asterisk, una placa DAHDI puede leer la tensión del FXO, y un FXO que no ve la tensión correcta figura en uso con alarma roja, como muestra un hilo de la comunidad de Asterisk. Grandstream suma Analog Record Trace, que graba el audio del puerto, y el módulo chan_dahdi de syslog para los eventos analógicos. Y los foros dejaron casos que hoy sirven de guía, como las entrantes fantasma que documentó FreePBX en 2016, causadas por la inversión de polaridad al colgar.

### Cómo funciona

El caso que guía la lección es real y está anonimizado: un comercio con dos líneas de Antel en el FXO1 y el FXO2 de un UCM6304A. Un día la línea 2 no recibe llamadas. Al siguiente, el FXO2 se ocupa y se libera cada unos 10 segundos. El Dashboard lo muestra naranja con cero llamadas activas; Active Calls muestra una llamada por Antel_Linea2 con destino s y otra por Antel_Linea1 con número Undetected que sí llega a recepción.

Lo que sigue es una hipótesis, no un diagnóstico. El destino s sugiere una entrante que no encontró ruta. Undetected, que no llegó el identificador (sin servicio o con otro esquema). El naranja sin llamadas puede ser un equipo en paralelo con la línea tomada o una tensión que la UCM no reconoce. Y el ritmo de diez segundos se parece al Ring Timeout de 8000 ms: la UCM toma algo por timbre, no vuelve a sonar y suelta.

El método separa causas en orden: medir el par sin la central, probar con un teléfono, sacar lo que cuelga, cruzar los pares entre FXO1 y FXO2, revisar ruta y detección y grabar. Recién con eso se sabe si llamar a Antel o seguir en la central.""",
    "teoria_figs": [
        {"file": "18-captura-troncales.webp", "after": "Al siguiente, el FXO2 se ocupa y se libera cada unos 10 segundos",
         "alt": "Captura editada del Dashboard de un UCM6304A durante el caso: en Interface Status, FXO 1 y FXO 2 en naranja y FXO 3 y 4 en gris; en Trunks, Antel_Linea1 y Antel_Linea2 con el punto naranja de Busy, y el resumen Available 0, Busy 2, Abnormal 0. Los nombres de las troncales se reemplazaron para no mostrar los números reales.",
         "caption": "Captura editada del caso: las dos troncales en Busy y los FXO 1 y 2 en naranja."},
        {"file": "18-t1.svg", "after": "la UCM toma algo por timbre, no vuelve a sonar y suelta",
         "alt": "Animación en cuatro tiempos de una hipótesis del caso: un FXO2 que se ocupa y se libera cada unos 10 segundos. Arriba, el estado del FXO2, Active Calls y una barra del Ring Timeout de 8000 ms; abajo, una línea de tiempo de 30 segundos con tres ciclos naranja y azul. 1: en el FXO2 aparece algo que la UCM toma por timbre, que puede ser un timbre real, ruido o una inversión. 2: la UCM toma la llamada, el puerto pasa a en uso y Active Calls muestra DAHDI/o2 por Antel_Linea2 hacia s. 3: no vuelve a sonar y, pasado el Ring Timeout, la da por cortada. 4: el puerto se libera un instante y, si el disparo se repite, el ciclo vuelve a empezar. Nota: es una hipótesis; se confirma midiendo, cruzando pares y grabando.",
         "caption": "Una hipótesis que encaja con el caso: toma por timbre, espera el Ring Timeout y suelta."},
    ],
}

# ----------------------------------------------------------------------------------- verificación
DASH = re.compile("[—–]")


def lab_lines(lid):
    d = next(CLASS.glob(f"{int(lid):02d}-*"))
    card = (d / "card.md").read_text(encoding="utf-8")
    lab = card.split("**Laboratorio**", 1)[1].split("**Regla para quedarse**", 1)[0]
    out, fence = [], False
    for ln in lab.splitlines():
        if ln.strip().startswith("```"):
            fence = not fence
            continue
        if not fence:
            out.append(ln)
    return out


# enriquecer.py (versión del 28/10) toma un .svg de fig o de paso como animación y lo busca tal cual en site2:
# las ilustraciones fijas van con su nombre .webp, que es lo que dejó render_svg.py.
for m in M.values():
    for it in [m["fig"]] + m["steps"]:
        if it["file"].endswith(".svg"):
            it["file"] = it["file"][:-4] + ".webp"

problemas = []
for lid, m in M.items():
    files = [m["fig"]["file"]] + [s["file"] for s in m["steps"]] + [t["file"] for t in m.get("teoria_figs", [])]
    for f in files:
        p = SITE / f
        if not p.exists():
            problemas.append(f"{lid}: falta {p.name}")
    lines = lab_lines(lid)
    for s in m["steps"]:
        n = sum(s["after"] in ln for ln in lines)
        if n != 1 or not 15 <= len(s["after"]) <= 43:
            problemas.append(f"{lid}: ancla de paso '{s['after']}' aparece {n} veces o tiene largo {len(s['after'])}")
    th = m["teoria_md"]
    w = len(th.split())
    if not (250 <= w <= 450) or "### Un poco de historia" not in th or "### Cómo funciona" not in th:
        problemas.append(f"{lid}: teoría con {w} palabras o sin subtítulos")
    paras = th.split("\n\n")
    for t in m.get("teoria_figs", []):
        hits = [p for p in paras if t["after"] in p]
        if len(hits) != 1 or hits[0].startswith("###") or th.count(t["after"]) != 1:
            problemas.append(f"{lid}: ancla de teoría '{t['after']}'")
    if not 2 <= len(m["concepts"]) <= 4:
        problemas.append(f"{lid}: {len(m['concepts'])} conceptos")
    if DASH.search(json.dumps(m, ensure_ascii=False)):
        problemas.append(f"{lid}: guion largo")
    print(lid, "teoría", w, "palabras")

out = ROOT / "ilustraciones" / "grandstream" / "manifest-fxo.json"
json.dump(M, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", out, len(M), "lecciones")
print("problemas:", problemas or "ninguno")
