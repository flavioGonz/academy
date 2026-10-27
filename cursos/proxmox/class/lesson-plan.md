# Plan del curso: Proxmox VE: virtualización y contenedores en producción

Público: técnicos instaladores y de soporte de IES, con base de redes, sin experiencia fuerte en Proxmox. Nivel inicial a intermedio.
Versión de referencia: Proxmox VE 9.2 (mayo de 2026, Debian 13.5, kernel 7.0) y Proxmox Backup Server 4.x. Donde algo cambió de 8 a 9, se dice.
Fuentes: 28 páginas en raw/web. Mapa de acuerdos: research/agreement-map.md (33 temas).
Laboratorio: un Proxmox VE 9 de pruebas (mini PC o VM con virtualización anidada). Para las lecciones de clúster, dos o tres Proxmox anidados en ese mismo host. No hay simulador oficial.

## Arco 1. Un host bien parado (lecciones 1 a 4)
Por qué este arco: casi todos los problemas de soporte en Proxmox nacen en la instalación; repositorios, red, disco y VM bien elegidos el primer día te ahorran meses de parches.

### Lección 1. Repos en orden
- 6 of 7 coinciden en la versión actual (TH01); 3 of 7 en repositorios (TH03, la wiki oficial contra guías que usan no-subscription sin aviso).
- Idea: Proxmox VE 9.2 es la rama actual; la 8 quedó sin soporte en agosto de 2026. Antes del primer update se elige el repositorio (enterprise con suscripción, no-subscription sabiendo que es para no producción) y se actualiza con full-upgrade.
- Por qué importa: el error de "401 Unauthorized" del primer apt update y los paquetes a medio actualizar por usar apt upgrade son los dos tickets más tontos que hay.
- Historia: 8.4 recibió un año de solapamiento, hasta agosto de 2026 (https://lists.proxmox.com/pipermail/pve-user/2025-August/017639.html). Formato deb822 obligatorio en Debian 13 (https://pve.proxmox.com/wiki/Package_Repositories).
- Laboratorio: Rápido · 10 min. Ver pveversion -v, revisar Node, Repositories, dejar un solo repositorio de Proxmox habilitado, apt update y apt full-upgrade.
- Regla: Un host, un repositorio de Proxmox decidido a conciencia, y siempre full-upgrade.

### Lección 2. Puente VLAN-aware
- 3 of 4 coinciden (TH06, TH07); OVS como alternativa en una fuente.
- Idea: el orden es placas, bond, bridge. Un vmbr0 VLAN-aware y el tag en cada placa virtual reemplaza a un bridge por VLAN. Los cambios se aplican con Apply Configuration o ifreload -a.
- Por qué importa: es la causa número uno de "la VM no tiene red" en obra.
- Historia: la confusión sobre qué crear primero (https://getlabsdone.com/steps-to-create-proxmox-bridge-with-multiple-ports-using-lacp-bonding/); ejemplo oficial con bridge-vids 2-4094 y gestión en vmbr0.5 (https://pve.proxmox.com/pve-docs/pve-admin-guide.html).
- Laboratorio: Foco · 15 min. Marcar vmbr0 como VLAN aware, crear VM de prueba con tag 10, verificar con bridge vlan show.
- Regla: Placas, bond, bridge; VLAN-aware en el bridge y el tag en la VM.

### Lección 3. Disco con criterio
- 2 of 2 en lo básico (TH09, evidencia fina); la regla de RAM de ZFS está disputada (TH10).
- Idea: LVM-thin es lo simple y rápido; ZFS da integridad, snapshots, replicación y RAID por software, pero pide RAM, discos directos (HBA) y mejor SSD con PLP. Nunca ZFS sobre RAID por hardware.
- Por qué importa: el almacenamiento elegido en la instalación es lo más caro de cambiar después.
- Historia: el veterano del foro que defiende ZFS pero avisa del desgaste y llama falsa la regla de 1 GB por TB (https://forum.proxmox.com/threads/filesystem-choice-for-consumer-ssd.181212/).
- Laboratorio: Rápido · 10 min. pvesm status, lvs, zpool status si hay ZFS, ver el límite del ARC.
- Regla: ZFS con discos directos y RAM; si no, LVM-thin; nunca ZFS sobre RAID por hardware.

### Lección 4. VM bien armada
- 3 of 4 en VirtIO y agente (TH13); el detalle de virtio-win es solo de la wiki oficial (TH14).
- Idea: VirtIO SCSI single con IO Thread, placa VirtIO, guest agent activado y adentro. En Windows, drivers virtio-win en la versión que Proxmox marca estable. CPU host solo si no vas a migrar.
- Por qué importa: backups consistentes, apagados limpios y rendimiento real dependen de esto.
- Historia: virtio-win 0.1.285 con errores de lectura en Windows Server 2025 con SQL; 0.1.271 sin problemas conocidos (https://pve.proxmox.com/wiki/Windows_VirtIO_Drivers).
- Laboratorio: Foco · 15 min. qm set --agent 1, instalar qemu-guest-agent en una VM Linux, qm agent ping.
- Regla: Toda VM nace con VirtIO y guest agent, y el agente se prueba con un ping.

## Arco 2. La operación de todos los días (lecciones 5 a 8)
Por qué este arco: con el host bien parado, el trabajo diario es crear invitados rápido y poder volver atrás; este arco cubre desplegar y respaldar.

### Lección 5. Plantilla y clon
- 4 of 4 coinciden en plantillas cloud-init (TH16); full contra linked está dividido (TH17).
- Idea: imagen cloud, disco importado, unidad cloud-init, plantilla. Cada clon recibe usuario, clave SSH e IP desde Proxmox.
- Historia: clonar en menos de un minuto contra veinte de ISO (https://computingforgeeks.com/create-proxmox-vm-templates-cloud-images/); borrar la plantilla rompe los linked clones.
- Laboratorio: Foco · 20 min. Crear plantilla 9000 desde Debian 13 genericcloud y clonar una VM con IP fija.
- Regla: Producción en full clone desde plantilla; linked clone solo para laboratorio.

### Lección 6. Contenedor sin privilegios
- 2 of 5 explícitos en no privilegiados (TH18); 3 of 5 en Docker en VM (TH19), con el foro en contra.
- Idea: LXC comparte el kernel del host; no privilegiado es el default y lo seguro. Docker en VM.
- Historia: usuario del foro con i5 y 20 GB que quería un CT por contenedor Docker (https://forum.proxmox.com/threads/proxmox-7-1-and-docker-lxc-vs-vm.105140/); WunderTech: "use a VM" (https://www.wundertech.net/how-to-run-docker-in-proxmox-on-a-vm/).
- Laboratorio: Rápido · 10 min. pveam update, bajar plantilla Debian, crear CT no privilegiado, pct enter.
- Regla: Servicios Linux livianos en LXC no privilegiado; Docker y lo expuesto, en VM.

### Lección 7. Backup que restaura
- 3 of 3 en probar restauraciones (TH21); 2 of 3 en modos (TH20); snapshot no es backup (TH25, evidencia fina).
- Idea: vzdump hace backups completos; snapshot con guest agent para no cortar; un snapshot no es un backup; un backup no probado tampoco.
- Historia: la doc de PBS pide restaurar a una VM nueva, nunca encima de la existente, y muestras al azar si son muchas (https://pbs.proxmox.com/docs/storage.html).
- Laboratorio: Foco · 15 min. vzdump de una VM a local, qmrestore con otro ID, arrancar sin red.
- Regla: Ningún backup cuenta hasta que lo restauré en una VM nueva.

### Lección 8. PBS sin sorpresas
- 5 of 7 en prune, GC y verify (TH22); 3 of 7 en usuario sin permiso de borrado (TH24), con Thomas Krenn usando root@pam.
- Idea: prune elige, GC libera, verify detecta. Usuario con DatastoreBackup, retención generosa, copia fuera del sitio.
- Historia: verify jobs que fallan como alarma de ransomware (https://pbs.proxmox.com/docs/storage.html); el rol que deja escribir pero no borrar (https://hakedev.substack.com/p/complete-proxmox-backup-server-setup).
- Laboratorio: Admin · 20 min. Crear prune job, GC semanal, verify job y usuario con token y rol DatastoreBackup.
- Regla: En PBS programo prune, GC y verify el mismo día que creo el datastore.

## Arco 3. Clúster, seguridad y rescate (lecciones 9 a 12)
Por qué este arco: el clúster y la HA son lo que más vende y lo que más rompe; este arco enseña cuándo armarlos, cómo protegerlos y cómo salir de un problema.

### Lección 9. Tres votos
- 2 of 2 (TH26, evidencia fina, pero es la guía oficial más un caso del foro).
- Idea: quórum es mayoría; sin quórum, solo lectura. Dos nodos solos no hacen HA; hace falta un QDevice. Corosync en red propia, menos de 5 ms.
- Historia: el usuario del foro que prueba failover con dos nodos y la HA no conmuta (https://forum.proxmox.com/threads/2-nodes-proxmox-cluster-qdevice.181580/).
- Laboratorio: Campo · 20 min. Dos PVE anidados, pvecm create, pvecm add, apagar uno y ver pvecm status; agregar QDevice.
- Regla: Nunca entrego un clúster de dos nodos sin QDevice.

### Lección 10. HA con fencing
- 2 of 2 (TH29, TH30, evidencia fina).
- Idea: HA reinicia en otro nodo lo que cayó, pero exige tres votos, almacenamiento compartido y fencing por watchdog. En 9.2 hay disarm para mantenimiento.
- Historia: la guía explica el fencing con la VM que escribe desde dos nodos y destruye el disco (https://pve.proxmox.com/pve-docs/pve-admin-guide.html).
- Laboratorio: Campo · 15 min. Migración en vivo, ha-manager add, ha-manager status, disarm y arm.
- Regla: Antes de tocar red o corosync en un clúster con HA, desarmo la HA.

### Lección 11. Acceso blindado
- 1 of 1 en usuarios y 2FA (TH31, solo oficial); 2 of 4 en firewall (TH32).
- Idea: usuarios personales con el rol justo, 2FA con claves de recuperación, y firewall habilitado con SSH abierto e IPSet management.
- Historia: Diego Carrasco quedó afuera de su servidor y volvió editando config.db desde rescate (https://diegocarrasco.com/regain-access-proxmox-firewall-misconfiguration/).
- Laboratorio: Admin · 15 min. pveum user add, rol PVEAuditor, TOTP, IPSet management, firewall a nivel datacenter.
- Regla: Nunca habilito el firewall sin una sesión SSH abierta y el IPSet management cargado.

### Lección 12. Upgrade y rescate
- 5 of 7 en el procedimiento de upgrade mayor (TH05); 3 of 4 en el orden de diagnóstico (TH33).
- Idea: upgrade mayor con backup probado, pve8to9 --full, consola fuera de la GUI, un nodo por vez. Diagnóstico: quórum, logs, locks, almacenamiento.
- Historia: /etc/sysctl.conf que deja de aplicarse en PVE 9 (https://pve.proxmox.com/wiki/Upgrade_from_8_to_9); los siete escenarios de romper y arreglar (https://www.flane.de/course/innovator-pveicm).
- Laboratorio: Admin · 15 min. Checklist de diagnóstico: pvecm status, journalctl, qm unlock, pvesm status, pve-firewall status.
- Regla: Upgrade mayor: backup probado, checklist limpio, consola fuera de la GUI, un nodo por vez.

## Divisiones (decisiones, no lecciones)
- Repositorio no-subscription en producción. Lados: la wiki oficial dice que no es para producción (https://pve.proxmox.com/wiki/Package_Repositories); muchas guías lo usan como rutina (https://techdirectarchive.com/2026/06/13/how-to-update-proxmox-ve-from-to-the-latest-version-9-2-3-today/). Cómo decidir: si el cliente necesita soporte del fabricante o el servicio es crítico, suscripción y enterprise; si no, no-subscription con backups probados y updates tras unos días.
- Docker en LXC o en VM. Lados: oficial y WunderTech, VM; foro y hhf, LXC funciona y ahorra. Cómo decidir: cliente en producción o expuesto a Internet, VM; laboratorio o servicio interno chico, LXC aceptable sabiendo que puede romperse en un upgrade.
- ZFS en SSD de consumo y RAM. Lados: guía oficial desaconseja SSD de consumo y pide RAM; foro dice que la RAM pedida es exagerada y que el desgaste es tolerable. Cómo decidir: con SSD de consumo y poca RAM, LVM-thin; con SSD de datacenter y HBA, ZFS.
- Linked o full clone. Lados: wiki oficial destaca linked; practicantes prefieren full para producción. Cómo decidir: si la VM va a vivir más que la plantilla, full.
- Usuario de PBS. Lados: root@pam (Thomas Krenn) contra usuario dedicado sin borrado (Hake Hardware, doc de PBS). Cómo decidir: si un atacante con el host PVE pudiera borrar los backups, cambiá a usuario dedicado.
- Garbage collection diario o semanal. Lados: doc PBS semanal, Thomas Krenn diario o semanal. Cómo decidir: si el datastore se llena rápido, diario; si no, semanal.

## Huecos
- Usuarios, 2FA, NFS/CIFS y HA se apoyan casi solo en la guía oficial; no se leyeron casos de practicantes.
- No se cubre: importación desde VMware (el importador ESXi), passthrough de PCI y USB, SDN, Ceph en profundidad, monitoreo con InfluxDB, Proxmox Datacenter Manager.
- La búsqueda web del lote tuvo límite de consultas; algunos temas quedaron con una sola fuente independiente.

## Entrega
12 carpetas class/NN-handle con script.txt, card.md y quiz.json; class/course.json. El audio lo renderiza el orquestador.
