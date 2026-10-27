"""Manifest Proxmox, lecciones 9 a 12 (lo arma manifest_pmx.py)."""
from _mbase import L, C, S

# =====================================================================================  9
L("9",
  {"file": "9.svg", "alt": "Tres casos. Dos nodos y cae uno: pve1 queda con 1 de 2 votos, sin quórum, en solo lectura, en rojo. Dos nodos más QDevice: pve1 y el QDevice suman 2 de 3 votos, con quórum, sigue andando, en verde. Tres nodos y cae uno: 2 de 3 votos, con quórum, en verde. Notas: sin quórum /etc/pve queda de solo lectura, no se crean ni arrancan VMs y la HA no conmuta; corosync pide menos de 5 ms, red física propia y un segundo enlace, y el QDevice va por TCP y puede estar en otra sede.",
   "caption": "Quórum es mayoría: con dos votos, perder uno deja al clúster quieto."},
  [{"file": "9-paso4.svg", "step": 4, "after": "Apagá `pve2`. En `pve1` corré",
    "alt": "pve1, 10.10.10.11, encendido, y pve2 apagado. Salida recortada de pvecm status en pve1: Expected votes 2, Total votes 1 en rojo, Quorum 2 y Quorate No en rojo. Al costado, crear una VM: no te deja, porque con 1 voto de 2 /etc/pve está en solo lectura. La cuenta: quórum es la mayoría de los votos esperados, 2; hay 1 voto, 1 es menos que 2, sin quórum. Nota: en el paso 6, con el QDevice, Expected votes pasa a 3, Quorum a 2, y pve1 con el QDevice suman 2: Quorate Yes.",
    "caption": "Con un voto de dos no hay mayoría: el clúster queda de solo lectura."},
   {"file": "9-paso5.svg", "step": 5, "after": "Prendé `pve2`. En una tercera máquina",
    "alt": "pve1, 10.10.10.11, y pve2, 10.10.10.12, unidos por corosync en UDP 5405 a 5412. Los dos hablan por TCP con una tercera máquina Debian, 10.10.10.13, que corre corosync-qnetd, no corre VMs y solo vota. En los dos nodos va corosync-qdevice, y en pve1 se corre pvecm qdevice setup 10.10.10.13. Nota: el QDevice no exige la latencia de corosync y puede estar en otra sede; se recomienda en clústeres pares, no en impares.",
    "caption": "Un tercer equipo que solo vota completa el quórum de un clúster de dos."}],
  [C("Quórum",
     "En un clúster, cada nodo podría tomar decisiones por su cuenta. Si la red se parte, dos mitades podrían arrancar la misma VM o escribir configuraciones distintas. El quórum resuelve eso: solo la parte con mayoría de votos puede cambiar algo.",
     "Cada nodo tiene un voto. `pvecm status` muestra Expected votes, Total votes, Quorum y Quorate. Sin quórum, /etc/pve pasa a solo lectura: no se crean ni arrancan VMs y la HA no actúa. `pvecm expected 1` fuerza el quórum en una emergencia, sabiendo lo que se hace.",
     "Te llaman porque en un clúster de dos nodos de un hotel en Punta del Este no se puede prender ninguna VM. Un nodo se apagó por un corte de luz; el otro quedó con 1 de 2 votos. Prendés el nodo caído y todo vuelve."),
   C("Corosync",
     "Un clúster necesita que todos los nodos reciban los mismos mensajes en el mismo orden. Corosync es la capa de comunicación que lo garantiza y la que cuenta los votos. Sobre ella, Proxmox replica /etc/pve a todos los nodos.",
     "Pide latencia menor a 5 ms, red física propia (nunca compartida con almacenamiento) y, mejor, un segundo enlace en otra red. Un NIC dedicado de 1 Gbit alcanza. Usa UDP 5405 a 5412. Su log se lee con `journalctl -b -u corosync`.",
     "En un clúster de tres nodos para una cadena de estaciones de servicio, ponés corosync en un switch aparte y un segundo enlace por la red de gestión. Un backup pesado ya no hace que los nodos se pierdan entre sí."),
   C("QDevice",
     "Con dos nodos, perder uno es perder la mayoría. Un tercer nodo completo cuesta un servidor. El QDevice es un tercer voto barato: un servicio en cualquier equipo Debian que no corre VMs, solo vota.",
     "corosync-qnetd en el tercer equipo, corosync-qdevice en los nodos y `pvecm qdevice setup IP` en uno de ellos. Va por TCP y no tiene la exigencia de latencia de corosync, así que puede estar en otra sede. Se recomienda en clústeres pares, no en impares.",
     "Un cliente con dos servidores en su sede de Montevideo: el QDevice corre en una VM chica en la infraestructura de IES. Si cae un servidor, el otro conserva el quórum y la HA arranca las VM.")],
  """
### Un poco de historia

Corosync nació del proyecto OpenAIS como un motor de comunicación para clústeres: entrega mensajes a todos los miembros en el mismo orden y lleva la cuenta de quién está. Proxmox lo adoptó temprano, y el gran salto fue montar encima el Proxmox Cluster File System, pmxcfs: una base de datos replicada en tiempo real que se ve como la carpeta /etc/pve. Con eso, según la propia documentación, manejar un clúster de 16 nodos es tan simple como manejar uno.

El concepto de quórum viene de los sistemas distribuidos: el número mínimo de votos que una operación necesita para estar permitida. En marzo de 2026, un usuario del foro oficial contaba que su clúster de dos nodos no conmutaba en las pruebas de falla; la respuesta fue la de siempre, un QDevice.

### Cómo funciona

Cada nodo aporta un voto y corosync los cuenta en todo momento. El quórum es la mayoría estricta de los votos esperados: con dos votos esperados hacen falta dos; con tres, alcanzan dos. Mientras un nodo es parte de la mayoría, /etc/pve acepta escrituras: se crean VMs, se arrancan, se cambia la configuración.

Si la red se parte, cada lado cuenta sus votos. El lado con mayoría sigue. El lado sin mayoría pasa a solo lectura y no toca nada. Con dos nodos, un corte del enlace deja a los dos con 1 de 2: ninguno sigue, y es preferible a que dos mitades hagan cosas distintas con las mismas VM.

Ese mismo razonamiento explica por qué dos nodos no alcanzan para alta disponibilidad: si cae uno, el otro queda en minoría y la HA no puede actuar. El QDevice agrega un tercer voto desde afuera. Con tres votos esperados, un nodo y el QDevice suman dos, y hay mayoría.

Por eso corosync quiere su propia red, con latencia baja y estable: si los mensajes se demoran, un nodo puede creer que perdió a los demás aunque estén vivos.
""",
  [{"file": "9-t1.svg", "after": "ninguno sigue, y es preferible a que dos mitades",
    "alt": "Animación en cuatro tiempos. 1: pve1 y pve2 se intercambian mensajes por corosync; cada uno ve 2 de 2 votos y hay quórum. 2: se corta el enlace; cada nodo ve 1 de 2 votos, ninguno tiene mayoría y los dos pasan a solo lectura. 3: se suma un QDevice con corosync-qnetd en un tercer equipo; el clúster espera 3 votos y tiene 3. 4: pve2 se apaga; pve1 y el QDevice suman 2 de 3 votos, mantienen el quórum y el clúster sigue andando.",
    "caption": "Sin mayoría nadie escribe; con un tercer voto, perder uno deja mayoría."}],
  S("Revisar el quórum y sumar el QDevice",
    "Muestra los votos y el estado del quórum, avisa si el clúster tiene dos votos sin QDevice y, solo si lo pedís, corre pvecm qdevice setup.",
    [("QNETD_IP", "10.10.10.13", "Equipo con corosync-qnetd"), ("HACER_SETUP", "no", "si para correr pvecm qdevice setup")],
    """# IES Training - Proxmox VE - Tres votos
# Correlo como root en un nodo del cluster (pve1 en el laboratorio).
(
QNETD="{{QNETD_IP}}"; HACER="{{HACER_SETUP}}"
test -e /etc/pve/corosync.conf || { echo "Este nodo no esta en un cluster"; exit 1; }
echo "== Votos =="
pvecm status | grep -E "Expected votes|Total votes|Quorum:|Quorate|Qdevice"
if pvecm status | grep -Eq "Quorate: +Yes"; then
  echo "OK: hay quorum"
else
  echo "Ojo: sin quorum, /etc/pve en solo lectura. Revisa nodos caidos y journalctl -b -u corosync"
fi
ESPERADOS=$(pvecm status | grep "Expected votes" | grep -o "[0-9]*")
if pvecm status | grep -q "Qdevice"; then
  echo "QDevice presente"
elif [ "$ESPERADOS" = "2" ]; then
  echo "Ojo: dos votos sin QDevice. Si cae un nodo, el otro queda sin quorum."
  echo "En $QNETD: apt install corosync-qnetd. En cada nodo: apt install corosync-qdevice"
  if [ "$HACER" = "si" ]; then
    pvecm qdevice setup $QNETD
    pvecm status | grep -E "Expected votes|Quorate"
  fi
fi
echo "Listo: quorum revisado. Proba apagar un nodo y mirar Quorate en el otro."
)""",
    ["pvecm qdevice setup necesita corosync-qdevice instalado en todos los nodos y corosync-qnetd en el tercer equipo: el script no instala en otras máquinas.",
     "Un nodo que se une a un clúster no puede tener VMs: vacialo antes del pvecm add."]))

# =====================================================================================  10
L("10",
  {"file": "10.svg", "alt": "Tres requisitos de la alta disponibilidad: 1, tres votos, tres nodos o dos y un QDevice, porque sin quórum la HA no mueve nada; 2, almacenamiento compartido, NFS, iSCSI, Ceph o replicación ZFS, porque con disco local la VM queda en el nodo caído; 3, fencing por watchdog, el nodo aislado se reinicia solo antes de que la VM arranque en otro lado. Cuando cae un nodo: pve1 cae o queda aislado, en rojo; pierde quórum y su watchdog lo reinicia, en ámbar; la VM arranca en pve2, en verde. El freno, desde Proxmox VE 9.2: antes de tocar la red o corosync, ha-manager crm-command disarm-ha freeze; terminado el mantenimiento, ha-manager crm-command arm-ha.",
   "caption": "Quórum, storage compartido y fencing; y en mantenimiento, desarmar la HA."},
  [{"file": "10-paso1.svg", "step": 1, "after": "Migración en vivo (si el disco es local",
    "alt": "Dos casos de migración de pve1 a pve2. Con almacenamiento compartido, qm migrate 100 pve2 --online: viajan la RAM y el estado de la VM, y el disco, que está en el storage compartido, no viaja. Con disco local, agregando --with-local-disks: viajan la RAM, el estado de la VM y el disco completo, marcado en ámbar. Nota: la VM sigue andando durante la copia; con CPU tipo host y procesadores distintos, la migración en vivo puede fallar.",
    "caption": "Con storage compartido viaja la memoria; con disco local, también el disco."},
   {"file": "10-paso3.svg", "step": 3, "after": "Desarmá la HA como harías antes",
    "alt": "Tres estados del fencing: armed, en verde, los watchdogs están abiertos y un nodo sin quórum se reinicia; disarming, en ámbar, congela los servicios y espera que cada nodo suelte su watchdog; disarmed, en rojo, sin fencing ni failover, la HA no protege nada. Una flecha punteada vuelve de disarmed a armed con ha-manager crm-command arm-ha. Se ve en la línea de fencing de ha-manager status. Notas: freeze deja los servicios como están e ignore los saca del control de la HA para moverlos a mano; mientras está desarmada, una falla real no se recupera sola, así que la ventana va lo más corta posible.",
    "caption": "armed, disarming, disarmed: la línea de fencing dice si la HA te protege."}],
  [C("Alta disponibilidad (HA)",
     "Cuando un nodo se cae, sus VMs se caen con él. La HA de Proxmox detecta la falla y arranca esas VMs en otro nodo, sin que nadie tenga que entrar a hacerlo a mano a las tres de la mañana.",
     "Se pone cada VM bajo HA con `ha-manager add vm:VMID` o en Datacenter, HA, y se mira con `ha-manager status`. Exige tres votos, almacenamiento compartido (o replicación ZFS) y hardware redundante. En Proxmox VE 9, los grupos de HA pasaron a reglas de afinidad.",
     "En el clúster de un centro de monitoreo, la VM de la receptora de alarmas está en HA. Un nodo se apaga por una falla de fuente y, en un par de minutos, la receptora está corriendo en otro nodo."),
   C("Fencing por watchdog",
     "Si un nodo queda aislado de la red del clúster pero sigue vivo, puede seguir escribiendo en el almacenamiento compartido. Arrancar la misma VM en otro nodo en ese momento la destruiría: dos escritores sobre un disco. El fencing garantiza que el nodo aislado esté apagado antes.",
     "Proxmox usa un watchdog: un temporizador que el nodo tiene que renovar mientras tiene quórum. Si lo pierde, no lo renueva y, a los 60 segundos, el watchdog lo reinicia. Puede ser un watchdog de hardware de la placa o, si no hay, el softdog del kernel.",
     "Un cable de corosync se suelta en un rack de un cliente en Canelones. El nodo aislado se reinicia solo y sus VMs arrancan en otro: no hay dos copias escribiendo el mismo disco."),
   C("Migración en vivo",
     "Mantenimiento sin cortar el servicio: mover una VM que está corriendo de un nodo a otro mientras los usuarios siguen trabajando.",
     "`qm migrate 100 pve2 --online`. Con almacenamiento compartido solo viajan la RAM y el estado; con disco local, `--with-local-disks` copia también el disco. La VM no puede tener dispositivos PCI o USB pasados, y el destino tiene que tener la misma versión de Proxmox o una más nueva.",
     "Antes de cambiar una memoria en pve1, migrás en vivo sus cinco VMs a pve2. El cliente no se entera, cambiás la memoria y las volvés."),
   C("Disarm de HA",
     "Ciertos trabajos, como reconfigurar la red o corosync, pueden hacer perder el quórum un momento. Con la HA armada, eso dispararía el fencing y reiniciaría nodos sin necesidad. Desde Proxmox VE 9.2 se puede desarmar la HA en todo el clúster.",
     "`ha-manager crm-command disarm-ha freeze` congela los servicios y libera los watchdogs; `ignore` los saca del control de la HA para moverlos a mano. Al terminar, `ha-manager crm-command arm-ha`. Mientras está desarmada no hay protección: la ventana, lo más corta posible.",
     "Antes de cambiar el switch de corosync de un cliente, desarmás la HA, hacés el cambio, confirmás el quórum y volvés a armar. Ningún nodo se reinicia por sorpresa.")],
  """
### Un poco de historia

El HA manager de Proxmox llegó con la versión 4.0, la misma que pasó de OpenVZ a LXC. Proxmox eligió no depender de herramientas externas como Pacemaker ni de dispositivos de fencing caros, como enchufes que cortan la energía de un nodo: usó watchdogs, temporizadores que existen en sistemas críticos desde los primeros microcontroladores. Proxmox VE 9 reemplazó los grupos de HA por reglas de afinidad, y la 9.2 agregó el disarm para mantenimiento.

La migración en vivo es más vieja que Proxmox: la técnica de copiar la memoria en pasadas mientras la VM sigue corriendo se describió en 2005 en un trabajo sobre Xen, y QEMU la implementa de la misma forma.

### Cómo funciona

Para migrar en vivo, Proxmox arranca en el destino un proceso QEMU vacío y en pausa, que espera los datos. Si el disco está en almacenamiento compartido, no viaja: solo falta la memoria. El origen manda toda la RAM mientras la VM sigue trabajando, y marca como sucias las páginas que la VM cambia en el camino. Después manda solo las sucias, que son menos, y repite. Cuando lo que falta se puede mandar en milisegundos, pausa la VM, envía el resto y el estado de los dispositivos, y el destino continúa. La pausa queda muy por debajo del segundo.

La HA resuelve el caso sin aviso: un nodo que se cae. El problema es distinguir un nodo caído de uno aislado. Cada nodo con servicios en HA renueva su watchdog mientras tiene quórum. Si queda aislado, pierde el quórum y deja de renovarlo; a los 60 segundos el watchdog lo reinicia. Ese reinicio es el fencing: la garantía de que la VM vieja ya no escribe.

Recién entonces el gestor de HA, del lado que conserva el quórum, arranca la VM en otro nodo, sobre el mismo disco compartido. Sin almacenamiento compartido o replicación, el disco quedó en el nodo caído y no hay nada que arrancar.
""",
  [{"file": "10-t1.svg", "after": "La pausa queda muy por debajo del segundo.",
    "alt": "Animación en cuatro tiempos de una migración en vivo de la VM 100 de pve1 a pve2, con la RAM dibujada como doce páginas. 1: en pve2 arranca un proceso QEMU en pausa que espera los datos; el disco está en almacenamiento compartido y no viaja. 2: primera pasada: se copian las doce páginas mientras la VM sigue escribiendo, y cuatro quedan marcadas como sucias. 3: la segunda pasada manda solo esas cuatro y queda una sucia; cada pasada es más chica. 4: el origen se pausa menos de un segundo, se manda la última página y el estado de los dispositivos, y la VM sigue corriendo en pve2.",
    "caption": "La memoria viaja en pasadas cada vez más chicas hasta que el corte es imperceptible."},
   {"file": "10-t2.svg", "after": "la garantía de que la VM vieja ya no escribe.",
    "alt": "Animación en cuatro tiempos de un clúster de tres nodos con alta disponibilidad y almacenamiento compartido. 1: la VM 100 corre en pve1, escribe en el storage y pve1 renueva su watchdog porque tiene quórum. 2: pve1 pierde la red del clúster y queda sin quórum; no puede renovar el watchdog y la VM sigue escribiendo, así que arrancarla en otro nodo la rompería. 3: a los 60 segundos el watchdog reinicia pve1 y la VM vieja deja de escribir. 4: con pve1 fuera, la HA arranca la VM 100 en pve2 sobre el mismo disco compartido.",
    "caption": "Primero el fencing apaga al nodo aislado; después la HA mueve la VM."}],
  S("Poner una VM bajo HA y mirar el fencing",
    "Confirma que hay quórum, agrega la VM a la HA si no estaba y muestra el estado con la línea de fencing. Los comandos de disarm y arm quedan comentados para la ventana de mantenimiento.",
    [("VMID", "100", "VM a proteger, en almacenamiento compartido")],
    """# IES Training - Proxmox VE - HA con fencing
# Correlo como root en un nodo del cluster con quorum.
(
VMID="{{VMID}}"
if pvecm status | grep -Eq "Quorate: +Yes"; then
  echo "OK: hay quorum"
else
  echo "Sin quorum: la HA no puede actuar. Revisa la leccion Tres votos."
  exit 1
fi
if ha-manager status | grep -q "vm:$VMID"; then
  echo "La VM $VMID ya estaba bajo HA"
else
  ha-manager add vm:$VMID
  echo "VM $VMID agregada a la HA"
fi
ha-manager status
# Antes de tocar red o corosync (Proxmox VE 9.2 o superior), y solo durante la ventana:
# ha-manager crm-command disarm-ha freeze
# ...mantenimiento...
# ha-manager crm-command arm-ha
echo "Listo: VM $VMID en HA. Mira la linea fencing: armed es protegido."
)""",
    ["Con disco local y sin replicación, la HA no puede recuperar la VM en otro nodo.",
     "El disarm queda comentado a propósito: mientras está desarmada, una falla real no se recupera sola."]))

# =====================================================================================  11
L("11",
  {"file": "11.svg", "alt": "Tres columnas de acceso. Un usuario por persona: tecnico@pve con PVEAuditor, que mira y no toca; operador@pve con PVEVMUser, consola, encendido y backup; root@pam, solo el administrador. Segundo factor: TOTP, código de la app del celular; WebAuthn, llave de seguridad; recovery keys guardadas en el gestor. Firewall sin quedarse afuera: sesión SSH abierta antes de habilitar, IPSet management con las IPs de administración y, recién al final, Firewall: Yes. Nota: con usuarios personales el log dice quién hizo cada cambio, y con más de un factor perder el celular no te deja afuera.",
   "caption": "Quién entra, cómo prueba que es él y desde dónde puede entrar."},
  [{"file": "11-paso1.svg", "step": 1, "after": "Usuario de solo lectura",
    "alt": "Comandos: pveum user add tecnico@pve con el comentario Técnico de soporte, pveum passwd tecnico@pve, pveum acl modify / --user tecnico@pve --role PVEAuditor resaltado, y pveum user permissions tecnico@pve. Al costado, el árbol de permisos con / y debajo /nodes, /vms y /storage; PVEAuditor asignado en / se hereda hacia abajo. Lo que puede hacer tecnico@pve: ver nodos, VMs y almacenamiento, y ver estado y configuración, con tilde; prender, apagar o borrar VMs y cambiar la configuración, con cruz. Nota: el realm pve tiene contraseñas propias de Proxmox, lo más cómodo en instalaciones chicas; pam es para usuarios del sistema Linux.",
    "caption": "Un rol asignado en / alcanza todo el árbol: PVEAuditor mira, no toca."},
   {"file": "11-paso3.svg", "step": 3, "after": "Firewall, en este orden:",
    "alt": "Tres pasos en orden: a, abrir una sesión SSH al nodo y dejarla abierta, es la salida si algo falla; b, IPSet management en Datacenter, Firewall, IPSet, con la IP de administración, por ejemplo 10.10.10.50; c, en verde, Firewall: Yes en Datacenter, Firewall, Options, recién ahora. Al costado, desde la sesión SSH: pve-firewall status para ver si compila sin errores y pve-firewall stop si quedaste afuera de la web. Nota: en un servidor remoto sin consola fuera de banda, un firewall mal configurado te deja sin acceso; hubo quien tuvo que arrancar en modo rescate y editar la base de configuración de Proxmox para volver a entrar.",
    "caption": "SSH abierta, IPSet cargado y recién entonces el firewall."}],
  [C("Roles y permisos",
     "Si todos entran como root, no hay forma de saber quién hizo un cambio ni de limitar lo que puede romper cada uno. Proxmox asigna roles (conjuntos de privilegios) a usuarios o grupos sobre rutas del árbol de permisos.",
     "Un usuario por persona en el realm pve, con `pveum user add`. El rol se asigna con `pveum acl modify RUTA --user USUARIO --role ROL`: PVEAuditor para mirar, PVEVMUser para operar VMs. Asignado en /, alcanza todo. `pveum user permissions` muestra lo que resulta. Root queda para el administrador.",
     "El técnico de guardia de IES entra a los Proxmox de los clientes con su usuario y PVEAuditor: ve alarmas de discos y estado de backups sin poder borrar nada por error."),
   C("Segundo factor (2FA)",
     "Una contraseña filtrada alcanza para entrar a la web de Proxmox y, desde ahí, a todas las VM. Un segundo factor pide además algo que tenés: el código del celular o una llave de seguridad.",
     "Cada usuario lo configura en Datacenter, Permissions, Two Factor: TOTP con una app, WebAuthn con una llave, y claves de recuperación de un solo uso guardadas en el gestor de contraseñas. Conviene más de un factor; si alguien pierde todo, un administrador lo destraba con `pveum user tfa unlock`.",
     "Una técnica cambia de celular y pierde la app de TOTP. Entra con una de sus claves de recuperación, registra el celular nuevo y sigue trabajando, sin esperar a que alguien la destrabe."),
   C("Firewall e IPSet management",
     "El firewall de Proxmox viene deshabilitado. Al habilitarlo a nivel datacenter, se bloquea el tráfico hacia los hosts salvo lo permitido, y un error puede dejarte sin acceso al servidor que estás configurando.",
     "Antes de habilitar: una sesión SSH abierta y el IPSet llamado management con las IPs desde donde se administra. Después, Firewall: Yes en Datacenter, Firewall, Options. `pve-firewall status` muestra si las reglas compilan; `pve-firewall stop` lo apaga desde la consola si algo salió mal.",
     "Configurás el firewall de un servidor alquilado en un datacenter, sin consola fuera de banda. Con la sesión SSH abierta y tu IP en management, habilitás, probás desde otra IP y confirmás que el bloqueo funciona sin quedarte afuera.")],
  """
### Un poco de historia

Proxmox autentica contra realms: PAM, los usuarios del sistema Linux; PVE, con contraseñas propias de Proxmox; y LDAP o Active Directory para empresas que ya tienen un directorio. Para el segundo factor usa estándares abiertos: TOTP, los códigos de seis dígitos que cambian cada 30 segundos, definido en la RFC 6238 de 2011, y WebAuthn, el estándar del W3C para llaves de seguridad.

El firewall integrado se construyó sobre las herramientas de filtrado del kernel Linux, y hoy convive con proxmox-firewall, una versión nueva basada en nftables que suma reglas de forward. En 2024, Diego Carrasco contó en su blog cómo quedó afuera de su servidor alquilado por habilitar el firewall con una regla equivocada: tuvo que arrancar en modo rescate y editar la base de configuración de Proxmox para volver.

### Cómo funciona

Los permisos se asignan sobre un árbol de rutas: /, /nodes, /vms, /storage y más abajo. Un rol asignado en una ruta se hereda hacia abajo. Un rol es un conjunto de privilegios: PVEAuditor reúne los de lectura; PVEVMUser, los de usar VMs. `pveum user permissions` calcula lo que resulta para un usuario, y es la forma de comprobar que no tiene de más.

El firewall tiene tres zonas: el host (a nivel datacenter o nodo), cada VM o contenedor, y las redes virtuales. Habilitado en el datacenter, bloquea el tráfico hacia los hosts salvo las excepciones de la red local, como la web en 8006, SSH en 22 y corosync. El IPSet management es una lista con nombre que el firewall ya conoce: las IPs que pongas ahí pueden administrar el host.

El orden importa. Una conexión SSH ya establecida es la puerta de atrás si la regla nueva te deja afuera. Con la sesión abierta y tu IP en management, habilitás, probás desde otra IP que no esté en la lista y, si algo salió mal, `pve-firewall stop` desde esa sesión te devuelve el acceso.
""",
  [{"file": "11-t1.svg", "after": "pueden administrar el host.",
    "alt": "Animación en cuatro tiempos con dos PC y el nodo pve1. 1: con el firewall apagado, la PC de administración 10.10.10.50 y una PC de otra red, 198.51.100.20, llegan a la web por 8006 y a SSH. 2: antes de habilitarlo, se abre una sesión SSH desde la PC de administración y se carga el IPSet management con 10.10.10.50. 3: con Firewall: Yes, el tráfico de 10.10.10.50 pasa porque está en management y el de 198.51.100.20 queda bloqueado. 4: si algo salió mal, desde la sesión SSH que quedó abierta se corre pve-firewall stop y se recupera el acceso.",
    "caption": "Habilitado, el firewall deja pasar solo lo permitido; la SSH abierta es la salida."}],
  S("Crear un usuario de solo lectura para soporte",
    "Crea el usuario en el realm pve si no existe, le asigna el rol en / y muestra sus permisos efectivos. También revisa que el firewall compile. No habilita el firewall.",
    [("USUARIO", "tecnico@pve", "Usuario personal, realm pve"), ("ROL", "PVEAuditor", "Rol a asignar en /")],
    """# IES Training - Proxmox VE - Acceso blindado
# Correlo como root en un nodo. La clave se carga al final, aparte.
(
USUARIO="{{USUARIO}}"; ROL="{{ROL}}"
if pveum user permissions "$USUARIO" >/dev/null 2>&1; then
  echo "El usuario $USUARIO ya existia"
else
  pveum user add "$USUARIO" --comment "Tecnico de soporte"
  echo "Usuario $USUARIO creado"
fi
pveum acl modify / --user "$USUARIO" --role "$ROL"
echo "== Permisos efectivos de $USUARIO =="
pveum user permissions "$USUARIO"
echo "== Firewall (solo estado) =="
pve-firewall status
echo "Listo: $USUARIO con $ROL en /."
echo "Falta la clave (te la pide por teclado): pveum passwd $USUARIO"
echo "Despues: 2FA en Datacenter > Permissions > Two Factor, con recovery keys."
)""",
    ["pveum passwd queda fuera del script porque pide la clave por teclado: correlo aparte.",
     "El script no habilita el firewall: eso va en el orden de la lección, con la sesión SSH abierta y el IPSet management cargado."]))

# =====================================================================================  12
L("12",
  {"file": "12.svg", "alt": "Cinco tarjetas en orden de diagnóstico: 1, quórum, con pvecm status, para ver Quorate Yes; 2, logs, con journalctl -b, de corosync y pve-cluster desde el arranque; 3, locks, con grep de lock en las configuraciones, por si una VM quedó trabada; 4, storage, con pvesm status, que todo esté active; 5, punteada, firewall, con pve-firewall status, si hay sospecha. Upgrade mayor de 8 a 9: backup probado de todo, pve8to9 --full antes, durante y después, SSH con tmux o IPMI y nunca la consola de la GUI, un nodo por vez verificando antes de seguir. La trampa silenciosa: en Proxmox VE 9 /etc/sysctl.conf ya no se lee y lo que estaba ahí se pierde en el próximo reinicio; va en /etc/sysctl.d/.",
   "caption": "Quórum, logs, locks y almacenamiento, en ese orden; y el upgrade, de a un nodo."},
  [{"file": "12-paso3.svg", "step": 3, "after": "Locks: mirá si alguna VM quedó con",
    "alt": "Ejemplo: grep -l de lock en /etc/pve/qemu-server/*.conf encuentra 100.conf, y grep en ese archivo muestra lock: backup. Quién pone un lock: un backup en curso, un snapshot o una migración; si se corta la luz a mitad, queda puesto. Antes de destrabar, confirmar que no hay una tarea corriendo sobre la VM 100 en Tasks del nodo y que no hay un backup ni una migración en curso; recién entonces qm unlock 100. Nota: destrabar con un backup corriendo puede dejar la VM o el backup a medias; el lock está para proteger.",
    "caption": "Un lock tiene un motivo: confirmalo antes del qm unlock."},
   {"file": "12-paso5.svg", "step": 5, "after": "Si el host viene de la 8, buscá",
    "alt": "A la izquierda, en rojo, /etc/sysctl.conf, ignorado en Proxmox VE 9, con ajustes de ejemplo net.ipv4.ip_forward=1 y vm.swappiness=10: al reiniciar vuelven al valor por defecto. Una flecha mover lleva a la derecha, en verde, /etc/sysctl.d/, un archivo por tema con nombre NN-nombre.conf, con el ejemplo /etc/sysctl.d/90-ies.conf y los mismos dos ajustes. Para ver qué hay en el viejo sin comentarios ni líneas vacías: cat /etc/sysctl.conf con grep -v de los comentarios y grep punto. Nota: los valores son un ejemplo de formato, no una recomendación.",
    "caption": "Lo que estaba en sysctl.conf pasa a un archivo en /etc/sysctl.d/."}],
  [C("Upgrade mayor",
     "Pasar de la 8 a la 9 cambia Debian, el kernel, QEMU y la forma en que se leen algunas configuraciones. Un upgrade cortado a la mitad o hecho en todos los nodos a la vez puede dejar un clúster entero fuera de servicio.",
     "Backup probado de todo, al menos 5 GB libres en la raíz y `pve8to9 --full` antes, durante y después, hasta que no marque errores. Se hace por SSH con tmux o por IPMI, nunca desde la consola web, que se corta. En clúster, un nodo por vez: se vacía, se actualiza, se controla y recién ahí el siguiente.",
     "Para el clúster de tres nodos de un cliente agendás tres ventanas nocturnas, una por nodo. Cada noche vaciás uno con migración en vivo, lo actualizás y lo dejás con sus VMs antes de irte."),
   C("Orden de diagnóstico",
     "Cuando algo falla en un clúster, los síntomas confunden: una VM que no arranca puede ser falta de quórum, un lock, un almacenamiento caído o el firewall. Seguir siempre el mismo orden evita perder una mañana probando al azar.",
     "Quórum con `pvecm status`; logs del arranque con `journalctl -b -u corosync` y `-u pve-cluster`; locks en las configuraciones de las VM; almacenamiento con `pvesm status`; y el firewall con `pve-firewall status` si hay sospecha. Conviene anotar cómo se ve cada salida en un host sano.",
     "Te llaman porque no se puede prender una VM en un clúster de una mutualista. pvecm status dice Quorate: Yes, los logs están limpios, pero la VM tiene lock: backup de un corte de luz de la noche. Confirmás que no hay tareas, `qm unlock` y arranca."),
   C("Lock de VM",
     "Mientras corre un backup, un snapshot o una migración, Proxmox pone un lock en la VM para que nadie la toque y la deje inconsistente. Si la tarea se corta, por ejemplo por un corte de luz, el lock queda puesto.",
     "Se ve como una línea `lock:` en /etc/pve/qemu-server/VMID.conf. `qm unlock VMID` lo saca, pero solo después de confirmar que no hay una tarea en curso sobre esa VM.",
     "Una VM de un cliente no arranca y la GUI dice que está bloqueada. El lock es de un backup nocturno que se cortó con la luz; las tareas del nodo no muestran nada corriendo, así que lo sacás con tranquilidad."),
   C("sysctl.d",
     "Los ajustes del kernel (reenvío de paquetes, uso de swap y otros) se cargan al arrancar. En Proxmox VE 9, systemd-sysctl dejó de leer /etc/sysctl.conf: lo que estaba ahí desaparece en el primer reinicio después del upgrade, sin avisar.",
     "Se revisa el archivo viejo sin comentarios (`grep -v '^#' /etc/sysctl.conf | grep .`) y cada ajuste se mueve a un archivo en /etc/sysctl.d/ con nombre NN-nombre.conf.",
     "Después de actualizar a la 9 el host de un cliente, una VM que hacía de router deja de rutear. El ip_forward estaba en sysctl.conf; lo pasás a /etc/sysctl.d/ y vuelve a funcionar.")],
  """
### Un poco de historia

Cada versión mayor de Proxmox VE acompaña una versión de Debian: la 8 iba sobre Debian 12 Bookworm y la 9, sobre Debian 13 Trixie. Por eso un upgrade mayor es también un upgrade de sistema operativo, y Proxmox publica para cada salto una herramienta de chequeo, pve8to9 en este caso, y una guía paso a paso.

El salto a la 9 trajo cambios silenciosos: systemd-sysctl dejó de leer /etc/sysctl.conf, se eliminó cgroup v1 y, con el kernel nuevo, algunas placas de red pueden cambiar de nombre y dejar al host sin red. Para eso la 9 trae pve-network-interface-pinning. Los cursos oficiales de partners de Proxmox para la 9 incluyen escenarios de romper y arreglar: deriva de repositorios, VLAN mal configurada, pérdida de quórum.

### Cómo funciona

En un clúster, el upgrade va de a un nodo. Primero se vacía: sus VMs migran en vivo a los otros. Con el nodo vacío, se corre pve8to9 --full, se cambian los repositorios a Trixie, se actualiza con apt full-upgrade, se reinicia y se vuelve a chequear. Después, las VMs del segundo nodo pasan al primero, que ya está en la 9. Migrar de una versión vieja a una nueva siempre funciona; al revés no está garantizado. Así se avanza hasta el último, y el clúster nunca pierde más de un voto a la vez.

Todo eso se hace por SSH dentro de tmux, o por IPMI: la consola web de la GUI depende de servicios que se reinician durante el upgrade y se corta a la mitad.

Para diagnosticar, el orden va de lo general a lo particular. Sin quórum no funciona nada más, así que es lo primero. Los logs del arranque de corosync y pve-cluster explican por qué. Después, los locks que dejan trabadas a VMs puntuales, el almacenamiento y, si hay sospecha, el firewall.
""",
  [{"file": "12-t1.svg", "after": "el clúster nunca pierde más de un voto a la vez.",
    "alt": "Animación en cuatro tiempos de un clúster de tres nodos en Proxmox VE 8.4 con cuatro VM. 1: las VM A y B migran en vivo de pve1 a pve2 y pve3, y pve1 queda vacío. 2: pve1 se actualiza a la 9 con pve8to9 --full antes, durante y después, se reinicia y se controla. 3: las VM A y C, que estaban en pve2, migran a pve1, porque de 8.4 a 9 siempre funciona; pve2 queda vacío y se actualiza. Migrar de 9 a 8.4 no está soportado. 4: las VM B y D pasan de pve3 a pve2 y pve3 se actualiza. Al final los tres nodos están en la 9 y nunca hubo dos actualizándose a la vez.",
    "caption": "Vaciar, actualizar, controlar y seguir con el próximo: nunca dos a la vez."}],
  S("Hoja de diagnóstico del nodo",
    "Solo lee: versión, quórum, últimas líneas de corosync y pve-cluster, locks, almacenamiento, firewall y ajustes de sysctl.conf que la 9 ya no lee. Sirve para anotar cómo se ve un nodo sano.",
    [("LINEAS", "5", "Cuántas líneas de log mostrar por servicio")],
    """# IES Training - Proxmox VE - Upgrade y rescate
# Solo lee: no destraba ni cambia nada. Correlo como root en el nodo.
(
LINEAS="{{LINEAS}}"
echo "== Version =="; pveversion
echo "== Quorum =="
if [ -e /etc/pve/corosync.conf ]; then
  pvecm status | grep -E "Quorate|Expected votes|Total votes"
else
  echo "Nodo sin cluster"
fi
echo "== corosync y pve-cluster desde el arranque =="
journalctl -b -u corosync | tail -n $LINEAS
journalctl -b -u pve-cluster | tail -n $LINEAS
echo "== Locks =="
LOCKS=$(grep -l '^lock:' /etc/pve/qemu-server/*.conf 2>/dev/null)
if [ -n "$LOCKS" ]; then
  grep -H '^lock:' $LOCKS
  echo "Antes de qm unlock, confirma que no hay backup, snapshot ni migracion en curso"
else
  echo "Sin locks en VMs"
fi
echo "== Almacenamiento =="; pvesm status
echo "== Firewall =="; pve-firewall status
echo "== Ajustes en /etc/sysctl.conf (la 9 no los lee) =="
grep -v '^#' /etc/sysctl.conf 2>/dev/null | grep . || echo "Ninguno"
ls /etc/sysctl.d/
if command -v pve8to9 >/dev/null 2>&1; then
  echo "Nodo en la 8: antes del upgrade corre pve8to9 --full"
fi
echo "Listo: hoja de diagnostico. Guardala para comparar el dia que algo falle."
)""",
    ["El script no corre qm unlock: el lock se saca a mano, después de confirmar que no hay tareas en curso.",
     "Si hay ajustes en sysctl.conf, pasalos a un archivo en /etc/sysctl.d/ antes de reiniciar en la 9."]))
