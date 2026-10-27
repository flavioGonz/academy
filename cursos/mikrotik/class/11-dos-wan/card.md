# Lección 11. Dos WAN

**Escuchá:** dos-wan.mp3 (2 min)

**La idea, en tres líneas**
- Rutas /32 a un host testigo por cada ISP, y rutas por defecto que apuntan al testigo con `check-gateway=ping` y distancias 1 y 2: así se detecta internet caída aunque el módem siga vivo.
- Dos testigos por enlace; el testigo del respaldo se alcanza por el respaldo.
- Las dos salidas en la lista WAN para que el masquerade cubra ambas.

**Impacto:** el local sigue cobrando cuando se cae la fibra y vos sabés cuánto tarda en conmutar.

**Quién lo dice:** 2 de 3 fuentes coinciden en rutas recursivas con check-gateway; MKController (que vende una plataforma de gestión) dice que conmutan en 20 a 30 segundos y sin ver pérdidas parciales, y suma Netwatch.

**Laboratorio** · Foco · 20 min
Ejemplo: ISP1 por ether1 con gateway 203.0.113.1; ISP2 (4G) por ether2 con gateway 192.168.8.1. Testigos 1.1.1.1 y 9.9.9.9 por ISP1, 8.8.8.8 y 208.67.222.222 por ISP2. Si los gateways son dinámicos (DHCP o PPPoE), hay que adaptar: las rutas recursivas necesitan gateways estables.
1. Antes de tocar rutas, export (lección 6) y Safe Mode (lección 1).
2. Rutas a los testigos, cada una por su ISP:
```routeros
/ip/route/add dst-address=1.1.1.1/32 gateway=203.0.113.1 scope=10 comment="testigo ISP1 a"
/ip/route/add dst-address=9.9.9.9/32 gateway=203.0.113.1 scope=10 comment="testigo ISP1 b"
/ip/route/add dst-address=8.8.8.8/32 gateway=192.168.8.1 scope=10 comment="testigo ISP2 a"
/ip/route/add dst-address=208.67.222.222/32 gateway=192.168.8.1 scope=10 comment="testigo ISP2 b"
```
3. Defaults recursivas:
```routeros
/ip/route/add dst-address=0.0.0.0/0 gateway=1.1.1.1 target-scope=11 check-gateway=ping distance=1
/ip/route/add dst-address=0.0.0.0/0 gateway=9.9.9.9 target-scope=11 check-gateway=ping distance=1
/ip/route/add dst-address=0.0.0.0/0 gateway=8.8.8.8 target-scope=11 check-gateway=ping distance=2
/ip/route/add dst-address=0.0.0.0/0 gateway=208.67.222.222 target-scope=11 check-gateway=ping distance=2
```
4. Segunda WAN en la lista (si usás el masquerade de la defconf, que sale por `out-interface-list=WAN`):
```routeros
/interface/list/member/add list=WAN interface=ether2
```
5. Desde una PC de la LAN dejá un ping continuo (`ping -t 1.0.0.1` en Windows) y cortá internet del ISP1 aguas arriba del módem. Mirá `/ip/route/print where dst-address=0.0.0.0/0` y contá cuántos pings se pierden hasta conmutar y al volver.

⚠️ Si los testigos son tus propios DNS, cuando cae ISP1 los equipos que los usan dejan de resolver por esa ruta: elegí testigos que no uses como DNS.

**Regla para quedarse**
Un failover que no probé desenchufando no existe.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Failover con rutas recursivas y check-gateway: https://help.mikrotik.com/docs/spaces/ROS/pages/26476608/Failover+WAN+Backup
- Tiempos de conmutación, Netwatch y prueba en campo: https://mkcontroller.com/blog/tutorials/mikrotik/mikrotik-dual-wan-failover-isp-guide/
- Masquerade, dos uplinks y fugas de IPs privadas: https://manual.mikrotik.com/docs/7.25/firewall-and-quality-of-service/firewall/nat
