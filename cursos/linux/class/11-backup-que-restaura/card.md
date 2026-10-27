# Lección 11. Backup que restaura

**Escuchá:** backup-que-restaura.mp3 (2 min)

**La idea, en tres líneas**
- Un backup existe cuando restauraste un archivo de él, no cuando el script terminó sin errores.
- `tar` para configuraciones (por ejemplo `/etc`), `rsync` para datos que cambian; la copia va a otro lugar físico; las bases de datos se respaldan con un dump.
- Programado con un timer de systemd (`Persistent=true` recupera la ejecución perdida si el equipo estaba apagado) o con cron para lo simple.

**Impacto:** ante un disco roto o un cambio que salió mal, recuperás la configuración del servidor en minutos y con un procedimiento ya probado.

**Quién lo dice:** 2 de 3 fuentes sobre backups coinciden (Ubuntu Server, Debian Handbook). En programación hay división: trstringer prefiere timers; la Arch Wiki marca sus costos (dos archivos, sin aviso por mail nativo); el Debian Handbook enseña cron primero.

**Laboratorio** · Admin · 20 min
En una VM de prueba (destino de ejemplo `/srv/backup`; en producción, un disco o servidor aparte):
1. Script de backup:
```bash
sudo mkdir -p /srv/backup
sudo tee /usr/local/bin/backup-etc.sh >/dev/null <<'FIN'
#!/bin/bash
set -e
destino=/srv/backup
archivo="$destino/$(hostname -s)-etc-$(date +%F).tar.gz"
tar czf "$archivo" /etc
find "$destino" -name "*-etc-*.tar.gz" -mtime +14 -delete
FIN
sudo chmod 750 /usr/local/bin/backup-etc.sh
```
2. Servicio y timer:
```text
# /etc/systemd/system/backup-etc.service
[Unit]
Description=Backup de /etc

[Service]
Type=oneshot
ExecStart=/usr/local/bin/backup-etc.sh
```
```text
# /etc/systemd/system/backup-etc.timer
[Unit]
Description=Backup diario de /etc

[Timer]
OnCalendar=*-*-* 02:30:00
Persistent=true
RandomizedDelaySec=15min

[Install]
WantedBy=timers.target
```
```bash
systemd-analyze calendar "*-*-* 02:30:00"     # valida y muestra la próxima ejecución
sudo systemctl daemon-reload
sudo systemctl enable backup-etc.timer
sudo systemctl start backup-etc.timer
sudo systemctl start backup-etc.service       # forzá una corrida
journalctl -u backup-etc.service -n 20
systemctl list-timers | grep backup
```
3. La prueba que importa, restaurar a /tmp y comparar:
```bash
ls -lh /srv/backup
sudo tar xzf /srv/backup/*-etc-*.tar.gz -C /tmp etc/hostname
diff /tmp/etc/hostname /etc/hostname && echo "restaurado OK"
```
4. Para datos, rsync a otro equipo (primero en simulacro con -n):
```bash
rsync -avn /srv/datos/ backup@10.10.10.20:/respaldos/servidor1/
```
Equivalente con cron, en una línea: `30 2 * * * root /usr/local/bin/backup-etc.sh` en `/etc/cron.d/backup-etc`.

**Regla para quedarse**
No hay backup hasta que restauré un archivo de él, y la copia vive en otro lugar físico.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Backups con tar, rotación y restauración en Ubuntu Server: https://documentation.ubuntu.com/server/how-to/backups/back-up-using-shell-scripts/
- La estrategia de Falcot Corp con rsync en el Debian Handbook: https://debian-handbook.info/browse/stable/sect.backup.html
- Timers de systemd, Persistent y OnCalendar: https://wiki.archlinux.org/title/Systemd/Timers
