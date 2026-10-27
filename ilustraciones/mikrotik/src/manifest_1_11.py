"""Genera manifest-1-11.json (ilustraciones, conceptos y teoría de las lecciones 1 a 11) y lo valida."""
import json, re
from pathlib import Path

CLASS = Path("/home/claude/claudemy/mikrotik/class")
OUT = Path("/home/claude/ies-training/ilustraciones/mikrotik/manifest-1-11.json")

M = {}

# =====================================================================================  1
M["1"] = {
    "fig": {"file": "1.svg",
            "alt": "Router de laboratorio con cinco puertos. ether1 está marcado como WAN y una notebook conectada ahí aparece con una cruz roja. ether2 a ether5 forman el bridge LAN y una notebook en ether2 aparece con un tilde verde. A la derecha, dos caminos para entrar: por IP 192.168.88.1 o por MAC desde Neighbors, con el aviso de que la MAC no cruza routers.",
            "caption": "Enchufate en cualquier puerto LAN, nunca en ether1; si la IP no responde, entrá por la MAC."},
    "steps": [
        {"file": "1-paso1.svg", "step": 1,
         "alt": "La notebook conectada con un cable a ether2 del router. Al lado, la ventana de WinBox con la pestaña Neighbors: la fila del equipo tiene la MAC resaltada y una flecha la lleva al campo Connect To, con usuario admin y la contraseña vacía o la de la etiqueta.",
         "caption": "Clic en la MAC dentro de Neighbors, usuario admin y Connect: no hace falta IP.",
         "after": "Conectá la notebook a ether2"},
        {"file": "1-paso2.svg", "step": 2,
         "alt": "Tres comandos con su resultado: las listas de interfaces (WAN es ether1, LAN es el bridge), las dos reglas defconf de drop del firewall y la dirección 192.168.88.1/24 en el bridge. Abajo, el router resumido con ether1 como WAN y ether2 a ether5 en el bridge.",
         "caption": "Tres comandos alcanzan para saber cómo viene el equipo de fábrica.",
         "after": "mirá qué trae de fábrica"},
        {"file": "1-paso4.svg", "step": 4,
         "alt": "Cuatro cajas en fila: Ctrl+X para entrar a Safe Mode con el prompt <SAFE>, agregar la regla prueba-safe, salir con Ctrl+D o perder la sesión, y el router deshace la regla. Debajo, Ctrl+X otra vez guarda los cambios, y un aviso de que Safe Mode recuerda hasta 100 acciones.",
         "caption": "Si la sesión muere en Safe Mode, el router vuelve solo a como estaba.",
         "after": "Probá Safe Mode: apretá"},
    ],
    "concepts": [
        {"name": "Entrar por MAC (MAC-WinBox)",
         "para_que": "Sirve para administrar un MikroTik aunque no tenga IP, tenga una IP de otra red o la configuración IP esté rota. WinBox habla con el equipo en capa 2, por su dirección física, así que no depende de ruteo ni de DHCP.",
         "como": "Conectás la notebook a un puerto LAN, abrís WinBox, vas a Neighbors y hacés clic en la MAC en vez de la IP. Solo funciona dentro del mismo segmento: si hay un router en el medio, la MAC no llega. En producción conviene dejarlo habilitado solo hacia la lista LAN (lección 3).",
         "ejemplo": "Llegás a un edificio en Pocitos donde otro instalador dejó el router con una IP fija de un rango que nadie anotó. Enchufás la notebook en ether2, lo ves en Neighbors, entrás por la MAC y en un minuto `/ip/address/print` te dice qué IP tiene."},
        {"name": "Configuración por defecto (defconf)",
         "para_que": "MikroTik la incluye para que un equipo salga de la caja funcionando y protegido: ether1 como WAN con cliente DHCP, el resto en un bridge con 192.168.88.1, servidor DHCP y un firewall que bloquea lo que entra por la WAN. Borrarla quita todas esas reglas de seguridad de un saque.",
         "como": "Para la mayoría de las obras conviene conservarla y agregar encima lo que haga falta, sin deshabilitar sus reglas. Sus reglas usan las listas WAN y LAN: si la WAN pasa a PPPoE, sumás esa interfaz a la lista WAN. Los CCR pueden venir sin configuración, y ahí bridge, IP, DHCP y firewall se arman a mano.",
         "ejemplo": "En un local de cobranzas en Ciudad Vieja ponés un hAP nuevo: dejás la defconf y agregás tus reglas arriba del drop. Si el proveedor después pasa a PPPoE, con `/interface/list/member/add list=WAN interface=pppoe-out1` el firewall sigue protegiendo igual."},
        {"name": "Export inicial: la foto de cómo estaba",
         "para_que": "Deja por escrito cómo estaba el equipo antes de que lo tocaras. Si algo deja de andar, comparás contra ese archivo y ves qué cambió, sin depender de la memoria de nadie.",
         "como": "Apenas entrás, antes del primer cambio: `/export file=inicial`. Queda un .rsc de texto en Files que bajás a la notebook y guardás en el legajo del cliente. El export común no incluye contraseñas de usuarios (la lección 6 lo profundiza).",
         "ejemplo": "Te toca un equipo heredado en una clínica de Cordón y el cliente dice que antes andaba la cámara de la puerta. Comparás el `inicial.rsc` del día que lo recibiste con un export de hoy y ves enseguida qué regla de NAT desapareció."},
    ],
    "teoria_md": """### Un poco de historia

MikroTik es una empresa de Riga, Letonia, que arrancó a mediados de los años 90 haciendo software de ruteo para PC y después sumó su propio hardware, los RouterBOARD. Su sistema, RouterOS, corre sobre un núcleo Linux, y la rama 7 salió estable en 2021: es la que usamos en todo el curso.

Desde temprano MikroTik resolvió un problema muy de campo: entrar a un equipo que todavía no tiene IP, o que tiene una que no conocés. Para eso creó WinBox, un programa de gestión propio, y una forma de hablar con el router por la dirección MAC. Junto con eso agregó un protocolo de descubrimiento de vecinos (MNDP), que hace que cada equipo se anuncie en la red local con su MAC, identidad y versión. RouterOS también entiende CDP y LLDP, los equivalentes de otras marcas.

La configuración por defecto (defconf) apareció para que un equipo hogareño o de oficina chica quede usable y razonablemente seguro apenas se enchufa. Los equipos pensados para operadores, como los CCR, pueden venir sin ella, porque se asume que el que los instala arma todo a mano.

### Cómo funciona

Cuando abrís WinBox, la pestaña Neighbors escucha esos anuncios de capa 2. Por eso ves el equipo aunque su IP sea `0.0.0.0` o de otra red: la notebook y el router comparten el mismo segmento Ethernet, y eso alcanza. Si hacés clic en la IP, WinBox abre una conexión TCP al puerto 8291, que necesita ruteo; si hacés clic en la MAC, viaja en tramas Ethernet directas. Esas tramas no cruzan routers: la MAC solo sirve en el mismo segmento.

La defconf de un equipo SOHO deja a `ether1` en la lista WAN con cliente DHCP, y al bridge (con `ether2` en adelante) en la lista LAN con `192.168.88.1/24` y un servidor DHCP. El firewall de fábrica tiene dos reglas clave: `drop all not coming from LAN` en input, que protege al router, y `drop all from WAN not DSTNATed` en forward, que protege a la LAN. Además limita el acceso por MAC a la lista LAN. Por eso, si te enchufás en `ether1`, no entrás ni por IP ni por MAC.

El `export` escribe la configuración como comandos de texto. Al hacerlo antes de tocar nada, tenés una foto del punto de partida que podés leer, guardar y comparar más adelante.
""",
}

# =====================================================================================  2
M["2"] = {
    "fig": {"file": "2.svg",
            "alt": "Tres usuarios a la izquierda: lucia.tecnico, mesa.ayuda limitado a 192.168.88.0/24 y admin tachado como deshabilitado. Al medio, los grupos: full puede todo; monitoreo tiene local, ssh, winbox, read y test, sin reboot ni write. A la derecha, el log muestra que lucia.tecnico entró por WinBox y agregó una regla.",
            "caption": "Cada técnico con su usuario y cada rol con su grupo: el log dice quién hizo qué."},
    "steps": [
        {"file": "2-paso2.svg", "step": 2,
         "alt": "Diagrama de decisión: entrás con lucia.tecnico en una sesión nueva; si entra, recién ahí /user/disable admin; si no entra, no toques admin. Al costado, /user/print muestra admin con la marca X de deshabilitado.",
         "caption": "Primero probás tu usuario, después deshabilitás admin; al revés te podés quedar afuera.",
         "after": "Cerrá WinBox y entrá con"},
        {"file": "2-paso3.svg", "step": 3,
         "alt": "El grupo monitoreo tiene las políticas local, ssh, winbox, read y test, y no tiene reboot, write ni policy. En la terminal de mesa.ayuda se escribe /system/reboot y el router lo rechaza.",
         "caption": "Sin la política reboot, el comando de reinicio no se ejecuta.",
         "after": "rechazarlo por falta de permisos"},
        {"file": "2-paso4.svg", "step": 4,
         "alt": "Dos filas. Si escribís password=\"Clave$Lab2026\", queda guardado solo Clave, más corta y sin aviso. Si escribís password=\"Clave\\$Lab2026\", queda la clave completa.",
         "caption": "Dentro de comillas, el $ arranca una variable: escribilo como \\$.",
         "after": "Probá el detalle del signo pesos"},
    ],
    "concepts": [
        {"name": "Un usuario por técnico",
         "para_que": "Sirve para saber quién hizo cada cambio y para dar de baja a una persona sin cambiarle la clave a todos. Con un admin compartido, el log dice siempre admin y, cuando alguien deja la empresa, hay que rotar la contraseña en cada equipo.",
         "como": "Creás un usuario por persona con contraseña de 12 caracteres o más, probás que entra en otra sesión y recién después deshabilitás admin. El log registra el nombre de usuario en cada ingreso y en cada cambio.",
         "ejemplo": "Un técnico deja de trabajar con vos. En cada router alcanza con `/user/disable juan.tecnico`: los demás siguen entrando con sus propias claves y nadie tiene que rehacer el gestor de contraseñas."},
        {"name": "Grupos y políticas",
         "para_que": "Los grupos definen qué puede hacer cada usuario: leer, escribir, reiniciar, entrar por SSH o por WinBox. Existen para dar a cada rol el permiso justo. El grupo read de fábrica puede reiniciar el router y ver configuración sensible, así que no sirve para alguien que solo mira.",
         "como": "Armás un grupo con las políticas que necesita el rol, por ejemplo `policy=local,ssh,winbox,read,test` para mesa de ayuda, y se lo asignás al usuario. Lo que no está en la lista, el router lo rechaza.",
         "ejemplo": "La mesa de ayuda que atiende un barrio privado entra con el grupo monitoreo: puede ver si el enlace del portón está caído, pero no puede reiniciar el router en plena hora de entrada de autos."},
        {"name": "Limitar la cuenta por origen (address)",
         "para_que": "Restringe desde qué direcciones puede entrar cada cuenta. Aunque alguien consiga la clave, si no está en la red permitida no entra.",
         "como": "Agregás `address=` al usuario con la red de gestión o la del túnel VPN, por ejemplo `address=192.168.88.0/24`. Es una segunda capa: el firewall (lección 4) corta antes, la restricción del usuario cubre si algo del firewall falla.",
         "ejemplo": "Un cliente quiere mirar su propio router: le creás una cuenta de monitoreo limitada a la IP de la PC de su oficina. Si esa clave termina en un papelito pegado al monitor, desde afuera de la LAN no sirve."},
        {"name": "El signo $ en las contraseñas",
         "para_que": "En la terminal de RouterOS, un $ dentro de comillas arranca el nombre de una variable. Si la variable no existe, se reemplaza por nada y la contraseña queda más corta, sin ningún aviso.",
         "como": "Cuando una clave lleve $, escribilo como `\\$`. Y siempre probá la clave nueva en otra sesión antes de cerrar la que tenés abierta.",
         "ejemplo": "Cargás la clave de un técnico como `password=\"Porton$2026\"` y queda guardada como Porton. Al otro día nadie entra con la clave anotada. Con `Porton\\$2026` queda completa."},
    ],
    "teoria_md": """### Un poco de historia

La idea de dar a cada persona solo los permisos que necesita es vieja en seguridad informática: Saltzer y Schroeder la describieron en 1975 como el principio de mínimo privilegio. Las cuentas compartidas tipo `admin` vienen de una época en que los equipos de red los tocaba una sola persona, y quedaron como costumbre aunque hoy un mismo router lo administran varios técnicos, una mesa de ayuda y a veces el propio cliente.

Con las contraseñas pasó algo parecido. Durante años se pidieron claves cortas con símbolos raros; las guías actuales, como la NIST SP 800-63B, ponen el peso en el largo. Por eso la documentación de MikroTik pide 12 caracteres o más. Y como una contraseña perdida en RouterOS no se recupera (hay que resetear o reinstalar), el orden de los pasos importa: primero probar el usuario nuevo, después deshabilitar `admin`.

### Cómo funciona

En RouterOS cada usuario pertenece a un grupo, y cada grupo es una lista de políticas. Algunas habilitan formas de entrar (`local` para consola, `ssh`, `winbox`, `web`, `api`) y otras habilitan acciones (`read` para ver, `write` para cambiar, `reboot` para reiniciar, `policy` para administrar usuarios, `test` para herramientas como ping y traceroute, `sensitive` para ver datos sensibles). Si una acción necesita una política que el grupo no tiene, el router la rechaza.

Vienen tres grupos de fábrica: `read`, `write` y `full`. El problema del `read` de fábrica es que incluye más de lo que su nombre sugiere, como reiniciar. Por eso conviene armar grupos propios con la lista exacta, como el grupo monitoreo del laboratorio.

La propiedad `address` del usuario agrega una condición más: el login solo se acepta si viene de esa red. Es independiente del firewall y se evalúa al momento de autenticar.

Cada ingreso y cada cambio quedan en el log con el nombre del usuario, algo como `user lucia.tecnico logged in from 192.168.88.10 via winbox`. Con cuentas personales, ese registro dice quién fue. Con `admin` compartido, no dice nada útil.

Por último, la terminal de RouterOS es un lenguaje de scripting: entre comillas, `$nombre` se reemplaza por el valor de una variable. Por eso el signo pesos de una contraseña se escribe `\\$`.
""",
}

# =====================================================================================  3
M["3"] = {
    "fig": {"file": "3.svg",
            "alt": "Router del cliente con su lista de servicios: winbox 8291 y ssh 22 solo desde LAN o VPN; telnet, ftp, www y api apagados. Desde internet, una flecha roja de escaneos termina con una cruz. Un técnico afuera entra por un túnel VPN con tilde verde, y una notebook en la LAN entra directo.",
            "caption": "Lo que no usás se apaga; lo que usás, solo desde la LAN o el túnel."},
    "steps": [
        {"file": "3-paso1.svg", "step": 1,
         "alt": "Tabla de servicios: telnet 23, ftp 21, www 80 y api 8728 quedan apagados, con el motivo de cada uno; winbox 8291 y ssh 22 quedan limitados a 192.168.88.0/24. Abajo, los dos comandos que lo hacen.",
         "caption": "Cuatro servicios afuera y dos limitados a la LAN, con dos comandos.",
         "after": "Mirá qué escucha el router"},
        {"file": "3-paso2.svg", "step": 2,
         "alt": "Router con allowed-interface-list=LAN. Del lado WAN, la red del proveedor tiene una cruz: no ve el router en Neighbors ni entra por MAC. Del lado LAN, la notebook tiene un tilde: lo ve y entra por MAC. Además quedan apagados bandwidth-server, socks, proxy y upnp.",
         "caption": "El acceso por MAC y el descubrimiento quedan solo para la LAN.",
         "after": "MAC server y descubrimiento"},
        {"file": "3-paso3.svg", "step": 3,
         "alt": "Tabla con cinco comandos de auditoría y, para cada uno, qué es normal y qué es sospechoso: scheduler con fetch, scripts que nadie conoce, SOCKS habilitado, un cliente L2TP desconocido como lvpn y una regla que acepta el puerto 5678.",
         "caption": "En un equipo heredado, buscá lo que dejó otro antes de confiar en él.",
         "after": "Auditoría de equipo heredado"},
    ],
    "concepts": [
        {"name": "Servicios IP del router",
         "para_que": "Cada servicio (WinBox, SSH, API, telnet, ftp, www) es una puerta para administrar el router. Existen para dar distintas formas de gestión, pero cada uno que escucha es algo más que se puede escanear y atacar.",
         "como": "Revisás `/ip/service/print`, apagás lo que no usás y a lo que queda le ponés `available-from` con la red de gestión. Ese filtro corta la conexión pero el puerto se sigue viendo: para esconderlo, drop en la cadena input (lección 4).",
         "ejemplo": "En un depósito con CCTV, el router quedó con telnet y www abiertos desde la instalación. Los apagás y dejás WinBox y SSH solo desde la LAN y la VPN: lo que queda escuchando es solo lo que vos usás."},
        {"name": "MAC server y descubrimiento de vecinos",
         "para_que": "Permiten encontrar y administrar el equipo en capa 2, sin IP. En la LAN te salvan (lección 1); hacia el proveedor no aportan nada y le muestran tu equipo, con nombre y versión, a quien esté del otro lado.",
         "como": "Se limitan con `allowed-interface-list=LAN` en mac-server y mac-winbox, y con `discover-interface-list=LAN` en neighbor discovery. Si el equipo no tiene la lista LAN (un CCR o un CHR), creala con el bridge adentro antes de aplicar esto.",
         "ejemplo": "En un shopping, el router de un local comparte el segmento del proveedor con otros locales. Con el descubrimiento abierto en la WAN, cualquier técnico del piso lo ve en su Neighbors. Limitado a LAN, deja de aparecer ahí."},
        {"name": "Auditoría de un equipo heredado",
         "para_que": "La botnet Mēris usó routers comprometidos años antes: los atacantes dejaron scheduler, scripts, SOCKS y túneles propios. MikroTik aclaró que actualizar no borra esa configuración: si la contraseña se filtró, el equipo sigue en manos ajenas.",
         "como": "En cada equipo que recibís revisás scheduler, scripts, SOCKS, clientes L2TP y reglas que aceptan el puerto 5678. Lo que nadie reconoce se anota en el legajo; si hay algo raro, contraseña nueva para todos los usuarios y revisión del firewall.",
         "ejemplo": "Tomás el mantenimiento de una cadena de farmacias. En una sucursal aparece un scheduler que hace fetch a una dirección desconocida y SOCKS habilitado. Lo documentás, lo deshabilitás, cambiás todas las claves y corrés los mismos comandos en las otras sucursales."},
    ],
    "teoria_md": """### Un poco de historia

Telnet (RFC 854, de 1983) y FTP (RFC 959, de 1985) nacieron en una internet chica, donde los equipos se conocían entre sí. Mandan usuario y contraseña en texto plano: cualquiera que vea el tráfico los lee. SSH apareció en 1995 justamente para reemplazar a telnet con una conexión cifrada. RouterOS todavía trae los dos viejos por compatibilidad, y por eso la guía de seguridad pide apagarlos.

En 2018 se publicó una falla del servicio WinBox (CVE-2018-14847) que, en versiones 6.42 y anteriores, permitía leer credenciales sin autenticarse. MikroTik la corrigió rápido, pero muchos equipos siguieron expuestos y sin actualizar. En 2021 apareció Mēris, una botnet hecha en su mayoría con MikroTik, que llegó a 21,8 millones de pedidos por segundo contra Yandex. MikroTik explicó que no había una falla nueva: eran routers tomados en 2018, actualizados después, pero con la configuración del atacante todavía adentro y la contraseña filtrada sin cambiar.

### Cómo funciona

Cada servicio de `/ip/service` es un programa escuchando en un puerto TCP: WinBox en 8291, SSH en 22, telnet en 23, FTP en 21, la web (WebFig) en 80, la API en 8728. Los escáneres automáticos recorren internet probando esos puertos todo el tiempo. Un honeypot con una versión vieja de RouterOS expuesta fue tomado en 15 minutos, aunque tenía usuario y contraseña fuertes: entraron por la falla, no por la clave.

`available-from` hace que el router rechace conexiones de otras direcciones, pero el puerto responde igual y se ve abierto en un escaneo. Un `drop` en la cadena input, en cambio, descarta el paquete antes de que llegue al servicio. Por eso MikroTik prefiere el firewall y deja `available-from` como capa extra.

El acceso por MAC y el descubrimiento de vecinos funcionan en capa 2: llegan a todos los equipos del mismo segmento Ethernet. Hacia la LAN es una ayuda; hacia el proveedor es información regalada. Con `allowed-interface-list=LAN` quedan del lado de adentro.

Lo que dejó Mēris en los equipos eran funciones normales de RouterOS: tareas del scheduler que bajaban scripts con `fetch`, un proxy SOCKS, un cliente L2TP propio y una regla que abría el puerto 5678. Por eso la auditoría busca exactamente eso.
""",
}

# =====================================================================================  4
M["4"] = {
    "fig": {"file": "4.svg",
            "alt": "Internet a la izquierda y la LAN con NVR y PCs a la derecha. Una flecha input va desde internet a los servicios del propio router (WinBox, SSH, DNS, API). Otra flecha forward atraviesa el router hacia la LAN. Abajo, tres reglas en orden: accept para admins al 8291, accept established y related, y drop de lo que no viene de la LAN.",
            "caption": "input es lo que va al router; forward, lo que pasa a través. Y se lee de arriba abajo."},
    "steps": [
        {"file": "4-paso1.svg", "step": 1,
         "alt": "Dos columnas con reglas defconf. En chain=input, que protege al router, la última es drop all not coming from LAN. En chain=forward, que protege a la LAN, la última es drop all from WAN not DSTNATed. Ambas resaltadas en rojo.",
         "caption": "Cada cadena termina con su drop: buscalo antes de agregar nada.",
         "after": "ubicá la regla que protege al router"},
        {"file": "4-paso2.svg", "step": 2,
         "alt": "La address-list admins con dos entradas, 192.168.88.10 notebook lab y 203.0.113.25 oficina ejemplo, apunta a una regla de input que acepta TCP 8291 con src-address-list=admins. Debajo: si cambia la IP de la oficina se edita la lista, y las interface lists hacen lo mismo con las interfaces.",
         "caption": "La regla nombra la lista; cuando cambia una IP, tocás la lista y no la regla.",
         "after": "Creá la lista de administradores"},
        {"file": "4-paso3.svg", "step": 3,
         "alt": "Dos listas de reglas. Con place-before, el accept del 8291 para admins queda arriba del drop y su contador sube. Sin place-before, queda debajo del drop: el drop corta la conexión de 203.0.113.25 y el accept queda con contador en 0. Abajo, el comando con place-before.",
         "caption": "Manda la primera regla que coincide: lo permitido va arriba del drop.",
         "after": "Agregá la regla arriba del drop"},
    ],
    "concepts": [
        {"name": "Cadena input y cadena forward",
         "para_que": "RouterOS separa el tráfico según su destino. input es lo que va al propio router (WinBox, DNS, un ping a cualquiera de sus IP, también la de la LAN); forward es lo que el router deja pasar de una red a otra. Así podés proteger el equipo sin afectar a la red, y al revés.",
         "como": "Antes de escribir una regla, preguntate si el destino es el router o algo detrás de él. WinBox, la VPN y los servicios del router van en input; el acceso a un NVR o el tráfico entre VLAN va en forward. El firewall de fábrica tiene un drop al final de cada cadena.",
         "ejemplo": "Para que la central de monitoreo llegue al NVR, el filtro va en forward (y el dst-nat en NAT). Para que vos entres por WinBox desde la oficina, la regla va en input. Si la ponés en la cadena equivocada, no coincide nunca."},
        {"name": "Orden de reglas y place-before",
         "para_que": "El firewall lee las reglas de arriba abajo y la primera que coincide decide. Eso lo hace rápido y predecible, pero una regla que quedó debajo de un drop nunca llega a evaluarse.",
         "como": "Agregá lo permitido con `place-before` apuntando al drop por su comentario, y mirá el contador con `print stats`: si no sube cuando probás, la regla está en la cadena o en el lugar equivocado. Los cambios en input, en Safe Mode.",
         "ejemplo": "Un técnico agrega un accept al 8291 para la oficina y no anda. Con `/ip/firewall/filter/print stats` ve que la regla quedó última, con contador en 0, debajo de `drop all not coming from LAN`. La sube y entra."},
        {"name": "Address-lists e interface lists",
         "para_que": "Agrupan direcciones (address-list) o interfaces (interface list) bajo un nombre. Las reglas apuntan al nombre, así que cuando cambia una IP o un puerto se edita la lista y la regla queda igual.",
         "como": "Creás la lista con `/ip/firewall/address-list/add list=admins address=...` y un comentario que diga quién es, y la usás con `src-address-list=admins`. La defconf ya trae las interface lists WAN y LAN, y sus reglas las usan.",
         "ejemplo": "La oficina de IES cambia de proveedor y su IP pública cambia. En vez de reescribir reglas en cada cliente, actualizás la entrada de la lista admins en cada router, sin mover ninguna regla de lugar."},
    ],
    "teoria_md": """### Un poco de historia

RouterOS corre sobre Linux, y su firewall hereda la lógica de netfilter, el sistema de filtrado del núcleo Linux que se popularizó con iptables a partir de Linux 2.4, en 2001. De ahí vienen los nombres de las cadenas: `input` para lo que va al propio equipo, `forward` para lo que lo atraviesa y `output` para lo que el equipo genera. También viene de ahí el seguimiento de conexiones (connection tracking), que le permite al firewall saber si un paquete abre una conexión nueva o pertenece a una que ya existe.

En el foro de MikroTik conviven dos escuelas. Una deja el firewall de fábrica, que está bien pensado, y le abre agujeros puntuales. La otra lo reescribe con un drop final explícito y agrega antes solo lo permitido. Las dos comparten lo mismo: el orden de las reglas es lo que define el resultado.

### Cómo funciona

Cuando llega un paquete, el router decide primero a dónde va. Si la dirección de destino es una de las suyas, cualquiera, incluida `192.168.88.1` de la LAN, el paquete entra en la cadena `input`. Si va hacia otra red, pasa por `forward`. Por eso una regla para WinBox en forward no coincide nunca: WinBox apunta al router.

Dentro de cada cadena, las reglas se evalúan en orden. La primera cuya condición coincide ejecuta su acción (`accept`, `drop`) y ahí termina el recorrido. El firewall de fábrica pone arriba `accept established,related,untracked`, para que las conexiones ya aceptadas no se vuelvan a evaluar entera, y abajo de todo el drop. Una regla agregada sin `place-before` queda al final, debajo del drop, y su contador se queda en cero.

Los contadores son la herramienta de diagnóstico más simple: `print stats` muestra cuántos paquetes y bytes coincidieron con cada regla. Si probás y el contador no sube, la regla no está viendo ese tráfico.

Las address-lists son conjuntos de direcciones con nombre. Una regla con `src-address-list=admins` coincide con cualquier IP de la lista, y la lista se puede cambiar sin tocar la regla. Las interface lists hacen lo mismo con interfaces: la defconf usa `WAN` y `LAN`, y por eso, si la WAN pasa a PPPoE, alcanza con sumar `pppoe-out1` a la lista para que todas las reglas la cubran.
""",
}

# =====================================================================================  5
M["5"] = {
    "fig": {"file": "5.svg",
            "alt": "Un MikroTik con un solo bridge y vlan-filtering=yes baja con un trunk de cuatro VLAN etiquetadas (10, 20, 30 y 99) a un switch de piso. Del switch salen puertos access a las cámaras y el NVR en VLAN 20 CCTV, a la controladora de acceso en VLAN 30 y a las PCs en VLAN 10 datos. Notas: la cámara infectada no ve las PCs y la gestión va por la VLAN 99, nunca por la 1.",
            "caption": "Cada sistema en su VLAN: para cruzar de una a otra hay que pasar por el router."},
    "steps": [
        {"file": "5-paso1.svg", "step": 1,
         "alt": "El router con ether2, ether3 y ether4 dentro de un recuadro punteado que marca el bridge, y ether5 en verde fuera del bridge con 10.255.255.1/30. Una notebook con 10.255.255.2/30 conectada a ether5.",
         "caption": "ether5 queda fuera del bridge: si algo sale mal con las VLAN, seguís adentro por ahí.",
         "after": "Puerto de rescate con IP propia"},
        {"file": "5-paso2.svg", "step": 2,
         "alt": "Tabla con columnas bridge, ether2, ether3 y ether4. VLAN 20: bridge con etiqueta, ether2 y ether3 sin etiqueta, ether4 con etiqueta. VLAN 99: bridge y ether4 con etiqueta, ether2 y ether3 no pasa. Debajo, la configuración de los puertos access (pvid=20) y del trunk ether4.",
         "caption": "El bridge también es un puerto: si no lleva la VLAN etiquetada, el router no la ve.",
         "after": "Puertos, PVID y tabla VLAN"},
        {"file": "5-paso4.svg", "step": 4,
         "alt": "Tres tarjetas con tilde: rescate, puertos y tabla, capa 3. Una flecha lleva a la tarjeta final vlan-filtering=yes desde ether5. Debajo, el comando para revisar la tabla y el que activa el filtrado.",
         "caption": "Revisás la tabla y recién ahí activás el filtrado, conectado por ether5.",
         "after": "Revisá la tabla antes de activar"},
    ],
    "concepts": [
        {"name": "Un bridge con vlan-filtering",
         "para_que": "Las VLAN separan sistemas que comparten cables y switches, como si fueran redes físicas distintas. En RouterOS 7 se arma con un solo bridge que tiene una tabla de VLAN: cada puerto sabe qué VLAN lleva y cómo.",
         "como": "Cargás los puertos con su PVID, la tabla `/interface/bridge/vlan` con una entrada por VLAN, las interfaces vlan para la capa 3 y, al final, `vlan-filtering=yes`. Para que dos VLAN se hablen, el tráfico pasa por el router, y ahí lo filtra la cadena forward.",
         "ejemplo": "En un edificio con CCTV, control de acceso y la red de la administración, ponés cámaras y NVR en la VLAN 20, controladoras en la 30 y PCs en la 10. Si una cámara barata queda infectada, no ve las PCs, y el NVR que satura no se lleva puesta la red de oficina."},
        {"name": "Puertos access y trunk",
         "para_que": "Un puerto access conecta un equipo que no sabe nada de VLAN (una cámara, una PC): entra sin etiqueta y el switch le asigna la VLAN de su PVID. Un trunk une switches y lleva varias VLAN a la vez, cada trama con su etiqueta.",
         "como": "En access: `pvid=20 frame-types=admit-only-untagged-and-priority-tagged ingress-filtering=yes`. En trunk: `frame-types=admit-only-vlan-tagged ingress-filtering=yes`. Sin ingress-filtering, frame-types no tiene efecto.",
         "ejemplo": "En el rack del piso 3, la boca que baja a la cámara del palier es access en VLAN 20 y la que sube al rack principal es trunk con 10, 20, 30 y 99. Si alguien enchufa una notebook en la boca de la cámara, cae en la VLAN 20 y no ve la red de oficina."},
        {"name": "VLAN de gestión y puerto de rescate",
         "para_que": "El router es un puerto más del bridge (el puerto del CPU). La gestión va en una VLAN propia, por ejemplo 99, y no en la VLAN 1 sin etiqueta, para que no cualquier boca llegue al router. Y como un error en la tabla te puede dejar afuera, conviene un puerto fuera del bridge para rescate.",
         "como": "En la tabla, la VLAN de gestión va con `tagged=bridge,ether4` y la IP del router en la interfaz vlan99. Antes de activar `vlan-filtering`, conectate por el puerto de rescate (ether5 con 10.255.255.1/30) o por consola serial.",
         "ejemplo": "Configurás un switch en un edificio de Malvín por la misma boca que estás cambiando, activás el filtrado y quedás afuera: hay que subir al rack con escalera. Con ether5 de rescate, corregís la tabla desde ahí sin moverte."},
    ],
    "teoria_md": """### Un poco de historia

Las VLAN se estandarizaron con IEEE 802.1Q en 1998. Antes, separar redes quería decir separar cables y switches: un switch para las cámaras, otro para las PCs. 802.1Q permitió que un mismo cable lleve varias redes lógicas, marcando cada trama con un número de VLAN.

En RouterOS las VLAN se configuraron durante años de varias maneras, según el equipo: en el menú del chip de switch, con puertos maestros o con interfaces vlan sueltas. Con RouterOS 6.41 desapareció el puerto maestro y el bridge pasó a ser el lugar central para armar switching, con su tabla de VLAN y descarga al hardware cuando el chip lo permite. Así sigue en RouterOS 7. La guía del foro de MikroTik para integradores y la documentación de Bridge VLAN Table describen este modelo.

### Cómo funciona

Una trama con etiqueta 802.1Q lleva 4 bytes extra con un identificador de VLAN de 12 bits: hay 4094 VLAN posibles (la 0 y la 4095 están reservadas). Un equipo final, como una cámara, manda tramas sin etiqueta. El puerto access del switch la recibe y le asigna su PVID, por ejemplo 20; cuando sale por un trunk, viaja etiquetada con 20; cuando llega a otro puerto access de la VLAN 20, sale de nuevo sin etiqueta.

La tabla `/interface/bridge/vlan` dice, para cada VLAN, qué puertos la llevan con etiqueta (`tagged`) y cuáles sin etiqueta (`untagged`). El bridge mismo figura como un puerto: es la puerta hacia el CPU del router. Si `bridge` no está como tagged en la VLAN 20, la interfaz `vlan20-cctv` no recibe nada y el router no ve esa red.

`frame-types` dice qué tramas acepta cada puerto, y `ingress-filtering=yes` hace que se cumpla: en access se descarta lo que llega etiquetado, en trunk lo que llega sin etiqueta. Sin esas dos cosas, una tabla bien hecha igual deja pasar tramas que no debería.

Mientras `vlan-filtering=no`, el bridge ignora la tabla y todo pasa como en un switch común. Al ponerlo en `yes`, la tabla empieza a mandar de golpe. Si la gestión todavía no está en su VLAN, la boca por la que estás conectado deja de llegar al router. Por eso se activa al final y desde un puerto fuera del bridge.
""",
}

# =====================================================================================  6
M["6"] = {
    "fig": {"file": "6.svg",
            "alt": "Dos tarjetas. .backup binario, con /system/backup/save: clona el equipo completo con usuarios, no se lee ni se compara y en otro modelo puede traer problemas; sirve para volver atrás en el mismo equipo. export texto .rsc, con /export file=antes: se lee y se compara con diff, no lleva contraseñas de usuarios ni certificados y con show-sensitive suma claves; sirve para leer, comparar y migrar.",
            "caption": "El .backup restaura el mismo equipo; el export se lee, se compara y se migra."},
    "steps": [
        {"file": "6-paso3.svg", "step": 3,
         "alt": "Los archivos antes.rsc y despues.rsc uno al lado del otro; en el de después aparecen dos líneas nuevas en verde, /system identity y set name=LAB-MT01. A la derecha, la salida de diff con la línea de fecha en ámbar y las dos líneas nuevas marcadas con el signo mayor.",
         "caption": "Lo verde es tu cambio; la línea de fecha siempre cambia y no cuenta.",
         "after": "WinBox, Files, arrastrar"},
        {"file": "6-paso5.svg", "step": 5,
         "alt": "Los archivos antes-sensible.rsc y antes.backup van con una flecha a un lugar con acceso restringido, en verde. Una tarjeta roja dice nunca en un chat ni en un mail sin cifrar. El archivo antes.rsc, sin secretos, va al legajo del cliente.",
         "caption": "Lo que tiene claves va bajo llave; el export común va al legajo.",
         "after": "en un lugar con acceso restringido"},
    ],
    "concepts": [
        {"name": ".backup binario",
         "para_que": "Clona la configuración completa del equipo, usuarios incluidos, en un archivo binario. Está pensado para volver atrás en el mismo equipo, rápido y sin revisar línea por línea.",
         "como": "`/system/backup/save name=antes password=...` y se restaura en el mismo router. No se lee ni se compara. En otro modelo puede traer problemas de interfaces y de MAC: para pasar a otro equipo se usa el export.",
         "ejemplo": "Antes de reconfigurar el failover de un supermercado, guardás un .backup con contraseña. Si a las 20 h algo no cierra y el local tiene que seguir cobrando, restaurás y volvés al estado anterior en minutos."},
        {"name": "Export de texto (.rsc)",
         "para_que": "Escribe la configuración como comandos de texto. Sirve para leerla, compararla con diff, guardarla en el legajo y llevarla a otro equipo con un import revisado.",
         "como": "`/export file=antes` antes de tocar y `/export file=despues` al terminar. No incluye contraseñas de usuarios ni certificados. Para probar un import sin aplicarlo: `/import file-name=despues.rsc verbose=yes dry-run`.",
         "ejemplo": "Cambiás el router de un estudio contable por un modelo más nuevo: exportás el viejo, adaptás los nombres de interfaces que cambian, probás con dry-run en el equipo nuevo y recién ahí importás."},
        {"name": "show-sensitive y archivos sensibles",
         "para_que": "Por defecto el export oculta las claves (WiFi, PPPoE, VPN). show-sensitive las incluye, para que el archivo sirva también como respaldo de esas credenciales.",
         "como": "`/export show-sensitive file=antes-sensible`. Ese archivo, igual que el .backup, se guarda en un lugar con acceso restringido: carpeta con permisos, gestor de claves o almacenamiento cifrado. Nunca por chat ni por mail sin cifrar.",
         "ejemplo": "El cliente pierde el usuario PPPoE que le dio el proveedor. Si tenés el export con show-sensitive en la carpeta restringida del cliente, lo recuperás sin esperar al proveedor. Si lo hubieras mandado por un chat, esa clave ya no sería solo tuya."},
    ],
    "teoria_md": """### Un poco de historia

Guardar configuraciones como texto y compararlas es una práctica que viene de Unix: la herramienta `diff`, que muestra las diferencias entre dos archivos, existe desde los años 70 y es la base de los sistemas de control de versiones que se usan hoy. Muchos administradores de red aplican la misma idea a sus equipos: si la configuración es texto, se puede leer, comparar y guardar con historia. Un practicante citado en el curso guarda los exports de sus MikroTik en git y así quedó registrado, sin que hiciera nada, el día que el proveedor le cambió las credenciales PPPoE.

RouterOS ofrece desde hace mucho dos formatos. El backup de sistema es la copia exacta para restaurar; el export es un script de comandos. En RouterOS 7 el export oculta los datos sensibles por defecto, y hay que pedirlos explícitamente con `show-sensitive`.

### Cómo funciona

El archivo `.backup` es binario y guarda el estado completo del equipo, usuarios y contraseñas incluidos. Al restaurarlo, el router queda igual que cuando se guardó. Como incluye referencias al hardware (interfaces, direcciones MAC), en otro modelo puede no encajar. Con `password=` se guarda cifrado.

El export recorre la configuración y la escribe como los mismos comandos que escribirías en la terminal, agrupados por menú: `/interface bridge`, `/ip address`, `/system identity`. Por defecto escribe solo lo que cambiaste respecto de los valores de fábrica, por eso es corto. La primera línea trae la fecha y la versión, y por eso esa línea aparece siempre en un diff. Las contraseñas de usuarios, los certificados y las claves SSH no se exportan nunca; las claves de WiFi, PPPoE y VPN, solo con `show-sensitive`.

Al importar, el router ejecuta el archivo línea por línea. Si una línea falla (una interfaz que no existe en el equipo nuevo, por ejemplo), `verbose=yes` muestra dónde, y `dry-run` permite ver los errores sin aplicar nada. La documentación recomienda importar en la misma versión de RouterOS.

`diff antes.rsc despues.rsc` marca con `<` lo que estaba solo en el primero y con `>` lo que está solo en el segundo. Con un export antes y otro después de cada intervención, cualquier pregunta de quién cambió esto se contesta mirando el legajo.
""",
}

# =====================================================================================  7
M["7"] = {
    "fig": {"file": "7.svg",
            "alt": "Cinco pasos en fila: backup con export y .backup, RouterOS con update/install, RouterBOOT con routerboard/upgrade resaltado como el paso que más se olvida, reinicio con /system/reboot y verificar que current sea igual a upgrade. Debajo, los canales long-term y stable en verde y testing y development en rojo, y avisos sobre RouterOS 6, HTTPS y no cortar la energía.",
            "caption": "RouterOS y RouterBOOT se actualizan juntos, con backup antes y un canal de producción."},
    "steps": [
        {"file": "7-paso3.svg", "step": 3,
         "alt": "Cuatro canales: long-term y stable marcados para producción con tilde verde; testing y development marcados como no en clientes con cruz roja, cada uno con su descripción. A la derecha, los comandos para elegir canal, buscar e instalar.",
         "caption": "En un cliente, long-term o stable; los otros dos quedan para el laboratorio.",
         "after": "Elegí canal y actualizá"},
        {"file": "7-paso4.svg", "step": 4,
         "alt": "Tabla de tres momentos. Antes de empezar, RouterOS, current-firmware y upgrade-firmware son la versión vieja. Después de install, RouterOS y upgrade-firmware son nuevas pero current-firmware sigue vieja: falta RouterBOOT. Después de upgrade y reboot, todo es nuevo. Debajo, los comandos y cómo leer los dos campos.",
         "caption": "Si current-firmware y upgrade-firmware no coinciden, falta actualizar el bootloader.",
         "after": "actualizá el bootloader y reiniciá"},
    ],
    "concepts": [
        {"name": "Canales de actualización",
         "para_que": "MikroTik publica RouterOS en cuatro canales según madurez: long-term (pocas veces, solo arreglos críticos), stable (cada pocos meses), testing y development. Existen para que cada uno elija entre estabilidad y novedades.",
         "como": "En equipos de clientes, long-term o stable; testing y development, solo en laboratorio. Se elige con `/system/package/update/set channel=...` antes de buscar. Desde 7.23 la búsqueda usa HTTPS: el router necesita salir por TCP 443.",
         "ejemplo": "Podés dejar long-term en los sitios que no se pueden caer, como una central de monitoreo, stable en el resto, y probar cada versión nueva primero en el MikroTik del laboratorio."},
        {"name": "RouterOS y RouterBOOT",
         "para_que": "RouterOS es el sistema; RouterBOOT es el cargador que arranca la placa, parecido al BIOS de una PC. Cada versión de RouterOS trae su RouterBOOT, pero no lo instala sola: queda pendiente hasta que lo pedís.",
         "como": "Cuando RouterOS reinicia con la versión nueva, `/system/routerboard/upgrade` y otro `/system/reboot`. Verificás que `current-firmware` coincida con `upgrade-firmware`. Solo se actualiza el RouterBOOT principal: el de respaldo queda para recuperar el equipo.",
         "ejemplo": "En un mantenimiento actualizás RouterOS y te vas. Meses después, `/system/routerboard/print` muestra current-firmware viejo: faltó el segundo reinicio. Desde entonces anotás en el legajo versión de RouterOS, de RouterBOOT, canal y fecha."},
        {"name": "Saltos de versión y plan de rescate",
         "para_que": "Desde RouterOS 6 no se salta directo a la última v7: primero se pasa por 7.12.1, y recién después aparecen las nuevas en el canal. Y una actualización cortada por falta de energía puede dejar el equipo sin arrancar.",
         "como": "Antes de actualizar, export y .backup. En sitios remotos, alguien en el lugar o un plan de rescate con Netinstall, que reinstala RouterOS por red y se activa con el botón de reset. Nunca cortes la energía en el medio.",
         "ejemplo": "Un router con RouterOS 6 en un establecimiento de Durazno: lo pasás a 7.12.1, verificás que arranca y recién después vas a la versión del canal elegido, con el encargado cerca del equipo durante la ventana."},
    ],
    "teoria_md": """### Un poco de historia

RouterOS tuvo varias generaciones; la 6 fue la que se usó durante la mayor parte de la década pasada y la 7 salió estable en 2021, con un núcleo Linux nuevo y funciones como WireGuard. En la rama 6 los canales se llamaban de otra forma (solo arreglos, actual y candidata); hoy son long-term, stable, testing y development. Un distribuidor de 2018 ya recomendaba la rama de solo arreglos para producción, y esa idea sigue vigente.

El motivo para actualizar está documentado. Según Eclypsium, más de 2 millones de MikroTik tenían alguna interfaz de gestión expuesta y unos 300.000 seguían vulnerables a fallas que ya tenían parche. El problema no es que el fabricante no corrija: es que los routers se actualizan mucho menos que una PC.

### Cómo funciona

RouterOS se distribuye en paquetes `.npk`. Al ejecutar `/system/package/update/install`, el router descarga los paquetes del canal elegido, reinicia y los instala al arrancar. Desde la versión 7.23 la consulta de versiones va por HTTPS, así que si el firewall o el proveedor bloquean la salida al puerto 443, el router no encuentra actualizaciones. Si el equipo viene de la rama 6, el canal solo le ofrece 7.12.1 como paso intermedio.

RouterBOOT es el programa que arranca la placa antes que RouterOS. Cada versión de RouterOS trae una versión de RouterBOOT, pero la instalación no la aplica. `/system/routerboard/print` muestra dos campos: `current-firmware`, el que corre hoy, y `upgrade-firmware`, el que trae el RouterOS instalado. Si no coinciden, `/system/routerboard/upgrade` lo graba y el siguiente reinicio lo activa.

La placa guarda además un RouterBOOT de respaldo que nunca se actualiza. Si mantenés apretado el botón de reset al dar energía, el equipo arranca con ese respaldo. Siguiendo con el botón apretado, el mismo botón resetea la configuración (unos 5 segundos), activa modo CAP o busca un servidor Netinstall. Netinstall reinstala RouterOS por red desde una PC conectada por cable, y es la salida cuando el sistema no arranca o se perdió la contraseña.

Por todo esto, la secuencia es siempre la misma: backup, RouterOS, reinicio, RouterBOOT, reinicio y verificación en el log.
""",
}

# =====================================================================================  8
M["8"] = {
    "fig": {"file": "8.svg",
            "alt": "La notebook del técnico, con 10.10.10.2, llega al router del cliente por un túnel WireGuard sobre UDP 13231 que cruza internet, y por adentro del túnel entra por WinBox a 10.10.10.1. En el router, la cadena input acepta UDP 13231 y el 8291 por wg-gestion, arriba del drop. Un escáner que intenta WinBox desde internet termina en el drop.",
            "caption": "Lo único abierto es el puerto del túnel; WinBox se alcanza solo desde adentro."},
    "steps": [
        {"file": "8-paso2.svg", "step": 2,
         "alt": "Router y notebook, cada uno con su clave privada, que no sale nunca de ese equipo, y su clave pública, que se copia a la otra punta. Una flecha lleva la pública del router al [Peer] de la notebook y otra lleva la de la notebook al peer del router con su /32. Debajo, el comando del peer.",
         "caption": "Las públicas se intercambian; las privadas no se mueven nunca.",
         "after": "creá un túnel vacío"},
        {"file": "8-paso4.svg", "step": 4,
         "alt": "Dos casos. Con AllowedIPs 10.10.10.0/24, solo el tráfico a 10.10.10.x va por el túnel y el mail y la web salen por tu internet. Con AllowedIPs 0.0.0.0/0, todo tu tráfico va por el túnel y sale por la conexión del cliente. Abajo, una nota sobre PersistentKeepalive 25.",
         "caption": "Para gestión, por el túnel va solo la red 10.10.10.0/24.",
         "after": "solo la red de gestión va por el túnel"},
    ],
    "concepts": [
        {"name": "WireGuard para gestión",
         "para_que": "Es una VPN moderna y liviana que RouterOS 7 trae de serie. Sirve para entrar a un cliente sin dejar WinBox ni SSH mirando a internet: lo único expuesto es un puerto UDP que solo atiende a quien tenga una clave cargada.",
         "como": "Creás la interfaz con `listen-port=13231`, le das una IP de gestión, cargás un peer por técnico con su clave pública y `allowed-address` /32, y aceptás ese UDP en input arriba del drop. WinBox se permite solo por la interfaz del túnel.",
         "ejemplo": "Un cliente de Carrasco llama porque su NVR no graba una cámara. Activás el túnel desde la notebook, entrás por WinBox a 10.10.10.1 y revisás el router, sin haber abierto ningún puerto de gestión en su conexión."},
        {"name": "Claves y un peer por técnico",
         "para_que": "WireGuard usa un par de claves en cada punta: la privada no sale del equipo y la pública se le da a la otra punta. Así cada técnico tiene su propia credencial y no hay una contraseña compartida.",
         "como": "Copiás la clave pública del router al [Peer] de la app, y la de la notebook al peer del router, cada uno con su /32. Para dar de baja a alguien, borrás su peer.",
         "ejemplo": "Se suma una técnica nueva: genera su túnel en la app, te pasa la clave pública y le creás el peer `notebook-sofia` con 10.10.10.3/32. Si un día pierde la notebook, borrás ese peer y los demás no se enteran."},
        {"name": "AllowedIPs y keepalive",
         "para_que": "AllowedIPs le dice a la notebook qué destinos van por el túnel. PersistentKeepalive manda un paquete cada tantos segundos para que el NAT del medio no cierre el camino cuando no hay tráfico.",
         "como": "Para gestión, `AllowedIPs = 10.10.10.0/24`: solo la red del túnel va por ahí y el resto sale por tu conexión. `PersistentKeepalive = 25` cuando hay NAT en el medio. Con 0.0.0.0/0 mandarías todo tu tráfico por el cliente.",
         "ejemplo": "Estás en un hotel del interior, con wifi detrás de NAT. Sin keepalive el túnel se queda mudo a los minutos; con 25 segundos se mantiene. Y tus videollamadas no pasan por la fibra del cliente."},
        {"name": "L2TP/IPsec cuando hace falta, PPTP nunca",
         "para_que": "L2TP/IPsec existe en el curso porque Windows, macOS, iOS y Android lo traen de fábrica, sin instalar nada. PPTP es viejo y tiene fallas conocidas.",
         "como": "Primera opción, WireGuard. L2TP/IPsec cuando del otro lado solo se puede usar el cliente nativo del sistema, con `use-ipsec=required` y un secreto largo. PPTP, nunca.",
         "ejemplo": "La administradora de un consorcio necesita entrar desde una PC donde no le permiten instalar programas: le armás L2TP/IPsec con el cliente de Windows. Para vos y los técnicos, WireGuard."},
    ],
    "teoria_md": """### Un poco de historia

Durante años, las VPN más comunes fueron PPTP, que Microsoft impulsó a fines de los 90 y que hoy se considera insegura, y L2TP combinado con IPsec, que viene incluido en casi todos los sistemas operativos pero es complejo de configurar y de diagnosticar. OpenVPN ocupó el espacio intermedio con software aparte.

WireGuard lo creó Jason A. Donenfeld con la idea opuesta: poco código, criptografía moderna fija y casi nada para configurar. Entró al núcleo Linux en la versión 5.6, en 2020, y MikroTik lo incorporó en RouterOS 7. La guía de seguridad de MikroTik lo nombra como la opción para acceso remoto, en lugar de exponer WinBox o SSH.

### Cómo funciona

Cada punta tiene un par de claves. La privada se genera en el equipo y no sale de ahí; la pública se copia a la otra punta. No hay usuarios ni contraseñas: un paquete que no está cifrado con una clave conocida se descarta sin respuesta, así que un escáner no ve nada del otro lado del puerto UDP.

La pieza central es lo que WireGuard llama ruteo por clave. En el router, cada peer tiene un `allowed-address`: el router solo acepta paquetes de ese peer si vienen con esa IP de origen, y manda por ese peer lo que va hacia esa IP. Con un /32 por técnico, cada uno queda atado a su dirección. En la notebook, `AllowedIPs` cumple el mismo papel al revés: define qué destinos se mandan por el túnel. Con `10.10.10.0/24`, solo la gestión; con `0.0.0.0/0`, todo.

WireGuard no mantiene una conexión abierta: si no hay tráfico, no manda nada. El problema es el NAT del medio (tu módem, un 4G), que olvida la asociación a los pocos minutos y deja de dejar pasar paquetes desde afuera. `PersistentKeepalive = 25` manda un paquete chico cada 25 segundos para mantenerla.

En RouterOS, la interfaz usa por defecto el puerto UDP 13231 y una MTU de 1420. El firewall de fábrica descarta en input todo lo que no viene de la LAN, incluido el túnel. Por eso hacen falta dos reglas arriba del drop: una para el UDP del túnel y otra para WinBox entrando por `wg-gestion`. Desde 7.21, el router puede generar la configuración del cliente, con código QR, para cargarla en la app.
""",
}

# =====================================================================================  9
M["9"] = {
    "fig": {"file": "9.svg",
            "alt": "Un técnico afuera consulta el nombre de IP Cloud, <serie>.sn.mynetname.net, que apunta a 203.0.113.10 y la sigue si cambia. Cuando intenta conectarse al router del cliente, una flecha roja choca contra el firewall de fábrica, que descarta lo que llega de internet. Debajo, los dos caminos para entrar: un túnel o Back To Home.",
            "caption": "El nombre de IP Cloud te dice dónde está el router; no abre ningún acceso."},
    "steps": [
        {"file": "9-paso1.svg", "step": 1,
         "alt": "La salida de /ip/cloud/print con ddns-enabled yes, dns-name <serie>.sn.mynetname.net, public-address 203.0.113.10 resaltada y status updated, con una nota que explica cada campo y el aviso de que el nombre no abre nada.",
         "caption": "public-address es el dato que vas a comparar con la IP de la WAN.",
         "after": "Activá el DDNS y leé el estado"},
        {"file": "9-paso3.svg", "step": 3,
         "alt": "Tres casos. IP pública directa: la WAN del MikroTik es 203.0.113.10, igual a public-address; se puede publicar con cuidado. NAT del módem: la WAN es 192.168.1.2 y public-address es 203.0.113.10; módem en bridge o reenvío también en el módem. CGNAT: la WAN es 100.64.12.34, dentro de 100.64.0.0/10; sin port forwarding, túnel saliente o Back To Home.",
         "caption": "Comparar dos IP alcanza para saber si el acceso remoto es posible y por dónde.",
         "after": "Decidí con esta tabla"},
    ],
    "concepts": [
        {"name": "IP Cloud y DDNS",
         "para_que": "Le da al router un nombre fijo, `<serie>.sn.mynetname.net`, que sigue a su IP pública aunque cambie. Resuelve el problema de las conexiones con IP dinámica: el nombre siempre apunta a donde está el router.",
         "como": "`/ip/cloud/set ddns-enabled=yes` y `/ip/cloud/print` para leer `dns-name`, `public-address` y `status`. El nombre no abre nada: el firewall sigue descartando lo que llega de internet. Si no lo vas a usar, `ddns-enabled=auto update-time=no`.",
         "ejemplo": "En un comercio con IP dinámica, el túnel WireGuard de gestión usa como Endpoint el nombre de IP Cloud en vez de la IP. Cuando el proveedor cambia la IP de madrugada, a la mañana el túnel levanta igual."},
        {"name": "public-address contra la IP del WAN",
         "para_que": "public-address es la IP con la que el router llega a los servidores de MikroTik. Si la comparás con la IP de su interfaz WAN, sabés si el router está directo en internet o detrás de otro NAT, que es lo que decide si se puede publicar algo.",
         "como": "Si son iguales, IP pública directa. Si la WAN es privada (192.168.x o 10.x) y public-address es otra, hay un módem haciendo NAT. Si la WAN está en 100.64.0.0/10, es CGNAT. Con varias WAN, public-address es la de la conexión que usa la ruta hacia cloud2.mikrotik.com.",
         "ejemplo": "Un cliente pide ver su NVR desde el celular. Antes de prometer nada comparás: la WAN es 192.168.1.2, detrás del módem del proveedor. Ya sabés que hace falta el módem en bridge o reenviar en los dos equipos, y lo ponés en el presupuesto."},
        {"name": "CGNAT y Back To Home",
         "para_que": "Con CGNAT el proveedor comparte una IP pública entre muchos clientes y nadie de afuera puede iniciar una conexión hacia el router: no hay port forwarding posible. Back To Home lo resuelve con WireGuard a través de relays de MikroTik, siempre abierto desde el router.",
         "como": "Detrás de CGNAT, las opciones son un túnel saliente a un equipo con IP fija o Back To Home (RouterOS 7.12 o posterior, CPU ARM, ARM64 o TILE). Por el relay puede ir más lento, y el tráfico va cifrado de punta a punta.",
         "ejemplo": "Una casa de playa con internet 4G, con la WAN en 100.64.x.x, quiere ver las cámaras. Le explicás que abrir puertos no va a funcionar y configurás Back To Home o un túnel saliente a un concentrador (lección 20)."},
    ],
    "teoria_md": """### Un poco de historia

NAT se describió en 1994 (RFC 1631) como un parche temporal para estirar las direcciones IPv4 mientras llegaba IPv6. Terminó siendo permanente: casi todas las casas y oficinas salen a internet con una sola IP pública compartida por toda la red. En 2011 se agotó el stock central de direcciones IPv4 de IANA, y los proveedores empezaron a compartir también la IP pública entre varios clientes. Para eso se reservó en 2012 el rango `100.64.0.0/10` (RFC 6598): es el que ves en la WAN cuando el proveedor hace CGNAT.

Los servicios de DNS dinámico existen desde que las conexiones hogareñas empezaron a recibir IP que cambian. MikroTik ofrece el suyo, IP Cloud, integrado en RouterOS, y más tarde sumó Back To Home, que usa la misma nube para resolver el caso en que no hay IP pública.

### Cómo funciona

Con `ddns-enabled=yes`, el router se comunica con `cloud2.mikrotik.com` por UDP 15252. El servidor ve desde qué IP le llega el mensaje y actualiza el nombre `<serie>.sn.mynetname.net` con esa dirección, con un TTL de 60 segundos. Si el router está detrás de NAT y no ve su IP pública en sus propias interfaces, manda una actualización por minuto.

Ese mismo dato es `public-address`: la IP con la que el router llega a internet. Comparada con la IP de la WAN te dice dónde está el NAT. Si coinciden, el router tiene la IP pública y un dst-nat suyo alcanza. Si no coinciden y la WAN es privada, hay un módem traduciendo antes: un reenvío en el MikroTik no sirve si el módem no reenvía también, o si no se pasa a modo bridge. Si la WAN está en `100.64.0.0/10`, el NAT es del proveedor y no hay forma de pedirle que reenvíe.

Detrás de CGNAT solo funcionan las conexiones que abre el propio router hacia afuera. Back To Home aprovecha eso: el router mantiene una conexión abierta hacia el relay más cercano de MikroTik, y el celular o la notebook se conectan a ese relay. Las claves WireGuard quedan solo en el router y en el cliente, así que el relay pasa tráfico cifrado que no puede leer. El nombre del DDNS, en cualquier caso, nunca abre nada por sí mismo: el firewall sigue decidiendo.
""",
}

# =====================================================================================  10
M["10"] = {
    "fig": {"file": "10.svg",
            "alt": "Una central de monitoreo con IP 203.0.113.25 entra con flecha verde al router, cuyo dst-nat exige in-interface-list=WAN, TCP 8000 y src-address-list=nvr-permitidos, y la lleva al NVR 192.168.88.50 por TCP 8000. Cualquier otra IP termina con una cruz roja. En el router, un recuadro rojo: los puertos 80, 443 y 8291 del router nunca se publican.",
            "caption": "Un puerto, solo para las IP de la lista y con fecha de revisión; los puertos del router, nunca."},
    "steps": [
        {"file": "10-paso2.svg", "step": 2,
         "alt": "La regla dst-nat desarmada en cuatro partes: por dónde (in-interface-list=WAN), qué puerto (protocol=tcp dst-port=8000), quién (src-address-list=nvr-permitidos, resaltada) y a dónde (to-addresses=192.168.88.50 to-ports=8000). Abajo, el comando que agrega la IP a la lista con comentario y fecha de revisión.",
         "caption": "Cada parte de la regla achica quién llega al NVR.",
         "after": "dst-nat solo desde esa lista"},
        {"file": "10-paso5.svg", "step": 5,
         "alt": "Dos casos con una PC 192.168.88.20, el router 203.0.113.10 y el NVR 192.168.88.50. Sin hairpin, la PC pide a la IP pública, el router hace dst-nat y el NVR contesta directo a la PC, que descarta la respuesta. Con hairpin, el NVR le contesta al router y el router se lo devuelve a la PC.",
         "caption": "El masquerade de hairpin hace que la respuesta vuelva por el router.",
         "after": "en la oficina entran por la IP pública"},
    ],
    "concepts": [
        {"name": "dst-nat filtrado por origen",
         "para_que": "dst-nat redirige una conexión que llega a la IP pública hacia un equipo de la LAN. Sin filtro de origen, cualquier escaneo de internet llega al NVR; con `src-address-list`, solo entran las IP que pusiste en la lista. La documentación de NAT lo considera la forma más segura.",
         "como": "Una regla por servicio: `in-interface-list=WAN`, el protocolo y el puerto exacto de la app, `src-address-list=nvr-permitidos` y `to-addresses` con la IP del NVR. En la lista, cada IP con un comentario y una fecha de revisión.",
         "ejemplo": "La empresa de monitoreo de un cliente sale siempre por 203.0.113.25. Publicás solo el TCP 8000 del NVR para esa IP, con el comentario revisar 2027-04, y en abril confirmás si sigue siendo la misma."},
        {"name": "Lo que no se publica nunca",
         "para_que": "Los puertos del propio router (80, 443, 8291) y todos los puertos del NVR por las dudas son lo primero que buscan los escaneos automáticos. Exponerlos convierte un acceso puntual en una puerta grande.",
         "como": "Averiguá qué puerto usa de verdad la app del NVR (8000 es solo un ejemplo) y publicá ese. Para entrar al router desde afuera, VPN (lección 8).",
         "ejemplo": "Un instalador anterior dejó publicado un rango enorme de puertos hacia el NVR de una clínica porque la app no andaba. Lo reemplazás por una sola regla al puerto real, para la IP de la central, y la app sigue funcionando."},
        {"name": "Connection tracking: limpiar después de cambiar NAT",
         "para_que": "NAT solo mira el primer paquete de cada conexión; después el router recuerda qué hizo con ella. Por eso una regla nueva parece no andar: las conexiones viejas siguen con la decisión anterior.",
         "como": "Después de cambiar NAT, `/ip/firewall/connection/remove [find dst-address~\":8000\"]` y probás de nuevo. Para saber si la regla coincide, mirás el contador con `print stats`.",
         "ejemplo": "Ajustás el dst-nat del NVR y desde el celular sigue entrando como antes. Limpiás las conexiones al 8000, reintentás con datos móviles y ahora, sin estar en la lista, no conecta."},
        {"name": "Hairpin NAT",
         "para_que": "Cuando un equipo de la LAN entra al NVR por la IP pública, el NVR le contesta directo por la LAN y la PC descarta la respuesta porque esperaba otra IP de origen. El hairpin hace que el router también cambie el origen, y así la respuesta vuelve por él.",
         "como": "Solo si en la oficina entran por la IP pública: un masquerade en srcnat desde la LAN hacia el NVR, y en el dst-nat `dst-address-type=local dst-address=!192.168.88.1` en lugar de la lista WAN. Si pueden usar la IP interna, es más simple y no hace falta.",
         "ejemplo": "En una oficina, la app del NVR en los celulares tiene cargada la IP pública. Funciona en la calle pero no con el wifi de la oficina. Con el hairpin anda en los dos lados sin reconfigurar cada celular."},
    ],
    "teoria_md": """### Un poco de historia

El port forwarding nació como consecuencia del NAT: si toda la red sale con una sola IP pública, para que alguien de afuera llegue a un equipo de adentro hay que decirle al router a quién mandarle cada puerto. Durante años fue la forma normal de ver cámaras y DVR desde afuera, y en el foro de MikroTik todavía se trata como rutina.

El costo de esa costumbre quedó claro en 2016 con Mirai, una botnet que se armó con cámaras IP y grabadores expuestos a internet, en muchos casos con usuario y contraseña de fábrica. Desde entonces, la recomendación de fabricantes y de la propia documentación de MikroTik es VPN primero y, si hay que publicar, lo mínimo y filtrado por origen. El comportamiento de hairpin, también llamado NAT loopback, lo describe como requisito la RFC 4787 de 2007.

### Cómo funciona

Un `dst-nat` cambia la dirección de destino de un paquete antes de rutearlo. La central manda a `203.0.113.10:8000`; la regla lo convierte en `192.168.88.50:8000` y el router lo pasa a la LAN por la cadena forward. Las condiciones de la regla deciden a qué paquetes se aplica: `in-interface-list=WAN` (por dónde llega), `dst-port` (qué servicio) y `src-address-list` (desde dónde). Si el origen no está en la lista, la regla no se aplica, el paquete sigue apuntando al router y el firewall de fábrica lo descarta.

NAT trabaja sobre el seguimiento de conexiones. Solo el primer paquete de cada conexión pasa por las reglas de NAT; el resto sigue la decisión guardada en la tabla de conexiones. Por eso, después de cambiar una regla, conviene borrar las conexiones existentes a ese puerto: si no, la prueba muestra el comportamiento viejo.

El hairpin resuelve un caso particular. Una PC de la LAN pide a la IP pública; el router hace dst-nat hacia el NVR, que está en la misma red que la PC. El NVR ve como origen a `192.168.88.20` y le contesta directo, sin pasar por el router. La PC esperaba la respuesta de `203.0.113.10`, recibe una de `192.168.88.50` y la descarta. Con un `masquerade` desde la LAN hacia el NVR, el router reemplaza también el origen por el suyo: el NVR le contesta al router, y el router deshace las dos traducciones y le devuelve la respuesta a la PC.
""",
}

# =====================================================================================  11
M["11"] = {
    "fig": {"file": "11.svg",
            "alt": "La LAN del local conectada al router, que tiene ether1 hacia un módem de fibra con gateway 203.0.113.1 y ether2 hacia un módem 4G con gateway 192.168.8.1. Detrás de cada módem, sus testigos: 1.1.1.1 y 9.9.9.9 para ISP1 con distance=1, y 8.8.8.8 y 208.67.222.222 para ISP2 con distance=2. Una flecha verde punteada indica que el check-gateway se hace al testigo, no al módem.",
            "caption": "El router prueba un host más allá del módem: si no contesta, pasa al respaldo."},
    "steps": [
        {"file": "11-paso3.svg", "step": 3,
         "alt": "Dos casos con la fibra cortada entre el módem y el testigo. Con check-gateway al módem, el módem contesta y la ruta 1 sigue activa aunque no haya internet. Con check-gateway al testigo, el testigo no contesta, la ruta 1 cae y entra la de distance=2.",
         "caption": "El módem puede contestar con la fibra cortada; el testigo, no.",
         "after": "Defaults recursivas"},
        {"file": "11-paso5.svg", "step": 5,
         "alt": "Una fila de pings: cinco bien con ISP1, seis perdidos durante la conmutación y cinco bien por ISP2. Debajo, la tabla de rutas por defecto: las de 1.1.1.1 y 9.9.9.9 activas antes del corte y caídas después; las de 8.8.8.8 y 208.67.222.222 en espera antes y activas después. Una nota pide cortar aguas arriba del módem.",
         "caption": "Contá los pings perdidos y mirá qué rutas quedan activas con el ISP1 cortado.",
         "after": "dejá un ping continuo"},
    ],
    "concepts": [
        {"name": "Rutas recursivas con host testigo",
         "para_que": "El check-gateway común le hace ping al gateway, que suele ser el módem del proveedor, y el módem puede contestar aunque la fibra esté cortada en la calle. La ruta recursiva apunta a un host de internet, el testigo, que se alcanza por ese ISP: si el testigo no contesta, de verdad no hay internet por ahí.",
         "como": "Una ruta /32 a cada testigo por su gateway, con `scope=10`, y las rutas por defecto con `gateway=<testigo>`, `target-scope=11` y `check-gateway=ping`. Necesita gateways estables: con DHCP o PPPoE hay que adaptarlo.",
         "ejemplo": "En un supermercado de Las Piedras con fibra y 4G de respaldo, una obra en la vereda corta la fibra. El módem sigue prendido y contesta, pero 1.1.1.1 y 9.9.9.9 no: el router pasa al 4G y las cajas siguen cobrando."},
        {"name": "distance y dos testigos por enlace",
         "para_que": "distance decide qué ruta gana: la de número más bajo es la principal. Dos testigos por enlace evitan que la caída de un solo servicio externo te haga conmutar sin motivo.",
         "como": "ISP1 con distance=1 y dos testigos; ISP2 con distance=2 y otros dos, alcanzados por el respaldo. El cambio completo ocurre cuando los dos testigos del principal dejan de contestar. No uses como testigos los DNS que usan los equipos de la red.",
         "ejemplo": "Si usaras 8.8.8.8 como testigo de ISP1 y también como DNS de las PCs, al caer ISP1 las PCs intentarían resolver nombres por una ruta muerta. Por eso los testigos son direcciones que no se usan para otra cosa."},
        {"name": "Masquerade en las dos salidas y prueba real",
         "para_que": "Sin NAT por la segunda salida, el tráfico conmuta pero sale con IP privada y no vuelve. Y un failover que nunca se probó puede tener cualquiera de estos detalles mal sin que nadie lo note.",
         "como": "Sumás ether2 a la lista WAN para que el masquerade de la defconf (`out-interface-list=WAN`) cubra las dos. Después cortás el ISP1 aguas arriba del módem con un ping continuo y contás los pings perdidos al conmutar y al volver. MKController habla de 20 a 30 segundos.",
         "ejemplo": "Al entregar el failover de un local de cobranzas anotás en el acta la prueba: corte de fibra simulado y cuántos pings se perdieron al conmutar y al volver. El cliente sabe qué esperar y vos tenés la prueba documentada."},
    ],
    "teoria_md": """### Un poco de historia

Tener dos proveedores de internet en un local chico es cada vez más común: fibra como principal y 4G de respaldo. Los grandes operadores resuelven la redundancia con BGP, pero eso pide IP propias y acuerdos con los proveedores. En una oficina o un comercio se usa algo más simple: dos rutas por defecto con distinta prioridad y un mecanismo que detecte cuándo la principal dejó de servir.

El problema clásico de esa solución es qué se vigila. Vigilar el gateway, que casi siempre es el módem del proveedor, detecta un módem apagado pero no una fibra cortada en la calle. Las rutas recursivas, que existen en la mayoría de los routers profesionales, permiten vigilar algo que está más lejos. La documentación de MikroTik, en su artículo de Failover WAN Backup, enseña exactamente ese método.

### Cómo funciona

En RouterOS cada ruta tiene una `distance`. Si hay dos rutas al mismo destino, gana la de distancia menor; si tienen la misma, se reparten el tráfico (ECMP). Con `check-gateway=ping`, el router le hace ping al gateway de la ruta cada unos 10 segundos y, tras dos fallas seguidas, la deja inactiva. Ahí entra la siguiente distancia. Por eso la conmutación no es instantánea: un practicante la mide en 20 a 30 segundos, y no reacciona a pérdidas parciales, solo a un gateway que no contesta.

La ruta recursiva cambia a quién se le hace el ping. La ruta por defecto dice `gateway=1.1.1.1`, una dirección que no está conectada al router. Para saber por dónde llegar a ella, el router busca otra ruta: la `/32` hacia `1.1.1.1` por `203.0.113.1`. Ese encadenamiento lo controlan `scope` y `target-scope`: una ruta solo puede resolver su gateway usando rutas cuyo `scope` sea menor o igual a su `target-scope`. Con `scope=10` en las rutas de testigos y `target-scope=11` en las por defecto, la resolución funciona.

El resultado es que el ping de `check-gateway` viaja hasta el testigo, pasando por el módem y por la red del proveedor. Si se corta cualquier tramo, el testigo no contesta y la ruta cae. Con dos testigos por enlace, la conmutación completa ocurre recién cuando fallan los dos.

Falta una pieza: la NAT. El masquerade de la defconf sale por `out-interface-list=WAN`; si ether2 no está en esa lista, el tráfico conmutado sale con IP privada y no vuelve.
""",
}


# ------------------------------------------------------------------ scripts (no van en 4 ni 11: los reescribe otro agente)
from scripts_1_11 import S as SCRIPTS
for _k, _v in SCRIPTS.items():
    M[_k]["script_rsc"] = _v

# ------------------------------------------------------------------ validación
def lab_lines(card):
    lines = card.split("\n")
    i0 = next(i for i, l in enumerate(lines) if l.startswith("**Laboratorio**"))
    i1 = next(i for i, l in enumerate(lines) if l.startswith("**Regla para quedarse**"))
    out, inside = [], False
    for l in lines[i0:i1]:
        if l.startswith("```"):
            inside = not inside
            continue
        if not inside:
            out.append(l)
    return out


errs = []
dirs = {int(p.name[:2]): p for p in CLASS.iterdir() if p.is_dir() and p.name[:2].isdigit()}
for k, v in M.items():
    card = (dirs[int(k)] / "card.md").read_text(encoding="utf-8")
    labs = lab_lines(card)
    full_lab = "\n".join(labs)
    for s in v["steps"]:
        a = s["after"]
        if not (15 <= len(a) <= 40):
            errs.append(f"{k}: after de largo {len(a)}: {a}")
        hits = [l for l in labs if a in l]
        if len(hits) != 1:
            errs.append(f"{k}: after '{a}' aparece {len(hits)} veces fuera de código")
        elif not hits[0].lstrip().startswith(f"{s['step']}."):
            errs.append(f"{k}: after '{a}' no está en la línea del paso {s['step']}: {hits[0][:60]}")
        if not Path("/home/claude/ies-training/ilustraciones/mikrotik/" + s["file"]).exists():
            errs.append(f"{k}: falta {s['file']}")
    if not Path("/home/claude/ies-training/ilustraciones/mikrotik/" + v["fig"]["file"]).exists():
        errs.append(f"{k}: falta {v['fig']['file']}")
    if not 2 <= len(v["concepts"]) <= 4:
        errs.append(f"{k}: {len(v['concepts'])} conceptos")
    t = v["teoria_md"]
    nw = len(re.findall(r"\S+", t))
    if not (250 <= nw <= 450):
        errs.append(f"{k}: teoria_md con {nw} palabras")
    if "### Un poco de historia" not in t or "### Cómo funciona" not in t:
        errs.append(f"{k}: faltan subtítulos")
    blob = json.dumps(v, ensure_ascii=False)
    if "—" in blob or "–" in blob:
        errs.append(f"{k}: tiene guiones largos")
    if re.search(r"\btenés que\b", blob, re.I):
        errs.append(f"{k}: usa 'tenés que'")
    sc = v.get("script_rsc")
    if sc:
        cod = sc["codigo"]
        nl = len(cod.split("\n"))
        if not 15 <= nl <= 60:
            errs.append(f"{k}: script con {nl} líneas")
        usadas = set(re.findall(r"\{\{([A-Z_]+)\}\}", cod))
        decl = {x["nombre"] for x in sc["variables"]}
        if usadas != decl:
            errs.append(f"{k}: variables usadas {usadas} != declaradas {decl}")
        if ':put "Listo' not in cod and ':put ("Listo' not in cod:
            errs.append(f"{k}: falta :put Listo")
        if cod.count("{") != cod.count("}"):
            errs.append(f"{k}: llaves desbalanceadas")
        if re.search(r"[^\x00-\x7f·]", cod):
            errs.append(f"{k}: script con caracteres no ASCII: {set(re.findall(r'[^\x00-\x7f·]', cod))}")
        print(k, "script:", nl, "líneas")
    print(k, "teoria:", nw, "palabras")

if errs:
    print("\n".join(errs))
    raise SystemExit(1)
OUT.write_text(json.dumps(M, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("ok", OUT)
