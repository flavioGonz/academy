# Lección 5. VMs bien armadas

**Escuchá:** vms-bien-armadas.mp3 (2 min)

**La idea, en tres líneas**
- Los appliances que mandan los fabricantes (.ova, .ovf) entran por **Deploy OVF Template**, no copiando el archivo al datastore.
- VMware Tools siempre instalado y al día: driver de balloon, snapshots con quiesce y latido para HA.
- Discos: thick lazy zeroed, thick eager zeroed (para Fault Tolerance) y thin. Thin puede crecer hasta llenar el datastore y, si se llena, la VM se detiene.

**Impacto:** menos llamados por VMs colgadas por datastore lleno y appliances que se instalan bien a la primera.

**Quién lo dice:** 3 de 4 fuentes sobre VMs coinciden en VMware Tools; 2 de 4 en vigilar el espacio con thin provisioning. Sin discrepancias.

**Laboratorio** · Rápido · 10 min
Por SSH en un ESXi de laboratorio:
```bash
# listar VMs con su Vmid
vim-cmd vmsvc/getallvms

# estado de VMware Tools de una VM (reemplazá 1 por el Vmid)
vim-cmd vmsvc/get.guest 1 | grep -i toolsRunningStatus
vim-cmd vmsvc/get.guest 1 | grep -i toolsVersionStatus

# espacio total y libre de cada datastore
esxcli storage filesystem list

# tamaño real ocupado por los discos de una VM
du -h /vmfs/volumes/datastore1/vm-prueba/*-flat.vmdk
ls -lh /vmfs/volumes/datastore1/vm-prueba/*-flat.vmdk
```
`ls -lh` muestra el tamaño provisionado y `du -h` lo realmente ocupado: la diferencia es lo que todavía puede crecer. Sumalo por datastore y comparalo con el libre.

**Regla para quedarse**
Ninguna VM queda en producción sin VMware Tools y sin saber cuánto puede crecer su disco.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Thin, thick lazy y thick eager (Broadcom TechDocs): https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-virtual-machine-administration/configuring-virtual-machine-hardwarevsphere-vm-admin/virtual-disk-configurationvsphere-vm-admin/about-virtual-disk-provisioning-policiesvsphere-vm-admin.html
- Formas de crear VMs y Deploy OVF Template: https://open-exam-prep.com/study-guides/vcp-dcv/lifecycle-management-configuration/vm-snapshots-management
- Balloon y VMware Tools en esxtop (KB de Broadcom): https://knowledge.broadcom.com/external/article/382249/using-esxtop-and-interpreting-esxtop-sta.html
