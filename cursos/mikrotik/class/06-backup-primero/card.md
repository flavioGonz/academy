# Lección 6. Backup primero

**Escuchá:** backup-primero.mp3 (2 min)

**La idea, en tres líneas**
- `.backup` es binario y clona todo: para restaurar el mismo equipo. `export` es texto `.rsc`: para leer, comparar y migrar.
- El export no lleva contraseñas de usuarios ni certificados; con `show-sensitive` incluye claves (WiFi, PPPoE, VPN) y pasa a ser un archivo sensible.
- Export antes de tocar y export después: cualquier "quién cambió esto" se contesta con un diff.

**Impacto:** volvés atrás en minutos y tenés registro de cada intervención en el legajo del cliente.

**Quién lo dice:** 3 de 3 fuentes coinciden (documentación de Configuration Management, primera configuración y un practicante que versiona exports en git); ninguna discrepa.

**Laboratorio** · Admin · 10 min
En RouterOS 7, desde New Terminal:
1. Foto de antes, en texto y en binario:
```routeros
/export file=antes
/export show-sensitive file=antes-sensible
/system/backup/save name=antes password="Backup-Lab-Ejemplo-1"
/file/print
```
2. Hacé un cambio chico (por ejemplo `/system/identity/set name=LAB-MT01`) y sacá la foto de después: `/export file=despues`.
3. Bajá `antes.rsc` y `despues.rsc` a la notebook (WinBox, Files, arrastrar) y comparalos:
```bash
diff antes.rsc despues.rsc
```
En Windows: `fc antes.rsc despues.rsc`.
4. Probá un import en seco sobre un equipo de prueba:
```routeros
/import file-name=despues.rsc verbose=yes dry-run
```
5. Guardá `antes-sensible.rsc` y el `.backup` en un lugar con acceso restringido, nunca en un chat ni en un mail sin cifrar.

⚠️ Un `.backup` restaurado en otro modelo puede traer problemas de interfaces y MAC; para migrar entre equipos distintos, export e import revisado.

**Regla para quedarse**
Antes de tocar, export; después de tocar, export.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Export, import, dry-run y reset en la documentación: https://help.mikrotik.com/docs/spaces/ROS/pages/328155/Configuration+Management
- Backup automático de exports a git por SSH: https://xtremeownage.com/blog/2025/mikrotik-backup-script/
