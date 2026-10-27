# Lección 9. Tres votos

**Escuchá:** tres-votos.mp3 (2 min)

**La idea, en tres líneas**
- Quórum es mayoría: cada nodo tiene un voto y sin mayoría el clúster queda en **solo lectura**.
- Dos nodos solos no hacen alta disponibilidad: si cae uno, el otro tiene un voto de dos. La solución es un **QDevice** en un tercer equipo.
- Corosync quiere menos de 5 ms entre nodos, red propia y un segundo enlace; el QDevice va por TCP y puede estar fuera de la LAN.

**Impacto:** no vendés un clúster que en la primera falla real se queda quieto.

**Quién lo dice:** 2 de 2 fuentes coinciden (evidencia fina: guía oficial y un hilo del foro de marzo de 2026); no se encontró quien discrepe.

**Laboratorio** · Campo · 20 min
Con dos Proxmox VE 9 anidados (`pve1` 10.10.10.11 y `pve2` 10.10.10.12, rango de documentación), sin VMs en `pve2`:
1. En `pve1`:
```bash
pvecm create lab
pvecm status
```
2. En `pve2` (pide la contraseña de root de `pve1`):
```bash
pvecm add 10.10.10.11
```
3. Mirá `pvecm status` en los dos: `Expected votes: 2`, `Quorate: Yes`.
4. Apagá `pve2`. En `pve1` corré `pvecm status` y fijate `Quorate`. Probá crear una VM: no te deja.
5. Prendé `pve2`. En una tercera máquina Debian (10.10.10.13):
```bash
apt install corosync-qnetd
```
En los dos nodos:
```bash
apt install corosync-qdevice
```
Y en `pve1`:
```bash
pvecm qdevice setup 10.10.10.13
pvecm status
```
6. Repetí el paso 4: ahora `pve1` conserva el quórum con el voto del QDevice.

⚠️ Un nodo que se une a un clúster no puede tener VMs (los IDs chocarían). Antes de unirlo, vacialo.

**Regla para quedarse**
Nunca entrego un clúster de dos nodos sin QDevice.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Guía oficial: quórum, red de clúster y QDevice: https://pve.proxmox.com/pve-docs/pve-admin-guide.html
- El hilo del foro sobre dos nodos y QDevice remoto: https://forum.proxmox.com/threads/2-nodes-proxmox-cluster-qdevice.181580/
