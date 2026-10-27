# Lección 11. Túnel entre sedes

**Escuchá:** tunel-entre-sedes.mp3 (2 min)

**La idea, en tres líneas**
- Auto IPsec: los dos gateways en sitios distintos del mismo controlador, ambos con IP pública en la WAN (sin NAT adelante) y LAN que no se solapen.
- Manual IPsec cuando hay NAT: UDP 500 y 4500 abiertos en el equipo que hace NAT y Local/Remote ID tipo Name. Verificación en Network Config > VPN Status > Site-to-Site VPN > IPsec.
- Con el túnel arriba, los equipos de la sucursal pueden adoptarse con option 138 apuntando a la IP privada del controlador, sin abrir puertos a internet.

**Impacto:** CCTV y control de acceso de varias sedes vistos desde la central sin exponer el controlador.

**Quién lo dice:** 2 de 3 fuentes sobre VPN coinciden; Evan McCann matiza: el sitio a sitio de Omada está bien, pero para VPN de usuarios remotos y routing avanzado recomienda otro firewall (reseña de 2022).

**Laboratorio** · Foco · 20 min
Dos ER (por ejemplo ER605) con IP en la WAN alcanzables entre sí (en laboratorio, 203.0.113.10 y 203.0.113.20):
1. Planificá subredes que no se solapen:
```text
Sitio Central   LAN 10.10.10.0/24   WAN 203.0.113.10
Sitio Sucursal  LAN 10.10.20.0/24   WAN 203.0.113.20
```
2. Adoptá cada ER en su propio sitio (Lección 5) y cambiá la LAN por defecto de cada uno según la tabla.
3. En el sitio Central: **Network Config > VPN > Site-to-Site VPN > Create New Site-to-Site VPN**, tipo **Auto IPsec**, sitio remoto `Sucursal`. Guardá.
4. Verificá en **Network Config > VPN Status > Site-to-Site VPN > IPsec** que aparezcan las entradas.
5. Desde una PC en la Central:
```powershell
ping 10.10.20.1
```
6. Si en la vida real la sucursal tiene el router del proveedor adelante, pasá a **Manual IPsec** y pedí al proveedor abrir UDP 500 y 4500 hacia el ER.
⚠️ Cambiar la LAN por defecto de un gateway en producción corta a todos los clientes hasta que renueven DHCP: hacelo en ventana de mantenimiento.

**Regla para quedarse**
Antes del túnel, una subred distinta por sede y saber si hay NAT adelante.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Auto IPsec entre gateways Omada: https://www.omadanetworks.com/us/support/faq/4699/
- Manual IPsec, NAT y adopción de la sucursal por el túnel: https://support.omadanetworks.com/de/document/124358/
- Límites de los gateways Omada en VPN y routing (visión de un practicante): https://evanmccann.net/blog/2022/3/tp-link-omada-overview
