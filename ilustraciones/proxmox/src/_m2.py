"""Manifest Proxmox, lecciones 5 a 8 (lo arma manifest_pmx.py)."""
from _mbase import L, C, S

# =====================================================================================  5
L("5",
  {"file": "5.svg", "alt": "Recorrido en cuatro bloques: imagen cloud debian-13-genericcloud-amd64.qcow2, VM 9000 con el disco importado y una unidad cloud-init, plantilla con qm template 9000 que ya no arranca, y clones 201, 202, 203 en full clone. Debajo, lo que cada clon recibe desde Proxmox por cloud-init en el primer arranque: usuario tecnico, clave SSH id_ed25519.pub, IP 10.10.10.201/24 y gateway 10.10.10.1. Notas: instalar desde ISO lleva unos veinte minutos y clonar menos de uno, y todas quedan iguales; un linked clone depende de la plantilla y se rompe si se borra, así que para producción, full clone.",
   "caption": "Imagen, disco, cloud-init, plantilla y clones: la línea de montaje de VMs."},
  [{"file": "5-paso2.svg", "step": 2, "after": "Creá la VM base, importá el disco",
    "alt": "Seis comandos con lo que deja cada uno en la VM 9000: qm create con virtio-scsi-single y agent 1 crea la VM vacía con CPU, RAM, red VirtIO y agente; qm set scsi0 con import-from de la imagen qcow2 deja el disco de la imagen cloud; qm set ide2 local-lvm:cloudinit agrega el CD de cloud-init; qm set boot order=scsi0 hace que arranque del disco importado; qm set serial0 socket y vga serial0 dan la consola serie que piden las imágenes cloud; qm template 9000 la convierte en plantilla. Los puntos suspensivos son las mismas opciones del laboratorio, abreviadas.",
    "caption": "Cada línea del paso 2 deja una pieza de la plantilla."},
   {"file": "5-paso3.svg", "step": 3, "after": "Si no tenés clave SSH en el host",
    "alt": "La plantilla 9000 se clona con --full 1 a la VM 201 prueba-ci, una copia independiente que se agranda con qm resize 201 scsi0 +10G. Lo que va al CD de cloud-init: qm set 201 con ciuser tecnico, sshkeys /root/.ssh/id_ed25519.pub e ipconfig0 ip=10.10.10.201/24,gw=10.10.10.1. En el primer arranque la VM crea el usuario tecnico, copia la clave SSH, pone 10.10.10.201/24 y el gateway 10.10.10.1. Después se mira el arranque en xterm.js y se entra con ssh tecnico@10.10.10.201. Nota: si cambiás cloud-init después, qm cloudinit update 201; mejor claves SSH que contraseña.",
    "caption": "El clon nace con usuario, clave e IP que le diste desde Proxmox."}],
  [C("Plantilla",
     "Instalar cada VM desde un ISO lleva tiempo y cada técnico la deja un poco distinta. Una plantilla es una VM preparada una vez y congelada: no arranca, solo sirve de molde para clonar.",
     "Se crea la VM con el hardware correcto (VirtIO, agente, consola serie si hace falta), se le pone el disco y la unidad cloud-init, y `qm template VMID` la convierte. Se le da un VMID alto y fácil de reconocer, como 9000. Cuando sale una versión nueva de la imagen, se arma otra plantilla.",
     "En IES tenés una plantilla Debian 13 en el clúster interno. Cuando un cliente pide un servidor nuevo para el software de control de acceso, en un minuto tenés la VM con usuario, clave e IP, y te dedicás a instalar lo que importa."),
   C("cloud-init",
     "Una imagen genérica no sabe qué usuario, clave ni IP tiene que tener. cloud-init es un programa que corre en el primer arranque, lee esa configuración de una fuente externa y se la aplica a la VM.",
     "En Proxmox la fuente es un CD que genera el propio Proxmox (`--ide2 local-lvm:cloudinit`). Se completa con `--ciuser`, `--sshkeys` e `--ipconfig0`, o en la pestaña Cloud-Init. Si cambiás algo después, `qm cloudinit update VMID` regenera el CD. Proxmox recomienda clave SSH antes que contraseña, porque la contraseña queda guardada en los datos de cloud-init.",
     "Clonás tres VM para un cliente en Rivera: cada una con su IP fija del rango del cliente y la misma clave SSH del equipo de soporte. Ninguna pasa por un instalador ni por un teclado."),
   C("Full clone y linked clone",
     "Clonar puede ser copiar todo el disco o apenas apuntar a la plantilla. El linked clone es casi instantáneo y ocupa poco porque reutiliza los bloques de la plantilla y guarda aparte solo lo que cambia; el full clone es una copia completa e independiente.",
     "`qm clone 9000 201 --full 1` hace un full clone. Sin `--full`, desde una plantilla, el clon es linked. El linked depende de la plantilla para siempre: si la plantilla desaparece, se rompe. Regla del curso: si la VM va a vivir más que la plantilla, full clone.",
     "Para un laboratorio de capacitación armás diez VM linked que se borran al final del día. Para el servidor del cliente en producción, full clone, aunque tarde un poco más."),
   C("Imagen cloud",
     "Las distribuciones publican imágenes de disco ya instaladas y mínimas, pensadas para nubes y plataformas de virtualización. Traen cloud-init y no tienen usuario ni clave cargados.",
     "Se baja la imagen (Debian 13 genericcloud, en formato qcow2) a /root/ del host y se importa como disco con `import-from`. Muchas necesitan consola serie (`--serial0 socket --vga serial0`). Proxmox recomienda armar la propia imagen para saber exactamente qué tiene.",
     "Bajás debian-13-genericcloud-amd64.qcow2 de cloud.debian.org, la importás y en el primer arranque ves por xterm.js cómo cloud-init crea el usuario y levanta la red.")],
  """
### Un poco de historia

cloud-init lo creó Canonical para que las imágenes de Ubuntu arrancaran listas en las nubes públicas, donde nadie se sienta frente a un instalador. Con el tiempo lo adoptaron casi todas las distribuciones, y Debian publica imágenes genericcloud que lo traen de fábrica. Proxmox lo integró generando un CD de configuración desde el propio hipervisor.

Las plantillas y los clones son anteriores: vienen de la idea de copy-on-write que ya usan LVM-thin y ZFS para los snapshots. Una guía de práctica lo resume con números: clonar una plantilla lleva menos de un minuto, contra unos veinte de instalar desde ISO.

### Cómo funciona

El recorrido tiene cuatro piezas. Primero, la imagen cloud: un disco con el sistema ya instalado, sin usuario ni red configurados. Segundo, la VM base: `qm create` arma el hardware y `import-from` copia la imagen como disco scsi0. Tercero, la unidad cloud-init, un CD que Proxmox genera con los datos de cada VM. Cuarto, `qm template`, que congela la VM como molde.

Al clonar hay dos caminos. El linked clone no copia el disco: lee de la plantilla y escribe aparte sus cambios, con copy-on-write. Es inmediato y ocupa poco, pero queda atado a la plantilla. El full clone copia todos los bloques: tarda más, ocupa más y no depende de nadie.

En el primer arranque, cloud-init busca su fuente de datos, encuentra el CD de Proxmox y aplica lo que dice: crea el usuario de `--ciuser`, copia la clave pública de `--sshkeys`, configura la IP y el gateway de `--ipconfig0` y agranda la partición si el disco creció con `qm resize`. Desde ese momento la VM es una más, con nombre, red y acceso propios.

Si después cambiás un dato de cloud-init, el CD no se actualiza solo: `qm cloudinit update` lo regenera. Y como la contraseña viaja dentro de esos datos, conviene la clave SSH.
""",
  [{"file": "5-t1.svg", "after": "Es inmediato y ocupa poco, pero queda atado a la plantilla.",
    "alt": "Animación en cuatro tiempos. 1: la plantilla 9000 tiene los bloques A, B, C y D, ahora de solo lectura. 2: el linked clone, VM 201, se crea al instante: sus bloques A, B y D apuntan a la plantilla y solo guarda aparte lo que cambió, el bloque C1. 3: el full clone, VM 202, copia los cuatro bloques uno por uno: tarda más pero queda independiente. 4: si la plantilla se borra, al linked clone le faltan bloques y se rompe; el full clone sigue andando.",
    "caption": "El linked clone pide prestados los bloques de la plantilla; el full clone tiene los suyos."}],
  S("Crear la plantilla Debian 13 y un clon full con cloud-init",
    "Crea la plantilla desde la imagen cloud si no existe y clona una VM full con usuario, clave SSH e IP fija. No pisa VMIDs que ya existan.",
    [("TPL_ID", "9000", "VMID de la plantilla"), ("VMID", "201", "VMID del clon"), ("NOMBRE", "prueba-ci", "Nombre del clon"),
     ("STORAGE", "local-lvm", "Almacenamiento de discos"), ("IMAGEN", "/root/debian-13-genericcloud-amd64.qcow2", "Imagen cloud bajada en el paso 1"),
     ("USUARIO", "tecnico", "Usuario que crea cloud-init"), ("CLAVE_SSH", "/root/.ssh/id_ed25519.pub", "Clave pública"),
     ("IP_CIDR", "10.10.10.201/24", "IP fija del clon (rango de documentación)"), ("GATEWAY", "10.10.10.1", "Gateway")],
    """# IES Training - Proxmox VE - Plantilla y clon
# Correlo como root en el host. No pisa VMs existentes.
(
TPL="{{TPL_ID}}"; VMID="{{VMID}}"; NOMBRE="{{NOMBRE}}"; STORAGE="{{STORAGE}}"
IMG="{{IMAGEN}}"; USUARIO="{{USUARIO}}"; CLAVE="{{CLAVE_SSH}}"
IP="{{IP_CIDR}}"; GW="{{GATEWAY}}"
test -e "$IMG" || { echo "Falta la imagen $IMG: bajala de cloud.debian.org (paso 1)"; exit 1; }
test -e "$CLAVE" || { echo "Falta la clave $CLAVE: creala con ssh-keygen"; exit 1; }
if [ -e /etc/pve/qemu-server/$TPL.conf ]; then
  echo "Ya existe el VMID $TPL: no creo la plantilla"
else
  qm create $TPL --name debian13-tpl --memory 2048 --cores 2 --net0 virtio,bridge=vmbr0 --scsihw virtio-scsi-single --agent 1
  qm set $TPL --scsi0 $STORAGE:0,import-from=$IMG
  qm set $TPL --ide2 $STORAGE:cloudinit
  qm set $TPL --boot order=scsi0
  qm set $TPL --serial0 socket --vga serial0
  qm template $TPL
fi
if [ -e /etc/pve/qemu-server/$VMID.conf ]; then
  echo "Ya existe la VM $VMID: no clono"
else
  qm clone $TPL $VMID --name $NOMBRE --full 1
  qm set $VMID --ciuser $USUARIO --sshkeys $CLAVE --ipconfig0 ip=$IP,gw=$GW
  qm resize $VMID scsi0 +10G
  qm start $VMID
fi
echo "Listo: plantilla $TPL y VM $VMID. Mira el arranque en xterm.js y entra con ssh $USUARIO@${IP%/*}"
)""",
    ["Si el VMID de la plantilla ya existe y no es una plantilla, el script no la toca: revisalo a mano.",
     "Si cambiás datos de cloud-init después del primer arranque: qm cloudinit update <VMID>."]))

# =====================================================================================  6
L("6",
  {"file": "6.svg", "alt": "Dos pilas lado a lado. Máquina virtual con KVM, de arriba hacia abajo: aplicaciones, kernel propio del invitado, hardware virtual de QEMU, kernel del host con KVM y hardware. Contenedor LXC: aplicaciones, sistema de archivos y procesos aislados sin kernel propio, kernel del host compartido y hardware. Debajo de la VM, tildes verdes: aísla más con otro kernel, corre Windows o cualquier Linux, y es donde van Docker y lo expuesto a internet. Debajo del contenedor: arranca en segundos y gasta poco, en verde; solo Linux con el mismo kernel del host, y si el kernel se compromete afecta al host, en ámbar.",
   "caption": "La diferencia de fondo: la VM trae su kernel; el contenedor usa el del host."},
  [{"file": "6-paso3.svg", "step": 3, "after": "Creá un contenedor no privilegiado",
    "alt": "Las opciones de pct create, una por fila: 300 es el CTID, como el VMID de una VM; local:vztmpl y el nombre de la plantilla es la plantilla Debian bajada con pveam; hostname ct-prueba es el nombre; unprivileged 1, resaltada en verde, es no privilegiado, el default y lo seguro; memory 512 son los MB de RAM; rootfs local-lvm:8 es un disco raíz de 8 GB en local-lvm; net0 name=eth0,bridge=vmbr0,ip=dhcp es la placa eth0 en vmbr0 con IP por DHCP; password con una clave de ejemplo que hay que cambiar. Después, pct start 300 y pct enter 300.",
    "caption": "Una línea crea el contenedor; la opción que importa es --unprivileged 1."},
   {"file": "6-paso4.svg", "step": 4, "after": "Entrá y mirá el mapeo de usuarios",
    "alt": "Adentro del CT 300, cat /proc/self/uid_map muestra 0, 100000 y 65536: el uid 0 de adentro corresponde al uid 100000 del host, y se mapean 65536 uid en fila. A la izquierda, el contenedor 300 con root, uid 0, y la serie uid 1 a 100001 hasta uid 65535 a 165535; una flecha lleva al host Proxmox, donde ese root es uid 100000, un usuario sin privilegios que no puede tocar archivos del host. Nota: en el host, pct config 300 con grep unprivileged tiene que mostrar unprivileged: 1; en un contenedor privilegiado, el root de adentro sería el root del host.",
    "caption": "El root del contenedor es, para el host, un usuario sin poder."}],
  [C("Contenedor LXC",
     "Muchos servicios Linux no necesitan una máquina entera: alcanza con aislar sus procesos y su sistema de archivos. Un contenedor LXC hace eso compartiendo el kernel del host, así que arranca en segundos y gasta mucho menos que una VM.",
     "Se baja una plantilla con `pveam` y se crea con `pct create`, o desde Create CT en la GUI. Se usa para servicios Linux livianos e internos: un DNS, un servidor de archivos chico, una herramienta de monitoreo. Para Windows, para lo expuesto a internet o para Docker en producción, VM.",
     "En el servidor de una cadena de farmacias armás un contenedor Debian con el colector de logs de las cámaras: 512 MB de RAM y arranca en segundos, sin gastar lo que pediría una VM."),
   C("Contenedor no privilegiado",
     "Si el root de adentro fuera el root del host, una falla que deje escapar un proceso del contenedor le daría todo el servidor. El contenedor no privilegiado mapea ese root a un usuario sin poder del host, y el equipo de LXC lo considera seguro por diseño.",
     "Es el default al crear (`--unprivileged 1`). Adentro, /proc/self/uid_map muestra la traducción: 0 adentro es 100000 afuera. Los privilegiados se reservan para entornos de confianza: el equipo de LXC no trata sus escapes como fallas de seguridad.",
     "Un proveedor te pide un contenedor privilegiado para su software. Antes de aceptar, preguntás qué necesita de verdad; casi siempre alcanza con uno no privilegiado y algún permiso puntual."),
   C("Docker en VM",
     "Docker es otra capa de contenedores, y meterlo adentro de un LXC suma complejidad: algunos contenedores piden modo privilegiado y un upgrade de Proxmox puede romperlo. La documentación oficial recomienda correrlo dentro de una VM.",
     "Una VM Debian o Ubuntu con Docker adentro: kernel propio, migración en vivo, HA y backups rápidos en PBS. En el foro mucha gente lo corre en LXC para ahorrar recursos; para el curso, LXC no privilegiado solo en laboratorio o servicio interno chico, sabiendo que un upgrade puede romperlo.",
     "El cliente quiere su sistema de gestión de visitas en contenedores Docker y expuesto a internet. Va en una VM con 4 GB y 32 GB de disco, con su backup en PBS.")],
  """
### Un poco de historia

Los contenedores en Linux vienen de juntar dos funciones del kernel: los namespaces, que le dan a un grupo de procesos su propia vista del sistema (procesos, red, usuarios), y los cgroups, que limitan cuánta CPU y memoria pueden usar. LXC apareció en 2008 como la forma de manejar esas piezas desde afuera. Los contenedores no privilegiados llegaron después, cuando el kernel completó los namespaces de usuario, alrededor de 2013, y LXC 1.0 los incorporó.

Proxmox usó OpenVZ para contenedores hasta la versión 4.0, que pasó a LXC. Desde entonces los contenedores comparten almacenamiento y red con las VM. Proxmox VE 9 dejó atrás cgroup v1: contenedores con sistemas muy viejos, como CentOS 7, ya no corren.

### Cómo funciona

Una VM tiene un kernel propio sobre hardware virtual. Un contenedor no: sus procesos corren en el kernel del host, igual que cualquier otro programa, pero encerrados en namespaces. Ven su propio árbol de procesos, su placa eth0, su sistema de archivos raíz y su lista de usuarios. Para ellos es una máquina; para el host, son procesos con etiquetas.

El punto delicado es el usuario root. En un contenedor no privilegiado, el namespace de usuarios traduce cada uid: el 0 de adentro es el 100000 del host, el 1 es el 100001, y así 65536 usuarios. Esa tabla es la que muestra /proc/self/uid_map. Si un proceso lograra escapar del contenedor, llegaría al host como el usuario 100000, sin permiso sobre /etc/pve ni sobre los discos de las VM.

En un contenedor privilegiado esa traducción no existe: el root de adentro es el root del host. Funciona igual mientras nada falle, pero un escape le da el servidor entero. Por eso el default es no privilegiado y los privilegiados se reservan para entornos de confianza.

Como el kernel es compartido, el contenedor solo puede correr Linux y depende de que el kernel del host le dé todo lo que necesita. Eso explica por qué Docker o un software exigente suelen estar mejor en una VM.
""",
  [{"file": "6-t1.svg", "after": "sin permiso sobre /etc/pve ni sobre los discos de las VM.",
    "alt": "Animación en cuatro tiempos con un contenedor, el kernel del host compartido y los archivos del host, cuyo dueño es root. 1: dentro del contenedor 300 un proceso corre como root, uid 0. 2: en un contenedor no privilegiado, el kernel lo traduce con el uid_map a uid 100000. 3: si ese proceso intentara tocar archivos del host como /etc/pve o discos de otras VM, recibe permiso denegado y el host queda a salvo. 4: en un contenedor privilegiado no hay mapeo, el uid 0 de adentro es el root del host y, si el proceso escapara, tendría acceso a todo.",
    "caption": "Con uid_map, el root de adentro llega al host sin poder; sin mapeo, llega como root."}],
  S("Crear un contenedor Debian no privilegiado",
    "Actualiza la lista de plantillas, baja la de Debian si falta y crea el contenedor no privilegiado si el CTID está libre. Al final confirma unprivileged: 1.",
    [("CTID", "300", "ID del contenedor"), ("HOSTNAME", "ct-prueba", "Nombre del contenedor"),
     ("DISTRO", "debian-13-standard", "Comienzo del nombre de la plantilla"), ("CLAVE", "Ejemplo.Cambiar.2026", "Clave de root de ejemplo: cambiala")],
    """# IES Training - Proxmox VE - Contenedor sin privilegios
# Correlo como root en el host. No pisa un CTID existente.
(
CTID="{{CTID}}"; NOMBRE="{{HOSTNAME}}"; DISTRO="{{DISTRO}}"; CLAVE="{{CLAVE}}"
pveam update
PLANTILLA=$(pveam available --section system | grep -o "$DISTRO[^ ]*" | tail -1)
test -n "$PLANTILLA" || { echo "No encontre una plantilla que empiece con $DISTRO"; exit 1; }
echo "Plantilla: $PLANTILLA"
if [ -e /var/lib/vz/template/cache/$PLANTILLA ]; then
  echo "Ya estaba bajada en local"
else
  pveam download local $PLANTILLA
fi
if pct config $CTID >/dev/null 2>&1; then
  echo "Ya existe el CT $CTID: no lo creo de nuevo"
else
  pct create $CTID local:vztmpl/$PLANTILLA --hostname $NOMBRE --unprivileged 1 --memory 512 --rootfs local-lvm:8 --net0 name=eth0,bridge=vmbr0,ip=dhcp --password "$CLAVE"
  pct start $CTID
fi
pct config $CTID | grep unprivileged
echo "Listo: CT $CTID. Entra con pct enter $CTID y mira cat /proc/self/uid_map"
)""",
    ["Cambiá la clave de ejemplo: después de entrar, passwd adentro del contenedor.",
     "Si pct config no muestra unprivileged: 1, el contenedor ya existía como privilegiado: el script no lo cambia."]))

# =====================================================================================  7
L("7",
  {"file": "7.svg", "alt": "A la izquierda, el disco del host local-lvm con la VM 100 en producción y un snapshot de la VM 100 en el mismo disco y el mismo pool; en rojo, si este disco muere se pierden la VM y su snapshot juntos. Una flecha vzdump lleva a otro almacenamiento, en verde: local, NFS o Proxmox Backup Server, con el archivo vzdump-qemu-100-fecha.vma.zst, copia completa de configuración y discos, que sobrevive si el disco de la VM muere. De ahí, un restore de prueba a la VM 900, nunca encima de la VM 100. Notas: el snapshot sirve para deshacer un cambio; un backup cuenta cuando lo restauraste en una VM nueva y arrancó.",
   "caption": "El snapshot vive con el disco; el backup, en otro lado, y cuenta cuando se restaura."},
  [{"file": "7-paso1.svg", "step": 1, "after": "Backup de la VM de prueba (ID 100)",
    "alt": "Las partes del comando: vzdump 100 es la VM a respaldar; mode snapshot, sin apagarla y con el agente que congela el disco; compress zstd, compresión rápida; storage local, destino /var/lib/vz/dump. Lo que aparece en esa carpeta, separado en partes: vzdump como prefijo, qemu para VM o lxc para contenedor, 100 el VMID, la fecha y hora, vma el formato y zst la compresión. Nota: en modo snapshot la VM sigue andando; el modo stop la apaga un momento y da la máxima consistencia.",
    "caption": "Qué le pedís a vzdump y cómo se lee el nombre del archivo que deja."},
   {"file": "7-paso3.svg", "step": 3, "after": "Antes de arrancar, desconectá la placa",
    "alt": "El bridge vmbr0, la red del cliente, con dos VM. La VM 100 original, 10.10.10.100, en producción, conectada en verde. La VM 900 restaurada, con la misma IP y la misma MAC adentro, con la conexión cortada en rojo y la etiqueta link_down=1. Antes de arrancarla: qm set 900 --net0 virtio,bridge=vmbr0,link_down=1 y qm start 900. Nota: si arranca conectada, la copia pelea la IP con la original; se prueba por la consola y se anota cuánto tardó.",
    "caption": "La copia arranca con el cable virtual desenchufado para no pelear con la original."}],
  [C("vzdump",
     "Es la herramienta de backup de Proxmox VE. Guarda la configuración y todos los discos de una VM o contenedor en un solo archivo, siempre completo, para poder reconstruirla en cualquier nodo.",
     "Se corre a mano (`vzdump 100 --mode snapshot --compress zstd --storage local`) o programado en Datacenter, Backup. El archivo queda en el almacenamiento elegido: local, NFS, CIFS o un PBS. Modo snapshot para no cortar el servicio, stop cuando la consistencia manda.",
     "Antes de actualizar el software de una central de monitoreo en una VM, corrés un vzdump a mano a un NFS. Si la actualización sale mal, tenés de dónde volver aunque el disco del host falle."),
   C("Modo snapshot y modo stop",
     "Copiar el disco de una VM que está escribiendo puede dejar archivos a medio guardar. Los modos son distintas formas de resolverlo: stop apaga la VM un instante y garantiza consistencia; snapshot la deja corriendo y congela el estado al inicio del backup.",
     "En modo snapshot, Proxmox usa su live backup: QEMU copia los bloques mientras la VM sigue, y si la VM quiere escribir uno que falta copiar, primero manda el viejo al backup. Con el guest agent, además, congela el sistema de archivos un instante al empezar. Suspend existe por compatibilidad y no se recomienda.",
     "Para el servidor de archivos de una inmobiliaria usás snapshot con agente cada noche. Para la base de datos de facturación, una vez por semana un stop en la madrugada, acordado con el cliente."),
   C("Snapshot no es backup",
     "Un snapshot de VM sirve para deshacer un cambio: antes de un upgrade, lo sacás, y si sale mal, rollback en minutos. Pero vive en el mismo pool que el disco: si ese disco o ese pool se pierde, se pierde con él.",
     "Snapshots para cambios puntuales, de vida corta. Backups con vzdump o PBS en otro almacenamiento, programados y probados. No acumular snapshots viejos: ocupan espacio y hacen más lentas algunas operaciones.",
     "Imaginá un cliente en Las Piedras que pierde el RAID de su servidor con tres snapshots de cada VM y ningún backup: no recupera nada, porque los snapshots estaban en ese RAID. El plan correcto es backup nocturno a otro equipo y snapshots solo para los cambios."),
   C("Restore de prueba",
     "Un backup que nunca se restauró es una suposición. Restaurarlo prueba que el archivo está sano, que la VM arranca y cuánto tarda, que es lo que el cliente va a preguntar el día que lo necesite.",
     "Siempre a un VMID nuevo (`qmrestore archivo 900`), nunca encima de la VM en producción, porque restaurar sobre el mismo ID borra sus discos. Antes de arrancar, placa con `link_down=1` para que no choque con la original. Si son muchas VM, muestras al azar cada tanto.",
     "Una vez por mes restaurás una VM al azar de cada cliente con contrato, anotás el tiempo y la borrás. Cuando un servidor se cae, ya sabés que el restore anda y cuánto demora.")],
  """
### Un poco de historia

vzdump nació en la época en que Proxmox usaba OpenVZ para contenedores, y de ahí el nombre. Con los años pasó a respaldar también las VM de KVM. Para hacerlo sin apagar la VM y en cualquier almacenamiento, Proxmox desarrolló su propio live backup dentro de QEMU: no necesita que el disco esté en un almacenamiento con snapshots.

Desde el principio los backups de Proxmox VE son completos: configuración y datos en un archivo. Lo incremental y la deduplicación llegaron con Proxmox Backup Server, que es tema de la próxima lección.

### Cómo funciona

En modo snapshot, todo empieza con un instante de quietud. Si la VM tiene el guest agent activado y corriendo, Proxmox le pide congelar el sistema de archivos: las escrituras quedan en pausa para no copiar algo a medio guardar. En Windows, eso se hace con VSS.

Enseguida QEMU instala un filtro copy-before-write sobre el disco y descongela. La VM sigue trabajando y el backup empieza a leer los bloques en orden. Si la VM quiere escribir un bloque que el backup todavía no copió, el filtro manda primero el contenido viejo al destino y después deja pasar la escritura. Así, el archivo final es la foto exacta del instante en que empezó, aunque la VM nunca se haya detenido. El costo es que esas escrituras esperan a que el destino reciba el bloque viejo; si el destino es lento, la VM lo nota.

En modo stop, la VM se apaga ordenadamente, arranca el backup y la VM vuelve a prender: el corte es breve y la consistencia, máxima.

Un snapshot de VM es otra cosa: queda dentro del mismo pool, sirve para volver atrás y no protege contra la pérdida del disco. El backup va a otro almacenamiento. Y cuenta recién cuando se restauró a un ID nuevo, con la placa desconectada, y la VM arrancó con sus datos.
""",
  [{"file": "7-t1.svg", "after": "aunque la VM nunca se haya detenido.",
    "alt": "Animación en cuatro tiempos de un backup de vzdump en modo snapshot de la VM 100, con ocho bloques de disco y un archivo de backup vacío. 1: al arrancar, el guest agent congela el sistema de archivos un instante y las escrituras quedan en pausa. 2: QEMU instala un filtro copy-before-write, descongela y la VM sigue corriendo mientras el backup copia los bloques 1 a 4. 3: la VM quiere escribir el bloque 6, que todavía no se copió: primero el bloque 6 viejo va al backup y recién después se escribe el dato nuevo. 4: se copian los bloques que faltan y el archivo queda como la foto del instante en que arrancó, con el bloque 6 viejo.",
    "caption": "Copy-before-write: lo viejo sale primero, así el backup es la foto del inicio."}],
  S("Backup de una VM y restore de prueba a un ID nuevo",
    "Hace un vzdump en modo snapshot a local, restaura el archivo más nuevo a un VMID libre con la placa desconectada, la arranca y mide cuánto tardó el restore.",
    [("VMID", "100", "VM a respaldar"), ("DESTINO", "900", "VMID libre para el restore de prueba")],
    """# IES Training - Proxmox VE - Backup que restaura
# Correlo como root en el host. Nunca restaura encima de una VM existente.
(
VMID="{{VMID}}"; DESTINO="{{DESTINO}}"
if [ -e /etc/pve/qemu-server/$DESTINO.conf ]; then
  echo "Ya existe la VM $DESTINO: no restauro encima (borraria sus discos). Elegi otro ID."
  exit 1
fi
vzdump $VMID --mode snapshot --compress zstd --storage local
ARCHIVO=$(ls -t /var/lib/vz/dump/vzdump-qemu-$VMID-*.vma.zst | head -1)
test -n "$ARCHIVO" || { echo "No encontre el backup de la VM $VMID"; exit 1; }
echo "Restauro $ARCHIVO en la VM $DESTINO"
INICIO=$(date +%s)
qmrestore "$ARCHIVO" $DESTINO
echo "Restore en $(( $(date +%s) - INICIO )) segundos: anotalo en la ficha"
# Placa desconectada: la copia tiene la misma IP que la original
qm set $DESTINO --net0 virtio,bridge=vmbr0,link_down=1
qm start $DESTINO
echo "Listo: VM $DESTINO arrancada sin red. Revisa por la consola."
echo "Al terminar: qm stop $DESTINO && qm destroy $DESTINO"
)""",
    ["El script usa el almacenamiento local (/var/lib/vz/dump). Para otro destino, cambiá --storage y la carpeta donde busca el archivo.",
     "qm set --net0 reemplaza la placa de la copia por una VirtIO en vmbr0; si la original usa otro bridge o VLAN, ajustalo.",
     "El borrado final queda como comando sugerido: hacelo vos cuando terminaste de revisar."]))

# =====================================================================================  8
L("8",
  {"file": "8.svg", "alt": "Línea de tiempo de una noche en Proxmox Backup Server, horario de ejemplo de la guía de Hake Hardware: 21:30 prune, que borra el índice de los backups que la retención no guarda y todavía no libera espacio; 22:00 backup, Proxmox VE manda los backups nuevos; 01:00 verify, que relee y compara checksums y, si un ransomware cifra backups, falla y avisa; domingo 02:00 garbage collection, que borra los trozos que ya nadie usa con un día de gracia y ahí libera espacio. Nota: retención generosa al principio y una copia fuera del sitio con sync job, regla 3-2-1. Abajo, en verde: usuario con rol DatastoreBackup, que puede crear backups pero no borrarlos; si alguien toma el host Proxmox VE, no puede borrar las copias.",
   "caption": "Prune elige, backup escribe, verify controla y GC libera, cada uno a su hora."},
  [{"file": "8-paso3.svg", "step": 3, "after": "Usuario de backup con token",
    "alt": "Cadena de tres pasos con proxmox-backup-manager en el PBS: usuario backup@pbs con user create, token backup@pbs!pve con user generate-token, y permiso DatastoreBackup con acl update sobre /datastore/main. Lo que puede hacer Proxmox VE con ese token: crear backups nuevos y leerlos para restaurar, con tilde verde; borrar backups y cambiar la retención, con cruz roja. Notas: PBS muestra el secreto del token una sola vez y conviene guardarlo en el gestor de contraseñas; hay guías que conectan con root@pam, que funciona, pero un host tomado podría borrar todo el datastore.",
    "caption": "Usuario, token y rol: Proxmox VE escribe backups pero no puede borrarlos."},
   {"file": "8-paso4.svg", "step": 4, "after": "En Proxmox VE: **Datacenter",
    "alt": "Diálogo Add: Proxmox Backup Server en Datacenter, Storage, Add, con ID pbs-main, Server con la IP del PBS, Username backup@pbs!pve resaltado, Password con el secreto del token, Datastore main y Fingerprint del dashboard. Notas: Username lleva el token completo, usuario, signo de exclamación y nombre del token; en Password va el secreto que PBS mostró una vez, no la clave del usuario; el fingerprint se copia del dashboard del PBS, web en el puerto 8007. Después, un backup de prueba y revisar en PBS, Content, que aparezca.",
    "caption": "En Username va el token completo y en Password, su secreto."}],
  [C("Proxmox Backup Server",
     "vzdump a un disco copia cada VM entera cada vez, y el espacio se va rápido. PBS es un servidor de backups pensado para Proxmox: guarda solo lo que cambió, deduplica entre backups y entre VM, verifica la integridad y permite restaurar archivos sueltos.",
     "Se instala en un equipo aparte (web en el puerto 8007), con un datastore en discos separados del sistema. En Proxmox VE se agrega como un almacenamiento más y los jobs de backup apuntan ahí. Proxmox recomienda SSD para el datastore, o un special device si son discos rotativos.",
     "Para un cliente con dos hosts en Montevideo, IES instala un PBS en un mini servidor con dos discos en espejo. Treinta noches de backup ocupan una fracción de lo que ocuparían treinta vzdump completos."),
   C("Prune, garbage collection y verify",
     "Son tres tareas de mantenimiento distintas que a menudo se confunden. Prune decide qué backups quedan según la retención; garbage collection borra los trozos de datos que ya no usa ningún backup y libera el espacio; verify relee los datos y compara checksums para detectar corrupción.",
     "Se programan el mismo día que se crea el datastore: prune diario con la retención, GC semanal para empezar (diario si el datastore se llena rápido) y verify diario de lo nuevo con reverificación al menos mensual de todo. Prune solo borra índices: sin GC, el disco no baja.",
     "Un cliente llama porque su PBS está al 95 %. Tenía prune pero no GC: los backups viejos ya no figuraban, pero sus trozos seguían en disco. Programás la GC y el domingo siguiente baja al 60 %."),
   C("Rol DatastoreBackup",
     "Si Proxmox VE se conecta al PBS con un usuario que puede borrar, un atacante que tome el host también puede borrar los backups, justo cuando más se necesitan. DatastoreBackup permite crear backups y leerlos, pero no borrarlos.",
     "Usuario dedicado (backup@pbs), un token de API para la conexión y el rol DatastoreBackup sobre /datastore/main. En Proxmox VE, Username es usuario!token y Password es el secreto del token, que PBS muestra una sola vez.",
     "Si un ransomware toma los hosts de una empresa de logística, puede cifrar las VM, pero con ese token no puede borrar los backups del PBS. La restauración sale de ahí."),
   C("Regla 3-2-1",
     "Un solo backup en un solo lugar falla junto con ese lugar: un incendio, un robo o un ransomware que llega a la red. La regla 3-2-1 pide tres copias, en dos medios distintos, con una fuera del sitio.",
     "En PBS, la copia fuera del sitio se hace con un sync job a otro PBS remoto, o a cinta. La retención conviene generosa al principio: siempre se puede achicar, pero no se recrean backups del pasado.",
     "El PBS principal del cliente está en su sala de servidores; un sync job nocturno copia el datastore al PBS de IES en otra ciudad. Si el edificio se pierde, los backups siguen.")],
  """
### Un poco de historia

Proxmox Backup Server salió en 2020 como un producto nuevo, escrito en Rust, para resolver lo que vzdump no podía: backups incrementales, deduplicación y verificación. Está integrado con Proxmox VE como un almacenamiento más. La versión 4.0 salió en agosto de 2025, junto con Proxmox VE 9, sobre la misma base Debian 13, y trajo soporte S3 en preview.

### Cómo funciona

PBS no guarda cada backup como un archivo entero. Parte los discos en trozos, les calcula un hash y guarda cada trozo una sola vez en el directorio .chunks del datastore. Cada backup es en realidad un índice: la lista de trozos que lo forman. El backup del martes reutiliza todos los trozos que no cambiaron desde el lunes y solo sube los nuevos. Esa deduplicación funciona también entre VM parecidas, y es la razón por la que treinta backups no ocupan treinta veces el disco.

Ese diseño explica las tres tareas de mantenimiento. Prune aplica la retención: borra los índices de los backups que sobran, pero no toca los trozos, porque otros backups pueden estar usándolos. Garbage collection recorre todos los índices, marca los trozos en uso y borra los que nadie usa. Para no borrar algo que un backup en curso está por referenciar, respeta un período de gracia de 24 horas y 5 minutos. Recién ahí baja el uso del disco.

Verify relee los trozos y compara su hash. Si un disco se degrada o un ransomware cifra backups existentes, los hashes dejan de coincidir y el job falla: también sirve de alarma. Como PBS no reescribe trozos existentes, un host comprometido tampoco puede modificar backups viejos.

Del lado de los permisos, el token de Proxmox VE con DatastoreBackup puede escribir y leer, pero no borrar. La copia fuera del sitio se completa con un sync job a otro PBS.
""",
  [{"file": "8-t1.svg", "after": "Recién ahí baja el uso del disco.",
    "alt": "Animación en cuatro tiempos de un datastore de Proxmox Backup Server. 1: el backup del lunes parte el disco en los trozos a, b, c y d y los guarda; su índice apunta a los cuatro. 2: el backup del martes solo sube el trozo e, que es nuevo, y reutiliza a, b y c: eso es la deduplicación. 3: prune borra el índice del lunes, pero los trozos siguen en disco y d queda sin dueño. 4: la garbage collection, pasado el plazo de gracia de 24 horas y 5 minutos, borra d, que ya no usa ningún índice, y recién ahí se libera espacio.",
    "caption": "Índices que comparten trozos: prune borra índices, GC borra trozos huérfanos."}],
  S("Programar prune, GC y verify y crear el usuario de backup",
    "En el PBS: crea el prune job con la retención del ejemplo oficial, programa la GC semanal y el verify diario, y crea el usuario con token y rol DatastoreBackup. Si algo ya existía, avisa y sigue.",
    [("STORE", "main", "Nombre del datastore"), ("USUARIO", "backup@pbs", "Usuario dedicado para Proxmox VE"),
     ("TOKEN", "pve", "Nombre del token"), ("CLAVE", "Ejemplo.Cambiar.2026", "Clave de ejemplo del usuario: cambiala")],
    """# IES Training - Proxmox VE - PBS sin sorpresas
# Correlo como root en el Proxmox Backup Server, no en el host de VMs.
(
STORE="{{STORE}}"; USUARIO="{{USUARIO}}"; TOKEN="{{TOKEN}}"; CLAVE="{{CLAVE}}"
# Retencion de ejemplo de la documentacion: ajustala al cliente
proxmox-backup-manager prune-job create diario --store $STORE --schedule '21:30' --keep-last 3 --keep-daily 13 --keep-weekly 8 --keep-monthly 11 || echo "El prune job ya existia"
proxmox-backup-manager datastore update $STORE --gc-schedule 'sun 02:00'
proxmox-backup-manager verify-job create verif-$STORE --store $STORE --schedule '01:00' --ignore-verified true --outdated-after 30 || echo "El verify job ya existia"
proxmox-backup-manager user create $USUARIO --password "$CLAVE" || echo "El usuario ya existia"
echo "== Token: el secreto aparece una sola vez, guardalo ya =="
proxmox-backup-manager user generate-token $USUARIO $TOKEN || echo "El token ya existia: si perdiste el secreto, genera uno con otro nombre"
# El signo de admiracion va entre comillas simples para que la consola no lo interprete
proxmox-backup-manager acl update /datastore/$STORE DatastoreBackup --auth-id "$USUARIO"'!'"$TOKEN"
echo "Listo: prune 21:30, GC domingos 02:00, verify 01:00 y $USUARIO con DatastoreBackup."
echo "En Proxmox VE: Datacenter > Storage > Add > Proxmox Backup Server, con el token y el fingerprint."
)""",
    ["Cambiá la clave de ejemplo. El usuario no la usa para los backups: la conexión va con el token.",
     "Probá la retención en el Prune Simulator de la documentación antes de dejarla en un cliente.",
     "La copia fuera del sitio (sync job a otro PBS) no la hace este script."]))
