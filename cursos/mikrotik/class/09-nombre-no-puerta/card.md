# Lección 9. Nombre, no puerta

**Escuchá:** nombre-no-puerta.mp3 (2 min)

**La idea, en tres líneas**
- IP Cloud da un nombre `<serie>.sn.mynetname.net` que sigue a la IP pública; no abre ningún acceso.
- Comparar `public-address` con la IP de la interfaz WAN dice si hay IP directa, NAT del módem o CGNAT (100.64.0.0/10).
- Detrás de CGNAT no hay port forwarding posible: queda túnel saliente o Back To Home (WireGuard por los relays de MikroTik).

**Impacto:** sabés en diez minutos si el acceso remoto que te piden es posible, y por qué camino.

**Quién lo dice:** 2 de 3 fuentes coinciden (documentación de Cloud y guía de seguridad); en el foro hay usuarios que publican cámaras por puerto detrás del nombre de IP Cloud como práctica habitual.

**Laboratorio** · Rápido · 10 min
En un MikroTik con RouterOS 7 (los servicios cloud no existen en RouterOS x86):
1. Activá el DDNS y leé el estado:
```routeros
/ip/cloud/set ddns-enabled=yes
/ip/cloud/print
```
Anotá `dns-name`, `public-address` y `status`.
2. Mirá la IP de tu WAN (o del PPPoE):
```routeros
/ip/address/print where interface~"ether1|pppoe"
```
3. Decidí con esta tabla:
```text
public-address = IP del WAN          -> IP pública directa: se puede publicar con cuidado (lección 10)
public-address != IP del WAN, WAN privada (192.168.x, 10.x) -> NAT del módem: modo bridge o reenvío también en el módem
WAN en 100.64.0.0/10                 -> CGNAT: sin port forwarding; túnel saliente o Back To Home
```
4. Si no vas a usar el nombre, dejalo como sugiere la guía de seguridad:
```routeros
/ip/cloud/set ddns-enabled=auto update-time=no
```

⚠️ Tener el nombre DDNS no es tener acceso: el firewall por defecto sigue descartando lo que llega de internet, y está bien que así sea.

**Regla para quedarse**
Antes de prometer acceso remoto, comparo `public-address` con la IP del WAN.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- IP Cloud, DDNS y Back To Home en RouterOS 7.25: https://manual.mikrotik.com/docs/7.25/network-management/cloud/
- CGNAT y por qué rompe el port forwarding: https://manual.mikrotik.com/docs/7.25/firewall-and-quality-of-service/firewall/nat
- Gestión de sitios detrás de CGNAT con túnel saliente a un VPS: https://mkcontroller.com/blog/remote_access/mikrotik/remote_mikrotik_management_via_vps
