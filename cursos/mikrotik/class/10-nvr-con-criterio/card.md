# Lección 10. NVR con criterio

**Escuchá:** nvr-con-criterio.mp3 (2 min)

**La idea, en tres líneas**
- Primera opción, VPN (lección 8). Si igual hay que publicar un NVR: solo el puerto que usa la app, entrando por la lista WAN y con origen limitado por address-list.
- Nunca un puerto del propio router (80, 443, 8291) ni "todos los puertos del NVR por las dudas".
- Hairpin solo si desde la LAN entran por la IP pública; después de cambiar NAT, limpiá las conexiones.

**Impacto:** el NVR deja de estar a la vista de cualquier escaneo y el acceso queda acotado a quien de verdad lo necesita.

**Quién lo dice:** 4 de 6 fuentes coinciden en publicar lo mínimo y filtrado; el ejemplo de primera configuración de MikroTik publica un puerto sin filtrar el origen, y en el foro publicar cámaras se trata como rutina.

**Laboratorio** · Campo · 15 min
Escenario de ejemplo: NVR en 192.168.88.50, su app usa TCP 8000 (cambialo por el puerto real de tu NVR); la central de monitoreo sale con 203.0.113.25.
1. Lista de orígenes permitidos:
```routeros
/ip/firewall/address-list/add list=nvr-permitidos address=203.0.113.25 comment="central monitoreo ejemplo, revisar 2027-04"
```
2. dst-nat solo desde esa lista y solo por WAN:
```routeros
/ip/firewall/nat/add chain=dstnat in-interface-list=WAN protocol=tcp dst-port=8000 src-address-list=nvr-permitidos action=dst-nat to-addresses=192.168.88.50 to-ports=8000 comment="NVR central"
```
3. Limpiá las conexiones viejas para que la regla nueva aplique:
```routeros
/ip/firewall/connection/remove [find dst-address~":8000"]
```
4. Probá desde el celular con datos móviles: sin estar en la lista no tiene que conectar. Agregá tu IP pública a `nvr-permitidos` y probá de nuevo. Mirá el contador: `/ip/firewall/nat/print stats where comment="NVR central"`.
5. Solo si en la oficina entran por la IP pública, hairpin:
```routeros
/ip/firewall/nat/add chain=srcnat src-address=192.168.88.0/24 dst-address=192.168.88.50 protocol=tcp dst-port=8000 out-interface=bridge action=masquerade comment="hairpin NVR"
```
(y en el dst-nat, en lugar de `in-interface-list=WAN`, `dst-address-type=local dst-address=!192.168.88.1`).

⚠️ No publiques el NVR a todo internet "un rato para probar": los escaneos automáticos llegan en minutos (lección 3).

**Regla para quedarse**
Si publico algo, publico un puerto, para una lista de orígenes, con fecha de revisión.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- dst-nat, src-address y hairpin en la documentación de NAT: https://manual.mikrotik.com/docs/7.25/firewall-and-quality-of-service/firewall/nat
- El caso de la cámara que no andaba desde adentro: https://forum.mikrotik.com/t/solved-hairpin-nat-not-working/97689
- Port forwarding en la primera configuración (y por qué filtrar el origen): https://manual.mikrotik.com/docs/7.25/getting-started/first-time-configuration
