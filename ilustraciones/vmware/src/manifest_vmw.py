"""Genera /home/claude/ies-training/ilustraciones/vmware/manifest.json (figuras, pasos, conceptos, teoría, figuras de teoría y scripts de shell del host).

Mismo esquema que manifest_pdx.py (Paradox). Los scripts van en el campo script_rsc, como pide la guía:
para VMware son de shell del host ESXi (sh por SSH), solo en las lecciones que enseñan esos comandos.
"""
import json, re

M = {}


def L(lid, fig, steps, concepts, teoria, tfig, script=None):
    M[lid] = {"fig": fig, "steps": steps, "concepts": concepts, "teoria_md": teoria.strip(), "teoria_figs": tfig}
    if script:
        M[lid]["script_rsc"] = script


def C(name, para_que, como, ejemplo):
    return {"name": name, "para_que": para_que, "como": como, "ejemplo": ejemplo}


def S(titulo, descripcion, variables, codigo, notas):
    return {"titulo": titulo, "descripcion": descripcion,
            "variables": [{"nombre": n, "valor": v, "detalle": d} for n, v, d in variables],
            "codigo": codigo.strip("\n"), "notas": notas}


# =====================================================================================  1
L("1",
  {"file": "1.svg", "alt": "Tabla con tres columnas de licencias: suscripción VVF o VCF, vigente y por núcleo; Standard o Enterprise Plus, solo hasta 8.0 Update 3; y ESXi gratuito 8.0 Update 3e. Filas: vCenter incluido en las dos primeras y no se gestiona en el gratuito; vMotion y HA sí, sí y no; backup por API (VADP) sí, sí y no; soporte y parches sí, hasta el 11/10/2027 y sin soporte; límites según edición, no pasa a la 9, y 2 CPU con 8 vCPU por VM. Notas: se cobra por núcleo físico con mínimo de 16 por CPU y vCenter incluido; vSphere 8 pierde soporte general el 11 de octubre de 2027.",
   "caption": "Qué habilita cada licencia, y la fecha que va a la ficha del cliente."},
  [{"file": "1-paso1.svg", "step": 1, "after": "Anotá clave, producto, funciones",
    "alt": "Ventana del Host Client en https://192.168.88.20/ui con el menú lateral Host, Manage resaltado, Monitor, Virtual Machines, Storage y Networking, y la pestaña Licensing elegida entre System, Hardware y Packages. Cuatro campos: clave, producto, funciones y vencimiento. Notas: anotar los cuatro datos en la ficha; la IP es la del ejemplo; si dice gratuito, no prometer vCenter, vMotion, HA ni backup por API.",
    "caption": "Los cuatro datos de Manage > Licensing que van a la ficha."},
   {"file": "1-paso3.svg", "step": 3, "after": "núcleos por CPU = CPU Cores",
    "alt": "Salida de esxcli hardware cpu global get con CPU Packages 2 y CPU Cores 16. La fórmula: núcleos por CPU igual a CPU Cores dividido CPU Packages, y por cada CPU se paga el mayor entre sus núcleos y 16. Dos ejemplos: 2 CPU de 8 núcleos son 16 físicos y 32 licenciables, con 8 núcleos por CPU que se pagan sin existir, en ámbar; 2 CPU de 24 núcleos son 48 físicos y 48 licenciables, en verde. Nota: con CPUs chicas se paga el doble; con 16 núcleos o más por CPU la cuenta es 1 a 1.",
    "caption": "Con CPUs de menos de 16 núcleos pagás núcleos que no existen."}],
  [C("Suscripción por núcleo, mínimo 16 por CPU",
     "Es como vende VMware Broadcom desde el 1 de febrero de 2024: suscripciones de 1, 3 o 5 años en lugar de licencias perpetuas por procesador. El mínimo de 16 núcleos por CPU hace que un servidor chico pague como si fuera más grande.",
     "Se leen CPU Packages y CPU Cores con `esxcli hardware cpu global get`, se calcula cuántos núcleos tiene cada CPU y por cada una se toma el mayor entre ese número y 16. Los núcleos deshabilitados en BIOS no bajan la cuenta salvo acuerdo por escrito. En inventarios grandes, RVTools (pestaña vHost) ayuda a contar.",
     "Un cliente con dos servidores de una CPU de 8 núcleos en un depósito de La Teja: 16 núcleos físicos, 32 licenciables. Ese número va a la ficha antes de que alguien pida cotizar la renovación."),
   C("VVF, VCF y las ediciones viejas",
     "Broadcom ordenó la oferta en dos paquetes: vSphere Foundation (VVF) y Cloud Foundation (VCF, con NSX, vSAN y el resto del stack). Standard y Enterprise Plus siguen existiendo, pero solo hasta 8.0 Update 3. En todas, vCenter viene incluido.",
     "En el Host Client, Manage > Licensing muestra clave, producto, funciones y vencimiento. Con eso sabés si el cliente puede tener vMotion, HA o backups por API, y si podrá pasar a la versión 9 o se queda en la 8.",
     "Un estudio contable en Pocitos tiene Standard con tres hosts y pregunta por DRS: la tabla de ediciones dice que Standard no lo trae. Se lo explicás antes de prometer nada."),
   C("ESXi gratuito 8.0 U3e",
     "Volvió en abril de 2025 para laboratorio y pruebas, después de que Broadcom discontinuara el hipervisor gratuito original. Permite instalar un host sin pagar, pero con límites fuertes.",
     "No se gestiona con vCenter, no tiene vMotion, HA ni DRS, no expone VADP, sus APIs son de solo lectura, admite hasta 2 CPU físicas y 8 vCPU por VM, y no tiene soporte. En un cliente solo tiene sentido si acepta eso y hay backup con agente dentro de cada VM.",
     "El ESXi de banco de la oficina de IES, en un servidor viejo, corre con la licencia gratuita: sirve para practicar todo este curso salvo lo que necesita vCenter."),
   C("Fin de soporte de vSphere 8",
     "Cada versión tiene fecha de fin de soporte general: después no hay soporte técnico ni parches nuevos. vSphere 7 terminó el 2 de octubre de 2025 y vSphere 8 termina el 11 de octubre de 2027.",
     "La fecha va a la ficha del cliente junto con la versión exacta (`vmware -vl`). Con tiempo, se plantea la decisión: pasar a la versión 9 con suscripción, o evaluar alternativas con un piloto, como se ve en la última lección.",
     "En la visita de mantenimiento de un cliente con vSphere 8 le dejás por escrito: soporte hasta octubre de 2027, y la propuesta de revisarlo un año antes.")],
  """
### Un poco de historia

VMware se fundó en 1998 y su primer producto fue un hipervisor de escritorio, que corría arriba de Windows o Linux. En 2001 llegó ESX Server, que se instala directo sobre el servidor, y desde vSphere 5.0, en 2011, queda solo ESXi. Durante muchos años se vendió con licencia perpetua por procesador, más un contrato de soporte aparte.

Broadcom compró VMware a fines de 2023 y cambió el modelo. Desde el 1 de febrero de 2024 todo producto nuevo se vende por suscripción de 1, 3 o 5 años y vCenter viene incluido. Se discontinuaron Essentials, Essentials Plus y el hipervisor gratuito original; en abril de 2025 volvió un ESXi gratuito con la 8.0 Update 3e. vSphere 7 terminó su soporte general el 2 de octubre de 2025 y vSphere 8 lo termina el 11 de octubre de 2027.

### Cómo funciona

La oferta vigente se ordena en dos paquetes: VVF, vSphere Foundation, y VCF, Cloud Foundation, que suma NSX, más capacidad de vSAN y el resto del stack. vSphere Standard y Enterprise Plus solo llegan hasta 8.0 Update 3: no pasan a la versión 9.

La cuenta es por núcleo físico, con un mínimo de 16 núcleos por CPU. Por cada CPU se paga el mayor entre sus núcleos reales y 16. Tres hosts con una CPU de 8 núcleos tienen 24 núcleos físicos pero se licencian 48. Los núcleos deshabilitados en BIOS no bajan la cuenta salvo acuerdo por escrito.

El ESXi gratuito sirve para laboratorio y pruebas: no se gestiona con vCenter, no tiene vMotion, HA ni DRS, no expone VADP para backups, sus APIs son de solo lectura, admite hasta 2 CPU físicas y 8 vCPU por VM y no tiene soporte. Las fuentes no coinciden en si conviene en producción: la KB lo ofrece, pero sin VADP no hay backup a nivel host y Broadcom ya cambió esta política una vez.

Por eso el primer dato de cualquier visita es qué licencia y versión tiene el host. En el Host Client, Manage > Licensing; por SSH, `vmware -vl` y `esxcli hardware cpu global get`. Con eso sabés qué podés prometer y cuándo avisar del fin de soporte.
""",
  [{"file": "1-t1.svg", "after": "Por cada CPU se paga el mayor entre sus núcleos reales y 16",
    "alt": "Animación en cuatro tiempos. 1: tres hosts con una CPU de 8 núcleos cada uno suman 24 núcleos físicos. 2: cada CPU se cobra como mínimo 16, así que a cada una se le suman 8 núcleos que no existen, marcados en ámbar. 3: el total queda en 24 físicos y 48 licenciables, el doble. 4: en cambio, dos hosts con una CPU de 24 núcleos suman 48 físicos y 48 licenciables, una relación 1 a 1.",
    "caption": "Los núcleos que se pagan sin existir, CPU por CPU."},
   {"file": "1-t2.webp", "after": "Broadcom compró VMware a fines de 2023",
    "alt": "Línea de tiempo: 2001, ESX Server, el hipervisor de VMware sobre el servidor; 2011, vSphere 5.0, queda solo ESXi; noviembre de 2023, Broadcom compra VMware; febrero de 2024, solo suscripción por núcleo con mínimo de 16 por CPU y vCenter incluido; abril de 2025, ESXi gratuito 8.0 U3e sin vCenter, sin VADP y sin soporte; 11 de octubre de 2027, fin de soporte de vSphere 8, sin parches ni soporte técnico.",
    "caption": "De la licencia perpetua a la suscripción, y la fecha que viene."}],
  S("Ficha de versión y núcleos licenciables del host",
    "Solo lee: muestra la versión de ESXi, cuenta CPU y núcleos, calcula los núcleos licenciables con el mínimo de 16 por CPU y guarda la ficha en un archivo del datastore.",
    [("CLIENTE", "cliente-prueba", "Nombre corto del cliente, sin espacios, para el archivo"),
     ("DATASTORE", "datastore1", "Datastore donde se guarda la ficha")],
    r'''
#!/bin/sh
# IES Training - VMware - Ficha de version y nucleos licenciables
# Solo lee y guarda un archivo de texto: no cambia la configuracion del host.
CLIENTE="{{CLIENTE}}"
DS="{{DATASTORE}}"
MINIMO=16
FICHA="/vmfs/volumes/$DS/ficha-$CLIENTE.txt"
[ -d "/vmfs/volumes/$DS" ] || { echo "No existe el datastore $DS"; exit 1; }
PKG=$(esxcli hardware cpu global get | awk '/CPU Packages/ {print $NF}')
CORES=$(esxcli hardware cpu global get | awk '/CPU Cores/ {print $NF}')
[ -n "$PKG" ] && [ "$PKG" -gt 0 ] || { echo "No pude leer CPU Packages"; exit 1; }
POR_CPU=$((CORES / PKG))
# por cada CPU se paga el mayor entre sus nucleos y 16
if [ "$POR_CPU" -lt "$MINIMO" ]; then LIC_CPU=$MINIMO; else LIC_CPU=$POR_CPU; fi
LIC=$((LIC_CPU * PKG))
{
  echo "Cliente: $CLIENTE"
  echo "Host: $(hostname)"
  echo "Fecha: $(date +%Y-%m-%d)"
  vmware -vl
  echo "CPU (packages): $PKG"
  echo "Nucleos fisicos: $CORES ($POR_CPU por CPU)"
  echo "Nucleos licenciables: $LIC"
  echo "Fin de soporte general de vSphere 8: 11/10/2027"
} | tee "$FICHA"
echo "Listo: ficha guardada en $FICHA. Completala con la licencia de Host Client > Manage > Licensing."
''',
    ["La licencia (clave, producto, funciones, vencimiento) se copia a mano desde Manage > Licensing: el script no la lee.",
     "Si lo corrés dos veces, la ficha se reescribe con los datos del momento.",
     "Habilitá SSH solo para esto y deshabilitalo al terminar (paso 5)."]))

# =====================================================================================  2
L("2",
  {"file": "2.svg", "alt": "Seis tarjetas con los requisitos de ESXi 8: CPU de 2 núcleos como mínimo y en la Compatibility Guide; BIOS con VT-x o AMD-V, NX/XD y UEFI; memoria de 8 GB como mínimo y 12 GB para producción; red con una NIC gigabit soportada, mejor dos; disco de arranque persistente de 32 GB mínimo y 128 GB óptimo en RAID 1, en verde; y SD o USB, en rojo, solo para arranque, en retirada y no sirven para OSDATA. Notas: primero el modelo en la Broadcom Compatibility Guide, la ex HCL; ESXi 9 deja afuera CPUs Skylake y anteriores.",
   "caption": "Hardware de la lista, BIOS bien configurado y disco de arranque persistente."},
  [{"file": "2-paso3.svg", "step": 3, "after": "Booteá el instalador ESXi 8 desde un USB",
    "alt": "Una notebook con consola remota y un USB con el instalador ESXi 8 llegan al servidor por medios virtuales de iLO o iDRAC o por USB. El instalador revisa CPU, NICs y controladora. Si detecta todo, en verde, se cancela o se sigue con la instalación en un disco persistente. Si avisa algo no soportado, en rojo, se frena, se revisa la Compatibility Guide y no se instala en un cliente. Nota: nada se escribe en los discos hasta confirmar la instalación.",
    "caption": "El instalador te dice qué ve antes de tocar un disco."},
   {"file": "2-paso4.svg", "step": 4, "after": "Si instalás, elegí un disco persistente",
    "alt": "Pantalla de la DCUI en Configure Management Network con las opciones Network Adapters, VLAN (optional), IPv4 Configuration resaltada, IPv6 Configuration, DNS Configuration resaltada y Custom DNS Suffixes. A la derecha, IPv4 en modo Static con IP 192.168.88.20, máscara 255.255.255.0 y gateway 192.168.88.1, y DNS 192.168.88.1 con hostname esxi-lab01. Abajo, Esc y Y reinician la red de gestión; después se entra con root a https://192.168.88.20/ui.",
    "caption": "IPv4 fija, DNS y hostname; Esc y Y aplican."}],
  [C("Broadcom Compatibility Guide",
     "ESXi no tiene un Windows ni un Linux debajo: trae sus propios drivers. La guía, que antes se llamaba HCL, es la lista de CPU, NIC y controladoras que tienen driver y soporte en cada versión.",
     "Antes de instalar se busca el modelo del servidor, la CPU, las NICs y la controladora para ESXi 8.0 U3, y para 9.0 si el cliente piensa actualizar. Si algo no está, no hay soporte. Parámetros como `allowLegacyCPU=true` fuerzan la instalación en CPUs viejas, pero solo para laboratorio.",
     "Te ofrecen un servidor usado barato para montar el grabador de un cliente en Maldonado. Su CPU es Broadwell: ESXi 8 todavía lo acepta, pero ESXi 9 deja afuera Skylake y anteriores. Lo anotás antes de comprarlo."),
   C("Disco de arranque persistente",
     "Además del arranque, ESXi guarda en la partición OSDATA el scratch y los logs. Si arranca de SD o USB, eso termina en memoria y se pierde al reiniciar, y aparece la alarma \"Secondary persistent device not found\".",
     "Se instala en un disco local persistente: 32 GB como mínimo y 128 GB como óptimo, idealmente en RAID 1. SD y USB quedan solo para arranque y están en retirada.",
     "Un host que se colgó de noche no deja rastros en sus logs: arrancaba de una SD. Al reinstalarlo en dos discos en RAID 1, el próximo problema sí queda registrado en vmkernel.log."),
   C("DCUI y red de gestión",
     "La DCUI es la pantalla de consola del host, la amarilla y gris. Sirve para dejar el host accesible por la red antes de que exista cualquier otra herramienta.",
     "Con F2 > Configure Management Network se elige la placa, la VLAN si hace falta, IPv4 estática, DNS y hostname. Con Esc y Y se reinicia la red de gestión. Desde ahí se entra al Host Client por https, con la IP del host seguida de /ui.",
     "En el rack de un cliente en el Centro, con monitor y teclado prestados, dejás el host en 192.168.88.20 con hostname esxi-lab01 y seguís el resto desde tu notebook.")],
  """
### Un poco de historia

En 1974 Gerald Popek y Robert Goldberg publicaron las condiciones formales para que un procesador se pueda virtualizar de forma eficiente. Los x86 de los noventa no las cumplían del todo: algunas instrucciones sensibles no avisaban al hipervisor. VMware lo resolvió por software, traduciendo esas instrucciones al vuelo, y así salieron su hipervisor de escritorio y, en 2001, ESX Server, que se instala directo sobre el servidor.

Entre 2005 y 2006 Intel y AMD agregaron VT-x y AMD-V, el soporte de virtualización dentro del propio procesador. Hoy ESXi 8 lo exige habilitado en BIOS, junto con NX/XD. Cada versión nueva deja afuera procesadores viejos: ESXi 8 dejó afuera Sandy Bridge, Ivy Bridge y Haswell, y ESXi 9 deja afuera Skylake y anteriores.

### Cómo funciona

Hay dos tipos de hipervisor. El tipo 2 es un programa que corre arriba de un sistema operativo: Windows o Linux manejan el hardware y el hipervisor les pide recursos. El tipo 1 se instala directo sobre el hardware. ESXi es tipo 1: su núcleo, el VMkernel, maneja CPU, memoria, discos y placas de red, y los reparte entre las VMs.

Con VT-x o AMD-V, el código normal de una VM corre directo en la CPU real y solo las instrucciones sensibles saltan al VMkernel. Por eso el BIOS tiene que tenerlos habilitados, y el arranque en UEFI.

Como no hay sistema operativo debajo, ESXi trae sus propios drivers. Si una NIC o una controladora no tiene driver en esa versión, no aparece o anda mal. De ahí la regla de la Broadcom Compatibility Guide. William Lam propone un truco: bootear el instalador sin instalar y ver qué detecta.

El disco de arranque también cambió. ESXi guarda en OSDATA el scratch y los logs; si arranca de SD o USB, eso queda en memoria. Por eso pide un disco persistente de 32 GB como mínimo y 128 GB como óptimo, con 2 núcleos, 8 GB de RAM (12 GB en producción) y una NIC gigabit soportada.
""",
  [{"file": "2-t1.svg", "after": "y los reparte entre las VMs",
    "alt": "Animación en cuatro tiempos con dos pilas de capas. A la izquierda, tipo 2: VM, hipervisor tipo 2 como Workstation, sistema operativo de la PC y hardware. A la derecha, tipo 1: VM, ESXi (VMkernel) y hardware del servidor. 1: un pedido de la VM baja tres capas hasta el hardware en el tipo 2. 2: en el tipo 1 baja una sola capa. 3: con VT-x o AMD-V el código normal de la VM corre directo en la CPU y las instrucciones sensibles saltan como trampa a ESXi. 4: ESXi trae sus propios drivers de NIC y controladora; si un driver no está incluido, la placa no aparece, y por eso se mira la Compatibility Guide.",
    "caption": "Menos capas entre la VM y el hierro, y drivers propios."}])

# =====================================================================================  3
L("3",
  {"file": "3.svg", "alt": "Interior de un host ESXi llamado esxi-lab01. A la izquierda, el port group Management Network con vmk0 en 192.168.88.20 y VLAN 0 sin etiqueta, colgado de vSwitch0 con el uplink vmnic0. A la derecha, dos VMs, video y acceso, en el port group VM-VLAN20 con VLAN 20, colgado de vSwitch1 con dos uplinks, vmnic2 y vmnic3. Abajo, el switch físico: vmnic0 a una boca de acceso y vmnic2 y vmnic3 a dos bocas en troncal. Notas: el port group es un enchufe virtual con su VLAN ID; dos uplinks a dos bocas para que el tráfico siga si se suelta un cable; la VLAN de Management Network se cambia solo con iLO, iDRAC o la pantalla abierta.",
   "caption": "Las VMs se enchufan a port groups; los port groups cuelgan de un vSwitch con sus uplinks."},
  [{"file": "3-paso1.svg", "step": 1, "after": "Configurá los dos puertos del switch",
    "alt": "Dos paneles con el mismo vSwitch1 y una VM de prueba en VM-VLAN20. Con los dos cables, vmnic2 y vmnic3 conectados, el ping tiene 0 por ciento perdido. Al desenchufar vmnic3, marcado en rojo con una cruz, el ping sigue por vmnic2. Abajo: puertos del switch en troncal con la VLAN 20 permitida y el comando esxcli network vswitch standard policy failover get -v vSwitch1 para revisar que los dos uplinks estén activos. Aviso: si al desenchufar se corta el ping, falta permitir la VLAN 20 en esa boca.",
    "caption": "Con un cable afuera, el ping tiene que seguir."}],
  [C("vSwitch estándar y uplinks",
     "Cuando un servidor aloja muchas VMs, el switch se mete adentro del host. El vSwitch estándar conecta las placas virtuales de las VMs y de los vmk con las placas físicas del servidor, que en ESXi se llaman vmnic y hacen de uplinks.",
     "Se crea con `esxcli network vswitch standard add` y se le suman uplinks con `uplink add`. Con dos uplinks a dos bocas distintas, si una se cae el tráfico sigue por la otra; `policy failover get` muestra cuáles están activos. Cada host tiene sus propios vSwitch estándar.",
     "El servidor de un edificio en Pocitos graba 40 cámaras. Con vmnic2 y vmnic3 en el mismo vSwitch, un patch cord flojo en el rack no corta la grabación."),
   C("Port group con VLAN ID",
     "Es el enchufe virtual con su VLAN: todas las VMs conectadas a un port group quedan en esa VLAN, sin configurar nada dentro de la VM. Es la misma lógica de VLAN de los switches, aplicada adentro del servidor.",
     "Cada port group lleva un VLAN ID; 0 es sin etiqueta, la VLAN nativa del switch físico. El vSwitch pone la etiqueta al salir y la saca al entrar. El puerto del switch físico va en troncal con esas VLAN permitidas.",
     "En un cliente con cámaras en VLAN 20 y control de acceso en VLAN 30, creás dos port groups en el mismo vSwitch: el NVR virtual va al de la 20 y el servidor de acceso al de la 30."),
   C("Red de gestión y consola fuera de banda",
     "La red de gestión es por donde entrás al host. Si cambiás su VLAN y el switch no la tiene, el host queda sin acceso y no lo podés arreglar por la misma red que acabás de cortar.",
     "La KB de Broadcom pide hacer esos cambios desde iLO, iDRAC o la consola física, nunca solo por SSH o desde el cliente web. Primero abrís la consola fuera de banda, después tocás Management Network.",
     "Antes de mover la gestión de un host a la VLAN de servidores en un shopping, abrís la iDRAC en otra pestaña. Si algo sale mal, volvés desde la DCUI sin ir al sitio.")],
  """
### Un poco de historia

La norma IEEE 802.1Q, de 1998, definió cómo etiquetar una trama Ethernet con un número de VLAN: 4 bytes extra con un identificador de 12 bits. Así un solo cable, el troncal, puede llevar muchas redes separadas, y cada switch sabe a cuál pertenece cada trama.

Antes de la virtualización, cada servidor tenía su placa en una boca de acceso de una sola VLAN. Cuando un servidor empezó a alojar decenas de VMs de redes distintas, el switch se mudó adentro del host: el vSwitch. ESXi trae el vSwitch estándar en cada host; con vCenter existe además un switch distribuido, que este curso no cubre.

### Cómo funciona

El vSwitch estándar tiene dos lados. De un lado, los uplinks: las placas físicas del servidor, que ESXi llama vmnic. Del otro, los port groups: los enchufes donde se conectan las placas virtuales de las VMs y los adaptadores del propio host.

Cada port group lleva un VLAN ID. La VM manda una trama común; al pasar por el port group, el vSwitch le pone la etiqueta de su VLAN, y al recibir se la saca. Con VLAN ID 0 la trama sale sin etiqueta y el switch físico la pone en su VLAN nativa. Por eso el puerto del switch va en troncal, con las VLAN de los port groups permitidas.

Con dos uplinks en el mismo vSwitch, a dos bocas distintas, el NIC teaming da balanceo y failover: si se suelta un cable o se cae una boca, el tráfico sigue por la otra y la VM no se entera. `esxcli network vswitch standard policy failover get` muestra qué uplinks están activos.

La instalación crea vSwitch0 con el port group Management Network y el vmk0 de gestión. Cambiar su VLAN sin que el switch la tenga deja al host sin acceso: la KB de Broadcom pide hacerlo con iLO, iDRAC o la pantalla abierta.
""",
  [{"file": "3-t1.svg", "after": "el vSwitch le pone la etiqueta de su VLAN",
    "alt": "Animación en cuatro tiempos de un host ESXi con un vSwitch, dos port groups (VLAN 20 para la VM de video y VLAN 0 para la gestión, vmk0) y dos uplinks, vmnic2 y vmnic3, hacia un switch físico en troncal. 1: la VM manda una trama sin etiqueta y al pasar por el port group recibe la etiqueta 802.1Q con VLAN 20. 2: la trama etiquetada viaja por el troncal y el switch la entrega al gateway de la VLAN 20. 3: la trama de gestión, en VLAN 0, sale sin etiqueta y el switch la pone en la red nativa; si se cambia esa VLAN sin que el switch la tenga, el host queda sin acceso. 4: se suelta el cable de vmnic3 y el tráfico sigue por vmnic2: el ping no se corta.",
    "caption": "Etiqueta en el port group, troncal en el switch, segundo uplink de respaldo."}],
  S("vSwitch con dos uplinks y port group con VLAN",
    "Crea el vSwitch si no existe, le suma los dos uplinks si están libres y crea el port group con su VLAN ID. No toca vSwitch0 ni Management Network.",
    [("VSWITCH", "vSwitch1", "Nombre del vSwitch nuevo"),
     ("NIC1", "vmnic2", "Primer uplink libre"),
     ("NIC2", "vmnic3", "Segundo uplink libre"),
     ("PORTGROUP", "VM-VLAN20", "Nombre del port group"),
     ("VLAN", "20", "VLAN ID (0 = sin etiqueta)")],
    r'''
#!/bin/sh
# IES Training - VMware - vSwitch con dos uplinks y port group con VLAN
# Probalo primero en un ESXi de laboratorio. No toca la red de gestion.
VSW="{{VSWITCH}}"
PG="{{PORTGROUP}}"
VLAN="{{VLAN}}"
[ "$PG" = "Management Network" ] && { echo "Este script no toca Management Network"; exit 1; }
[ "$VSW" = "vSwitch0" ] && { echo "Este script no toca vSwitch0"; exit 1; }
if esxcli network vswitch standard list | grep -q "Name: $VSW\$"; then
  echo "Ya existe $VSW"
else
  esxcli network vswitch standard add -v "$VSW" && echo "Creado $VSW"
fi
for NIC in "{{NIC1}}" "{{NIC2}}"; do
  if esxcli network vswitch standard list -v "$VSW" | grep "Uplinks:" | grep -qw "$NIC"; then
    echo "$NIC ya es uplink de $VSW"
  elif esxcli network vswitch standard list | grep "Uplinks:" | grep -qw "$NIC"; then
    echo "Ojo: $NIC ya es uplink de otro vSwitch. No la muevo."
  else
    esxcli network vswitch standard uplink add -u "$NIC" -v "$VSW" && echo "Sumado $NIC"
  fi
done
if esxcli network vswitch standard portgroup list | awk -v p="$PG" '$1==p {f=1} END {exit !f}'; then
  echo "Ya existe el port group $PG"
else
  esxcli network vswitch standard portgroup add -p "$PG" -v "$VSW" && echo "Creado $PG"
fi
esxcli network vswitch standard portgroup set -p "$PG" -v "$VLAN"
esxcli network vswitch standard policy failover get -v "$VSW"
echo "Listo: $VSW con sus uplinks y $PG en VLAN $VLAN. Verifica con esxcfg-vswitch -l"
''',
    ["Las bocas del switch físico van en troncal con la VLAN permitida: eso no lo hace el script.",
     "Si una placa ya es uplink de otro vSwitch (por ejemplo de gestión), el script avisa y no la mueve.",
     "Después conectá una VM al port group, probá ping a su gateway y desenchufá un cable."]))

# =====================================================================================  4
L("4",
  {"file": "4.svg", "alt": "Host ESXi con tres adaptadores VMkernel: vmk0 de gestión en 192.168.88.20 en Management Network; vmk1 de almacenamiento IP en 10.10.10.21 con MTU 9000 en Storage-VLAN30, conectado por NFS a un NAS de prueba en 10.10.10.50; y vmk2 de vMotion en una red privada solo de hosts, VLAN propia, en ámbar. A la derecha, dos datastores: nfs-lab, NFS 3 o 4.1, y datastore1, VMFS sobre disco local o LUN. Notas: el tráfico de vMotion va sin cifrar y lleva la memoria de la VM, por eso va aislado; cada vmk con su VLAN, su subred y su prueba de vmkping.",
   "caption": "Un vmk por tráfico: gestión, almacenamiento y vMotion, cada uno en su red."},
  [{"file": "4-paso1.svg", "step": 1, "after": "Si el vmkping grande falla",
    "alt": "El comando vmkping -I vmk1 -d -s 8972 10.10.10.50 y la cuenta 8972 más 28 de encabezados igual a 9000. Dos filas con cuatro saltos: vmk1, vSwitch1, switch físico y NAS. Arriba, todo en MTU 9000 y el ping pasa, en verde. Abajo, el switch físico en MTU 1500, en rojo, y el paquete grande no pasa. Notas: -d prohíbe fragmentar, así que si algún salto tiene 1500 el ping grande se pierde y el normal anda; cambiar el MTU de un vSwitch con VMs en producción puede cortar un instante y va en ventana de mantenimiento.",
    "caption": "El ping grande con -d prueba el MTU de cada salto."}],
  [C("Adaptador VMkernel (vmk)",
     "Las VMs tienen sus IPs, pero el host también necesita las suyas para que lo gestionen, para mover VMs y para hablar con el almacenamiento por red. Cada una de esas IPs es un adaptador VMkernel.",
     "La documentación pide uno por tipo de tráfico: gestión, vMotion, almacenamiento IP, backup, replicación. Cada vmk va en su port group, su VLAN y su subred; varios vmk en la misma subred no están soportados, salvo casos como iSCSI con varias placas. Se crea con `esxcli network ip interface add` y se le da IP con `ipv4 set`.",
     "En un host de un cliente con NAS para las grabaciones, vmk0 queda en la red de gestión y vmk1 en la VLAN 30 de almacenamiento: los backups nocturnos no compiten con el Host Client."),
   C("Datastore VMFS y NFS",
     "Un datastore es donde viven los archivos de las VMs. VMFS es el sistema de archivos propio de ESXi, pensado para que varios hosts compartan el mismo disco; NFS deja que un NAS ponga su propio sistema de archivos y el host lo monte por red.",
     "VMFS se arma sobre un disco local o una LUN (SAN o iSCSI). NFS, en versión 3 o 4.1, se monta con `esxcli storage nfs add` por un vmk de almacenamiento. En NFS sin aceleración por hardware los discos solo pueden ser thin. `esxcli storage filesystem list` muestra todos con su tamaño y libre.",
     "Para un grabador virtual en una cadena de farmacias, el NAS del cliente se monta como nfs-lab y las grabaciones viven ahí, separadas del datastore local donde está el sistema."),
   C("Jumbo frames y vmkping",
     "Con tramas de 9000 bytes en lugar de 1500, el almacenamiento por red mueve más datos con menos paquetes. Pero si un solo salto del camino queda en 1500, aparecen cortes intermitentes difíciles de entender.",
     "MTU 9000 igual en el vmk, el vSwitch, el switch físico y el NAS. Se prueba con `vmkping -I vmk1 -d -s 8972 <IP del NAS>`: -d prohíbe fragmentar y 8972 más 28 de encabezados da 9000. Si el grande falla y el normal anda, hay un salto en 1500.",
     "Un NAS que \"se desconecta solo\" en un depósito de Carrasco: el vmkping grande falla. El switch nuevo había quedado en 1500 en las bocas del NAS; con 9000 se acaban los cortes.")],
  """
### Un poco de historia

VMFS es el sistema de archivos que VMware creó para ESXi, con una idea central: varios hosts pueden usar el mismo disco a la vez, cada uno bloqueando solo los archivos de sus VMs. Esa capacidad de compartir es la base de vMotion y HA. La versión actual, VMFS-6, llegó con vSphere 6.5 en 2016.

NFS es más viejo y más general: Sun Microsystems lo creó en 1984 para compartir archivos por la red. ESXi lo usa en las versiones 3 y 4.1. iSCSI, estandarizado en 2004, lleva comandos SCSI por IP, para que una red Ethernet haga de SAN. Las tramas jumbo de 9000 bytes nunca fueron parte formal de Ethernet, que define 1500: por eso hay que configurarlas igual en cada salto.

### Cómo funciona

Un adaptador VMkernel es una IP del propio host. La documentación pide uno por tipo de tráfico: gestión, vMotion, almacenamiento IP, Fault Tolerance, replicación, vSAN o backup. Cada uno en su port group, su VLAN y su subred, y para redundancia, dos placas físicas detrás.

El tráfico de vMotion no va cifrado y lleva la memoria de la VM: por eso va en una red privada solo de hosts. Tener varios vmk en la misma subred no está soportado, salvo casos puntuales como iSCSI con varias placas.

Un datastore VMFS se arma sobre un disco local o una LUN, y el host maneja el sistema de archivos por bloques. Un datastore NFS es un export de un NAS: el NAS maneja los archivos y el host los usa por un vmk. Adentro, cada VM es una carpeta con su `.vmx` y sus `.vmdk`.

Con jumbo frames, el MTU tiene que ser 9000 de punta a punta: vmk, vSwitch, switch físico y NAS. `vmkping -I vmk1 -d -s 8972` lo prueba: 8972 de datos, más 8 de ICMP y 20 de IP, dan 9000, y -d prohíbe partir el paquete. Si un salto quedó en 1500, el ping grande se pierde y el normal anda.
""",
  [{"file": "4-t1.svg", "after": "el ping grande se pierde y el normal anda",
    "alt": "Animación en cuatro tiempos con cuatro saltos en fila: vmk1, vSwitch1, switch físico y NAS. 1: vmkping con -d y -s 8972 arma un paquete de 9000 bytes que no se puede fragmentar. 2: atraviesa vmk1 y vSwitch1, que están en MTU 9000. 3: el switch físico está en MTU 1500 y el paquete se descarta; el ping normal seguiría andando. 4: con el switch en 9000, el paquete llega al NAS y vuelve la respuesta. Abajo, la cuenta: 8972 de datos más 8 de ICMP más 20 de IP son 9000 bytes.",
    "caption": "Un solo salto en 1500 alcanza para que el paquete grande no pase."},
   {"file": "4-t2.webp", "after": "Adentro, cada VM es una carpeta con su",
    "alt": "Comparación en dos paneles. VMFS: dos hosts ESXi acceden por SAN, iSCSI o disco local a un disco o LUN que ESXi formatea con VMFS y maneja por bloques. NFS: dos hosts ESXi acceden por NFS 3 o 4.1 a través de un vmk a un export de un NAS, que maneja su propio sistema de archivos. En los dos, una carpeta por VM con el .vmx de configuración y el .vmdk y -flat.vmdk del disco. Nota: si el datastore es compartido, varios hosts ven las mismas VMs, lo que habilita vMotion y HA.",
    "caption": "Bloques con VMFS o archivos con NFS; adentro, una carpeta por VM."}],
  S("vmk de almacenamiento con MTU 9000 y montaje NFS",
    "Pone el vSwitch en MTU 9000, crea el vmk de almacenamiento con IP fija si no existe, prueba el MTU con vmkping y monta el export NFS si todavía no está montado.",
    [("VSWITCH", "vSwitch1", "vSwitch donde está el port group de almacenamiento"),
     ("PORTGROUP", "Storage-VLAN30", "Port group de almacenamiento, ya creado"),
     ("VMK", "vmk1", "Nombre del adaptador VMkernel"),
     ("IP_VMK", "10.10.10.21", "IP del host en la red de almacenamiento"),
     ("MASCARA", "255.255.255.0", "Máscara de la red de almacenamiento"),
     ("NAS", "10.10.10.50", "IP del NAS"),
     ("EXPORT", "/export/lab", "Ruta del export NFS"),
     ("DATASTORE", "nfs-lab", "Nombre del datastore NFS")],
    r'''
#!/bin/sh
# IES Training - VMware - vmk de almacenamiento con MTU 9000 y NFS
# Solo en laboratorio o en ventana: cambiar el MTU puede cortar un instante.
VSW="{{VSWITCH}}"; PG="{{PORTGROUP}}"; VMK="{{VMK}}"; NAS="{{NAS}}"; DS="{{DATASTORE}}"
esxcli network vswitch standard portgroup list | awk -v p="$PG" '$1==p {f=1} END {exit !f}' || { echo "No existe $PG: crealo antes (leccion 3)"; exit 1; }
MTU=$(esxcli network vswitch standard list -v "$VSW" | awk '/MTU:/ {print $2; exit}')
if [ "$MTU" != "9000" ]; then
  esxcli network vswitch standard set -v "$VSW" -m 9000 && echo "$VSW en MTU 9000"
fi
if esxcli network ip interface list | grep -q "Name: $VMK\$"; then
  echo "Ya existe $VMK"
else
  esxcli network ip interface add -i "$VMK" -p "$PG" -m 9000 && echo "Creado $VMK"
fi
esxcli network ip interface set -i "$VMK" -m 9000
esxcli network ip interface ipv4 set -i "$VMK" -t static -I "{{IP_VMK}}" -N "{{MASCARA}}"
# 8972 + 28 de encabezados = 9000; -d prohibe fragmentar
if vmkping -I "$VMK" -d -s 8972 -c 3 "$NAS" >/dev/null 2>&1; then
  echo "OK: MTU 9000 de punta a punta hasta $NAS"
else
  echo "Ojo: el vmkping grande falla. Hay un salto en 1500. No monto el NFS."
  exit 1
fi
if esxcli storage nfs list | awk -v d="$DS" '$1==d {f=1} END {exit !f}'; then
  echo "Ya estaba montado $DS"
else
  esxcli storage nfs add -H "$NAS" -s "{{EXPORT}}" -v "$DS" && echo "Montado $DS"
fi
esxcli storage filesystem list
echo "Listo: $VMK en $PG con MTU 9000 y $DS montado. Verifica con esxcli storage nfs list"
''',
    ["El switch físico y el NAS también tienen que estar en MTU 9000: eso se configura en cada equipo.",
     "Si el vmkping grande falla, el script no monta el NFS: corregí el MTU y volvé a pegarlo.",
     "No asigna el servicio vMotion ni otros tags al vmk: solo lo deja para almacenamiento."]))

# =====================================================================================  5
L("5",
  {"file": "5.svg", "alt": "Tres tarjetas con los formatos de disco. Thick lazy zeroed: reserva todo al crear y pone en cero al primer uso; el espacio queda apartado. Thick eager zeroed: reserva y pone en cero todo al crear, tarda más, y es el que pide Fault Tolerance. Thin, en ámbar: crece a demanda hasta su tamaño máximo y deja libre el resto para otros; si llena el datastore, la VM se detiene. Abajo: un appliance .ova entra por Deploy OVF Template, que crea la VM con su hardware, y copiar el .ova al datastore no lo instala; VMware Tools siempre, por el driver de balloon, los snapshots con quiesce y el latido que mira HA.",
   "caption": "Thick aparta el espacio; thin lo promete. Y Tools en todas."},
  [{"file": "5-paso1.svg", "step": 1, "after": "muestra el tamaño provisionado",
    "alt": "Terminal con vim-cmd vmsvc/get.guest 1 filtrado por tools: toolsRunningStatus guestToolsRunning y toolsVersionStatus guestToolsCurrent, Tools corriendo y al día. Otra terminal con valores de ejemplo: ls -lh muestra 100G del vm-prueba-flat.vmdk y du -h muestra 18G. Una barra del disco thin: 18G ocupados en azul y 82G que todavía puede crecer, en ámbar punteado. Notas: sumar lo que pueden crecer todas las VMs thin del datastore y compararlo con el libre de esxcli storage filesystem list; si la suma supera el libre, el datastore está sobreasignado.",
    "caption": "ls -lh es lo prometido; du -h, lo ocupado; la diferencia, lo que falta crecer."}],
  [C("Deploy OVF Template",
     "Los fabricantes de software de video, acceso o telefonía entregan sus servidores como appliances: un .ova o un .ovf con la VM armada. El asistente los importa creando la VM con el hardware que definió el fabricante.",
     "En el Host Client o en vCenter se elige Deploy OVF Template y el archivo .ova. Se elige datastore, red y formato de disco. Copiar el .ova al datastore o intentar registrarlo como si fuera un .vmx no lo instala.",
     "El proveedor del software de cámaras manda un .ova para la obra de un shopping: con Deploy OVF Template queda andando en minutos y con el hardware que el fabricante soporta."),
   C("VMware Tools",
     "Es el paquete de drivers y servicios que va dentro de cada VM. Le permite al host recuperar memoria con el balloon, congelar el sistema de archivos para un snapshot coherente y saber que la VM está viva.",
     "Se instala en cada VM y se mantiene al día. `vim-cmd vmsvc/get.guest <Vmid>` muestra toolsRunningStatus y toolsVersionStatus. Sin Tools no hay quiesce ni latido para VM Monitoring de HA, y en esxtop la columna del balloon lo delata.",
     "Un servidor de control de acceso clonado de otro cliente no tenía Tools: los backups salían inconsistentes. Instaladas las Tools, el job usa quiesce y la base del sistema queda bien."),
   C("Thin, thick y sobreasignación",
     "Thin reserva solo lo escrito, así que permite prometer más espacio del que hay. Thick aparta todo el tamaño desde el principio: lazy pone en cero al primer uso y eager al crear, que es lo que pide Fault Tolerance.",
     "Con thin hay que vigilar: `ls -lh` del -flat.vmdk muestra lo provisionado y `du -h` lo ocupado. Sumado por datastore y comparado con el libre, sabés cuánto falta para que se llene. Un disco se puede pasar de thin a thick con Storage vMotion.",
     "Un datastore de 1 TB con tres VMs thin de 500 GB anda bien un año, hasta que las grabaciones crecen y se llena: las VMs se detienen. Con la suma hecha, se avisaba antes.")],
  """
### Un poco de historia

Una VM de VMware es, en el fondo, una carpeta en un datastore: un `.vmx` con la configuración del hardware virtual y uno o más discos, cada uno con su descriptor `.vmdk` y su archivo de datos `-flat.vmdk`. Esa idea de VM como archivos es la que permite copiarla, moverla y respaldarla.

Para que los fabricantes pudieran entregar VMs armadas sin depender de una marca, la industria acordó OVF, un formato abierto publicado por la DMTF. Un OVA es lo mismo empaquetado en un solo archivo. Del lado de adentro, VMware Tools acompaña al producto desde sus primeras versiones como el puente entre la VM y el host. En vSphere 9 el hardware virtual llega a la versión 22.

### Cómo funciona

Un appliance .ova entra por Deploy OVF Template: el asistente lee el descriptor, crea la VM con su hardware y copia los discos al datastore elegido. Copiar el archivo a mano no lo instala.

VMware Tools agrega drivers y servicios dentro del sistema operativo de la VM. El driver de balloon le permite al host pedirle memoria a la VM cuando le falta; el quiesce congela el sistema de archivos para que un snapshot sea coherente, y el latido le avisa a HA que la VM está viva.

Los discos tienen tres formatos. Thick lazy zeroed reserva todo el espacio al crear y pone en cero cada bloque la primera vez que se usa. Thick eager zeroed pone todo en cero al crear: tarda más y es el que pide Fault Tolerance. Thin reserva solo lo escrito y crece a demanda hasta su tamaño máximo.

Thin permite sobreasignar: prometer a las VMs más espacio del que tiene el datastore. Mientras sobra lugar nadie lo nota; si el datastore se llena con las VMs corriendo, las VMs se detienen. Por eso se suma lo que cada disco thin todavía puede crecer y se compara con el libre del datastore.
""",
  [{"file": "5-t1.svg", "after": "si el datastore se llena con las VMs corriendo",
    "alt": "Animación en cuatro tiempos. Tres VMs con disco thin de 500 GB cada una, 1,5 TB provisionados, en un datastore de 1 TB. 1: se muestran los números: 1,5 TB prometidos contra 1 TB real. 2: al principio las tres ocupan poco y sobra espacio. 3: los datos crecen y la barra del datastore llega al 100 por ciento. 4: sin espacio para escribir, las tres VMs quedan detenidas, marcadas en rojo.",
    "caption": "Thin crece sin avisar hasta que el datastore se llena."}],
  S("Tools y crecimiento posible de los discos thin",
    "Solo lee: lista las VMs con el estado de VMware Tools, y en un datastore suma lo provisionado contra lo ocupado de cada -flat.vmdk para comparar con el libre.",
    [("DATASTORE", "datastore1", "Datastore a revisar")],
    r'''
#!/bin/sh
# IES Training - VMware - Tools y crecimiento posible de discos thin
# Solo lee: no cambia nada en el host ni en las VMs.
DS="{{DATASTORE}}"
[ -d "/vmfs/volumes/$DS" ] || { echo "No existe el datastore $DS"; exit 1; }
echo "== VMware Tools por VM =="
for ID in $(vim-cmd vmsvc/getallvms | awk 'NR>1 && $1 ~ /^[0-9]+$/ {print $1}'); do
  NOMBRE=$(vim-cmd vmsvc/get.config "$ID" | awk -F'"' '/^ *name = / {print $2; exit}')
  ESTADO=$(vim-cmd vmsvc/get.guest "$ID" | awk -F'"' '/toolsRunningStatus/ {print $2; exit}')
  VERSION=$(vim-cmd vmsvc/get.guest "$ID" | awk -F'"' '/toolsVersionStatus/ {print $2; exit}')
  echo "$ID $NOMBRE: $ESTADO / $VERSION"
done
echo "== Discos en $DS (GB provisionados / GB ocupados) =="
PROV=0; USADO=0
for F in /vmfs/volumes/"$DS"/*/*-flat.vmdk; do
  [ -f "$F" ] || continue
  P=$(ls -l "$F" | awk '{printf "%d", $5/1073741824}')
  U=$(du -k "$F" | awk '{printf "%d", $1/1048576}')
  echo "$F: $P / $U"
  PROV=$((PROV + P)); USADO=$((USADO + U))
done
echo "Total provisionado: $PROV GB, ocupado: $USADO GB, puede crecer: $((PROV - USADO)) GB"
esxcli storage filesystem list | awk -v d="$DS" '$0 ~ d'
echo "Listo: compara lo que puede crecer con el libre de $DS. Si no entra, esta sobreasignado."
''',
    ["Una VM sin Tools o con versión vieja aparece con guestToolsNotRunning o guestToolsNeedUpgrade: anotala.",
     "Los valores en GB se redondean hacia abajo; para el detalle, ls -lh y du -h de cada disco.",
     "No cuenta los deltas de snapshots: eso se revisa en la lección siguiente."]))

# =====================================================================================  6
L("6",
  {"file": "6.svg", "alt": "Una VM encendida, vm-prueba, sobre su disco base vm-prueba-flat.vmdk, congelado y con candado. Las escrituras nuevas van al delta vm-prueba-000001.vmdk, en ámbar, que depende del base; un segundo snapshot crearía vm-prueba-000002.vmdk, que depende del primero. Tres reglas: 2 o 3 por VM en la práctica, con 32 como tope técnico; 72 horas como máximo y mejor borrarlo apenas se valida; fecha en el nombre, como borrar-2026-10-30-antes-update. Avisos: si se pierde el disco base, el delta solo no restaura nada; no agrandar un disco con snapshots vivos ni cancelar una consolidación en curso.",
   "caption": "El delta recibe lo nuevo y depende del base: por eso no es backup."},
  [{"file": "6-paso1.svg", "step": 1, "after": "Con vCenter, lo mismo con PowerCLI",
    "alt": "Tres columnas con ls -lh de la carpeta vm-prueba. Antes: vm-prueba.vmx, vm-prueba.vmdk y vm-prueba-flat.vmdk. Con el snapshot, creado con snapshot.create 1 y el nombre borrar-2026-10-30: aparece además vm-prueba-000001.vmdk, en ámbar. Después de snapshot.removeall 1, en verde: vuelven a quedar los tres archivos. Abajo, el comando find /vmfs/volumes/datastore1/ -name con el patrón -0000 que al final no tiene que devolver nada. Aviso: un snapshot que dejó un backup puede no verse en el Snapshot Manager, por eso el find.",
    "caption": "Antes, durante y después: al final no queda ningún -0000."}],
  [C("Snapshot y disco delta",
     "Sirve para probar un cambio con vuelta atrás rápida: una actualización, un parche, un cambio de configuración. No es una copia: congela el disco base y manda todo lo nuevo a un archivo delta.",
     "Se crea con `vim-cmd vmsvc/snapshot.create` o desde el cliente, con la fecha de borrado en el nombre. La KB de Broadcom permite hasta 32 en cadena pero recomienda 2 o 3, y ninguno por más de 72 horas; CloudBolt es más estricta y habla de 24 a 72. Mientras existe, el delta crece y la VM se pone más lenta.",
     "Antes de actualizar el software de un grabador en un supermercado, sacás `borrar-2026-10-30-antes-update`. Validás al día siguiente con el cliente y lo borrás esa misma tarde."),
   C("Consolidación",
     "Borrar un snapshot no tira el delta: lo funde con el disco base para que vuelva a quedar un solo disco. Ese proceso es la consolidación, y con deltas grandes puede tardar.",
     "`vim-cmd vmsvc/snapshot.removeall` borra todos los snapshots y consolida. Una consolidación en curso no se cancela, porque puede corromper el disco. Si aparece \"Virtual machine disks consolidation is needed\", se libera lo que bloquea (por ejemplo un proxy de backup con el disco montado) y se usa Snapshots > Consolidate.",
     "Un lunes, el ERP de un estudio va lento y vCenter pide consolidación: los backups del fin de semana fallaron y dejaron deltas. Liberás el proxy, consolidás y verificás que no quede ningún -00000N.vmdk."),
   C("Snapshots huérfanos",
     "Los productos de backup sacan snapshots por la API; si un job falla, el snapshot puede quedar vivo y no verse en el Snapshot Manager. Ese delta sigue creciendo hasta llenar el datastore.",
     "Se buscan por línea de comandos: `find /vmfs/volumes/datastore1/ -name \"*-0000*.vmdk\"`. Con vCenter, PowerCLI lista los de más de 3 días con `Get-Snapshot`, y RVTools tiene la pestaña vSnapshot.",
     "En la recorrida mensual de un cliente, el find devuelve un delta de 200 GB de hace tres semanas, de un backup que falló. Se consolida antes de que llene el datastore.")],
  """
### Un poco de historia

El snapshot nació como una herramienta de comodidad: poder probar algo en una VM y volver atrás en segundos, algo imposible con un servidor físico. Con vSphere 4, en 2009, se volvió además la pieza central de los backups: las APIs de protección de datos sacan un snapshot para copiar un disco coherente mientras la VM sigue andando.

Esa doble vida explica los problemas típicos. Un snapshot olvidado después de un cambio, o uno que quedó colgado de un backup fallido, sigue creciendo en silencio. La KB de Broadcom insiste en lo mismo hace años: un snapshot no es un backup.

### Cómo funciona

Cuando sacás un snapshot, el disco base, el `-flat.vmdk`, queda congelado en solo lectura. Nace un disco delta, `-000001.vmdk`, y desde ese momento cada bloque que la VM escribe va al delta. Al leer, el host busca primero en el delta y, si ese bloque no cambió, en el base. Un segundo snapshot agrega otro delta que depende del primero.

Por eso el snapshot depende del original: si el disco base se pierde o se rompe, el delta solo no sirve para nada. Y por eso crece: más horas, más bloques cambiados, delta más grande, VM más lenta y borrado más largo.

Un snapshot puede incluir la memoria, para volver a la VM prendida tal como estaba, o pedir quiesce, que congela el sistema de archivos con VMware Tools; el quiesce solo aplica cuando no se incluye la memoria.

Borrarlo es consolidar: los bloques del delta se escriben en el base y el delta desaparece. No se cancela una consolidación en curso ni se agranda un disco con snapshots vivos. Los snapshots de los backups pueden no verse en el Snapshot Manager: el `find` de los `-0000*.vmdk` es la forma de estar seguro.
""",
  [{"file": "6-t1.svg", "after": "Un segundo snapshot agrega otro delta que depende",
    "alt": "Animación en cuatro tiempos con una VM encima de su disco base, vm-prueba-flat.vmdk. 1: sin snapshot, una escritura de la VM va directo al disco base. 2: al sacar el snapshot, el base queda congelado, en solo lectura, y aparece el delta vm-prueba-000001.vmdk. 3: cada bloque que cambia se escribe en el delta, que crece mientras el snapshot exista. 4: al borrar el snapshot, los bloques del delta se consolidan en el disco base, el delta desaparece y queda un solo disco otra vez.",
    "caption": "Base congelado, delta que crece y consolidación al borrar."}],
  S("Revisar snapshots vencidos y deltas en el host",
    "Solo lee: lista los snapshots de cada VM, marca como vencidos los que tienen en el nombre una fecha de borrado ya pasada y busca deltas en el datastore.",
    [("DATASTORE", "datastore1", "Datastore donde buscar deltas")],
    r'''
#!/bin/sh
# IES Training - VMware - Snapshots vencidos y deltas
# Solo lee. Convencion del curso: nombre borrar-AAAA-MM-DD-motivo.
DS="{{DATASTORE}}"
HOY=$(date +%Y-%m-%d)
echo "== Snapshots por VM (hoy $HOY) =="
for ID in $(vim-cmd vmsvc/getallvms | awk 'NR>1 && $1 ~ /^[0-9]+$/ {print $1}'); do
  vim-cmd vmsvc/snapshot.get "$ID" | awk -F': ' '/Snapshot Name/ {print $2}' | while read -r SNAP; do
    FECHA=$(echo "$SNAP" | sed -n 's/^borrar-\([0-9-]\{10\}\).*/\1/p')
    if [ -z "$FECHA" ]; then
      echo "Vmid $ID: $SNAP (sin fecha de borrado en el nombre)"
    elif [ "$(echo "$FECHA" | tr -d -)" -lt "$(echo "$HOY" | tr -d -)" ]; then
      echo "Vmid $ID: $SNAP VENCIDO desde $FECHA"
    else
      echo "Vmid $ID: $SNAP vence $FECHA"
    fi
  done
done
echo "== Deltas en $DS =="
find /vmfs/volumes/"$DS"/ -name "*-0000*.vmdk"
# Para crear uno con fecha (Vmid 1, sin memoria ni quiesce):
# vim-cmd vmsvc/snapshot.create 1 "borrar-AAAA-MM-DD-motivo" "detalle" 0 0
echo "Listo: revisa los VENCIDOS y los deltas sin snapshot. Para borrar: vim-cmd vmsvc/snapshot.removeall <Vmid>"
''',
    ["No borra nada: borrar es consolidar y conviene hacerlo a mano, viendo cada VM.",
     "Un delta que aparece en el find pero no en la lista de snapshots puede ser de un backup fallido: pide consolidación.",
     "La creación de snapshots queda comentada como ejemplo, con la convención de fecha del curso."]))

# =====================================================================================  7
L("7",
  {"file": "7.svg", "alt": "Un host ESXi con la VM srv-video, el vmk0 de gestión, un proxy virtual y un datastore en una LUN, y a la derecha el repositorio y un proxy físico. Tres caminos al repositorio: NBD desde vmk0 por la red de gestión; HotAdd desde el proxy virtual, en verde; y SAN desde la LUN al proxy físico, que copia al repositorio. Leyenda: NBD es el más simple y en 1 GbE puede ir lento, 10 a 20 MB/s según una guía vieja de Veeam; HotAdd monta el disco en un proxy virtual del mismo host y no anda con discos IDE; SAN lee la LUN directo sin pasar por el host. Notas: todos usan VADP; el ESXi gratuito no tiene VADP y solo queda el agente dentro de la VM.",
   "caption": "Tres caminos para la misma copia: por la red de gestión, por un proxy virtual o por la SAN."},
  [{"file": "7-paso1.svg", "step": 1, "after": "Creá en el host un port group aislado",
    "alt": "Un host ESXi con dos zonas. Producción: srv-prueba con IP 192.168.88.50 en vSwitch1 VM-VLAN20, con uplinks vmnic2 y vmnic3 cableados a la red del cliente. Aislado, en verde: srv-prueba-restore, misma IP y otro nombre, en vSwitch-Aislado con el port group Restore-Aislado y sin uplinks, así que no sale del host. Los comandos esxcli para crear vSwitch-Aislado y el port group Restore-Aislado. Nota: restaurada con la misma IP que el original, aislada no choca.",
    "caption": "Un vSwitch sin placas físicas: la restaurada no puede chocar con la original."},
   {"file": "7-paso4.svg", "step": 4, "after": "Anotá: tiempo total de restauración",
    "alt": "Ficha de prueba de restauración con seis campos para completar: VM restaurada srv-prueba-restore, tiempo total en horas y minutos, modo de transporte NBD, HotAdd o SAN, tamaño en GB, datos y servicios verificados sí o no, y snapshots colgados: ninguno en el original. Al costado, la regla 3-2-1: 3 copias de los datos, 2 medios distintos, 1 fuera del sitio. Nota: con el tiempo anotado sabés cuánto tarda volver el día que se rompe algo.",
    "caption": "Tiempo, modo y tamaño: lo que vas a necesitar el día del problema."}],
  [C("VADP y CBT",
     "Las APIs de protección de datos de vSphere (VADP) permiten que un producto de backup copie el disco de una VM encendida sin agente adentro. Changed Block Tracking (CBT) le dice qué bloques cambiaron desde el último backup, para copiar solo eso.",
     "El job pide un snapshot, copia los bloques que marca CBT y borra el snapshot. Veeam, Nakivo, Altaro y otros trabajan así. El ESXi gratuito no expone VADP: ahí solo queda un agente dentro de cada VM.",
     "En una cadena de locales, el incremental nocturno del servidor de video copia solo lo que cambió en el día, y termina antes de que abran."),
   C("Modos de transporte: NBD, HotAdd y SAN",
     "Son los caminos por los que viajan los datos del disco al repositorio. Elegir bien define cuánto tarda un backup y, sobre todo, una restauración.",
     "NBD (o NBDSSL, cifrado) va por la red de gestión: es el más simple, pero en 1 GbE puede rendir 10 a 20 MB/s según una guía vieja de Veeam. HotAdd usa un proxy virtual en el mismo host que monta el disco, y no anda con discos IDE. SAN usa un proxy físico que ve la LUN. El log del job dice cuál se usó.",
     "Una restauración de 2 TB por NBD en 1 GbE puede llevar más de un día. Con un proxy virtual para HotAdd, el mismo cliente vuelve en horas."),
   C("Restauración aislada y regla 3-2-1",
     "Un backup que nunca se restauró no está probado. La regla 3-2-1 (tres copias, dos medios, una fuera del sitio) cubre la pérdida del sitio; la restauración de prueba cubre el \"no sé si anda\".",
     "Se crea un vSwitch sin uplinks con un port group aislado, se restaura la VM con otro nombre ahí, se prende y se verifica. Se anota el tiempo total, el modo de transporte y el tamaño, y se confirma que el job no dejó snapshots colgados en la original.",
     "Una vez por trimestre restaurás el servidor de control de acceso de un edificio en el Prado como srv-acceso-restore, aislado. Ya sabés que vuelve en 40 minutos, y se lo podés decir al administrador.")],
  """
### Un poco de historia

Antes de vSphere 4, respaldar VMs a nivel host era incómodo: se montaban los discos en un servidor intermedio y se copiaban enteros. Con vSphere 4, en 2009, VMware presentó VADP, las APIs de protección de datos, y Changed Block Tracking, que lleva la cuenta de qué bloques cambiaron. Desde entonces casi todos los productos de backup de VMs funcionan así.

La regla 3-2-1 viene de antes y no es de VMware: tres copias de los datos, en dos medios distintos, con una fuera del sitio. En 2026 apareció una duda nueva: Broadcom retiró las descargas públicas del VDDK, la librería de discos que usan varias herramientas; ninguna fuente leída confirma si afecta a productos de backup, así que conviene preguntarle al proveedor.

### Cómo funciona

Un job de backup con VADP sigue siempre la misma secuencia. Primero pide un snapshot de la VM: el disco base queda congelado y coherente mientras la VM sigue escribiendo en el delta. Después copia los bloques del disco base; en un incremental, CBT le dice cuáles cambiaron y se copian solo esos. Al final borra el snapshot.

La copia viaja por uno de tres modos. NBD, o NBDSSL cifrado, usa la red de gestión del host: es el más simple y el más lento. HotAdd usa un proxy virtual en el mismo host que monta el disco como si fuera propio; no anda con discos IDE. SAN usa un proxy físico que ve la LUN directo. Un proxy virtual también acorta las restauraciones.

Si el job falla antes de borrar el snapshot, queda colgado y crece: por eso después de cada prueba se revisa la VM original. Y si el host tiene la licencia gratuita, no hay VADP: solo queda un agente dentro de cada VM.

El último paso no es del producto, es tuyo: restaurar con otro nombre en un port group sin uplinks, prenderla, verificar datos y servicios, y anotar cuánto tardó.
""",
  [{"file": "7-t1.svg", "after": "Al final borra el snapshot",
    "alt": "Animación en cuatro tiempos con un host ESXi que tiene la VM srv-video y su disco, y a la derecha el producto de backup y el repositorio. 1: el producto de backup pide por la API de vSphere (VADP) un snapshot de la VM, que congela el disco base. 2: Changed Block Tracking marca los tres bloques que cambiaron desde el último backup y solo esos viajan al repositorio, por NBD, HotAdd o SAN. 3: terminada la copia, el job borra el snapshot; si el job fallara antes, el snapshot quedaría colgado. 4: la prueba: la VM se restaura como srv-prueba-restore en el port group Restore-Aislado, sin uplinks.",
    "caption": "Snapshot, copia de lo cambiado, borrado y la prueba que lo confirma."}],
  S("Port group aislado para pruebas de restauración",
    "Crea un vSwitch sin uplinks y su port group para restaurar VMs sin que salgan a la red, si todavía no existen, y avisa si alguien le agregó una placa física.",
    [("VSWITCH", "vSwitch-Aislado", "vSwitch sin uplinks"),
     ("PORTGROUP", "Restore-Aislado", "Port group donde se conecta la VM restaurada")],
    r'''
#!/bin/sh
# IES Training - VMware - Port group aislado para restaurar
# Crea un vSwitch SIN uplinks: lo que se conecte ahi no sale del host.
VSW="{{VSWITCH}}"
PG="{{PORTGROUP}}"
if esxcli network vswitch standard list | grep -q "Name: $VSW\$"; then
  echo "Ya existe $VSW"
else
  esxcli network vswitch standard add -v "$VSW" && echo "Creado $VSW"
fi
if esxcli network vswitch standard portgroup list | awk -v p="$PG" '$1==p {f=1} END {exit !f}'; then
  echo "Ya existe el port group $PG"
else
  esxcli network vswitch standard portgroup add -p "$PG" -v "$VSW" && echo "Creado $PG"
fi
UPL=$(esxcli network vswitch standard list -v "$VSW" | awk -F': ' '/Uplinks:/ {print $2}')
if [ -n "$UPL" ]; then
  echo "Ojo: $VSW tiene uplinks ($UPL). Ya no esta aislado: sacalos antes de restaurar."
  exit 1
fi
echo "OK: $VSW sin uplinks."
echo "Checklist: restaurar con otro nombre, placa de red en $PG, prender, verificar,"
echo "anotar tiempo total, modo (NBD, HotAdd o SAN) y tamano, y borrar la restaurada."
echo "Listo: $PG aislado en $VSW. Verifica con esxcfg-vswitch -l"
''',
    ["La restauración se hace con el producto de backup del cliente: el script solo prepara la red aislada.",
     "Nunca restaures sobre la VM original ni la conectes a la red de producción.",
     "Al terminar, confirmá que el job no dejó snapshots en la VM original (lección 6)."]))

# =====================================================================================  8
L("8",
  {"file": "8.svg", "alt": "Arriba, la fórmula del permiso: quién, usuario o grupo, como tecnico.prueba; más qué rol, conjunto de privilegios, como Soporte-Lectura; más dónde, objeto del inventario, como una carpeta o clúster; igual a permiso, que con Propagate también vale en los hijos. Abajo, vCenter (VCSA), el appliance que gestiona varios hosts, con Single Sign-On en el dominio vsphere.local y las funciones de clúster, vMotion, HA y DRS. En rojo, administrator@vsphere.local: la llave maestra va al gestor de contraseñas y no se usa a diario. Notas: cada técnico con su usuario para que cada cambio quede a su nombre; en vSphere 8 el tamaño Tiny de la VCSA pide 14 GB de RAM.",
   "caption": "Un permiso es usuario, rol y objeto; la llave maestra se guarda."},
  [{"file": "8-paso2.svg", "step": 2, "after": "Agregale solo el privilegio",
    "alt": "En Administration, Access Control, Roles: el rol de fábrica Read-only, que ve inventario y configuración sin cambiar nada, se clona como Soporte-Lectura, en verde, con todo lo de Read-only más un privilegio: Virtual machine, Interaction, Console interaction. Puede abrir la consola de una VM y no puede apagar, borrar ni cambiar hardware. Notas: se clona en vez de editar para que los roles de fábrica queden intactos; cada privilegio que se suma es algo más que ese usuario puede romper.",
    "caption": "Clonar Read-only y sumar solo la consola."},
   {"file": "8-paso3.svg", "step": 3, "after": "sobre una carpeta o clúster de prueba",
    "alt": "Árbol del inventario: Datacenter; la carpeta Lab-Pruebas con el permiso puesto ahí, y sus VMs vm-prueba y vm-prueba-2, en verde, que lo heredan; la carpeta Produccion con srv-video, que el usuario no ve. Al lado, la ventana Add Permission con User tecnico.prueba, Role Soporte-Lectura y Propagate to children marcado. Nota: después se cierra sesión y se entra como tecnico.prueba@vsphere.local para ver qué ve y qué no.",
    "caption": "El permiso en la carpeta baja a sus VMs; lo de al lado no se ve."}],
  [C("vCenter (VCSA)",
     "Un host solo se gestiona bien con el Host Client, pero varios hosts necesitan un punto central. vCenter es ese punto, y es el que habilita el clúster, vMotion, HA y DRS.",
     "Hoy se instala como appliance, la VCSA, una VM con todo adentro. Pide RAM en serio: en vSphere 8 el tamaño Tiny pide 14 GB. Los logs del appliance quedan en /var/log/vmware.",
     "Un cliente pasa de un servidor a tres en su planta de Paso Carrasco: con la VCSA en uno de ellos, ves los tres hosts en un solo inventario y podés armar el clúster."),
   C("vCenter Single Sign-On y administrator@vsphere.local",
     "SSO es el que dice quién sos: autentica a los usuarios de vCenter, con el dominio por defecto vsphere.local. Al principio solo administrator@vsphere.local puede entrar, y es la llave maestra de todo.",
     "Se crean usuarios en Administration > Single Sign On > Users and Groups, o se suma Active Directory como fuente de identidad. La contraseña de administrator@vsphere.local va al gestor de contraseñas de la empresa y no se usa para el día a día. El dominio se elige al instalar y después no se cambia sin trabajo.",
     "En la entrega de una obra, la clave de administrator@vsphere.local queda en el gestor de IES y del cliente, no en un chat. Cada técnico entra con el suyo."),
   C("Rol y permiso",
     "Con un usuario compartido no se sabe quién hizo qué, y cualquier error puede tumbar todo. El modelo de permisos deja a cada uno con lo justo, sobre los objetos que le tocan.",
     "Un permiso es usuario o grupo, más un rol (un conjunto de privilegios), asignado sobre un objeto del inventario. Con Propagate to children baja a los hijos. Los roles de fábrica no se editan: se clonan, como Read-only a Soporte-Lectura con Console interaction.",
     "El técnico de soporte de primera línea de un cliente puede abrir la consola del servidor de video para ver qué pasa, pero no puede apagarlo por error.")],
  """
### Un poco de historia

El primer vCenter se llamaba VirtualCenter, salió en 2003 y corría sobre Windows. Con vSphere 5.0, en 2011, apareció el vCenter Server Appliance, la VCSA, una VM con todo adentro, y desde vSphere 7, en 2020, es la única forma. vCenter Single Sign-On llegó con vSphere 5.1, en 2012, para que todos los componentes usen el mismo inicio de sesión.

El appliance fue pidiendo más recursos con cada versión. William Lam cuenta que el tamaño Tiny pasó de 12 a 14 GB de RAM en vSphere 8, y que en laboratorio lo corrió con 10 GB, algo que no está soportado.

### Cómo funciona

Entrar a vCenter tiene dos pasos separados. El primero es la autenticación: SSO verifica usuario y contraseña contra su dominio, vsphere.local por defecto, o contra una fuente de identidad como Active Directory. Al desplegar vCenter, al principio solo administrator@vsphere.local puede entrar.

El segundo es la autorización: qué puede hacer ese usuario y dónde. Un permiso une tres cosas: un usuario o grupo, un rol, que es un conjunto de privilegios, y un objeto del inventario. Con Propagate to children, el permiso baja a todo lo que cuelga de ese objeto. Donde no hay permiso, el objeto ni siquiera aparece.

Los roles de fábrica, como Read-only o Administrator, no se editan: se clonan y se ajustan. Soporte-Lectura es Read-only más Console interaction: puede abrir la consola de una VM, pero no apagarla, borrarla ni cambiarle hardware. Un error de soporte no puede tumbar un servidor si su rol no lo permite.

Con cada técnico en su usuario, cada tarea queda registrada a su nombre. administrator@vsphere.local se guarda en el gestor de contraseñas de la empresa y se usa solo para lo que de verdad lo necesita.
""",
  [{"file": "8-t1.svg", "after": "Donde no hay permiso, el objeto ni siquiera aparece",
    "alt": "Animación en cuatro tiempos. A la izquierda el usuario tecnico.prueba y vCenter SSO; a la derecha el inventario con dos carpetas: Lab-Pruebas, con el rol Soporte-Lectura propagado, y Produccion, sin permiso. 1: el usuario entra y SSO valida usuario y clave en vsphere.local. 2: en Lab-Pruebas ve las VMs y puede abrir la consola. 3: intenta apagar vm-prueba-2 y se rechaza porque el rol no tiene ese privilegio. 4: la carpeta Produccion directamente no aparece para ese usuario.",
    "caption": "SSO dice quién sos; el permiso, qué ves y qué podés tocar."}])

# =====================================================================================  9
L("9",
  {"file": "9.svg", "alt": "Tabla comparativa de vMotion, que mueve una VM encendida a otro host; HA, en ámbar, que reinicia en otro host las VMs de un host caído; y DRS, que reparte la carga de CPU y memoria. Corta el servicio: vMotion no, copia memoria y estado en vivo; HA sí, minutos, lo que tarda en arrancar, en rojo; DRS no, usa vMotion. Necesita vCenter: vMotion sí para lanzarla; HA no para actuar, anda con vCenter caído; DRS sí, siempre. Qué pide: vMotion almacenamiento compartido y vmk de vMotion; HA capacidad libre en los otros hosts; DRS empezar en manual o parcial. Notas: crear el clúster es libre y activar HA o DRS depende de la licencia; al cliente se le dice HA reinicia en otro host, nunca no se cae.",
   "caption": "vMotion no corta, HA corta minutos, DRS reparte. Y lo que cada uno necesita."},
  [{"file": "9-paso3.svg", "step": 3, "after": "Elegí una VM de prueba encendida",
    "alt": "Dos hosts del Cluster-Lab, esxi-lab01 con vm-prueba encendida y esxi-lab02 con el lugar de destino punteado. Una flecha lleva memoria y estado de un host al otro por la red de vMotion, en VLAN propia, entre los vmk de vMotion de cada host. Los dos hosts se conectan al mismo datastore compartido, donde el disco no se mueve. Notas: los dos hosts tienen que ver el mismo datastore; si la migración falla, la VM vuelve sola a su host de origen. Abajo: Migrate, Change compute resource only, destino el otro host.",
    "caption": "Viaja la memoria; el disco se queda en el datastore compartido."},
   {"file": "9-paso4.svg", "step": 4, "after": "dejá un ping continuo a la VM",
    "alt": "El comando ping -t 192.168.88.50 y una salida de ejemplo con cinco respuestas, una con tiempo de 3 ms durante el cambio de host. Una línea de tiempo en verde: la VM sigue respondiendo en esxi-lab01 y después en esxi-lab02, con una franja ámbar mínima en el cambio de host. Notas: anotar cuántos pings se perdieron, cero o casi, y el tiempo de la migración en Monitor, Tasks; comparar con HA, donde la VM se reinicia y el ping se corta minutos.",
    "caption": "Durante un vMotion el ping casi no se entera."}],
  [C("vMotion",
     "Permite mover una VM encendida de un host a otro sin apagarla: para hacer mantenimiento de un host, repartir carga o liberar un servidor, sin corte para los usuarios.",
     "Se lanza desde vCenter con Migrate. Con Change compute resource only cambia solo el host, y el disco tiene que estar en un datastore compartido. Cada host necesita un vmk con el servicio vMotion, en su VLAN. Si la migración falla, la VM vuelve a su lugar.",
     "Antes de cambiar una fuente del servidor 1 en un sanatorio, movés sus VMs al servidor 2 con vMotion en horario de atención. El ping continuo pierde, como mucho, un paquete."),
   C("vSphere HA",
     "Cubre la caída de un host: si un servidor se apaga de golpe, sus VMs se reinician solas en los otros hosts del clúster. No evita el corte, lo acorta a lo que tardan en arrancar.",
     "Se activa en el clúster, si la licencia lo permite. Los hosts se vigilan entre sí y eligen un primario; funciona aunque vCenter esté caído. El control de admisión reserva capacidad para la falla; sin DRS conviene dejar lugar libre de sobra en cada host.",
     "En una clínica con tres hosts, se quema la fuente de uno a las 3 de la mañana. A los pocos minutos, el servidor de la central telefónica ya arrancó en otro host. Al cliente le explicaste antes: reinicia, no evita el corte."),
   C("DRS",
     "Reparte la carga de CPU y memoria entre los hosts del clúster moviendo VMs con vMotion. También vacía un host cuando entra en modo mantenimiento.",
     "Necesita vCenter y licencia. Tiene tres niveles: Manual, que solo recomienda; Partially Automated; y Fully Automated. En clústeres chicos conviene arrancar en manual o parcial y mirar qué recomienda antes de automatizar. Solo mira CPU y memoria.",
     "En el clúster de un cliente con grabación y ERP, DRS en Partially Automated una semana: ves que siempre recomienda separar dos VMs pesadas y recién ahí lo pasás a automático.")],
  """
### Un poco de historia

vMotion salió en 2003, junto con el primer VirtualCenter, y fue la función que convenció a muchos de virtualizar: mover un servidor encendido de una máquina física a otra parecía magia. En 2006, con VMware Infrastructure 3, llegaron HA, para reiniciar VMs cuando se cae un host, y DRS, para repartir la carga automáticamente.

Los conceptos no cambiaron desde entonces, aunque los detalles internos sí. Lo que cambió en 2024 es el acceso: crear un clúster sigue siendo libre, pero activar HA o DRS depende de la licencia del cliente.

### Cómo funciona

vMotion copia la memoria de la VM mientras sigue andando. En una primera pasada copia toda la memoria por la red de vMotion; como la VM sigue escribiendo, vuelve a copiar las páginas que cambiaron, en pasadas cada vez más chicas. Cuando queda muy poco, pausa la VM un instante, pasa el estado y la arranca en el destino. Si cambia solo el host, el disco no se mueve: tiene que estar en un datastore compartido. Si algo falla, la VM vuelve a su host original.

HA trabaja de otra forma. Los hosts del clúster se vigilan entre sí y uno queda como primario. Si un host deja de responder, HA arranca sus VMs en los otros hosts. Hay corte: el tiempo que tardan en arrancar. Como lo hacen los hosts, funciona aunque vCenter esté caído. El control de admisión reserva capacidad para que haya dónde arrancarlas, y con VMware Tools HA también puede vigilar cada VM por su latido.

DRS necesita vCenter: mira CPU y memoria de cada host y mueve VMs con vMotion para equilibrar, o vacía un host que entra en mantenimiento. Arranca en Manual, Partially Automated o Fully Automated.

Si los hosts tienen CPUs de generaciones distintas, EVC iguala lo que ven las VMs para que vMotion funcione entre ellos.
""",
  [{"file": "9-t1.svg", "after": "pasa el estado y la arranca en el destino",
    "alt": "Animación en cuatro tiempos con dos hosts, esxi-lab01 y esxi-lab02, la memoria de la VM en cada uno y un datastore compartido abajo. 1: en una primera pasada toda la memoria se copia por la red de vMotion al destino. 2: como la VM sigue escribiendo, tres páginas cambian en el origen y se vuelven a copiar. 3: con pocas páginas pendientes, la VM se pausa un instante, se pasa el estado y arranca en el destino. 4: la VM corre en esxi-lab02 y su disco nunca se movió del datastore compartido.",
    "caption": "Pasadas de memoria cada vez más chicas y un cambio de host de un instante."},
   {"file": "9-t2.svg", "after": "HA arranca sus VMs en los otros hosts",
    "alt": "Animación en cuatro tiempos con tres hosts de un clúster: esxi-lab01 con la VM ERP, esxi-lab02 con VM video y VM telefonía, esxi-lab03 con VM acceso. 1: los hosts se vigilan entre sí con latidos. 2: esxi-lab02 se queda sin energía y sus dos VMs se caen. 3: HA detecta la falla y arranca VM video en esxi-lab01 y VM telefonía en esxi-lab03, aunque vCenter esté caído. 4: las VMs vuelven a andar; una barra abajo muestra los minutos sin servicio: HA no evita el corte, lo acorta.",
    "caption": "HA reinicia en otro host: hay corte, pero corto."}])

# =====================================================================================  10
L("10",
  {"file": "10.svg", "alt": "Arriba, en rojo: antes de todo, backup del vCenter, de la configuración del host y de las VMs críticas, y la Compatibility Guide de la versión destino. Cuatro pasos numerados de Lifecycle Manager: 1 Check Compliance, compara el host con la imagen y no cambia nada; 2 Run Pre-check, revisa que se pueda aplicar y no cambia nada; 3 Stage, baja los paquetes al host todavía sin aplicar; 4 Remediate, en ámbar, modo mantenimiento, aplica y reinicia. Con el staging hecho, el host pasa menos tiempo en mantenimiento. Notas: vLCM vive dentro de vCenter en Cluster, Updates, Image, y en vSphere 9 se retiran las baselines; el rollback de 8 a 7 solo es posible si no se tocaron los bootbanks.",
   "caption": "Backup, después compliance, pre-check, stage y recién al final remediate."},
  [{"file": "10-paso1.svg", "step": 1, "after": "con el parche oficial",
    "alt": "Seis pasos en orden para un host suelto: 1 vmware -vl para anotar la versión de partida; 2 esxcli system maintenanceMode set -e true, con las VMs apagadas o movidas antes, en ámbar; 3 esxcli software sources profile list con el depot para ver qué perfiles trae el parche; 4 esxcli software profile update con --dry-run, que simula sin aplicar nada, en verde; 5 esxcli software profile update y reboot, solo en el host de laboratorio, en rojo; 6 vmware -vl y maintenanceMode set -e false para verificar y salir de mantenimiento, en verde. Abajo, el depot y el perfil de ejemplo.",
    "caption": "Primero mantenimiento, después dry-run, y recién ahí el parche."}],
  [C("vSphere Lifecycle Manager y el modelo de imágenes",
     "Actualizar host por host a mano es lento y deja hosts en versiones distintas. vLCM, que vive dentro de vCenter, define una imagen para todo el clúster y lleva cada host a esa imagen.",
     "En Cluster > Updates > Image: Check Compliance compara sin cambiar nada, Run Pre-check revisa que se pueda, Stage baja los paquetes y Remediate aplica. Sin internet se usa UMDS o se importan los paquetes a mano. En vSphere 9 se retiran las baselines y queda solo el modelo de imágenes.",
     "En un clúster de tres hosts de un cliente logístico, Check Compliance muestra que uno quedó con un parche menos. Remediate lo lleva a la misma imagen que los otros dos."),
   C("Staging y modo mantenimiento",
     "Mientras un host está en modo mantenimiento no corre VMs: es el estado seguro para parchear. Cuanto menos dure, mejor. El staging baja los paquetes antes, para que ese tiempo sea solo el de aplicar y reiniciar.",
     "Se hace Stage en todos los hosts primero, sin cortar nada. Después se remedia de a uno: el host entra en mantenimiento, DRS mueve sus VMs (o se mueven a mano), se aplica, reinicia y sale. Un host por vez, para que siempre quede capacidad.",
     "Un sábado a la mañana en un clúster de un supermercado: staging el viernes a la tarde, y el sábado cada host pasa unos pocos minutos en mantenimiento mientras las cajas siguen facturando."),
   C("Actualizar un host suelto con esxcli y --dry-run",
     "Sin vCenter, un host se actualiza con el depot .zip oficial y esxcli. El --dry-run deja ver qué se va a instalar y quitar antes de tocar nada.",
     "Con las VMs apagadas o movidas: `esxcli system maintenanceMode set -e true`, `esxcli software sources profile list -d <depot>` para ver perfiles, `esxcli software profile update ... --dry-run` para simular, y recién después el update y el reboot. Antes, backup; y el rollback de 8 a 7 solo se puede si no se tocaron los bootbanks.",
     "En el único host de una oficina chica en Salto, el dry-run muestra que el parche quita un driver de la NIC que usa el cliente. Frenás, revisás la Compatibility Guide y evitás dejarlo sin red.")],
  """
### Un poco de historia

Durante años los hosts se parcheaban con Update Manager, un componente aparte, con baselines: listas de parches que cada host tenía que tener. Con vSphere 7, en 2020, llegó vSphere Lifecycle Manager, vLCM, dentro de vCenter y sin instalación extra, con un modelo nuevo de imágenes: se define cómo tiene que quedar el host y vLCM lo lleva ahí.

Los dos modelos convivieron unos años. Con vSphere 9, VMware retira las baselines y queda solo el de imágenes, con hasta cuatro configuraciones de imagen extra por clúster para hardware mixto.

### Cómo funciona

Una imagen describe la versión de ESXi del clúster y los componentes que van con ella. vLCM trabaja en cuatro operaciones. Check Compliance compara cada host con la imagen y no cambia nada. Remediation Pre-check revisa que la actualización se pueda aplicar. Stage baja los paquetes a los hosts, todavía sin aplicar. Remediate aplica: pone el host en modo mantenimiento, instala y reinicia.

El staging existe para acortar el tiempo en mantenimiento. Se hace en todos los hosts primero, porque no corta nada. Después se remedia de a un host: entra en mantenimiento, DRS mueve sus VMs con vMotion a los otros, se aplica el parche, reinicia y sale. Las VMs siguen andando en el resto del clúster y siempre queda capacidad.

Un host sin vCenter se actualiza con esxcli y el depot .zip oficial: modo mantenimiento, ver los perfiles del depot, simular con `--dry-run` y recién después aplicar y reiniciar.

Antes de cualquier actualización: backup del vCenter, de la configuración de cada host y de las VMs críticas, y la Compatibility Guide revisada para la versión destino. El rollback de 8 a 7 solo es posible si no se tocaron los bootbanks.
""",
  [{"file": "10-t1.svg", "after": "Las VMs siguen andando en el resto del clúster",
    "alt": "Animación en cuatro tiempos con tres hosts en 8.0 U3. 1: en el staging, los paquetes bajan a los tres hosts sin aplicarse. 2: esxi-lab01 entra en modo mantenimiento y sus dos VMs, video y ERP, se mueven con vMotion a los otros hosts. 3: sin VMs encima se aplica el parche y el host reinicia, mientras las VMs siguen andando en los otros. 4: el host vuelve actualizado, sale de mantenimiento y el siguiente host queda marcado como el próximo. Abajo, el recordatorio de hacer backup antes de empezar.",
    "caption": "Stage en todos, remediate de a uno, con las VMs en los otros hosts."}],
  S("Chequeo previo y simulación de un parche en un host suelto",
    "Muestra la versión, se niega a seguir si hay VMs encendidas, pone el host en mantenimiento, lista los perfiles del depot y simula la actualización con --dry-run. La aplicación real queda comentada.",
    [("DEPOT", "/vmfs/volumes/datastore1/VMware-ESXi-8.0U3-depot.zip", "Ruta del depot .zip oficial en el datastore"),
     ("PERFIL", "ESXi-8.0U3-standard", "Perfil del depot a aplicar")],
    r'''
#!/bin/sh
# IES Training - VMware - Chequeo previo y dry-run de un parche
# Solo en un host de laboratorio. Antes: backup del host y de las VMs.
DEPOT="{{DEPOT}}"
PERFIL="{{PERFIL}}"
echo "== Version actual =="
vmware -vl
[ -f "$DEPOT" ] || { echo "No encuentro el depot $DEPOT"; exit 1; }
PRENDIDAS=0
for ID in $(vim-cmd vmsvc/getallvms | awk 'NR>1 && $1 ~ /^[0-9]+$/ {print $1}'); do
  vim-cmd vmsvc/power.getstate "$ID" | grep -q "Powered on" && { echo "Vmid $ID esta encendida"; PRENDIDAS=1; }
done
[ "$PRENDIDAS" = "1" ] && { echo "Apaga o move las VMs antes. No sigo."; exit 1; }
if esxcli system maintenanceMode get | grep -q Enabled; then
  echo "El host ya estaba en mantenimiento"
else
  esxcli system maintenanceMode set -e true && echo "Host en mantenimiento"
fi
esxcli software sources profile list -d "$DEPOT"
esxcli software profile get
echo "== Simulacion: no aplica nada =="
esxcli software profile update -d "$DEPOT" -p "$PERFIL" --dry-run
# Para aplicar de verdad, solo en laboratorio, y despues reiniciar:
# esxcli software profile update -d "$DEPOT" -p "$PERFIL"
# reboot
echo "Listo: dry-run hecho y host en mantenimiento. Al terminar: esxcli system maintenanceMode set -e false"
''',
    ["No aplica el parche: la línea que lo hace queda comentada a propósito.",
     "Deja el host en modo mantenimiento: si no vas a seguir, sacalo con esxcli system maintenanceMode set -e false.",
     "Con vCenter, el camino es Lifecycle Manager: Check Compliance, Pre-check, Stage y Remediate."]))

# =====================================================================================  11
L("11",
  {"file": "11.svg", "alt": "Cuatro tarjetas, una por tecla de esxtop. c, CPU: %RDY, el tiempo que la VM esperó una CPU física libre; alto quiere decir fila de CPU, no falta de vCPU. m, memoria: MCTLSZ y SWCUR, balloon y swap del host; si crecen, al host le falta memoria. u, disco: DAVG, KAVG y GAVG, latencia del almacenamiento y del host; DAVG alto apunta al storage y KAVG alto a la cola del host. n, red: %DRPTX y %DRPRX, paquetes descartados; mayores a cero, mirar NIC y vSwitch. Notas: ninguna fuente da un umbral universal, se compara con un día normal del cliente; antes de opinar, vmkernel.log y vmkwarning.log en /var/run/log.",
   "caption": "Cada sospechoso tiene su tecla y su columna."},
  [{"file": "11-paso2.svg", "step": 2, "after": "Grabá un minuto en modo batch",
    "alt": "El comando esxtop -b -a -d 5 -n 12 redirigido a un CSV en datastore1 con hostname, fecha y hora en el nombre. Cinco tarjetas explican cada parte: -b modo batch, escribe en vez de mostrar; -a todos los contadores; -d 5 cada 5 segundos una muestra; -n 12, 12 muestras, 12 por 5 segundos es un minuto; y la redirección al datastore. Una fila de doce casilleros de 5 a 60 segundos. Nota: ese CSV es la prueba y se compara con el de un día normal.",
    "caption": "Doce muestras de cinco segundos: un minuto guardado."},
   {"file": "11-paso3.svg", "step": 3, "after": "Buscá errores recientes en los logs",
    "alt": "Tres archivos en /var/run/log: vmkernel.log, el núcleo con discos, rutas, red y drivers, primero; vmkwarning.log, solo las advertencias del núcleo, segundo; y hostd.log, el agente del host, si hace falta. Una terminal con grep -i -E de error, fail y lost sobre vmkernel.log con tail de 30 líneas, y tail de 50 líneas de vmkwarning.log. Notas: en vCenter el equivalente es vpxd; si el host arranca de SD o USB, estos logs viven en memoria y se pierden al reiniciar.",
    "caption": "vmkernel.log primero, vmkwarning.log después."}],
  [C("%RDY",
     "Una VM con varias vCPU tiene que esperar a que haya CPUs físicas libres para correr. %RDY mide ese tiempo de espera: es la diferencia entre \"le falta CPU\" y \"hay fila para usar la CPU\".",
     "En esxtop, tecla `c`, columna %RDY por VM, junto a %USED. Un %RDY alto indica contención: demasiadas vCPU repartidas en pocos núcleos físicos. Agregarle vCPU a esa VM suele empeorarlo. No hay umbral universal: se compara con un día normal del mismo host.",
     "El servidor de video de un cliente \"anda lento\" a la noche. %RDY sube cuando arranca el backup de otra VM con 8 vCPU: le bajás vCPU a esa y la grabación vuelve a la normalidad."),
   C("DAVG, KAVG y GAVG",
     "Separan dónde se pierde el tiempo de una operación de disco: GAVG es lo que siente la VM, DAVG lo que tarda el almacenamiento y KAVG lo que tarda el propio host.",
     "En esxtop, tecla `u`, columnas DAVG/cmd, KAVG/cmd y GAVG/cmd. GAVG = DAVG + KAVG. Si DAVG es alto, mirá el storage: controladora, red de almacenamiento, NAS o SAN. KAVG tendría que estar cerca de cero; si sube, hay encolamiento en el host.",
     "Las VMs de un cliente se ponen lentas a las 2 de la mañana: DAVG se dispara mientras el NAS hace su propia tarea de mantenimiento. KAVG en cero confirma que el host no tiene la culpa."),
   C("Modo batch y línea base",
     "Mirar esxtop en vivo sirve para orientarse, pero un número sin comparación no dice nada. El modo batch guarda los contadores en un CSV para revisarlos con calma y compararlos.",
     "`esxtop -b -a -d 5 -n 12 > archivo.csv` graba un minuto: 12 muestras cada 5 segundos, con todos los contadores. Se guarda en el datastore con host y fecha en el nombre. Los valores normales de %RDY y DAVG de cada cliente van a su ficha: esa es la línea base.",
     "En la puesta en marcha de un cliente nuevo grabás un minuto de esxtop un día tranquilo. Seis meses después, ante \"anda lento\", tenés contra qué comparar.")],
  """
### Un poco de historia

esxtop es la versión de ESXi de top, el monitor de procesos de Unix de mediados de los ochenta: una tabla que se actualiza sola con lo que pasa en el sistema. La diferencia es que esxtop mira lo que importa en un hipervisor: cuánto espera cada VM por CPU, cuánta memoria le saca el host, cuánto tarda cada disco.

Las fuentes coinciden en el método: medir y leer los logs antes de opinar. William Lam cuenta el caso de un procesador de escritorio no soportado que arrancaba con un parámetro forzado y después tenía cuelgues de red; los avisos estaban en vmkernel.log y vmkwarning.log desde el principio.

### Cómo funciona

esxtop se abre por SSH y se maneja con teclas, que distinguen mayúsculas: `c` CPU, `m` memoria, `u` disco por dispositivo, `v` disco por VM, `n` red, `f` campos, `h` ayuda y `q` salir.

En CPU, %RDY es el tiempo que una VM estuvo lista para correr esperando una CPU física. Alto significa fila: hay más vCPU que núcleos libres. En memoria, MCTLSZ muestra cuánto recuperó el balloon de VMware Tools y SWCUR cuánto mandó el host a swap; si crecen, al host le falta memoria.

En disco, el tiempo de cada operación se parte en dos. KAVG es lo que la operación pasa dentro del VMkernel; DAVG, lo que tarda el dispositivo de almacenamiento. Lo que siente la VM es la suma: GAVG = DAVG + KAVG. KAVG debería estar cerca de cero; si DAVG es el grande, el problema está en el storage y no en el host.

En red, %DRPTX y %DRPRX muestran paquetes descartados. El modo batch, `esxtop -b -a -d 5 -n 12`, guarda un minuto en CSV. Y los logs del host viven en /var/run/log: vmkernel.log y vmkwarning.log primero. Ninguna fuente da un umbral universal: se compara con un día normal.
""",
  [{"file": "11-t1.svg", "after": "el problema está en el storage y no en el host",
    "alt": "Animación en cuatro tiempos con tres cajas en fila: la VM, el VMkernel del host y el almacenamiento, y abajo una barra con el tiempo de la lectura. 1: la VM pide una lectura y arranca el reloj de GAVG. 2: la lectura pasa por la cola del VMkernel, un tramo corto llamado KAVG, que debería ser casi cero. 3: llega al almacenamiento y vuelve; ese tramo, DAVG, es el más largo de la barra, y GAVG queda como la suma de KAVG y DAVG. 4: como DAVG es el grande, la demora está en el almacenamiento y no en el host.",
    "caption": "KAVG es el host, DAVG el storage, GAVG lo que siente la VM."}],
  S("Un minuto de esxtop y los errores recientes del host",
    "Graba un minuto de esxtop en modo batch a un CSV del datastore, con host y fecha en el nombre, y muestra los errores y advertencias recientes de vmkernel.log y vmkwarning.log.",
    [("DATASTORE", "datastore1", "Datastore donde se guarda el CSV"),
     ("INTERVALO", "5", "Segundos entre muestras"),
     ("MUESTRAS", "12", "Cantidad de muestras (12 x 5 s = 1 minuto)")],
    r'''
#!/bin/sh
# IES Training - VMware - Un minuto de esxtop y logs del host
# Solo lee y guarda un CSV: no cambia la configuracion.
DS="{{DATASTORE}}"
D="{{INTERVALO}}"
N="{{MUESTRAS}}"
[ -d "/vmfs/volumes/$DS" ] || { echo "No existe el datastore $DS"; exit 1; }
CSV="/vmfs/volumes/$DS/esxtop-$(hostname)-$(date +%Y%m%d-%H%M).csv"
echo "Grabando $N muestras cada $D segundos en $CSV ..."
esxtop -b -a -d "$D" -n "$N" > "$CSV"
ls -lh "$CSV"
echo "== Errores recientes en vmkernel.log =="
grep -i -E "error|fail|lost" /var/run/log/vmkernel.log | tail -n 30
echo "== Ultimas advertencias en vmkwarning.log =="
tail -n 50 /var/run/log/vmkwarning.log
echo "Listo: CSV en $CSV. Abrilo despues y compara %RDY y DAVG con la linea base del cliente."
''',
    ["Cada vez que lo pegás crea un CSV nuevo, con la hora en el nombre: no pisa los anteriores.",
     "El CSV con -a es grande: bajalo y borralo del datastore cuando lo hayas guardado en el legajo del cliente.",
     "No interpreta los números: eso se hace comparando con un día normal."]))

# =====================================================================================  12
L("12",
  {"file": "12.svg", "alt": "Tres preguntas numeradas: 1, núcleos, físicos contra licenciables, cuánto se paga de más por el mínimo de 16; 2, funciones, si se usa de verdad vSAN, NSX o DRS o solo el hipervisor; 3, piloto, un host no crítico con 2 o 3 VMs y backup y restauración probados. En verde, renovar tiene sentido si la relación entre físicos y licenciables está cerca de 1 a 1, se usa el stack y hay apps certificadas solo para vSphere. En ámbar, conviene cotizar alternativa si son 2 a 10 hosts con CPUs de menos de 16 núcleos, solo se usa el hipervisor y el costo subió sin funciones nuevas que lo paguen. Abajo: ninguna migración arranca sin piloto, backup verificado y vuelta atrás; Broadcom recomienda VCF 9 o VVF 9 y Introserv y Redress dicen que en clientes chicos la cuenta suele no cerrar.",
   "caption": "Renovar o migrar se decide con núcleos, funciones usadas y un piloto."},
  [{"file": "12-paso2.svg", "step": 2, "after": "Skip Certificate Verification",
    "alt": "Ventana Add: ESXi de Proxmox con ID esxi-lab, Server 192.168.88.20, Username root, Password la del root del ESXi y Skip Certificate Verification marcado y resaltado. A la derecha, Proxmox VE de laboratorio conectado directo al ESXi de laboratorio en 192.168.88.20. Notas: contra el host y no contra vCenter, que es mucho más lento; marcar Skip Certificate Verification solo si el ESXi usa certificado autofirmado. Después aparece esxi-lab en el árbol para elegir la VM apagada, Import, storage de destino y bridge vmbr0.",
    "caption": "Proxmox se conecta directo al host ESXi como si fuera un storage."},
   {"file": "12-paso4.svg", "step": 4, "after": "Si es Linux y no bootea con VirtIO SCSI",
    "alt": "Dos columnas. Linux: arrancar con el disco en VirtIO SCSI; si no bootea, probar el disco en SATA; reconfigurar la IP si la placa cambió de nombre e instalar el agente QEMU. Windows: arrancar con el disco en SATA; instalar los drivers VirtIO desde adentro; cambiar a VirtIO, reconfigurar la IP e instalar el agente QEMU. Abajo: verificar desde la consola de la VM con ip a y ping -c 3 192.168.88.1.",
    "caption": "Linux prueba VirtIO primero; Windows arranca en SATA hasta tener los drivers."}],
  [C("Importador ESXi de Proxmox VE",
     "Proxmox VE trae un importador que se conecta a un host ESXi como si fuera un storage y deja importar sus VMs desde la propia interfaz, sin herramientas de terceros. No depende del VDDK, que Broadcom dejó de ofrecer en 2026.",
     "En Datacenter > Storage > Add > ESXi se carga el host, usuario y contraseña. Conviene conectarlo al host y no a vCenter, que es mucho más lento. No sirve para discos en vSAN ni VMs cifradas, y con snapshots es más lento. Para importaciones grandes, no más de cuatro discos a la vez.",
     "En el laboratorio de IES conectás el Proxmox de prueba al ESXi de banco como esxi-lab y ves la lista de VMs lista para importar."),
   C("Importación en frío o en vivo",
     "El importador permite arrancar la VM mientras se copia (live-import) para cortar menos. Las fuentes no coinciden: el wiki de Proxmox lo ofrece y Thomas-Krenn prefiere apagar e importar en frío, porque si falla se pierde lo escrito.",
     "Por defecto, en frío: la VM se apaga en ESXi, se importa y se prende en Proxmox. Live-import solo con buena red y después de probarlo con una VM de prueba. Nunca la misma VM encendida en los dos lados a la vez.",
     "Un servidor de una academia en Cordón se migra un domingo, en frío. Si algo sale mal, la VM sigue apagada en ESXi, intacta, y se vuelve a prender ahí."),
   C("Preparar la VM antes de importar",
     "La VM cambia de hipervisor: cambian la placa de red, el controlador de disco y los drivers. Prepararla antes evita que no arranque o que quede sin red.",
     "Se desinstala VMware Tools, se anota IP, máscara, gateway y DNS, y en Windows se preparan los drivers VirtIO. El vTPM no se migra: hay que tener a mano las claves de BitLocker. Después se instala el agente QEMU.",
     "Antes de importar el servidor Windows de un estudio, guardás la clave de recuperación de BitLocker en el gestor de contraseñas. Al primer arranque en Proxmox la pide, y la tenés.")],
  """
### Un poco de historia

Proxmox VE nació en 2008, en Austria, como una plataforma de virtualización libre basada en Debian, KVM y contenedores. Su licencia es AGPLv3, con suscripción opcional por socket para soporte y repositorios estables. Desde la versión 8.1 trae un importador de VMs de ESXi, probado contra ESXi 6.5 a 8.0.

En 2026 la pregunta de los clientes es frecuente. Broadcom recomienda pasar a VCF 9 o VVF 9; Introserv y Redress sostienen que en 2 a 10 hosts con CPUs chicas la cuenta suele no cerrar. En agosto y septiembre de 2026 Broadcom retiró además las descargas públicas del VDDK, que usan varias herramientas de migración; el importador de Proxmox no depende de él. Ninguna plataforma reemplaza vSphere en un clic: XCP-ng y SUSE Virtualization son otras opciones.

### Cómo funciona

La decisión se toma con números: núcleos físicos contra licenciables, qué funciones se usan de verdad, como vSAN, NSX o DRS, y un piloto en un host no crítico. Si la relación está cerca de 1 a 1 y se usa el stack, renovar tiene sentido.

El importador de Proxmox se agrega como un storage de tipo ESXi y habla con la API del host. Conviene apuntarlo al host y no a vCenter, que es mucho más lento. Lista las VMs y, con Import, copia sus discos al storage de destino. La API de ESXi tiene pocas conexiones: con más de cuatro discos a la vez se bloquea unos 30 segundos. No sirve para discos en vSAN ni VMs cifradas.

Antes de importar, la VM se apaga en ESXi, se le desinstala VMware Tools y se anota su red: en Proxmox la placa cambia de nombre y de MAC. En Windows se preparan los drivers VirtIO; el vTPM no se migra, así que hay que tener las claves de BitLocker.

Importar en frío es lo más seguro: si algo falla, la VM sigue intacta en ESXi y esa es la vuelta atrás. La regla de oro: nunca encendida en los dos lados a la vez.
""",
  [{"file": "12-t1.svg", "after": "con más de cuatro discos a la vez se bloquea",
    "alt": "Animación en cuatro tiempos con un ESXi de laboratorio a la izquierda y un Proxmox VE a la derecha. 1: en el ESXi, la VM vm-prueba está apagada, sin VMware Tools y con su configuración de red anotada; tiene tres discos. 2: Proxmox se conecta al host ESXi por su API como storage esxi-lab; pasar por vCenter sería mucho más lento. 3: los discos se copian de a pocos, no más de cuatro a la vez, con la VM apagada. 4: la VM arranca en Proxmox en el bridge vmbr0 con el agente QEMU, y en el ESXi queda apagada como vuelta atrás; nunca encendida en los dos lados a la vez.",
    "caption": "Apagada en ESXi, copiada de a pocos discos, prendida en Proxmox."}])

# ------------------------------------------------------------------ salida y chequeos
order = [str(i) for i in range(1, 13)]
out = "/home/claude/ies-training/ilustraciones/vmware/manifest.json"
json.dump({k: M[k] for k in order}, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
s = json.dumps(M, ensure_ascii=False)
print("ok", out, len(M), "lecciones · guiones largos:", "—" in s or "–" in s)
for k in order:
    t = M[k]["teoria_md"]
    w = len(re.findall(r"\w+", t))
    bad = [f["after"] for f in M[k]["teoria_figs"] if t.count(f["after"]) != 1 or not (15 <= len(f["after"]) <= 60)]
    print(k, "palabras", w, "conceptos", len(M[k]["concepts"]), "script" if M[k].get("script_rsc") else "", "teoria_figs mal:" if bad else "", bad if bad else "",
          "" if "### Un poco de historia" in t and "### Cómo funciona" in t else "SIN SUBTITULOS")
