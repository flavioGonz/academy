"""Scripts de RouterOS (campo script_rsc) para las lecciones 1-3 y 5-10. Lo importa manifest_1_11.py."""

NOTA_ASCII = "Va sin tildes a propósito: la terminal de RouterOS no siempre muestra bien los acentos."
HEAD = "# Probalo primero en un equipo de banco y en Safe Mode (Ctrl+X).\n"

S = {}

# ------------------------------------------------------------------ 1
S["1"] = {
    "titulo": "Revisar lo que trae de fábrica y guardar la foto inicial",
    "descripcion": "No cambia la configuración: muestra las listas WAN y LAN, las IP y si está el drop de fábrica, y guarda un export inicial solo si todavía no existe.",
    "variables": [
        {"nombre": "ARCHIVO", "valor": "inicial", "detalle": "Nombre del export (sin .rsc)"},
    ],
    "codigo": "# IES Training · MikroTik · L1 · Foto de fabrica\n" + HEAD + """# Solo lee y guarda un export: no toca la configuracion.
{
:local archivo "{{ARCHIVO}}"
:put "== Listas de interfaces (WAN y LAN) =="
/interface/list/member/print
:put "== Direcciones IP =="
/ip/address/print
:put ("Reglas de firewall filter: " . [:len [/ip/firewall/filter/find]])
:if ([:len [/ip/firewall/filter/find comment="defconf: drop all not coming from LAN"]] > 0) do={
  :put "OK: esta el drop de fabrica que protege al router (input)."
} else={
  :put "Ojo: no esta el drop de fabrica. Equipo sin defconf (CCR) o firewall reescrito."
}
:if ([:len [/interface/list/find name=LAN]] = 0) do={
  :put "Ojo: no existe la lista LAN. Antes de seguir, crearla con el bridge adentro."
}
# El export inicial es la foto del primer dia: si ya existe, no se pisa
:if ([:len [/file/find where name~$archivo]] = 0) do={
  /export file=$archivo
  :put ("Export guardado: " . $archivo . ".rsc")
} else={
  :put ("Ya habia un " . $archivo . ".rsc: no lo piso.")
}
:put ("Listo: revisado lo de fabrica y foto en " . $archivo . ".rsc. Verifica con /file/print")
}""",
    "notas": ["Bajá el .rsc a la notebook (WinBox, Files, arrastrar) y guardalo en el legajo del cliente.",
              "No activa Safe Mode por vos: eso se hace con Ctrl+X antes de cualquier cambio.",
              NOTA_ASCII],
}

# ------------------------------------------------------------------ 2
S["2"] = {
    "titulo": "Crear tu usuario, el grupo de monitoreo y la cuenta de mesa de ayuda",
    "descripcion": "Crea tu usuario con grupo full, un grupo monitoreo sin reboot ni write y un usuario de mesa de ayuda limitado a la red de gestión. Deshabilitar admin queda comentado para hacerlo a mano después de probar.",
    "variables": [
        {"nombre": "USUARIO", "valor": "lucia.tecnico", "detalle": "Tu usuario personal (grupo full)"},
        {"nombre": "CLAVE", "valor": "Cambiar-Esta-Clave-2026", "detalle": "Clave de tu usuario: 12 caracteres o más, sin el signo $"},
        {"nombre": "USUARIO_MESA", "valor": "mesa.ayuda", "detalle": "Usuario de solo lectura"},
        {"nombre": "CLAVE_MESA", "valor": "Cambiar-Esta-Otra-2026", "detalle": "Clave del usuario de mesa de ayuda, sin el signo $"},
        {"nombre": "RED_GESTION", "valor": "192.168.88.0/24", "detalle": "Desde dónde puede entrar la mesa de ayuda"},
    ],
    "codigo": "# IES Training · MikroTik · L2 · Usuarios propios\n" + HEAD + """{
:local usuario "{{USUARIO}}"
:local clave "{{CLAVE}}"
:local mesa "{{USUARIO_MESA}}"
:local claveMesa "{{CLAVE_MESA}}"
:local red "{{RED_GESTION}}"
# Tu usuario con grupo full (si ya existe, no se toca su clave)
:if ([:len [/user/find name=$usuario]] = 0) do={
  /user/add name=$usuario group=full password=$clave comment="ies-usuario-tecnico"
  :put ("Creado " . $usuario)
} else={ :put ("Ya existia " . $usuario . ": no cambio su clave") }
# Grupo para mirar sin tocar: sin reboot ni write
:if ([:len [/user/group/find name=monitoreo]] = 0) do={
  /user/group/add name=monitoreo policy=local,ssh,winbox,read,test
} else={ /user/group/set [find name=monitoreo] policy=local,ssh,winbox,read,test }
# Mesa de ayuda: grupo monitoreo y solo desde la red de gestion
:if ([:len [/user/find name=$mesa]] = 0) do={
  /user/add name=$mesa group=monitoreo password=$claveMesa address=$red comment="ies-usuario-mesa"
  :put ("Creado " . $mesa)
} else={ /user/set [find name=$mesa] group=monitoreo address=$red }
# Deshabilitar admin: SOLO despues de entrar con tu usuario en otra sesion.
# Si tu usuario no anda y admin queda deshabilitado, la salida es reset o Netinstall.
# /user/disable [find name=admin]
:put ("Listo: " . $usuario . " (full) y " . $mesa . " (monitoreo). Proba entrar con " . $usuario . " y despues deshabilita admin a mano.")
/user/print
}""",
    "notas": ["Cambiá las dos claves de ejemplo antes de pegar. Si tu clave lleva el signo $, escribilo como \\$.",
              "No deshabilita admin: esa línea queda comentada a propósito. Hacelo vos, después de probar tu usuario en otra sesión.",
              "Si el usuario ya existía, el script no le cambia la clave.",
              NOTA_ASCII],
}

# ------------------------------------------------------------------ 3
S["3"] = {
    "titulo": "Apagar servicios, limitar la gestión a la LAN y auditar",
    "descripcion": "Apaga telnet, ftp, www y api, limita WinBox y SSH a la red de gestión, deja MAC server y descubrimiento solo hacia la LAN, apaga bandwidth-server, SOCKS, proxy y UPnP, e imprime la auditoría de equipo heredado.",
    "variables": [
        {"nombre": "RED_GESTION", "valor": "192.168.88.0/24", "detalle": "Única red desde la que se acepta WinBox y SSH"},
    ],
    "codigo": "# IES Training · MikroTik · L3 · Cerrar puertas\n" + HEAD + """{
:local red {{RED_GESTION}}
# Antes de limitar: hay alguien conectado desde afuera de esa red?
:local fuera 0
:foreach s in=[/user/active/find] do={
  :local a [:toip [/user/active/get $s address]]
  :if ([:typeof $a] = "ip") do={ :if (!($a in $red)) do={ :set fuera ($fuera + 1) } }
}
# Si hay una sesion por WebFig, www no se apaga (te cortaria)
:if ([:len [/user/active/find via="web"]] > 0) do={
  /ip/service/disable telnet,ftp,api
  :put "Ojo: hay una sesion por WebFig. Deje www prendido: apagalo desde WinBox."
} else={ /ip/service/disable telnet,ftp,www,api }
:if ($fuera = 0) do={
  /ip/service/set winbox,ssh available-from=$red
} else={ :put "Ojo: hay sesiones desde fuera de la red de gestion. No limite winbox ni ssh." }
# MAC server y descubrimiento: solo hacia la lista LAN, si existe
:if ([:len [/interface/list/member/find list=LAN]] > 0) do={
  /tool/mac-server/set allowed-interface-list=LAN
  /tool/mac-server/mac-winbox/set allowed-interface-list=LAN
  /ip/neighbor/discovery-settings/set discover-interface-list=LAN
} else={ :put "Ojo: la lista LAN no existe o esta vacia. No toque MAC server ni descubrimiento." }
/tool/bandwidth-server/set enabled=no
/ip/socks/set enabled=no
/ip/proxy/set enabled=no
/ip/upnp/set enabled=no
:put "== Auditoria de equipo heredado (lo normal es que esto este vacio) =="
/system/scheduler/print
/system/script/print
/ip/socks/print
/interface/l2tp-client/print
/ip/firewall/filter/print where dst-port~"5678"
:put "Listo: servicios cerrados y gestion limitada. Verifica con /ip/service/print"
}""",
    "notas": ["Si el script avisa que hay sesiones desde fuera de la red de gestión, no limita WinBox ni SSH: revisá desde dónde estás entrando antes de hacerlo a mano.",
              "available-from deja el puerto visible: para esconderlo hace falta el drop en input (lección 21).",
              "La auditoría solo imprime: lo que nadie reconoce se anota en el legajo y se decide a mano.",
              NOTA_ASCII],
}

# ------------------------------------------------------------------ 5
S["5"] = {
    "titulo": "Preparar VLAN de CCTV y de gestión en el bridge",
    "descripcion": "Arma el puerto de rescate, los puertos access de cámaras, el trunk, la tabla VLAN y las interfaces con IP para CCTV y gestión. Deja comentado el último paso, activar vlan-filtering, para hacerlo a mano desde el puerto de rescate.",
    "variables": [
        {"nombre": "BRIDGE", "valor": "bridge", "detalle": "Nombre del bridge"},
        {"nombre": "ACCESS", "valor": "ether2,ether3", "detalle": "Puertos de cámaras (access), separados por coma"},
        {"nombre": "TRUNK", "valor": "ether4", "detalle": "Puerto trunk hacia el otro switch"},
        {"nombre": "RESCATE", "valor": "ether5", "detalle": "Puerto de rescate, fuera del bridge"},
        {"nombre": "IP_RESCATE", "valor": "10.255.255.1/30", "detalle": "IP del router en el puerto de rescate"},
        {"nombre": "VLAN_CCTV", "valor": "20", "detalle": "VLAN de cámaras y NVR"},
        {"nombre": "IP_CCTV", "valor": "10.10.20.1/24", "detalle": "IP del router en la VLAN de CCTV"},
        {"nombre": "VLAN_GESTION", "valor": "99", "detalle": "VLAN de gestión"},
        {"nombre": "IP_GESTION", "valor": "10.10.99.1/24", "detalle": "IP del router en la VLAN de gestión"},
    ],
    "codigo": "# IES Training · MikroTik · L5 · VLAN por sistema\n" + HEAD + """# NO lo pegues conectado por el puerto de rescate: ese puerto sale del bridge.
{
:local br "{{BRIDGE}}"
:local acc "{{ACCESS}}"
:local trunk "{{TRUNK}}"
:local resc "{{RESCATE}}"
:local vc {{VLAN_CCTV}}
:local vg {{VLAN_GESTION}}
# 1. Puerto de rescate fuera del bridge, con IP propia
:if ([:len [/ip/address/find comment="ies-rescate"]] = 0) do={
  /interface/bridge/port/remove [find interface=$resc]
  /ip/address/add address={{IP_RESCATE}} interface=$resc comment="ies-rescate"
}
# 2. Puertos access (camaras) y trunk
:foreach p in=[:toarray $acc] do={
  /interface/bridge/port/set [find interface=$p] pvid=$vc frame-types=admit-only-untagged-and-priority-tagged ingress-filtering=yes
}
/interface/bridge/port/set [find interface=$trunk] frame-types=admit-only-vlan-tagged ingress-filtering=yes
# 3. Tabla VLAN: una entrada por VLAN; el bridge va tagged para que el router la vea
:if ([:len [/interface/bridge/vlan/find comment="ies-vlan-cctv"]] = 0) do={
  /interface/bridge/vlan/add bridge=$br tagged="$br,$trunk" untagged=$acc vlan-ids=$vc comment="ies-vlan-cctv"
}
:if ([:len [/interface/bridge/vlan/find comment="ies-vlan-gestion"]] = 0) do={
  /interface/bridge/vlan/add bridge=$br tagged="$br,$trunk" vlan-ids=$vg comment="ies-vlan-gestion"
}
# 4. Capa 3: interfaces vlan con su IP
:local ifc ("vlan" . $vc . "-cctv")
:local ifg ("vlan" . $vg . "-gestion")
:if ([:len [/interface/vlan/find name=$ifc]] = 0) do={ /interface/vlan/add name=$ifc interface=$br vlan-id=$vc comment="ies-vlan-cctv" }
:if ([:len [/interface/vlan/find name=$ifg]] = 0) do={ /interface/vlan/add name=$ifg interface=$br vlan-id=$vg comment="ies-vlan-gestion" }
:if ([:len [/ip/address/find comment="ies-ip-cctv"]] = 0) do={ /ip/address/add address={{IP_CCTV}} interface=$ifc comment="ies-ip-cctv" }
:if ([:len [/ip/address/find comment="ies-ip-gestion"]] = 0) do={ /ip/address/add address={{IP_GESTION}} interface=$ifg comment="ies-ip-gestion" }
/interface/bridge/vlan/print
# 5. Ultimo paso, A MANO y conectado por el puerto de rescate:
# /interface/bridge/set [find name="{{BRIDGE}}"] vlan-filtering=yes
:put ("Listo: VLAN " . $vc . " y " . $vg . " cargadas. Revisa la tabla y activa vlan-filtering desde " . $resc . ".")
}""",
    "notas": ["Después de pegarlo, poné la notebook en el puerto de rescate con 10.255.255.2/30 y conectate por ahí.",
              "No activa vlan-filtering: es el único paso que puede dejarte afuera, por eso queda comentado.",
              "Si el puerto de rescate no estaba en el bridge, la línea que lo saca no hace nada.",
              NOTA_ASCII],
}

# ------------------------------------------------------------------ 6
S["6"] = {
    "titulo": "Sacar la foto de antes: export, export sensible y .backup",
    "descripcion": "Guarda un export de texto, un export con show-sensitive y un .backup con contraseña, todos con el mismo prefijo, y lista los archivos. Si ya existen, los reemplaza.",
    "variables": [
        {"nombre": "PREFIJO", "valor": "antes", "detalle": "Prefijo de los archivos (antes, despues, pre-cambio)"},
        {"nombre": "CLAVE_BACKUP", "valor": "Cambiar-Clave-Backup-1", "detalle": "Contraseña del .backup, sin el signo $"},
    ],
    "codigo": "# IES Training · MikroTik · L6 · Backup primero\n" + """# Solo guarda archivos: no cambia la configuracion.
{
:local p "{{PREFIJO}}"
:local clave "{{CLAVE_BACKUP}}"
# Texto para leer y comparar (sin secretos)
/export file=$p
# Texto con claves WiFi, PPPoE y VPN: archivo sensible
/export show-sensitive file=($p . "-sensible")
# Binario para restaurar este mismo equipo, con contrasena
/system/backup/save name=$p password=$clave
:delay 2s
/file/print where name~$p
:put ("Listo: " . $p . ".rsc, " . $p . "-sensible.rsc y " . $p . ".backup. Bajalos y borra del router el sensible si no lo necesitas ahi.")
:put "Para comparar despues: /export file=despues y en la notebook diff antes.rsc despues.rsc"
}""",
    "notas": ["El -sensible.rsc y el .backup van a un lugar con acceso restringido, nunca a un chat ni a un mail sin cifrar.",
              "Anotá la contraseña del .backup en el gestor de claves, no al lado del archivo.",
              "Si pegás dos veces con el mismo prefijo, los archivos se reemplazan: para no perder la foto de antes, usá otro prefijo después del cambio.",
              NOTA_ASCII],
}

# ------------------------------------------------------------------ 7
S["7"] = {
    "titulo": "Preparar la actualización y revisar RouterBOOT",
    "descripcion": "Guarda export y .backup, fija el canal, busca la versión disponible y compara current-firmware con upgrade-firmware. La instalación y el upgrade de RouterBOOT quedan comentados para hacerlos a mano.",
    "variables": [
        {"nombre": "CANAL", "valor": "long-term", "detalle": "long-term o stable (nunca testing ni development en un cliente)"},
        {"nombre": "CLAVE_BACKUP", "valor": "Cambiar-Clave-Backup-1", "detalle": "Contraseña del .backup previo, sin el signo $"},
    ],
    "codigo": "# IES Training · MikroTik · L7 · Actualizar en orden\n" + """# Diagnostico y preparacion: no instala nada por su cuenta.
{
:local canal "{{CANAL}}"
:if ($canal != "long-term" && $canal != "stable") do={ :error "Canal no apto para produccion: usa long-term o stable" }
# 1. Backup antes de tocar
/export file=pre-upgrade
/system/backup/save name=pre-upgrade password="{{CLAVE_BACKUP}}"
# 2. Canal y busqueda (desde 7.23 necesita salir por TCP 443)
/system/package/update/set channel=$canal
/system/package/update/check-for-updates
:delay 5s
:put ("RouterOS instalado: " . [/system/package/update/get installed-version])
:put ("Disponible en " . $canal . ": " . [/system/package/update/get latest-version])
:put ("Estado: " . [/system/package/update/get status])
# 3. RouterBOOT (solo en RouterBOARD)
:if ([/system/routerboard/get routerboard] = true) do={
  :local cur [/system/routerboard/get current-firmware]
  :local upg [/system/routerboard/get upgrade-firmware]
  :put ("current-firmware: " . $cur . " / upgrade-firmware: " . $upg)
  :if ($cur != $upg) do={ :put "Falta RouterBOOT: /system/routerboard/upgrade y despues /system/reboot" }
}
# 4. A mano, con alguien en el sitio o plan de rescate:
# /system/package/update/install
# (despues del reinicio) /system/routerboard/upgrade  y  /system/reboot
:put "Listo: backup pre-upgrade guardado y versiones a la vista. Verifica despues con /log/print where topics~\\"system\\""
}""",
    "notas": ["No instala ni reinicia: esas líneas quedan comentadas para que elijas el momento.",
              "Si no aparece versión disponible, revisá que el router salga a internet por TCP 443.",
              "Si el equipo viene de RouterOS 6, primero va a ofrecer 7.12.1.",
              "Anotá en el legajo versión de RouterOS, de RouterBOOT, canal y fecha.",
              NOTA_ASCII],
}

# ------------------------------------------------------------------ 8
S["8"] = {
    "titulo": "Túnel WireGuard de gestión con un peer por técnico",
    "descripcion": "Crea la interfaz WireGuard con su IP, agrega el peer del técnico si ya pegaste su clave pública y acepta el UDP del túnel y WinBox por el túnel arriba del drop de fábrica.",
    "variables": [
        {"nombre": "WG", "valor": "wg-gestion", "detalle": "Nombre de la interfaz WireGuard"},
        {"nombre": "PUERTO", "valor": "13231", "detalle": "Puerto UDP del túnel"},
        {"nombre": "IP_TUNEL", "valor": "10.10.10.1/24", "detalle": "IP del router dentro del túnel"},
        {"nombre": "PEER", "valor": "notebook-lucia", "detalle": "Nombre del peer (uno por técnico)"},
        {"nombre": "PEER_CLAVE_PUBLICA", "valor": "PEGAR-CLAVE-PUBLICA-DE-LA-NOTEBOOK", "detalle": "Clave pública que muestra la app WireGuard de la notebook"},
        {"nombre": "PEER_IP", "valor": "10.10.10.2/32", "detalle": "IP del técnico en el túnel, siempre /32"},
    ],
    "codigo": "# IES Training · MikroTik · L8 · Tunel de gestion\n" + HEAD + """{
:local wg "{{WG}}"
:local puerto {{PUERTO}}
:local pk "{{PEER_CLAVE_PUBLICA}}"
# 1. Interfaz y direccion
:if ([:len [/interface/wireguard/find name=$wg]] = 0) do={
  /interface/wireguard/add name=$wg listen-port=$puerto comment="ies-wireguard"
}
:if ([:len [/ip/address/find comment="ies-ip-tunel"]] = 0) do={
  /ip/address/add address={{IP_TUNEL}} interface=$wg comment="ies-ip-tunel"
}
# 2. Peer del tecnico (solo si pegaste una clave real)
:if ($pk = "PEGAR-CLAVE-PUBLICA-DE-LA-NOTEBOOK") do={
  :put "Falta la clave publica de la notebook: no agregue el peer."
} else={
  :if ([:len [/interface/wireguard/peers/find public-key=$pk]] = 0) do={
    /interface/wireguard/peers/add interface=$wg name="{{PEER}}" public-key=$pk allowed-address={{PEER_IP}} comment="ies-peer"
  }
}
# 3. Firewall: arriba del drop de fabrica, si existe
:local drop [/ip/firewall/filter/find comment="defconf: drop all not coming from LAN"]
:if ([:len [/ip/firewall/filter/find comment="ies-wireguard"]] = 0) do={
  /ip/firewall/filter/add chain=input protocol=udp dst-port=$puerto action=accept comment="ies-wireguard"
  :if ([:len $drop] > 0) do={ /ip/firewall/filter/move [find comment="ies-wireguard"] destination=[:pick $drop 0] }
}
:if ([:len [/ip/firewall/filter/find comment="ies-winbox-tunel"]] = 0) do={
  /ip/firewall/filter/add chain=input in-interface=$wg protocol=tcp dst-port=8291 action=accept comment="ies-winbox-tunel"
  :if ([:len $drop] > 0) do={ /ip/firewall/filter/move [find comment="ies-winbox-tunel"] destination=[:pick $drop 0] }
}
:if ([:len $drop] = 0) do={ :put "Ojo: no encontre el drop de fabrica. Revisa el orden de input a mano." }
:put ("Clave publica del router: " . [/interface/wireguard/get [find name=$wg] public-key])
:put "Listo: tunel creado. Verifica last-handshake con /interface/wireguard/peers/print"
}""",
    "notas": ["Copiá la clave pública del router que imprime el final al [Peer] de la app, con AllowedIPs = 10.10.10.0/24 y PersistentKeepalive = 25.",
              "Para sumar otro técnico, volvé a pegarlo con otro nombre de peer, otra clave y otra IP /32.",
              "Las reglas se mueven arriba del drop: no hace falta place-before.",
              NOTA_ASCII],
}

# ------------------------------------------------------------------ 9
S["9"] = {
    "titulo": "Diagnóstico: IP directa, NAT del módem o CGNAT",
    "descripcion": "Activa el DDNS de IP Cloud, lee public-address y la compara con las IP de las interfaces de la lista WAN para decir en qué caso estás.",
    "variables": [
        {"nombre": "LISTA_WAN", "valor": "WAN", "detalle": "Interface list donde está la salida a internet"},
    ],
    "codigo": "# IES Training · MikroTik · L9 · Nombre, no puerta\n" + """# Solo diagnostico. El nombre DDNS no abre ningun acceso.
{
:local lista "{{LISTA_WAN}}"
/ip/cloud/set ddns-enabled=yes
/ip/cloud/force-update
:delay 8s
:local pub [:tostr [/ip/cloud/get public-address]]
:put ("dns-name: " . [/ip/cloud/get dns-name])
:put ("public-address: " . $pub . "  (status: " . [/ip/cloud/get status] . ")")
:local caso "sin WAN con IP"
:foreach m in=[/interface/list/member/find list=$lista] do={
  :local i [/interface/list/member/get $m interface]
  :foreach a in=[/ip/address/find interface=$i] do={
    :local d [/ip/address/get $a address]
    :local ip [:toip [:pick $d 0 [:find $d "/"]]]
    :put ("IP de " . $i . ": " . $ip)
    :if ([:tostr $ip] = $pub) do={ :set caso "IP publica directa: se puede publicar con cuidado (leccion 10)" } else={
      :if ($ip in 100.64.0.0/10) do={ :set caso "CGNAT: sin port forwarding; tunel saliente o Back To Home" } else={
        :if ($caso = "sin WAN con IP") do={ :set caso "NAT del modem: modo bridge o reenvio tambien en el modem" }
      }
    }
  }
}
:put ("Listo: " . $caso . ". Verifica con /ip/cloud/print")
# Si no vas a usar el nombre, como sugiere la guia de seguridad:
# /ip/cloud/set ddns-enabled=auto update-time=no
}""",
    "notas": ["Si public-address sale vacío, esperá un minuto y volvé a correrlo: el router tiene que llegar a cloud2.mikrotik.com por UDP 15252.",
              "Con WAN por PPPoE, la interfaz pppoe-out1 tiene que estar en la lista WAN para que el script la mire.",
              "No funciona en RouterOS x86: ahí no existen los servicios cloud.",
              NOTA_ASCII],
}

# ------------------------------------------------------------------ 10
S["10"] = {
    "titulo": "Publicar un puerto del NVR solo para una lista de orígenes",
    "descripcion": "Agrega la IP permitida a una address-list con fecha de revisión, crea un único dst-nat por la lista WAN hacia el NVR y limpia las conexiones viejas a ese puerto. El hairpin queda comentado.",
    "variables": [
        {"nombre": "NVR_IP", "valor": "192.168.88.50", "detalle": "IP interna del NVR"},
        {"nombre": "PUERTO", "valor": "8000", "detalle": "Puerto TCP que usa la app del NVR (cambialo por el real)"},
        {"nombre": "ORIGEN", "valor": "203.0.113.25", "detalle": "IP pública que puede entrar (central de monitoreo)"},
        {"nombre": "LISTA", "valor": "nvr-permitidos", "detalle": "Nombre de la address-list"},
        {"nombre": "REVISAR", "valor": "2027-04", "detalle": "Fecha de revisión de la entrada"},
    ],
    "codigo": "# IES Training · MikroTik · L10 · NVR con criterio\n" + HEAD + """# Primera opcion siempre: VPN (leccion 8). Esto es para cuando no queda otra.
{
:local nvr "{{NVR_IP}}"
:local puerto "{{PUERTO}}"
:local lista "{{LISTA}}"
:if ($puerto = "80" || $puerto = "443" || $puerto = "8291") do={ :error "Ese puerto es del propio router: no se publica." }
# 1. Origen permitido, con fecha de revision
:if ([:len [/ip/firewall/address-list/find list=$lista address={{ORIGEN}}]] = 0) do={
  /ip/firewall/address-list/add list=$lista address={{ORIGEN}} comment="ies-nvr origen, revisar {{REVISAR}}"
}
# 2. Un solo dst-nat: por WAN, un puerto, solo la lista
:if ([:len [/ip/firewall/nat/find comment="ies-nvr"]] = 0) do={
  /ip/firewall/nat/add chain=dstnat in-interface-list=WAN protocol=tcp dst-port=$puerto src-address-list=$lista action=dst-nat to-addresses=$nvr to-ports=$puerto comment="ies-nvr"
} else={
  /ip/firewall/nat/set [find comment="ies-nvr"] dst-port=$puerto src-address-list=$lista to-addresses=$nvr to-ports=$puerto
}
# 3. Conexiones viejas fuera, para que la regla nueva aplique
:local re (":" . $puerto)
/ip/firewall/connection/remove [find where dst-address~$re]
# 4. Hairpin: solo si desde la LAN entran por la IP publica. Ademas, en el
# dst-nat, cambiar in-interface-list=WAN por dst-address-type=local dst-address=!192.168.88.1
# /ip/firewall/nat/add chain=srcnat src-address=192.168.88.0/24 dst-address={{NVR_IP}} protocol=tcp dst-port={{PUERTO}} out-interface=bridge action=masquerade comment="ies-nvr-hairpin"
:put ("Listo: TCP " . $puerto . " hacia " . $nvr . " solo para la lista " . $lista . ". Verifica con /ip/firewall/nat/print stats where comment=\\"ies-nvr\\"")
}""",
    "notas": ["Probá desde el celular con datos móviles: sin estar en la lista no tiene que conectar.",
              "Para sumar otra IP permitida, volvé a pegarlo con otro ORIGEN: la regla de NAT no se duplica.",
              "El hairpin queda comentado: activalo solo si en la oficina entran por la IP pública.",
              NOTA_ASCII],
}
