"""Manifest Proxmox, lecciones 1 a 4 (lo arma manifest_pmx.py)."""
from _mbase import L, C, S

# =====================================================================================  1
L("1",
  {"file": "1.svg", "alt": "Tres tarjetas, una por repositorio de Proxmox VE. pve-enterprise, en verde: con suscripción, para producción y soporte, paquetes más validados, viene habilitado de fábrica; sin suscripción da error 401. pve-no-subscription, en ámbar: gratis y sin clave, para pruebas y uso no productivo, paquetes menos validados; en producción decide el cliente, con backups probados. pve-test, en gris: lo que viene, para desarrolladores, nunca en un cliente. Abajo, el archivo /etc/apt/sources.list.d/proxmox.sources en formato deb822 con Types deb, URIs http://download.proxmox.com/debian/pve, Suites trixie y Components pve-no-subscription; una nota recuerda que siempre se necesitan además los repositorios base de Debian, y que para actualizar se usa apt full-upgrade.",
   "caption": "Tres repositorios posibles, uno solo habilitado, y siempre apt full-upgrade."},
  [{"file": "1-paso3.svg", "step": 3, "after": "Si no hay suscripción: en",
    "alt": "Ventana de Node, Updates, Repositories del nodo pve1 con tres archivos: pve-enterprise.sources con el componente pve-enterprise en estado Disabled, proxmox.sources con pve-no-subscription en estado Enabled y resaltado, y debian.sources con main en Enabled. A la derecha, dos acciones: a, seleccionar pve-enterprise y tocar Disable; b, Add No-Subscription, que queda en proxmox.sources. Abajo, cómo queda deshabilitado el archivo: Components pve-enterprise y la línea Enabled: no. Nota: sin clave de suscripción, enterprise responde 401 Unauthorized en cada apt update.",
    "caption": "Disable en enterprise y Add en no-subscription: los dos pasos, en ese orden."}],
  [C("Repositorio de paquetes",
     "Proxmox VE es Debian con paquetes propios, y esos paquetes salen de un repositorio. Proxmox ofrece tres: enterprise, más probado y para clientes con suscripción; no-subscription, gratis y pensado para pruebas; y test, para desarrolladores. Elegir uno a conciencia evita el error del primer update y deja claro qué nivel de prueba tiene lo que instalás.",
     "Se mira y se cambia en Node, Updates, Repositories, o en los archivos .sources de /etc/apt/sources.list.d/. Conviene que quede un solo repositorio de Proxmox habilitado, además de los de Debian. Si el cliente paga suscripción, se queda en enterprise; si no, se deshabilita enterprise y se agrega no-subscription, sabiendo que Proxmox no lo recomienda para producción.",
     "Instalás un Proxmox en una clínica de Pocitos sin suscripción y el primer apt update termina en 401 Unauthorized. No es un problema de red: enterprise pide clave. Lo deshabilitás, sumás no-subscription y anotás en la ficha del cliente que la decisión fue suya, con backups probados."),
   C("apt full-upgrade",
     "Una actualización de Proxmox a veces trae paquetes que piden instalar otros nuevos o quitar alguno viejo. apt upgrade no puede quitar paquetes, así que deja retenido lo que necesita ese cambio y el host queda a medio actualizar. full-upgrade resuelve las dependencias completas.",
     "Siempre en dos pasos: apt update para bajar las listas y apt full-upgrade para instalar. El botón Upgrade de la GUI hace lo mismo. Después de una actualización con kernel nuevo, se reinicia en una ventana acordada con el cliente.",
     "Un técnico corre apt upgrade en un host de un estudio contable y la web empieza a dar errores raros: la mitad de los paquetes de Proxmox quedaron en una versión y la otra mitad en otra. Un `apt full-upgrade` lo deja coherente."),
   C("Formato deb822",
     "Desde Debian 13, apt se queja del formato viejo de una línea en archivos .list. El formato deb822 escribe cada repositorio como un bloque de campos con nombre (Types, URIs, Suites, Components), más fácil de leer y de deshabilitar sin borrar.",
     "Los repositorios van en archivos .sources dentro de /etc/apt/sources.list.d/. Para apagar uno se agrega la línea `Enabled: no` en su bloque. Si un host viene de una versión vieja con archivos .list, `apt modernize-sources` migra la mayoría.",
     "Recibís un host que alguien actualizó de la 8 a la 9 y apt update muestra advertencias de formato. Corrés `apt modernize-sources`, revisás que queden los .sources de Debian y de Proxmox, y las advertencias desaparecen.")],
  """
### Un poco de historia

Proxmox VE nació en Viena: el proyecto empezó en 2007 y la primera versión estable salió en 2008, con KVM para máquinas virtuales y OpenVZ para contenedores. Desde el principio se apoyó en Debian, y eso explica buena parte de su mantenimiento: los paquetes se instalan y actualizan con apt, como en cualquier Debian, pero desde repositorios propios de Proxmox.

La versión 9.0 salió el 5 de agosto de 2025 sobre Debian 13 Trixie, y la rama vigente es la 9.2, de mayo de 2026. La 8.4 tuvo un año de solapamiento con parches de seguridad hasta agosto de 2026: hoy un host en 8 ya no recibe correcciones. Con Debian 13 llegó otro cambio que se nota en el primer día: los repositorios pasan al formato deb822, en archivos .sources.

### Cómo funciona

Cuando corrés `apt update`, el host le pide a cada repositorio habilitado la lista de paquetes que tiene. Los de Debian traen el sistema base. Los de Proxmox traen pve-manager, el kernel, QEMU, LXC y el resto de la plataforma. El repositorio enterprise exige la clave de suscripción del host: sin clave, contesta 401 Unauthorized y apt marca error.

El repositorio no-subscription tiene los mismos paquetes, publicados antes y con menos validación. Por eso Proxmox lo indica para pruebas y uso no productivo. El de test es todavía más temprano. La regla práctica es tener uno solo de Proxmox habilitado, elegido a propósito, y que la decisión quede anotada.

Después viene la instalación. `apt upgrade` actualiza lo que puede sin quitar nada; si un paquete nuevo necesita reemplazar a otro, lo deja retenido. `apt full-upgrade` instala lo nuevo y quita lo que sobra, y deja el host en una versión coherente. Es lo que hace también el botón Upgrade del nodo.

Para saber dónde estás parado, `pveversion -v` muestra la versión real de cada componente: pve-manager 9.2.3 dentro de la rama 9.2, por ejemplo. Ese dato va a la ficha del cliente antes de tocar nada.
""",
  [{"file": "1-t1.svg", "after": "contesta 401 Unauthorized y apt marca error",
    "alt": "Animación en cuatro tiempos. 1: el host pve1 corre apt update contra el repositorio pve-enterprise sin clave de suscripción y recibe 401 Unauthorized. 2: con enterprise deshabilitado (Enabled: no), responde pve-no-subscription y las listas de paquetes bajan bien. 3: con apt upgrade, un paquete A que en su versión 9.2 necesita instalar B y reemplazar a C queda retenido en 9.1. 4: con apt full-upgrade, A pasa a 9.2, B se instala y C se quita. Las dependencias son un ejemplo genérico.",
    "caption": "Quién responde al apt update, y por qué full-upgrade y no upgrade."}],
  S("Revisar repositorios y actualizar con full-upgrade",
    "Muestra la versión, los repositorios con su estado y migra archivos .list viejos a .sources. Corre apt update y, solo si lo pedís en la variable, apt full-upgrade.",
    [("ACTUALIZAR", "no", "si para correr apt full-upgrade al final")],
    """# IES Training - Proxmox VE - Repos en orden
# Correlo como root en el host, por SSH o IPMI. Probalo primero en un host de banco.
(
ACTUALIZAR="{{ACTUALIZAR}}"
echo "== Version =="
pveversion -v | head -3
echo "== Archivos de repositorio =="
ls /etc/apt/sources.list.d/
# Formato viejo de una linea: apt modernize-sources lo pasa a .sources (puede pedir confirmacion)
if ls /etc/apt/sources.list.d/*.list >/dev/null 2>&1; then
  echo "Hay archivos .list viejos: los migro"
  apt modernize-sources
fi
echo "== Componentes y estado de cada .sources =="
grep -H -E "^(Components|Enabled):" /etc/apt/sources.list.d/*.sources
echo "== apt update =="
if apt update; then
  echo "OK: apt update sin errores"
else
  echo "Ojo: apt update con errores. Si dice 401, enterprise sigue habilitado sin suscripcion."
  exit 1
fi
if [ "$ACTUALIZAR" = "si" ]; then
  apt full-upgrade
else
  echo "No actualizo. Cuando quieras: apt full-upgrade (nunca apt upgrade a secas)."
fi
echo "Listo: repositorios revisados. Verifica con: pveversion -v | head -3"
)""",
    ["Tiene que quedar un solo componente de Proxmox sin Enabled: no (pve-enterprise o pve-no-subscription).",
     "El script no habilita ni deshabilita repositorios: eso se decide con el cliente y se hace en Node, Updates, Repositories.",
     "apt full-upgrade pide confirmación; si trae kernel nuevo, reiniciá en una ventana acordada."]))

# =====================================================================================  2
L("2",
  {"file": "2.svg", "alt": "Pila de la red del host, de abajo hacia arriba: un switch con port-channel en trunk que permite las VLAN 10 y 20; las placas físicas eno1 y eno2; encima bond0, dos placas como una, en 802.3ad (LACP) si el switch lo soporta; encima vmbr0, el switch virtual, VLAN aware con bridge-vids 2-4094; y arriba tres VM: VM 100 con tag 10 para cámaras, VM 101 con tag 20 para voz y VM 102 sin tag. Numerado a la derecha: 1 placas físicas, 2 bond encima, 3 bridge encima, 4 tag en cada VM. Notas: con VLAN aware un solo vmbr0 lleva todas las VLAN; el modo viejo crea un bridge por VLAN (vmbr0v10, vmbr0v20); balance-alb y balance-tlb no sirven con un bridge con VMs.",
   "caption": "Se arma de abajo hacia arriba: placas, bond, bridge y el tag en cada VM."},
  [{"file": "2-paso1.svg", "step": 1, "after": "En la web: **Node → System → Network**",
    "alt": "Diálogo Edit: Linux Bridge de vmbr0, en Node, System, Network, con IPv4 10.10.10.2/24, gateway 10.10.10.1, bridge ports eno1 y la fila VLAN aware tildada y resaltada. A la derecha, el flujo: la GUI escribe primero en /etc/network/interfaces.new, se toca Apply Configuration y recién ahí pasa a /etc/network/interfaces. Notas: editado a mano se aplica con ifreload -a; si la IP de gestión pasa a una VLAN tagueada, al aplicar desde lejos se corta, así que se hace con consola local o IPMI.",
    "caption": "Tildar VLAN aware queda en interfaces.new hasta Apply Configuration."},
   {"file": "2-paso4.svg", "step": 4, "after": "Arrancá la VM y en el host mirá el tag",
    "alt": "Salida de ejemplo de bridge vlan show con la VM 100 en tag 10: eno1 con VLAN 1 PVID Egress Untagged y 2-4094, vmbr0 con 1 PVID Egress Untagged y tap100i0 con 10 PVID Egress Untagged, resaltado. Explicaciones: eno1 lleva todas las VLAN etiquetadas hacia el switch; tap100i0 con PVID 10 mete en la VLAN 10 lo que sale de la VM, que no ve tags; Egress Untagged significa que al entregarle a la VM el bridge saca la etiqueta. tap100i0 es la placa net0 de la VM 100. Qué buscar: si tap100i0 no aparece, la VM está apagada; si aparece con 1 en vez de 10, el tag no quedó en la placa.",
    "caption": "Cada puerto del bridge con sus VLAN: la placa física, todas; la VM, la suya."}],
  [C("Bridge VLAN-aware",
     "Un bridge es un switch virtual dentro del host: une las placas de las VM con la placa física. Antes, para separar VLAN se creaba un bridge por VLAN, y la configuración crecía con cada red nueva del cliente. Con VLAN aware, un solo vmbr0 maneja todas.",
     "Se tilda VLAN aware en vmbr0 (Node, System, Network) y se aplica. Después, en cada VM, Hardware, Network Device, VLAN Tag: el número de su VLAN. En el archivo queda `bridge-vlan-aware yes` y `bridge-vids 2-4094`. El puerto del switch que va al host tiene que estar en trunk con esas VLAN permitidas.",
     "En un edificio de oficinas en Ciudad Vieja, el servidor corre el VMS en la VLAN 10 de cámaras y la central telefónica en la VLAN 20. Un solo vmbr0 VLAN aware, tag 10 en una VM y tag 20 en la otra, y el switch en trunk."),
   C("Bond",
     "Juntar dos placas físicas en una lógica da redundancia (si se corta un cable, sigue la otra) y, con LACP, más ancho de banda total. Es la base de un host que no se queda sin red por un patch cord flojo.",
     "Se crea el bond con las placas como esclavas, en modo 802.3ad si el switch soporta LACP, o active-backup si no. Encima va el bridge, con bridge-ports bond0. En un stack, conviene repartir los miembros del port-channel entre dos switches. Los modos balance-alb y balance-tlb no sirven con VM en el bridge.",
     "Un servidor de un supermercado en Maldonado tiene dos placas: armás bond0 en 802.3ad, cada cable a un switch distinto del stack y el port-channel en trunk. Desenchufás uno de prueba y las VM siguen con red."),
   C("Apply Configuration",
     "Un error en la red del host puede dejarlo inaccesible. Por eso Proxmox no escribe directo: guarda los cambios de la GUI en un archivo aparte y los aplica todos juntos cuando vos lo pedís.",
     "Los cambios quedan en /etc/network/interfaces.new y se aplican con Apply Configuration, que usa ifupdown2. Si editaste /etc/network/interfaces a mano, el equivalente es `ifreload -a`. Mover la IP de gestión a otra VLAN se hace con consola local o IPMI, no desde una sesión remota.",
     "Desde la oficina tocás la red de un host en Colonia y, antes de aplicar, revisás el diff. Como la gestión no cambia de VLAN, aplicás sin miedo; si cambiara, coordinás con alguien en sitio.")],
  """
### Un poco de historia

Las VLAN se estandarizaron con IEEE 802.1Q en 1998, y la agregación de enlaces con LACP llegó con 802.3ad en 2000. Linux tiene desde hace mucho un bridge en el kernel que funciona como un switch por software, y Proxmox lo usa desde sus primeras versiones como vmbr0.

Durante años, la forma de dar VLAN a las VM fue crear una subinterfaz y un bridge por cada VLAN: eno1.10 con vmbr0v10, eno1.20 con vmbr0v20. Funciona, pero cada red nueva del cliente era otro bridge. El modo VLAN aware llevó el filtrado de VLAN al propio bridge, y hoy es la forma recomendada. Para aplicar cambios sin reiniciar, Proxmox usa ifupdown2, una reescritura de las herramientas clásicas de red de Debian.

### Cómo funciona

La red del host se arma en capas. Abajo están las placas físicas. Si hay dos o más, se agrupan en un bond, que el resto del sistema ve como una sola placa. Encima va vmbr0, el bridge, y a ese bridge se conectan las placas virtuales de las VM, cada una como un puerto llamado tap, con el VMID en el nombre: tap100i0 es la placa net0 de la VM 100.

Con VLAN aware, cada puerto del bridge tiene su lista de VLAN. La VM no sabe nada de VLAN: manda tramas comunes. El puerto tap100i0 tiene PVID 10, así que todo lo que entra por ahí queda en la VLAN 10. Hacia la placa física, el bridge deja pasar de 2 a 4094 con etiqueta, y el switch las recibe en un puerto trunk.

De vuelta pasa lo mismo al revés: una trama con tag 20 que llega del switch solo se entrega a los puertos que tienen la VLAN 20, y se entrega sin etiqueta. La VM 100, en la VLAN 10, nunca la ve. `bridge vlan show` muestra esa tabla y es la forma más rápida de confirmar que el tag quedó donde tiene que estar.

Los cambios hechos en la GUI esperan en interfaces.new hasta Apply Configuration. Así, un error a medio escribir no deja al nodo sin red.
""",
  [{"file": "2-t1.svg", "after": "nunca la ve. `bridge vlan show` muestra esa tabla",
    "alt": "Animación en cuatro tiempos sobre un bridge vmbr0 VLAN aware con dos VM. 1: la VM 100 manda una trama común, sin etiqueta, hacia su puerto tap100i0. 2: ese puerto tiene PVID 10, así que dentro del bridge la trama queda en la VLAN 10. 3: sale por bond0, que lleva las VLAN 2 a 4094 etiquetadas, hacia el puerto trunk del switch con el tag 10. 4: una trama con tag 20 que vuelve del switch solo se entrega por tap101i0 a la VM 101, ya sin etiqueta; la VM 100 no la ve.",
    "caption": "La VM manda sin tag; el bridge etiqueta, el trunk transporta y la vuelta se filtra por VLAN."}],
  S("Verificar el bridge VLAN-aware y el tag de una VM",
    "No cambia la red: revisa que el bridge sea VLAN aware, avisa si hay cambios sin aplicar y confirma que el puerto de la VM esté en su VLAN.",
    [("BRIDGE", "vmbr0", "Bridge a revisar"), ("VMID", "100", "VM de prueba, encendida"), ("VLAN", "10", "VLAN que tiene que tener su placa net0")],
    """# IES Training - Proxmox VE - Puente VLAN-aware
# Solo lee: no toca /etc/network/interfaces. Correlo como root en el host.
(
BRIDGE="{{BRIDGE}}"
VMID="{{VMID}}"
VLAN="{{VLAN}}"
echo "== $BRIDGE en /etc/network/interfaces =="
grep -A9 "^iface $BRIDGE" /etc/network/interfaces
if grep -A9 "^iface $BRIDGE" /etc/network/interfaces | grep -q "bridge-vlan-aware yes"; then
  echo "OK: $BRIDGE es VLAN aware"
else
  echo "Ojo: $BRIDGE no es VLAN aware. Tildalo en Node > System > Network y Apply Configuration."
fi
if [ -e /etc/network/interfaces.new ]; then
  echo "Ojo: hay cambios esperando en interfaces.new. Falta Apply Configuration."
fi
echo "== Placas de la VM $VMID =="
grep "^net" /etc/pve/qemu-server/$VMID.conf
echo "== Puerto tap${VMID}i0 en el bridge =="
bridge vlan show dev tap${VMID}i0
if bridge vlan show dev tap${VMID}i0 | grep -Eq "(^|[[:space:]])$VLAN PVID"; then
  echo "OK: la VM $VMID entra al bridge en la VLAN $VLAN"
else
  echo "Ojo: tap${VMID}i0 no tiene PVID $VLAN. VM apagada o sin VLAN Tag en net0."
fi
echo "Listo: revisado $BRIDGE y la VM $VMID. Falta el switch: puerto en trunk con la VLAN $VLAN."
)""",
    ["Si la VM está apagada, tap<VMID>i0 no existe y bridge vlan show da error: prendela y repetí.",
     "El script no cambia la red a propósito: un error remoto en la red del host te deja sin acceso."]))

# =====================================================================================  3
L("3",
  {"file": "3.svg", "alt": "Comparación en dos columnas. LVM-thin, local-lvm, instalando con ext4 o xfs: simple y rápido, snapshots y linked clones, ocupa solo lo escrito; como atención, sin integridad ni RAID propio; va bien con RAID por hardware, SSD de consumo o poca RAM. ZFS, local-zfs, instalando con ZFS: detecta y corrige corrupción, compresión y snapshots, RAID por software y replicación; como atención, pide RAM, ECC y discos directos; va bien con HBA o modo IT, SSD con PLP y RAM de sobra. Abajo, en rojo: nunca ZFS encima de una controladora RAID por hardware con caché, porque ZFS necesita ver cada disco. Nota: es lo más caro de cambiar después, se elige en el instalador.",
   "caption": "Cada uno tiene su servidor: el hardware decide entre LVM-thin y ZFS."},
  [{"file": "3-paso1.svg", "step": 1, "after": "Mirá qué almacenamientos tiene el nodo",
    "alt": "Salida de ejemplo de pvesm status con tamaños en KiB: local, tipo dir, activo, 11.76 por ciento usado; local-lvm, tipo lvmthin, activo, 7.36 por ciento usado. Debajo, qué es cada uno: local es un directorio que guarda archivos como ISO, plantillas de contenedor y backups de vzdump en /var/lib/vz; local-lvm es el thin pool data con los discos de VM y contenedores, donde un disco de 32 GB con 3 GB escritos ocupa 3 GB. En un host instalado con ZFS aparece local-zfs, tipo zfspool, en lugar de local-lvm.",
    "caption": "local guarda archivos; local-lvm, los discos de las VM."},
   {"file": "3-paso4.svg", "step": 4, "after": "Calculá la regla oficial",
    "alt": "La cuenta del ARC para un pool ZFS de 4 TiB: 2 GiB de base más 4 GiB, uno por TiB, igual a 6 GiB de límite sugerido. En bytes, como lo pide el módulo: 6 por 1024 al cubo, 6442450944. Bloque con lo que se vería con ese límite: zfs_arc_max en /sys/module/zfs/parameters vale 6442450944 y /etc/modprobe.d/zfs.conf tiene options zfs zfs_arc_max=6442450944. Notas: desde la 8.1 el instalador lo deja en el 10 por ciento de la RAM con tope de 16 GiB; bajarlo en producción hace que el disco rinda menos.",
    "caption": "2 GiB más 1 GiB por TiB, pasado a bytes para comparar con lo configurado."}],
  [C("LVM-thin",
     "Un disco virtual de 100 GB no tendría por qué ocupar 100 GB el primer día. LVM-thin reserva bloques recién cuando la VM los escribe, así que el almacenamiento se reparte entre lo que realmente se usa, y además permite snapshots y linked clones.",
     "Es lo que deja el instalador si elegís ext4 o xfs: un thin pool llamado data, que la GUI muestra como local-lvm. Con `lvs` ves el tamaño asignado y el porcentaje usado de cada disco. Ojo con sobreasignar: si todas las VM llenan su disco a la vez, el pool se queda sin lugar.",
     "En un servidor de una barraca en La Paz con RAID por hardware y 32 GB de RAM, LVM-thin es la elección natural: rápido, simple y sin pelear con la controladora."),
   C("ZFS",
     "ZFS junta en una sola pieza el sistema de archivos y el manejo de discos: guarda checksums de todo, detecta y corrige corrupción, comprime, hace snapshots y RAID por software, y replica entre nodos. Vino a reemplazar controladoras RAID caras con CPU y memoria.",
     "Se elige en el instalador o se crea después sobre discos directos, por HBA o controladora en modo IT. Necesita RAM (8 GB para arrancar, según la guía), y conviene ECC y SSD con protección contra cortes (PLP). Nunca encima de una RAID por hardware con caché: ZFS tiene que ver cada disco para hacer su trabajo.",
     "Para un cliente con dos servidores en una clínica de Punta Carretas querés replicación entre nodos: los armás con ZFS sobre HBA y SSD de datacenter, y la replicación cada pocos minutos te cubre si un servidor se cae."),
   C("ARC",
     "El ARC es la caché de lectura de ZFS en RAM. Cuanta más memoria tiene, menos va al disco. Pero esa memoria compite con las VM, y por eso Proxmox le pone un límite.",
     "Desde la 8.1, el instalador lo limita al 10 % de la RAM con tope de 16 GiB. La regla oficial es 2 GiB de base más 1 GiB por TiB de pool. El valor actual está en /sys/module/zfs/parameters/zfs_arc_max y el fijo en /etc/modprobe.d/zfs.conf, en bytes.",
     "Un host con 64 GB de RAM y un pool de 4 TiB: la regla da 6 GiB. Si ves que el ARC usa 16 GiB y las VM piden memoria, lo ajustás en una ventana acordada, sabiendo que con menos caché el disco rinde un poco menos.")],
  """
### Un poco de historia

ZFS lo creó Sun Microsystems y se publicó en 2005 con OpenSolaris. Su idea fue romper la separación entre controladora RAID, gestor de volúmenes y sistema de archivos: un solo componente que sabe qué bloques tienen datos y verifica cada uno con un checksum. Tras el cierre de OpenSolaris, la comunidad siguió el desarrollo como OpenZFS, y Proxmox fue la primera distribución en traer ZFS on Linux de fábrica, en 2014.

LVM, el gestor de volúmenes de Linux, es más viejo y más simple. Su variante thin agregó la asignación por demanda y los snapshots baratos. Desde Proxmox VE 4.2, el volumen data del instalador es un thin pool: el local-lvm que ves en casi todos los hosts instalados con ext4.

### Cómo funciona

Los dos son de bloque: cada disco de VM es un volumen. Y los dos son thin: un disco de 32 GB con 3 GB escritos ocupa 3 GB, porque un bloque recién se reserva cuando la VM lo escribe.

La pieza clave es el copy-on-write. Un snapshot no copia datos: anota qué bloques forman el disco en ese momento. Desde ahí, cuando la VM cambia un bloque, el dato nuevo se escribe en un bloque aparte y el viejo queda para el snapshot. Por eso sacar un snapshot es instantáneo y solo ocupa lo que cambió después. Volver atrás es apuntar el disco a los bloques anotados.

ZFS suma checksums en cada bloque, compresión, RAID por software y replicación por snapshots incrementales. Para eso necesita ver los discos de verdad y memoria para su caché, el ARC. LVM-thin no verifica datos ni hace RAID: confía en lo que tenga debajo, que puede ser una controladora por hardware.

De ahí sale la decisión. Con RAID por hardware, SSD de consumo o poca RAM, LVM-thin. Con HBA, SSD con PLP y RAM de sobra, ZFS. Y un snapshot, en cualquiera de los dos, vive en el mismo pool que el disco: si el pool se pierde, se pierde con él.
""",
  [{"file": "3-t1.svg", "after": "Volver atrás es apuntar el disco a los bloques anotados.",
    "alt": "Animación en cuatro tiempos de un snapshot copy-on-write. 1: el disco de la VM usa los bloques A, B, C y D del pool; los bloques libres no ocupan espacio. 2: al sacar el snapshot no se copia nada: se anota que A, B, C y D pertenecen al snapshot. 3: la VM modifica B; el dato nuevo se escribe en un bloque aparte, B2, y el disco pasa a ver A, B2, C y D, mientras el snapshot conserva B. 4: con un rollback el disco vuelve a A, B, C y D y B2 se descarta. Todo vive en el mismo pool, así que un snapshot no reemplaza a un backup.",
    "caption": "El snapshot anota bloques; lo nuevo se escribe aparte y lo viejo queda para volver."}],
  S("Revisar almacenamiento y el límite del ARC",
    "Muestra el estado de cada almacenamiento y, si hay ZFS, la salud del pool y el límite del ARC comparado con la regla de 2 GiB más 1 GiB por TiB. No cambia nada.",
    [("POOL_TIB", "4", "Tamaño del pool ZFS en TiB, número entero")],
    """# IES Training - Proxmox VE - Disco con criterio
# Solo lee. Correlo como root en el host.
(
POOL_TIB="{{POOL_TIB}}"
echo "== Almacenamientos =="
pvesm status
echo "== Volumenes LVM (data es el thin pool de local-lvm) =="
lvs 2>/dev/null || echo "Sin LVM"
if [ -e /sys/module/zfs/parameters/zfs_arc_max ]; then
  echo "== Pools ZFS =="
  zpool status
  ACTUAL=$(cat /sys/module/zfs/parameters/zfs_arc_max)
  SUGERIDO=$(( (2 + POOL_TIB) * 1024 * 1024 * 1024 ))
  echo "zfs_arc_max actual: $ACTUAL bytes (0 = valor por defecto del modulo)"
  echo "Regla 2 GiB + 1 GiB por TiB para $POOL_TIB TiB: $SUGERIDO bytes"
  if [ -e /etc/modprobe.d/zfs.conf ]; then
    cat /etc/modprobe.d/zfs.conf
  else
    echo "No hay /etc/modprobe.d/zfs.conf: el limite no esta fijado a mano"
  fi
  # Para fijarlo (con cuidado y en una ventana acordada):
  # options zfs zfs_arc_max=<bytes> en /etc/modprobe.d/zfs.conf
else
  echo "El modulo ZFS no esta cargado: este host no usa ZFS."
fi
echo "Listo: almacenamiento revisado. Revisa tambien Datacenter > Storage."
)""",
    ["El script no cambia el ARC: con menos caché el disco rinde menos, y eso se decide mirando el uso real.",
     "zpool status tiene que decir state: ONLINE y errors: No known data errors."]))

# =====================================================================================  4
L("4",
  {"file": "4.svg", "alt": "Ventana de Hardware y Options de la VM 100 con seis filas: tipo de procesador x86-64-v2-AES, controladora SCSI VirtIO SCSI single, disco scsi0 con iothread=1, placa net0 virtio en vmbr0, QEMU Guest Agent Enabled y CD ide2 con virtio-win.iso. Numeradas, cuatro elecciones: 1, disco en VirtIO SCSI single con IO Thread, lo que la guía recomienda para rendimiento, e IDE solo para sistemas muy viejos; 2, placa de red VirtIO, paravirtual; 3, guest agent activado y adentro, para apagado limpio y backups con el sistema de archivos congelado; 4, en ámbar, CPU host solo si no vas a migrar: con migración en vivo, el modelo de la generación más vieja del clúster. Nota de Windows: los drivers van desde el ISO virtio-win, en la versión que la wiki marca sin problemas conocidos, 0.1.271 a septiembre de 2026.",
   "caption": "Disco, red, agente y CPU: lo que se decide al crear la VM y después cuesta cambiar."},
  [{"file": "4-paso4.svg", "step": 4, "after": "probá que el agente responde",
    "alt": "El host pve1 corre qm agent 100 ping, que no muestra salida porque el agente respondió, y qm agent 100 network-get-interfaces, que devuelve ip-address 10.10.10.100. Una flecha de pedido va del host a la VM 100, una Debian con el servicio qemu-guest-agent corriendo adentro, y una de respuesta vuelve, por el canal virtio-serial. Recordatorio: se instaló en el paso 2 con apt install qemu-guest-agent. Si no responde, aparece QEMU guest agent is not running: falta instalar o arrancar el servicio adentro, o la VM no se apagó y prendió desde Proxmox después del qm set. Para qué sirve: Proxmox ve las IP de la VM, la apaga limpia y congela el disco antes de un backup.",
    "caption": "El ping al agente viaja por un canal propio entre el host y la VM."},
   {"file": "4-paso6.svg", "step": 6, "after": "Para Windows: subí el ISO de virtio-win",
    "alt": "Instalación de Windows con dos CD: el instalador del sistema y el ISO virtio-win con los drivers de Proxmox. Adentro de Windows, desde el CD de virtio-win: a, virtio-win-gt-x64, los drivers; b, virtio-win-guest-tools, el agente y los servicios. Qué versión: 0.1.271 sin problemas conocidos, en verde; 0.1.285 con errores con Windows Server 2025 y SQL, en rojo; de 0.1.215 a 0.1.262, eventos 129 Reset to device, en ámbar. Nota: la lista cambia, conviene mirar la página Windows VirtIO Drivers de la wiki de Proxmox; los datos son a septiembre de 2026.",
    "caption": "Primero los drivers, después las herramientas, y la versión que la wiki marca estable."}],
  [C("VirtIO",
     "Emular una controladora o una placa de red real obliga a QEMU a imitar hardware que nunca existió dentro de la VM, acceso por acceso. VirtIO es paravirtualización: el sistema invitado sabe que está virtualizado y habla con el host por colas compartidas, con mucho menos trabajo por operación.",
     "En el asistente: controladora VirtIO SCSI single con IO Thread en cada disco, y placa de red VirtIO. Linux trae los drivers; Windows no, y se instalan desde el ISO virtio-win durante la instalación o después. IDE queda solo para sistemas anteriores a 2003.",
     "Te llaman porque el servidor de un estudio jurídico con Windows anda lento. Ves que el disco quedó en IDE porque nadie cargó los drivers. Planificás la migración a VirtIO SCSI con el ISO de virtio-win y el disco vuelve a rendir."),
   C("QEMU guest agent",
     "Desde afuera, el host no sabe qué pasa adentro de la VM. El agente es un servicio dentro del invitado que contesta pedidos del host: apagarse limpio sin depender del botón ACPI, informar sus IP y, sobre todo, congelar el sistema de archivos un instante antes de un backup o un snapshot.",
     "Dos mitades: `qm set VMID --agent 1` del lado de Proxmox (o Options, QEMU Guest Agent) y el paquete qemu-guest-agent adentro. El cambio de hardware necesita apagar y prender la VM desde Proxmox. Se prueba con `qm agent VMID ping`; si responde, `network-get-interfaces` devuelve las IP.",
     "En la VM del servidor de bases de datos de una cooperativa en Paysandú, el backup nocturno sale consistente porque el agente congela el disco justo antes. Sin el agente, el backup es como desenchufar el equipo y copiar el disco."),
   C("Tipo de CPU",
     "La VM ve un procesador virtual con un conjunto de instrucciones. Con tipo host ve exactamente el del servidor y rinde al máximo; pero si la migrás en vivo a un nodo con otro procesador, puede encontrarse sin instrucciones que estaba usando.",
     "El default x86-64-v2-AES es un modelo genérico compatible. Tipo host solo cuando no vas a migrar o el clúster es homogéneo. Con migración en vivo, el modelo de la generación más vieja del clúster. Entre Intel y AMD, la migración en vivo no está garantizada.",
     "Un cliente suma un tercer nodo más nuevo a su clúster. Las VM con CPU host no migran en vivo hacia los viejos. Las pasás a un modelo común en una ventana de mantenimiento y la HA vuelve a poder moverlas.")],
  """
### Un poco de historia

QEMU lo escribió Fabrice Bellard a partir de 2003 como un emulador capaz de simular una computadora completa por software. Era muy flexible pero lento, porque traducía cada instrucción. A mediados de esa década Intel y AMD sumaron a sus procesadores extensiones de virtualización, VT-x y AMD-V, y en 2007 entró al kernel Linux 2.6.20 el módulo KVM, desarrollado por la empresa Qumranet, que aprovecha esas extensiones.

La combinación quedó así: KVM hace que el código de la VM corra directo en el procesador, y QEMU pone todo lo demás. Proxmox fue de las primeras empresas en dar soporte comercial a KVM. Para no imitar hardware viejo, el kernel Linux adoptó VirtIO, una familia de dispositivos pensados para máquinas virtuales que hoy es una especificación de OASIS.

### Cómo funciona

Para el host, cada VM es un proceso QEMU, identificado por su VMID. Ese proceso reserva la memoria de la VM, arma su hardware virtual (disco, placa de red, consola) y le pide al módulo KVM que ejecute las vCPU. Las instrucciones del invitado corren en el CPU real, casi sin pérdida; solo cuando la VM toca hardware, el control vuelve al host.

Adentro arranca un kernel propio: Windows, Debian o lo que sea. Por eso una VM aísla más que un contenedor: no comparte kernel con el host.

El disco y la red son el punto fino. Si la VM cree tener un disco IDE, QEMU tiene que imitar esa controladora acceso por acceso. Con VirtIO, el invitado sabe que es virtual y deja los pedidos en colas compartidas que QEMU atiende en tandas. Con VirtIO SCSI single e IO Thread, cada disco tiene además su propio hilo de atención.

El guest agent completa el cuadro: un canal entre el host y un servicio dentro de la VM. Por ahí Proxmox pide un apagado limpio, lee las IP y, antes de un backup, congela el sistema de archivos para no copiar algo a medio escribir.
""",
  [{"file": "4-t1.svg", "after": "no comparte kernel con el host.",
    "alt": "Animación en cuatro tiempos de la pila de virtualización de Proxmox VE. 1: abajo, el hardware con un CPU que tiene VT-x o AMD-V. 2: encima, el kernel Linux de Proxmox con el módulo KVM; cada VM aparece como un proceso QEMU, uno para la VM 100 y otro para la VM 101. 3: dentro de cada proceso corre el kernel propio del invitado, Windows o Linux, con sus aplicaciones, y las vCPU ejecutan directo sobre el CPU real. 4: disco y placa son virtuales; emulados como IDE, QEMU imita un disco real y traduce cada acceso; con VirtIO el invitado sabe que es virtual y usa colas compartidas, y en Windows eso pide los drivers virtio-win.",
    "caption": "KVM corre el código, QEMU arma el hardware y VirtIO acorta el camino del disco y la red."}],
  S("Activar el guest agent de una VM y probarlo",
    "Activa el agente en la configuración de la VM si no lo estaba, muestra disco, red y CPU, y prueba si el agente de adentro responde.",
    [("VMID", "100", "VM Linux de prueba")],
    """# IES Training - Proxmox VE - VM bien armada
# Correlo como root en el host. Adentro de la VM: apt install qemu-guest-agent
(
VMID="{{VMID}}"
CONF=/etc/pve/qemu-server/$VMID.conf
test -e "$CONF" || { echo "No existe la VM $VMID en este nodo"; exit 1; }
if grep -Eq "^agent: (1|enabled=1)" "$CONF"; then
  echo "El agente ya estaba activado en la VM $VMID"
else
  qm set "$VMID" --agent 1
  echo "Agente activado. Apaga y prende la VM desde Proxmox para que tome el cambio."
fi
echo "== Disco, red y CPU =="
grep -E "^(scsihw|scsi0|net0|cpu):" "$CONF"
grep -q "^scsihw: virtio-scsi-single" "$CONF" || echo "Ojo: la controladora no es VirtIO SCSI single"
echo "== Agente =="
if qm agent "$VMID" ping; then
  echo "OK: el agente responde"
  qm agent "$VMID" network-get-interfaces | grep '"ip-address"'
else
  echo "Sin respuesta: instala qemu-guest-agent adentro, arrancalo y apaga y prende desde Proxmox."
fi
echo "Listo: revisa en Options que diga QEMU Guest Agent: Enabled."
)""",
    ["Reiniciar desde adentro de la VM no alcanza para el cambio de hardware: se apaga y se prende desde Proxmox.",
     "El script no cambia la controladora ni el tipo de CPU: eso se planifica, sobre todo en Windows y en clústeres."]))
