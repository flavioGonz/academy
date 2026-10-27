# Lección 7. Backup que restaura

**Escuchá:** backup-que-restaura.mp3 (2 min)

**La idea, en tres líneas**
- `vzdump` hace backups **completos** (configuración y discos). Modo **snapshot** con guest agent para no cortar; modo **stop** cuando la consistencia manda.
- Un **snapshot de la VM** no es un backup: vive en el mismo disco y sirve para deshacer un cambio.
- Un backup cuenta cuando lo **restauraste en una VM nueva**, nunca encima de la que está en producción.

**Impacto:** cuando un cliente pierde un servidor, ya sabés cuánto tarda la restauración y que funciona.

**Quién lo dice:** 3 de 3 fuentes que tratan la restauración coinciden en probarla; ninguna discrepa.

**Laboratorio** · Foco · 15 min
1. Backup de la VM de prueba (ID 100) al almacenamiento `local`:
```bash
vzdump 100 --mode snapshot --compress zstd --storage local
ls /var/lib/vz/dump/
```
2. Restaurá con otro ID (cambiá el nombre por el archivo que generó el paso 1):
```bash
qmrestore /var/lib/vz/dump/vzdump-qemu-100-<fecha>.vma.zst 900
```
3. Antes de arrancar, desconectá la placa para que no choque con la original:
```bash
qm set 900 --net0 virtio,bridge=vmbr0,link_down=1
qm start 900
```
4. Entrá por la consola, verificá que el sistema y los datos estén. Anotá cuánto tardó la restauración.
5. Borrá la VM de prueba: `qm stop 900 && qm destroy 900`.

⚠️ Restaurar encima de una VM existente (mismo ID) borra sus discos actuales. En producción, siempre a un ID nuevo.

**Regla para quedarse**
Ningún backup cuenta hasta que lo restauré en una VM nueva.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Guía oficial, modos de backup, live-restore y fleecing: https://pve.proxmox.com/pve-docs/pve-admin-guide.html
- Pruebas de restauración y regla 3-2-1 en PBS: https://pbs.proxmox.com/docs/storage.html
- Cómo actúa el guest agent en el backup: https://pve.proxmox.com/wiki/Qemu-guest-agent
