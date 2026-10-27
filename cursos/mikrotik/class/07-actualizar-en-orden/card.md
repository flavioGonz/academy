# Lección 7. Actualizar en orden

**Escuchá:** actualizar-en-orden.mp3 (2 min)

**La idea, en tres líneas**
- Canal `stable` o `long-term` en producción; `testing` y `development`, nunca.
- Orden: backup, RouterOS, reinicio, RouterBOOT (`/system/routerboard/upgrade`), reinicio.
- Desde RouterOS 6 se pasa por una versión intermedia (7.12.1); desde 7.23 el chequeo usa HTTPS y el router necesita salir por TCP 443.

**Impacto:** los equipos que entregás no quedan con fallas que tienen parche hace años.

**Quién lo dice:** 4 de 6 fuentes coinciden en el método; sobre stable o long-term no hay ganador. Según Eclypsium (vía CSO), más de 2 millones de MikroTik tenían gestión expuesta y unos 300.000 seguían vulnerables a fallas ya corregidas.

**Laboratorio** · Admin · 15 min
En un RouterBOARD de laboratorio con RouterOS 7 y salida a internet:
1. Antes de actualizar, backup. Siempre.
```routeros
/export file=pre-upgrade
/system/backup/save name=pre-upgrade password="Backup-Lab-Ejemplo-1"
```
2. Mirá versión, canal y bootloader:
```routeros
/system/resource/print
/system/package/update/print
/system/routerboard/print
```
Anotá `current-firmware` y `upgrade-firmware`.
3. Elegí canal y actualizá:
```routeros
/system/package/update/set channel=long-term
/system/package/update/check-for-updates
/system/package/update/install
```
4. Después del reinicio, actualizá el bootloader y reiniciá otra vez:
```routeros
/system/routerboard/upgrade
/system/reboot
```
5. Verificá que `current-firmware` ahora coincide con `upgrade-firmware` y revisá el log: `/log/print where topics~"system"`.
6. Anotá en el legajo del cliente: versión de RouterOS, de RouterBOOT, canal y fecha.

⚠️ No cortes la energía durante la actualización. En sitios remotos, actualizá con alguien en el lugar o con un plan de rescate (Netinstall, lección 1).

**Regla para quedarse**
RouterOS y RouterBOOT se actualizan juntos, con backup antes.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Canales y actualización estándar: https://help.mikrotik.com/docs/spaces/ROS/pages/328142/Upgrading+and+installation
- RouterBOOT, loader de respaldo y botón de reset: https://help.mikrotik.com/docs/display/ROS/RouterBOOT
- El estudio de los 300.000 routers sin parchar: https://www.csoonline.com/article/3644469/researchers-warn-about-continuous-abuse-of-unpatched-mikrotik-routers.html
