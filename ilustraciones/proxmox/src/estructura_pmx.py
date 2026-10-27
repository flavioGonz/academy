"""Genera /home/claude/ies-training/ilustraciones/proxmox/estructura.json."""
import json

E = {
 "curso": {
  "objetivo": "Al terminar el curso vas a poder dejar un host Proxmox VE 9 con repositorio, red y almacenamiento bien elegidos, crear VMs y contenedores con la configuración correcta y en minutos, respaldar con vzdump y Proxmox Backup Server con restores probados, armar un clúster con quórum real y alta disponibilidad, cerrar el acceso con usuarios, 2FA y firewall, y diagnosticar o actualizar un clúster sin sustos.",
  "recorrido": "Arrancás por el host: el repositorio y la forma de actualizar, la red en capas con VLAN y el disco según el hardware. Sobre ese host creás invitados: VMs con VirtIO y guest agent, plantillas con cloud-init para clonar en minutos, y contenedores no privilegiados para lo liviano. Con invitados que importan, aprendés a respaldarlos de verdad: vzdump con restore de prueba y después PBS con su mantenimiento y permisos. Cerrás con lo que más se vende y más se rompe: clúster y quórum, migración y HA con fencing, el acceso blindado y el diagnóstico y upgrade de un clúster en producción."
 },
 "modulos": [
  {"title": "Un host bien parado",
   "why": "Casi todos los problemas de soporte nacen en la instalación. Va de lo que se decide en los primeros minutos (de dónde salen los paquetes) a lo más caro de cambiar después (el disco). Termina con un host actualizado, con la red lista para VLAN y el almacenamiento elegido con criterio.",
   "objetivos": [
    "Al terminar el módulo vas a poder elegir el repositorio de Proxmox con el cliente y actualizar siempre con apt full-upgrade.",
    "Al terminar el módulo vas a poder armar la red del host en capas, con bond y un bridge VLAN-aware, sin quedarte sin acceso.",
    "Al terminar el módulo vas a poder elegir entre LVM-thin y ZFS según discos, controladora y RAM, y revisar el ARC."
   ],
   "lessons": ["1", "2", "3"]},
  {"title": "Máquinas y contenedores",
   "why": "Con el host en orden, el trabajo de todos los días es crear invitados. Va de la VM bien armada a la plantilla que la reproduce en un minuto, y cierra con el contenedor, la alternativa liviana. Termina con una plantilla Debian 13, un clon con su IP y un contenedor no privilegiado.",
   "objetivos": [
    "Al terminar el módulo vas a poder crear VMs con VirtIO SCSI, red VirtIO y guest agent probado, y elegir el tipo de CPU.",
    "Al terminar el módulo vas a poder armar una plantilla desde una imagen cloud y clonar VMs con usuario, clave e IP por cloud-init.",
    "Al terminar el módulo vas a poder crear contenedores no privilegiados y decidir cuándo un servicio va en VM y cuándo en LXC."
   ],
   "lessons": ["4", "5", "6"]},
  {"title": "Backups que restauran",
   "why": "Un servidor sin backup probado es una apuesta. Primero el backup completo con vzdump y el restore de prueba, después Proxmox Backup Server con deduplicación, mantenimiento y permisos que un atacante no pueda usar para borrar. Termina con un PBS programado y un restore medido.",
   "objetivos": [
    "Al terminar el módulo vas a poder hacer backups con vzdump en el modo correcto y restaurarlos a un VMID nuevo sin chocar con la original.",
    "Al terminar el módulo vas a poder programar prune, garbage collection y verify en PBS y explicar qué hace cada uno.",
    "Al terminar el módulo vas a poder conectar Proxmox VE a PBS con un token que puede escribir backups pero no borrarlos."
   ],
   "lessons": ["7", "8"]},
  {"title": "Clúster, acceso y rescate",
   "why": "El clúster y la alta disponibilidad son lo que más se vende y lo que más se rompe. Va del quórum a la HA con fencing, sigue con quién entra y cómo, y cierra con el diagnóstico y el upgrade de un clúster en producción.",
   "objetivos": [
    "Al terminar el módulo vas a poder armar un clúster con quórum real, con QDevice cuando son dos nodos.",
    "Al terminar el módulo vas a poder migrar en vivo, poner VMs en HA y desarmar la HA para un mantenimiento de red.",
    "Al terminar el módulo vas a poder cerrar el acceso con usuarios, 2FA y firewall, y diagnosticar o actualizar un clúster en orden."
   ],
   "lessons": ["9", "10", "11", "12"]}
 ],
 "lecciones": {
  "1": {"objetivos": [
         "Al terminar vas a poder leer la versión real del host con pveversion -v.",
         "Al terminar vas a poder dejar un solo repositorio de Proxmox habilitado, elegido con el cliente.",
         "Al terminar vas a poder actualizar con apt full-upgrade y explicar por qué no apt upgrade."],
        "sigue": "Con el host al día, la próxima arma su red: placas, bond y un bridge que lleve todas las VLAN del cliente.",
        "requisitos": []},
  "2": {"objetivos": [
         "Al terminar vas a poder armar la red en el orden placas, bond y bridge.",
         "Al terminar vas a poder marcar vmbr0 como VLAN aware y poner el tag en la placa de cada VM.",
         "Al terminar vas a poder confirmar el tag con bridge vlan show y aplicar cambios sin cortar la gestión."],
        "conecta": "En Repos en orden dejaste el host actualizado. Acá le das la red por la que van a salir sus VMs.",
        "sigue": "Con la red lista, la próxima mira el disco: dónde van a vivir esas VMs y por qué se elige una sola vez.",
        "requisitos": ["1"]},
  "3": {"objetivos": [
         "Al terminar vas a poder leer pvesm status y reconocer local, local-lvm y local-zfs.",
         "Al terminar vas a poder elegir entre LVM-thin y ZFS según controladora, discos y RAM.",
         "Al terminar vas a poder calcular el límite del ARC y compararlo con lo configurado."],
        "conecta": "En Repos en orden viste que el instalador decide muchas cosas. Acá está la más cara de cambiar: el almacenamiento.",
        "sigue": "El host quedó bien parado. El próximo módulo crea invitados, empezando por una VM bien armada.",
        "requisitos": ["1"]},
  "4": {"objetivos": [
         "Al terminar vas a poder crear una VM con VirtIO SCSI single, IO Thread y placa VirtIO.",
         "Al terminar vas a poder activar el guest agent y probarlo con qm agent ping.",
         "Al terminar vas a poder elegir el tipo de CPU según si la VM va a migrar, e instalar virtio-win en Windows."],
        "conecta": "En Puente VLAN-aware pusiste el tag en la placa de una VM y en Disco con criterio elegiste dónde vive su disco. Acá armás el resto de esa VM.",
        "sigue": "Con una VM bien armada, la próxima la convierte en plantilla para tener las siguientes en un minuto.",
        "requisitos": ["2", "3"]},
  "5": {"objetivos": [
         "Al terminar vas a poder crear una plantilla desde una imagen cloud con disco importado y unidad cloud-init.",
         "Al terminar vas a poder clonar una VM full con usuario, clave SSH e IP fija.",
         "Al terminar vas a poder decidir entre full clone y linked clone."],
        "conecta": "En VM bien armada elegiste VirtIO y el agente. La plantilla nace con esas mismas opciones.",
        "sigue": "No todo necesita una VM. La próxima arma un contenedor no privilegiado para los servicios livianos.",
        "requisitos": ["4"]},
  "6": {"objetivos": [
         "Al terminar vas a poder bajar una plantilla con pveam y crear un contenedor no privilegiado.",
         "Al terminar vas a poder leer el uid_map y explicar por qué el root de adentro no es root afuera.",
         "Al terminar vas a poder decidir cuándo un servicio va en LXC y cuándo, como Docker, en VM."],
        "conecta": "En VM bien armada viste que una VM trae su propio kernel. El contenedor usa el del host, y de ahí salen sus ventajas y sus límites.",
        "sigue": "Ya tenés invitados que importan. El próximo módulo los respalda, empezando por un backup que se restaura de verdad.",
        "requisitos": ["2", "3"]},
  "7": {"objetivos": [
         "Al terminar vas a poder hacer un backup con vzdump en modo snapshot o stop.",
         "Al terminar vas a poder restaurarlo a un VMID nuevo con la placa desconectada y medir cuánto tardó.",
         "Al terminar vas a poder explicar por qué un snapshot no es un backup."],
        "conecta": "En VM bien armada activaste el guest agent. Acá es el que congela el disco para que el backup salga consistente.",
        "sigue": "vzdump copia todo cada vez. La próxima pasa a Proxmox Backup Server, que guarda solo lo nuevo.",
        "requisitos": ["4"]},
  "8": {"objetivos": [
         "Al terminar vas a poder programar prune, garbage collection y verify en un datastore.",
         "Al terminar vas a poder crear un usuario con token y rol DatastoreBackup.",
         "Al terminar vas a poder agregar el PBS en Proxmox VE y comprobar un backup de prueba."],
        "conecta": "En Backup que restaura los backups eran archivos completos. Acá cada backup es un índice de trozos compartidos.",
        "sigue": "Los backups están cubiertos. El último módulo arma el clúster, empezando por los votos que lo mantienen en pie.",
        "requisitos": ["7"]},
  "9": {"objetivos": [
         "Al terminar vas a poder crear un clúster con pvecm y unir un nodo vacío.",
         "Al terminar vas a poder leer pvecm status y decir si hay quórum y por qué.",
         "Al terminar vas a poder sumar un QDevice a un clúster de dos nodos."],
        "conecta": "En Puente VLAN-aware armaste la red del host. Corosync necesita la suya, propia y de baja latencia.",
        "sigue": "Con tres votos, la próxima mueve VMs entre nodos y las pone en alta disponibilidad.",
        "requisitos": ["2"]},
  "10": {"objetivos": [
          "Al terminar vas a poder migrar una VM en vivo, con disco compartido o local.",
          "Al terminar vas a poder poner una VM bajo HA y leer la línea de fencing de ha-manager status.",
          "Al terminar vas a poder desarmar y volver a armar la HA para un mantenimiento de red."],
         "conecta": "En Tres votos viste que sin quórum el clúster se queda quieto. La HA depende de eso, y en Disco con criterio elegiste si el disco puede estar en otro nodo.",
         "sigue": "El clúster funciona. La próxima cierra quién puede entrar y desde dónde.",
         "requisitos": ["9", "3"]},
  "11": {"objetivos": [
          "Al terminar vas a poder crear usuarios personales con el rol justo y comprobar sus permisos.",
          "Al terminar vas a poder configurar 2FA con claves de recuperación.",
          "Al terminar vas a poder habilitar el firewall en orden, sin quedarte afuera."],
         "conecta": "En PBS sin sorpresas le diste a Proxmox VE un token que no puede borrar. Acá aplicás la misma idea a las personas.",
         "sigue": "Con el acceso cerrado, la última lección arma tu hoja de diagnóstico y el plan para el upgrade mayor.",
         "requisitos": ["1"]},
  "12": {"objetivos": [
          "Al terminar vas a poder diagnosticar en orden: quórum, logs, locks, almacenamiento y firewall.",
          "Al terminar vas a poder destrabar un lock sabiendo por qué quedó.",
          "Al terminar vas a poder planificar un upgrade de 8 a 9 nodo por nodo y mover los ajustes de sysctl.conf."],
         "conecta": "En HA con fencing migraste VMs en vivo. Es la herramienta que hace posible actualizar un clúster de a un nodo.",
         "cierre": "Con esto recorriste Proxmox VE de punta a punta: del primer apt update al clúster con HA. Repositorio decidido, red en capas, disco con criterio, invitados desde plantilla, backups restaurados, quórum real y una hoja de diagnóstico son tu kit para el próximo servidor de un cliente.",
         "requisitos": ["9", "10", "7"]}
 },
 "avisos": [
  {"id": "10", "archivo": "card.md",
   "texto": "En el clúster `lab` de la lección 9 (con QDevice)",
   "sugerencia": "En el clúster `lab` de Tres votos (con QDevice)"}
 ]
}
out = "/home/claude/ies-training/ilustraciones/proxmox/estructura.json"
json.dump(E, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
s = json.dumps(E, ensure_ascii=False)
print("ok", out, "guiones largos:", "—" in s or "–" in s)
