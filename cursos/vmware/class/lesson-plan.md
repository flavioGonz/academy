# Plan del curso: VMware vSphere: ESXi y vCenter en la práctica

Público: técnicos instaladores y de soporte de IES, con base de redes. Nivel inicial a intermedio.
Versión de referencia: vSphere 8.0 Update 3 (ESXi 8 y vCenter 8), con notas sobre vSphere 9 / VCF 9.x, que es lo vigente a octubre de 2026. Fin de soporte general de vSphere 8: 11 de octubre de 2027.
Formato: 12 lecciones de unos 2 minutos, 3 arcos de 4. Cada lección: guion de dos conductores (Lucía y Martín), tarjeta y 3 preguntas.
Laboratorio: un ESXi 8 de prueba (en hardware viejo de la oficina o anidado dentro de otra VM), con licencia gratuita o el período de evaluación; para lo que necesita vCenter y clúster, los Hands-On Labs de Broadcom o un vCenter de laboratorio.

## Arco 1. Fundamentos: qué tiene el cliente y cómo se arma un host
Por qué este arco: antes de tocar un ESXi hace falta saber qué licencia y qué versión tiene el cliente, si el hardware sirve, y cómo queda la red del host, que es donde se cometen los errores que dejan a un sitio sin gestión. Cierra con un host instalado, con su red y su almacenamiento IP armados.

### Lección 1. Qué licencia hay
- 6 de 9 fuentes de licenciamiento coinciden en el cuadro: suscripción, por núcleo, mínimo 16 por CPU, vCenter incluido. Sobre el ESXi gratuito: 3 lo dan vigente (8.0 U3e), 2 páginas más viejas lo dan por discontinuado.
- Idea: desde 2024 VMware se vende solo por suscripción (VVF, VCF; Standard y Enterprise Plus solo hasta 8.0 U3), por núcleo físico con mínimo de 16 por CPU. El ESXi gratuito volvió con 8.0 U3e, pero sin vCenter, sin backups por API y sin soporte.
- Por qué importa: el técnico tiene que saber qué tiene el cliente para no prometer vMotion o backups que su licencia no da, y para avisar del fin de soporte de vSphere 8 en octubre de 2027.
- Historia: tres hosts con una CPU de 8 núcleos son 24 núcleos físicos pero se licencian 48 (ejemplo de la KB 313548 citado por Introserv): https://introserv.com/blog/migrating-from-vmware-in-2026-the-end-of-perpetual-licenses-vsphere-8-end-of-support-and-replacement-options/
- Laboratorio (Admin, 10 min): en el Host Client ver Manage > Licensing; por SSH `vmware -vl` y `esxcli hardware cpu global get`; calcular núcleos licenciables con la regla de 16.
- Regla: antes de proponer una función de VMware, miro qué licencia y versión tiene el host.
- Fuentes: https://knowledge.broadcom.com/external/article/399823/vmware-esxi-80-update-3e-now-available-a.html, https://knowledge.broadcom.com/external/article/456708/upcoming-end-of-service-for-vsphere-8-vs.html, https://thomas-krenn.com/en/wiki/VMware_license_model_by_Broadcom

### Lección 2. ESXi bien instalado
- 3 de 3 fuentes de hardware coinciden: primero la Compatibility Guide. Lam documenta cómo forzar CPUs viejas, solo para laboratorio.
- Idea: ESXi 8 pide 2 núcleos, 8 GB de RAM, NX/XD y VT habilitados, UEFI y disco de arranque persistente (32 GB mínimo, 128 GB óptimo, RAID 1). SD/USB ya no sirve para OSDATA. ESXi 9 deja afuera CPUs Skylake y anteriores.
- Por qué importa: un servidor fuera de lista o arrancando de SD falla de formas difíciles de diagnosticar y no tiene soporte.
- Historia: bootear el instalador desde USB sin instalar para ver si reconoce CPU, NICs y controladora (William Lam): https://williamlam.com/2022/09/homelab-considerations-for-vsphere-8.html
- Laboratorio (Campo, 15 min): buscar el modelo en la Broadcom Compatibility Guide, bootear el instalador sin instalar, configurar IP fija, DNS y hostname desde la DCUI.
- Regla: ningún ESXi se instala en hardware que no chequeé en la Compatibility Guide ni en un pendrive.
- Fuentes: https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/esx-installation-and-setup/installing-and-setting-up-esxi-install/esxi-requirements-install/esxi-hardware-requirements-install.html, https://williamlam.com/2025/06/ultimate-lab-resource-for-vcf-9-0.html, https://phoenixnap.com/kb/vmware-esxi

### Lección 3. Red del host
- 2 de 2 fuentes que cubren redes estándar coinciden (evidencia fina en cantidad, pero una es la KB oficial).
- Idea: el vSwitch estándar une uplinks físicos (vmnic) con port groups; cada port group lleva un VLAN ID (0 es sin etiqueta) y el puerto del switch físico va en troncal. Dos uplinks por vSwitch para no depender de un cable.
- Por qué importa: es la misma lógica de VLAN que el técnico ya conoce de switches, aplicada adentro del servidor; y tocar la red de gestión mal deja el host inaccesible.
- Historia: la KB de Broadcom advierte que cambiar la VLAN del port group de gestión por SSH o desde el cliente puede cortar el acceso; recomienda hacerlo desde iLO, iDRAC o la consola: https://knowledge.broadcom.com/external/article/311057/configuring-vlan-on-a-vswitch-standard.html
- Laboratorio (Foco, 15 min): crear vSwitch1 con dos uplinks y un port group VLAN 20 por esxcli; verificar con `esxcfg-vswitch -l`.
- Regla: la red de gestión se toca solo con consola fuera de banda abierta.
- Fuentes: https://knowledge.broadcom.com/external/article/311057/configuring-vlan-on-a-vswitch-standard.html, https://phoenixnap.com/kb/vmware-esxi

### Lección 4. VMkernel y almacenamiento
- 2 de 2 fuentes coinciden: un adaptador VMkernel por tipo de tráfico; iSCSI y NFS sobre vmk dedicado, con MTU 9000 de punta a punta si se usan jumbo frames.
- Idea: los vmk son las IPs del propio host (gestión, vMotion, almacenamiento). Cada servicio en su vmk, su VLAN y su subred. Datastores: VMFS sobre disco o LUN, NFS 3 o 4.1 sobre la red.
- Por qué importa: mezclar tráfico de almacenamiento con el de cámaras o usuarios da latencias raras; un MTU desparejo da cortes intermitentes.
- Historia: la documentación dice que vMotion viaja sin cifrar y pide red privada solo para hosts: https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-networking/setting-up-vmkernel-networking/the-vmkernel-networking-layer.html
- Laboratorio (Foco, 20 min): crear vmk1 en una VLAN de almacenamiento, probar `vmkping -I vmk1 -d -s 8972`, montar un NFS de laboratorio con `esxcli storage nfs add`.
- Regla: cada tráfico del host tiene su vmk, su VLAN y su prueba de vmkping.
- Fuentes: https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-networking/setting-up-vmkernel-networking/the-vmkernel-networking-layer.html, https://phoenixnap.com/kb/vmware-esxi

## Arco 2. Operación diaria: VMs, snapshots, backups y vCenter
Por qué este arco: es lo que el técnico de soporte toca todas las semanas: crear o recibir VMs, hacer un snapshot antes de un cambio, verificar backups y entrar a vCenter con su propio usuario. Cierra con un circuito seguro de cambio: snapshot con fecha, backup probado y permisos nominales.

### Lección 5. VMs bien armadas
- 3 de 4 fuentes de VMs coinciden en VMware Tools siempre instalado; 2 de 4 en vigilar thin provisioning.
- Idea: VMware Tools es obligatorio en la práctica (balloon, quiesce, heartbeat de HA); discos thin ahorran espacio pero pueden llenar el datastore y frenar la VM; thick eager zeroed para FT; los appliances (.ova) entran por Deploy OVF Template.
- Por qué importa: muchos servidores de video o de control de acceso llegan como OVA o se instalan en VMs; una VM sin Tools o un datastore lleno sobreasignado son llamados de soporte evitables.
- Historia: la documentación oficial avisa que un disco thin puede crecer hasta llenar el datastore y que la VM se detiene si se queda sin espacio: https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-virtual-machine-administration/configuring-virtual-machine-hardwarevsphere-vm-admin/virtual-disk-configurationvsphere-vm-admin/about-virtual-disk-provisioning-policiesvsphere-vm-admin.html
- Laboratorio (Rápido, 10 min): listar VMs con `vim-cmd vmsvc/getallvms`, ver estado de Tools, comparar espacio provisionado contra usado del datastore.
- Regla: ninguna VM queda en producción sin Tools y sin revisar cuánto puede crecer.
- Fuentes: https://knowledge.broadcom.com/external/article/382249/using-esxtop-and-interpreting-esxtop-sta.html, https://open-exam-prep.com/study-guides/vcp-dcv/lifecycle-management-configuration/vm-snapshots-management

### Lección 6. Snapshots con fecha
- 3 de 3 fuentes coinciden: el snapshot no es backup, 2 o 3 por VM, no más de 72 horas. CloudBolt es más estricto: 24 a 72 horas.
- Idea: el snapshot congela el disco base y escribe todo en un delta que crece; depende del disco original. No agrandar discos con snapshots, no cancelar una consolidación.
- Por qué importa: el "snapshot de seguridad" olvidado es una de las causas clásicas de datastore lleno y VMs lentas.
- Historia: "Virtual machine disks consolidation is needed" después de backups nocturnos que fallaron y dejaron deltas: https://open-exam-prep.com/study-guides/vcp-dcv/lifecycle-management-configuration/vm-snapshots-management
- Laboratorio (Rápido, 10 min): crear un snapshot por `vim-cmd`, ver el archivo delta en el datastore, borrarlo y verificar que no quedan deltas.
- Regla: todo snapshot que saco lleva fecha de borrado en el nombre y se borra antes de 72 horas.
- Fuentes: https://knowledge.broadcom.com/external/article/318825/best-practices-for-using-vmware-snapshot.html, https://www.cloudbolt.io/vmware-administration/vmware-snapshot-best-practices/

### Lección 7. Backup que restaura
- 5 de 8 fuentes de backup coinciden: producto que use las APIs de vSphere (VADP con CBT), regla 3-2-1, y elegir bien el modo de transporte.
- Idea: Veeam y similares sacan un snapshot, copian por NBD (red de gestión), HotAdd (proxy virtual) o SAN, y lo borran. El ESXi gratuito no expone VADP: no se puede respaldar así. Un backup que nunca se restauró no está probado.
- Por qué importa: el cliente cree que tiene backup; el técnico es quien lo comprueba.
- Historia: según la guía de Veeam, el modo red en 1 GbE puede rendir 10 a 20 MB/s, lo que hace eternas las restauraciones grandes: https://veeam-best-practices-guide-v9.readthedocs.io/resource_planning/network_mode.html
- Laboratorio (Foco, 20 min): restaurar una VM con otro nombre en un port group sin uplink, arrancarla y verificar; mirar qué modo de transporte usó el job.
- Regla: un backup cuenta cuando lo restauré al menos una vez en un lugar aislado.
- Fuentes: https://developer.broadcom.com/xapis/virtual-disk-api/latest/vddkBkupVadp.9.5.html, https://veeam-best-practices-guide-v9.readthedocs.io/resource_planning/network_mode.html, https://knowledge.broadcom.com/external/article/399823/vmware-esxi-80-update-3e-now-available-a.html

### Lección 8. vCenter y permisos
- 2 de 4 fuentes de vCenter coinciden en dimensionar la VCSA (Tiny pide 14 GB en vSphere 8); 2 de 3 de permisos en el modelo usuario o grupo + rol + objeto.
- Idea: vCenter es un appliance (VCSA) que gestiona muchos hosts y habilita clúster, vMotion, HA y DRS. El acceso pasa por SSO (vsphere.local); administrator@vsphere.local es la llave maestra y se guarda. Cada técnico con su usuario y un rol acotado.
- Por qué importa: con un usuario compartido no se sabe quién hizo qué; con permisos acotados un error no tumba todo.
- Historia: William Lam cuenta que la VCSA Tiny subió de 12 a 14 GB de RAM en vSphere 8, y que él la corrió con 10 GB en laboratorio (no soportado): https://williamlam.com/2022/09/homelab-considerations-for-vsphere-8.html
- Laboratorio (Admin, 15 min): crear un usuario en vsphere.local, clonar el rol Read-only como "Soporte-Lectura", asignarlo en un objeto y probar el login.
- Regla: nadie entra a vCenter con administrator@vsphere.local para tareas del día a día.
- Fuentes: https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-security/vsphere-permissions-and-user-management-tasks.html, https://williamlam.com/2022/09/homelab-considerations-for-vsphere-8.html

## Arco 3. Avanzado y troubleshooting
Por qué este arco: con varios hosts aparecen el clúster, los parches coordinados y los diagnósticos de rendimiento; y en 2026 también la pregunta del cliente sobre irse de VMware. Cierra con un técnico que sabe mover VMs, parchear sin cortes, encontrar el cuello de botella y dar un panorama honesto de salida.

### Lección 9. Clúster y vMotion
- 2 de 4 fuentes de clúster coinciden: HA reinicia VMs (no evita el corte) y funciona sin vCenter; DRS balancea y necesita vCenter. Evidencia moderada; TechTarget es de 2011 y vale por los conceptos.
- Idea: vMotion mueve una VM encendida copiando su memoria a otro host; si cambia solo el host, el disco va en almacenamiento compartido. HA detecta la caída de un host y arranca sus VMs en otro; DRS reparte carga. Crear el clúster es libre, activar HA o DRS requiere licencia.
- Por qué importa: el cliente suele creer que HA es "no se cae nunca"; el técnico explica que es un reinicio automático en minutos.
- Historia: la KB de Broadcom aclara que se puede crear un clúster sin licencia especial, pero activar DRS o HA sí la requiere: https://knowledge.broadcom.com/external/article/308413
- Laboratorio (Foco, 20 min, con vCenter de laboratorio o Hands-On Lab): crear clúster, activar HA, hacer un vMotion y mirar la tarea.
- Regla: a un cliente le digo "HA reinicia en otro host", nunca "no se cae".
- Fuentes: https://knowledge.broadcom.com/external/article/308413, https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vcenter-and-host-management/migrating-virtual-machines-host-management/migration-with-vmotion-host-management.html, https://www.techtarget.com/it-infrastructure/feature/Enabling-VMware-HA-DRS-Advanced-vSphere-features

### Lección 10. Parches sin sustos
- 3 de 4 fuentes de actualización coinciden en el ciclo de Lifecycle Manager: compliance, pre-check, staging, remediate.
- Idea: vLCM vive dentro de vCenter; en vSphere 9 desaparecen las baselines y queda el modelo de imágenes. Host suelto: modo mantenimiento y esxcli. Antes de actualizar, backup del vCenter y del arranque.
- Por qué importa: los parches de seguridad no son opcionales, y un upgrade mal ordenado deja hosts que vCenter no gestiona.
- Historia: la documentación explica que el staging baja los paquetes al host antes, para que el tiempo en modo mantenimiento sea menor: https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/managing-host-and-cluster-lifecycle/about-vsphere-lifecycle-manager-new.html
- Laboratorio (Admin, 15 min): en un host de laboratorio, entrar en mantenimiento por esxcli, listar perfiles de un depot zip y hacer un `--dry-run`.
- Regla: antes de actualizar, backup. Siempre. Y el host va a mantenimiento antes que el parche.
- Fuentes: https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/managing-host-and-cluster-lifecycle/about-vsphere-lifecycle-manager-new.html, https://www.starwindsoftware.com/blog/vmware-cloud-foundation-vcf-9-0-with-vsphere-9-0-and-esxi-9-0-has-been-released/

### Lección 11. Diagnóstico con esxtop
- 4 de 7 fuentes de troubleshooting coinciden: medir con esxtop y leer los logs del host antes de opinar.
- Idea: esxtop por SSH: c para CPU (%RDY), m para memoria (balloon, swap), u para disco (DAVG contra KAVG), n para red. Modo batch a CSV. Logs: vmkernel.log y hostd.log en el host, vpxd en vCenter.
- Por qué importa: "anda lento" se convierte en un número que separa problema de CPU, de disco del storage o de cola del host.
- Historia: la KB de esxtop explica que GAVG es DAVG más KAVG; si DAVG es alto, mirar el storage; KAVG debería estar cerca de cero: https://knowledge.broadcom.com/external/article/382249/using-esxtop-and-interpreting-esxtop-sta.html
- Laboratorio (Foco, 15 min): abrir esxtop, mirar %RDY y DAVG, grabar un minuto en batch, y buscar errores en vmkernel.log.
- Regla: no diagnostico "lentitud" sin un minuto de esxtop guardado.
- Fuentes: https://knowledge.broadcom.com/external/article/382249/using-esxtop-and-interpreting-esxtop-sta.html, https://www.virtualizationhowto.com/2023/07/esxtop-commands-the-ultimate-guide/, https://williamlam.com/2022/09/homelab-considerations-for-vsphere-8.html

### Lección 12. Plan de salida
- 3 de 4 fuentes de migración coinciden en el método (importador de Proxmox contra el host, Tools afuera, VirtIO, de a poco). Broadcom recomienda VCF 9 o VVF 9; Introserv y Redress sostienen que en 2 a 10 hosts chicos la cuenta suele no cerrar.
- Idea: migrar es un proyecto, no un clic. Inventario de licencias, núcleos y funciones usadas; piloto en un host no crítico; importador ESXi de Proxmox VE contra el host (no contra vCenter), en frío, desinstalando Tools y preparando VirtIO.
- Por qué importa: los clientes preguntan; el técnico tiene que dar un panorama honesto, con riesgos y sin vender humo.
- Historia: en agosto y septiembre de 2026 Broadcom retiró las descargas públicas del VDDK, que usan varias herramientas de migración; el importador de Proxmox no depende de él: https://www.virtualizationhowto.com/2026/09/leaving-vmware-just-got-harder-after-broadcom-pulled-vddk-downloads/
- Laboratorio (Campo, 20 min): en un Proxmox VE de laboratorio, agregar el ESXi como storage de importación y migrar una VM de prueba apagada.
- Regla: ninguna migración arranca sin piloto, backup verificado y vuelta atrás.
- Fuentes: https://pve.proxmox.com/wiki/Migrate_to_Proxmox_VE, https://www.thomas-krenn.com/en/wiki/ESXi_VM_importer_-_Proxmox_VE_Storage_Plugin, https://introserv.com/blog/migrating-from-vmware-in-2026-the-end-of-perpetual-licenses-vsphere-8-end-of-support-and-replacement-options/

## Divisiones (decisiones, no lecciones)
- Renovar VMware o migrar. Lado A: Broadcom recomienda VCF 9 o VVF 9 (https://knowledge.broadcom.com/external/article/456708/upcoming-end-of-service-for-vsphere-8-vs.html, https://blogs.vmware.com/cloud-foundation/2026/02/06/global-supports-vmware-cloud-foundation-9-paths-to-adoption). Lado B: en pocos hosts con CPUs de menos de 16 núcleos se paga por núcleos inexistentes y conviene cotizar alternativa (https://introserv.com/blog/migrating-from-vmware-in-2026-the-end-of-perpetual-licenses-vsphere-8-end-of-support-and-replacement-options/, https://redresscompliance.com/vcf-licensing-guide-2026.html). Cómo decidir: contar núcleos licenciables contra físicos, listar qué funciones se usan (vSAN, NSX, DRS) y hacer un piloto; si la relación está cerca de 1 a 1 y se usa el stack, renovar tiene sentido.
- ESXi gratuito en un cliente. Lado A: la KB 399823 lo ofrece como versión de producción sin soporte. Lado B: sin VADP no hay backup a nivel host y Broadcom ya cambió esta política una vez (https://www.it-connect.fr/la-version-gratuite-de-vmware-esxi-free-est-de-retour-en-2025/). Cómo decidir: laboratorio y pruebas sí; producción de un cliente solo si acepta sin soporte y con backup dentro del sistema operativo invitado.
- Hardware fuera de lista. Lado A: parámetros como allowLegacyCPU permiten instalar en CPUs viejas (https://williamlam.com/2025/06/ultimate-lab-resource-for-vcf-9-0.html). Lado B: la documentación oficial exige la Compatibility Guide. Cómo decidir: laboratorio sí, cliente nunca.
- Live-import a Proxmox. Lado A: reduce el corte (wiki de Proxmox). Lado B: si falla se pierde lo escrito, mejor en frío (Thomas-Krenn). Cómo decidir: en frío por defecto; live-import solo con red buena y una VM de prueba antes.
- DRS automático desde el día uno o en manual primero: la única fuente (TechTarget, 2011) sugiere observar en manual y luego automatizar. Cómo decidir: en clústeres chicos de clientes, empezar en Partially Automated una semana.

## Huecos
- Redes, VMkernel y almacenamiento tienen solo 2 páginas cada uno en la lista (documentación oficial más un practicante). Las lecciones 3 y 4 se apoyan en la documentación de Broadcom; faltó una fuente de NIC teaming (políticas de balanceo) y de iSCSI paso a paso.
- Despliegue paso a paso del VCSA y su backup por archivo (puerto 5480) no tienen página leída: la lección 8 lo menciona como concepto.
- EVC solo aparece mencionado en la KB de clúster.
- Backups: la guía de Veeam leída es de la versión 9 (antigua); no hay fuente actual de Veeam 12/13 ni de otros productos. El retiro del VDDK en 2026 podría afectar a productos de backup de terceros: ninguna fuente lo confirma.
- Orden de actualización (vCenter antes que los hosts): no quedó en la lista final ninguna página que lo diga, así que no se enseña como afirmación citada.
- vSphere 9 operativo (pantallas, Host Client 9): sin fuente práctica; el curso enseña sobre vSphere 8 y marca lo que cambia en 9.
- vinfrastructure.it bloqueó el scraper (403) y 4sysops no apareció con páginas útiles antes de agotar el presupuesto de búsqueda.

## Entrega
12 carpetas `class/NN-handle/` con script.txt, card.md y quiz.json; `class/course.json` con la ficha. El audio lo renderiza el orquestador.
