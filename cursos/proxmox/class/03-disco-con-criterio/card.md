# Lección 3. Disco con criterio

**Escuchá:** disco-con-criterio.mp3 (2 min)

**La idea, en tres líneas**
- Instalar con ext4 o xfs deja **LVM-thin** (`local-lvm`): simple, rápido, con snapshots, y solo ocupa lo que se escribe.
- **ZFS** suma integridad, compresión, RAID por software y replicación, pero pide RAM (8 GB para arrancar, según la guía), ECC recomendada y discos directos por HBA.
- ZFS **nunca** encima de una controladora RAID por hardware con caché.

**Impacto:** elegís el almacenamiento una vez y bien, en vez de migrar VMs cuando el servidor ya está en producción.

**Quién lo dice:** las 2 fuentes que tratan el tema coinciden en lo básico (evidencia fina); el foro de Proxmox dice que la regla de 1 GB de RAM por TB es falsa y que ZFS gasta más los SSD de consumo.

**Laboratorio** · Rápido · 10 min
1. Mirá qué almacenamientos tiene el nodo y cuánto usan:
```bash
pvesm status
```
2. Si es LVM-thin, mirá el pool `data` y el uso real de cada disco de VM:
```bash
lvs
```
3. Si es ZFS, mirá la salud del pool y el límite de memoria del ARC (en bytes):
```bash
zpool status
cat /sys/module/zfs/parameters/zfs_arc_max
cat /etc/modprobe.d/zfs.conf
```
4. Calculá la regla oficial: 2 GiB base más 1 GiB por TiB de pool. Compará con lo configurado.
5. Mirá en **Datacenter → Storage** qué tipo es cada uno y qué contenido acepta (imágenes, ISO, backups).

⚠️ Cambiar el límite del ARC en un servidor en producción se hace con cuidado: con poca caché, el disco rinde menos.

**Regla para quedarse**
ZFS con discos directos y RAM de sobra; si no, LVM-thin; nunca ZFS sobre RAID por hardware.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Guía oficial: requisitos de hardware, ZFS y LVM-thin: https://pve.proxmox.com/pve-docs/pve-admin-guide.html
- Discusión del foro sobre ZFS en SSD de consumo: https://forum.proxmox.com/threads/filesystem-choice-for-consumer-ssd.181212/
