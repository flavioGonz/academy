# Lección 26. Asignar IP

**Escuchá:** asignar-ip.mp3 (2 min)

**La idea, en tres líneas**
- `/ip/address/add address=10.10.20.1/24 interface=...`: dirección con máscara e interfaz. RouterOS calcula la red y el broadcast, y crea solo la ruta conectada (`DAc` en `/ip/route`).
- Una interfaz puede tener varias IP: sirve para una migración o para llegar a un equipo que viene de fábrica en otra red. La IP va en el bridge o en una interfaz VLAN, nunca en un puerto que está dentro del bridge.
- Un servidor DHCP son cuatro piezas: la IP en la interfaz, un pool que no incluye la IP del router, la red con gateway y DNS (`/ip/dhcp-server/network`) y el servidor que une interfaz y pool. `/ip/dhcp-server/setup` las arma en un paso.

**Impacto:** cada red del sitio queda con su gateway, su DHCP y sus reservas, y sabés leer por qué un equipo no toma dirección.

**Quién lo dice:** 4 de 4 fuentes oficiales coinciden (IP Addressing, Networking Fundamentals, DHCP Server y la guía de configuración manual de RouterOS 7.25); no hay discrepancias, solo matices: la documentación de DHCP advierte que el servidor no funciona en un bridge sin puertos y que guarda los leases en disco cada 5 minutos.

**Laboratorio** · Rápido · 15 min
En un hAP o hEX de banco con RouterOS 7 y la configuración por defecto, la notebook en ether2:
1. Leé lo que hay:
```routeros
/ip/address/print detail
/ip/route/print where connect
```
192.168.88.1/24 en `bridge`, con `network=192.168.88.0`, y su ruta conectada `DAc 192.168.88.0/24 bridge`.
2. Segunda IP en la misma interfaz, para llegar a un equipo que viene de fábrica en otra red (ejemplo: 192.168.1.0/24):
```routeros
/ip/address/add address=192.168.1.254/24 interface=bridge comment="lab temporal"
/ip/route/print where connect
```
Aparece una segunda ruta conectada. Cuando terminás con ese equipo, la sacás:
```routeros
/ip/address/remove [find comment="lab temporal"]
```
3. Una red nueva para cámaras en ether5. Sacalo del bridge, dale su IP y sumalo a la lista LAN, así el router le contesta DNS y WinBox:
```routeros
/interface/bridge/port/remove [find interface=ether5]
/ip/address/add address=10.10.20.1/24 interface=ether5 comment="CCTV"
/interface/list/member/add list=LAN interface=ether5
```
4. El servidor DHCP, pieza por pieza (o `/ip/dhcp-server/setup` y Enter a cada pregunta). El pool deja del .2 al .99 para IP fijas:
```routeros
/ip/pool/add name=pool-cctv ranges=10.10.20.100-10.10.20.199
/ip/dhcp-server/network/add address=10.10.20.0/24 gateway=10.10.20.1 dns-server=10.10.20.1
/ip/dhcp-server/add name=dhcp-cctv interface=ether5 address-pool=pool-cctv disabled=no
```
5. Conectá una cámara o la notebook en DHCP a ether5 y mirá el lease. Si es un equipo que siempre tiene que tener la misma IP, hacelo reserva:
```routeros
/ip/dhcp-server/lease/print where server=dhcp-cctv
/ip/dhcp-server/lease/make-static [find address=10.10.20.100]
```
6. Para dejar el banco como estaba: borrá servidor, red, pool, la IP y el miembro de la lista, y devolvé ether5 al bridge con `/interface/bridge/port/add bridge=bridge interface=ether5`.

⚠️ Un servidor DHCP en una red donde ya hay otro (el módem del cliente, un NVR con DHCP prendido) reparte direcciones que pelean entre sí. Antes de habilitarlo, fijate que la red sea tuya.

**Regla para quedarse**
La IP va en el bridge o en la VLAN; el pool, sin la IP del router y con lugar para las fijas.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- IP Addressing: máscara, varias IP por interfaz y la marca slave: https://help.mikrotik.com/docs/spaces/ROS/pages/328247/IP+Addressing
- DHCP Server en RouterOS 7.25: las cuatro piezas, setup, leases y reservas: https://manual.mikrotik.com/docs/7.25/network-management/dhcp/server
- Fundamentos de red: máscara, enlaces /31 y /32, y ARP: https://manual.mikrotik.com/docs/7.25/getting-started/networking-fundamentals/
- Configuración manual sin la configuración por defecto: bridge, IP y DHCP: https://manual.mikrotik.com/docs/7.25/getting-started/manual-network-setup
