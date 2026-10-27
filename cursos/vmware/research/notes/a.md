# Notes: batch a
Pages read: 30. With notes: 30. Skipped: 0. (Se descartaron antes de la lista final: un FAQ de un revendedor de hardware con fechas de soporte erróneas, un post de foro duplicado con el wiki de Proxmox, un post de William Lam sobre VCF 9.1.1 demasiado avanzado para el nivel y un artículo general de tendencias.)

## T01 Licenciamiento y ciclo de vida post-Broadcom
- a:N1. Desde el 1 de febrero de 2024 todo producto VMware nuevo se vende por suscripción (1, 3 o 5 años); las licencias perpetuas dejaron de venderse y no se puede extender su mantenimiento. vCenter ya no se vende aparte: viene incluido en cada suscripción.
  - Source: https://thomas-krenn.com/en/wiki/VMware_license_model_by_Broadcom  Quote: "The vCenter is no longer a separate product, but is included in all licenses."
  - Kind: definition
  - Level: foundation
  - Bias: Thomas-Krenn vende servidores, incluidos con VMware y Proxmox.
- a:N2. Se cobra por núcleo físico con mínimo de 16 núcleos por CPU. Ejemplo de la KB 313548 citada: tres hosts con una CPU de 8 núcleos son 24 núcleos físicos pero se licencian 48 (su afirmación sobre la tabla de Broadcom).
  - Source: https://introserv.com/blog/migrating-from-vmware-in-2026-the-end-of-perpetual-licenses-vsphere-8-end-of-support-and-replacement-options/  Quote: "You pay for twice as many cores as you own."
  - Kind: number
  - Level: foundation
  - Bias: Introserv vende servidores para migrar a Proxmox/XCP-ng.
- a:N3. Oferta vigente a 2026: VVF (vSphere Foundation: vSphere, VKS, VCF Operations, vSAN base de 0,25 TiB por núcleo), VCF (stack completo con NSX, vSAN 1 TiB por núcleo, HCX, Automation) y VCF Edge (mínimo 10 sitios, 8 núcleos por CPU). vSphere Standard y Enterprise Plus solo llegan hasta 8.0 Update 3; las capacidades 9.1 solo existen en VVF y VCF (su lectura de documentos oficiales).
  - Source: https://introserv.com/blog/migrating-from-vmware-in-2026-the-end-of-perpetual-licenses-vsphere-8-end-of-support-and-replacement-options/  Quote: "vSphere Standard and vSphere Enterprise Plus are available only up to the 8 Update 3 release"
  - Kind: definition
  - Level: foundation
  - Bias: vendedor de alternativas.
- a:N4. Productos discontinuados: vSphere Essentials, Essentials Plus (venta cortada en abril 2025, contratos vigentes no se renuevan), kits ROBO y el hipervisor gratuito original. Enterprise Plus volvió como suscripción en noviembre 2024.
  - Source: https://thomas-krenn.com/en/wiki/VMware_license_model_by_Broadcom  Quote: "Broadcom has discontinued the sale of VVEP."
  - Kind: definition
  - Level: foundation
- a:N5. El aumento de costo pegó más fuerte en clientes chicos que solo usaban el hipervisor: según Redress, entre 2 y 5 veces el costo anual; en 22 de 35 renovaciones revisadas la discusión del descuento tapó el conteo de núcleos (sus cifras).
  - Source: https://redresscompliance.com/vcf-licensing-guide-2026.html  Quote: "annual cost rose 2 to 5 times"
  - Kind: number
  - Level: core
  - Bias: Redress vende servicios de negociación a compradores.
- a:N6. Para contar núcleos licenciables: RVTools (pestaña vHost) y los scripts PowerCLI oficiales de la KB 313548; los núcleos deshabilitados en BIOS no se aceptan como reducción salvo acuerdo por escrito.
  - Source: https://redresscompliance.com/vcf-licensing-guide-2026.html  Quote: "Do not rely on disabled cores to lower the count"
  - Kind: technique
  - Level: core
  - Also: T14
- a:N7. ESXi gratuito volvió con ESXi 8.0 Update 3e (abril 2025), descargable del Broadcom Support Portal en "Free Software Downloads". Límites según la KB: no se gestiona con vCenter, sin vMotion/HA/DRS, sin backups VADP, APIs solo lectura, máximo 2 CPU físicas por host y 8 vCPU por VM, sin soporte oficial. Uso pensado: laboratorio y pruebas.
  - Source: https://knowledge.broadcom.com/external/article/399823/vmware-esxi-80-update-3e-now-available-a.html  Quote: "Cannot be managed by vCenter Server"
  - Kind: definition
  - Level: foundation
  - Also: T12
- a:N8. Practicante francés celebra la vuelta del ESXi gratis pero avisa que Broadcom cambia rápido y puede revertirlo; recuerda que el anuncio fue una sola frase en las release notes.
  - Source: https://www.it-connect.fr/la-version-gratuite-de-vmware-esxi-free-est-de-retour-en-2025/  Quote: "un revirement de situation n'est pas impossible"
  - Kind: story
  - Level: foundation
- a:N9. El ESXi gratuito no sirve para backup a nivel host con herramientas de terceros porque no expone VADP; con 8 vCPU por VM como tope.
  - Source: https://phoenixnap.com/kb/vmware-esxi  Quote: "preventing host-level backup using third-party tools"
  - Kind: mistake
  - Level: foundation
  - Also: T12
  - Bias: phoenixNAP vende servidores bare metal.
- a:N10. Fin de soporte general de vSphere 8 (ESXi 8.x, vCenter 8.x, vSAN 8.x): 11 de octubre de 2027. Después no hay soporte técnico ni parches. Broadcom recomienda VCF 9 o VVF 9.
  - Source: https://knowledge.broadcom.com/external/article/456708/upcoming-end-of-service-for-vsphere-8-vs.html  Quote: "there will be no Technical Support and no new patches"
  - Kind: number
  - Level: foundation
- a:N11. vSphere 7 terminó soporte general el 2 de octubre de 2025. Los parches zero-day gratuitos (CVSS 9.0 o más) solo cubren versiones soportadas; no dan drivers ni soporte. Para pasar a versión 9 con licencias perpetuas primero hay que pasar a suscripción (según la FAQ de VCF 9.1 que citan).
  - Source: https://introserv.com/blog/migrating-from-vmware-in-2026-the-end-of-perpetual-licenses-vsphere-8-end-of-support-and-replacement-options/  Quote: "customers with perpetual licenses must first move to a subscription to upgrade to version 9"
  - Kind: rule of thumb
  - Level: core
- a:N12. VCF 9.0 salió GA el 17 de junio de 2025, con ESXi 9.0 y vCenter 9.0; trae NVMe Tiering de memoria, live patching ampliado y vLCM que retira las baselines.
  - Source: https://www.starwindsoftware.com/blog/vmware-cloud-foundation-vcf-9-0-with-vsphere-9-0-and-esxi-9-0-has-been-released/  Quote: "hitting general availability on June 17, 2025"
  - Kind: definition
  - Level: core
  - Also: T13
  - Bias: StarWind vende vSAN alternativo.

- a:N14. VCF 9 introduce una licencia por defecto por producto que se puede dividir; consultas de licencias se abren como caso "Non Technical" en Broadcom Support.
  - Source: https://blogs.vmware.com/cloud-foundation/2026/02/06/global-supports-vmware-cloud-foundation-9-paths-to-adoption  Quote: "the Non Technical category must be selected"
  - Kind: technique
  - Level: core

## T02 Hardware y compatibilidad
- a:N15. ESXi 8.0 pide al menos 2 núcleos, NX/XD habilitado en BIOS, VT-x o AMD-V, 8 GB de RAM (12 GB recomendado para producción), una NIC gigabit soportada y disco de arranque de 32 GB; recomienda arranque UEFI.
  - Source: https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/esx-installation-and-setup/installing-and-setting-up-esxi-install/esxi-requirements-install/esxi-hardware-requirements-install.html  Quote: "ESXi 8.0 requires a minimum of 8 GB of physical RAM."
  - Kind: number
  - Level: foundation
  - Also: T03
- a:N16. SD y USB quedan solo para particiones de arranque; OSDATA en SD/USB está en deprecación. Lo óptimo es un disco local persistente de 128 GB, idealmente RAID 1. Sin disco persistente aparece la alarma "Secondary persistent device not found".
  - Source: https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/esx-installation-and-setup/installing-and-setting-up-esxi-install/esxi-requirements-install/esxi-hardware-requirements-install.html  Quote: "Secondary persistent device not found"
  - Kind: rule of thumb
  - Level: foundation
- a:N17. ESXi 8 dejó fuera CPUs viejas (Sandy Bridge, Ivy Bridge, Haswell, Broadwell-DT) y NICs como Mellanox ConnectX-3. Truco no invasivo: bootear el instalador desde USB y ver si detecta todo, sin instalar.
  - Source: https://williamlam.com/2022/09/homelab-considerations-for-vsphere-8.html  Quote: "You do NOT have to perform an installation to check for compatibility"
  - Kind: technique
  - Level: foundation
  - Bias: autor empleado de VMware/Broadcom; el texto es para homelab.
- a:N18. ESXi 9.0 deja sin soporte Broadwell-EP, Kaby Lake-S y Skylake (D, S, SP, W). La opción allowLegacyCPU=true convierte el error en advertencia pero deja la instalación sin soporte: solo para laboratorio.
  - Source: https://williamlam.com/2025/06/ultimate-lab-resource-for-vcf-9-0.html  Quote: "knowing that the CPU is NOT officially supported"
  - Kind: mistake
  - Level: core
- a:N19. La HCL (hoy Broadcom Compatibility Guide) es la única forma de tener configuración soportada; revisar release notes antes de cada versión.
  - Source: https://williamlam.com/2022/09/homelab-considerations-for-vsphere-8.html  Quote: "This is the only way to ensure that you will have the best possible experience"
  - Kind: rule of thumb
  - Level: foundation


## T03 Instalación de ESXi y configuración inicial
- a:N21. Pasos de instalación: bajar ISO del Broadcom Support Portal, bootear (USB o iDRAC/iLO), aceptar EULA con F11, elegir disco, root password, reiniciar. Luego en DCUI con F2: Configure Management Network, IPv4 estática, DNS y hostname, y entrar al Host Client por la IP.
  - Source: https://phoenixnap.com/kb/vmware-esxi  Quote: "Change the setting from Dynamic to Static mode."
  - Kind: template
  - Level: foundation
  - Also: T04

## T04 Host Client
- a:N22. El Host Client permite editar port groups y VLAN sin vCenter: Networking, el vSwitch, el port group, Edit Settings. Con licencia gratuita es la única consola de gestión.
  - Source: https://knowledge.broadcom.com/external/article/311057/configuring-vlan-on-a-vswitch-standard.html  Quote: "Log into the ESXi host client with root credentials"
  - Kind: technique
  - Level: foundation
  - Also: T05

## T05 Redes estándar
- a:N23. VLAN en port group: VLAN ID 0 es sin etiqueta (VLAN nativa del switch físico). Por CLI: esxcfg-vswitch -l para ver, esxcfg-vswitch -p "VM Network" -v 111 vSwitch0 para etiquetar.
  - Source: https://knowledge.broadcom.com/external/article/311057/configuring-vlan-on-a-vswitch-standard.html  Quote: "enter 0 for no VLAN"
  - Kind: technique
  - Level: foundation
- a:N24. Cambiar la VLAN del port group de gestión desde el vSphere Client o SSH puede dejarte sin acceso al host; conviene hacerlo desde consola remota (iLO, iDRAC) o física.
  - Source: https://knowledge.broadcom.com/external/article/311057/configuring-vlan-on-a-vswitch-standard.html  Quote: "may cause the host to lose management network connectivity"
  - Kind: mistake
  - Level: foundation
  - Also: T15
- a:N25. Cada vSwitch se mapea a uno o más uplinks físicos; NIC teaming da balanceo y failover; los port groups llevan VLAN ID para separar gestión, vMotion, almacenamiento y VMs.
  - Source: https://phoenixnap.com/kb/vmware-esxi  Quote: "Assign VLAN IDs to port groups to segment network traffic"
  - Kind: technique
  - Level: foundation
  - Also: T06

## T06 VMkernel
- a:N26. Un adaptador VMkernel (vmk) por tipo de tráfico: gestión, vMotion, almacenamiento IP, FT, replicación, vSAN, backup NFC. La instalación crea un vSwitch estándar con un vmk de gestión; para redundancia, dos NICs físicas al vmk de gestión.
  - Source: https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-networking/setting-up-vmkernel-networking/the-vmkernel-networking-layer.html  Quote: "Dedicate a separate VMkernel adapter for every traffic type"
  - Kind: rule of thumb
  - Level: foundation
- a:N27. El tráfico de vMotion no va cifrado: va en red privada aislada solo con los hosts. Varios vmk en la misma subred dentro de una pila no está soportado (salvo iSCSI, multi-NIC vMotion).
  - Source: https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-networking/setting-up-vmkernel-networking/the-vmkernel-networking-layer.html  Quote: "vMotion network traffic is not encrypted."
  - Kind: mistake
  - Level: core
  - Also: T11

## T07 Almacenamiento
- a:N28. Para iSCSI: Software iSCSI Adapter sobre vmk dedicado, jumbo frames MTU 9000 de punta a punta (vmk y switches); NFS se monta desde el Host Client. VMFS para LUNs locales o SAN.
  - Source: https://phoenixnap.com/kb/vmware-esxi  Quote: "Enable Jumbo Frames (MTU 9000) on the VMkernel port and the physical network"
  - Kind: technique
  - Level: core
  - Also: T06
- a:N29. NFS e iSCSI por software dependen de la red VMkernel; ESXi soporta NFS 3 y 4.1; con dos NICs para iSCSI se arma multipathing.
  - Source: https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-networking/setting-up-vmkernel-networking/the-vmkernel-networking-layer.html  Quote: "If you have two or more physical NICs for iSCSI, you can configure iSCSI multipathing."
  - Kind: definition
  - Level: core

## T08 Máquinas virtuales
- a:N30. Tres formatos de disco: thick lazy zeroed (reserva al crear, pone en cero al primer uso), thick eager zeroed (pone en cero al crear, necesario para FT), thin (crece a demanda). Thin permite sobreasignar; si el datastore se llena con la VM corriendo, la VM se detiene.
  - Source: https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-virtual-machine-administration/configuring-virtual-machine-hardwarevsphere-vm-admin/virtual-disk-configurationvsphere-vm-admin/about-virtual-disk-provisioning-policiesvsphere-vm-admin.html  Quote: "it can grow to its maximum capacity and occupy the entire datastore space"
  - Kind: definition
  - Level: foundation
- a:N31. Se puede pasar un disco de thin a thick (o al revés) con Storage vMotion. En NFS sin aceleración por hardware solo existe thin.
  - Source: https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-virtual-machine-administration/configuring-virtual-machine-hardwarevsphere-vm-admin/virtual-disk-configurationvsphere-vm-admin/about-virtual-disk-provisioning-policiesvsphere-vm-admin.html  Quote: "only thin format is available"
  - Kind: technique
  - Level: core
- a:N32. Formas de crear VMs: asistente, clonar, desde plantilla, Deploy OVF Template (un .ova de un fabricante va por este asistente, no registrando el archivo), content library, registrar un .vmx existente.
  - Source: https://open-exam-prep.com/study-guides/vcp-dcv/lifecycle-management-configuration/vm-snapshots-management  Quote: "Use the Deploy OVF Template wizard and select the .ova file"
  - Kind: technique
  - Level: foundation
- a:N33. VMware Tools trae el driver de balloon; si MCTL? en esxtop dice que no está, falta instalar Tools. Tools también es requisito para quiesce y para el heartbeat de VM Monitoring de HA.
  - Source: https://knowledge.broadcom.com/external/article/382249/using-esxtop-and-interpreting-esxtop-sta.html  Quote: "If not, install VMware tools which contains the balloon driver."
  - Kind: rule of thumb
  - Level: foundation
  - Also: T15
- a:N34. vSphere 9 usa hardware virtual versión 22.
  - Source: https://www.starwindsoftware.com/blog/vmware-cloud-foundation-vcf-9-0-with-vsphere-9-0-and-esxi-9-0-has-been-released/  Quote: "the new virtual hardware v22"
  - Kind: definition
  - Level: core

## T09 Snapshots
- a:N35. KB oficial: un snapshot no es backup, es un registro de cambios sobre el disco base (archivo -00000#-delta.vmdk); si se pierde el disco base, el snapshot solo no restaura nada. Máximo 32 en cadena, usar 2 o 3; no más de 72 horas.
  - Source: https://knowledge.broadcom.com/external/article/318825/best-practices-for-using-vmware-snapshot.html  Quote: "Do not use VMware snapshots as backups."
  - Kind: rule of thumb
  - Level: foundation
- a:N36. No agrandar un disco con snapshots existentes (riesgo de corrupción y pérdida de datos) y no cancelar una consolidación en curso. Los snapshots creados por software de backup vía API pueden no verse en el Snapshot Manager: revisar por línea de comandos.
  - Source: https://knowledge.broadcom.com/external/article/318825/best-practices-for-using-vmware-snapshot.html  Quote: "Do not cancel a running deletion/consolidation task"
  - Kind: mistake
  - Level: core
  - Also: T12
- a:N37. Caso típico: "Virtual machine disks consolidation is needed" después de backups nocturnos que fallaron; el proxy puede tener discos hot-added que bloquean. Liberar el proxy, Snapshots > Consolidate, verificar que no queden -00000N.vmdk.
  - Source: https://open-exam-prep.com/study-guides/vcp-dcv/lifecycle-management-configuration/vm-snapshots-management  Quote: "Virtual machine disks consolidation is needed"
  - Kind: story
  - Level: core
  - Also: T12, T15
- a:N38. Alarma de vCenter por "VM Snapshot Size (GB)" y PowerCLI para listar snapshots de más de 3 días: Get-VM | Get-Snapshot | Where {$_.Created -lt (Get-Date).AddDays(-3)}. RVTools pestaña vSnapshot también sirve.
  - Source: https://www.cloudbolt.io/vmware-administration/vmware-snapshot-best-practices/  Quote: "we recommend not using a single snapshot for more than 24-72 hours"
  - Kind: technique
  - Level: core
  - Bias: CloudBolt vende plataforma de gestión cloud.
- a:N39. Quiesce del sistema de archivos requiere VMware Tools y solo aplica cuando el snapshot no incluye memoria.
  - Source: https://open-exam-prep.com/study-guides/vcp-dcv/lifecycle-management-configuration/vm-snapshots-management  Quote: "only applies when memory is not included"
  - Kind: definition
  - Level: core

## T10 vCenter (VCSA)
- a:N40. VCSA en vSphere 8 pide 2 GB más de RAM que en 7 en cada tamaño: Tiny pasó de 12 a 14 GB. Lam reporta haberlo corrido con 10 GB en laboratorio sin problemas (su experiencia, no soportado).
  - Source: https://williamlam.com/2022/09/homelab-considerations-for-vsphere-8.html  Quote: "in vSphere 8, it now will require 14GB of memory"
  - Kind: number
  - Level: foundation
- a:N41. VCF 9.0 en laboratorio: un vCenter solo ya pide 4 vCPU y 21 GB de RAM; el stack completo (NSX, SDDC Manager, Operations, Automation) suma mucho más.
  - Source: https://williamlam.com/2025/06/ultimate-lab-resource-for-vcf-9-0.html  Quote: "1 x vCenter Server 4 21GB"
  - Kind: number
  - Level: advanced
- a:N42. Al desplegar vCenter, al principio solo el administrador del dominio SSO (por defecto administrator@vsphere.local) puede entrar; el dominio se puede cambiar durante la instalación y no después sin trabajo.
  - Source: https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-security/vsphere-permissions-and-user-management-tasks.html  Quote: "Initially, only the administrator user for the vCenter Single Sign-On domain is authorized to log in"
  - Kind: definition
  - Level: foundation
  - Also: T14
- a:N42b. Si no hay disco persistente (instalación en SD/USB), ESX-OSData, que es donde van scratch y los logs de /var/run/log, se crea en un RAM disk. Inferencia del lector: lo que está en RAM no sobrevive al reinicio, así que el disco persistente también importa para diagnosticar.
  - Source: https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/esx-installation-and-setup/installing-and-setting-up-esxi-install/esxi-requirements-install/esxi-hardware-requirements-install.html  Quote: "ESX-OSData is automatically created on a RAM disk"
  - Kind: mistake
  - Level: core
  - Also: T15

## T11 Clúster, vMotion, HA y DRS
- a:N43. vMotion copia memoria, registros y conexiones al host destino y la VM sigue corriendo; si cambia solo el host, el disco queda en almacenamiento compartido; también se puede mover host y datastore sin almacenamiento compartido. Si falla, la VM vuelve a su estado original.
  - Source: https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vcenter-and-host-management/migrating-virtual-machines-host-management/migration-with-vmotion-host-management.html  Quote: "the virtual machine reverts to its original state and location"
  - Kind: definition
  - Level: core
- a:N44. Crear clúster: clic derecho en el datacenter, New Cluster, activar DRS (Manual, Partially Automated, Fully Automated), activar HA (host monitoring, admission control), EVC si hay CPUs distintas. Crear el clúster no requiere licencia; activar DRS o HA sí.
  - Source: https://knowledge.broadcom.com/external/article/308413  Quote: "you need a license to enable a cluster for vSphere DRS (or vSphere HA)"
  - Kind: template
  - Level: core
- a:N45. HA reinicia las VMs en otro host; no es cero corte. Sigue funcionando aunque vCenter esté caído; DRS en cambio necesita vCenter. Control de admisión reserva capacidad para la falla.
  - Source: https://www.techtarget.com/it-infrastructure/feature/Enabling-VMware-HA-DRS-Advanced-vSphere-features  Quote: "HA does not provide 100% availability of VMs"
  - Kind: definition
  - Level: core
  - Bias: artículo de 2011 (vSphere 4); los conceptos siguen, los detalles internos cambiaron.
- a:N46. Al empezar con DRS, dejarlo en Manual o Partially Automated un tiempo para ver qué recomienda antes de pasar a Fully Automated. DRS solo mira CPU y memoria.
  - Source: https://www.techtarget.com/it-infrastructure/feature/Enabling-VMware-HA-DRS-Advanced-vSphere-features  Quote: "you might want to set the automation level to Manual or Partially Automated"
  - Kind: technique
  - Level: core
- a:N47. Si se usa HA sin DRS, dejar capacidad libre de sobra en cada host, porque las VMs de un host caído se arrancan donde haya lugar.
  - Source: https://www.techtarget.com/it-infrastructure/feature/Enabling-VMware-HA-DRS-Advanced-vSphere-features  Quote: "If you plan to use HA without DRS"
  - Kind: rule of thumb
  - Level: core

## T12 Backups
- a:N48. Transportes de VADP: SAN (proxy físico con acceso a la LUN), HotAdd (proxy virtual que monta el disco), NBD/NBDSSL (por la red de gestión, el más simple). HotAdd no funciona con discos IDE.
  - Source: https://developer.broadcom.com/xapis/virtual-disk-api/latest/vddkBkupVadp.9.5.html  Quote: "NBDSSL is a secure fallback when over-the-network backup is your only choice."
  - Kind: definition
  - Level: core
- a:N49. Veeam en modo red (NBD) entra por el vmk de gestión resuelto por DNS; es el más fácil pero en 1 GbE puede ir a 10 a 20 MB/s por el throttling de la interfaz de gestión (su medición, versiones viejas). Un proxy virtual para restaurar con HotAdd acorta el RTO.
  - Source: https://veeam-best-practices-guide-v9.readthedocs.io/resource_planning/network_mode.html  Quote: "It can be rather slow on 1 Gb Ethernet (about 10-20 MB/s)"
  - Kind: number
  - Level: core
  - Bias: guía de Veeam v9 (antigua).
- a:N50. Estrategia 3-2-1: tres copias, dos medios, una fuera del sitio; los snapshots no cubren pérdida del disco base.
  - Source: https://www.cloudbolt.io/vmware-administration/vmware-snapshot-best-practices/  Quote: "VM snapshots alone can’t cover all data loss scenarios"
  - Kind: rule of thumb
  - Level: foundation

## T13 Parches con Lifecycle Manager
- a:N51. vLCM corre dentro de vCenter sin instalación extra; reemplaza a Update Manager. Operaciones: compliance check (no cambia nada), remediation pre-check, staging (baja los paquetes sin aplicar, acorta el tiempo en mantenimiento), remediation. Sin internet se usa UMDS o importación manual.
  - Source: https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/managing-host-and-cluster-lifecycle/about-vsphere-lifecycle-manager-new.html  Quote: "Staging makes the components, patches, and extensions available locally on the hosts."
  - Kind: definition
  - Level: core
- a:N52. En vSphere 9 se retiran las baselines y queda el modelo de imágenes; con hasta cuatro configuraciones de imagen extra por clúster para hardware mixto.
  - Source: https://www.starwindsoftware.com/blog/vmware-cloud-foundation-vcf-9-0-with-vsphere-9-0-and-esxi-9-0-has-been-released/  Quote: "Phasing out the baselines-based updates in the v9"
  - Kind: definition
  - Level: core
- a:N53. Rollback de ESXi 8 a 7 es posible si no se tocaron los bootbanks; a versiones previas a 7 no, porque se reparticiona el disco de arranque. Backup del dispositivo de arranque antes del upgrade.
  - Source: https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/esx-installation-and-setup/installing-and-setting-up-esxi-install/esxi-requirements-install/esxi-hardware-requirements-install.html  Quote: "Rollback from ESXi 8.x to 7.x is possible as long as no changes to the bootbank partitions have been made"
  - Kind: rule of thumb
  - Level: core

## T14 Usuarios y roles
- a:N54. Autenticación via vCenter Single Sign-On, dominio por defecto vsphere.local, admin inicial administrator@vsphere.local. Permiso = usuario o grupo + rol (conjunto de privilegios) asignado sobre un objeto del inventario. Se pueden agregar fuentes de identidad (AD).
  - Source: https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-security/vsphere-permissions-and-user-management-tasks.html  Quote: "To specify the privileges, you use roles, which are sets of privileges."
  - Kind: definition
  - Level: core
- a:N55. Aislar la red de gestión para que solo accedan administradores de red y seguridad.
  - Source: https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-networking/setting-up-vmkernel-networking/the-vmkernel-networking-layer.html  Quote: "Isolate the management traffic in a network that only network and security administrators can access."
  - Kind: rule of thumb
  - Level: core
  - Also: T06

## T15 Troubleshooting
- a:N56. esxtop por SSH: c CPU, m memoria, d adaptador de disco, u dispositivo, v disco por VM, n red, f campos, h ayuda. Modo batch: esxtop -b -a -d 5 -n 12 > archivo.csv para analizar después.
  - Source: https://knowledge.broadcom.com/external/article/382249/using-esxtop-and-interpreting-esxtop-sta.html  Quote: "In the batch mode, data can be redirected to a file for offline uses."
  - Kind: technique
  - Level: core
- a:N57. Latencia de disco: GAVG = DAVG + KAVG. DAVG alto apunta al almacenamiento; KAVG debería estar cerca de cero y si sube hay encolamiento en el host. %RDY es tiempo listo esperando CPU física.
  - Source: https://knowledge.broadcom.com/external/article/382249/using-esxtop-and-interpreting-esxtop-sta.html  Quote: "The KAVG value should be very small in comparison to the DAVG value and should be close to zero."
  - Kind: test
  - Level: core
- a:N58. Practicante: esxtop es la herramienta para CPU, memoria, disco y red; en el CSV de batch se ven tendencias. Comandos sensibles a mayúsculas.
  - Source: https://www.virtualizationhowto.com/2023/07/esxtop-commands-the-ultimate-guide/  Quote: "ESXTOP commands are case-sensitive"
  - Kind: technique
  - Level: core
- a:N59. Caso real de comentario: un i9 de 12ª generación con ESXi 8 necesitó cpuUniformityHardCheckPanic=FALSE para arrancar y luego tuvo cuelgues de red; los mensajes estaban en vmkernel.log y vmkwarning.log. Hardware fuera de HCL da problemas difíciles.
  - Source: https://williamlam.com/2022/09/homelab-considerations-for-vsphere-8.html  Quote: "On vmkwarning.log and vmkernel.log I found many warning messages."
  - Kind: story
  - Level: core
  - Also: T02
- a:N60. Modo mantenimiento: DRS mueve con prioridad máxima (cinco estrellas) las VMs de un host que entra en mantenimiento; vLCM usa staging para acortar el tiempo en ese modo.
  - Source: https://www.techtarget.com/it-infrastructure/feature/Enabling-VMware-HA-DRS-Advanced-vSphere-features  Quote: "a mandatory move because of a host entering maintenance mode"
  - Kind: definition
  - Level: core
  - Also: T13

## T16 Migración a otras plataformas
- a:N68. En agosto y septiembre de 2026 Broadcom retiró las descargas públicas del VDDK (la librería de discos que usan Azure Migrate, Red Hat MTV, Nutanix Move y otras herramientas de migración y backup); soporte respondió que ya no está disponible para uso general. El importador de Proxmox no depende del VDDK (su lectura de hilos de Reddit, ShapeBlue, Red Hat y Microsoft).
  - Source: https://www.virtualizationhowto.com/2026/09/leaving-vmware-just-got-harder-after-broadcom-pulled-vddk-downloads/  Quote: "Proxmox doesn’t depend on the VDDK to import VMware workloads"
  - Kind: story
  - Level: advanced
  - Also: T12
  - Bias: blog de homelab con tono crítico hacia Broadcom.
- a:N61. Proxmox VE (desde 8.1, probado contra ESXi 6.5 a 8.0) trae importador: Datacenter > Storage > Add > ESXi, ver VMs, Import. Importar contra el host ESXi y no por vCenter (mucho más lento). No soporta discos en vSAN ni VMs cifradas; con snapshots es más lento.
  - Source: https://pve.proxmox.com/wiki/Migrate_to_Proxmox_VE  Quote: "While one can also import through a vCenter instance, doing so will dramatically reduce performance."
  - Kind: technique
  - Level: core
  - Bias: documentación del fabricante destino.
- a:N62. Preparación: desinstalar VMware Tools antes, anotar la config de red (la NIC cambia de nombre y MAC), en Windows instalar drivers VirtIO; el vTPM no se migra, tener a mano las claves de BitLocker.
  - Source: https://pve.proxmox.com/wiki/Migrate_to_Proxmox_VE  Quote: "It is currently not possible to migrate the vTPM state to Proxmox VE from VMware."
  - Kind: mistake
  - Level: core
- a:N63. Live-import arranca la VM durante la importación, pero si falla se pierde todo lo escrito desde el inicio. Thomas-Krenn sugiere apagar la VM y no usar live restore como camino más seguro.
  - Source: https://www.thomas-krenn.com/en/wiki/ESXi_VM_importer_-_Proxmox_VE_Storage_Plugin  Quote: "The safest approach is to stop VMs on the ESXi side for import"
  - Kind: rule of thumb
  - Level: core

- a:N65. Para importaciones masivas, no más de cuatro discos a la vez: la API de ESXi tiene pocas conexiones y bloquea unos 30 segundos al pasarse.
  - Source: https://pve.proxmox.com/wiki/Migrate_to_Proxmox_VE  Quote: "no more than four VM disks are imported at the same time"
  - Kind: number
  - Level: advanced
- a:N66. Alternativas: Proxmox VE (AGPLv3, suscripción opcional por socket de 120 a 1100 euros por año), XCP-ng (Xen, Vates) y SUSE Virtualization (Harvester). Ninguna reemplaza vSphere "en un clic"; para 2 o 3 hosts el trabajo es acotado. Plan: piloto en un host no crítico, mover 2 o 3 VMs, probar backup y restore.
  - Source: https://introserv.com/blog/migrating-from-vmware-in-2026-the-end-of-perpetual-licenses-vsphere-8-end-of-support-and-replacement-options/  Quote: "None of these platforms replaces vSphere in one click."
  - Kind: technique
  - Level: core
  - Bias: vende servidores para estas plataformas.
- a:N67. Hay casos donde renovar VMware conviene: hosts densos (16 núcleos o más por CPU), uso real de vSAN/NSX, apps certificadas solo para vSphere.
  - Source: https://introserv.com/blog/migrating-from-vmware-in-2026-the-end-of-perpetual-licenses-vsphere-8-end-of-support-and-replacement-options/  Quote: "There are configurations where the new model works in the customer's favor."
  - Kind: rule of thumb
  - Level: core
  - Also: T01

## Disagreements seen
- Tiempo máximo de un snapshot: la KB dice no más de 72 horas (https://knowledge.broadcom.com/external/article/318825/best-practices-for-using-vmware-snapshot.html); CloudBolt recomienda 24 a 72 horas (https://www.cloudbolt.io/vmware-administration/vmware-snapshot-best-practices/).
- Renovar o migrar: Broadcom empuja VCF 9 / VVF 9 como camino (https://knowledge.broadcom.com/external/article/456708/upcoming-end-of-service-for-vsphere-8-vs.html, https://blogs.vmware.com/cloud-foundation/2026/02/06/global-supports-vmware-cloud-foundation-9-paths-to-adoption); Introserv y Redress dicen que para 2 a 10 hosts chicos la cuenta suele no cerrar y conviene cotizar alternativa (https://introserv.com/blog/migrating-from-vmware-in-2026-the-end-of-perpetual-licenses-vsphere-8-end-of-support-and-replacement-options/, https://redresscompliance.com/vcf-licensing-guide-2026.html).
- Confianza en la plataforma: virtualizationhowto lee el retiro del VDDK como lock-in y dice que se perdió la confianza (https://www.virtualizationhowto.com/2026/09/leaving-vmware-just-got-harder-after-broadcom-pulled-vddk-downloads/); Broadcom presenta VCF 9 como plataforma unificada con caminos de adopción claros (https://blogs.vmware.com/cloud-foundation/2026/02/06/global-supports-vmware-cloud-foundation-9-paths-to-adoption).
- Live import en Proxmox: el wiki lo presenta como forma de reducir corte (https://pve.proxmox.com/wiki/Migrate_to_Proxmox_VE); Thomas-Krenn prefiere importar en frío (https://www.thomas-krenn.com/en/wiki/ESXi_VM_importer_-_Proxmox_VE_Storage_Plugin).
- Hardware no soportado: Lam publica los parámetros para forzar CPUs viejas en laboratorio (https://williamlam.com/2025/06/ultimate-lab-resource-for-vcf-9-0.html); la documentación oficial exige la compatibility guide (https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/esx-installation-and-setup/installing-and-setting-up-esxi-install/esxi-requirements-install/esxi-hardware-requirements-install.html).

## Best stories
- ESXi gratis vuelve con una sola frase en las release notes de 8.0 U3e: https://www.it-connect.fr/la-version-gratuite-de-vmware-esxi-free-est-de-retour-en-2025/
- Tres hosts de 8 núcleos pagan como 48: https://introserv.com/blog/migrating-from-vmware-in-2026-the-end-of-perpetual-licenses-vsphere-8-end-of-support-and-replacement-options/
- "Consolidation is needed" tras backups nocturnos fallidos: https://open-exam-prep.com/study-guides/vcp-dcv/lifecycle-management-configuration/vm-snapshots-management
- Bootear el instalador sin instalar para chequear compatibilidad: https://williamlam.com/2022/09/homelab-considerations-for-vsphere-8.html
- Broadcom retira el VDDK y frena migraciones de terceros: https://www.virtualizationhowto.com/2026/09/leaving-vmware-just-got-harder-after-broadcom-pulled-vddk-downloads/
- El i9 de 12ª generación y el vmkwarning.log: https://williamlam.com/2022/09/homelab-considerations-for-vsphere-8.html
