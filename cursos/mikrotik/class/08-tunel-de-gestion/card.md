# Lección 8. Túnel de gestión

**Escuchá:** tunel-de-gestion.mp3 (2 min)

**La idea, en tres líneas**
- Para entrar de afuera, VPN: WireGuard como primera opción; L2TP/IPsec cuando del otro lado solo hay el cliente nativo del sistema; PPTP, nunca.
- Un peer por técnico con `allowed-address` /32, y el puerto UDP del túnel aceptado en `input` arriba del drop.
- `persistent-keepalive=25s` si hay NAT en el medio; desde 7.21 el router genera la configuración del cliente con QR.

**Impacto:** entrás a cualquier cliente sin dejar WinBox ni SSH mirando a internet, y das de baja a un técnico borrando su peer.

**Quién lo dice:** 4 de 7 fuentes coinciden en VPN con WireGuard primero; una guía práctica (con sesgo comercial) defiende L2TP/IPsec por compatibilidad nativa y el aviso de Mēris nombra IPsec.

**Laboratorio** · Foco · 20 min
En un router de laboratorio con RouterOS 7 y configuración por defecto (claves y rangos de ejemplo):
1. Interfaz y dirección del túnel:
```routeros
/interface/wireguard/add name=wg-gestion listen-port=13231
/ip/address/add address=10.10.10.1/24 interface=wg-gestion
/interface/wireguard/print
```
Copiá la `public-key` del router.
2. En la notebook, en la app WireGuard, creá un túnel vacío y copiá su clave pública. Agregá el peer en el router:
```routeros
/interface/wireguard/peers/add interface=wg-gestion name=notebook-lucia public-key="PEGAR-CLAVE-PUBLICA-DE-LA-NOTEBOOK" allowed-address=10.10.10.2/32
```
3. Abrí el puerto del túnel arriba del drop de la defconf y permití WinBox solo desde el túnel:
```routeros
/ip/firewall/filter/add chain=input protocol=udp dst-port=13231 action=accept comment="wireguard" place-before=[find comment="defconf: drop all not coming from LAN"]
/ip/firewall/filter/add chain=input in-interface=wg-gestion protocol=tcp dst-port=8291 action=accept comment="winbox por tunel" place-before=[find comment="defconf: drop all not coming from LAN"]
```
4. Configuración de la notebook (solo la red de gestión va por el túnel):
```text
[Interface]
PrivateKey = (la genera la app)
Address = 10.10.10.2/32

[Peer]
PublicKey = CLAVE-PUBLICA-DEL-ROUTER
Endpoint = 203.0.113.10:13231
AllowedIPs = 10.10.10.0/24
PersistentKeepalive = 25
```
5. Activá el túnel, mirá `last-handshake` en `/interface/wireguard/peers/print` y entrá por WinBox a `10.10.10.1`.

⚠️ No pongas `AllowedIPs = 0.0.0.0/0` en la notebook si solo querés gestión: mandarías todo tu tráfico por el cliente.

**Regla para quedarse**
A un cliente se entra por túnel, nunca por un puerto abierto.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- WireGuard en RouterOS: road warrior, sitio a sitio y firewall: https://help.mikrotik.com/docs/spaces/ROS/pages/69664792/WireGuard
- Por qué VPN y no gestión expuesta: https://manual.mikrotik.com/docs/7.25/getting-started/securing-your-router
- L2TP/IPsec paso a paso, puertos y FastTrack (en alemán, de un proveedor de VPS): https://cloudzy.com/de/blog/mikrotik-l2tp-vpn/
