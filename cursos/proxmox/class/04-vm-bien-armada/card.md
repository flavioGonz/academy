# Lección 4. VM bien armada

**Escuchá:** vm-bien-armada.mp3 (2 min)

**La idea, en tres líneas**
- Disco en **VirtIO SCSI single** con **IO Thread** y placa de red **VirtIO**: es lo que recomienda la guía oficial para rendimiento.
- **QEMU guest agent** activado en la VM e instalado adentro: apagado limpio y backups con el sistema de archivos congelado.
- En Windows, drivers **virtio-win** en la versión que la wiki de Proxmox marca sin problemas (0.1.271 a septiembre de 2026), no la última a ciegas.

**Impacto:** backups consistentes, apagados que no cuelgan y discos que rinden lo que el hardware da.

**Quién lo dice:** 3 de 4 fuentes coinciden en VirtIO y guest agent; el detalle de versiones de virtio-win viene solo de la wiki oficial.

**Laboratorio** · Foco · 15 min
1. Elegí una VM Linux de prueba (ID 100 en el ejemplo) y activá el agente:
```bash
qm set 100 --agent 1
```
2. Adentro de la VM (Debian o Ubuntu):
```bash
apt install qemu-guest-agent
systemctl start qemu-guest-agent
```
3. Apagá y prendé la VM desde Proxmox (el cambio de agente necesita un arranque nuevo).
4. Desde el host, probá que el agente responde y pedile las IPs:
```bash
qm agent 100 ping
qm agent 100 network-get-interfaces
```
5. Revisá en **Hardware** que el disco esté en `VirtIO SCSI single` y en **Options** que diga `QEMU Guest Agent: Enabled`.
6. Para Windows: subí el ISO de virtio-win a `local`, montalo como segundo CD y ejecutá `virtio-win-gt-x64` y después `virtio-win-guest-tools`.

⚠️ En un clúster, CPU tipo `host` puede impedir la migración en vivo entre nodos con procesadores distintos.

**Regla para quedarse**
Toda VM nace con VirtIO y guest agent, y el agente se prueba con un ping.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Qué hace el guest agent y cómo probarlo: https://pve.proxmox.com/wiki/Qemu-guest-agent
- Versiones de virtio-win y problemas conocidos: https://pve.proxmox.com/wiki/Windows_VirtIO_Drivers
- Guía oficial, controladoras de disco y tipo de CPU: https://pve.proxmox.com/pve-docs/pve-admin-guide.html
