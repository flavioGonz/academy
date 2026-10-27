"""Genera /home/claude/ies-training/ilustraciones/windows/manifest.json (figuras, pasos, conceptos, teoría, figuras de teoría y script PowerShell)."""
import json

M = {}


def L(lid, fig, steps, concepts, teoria, tfig, script):
    M[lid] = {"fig": fig, "steps": steps, "concepts": concepts, "teoria_md": teoria.strip(), "teoria_figs": tfig, "script_rsc": script}


def C(name, para_que, como, ejemplo):
    return {"name": name, "para_que": para_que, "como": como, "ejemplo": ejemplo}


def S(titulo, descripcion, variables, codigo, notas):
    return {"titulo": titulo, "descripcion": descripcion,
            "variables": [{"nombre": n, "valor": v, "detalle": d} for n, v, d in variables],
            "codigo": codigo.strip("\n"), "notas": notas}


# =====================================================================================  1
L("1",
  {"file": "1.svg", "alt": "A la izquierda, la clave del registro HKLM SOFTWARE Microsoft Windows NT CurrentVersion con cuatro valores de ejemplo: EditionID Professional, DisplayVersion 24H2 resaltado, CurrentBuild 26100 y UBR, el parche del mes. A la derecha, lo que cambió desde Windows 11 24H2 y Server 2025 según Get-SmbClientConfiguration: RequireSecuritySignature en True, firma SMB obligatoria en cada conexión, y EnableInsecureGuestLogons en False, Windows 11 Pro ya no entra como invitado. Abajo, una notebook con Windows 11 24H2 intenta abrir \\\\IP\\carpeta en un NAS o grabador viejo sin firma y con invitado, y falla aunque la red esté bien. Nota: primero firmware del NAS o una cuenta con contraseña propia; volver a permitir invitados o quitar la firma deja el puesto más expuesto.",
   "caption": "Edición, versión y build primero: dicen qué reglas de SMB trae ese Windows."},
  [{"file": "1-paso2.svg", "step": 2, "after": "sacá los mismos datos por registro",
    "alt": "Consola de PowerShell con el comando Get-ItemProperty sobre HKLM SOFTWARE Microsoft Windows NT CurrentVersion, filtrado con Select-Object a EditionID, DisplayVersion, CurrentBuild y UBR, y una salida de ejemplo: Professional, 24H2, 26100. Debajo, cuatro tarjetas explican cada valor: edición (Pro, Enterprise, Server), versión (24H2, 25H2), build (la base del sistema) y UBR (sube con cada parche). Nota: va a la planilla de obra junto con los dos valores de SMB.",
    "caption": "Los cuatro datos de winver, leídos por consola y listos para la planilla."},
   {"file": "1-paso5.svg", "step": 5, "after": "Si tenés un NAS o grabador viejo a mano",
    "alt": "Una notebook con Windows 11 24H2 abre \\\\192.168.88.30\\video, de ejemplo. Dos caminos: en rojo, como invitado sin usuario, Pro 24H2 no hace el acceso invitado y la carpeta no abre aunque el NAS responda. En verde, con usuario y contraseña del NAS, abre si el NAS también firma SMB; si igual falla, el siguiente paso es el firmware del NAS o del grabador. Nota: bajar la seguridad del cliente SMB es la última opción.",
    "caption": "Como invitado no abre; con un usuario del equipo, sí."}],
  [C("Edición, versión y build",
     "Windows dejó de ser un producto que cambia cada muchos años: recibe una versión con nombre de año y semestre (23H2, 24H2) y parches todos los meses. Dos equipos que dicen \"Windows 11\" pueden comportarse distinto, y la diferencia está en estos datos.",
     "winver los muestra en pantalla; por consola salen del registro en CurrentVersion: EditionID, DisplayVersion, CurrentBuild y UBR, que es el número del último parche acumulado. Se anotan en la planilla de obra antes que la IP, junto con la configuración del cliente SMB.",
     "Te llaman de un consultorio en el Cordón: \"desde que se actualizó la PC no veo el grabador\". La ficha dice 24H2 y el grabador comparte por SMB sin usuario. Ya tenés la causa más probable sin haber tocado un cable."),
   C("Firma SMB obligatoria",
     "SMB es el protocolo con el que Windows abre carpetas compartidas. Firmar cada mensaje prueba que viene de quien dice y que nadie lo cambió en el camino, algo que antes era opcional para la mayoría de las conexiones.",
     "Desde Windows 11 24H2 y en Windows Server 2025 la firma se exige en todas las conexiones salientes. Se ve con Get-SmbClientConfiguration, en RequireSecuritySignature. Un equipo del otro lado que no sabe firmar queda afuera, y desde el usuario parece una falla de red.",
     "Un NAS doméstico de hace años en una casa de Carrasco, donde el VMS guarda exportaciones, deja de abrir. La solución es actualizar su firmware o reemplazarlo, no apagar la firma en la notebook del cliente."),
   C("Acceso invitado",
     "Permitía entrar a una carpeta compartida sin usuario ni contraseña. Era cómodo, pero no hay forma de saber quién entró ni de firmar la sesión, porque no hay credencial de la que salga una clave.",
     "Windows 11 Pro 24H2 ya no lo hace: EnableInsecureGuestLogons queda en False. La carpeta del NAS o del grabador se abre con un usuario y una contraseña propios de ese equipo, escritos en el Explorador cuando los pide.",
     "Un pendrive enchufado al router de un local de Pocitos servía de \"carpeta común\". Con 24H2 dejó de abrir. Creás un usuario en el router o movés esa carpeta a un equipo que lo soporte, y queda documentado.")],
  """
### Un poco de historia

Desde Windows 10, en 2015, Microsoft trata a Windows como un servicio: en vez de una versión nueva cada varios años, llegan actualizaciones de funciones periódicas, hoy con nombre de año y semestre como 23H2 o 24H2, y parches acumulados todos los meses. Windows 11 salió en 2021 y su versión 24H2 llegó en 2024, el mismo año que Windows Server 2025. Los dos comparten la base, el build 26100.

SMB, el protocolo para compartir carpetas, nació en IBM en los años ochenta y Microsoft lo hizo propio. Durante décadas priorizó que todo conectara con todo: firma opcional e invitados permitidos. Con 24H2, Microsoft cambió esas dos cosas por defecto, y Ned Pyle, de Microsoft, avisó que el NAS viejo \"bajo la escalera\" podía dejar de funcionar.

### Cómo funciona

Windows guarda su identidad en el registro, en HKLM:\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion. EditionID dice la edición, DisplayVersion la versión con nombre (24H2), CurrentBuild la base y UBR, Update Build Revision, cuántos parches acumulados tiene encima. Con esos cuatro datos sabés qué reglas trae ese equipo.

Abrir \\\\IP\\carpeta es una conversación SMB en tres tiempos. Primero se negocia el dialecto y si se va a firmar. Después viene la sesión, donde el cliente se autentica con usuario y contraseña. Recién ahí se conecta a la carpeta compartida.

La firma usa una clave que sale de esa autenticación: cada mensaje lleva un sello calculado con ella. Por eso firma e invitado no se llevan bien. Una sesión de invitado no tiene credencial, no hay clave y no se puede firmar. Si el cliente exige firma, el invitado queda afuera por las dos puntas.

Cuando el otro equipo no soporta firma, la conexión se corta en la negociación. Para el usuario es \"no se ve la carpeta\", igual que un cable suelto, y por eso la versión se anota antes de buscar fallas de red.

La salida que recomienda Microsoft no es bajar la seguridad del cliente: es actualizar o reemplazar el equipo viejo, o al menos darle un usuario con contraseña.
""",
  [{"file": "1-t1.svg", "after": "Si el cliente exige firma, el invitado queda afuera",
    "alt": "Animación en cuatro tiempos entre un Windows 11 24H2 y un NAS o grabador. 1: el cliente negocia SMB y exige firmar cada mensaje. 2: un NAS viejo responde que no firma y la conexión se corta. 3: un intento como invitado, sin usuario, tampoco entra porque Pro 24H2 tiene el invitado deshabilitado. 4: con firmware al día y un usuario propio, el NAS firma, acepta el usuario y la carpeta abre con mensajes firmados.",
    "caption": "Firma e invitado, mensaje por mensaje: por qué el NAS viejo deja de abrir."}],
  S("Ficha del equipo: edición, versión, build y SMB",
    "Lee edición, versión, build y parche del registro, y los dos valores del cliente SMB que cambiaron en 24H2 y Server 2025. No cambia nada.",
    [("NAS_IP", "192.168.88.30", "IP del NAS o grabador que vas a probar"),
     ("CARPETA", "video", "Nombre de la carpeta compartida")],
    r"""
# IES Training - Windows - Ficha del equipo: edicion, version, build y SMB
# Solo lee: no cambia nada. Sirve tambien por escritorio remoto.
& {
  $nasIp   = '{{NAS_IP}}'
  $carpeta = '{{CARPETA}}'

  $v = Get-ItemProperty 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion' |
    Select-Object EditionID, DisplayVersion, CurrentBuild, UBR
  $smb = Get-SmbClientConfiguration |
    Select-Object RequireSecuritySignature, EnableInsecureGuestLogons

  Write-Host '--- Ficha del equipo (va a la planilla de obra) ---'
  Write-Host ('Equipo:        ' + $env:COMPUTERNAME)
  Write-Host ('Edicion:       ' + $v.EditionID)
  Write-Host ('Version:       ' + $v.DisplayVersion)
  Write-Host ('Build:         ' + $v.CurrentBuild + '.' + $v.UBR)
  Write-Host ('Firma SMB:     ' + $smb.RequireSecuritySignature)
  Write-Host ('Invitado SMB:  ' + $smb.EnableInsecureGuestLogons)

  # Lectura rapida de lo que cambio desde 24H2 y Server 2025
  if ($smb.RequireSecuritySignature) {
    Write-Host 'Firma obligatoria: un NAS o grabador que no firma SMB no va a abrir.'
  }
  if (-not $smb.EnableInsecureGuestLogons) {
    Write-Host 'Sin invitado: la carpeta se abre con usuario y contrasena del propio equipo.'
  }
  # A proposito no se cambia ninguno de los dos valores.
  Write-Host ('Proba abrir \\' + $nasIp + '\' + $carpeta + ' desde el Explorador con un usuario del NAS.')
  Write-Host 'Listo: ficha impresa. Verifica con winver que version y build coincidan.'
}
""",
    ["No hace falta PowerShell como administrador: solo lee.",
     "El script no baja la firma ni habilita invitados: si el NAS no abre con usuario propio, el camino es su firmware o reemplazarlo.",
     "Copiá la salida a la planilla de obra antes de tocar la red."]))

# =====================================================================================  2
L("2",
  {"file": "2.svg", "alt": "Cuatro tarjetas en orden, unidas por flechas. 1: ¿mi placa está bien?, ipconfig /all, IP, máscara, puerta de enlace y DNS; si esto está mal, lo demás no importa. 2: ¿llego al gateway?, ping 192.168.88.1, el primer salto; sin gateway nada sale de la subred. 3: ¿el equipo está vivo?, arp -a, su MAC en la tabla ARP; hay MAC aunque el ping falle. 4: ¿dónde se pierde?, pathping -n, pérdida y demora por salto, para destinos en otra red. Abajo, en ámbar: un ping que falla no prueba que el equipo esté apagado, porque muchos equipos y firewalls bloquean ICMP; antes de mandar a alguien, mirá ARP en su subred.",
   "caption": "De tu placa hacia afuera, y ARP antes de dar por caído un equipo."},
  [{"file": "2-paso2.svg", "step": 2, "after": "Gateway y un equipo de la misma subred",
    "alt": "Una notebook 192.168.88.10 en la subred 192.168.88.0/24. El ping al gateway 192.168.88.1 responde, en verde; el ping a la cámara 192.168.88.20 no vuelve, en rojo, porque la cámara bloquea ICMP. Debajo, la salida de arp -a con dos entradas dinámicas: 192.168.88.1 y 192.168.88.20 con MAC de ejemplo 00-11-22-33-44-20, resaltada. Nota en verde: la cámara contestó la pregunta de ARP, está viva; lo que no contesta es el ping.",
    "caption": "Ping fallido y MAC en la tabla: la cámara está viva."},
   {"file": "2-paso3.svg", "step": 3, "after": "Un destino en otra red, rápido",
    "alt": "El comando pathping -n -q 10 -h 5 203.0.113.10 y una tabla de ejemplo con cuatro saltos: 1, 192.168.88.1, 0 de 10 perdidos, tu gateway; 2, 198.51.100.1, 0 de 10, proveedor; 3, 203.0.113.1, 4 de 10, 40 por ciento, resaltado como el salto donde empieza; 4, 203.0.113.10, 40 por ciento, sigue hasta el destino. Notas: la pérdida que aparece en un salto y sigue en todos los siguientes es la que importa, el problema está entre el salto 2 y el 3; -n no resuelve nombres, -q 10 baja de 100 a 10 consultas y -h 5 corta a 5 saltos.",
    "caption": "La pérdida que empieza en un salto y llega al destino marca el tramo con problemas."}],
  [C("Diagnóstico por capas",
     "Cuando \"no anda la red\" hay demasiadas causas posibles. Ir por capas, de tu propia placa hacia afuera, descarta lo básico primero y evita buscar en el router lo que era una máscara mal puesta en tu notebook.",
     "Primero ipconfig /all: IP, máscara, puerta de enlace y DNS de la placa activa. Después ping al gateway, después ARP en la subred y recién al final la ruta con pathping o Test-NetConnection -TraceRoute. Si una capa falla, no tiene sentido seguir a la siguiente.",
     "En un depósito de Colonia, el técnico tenía la notebook con IP fija de otra obra. ipconfig /all lo mostró en diez segundos, antes de llamar al proveedor de internet."),
   C("ARP y la tabla ARP",
     "Dentro de una subred, los equipos se hablan por MAC, no por IP. ARP es la pregunta \"¿quién tiene esta IP?\" que averigua la MAC antes de mandar cualquier paquete.",
     "La respuesta queda guardada en la tabla ARP del equipo, que se ve con arp -a. Si la MAC de un equipo aparece como dinámica, ese equipo respondió hace poco, aunque tenga el ping bloqueado. Solo sirve en tu misma subred: un equipo de otra red nunca aparece ahí.",
     "La cámara del portón no responde ping y el cliente quiere que vayas. arp -a muestra su MAC: la cámara está viva y el problema es otro, por ejemplo el puerto del servicio."),
   C("pathping",
     "tracert muestra el camino, pero no dice dónde se pierden paquetes cuando la falla es intermitente. pathping combina ping y tracert: primero traza la ruta y después mide pérdida y demora en cada salto.",
     "Por defecto manda 100 consultas por salto y resuelve nombres, y tarda. Con -n no resuelve nombres, -q 10 baja a 10 consultas y -h 5 corta a 5 saltos. Se lee buscando el salto donde la pérdida empieza y sigue hasta el destino.",
     "Un NVR en una sucursal del interior pierde video a ratos. pathping -n -q 10 desde la central muestra 0 por ciento hasta el router de la oficina y 30 por ciento desde el primer salto del proveedor: llamás al proveedor con ese dato.")],
  """
### Un poco de historia

Las herramientas de este diagnóstico son de los primeros años de internet. ICMP, el protocolo de mensajes de control de IP, se definió en el RFC 792 de 1981, y ARP en el RFC 826 de 1982. Mike Muuss escribió ping en 1983 para revisar una red que fallaba, y Van Jacobson creó traceroute a fines de los ochenta aprovechando un detalle de IP: cada router descuenta uno al TTL del paquete y avisa cuando llega a cero.

Windows trajo esas ideas como ping y tracert. pathping, que también viene en Windows, junta las dos cosas: traza la ruta y después le pega a cada salto muchas veces para medir pérdida. Más tarde PowerShell sumó Test-NetConnection, que hace la traza con -TraceRoute pero sin la estadística por salto.

### Cómo funciona

Antes de mandar un paquete a una IP de su misma subred, tu equipo necesita la MAC del destino. Para eso grita a todos una pregunta ARP: ¿quién tiene 192.168.88.20? El dueño de esa IP contesta con su MAC y tu equipo la guarda en la tabla ARP por un rato. Recién después sale el paquete.

El ping es otra cosa: un ICMP echo que el destino puede contestar o no. Muchos equipos y firewalls lo descartan, y el Firewall de Windows bloquea lo entrante salvo que haya regla. Por eso un ping fallido con la MAC en la tabla quiere decir \"está vivo, pero no contesta ping\".

Para otra red, ARP solo te da la MAC del gateway; desde ahí, el paquete salta de router en router. tracert y pathping mandan paquetes con TTL 1, 2, 3 y así: cada router que lo descarta avisa por ICMP y queda identificado. pathping, además, repite las consultas en cada salto para medir qué porcentaje se pierde.

Un router intermedio puede contestar poco a ICMP y mostrar pérdida sin que haya problema. La pérdida que importa es la que aparece en un salto y sigue en todos los siguientes hasta el destino.
""",
  [{"file": "2-t1.svg", "after": "Recién después sale el paquete.",
    "alt": "Animación en cuatro tiempos con una notebook, un gateway y una cámara en la misma subred 192.168.88.0/24. 1: la notebook manda una pregunta ARP a todos: quién tiene 192.168.88.20. 2: la cámara contesta con su MAC 00-11-22-33-44-20 y aparece en la tabla de arp -a. 3: sale el ping, que es ICMP, y el firewall de la cámara lo descarta. 4: queda el ping fallido y la MAC resaltada: la cámara está viva.",
    "caption": "ARP llega antes que el ping: por eso la MAC aparece aunque el ICMP esté bloqueado."}],
  S("Diagnóstico capa por capa",
    "Corre en orden ipconfig, ping al gateway y al equipo, la tabla ARP del equipo y la ruta hacia un destino de otra red. No cambia nada.",
    [("GATEWAY", "192.168.88.1", "Puerta de enlace de tu subred"),
     ("EQUIPO", "192.168.88.20", "Equipo de la misma subred que \"no responde\""),
     ("DESTINO", "203.0.113.10", "Destino en otra red para ver la ruta")],
    r"""
# IES Training - Windows - Diagnostico capa por capa
# Solo lee: no cambia nada. Pegalo en PowerShell.
& {
  $gateway = '{{GATEWAY}}'
  $equipo  = '{{EQUIPO}}'
  $destino = '{{DESTINO}}'

  Write-Host '--- 1. Tu placa: IP, mascara, puerta de enlace y DNS ---'
  ipconfig /all

  Write-Host '--- 2. Gateway y equipo de la misma subred ---'
  ping -n 2 $gateway
  ping -n 2 $equipo

  # Si figura la MAC, el equipo respondio a ARP aunque el ping falle
  Write-Host '--- 3. Tabla ARP del equipo ---'
  arp -a $equipo

  # pathping rapido: sin nombres, 10 consultas y 5 saltos
  Write-Host '--- 4. Ruta hacia otra red ---'
  pathping -n -q 10 -h 5 $destino
  Test-NetConnection $destino -TraceRoute

  Write-Host 'Listo: placa, gateway, ARP y ruta revisados. Sin MAC en ARP, mira cable, VLAN o energia del equipo.'
}
""",
    ["pathping tarda un poco aunque esté acelerado: dejalo terminar.",
     "arp -a con una IP filtra la tabla a ese equipo; si no figura, no respondió a ARP o está en otra subred.",
     "Un ping fallido con MAC presente es un equipo vivo con ICMP bloqueado: seguí por la lección de puertos."]))

# =====================================================================================  3
L("3",
  {"file": "3.svg", "alt": "Tres franjas, una por pregunta. 1: ¿hay alguien?, con ping y arp -a, resultado MAC en la tabla: la red llega al equipo. 2: ¿el servicio atiende?, con Test-NetConnection 192.168.88.20 -Port 554, resultado TcpTestSucceeded True: el puerto exacto responde. 3: ¿qué nombre ve la app?, con Resolve-DnsName vms-lab, resultado 192.168.88.50, igual que una aplicación de Windows. Abajo a la izquierda, Get-NetTCPConnection -State Listen: 0.0.0.0 escucha en todas las placas; 192.168.88.10, solo en esa placa. A la derecha, la regla: no digas no hay red hasta probar el puerto exacto del servicio.",
   "caption": "Red, servicio y nombre se prueban por separado."},
  [{"file": "3-paso2.svg", "step": 2, "after": "Qué escucha en tu equipo y quién es",
    "alt": "Consola con Get-NetTCPConnection -State Listen ordenado por puerto, con LocalAddress, LocalPort y OwningProcess. Dos filas de ejemplo: 0.0.0.0 puerto 135 proceso 1104, resaltada, y 192.168.88.10 puerto 139 proceso 4. Una flecha lleva el número de proceso a Get-Process -Id 1104, que devuelve svchost. Notas: 0.0.0.0 es todas las placas y una IP concreta es solo esa placa; netstat -ano | findstr LISTENING da lo mismo a la vieja usanza.",
    "caption": "Del puerto al número de proceso, y del número al programa."},
   {"file": "3-paso5.svg", "step": 5, "after": "al archivo hosts (como administrador",
    "alt": "La línea 192.168.88.50 vms-lab agregada al archivo hosts en C:\\Windows\\System32\\drivers\\etc. En verde, Resolve-DnsName vms-lab usa el resolvedor de Windows, archivo hosts, caché y DNS, y encuentra 192.168.88.50 como lo haría el VMS. En rojo, nslookup vms-lab pregunta solo al servidor DNS, no lee hosts ni la caché, y además agrega los sufijos de búsqueda a un nombre sin punto final. Nota: al terminar, borrar la línea; empezar con Resolve-DnsName y usar nslookup para comparar.",
    "caption": "Una línea en hosts: Resolve-DnsName la ve, nslookup no."}],
  [C("Prueba de puerto con Test-NetConnection",
     "Que un equipo responda ping no dice que el servicio funcione: una cámara puede estar viva con el RTSP caído o con el puerto cerrado por firewall. Hace falta probar el puerto exacto, sin instalar nada.",
     "Test-NetConnection IP -Port 554 intenta abrir una conexión TCP y devuelve TcpTestSucceeded True o False. -InformationLevel Quiet deja solo el True o False, útil en scripts, y -CommonTCPPort acepta nombres como RDP, HTTP, SMB o WINRM.",
     "Al dar de alta cámaras en un VMS para un edificio de Pocitos, una no agrega. Test-NetConnection al 554 da False y al 80 da True: el problema es el RTSP de esa cámara, no la red."),
   C("Puertos en escucha",
     "Cuando un servicio \"no responde\", conviene saber si de verdad está escuchando, en qué puerto y en qué placa. Si escucha solo en una IP, los pedidos por otra placa no llegan aunque todo lo demás esté bien.",
     "Get-NetTCPConnection -State Listen lista los puertos en escucha con LocalAddress y OwningProcess; Get-Process -Id con ese número da el nombre del programa. 0.0.0.0 quiere decir todas las placas. netstat -ano | findstr LISTENING muestra lo mismo en la consola clásica.",
     "El servidor del VMS tiene dos placas, cámaras y gestión. El servicio web figura en 192.168.88.10:8443 y no en 0.0.0.0: desde la red de gestión nunca va a contestar."),
   C("Resolve-DnsName contra nslookup",
     "Las aplicaciones de Windows resuelven nombres con el resolvedor del sistema, que mira el archivo hosts y la caché antes que el DNS. nslookup tiene su propio cliente DNS y le pregunta solo al servidor, así que puede dar un resultado distinto al que ve el programa.",
     "Resolve-DnsName reproduce lo que ve una aplicación; con -DnsOnly y -Server consulta un servidor concreto. nslookup sirve para comparar y aislar fallas del resolvedor. Con nslookup, el punto final (nombre.) evita que pruebe los sufijos de búsqueda primero.",
     "El VMS de un cliente apunta a vms-lab y funciona, pero nslookup dice que el nombre no existe. Resolve-DnsName lo encuentra: está en el archivo hosts de ese servidor, y eso se anota en el informe.")],
  """
### Un poco de historia

Durante años, el técnico probaba un puerto con telnet IP puerto y miraba si la pantalla quedaba en negro. Windows dejó de traer telnet instalado y, con Windows 8.1 y Windows Server 2012 R2, PowerShell sumó Test-NetConnection, que hace esa prueba y devuelve un sí o un no. netstat viene de mucho antes, de los sistemas Unix de los ochenta, y Get-NetTCPConnection es su versión en PowerShell.

Los nombres tienen una historia parecida. Antes del DNS, definido en los RFC 1034 y 1035 de 1987, cada equipo de ARPANET tenía un archivo con todos los nombres y sus direcciones. El archivo hosts de Windows es heredero directo de esa lista, y todavía le gana al DNS.

### Cómo funciona

Una conexión TCP arranca con tres mensajes. Tu equipo manda un SYN al puerto; si hay un programa escuchando y nada lo bloquea, vuelve un SYN/ACK y la conexión queda abierta. Test-NetConnection -Port hace exactamente eso y, si recibe el SYN/ACK, informa True.

Hay dos formas de False. Si nadie escucha en ese puerto, el equipo contesta con un RST y el resultado llega al instante. Si un firewall descarta el SYN, no vuelve nada: Test-NetConnection espera y termina por tiempo. Un False rápido apunta al servicio; uno lento, a un firewall.

Para los nombres, Windows tiene un resolvedor propio. Primero mira el archivo hosts, que se carga en la caché, y la caché de respuestas anteriores; después pregunta a los servidores DNS de la placa, agregando los sufijos de búsqueda si el nombre es corto. Si el DNS no lo encuentra, todavía prueba LLMNR y mDNS en la red local.

nslookup no usa ese camino. Le pregunta directo al servidor DNS, sin hosts ni caché, y a un nombre sin punto final le agrega cada sufijo antes de probarlo tal cual. Por eso el resultado puede diferir del que ve el VMS, y por eso Resolve-DnsName va primero.
""",
  [{"file": "3-t1.svg", "after": "Un False rápido apunta al servicio",
    "alt": "Animación en cuatro tiempos entre tu equipo y una cámara 192.168.88.20. 1: tu equipo manda un SYN al puerto 554. 2: el servicio escucha y contesta SYN/ACK, y Test-NetConnection muestra TcpTestSucceeded True. 3: al puerto 8443, donde nadie escucha, vuelve un RST y el resultado es False al instante. 4: un firewall descarta el SYN, no vuelve nada y el resultado es False por tiempo.",
    "caption": "True, False al instante o False por tiempo: cada uno apunta a otra causa."},
   {"file": "3-t2.webp", "after": "pregunta directo al servidor DNS, sin hosts ni caché",
    "alt": "Diagrama de dos caminos. Resolve-DnsName, igual que el VMS, entra al resolvedor de Windows, que recorre en orden archivo hosts, caché DNS, servidor DNS 192.168.88.1 y, si el DNS no lo encuentra, LLMNR y mDNS. nslookup, consulta directa, va con una línea punteada solo al servidor DNS. Recuadro: nslookup vms-lab prueba vms-lab.sufijo1, vms-lab.sufijo2 y así antes del nombre tal cual; con punto final pregunta solo ese.",
    "caption": "El resolvedor de Windows recorre varias fuentes; nslookup, solo el DNS."}],
  S("Probar puertos y nombres de un equipo",
    "Prueba una lista de puertos de un equipo, muestra qué escucha en este servidor con el nombre del programa y compara cómo resuelven un nombre Resolve-DnsName y nslookup. No cambia nada.",
    [("EQUIPO", "192.168.88.20", "IP del equipo a probar (cámara, NVR, servidor)"),
     ("PUERTOS", "554, 80, 8443", "Puertos separados por coma"),
     ("NOMBRE", "vms-lab", "Nombre que usa la aplicación"),
     ("DNS", "1.1.1.1", "Servidor DNS para comparar")],
    r"""
# IES Training - Windows - Probar puertos y nombres
# Solo lee: no cambia nada. PowerShell como administrador.
& {
  $equipo  = '{{EQUIPO}}'
  $puertos = @({{PUERTOS}})
  $nombre  = '{{NOMBRE}}'
  $dns     = '{{DNS}}'

  Write-Host ('--- Puertos de ' + $equipo + ' ---')
  foreach ($p in $puertos) {
    $ok = Test-NetConnection $equipo -Port $p -InformationLevel Quiet
    Write-Host ('Puerto ' + $p + ' -> ' + $ok)
  }

  Write-Host '--- Lo que escucha este equipo (0.0.0.0 = todas las placas) ---'
  Get-NetTCPConnection -State Listen |
    Sort-Object LocalPort |
    Select-Object LocalAddress, LocalPort, OwningProcess,
      @{n='Programa'; e={(Get-Process -Id $_.OwningProcess -ErrorAction SilentlyContinue).ProcessName}}

  Write-Host ('--- ' + $nombre + ' como lo ve una aplicacion (hosts, cache y DNS) ---')
  Resolve-DnsName $nombre -ErrorAction SilentlyContinue
  Write-Host ('--- ' + $nombre + ' solo en el servidor DNS ' + $dns + ' ---')
  Resolve-DnsName $nombre -DnsOnly -Server $dns -ErrorAction SilentlyContinue
  nslookup ($nombre + '.') $dns

  Write-Host 'Listo: True es servicio atendiendo. Si la aplicacion resuelve el nombre y el DNS no, mira el archivo hosts.'
}
""",
    ["Un False que tarda suele ser un firewall; un False inmediato, un puerto sin servicio.",
     "nslookup recibe el nombre con punto final para que no pruebe los sufijos de búsqueda.",
     "El script no toca el archivo hosts: agregar o borrar líneas queda a mano, como en el laboratorio."]))

# =====================================================================================  4
L("4",
  {"file": "4.svg", "alt": "Cinco tarjetas en fila. 1: ver la placa con Get-NetAdapter, nombre e índice. 2: limpiar con Remove-NetIPAddress y Remove-NetRoute 0.0.0.0/0. 3: asignar con New-NetIPAddress, -PrefixLength 24 y -DefaultGateway. 4: DNS aparte con Set-DnsClientServerAddress, ServerAddresses 10.10.10.1. 5, en verde: verificar con Get-NetIPAddress y Get-NetRoute 0.0.0.0/0. Debajo: -PrefixLength 24 equivale a máscara 255.255.255.0, porque New-NetIPAddress no toma la máscara en decimal; en rojo, sin limpiar quedan dos gateways y el tráfico sale por donde quiere. Nota en ámbar: hacerlo desde la consola, porque cambiar la IP por escritorio remoto desconecta.",
   "caption": "Ver, limpiar, asignar, DNS y verificar: repetible y para el informe."},
  [{"file": "4-paso2.svg", "step": 2, "after": "Limpiar y asignar (cambiá",
    "alt": "Get-NetRoute -DestinationPrefix 0.0.0.0/0 en dos situaciones. A la izquierda, en rojo, sin Remove-NetRoute: dos rutas por defecto, la vieja por 192.168.88.1 y la nueva por 10.10.10.1; el tráfico puede salir por un gateway que ya no existe. A la derecha, en verde, con Remove-NetRoute antes: una sola ruta por defecto por 10.10.10.1, la que se puso con -DefaultGateway. Nota: Remove-NetIPAddress y Remove-NetRoute, con -Confirm:$false, antes de New-NetIPAddress. IPs de ejemplo.",
    "caption": "Una sola ruta por defecto: lo que tenés que ver al verificar."},
   {"file": "4-paso5.svg", "step": 5, "after": "de prueba sin dominio",
    "alt": "Un Windows Server 2025 de prueba, servidor DHCP con IP fija 10.10.10.20, conectado a una cámara de acceso con MAC 00-11-22-33-44-55. El ámbito Lab CCTV reparte de 10.10.10.100 a 10.10.10.200 con máscara 255.255.255.0, con opciones router 10.10.10.1 y DNS 10.10.10.20, y una reserva de 10.10.10.150 para la MAC de la cámara, que siempre recibe la misma IP. Notas: con dominio falta Add-DhcpServerInDC porque un DHCP no autorizado en Active Directory no entrega direcciones; conectado a la red del cliente, un DHCP de laboratorio puede repartir direcciones, así que se prueba aislado.",
    "caption": "Ámbito, opciones y reserva por MAC, en una red aislada."}],
  [C("IP fija por PowerShell",
     "En un servidor de VMS la IP no puede cambiar: cámaras, clientes y reglas apuntan a ella. Ponerla por consola deja un procedimiento que se repite igual en cada obra, se pega en el informe y funciona en un Server Core sin ventanas.",
     "Cuatro pasos: Get-NetAdapter para el nombre de la placa, Remove-NetIPAddress y Remove-NetRoute para limpiar lo viejo, New-NetIPAddress con -IPAddress, -PrefixLength y -DefaultGateway, y Set-DnsClientServerAddress para el DNS. Después se verifica con Get-NetIPAddress, Get-NetRoute y Get-DnsClientServerAddress.",
     "Dejás el servidor de una portería IP en 10.10.10.20/24 con gateway 10.10.10.1, y el bloque de comandos va tal cual al informe de obra. Si el año que viene hay que rehacer el servidor, el informe ya tiene la receta."),
   C("PrefixLength y ruta por defecto",
     "New-NetIPAddress no recibe la máscara en decimal sino el largo del prefijo, la notación /24 de CIDR. Y el gateway no es un dato de la IP sino una ruta aparte, la 0.0.0.0/0, que puede quedar duplicada.",
     "-PrefixLength 24 equivale a 255.255.255.0. -DefaultGateway crea la ruta 0.0.0.0/0; si la vieja no se borró antes con Remove-NetRoute, quedan dos. Al verificar, Get-NetRoute -DestinationPrefix '0.0.0.0/0' tiene que mostrar una sola.",
     "Un servidor que antes estaba en la red de la oficina, 192.168.88.0/24, pasa a la red de CCTV. Sin limpiar la ruta, a veces sale por el gateway viejo y el acceso remoto anda un día sí y otro no."),
   C("Reserva DHCP y autorización",
     "Cámaras y controladoras tienen que tener siempre la misma IP, pero configurarlas una por una a mano es lento y se presta a errores. La reserva por MAC le da a cada equipo su IP desde el DHCP, con el inventario en un solo lugar.",
     "El rol DHCP de Windows Server pide IP fija. Se crea el ámbito con Add-DhcpServerv4Scope, las opciones con Set-DhcpServerv4OptionValue (router y DNS) y cada reserva con Add-DhcpServerv4Reservation y la MAC. Si hay dominio, el servidor se autoriza con Add-DhcpServerInDC o no entrega direcciones.",
     "En un depósito con 40 cámaras, cada una tiene su reserva con descripción: \"Cámara acceso\", \"Muelle 3\". Cambiar una cámara rota es cambiar una MAC en la reserva.")],
  """
### Un poco de historia

Antes de DHCP, cada equipo de una red se configuraba a mano o con BOOTP, un protocolo de 1985 pensado para estaciones sin disco. DHCP, definido en su forma actual en el RFC 2131 de 1997, sumó lo que faltaba: préstamos con vencimiento, reservas y opciones como el gateway y el DNS. Windows NT ya traía su servidor DHCP.

Con Active Directory, en Windows 2000, apareció la autorización: un DHCP de Windows en un dominio tiene que figurar como autorizado o no reparte. La idea era frenar al servidor \"pirata\" que alguien enchufa y deja a media empresa sin red.

La configuración por consola vivió años en netsh. Con Windows 8 y Server 2012, PowerShell trajo cmdlets propios como New-NetIPAddress, que piden el prefijo en la notación CIDR de 1993.

### Cómo funciona

Para Windows, una IP fija no es un solo dato. La dirección con su prefijo es un objeto; la ruta por defecto, 0.0.0.0/0 hacia el gateway, es otro; y los servidores DNS de la placa, un tercero. Por eso se limpian por separado y se verifican por separado.

Cuando un equipo pide IP por DHCP pasan cuatro mensajes, que se recuerdan como DORA. Discover: el equipo, que todavía no tiene IP, manda un broadcast pidiendo dirección. Offer: el servidor ofrece una. Request: el equipo la pide formalmente. Ack: el servidor confirma y entrega las opciones, como el router (opción 3) y el DNS (opción 6).

Con una reserva, en el Offer el servidor busca la MAC del pedido en su lista y, si está, ofrece siempre la misma IP. Si hay dos servidores DHCP en la misma red, los dos contestan el Discover y el equipo se queda con la primera oferta: así un DHCP de laboratorio enchufado a la red del cliente reparte direcciones equivocadas.

En un dominio, el DHCP de Windows consulta Active Directory al arrancar. Si no figura como autorizado, no responde y el rol queda instalado pero mudo.
""",
  [{"file": "4-t1.svg", "after": "y el DNS (opción 6).",
    "alt": "Animación en cuatro tiempos entre una cámara con MAC 00-11-22-33-44-55 y un servidor DHCP de Windows con IP fija 10.10.10.20. 1: Discover, la cámara manda un broadcast pidiendo IP. 2: Offer, el servidor encuentra la MAC en la reserva del ámbito Lab CCTV y ofrece 10.10.10.150. 3: Request, la cámara pide esa IP. 4: Ack, el servidor confirma con router 10.10.10.1 y DNS 10.10.10.20 y la cámara queda configurada.",
    "caption": "Discover, Offer, Request y Ack, con la reserva resolviendo la IP."}],
  S("IP fija por consola, verificada",
    "Deja una placa con IP fija, gateway y DNS, limpiando antes la IP y la ruta por defecto viejas, y muestra la verificación. Si la placa ya tiene esa IP, no la toca.",
    [("PLACA", "Ethernet", "Nombre de la placa, como lo muestra Get-NetAdapter"),
     ("IP", "10.10.10.20", "IP fija del servidor"),
     ("PREFIJO", "24", "Largo del prefijo: 24 es 255.255.255.0"),
     ("GATEWAY", "10.10.10.1", "Puerta de enlace"),
     ("DNS", "10.10.10.1", "Servidor DNS")],
    r"""
# IES Training - Windows - IP fija por consola, verificada
# Pegalo desde la consola del equipo, no por escritorio remoto: cambiar la IP desconecta.
& {
  $if      = '{{PLACA}}'
  $ip      = '{{IP}}'
  $prefijo = {{PREFIJO}}
  $gw      = '{{GATEWAY}}'
  $dns     = '{{DNS}}'

  if ($env:SESSIONNAME -like 'RDP*') { Write-Host 'Estas por escritorio remoto: hacelo desde la consola.'; return }
  if (-not (Get-NetAdapter -Name $if -ErrorAction SilentlyContinue)) {
    Write-Host ('No existe la placa ' + $if + '. Estas son las que hay:')
    Get-NetAdapter | Select-Object Name, InterfaceIndex, Status, MacAddress
    return
  }
  $actual = Get-NetIPAddress -InterfaceAlias $if -AddressFamily IPv4 -ErrorAction SilentlyContinue
  if ($actual.IPAddress -contains $ip) {
    Write-Host ('La placa ya tiene ' + $ip + ': no se toca la IP.')
  } else {
    # Limpiar IP y gateway viejos para que no queden dos rutas por defecto
    Remove-NetIPAddress -InterfaceAlias $if -AddressFamily IPv4 -Confirm:$false -ErrorAction SilentlyContinue
    Remove-NetRoute -InterfaceAlias $if -DestinationPrefix '0.0.0.0/0' -Confirm:$false -ErrorAction SilentlyContinue
    New-NetIPAddress -InterfaceAlias $if -IPAddress $ip -PrefixLength $prefijo -DefaultGateway $gw
  }
  Set-DnsClientServerAddress -InterfaceAlias $if -ServerAddresses $dns

  Write-Host '--- Verificacion ---'
  Get-NetIPAddress -InterfaceAlias $if -AddressFamily IPv4 | Select-Object IPAddress, PrefixLength
  Get-NetRoute -DestinationPrefix '0.0.0.0/0' | Select-Object InterfaceAlias, NextHop
  Get-DnsClientServerAddress -InterfaceAlias $if -AddressFamily IPv4 | Select-Object ServerAddresses
  # Para volver a DHCP: Set-NetIPInterface -InterfaceAlias $if -Dhcp Enabled
  # y Set-DnsClientServerAddress -InterfaceAlias $if -ResetServerAddresses
  Write-Host ('Listo: ' + $if + ' con ' + $ip + '/' + $prefijo + ', gateway ' + $gw + ' y DNS ' + $dns + '. Tiene que haber una sola ruta 0.0.0.0/0.')
}
""",
    ["Corre desde la consola de la VM o del servidor: si detecta una sesión de escritorio remoto, no hace nada.",
     "Si la placa ya tiene esa IP, solo ajusta el DNS: se puede pegar dos veces.",
     "El DHCP de Windows Server no está en el script: en una red de cliente, un ámbito de prueba reparte direcciones."]))

# =====================================================================================  5
L("5",
  {"file": "5.svg", "alt": "Arriba, los tres perfiles del Firewall de Windows: Dominio, unida a Active Directory; Privado, una red tuya de confianza; Público, cualquier red ajena; en los tres, lo entrante queda bloqueado salvo regla. Debajo, la regla LAB VMS web 8443 con -Profile Private,Domain en dos casos: en verde, la placa en Privado, su perfil está activo, la regla actúa y el 8443 entra desde la subred local; en rojo, la placa en Público, la regla existe pero no actúa y el 8443 queda bloqueado. Nota: mirar el perfil con Get-NetConnectionProfile antes de crear nada, abrir por puerto o programa con origen limitado y exportar antes de tocar.",
   "caption": "La misma regla funciona o no según el perfil de la placa."},
  [{"file": "5-paso4.svg", "step": 4, "after": "Regla por puerto, solo desde",
    "alt": "La regla New-NetFirewallRule LAB VMS web 8443 desarmada en cuatro partes, cada una con su significado. -Direction Inbound -Action Allow: qué hace, permite lo que entra. -Protocol TCP -LocalPort 8443: qué abre, un puerto concreto. -RemoteAddress LocalSubnet, en verde: desde dónde, solo la subred local del equipo. -Profile Private,Domain, en ámbar: cuándo, solo con esos perfiles activos. Nota: para una regla por programa va -Program con la ruta completa del ejecutable; nunca todo a todos.",
    "caption": "Qué entra, desde dónde y con qué perfil."},
   {"file": "5-paso5.svg", "step": 5, "after": "Ver qué abre de verdad",
    "alt": "Tres consolas. Get-NetFirewallRule LAB VMS web 8443 muestra nombre, Enabled True y Profile Private, Domain, sin puerto ni dirección. Encadenado a Get-NetFirewallPortFilter muestra Protocol TCP y LocalPort 8443. Encadenado a Get-NetFirewallAddressFilter muestra RemoteAddress LocalSubnet y LocalAddress Any. Nota: así se audita un servidor con reglas; al terminar, Remove-NetFirewallRule con el mismo nombre.",
    "caption": "Puerto y origen se ven en los filtros, no en la regla."}],
  [C("Perfil de red",
     "Una notebook no puede confiar igual en la red de la oficina que en el wifi de un bar. Windows clasifica cada conexión en Dominio, Privado o Público, y el firewall aplica reglas distintas según esa categoría.",
     "Get-NetConnectionProfile muestra la categoría de cada placa. Si una red tuya quedó como Pública, se pasa a Privada con Set-NetConnectionProfile. Dominio la pone Windows sola cuando la placa ve un controlador de dominio; no se elige a mano.",
     "En un servidor con dos placas, la de cámaras quedó como Pública porque esa red no tiene gateway. Las reglas del VMS estaban creadas para Privado y nada entraba, con el firewall \"bien configurado\"."),
   C("Regla con origen limitado",
     "Abrir un puerto \"a todos\" deja el servicio expuesto a cualquier equipo que llegue a esa placa, incluida una notebook infectada en la misma red. Limitar el origen achica quién puede siquiera intentarlo.",
     "New-NetFirewallRule con -Protocol y -LocalPort, o con -Program, y siempre con -RemoteAddress: LocalSubnet, una subred o IP concretas. -Profile define en qué perfiles actúa; si no se pone, vale para todos. Para ver qué abre, se encadenan Get-NetFirewallPortFilter y Get-NetFirewallAddressFilter.",
     "El cliente web del VMS en un shopping se abre en el 8443 solo para la subred de los puestos de monitoreo. Una PC de administración del mismo edificio, en otra subred, ni lo ve."),
   C("Respaldo del firewall",
     "Cuando algo deja de conectar después de tocar reglas, volver atrás regla por regla es lento y propenso a errores. Un export completo es la marcha atrás de un solo paso.",
     "netsh advfirewall export \"C:\\Lab\\firewall-antes.wfw\" guarda toda la configuración; netsh advfirewall import la restaura. netsh advfirewall reset borra todas las reglas propias: en producción, solo con el export hecho y a mano.",
     "Antes de ajustar las reglas de un servidor de control de acceso en una clínica, exportás el firewall con la fecha en el nombre. Si algo falla en la puesta en marcha, en un minuto queda como estaba.")],
  """
### Un poco de historia

El Firewall de Windows llegó encendido por defecto con Windows XP Service Pack 2, en 2004, después de que el gusano Blaster de 2003 se propagara por equipos que tenían puertos abiertos a cualquiera. Era simple: bloqueaba lo entrante y poco más.

Windows Vista y Server 2008 trajeron el Firewall de Windows con seguridad avanzada: reglas de entrada y de salida, filtros por programa, puerto y dirección, y los perfiles por tipo de red, Dominio, Privado y Público. Con Windows 8 y Server 2012, PowerShell sumó el módulo NetSecurity con cmdlets como New-NetFirewallRule.

### Cómo funciona

Cada placa de red tiene una categoría. Windows marca como Dominio la placa que llega a un controlador de dominio y se autentica; las demás quedan como Privada o Pública según lo que se eligió. En cada perfil, la acción por defecto es dejar salir todo y bloquear todo lo que entra salvo lo que tenga regla.

Una regla es un conjunto de filtros: dirección, acción, protocolo y puerto, programa, direcciones remotas y perfiles. Cuando llega una conexión, el firewall busca una regla habilitada cuyos filtros coincidan todos, incluido el perfil de la placa por la que entró. Si encuentra una de permitir, la deja pasar; si no encuentra ninguna, la bloquea. Las reglas de bloqueo explícito ganan sobre las de permitir.

Por eso la misma regla puede andar en una placa y no en otra del mismo servidor. Y por eso Get-NetFirewallRule no alcanza para saber qué abre: el puerto y el origen viven en objetos de filtro aparte, que se piden con Get-NetFirewallPortFilter y Get-NetFirewallAddressFilter.

LocalSubnet es una palabra clave que el firewall traduce a las subredes de las placas del propio equipo. Si mañana cambia la IP del servidor, la regla se adapta sola.
""",
  [{"file": "5-t1.svg", "after": "incluido el perfil de la placa por la que entró",
    "alt": "Animación en cuatro tiempos con un servidor del VMS que escucha en 8443 y tiene la regla LAB VMS web 8443 (TCP 8443 entrante, origen LocalSubnet, perfiles Private y Domain), detrás de la pared del firewall. 1: con la placa en Privado, la conexión de un puesto de monitoreo de la misma subred entra. 2: la de un equipo de otra red, 10.20.0.5, se bloquea porque el origen no está en la subred local. 3: la placa pasa a Público y la conexión del puesto se bloquea porque la regla deja de actuar. 4: con Set-NetConnectionProfile la placa vuelve a Privado y la conexión entra otra vez.",
    "caption": "Perfil, puerto y origen tienen que coincidir los tres."}],
  S("Regla de entrada con origen limitado, con respaldo antes",
    "Muestra el perfil de cada placa, exporta el firewall con fecha, crea una regla de entrada por puerto con origen y perfiles limitados si todavía no existe, y muestra lo que abre de verdad.",
    [("NOMBRE_REGLA", "LAB VMS web 8443", "Nombre visible de la regla"),
     ("PUERTO", "8443", "Puerto TCP a abrir"),
     ("ORIGEN", "LocalSubnet", "Desde dónde: LocalSubnet, una subred o IP"),
     ("PERFILES", "Private,Domain", "Perfiles en los que actúa, separados por coma"),
     ("CARPETA", "C:\\Lab", "Carpeta para el respaldo del firewall")],
    r"""
# IES Training - Windows - Regla de entrada con origen limitado
# PowerShell como administrador. Exporta el firewall antes de tocar.
& {
  $nombre   = '{{NOMBRE_REGLA}}'
  $puerto   = {{PUERTO}}
  $origen   = '{{ORIGEN}}'
  $perfiles = '{{PERFILES}}' -split '\s*,\s*'
  $carpeta  = '{{CARPETA}}'

  Write-Host '--- Perfil de cada placa y estado del firewall ---'
  Get-NetConnectionProfile | Select-Object InterfaceAlias, NetworkCategory
  Get-NetFirewallProfile | Select-Object Name, Enabled, DefaultInboundAction

  # Respaldo con fecha: se restaura con netsh advfirewall import
  New-Item -ItemType Directory $carpeta -Force
  netsh advfirewall export ($carpeta + '\firewall-' + (Get-Date -Format 'yyyyMMdd-HHmm') + '.wfw')

  if (Get-NetFirewallRule -DisplayName $nombre -ErrorAction SilentlyContinue) {
    Write-Host ('La regla ' + $nombre + ' ya existe: no se duplica.')
  } else {
    New-NetFirewallRule -DisplayName $nombre -Direction Inbound -Action Allow `
      -Protocol TCP -LocalPort $puerto -RemoteAddress $origen -Profile $perfiles
  }

  Write-Host '--- Lo que abre de verdad ---'
  Get-NetFirewallRule -DisplayName $nombre | Get-NetFirewallPortFilter | Select-Object Protocol, LocalPort
  Get-NetFirewallRule -DisplayName $nombre | Get-NetFirewallAddressFilter | Select-Object RemoteAddress
  # Si una red tuya quedo como Publica, la regla no actua en esa placa. A mano:
  # Set-NetConnectionProfile -InterfaceAlias 'Ethernet' -NetworkCategory Private
  Write-Host ('Listo: ' + $nombre + ' permite TCP ' + $puerto + ' desde ' + $origen + '. Proba desde otro equipo con Test-NetConnection IP -Port ' + $puerto)
}
""",
    ["Si la regla ya existe con ese nombre, no la modifica: borrala con Remove-NetFirewallRule si querés recrearla.",
     "El cambio de perfil de red queda comentado: pasar una placa a Privada solo si es una red tuya.",
     "Nunca netsh advfirewall reset en producción sin el export a mano."]))

# =====================================================================================  6
L("6",
  {"file": "6.svg", "alt": "Diagrama de acceso remoto. Desde internet, con escaneos al 3389, una flecha roja hacia el router del cliente aparece cruzada: el 3389 directo no existe. El técnico en la casa entra por un túnel VPN al router del cliente, que tiene VPN y ningún reenvío al 3389. Del router, una flecha verde llega a la zona de gestión 10.10.10.0/24, donde está el servidor del VMS con RDP 3389 y NLA activa, y la regla de RDP con -RemoteAddress 10.10.10.0/24, que solo acepta esa subred. Notas: el 3389 nunca abierto a internet, ni con contraseña larga ni con otro puerto; adentro, NLA autentica antes de abrir la sesión y cambiar el puerto solo baja el ruido de los escaneos.",
   "caption": "RDP llega por VPN y solo desde la subred de gestión."},
  [{"file": "6-paso4.svg", "step": 4, "after": "Desde un equipo de esa subred",
    "alt": "Un servidor con la regla de RDP limitada a 10.10.10.0/24. Desde un puesto de gestión 10.10.10.40, Test-NetConnection IP -CommonTCPPort RDP da TcpTestSucceeded True, en verde. Desde un puesto de otra red, 192.168.88.40, da False, en rojo. Nota: si se tocan estas reglas por escritorio remoto desde fuera de la subred elegida, te cortás; hacerlo por consola o desde la subred de gestión.",
    "caption": "La prueba desde dos subredes confirma que el límite funciona."},
   {"file": "6-paso5.svg", "step": 5, "after": "no exista ningún reenvío de puerto",
    "alt": "Tabla de reenvío de puertos de un router de laboratorio con dos filas de ejemplo que hay que borrar: TCP 3389 hacia 10.10.10.20:3389, y TCP 33890 hacia 10.10.10.20:3389, cada una con una cruz roja. Notas: cambiar el número externo no alcanza, el servidor queda expuesto igual; lo que sí, el acceso desde afuera entra por la VPN del router y adentro llega desde la subred de gestión.",
    "caption": "Ningún puerto externo puede terminar en el 3389."}],
  [C("RDP sin exponer",
     "El escritorio remoto da control total del servidor. Con el 3389 abierto a internet, el servidor recibe intentos de contraseña todo el día; TechTarget cuenta ataques de ransomware, como los de Baltimore y Atlanta, que empezaron por RDP.",
     "El acceso desde afuera entra por VPN o por un gateway de escritorio remoto, y adentro la regla de RDP acepta solo la subred de gestión con -RemoteAddress. En el router no tiene que existir ningún reenvío hacia el 3389, con ningún número de puerto externo.",
     "El dueño de un supermercado quiere mirar el servidor del VMS desde la casa. Le dejás la VPN del router y RDP limitado a la subred de gestión: entra igual, y el servidor no aparece en ningún escaneo."),
   C("NLA (Network Level Authentication)",
     "Sin NLA, cualquiera que llegue al 3389 hace que el servidor arme una sesión y dibuje la pantalla de inicio, gastando recursos antes de saber quién es. NLA obliga a autenticarse primero.",
     "Viene activada en todas las versiones soportadas. Se consulta con Win32_TSGeneralSetting, propiedad UserAuthenticationRequired (1 es activa), o en Configuración > Sistema > Escritorio remoto. Desactivarla es un parche temporal mientras se arregla la causa real.",
     "Un servidor de control de acceso en un edificio del Centro dice \"requiere NLA\" al conectar. En lugar de apagarla, revisás la hora y el DNS del servidor, y el error desaparece."),
   C("El error \"requiere NLA\"",
     "Cuando NLA falla, el mensaje culpa al escritorio remoto, pero casi siempre la causa está en la autenticación: el servidor no puede validar la credencial que mandás.",
     "Las causas típicas son DNS mal configurado, controlador de dominio que no responde, relación de confianza rota con el dominio u hora desfasada. Conectar por IP en vez de por nombre puede impedir Kerberos y romper NLA en dominio. Para entrar mientras tanto, cuenta de administrador local o consola de la VM.",
     "Después de un corte, un servidor en dominio arranca con la hora corrida. Nadie entra por RDP. Corregís la hora desde la consola de la VM y NLA vuelve a funcionar sin tocar ninguna configuración de RDP.")],
  """
### Un poco de historia

El escritorio remoto nació con Windows NT 4.0 Terminal Server Edition, en 1998, y desde entonces escucha en el puerto 3389. Durante años, la pantalla de inicio de sesión se dibujaba para cualquiera que llegara al puerto: la autenticación pasaba adentro de la sesión ya creada.

Windows Vista y Server 2008 trajeron NLA, Network Level Authentication, que da vuelta ese orden con un mecanismo llamado CredSSP: primero se prueba la credencial y recién después existe la sesión. En 2019, la falla conocida como BlueKeep afectó al RDP de versiones viejas de Windows, y tener NLA activa fue una de las mitigaciones recomendadas, porque obligaba al atacante a autenticarse antes de llegar al código vulnerable.

### Cómo funciona

Una conexión de escritorio remoto empieza con TCP al 3389 y un canal cifrado con TLS, para que nadie en el medio lea lo que viaja. Con NLA, por ese canal el cliente manda las credenciales antes de pedir el escritorio, y el servidor las valida contra Active Directory o contra sus cuentas locales.

Si la credencial es válida, el servidor arma la sesión y recién ahí aparece el escritorio. Si es mala, la conexión termina sin que el servidor haya creado nada. Un atacante que solo llega al puerto no consigue ni la pantalla de inicio.

En un dominio, esa validación usa Kerberos, que necesita tres cosas: que el cliente encuentre el controlador de dominio por DNS, que la cuenta del servidor tenga su relación de confianza sana y que los relojes estén cerca, con no más de unos minutos de diferencia. Kerberos además trabaja con nombres: si conectás por IP, puede caer a NTLM y, según la configuración, NLA falla.

El firewall agrega la otra capa. La regla de RDP con -RemoteAddress limitada a la subred de gestión hace que una conexión de cualquier otro origen ni siquiera llegue a la parte de NLA. Y sin reenvío en el router, desde internet el 3389 no existe.
""",
  [{"file": "6-t1.svg", "after": "Un atacante que solo llega al puerto no consigue",
    "alt": "Animación en cuatro tiempos entre un cliente RDP que entra por VPN y por nombre y el servidor del VMS con NLA activa en el 3389. 1: se establece TCP 3389 y un canal TLS. 2: con NLA, el cliente manda las credenciales por CredSSP antes de abrir sesión y el servidor las valida contra Active Directory o cuentas locales. 3: con credencial válida, recién ahí el servidor arma el escritorio remoto. 4: con credencial mala, la conexión termina sin dibujar ninguna pantalla ni gastar recursos.",
    "caption": "Primero quién sos, después el escritorio."}],
  S("Revisar NLA y limitar RDP a la subred de gestión",
    "Muestra si NLA está activa, lista las reglas de escritorio remoto y, solo si se corre desde la consola del servidor, las limita a la subred de gestión.",
    [("SUBRED_GESTION", "10.10.10.0/24", "Subred desde la que se permite RDP"),
     ("GRUPO_RDP", "Remote Desktop", "Grupo de reglas: en Windows en español puede ser Escritorio remoto")],
    r"""
# IES Training - Windows - NLA y RDP limitado a la subred de gestion
# PowerShell como administrador, desde la consola del servidor.
& {
  $gestion = '{{SUBRED_GESTION}}'
  $grupo   = '{{GRUPO_RDP}}'

  $nla = (Get-CimInstance -ClassName Win32_TSGeneralSetting -Namespace root\cimv2\terminalservices `
    -Filter "TerminalName='RDP-tcp'").UserAuthenticationRequired
  if ($nla -eq 1) { Write-Host 'NLA activa.' }
  else { Write-Host 'NLA apagada: activala en Configuracion > Sistema > Escritorio remoto.' }

  $reglas = Get-NetFirewallRule -DisplayGroup $grupo -ErrorAction SilentlyContinue
  if (-not $reglas) { Write-Host ('No hay reglas en el grupo ' + $grupo + '. Proba con Escritorio remoto.'); return }
  Write-Host '--- Reglas de escritorio remoto ---'
  $reglas | Select-Object DisplayName, Enabled, Profile

  if ($env:SESSIONNAME -eq 'Console') {
    $reglas | Set-NetFirewallRule -RemoteAddress $gestion
    Write-Host ('Reglas de RDP limitadas a ' + $gestion + '.')
  } else {
    # Por escritorio remoto, desde fuera de esa subred, te cortarias: no se aplica.
    Write-Host 'Estas por escritorio remoto: no se limita nada. Corre el script desde la consola.'
  }
  Write-Host ('Listo. Verifica desde un equipo de ' + $gestion + ' con Test-NetConnection IP -CommonTCPPort RDP y revisa que el router no reenvie nada al 3389.')
}
""",
    ["Solo aplica el límite si la sesión es la consola del servidor: por escritorio remoto no toca nada.",
     "El reenvío de puertos del router no se puede revisar desde Windows: queda como paso a mano.",
     "Volver a correrlo deja el mismo límite: se puede pegar dos veces."]))

# =====================================================================================  7
L("7",
  {"file": "7.svg", "alt": "Tres bloques. Tipo de inicio: Automático (start= auto), Automático retrasado en verde (start= delayed-auto), Manual (start= demand) y Deshabilitado (start= disabled); retrasado es para lo que depende de la red o de la base de datos. Recuperación ante fallas: primera falla, segunda falla y siguientes, todas con reiniciar a los 3 minutos, y el contador a cero después de 24 horas sin fallas; valores de partida de una plantilla, con failureflag 1 también actúa si el servicio se detiene con error. Abajo, lo que no es servicio va como tarea programada al inicio: AtStartup, NT AUTHORITY SYSTEM, sin sesión iniciada, RunLevel Highest y WorkingDirectory.",
   "caption": "Arranque retrasado, recuperación y tarea al inicio: el servidor se levanta solo."},
  [{"file": "7-paso2.svg", "step": 2, "after": "Automático retrasado y recuperación",
    "alt": "El comando sc.exe failure Spooler reset= 86400 actions= restart/180000/restart/180000/restart/180000, con dos flechas. reset= 86400 está en segundos, 24 horas: sin fallas, el contador vuelve a 0. restart/180000 está en milisegundos, 3 minutos, una acción por falla: primera, segunda y siguientes. Notas en ámbar: el espacio después del igual es obligatorio, reset= 86400 funciona y reset=86400 da error, lo mismo con start= delayed-auto; en PowerShell, sc a secas es Set-Content, hay que escribir sc.exe.",
    "caption": "Segundos para el reset, milisegundos para la espera, y un espacio después del igual."},
   {"file": "7-paso4.svg", "step": 4, "after": "Tarea al inicio, como SYSTEM, sin sesión",
    "alt": "Register-ScheduledTask Lab arranque en la carpeta Lab, desarmada en cuatro partes. Acción: powershell.exe -File C:\\Lab\\arranque.ps1, con -NoProfile y -ExecutionPolicy Bypass. Carpeta: -WorkingDirectory C:\\Lab; sin esto, el script escribe en System32. Disparador: New-ScheduledTaskTrigger -AtStartup, al encender sin esperar sesión. Cuenta: -User NT AUTHORITY SYSTEM con -RunLevel Highest. Nota: para probar, reiniciar la VM sin iniciar sesión, esperar un minuto y mirar C:\\Lab\\arranque.log; al terminar, Unregister-ScheduledTask.",
    "caption": "Acción, carpeta, disparador y cuenta de una tarea que corre sin nadie conectado."}],
  [C("Tipo de inicio del servicio",
     "Un VMS o una controladora corren como servicios de Windows, programas que viven sin que nadie inicie sesión. El tipo de inicio decide si arrancan solos con el equipo y en qué momento.",
     "Automático arranca con Windows; Automático retrasado arranca un rato después, cuando la red y la base de datos ya están arriba; Manual solo si alguien lo inicia. Se ve con Get-Service o sc.exe qc y se cambia con sc.exe config nombre start= delayed-auto, con el espacio después del igual.",
     "El servicio del VMS de un depósito fallaba en cada arranque porque salía antes que la base de datos local. Pasado a Automático retrasado, arranca siempre a la primera."),
   C("Recuperación ante fallas",
     "Un servicio que se cae de madrugada queda caído hasta que alguien lo note, a veces el lunes. La recuperación le dice a Windows qué hacer solo cuando el servicio termina mal.",
     "sc.exe failure nombre reset= 86400 actions= restart/180000/restart/180000/restart/180000: reiniciar a los 3 minutos en cada falla y volver el contador a cero después de un día sin fallas. sc.exe failureflag nombre 1 hace que también actúe si el servicio se detiene con error. sc.exe qfailure muestra cómo quedó.",
     "Un sábado se cae el servicio de grabación de una tienda en Ciudad Vieja. Con recuperación configurada, a los 3 minutos vuelve a grabar y el lunes solo encontrás el evento en el registro."),
   C("Tarea programada al inicio",
     "Hay cosas que no son servicio pero tienen que correr al encender: un script que monta una unidad, que registra el arranque o que levanta un programa auxiliar. Ponerlas en la carpeta Inicio depende de que alguien entre al equipo.",
     "Una tarea con disparador AtStartup, cuenta NT AUTHORITY\\SYSTEM y -RunLevel Highest corre al arrancar, sin sesión y con privilegios altos. Conviene darle carpeta propia con -TaskPath, -NoProfile y -WorkingDirectory: sin carpeta de inicio, el script deja sus archivos en C:\\Windows\\System32.",
     "Un puesto de monitoreo necesita un script que anote cada arranque. Como tarea AtStartup, el registro aparece aunque el equipo vuelva de un corte y nadie inicie sesión.")],
  """
### Un poco de historia

Los servicios existen desde Windows NT 3.1, en 1993: programas sin ventana que el Administrador de control de servicios arranca, detiene y vigila. sc.exe es la herramienta de consola para hablar con ese administrador, y por eso su sintaxis antigua, con el espacio obligatorio después del igual, sigue igual.

Windows Vista y Server 2008 sumaron el inicio Automático retrasado, pensado justamente para que no todos los servicios compitan en el mismo instante del arranque. En esa misma época, el Programador de tareas se rehízo y trajo disparadores como \"al iniciar el sistema\", que permiten correr algo sin depender de un usuario.

### Cómo funciona

Al encender, Windows levanta el Administrador de control de servicios, que arranca primero los servicios en Automático, respetando sus dependencias. Los que están en Automático retrasado esperan a que termine esa primera tanda y arrancan después, alrededor de dos minutos más tarde con la configuración de fábrica. Para un VMS que necesita red y base de datos, ese margen evita arrancar contra algo que todavía no está.

Mientras tanto, el Programador de tareas dispara las tareas con AtStartup. Una tarea que corre como SYSTEM no necesita contraseña guardada ni sesión: corre aunque nadie toque el equipo, y si no tiene carpeta de inicio usa la del sistema.

Cuando un servicio termina de forma inesperada, el administrador de servicios lo anota como falla, suma uno al contador y busca la acción configurada para ese número de falla: reiniciar el servicio, correr un programa o reiniciar el equipo, cada una con su espera en milisegundos. El contador vuelve a cero cuando pasa el tiempo de reset, en segundos, sin fallas nuevas.

Un servicio que se detiene \"prolijo\" pero con código de error no cuenta como falla, salvo que failureflag esté en 1. Con eso, la recuperación cubre también ese caso.
""",
  [{"file": "7-t1.svg", "after": "ese margen evita arrancar contra algo que todavía no está",
    "alt": "Animación en cuatro tiempos sobre una línea de tiempo desde el encendido, con cuatro carriles: servicios en Automático, servicio del VMS en Automático retrasado, tarea al inicio y sesión de usuario. 1: arrancan los servicios en Automático. 2: un rato después arranca el servicio del VMS, en retrasado. 3: la tarea AtStartup corre arranque.ps1 como SYSTEM y escribe C:\\Lab\\arranque.log sin sesión. 4: el servicio del VMS se cae, queda 3 minutos caído y la recuperación lo reinicia. El carril de sesión dice que nadie entró.",
    "caption": "Qué arranca y cuándo, y cómo vuelve un servicio caído."}],
  S("Servicio con recuperación y tarea al inicio",
    "Pone un servicio en Automático retrasado con recuperación ante fallas y registra una tarea al inicio como SYSTEM, sin sesión. Se puede pegar dos veces: los valores se vuelven a escribir y la tarea se reemplaza.",
    [("SERVICIO", "Spooler", "Nombre del servicio (en el laboratorio, la cola de impresión)"),
     ("ESPERA_MS", "180000", "Espera antes de reiniciar, en milisegundos (180000 = 3 minutos)"),
     ("RESET_S", "86400", "Segundos sin fallas para volver el contador a cero (86400 = 24 horas)"),
     ("TAREA", "Lab arranque", "Nombre de la tarea al inicio"),
     ("SCRIPT", "C:\\Lab\\arranque.ps1", "Script que corre la tarea"),
     ("CARPETA", "C:\\Lab", "Carpeta de inicio de la tarea")],
    r"""
# IES Training - Windows - Servicio con recuperacion y tarea al inicio
# PowerShell como administrador. Probalo en un equipo de banco.
& {
  $servicio = '{{SERVICIO}}'
  $esperaMs = {{ESPERA_MS}}
  $resetS   = {{RESET_S}}
  $tarea    = '{{TAREA}}'
  $script   = '{{SCRIPT}}'
  $carpeta  = '{{CARPETA}}'

  if (-not (Get-Service $servicio -ErrorAction SilentlyContinue)) { Write-Host ('No existe el servicio ' + $servicio); return }
  # Automatico retrasado: arranca cuando ya estan la red y la base
  sc.exe config $servicio start= delayed-auto
  # Reiniciar en cada falla; el contador vuelve a cero tras RESET_S sin fallas
  $acciones = "restart/$esperaMs/restart/$esperaMs/restart/$esperaMs"
  sc.exe failure $servicio reset= $resetS actions= $acciones
  sc.exe failureflag $servicio 1
  Write-Host '--- Servicio ---'
  Get-Service $servicio | Select-Object Name, Status, StartType
  sc.exe qfailure $servicio

  # Tarea al inicio, como SYSTEM y sin sesion; -Force la reemplaza si ya existe
  $a = New-ScheduledTaskAction -Execute 'powershell.exe' `
    -Argument ('-NoProfile -ExecutionPolicy Bypass -File "' + $script + '"') -WorkingDirectory $carpeta
  $t = New-ScheduledTaskTrigger -AtStartup
  Register-ScheduledTask -TaskName $tarea -TaskPath '\IES\' -Action $a -Trigger $t `
    -User 'NT AUTHORITY\SYSTEM' -RunLevel Highest -Force
  Write-Host ('Listo: ' + $servicio + ' en automatico retrasado, se reinicia a los ' + ($esperaMs / 60000) + ' min y la tarea ' + $tarea + ' corre al encender.')
  Write-Host 'Verifica con sc.exe qfailure y reiniciando el equipo de banco sin iniciar sesion.'
}
""",
    ["No mata el servicio para probar: la prueba de caída va a mano y nunca con el servicio del VMS en producción.",
     "La tarea queda en la carpeta \\IES\\ del Programador de tareas; para borrarla, Unregister-ScheduledTask con su nombre.",
     "Si el script de la tarea no existe, la tarea igual se crea y falla al arrancar: crealo antes."]))

# =====================================================================================  8
L("8",
  {"file": "8.svg", "alt": "Dos bloques. En Windows, con powercfg: standby-timeout-ac 0, suspensión nunca; hibernate-timeout-ac 0, hibernación nunca; disk-timeout-ac 0, apagar disco nunca; monitor-timeout-ac 15, el monitor sí se apaga; /hibernate off, sin hibernación ni inicio rápido; 0 quiere decir nunca. En el BIOS o UEFI, la opción Restore on AC Power Loss o After Power Failure con tres valores: Power On en verde, vuelve siempre que vuelve la luz; Last State en ámbar, solo si estaba prendido; Power Off en rojo, queda apagado. Nota: con una UPS que apaga el equipo en orden, Last State recuerda apagado y no vuelve; con UPS conviene Power On.",
   "caption": "powercfg para que no duerma, BIOS para que vuelva solo."},
  [{"file": "8-paso5.svg", "step": 5, "after": "entrá al BIOS o UEFI y buscá la opción",
    "alt": "Menú de BIOS genérico, dibujado y no copiado de una marca, con las pestañas Main, Advanced, Power (resaltada), Chipset y Boot. Entre otras opciones, Restore on AC Power Loss resaltada con el valor Power On, y abajo las opciones Power On, Last State y Power Off. A la derecha, cómo puede llamarse: Restore on AC Power Loss o After Power Failure, según la marca en Power, Advanced, Chipset o ACPI. Nota en verde: anotar cómo se llama en esa marca y ponerla en Power On.",
    "caption": "El nombre y la pestaña cambian; el valor buscado es Power On."},
   {"file": "8-paso6.svg", "step": 6, "after": "cortá la energía unos segundos",
    "alt": "Cuatro pasos en fila: encendido funcionando; corte, unos segundos sin luz, en rojo; vuelve la luz, Power On arranca solo, en verde; confirmá con el evento 6008. Debajo, la consola con Get-WinEvent -FilterHashtable LogName System e Id 6008, MaxEvents 3, y una fila de ejemplo con fecha y hora, Id 6008, el apagado anterior fue inesperado. Nota: el 6008 marca un apagado inesperado, corte de luz o pantallazo azul; nunca hacer esta prueba en un servidor en producción con discos girando.",
    "caption": "Cortar, ver que vuelve solo y confirmarlo con el 6008."}],
  [C("Energía en nunca",
     "Windows viene pensado para escritorios y notebooks: duerme para ahorrar energía. Un puesto de monitoreo o un servidor de VMS que se suspende deja de grabar o de mostrar alarmas sin que nadie lo note.",
     "powercfg /change con standby-timeout-ac, hibernate-timeout-ac y disk-timeout-ac en 0, que quiere decir nunca, con el equipo enchufado. El monitor sí se puede apagar, con monitor-timeout-ac. powercfg /requests y /lastwake muestran qué mantiene despierto o despertó al equipo.",
     "En una central de monitoreo, los puestos amanecían suspendidos y el operador perdía los primeros eventos del turno. Con todo en nunca y el monitor a los 15 minutos, el problema no volvió."),
   C("Inicio rápido (Fast Startup)",
     "Hace que Windows arranque más rápido guardando el núcleo del sistema en disco al apagar, como una hibernación parcial. En un equipo 24/7 no aporta y trae efectos secundarios.",
     "Con el inicio rápido activo, Wake on LAN puede fallar y algunas actualizaciones no terminan de aplicarse porque el equipo nunca arranca \"en limpio\". powercfg /hibernate off apaga la hibernación y con ella el inicio rápido.",
     "Una PC de portería que se prende por Wake on LAN desde el servidor dejó de despertar después de una actualización. Con /hibernate off, vuelve a responder."),
   C("Vuelta tras corte en el BIOS",
     "Windows no puede encender un equipo apagado: eso lo decide el BIOS o UEFI cuando vuelve la energía. Sin esa opción bien puesta, un servidor puede quedar apagado hasta que alguien vaya a apretar el botón.",
     "La opción se llama Restore on AC Power Loss o After Power Failure, en Power, Advanced, Chipset o ACPI. Power On enciende siempre que vuelve la luz; Last State, solo si estaba prendido. Con una UPS que apaga en orden, el último estado es apagado y Last State no vuelve.",
     "Un NVR en una sucursal del interior quedaba apagado después de cada corte largo, aunque tenía UPS. La UPS lo apagaba prolijo y el BIOS estaba en Last State. En Power On, vuelve solo.")],
  """
### Un poco de historia

Los estados de energía que usa Windows salen de ACPI, una norma que Intel, Microsoft y Toshiba presentaron en 1996 para que el sistema operativo, y no el BIOS, manejara la energía. ACPI definió los estados que todavía se usan: S3 es la suspensión, con la memoria alimentada; S4 la hibernación, con la memoria guardada en disco; S5 el apagado.

Windows 8, en 2012, sumó el inicio rápido: al apagar, en vez de cerrar todo, guarda el núcleo en disco y lo recupera al encender. Para una notebook es una ventaja; para un servidor que casi nunca se apaga, es una complicación más. La vuelta tras corte, en cambio, siempre fue cosa del BIOS de la placa madre.

### Cómo funciona

powercfg trabaja sobre el plan de energía activo y guarda cada valor dos veces: con corriente (ac) y con batería (dc). Un tiempo en 0 quiere decir nunca. /hibernate off borra el archivo de hibernación, y como el inicio rápido usa ese mismo mecanismo, también lo apaga.

Cuando vuelve la energía después de un corte, Windows todavía no existe: el que decide es el chipset de la placa, según lo que diga el BIOS. Con Power On, enciende siempre. Con Last State, mira cuál era el último estado guardado: si el equipo estaba prendido cuando se cortó, lo prende; si estaba apagado, no.

La trampa está en la UPS. Durante un corte largo, la UPS sostiene el servidor hasta que la batería baja y entonces le pide un apagado ordenado. Para Windows y para el BIOS fue un apagado normal, y el último estado quedó en apagado. Cuando vuelve la luz, Last State no lo enciende. Power On sí, con la contra de que también enciende equipos que alguien apagó a propósito.

Si el corte fue brusco, sin UPS o con la batería agotada, Windows no llegó a apagarse prolijo. Al arrancar de nuevo, el servicio de registro lo nota y escribe el evento 6008, apagado inesperado. Así se confirma una prueba de corte.
""",
  [{"file": "8-t1.svg", "after": "Last State no lo enciende",
    "alt": "Animación en cuatro tiempos con una UPS que alimenta dos servidores del VMS iguales, uno con el BIOS en Last State y otro en Power On. 1: se corta la luz y la UPS sostiene a los dos, encendidos. 2: con la batería baja, la UPS los apaga en orden. 3: vuelve la luz y el de Last State sigue apagado, marcado en rojo, porque recordó apagado. 4: el de Power On arranca solo, marcado en verde.",
    "caption": "Con UPS que apaga en orden, Last State no vuelve y Power On sí."}],
  S("Equipo 24/7: energía en nunca",
    "Pone suspensión, hibernación y apagado de disco en nunca con corriente, deja apagar el monitor, apaga hibernación e inicio rápido y muestra qué mantiene despierto al equipo y los últimos apagados inesperados.",
    [("MONITOR_MIN", "15", "Minutos para apagar el monitor (0 = nunca)")],
    r"""
# IES Training - Windows - Equipo 24/7: energia en nunca
# Consola como administrador. Se puede pegar dos veces: los valores se vuelven a escribir.
& {
  $monitorMin = {{MONITOR_MIN}}

  Write-Host '--- Plan activo ---'
  powercfg /getactivescheme

  # Con corriente: suspension, hibernacion y disco en nunca (0)
  powercfg /change standby-timeout-ac 0
  powercfg /change hibernate-timeout-ac 0
  powercfg /change disk-timeout-ac 0
  powercfg /change monitor-timeout-ac $monitorMin
  # Sin hibernacion ni inicio rapido
  powercfg /hibernate off

  Write-Host '--- Estados disponibles y quien mantiene o despierta el equipo ---'
  powercfg /a
  powercfg /requests
  powercfg /lastwake

  Write-Host '--- Ultimos apagados inesperados (6008) ---'
  Get-WinEvent -FilterHashtable @{LogName='System'; Id=6008} -MaxEvents 3 -ErrorAction SilentlyContinue |
    Select-Object TimeCreated, Message
  # El BIOS no se toca desde Windows: Restore on AC Power Loss en Power On, a mano.
  Write-Host ('Listo: el equipo no duerme y el monitor se apaga a los ' + $monitorMin + ' min. Falta el BIOS en Power On tras corte.')
}
""",
    ["La vuelta tras corte del BIOS no se puede cambiar desde este script: queda como paso a mano en el equipo.",
     "Si no aparece ningún 6008, no hubo apagados inesperados que el registro todavía guarde.",
     "Con UPS que apaga en orden, el BIOS va en Power On."]))

# =====================================================================================  9
L("9",
  {"file": "9.svg", "alt": "A la izquierda, un gráfico genérico del Monitor de confiabilidad, perfmon /rel, con el índice de 1 a 10 por día: estable cerca de 10 de lunes a jueves, se desploma a 3 el viernes, resaltado, y sube de a poco. Ese día, en la misma columna, una instalación de una aplicación nueva y una falla de aplicación. A la derecha, dos tarjetas: 1074, quién pidió el reinicio, un usuario, Windows Update como SYSTEM o un programa, con fecha y hora; 6008 en rojo, apagado inesperado, corte de luz o pantallazo azul. Nota: Get-WinEvent -FilterHashtable con LogName System e Id 1074 filtra en el origen, mucho más rápido que Where-Object.",
   "caption": "Confiabilidad dice qué cambió; los eventos 1074 y 6008, quién reinició."},
  [{"file": "9-paso1.svg", "step": 1, "after": "Abrí el Monitor de confiabilidad",
    "alt": "Dibujo genérico del Monitor de confiabilidad abierto con Win+R y perfmon /rel, en vista por semanas. El gráfico muestra el índice estable y una caída fuerte en la semana 4, resaltada. Debajo, las filas de fallas de aplicaciones, fallas de Windows e información de instalaciones y actualizaciones, con una cruz roja y un ícono de información en la columna de la semana 4. Notas: la semana donde el índice se desploma, mirar qué se instaló; guardar el historial de confiabilidad en XML para el informe.",
    "caption": "La caída del índice y la instalación del mismo día, en una columna."},
   {"file": "9-paso4.svg", "step": 4, "after": "Errores y críticos del log Sistema",
    "alt": "El comando Get-WinEvent -FilterHashtable con LogName System, Level 1,2 y StartTime de las últimas 24 horas, desarmado en tres partes: LogName System, qué log; Level 1,2, qué nivel, 1 crítico y 2 error; StartTime, desde cuándo. Debajo, en verde, FilterHashtable: el servicio de registro devuelve solo lo que coincide, rápido aunque el log sea grande; en ámbar, Where-Object: trae todos los eventos a PowerShell y recién ahí filtra, con logs grandes tarda mucho más.",
    "caption": "Log, nivel y fecha en el filtro: el registro hace el trabajo."}],
  [C("Monitor de confiabilidad",
     "Ante \"ayer andaba y hoy no\", la primera pregunta es qué cambió. Revisar a mano instalaciones, actualizaciones y fallas en logs distintos lleva mucho tiempo; el Monitor de confiabilidad las junta por día en un solo gráfico.",
     "Se abre con perfmon /rel. Muestra un índice de 1 a 10 por día o por semana y, debajo, las fallas de aplicaciones y de Windows y las instalaciones y actualizaciones. Se busca la caída del índice y lo que se instaló ese día. El historial se exporta a XML para el informe.",
     "Un servidor de control de acceso en un club de Punta Carretas empieza a cerrarse solo. En Confiabilidad, el índice cae el mismo día que se instaló un software de backup del cliente."),
   C("Eventos 1074 y 6008",
     "Cuando un servidor se reinició y nadie sabe por qué, el registro de eventos tiene la respuesta: distingue un reinicio que alguien pidió de un apagado que nadie pidió.",
     "El 1074 en el log System dice quién o qué pidió el reinicio: un usuario, el servicio de Windows Update como SYSTEM o un programa. El 6008 marca un apagado inesperado, como un corte de luz o un pantallazo azul. Se buscan con Get-WinEvent filtrando por Id.",
     "El cliente jura que nadie tocó el NVR. El 1074 de las 3:05 dice que lo reinició Windows Update: la explicación sale con fecha y hora, sin suposiciones."),
   C("FilterHashtable",
     "Los logs de un servidor guardan decenas de miles de eventos. Traerlos todos a PowerShell para quedarse con tres es lento, y en un servidor cargado se nota.",
     "Get-WinEvent -FilterHashtable @{LogName='System'; Id=1074} manda el filtro al servicio de registro, que devuelve solo lo que coincide. Acepta LogName, Id, Level (1 crítico, 2 error) y StartTime. Filtrar después con Where-Object funciona, pero tarda mucho más.",
     "Para un informe mensual de un edificio, sacás todos los errores y críticos del último mes con Level=1,2 y StartTime, en segundos, en vez de esperar minutos.")],
  """
### Un poco de historia

El registro de eventos existe desde Windows NT 3.1, en 1993. Windows Vista, en 2007, lo rehízo por completo: un formato nuevo, muchos más registros por componente y consultas en XPath. Con Vista llegó también el Monitor de confiabilidad, que resume la salud del equipo en un índice por día.

PowerShell trajo primero Get-EventLog, que leía solo los registros clásicos. Get-WinEvent, de PowerShell 2.0, entiende el formato nuevo y acepta filtros que se resuelven en el propio servicio de registro. En PowerShell 7, Get-EventLog ya no existe, así que Get-WinEvent es la herramienta que conviene aprender.

### Cómo funciona

Cada registro, como System o Application, es un archivo con un tamaño máximo. Cuando se llena, los eventos más viejos se pisan. Por eso el tamaño del log define cuánto historial tenés: si se sobrescribió, no hay forma de saber quién reinició hace un mes.

Cada evento tiene un origen, un número de Id, un nivel (1 crítico, 2 error, 3 advertencia, 4 información) y una fecha. Cuando un programa o una persona pide apagar o reiniciar, Windows escribe el 1074 con el proceso, el usuario y el motivo. Si el equipo se apagó sin ese aviso, al arrancar de nuevo el servicio de registro lo nota y escribe el 6008.

Con Where-Object, Get-WinEvent lee todos los eventos del log, los convierte en objetos y recién ahí PowerShell descarta los que no sirven. Con -FilterHashtable, el filtro viaja al servicio de registro convertido en una consulta, y del registro salen solo los eventos que coinciden. Mismo resultado, una fracción del trabajo.

El Monitor de confiabilidad arma su índice con fallas de aplicaciones, fallas de Windows y otros problemas de cada día, y pone en la misma columna las instalaciones y actualizaciones. La caída del índice y el cambio aparecen juntos.
""",
  [{"file": "9-t1.svg", "after": "Mismo resultado, una fracción del trabajo.",
    "alt": "Animación en cuatro tiempos con el log System a la izquierda, con eventos 7036, 1074, 10016, 6008 y otros, y la consola de PowerShell a la derecha. 1: con Where-Object, Get-WinEvent trae todos los eventos a PowerShell. 2: PowerShell los revisa uno por uno y descarta casi todos, queda el 1074. 3: con -FilterHashtable, el pedido viaja al registro con el filtro LogName System e Id 1074. 4: el registro devuelve solo ese evento.",
    "caption": "El filtro en el origen hace que viaje solo lo que buscás."}],
  S("Qué pasó en este equipo",
    "Muestra quién pidió reinicios (1074), los apagados inesperados (6008), los errores y críticos del log Sistema de las últimas horas y cuánto historial guarda el log, y abre el Monitor de confiabilidad. No cambia nada.",
    [("HORAS", "24", "Horas hacia atrás para errores y críticos"),
     ("MAX_EVENTOS", "5", "Cantidad de eventos 1074 y 6008 a mostrar")],
    r"""
# IES Training - Windows - Que paso en este equipo
# Solo lee: no cambia nada. PowerShell como administrador.
& {
  $horas = {{HORAS}}
  $max   = {{MAX_EVENTOS}}

  Write-Host '--- Quien pidio reinicios (1074) ---'
  Get-WinEvent -FilterHashtable @{LogName='System'; Id=1074} -MaxEvents $max -ErrorAction SilentlyContinue |
    Format-List TimeCreated, Message

  Write-Host '--- Apagados inesperados (6008) ---'
  Get-WinEvent -FilterHashtable @{LogName='System'; Id=6008} -MaxEvents $max -ErrorAction SilentlyContinue |
    Select-Object TimeCreated, Message

  Write-Host ('--- Errores y criticos de las ultimas ' + $horas + ' horas ---')
  Get-WinEvent -FilterHashtable @{LogName='System'; Level=1,2; StartTime=(Get-Date).AddHours(-$horas)} -ErrorAction SilentlyContinue |
    Select-Object TimeCreated, Id, ProviderName, Message | Format-Table -Wrap

  Write-Host '--- Cuanto historial guarda el log ---'
  Get-WinEvent -ListLog System | Select-Object LogName, MaximumSizeInBytes, RecordCount

  # Confiabilidad cruza fallas con instalaciones y actualizaciones por dia
  perfmon /rel
  Write-Host 'Listo: busca el dia con el indice mas bajo y guarda el historial de confiabilidad para el informe.'
}
""",
    ["Si un bloque sale vacío, no hay eventos de ese tipo en lo que el log todavía guarda.",
     "Para filtrar por otro Id, cambiá el número en el filtro: sigue siendo rápido.",
     "Agrandar el tamaño máximo del log no está en el script: se decide con el cliente según cuánto historial necesita."]))

# =====================================================================================  10
L("10",
  {"file": "10.svg", "alt": "Tres tarjetas. Latencia, Avg. Disk sec/Transfer, cuánto tarda cada operación; en rojo, más de 25 ms sostenidos no da abasto. IOPS, Disk Transfers/sec, operaciones por segundo; se compara contra lo que da ese disco. Cola, Avg. Disk Queue Length, cuántas esperan su turno; en ámbar, un disco solo no más de 2. Umbrales según woshub; para grabación manda la guía del fabricante del VMS. Abajo, en rojo: el antivirus no escanea la base de grabación; ejemplo de Milestone, C:\\mediadatabase y los archivos .blk, .idx y .pic, porque el escaneo puede cortar la grabación o corromper la base; se excluye solo lo que pide el fabricante, nunca un disco entero.",
   "caption": "Latencia, IOPS y cola, y la base de grabación fuera del antivirus."},
  [{"file": "10-paso3.svg", "step": 3, "after": "mientras copiás un archivo grande",
    "alt": "Arriba, la conversión 0,025 segundos por mil igual a 25 ms, el umbral de woshub para latencia sostenida. Debajo, dos paneles con valores de ejemplo. En reposo, en verde: latencia 0,002 s, muy lejos de la marca de 25 ms; IOPS 40; cola 0,1, lejos de la marca de 2. Copiando un archivo grande, en rojo: latencia 0,031 s, pasando la marca de 25 ms; IOPS 110; cola 3,4, pasando la marca de 2.",
    "caption": "Avg. Disk sec/Transfer viene en segundos: 0,025 son 25 ms."},
   {"file": "10-paso4.svg", "step": 4, "after": "Exclusiones de Defender actuales",
    "alt": "Consola de PowerShell con tres comandos: (Get-MpPreference).ExclusionPath, Add-MpPreference -ExclusionPath D:\\LabGrabacion y Add-MpPreference -ExclusionExtension .blk, .idx y .pic. Debajo, en verde: la carpeta de grabación, las carpetas, extensiones y procesos que indique el fabricante del VMS, anotados en el informe; en rojo: un disco entero por las dudas, excluir reduce la protección. Nota: al terminar el laboratorio, Remove-MpPreference con los mismos parámetros.",
    "caption": "Solo lo que pide el fabricante, y anotado."}],
  [C("Latencia, IOPS y cola",
     "\"El disco anda lento\" no se puede comparar ni poner en un informe. Tres contadores de Windows describen el disco con números: cuánto tarda cada operación, cuántas hace por segundo y cuántas esperan.",
     "Avg. Disk sec/Transfer es la latencia, en segundos; Disk Transfers/sec, las IOPS; Avg. Disk Queue Length, la cola. Se ven rápido en el Administrador de tareas y en resmon, y con Get-Counter se toma una muestra de un minuto. Según woshub, más de 25 ms sostenidos es un disco que no da abasto, y la cola de un disco solo no debería pasar de 2.",
     "Un NVR basado en Windows pierde cuadros en horario pico. Get-Counter muestra 40 ms de latencia y cola en 6 durante la tarde: el informe recomienda más discos o repartir cámaras, con números."),
   C("Reposo contra carga",
     "Un disco puede verse perfecto a las 3 de la mañana y no dar abasto a las 18. La medición sirve si se compara el mismo disco con y sin carga, o en el horario en que se pierden cuadros.",
     "Se toma una muestra en reposo, después otra copiando un archivo grande al mismo disco, y se comparan. Los contadores están en inglés; en Windows en español pueden figurar traducidos. Las pruebas de carga sintética, como DiskSpd, no se corren en producción en horario de uso.",
     "En el banco, el disco nuevo da 2 ms en reposo y 9 ms copiando. El viejo da 31 ms copiando: ya sabés cuál va al servidor de grabación."),
   C("Exclusiones del antivirus",
     "El antivirus en tiempo real abre y revisa cada archivo que se escribe. En la base de grabación eso consume recursos y puede bloquear archivos: Milestone advierte que puede cortar la grabación o corromper la base.",
     "Se excluye solo lo que indica el fabricante del VMS instalado: carpetas, extensiones y procesos. En Defender, Add-MpPreference -ExclusionPath y -ExclusionExtension; se revisa con Get-MpPreference y se quita con Remove-MpPreference. Todo queda anotado en el informe.",
     "En un servidor Milestone, excluís C:\\mediadatabase y los .blk, .idx y .pic, como pide su documentación. Nunca \"todo el disco D: por las dudas\": eso deja sin revisar todo lo que se copie ahí.")],
  """
### Un poco de historia

Windows NT trajo el Monitor de rendimiento y sus contadores, que siguen siendo la forma oficial de medir un disco: el objeto PhysicalDisk, con contadores como Avg. Disk sec/Transfer, existe desde entonces. El Administrador de tareas y el Monitor de recursos muestran los mismos datos con menos detalle.

La relación entre cola, ritmo y espera es más vieja que la informática personal: John Little la demostró en 1961, y se usa igual para un disco que para la fila de un banco. Del lado del video, los fabricantes de VMS empezaron a publicar listas de exclusiones del antivirus a medida que las grabaciones crecieron y los antivirus pasaron a revisar cada archivo en el momento.

### Cómo funciona

Cada cámara manda video al VMS y el VMS lo escribe en disco en pedidos chicos y continuos. El disco atiende esos pedidos de a uno: si llegan más rápido de lo que los atiende, se forma una fila.

La ley de Little dice que, en promedio, el largo de la fila es el ritmo de llegada por el tiempo que pasa cada pedido en el sistema. Para un disco: cola aproximadamente igual a IOPS por latencia. Con 110 IOPS y 0,031 segundos de latencia, la cola ronda 3,4. Por eso los tres números se miran juntos: si suben las IOPS y la latencia se mantiene, el disco acompaña; si la latencia y la cola suben juntas, el disco está saturado.

Cuando la latencia pasa de 25 ms de forma sostenida, cada escritura espera demasiado, el VMS acumula video en memoria y, si no le alcanza, descarta cuadros. Un pico aislado no es problema; una tarde entera arriba del umbral, sí.

El antivirus agrega otra espera. El de tiempo real se mete en el sistema de archivos y revisa cada archivo que se abre o se escribe. Sobre una base de grabación, eso suma latencia a cada pedido y puede bloquear un archivo justo cuando el VMS necesita escribirlo.
""",
  [{"file": "10-t1.svg", "after": "cola aproximadamente igual a IOPS por latencia",
    "alt": "Animación en cuatro tiempos con cámaras que mandan pedidos a una cola de ocho lugares frente a un disco, y dos barras de ejemplo, latencia y cola. 1: con pocas cámaras la cola casi no tiene pedidos y la latencia es de unos 2 ms. 2: con más cámaras la cola empieza a llenarse. 3: la cola crece y la latencia sube a 18 ms. 4: la cola está llena, la latencia pasa la marca de 25 ms y se marca en rojo. Abajo, cola aproximadamente igual a IOPS por latencia.",
    "caption": "Cuando entran más pedidos de los que salen, la cola y la latencia suben juntas."}],
  S("Medir el disco que graba y excluir la base",
    "Toma una muestra de latencia, IOPS y cola del disco, compara con los umbrales de la lección y, si se indica una carpeta, agrega las exclusiones de Defender sin duplicarlas.",
    [("MUESTRAS", "12", "Cantidad de muestras"),
     ("INTERVALO_S", "5", "Segundos entre muestras (12 x 5 = un minuto)"),
     ("CARPETA_GRABACION", "D:\\LabGrabacion", "Carpeta a excluir según el fabricante; vacía para no excluir nada"),
     ("EXTENSIONES", "'.blk','.idx','.pic'", "Extensiones a excluir según el fabricante, entre comillas simples")],
    r"""
# IES Training - Windows - Medir el disco que graba y excluir la base
# PowerShell como administrador. Contadores en ingles: en Windows en espanol pueden figurar traducidos.
& {
  $muestras  = {{MUESTRAS}}
  $intervalo = {{INTERVALO_S}}
  $excluir   = '{{CARPETA_GRABACION}}'
  $exts      = @({{EXTENSIONES}})

  $c = '\PhysicalDisk(_Total)\Avg. Disk sec/Transfer',
       '\PhysicalDisk(_Total)\Disk Transfers/sec',
       '\PhysicalDisk(_Total)\Avg. Disk Queue Length'
  $r = Get-Counter -Counter $c -SampleInterval $intervalo -MaxSamples $muestras
  $lat = 0; $iops = 0; $cola = 0
  foreach ($m in $r.CounterSamples) {
    if ($m.Path -like '*sec/transfer') { $lat += $m.CookedValue }
    elseif ($m.Path -like '*transfers/sec') { $iops += $m.CookedValue }
    else { $cola += $m.CookedValue }
  }
  $latMs = [math]::Round($lat / $muestras * 1000, 1)
  $iops  = [math]::Round($iops / $muestras, 0)
  $cola  = [math]::Round($cola / $muestras, 2)
  Write-Host ('Latencia media: ' + $latMs + ' ms | IOPS: ' + $iops + ' | Cola: ' + $cola)
  if ($latMs -gt 25) { Write-Host 'Mas de 25 ms: si es sostenido, el disco no da abasto.' }
  if ($cola -gt 2) { Write-Host 'Cola mayor a 2 para un disco solo: revisa la carga.' }

  # Exclusiones: solo lo que pide el fabricante del VMS, sin duplicar
  if ($excluir) {
    if ((Get-MpPreference).ExclusionPath -notcontains $excluir) { Add-MpPreference -ExclusionPath $excluir }
    foreach ($e in $exts) {
      if ((Get-MpPreference).ExclusionExtension -notcontains $e) { Add-MpPreference -ExclusionExtension $e }
    }
  }
  Write-Host '--- Exclusiones actuales ---'
  (Get-MpPreference).ExclusionPath
  (Get-MpPreference).ExclusionExtension
  Write-Host 'Listo: numeros del disco y exclusiones anotados. Repeti la medicion en el horario en que se pierden cuadros.'
}
""",
    ["Medí en reposo y con carga, o en el horario del problema: una sola muestra no alcanza.",
     "Dejá CARPETA_GRABACION vacía para medir sin tocar el antivirus.",
     "Las exclusiones salen de la guía del fabricante del VMS instalado, nunca un disco entero; se quitan con Remove-MpPreference."]))

# =====================================================================================  11
L("11",
  {"file": "11.svg", "alt": "Cuatro tarjetas en orden. 1, en verde: backup restaurable con wbadmin -allCritical, la única marcha atrás real. 2: momento elegido, horas activas y ventana, nada de reinicios sorpresa. 3: aviso en servidores, avisar para instalar y reiniciar, la opción 7 de Microsoft. 4: verificar con Get-HotFix y el evento 1074, qué entró y quién reinició. Debajo: ciclo validado con el VMS, Bosch pide para su VMS un ciclo de 6 meses como máximo; en rojo, noviembre de 2024, servidores con Windows Server 2022 amanecieron actualizados a 2025, sin licencia, por una actualización mal clasificada, y sin backup quedaba reinstalar o pagar. Nota: antes de actualizar, backup, siempre.",
   "caption": "Actualizar con calendario, aviso y backup antes de cada cambio grande."},
  [{"file": "11-paso1.svg", "step": 1, "after": "Opciones avanzadas > Horas activas",
    "alt": "La ruta Configuración, Windows Update, Opciones avanzadas, Horas activas, y una barra de 24 horas con las horas activas de 8:00 a 17:00 marcadas en verde, donde Windows no reinicia, y el resto marcado como puede reiniciar. Notas: de fábrica van de 8 a 17 y el rango máximo es de 18 horas, se ajustan al horario de operación del cliente; en ámbar, solo cuenta como usuario conectado una sesión local o de escritorio remoto activa, sin nadie el equipo se reinicia cuando le toca.",
    "caption": "Dentro de las horas activas no reinicia; fuera, sí."},
   {"file": "11-paso4.svg", "step": 4, "after": "Backup de los volúmenes críticos",
    "alt": "Consola de símbolo del sistema con wbadmin start backup -backupTarget:E: -allCritical -quiet y wbadmin get versions -backupTarget:E:, con la línea Identificador de versión resaltada. Debajo, el servidor con C: y los volúmenes críticos, una flecha -allCritical hacia el disco E:, destino del backup, y un recuadro verde: paso 5, a la planilla el identificador y la fecha de esta versión. Nota: -allCritical incluye lo necesario para restaurar el sistema; un backup se confirma restaurando un archivo a otra carpeta con -recoveryTarget; -recreateDisks borra datos.",
    "caption": "Backup de lo crítico a otro disco, con su identificador en la planilla."}],
  [C("Ciclo de actualización",
     "Un servidor sin parches queda expuesto, pero uno que se actualiza solo puede reiniciarse en medio de la grabación o cambiar algo que el VMS no soporta. Un ciclo definido busca el punto medio: actualizar siempre, en un momento elegido.",
     "Se acuerda con el cliente una ventana y una frecuencia validada con el fabricante del VMS: Bosch, por ejemplo, pide un ciclo de 6 meses como máximo. Get-HotFix muestra qué se instaló y el evento 1074 quién reinició por eso.",
     "Para los servidores de grabación de una cadena de farmacias, se acuerda el segundo domingo de cada mes a la madrugada, con backup antes y control al día siguiente."),
   C("Horas activas y opción 7",
     "Windows reinicia para terminar de instalar, y si nadie le dice cuándo, elige él. Las horas activas y la opción 7 le ponen reglas a ese momento.",
     "Las horas activas, de fábrica de 8 a 17 y con un rango máximo de 18 horas, son el horario en que Windows no reinicia. Solo cuenta como usuario conectado una sesión local o de escritorio remoto activa: un servidor sin nadie se reinicia cuando le toca. Para servidores, Microsoft sugiere la opción 7 de Configurar actualizaciones automáticas: avisar para instalar y avisar para reiniciar.",
     "El puesto de monitoreo trabaja de 7 a 23: ajustás las horas activas a ese rango de 16 horas y los reinicios caen de madrugada."),
   C("Backup restaurable",
     "Si una actualización rompe algo, desinstalarla no siempre alcanza. El backup es la única marcha atrás real, y solo sirve si se sabe restaurar.",
     "En Windows Server se instala la característica Windows-Server-Backup y se corre wbadmin start backup -backupTarget:E: -allCritical -quiet. wbadmin get versions lista las versiones con su identificador, que va a la planilla. Se prueba restaurando un archivo con wbadmin start recovery a otra carpeta.",
     "En noviembre de 2024, servidores con Windows Server 2022 amanecieron actualizados a 2025 y sin licencia. Los que tenían backup restaurable volvieron atrás en una mañana.")],
  """
### Un poco de historia

Windows Update existe desde 1998. En octubre de 2003 Microsoft ordenó la publicación de parches en un día fijo, el segundo martes de cada mes, que el ambiente conoce como Patch Tuesday. Desde Windows 10, los parches son acumulados: cada uno trae todos los anteriores.

En Windows Server 2008, Windows Server Backup y su comando wbadmin reemplazaron al viejo NTBackup. En noviembre de 2024, varias empresas encontraron sus servidores Windows Server 2022 actualizados a 2025 de un día para otro, sin licencia, porque una actualización llegó mal clasificada a herramientas de parches de terceros. Quien tenía backup restaurable volvió atrás; el resto tuvo que reinstalar o pagar la licencia.

### Cómo funciona

Una actualización se descarga e instala en segundo plano, pero muchos archivos del sistema están en uso y solo se pueden reemplazar al reiniciar. Hasta ese reinicio, la actualización queda pendiente.

Las horas activas le dicen a Windows en qué horario no reiniciar. Fuera de ese rango, si no hay nadie conectado, reinicia solo. Para Windows, conectado quiere decir una sesión local o de escritorio remoto activa: un servidor de VMS que nadie mira casi siempre cumple la condición y se reinicia de madrugada, con la grabación cortada unos minutos.

En servidores, Microsoft sugiere la opción 7 de la directiva Configurar actualizaciones automáticas: avisar para instalar y avisar para reiniciar. Así las actualizaciones no se aplican hasta que un técnico elige la ventana, con el backup hecho y el cliente avisado.

wbadmin con -allCritical incluye todos los volúmenes que el sistema necesita para arrancar y restaurarse. Cada backup queda como una versión con su identificador de fecha y hora. Restaurar un archivo de prueba con -recoveryTarget confirma que el backup sirve; -recreateDisks, en cambio, rehace los discos y borra lo que tengan.
""",
  [{"file": "11-t1.svg", "after": "se reinicia de madrugada, con la grabación cortada",
    "alt": "Animación en cuatro tiempos sobre una barra de 24 horas con las horas activas de 8 a 17 en verde y un indicador de la hora que avanza. 1: una actualización queda instalada y pendiente de reinicio. 2: dentro de las horas activas, Windows no reinicia. 3: fuera de ese horario y sin sesiones locales ni de escritorio remoto activas, el equipo se reinicia solo. 4: en un servidor con la opción 7, Windows avisa antes de instalar y de reiniciar, y el técnico elige la ventana con el backup hecho.",
    "caption": "Horas activas, sesiones y opción 7 deciden cuándo reinicia."}],
  S("Antes de actualizar: qué entró, quién reinició y backup",
    "Lista las últimas actualizaciones y los reinicios 1074 y, en Windows Server, instala la característica de backup si falta y hace un backup de los volúmenes críticos al disco indicado.",
    [("DESTINO_BACKUP", "E:", "Disco destino del backup, distinto del sistema"),
     ("CANTIDAD", "10", "Cantidad de actualizaciones y eventos a mostrar")],
    r"""
# IES Training - Windows - Antes de actualizar: que entro, quien reinicio y backup
# PowerShell como administrador. El backup es solo para Windows Server.
& {
  $destino  = '{{DESTINO_BACKUP}}'
  $cantidad = {{CANTIDAD}}

  Write-Host '--- Ultimas actualizaciones instaladas ---'
  Get-HotFix | Sort-Object InstalledOn -Descending | Select-Object -First $cantidad
  Write-Host '--- Quien reinicio (1074) ---'
  Get-WinEvent -FilterHashtable @{LogName='System'; Id=1074} -MaxEvents $cantidad -ErrorAction SilentlyContinue |
    Select-Object TimeCreated, Message

  # Caracteristica de backup: si ya esta instalada, no hace nada
  try { Install-WindowsFeature Windows-Server-Backup -ErrorAction Stop }
  catch { Write-Host 'No se pudo instalar Windows-Server-Backup: no es Windows Server o falta administrador.'; return }

  # Backup de los volumenes criticos para restaurar el sistema
  wbadmin start backup ('-backupTarget:' + $destino) -allCritical -quiet
  wbadmin get versions ('-backupTarget:' + $destino)

  Write-Host ('Listo: backup en ' + $destino + '. Anota el identificador de version y la fecha en la planilla del servidor.')
  Write-Host 'Confirma que sirve restaurando un archivo de prueba con wbadmin start recovery a otra carpeta.'
}
""",
    ["El backup puede tardar: corrélo en la ventana acordada, no en horario de grabación pesada.",
     "Cada corrida suma una versión nueva en el destino; no borra las anteriores.",
     "El script no restaura nada: -recreateDisks borra datos y solo se usa sabiendo lo que hace."]))

# =====================================================================================  12
L("12",
  {"file": "12.svg", "alt": "Tres tarjetas, una por llave. Administrador local, único por equipo: Windows LAPS si hay dominio, guardado en AD o Entra ID, es la puerta cuando el dominio no responde. Clave de BitLocker, 48 dígitos de recuperación: fuera del disco cifrado, en un gestor de contraseñas o AD, y sin ella no hay recuperación. Contraseña DSRM del controlador de dominio: nunca en texto plano, ni en un script ni en un ticket, se pide de forma segura. Regla en verde: ninguna llave vive solo dentro del equipo que protege.",
   "caption": "Administrador local, BitLocker y DSRM: cada llave guardada fuera del equipo."},
  [{"file": "12-paso2.svg", "step": 2, "after": "Anotá el ID del protector",
    "alt": "Salida abreviada de manage-bde -protectors -get C: con un protector TPM y un protector Contraseña numérica, con su ID resaltado y la contraseña tapada con numerales. Una flecha verde, copiar, lleva al gestor de contraseñas de la empresa, con una entrada nueva para el equipo SRV-VMS-01 y el ID del protector. Notas: anotar el ID y copiar la clave con el nombre del equipo, y si hay dominio y la directiva lo permite también a Active Directory; en rojo, nunca guardarla solo en el mismo disco cifrado, ni el soporte de Microsoft la puede recuperar. Datos de ejemplo.",
    "caption": "La clave de recuperación va al gestor, con el nombre del equipo y el ID."},
   {"file": "12-paso4.svg", "step": 4, "after": "suspendé BitLocker por un reinicio",
    "alt": "El comando Suspend-BitLocker -MountPoint C: -RebootCount 1 y cuatro pasos: suspender por un reinicio; actualizar BIOS o firmware; reinicio, arranca sin pedir clave, en verde; se reanuda solo y vuelve a proteger, en verde. Debajo, en rojo, sin suspender: un cambio de BIOS, firmware o hardware puede hacer aparecer la pantalla de recuperación de BitLocker, y ahí solo sirve la clave guardada fuera del equipo. Nota: -RebootCount 1 hace que la protección vuelva sola después del primer reinicio.",
    "caption": "Suspender por un reinicio deja pasar el cambio de BIOS sin pedir la clave."},
   {"file": "12-paso5.svg", "step": 5, "after": "Quién es administrador local",
    "alt": "Consola con Get-LocalGroupMember -SID S-1-5-32-544, el grupo Administradores en cualquier idioma, y tres miembros de ejemplo: el usuario local Administrador de SRV-VMS-01, el grupo Admins. del dominio de EMPRESA desde Active Directory y un usuario local soporte2 resaltado en ámbar. Notas: una cuenta que nadie reconoce se anota y se consulta antes de borrarla, puede ser de un software o de otro proveedor; mínimo privilegio, cada equipo con su administrador local único y recuperable y el resto con lo mínimo.",
    "caption": "Quién tiene llave de administrador, y qué hacer con la que nadie reconoce."}],
  [C("Administrador local único (Windows LAPS)",
     "Cuando todos los equipos de un cliente tienen la misma contraseña de administrador local, quien la saca de uno entra a todos: eso se llama movimiento lateral. Además, esa cuenta es la puerta de emergencia cuando el dominio no responde.",
     "Windows LAPS genera una contraseña única y aleatoria para el administrador local de cada equipo unido al dominio, la rota y la guarda en Active Directory o en Entra ID. Viene integrado en Windows 11 y en Server 2019 a 2025 con las actualizaciones de abril de 2023. Sin dominio, cada equipo con su clave en el gestor de contraseñas.",
     "Una empresa con 30 puestos de monitoreo usaba la misma clave de administrador en todos. Con LAPS, cada puesto tiene la suya, y cuando el dominio se cae entrás al servidor con su clave local."),
   C("Clave de recuperación de BitLocker",
     "BitLocker cifra el disco para que nadie lea los datos si se roban el equipo. Cuando algo cambia en el arranque, pide una clave de recuperación; si nadie la tiene, los datos se pierden, y ni el soporte de Microsoft la puede recuperar.",
     "manage-bde -status y -protectors -get muestran el estado y los protectores. Se anota el ID del protector Contraseña numérica y la clave va al gestor de contraseñas con el nombre del equipo, o a Active Directory con Backup-BitLockerKeyProtector si hay dominio. Nunca solo en el mismo disco cifrado.",
     "Una notebook de un supervisor pide la clave después de un cambio de placa. Buscás el nombre del equipo en el gestor, comparás el ID del protector y la notebook arranca en cinco minutos."),
   C("Suspender antes de tocar el BIOS",
     "Una actualización de BIOS o de firmware cambia lo que BitLocker mide al arrancar, y puede disparar la pantalla de recuperación en el peor momento, con el cliente mirando.",
     "Suspend-BitLocker -MountPoint C: -RebootCount 1 deja la protección en pausa por un reinicio: el cambio pasa sin pedir clave y después se reanuda sola. Igual conviene tener la clave a mano.",
     "Antes de actualizar el BIOS de un servidor de VMS, suspendés BitLocker por un reinicio. El servidor vuelve solo y sigue cifrado."),
   C("Contraseña DSRM",
     "Un controlador de dominio tiene una cuenta de emergencia para arrancar en el modo de restauración de servicios de directorio, cuando Active Directory no funciona. Esa contraseña es tan valiosa como la del dominio.",
     "Se define al crear el controlador de dominio, por ejemplo con Install-ADDSForest. Nunca se escribe en texto plano en un script, un ticket o un chat: se pide de forma segura en el momento y se guarda en el gestor de contraseñas.",
     "Al montar el dominio de un cliente, la guía interna dejaba la contraseña DSRM escrita en el script de instalación. Se cambió para que la pida al correrlo, y la clave quedó solo en el gestor.")],
  """
### Un poco de historia

BitLocker llegó con Windows Vista, en 2007, y desde el principio se apoyó en el TPM, un chip de seguridad de la placa madre que guarda la llave del disco. Su clave de recuperación es una contraseña numérica de 48 dígitos.

Microsoft publicó el primer LAPS como herramienta aparte en 2015, para terminar con la misma contraseña de administrador en todos los equipos. En abril de 2023 lo integró en Windows como Windows LAPS, con soporte para Entra ID, y el LAPS heredado quedó en desuso. Windows 11 24H2 y Server 2025 le sumaron gestión automática de la cuenta y frases de contraseña. La contraseña DSRM existe desde Active Directory en Windows 2000.

### Cómo funciona

Al encender, el TPM mide cada pieza del arranque, como el BIOS, el firmware y el cargador, y compara esas mediciones con las que guardó cuando se activó BitLocker. Si coinciden, entrega la llave y Windows arranca sin pedir nada. Si algo cambió, el TPM no la entrega y aparece la pantalla de recuperación, que solo se pasa con la clave de 48 dígitos.

Para el TPM, un BIOS distinto podría ser alguien que manipuló el arranque. No distingue una actualización legítima de un ataque, y por eso se suspende BitLocker antes: suspendido, la llave queda disponible por la cantidad de reinicios indicada y después la protección se vuelve a activar sola.

Windows LAPS trabaja desde cada equipo. El propio equipo genera una contraseña aleatoria para su administrador local, la cambia según la directiva y la guarda en un atributo de su objeto en Active Directory, o en Entra ID, que solo pueden leer las cuentas autorizadas. Si alguien obtiene la contraseña de un puesto, esa clave no le sirve en ningún otro.

La regla que une las tres llaves es la misma: la de BitLocker no va en el disco que cifra, la del administrador local no se repite en otros equipos y la DSRM no queda escrita en ningún archivo.
""",
  [{"file": "12-t1.svg", "after": "que solo se pasa con la clave de 48 dígitos",
    "alt": "Animación en cuatro tiempos con el arranque (BIOS, firmware y cargador), el TPM que guarda la llave y la medición del arranque, y el disco C: cifrado con BitLocker. 1: el TPM compara lo que mide con lo que guardó. 2: si coincide, entrega la llave y Windows arranca sin pedir nada. 3: con un BIOS nuevo la medición no coincide y aparece la pantalla de recuperación que pide la clave de 48 dígitos. 4: con BitLocker suspendido por un reinicio, arranca sin pedir clave y después vuelve a proteger.",
    "caption": "El TPM entrega la llave solo si el arranque es el mismo."},
   {"file": "12-t2.webp", "after": "esa clave no le sirve en ningún otro",
    "alt": "Comparación en dos paneles con cuatro puestos cada uno. A la izquierda, en rojo, sin LAPS: los cuatro puestos tienen la misma contraseña de administrador y desde el puesto 1 salen flechas rojas a los otros tres: quien la saca de uno entra a todos. A la derecha, en verde, con Windows LAPS: cada puesto tiene su propia clave, única, aleatoria, rotada y guardada en AD o Entra ID. Pie: las fuentes lo llaman movimiento lateral, saltar de equipo en equipo con la misma credencial.",
    "caption": "Con la misma clave en todos, uno abre todos; con LAPS, cada uno la suya."}],
  S("Llaves en orden: BitLocker y administradores locales",
    "Muestra el estado de BitLocker y el ID del protector de recuperación sin imprimir la clave, la respalda en Active Directory si se pide, y lista quién es administrador local.",
    [("UNIDAD", "C:", "Unidad cifrada a revisar"),
     ("RESPALDAR_AD", "no", "si para respaldar la clave en Active Directory (equipo en dominio y directiva que lo permita)")],
    r"""
# IES Training - Windows - Llaves en orden: BitLocker y administradores locales
# PowerShell como administrador. No imprime la clave de recuperacion.
& {
  $unidad      = '{{UNIDAD}}'
  $respaldarAD = '{{RESPALDAR_AD}}'

  manage-bde -status $unidad
  $vol = Get-BitLockerVolume $unidad
  $kp = $vol.KeyProtector | Where-Object KeyProtectorType -eq 'RecoveryPassword' | Select-Object -First 1
  if (-not $kp) {
    Write-Host 'No hay protector de contrasena numerica: no hay clave de recuperacion. Resolvelo antes de tocar el BIOS.'
  } else {
    Write-Host ('ID del protector de recuperacion: ' + $kp.KeyProtectorId)
    Write-Host 'La clave se ve con manage-bde -protectors -get: va al gestor de contrasenas con el nombre del equipo.'
    if ($respaldarAD -eq 'si') {
      Backup-BitLockerKeyProtector -MountPoint $unidad -KeyProtectorId $kp.KeyProtectorId
    }
  }
  # Antes de actualizar el BIOS, quita el numeral de la linea siguiente (se reanuda sola tras un reinicio):
  # Suspend-BitLocker -MountPoint $unidad -RebootCount 1

  Write-Host '--- Administradores locales (S-1-5-32-544) ---'
  Get-LocalGroupMember -SID S-1-5-32-544 | Select-Object ObjectClass, Name, PrincipalSource
  Write-Host ('Listo: ' + $env:COMPUTERNAME + ' revisado. Si hay cuentas que nadie reconoce, anotalas y consulta antes de borrarlas.')
}
""",
    ["El script no muestra la clave: se copia a mano del comando manage-bde -protectors -get directo al gestor.",
     "La suspensión de BitLocker queda comentada: se activa solo antes de un cambio de BIOS o firmware.",
     "No borra cuentas: las desconocidas se anotan y se consultan."]))

# ------------------------------------------------------------------ salida y chequeos
import re
order = [str(i) for i in range(1, 13)]
out = "/home/claude/ies-training/ilustraciones/windows/manifest.json"
json.dump({k: M[k] for k in order}, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
s = json.dumps(M, ensure_ascii=False)
print("ok", out, len(M), "lecciones · guiones largos:", "—" in s or "–" in s)
for k in order:
    t = M[k]["teoria_md"]
    w = len(re.findall(r"\w+", t))
    bad = [f["after"] for f in M[k]["teoria_figs"] if t.count(f["after"]) != 1 or not (15 <= len(f["after"]) <= 60)]
    code = M[k]["script_rsc"]["codigo"]
    nl = code.count("\n") + 1
    used = set(re.findall(r"\{\{([^{}]*)\}\}", code))
    decl = {v["nombre"] for v in M[k]["script_rsc"]["variables"]}
    nonascii = [ln for ln in code.split("\n") if any(ord(ch) > 127 for ch in ln)]
    print(k, "palabras", w, "conceptos", len(M[k]["concepts"]), "| script", nl, "líneas",
          "vars ok" if used == decl else f"VARS {used ^ decl}", "| no ascii" if nonascii else "",
          "| ? en código" if "?" in code else "",
          "teoria_figs mal:" if bad else "", bad if bad else "",
          "" if "### Un poco de historia" in t and "### Cómo funciona" in t else "SIN SUBTITULOS")
