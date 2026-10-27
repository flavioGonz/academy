"""Genera ilustraciones/proxmox/glosario-propuesta.json y lo prueba sobre una copia combinada del glosario.

  python3 glosario_pmx.py    # escribe la propuesta y valida la copia en /tmp/claude-0/glosario-proxmox.json

terms: entradas nuevas completas. alias_agregar: alias nuevos para entradas existentes.
modificar: campos a reemplazar en entradas existentes. No toca site2/data/glosario.json.
"""
import json, subprocess, sys
from pathlib import Path

V = "Virtualización"


def t(id_, term, aliases, cat, short, long, case=True, year=None):
    d = {"id": id_, "term": term, "aliases": aliases, "cat": cat, "short": short, "long": long, "case": case}
    if year:
        d["year"] = year
    return d


T = [
    t("proxmox-ve", "Proxmox VE", ["Proxmox", "PVE", "Proxmox Virtual Environment"], V,
      "Plataforma de virtualización de código abierto basada en Debian: máquinas virtuales KVM y contenedores LXC con una web de gestión.",
      "La desarrolla Proxmox Server Solutions, en Viena; el proyecto empezó en 2007 y la primera versión estable salió en 2008. La 9.0 salió en agosto de 2025 sobre Debian 13 y la rama vigente es la 9.2. Suma clúster, alta disponibilidad, firewall y backups sin herramientas externas."),
    t("pbs", "PBS", ["Proxmox Backup Server"], V,
      "Proxmox Backup Server: servidor de backups para Proxmox VE con backups incrementales, deduplicación y verificación.",
      "Salió en 2020, escrito en Rust. Guarda cada backup como un índice de trozos que se comparten entre backups y entre VM. Se mantiene con prune, garbage collection y verify. Su web va en el puerto 8007."),
    t("kvm", "KVM", ["Kernel-based Virtual Machine"], V,
      "Kernel-based Virtual Machine: módulo del kernel Linux que usa VT-x o AMD-V para correr máquinas virtuales.",
      "Entró al kernel Linux 2.6.20 en 2007. Junto con QEMU es el motor de las VM de Proxmox VE: KVM ejecuta el código del invitado en el CPU real y QEMU arma el hardware virtual. No confundir con un KVM switch de teclado, video y mouse."),
    t("qemu", "QEMU", [], V,
      "Emulador y virtualizador de código abierto que arma el hardware virtual de cada VM.",
      "Lo empezó Fabrice Bellard en 2003. En Proxmox VE cada VM es un proceso QEMU con su VMID; con KVM, las vCPU corren directo en el procesador y QEMU atiende discos, placas y consola."),
    t("lxc", "LXC", ["contenedor LXC", "contenedores LXC", "Linux Containers", "CT"], V,
      "Linux Containers: contenedores de sistema que comparten el kernel del host y aíslan procesos, red y archivos.",
      "Apareció en 2008 y Proxmox lo usa desde la versión 4.0, cuando reemplazó a OpenVZ. Arranca en segundos y gasta poco, pero solo corre Linux. El default en Proxmox es el contenedor no privilegiado, donde el root de adentro es un usuario sin poder del host."),
    t("zfs", "ZFS", ["OpenZFS"], "Servidores y almacenamiento",
      "Sistema de archivos y gestor de discos que verifica cada bloque con checksums, comprime, hace snapshots, RAID por software y replicación.",
      "Lo creó Sun Microsystems y salió en 2005; hoy lo mantiene el proyecto OpenZFS. Proxmox lo trae de fábrica desde 2014. Pide RAM para su caché (ARC), mejor ECC, y discos directos por HBA: nunca encima de una RAID por hardware con caché."),
    t("lvm-thin", "LVM-thin", ["LVM", "thin pool", "local-lvm", "lvmthin"], "Servidores y almacenamiento",
      "Variante de LVM que reserva espacio recién cuando se escribe: un disco de 32 GB con 3 GB de datos ocupa 3 GB.",
      "Es el almacenamiento que deja el instalador de Proxmox VE con ext4 o xfs, el thin pool data que la web muestra como local-lvm. Permite snapshots y linked clones. No verifica datos ni hace RAID: se apoya en lo que tenga debajo."),
    t("arc", "ARC", ["Adaptive Replacement Cache", "zfs_arc_max"], "Servidores y almacenamiento",
      "La caché de lectura de ZFS en memoria RAM.",
      "Desde Proxmox VE 8.1 el instalador la limita al 10 % de la RAM con tope de 16 GiB. La regla oficial es 2 GiB más 1 GiB por TiB de pool. El límite se fija en bytes en /etc/modprobe.d/zfs.conf."),
    t("hba", "HBA", ["Host Bus Adapter", "modo IT"], "Servidores y almacenamiento",
      "Host Bus Adapter: controladora que entrega los discos directos al sistema, sin armar RAID.",
      "Es lo que pide ZFS. Muchas controladoras RAID se pueden pasar a modo IT para comportarse como HBA."),
    t("ssd-datacenter", "SSD de datacenter", ["SSD de consumo"], "Servidores y almacenamiento",
      "Disco de estado sólido, sin partes móviles.",
      "Para Proxmox, y sobre todo para ZFS, la guía oficial desaconseja los SSD de consumo y prefiere los de datacenter, con protección contra cortes de energía (PLP) y más resistencia al desgaste."),
    t("plp", "PLP", ["Power Loss Protection"], "Servidores y almacenamiento",
      "Power Loss Protection: capacitores en un SSD que le permiten terminar de guardar lo que tiene en caché si se corta la luz.",
      "Es típica de los SSD de datacenter. Con PLP el disco puede confirmar escrituras más rápido sin riesgo de perderlas, algo que ZFS aprovecha."),
    t("ecc", "ECC", ["memoria ECC", "Error-Correcting Code"], "Servidores y almacenamiento",
      "Memoria RAM que detecta y corrige errores de bits.",
      "La guía de Proxmox la recomienda para ZFS, que confía en la RAM para su caché y sus checksums."),
    t("ha-proxmox", "HA de Proxmox", ["ha-manager", "alta disponibilidad"], V,
      "Alta disponibilidad: si un nodo de un clúster cae, sus VMs arrancan solas en otro nodo.",
      "En Proxmox VE se maneja con ha-manager desde la versión 4.0. Exige tres votos de quórum, almacenamiento compartido o replicación, y fencing por watchdog. En la 9, los grupos de HA pasaron a reglas de afinidad y la 9.2 sumó el disarm para mantenimiento."),
    t("fencing", "fencing", ["self-fencing"], V,
      "Asegurar que un nodo con falla esté apagado antes de arrancar sus servicios en otro nodo.",
      "Evita que dos nodos escriban a la vez el mismo disco de una VM, lo que la destruiría. Proxmox lo hace con un watchdog: el nodo que pierde el quórum se reinicia solo a los 60 segundos."),
    t("watchdog", "watchdog", ["softdog", "watchdog-mux"], V,
      "Temporizador que reinicia el equipo si el software no lo renueva a tiempo.",
      "Se usa en sistemas críticos desde los primeros microcontroladores. En Proxmox VE, ha-manager lo renueva mientras el nodo tiene quórum; puede ser el watchdog de hardware de la placa o el softdog del kernel.", case=False),
    t("quorum", "quórum", ["quorum", "Quorate"], V,
      "La mayoría de votos que un clúster necesita para poder cambiar algo.",
      "En Proxmox VE cada nodo vota y sin mayoría el clúster pasa a solo lectura: no se crean ni arrancan VMs. Con dos nodos, perder uno es perder la mayoría; por eso se suma un QDevice.", case=False),
    t("corosync", "corosync", [], V,
      "Motor de comunicación de clúster que entrega los mensajes a todos los nodos en orden y cuenta los votos del quórum.",
      "Nació del proyecto OpenAIS. Pide latencia menor a 5 ms, red propia y un segundo enlace; usa UDP 5405 a 5412. Sobre él, Proxmox replica /etc/pve.", case=False),
    t("qdevice", "QDevice", ["corosync-qdevice", "corosync-qnetd", "qnetd"], V,
      "Voto externo para un clúster: un servicio en un tercer equipo que no corre VMs, solo vota.",
      "Se instala corosync-qnetd en el tercer equipo y corosync-qdevice en los nodos, y se configura con pvecm qdevice setup. Va por TCP y puede estar en otra sede. Se recomienda en clústeres pares."),
    t("pmxcfs", "pmxcfs", ["Proxmox Cluster File System", "/etc/pve"], V,
      "El sistema de archivos de clúster de Proxmox: una base de datos replicada por corosync que se ve como /etc/pve.",
      "Guarda la configuración de todas las VM y nodos, y la copia a todo el clúster en tiempo real. Sin quórum queda en solo lectura.", case=False),
    t("migracion-en-vivo", "migración en vivo", ["live migration", "online migration", "qm migrate"], V,
      "Mover una VM encendida de un nodo a otro sin cortar el servicio.",
      "La memoria se copia en pasadas mientras la VM corre, cada vez solo lo que cambió, hasta que el resto se manda en milisegundos. Con almacenamiento compartido el disco no viaja; con disco local se agrega --with-local-disks.", case=False),
    t("vzdump", "vzdump", [], V,
      "La herramienta de backup de Proxmox VE: guarda configuración y discos de una VM o contenedor en un archivo completo.",
      "Tiene modos stop, suspend y snapshot. El nombre viene de la época de OpenVZ. Los archivos quedan como vzdump-qemu-VMID-fecha.vma.zst.", case=False),
    t("copy-on-write", "copy-on-write", ["CoW"], V,
      "Técnica de almacenamiento que escribe los cambios en bloques nuevos y deja los viejos intactos.",
      "Es lo que hace instantáneos a los snapshots y los linked clones: no se copia nada hasta que algo cambia. Los backups de QEMU usan una idea hermana, copy-before-write: antes de pisar un bloque, se copia el viejo al backup.", case=False),
    t("virtio", "VirtIO", ["virtio-win", "VirtIO SCSI single", "paravirtualización"], V,
      "Dispositivos virtuales pensados para VM: el invitado sabe que es virtual y habla con el host por colas compartidas.",
      "Rinden mucho más que emular hardware real. Linux trae los drivers; Windows los necesita desde el ISO virtio-win, en la versión que la wiki de Proxmox marca sin problemas. Hoy es una especificación de OASIS."),
    t("guest-agent", "guest agent", ["QEMU guest agent", "qemu-guest-agent"], V,
      "Servicio dentro de la VM que atiende pedidos del host: apagado limpio, IPs y congelar el disco antes de un backup.",
      "Se activa con qm set VMID --agent 1, se instala adentro y se prueba con qm agent VMID ping. En Windows viene con virtio-win-guest-tools.", case=False),
    t("cloud-init", "cloud-init", [], V,
      "Programa que configura una VM en su primer arranque: usuario, claves SSH, red y disco.",
      "Lo creó Canonical para las nubes públicas. En Proxmox VE lee sus datos de un CD que genera el propio Proxmox; se completa con ciuser, sshkeys e ipconfig0.", case=False),
    t("linked-clone", "linked clone", ["full clone", "clon enlazado"], V,
      "Clon de VM que lee de la plantilla y guarda aparte solo sus cambios.",
      "Es casi instantáneo y ocupa poco, pero depende de la plantilla: si se borra, se rompe. Un full clone copia todo el disco y queda independiente; es lo que va a producción.", case=False),
    t("bond", "bond", ["bonding", "LACP", "802.3ad"], "Redes",
      "Varias placas de red unidas como una sola, para redundancia y más ancho de banda.",
      "Con LACP (IEEE 802.3ad, de 2000) el switch negocia el grupo; si no lo soporta, active-backup. En Proxmox VE el bridge va encima del bond.", case=False),
    t("vlan-aware", "VLAN aware", ["bridge VLAN-aware", "bridge-vlan-aware"], "Redes",
      "Bridge de Linux que maneja VLAN por puerto: un solo bridge lleva todas las VLAN y cada VM pone su tag.",
      "En Proxmox VE se tilda en vmbr0 y en el archivo queda bridge-vlan-aware yes y bridge-vids 2-4094. Reemplaza al modo viejo de un bridge por VLAN."),
    t("vmid", "VMID", ["CTID"], V,
      "Número que identifica una VM o un contenedor en Proxmox VE.",
      "Es único en todo el clúster y aparece en los archivos de configuración (/etc/pve/qemu-server/100.conf), en los backups y en los puertos tap del bridge."),
    t("deb822", "deb822", [".sources"], "Herramientas",
      "Formato de los repositorios de apt en bloques de campos (Types, URIs, Suites, Components), en archivos .sources.",
      "Desde Debian 13 apt se queja del formato viejo de una línea. Un repositorio se deshabilita con Enabled: no, y apt modernize-sources migra los archivos .list.", case=False),
    t("totp", "TOTP", ["Time-based One-Time Password"], "Seguridad",
      "Código de un solo uso que cambia cada 30 segundos, generado por una app del celular.",
      "Lo define la RFC 6238, de 2011. Es uno de los segundos factores de Proxmox VE, junto con WebAuthn y las claves de recuperación."),
    t("rfc6238", "RFC 6238", ["RFC6238"], "RFC",
      "TOTP: el algoritmo de contraseñas de un solo uso basadas en la hora.",
      "Extiende el HOTP de la RFC 4226 usando la hora como contador, en general en pasos de 30 segundos. Es lo que usan las apps de autenticación del celular.", year=2011),
    t("webauthn", "WebAuthn", ["llave de seguridad", "Web Authentication"], "Seguridad",
      "Estándar del W3C para iniciar sesión con una llave de seguridad o el lector biométrico del equipo.",
      "En Proxmox VE es uno de los segundos factores. Conviene registrar más de uno para no quedar afuera si se pierde la llave."),
    t("ipmi", "IPMI", ["iKVM", "consola fuera de banda"], "Servidores y almacenamiento",
      "Interfaz de gestión de la placa del servidor: consola, encendido y apagado aunque el sistema operativo no responda.",
      "Es la red de rescate cuando un cambio de red o un firewall deja al host inaccesible, y la consola recomendada para un upgrade mayor."),
    t("ipset", "IPSet", ["IPSet management", "ipset"], "Seguridad",
      "Lista de direcciones IP con nombre que usan las reglas del firewall.",
      "En Proxmox VE, el IPSet llamado management define desde qué IPs se puede administrar el host: cargarlo antes de habilitar el firewall evita quedarse afuera."),
    t("prune", "prune", ["prune job"], V,
      "Tarea de PBS que aplica la retención: borra los índices de los backups que sobran.",
      "No libera espacio por sí sola: los trozos de datos siguen hasta la garbage collection. La retención se puede probar en el Prune Simulator.", case=False),
    t("garbage-collection", "garbage collection", ["GC"], V,
      "Tarea de PBS que borra los trozos que ya no usa ningún backup y libera el espacio.",
      "Respeta un período de gracia de 24 horas y 5 minutos. Semanal es un buen punto de partida; diaria si el datastore se llena rápido.", case=False),
    t("verify-job", "verify job", ["verify"], V,
      "Tarea de PBS que relee los backups y compara sus checksums para detectar corrupción.",
      "Conviene un job frecuente para lo nuevo y reverificar todo al menos una vez por mes. Si un ransomware cifra backups, el verify falla y sirve de alarma.", case=False),
    t("ceph", "Ceph", [], "Servidores y almacenamiento",
      "Almacenamiento distribuido que reparte los datos entre varios servidores.",
      "Proxmox VE puede correrlo en los mismos nodos del clúster: pide al menos tres servidores, mejor idénticos, y red dedicada de 10 Gbps o más."),
    t("tmux", "tmux", [], "Herramientas",
      "Programa que mantiene una sesión de terminal viva aunque se corte la conexión SSH.",
      "Para un upgrade mayor de Proxmox se trabaja dentro de tmux: si se corta la red, el upgrade sigue y te volvés a conectar a la misma sesión.", case=False),
    t("vss", "VSS", ["Volume Shadow Copy"], "Herramientas",
      "Servicio de Windows que congela los datos para sacar copias consistentes.",
      "El guest agent de Proxmox lo usa en VM Windows para que el backup en modo snapshot salga consistente."),
    t("oci", "OCI", ["imágenes OCI"], V,
      "Open Container Initiative: el formato estándar de imágenes de contenedores de aplicación, como las de Docker.",
      "Proxmox VE puede crear contenedores desde imágenes OCI como tecnología en preview; para Docker en producción, la recomendación sigue siendo una VM."),
    t("realm", "realm", ["realms", "PAM", "realm pve"], "Seguridad",
      "En Proxmox VE, el lugar contra el que se valida un usuario: PAM, PVE, LDAP o Active Directory.",
      "PAM son los usuarios del sistema Linux (como root@pam); PVE guarda contraseñas propias de Proxmox y es lo más cómodo en instalaciones chicas (tecnico@pve). El realm va después de la arroba en el nombre de usuario.", case=False),
    t("cifs", "CIFS", ["SMB", "recurso compartido de Windows"], "Servidores y almacenamiento",
      "Protocolo de Windows para compartir carpetas por la red.",
      "En Proxmox VE se agrega como almacenamiento de tipo archivo, igual que NFS, para backups e ISOs."),
]

ALIAS = {"mfa": ["segundo factor"]}
MOD_SNAP = " En Proxmox VE, sobre LVM-thin o ZFS, el snapshot es copy-on-write: instantáneo, y vive en el mismo pool que el disco."

ROOT = Path("/home/claude/ies-training")
GLOS = ROOT / "site2/data/glosario.json"
OUT = ROOT / "ilustraciones/proxmox/glosario-propuesta.json"
COMB = Path("/tmp/claude-0/glosario-proxmox.json")

g = json.load(open(GLOS, encoding="utf-8"))
by = {x["id"]: x for x in g["terms"]}
P = {"nota": "Propuesta para el curso Proxmox VE. terms: entradas nuevas completas (categorías existentes Virtualización y Servidores y almacenamiento). alias_agregar: alias nuevos para entradas existentes. Probada sobre una copia combinada con glosario_check.py.",
     "terms": T, "alias_agregar": ALIAS, "modificar": {"snapshot": {"long": by["snapshot"]["long"] if MOD_SNAP.strip() in by["snapshot"]["long"] else by["snapshot"]["long"] + MOD_SNAP}}}
json.dump(P, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
dup = [x["id"] for x in T if x["id"] in by]
if dup:
    sys.exit(f"ids que ya existen en el glosario: {dup}")
n0 = len(g["terms"])
g["terms"] += T
for k, al in ALIAS.items():
    by[k]["aliases"] += [a for a in al if a not in by[k]["aliases"]]
for k, ch in P["modificar"].items():
    by[k].update(ch)
COMB.parent.mkdir(parents=True, exist_ok=True)
json.dump(g, open(COMB, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
s = json.dumps(P, ensure_ascii=False)
print("ok", OUT, len(T), "entradas nuevas sobre", n0, "· guiones largos:", "—" in s or "–" in s)
r = subprocess.run([sys.executable, str(ROOT / "tools/glosario_check.py"), "proxmox", "--glosario", str(COMB)], capture_output=True, text=True)
print(r.stdout[-2500:], r.stderr, "exit", r.returncode)
