#!/usr/bin/env python3
"""Genera manifest-scripts-12-24.json (campo script_rsc de las lecciones 12 a 24 del curso MikroTik).

Los scripts estan aca como texto crudo para no escapar comillas a mano. Regenerar con:
  python3 /home/claude/ies-training/ilustraciones/mikrotik/src/scripts_12_24.py
y validar con:
  python3 /home/claude/ies-training/tools/rsc_check.py
"""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "manifest-scripts-12-24.json"

S = {}

# ---------------------------------------------------------------- 12
S["12"] = dict(
    titulo="Diagnosticar un equipo: ping, Torch, captura y log temporal",
    descripcion="Pregunta si hay camino, mira 10 segundos de flujos del equipo con Torch, captura a un .pcap con límite y prende el log del drop invalid de fábrica solo mientras dura la captura. No deja nada cambiado.",
    variables=[
        {"nombre": "IP_EQUIPO", "valor": "192.168.88.50", "detalle": "IP de la cámara o PC que estás diagnosticando"},
        {"nombre": "INTERFAZ_LAN", "valor": "bridge", "detalle": "Interfaz LAN donde mirar (el bridge, no la WAN)"},
        {"nombre": "DESTINO", "valor": "8.8.8.8", "detalle": "IP de internet para ping y traceroute"},
        {"nombre": "ARCHIVO_PCAP", "valor": "camara.pcap", "detalle": "Nombre del archivo de captura en Files"},
        {"nombre": "DURACION", "valor": "30s", "detalle": "Cuánto dura la captura (corta en producción)"},
    ],
    codigo=r'''# IES Training - MikroTik - Leccion 12: Torch y sniffer
# Solo diagnostico: al terminar vuelve el log a como estaba. Torch y sniffer suben la CPU.
{
  :local equipo "{{IP_EQUIPO}}"
  :local lan "{{INTERFAZ_LAN}}"
  :local destino "{{DESTINO}}"
  :local archivo "{{ARCHIVO_PCAP}}"
  :local duracion [:totime "{{DURACION}}"]
  # 1. Preguntar: hay camino
  :local ok [/ping $destino count=5]
  :put ("Ping a " . $destino . ": " . $ok . " de 5 respuestas")
  /tool/traceroute $destino count=1
  # 2. Mirar: flujos del equipo en vivo, 10 segundos
  /tool/torch interface=$lan src-address=($equipo . "/32") duration=10s
  # 4. Registrar: log temporal en los drop invalid de fabrica (si estan)
  :local regla [/ip/firewall/filter/find comment="defconf: drop invalid"]
  :if ([:len $regla] > 0) do={ /ip/firewall/filter/set $regla log=yes log-prefix="DROP-INV" }
  # 3. Capturar a archivo, con limite para no llenar el disco
  /tool/sniffer/set file-name=$archivo file-limit=10000KiB
  /tool/sniffer/start interface=$lan ip-address=($equipo . "/32")
  :delay $duracion
  /tool/sniffer/stop
  # Log de vuelta a no, y lo que registro mientras tanto
  :if ([:len $regla] > 0) do={ /ip/firewall/filter/set $regla log=no }
  /log/print where message~"DROP-INV"
  :local f [/file/find where name~$archivo]
  :if ([:len $f] = 0) do={ :put "No se creo el archivo de captura: revisa el nombre y el espacio libre" } else={
    :local tam [:tonum [/file/get [:pick $f 0] size]]
    :put ("Captura: " . [/file/get [:pick $f 0] name] . " (" . $tam . " bytes)")
    :if ($tam <= 24) do={ :put "Pesa 24 bytes o menos: no capturo nada. Revisa IP e interfaz." }
  }
  :put "Listo: ping, traceroute, Torch, captura y log temporal. Baja el .pcap de Files y abrilo en Wireshark (filtro rtsp o dns)."
  :put "Verifica: /file/print where name~\"pcap\""
}''',
    notas=[
        "Torch muestra la tabla 10 segundos y sigue: si el tráfico del equipo cae a cero a ratos, mirá cámara y cable; si fluye parejo, mirá el NVR.",
        "El script vuelve a dejar log=no en las reglas \"defconf: drop invalid\". Si no tenés la configuración por defecto, elegí a mano la regla de drop que sospeches (paso 4 del laboratorio).",
        "No borra el .pcap: bajalo desde Files y borralo después para no llenar el disco.",
        "Para una captura más larga o con otro filtro (puerto 554, por ejemplo), usá los comandos del laboratorio a mano.",
    ],
)

# ---------------------------------------------------------------- 13
S["13"] = dict(
    titulo="Cargar una IP fija en la WAN y probarla por capas",
    descripcion="Hace un export de antes, apaga el cliente DHCP de la WAN, carga dirección, ruta por defecto y DNS del proveedor y prueba gateway, internet y resolución de nombres. Si se pega dos veces, corrige lo cargado en vez de duplicarlo.",
    variables=[
        {"nombre": "WAN", "valor": "ether1", "detalle": "Interfaz que va al proveedor"},
        {"nombre": "WAN_IP", "valor": "203.0.113.10/29", "detalle": "IP fija con máscara que entregó el proveedor"},
        {"nombre": "GATEWAY", "valor": "203.0.113.9", "detalle": "Gateway del proveedor"},
        {"nombre": "DNS", "valor": "1.1.1.1,9.9.9.9", "detalle": "Servidores DNS separados por coma, sin espacios"},
    ],
    codigo=r'''# IES Training - MikroTik - Leccion 13: IP fija en la WAN
# Probalo primero en un equipo de banco y en Safe Mode (Ctrl+X): un gateway mal escrito te deja afuera.
{
  :local wan "{{WAN}}"
  :local ip "{{WAN_IP}}"
  :local gw [:toip "{{GATEWAY}}"]
  # Foto de antes (leccion 6)
  /export file=ies-antes-ip-fija
  # 1. El cliente DHCP de la WAN se apaga para que no compita
  /ip/dhcp-client/disable [find interface=$wan]
  # 2. Direccion: si ya esta (por comentario o por IP), se corrige; si no, se agrega
  :local a [/ip/address/find where comment="ies-WAN fija"]
  :if ([:len $a] = 0) do={ :set a [/ip/address/find where address=$ip interface=$wan] }
  :if ([:len $a] = 0) do={ /ip/address/add address=$ip interface=$wan comment="ies-WAN fija" } else={ /ip/address/set $a address=$ip interface=$wan comment="ies-WAN fija" }
  :local r [/ip/route/find where comment="ies-default WAN fija"]
  :if ([:len $r] = 0) do={ /ip/route/add dst-address=0.0.0.0/0 gateway=$gw comment="ies-default WAN fija" } else={ /ip/route/set $r gateway=$gw }
  /ip/dns/set servers={{DNS}}
  # 3. Verificar por capas
  :delay 2s
  :local p1 [/ping $gw count=3]
  :local p2 [/ping 1.1.1.1 count=3]
  :local nombre "sin resolver"
  :do { :set nombre [:tostr [:resolve mikrotik.com]] } on-error={}
  :put ("Gateway " . $gw . ": " . $p1 . "/3 | Internet 1.1.1.1: " . $p2 . "/3 | mikrotik.com: " . $nombre)
  :if ($p1 = 0) do={ :put "Gateway sin respuesta: cable, mascara o VLAN." }
  :if ($p1 > 0 && $p2 = 0) do={ :put "Internet sin respuesta: ruta o proveedor." }
  :if ($p2 > 0 && $nombre = "sin resolver") do={ :put "Nombre sin resolver: DNS." }
  # 4. IP directa: public-address de IP Cloud tiene que ser la misma IP (con DDNS activo)
  :local pub ""
  :do { :set pub [:tostr [/ip/cloud/get public-address]] } on-error={}
  :put ("public-address: " . $pub . " | IP WAN: " . [:pick $ip 0 [:find $ip "/"]])
  :put "Listo: WAN fija con direccion, ruta y DNS. Anota en el legajo IP, mascara, gateway, DNS y quien los entrego."
  :put "Verifica: /ip/route/print where dst-address=0.0.0.0/0"
}''',
    notas=[
        "Si entrás al router por la IP que entrega el DHCP de esa WAN, la sesión se corta al apagar el cliente: pegalo desde la LAN o en Safe Mode.",
        "El masquerade de fábrica sigue andando con IP fija; cambiarlo a src-nat es opcional y no lo hace este script.",
        "public-address vacío: activá DDNS (lección 28) y volvé a mirar /ip/cloud/print.",
        "Para volver atrás: /ip/address/remove [find comment=\"ies-WAN fija\"], /ip/route/remove [find comment=\"ies-default WAN fija\"] y /ip/dhcp-client/enable [find interface=ether1].",
    ],
)

# ---------------------------------------------------------------- 14
S["14"] = dict(
    titulo="Cliente DHCP en la WAN: distancia, lease nuevo y doble NAT",
    descripcion="Deja el cliente DHCP de la WAN con la distancia de ruta elegida (1 principal, 2 o más respaldo), pide un lease nuevo, muestra lo que recibió y avisa si la IP es privada (doble NAT) o de CGNAT.",
    variables=[
        {"nombre": "WAN", "valor": "ether1", "detalle": "Interfaz conectada al módem o router que entrega DHCP"},
        {"nombre": "DISTANCIA", "valor": "2", "detalle": "default-route-distance: 1 si es la WAN principal, 2 o más si es el respaldo"},
    ],
    codigo=r'''# IES Training - MikroTik - Leccion 14: Cliente DHCP en la WAN
# Probalo primero en un equipo de banco. Si es la unica WAN y entras por ella, en Safe Mode (Ctrl+X).
{
  :local wan "{{WAN}}"
  :local dist {{DISTANCIA}}
  :local c [/ip/dhcp-client/find interface=$wan]
  :if ([:len $c] = 0) do={
    # No hay cliente: se crea solo si la interfaz no tiene IP fija, para que no compitan
    :if ([:len [/ip/address/find interface=$wan dynamic=no]] > 0) do={ :error "La WAN tiene IP fija: sacala antes (leccion 13)" }
    /ip/dhcp-client/add interface=$wan add-default-route=yes use-peer-dns=yes use-peer-ntp=yes default-route-distance=$dist comment="ies-dhcp-wan" disabled=no
    :set c [/ip/dhcp-client/find interface=$wan]
  } else={
    /ip/dhcp-client/set $c default-route-distance=$dist disabled=no
  }
  # 3. Lease nuevo sin esperar
  /ip/dhcp-client/renew $c
  :delay 5s
  # 1. Lo que recibio
  :local st [:tostr [/ip/dhcp-client/get $c status]]
  :local addr [:tostr [/ip/dhcp-client/get $c address]]
  :put ("status=" . $st . " address=" . $addr . " gateway=" . [/ip/dhcp-client/get $c gateway])
  :put ("primary-dns=" . [/ip/dhcp-client/get $c primary-dns] . " primary-ntp=" . [/ip/dhcp-client/get $c primary-ntp])
  :if ($st != "bound") do={ :put "Todavia no esta bound: revisa cable y modem, y /log/print where topics~\"dhcp\"" }
  # 4. Doble NAT o CGNAT: lo dice la IP recibida
  :if ([:len $addr] > 0) do={
    :local ip [:toip [:pick $addr 0 [:find $addr "/"]]]
    :if (($ip in 10.0.0.0/8) || ($ip in 172.16.0.0/12) || ($ip in 192.168.0.0/16)) do={ :put "IP privada: hay otro NAT adelante (modem en modo router)." }
    :if ($ip in 100.64.0.0/10) do={ :put "IP en 100.64.0.0/10: CGNAT, sin acceso entrante (leccion 9)." }
  }
  /ip/route/print where dst-address=0.0.0.0/0
  :put ("Listo: cliente DHCP en " . $wan . " con distancia " . $dist . ". Verifica: /ip/cloud/print (public-address)")
}''',
    notas=[
        "Con dos WAN en distancia 1 el tráfico se reparte (ECMP): el respaldo va con distancia mayor.",
        "Si el servidor manda rutas por la opción 121 y te falta la ruta por defecto, probá a mano add-default-route=special-classless.",
        "El script de lease para failover con gateway dinámico (paso 5 del laboratorio) no está incluido: probalo aparte en laboratorio.",
    ],
)

# ---------------------------------------------------------------- 15
S["15"] = dict(
    titulo="PPPoE con Antel sobre el ONT en modo puente",
    descripcion="Hace el export de antes, apaga el cliente DHCP de la WAN, crea o corrige el cliente PPPoE (sobre la VLAN solo si la cargás), lo suma a la lista WAN y agrega el ajuste de MSS si el perfil PPP no lo hace. Muestra el estado negociado.",
    variables=[
        {"nombre": "WAN", "valor": "ether1", "detalle": "Puerto conectado al ONT de Antel en modo puente"},
        {"nombre": "PPPOE", "valor": "pppoe-antel", "detalle": "Nombre de la interfaz PPPoE"},
        {"nombre": "USUARIO", "valor": "cliente-ejemplo", "detalle": "Usuario PPPoE que entregó Antel para ese servicio"},
        {"nombre": "CLAVE", "valor": "Clave-De-Ejemplo-1", "detalle": "Contraseña PPPoE de Antel (la de ejemplo no sirve: cambiala). Sin comillas ni signo $"},
        {"nombre": "VLAN_ID", "valor": "", "detalle": "Opcional. Vacío = sin VLAN. Ninguna fuente confirma que Antel la pida: cargá el número solo si Antel te lo confirma"},
        {"nombre": "MTU", "valor": "1492", "detalle": "Opcional. MTU y MRU máximos; 1492 es el máximo de PPPoE sobre Ethernet según MikroTik, no un dato de Antel. Vacío = lo que negocie el equipo"},
    ],
    codigo=r'''# IES Training - MikroTik - Leccion 15: PPPoE con Antel
# Con el ONT ya en puente. El sitio queda sin internet hasta que el PPPoE marque: coordina la ventana.
{
  :local wan "{{WAN}}"
  :local nombre "{{PPPOE}}"
  # Opcionales: VLAN vacia salvo que Antel confirme un numero; MTU vacio = lo que negocie
  :local vlan "{{VLAN_ID}}"
  :local mtu "{{MTU}}"
  /export file=ies-antes-pppoe
  /ip/dhcp-client/disable [find interface=$wan]
  :if ([:len [/ip/address/find interface=$wan dynamic=no]] > 0) do={ :put "Ojo: la WAN tiene IP estatica. La documentacion desaconseja IP y PPPoE en la misma interfaz." }
  # 3. Con VLAN confirmada, el PPPoE va sobre la VLAN
  :local base $wan
  :if ([:len $vlan] > 0) do={
    :if ([:len [/interface/vlan/find name="vlan-wan"]] = 0) do={ /interface/vlan/add name=vlan-wan interface=$wan vlan-id=[:tonum $vlan] comment="ies-vlan-wan" } else={ /interface/vlan/set [find name="vlan-wan"] interface=$wan vlan-id=[:tonum $vlan] }
    :set base "vlan-wan"
  }
  # 2. Cliente PPPoE
  :local p [/interface/pppoe-client/find name=$nombre]
  :if ([:len $p] = 0) do={
    /interface/pppoe-client/add name=$nombre interface=$base user="{{USUARIO}}" password="{{CLAVE}}" add-default-route=yes use-peer-dns=yes comment="ies-pppoe-antel" disabled=no
  } else={
    /interface/pppoe-client/set $p interface=$base user="{{USUARIO}}" password="{{CLAVE}}" add-default-route=yes use-peer-dns=yes disabled=no
  }
  :if ([:len $mtu] > 0) do={ /interface/pppoe-client/set [find name=$nombre] max-mtu=[:tonum $mtu] max-mru=[:tonum $mtu] }
  # La WAN pasa a ser el PPPoE: masquerade y reglas por la lista WAN
  :if ([:len [/interface/list/find name=WAN]] = 0) do={ /interface/list/add name=WAN comment="ies-pppoe-antel" }
  :if ([:len [/interface/list/member/find list=WAN interface=$nombre]] = 0) do={ /interface/list/member/add list=WAN interface=$nombre comment="ies-pppoe-antel" }
  # 5. MSS: si el perfil PPP no lo ajusta, regla de mangle
  :local perfil [/interface/pppoe-client/get [find name=$nombre] profile]
  :local mss [:tostr [/ppp/profile/get [find name=$perfil] change-tcp-mss]]
  :if ($mss != "yes" && $mss != "true" && [:len [/ip/firewall/mangle/find comment="ies-MSS PPPoE"]] = 0) do={
    /ip/firewall/mangle/add chain=forward out-interface=$nombre protocol=tcp tcp-flags=syn action=change-mss new-mss=clamp-to-pmtu passthrough=yes comment="ies-MSS PPPoE"
  }
  # 4. Estado y MTU negociado
  :delay 10s
  /interface/pppoe-client/monitor [find name=$nombre] once
  :put ("Listo: PPPoE " . $nombre . " sobre " . $base . ", en la lista WAN y con MSS cubierto. Anota status, mtu, mru y local-address.")
  :put "Verifica: /ip/route/print where dst-address=0.0.0.0/0 ; /ping 1.1.1.1 count=3"
}''',
    notas=[
        "Antes de pegarlo, buscá el concentrador a mano: /interface/pppoe-client/scan interface=ether1. Si aparece un ac-name, va sin VLAN; si no aparece nada, pedile el dato de VLAN a Antel.",
        "Cambiá USUARIO y CLAVE por los del servicio y anotá en el legajo qué te dijo Antel (modo puente, VLAN) y quién.",
        "La contraseña va entre comillas en el script: si tiene comillas, barra invertida o signo $, cargala a mano en WinBox.",
        "Si al reconectar (disable y enable del PPPoE) cambia local-address, el acceso remoto va por DDNS o túnel (lecciones 18 a 20).",
    ],
)

# ---------------------------------------------------------------- 16
S["16"] = dict(
    titulo="Backup previo y reporte de paquetes y RouterBOOT",
    descripcion="Guarda un backup con contraseña y un export antes de tocar paquetes, y muestra arquitectura, versión, lo que ofrece el canal, los paquetes, los .npk subidos a Files y si falta actualizar RouterBOOT. No instala ni reinicia.",
    variables=[
        {"nombre": "NOMBRE_BACKUP", "valor": "pre-paquetes", "detalle": "Nombre del backup y del export en Files"},
        {"nombre": "CLAVE_BACKUP", "valor": "Backup-Lab-Ejemplo-1", "detalle": "Contraseña del backup (la de ejemplo no sirve: cambiala). Sin comillas ni signo $"},
    ],
    codigo=r'''# IES Training - MikroTik - Leccion 16: Paquetes al dia (backup y reporte)
# No instala ni reinicia: deja el backup hecho y te dice que falta. Lee el changelog antes de instalar.
{
  :local nombre "{{NOMBRE_BACKUP}}"
  # 1. Backup y export antes de tocar paquetes
  /system/backup/save name=$nombre password="{{CLAVE_BACKUP}}"
  /export file=$nombre
  # 2. Arquitectura, version y lo que ofrece el canal
  :local arch [/system/resource/get architecture-name]
  :put ("Equipo " . [/system/resource/get board-name] . " | arquitectura " . $arch . " | RouterOS " . [/system/resource/get version])
  /system/package/update/check-for-updates once
  :delay 5s
  :put ("Canal " . [/system/package/update/get channel] . " | instalada " . [/system/package/update/get installed-version] . " | ultima " . [/system/package/update/get latest-version])
  :put ("Estado: " . [/system/package/update/get status])
  /system/package/print
  # 4. .npk subidos a Files para actualizar sin internet: tienen que ser de esta arquitectura
  :foreach f in=[/file/find where name~"\\.npk\$"] do={ :put ("En Files: " . [/file/get $f name] . " (tiene que ser " . $arch . ")") }
  # 6. RouterBOOT: firmware actual contra el que trae esta version
  :do {
    :local cur [/system/routerboard/get current-firmware]
    :local upg [/system/routerboard/get upgrade-firmware]
    :put ("RouterBOOT actual " . $cur . " | disponible " . $upg)
    :if ($cur != $upg) do={ :put "Falta RouterBOOT: /system/routerboard/upgrade y despues /system/reboot" }
  } on-error={ :put "Sin menu RouterBOARD (CHR o x86): RouterBOOT no aplica." }
  # Para instalar, a mano y con el changelog leido: /system/package/update/install
  :put ("Listo: backup " . $nombre . ".backup y export " . $nombre . ".rsc en Files, y reporte de version.")
  :put ("Verifica: /file/print where name~\"" . $nombre . "\"")
}''',
    notas=[
        "Bajá el .backup y el .rsc a tu PC antes de actualizar: si el equipo no arranca, en el router no te sirven.",
        "En equipos WiFi, si actualizás a mano subí también el paquete de radio (wifi-qcom o wireless) de la misma versión.",
        "Instalar (Download&Install), habilitar paquetes extra, downgrade y RouterBOOT con reinicio quedan a mano, como en el laboratorio: este script solo prepara y reporta.",
    ],
)

# ---------------------------------------------------------------- 17
S["17"] = dict(
    titulo="Comparar canales y dejar el elegido",
    descripcion="Muestra la versión instalada, lo que ofrecen long-term y stable sin instalar nada, y deja configurado el canal elegido comparando su última versión con la instalada.",
    variables=[
        {"nombre": "CANAL", "valor": "long-term", "detalle": "Canal a dejar: long-term (clientes), stable (solo si probaste en el banco), testing o development (solo banco)"},
    ],
    codigo=r'''# IES Training - MikroTik - Leccion 17: Elegir el canal
# Solo consulta y cambia el canal: no instala nada. Necesita salida a internet por HTTPS.
{
  :local canal "{{CANAL}}"
  :if (!($canal = "long-term" || $canal = "stable" || $canal = "testing" || $canal = "development")) do={ :error "Canal invalido: long-term, stable, testing o development" }
  # 1. Canal y version actuales
  :local antes [/system/package/update/get channel]
  :local inst [/system/package/update/get installed-version]
  :put ("Canal actual: " . $antes . " | instalada: " . $inst)
  # 2. Que ofrece cada canal, sin instalar
  :foreach c in={"long-term";"stable"} do={
    /system/package/update/set channel=$c
    /system/package/update/check-for-updates once
    :delay 5s
    :put ("  " . $c . " ofrece: " . [/system/package/update/get latest-version])
  }
  # 3. Dejar el canal elegido
  /system/package/update/set channel=$canal
  /system/package/update/check-for-updates once
  :delay 5s
  :local ult [/system/package/update/get latest-version]
  :if ([:len $ult] = 0) do={ :put "El servidor no contesto: revisa salida a internet (TCP 443) y repeti." } else={
    :if ($ult = $inst) do={ :put ("Al dia en " . $canal . ": " . $inst) } else={ :put ("En " . $canal . " hay " . $ult . " (instalada " . $inst . "). Si es menor, el canal ofrece bajar. Backup antes (leccion 16).") }
  }
  :if ($canal != "long-term") do={ :put "Ojo: en sitios de clientes, long-term salvo que necesites algo de stable probado en el banco." }
  :put ("Listo: canal " . $canal . " (antes " . $antes . "). Anota canal, version y fecha en el legajo.")
  :put "Verifica: /system/package/update/print"
}''',
    notas=[
        "Si el cliente tiene varios equipos, pegalo en todos con el mismo canal.",
        "Para pasar de stable a long-term: con el canal ya cambiado, backup (lección 38) y después instalá a mano la versión que ofrezca.",
        "No uses el script de actualización automática de la documentación en clientes: instala lo que salga sin que lo pruebes.",
    ],
)

# ---------------------------------------------------------------- 18
S["18"] = dict(
    titulo="DDNS con verificación y hora por NTP",
    descripcion="Activa DDNS, pone la hora por NTP en vez de la hora aproximada de la nube, fuerza una actualización y comprueba que el nombre resuelva a public-address. Avisa si hay NAT adelante y si detect-internet está moviendo interfaces entre listas.",
    variables=[
        {"nombre": "NTP", "valor": "pool.ntp.org", "detalle": "Servidores NTP separados por coma, sin espacios"},
    ],
    codigo=r'''# IES Training - MikroTik - Leccion 18: Cloud a fondo (DDNS y hora por NTP)
# No anda en x86 y en CHR pide licencia paga. El nombre no abre nada: el firewall queda igual.
{
  # 1. DDNS
  /ip/cloud/set ddns-enabled=yes
  # 3. Hora por NTP en vez de la hora aproximada de la nube
  /system/ntp/client/set enabled=yes servers={{NTP}}
  /ip/cloud/set update-time=no
  # 2. Forzar la actualizacion y comprobar que el nombre resuelve a public-address
  /ip/cloud/force-update
  :delay 5s
  :local nombre [:tostr [/ip/cloud/get dns-name]]
  :local pub [:tostr [/ip/cloud/get public-address]]
  :put ("dns-name=" . $nombre . " public-address=" . $pub . " status=" . [/ip/cloud/get status])
  :local res "sin resolver"
  :do { :set res [:tostr [:resolve $nombre]] } on-error={}
  :if ($res = $pub) do={ :put "El nombre resuelve a public-address: OK" } else={ :put ("El nombre resuelve a " . $res . ": espera un minuto (TTL 60 s) y repeti") }
  # DDNS es un nombre, no un camino: si public-address no esta en el router, hay NAT adelante
  :if ([:len $pub] > 0 && [:len [/ip/address/find where address~("^" . $pub . "/")]] = 0) do={ :put "public-address no esta en ninguna interfaz: hay NAT adelante (doble NAT o CGNAT). Para entrar: lecciones 19 y 20." }
  # 4. Deteccion de internet moviendo interfaces entre listas
  :local det [:tostr [/interface/detect-internet/get detect-interface-list]]
  :if ($det != "none") do={ :put ("detect-internet activo (" . $det . "). Si tus reglas dependen de LAN y WAN, apagalo con /interface/detect-internet/set detect-interface-list=none") }
  /system/ntp/client/print
  :put ("Listo: DDNS activo (" . $nombre . "), NTP con {{NTP}} y update-time=no.")
  :put "Verifica: /ip/cloud/print ; /system/clock/print"
}''',
    notas=[
        "Con dos WAN, public-address es la del enlace por donde sale la ruta a la nube: cortá la principal y mirá cómo cambia.",
        "El script no apaga detect-internet: solo avisa. Apagalo vos si tus reglas dependen de las listas LAN y WAN.",
        "Publicar servicios detrás del nombre es la lección 32 (o la 24), con sus reglas.",
    ],
)

# ---------------------------------------------------------------- 19
S["19"] = dict(
    titulo="Back To Home con un usuario por dispositivo",
    descripcion="Verifica que la CPU sea compatible, activa Back To Home, espera vpn-status running y crea un usuario para el dispositivo de un técnico con acceso a la LAN acotado y vencimiento. Muestra el QR para importar en la app.",
    variables=[
        {"nombre": "USUARIO", "valor": "tecnico-lucia", "detalle": "Un usuario por dispositivo (nombre del técnico o del equipo)"},
        {"nombre": "DISPOSITIVO", "valor": "Celular Lucia", "detalle": "Comentario: qué dispositivo es (la app lo usa como nombre del túnel)"},
        {"nombre": "LAN", "valor": "192.168.88.0/24", "detalle": "Red local a la que puede entrar (client-allowed-address)"},
        {"nombre": "VENCE", "valor": "30d", "detalle": "Vencimiento: never, una fecha o un intervalo como 7d. No se puede cambiar después"},
    ],
    codigo=r'''# IES Training - MikroTik - Leccion 19: Back To Home
# Solo CPU ARM, ARM64 o TILE con RouterOS 7.12 o posterior. Nunca revoques para dar una baja.
{
  :local usuario "{{USUARIO}}"
  :local equipo "{{DISPOSITIVO}}"
  # 1. Arquitectura antes de prometerlo
  :local arch [/system/resource/get architecture-name]
  :if (!($arch = "arm" || $arch = "arm64" || $arch = "tile")) do={ :error ("Back To Home no corre en " . $arch . ": usa un concentrador (leccion 20)") }
  :put ("Arquitectura " . $arch . " | RouterOS " . [/system/resource/get version])
  # Activar y esperar vpn-status: running (hasta 30 s)
  /ip/cloud/set back-to-home-vpn=enabled
  :local i 0
  :while ((!([:tostr [/ip/cloud/get vpn-status]] ~ "running")) && ($i < 15)) do={ :delay 2s; :set i ($i + 1) }
  :if (!([:tostr [/ip/cloud/get vpn-status]] ~ "running")) do={ :error "Back To Home no llego a running: mira /ip/cloud/print" }
  # 2. Usuario del dispositivo, con LAN acotada y vencimiento
  :local u [/ip/cloud/back-to-home-user/find name=$usuario]
  :if ([:len $u] = 0) do={
    /ip/cloud/back-to-home-user/add name=$usuario allow-lan=yes client-allowed-address={{LAN}} expires={{VENCE}} comment=("ies-" . $equipo)
  } else={
    /ip/cloud/back-to-home-user/set $u allow-lan=yes client-allowed-address={{LAN}}
    :put ("El usuario " . $usuario . " ya existia: el vencimiento no se cambia (para otro, borralo y crealo de nuevo).")
  }
  # 5. La restriccion depende de la lista LAN
  :if ([:len [/interface/list/member/find list=LAN]] = 0) do={ :put "La lista LAN esta vacia: agrega tus redes locales antes de dar acceso." }
  :put ("vpn-dns-name: " . [:tostr [/ip/cloud/get vpn-dns-name]] . " | relay: " . [:tostr [/ip/cloud/get vpn-relay-ipv4-status]])
  # 3. QR y configuracion para la app WireGuard o Back To Home
  /ip/cloud/back-to-home-user/show-client-config [find name=$usuario]
  :put ("Listo: Back To Home activo y usuario " . $usuario . " con LAN {{LAN}}, vence {{VENCE}}.")
  :put ("Baja de esa persona: /ip/cloud/back-to-home-user/remove [find name=" . $usuario . "]")
}''',
    notas=[
        "Probá con el celular en datos móviles: WinBox a 192.168.88.1 o el NVR de ejemplo en 192.168.88.50.",
        "Para un usuario de solo internet (sin LAN), crealo a mano con allow-lan=no, como el invitado del laboratorio.",
        "back-to-home-vpn=revoked-and-disabled borra todos los usuarios y claves: para una baja, borrá el usuario.",
    ],
)

# ---------------------------------------------------------------- 20
S["20"] = dict(
    titulo="Endurecer el CHR y armar el hub WireGuard",
    descripcion="En el CHR: crea tu usuario full, deshabilita admin, cierra servicios y descubrimiento, arma la lista WAN, el firewall de input y el hub wg-hub con un peer por sitio. Lo que puede dejarte afuera (drop de WAN, available-from, MAC server) se aplica solo si estás entrando desde la oficina o por el túnel.",
    variables=[
        {"nombre": "USUARIO", "valor": "tecnico-lucia", "detalle": "Tu usuario full en el CHR"},
        {"nombre": "CLAVE", "valor": "Cambiar-Esta-Clave-Ejemplo-1", "detalle": "Contraseña de tu usuario (la de ejemplo no sirve: cambiala). Sin comillas ni signo $"},
        {"nombre": "WAN", "valor": "ether1", "detalle": "Interfaz pública del CHR"},
        {"nombre": "OFICINA", "valor": "203.0.113.50/32", "detalle": "IP fija de la oficina con máscara (una sola red)"},
        {"nombre": "TUNEL_RED", "valor": "10.10.10.0/24", "detalle": "Rango del túnel"},
        {"nombre": "HUB_IP", "valor": "10.10.10.1/24", "detalle": "IP del hub dentro del túnel"},
        {"nombre": "PUERTO", "valor": "13231", "detalle": "Puerto UDP de WireGuard"},
        {"nombre": "PEER_NOMBRE", "valor": "sitio-lab", "detalle": "Nombre del sitio (peer)"},
        {"nombre": "PEER_CLAVE", "valor": "CLAVE-PUBLICA-DEL-SITIO", "detalle": "Clave pública WireGuard del router del sitio (44 caracteres). Con el valor de ejemplo el peer no se crea"},
        {"nombre": "PEER_IP", "valor": "10.10.10.2/32", "detalle": "IP del sitio en el túnel (allowed-address)"},
    ],
    codigo=r'''# IES Training - MikroTik - Leccion 20: Concentrador CHR (hub WireGuard)
# Va en el CHR. Primera vez como admin: crea tu usuario y frena. Entra con el y pegalo de nuevo.
{
  :local usuario "{{USUARIO}}"
  :local oficina {{OFICINA}}
  :local tunel {{TUNEL_RED}}
  :local clave "{{PEER_CLAVE}}"
  # 1. Usuario propio; admin se deshabilita solo cuando no hay una sesion de admin abierta
  :if ([:len [/user/find name=$usuario]] = 0) do={ /user/add name=$usuario group=full password="{{CLAVE}}" comment="ies-hub" }
  :if ([:len [/user/active/find name="admin"]] > 0) do={ :error ("Sesion de admin abierta: entra como " . $usuario . " y volve a pegar el script") }
  /user/disable [find name="admin"]
  /ip/service/disable telnet,ftp,www,api,api-ssl
  /ip/neighbor/discovery-settings/set discover-interface-list=none
  /ip/dns/set allow-remote-requests=no
  # Desde donde entras: lo que puede cortarte se aplica solo si es la oficina o el tunel
  :local desde false
  :foreach s in=[/user/active/find name=$usuario] do={
    :local a [:toip [:tostr [/user/active/get $s address]]]
    :if (([:typeof $a] = "ip") && (($a in $oficina) || ($a in $tunel))) do={ :set desde true }
  }
  # 4. Hub WireGuard (antes del firewall: la regla del tunel usa wg-hub)
  :if ([:len [/interface/wireguard/find name=wg-hub]] = 0) do={ /interface/wireguard/add name=wg-hub listen-port={{PUERTO}} comment="ies-hub" }
  :if ([:len [/ip/address/find interface=wg-hub]] = 0) do={ /ip/address/add address={{HUB_IP}} interface=wg-hub comment="ies-hub" }
  :if ([:len $clave] = 44) do={
    :if ([:len [/interface/wireguard/peers/find interface=wg-hub name="{{PEER_NOMBRE}}"]] = 0) do={ /interface/wireguard/peers/add interface=wg-hub name="{{PEER_NOMBRE}}" public-key=$clave allowed-address={{PEER_IP}} comment="ies-hub" }
  } else={ :put "Sin clave publica real del sitio: el peer no se crea. Cargala en PEER_CLAVE y volve a pegar." }
  # 2. Lista WAN y firewall de input, en orden y una sola vez cada regla
  :if ([:len [/interface/list/find name=WAN]] = 0) do={ /interface/list/add name=WAN comment="ies-hub" }
  :if ([:len [/interface/list/member/find list=WAN interface={{WAN}}]] = 0) do={ /interface/list/member/add list=WAN interface={{WAN}} comment="ies-hub" }
  :if ([:len [/ip/firewall/filter/find comment="ies-established"]] = 0) do={ /ip/firewall/filter/add chain=input connection-state=established,related action=accept comment="ies-established" }
  :if ([:len [/ip/firewall/filter/find comment="ies-wireguard hub"]] = 0) do={ /ip/firewall/filter/add chain=input protocol=udp dst-port={{PUERTO}} action=accept comment="ies-wireguard hub" }
  :if ([:len [/ip/firewall/filter/find comment="ies-gestion oficina"]] = 0) do={ /ip/firewall/filter/add chain=input src-address=$oficina protocol=tcp dst-port=22,8291 action=accept comment="ies-gestion oficina" }
  :if ([:len [/ip/firewall/filter/find comment="ies-icmp"]] = 0) do={ /ip/firewall/filter/add chain=input protocol=icmp action=accept comment="ies-icmp" }
  :if ([:len [/ip/firewall/filter/find comment="ies-winbox por tunel"]] = 0) do={ /ip/firewall/filter/add chain=input in-interface=wg-hub protocol=tcp dst-port=8291 action=accept comment="ies-winbox por tunel" }
  :if ($desde) do={
    :if ([:len [/ip/firewall/filter/find comment="ies-drop resto WAN"]] = 0) do={ /ip/firewall/filter/add chain=input in-interface-list=WAN action=drop comment="ies-drop resto WAN" }
    /ip/service/set winbox,ssh available-from={{OFICINA}},{{TUNEL_RED}}
    /tool/mac-server/set allowed-interface-list=none
    /tool/mac-server/mac-winbox/set allowed-interface-list=none
  } else={ :put "No entras desde la oficina ni por el tunel: el drop de WAN, available-from y el MAC server quedan sin tocar. Pegalo desde ahi." }
  # 3. Licencia (prueba de 60 dias: /system/license/renew con tu cuenta)
  /system/license/print
  :put ("Clave publica del hub, para el sitio: " . [/interface/wireguard/get wg-hub public-key])
  :put "Listo: CHR endurecido y wg-hub escuchando. Verifica: /ip/firewall/filter/print ; /interface/wireguard/peers/print"
}''',
    notas=[
        "Mirá antes si el CHR ya trae reglas (/ip/firewall/filter/print): el script agrega las suyas al final, y si hay un drop previo quedan debajo.",
        "Del lado del sitio (paso 5 del laboratorio) va wg-central con la clave pública del hub que imprime este script, endpoint a la IP pública del CHR y persistent-keepalive=25s.",
        "Con la licencia Free el hub sube a 1 Mbps por interfaz: alcanza para WinBox y monitoreo, no para video.",
        "available-from es el nombre de la propiedad en la documentación 7.25; en versiones 7 anteriores la misma opción se llama address.",
    ],
)

# ---------------------------------------------------------------- 21
S["21"] = dict(
    titulo="Servidor L2TP con IPsec obligatorio y un usuario",
    descripcion="Crea o corrige pool, perfil PPP y servidor L2TP con use-ipsec=required, un usuario por persona, los puertos UDP 500, 4500, 1701 y ESP arriba del drop de fábrica, y la regla que saca el tráfico IPsec de FastTrack si no está.",
    variables=[
        {"nombre": "POOL", "valor": "192.168.89.10-192.168.89.50", "detalle": "Rango de IPs para los clientes VPN"},
        {"nombre": "IP_LOCAL", "valor": "192.168.89.1", "detalle": "IP del router del lado del túnel (local-address)"},
        {"nombre": "DNS", "valor": "192.168.88.1", "detalle": "DNS que reciben los clientes"},
        {"nombre": "SECRETO_IPSEC", "valor": "Secreto-IPsec-Largo-De-Ejemplo-2026", "detalle": "Clave IPsec compartida (la de ejemplo no sirve: cambiala). Sin comillas ni signo $"},
        {"nombre": "USUARIO", "valor": "encargado", "detalle": "Usuario de la persona que se conecta"},
        {"nombre": "CLAVE", "valor": "Clave-Usuario-Ejemplo-1", "detalle": "Contraseña de ese usuario (la de ejemplo no sirve: cambiala). Sin comillas ni signo $"},
    ],
    codigo=r'''# IES Training - MikroTik - Leccion 21: Servidor L2TP con IPsec obligatorio
# Probalo primero en un equipo de banco. Pensado para la configuracion por defecto.
{
  :local drop [/ip/firewall/filter/find comment="defconf: drop all not coming from LAN"]
  :if ([:len $drop] = 0) do={ :error "No esta el drop de fabrica en input: ubica las reglas a mano (leccion 4). No se cambio nada." }
  # 1. Pool, perfil y servidor
  :if ([:len [/ip/pool/find name=pool-l2tp]] = 0) do={ /ip/pool/add name=pool-l2tp ranges={{POOL}} comment="ies-l2tp" } else={ /ip/pool/set [find name=pool-l2tp] ranges={{POOL}} }
  :if ([:len [/ppp/profile/find name=perfil-l2tp]] = 0) do={
    /ppp/profile/add name=perfil-l2tp local-address={{IP_LOCAL}} remote-address=pool-l2tp dns-server={{DNS}} comment="ies-l2tp"
  } else={ /ppp/profile/set [find name=perfil-l2tp] local-address={{IP_LOCAL}} remote-address=pool-l2tp dns-server={{DNS}} }
  /interface/l2tp-server/server/set enabled=yes use-ipsec=required ipsec-secret="{{SECRETO_IPSEC}}" default-profile=perfil-l2tp
  # 2. Un usuario por persona
  :if ([:len [/ppp/secret/find name="{{USUARIO}}"]] = 0) do={
    /ppp/secret/add name="{{USUARIO}}" password="{{CLAVE}}" service=l2tp profile=perfil-l2tp comment="ies-l2tp"
  } else={ /ppp/secret/set [find name="{{USUARIO}}"] password="{{CLAVE}}" service=l2tp profile=perfil-l2tp }
  # 3. Input, arriba del drop de fabrica
  :if ([:len [/ip/firewall/filter/find comment="ies-L2TP IPsec"]] = 0) do={ /ip/firewall/filter/add chain=input protocol=udp dst-port=500,4500,1701 action=accept comment="ies-L2TP IPsec" place-before=[:pick $drop 0] }
  :if ([:len [/ip/firewall/filter/find comment="ies-ESP"]] = 0) do={ /ip/firewall/filter/add chain=input protocol=ipsec-esp action=accept comment="ies-ESP" place-before=[:pick $drop 0] }
  # 4. Trafico del tunel fuera de FastTrack, si no hay ya un accept in,ipsec activo
  :local ft [/ip/firewall/filter/find action=fasttrack-connection]
  :local hay [:len [/ip/firewall/filter/find chain=forward action=accept ipsec-policy="in,ipsec" disabled=no]]
  :if ($hay = 0 && [:len [/ip/firewall/filter/find comment="ies-IPsec fuera de FastTrack"]] = 0) do={
    :if ([:len $ft] > 0) do={ /ip/firewall/filter/add chain=forward ipsec-policy=in,ipsec action=accept comment="ies-IPsec fuera de FastTrack" place-before=[:pick $ft 0] } else={ /ip/firewall/filter/add chain=forward ipsec-policy=in,ipsec action=accept comment="ies-IPsec fuera de FastTrack" }
  }
  /ip/firewall/filter/print where comment~"^ies-"
  :put "Listo: L2TP con IPsec obligatorio, perfil perfil-l2tp, usuario {{USUARIO}} y UDP 500, 4500, 1701 y ESP en input."
  :put "Verifica: /ip/ipsec/active-peers/print ; /ppp/active/print ; /log/print where topics~\"ipsec|l2tp\""
}''',
    notas=[
        "En Windows: VPN L2TP/IPsec con clave precompartida. Si la notebook está detrás de NAT y no conecta, la clave AssumeUDPEncapsulationContextOnSendRule en 2 y reinicio (paso 5 del laboratorio).",
        "Para otra persona, volvé a pegarlo cambiando USUARIO y CLAVE: pool, perfil y reglas no se duplican.",
        "Nunca use-ipsec=no en un servidor expuesto, y PPTP nunca.",
    ],
)

# ---------------------------------------------------------------- 22
S["22"] = dict(
    titulo="Túnel IPsec sitio a sitio: las cinco piezas y los dos bypass",
    descripcion="En el sitio A (MikroTik) crea profile, peer IKEv2, identity con clave, proposal y policy con los valores de la tabla de la lección, abre UDP 500/4500 y ESP solo desde el otro extremo, agrega el bypass de NAT y de FastTrack, el log de IPsec, y muestra fase 1 y fase 2.",
    variables=[
        {"nombre": "NOMBRE", "valor": "sucursal", "detalle": "Nombre del túnel (peer); arma perfil-<nombre> y prop-<nombre>"},
        {"nombre": "PEER_IP", "valor": "198.51.100.20", "detalle": "IP pública del otro extremo"},
        {"nombre": "RED_LOCAL", "valor": "192.168.88.0/24", "detalle": "LAN de este sitio"},
        {"nombre": "RED_REMOTA", "valor": "10.10.10.0/24", "detalle": "LAN del otro sitio (no puede ser igual a la local)"},
        {"nombre": "PSK", "valor": "Clave-Larga-De-Ejemplo-Para-El-Tunel-2026", "detalle": "Clave precompartida acordada (la de ejemplo no sirve: cambiala). Sin comillas ni signo $"},
    ],
    codigo=r'''# IES Training - MikroTik - Leccion 22: IPsec sitio a sitio (IKEv2, clave precompartida)
# Primero la tabla firmada por las dos puntas. Fase 1: AES-256, SHA-256, DH 14, 1d. Fase 2: AES-256-CBC, SHA-256, PFS 14, 1h.
{
  :local n "{{NOMBRE}}"
  :local remoto {{PEER_IP}}
  :local redL {{RED_LOCAL}}
  :local redR {{RED_REMOTA}}
  :if ($redL = $redR) do={ :error "Las dos LAN tienen el mismo rango: renumera una antes del tunel" }
  :local drop [/ip/firewall/filter/find comment="defconf: drop all not coming from LAN"]
  :if ([:len $drop] = 0) do={ :error "No esta el drop de fabrica en input: ubica las reglas a mano (leccion 4). No se cambio nada." }
  # 2. Las cinco piezas (profile no tiene comment: se busca por nombre)
  :if ([:len [/ip/ipsec/profile/find name=("perfil-" . $n)]] = 0) do={ /ip/ipsec/profile/add name=("perfil-" . $n) hash-algorithm=sha256 enc-algorithm=aes-256 dh-group=modp2048 lifetime=1d }
  :if ([:len [/ip/ipsec/peer/find name=$n]] = 0) do={ /ip/ipsec/peer/add name=$n address=$remoto profile=("perfil-" . $n) exchange-mode=ike2 comment=("ies-ipsec " . $n) }
  :if ([:len [/ip/ipsec/identity/find peer=$n]] = 0) do={ /ip/ipsec/identity/add peer=$n auth-method=pre-shared-key secret="{{PSK}}" comment=("ies-ipsec " . $n) } else={ /ip/ipsec/identity/set [find peer=$n] secret="{{PSK}}" }
  :if ([:len [/ip/ipsec/proposal/find name=("prop-" . $n)]] = 0) do={ /ip/ipsec/proposal/add name=("prop-" . $n) auth-algorithms=sha256 enc-algorithms=aes-256-cbc pfs-group=modp2048 lifetime=1h comment=("ies-ipsec " . $n) }
  :if ([:len [/ip/ipsec/policy/find peer=$n]] = 0) do={ /ip/ipsec/policy/add peer=$n tunnel=yes src-address=$redL dst-address=$redR proposal=("prop-" . $n) action=encrypt comment=("ies-ipsec " . $n) }
  # 3. Puertos solo desde el otro extremo, arriba del drop
  :if ([:len [/ip/firewall/filter/find comment=("ies-IKE " . $n)]] = 0) do={ /ip/firewall/filter/add chain=input src-address=$remoto protocol=udp dst-port=500,4500 action=accept comment=("ies-IKE " . $n) place-before=[:pick $drop 0] }
  :if ([:len [/ip/firewall/filter/find comment=("ies-ESP " . $n)]] = 0) do={ /ip/firewall/filter/add chain=input src-address=$remoto protocol=ipsec-esp action=accept comment=("ies-ESP " . $n) place-before=[:pick $drop 0] }
  # 4. Bypass de NAT (arriba de todo el NAT) y de FastTrack (arriba del fasttrack)
  :local nat [/ip/firewall/nat/find]
  :if ([:len [/ip/firewall/nat/find comment=("ies-no NAT al tunel " . $n)]] = 0) do={
    :if ([:len $nat] > 0) do={ /ip/firewall/nat/add chain=srcnat src-address=$redL dst-address=$redR action=accept comment=("ies-no NAT al tunel " . $n) place-before=[:pick $nat 0] } else={ /ip/firewall/nat/add chain=srcnat src-address=$redL dst-address=$redR action=accept comment=("ies-no NAT al tunel " . $n) }
  }
  :local ft [/ip/firewall/filter/find action=fasttrack-connection]
  :if ([:len $ft] > 0 && [:len [/ip/firewall/filter/find comment=("ies-tunel fuera de FastTrack " . $n)]] = 0) do={
    /ip/firewall/filter/add chain=forward src-address=$redL dst-address=$redR action=accept comment=("ies-tunel fuera de FastTrack " . $n) place-before=[:pick $ft 0]
    /ip/firewall/filter/add chain=forward src-address=$redR dst-address=$redL action=accept comment=("ies-tunel fuera de FastTrack " . $n) place-before=[:pick $ft 0]
  }
  # 5. Log de IPsec (sin debug), una sola vez
  :local hayLog false
  :foreach l in=[/system/logging/find] do={ :if ([:tostr [/system/logging/get $l topics]] ~ "ipsec") do={ :set hayLog true } }
  :if (!$hayLog) do={ /system/logging/add topics=ipsec,!debug }
  :delay 5s
  /ip/ipsec/active-peers/print
  :put ("ph2-state: " . [/ip/ipsec/policy/get [find peer=$n] ph2-state] . " (established = fase 2 arriba)")
  :put ("Listo: tunel " . $n . " " . $redL . " <-> " . $redR . " con bypass de NAT y FastTrack.")
  :put "Verifica: /ip/ipsec/installed-sa/print ; /log/print where topics~\"ipsec\""
}''',
    notas=[
        "Del otro lado (otro MikroTik, pfSense u otra marca) van los mismos valores de la tabla, con las redes al revés.",
        "Si probaste antes del bypass, limpiá las conexiones viejas: /ip/firewall/connection/remove [find where dst-address~\"^10.10.10.\"] (cambiá por tu red remota).",
        "Síntomas: no suitable proposal = parámetros distintos; phase1 time up = UDP 500/4500 o IP del peer; fases arriba sin tráfico = bypass de NAT; lento y se arregla con Torch = FastTrack.",
    ],
)

# ---------------------------------------------------------------- 23
S["23"] = dict(
    titulo="Red de seguridad: export, backup y rescate programado",
    descripcion="Para los cambios que Safe Mode no cubre (por ejemplo mover la VPN por la que entrás): guarda un export legible y un backup, y programa un rescate que restaura ese backup, y reinicia el equipo, si no lo borrás antes de que se cumpla el tiempo. Si ya está armado, solo muestra cuándo corre.",
    variables=[
        {"nombre": "NOMBRE", "valor": "ies-rescate", "detalle": "Nombre del backup y de la tarea programada"},
        {"nombre": "MINUTOS", "valor": "5", "detalle": "Minutos hasta el rescate (subilo si el cambio lleva más)"},
        {"nombre": "CLAVE_BACKUP", "valor": "Backup-Rescate-Ejemplo-1", "detalle": "Contraseña del backup (la de ejemplo no sirve: cambiala). Sin comillas ni signo $"},
    ],
    codigo=r'''# IES Training - MikroTik - Leccion 23: Rescate para cambios que Safe Mode no cubre
# OJO: si no borras la tarea a tiempo, el router carga el backup y REINICIA. Solo en banco o con ventana acordada.
{
  :local nombre "{{NOMBRE}}"
  :local espera [:totime "{{MINUTOS}}m"]
  :local s [/system/scheduler/find name=$nombre]
  # Una tarea que ya corrio (run-count mayor a 0) y sigue en la lista se rearma
  :if ([:len $s] > 0) do={ :if ([/system/scheduler/get $s run-count] > 0) do={ /system/scheduler/remove $s; :set s [/system/scheduler/find name=$nombre] } }
  :if ([:len $s] > 0) do={
    :put ("El rescate ya esta armado y corre en " . [/system/scheduler/get $s next-run] . ". No se toca el backup.")
  } else={
    # Hora del rescate: ahora mas N minutos, el mismo dia
    :local hora ([/system/clock/get time] + $espera)
    :if ($hora >= 1d) do={ :error "El rescate caeria despues de medianoche: espera o baja MINUTOS. No se cambio nada." }
    # 1. Foto de antes: export legible y backup completo para restaurar
    /export file=($nombre . "-antes")
    /system/backup/save name=$nombre password="{{CLAVE_BACKUP}}"
    :delay 2s
    # 2. Rescate de una sola vez: carga el backup, que no tiene esta tarea adentro
    /system/scheduler/add name=$nombre start-time=$hora interval=0s comment="ies-rescate" on-event=("/system/backup/load name=" . $nombre . ".backup password=\"{{CLAVE_BACKUP}}\"")
    :put ("Rescate armado: corre en " . [/system/scheduler/get [find name=$nombre] next-run])
  }
  # Estado: las acciones con F se deshacen si se corta una sesion en Safe Mode
  /system/history/print
  :put ("Listo: export " . $nombre . "-antes.rsc, backup " . $nombre . ".backup y rescate a {{MINUTOS}} min.")
  :put "Ahora: Ctrl+X (Safe Mode), un cambio, verificas y confirmas con Ctrl+X."
  :put ("Si salio bien, desarmalo ya: /system/scheduler/remove [find name=" . $nombre . "]")
}''',
    notas=[
        "Este script no reemplaza a Safe Mode: Safe Mode se toma con Ctrl+X en la terminal o con el botón de WinBox, y no se puede activar desde un script.",
        "Mirá next-run después de pegarlo: tiene que dar la hora actual más los minutos elegidos. Si no, borrá la tarea con el comando del final.",
        "El backup se toma antes de crear la tarea, así que al restaurarlo la tarea no vuelve y no queda un ciclo de reinicios.",
        "Un corte de energía no es una forma de deshacer: no lo uses para probar.",
    ],
)

# ---------------------------------------------------------------- 24
S["24"] = dict(
    titulo="Publicar un NVR solo para orígenes conocidos",
    descripcion="Hace el export de antes, avisa si la WAN está detrás de doble NAT o CGNAT, carga la lista de orígenes permitidos y las reglas dst-nat atadas a la WAN y a esa lista (SDK y, si lo pedís, RTSP) con puerto externo distinto del interno. Limpia conexiones viejas y muestra los contadores.",
    variables=[
        {"nombre": "WAN", "valor": "ether1", "detalle": "Interfaz WAN (la que tiene la IP pública; con PPPoE, la interfaz PPPoE)"},
        {"nombre": "NVR_NOMBRE", "valor": "NVR1", "detalle": "Nombre corto del NVR para los comentarios"},
        {"nombre": "NVR_IP", "valor": "192.168.88.50", "detalle": "IP del NVR en la LAN"},
        {"nombre": "LISTA", "valor": "nvr-permitidos", "detalle": "Nombre de la address-list de orígenes"},
        {"nombre": "ORIGENES", "valor": "198.51.100.20,203.0.113.25", "detalle": "IPs o nombres DDNS permitidos, separados por coma (oficina, central de monitoreo)"},
        {"nombre": "REVISAR", "valor": "2027-04", "detalle": "Cuándo revisar si esos orígenes siguen valiendo"},
        {"nombre": "PUERTO_EXT", "valor": "18000", "detalle": "Puerto externo para el SDK (iVMS-4200 y la app)"},
        {"nombre": "PUERTO_INT", "valor": "8000", "detalle": "Puerto interno del NVR: Hikvision 8000, Dahua 37777"},
        {"nombre": "PUERTO_EXT_RTSP", "valor": "18554", "detalle": "Opcional. Puerto externo para RTSP; vacío = no publicar RTSP"},
        {"nombre": "PUERTO_INT_RTSP", "valor": "554", "detalle": "Puerto RTSP del NVR (554, o 10554 en firmware nuevo)"},
    ],
    codigo=r'''# IES Training - MikroTik - Leccion 24: Port forwarding de un NVR, solo para origenes conocidos
# Probalo primero en un equipo de banco y en Safe Mode (Ctrl+X). Primera opcion para entrar: VPN.
{
  :local wan "{{WAN}}"
  :local nvr "{{NVR_NOMBRE}}"
  :local ip [:toip "{{NVR_IP}}"]
  :local lista "{{LISTA}}"
  :local extR "{{PUERTO_EXT_RTSP}}"
  :local intR "{{PUERTO_INT_RTSP}}"
  /export file=ies-antes-port-forwarding
  # 1. La IP del WAN dice si se puede: doble NAT o CGNAT
  :foreach a in=[/ip/address/find interface=$wan] do={
    :local d [:tostr [/ip/address/get $a address]]
    :local w [:toip [:pick $d 0 [:find $d "/"]]]
    :if ($w in 100.64.0.0/10) do={ :put "WAN en 100.64.0.0/10: CGNAT, no hay port forwarding posible (lecciones 19 y 20)." }
    :if (($w in 10.0.0.0/8) || ($w in 172.16.0.0/12) || ($w in 192.168.0.0/16)) do={ :put "WAN privada: doble NAT. ONT en bridge (leccion 15) o reenvio tambien en el modem." }
  }
  # 2. Origenes permitidos (se agregan una sola vez)
  :foreach o in=[:toarray "{{ORIGENES}}"] do={
    :if ([:len [/ip/firewall/address-list/find list=$lista address=$o]] = 0) do={ /ip/firewall/address-list/add list=$lista address=$o comment="ies-origen NVR, revisar {{REVISAR}}" }
  }
  # 3. dst-nat atado a la WAN y a la lista; si ya estaba, se reemplaza
  /ip/firewall/nat/remove [find chain=dstnat comment~("^ies-" . $nvr . " SDK ")]
  /ip/firewall/nat/add chain=dstnat in-interface-list=WAN src-address-list=$lista protocol=tcp dst-port={{PUERTO_EXT}} action=dst-nat to-addresses=$ip to-ports={{PUERTO_INT}} comment=("ies-" . $nvr . " SDK {{PUERTO_EXT}}>{{PUERTO_INT}}")
  :if ([:len $extR] > 0) do={
    /ip/firewall/nat/remove [find chain=dstnat comment~("^ies-" . $nvr . " RTSP ")]
    /ip/firewall/nat/add chain=dstnat in-interface-list=WAN src-address-list=$lista protocol=tcp dst-port=$extR action=dst-nat to-addresses=$ip to-ports=$intR comment=("ies-" . $nvr . " RTSP " . $extR . ">" . $intR)
  }
  # 4. Forward: la regla de fabrica ya deja pasar lo dst-nateado
  :if ([:len [/ip/firewall/filter/find comment~"not DSTNATed"]] = 0) do={ :put "No esta la regla de fabrica not DSTNATed: agrega el accept de publicados arriba de tu drop de forward (leccion 4)." }
  # 5. Conexiones viejas afuera
  /ip/firewall/connection/remove [find dst-address~":{{PUERTO_EXT}}"]
  :if ([:len $extR] > 0) do={ /ip/firewall/connection/remove [find dst-address~(":" . $extR)] }
  # 6. Contadores: si no suben al probar, el paquete no llega o el origen no esta en la lista
  /ip/firewall/nat/print stats where comment~("^ies-" . $nvr)
  :put ("Listo: " . $nvr . " publicado en {{PUERTO_EXT}} hacia " . $ip . ":{{PUERTO_INT}} solo para la lista " . $lista . ".")
  :put "Verifica desde la oficina: Test-NetConnection <IP publica> -Port {{PUERTO_EXT}} y mira que suba el contador."
}''',
    notas=[
        "Un segundo NVR detrás de la misma IP pública: volvé a pegarlo con otro NVR_NOMBRE, otra NVR_IP y otro PUERTO_EXT.",
        "Hairpin (paso 7 del laboratorio) no está incluido: agregalo a mano solo si en la oficina entran por la IP pública.",
        "No publiques el 80 ni el 443 del NVR: para la web, VPN (lecciones 8 y 19).",
        "Desde el celular con datos móviles (fuera de la lista) no tiene que conectar: es lo esperado.",
    ],
)


def main():
    out = {k: {"script_rsc": v} for k, v in S.items()}
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"escrito {OUT} ({len(out)} lecciones)")


if __name__ == "__main__":
    main()
