# Notes: batch a
Pages read: 16. With notes: 16. Skipped: 0 (all official Debian and Ubuntu documentation plus the sshd_config man page).

## T01 Terminal y navegación
- a:N1. Todo cuelga de un único árbol que arranca en "/"; no confundir "/" con "/root", que es el home del superusuario. Los nombres distinguen mayúsculas.
  - Source: https://www.debian.org/doc/manuals/debian-reference/ch01.en.html  Quote: "Don't confuse this with the home directory for the root user"
  - Kind: definition
  - Level: foundation
  - Bias: none
- a:N2. Tabla de comandos básicos para practicar como usuario sin privilegios: pwd, id, ls -la, cd -, cd .., find . -name, grep -e, ps aux, top, tar -xvzf. La propia Debian Reference propone recorrer el sistema con ellos "como entrenamiento".
  - Source: https://www.debian.org/doc/manuals/debian-reference/ch01.en.html  Quote: "traverse directories and peek into the system using the above commands as training"
  - Kind: technique
  - Level: foundation
  - Also: T12
- a:N3. less es el paginador: "/" o "?" para buscar, "h" ayuda, "q" sale. Sirve tanto para archivos como para la salida de otro comando por tubería.
  - Source: https://www.debian.org/doc/manuals/debian-reference/ch01.en.html  Quote: "type " / " or " ? " to search a string"
  - Kind: technique
  - Level: foundation
- a:N4. Idiomas de shell: tubería "|", "&&" ejecuta el segundo solo si el primero salió bien, "||" si falló, ">" sobrescribe, ">>" agrega, "2>&1" junta errores con la salida.
  - Source: https://www.debian.org/doc/manuals/debian-reference/ch01.en.html  Quote: "execute command1 ; if successful, execute command2"
  - Kind: template
  - Level: foundation
- a:N5. "ps aux | grep -e "[e]xim4*"": el truco del corchete evita que grep se encuentre a sí mismo en la lista de procesos.
  - Source: https://www.debian.org/doc/manuals/debian-reference/ch01.en.html  Quote: "enable grep to avoid matching itself"
  - Kind: technique
  - Level: core
  - Also: T12

## T02 Permisos y propiedad
- a:N6. Tres categorías (u, g, o) por tres derechos (r=4, w=2, x=1). 755 para ejecutables y directorios, 644 para datos, 600 solo el dueño.
  - Source: https://debian-handbook.info/browse/stable/sect.rights-management.html  Quote: "The most frequent right combinations are 755 for executable files and directories, and 644 for data files"
  - Kind: rule of thumb
  - Level: foundation
- a:N7. En un directorio, x significa "poder atravesarlo": sin x no entrás con cd aunque tengas r. Con x pero sin r, accedés a lo que conocés por nombre pero no podés listar.
  - Source: https://debian-handbook.info/browse/stable/sect.rights-management.html  Quote: "execute access allows crossing through it"
  - Kind: definition
  - Level: core
- a:N8. Al usar -R, la "X" mayúscula agrega ejecución a directorios y solo a archivos que ya eran ejecutables para alguien; evita volver ejecutables los archivos de datos.
  - Source: https://debian-handbook.info/browse/stable/sect.rights-management.html  Quote: "For directories it adds executable permissions"
  - Kind: technique
  - Level: core
- a:N9. umask 0022 convierte 666/777 en 644/755. Se define en pam_umask y /etc/login.defs, o por sesión en ~/.bashrc.
  - Source: https://debian-handbook.info/browse/stable/sect.rights-management.html  Quote: "the default for directories 777 becomes 755"
  - Kind: definition
  - Level: core
- a:N10. setgid en un directorio hace que lo creado adentro herede el grupo del directorio; el sticky bit (como en /tmp) impide borrar archivos ajenos.
  - Source: https://debian-handbook.info/browse/stable/sect.rights-management.html  Quote: "it restricts deletion of files so that only their owner"
  - Kind: definition
  - Level: core
  - Also: T03
- a:N11. Un "+" al final de los permisos en ls -l indica ACL; se consultan con getfacl y se ponen con setfacl (paquete acl).
  - Source: https://debian-handbook.info/browse/stable/sect.rights-management.html  Quote: "the output of the ls -l command will show a plus-sign"
  - Kind: definition
  - Level: advanced

## T03 Usuarios, grupos y sudo
- a:N12. La regla "usuario ALL=(ALL) NOPASSWD:ALL" en sudoers solo tiene sentido en una estación de un solo usuario; para acceso a dispositivos o archivos concretos conviene usar grupos en vez de root.
  - Source: https://www.debian.org/doc/manuals/debian-reference/ch01.en.html  Quote: "should only be used for the single user workstation"
  - Kind: rule of thumb
  - Level: core
  - Also: T02
- a:N13. setuid es riesgoso: para correr algo con otro usuario, sudo, su o runuser son mejores opciones que poner bits especiales.
  - Source: https://debian-handbook.info/browse/stable/sect.rights-management.html  Quote: "the sudo , su , or runuser commands are usually better choices"
  - Kind: rule of thumb
  - Level: core

## T04 Paquetes con apt
- a:N14. apt es para uso interactivo; apt-get tiene interfaz estable y es el indicado para scripts.
  - Source: https://debian-handbook.info/browse/stable/sect.apt-get.html  Quote: "It is thus the tool that you want to use when you need to script"
  - Kind: rule of thumb
  - Level: foundation
- a:N15. Secuencia: apt update (listas), apt upgrade (sin quitar paquetes), apt full-upgrade (puede quitar e instalar dependencias; el cambio de versión mayor). purge borra también la configuración.
  - Source: https://debian-handbook.info/browse/stable/sect.apt-get.html  Quote: "apt will complete the upgrade even if it has to remove some obsolete packages"
  - Kind: definition
  - Level: foundation
- a:N16. Todo queda registrado en /var/log/apt/history.log, /var/log/apt/term.log y /var/log/dpkg.log: es lo primero a mirar cuando algo cambió "solo".
  - Source: https://debian-handbook.info/browse/stable/sect.apt-get.html  Quote: "The results of these operations are logged into /var/log/apt/history.log"
  - Kind: technique
  - Level: core
  - Also: T07
- a:N17. Un .deb suelto se instala con dependencias usando "apt install ./archivo.deb"; el "./" es lo que le indica que es un archivo y no un nombre de paquete.
  - Source: https://debian-handbook.info/browse/stable/sect.apt-get.html  Quote: "The leading ./ is important"
  - Kind: technique
  - Level: core
- a:N18. /var/cache/apt/archives crece con cada actualización; apt-get clean o autoclean liberan espacio.
  - Source: https://debian-handbook.info/browse/stable/sect.apt-get.html  Quote: "this directory can quickly take a lot of disk space"
  - Kind: technique
  - Level: core
  - Also: T11

## T05 Editar configuración sin romper
- a:N19. Los directorios .d (apt.conf.d, sshd_config.d, sources.list.d) permiten agregar un archivo propio en vez de tocar el original del paquete; se leen en orden alfabético.
  - Source: https://debian-handbook.info/browse/stable/sect.apt-get.html  Quote: "APT includes them in alphabetical order"
  - Kind: technique
  - Level: core
  - Also: T09
- a:N20. En Ubuntu, sshd_config arranca con Include de /etc/ssh/sshd_config.d/*.conf y en OpenSSH vale el primer valor leído: lo que pongas en un snippet gana sobre el archivo principal.
  - Source: https://documentation.ubuntu.com/server/how-to/security/openssh-server/  Quote: "OpenSSH uses the first value set for most directives"
  - Kind: mistake
  - Level: core
  - Also: T09
- a:N21. Antes de reiniciar sshd: "sudo sshd -t" valida la configuración. Copiar el original y protegerlo contra escritura (cp a .original, chmod a-w) da un punto de vuelta.
  - Source: https://documentation.ubuntu.com/server/how-to/security/openssh-server/  Quote: "check the configuration after changing it and before restarting"
  - Kind: technique
  - Level: foundation
  - Also: T09
- a:N22. vim mínimo: i para insertar, Esc para volver, :w guarda, :q sale, :q! sale sin guardar; vimtutor es el tutorial interactivo.
  - Source: https://www.debian.org/doc/manuals/debian-reference/ch01.en.html  Quote: "Please use the " vimtutor " program"
  - Kind: template
  - Level: foundation

## T06 Servicios con systemd
- a:N23. Un .service es declarativo: [Unit] (descripción, orden), [Service] (cómo arranca), [Install] (en qué target se habilita). Los del paquete van en /lib/systemd/system, los del admin en /etc/systemd/system.
  - Source: https://debian-handbook.info/browse/stable/unix-services.html  Quote: "there is very little code in there, only declarations"
  - Kind: definition
  - Level: foundation
- a:N24. start/stop/restart/reload actúan ahora; enable/disable deciden si arranca al bootear. Son cosas distintas.
  - Source: https://debian-handbook.info/browse/stable/unix-services.html  Quote: "To control whether a service is active (i.e. whether it will get started automatically on boot)"
  - Kind: definition
  - Level: foundation
- a:N25. Historia: ssh.service no arranca; systemctl status muestra "failed"; journalctl -u ssh.service revela "sshd_config line 28: unsupported option "yess"". Se corrige el archivo y se vuelve a arrancar. Es el método: status primero, journal después.
  - Source: https://debian-handbook.info/browse/stable/unix-services.html  Quote: "unsupported option "yess""
  - Kind: story
  - Level: foundation
  - Also: T07

## T07 Logs
- a:N26. journalctl -u servicio filtra por unidad; -f sigue en vivo como tail -f.
  - Source: https://debian-handbook.info/browse/stable/unix-services.html  Quote: "-f , which instructs journalctl to keep displaying new messages"
  - Kind: technique
  - Level: foundation
- a:N27. Programas viejos escriben texto en /var/log (rotado por logrotate); los nuevos escriben en el journal binario en /var/log/journal. Un script puede escribir al journal con systemd-cat.
  - Source: https://www.debian.org/doc/manuals/debian-reference/ch09.en.html  Quote: "logrotate(8) is used to simplify the administration of log files"
  - Kind: definition
  - Level: core

## T08 Red
- a:N28. Tabla de traducción net-tools a iproute2: ifconfig pasa a ip addr, route a ip route, arp a ip neigh. Comandos seguros que no cambian nada: ip addr show, ip route show, ip neigh, ss -l -t -n, dig, tracepath, mtr.
  - Source: https://www.debian.org/doc/manuals/debian-reference/ch05.en.html  Quote: "You may use low level network commands as follows safely"
  - Kind: template
  - Level: foundation
- a:N29. La resolución de nombres sigue /etc/nsswitch.conf ("hosts: files dns"): primero /etc/hosts, después el DNS de /etc/resolv.conf.
  - Source: https://www.debian.org/doc/manuals/debian-reference/ch05.en.html  Quote: "hosts: files dns " dictates the hostname resolution order"
  - Kind: definition
  - Level: core
- a:N30. En Debian servidor sin NetworkManager, el instalador usa ifupdown y /etc/network/interfaces; "auto" levanta la interfaz al bootear; static lleva address con /24 y gateway.
  - Source: https://www.debian.org/doc/manuals/debian-handbook/sect.network-config.en.html  Quote: "In a server context, ifupdown is thus the network configuration tool that you usually get"
  - Kind: template
  - Level: foundation
- a:N31. Nombres predecibles (enp0s31f6): en = cableada, p0 bus PCI, s31 slot, f6 función. eth0 ya no es la norma; ip addr o /sys/class/net muestran el nombre real.
  - Source: https://www.debian.org/doc/manuals/debian-handbook/sect.network-config.en.html  Quote: "you will see names starting with en for wired ethernet"
  - Kind: definition
  - Level: foundation
  - Disagree: none
- a:N32. Si /etc/network/interfaces guarda una clave WPA, conviene restringir su lectura a root.
  - Source: https://www.debian.org/doc/manuals/debian-handbook/sect.network-config.en.html  Quote: "consider restricting the read permissions on /etc/network/interfaces"
  - Kind: rule of thumb
  - Level: core
  - Also: T02

## T09 SSH
- a:N33. Ubuntu recomienda ed25519 (clave corta, menos cómputo); RSA 4096 como alternativa. ssh-copy-id copia la pública; authorized_keys no debe ser escribible por otros (chmod go-w).
  - Source: https://documentation.ubuntu.com/server/how-to/security/openssh-server/  Quote: "We recommend the ed25519 Elliptic Curve algorithm"
  - Kind: technique
  - Level: foundation
- a:N34. Advertencia oficial: si SSH es tu único acceso y te equivocás en sshd_config, podés quedar afuera al reiniciar.
  - Source: https://documentation.ubuntu.com/server/how-to/security/openssh-server/  Quote: "you may find you are locked out of the server upon restarting it"
  - Kind: mistake
  - Level: foundation
- a:N35. Para depurar llaves: "sudo journalctl -fu ssh.service" en el servidor mientras probás desde el cliente.
  - Source: https://documentation.ubuntu.com/server/how-to/security/openssh-server/  Quote: "have a look at the target_machine 's live logs"
  - Kind: technique
  - Level: core
  - Also: T07
- a:N36. PermitRootLogin por defecto es prohibit-password (root solo con llave); "no" lo prohíbe del todo. PasswordAuthentication por defecto es yes.
  - Source: https://manpages.debian.org/testing/openssh-server/sshd_config.5.en.html  Quote: "The default is prohibit-password"
  - Kind: definition
  - Level: foundation
- a:N37. PerSourcePenalties viene activado por defecto: penaliza direcciones que fallan autenticación (authfail 5s por defecto) y las rechaza un tiempo. Es un freno nativo a la fuerza bruta.
  - Source: https://manpages.debian.org/testing/openssh-server/sshd_config.5.en.html  Quote: "Penalties are enabled by default"
  - Kind: definition
  - Level: advanced
  - Also: T10
- a:N38. AllowUsers limita quién entra, y acepta usuario@host con rangos CIDR (ej. tecnico@10.10.10.0/24).
  - Source: https://manpages.debian.org/testing/openssh-server/sshd_config.5.en.html  Quote: "HOST criteria may additionally contain addresses to match in CIDR"
  - Kind: technique
  - Level: core
- a:N39. Para sesiones que se cortan: tmux o screen en el servidor mantienen el trabajo vivo y te reenganchás.
  - Source: https://documentation.ubuntu.com/server/how-to/security/openssh-server/  Quote: "you can reconnect and reattach to your existing session"
  - Kind: technique
  - Level: core

## T10 Firewall
- a:N40. ufw viene deshabilitado por defecto en Ubuntu; se habilita con ufw enable, se abre con ufw allow, y "ufw allow proto tcp from 192.168.0.0/24 to any port 22" restringe por origen. --dry-run muestra las reglas sin aplicarlas.
  - Source: https://documentation.ubuntu.com/server/how-to/security/firewalls/  Quote: "ufw by default is initially disabled"
  - Kind: technique
  - Level: foundation
- a:N41. Gateway con NAT: DEFAULT_FORWARD_POLICY="ACCEPT", ip_forward=1 y una regla MASQUERADE en la tabla nat de /etc/ufw/before.rules (con su COMMIT).
  - Source: https://documentation.ubuntu.com/server/how-to/security/firewalls/  Quote: "don't delete the 'COMMIT' line"
  - Kind: template
  - Level: advanced
- a:N42. Debian usa nftables por defecto desde Buster; las reglas viven en /etc/nftables.conf y se cargan al boot con systemctl enable nftables. Lo que se hace con nft en vivo se pierde si no se guarda.
  - Source: https://debian-handbook.info/browse/stable/sect.firewall-packet-filtering.html  Quote: "The executed nft commands do not make permanent changes"
  - Kind: technique
  - Level: core
- a:N43. Antes que filtrar un puerto, mejor que el servicio no escuche en esa interfaz o directamente no esté instalado.
  - Source: https://debian-handbook.info/browse/stable/sect.firewall-packet-filtering.html  Quote: "always better to configure services to not listen on those network interfaces"
  - Kind: rule of thumb
  - Level: core
  - Also: T16
- a:N44. iptables-translate traduce reglas viejas a sintaxis nft; los iptables-nft existen solo por compatibilidad.
  - Source: https://debian-handbook.info/browse/stable/sect.firewall-packet-filtering.html  Quote: "these tools should only be used for backwards compatibility"
  - Kind: technique
  - Level: advanced

## T11 Discos y espacio
- a:N45. df mide el sistema de archivos, du el árbol de directorios; lsblk -f y blkid muestran UUID para usar en fstab con mount -U.
  - Source: https://www.debian.org/doc/manuals/debian-reference/ch09.en.html  Quote: "You can also probe UUID and other information with " lsblk -f ""
  - Kind: technique
  - Level: foundation
- a:N46. SMART: smartctl -a /dev/sda para ver salud del disco, smartd para vigilar.
  - Source: https://www.debian.org/doc/manuals/debian-reference/ch09.en.html  Quote: "Check the output of " smartctl -a /dev/sda ""
  - Kind: test
  - Level: advanced

## T12 Procesos y recursos
- a:N47. Señales: 15 SIGTERM pide terminar (se puede atrapar), 9 SIGKILL no se puede bloquear, 1 SIGHUP. kill por PID, pkill/killall por nombre.
  - Source: https://www.debian.org/doc/manuals/debian-reference/ch09.en.html  Quote: "9 SIGKILL terminate the process unblockable kill signal"
  - Kind: definition
  - Level: foundation
- a:N48. Leer free: no asustarse por "used" alto y "free" bajo; lo que importa es lo que queda descontando buffers y caché.
  - Source: https://www.debian.org/doc/manuals/debian-reference/ch09.en.html  Quote: "Do not worry about the large size of " used ""
  - Kind: rule of thumb
  - Level: foundation
- a:N49. lsof -p PID lista archivos abiertos por un proceso; fuser -v archivo dice qué proceso lo tiene.
  - Source: https://www.debian.org/doc/manuals/debian-reference/ch09.en.html  Quote: "You can list all files opened by a process"
  - Kind: technique
  - Level: core
  - Also: T11

## T13 Tareas programadas
- a:N50. crontab tiene 5 campos (min hora día mes díasemana) más el comando; en /etc/crontab y /etc/cron.d se agrega el usuario. Atajos: @daily, @reboot. Los directorios cron.daily, cron.weekly ejecutan scripts sueltos.
  - Source: https://debian-handbook.info/browse/stable/sect.task-scheduling-cron-atd.html  Quote: "the user name under whose identity the command must be executed"
  - Kind: template
  - Level: foundation
- a:N51. Cambio de hora: en Debian, cron ejecuta una sola vez las tareas de la hora repetida y corre después las de la hora que no existió.
  - Source: https://debian-handbook.info/browse/stable/sect.task-scheduling-cron-atd.html  Quote: "are only executed once"
  - Kind: mistake
  - Level: advanced
- a:N52. Redirigir salida en cron ("> archivo 2>&1") o usar MAILTO; sin eso los errores se pierden.
  - Source: https://www.debian.org/doc/manuals/debian-reference/ch09.en.html  Quote: "mail any output to paul"
  - Kind: technique
  - Level: core
  - Also: T07

## T14 Backups
- a:N53. Script oficial de Ubuntu: tar czf con nombre de host y día de la semana (siete copias rotativas); ejecutable con chmod u+x y programado con sudo crontab -e.
  - Source: https://documentation.ubuntu.com/server/how-to/backups/back-up-using-shell-scripts/  Quote: "giving a backup history of seven days"
  - Kind: template
  - Level: foundation
- a:N54. Listar el contenido (tar -tzvf) no alcanza: la mejor prueba es restaurar un archivo a otro directorio con -C /tmp. Restaurar todo en / sobrescribe.
  - Source: https://documentation.ubuntu.com/server/how-to/backups/back-up-using-shell-scripts/  Quote: "the best test is to restore a file from the archive"
  - Kind: test
  - Level: foundation
- a:N55. Historia Falcot Corp: rsync diario con copias por hard links (cada día parece completo pero solo ocupa lo que cambió) en un servidor separado, en otra sala, por si hay incendio.
  - Source: https://debian-handbook.info/browse/stable/sect.backup.html  Quote: "a great number of backups can be kept in a small amount of space"
  - Kind: story
  - Level: core
- a:N56. Las bases de datos no se respaldan copiando archivos en caliente: se exporta un dump y se guarda eso.
  - Source: https://debian-handbook.info/browse/stable/sect.backup.html  Quote: "cannot be backed up by simply copying their files"
  - Kind: mistake
  - Level: core

## T15 Actualizaciones
- a:N57. Ubuntu instala unattended-upgrades por defecto y aplica solo seguridad una vez por día; 20auto-upgrades lo activa, 50unattended-upgrades define orígenes, lista negra, mail y reinicio. Logs en /var/log/unattended-upgrades.
  - Source: https://documentation.ubuntu.com/server/how-to/software/automatic-updates/  Quote: "By default, unattended-upgrades runs once per day"
  - Kind: definition
  - Level: foundation
- a:N58. Agregar un repositorio no hace que unattended-upgrades lo actualice: hay que sumar su Origin a Allowed-Origins.
  - Source: https://documentation.ubuntu.com/server/how-to/software/automatic-updates/  Quote: "Just adding another package repository to an Ubuntu system WILL NOT make unattended-upgrades consider it"
  - Kind: mistake
  - Level: core
- a:N59. Automatic-Reboot viene en false; si se activa, Automatic-Reboot-Time "03:30" lo lleva a una hora fija. El indicador es /var/run/reboot-required.
  - Source: https://documentation.ubuntu.com/server/how-to/software/automatic-updates/  Quote: "Reboots can be very disruptive, especially if the system fails to come back"
  - Kind: technique
  - Level: core
- a:N60. Desde 24.04, needrestart reinicia servicios afectados automáticamente; para excluir uno crítico, un archivo en /etc/needrestart/conf.d con override_rc en 0.
  - Source: https://documentation.ubuntu.com/server/how-to/software/automatic-updates/  Quote: "needrestart restarts the affected services automatically by default"
  - Kind: technique
  - Level: advanced
- a:N61. Ubuntu considera que el riesgo de no aplicar seguridad es mayor que el de aplicarla; en lugar de apagar todo, bloquear paquetes puntuales con Package-Blacklist.
  - Source: https://documentation.ubuntu.com/server/how-to/software/automatic-updates/  Quote: "Ubuntu believes that risk to be less than the risk of NOT applying a security update"
  - Kind: rule of thumb
  - Level: core
- a:N62. Máquinas que se prenden poco: los timers apt-daily recuperan la ejecución perdida al arrancar y pueden trabar apt; se ajusta con Persistent=false vía systemctl edit.
  - Source: https://documentation.ubuntu.com/server/how-to/software/automatic-updates/  Quote: "unattended-upgrades may often run on system startup"
  - Kind: mistake
  - Level: advanced
  - Also: T13

## T16 Docker
- a:N63. Ubuntu documenta docker.io (paquete de Ubuntu, soportado por Canonical); volúmenes en /var/lib/docker/volumes; bind mounts para carpetas del host.
  - Source: https://documentation.ubuntu.com/server/how-to/containers/docker-for-system-admins/  Quote: "By default, all your volumes will be stored in /var/lib/docker/volumes"
  - Kind: definition
  - Level: foundation
- a:N64. Publicar puertos solo si algo fuera de Docker los necesita; entre contenedores alcanza con la misma red. "--publish 127.0.0.1:8080:80" deja el servicio solo para el host.
  - Source: https://documentation.ubuntu.com/server/how-to/containers/docker-for-system-admins/  Quote: "You should publish ports of a container to the host only if you want to make it available to non-Docker workloads"
  - Kind: rule of thumb
  - Level: core
  - Also: T10
- a:N65. Docker rootless disponible desde Ubuntu 26.04 con docker.io 29.1.3.
  - Source: https://documentation.ubuntu.com/server/how-to/containers/docker-for-system-admins/  Quote: "Starting in Ubuntu 26.04"
  - Kind: definition
  - Level: advanced

## Disagreements seen
- Herramienta de firewall: Ubuntu enseña ufw como frontend por defecto (https://documentation.ubuntu.com/server/how-to/security/firewalls/), Debian enseña nftables directo con /etc/nftables.conf (https://debian-handbook.info/browse/stable/sect.firewall-packet-filtering.html).
- Configuración de red: Debian servidor usa ifupdown y /etc/network/interfaces (https://www.debian.org/doc/manuals/debian-handbook/sect.network-config.en.html); la Debian Reference lista netplan como opción minoritaria (https://www.debian.org/doc/manuals/debian-reference/ch05.en.html).
- PermitRootLogin: el valor por defecto upstream es prohibit-password (https://manpages.debian.org/testing/openssh-server/sshd_config.5.en.html); las guías de practicantes recomiendan "no".

## Best stories
- El "yess" en la línea 28 de sshd_config que tumba ssh.service, encontrado con status y journalctl: https://debian-handbook.info/browse/stable/unix-services.html
- Falcot Corp guarda el servidor de backup en otra sala por si hay incendio: https://debian-handbook.info/browse/stable/sect.backup.html
- unattended-upgrades encuentra /var/run/reboot-required y agenda el reinicio para las 20:45: https://documentation.ubuntu.com/server/how-to/software/automatic-updates/
