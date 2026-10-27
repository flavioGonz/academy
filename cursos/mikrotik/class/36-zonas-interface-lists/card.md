# Lección 36. Zonas con listas

**Escuchá:** zonas-interface-lists.mp3 (2 min)

**La idea, en tres líneas**
- Una zona es una interface list: las interfaces ruteadas (VLAN, bridge, puerto suelto, PPPoE, túnel) que tienen el mismo nivel de confianza. La configuración por defecto ya trae dos, LAN y WAN; para un edificio se suman GESTION, ADMIN, CCTV, ACCESOS, INVITADOS y VPN.
- El firewall se escribe como una matriz "de → a": en forward, una regla por par de zonas permitido con `in-interface-list` y `out-interface-list`; en input, qué servicios del router ve cada zona; y al final, un drop. Lo que no está en la matriz no pasa.
- Una VLAN nueva entra a su lista y hereda la política sin tocar una regla. `include` suma listas enteras (SISTEMAS = CCTV + ACCESOS); `exclude` resta. Lo que comparte la misma red del bridge no pasa por forward: la zona separa redes, no equipos.

**Impacto:** el firewall de un edificio se lee como una tabla, se audita en cinco minutos y sumar la VLAN de cámaras del tercer piso es una línea.

**Quién lo dice:** 5 de 6 fuentes coinciden en agrupar interfaces en zonas y escribir las reglas entre zonas (la documentación de Interface Lists, un artículo de 2024 sobre firewall por zonas en MikroTik, dos hilos del foro, y las zonas de Fortinet y Cisco). En el debate del foro de septiembre de 2026, un veterano discrepa: partir de la configuración por defecto y no armar "grupos y subgrupos"; otro prefiere listas anidadas pero se queja de que WinBox no muestra los miembros que entran por `include`.

**Laboratorio** · Foco · 25 min
El edificio de ejemplo, en un hAP o hEX de banco con RouterOS 7 y configuración por defecto. En obra cada zona es una VLAN (lección VLAN por sistema); en el banco usamos puertos sueltos, y las reglas son exactamente las mismas: eso es lo que se aprende acá. Notebook en ether2 (GESTION), ether1 a la red de la oficina como WAN.
La matriz que vamos a escribir:
```text
de \ a      WAN     GESTION  ADMIN  CCTV              ACCESOS  INVITADOS  ROUTER (input)
GESTION+VPN sí      .        sí     sí                sí       sí         todo
ADMIN       sí      no       .      solo NVR 80,443,  no       no         DNS, DHCP
                                    8000
CCTV        NTP     no       no     .                 no       no         DNS, DHCP
ACCESOS     NTP     no       no     no                .        no         DNS, DHCP
INVITADOS   sí      no       no     no                no       .          DNS, DHCP
WAN         .       solo lo publicado con dst-nat (lección de port forwarding)   túnel UDP 13231
```
1. Safe Mode (Ctrl+X) y export. Armá las redes del banco: ether3, ether4 y ether5 fuera del bridge, con su IP, y un túnel WireGuard vacío para la zona VPN:
```routeros
/export file=antes-zonas
/interface/bridge/port/remove [find interface=ether3]
/interface/bridge/port/remove [find interface=ether4]
/interface/bridge/port/remove [find interface=ether5]
/ip/address/add address=10.10.20.1/24 interface=ether3 comment="lab: zona CCTV"
/ip/address/add address=10.10.30.1/24 interface=ether4 comment="lab: zona ACCESOS"
/ip/address/add address=10.10.40.1/24 interface=ether5 comment="lab: zona INVITADOS"
/interface/wireguard/add name=wg-gestion listen-port=13231 comment="lab: zona VPN"
```
2. Creá las zonas y sus miembros. Una interfaz va en una sola zona; las listas compuestas se arman con `include` y no llevan miembros propios:
```routeros
/interface/list/add name=VPN comment="lab: zona tuneles de tecnicos"
/interface/list/add name=GESTION include=VPN comment="lab: zona tecnicos, switches, APs"
/interface/list/add name=ADMIN comment="lab: zona PCs de administracion"
/interface/list/add name=CCTV comment="lab: zona camaras y NVR"
/interface/list/add name=ACCESOS comment="lab: zona control de acceso"
/interface/list/add name=INVITADOS comment="lab: zona WiFi de invitados"
/interface/list/add name=SISTEMAS include=CCTV,ACCESOS comment="lab: compuesta"
/interface/list/add name=CLIENTES include=ADMIN,CCTV,ACCESOS,INVITADOS comment="lab: compuesta"
/interface/list/member/add list=GESTION interface=bridge comment="lab:"
/interface/list/member/add list=CCTV interface=ether3 comment="lab:"
/interface/list/member/add list=ACCESOS interface=ether4 comment="lab:"
/interface/list/member/add list=INVITADOS interface=ether5 comment="lab:"
/interface/list/member/add list=VPN interface=wg-gestion comment="lab:"
/interface/list/member/print
```
En WinBox: Interfaces, pestaña Interface List; el botón Lists crea las listas (Include y Exclude están en la ventana de cada lista) y `+` agrega miembros. El print muestra solo los miembros estáticos: lo que entra por `include` no aparece ahí. ADMIN queda vacía a propósito (paso 6). Primero se suman los `include`, después se restan los `exclude` y al final se agregan los miembros estáticos.
3. Input por zona: GESTION ve todo el router; las demás zonas, DNS y DHCP; desde WAN, solo el puerto del túnel. Van arriba del drop de la configuración por defecto, que ya descarta lo que no viene de LAN (las zonas nuevas no están en LAN):
```routeros
/ip/firewall/filter/add chain=input in-interface-list=GESTION action=accept comment="lab: zona GESTION al router" place-before=[find comment="defconf: drop all not coming from LAN"]
/ip/firewall/filter/add chain=input in-interface-list=CLIENTES protocol=udp dst-port=53,67 action=accept comment="lab: zonas DNS y DHCP" place-before=[find comment="defconf: drop all not coming from LAN"]
/ip/firewall/filter/add chain=input in-interface-list=CLIENTES protocol=tcp dst-port=53 action=accept comment="lab: zonas DNS tcp" place-before=[find comment="defconf: drop all not coming from LAN"]
/ip/firewall/filter/add chain=input in-interface-list=WAN protocol=udp dst-port=13231 action=accept comment="lab: WAN al tunel de gestion" place-before=[find comment="defconf: drop all not coming from LAN"]
```
4. Forward por par de zonas, en el orden de la matriz, y el drop final. Con `add` común quedan al final de forward, debajo de las reglas de la configuración por defecto, que es donde van:
```routeros
/ip/firewall/filter/add chain=forward in-interface-list=GESTION action=accept comment="lab: GESTION a todas"
/ip/firewall/filter/add chain=forward in-interface-list=ADMIN out-interface-list=WAN action=accept comment="lab: ADMIN a WAN"
/ip/firewall/filter/add chain=forward in-interface-list=INVITADOS out-interface-list=WAN action=accept comment="lab: INVITADOS a WAN"
/ip/firewall/filter/add chain=forward in-interface-list=ADMIN out-interface-list=CCTV dst-address=10.10.20.50 protocol=tcp dst-port=80,443,8000 action=accept comment="lab: ADMIN al NVR"
/ip/firewall/filter/add chain=forward in-interface-list=SISTEMAS out-interface-list=WAN protocol=udp dst-port=123 action=accept comment="lab: SISTEMAS a NTP"
/ip/firewall/filter/add chain=forward in-interface-list=WAN connection-nat-state=dstnat action=accept comment="lab: WAN a lo publicado"
/ip/firewall/filter/add chain=forward action=drop log=yes log-prefix="ZONA-DROP" comment="lab: drop final entre zonas"
```
Sin la regla de lo publicado, el drop final se come los port forwarding: le pasó a un usuario del foro hasta que sumó `connection-nat-state=dstnat`.
5. Probá la matriz. Notebook en ether3 con 10.10.20.50/24, puerta de enlace 10.10.20.1 y DNS 10.10.20.1, como si fuera el NVR: el ping a 10.10.20.1 contesta (ICMP de la configuración por defecto), una página web no abre, WinBox a 10.10.20.1 no entra. Pasala a ether5 con 10.10.40.10/24, puerta de enlace y DNS 10.10.40.1 (invitados): navega, WinBox a 10.10.40.1 no entra y un ping a 10.10.20.50 (la red de cámaras) no sale y aparece en el log. Mirá quién suma:
```routeros
/ip/firewall/filter/print stats where comment~"^lab:"
/log/print where message~"ZONA-DROP"
```
6. Una red nueva, sin tocar reglas. Creá la VLAN de administración y metela en su zona: desde ese momento tiene internet, DNS y el NVR, y nada más.
```routeros
/interface/vlan/add name=vlan10-admin interface=bridge vlan-id=10 comment="lab:"
/ip/address/add address=10.10.10.1/24 interface=vlan10-admin comment="lab: zona ADMIN"
/interface/list/member/add list=ADMIN interface=vlan10-admin comment="lab:"
```
Lo mismo con cualquier interfaz: si la WAN pasa a PPPoE, `pppoe-out1` va a la lista WAN o las reglas de WAN no la ven; los túneles L2TP o SSTP de servidor son dinámicos y entran desde el perfil, con `/ppp/profile/set [find name=tecnicos] interface-list=VPN` (perfil de ejemplo).
7. En obra, el mismo firewall con VLANs. Cambian solo los miembros:
```routeros
/interface/list/member/add list=GESTION interface=vlan99-gestion
/interface/list/member/add list=ADMIN interface=vlan10-admin
/interface/list/member/add list=CCTV interface=vlan20-cctv
/interface/list/member/add list=ACCESOS interface=vlan30-accesos
/interface/list/member/add list=INVITADOS interface=vlan40-invitados
/interface/list/member/add list=VPN interface=wg-gestion
```
Ahí conviene que la lista LAN de fábrica sea la de gestión, así MAC server y descubrimiento (lección de cerrar puertas) quedan solo para los técnicos: `/interface/list/set LAN include=GESTION` y después se saca el miembro suelto que tenía. Dos VLAN de la misma zona (CCTV de dos edificios) no se hablan con el drop final: si querés, `in-interface-list=CCTV out-interface-list=CCTV action=accept`.
8. Para volver el banco a como estaba:
```routeros
/ip/firewall/filter/remove [find comment~"^lab:"]
/interface/list/member/remove [find comment~"^lab:"]
/interface/list/remove [find comment~"^lab:"]
/ip/address/remove [find comment~"^lab:"]
/interface/vlan/remove [find comment~"^lab:"]
/interface/wireguard/remove [find comment~"^lab:"]
/interface/bridge/port/add bridge=bridge interface=ether3
/interface/bridge/port/add bridge=bridge interface=ether4
/interface/bridge/port/add bridge=bridge interface=ether5
```

⚠️ El drop final corta el forward de toda red que no esté en una zona. En un sitio en producción, primero la regla con `action=log` unos días, mirás el log y recién después la pasás a drop. Siempre en Safe Mode y con un acceso de rescate.

**Regla para quedarse**
Primero la matriz en papel, después una lista por zona y una regla por casillero; lo nuevo se suma a la lista, no al firewall.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Interface lists: include, exclude, orden y el cuidado con los bridges: https://help.mikrotik.com/docs/spaces/ROS/pages/47579180/Interface+Lists
- Firewall por zonas en MikroTik, con una cadena por par de zonas: https://www.h-schmidt.net/articles/zone-based-firewalling-on-mikrotik-routers.html
- Una regla por par de VLAN o una lista: el hilo de 2018 que lo prueba en un CCR: https://forum.mikrotik.com/t/comfortable-way-to-block-inter-vlan-traffic/117490
- El debate de 2026: listas anidadas o una regla por servicio: https://forum.mikrotik.com/t/firewall-rules-and-interface-lists-best-practice/273047
- Las listas WAN y LAN en el firewall avanzado de MikroTik: https://help.mikrotik.com/docs/spaces/ROS/pages/328513/Building+Advanced+Firewall
- Zonas en Cisco IOS: zone-pair y self zone: https://grumpy-networkers-journal.readthedocs.io/en/latest/VENDOR/CISCO/FIREWALL/IOS/ZBFW.html
