# Lección 12. Plan de salida

**Escuchá:** plan-de-salida.mp3 (2 min)

**La idea, en tres líneas**
- Renovar o migrar se decide con números: núcleos físicos contra licenciables, funciones que se usan de verdad (vSAN, NSX, DRS) y un piloto en un host no crítico.
- Proxmox VE trae importador ESXi: se conecta directo al host (no a vCenter, que es mucho más lento), en frío y de a pocos discos a la vez.
- Antes de importar: desinstalar VMware Tools, anotar la configuración de red, preparar VirtIO en Windows y tener a mano las claves de BitLocker (el vTPM no se migra).

**Impacto:** le das al cliente un panorama honesto, con riesgos y tiempos reales, en vez de prometer una migración "de un día".

**Quién lo dice:** 3 de 4 fuentes de migración coinciden en el método; Broadcom recomienda pasar a VCF 9 o VVF 9, mientras Introserv y Redress sostienen que en 2 a 10 hosts de pocos núcleos la cuenta suele no cerrar.

**Laboratorio** · Campo · 20 min
En un Proxmox VE 8 o 9 de laboratorio y el ESXi de laboratorio de las lecciones anteriores:
1. En el ESXi, apagá una VM de prueba y desinstalale antes VMware Tools. Anotá IP, máscara, gateway y DNS.
2. En Proxmox: **Datacenter > Storage > Add > ESXi**. ID `esxi-lab`, servidor `192.168.88.20`, usuario `root` y su contraseña; marcá **Skip Certificate Verification** si el ESXi usa certificado autofirmado.
3. Seleccioná `esxi-lab` en el árbol, elegí la VM y tocá **Import**. Elegí storage de destino y bridge (`vmbr0`). En **Advanced**, revisá disco y placa de red.
4. Arrancá la VM. Si es Linux y no bootea con VirtIO SCSI, probá el disco en SATA. Si es Windows, arrancá con SATA, instalá los drivers VirtIO y después cambiá.
5. Verificá desde la consola de la VM:
```bash
ip a
ping -c 3 192.168.88.1
```
6. Reconfigurá la IP si la placa cambió de nombre, e instalá el agente QEMU.

⚠️ La VM nunca debe quedar encendida en VMware y en Proxmox a la vez. Antes de migrar producción: backup verificado (lección 7) y plan de vuelta atrás.

**Regla para quedarse**
Ninguna migración arranca sin piloto, backup verificado y vuelta atrás.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Guía oficial de migración a Proxmox VE e importador ESXi: https://pve.proxmox.com/wiki/Migrate_to_Proxmox_VE
- Importador paso a paso y tareas posteriores (Thomas-Krenn): https://www.thomas-krenn.com/en/wiki/ESXi_VM_importer_-_Proxmox_VE_Storage_Plugin
- Cuándo conviene renovar y cuándo migrar, con cuentas de núcleos: https://introserv.com/blog/migrating-from-vmware-in-2026-the-end-of-perpetual-licenses-vsphere-8-end-of-support-and-replacement-options/
- El retiro del VDDK y su impacto en herramientas de migración: https://www.virtualizationhowto.com/2026/09/leaving-vmware-just-got-harder-after-broadcom-pulled-vddk-downloads/
