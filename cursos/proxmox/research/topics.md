# Mapa del tema: Proxmox VE en producción (nivel inicial a intermedio)

Cómo se enseña: el curso oficial y los cursos de partners (por ejemplo "Proxmox VE 9.x: Install, Configure, Manage" de Fast Lane, https://www.flane.de/course/innovator-pveicm) arrancan por un host único (instalación, repositorios, red, almacenamiento local, VMs, plantillas, contenedores) y después pasan a clúster (corosync y quórum, almacenamiento compartido, migración, HA, firewall, backup con Proxmox Backup Server). La guía de administración oficial (pve-admin-guide) sigue el mismo orden por capítulos. Este mapa sigue ese orden, recortado a lo que un técnico de obra y soporte necesita.

Versión de referencia: Proxmox VE 9.2 (publicada el 21 de mayo de 2026, Debian 13.5 "Trixie", kernel 7.0) y Proxmox Backup Server 4.x. Proxmox VE 8.4 tuvo soporte de seguridad hasta agosto de 2026.

- T01 Qué es Proxmox VE, versiones y ciclo de vida (KVM + LXC sobre Debian, 9.x vs 8.x, soporte)
- T02 Instalación y hardware (requisitos, RAID por hardware vs ZFS, SSD con PLP, acceso fuera de banda)
- T03 Repositorios y actualizaciones (enterprise vs no-subscription, formato deb822, full-upgrade, upgrades mayores)
- T04 Red del host (Linux bridge, VLAN-aware, bonds LACP/active-backup, aplicar cambios con ifreload)
- T05 Almacenamiento local (LVM-thin, ZFS, directorio, ARC, desgaste de SSD)
- T06 Almacenamiento compartido (NFS, CIFS, iSCSI con LVM, Ceph como panorama, la marca "shared")
- T07 Máquinas virtuales KVM (VirtIO SCSI, drivers virtio-win, guest agent, tipo de CPU)
- T08 Plantillas, clones y cloud-init (imágenes cloud, full vs linked clone)
- T09 Contenedores LXC (no privilegiados vs privilegiados, Docker en LXC vs VM, imágenes OCI)
- T10 Backups con vzdump (modos stop/suspend/snapshot, retención, restauración, prueba de restore)
- T11 Proxmox Backup Server (datastore, prune, garbage collection, verify, sync, permisos, ransomware, 3-2-1)
- T12 Snapshots (qué son, dónde viven, snapshots en LVM de PVE 9, diferencia con backup)
- T13 Clúster (corosync, quórum, red de clúster, 3 nodos, QDevice para 2 nodos)
- T14 Migración y alta disponibilidad (live migration, tipo de CPU, HA, fencing por watchdog, disarm en 9.2, replicación)
- T15 Usuarios, permisos y 2FA (realms PAM/PVE, roles, API tokens, TOTP, claves de recuperación)
- T16 Firewall y troubleshooting (habilitar sin quedarse afuera, IPSet management, locks, quórum perdido, rescate)
