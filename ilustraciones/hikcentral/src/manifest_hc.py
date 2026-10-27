"""Genera /home/claude/ies-training/ilustraciones/hikcentral/manifest.json (figuras, pasos, conceptos, teoría y figuras de teoría).

Al final valida: anclas `after` únicas en el laboratorio (fuera de bloques de código y en el paso correcto),
anclas de teoría únicas, 250 a 450 palabras de teoría, 2 a 4 conceptos y nada de guiones largos.
"""
import json, re, sys

M = {}

# =====================================================================================  1
M["1"] = {
    "fig": {"file": "1.svg",
            "alt": "Cuatro capas apiladas de una instalación HikCentral Professional, cada una con su síntoma típico al costado. Clientes (Web Client configura, Control Client opera, Mobile Client): error VSM217 cuando el Control Client es de otra versión. Streaming Server, en otra máquina y solo si hace falta: se suma con más de 200 cámaras. SYS más Streaming Gateway, resaltado, con gestión, usuarios, base de datos y video: puerto en rojo en Service Manager. Equipos (cámaras, NVR, controladoras): cámara offline en la plataforma. Abajo: el Streaming Gateway viene dentro del SYS y según el FAQ sirve hasta 200 cámaras reenviadas, por eso el Streaming Server va en otra máquina.",
            "caption": "Antes de diagnosticar, ubicá la capa: equipo, SYS, streaming o cliente."},
    "steps": [
        {"file": "1-paso3.svg", "step": 3, "after": "abrí Service Manager con clic derecho",
         "alt": "Planilla de ejemplo con cuatro filas: servicio, estado, puerto y lectura. SYS para la web de clientes en estado Exceptional con el puerto 80 en rojo, marcado como conflicto porque otro proceso tomó el puerto; SYS HTTPS en 443, Streaming Gateway RTSP en 554 y Streaming Gateway para vivo web en 559, todos bien. Notas: Service Manager se abre como administrador y un puerto en rojo es un conflicto; en producción, solo mirar y anotar.",
         "caption": "Servicio, estado y puerto de cada uno; el rojo marca un puerto tomado por otro programa."},
        {"file": "1-paso5.svg", "step": 5, "after": "Compará la versión del SYS",
         "alt": "Dos paneles. En verde, SYS V2.5.500 y Control Client V2.5.500: el login funciona, con vivo y alarmas. En rojo, SYS V2.5.500 y Control Client V2.4.1: el login falla con VSM217 y la solución es instalar el Control Client de la misma versión que el SYS. Nota: después de actualizar el SYS se actualiza el Control Client de cada puesto, y el Control Client no corre en una máquina virtual.",
         "caption": "Versión del SYS y del Control Client: si no son la misma, VSM217."},
    ],
    "concepts": [
        {"name": "SYS (System Management Service)",
         "para_que": "Es el corazón de HikCentral Professional: autentica usuarios, guarda roles, dispositivos y configuración en la base de datos y expone lo que usan los clientes. Se creó para que una sola plataforma gestione cámaras, NVR y controladoras que antes se manejaban equipo por equipo.",
         "como": "Se instala en un servidor Windows y se controla desde Service Manager, donde se ven sus servicios y puertos. Trae adentro un Streaming Gateway para reenviar video. Si el SYS no arranca, nada de lo de arriba funciona: por eso es la primera capa a revisar cuando todos los clientes fallan a la vez.",
         "ejemplo": "En un depósito en Canelones, ningún puesto puede entrar al Control Client. Antes de tocar las PC, abrís Service Manager en el servidor y ves el servicio del SYS en rojo: el problema está en esa capa, no en los puestos."},
        {"name": "Streaming Gateway y Streaming Server",
         "para_que": "Reenvían el video del equipo a los clientes, para que diez operadores mirando la misma cámara no le pidan diez flujos al NVR. El Gateway viene dentro del SYS; el Server se instala aparte cuando la carga crece.",
         "como": "Según el FAQ, el Gateway sirve hasta 200 cámaras reenviadas; por encima conviene un Streaming Server, que nunca va en la misma PC que el SYS. Usan el 554 para RTSP y el 559 para el vivo en Chrome y Firefox.",
         "ejemplo": "Un shopping con 260 cámaras y un centro de monitoreo: el SYS queda en un servidor y el Streaming Server en otro, y los puestos toman el video de este último."},
        {"name": "Web Client y Control Client",
         "para_que": "Separan configurar de operar. El Web Client, en el navegador, es donde se arma el sistema; el Control Client, programa instalado en el puesto, es donde se mira vivo, se mueve un PTZ, se reproduce y se atienden alarmas.",
         "como": "El Control Client tiene que ser exactamente de la misma versión que el SYS; si no, el login falla con VSM217. No corre en una máquina virtual. El Mobile Client acompaña desde el celular.",
         "ejemplo": "Actualizaste el SYS de un cliente el viernes y el lunes el monitoreo llama porque no entra nadie: los puestos siguen con el Control Client viejo. Se instala el de la versión nueva en cada PC y listo."},
    ],
    "teoria_md": """### Un poco de historia

Antes de las plataformas centrales, cada equipo Hikvision se administraba por separado: su web local o el software cliente iVMS-4200, que se conecta a cada cámara o NVR por el puerto de servidor, el 8000. Con diez equipos alcanza; con cien sitios, usuarios y alarmas que tienen que estar en un solo lugar, no.

HikCentral nació para eso, como una familia. HikCentral Professional es el producto grande, centrado en video y con acceso, alarmas, asistencia y mapas; HikCentral Lite y HikCentral Access Control cubren sitios chicos, y Connect y FocSign apuntan a la nube y a la cartelería. Professional tuvo una línea V1.x, después la V2.x (la documentación pide el doble de espacio en disco para pasar de una a otra) y hoy la V3.x. En el camino cambió piezas internas: el FAQ cuenta que la V2.3 pasó a un streaming server nuevo.

### Cómo funciona

La arquitectura se lee en capas. Abajo están los equipos: cámaras, NVR, controladoras. En el medio, el SYS (System Management Service), que autentica, guarda usuarios, roles y dispositivos en la base de datos y ofrece las APIs de configuración. El SYS trae incluido un Streaming Gateway que reenvía video.

El reenvío existe para que el equipo no atienda a todos los clientes. El cliente pide el vivo, el gateway toma el flujo de la cámara y lo reparte. Según el FAQ, el gateway alcanza hasta 200 cámaras reenviadas; por encima se instala un Streaming Server, siempre en otra máquina.

Arriba están los clientes. El Web Client funciona en el navegador (modelo B/S, navegador y servidor) y sirve para configurar. El Control Client es un programa instalado (modelo C/S, cliente y servidor) y sirve para operar. El Mobile Client va en el celular.

Cada capa falla a su manera. Un equipo offline es un problema de abajo; un servicio en rojo en Service Manager es del SYS; un vivo que no abre en Chrome suele ser el puerto 559 del gateway; un VSM217 es del cliente, porque su versión no coincide con la del SYS. Ubicar la capa antes de tocar nada ahorra la mitad del diagnóstico.""",
    "teoria_figs": [
        {"file": "1-t1.svg", "after": "El cliente pide el vivo, el gateway toma el flujo",
         "alt": "Animación en cuatro tiempos. 1: el Control Client inicia sesión en el SYS. 2: un operador pide el vivo de una cámara y el Streaming Gateway, dentro del SYS, abre un solo flujo contra la cámara. 3: el gateway reenvía ese flujo al primer cliente. 4: un segundo cliente pide la misma cámara y recibe el mismo flujo desde el gateway, sin abrir otra conexión contra la cámara. Al pie: hasta 200 cámaras reenviadas en el gateway; por encima, Streaming Server en otra máquina.",
         "caption": "El gateway toma una vez el video de la cámara y lo reparte entre los clientes."},
    ],
}

# =====================================================================================  2
M["2"] = {
    "fig": {"file": "2.svg",
            "alt": "Dos tarjetas con los perfiles de la guía de requisitos V2.4.510. Perfil bajo: CPU Intel Core i5-8500, 8 GB de RAM, NIC gigabit y disco de 650 GB como mínimo. Alto rendimiento: Xeon E-2314 o E-2378, 16 GB de RAM con 32 GB recomendados, NIC gigabit y 650 GB. Debajo, tres reglas: el SYS puede ir en máquina virtual, ESXi 6.x o 7.x o Hyper-V, en verde; el Control Client no corre en máquina virtual, en rojo; migrar la VM del SYS con vMotion o similar rompe la verificación de licencia, en rojo. Al pie: para V3.x, confirmar las cifras en la guía de esa versión.",
            "caption": "Perfil de hardware según la guía oficial, y qué puede y qué no puede ir virtualizado."},
    "steps": [
        {"file": "2-paso2.svg", "step": 2, "after": "Verificá el instalador antes de correrlo",
         "alt": "El instalador HikCentral_Professional.exe pasa por el comando Get-FileHash con algoritmo MD5. Abajo, dos casillas: el valor que da PowerShell y el valor publicado en la página de descarga de Hikvision. Si son iguales, nota verde: instalá como administrador. Si son distintos, nota roja: descarga cortada o archivo cambiado, bajalo de nuevo y volvé a comparar.",
         "caption": "Mismo hash que el publicado: recién ahí se instala."},
        {"file": "2-paso3.svg", "step": 3, "after": "instalación típica > Install Now",
         "alt": "Dos paneles. Instalación típica, en verde: en una sola PC quedan SYS, base de datos, Streaming Gateway y Control Client, todo menos el Streaming Server; sirve para el laboratorio y la mayoría de las obras. Instalación personalizada: se eligen módulos y carpetas, con SYS en la PC 1 y Streaming Server en la PC 2, nunca juntos; ahí también se decide Normal o Mirror Hot Spare. Nota ámbar: siempre clic derecho y Ejecutar como administrador; si el asistente pide reiniciar, reiniciá.",
         "caption": "Típica pone todo menos el Streaming Server en una PC; personalizada permite separar módulos."},
        {"file": "2-paso5.svg", "step": 5, "after": "Si un puerto aparece en rojo",
         "alt": "Persecución de un puerto tomado. netstat -ano filtrado por :80 devuelve una línea TCP 0.0.0.0:80 LISTENING con el PID 4321. Con tasklist filtrado por 4321 aparece el nombre del programa, otro-programa.exe. Dos salidas: A, cerrar el proceso con autorización del cliente, en ámbar; B, cambiar el puerto del servicio en Service Manager y entrar con el puerto en la URL, http://192.168.88.10:81.",
         "caption": "Del puerto al PID y del PID al programa; después, cerrarlo con permiso o mover el puerto."},
    ],
    "concepts": [
        {"name": "Dimensionar con la guía de requisitos",
         "para_que": "Un servidor que anda el día uno y se arrastra a los seis meses suele ser uno elegido a ojo. La guía de requisitos de Hikvision traduce cantidad de cámaras, puertas y eventos en CPU, RAM y disco.",
         "como": "Para V2.4.510, el perfil bajo es i5-8500, 8 GB y 650 GB; el alto, Xeon E-2314 o E-2378 con 16 GB, recomendando 32. La base de datos es PostgreSQL. El SYS puede ir en VM (ESXi 6.x o 7.x, Hyper-V), pero el Control Client no, y la VM del SYS no se migra en caliente porque rompe la licencia. Para V3.x conviene bajar la guía de esa versión.",
         "ejemplo": "Una obra con 40 cámaras y 6 puertas en una barraca de Montevideo: perfil bajo con margen de disco. Un parque industrial con varios cientos de cámaras y asistencia: perfil alto con 32 GB."},
        {"name": "Verificación por hash",
         "para_que": "Un instalador cortado a mitad de descarga, o cambiado en el camino, falla de formas raras y hace perder horas. Comparar el hash contra el publicado confirma que el archivo es el original.",
         "como": "En PowerShell, `Get-FileHash .\\HikCentral_Professional.exe -Algorithm MD5` da el valor; se compara con el de la página de descarga de Hikvision. Si coinciden, se instala con clic derecho y Ejecutar como administrador.",
         "ejemplo": "El instalador bajó por el WiFi de la obra y el asistente se cierra solo. El MD5 no coincide: lo bajás de nuevo por cable y el hash da igual."},
        {"name": "Service Manager y conflicto de puertos",
         "para_que": "Muestra cada servicio de HikCentral con su estado y su puerto, y permite arrancarlos, pararlos o cambiar el puerto. Es la primera pantalla para saber si el servidor está sano.",
         "como": "Se abre como administrador. Un puerto en rojo significa que otro proceso ya lo usa: `netstat -ano | findstr :80` da el PID y `tasklist | findstr <PID>` el programa. Con permiso del cliente se cierra ese programa, o se cambia el puerto del servicio y se entra con él en la URL.",
         "ejemplo": "En un servidor del cliente ya corría una web interna en el 80. El SYS queda en el 81 y los puestos entran a `http://192.168.88.10:81`."},
    ],
    "teoria_md": """### Un poco de historia

HikCentral Professional es software on-premises: corre en un servidor Windows del cliente o del integrador, con una base de datos PostgreSQL (la guía de requisitos V2.4.510 lista la versión 11.8). Esa decisión tiene costo y beneficio. VXG, un competidor que vende video en la nube, lo resume en contra: mantenimiento, actualizaciones, backups, seguridad y escala quedan del lado del integrador o del cliente. Hikvision trata el servidor propio como la base y admite AWS y Azure con limitaciones.

Por eso Hikvision publica, para cada versión, una guía de requisitos con perfiles de hardware y una lista de sistemas operativos y virtualizadores soportados. Y por eso el FAQ insiste en dos cosas viejas pero vigentes: instalar con permisos de administrador y verificar el MD5 del instalador. MD5 es un hash publicado en 1992; hoy se considera débil contra un atacante que fabrica colisiones, pero sigue sirviendo para detectar una descarga cortada o corrupta.

### Cómo funciona

Instalar es elegir dónde queda cada módulo. El paquete trae el servicio de gestión (SYS), el servicio de streaming, el Control Client y la base de datos. En modo típico se instala todo menos el Streaming Server en una sola PC; en modo personalizado se eligen módulos y carpetas, y se decide si el sistema es Normal o Mirror Hot Spare, con un servidor de respaldo. El SYS y el Streaming Server nunca van en la misma PC.

Cada servicio, al arrancar, pide al sistema operativo escuchar en un puerto: el 80 y el 443 para los clientes, el 554 y el 559 para el video. Un puerto lo puede escuchar un solo proceso a la vez. Si otro programa llegó antes, el servicio no consigue el puerto y Service Manager lo muestra en rojo.

La salida es averiguar quién lo tiene. `netstat -ano` lista los puertos en escucha con el PID del proceso dueño, y `tasklist` traduce ese PID a un nombre de programa. Con eso se decide: cerrar el programa, si el cliente lo autoriza, o mover el puerto del servicio en Service Manager y entrar con él en la URL, como `http://192.168.88.10:81`.

Service Manager además tiene Auto Recover Database Exception, para cortes de luz, con una ruta de archivo que necesita el doble del tamaño de la base libre.""",
    "teoria_figs": [
        {"file": "2-t1.svg", "after": "Si otro programa llegó antes, el servicio no consigue",
         "alt": "Animación en cuatro tiempos. 1: otro programa del servidor ya escucha en el puerto 80. 2: el servicio del SYS arranca, pide el puerto 80 y no lo consigue; Service Manager lo muestra en rojo como Exceptional. 3: netstat -ano da el PID 4321 y tasklist muestra el programa que lo tiene. 4: se cambia el puerto del SYS al 81, el servicio queda en verde y el navegador entra a http://192.168.88.10:81.",
         "caption": "Un puerto, un proceso: si otro llegó antes, el servicio queda en rojo hasta mover uno de los dos."},
    ],
}

# =====================================================================================  3
M["3"] = {
    "fig": {"file": "3.svg",
            "alt": "A la izquierda, en verde, tres bloques de expansión (cámaras, puertas, módulos) apilados sobre un bloque grande de licencia base. Debajo, en rojo, una expansión de cámaras sin base, con el error 1113. A la derecha, el panel online u offline: online, el SYS tiene internet y habla con el servidor de licencias, y sin salida aparece 1103; offline, archivo de pedido y de respuesta con una PC que sí tiene internet, dentro de las 24 horas. Recuadro ámbar: en los dos casos solo el usuario admin activa, actualiza o desactiva, y la hora del SYS tiene que ser correcta. Al pie: registrá el email del admin para recuperar el código.",
            "caption": "La base va primero; las expansiones suman sobre ella, online u offline."},
    "steps": [
        {"file": "3-paso5.svg", "step": 5, "after": "En una PC con internet, entrá a kms.hikvision.com",
         "alt": "Ida y vuelta de la activación offline entre el SYS sin internet, 192.168.88.10, y una PC con internet en kms.hikvision.com: va ActivationRequestFile.bin y vuelve ActivationResponseFile.bin, en un pendrive. Cuatro pasos numerados: Generate Request File con un solo clic, porque un segundo clic invalida el primer pedido; subir el pedido; bajar la respuesta de ese pedido; Import y Activate, cargando el email del admin. Notas ámbar: todo dentro de las 24 horas o falla con 1105; con más de 24 horas de diferencia en la hora del SYS, falla con Operation timeout.",
         "caption": "Un pedido, una respuesta y menos de 24 horas entre los dos."},
        {"file": "3-paso6.svg", "step": 6, "after": "Armá la ficha de licencia de la obra",
         "alt": "Tabla de códigos de activación del FAQ V2.5.500. 1103: el SYS no llega al servidor de licencias o está caído; revisar internet o pasar a offline. 1105: la respuesta no corresponde al pedido o pasaron 24 horas; generar un pedido nuevo con un solo clic. 1108: código ya usado en otro SYS; desactivar primero en el servidor viejo. 1113: expansión sin licencia base; activar primero la base. 1114: se modificó la hora del SYS; volver a la hora correcta. 1116: más recursos que los licenciados; licenciar según los recursos actuales. Nota: 1108 también aparece si la versión de la licencia no corresponde a la del sistema.",
         "caption": "Cada código apunta a una causa concreta; anotalo en la ficha de la obra."},
    ],
    "concepts": [
        {"name": "Licencia base y expansiones",
         "para_que": "HikCentral se licencia por partes: una licencia base habilita el sistema y las expansiones suman capacidad o funciones (cámaras, puertas, módulos). Así se compra lo que la obra necesita y se crece después.",
         "como": "Primero se activa al menos una base; recién después, las expansiones. Al revés da error 1113. Solo el usuario admin activa, actualiza o desactiva. Recién instalado trae una licencia temporal limitada, y cuando conviven una de prueba y una de venta, manda la de venta.",
         "ejemplo": "Un colegio en Maldonado arranca con base y 32 cámaras; al año suma 8 puertas con una expansión, sobre la misma base y sin reinstalar nada."},
        {"name": "Activación offline",
         "para_que": "Muchos servidores de seguridad no tienen salida a internet, por diseño. La activación offline permite licenciarlos igual, llevando un archivo de pedido y uno de respuesta en un pendrive.",
         "como": "En el Web Client se carga el código (16 o 32 caracteres, sin guiones), se elige Physical Machine, AWS o Azure, y con un solo clic se genera ActivationRequestFile.bin. En una PC con internet se sube a kms.hikvision.com, se baja ActivationResponseFile.bin y se importa. Todo dentro de las 24 horas; un segundo clic en Generate invalida el primer pedido y termina en 1105.",
         "ejemplo": "El SYS de un frigorífico vive en una red aislada. El técnico genera el pedido, lo activa desde la notebook con 4G en el estacionamiento y vuelve con la respuesta en veinte minutos."},
        {"name": "La hora del servidor y la licencia",
         "para_que": "La licencia se valida con fechas: el pedido offline vence a las 24 horas y el sistema detecta si alguien tocó el reloj. La hora correcta no es un detalle: es parte del licenciamiento.",
         "como": "Antes de activar se revisa con `w32tm /query /status` y `Get-Date`. Con más de 24 horas de diferencia con la hora real, la activación offline falla con Operation timeout; si la hora del SYS fue modificada, aparece 1114.",
         "ejemplo": "Un servidor recién armado quedó con la fecha de fábrica de la placa. La activación falla; se sincroniza la hora y la segunda vez entra."},
    ],
    "teoria_md": """### Un poco de historia

La activación por pedido y respuesta es un esquema viejo del software comercial: el programa genera un archivo que identifica la instalación, el fabricante lo firma y devuelve otro que la habilita. Sirve igual con internet que sin ella, porque el archivo puede viajar en un pendrive. HikCentral lo usa con su portal de licencias, kms.hikvision.com.

El modelo de base más expansiones también tiene lógica de negocio: una base habilita la plataforma y cada expansión suma cámaras, puertas o módulos. El FAQ V2.5.500 dedica un capítulo entero a los errores de activación, del 1103 al 1116, y a la licencia que no toma efecto: cuando conviven una licencia de prueba y una de venta, solo manda la de venta.

### Cómo funciona

La licencia se ata a la instalación. Al activar se elige el entorno: Physical Machine, AWS o Azure. En máquina física queda atada al hardware: si el hardware cambia, se invalida. Por eso, antes de tocar el servidor, se desactiva.

Online, el SYS habla directo con el servidor de licencias. Si no tiene salida a internet, o el servidor de licencias no responde, aparece 1103 y se pasa a offline.

Offline, el flujo tiene cuatro tiempos. En el Web Client se carga el código y se genera ActivationRequestFile.bin, con un solo clic: cada clic genera un pedido nuevo y deja inválido el anterior. Ese archivo viaja a una PC con internet, que lo sube a kms.hikvision.com y baja ActivationResponseFile.bin. La respuesta vuelve al SYS y se importa. Si la respuesta no corresponde a ese pedido, o pasaron más de 24 horas, el sistema la rechaza con 1105: "Operation is out of sequence".

La hora es parte del mecanismo. Si el reloj del SYS difiere más de 24 horas de la hora real, la activación offline falla por tiempo. Si la hora fue modificada, aparece 1114.

Los demás códigos cuentan la historia de la instalación: 1108 dice que el código ya se usó en otro SYS, o que la licencia es de otra versión; 1113, que se intentó una expansión sin base; 1116, que hay más recursos agregados que los licenciados. Al activar se registra el email del admin, que sirve para recuperar el código si se pierden la contraseña y el código a la vez.""",
    "teoria_figs": [
        {"file": "3-t1.svg", "after": "Offline, el flujo tiene cuatro tiempos",
         "alt": "Animación en cuatro tiempos con un reloj de 24 horas que corre. 1: el SYS sin internet genera ActivationRequestFile.bin con un solo clic. 2: el archivo viaja en un pendrive a una PC con internet y se sube a kms.hikvision.com. 3: el portal devuelve ActivationResponseFile.bin. 4: la respuesta vuelve al SYS, se importa y la licencia queda activa antes de que el reloj llegue a 24 horas. Al pie: un segundo clic en Generate o una respuesta vieja terminan en 1105.",
         "caption": "Pedido y respuesta tienen que ser del mismo par y volver antes de las 24 horas."},
    ],
}

# =====================================================================================  4
M["4"] = {
    "fig": {"file": "4.svg",
            "alt": "Cinco pasos en fila: 1, backup ahora con Back Up Now; 2, copia afuera en otra máquina, verificada; 3, desactivar licencia online u offline; 4, resaltado, cambiar o migrar disco, servidor o VM; 5, reactivar y revisar licencia y servicios. Debajo, dos paneles rojos. Si cambiás hardware sin desactivar: en máquina física la licencia queda atada al hardware y se invalida, el SYS alterna entre Starting y Stopped en Service Manager y en el servidor nuevo el código da 1108. Si el backup quedó solo en el SYS: el backup programado se guarda en el propio servidor y si muere el disco se lleva todo, por eso se copia a otra máquina y se prueba. Al pie: migrar la VM del SYS con vMotion o similar también rompe la licencia.",
            "caption": "Backup afuera y licencia desactivada antes de cualquier cambio en el servidor."},
    "steps": [
        {"file": "4-paso2.svg", "step": 2, "after": "En Type marcá configuración",
         "alt": "Ventana Back Up and Restore System Data, pestaña Back Up: Type con configuración, imágenes, eventos y pasadas; How Often semanal; When domingo 03:00; Max. Number of Backups 5, resaltado; botón Save and Back Up Now. A la derecha, cinco copias semanales en verde; cuando sale la sexta, la más vieja se borra. Nota ámbar: las cinco copias viven en el servidor SYS y sirven para volver una semana atrás, no para sobrevivir a un disco muerto. Ruta del manual V2.6.1; en V3.x el menú puede llamarse distinto.",
         "caption": "Cinco copias semanales que rotan solas, todas dentro del SYS."},
        {"file": "4-paso3.svg", "step": 3, "after": "Copiá la carpeta de backups a otra máquina",
         "alt": "El SYS, con la carpeta D:\\HikCentral\\Backup, copia por la red a otra máquina en \\\\192.168.88.20\\backups\\hcp con robocopy. Debajo, el comando completo y una tabla: /E copia subcarpetas incluidas las vacías, /R:2 reintenta dos veces, /W:5 espera cinco segundos entre reintentos. La ruta de origen es de ejemplo. Al pie: abrí la carpeta de destino y fijate que estén los archivos de hoy.",
         "caption": "El backup sirve cuando también existe fuera del servidor."},
    ],
    "concepts": [
        {"name": "Licencia atada al hardware",
         "para_que": "La licencia de HikCentral identifica el servidor donde se activó, para que un mismo código no se use en varias instalaciones. El costo es que un cambio de hardware la invalida.",
         "como": "En máquina física, cambiar placa o disco puede romper la detección: el SYS alterna entre Starting y Stopped en Service Manager. Migrar la VM del SYS con vMotion o similar también rompe la verificación. La salida limpia es desactivar antes, en el servidor viejo, y activar después en el nuevo; si no, el nuevo da 1108.",
         "ejemplo": "Un cliente cambia el servidor por uno más grande. Con la licencia desactivada antes de apagar el viejo, el nuevo activa a la primera. Sin eso, hay que pedir ayuda al soporte para liberar el código."},
        {"name": "Backup del sistema",
         "para_que": "Guarda la configuración y los datos de la plataforma (dispositivos, áreas, personas, eventos, pasadas) para poder volver atrás o rearmar el sistema en otro servidor.",
         "como": "Se programa en Back Up and Restore System Data: qué tipos, cada cuánto y cuántas copias, de 1 a 5. Esas copias quedan en el propio servidor SYS, así que se copian afuera, por ejemplo con `robocopy`, y se prueba que la copia exista. Antes de un cambio, además, Save and Back Up Now.",
         "ejemplo": "Muere el disco del servidor de un hotel en Punta del Este. Con el backup del domingo en el NAS de IES, el sistema nuevo queda con las mismas áreas, personas y niveles de acceso."},
        {"name": "Checklist de cambio",
         "para_que": "Un cambio en el servidor tiene pasos que no se pueden hacer en otro orden. Escribirlos evita el clásico \"apagué y después me acordé de la licencia\".",
         "como": "Uno: backup ahora. Dos: copia fuera del SYS, verificada. Tres: licencia desactivada, solo quien tiene los códigos y el visto bueno del cliente. Cuatro: cambiar o migrar. Cinco: reactivar y revisar Service Manager. Se pega en la carpeta de la obra.",
         "ejemplo": "El cliente pide pasar el SYS de una PC de escritorio a un servidor en rack. El técnico sigue la lista en voz alta con el encargado de IT y el cambio se hace en una ventana de una hora un sábado."},
    ],
    "teoria_md": """### Un poco de historia

Atar una licencia al hardware es una técnica clásica del software comercial: al activar, el programa calcula una huella del equipo y el fabricante la registra con el código. Si la huella cambia, la licencia deja de valer. Protege al fabricante contra copias, y le traslada al integrador una regla: antes de tocar el hardware, liberar la licencia.

La virtualización agregó un caso. Mover una máquina virtual en caliente de un servidor físico a otro es una función común de VMware (vMotion) y de otros hipervisores. Para HikCentral, según la guía de requisitos V2.4.510, esa migración rompe la verificación de licencia, y tampoco se soporta la VM en modo clúster.

La copia de seguridad tiene una regla igual de vieja: un backup que vive en el mismo disco que los datos no es un backup. `robocopy`, la herramienta de Windows para copiar carpetas con reintentos, viene incluida en el sistema desde Windows Vista y Server 2008.

### Cómo funciona

El SYS revisa la licencia al arrancar. Si el hardware cambió, la detección falla y el servicio no logra quedar arriba: en Service Manager se ve alternando entre Starting y Stopped. El FAQ da la salida de emergencia (parar servicios, limpiar y volver a actualizar la licencia), pero el camino limpio es otro: desactivar primero.

Desactivar le avisa al servidor de licencias que ese código queda libre. Después se cambia el hardware o se migra, y en el destino se activa de nuevo. Si no se desactivó, el destino recibe 1108: el código figura usado en otro SYS.

El backup del sistema se arma en Back Up and Restore System Data. Se elige qué guardar (configuración, imágenes, eventos y alarmas, pasadas), cada cuánto y cuántas copias conservar, de 1 a 5. Cuando se llega al máximo, la copia nueva desplaza a la más vieja. Todas quedan en el servidor SYS: si el disco muere, se las lleva.

Por eso el procedimiento completo tiene dos movimientos. Adentro, el backup programado y uno manual antes de cada cambio. Afuera, una copia en otra máquina, por ejemplo con `robocopy` hacia una carpeta compartida, y una mirada a la carpeta de destino para confirmar que llegó. Algunas imágenes de módulos específicos se pierden en backup y restauración, según el FAQ: si la obra los usa, se guardan antes.""",
    "teoria_figs": [
        {"file": "4-t1.svg", "after": "Desactivar le avisa al servidor de licencias",
         "alt": "Animación en dos recorridos. Recorrido con error: se cambia el hardware del SYS sin desactivar, la huella ya no coincide, el SYS alterna entre Starting y Stopped y en el servidor nuevo el código da 1108. Recorrido correcto: backup copiado afuera, licencia desactivada y liberada en el servidor de licencias, cambio de hardware, activación en el servidor nuevo y servicios en verde.",
         "caption": "Desactivar antes libera el código; sin eso, el servidor nuevo lo encuentra ocupado."},
    ],
}

# =====================================================================================  5
M["5"] = {
    "fig": {"file": "5.svg",
            "alt": "Tres columnas que muestran quién abre la conexión. Por IP o dominio: el SYS, 192.168.88.10, entra a la cámara o NVR, 192.168.88.21; hace falta IP fija y ruta al equipo; puerto 8000, o 8443 cifrado. Por ISUP, ex EHome, en verde: la cámara sin IP fija se registra en el SYS, que escucha el 7660, con Device ID y clave; alcanza con que el equipo tenga salida. Por Hik-Connect, en ámbar: el equipo y el SYS pasan por la nube, con serie y código de verificación, y esos equipos no graban en Hybrid SAN ni Cloud Storage. Al pie: IP fija, por IP; sin IP fija, ISUP; Hik-Connect solo si aceptás sus límites; ONVIF para otras marcas; no abrir el 8000 ni el 80 a internet.",
            "caption": "La diferencia de fondo es quién inicia la conexión: el SYS, el equipo o la nube."},
    "steps": [
        {"file": "5-paso2.svg", "step": 2, "after": "Platform Access, tipo ISUP",
         "alt": "Dos ventanas lado a lado. En la cámara, Platform Access: tipo ISUP, Server address 192.168.88.10, Port 7660, Device ID LAB-CAM-01, Key Ejemplo.2026!. En HikCentral, Add Encoding Device: Access Protocol Hikvision ISUP, Adding mode Device ID, Device ID LAB-CAM-01, clave ISUP 5.0 Ejemplo.2026!, Add Resource to Area activado. Líneas verdes unen Device ID con Device ID y clave con clave: iguales. Notas: antes, en el SYS, Allow ISUP Registration en System, Network, Device Access Protocol; la cámara llama hacia el 7660 y no hace falta abrir nada hacia ella. Rutas de menú de V2.x.",
         "caption": "Device ID y clave tienen que ser idénticos en la cámara y en HikCentral."},
        {"file": "5-paso5.svg", "step": 5, "after": "Si no aparece online, probá el puerto",
         "alt": "Cuatro chequeos numerados: Allow ISUP Registration activado en el SYS; Device ID idéntico en la cámara y en HikCentral; la misma clave ISUP de los dos lados; puerto 7660 alcanzable desde la red de la cámara. A la derecha, el comando Test-NetConnection 192.168.88.10 -Port 7660 con dos salidas: TcpTestSucceeded True si llega, False si no llega. Nota ámbar: con False el problema está en el camino, firewall, ruta o VPN, no en la cámara. Nota: probalo desde una PC de la red de la cámara.",
         "caption": "Cuatro cosas para revisar, y una prueba de puerto que separa red de configuración."},
    ],
    "concepts": [
        {"name": "Alta por IP con el protocolo privado",
         "para_que": "Es la forma directa: el SYS se conecta al equipo por su IP o dominio, como lo hacía el iVMS-4200, por el puerto de servidor. Sirve cuando el equipo tiene IP fija y el servidor tiene ruta hasta él.",
         "como": "Access Protocol: Hikvision Private Protocol, puerto 8000 por defecto, u 8443 si se marca Encrypted Add. Para equipos de otras marcas, ONVIF. Conviene configurar NTP antes: el propio asistente avisa si falta. El 8000 no se abre a internet: si hay sitios remotos, se llega por VPN.",
         "ejemplo": "Un NVR en la misma LAN del servidor de una fábrica en Paysandú, 192.168.88.21: se agrega por IP al 8000 y aparece online en segundos."},
        {"name": "ISUP (ex EHome)",
         "para_que": "Resuelve el sitio sin IP fija o detrás de NAT: en vez de que el servidor salga a buscar al equipo, el equipo se registra en el servidor. El manual lo presenta como la opción costo efectiva para equipos sin IP fija.",
         "como": "En el SYS se habilita Allow ISUP Registration. En el equipo, Platform Access tipo ISUP con la dirección del SYS, puerto 7660, un Device ID y una clave (ISUP 5.0 la exige). En HikCentral se agrega por Device ID con los mismos datos. El equipo inicia la conexión, así que no hace falta abrir puertos hacia él.",
         "ejemplo": "Una cadena de farmacias con un NVR por local y conexiones de fibra sin IP fija: cada NVR se registra por ISUP contra el SYS central, que es el único con el 7660 publicado."},
        {"name": "Hik-Connect DDNS y sus límites",
         "para_que": "Es el atajo para equipos con IP dinámica que ya usan la nube de Hikvision: se agregan con número de serie y código de verificación, o en lote desde la cuenta Hik-Connect.",
         "como": "Requiere el servicio Hik-Connect habilitado en el equipo y salida a internet. El costo está en la grabación: equipos agregados por Hik-Connect o por dominio no graban en Hybrid SAN ni en Cloud Storage. Si la obra pide grabación central, el alta va por IP o ISUP.",
         "ejemplo": "Un local chico con un DVR que el cliente ya mira desde la app: se suma a HikCentral por Hik-Connect para ver el vivo, sabiendo que la grabación queda en el DVR."},
    ],
    "teoria_md": """### Un poco de historia

Las cámaras IP nacieron en redes donde el que mira y el que filma estaban en la misma LAN. Con los años, los sitios se llenaron de conexiones de internet con IP dinámica y NAT, que traduce las direcciones privadas a una pública y no deja entrar conexiones nuevas desde afuera. La respuesta casera fue el port forwarding: abrir en el router el 80, el 554 y el 8000 del equipo. Hay blogs de instaladores que todavía lo enseñan paso a paso, y es justo lo que conviene evitar.

Hikvision fue por otro lado. Además del protocolo privado de siempre (el del puerto 8000, el que usa el iVMS-4200), creó EHome, hoy llamado ISUP, para que el equipo sea el que llama. La Communication Matrix muestra los puertos de ISUP desde HikCentral V1.4. Y sumó Hik-Connect, su nube, con servicio de dominio para equipos con IP dinámica.

### Cómo funciona

El alta por IP es una conexión que arranca en el SYS: el servidor abre una sesión TCP contra el 8000 del equipo (8443 con Encrypted Add) y desde ahí pide video, eventos y configuración. Funciona si el SYS tiene ruta al equipo: misma LAN, o una VPN entre sitios.

ISUP da vuelta la dirección. El equipo, configurado con la IP del SYS, el puerto 7660, un Device ID y una clave, abre la conexión hacia afuera. Para el router del sitio es una salida más, como navegar, así que pasa el NAT sin abrir nada. El SYS valida el Device ID y la clave, registra el equipo y usa ese canal para comandos; el video y los archivos tienen sus propios puertos en la matriz (16000 y 16001 para stream, 8555 para archivos). Solo el lado central publica puertos.

Hik-Connect agrega un intermediario: equipo y plataforma se encuentran a través de la nube de Hikvision, identificando el equipo por número de serie y código de verificación. Es cómodo, pero trae límites documentados en el FAQ, como no poder grabar en Hybrid SAN ni en Cloud Storage.

La regla de decisión sale de ahí: con IP fija y ruta, por IP; sin IP fija, ISUP; Hik-Connect cuando se aceptan sus límites. Y para cámaras de otras marcas, ONVIF, el estándar que fundaron Axis, Bosch y Sony en 2008.""",
    "teoria_figs": [
        {"file": "5-t1.svg", "after": "ISUP da vuelta la dirección",
         "alt": "Animación en cuatro tiempos con un router con NAT entre la cámara y el SYS. 1: el SYS intenta entrar por IP al 8000 de la cámara y el NAT del router corta la conexión entrante. 2: la cámara, con ISUP, abre la conexión hacia afuera, al 7660 del SYS, y el router la deja salir. 3: el SYS valida Device ID y clave y la cámara queda registrada. 4: por esa misma sesión el SYS le pide video y eventos; la cámara queda online sin ningún puerto abierto en el router del sitio.",
         "caption": "Con ISUP la cámara llama hacia afuera, y el NAT del sitio deja de ser un problema."},
    ],
}

# =====================================================================================  6
M["6"] = {
    "fig": {"file": "6.svg",
            "alt": "Dos paneles con el mismo NVR del depósito, online en Device. En rojo, agregado sin importar a un área: sus canales quedan sin ubicar y no hay vivo, ni reproducción, ni eventos y alarmas. En verde, con los canales importados al área Nave 1, CAM-01 a CAM-04 y la Puerta N1: vivo, reproducción y eventos funcionan. Al pie: en el alta activá Add Resource to Area, o importá los canales desde el área; el árbol de áreas se diseña antes de dar de alta el primer equipo.",
            "caption": "Un equipo online sin área no tiene vivo, reproducción ni eventos."},
    "steps": [
        {"file": "6-paso5.svg", "step": 5, "after": "Doble clic en Depósito",
         "alt": "Árbol de áreas: Sitio Ejemplo, con Depósito, resaltado y sin cámaras propias, que tiene las hijas Nave 1, CAM-01 a 04, y Nave 2, CAM-05 a 08; y Oficinas, CAM-09 a 10. Doble clic en Depósito muestra There is no camera in this area, porque las ocho cámaras están en las hijas. Doble clic en Nave 1 muestra el vivo de las cuatro cámaras de la nave. Al pie: cada recurso va en el área donde el operador lo busca.",
         "caption": "El área madre no muestra las cámaras de sus hijas."},
        {"file": "6-paso6.svg", "step": 6, "after": "cargá un plano JPG de la planta",
         "alt": "Dos paneles. E-map: imagen estática con el plano de la planta, Nave 1, Nave 2 y Oficinas, con cámaras como puntos calientes; se carga un JPG del plano y se ubica cada cámara. GIS: mapa geográfico con calles y puntos, con datos en tiempo real, para sitios repartidos en una ciudad o una ruta. Nota: una cámara entra una sola vez en cada mapa y puede ser punto caliente en hasta 6 mapas.",
         "caption": "E-map para un plano fijo; GIS para un mapa geográfico vivo."},
    ],
    "concepts": [
        {"name": "Área",
         "para_que": "Es la unidad con la que HikCentral ordena todo: cámaras, puertas, entradas de alarma y mapas. Se creó para que el operador encuentre los recursos como encuentra el edificio, y para dar permisos por zona.",
         "como": "Se arma un árbol (sitio, edificio, piso, sector) y cada canal se importa al área donde se usa, con Add Resource to Area al dar de alta o con Import en el área. Un recurso que no está en ningún área no tiene vivo, reproducción ni eventos, y las cámaras de un área hija no aparecen al abrir la madre.",
         "ejemplo": "Un hospital en Montevideo: áreas por edificio y piso. El guardia de Emergencia abre su piso y ve sus cámaras y sus puertas, sin recorrer una lista de 300 canales."},
        {"name": "Vista pública y vista privada",
         "para_que": "Una vista es un mosaico guardado de cámaras. Sirve para que el puesto de monitoreo abra siempre lo mismo y cada operador tenga, además, sus propias combinaciones.",
         "como": "La vista pública la ve cualquier usuario; la privada, solo quien la creó. Los grupos de vistas permiten rotación automática en el Control Client. Se arman en Monitoring, con las cámaras ya ubicadas en sus áreas.",
         "ejemplo": "En un supermercado de Las Piedras, la vista pública Cajas de 9 ventanas queda para el turno; el jefe de seguridad tiene una privada con depósito y estacionamiento."},
        {"name": "E-map y GIS",
         "para_que": "Ponen las cámaras y alarmas sobre un mapa, para que el operador vea dónde pasa lo que pasa. E-map es para planos fijos; GIS, para mapas geográficos con datos en tiempo real.",
         "como": "En E-map se carga una imagen del plano y cada cámara se ubica como punto caliente. En GIS se trabaja sobre un mapa geográfico. Según el FAQ, una cámara entra una sola vez por mapa y en hasta 6 mapas.",
         "ejemplo": "Una intendencia con cámaras en varias plazas del departamento usa GIS para ubicarlas; un shopping usa un E-map por nivel."},
    ],
    "teoria_md": """### Un poco de historia

Ordenar cámaras en un árbol es casi tan viejo como el video sobre IP: cuando un sistema pasó de dieciséis cámaras a cientos, la lista plana se volvió inmanejable. Los VMS adoptaron árboles de sitios y zonas, y HikCentral los llama áreas.

Los mapas tienen dos linajes. El plano del edificio con íconos encima viene de los paneles de alarma y de las primeras centrales de monitoreo. El mapa geográfico viene de los sistemas de información geográfica, GIS, una idea que Roger Tomlinson impulsó en Canadá en los años sesenta para gestionar datos sobre el territorio. HikCentral los ofrece por separado: E-map para planos, GIS para geografía.

### Cómo funciona

Un equipo agregado y un recurso utilizable no son lo mismo. Al dar de alta un NVR, HikCentral conoce el equipo, pero sus canales todavía no están en ningún lado. Recién cuando se importan a un área existen para el operador: tienen vivo, reproducción, eventos y permisos. El manual lo dice sin vueltas: si no se importan los canales a un área, no hay vivo, reproducción ni configuración de eventos.

El área es además la unidad de los permisos. Un rol dice qué áreas ve un usuario, y con eso ve sus cámaras, sus puertas y sus alarmas. Por eso conviene diseñar el árbol en papel antes del primer alta: el mismo dibujo después define quién ve qué.

La regla que más confunde: cada recurso pertenece a un área concreta. Las cámaras de un área hija no aparecen al abrir la madre, y el Control Client lo avisa con "There is no camera in this area". Si el operador busca en Depósito, las cámaras van en Depósito; si busca en Nave 1, en Nave 1.

Sobre esas áreas se construye la operación. Las vistas guardan mosaicos de cámaras: públicas para el puesto, privadas para cada operador. Los mapas muestran los recursos en su lugar: un E-map es una imagen fija, un plano de planta cargado como JPG, con cada cámara como punto caliente; un GIS es un mapa geográfico con datos en tiempo real. Una cámara entra una sola vez por mapa y puede estar en hasta seis.""",
    "teoria_figs": [
        {"file": "6-t1.svg", "after": "El área es además la unidad de los permisos",
         "alt": "Animación en cuatro tiempos. 1: un NVR de ocho canales queda agregado y online, con los canales en gris, sin área. 2: los canales 1 a 4 se importan al área Nave 1 y los 5 a 8 al área Nave 2. 3: el operador con rol de Nave 1 abre su vista y aparecen solo las cuatro cámaras de esa nave. 4: abre el área madre Depósito y ve el aviso There is no camera in this area, porque las cámaras están en las hijas.",
         "caption": "Importar a un área es lo que convierte un canal en algo que el operador puede ver."},
    ],
}

# =====================================================================================  7
M["7"] = {
    "fig": {"file": "7.svg",
            "alt": "A la izquierda, la sucursal: CAM-01, dada de alta por IP, graba en el NVR del sitio, resaltado en verde porque no depende del enlace al centro. Un cable marcado enlace al centro lleva al centro, con cuatro opciones de almacenamiento central: pStor, servicio que administra discos de un servidor; pStor Cluster, varios pStor juntos; Hybrid SAN, equipo de almacenamiento de Hikvision; Cloud Storage Server. En el medio: el video viaja por el enlace, si es chico o inestable, mejor en el sitio. Notas: por dominio o Hik-Connect no se graba en Hybrid SAN ni Cloud Storage y pStor Cluster no hace grabación por movimiento; se decide por cámara, por escrito, antes del alta, y cambiarla después no mueve el video viejo.",
            "caption": "Grabar en el sitio no depende del enlace; grabar en el centro sí, y cada opción tiene límites."},
    "steps": [
        {"file": "7-paso2.svg", "step": 2, "after": "Revisá cada fila contra los límites",
         "alt": "Tabla de grabación con chequeo: CAM-01, alta por IP, graba en NVR del sitio, válido; CAM-02, ISUP, NVR del sitio, válido; CAM-09, IP, pStor central, válido; CAM-05, fila de ejemplo resaltada, Hik-Connect a Hybrid SAN, no se soporta, con cruz roja. Notas: si el alta es por dominio o Hik-Connect, la grabación no puede ir a Hybrid SAN ni Cloud Storage; se arregla cambiando el alta a IP o ISUP o grabando en el NVR del sitio, y por dominio solo graba en el propio equipo.",
         "caption": "La columna Alta por limita lo que puede decir la columna Graba en."},
        {"file": "7-paso3.svg", "step": 3, "after": "abrí la configuración de grabación",
         "alt": "El NVR del sitio, que ya tiene su calendario, pasa ese calendario a la configuración de grabación de HikCentral con la opción Get Device's Recording Settings. Debajo, dos calendarios de ejemplo iguales, de lunes a domingo: el del NVR y el que queda en HikCentral. Nota ámbar: sin esa opción, una plantilla de la plataforma puede pisar el calendario del NVR.",
         "caption": "Get Device's Recording Settings copia el calendario del NVR en lugar de pisarlo."},
    ],
    "concepts": [
        {"name": "Grabación en el equipo",
         "para_que": "Que el video quede en el NVR o en la tarjeta de la cámara, en el mismo sitio donde se filma. Así la grabación no depende del enlace con el centro ni del servidor central.",
         "como": "Al dar de alta se elige que grabe en el equipo, con su calendario. Con Get Device's Recording Settings, HikCentral toma el calendario que ya tenía el NVR en lugar de pisarlo. La reproducción desde los clientes sí usa el enlace, pero solo cuando alguien la pide.",
         "ejemplo": "Una sucursal en Rivera con 20 Mbps hacia Montevideo: las cámaras graban en el NVR del local y el centro solo trae video cuando el operador reproduce algo."},
        {"name": "Almacenamiento central",
         "para_que": "Concentrar la grabación en el centro, para dar retención larga y redundancia que un NVR de sitio no tiene. HikCentral ofrece pStor, pStor Cluster, Hybrid SAN y Cloud Storage Server.",
         "como": "El video viaja continuo por el enlace hasta el almacenamiento central, así que hace falta ancho de banda sostenido. Cada opción tiene límites del FAQ: por dominio o Hik-Connect no se graba en Hybrid SAN ni en Cloud Storage; pStor Cluster no hace grabación por movimiento; pStor, clúster y SYS van en el mismo dominio de red y la misma zona horaria.",
         "ejemplo": "Un banco que pide 90 días de retención para las cámaras de cajas, todas en la casa central: graban en pStor en el datacenter, a pocos metros."},
        {"name": "Tabla de grabación por cámara",
         "para_que": "Decidir antes del alta, y por escrito, dónde graba cada cámara y por qué. Evita descubrir semanas después que una cámara nunca grabó o que su histórico quedó en otro lado.",
         "como": "Una fila por cámara: alta por, graba en, motivo. Cada fila se chequea contra los límites. Después, en Maintenance, se busca el estado de grabación de los recursos y se anotan las que no graban. Cambiar la ubicación en producción no mueve el video viejo.",
         "ejemplo": "En la entrega de una obra, la tabla va al cliente junto con el plano: quien herede el sistema sabe dónde buscar cada grabación."},
    ],
    "teoria_md": """### Un poco de historia

La grabación de video pasó por varias casas. Primero el videograbador de cinta, después el DVR con disco para cámaras analógicas y el NVR para cámaras IP, siempre en el mismo sitio que las cámaras. La compresión ayudó a que el video viajara: H.264, estandarizado en 2003, y H.265, de 2013, bajaron mucho el ancho de banda y el disco por cámara.

Con enlaces mejores apareció la otra opción: grabar lejos, en almacenamiento central. Las redes de almacenamiento, SAN, llevan los discos a equipos dedicados que varios servidores comparten. Hikvision tiene su propia familia para eso: pStor, un servicio que administra discos de un servidor; pStor Cluster, que agrupa varios; Hybrid SAN, su equipo de almacenamiento; y Cloud Storage Server.

### Cómo funciona

La decisión se toma al dar de alta cada cámara, y tiene consecuencias físicas.

Si graba en el equipo, el video recorre unos metros: de la cámara al NVR del sitio, por la LAN. El enlace al centro solo se usa cuando alguien mira o reproduce. Si el enlace se corta, la grabación sigue.

Si graba en el centro, el video viaja continuo por el enlace hasta el almacenamiento central, las 24 horas. Ese flujo constante necesita ancho de banda sostenido, y si el enlace se corta, en el centro queda un hueco mientras dure el corte. A cambio, la retención y la redundancia quedan en un lugar mantenido, con discos en clúster o en SAN.

Para reproducir, el cliente le pide al sistema el tramo de video; la plataforma sabe dónde quedó grabado y lo trae desde ahí, sea el NVR del sitio o el almacenamiento central. Si un Recording Server está en la LAN y se quiere buscar video desde la WAN, el FAQ pide habilitarle WAN Access.

Cada opción central tiene límites. Los equipos agregados por dominio o por Hik-Connect no graban en Hybrid SAN ni en Cloud Storage. pStor Cluster no hace grabación por movimiento ni miniaturas. pStor, clúster y SYS van en el mismo dominio de red y la misma zona horaria. Y cambiar la ubicación de una cámara en producción no mueve el video viejo: el histórico queda donde estaba.

Con NVR que ya tienen calendario, Get Device's Recording Settings lo trae a la plataforma en lugar de reemplazarlo.""",
    "teoria_figs": [
        {"file": "7-t1.svg", "after": "Si graba en el centro, el video viaja continuo",
         "alt": "Animación en cuatro tiempos con dos cámaras de una sucursal: una graba en el NVR del sitio y otra en pStor en el centro. 1: los dos flujos de grabación corren, uno por la LAN al NVR y otro por el enlace al centro. 2: se corta el enlace. El NVR sigue grabando; en el centro, la línea de tiempo de la segunda cámara queda con un hueco. 3: vuelve el enlace y la grabación central sigue, con el hueco marcado. 4: un operador reproduce la primera cámara y el video viaja desde el NVR del sitio solo mientras se reproduce.",
         "caption": "Un corte del enlace deja un hueco en la grabación central; la del sitio sigue."},
    ],
}

# =====================================================================================  8
M["8"] = {
    "fig": {"file": "8.svg",
            "alt": "La anatomía de una regla: disparador, por ejemplo Camera Offline o Alarm Input, más fuente, horario de recepción y acciones, como grabar, bloquear o avisar, da un evento, que queda registrado. Con Trigger Alarm en on, el evento pasa a alarma, en rojo, con prioridad y destinatarios que la reciben en clientes y móvil. Panel de menos ruido: Ignore Repetitive Events de 30 segundos cuenta como uno los iguales de la misma fuente; Delay Alarm para cámara offline no avisa si vuelve dentro del plazo. Notas: más de 20 eventos con imagen por segundo traban el Web Client; ejemplo, cámara caída como evento para mantenimiento y puerta forzada de noche como alarma para el guardia.",
            "caption": "Todo empieza como evento; solo lo que alguien atiende se convierte en alarma."},
    "steps": [
        {"file": "8-paso2.svg", "step": 2, "after": "Regla 1, evento de mantenimiento",
         "alt": "Dos líneas de tiempo de 0 a 150 segundos con una demora de 120 segundos marcada. Corte de 30 segundos: la cámara vuelve antes del fin de la demora y no avisa. Corte de 3 minutos: la cámara sigue offline al llegar a 120 segundos y aparece el evento. Notas: la regla 1 del laboratorio es Camera Offline (Maintenance) sobre CAM-01 a CAM-04, con Trigger Alarm apagado; sirve para que mantenimiento vea solo las cámaras realmente caídas.",
         "caption": "Con 120 s de demora, un corte breve no genera evento; uno largo, sí."},
        {"file": "8-paso3.svg", "step": 3, "after": "Regla 2, alarma real",
         "alt": "Línea de tiempo del clip: al activarse la entrada 1, el contacto de puerta, se graban 10 segundos previos y 30 posteriores; otro disparo dentro de esos 30 segundos cuenta como el mismo por Ignore Repetitive. Tabla de la regla 2: Trigger Recording en CAM-02 con pre 10 s y post 30 s; Lock Video Files 7 días, no se sobrescribe; Trigger Alarm on, prioridad alta, usuario guardia. Al pie: CAM-02 necesita calendario de grabación o la regla queda en excepción.",
         "caption": "Pre y post evento arman el clip; el bloqueo evita que se sobrescriba."},
    ],
    "concepts": [
        {"name": "Evento contra alarma",
         "para_que": "Separar lo que se registra de lo que alguien tiene que atender. Si todo suena, el operador deja de mirar; si solo suena lo importante, lo atiende.",
         "como": "Un evento es un disparador con fuente, horario de recepción y acciones. Con Trigger Alarm pasa a ser alarma, con prioridad y destinatarios que la reciben en el Control Client y el móvil. La pregunta para decidir: ¿hay alguien que vaya a hacer algo cuando aparezca?",
         "ejemplo": "En una planta de Fray Bentos, cámara offline queda como evento que mantenimiento revisa a la mañana; la puerta de emergencia abierta de noche es alarma de prioridad alta para el guardia."},
        {"name": "Ignore Repetitive Events y Delay Alarm",
         "para_que": "Bajar el ruido sin perder información. Una entrada que rebota o una cámara que parpadea por un corte de segundos no deberían llenar la pantalla de avisos.",
         "como": "Ignore Repetitive Events con 30 s hace que los eventos iguales de la misma fuente dentro de ese plazo cuenten como uno. Delay Alarm, para cámara offline, espera el plazo configurado: si la cámara vuelve antes, no hay aviso. Además, según el FAQ, más de 20 eventos con imagen por segundo hacia el Web Client lo traban.",
         "ejemplo": "Un switch de piso que se reinicia de madrugada deja cámaras offline 40 segundos. Con Delay Alarm de 120 s, a la mañana no hay cien eventos falsos."},
        {"name": "Pre y post evento con bloqueo",
         "para_que": "Que el clip muestre lo que pasó antes del disparo, no solo después, y que no desaparezca cuando el disco se recicla.",
         "como": "La acción Trigger Recording define segundos previos y posteriores; Lock Video Files protege el archivo de la sobrescritura por N días. La cámara necesita calendario de grabación configurado; si no, la regla queda en excepción.",
         "ejemplo": "Un contacto de puerta en un depósito de Colonia dispara a las 2:14. El clip arranca 10 s antes y muestra a la persona acercándose, y queda bloqueado 7 días para entregarlo a la aseguradora."},
    ],
    "teoria_md": """### Un poco de historia

El problema del exceso de alarmas no lo inventó la videovigilancia. En la industria de procesos se estudió a fondo después de accidentes donde los operadores, inundados de avisos, no vieron el importante. De ahí salieron guías como EEMUA 191, de 1999, y la norma ANSI/ISA-18.2, de 2009, sobre gestión de alarmas. Su idea central es la misma que usa este curso: una alarma tiene que pedir una respuesta de un operador; si nadie va a hacer nada, no es alarma.

En video se sumó la grabación por evento. Como la cámara graba en un buffer continuo, el sistema puede guardar segundos de antes del disparo, algo imposible con una grabación que arranca recién cuando llega la señal.

### Cómo funciona

En HikCentral, una regla une cuatro piezas: un disparador (cámara offline, entrada de alarma, una analítica), una fuente (qué cámaras o entradas), un horario de recepción y acciones. Lo que produce es un evento, que queda registrado.

Cuando la fuente dispara, el equipo avisa a la plataforma. Antes de hacer nada, la regla filtra. Ignore Repetitive Events agrupa los eventos iguales de la misma fuente dentro del plazo: con 30 s, cinco rebotes de un contacto cuentan como uno. Delay Alarm, en cámara offline, espera: si la cámara vuelve dentro del plazo, no pasa nada; si sigue caída, recién ahí aparece el evento.

Después se ejecutan las acciones. Trigger Recording guarda el clip con los segundos previos y posteriores configurados, y Lock Video Files lo protege de la sobrescritura durante los días indicados. Para eso la cámara tiene que tener calendario de grabación.

Si la regla tiene Trigger Alarm encendido, el evento sube de categoría: pasa a alarma, con prioridad y destinatarios. Los usuarios destinatarios la reciben en el Control Client y en el Mobile Client, y la reconocen, de a una o en lote, hasta 100 a la vez según el FAQ.

El ruido también pesa en la plataforma: el FAQ marca que más de 20 eventos con imagen por segundo hacia el Web Client producen lag, y sugiere cortar la suscripción y guardar las imágenes en pStor. Diseñar pocas alarmas buenas es, además, cuidar el servidor.""",
    "teoria_figs": [
        {"file": "8-t1.svg", "after": "Cuando la fuente dispara, el equipo avisa",
         "alt": "Animación en cuatro tiempos. 1: se activa la entrada de alarma del contacto de puerta y el NVR avisa a la plataforma. 2: llegan dos disparos más dentro de 30 segundos y Ignore Repetitive los agrupa en un solo evento. 3: la acción Trigger Recording guarda el clip de CAM-02 desde 10 segundos antes hasta 30 después, y Lock Video Files lo bloquea 7 días. 4: con Trigger Alarm encendido, la alarma de prioridad alta aparece en el Control Client del usuario guardia, que la reconoce.",
         "caption": "Del disparo a la alarma: filtrar, grabar con pre y post, y avisar a quien la atiende."},
    ],
}

# =====================================================================================  9
M["9"] = {
    "fig": {"file": "9.svg",
            "alt": "Cadena de izquierda a derecha: persona, Prueba Lab con ID 9001, con credencial que puede ser tarjeta, huella, rostro, PIN o QR; nivel de acceso Oficina hábil, puertas más plantilla de horario; asignación a la persona o a un departamento entero; y Aplicar a los dispositivos, en oscuro, que es cuando el permiso viaja a la controladora de la Puerta Lab. Panel ámbar, si no aplicaste: la plataforma muestra el permiso pero la controladora no lo tiene y la tarjeta no abre, aparece un ícono de pendiente junto a Apply y si falla, Access Control Test muestra en qué quedó. Al pie: alta de personas en la plataforma, una sola fuente de verdad.",
            "caption": "Persona, nivel y asignación quedan en la plataforma hasta que aplicás a los dispositivos."},
    "steps": [
        {"file": "9-paso4.svg", "step": 4, "after": "Aplicá (en V2.x: Passing Management",
         "alt": "Dos paneles. En verde, Apply (Initial) sin marcar: HikCentral manda solo lo cambiado a la controladora, que sigue online; las puertas funcionan y sirve para el día a día. En rojo, Apply (Initial) marcado: borra y reescribe todo, la controladora queda offline y nadie pasa; solo fuera de horario y con aviso al cliente. Abajo, los valores del laboratorio: Specified Persons Prueba Lab, Specified Access Point Puerta Lab, Apply (Initial) sin marcar. Ruta de V2.x.",
         "caption": "Aplicar cambios no corta el servicio; Apply (Initial) deja las puertas offline mientras reescribe."},
        {"file": "9-paso5.svg", "step": 5, "after": "Pasá la tarjeta dentro y fuera del horario",
         "alt": "Línea de un lunes de 00:00 a 24:00 con la ventana de la plantilla Oficina hábil de 08:00 a 19:00 en verde. Tarjeta a las 10:00, dentro de la ventana: acceso concedido. Tarjeta a las 21:00, fuera: acceso denegado. Abajo, el registro de acceso con esas dos filas para Prueba Lab en la Puerta Lab. Nota: si las dos abren o ninguna, revisá que hayas aplicado y la hora de la controladora.",
         "caption": "Una pasada dentro y otra fuera del horario prueban el nivel completo."},
    ],
    "concepts": [
        {"name": "Nivel de acceso",
         "para_que": "Agrupa puertas con una plantilla de horario para dar permisos por función y no puerta por puerta. Responde dónde y cuándo; la persona y su credencial responden quién.",
         "como": "Se crea con un nombre, las puertas y la plantilla (por ejemplo lunes a viernes de 08:00 a 19:00) y se asigna a personas o a departamentos. La persona tiene su credencial: tarjeta, huella, rostro, PIN o QR, según la lectora.",
         "ejemplo": "En una mutualista, el nivel Administración abre las puertas de oficinas en días hábiles; el de Mantenimiento abre salas técnicas las 24 horas. Una persona nueva recibe el nivel y listo."},
        {"name": "Aplicar a los dispositivos",
         "para_que": "La controladora decide en la puerta con lo que tiene guardado; la plataforma es donde se edita. Aplicar es el paso que lleva lo editado a cada controladora.",
         "como": "Sin marcar Apply (Initial), se mandan solo los cambios y las puertas siguen andando. Con Apply (Initial), se borra y reescribe todo, y durante ese proceso las controladoras quedan offline y nadie pasa: fuera de horario y con aviso. Un ícono de pendiente marca lo no aplicado; Access Control Test ayuda si falla.",
         "ejemplo": "Recursos humanos da de alta diez personas el lunes a las 9. Aplicar cambios las lleva a las puertas en minutos sin trancar el hall. El Apply (Initial) queda para el sábado a la noche, si hace falta."},
        {"name": "Una sola fuente de personas",
         "para_que": "Si las personas se cargan a veces en la plataforma y a veces en el equipo, las listas se desincronizan y nadie sabe cuál es la buena. El FAQ recomienda elegir un solo origen.",
         "como": "Con HikCentral, el alta se hace en la plataforma y se aplica a los equipos. Solo en sitios sin servidor permanente se trabaja en el equipo. Las reglas de ID de persona se configuran con la lista vacía, antes de la primera alta.",
         "ejemplo": "Un edificio corporativo donde la recepción cargaba tarjetas en la controladora: al pasar a HikCentral, todas las altas van por la plataforma y la recepción deja de tocar el equipo."},
    ],
    "teoria_md": """### Un poco de historia

El control de acceso electrónico reemplazó la llave por una credencial que se puede dar de baja sin cambiar cerraduras. Las tarjetas de proximidad y la interfaz Wiegand entre lector y controladora se volvieron estándar de hecho; después llegaron la huella, el rostro, el PIN y el QR. HikCentral Access Control, el hermano chico de la familia, lista todas esas credenciales, además de interbloqueo, antipassback y autenticación multifactor.

Lo que no cambió es la arquitectura: la controladora vive junto a la puerta y decide ahí, con su propia copia de los permisos. La plataforma central es donde se edita y desde donde se reparte. Ese reparto es el paso que el técnico tiene que entender.

### Cómo funciona

Un permiso se arma en tres piezas. La persona, con su credencial. El nivel de acceso, que junta puertas y una plantilla de horario. Y la asignación del nivel a la persona o a su departamento. Todo eso queda guardado en la base de datos del SYS.

La puerta todavía no sabe nada. Cuando alguien pasa la tarjeta, la controladora busca en lo que tiene guardado: si no hay registro de esa tarjeta, niega. Por eso la plataforma marca con un ícono de pendiente los cambios que no llegaron a los dispositivos.

Aplicar es enviar. En el modo normal, sin Apply (Initial), la plataforma calcula lo que cambió y manda solo eso: altas, bajas, horarios. Las puertas siguen funcionando durante el envío. Con Apply (Initial), la plataforma borra todo lo que tiene la controladora y lo vuelve a escribir. Es útil cuando un equipo quedó desordenado o se cambió, pero durante ese proceso, dice el manual, los dispositivos quedan offline y las personas no pueden pasar por esos puntos de acceso.

Después de aplicar, la prueba es física: la tarjeta dentro y fuera del horario, y el registro de acceso que muestra concedido y denegado. Si el aplicado falló, Access Control Test ayuda a ver dónde.

Para que todo esto sea confiable hace falta un solo origen de las personas. El FAQ recomienda no combinar altas en la plataforma y en el equipo: con HikCentral, se carga en la plataforma y se aplica.""",
    "teoria_figs": [
        {"file": "9-t1.svg", "after": "En el modo normal, sin Apply (Initial)",
         "alt": "Animación en cuatro tiempos. 1: en el SYS se asigna el nivel Oficina hábil a Prueba Lab y aparece el ícono de pendiente. 2: Prueba Lab pasa la tarjeta y la controladora, que todavía no tiene el permiso, deniega. 3: se aplican los cambios y solo ese registro viaja a la controladora, que sigue online. 4: la misma tarjeta pasa de nuevo y la controladora concede el acceso con lo que tiene guardado.",
         "caption": "La controladora decide con su copia: hasta que aplicás, el permiso nuevo no existe en la puerta."},
    ],
}

# =====================================================================================  10
M["10"] = {
    "fig": {"file": "10.svg",
            "alt": "Siete pasos en orden: 0, hora y zona, iguales en SYS y controladoras, resaltado en ámbar; 1, puntos de marca, qué lectoras son de entrada, de salida o ambas; 2, regla general, fin de semana y ausencias; 3, plantilla de turno, Normal o Man-Hour; 4, turno, repetir por semana; 5, asignar a personas con fechas; 6, registros al día siguiente. Recuadro: la plataforma calcula con la hora del servidor y no maneja múltiples zonas horarias. Nota: es la receta del soporte de Hikvision USA, y las mismas lectoras de acceso hacen de reloj.",
            "caption": "Primero la hora; después puntos de marca, regla, plantilla, turno y asignación."},
    "steps": [
        {"file": "10-paso1.svg", "step": 1, "after": "Revisá hora y zona del SYS",
         "alt": "Dos paneles. En verde, misma zona y NTP común: SYS 192.168.88.10 en UTC-3 y controladora en UTC-3 con NTP al SYS; las pasadas llegan en vivo y los reportes cierran. En rojo, la controladora en otra zona horaria: el histórico aparece pero las pasadas en vivo no. Abajo, los comandos Get-TimeZone y w32tm /query /status, y en la controladora Configuración, Hora, con la misma zona y NTP al SYS o al del cliente. Al pie: Uruguay es UTC-3 todo el año, sin horario de verano desde 2015.",
         "caption": "Misma zona y misma fuente de hora en el SYS y en las controladoras."},
        {"file": "10-paso4.svg", "step": 4, "after": "Shift Settings > Template > Add",
         "alt": "Línea de un día de 07:00 a 19:00 con la plantilla de 08:00 a 17:00 punteada. Marcas de ejemplo: 07:52 primera entrada y 17:10 última salida, en verde, y dos marcas del medio, 12:30 y 13:15, en gris. Debajo, una barra verde: el cálculo toma de 07:52 a 17:10. Notas: el turno Normal exige entrar y salir dentro de ventanas válidas; el Man-Hour es más flexible y el cálculo más usado es primera entrada y última salida.",
         "caption": "En Man-Hour con primera entrada y última salida, cuentan la primera y la última marca del día."},
    ],
    "concepts": [
        {"name": "Punto de marca",
         "para_que": "Le dice al sistema qué lectoras cuentan para la asistencia y cómo: entrada, salida o ambas. Así las mismas lectoras del control de acceso hacen de reloj, sin un equipo aparte.",
         "como": "En Attendance, Attendance Checkpoint, se agregan las lectoras elegidas y se marca su función. Las demás puertas del edificio siguen controlando acceso, pero no suman horas.",
         "ejemplo": "En una curtiembre con tres puertas, solo el molinete de personal es punto de marca de entrada y salida; la puerta del depósito no cuenta para el reloj."},
        {"name": "Turno Normal y turno Man-Hour",
         "para_que": "Modelan dos maneras de trabajar. El Normal exige entrar y salir dentro de ventanas válidas; el Man-Hour es más flexible y mide horas, útil para horarios que se mueven.",
         "como": "Se arma una plantilla (tipo, horario y forma de cálculo), después un turno que la repite por semana, y se asigna a personas con fechas. En Man-Hour, el cálculo más usado es primera entrada y última salida.",
         "ejemplo": "La planta trabaja con turno Normal de 06:00 a 14:00; el personal administrativo, con Man-Hour de 08:00 a 17:00 y primera entrada y última salida."},
        {"name": "Una sola zona horaria",
         "para_que": "La asistencia es aritmética con horas: si los relojes no coinciden, los cálculos no cierran. HikCentral calcula con la hora del servidor y no maneja múltiples zonas horarias.",
         "como": "SYS y controladoras en la misma zona y con la misma fuente de hora, por ejemplo NTP al SYS o al servidor del cliente. Si una controladora queda en otra zona, el Control Client no muestra sus pasadas en tiempo real aunque sí el histórico. Se revisa antes de crear turnos.",
         "ejemplo": "Una controladora que vino configurada de fábrica en otra zona hace que la asistencia del primer mes no cierre. Se corrige la zona y el NTP, y el mes siguiente sale bien."},
    ],
    "teoria_md": """### Un poco de historia

Medir la asistencia con una máquina es una idea del siglo XIX: Willard Bundy patentó en 1888 un reloj que marcaba en una tarjeta la hora de entrada y salida de cada empleado. Durante un siglo el reloj fue un aparato aparte; con el control de acceso electrónico, la misma lectora que abre la puerta empezó a servir de reloj.

La hora de esos relojes también se volvió un problema de red. NTP, el protocolo que sincroniza relojes por la red, lo creó David Mills en los años ochenta; su versión vigente es la RFC 5905, de 2010. Y la zona horaria cambia con las decisiones de cada país: Uruguay usa UTC-3 todo el año desde que dejó el horario de verano en 2015.

### Cómo funciona

La asistencia en HikCentral es una cadena de configuraciones que se hace en orden, siguiendo la receta del soporte de Hikvision USA. Primero, la controladora agregada y las personas con credenciales. Después, los puntos de marca: qué lectoras cuentan y si son de entrada, de salida o de ambas. La regla general fija el fin de semana y qué pasa si alguien no marca. La plantilla de turno define tipo y horario, el turno la repite por semana y la asignación la vincula a personas desde una fecha.

Cada pasada genera un registro en la controladora, con la hora de la controladora. Ese registro sube al SYS, que lo cruza con el turno usando la hora del servidor. En un turno Man-Hour con primera entrada y última salida, el sistema toma la primera y la última marca del día y calcula con ellas.

Ahí entra la hora. La plataforma no maneja múltiples zonas horarias: si la controladora está en otra zona que el SYS, sus pasadas no aparecen en tiempo real en el Control Client, aunque sí en el histórico, y los cálculos del turno no cierran. Por eso el primer paso del laboratorio es revisar `Get-TimeZone` y `w32tm /query /status` en el servidor, y la zona y el NTP en la controladora.

Un detalle más del FAQ: los registros de acceso se guardan cada minuto. Si el servicio cae justo en ese momento, se puede perder ese minuto de datos. Los reportes se miran al día siguiente, en Attendance Records.""",
    "teoria_figs": [
        {"file": "10-t1.svg", "after": "Cada pasada genera un registro en la controladora",
         "alt": "Animación en cuatro tiempos con dos controladoras y el SYS en UTC-3. 1: una persona marca a las 10:00 en la controladora A, configurada en UTC-3, y el registro sube al SYS. 2: el SYS lo cruza con el turno y la pasada aparece en vivo en el Control Client. 3: otra persona marca en la controladora B, configurada en otra zona horaria; el registro sube con otra hora. 4: esa pasada no aparece en vivo y queda solo en el histórico; la corrección es poner la controladora en la misma zona y con NTP al SYS.",
         "caption": "El registro viaja con la hora de la controladora; si su zona no es la del SYS, no aparece en vivo."},
    ],
}

# =====================================================================================  11
M["11"] = {
    "fig": {"file": "11.svg",
            "alt": "A la izquierda, los roles fijos Administrator, con todos los permisos, y Operator, con recursos y aplicaciones, que no se editan ni se borran. En el centro, el rol a medida Guardia con cuatro perillas: vigencia hoy a fin de año; horario de permisos todos los días de 19:00 a 07:00; áreas visibles, solo Depósito; recursos, vivo y reproducción de Depósito. El rol se asigna al usuario guardia.lab. Nota ámbar: con el rol vencido o fuera de horario, el usuario es expulsado. Nota: subir la contraseña mínima de Medium a Strong. Al pie: cada persona su usuario, cada usuario el rol mínimo.",
            "caption": "Vigencia, horario, áreas y recursos definen qué ve y cuándo cada usuario."},
    "steps": [
        {"file": "11-paso4.svg", "step": 4, "after": "Entrá con guardia.lab dentro y fuera",
         "alt": "Dos paneles. A las 22:00, dentro del horario, en verde: el usuario ve solo el área Depósito con el vivo de cuatro cámaras, y el resto de las áreas no existe para él. A las 10:00, fuera del horario, en rojo: no puede iniciar sesión y, si estaba adentro, lo expulsa; lo mismo pasa al vencer la vigencia, útil para contratistas y turnos. Nota: el horario del rol Guardia del laboratorio es de 19:00 a 07:00 todos los días.",
         "caption": "Dentro del horario ve su área; fuera, el sistema no lo deja entrar."},
        {"file": "11-paso5.svg", "step": 5, "after": "Opcional (HTTPS)",
         "alt": "El certificado .crt firmado por una CA y la clave privada exportada en texto se juntan en un archivo .pem: primero el bloque BEGIN CERTIFICATE, después el bloque BEGIN PRIVATE KEY. El .pem se sube en HikCentral en System, Advanced, Transfer. Con el certificado embebido el navegador muestra No seguro; con el .pem firmado por una CA, sin advertencia si los puestos confían en esa CA. Nota roja: la clave privada no se manda por correo ni se pega en conversores online; armá el .pem en una PC de confianza.",
         "caption": "Certificado y clave privada en un .pem, armado en una PC de confianza."},
    ],
    "concepts": [
        {"name": "Rol a medida",
         "para_que": "Dar a cada usuario exactamente lo que su tarea pide. Con un admin compartido, cualquier acción es de nadie; con roles, cada acción queda asociada a una persona con permisos acotados.",
         "como": "Administrator y Operator vienen fijos y no se editan. Un rol nuevo define vigencia, plantilla horaria de permisos, áreas visibles, acceso a recursos y permisos de configuración. Las áreas visibles se apoyan en el árbol de áreas: un área oculta no se ve ni se accede.",
         "ejemplo": "En un shopping, rol Guardia con pasillos y estacionamiento, solo vivo y reproducción; rol Mantenimiento con estado de equipos. Cada persona con su usuario."},
        {"name": "Horario de permisos y vigencia",
         "para_que": "Hacer que los permisos se apaguen solos. Un contratista que termina su trabajo o un turno que cambia no dependen de que alguien se acuerde de dar de baja.",
         "como": "La vigencia fija desde y hasta cuándo vale el rol; la plantilla horaria, en qué horas. Si el rol vence o queda fuera de horario, el usuario es expulsado y no puede volver a entrar.",
         "ejemplo": "Una empresa de mantenimiento de ascensores necesita ver dos cámaras durante un mes de obra. Su rol vence el último día y el acceso se corta sin intervención."},
        {"name": "Endurecer el acceso",
         "para_que": "Un sistema de seguridad con valores por defecto es un riesgo en sí mismo. La crítica sobre el historial de fallas de seguridad de Hikvision es un motivo más para no dejar nada de fábrica.",
         "como": "Subir la fuerza mínima de contraseña de Medium, que viene por defecto, a Strong. Instalar HTTPS con un certificado propio en formato .pem firmado por una CA, en lugar del embebido que da No seguro. Y no exponer el sistema a internet sin necesidad.",
         "ejemplo": "En la entrega de una obra, IES deja el SYS con HTTPS de la CA interna del cliente, contraseña mínima Strong y un usuario por operador, todo anotado en el acta."},
    ],
    "teoria_md": """### Un poco de historia

Que cada usuario tenga solo los permisos que su tarea necesita es el principio de mínimo privilegio, que formularon Jerome Saltzer y Michael Schroeder en 1975. Asignar esos permisos a roles, y los roles a personas, es el control de acceso basado en roles (RBAC): lo describieron David Ferraiolo y Richard Kuhn, del NIST, en 1992, y se estandarizó como ANSI INCITS 359 en 2004.

La otra mitad de la lección es el cifrado de la web. HTTPS usa TLS, cuya versión 1.0 se publicó en 1999, con certificados X.509 que firma una autoridad certificante (CA). El formato .pem, texto con bloques BEGIN y END, viene del correo seguro de los noventa (RFC 1421, de 1993) y hoy es la forma más común de mover certificados y claves.

### Cómo funciona

En HikCentral, cada vez que un usuario inicia sesión, la plataforma mira su rol y responde cuatro preguntas. ¿El rol está vigente? ¿Estamos dentro de su horario de permisos? ¿Qué áreas ve? ¿Qué puede hacer con los recursos de esas áreas? La respuesta arma lo que el usuario ve: un Guardia con el área Depósito no ve las demás áreas, porque para él no existen.

Las preguntas no se hacen solo al entrar. Si el rol vence o el reloj sale del horario de permisos, el manual dice que los usuarios con ese rol son forzados a cerrar sesión y no pueden volver a entrar. Eso permite roles para contratistas, con fecha de fin, o para turnos, con horario.

Administrator y Operator son roles predefinidos que no se editan ni se borran. Todo lo demás se arma a medida, y lo correcto es empezar por lo mínimo y sumar.

La contraseña es la primera barrera. Por defecto, la fuerza mínima es Medium: 8 caracteres o más, con al menos tres tipos, sin "123" ni "admin" y sin más de tres caracteres iguales seguidos. Subirla a Strong endurece todas las cuentas.

El canal es la segunda. Con el certificado embebido, el navegador muestra "No seguro" porque nadie de confianza lo firmó. Al subir un .pem con el certificado firmado por una CA y su clave privada, el navegador puede verificar con quién habla, y la clave se maneja solo en una PC de confianza.""",
    "teoria_figs": [
        {"file": "11-t1.svg", "after": "cada vez que un usuario inicia sesión",
         "alt": "Animación en cuatro tiempos con el usuario guardia.lab y su rol Guardia. 1: a las 19:30 inicia sesión; el SYS revisa vigencia y horario de permisos, los dos en verde. 2: el SYS filtra por áreas visibles y le muestra solo Depósito con sus cámaras. 3: a las 07:00 termina el horario de permisos; el SYS cierra la sesión y lo expulsa. 4: a las 10:00 intenta entrar de nuevo y el login se rechaza por estar fuera de horario.",
         "caption": "El rol se evalúa al entrar y mientras dura la sesión: fuera de horario, el usuario sale."},
    ],
}

# =====================================================================================  12
M["12"] = {
    "fig": {"file": "12.svg",
            "alt": "Escalera de cinco escalones que se sube desde abajo, con la prueba de cada uno al costado. 1, físico: cable, enlace y alimentación, mirando luces del puerto y PoE. 2, IP y gateway: ping 192.168.88.1 y al equipo. 3, DNS, si usa dominio o Hik-Connect: Resolve-DnsName dev.hik-connect.com. 4, servicio habilitado, Platform Access, ISUP u ONVIF: la casilla activada en el equipo. 5, puertos contra la Communication Matrix: Test-NetConnection al 7660. Al pie: si el escalón 2 falla, no tiene sentido mirar puertos; anotá en qué escalón quedó.",
            "caption": "Del cable a los puertos, en ese orden, anotando dónde se cortó."},
    "steps": [
        {"file": "12-paso2.svg", "step": 2, "after": "Puertos clave:",
         "alt": "Diagrama: el puesto o navegador con Web y Control Client llega al SYS más Streaming Gateway, 192.168.88.10, por 80 y 443 y por 559 para el vivo web; el SYS entra a la cámara 192.168.88.21 por el 8000; la cámara se registra en el SYS por el 7660. Tabla de la Communication Matrix V2.4.1: 80 y 443 al SYS para Web, Control y Mobile Client; 7660 al SYS para registro ISUP; 554 al Streaming Gateway para video RTSP; 559 al Streaming Gateway para vivo en Chrome y Firefox; 8000 al equipo para alta por IP. Abajo, los tres Test-NetConnection del laboratorio.",
         "caption": "Cada puerto tiene un origen, un destino y un para qué; la matriz es la referencia."},
        {"file": "12-paso5.svg", "step": 5, "after": "contá conexiones al NVR",
         "alt": "Dos paneles. En rojo, cinco puestos piden video directo al NVR, una conexión por pedido, contra un tope de conexiones remotas. En verde, los mismos cinco puestos piden al Streaming Server, que reparte el video y hace menos conexiones directas contra el NVR. Nota: en el caso del soporte de Hikvision USA, el NVR llegaba a 128 conexiones; antes de tocar el ancho de banda, contá cuántos clientes piden video al NVR.",
         "caption": "Maximum number of streams es un tope de conexiones del NVR, no de ancho de banda."},
    ],
    "concepts": [
        {"name": "Diagnóstico de abajo arriba",
         "para_que": "Evitar el prueba y error. Cada capa depende de la de abajo: si no hay enlace, no hay IP; si no hay IP, no hay DNS; si el servicio está apagado, el puerto no contesta. Empezar por abajo descarta rápido.",
         "como": "Orden: físico, IP y gateway, DNS, servicio habilitado y puertos. Con `ipconfig`, `ping`, `Resolve-DnsName` y `Test-NetConnection`. Después, el registro de online y offline del equipo en el Web Client dice a qué hora cae.",
         "ejemplo": "Una cámara de un liceo en Salto aparece offline. Ping al gateway bien, ping a la cámara no: el problema está abajo, y resulta ser el puerto del switch apagado por un corte."},
        {"name": "Communication Matrix",
         "para_que": "Es la lista oficial de qué puerto usa cada componente, en qué dirección y para qué. Reemplaza el abrí todo por abrí exactamente esto.",
         "como": "Según la V2.4.1: 80 y 443 del SYS para los clientes; 7660 para registro ISUP, 7332 para alarmas ISUP, 8555 para archivos; 554 y 559 del Streaming Gateway, este último para el vivo en Chrome y Firefox; 16000 y 16001 para stream ISUP. Cada prueba de puerto se valida contra la matriz de la versión instalada.",
         "ejemplo": "El vivo anda en un navegador viejo pero no en Chrome. La matriz dice que el Web Client usa el 559 del gateway en los demás navegadores: estaba cerrado en el firewall."},
        {"name": "Máximo número de streams",
         "para_que": "Distinguir conexiones de ancho de banda. Un NVR tiene un tope de conexiones remotas; cuando se llena, rechaza pedidos aunque la red esté sobrada.",
         "como": "El error maximum number of streams indica ese tope: en el caso del soporte de Hikvision USA, 128 conexiones. Se cuentan los clientes que piden video al NVR; un Streaming Server concentra pedidos y reduce las conexiones directas.",
         "ejemplo": "Un centro de monitoreo con muchos puestos mirando el mismo NVR: al pasar el video por el Streaming Server, el error desaparece sin tocar el enlace."},
    ],
    "teoria_md": """### Un poco de historia

Diagnosticar por capas viene del modelo OSI, que ISO publicó como norma ISO 7498 en 1984: siete capas, cada una apoyada en la de abajo. Los técnicos de redes lo convirtieron en método: si el problema puede estar en cualquier capa, conviene empezar por la física y subir, porque cada escalón que funciona descarta todo lo que tiene debajo.

Las herramientas también tienen historia. `ping` lo escribió Mike Muuss en 1983. `Test-NetConnection`, que prueba un puerto TCP desde PowerShell, llegó con Windows 8.1 y Windows Server 2012 R2. Y el navegador cambió las reglas del video: Internet Explorer, que Microsoft retiró en 2022, era el caso especial; en los demás navegadores, el Web Client de HikCentral toma el vivo por el puerto 559 del gateway.

### Cómo funciona

El método tiene cinco escalones. Físico: enlace, cable, alimentación. IP y gateway: `ipconfig` y `ping` al gateway y al equipo. DNS: `Resolve-DnsName` si el equipo usa dominio o Hik-Connect. Servicio habilitado: que la casilla de Platform Access, ISUP u ONVIF esté activada. Y recién ahí, puertos.

Para los puertos, la referencia es la Communication Matrix. Cada fila dice origen, destino, puerto y para qué: los clientes al 80 y 443 del SYS; los equipos ISUP al 7660 del SYS; los clientes al 554 del gateway para RTSP y al 559 para el vivo web. Probar un puerto sin saber quién debería hablar con quién es tirar comandos al aire.

Cuando el vivo funciona en un lado y no en otro, la matriz explica el porqué. El navegador pide el vivo al gateway por el 559; si un firewall lo bloquea, la página carga pero la ventana de video queda negra. Abrir ese puerto, o mapearlo hacia la WAN cuando corresponde, lo resuelve.

No todo offline es red. Con Hik-Connect, el equipo necesita DNS que resuelva (el soporte sugiere 8.8.8.8 y 8.8.4.4) y los puertos STUN 6002, 6800, 8555, 9010 y 9020 sin bloquear. Una cámara ONVIF puede quedar offline porque HikCentral la busca en el 80 y ella usa otro puerto. Y "maximum number of streams" es el tope de conexiones del NVR, 128 en el caso documentado, no falta de ancho de banda: un Streaming Server concentra los pedidos.

Cada caso se cierra anotando en qué escalón estaba la falla.""",
    "teoria_figs": [
        {"file": "12-t1.svg", "after": "El navegador pide el vivo al gateway por el 559",
         "alt": "Animación en cuatro tiempos. 1: Chrome abre el Web Client contra el SYS por el 443 y la página carga. 2: el navegador pide el vivo al Streaming Gateway por el 559 y el firewall lo bloquea; la ventana de video queda negra. 3: se revisa la Communication Matrix y se habilita el 559 en el firewall, con autorización del cliente. 4: el pedido por el 559 pasa, el gateway reenvía el video de la cámara y el vivo aparece en el navegador.",
         "caption": "La página carga por el 443, pero el vivo en Chrome necesita el 559 del gateway."},
    ],
}

# ===================================================================================== validación
OUT = "/home/claude/ies-training/ilustraciones/hikcentral/manifest.json"
pub = json.load(open("/home/claude/ies-training/site2/data/hikcentral.json", encoding="utf-8"))
labs = {str(l["id"]): l["lab"]["md"] for l in pub["lessons"]}
NUM = re.compile(r"^(\d+)\.\s")
err = []


def lab_lines(md):
    fence, step, out = False, 0, []
    for ln in md.split("\n"):
        if ln.strip().startswith("```"):
            fence = not fence; continue
        m = NUM.match(ln)
        if not fence and m:
            step = int(m.group(1))
        out.append((fence, step, ln))
    return out


for lid, m in M.items():
    s = json.dumps(m, ensure_ascii=False)
    if "—" in s or "–" in s:
        err.append(f"{lid}: guion largo")
    n = len(m["concepts"])
    if not 2 <= n <= 4:
        err.append(f"{lid}: {n} conceptos")
    th = m["teoria_md"]
    w = len(re.sub(r"[#`*]", "", th).split())
    if not 250 <= w <= 450:
        err.append(f"{lid}: teoría con {w} palabras")
    if "### Un poco de historia" not in th or "### Cómo funciona" not in th:
        err.append(f"{lid}: faltan subtítulos")
    ll = lab_lines(labs[lid])
    for st in m["steps"]:
        a = st["after"]
        hits = [(f, sp) for f, sp, ln in ll if a in ln]
        if len(hits) != 1 or hits[0][0] or hits[0][1] != st["step"] or labs[lid].count(a) != 1:
            err.append(f"{lid}: ancla de paso {st['file']} mal: {hits}")
        if not st["file"].startswith(f"{lid}-paso{st['step']}."):
            err.append(f"{lid}: nombre {st['file']}")
    for tf in m.get("teoria_figs", []):
        a = tf["after"]
        if th.count(a) != 1 or not 15 <= len(a) <= 60:
            err.append(f"{lid}: ancla de teoría {a!r} aparece {th.count(a)} veces o largo {len(a)}")
        par = [p for p in th.split("\n\n") if a in p]
        if par and par[0].startswith("#"):
            err.append(f"{lid}: ancla de teoría en un título")
    print(lid, "palabras", w, "conceptos", n, "pasos", [x["step"] for x in m["steps"]])

json.dump(M, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", OUT, len(M))
if err:
    print("\n".join(err)); sys.exit(1)
