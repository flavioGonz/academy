"""Genera manifest-33-35.json (figuras, pasos, conceptos, teoría y script_rsc de las lecciones 33 a 35)."""
import json, re
from pathlib import Path

OUT = Path("/home/claude/ies-training/ilustraciones/mikrotik/manifest-33-35.json")
CLASS = Path("/home/claude/claudemy/mikrotik/class")

M = {}

# ====================================================================== 33
M["33"] = {
    "fig": {"file": "33.svg",
            "alt": "Tabla con las reglas de protección en orden: en input, aceptar established y related, drop invalid, ICMP con ping de WAN limitado, aceptar la lista admins y drop de todo lo que no viene de LAN; en forward, fasttrack, drop invalid y drop de lo que entra por WAN sin dst-nat; como extras, drop del puerto 53 desde WAN y listas SSH por etapas. Cada regla dice qué frena.",
            "caption": "Cada regla frena algo concreto; lo permitido va arriba del drop y lo extra no reemplaza a no exponer."},
    "steps": [
        {"file": "33-paso3.svg", "step": 3,
         "alt": "Una consulta DNS desde internet al puerto 53 del router queda bloqueada, mientras la PC de la LAN sigue usando el DNS del router. Abajo, el caso del DNS abierto con 409 GB de subida y la prueba con nslookup desde la notebook WAN.",
         "caption": "El DNS del router atiende a la LAN; desde la WAN, el 53 se descarta arriba de todo.",
         "after": "cerrá el 53 desde WAN arriba de todo"},
        {"file": "33-paso4.svg", "step": 4,
         "alt": "Escalera de cuatro escalones: connection1 por 5 minutos, connection2 por 15, connection3 por una hora y bruteforce_blacklist por un día con drop. Arriba, la lista admins se acepta primero y no cuenta.",
         "caption": "Cada conexión SSH nueva sube un escalón; la lista admins va primero para no bloquearte.",
         "after": "admins exceptuados y las listas por etapas"},
    ],
    "concepts": [
        {"name": "Estados de conexión (established, related, invalid)",
         "para_que": "Un firewall que mira paquete por paquete tendría que abrir a mano el camino de vuelta de cada conexión. El seguimiento de conexiones se creó para que el router recuerde qué conversaciones aceptó y deje pasar sus respuestas sin pensarlo dos veces.",
         "como": "Por eso la primera regla de cada cadena acepta established y related, y la segunda descarta invalid: paquetes que no pertenecen a ninguna conversación conocida. El resto de las reglas trabaja solo con lo nuevo, que es poco y le baja la carga al router. La documentación avisa que en ruteo asimétrico (sale por un ISP y vuelve por otro) la vuelta puede verse como invalid.",
         "ejemplo": "En un local con dos WAN, si los pings que salen por la fibra vuelven por el 4G, el contador de `defconf: drop invalid` sube y la conexión se corta: el arreglo está en las rutas (lección de dos WAN), no en borrar la regla."},
        {"name": "Drop final y drop de WAN sin dst-nat",
         "para_que": "Hay dos formas de filtrar: permitir lo que hace falta y descartar el resto, o descartar solo lo malo. La primera es más segura, y es la que usa la configuración por defecto para proteger al router y a la LAN.",
         "como": "En input, `drop all not coming from LAN` descarta todo lo que llega al router desde afuera que no aceptaste arriba. En forward, `drop all from WAN not DSTNATed` descarta las conexiones nuevas que entran por la WAN hacia la LAN, salvo las que tienen un port forwarding. Todo lo que quieras permitir va arriba de esos drops, con place-before.",
         "ejemplo": "Un atacante que conoce tu red 192.168.88.0/24 manda un paquete directo a la cámara 192.168.88.60: como no tiene dst-nat, la regla de forward lo descarta aunque el router sepa cómo llegar."},
        {"name": "Address-list con timeout",
         "para_que": "Para que una regla recuerde a quién vio, sin escribir IPs a mano. Una regla con add-src-to-address-list anota la IP de origen en una lista por un tiempo, y otras reglas deciden según esa lista.",
         "como": "Las entradas con timeout son dinámicas: no se guardan en la configuración, un reinicio las borra y cada coincidencia nueva renueva el tiempo. La regla que anota no frena el paquete, sigue a la siguiente: por eso las listas por etapas van en orden inverso y terminan en un drop.",
         "ejemplo": "Con las listas de la lección, un bot que abre cuatro SSH en minutos queda en `bruteforce_blacklist` por un día; lo ves con `/ip/firewall/address-list/print where list~\"^connection|^bruteforce\"` y lo sacás con remove."},
        {"name": "DNS abierto y amplificación",
         "para_que": "El router puede resolver nombres para la LAN (allow-remote-requests). El problema aparece cuando también contesta a internet: un atacante manda consultas chicas con la IP de la víctima falsificada y tu router le dispara respuestas grandes.",
         "como": "Si la LAN no usa al router como DNS, allow-remote-requests=no. Si lo usa, drop de UDP y TCP 53 que entra por la WAN, arriba de todo, y la prueba desde afuera con nslookup a la IP pública del router.",
         "ejemplo": "En el foro, un usuario vio 5 Mb/s de subida constantes y 409 GB en una semana hasta que el proveedor le avisó: era su router contestando DNS a internet."},
    ],
    "teoria_md": (
        "### Un poco de historia\n"
        "Los primeros firewalls de fines de los ochenta miraban cada paquete por separado: dirección, puerto y protocolo. Para dejar volver las respuestas había que abrir puertos altos a mano, y eso dejaba agujeros. En los noventa apareció el firewall con estado: el equipo arma una tabla de conexiones y sabe si un paquete es nuevo, es la respuesta de algo que ya aceptó o no tiene sentido.\n\n"
        "RouterOS corre sobre el kernel Linux y su firewall hereda esa idea de netfilter, el subsistema de filtrado que Linux trae desde la versión 2.4 (2001). Por eso la documentación de MikroTik habla del límite de ICMP del kernel: unos 100 paquetes por segundo.\n\n"
        "Los ataques que esta lección frena también tienen historia. SSH reemplazó a Telnet a mediados de los noventa, y desde entonces hay bots probando contraseñas contra el puerto 22 de cualquier IP pública. Y en 2013 el CERT de Estados Unidos emitió una alerta (TA13-088A) por ataques de amplificación con resolvers DNS abiertos; ese mismo año ya se pedía en el foro de MikroTik descartar las consultas al 53 que llegan desde internet.\n\n"
        "### Cómo funciona\n"
        "**Connection tracking.** El primer paquete de una conversación es `new`; si el router lo deja pasar, la conversación queda en la tabla y lo que sigue es `established`. Lo que nace de otra conexión (un error ICMP, el canal de datos de FTP) es `related`. Lo que no encaja con nada es `invalid`.\n\n"
        "**Orden.** Cada cadena se lee de arriba abajo y manda la primera regla que coincide. Por eso arriba van los accept de established y related (la mayoría del tráfico sale ahí, rápido), después el drop de invalid, después lo nuevo que querés permitir, y al final el drop.\n\n"
        "**FastTrack.** En forward, las conexiones ya aceptadas se marcan para un camino rápido que saltea firewall y colas. Como no todos los paquetes toman ese atajo, va seguido de un accept igual.\n\n"
        "**Input y forward.** `drop all not coming from LAN` cuida al router; `connection-nat-state=!dstnat` en forward cuida a la LAN de conexiones que entran sin un port forwarding.\n\n"
        "**Listas por etapas.** Con los tiempos de la documentación (5 min, 15 min, 1 h y 1 día), un atacante rápido logra 27 intentos de contraseña antes del bloqueo, porque el servidor SSH acepta 9 por conexión. Uno paciente, que espera más de 5 minutos entre conexiones, nunca pasa del primer escalón: por eso la defensa de fondo sigue siendo no exponer y usar claves."
    ),
    "script_rsc": {
        "titulo": "Reglas de protección sobre el firewall por defecto",
        "descripcion": "Agrega la lista admins, el ping de WAN limitado y el drop del puerto 53 desde WAN, todo con comentarios ies-. Las listas SSH contra fuerza bruta solo se crean si elegís abrir SSH a la WAN.",
        "variables": [
            {"nombre": "ADMIN_IP", "valor": "198.51.100.7", "detalle": "IP pública fija de la oficina que administra (va a la lista admins)"},
            {"nombre": "ABRIR_SSH_WAN", "valor": "no", "detalle": "si o no: crear las listas por etapas y abrir SSH desde WAN (solo si un proveedor lo exige)"},
        ],
        "codigo": "\n".join([
            "# IES Training · MikroTik · Reglas de protección (lección 23)",
            "# Probalo primero en un equipo de banco y en Safe Mode (Ctrl+X).",
            "# Requiere el firewall por defecto (defconf). No borra ni mueve reglas existentes.",
            "{",
            ":local admin \"{{ADMIN_IP}}\"",
            ":local abrirSsh \"{{ABRIR_SSH_WAN}}\"",
            ":local drop [/ip/firewall/filter/find chain=input comment=\"defconf: drop all not coming from LAN\"]",
            ":if ([:len $drop] = 0) do={ :error \"No encuentro el drop de la defconf: revisá el firewall a mano\" }",
            "# 1. Lista admins (se usa antes de cualquier drop)",
            ":if ([:len [/ip/firewall/address-list/find list=admins address=$admin]] = 0) do={",
            "  /ip/firewall/address-list/add list=admins address=$admin comment=\"ies-admins\" }",
            "# 2. Ping desde WAN limitado a 5 por segundo, arriba del accept ICMP de fábrica",
            ":local icmp [/ip/firewall/filter/find chain=input comment=\"defconf: accept ICMP\"]",
            ":if (([:len $icmp] > 0) && ([:len [/ip/firewall/filter/find comment=\"ies-ping-wan-limitado\"]] = 0)) do={",
            "  /ip/firewall/filter/add chain=input in-interface-list=WAN protocol=icmp icmp-options=8:0 limit=5,10:packet action=accept comment=\"ies-ping-wan-limitado\" place-before=$icmp",
            "  /ip/firewall/filter/add chain=input in-interface-list=WAN protocol=icmp icmp-options=8:0 action=drop comment=\"ies-ping-wan-excedido\" place-before=$icmp }",
            "# 3. DNS: el 53 no se atiende desde WAN (arriba de todo; no afecta a la LAN)",
            ":local arriba [/ip/firewall/filter/find chain=input comment=\"defconf: accept established,related,untracked\"]",
            ":if ([:len $arriba] = 0) do={ :set arriba $drop }",
            ":foreach p in={\"udp\";\"tcp\"} do={",
            "  :if ([:len [/ip/firewall/filter/find comment=(\"ies-dns-wan-\" . $p)]] = 0) do={",
            "    /ip/firewall/filter/add chain=input in-interface-list=WAN protocol=$p dst-port=53 action=drop comment=(\"ies-dns-wan-\" . $p) place-before=$arriba } }",
            "# 4. Solo si SSH tiene que quedar abierto a WAN: admins primero y listas por etapas",
            ":if (($abrirSsh = \"si\") && ([:len [/ip/firewall/filter/find comment=\"ies-ssh-admins\"]] = 0)) do={",
            "  /ip/firewall/filter/add chain=input protocol=tcp dst-port=22 in-interface-list=WAN src-address-list=admins action=accept comment=\"ies-ssh-admins\" place-before=$drop",
            "  /ip/firewall/filter/add chain=input protocol=tcp dst-port=22 connection-state=new in-interface-list=WAN src-address-list=connection3 action=add-src-to-address-list address-list=bruteforce_blacklist address-list-timeout=1d comment=\"ies-ssh-lista-negra\" place-before=$drop",
            "  /ip/firewall/filter/add chain=input protocol=tcp dst-port=22 connection-state=new in-interface-list=WAN src-address-list=connection2 action=add-src-to-address-list address-list=connection3 address-list-timeout=1h comment=\"ies-ssh-tercera\" place-before=$drop",
            "  /ip/firewall/filter/add chain=input protocol=tcp dst-port=22 connection-state=new in-interface-list=WAN src-address-list=connection1 action=add-src-to-address-list address-list=connection2 address-list-timeout=15m comment=\"ies-ssh-segunda\" place-before=$drop",
            "  /ip/firewall/filter/add chain=input protocol=tcp dst-port=22 connection-state=new in-interface-list=WAN action=add-src-to-address-list address-list=connection1 address-list-timeout=5m comment=\"ies-ssh-primera\" place-before=$drop",
            "  /ip/firewall/filter/add chain=input protocol=tcp dst-port=22 in-interface-list=WAN src-address-list=!bruteforce_blacklist action=accept comment=\"ies-ssh-aceptar\" place-before=$drop",
            "  /ip/firewall/filter/add chain=input protocol=tcp dst-port=22 in-interface-list=WAN action=drop comment=\"ies-ssh-drop-lista-negra\" place-before=$drop }",
            ":put \"Listo: admins, ping de WAN limitado y 53 cerrado desde WAN. Verificá con /ip/firewall/filter/print stats where comment~\\\"ies-\\\"\"",
            "}",
        ]),
        "notas": [
            "No toca la sesión de quien lo pega: todo lo que agrega aplica solo a lo que entra por la lista WAN, y la regla de admins queda antes del drop.",
            "Probá desde una notebook del lado WAN: nslookup a la IP WAN del router no tiene que responder.",
            "Con ABRIR_SSH_WAN=si, SSH queda abierto desde internet con las listas por etapas: preferí VPN y claves. Si limitaste SSH con available-from, también hay que sumar el origen ahí.",
            "No borra nada: para deshacer, /ip/firewall/filter/remove [find comment~\"^ies-\"].",
        ],
    },
}

# ====================================================================== 34
M["34"] = {
    "fig": {"file": "34.svg",
            "alt": "Tres tarjetas: MNDP de MikroTik por UDP 5678 en broadcast, que usa WinBox; CDP de Cisco de 1994 por multicast cada 60 segundos; LLDP, estándar IEEE 802.1AB con EtherType 0x88CC, que habla casi cualquier marca. Las tres flechas bajan a /ip/neighbor, que muestra identidad, plataforma, versión, IP, MAC y puerto físico.",
            "caption": "Tres protocolos alimentan la misma tabla; lo que vos ves de los vecinos, ellos lo ven de vos."},
    "steps": [
        {"file": "34-paso1.svg", "step": 1,
         "alt": "Salida de /ip/neighbor/print como tabla: un switch en ether3,bridge descubierto por LLDP, un hAP en ether4,bridge por MNDP y un router del proveedor en ether1 por LLDP, marcado en rojo.",
         "caption": "INTERFACE trae el puerto físico y el bridge; un vecino en ether1 avisa que también te anunciás hacia la WAN.",
         "after": "Mirá los vecinos y en qué puerto aparece"},
        {"file": "34-paso4.svg", "step": 4,
         "alt": "Router con cinco puertos: ether2 con la notebook y ether3 con el switch en verde, en la lista descubrir y anunciándose; ether1 hacia internet en rojo y ether5 con una cámara en gris, sin anunciarse. Abajo, los comandos de la lista.",
         "caption": "Solo los puertos de la lista se anuncian y escuchan; WAN y cámaras quedan afuera.",
         "after": "Anunciate solo donde hace falta"},
    ],
    "concepts": [
        {"name": "Descubrimiento en capa 2",
         "para_que": "En una red con equipos de varias marcas, saber qué hay conectado en cada puerto llevaba cables, etiquetas y paciencia. Los protocolos de descubrimiento hacen que cada equipo se presente solo a su vecino: nombre, modelo, versión, IP y por qué puerto habla.",
         "como": "Los anuncios viajan dentro del mismo dominio de capa 2: no cruzan routers. El router junta lo que recibe por MNDP, CDP y LLDP en `/ip/neighbor`; `/ip/neighbor/lldp` muestra solo lo de LLDP. Que un equipo aparezca depende de que él también anuncie: muchos switches administrables y teléfonos IP lo hacen; en cámaras y NVR depende del modelo y del firmware.",
         "ejemplo": "En un rack heredado de un edificio en Pocitos, `/ip/neighbor/print` te muestra `ether3,bridge` con identity `sw-piso2`: sabés qué switch es y en qué puerto está antes de tocar un solo cable."},
        {"name": "discover-interface-list",
         "para_que": "Hasta RouterOS 6.40 se habilitaba el descubrimiento interfaz por interfaz; desde 6.41 se maneja con una lista de interfaces, para decidir de una vez dónde el router se presenta y dónde no.",
         "como": "Una interfaz en la lista anuncia y escucha; fuera de la lista, ninguna de las dos cosas. Con la configuración por defecto queda en LAN; sin ella, el valor de fábrica es static y entra la WAN. Si ponés el bridge, participan todos sus puertos; para algunos puertos, ponés esos puertos sueltos y el bridge no.",
         "ejemplo": "En un local donde ether5 va a la red del shopping, una lista `descubrir` con ether2 (gestión) y ether3 (switch propio) evita que el router le cuente su versión a la red del shopping y sigue mostrándote tu switch."},
        {"name": "LLDP y sus TLV",
         "para_que": "Cada fabricante tenía su protocolo (CDP en Cisco, otros en otras marcas) y no se entendían entre sí. LLDP, IEEE 802.1AB, fijó un formato común para que cualquier marca se presente igual.",
         "como": "Cada anuncio es una trama Ethernet (EtherType 0x88CC) con campos tipo-largo-valor: obligatorios el Chassis ID, el Port ID y el TTL, y después nombre, descripción, capacidades, IP de gestión, PoE. RouterOS manda cada 30 s y el vecino lo olvida si no recibe nada en 121 s. LLDP-MED suma la VLAN de voz para teléfonos IP.",
         "ejemplo": "Un switch de otra marca en el rack: `/ip/neighbor/lldp/print` te muestra su nombre, su puerto y si es bridge o router, aunque el switch no hable MNDP ni CDP."},
    ],
    "teoria_md": (
        "### Un poco de historia\n"
        "Cisco creó CDP en 1994 para que sus equipos se reconocieran entre sí: cada uno anuncia cada 60 segundos su nombre, su versión, sus IP y el puerto por el que habla, y el vecino guarda esa información unos 180 segundos. Otros fabricantes armaron sus propios protocolos, y en una red mixta nadie entendía a nadie.\n\n"
        "La IEEE publicó LLDP como estándar 802.1AB en 2005, con revisiones posteriores (la vigente es de 2016). En 2006 la TIA sumó LLDP-MED (ANSI/TIA-1057) para teléfonos IP: VLAN de voz, prioridad, ubicación y potencia PoE. Ese mismo año HP dejó de transmitir CDP en sus switches y pasó a LLDP.\n\n"
        "MikroTik tiene su protocolo propio, MNDP, que es el que llena la pestaña Neighbors de WinBox. RouterOS habla los tres. En la versión 6.41 cambió la forma de configurarlo: dejó de ser una casilla por interfaz y pasó a una lista de interfaces, `discover-interface-list`.\n\n"
        "### Cómo funciona\n"
        "**Anuncios periódicos.** Cada interfaz que está en la lista manda un anuncio cada `discover-interval` (30 s por defecto). En CDP y LLDP el anuncio lleva un TTL de intervalo por cuatro más uno: 121 s. Si en ese tiempo no llega otro, el vecino se borra de la tabla. Con `dying-gasp` el router manda un anuncio con TTL cero antes de un reinicio ordenado, y el vecino lo borra al instante.\n\n"
        "**Formatos.** LLDP viaja en una trama Ethernet con EtherType `0x88CC` hacia una dirección multicast que los switches estándar no reenvían: cada puerto ve a su vecino directo. Por dentro son TLV (tipo, largo, valor): Chassis ID, Port ID y TTL obligatorios, y opcionales como nombre del sistema, descripción, capacidades e IP de gestión. MNDP usa UDP 5678 por broadcast; CDP, una multicast propia de Cisco.\n\n"
        "**La tabla.** `/ip/neighbor` muestra la interfaz por la que llegó el anuncio (el puerto real y su bridge), la IP más alta del vecino, la MAC, la identidad, la plataforma, la versión y por qué protocolo lo descubrió. Para no agotar memoria, guarda como máximo 16 vecinos por megabyte de RAM en cada interfaz.\n\n"
        "**La otra cara.** Todo lo que el router aprende de sus vecinos, ellos lo aprenden de él. Por eso la lista de descubrimiento lleva solo los puertos propios: sacar una interfaz corta el anuncio y la escucha en ese puerto."
    ),
    "script_rsc": {
        "titulo": "Descubrimiento solo en los puertos propios",
        "descripcion": "Crea una lista de interfaces para el descubrimiento con los puertos que elijas, deja LLDP y MNDP y muestra los vecinos antes y después.",
        "variables": [
            {"nombre": "LISTA", "valor": "descubrir", "detalle": "Nombre de la lista de interfaces para el descubrimiento"},
            {"nombre": "PUERTOS", "valor": "ether2,ether3", "detalle": "Puertos sueltos (no el bridge) donde el router se anuncia: gestión y switches propios"},
            {"nombre": "PROTOCOLOS", "valor": "lldp,mndp", "detalle": "Protocolos a usar; sumá cdp solo si hay equipos Cisco"},
        ],
        "codigo": "\n".join([
            "# IES Training · MikroTik · Descubrir vecinos (lección 17)",
            "# Probalo primero en un equipo de banco y en Safe Mode (Ctrl+X).",
            "{",
            ":local lista \"{{LISTA}}\"",
            ":local puertos [:toarray \"{{PUERTOS}}\"]",
            ":local proto \"{{PROTOCOLOS}}\"",
            ":put \"Antes:\"",
            "/ip/neighbor/discovery-settings/print",
            "# Lista propia (si ya existe, se reutiliza)",
            ":if ([:len [/interface/list/find name=$lista]] = 0) do={",
            "  /interface/list/add name=$lista comment=\"ies-descubrir\" }",
            ":foreach p in=$puertos do={",
            "  :if ([:len [/interface/find name=$p]] = 0) do={",
            "    :put (\"No existe la interfaz \" . $p . \": la salteo\")",
            "  } else={",
            "    :if ([:len [/interface/list/member/find list=$lista interface=$p]] = 0) do={",
            "      /interface/list/member/add list=$lista interface=$p comment=\"ies-descubrir\" } } }",
            "# Sin puertos válidos no se cambia nada",
            ":if ([:len [/interface/list/member/find list=$lista]] = 0) do={ :error \"La lista quedó vacía: revisá los nombres de los puertos\" }",
            "/ip/neighbor/discovery-settings/set discover-interface-list=$lista protocol=$proto",
            ":put \"Después:\"",
            "/ip/neighbor/discovery-settings/print",
            "/ip/neighbor/print",
            ":put (\"Listo: el router se anuncia solo en la lista \" . $lista . \". Verificá desde la WAN con WinBox, pestaña Neighbors.\")",
            "}",
        ]),
        "notas": [
            "No corta el acceso: WinBox por MAC depende del MAC server (lección de cerrar puertas), no de esta lista. Pero si el puerto de tu notebook queda afuera, el router deja de aparecer en Neighbors desde ahí.",
            "Los puertos van sueltos: si ponés el bridge, se anuncian todos sus puertos, cámaras incluidas.",
            "Para volver a la configuración por defecto: /ip/neighbor/discovery-settings/set discover-interface-list=LAN protocol=cdp,lldp,mndp.",
        ],
    },
}

# ====================================================================== 35
M["35"] = {
    "fig": {"file": "35.svg",
            "alt": "El router con Netwatch vigila un NVR en 192.168.88.50 con una sonda tcp-conn al puerto 554 y una cámara PoE en 192.168.88.60 con una sonda icmp de 10 paquetes. Al pasar de up a down corre el down-script (mail, Telegram, cortar PoE); al pasar de down a up, el up-script. Abajo, las seis sondas de RouterOS 7.",
            "caption": "La sonda prueba; el script corre una sola vez por cada cambio de estado."},
    "steps": [
        {"file": "35-paso2.svg", "step": 2,
         "alt": "Línea de tiempo con una prueba cada 30 segundos: tres bien, tres fallas desde que se desenchufa el NVR y de nuevo bien al enchufarlo. En la primera falla aparece event down y corre el down-script; al volver, event up. Abajo, las líneas del log.",
         "caption": "La primera prueba fallida cambia el estado a down y deja el evento en el log.",
         "after": "Desenchufá el NVR (o deshabilitá"},
        {"file": "35-paso4.svg", "step": 4,
         "alt": "Netwatch manda al caer un mail con /tool/e-mail/send por SMTP 587 y al volver un Telegram con /tool/fetch mode=https y output=none. Un recuadro rojo avisa que desde RouterOS 7.13, sin output=none, el aviso no llega.",
         "caption": "Mail al caer, Telegram al volver; output=none es lo que hace andar el fetch desde Netwatch.",
         "after": "Aviso a Telegram (token del bot"},
        {"file": "35-paso5.svg", "step": 5,
         "alt": "Router con PoE out alimentando una cámara por ether5. Una línea de alimentación muestra la cámara colgada, 10 segundos sin PoE y el arranque de nuevo. Al costado, la alternativa power-cycle-ping del propio puerto, y abajo el comando de Netwatch.",
         "caption": "El down-script corta el PoE 10 segundos y la cámara arranca de nuevo.",
         "after": "Cámara PoE que se cuelga: Netwatch"},
    ],
    "concepts": [
        {"name": "Sonda y cambio de estado",
         "para_que": "Revisar a mano si cada NVR, cámara o enlace de un cliente está vivo no escala. Netwatch se creó para que el router pruebe un equipo cada tanto y haga algo solo cuando el estado cambia.",
         "como": "Cada sonda arranca en unknown y pasa a up o down después de la primera prueba. El down-script corre al pasar a down y el up-script al pasar a up, una vez por cambio, no en cada prueba. Después de un reinicio espera 5 minutos (startup-delay). Sin scripts, el cambio igual queda en el log.",
         "ejemplo": "En un local de Tres Cruces, la sonda al NVR cae a las 3 de la mañana: llega un solo mail de caída, y uno de vuelta cuando vuelve la luz, no cien mensajes."},
        {"name": "Qué sonda elegir",
         "para_que": "Un ping solo dice que el equipo está prendido. RouterOS 7 agregó sondas que prueban lo que de verdad importa: que un puerto atienda, que una web conteste bien, que un DNS resuelva.",
         "como": "`icmp` manda 10 paquetes por prueba y cae con 85% de pérdida o latencia alta: sirve para enlaces y para evitar falsas alarmas. `tcp-conn` prueba el saludo TCP a un puerto (el 554 de un NVR). `http-get` y `https-get` miran el código de respuesta (100 a 299 es up). `dns` pregunta un nombre a un servidor.",
         "ejemplo": "Un NVR que contesta ping con el servicio colgado sigue up para una sonda simple; con `type=tcp-conn port=554` pasa a down y te enterás antes de que el cliente quiera ver una grabación."},
        {"name": "Permisos de los scripts de Netwatch",
         "para_que": "Netwatch corre scripts solo, sin nadie logueado, así que RouterOS le da permisos acotados para que un script no haga más de lo necesario.",
         "como": "Los scripts corren como el usuario *sys con las políticas read, write, test y reboot; si un comando pide más, el script no corre. Desde 7.13, fetch pide otra política para guardar la respuesta en un archivo: con `output=none` no guarda nada y corre. Lo que anda en la terminal puede no andar desde Netwatch, por eso se prueba desenchufando.",
         "ejemplo": "Después de actualizar una flota a 7.13, los avisos de Telegram dejaron de llegar sin un solo error visible; agregar `output=none` al fetch los devolvió."},
        {"name": "Quién vigila al que vigila",
         "para_que": "Netwatch vive en el router: si se corta la luz del router o su única salida a internet, no puede avisar nada. Es un límite de diseño, no un error.",
         "como": "Para la caída del sitio entero hace falta un monitor de afuera: otro router o un servidor en la oficina que vigile la IP pública o el túnel del cliente, o un equipo con batería y 4G en el sitio. Netwatch cubre lo de adentro: NVR, cámaras, enlaces de respaldo.",
         "ejemplo": "El router de la oficina del integrador vigila con Netwatch el túnel de cada cliente; el Netwatch de cada cliente vigila su NVR y sus cámaras."},
    ],
    "teoria_md": (
        "### Un poco de historia\n"
        "Vigilar equipos con ping es casi tan viejo como internet: el mensaje ICMP echo está definido en el RFC 792 de 1981 y el programa ping lo escribió Mike Muuss en 1983. Las herramientas de monitoreo de red se armaron sobre esa idea: probar cada tanto, marcar si responde o no, y avisar.\n\n"
        "En RouterOS, Netwatch empezó como un ping simple con dos scripts, uno al caer y otro al volver. En RouterOS 7 se rehízo con varios tipos de sonda: `icmp` con estadísticas de pérdida, latencia y jitter, `tcp-conn`, `http-get`, `https-get` y `dns`. El tipo `simple` quedó por compatibilidad con la versión vieja.\n\n"
        "Con los años el foro de MikroTik se llenó de recetas para avisar por mail, por SMS o por Telegram, y de una lección repetida: un cambio de versión puede romper un aviso en silencio, como pasó con fetch en la 7.13.\n\n"
        "### Cómo funciona\n"
        "**Estados.** Cada sonda arranca en `unknown`. Después de la primera prueba pasa a `up` o `down`. El `up-script` corre al pasar a up y el `down-script` al pasar a down; `test-script`, si lo hay, corre en cada prueba. `ignore-initial-up` e `ignore-initial-down` evitan avisos al habilitar la sonda o después de un reinicio, y `startup-delay` (5 minutos por defecto) la deja esperar a que el router termine de arrancar.\n\n"
        "**Pruebas.** Cada `interval` (10 s por defecto) la sonda prueba y espera hasta `timeout`. La sonda `icmp` manda `packet-count` paquetes (10, cada 50 ms) y calcula pérdida, promedio, máximo, desvío y jitter; si alguno pasa su umbral (por ejemplo `thr-loss-percent` de 85% o `thr-avg` de 100 ms), la prueba falla. `tcp-conn` completa el saludo TCP de tres pasos con el puerto y mide cuánto tarda. `http-get` pide la página y compara el código con `http-codes` (100 a 299). `dns` pregunta un registro A, AAAA, MX o NS.\n\n"
        "**Scripts.** Corren como `*sys` con políticas read, write, test y reboot, y pueden leer variables de la sonda (`$\"loss-percent\"`, `$\"http-status-code\"`). Por eso un fetch a Telegram lleva `output=none` y un mail se arma con texto ASCII.\n\n"
        "**Límite.** El router no puede avisar su propia caída: para eso, un monitor de afuera."
    ),
    "script_rsc": {
        "titulo": "Netwatch para el NVR y una cámara PoE, con avisos",
        "descripcion": "Crea o actualiza una sonda tcp-conn al NVR con aviso por mail al caer y, si cargás token y chat, Telegram al volver; opcionalmente, una sonda a una cámara que le corta el PoE 10 segundos.",
        "variables": [
            {"nombre": "NVR_IP", "valor": "192.168.88.50", "detalle": "IP del NVR"},
            {"nombre": "NVR_PUERTO", "valor": "554", "detalle": "Puerto del servicio a vigilar (RTSP u otro)"},
            {"nombre": "MAIL_DESTINO", "valor": "soporte@example.com", "detalle": "A quién llega el aviso"},
            {"nombre": "SMTP_SERVIDOR", "valor": "smtp.gmail.com", "detalle": "Servidor SMTP (puerto 587 con STARTTLS); vacío para no tocar /tool/e-mail"},
            {"nombre": "SMTP_USUARIO", "valor": "alertas@example.com", "detalle": "Cuenta que envía (también va en from)"},
            {"nombre": "CLAVE", "valor": "clave-de-aplicacion-EJEMPLO", "detalle": "Contraseña de aplicación del SMTP: cambiala"},
            {"nombre": "TG_TOKEN", "valor": "", "detalle": "Token del bot de Telegram (vacío = sin Telegram)"},
            {"nombre": "TG_CHAT", "valor": "", "detalle": "chat_id del grupo o persona"},
            {"nombre": "CAM_IP", "valor": "", "detalle": "IP de la cámara PoE (vacío = sin reinicio de PoE)"},
            {"nombre": "CAM_PUERTO_POE", "valor": "ether5", "detalle": "Puerto PoE out de la cámara"},
        ],
        "codigo": "\n".join([
            "# IES Training · MikroTik · Vigilar con Netwatch (lección 16)",
            "# Probalo primero en un equipo de banco. No cambia firewall ni rutas.",
            "{",
            ":local nvr \"{{NVR_IP}}\"; :local puerto [:tonum \"{{NVR_PUERTO}}\"]; :local mail \"{{MAIL_DESTINO}}\"",
            ":local smtp \"{{SMTP_SERVIDOR}}\"; :local usuario \"{{SMTP_USUARIO}}\"; :local clave \"{{CLAVE}}\"",
            ":local token \"{{TG_TOKEN}}\"; :local chat \"{{TG_CHAT}}\"",
            ":local cam \"{{CAM_IP}}\"; :local poe \"{{CAM_PUERTO_POE}}\"",
            "# 1. Servidor de correo (587 + STARTTLS)",
            ":if ([:len $smtp] > 0) do={",
            "  /tool/e-mail/set server=$smtp port=587 tls=starttls from=$usuario user=$usuario password=$clave }",
            "# 2. Scripts de aviso (texto sin tildes)",
            ":local down (\":log warning \\\"NVR \" . $nvr . \" caido\\\"; /tool/e-mail/send to=\" . $mail . \" subject=\\\"NVR caido\\\" body=\\\"El NVR \" . $nvr . \" no responde en el puerto \" . $puerto . \"\\\"\")",
            ":local up (\":log info \\\"NVR \" . $nvr . \" volvio\\\"\")",
            ":if (([:len $token] > 0) && ([:len $chat] > 0)) do={",
            "  :set up ($up . \"; /tool/fetch mode=https address=api.telegram.org src-path=\\\"bot\" . $token . \"/sendMessage\\3Fchat_id=\" . $chat . \"&text=NVR%20volvio\\\" check-certificate=yes output=none\") }",
            "# 3. Sonda al NVR: se crea o se actualiza",
            ":local id [/tool/netwatch/find name=\"ies-nvr\"]",
            ":if ([:len $id] = 0) do={",
            "  /tool/netwatch/add name=\"ies-nvr\" comment=\"ies-netwatch\" host=$nvr type=tcp-conn port=$puerto interval=30s down-script=$down up-script=$up",
            "} else={",
            "  /tool/netwatch/set $id host=$nvr type=tcp-conn port=$puerto interval=30s down-script=$down up-script=$up }",
            "# 4. Cámara PoE: corte de 10 s al caer (solo si cargaste CAM_IP)",
            ":if ([:len $cam] > 0) do={",
            "  :local ps (\"/interface/ethernet/poe/power-cycle \" . $poe . \" duration=10s\")",
            "  :local idc [/tool/netwatch/find name=\"ies-camara\"]",
            "  :if ([:len $idc] = 0) do={",
            "    /tool/netwatch/add name=\"ies-camara\" comment=\"ies-netwatch\" host=$cam type=icmp interval=1m down-script=$ps",
            "  } else={ /tool/netwatch/set $idc host=$cam type=icmp interval=1m down-script=$ps } }",
            "/tool/netwatch/print where comment=\"ies-netwatch\"",
            ":put \"Listo: sondas ies-nvr (y ies-camara si la cargaste). Probá desenchufando y mirá /log/print where message~\\\"NVR\\\"\"",
            "}",
        ]),
        "notas": [
            "Antes de confiar en el mail, probalo solo: /tool/e-mail/send to=... subject=\"Prueba\" body=\"hola\" y mirá last-status en /tool/e-mail/print. Con Gmail hace falta una contraseña de aplicación.",
            "El fetch a Telegram usa check-certificate=yes: el reloj del router tiene que estar en hora (NTP).",
            "La clave queda guardada en /tool/e-mail: cambiá el valor de ejemplo y no compartas el export sin revisarlo.",
            "Si el puerto PoE ya tiene power-cycle-ping-enabled=yes, dejá CAM_IP vacío: elegí uno de los dos mecanismos.",
            "Netwatch no avisa si se cae el router entero: para eso, un monitor de afuera.",
        ],
    },
}


# ---------------------------------------------------------------------- validación
def lab_lines(card):
    t = card.read_text(encoding="utf-8")
    lab = t.split("**Laboratorio**", 1)[1].split("**Regla para quedarse**", 1)[0]
    out, inside = [], False
    for ln in lab.splitlines():
        if ln.startswith("```"):
            inside = not inside
            continue
        if not inside:
            out.append(ln)
    return out


DIRS = {"33": "33-firewall-proteccion", "34": "34-ip-neighbors", "35": "35-netwatch"}
for k, v in M.items():
    lines = lab_lines(CLASS / DIRS[k] / "card.md")
    for s in v["steps"]:
        n = sum(ln.count(s["after"]) for ln in lines)
        assert n == 1 and 15 <= len(s["after"]) <= 43, (k, s["after"], n, len(s["after"]))
        assert (Path(OUT).parent / s["file"]).exists(), s["file"]
    w = len(re.sub(r"[#*`]", " ", v["teoria_md"]).split())
    assert 250 <= w <= 450, (k, w)
    assert "### Un poco de historia" in v["teoria_md"] and "### Cómo funciona" in v["teoria_md"]
    txt = json.dumps(v, ensure_ascii=False)
    assert "—" not in txt and "–" not in txt, k
    nl = v["script_rsc"]["codigo"].count("\n") + 1
    assert 15 <= nl <= 60, (k, nl)
    print(k, "teoría", w, "palabras · script", nl, "líneas · pasos", [s["step"] for s in v["steps"]])

# En las líneas que ejecuta RouterOS, texto ASCII (la terminal no muestra bien las tildes); los comentarios quedan con tildes.
TR = str.maketrans("áéíóúÁÉÍÓÚñÑ", "aeiouAEIOUnN")
for v in M.values():
    v["script_rsc"]["codigo"] = "\n".join(ln if ln.lstrip().startswith("#") else ln.translate(TR) for ln in v["script_rsc"]["codigo"].split("\n"))
OUT.write_text(json.dumps(M, ensure_ascii=False, indent=2), encoding="utf-8")
print("guardado", OUT)
