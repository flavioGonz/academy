# Lección 12. Upgrade y rescate

**Escuchá:** upgrade-y-rescate.mp3 (2 min)

**La idea, en tres líneas**
- Upgrade mayor (8 a 9): backup probado, `pve8to9 --full` antes, durante y después, consola por SSH con tmux o IPMI (no la consola de la GUI), y un nodo por vez.
- En Proxmox VE 9, `/etc/sysctl.conf` ya no se lee: los ajustes van en `/etc/sysctl.d/`.
- Diagnóstico en orden: quórum, logs, locks, almacenamiento (y firewall si hay sospecha).

**Impacto:** upgrades sin sustos y un primer diagnóstico en cinco minutos en vez de una mañana.

**Quién lo dice:** 5 de 7 fuentes coinciden en el procedimiento de upgrade; 3 de 4 en los pasos de diagnóstico; no se encontró quien discrepe.

**Laboratorio** · Admin · 15 min
Armá tu hoja de diagnóstico corriendo esto en el nodo de prueba y anotando cómo se ve sano:
1. Versión y quórum:
```bash
pveversion
pvecm status
```
2. Logs del último arranque de los servicios clave:
```bash
journalctl -b -u corosync | tail -20
journalctl -b -u pve-cluster | tail -20
```
3. Locks: mirá si alguna VM quedó con `lock:` en su configuración y destrabala (ejemplo VM 100):
```bash
grep -l '^lock:' /etc/pve/qemu-server/*.conf
qm unlock 100
```
4. Almacenamiento y firewall:
```bash
pvesm status
pve-firewall status
```
5. Si el host viene de la 8, buscá ajustes que se pierden en la 9:
```bash
cat /etc/sysctl.conf | grep -v '^#' | grep .
ls /etc/sysctl.d/
```
6. En un nodo que todavía esté en 8.4, el chequeo previo es:
```bash
pve8to9 --full
```

⚠️ `qm unlock` solo después de confirmar que no hay un backup, snapshot o migración en curso sobre esa VM.

**Regla para quedarse**
Upgrade mayor: backup probado, checklist limpio, consola fuera de la GUI, un nodo por vez.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Guía oficial de upgrade de 8 a 9, con problemas conocidos: https://pve.proxmox.com/wiki/Upgrade_from_8_to_9
- Curso de partner con escenarios de romper y arreglar en PVE 9: https://www.flane.de/course/innovator-pveicm
- Guía oficial, locks y diagnóstico de clúster: https://pve.proxmox.com/pve-docs/pve-admin-guide.html
