# Lección 6. Snapshots con fecha

**Escuchá:** snapshots-con-fecha.mp3 (2 min)

**La idea, en tres líneas**
- Un snapshot no es backup: congela el disco base y escribe los cambios en un delta (-00000N.vmdk) que depende del original.
- Según la KB de Broadcom: hasta 32 en cadena como máximo técnico, pero 2 o 3 en la práctica, y ninguno más de 72 horas.
- No agrandes discos con snapshots vivos ni canceles una consolidación en curso. Los snapshots de los backups fallidos pueden no verse en el Snapshot Manager.

**Impacto:** se terminan los datastores llenos y las VMs lentas por snapshots olvidados.

**Quién lo dice:** 3 de 3 fuentes sobre snapshots coinciden; CloudBolt es más estricta y sugiere 24 a 72 horas en vez de 72.

**Laboratorio** · Rápido · 10 min
En un ESXi de laboratorio, con una VM de prueba (Vmid 1 en el ejemplo):
```bash
# crear un snapshot con fecha de borrado en el nombre (sin memoria, sin quiesce)
vim-cmd vmsvc/snapshot.create 1 "borrar-2026-10-30-antes-update" "prueba lab" 0 0

# ver el árbol de snapshots
vim-cmd vmsvc/snapshot.get 1

# ver el delta en el datastore
ls -lh /vmfs/volumes/datastore1/vm-prueba/

# borrar todos los snapshots (consolida en el disco base)
vim-cmd vmsvc/snapshot.removeall 1

# buscar deltas huérfanos en todo el datastore
find /vmfs/volumes/datastore1/ -name "*-0000*.vmdk"
```
Con vCenter, lo mismo con PowerCLI para todo el inventario:
```powershell
Get-VM | Get-Snapshot | Where {$_.Created -lt (Get-Date).AddDays(-3)} | Select VM, Name, Created, SizeGB
```
⚠️ En producción, no canceles una tarea de borrado o consolidación de snapshot: puede corromper el disco.

**Regla para quedarse**
Todo snapshot que saco lleva la fecha de borrado en el nombre y se borra antes de 72 horas.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Buenas prácticas oficiales de snapshots (KB de Broadcom): https://knowledge.broadcom.com/external/article/318825/best-practices-for-using-vmware-snapshot.html
- Archivos del snapshot, alarmas y PowerCLI: https://www.cloudbolt.io/vmware-administration/vmware-snapshot-best-practices/
- El caso "consolidation is needed" tras backups: https://open-exam-prep.com/study-guides/vcp-dcv/lifecycle-management-configuration/vm-snapshots-management
