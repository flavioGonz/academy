# Notes: batch b (practicantes, foro y prensa)
Pages read: 18. With notes: 17. Skipped: 1 (xaweho.de es un índice de artículos de un proveedor de PBS alojado, sin contenido propio salvo títulos; se usa solo como señal de qué temas importan). Bias anotado donde un sitio vende backup o servicios.

## T01 Qué es Proxmox VE, versiones y ciclo de vida
- b:N1. Proxmox VE 9.2 salió el 21 de mayo de 2026 sobre Debian 13.5, kernel 7.0, QEMU 11.0, LXC 7.0, ZFS 2.4 y Ceph Tentacle 20.2 por defecto. Trae balanceador dinámico de carga en el CRS, HA arm/disarm, gestión de modelos de CPU personalizados y SDN con WireGuard y BGP.
  - Source: https://techdirectarchive.com/2026/06/13/how-to-update-proxmox-ve-from-to-the-latest-version-9-2-3-today/  Quote: "introduces Linux kernel 7.0 as its new stable default"
  - Kind: definition
  - Level: foundation
- b:N2. Misma información de 9.2 desde un vendedor de backup; agrega que antes de actualizar conviene validar passthrough de GPU, NICs con drivers propios y controladoras de almacenamiento especiales con el kernel nuevo.
  - Source: https://vinchin.com/vm-tips/proxmox-ve-9-2.html  Quote: "administrators should still validate compatibility before production upgrades"
  - Kind: rule of thumb
  - Level: core
  - Also: T03
  - Bias: vende Vinchin Backup & Recovery.
- b:N3. Proxmox VE es Debian modificado más KVM/QEMU, LXC, ZFS integrado en el kernel y Ceph, con una GUI web propia. PBS 4.0 salió junto con PVE 9 sobre la misma base, con soporte S3 en preview.
  - Source: https://www.theregister.com/2025/08/11/proxmox_ve9_and_bs4/  Quote: "Proxmox is built from several separate FOSS products"
  - Kind: definition
  - Level: foundation
  - Also: T11
- b:N4. PVE 9.0: expansión de RAID-Z agregando un disco sin reconstruir, snapshots en LVM grueso (tech preview), afinidad en HA, nueva interfaz móvil.
  - Source: https://www.livewatch.de/en/news/read/proxmox-ve-9-0-released-what-s-new  Quote: "dynamic expansion of RAID-Z pools is now possible"
  - Kind: definition
  - Level: foundation
  - Bias: vende monitoreo de servidores.
- b:N5. El curso de partner de 5 días para PVE 9.x incluye siete escenarios de "romper y arreglar": deriva de repositorios, VLAN mal configurada, pérdida de quórum, falla de OSD, firmware equivocado tras importar. Pensado para administradores que vienen de VMware tras Broadcom.
  - Source: https://www.flane.de/course/innovator-pveicm  Quote: "Repository-Drift, VLAN-Fehlkonfiguration, Quorum-Verlust"
  - Kind: story
  - Level: foundation
  - Also: T16
  - Bias: vende el curso.

## T03 Repositorios y actualizaciones
- b:N6. Una actualización menor (9.0 a 9.1, 9.1 a 9.2) es apt update más apt dist-upgrade o el botón Upgrade del nodo, y después reiniciar. "pveversion -v" muestra la versión real (pve-manager 9.2.3 dentro de la rama 9.2).
  - Source: https://techdirectarchive.com/2026/06/13/how-to-update-proxmox-ve-from-to-the-latest-version-9-2-3-today/  Quote: "The most reliable way to verify your installed Proxmox VE version"
  - Kind: technique
  - Level: foundation
- b:N7. Antes del upgrade mayor: backups, deshabilitar repos de terceros, revisar compatibilidad de Ceph y ZFS, leer cambios incompatibles.
  - Source: https://www.livewatch.de/en/news/read/proxmox-ve-9-0-released-what-s-new  Quote: "Disable third-party repositories"
  - Kind: rule of thumb
  - Level: core

## T04 Red del host
- b:N8. Orden correcto: bond (con las placas físicas como esclavas y modo 802.3ad, miimon 100, hash layer2+3) y encima el bridge vmbr0 con bridge-ports bond0. Mucha gente se confunde sobre qué crear primero y termina con VMs sin red.
  - Source: https://getlabsdone.com/steps-to-create-proxmox-bridge-with-multiple-ports-using-lacp-bonding/  Quote: "Many users new to Proxmox get confused and do not know what to create first"
  - Kind: mistake
  - Level: foundation
- b:N9. En un switch apilado, repartir los miembros del port-channel entre dos unidades del stack, así una unidad caída no corta el servidor. El port-channel del switch va en trunk con las VLANs permitidas.
  - Source: https://getlabsdone.com/steps-to-create-proxmox-bridge-with-multiple-ports-using-lacp-bonding/  Quote: "take the first two ports from the first stack member and the second pair from the second member"
  - Kind: technique
  - Level: core
- b:N10. Para que la gestión ande en VLAN tagueada, la PC de gestión tiene que estar en un puerto access de esa VLAN; al aplicar el cambio remotamente se pierde la conexión.
  - Source: https://getlabsdone.com/steps-to-create-proxmox-bridge-with-multiple-ports-using-lacp-bonding/  Quote: "you will lose the network connectivity to the Proxmox server after performing the next step"
  - Kind: mistake
  - Level: core
- b:N11. Alternativa: Open vSwitch (apt install openvswitch-switch) con OVS Bond LACP balance-tcp e IntPorts para IPs de host en VLAN. Sin tag, el puerto de la VM es trunk. OVS no pasa tráfico con SR-IOV activo.
  - Source: https://opensourceisfun.substack.com/p/proxmox-setup-part-2-network  Quote: "OVS bridging doesn’t work if SR-IOV is enabled"
  - Kind: technique
  - Level: advanced
- b:N12. Un bond necesita al menos dos miembros para levantar; aun así conviene usar el nombre del bond para poder agregar placas después.
  - Source: https://opensourceisfun.substack.com/p/proxmox-setup-part-2-network  Quote: "a bond requires at least two member interfaces"
  - Kind: mistake
  - Level: core

## T05 Almacenamiento local
- b:N13. Contras de ZFS en SSD de consumo según un miembro veterano del foro: más desgaste (el SSD dura menos que con LVM/ext4) y más escritura, sin PLP para diferir escrituras. La vieja regla "1 GB de RAM por TB" es falsa. Él igual recomienda ZFS donde se pueda.
  - Source: https://forum.proxmox.com/threads/filesystem-choice-for-consumer-ssd.181212/  Quote: "the old rule of "1 GB Ram per 1 TB of disk space" is bogus"
  - Kind: rule of thumb
  - Level: core

## T08 Plantillas, clones y cloud-init
- b:N14. Imagen cloud a plantilla: qm create con VirtIO SCSI y agente, qm importdisk al storage, qm set --scsi0, --boot order=scsi0, --ide2 storage:cloudinit, ciuser, sshkeys, ipconfig0, qm resize, qm template. Clonar lleva menos de un minuto contra 20 de instalar desde ISO (su cálculo).
  - Source: https://computingforgeeks.com/create-proxmox-vm-templates-cloud-images/  Quote: "Cloning a VM from a template takes under a minute."
  - Kind: template
  - Level: core
- b:N15. Linked clone ahorra disco pero si se borra la plantilla, todos los linked clones se rompen: full clone para lo que vive en producción.
  - Source: https://computingforgeeks.com/create-proxmox-vm-templates-cloud-images/  Quote: "if you delete the template, all linked clones break"
  - Kind: mistake
  - Level: core
- b:N16. Después de cambiar parámetros de cloud-init en un clon, "qm cloudinit update ID" regenera el ISO; con el agente, "qm agent ID network-get-interfaces" devuelve la IP.
  - Source: https://computingforgeeks.com/create-proxmox-vm-templates-cloud-images/  Quote: "Regenerate the cloud-init ISO after changes"
  - Kind: technique
  - Level: core
- b:N17. croit recomienda clonar la plantilla como Full Clone para que la VM sea independiente, y usar consola xterm.js con serial para ver el arranque con scroll.
  - Source: https://www.croit.io/blog/how-to-use-cloud-images-for-faster-vm-deployment-in-proxmox-ve  Quote: "the clone mode should be “Full Clone”"
  - Kind: technique
  - Level: core
  - Bias: empresa de servicios Ceph/Proxmox.

## T09 Contenedores LXC
- b:N18. WunderTech (Proxmox 9.1, clúster de dos nodos propio): para Docker, VM. LXC usa menos recursos y le anduvo sin problemas, pero la recomendación del equipo de Proxmox es VM por aislamiento: kernel propio. Arranque sugerido 2 a 4 vCPU, 4 GB, 32 GB de disco.
  - Source: https://www.wundertech.net/how-to-run-docker-in-proxmox-on-a-vm/  Quote: "The short answer is to use a VM."
  - Kind: rule of thumb
  - Level: core
- b:N19. En el foro oficial, un usuario arma la lista: Docker en LXC gasta menos y permite restaurar archivos sueltos desde PBS; pero aísla menos, algunos contenedores piden modo privilegiado y los backups tardan más. Docker en VM: aislamiento máximo, funciona como nativo, backups PBS más rápidos.
  - Source: https://forum.proxmox.com/threads/proxmox-7-1-and-docker-lxc-vs-vm.105140/  Quote: "some containers might not work and need the option “privileged container”"
  - Kind: rule of thumb
  - Level: core
- b:N20. Comparación VM vs LXC vs bare metal para Docker: LXC es liviano pero comparte kernel, un compromiso puede afectar al host; VMs permiten migración en vivo y HA.
  - Source: https://forum.hhf.technology/t/docker-in-proxmox-pros-and-cons-of-using-vms-lxcs-and-bare-metal/342  Quote: "Running Docker inside LXCs is common, although it’s not officially recommended"
  - Kind: rule of thumb
  - Level: core

## T11 Proxmox Backup Server
- b:N21. Thomas Krenn: PBS se administra en https://IP:8007; crear pool ZFS (espejo o RAIDZ2) como datastore; Proxmox recomienda solo SSD para backup, o un special device si hay discos rotativos. En PVE se agrega en Datacenter, Storage, Add, Proxmox Backup Server, con el fingerprint del dashboard de PBS.
  - Source: https://www.thomas-krenn.com/en/wiki/Proxmox_Backup_Server_configuration  Quote: "Proxmox recommends SSD-only for backup storage."
  - Kind: technique
  - Level: core
  - Bias: vende servidores y suscripciones.
- b:N22. Thomas Krenn explica que prune no genera carga y puede correr cuando sea; garbage collection sí carga el storage; recomiendan GC diario o semanal y una fase de prueba con el simulador.
  - Source: https://www.thomas-krenn.com/en/wiki/Proxmox_Backup_Server_configuration  Quote: "No load is created on the storage during the process"
  - Kind: rule of thumb
  - Level: core
- b:N23. Hake Hardware: usuario dedicado backup@pbs con API token y rol DatastoreBackup sobre el datastore, que permite crear backups pero no borrarlos, así un nodo comprometido no puede eliminar lo existente. Horario: prune 21:30, backup 22:00, verify 01:00, GC domingos 02:00.
  - Source: https://hakedev.substack.com/p/complete-proxmox-backup-server-setup  Quote: "DatastoreBackup role allows creating backups but not deleting them"
  - Kind: template
  - Level: core
- b:N24. Hake Hardware: disco separado para el datastore, así reinstalar el sistema no toca los backups. Un solo disco para todo es aceptable para 5 a 10 VMs pero si muere, se pierden también los backups.
  - Source: https://hakedev.substack.com/p/complete-proxmox-backup-server-setup  Quote: "OS disk failure means losing backups too"
  - Kind: rule of thumb
  - Level: core
- b:N25. Tuxis recomienda fijar la retención en el datastore de PBS y no en el job de PVE, y activar el botón de habilitado del prune job, que es un olvido común.
  - Source: https://support.tuxis.nl/en/knowledgebase/article/how-to-setup-a-prune-job-and-garbage-collection  Quote: "The best option is to set retentions on your Proxmox backup datastore."
  - Kind: mistake
  - Level: core
  - Bias: proveedor de PBS alojado.
- b:N26. Un proveedor de PBS alojado ordena su base de conocimiento en: datastore, cifrado del lado cliente, primer backup manual de prueba, job programado, restore completo, restore de archivo suelto, verify, prune, GC, retención, sync a segundo PBS, protección contra ransomware, deduplicación ("100 GB de backups ocupan 30 GB", su cifra).
  - Source: https://xaweho.de/en/wissen/proxmox-backup  Quote: "Why 100 GB of backups often occupy just 30 GB"
  - Kind: number
  - Level: foundation
  - Bias: vende PBS alojado.

## T13 Clúster
- b:N27. Caso real del foro (marzo 2026): con dos nodos, en las pruebas de falla, al caer uno el clúster pierde quórum y la HA no hace failover. El usuario descubre el QDevice y pregunta si puede ponerlo en otra sede.
  - Source: https://forum.proxmox.com/threads/2-nodes-proxmox-cluster-qdevice.181580/  Quote: "when one node becomes unavailable, the cluster loses quorum and HA cannot properly perform failover"
  - Kind: story
  - Level: core

## T16 Firewall y troubleshooting
- b:N28. Diego Carrasco habilitó el firewall con una configuración incorrecta en un servidor Hetzner y quedó afuera. La salida: arrancar en modo rescate, montar la raíz, abrir /var/lib/pve-cluster/config.db con sqlite3 y cambiar "enable: 1" por "enable: 0" en cluster.fw. La configuración de /etc/pve vive en esa base SQLite.
  - Source: https://diegocarrasco.com/regain-access-proxmox-firewall-misconfiguration/  Quote: "I made a noob mistake and locked myself out of my server."
  - Kind: story
  - Level: advanced

## Disagreements seen
- Docker en LXC: WunderTech y el FAQ oficial dicen VM (https://www.wundertech.net/how-to-run-docker-in-proxmox-on-a-vm/); el foro y hhf muestran que mucha gente lo corre en LXC por recursos (https://forum.proxmox.com/threads/proxmox-7-1-and-docker-lxc-vs-vm.105140/, https://forum.hhf.technology/t/docker-in-proxmox-pros-and-cons-of-using-vms-lxcs-and-bare-metal/342).
- Linked vs full clone: la wiki oficial destaca linked clones rápidos desde plantilla (https://pve.proxmox.com/wiki/Cloud-Init_Support); computingforgeeks y croit recomiendan full clone para producción (https://computingforgeeks.com/create-proxmox-vm-templates-cloud-images/, https://www.croit.io/blog/how-to-use-cloud-images-for-faster-vm-deployment-in-proxmox-ve).
- GC: la doc de PBS sugiere semanal; Thomas Krenn diario o semanal (https://www.thomas-krenn.com/en/wiki/Proxmox_Backup_Server_configuration).
- Imágenes cloud: Proxmox recomienda preparar la propia imagen (https://pve.proxmox.com/wiki/Cloud-Init_Support); computingforgeeks y croit usan directamente las imágenes oficiales de las distros.
- ZFS en SSD de consumo: la guía oficial desaconseja SSD de consumo; el foro dice que ZFS los gasta más pero igual lo prefiere por sus ventajas (https://forum.proxmox.com/threads/filesystem-choice-for-consumer-ssd.181212/).

## Best stories
- Dos nodos, prueba de falla, la HA no conmuta: https://forum.proxmox.com/threads/2-nodes-proxmox-cluster-qdevice.181580/
- Quedarse afuera por el firewall y volver editando la base SQLite desde rescate: https://diegocarrasco.com/regain-access-proxmox-firewall-misconfiguration/
- Clonar en menos de un minuto contra 20 minutos de ISO: https://computingforgeeks.com/create-proxmox-vm-templates-cloud-images/
- Rol DatastoreBackup: el nodo puede escribir backups pero no borrarlos: https://hakedev.substack.com/p/complete-proxmox-backup-server-setup
- Siete escenarios de romper y arreglar del curso de PVE 9: https://www.flane.de/course/innovator-pveicm
