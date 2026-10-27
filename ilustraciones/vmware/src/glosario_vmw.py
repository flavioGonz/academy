"""Genera ilustraciones/vmware/glosario-propuesta.json y lo prueba sobre una copia combinada del glosario.

  python3 glosario_vmw.py            # escribe la propuesta y valida la copia en /tmp/claude-0/glosario-vmware.json

terms: entradas nuevas completas. alias_agregar: alias nuevos para entradas existentes.
modificar: campos a reemplazar en entradas existentes. No toca site2/data/glosario.json.
Mismo esquema que glosario_pdx.py (Paradox).
"""
import json, subprocess, sys

V, SA, R = "Virtualización", "Servidores y almacenamiento", "Redes"


def T(id, term, aliases, cat, short, long, case=True, year=None):
    d = {"id": id, "term": term, "aliases": aliases, "cat": cat, "short": short, "long": long, "case": case}
    if year:
        d["year"] = year
    return d


TERMS = [
    T("esxi", "ESXi", ["VMware ESXi", "ESX", "ESX Server"], V,
      "El hipervisor tipo 1 de VMware: se instala directo sobre el servidor, sin otro sistema operativo debajo.",
      "ESX Server salió en 2001 y desde vSphere 5.0, en 2011, queda solo ESXi. Su núcleo es el VMkernel y trae sus propios drivers, por eso el hardware tiene que estar en la Broadcom Compatibility Guide. ESXi 8 pide 2 núcleos, 8 GB de RAM y un disco de arranque persistente; vSphere 8 pierde soporte general el 11 de octubre de 2027.", year=2001),
    T("vsphere", "vSphere", ["VMware vSphere"], V,
      "La plataforma de virtualización de VMware: los hosts ESXi más vCenter, que los gestiona juntos.",
      "Desde 2024 se vende solo por suscripción y por núcleo, dentro de VVF o VCF; Standard y Enterprise Plus llegan hasta 8.0 Update 3. vSphere 9 retira las baselines de Lifecycle Manager y usa hardware virtual versión 22."),
    T("vcenter", "vCenter", ["vCenter Server", "VCSA", "vCenter Server Appliance", "VirtualCenter"], V,
      "El servidor que gestiona varios hosts ESXi juntos y habilita clúster, vMotion, HA y DRS.",
      "Nació como VirtualCenter en 2003. Hoy se instala como appliance, la VCSA, que en vSphere 8 pide 14 GB de RAM en el tamaño Tiny. El acceso pasa por vCenter Single Sign-On, con el dominio vsphere.local por defecto. Viene incluido en las suscripciones; el ESXi gratuito no se puede gestionar con vCenter."),
    T("vmkernel", "VMkernel", [], V,
      "El núcleo de ESXi: maneja CPU, memoria, discos y placas de red y los reparte entre las VMs.",
      "Al no haber un sistema operativo debajo, el VMkernel trae sus propios drivers. Sus mensajes quedan en /var/run/log/vmkernel.log, y en esxtop KAVG mide el tiempo que una operación de disco pasa adentro de él."),
    T("vmk", "vmk", ["adaptador VMkernel", "adaptadores VMkernel", "vmk0", "vmk1"], V,
      "Adaptador VMkernel: una IP del propio host ESXi, para gestión, vMotion, almacenamiento o backup.",
      "La documentación pide uno por tipo de tráfico, cada uno en su port group, su VLAN y su subred. vmk0 es el de gestión que crea la instalación. Se prueban con vmkping -I vmkN, y con -d -s 8972 se verifica MTU 9000 de punta a punta.", case=False),
    T("vswitch", "vSwitch", ["vSwitch estándar", "switch virtual", "standard switch"], V,
      "El switch virtual adentro de un host ESXi: une las placas de las VMs y los vmk con las placas físicas.",
      "Cada host tiene sus vSwitch estándar; vSwitch0 lo crea la instalación con la red de gestión. Los uplinks son las vmnic y las VMs se conectan a port groups. Con dos uplinks a dos bocas distintas, un cable suelto no corta el servicio.", case=False),
    T("port-group", "port group", ["port groups", "grupo de puertos"], V,
      "El enchufe virtual de un vSwitch, con su VLAN ID: las VMs y los vmk se conectan ahí.",
      "VLAN ID 0 es sin etiqueta, la VLAN nativa del switch físico. El vSwitch pone y saca la etiqueta 802.1Q según el port group, así que la VM no necesita saber de VLAN. Management Network es el port group de gestión y se cambia solo con consola fuera de banda abierta.", case=False),
    T("vmnic", "vmnic", ["vmnic0", "vmnic2", "uplink del vSwitch"], V,
      "El nombre que ESXi le da a cada placa de red física del servidor: vmnic0, vmnic1 y así.",
      "Las vmnic son los uplinks de los vSwitch. esxcli network nic list las muestra con su estado y velocidad. Conviene que cada vSwitch tenga dos, conectadas a bocas distintas del switch físico.", case=False),
    T("datastore", "datastore", ["datastores", "datastore1"], V,
      "El almacenamiento donde ESXi guarda las VMs: una carpeta por VM con su configuración y sus discos.",
      "Puede ser VMFS, sobre un disco local o una LUN, o NFS, montado desde un NAS. esxcli storage filesystem list muestra cada uno con su tamaño y su libre. Si un datastore con discos thin se llena, las VMs se detienen.", case=False),
    T("vmfs", "VMFS", ["Virtual Machine File System", "VMFS-6"], V,
      "Virtual Machine File System: el sistema de archivos de ESXi, pensado para que varios hosts compartan el mismo disco.",
      "Se arma sobre un disco local o una LUN de una SAN o de iSCSI. Cada host bloquea solo los archivos de sus VMs, y eso es lo que permite vMotion y HA con almacenamiento compartido. La versión actual, VMFS-6, llegó con vSphere 6.5 en 2016."),
    T("nfs", "NFS", ["Network File System", "NFS 3", "NFS 4.1"], SA,
      "Network File System: el protocolo para compartir archivos por red que ESXi usa para montar datastores desde un NAS.",
      "Lo creó Sun Microsystems en 1984. ESXi soporta NFS 3 y 4.1, por un vmk de almacenamiento, y lo monta con esxcli storage nfs add. En NFS sin aceleración por hardware los discos de las VMs solo pueden ser thin.", year=1984),
    T("iscsi", "iSCSI", ["Internet SCSI", "Software iSCSI Adapter"], SA,
      "SCSI sobre IP: lleva comandos de disco por una red Ethernet para que funcione como una SAN.",
      "Se estandarizó en 2004. En ESXi se usa el adaptador de software sobre un vmk dedicado, con MTU 9000 de punta a punta si hay jumbo frames, y con dos placas se arma multipathing.", year=2004),
    T("scsi", "SCSI", ["Small Computer System Interface", "VirtIO SCSI"], SA,
      "Small Computer System Interface: la familia de comandos con la que un sistema habla con sus discos.",
      "En virtualización es también un tipo de controlador de disco virtual. Al migrar una VM Linux de ESXi a Proxmox VE se prueba primero el disco en VirtIO SCSI; iSCSI lleva estos comandos por la red."),
    T("sata", "SATA", ["Serial ATA"], SA,
      "Serial ATA: la interfaz de disco más común en PCs, también disponible como controlador de disco virtual.",
      "Al importar una VM Windows de ESXi a Proxmox VE se arranca con el disco en SATA, porque Windows ya trae ese driver; después de instalar los drivers VirtIO se cambia."),
    T("lun", "LUN", ["Logical Unit Number", "LUNs"], SA,
      "Logical Unit Number: un disco lógico que una SAN o un equipo iSCSI le presenta a un servidor.",
      "En ESXi una LUN se formatea con VMFS y queda como datastore, que varios hosts pueden compartir. En backups, el modo SAN usa un proxy físico que lee la LUN directo."),
    T("jumbo-frame", "jumbo frame", ["jumbo frames", "tramas jumbo", "MTU 9000"], R,
      "Trama Ethernet más grande que los 1500 bytes estándar, típicamente de 9000, usada en redes de almacenamiento.",
      "No es parte formal de Ethernet, así que hay que configurarla igual en cada salto: vmk, vSwitch, switch físico y NAS. Se prueba con vmkping -d -s 8972: 8972 de datos más 28 de encabezados dan 9000. Un solo salto en 1500 da cortes intermitentes.", case=False),
    T("snapshot", "snapshot", ["snapshots", "instantánea"], V,
      "Foto del estado de una VM para volver atrás: congela el disco base y manda lo nuevo a un disco delta.",
      "No es backup: si se pierde el disco base, el delta solo no restaura nada. La KB de Broadcom permite hasta 32 en cadena, pero recomienda 2 o 3 por VM y ninguno por más de 72 horas. Se crean y borran con vim-cmd vmsvc/snapshot.create y snapshot.removeall.", case=False),
    T("disco-delta", "disco delta", ["delta disk", "-000001.vmdk"], V,
      "El archivo que recibe todo lo que la VM escribe mientras existe un snapshot (-00000N.vmdk).",
      "Crece mientras el snapshot exista y depende del disco base. Los que deja un backup fallido pueden no verse en el Snapshot Manager: se buscan con find /vmfs/volumes/datastore1/ -name \"*-0000*.vmdk\".", case=False),
    T("consolidacion", "consolidación", ["consolidar", "consolidate", "disks consolidation"], V,
      "Fundir los discos delta de los snapshots con el disco base, para que la VM vuelva a tener un solo disco.",
      "Es lo que pasa al borrar un snapshot. No se cancela una consolidación en curso. El aviso \"Virtual machine disks consolidation is needed\" aparece cuando quedan deltas, por ejemplo de backups nocturnos fallidos.", case=False),
    T("thin", "thin provisioning", ["thin", "disco thin"], V,
      "Disco virtual que reserva solo lo que la VM escribió y crece a demanda hasta su tamaño máximo.",
      "Permite prometer más espacio del que tiene el datastore. Si el datastore se llena con las VMs corriendo, las VMs se detienen. ls -lh del -flat.vmdk muestra lo provisionado y du -h lo ocupado.", case=False),
    T("thick", "thick provisioning", ["thick", "thick lazy zeroed", "thick eager zeroed"], V,
      "Disco virtual que aparta todo su tamaño en el datastore desde que se crea.",
      "Lazy zeroed pone cada bloque en cero la primera vez que se usa; eager zeroed lo hace todo al crear, tarda más y es el que pide Fault Tolerance. Un disco se puede pasar de thin a thick con Storage vMotion.", case=False),
    T("ovf", "OVF", ["Open Virtualization Format", "OVA", ".ova", ".ovf"], V,
      "Open Virtualization Format: formato abierto de la DMTF para entregar VMs armadas; un OVA es lo mismo en un solo archivo.",
      "Los fabricantes de software de video, acceso o telefonía entregan sus servidores así. En ESXi entran por Deploy OVF Template, que crea la VM con su hardware; copiar el archivo al datastore no lo instala."),
    T("vmware-tools", "VMware Tools", [], V,
      "Drivers y servicios que van dentro de cada VM para que el host pueda administrarla bien.",
      "Traen el driver de balloon, permiten snapshots con quiesce y le dan a HA el latido de la VM. vim-cmd vmsvc/get.guest muestra toolsRunningStatus y toolsVersionStatus. Antes de migrar una VM a Proxmox VE se desinstalan.", case=False),
    T("balloon", "balloon", ["ballooning", "MCTL", "MCTLSZ", "driver de balloon"], V,
      "Mecanismo por el que el host le pide memoria a una VM a través de VMware Tools cuando le falta.",
      "En esxtop, pantalla m, la columna MCTLSZ muestra cuánto recuperó. Si MCTL? dice que no hay driver, falta instalar VMware Tools. Si el balloon y el swap del host (SWCUR) crecen, al host le falta memoria.", case=False),
    T("swcur", "SWCUR", ["swap del host"], V,
      "Columna de esxtop (pantalla m) con la memoria de una VM que el host mandó a swap.",
      "Junto con MCTLSZ, el balloon, indica que al host le falta memoria física. Que crezca es peor que el balloon: el swap del host va a disco."),
    T("vmotion", "vMotion", ["Storage vMotion"], V,
      "Mover una VM encendida de un host a otro sin apagarla, copiando su memoria y su estado.",
      "Salió en 2003. Copia la memoria en pasadas cada vez más chicas y cambia de host en un instante; si solo cambia el host, el disco tiene que estar en un datastore compartido. Viaja sin cifrar por un vmk de vMotion en una red solo de hosts. Storage vMotion mueve los discos.", year=2003),
    T("vsphere-ha", "vSphere HA", ["HA", "High Availability"], V,
      "Función del clúster que reinicia en otros hosts las VMs de un host que se cayó.",
      "Llegó en 2006. No evita el corte: lo acorta a lo que tardan las VMs en arrancar. Los hosts se vigilan entre sí y funciona aunque vCenter esté caído. Crear el clúster es libre; activar HA depende de la licencia.", year=2006),
    T("drs", "DRS", ["Distributed Resource Scheduler", "vSphere DRS"], V,
      "Distributed Resource Scheduler: reparte la carga de CPU y memoria del clúster moviendo VMs con vMotion.",
      "Necesita vCenter y licencia. Niveles Manual, Partially Automated y Fully Automated; en clústeres chicos conviene arrancar en manual o parcial y mirar qué recomienda. También vacía un host que entra en modo mantenimiento.", year=2006),
    T("evc", "EVC", ["Enhanced vMotion Compatibility"], V,
      "Enhanced vMotion Compatibility: iguala lo que ven las VMs en un clúster con CPUs de generaciones distintas.",
      "Se configura en el clúster para que vMotion funcione entre hosts con procesadores diferentes."),
    T("vadp", "VADP", ["vSphere APIs for Data Protection", "APIs de protección de datos"], V,
      "vSphere APIs for Data Protection: las APIs con las que los productos de backup copian VMs encendidas sin agente.",
      "Llegaron con vSphere 4 en 2009. Un job pide un snapshot, copia los bloques por NBD, HotAdd o SAN y borra el snapshot. El ESXi gratuito no las expone: ahí solo queda un agente dentro de cada VM.", year=2009),
    T("cbt", "CBT", ["Changed Block Tracking"], V,
      "Changed Block Tracking: registro de los bloques de un disco que cambiaron desde el último backup.",
      "Con CBT, un backup incremental de una VM copia solo lo cambiado en lugar del disco entero. Trabaja junto con VADP."),
    T("nbd", "NBD", ["NBDSSL", "modo red"], V,
      "Modo de transporte de backup que copia los discos por la red de gestión del host (NBDSSL es la variante cifrada).",
      "Es el más simple y el más lento: una guía vieja de Veeam habla de 10 a 20 MB/s en 1 GbE. Para restaurar rápido conviene un proxy virtual con HotAdd."),
    T("hotadd", "HotAdd", ["Hot-Add", "hot add"], V,
      "Modo de transporte de backup en el que un proxy virtual del mismo host monta el disco de la VM para copiarlo.",
      "Evita pasar por la red de gestión y acorta las restauraciones. No funciona con discos IDE.", case=False),
    T("vddk", "VDDK", ["Virtual Disk Development Kit"], V,
      "Virtual Disk Development Kit: la librería de VMware para leer y escribir discos de VMs, que usan herramientas de migración y backup.",
      "En agosto y septiembre de 2026 Broadcom retiró sus descargas públicas. El importador ESXi de Proxmox VE no depende de ella; para productos de backup, ninguna fuente leída confirma el impacto."),
    T("regla-3-2-1", "regla 3-2-1", ["3-2-1"], SA,
      "Tres copias de los datos, en dos medios distintos, con una fuera del sitio.",
      "Cubre la pérdida de un equipo, de un medio o del sitio entero. No reemplaza la prueba: un backup cuenta cuando se restauró al menos una vez en un lugar aislado y se sabe cuánto tardó.", case=False),
    T("vvf", "VVF", ["vSphere Foundation", "VMware vSphere Foundation"], V,
      "VMware vSphere Foundation: la suscripción de Broadcom con vSphere, vCenter y una base de vSAN.",
      "Se licencia por núcleo físico con mínimo de 16 por CPU. Incluye 0,25 TiB de vSAN por núcleo. Es uno de los caminos que Broadcom recomienda al terminar vSphere 8."),
    T("vcf", "VCF", ["VMware Cloud Foundation", "Cloud Foundation"], V,
      "VMware Cloud Foundation: la suscripción con el stack completo de Broadcom, con NSX, vSAN y automatización.",
      "Se licencia por núcleo físico con mínimo de 16 por CPU e incluye 1 TiB de vSAN por núcleo. VCF 9.0 salió el 17 de junio de 2025 con ESXi y vCenter 9.0."),
    T("nsx", "NSX", ["VMware NSX"], V,
      "La plataforma de redes y seguridad virtuales de VMware, incluida en VCF.",
      "Al decidir entre renovar o migrar, se pregunta si el cliente usa de verdad NSX, vSAN o DRS: si solo usa el hipervisor, la cuenta cambia."),
    T("vsan", "vSAN", ["VMware vSAN"], V,
      "El almacenamiento de VMware que junta los discos locales de los hosts en un datastore compartido.",
      "VVF incluye 0,25 TiB por núcleo y VCF 1 TiB por núcleo. El importador ESXi de Proxmox VE no puede importar discos que estén en vSAN.", case=False),
    T("compatibility-guide", "Broadcom Compatibility Guide", ["Compatibility Guide", "HCL", "Hardware Compatibility List"], SA,
      "La lista oficial de CPU, NIC, controladoras y servidores soportados en cada versión de ESXi (la ex HCL).",
      "Es la única forma de tener una configuración soportada. ESXi 8 dejó afuera CPUs como Sandy Bridge y Haswell, y ESXi 9 deja afuera Skylake y anteriores. Parámetros como allowLegacyCPU fuerzan la instalación, solo en laboratorio."),
    T("dcui", "DCUI", ["Direct Console User Interface"], V,
      "Direct Console User Interface: la pantalla de consola de un host ESXi, en el monitor del servidor o por iLO o iDRAC.",
      "Con F2 > Configure Management Network se elige la placa, la VLAN, la IP fija, el DNS y el hostname. Es el camino para recuperar un host que quedó sin acceso por la red."),
    T("osdata", "OSDATA", ["ESX-OSData"], V,
      "La partición de ESXi donde van el scratch y los logs, en el disco de arranque.",
      "Si el host arranca de SD o USB, OSDATA se crea en un disco en memoria y lo que guarda se pierde al reiniciar; por eso ESXi 8 pide un disco persistente de 32 GB como mínimo y 128 GB como óptimo."),
    T("uefi", "UEFI", ["Unified Extensible Firmware Interface"], SA,
      "Unified Extensible Firmware Interface: el firmware de arranque que reemplazó al BIOS clásico.",
      "ESXi 8 recomienda arrancar en modo UEFI. En el mismo menú se habilitan VT-x o AMD-V y NX/XD."),
    T("raid", "RAID", ["RAID 1", "Redundant Array of Independent Disks"], SA,
      "Redundant Array of Independent Disks: varios discos que la controladora presenta como uno, con redundancia.",
      "En RAID 1 dos discos guardan lo mismo: si uno falla, el otro sigue. Es lo que se recomienda para el disco de arranque de ESXi."),
    T("vt-x", "VT-x", ["VT", "AMD-V", "Intel VT", "virtualización por hardware"], SA,
      "Las extensiones de virtualización de Intel (VT-x) y AMD (AMD-V) dentro del procesador.",
      "Llegaron entre 2005 y 2006. Con ellas el código de las VMs corre directo en la CPU y solo las instrucciones sensibles pasan por el hipervisor. ESXi 8 las exige habilitadas en BIOS, junto con NX/XD."),
    T("nx-xd", "NX/XD", ["NX", "XD", "No-Execute", "Execute Disable"], SA,
      "Bit de protección de memoria del procesador (NX en AMD, XD en Intel) que ESXi exige habilitado en BIOS.",
      "Marca zonas de memoria como no ejecutables. Si está deshabilitado, el instalador de ESXi 8 no sigue."),
    T("vlcm", "vSphere Lifecycle Manager", ["vLCM", "Lifecycle Manager", "Update Manager"], V,
      "La herramienta de vCenter que actualiza los hosts ESXi de un clúster llevándolos a una imagen.",
      "Llegó con vSphere 7 en 2020 y reemplazó a Update Manager; en vSphere 9 se retiran las baselines y queda el modelo de imágenes. Sus pasos: Check Compliance, Remediation Pre-check, Stage y Remediate.", year=2020),
    T("modo-mantenimiento", "modo mantenimiento", ["maintenance mode", "maintenanceMode"], V,
      "Estado de un host ESXi sin VMs corriendo, listo para parchearlo o repararlo.",
      "Con DRS, al entrar en mantenimiento las VMs se mueven solas con vMotion; sin DRS se mueven a mano o se apagan. Por esxcli: esxcli system maintenanceMode set -e true.", case=False),
    T("esxtop", "esxtop", [], V,
      "El monitor de rendimiento de ESXi por SSH: CPU, memoria, disco y red de cada VM y del host.",
      "Teclas c, m, u, v y n para cada pantalla, distinguiendo mayúsculas. El modo batch, esxtop -b -a -d 5 -n 12, guarda un minuto en CSV para comparar con un día normal.", case=False),
    T("rdy", "%RDY", ["RDY", "CPU ready", "ready time"], V,
      "Columna de esxtop con el tiempo que una VM estuvo lista para correr esperando una CPU física libre.",
      "Alto indica fila de CPU: hay más vCPU que núcleos disponibles. Agregar vCPU a esa VM suele empeorarlo. No hay umbral universal: se compara con un día normal del mismo host."),
    T("used", "%USED", ["USED"], V,
      "Columna de esxtop (pantalla c) con el uso de CPU física de cada VM.",
      "Se lee junto con %RDY: una VM puede usar poco y esperar mucho si el host está saturado."),
    T("davg", "DAVG", ["DAVG/cmd"], V,
      "Columna de esxtop con la latencia del dispositivo de almacenamiento, en milisegundos por operación.",
      "Si DAVG es alto, el problema está en el storage: controladora, red de almacenamiento, NAS o SAN. GAVG = DAVG + KAVG."),
    T("kavg", "KAVG", ["KAVG/cmd"], V,
      "Columna de esxtop con el tiempo que una operación de disco pasa dentro del VMkernel del host.",
      "Debería estar cerca de cero. Si sube, hay encolamiento en el host y no en el almacenamiento."),
    T("gavg", "GAVG", ["GAVG/cmd"], V,
      "Columna de esxtop con la latencia de disco que siente la VM: la suma de DAVG y KAVG.",
      "Separar GAVG en sus dos partes evita culpar al host por un almacenamiento lento, o al revés."),
    T("drptx", "%DRPTX", ["DRPTX", "%DRPRX", "DRPRX"], V,
      "Columnas de esxtop (pantalla n) con el porcentaje de paquetes descartados al transmitir y al recibir.",
      "Valores mayores a cero en una VM o un vmk piden revisar la placa física, el vSwitch y el switch."),
    T("vmkernel-log", "vmkernel.log", ["vmkwarning.log", "hostd.log", "/var/run/log"], V,
      "Los logs del host ESXi, en /var/run/log: vmkernel.log del núcleo, vmkwarning.log con sus advertencias y hostd.log del agente.",
      "Son el primer lugar para buscar errores de discos, rutas, red o drivers. En vCenter el equivalente es vpxd. Si el host arranca de SD o USB, viven en memoria y se pierden al reiniciar.", case=False),
    T("vsphere-local", "vsphere.local", ["administrator@vsphere.local"], V,
      "El dominio por defecto de vCenter Single Sign-On; administrator@vsphere.local es su administrador inicial.",
      "Al desplegar vCenter solo ese usuario puede entrar: es la llave maestra. Va al gestor de contraseñas de la empresa y cada técnico usa su propio usuario con un rol acotado. El dominio se elige al instalar.", case=False),
    T("vtpm", "vTPM", ["TPM virtual"], V,
      "Chip TPM virtual de una VM, que por ejemplo usa BitLocker en Windows para guardar sus claves.",
      "No se migra de VMware a Proxmox VE: antes de importar una VM Windows con BitLocker hay que tener a mano sus claves de recuperación."),
    T("erp", "ERP", ["Enterprise Resource Planning"], "Web e integración",
      "Enterprise Resource Planning: el sistema de gestión de una empresa (facturación, stock, contabilidad).",
      "En los clientes chicos suele ser una de las pocas VMs críticas junto al grabador de video: entra en la cuenta de qué funciones de VMware se usan de verdad."),
    T("tarjeta-sd", "tarjeta SD", ["SD", "microSD", "tarjeta microSD"], SA,
      "Memoria flash en formato tarjeta. En servidores se usaba para arrancar ESXi.",
      "En ESXi 8 SD y USB quedan solo para el arranque y están en retirada: OSDATA no puede ir ahí, y los logs se pierden al reiniciar.", case=False),
    T("ide", "IDE", ["Integrated Drive Electronics"], SA,
      "Integrated Drive Electronics: interfaz de disco vieja, que también existe como controlador de disco virtual.",
      "En backups de VMware, el modo HotAdd no funciona con discos IDE: esas VMs se copian por NBD o se pasan a otro controlador."),
    T("dmtf", "DMTF", ["Distributed Management Task Force"], "Normas",
      "Distributed Management Task Force: organización que publica estándares de gestión de sistemas, como OVF.",
      "Gracias a OVF, un fabricante puede entregar una VM armada que se importa en distintos hipervisores."),
    T("umds", "UMDS", ["Update Manager Download Service"], V,
      "Update Manager Download Service: baja los parches de VMware en un equipo con internet para usarlos donde vCenter no tiene salida.",
      "Con Lifecycle Manager, si vCenter no tiene internet, los paquetes se bajan con UMDS o se importan a mano."),

]

ALIAS = {"sso": ["vCenter Single Sign-On"]}
MOD_HIPERVISOR = " Tipo 1 (ESXi, Proxmox VE) va directo sobre el hardware; tipo 2 corre arriba de un sistema operativo, como un programa."

GLOS = "/home/claude/ies-training/site2/data/glosario.json"
OUT = "/home/claude/ies-training/ilustraciones/vmware/glosario-propuesta.json"
COMB = "/tmp/claude-0/glosario-vmware.json"

g = json.load(open(GLOS, encoding="utf-8"))
by = {t["id"]: t for t in g["terms"]}
hip = by["hipervisor"]["long"]
P = {
    "nota": "Propuesta para el curso VMware. terms: entradas nuevas completas. alias_agregar: alias nuevos para entradas existentes. modificar: campos a reemplazar en entradas existentes. Probada sobre una copia combinada con glosario_check.py. Categorías nuevas: Virtualización y Servidores y almacenamiento.",
    "terms": TERMS,
    "alias_agregar": ALIAS,
    "modificar": {"hipervisor": {"long": hip if MOD_HIPERVISOR.strip() in hip else hip + MOD_HIPERVISOR}},
}
json.dump(P, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
dup = [t["id"] for t in TERMS if t["id"] in by]
if dup:
    sys.exit(f"ids que ya existen en el glosario: {dup}")
n0 = len(g["terms"])
g["terms"] += TERMS
for k, al in ALIAS.items():
    by[k]["aliases"] += [a for a in al if a not in by[k]["aliases"]]
for k, ch in P["modificar"].items():
    by[k].update(ch)
json.dump(g, open(COMB, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
s = json.dumps(P, ensure_ascii=False)
print("ok", OUT, len(TERMS), "entradas nuevas sobre", n0, "· guiones largos:", "—" in s or "–" in s)
r = subprocess.run([sys.executable, "/home/claude/ies-training/tools/glosario_check.py", "vmware", "--glosario", COMB], capture_output=True, text=True)
print(r.stdout[-2500:], r.stderr[-1500:], "exit", r.returncode)
