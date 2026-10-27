"""Genera /home/claude/ies-training/ilustraciones/grandstream/manifest.json (figuras, pasos, conceptos y teoría)."""
import json

M = {}

# =====================================================================================  1
M["1"] = {
    "fig": {"file": "1.svg", "alt": "Tres tarjetas con la UCM6300 y sus puertos WAN y LAN. Switch, el modo de fábrica: WAN sube a la red y LAN queda en puente para una PC. Route, resaltado en verde: WAN sube a la red y LAN es un router con su propio DHCP; habilita DHCP opción 66 y Dynamic Defense. Dual: WAN y LAN son dos subidas independientes, LAN2 y LAN1. Abajo, un aviso: cambiar el modo en producción corta la web y los teléfonos.",
            "caption": "El modo de red cambia qué hace el puerto LAN; Route es el único que habilita opción 66 y Dynamic Defense."},
    "steps": [
        {"file": "1-paso1.svg", "step": 1, "after": "leé la IP en el LCD (botón Home)",
         "alt": "La UCM6300 conectada por su puerto WAN, resaltado, al router de laboratorio con DHCP 192.168.88.0/24, donde también está la notebook. El LCD de la central muestra 192.168.88.20 y la lista de DHCP del router muestra la misma IP.",
         "caption": "La IP se lee en el LCD con el botón Home o en la lista de DHCP del router."},
        {"file": "1-paso2.svg", "step": 2, "after": "cambiá la contraseña de admin",
         "alt": "A la izquierda, el navegador en https://192.168.88.20:8089 con usuario admin y la contraseña de la etiqueta trasera; abajo, la etiqueta con una contraseña única desde enero de 2017 y admin/admin tachado. A la derecha, Maintenance > Login Settings > Change Password con 10 a 30 caracteres, mayúscula, minúscula, número y especial, y un aviso sobre el CVE-2025-28172.",
         "caption": "Se entra con la contraseña de la etiqueta y se cambia en el mismo primer ingreso."},
        {"file": "1-paso4.svg", "step": 4, "after": "bajá un backup completo a tu notebook",
         "alt": "Tres tarjetas en orden: anotá la versión en Maintenance > Upgrade, bajá el backup en Maintenance > Backup a la notebook (resaltado) y recién al final actualizá. Notas: el archivo de restauración va en .tar o .tgz, menos de 100 MB y sin caracteres especiales; conviene programar backups a USB, SD, SFTP, NAS o S3.",
         "caption": "Primero la versión, después el backup fuera de la central y recién ahí el upgrade."},
    ],
    "concepts": [
        {"name": "Modo de red: Switch, Route o Dual",
         "para_que": "La UCM6300 tiene un puerto WAN y un puerto LAN, y el modo decide qué hace el LAN. Existe porque la misma central se instala en redes muy distintas: oficinas con router propio, sitios donde la central tiene que repartir IP a los teléfonos, o lugares con dos redes separadas.",
         "como": "Se elige en System Settings > Network Settings > Basic Settings > Method. Switch (de fábrica) deja el LAN en puente, para colgar una PC. Route convierte el LAN en un router con DHCP propio (192.168.2.1 de fábrica) y es el único modo que habilita DHCP opción 66 y Dynamic Defense. Dual usa los dos puertos como subidas independientes. Conviene decidirlo con la central vacía.",
         "ejemplo": "Una inmobiliaria en Pocitos ya tiene su MikroTik con DHCP: Switch alcanza. Una obra nueva en Maldonado donde la central va a aprovisionar 40 teléfonos por opción 66 en su propia red de voz: Route desde el primer día."},
        {"name": "Contraseña de la etiqueta",
         "para_que": "Las centrales con usuario y clave de fábrica son de las más comprometidas. Por eso Grandstream imprime desde enero de 2017 una contraseña de admin única en la etiqueta de cada equipo, en lugar del viejo admin/admin que todavía repiten algunas guías.",
         "como": "Se entra por HTTPS al puerto 8089 con usuario admin y la clave de la etiqueta, y en el primer ingreso se cambia en Maintenance > Login Settings > Change Password: 10 a 30 caracteres con mayúscula, minúscula, número y especial. La nueva va a la ficha del cliente, no a un papel pegado en el rack.",
         "ejemplo": "Llegás a un consultorio en Ciudad Vieja, sacás la central de la caja y antes de cargar una sola extensión ya cambiaste la clave y la guardaste en la ficha. Si alguien prueba admin/admin desde internet, no entra."},
        {"name": "Backup antes del firmware",
         "para_que": "Actualizar firmware corrige fallas y agujeros de seguridad, como el CVE-2025-28172 que dejaba probar contraseñas sin límite en la UCM6510 hasta la 1.0.20.52. Pero una actualización que sale mal sin backup obliga a reconfigurar todo de memoria.",
         "como": "Anotá la versión en Maintenance > Upgrade, bajá el backup completo en Maintenance > Backup > Backup/Restore a tu notebook y recién ahí actualizá. Para restaurar, el archivo va en .tar o .tgz, menos de 100 MB y sin caracteres especiales en el nombre. Después, backups programados a USB, SD, SFTP, NAS o S3.",
         "ejemplo": "Un sábado actualizás la central de una barraca en Paysandú y algo no queda como estaba. Con el .tar en la notebook, restaurás y en media hora la oficina vuelve a tener teléfonos el lunes."},
    ],
    "teoria_md": """### Un poco de historia

Las centrales telefónicas pasaron de ser armarios de relés y tarjetas a ser computadoras con Linux y una página web. Ese cambio trajo lo bueno de la informática (configuración remota, actualizaciones, backups) y también sus problemas: una central IP conectada a internet es un servidor más, y los servidores con usuario y clave de fábrica se atacan en masa.

En 2016 la botnet Mirai mostró a escala mundial lo que pasa con equipos que salen con credenciales conocidas: tomó cientos de miles de cámaras y routers probando listas de usuarios y contraseñas de fábrica. Desde enero de 2017 Grandstream imprime en la etiqueta de cada unidad una contraseña de admin única. Las guías de proveedores que todavía dicen admin/admin hablan de equipos anteriores.

El firmware también importa: el CVE-2025-28172 describe que la UCM6510 hasta la versión 1.0.20.52 no limitaba los intentos de login, una puerta abierta a la fuerza bruta. La corrección llega con firmware nuevo, y el firmware nuevo se instala con un backup a mano.

### Cómo funciona

La UCM6300 tiene dos puertos de red, WAN y LAN, y el modo de red define su relación:

- **Switch** (de fábrica): WAN sube a la red y LAN es un puente, como un switch de dos bocas.
- **Route**: la central rutea; el LAN tiene su propia red (192.168.2.1 de fábrica) con DHCP. Al ser el DHCP de esa red, puede entregar la opción 66 con la dirección de aprovisionamiento, y puede bloquear hosts por cantidad de conexiones (Dynamic Defense).
- **Dual**: los dos puertos son subidas independientes (LAN2 y LAN1) y se elige cuál es la interfaz por defecto.

La web va por HTTPS al puerto 8089; con Redirect From Port 80 activo, escribir la IP sola redirige ahí. Después de 5 intentos fallidos de login, la central bloquea el acceso 5 minutos. El primer ingreso abre un asistente que guía contraseña, red, zona horaria, extensiones y rutas.

El backup es un archivo `.tar` con la configuración. Guardado fuera de la central, es el único punto de vuelta atrás si una actualización o un cambio de modo de red sale mal: por eso el orden del laboratorio es versión, backup y recién después upgrade.""",
}

# =====================================================================================  2
M["2"] = {
    "fig": {"file": "2.svg", "alt": "Ventana de la extensión 1001 con cinco ajustes y, a la derecha, el problema que evita cada uno: contraseña SIP aleatoria, que nadie adivine la cuenta; Concurrent Registrations 1 o 2, menos equipos con la misma cuenta; NAT activado, que el teléfono detrás de un router reciba respuesta; Direct Media desactivado, que el audio pase por la central; DTMF Mode RFC4733, que buzón e IVR reconozcan las teclas.",
            "caption": "Cinco valores de la extensión, cada uno contra un problema concreto de soporte."},
    "steps": [
        {"file": "2-paso1.svg", "step": 1, "after": "Activá la contraseña aleatoria",
         "alt": "PBX Settings > General Settings con Enable Random Password en Sí; abajo, la extensión nueva 1001 con SIP/IAX Password que se completa sola. A la derecha, lo que pide la central (10 caracteres o más, mayúscula, minúscula, número, especial, sin secuencias) y lo que no: contraseña 1001 en la extensión 1001 o una clave inventada por una persona.",
         "caption": "Con Enable Random Password, cada extensión nueva nace con una contraseña que nadie inventó."},
        {"file": "2-paso3.svg", "step": 3, "after": "En cada una, revisá:",
         "alt": "Dos escenas. Izquierda, en verde, Direct Media desactivado: el audio de la interna 1001 y de la 1002, que está detrás de un router remoto, pasa por la UCM. Derecha, en rojo, Direct Media activado: la central solo arma la llamada y el audio directo entre teléfonos se corta en el NAT remoto.",
         "caption": "Con Direct Media apagado la central lleva el audio de los dos lados y el NAT no lo corta."},
    ],
    "concepts": [
        {"name": "Contraseña SIP aleatoria",
         "para_que": "La extensión SIP es una cuenta: quien tenga número y contraseña puede registrarse y llamar a cuenta del cliente. Las contraseñas inventadas por personas (1001, 1234, el nombre de la empresa) son las primeras que prueban los barridos automáticos.",
         "como": "En PBX Settings > General Settings se activa Enable Random Password y la central completa SIP/IAX Password con 10 caracteres o más, mayúscula, minúscula, número y especial. El teléfono la carga por aprovisionamiento; nadie la tipea. Cambiarla en producción desregistra el teléfono hasta que se reprovisiona.",
         "ejemplo": "Un estudio contable en el Centro tenía la 1001 con contraseña 1001. Con la contraseña aleatoria y Zero Config, nadie del estudio la conoce y no hay nada que adivinar."},
        {"name": "Registros concurrentes",
         "para_que": "Una misma extensión puede estar registrada en varios equipos a la vez, por ejemplo el teléfono del escritorio y la app Wave. Cada registro de más es un equipo más que puede usar esa cuenta, y si las credenciales se filtran, un registro ajeno pasa desapercibido.",
         "como": "En Basic Settings > Concurrent Registrations el valor de fábrica es 3 y el máximo 10. Conviene dejar 1, o 2 si la persona usa Wave, y anotar en la ficha qué equipo ocupa cada registro.",
         "ejemplo": "La recepcionista de una clínica en Tres Cruces usa solo el GRP del mostrador: Concurrent Registrations en 1. Si mañana aparece un segundo registro con su número, la central lo rechaza."},
        {"name": "Direct Media",
         "para_que": "Por defecto la central lleva el audio de los dos lados de la llamada por ella misma. Direct Media existe para que, cuando se puede, los teléfonos se manden el audio directo y la central se ahorre ese trabajo.",
         "como": "En la pestaña Media de la extensión, Enable Direct Media viene desactivado y así conviene dejarlo. Activado, la central intenta redirigir el RTP entre los teléfonos, y el propio manual avisa que no siempre se puede negociar: con un teléfono detrás de NAT, el audio directo no llega y aparece el audio de un solo lado.",
         "ejemplo": "La 1002 es el teléfono del gerente en su casa del Prado. Con Direct Media apagado, el audio va por la central y llega; activado, la 1001 de la oficina intenta mandarle audio a una IP privada de otra red y se corta."},
        {"name": "NAT en la extensión y DTMF RFC4733",
         "para_que": "SIP escribe direcciones IP dentro de sus mensajes, y un teléfono detrás de un router escribe la suya privada. El ajuste NAT hace que la central le conteste a la dirección real de donde vino el paquete. El modo DTMF define cómo viajan las teclas que marcás durante una llamada.",
         "como": "En Media, NAT viene activado y DTMF Mode en RFC4733, que manda cada tecla como evento dentro del audio RTP. Con Info las teclas van en mensajes SIP INFO; con Inband, como sonido, y requiere G.711.",
         "ejemplo": "Un cliente llama al buzón para escuchar sus mensajes y las teclas no responden. Revisás y la extensión quedó en Inband con un codec comprimido; la volvés a RFC4733 y el buzón entiende cada tecla."},
    ],
    "teoria_md": """### Un poco de historia

SIP, el protocolo que usan la UCM y sus teléfonos, se publicó primero como RFC 2543 en 1999 y quedó en su forma actual con la RFC 3261 en 2002. Para autenticar copió el mecanismo Digest de HTTP (RFC 2617, de 1999): el teléfono nunca manda la contraseña, manda un cálculo hecho con ella y con un número que la central le pide resolver. Es un buen mecanismo, pero no protege de una contraseña fácil de adivinar: un barrido automático prueba contraseñas una tras otra contra la extensión.

SIP también se diseñó pensando en direcciones públicas, y los teléfonos escriben su IP dentro de los mensajes. Cuando NAT se volvió la norma en oficinas y casas, aparecieron extensiones como la RFC 3581 (2003), que permite responder al puerto y la dirección reales de origen. El ajuste NAT de la extensión de la UCM va en esa línea.

Para las teclas, la RFC 2833 (2000) definió cómo mandarlas como eventos dentro del flujo RTP; la reemplazó la RFC 4733 en 2006, y por eso la UCM muestra RFC4733 donde otros equipos todavía dicen RFC 2833.

### Cómo funciona

Una extensión SIP en la UCM es una cuenta con número, contraseña y una pestaña Media que define cómo se maneja el audio:

- **Registro**: el teléfono manda REGISTER, la central responde 401 pidiendo credenciales, el teléfono vuelve con el cálculo Digest y la central contesta 200 OK. Concurrent Registrations limita cuántos equipos pueden tener ese registro a la vez (3 de fábrica, hasta 10).
- **Audio**: en cada llamada los equipos anuncian en el SDP a qué IP y puerto quieren recibir el RTP. Con Direct Media apagado, cada teléfono le habla a la central y la central reenvía; con Direct Media activado, la central intenta que se hablen entre ellos, lo que falla cuando hay NAT de por medio.
- **Teclas**: con RFC4733, cada tecla viaja como un paquete RTP especial que dice qué tecla fue y cuánto duró, por el mismo camino que la voz.

La contraseña aleatoria cierra la puerta de entrada; NAT activado y Direct Media apagado sostienen el audio; RFC4733 hace que buzón, IVR y portero entiendan las teclas.""",
}

# =====================================================================================  3
M["3"] = {
    "fig": {"file": "3.svg", "alt": "Dos diagramas de secuencia entre un teléfono recién reseteado y la UCM. SIP SUBSCRIBE, en cualquier modo de red: el teléfono manda SUBSCRIBE a multicast, la UCM contesta NOTIFY con la URL y el teléfono baja el XML. DHCP opción 66, solo con la UCM en Route: DHCP DISCOVER, OFFER con opción 66 y descarga del XML. Notas: el XML viaja por TFTP, HTTP o HTTPS; en Route la URL es por ejemplo https://192.168.2.1:8089/zccgi/.",
            "caption": "Dos caminos para que el teléfono encuentre a la UCM; los dos terminan bajando un XML."},
    "steps": [
        {"file": "3-paso2.svg", "step": 2, "after": "reseteado de fábrica a la misma red",
         "alt": "La UCM 192.168.88.20 manda un SIP Message a toda la red 192.168.88.0/24; dos GRP26xx reseteados responden y aparecen en la lista, un equipo de otra marca no aparece. A la derecha, Auto Discover en Device Management > Zero Config con Scan Method SIP Message, Scan IP 192.168.88.255 y Scan all MACs en No, y un aviso sobre Auto Assign Extension.",
         "caption": "Con Scan IP terminada en .255 el escaneo llega a toda la red; solo aparecen equipos con OUI de Grandstream."},
        {"file": "3-paso4.svg", "step": 4, "after": "En Global Policy, poné idioma español",
         "alt": "Tres niveles apilados: Global Policy abajo con idioma español y zona de Montevideo, Global Template en el medio sin idioma, Model Template arriba con idioma inglés para el GRP, marcado como el que gana. Resultado: el GRP queda en inglés con hora de Montevideo. Abajo, un aviso: lo configurado a mano en la web del teléfono no lo pisa ninguna plantilla.",
         "caption": "Cuando dos plantillas dicen distinto gana la de más arriba; lo tocado a mano en el teléfono no lo pisa ninguna."},
    ],
    "concepts": [
        {"name": "Zero Config",
         "para_que": "Configurar teléfono por teléfono a mano es lento y deja diferencias: uno con otra hora, otro con otro idioma, otro con la contraseña mal copiada. Zero Config hace que la central descubra los teléfonos y les mande la configuración entera, igual para todos.",
         "como": "Se activa en Device Management > Zero Config. El teléfono reseteado aparece solo; si no, Auto Discover con Scan Method SIP Message y la dirección de broadcast de la red. Se edita el equipo descubierto, se le asigna la extensión en la cuenta 1 y se sincroniza. Si falta el modelo, se baja su plantilla en Model Update.",
         "ejemplo": "Un hotel en Punta del Este con 60 habitaciones: se conectan los GRP al switch de voz, aparecen en la lista, se asigna cada extensión y en una tarde todos quedan con idioma, hora y cuenta correctos."},
        {"name": "SIP SUBSCRIBE y DHCP opción 66",
         "para_que": "El teléfono recién reseteado no sabe dónde está su central. Hay dos formas de que se entere: preguntando a toda la red local o recibiendo la dirección junto con su IP.",
         "como": "Con SIP SUBSCRIBE el teléfono, al arrancar, manda un SUBSCRIBE a una dirección multicast; la UCM lo ve y le contesta un NOTIFY con la URL del XML. Con DHCP opción 66, la UCM tiene que ser el DHCP de esa red, o sea estar en modo Route: el teléfono pide IP y en la respuesta viene la URL, por ejemplo https://192.168.2.1:8089/zccgi/.",
         "ejemplo": "En una oficina en Carrasco el DHCP lo da el router del cliente y la UCM está en Switch: los teléfonos se descubren por SUBSCRIBE. En la obra de Maldonado con la UCM en Route, la opción 66 los lleva directo a la central."},
        {"name": "Prioridad de plantillas",
         "para_que": "Hay ajustes que valen para todos los teléfonos (idioma, zona horaria) y otros que dependen del modelo. Las plantillas por nivel permiten escribir cada cosa una sola vez y que la más específica mande.",
         "como": "La prioridad es Global Policy < Global Template < Model Template: si dos dicen distinto, gana la de la derecha. Global Policy es una sola para todos; Global Template puede haber varias con una por defecto; Model Template es por modelo. Lo configurado a mano en la web del teléfono no lo pisa ninguna.",
         "ejemplo": "Pusiste español y Montevideo en Global Policy, pero un GRP sigue en inglés. Hay un Model Template de ese modelo con idioma inglés, o alguien lo cambió a mano en el teléfono; en ese caso, reset de fábrica y que lo tome Zero Config."},
    ],
    "teoria_md": """### Un poco de historia

El aprovisionamiento automático de teléfonos IP se apoya en piezas viejas de internet. TFTP, el protocolo más simple para bajar un archivo, es la RFC 1350 de 1992. La opción 66 de DHCP, "nombre del servidor TFTP", quedó definida en la RFC 2132 de 1997, y los fabricantes de teléfonos la adoptaron para decirle a cada equipo de dónde bajar su configuración apenas recibe su IP.

SIP sumó otro camino. El par SUBSCRIBE y NOTIFY, pensado para que un equipo se suscriba a eventos de otro, se definió en la RFC 3265 en 2002 (hoy RFC 6665, de 2012). Grandstream lo usa para el descubrimiento: el teléfono anuncia que existe y la central le responde con la dirección de su configuración.

Con los años la configuración pasó de archivos de texto planos a XML, y de TFTP a HTTP y HTTPS. Para varios sitios, Grandstream propone hoy GDMS, su plataforma en la nube; Zero Config es la versión local, dentro de la UCM.

### Cómo funciona

1. **Descubrimiento**. El teléfono arranca y manda un SUBSCRIBE a una dirección multicast de la LAN; la UCM contesta con un NOTIFY que trae la URL del XML. Si la UCM está en Route, el teléfono también puede recibir esa URL en la opción 66 del DHCP. Si alguno no aparece, Auto Discover manda un SIP Message a la dirección de broadcast (por ejemplo `192.168.88.255`) y los teléfonos responden.
2. **Armado del XML**. La UCM junta los parámetros de las plantillas en orden de prioridad (Global Policy, Global Template, Model Template) y los datos de la cuenta asignada. La configuración se escribe en XML, pero se arma desde la web sin tocar XML.
3. **Entrega**. El teléfono baja el archivo por TFTP, HTTP o HTTPS, lo aplica y registra su cuenta.

Hay una excepción importante: lo que alguien configuró a mano en la web del teléfono queda por encima de cualquier plantilla. Por eso el teléfono aprovisionado no se toca a mano; si quedó distinto, se resetea y se deja que Zero Config lo configure de nuevo. Y Auto Assign Extension, que asigna extensiones solo, va únicamente en una red de voz separada, para no tomar teléfonos ajenos.""",
}

# =====================================================================================  4
M["4"] = {
    "fig": {"file": "4.svg", "alt": "Tres tarjetas. Register SIP Trunk, resaltada: la UCM se registra en el proveedor con usuario y clave. Peer SIP Trunk: dos UCM, casa central y sucursal, se hablan por IP sin registro. Account SIP Trunk: un ATA o gateway sin IP fija se registra en tu UCM. Abajo: proveedor con usuario y contraseña es Register; la UCM admite hasta 200 troncales SIP.",
            "caption": "La pregunta es quién se registra en quién: con un proveedor de usuario y clave, Register."},
    "steps": [
        {"file": "4-paso1.svg", "step": 1, "after": "Creá el troncal con los datos",
         "alt": "Diagrama de secuencia entre la UCM, el router del cliente y el proveedor sip.proveedor.example: REGISTER con usuario 21000000, 401 pidiendo credenciales, REGISTER con la respuesta, 200 OK Registered, y después OPTIONS cada 60 segundos con su 200 OK como heartbeat. Nota: la UCM inicia la charla y las respuestas vuelven por la misma sesión del router.",
         "caption": "La central sale a registrarse y las respuestas vuelven por la misma sesión: el troncal registrado no pide reenvío de puertos."},
        {"file": "4-paso3.svg", "step": 3, "after": "Revisá el estado en System Status",
         "alt": "System Status > Dashboard > Trunks con los dos estados posibles: Registered y Rejected, este resaltado. Dos preguntas para Rejected: si desde una PC en la misma red el host del proveedor resuelve y responde, y si usuario, Auth ID y contraseña son los del proveedor, copiados y pegados.",
         "caption": "Rejected tiene dos causas: no llegás al proveedor o las credenciales no son las suyas."},
        {"file": "4-paso4.svg", "step": 4, "after": "Hacé las cuatro pruebas",
         "alt": "Cuatro tarjetas en verde: sale, llamando a un celular desde una interna; entra, llamando desde un celular al número del troncal; muestra bien el número, el celular ve el caller ID que corresponde; pasa los tonos, dejando un mensaje en un buzón usando el teclado.",
         "caption": "Registered no alcanza: el troncal se da por terminado cuando pasan las cuatro pruebas."},
    ],
    "concepts": [
        {"name": "Register, Peer y Account",
         "para_que": "Un troncal SIP es la conexión de la central con afuera, y hay tres formas de armarla según quién tenga IP fija y quién se autentique. Elegir el tipo equivocado es la primera causa de un troncal que nunca registra.",
         "como": "Register SIP Trunk es para el proveedor que te da usuario y contraseña: tu UCM se registra en él. Peer une centrales por IP, sin registro, por ejemplo casa central y sucursal. Account es al revés que Register: un equipo sin IP fija, como un ATA o un gateway, se registra en tu UCM. Todo en Extension/Trunk > VoIP Trunks > Add.",
         "ejemplo": "Una distribuidora con local en Montevideo y depósito en Canelones: troncal Register contra el proveedor en la central principal y un Peer entre las dos UCM para que las internas se llamen entre sedes."},
        {"name": "Estado del troncal: Registered o Rejected",
         "para_que": "Un troncal caído no avisa: el cliente se entera cuando no le entran llamadas. El Dashboard muestra en un solo lugar si cada troncal registró, para verlo antes que el cliente.",
         "como": "En System Status > Dashboard, Trunks. Rejected significa que la UCM no logró registrarse: o no llega al servidor del proveedor (DNS, salida a internet, firewall) o las credenciales no coinciden. Se prueba desde una PC en la misma red que el host resuelve y responde, y se vuelven a pegar usuario, Auth ID y contraseña.",
         "ejemplo": "Instalás en una escribanía y el troncal queda en Rejected. Desde tu notebook el host del proveedor resuelve, así que vas a las credenciales: el Auth ID era distinto del usuario y lo habías dejado igual."},
        {"name": "Heartbeat",
         "para_que": "Un troncal puede figurar como registrado y haber dejado de responder. El heartbeat es una pregunta periódica para saber si el otro lado sigue vivo y, si no, dejar de mandarle llamadas.",
         "como": "En Advanced Settings del troncal, Enable Heartbeat Detection (viene en No) y Heartbeat Frequency, 60 segundos de fábrica. La UCM manda un SIP OPTIONS y espera respuesta. Con heartbeat, la caída se detecta y el failover de la ruta saliente puede usar otro troncal.",
         "ejemplo": "El proveedor principal de una clínica en el Cordón tiene un corte. Con heartbeat, la central lo marca caído y las salientes van por el troncal de respaldo sin que nadie llame a soporte."},
        {"name": "Codecs del troncal",
         "para_que": "El codec es el formato en que viaja la voz. Si la central ofrece codecs que el proveedor no usa, la negociación puede elegir mal o fallar; recortar la lista deja solo lo que funciona.",
         "como": "En Advanced Settings, Codec Preference con PCMA y PCMU (las dos variantes de G.711) y el resto afuera; PCMA primero cuando la red pública usa A-law. DTMF Mode en RFC4733, igual que las extensiones.",
         "ejemplo": "Un troncal que entra bien pero algunas llamadas suenan raras o no pasan los tonos. Dejás solo PCMA y PCMU, como pide el proveedor, y la negociación queda siempre igual."},
    ],
    "teoria_md": """### Un poco de historia

Antes de SIP, la central se conectaba al mundo con líneas analógicas o con enlaces digitales E1, cables físicos de la telefónica que entraban a una tarjeta. El troncal SIP reemplazó ese cable por una cuenta: la misma voz viaja por internet y la central se autentica ante el proveedor como si fuera un teléfono grande.

Todo eso está en SIP desde la RFC 3261 (2002): el método REGISTER para anunciarse, el desafío 401 con autenticación Digest y el método OPTIONS, que sirve para preguntarle a otro equipo qué soporta y, de paso, si está vivo. La voz, en cambio, sigue usando el codec más viejo de todos: G.711, la norma de la UIT de 1972 para digitalizar la voz a 64 kbit/s. Tiene dos variantes, A-law y µ-law; µ-law se usa en Norteamérica y Japón, A-law en casi todo el resto del mundo. En SIP se las llama PCMA (A-law) y PCMU (µ-law).

### Cómo funciona

Con un **Register SIP Trunk**, la UCM sale a buscar al proveedor:

1. Manda `REGISTER` al host del proveedor con su usuario.
2. El proveedor responde `401` con un desafío.
3. La UCM repite el `REGISTER` con el cálculo hecho con su contraseña y su Auth ID.
4. Con `200 OK`, el Dashboard muestra el troncal registrado.

Como la UCM inicia la conversación, el router del cliente arma una sesión de NAT y las respuestas vuelven por ella. Por eso, para el troncal registrado no hace falta reenviar puertos: Simtex, un proveedor de troncales, dice que en el 99,9 % de los casos no se necesita.

Con el **heartbeat** activo, la UCM manda `OPTIONS` cada 60 segundos y espera respuesta. Si no llega, considera el troncal caído y las rutas pueden pasar al troncal de failover.

Al armar cada llamada, los dos lados intercambian en el SDP la lista de codecs que aceptan. Con la lista recortada a PCMA y PCMU no hay sorpresas.

Un troncal registrado todavía puede fallar en algo: el caller ID, las entrantes o los tonos. Por eso las cuatro pruebas: sale, entra, muestra bien el número y pasa el DTMF.""",
}

# =====================================================================================  5
M["5"] = {
    "fig": {"file": "5.svg", "alt": "Escalera de cuatro niveles de privilegio, de menos a más: Internal, Local, National e International. Tabla: una extensión de nivel Local no sale ni por la ruta nacional ni por la internacional; una de nivel National sale por la nacional y no por la internacional; una International sale por las dos y en la internacional le piden PIN. Notas: si roban una interna National el fraude choca contra la ruta internacional; nivel igual o mayor pasa, menor se rechaza.",
            "caption": "La extensión pasa por la ruta si su nivel es igual o mayor; la internacional además pide PIN."},
    "steps": [
        {"file": "5-paso1.svg", "step": 1, "after": "Ruta nacional (ejemplo con numeración",
         "alt": "El patrón _[24]XXXXXXX desarmado en casillas: guion bajo, el grupo [24] y siete X; abajo, marca 29001007 y coincide. El patrón _09XXXXXXX con 0, 9 y siete X; un número con dígitos de menos no coincide. Tabla de comodines: guion bajo empieza el patrón, X de 0 a 9, Z de 1 a 9, N de 2 a 9, [24] uno de esos, punto uno o más.",
         "caption": "Cada carácter del patrón es un dígito: con uno de más o de menos, el número no matchea."},
        {"file": "5-paso3.svg", "step": 3, "after": "Si el cliente marca 9 para salir",
         "alt": "La interna marca 929001007; el número matchea _9NXXXXXXX; Strip 1 tacha el 9 y al proveedor llega 29001007. Nota en rojo: sin Strip, el 9 viaja al proveedor pegado al número.",
         "caption": "El 9 elige la ruta y Strip 1 lo saca antes de mandar el número al troncal."},
    ],
    "concepts": [
        {"name": "Patrón de marcado",
         "para_que": "La central necesita decidir, con solo mirar los dígitos marcados, qué tipo de llamada es y por qué troncal sale. El patrón es una plantilla que describe una familia de números en lugar de cada número suelto.",
         "como": "Todos empiezan con guion bajo. X es cualquier dígito, Z de 1 a 9, N de 2 a 9, los corchetes dan opciones ([24] es 2 o 4) y el punto es uno o más de cualquier cosa. Un patrón por línea en Outbound Routes; el largo cuenta, así que un dígito de más o de menos no matchea.",
         "ejemplo": "Para una oficina en Montevideo: `_[24]XXXXXXX` agarra los fijos de 8 dígitos y `_09XXXXXXX` los celulares. Un número de 7 dígitos marcado por error no sale por ninguna de las dos."},
        {"name": "Privilegio de ruta",
         "para_que": "Si alguien roba la contraseña de una extensión, lo primero que intenta es llamar a destinos caros. El privilegio separa quién puede llamar a dónde, para que una extensión comprometida no pueda hacer todo.",
         "como": "Hay cuatro niveles: Internal, Local, National e International. Cada ruta tiene uno y cada extensión otro; la extensión usa la ruta si su nivel es igual o mayor. La ruta internacional va con International y la mayoría de las extensiones, con National o menos.",
         "ejemplo": "En una barraca de Colonia solo el administrativo hace llamadas al exterior: su extensión es International y el resto National. Si roban la cuenta del depósito, la llamada a un destino premium del exterior se rechaza."},
        {"name": "PIN en rutas caras",
         "para_que": "El privilegio frena a la extensión equivocada, pero no a la correcta usada por otra persona. El PIN agrega algo que la persona sabe y la extensión no guarda.",
         "como": "En Outbound Routes > PIN Groups se crea el grupo con los PIN y en la ruta internacional se elige en Password Settings. Al marcar un número internacional, la central pide el PIN antes de cursar la llamada. Con PIN Groups with Privilege Level se pueden usar PIN y privilegio juntos.",
         "ejemplo": "El gerente de un estudio en Pocitos llama a clientes en Buenos Aires: marca 00 54 y el número, la central le pide su PIN y recién ahí sale."},
        {"name": "Strip y failover",
         "para_que": "Muchas oficinas marcan un prefijo para salir, como el 9, que no es parte del número. Strip lo saca antes del troncal. El failover existe para que las salientes sigan si el troncal principal cae.",
         "como": "Con `_9NXXXXXXX` y Strip 1 la central usa el 9 para elegir la ruta y manda el resto. En la ruta se agrega un troncal de failover: la UCM lo usa si el principal no responde en 32 segundos o devuelve 403, 407, 408, 503 o 603. La prioridad entre rutas depende de Outgoing Routing Priority (orden de lista o precisión del patrón).",
         "ejemplo": "Una inmobiliaria con costumbre de marcar 9: marcan 929001007 y al proveedor llega 29001007. Si el proveedor principal se cae, la llamada sale por el segundo troncal."},
    ],
    "teoria_md": """### Un poco de historia

Los números de teléfono siguen un plan mundial, la recomendación E.164 de la UIT: código de país, código de área y número, hasta 15 dígitos. Uruguay es el 598 y desde adentro se marca 00 para salir al exterior. Cada central tiene que reconocer esa estructura con solo mirar los dígitos.

La forma de escribir patrones que usa la UCM, con guion bajo, X, Z, N y punto, es la que popularizó Asterisk, la central de software libre que Mark Spencer empezó en 1999. La UCM comparte esa herencia: su syslog nombra módulos como pjsip y chan_dahdi, y menciona AMI, la interfaz de administración de Asterisk.

El fraude de peaje es tan viejo como las centrales con salida automática. Con la telefonía IP cambió de escala: ya no hace falta estar dentro de la oficina, alcanza con adivinar una extensión desde internet y llamar a destinos caros a cuenta del cliente. Por eso el manual de seguridad de la UCM pone juntos privilegios por ruta, PIN, filtro por caller ID de origen y bloqueo de países.

### Cómo funciona

Cuando una extensión marca, la central:

1. **Compara** los dígitos con los patrones de cada ruta saliente. Si coinciden con más de una, decide Outgoing Routing Priority: orden en la lista o el patrón más preciso.
2. **Verifica el privilegio**: si el nivel de la extensión es igual o mayor que el de la ruta, sigue; si es menor, rechaza.
3. **Pide el PIN** si la ruta lo tiene.
4. **Aplica Strip** (y Prepend si lo hay) para dejar el número como lo espera el proveedor.
5. **Elige el troncal**: el principal, y si no responde en 32 segundos o contesta 403, 407, 408, 503 o 603, el de failover.

Un ejemplo con `_00X.` en la ruta internacional: el 00 fija el prefijo, X exige al menos un dígito y el punto acepta el resto, sea del largo que sea. Por eso esa ruta es la que más protección necesita: un patrón que agarra todo, sin PIN, es una invitación al fraude.""",
}

# =====================================================================================  6
M["6"] = {
    "fig": {"file": "6.svg", "alt": "Tres llamadas entran del troncal a los números 29001007, 29001012 y 29001020 y pasan por una sola ruta entrante con Pattern _2900XXXX, destino By DID y Strip 4. Cada una sale hacia su interna: 1007, 1012 y 1020. Debajo: 2900 se saca y queda 1007.",
            "caption": "Una ruta con patrón, ByDID y Strip reemplaza una ruta por cada número directo."},
    "steps": [
        {"file": "6-paso2.svg", "step": 2, "after": "revisá de dónde lee el DID",
         "alt": "Un INVITE de ejemplo del proveedor: la primera línea, la Request-line, trae sip:29001007; el encabezado To trae la cuenta 21000000. Abajo, VoIP Trunks > Advanced Settings con DID Mode en Request-line, y un aviso: con DID Mode en To-header ese INVITE se leería como 21000000 y no matchearía _2900XXXX.",
         "caption": "El proveedor puede mandar el número llamado en la Request-line o en el To; DID Mode dice dónde leerlo."},
        {"file": "6-paso3.svg", "step": 3, "after": "Calculá el Strip para tres formatos",
         "alt": "Tres números en casillas con los caracteres que se sacan tachados en rojo y los que quedan en verde: 29001007 con Strip 4, 59829001007 con Strip 7 y +59829001007 con Strip 8 porque el más cuenta. En los tres queda 1007.",
         "caption": "Strip cuenta caracteres desde la izquierda, el más incluido, hasta que queda la interna."},
    ],
    "concepts": [
        {"name": "DID y ByDID",
         "para_que": "Un DID es un número directo: el cliente compra varios y quiere que cada uno suene en un escritorio. Hacer una ruta por número funciona con tres, pero con cien se vuelve inmanejable.",
         "como": "En Extension/Trunk > Inbound Routes, sobre el troncal, se crea una ruta con un patrón que agrupa los DID, destino By DID y un Strip. La central toma el número que llega, le saca los primeros dígitos y llama a la interna que queda.",
         "ejemplo": "Una empresa de seguridad en Ciudad Vieja compró 29001000 a 29001099. Con `_2900XXXX`, By DID y Strip 4, cada número suena en su interna 1000 a 1099 sin cien rutas."},
        {"name": "DID Mode",
         "para_que": "En el INVITE que manda el proveedor, el número llamado puede venir en la primera línea (Request-line) o en el encabezado To. Si la central mira el lugar equivocado, ve otro número y la entrante no matchea.",
         "como": "En VoIP Trunks > troncal > Advanced Settings > DID Mode se elige Request-line (de fábrica) o To-header. Si las entrantes no matchean, se mira una captura o el CDR para ver dónde viene realmente el DID.",
         "ejemplo": "Cambiás de proveedor en una clínica y desde ese día las entrantes van al destino por defecto. En la captura, el DID viene en el To y la Request-line trae la cuenta: pasás DID Mode a To-header y cada número vuelve a su interna."},
        {"name": "Strip en la entrante",
         "para_que": "El proveedor manda el número completo, a veces con código de país o con el más adelante, y la interna es solo el final. Strip recorta exactamente lo que sobra.",
         "como": "Se cuentan los caracteres desde la izquierda hasta donde empieza la interna: 29001007 con Strip 4, 59829001007 con Strip 7 y +59829001007 con Strip 8, porque el más cuenta. Cada formato necesita además su propio patrón. El dato sale de la primera llamada de prueba en el CDR, no de la factura.",
         "ejemplo": "En la factura figura 2900 1007, pero en el CDR el número llega como +59829001007. Con Strip 4 la central buscaría una interna que no existe; con Strip 8 suena la 1007."},
    ],
    "teoria_md": """### Un poco de historia

Antes de las centrales con marcación directa, todas las llamadas entraban por un mismo número y una operadora las pasaba a mano. La marcación directa entrante (DID en inglés, DDI en Europa) permitió que el que llama marque directamente un escritorio. En las líneas digitales E1 la telefónica mandaba los últimos dígitos marcados y la central los usaba para elegir la interna.

Con SIP, el número viaja dentro del mensaje `INVITE`. La RFC 3261 (2002) define dos lugares donde aparece el destino: la Request-URI, en la primera línea, que dice a dónde va el pedido en ese tramo, y el encabezado `To`, que dice a quién estaba dirigida la llamada originalmente. En una llamada simple coinciden; cuando pasa por proxies y proveedores, pueden ser distintos, y cada proveedor decide dónde pone el DID.

### Cómo funciona

Cuando entra una llamada por el troncal, la UCM:

1. **Lee el número llamado** según DID Mode: de la Request-line (de fábrica) o del To.
2. **Lo compara** con los patrones de las rutas entrantes de ese troncal, por ejemplo `_2900XXXX`.
3. **Aplica el destino**. Con By DID, saca los caracteres que indica Strip y usa lo que queda como número de interna.

El ejemplo oficial de Grandstream es claro: patrón `_0655441XXX`, By DID y Strip 6; una llamada a 0655441007 pierde 065544 y llega a la 1007.

El Strip cuenta caracteres, no dígitos: el `+` del formato internacional también cuenta. Por eso conviene mirar el número real en el CDR o en una captura antes de calcular, porque la factura suele mostrarlo en otro formato.

La ruta entrante admite además condiciones de horario (definidas en System Settings > Time Settings > Office Time/Holiday) y una lista negra global de entrantes que acepta incluso Anonymous. Así la misma ruta puede mandar los DID a las internas en horario y a un buzón o un IVR fuera de horario.""",
}

# =====================================================================================  7
M["7"] = {
    "fig": {"file": "7.svg", "alt": "Árbol del IVR principal, extensión 7000 con prompt de bienvenida. Tecla 1: en Office Time va al Ring Group ventas, fuera de horario al buzón 1001. Tecla 2: siempre a la interna 1002. Si no marca nada, Response Timeout lleva al Ring Group recepción; si marca mal, Invalid lleva también a recepción. Notas: hasta cinco destinos por tecla con su horario; sin destino de Timeout o Invalid, la central corta.",
            "caption": "Cada tecla con su destino por horario, y destino también para el que no marca o marca mal."},
    "steps": [
        {"file": "7-paso4.svg", "step": 4, "after": "Si habilitás Dial Other Extensions",
         "alt": "Quien llama al IVR 7000 marca 1002, recepción, que está en la lista y suena; marca 1010, gerencia, que está fuera de la lista y no se puede marcar. Abajo, Basic Call Features > IVR con Dial Other Extensions en Sí y Dial Block/Allowlist con Allowlist 1002.",
         "caption": "Con la lista blanca, desde el IVR solo se llega a las internas públicas."},
        {"file": "7-paso5.svg", "step": 5, "after": "y no marques nada",
         "alt": "Dos recorridos para quien no marca nada: bienvenida, espera de 10 segundos de Response Timeout y 3 repeticiones. Con destino de Timeout, termina en el Ring Group recepción; sin destino, la central corta.",
         "caption": "Después de las repeticiones, la llamada va al destino de Timeout; si no hay, se corta."},
    ],
    "concepts": [
        {"name": "IVR",
         "para_que": "El IVR es el menú que atiende y ofrece opciones con el teclado. Sirve para repartir llamadas sin una telefonista y para dar información básica (horarios, dirección) sin ocupar a nadie.",
         "como": "Se crea en Basic Call Features > IVR con un número propio (por ejemplo 7000), un prompt de bienvenida subido en PBX Settings > Voice Prompt > Custom Prompt y un destino por tecla: extensión, grupo, cola, buzón, otro IVR o número externo. La ruta entrante apunta al IVR.",
         "ejemplo": "Una automotora en Avenida Italia: 1 ventas, 2 taller, 3 repuestos. El que llama elige y cae directo en el grupo que corresponde."},
        {"name": "Condición de horario por tecla",
         "para_que": "La misma tecla no debería hacer lo mismo a las 10 de la mañana que a las 10 de la noche o un feriado. Con condiciones de horario, un solo IVR cubre día, noche y feriados.",
         "como": "Primero se define el horario de oficina y los feriados en System Settings > Time Settings > Office Time/Holiday. Después, cada tecla admite hasta cinco destinos con condiciones distintas: Office Time, Out of Office Time, Holiday, Specific Time o All Time.",
         "ejemplo": "En la automotora, la tecla 1 en Office Time va al Ring Group ventas; fuera de horario, al buzón 1001; el 1 de mayo, feriado cargado, también al buzón."},
        {"name": "Timeout e Invalid",
         "para_que": "Mucha gente no marca nada: llama desde el auto, no entiende el menú o espera a una persona. Si el IVR no sabe qué hacer con ella, la llamada se pierde.",
         "como": "Response Timeout es lo que espera la central después del prompt (10 segundos de fábrica), repite el aviso (3 veces de fábrica) y al terminar va al destino de Timeout; si no hay destino, corta. Invalid funciona igual para la tecla equivocada. Los dos admiten destinos por horario.",
         "ejemplo": "Una señora llama a una veterinaria en Malvín y no marca nada. Sin destino de Timeout, después de tres repeticiones la central le corta; con destino a recepción, a los pocos segundos la atiende una persona."},
        {"name": "Lista blanca de internas en el IVR",
         "para_que": "Dial Other Extensions permite marcar una interna directo desde el menú. Es cómodo, pero sin límite cualquiera que conozca un número llega a la gerencia, a una sala o a un equipo que no debería recibir llamadas de afuera.",
         "como": "En el IVR, Dial Block/Allowlist en Allowlist con solo las internas públicas (hasta 500). Las que no están en la lista no se pueden marcar desde el IVR.",
         "ejemplo": "En un estudio jurídico, el socio solo quiere llamadas pasadas por la secretaria. Su interna queda fuera de la lista; recepción y administración, adentro."},
    ],
    "teoria_md": """### Un poco de historia

El IVR existe porque existe el DTMF. Cuando Bell lanzó en 1963 los teléfonos de teclado Touch-Tone, cada tecla pasó a sonar como la mezcla de dos tonos que una máquina podía reconocer. A partir de ahí, una computadora podía atender, reproducir un mensaje grabado y entender qué opción elegía quien llamaba. Los bancos, las aerolíneas y las telefónicas fueron los primeros en usarlo para atender volumen sin sumar operadoras.

En una central IP como la UCM, el IVR es una función más del sistema, y las teclas ya no llegan como sonido sino como eventos RFC 4733 dentro del audio. La capacidad creció con las versiones: un post viejo del blog de Grandstream hablaba de menús de hasta 5 niveles, y el manual actual admite hasta 64 IVR anidados.

### Cómo funciona

Un IVR es una pequeña máquina de estados:

1. **Bienvenida**. La llamada entra (por ejemplo desde una ruta entrante) y suena el prompt.
2. **Espera**. La central espera una tecla durante el Response Timeout (10 segundos de fábrica). Entre dígitos, si se permite marcar internas, espera el Digit Timeout (3 segundos) para dar el número por completo.
3. **Decide**. Si la tecla tiene evento, evalúa sus condiciones de horario en orden y manda la llamada al destino que corresponde a ese momento. Si no hay tecla, repite el prompt de timeout (3 veces de fábrica) y al terminar va al destino de Timeout. Si la tecla no existe, hace lo mismo con Invalid.
4. **Sin destino, corta**. Si Timeout o Invalid quedaron vacíos, al terminar las repeticiones la central cuelga.

Los horarios salen de Office Time/Holiday: la central compara la hora actual con esa definición. Por eso conviene que la zona horaria de la UCM esté bien configurada, y por eso para probar fuera de horario alcanza con cambiar el horario de oficina y volver a llamar.

Si se habilita Dial Other Extensions, el IVR acepta números de interna además de las teclas. La lista blanca (o negra) limita a cuáles se puede llegar.""",
}

# =====================================================================================  8
M["8"] = {
    "fig": {"file": "8.svg", "alt": "Dos tarjetas. Ring Group 6000, sin espera: una llamada hace sonar las internas 1001 y 1002; todos a la vez o en orden con 60 segundos por miembro, y si nadie atiende va al destino del grupo. Call Queue 6500, en verde, retiene y reparte: cuatro llamadas esperan con música y pasan a los agentes 1001, 1002 y 1003; estrategia Ring All de fábrica, Least Recent, Fewest Calls y otras; largo máximo y destino de desborde.",
            "caption": "El grupo hace sonar teléfonos; la cola hace esperar llamadas y las reparte."},
    "steps": [
        {"file": "8-paso3.svg", "step": 3, "after": "marcá *97 desde la 1001",
         "alt": "La interna 1001 marca *97 y entra al buzón, que pide PIN nuevo. 1234 se rechaza por secuencia, 1111 por repetido, y un PIN propio de 4 dígitos o más sin patrón se acepta. Notas: con un PIN trivial cualquiera escucha los mensajes; el envío a correo necesita SMTP configurado y Keep Voicemail after Emailing viene activo.",
         "caption": "La central rechaza 1234 y 1111: el PIN del buzón tiene que ser propio."},
        {"file": "8-paso5.svg", "step": 5, "after": "Llamá a la cola desde dos teléfonos",
         "alt": "Cinco llamadas esperan en una cola con Max Queue Length 5; la sexta va al Failover Destination, Ring Group 6000. Tres agentes: 1001 en otra llamada, 1002 que atendió hace 2 minutos y 1003 que hace más que no atiende, al que le toca con Least Recent. Tabla: Agent Ring Time 30 s, Retry Time 5 s, Agent Rest Time 10 s. Aviso: Max Queue Length viene en 0, sin límite.",
         "caption": "Least Recent le da la llamada al agente que hace más que no atiende; la que no entra va al desborde."},
    ],
    "concepts": [
        {"name": "Grupo de llamada",
         "para_que": "Es la respuesta al pedido más común: que cuando llamen suene en varios teléfonos. No retiene a nadie: suena, alguien atiende o la llamada sigue a otro destino.",
         "como": "En Basic Call Features > Ring Group: número (6000), miembros y estrategia, Ring Simultaneously para todos a la vez o en orden, con 60 segundos por miembro de fábrica. Skip Busy Agent saltea a quien está hablando. Si nadie atiende, va al destino del grupo, que puede ser un buzón propio.",
         "ejemplo": "En una ferretería de La Teja, el número principal hace sonar el mostrador y la oficina a la vez. Atiende el primero que puede."},
        {"name": "Cola de llamadas",
         "para_que": "Cuando entran más llamadas que personas para atender, el grupo no alcanza: los que llaman reciben ocupado o quedan sonando. La cola los retiene con música y los reparte a medida que los agentes se liberan.",
         "como": "En Basic Call Features > Call Queue: número (6500), agentes y estrategia (Ring All de fábrica, Linear, Least Recent, Fewest Calls, Random, Round Robin). Tiempos de fábrica: 30 s sonando por agente, 5 s antes de pasar al siguiente y 10 s de descanso después de cortar.",
         "ejemplo": "La mesa de ayuda de un proveedor de internet en Las Piedras: con Least Recent, cada llamada va al técnico que hace más tiempo que no atiende, y la carga se reparte pareja."},
        {"name": "Largo máximo y desborde",
         "para_que": "Una cola sin límite puede dejar gente esperando con música hasta que corta sola. El largo máximo y el destino de desborde le dan una salida a la llamada que ya no conviene retener.",
         "como": "Max Queue Length viene en 0, que es sin límite. Con un valor (por ejemplo 5), la sexta llamada escucha ocupado y va al Failover Destination: un grupo, un buzón, otro IVR o un número externo. El mismo destino se usa si la cola queda sin agentes.",
         "ejemplo": "Un lunes a primera hora la mesa de ayuda se satura: desde la sexta llamada en espera, van al Ring Group de administración, que toma los datos y devuelve."},
        {"name": "Buzón de voz con PIN propio",
         "para_que": "El buzón guarda mensajes que pueden ser privados, y se entra por teléfono. Con un PIN trivial, cualquiera que tenga acceso a un teléfono de la oficina, o desde afuera si se habilita el acceso remoto, los escucha.",
         "como": "Desde la propia interna se marca *97. El PIN es numérico de 4 dígitos o más y la central rechaza secuencias y repeticiones como 1234 o 1111. Send Voicemail to Email requiere el SMTP de la central configurado; Keep Voicemail after Emailing viene activo.",
         "ejemplo": "La dueña de una inmobiliaria recibe los mensajes en su correo mientras visita propiedades. El PIN de su buzón no es su interna ni 1234, y el acceso remoto por DID queda apagado."},
    ],
    "teoria_md": """### Un poco de historia

Las dos herramientas vienen de mundos distintos. El grupo de llamada es la versión digital de una costumbre de las centrales de siempre: que varias líneas internas suenen juntas para que atienda el que esté libre. La cola viene de los centros de llamadas, donde se desarrolló la distribución automática de llamadas (ACD en inglés): retener a quien llama, ordenarlo en fila y entregarlo a la próxima persona disponible según una regla.

En la UCM las dos conviven y el blog de Grandstream suma funciones de call center sobre la cola: anuncio de posición, devolución de llamada que conserva el lugar en la fila, escucha y susurro por códigos y estadísticas de cola.

El buzón de voz, por su parte, es de las funciones más viejas de las centrales con computadora, y también de las más atacadas: un buzón con PIN trivial es una puerta a información privada.

### Cómo funciona

**Grupo (Ring Group)**. Cuando entra una llamada, la central hace sonar a los miembros todos a la vez (Ring Simultaneously) o uno tras otro (en orden), con 60 segundos por miembro de fábrica. No hay espera: si nadie atiende, la llamada va al destino del grupo.

**Cola (Call Queue)**. La llamada entra a una fila y escucha música. Por cada llamada, la central elige un agente según la estrategia:

- **Ring All**: suenan todos los libres (de fábrica).
- **Least Recent**: el que hace más tiempo que no atiende.
- **Fewest Calls**: el que menos llamadas atendió.
- También Linear, Random y Round Robin.

Con los tiempos de fábrica, el teléfono del agente suena 30 s; si no atiende, la central espera 5 s y prueba con el siguiente; después de cada llamada, el agente descansa 10 s. Max Queue Length limita cuántas llamadas esperan a la vez (0 es sin límite); al pasarse, y también si la cola queda sin agentes, la llamada va al Failover Destination.

**Buzón**. Cada interna tiene el suyo; `*97` entra al propio con el PIN. Los mensajes duran hasta 15 minutos de fábrica y hay hasta 50 por carpeta. Con SMTP configurado, cada mensaje puede llegar al correo.""",
}

# =====================================================================================  9
M["9"] = {
    "fig": {"file": "9.svg", "alt": "A la izquierda, la casa del gerente: el interno remoto 1003 detrás de un router hogareño con NAT. En el medio, internet. A la derecha, la oficina 192.168.88.0/24: el router de la oficina con IP 203.0.113.10 reenvía UDP 5060 y UDP 10000-20000 a la UCM y tiene SIP ALG apagado; la UCM 192.168.88.20 tiene External Host 203.0.113.10 y Local Network 192.168.88.0/24. Nota: tres lugares, tres ajustes.",
            "caption": "El interno remoto necesita ajustes en la central, en el router de la oficina y en la extensión."},
    "steps": [
        {"file": "9-paso1.svg", "step": 1, "after": "Guardá y reiniciá cuando lo pida",
         "alt": "PBX Settings > SIP Settings > NAT con External Host 203.0.113.10, Use IP address in SDP en Sí y Local Network Address 192.168.88.0/24. A un teléfono de la oficina, 192.168.88.30, la central le anuncia c=IN IP4 192.168.88.20; al interno remoto, fuera de esa red, le anuncia c=IN IP4 203.0.113.10. Aviso: sin Local Network Address la dirección externa no se arma bien.",
         "caption": "Local Network Address le dice a la central qué es adentro, y con eso elige qué IP anunciar."},
        {"file": "9-paso2.svg", "step": 2, "after": "En el router de la central",
         "alt": "Tabla del router: UDP 5060 hacia 192.168.88.20:5060 para señalización SIP, UDP 10000-20000 hacia 192.168.88.20:10000-20000 para audio RTP, y SIP ALG apagado. En rojo: reenviar UDP 5555 afuera hacia 5060 adentro no funciona porque SIP lleva el puerto en sus encabezados. Avisos sobre Fail2ban y RemoteConnect.",
         "caption": "Dos reenvíos y el ALG apagado; el puerto SIP se cambia en la central, no solo en el router."},
        {"file": "9-paso4.svg", "step": 4, "after": "En el teléfono remoto: servidor SIP",
         "alt": "Secuencia entre el teléfono remoto, su router hogareño y el servidor STUN stun.ipvideotalk.com: el teléfono pregunta con qué IP y puerto lo ven, el servidor responde 198.51.100.7 y un puerto, y el teléfono usa esa dirección para registrarse en 203.0.113.10. Abajo, la configuración STUN Server y NAT Traversal en STUN, y un aviso: con NAT simétrico STUN no alcanza.",
         "caption": "STUN le dice al teléfono cómo lo ve internet, para que anuncie esa dirección."},
    ],
    "concepts": [
        {"name": "External Host y Use IP address in SDP",
         "para_que": "La UCM detrás de un router solo conoce su IP privada. Si la escribe en los mensajes que salen a internet, el teléfono remoto intenta mandarle audio a una dirección que no puede alcanzar. External Host le dice cuál es su dirección pública.",
         "como": "En PBX Settings > SIP Settings > NAT, External Host con la IP pública fija o el nombre DDNS. Use IP address in SDP hace que el SDP use esa IP resuelta. Si es un nombre, la central lo resuelve una sola vez. Se guarda y se reinicia.",
         "ejemplo": "Una oficina en el Centro con IP fija 203.0.113.10: External Host 203.0.113.10. Si el servicio tiene IP dinámica, se configura DDNS en System Settings > DDNS Settings y se pone el nombre."},
        {"name": "Local Network Address",
         "para_que": "Con External Host solo, la central no sabe a quién le corresponde la IP pública y a quién la privada. Local Network Address lista las redes que son adentro; sin eso, la guía oficial avisa que la dirección externa no se arma bien.",
         "como": "En la misma pantalla NAT se cargan las redes internas, por ejemplo 192.168.88.0/24, y todas las que tengan teléfonos (VLAN de voz incluida). A los equipos de esas redes la central les anuncia su IP privada; al resto, External Host.",
         "ejemplo": "Configuraste External Host y ahora los internos de la oficina tienen audio cortado. Falta Local Network Address: la central les está mandando la IP pública también a ellos."},
        {"name": "Reenvío de puertos y puerto SIP",
         "para_que": "El interno remoto llega desde internet, así que el router de la oficina tiene que dejar pasar la señalización y el audio hacia la central. Y SIP escribe el puerto adentro de sus mensajes, por eso cambiarlo solo en el router no sirve.",
         "como": "En el router: UDP 5060 y UDP 10000 a 20000 hacia la IP de la UCM, y SIP ALG apagado. En la extensión, NAT activado. Si querés otro puerto SIP, se cambia en la central y se reenvía ese mismo puerto: 5555 afuera hacia 5060 adentro no funciona.",
         "ejemplo": "Un técnico abrió 5555 en el router hacia el 5060 de la central para esconder el puerto. El remoto registra a medias y las llamadas fallan: los mensajes de la central siguen diciendo 5060."},
        {"name": "STUN",
         "para_que": "El teléfono remoto también está detrás de un router y no sabe cómo lo ve internet. STUN es un servidor al que le pregunta qué IP y puerto ve de afuera, para anunciar esa dirección.",
         "como": "En el teléfono, Settings > General Settings > STUN Server stun.ipvideotalk.com (puerto 3478) y en la cuenta, NAT Traversal en STUN. Con NAT simétrico, donde el router cambia el puerto para cada destino, STUN no alcanza y se recurre a keep-alive y puertos abiertos.",
         "ejemplo": "El GRP del gerente en su casa del Prado no registra. Con STUN activo, aprende la IP pública de su casa y la anuncia; registra y la llamada de prueba tiene audio en los dos sentidos."},
    ],
    "teoria_md": """### Un poco de historia

SIP se diseñó (RFC 2543 en 1999, RFC 3261 en 2002) en una internet donde se suponía que cada equipo tenía su dirección pública. Por eso los mensajes SIP llevan adentro la IP y el puerto de quien los manda, y el SDP dice a qué IP y puerto mandar el audio.

Pero para ese momento NAT ya estaba en todos lados. Las direcciones privadas, como 192.168.x.x, se reservaron en la RFC 1918 de 1996, y NAT, descripto en la RFC 1631 de 1994 y actualizado en la RFC 3022 de 2001, permite que muchas compartan una IP pública. NAT cambia las direcciones de los encabezados IP, pero no toca lo que está escrito dentro de SIP y SDP.

Para resolverlo nacieron varias herramientas. STUN se publicó en la RFC 3489 en 2003 y se actualizó en la RFC 5389 en 2008: un servidor que le dice a un equipo cómo lo ven desde afuera. Las centrales sumaron ajustes como External Host para anunciar su IP pública. Y aparecieron los SIP ALG en los routers, que intentan reescribir los mensajes y muchas veces lo hacen mal.

### Cómo funciona

Con la UCM en `192.168.88.20` detrás del router `203.0.113.10`:

1. **El remoto registra**. El teléfono manda REGISTER a `203.0.113.10:5060`; el router lo reenvía a la UCM. Con NAT activado en la extensión, la UCM contesta a la IP y el puerto de donde vino el paquete.
2. **La UCM anuncia su dirección**. En cada llamada escribe en el SDP a dónde quiere recibir el audio. Si el destino está en Local Network Address, pone `192.168.88.20`; si no, pone External Host, `203.0.113.10`.
3. **El audio cruza**. El remoto manda RTP a `203.0.113.10` en un puerto entre 10000 y 20000; el router lo reenvía a la UCM.
4. **El teléfono también se describe bien**. Si su router no lo deja registrar, STUN le informa su IP y puerto públicos.

RemoteConnect, el servicio pago de Grandstream, evita tocar el router; si se usa el método manual, su MediaNAT Traversal queda desactivado.

Cada puerto que se abre hacia internet recibe barridos: por eso este laboratorio se termina de verdad cuando la central queda cerrada con Fail2ban, listas blancas y Geo-IP.""",
}

# =====================================================================================  10
M["10"] = {
    "fig": {"file": "10.svg", "alt": "Tres tarjetas en orden. 1, NAT y puertos: External Host, Local Network Address, UDP 5060 y 10000-20000. 2, SIP ALG: apagado en el router, reiniciar o limpiar sesiones, y si no se apaga TLS u otro router. 3, en verde, captura: Ethernet Capture en la UCM, línea c= del SDP, RTP Streams en Wireshark. Notas sobre el corte de los 32 segundos por ACK perdido y por qué este orden.",
            "caption": "Primero NAT y puertos, después el ALG, y la captura para confirmar antes de tocar nada."},
    "steps": [
        {"file": "10-paso3.svg", "step": 3, "after": "En Wireshark filtrá la señalización",
         "alt": "SDP de un INVITE o 200 OK con el filtro sip || sdp: la línea c=IN IP4 203.0.113.10, IP pública, dice al otro lado a dónde devolver el audio; m=audio 10044 RTP/AVP 8 0 da el puerto RTP dentro de 10000 a 20000. En rojo: c=IN IP4 192.168.88.20 hacia afuera hace que el otro extremo mande el audio a una IP privada y se pierda.",
         "caption": "Si la línea c= de un mensaje que sale a internet trae una IP privada, ahí está el audio que no llega."},
        {"file": "10-paso4.svg", "step": 4, "after": "Verificá el audio real",
         "alt": "Tabla de RTP Streams de una llamada de 20 segundos: de la UCM 192.168.88.20:10044 al remoto 198.51.100.7 hay unos 1000 paquetes; del remoto a la UCM, 0. Lo que dice la tabla y qué mirar después: el c= y m= anunciados, el reenvío de ese puerto y si un ALG tocó el SDP.",
         "caption": "RTP Streams muestra el audio real: un sentido con paquetes y el otro en cero es audio de un lado."},
        {"file": "10-paso5.svg", "step": 5, "after": "Si sospechás ALG: apagalo",
         "alt": "La UCM manda bien c=IN IP4 203.0.113.10; un router con SIP ALG reescribe SIP y SDP y al otro extremo llega c=IN IP4 192.168.88.20. Síntomas: audio de un solo lado, corte a los 30 y pico segundos, registra pero no entran llamadas. Qué hacer: apagarlo, reiniciar el router, repetir la captura y comparar; si no se puede apagar, TLS, otro segmento o cambiar el router.",
         "caption": "Un ALG reescribe lo que la central mandó bien; se apaga, se reinicia el router y se vuelve a capturar."},
    ],
    "concepts": [
        {"name": "SDP y la línea c=",
         "para_que": "SIP arma la llamada, pero el audio viaja aparte, por RTP. El SDP es la parte del mensaje donde cada lado dice a qué IP y puerto quiere recibir ese audio y con qué codecs. Si esa dirección está mal, la llamada conecta y el audio no llega.",
         "como": "En la captura, con el filtro `sip || sdp`, se abre el INVITE y el 200 OK. La línea `c=IN IP4` da la IP; la línea `m=audio` da el puerto (dentro de 10000 a 20000 en la UCM) y los codecs. Hacia afuera tiene que verse la IP pública; una privada indica que falta External Host o que un ALG la reescribió.",
         "ejemplo": "En la oficina de una despachante en la Aguada, el remoto no se escucha. En el 200 OK que sale de la central aparece `c=IN IP4 192.168.88.20`: faltaba External Host."},
        {"name": "SIP ALG",
         "para_que": "El SIP ALG es una función de muchos routers que intenta arreglar el problema de SIP con NAT reescribiendo las direcciones dentro de los mensajes. La UCM y los teléfonos Grandstream ya manejan NAT, y el ALG termina rompiendo lo que estaba bien.",
         "como": "Se apaga en el router (SIP ALG o SIP Helper) y después se reinicia el router o se limpian las sesiones. La RFC 4787 pide que estos ALG vengan apagados. Si no se puede apagar: TLS, que el router no puede leer, otro segmento o cambiar el router. Plexatalk y SureVoIP admiten casos raros donde ayuda, con servidores viejos que no manejan NAT.",
         "ejemplo": "Un cliente cambia el router del proveedor y desde ese día las llamadas se cortan a los 32 segundos. El router nuevo traía SIP ALG activo; se apaga, se reinicia y el corte desaparece."},
        {"name": "Corte a los 32 segundos (Timer H)",
         "para_que": "Un síntoma muy reconocible: la llamada se atiende, se habla, y se corta siempre entre los 30 y 35 segundos. Saber de dónde sale ese número ahorra horas de prueba y error.",
         "como": "Al atender, el que llamó confirma con un ACK. Si el ACK no llega (casi siempre porque algo en el camino reescribió mal las direcciones), el que atendió lo sigue esperando hasta el Timer H, 64 veces T1 de 500 ms: 32 segundos. Al vencer, corta.",
         "ejemplo": "Soporte típico: \"se corta siempre al medio minuto\". Antes de tocar codecs, se busca en la captura el ACK del 200 OK; no está, y el router tiene ALG."},
        {"name": "Captura en la UCM",
         "para_que": "Sin captura, el audio de un lado se diagnostica cambiando cosas a ver qué pasa. Con captura, se ve qué dirección anunció cada lado y en qué sentido viaja el audio.",
         "como": "En Maintenance > Network Troubleshooting > Ethernet Capture, interfaz de los teléfonos, Start; llamada de 20 segundos; Stop y descarga. En Wireshark, `sip || sdp` para la señalización y Telephony > RTP > RTP Streams para el audio. Conviene capturar en el propio equipo y comparar lo que salió con lo que llegó.",
         "ejemplo": "Un GXP oye pero no es oído, y solo contra un servidor. RTP Streams muestra paquetes en un sentido y cero en el otro: el problema queda acotado a un camino concreto en lugar de a \"la red\"."},
    ],
    "teoria_md": """### Un poco de historia

SIP separa la señalización del audio desde su origen. El SDP, el formato con que cada lado describe su audio, se publicó en la RFC 2327 en 1998, se actualizó en la RFC 4566 en 2006 y hoy rige la RFC 8866 de 2021. El modelo de oferta y respuesta que usa SIP para negociarlo es la RFC 3264 (2002). El audio viaja por RTP, la RFC 1889 de 1996 reemplazada por la RFC 3550 en 2003.

Cuando NAT se generalizó, algunos fabricantes de routers sumaron los SIP ALG para reescribir esas direcciones al vuelo. El resultado fue tan irregular que la RFC 4787 (2007, BCP 127), que fija cómo deben comportarse los NAT con UDP, recomienda en su requisito REQ-10 que estos ALG vengan apagados.

Para ver todo esto existe Wireshark, el analizador de protocolos que nació en 1998 como Ethereal y tomó su nombre actual en 2006. La UCM puede capturar en su propia interfaz, sin un switch con puerto espejo.

### Cómo funciona

Una llamada tiene dos conversaciones:

- **Señalización SIP**: `INVITE`, `200 OK`, `ACK`. En el INVITE y en el 200 OK viaja el SDP. La línea `c=IN IP4 203.0.113.10` dice "mandame el audio a esta IP"; `m=audio 10044 RTP/AVP 8 0` dice "a este puerto, con PCMA o PCMU".
- **Audio RTP**: cada lado manda paquetes a la dirección que anunció el otro, unos 50 por segundo con G.711 a 20 ms.

Si un lado anuncia una IP privada hacia internet, el otro le manda el audio a una dirección inalcanzable: se escucha en un sentido y no en el otro. Si el puerto RTP anunciado no está reenviado, pasa lo mismo.

Si algo reescribe mal la señalización, el `ACK` puede no llegar. SIP retransmite el 200 OK y espera el ACK hasta el Timer H, 64 veces T1 (500 ms), o sea 32 segundos, y después corta. De ahí el corte fijo cerca del medio minuto.

El orden de diagnóstico sigue la frecuencia de las causas: el manual de la UCM repite que el audio de un lado casi siempre es NAT o puertos SIP y RTP; después el ALG; y la captura confirma antes de tocar el router. Una captura tiene números y audio reales: se guarda lo justo y no sale del soporte.""",
}

# =====================================================================================  11
M["11"] = {
    "fig": {"file": "11.svg", "alt": "Un barrido desde internet, con varios intentos de INVITE y REGISTER por segundo, atraviesa cinco capas: router con solo puertos con nombre y motivo, Geo-IP con los países que usás, Fail2ban con 600 segundos de baneo, administración con lista blanca web, sin 80 ni 443 y SSH y AMI apagados, y rutas con privilegio y PIN en verde. Una franja roja se angosta capa tras capa. Nota con el caso de Wazo y más de 50 IPs baneadas.",
            "caption": "Ninguna capa sola alcanza: cada una frena lo que dejó pasar la anterior."},
    "steps": [
        {"file": "11-paso1.svg", "step": 1, "after": "Fail2ban y tus IPs permitidas",
         "alt": "La IP 198.51.100.66 manda REGISTER fallidos a la UCM con Fail2Ban activo y queda baneada 600 segundos; la oficina técnica 198.51.100.20 está en la Allowlist y nunca se banea. Abajo, System Settings > Security Settings > Fail2Ban con Banned Duration 600 y Allowlist 192.168.88.0/24, 198.51.100.20.",
         "caption": "Fail2ban banea a quien falla una y otra vez; la Allowlist evita banear a tu propio soporte."},
        {"file": "11-paso2.svg", "step": 2, "after": "Acceso web:",
         "alt": "System Settings > HTTP Server con Redirect From Port 80 en No, puerto 8089, Enable IP Address Whitelist en Sí y la lista con red local y oficina. La red local y la oficina técnica ven el login; cualquier otra IP ni siquiera lo ve. Aviso: activar la lista o Geo-IP en remoto sin tu IP te deja afuera. Nota sobre SSH, GDMS Remote SSH y AMI.",
         "caption": "La web solo para quien la administra; tu IP se agrega antes de activar la lista."},
        {"file": "11-paso5.svg", "step": 5, "after": "En el router, hacé una tabla",
         "alt": "Tabla de puertos del router: UDP 5060 a la UCM para internos remotos, pedido por gerencia, queda abierto; UDP 10000-20000 para audio de remotos, queda abierto; TCP 8089 y TCP 22 sin motivo y sin nadie que los haya pedido, se cierran. Notas: la administración se hace desde la red local o la oficina técnica; lo que queda abierto tiene Fail2ban y Geo-IP.",
         "caption": "Cada puerto abierto con nombre, motivo y quién lo pidió; lo que no tiene motivo se cierra."},
    ],
    "concepts": [
        {"name": "Fail2ban",
         "para_que": "Una central expuesta recibe intentos automáticos de registro y llamadas desde el primer día. Fail2ban mira los intentos fallidos y bloquea por un tiempo a la IP que insiste, para que probar contraseñas sea lento y caro.",
         "como": "En System Settings > Security Settings > Fail2Ban viene activo: SIP Defense mira REGISTER, INVITE y SUBSCRIBE fallidos y Login Attack Defense los ingresos a la web. El baneo de fábrica es 600 segundos. En la Allowlist van la red local y la IP fija de la oficina técnica, para no bloquearse a uno mismo.",
         "ejemplo": "Un administrador de Wazo abrió la consola de su central expuesta y vio varios INVITE maliciosos por segundo; en sus primeros baneos juntó más de 50 IPs. Con Fail2ban, cada una queda afuera después de pocos intentos."},
        {"name": "Administración cerrada",
         "para_que": "La web de la central controla todo: extensiones, rutas, troncales. Si está publicada en internet, un error de firmware o una contraseña filtrada alcanza para perder la central.",
         "como": "En System Settings > HTTP Server: Redirect From Port 80 en No, puerto 8089 u otro no estándar (nunca 80 ni 443) y lista blanca de hasta 10 IPs. SSH viene apagado y así se queda; GDMS Remote SSH solo durante un soporte; AMI no se habilita en una central expuesta. MFA está disponible para la web.",
         "ejemplo": "Un técnico de IES administra la central de un cliente en Salto desde la oficina en Montevideo: la IP fija de la oficina está en la lista blanca y la web no responde a nadie más."},
        {"name": "Geo-IP",
         "para_que": "La mayoría de los barridos vienen de países donde el cliente no tiene ni internos ni clientes. Geo-IP bloquea países enteros para los servicios de la central y achica la superficie de ataque de un saque.",
         "como": "En System Settings > Security Settings > Geo-IP Access Control se permiten solo los países que se usan. Antes de activarlo, conviene verificar que tu propia IP no quede bloqueada, sobre todo si estás conectado en remoto.",
         "ejemplo": "Una empresa con internos remotos solo en Uruguay y Argentina: Geo-IP permite esos dos países. Los intentos desde el resto del mundo ni llegan a Fail2ban."},
        {"name": "VPN o puertos abiertos para remotos",
         "para_que": "Los internos remotos obligan a decidir cómo llegan a la central. No hay una respuesta única: VPN reduce lo expuesto pero hay que mantenerla; los puertos abiertos son simples pero quedan a la vista.",
         "como": "Pocas sedes con IP fija: lista blanca por IP en el firewall. Muchos móviles y alguien que mantenga certificados: VPN. Si no hay ninguna de las dos: puerto no estándar configurado en la central, Fail2ban, Geo-IP y PIN en rutas caras. Un integrador con 15 años en FreePBX usa VPN siempre y cuenta caídas de 2 a 4 veces por año, casi siempre por certificados vencidos.",
         "ejemplo": "Una cadena con cuatro locales en el interior, todos con IP fija: lista blanca con esas cuatro IP. El vendedor que viaja con la app, en cambio, entra por VPN."},
    ],
    "teoria_md": """### Un poco de historia

Desde que las centrales pasaron a hablar SIP por internet, los barridos automáticos las buscan sin parar: programas que recorren rangos de IP, encuentran algo que responde en el 5060 y prueban extensiones y contraseñas. El objetivo casi siempre es el mismo, el fraude de peaje: llamar a destinos caros a cuenta del dueño de la central.

Fail2ban nació en el mundo Linux a mediados de los años 2000 como una idea simple: leer los registros de intentos fallidos y bloquear en el firewall a la IP que insiste. La UCM trae su propia versión integrada. Geo-IP usa bases que asocian rangos de direcciones a países, armadas a partir de las asignaciones de los registros regionales (LACNIC en el caso de Uruguay).

Los equipos también tienen fallas: el CVE-2025-28172 mostró que la UCM6510 hasta la 1.0.20.52 no limitaba los intentos de login. Por eso las defensas se superponen: ninguna alcanza sola.

### Cómo funciona

La UCM aplica sus defensas en este orden de prioridad, según su manual: defensa estática, Geo-IP estricto, defensa dinámica, Fail2Ban, ACL y Geo-IP no estricto. En la práctica, para un técnico se ordenan así, de afuera hacia adentro:

1. **Router**: solo están abiertos los puertos con nombre y motivo (por ejemplo `UDP 5060` y `UDP 10000-20000` para remotos). Lo que no está abierto ni llega.
2. **Geo-IP**: descarta países que no se usan.
3. **Fail2ban**: cuenta fallas de REGISTER, INVITE, SUBSCRIBE y de login, y banea 600 segundos de fábrica. La defensa dinámica, apagada de fábrica y solo en modo Route, bloquea por cantidad de conexiones (umbral 100).
4. **Administración**: la web solo para la lista blanca (hasta 10 IPs), 5 intentos fallidos de login dan 5 minutos de bloqueo, SSH y AMI apagados.
5. **Rutas**: si aun así alguien obtiene una extensión, el privilegio y el PIN impiden que llame afuera.

La tabla de puertos del router cierra el círculo: cada regla tiene destino, motivo y quién la pidió. Lo que nadie sabe para qué está, se cierra.""",
}

# =====================================================================================  12
M["12"] = {
    "fig": {"file": "12.svg", "alt": "El portero GDS3710, extensión 8001, manda REGISTER 8001 a la UCM 192.168.88.20 y al tocar timbre llama al 6000. La UCM hace sonar el Ring Group 6000 con los GRP de recepción y seguridad. Desde ahí vuelve al portero el PIN 4829# o la tecla OpenDoor, y la salida de alarma del portero mueve la cerradura en modo Open Door.",
            "caption": "Registro, timbre y apertura pasan por la central, con un PIN propio."},
    "steps": [
        {"file": "12-paso3.svg", "step": 3, "after": "Timbre y apertura:",
         "alt": "Web del GDS3710 en Door System Settings > Basic Settings: Doorbell Mode en Call Doorbell Number, Number Called When Door Bell Pressed 6000, Enable DTMF Open Door en Sí, Remote PIN to Open the Door 4829 de ejemplo y ALMOUT1 Feature en Open Door. A la derecha, la salida ALMOUT1 cableada a la cerradura. Aviso: si la salida no está en Open Door, el PIN se acepta y la puerta no se mueve.",
         "caption": "El timbre llama al grupo 6000 y el PIN abre por la salida que está en Open Door."},
        {"file": "12-paso4.svg", "step": 4, "after": "agregá el portero como acceso",
         "alt": "Web del GRP26xx en External Service > GDS con Service Type GDS, Account 1, System Number 8001 y Access Password 4829, igual al del GDS. Tabla: GRP2601 a 2604, 2612 y 2613 solo audio; 2614, 2615, 2616, 2624, 2634, 2636, 2650 y 2670 audio y video JPEG. Aviso: con RemoteConnect el MJPEG no anda en los GRP; para imagen conviene un GXV.",
         "caption": "El GRP necesita el número del portero y el mismo PIN; el modelo decide si muestra imagen."},
        {"file": "12-paso5.svg", "step": 5, "after": "Tocá el timbre, atendé, marcá el PIN",
         "alt": "Secuencia entre el GRP de recepción, la UCM y el GDS3710: tocan timbre y suena el 6000. A, atendés: marcás 4829# por DTMF RFC4733 y abre. B, sin atender: la tecla OpenDoor manda un mensaje SIP y abre. Aviso: probalo con la puerta abierta o alguien del lado de adentro.",
         "caption": "Se abre marcando el PIN durante la llamada o con OpenDoor sin atender."},
    ],
    "concepts": [
        {"name": "Portero como extensión",
         "para_que": "Un portero IP habla SIP como un teléfono. Registrarlo en la central en lugar de conectarlo directo a un solo teléfono permite que el timbre llame a un grupo, que se atienda desde cualquier interno y que quede registro en la central.",
         "como": "En la UCM se crea una extensión para el portero (8001) con contraseña aleatoria. En el GDS3710, Account 1 con SIP Server 192.168.88.20, User ID y Authenticate ID 8001 y la contraseña de esa extensión. Sin central, el GDS también puede llamar directo por IP a un GRP, pero solo a ese.",
         "ejemplo": "En un edificio de oficinas en el WTC, el portero de la entrada de servicio llama al grupo de seguridad: suena en la garita y en el teléfono del encargado, y atiende el que esté."},
        {"name": "Timbre a un grupo",
         "para_que": "Si el timbre llama a una sola interna y esa persona no está, nadie abre. Llamar a un grupo reparte la atención entre recepción, seguridad o quien corresponda.",
         "como": "En Door System Settings > Basic Settings, Doorbell Mode en Call Doorbell Number y en Number Called When Door Bell Pressed el número del grupo (6000). Las otras opciones del modo son controlar la salida de la puerta al tocar timbre o las dos cosas a la vez.",
         "ejemplo": "Una clínica en Pocitos: el timbre del acceso de proveedores llama al 6000, con la recepción y el depósito. Si la recepción está atendiendo a un paciente, abre el depósito."},
        {"name": "Apertura por DTMF y OpenDoor",
         "para_que": "Atender no alcanza: hay que poder abrir desde el teléfono. El GDS acepta dos caminos, el PIN durante la llamada o un mensaje directo desde la tecla del GRP.",
         "como": "Con Enable DTMF Open Door y Remote PIN to Open the Door, durante la llamada se marca el PIN seguido de # y el portero activa la salida configurada como Open Door (ALMOUT1). En el GRP, External Service > GDS con el número 8001 y el mismo PIN como Access Password: la tecla OpenDoor manda un mensaje SIP y abre, aun sin atender.",
         "ejemplo": "Llega un repartidor: la recepcionista ve la llamada del portero y toca OpenDoor sin atender. Si atiende para preguntar algo, marca su PIN y # y la puerta abre igual."},
        {"name": "PIN de apertura propio",
         "para_que": "El PIN de apertura es la llave de la puerta. Si es el de fábrica, el del buzón o uno obvio, cualquiera que llegue a marcarlo en una llamada con el portero abre.",
         "como": "Un PIN propio de 4 dígitos o más, distinto del de fábrica, del buzón y de cualquier interna. Va igual en el GDS y en el Access Password del GRP, y se anota en la ficha del cliente. Se prueba con la puerta abierta o con alguien adentro.",
         "ejemplo": "En la puesta en marcha de un depósito en Colón, el ejemplo de la guía (123456) queda reemplazado por un PIN que solo conocen el encargado y la ficha de IES."},
    ],
    "teoria_md": """### Un poco de historia

Los porteros eléctricos clásicos usaban sus propios cables y su propio teléfono en cada departamento u oficina. Con los porteros IP, el frente de calle pasó a ser un equipo SIP con cámara: puede llamar a cualquier teléfono de la central, y el que atiende puede abrir desde donde esté.

Para abrir se usan dos herramientas de SIP. La primera es el DTMF durante la llamada, que en la UCM viaja como evento RFC 4733 (2006), sucesora de la RFC 2833 (2000): el portero escucha los dígitos y, si forman el PIN, activa la salida. La segunda es el método MESSAGE, definido en la RFC 3428 en 2002 para mensajes instantáneos: la tecla OpenDoor del GRP manda un mensaje SIP al portero, sin necesidad de atender.

Grandstream integra el GDS3710 con sus teléfonos GRP en dos modos: directo por IP, sin central, o registrando el portero en la UCM como una extensión más. Un GRP puede tener hasta 10 porteros GDS37xx configurados.

### Cómo funciona

1. **Registro**. El GDS3710 registra la cuenta 8001 en la UCM como cualquier teléfono.
2. **Timbre**. Con Doorbell Mode en Call Doorbell Number, al tocar el botón llama al número configurado; si es un grupo (6000), la UCM hace sonar a todos sus miembros.
3. **Apertura con la llamada**. Quien atiende marca el PIN seguido de `#`. Con Enable DTMF Open Door, el GDS compara y, si coincide, activa la salida configurada como Open Door.
4. **Apertura sin atender**. En el GRP, el servicio GDS conoce el número del portero (System Number 8001) y el PIN (Access Password). La tecla OpenDoor manda un mensaje SIP con esos datos.

El video depende del teléfono: GRP2601 a 2604, 2612 y 2613 solo audio; GRP2614, 2615, 2616, 2624, 2634, 2636, 2650 y 2670 muestran imagen JPEG del portero. La UCM tiene además la opción Transparent Call-Info header para pasarle a ciertos GXP y GRP el pedido de video y la tecla de apertura. Si el portero entra por RemoteConnect, el MJPEG no funciona en los GRP y conviene un GXV para ver imagen.""",
}

out = "/home/claude/ies-training/ilustraciones/grandstream/manifest.json"
json.dump(M, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", out, len(M))
