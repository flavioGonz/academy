# Lección 1. Primer arranque

**Escuchá:** primer-arranque.mp3 (2 min)

**La idea, en tres líneas**
- El modo de red (Switch, Route o Dual) se decide antes de configurar nada: DHCP opción 66 y la defensa dinámica solo andan en Route.
- Se entra por HTTPS al 8089 con la contraseña de la etiqueta, y se cambia en el primer ingreso.
- Firmware al día, pero antes de actualizar, backup. Siempre.

**Impacto:** la central arranca cerrada y con un punto de vuelta atrás desde el primer día.

**Quién lo dice:** 3 de 4 fuentes coinciden; la guía de Telnyx todavía cita admin/admin, que no aplica a equipos fabricados desde 2017.

**Laboratorio** · Foco · 15 min
1. Con la UCM6300 conectada por el puerto WAN, leé la IP en el LCD (botón Home) o en el DHCP de tu red de laboratorio.
2. Entrá a la web y cambiá la contraseña de admin (10 a 30 caracteres, mayúscula, minúscula, número y especial).
```text
192.168.88.20:8089   (se abre por HTTPS)
Usuario: admin   Contraseña: la de la etiqueta trasera
Maintenance > Login Settings > Change Password
```
3. Elegí el modo de red y anotá por qué. Si vas a usar opción 66 o Dynamic Defense, Route.
```text
System Settings > Network Settings > Basic Settings > Method: Switch | Route | Dual
```
4. Anotá la versión de firmware y bajá un backup completo a tu notebook.
```text
Maintenance > Upgrade   (versión actual, botón Detect)
Maintenance > Backup > Backup/Restore > Backup   (guardá el .tar fuera de la central)
```
5. Con el backup guardado, recién ahí actualizá si hay versión nueva.
⚠️ Cambiar el modo de red en una central en producción corta el acceso web y los teléfonos: hacelo en ventana de mantenimiento y con acceso por consola o LCD a mano.

**Regla para quedarse**
Antes de actualizar, backup; y ninguna central sale de la camioneta con la contraseña de la etiqueta.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Manual de seguridad de la UCM (contraseña, login, MFA): https://documentation.grandstream.com/knowledge-base/ucm6xxx-security-manual/
- Manual del UCM630x (modos de red, upgrade, backup): https://documentation.grandstream.com/knowledge-base/ucm630x-series-user-manual/
- CVE-2025-28172, fuerza bruta en UCM6510: https://www.tenable.com/cve/CVE-2025-28172
