# Plan: Linux para técnicos de infraestructura

Público: técnicos instaladores y de soporte de IES Training, con base de redes, que administran servidores chicos, contenedores LXC, appliances y gateways. Nivel inicial a intermedio.
Versiones (verificadas en octubre de 2026): Debian 13 "trixie" (13.7, 12 de septiembre de 2026; soporte regular hasta agosto de 2028), Ubuntu Server 24.04 LTS y 26.04 LTS (26.04.1 del 27 de agosto de 2026; soporte estándar hasta abril de 2031). Donde 26.04 cambia algo (sudo-rs, apt-key eliminado, /tmp en tmpfs, OpenSSH 10.2, chrony con NTS) se dice.
Fuentes: 30 páginas en raw/web (16 oficiales de Debian, Ubuntu, man pages y Docker; 14 de practicantes, Arch Wiki y un hilo de Q&A).

## Arco 1. Fundamentos: moverse y no romper (lecciones 1 a 4)
Por qué este arco: antes de administrar nada, un técnico necesita leer el sistema, entender quién puede tocar qué, instalar y actualizar con método y editar un archivo sin dejar el equipo afuera. Termina con un servidor que sabés recorrer, actualizar y configurar sin miedo.

### Lección 1. Moverse sin miedo
- 2 of 2 fuentes que cubren navegación coinciden (evidencia fina, TH01 y TH02).
- Idea: todo cuelga de "/"; con pwd, ls -la, cd, less, find y grep, más tuberías, leés cualquier equipo antes de tocarlo.
- Por qué importa: en un appliance desconocido, el primer error es editar sin saber dónde estás.
- Historia: la Debian Reference propone recorrer el sistema con su tabla de comandos "como entrenamiento" y el truco de "[e]xim4" para que grep no se encuentre a sí mismo (https://www.debian.org/doc/manuals/debian-reference/ch01.en.html).
- Laboratorio · Rápido · 10 min: recorrer /etc, buscar un archivo con find, filtrar con grep y paginar con less.
- Regla: primero leo, después toco.

### Lección 2. Nunca 777
- 3 of 5 fuentes (TH03, TH04, TH06).
- Idea: permisos u/g/o con r=4 w=2 x=1; 755 directorios, 644 archivos, 600 secretos; el acceso compartido se da por grupo (usermod -aG), no con 777 ni con root.
- Por qué importa: el 777 "arregla" y deja el equipo abierto.
- Historia: linuxblog.io describe al 777 como el arreglo rápido de los tutoriales y el chmod -R 755 que vuelve ejecutable toda una web (https://linuxblog.io/linux-file-permissions-explained-chmod-chown-and-umask-in-practice/). En Ubuntu 26.04 sudo es sudo-rs (https://computingforgeeks.com/ubuntu-2604-lts-features/).
- Laboratorio · Foco · 15 min: carpeta compartida con setgid para un grupo de técnicos.
- Regla: si pienso en 777, lo que falta es arreglar dueño y grupo.

### Lección 3. Actualizar con método
- 3 of 4 fuentes de apt y actualizaciones (TH08, TH30, TH31).
- Idea: apt update y apt upgrade con regularidad, full-upgrade planificado; seguridad automática con unattended-upgrades; el reinicio lo decidís vos.
- Por qué importa: un gateway sin parches es el eslabón débil; uno que se reinicia solo a media tarde, también.
- Historia: el log de Ubuntu donde unattended-upgrades encuentra /var/run/reboot-required y agenda el reinicio (https://documentation.ubuntu.com/server/how-to/software/automatic-updates/); el upgrade a 26.04 que falla por un reinicio pendiente (https://computingforgeeks.com/ubuntu-2604-lts-features/).
- Laboratorio · Admin · 15 min: revisar 20auto-upgrades, el log y history.log; fijar hora de reinicio.
- Regla: seguridad automática, reinicio con hora y full-upgrade con backup.

### Lección 4. Copiá y validá
- 4 of 5 fuentes (TH11).
- Idea: antes de editar, copia; tu cambio en un archivo .d propio; validar con sshd -t, netplan generate o findmnt -x antes de reiniciar el servicio.
- Por qué importa: un error de tipeo en sshd_config o en fstab te deja sin acceso o sin arranque.
- Historia: el "yess" de la línea 28 que tumba ssh.service en el Debian Handbook (https://debian-handbook.info/browse/stable/unix-services.html); en Ubuntu el snippet de sshd_config.d gana porque vale el primer valor (https://documentation.ubuntu.com/server/how-to/security/openssh-server/).
- Laboratorio · Foco · 15 min: banner de SSH en un snippet, error a propósito, sshd -t lo atrapa.
- Regla: copia, cambio en .d, validación, y recién ahí restart.

## Arco 2. Operación diaria (lecciones 5 a 8)
Por qué este arco: lo que se hace todas las semanas en soporte: un servicio que no levanta, una red que no responde, un acceso remoto seguro y un firewall que deja pasar solo lo necesario. Termina con un servidor accesible por SSH con llave, detrás de un firewall que entendés.

### Lección 5. Status y journal
- 5 of 6 fuentes de logs y 2 of 2 de systemd (TH13, TH14).
- Idea: systemctl status primero, journalctl -u después; start no es enable; -b -1 muestra el arranque anterior.
- Historia: el "unsupported option yess" (https://debian-handbook.info/browse/stable/unix-services.html); opciones de journalctl de phoenixNAP (https://phoenixnap.com/kb/journalctl-systemd-logs).
- Laboratorio · Rápido · 10 min: romper y arreglar un servicio leyendo su journal.
- Regla: status, journal, arreglo, status otra vez.

### Lección 6. Escalera de red
- 4 of 5 fuentes (TH15, TH16, TH17, TH18).
- Idea: iproute2 en vez de ifconfig; diagnosticar en escalera (interfaz, gateway, IP pública, DNS, puerto); IP fija con netplan en Ubuntu y /etc/network/interfaces en Debian; netplan try para cambios remotos.
- Historia: la escalera de linuxconfig ("si internet anda y el DNS no, revisá los nameservers") (https://linuxconfig.org/netplan-configuration-guide-on-ubuntu-26-04); comandos seguros de la Debian Reference (https://www.debian.org/doc/manuals/debian-reference/ch05.en.html).
- Laboratorio · Campo · 15 min: escalera completa y cambio de IP con netplan try.
- Regla: subo la escalera de abajo hacia arriba y no salteo escalones.

### Lección 7. Llave, no contraseña
- 4 of 7 fuentes (TH19, TH20, TH21).
- Idea: llave ed25519 con ssh-copy-id, después PasswordAuthentication no y PermitRootLogin no en un snippet, con una segunda sesión abierta; fail2ban queda como opcional.
- Historia: el hilo de Akamai donde se discute fail2ban con llaves (https://www.akamai.com/community/questions/10861/how-important-is-fail2ban); PerSourcePenalties por defecto (https://manpages.debian.org/testing/openssh-server/sshd_config.5.en.html).
- Laboratorio · Foco · 20 min.
- Regla: nunca cierro la sesión que funciona hasta probar la nueva.

### Lección 8. Deny por defecto
- 4 of 7 fuentes (TH22, TH23).
- Idea: entrante en deny, permitir SSH primero (desde la red de gestión si se puede), después lo que el equipo sirve; ufw en Ubuntu, nftables en Debian; mejor que un servicio no escuche a filtrarlo.
- Historia: el Debian Handbook prefiere que el servicio no escuche antes que filtrarlo (https://debian-handbook.info/browse/stable/sect.firewall-packet-filtering.html); ufw con origen por subred (https://documentation.ubuntu.com/server/how-to/security/firewalls/).
- Laboratorio · Campo · 15 min.
- Regla: primero permito SSH, después activo el firewall.

## Arco 3. Avanzado y troubleshooting (lecciones 9 a 12)
Por qué este arco: los llamados de soporte que más se repiten: disco lleno, equipo lento, un backup que nadie probó y un contenedor que quedó expuesto. Termina con un método para cada uno.

### Lección 9. Disco lleno
- 3 of 4 fuentes (TH25, TH26).
- Idea: df dice qué sistema de archivos, du dice qué carpeta; sospechosos habituales: caché de apt, journal, logs y /tmp; en fstab, UUID y nofail con timeout.
- Historia: el disco externo ausente que suma 90 segundos al arranque (https://wiki.archlinux.org/title/Fstab); /tmp en tmpfs con tope de la mitad de la RAM en 26.04 (https://computingforgeeks.com/ubuntu-2604-lts-features/).
- Laboratorio · Campo · 15 min.
- Regla: df para saber dónde, du para saber qué, y nunca /dev/sdX en fstab.

### Lección 10. Available, no free
- 2 of 3 fuentes (TH27).
- Idea: la columna que importa en free es available; top u htop para ver quién consume; kill con SIGTERM antes que SIGKILL.
- Historia: Server B con 153 días encendido y 30 GB libres "desperdiciados" (https://linuxblog.io/free-vs-available); señales de la Debian Reference (https://www.debian.org/doc/manuals/debian-reference/ch09.en.html).
- Laboratorio · Rápido · 10 min.
- Regla: miro available y load antes de decir que falta RAM.

### Lección 11. Backup que restaura
- 2 of 3 fuentes de backup y 4 of 5 de programación (TH28, TH29).
- Idea: tar o rsync programado con cron o con un timer; copia en otro lugar físico; un backup existe cuando restauraste un archivo.
- Historia: Falcot Corp guarda el servidor de backup en otra sala por si hay incendio (https://debian-handbook.info/browse/stable/sect.backup.html); restaurar a /tmp con -C (https://documentation.ubuntu.com/server/how-to/backups/back-up-using-shell-scripts/).
- Laboratorio · Admin · 20 min.
- Regla: no hay backup hasta que restauré un archivo de él.

### Lección 12. Docker sin sorpresas
- 4 of 6 fuentes (TH24, TH32).
- Idea: Docker en panorama (imágenes, contenedores, volúmenes, redes); los puertos publicados se saltean ufw; publicar en 127.0.0.1 y verificar desde afuera.
- Historia: n8n publicado con ufw en deny, abierto a internet; Intruder (mayo 2026, citado por findstack) halló 31% de 5.200 Ollama expuestos respondiendo sin credenciales (https://findstack.com/resources/ufw-not-blocking-docker-ports).
- Laboratorio · Foco · 20 min.
- Regla: todo puerto de contenedor va a 127.0.0.1 salvo que haya un motivo, y lo verifico desde otra red.

## Divisiones (decisiones, no lecciones)
- fail2ban con SSH solo por llaves. Lados: las guías de configuración inicial lo instalan siempre; un participante del hilo de Akamai lo ve como ruido de logs y superficie extra (https://www.akamai.com/community/questions/10861/how-important-is-fail2ban). Cómo decidir: si hay contraseñas habilitadas o servicios con login web expuestos, fail2ban suma; si es solo SSH con llave, PerSourcePenalties y un firewall por origen ya cubren lo principal.
- ufw o nftables. Lados: Ubuntu enseña ufw (https://documentation.ubuntu.com/server/how-to/security/firewalls/), Debian enseña nftables directo (https://debian-handbook.info/browse/stable/sect.firewall-packet-filtering.html). Cómo decidir: host simple en Ubuntu, ufw; gateway con NAT o Debian, nftables con /etc/nftables.conf.
- cron o timers de systemd. Lados: trstringer prefiere timers (https://trstringer.com/systemd-timer-vs-cronjob/); la Arch Wiki marca que son dos archivos y no tienen MAILTO (https://wiki.archlinux.org/title/Systemd/Timers). Cómo decidir: una línea simple, cron; si importa el log, la recuperación tras apagado (Persistent) o dependencias, timer.
- PermitRootLogin no o prohibit-password. Lados: guías prácticas usan "no"; el valor por defecto es prohibit-password (https://manpages.debian.org/testing/openssh-server/sshd_config.5.en.html). Cómo decidir: "no" salvo que un proceso automatizado entre como root con llave; en ese caso prohibit-password o forced-commands-only.
- Reinicio automático tras actualizar. Lados: Ubuntu lo trae en false y lo describe como disruptivo (https://documentation.ubuntu.com/server/how-to/software/automatic-updates/). Cómo decidir: en un gateway o NVR que nadie mira, reinicio automático a una hora fija de madrugada; en un servidor con usuarios, reinicio manual en ventana.

## Huecos
- Navegación (T01) y systemd (T06) se apoyan en solo 2 páginas cada uno; el presupuesto de búsqueda se agotó antes de sumar más.
- LXC en Proxmox no aparece en ninguna fuente leída; el curso lo trata desde lo general.
- htop, curl, dig y las opciones de rsync aparecen en tablas de referencia y en man pages, sin ejemplos de practicantes.
- Las tarjetas evitan opciones largas con doble guion (el checker las rechaza); se usan las cortas equivalentes (findmnt -x, rsync -n).

## Entrega
12 lecciones de unos 2 minutos, cada una con guion, tarjeta y 3 preguntas. Audio a cargo del orquestador.
