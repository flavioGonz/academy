# Lección 13. IP fija

**Escuchá:** ip-fija.mp3 (2 min)

**La idea, en tres líneas**
- IP fija son cuatro datos (dirección con máscara, gateway, DNS) y tres comandos: `/ip/address`, `/ip/route` y `/ip/dns`.
- Antes de cargarla, deshabilitá el cliente DHCP que la configuración por defecto deja en ether1, para que no compitan por la interfaz.
- Verificá en orden: ping al gateway, ping a una IP de internet, resolución de nombres; cada falla apunta a una capa distinta.

**Impacto:** la WAN queda documentada y probada en minutos, y con gateway fijo el sitio queda listo para un failover con rutas recursivas (lección 11).

**Quién lo dice:** 3 de 5 fuentes coinciden (documentación de primera configuración y las páginas de Internet pyme y corporativo de Antel); ninguna discrepa. La documentación de NAT agrega que masquerade está pensado para IP dinámica.

**Laboratorio** · Rápido · 15 min
En un RouterBOARD con RouterOS 7 y configuración por defecto. Datos de ejemplo del proveedor: IP 203.0.113.10/29, gateway 203.0.113.9, DNS 1.1.1.1 y 9.9.9.9.
1. Antes de tocar la WAN, export (lección 6) y Safe Mode (lección 1). Mirá qué hay en ether1:
```routeros
/ip/dhcp-client/print
/ip/address/print where interface=ether1
```
2. Deshabilitá el cliente DHCP de ether1 y cargá la IP fija:
```routeros
/ip/dhcp-client/disable [find interface=ether1]
/ip/address/add address=203.0.113.10/29 interface=ether1 comment="WAN fija"
/ip/route/add dst-address=0.0.0.0/0 gateway=203.0.113.9 comment="default WAN fija"
/ip/dns/set servers=1.1.1.1,9.9.9.9
```
3. Verificá por capas:
```routeros
/ping 203.0.113.9 count=3
/ping 1.1.1.1 count=3
:put [:resolve mikrotik.com]
/ip/route/print where dst-address=0.0.0.0/0
```
Gateway sin respuesta: cable, máscara o VLAN. IP de internet sin respuesta: ruta o proveedor. Nombre sin resolver: DNS.
4. Confirmá que la IP es directa: `/ip/cloud/print` y compará `public-address` con 203.0.113.10 (lección 9).
5. Anotá en el legajo del cliente: IP, máscara, gateway, DNS y quién los entregó.

⚠️ Si cambiás la IP de la WAN de un router al que entrás de forma remota, hacelo en Safe Mode: un gateway mal escrito te deja afuera.

**Regla para quedarse**
IP fija: dirección, ruta y DNS a mano, y tres pings antes de irme.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- DHCP, IP estática y PPPoE en la primera configuración: https://manual.mikrotik.com/docs/7.25/getting-started/first-time-configuration
- Internet pyme de Antel, con una IP pública fija: https://antel.com.uy/empresas/internet-y-fija/planes/internet-pyme
- Masquerade, src-nat y IP dinámica: https://manual.mikrotik.com/docs/7.25/firewall-and-quality-of-service/firewall/nat
