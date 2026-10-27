# Notes: batch b
Pages read: 14. With notes: 14. Skipped: 0. Practitioner blogs, Arch Wiki, Docker docs, a Q&A thread. Several pages belong to hosting or software-review companies (bias noted per note).

## T01 Terminal y navegación
- b:N1. Auditoría con find: "find / -perm /4000 -type f 2>/dev/null" lista binarios SUID; "find /var/www -perm -o+w -type f" encuentra escribibles por todos; "find / -nouser" encuentra huérfanos tras borrar un usuario.
  - Source: https://linuxblog.io/linux-file-permissions-explained-chmod-chown-and-umask-in-practice/  Quote: "Find world-writable files (potential security issue)"
  - Kind: technique
  - Level: core
  - Also: T02
  - Bias: blog alojado por una empresa de hosting (StackLinux)

## T02 Permisos y propiedad
- b:N2. "chmod -R 755" sobre una web vuelve ejecutables todos los archivos; lo correcto es separar con find -type d (755) y find -type f (644).
  - Source: https://linuxblog.io/linux-file-permissions-explained-chmod-chown-and-umask-in-practice/  Quote: "That find approach is a habit worth building"
  - Kind: mistake
  - Level: core
  - Bias: hosting
- b:N3. 777 "aparece en tutoriales como arreglo rápido"; casi nunca es apropiado en un servidor: lo que falta es ajustar dueño y grupo.
  - Source: https://linuxblog.io/linux-file-permissions-explained-chmod-chown-and-umask-in-practice/  Quote: "It works but it is lazy and often insecure"
  - Kind: rule of thumb
  - Level: foundation
- b:N4. Permisos SSH: ~/.ssh 700, clave privada 600, authorized_keys 600; si están mal, la autenticación falla.
  - Source: https://linuxblog.io/linux-file-permissions-explained-chmod-chown-and-umask-in-practice/  Quote: "SSH is strict about key file permissions"
  - Kind: rule of thumb
  - Level: foundation
  - Also: T09
- b:N5. Config que una app lee sin correr como root: 640 con grupo de la app (root:www-data) en vez de 600.
  - Source: https://linuxblog.io/linux-file-permissions-explained-chmod-chown-and-umask-in-practice/  Quote: "This pattern (640 with a specific group) is cleaner than 600"
  - Kind: technique
  - Level: core
- b:N6. Carpeta compartida: groupadd, chown root:grupo, chmod 2770, usermod -aG grupo usuario. Ojo: -aG agrega, sin -a reemplaza los grupos.
  - Source: https://linuxblog.io/linux-file-permissions-explained-chmod-chown-and-umask-in-practice/  Quote: "usermod -aG devteam alice"
  - Kind: template
  - Level: core
  - Also: T03

## T03 Usuarios, grupos y sudo
- b:N7. Ubuntu 26.04 reemplazó sudo por sudo-rs (Rust); el original queda como sudo.ws. "sudo -E" ahora se ignora con un aviso; se usa --preserve-env=VAR. Opciones como requiretty hacen fallar visudo -c.
  - Source: https://computingforgeeks.com/ubuntu-2604-lts-features/  Quote: "preserving the entire environment is not supported, '-E' is ignored"
  - Kind: mistake
  - Level: core
  - Also: T15
- b:N8. Volver al sudo clásico: update-alternatives --set sudo /usr/bin/sudo.ws.
  - Source: https://computingforgeeks.com/ubuntu-2604-lts-features/  Quote: "The alternative switches immediately"
  - Kind: technique
  - Level: advanced

## T04 Paquetes con apt
- b:N9. En Ubuntu 26.04 apt-key ya no existe: las llaves van en /etc/apt/keyrings/ y se referencian con Signed-By en un archivo .sources (formato deb822). Instrucciones viejas fallan en la primera línea.
  - Source: https://computingforgeeks.com/ubuntu-2604-lts-features/  Quote: "apt-key: command not found"
  - Kind: mistake
  - Level: core
- b:N10. APT 3.2 trae historial deshacible: apt history-list, history-info, history-undo, history-rollback.
  - Source: https://computingforgeeks.com/ubuntu-2604-lts-features/  Quote: "Each transaction gets an ID"
  - Kind: technique
  - Level: advanced
  - Also: T15
- b:N11. Debian: usar el codename (trixie) en sources y no "stable", así el sistema no salta de versión cuando sale la próxima.
  - Source: https://linuxize.com/post/debian-versions/  Quote: "Using a codename keeps your sources on the same release"
  - Kind: rule of thumb
  - Level: core
  - Also: T15

## T05 Editar configuración
- b:N12. Netplan es YAML: 2 espacios, nunca tabulaciones, espacio después de los dos puntos, true/false en minúscula. Un "adresses" mal escrito da "unknown key".
  - Source: https://linuxconfig.org/netplan-configuration-guide-on-ubuntu-26-04  Quote: "Tabs will cause parsing errors"
  - Kind: mistake
  - Level: foundation
  - Also: T08
- b:N13. findmnt --verify --verbose valida fstab antes de reiniciar.
  - Source: https://wiki.archlinux.org/title/Fstab  Quote: "Use findmnt --verify --verbose to check for syntax errors"
  - Kind: test
  - Level: core
  - Also: T11

## T06 Servicios con systemd
- b:N14. Un timer de systemd son dos archivos: .service dice qué, .timer dice cuándo; se habilita el .timer.
  - Source: https://trstringer.com/systemd-timer-vs-cronjob/  Quote: "describes what to do, and the my_job.timer unit describes when"
  - Kind: template
  - Level: core
  - Also: T13
  - Bias: none

## T07 Logs
- b:N15. journalctl útil en obra: -b (este arranque), -b -1 (el anterior, para ver por qué se reinició), -p err (solo errores), -S "1 hour ago", -k (kernel), --disk-usage y --vacuum-size para controlar el espacio.
  - Source: https://phoenixnap.com/kb/journalctl-systemd-logs  Quote: "show the previous boot logs with: journalctl -b -1"
  - Kind: template
  - Level: foundation
  - Bias: blog de proveedor de infraestructura (phoenixNAP)
- b:N16. Prioridades: 0 emerg a 7 debug; "-p err" muestra err y todo lo más grave.
  - Source: https://phoenixnap.com/kb/journalctl-systemd-logs  Quote: "Specifying a single-level priority also shows all lower priority number"
  - Kind: definition
  - Level: core
- b:N17. El journal de un timer es nativo: journalctl -u del servicio, en lugar de bucear en syslog por la salida de cron.
  - Source: https://trstringer.com/systemd-timer-vs-cronjob/  Quote: "This beats the experience of grep'ing through syslog"
  - Kind: rule of thumb
  - Level: core
  - Also: T13

## T08 Red
- b:N18. Netplan en Ubuntu: YAML en /etc/netplan/, Ubuntu Server usa systemd-networkd como renderer. Ejemplo estático: addresses con /24, routes "to: default via:", nameservers.
  - Source: https://linuxconfig.org/netplan-configuration-guide-on-ubuntu-26-04  Quote: "This guide focuses on Ubuntu Server, which uses systemd-networkd"
  - Kind: template
  - Level: foundation
- b:N19. "sudo netplan try" aplica con reversión automática a los 120 segundos si no confirmás: la red de seguridad para cambios remotos. "netplan apply" no tiene vuelta.
  - Source: https://linuxconfig.org/netplan-configuration-guide-on-ubuntu-26-04  Quote: "it automatically reverts to the previous working configuration"
  - Kind: technique
  - Level: foundation
- b:N20. Archivos de netplan con chmod 600, si no, aviso "Permissions ... are too open".
  - Source: https://linuxconfig.org/netplan-configuration-guide-on-ubuntu-26-04  Quote: "Netplan configuration should NOT be accessible by others"
  - Kind: rule of thumb
  - Level: core
  - Also: T02
- b:N21. Escalera de diagnóstico: ip addr, ip route, ping al gateway, ping a una IP pública, ping a un nombre. Si la IP pública responde y el nombre no, es DNS.
  - Source: https://linuxconfig.org/netplan-configuration-guide-on-ubuntu-26-04  Quote: "If internet works but DNS fails, verify your nameserver settings"
  - Kind: test
  - Level: foundation
- b:N22. En 26.04 la hora se sincroniza con chrony y NTS; necesita TCP 4460 saliente o no sincroniza.
  - Source: https://computingforgeeks.com/ubuntu-2604-lts-features/  Quote: "Networks that block TCP 4460 (NTS-KE) will see chrony fail to sync"
  - Kind: mistake
  - Level: advanced
  - Also: T15

## T09 SSH
- b:N23. La llave no viaja: la passphrase solo descifra la privada en tu máquina. Con llaves no hay fuerza bruta posible y un servidor comprometido no expone tu credencial.
  - Source: https://wiki.archlinux.org/title/SSH_keys  Quote: "it is not prone to brute-force attacks"
  - Kind: definition
  - Level: foundation
- b:N24. ssh-keygen ya genera ed25519 por defecto; DSA fue eliminado en OpenSSH 10.0; RSA solo para compatibilidad con equipos viejos.
  - Source: https://wiki.archlinux.org/title/SSH_keys  Quote: "OpenSSH 10.0 and libssh 0.11.0 removed support for DSA keys entirely"
  - Kind: rule of thumb
  - Level: foundation
- b:N25. ssh-keygen -C "usuario@equipo-fecha" pone un comentario que después identifica la llave en authorized_keys.
  - Source: https://wiki.archlinux.org/title/SSH_keys  Quote: "will add a comment saying which user created the key"
  - Kind: technique
  - Level: core
- b:N26. Si ya está deshabilitada la contraseña y no tenés tu llave cargada, el camino es consola fuera de banda (IPMI, consola de la VM, cloud-init).
  - Source: https://wiki.archlinux.org/title/SSH_keys  Quote: "use an Intelligent Platform Management Interface (IPMI)"
  - Kind: technique
  - Level: core
- b:N27. Discrepancia: con solo llaves, fail2ban apenas reduce ruido en logs; un participante prefiere no correr un script como root que parsea con regex logs con datos del atacante.
  - Source: https://www.akamai.com/community/questions/10861/how-important-is-fail2ban  Quote: "fail2ban's sole purpose is cutting down on the spam"
  - Kind: rule of thumb
  - Level: advanced
- b:N28. Contrapunto en el mismo hilo: fail2ban sirve para cualquier log, no solo SSH.
  - Source: https://www.akamai.com/community/questions/10861/how-important-is-fail2ban  Quote: "Fail2ban does more than just SSH"
  - Kind: rule of thumb
  - Level: advanced
- b:N29. OpenSSH 10.2 en Ubuntu 26.04: intercambio de claves post cuántico por defecto, sshd.service es alias de ssh.service, PerSourcePenalties activo (los sondeos de monitoreo a puerto 22 pueden ganarse penalidad).
  - Source: https://computingforgeeks.com/ubuntu-2604-lts-features/  Quote: "monitoring probes that open bare TCP connections to port 22 can earn penalties"
  - Kind: mistake
  - Level: advanced

## T10 Firewall
- b:N30. Docker publica puertos con DNAT en la tabla nat antes de que el paquete llegue a INPUT, donde viven las reglas de ufw: "ufw status" dice cerrado y el puerto responde a internet.
  - Source: https://docs.docker.com/engine/network/packet-filtering-firewalls/  Quote: "effectively ignoring your firewall configuration"
  - Kind: mistake
  - Level: core
  - Also: T16
- b:N31. Docker documenta que poner "iptables": false rompe la red de contenedores y deja sus puertos accesibles desde la LAN.
  - Source: https://docs.docker.com/engine/network/packet-filtering-firewalls/  Quote: "this option is not appropriate for most users"
  - Kind: mistake
  - Level: advanced
- b:N32. Historia: ufw default deny, se publica n8n en 5678 y el panel queda abierto a internet. El artículo cita a Intruder (mayo 2026): de más de 5.200 servidores Ollama expuestos, 31% respondió sin credenciales (su cifra).
  - Source: https://findstack.com/resources/ufw-not-blocking-docker-ports  Quote: "And the n8n admin panel is reachable from anywhere on the internet"
  - Kind: story
  - Level: core
  - Also: T16
  - Bias: sitio de reseñas de software con publicidad
- b:N33. Verificar desde afuera: nmap -Pn -p o nc -zv desde otra red. Cualquier chequeo en el propio servidor mira el camino equivocado.
  - Source: https://findstack.com/resources/ufw-not-blocking-docker-ports  Quote: "any check that runs on the box is checking the wrong thing"
  - Kind: test
  - Level: core
- b:N34. Arreglo preferido: publicar en 127.0.0.1 (desde Docker Engine 28 bloquea además a vecinos de la misma capa 2); si un puerto tiene que ser público, filtrar en la cadena DOCKER-USER y persistir en /etc/ufw/after.rules.
  - Source: https://www.ssdnodes.com/learn/docker-ports-bypass-ufw  Quote: "on Docker Engine 28.0.0 and later Docker also adds a rule"
  - Kind: technique
  - Level: core
  - Also: T16
  - Bias: proveedor de VPS
- b:N35. Diferencia entre "connection refused" (nada escucha) y timeout (un DROP filtra): sirve para diagnosticar si es firewall o servicio caído.
  - Source: https://www.ssdnodes.com/learn/docker-ports-bypass-ufw  Quote: "the fastest way to tell a filtered port from a service that simply is not listening"
  - Kind: test
  - Level: core
  - Also: T08
- b:N36. "ss -tlnp | grep 8080": tiene que decir 127.0.0.1:8080 y no 0.0.0.0:8080.
  - Source: https://www.ssdnodes.com/learn/docker-ports-bypass-ufw  Quote: "You want 127.0.0.1:8080 in the output"
  - Kind: test
  - Level: core
  - Also: T08

## T11 Discos y espacio
- b:N37. fstab: identificar por UUID (lsblk -f), nunca /dev/sdX, porque los nombres de kernel pueden cambiar en cada arranque.
  - Source: https://wiki.archlinux.org/title/Fstab  Quote: "Kernel name descriptors for block devices are not persistent"
  - Kind: rule of thumb
  - Level: foundation
- b:N38. Un disco listado en fstab que no está da error de arranque salvo con nofail; combinado con x-systemd.device-timeout=5 evita esperar 90 segundos.
  - Source: https://wiki.archlinux.org/title/Fstab  Quote: "a disconnected external device with only nofail will make your boot take 90 seconds longer"
  - Kind: mistake
  - Level: core
- b:N39. Montajes de red (NFS, CIFS): opción _netdev para que systemd espere la red.
  - Source: https://wiki.archlinux.org/title/Fstab  Quote: "the _netdev option ensures systemd understands that the mount is network dependent"
  - Kind: technique
  - Level: core
- b:N40. En Ubuntu 26.04 /tmp es tmpfs con tope en la mitad de la RAM (2 GB en un server de 4 GB); dumps grandes conviene llevarlos a /var/tmp.
  - Source: https://computingforgeeks.com/ubuntu-2604-lts-features/  Quote: "Anything that stages large files in /tmp"
  - Kind: mistake
  - Level: core
  - Also: T14

## T12 Procesos y recursos
- b:N41. Free es memoria sin uso ("memoria desperdiciada" para el autor); available estima cuánto se puede usar sin swap, incluyendo caché liberable. Ejemplo: Server B con 153 días de uptime y 30 GB libres.
  - Source: https://linuxblog.io/free-vs-available  Quote: "I like to consider free memory as wasted memory"
  - Kind: story
  - Level: foundation
  - Bias: hosting
- b:N42. Muchas herramientas de monitoreo alertan mirando "free" y no "available"; un servidor sano puede figurar "en presión de memoria".
  - Source: https://linuxblog.io/free-vs-available  Quote: "will be flagged as being under memory pressure"
  - Kind: mistake
  - Level: core

## T13 Tareas programadas
- b:N43. Timers: Persistent=true ejecuta lo perdido si el equipo estaba apagado; RandomizedDelaySec evita que todo arranque junto; systemctl list-timers muestra próximas y últimas ejecuciones.
  - Source: https://wiki.archlinux.org/title/Systemd/Timers  Quote: "it triggers the service immediately if it missed the last start time"
  - Kind: technique
  - Level: core
- b:N44. "systemd-analyze calendar" valida la expresión OnCalendar y dice cuándo será la próxima ejecución.
  - Source: https://wiki.archlinux.org/title/Systemd/Timers  Quote: "calculate the next time the condition would elapse"
  - Kind: test
  - Level: core
- b:N45. Contras de los timers: dos archivos y comandos systemctl contra una línea de crontab, y no hay MAILTO nativo.
  - Source: https://wiki.archlinux.org/title/Systemd/Timers  Quote: "there is no built-in equivalent to cron's MAILTO"
  - Kind: rule of thumb
  - Level: core
- b:N46. Opinión: la sintaxis de crontab es fácil de olvidar y de errar; OnCalendar es más legible.
  - Source: https://trstringer.com/systemd-timer-vs-cronjob/  Quote: "they are very unapproachable, easy to forget, and definitely easy to make mistakes"
  - Kind: rule of thumb
  - Level: core

## T14 Backups
- b:N47. Si un job de backup calcula hashes grandes en Ubuntu 26.04, sha256sum de uutils resultó unas 2,5 veces más lento en su prueba; gnusha256sum usa la versión GNU.
  - Source: https://computingforgeeks.com/ubuntu-2604-lts-features/  Quote: "call gnusha256sum explicitly"
  - Kind: number
  - Level: advanced

## T15 Actualizaciones y ciclo de vida
- b:N48. Debian 13 trixie salió el 9 de agosto de 2025; 13.7 el 12 de septiembre de 2026; soporte regular hasta 9 de agosto de 2028 y LTS hasta 30 de junio de 2030. Debian 11 ya no tiene soporte gratuito.
  - Source: https://linuxize.com/post/debian-versions/  Quote: "the current stable version is Debian 13 "Trixie""
  - Kind: number
  - Level: foundation
- b:N49. Ubuntu 26.04 LTS salió el 23 de abril de 2026, 26.04.1 el 27 de agosto; soporte estándar hasta abril de 2031. La actualización desde 24.04 se ofrece desde 26.04.1.
  - Source: https://computingforgeeks.com/ubuntu-2604-lts-features/  Quote: "Standard support runs five years, to April 2031"
  - Kind: number
  - Level: foundation
- b:N50. Historia: el primer do-release-upgrade falló porque había un reinicio pendiente; tras reiniciar, 10 minutos en una VM de 4 vCPU. El actualizador levanta un sshd extra en el puerto 1022 que no abre en el firewall.
  - Source: https://computingforgeeks.com/ubuntu-2604-lts-features/  Quote: "You have not rebooted after updating a package which requires a reboot"
  - Kind: story
  - Level: core
- b:N51. Una máquina actualizada de 24.04 a 26.04 no queda igual que una instalación nueva: conserva timesyncd e initramfs-tools.
  - Source: https://computingforgeeks.com/ubuntu-2604-lts-features/  Quote: "it was not the same as a fresh install"
  - Kind: mistake
  - Level: advanced
- b:N52. Trampa amd64v3: habilitarlo en una VM Proxmox con CPU kvm64 (sin AVX2) dejó libc6 a medio instalar; se volvió con un snapshot.
  - Source: https://computingforgeeks.com/ubuntu-2604-lts-features/  Quote: "the upgrade died on libc6"
  - Kind: story
  - Level: advanced
  - Also: T04

## T16 Docker
- b:N53. docker.io en 24.04 y 26.04 es la misma 29.1.3: Docker no es motivo para migrar de versión.
  - Source: https://computingforgeeks.com/ubuntu-2604-lts-features/  Quote: "Docker 29 is no longer a reason to upgrade"
  - Kind: number
  - Level: core
- b:N54. Patrón que aguanta: todo puerto interno en 127.0.0.1, un único proxy inverso en 80/443, ufw en deny por defecto para el host, iptables de Docker sin tocar.
  - Source: https://www.ssdnodes.com/learn/docker-ports-bypass-ufw  Quote: "Leave Docker's iptables integration on"
  - Kind: template
  - Level: core

## Disagreements seen
- fail2ban: la mayoría de guías de configuración inicial lo recomiendan; un participante del hilo de Akamai lo considera ruido innecesario con llaves solamente: https://www.akamai.com/community/questions/10861/how-important-is-fail2ban
- cron vs timers: trstringer prefiere timers (https://trstringer.com/systemd-timer-vs-cronjob/); la Arch Wiki lista costos reales (dos archivos, sin MAILTO) (https://wiki.archlinux.org/title/Systemd/Timers); el Debian Handbook sigue enseñando cron como principal (https://debian-handbook.info/browse/stable/sect.task-scheduling-cron-atd.html).
- ufw-docker: findstack lo acepta como tercera opción con reservas; ssdnodes no lo menciona y propone after.rules.
- Medir memoria: herramientas de monitoreo que miran "free" contra quienes miran "available": https://linuxblog.io/free-vs-available

## Best stories
- n8n publicado con -p 5678 detrás de ufw en deny, abierto a internet: https://findstack.com/resources/ufw-not-blocking-docker-ports
- El upgrade a 26.04 que falló por reinicio pendiente y el sshd de emergencia en el 1022: https://computingforgeeks.com/ubuntu-2604-lts-features/
- Server B con 153 días encendido y 30 GB "free" desperdiciados: https://linuxblog.io/free-vs-available
- amd64v3 en una VM sin AVX2 deja libc6 rota: https://computingforgeeks.com/ubuntu-2604-lts-features/
