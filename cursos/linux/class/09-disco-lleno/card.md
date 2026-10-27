# Lección 9. Disco lleno

**Escuchá:** disco-lleno.mp3 (2 min)

**La idea, en tres líneas**
- `df -h` dice qué sistema de archivos se llenó; `du` dice qué carpeta lo llenó. Se baja de a un nivel.
- Sospechosos habituales: caché de apt, journal, logs sin rotar y, en Ubuntu 26.04, `/tmp` en memoria con tope de la mitad de la RAM.
- En `/etc/fstab`: UUID siempre (nunca `/dev/sdX`), `nofail` con timeout para discos que pueden faltar, y validar antes de reiniciar.

**Impacto:** un "no space left on device" en un servidor de video o de logs se resuelve en minutos, y un disco ausente no deja el equipo sin arrancar.

**Quién lo dice:** 3 de 4 fuentes sobre discos coinciden (Debian Reference, Debian Handbook, computingforgeeks); la Arch Wiki aporta fstab. La propia Arch Wiki marca como discutida su sección sobre nofail en discos externos.

**Laboratorio** · Campo · 15 min
En una VM de prueba (con un disco extra vacío para el paso 4, por ejemplo agregado desde Proxmox):
1. ¿Dónde está lleno?
```bash
df -h
df -i        # inodos: a veces se agotan antes que el espacio
```
2. ¿Qué lo llenó? (-x no cruza a otros discos)
```bash
sudo du -xh -d1 /var | sort -h | tail
sudo du -xh -d1 /var/log | sort -h | tail
```
3. Liberá lo seguro:
```bash
sudo apt-get clean                 # vacía /var/cache/apt/archives
sudo du -sh /var/log/journal       # cuánto ocupa el journal
```
Para achicar el journal a 500 MB de forma permanente:
```text
# /etc/systemd/journald.conf.d/ies.conf
[Journal]
SystemMaxUse=500M
```
```bash
sudo systemctl restart systemd-journald
```
4. Disco extra en fstab por UUID:
```bash
lsblk -f                                   # anotá el UUID del disco nuevo
sudo mkdir -p /srv/datos
```
```text
# /etc/fstab
UUID=el-uuid-que-viste  /srv/datos  ext4  defaults,nofail,x-systemd.device-timeout=5  0  2
```
```bash
sudo findmnt -x            # valida fstab antes de reiniciar
sudo mount -a && df -h /srv/datos
```
⚠️ Un error en fstab puede dejar el equipo en modo emergencia: validá siempre con findmnt -x y tené la consola a mano.

**Regla para quedarse**
df para saber dónde, du para saber qué, y en fstab siempre UUID y nunca /dev/sdX.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- fstab, UUID, nofail y opciones de systemd: https://wiki.archlinux.org/title/Fstab
- Uso de disco, UUID y SMART en la Debian Reference: https://www.debian.org/doc/manuals/debian-reference/ch09.en.html
- /tmp en tmpfs y otros cambios de Ubuntu 26.04: https://computingforgeeks.com/ubuntu-2604-lts-features/
