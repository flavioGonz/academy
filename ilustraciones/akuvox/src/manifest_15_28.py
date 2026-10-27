"""Genera manifest-15-28.json (lecciones 15 a 28 del curso Akuvox) y valida:
- que cada SVG exista, - que cada `after` aparezca una sola vez en el laboratorio de card.md y fuera de bloques de código,
- que teoria_md tenga 250 a 450 palabras y los dos subtítulos exactos, - que no haya guiones largos."""
import json, re, glob, sys
from pathlib import Path

OUT = Path("/home/claude/ies-training/ilustraciones/akuvox")
CLASS = Path("/home/claude/claudemy/akuvox/class")

M = {}

# =============================================================== 15
M["15"] = {
    "fig": {"file": "15.svg",
            "alt": "Un monitor en el centro con dos teclas, Hall y Portón. A la izquierda, el portero del hall (192.168.88.21) está en llamada con el monitor por SIP y DTMF. A la derecha, el portero del portón (192.168.88.22) no está en llamada y recibe un pedido HTTP del monitor. Abajo, la URL que manda la tecla Portón, con DoorNum=1 resaltado.",
            "caption": "DTMF solo llega al portero que está en la llamada; la tecla HTTP llega a cualquier portero por su IP."},
    "steps": [
        {"file": "15-paso2.svg", "step": 2,
         "alt": "Ventana web del monitor en Phone > Relay > Remote Relay By HTTP or HTTPS con IP 192.168.88.22, formato /fcgi/OpenDoor, usuario monitor-porton, clave Ejemplo-Mon-2026 y DoorNum 1; botón +Add marcado como paso 3. A la derecha, el portero del portón con Open Relay via HTTP habilitado (paso 1).",
         "caption": "El monitor guarda IP, formato, usuario propio y DoorNum del portero del portón; +Add lo deja listo.",
         "after": "(en otros modelos, buscá"},
        {"file": "15-paso4.svg", "step": 4,
         "alt": "Tres pantallas de monitor con la tecla Portón: monitoreo (Softkey In Monitor Page, paso 4), en llamada (Softkey in Talking Page, paso 6) y vista previa (Softkey In Call-Preview Page, opcional). Abajo, la configuración de la tecla: Enabled sí, Type Remote Relay By HTTP or HTTPS, Label Portón.",
         "caption": "La misma tecla se repite en cada pantalla donde el cliente la quiera usar.",
         "after": "habilitá una tecla, tipo"},
    ],
    "concepts": [
        {"name": "Remote Relay By HTTP or HTTPS",
         "para_que": "Nació para el caso que el DTMF no resuelve: abrir un portero que no está en la llamada. El código DTMF viaja dentro de la llamada y solo lo escucha el equipo con el que estás hablando; si el cliente atiende al hall y quiere abrir el portón, el portón nunca se entera.",
         "como": "En el monitor se carga la IP (o el número SIP) del portero de destino, el formato de URL que ese portero acepta y un usuario y clave propios del monitor. El formato lo decide el firmware del portero: con alta seguridad encendida, solo `/fcgi/OpenDoor`. DoorNum elige el relé: 1 es el A, 2 es el B.",
         "ejemplo": "Casa en Carrasco con portero en la puerta peatonal y otro en el portón del garaje. El monitor del living tiene `Remote Relay` apuntando a 192.168.88.22 con el usuario `monitor-porton`: el dueño atiende al cartero en la peatonal y abre el garaje para el delivery sin cortar."},
        {"name": "Las tres pantallas de teclas",
         "para_que": "Cada momento de uso tiene su pantalla: en llamada (Talking Page), mirando la cámara sin que nadie llame (Monitor Page) y viendo quién llama antes de atender (Call-Preview Page). Akuvox separó las teclas para que el instalador decida dónde tiene sentido cada apertura.",
         "como": "En `Phone > Relay > Key Setting` se habilita una tecla por pantalla, tipo `Remote Relay By HTTP or HTTPS` y con una etiqueta que diga el nombre de la puerta. Monitoreo y vista previa necesitan que el monitor ya reciba el video de ese portero; si no ves el video, arreglá eso primero.",
         "ejemplo": "En un PH de Malvín, la señora mayor usa sobre todo la pantalla de monitoreo: mira el portón y toca `Portón` cuando llega la camioneta del supermercado. La misma tecla en la pantalla de llamada le sirve cuando el repartidor sí toca timbre."},
        {"name": "Un usuario HTTP por monitor",
         "para_que": "Una tecla que abre sin llamada es una llave más del edificio. Si todos los monitores usan la misma credencial, no hay forma de dar de baja uno sin tocar a los demás, y ningún registro dice desde dónde se abrió.",
         "como": "En el portero de destino se crea un usuario para cada monitor (`monitor-porton`, `monitor-apto3`) y se anota en la planilla de credenciales de la lección 14. Conviene que el monitor esté en un ambiente que el cliente controle, no en un pasillo común.",
         "ejemplo": "Un inquilino se muda de un edificio en Cordón y se lleva el monitor por error. Con usuarios separados, en el portón cambiás la clave de `monitor-apto3` y listo; los demás monitores siguen abriendo."},
    ],
    "teoria_md": """### Un poco de historia

Los porteros de dos hilos resolvían la apertura con un pulsador en el auricular que cerraba un circuito hasta la cerradura. Cuando el portero pasó a IP y a SIP, la apertura se mudó a la llamada: el monitor manda un tono DTMF (RFC 2833, o su sucesor RFC 4733) y el portero, que lo escucha, dispara su relé. Funciona muy bien mientras haya una sola puerta, porque el tono solo viaja por la llamada en curso.

Con dos porteros aparece el problema que la comunidad de FreePBX documentó con dos puertas: el DTMF solo llega al equipo con el que estás hablando. La salida que tomó Akuvox fue la misma que ya usaba en su API: abrir por HTTP. Su guía oficial lo muestra con un R29 como portero y un C313 como monitor, y aclara que todos sus equipos de intercom soportan la función.

### Cómo funciona

Hay dos mitades. En el portero de destino, `Open Relay via HTTP` habilita un pequeño servicio web que acepta pedidos de apertura con usuario y clave. En el monitor, `Remote Relay By HTTP or HTTPS` guarda a quién pedirle: IP o número SIP, formato de URL y credenciales.

Cuando tocás la tecla, el monitor arma un pedido HTTP GET como este:

`http://monitor-porton:clave@192.168.88.22/fcgi/OpenDoor?action=OpenDoor&DoorNum=1`

El portero verifica la credencial y dispara el relé indicado: `DoorNum=1` es el relé A y `DoorNum=2` el B. No hace falta llamada abierta ni central: el pedido va directo por la red, por eso conviene que monitor y portero estén en la misma VLAN de porteros.

El formato importa. Un portero con firmware de alta seguridad (tercer bloque del firmware 10 o más) y el modo encendido solo acepta `/fcgi/OpenDoor`; la URL vieja `/fcgi/do` con usuario y clave en la consulta queda rechazada. Por eso, antes de cargar el monitor, se mira el firmware del portero.

Las teclas se crean por pantalla: llamada, monitoreo y vista previa. Monitoreo y vista previa dependen de que el monitor ya reciba el video del portero, así que el orden práctico es video primero, tecla después. Akuvox documenta esto con una sola guía, así que conviene probarlo en el modelo real antes de prometerlo en obra."""
}

# =============================================================== 16
M["16"] = {
    "fig": {"file": "16.svg",
            "alt": "Comparación en dos paneles. Izquierda, en rojo: el relé A del portero, en la calle, maneja directamente la cerradura; si rompen el portero, la cerradura queda a su alcance. Derecha, en verde: el portero se conecta por RS485 a un SR01 adentro, y el SR01 maneja la cerradura; rompen el portero y la puerta sigue cerrada. Abajo, la URL con DoorNum=SB.",
            "caption": "Con el SR01, el relé que abre queda del lado de adentro y el portero solo pide."},
    "steps": [
        {"file": "16-paso1.svg", "step": 1,
         "alt": "Portero en la zona calle conectado por RS485 a un SR01 en la zona adentro; el SR01 conecta por su relé a una cerradura de banco. En línea punteada roja, la otra opción: la salida de 12 V del portero al SR01, que se habilita como Security Relay A. Aviso: el E12 no tiene RS485.",
         "caption": "Por RS485 se habilita Security Relay B; por la salida de 12 V, Security Relay A.",
         "after": "Cableá el SR01 al portero por RS485"},
        {"file": "16-paso2.svg", "step": 2,
         "alt": "Ventana Access Control > Relay > Security Relay con Security Relay B habilitado, Trigger Delay 0 y Hold Delay 5, y ventana Device > RS485 con Apply RS485 Setting To en Others y botón Submit. Abajo, una línea de tiempo: con Trigger Delay 0 el relé se activa al instante y queda activado 5 segundos.",
         "caption": "Trigger Delay es la espera antes de activar; Hold Delay, cuánto queda activado.",
         "after": "(su modo de servidor es RS485)"},
        {"file": "16-paso4.svg", "step": 4,
         "alt": "Terminal con el comando curl a $PORTERO/fcgi/OpenDoor con DoorNum=SB. Debajo, cuatro filas: DoorNum=1 relé A en el portero, DoorNum=2 relé B en el portero (paso 5), DoorNum=SA Security Relay A por la salida de 12 V, DoorNum=SB Security Relay B por RS485 (paso 4).",
         "caption": "La misma URL abre relés distintos según DoorNum: 1 y 2 en el portero, SA y SB en el SR01.",
         "after": "con el usuario HTTP de la lección 13"},
    ],
    "concepts": [
        {"name": "SR01, relé de seguridad",
         "para_que": "Si la cerradura cuelga del relé del portero, el contacto que abre está en la calle: quien rompe el frente encuentra los cables a mano. Akuvox lo explica así en su guía: el SR01 va adentro y maneja la cerradura directo, de modo que aunque destruyan el portero la puerta no abre.",
         "como": "Se conecta al portero por RS485 (se habilita `Security Relay B` y en `Device > RS485` se elige `Others`) o por la salida de 12 V (se habilita `Security Relay A` y se elige ese tipo en `12V Power Output`). Cada modelo pide un firmware mínimo, listado en la guía. Los bornes exactos salen del video de cableado de Akuvox.",
         "ejemplo": "Edificio en Pocitos con el portero en la reja de la vereda: el SR01 va en la caja de la portería, adentro, y maneja el electroimán de la puerta del hall. Si un día aparece el frente arrancado, el hall sigue cerrado."},
        {"name": "DoorNum: 1, 2, SA y SB",
         "para_que": "Un mismo comando HTTP tiene que poder elegir qué relé dispara, sea uno del portero o uno externo. DoorNum es ese selector.",
         "como": "`DoorNum=1` dispara el relé A local, `2` el B, `SA` el Security Relay A (SR01 por 12 V) y `SB` el Security Relay B (SR01 por RS485). La URL, el usuario y el formato son los mismos de la lección 13; solo cambia ese valor.",
         "ejemplo": "`curl -s -u 'abre-lab:Ejemplo-Http-2026' \"192.168.88.21/fcgi/OpenDoor?action=OpenDoor&DoorNum=SB\"` abre la puerta del hall por el SR01, y con `DoorNum=2` el mismo usuario abre el portón vehicular cableado al relé B."},
        {"name": "Trigger Delay y Hold Delay",
         "para_que": "No todas las cargas quieren lo mismo: un electroimán necesita unos segundos sin energía para que la persona empuje, y un portón con central propia solo quiere un pulso. Los dos tiempos permiten ajustar eso sin tocar cables.",
         "como": "Trigger Delay es la espera desde la orden hasta que el relé se activa (0 es inmediato). Hold Delay es cuánto queda activado. En el E18 no hay Hold Delay. Anotá en la ficha qué relé maneja cada carga y con qué tiempos.",
         "ejemplo": "En una cochera de Punta Carretas, el relé B da un pulso a la central del portón (Hold Delay corto) y el SR01 libera 5 segundos el electroimán de la puerta peatonal."},
        {"name": "Web Relay y relés del monitor",
         "para_que": "A veces la carga está lejos del portero o hacen falta más salidas. Para eso Akuvox suma relés por red: Web Relay de terceros desde el portero, módulos RS485 en el monitor (MK485, RSAC-C1-R8) y el WR01 como relé de borde.",
         "como": "En el portero, `Access Control > Web Relay` manda comandos tipo `state.xml?relayState=2` a un relé web (hasta 50 URLs completas dejando la IP en blanco), disparados por DTMF, tarjeta o nube. En el monitor, `Device > External Relay` maneja hasta 8 relés por módulo. El WR01 trae 2 relés, 2 entradas y API.",
         "ejemplo": "En una casa con barbacoa al fondo, el residente prende la luz del jardín desde el monitor con un RSAC-C1-R8 en el tablero, sin tirar un cable nuevo hasta el portero."},
    ],
    "teoria_md": """### Un poco de historia

Durante décadas el portero eléctrico se cableó igual: el frente en la calle y, detrás, el contacto que alimenta la cerradura. Era simple y barato, pero dejaba el punto débil afuera. La industria del control de acceso resolvió esto hace mucho separando el lector, que puede estar expuesto, del controlador, que va del lado seguro. El SR01 aplica esa misma idea al portero: el frente pide, el relé de adentro decide.

Para hablar entre las dos piezas Akuvox usa RS485, un estándar de capa física de 1983 (TIA/EIA-485) pensado para la industria: un par trenzado diferencial, distancias largas y tolerancia al ruido. Es el mismo bus que se usa en lectores, controladoras y automatismos, y por eso aparece también en los monitores para sumar módulos de relés.

### Cómo funciona

Hay tres familias de relés en esta lección:

- **Locales**: los relés A y B del propio portero. `DoorNum=1` y `DoorNum=2`.
- **De seguridad**: el SR01 adentro. Por RS485 se configura como `Security Relay B` y por la salida de 12 V como `Security Relay A`. Por HTTP, `DoorNum=SB` o `DoorNum=SA`.
- **Por red**: Web Relay de terceros desde el portero, MK485 o RSAC-C1-R8 en el monitor, y el WR01 como controlador de borde con 2 relés, 2 entradas, PoE o 12 a 24 V y API abierta.

Cuando el SR01 va por RS485, el portero le manda la orden por el bus y el SR01 cierra su propio contacto. Si alguien arranca el frente y puentea los cables que encuentra, solo tiene un bus de datos: ningún par de esos cables alimenta la cerradura. Akuvox pide además cargar usuarios y credenciales para el SR01, y lista un firmware mínimo por modelo.

Cada relé tiene dos tiempos. **Trigger Delay** es la espera desde la orden hasta que el relé actúa; **Hold Delay**, cuánto tiempo queda activado. Con `Trigger Delay 0` y `Hold Delay 5`, el relé se activa al instante y vuelve al reposo a los 5 segundos.

La excepción importante es el E12: no tiene RS485 y su conexión al SR01 es especial. Akuvox no la recomienda por seguridad. Si la cerradura tiene que resistir un ataque al frente, conviene un portero con RS485."""
}

# =============================================================== 17
M["17"] = {
    "fig": {"file": "17.svg",
            "alt": "Un portero (192.168.88.21) y un servidor (192.168.88.10, puerto 8000). En el medio, tres eventos: tarjeta válida, relé A se dispara y relé A cierra. Para cada uno se ve la URL cargada con variables ($card_sn, $relay1status) y lo que realmente llega al servidor (/validcard=número de tarjeta, /relaytrigger=1, /relayclose=0).",
            "caption": "El portero reemplaza cada variable por el dato real y manda un GET por evento."},
    "steps": [
        {"file": "17-paso2.svg", "step": 2,
         "alt": "Ventana Device Management > Setting > Action URL con Action URL habilitado y tres URLs: Relay A Triggered, Relay A Closed y Valid Card Entered apuntando a http://<IP_SERVIDOR>:8000; Setup Completed resaltado y vacío. Debajo, tabla de variables y un aviso de que Setup Completed no depende del interruptor.",
         "caption": "Una URL por evento; Setup Completed queda vacío porque no lo controla el interruptor general.",
         "after": "habilitado; cargá (reemplazando"},
        {"file": "17-paso3.svg", "step": 3,
         "alt": "Terminal de la PC de laboratorio con python3 -m http.server y tres líneas GET que llegan desde 192.168.88.21: /validcard=..., /relaytrigger=1 y /relayclose=0, todas con respuesta 404. Flechas las asocian a tarjeta válida, relé abre y relé cierra.",
         "caption": "El 404 no importa: cada línea demuestra que el portero avisó.",
         "after": "abrí la puerta con una tarjeta válida"},
    ],
    "concepts": [
        {"name": "Action URL",
         "para_que": "Para que otros sistemas se enteren de lo que pasa en el portero sin preguntarle a cada rato. En vez de que el NVR o la domótica consulten el estado, el portero avisa cuando hay un evento: llamada, relé, entrada, código, tarjeta, rostro, QR, intrusión o arranque.",
         "como": "En `Device Management > Setting > Action URL` (así en el R20A 320.30.11.47) se habilita la función y se carga una URL por evento. Si el servidor pide digest, hay campos de usuario y clave; si la URL trae credenciales, mandan esas. Los eventos disponibles cambian por modelo.",
         "ejemplo": "En una oficina en Ciudad Vieja, cada `Valid Card Entered` le avisa a un servidor de registro que guarda hora y tarjeta: el encargado sabe quién abrió a las 7 de la mañana sin entrar a la web del portero."},
        {"name": "Variables que el equipo completa",
         "para_que": "Una URL fija solo diría qué pasó; las variables dicen con qué dato. El portero las reemplaza antes de mandar el pedido.",
         "como": "`$relay1status` vale 1 abierto y 0 cerrado, `$card_sn` es el número de tarjeta, `$code` el código, `$unlocktype` cómo se abrió, y `$mac`, `$ip`, `$model`, `$firmware` identifican al equipo. Se pueden encadenar, por ejemplo `mac=$mac:ip=$ip:model=$model`.",
         "ejemplo": "Con dos porteros mandando al mismo servidor en un edificio de Cordón, sumar `ip=$ip` a la URL permite separar en el registro qué aperturas fueron del hall y cuáles del garaje."},
        {"name": "Setup Completed y los datos sensibles",
         "para_que": "El evento de arranque sirve para saber que el portero se reinició (corte de luz, actualización). Justamente por eso Akuvox lo dejó fuera del interruptor general: avisa aunque Action URL esté apagado.",
         "como": "Si no lo vas a usar, el campo queda vacío. Y como `$card_sn` y `$code` viajan dentro de la URL, el servidor que recibe va en la VLAN de porteros y no deja esos logs a la vista de cualquiera.",
         "ejemplo": "Un técnico deja una URL de prueba en Setup Completed y se olvida: meses después, cada corte de UTE manda un aviso a una PC que ya no existe. Mejor vacío que apuntando a la nada."},
    ],
    "teoria_md": """### Un poco de historia

Hay dos formas de enterarse de lo que pasa en un equipo: preguntarle cada tanto (polling) o que él avise cuando ocurre algo. La segunda se popularizó en la web con los webhooks, pedidos HTTP que un sistema le manda a otro ante un evento. Los equipos IP de seguridad adoptaron la misma idea con distintos nombres; en Akuvox se llama Action URL.

El patrón ida y vuelta ya está documentado por terceros: ComfortClick integra un E11R escuchando por HTTP el timbre, el botón de salida y el movimiento, y abre los relés también por HTTP. Lo que abre por HTTP avisa por HTTP.

### Cómo funciona

Action URL es un cliente HTTP dentro del portero. Para cada evento hay un campo donde cargás una URL completa. Cuando el evento ocurre, el portero:

1. toma la URL cargada,
2. reemplaza las variables (`$relay1status`, `$card_sn`, `$code`, `$mac`, `$ip`, `$model`, `$firmware`, entre otras),
3. manda un GET a esa dirección.

Con la URL `http://192.168.88.10:8000/relaytrigger=$relay1status`, al dispararse el relé A llega `GET /relaytrigger=1`; al cerrarse, la URL de Relay A Closed manda `GET /relayclose=0`. El servidor no necesita hacer nada especial: alcanza con registrar la línea.

Por eso el laboratorio usa `python3 -m http.server`, el servidor web que viene con Python. No tiene esas páginas, así que responde 404, pero imprime cada pedido con la IP de origen y la ruta. Esa línea es la prueba de que el portero avisó.

Los eventos varían por modelo. En el X915V2 la lista incluye llamada, corte, relé A, B o C disparado y cerrado, entradas, código válido e inválido, tarjeta, rostro, QR, alarma de intrusión y arranque. El arranque (`Setup Completed`) tiene una particularidad: no lo controla el interruptor general de Action URL.

Si el servidor exige autenticación digest, Action URL tiene usuario y clave; si la URL ya trae credenciales, mandan esas. Como los datos viajan en la ruta, en texto claro cuando es HTTP, el receptor va en la misma VLAN que los porteros y sus registros se tratan como datos de acceso."""
}

# =============================================================== 18
M["18"] = {
    "fig": {"file": "18.svg",
            "alt": "Cuatro sistemas a la izquierda, cada uno con su usuario: PC con curl (curl-lab), MikroTik con /tool/fetch (mk-porton), Home Assistant con rest_command (ha-porton) y Asterisk o FreePBX con CURL() (usuario propio). Todos apuntan al mismo portero, que por el relé B abre un portón. Abajo, la URL común con DoorNum=2.",
            "caption": "La URL es la misma para todos; lo que cambia es el usuario de cada sistema."},
    "steps": [
        {"file": "18-paso1.svg", "step": 1,
         "alt": "Diagrama de secuencia entre curl y el portero 192.168.88.21: curl -u con basic recibe 401 Unauthorized; curl --digest abre el relé B. Debajo, tabla de cómo se elige basic o digest en curl, MikroTik /tool/fetch y Home Assistant.",
         "caption": "Si responde 401, el cliente habla otro método: igualalo con digest.",
         "after": "si responde 401 con basic"},
        {"file": "18-paso4.svg", "step": 4,
         "alt": "Un interno autorizado marca 7001 y la central Asterisk o FreePBX manda un GET al portero, que abre el portón. Otro interno que marca 7001 queda bloqueado en la central. Abajo, el dialplan con CURL y el aviso de restringir la extensión.",
         "caption": "La extensión 7001 es una llave: la central decide qué internos pueden marcarla.",
         "after": "Asterisk o FreePBX (extensión de prueba)"},
    ],
    "concepts": [
        {"name": "Probar con curl antes de integrar",
         "para_que": "Cuando algo no abre desde Home Assistant o desde la central, hay demasiadas capas para sospechar. curl es el cliente HTTP más directo: si con curl abre, el portero está bien y el problema está en el sistema que integra.",
         "como": "Se arma la URL completa y se prueba desde una PC de la misma red con el usuario de esa integración. Si responde 401 con basic, se agrega `--digest`. Recién cuando curl abre, se copia la misma URL al sistema final.",
         "ejemplo": "`curl -s -u 'curl-lab:Ejemplo-Curl-2026' \"192.168.88.21/fcgi/OpenDoor?action=OpenDoor&DoorNum=2\"` abre el portón de banco: ahora sabés que cualquier falla en Home Assistant es de su configuración."},
        {"name": "Basic o digest",
         "para_que": "Son dos formas estándar de mandar usuario y clave por HTTP. Basic los manda codificados en Base64, que se lee a simple vista; digest manda un resumen calculado con la clave, sin la clave en sí.",
         "como": "Cliente y portero tienen que hablar el mismo método. Home Assistant y MikroTik usan basic por defecto: en Home Assistant se pone `authentication: digest` y en MikroTik `http-auth-scheme=digest`. En curl, `--digest`.",
         "ejemplo": "Un MikroTik de un barrio en Canelones que abre el portón con un script devuelve error; el portero pide digest. Agregar `http-auth-scheme=digest` al `/tool/fetch` lo resuelve sin tocar el portero."},
        {"name": "Un usuario por sistema",
         "para_que": "Cada sistema que abre es una llave. Con un usuario por integración, se puede revocar una sin romper las otras y saber quién tiene cada credencial.",
         "como": "En el portero se crean `curl-lab`, `mk-porton`, `ha-porton` y uno para la central, y se anotan en la tabla de credenciales de la lección 14. Nunca `admin`.",
         "ejemplo": "La empresa que mantenía el Home Assistant de una casa en Carrasco deja de trabajar con el cliente: cambiás la clave de `ha-porton` y el MikroTik y la central siguen abriendo como siempre."},
        {"name": "Cámaras de patentes y sistemas sin acción HTTP",
         "para_que": "Algunas cámaras LPR pueden abrir directamente cuando leen una matrícula cargada, sin servidor intermedio. Otros sistemas, como UCM o HikCentral, no tienen una acción HTTP documentada en las páginas leídas.",
         "como": "Para LPR, la HTTP API del portero va en Allowlist con la IP de la cámara y la patente se carga en el usuario (hasta 5). Hikvision solo con X912 912.30.12.114 o R29 29.30.10.745 en adelante. Para UCM o HikCentral, DTMF o un intermediario.",
         "ejemplo": "En la entrada vehicular de un complejo en Ciudad de la Costa, una cámara Hikvision lee la matrícula del vecino y el R29 abre el portón por la HTTP API, sin que nadie toque un botón."},
    ],
    "teoria_md": """### Un poco de historia

HTTP nació para pedir páginas web, pero su forma simple (un método, una ruta, encabezados y una respuesta con código) lo volvió el idioma común entre equipos. HTTP/1.1 se publicó como RFC 2068 en 1997 y RFC 2616 en 1999; hoy lo describen los RFC 9110 a 9112 de 2022.

La autenticación también es antigua. Basic y Digest se definieron juntas en el RFC 2617 de 1999 y hoy viven en el RFC 7617 (Basic) y el RFC 7616 (Digest), ambos de 2015. curl, el cliente de línea de comandos que usamos para probar, existe desde 1998. Asterisk, la central de código abierto sobre la que corre FreePBX, nació en 1999 y su función `CURL()` está disponible desde Asterisk 10. Home Assistant arrancó en 2013 y `rest_command` es una de sus integraciones básicas. MikroTik trae `/tool/fetch` en RouterOS.

### Cómo funciona

Todos los clientes hacen lo mismo: un GET a `/fcgi/OpenDoor?action=OpenDoor&DoorNum=2` con un usuario y una clave. Lo que cambia es cómo se escribe en cada sistema.

Con **Basic**, el cliente manda el encabezado `Authorization: Basic` seguido de `usuario:clave` en Base64. Cualquiera que capture el tráfico puede decodificarlo. Con **Digest**, el servidor primero responde `401` con un desafío (un número aleatorio llamado nonce); el cliente calcula un resumen con la clave, la ruta y ese nonce, y lo manda en un segundo pedido. La clave no viaja.

Por eso el síntoma clásico es un `401`: el cliente mandó basic y el portero esperaba digest, o al revés. curl lo resuelve con `--digest`, Home Assistant con `authentication: digest` y MikroTik con `http-auth-scheme=digest`. Asterisk, con `CURL()`, pone el usuario y la clave dentro de la URL.

Dos detalles de cada sistema. En la consola de MikroTik, el `?` abre la ayuda, por eso se escribe `\\?` dentro de la URL. En Asterisk, la extensión que hace el `CURL()` abre el portón para quien la marque, así que la central restringe qué internos pueden llamarla.

Ninguno de estos métodos cifra el tráfico: eso lo hace HTTPS. Por eso todo esto vive en la VLAN de porteros, con un usuario dedicado por sistema."""
}

# =============================================================== 19
M["19"] = {
    "fig": {"file": "19.svg",
            "alt": "Cuatro columnas con un dibujo de edificio o casa y un portero genérico: casa u oficina chica con portero de un botón (E13S, E12, X910, R20A, R25A); edificio con varios destinos con teclado o botones (R20K, R20K-L, R20B con MD06 o MD12, R28); acceso con pantalla y rostro (R29, S535, X912, E18, E16); acceso principal grande con Android grande (S539, S538, X916, X915). Abajo: portón con cámara de patentes Hikvision, R29 o X912.",
            "caption": "Una orientación para arrancar: la forma de llamar y la pantalla ordenan el catálogo."},
    "steps": [
        {"file": "19-paso2.svg", "step": 2,
         "alt": "Planilla con columnas Modelo, Tipo, Serie, Sistema, PoE, Relé y En el menú hoy, y filas R29, E16C y C315 (resaltada, no está en el menú). Flechas indican la fuente de cada columna: tabla de alimentación para PoE, tabla de relé para Relé y menú de akuvox.com para En el menú hoy.",
         "caption": "Cada columna sale de una fuente distinta; lo que no figura se escribe sin dato.",
         "after": "Armá la planilla:"},
        {"file": "19-paso4.svg", "step": 4,
         "alt": "Seis tarjetas de versiones con sufijo: R29S una cámara sin Bluetooth; R29C-L LTE sin PoE; R29C-T lector de huella; R20K-L LTE; X915P y E16P venas de la palma; X915 HID iClass o Prox con lector HID.",
         "caption": "El sufijo cambia la fuente o las credenciales: cada versión va marcada en la planilla.",
         "after": "Marcá en otro color las versiones"},
    ],
    "concepts": [
        {"name": "Vigente contra parque instalado",
         "para_que": "En las paredes hay modelos de varias generaciones, y no todos se venden hoy. Separar lo vigente de lo instalado evita cotizar algo que ya no se consigue o decirle a un cliente que su equipo no tiene soporte sin saberlo.",
         "como": "Vigente es lo que está en el menú de productos de akuvox.com el día que cotizás. Lo que aparece en tablas de la Knowledge Base pero no en el menú (E11, C315, IT83) es parque instalado. No hay lista oficial de discontinuados en lo leído, así que antes de decirle algo al cliente se consulta al distribuidor.",
         "ejemplo": "Un consorcio de la Aguada pide reponer un C315 roto. No está en el menú: la propuesta ofrece un monitor vigente y aclara que el C315 se consulta con el distribuidor, en vez de decir que está discontinuado."},
        {"name": "Tablas transversales de la Knowledge Base",
         "para_que": "Las fichas de producto no siempre están, y cuando están no siempre traen todo. Akuvox publica tablas que cruzan toda la línea: alimentación, carga del relé, salida de 12 V, métodos de acceso e interfaces de monitores.",
         "como": "La planilla toma PoE de la tabla de alimentación, el relé de la tabla de carga resistiva y las credenciales de la tabla de métodos de acceso. Si un dato no aparece, se escribe \"sin dato\": suponerlo es la forma más rápida de cotizar mal.",
         "ejemplo": "Para una obra en Maldonado, la planilla muestra que el E16C es 802.3af y su relé 30 V 2 A: el switch del rack alcanza y la cerradura va con fuente propia."},
        {"name": "Sufijos de versión",
         "para_que": "Un mismo modelo sale en versiones con funciones distintas, y la letra del final es lo único que las distingue en un pedido.",
         "como": "En la planilla, cada versión va en su fila y marcada en otro color si cambia funciones: -L es LTE (el R29C-L no acepta PoE), -T huella, P palma (X915P, E16P), HID para lectores HID en el X915.",
         "ejemplo": "Un pedido que dice solo \"R29C\" para un portón sin cableado de datos debería decir R29C-L, y llevar fuente de 12 V 1,5 A porque esa versión no arranca por PoE."},
    ],
    "teoria_md": """### Un poco de historia

Akuvox ordena su menú de productos por tipo: porteros, monitores interiores, el panel AKClaw, casa inteligente, cuidado de mayores, 2 hilos, kits, control de acceso, un teléfono de video Android, teléfonos IP, una cámara IP, software y accesorios. Esa organización es la foto del catálogo al 27 de octubre de 2026, el día en que se guardaron las páginas para este curso.

Al mismo tiempo, la Knowledge Base conserva tablas con modelos que ya no están en el menú: E11, C315, IT83, C310, R27. Son equipos que siguen funcionando en edificios y que vas a encontrar en soporte. El caso del E11 es conocido: en 2023 Claroty publicó 13 vulnerabilidades en ese modelo y CISA emitió un aviso con puntaje 9,8. Es un buen recordatorio de que el parque instalado necesita tanta atención como lo nuevo.

Una sorpresa del relevamiento: el E16 y el C316 siguen en el menú, aunque uno podría suponer que no.

### Cómo funciona

El catálogo se lee con tres fuentes, cada una con su rol:

- **El menú de akuvox.com** dice qué se vende hoy y en qué versiones.
- **Las tablas de la Knowledge Base** dan los datos que cruzan toda la línea: alimentación y PoE, carga del relé, salida de 12 V, métodos de acceso e interfaces.
- **Las fichas de producto**, cuando existen, dan datos propios de cada modelo, como el grado IP e IK.

Para el instalador, el criterio más rápido para ubicar un portero es cómo llama. Un botón llama a un solo destino: casa u oficina chica. Teclado o varios botones (con módulos de nombres como MD06 o MD12) llaman a varios destinos. Una pantalla táctil suma rostro, QR y directorio, y los Android grandes de las series S y X apuntan al acceso principal de un edificio de categoría. Es una orientación para arrancar; la decisión final la dan la obra y la ficha.

El sufijo cambia funciones. En el R29: S una cámara, C doble cámara y Bluetooth, C-L con LTE (sin PoE), C-T con huella. En el X915 hay versiones HID y la X915P con palma. El número de firmware también identifica: el primer bloque es el código del modelo (29 para R29, 915 para X915, 320 para el R20 versión 5) y por eso la planilla se completa mirando la web del equipo, no solo la etiqueta."""
}

# =============================================================== 20
M["20"] = {
    "fig": {"file": "20.svg",
            "alt": "Dos porteros Android genéricos, S539 de 10 pulgadas y S538 Tri-Vision, con la etiqueta acceso principal de edificio. Una grilla compara: ambos con PIN, tarjeta 13,56 y 125 kHz, rostro, Bluetooth y QR, relé 30 V 3 A y PoE 802.3at; S539 con fuente 12 V 3 A o 24 V 1,5 A y 12 V de 1 A por el relé; S538 con fuente 24 V 2 A y borne propio de 12 V 500 mA.",
            "caption": "Las credenciales son las mismas; lo que cambia es la fuente y de dónde salen los 12 V."},
    "steps": [
        {"file": "20-paso1.svg", "step": 1,
         "alt": "Cuatro pantallas en secuencia: 9999 más Dial, 3888 más OK, System Info y, en el S539, Network con la IP. Notas: el firmware empieza con 539. o 538. y el tercer bloque 10 o más indica alta seguridad.",
         "caption": "9999, 3888 y System Info: el mismo camino sirve en S539, S538, S535, X915, X916 y R29.",
         "after": "Sacá la IP: en la pantalla"},
        {"file": "20-paso3.svg", "step": 3,
         "alt": "Un switch PoE con puertos 802.3at conectados a un S539 y a un S538. Debajo, las alternativas: S539 PoE+ 802.3at o fuente 12 V 3 A o 24 V 1,5 A; S538 PoE 802.3at o fuente 24 V 2 A, y la versión para frío solo con fuente de 24 V 2 A o más.",
         "caption": "Antes de ir a obra, el puerto del switch tiene que dar 802.3at.",
         "after": "Revisá el puerto del switch"},
        {"file": "20-paso4.svg", "step": 4,
         "alt": "Dos paneles. S539: la cerradura toma 12 V hasta 1 A por el relé solo con fuente de 24 V 2,5 A o más; con PoE solo no hay salida. S538: la cerradura toma 12 V hasta 500 mA de un borne propio, independiente del relé.",
         "caption": "S539 da 12 V por el relé solo con fuente de 24 V; S538 tiene borne propio de 500 mA.",
         "after": "la cerradura se alimenta desde el"},
    ],
    "concepts": [
        {"name": "PoE 802.3at (PoE+)",
         "para_que": "Un portero Android con pantalla grande consume más de lo que da un puerto PoE común. 802.3at, conocido como PoE+, nació para alimentar equipos de más consumo por el mismo cable de datos.",
         "como": "S539 y S538 piden 802.3at. Antes de la obra se revisa que el switch dé at en ese puerto y que el presupuesto de potencia del switch alcance; si no, se alimentan con fuente: S539 12 V 3 A o 24 V 1,5 A, S538 24 V 2 A.",
         "ejemplo": "En un edificio nuevo en Punta Carretas, el switch de la sala técnica solo daba 802.3af. El S539 del hall se alimentó con una fuente de 24 V hasta que se cambió el switch."},
        {"name": "Salida de 12 V por el relé o borne propio",
         "para_que": "Algunos porteros pueden alimentar una cerradura chica o un relé externo sin fuente aparte. Ahorra un equipo, pero tiene límites de corriente y condiciones de alimentación.",
         "como": "El S539 da 12 V hasta 1 A por el relé, solo si él mismo se alimenta con fuente de 24 V 2,5 A o más. El S538 tiene un borne de 12 V propio de 500 mA, independiente del relé. Si la cerradura pide más, fuente propia.",
         "ejemplo": "Una cerradura de 12 V que consume 300 mA en una puerta de servicio puede colgar del borne del S538; un electroimán de 600 mA no, y va con su fuente."},
        {"name": "Versión para frío del S538",
         "para_que": "Para climas muy fríos existe una versión del S538 resistente al frío. Su consumo cambia y Akuvox la deja solo con alimentación externa.",
         "como": "Va solo con fuente de 24 V 2 A o más: nada de PoE. En Uruguay es raro encontrarla, pero si llega una a obra, la fuente tiene que estar en el pedido.",
         "ejemplo": "Un cliente importa por su cuenta un S538 para frío para una estancia en Tacuarembó; el técnico revisa la etiqueta, ve la versión y lleva una fuente de 24 V en vez de contar con el switch."},
    ],
    "teoria_md": """### Un poco de historia

Power over Ethernet llegó como estándar en 2003 con IEEE 802.3af: hasta 15,4 W en el puerto del switch y unos 12,95 W disponibles en el equipo, suficiente para teléfonos IP y cámaras. Cuando aparecieron equipos con más consumo, en 2009 se publicó IEEE 802.3at, conocido como PoE+, con hasta 30 W en el puerto y 25,5 W en el equipo. En 2018, IEEE 802.3bt subió todavía más el techo usando los cuatro pares.

Los porteros siguieron ese camino. Un portero de botón o teclado vive cómodo con 802.3af; un portero Android con pantalla grande, cámara y lectores necesita PoE+. Por eso en la serie S de Akuvox los Android de punta, S539 y S538, piden 802.3at.

### Cómo funciona

En PoE, el switch (PSE) primero detecta si del otro lado hay un equipo compatible (PD) y qué clase de potencia pide; recién ahí entrega energía. Si el puerto solo es af y el equipo necesita at, puede no arrancar o reiniciarse cuando sube el consumo. Por eso la lección pide revisar el puerto antes de ir: no alcanza con que diga PoE.

Los datos de esta lección vienen de las tablas de Akuvox:

- **S539**: Android, 10", IP66 según la guía. PoE+ 802.3at, o fuente de 12 V 3 A o 24 V 1,5 A.
- **S538**: presentado como Tri-Vision. PoE 802.3at o fuente de 24 V 2 A. La versión para frío, solo fuente de 24 V 2 A o más.

Los dos aceptan PIN, tarjeta de 13,56 MHz y 125 kHz, rostro, Bluetooth y QR, con relé de 30 V 3 A.

La diferencia práctica está en los 12 V para la cerradura. El S539 los saca por el relé, hasta 1 A, pero solo si él se alimenta con una fuente de 24 V 2,5 A o más: con PoE no hay salida. El S538 tiene un borne de 12 V propio de 500 mA, que no ocupa el relé.

La regla de la lección 4 sigue valiendo: cuando la cerradura pide más de lo que da la salida, o es la puerta principal de un edificio, va con fuente propia y el relé del portero solo conmuta. Para entrar a estos equipos: `9999` + Dial, `3888` + OK y `System Info`."""
}

# =============================================================== 21
M["21"] = {
    "fig": {"file": "21.svg",
            "alt": "Panel S535 (Linux, 5 pulgadas, IP66) con un portero genérico y cuatro módulos opcionales: huella, LTE, lector QR y lazo de inducción. Panel S532 de 2,8 pulgadas con sus versiones estándar, IP y lazo de inducción. Debajo, una grilla: S535 con rostro y QR, relé 30 V 2 A y 12 V hasta 1 A por el relé; S532 sin rostro ni QR, relé 30 V 3 A y 12 V de 500 mA solo con fuente.",
            "caption": "El S535 se completa con módulos; el S532 se elige por versión."},
    "steps": [
        {"file": "21-paso1.svg", "step": 1,
         "alt": "Hoja de pedido para un edificio con huella y LTE: 1 S535 frente, 1 módulo de huella, 1 módulo LTE, alimentación PoE+ o fuente 12 V hasta 4 A, cerradura hasta 12 V 1 A por el relé. Al lado, el frente con los dos módulos y un aviso: si el pedido dice solo S535, llega sin módulos.",
         "caption": "Cada módulo es una línea del pedido.",
         "after": "Armá el pedido de un S535"},
        {"file": "21-paso2.svg", "step": 2,
         "alt": "Dos paneles. Rojo: S532 alimentado solo por PoE+, anda pero sin salida de 12 V. Verde: S532 con fuente de 12 V 2,5 A, entrega 12 V a una cerradura de hasta 500 mA.",
         "caption": "En el S532, la salida de 12 V existe solo con fuente de 12 V 2,5 A.",
         "after": "Para un S532 con cerradura"},
        {"file": "21-paso3.svg", "step": 3,
         "alt": "Dos secuencias de pantallas. S535: 9999 más Dial, 3888 más OK, System Info. S532: *2396# y luego 1, igual que R28 y R27.",
         "caption": "S535 se entra como el R29; S532 como el R28.",
         "after": "Anotá cómo se entra a cada uno"},
    ],
    "concepts": [
        {"name": "Portero modular",
         "para_que": "Un mismo frente sirve para obras distintas si las funciones extra se suman como módulos. Así no hace falta un modelo distinto para cada combinación de huella, LTE, QR o lazo de inducción.",
         "como": "El S535 se lista con unidades de huella, LTE, lector QR y lazo de inducción. En el pedido va el frente más cada módulo como línea aparte. La alimentación del conjunto: PoE+ o fuente de 12 V hasta 4 A.",
         "ejemplo": "Una cooperativa de viviendas en el Cerro quiere huella y un respaldo LTE por si se corta la fibra: el pedido lleva S535, módulo de huella y módulo LTE. Si dice solo S535, llega el frente pelado."},
        {"name": "Lazo de inducción",
         "para_que": "Permite que una persona con audífono escuche el portero sin acoplar el sonido por el aire: el audio llega por un campo magnético que el audífono capta con su bobina (telebobina).",
         "como": "En el S535 es un módulo; en el S532 y el R28, una versión del equipo. Se pide cuando el pliego o el cliente lo requieren por accesibilidad.",
         "ejemplo": "En el acceso a un centro de salud en Paysandú, el pliego pide accesibilidad auditiva: el S532 en versión con lazo de inducción cumple sin sumar un equipo aparte."},
        {"name": "La salida de 12 V del S532",
         "para_que": "El S532 puede alimentar una cerradura chica, pero solo si él tiene energía de sobra. Con PoE anda el portero, no la salida.",
         "como": "Para usar su salida de 12 V (500 mA), el S532 va con fuente de 12 V 2,5 A o más. El S535 da hasta 1 A por el relé con PoE+ o fuente de 12 V 2 A. Por encima de esos valores, la cerradura va con su propia fuente.",
         "ejemplo": "Un técnico deja un S532 solo con PoE en un consultorio de Salto y la cerradura no abre. Con una fuente de 12 V 2,5 A la salida aparece; mejor todavía, la cerradura con su fuente y el relé solo conmutando."},
    ],
    "teoria_md": """### Un poco de historia

La serie S de Akuvox tiene dos mundos: los Android grandes (S539, S538) y los Linux (S535, S532). Linux en un portero suele significar un equipo más acotado en funciones, sin apps de terceros, pero estable y con menos consumo. La guía de selección marca justamente eso: los Android admiten apps de terceros y los Linux no.

El S535 introduce una idea que en la industria ya era común en porteros de edificio: el frente modular. En vez de fabricar una versión para cada combinación, se arma un frente base y se le suman unidades. Akuvox lista cuatro para el S535: huella, LTE, lector QR y lazo de inducción.

El lazo de inducción tiene una historia larga: las bobinas para audífonos (telebobinas) se usan desde mediados del siglo XX y los sistemas de lazo están normalizados por IEC 60118-4. En un portero, el lazo hace que el audio llegue directo al audífono sin ruido de calle.

### Cómo funciona

**S535**: Linux, 5", aluminio, IP66 y Wiegand según la guía de selección. Acepta PIN, tarjetas de 13,56 MHz y 125 kHz, rostro, Bluetooth, QR y huella como opción. Relé de 30 V 2 A. Alimentación por PoE+ o fuente de 12 V hasta 4 A. Puede dar 12 V hasta 1 A por el relé con PoE+ o fuente de 12 V 2 A.

**S532**: 2,8", en versiones estándar, IP y lazo de inducción. PIN, tarjetas y Bluetooth, sin rostro ni QR. Relé de 30 V 3 A. PoE+ o fuente de 12 V 2 A, pero su salida de 12 V (500 mA) pide fuente de 12 V 2,5 A. No figura en la guía de selección, así que sus datos salen de las tablas.

La consecuencia práctica es de pedido y de fuente. El S535 se cotiza por módulos: cada uno es una línea del presupuesto. El S532 con cerradura colgando de su salida necesita fuente, aunque el switch dé PoE+.

También cambia cómo se entra al menú. El S535 va como los Android: `9999` + Dial, `3888` + OK, `System Info`. El S532 va como el R28 y el R27: `*2396#` y después `1`. Tener eso anotado en la ficha ahorra la primera media hora en obra."""
}

# =============================================================== 22
M["22"] = {
    "fig": {"file": "22.svg",
            "alt": "Dos porteros genéricos: X916 de 13 pulgadas con cámara Starlight y X915 de 8 pulgadas, con la etiqueta edificio de categoría. Grilla: X916 versiones estándar y LTE, relé 30 V 5 A, PoE+, fuente 12 V 4 A o 24 V 2 A, 12 V de 500 mA; X915 versiones estándar, HID y palma, relé 30 V 3 A, PoE+, fuente 24 V 2 A, 12 V de 1 A. Los dos piden fuente de 24 V 2,5 A para la salida de 12 V, con excepción del X915 V2.",
            "caption": "El X916 tiene el relé más fuerte de la línea; la salida de 12 V en los dos pide fuente de 24 V."},
    "steps": [
        {"file": "22-paso3.svg", "step": 3,
         "alt": "Dos documentos: la guía de selección dice IP65 para el X915 y la ficha X915 V2.0 dice IP66 e IK10. Una flecha verde lleva el dato de la ficha a la planilla, con la fuente anotada: ficha X915 V2.0.",
         "caption": "Ante dos datos distintos, al pliego va la ficha de la versión exacta.",
         "after": "Buscá en la ficha de esa versión"},
        {"file": "22-paso4.svg", "step": 4,
         "alt": "Árbol de decisión: ¿cerradura desde el portero? No: PoE+ 802.3at alcanza. Sí: fuente de 24 V 2,5 A o más. Excepción: X915 V2 con hardware 2915.1.0.8 a 2915.1.0.13 y firmware 2915.30.10.228 o más, la salida de 12 V anda también con PoE.",
         "caption": "La cerradura desde el portero decide la fuente; el X915 V2 tiene una excepción por hardware y firmware.",
         "after": "Decidí la alimentación:"},
    ],
    "concepts": [
        {"name": "Grado IP",
         "para_que": "Dice cuánto protege el gabinete contra polvo y agua, con un código normalizado que se puede exigir en un pliego.",
         "como": "El primer dígito es polvo (6 es hermético) y el segundo agua: 5 chorros de agua, 6 chorros potentes. La guía de selección dice IP65 para X916 y X915; la ficha del X915 V2.0 dice IP66. Se cita la ficha de la versión que se compra.",
         "ejemplo": "Un pliego para un edificio frente a la rambla en Pocitos pide IP66 por el agua con viento: el X915 V2.0 cumple según su ficha, y en la propuesta se cita \"ficha X915 V2.0\", no la guía."},
        {"name": "Grado IK",
         "para_que": "Mide la resistencia a golpes, es decir, al vandalismo. Un frente de calle con IK alto aguanta mejor un golpe con objeto contundente.",
         "como": "La escala va de IK00 a IK10; IK10 soporta un impacto de 20 joules. La ficha del X915 V2.0 declara IK10. Como con el IP, el dato sale de la ficha de la versión.",
         "ejemplo": "En un acceso de complejo con antecedentes de roturas en Las Piedras, el pliego exige IK10: el X915 V2.0 lo declara; el R29 publica IK06."},
        {"name": "Versiones del X915 y relé del X916",
         "para_que": "El X915 se adapta a sistemas de credenciales existentes y a biometría; el X916 apunta a accesos grandes y con poca luz.",
         "como": "X915: estándar, HID iClass, HID Prox y X915P con venas de la palma, relé 30 V 3 A. X916: 13\", cámara Starlight, versiones estándar y LTE, y relé de 30 V 5 A, el más fuerte de la línea.",
         "ejemplo": "Una empresa en Zonamerica ya tiene tarjetas HID Prox: el X915 en versión HID Prox lee las mismas tarjetas y evita recambiar credenciales."},
    ],
    "teoria_md": """### Un poco de historia

Los códigos IP (Ingress Protection) los define la norma IEC 60529 y se usan en todo el mundo para equipos eléctricos. El código IK, para resistencia a impactos mecánicos, lo define IEC 62262, publicada en 2002; antes de ella, ese dato se daba como un tercer dígito agregado al IP, lo que generaba confusión.

Las dos escalas importan en un portero de calle, que vive bajo lluvia, sol y, a veces, golpes. Por eso los pliegos de edificios de categoría piden valores mínimos de IP e IK, y por eso un número mal citado puede dejar una propuesta fuera.

En Akuvox pasa algo que conviene tener presente: dos páginas del mismo fabricante no coinciden. La guía de selección dice IP65 para el X915, y la ficha del X915 V2.0 dice IP66 e IK10. Ninguna fuente leída explica la diferencia; la regla práctica es citar la ficha de la versión exacta.

### Cómo funciona

**Código IP**: dos dígitos. El primero, sólidos (6 es hermético al polvo). El segundo, agua: 5 resiste chorros de agua, 6 chorros potentes. IP65 e IP66 son ambos herméticos al polvo; cambia la fuerza del agua que soportan.

**Código IK**: un número de 00 a 10 que indica la energía de impacto que soporta el gabinete. IK06 corresponde a 1 joule; IK10, a 20 joules, el valor más alto de la escala. El R29 publica IK06; el X915 V2.0, IK10.

Los dos Android de acero de esta lección:

- **X916**: 13", cámara Starlight para poca luz, versiones estándar y LTE, relé de 30 V 5 A. PoE+, o fuente de 12 V 4 A o 24 V 2 A. Salida de 12 V de 500 mA.
- **X915**: 8", versiones estándar, HID iClass, HID Prox y X915P con palma, relé de 30 V 3 A. PoE+ o fuente de 24 V 2 A. Salida de 12 V de 1 A.

Para usar la salida de 12 V, ambos piden fuente de 24 V 2,5 A o más. La excepción es el X915 V2 con hardware 2915.1.0.8 a 2915.1.0.13 y firmware 2915.30.10.228 o más, que la entrega también con PoE. Como el X915 tiene dos versiones de hardware, se lee en la web antes de decidir la fuente."""
}

# =============================================================== 23
M["23"] = {
    "fig": {"file": "23.svg",
            "alt": "Dos porteros genéricos: X912 con pantalla táctil de acero y X910 de un botón. Grilla: X912 con PIN, tarjetas 13,56 y 125 kHz, rostro, Bluetooth y QR, relé 30 V 3 A, PoE+, 12 V de 1 A con PoE+ o fuente 12 V 2,5 A; X910 sin PIN ni rostro, solo 13,56 MHz, Bluetooth y QR, relé 30 V 2 A, PoE 802.3af o 12 a 24 V, 12 V de 600 mA con PoE+ o fuente 12 V 2 A.",
            "caption": "El X910 anda con PoE af, pero su salida de 12 V pide PoE+ o fuente."},
    "steps": [
        {"file": "23-paso1.svg", "step": 1,
         "alt": "X912: secuencia de pantallas ícono de llave, 2396 y Dial, que muestra la IP. X910: se mantiene el botón 5 segundos y el equipo anuncia la IP en voz alta.",
         "caption": "El X912 muestra la IP con 2396 y Dial; el X910 la dice en voz alta.",
         "after": "ícono de llave o teclado"},
        {"file": "23-paso4.svg", "step": 4,
         "alt": "Dos paneles. En vacío, un tester conectado a la salida del portero marca 12 V y puede engañar. Con la cerradura de banco conectada y el tester en paralelo, se lee la tensión durante la apertura hecha desde la web.",
         "caption": "La tensión que vale es la que se mide con la cerradura conectada, al abrir.",
         "after": "Conectá una cerradura de banco"},
    ],
    "concepts": [
        {"name": "Medir con carga",
         "para_que": "Una fuente débil puede mostrar la tensión nominal sin carga y caerse cuando la cerradura pide corriente. Medir en vacío da un falso positivo.",
         "como": "Se conecta la cerradura de banco a la salida de 12 V, se pone el tester en paralelo con la cerradura y se abre desde la web: la lectura que vale es la de ese momento. Si cae, se cambia la alimentación del portero según la tabla o la cerradura pasa a fuente propia.",
         "ejemplo": "En un local de 18 de Julio, el X910 con PoE af marcaba 12 V en vacío y la cerradura no abría. Con el tester durante la apertura se vio la caída; pasando a PoE+ quedó resuelto."},
        {"name": "Un botón con detección de paquetes",
         "para_que": "Akuvox presenta al X910 como portero de un botón con detección de paquetes: pensado para la puerta de una casa o un local donde llegan entregas.",
         "como": "Sin pantalla ni PIN; tarjeta de 13,56 MHz, Bluetooth y QR. IP66 según la guía. La IP se pide manteniendo el botón 5 s, y el firmware empieza con `2910.`.",
         "ejemplo": "Una casa en Atlántida con muchas compras por internet: el X910 en la puerta, con QR para el delivery habitual y tarjeta para la familia."},
        {"name": "X912 antivandálico",
         "para_que": "Frente de acero y pantalla táctil para lugares donde el portero se expone a golpes, manteniendo rostro, QR y PIN.",
         "como": "Linux, IP65 y Wiegand según la guía, en versión estándar o con teclado físico. Se entra con el ícono de llave, `2396` y Dial. Da 12 V hasta 1 A por el relé con PoE+ o fuente de 12 V 2,5 A, y lee patentes Hikvision desde 912.30.12.114.",
         "ejemplo": "Para el acceso peatonal de un estacionamiento en el Centro, el X912 con teclado físico permite PIN aunque el usuario tenga guantes, y su frente de acero soporta mejor el maltrato."},
    ],
    "teoria_md": """### Un poco de historia

La serie X de Akuvox reúne los porteros de acero. Dentro de ella hay dos Android (X916, X915) y dos Linux (X912, X910). Esta lección mira los Linux, que resuelven problemas muy distintos: el X912 es el antivandálico con pantalla táctil, y el X910 es un portero de un botón que Akuvox presenta con detección de paquetes, una respuesta al crecimiento de las compras con entrega a domicilio.

La pregunta que une a los dos es eléctrica: cuánta corriente pueden dar a una cerradura y con qué alimentación. Es la misma pregunta que se repite en todo el catálogo, porque PoE tiene un presupuesto de potencia limitado: 802.3af entrega unos 12,95 W al equipo y 802.3at (PoE+) unos 25,5 W.

### Cómo funciona

Cuando un portero alimenta la cerradura, la energía sale de su propia alimentación. Si esa alimentación es justa, todo anda hasta el momento en que la cerradura pide corriente: ahí la tensión cae. Por eso la tabla de 12 V de Akuvox pone condiciones de alimentación a cada salida.

- **X912**: 12 V hasta 1 A por el relé, con PoE+ o fuente de 12 V 2,5 A.
- **X910**: 12 V hasta 600 mA por el relé, con PoE+ o fuente de 12 V 2 A. Con PoE af, el equipo anda pero esa salida no alcanza.

La medición correcta se hace con carga. En vacío, un tester mide la tensión sin que circule corriente: cualquier fuente parece buena. Con la cerradura conectada y el tester en paralelo, la lectura durante la apertura muestra la tensión real que recibe la cerradura. Si cae, se corrige la alimentación del portero o se pasa la cerradura a fuente propia.

Credenciales: el X912 acepta PIN, tarjetas de 13,56 MHz y 125 kHz, rostro, Bluetooth y QR, con relé de 30 V 3 A. El X910 no tiene PIN ni rostro, lee solo 13,56 MHz y suma Bluetooth y QR, con relé de 30 V 2 A.

Acceso al menú: en el X912, ícono de llave o teclado, `2396` (el PIN de sistema de fábrica) y Dial. En el X910, se mantiene el botón 5 s y el equipo anuncia su IP en voz alta. El firmware empieza con `912.` o `2910.`."""
}

# =============================================================== 24
M["24"] = {
    "fig": {"file": "24.svg",
            "alt": "Cuatro porteros genéricos lado a lado. R29S: una cámara, sin Bluetooth, PoE 802.3at, la tabla no lista fuente. R29C: dos cámaras, Bluetooth, PoE at o 12 V 2,5 A. R29C-L resaltado en rojo: dos cámaras, LTE, sin PoE, fuente de 12 V 1,5 A, con el switch solo no arranca. R29C-T: dos cámaras, huella en lugar de QR, PoE af o 12 V 1,5 A. Abajo: todas con tarjetas 13,56 y 125 kHz, relé 30 V 3 A, IP65 e IK06, Android de 7 pulgadas.",
            "caption": "La letra de la versión decide la fuente y las credenciales del R29."},
    "steps": [
        {"file": "24-paso3.svg", "step": 3,
         "alt": "Dos paneles. Rojo: R29C-L conectado solo a un switch PoE 802.3at, no acepta PoE y queda apagado. Verde: R29C-L con fuente de 12 V 1,5 A, arranca. Nota: en la lista de obra va con fuente y con el soporte de pared R29C-L.",
         "caption": "El R29C-L no arranca por PoE: la fuente de 12 V 1,5 A va en la lista de obra.",
         "after": "Completá la lista de obra"},
        {"file": "24-paso4.svg", "step": 4,
         "alt": "Corte de pared con dos montajes dibujados de forma genérica. De superficie: portero sobre soporte de pared con cubierta de lluvia arriba. Embutido: portero dentro de una caja en la pared, con soporte para embutir y cubierta de lluvia.",
         "caption": "Cubierta de lluvia y soporte se eligen según el montaje, en negro o plata.",
         "after": "Elegí cubierta de lluvia y soporte"},
    ],
    "concepts": [
        {"name": "Versiones del R29",
         "para_que": "El R29 es la base de muchos ejemplos de Akuvox, y sale en cuatro versiones para adaptarse a obras distintas: más simple, con Bluetooth, con LTE o con huella.",
         "como": "R29S una cámara y sin Bluetooth; R29C doble cámara y Bluetooth; R29C-L con LTE; R29C-T con huella (cambia QR por huella). Todas leen tarjetas de 13,56 y 125 kHz. La versión se identifica en la etiqueta antes de armar la lista de obra.",
         "ejemplo": "Para una chacra en Canelones sin fibra hasta la tranquera, el R29C-L con LTE evita tirar datos hasta el portón; solo hace falta energía."},
        {"name": "LTE sin PoE",
         "para_que": "La versión LTE existe para lugares sin red cableada, y por eso Akuvox no la alimenta por PoE: necesita fuente.",
         "como": "La tabla de alimentación marca que el R29C-L no admite PoE y va con fuente de 12 V 1,5 A. En la lista de obra va la fuente y el soporte de pared R29C-L.",
         "ejemplo": "Un técnico instala un R29C-L contando con el switch del cliente y no arranca. Con la fuente de 12 V 1,5 A que debería haber estado en la lista, el problema desaparece."},
        {"name": "Montaje y accesorios",
         "para_que": "Un portero de calle necesita protección contra lluvia directa y una fijación adecuada a la pared o a la caja embutida.",
         "como": "Según la ficha, el R29 admite montaje de superficie o embutido, con cubiertas de lluvia y soportes para pared y embutir, en negro o plata. El R29C-L lleva su soporte de pared propio. Con IK06, en lugares con riesgo de golpe conviene comparar con el pliego.",
         "ejemplo": "En la fachada de un edificio nuevo en Parque Batlle, el arquitecto quiere el portero al ras: se pide el soporte para embutir y la cubierta de lluvia en plata para que combine."},
    ],
    "teoria_md": """### Un poco de historia

El R29 es, según la ficha de Akuvox, un portero Android con pantalla táctil de 7", frente de aluminio, montaje de superficie o embutido, IP65 e IK06. Aparece en buena parte de las guías del fabricante como modelo de ejemplo: la apertura por HTTP, la HTTP API y la integración con cámaras de patentes se explican con un R29.

Su historia en este curso es la de las versiones. El mismo nombre se vende en cuatro variantes, y una de ellas, la de LTE, tiene una restricción de alimentación que no se ve a simple vista. LTE es la tecnología celular 4G estandarizada por 3GPP en su Release 8 de 2008; en un portero sirve para dar conectividad donde no llega la red cableada.

### Cómo funciona

Las cuatro versiones:

- **R29S**: una cámara, sin Bluetooth. PoE 802.3at; la tabla no lista fuente.
- **R29C**: doble cámara y Bluetooth. PoE 802.3at o fuente de 12 V 2,5 A (fila "R29" de la tabla).
- **R29C-L**: doble cámara y LTE. No admite PoE: solo fuente de 12 V 1,5 A.
- **R29C-T**: doble cámara y huella. PoE 802.3af o fuente de 12 V 1,5 A.

Todas leen tarjetas de 13,56 MHz y 125 kHz. En credenciales, el R29C acepta PIN, tarjeta, rostro, Bluetooth y QR; el R29CT cambia QR por huella; el R29S no tiene Bluetooth. El relé soporta 30 V 3 A y la versión de hardware V1.1 da 12 V 500 mA por el relé.

Un dato que viene de la parte de HTTP: desde el firmware 29.30.10.745, el R29 abre leyendo patentes de cámaras Hikvision y Dahua por la HTTP API.

Para entrar: `9999` + Dial, `3888` + OK, `System Info`. En la web, el firmware aparece como `29.x.y.z` en `Status > Basic > Product Information`; el primer bloque, 29, es el código del modelo.

El montaje cierra la lista de obra. La ficha ofrece cubiertas de lluvia y soportes de pared y para embutir, en negro o plata. El grado IK06 es el que publica la ficha: alcanza para un hall o un acceso controlado, pero si el pliego pide más resistencia al impacto, la serie X de acero tiene fichas con IK más alto."""
}

# =============================================================== 25
M["25"] = {
    "fig": {"file": "25.svg",
            "alt": "Tres porteros genéricos: R28 con pantalla de 4,3 pulgadas no táctil y teclado, R25A de un botón y R25K con teclado. Grilla: R28 con PIN, tarjetas 13,56 y 125 kHz, relé 30 V 3 A, PoE af o 12 V 1 A, salida de 12 V 400 mA por borne propio que funciona con PoE; R25 sin PIN según la tabla, relé 30 V 2 A, salida de 12 V 400 mA por el relé que con PoE depende del volumen.",
            "caption": "El R28 tiene 12 V propios; el R25 no promete PIN y su salida con PoE depende del volumen."},
    "steps": [
        {"file": "25-paso1.svg", "step": 1,
         "alt": "Tres paneles: R28 con *2396# y después 1; R25A manteniendo el botón 5 segundos; R25K con *3258*, como el R20K. Nota: el firmware empieza con 28. o 228. y 25.",
         "caption": "Cada modelo pide la IP a su manera.",
         "after": "R25A manteniendo el botón 5 s"},
        {"file": "25-paso3.svg", "step": 3,
         "alt": "Switch PoE 802.3af conectado a un R25A; la salida de 12 V por el relé alimenta una carga de banco con un tester en paralelo. Una tabla para anotar la tensión durante la apertura con volumen bajo y alto.",
         "caption": "Con PoE, la salida del R25 cambia con el volumen: medilo con los dos ajustes.",
         "after": "conectá una carga de banco a la salida"},
        {"file": "25-paso4.svg", "step": 4,
         "alt": "Opción 1: fuente de 12 V 1 A para el R25 y la cerradura por el relé. Opción 2, en verde: el R25 con PoE y su relé como contacto seco; la fuente de la cerradura va a COM, NO va al positivo de la cerradura y el negativo de la cerradura vuelve a la fuente.",
         "caption": "En obra, la cerradura con su fuente y el relé del R25 solo conmutando.",
         "after": "Si la caída afecta a la cerradura"},
    ],
    "concepts": [
        {"name": "Borne de 12 V propio",
         "para_que": "Tener una salida de 12 V que no pasa por el relé permite alimentar un accesorio sin ocupar el contacto que abre.",
         "como": "El R28 tiene un borne independiente de 12 V 400 mA que funciona con PoE o con fuente. Se conecta entre la salida de alimentación y GND, sin tocar el relé.",
         "ejemplo": "En un edificio chico de La Blanqueada, el R28 alimenta desde su borne un relé auxiliar de 12 V y su relé queda libre para la cerradura con su propia fuente."},
        {"name": "La salida que depende del volumen",
         "para_que": "En el R25 con PoE, la energía disponible se reparte. Akuvox avisa que la salida de 12 V se ve afectada por el ajuste de volumen del equipo.",
         "como": "Se pide firmware 25.30.10.11 o más para usar la salida con PoE. En banco se mide la tensión durante la apertura con volumen bajo y alto; si cae, fuente de 12 V 1 A para el portero o fuente propia para la cerradura.",
         "ejemplo": "Un R25A en una oficina de la Ciudad Vieja abre bien en la prueba de la tarde y falla de noche, cuando el encargado subió el volumen. La solución estable: la cerradura con su fuente."},
        {"name": "No prometer PIN en un R25",
         "para_que": "El nombre R25K sugiere teclado, y de hecho la IP se consulta marcando como en el R20K. Pero la tabla de métodos de acceso marca a toda la serie R25 sin PIN.",
         "como": "En la propuesta se ofrecen tarjetas de 13,56 y 125 kHz para el R25. Si el cliente necesita PIN, se elige un R28 o un R20K, que sí lo tienen según la tabla, o se prueba en el modelo real antes de comprometerlo.",
         "ejemplo": "Un consorcio en el Prado quiere que los proveedores entren con código: en vez del R25K que tenía en mente, la propuesta lleva un R20K."},
    ],
    "teoria_md": """### Un poco de historia

La serie R de Akuvox tiene porteros compactos de aluminio que se instalan mucho en edificios chicos y oficinas. El R28 suma una pequeña pantalla de 4,3" no táctil; los R25 vienen en versión de un botón (R25A) y R25K. Comparten con el resto de la serie el trabajo con Linux, IP65 y Wiegand según la guía de selección.

Wiegand es una interfaz con historia: toma el nombre del efecto Wiegand, descubierto por John Wiegand, y se volvió el estándar de hecho para conectar lectores de tarjetas a controladoras de acceso con dos líneas de datos. Que un portero tenga Wiegand significa que puede entregar lo que lee a otra controladora, o recibir un lector externo.

### Cómo funciona

**R28**: pantalla de 4,3" no táctil, PIN y tarjetas de 13,56 MHz y 125 kHz, relé de 30 V 3 A. PoE 802.3af o fuente de 12 V 1 A. Tiene un borne independiente de 12 V 400 mA que funciona con PoE o con fuente: la tabla de Akuvox explica que en estos equipos alcanza con conectar la carga entre la salida de alimentación y GND. Tiene dos versiones de hardware; el firmware empieza con `28.` o `228.`.

**R25A y R25K**: relé de 30 V 2 A, PoE 802.3af o fuente de 12 V 1 A. La tabla de métodos de acceso marca la serie sin PIN, solo tarjetas. Su salida de 12 V (400 mA) sale por el relé.

Ahí está la parte delicada. Con fuente de 12 V 1,2 A o más, la salida es estable. Con PoE, Akuvox pide firmware 25.30.10.11 o más y avisa que la salida queda afectada por el ajuste de volumen. Ninguna página leída detalla el mecanismo, pero la consecuencia práctica es clara: la tensión que recibe la cerradura puede cambiar según cómo esté el volumen.

Por eso el laboratorio mide con volumen bajo y alto, con la carga conectada y durante la apertura. Si la caída afecta a la cerradura, hay dos caminos: fuente de 12 V 1 A para el portero, o fuente propia para la cerradura y el relé como contacto seco. En obra, el segundo es el estable: la cerradura no depende del volumen.

Acceso al menú: R28 con `*2396#` y después `1`; R25A manteniendo el botón 5 s; R25K con `*3258*`."""
}

# =============================================================== 26
M["26"] = {
    "fig": {"file": "26.svg",
            "alt": "Cuatro porteros genéricos: R20A de un botón con tarjetas 13,56 y 125 kHz, QR desde 320.30.12.19 y sin PIN; R20K con teclado, PIN y tarjetas; R20K-L con teclado y LTE, PIN y solo 13,56 MHz; R20B con varios botones, tarjetas, módulos MD06 o MD12 y sin PIN. Abajo: todos Linux, aluminio, sin pantalla, IP65, PoE 802.3af o 12 V 1 A y relé 30 V 2 A.",
            "caption": "Los cuatro R20 comparten base; cambia cómo entra la gente."},
    "steps": [
        {"file": "26-paso2.svg", "step": 2,
         "alt": "Una etiqueta que dice R20A V3.0, una ventana web con Hardware Version 220.x y el resultado: hardware 2, no 3. Debajo, una tabla: 20.x hardware 1; 220.x hardware 2 (R20A con etiqueta V3.0); 320.x hardware 3 (R20A V5.0 y R20K V3.0).",
         "caption": "El primer bloque de Hardware Version dice la generación real, no la etiqueta.",
         "after": "Product Information`, `Hardware Version`"},
        {"file": "26-paso3.svg", "step": 3,
         "alt": "Tres filas de decisión: hardware 3 o R20B V2.0 con fuente de 12 V 1,2 A o más da 12 V 500 mA por el relé; hardware 3 con PoE y firmware 320.30.11.42 o más da 12 V 500 mA afectada por el volumen; hardware viejo no tiene salida y la cerradura va con fuente propia.",
         "caption": "La salida de 12 V depende de la versión de hardware real y de la alimentación.",
         "after": "Decidí la cerradura:"},
    ],
    "concepts": [
        {"name": "Versión de hardware real",
         "para_que": "Un mismo modelo se fabrica en generaciones de hardware distintas, con firmware distinto y funciones distintas. La etiqueta comercial no siempre coincide con la generación.",
         "como": "En la web, `Status > Basic > Product Information`, `Hardware Version`: si empieza con `20.` es hardware 1, `220.` hardware 2 y `320.` hardware 3. Akuvox avisa que un R20A con etiqueta V3.0 es hardware 2 y uno V5.0 es hardware 3.",
         "ejemplo": "En un edificio de la Unión hay que actualizar cinco R20A. Dos dicen V3.0 en la etiqueta pero en la web marcan `220.`: se baja el firmware de hardware 2 para esos dos, y el de hardware 3 para el resto."},
        {"name": "Firmware por hardware",
         "para_que": "Cada generación tiene su propio archivo de firmware. Cargar el de otra generación puede fallar o dejar el equipo inutilizable.",
         "como": "Se baja el archivo de la versión real que muestra la web, no el de la etiqueta. Se anota en la planilla hardware, firmware y decisión de cerradura.",
         "ejemplo": "Un técnico apurado carga a todos los R20 de un complejo el mismo archivo; los de hardware 2 rechazan la actualización. Con la planilla por equipo, eso no pasa."},
        {"name": "Cómo se entra a la puerta en cada R20",
         "para_que": "Los cuatro R20 comparten base pero no credenciales. Elegir mal el modelo deja al cliente sin PIN o sin la tarjeta que ya usa.",
         "como": "R20A: un botón, tarjetas de 13,56 y 125 kHz, QR desde 320.30.12.19, sin PIN. R20K: teclado, PIN y tarjetas. R20K-L: LTE, PIN y solo 13,56 MHz. R20B: botones y tarjetas, sin PIN; MD06 y MD12 son módulos de nombres.",
         "ejemplo": "Un edificio de cuatro apartamentos en Malvín Norte usa llaveros de 125 kHz: un R20B con botón por apartamento lee esos llaveros; un R20K-L no, porque solo lee 13,56 MHz."},
    ],
    "teoria_md": """### Un poco de historia

Los R20 son, probablemente, el portero Akuvox que más vas a encontrar en paredes de Uruguay: compactos, de aluminio, sin pantalla, para edificios chicos y casas. Akuvox los presenta como porteros SIP compactos, y el R20K-L como la versión con LTE.

Su historia es la de un modelo que se fue renovando por dentro sin cambiar de nombre. La familia tiene tres versiones de hardware, cada una con su firmware. Y la guía de actualización de Akuvox avisa algo que sorprende: la etiqueta comercial no siempre coincide con la generación. Un R20A con etiqueta V3.0 es hardware 2, y uno con etiqueta V5.0 es hardware 3.

En tarjetas conviven dos mundos. Las de 125 kHz son la generación vieja de proximidad (tipo EM o HID Prox), simples y fáciles de copiar. Las de 13,56 MHz (ISO 14443, como MIFARE) permiten cifrado y más datos. Por eso importa qué frecuencia lee cada modelo.

### Cómo funciona

El firmware de Akuvox tiene la forma `A.B.C.D`, y el primer bloque identifica el modelo y la generación. En los R20:

- `20.x` es hardware 1,
- `220.x` es hardware 2,
- `320.x` es hardware 3 (R20A V5.0, R20K V3.0).

Se lee en `Status > Basic > Product Information`, `Hardware Version`, después de sacar la IP con el método de la familia: R20A manteniendo el botón 5 s, R20K con `*3258*`, R20B manteniendo el primer botón 5 s.

La versión de hardware decide la cerradura. R20K V3.0, R20A V5.0 y R20B V2.0 dan 12 V 500 mA por el relé:

- con fuente de 12 V 1,2 A o más, la salida es estable;
- con PoE, solo desde el firmware 320.30.11.42, y afectada por el volumen del equipo;
- las versiones viejas no tienen salida: la cerradura va con fuente propia.

Credenciales por modelo: R20A un botón, tarjetas de las dos frecuencias y QR desde 320.30.12.19, sin PIN; R20K teclado con PIN y tarjetas; R20K-L con PIN y solo 13,56 MHz; R20B botones y tarjetas, sin PIN. MD06 y MD12 son módulos de nombres; no hay ficha leída con su detalle.

Todos: Linux, IP65, Wiegand, PoE 802.3af o 12 V 1 A, relé de 30 V 2 A."""
}

# =============================================================== 27
M["27"] = {
    "fig": {"file": "27.svg",
            "alt": "Dos porteros genéricos con pantalla, E18 (estándar o LTE) y E16 (5 pulgadas táctil). Grilla: ambos con PIN, rostro, Bluetooth y QR, relé 30 V 2 A y PoE 802.3af; E18 con tarjetas 13,56 y 125 kHz y fuente E18C 12 V 1,5 A (con LTE 12 V 2,5 A); E16 solo 13,56 MHz, E16P con palma, fuente E16C 12 V 1 A. Ninguno tiene salida de 12 V.",
            "caption": "En la serie E de rostro, la cerradura siempre va con fuente propia."},
    "steps": [
        {"file": "27-paso1.svg", "step": 1,
         "alt": "Un portero con la pantalla marcada para mantenerla 5 segundos. Dos filas: E16 hasta 216.30.10.121 PIN admin, después Admin321; E18 hasta 18.30.10.211 PIN admin, después Admin321. Nota sobre los prefijos de firmware y el cambio del PIN.",
         "caption": "El PIN de sistema de fábrica cambió con el firmware: admin antes, Admin321 después.",
         "after": "Mantené la pantalla 5 s"},
        {"file": "27-paso3.svg", "step": 3,
         "alt": "Cableado de un E16C o E18C sin borne de 12 V: el relé A del portero como contacto seco; el positivo de la fuente de la cerradura va a COM, NO va al positivo de la cerradura y el negativo de la cerradura vuelve al negativo de la fuente.",
         "caption": "Sin salida de 12 V, el relé solo conmuta la fuente propia de la cerradura.",
         "after": "Elegí la fuente:"},
    ],
    "concepts": [
        {"name": "PIN de sistema",
         "para_que": "Es la clave que protege el menú del equipo desde su propia pantalla, en la calle. Quien la conoce puede ver la IP y tocar ajustes.",
         "como": "Se mantiene la pantalla 5 s y se ingresa el PIN. De fábrica es `admin` hasta 216.30.10.121 (E16) y 18.30.10.211 (E18), y `Admin321` después. El primer día se cambia por uno propio y se anota en la ficha.",
         "ejemplo": "En un edificio de Tres Cruces, alguien probó `admin` en el E16 del hall y entró al menú. Desde entonces, cada portero se entrega con PIN de sistema propio documentado en la ficha del consorcio."},
        {"name": "Contacto seco",
         "para_que": "Un relé de contacto seco solo abre o cierra un circuito, sin aportar energía. Separa la lógica del portero de la energía de la cerradura.",
         "como": "El E18C y el E16C no tienen salida de 12 V: la fuente de la cerradura va a COM, NO al positivo de la cerradura (fail-secure) y el negativo vuelve a la fuente. Para fail-safe, NC. El relé soporta 30 V 2 A.",
         "ejemplo": "Un electroimán de una puerta de vidrio en una clínica de Pocitos se cablea en NC para liberar si se corta la luz; el E16 solo conmuta su fuente."},
        {"name": "Reconocimiento facial y palma",
         "para_que": "Permiten entrar sin tarjeta ni código. El rostro es cómodo para residentes; la palma suma una biometría que no depende de la cara.",
         "como": "E18 y E16 hacen rostro; el E16P suma venas de la palma. Se cargan por usuario, con horarios como cualquier credencial. La antisuplantación se revisa en la configuración (lección 7).",
         "ejemplo": "En un edificio de oficinas de la Aguada, los empleados entran por rostro en el E18 y las visitas con QR; nadie anda buscando la tarjeta."},
    ],
    "teoria_md": """### Un poco de historia

La serie E de Akuvox agrupa porteros de plástico, y dentro de ella el E18 y el E16 son los que traen reconocimiento facial. El E16 es un viejo conocido del curso: buena parte de las guías de configuración de los primeros arcos se escribieron con él, y sigue en el menú vigente al 27 de octubre de 2026.

Una historia que se repite en soporte es la del PIN de sistema. Hasta cierto firmware era `admin`, en minúscula; después pasó a ser `Admin321`. El cambio es bueno para la seguridad, porque `admin` era la clave más probada del mundo, pero deja afuera a quien prueba la vieja en un equipo actualizado.

El E16 tiene tres versiones de hardware, con firmware que empieza en `116.`, `216.` o `416.`. El E18 suma acciones HTTP extra desde el firmware 18.30.11.27: además de abrir, puede cerrar, dejar abierto, consultar el estado de la puerta y rechazar una tarjeta equivocada.

### Cómo funciona

**Credenciales**. E18C: PIN, tarjetas de 13,56 MHz y 125 kHz, rostro, Bluetooth y QR. E16: PIN, solo 13,56 MHz, rostro, Bluetooth y QR; el E16P suma venas de la palma.

**Alimentación**. Los dos son PoE 802.3af. Con fuente: E16C 12 V 1 A, E18C 12 V 1,5 A, E18 con LTE 12 V 2,5 A. Relé de 30 V 2 A.

**Sin salida de 12 V**. La tabla de Akuvox marca E18C y E16C sin salida de 12 V. El relé es un contacto seco: abre o cierra un circuito, pero no aporta energía. La cerradura se cablea como en la lección 4:

- positivo de la fuente a `COM`,
- `NO` al positivo de la cerradura (fail-secure),
- negativo de la cerradura al negativo de la fuente.

Para que libere sin energía (fail-safe), se usa `NC`. En un electroimán, diodo en antiparalelo.

**PIN de sistema**. Se mantiene la pantalla 5 s y se ingresa: `admin` hasta 216.30.10.121 en el E16 y 18.30.10.211 en el E18, `Admin321` después. Ese PIN abre el menú del equipo en la calle, así que se cambia el primer día.

**Estado de puerta en el E18**. Con 18.30.11.27 o más, `action=DoorStatus` en el mismo endpoint `/fcgi/OpenDoor` consulta el estado: útil para saber, sin ir, si la puerta quedó abierta."""
}

# =============================================================== 28
M["28"] = {
    "fig": {"file": "28.svg",
            "alt": "Dos porteros genéricos de un botón, E13S y E12 (E12S o E12W), con la etiqueta casa u oficina chica. Grilla: ambos con tarjeta 13,56 MHz, sin PIN ni rostro, relé 30 V 2 A; E12 con Bluetooth, Wi-Fi en la versión E12W según la guía, PoE af o 12 V 1 A, sin salida de 12 V y sin RS485. Varias celdas del E13S figuran sin dato.",
            "caption": "Un botón y tarjeta: la cerradura va con fuente propia y el E12 no tiene RS485 para el SR01."},
    "steps": [
        {"file": "28-paso1.svg", "step": 1,
         "alt": "Un portero de un botón con el botón marcado para mantenerlo 5 segundos; un globo dice que anuncia la IP en voz alta. Al lado, la web en Status > Basic > Product Information con firmware 12., 312. o 13. y la clave web resaltada para cambiarla hoy.",
         "caption": "IP por voz, firmware en la web y la clave web cambiada en la misma visita.",
         "after": "Mantené el botón de llamada 5 s"},
        {"file": "28-paso4.svg", "step": 4,
         "alt": "Dos paneles. Rojo: E12 con SR01 por una conexión especial, sin RS485, que Akuvox no recomienda. Verde: portero con RS485 conectado a un SR01 adentro que maneja la cerradura; rompen el portero y la puerta sigue cerrada. Abajo, tres caminos para recuperar una clave web perdida: SmartPlus, PC Manager en la misma LAN y llave del equipo a soporte.",
         "caption": "Si la cerradura tiene que resistir un ataque, conviene un portero con RS485 y SR01.",
         "after": "Dejá escrito en la ficha:"},
    ],
    "concepts": [
        {"name": "Portero de un botón",
         "para_que": "La forma más simple de portero IP: un botón que llama a un destino y un lector de tarjeta. Pensado para una casa o una oficina chica.",
         "como": "E13S y E12 leen tarjeta de 13,56 MHz, sin PIN ni rostro; el E12 suma Bluetooth. La IP se pide manteniendo el botón 5 s y la anuncia en voz alta. Relé de 30 V 2 A en los dos.",
         "ejemplo": "Una casa en El Pinar con el E12 en la reja: el botón llama al monitor de la cocina y la familia entra con llavero de 13,56 MHz."},
        {"name": "Clave web y su recuperación",
         "para_que": "La clave web de fábrica da acceso total al equipo desde la red. En los de un botón no hay pantalla para resetear a mano, así que perderla complica.",
         "como": "Se cambia el primer día y se anota en la ficha. Si se pierde, el soporte de Akuvox documenta tres caminos: SmartPlus, PC Manager en la misma LAN o exportar la llave del equipo y mandarla a soporte.",
         "ejemplo": "Un instalador anterior dejó un E12 sin documentar en una oficina de Cordón. Con PC Manager desde una notebook en la misma red se recupera el acceso sin sacar el equipo de la pared."},
        {"name": "E12 y el SR01",
         "para_que": "El SR01 protege la cerradura cuando el portero queda expuesto. Para eso necesita una conexión segura con el portero, normalmente RS485.",
         "como": "El E12 no tiene RS485 ni salida de 12 V; su conexión al SR01 es especial y Akuvox no la recomienda por seguridad. Si la cerradura tiene que resistir que rompan el portero, conviene otro modelo con RS485.",
         "ejemplo": "Un local comercial en Av. Italia pide que nadie pueda abrir arrancando el portero: en vez del E12 se cotiza un portero con RS485 y SR01 adentro."},
    ],
    "teoria_md": """### Un poco de historia

Los porteros de un botón son la versión IP del timbre de toda la vida: un pulsador que llama a un destino. Akuvox presenta al E13S como portero SIP de un botón y al E12 como portero SIP compacto; los dos son de plástico, Linux y con Wiegand según la guía de selección, y están pensados para una casa o una oficina chica.

El modelo que los precedió en muchas instalaciones es el E11, que sigue en paredes aunque ya no está en el menú. En 2023 el equipo de Claroty publicó 13 vulnerabilidades en el E11 y encontró unos 5.000 equipos expuestos a internet; CISA emitió un aviso con puntaje 9,8. La lección quedó clara para toda la familia: clave web propia el primer día, firmware al día y nada publicado a internet.

### Cómo funciona

**Credenciales**. Tarjeta de 13,56 MHz, sin PIN y sin rostro. El E12 suma Bluetooth. La tabla de métodos separa E12S y E12W, y la guía de selección marca Wi-Fi para el E12: lo razonable es leer la W como la versión con Wi-Fi y confirmarlo en la etiqueta antes de prometerlo.

**Alimentación**. El E12 va con PoE 802.3af o fuente de 12 V 1 A. Del E13 la tabla de alimentación no dice nada; la guía solo marca PoE. Relé de 30 V 2 A en los dos.

**Sin salida de 12 V ni RS485 en el E12**. La cerradura va con fuente propia y el relé como contacto seco. Y como no tiene RS485, el SR01 se le conecta de una forma especial que el propio Akuvox no recomienda por seguridad. Si la cerradura tiene que resistir un ataque al frente, conviene otro portero.

**Versiones de hardware**. El E12 tiene dos: firmware `12.` o `312.`. El E13 aparece como `13.`.

**Acceso**. Se mantiene el botón de llamada 5 s y el equipo dice su IP en voz alta. En la web, `Status > Basic > Product Information` muestra el firmware.

**Clave perdida**. Sin pantalla, recuperar el acceso no es trivial. El soporte de Akuvox documenta tres caminos para los de un botón: SmartPlus, PC Manager desde una PC en la misma LAN, o exportar la llave del equipo con la herramienta y mandarla a soporte, que devuelve un archivo para desbloquear. Por eso la clave web se cambia y se documenta en la primera visita."""
}


# =============================================================== validación
def lab_lines(lid):
    card = next(CLASS.glob(f"{int(lid):02d}-*/card.md")).read_text(encoding="utf-8")
    lab = card.split("**Laboratorio**", 1)[1].split("**Regla para quedarse**", 1)[0]
    out, inside = [], False
    for ln in lab.splitlines():
        if ln.strip().startswith("```"):
            inside = not inside
            continue
        if not inside:
            out.append(ln)
    return out


errs = []
for lid, ent in M.items():
    for f in [ent["fig"]["file"]] + [s["file"] for s in ent["steps"]]:
        if not (OUT / f).exists():
            errs.append(f"{lid}: falta {f}")
    lines = lab_lines(lid)
    for s in ent["steps"]:
        a = s["after"]
        hits = [l for l in lines if a in l]
        if len(hits) != 1 or not (15 <= len(a) <= 40):
            errs.append(f"{lid}: after {a!r} aparece {len(hits)} veces (len {len(a)})")
        elif not re.match(rf"\s*{s['step']}\.", hits[0]):
            errs.append(f"{lid}: after {a!r} no está en el paso {s['step']}: {hits[0][:50]}")
    t = ent["teoria_md"]
    n = len(re.findall(r"\S+", t))
    if not (250 <= n <= 450):
        errs.append(f"{lid}: teoria_md tiene {n} palabras")
    if "### Un poco de historia" not in t or "### Cómo funciona" not in t:
        errs.append(f"{lid}: faltan subtítulos")
    if not (2 <= len(ent["concepts"]) <= 4):
        errs.append(f"{lid}: {len(ent['concepts'])} conceptos")
    blob = json.dumps(ent, ensure_ascii=False)
    if "—" in blob or "–" in blob:
        errs.append(f"{lid}: guion largo")
    print(lid, "teoria", n, "palabras")

if errs:
    print("\n".join(errs))
    sys.exit(1)
(OUT / "manifest-15-28.json").write_text(json.dumps(M, ensure_ascii=False, indent=2), encoding="utf-8")
print("ok", len(M), "lecciones")
