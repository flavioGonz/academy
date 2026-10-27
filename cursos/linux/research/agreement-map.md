# Mapa de acuerdos: Linux para técnicos de infraestructura

Notas: research/notes/a.md (16 páginas oficiales) y research/notes/b.md (14 páginas de practicantes, Arch Wiki, Docker docs y un hilo de Q&A). M = páginas distintas con notas en el subtema (incluye Also:). Versión compacta: 30 temas.

## TH01 Leé el árbol desde "/" y movete con pwd, ls -la, cd y less antes de tocar nada
- Sub-topic: T01
- Agree: 2 of 2. Notes: a:N1, a:N2, a:N3. Urls: https://www.debian.org/doc/manuals/debian-reference/ch01.en.html
- Disagree: none found
- Level: foundation
- Best story: none. Thin evidence (M bajo 3).

## TH02 Encadená comandos con tuberías y redirección (|, &&, >, >>, 2>&1) y buscá con find y grep
- Sub-topic: T01 (also T02)
- Agree: 2 of 2. Notes: a:N4, a:N5, b:N1. Urls: https://www.debian.org/doc/manuals/debian-reference/ch01.en.html, https://linuxblog.io/linux-file-permissions-explained-chmod-chown-and-umask-in-practice/
- Disagree: none found
- Level: foundation
- Best story: find que encuentra SUID y archivos escribibles por todos en una auditoría: https://linuxblog.io/linux-file-permissions-explained-chmod-chown-and-umask-in-practice/. Thin evidence.

## TH03 Leé permisos como u/g/o por r=4 w=2 x=1; 755 directorios, 644 archivos, 600 secretos
- Sub-topic: T02
- Agree: 3 of 5. Notes: a:N6, a:N7, b:N3, a:N2. Urls: https://debian-handbook.info/browse/stable/sect.rights-management.html, https://linuxblog.io/linux-file-permissions-explained-chmod-chown-and-umask-in-practice/, https://www.debian.org/doc/manuals/debian-reference/ch01.en.html
- Disagree: none found
- Level: foundation
- Best story: 777 como "arreglo rápido" de tutoriales: https://linuxblog.io/linux-file-permissions-explained-chmod-chown-and-umask-in-practice/

## TH04 Nunca 777; arreglá dueño y grupo, y separá directorios de archivos con find o con X
- Sub-topic: T02
- Agree: 2 of 5. Notes: a:N8, b:N2, b:N3, b:N5. Urls: https://debian-handbook.info/browse/stable/sect.rights-management.html, https://linuxblog.io/linux-file-permissions-explained-chmod-chown-and-umask-in-practice/
- Disagree: none found
- Level: core
- Best story: chmod -R 755 vuelve ejecutables los archivos de una web: https://linuxblog.io/linux-file-permissions-explained-chmod-chown-and-umask-in-practice/

## TH05 Archivos con secretos (netplan, interfaces con WPA, llaves) solo legibles por root o el dueño
- Sub-topic: T02 (also T08, T09)
- Agree: 3 of 5. Notes: a:N32, b:N20, b:N4. Urls: https://www.debian.org/doc/manuals/debian-handbook/sect.network-config.en.html, https://linuxconfig.org/netplan-configuration-guide-on-ubuntu-26-04, https://linuxblog.io/linux-file-permissions-explained-chmod-chown-and-umask-in-practice/
- Disagree: none found
- Level: core
- Best story: none

## TH06 Trabajá con un usuario con sudo y dá acceso por grupos (usermod -aG), no con root ni NOPASSWD
- Sub-topic: T03
- Agree: 3 of 4. Notes: a:N12, a:N13, b:N6. Urls: https://www.debian.org/doc/manuals/debian-reference/ch01.en.html, https://debian-handbook.info/browse/stable/sect.rights-management.html, https://linuxblog.io/linux-file-permissions-explained-chmod-chown-and-umask-in-practice/
- Disagree: none found
- Level: foundation
- Best story: none

## TH07 En Ubuntu 26.04 sudo es sudo-rs: -E se ignora, usá --preserve-env y validá sudoers con visudo -c
- Sub-topic: T03 (also T15)
- Agree: 1 of 4. Notes: b:N7, b:N8. Urls: https://computingforgeeks.com/ubuntu-2604-lts-features/
- Disagree: none found (las otras fuentes son anteriores al cambio)
- Level: advanced
- Best story: script que dependía de sudo -E y ahora corre sin las variables: https://computingforgeeks.com/ubuntu-2604-lts-features/

## TH08 apt update, después apt upgrade; full-upgrade solo cuando lo planificás; apt-get en scripts
- Sub-topic: T04
- Agree: 2 of 3. Notes: a:N14, a:N15, b:N11. Urls: https://debian-handbook.info/browse/stable/sect.apt-get.html, https://linuxize.com/post/debian-versions/
- Disagree: none found
- Level: foundation
- Best story: none

## TH09 Repos de terceros con llave en /etc/apt/keyrings y Signed-By; apt-key ya no existe
- Sub-topic: T04
- Agree: 1 of 3. Notes: b:N9. Urls: https://computingforgeeks.com/ubuntu-2604-lts-features/
- Disagree: none found
- Level: core
- Best story: "apt-key: command not found" en la primera línea de instrucciones viejas: https://computingforgeeks.com/ubuntu-2604-lts-features/

## TH10 Cuando algo cambió solo, mirá /var/log/apt/history.log y dpkg.log
- Sub-topic: T04 (also T07)
- Agree: 1 of 3. Notes: a:N16, b:N10. Urls: https://debian-handbook.info/browse/stable/sect.apt-get.html, https://computingforgeeks.com/ubuntu-2604-lts-features/
- Disagree: none found
- Level: core
- Best story: none

## TH11 Copiá el original, editá en un archivo .d propio y validá (sshd -t, netplan generate, findmnt --verify) antes de reiniciar
- Sub-topic: T05 (also T09, T11)
- Agree: 4 of 5. Notes: a:N19, a:N20, a:N21, b:N12, b:N13. Urls: https://documentation.ubuntu.com/server/how-to/security/openssh-server/, https://debian-handbook.info/browse/stable/sect.apt-get.html, https://linuxconfig.org/netplan-configuration-guide-on-ubuntu-26-04, https://wiki.archlinux.org/title/Fstab
- Disagree: none found
- Level: foundation
- Best story: el "yess" de la línea 28 que tumba ssh.service: https://debian-handbook.info/browse/stable/unix-services.html

## TH12 vim de supervivencia: i, Esc, :w, :q!; nano para lo rápido
- Sub-topic: T05
- Agree: 1 of 5. Notes: a:N22. Urls: https://www.debian.org/doc/manuals/debian-reference/ch01.en.html
- Disagree: none found
- Level: foundation
- Best story: none

## TH13 systemctl status primero, journalctl -u después; start no es enable
- Sub-topic: T06 (also T07)
- Agree: 2 of 2. Notes: a:N23, a:N24, a:N25, b:N14. Urls: https://debian-handbook.info/browse/stable/unix-services.html, https://trstringer.com/systemd-timer-vs-cronjob/
- Disagree: none found
- Level: foundation
- Best story: "unsupported option yess": https://debian-handbook.info/browse/stable/unix-services.html. Thin evidence en T06, reforzado por T07.

## TH14 Filtrá el journal: -u, -f, -b -1, -p err, -S "1 hour ago"; vigilá su tamaño
- Sub-topic: T07
- Agree: 5 of 6. Notes: a:N26, a:N27, a:N35, b:N15, b:N16, b:N17. Urls: https://debian-handbook.info/browse/stable/unix-services.html, https://www.debian.org/doc/manuals/debian-reference/ch09.en.html, https://documentation.ubuntu.com/server/how-to/security/openssh-server/, https://phoenixnap.com/kb/journalctl-systemd-logs, https://trstringer.com/systemd-timer-vs-cronjob/
- Disagree: none found
- Level: foundation
- Best story: journalctl -b -1 para ver por qué se reinició el equipo: https://phoenixnap.com/kb/journalctl-systemd-logs

## TH15 Usá iproute2 (ip addr, ip route, ip neigh, ss) y olvidate de ifconfig
- Sub-topic: T08
- Agree: 4 of 5. Notes: a:N28, a:N31, b:N21, b:N36. Urls: https://www.debian.org/doc/manuals/debian-reference/ch05.en.html, https://www.debian.org/doc/manuals/debian-handbook/sect.network-config.en.html, https://linuxconfig.org/netplan-configuration-guide-on-ubuntu-26-04, https://www.ssdnodes.com/learn/docker-ports-bypass-ufw
- Disagree: none found
- Level: foundation
- Best story: none

## TH16 Diagnosticá en escalera: interfaz, gateway, IP pública, nombre (DNS), puerto
- Sub-topic: T08 (also T10)
- Agree: 3 of 5. Notes: b:N21, a:N29, b:N35. Urls: https://linuxconfig.org/netplan-configuration-guide-on-ubuntu-26-04, https://www.debian.org/doc/manuals/debian-reference/ch05.en.html, https://www.ssdnodes.com/learn/docker-ports-bypass-ufw
- Disagree: none found
- Level: foundation
- Best story: refused contra timeout para distinguir servicio caído de firewall: https://www.ssdnodes.com/learn/docker-ports-bypass-ufw

## TH17 IP fija según distro: netplan YAML en Ubuntu, /etc/network/interfaces en Debian
- Sub-topic: T08
- Agree: 3 of 5. Notes: a:N30, b:N18, b:N12. Urls: https://www.debian.org/doc/manuals/debian-handbook/sect.network-config.en.html, https://linuxconfig.org/netplan-configuration-guide-on-ubuntu-26-04, https://www.debian.org/doc/manuals/debian-reference/ch05.en.html
- Disagree: la Debian Reference lista netplan como opción posible también en Debian (minoritaria): https://www.debian.org/doc/manuals/debian-reference/ch05.en.html
- Level: foundation
- Best story: none

## TH18 Cambios de red remotos con netplan try (vuelve solo a los 120 s), nunca apply a ciegas
- Sub-topic: T08
- Agree: 1 of 5. Notes: b:N19. Urls: https://linuxconfig.org/netplan-configuration-guide-on-ubuntu-26-04
- Disagree: none found
- Level: core
- Best story: none

## TH19 Entrá con llave ed25519 (ssh-keygen, ssh-copy-id) y protegé ~/.ssh
- Sub-topic: T09
- Agree: 4 of 7. Notes: a:N33, b:N23, b:N24, b:N25, b:N4. Urls: https://documentation.ubuntu.com/server/how-to/security/openssh-server/, https://wiki.archlinux.org/title/SSH_keys, https://linuxblog.io/linux-file-permissions-explained-chmod-chown-and-umask-in-practice/, https://computingforgeeks.com/ubuntu-2604-lts-features/
- Disagree: none found
- Level: foundation
- Best story: none

## TH20 Deshabilitá contraseña y root en un snippet de sshd_config.d, con una segunda sesión abierta
- Sub-topic: T09 (also T05)
- Agree: 3 of 7. Notes: a:N20, a:N34, a:N36, b:N26. Urls: https://documentation.ubuntu.com/server/how-to/security/openssh-server/, https://manpages.debian.org/testing/openssh-server/sshd_config.5.en.html, https://wiki.archlinux.org/title/SSH_keys
- Disagree: el valor por defecto upstream es prohibit-password, no "no": https://manpages.debian.org/testing/openssh-server/sshd_config.5.en.html
- Level: foundation
- Best story: advertencia oficial de quedar afuera al reiniciar sshd: https://documentation.ubuntu.com/server/how-to/security/openssh-server/

## TH21 fail2ban es opcional si ya usás solo llaves; OpenSSH trae PerSourcePenalties
- Sub-topic: T09
- Agree: 3 of 7. Notes: b:N27, a:N37, b:N29. Urls: https://www.akamai.com/community/questions/10861/how-important-is-fail2ban, https://manpages.debian.org/testing/openssh-server/sshd_config.5.en.html, https://computingforgeeks.com/ubuntu-2604-lts-features/
- Disagree: https://www.akamai.com/community/questions/10861/how-important-is-fail2ban: fail2ban sirve para cualquier log, no solo SSH (b:N28). La Debian Reference lo lista como analizador de logs: https://www.debian.org/doc/manuals/debian-reference/ch09.en.html
- Level: advanced
- Best story: "un script como root parseando con regex logs del atacante": https://www.akamai.com/community/questions/10861/how-important-is-fail2ban

## TH22 Firewall de host en deny por defecto, permitiendo SSH primero (ufw en Ubuntu, nftables en Debian)
- Sub-topic: T10
- Agree: 4 of 7. Notes: a:N40, a:N42, b:N34, b:N54. Urls: https://documentation.ubuntu.com/server/how-to/security/firewalls/, https://debian-handbook.info/browse/stable/sect.firewall-packet-filtering.html, https://www.ssdnodes.com/learn/docker-ports-bypass-ufw, https://findstack.com/resources/ufw-not-blocking-docker-ports
- Disagree: Debian enseña nft directo; Ubuntu enseña ufw: ver Divisiones.
- Level: foundation
- Best story: none

## TH23 Mejor que filtrar: que el servicio no escuche donde no debe
- Sub-topic: T10 (also T16)
- Agree: 4 of 7. Notes: a:N43, a:N64, b:N34, b:N54. Urls: https://debian-handbook.info/browse/stable/sect.firewall-packet-filtering.html, https://documentation.ubuntu.com/server/how-to/containers/docker-for-system-admins/, https://www.ssdnodes.com/learn/docker-ports-bypass-ufw, https://findstack.com/resources/ufw-not-blocking-docker-ports
- Disagree: none found
- Level: core
- Best story: none

## TH24 Docker se saltea ufw en los puertos publicados; verificá desde afuera
- Sub-topic: T10 (also T16)
- Agree: 4 of 7. Notes: b:N30, b:N32, b:N33, b:N34. Urls: https://docs.docker.com/engine/network/packet-filtering-firewalls/, https://findstack.com/resources/ufw-not-blocking-docker-ports, https://www.ssdnodes.com/learn/docker-ports-bypass-ufw, https://debian-handbook.info/browse/stable/sect.firewall-packet-filtering.html
- Disagree: none found (el hilo del foro de Docker, descartado por corto, matizaba que en un homelab importa menos)
- Level: core
- Best story: n8n abierto a internet con ufw en deny: https://findstack.com/resources/ufw-not-blocking-docker-ports

## TH25 En fstab: UUID siempre; nofail y timeout para discos que pueden faltar; findmnt --verify antes de reiniciar
- Sub-topic: T11
- Agree: 2 of 4. Notes: b:N37, b:N38, b:N13, a:N45. Urls: https://wiki.archlinux.org/title/Fstab, https://www.debian.org/doc/manuals/debian-reference/ch09.en.html
- Disagree: la propia Arch Wiki marca como discutida la sección de nofail en externos.
- Level: core
- Best story: un disco externo ausente que demora 90 segundos el arranque: https://wiki.archlinux.org/title/Fstab

## TH26 df para el sistema de archivos, du para encontrar el culpable; ojo con caché de apt, journal y /tmp en tmpfs
- Sub-topic: T11
- Agree: 3 of 4. Notes: a:N45, a:N18, b:N40. Urls: https://www.debian.org/doc/manuals/debian-reference/ch09.en.html, https://debian-handbook.info/browse/stable/sect.apt-get.html, https://computingforgeeks.com/ubuntu-2604-lts-features/
- Disagree: none found
- Level: foundation
- Best story: none

## TH27 Mirá "available", no "free"; SIGTERM antes que SIGKILL
- Sub-topic: T12
- Agree: 2 of 3. Notes: a:N47, a:N48, b:N41, b:N42. Urls: https://www.debian.org/doc/manuals/debian-reference/ch09.en.html, https://linuxblog.io/free-vs-available
- Disagree: herramientas de monitoreo que alertan por "free": https://linuxblog.io/free-vs-available
- Level: foundation
- Best story: Server B con 153 días y 30 GB libres desperdiciados: https://linuxblog.io/free-vs-available

## TH28 Programá con cron para lo simple y timers cuando necesitás logs, Persistent o dependencias
- Sub-topic: T13
- Agree: 4 of 5. Notes: a:N50, a:N52, b:N43, b:N44, b:N45, b:N46. Urls: https://debian-handbook.info/browse/stable/sect.task-scheduling-cron-atd.html, https://www.debian.org/doc/manuals/debian-reference/ch09.en.html, https://wiki.archlinux.org/title/Systemd/Timers, https://trstringer.com/systemd-timer-vs-cronjob/
- Disagree: trstringer prefiere timers siempre; Arch Wiki marca costos (dos archivos, sin MAILTO); Debian Handbook enseña cron primero.
- Level: core
- Best story: none

## TH29 Un backup no existe hasta que restauraste un archivo; guardalo en otro lugar físico; bases con dump
- Sub-topic: T14
- Agree: 2 of 3. Notes: a:N53, a:N54, a:N55, a:N56. Urls: https://documentation.ubuntu.com/server/how-to/backups/back-up-using-shell-scripts/, https://debian-handbook.info/browse/stable/sect.backup.html
- Disagree: none found
- Level: foundation
- Best story: Falcot Corp y el servidor de backup en otra sala: https://debian-handbook.info/browse/stable/sect.backup.html

## TH30 Dejá activas las actualizaciones de seguridad automáticas; decidí el reinicio vos
- Sub-topic: T15
- Agree: 2 of 3. Notes: a:N57, a:N59, a:N61, b:N50. Urls: https://documentation.ubuntu.com/server/how-to/software/automatic-updates/, https://computingforgeeks.com/ubuntu-2604-lts-features/
- Disagree: la doc de Ubuntu reconoce casos para desactivarlas (sistemas que se recrean, pasos manuales, riesgo alto) y prefiere bloquear paquetes puntuales.
- Level: foundation
- Best story: reinicio agendado a las 20:45 al encontrar /var/run/reboot-required: https://documentation.ubuntu.com/server/how-to/software/automatic-updates/

## TH31 Conocé el soporte de tu versión y actualizá de versión mayor con backup y sin reinicio pendiente
- Sub-topic: T15
- Agree: 2 of 3. Notes: b:N48, b:N49, b:N50, b:N51. Urls: https://linuxize.com/post/debian-versions/, https://computingforgeeks.com/ubuntu-2604-lts-features/
- Disagree: none found
- Level: core
- Best story: upgrade fallido por reinicio pendiente y el sshd de emergencia en el 1022: https://computingforgeeks.com/ubuntu-2604-lts-features/

## TH32 Docker: publicá en 127.0.0.1, volúmenes para datos, iptables de Docker sin tocar
- Sub-topic: T16
- Agree: 4 of 6. Notes: a:N63, a:N64, b:N31, b:N34, b:N54. Urls: https://documentation.ubuntu.com/server/how-to/containers/docker-for-system-admins/, https://docs.docker.com/engine/network/packet-filtering-firewalls/, https://www.ssdnodes.com/learn/docker-ports-bypass-ufw, https://findstack.com/resources/ufw-not-blocking-docker-ports
- Disagree: none found
- Level: core
- Best story: n8n expuesto: https://findstack.com/resources/ufw-not-blocking-docker-ports

## The big splits
- fail2ban con SSH solo por llaves: guías de setup lo incluyen siempre; el hilo de Akamai lo ve como ruido y superficie de ataque (https://www.akamai.com/community/questions/10861/how-important-is-fail2ban). Gira en torno a si hay contraseñas habilitadas y a si hay otros servicios con login expuestos.
- ufw contra nftables directo: Ubuntu (https://documentation.ubuntu.com/server/how-to/security/firewalls/) contra Debian (https://debian-handbook.info/browse/stable/sect.firewall-packet-filtering.html). Gira en la distro y en si el equipo es un host simple o un gateway con NAT.
- cron contra timers: https://trstringer.com/systemd-timer-vs-cronjob/ contra https://wiki.archlinux.org/title/Systemd/Timers y https://debian-handbook.info/browse/stable/sect.task-scheduling-cron-atd.html. Gira en si importan logs, recuperación tras apagado y dependencias.
- PermitRootLogin "no" contra el valor por defecto prohibit-password (https://manpages.debian.org/testing/openssh-server/sshd_config.5.en.html). Gira en si hay procesos automatizados que entran como root con llave (backups).
- Reinicio automático tras actualizar: Ubuntu lo deja en false por defecto y lo describe como disruptivo (https://documentation.ubuntu.com/server/how-to/software/automatic-updates/).

## Coverage gaps
- T01 y T06 con evidencia fina (2 páginas cada uno): la navegación básica y systemctl se sostienen en la Debian Reference y el Debian Handbook. No se pudo agregar más (presupuesto de búsqueda agotado).
- htop, curl y dig con ejemplos de practicantes: solo aparecen en tablas de referencia.
- Contenedores LXC (Proxmox) como caso particular: ninguna fuente leída lo cubre; se trata desde lo general (systemd, red, apt funcionan igual dentro de un LXC).
- rsync con ejemplos concretos de flags (-a, --delete, --dry-run): el Debian Handbook explica el mecanismo de hard links pero no las opciones; los ejemplos del curso se apoyan en la página de manual.
