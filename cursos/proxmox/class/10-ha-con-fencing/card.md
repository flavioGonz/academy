# Lección 10. HA con fencing

**Escuchá:** ha-con-fencing.mp3 (2 min)

**La idea, en tres líneas**
- La HA arranca en otro nodo lo que cayó, pero primero el nodo aislado se **reinicia solo por watchdog** (fencing), para que la VM nunca corra dos veces sobre el mismo disco.
- Requisitos: tres votos, almacenamiento compartido (o replicación ZFS) y hardware redundante.
- En Proxmox VE 9.2, antes de tocar red o corosync se **desarma la HA** y después se vuelve a armar.

**Impacto:** la HA hace lo que vendiste y un mantenimiento de red no reinicia el clúster entero.

**Quién lo dice:** 2 de 2 fuentes coinciden (evidencia fina: guía oficial y wiki de upgrade a 9); no se encontró quien discrepe.

**Laboratorio** · Campo · 15 min
En el clúster `lab` de la lección 9 (con QDevice), con la VM 100 en `pve1`:
1. Migración en vivo (si el disco es local, agregá `--with-local-disks`):
```bash
qm migrate 100 pve2 --online
```
2. Poné la VM bajo HA y mirá el estado:
```bash
ha-manager add vm:100
ha-manager status
```
3. Desarmá la HA como harías antes de tocar corosync, y mirá la línea de fencing:
```bash
ha-manager crm-command disarm-ha freeze
ha-manager status
```
4. Volvé a armar y confirmá:
```bash
ha-manager crm-command arm-ha
ha-manager status
```
5. Si el comando de desarme no existe, revisá con `pveversion` que estés en 9.2 o superior.

⚠️ Con almacenamiento local y sin replicación, la HA no puede recuperar la VM en otro nodo: el disco quedó en el nodo caído.

**Regla para quedarse**
Antes de tocar red o corosync en un clúster con HA, desarmo la HA.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Guía oficial: HA, fencing, disarm y migración: https://pve.proxmox.com/pve-docs/pve-admin-guide.html
- Migraciones y grupos de HA en el upgrade a 9: https://pve.proxmox.com/wiki/Upgrade_from_8_to_9
