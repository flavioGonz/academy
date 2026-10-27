# Lección 10. Parches sin sustos

**Escuchá:** parches-sin-sustos.mp3 (2 min)

**La idea, en tres líneas**
- vSphere Lifecycle Manager (vLCM) vive dentro de vCenter: compliance check, remediation pre-check, staging y remediation.
- El staging baja los paquetes antes, para que el host pase menos tiempo en modo mantenimiento. En vSphere 9 se retiran las baselines y queda el modelo de imágenes.
- Host suelto: modo mantenimiento y esxcli con el depot zip. Rollback de 8 a 7 solo si no se tocaron los bootbanks. Antes de actualizar, backup. Siempre.

**Impacto:** ventanas de mantenimiento más cortas y ningún host que queda a medio actualizar sin plan de vuelta.

**Quién lo dice:** 3 de 4 fuentes sobre parches coinciden en el ciclo de vLCM con imágenes; sin discrepancias.

**Laboratorio** · Admin · 15 min
En un ESXi de laboratorio, con el parche oficial (depot .zip descargado del Broadcom Support Portal con la cuenta del cliente) copiado a `datastore1`:
```bash
# versión actual
vmware -vl

# apagar o mover las VMs y entrar en mantenimiento
esxcli system maintenanceMode set -e true
esxcli system maintenanceMode get

# ver qué perfiles trae el depot y qué paquetes incluye uno
esxcli software sources profile list -d /vmfs/volumes/datastore1/VMware-ESXi-8.0U3-depot.zip
esxcli software sources profile get -d /vmfs/volumes/datastore1/VMware-ESXi-8.0U3-depot.zip -p ESXi-8.0U3-standard

# comparar con lo instalado hoy
esxcli software profile get
esxcli software vib list | head -n 20

# simular la actualización sin aplicar nada
esxcli software profile update -d /vmfs/volumes/datastore1/VMware-ESXi-8.0U3-depot.zip -p ESXi-8.0U3-standard --dry-run

# aplicar (solo en el host de laboratorio) y reiniciar
esxcli software profile update -d /vmfs/volumes/datastore1/VMware-ESXi-8.0U3-depot.zip -p ESXi-8.0U3-standard
reboot

# después del reinicio: verificar y salir de mantenimiento
vmware -vl
esxcli system maintenanceMode set -e false
```
Con vCenter: **Cluster > Updates > Image**, botón **Check Compliance**, después **Run Pre-check** y **Stage**.

⚠️ Antes de actualizar en producción: backup del vCenter, de la configuración del host y de las VMs críticas, y la Compatibility Guide revisada para la versión de destino.

**Regla para quedarse**
Antes de actualizar, backup. Siempre. Y el host entra en modo mantenimiento antes que el parche.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Qué es vSphere Lifecycle Manager y sus operaciones (Broadcom TechDocs): https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/managing-host-and-cluster-lifecycle/about-vsphere-lifecycle-manager-new.html
- Cambios de vLCM en vSphere 9: https://www.starwindsoftware.com/blog/vmware-cloud-foundation-vcf-9-0-with-vsphere-9-0-and-esxi-9-0-has-been-released/
- Rollback y reparticionado del arranque al actualizar a ESXi 8: https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/esx-installation-and-setup/installing-and-setting-up-esxi-install/esxi-requirements-install/esxi-hardware-requirements-install.html
