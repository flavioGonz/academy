# Lección 15. PPPoE con Antel

**Escuchá:** pppoe-con-antel.mp3 (2 min)

**La idea, en tres líneas**
- El ONT de Antel puede funcionar en modo puente o router; el cambio se pide a Antel (MiAntel o 121) y en fibra lo hace el proveedor de forma remota. En puente, el MikroTik hace el PPPoE con el usuario y la contraseña del servicio.
- Con PPPoE la WAN pasa a ser `pppoe-out1`: masquerade, lista WAN y reglas apuntan ahí. MTU y MRU hasta 1492, y MSS ajustado.
- VLAN: ninguna fuente leída confirma si Antel la pide con el ONT en puente. Probá primero sin VLAN con `pppoe-client/scan` y confirmalo con Antel.

**Impacto:** el router del cliente es el tuyo (firewall, VLANs, VPN y DDNS bajo tu control) y no un equipo intermedio con doble NAT.

**Quién lo dice:** 3 de 8 fuentes coinciden en que el puente se pide a Antel y el router propio marca PPPoE (Antel, un foro uruguayo y un instructivo de Montevideo COMM); 2 de 8 detallan MTU y MSS (documentación de MikroTik y una guía práctica). En contra: usuarios del foro macacos tuvieron cortes en 2017 con el ONT en puente y volvieron a modo router con doble NAT.

**Laboratorio** · Campo · 20 min
En un RouterBOARD con RouterOS 7, ether1 al puerto del ONT ya pasado a modo puente por Antel. Usuario y contraseña de ejemplo: `cliente-ejemplo` y `Clave-De-Ejemplo-1` (usá los que entregue Antel para ese servicio).
1. Export (lección 6). Deshabilitá el cliente DHCP de ether1 y buscá el concentrador:
```routeros
/ip/dhcp-client/disable [find interface=ether1]
/interface/pppoe-client/scan interface=ether1
```
Si aparece un `ac-name`, el PPPoE responde sin VLAN. Si no aparece nada, pedile a Antel el dato de VLAN antes de seguir.
2. Cliente PPPoE:
```routeros
/interface/pppoe-client/add name=pppoe-antel interface=ether1 user="cliente-ejemplo" password="Clave-De-Ejemplo-1" add-default-route=yes use-peer-dns=yes max-mtu=1492 max-mru=1492 disabled=no
/interface/list/member/add list=WAN interface=pppoe-antel
```
3. Si Antel te confirma una VLAN, el PPPoE va sobre la VLAN, no sobre ether1 (el número es de ejemplo):
```routeros
/interface/vlan/add name=vlan-wan interface=ether1 vlan-id=10
/interface/pppoe-client/set pppoe-antel interface=vlan-wan
```
4. Mirá el estado y el MTU negociado:
```routeros
/interface/pppoe-client/monitor pppoe-antel once
```
Anotá `status`, `mtu`, `mru` y `local-address`.
5. MSS: mirá si el perfil PPP que usa el cliente ya lo ajusta (`change-tcp-mss`). Si no, agregá la regla:
```routeros
/ppp/profile/print detail where name=default
/ip/firewall/mangle/add chain=forward out-interface=pppoe-antel protocol=tcp tcp-flags=syn action=change-mss new-mss=clamp-to-pmtu passthrough=yes comment="MSS PPPoE"
```
6. Reconectá (`/interface/pppoe-client/disable pppoe-antel` y `enable`) y mirá si `local-address` cambió. Si cambia, el acceso remoto va por DDNS o túnel (lecciones 18 a 20).

⚠️ No pongas IP estática ni cliente DHCP en la misma interfaz que el PPPoE: la documentación lo desaconseja por seguridad. Y si Antel pasa el ONT a puente, el sitio queda sin internet hasta que el MikroTik marque: coordiná la ventana con el cliente.

**Regla para quedarse**
Con Antel, confirmo modo puente y VLAN antes de ir, y anoto lo que me dijeron y quién.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- PPPoE en RouterOS 7.25, fases, MTU de 1492 y MSS: https://manual.mikrotik.com/docs/7.25/virtual-private-networks/pppoe/
- Antel: modo puente o router WiFi, cómo pedir el cambio: https://antel.com.uy/personas/preguntas-frecuentes/internet
- PPPoE con VLAN y problemas típicos (autenticación, NAT, MTU): https://getlabsdone.com/how-to-configure-pppoe-in-mikrotik-router/
