# Lección 2. Usuarios propios

**Escuchá:** usuarios-propios.mp3 (2 min)

**La idea, en tres líneas**
- Un usuario por técnico, con contraseña de 12 caracteres o más; probalo y recién después deshabilitá `admin`.
- El grupo `read` de fábrica puede reiniciar y ver configuración sensible: para mirar sin tocar, armá un grupo propio.
- Limitá cada cuenta a direcciones de origen (la LAN de gestión o la VPN) con la propiedad `address`.

**Impacto:** sabés quién cambió qué, y das de baja a un técnico sin tocar la clave de todos.

**Quién lo dice:** 3 de 3 fuentes coinciden; ninguna discrepa. Un practicante suma el usuario dedicado con permisos mínimos para backups automáticos.

**Laboratorio** · Admin · 10 min
En el equipo de laboratorio (RouterOS 7), desde New Terminal:
1. Creá tu usuario y un grupo de monitoreo sin `reboot` ni `write`:
```routeros
/user/add name=lucia.tecnico group=full password="Ejemplo-Lab-2026!x"
/user/group/add name=monitoreo policy=local,ssh,winbox,read,test
/user/add name=mesa.ayuda group=monitoreo password="Otro-Ejemplo-Lab-77" address=192.168.88.0/24
```
2. Cerrá WinBox y entrá con `lucia.tecnico`. Si entra, recién ahí:
```routeros
/user/disable admin
/user/print
```
3. Entrá con `mesa.ayuda` y probá `/system/reboot`: tiene que rechazarlo por falta de permisos.
4. Probá el detalle del signo pesos: en una contraseña entre comillas, escribilo como `\$`.

⚠️ No deshabilites `admin` sin haber probado antes tu usuario en otra sesión: si falla, quedás afuera y la única salida es reset o Netinstall.

**Regla para quedarse**
Nadie entra como admin: cada técnico tiene su usuario y cada rol su grupo.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Usuarios, grupos y contraseñas en la guía de seguridad 7.25: https://manual.mikrotik.com/docs/7.25/getting-started/securing-your-router
- Crear usuario nuevo y deshabilitar admin: https://manual.mikrotik.com/docs/7.25/getting-started/first-time-configuration
- Usuario de backup con permisos mínimos: https://xtremeownage.com/blog/2025/mikrotik-backup-script/
