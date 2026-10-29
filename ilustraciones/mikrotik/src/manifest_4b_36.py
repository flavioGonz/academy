"""Genera manifest-4b.json (entrada "4" completa, reemplaza la de manifest-1-11.json) y manifest-36.json."""
import json

OUT = "/home/claude/ies-training/ilustraciones/mikrotik/"

# ---------------------------------------------------------------- lección 21
TEORIA_4 = """### Un poco de historia

El firewall de RouterOS no es un invento aislado: RouterOS corre sobre Linux y su firewall usa el mismo modelo de cadenas y tablas que netfilter, el marco de filtrado del kernel. Netfilter lo empezó Rusty Russell en 1998, después de haber escrito ipchains, su antecesor. El 26 de agosto de 1999 entró al kernel en desarrollo 2.3.15 y quedó en la versión estable 2.4.0, que salió a comienzos de 2001 con la herramienta iptables.

La gran diferencia con ipfwadm e ipchains fue separar el trabajo en piezas que se enganchan en puntos fijos del camino del paquete, y sumar un connection tracking de verdad: el kernel recuerda cada conexión y puede decir si un paquete es nuevo, parte de algo ya aceptado o basura. Ese seguimiento es lo que permite que una sola regla de established y related deje volver todas las respuestas, incluso en UDP.

MikroTik tomó esa base y le puso su propia interfaz: los mismos nombres de cadenas, los mismos estados, y agregados propios como las address lists, las interface lists y FastTrack. RouterOS 7, estable desde 2021, mantiene el mismo modelo.

### Cómo funciona

Un paquete que entra recorre etapas fijas. En prerouting pasan raw, el connection tracking (que le pone el estado) y el dst-nat. Recién después el router decide el camino: si el destino es una de sus IP, el paquete va a input; si no, a forward. Lo que genera el propio router sale por output. Al final, en postrouting, se aplica el src-nat, por ejemplo el masquerade hacia la WAN.

Eso explica dos cosas que confunden en obra. Un port forwarding nunca se ve en input: el dst-nat ya cambió el destino al NVR antes de la decisión. Y una regla de forward ve las direcciones privadas originales de la LAN, porque el masquerade todavía no ocurrió.

Dentro de cada cadena las reglas se leen en orden. Las acciones accept, drop, reject y jump deciden; passthrough y log anotan y dejan seguir. Si el paquete llega al final sin que nadie decida, pasa: en `/ip/firewall/filter` una cadena vacía es un accept. Una cadena propia creada con `jump` vuelve sola a la cadena que la llamó si no decide nada.

FastTrack marca conexiones establecidas para que sus paquetes salteen firewall, connection tracking y colas. Por eso se acompaña con un accept igual, y por eso un contador de forward puede quedar quieto aunque haya tráfico."""

CONCEPTS_4 = [
    {
        "name": "El camino del paquete y dónde entra el NAT",
        "para_que": "El router necesita saber qué hacer con cada paquete antes de filtrarlo: si es para él o si lo tiene que reenviar. Separar el recorrido en etapas fijas permite poner cada función en su lugar: traducir el destino antes de decidir, filtrar después, y traducir el origen al salir.",
        "como": "Pensá el recorrido como una línea: prerouting (raw, estado de la conexión, dst-nat), decisión de ruteo, input o forward, y postrouting (src-nat). Antes de escribir una regla, preguntate en qué punto de esa línea está el paquete que querés frenar y con qué direcciones llega ahí. Las reglas de forward ven la IP privada de la PC, porque el masquerade viene después; las del NVR publicado ven la IP del NVR, porque el dst-nat vino antes.",
        "ejemplo": "Un NVR en una clínica de Pocitos está publicado por el 18000. El técnico pone `chain=input dst-port=18000` para limitar orígenes y el contador queda en 0. La regla correcta es en forward, con `dst-address=192.168.88.50 dst-port=8000`: cuando el paquete llega al filter ya tiene el destino y el puerto del NVR."
    },
    {
        "name": "Estados de conexión y FastTrack",
        "para_que": "Revisar cada paquete de una descarga o de un flujo de video contra todas las reglas sería lento y difícil de escribir. El connection tracking recuerda cada conexión, así el firewall decide una vez, con el primer paquete, y el resto viaja con el estado established.",
        "como": "La primera regla de input y de forward acepta established, related y untracked; después se descarta invalid; recién ahí van tus reglas, que solo ven paquetes new. FastTrack acelera lo ya establecido salteando firewall y colas: si usás colas simples o IPsec, conviene revisarlo. Ojo: una regla nueva no corta lo que ya estaba abierto; para probar, se borra la conexión en `/ip/firewall/connection`.",
        "ejemplo": "Bloqueás la salida a internet de una cámara que mandaba video a una nube y la cámara sigue subiendo. No es que la regla esté mal: la sesión ya estaba establecida. Con `/ip/firewall/connection/remove [find src-address~\"192.168.88.101\"]` la cortás y desde ahí manda tu drop."
    },
    {
        "name": "drop, reject, jump y passthrough",
        "para_que": "No todo bloqueo es igual. Hacia internet conviene no dar información; adentro conviene que el equipo se entere rápido para no colgar procesos esperando. Y cuando las reglas crecen, hace falta ordenarlas en grupos y poder contar sin decidir.",
        "como": "drop descarta en silencio; reject descarta y avisa con un ICMP o un `tcp-reset` (`reject-with=icmp-admin-prohibited`, por ejemplo). jump manda el paquete a una cadena tuya, como `gestion-wan`, y si ahí nadie decide vuelve a la cadena original. passthrough suma al contador y deja seguir: sirve para medir sin tocar nada. log=yes con un `log-prefix` deja el paquete en el log con una etiqueta fácil de buscar.",
        "ejemplo": "En un barrio privado de Canelones, la central de monitoreo entra por WinBox desde su IP fija. Una regla `jump` de la WAN al 8291 lleva todo a `gestion-wan`: la IP de la central se acepta, el resto se registra con `GESTION-WAN` y se descarta. Al otro día, `/log/print where message~\"GESTION-WAN\"` muestra quién estuvo probando."
    },
    {
        "name": "Contadores y diagnóstico",
        "para_que": "El firewall no da errores: si una regla está mal ubicada, simplemente no coincide. Los contadores son la forma de saber qué regla se queda con cada paquete sin adivinar.",
        "como": "`/ip/firewall/filter/print stats` muestra bytes y paquetes por regla. Ponés en cero con `reset-counters`, generás el tráfico y mirás cuál sube. Si no sube ninguna, el tráfico no llega (Torch lo confirma); si sube una de arriba, esa se lo come. `disable` y `enable` sirven para probar sin borrar, y `move` reordena. En WinBox es lo mismo: columnas Bytes y Packets, el botón de reset y arrastrar la regla.",
        "ejemplo": "Un NVR no sincroniza la hora. En el print stats, la regla `NVR a NTP` está en 0 y `NVR resto` en 377: alguien movió el reject arriba. Un `move` lo devuelve abajo y el contador de NTP empieza a subir en un minuto."
    },
]

SCRIPT_4 = {
    "titulo": "Reglas de obra: gestión desde la oficina, salida del NVR y cámaras sin internet",
    "descripcion": "Agrega la oficina a la lista admins, una cadena gestion-wan que deja entrar a WinBox y SSH desde WAN solo a esa lista y registra el resto, y en forward deja al NVR salir solo a NTP y a su nube y a las cámaras sin internet. Todo con comentarios ies- y sobre el firewall por defecto.",
    "variables": [
        {"nombre": "OFICINA_IP", "valor": "203.0.113.25", "detalle": "IP pública fija de la oficina que administra (va a la lista admins)"},
        {"nombre": "NVR_IP", "valor": "192.168.88.50", "detalle": "IP del NVR en la LAN"},
        {"nombre": "NUBE_NVR", "valor": "nube.fabricante.example", "detalle": "Nombre o IP de la nube que publica el fabricante del NVR"},
        {"nombre": "CAMARAS", "valor": "192.168.88.101-192.168.88.150", "detalle": "Rango o red de las cámaras"},
    ],
    "codigo": """# IES Training · MikroTik · Input y forward: reglas de obra (lección 21)
# Probalo primero en un equipo de banco y en Safe Mode (Ctrl+X).
# Requiere el firewall por defecto. No borra reglas existentes.
{
:local oficina "{{OFICINA_IP}}"
:local nvr "{{NVR_IP}}"
:local nube "{{NUBE_NVR}}"
:local camaras "{{CAMARAS}}"
:local drop [/ip/firewall/filter/find chain=input comment="defconf: drop all not coming from LAN"]
:if ([:len $drop] = 0) do={ :error "No encuentro el drop de la defconf: revisa el firewall a mano" }
# 1. La oficina en la lista admins
:if ([:len [/ip/firewall/address-list/find list=admins address=$oficina]] = 0) do={
  /ip/firewall/address-list/add list=admins address=$oficina comment="ies-admins" }
# 2. Gestion desde WAN: cadena propia; admins entra, el resto queda en el log
:if ([:len [/ip/firewall/filter/find comment="ies-gestion-wan"]] = 0) do={
  /ip/firewall/filter/add chain=gestion-wan src-address-list=admins action=accept comment="ies-gestion-wan-admins"
  /ip/firewall/filter/add chain=gestion-wan action=drop log=yes log-prefix="GESTION-WAN" comment="ies-gestion-wan-resto"
  /ip/firewall/filter/add chain=input in-interface-list=WAN protocol=tcp dst-port=22,8291 action=jump jump-target=gestion-wan comment="ies-gestion-wan" place-before=$drop }
# 3. Listas del NVR y de las camaras
:if ([:len [/ip/firewall/address-list/find list=nube-nvr address=$nube]] = 0) do={
  /ip/firewall/address-list/add list=nube-nvr address=$nube comment="ies-nube-nvr" }
:if ([:len [/ip/firewall/address-list/find list=camaras address=$camaras]] = 0) do={
  /ip/firewall/address-list/add list=camaras address=$camaras comment="ies-camaras" }
# 4. Forward: NVR solo a NTP y a su nube (reject al resto); camaras sin internet
:if ([:len [/ip/firewall/filter/find comment="ies-nvr-ntp"]] = 0) do={
  /ip/firewall/filter/add chain=forward src-address=$nvr out-interface-list=WAN protocol=udp dst-port=123 action=accept comment="ies-nvr-ntp"
  /ip/firewall/filter/add chain=forward src-address=$nvr out-interface-list=WAN dst-address-list=nube-nvr action=accept comment="ies-nvr-nube"
  /ip/firewall/filter/add chain=forward src-address=$nvr out-interface-list=WAN action=reject reject-with=icmp-admin-prohibited comment="ies-nvr-resto"
  /ip/firewall/filter/add chain=forward src-address-list=camaras out-interface-list=WAN action=drop comment="ies-camaras-sin-internet" }
# Si ya hay un drop final de zonas (lección 22), estas reglas van arriba de el
:local fin [/ip/firewall/filter/find comment="ies-zona-fin"]
:if ([:len $fin] > 0) do={
  :foreach c in={"ies-nvr-ntp";"ies-nvr-nube";"ies-nvr-resto";"ies-camaras-sin-internet"} do={
    /ip/firewall/filter/move [/ip/firewall/filter/find comment=$c] destination=$fin } }
:put "Listo: admins, cadena gestion-wan, salida del NVR y camaras sin internet."
:put "Verifica con: /ip/firewall/filter/print stats where comment~\\"ies-\\""
}""",
    "notas": [
        "Si entrás desde la WAN para pegarlo, tu IP tiene que ser la de OFICINA_IP: las conexiones nuevas de otras IP al 22 y al 8291 quedan en el log y se descartan. Lo más seguro es pegarlo desde la LAN.",
        "Si limitaste WinBox con available-from (lección de cerrar puertas), sumá ahí también la IP de la oficina.",
        "El DNS del NVR conviene que sea el router: es input y ya está permitido desde la LAN. Si el NVR usa un DNS público, la regla de reject lo corta.",
        "No hace el ping limitado ni las reglas con horario: el ping desde WAN lo resuelve el script de la lección de reglas de protección, y el horario de invitados se arma a mano con los valores del cliente.",
        "Para deshacer: /ip/firewall/filter/remove [find comment~\"^ies-(gestion-wan|nvr|camaras)\"] y /ip/firewall/address-list/remove [find comment~\"^ies-(nube-nvr|camaras)\"].",
    ],
}

E4 = {
    "fig": {
        "file": "4.svg",
        "alt": "Internet a la izquierda y la LAN con NVR y PCs a la derecha. Una flecha input va desde internet a los servicios del propio router (WinBox, SSH, DNS, API). Otra flecha forward atraviesa el router hacia la LAN. Abajo, tres reglas en orden: accept para admins al 8291, accept established y related, y drop de lo que no viene de la LAN.",
        "caption": "input es lo que va al router; forward, lo que pasa a través. Y se lee de arriba abajo.",
    },
    "steps": [
        {
            "file": "4-paso2.svg", "step": 2,
            "alt": "El camino del paquete de izquierda a derecha: entra por una interfaz, pasa por prerouting (raw, connection tracking y dst-nat resaltado), llega a la decisión de ruteo que pregunta si el destino es una IP del router. Si es así va a input y al router (WinBox, DNS, ping); si no, a forward. Lo que genera el router baja por output. Todo sale por postrouting, donde está el src-nat (masquerade). Una nota dice que el dst-nat cambia el destino antes de la decisión, así que un port forwarding cae en forward. Abajo, tres ejemplos: ping a 192.168.88.1 va a input, ping a 1.1.1.1 a forward y el ping desde el router a output.",
            "caption": "El dst-nat va antes de decidir el camino; el masquerade, después del filter.",
            "after": "Mirá el camino del paquete",
        },
        {
            "file": "4-paso4.svg", "step": 4,
            "alt": "A la izquierda, las reglas de la cadena input en orden: accept established, drop invalid, accept ICMP, un jump resaltado a gestion-wan para WAN TCP 22 y 8291, y el drop de lo que no viene de LAN. Una flecha jump lleva a la cadena gestion-wan, con accept para la lista admins y drop con log-prefix GESTION-WAN; una flecha punteada vuelve a input si nadie decide. Abajo, 203.0.113.25 en admins entra por WinBox (verde) y 198.51.100.7 queda en el log y se descarta (rojo). Una terminal muestra la línea del log con el prefijo GESTION-WAN.",
            "caption": "jump ordena la gestión desde WAN en una cadena propia; log-prefix la hace fácil de buscar.",
            "after": "Ejemplo 1: WinBox y SSH desde WAN",
        },
        {
            "file": "4-paso9.svg", "step": 9,
            "alt": "Arriba, el comando print stats de forward. Dos tablas con números de ejemplo. Bien ordenado: NVR a NTP 12 paquetes, NVR a su nube 340, NVR resto 25. Con el reject arriba por error: NVR resto 377 y las dos reglas accept en 0, en rojo. Notas: manda la primera que coincide y move la devuelve a su lugar; si no sube ninguna, el tráfico no llega y se mira con Torch.",
            "caption": "La regla que suma es la que coincide; la de abajo queda en 0 aunque esté bien escrita.",
            "after": "Diagnóstico, en este orden",
        },
    ],
    "concepts": CONCEPTS_4,
    "teoria_md": TEORIA_4,
    "script_rsc": SCRIPT_4,
}

# ---------------------------------------------------------------- lección 22
TEORIA_36 = """### Un poco de historia

Los primeros firewalls de routers se escribían interfaz por interfaz: una lista de acceso en la entrada de cada puerto. En Cisco IOS, el firewall clásico (CBAC) aplicaba la inspección por interfaz. Con dos o tres redes alcanzaba; con diez, cada servicio nuevo obligaba a tocar varias listas y nadie podía decir de un vistazo qué red hablaba con cuál.

La respuesta de la industria fueron las zonas. Cisco sumó su Zone-Based Policy Firewall con IOS 12.4(6)T: cada interfaz pertenece a una zona, las interfaces de una misma zona se hablan, y la política se escribe para un par de zonas (zone-pair), una por sentido. El router mismo es una zona más, la self zone. Fortinet hace algo parecido en FortiGate: agrupa VLAN, puertos o túneles IPsec en una zona y la política nombra la zona, no cada interfaz.

Netfilter, la base del firewall de Linux y de RouterOS, no tiene zonas propias: tiene cadenas, reglas y la interfaz de entrada y de salida. MikroTik resolvió el agrupamiento con las interface lists de RouterOS 6, que ya en 6.41 se usaban también para elegir dónde anunciarse con descubrimiento de vecinos. La configuración por defecto trae dos, LAN y WAN, y todas sus reglas las usan. Con eso, el firewall por zonas en MikroTik no es una función especial: es una forma de escribir.

### Cómo funciona

Una interface list es un conjunto de interfaces con nombre. Hay cuatro fijas (`all`, `none`, `dynamic`, `static`) y las que crees vos. Una lista se arma en tres pasos y en este orden: se suman los miembros de las listas de `include`, se restan los de `exclude` y al final se agregan los miembros estáticos. Lo que entra por `include` no aparece en `/interface/list/member/print`.

Cuando un paquete llega a una regla con `in-interface-list=CCTV`, el router pregunta si la interfaz por la que entró está en esa lista. `out-interface-list` pregunta lo mismo por la interfaz de salida, que recién se conoce después de la decisión de ruteo: por eso tiene sentido en forward y no en input.

La zona agrupa interfaces ruteadas, no equipos. Dos equipos en la misma red del bridge se hablan sin pasar por el router, y ninguna regla los ve. Por eso el orden en obra es VLAN primero, zonas después.

La matriz se traduce así: en forward, una regla accept por casillero permitido con la zona de origen y la de destino, una regla que deja pasar lo dst-nateado y un drop al final; en input, qué servicios del router ve cada zona, arriba del drop de fábrica. Una interfaz nueva hereda la política en el momento en que entra a su lista."""

CONCEPTS_36 = [
    {
        "name": "La zona es una interface list",
        "para_que": "En un edificio con cámaras, control de acceso, administración e invitados, las reglas escritas interfaz por interfaz se multiplican y nadie puede auditarlas. La zona agrupa las interfaces que merecen la misma confianza, y las reglas hablan de zonas.",
        "como": "Creás una lista por zona (`/interface/list/add name=CCTV`) y metés en cada una sus interfaces ruteadas: la VLAN, el bridge, un puerto suelto, la PPPoE o el túnel. Cada interfaz va en una sola zona. Los puertos que están dentro de un bridge no van: el tráfico ruteado entra por el bridge o por la VLAN, no por ether3.",
        "ejemplo": "En un edificio de oficinas de Ciudad Vieja, `vlan20-cctv` del subsuelo y `vlan21-cctv` de la azotea van a la lista CCTV. Las reglas dicen `in-interface-list=CCTV` una vez, y valen para las dos."
    },
    {
        "name": "La matriz de zonas y el drop final",
        "para_que": "Una tabla de \"de, a\" obliga a decidir qué tiene que hablar con qué antes de escribir reglas, y deja a la vista lo que no se pensó. Con un drop al final de forward, todo lo que no está en la tabla queda cortado.",
        "como": "Dibujá la matriz con las zonas en filas y columnas, y una columna más para el router. Cada casillero verde o ámbar es una regla: en forward con `in-interface-list` y `out-interface-list`, en input con `in-interface-list` y el servicio. Los rojos no se escriben. Antes del drop final va el accept de `connection-nat-state=dstnat`, o se caen los port forwarding. En un sitio en uso, el último renglón empieza como `action=log` y pasa a drop cuando el log queda limpio.",
        "ejemplo": "Un hotel en Punta del Este pide que el WiFi de huéspedes no vea las cámaras. En la matriz, INVITADOS a CCTV queda en rojo: no se escribe nada y el drop final lo resuelve. Si un día el gerente quiere ver el NVR desde administración, se pinta un casillero ámbar y se agrega una regla con el puerto del NVR."
    },
    {
        "name": "include, exclude y listas compuestas",
        "para_que": "Algunas reglas valen para varias zonas a la vez: DNS y DHCP para todos los clientes, NTP para los sistemas de seguridad. En vez de repetir la regla por zona, se arma una lista que junta otras listas.",
        "como": "`/interface/list/add name=SISTEMAS include=CCTV,ACCESOS` crea una lista que siempre tiene lo que tengan CCTV y ACCESOS. `exclude` resta, y los miembros estáticos se suman al final, así que un miembro estático gana sobre un exclude. Conviene usar include solo para grupos evidentes y no armar listas que incluyan listas compuestas: el print de miembros no muestra lo que entra por include y cuesta seguirlo.",
        "ejemplo": "Una regla `in-interface-list=SISTEMAS out-interface-list=WAN protocol=udp dst-port=123` deja sincronizar la hora a las cámaras y a la controladora de accesos. Cuando el cliente suma una zona de alarmas, la incluís en SISTEMAS y ya tiene NTP."
    },
    {
        "name": "Interfaces nuevas, PPPoE y túneles",
        "para_que": "Una obra cambia: llega otra VLAN, la WAN pasa de DHCP a PPPoE, se suman técnicos por VPN. Si la política vive en las listas, el firewall no se toca: se actualiza la membresía.",
        "como": "Para una interfaz estática alcanza con `/interface/list/member/add list=ADMIN interface=vlan10-admin`. Una `pppoe-out1` creada a mano también es estática y va a la lista WAN, o las reglas de WAN y el masquerade no la ven. Las interfaces de servidor L2TP o SSTP son dinámicas: aparecen al conectar, y entran a una lista desde el perfil con `/ppp/profile/set ... interface-list=VPN`.",
        "ejemplo": "Antel cambia el servicio de un cliente a PPPoE. El técnico crea `pppoe-out1`, la suma a WAN y listo: el drop de lo que entra por WAN sin dst-nat, la regla del túnel y el masquerade siguen funcionando sin tocar una sola regla."
    },
]

SCRIPT_36 = {
    "titulo": "Zonas de un edificio y su matriz de reglas",
    "descripcion": "Crea las listas GESTION, ADMIN, CCTV, ACCESOS, INVITADOS y VPN con la interfaz de cada una, las compuestas SISTEMAS y CLIENTES, las reglas de input por zona y las de forward por par de zonas. El drop final queda en modo ensayo (solo log) hasta que lo pases a drop.",
    "variables": [
        {"nombre": "IF_GESTION", "valor": "vlan99-gestion", "detalle": "Interfaz de la zona de gestión (técnicos, switches, APs). En el banco: bridge"},
        {"nombre": "IF_ADMIN", "valor": "vlan10-admin", "detalle": "Interfaz de la zona de administración"},
        {"nombre": "IF_CCTV", "valor": "vlan20-cctv", "detalle": "Interfaz de la zona de cámaras y NVR"},
        {"nombre": "IF_ACCESOS", "valor": "vlan30-accesos", "detalle": "Interfaz de la zona de control de acceso"},
        {"nombre": "IF_INVITADOS", "valor": "vlan40-invitados", "detalle": "Interfaz de la zona de WiFi de invitados"},
        {"nombre": "IF_VPN", "valor": "wg-gestion", "detalle": "Túnel de los técnicos (zona VPN)"},
        {"nombre": "NVR_IP", "valor": "10.10.20.50", "detalle": "IP del NVR que administración puede ver"},
        {"nombre": "PUERTO_VPN", "valor": "13231", "detalle": "Puerto UDP del túnel que se acepta desde WAN"},
    ],
    "codigo": """# IES Training · MikroTik · Zonas con interface lists (lección 22)
# Probalo primero en un equipo de banco y en Safe Mode (Ctrl+X).
# Requiere el firewall por defecto. El drop final queda en ensayo: solo log.
{
:local zonas {"GESTION"="{{IF_GESTION}}";"ADMIN"="{{IF_ADMIN}}";"CCTV"="{{IF_CCTV}}";"ACCESOS"="{{IF_ACCESOS}}";"INVITADOS"="{{IF_INVITADOS}}";"VPN"="{{IF_VPN}}"}
:local nvr "{{NVR_IP}}"
:local vpn "{{PUERTO_VPN}}"
:local drop [/ip/firewall/filter/find chain=input comment="defconf: drop all not coming from LAN"]
:if ([:len $drop] = 0) do={ :error "No encuentro el drop de la defconf: revisa el firewall a mano" }
# 1. Una lista por zona, con su interfaz si existe
:foreach z,i in=$zonas do={
  :if ([:len [/interface/list/find name=$z]] = 0) do={ /interface/list/add name=$z comment="ies-zona" }
  :if ([:len [/interface/find name=$i]] = 0) do={ :put ("Ojo: no existe " . $i . ", la zona " . $z . " queda vacia") } else={
    :if ([:len [/interface/list/member/find list=$z interface=$i]] = 0) do={ /interface/list/member/add list=$z interface=$i comment="ies-zona" } } }
# 2. Compuestas: VPN cuenta como gestion; SISTEMAS y CLIENTES
/interface/list/set [find name=GESTION] include=VPN
:if ([:len [/interface/list/find name=SISTEMAS]] = 0) do={ /interface/list/add name=SISTEMAS include=CCTV,ACCESOS comment="ies-zona" }
:if ([:len [/interface/list/find name=CLIENTES]] = 0) do={ /interface/list/add name=CLIENTES include=ADMIN,CCTV,ACCESOS,INVITADOS comment="ies-zona" }
# 3. Input por zona, arriba del drop de fabrica (solo accepts: no corta a nadie)
:if ([:len [/ip/firewall/filter/find comment="ies-zona-in-gestion"]] = 0) do={
  /ip/firewall/filter/add chain=input in-interface-list=GESTION action=accept comment="ies-zona-in-gestion" place-before=$drop
  /ip/firewall/filter/add chain=input in-interface-list=CLIENTES protocol=udp dst-port=53,67 action=accept comment="ies-zona-in-dns-dhcp" place-before=$drop
  /ip/firewall/filter/add chain=input in-interface-list=CLIENTES protocol=tcp dst-port=53 action=accept comment="ies-zona-in-dns-tcp" place-before=$drop
  /ip/firewall/filter/add chain=input in-interface-list=WAN protocol=udp dst-port=$vpn action=accept comment="ies-zona-in-tunel" place-before=$drop }
# 4. Forward: primero el renglon final (ensayo), despues un accept por casillero
:if ([:len [/ip/firewall/filter/find comment="ies-zona-fin"]] = 0) do={
  /ip/firewall/filter/add chain=forward action=log log-prefix="ZONA-ENSAYO" comment="ies-zona-fin" }
:local fin [/ip/firewall/filter/find comment="ies-zona-fin"]
:if ([:len [/ip/firewall/filter/find comment="ies-zona-gestion"]] = 0) do={
  /ip/firewall/filter/add chain=forward in-interface-list=GESTION action=accept comment="ies-zona-gestion" place-before=$fin
  /ip/firewall/filter/add chain=forward in-interface-list=ADMIN out-interface-list=WAN action=accept comment="ies-zona-admin-wan" place-before=$fin
  /ip/firewall/filter/add chain=forward in-interface-list=INVITADOS out-interface-list=WAN action=accept comment="ies-zona-invitados-wan" place-before=$fin
  /ip/firewall/filter/add chain=forward in-interface-list=ADMIN out-interface-list=CCTV dst-address=$nvr protocol=tcp dst-port=80,443,8000 action=accept comment="ies-zona-admin-nvr" place-before=$fin
  /ip/firewall/filter/add chain=forward in-interface-list=SISTEMAS out-interface-list=WAN protocol=udp dst-port=123 action=accept comment="ies-zona-sistemas-ntp" place-before=$fin
  /ip/firewall/filter/add chain=forward in-interface-list=WAN connection-nat-state=dstnat action=accept comment="ies-zona-publicado" place-before=$fin }
# Cuando el log ZONA-ENSAYO muestre solo lo que esperabas, pasalo a drop:
# /ip/firewall/filter/set [find comment="ies-zona-fin"] action=drop log=yes log-prefix="ZONA-DROP"
:put "Listo: zonas, compuestas, input por zona y forward por par de zonas (final en ensayo)."
:put "Verifica con: /interface/list/member/print y /ip/firewall/filter/print stats where comment~\\"ies-zona\\""
}""",
    "notas": [
        "Mientras el renglón final esté en ensayo (action=log), lo que no está en la matriz sigue pasando y queda en el log con ZONA-ENSAYO. Miralo unos días con /log/print where message~\"ZONA-ENSAYO\" antes de pasarlo a drop.",
        "En input solo agrega accepts: las zonas que no están en la lista LAN ya las corta el drop de fábrica, salvo DNS, DHCP y el túnel.",
        "Si una interfaz no existe, el script avisa y deja la zona vacía: cuando la crees, sumala con /interface/list/member/add.",
        "No crea VLANs, IPs, servidores DHCP ni el túnel WireGuard: eso es de las lecciones de VLAN, IP, DHCP y túnel de gestión.",
        "En obra conviene que la lista LAN de fábrica sea la de gestión (/interface/list/set LAN include=GESTION y sacar el miembro suelto). El script no lo hace porque cambia desde dónde se administra el router.",
        "Para deshacer: /ip/firewall/filter/remove [find comment~\"^ies-zona\"], /interface/list/member/remove [find comment=\"ies-zona\"] y /interface/list/remove [find comment=\"ies-zona\"].",
    ],
}

E36 = {
    "fig": {
        "file": "36.svg",
        "alt": "Una tabla con las zonas de origen en filas (GESTION más VPN, ADMIN, CCTV, ACCESOS, INVITADOS, WAN) y las de destino en columnas (WAN, GESTION, ADMIN, CCTV, ACCESOS, INVITADOS y el router). GESTION y VPN pueden todo, en verde. ADMIN e INVITADOS salen a WAN en verde. ADMIN a CCTV solo el NVR, en ámbar. CCTV y ACCESOS a WAN solo NTP, en ámbar. Todas las zonas ven DNS y DHCP del router, en ámbar. Desde WAN, solo lo publicado con dst-nat y el túnel. El resto, en rojo. Leyenda: verde es una regla accept, ámbar un accept con puerto o destino, rojo lo corta el drop final.",
        "caption": "Cada casillero verde o ámbar es una regla; los rojos no se escriben.",
    },
    "steps": [
        {
            "file": "36-paso2.svg", "step": 2,
            "alt": "Tres columnas. Interfaces del banco: bridge (ether2), ether3, ether4, ether5, wg-gestion y, punteada, vlan10-admin que entra en el paso 6. Cada una apunta a su zona: GESTION, CCTV, ACCESOS, INVITADOS, VPN y ADMIN. A la derecha, las listas compuestas: GESTION con include=VPN, SISTEMAS con include=CCTV,ACCESOS para NTP, y CLIENTES con include de ADMIN, CCTV, ACCESOS e INVITADOS para DNS y DHCP. Una nota explica el orden: include suma, exclude resta, los miembros estáticos suman al final, y member print solo muestra los estáticos.",
            "caption": "Una interfaz, una zona; las listas compuestas se arman por include.",
            "after": "Creá las zonas y sus miembros",
        },
        {
            "file": "36-paso4.svg", "step": 4,
            "alt": "Dos paquetes del NVR 10.10.20.50 que entra por ether3, zona CCTV. El primero, UDP 123 hacia WAN, baja por la lista de reglas de forward y coincide con SISTEMAS a WAN udp 123, en verde. El segundo, TCP 443 para navegar, no coincide con ningún casillero y termina en el drop final con log ZONA-DROP, en rojo. Las reglas en orden: GESTION a todas, ADMIN a WAN, INVITADOS a WAN, ADMIN al NVR, SISTEMAS a WAN, WAN a lo publicado y drop final.",
            "caption": "Lo que coincide con un casillero pasa; lo demás baja hasta el drop final.",
            "after": "Forward por par de zonas",
        },
        {
            "file": "36-paso6.svg", "step": 6,
            "alt": "Una terminal con tres líneas: crear vlan10-admin sobre el bridge, darle 10.10.10.1/24 y sumarla a la lista ADMIN, resaltada en verde. A la derecha, vlan10-admin entra a ADMIN y ya le aplican ADMIN a WAN, ADMIN al NVR y DNS y DHCP, con tildes verdes, y WinBox al router no, con una cruz roja. Dos notas: si la WAN pasa a PPPoE, pppoe-out1 va a la lista WAN; los túneles L2TP o SSTP del servidor son dinámicos y entran a VPN desde el perfil PPP con interface-list.",
            "caption": "Lo nuevo se suma a la lista; las reglas no cambian.",
            "after": "Una red nueva, sin tocar reglas",
        },
    ],
    "concepts": CONCEPTS_36,
    "teoria_md": TEORIA_36,
    "script_rsc": SCRIPT_36,
}

json.dump({"4": E4}, open(OUT + "manifest-4b.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump({"36": E36}, open(OUT + "manifest-36.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok")
