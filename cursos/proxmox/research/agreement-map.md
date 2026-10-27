# Mapa de acuerdos: Proxmox VE en producción

Fuentes: 28 páginas en raw/web (9 oficiales de Proxmox, 19 de practicantes, foro y prensa). Notas en research/notes/a.md y b.md.
M por subtema (páginas con al menos una nota en ese subtema, incluyendo líneas Also): T01 7, T02 2, T03 7, T04 4, T05 2, T06 1, T07 4, T08 4, T09 5, T10 3, T11 7, T12 2, T13 2, T14 2, T15 1, T16 4.

## TH01 Ubicá la versión: Proxmox VE 9.2 sobre Debian 13 es la rama actual; la 8.x quedó sin soporte en agosto de 2026
- Sub-topic: T01 (also T03)
- Agree: 6 of 7. Notes: a:N1, a:N2, b:N1, b:N2, b:N3, b:N4. Urls: https://lists.proxmox.com/pipermail/pve-user/2025-August/017639.html, https://techdirectarchive.com/2026/06/13/how-to-update-proxmox-ve-from-to-the-latest-version-9-2-3-today/, https://vinchin.com/vm-tips/proxmox-ve-9-2.html, https://www.theregister.com/2025/08/11/proxmox_ve9_and_bs4/, https://www.livewatch.de/en/news/read/proxmox-ve-9-0-released-what-s-new, https://pve.proxmox.com/pve-docs/pve-admin-guide.html
- Disagree: none found
- Level: foundation
- Best story: 8.4 con un año de solapamiento, hasta agosto de 2026, https://lists.proxmox.com/pipermail/pve-user/2025-August/017639.html

## TH02 Elegí el hardware pensando en el almacenamiento: nada de ZFS sobre RAID por hardware, SSD con PLP, acceso fuera de banda
- Sub-topic: T02 (also T05)
- Agree: 2 of 2 (thin evidence). Notes: a:N4, a:N6. Urls: https://pve.proxmox.com/pve-docs/pve-admin-guide.html, https://pve.proxmox.com/wiki/Upgrade_from_8_to_9
- Disagree: https://forum.proxmox.com/threads/filesystem-choice-for-consumer-ssd.181212/: usa ZFS aun en SSD de consumo sabiendo que se gastan más
- Level: foundation
- Best story: nombres de NIC que cambian con el kernel nuevo, https://pve.proxmox.com/wiki/Upgrade_from_8_to_9

## TH03 Configurá los repositorios antes de la primera actualización: enterprise con suscripción, no-subscription solo sabiendo lo que implica
- Sub-topic: T03
- Agree: 3 of 7. Notes: a:N7, a:N8, b:N6. Urls: https://pve.proxmox.com/wiki/Package_Repositories, https://pve.proxmox.com/wiki/Upgrade_from_8_to_9, https://techdirectarchive.com/2026/06/13/how-to-update-proxmox-ve-from-to-the-latest-version-9-2-3-today/
- Disagree: https://techdirectarchive.com/2026/06/13/how-to-update-proxmox-ve-from-to-the-latest-version-9-2-3-today/: usa no-subscription como rutina, sin advertencia de producción
- Level: foundation
- Best story: none

## TH04 Actualizá con full-upgrade, nunca con apt upgrade
- Sub-topic: T03
- Agree: 3 of 7. Notes: a:N9, b:N6, a:N10. Urls: https://pve.proxmox.com/pve-docs/pve-admin-guide.html, https://techdirectarchive.com/2026/06/13/how-to-update-proxmox-ve-from-to-the-latest-version-9-2-3-today/, https://pve.proxmox.com/wiki/Upgrade_from_8_to_9
- Disagree: none found
- Level: foundation
- Best story: none

## TH05 Upgrade mayor: backup probado, checklist pve8to9 --full, consola fuera de la GUI, un nodo por vez
- Sub-topic: T03 (also T14)
- Agree: 5 of 7. Notes: a:N10, a:N12, a:N13, b:N2, b:N7. Urls: https://pve.proxmox.com/wiki/Upgrade_from_8_to_9, https://pve.proxmox.com/pve-docs/pve-admin-guide.html, https://vinchin.com/vm-tips/proxmox-ve-9-2.html, https://www.livewatch.de/en/news/read/proxmox-ve-9-0-released-what-s-new, https://lists.proxmox.com/pipermail/pve-user/2025-August/017639.html
- Disagree: none found
- Level: core
- Best story: /etc/sysctl.conf que deja de aplicarse en PVE 9, https://pve.proxmox.com/wiki/Upgrade_from_8_to_9

## TH06 Armá la red en orden: placas físicas, bond, bridge; y aplicá con Apply Configuration o ifreload
- Sub-topic: T04
- Agree: 3 of 4. Notes: a:N14, b:N8, b:N12. Urls: https://pve.proxmox.com/pve-docs/pve-admin-guide.html, https://getlabsdone.com/steps-to-create-proxmox-bridge-with-multiple-ports-using-lacp-bonding/, https://opensourceisfun.substack.com/p/proxmox-setup-part-2-network
- Disagree: none found
- Level: foundation
- Best story: gente que no sabe qué crear primero y termina con VMs sin red, https://getlabsdone.com/steps-to-create-proxmox-bridge-with-multiple-ports-using-lacp-bonding/

## TH07 Usá un bridge VLAN-aware y poné el tag en la placa de la VM
- Sub-topic: T04
- Agree: 3 of 4. Notes: a:N15, b:N10, b:N11. Urls: https://pve.proxmox.com/pve-docs/pve-admin-guide.html, https://getlabsdone.com/steps-to-create-proxmox-bridge-with-multiple-ports-using-lacp-bonding/, https://opensourceisfun.substack.com/p/proxmox-setup-part-2-network
- Disagree: https://opensourceisfun.substack.com/p/proxmox-setup-part-2-network: prefiere Open vSwitch para separar clientes con bridges por cliente
- Level: foundation
- Best story: perder la conexión remota al mover la IP de gestión a una VLAN tagueada, https://getlabsdone.com/steps-to-create-proxmox-bridge-with-multiple-ports-using-lacp-bonding/

## TH08 Bond: LACP 802.3ad si el switch lo soporta, active-backup si no; repartí miembros entre unidades del stack
- Sub-topic: T04 (also T13)
- Agree: 3 of 4. Notes: a:N16, b:N8, b:N9. Urls: https://pve.proxmox.com/pve-docs/pve-admin-guide.html, https://getlabsdone.com/steps-to-create-proxmox-bridge-with-multiple-ports-using-lacp-bonding/, https://opensourceisfun.substack.com/p/proxmox-setup-part-2-network
- Disagree: none found
- Level: core
- Best story: none

## TH09 LVM-thin para empezar simple; ZFS cuando querés integridad, snapshots y replicación y tenés RAM y discos adecuados
- Sub-topic: T05 (also T02)
- Agree: 2 of 2 (thin evidence). Notes: a:N5, a:N17, a:N18, b:N13. Urls: https://pve.proxmox.com/pve-docs/pve-admin-guide.html, https://forum.proxmox.com/threads/filesystem-choice-for-consumer-ssd.181212/
- Disagree: https://forum.proxmox.com/threads/filesystem-choice-for-consumer-ssd.181212/: la regla de 1 GB por TB que cita la guía oficial es falsa según él
- Level: core
- Best story: "I always advocate using ZFS. Please, don't feel compelled to use it.", https://forum.proxmox.com/threads/filesystem-choice-for-consumer-ssd.181212/

## TH10 Dimensioná el ARC de ZFS: 2 GiB base más 1 GiB por TiB
- Sub-topic: T05
- Agree: 1 of 2 (thin evidence). Notes: a:N19. Urls: https://pve.proxmox.com/pve-docs/pve-admin-guide.html
- Disagree: https://forum.proxmox.com/threads/filesystem-choice-for-consumer-ssd.181212/: la RAM necesaria es menos de lo que se repite
- Level: core
- Best story: none

## TH11 Distinguí almacenamiento de archivo y de bloque, y local de compartido, antes de elegir dónde va cada cosa
- Sub-topic: T06 (also T05, T12)
- Agree: 1 of 1 (thin evidence). Notes: a:N20, a:N21, a:N22. Urls: https://pve.proxmox.com/pve-docs/pve-admin-guide.html
- Disagree: none found
- Level: core
- Best story: snapshots qcow2 en NFS que tardan horas, https://pve.proxmox.com/pve-docs/pve-admin-guide.html

## TH12 Ceph es para tres o más nodos idénticos con red dedicada de 10G: si no, no es tu primera opción
- Sub-topic: T06
- Agree: 1 of 1 (thin evidence). Notes: a:N23. Urls: https://pve.proxmox.com/pve-docs/pve-admin-guide.html
- Disagree: none found
- Level: advanced
- Best story: none

## TH13 Creá VMs con VirtIO SCSI single, IO Thread y guest agent activado
- Sub-topic: T07
- Agree: 3 of 4. Notes: a:N25, a:N27, b:N14. Urls: https://pve.proxmox.com/pve-docs/pve-admin-guide.html, https://pve.proxmox.com/wiki/Qemu-guest-agent, https://computingforgeeks.com/create-proxmox-vm-templates-cloud-images/
- Disagree: none found
- Level: foundation
- Best story: none

## TH14 En Windows, elegí la versión de virtio-win que Proxmox marca sin problemas, no la última
- Sub-topic: T07
- Agree: 1 of 4. Notes: a:N26. Urls: https://pve.proxmox.com/wiki/Windows_VirtIO_Drivers
- Disagree: none found
- Level: core
- Best story: 0.1.285 con errores de lectura en Windows Server 2025 y SQL, https://pve.proxmox.com/wiki/Windows_VirtIO_Drivers

## TH15 Elegí el tipo de CPU según si vas a migrar: host en nodo único, el modelo más viejo del clúster si migrás
- Sub-topic: T07 (also T14)
- Agree: 2 of 4. Notes: a:N28, b:N2. Urls: https://pve.proxmox.com/pve-docs/pve-admin-guide.html, https://vinchin.com/vm-tips/proxmox-ve-9-2.html
- Disagree: none found
- Level: core
- Best story: none

## TH16 Hacé una plantilla desde una imagen cloud con cloud-init y desplegá clones en un minuto
- Sub-topic: T08
- Agree: 4 of 4. Notes: a:N30, a:N31, b:N14, b:N16, b:N17. Urls: https://pve.proxmox.com/wiki/Cloud-Init_Support, https://computingforgeeks.com/create-proxmox-vm-templates-cloud-images/, https://www.croit.io/blog/how-to-use-cloud-images-for-faster-vm-deployment-in-proxmox-ve, https://pve.proxmox.com/pve-docs/pve-admin-guide.html
- Disagree: https://pve.proxmox.com/wiki/Cloud-Init_Support: prefiere preparar tu propia imagen antes que usar la lista de la distro
- Level: core
- Best story: menos de un minuto contra veinte de ISO, https://computingforgeeks.com/create-proxmox-vm-templates-cloud-images/

## TH17 Full clone para producción; linked clone para laboratorio
- Sub-topic: T08
- Agree: 2 of 4. Notes: b:N15, b:N17. Urls: https://computingforgeeks.com/create-proxmox-vm-templates-cloud-images/, https://www.croit.io/blog/how-to-use-cloud-images-for-faster-vm-deployment-in-proxmox-ve
- Disagree: https://pve.proxmox.com/wiki/Cloud-Init_Support: destaca los linked clones como el método rápido de despliegue
- Level: core
- Best story: borrar la plantilla rompe todos los linked clones, https://computingforgeeks.com/create-proxmox-vm-templates-cloud-images/

## TH18 Contenedores no privilegiados por defecto; privilegiados solo en entornos de confianza
- Sub-topic: T09
- Agree: 2 of 5. Notes: a:N33, b:N19. Urls: https://pve.proxmox.com/pve-docs/pve-admin-guide.html, https://forum.proxmox.com/threads/proxmox-7-1-and-docker-lxc-vs-vm.105140/
- Disagree: none found
- Level: foundation
- Best story: none

## TH19 Docker va en una VM, no en LXC ni en el host
- Sub-topic: T09
- Agree: 3 of 5. Notes: a:N34, b:N18, b:N20. Urls: https://pve.proxmox.com/pve-docs/pve-admin-guide.html, https://www.wundertech.net/how-to-run-docker-in-proxmox-on-a-vm/, https://forum.hhf.technology/t/docker-in-proxmox-pros-and-cons-of-using-vms-lxcs-and-bare-metal/342
- Disagree: https://forum.proxmox.com/threads/proxmox-7-1-and-docker-lxc-vs-vm.105140/: con hardware limitado prefiere LXC por recursos; https://www.wundertech.net/how-to-run-docker-in-proxmox-on-a-vm/ admite que LXC le anduvo sin problemas
- Level: core
- Best story: un homelab con i5 y 20 GB que quiere un CT por contenedor Docker, https://forum.proxmox.com/threads/proxmox-7-1-and-docker-lxc-vs-vm.105140/

## TH20 Backups en modo snapshot con guest agent; stop cuando la consistencia manda
- Sub-topic: T10
- Agree: 2 of 3. Notes: a:N37, a:N27. Urls: https://pve.proxmox.com/pve-docs/pve-admin-guide.html, https://pve.proxmox.com/wiki/Qemu-guest-agent
- Disagree: none found
- Level: foundation
- Best story: none

## TH21 Un backup que no restauraste no es un backup: probá restores a una VM nueva
- Sub-topic: T10 (also T11)
- Agree: 3 of 3. Notes: a:N43, a:N38, b:N26. Urls: https://pbs.proxmox.com/docs/storage.html, https://pve.proxmox.com/pve-docs/pve-admin-guide.html, https://xaweho.de/en/wissen/proxmox-backup
- Disagree: none found
- Level: core
- Best story: none

## TH22 Con PBS: prune decide qué se borra, garbage collection libera el espacio, verify detecta corrupción
- Sub-topic: T11
- Agree: 5 of 7. Notes: a:N40, a:N42, b:N22, b:N23, b:N25. Urls: https://pbs.proxmox.com/docs/maintenance.html, https://www.thomas-krenn.com/en/wiki/Proxmox_Backup_Server_configuration, https://hakedev.substack.com/p/complete-proxmox-backup-server-setup, https://support.tuxis.nl/en/knowledgebase/article/how-to-setup-a-prune-job-and-garbage-collection, https://xaweho.de/en/wissen/proxmox-backup
- Disagree: https://www.thomas-krenn.com/en/wiki/Proxmox_Backup_Server_configuration: GC diario o semanal; la doc oficial arranca con semanal
- Level: core
- Best story: GC con período de gracia de 24 horas y 5 minutos, https://pbs.proxmox.com/docs/maintenance.html

## TH23 Retené de más al principio: siempre podés achicar, nunca recrear el pasado
- Sub-topic: T11
- Agree: 3 of 7. Notes: a:N41, b:N22, b:N23. Urls: https://pbs.proxmox.com/docs/maintenance.html, https://www.thomas-krenn.com/en/wiki/Proxmox_Backup_Server_configuration, https://hakedev.substack.com/p/complete-proxmox-backup-server-setup
- Disagree: https://hakedev.substack.com/p/complete-proxmox-backup-server-setup: retención corta de homelab (3 últimos, 7 diarios, 4 semanales, 2 mensuales)
- Level: core
- Best story: none

## TH24 Conectá PVE a PBS con un usuario que pueda escribir pero no borrar, y sacá una copia fuera del sitio
- Sub-topic: T11
- Agree: 3 of 7. Notes: a:N43, b:N23, b:N24. Urls: https://pbs.proxmox.com/docs/storage.html, https://hakedev.substack.com/p/complete-proxmox-backup-server-setup, https://xaweho.de/en/wissen/proxmox-backup
- Disagree: https://www.thomas-krenn.com/en/wiki/Proxmox_Backup_Server_configuration: conecta con root@pam
- Level: core
- Best story: verify jobs que fallan cuando un ransomware cifra backups, https://pbs.proxmox.com/docs/storage.html

## TH25 Un snapshot no es un backup: vive en el mismo storage y sirve para volver atrás antes de un cambio
- Sub-topic: T12
- Agree: 2 of 2 (thin evidence). Notes: a:N20, a:N45, a:N46, a:N37. Urls: https://pve.proxmox.com/pve-docs/pve-admin-guide.html, https://lists.proxmox.com/pipermail/pve-user/2025-August/017639.html
- Disagree: none found
- Level: foundation
- Best story: none

## TH26 Un clúster necesita mayoría: tres nodos, o dos más un QDevice
- Sub-topic: T13
- Agree: 2 of 2 (thin evidence). Notes: a:N47, a:N49, b:N27. Urls: https://pve.proxmox.com/pve-docs/pve-admin-guide.html, https://forum.proxmox.com/threads/2-nodes-proxmox-cluster-qdevice.181580/
- Disagree: none found
- Level: foundation
- Best story: dos nodos, prueba de falla, la HA no conmuta, https://forum.proxmox.com/threads/2-nodes-proxmox-cluster-qdevice.181580/

## TH27 Dale a corosync su propia red de baja latencia y un segundo enlace
- Sub-topic: T13
- Agree: 1 of 2 (thin evidence). Notes: a:N48, a:N16. Urls: https://pve.proxmox.com/pve-docs/pve-admin-guide.html
- Disagree: none found
- Level: core
- Best story: none

## TH28 Antes de unir un nodo, vacialo: no puede tener VMs
- Sub-topic: T13
- Agree: 1 of 2 (thin evidence). Notes: a:N50. Urls: https://pve.proxmox.com/pve-docs/pve-admin-guide.html
- Disagree: none found
- Level: core
- Best story: none

## TH29 HA solo con fencing, almacenamiento compartido y tres votos; para mantenimiento, disarm
- Sub-topic: T14
- Agree: 2 of 2 (thin evidence). Notes: a:N51, a:N53, a:N52, b:N1. Urls: https://pve.proxmox.com/pve-docs/pve-admin-guide.html, https://pve.proxmox.com/wiki/Upgrade_from_8_to_9
- Disagree: none found
- Level: core
- Best story: la VM que escribe desde dos nodos y destruye el disco, https://pve.proxmox.com/pve-docs/pve-admin-guide.html

## TH30 Migración en vivo con CPUs del mismo fabricante y misma versión o superior en destino
- Sub-topic: T14
- Agree: 2 of 2 (thin evidence). Notes: a:N13, a:N28, a:N36. Urls: https://pve.proxmox.com/wiki/Upgrade_from_8_to_9, https://pve.proxmox.com/pve-docs/pve-admin-guide.html
- Disagree: none found
- Level: core
- Best story: none

## TH31 Un usuario por persona con el rol justo, y 2FA con claves de recuperación guardadas
- Sub-topic: T15
- Agree: 1 of 1 (thin evidence). Notes: a:N55, a:N56, a:N57. Urls: https://pve.proxmox.com/pve-docs/pve-admin-guide.html
- Disagree: none found
- Level: core
- Best story: none

## TH32 Habilitá el firewall con una sesión SSH abierta y el IPSet management cargado
- Sub-topic: T16
- Agree: 2 of 4. Notes: a:N58, a:N60, b:N28. Urls: https://pve.proxmox.com/pve-docs/pve-admin-guide.html, https://diegocarrasco.com/regain-access-proxmox-firewall-misconfiguration/
- Disagree: none found
- Level: core
- Best story: quedarse afuera en Hetzner y volver editando config.db, https://diegocarrasco.com/regain-access-proxmox-firewall-misconfiguration/

## TH33 Troubleshooting en orden: quórum, logs, locks, almacenamiento
- Sub-topic: T16 (also T13)
- Agree: 3 of 4. Notes: a:N61, a:N46, a:N29, b:N5. Urls: https://pve.proxmox.com/pve-docs/pve-admin-guide.html, https://pve.proxmox.com/wiki/Upgrade_from_8_to_9, https://www.flane.de/course/innovator-pveicm
- Disagree: none found
- Level: advanced
- Best story: los siete escenarios de romper y arreglar del curso de PVE 9, https://www.flane.de/course/innovator-pveicm

## The big splits
- Repositorio no-subscription en producción: la wiki oficial dice que no (https://pve.proxmox.com/wiki/Package_Repositories); guías de practicantes lo usan sin advertencia (https://techdirectarchive.com/2026/06/13/how-to-update-proxmox-ve-from-to-the-latest-version-9-2-3-today/). Gira en torno a presupuesto, soporte y tolerancia a riesgo.
- Docker en LXC o en VM: oficial y WunderTech dicen VM (https://pve.proxmox.com/pve-docs/pve-admin-guide.html, https://www.wundertech.net/how-to-run-docker-in-proxmox-on-a-vm/); foro y hhf muestran que LXC funciona y ahorra recursos (https://forum.proxmox.com/threads/proxmox-7-1-and-docker-lxc-vs-vm.105140/, https://forum.hhf.technology/t/docker-in-proxmox-pros-and-cons-of-using-vms-lxcs-and-bare-metal/342). Gira en torno a aislamiento contra recursos.
- ZFS en SSD de consumo y cuánta RAM: guía oficial (https://pve.proxmox.com/pve-docs/pve-admin-guide.html) contra foro (https://forum.proxmox.com/threads/filesystem-choice-for-consumer-ssd.181212/).
- Linked o full clone: wiki oficial (https://pve.proxmox.com/wiki/Cloud-Init_Support) contra computingforgeeks y croit.
- Usuario de conexión a PBS: root@pam (https://www.thomas-krenn.com/en/wiki/Proxmox_Backup_Server_configuration) contra usuario dedicado que no puede borrar (https://hakedev.substack.com/p/complete-proxmox-backup-server-setup).

## Coverage gaps
- T06, T15: solo la guía oficial. No hay practicante leído sobre NFS/CIFS en obra ni sobre usuarios y 2FA.
- T13, T14: pocas fuentes independientes; la base es la guía oficial más un hilo del foro. No se leyó ningún caso de HA real en producción.
- T05: el desgaste de SSD es afirmación del foro, sin medición propia leída.
- Lo que un técnico esperaría y nadie cubrió en profundidad: importar VMs desde VMware (solo mencionado en el curso de Fast Lane), passthrough de PCI/USB (por ejemplo una placa capturadora o un dongle de licencia), monitoreo con métricas externas, y el aviso de suscripción en la GUI.
