# Lección 39. Dos WAN: IP fija + DHCP

**Escuchá:** dos-wan-fija-dhcp.mp3 (2 min)

**La idea, en tres líneas**
- IP fija como principal con rutas recursivas por su gateway, y un módem 4G/LTE o un ISP por DHCP de respaldo con `default-route-distance=2` y `use-peer-dns=no`. El respaldo celular casi siempre entrega IP privada o CGNAT: por ahí sale todo, pero no entra nada publicado, y Back To Home pasa a ir por el relay.
- Si el router 4G está en modo router, su gateway (192.168.8.1) no cambia y sirve igual que uno fijo; si el gateway cambia, el script de lease de la documentación del cliente DHCP mantiene la ruta al día.
- Variante opcional: balanceo PCC con dos tablas, `both-addresses` para que cada par cliente servidor quede en un enlace, y las rutas de main como failover. Solo si el segundo enlace no tiene tope de datos.

**Impacto:** el respaldo celular entra solo, sabés de antemano qué deja de funcionar mientras está activo (lo publicado) y no gastás el plan de datos del 4G repartiendo tráfico sin querer.

**Quién lo dice:** 3 de 3 fuentes coinciden en el respaldo DHCP con distancia mayor (documentación del cliente DHCP 7.25, página de Load Balancing y un hilo del foro con ISP y LTE por DHCP); para balancear, la documentación de PCC da la receta completa y avisa que no sirve con Hotspot; MKController (vende una plataforma de gestión) marca que failover no es balanceo y que el respaldo celular suele ir detrás de CGNAT.

**Laboratorio** · Foco · 20 min (+15 con PCC)
Banco: ether1 con IP fija de ejemplo 203.0.113.10/29 y gateway 203.0.113.9, ether2 a un router 4G que entrega DHCP con gateway 192.168.8.1, notebook en ether3.
1. Export y Safe Mode. ether2 fuera del bridge:
```routeros
/interface/bridge/port/remove [find interface=ether2]
```
2. Recursivas por la IP fija, como en la lección de IP fija + PPPoE:
```routeros
/ip/route/add dst-address=1.1.1.1/32 gateway=203.0.113.9 scope=10 comment="ies-testigo-fija-a"
/ip/route/add dst-address=9.9.9.9/32 gateway=203.0.113.9 scope=10 comment="ies-testigo-fija-b"
/ip/route/add gateway=1.1.1.1 target-scope=11 check-gateway=ping distance=1 comment="ies-default-fija-a"
/ip/route/add gateway=9.9.9.9 target-scope=11 check-gateway=ping distance=1 comment="ies-default-fija-b"
/ip/route/disable [find where static and dst-address=0.0.0.0/0 and gateway=203.0.113.9]
```
3. DHCP de respaldo y qué recibió:
```routeros
/ip/dhcp-client/add interface=ether2 add-default-route=yes default-route-distance=2 use-peer-dns=no use-peer-ntp=no disabled=no
/ip/dhcp-client/print detail where interface=ether2
```
`address` en 192.168.x es doble NAT (el 4G en modo router); en 100.64.0.0/10, CGNAT del operador. En los dos casos, nada publicado entra por el 4G.
4. NAT y DNS:
```routeros
/interface/list/member/add list=WAN interface=ether2
/ip/dns/set servers=1.0.0.1,8.8.4.4
/ip/route/print where dst-address=0.0.0.0/0
```
5. Failover: descartá los pings del router a 1.1.1.1 y 9.9.9.9 por ether1 (como en la lección de dos WAN), con `ping -t 1.0.0.1` desde la notebook. Mirá cómo cambia lo que ve la nube:
```routeros
/ip/cloud/force-update
/ip/cloud/print
```
`public-address` pasa a ser la del 4G; con Back To Home activo, `vpn-relay-ipv4-status` dice si los celulares entran directo o por el relay.
6. Volvé (sacá las reglas de descarte) y mirá lo que quedó armado por el 4G:
```routeros
/ip/firewall/connection/print where reply-dst-address~"^192.168.8."
```
7. (Opcional, +15 min) Balanceo PCC entre la fija y el 4G, adaptado del ejemplo oficial:
```routeros
/routing/table/add name=por-fija fib
/routing/table/add name=por-4g fib
/ip/route/add dst-address=0.0.0.0/0 gateway=203.0.113.9@main routing-table=por-fija check-gateway=ping comment="ies-pcc-fija"
/ip/route/add dst-address=0.0.0.0/0 gateway=192.168.8.1@main routing-table=por-4g check-gateway=ping comment="ies-pcc-4g"
/ip/firewall/address-list/add list=no-balancear address=192.168.88.0/24
/ip/firewall/address-list/add list=no-balancear address=192.168.8.0/24
/ip/firewall/address-list/add list=no-balancear address=203.0.113.8/29
/ip/firewall/mangle/add chain=prerouting in-interface-list=LAN dst-address-list=no-balancear action=accept comment="ies-pcc"
/ip/firewall/mangle/add chain=prerouting in-interface-list=LAN dst-address-type=!local connection-state=new connection-mark=no-mark per-connection-classifier=both-addresses:2/0 action=mark-connection new-connection-mark=pcc-fija comment="ies-pcc"
/ip/firewall/mangle/add chain=prerouting in-interface-list=LAN dst-address-type=!local connection-state=new connection-mark=no-mark per-connection-classifier=both-addresses:2/1 action=mark-connection new-connection-mark=pcc-4g comment="ies-pcc"
/ip/firewall/mangle/add chain=prerouting in-interface-list=LAN connection-mark=pcc-fija action=mark-routing new-routing-mark=por-fija comment="ies-pcc"
/ip/firewall/mangle/add chain=prerouting in-interface-list=LAN connection-mark=pcc-4g action=mark-routing new-routing-mark=por-4g comment="ies-pcc"
/ip/firewall/filter/set [find action=fasttrack-connection] connection-mark=no-mark
```
Abrí varias páginas desde la notebook y contá:
```routeros
/ip/firewall/connection/print count-only where connection-mark=pcc-fija
/ip/firewall/connection/print count-only where connection-mark=pcc-4g
```
Si una tabla pierde su gateway, sus conexiones caen a main y siguen el failover. Ojo: el chequeo de cada tabla mira solo el gateway, no internet. Para deshacer: `/ip/firewall/mangle/remove [find comment="ies-pcc"]`.

Errores típicos de esta combinación: el DHCP en distancia 1 (balanceo sin control, por ECMP); `use-peer-dns=yes` en el 4G; prometer acceso remoto por el 4G con IP privada o CGNAT; PCC con un 4G de datos limitados; PCC sin la lista `no-balancear` (el tráfico a redes locales sale a internet); PCC en un sitio con Hotspot, que la documentación descarta.

⚠️ Sin FastTrack para las conexiones marcadas, la CPU de un router chico sube: medila con el balanceo andando antes de dejarlo en un cliente.

**Regla para quedarse**
El 4G de respaldo espera en distancia 2 y sin sus DNS; balanceo solo con enlaces sin tope y con la lista de lo que no se balancea.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Cliente DHCP 7.25: distancia, ECMP y el script de lease para gateways que cambian: https://manual.mikrotik.com/docs/7.25/network-management/dhcp/client/
- Balanceo PCC con tablas, marcas y failover (documentación oficial): https://help.mikrotik.com/docs/spaces/ROS/pages/152600617/Per+connection+classifier
- Por conexión o por paquete, y el failover simple (documentación oficial): https://help.mikrotik.com/docs/spaces/ROS/pages/4390920/Load+Balancing
- Foro: ISP y LTE por DHCP, testigo con blackhole y conexiones a limpiar: https://forum.mikrotik.com/t/automated-wan-failover-using-2-dhcp-wan-connections/161606
- public-address, relay y Back To Home: https://manual.mikrotik.com/docs/7.25/network-management/cloud/back-to-home/
