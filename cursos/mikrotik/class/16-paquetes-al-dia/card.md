# Lección 16. Paquetes al día

**Escuchá:** paquetes-al-dia.mp3 (2 min)

**La idea, en tres líneas**
- System > Packages > Check for Updates muestra el changelog del canal; **Download** baja y espera que reinicies vos, **Download&Install** reinicia solo al terminar.
- Casi todo está en el paquete `routeros`; los extras (container, zerotier, user-manager, wifi-qcom, wireless) se habilitan y se aplican con reinicio. Desde 7.13, `wireless` y `wifi-qcom` no pueden estar activos a la vez.
- Sin internet: `.npk` de la arquitectura del equipo, a la raíz de Files, y reinicio. Para volver atrás: `.npk` viejos y `/system/package/downgrade`. Después de cualquier cambio, RouterBOOT.

**Impacto:** actualizás también los sitios sin salida a internet y sabés deshacer una versión que falló, sin Netinstall.

**Quién lo dice:** 2 de 3 fuentes coinciden (las dos páginas oficiales de paquetes y de actualización); ninguna discrepa. El distribuidor LinITX solo opina sobre canales (lección 17).

**Laboratorio** · Admin · 20 min
En un RouterBOARD de laboratorio con RouterOS 7 y salida a internet:
1. Antes de actualizar, backup. Siempre.
```routeros
/system/backup/save name=pre-paquetes password="Backup-Lab-Ejemplo-1"
/export file=pre-paquetes
```
2. Arquitectura, versión y paquetes:
```routeros
/system/resource/print
/system/package/update/check-for-updates
/system/package/print
```
Anotá `architecture-name`. Los paquetes con flags `X A` están disponibles en el servidor pero no instalados.
3. Instalá un paquete extra que no uses y deshacelo (zerotier es de ejemplo; en equipos sin ese paquete, elegí otro de la lista):
```routeros
/system/package/enable zerotier
/system/package/apply-changes
```
Después del reinicio, revisá `/log/print where topics~"system"` y desinstalalo:
```routeros
/system/package/uninstall zerotier
/system/package/apply-changes
```
4. Actualización sin internet: en la PC bajá de mikrotik.com el `.npk` de la misma arquitectura y arrastralo a Files en WinBox, en la raíz. Verificá y reiniciá:
```routeros
/file/print where name~".npk"
/system/reboot
```
5. Downgrade de práctica: subí el `.npk` de la versión anterior y ejecutá:
```routeros
/system/package/downgrade
```
6. Cerrá con RouterBOOT:
```routeros
/system/routerboard/print
/system/routerboard/upgrade
/system/reboot
```

⚠️ En equipos WiFi, si actualizás a mano subí también el paquete de radio (`wifi-qcom` o `wireless`) de la misma versión, o el equipo arranca sin WiFi. Nunca cortes la energía durante la instalación.

**Regla para quedarse**
Changelog, backup, paquetes de la misma arquitectura y versión, y RouterBOOT al final.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Paquetes de RouterOS 7.25: extras, instalar, desinstalar y downgrade: https://manual.mikrotik.com/docs/7.25/getting-started/installation-and-upgrade/packages/
- Actualización estándar, manual por Files y actualización local: https://help.mikrotik.com/docs/spaces/ROS/pages/328142/Upgrading+and+installation
- RouterBOOT después de RouterOS: https://help.mikrotik.com/docs/display/ROS/RouterBOOT
