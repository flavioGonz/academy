# Lección 11. Dos WAN

**Escuchá:** dos-wan.mp3 (2 min)

**La idea, en tres líneas**
- Failover (una WAN trabaja, la otra espera) es lo que pide casi toda obra; balanceo con PCC reparte conexiones entre dos enlaces parecidos y suma marcas y tablas. Cada tipo de WAN pone su ruta por defecto distinto: la IP fija la escribís vos, el cliente DHCP la instala con `default-route-distance` y el PPPoE con `add-default-route` y `default-route-distance`.
- `distance` elige la ruta y `check-gateway=ping` solo mira el próximo salto: con el módem vivo e internet caída no conmuta. Por eso, rutas recursivas: dos hosts testigo por proveedor con /32 (`scope=10`) y las rutas por defecto apuntando al testigo (`target-scope=11`). Netwatch es la alternativa con scripts.
- Lo que se olvida: masquerade por las dos salidas, las conexiones viejas que quedan en conntrack al conmutar y volver, y lo que entra de afuera (port forwarding, WinBox, Back To Home), que responde por la ruta por defecto salvo que marques la conexión y la mandes por la WAN por donde entró.

**Impacto:** el local sigue cobrando cuando se cae la fibra, sabés cuánto tarda en conmutar y en volver, y los accesos publicados no se rompen por responder por el enlace equivocado.

**Quién lo dice:** 4 de 5 fuentes sobre failover coinciden en rutas recursivas con dos testigos (documentación de Failover, Routing Decision 7.25, MKController y el foro); MKController (vende una plataforma de gestión) las mide en 20 a 30 segundos y suma Netwatch; un hilo de 2015 (RouterOS 6) no logró la recursiva por la interfaz PPPoE, cosa que el foro en 2024 atribuye a la versión 6.

**Laboratorio** · Foco · 25 min
Banco: ether1 con IP fija de ejemplo 203.0.113.10/29 y gateway 203.0.113.9 (como en la lección de IP fija), ether2 a un router 4G en 192.168.8.1 con el MikroTik en 192.168.8.2/24 (fuera del bridge), notebook en ether3. Testigos: 1.1.1.1 y 9.9.9.9 por el ISP1, 8.8.8.8 y 208.67.222.222 por el ISP2. Si alguna WAN es PPPoE o DHCP, las lecciones que siguen traen la variante exacta.
1. Export (lección Backup primero) y Safe Mode. Mirá quién pone rutas por defecto y con qué distancia:
```routeros
/ip/route/print where dst-address=0.0.0.0/0
/ip/dhcp-client/print
/interface/pppoe-client/print
```
Un cliente DHCP o PPPoE con su ruta automática en distancia 1 compite con las tuyas: subile `default-route-distance` o ponele `add-default-route=no`.
2. Rutas a los testigos, cada una por su proveedor:
```routeros
/ip/route/add dst-address=1.1.1.1/32 gateway=203.0.113.9 scope=10 comment="ies-testigo-isp1-a"
/ip/route/add dst-address=9.9.9.9/32 gateway=203.0.113.9 scope=10 comment="ies-testigo-isp1-b"
/ip/route/add dst-address=8.8.8.8/32 gateway=192.168.8.1 scope=10 comment="ies-testigo-isp2-a"
/ip/route/add dst-address=208.67.222.222/32 gateway=192.168.8.1 scope=10 comment="ies-testigo-isp2-b"
```
3. Rutas por defecto recursivas, y apagá la ruta por defecto común que dejó la lección de IP fija:
```routeros
/ip/route/add gateway=1.1.1.1 target-scope=11 check-gateway=ping distance=1 comment="ies-default-isp1-a"
/ip/route/add gateway=9.9.9.9 target-scope=11 check-gateway=ping distance=1 comment="ies-default-isp1-b"
/ip/route/add gateway=8.8.8.8 target-scope=11 check-gateway=ping distance=2 comment="ies-default-isp2-a"
/ip/route/add gateway=208.67.222.222 target-scope=11 check-gateway=ping distance=2 comment="ies-default-isp2-b"
/ip/route/disable [find where static and dst-address=0.0.0.0/0 and gateway=203.0.113.9]
```
4. NAT y DNS. El masquerade de fábrica sale por `out-interface-list=WAN`: sumá ether2 a la lista. Los DNS del router, que no sean testigos:
```routeros
/interface/list/member/add list=WAN interface=ether2
/ip/firewall/nat/print where action=masquerade
/ip/dns/set servers=1.0.0.1,8.8.4.4
```
5. Simulá internet caída con el módem vivo: descartá los pings del router a los testigos del ISP1 y mirá la tabla.
```routeros
/ip/firewall/filter/add chain=output dst-address=1.1.1.1 protocol=icmp action=drop comment="lab corte isp1"
/ip/firewall/filter/add chain=output dst-address=9.9.9.9 protocol=icmp action=drop comment="lab corte isp1"
/ip/route/print where dst-address=0.0.0.0/0
```
Desde la notebook, `ping -t 1.0.0.1` y contá los pings perdidos hasta que las rutas del ISP1 quedan inactivas.
6. Volvé y contá de nuevo: `/ip/firewall/filter/remove [find comment="lab corte isp1"]`. Mirá las conexiones que quedaron armadas por el ISP2 (una llamada SIP, una VPN):
```routeros
/ip/firewall/connection/print where protocol=udp
```
Si algo quedó colgado, se puede borrar solo lo UDP: `/ip/firewall/connection/remove [find protocol=udp]` (⚠️ corta las llamadas en curso).
7. Si se publica algo por la WAN2 o entrás por ella con WinBox (con el 4G en IP privada, solo si el router 4G reenvía el puerto), que la respuesta salga por donde entró:
```routeros
/routing/table/add name=por-isp2 fib
/ip/route/add dst-address=0.0.0.0/0 gateway=192.168.8.1@main routing-table=por-isp2 comment="ies-tabla-isp2"
/ip/firewall/mangle/add chain=prerouting in-interface=ether2 connection-state=new action=mark-connection new-connection-mark=entra-isp2 comment="ies-entra-isp2"
/ip/firewall/mangle/add chain=prerouting in-interface-list=LAN connection-mark=entra-isp2 action=mark-routing new-routing-mark=por-isp2 comment="ies-entra-isp2"
/ip/firewall/mangle/add chain=output connection-mark=entra-isp2 action=mark-routing new-routing-mark=por-isp2 comment="ies-entra-isp2"
/ip/firewall/filter/set [find action=fasttrack-connection] connection-mark=no-mark
```
La última línea saca de FastTrack las conexiones marcadas: FastTrack solo usa la tabla main.
8. Prueba de campo, cuando haya ventana: cortá la fibra aguas arriba del módem (no el cable del router) y anotá en el legajo los pings perdidos al conmutar y al volver.

⚠️ Tocar rutas por defecto y mangle en un router remoto puede dejarte afuera: Safe Mode, export antes y un cambio por vez.

**Regla para quedarse**
Un failover que no probé cortando aguas arriba del módem, y volviendo, no existe.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Failover con rutas recursivas, scope y target-scope (documentación oficial): https://help.mikrotik.com/docs/spaces/ROS/pages/26476608/Failover+WAN+Backup
- check-gateway, distance, ECMP y los tiempos de prueba en RouterOS 7.25: https://manual.mikrotik.com/docs/7.25/user-guides/routing-and-networking-protocols/routing-decision
- Balanceo PCC con tablas, marcas y failover (documentación oficial): https://help.mikrotik.com/docs/spaces/ROS/pages/152600617/Per+connection+classifier
- Masquerade, conexiones que se borran y fuga de IPs privadas al volver: https://manual.mikrotik.com/docs/7.25/firewall-and-quality-of-service/firewall/nat
- Foro: el ping que no vuelve hasta borrar las conexiones, con PPPoE y LTE: https://forum.mikrotik.com/t/simple-failover-isp1-pppoe-isp2-lte/178550
- Foro: por qué el port forward por la segunda WAN responde por la primera: https://forum.mikrotik.com/t/what-is-the-right-way-to-do-port-forward-with-multiple-wans-and-lans/143684
