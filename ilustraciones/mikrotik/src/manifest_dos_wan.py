"""Genera manifest-11b.json (entrada 11 completa, reemplaza la vieja) y manifest-37-39.json."""
import json, re
from pathlib import Path

OUT = Path("/home/claude/ies-training/ilustraciones/mikrotik")
CLASS = Path("/home/claude/claudemy/mikrotik/class")

# ---------------------------------------------------------------- scripts RouterOS


def L(*lines):
    return "\n".join(lines)


def if_route(comment, add_args, set_args):
    return (f':if ([:len [/ip/route/find where comment="{comment}"]] = 0) do={{/ip/route/add {add_args} comment="{comment}"}} '
            f'else={{/ip/route/set [find where comment="{comment}"] {set_args}}}')


def testigo(c, host, gw):
    a = f"dst-address=${host} gateway={gw} scope=10"
    return if_route(c, a, a)


def default_rec(c, host, dist):
    a = f"dst-address=0.0.0.0/0 gateway=${host} target-scope=11 check-gateway=ping distance={dist}"
    return if_route(c, a, a)


def wan_list(*vars_):
    arr = ";".join(f"${v}" for v in vars_)
    return (f':foreach i in={{{arr}}} do={{:if ([:len [/interface/list/member/find where list=WAN and interface=$i]] = 0) do={{'
            f'/interface/list/member/add list=WAN interface=$i comment="ies-dos-wan"}}}}')


MSS = (':if ([:len [/ip/firewall/mangle/find where comment="ies-mss-pppoe"]] = 0) do={/ip/firewall/mangle/add chain=forward '
       'out-interface=$pp protocol=tcp tcp-flags=syn action=change-mss new-mss=clamp-to-pmtu passthrough=yes comment="ies-mss-pppoe"}')
BRIDGE_WARN = (':if ([:len [/interface/bridge/port/find where interface=$WAN]] > 0) do={:put ("Ojo: " . $WAN . " está en el bridge. '
               'Si no entrás por ese puerto, sacalo con /interface/bridge/port/remove [find interface=" . $WAN . "]")}')
HEAD = "# Probalo primero en un equipo de banco y en Safe Mode (Ctrl+X). Antes, un export."

CODE_11 = L(
    "# IES Training · MikroTik · Dos WAN con failover por rutas recursivas",
    HEAD,
    ':local wan1 "{{WAN1_IF}}"',
    ':local wan2 "{{WAN2_IF}}"',
    ':local gw1 "{{GW1}}"',
    ':local gw2 "{{GW2}}"',
    ':local t1a "{{TESTIGO1_A}}"',
    ':local t1b "{{TESTIGO1_B}}"',
    ':local t2a "{{TESTIGO2_A}}"',
    ':local t2b "{{TESTIGO2_B}}"',
    ':local dns "{{DNS}}"',
    "# Testigos: una /32 por su proveedor (scope=10)",
    testigo("ies-testigo-isp1-a", "t1a", "$gw1"),
    testigo("ies-testigo-isp1-b", "t1b", "$gw1"),
    testigo("ies-testigo-isp2-a", "t2a", "$gw2"),
    testigo("ies-testigo-isp2-b", "t2b", "$gw2"),
    "# Rutas por defecto recursivas: ISP1 distancia 1, ISP2 distancia 2",
    default_rec("ies-default-isp1-a", "t1a", 1),
    default_rec("ies-default-isp1-b", "t1b", 1),
    default_rec("ies-default-isp2-a", "t2a", 2),
    default_rec("ies-default-isp2-b", "t2b", 2),
    "# Las rutas por defecto comunes a esos gateways compiten: se apagan, no se borran",
    "/ip/route/disable [find where static and dst-address=0.0.0.0/0 and (gateway=$gw1 or gateway=$gw2)]",
    "# Las dos salidas en la lista WAN, para el masquerade de fábrica",
    wan_list("wan1", "wan2"),
    "# DNS del router que no sean testigos",
    "/ip/dns/set servers=[:toarray $dns]",
    "# Clientes DHCP o PPPoE que meten su propia ruta con distancia baja",
    ':foreach c in=[/ip/dhcp-client/find where disabled=no and add-default-route=yes and default-route-distance<3] do={:put ("Ojo: el cliente DHCP de " . [/ip/dhcp-client/get $c interface] . " instala su ruta por defecto con distancia baja")}',
    ':foreach c in=[/interface/pppoe-client/find where disabled=no and add-default-route=yes and default-route-distance<3] do={:put ("Ojo: el PPPoE " . [/interface/pppoe-client/get $c name] . " instala su ruta por defecto con distancia baja")}',
    ':put "Listo: testigos, recursivas con distancias 1 y 2, lista WAN y DNS. Verificá con /ip/route/print where dst-address=0.0.0.0/0"',
)

CODE_37 = L(
    "# IES Training · MikroTik · Dos WAN: PPPoE principal + DHCP de respaldo",
    HEAD,
    ':local wanP "{{WAN_PPPOE_IF}}"',
    ':local wanD "{{WAN_DHCP_IF}}"',
    ':local pp "{{PPPOE_NOMBRE}}"',
    ':local usuario "{{PPPOE_USUARIO}}"',
    ':local clave "{{PPPOE_CLAVE}}"',
    ':local t1 "{{TESTIGO_A}}"',
    ':local t2 "{{TESTIGO_B}}"',
    ':local dns "{{DNS}}"',
    "# El puerto del respaldo no puede estar en el bridge: el script avisa, no lo saca",
    BRIDGE_WARN.replace("$WAN", "$wanD"),
    "# El cliente DHCP de fábrica en el puerto de la fibra, apagado",
    "/ip/dhcp-client/disable [find where interface=$wanP]",
    "# PPPoE principal sin ruta ni DNS automáticos (las rutas las ponen las recursivas)",
    ':if ([:len [/interface/pppoe-client/find where name=$pp]] = 0) do={/interface/pppoe-client/add name=$pp interface=$wanP user=$usuario password=$clave add-default-route=no use-peer-dns=no max-mtu=1492 max-mru=1492 disabled=no comment="ies-wan1"} else={/interface/pppoe-client/set [find where name=$pp] interface=$wanP user=$usuario password=$clave add-default-route=no use-peer-dns=no}',
    "# DHCP de respaldo: su ruta en distancia 2, sin DNS ni NTP del 4G",
    ':if ([:len [/ip/dhcp-client/find where interface=$wanD]] = 0) do={/ip/dhcp-client/add interface=$wanD add-default-route=yes default-route-distance=2 use-peer-dns=no use-peer-ntp=no disabled=no comment="ies-wan2"} else={/ip/dhcp-client/set [find where interface=$wanD] add-default-route=yes default-route-distance=2 use-peer-dns=no use-peer-ntp=no disabled=no}',
    "# Testigos por la interfaz PPPoE (en RouterOS 7 sirve el nombre) y recursivas",
    testigo("ies-testigo-pppoe-a", "t1", "$pp"),
    testigo("ies-testigo-pppoe-b", "t2", "$pp"),
    default_rec("ies-default-pppoe-a", "t1", 1),
    default_rec("ies-default-pppoe-b", "t2", 1),
    "# NAT por las dos salidas y MSS para el PPPoE",
    wan_list("pp", "wanD"),
    MSS,
    "/ip/dns/set servers=[:toarray $dns]",
    "# (Opcional) limpiar UDP cuando vuelve la fibra. Corta las llamadas en curso: sacale el # si lo querés",
    '# /ip/route/add dst-address=$t2 blackhole distance=20 comment="ies-testigo-pppoe-bh"',
    '# /tool/netwatch/add host=$t2 type=simple interval=10s up-script="/ip/firewall/connection/remove [find protocol=udp]" comment="ies-limpia-udp"',
    ':put ("Listo: " . $pp . " principal con testigos " . $t1 . " y " . $t2 . ", " . $wanD . " de respaldo en distancia 2. Verificá con /ip/route/print where dst-address=0.0.0.0/0")',
)

CODE_38 = L(
    "# IES Training · MikroTik · Dos WAN: IP fija principal + PPPoE de respaldo",
    HEAD,
    ':local wanF "{{WAN_FIJA_IF}}"',
    ':local ipF "{{IP_FIJA}}"',
    ':local gwF "{{GW_FIJA}}"',
    ':local wanP "{{WAN_PPPOE_IF}}"',
    ':local pp "{{PPPOE_NOMBRE}}"',
    ':local usuario "{{PPPOE_USUARIO}}"',
    ':local clave "{{PPPOE_CLAVE}}"',
    ':local t1 "{{TESTIGO_A}}"',
    ':local t2 "{{TESTIGO_B}}"',
    ':local dns "{{DNS}}"',
    BRIDGE_WARN.replace("$WAN", "$wanP"),
    "# IP fija en su puerto (si ya estaba, sigue de largo) y sin cliente DHCP ahí",
    "/ip/dhcp-client/disable [find where interface=$wanF]",
    ':do {/ip/address/add address=$ipF interface=$wanF comment="ies-ip-fija"} on-error={:put "La IP fija ya estaba cargada"}',
    "# Testigos por el gateway de la fija y recursivas en distancia 1",
    testigo("ies-testigo-fija-a", "t1", "$gwF"),
    testigo("ies-testigo-fija-b", "t2", "$gwF"),
    default_rec("ies-default-fija-a", "t1", 1),
    default_rec("ies-default-fija-b", "t2", 1),
    "/ip/route/disable [find where static and dst-address=0.0.0.0/0 and gateway=$gwF]",
    "# PPPoE de respaldo con su ruta en distancia 2 y sin sus DNS",
    ':if ([:len [/interface/pppoe-client/find where name=$pp]] = 0) do={/interface/pppoe-client/add name=$pp interface=$wanP user=$usuario password=$clave add-default-route=yes default-route-distance=2 use-peer-dns=no max-mtu=1492 max-mru=1492 disabled=no comment="ies-wan2"} else={/interface/pppoe-client/set [find where name=$pp] interface=$wanP user=$usuario password=$clave add-default-route=yes default-route-distance=2 use-peer-dns=no}',
    wan_list("wanF", "pp"),
    MSS,
    "/ip/dns/set servers=[:toarray $dns]",
    "# Lo que entra por la IP fija responde por la IP fija, sea cual sea el principal",
    ':if ([:len [/routing/table/find where name="por-fija"]] = 0) do={/routing/table/add name=por-fija fib}',
    ':if ([:len [/ip/route/find where comment="ies-tabla-fija"]] = 0) do={/ip/route/add dst-address=0.0.0.0/0 gateway=($gwF . "@main") routing-table=por-fija comment="ies-tabla-fija"}',
    ':if ([:len [/ip/firewall/mangle/find where comment="ies-entra-fija"]] = 0) do={',
    '/ip/firewall/mangle/add chain=prerouting in-interface=$wanF connection-state=new action=mark-connection new-connection-mark=entra-fija comment="ies-entra-fija"',
    '/ip/firewall/mangle/add chain=prerouting in-interface-list=LAN connection-mark=entra-fija action=mark-routing new-routing-mark=por-fija comment="ies-entra-fija"',
    '/ip/firewall/mangle/add chain=output connection-mark=entra-fija action=mark-routing new-routing-mark=por-fija comment="ies-entra-fija"',
    "}",
    "# FastTrack solo usa la tabla main: que no agarre lo marcado",
    "/ip/firewall/filter/set [find where action=fasttrack-connection] connection-mark=no-mark",
    ':put ("Listo: " . $wanF . " principal con recursivas, " . $pp . " de respaldo en distancia 2 y respuestas por la fija. Verificá con /ip/firewall/mangle/print stats where comment=\\"ies-entra-fija\\"")',
)

CODE_39 = L(
    "# IES Training · MikroTik · Dos WAN: IP fija principal + DHCP (4G) de respaldo",
    HEAD,
    ':local wanF "{{WAN_FIJA_IF}}"',
    ':local gwF "{{GW_FIJA}}"',
    ':local wanD "{{WAN_DHCP_IF}}"',
    ':local gw4 "{{GW_4G}}"',
    ':local t1 "{{TESTIGO_A}}"',
    ':local t2 "{{TESTIGO_B}}"',
    ':local dns "{{DNS}}"',
    ':local balancear "{{BALANCEAR}}"',
    ':local locales "{{NO_BALANCEAR}}"',
    BRIDGE_WARN.replace("$WAN", "$wanD"),
    "# Recursivas por la IP fija (la IP ya cargada como en la lección de IP fija)",
    testigo("ies-testigo-fija-a", "t1", "$gwF"),
    testigo("ies-testigo-fija-b", "t2", "$gwF"),
    default_rec("ies-default-fija-a", "t1", 1),
    default_rec("ies-default-fija-b", "t2", 1),
    "/ip/route/disable [find where static and dst-address=0.0.0.0/0 and gateway=$gwF]",
    "# DHCP del 4G de respaldo: distancia 2, sin sus DNS ni NTP",
    ':if ([:len [/ip/dhcp-client/find where interface=$wanD]] = 0) do={/ip/dhcp-client/add interface=$wanD add-default-route=yes default-route-distance=2 use-peer-dns=no use-peer-ntp=no disabled=no comment="ies-wan2"} else={/ip/dhcp-client/set [find where interface=$wanD] add-default-route=yes default-route-distance=2 use-peer-dns=no use-peer-ntp=no disabled=no}',
    wan_list("wanF", "wanD"),
    "/ip/dns/set servers=[:toarray $dns]",
    '# Balanceo PCC: solo si BALANCEAR es "si" y el 4G no tiene tope de datos',
    ':if ($balancear = "si") do={',
    ':foreach t in={"por-fija";"por-4g"} do={:if ([:len [/routing/table/find where name=$t]] = 0) do={/routing/table/add name=$t fib}}',
    ':if ([:len [/ip/route/find where comment="ies-pcc-fija"]] = 0) do={/ip/route/add dst-address=0.0.0.0/0 gateway=($gwF . "@main") routing-table=por-fija check-gateway=ping comment="ies-pcc-fija"}',
    ':if ([:len [/ip/route/find where comment="ies-pcc-4g"]] = 0) do={/ip/route/add dst-address=0.0.0.0/0 gateway=($gw4 . "@main") routing-table=por-4g check-gateway=ping comment="ies-pcc-4g"}',
    ':foreach n in=[:toarray $locales] do={:do {/ip/firewall/address-list/add list=no-balancear address=$n comment="ies-pcc"} on-error={}}',
    ':if ([:len [/ip/firewall/mangle/find where comment="ies-pcc"]] = 0) do={',
    '/ip/firewall/mangle/add chain=prerouting in-interface-list=LAN dst-address-list=no-balancear action=accept comment="ies-pcc"',
    '/ip/firewall/mangle/add chain=prerouting in-interface-list=LAN dst-address-type=!local connection-state=new connection-mark=no-mark per-connection-classifier=both-addresses:2/0 action=mark-connection new-connection-mark=pcc-fija comment="ies-pcc"',
    '/ip/firewall/mangle/add chain=prerouting in-interface-list=LAN dst-address-type=!local connection-state=new connection-mark=no-mark per-connection-classifier=both-addresses:2/1 action=mark-connection new-connection-mark=pcc-4g comment="ies-pcc"',
    '/ip/firewall/mangle/add chain=prerouting in-interface-list=LAN connection-mark=pcc-fija action=mark-routing new-routing-mark=por-fija comment="ies-pcc"',
    '/ip/firewall/mangle/add chain=prerouting in-interface-list=LAN connection-mark=pcc-4g action=mark-routing new-routing-mark=por-4g comment="ies-pcc"',
    "}",
    "/ip/firewall/filter/set [find where action=fasttrack-connection] connection-mark=no-mark",
    "}",
    ':put ("Listo: " . $wanF . " principal con recursivas y " . $wanD . " de respaldo en distancia 2, balanceo: " . $balancear . ". Verificá con /ip/route/print where dst-address=0.0.0.0/0")',
)

V_T = [{"nombre": "TESTIGO_A", "valor": "1.1.1.1", "detalle": "Primer host testigo del principal (que no sea un DNS de la red)"},
       {"nombre": "TESTIGO_B", "valor": "9.9.9.9", "detalle": "Segundo host testigo del principal"},
       {"nombre": "DNS", "valor": "1.0.0.1,8.8.4.4", "detalle": "DNS del router separados por coma, distintos de los testigos"}]
V_PPPOE = [{"nombre": "PPPOE_NOMBRE", "valor": "pppoe-antel", "detalle": "Nombre de la interfaz PPPoE"},
           {"nombre": "PPPOE_USUARIO", "valor": "cliente-ejemplo", "detalle": "Usuario PPPoE que entrega el proveedor"},
           {"nombre": "PPPOE_CLAVE", "valor": "Clave-De-Ejemplo-1", "detalle": "Clave PPPoE: este valor es de ejemplo, poné la del servicio"}]

SCRIPTS = {
    "11": {
        "titulo": "Failover con dos WAN por rutas recursivas",
        "descripcion": "Crea dos testigos por proveedor con su /32, las rutas por defecto recursivas con distancias 1 y 2, suma las dos salidas a la lista WAN y fija DNS que no son testigos. Avisa si algún cliente DHCP o PPPoE mete su propia ruta con distancia baja.",
        "variables": [
            {"nombre": "WAN1_IF", "valor": "ether1", "detalle": "Interfaz del proveedor principal (con gateway fijo)"},
            {"nombre": "WAN2_IF", "valor": "ether2", "detalle": "Interfaz del proveedor de respaldo"},
            {"nombre": "GW1", "valor": "203.0.113.9", "detalle": "Gateway del principal"},
            {"nombre": "GW2", "valor": "192.168.8.1", "detalle": "Gateway del respaldo (por ejemplo, el router 4G)"},
            {"nombre": "TESTIGO1_A", "valor": "1.1.1.1", "detalle": "Primer testigo del principal"},
            {"nombre": "TESTIGO1_B", "valor": "9.9.9.9", "detalle": "Segundo testigo del principal"},
            {"nombre": "TESTIGO2_A", "valor": "8.8.8.8", "detalle": "Primer testigo del respaldo"},
            {"nombre": "TESTIGO2_B", "valor": "208.67.222.222", "detalle": "Segundo testigo del respaldo"},
            {"nombre": "DNS", "valor": "1.0.0.1,8.8.4.4", "detalle": "DNS del router separados por coma, distintos de los testigos"}],
        "codigo": CODE_11,
        "notas": ["Pensado para gateways estables (IP fija o un router 4G en modo router). Con PPPoE o DHCP en el principal, usá el script de la lección de esa combinación.",
                  "Apaga (no borra) las rutas por defecto estáticas a GW1 y GW2: si algo falla, se vuelven a habilitar.",
                  "No arma marcas para el acceso entrante ni limpia conexiones: eso está en los pasos 6 y 7 del laboratorio.",
                  "Probalo cortando aguas arriba del módem y anotá cuántos pings se pierden al conmutar y al volver."],
    },
    "37": {
        "titulo": "PPPoE de Antel principal y 4G por DHCP de respaldo",
        "descripcion": "Crea el PPPoE sin ruta automática, el cliente DHCP de respaldo en distancia 2, los testigos por la interfaz PPPoE con sus rutas recursivas, NAT por las dos salidas, MSS y DNS fijos. El Netwatch que limpia UDP queda comentado.",
        "variables": [{"nombre": "WAN_PPPOE_IF", "valor": "ether1", "detalle": "Puerto conectado al ONT en modo puente"},
                      {"nombre": "WAN_DHCP_IF", "valor": "ether2", "detalle": "Puerto conectado al router 4G o cablemódem"}] + V_PPPOE + V_T,
        "codigo": CODE_37,
        "notas": ["Si el puerto del 4G está en el bridge, el script avisa y no lo saca: hacelo a mano si no entrás por ahí.",
                  "Si Antel pide VLAN, el PPPoE va sobre la VLAN: ninguna fuente leída lo confirma; probá antes con /interface/pppoe-client/scan.",
                  "Cambiá la clave de ejemplo por la del servicio antes de pegar.",
                  "Verificá con /interface/pppoe-client/monitor y /ip/route/print where dst-address=0.0.0.0/0."],
    },
    "38": {
        "titulo": "IP fija principal, PPPoE de respaldo y respuestas por la fija",
        "descripcion": "Carga la IP fija si falta, arma testigos y recursivas por su gateway, deja el PPPoE de respaldo con su ruta en distancia 2 y agrega la tabla por-fija con las tres marcas para que lo que entra por la IP fija responda por ahí.",
        "variables": [{"nombre": "WAN_FIJA_IF", "valor": "ether1", "detalle": "Puerto del enlace con IP fija"},
                      {"nombre": "IP_FIJA", "valor": "203.0.113.10/29", "detalle": "IP fija con máscara"},
                      {"nombre": "GW_FIJA", "valor": "203.0.113.9", "detalle": "Gateway de la IP fija"},
                      {"nombre": "WAN_PPPOE_IF", "valor": "ether2", "detalle": "Puerto del PPPoE de respaldo"}] + V_PPPOE[:1] + [dict(V_PPPOE[0], valor="pppoe-respaldo")][:0] + V_PPPOE[1:] + V_T,
        "codigo": CODE_38,
        "notas": ["No crea el port forward: armalo como en la lección de port forwarding, atado a la IP fija y a una lista de origen.",
                  "Cambia FastTrack para que no agarre conexiones marcadas: en un router chico puede subir la CPU.",
                  "Cambiá la clave de ejemplo por la del servicio antes de pegar.",
                  "Verificá con /ip/firewall/mangle/print stats y probando el acceso publicado desde afuera."],
    },
    "39": {
        "titulo": "IP fija principal y 4G por DHCP de respaldo, con PCC opcional",
        "descripcion": "Arma testigos y recursivas por la IP fija, el cliente DHCP del 4G en distancia 2 sin sus DNS y la lista WAN. Con BALANCEAR en si, agrega el balanceo PCC con dos tablas, la lista no-balancear y FastTrack solo para lo no marcado.",
        "variables": [{"nombre": "WAN_FIJA_IF", "valor": "ether1", "detalle": "Puerto del enlace con IP fija (la IP ya cargada)"},
                      {"nombre": "GW_FIJA", "valor": "203.0.113.9", "detalle": "Gateway de la IP fija"},
                      {"nombre": "WAN_DHCP_IF", "valor": "ether2", "detalle": "Puerto del router 4G"},
                      {"nombre": "GW_4G", "valor": "192.168.8.1", "detalle": "Gateway que entrega el router 4G (para PCC)"}] + V_T + [
                      {"nombre": "BALANCEAR", "valor": "no", "detalle": "si para agregar PCC; solo con un segundo enlace sin tope de datos"},
                      {"nombre": "NO_BALANCEAR", "valor": "192.168.88.0/24,192.168.8.0/24,203.0.113.8/29", "detalle": "Redes locales y de las WAN que no se balancean, separadas por coma"}],
        "codigo": CODE_39,
        "notas": ["Con el 4G en IP privada o CGNAT, nada publicado entra por ahí y Back To Home pasa por el relay.",
                  "Si el gateway del 4G cambia, PCC necesita el script de lease del cliente DHCP en vez de GW_4G fijo.",
                  "Con PCC, el chequeo de cada tabla mira solo el gateway, no internet.",
                  "Verificá con /ip/route/print where dst-address=0.0.0.0/0 y, con PCC, contando conexiones por marca."],
    },
}
# 38: nombre de interfaz PPPoE propio
SCRIPTS["38"]["variables"] = [v if v["nombre"] != "PPPOE_NOMBRE" else dict(v, valor="pppoe-respaldo") for v in SCRIPTS["38"]["variables"]]

# ---------------------------------------------------------------- manifests
M11 = {
    "fig": {"file": "11.svg", "alt": "La LAN 192.168.88.0/24 conectada al router. ether1 va al ISP1 con IP fija 203.0.113.10/29, gateway 203.0.113.9 y ruta recursiva con distance=1; ether2 va al router 4G con gateway 192.168.8.1 y distance=2 de respaldo. Cada ISP tiene sus testigos con ruta /32 y scope=10: 1.1.1.1 y 9.9.9.9 para el ISP1, 8.8.8.8 y 208.67.222.222 para el ISP2. Abajo, tres tarjetas: la IP fija escribe su ruta en /ip/route, el cliente DHCP la instala con default-route-distance y el PPPoE con add-default-route y default-route-distance.",
            "caption": "Cada WAN pone su ruta por defecto distinto; la distancia decide cuál trabaja y los testigos dicen si hay internet."},
    "steps": [
        {"file": "11-paso3.svg", "step": 3, "alt": "Tres cajas encadenadas: la ruta 0.0.0.0/0 con gateway=1.1.1.1 y target-scope=11 se resuelve con la ruta 1.1.1.1/32 por 203.0.113.9 con scope=10, que a su vez se resuelve con la red conectada 203.0.113.8/29 en ether1. Debajo, el ping de check-gateway sale del router, pasa por el módem e internet y llega a 1.1.1.1. Una nota explica que la ruta del DHCP del 4G, con scope 30, no puede resolver el testigo.",
         "caption": "La default apunta al testigo y el ping de check-gateway llega hasta él, pasando por el módem.", "after": "Rutas por defecto recursivas, y apagá"},
        {"file": "11-paso5.svg", "step": 5, "alt": "Una fila de pings desde la notebook: cinco bien por el ISP1, seis perdidos hasta conmutar y cinco bien por el ISP2. Debajo, la tabla de rutas por defecto: las de 1.1.1.1 y 9.9.9.9 activas antes y inactivas con el corte; las de 8.8.8.8 y 208.67.222.222 en espera antes y activas con el corte. Una nota aclara que el corte simulado descarta los pings del router a los testigos y que el módem sigue vivo.",
         "caption": "Con el corte simulado caen las recursivas del ISP1 y entran las del ISP2; contá los pings perdidos.", "after": "Simulá internet caída con el módem vivo"},
        {"file": "11-paso7.svg", "step": 7, "alt": "Dos paneles. Sin marcas: un pedido entra por el ISP2, el NVR responde y la respuesta sale por el ISP1 con otra IP y se descarta. Con marcas: la respuesta sale por el ISP2. Abajo, las tres reglas de mangle: marcar la conexión nueva que entra por ether2, marcar la ruta de las respuestas desde la LAN y marcar la ruta de las respuestas del propio router en output.",
         "caption": "La marca de conexión recuerda por dónde entró; la marca de ruteo manda la respuesta por ahí.", "after": "que la respuesta salga por donde entró"},
    ],
    "concepts": [
        {"name": "Failover o balanceo",
         "para_que": "Dos enlaces se pueden usar de dos maneras: uno trabaja y el otro espera (failover), o los dos trabajan a la vez repartiendo conexiones (balanceo). La mayoría de las obras de seguridad electrónica necesitan continuidad, no más ancho de banda, y el respaldo suele ser un 4G con datos limitados.",
         "como": "El failover se arma con distancias: la ruta del principal con distancia menor y la del respaldo con distancia mayor, más algo que detecte la caída. El balanceo por conexión usa PCC con marcas y una tabla por enlace; la documentación de MikroTik lo describe como obligatorio por conexión cuando controlás una sola punta.",
         "ejemplo": "Un supermercado con fibra y un 4G de 30 GB: failover. Una oficina con dos fibras parecidas de proveedores distintos que pide sumar velocidad: PCC, con la lista de redes locales que no se balancean."},
        {"name": "check-gateway y rutas recursivas",
         "para_que": "check-gateway=ping le hace ping al gateway cada 10 segundos y, con dos fallas, deja la ruta inactiva. Mira el próximo salto, que casi siempre es el módem. La ruta recursiva cambia a quién se le hace el ping: a un host testigo en internet que se alcanza por ese proveedor.",
         "como": "Una /32 a cada testigo por el gateway de su proveedor con scope=10 y la ruta por defecto con gateway=<testigo>, target-scope=11 y check-gateway=ping. Dos testigos por enlace: el cambio completo ocurre solo cuando fallan los dos. Los testigos no se usan como DNS de la red.",
         "ejemplo": "En un local de Pando una obra corta la fibra en la vereda. El módem sigue con luz verde y contesta, pero 1.1.1.1 y 9.9.9.9 no: las dos defaults del ISP1 caen y las cajas siguen cobrando por el 4G. Con check-gateway al módem, el local se habría quedado sin internet."},
        {"name": "Conntrack al conmutar y al volver",
         "para_que": "Cada conexión queda registrada en connection tracking con su traducción de NAT. Si el enlace cambia, las conexiones viejas siguen con la IP del enlace anterior y no sirven por el nuevo.",
         "como": "El masquerade borra sus conexiones cuando la interfaz se cae o cambia de IP. Con rutas recursivas la interfaz no se cae, así que las conexiones quedan hasta que vencen. Se miran en /ip/firewall/connection y, si hace falta, un Netwatch borra las UDP al volver el principal.",
         "ejemplo": "Vuelve la fibra y el teléfono IP de la recepción no registra: su conexión UDP se armó por el 4G y sigue ahí. Borrar las conexiones UDP lo resuelve sin reiniciar el router, sabiendo que corta las llamadas en curso."},
        {"name": "Acceso entrante con dos WAN",
         "para_que": "Un port forward, WinBox o Back To Home reciben pedidos por una WAN, pero la respuesta sigue la ruta por defecto. Si el pedido entró por la WAN que no es la principal, la respuesta sale por la otra con otra IP y se pierde.",
         "como": "Se marca la conexión nueva según la interfaz de entrada (mark-connection en prerouting), después se marca la ruta de sus respuestas desde la LAN y desde el router (mark-routing en prerouting y output) hacia una tabla creada en /routing/table con su ruta por defecto por esa WAN. FastTrack solo usa la tabla main, así que se limita a connection-mark=no-mark.",
         "ejemplo": "Una central de monitoreo entra al NVR por la IP del segundo proveedor mientras la fibra es la principal. Sin marcas, el NVR responde por la fibra y la central no ve nada; con las tres reglas, la respuesta sale por donde entró."},
    ],
    "teoria_md": """### Un poco de historia

Los grandes operadores resuelven la redundancia con BGP y bloques de IP propios. Un comercio o una oficina no tiene eso: tiene dos proveedores, cada uno con su IP y su gateway, y un router que tiene que elegir. La solución clásica es tener dos rutas por defecto con distinta prioridad y algo que detecte cuándo la principal dejó de servir.

La búsqueda recursiva del próximo salto nació para BGP: un vecino iBGP anuncia rutas cuyo next hop está a varios saltos, y el router tiene que resolverlo con otras rutas. RouterOS controla esa búsqueda con `scope` y `target-scope`. En el foro de MikroTik describen el failover con testigos como un uso creativo de esa búsqueda, y la documentación oficial lo enseña en su artículo de Failover. En RouterOS 7, estable desde 2021, `target-scope` y `check-gateway` pasaron a guardarse por gateway, y las tablas de ruteo se crean en `/routing/table` antes de usarlas.

El otro protagonista es el NAT. El RFC 1631, de 1994, lo describió como una salida temporal a la falta de direcciones, y el RFC 3022, de 2001, lo actualizó. MikroTik pensó `masquerade` para IP dinámicas: cuando la interfaz se cae o cambia de IP, borra sus conexiones.

### Cómo funciona

Cada ruta tiene una `distance`. Entre rutas al mismo destino gana la menor; con la misma distancia, quedan activas las dos y se reparte el tráfico (ECMP). El cliente DHCP pone su ruta con `default-route-distance` y el PPPoE con `add-default-route` y `default-route-distance`.

Con `check-gateway=ping`, el router le hace ping al gateway cada 10 segundos, espera 1 segundo y, tras dos fallas, deja la ruta inactiva. En la ruta recursiva el gateway es el testigo: la default dice `gateway=1.1.1.1` con `target-scope=11`, y el router busca cómo llegar a 1.1.1.1 solo entre rutas con `scope` menor o igual a 11. La /32 con `scope=10` cumple; la ruta del DHCP, con scope 30, no. El ping viaja hasta el testigo, y si cualquier tramo se corta, la ruta cae.

Al conmutar, conntrack conserva cada conexión con su traducción. Si la interfaz no bajó, nada las borra, y las que se armaron por un enlace quedan inservibles por el otro hasta que vencen.

Lo que entra de afuera sigue la misma lógica de ruteo: la respuesta sale por la ruta por defecto. Por eso se marca la conexión al entrar y se marca la ruta de su respuesta hacia una tabla que sale por la misma WAN.
""",
    "script_rsc": SCRIPTS["11"],
}

M37 = {
    "fig": {"file": "37.svg", "alt": "El router con la LAN a la izquierda. ether1 lleva al principal, el PPPoE de Antel pppoe-antel con add-default-route=no, testigos por la interfaz y ruta recursiva con distance=1, conectado a los testigos 1.1.1.1 y 9.9.9.9 con gateway=pppoe-antel. ether2 lleva al respaldo, el DHCP del router 4G con gateway 192.168.8.1, default-route-distance=2 y use-peer-dns=no. A la derecha, los DNS del router 1.0.0.1 y 8.8.4.4, que no son testigos.",
            "caption": "El PPPoE trabaja con rutas recursivas por su interfaz; el DHCP del 4G espera en distancia 2 y sin sus DNS."},
    "steps": [
        {"file": "37-paso1.svg", "step": 1, "alt": "El router con cinco puertos: ether1 en azul con un cable marcado PPPoE al ONT de Antel en modo puente, ether2 en ámbar con un cable marcado DHCP al router 4G 192.168.8.1, y ether3 en verde a la notebook. Una etiqueta indica que el bridge queda con ether3 a ether5. Una nota avisa que si entrás por ether2, al sacarlo del bridge te cortás.",
         "caption": "ether2 sale del bridge antes de ser WAN; entrás por ether3.", "after": "Apagá el cliente DHCP de fábrica"},
        {"file": "37-paso4.svg", "step": 4, "alt": "La tabla esperada: 1.1.1.1/32 y 9.9.9.9/32 por pppoe-antel, activas; dos rutas 0.0.0.0/0 por 1.1.1.1 y 9.9.9.9 con distancia 1, activas; la ruta 0.0.0.0/0 del DHCP por 192.168.8.1 con distancia 2, en espera. A la derecha, dos avisos: una default por pppoe-antel con distancia 1 significa que el PPPoE quedó con add-default-route=yes y el failover nunca ocurre; la ruta del DHCP con distancia 1 reparte tráfico con la fibra.",
         "caption": "Las recursivas activas y el DHCP en espera; una default por pppoe-antel en distancia 1 es el error.", "after": "Testigos por la interfaz PPPoE y rutas"},
        {"file": "37-paso7.svg", "step": 7, "alt": "Dos paneles. Corte 1, la sesión se cae: pppoe-antel baja, la /32 queda inactiva, las recursivas caen y entra la del DHCP, y masquerade borra sus conexiones solo. Corte 2, PPPoE arriba sin internet: la sesión sigue y solo fallan los testigos, las recursivas caen y entra la del DHCP, y las conexiones por la fibra quedan. Abajo, al volver la fibra, lo armado por el 4G sigue en conntrack y se mira con un print filtrado por 192.168.8.",
         "caption": "Dos cortes distintos llevan al mismo failover, pero dejan conntrack distinto.", "after": "Corte 2, PPPoE arriba sin internet"},
    ],
    "concepts": [
        {"name": "Recursiva por la interfaz PPPoE",
         "para_que": "En PPPoE la IP del otro extremo puede cambiar en cada reconexión, así que una ruta al testigo por una IP fija de gateway se rompería. Usar el nombre de la interfaz como gateway evita depender de esa IP.",
         "como": "La /32 al testigo va con gateway=pppoe-antel y scope=10, y la ruta por defecto con gateway=<testigo>, target-scope=11 y check-gateway=ping. El PPPoE va con add-default-route=no para que su ruta automática no compita. Según el foro, en RouterOS 6 esto no resolvía y hacía falta la IP; en RouterOS 7 el nombre de la interfaz sirve.",
         "ejemplo": "Un local de Maldonado con fibra de Antel por PPPoE: a la madrugada el PPPoE se reconecta y cambia la IP del concentrador. Las rutas a 1.1.1.1 y 9.9.9.9 por pppoe-antel siguen valiendo y el failover queda armado sin tocar nada."},
        {"name": "El DHCP que se cuela",
         "para_que": "El cliente DHCP del respaldo instala su ruta por defecto con distancia 1 y suma los DNS del 4G. Sin tocarlo, el router reparte tráfico entre la fibra y el 4G y mezcla DNS que viven detrás de enlaces distintos.",
         "como": "default-route-distance=2, use-peer-dns=no y use-peer-ntp=no en el cliente del 4G, y DNS fijos en /ip/dns que no sean los testigos. Antes, ether2 fuera del bridge de fábrica: si queda adentro, el DHCP del 4G atiende a la LAN.",
         "ejemplo": "Un técnico suma el 4G y al rato las cámaras toman IP 192.168.8.x: ether2 seguía en el bridge. Lo saca del bridge, crea el cliente DHCP con distancia 2 y la LAN vuelve a su rango."},
        {"name": "Dos cortes, dos pruebas",
         "para_que": "Que se caiga la sesión PPPoE y que la sesión siga arriba sin internet son fallas distintas, y el failover tiene que resolver las dos. Además dejan conntrack distinto.",
         "como": "Corte 1: deshabilitar el cliente PPPoE; la interfaz baja, la /32 queda inactiva y masquerade borra sus conexiones. Corte 2: descartar en la cadena output los pings del router a los testigos; la sesión sigue y solo las recursivas lo ven. Al volver, mirar las conexiones que quedaron armadas por el 4G.",
         "ejemplo": "En el acta de entrega de una farmacia quedan los dos números: pings perdidos al cortar la sesión y al simular el corte con el PPPoE arriba, y lo mismo al volver."},
    ],
    "teoria_md": """### Un poco de historia

PPPoE lleva el protocolo PPP, el de los módems telefónicos, sobre Ethernet. Está definido en el RFC 2516, de 1999, y se volvió el estándar de los proveedores para identificar a cada cliente por usuario y clave. En Uruguay es la forma en que el router propio marca la fibra de Antel con el ONT en modo puente, como vimos en la lección de PPPoE con Antel.

DHCP llegó antes a las LAN: el RFC 2131, de 1997, describe cómo un equipo recibe dirección, gateway y DNS sin configurar nada. Los routers 4G y los cablemódems lo usan para entregar IP al equipo que se conecta detrás. El RFC 3442 sumó las rutas sin clase (opción 121), que la documentación del cliente DHCP de MikroTik menciona porque cambia qué ruta por defecto se instala.

Cuando los técnicos empezaron a combinar los dos en un mismo router apareció la pregunta de este capítulo: cómo hacer rutas recursivas si el gateway del PPPoE no es fijo. En el foro de MikroTik hay un hilo de 2015, con RouterOS 6, que no lo logró; en 2024 otro hilo aclara que en RouterOS 7 el nombre de la interfaz alcanza.

### Cómo funciona

El PPPoE crea una interfaz punto a punto, `pppoe-antel`. Como es punto a punto, el router sabe que todo lo que manda por ahí llega al otro extremo, y por eso una ruta puede tener la interfaz como gateway. Con `add-default-route=yes`, el cliente instala una ruta por defecto que existe mientras la sesión esté arriba, haya internet o no. Por eso, cuando el PPPoE es el principal, se apaga esa ruta y se reemplaza por las recursivas.

El cliente DHCP del 4G instala su ruta con `default-route-distance`, 1 de fábrica. Con 2, espera. Con `use-peer-dns=no`, no suma los DNS del 4G.

Los dos cortes recorren caminos distintos. Si la sesión cae, la interfaz baja, la /32 queda inactiva y las recursivas no pueden resolver su gateway; `masquerade` además borra las conexiones de esa interfaz. Si la sesión sigue pero no hay internet, solo los pings de `check-gateway` a los testigos lo detectan. Al volver, lo que se armó por el 4G sigue en conntrack, porque ether2 nunca bajó.
""",
    "script_rsc": SCRIPTS["37"],
}

M38 = {
    "fig": {"file": "38.svg", "alt": "El router con el NVR 192.168.88.20:443 en la LAN. ether1 lleva al principal, la IP fija 203.0.113.10/29 con gateway 203.0.113.9, testigos 1.1.1.1 y 9.9.9.9 y ruta recursiva con distance=1. ether2 lleva al respaldo, pppoe-respaldo con add-default-route=yes y default-route-distance=2. La central de monitoreo 198.51.100.50 entra a 203.0.113.10:8443. Al lado del PPPoE, una caja dice IP dinámica: nada publicado entra por acá.",
            "caption": "La fija trabaja y publica; el PPPoE espera en distancia 2 y no publica nada."},
    "steps": [
        {"file": "38-paso5.svg", "step": 5, "alt": "Dos reglas de dst-nat. Así: chain=dstnat in-interface=ether1 dst-address=203.0.113.10 protocol=tcp dst-port=8443 src-address-list=monitoreo hacia 192.168.88.20:443, solo la central y solo por la IP fija. Así no: chain=dstnat in-interface-list=WAN protocol=tcp dst-port=8443 hacia el mismo NVR, que agarra por las dos WAN y para cualquiera, y lo que entra por el PPPoE responde por la fija.",
         "caption": "El dst-nat va atado a ether1, a la IP fija y a la lista de la central.", "after": "El servicio publicado, solo por la IP"},
        {"file": "38-paso7.svg", "step": 7, "alt": "Dos paneles con el PPPoE como principal. Sin marcas: la central entra por la IP fija y el router responde por el PPPoE con otra IP, y no abre. Con marcas: la respuesta sale por la IP fija. Abajo, la tabla por-fija con su ruta por 203.0.113.9@main y las tres reglas de mangle: marcar la conexión nueva que entra por ether1, marcar la ruta de las respuestas desde la LAN y de las respuestas del router en output. Una línea recuerda limitar FastTrack a connection-mark=no-mark.",
         "caption": "Con el PPPoE de principal, las marcas devuelven por la fija lo que entró por la fija.", "after": "Al revés: el PPPoE pasa a principal"},
    ],
    "concepts": [
        {"name": "Respaldo sin testigos",
         "para_que": "Las rutas recursivas sirven para saber si el enlace que trabaja tiene internet. El respaldo solo trabaja cuando el principal cayó, así que no necesita detectar nada para entrar.",
         "como": "El PPPoE de respaldo deja su ruta automática con add-default-route=yes y default-route-distance=2. Mientras las recursivas de la fija estén activas, esa ruta espera; cuando caen, entra. Con distancia 1 repartiría tráfico con la fija.",
         "ejemplo": "Un depósito con enlace dedicado de IP fija y un PPPoE de otro proveedor: un corte en la fibra del dedicado hace caer las recursivas y la ruta del PPPoE entra sola."},
        {"name": "dst-nat atado a la IP fija",
         "para_que": "Un dst-nat abierto en toda la lista WAN agarra pedidos por las dos salidas y para cualquier origen. Por el PPPoE, además, la respuesta sale por la fija y se pierde.",
         "como": "in-interface=ether1 y dst-address=203.0.113.10, con src-address-list para la central de monitoreo, como en la lección de port forwarding. La IP dinámica del PPPoE no publica nada.",
         "ejemplo": "La central de monitoreo tiene IP fija 198.51.100.50: el NVR se publica en 203.0.113.10:8443 solo para esa dirección, y el resto de internet no ve el puerto."},
        {"name": "Marca de conexión y marca de ruteo",
         "para_que": "La respuesta a un pedido sigue la ruta por defecto. Si el principal es el PPPoE, lo que entra por la fija responde por el PPPoE con otra IP y no abre.",
         "como": "Una tabla por-fija en /routing/table con su ruta 0.0.0.0/0 por 203.0.113.9@main; mark-connection en prerouting para lo nuevo que entra por ether1; mark-routing hacia por-fija para sus respuestas desde la LAN (prerouting con in-interface-list=LAN) y desde el router (output). FastTrack solo para connection-mark=no-mark, porque trabaja con la tabla main.",
         "ejemplo": "Un cliente cambia de proveedor y deja el PPPoE nuevo como principal. Con las tres reglas cargadas desde el día uno, la central sigue entrando por la IP fija sin que nadie note el cambio."},
    ],
    "teoria_md": """### Un poco de historia

El enlace dedicado con IP fija es el servicio clásico de empresa: dirección pública que no cambia, gateway estable y, muchas veces, un rango ruteado. Sobre esa IP se publican servicios que terceros necesitan alcanzar, como una central de monitoreo que entra al NVR. El PPPoE dinámico aparece como respaldo barato, o al revés, como principal cuando el dedicado queda de reserva.

El ruteo por políticas existe en RouterOS desde mucho antes de la versión 7, pero cambió de lugar con ella. La guía de migración de MikroTik lo resume: las reglas pasaron de `/ip route rule` a `/routing rule`, y cada tabla se crea en `/routing/table` con `fib` antes de referenciarla. La misma guía advierte que marcar tráfico local con mangle deja inalcanzables las IP del propio router.

En el foro, un hilo de 2024 con PPPoE más IP fija lo dice sin vueltas: para que el router responda desde la dirección a la que llegó el pedido hace falta ruteo por políticas, y con servidores en la LAN, marcas de conexión.

### Cómo funciona

Cada paquete que el router reenvía pasa por una decisión de ruteo que mira destino, origen, interfaz de entrada y marca de ruteo. Sin marca, se usa la tabla `main`, donde está la ruta por defecto activa.

La marca de ruteo es por paquete; la de conexión queda guardada en conntrack para toda la conexión. Por eso se combinan: cuando entra una conexión nueva por ether1, `mark-connection` le pone `entra-fija`. Cuando el NVR responde, el paquete llega desde la LAN con esa conexión marcada y `mark-routing` lo manda a la tabla `por-fija`, cuya ruta por defecto sale por 203.0.113.9. Si responde el propio router, como con WinBox, el paquete nace en la cadena `output` y necesita la misma marca ahí.

FastTrack acelera conexiones establecidas salteando el firewall, y según la documentación de mangle solo trabaja con la tabla `main`. Si una conexión marcada entra en FastTrack, sus paquetes se escapan por la ruta por defecto. Limitar la regla de FastTrack a `connection-mark=no-mark` lo evita, a costa de algo de CPU.
""",
    "script_rsc": SCRIPTS["38"],
}

M39 = {
    "fig": {"file": "39.svg", "alt": "El router con la LAN a la izquierda. ether1 lleva al principal, la IP fija 203.0.113.10/29 con gateway 203.0.113.9, testigos 1.1.1.1 y 9.9.9.9 y ruta recursiva con distance=1. ether2 lleva al respaldo, el DHCP del router 4G con gateway 192.168.8.1, default-route-distance=2 e IP privada o CGNAT. A la derecha, con el 4G activo: sale todo, no entra lo publicado y Back To Home va por el relay.",
            "caption": "Con el 4G activo sale todo, pero nada publicado entra y Back To Home pasa por el relay."},
    "steps": [
        {"file": "39-paso5.svg", "step": 5, "alt": "Dos terminales con /ip/cloud/force-update y /ip/cloud/print. Con la fibra activa: public-address 203.0.113.10 y vpn-relay-ipv4-status reachable directly. Con el 4G activo: public-address 198.51.100.77, un ejemplo, y reachable via relay. Una nota explica que la nube contesta con la IP desde la que recibió el pedido y que el nombre sigue a la WAN por la que sale el router, con TTL de 60 segundos.",
         "caption": "public-address y el estado del relay cambian cuando el router sale por el 4G.", "after": "Mirá cómo cambia lo que ve la nube"},
        {"file": "39-paso7.svg", "step": 7, "alt": "Diagrama de flujo de PCC. Una conexión nueva desde la LAN pregunta si va a una red local de la lista no-balancear: si sí, accept y sigue en la tabla main. Si no, PCC con both-addresses:2 la manda con resto 0 a la marca pcc-fija y la tabla por-fija por ether1, o con resto 1 a pcc-4g y la tabla por-4g por ether2. Una nota avisa que si el gateway de una tabla no responde, sus conexiones caen a main, que el chequeo mira solo el gateway y que FastTrack queda para lo no marcado.",
         "caption": "PCC reparte por par cliente servidor; lo local no se balancea y main queda de red de seguridad.", "after": "Balanceo PCC entre la fija y el 4G"},
    ],
    "concepts": [
        {"name": "El 4G detrás de NAT",
         "para_que": "El respaldo celular casi siempre entrega una IP privada (el router 4G hace NAT) o una de CGNAT del operador, en 100.64.0.0/10. Por ahí se puede salir a internet, pero nadie de afuera puede iniciar una conexión hacia adentro.",
         "como": "Se mira en /ip/dhcp-client/print detail y en /ip/cloud. Mientras el 4G está activo, lo publicado por la IP fija no se ve porque ese enlace está caído, y Back To Home sigue funcionando por el relay de MikroTik. Se avisa al cliente antes.",
         "ejemplo": "Una oficina con central de monitoreo: durante un corte de la fibra, la central deja de ver el NVR. El técnico lo dejó escrito en el acta, junto con la alternativa: el acceso del técnico por Back To Home sigue andando."},
        {"name": "Gateway del 4G fijo o que cambia",
         "para_que": "Las rutas que apuntan a un gateway necesitan que ese gateway no cambie. Un router 4G en modo router da siempre el mismo (192.168.8.1); uno en modo puente o un ISP por DHCP puede cambiarlo.",
         "como": "Con gateway estable, se usa como uno fijo, también para la tabla de PCC. Si cambia, la documentación del cliente DHCP trae un script de lease que crea o corrige la ruta con el gateway recibido y la borra al perder el lease.",
         "ejemplo": "Un local usa un ISP de cable por DHCP como respaldo y el gateway cambió tras un corte. La ruta de la tabla por-4g quedó apuntando al viejo; con el script de lease se corrige sola."},
        {"name": "Balanceo PCC",
         "para_que": "PCC reparte conexiones entre dos enlaces sin partir ninguna: cada conexión queda en un enlace. Con both-addresses, todo el tráfico entre un cliente y un mismo servidor va por el mismo enlace, lo que evita que una página de banco vea dos IP distintas.",
         "como": "Una tabla por enlace con su ruta por defecto y check-gateway, una lista de redes locales que no se balancean (accept primero), dos reglas PCC both-addresses:2/0 y 2/1 que marcan la conexión, y dos mark-routing hacia las tablas. Si una tabla pierde su gateway, sus conexiones caen a main y siguen el failover. FastTrack solo para lo no marcado. No sirve con Hotspot.",
         "ejemplo": "Un estudio contable con dos fibras de proveedores distintos activa PCC: las descargas pesadas se reparten y el sistema de facturación sigue entrando siempre por la misma IP al mismo servidor."},
    ],
    "teoria_md": """### Un poco de historia

Las redes celulares se quedaron sin direcciones IPv4 públicas mucho antes que las fijas. La respuesta fue el NAT de operador: el RFC 6598, de 2012, reservó el bloque 100.64.0.0/10 para que los proveedores numeren a sus clientes detrás de su propio NAT. Por eso un módem 4G de respaldo casi nunca recibe una IP alcanzable desde internet, y si el router 4G está en modo router, suma un segundo NAT propio.

El balanceo de carga en RouterOS se arma con piezas del firewall. La página de Load Balancing de MikroTik separa los métodos por paquete, que solo funcionan si controlás las dos puntas, de los métodos por conexión, que son los que sirven en un router con varias WAN. PCC (Per Connection Classifier) es el más usado de los segundos, y la documentación lo descarta para sitios con Hotspot.

El servicio IP Cloud de MikroTik resolvió otro problema: saber qué IP pública tiene un router detrás de NAT. El router le pregunta a la nube y la nube le contesta con la dirección desde la que recibió el pedido. Back To Home se apoya en eso y, cuando no hay IP alcanzable, usa un relay.

### Cómo funciona

El cliente DHCP del 4G instala su ruta con `default-route-distance=2` y espera mientras las recursivas de la fija estén activas. Cuando caen, el router sale por el 4G y la nube ve la IP pública del 4G: `public-address` cambia y el nombre `.sn.mynetname.net`, con TTL de 60 segundos, la sigue. Detrás de NAT, el router actualiza cada minuto.

PCC toma campos del encabezado (con `both-addresses`, las direcciones de origen y destino), calcula un hash y se queda con el resto de dividirlo por el denominador. Con `:2/0` y `:2/1`, cada conexión cae en uno de dos grupos de forma estable: el mismo par cliente servidor siempre da el mismo resto. Cada grupo recibe una marca de conexión, y cada marca, una marca de ruteo hacia su tabla.

Si la ruta de una tabla queda inactiva porque su gateway no responde, la búsqueda sigue en `main`, donde están las recursivas y el respaldo. Ese chequeo mira el gateway, no internet. Las conexiones marcadas no pueden usar FastTrack, que trabaja con `main`, así que la CPU trabaja más.
""",
    "script_rsc": SCRIPTS["39"],
}


def check_after(lid, entry):
    card = next(CLASS.glob(f"{lid}-*/card.md")).read_text(encoding="utf-8")
    lab = card.split("**Laboratorio**", 1)[1].split("**Regla para quedarse**", 1)[0]
    nocode = re.sub(r"```.*?```", "", lab, flags=re.S)
    for s in entry["steps"]:
        a = s["after"]
        assert 15 <= len(a) <= 40, (lid, a, len(a))
        assert nocode.count(a) == 1, (lid, a, nocode.count(a))
        line = next(l for l in nocode.splitlines() if a in l)
        assert line.startswith(f"{s['step']}."), (lid, a, line[:20])


def words(md):
    return len(re.sub(r"[#`*]", " ", md).split())


for lid, e in [("11", M11), ("37", M37), ("38", M38), ("39", M39)]:
    check_after(lid, e)
    w = words(e["teoria_md"])
    assert 250 <= w <= 450, (lid, w)
    assert "### Un poco de historia" in e["teoria_md"] and "### Cómo funciona" in e["teoria_md"]
    blob = json.dumps(e, ensure_ascii=False)
    assert "—" not in blob and "–" not in blob, lid
    assert not re.search(r"tenés que|debés|asegurate de|no te olvides", blob, re.I), lid
    n = e["script_rsc"]["codigo"].count("\n") + 1
    assert 15 <= n <= 60, (lid, n)
    names = set(re.findall(r"\{\{([A-Z0-9_]+)\}\}", e["script_rsc"]["codigo"]))
    declared = {v["nombre"] for v in e["script_rsc"]["variables"]}
    assert names == declared, (lid, names ^ declared)
    print(lid, "teoria", w, "palabras · script", n, "líneas · variables", len(names))

(OUT / "manifest-11b.json").write_text(json.dumps({"11": M11}, ensure_ascii=False, indent=2), encoding="utf-8")
(OUT / "manifest-37-39.json").write_text(json.dumps({"37": M37, "38": M38, "39": M39}, ensure_ascii=False, indent=2), encoding="utf-8")
print("ok")
