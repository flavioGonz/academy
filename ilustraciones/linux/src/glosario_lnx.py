"""Genera ilustraciones/linux/glosario-propuesta.json y lo prueba sobre una copia combinada del glosario.

  python3 glosario_lnx.py     # escribe la propuesta y valida la copia en el scratchpad

terms: entradas nuevas completas. alias_agregar: alias nuevos para entradas existentes.
modificar: campos a reemplazar en entradas existentes. No toca site2/data/glosario.json.
También compara contra las propuestas de otros cursos (ilustraciones/*/glosario-propuesta.json) para no duplicar.
"""
import glob, json, subprocess, sys

L = "Linux"


def T(id, term, aliases, short, long, cat=L, case=True, year=None):
    d = {"id": id, "term": term, "aliases": aliases, "cat": cat, "short": short, "long": long, "case": case}
    if year:
        d["year"] = year
    return d


TERMS = [
    T("systemd", "systemd", ["systemctl", "unidad de systemd", "multi-user.target"],
      "El sistema de arranque y de servicios de Debian y Ubuntu: es el primer proceso, el PID 1.",
      "Lo presentaron Lennart Poettering y Kay Sievers en 2010; Debian lo usa por defecto desde Jessie (2015). Lee unidades declarativas: un .service dice cómo arrancar un programa y un .target es un estado del sistema, como multi-user.target. systemctl start lo levanta ahora y systemctl enable lo engancha al arranque.", year=2010),
    T("journald", "journald", ["journalctl", "systemd-journald", "journal de systemd"],
      "El registro de systemd: guarda lo que dicen los servicios y el arranque, cada línea con su unidad y su prioridad.",
      "Se lee con journalctl: -u filtra por servicio, -p err por gravedad, -b -1 trae el arranque anterior y -f muestra en vivo. Vive en /var/log/journal y crece hasta su tope: SystemMaxUse en un archivo de /etc/systemd/journald.conf.d lo limita."),
    T("systemd-timer", "timer de systemd", ["timers de systemd", "OnCalendar", "systemctl list-timers"],
      "Una tarea programada de systemd: un .timer que dice cuándo correr un .service.",
      "Son dos archivos: el .service dice qué hacer y el .timer cuándo (OnCalendar). Persistent=true corre la ejecución perdida si el equipo estaba apagado, y el resultado queda en el journal. Se habilita el .timer, no el servicio. Para algo simple de una línea, cron sigue alcanzando."),
    T("cron", "cron", ["crontab", "/etc/cron.d"],
      "El programador de tareas clásico de Unix: corre comandos a horas fijas.",
      "Una línea tiene cinco campos de tiempo (minuto, hora, día, mes, día de la semana) y el comando; en /etc/crontab y /etc/cron.d se agrega el usuario. Si la salida no se redirige o no hay MAILTO, los errores se pierden. Si el equipo estaba apagado a esa hora, la tarea no corre."),
    T("grub", "GRUB", ["GRand Unified Bootloader", "cargador de arranque"],
      "El cargador de arranque de Debian y Ubuntu: carga el kernel y el initramfs.",
      "Lo lanza el firmware (BIOS o UEFI). El Debian Handbook recomienda protegerlo con contraseña, porque desde su menú se puede arrancar con init=/bin/sh y entrar como root sin clave."),
    T("initramfs", "initramfs", ["initrd"],
      "Un sistema de archivos mínimo en RAM que el kernel usa para encontrar y montar el disco raíz.",
      "Lo carga el cargador de arranque junto con el kernel. Trae los módulos y scripts justos para el disco, RAID, LVM o cifrado; con la raíz montada, le pasa el control a systemd."),
    T("apt", "apt", ["apt-get", "apt update", "apt upgrade", "apt full-upgrade"],
      "El gestor de paquetes de Debian y Ubuntu: baja listas de repositorios, resuelve dependencias e instala.",
      "apt update baja las listas, apt upgrade instala lo nuevo sin quitar paquetes y apt full-upgrade puede quitar paquetes, por eso se reserva para el salto de versión. apt es para usar a mano y apt-get para scripts. Todo queda en /var/log/apt/history.log."),
    T("dpkg", "dpkg", ["paquete .deb", "dpkg-reconfigure"],
      "El instalador de bajo nivel de Debian: instala un paquete .deb, sin resolver dependencias.",
      "apt lo usa por debajo. dpkg-reconfigure vuelve a hacer las preguntas de configuración de un paquete instalado, como la de activar unattended-upgrades. Un .deb suelto con dependencias se instala con apt install ./archivo.deb."),
    T("unattended-upgrades", "unattended-upgrades", ["actualizaciones automáticas", "20auto-upgrades", "Automatic-Reboot"],
      "El paquete que aplica solo las actualizaciones de seguridad, una vez por día.",
      "Ubuntu lo trae instalado; en Debian 13 se verifica y, si falta, se instala. 20auto-upgrades lo activa con dos valores en \"1\" y 50unattended-upgrades define orígenes, exclusiones y reinicio. Automatic-Reboot viene en \"false\": o se fija una hora de madrugada o se reinicia en una ventana acordada. La marca de reinicio pendiente es /var/run/reboot-required."),
    T("lts", "LTS", ["Long Term Support"],
      "Long Term Support: una versión con soporte extendido de actualizaciones.",
      "Ubuntu publica una LTS cada dos años, en abril: 24.04 y 26.04, con cinco años de soporte estándar (26.04 hasta abril de 2031). Para servidores de clientes conviene una LTS."),
    T("debian", "Debian", ["trixie", "Debian 13"],
      "Distribución Linux comunitaria, base de Ubuntu y de muchos appliances.",
      "Nació en 1993. Debian 13 trixie salió en agosto de 2025 y tiene soporte regular hasta agosto de 2028. En los repositorios conviene usar el nombre (trixie) y no stable, para que el equipo no salte de versión solo cuando salga la próxima.", year=1993),
    T("ubuntu-server", "Ubuntu Server", ["Ubuntu", "Ubuntu 24.04", "Ubuntu 26.04"],
      "La edición para servidores de Ubuntu, la distribución de Canonical basada en Debian.",
      "Ubuntu 26.04 LTS salió en abril de 2026 y trae cambios que rompen guías viejas: sudo-rs en lugar de sudo, apt-key eliminado, /tmp en memoria, OpenSSH 10.2 y chrony con NTS para la hora."),
    T("sudo", "sudo", ["sudo-rs", "sudoers", "visudo"],
      "Comando para ejecutar otro comando como root (u otro usuario), sin compartir la clave de root.",
      "Se configura en sudoers, que se edita con visudo y se valida con visudo -c. En Ubuntu 26.04 es sudo-rs, reescrito en Rust: sudo -E se ignora con un aviso. Dar sudo sin contraseña (NOPASSWD) solo tiene sentido en una estación de un único usuario."),
    T("root", "root", ["superusuario"],
      "El usuario administrador de Linux, con todos los permisos.",
      "No confundir con la raíz del árbol, /: /root es solo la carpeta personal de root. Por SSH conviene PermitRootLogin no y trabajar con un usuario propio y sudo."),
    T("permisos-unix", "permisos de Unix", ["chmod", "chown", "rwx", "permisos octales"],
      "Lectura, escritura y ejecución (r, w, x) para el dueño, el grupo y el resto de cada archivo.",
      "En números, r=4, w=2 y x=1, sumados por categoría: 755 para directorios y programas, 644 para datos, 600 para secretos. chmod los cambia y chown cambia dueño y grupo. En un directorio, x es poder entrar. 777 deja escribir a cualquiera: lo que falta casi siempre es arreglar dueño y grupo."),
    T("setgid", "setgid", ["setuid", "SUID", "sticky bit"],
      "Bits especiales de permisos: setgid en un directorio hace que lo creado adentro herede el grupo de la carpeta.",
      "Es el 2 de 2770, y ls -l lo muestra como una s en el lugar de la x del grupo. El sticky bit, como en /tmp, impide borrar archivos ajenos. setuid hace que un programa corra con los permisos de su dueño: es riesgoso, y find / -perm /4000 lista los que lo tienen."),
    T("umask", "umask", [],
      "La máscara que define los permisos con que nacen los archivos y directorios nuevos.",
      "Con umask 0022, un archivo nace 644 y un directorio 755. Se fija en /etc/login.defs o pam_umask, o por sesión en ~/.bashrc."),
    T("uuid", "UUID", ["Universally Unique Identifier"],
      "Universally Unique Identifier: un identificador único, como el que lleva cada sistema de archivos.",
      "lsblk -f y blkid muestran el UUID de cada disco. En /etc/fstab se usa UUID=... y nunca /dev/sdX, porque los nombres del kernel cambian según el orden en que aparecen los discos al arrancar.", cat="Herramientas"),
    T("fstab", "fstab", ["/etc/fstab", "nofail"],
      "El archivo que dice qué disco se monta en qué carpeta al arrancar.",
      "Cada línea tiene seis campos: qué (UUID=...), dónde, tipo, opciones, dump y orden de chequeo. nofail deja arrancar aunque el disco falte y x-systemd.device-timeout=5 evita esperarlo 90 segundos. Un error puede dejar el equipo en modo emergencia: se valida con findmnt -x antes de reiniciar."),
    T("tmpfs", "tmpfs", [],
      "Sistema de archivos que vive en la memoria RAM y se vacía al reiniciar.",
      "En Ubuntu 26.04, /tmp es tmpfs con tope de la mitad de la RAM: un dump grande ahí ocupa memoria. Para archivos grandes temporales conviene /var/tmp."),
    T("inodo", "inodo", ["inodos", "inode", "df -i"],
      "La ficha que el sistema de archivos guarda por cada archivo; hay una cantidad fija.",
      "Millones de archivos chicos pueden agotar los inodos antes que el espacio: el disco dice lleno aunque df -h muestre lugar. df -i lo muestra.", case=False),
    T("logrotate", "logrotate", [],
      "Herramienta que rota, comprime y borra los logs de texto viejos de /var/log.",
      "Los programas que escriben su propio archivo de log dependen de logrotate para no llenar el disco; el journal de systemd tiene su propio tope."),
    T("lsof", "lsof", ["fuser"],
      "Lista los archivos abiertos por los procesos.",
      "lsof -p PID muestra lo que tiene abierto un proceso y fuser -v archivo dice qué proceso usa un archivo. Sirve cuando df y du no coinciden: un archivo borrado que un proceso sigue usando no libera su espacio."),
    T("grep", "grep", ["grep -rn"],
      "Busca texto dentro de archivos o en la salida de otro comando.",
      "-r recorre carpetas y -n agrega el número de línea. Con el truco del corchete, ps aux | grep \"[s]shd\", grep no aparece en su propia búsqueda."),
    T("yaml", "YAML", ["YAML Ain't Markup Language"],
      "Formato de texto para configuración basado en sangrías, usado por netplan y Docker Compose.",
      "La sangría es la estructura: dos espacios por nivel, nunca tabulaciones, y un espacio después de los dos puntos. Un error de sangría o una clave mal escrita, como adresses, hace fallar todo el archivo.", cat="Web e integración"),
    T("netplan", "netplan", ["netplan try", "netplan apply"],
      "La configuración de red de Ubuntu Server: archivos YAML en /etc/netplan.",
      "netplan generate valida, netplan apply aplica sin vuelta y netplan try aplica y vuelve solo a lo anterior si no confirmás con Enter en 120 segundos, la red de seguridad para cambios remotos. Los archivos van con permisos 600."),
    T("iproute2", "iproute2", ["ip addr", "ip route", "ip neigh", "ip -br addr"],
      "Las herramientas de red actuales de Linux: ip para interfaces, direcciones y rutas, y ss para conexiones.",
      "Reemplazan a net-tools: ifconfig pasa a ip addr, route a ip route, arp a ip neigh y netstat a ss. ip -br addr muestra una línea por interfaz y ss -tlnp lo que escucha y en qué dirección."),
    T("net-tools", "net-tools", ["ifconfig"],
      "Las herramientas de red viejas de Linux: ifconfig, route, arp y netstat.",
      "Muchos servidores ya no las traen. Sus equivalentes en iproute2 son ip addr, ip route, ip neigh y ss."),
    T("ufw", "ufw", ["Uncomplicated Firewall"],
      "Uncomplicated Firewall: la forma simple de configurar el firewall de host en Ubuntu.",
      "Viene instalado y deshabilitado. El orden seguro es default deny incoming, allow desde la red de gestión al 22 y recién ahí enable. Ojo: los puertos que publica Docker pasan por al lado de sus reglas."),
    T("nftables", "nftables", ["nft", "/etc/nftables.conf"],
      "El sucesor de iptables para escribir reglas de netfilter, por defecto en Debian.",
      "Entró al kernel 3.13 en 2014 y Debian lo usa por defecto desde Buster. Las reglas van en /etc/nftables.conf, se validan con nft -c -f y se cargan al arrancar con systemctl enable nftables; lo que se hace con nft en vivo se pierde al reiniciar.", year=2014),
    T("docker-user", "DOCKER-USER", [],
      "La cadena de netfilter que Docker deja para que el administrador filtre el tráfico hacia los contenedores.",
      "Los puertos publicados se redirigen en la tabla nat y pasan por forward, no por input: ufw no los ve. Si un puerto de contenedor tiene que ser público, se filtra por origen en DOCKER-USER; lo preferido es publicar en 127.0.0.1."),
    T("openssh", "OpenSSH", ["sshd", "sshd_config", "sshd -t"],
      "La implementación libre de SSH que viene en Debian y Ubuntu, cliente y servidor.",
      "La lanzó el proyecto OpenBSD en 1999. Para la mayoría de las opciones vale el primer valor leído, y los snippets de /etc/ssh/sshd_config.d se leen antes que el archivo principal. sshd -t valida y sshd -T muestra la configuración efectiva. Ubuntu 26.04 trae la versión 10.2.", year=1999),
    T("ed25519", "ed25519", ["llave ed25519", "id_ed25519"],
      "Algoritmo de llave SSH de curva elíptica: llave corta, rápida y recomendada.",
      "ssh-keygen la genera por defecto. La privada (id_ed25519) queda en tu equipo con 600 y la pública (.pub) se copia al servidor. RSA queda para equipos viejos; DSA ya no existe en OpenSSH 10."),
    T("dsa", "DSA", ["Digital Signature Algorithm"],
      "Digital Signature Algorithm: un tipo de llave SSH viejo, eliminado en OpenSSH 10.0.",
      "Un equipo viejo que solo acepta llaves DSA no va a hablar con un cliente OpenSSH actual: se usa ed25519 o, si el equipo no la soporta, RSA.", cat="Seguridad"),
    T("authorized-keys", "authorized_keys", ["ssh-copy-id"],
      "El archivo del servidor con las llaves públicas que pueden entrar a un usuario.",
      "Vive en ~/.ssh/authorized_keys, con ~/.ssh en 700 y el archivo en 600; si los permisos están abiertos, SSH ignora la llave. ssh-copy-id agrega tu pública. Borrar la línea de alguien le quita el acceso sin cambiar ninguna clave."),
    T("persourcepenalties", "PerSourcePenalties", [],
      "Opción de OpenSSH, activa por defecto, que penaliza a las direcciones que fallan la autenticación.",
      "Las rechaza un tiempo después de fallar: es un freno nativo a la fuerza bruta. Con solo llaves y PerSourcePenalties, fail2ban pasa a ser opcional. Los sondeos de monitoreo que abren el 22 y cortan pueden ganarse una penalidad.", cat="Seguridad"),
    T("fail2ban", "fail2ban", [],
      "Programa que lee logs y bloquea en el firewall las IP que fallan muchas veces.",
      "Con SSH solo por llave aporta poco y hay quien prefiere no correr como root algo que interpreta logs con datos del atacante; suma si hay contraseñas o paneles web con login expuestos.", cat="Seguridad"),
    T("sigterm", "SIGTERM", ["SIGKILL", "SIGHUP", "kill -9"],
      "Las señales para terminar un proceso: SIGTERM (15) pide terminar; SIGKILL (9) lo saca sin aviso.",
      "kill PID manda SIGTERM, que el programa puede atrapar para cerrar sus archivos. kill -9 manda SIGKILL, que no se puede atrapar: lo que estaba a medio escribir queda a medias. SIGHUP (1) se usa para pedir que relea la configuración. A un servicio, mejor systemctl restart."),
    T("load-average", "load average", ["carga promedio"],
      "La carga de un equipo: promedios de 1, 5 y 15 minutos de procesos corriendo o esperando.",
      "La muestran uptime y top. Se compara con la cantidad de núcleos (nproc): sostenida por encima, el equipo está saturado.", case=False),
    T("memavailable", "MemAvailable", ["columna available", "buff/cache"],
      "La estimación de memoria que se le puede dar a un programa sin ir a swap, contando la caché liberable.",
      "La sumó el kernel 3.14 en 2014 y free -h la muestra como available. free bajo es normal: Linux usa la RAM que sobra como caché de disco (buff/cache) y la suelta cuando un programa la pide. Muchos monitoreos alertan mirando free y no available."),
    T("swap", "swap", ["memoria swap"],
      "Espacio en disco que el sistema usa como memoria cuando la RAM no alcanza.",
      "Es mucho más lento que la RAM: un equipo que usa swap todo el tiempo necesita memoria o tiene un proceso que se la come. available dice cuánto queda antes de llegar a swap.", case=False),
    T("tar", "tar", [".tar.gz", "tar czf"],
      "Empaqueta carpetas en un solo archivo, comprimido con z (gzip).",
      "Su nombre viene de tape archive. tar czf crea, tar tzvf lista y tar xzf extrae; con -C elegís dónde, por ejemplo -C /tmp para probar una restauración sin pisar nada."),
    T("rsync", "rsync", [],
      "Copia y sincroniza carpetas, local o a otro equipo, transfiriendo solo lo que cambió.",
      "Apareció en 1996, de Andrew Tridgell y Paul Mackerras. rsync -av copia con permisos y fechas; -n simula sin copiar. Con enlaces duros entre copias diarias, cada día parece completo y ocupa solo lo que cambió.", year=1996),
    T("docker", "Docker", ["docker.io", "Docker Engine", "docker run"],
      "Plataforma para empaquetar programas en imágenes y correrlos como contenedores aislados.",
      "Apareció en 2013. Usa funciones del kernel Linux, como los espacios de nombres y los cgroups, y escribe sus propias reglas de netfilter. En Ubuntu, el paquete docker.io lo mantiene Canonical. Un puerto publicado con -p en todas las interfaces pasa por al lado de ufw.", year=2013),
    T("docker-volume", "volumen de Docker", ["volúmenes de Docker", "docker volume"],
      "El lugar donde Docker guarda los datos que tienen que sobrevivir al contenedor.",
      "Vive en /var/lib/docker/volumes. El contenedor se puede borrar y recrear desde la imagen; los datos del volumen siguen. docker volume inspect muestra su Mountpoint.", case=False),
    T("rsa", "RSA", ["Rivest-Shamir-Adleman", "RSA 4096"],
      "Algoritmo clásico de llave pública, usado en SSH, certificados y firmas.",
      "En SSH queda como alternativa para equipos viejos que no aceptan ed25519; Ubuntu sugiere RSA de 4096 bits en ese caso.", cat="Seguridad"),
    T("gnu", "GNU", ["GNU's Not Unix", "herramientas GNU"],
      "Proyecto de software libre que aportó las herramientas básicas que acompañan al kernel Linux.",
      "Lo inició Richard Stallman en 1983. Las distribuciones juntan el kernel Linux con herramientas GNU como bash, grep, tar y las coreutils; por eso se habla también de GNU/Linux.", year=1983),
    T("smart", "SMART", ["smartctl", "S.M.A.R.T."],
      "Self-Monitoring, Analysis and Reporting Technology: el autodiagnóstico que traen los discos.",
      "smartctl -a /dev/sda muestra la salud del disco y smartd la vigila. Sirve para cambiar un disco antes de que falle.", cat="Herramientas"),
]

ALIAS = {"dst-nat": ["DNAT"]}

GLOS = "/home/claude/ies-training/site2/data/glosario.json"
OUT = "/home/claude/ies-training/ilustraciones/linux/glosario-propuesta.json"
COMB = "/tmp/claude-0/-home-claude/e7efb7ec-f4b7-5f80-a457-304e3488cc08/scratchpad/glosario-linux.json"

g = json.load(open(GLOS, encoding="utf-8"))
by = {t["id"]: t for t in g["terms"]}
MOD = {
    "netfilter": {"long": by["netfilter"]["long"] + " En Debian se escribe hoy con nftables, y en Ubuntu ufw es la capa simple por encima."},
    "pid": {"long": by["pid"]["long"] + " En Linux, ps aux y pgrep lo muestran, kill PID le manda una señal y el PID 1 es systemd."},
}
P = {
    "nota": "Propuesta para el curso Linux. terms: entradas nuevas completas. alias_agregar: alias nuevos para entradas existentes. modificar: campos a reemplazar en entradas existentes. Probada sobre una copia combinada con glosario_check.py. Categoría nueva: Linux.",
    "terms": TERMS, "alias_agregar": ALIAS, "modificar": MOD,
}

# --- chequeos de duplicados: glosario vigente y propuestas de otros cursos
def keys(t):
    return {t["id"].lower(), t["term"].lower(), *[a.lower() for a in t.get("aliases", [])]}

vig = set()
for t in g["terms"]:
    vig |= keys(t)
otros = {}
for f in glob.glob("/home/claude/ies-training/ilustraciones/*/glosario-propuesta.json"):
    if "/linux/" in f:
        continue
    for t in json.load(open(f, encoding="utf-8")).get("terms", []):
        for k in keys(t):
            otros[k] = f.split("/")[-2]
mine = set()
for t in TERMS:
    ks = keys(t)
    if ks & vig:
        sys.exit(f"{t['id']}: choca con el glosario vigente: {ks & vig}")
    if ks & mine:
        sys.exit(f"{t['id']}: repetido dentro de la propuesta: {ks & mine}")
    mine |= ks
    hit = {k: otros[k] for k in ks if k in otros}
    if hit:
        print("AVISO, también en otra propuesta:", t["id"], hit)
for k, al in ALIAS.items():
    for a in al:
        if a.lower() in vig or a.lower() in mine:
            sys.exit(f"alias {a} ya existe")

json.dump(P, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
n0 = len(g["terms"])
g["terms"] += TERMS
for k, al in ALIAS.items():
    by[k]["aliases"] += [a for a in al if a not in by[k]["aliases"]]
for k, ch in MOD.items():
    by[k].update(ch)
json.dump(g, open(COMB, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
s = json.dumps(P, ensure_ascii=False)
print("ok", OUT, len(TERMS), "entradas nuevas sobre", n0, "· guiones largos:", "—" in s or "–" in s)
r = subprocess.run([sys.executable, "/home/claude/ies-training/tools/glosario_check.py", "linux", "--glosario", COMB], capture_output=True, text=True)
print(r.stdout[-2500:], r.stderr[-1500:], "exit", r.returncode)
