# Subtemas: Linux para técnicos de infraestructura

Nivel: inicial a intermedio. Distros: Debian 13 "trixie" (13.7, sept 2026), Ubuntu Server 24.04 LTS y 26.04 LTS (26.04.1, ago 2026).

Cómo se enseña (lo que se vio al buscar): el temario de LFCS de la Linux Foundation (operación, usuarios y grupos, red, almacenamiento, servicios), el Debian Administrator's Handbook (capítulos de servicios Unix, red, apt, seguridad), la Debian Reference (tutoriales GNU/Linux, red, trucos del sistema) y la Ubuntu Server documentation (how-to de seguridad, software, red, backups, contenedores). Los tutoriales de practicantes (configuración inicial de VPS) repiten el mismo orden: actualizar, usuario con sudo, llaves SSH, firewall, actualizaciones automáticas.

- T01 Terminal y navegación: rutas, ls, cd, less, find, grep, tuberías y redirección
- T02 Permisos y propiedad: chmod, chown, umask, bits especiales, ACL
- T03 Usuarios, grupos y sudo (incluye sudo-rs en Ubuntu 26.04)
- T04 Paquetes con apt: update, upgrade, full-upgrade, repositorios y llaves
- T05 Editar configuración sin romper: nano/vim mínimo, directorios .d, validar antes de reiniciar
- T06 Servicios con systemd: systemctl, unidades, targets
- T07 Logs: journalctl, /var/log, logrotate
- T08 Red: ip addr/route/link, ss, ping, dig, curl; netplan (Ubuntu) e ifupdown (Debian)
- T09 SSH bien hecho: llaves, root y contraseña deshabilitados, fail2ban
- T10 Firewall: nftables y ufw, gateway con NAT
- T11 Discos y espacio: df, du, lsblk, mount, fstab
- T12 Procesos y recursos: top/htop, free, kill
- T13 Tareas programadas: cron y timers de systemd
- T14 Backups: tar, rsync, prueba de restauración
- T15 Actualizaciones y ciclo de vida: unattended-upgrades, reinicios, soporte por versión
- T16 Docker como panorama: paquetes, volúmenes, redes, puertos publicados
