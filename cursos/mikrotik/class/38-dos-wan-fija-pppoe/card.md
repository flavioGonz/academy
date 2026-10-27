# Lección 38. Dos WAN: IP fija + PPPoE

**Escuchá:** dos-wan-fija-pppoe.mp3 (2 min)

**La idea, en tres líneas**
- Enlace dedicado con IP fija como principal, con rutas recursivas por su gateway, y PPPoE dinámico de respaldo con su ruta automática en distancia 2 (`default-route-distance=2`): el respaldo no necesita testigos porque solo trabaja cuando el principal cae.
- Lo que se publica (NVR, central de monitoreo, WinBox de soporte) entra por la IP fija: el dst-nat va atado a esa IP o a esa interfaz, nunca a toda la lista WAN.
- Si un día el PPPoE pasa a principal, o querés entrar por las dos, la respuesta tiene que salir por donde entró: tabla `por-fija`, marca de conexión para lo que entra por ether1 y marca de ruteo para sus respuestas desde la LAN y desde el router, fuera de FastTrack.

**Impacto:** el respaldo entra solo y los accesos publicados por la IP fija siguen andando aunque cambie qué enlace es el principal.

**Quién lo dice:** 3 de 3 fuentes sobre acceso entrante con dos WAN coinciden en marcar la conexión por la interfaz de entrada y rutear la respuesta por su tabla (documentación de PCC y dos hilos del foro); la documentación de Policy Routing ofrece `/routing/rule` como camino más simple y desaconseja mezclarlo con mangle. Si Antel entrega IP fija por PPPoE en algún plan: ninguna fuente leída lo confirma.

**Laboratorio** · Foco · 25 min
Banco: ether1 con IP fija de ejemplo 203.0.113.10/29 y gateway 203.0.113.9, ether2 a un servidor PPPoE (ONT en puente o un MikroTik de banco), notebook en ether3, un NVR o una PC de prueba en 192.168.88.20 con HTTPS. Desde afuera prueba una IP de ejemplo 198.51.100.50 (la central de monitoreo).
1. Export y Safe Mode. ether2 fuera del bridge, y la IP fija cargada como en la lección de IP fija:
```routeros
/interface/bridge/port/remove [find interface=ether2]
/ip/address/print where interface=ether1
```
2. Testigos y rutas por defecto recursivas por la IP fija, y apagá la ruta por defecto común:
```routeros
/ip/route/add dst-address=1.1.1.1/32 gateway=203.0.113.9 scope=10 comment="ies-testigo-fija-a"
/ip/route/add dst-address=9.9.9.9/32 gateway=203.0.113.9 scope=10 comment="ies-testigo-fija-b"
/ip/route/add gateway=1.1.1.1 target-scope=11 check-gateway=ping distance=1 comment="ies-default-fija-a"
/ip/route/add gateway=9.9.9.9 target-scope=11 check-gateway=ping distance=1 comment="ies-default-fija-b"
/ip/route/disable [find where static and dst-address=0.0.0.0/0 and gateway=203.0.113.9]
```
3. PPPoE de respaldo con su ruta en distancia 2 y sin sus DNS:
```routeros
/interface/pppoe-client/add name=pppoe-respaldo interface=ether2 user="cliente-ejemplo" password="Clave-De-Ejemplo-1" add-default-route=yes default-route-distance=2 use-peer-dns=no max-mtu=1492 max-mru=1492 disabled=no
/ip/route/print where dst-address=0.0.0.0/0
```
Esperado: las recursivas activas y la del PPPoE (distancia 2) en espera.
4. NAT, MSS y DNS:
```routeros
/interface/list/member/add list=WAN interface=pppoe-respaldo
/ip/firewall/mangle/add chain=forward out-interface=pppoe-respaldo protocol=tcp tcp-flags=syn action=change-mss new-mss=clamp-to-pmtu passthrough=yes comment="ies-mss-pppoe"
/ip/dns/set servers=1.0.0.1,8.8.4.4
```
5. El servicio publicado, solo por la IP fija y solo para la central:
```routeros
/ip/firewall/address-list/add list=monitoreo address=198.51.100.50
/ip/firewall/nat/add chain=dstnat in-interface=ether1 dst-address=203.0.113.10 protocol=tcp dst-port=8443 src-address-list=monitoreo action=dst-nat to-addresses=192.168.88.20 to-ports=443 comment="ies-nvr-fija"
```
6. Failover: descartá los pings del router a 1.1.1.1 y 9.9.9.9 por ether1 (como en la lección de dos WAN) y mirá que entre la ruta del PPPoE. Mientras dura, el NVR no se ve por la IP fija: es lo esperado, ese enlace está sin internet.
7. Al revés: el PPPoE pasa a principal y la IP fija sigue publicando. Subí la distancia de la fija y probá el NVR desde afuera (no abre: la respuesta sale por el PPPoE):
```routeros
/ip/route/set [find comment~"ies-default-fija"] distance=3
```
Ahora la marca, para que lo que entra por ether1 responda por ether1:
```routeros
/routing/table/add name=por-fija fib
/ip/route/add dst-address=0.0.0.0/0 gateway=203.0.113.9@main routing-table=por-fija comment="ies-tabla-fija"
/ip/firewall/mangle/add chain=prerouting in-interface=ether1 connection-state=new action=mark-connection new-connection-mark=entra-fija comment="ies-entra-fija"
/ip/firewall/mangle/add chain=prerouting in-interface-list=LAN connection-mark=entra-fija action=mark-routing new-routing-mark=por-fija comment="ies-entra-fija"
/ip/firewall/mangle/add chain=output connection-mark=entra-fija action=mark-routing new-routing-mark=por-fija comment="ies-entra-fija"
/ip/firewall/filter/set [find action=fasttrack-connection] connection-mark=no-mark
```
Probá de nuevo desde afuera: abre. Después volvé la distancia a 1 o, si el PPPoE queda de principal, armale las recursivas por la interfaz como en la lección de PPPoE + DHCP.
8. Verificá que las marcas cuentan:
```routeros
/ip/firewall/mangle/print stats where comment="ies-entra-fija"
/ip/firewall/connection/print where connection-mark=entra-fija
```

Errores típicos de esta combinación: el dst-nat con `in-interface-list=WAN` y sin `dst-address` (agarra por las dos WAN y responde por una sola); el PPPoE en distancia 1 junto con la fija (reparte tráfico); marcar ruteo en prerouting sin `in-interface-list=LAN` (las IP del router dejan de responder); la marca solo en prerouting, sin la de output (WinBox por la IP fija no responde); FastTrack sin `connection-mark=no-mark` (las respuestas marcadas se escapan por la tabla main).

⚠️ El paso 7 cambia qué enlace es el principal en vivo: en un sitio con clientes, ventana coordinada y Safe Mode.

**Regla para quedarse**
Lo publicado entra por la IP fija y sale por la IP fija, sea cual sea el principal.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Foro: PPPoE más IP fija, responder por la WAN por donde llegó el pedido: https://forum.mikrotik.com/t/failover-pppoe-static-with-dynamics-gateways/177576
- Foro: marca de conexión por interfaz de entrada y marca de ruteo para la respuesta: https://forum.mikrotik.com/t/what-is-the-right-way-to-do-port-forward-with-multiple-wans-and-lans/143684
- Tablas de ruteo, mangle o routing rules (documentación oficial): https://help.mikrotik.com/docs/spaces/ROS/pages/59965508/Policy+Routing
- Mangle, mark-routing y FastTrack: https://help.mikrotik.com/docs/spaces/ROS/pages/48660587/Mangle
- No marcar el tráfico local del router en RouterOS 7: https://help.mikrotik.com/docs/spaces/ROS/pages/30474256/Moving+from+ROSv6+to+v7+with+examples
