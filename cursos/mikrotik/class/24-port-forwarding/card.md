# Lección 24. Port forwarding

**Escuchá:** port-forwarding.mp3 (2 min)

**La idea, en tres líneas**
- En RouterOS 7 un port forwarding es una regla `chain=dstnat action=dst-nat` que cambia el destino (`to-addresses`) y, si querés, el puerto (`to-ports`): afuera 18000, adentro 8000. El firewall por defecto ya deja pasar en forward lo que fue dst-nateado (`connection-nat-state=dstnat`).
- La regla se ata a la entrada (`in-interface-list=WAN`, o `dst-address=` con la IP pública si es fija) y al origen (`src-address-list`). Con solo `dst-port`, también agarra a las PC de la LAN que salen a ese puerto de cualquier servidor de internet.
- Puertos de fábrica: Hikvision 8000 (iVMS-4200 y la app), 554 o 10554 RTSP, 80 y 443 web; Dahua 37777 TCP (SmartPSS y DMSS), 37778 UDP, 554, 80 y 443. Si la IP del WAN es privada hay doble NAT; si está en 100.64.0.0/10, CGNAT y no hay port forwarding posible.

**Impacto:** publicás un NVR con reglas que entendés, lo probás desde afuera con números en los contadores y en cinco minutos sabés si el problema está en el MikroTik, en el módem del proveedor o en el CGNAT.

**Quién lo dice:** 5 de 6 fuentes de MikroTik y del foro coinciden en atar el dst-nat a la WAN o a la IP pública y filtrar el origen; el ejemplo de primera configuración de MikroTik publica con solo protocolo y puerto. En puertos, el aviso de Dahua dice que suele alcanzar con HTTP y 37777, y un integrador del foro tuvo que sumar 554 y 37778 UDP para ver video.

**Laboratorio** · Campo · 20 min
Escenario de ejemplo (rangos de documentación): MikroTik con RouterOS 7 y configuración por defecto, `ether1` en la lista WAN con la IP pública 203.0.113.10, LAN 192.168.88.0/24 en `bridge`, NVR Hikvision de banco en 192.168.88.50 con 8000 y 554. Sin NVR sirve una PC con un servicio escuchando en esos puertos. Con un NVR real, usá sus puertos:
```text
Marca      Puerto      Para qué                                  ¿Se publica?
Hikvision  8000 TCP    servidor (SDK): iVMS-4200 y la app        sí, si la app entra por IP
Hikvision  554 TCP     RTSP (VLC, VMS de terceros); 10554 en     solo si hace falta RTSP
                       firmware nuevo o si la operadora móvil
                       bloquea el 554
Hikvision  80 / 443    web del equipo                            mejor no: para la web, VPN
Dahua      37777 TCP   SmartPSS y DMSS: login, vivo, grabaciones sí, si la app entra por IP
Dahua      37778 UDP   UDP del equipo (lo lista el aviso oficial) si la app no muestra video
Dahua      554 TCP     RTSP                                      solo si hace falta RTSP
Dahua      80 / 443    web del equipo                            mejor no: para la web, VPN
```
Los puertos se cambian en la web del NVR (sección de red) o, en Hikvision, también con SADP.

1. Antes de tocar: export (lección 6), Safe Mode (lección 23) y la prueba de la lección 9, con DDNS activo:
```routeros
/export file=antes-port-forwarding
/ip/address/print where interface=ether1
/ip/cloud/print
```
```text
IP del WAN = public-address              -> IP pública directa: seguí
IP del WAN privada (192.168.x, 10.x)     -> doble NAT: módem u ONT en bridge (lección 15), o reenvío también en el módem hacia la IP WAN del MikroTik
IP del WAN en 100.64.0.0/10              -> CGNAT: no hay port forwarding; Back To Home (lección 19), concentrador (lección 20) o IP pública del proveedor
```
2. Lista de orígenes permitidos (IPs de ejemplo):
```routeros
/ip/firewall/address-list/add list=nvr-permitidos address=198.51.100.20 comment="oficina IES ejemplo, revisar 2027-04"
/ip/firewall/address-list/add list=nvr-permitidos address=203.0.113.25 comment="central monitoreo ejemplo, revisar 2027-04"
```
Si la oficina tiene IP dinámica, la lista acepta un nombre DDNS (por ejemplo el `<serie>.sn.mynetname.net` de su MikroTik) y el router lo resuelve.
3. Las dos reglas, con puerto externo distinto del interno:
```routeros
/ip/firewall/nat/add chain=dstnat in-interface-list=WAN src-address-list=nvr-permitidos protocol=tcp dst-port=18000 action=dst-nat to-addresses=192.168.88.50 to-ports=8000 comment="NVR1 SDK 18000>8000"
/ip/firewall/nat/add chain=dstnat in-interface-list=WAN src-address-list=nvr-permitidos protocol=tcp dst-port=18554 action=dst-nat to-addresses=192.168.88.50 to-ports=554 comment="NVR1 RTSP 18554>554"
```
Un segundo NVR detrás de la misma IP pública usa otro puerto externo hacia su propia IP:
```routeros
/ip/firewall/nat/add chain=dstnat in-interface-list=WAN src-address-list=nvr-permitidos protocol=tcp dst-port=18001 action=dst-nat to-addresses=192.168.88.51 to-ports=8000 comment="NVR2 SDK 18001>8000"
```
En la app, cada NVR se carga con la IP pública (o el nombre DDNS) y su puerto externo.
4. Forward: con la configuración por defecto no hace falta ninguna regla nueva. Comprobá que está la que deja pasar lo dst-nateado:
```routeros
/ip/firewall/filter/print where comment~"not DSTNATed"
```
Si tu firewall termina con un drop propio en forward, una sola regla arriba de ese drop (lección 4) permite todo lo publicado. Cambiá `drop final forward` por el comentario de tu drop:
```routeros
/ip/firewall/filter/add chain=forward in-interface-list=WAN connection-state=new connection-nat-state=dstnat action=accept comment="permitir publicados" place-before=[find comment="drop final forward"]
```
5. Limpiá las conexiones viejas y probá desde afuera:
```routeros
/ip/firewall/connection/remove [find dst-address~":18000"]
/ip/firewall/connection/remove [find dst-address~":18554"]
```
Desde la oficina (en la lista), en PowerShell; lo esperado es `TcpTestSucceeded : True`:
```powershell
Test-NetConnection 203.0.113.10 -Port 18000
```
RTSP en VLC (Medio, Abrir ubicación de red; pide usuario y clave del NVR). En Hikvision, 101 es el flujo principal del canal 1:
```text
rtsp://203.0.113.10:18554/Streaming/Channels/101
```
Desde el celular con datos móviles y el wifi apagado (fuera de la lista) no conecta. Un chequeo de puertos externo, como el canyouseeme que sugiere Dahua, también da cerrado: es lo esperado, su IP no está en la lista.
6. Mirá los contadores mientras probás:
```routeros
/ip/firewall/nat/print stats where comment~"NVR"
/ip/firewall/connection/print where dst-address~":18000"
```
Si el contador no sube, el paquete no llega al MikroTik o el origen no está en la lista: doble NAT, CGNAT, filtro del proveedor. Si sube y no conecta, mirá el NVR (gateway que no es el MikroTik, puerto cambiado) o el forward.
7. Hairpin, solo si en la oficina entran por la IP pública. Un dst-nat para la LAN (desde adentro no se entra por la WAN) y el masquerade que hace volver la respuesta por el router:
```routeros
/ip/firewall/nat/add chain=dstnat src-address=192.168.88.0/24 dst-address-type=local dst-address=!192.168.88.1 protocol=tcp dst-port=18000 action=dst-nat to-addresses=192.168.88.50 to-ports=8000 comment="NVR1 hairpin dstnat"
/ip/firewall/nat/add chain=srcnat src-address=192.168.88.0/24 dst-address=192.168.88.50 protocol=tcp dst-port=8000 out-interface=bridge action=masquerade comment="NVR1 hairpin srcnat"
```
En el srcnat va el puerto interno (8000), porque se evalúa después del dst-nat. Con IP pública fija, `dst-address=203.0.113.10` reemplaza a `dst-address-type=local dst-address=!192.168.88.1`. La alternativa sin hairpin es un DNS local, que deja al NVR ver la IP real de cada PC, pero solo sirve si el puerto externo es igual al interno (el DNS cambia la IP, no el puerto):
```routeros
/ip/dns/static/add name=nvr.ejemplo.com address=192.168.88.50
```

⚠️ No publiques sin `src-address-list` "un rato para probar": un análisis de 2026 encontró casi un millón de servicios RTSP en internet, en más de diez mil puertos distintos. Cambiar el puerto saca ruido, no esconde el servicio.

⚠️ El 8000 y el 37777 dan login, video y configuración del NVR. Con clave débil o firmware viejo (Hikvision CVE-2021-36260 por la web, Dahua CVE-2021-33044 y CVE-2021-33045) es entregar el equipo. Primera opción, VPN (lecciones 8 y 19); publicar es para orígenes fijos y conocidos.

**Regla para quedarse**
Un puerto por servicio, entrando por la WAN, para una lista de orígenes; lo pruebo desde afuera y miro el contador.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- dst-nat, hairpin y CGNAT en RouterOS 7.25: https://manual.mikrotik.com/docs/7.25/firewall-and-quality-of-service/firewall/nat
- La regla demasiado general que dejó a la LAN sin navegar: https://forum.mikrotik.com/t/noob-sorry-nat-port-80-breaking-outbound-web/41994
- Login sí, video no: los puertos de un Dahua detrás de un MikroTik: https://forum.mikrotik.com/t/need-help-with-port-forwarding/159605
- Puertos por defecto de Hikvision y cómo cambiarlos: https://learncctv.com/default-ports-for-hikvision-dvr
- Puertos de fábrica y chequeo externo según Dahua: https://www.dahuasecurity.com/about-dahua/news-events/notice/how-to-setup-remote-access-for-nvr
- Hairpin o DNS local, y la IP real del cliente: https://forum.mikrotik.com/t/hairpin-nat-using-local-dns/174370
- RTSP expuesto en internet, análisis de 2026: https://www.modat.io/post/exposed-rtsp
