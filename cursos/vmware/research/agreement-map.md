# Mapa de acuerdos: VMware vSphere (ESXi y vCenter)

Fuente: research/notes/a.md (30 páginas). M = páginas con alguna nota en el subtema del tema (incluye Also). Contamos páginas, no notas.
Totales por subtema: T01 9 · T02 3 · T03 2 · T04 2 · T05 2 · T06 2 · T07 2 · T08 4 · T09 3 · T10 4 · T11 4 · T12 8 · T13 4 · T14 3 · T15 7 · T16 4.

## TH01 Entendé qué licencia tiene el cliente antes de tocar nada: hoy todo es suscripción por núcleo
- Sub-topic: T01
- Agree: 6 of 9. Notes: a:N1, a:N2, a:N3, a:N4, a:N5, a:N11. Urls: https://thomas-krenn.com/en/wiki/VMware_license_model_by_Broadcom, https://introserv.com/blog/migrating-from-vmware-in-2026-the-end-of-perpetual-licenses-vsphere-8-end-of-support-and-replacement-options/, https://redresscompliance.com/vcf-licensing-guide-2026.html, https://knowledge.broadcom.com/external/article/456708/upcoming-end-of-service-for-vsphere-8-vs.html, https://blogs.vmware.com/cloud-foundation/2026/02/06/global-supports-vmware-cloud-foundation-9-paths-to-adoption, https://www.starwindsoftware.com/blog/vmware-cloud-foundation-vcf-9-0-with-vsphere-9-0-and-esxi-9-0-has-been-released/
- Disagree: none found sobre el hecho; la discusión es si conviene (ver TH30).
- Level: foundation
- Best story: tres hosts de 8 núcleos se licencian como 48, https://introserv.com/blog/migrating-from-vmware-in-2026-the-end-of-perpetual-licenses-vsphere-8-end-of-support-and-replacement-options/

## TH02 Contá núcleos con la regla del mínimo de 16 por CPU (RVTools o el script oficial)
- Sub-topic: T01 (also T14)
- Agree: 2 of 9. Notes: a:N2, a:N6. Urls: https://introserv.com/blog/migrating-from-vmware-in-2026-the-end-of-perpetual-licenses-vsphere-8-end-of-support-and-replacement-options/, https://redresscompliance.com/vcf-licensing-guide-2026.html
- Disagree: none found
- Level: core
- Best story: 40 hosts de 2x12 núcleos facturan 1280 en vez de 960, https://redresscompliance.com/vcf-licensing-guide-2026.html

## TH03 El ESXi gratuito existe otra vez (8.0 U3e) pero es para laboratorio: sin vCenter, sin VADP, sin soporte
- Sub-topic: T01 (also T12)
- Agree: 3 of 9. Notes: a:N7, a:N8, a:N9. Urls: https://knowledge.broadcom.com/external/article/399823/vmware-esxi-80-update-3e-now-available-a.html, https://www.it-connect.fr/la-version-gratuite-de-vmware-esxi-free-est-de-retour-en-2025/, https://phoenixnap.com/kb/vmware-esxi
- Disagree: https://thomas-krenn.com/en/wiki/VMware_license_model_by_Broadcom: lo sigue listando como discontinuado (página no actualizada); https://introserv.com/blog/migrating-from-vmware-in-2026-the-end-of-perpetual-licenses-vsphere-8-end-of-support-and-replacement-options/: dice que fue retirado sin reemplazo.
- Level: foundation
- Best story: volvió con una sola frase en las release notes, https://www.it-connect.fr/la-version-gratuite-de-vmware-esxi-free-est-de-retour-en-2025/

## TH04 Anotá la fecha: vSphere 8 deja de tener soporte y parches el 11 de octubre de 2027
- Sub-topic: T01
- Agree: 2 of 9. Notes: a:N10, a:N11. Urls: https://knowledge.broadcom.com/external/article/456708/upcoming-end-of-service-for-vsphere-8-vs.html, https://introserv.com/blog/migrating-from-vmware-in-2026-the-end-of-perpetual-licenses-vsphere-8-end-of-support-and-replacement-options/
- Disagree: none found entre las páginas finales.
- Level: foundation
- Best story: none

## TH05 vSphere 9 llega dentro de VCF/VVF 9: baselines afuera, imágenes adentro
- Sub-topic: T01 (also T13)
- Agree: 3 of 9. Notes: a:N12, a:N14, a:N52. Urls: https://www.starwindsoftware.com/blog/vmware-cloud-foundation-vcf-9-0-with-vsphere-9-0-and-esxi-9-0-has-been-released/, https://blogs.vmware.com/cloud-foundation/2026/02/06/global-supports-vmware-cloud-foundation-9-paths-to-adoption, https://williamlam.com/2025/06/ultimate-lab-resource-for-vcf-9-0.html
- Disagree: none found
- Level: core
- Best story: none

## TH06 Chequeá el hardware contra la Compatibility Guide antes de cotizar o actualizar
- Sub-topic: T02
- Agree: 3 of 3. Notes: a:N15, a:N17, a:N18, a:N19. Urls: https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/esx-installation-and-setup/installing-and-setting-up-esxi-install/esxi-requirements-install/esxi-hardware-requirements-install.html, https://williamlam.com/2022/09/homelab-considerations-for-vsphere-8.html, https://williamlam.com/2025/06/ultimate-lab-resource-for-vcf-9-0.html
- Disagree: Lam publica el parámetro allowLegacyCPU para forzar CPUs fuera de soporte en laboratorio; la doc oficial no lo contempla.
- Level: foundation
- Best story: bootear el instalador desde USB sin instalar para ver si detecta todo, https://williamlam.com/2022/09/homelab-considerations-for-vsphere-8.html

## TH07 Instalá ESXi en disco persistente (idealmente 128 GB en RAID 1), no en SD/USB
- Sub-topic: T02 (also T15)
- Agree: 2 of 3. Notes: a:N16, a:N42b. Urls: https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/esx-installation-and-setup/installing-and-setting-up-esxi-install/esxi-requirements-install/esxi-hardware-requirements-install.html, https://williamlam.com/2022/09/homelab-considerations-for-vsphere-8.html
- Disagree: none found
- Level: foundation
- Best story: alarma "Secondary persistent device not found", techdocs requisitos.

## TH08 Configurá la red de gestión con IP fija, DNS y hostname desde la DCUI y verificá con el Host Client
- Sub-topic: T03 (also T04)
- Agree: 2 of 2. Notes: a:N21, a:N15. Urls: https://phoenixnap.com/kb/vmware-esxi, https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/esx-installation-and-setup/installing-and-setting-up-esxi-install/esxi-requirements-install/esxi-hardware-requirements-install.html
- Disagree: none found
- Level: foundation
- Best story: none

## TH09 Un port group = una VLAN; VLAN 0 es sin etiqueta
- Sub-topic: T05
- Agree: 2 of 2. Notes: a:N23, a:N25. Urls: https://knowledge.broadcom.com/external/article/311057/configuring-vlan-on-a-vswitch-standard.html, https://phoenixnap.com/kb/vmware-esxi
- Disagree: none found
- Level: foundation
- Best story: none

## TH10 Nunca cambies la red de gestión sin consola fuera de banda (iLO, iDRAC o pantalla)
- Sub-topic: T05 (also T15)
- Agree: 1 of 2. Notes: a:N24. Urls: https://knowledge.broadcom.com/external/article/311057/configuring-vlan-on-a-vswitch-standard.html
- Disagree: none found. Thin evidence (M=2), pero es la KB oficial.
- Level: foundation
- Best story: none

## TH11 Dos uplinks por vSwitch y NIC teaming para no tener un único punto de falla
- Sub-topic: T05 (also T06)
- Agree: 2 of 2. Notes: a:N25, a:N26. Urls: https://phoenixnap.com/kb/vmware-esxi, https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-networking/setting-up-vmkernel-networking/the-vmkernel-networking-layer.html
- Disagree: none found
- Level: foundation
- Best story: none

## TH12 Un vmk por tipo de tráfico, cada uno en su VLAN y subred
- Sub-topic: T06
- Agree: 2 of 2. Notes: a:N26, a:N25, a:N28. Urls: https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-networking/setting-up-vmkernel-networking/the-vmkernel-networking-layer.html, https://phoenixnap.com/kb/vmware-esxi
- Disagree: none found
- Level: foundation
- Best story: none

## TH13 vMotion no va cifrado: red aislada solo para hosts
- Sub-topic: T06 (also T11)
- Agree: 1 of 2 (más TechTarget en T11 sobre separar tráfico). Notes: a:N27. Urls: https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-networking/setting-up-vmkernel-networking/the-vmkernel-networking-layer.html
- Disagree: none found. Thin evidence.
- Level: core
- Best story: none

## TH14 Para iSCSI/NFS: vmk dedicado, MTU 9000 de punta a punta, dos NICs para multipath
- Sub-topic: T07 (also T06)
- Agree: 2 of 2. Notes: a:N28, a:N29. Urls: https://phoenixnap.com/kb/vmware-esxi, https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-networking/setting-up-vmkernel-networking/the-vmkernel-networking-layer.html
- Disagree: none found. Thin evidence.
- Level: core
- Best story: none

## TH15 Thin provisioning ahorra espacio pero puede llenar el datastore y frenar las VMs: vigilá el espacio libre
- Sub-topic: T08 (also T07)
- Agree: 2 of 4. Notes: a:N30, a:N31. Urls: https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-virtual-machine-administration/configuring-virtual-machine-hardwarevsphere-vm-admin/virtual-disk-configurationvsphere-vm-admin/about-virtual-disk-provisioning-policiesvsphere-vm-admin.html, https://veeam-best-practices-guide-v9.readthedocs.io/resource_planning/network_mode.html (restaurar en thin para transportar menos)
- Disagree: none found
- Level: foundation
- Best story: none

## TH16 VMware Tools siempre instalado y al día
- Sub-topic: T08 (also T09, T11)
- Agree: 3 of 4. Notes: a:N33, a:N39, a:N45. Urls: https://knowledge.broadcom.com/external/article/382249/using-esxtop-and-interpreting-esxtop-sta.html, https://open-exam-prep.com/study-guides/vcp-dcv/lifecycle-management-configuration/vm-snapshots-management, https://www.techtarget.com/it-infrastructure/feature/Enabling-VMware-HA-DRS-Advanced-vSphere-features
- Disagree: https://pve.proxmox.com/wiki/Migrate_to_Proxmox_VE: al migrar hay que sacarlo antes (no es desacuerdo, es otro momento).
- Level: foundation
- Best story: none

## TH17 Los appliances de fabricantes (.ova) entran por Deploy OVF Template
- Sub-topic: T08
- Agree: 1 of 4. Notes: a:N32. Urls: https://open-exam-prep.com/study-guides/vcp-dcv/lifecycle-management-configuration/vm-snapshots-management
- Disagree: none found. Thin evidence.
- Level: foundation
- Best story: none

## TH18 Un snapshot no es un backup: máximo 2 o 3 por VM y nunca más de 72 horas
- Sub-topic: T09 (also T12)
- Agree: 3 of 3. Notes: a:N35, a:N38, a:N50, a:N39. Urls: https://knowledge.broadcom.com/external/article/318825/best-practices-for-using-vmware-snapshot.html, https://www.cloudbolt.io/vmware-administration/vmware-snapshot-best-practices/, https://open-exam-prep.com/study-guides/vcp-dcv/lifecycle-management-configuration/vm-snapshots-management
- Disagree: https://www.cloudbolt.io/vmware-administration/vmware-snapshot-best-practices/: sugiere 24 a 72 horas (más estricto).
- Level: foundation
- Best story: delta que crece hasta llenar el datastore.

## TH19 No agrandes discos con snapshots vivos ni canceles una consolidación
- Sub-topic: T09
- Agree: 2 of 3. Notes: a:N36, a:N37. Urls: https://knowledge.broadcom.com/external/article/318825/best-practices-for-using-vmware-snapshot.html, https://open-exam-prep.com/study-guides/vcp-dcv/lifecycle-management-configuration/vm-snapshots-management
- Disagree: none found
- Level: core
- Best story: "consolidation is needed" tras backups fallidos, https://open-exam-prep.com/study-guides/vcp-dcv/lifecycle-management-configuration/vm-snapshots-management

## TH20 Vigilá snapshots huérfanos con alarma, PowerCLI o RVTools
- Sub-topic: T09 (also T12, T15)
- Agree: 3 of 3. Notes: a:N36, a:N37, a:N38. Urls: https://knowledge.broadcom.com/external/article/318825/best-practices-for-using-vmware-snapshot.html, https://open-exam-prep.com/study-guides/vcp-dcv/lifecycle-management-configuration/vm-snapshots-management, https://www.cloudbolt.io/vmware-administration/vmware-snapshot-best-practices/
- Disagree: none found
- Level: core
- Best story: none

## TH21 vCenter es una VM (VCSA) que pide RAM en serio: dimensionala antes
- Sub-topic: T10
- Agree: 2 of 4. Notes: a:N40, a:N41. Urls: https://williamlam.com/2022/09/homelab-considerations-for-vsphere-8.html, https://williamlam.com/2025/06/ultimate-lab-resource-for-vcf-9-0.html
- Disagree: Lam corre Tiny con 10 GB en laboratorio; la cifra soportada es 14 GB.
- Level: foundation
- Best story: Tiny pasó de 12 a 14 GB, https://williamlam.com/2022/09/homelab-considerations-for-vsphere-8.html

## TH22 administrator@vsphere.local es la llave maestra: guardala y no la uses para el día a día
- Sub-topic: T10 (also T14)
- Agree: 1 of 4 (más T14). Notes: a:N42, a:N54. Urls: https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-security/vsphere-permissions-and-user-management-tasks.html
- Disagree: none found
- Level: foundation
- Best story: none

## TH23 vMotion mueve la VM encendida; para cambiar solo de host hace falta almacenamiento compartido
- Sub-topic: T11
- Agree: 2 of 4. Notes: a:N43, a:N27. Urls: https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vcenter-and-host-management/migrating-virtual-machines-host-management/migration-with-vmotion-host-management.html, https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-networking/setting-up-vmkernel-networking/the-vmkernel-networking-layer.html
- Disagree: none found
- Level: core
- Best story: si falla, la VM vuelve sola a su origen.

## TH24 HA reinicia (no evita el corte) y funciona sin vCenter; DRS balancea y necesita vCenter
- Sub-topic: T11
- Agree: 2 of 4. Notes: a:N44, a:N45, a:N47. Urls: https://knowledge.broadcom.com/external/article/308413, https://www.techtarget.com/it-infrastructure/feature/Enabling-VMware-HA-DRS-Advanced-vSphere-features
- Disagree: none found
- Level: core
- Best story: none

## TH25 Empezá DRS en Manual o Parcial y mirá sus recomendaciones antes de automatizar
- Sub-topic: T11
- Agree: 1 of 4. Notes: a:N46. Urls: https://www.techtarget.com/it-infrastructure/feature/Enabling-VMware-HA-DRS-Advanced-vSphere-features
- Disagree: el mismo artículo dice que lo usual es terminar en Fully Automated. Thin evidence y fuente de 2011.
- Level: core
- Best story: none

## TH26 Backups con producto que use VADP/CBT y regla 3-2-1; elegí bien el modo de transporte
- Sub-topic: T12
- Agree: 5 of 8. Notes: a:N48, a:N49, a:N50, a:N9, a:N7. Urls: https://developer.broadcom.com/xapis/virtual-disk-api/latest/vddkBkupVadp.9.5.html, https://veeam-best-practices-guide-v9.readthedocs.io/resource_planning/network_mode.html, https://www.cloudbolt.io/vmware-administration/vmware-snapshot-best-practices/, https://phoenixnap.com/kb/vmware-esxi, https://knowledge.broadcom.com/external/article/399823/vmware-esxi-80-update-3e-now-available-a.html
- Disagree: none found
- Level: core
- Best story: NBD en 1 GbE puede ir a 10 a 20 MB/s, https://veeam-best-practices-guide-v9.readthedocs.io/resource_planning/network_mode.html

## TH27 Probá el restore, no solo el backup
- Sub-topic: T12 (also T16)
- Agree: 2 of 8. Notes: a:N66, a:N49. Urls: https://introserv.com/blog/migrating-from-vmware-in-2026-the-end-of-perpetual-licenses-vsphere-8-end-of-support-and-replacement-options/, https://veeam-best-practices-guide-v9.readthedocs.io/resource_planning/network_mode.html
- Disagree: none found
- Level: core
- Best story: none

## TH28 Parcheá con Lifecycle Manager: compliance, pre-check, staging, remediate
- Sub-topic: T13
- Agree: 3 of 4. Notes: a:N51, a:N52, a:N60. Urls: https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/managing-host-and-cluster-lifecycle/about-vsphere-lifecycle-manager-new.html, https://www.starwindsoftware.com/blog/vmware-cloud-foundation-vcf-9-0-with-vsphere-9-0-and-esxi-9-0-has-been-released/, https://www.techtarget.com/it-infrastructure/feature/Enabling-VMware-HA-DRS-Advanced-vSphere-features
- Disagree: none found
- Level: core
- Best story: staging para acortar el modo mantenimiento.

## TH29 Antes de actualizar ESXi, backup del arranque y plan de vuelta
- Sub-topic: T13
- Agree: 1 of 4. Notes: a:N53. Urls: https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/esx-installation-and-setup/installing-and-setting-up-esxi-install/esxi-requirements-install/esxi-hardware-requirements-install.html
- Disagree: none found. Thin.
- Level: core
- Best story: none

## TH30 Permisos = usuario o grupo + rol sobre un objeto; usuarios nominales, no cuentas compartidas
- Sub-topic: T14
- Agree: 2 of 3. Notes: a:N54, a:N55. Urls: https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-security/vsphere-permissions-and-user-management-tasks.html, https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-networking/setting-up-vmkernel-networking/the-vmkernel-networking-layer.html
- Disagree: none found
- Level: core
- Best story: none

## TH31 Lentitud: mirá esxtop antes de opinar (%RDY para CPU, DAVG contra KAVG para disco)
- Sub-topic: T15
- Agree: 2 of 7. Notes: a:N56, a:N57, a:N58. Urls: https://knowledge.broadcom.com/external/article/382249/using-esxtop-and-interpreting-esxtop-sta.html, https://www.virtualizationhowto.com/2023/07/esxtop-commands-the-ultimate-guide/
- Disagree: none found
- Level: core
- Best story: GAVG = DAVG + KAVG, KAVG cerca de cero, https://knowledge.broadcom.com/external/article/382249/using-esxtop-and-interpreting-esxtop-sta.html

## TH32 Logs: vmkernel.log y compañía en /var/run/log del host; los de vCenter en /var/log/vmware
- Sub-topic: T15
- Agree: 2 of 7. Notes: a:N59, a:N42b. Urls: https://williamlam.com/2022/09/homelab-considerations-for-vsphere-8.html, https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/esx-installation-and-setup/installing-and-setting-up-esxi-install/esxi-requirements-install/esxi-hardware-requirements-install.html
- Disagree: none found
- Level: core
- Best story: i9 de 12ª generación con warnings en vmkwarning.log, https://williamlam.com/2022/09/homelab-considerations-for-vsphere-8.html

## TH33 Modo mantenimiento antes de cualquier intervención en un host
- Sub-topic: T15 (also T13)
- Agree: 2 of 7. Notes: a:N60, a:N51. Urls: https://www.techtarget.com/it-infrastructure/feature/Enabling-VMware-HA-DRS-Advanced-vSphere-features, https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/managing-host-and-cluster-lifecycle/about-vsphere-lifecycle-manager-new.html
- Disagree: none found
- Level: foundation
- Best story: none

## TH34 Migrar a Proxmox: importador ESXi directo al host, Tools afuera antes, VirtIO, en frío y de a pocos discos
- Sub-topic: T16
- Agree: 3 of 4. Notes: a:N61, a:N62, a:N63, a:N65, a:N68. Urls: https://pve.proxmox.com/wiki/Migrate_to_Proxmox_VE, https://www.thomas-krenn.com/en/wiki/ESXi_VM_importer_-_Proxmox_VE_Storage_Plugin, https://www.virtualizationhowto.com/2026/09/leaving-vmware-just-got-harder-after-broadcom-pulled-vddk-downloads/
- Disagree: el wiki ofrece live-import para reducir el corte; Thomas-Krenn prefiere en frío.
- Level: core
- Best story: Broadcom retira el VDDK y las herramientas de terceros quedan trabadas, Proxmox no, https://www.virtualizationhowto.com/2026/09/leaving-vmware-just-got-harder-after-broadcom-pulled-vddk-downloads/

## TH35 Renovar o migrar se decide con números: núcleos licenciables, funciones usadas y un piloto
- Sub-topic: T16 (also T01)
- Agree: 2 of 4 (más Redress en T01). Notes: a:N66, a:N67, a:N5. Urls: https://introserv.com/blog/migrating-from-vmware-in-2026-the-end-of-perpetual-licenses-vsphere-8-end-of-support-and-replacement-options/, https://redresscompliance.com/vcf-licensing-guide-2026.html
- Disagree: https://knowledge.broadcom.com/external/article/456708/upcoming-end-of-service-for-vsphere-8-vs.html y https://blogs.vmware.com/cloud-foundation/2026/02/06/global-supports-vmware-cloud-foundation-9-paths-to-adoption: el camino recomendado es VCF 9 o VVF 9.
- Level: core
- Best story: none

## The big splits
- Renovar VMware o migrar: Broadcom (KB 456708, blog VCF) recomienda pasar a VCF/VVF 9; Introserv y Redress muestran que en 2 a 10 hosts de pocos núcleos se paga por núcleos que no existen y conviene cotizar alternativa; Introserv admite que en hosts densos con vSAN/NSX la cuenta cierra. Gira en la forma del hardware y en qué funciones se usan de verdad.
- ESXi gratuito: la KB 399823 y phoenixNAP lo describen vigente (8.0 U3e); Thomas-Krenn e Introserv lo dan por discontinuado; it-connect advierte que puede volver a cambiar. Gira en la fecha de cada página y en para qué se usa (laboratorio sí, cliente en producción no).
- Hardware fuera de lista: Lam documenta cómo forzarlo en laboratorio; la doc oficial exige compatibility guide. Gira en laboratorio contra producción con soporte.
- Live-import en Proxmox: wiki a favor para bajar el corte, Thomas-Krenn prefiere en frío. Gira en la calidad de la red y la tolerancia a perder lo escrito si falla.
- Edad máxima de un snapshot: 72 horas (KB) contra 24 a 72 (CloudBolt).

## Coverage gaps
- T03 a T07 (instalación, Host Client, redes, VMkernel, almacenamiento) tienen M=2: evidencia fina en cantidad, aunque con documentación oficial. Faltó una página dedicada a NFS/iSCSI paso a paso y a NIC teaming (políticas de balanceo).
- No hay fuente leída sobre despliegue paso a paso del VCSA (stage 1 y stage 2) ni sobre backup basado en archivos del vCenter; se tratará como concepto.
- EVC solo aparece mencionado en la KB de clúster; no hay detalle.
- Veeam: solo la guía de best practices v9 (antigua) y la doc VDDK; falta doc actual de Veeam 12/13 y de otros productos (Nakivo, Altaro). El retiro del VDDK (sept 2026) podría afectar a productos de backup de terceros: no hay fuente que lo confirme para Veeam.
- Roles personalizados y lista de privilegios: solo el concepto.
- vSphere 9 operativo (Host Client 9, cambios de UI): sin fuente práctica; el curso queda en vSphere 8 con notas de 9.
- Fuentes pedidas que no se pudieron leer: vinfrastructure.it devolvió 403 al scraper; 4sysops no apareció en resultados útiles antes de agotar el presupuesto de búsqueda.
