# Lección 37. Dos WAN: PPPoE + DHCP

**Escuchá:** dos-wan-pppoe-dhcp.mp3 (2 min)

**La idea, en tres líneas**
- Fibra de Antel por PPPoE como principal, sin ruta automática (`add-default-route=no`), y rutas recursivas con los testigos por la interfaz `pppoe-antel`: en RouterOS 7 el nombre de la interfaz sirve de gateway aunque la IP del otro extremo cambie en cada reconexión.
- El respaldo por DHCP (router 4G o cablemódem de otro proveedor) trae su propia ruta por defecto, sus DNS y a veces doble NAT: `default-route-distance=2`, `use-peer-dns=no` y DNS fijos en el router que no sean testigos.
- Dos cortes distintos para probar: la sesión PPPoE que se cae (el masquerade limpia esas conexiones solo) y el PPPoE arriba sin internet (solo lo ven las recursivas). Al volver, lo que se armó por el 4G puede quedar colgado.

**Impacto:** el cliente con fibra de Antel y un 4G de respaldo no se entera del corte, y vos no tenés la ruta del 4G repartiendo tráfico ni DNS que dejan de resolver en pleno failover.

**Quién lo dice:** 3 de 4 fuentes coinciden en recursivas con la interfaz PPPoE de gateway y respaldo con distancia mayor (documentación de Failover y dos hilos del foro de 2024); un hilo de 2015, con RouterOS 6, no logró resolver la recursiva por la interfaz PPPoE. VLAN y MTU propios de Antel: ninguna fuente leída los confirma.

**Laboratorio** · Campo · 25 min
Banco: ether1 al ONT de Antel en modo puente (o a un MikroTik de banco con servidor PPPoE), ether2 a un router 4G que entrega DHCP con gateway 192.168.8.1, notebook en ether3. Usuario y clave de ejemplo: `cliente-ejemplo` y `Clave-De-Ejemplo-1`.
1. Export y Safe Mode. Apagá el cliente DHCP de fábrica en ether1 y sacá ether2 del bridge (si entrás por ether2, te cortás: entrá por ether3):
```routeros
/ip/dhcp-client/disable [find interface=ether1]
/interface/bridge/port/remove [find interface=ether2]
```
2. PPPoE principal, sin ruta ni DNS automáticos:
```routeros
/interface/pppoe-client/add name=pppoe-antel interface=ether1 user="cliente-ejemplo" password="Clave-De-Ejemplo-1" add-default-route=no use-peer-dns=no max-mtu=1492 max-mru=1492 disabled=no
/interface/pppoe-client/monitor pppoe-antel once
```
Si no conecta, buscá el concentrador con `/interface/pppoe-client/scan interface=ether1` y confirmá con Antel si hace falta VLAN, como en la lección de PPPoE con Antel.
3. DHCP de respaldo con distancia 2 y sin DNS del 4G:
```routeros
/ip/dhcp-client/add interface=ether2 add-default-route=yes default-route-distance=2 use-peer-dns=no use-peer-ntp=no disabled=no
/ip/dhcp-client/print detail where interface=ether2
```
Mirá `status=bound`, `gateway` y `address`: si es 192.168.x o 100.64.x, por el 4G no entra nada de afuera.
4. Testigos por la interfaz PPPoE y rutas por defecto recursivas:
```routeros
/ip/route/add dst-address=1.1.1.1/32 gateway=pppoe-antel scope=10 comment="ies-testigo-pppoe-a"
/ip/route/add dst-address=9.9.9.9/32 gateway=pppoe-antel scope=10 comment="ies-testigo-pppoe-b"
/ip/route/add gateway=1.1.1.1 target-scope=11 check-gateway=ping distance=1 comment="ies-default-pppoe-a"
/ip/route/add gateway=9.9.9.9 target-scope=11 check-gateway=ping distance=1 comment="ies-default-pppoe-b"
/ip/route/print where dst-address=0.0.0.0/0
```
Esperado: las dos recursivas activas y la del DHCP, con distancia 2, en espera.
5. NAT, MSS y DNS:
```routeros
/interface/list/member/add list=WAN interface=pppoe-antel
/interface/list/member/add list=WAN interface=ether2
/ip/firewall/mangle/add chain=forward out-interface=pppoe-antel protocol=tcp tcp-flags=syn action=change-mss new-mss=clamp-to-pmtu passthrough=yes comment="ies-mss-pppoe"
/ip/dns/set servers=1.0.0.1,8.8.4.4
```
6. Corte 1, la sesión se cae: con `ping -t 1.0.0.1` desde la notebook, `/interface/pppoe-client/disable pppoe-antel`. Contá pings perdidos, mirá la tabla y volvé con `enable`.
7. Corte 2, PPPoE arriba sin internet: descartá los pings del router a los testigos y mirá que conmute; después sacá las reglas y mirá que vuelva.
```routeros
/ip/firewall/address-list/add list=testigos-lab address=1.1.1.1
/ip/firewall/address-list/add list=testigos-lab address=9.9.9.9
/ip/firewall/filter/add chain=output out-interface=pppoe-antel protocol=icmp dst-address-list=testigos-lab action=drop comment="lab corte"
/ip/route/print where dst-address=0.0.0.0/0
```
Para volver, y ver lo que quedó armado por el 4G:
```routeros
/ip/firewall/filter/remove [find comment="lab corte"]
/ip/firewall/connection/print where reply-dst-address~"^192.168.8."
```
8. (Opcional) Netwatch que limpia las conexiones UDP cuando el testigo vuelve, con una blackhole para que el testigo no se alcance por el 4G:
```routeros
/ip/route/add dst-address=9.9.9.9/32 blackhole distance=20 comment="ies-testigo-pppoe-bh"
/tool/netwatch/add host=9.9.9.9 type=simple interval=10s up-script="/ip/firewall/connection/remove [find protocol=udp]" comment="ies-limpia-udp"
```

Errores típicos de esta combinación: dejar el PPPoE con `add-default-route=yes` en distancia 1 (esa ruta queda activa aunque no haya internet y el failover nunca ocurre); el DHCP del 4G en distancia 1 (reparte tráfico); ether2 todavía en el bridge (el DHCP del 4G termina repartiendo IP a la LAN); ether1 en la lista WAN y `pppoe-antel` no; probar solo desenchufando ether1, que no prueba las recursivas.

⚠️ Al pasar el ONT a puente, el sitio queda sin internet hasta que el MikroTik marque: ventana coordinada con el cliente. El paso 8 borra las conexiones UDP, incluidas las llamadas en curso.

**Regla para quedarse**
PPPoE principal sin ruta automática, testigos por la interfaz PPPoE, DHCP de respaldo en distancia 2 y sin sus DNS, y dos cortes probados.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Foro: PPPoE y LTE, testigo por pppoe-out1, blackhole y conexiones colgadas al volver: https://forum.mikrotik.com/t/simple-failover-isp1-pppoe-isp2-lte/178550
- Foro: en RouterOS 7 la interfaz PPPoE sirve de gateway en la recursiva: https://forum.mikrotik.com/t/failover-pppoe-static-with-dynamics-gateways/177576
- Propiedades del cliente PPPoE, add-default-route y default-route-distance: https://help.mikrotik.com/docs/spaces/ROS/pages/2031625/PPPoE
- Cliente DHCP 7.25, default-route-distance, ECMP y check-gateway: https://manual.mikrotik.com/docs/7.25/network-management/dhcp/client/
- Failover con rutas recursivas (documentación oficial): https://help.mikrotik.com/docs/spaces/ROS/pages/26476608/Failover+WAN+Backup
