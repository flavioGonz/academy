# Lección 20. Concentrador CHR

**Escuchá:** concentrador-chr.mp3 (2 min)

**La idea, en tres líneas**
- "VPS" en esta lección es un MikroTik CHR (Cloud Hosted Router) en un servidor en la nube con IP pública, usado como concentrador de VPN: cada sitio sin IP pública abre un túnel saliente hacia él, así que el CGNAT del cliente deja de importar.
- Se instala escribiendo la imagen raw del CHR con `dd` desde el modo rescate del VPS, y arranca con admin sin contraseña en una IP pública: endurecerlo es el primer paso, no el último.
- Licencias según MikroTik: Free sin vencimiento con 1 Mbps de subida por interfaz; P1 1 Gbps (45 dólares), P10 10 Gbps (95), P-Unlimited (250); prueba de 60 días con cuenta de mikrotik.com. Las copias no reinician la prueba y IP Cloud pide licencia paga.

**Impacto:** un solo punto fijo para entrar a todos los sitios con CGNAT, también a los MikroTik MIPS que no tienen Back To Home.

**Quién lo dice:** 2 de 5 fuentes describen el concentrador con túnel saliente (MKController, que vende su propia nube como alternativa, y una guía de WireGuard sitio a sitio); la documentación de licencias y la guía de instalación de Hetzner completan el cuadro; nadie discrepa del patrón.

**Laboratorio** · Foco · 20 min
Un CHR de prueba (VM en Proxmox o VPS con IP pública de ejemplo 198.51.100.20) y un router de laboratorio detrás de NAT. Rango de túnel 10.10.10.0/24.
1. Endurecé el CHR antes de cualquier otra cosa (la oficina de ejemplo sale por 203.0.113.50):
```routeros
/user/add name=tecnico-lucia group=full password="Cambiar-Esta-Clave-Ejemplo-1"
```
Entrá con el usuario nuevo y recién ahí seguí:
```routeros
/user/disable admin
/ip/service/disable telnet,ftp,www,api,api-ssl
/ip/service/set winbox,ssh available-from=203.0.113.50/32,10.10.10.0/24
/tool/mac-server/set allowed-interface-list=none
/tool/mac-server/mac-winbox/set allowed-interface-list=none
/ip/neighbor/discovery-settings/set discover-interface-list=none
/ip/dns/set allow-remote-requests=no
```
2. Firewall de input del CHR. Mirá primero si ya trae reglas (`/ip/firewall/filter/print`); la lista WAN no viene, se crea:
```routeros
/interface/list/add name=WAN
/interface/list/member/add list=WAN interface=ether1
/ip/firewall/filter/add chain=input connection-state=established,related action=accept
/ip/firewall/filter/add chain=input protocol=udp dst-port=13231 action=accept comment="wireguard hub"
/ip/firewall/filter/add chain=input src-address=203.0.113.50/32 protocol=tcp dst-port=22,8291 action=accept comment="gestion oficina"
/ip/firewall/filter/add chain=input protocol=icmp action=accept
/ip/firewall/filter/add chain=input in-interface-list=WAN action=drop comment="drop resto WAN"
```
3. Licencia:
```routeros
/system/license/print
```
Para la prueba de 60 días, `/system/license/renew` con tu cuenta de mikrotik.com.
4. Hub WireGuard y un peer por sitio:
```routeros
/interface/wireguard/add name=wg-hub listen-port=13231
/ip/address/add address=10.10.10.1/24 interface=wg-hub
/interface/wireguard/peers/add interface=wg-hub name=sitio-lab public-key="CLAVE-PUBLICA-DEL-SITIO" allowed-address=10.10.10.2/32
/ip/firewall/filter/add chain=input in-interface=wg-hub protocol=tcp dst-port=8291 action=accept place-before=[find comment="drop resto WAN"] comment="winbox por tunel"
```
5. En el router del sitio (detrás de NAT o CGNAT):
```routeros
/interface/wireguard/add name=wg-central listen-port=13231
/ip/address/add address=10.10.10.2/24 interface=wg-central
/interface/wireguard/peers/add interface=wg-central public-key="CLAVE-PUBLICA-DEL-CHR" endpoint-address=198.51.100.20 endpoint-port=13231 allowed-address=10.10.10.0/24 persistent-keepalive=25s
/ip/firewall/filter/add chain=input in-interface=wg-central protocol=tcp dst-port=8291 action=accept place-before=[find comment="defconf: drop all not coming from LAN"] comment="winbox desde el hub"
```
6. Desde el CHR, `/ping 10.10.10.2`; desde tu notebook conectada al hub (peer propio, lección 8), WinBox a 10.10.10.2.

⚠️ Con la licencia Free el hub sube a 1 Mbps por interfaz: alcanza para WinBox y monitoreo de pocos sitios, no para ver video. Licenciá lo que uses; nada de clonar para estirar la prueba.

**Regla para quedarse**
El hub se endurece el día uno y se licencia según lo que transporta.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Licencias CHR en RouterOS 7.25: niveles, prueba, renovación y transferencia: https://manual.mikrotik.com/docs/7.25/getting-started/routeros-licensing/chr/chr-licensing/
- Instalar CHR en un servidor en la nube y endurecerlo: https://community.hetzner.com/tutorials/mikrotik-chr-basic-setup
- Un VPS como punto de encuentro para sitios con CGNAT: https://mkcontroller.com/blog/remote_access/mikrotik/remote_mikrotik_management_via_vps
