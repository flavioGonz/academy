# Lección 11. Backup y etapas

**Escuchá:** backup-y-etapas.mp3 (2 min)

**La idea, en tres líneas**
- Antes de actualizar, backup. Siempre. Y dos copias recientes fuera del equipo (el backup no incluye video de Protect ni logs).
- Leé las notas de versión antes de un salto mayor: Network 11.0 borra el historial de estadísticas, quita soporte a USG y migra todo a zonas.
- Actualizá por etapas: solo Official, esperar unas semanas, un sitio piloto, después el resto. Network 10.5 y posteriores permiten revertir firmware y aplicación.

**Impacto:** las actualizaciones dejan de ser la causa de los llamados del lunes.

**Quién lo dice:** 3 de 3 fuentes sobre backups coinciden; 4 de 5 actualizan por etapas (HostiFi espera 2 a 3 semanas tras el pase a Official); nadie defiende actualizar todo el día del lanzamiento.

**Laboratorio** · Admin · 15 min
1. En la consola de laboratorio: Settings > System > Backups. Bajá un backup manual (archivo .unf o el backup de UniFi OS) y guardalo en dos lugares fuera del equipo.
2. Revisá que el autobackup esté activo y con qué frecuencia.
3. En la VM de UniFi OS Server de laboratorio, misma versión o superior: restaurá el archivo (Restore > subir archivo). El controlador reinicia.
4. Entrá con el usuario y contraseña que existían cuando se hizo el backup.
5. Si los equipos quedan "Disconnected" porque cambió la IP del controlador, apuntalos al nuevo con option 43, DNS o:
```bash
set-inform http://<controlador-nuevo>:8080/inform
```
6. Abrí las notas de versión de la próxima actualización (community.ui.com, sección Releases) y anotá: versión mínima de UniFi OS, qué se elimina, qué se migra.
7. Programá el firmware de equipos por sitio (HostiFi lo ubica en Settings > Services > Scheduled Upgrades; en Network 10.6 y 11 el nombre puede variar).
⚠️ Nunca actualices todos los sitios el mismo día. Un sitio piloto primero, los demás después.

**Regla para quedarse**
Antes de actualizar, backup. Siempre. Y un sitio piloto antes que el resto.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Cómo prueba y escalona HostiFi las versiones: https://www.hostifi.com/support/hostifi-how-we-handle-unifi-updates
- Restaurar un backup paso a paso: https://deluisio.com/networking/unifi/2025/08/05/how-to-restore-unifi-from-backup/
- Notas de Network 11.0.97, qué se elimina y migra: https://community.ui.com/releases/UniFi-Network-Application-11-0-97/15662d06-8122-44e2-a1ba-af5d71b8a045
- Revert y Test and Confirm en Network 10.5: https://forums.lawrencesystems.com/t/unifi-10-5-made-changes-safer-troubleshooting-clients-a-lot-easier-youtube-release/26907
