# Lección 3. Cerrar puertas

**Escuchá:** cerrar-puertas.mp3 (2 min)

**La idea, en tres líneas**
- WinBox, SSH y API nunca hacia internet; si hace falta entrar de afuera, VPN.
- Apagá los servicios que no usás (telnet, ftp, www, api) y dejá MAC server y descubrimiento solo hacia la LAN.
- En un equipo heredado, actualizar no alcanza: contraseña nueva y auditoría de scheduler, SOCKS, clientes PPP y reglas raras.

**Impacto:** el router deja de aparecer en los escaneos automáticos y detectás equipos que ya fueron tomados.

**Quién lo dice:** 7 de 7 fuentes coinciden en no exponer la gestión; la guía de MikroTik documenta cómo abrirla filtrada por origen solo cuando es inevitable. Según un honeypot de Gen Digital, una versión vieja expuesta cayó en 15 minutos pese a tener contraseña fuerte.

**Laboratorio** · Foco · 15 min
En RouterOS 7, desde New Terminal:
1. Mirá qué escucha el router y apagá lo que no usás:
```routeros
/ip/service/print
/ip/service/disable telnet,ftp,www,api
/ip/service/set winbox,ssh available-from=192.168.88.0/24
```
2. MAC server y descubrimiento solo hacia la LAN (la lista `LAN` viene en la configuración por defecto):
```routeros
/tool/mac-server/set allowed-interface-list=LAN
/tool/mac-server/mac-winbox/set allowed-interface-list=LAN
/ip/neighbor/discovery-settings/set discover-interface-list=LAN
/tool/bandwidth-server/set enabled=no
/ip/socks/set enabled=no
/ip/proxy/set enabled=no
/ip/upnp/set enabled=no
```
3. Auditoría de equipo heredado (lo que MikroTik pidió revisar tras Mēris):
```routeros
/system/scheduler/print
/system/script/print
/ip/socks/print
/interface/l2tp-client/print
/ip/firewall/filter/print where dst-port~"5678"
```
4. Anotá en el legajo del cliente lo que encontraste. Si hay scheduler o scripts que nadie reconoce: contraseña nueva para todos los usuarios y revisión del firewall.

⚠️ `available-from` deja el puerto visible: el router cierra la conexión pero no la oculta. Para esconder el servicio, además, drop en la cadena input (lección 4).

**Regla para quedarse**
La gestión no mira a internet; si hay que entrar de afuera, se entra por VPN.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Guía oficial de hardening RouterOS 7.25: https://manual.mikrotik.com/docs/7.25/getting-started/securing-your-router
- Aviso de MikroTik sobre Mēris y qué revisar: https://mikrotik.com/supportsec/meris-botnet
- El honeypot comprometido en 15 minutos: https://www.gendigital.com/blog/insights/research/meris-and-trickbot-standing-on-the-shoulders-of-giants
