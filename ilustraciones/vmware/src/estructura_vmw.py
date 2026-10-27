"""Genera /home/claude/ies-training/ilustraciones/vmware/estructura.json (mismo esquema que estructura_pdx.py).

El orden de las lecciones no cambia (1 a 12): las referencias "lección uno", "lección 3" y "lección 7"
de las charlas y laboratorios siguen siendo correctas, así que no hace falta ningún aviso de renumeración.
"""
import json

E = {
 "curso": {
  "objetivo": "Al terminar el curso vas a poder leer qué licencia y qué hardware tiene un cliente con VMware, dejar un host ESXi 8 bien instalado con su red, sus vmk y su almacenamiento, operar VMs, snapshots y backups con criterio, moverte en vCenter con permisos nominales, clúster, vMotion, HA y parches, diagnosticar lentitud con esxtop y los logs, y darle al cliente un panorama honesto de renovar o migrar.",
  "recorrido": "Arrancás por el host: qué licencia tiene, si el hardware sirve, cómo se instala y cómo quedan su red y su almacenamiento. Con el host bien parado, pasás a lo que se toca todas las semanas: VMs bien armadas, snapshots con fecha y backups que se restauran. Después sumás vCenter y varios hosts: usuarios y roles, clúster con vMotion y HA, y parches sin cortar. Cerrás con el diagnóstico de rendimiento y con la decisión que hoy preguntan todos los clientes: seguir con VMware o irse."
 },
 "modulos": [
  {"title": "El host bien parado",
   "why": "Antes de tocar una VM hay que saber qué licencia tiene el cliente, si el servidor sirve y cómo quedan la red y el almacenamiento del host, que es donde se cometen los errores que dejan un sitio sin gestión. Va del papel (licencia y compatibilidad) a la red y los datastores. Termina con un host instalado, con vSwitch, VLAN, vmk y un NFS montado.",
   "objetivos": [
    "Al terminar el módulo vas a poder identificar la licencia y la versión de un host y calcular sus núcleos licenciables.",
    "Al terminar el módulo vas a poder validar el hardware, instalar ESXi 8 en un disco persistente y dejar la red de gestión desde la DCUI.",
    "Al terminar el módulo vas a poder armar vSwitch, port groups con VLAN, un vmk por tráfico y un datastore NFS probado con vmkping."
   ],
   "lessons": ["1", "2", "3", "4"]},
  {"title": "VMs con red de seguridad",
   "why": "Es el trabajo de soporte de todas las semanas: recibir o crear VMs, sacar un snapshot antes de un cambio y confiar en el backup. Va de la VM bien armada al snapshot con fecha y termina en la prueba que cierra el círculo: restaurar en un lugar aislado y saber cuánto tarda.",
   "objetivos": [
    "Al terminar el módulo vas a poder instalar appliances con Deploy OVF Template, verificar VMware Tools y vigilar el crecimiento de los discos thin.",
    "Al terminar el módulo vas a poder usar snapshots con fecha de borrado y encontrar deltas olvidados.",
    "Al terminar el módulo vas a poder explicar VADP, CBT y los modos de transporte, y probar un backup con una restauración aislada."
   ],
   "lessons": ["5", "6", "7"]},
  {"title": "Varios hosts con vCenter",
   "why": "Cuando el cliente pasa de un servidor a varios aparece vCenter, y con él el clúster, vMotion, HA y los parches coordinados. Primero se ordena quién entra y con qué permisos; después se mueve y se protege; al final se actualiza sin cortar.",
   "objetivos": [
    "Al terminar el módulo vas a poder crear usuarios en vsphere.local y darles roles acotados sobre objetos del inventario.",
    "Al terminar el módulo vas a poder explicar y probar vMotion, HA y DRS, y decirle al cliente qué protege cada uno.",
    "Al terminar el módulo vas a poder parchear con Lifecycle Manager o con esxcli, con backup antes y modo mantenimiento."
   ],
   "lessons": ["8", "9", "10"]},
  {"title": "Diagnóstico y decisión",
   "why": "Las dos preguntas que más se escuchan después de la entrega: \"anda lento\" y \"¿nos vamos de VMware?\". Va de medir con esxtop y los logs a armar una decisión con números y un piloto.",
   "objetivos": [
    "Al terminar el módulo vas a poder separar un problema de CPU, memoria, almacenamiento o red con esxtop y vmkernel.log.",
    "Al terminar el módulo vas a poder decidir con números entre renovar y migrar, e importar una VM a Proxmox VE en frío con vuelta atrás."
   ],
   "lessons": ["11", "12"]}
 ],
 "lecciones": {
  "1": {"objetivos": [
         "Al terminar vas a poder reconocer en el Host Client qué licencia tiene un host y qué funciones habilita.",
         "Al terminar vas a poder calcular los núcleos licenciables con el mínimo de 16 por CPU.",
         "Al terminar vas a poder completar la ficha del cliente con versión, licencia, núcleos y fin de soporte."],
        "sigue": "Con la licencia clara, la próxima mira el hardware: si el servidor está en la lista y cómo se instala ESXi 8.",
        "requisitos": []},
  "2": {"objetivos": [
         "Al terminar vas a poder validar CPU, NICs y controladora en la Broadcom Compatibility Guide.",
         "Al terminar vas a poder preparar el BIOS y bootear el instalador para ver qué detecta sin instalar.",
         "Al terminar vas a poder instalar en un disco persistente y dejar IP, DNS y hostname desde la DCUI."],
        "conecta": "En Qué licencia hay viste qué versión puede usar el cliente. Acá revisás si su hardware la soporta.",
        "sigue": "Con el host instalado y accesible, la próxima arma su red: vSwitch, port groups y VLAN.",
        "requisitos": ["1"]},
  "3": {"objetivos": [
         "Al terminar vas a poder crear un vSwitch estándar con dos uplinks.",
         "Al terminar vas a poder crear port groups con VLAN ID y configurar el troncal del switch físico.",
         "Al terminar vas a poder cambiar la red de gestión sin quedarte afuera."],
        "conecta": "En ESXi bien instalado dejaste la red de gestión desde la DCUI. Acá sumás la red de las VMs sin tocar esa.",
        "sigue": "Las VMs ya tienen red. La próxima le da al host sus propias IPs para almacenamiento y vMotion.",
        "requisitos": ["2"]},
  "4": {"objetivos": [
         "Al terminar vas a poder crear un vmk por tipo de tráfico, en su VLAN y su subred.",
         "Al terminar vas a poder montar un datastore NFS y distinguirlo de uno VMFS.",
         "Al terminar vas a poder probar jumbo frames de punta a punta con vmkping."],
        "conecta": "En Red del host creaste port groups para VMs. Acá creás uno de almacenamiento y le colgás un vmk.",
        "sigue": "El host quedó bien parado. El próximo módulo pone VMs arriba, empezando por cómo se arman bien.",
        "requisitos": ["3"]},
  "5": {"objetivos": [
         "Al terminar vas a poder instalar un appliance .ova con Deploy OVF Template.",
         "Al terminar vas a poder verificar VMware Tools en cada VM.",
         "Al terminar vas a poder elegir thin o thick y calcular cuánto pueden crecer los discos de un datastore."],
        "conecta": "En VMkernel y almacenamiento montaste los datastores. Acá los llenás de VMs sin quedarte sin espacio.",
        "sigue": "Con las VMs armadas, la próxima aprende a cambiarles algo con vuelta atrás: el snapshot.",
        "requisitos": ["4"]},
  "6": {"objetivos": [
         "Al terminar vas a poder explicar por qué un snapshot no es backup.",
         "Al terminar vas a poder crear, revisar y borrar snapshots con fecha de borrado en el nombre.",
         "Al terminar vas a poder encontrar deltas huérfanos y saber cuándo hace falta consolidar."],
        "conecta": "En VMs bien armadas viste los archivos de un disco. Acá aparece el delta, el archivo que crece con cada snapshot.",
        "sigue": "Si el snapshot no es backup, ¿qué sí? La próxima arma y prueba un backup que restaura.",
        "requisitos": ["5"]},
  "7": {"objetivos": [
         "Al terminar vas a poder explicar cómo un job con VADP y CBT usa un snapshot para copiar una VM encendida.",
         "Al terminar vas a poder distinguir los modos NBD, HotAdd y SAN y encontrar cuál usó un job.",
         "Al terminar vas a poder restaurar una VM en un port group aislado y anotar cuánto tardó."],
        "conecta": "En Snapshots con fecha viste que un backup fallido deja snapshots colgados. Acá ves de dónde salen y cómo se evita.",
        "sigue": "Con un host que se respalda y restaura, el próximo módulo suma vCenter y varios hosts, empezando por quién entra.",
        "requisitos": ["6", "3"]},
  "8": {"objetivos": [
         "Al terminar vas a poder explicar qué agrega vCenter y cuánto pide la VCSA.",
         "Al terminar vas a poder crear usuarios en vsphere.local y guardar la llave maestra.",
         "Al terminar vas a poder clonar un rol y asignarlo con propagación sobre una carpeta."],
        "conecta": "En Qué licencia hay viste que vCenter viene incluido en la suscripción y que el ESXi gratuito no lo admite.",
        "sigue": "Con vCenter y permisos en orden, la próxima arma el clúster y prueba vMotion y HA.",
        "requisitos": ["1"]},
  "9": {"objetivos": [
         "Al terminar vas a poder crear un clúster y activar HA y DRS cuando la licencia lo permite.",
         "Al terminar vas a poder hacer un vMotion y medir cuánto se nota con un ping continuo.",
         "Al terminar vas a poder explicarle al cliente que HA reinicia en otro host y no evita el corte."],
        "conecta": "En VMkernel y almacenamiento dejaste un vmk de vMotion en su VLAN y un datastore compartido: acá se usan los dos.",
        "sigue": "Con el clúster andando, la próxima lo actualiza de a un host sin cortar las VMs.",
        "requisitos": ["8", "4"]},
  "10": {"objetivos": [
          "Al terminar vas a poder recorrer las cuatro operaciones de Lifecycle Manager.",
          "Al terminar vas a poder actualizar un host suelto con esxcli, simulando primero con --dry-run.",
          "Al terminar vas a poder planificar una actualización con backup, staging y modo mantenimiento."],
         "conecta": "En Clúster y vMotion viste cómo se mueven las VMs entre hosts. Acá eso es lo que deja parchear sin cortar.",
         "sigue": "La infraestructura quedó al día. El último módulo trata lo que pasa después: diagnosticar y decidir.",
         "requisitos": ["9", "7"]},
  "11": {"objetivos": [
          "Al terminar vas a poder recorrer esxtop y leer %RDY, balloon, swap, DAVG, KAVG y paquetes descartados.",
          "Al terminar vas a poder grabar un minuto en modo batch y dejar una línea base del cliente.",
          "Al terminar vas a poder buscar errores en vmkernel.log y vmkwarning.log."],
         "conecta": "En ESXi bien instalado viste que sin disco persistente los logs se pierden; en VMs bien armadas, que sin Tools no hay balloon. Acá los dos se ven en números.",
         "sigue": "Con el diagnóstico resuelto, la última lección responde la otra pregunta del cliente: ¿nos vamos de VMware?",
         "requisitos": ["4", "5"]},
  "12": {"objetivos": [
          "Al terminar vas a poder decidir entre renovar y migrar con núcleos, funciones usadas y un piloto.",
          "Al terminar vas a poder importar una VM de ESXi a Proxmox VE en frío.",
          "Al terminar vas a poder preparar la VM y resolver el arranque con VirtIO o SATA."],
         "conecta": "En Qué licencia hay calculaste los núcleos licenciables, y en Backup que restaura probaste un backup: acá son la base de la decisión y de la vuelta atrás.",
         "cierre": "Con esto recorriste VMware completo: de la licencia y el hardware al plan de salida. La ficha del cliente con versión y núcleos, un vmk y una VLAN por tráfico, snapshots con fecha, un backup restaurado, usuarios nominales, HA explicado sin promesas, parches con backup antes y un minuto de esxtop guardado son tu kit para el próximo host.",
          "requisitos": ["1", "7"]}
 },
 "avisos": []
}
out = "/home/claude/ies-training/ilustraciones/vmware/estructura.json"
json.dump(E, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
s = json.dumps(E, ensure_ascii=False)
print("ok", out, "guiones largos:", "—" in s or "–" in s)
