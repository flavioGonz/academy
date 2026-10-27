"""Genera ilustraciones/omada/glosario-propuesta.json y lo prueba sobre una copia combinada del glosario.

  python3 glosario_om.py            # escribe la propuesta y valida la copia en /tmp/claude-0/glosario-omada.json

La propuesta tiene tres partes:
- terms: entradas nuevas completas (id, term, aliases, cat, short, long, year si corresponde, case).
- alias_agregar: alias nuevos para entradas que ya existen.
- modificar: campos a reemplazar en entradas existentes (solo los indicados).
No toca site2/data/glosario.json.
"""
import json, subprocess, sys

T = [
    {"id": "eap-omada", "term": "EAP", "aliases": ["EAPs", "access point EAP"], "cat": "Redes",
     "short": "El nombre de los access points de TP-Link Omada, como el EAP225, el EAP610 o el EAP660.",
     "long": "Se gestionan desde el controlador Omada o, sin controlador, desde su propia web en modo standalone. Ojo con la sigla: en seguridad WiFi, EAP también es Extensible Authentication Protocol, el marco de autenticación de 802.1X y de WPA2 y WPA3 Enterprise (RFC 3748, de 2004).",
     "case": True},
    {"id": "omada", "term": "Omada", "aliases": ["TP-Link Omada", "Omada SDN", "Omada SDN Controller", "Omada Controller", "controlador Omada"], "cat": "Redes",
     "short": "La plataforma de redes administradas de TP-Link: gateways ER, switches JetStream y access points EAP gestionados desde un controlador.",
     "long": "Las primeras versiones del controlador gestionaban los access points EAP; con la 4.1.5 pasó a llamarse Omada SDN Controller y sumó gateways y switches. Hoy el controlador puede ser software propio, un OC de hardware, Omada Central en la nube o un gateway con controlador integrado.",
     "case": True},
    {"id": "avx", "term": "AVX", "aliases": ["Advanced Vector Extensions"], "cat": "Herramientas",
     "short": "Advanced Vector Extensions: instrucciones de los procesadores x86 que pide el MongoDB del controlador Omada 6.",
     "long": "Intel las estrenó en 2011 con la generación Sandy Bridge. MongoDB 5.0 y posteriores no arrancan en una CPU x86 sin AVX, por eso el controlador 6.x no corre en equipos viejos ni en una Raspberry Pi 4, que es ARM. En Linux se verifica con grep avx /proc/cpuinfo.",
     "year": 2011, "case": True},
    {"id": "wlan", "term": "WLAN", "aliases": ["Wireless LAN"], "cat": "Redes",
     "short": "Wireless LAN: una red local inalámbrica; en la práctica, la red WiFi.",
     "long": "La define la norma IEEE 802.11, de 1997. En Omada, el menú WLAN agrupa los SSID del sitio y la función WLAN Optimization.",
     "year": 1997, "case": True},
    {"id": "wlan-optimization", "term": "WLAN Optimization", "aliases": ["RRM", "Radio Resource Management", "Adaptive WLAN Optimization"], "cat": "Redes",
     "short": "Función de Omada que elige canal, ancho y potencia de los EAP de forma automática; también se la llama RRM.",
     "long": "Se corre a mano, programada o en modo adaptativo desde Network Config > Network Settings > WLAN. Mientras escanea, los clientes se quedan sin internet varios minutos: se programa de madrugada y al menos 10 minutos lejos del reinicio programado. Apply Previous Settings vuelve a la configuración anterior.",
     "case": True},
    {"id": "omada-hardware-controller", "term": "Omada Hardware Controller", "aliases": ["OC", "OC200", "OC220", "OC300", "OC400"], "cat": "Redes",
     "short": "Los controladores Omada en hardware dedicado: OC200, OC220, OC300 y OC400.",
     "long": "Se eligen por la capacidad recomendada de la tabla oficial: OC200 hasta 25 equipos, OC220 hasta 40, OC300 hasta 160 y OC400 hasta 500. Gestionan sin internet y no necesitan una PC prendida, pero no tienen modo MSP. El upgrade de firmware tarda de 6 a 8 minutos con el equipo offline.",
     "case": True},
    {"id": "sdn", "term": "SDN", "aliases": ["Software-Defined Networking", "redes definidas por software"], "cat": "Redes",
     "short": "Software-Defined Networking: la red se configura desde un controlador central en lugar de equipo por equipo.",
     "long": "La idea viene de la investigación en redes de fines de los años 2000. En el uso comercial, como en Omada SDN, significa que gateways, switches y access points reciben su configuración de un controlador y se gestionan desde una sola interfaz.",
     "case": True},
    {"id": "gui", "term": "GUI", "aliases": ["GUI local", "interfaz gráfica", "web local"], "cat": "Herramientas",
     "short": "Graphical User Interface: la interfaz gráfica de un equipo; en redes, su página web de administración.",
     "long": "En Omada se habla de la GUI local o web standalone de cada equipo. Cuando el controlador adopta el equipo, esa GUI deja de mandar; si alguien la usó antes de adoptar, aparece Adopt Failed pidiendo esas credenciales.",
     "case": True},
    {"id": "sftp", "term": "SFTP", "aliases": ["SSH File Transfer Protocol"], "cat": "Redes",
     "short": "SSH File Transfer Protocol: transferencia de archivos cifrada que viaja dentro de SSH, por el TCP 22.",
     "long": "No es FTP con cifrado sino un protocolo distinto. En Omada es el destino recomendado del Backup Schedule (Save to File Server): el backup queda en otro equipo y sobrevive si muere el controlador.",
     "case": True},
    {"id": "ldap", "term": "LDAP", "aliases": ["Lightweight Directory Access Protocol", "servidor LDAP"], "cat": "Seguridad",
     "short": "Lightweight Directory Access Protocol: el protocolo para consultar directorios de usuarios, como Active Directory.",
     "long": "Su versión vigente, LDAPv3, está en la RFC 4511, de 2006. En Omada, desde la 5.12, el portal cautivo puede autenticar contra un servidor LDAP externo.",
     "case": True},
    {"id": "sms", "term": "SMS", "aliases": ["Short Message Service"], "cat": "Redes",
     "short": "Short Message Service: el mensaje de texto del celular.",
     "long": "En el portal cautivo de Omada es una de las opciones de Hotspot: el cliente recibe un código de verificación en el celular y lo ingresa en el portal.",
     "case": True},
    {"id": "release-candidate", "term": "Release Candidate", "aliases": ["RC", "Early Access"], "cat": "Herramientas",
     "short": "Versión candidata a estable: casi terminada, publicada para probar antes del lanzamiento.",
     "long": "TP-Link ofrece firmware Beta y Release Candidate dentro de su programa Early Access y avisa que puede ser inestable. En producción se usa el canal estable; Beta y RC, solo en laboratorio.",
     "case": True},
    {"id": "heredoc", "term": "heredoc", "aliases": ["here document", "EOF"], "cat": "Herramientas",
     "short": "Here document: forma de la terminal de Linux para escribir un bloque de texto en un archivo o pasárselo a un comando.",
     "long": "Se abre con <<'EOF' y se cierra con una línea que dice solo EOF; todo lo del medio va tal cual. Con las comillas en 'EOF', la terminal no reemplaza variables adentro. En el curso de Omada se usa para crear el docker-compose.yml de una vez.",
     "case": True},
    {"id": "tz", "term": "TZ", "aliases": ["variable TZ"], "cat": "Herramientas",
     "short": "Variable de entorno con la zona horaria, en formato de la base de datos IANA, por ejemplo America/Montevideo.",
     "long": "Un contenedor no siempre toma la zona horaria del host y suele quedar en UTC: los logs y las tareas programadas salen con otra hora. En el controlador Omada en Docker se pasa como TZ=America/Montevideo en el compose.",
     "case": True},
    {"id": "capwap", "term": "CAPWAP", "aliases": ["Control And Provisioning of Wireless Access Points"], "cat": "Redes",
     "short": "Control And Provisioning of Wireless Access Points: el estándar del IETF para que access points y controladores se encuentren y se gestionen.",
     "long": "Se publicó en 2009 (RFC 5415). La RFC 5417, del mismo año, le asignó la opción 138 de DHCP para decirle al AP dónde está su controlador. TP-Link usa ese mismo número de opción en Omada para indicar la IP del controlador.",
     "year": 2009, "case": True},
    {"id": "chap", "term": "CHAP", "aliases": ["Challenge Handshake Authentication Protocol"], "cat": "Seguridad",
     "short": "Challenge Handshake Authentication Protocol: autenticación en la que la clave no viaja, sino una respuesta calculada a un desafío.",
     "long": "Viene de PPP y está en la RFC 1994, de 1996. Su alternativa simple es PAP, que manda la clave tal cual. En el portal de Omada con RADIUS se elige PAP o CHAP; CHAP está desde la 5.12.",
     "year": 1996, "case": True},
    {"id": "rfc2865", "term": "RFC 2865", "aliases": ["RFC2865"], "cat": "RFC",
     "short": "RADIUS: el protocolo para autenticar usuarios contra un servidor central.",
     "long": "Es la versión vigente de RADIUS, de 2000, y usa UDP 1812 para autenticar. La contabilidad (accounting) va aparte, en la RFC 2866. En WiFi Enterprise y en portales cautivos, el AP o el controlador le pregunta al servidor RADIUS si el usuario vale.",
     "year": 2000, "case": True},
    {"id": "rfc5417", "term": "RFC 5417", "aliases": ["RFC5417"], "cat": "RFC",
     "short": "La opción 138 de DHCP: la lista de direcciones de los controladores de access points (CAPWAP).",
     "long": "Es de 2009. El servidor DHCP entrega, junto con la IP, las direcciones IPv4 de los controladores, 4 bytes cada una. TP-Link usa la opción 138 en Omada para que los equipos encuentren el controlador desde otra subred.",
     "year": 2009, "case": True},
    {"id": "opcion-138", "term": "opción 138", "aliases": ["option 138", "DHCP option 138"], "cat": "Redes",
     "short": "Opción de DHCP que le dice a un equipo Omada la IP de su controlador.",
     "long": "La definió la RFC 5417, de 2009, para controladores de access points. En un gateway Omada se carga la IP tal cual en Advanced DHCP Options; en un MikroTik va en hexadecimal, un byte por octeto (192.168.88.10 queda 0xC0A8580A). Solo llega cuando el equipo renueva el DHCP.",
     "year": 2009, "case": False},
    {"id": "inform-url", "term": "Inform URL", "aliases": ["Site URL", "Controller Inform URL"], "cat": "Redes",
     "short": "La dirección del controlador Omada que se le escribe a un equipo para que lo encuentre desde otra subred.",
     "long": "Se carga en la web standalone del equipo, en System Tools > Controller Settings, o en lote con la Omada Discovery Utility. Para Omada Central se usa la Site URL que se copia en Global View > Dashboard. También sirve para migrar equipos a un controlador nuevo.",
     "case": True},
    {"id": "portal-cautivo", "term": "portal cautivo", "aliases": ["portales cautivos", "captive portal"], "cat": "Redes",
     "short": "Página que aparece antes de dar internet en un WiFi, para autenticar al cliente o mostrarle condiciones.",
     "long": "En Omada lo sirve el controlador, por el 8088 en HTTP o el 8843 en HTTPS, así que sin controlador corriendo los clientes nuevos no se autentican. Puede pedir voucher, clave, usuario local, SMS, RADIUS o LDAP.",
     "case": False},
    {"id": "voucher", "term": "voucher", "aliases": ["vouchers"], "cat": "Redes",
     "short": "Código de acceso con duración que genera el controlador para entrar por el portal cautivo.",
     "long": "Se usa en hotelería y locales: el cliente recibe su código en recepción y deja de servir al vencer, sin cambiar claves. En Omada se genera en la sección Voucher de un portal tipo Hotspot.",
     "case": False},
    {"id": "mesh", "term": "mesh", "aliases": ["red mesh", "Mesh AP", "Root AP"], "cat": "Redes",
     "short": "Access points enlazados por radio entre sí, sin cable de datos, a partir de uno cableado (Root AP).",
     "long": "Sirve para extender cobertura, no capacidad: cada salto resta rendimiento. En Omada admite hasta 3 saltos y 4 downlinks por uplink, con señal del uplink entre -40 y -62 dBm.",
     "case": False},
]

ALIAS = {"gateway": ["GW"]}

MOD_FAST_ROAMING_EXTRA = " Ojo con los nombres: en Omada, el interruptor Fast Roaming de Site Settings > Wireless Features activa 802.11k y 802.11v; 802.11r se habilita aparte en cada SSID."

GLOS = "/home/claude/ies-training/site2/data/glosario.json"
OUT = "/home/claude/ies-training/ilustraciones/omada/glosario-propuesta.json"
COMB = "/tmp/claude-0/glosario-omada.json"

g = json.load(open(GLOS, encoding="utf-8"))
by = {t["id"]: t for t in g["terms"]}
fr_long = by["fast-roaming"]["long"]
P = {
    "nota": "Propuesta para el curso Omada. terms: entradas nuevas completas. alias_agregar: alias nuevos para entradas existentes. modificar: campos a reemplazar en entradas existentes. Probada sobre una copia combinada con glosario_check.py.",
    "terms": T,
    "alias_agregar": ALIAS,
    "modificar": {"fast-roaming": {"long": fr_long if MOD_FAST_ROAMING_EXTRA.strip() in fr_long else fr_long + MOD_FAST_ROAMING_EXTRA}},
}
json.dump(P, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# copia combinada
dup = [t["id"] for t in T if t["id"] in by]
if dup:
    sys.exit(f"ids que ya existen en el glosario: {dup}")
g["terms"] += T
for k, al in ALIAS.items():
    by[k]["aliases"] += [a for a in al if a not in by[k]["aliases"]]
for k, ch in P["modificar"].items():
    by[k].update(ch)
json.dump(g, open(COMB, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
s = json.dumps(P, ensure_ascii=False)
print("ok", OUT, len(T), "entradas;", "guiones largos:", "—" in s or "–" in s)
r = subprocess.run([sys.executable, "/home/claude/ies-training/tools/glosario_check.py", "omada", "--glosario", COMB], capture_output=True, text=True)
print(r.stdout, r.stderr, "exit", r.returncode)
