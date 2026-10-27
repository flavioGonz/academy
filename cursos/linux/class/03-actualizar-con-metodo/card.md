# Lección 3. Actualizar con método

**Escuchá:** actualizar-con-metodo.mp3 (2 min)

**La idea, en tres líneas**
- `apt update` baja la lista, `apt upgrade` instala sin quitar nada; `apt full-upgrade` puede quitar paquetes y se planifica con backup.
- unattended-upgrades aplica solo seguridad una vez por día (instalado por defecto en Ubuntu; en Debian 13 se verifica y, si falta, se instala).
- El reinicio automático viene apagado: o lo fijás a una hora de madrugada, o reiniciás vos en una ventana.

**Impacto:** gateways, servidores y appliances con parches al día sin reinicios sorpresa en horario de uso.

**Quién lo dice:** 3 de 4 fuentes sobre paquetes y actualizaciones coinciden (Debian Handbook, documentación de Ubuntu Server, computingforgeeks). La propia doc de Ubuntu reconoce casos para no automatizar y prefiere bloquear paquetes puntuales antes que apagar todo.

**Laboratorio** · Admin · 15 min
En una VM de prueba:
1. Actualizá y mirá qué hay pendiente:
```bash
sudo apt update
apt-get -s upgrade | grep ^Inst     # -s simula, no instala
```
2. Instalá (si falta) y activá las actualizaciones automáticas; en Ubuntu ya vienen activas:
```bash
sudo apt install unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades
cat /etc/apt/apt.conf.d/20auto-upgrades   # ambos valores en "1"
```
3. Leé qué hizo y qué cambió:
```bash
sudo less /var/log/unattended-upgrades/unattended-upgrades.log
grep -A3 "Start-Date" /var/log/apt/history.log | tail -20
```
4. ¿Hay reinicio pendiente?
```bash
ls /var/run/reboot-required 2>/dev/null && cat /var/run/reboot-required.pkgs
```
5. Reinicio automático a hora fija, en un archivo propio:
```text
# /etc/apt/apt.conf.d/52reinicio-ies
Unattended-Upgrade::Automatic-Reboot "true";
Unattended-Upgrade::Automatic-Reboot-Time "04:30";
```
⚠️ En equipos que atienden gente de día (servidor de accesos, central IP), dejá Automatic-Reboot en "false" y reiniciá en una ventana acordada.

Versiones a octubre de 2026: Debian 13.7 (soporte regular hasta agosto de 2028), Ubuntu 26.04.1 LTS (hasta abril de 2031). En Debian, usá el nombre `trixie` en los repositorios y no `stable`, así no salta de versión solo.

**Regla para quedarse**
Seguridad automática todos los días, reinicio con hora, y el salto de versión mayor con backup.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Actualizaciones automáticas en Ubuntu Server (orígenes, reinicios, needrestart): https://documentation.ubuntu.com/server/how-to/software/automatic-updates/
- apt update, upgrade y full-upgrade en el Debian Handbook: https://debian-handbook.info/browse/stable/sect.apt-get.html
- Versiones de Debian y fechas de soporte: https://linuxize.com/post/debian-versions/
