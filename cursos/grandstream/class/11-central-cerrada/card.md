# Lección 11. Central cerrada

**Escuchá:** central-cerrada.mp3 (2 min)

**La idea, en tres líneas**
- Fail2ban viene activo (baneo de 600 s por defecto): sumá tus IPs de soporte a la Allowlist.
- Administración cerrada: lista blanca web de hasta 10 IPs, sin 80 ni 443, SSH y AMI apagados, Geo-IP para países que no usás.
- Remotos: VPN si alguien la mantiene, lista blanca por IP para sedes fijas, o puerto no estándar con Fail2ban, Geo-IP y PIN.

**Impacto:** la central sobrevive a los barridos automáticos y una extensión comprometida no se convierte en una factura internacional.

**Quién lo dice:** 4 de 7 fuentes coinciden en cerrar la administración y 3 de 7 en Fail2ban; para remotos hay división: VPN primero (FreePBX, integrador con 15 años) contra lista blanca por IP o puertos con defensas (otros hilos de FreePBX).

**Laboratorio** · Admin · 15 min
1. Fail2ban y tus IPs permitidas:
```text
System Settings > Security Settings > Fail2Ban
Enable: Sí   Banned Duration: 600 (o más)
Allowlist: 192.168.88.0/24, IP fija de la oficina técnica
SIP Defense y Login Attack Defense: activos
```
2. Acceso web:
```text
System Settings > HTTP Server
Redirect From Port 80: No
Port: 8089 (o uno no estándar, nunca 80 ni 443)
Enable IP Address Whitelist: Sí (red local y oficina técnica)
```
3. Servicios:
```text
System Settings > Security Settings > SSH Access: desactivado
GDMS Remote SSH: desactivado salvo durante un soporte
```
4. Geo-IP (si la central recibe remotos por internet): permití solo los países que usás, verificando antes que tu propia IP no quede bloqueada.
```text
System Settings > Security Settings > Geo-IP Access Control
```
5. En el router, hacé una tabla: puerto abierto, destino, motivo, quién lo pidió. Cerrá lo que no tenga motivo.
⚠️ Activar la lista blanca web o Geo-IP en remoto sin incluir tu propia IP te deja afuera de la central.

**Regla para quedarse**
Cada puerto abierto tiene nombre, motivo y Fail2ban mirando.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Manual de seguridad de la UCM: https://documentation.grandstream.com/knowledge-base/ucm6xxx-security-manual/
- Cuántos ataques llegan a un PBX expuesto: https://wazo-platform.discourse.group/t/fail2ban-guide-for-servers-on-the-internet/399
- VPN o TLS para remotos, la discusión: https://community.freepbx.org/t/vpn-or-tls/91126
