# Mapa del tema: VMware vSphere (ESXi y vCenter) para técnicos integradores

Nivel: inicial a intermedio. Público: técnicos instaladores y de soporte con base de redes.
Cómo se enseña (búsqueda): el curso oficial "VMware vSphere Foundation: Build, Manage, and Operate [V9.0]" (Global Knowledge / Arrow), la guía del examen VCP-VVF Administrator (docs.broadcom.com), las guías de techdocs.broadcom.com de vSphere 8.0 (ESXi Installation and Setup, Networking, Storage, VM Administration, Availability, Lifecycle Manager, Security, Monitoring), guías de estudio VCP-DCV y blogs de practicantes (William Lam, virtualizationhowto, vinfrastructure).

- T01 Licenciamiento y ciclo de vida post-Broadcom: VVF, VCF, VCF Edge, ediciones previas, ESXi gratuito, fin de soporte de vSphere 8, vSphere 9 / VCF 9.x.
- T02 Hardware y compatibilidad: requisitos de ESXi 8, HCL / Broadcom Compatibility Guide, CPUs y NICs deprecadas, medio de arranque (SD/USB vs disco persistente).
- T03 Instalación de ESXi y configuración inicial: instalador, DCUI, red de gestión, DNS, NTP.
- T04 Host Client y gestión de un host suelto: interfaz web del host, SSH, ESXi Shell.
- T05 Redes estándar: vSwitch estándar, port groups, VLAN ID, uplinks, NIC teaming.
- T06 VMkernel: adaptadores vmk, pilas TCP/IP, separación de tráfico (gestión, vMotion, almacenamiento IP).
- T07 Almacenamiento: datastores VMFS, NFS, iSCSI, jumbo frames, multipathing.
- T08 Máquinas virtuales: VMware Tools, hardware virtual, VMXNET3, discos thin/thick, plantillas y OVF.
- T09 Snapshots: qué son, límites, consolidación, por qué no son backup.
- T10 vCenter (VCSA): despliegue, requisitos, inventario, backup basado en archivos.
- T11 Clúster, vMotion, HA y DRS: requisitos, cómo funcionan, control de admisión, EVC.
- T12 Backups: VADP, CBT, modos de transporte (NBD, HotAdd, SAN), Veeam y otros, 3-2-1.
- T13 Parches y actualizaciones: vSphere Lifecycle Manager, imágenes vs baselines, modo mantenimiento.
- T14 Usuarios, roles y permisos: SSO, vsphere.local, roles, privilegios mínimos.
- T15 Troubleshooting: logs de ESXi y vCenter, esxtop, modo mantenimiento, red de gestión.
- T16 Migración a otras plataformas: Proxmox VE (importador ESXi), XCP-ng, otras; preparación de VMs.
