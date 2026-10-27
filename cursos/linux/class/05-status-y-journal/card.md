# Lección 5. Status y journal

**Escuchá:** status-y-journal.mp3 (2 min)

**La idea, en tres líneas**
- `systemctl status servicio` primero: estado, desde cuándo y últimas líneas de log; después `journalctl -u servicio` para el log completo.
- `start` lo levanta ahora; `enable` hace que arranque en el próximo booteo. Son cosas distintas.
- `journalctl -b -1` muestra el arranque anterior: lo que pasó antes de un corte o reinicio.

**Impacto:** diagnosticás un servicio caído leyendo el error real en vez de reiniciar a ciegas, y evitás servicios que no vuelven tras un corte de luz.

**Quién lo dice:** 5 de 6 fuentes sobre logs coinciden (Debian Handbook, Debian Reference, Ubuntu Server, phoenixNAP, trstringer); en systemd, 2 de 2. Ninguna discrepa.

**Laboratorio** · Rápido · 10 min
En una VM con Debian 13 o Ubuntu, con la consola abierta:
1. Estado y si arranca al bootear:
```bash
systemctl status ssh
systemctl is-enabled ssh
systemctl list-units | grep -i failed
```
2. Rompé la configuración a propósito y mirá el error (en la consola de la VM, no por SSH):
```bash
echo "PasswordAuthentication yess" | sudo tee /etc/ssh/sshd_config.d/99-roto.conf
sudo systemctl restart ssh
systemctl status ssh
sudo journalctl -u ssh -n 20
```
3. Arreglá y verificá:
```bash
sudo rm /etc/ssh/sshd_config.d/99-roto.conf
sudo systemctl restart ssh && systemctl status ssh
```
4. Filtros de journalctl para obra:
```bash
sudo journalctl -b -1 -p err      # errores del arranque anterior
sudo journalctl -u ssh -S "1 hour ago"
sudo journalctl -f                 # en vivo, Ctrl+C para salir
sudo du -sh /var/log/journal     # tamaño del journal
```
⚠️ Hacé el paso 2 en una VM de laboratorio y desde la consola: en un servidor remoto te deja sin SSH.

**Regla para quedarse**
Status, journal, arreglo, status otra vez; y todo servicio que tiene que volver tras un corte, con enable.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- systemd, unidades y el ejemplo del "yess" en el Debian Handbook: https://debian-handbook.info/browse/stable/unix-services.html
- Opciones de journalctl con ejemplos: https://phoenixnap.com/kb/journalctl-systemd-logs
