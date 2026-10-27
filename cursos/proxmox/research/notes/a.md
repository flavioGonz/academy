# Notes: batch a (documentación oficial de Proxmox)
Pages read: 10. With notes: 9. Skipped: 1 (la página de video "What's new in Proxmox VE 9.2" no se guardó por ser JavaScript; la reemplaza el anuncio en lists y la página de vinchin del lote b).

Páginas: pve-admin-guide, Package_Repositories, Upgrade_from_8_to_9, Cloud-Init_Support, Qemu-guest-agent, Windows_VirtIO_Drivers, pbs maintenance, pbs storage, lists.proxmox.com anuncio 9.0.

## T01 Qué es Proxmox VE, versiones y ciclo de vida
- a:N1. Proxmox VE 9.0 salió el 5 de agosto de 2025 sobre Debian 13 "Trixie" con kernel 6.14, QEMU 10, LXC 6, ZFS 2.3.3 y Ceph Squid 19.2. Novedades: snapshots como cadena de volúmenes en almacenamiento de bloques (iSCSI, FC), reglas de afinidad para HA, fabrics de SDN.
  - Source: https://lists.proxmox.com/pipermail/pve-user/2025-August/017639.html  Quote: "first stable release of Proxmox Virtual Environment v9.0"
  - Kind: definition
  - Level: foundation
- a:N2. Proxmox VE 8.4 recibe actualizaciones de seguridad y correcciones críticas hasta agosto de 2026, un año de solapamiento con 9.0 para planificar la migración. A octubre de 2026 la rama 8 ya quedó fuera de soporte.
  - Source: https://lists.proxmox.com/pipermail/pve-user/2025-August/017639.html  Quote: "will receive security updates and critical bug fixes until August 2026"
  - Kind: number
  - Level: foundation
  - Also: T03
- a:N3. Proxmox VE se apoya en KVM/QEMU para VMs y LXC para contenedores, con HA integrada (sin Pacemaker) que detecta fallas de nodo con fencing por watchdog.
  - Source: https://pve.proxmox.com/pve-docs/pve-admin-guide.html  Quote: "No external tools like Pacemaker are needed"
  - Kind: definition
  - Level: foundation

## T02 Instalación y hardware
- a:N4. Requisitos recomendados: CPU con VT/AMD-V, 2 GB para el sistema más la RAM de los invitados, y para ZFS o Ceph aproximadamente 1 GB por TB usado. ZFS y Ceph no son compatibles con una controladora RAID por hardware. Se desaconsejan los SSD de consumo; se recomiendan SSD con protección contra corte de energía (PLP).
  - Source: https://pve.proxmox.com/pve-docs/pve-admin-guide.html  Quote: "Using consumer SSDs is discouraged."
  - Kind: rule of thumb
  - Level: foundation
  - Also: T05
- a:N5. El instalador usa LVM (con un thin pool llamado local-lvm) si elegís ext4 o xfs; si elegís ZFS crea local-zfs. ZFS en el instalador ofrece RAID por software para equipos sin RAID por hardware.
  - Source: https://pve.proxmox.com/pve-docs/pve-admin-guide.html  Quote: "The installer uses LVM if you select ext4 or xfs"
  - Kind: definition
  - Level: foundation
  - Also: T05
- a:N6. Para upgrades mayores y cambios de red se recomienda acceso independiente del host (IPMI, iKVM o físico), porque con kernels nuevos los nombres de las placas de red pueden cambiar y el host queda sin red. PVE 9 trae pve-network-interface-pinning para fijar nombres nicX.
  - Source: https://pve.proxmox.com/wiki/Upgrade_from_8_to_9  Quote: "some NICs may change their name"
  - Kind: mistake
  - Level: core
  - Also: T04

## T03 Repositorios y actualizaciones
- a:N7. Hay tres repositorios de Proxmox además de los de Debian: enterprise (recomendado para producción, requiere suscripción, viene habilitado por defecto), no-subscription (gratis, para pruebas y no producción, paquetes menos validados) y test. Sin suscripción, se deshabilita enterprise con "Enabled: no" y se agrega no-subscription.
  - Source: https://pve.proxmox.com/wiki/Package_Repositories  Quote: "It’s not recommended to use this on production servers"
  - Kind: rule of thumb
  - Level: foundation
- a:N8. Desde Debian 13 los repositorios van en formato deb822, archivos .sources en /etc/apt/sources.list.d/; apt se queja del formato viejo de una línea. "apt modernize-sources" migra la mayoría.
  - Source: https://pve.proxmox.com/wiki/Package_Repositories  Quote: "Since Debian 13 Trixie apt will complain about using this format."
  - Kind: technique
  - Level: foundation
- a:N9. Para actualizar se usa "apt update" y "apt full-upgrade" (o el botón de la GUI). "apt upgrade" puede dejar paquetes a medio actualizar porque no puede quitar paquetes para resolver dependencias.
  - Source: https://pve.proxmox.com/pve-docs/pve-admin-guide.html  Quote: "performing an apt upgrade may result in a partially upgraded or broken package state"
  - Kind: mistake
  - Level: foundation
- a:N10. Upgrade mayor 8 a 9: correr "pve8to9 --full" antes, durante y después; backup probado de todo; al menos 5 GB libres en raíz; hacerlo por consola o SSH con tmux, nunca desde la consola web de la GUI porque se corta.
  - Source: https://pve.proxmox.com/wiki/Upgrade_from_8_to_9  Quote: "Do not carry out the upgrade when connected via the virtual console offered by the GUI"
  - Kind: technique
  - Level: core
- a:N11. En PVE 9, systemd-sysctl ya no lee /etc/sysctl.conf: cualquier ajuste ahí deja de aplicarse tras reiniciar; va en /etc/sysctl.d/NN-nombre.conf.
  - Source: https://pve.proxmox.com/wiki/Upgrade_from_8_to_9  Quote: "/etc/sysctl.conf is no longer honored"
  - Kind: mistake
  - Level: advanced
- a:N12. En clúster, la HA se actualiza nodo por nodo, nunca todos a la vez, verificando cada nodo antes de seguir.
  - Source: https://pve.proxmox.com/pve-docs/pve-admin-guide.html  Quote: "you should do one node after the other, never all at once"
  - Kind: rule of thumb
  - Level: core
  - Also: T14
- a:N13. Migrar una VM de un nodo con versión vieja a uno con versión nueva siempre funciona; al revés no está soportado. Por eso en un upgrade de clúster se vacía el nodo, se actualiza y se avanza.
  - Source: https://pve.proxmox.com/wiki/Upgrade_from_8_to_9  Quote: "A migration of a VM or CT from an older version of Proxmox VE to a newer version will always work."
  - Kind: rule of thumb
  - Level: core
  - Also: T14

## T04 Red del host
- a:N14. Proxmox no escribe directo en /etc/network/interfaces: los cambios de la GUI van a interfaces.new y se aplican con "Apply Configuration" (ifupdown2) o con "ifreload -a" si editaste a mano. Esto evita dejar el nodo inaccesible por un error a medio aplicar.
  - Source: https://pve.proxmox.com/pve-docs/pve-admin-guide.html  Quote: "a wrong network configuration may render a node inaccessible"
  - Kind: technique
  - Level: foundation
- a:N15. Bridge VLAN-aware: cada placa virtual lleva su tag de VLAN y el bridge lo maneja de forma transparente. El modo "tradicional" crea una interfaz y un bridge por VLAN (eno1.5, vmbr0v5). El ejemplo oficial usa bridge-vlan-aware yes y bridge-vids 2-4094, con la IP de gestión en vmbr0.5.
  - Source: https://pve.proxmox.com/pve-docs/pve-admin-guide.html  Quote: "each guest’s virtual network card is assigned to a VLAN tag"
  - Kind: template
  - Level: foundation
- a:N16. Bonds: si el switch soporta LACP, usar 802.3ad; si no, active-backup. balance-alb y balance-tlb no sirven con un bridge con invitados. Corosync no necesita bond: maneja varios enlaces por sí mismo.
  - Source: https://pve.proxmox.com/pve-docs/pve-admin-guide.html  Quote: "If your switch supports the LACP (IEEE 802.3ad) protocol, then we recommend using the corresponding bonding mode"
  - Kind: rule of thumb
  - Level: core
  - Also: T13

## T05 Almacenamiento local
- a:N17. LVM-thin asigna bloques recién cuando se escriben: un disco de 32 GB con 3 GB de datos ocupa 3 GB. Soporta snapshots y linked clones. Es el local-lvm por defecto en instalaciones ext4.
  - Source: https://pve.proxmox.com/pve-docs/pve-admin-guide.html  Quote: "only the blocks that the guest system actually use will be written"
  - Kind: definition
  - Level: foundation
- a:N18. ZFS: protección contra corrupción, compresión, snapshots, RAID por software, replicación. Necesita al menos 8 GB para arrancar, ECC recomendado, y acceso directo a los discos (HBA o controladora en modo IT), nunca encima de RAID por hardware con caché.
  - Source: https://pve.proxmox.com/pve-docs/pve-admin-guide.html  Quote: "Do not use ZFS on top of a hardware RAID controller"
  - Kind: rule of thumb
  - Level: core
- a:N19. ARC de ZFS: desde PVE 8.1 el instalador lo limita al 10 % de la RAM con tope de 16 GiB. Regla: 2 GiB base más 1 GiB por TiB de almacenamiento. Se ajusta en /etc/modprobe.d/zfs.conf.
  - Source: https://pve.proxmox.com/pve-docs/pve-admin-guide.html  Quote: "allocate at least 2 GiB Base + 1 GiB/TiB-Storage"
  - Kind: number
  - Level: core
- a:N20. Directorio, NFS y CIFS son almacenamiento a nivel archivo (guardan ISOs, backups, plantillas); LVM-thin y ZFS zvol son de bloque. En almacenamiento de archivos los snapshots usan qcow2, y los snapshots internos de qcow2 en NFS pueden tardar minutos u horas en discos grandes.
  - Source: https://pve.proxmox.com/pve-docs/pve-admin-guide.html  Quote: "The performance is particularly bad with network storages like NFS."
  - Kind: definition
  - Level: core
  - Also: T06, T12

## T06 Almacenamiento compartido
- a:N21. Tabla oficial: NFS, CIFS, iSCSI, Ceph RBD y PBS son compartidos; LVM-thin, ZFS local y directorio no. Para HA hace falta almacenamiento compartido (o replicación ZFS).
  - Source: https://pve.proxmox.com/pve-docs/pve-admin-guide.html  Quote: "Available storage types"
  - Kind: definition
  - Level: core
  - Also: T14
- a:N22. NFS y CIFS se agregan con pvesm (pvesm scan nfs servidor para ver exports; pvesm add nfs o cifs) y quedan disponibles en todo el clúster.
  - Source: https://pve.proxmox.com/pve-docs/pve-admin-guide.html  Quote: "pvesm scan nfs"
  - Kind: technique
  - Level: foundation
- a:N23. Ceph hiperconvergente: al menos tres servidores preferentemente idénticos, red dedicada de 10 Gbps o más para Ceph (o malla completa para 3 a 5 nodos sin switches de 10G). El tráfico de recuperación interfiere con lo sensible a latencia.
  - Source: https://pve.proxmox.com/pve-docs/pve-admin-guide.html  Quote: "you must use at least three (preferably) identical servers"
  - Kind: rule of thumb
  - Level: advanced
- a:N24. No apuntar dos clústeres distintos al mismo pool de almacenamiento: el bloqueo funciona dentro de un clúster, no entre clústeres.
  - Source: https://pve.proxmox.com/pve-docs/pve-admin-guide.html  Quote: "It is not advisable to use the same storage pool on different Proxmox VE clusters."
  - Kind: mistake
  - Level: core

## T07 Máquinas virtuales KVM
- a:N25. Controladora de disco: VirtIO SCSI single con IO Thread por disco es lo recomendado para rendimiento y es el default para Linux desde 7.3. IDE solo para sistemas anteriores a 2003. Windows necesita el ISO de drivers durante la instalación.
  - Source: https://pve.proxmox.com/pve-docs/pve-admin-guide.html  Quote: "It is highly recommended to use the VirtIO SCSI or VirtIO Block controller"
  - Kind: rule of thumb
  - Level: foundation
- a:N26. Drivers virtio-win: Windows no los trae. Proxmox marca 0.1.271 sin problemas conocidos; 0.1.285 dio errores de lectura con Windows Server 2025 y SQL Server; de 0.1.215 a 0.1.262 aparecían eventos 129 "Reset to device" con IO bloqueado. Al 10 de septiembre de 2026 estaban probando 0.1.302 sin recomendarlo aún para producción.
  - Source: https://pve.proxmox.com/wiki/Windows_VirtIO_Drivers  Quote: "Currently, there are no known issues for version virtio-win 0.1.271"
  - Kind: story
  - Level: core
- a:N27. El guest agent sirve para dos cosas: apagado limpio sin depender de ACPI, y congelar el sistema de archivos (fsfreeze, VSS en Windows) durante backups y snapshots. Se activa con "qm set VMID --agent 1" y se instala dentro del invitado; se prueba con "qm agent VMID ping".
  - Source: https://pve.proxmox.com/wiki/Qemu-guest-agent  Quote: "To freeze the guest file system when making a backup/snapshot"
  - Kind: technique
  - Level: foundation
  - Also: T10
- a:N28. Tipo de CPU: "host" da máximo rendimiento si no te importa la migración en vivo o el clúster es homogéneo; con migración, elegir el modelo de la generación más vieja del clúster. Migrar en vivo entre Intel y AMD no está garantizado. El default es x86-64-v2-AES.
  - Source: https://pve.proxmox.com/pve-docs/pve-admin-guide.html  Quote: "Live migrations between Intel and AMD host CPUs have no guarantee to work."
  - Kind: rule of thumb
  - Level: core
  - Also: T14
- a:N29. Si el ballooning está deshabilitado o el BalloonService no corre en Windows, PVE 9 muestra el uso de memoria visto desde el host, que puede pasar el 100 %. No es una falla de la VM.
  - Source: https://pve.proxmox.com/wiki/Upgrade_from_8_to_9  Quote: "the percentage may spike to over 100% in some cases"
  - Kind: mistake
  - Level: core
  - Also: T16

## T08 Plantillas, clones y cloud-init
- a:N30. Cloud-init: la configuración de red y claves SSH se define del lado del hipervisor y se aplica en el primer arranque mediante un CD-ROM que genera Proxmox (qm set ID --ide2 local-lvm:cloudinit). Muchas imágenes cloud necesitan consola serie (--serial0 socket --vga serial0).
  - Source: https://pve.proxmox.com/wiki/Cloud-Init_Support  Quote: "all Cloud-Init VMs need to have an assigned CD-ROM drive"
  - Kind: technique
  - Level: core
- a:N31. Proxmox recomienda claves SSH antes que contraseña en cloud-init, porque la contraseña queda guardada cifrada dentro de los datos de cloud-init. También recomienda preparar tu propia imagen antes que bajar una lista, para saber qué tiene.
  - Source: https://pve.proxmox.com/wiki/Cloud-Init_Support  Quote: "we usually recommended to prepare the images by yourself"
  - Kind: rule of thumb
  - Level: core
- a:N32. Linked clone: copia casi instantánea que referencia la imagen original (copy-on-write); full clone: copia completa e independiente, más lenta. Desde una plantilla se pueden hacer linked clones rápidos.
  - Source: https://pve.proxmox.com/pve-docs/pve-admin-guide.html  Quote: "Creating a linked clone is nearly instantaneous"
  - Kind: definition
  - Level: foundation

## T09 Contenedores LXC
- a:N33. No privilegiados (default al crear): el root del contenedor se mapea a un usuario sin privilegios del host, y el equipo de LXC los considera seguros por diseño. Privilegiados: el equipo de LXC no trata los escapes como fallas dignas de CVE; usarlos solo en entornos de confianza.
  - Source: https://pve.proxmox.com/pve-docs/pve-admin-guide.html  Quote: "privileged containers should only be used in trusted environments"
  - Kind: rule of thumb
  - Level: foundation
- a:N34. Los contenedores comparten el kernel del host; para usuarios no confiables, una VM aísla mejor. Docker directo en el host no se recomienda; contenedores de aplicación OCI son tecnología en preview; para orquestación o migración en vivo, se recomienda Docker dentro de una VM QEMU.
  - Source: https://pve.proxmox.com/pve-docs/pve-admin-guide.html  Quote: "it is still recommended to run them inside a Proxmox QEMU virtual machine"
  - Kind: rule of thumb
  - Level: core
- a:N35. PVE 9 eliminó cgroup v1: contenedores con systemd 230 o anterior (CentOS 7, Ubuntu 16.04) ya no corren.
  - Source: https://pve.proxmox.com/wiki/Upgrade_from_8_to_9  Quote: "Containers running systemd version 230 (released in 2016!) or older will not be supported"
  - Kind: mistake
  - Level: advanced
- a:N36. Los contenedores se migran con "restart migration": se apagan, se mueven y arrancan, con una caída que suele ser de cientos de milisegundos.
  - Source: https://pve.proxmox.com/pve-docs/pve-admin-guide.html  Quote: "only in a downtime of some hundreds of milliseconds"
  - Kind: number
  - Level: core
  - Also: T14

## T10 Backups con vzdump
- a:N37. Los backups de Proxmox VE son siempre completos (configuración y datos). Modos para VM: stop (máxima consistencia, corte breve), suspend (compatibilidad, no recomendado), snapshot (sin corte, pequeño riesgo de inconsistencia, que el guest agent reduce con fsfreeze).
  - Source: https://pve.proxmox.com/pve-docs/pve-admin-guide.html  Quote: "Proxmox VE backups are always full backups"
  - Kind: definition
  - Level: foundation
- a:N38. Live-restore desde PBS: la VM arranca apenas empieza la restauración y los datos se copian en segundo plano, con lectura lenta mientras tanto.
  - Source: https://pve.proxmox.com/pve-docs/pve-admin-guide.html  Quote: "causes the VM to start as soon as the restore begins"
  - Kind: technique
  - Level: core
- a:N39. Fleecing: guarda en una imagen temporal los datos viejos que el backup todavía necesita, para que el backup no frene la escritura de la VM cuando el destino es lento.
  - Source: https://pve.proxmox.com/pve-docs/pve-admin-guide.html  Quote: "can help guest IO performance and even prevent hangs"
  - Kind: technique
  - Level: advanced

## T11 Proxmox Backup Server
- a:N40. Prune solo borra metadatos de los snapshots; el espacio se libera recién con garbage collection, que tiene un período de gracia de 24 horas y 5 minutos. GC semanal es un buen punto de partida.
  - Source: https://pbs.proxmox.com/docs/maintenance.html  Quote: "For most setups a weekly schedule provides a good interval to start."
  - Kind: rule of thumb
  - Level: core
- a:N41. Ejemplo oficial de retención: keep-last 3, keep-daily 13, keep-weekly 8, keep-monthly 11, keep-yearly 9. Recomiendan retener de más: siempre se puede reducir, pero no se recrean backups del pasado. Hay un simulador de prune.
  - Source: https://pbs.proxmox.com/docs/maintenance.html  Quote: "you cannot recreate backup snapshots from the past"
  - Kind: template
  - Level: core
- a:N42. Verify: revalidar todos los backups al menos una vez por mes aunque ya hayan pasado, por bit rot. Un job frecuente para lo nuevo y otro mensual para todo.
  - Source: https://pbs.proxmox.com/docs/maintenance.html  Quote: "reverify all backups at least monthly"
  - Kind: rule of thumb
  - Level: core
- a:N43. PBS no reescribe bloques existentes, así que un host PVE comprometido no puede modificar backups viejos. Regla 3-2-1: 3 copias, 2 medios, 1 fuera del sitio; sync jobs a un PBS remoto y cinta. Probar restauraciones a una VM nueva, nunca encima de la existente; si son muchas, muestras al azar periódicas.
  - Source: https://pbs.proxmox.com/docs/storage.html  Quote: "restore to a new guest and not to overwrite your current guest"
  - Kind: rule of thumb
  - Level: core
  - Also: T10
- a:N44. Si un ransomware empieza a cifrar backups, los verify jobs fallan porque los checksums ya no coinciden: sirven también como alarma.
  - Source: https://pbs.proxmox.com/docs/storage.html  Quote: "they will start to fail if a ransomware starts to encrypt existing backups"
  - Kind: test
  - Level: advanced

## T12 Snapshots
- a:N45. PVE 9 agregó snapshots como cadena de volúmenes en LVM grueso, útil para SAN iSCSI o FC compartidas (tech preview en 9.0). Antes, LVM compartido no tenía snapshots.
  - Source: https://lists.proxmox.com/pipermail/pve-user/2025-August/017639.html  Quote: "Snapshots as volume chains provide vendor-agnostic support for snapshots"
  - Kind: definition
  - Level: advanced
- a:N46. Snapshots, backups y migraciones ponen un lock en la VM; después de un corte de luz puede quedar trabado y se saca con "qm unlock VMID".
  - Source: https://pve.proxmox.com/pve-docs/pve-admin-guide.html  Quote: "Sometimes you need to remove such a lock manually"
  - Kind: technique
  - Level: core
  - Also: T16

## T13 Clúster
- a:N47. Quórum: cada nodo tiene un voto; ante una partición se necesita mayoría; sin quórum el clúster pasa a solo lectura. Para HA, al menos tres nodos; en clústeres de 2 nodos, un QDevice aporta el tercer voto.
  - Source: https://pve.proxmox.com/pve-docs/pve-admin-guide.html  Quote: "The cluster switches to read-only mode if it loses quorum."
  - Kind: definition
  - Level: foundation
- a:N48. Red de clúster: latencia menor a 5 ms, idealmente red física propia para corosync, nunca compartida con almacenamiento. Un NIC dedicado de 1 Gbit alcanza; agregar un segundo enlace (link1) en otra red física. Puertos UDP 5405 a 5412, hora sincronizada, SSH entre nodos.
  - Source: https://pve.proxmox.com/pve-docs/pve-admin-guide.html  Quote: "latencies under 5 milliseconds (LAN performance)"
  - Kind: number
  - Level: core
- a:N49. QDevice: corosync-qnetd en un host externo y corosync-qdevice en los nodos; "pvecm qdevice setup IP". Se conecta por TCP y no tiene la exigencia de latencia de corosync, puede estar fuera de la LAN. Recomendado para clústeres pares; desaconsejado para impares.
  - Source: https://pve.proxmox.com/pve-docs/pve-admin-guide.html  Quote: "isn’t limited to the low latencies requirements of corosync"
  - Kind: technique
  - Level: core
- a:N50. Un nodo que se une a un clúster no puede tener invitados (choque de IDs) y hereda la configuración de almacenamiento del clúster. "pvecm expected 1" fuerza quórum para emergencias, sabiendo lo que se hace.
  - Source: https://pve.proxmox.com/pve-docs/pve-admin-guide.html  Quote: "a joining node cannot hold any guests"
  - Kind: mistake
  - Level: core
  - Also: T16

## T14 Migración y alta disponibilidad
- a:N51. HA requiere al menos tres nodos, almacenamiento compartido, redundancia de hardware. El fencing por watchdog reinicia el nodo que perdió quórum para que una VM nunca corra dos veces escribiendo el mismo disco; con el watchdog de 60 segundos.
  - Source: https://pve.proxmox.com/pve-docs/pve-admin-guide.html  Quote: "This is really dangerous!"
  - Kind: rule of thumb
  - Level: core
- a:N52. PVE 9 reemplazó los grupos de HA por reglas de afinidad (nodo y recurso), migrando automáticamente cuando todos los nodos están en 9.
  - Source: https://pve.proxmox.com/wiki/Upgrade_from_8_to_9  Quote: "Proxmox VE 9 deprecates HA groups in favor of HA rules."
  - Kind: definition
  - Level: advanced
- a:N53. Disarm de HA (9.2): "ha-manager crm-command disarm-ha freeze" libera los watchdogs en todo el clúster para hacer mantenimiento de red o corosync sin que los nodos se reinicien solos; "arm-ha" para volver. Mientras está desarmado no hay protección.
  - Source: https://pve.proxmox.com/pve-docs/pve-admin-guide.html  Quote: "Keep the disarm window as short as possible."
  - Kind: technique
  - Level: advanced
- a:N54. Replicación de almacenamiento (pvesr) con ZFS local: copia incremental por snapshots cada 1 minuto a 1 semana; reduce migración y da redundancia sin almacenamiento compartido.
  - Source: https://pve.proxmox.com/pve-docs/pve-admin-guide.html  Quote: "The minimum replication interval is one minute"
  - Kind: technique
  - Level: advanced
  - Also: T05

## T15 Usuarios, permisos y 2FA
- a:N55. Realms: PAM (usuarios del sistema), PVE (contraseñas propias de Proxmox, lo más cómodo para instalaciones chicas), LDAP y AD. Roles predefinidos como PVEAuditor (solo lectura) y PVEVMUser (consola, encendido, backup). Grupos con "pveum group add" y "pveum acl modify".
  - Source: https://pve.proxmox.com/pve-docs/pve-admin-guide.html  Quote: "PVEAuditor : has read only access"
  - Kind: template
  - Level: core
- a:N56. API tokens con privsep 1: el token tiene sus propios permisos separados del usuario, por ejemplo solo PVEAuditor sobre /vms para monitoreo.
  - Source: https://pve.proxmox.com/pve-docs/pve-admin-guide.html  Quote: "pveum user token add joe@pve monitoring -privsep 1"
  - Kind: technique
  - Level: advanced
- a:N57. 2FA: TOTP, WebAuthn y claves de recuperación de un solo uso. Configurar más de un segundo factor para no quedar afuera si se pierde el celular. Un admin puede desbloquear con "pveum user tfa unlock".
  - Source: https://pve.proxmox.com/pve-docs/pve-admin-guide.html  Quote: "in order to avoid a situation in which losing your smartphone or security key locks you out"
  - Kind: rule of thumb
  - Level: core

## T16 Firewall y troubleshooting
- a:N58. El firewall viene deshabilitado; al habilitarlo a nivel datacenter, se bloquea el tráfico a los hosts salvo excepciones desde la red local (8006, 22, VNC, corosync). Antes de habilitarlo, dejar abierta una sesión SSH; o crear un IPSet llamado "management" con las IPs de administración.
  - Source: https://pve.proxmox.com/pve-docs/pve-admin-guide.html  Quote: "Please open a SSH connection to one of your Proxmox VE hosts before enabling the firewall."
  - Kind: rule of thumb
  - Level: core
- a:N59. Tres zonas: host (datacenter o nodo), VM/CT, y VNet. Las reglas forward y de VNet solo funcionan con el nuevo proxmox-firewall basado en nftables.
  - Source: https://pve.proxmox.com/pve-docs/pve-admin-guide.html  Quote: "only possible when using the new nftables-based proxmox-firewall"
  - Kind: definition
  - Level: advanced
- a:N60. "pve-firewall status" compila las reglas y muestra errores; "pve-firewall stop" corta el servicio desde consola.
  - Source: https://pve.proxmox.com/pve-docs/pve-admin-guide.html  Quote: "pve-firewall status"
  - Kind: technique
  - Level: core
- a:N61. Diagnóstico de clúster: "pvecm status" para ver quórum y "journalctl -b -u corosync" para el log de corosync.
  - Source: https://pve.proxmox.com/pve-docs/pve-admin-guide.html  Quote: "journalctl -b -u corosync"
  - Kind: technique
  - Level: core
  - Also: T13

## Disagreements seen
- Memoria para ZFS: la guía oficial en requisitos dice "aproximadamente 1 GB por TB" y en la sección ARC "2 GiB base + 1 GiB/TiB" (https://pve.proxmox.com/pve-docs/pve-admin-guide.html); un miembro destacado del foro dice que la regla de 1 GB por TB es falsa (https://forum.proxmox.com/threads/filesystem-choice-for-consumer-ssd.181212/).
- Repositorio no-subscription en producción: la wiki no lo recomienda para producción (https://pve.proxmox.com/wiki/Package_Repositories); muchas guías de practicantes lo usan sin más (https://techdirectarchive.com/2026/06/13/how-to-update-proxmox-ve-from-to-the-latest-version-9-2-3-today/).
- Usuario para conectar PBS: la wiki de Thomas Krenn usa root@pam (https://www.thomas-krenn.com/en/wiki/Proxmox_Backup_Server_configuration); la guía de Hake Hardware usa un usuario dedicado con token y rol DatastoreBackup que no puede borrar (https://hakedev.substack.com/p/complete-proxmox-backup-server-setup).

## Best stories
- virtio-win 0.1.285 rompió lecturas en Windows Server 2025 con SQL; la wiki oficial aconseja quedarse en 0.1.271: https://pve.proxmox.com/wiki/Windows_VirtIO_Drivers
- systemd-sysctl en PVE 9 dejó de leer /etc/sysctl.conf; los ajustes desaparecen tras reiniciar: https://pve.proxmox.com/wiki/Upgrade_from_8_to_9
- El fencing existe porque una VM que sigue escribiendo en el storage compartido mientras otro nodo la arranca destruye el disco: https://pve.proxmox.com/pve-docs/pve-admin-guide.html
- Verify jobs que empiezan a fallar como alarma de ransomware: https://pbs.proxmox.com/docs/storage.html
