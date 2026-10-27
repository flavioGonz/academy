"""Genera /home/claude/ies-training/ilustraciones/linux/manifest.json (figuras, pasos, conceptos, teoría, figuras de teoría y script bash)."""
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


PEGAR = "Pegalo en la terminal tal cual: va dentro de una función, así un error no te cierra la sesión."
ROOT = "Si lo pegás, entrá antes como root con sudo -i: así sudo no toma las líneas pegadas como contraseña. También lo podés guardar como archivo y correrlo con sudo bash archivo.sh."

# =====================================================================================  1
L("1",
  {"file": "1.svg", "alt": "A la izquierda, la raíz / con seis ramas: /etc, configuración del sistema (ssh/sshd_config, netplan, fstab); /var, lo que cambia con el uso (log/journal, cache/apt, lib/docker); /home, carpetas de los usuarios (/home/tecnico); /root, en ámbar, carpeta personal del administrador, que no es la raíz; /srv, datos que sirve el equipo (/srv/obra, /srv/backup); /tmp, temporales, que en Ubuntu 26.04 vive en RAM. A la derecha, en verde, los comandos que solo leen: pwd, ls -la, less, find, grep -rn y la tubería. Nota: todo es /algo, no hay disco C ni D; un disco extra se monta en una carpeta como /srv/datos.",
   "caption": "Un solo árbol desde /, y seis comandos para recorrerlo sin cambiar nada."},
  [{"file": "1-paso1.svg", "step": 1, "after": "Ubicate y listá:",
    "alt": "El comando ls -la /etc | less y dos líneas de ejemplo, una del directorio ssh y otra del archivo fstab, con las columnas marcadas: el primer carácter es el tipo (d directorio, guion archivo), los nueve siguientes son los permisos de dueño, grupo y resto, después el dueño y el grupo (root root), el tamaño y la fecha, y al final el nombre. Abajo, las teclas de less: barra para buscar, n repite la búsqueda y q sale sin cambiar nada. Nota: el usuario común puede leer casi todo /etc; un Permission denied es un archivo protegido.",
    "caption": "Tipo, permisos, dueño y grupo, tamaño, fecha y nombre, en ese orden."},
   {"file": "1-paso3.svg", "step": 3, "after": "Buscá una palabra dentro de los archivos",
    "alt": "Terminal con grep -rn \"Port\" /etc/ssh 2>/dev/null y dos líneas de resultado de ejemplo: /etc/ssh/sshd_config:14:#Port 22 y /etc/ssh/ssh_config:41 con Port 22 comentado. En la primera se marcan el archivo, el número de línea y la línea encontrada. Tres tarjetas: -r recorre la carpeta con sus subcarpetas y -n agrega el número de línea; el numeral al principio indica una línea comentada, que no cuenta, y vale el puerto por defecto 22; 2>/dev/null descarta los errores como Permission denied.",
    "caption": "Cada resultado trae archivo, número de línea y texto, separados por dos puntos."}],
  [C("El árbol único y /etc",
     "Unix decidió que todo, discos incluidos, cuelgue de una sola raíz. Así un programa siempre sabe dónde buscar su configuración, sus datos y sus logs, en cualquier equipo.",
     "La configuración del sistema está en /etc, lo que cambia con el uso en /var, y los usuarios en /home. /root es solo la carpeta personal del administrador. Cuando un técnico dice \"está en root\", casi siempre quiere decir /etc.",
     "Te dan un LXC con una herramienta de monitoreo que nadie documentó. Antes de tocar nada, `ls -la /etc` y `find /etc -name \"*monitor*\"` te muestran dónde está su configuración."),
   C("Leer sin modificar: less, find y grep",
     "En un equipo desconocido, el riesgo es cambiar algo sin querer. Estas herramientas existen para mirar: ninguna escribe en lo que lee.",
     "less abre un archivo o la salida de un comando; con / buscás, con n repetís y con q salís. find busca por nombre y grep busca texto adentro de los archivos; con -rn recorre carpetas y te da archivo y número de línea. Conviene hacer este recorrido como usuario común, sin sudo.",
     "En un appliance de grabación, `grep -rn \"Port\" /etc/ssh` te dice en qué puerto escucha SSH sin abrir ningún editor, y `less /etc/ssh/sshd_config` te deja leer el resto con calma."),
   C("Tubería y redirección",
     "Cada programa de Unix hace una sola cosa. La tubería permite combinarlos sin archivos intermedios: la salida de uno entra al siguiente.",
     "`|` conecta la salida de un comando con la entrada de otro. Los errores van por otro canal: `2>/dev/null` los descarta y deja solo los resultados. El truco del corchete, `grep \"[s]shd\"`, evita que grep aparezca en su propia búsqueda.",
     "Querés saber si SSH está corriendo en un servidor de accesos: `ps aux | grep \"[s]shd\"` te muestra solo los procesos de sshd, sin la línea del grep.")],
  """
### Un poco de historia

Linux sigue el modelo de Unix, el sistema que Ken Thompson y Dennis Ritchie empezaron en los Laboratorios Bell en 1969. De ahí vienen dos ideas que usás todos los días: un único árbol de archivos que arranca en `/`, y programas chicos que hacen una sola cosa y se combinan. La tubería `|`, que conecta la salida de un programa con la entrada de otro, la propuso Doug McIlroy y entró a Unix en 1973.

Linus Torvalds publicó el núcleo Linux en 1991, y las distribuciones lo juntaron con las herramientas GNU: así nacieron Debian, en 1993, y sobre Debian, Ubuntu, en 2004. Por eso un servidor Debian 13, un Ubuntu 26.04, un LXC de Proxmox o un appliance de grabación se recorren con los mismos comandos. La Debian Reference propone justamente eso como entrenamiento: recorrer el sistema con su tabla de comandos básicos, desde un usuario sin privilegios.

### Cómo funciona

No hay disco C ni disco D: todo cuelga de `/`, y cada disco extra se monta en una carpeta, como `/srv/datos`. La configuración vive en `/etc`; lo que cambia con el uso, como logs, caché de paquetes o datos de Docker, en `/var`; las carpetas de los usuarios en `/home`. `/root` es solo la carpeta personal del administrador.

Leer no cambia nada. `pwd` te dice dónde estás, `ls -la` lista todo con permisos y dueños, `less` abre un archivo sin poder editarlo, `find` busca por nombre y `grep` busca texto adentro de los archivos. Con `grep -rn` recorrés una carpeta entera y te devuelve archivo, número de línea y texto.

Cada programa tiene tres canales: entrada, salida y errores. La tubería lleva la salida de uno a la entrada del siguiente: `ps aux | grep sshd` filtra la lista de procesos. Los errores van por su propio canal, y `2>/dev/null` los descarta: por eso `find /etc -name "*sshd*" 2>/dev/null` no te llena la pantalla de Permission denied cuando corrés como usuario común.

El truco de la Debian Reference para que grep no se encuentre a sí mismo es `grep "[s]shd"`. El patrón busca una s seguida de shd, y la línea del propio grep dice `[s]shd`, que no coincide.
""",
  [{"file": "1-t1.svg", "after": "filtra la lista de procesos",
    "alt": "Animación en cuatro tiempos. 1: a la izquierda, ps aux lista seis procesos de ejemplo: init, journald, dos de sshd, una bash y el propio grep [s]shd. 2: puntos de colores viajan por la tubería, del cuadro de ps al de grep. 3: las líneas que no dicen sshd se apagan, las dos de sshd quedan en verde y aparecen a la derecha como resultado. 4: la línea del propio grep se marca en ámbar y una nota explica que el patrón [s]shd busca una s seguida de shd, y que el texto grep [s]shd no lo contiene, por eso no aparece.",
    "caption": "La salida de ps entra a grep, y el corchete deja afuera al propio grep."}],
  S("Recorrer un equipo sin tocar nada",
    "Solo lee: muestra dónde estás, lista una carpeta, busca archivos de configuración por nombre, busca una palabra con número de línea y lista los procesos de un servicio. No necesita sudo.",
    [("CARPETA", "/etc/ssh", "Carpeta a revisar"), ("PALABRA", "Port", "Texto a buscar dentro de los archivos"), ("PROCESO", "sshd", "Nombre del servicio o proceso")],
    r'''
# IES Training - Linux - Recorrer un equipo sin tocar nada
# Solo lee: no usa sudo ni cambia la configuracion.
ies_recorrer() {
  local carpeta="{{CARPETA}}"
  local palabra="{{PALABRA}}"
  local proceso="{{PROCESO}}"
  echo "== Donde estoy =="
  pwd
  echo "== Contenido de $carpeta =="
  ls -la "$carpeta" 2>/dev/null || echo "No existe $carpeta o no tengo permiso para listarla"
  echo "== Archivos en /etc con '$proceso' en el nombre =="
  find /etc -name "*${proceso}*" 2>/dev/null
  echo "== Lineas con '$palabra' en $carpeta (archivo:linea:texto) =="
  grep -rn "$palabra" "$carpeta" 2>/dev/null || echo "Sin coincidencias"
  echo "== Procesos de $proceso (sin el propio grep) =="
  ps aux | grep "[${proceso:0:1}]${proceso:1}" || echo "No hay procesos de $proceso"
  echo "Listo: recorrido sin cambios. Para leer un archivo entero: less $carpeta/<archivo>"
}
ies_recorrer
''',
    [PEGAR, "Correlo como usuario común: lo que diga Permission denied es un archivo protegido, no un error del script.",
     "No abre editores ni escribe archivos: es la regla de la lección, primero se lee."]))

# =====================================================================================  2
L("2",
  {"file": "2.svg", "alt": "A la izquierda, cada letra vale un número: r igual 4, leer; w igual 2, escribir; x igual 1, ejecutar o entrar; rwx suma 7, r-x 5, rw- 6 y r-- 4. Debajo, tres cifras para tres categorías: 7 dueño, 5 grupo, 5 resto. A la derecha, los valores de siempre: 755 rwxr-xr-x para directorios y programas, 644 rw-r--r-- para archivos de datos, 600 rw------- para secretos como llaves y claves, 2770 rwxrws--- para una carpeta compartida de un grupo, y en rojo 777 rwxrwxrwx, cualquiera escribe, nunca.",
   "caption": "Tres cifras, una por categoría, cada una suma de 4, 2 y 1."},
  [{"file": "2-paso2.svg", "step": 2, "after": "Carpeta compartida con setgid",
    "alt": "Terminal con chown root:tecnicos /srv/obra, chmod 2770 y ls -ld, que muestra drwxrws--- 2 root tecnicos; la s en el lugar de ejecución del grupo se marca como setgid activo. Nota: 2770 es setgid más dueño rwx, grupo rwx y resto nada. Abajo, el usuario tec1, del grupo tecnicos, crea plano.txt en /srv/obra y el archivo queda con grupo tecnicos; el usuario nobody, fuera del grupo, intenta listar y recibe Permission denied.",
    "caption": "Con la s del setgid, todo lo que se crea adentro queda del grupo de la carpeta."},
   {"file": "2-paso4.svg", "step": 4, "after": "Permisos recursivos sin volver ejecutable",
    "alt": "Dos árboles iguales, obra con la carpeta planos y los archivos plano.txt, fotos.zip y notas.txt. A la izquierda, en rojo, chmod -R 755 deja todos los archivos como rwxr-xr-x, ejecutables. A la derecha, en verde, con find por tipo los directorios quedan rwxrws--- y los archivos rw-rw----. Debajo, los dos comandos: find /srv/obra -type d -exec chmod 2770 y find /srv/obra -type f -exec chmod 660. Nota: con -R un solo número va a directorios y archivos por igual.",
    "caption": "find separa directorios y archivos para darle a cada uno lo suyo."}],
  [C("Permisos en números (r=4, w=2, x=1)",
     "Unix necesitaba una forma compacta de decir quién puede hacer qué con cada archivo. Tres derechos por tres categorías entran en tres cifras.",
     "Cada cifra es la suma de 4 (leer), 2 (escribir) y 1 (ejecutar, o entrar si es un directorio), para dueño, grupo y resto en ese orden. 755 para directorios y programas, 644 para datos, 600 para secretos. ls -l muestra lo mismo en letras.",
     "Una llave privada SSH con 644 hace que SSH la rechace por estar demasiado abierta: `chmod 600 ~/.ssh/id_ed25519` y anda."),
   C("Grupos en lugar de 777",
     "Cuando dos usuarios o un software y un técnico tienen que escribir en el mismo lugar, el atajo es 777, que abre la carpeta a todo el equipo. El grupo da acceso solo a quien corresponde.",
     "Se crea el grupo con groupadd, se suma cada usuario con `usermod -aG` (la a es la que agrega; sin ella se reemplazan sus grupos) y la carpeta queda con `chown root:grupo`. El grupo nuevo vale desde la próxima sesión del usuario.",
     "El software del NVR no puede escribir en /srv/grabaciones. En vez de 777, sumás su usuario al grupo de la carpeta con `usermod -aG` y le das 2770."),
   C("setgid en directorios",
     "Sin setgid, cada archivo nuevo toma el grupo principal de quien lo crea, y una carpeta compartida se llena de archivos que el resto del grupo no puede tocar.",
     "Con el 2 delante (2770), lo que se crea adentro hereda el grupo de la carpeta. ls -ld lo muestra como una s en el lugar de la x del grupo. Para aplicarlo a una carpeta que ya tiene contenido, find por tipo.",
     "En /srv/obra, tec1 sube un plano y tec2 lo puede corregir al rato: el archivo nació del grupo tecnicos, no del grupo personal de tec1.")],
  """
### Un poco de historia

El modelo de permisos de Linux viene del Unix original: cada archivo tiene un dueño, un grupo y tres juegos de derechos, de lectura, escritura y ejecución, para el dueño, para el grupo y para el resto. Es un modelo simple, y por eso sobrevivió: un servidor Debian 13 decide hoy quién puede escribir en una carpeta con la misma lógica.

Con los años se sumaron piezas: los bits especiales setuid, setgid y sticky; las ACL para casos finos, que se notan por un + al final de los permisos en `ls -l`; y sudo, para dar privilegios de administrador por comando en lugar de compartir la clave de root. En Ubuntu 26.04, sudo pasó a ser sudo-rs, una reescritura en Rust: `sudo -E` se ignora con un aviso y para pasar una variable se usa la opción preserve-env con su nombre.

### Cómo funciona

Cada derecho vale un número: r=4, w=2, x=1. Se suman por categoría: 7 es rwx, 6 es rw-, 5 es r-x y 4 es r--. Así 755 se lee como dueño todo, grupo y resto leen y entran; 644 como dueño lee y escribe, el resto solo lee; y 600 como solo el dueño.

En un directorio, x significa poder atravesarlo: sin x no entrás con cd aunque tengas r. Por eso los directorios llevan x y los archivos de datos no.

Cuando un proceso quiere abrir un archivo, el kernel pregunta en orden: si el usuario es el dueño, usa los permisos del dueño; si no, y está en el grupo, los del grupo; si no, los del resto. Vale la primera categoría que coincide, no la más generosa.

Los permisos de lo nuevo salen de la umask: con 0022, un archivo nace 644 y un directorio 755. El setgid en un directorio, el 2 de 2770, hace que lo creado adentro herede el grupo de la carpeta y no el grupo principal de quien lo crea. El sticky bit, como en /tmp, impide borrar archivos ajenos.

Ojo con usermod: `-aG` agrega al usuario a un grupo; sin la a, reemplaza todos sus grupos secundarios. Y la Debian Reference recuerda que dar sudo sin contraseña solo tiene sentido en una estación de un único usuario.
""",
  [{"file": "2-t1.svg", "after": "Vale la primera categoría que coincide",
    "alt": "Animación en cuatro tiempos sobre la carpeta /srv/obra, dueño root, grupo tecnicos, permisos rwx, rws y tres guiones. Abajo, las tres preguntas en orden: ¿es el dueño?, ¿está en el grupo?, si no, el resto. 1: el usuario tec1 quiere crear un archivo. 2: no es root, se marca en rojo el bloque del dueño y el kernel pasa a la pregunta del grupo. 3: tec1 está en tecnicos, se marca en verde el bloque del grupo, el acceso se permite y plano.txt nace con grupo tecnicos por el setgid. 4: el usuario nobody no es dueño ni del grupo, cae en el resto, con tres guiones, y recibe Permission denied.",
    "caption": "El kernel usa la primera categoría que coincide: dueño, grupo o resto."}],
  S("Carpeta compartida para un grupo de técnicos",
    "Crea el grupo si falta, suma un usuario existente al grupo y deja la carpeta con dueño root, grupo del equipo, 2770 en directorios y 660 en archivos. Se puede correr varias veces.",
    [("GRUPO", "tecnicos", "Grupo que comparte la carpeta"), ("USUARIO", "tec1", "Usuario existente que se suma al grupo"), ("CARPETA", "/srv/obra", "Carpeta compartida")],
    r'''
# IES Training - Linux - Carpeta compartida para un grupo
# Probalo primero en una VM de laboratorio. Correlo como root (sudo -i).
ies_carpeta_grupo() {
  local grupo="{{GRUPO}}"
  local usuario="{{USUARIO}}"
  local carpeta="{{CARPETA}}"
  if [ "$(id -u)" -ne 0 ]; then echo "Correlo como root: sudo -i"; return 1; fi
  # Grupo: se crea solo si no existe
  if ! grep -q "^${grupo}:" /etc/group; then
    groupadd "$grupo" && echo "Grupo $grupo creado"
  fi
  # Usuario: -aG agrega sin sacarle sus otros grupos
  if id "$usuario" >/dev/null 2>&1; then
    usermod -aG "$grupo" "$usuario"
    id "$usuario"
  else
    echo "El usuario $usuario no existe: crealo antes con adduser $usuario"
  fi
  # Carpeta con setgid: lo nuevo hereda el grupo
  mkdir -p "$carpeta"
  chown root:"$grupo" "$carpeta"
  find "$carpeta" -type d -exec chmod 2770 {} \;
  find "$carpeta" -type f -exec chmod 660 {} \;
  ls -ld "$carpeta"
  echo "Listo: $carpeta del grupo $grupo con 2770. Verifica con: sudo -u $usuario touch $carpeta/prueba.txt"
}
ies_carpeta_grupo
''',
    [ROOT, "No crea usuarios: adduser pide la contraseña y conviene hacerlo a mano.",
     "El grupo nuevo vale desde la próxima sesión del usuario: que cierre y vuelva a entrar.",
     "No cambia el dueño de los archivos que ya estaban: solo el grupo de la carpeta y los permisos."]))

# =====================================================================================  4
L("4",
  {"file": "4.svg", "alt": "Cuatro pasos en fila: 1, copia sshd_config.original protegida con chmod a-w; 2, cambio en el directorio sshd_config.d, en 10-ies.conf, con el original intacto; 3, validación con sudo sshd -t, donde sin salida significa que está bien; 4, en verde, recarga con systemctl reload ssh con otra sesión abierta. Una flecha roja vuelve de la validación al cambio: el error dice archivo y línea, se corrige y se vuelve a validar. Abajo, tabla de validadores: SSH con sshd -t, red en Ubuntu con netplan generate, discos con findmnt -x, sudoers con visudo -c y nginx con nginx -t. Notas: el cambio va en un archivo propio del directorio .d para que una actualización no lo pise; un error en sshd_config con SSH como único acceso te deja afuera.",
   "caption": "Copia, archivo .d, validación y recién ahí recarga; si falla, se vuelve al cambio."},
  [{"file": "4-paso2.svg", "step": 2, "after": "Mirá qué snippets ya existen",
    "alt": "Terminal con ls -l /etc/ssh/sshd_config.d/ que lista dos archivos de ejemplo, 10-ies.conf y 50-cloud-init.conf. Debajo, el orden en que sshd arma su configuración: 1, la primera línea de /etc/ssh/sshd_config con el Include de sshd_config.d; 2, 10-ies.conf, el propio, que se lee primero por su número bajo; 3, 50-cloud-init.conf, después, en orden alfabético; 4, el resto del archivo principal. A la derecha, en verde: en OpenSSH gana el primer valor leído, así que el snippet gana sobre el archivo principal y 10-ies sobre 50-cloud-init. Nota: 50-cloud-init.conf es un ejemplo de lo que puede aparecer en una imagen de nube.",
    "caption": "Los snippets se leen primero y en orden alfabético: el número bajo gana."},
   {"file": "4-paso4.svg", "step": 4, "after": "Error a propósito, para ver cómo lo marca",
    "alt": "Terminal de una VM de laboratorio: se agrega PasswordAuthentication yess al snippet, sshd -t responde /etc/ssh/sshd_config.d/10-ies.conf line 2: unsupported option yess, con el archivo y la línea marcados; sed borra la línea con yess, sshd -t no dice nada y se recarga SSH. Dos tarjetas: en rojo, si hubieras hecho restart el servicio falla y queda caído y por SSH nadie más entra hasta arreglarlo desde la consola; en verde, con sshd -t primero el error aparece en pantalla, el servicio sigue con la configuración vieja y se recarga recién después de validar.",
    "caption": "sshd -t te da archivo y línea, y el servicio sigue andando mientras corregís."}],
  [C("Directorio .d y archivo propio",
     "El archivo principal de un servicio es del paquete: cuando se actualiza, apt pregunta qué hacer con tus cambios o los mezcla con los del fabricante. Un archivo propio al lado evita ese choque.",
     "Tu cambio va en un archivo con nombre propio dentro del directorio .d del servicio (sshd_config.d, apt.conf.d, journald.conf.d). Se leen en orden alfabético, por eso se numeran. Antes de sumar el tuyo, conviene mirar qué snippets ya existen.",
     "En un servidor Ubuntu de un cliente, el banner legal de SSH va en `/etc/ssh/sshd_config.d/10-ies.conf`. Cuando el paquete openssh-server se actualiza, el archivo principal se renueva y tu banner sigue ahí."),
   C("En OpenSSH gana el primer valor",
     "OpenSSH lee su configuración de arriba abajo y, para la mayoría de las opciones, se queda con el primer valor que encuentra. Si no lo sabés, un cambio al final del archivo parece no funcionar.",
     "Como el Include de sshd_config.d está en la primera línea, lo que pongas en un snippet gana sobre el archivo principal, y entre snippets gana el de número más bajo. `sudo sshd -T` imprime la configuración efectiva para comprobar qué quedó.",
     "Apagaste las contraseñas al final de sshd_config y siguen entrando con clave. `sshd -T | grep -i passwordauth` dice yes: un 50-cloud-init.conf lo estaba fijando antes."),
   C("Validar antes de reiniciar",
     "Un error de tipeo en la configuración de un servicio crítico, reiniciado a ciegas, deja el servicio caído. Si es SSH y es tu único acceso, quedás afuera.",
     "Cada servicio trae su validador: `sshd -t`, `netplan generate`, `findmnt -x`, `visudo -c`, `nginx -t`. Se corre después de editar y antes de recargar; si dice algo, te da el archivo y la línea. Con `&&`, la recarga solo se ejecuta si la validación salió bien.",
     "Un compañero cambia el puerto de SSH en un gateway remoto. `sudo sshd -t && sudo systemctl reload ssh` atrapa la línea mal escrita y el gateway sigue accesible.")],
  """
### Un poco de historia

Durante años, cambiar un servicio era editar su archivo principal. El problema aparecía al actualizar: el paquete traía una versión nueva y apt preguntaba qué hacer con tus cambios, o tus líneas quedaban mezcladas con las del fabricante. La solución que se generalizó en Debian fueron los directorios `.d`: el paquete es dueño del archivo principal y vos agregás uno propio al lado, que se lee en orden alfabético. Así trabajan `apt.conf.d`, `sources.list.d`, `sshd_config.d` y `journald.conf.d`.

OpenSSH sumó la directiva Include en su versión 7.3, de 2016, y Ubuntu arranca su sshd_config con `Include /etc/ssh/sshd_config.d/*.conf`. El Debian Handbook cuenta el caso clásico que motiva esta lección: un "yess" en la línea 28 de sshd_config y ssh.service que no vuelve a arrancar.

### Cómo funciona

OpenSSH tiene una regla que sorprende: para la mayoría de las opciones vale el primer valor que lee, no el último. Como el Include está arriba, todo lo que pongas en un snippet gana sobre el archivo principal. Y entre snippets gana el que va primero en orden alfabético: por eso se numeran, y `10-ies.conf` va antes que un `50-cloud-init.conf`.

El validador lee la configuración igual que el servicio, pero sin aplicarla. `sshd -t` no dice nada si está todo bien y, si hay un error, te da el archivo y la línea. `sshd -T` va más allá: imprime la configuración efectiva, con el valor que quedó para cada opción. Cada servicio trae el suyo: `netplan generate`, `findmnt -x` para fstab, `visudo -c` para sudoers, `nginx -t`.

El orden importa porque reiniciar con un error deja el servicio caído. El propio ssh.service de Debian corre `sshd -t` antes de arrancar y antes de recargar: con un error, no levanta. `reload` le pide al proceso que relea la configuración sin cortar las sesiones abiertas; `restart` lo baja y lo vuelve a levantar.

La copia cierra el método: `cp` a `.original` y `chmod a-w` te dejan un punto de vuelta que nadie pisa sin querer. En un equipo remoto, se recarga con otra sesión abierta y se prueba entrar desde una nueva antes de cerrar la que funciona.
""",
  [{"file": "4-t1.svg", "after": "no el último. Como el Include está arriba",
    "alt": "Animación en cuatro tiempos. A la izquierda, cuatro bloques en el orden en que sshd los lee: la primera línea de /etc/ssh/sshd_config con el Include de sshd_config.d, el snippet 10-ies.conf con PasswordAuthentication no, el snippet 50-cloud-init.conf con PasswordAuthentication yes, y el resto del archivo principal con PasswordAuthentication yes. 1: un cursor marca la línea del Include. 2: el cursor baja a 10-ies.conf, que se marca en verde, y el panel de la derecha fija el valor no. 3: los dos bloques que dicen yes se apagan con la etiqueta ignorado. 4: sshd -T con grep muestra passwordauthentication no.",
    "caption": "El primer valor leído es el que queda; los que vienen después se ignoran."}],
  S("Cambio en sshd_config.d con copia y validación",
    "Guarda una copia protegida del sshd_config original (solo la primera vez), escribe el snippet con el banner, valida con sshd -t y recarga solo si está bien. Si la validación falla, borra el snippet y no toca el servicio.",
    [("SNIPPET", "10-ies.conf", "Nombre del archivo en sshd_config.d"), ("BANNER", "/etc/issue.net", "Archivo con el texto del banner")],
    r'''
# IES Training - Linux - Cambio en sshd_config.d con copia y validacion
# Probalo en una VM de laboratorio, con la consola abierta. Correlo como root (sudo -i).
ies_snippet_ssh() {
  local snippet="/etc/ssh/sshd_config.d/{{SNIPPET}}"
  local banner="{{BANNER}}"
  if [ "$(id -u)" -ne 0 ]; then echo "Correlo como root: sudo -i"; return 1; fi
  # 1. Copia del original, una sola vez y protegida contra escritura
  if [ ! -e /etc/ssh/sshd_config.original ]; then
    cp /etc/ssh/sshd_config /etc/ssh/sshd_config.original
    chmod a-w /etc/ssh/sshd_config.original
    echo "Copia guardada en /etc/ssh/sshd_config.original"
  fi
  # 2. Snippets que ya existen (pueden fijar valores antes que el tuyo)
  ls -l /etc/ssh/sshd_config.d/
  # 3. Tu cambio en un archivo propio (se reescribe igual si lo corres de nuevo)
  echo "Banner $banner" > "$snippet"
  # 4. Validacion: si falla, se borra el snippet y no se toca el servicio
  if sshd -t; then
    systemctl reload ssh
    sshd -T | grep -i "^banner"
    echo "Listo: $snippet validado y SSH recargado. Proba entrar desde OTRA terminal antes de cerrar esta."
  else
    rm -f "$snippet"
    echo "sshd -t encontro un error (arriba dice archivo y linea): borre $snippet y SSH sigue como estaba."
  fi
}
ies_snippet_ssh
''',
    [ROOT, "Usa reload y no restart: las sesiones abiertas no se cortan.",
     "Si sshd -t marca un error en otro archivo (no en el tuyo), el script no lo arregla: leé la línea que indica y corregila a mano.",
     "Para volver atrás: borrá el snippet, sshd -t y systemctl reload ssh."]))

# =====================================================================================  5
L("5",
  {"file": "5.svg", "alt": "A la izquierda, dos órdenes distintas: systemctl start ssh lo arranca ahora, pero si se corta la luz al volver no arranca solo; systemctl enable ssh, en verde, lo engancha al arranque en multi-user.target y vuelve solo después de cada reinicio. Nota: un servicio que tiene que volver tras un corte lleva start y enable, y se revisa con systemctl is-enabled. A la derecha, el método ante un servicio caído: 1, systemctl status ssh para ver si está activo o caído y desde cuándo; 2, journalctl -u ssh -n 20 para el error real con archivo y línea; 3, el arreglo; 4, systemctl status ssh para confirmar active running. Pie: reiniciar a ciegas borra la pista, primero se lee.",
   "caption": "start y enable son dos cosas; y ante una falla, status, journal, arreglo y status."},
  [{"file": "5-paso2.svg", "step": 2, "after": "Rompé la configuración a propósito",
    "alt": "Terminal de la consola de la VM con un ejemplo. systemctl status ssh muestra ssh.service, Loaded con la unidad y enabled marcado como arranca al bootear, y Active: failed marcado en rojo como está caído. Después, journalctl -u ssh -n 20 muestra en ámbar el mensaje de sshd: /etc/ssh/sshd_config.d/99-roto.conf line 1: unsupported option yess. Tres tarjetas: Loaded dice si encontró la unidad y si está habilitada; Active dice active running, inactive o failed y desde cuándo; journalctl -u muestra el mensaje del propio sshd con archivo, línea y opción mala.",
    "caption": "status dice que está caído; el journal dice qué línea lo tumbó."},
   {"file": "5-paso4.svg", "step": 4, "after": "Filtros de journalctl para obra",
    "alt": "Cuatro tarjetas con comandos: journalctl -b -1 -p err para los errores del arranque anterior, lo que pasó antes del corte o del reinicio; journalctl -u ssh -S \"1 hour ago\" para un servicio desde un momento; journalctl -f para ver en vivo, como tail -f, con Ctrl+C para salir; du -sh /var/log/journal para saber cuánto ocupa el journal. Abajo, la escala de prioridades de 0 a 7: emerg, alert, crit, err, warning, notice, info y debug; las cuatro primeras, hasta err, en rojo: es lo que se ve con -p err.",
    "caption": "-b elige el arranque, -u la unidad, -S el momento y -p la gravedad."}],
  [C("Unidad de systemd (.service)",
     "Los scripts de arranque viejos eran programas de shell, cada uno con su forma de arrancar, parar y vigilar. systemd los reemplazó por declaraciones: el archivo dice qué correr y systemd se encarga del resto.",
     "Un .service tiene tres secciones: [Unit] con la descripción y el orden, [Service] con el comando y cómo reiniciarlo, e [Install] con el target donde se engancha. Los del paquete están en /lib/systemd/system y los tuyos van en /etc/systemd/system. systemctl status te muestra cuál se cargó.",
     "En el ssh.service de Debian se ve `ExecStartPre=/usr/sbin/sshd -t`: antes de arrancar, systemd valida la configuración. Por eso un yess en un snippet deja el servicio en failed en vez de a medio arrancar."),
   C("start contra enable",
     "Arrancar un servicio y hacer que arranque solo son dos decisiones distintas. Confundirlas deja equipos que andan hasta el primer corte de luz.",
     "`start` lo levanta ahora; `enable` crea el enlace en multi-user.target.wants para que arranque en cada booteo. `is-enabled` responde enabled o disabled. Un servicio crítico lleva las dos cosas.",
     "Instalaste el servicio de un gestor de accesos con start y anduvo toda la semana. El lunes, después de un corte, no estaba: le faltaba `systemctl enable`."),
   C("journalctl y el arranque anterior",
     "Los logs de texto quedaban repartidos en archivos y sin relación con el servicio que los escribió. journald guarda cada línea con su unidad, su prioridad y el arranque al que pertenece.",
     "`journalctl -u servicio` muestra solo esa unidad; `-p err` filtra errores y lo más grave; `-S` desde un momento; `-f` en vivo; `-b -1` el arranque anterior. El journal ocupa disco: `du -sh /var/log/journal` dice cuánto.",
     "Un NVR se reinició de madrugada y nadie sabe por qué. `sudo journalctl -b -1 -p err` muestra los errores del arranque anterior, justo antes del reinicio.")],
  """
### Un poco de historia

Durante décadas, Linux arrancó con el init de System V: scripts de shell que se ejecutaban uno detrás de otro, en orden numérico, por niveles de ejecución. Funcionaba, pero era lento y cada script reinventaba cómo arrancar, parar y vigilar su servicio. Ubuntu probó Upstart, basado en eventos, y en 2010 Lennart Poettering y Kay Sievers presentaron systemd. Debian lo adoptó por defecto en Jessie, Debian 8, en 2015, y Ubuntu ese mismo año. Hoy Debian 13 y Ubuntu 24.04 y 26.04 arrancan con systemd, y su journal es el primer lugar donde mirar.

### Cómo funciona

El arranque tiene una cadena fija. El firmware, BIOS o UEFI, inicia el hardware y lanza el cargador, GRUB en Debian y Ubuntu. GRUB carga el kernel y un initramfs, un sistema de archivos mínimo en RAM con lo justo para encontrar el disco raíz. Con la raíz montada, el kernel arranca el primer proceso, el PID 1: systemd.

systemd no ejecuta una lista en orden: lee unidades declarativas. Un `.service` dice cómo arrancar un programa, en tres secciones: [Unit] con la descripción y el orden, [Service] con el comando, e [Install] con el target donde se engancha. Un `.target` es un estado del sistema: `local-fs.target` es discos montados y `multi-user.target` es sistema listo, con red y consola. systemd arranca en paralelo todo lo que cada target necesita.

Ahí está la diferencia entre start y enable. `start` levanta el servicio ahora. `enable` crea un enlace en `multi-user.target.wants/` para que se arranque en el próximo booteo. Un servicio con start y sin enable anda hasta el primer corte de luz.

journald guarda lo que dicen los servicios y el propio arranque, cada línea con su unidad y su prioridad, de 0 (emerg) a 7 (debug). Por eso `journalctl -u ssh` muestra solo lo de SSH, `-p err` filtra errores y lo más grave, y `-b -1` trae el arranque anterior: lo que pasó antes del reinicio.

`systemctl status` junta todo en una pantalla: si la unidad está cargada y habilitada, si está activa, desde cuándo, y las últimas líneas del journal. Por eso es lo primero que se mira, antes de reiniciar nada.
""",
  [{"file": "5-t1.svg", "after": "el kernel arranca el primer proceso, el PID 1",
    "alt": "Animación en cinco tiempos del arranque de un servidor Debian o Ubuntu. Arriba, cuatro cajas en fila: firmware (BIOS o UEFI), GRUB, kernel con initramfs y systemd como PID 1, que se encienden una tras otra. 1: el firmware inicia el hardware y lanza el cargador. 2: GRUB carga el kernel y el initramfs. 3: el kernel monta la raíz y arranca systemd. 4: debajo aparecen los targets local-fs, network-online y multi-user, y los servicios habilitados que cuelgan de multi-user.target.wants: ssh, nftables y cron. 5: en la franja del journal aparecen líneas del kernel y de systemd, como Reached target local-fs.target y Started ssh.service, y se recuerda que journalctl -b -1 muestra el arranque anterior.",
    "caption": "Firmware, GRUB, kernel y systemd; después, los targets y lo habilitado."}],
  S("Diagnóstico de un servicio con systemctl y journalctl",
    "Muestra el estado del servicio, si arranca al bootear, las unidades caídas, sus últimas líneas de log, los errores del arranque anterior y el tamaño del journal. Solo habilita el servicio si lo pedís con la variable HABILITAR.",
    [("SERVICIO", "ssh", "Servicio a revisar"), ("LINEAS", "20", "Cantidad de líneas de log"), ("HABILITAR", "no", "si = hacer enable si está deshabilitado")],
    r'''
# IES Training - Linux - Diagnostico de un servicio
# Solo lee, salvo que HABILITAR sea "si". Correlo como root (sudo -i).
ies_diagnostico() {
  local svc="{{SERVICIO}}"
  local n="{{LINEAS}}"
  local habilitar="{{HABILITAR}}"
  echo "== Estado de $svc =="
  systemctl status "$svc" --no-pager -n 0
  echo "== Arranca al bootear =="
  local estado
  estado=$(systemctl is-enabled "$svc" 2>/dev/null)
  echo "$svc: ${estado:-desconocido}"
  echo "== Unidades caidas =="
  systemctl list-units | grep -i failed || echo "Ninguna"
  echo "== Ultimas $n lineas del journal de $svc =="
  journalctl -u "$svc" -n "$n" --no-pager
  echo "== Errores del arranque anterior =="
  journalctl -b -1 -p err --no-pager 2>/dev/null | tail -n "$n" || echo "Sin arranque anterior guardado"
  echo "== Tamano del journal =="
  du -sh /var/log/journal 2>/dev/null
  # enable solo si lo pediste y si estaba deshabilitado
  if [ "$habilitar" = "si" ] && [ "$estado" = "disabled" ]; then
    systemctl enable "$svc" && echo "$svc habilitado: va a arrancar en cada booteo"
  fi
  echo "Listo: diagnostico de $svc. En vivo: journalctl -u $svc -f"
}
ies_diagnostico
''',
    [ROOT, "No reinicia nada: el método es leer primero. El restart lo decidís vos después de ver el error.",
     "journalctl -b -1 necesita el journal guardado en disco (/var/log/journal); si no existe, solo hay datos del arranque actual."]))

# =====================================================================================  10
L("10",
  {"file": "10.svg", "alt": "Terminal con free -h de ejemplo: total 7,8Gi, used 2,1Gi, free 0,9Gi marcado en rojo, buff/cache 4,8Gi y available 5,4Gi marcado en verde. Debajo, una barra con los 7,8 GB de RAM: 2,1 GB usados por programas, 4,8 GB de caché de disco y 0,9 GB libres; una llave verde abarca la mayor parte de la caché y la parte libre: available, unos 5,4 GB, lo que se le puede dar a un programa sin ir a swap. Notas: free bajo es normal porque Linux usa la RAM que sobra como caché y la suelta cuando un programa la pide; muchas herramientas de monitoreo alertan mirando free y un servidor sano puede figurar en presión de memoria.",
   "caption": "La caché se libera cuando un programa la pide: available es lo que de verdad queda."},
  [{"file": "10-paso1.svg", "step": 1, "after": "Memoria y carga:",
    "alt": "Terminal con uptime de ejemplo, 153 días encendido y load average 0,52, 0,61 y 0,70, y nproc que responde 4. Nota: los tres números son promedios de 1, 5 y 15 minutos de procesos corriendo o esperando turno. Una escala de 0 a 8 para 4 núcleos: en verde por debajo de 4 hay lugar, en ámbar cerca o arriba de 4 está llena, en rojo sostenida arriba es saturación; dos rayas marcan 0,52 y 0,70, tranquilo. Dos tarjetas: carga alta y available bajo, falta memoria o un proceso se la come, top con Shift+M; carga alta y available alto, es CPU o disco, top con Shift+P.",
    "caption": "La carga se lee contra la cantidad de núcleos que da nproc."},
   {"file": "10-paso3.svg", "step": 3, "after": "Señales, con un proceso de prueba",
    "alt": "Terminal de ejemplo: sleep 600 & devuelve [1] 12345; pgrep -a sleep muestra 12345 sleep 600, marcado como el PID para kill; kill 12345; pgrep -a sleep ya no muestra nada. A la derecha, de menos a más: en verde, systemctl restart servicio, si es un servicio systemd lo baja y lo levanta; kill PID, SIGTERM 15, le pide terminar y el programa cierra y guarda; en rojo, kill -9 PID, SIGKILL, el kernel lo saca y nada se guarda, último recurso. Nota: el & deja el sleep en segundo plano para practicar sin riesgo.",
    "caption": "Primero se pide con kill; kill -9 queda para cuando el pedido no alcanza."}],
  [C("available contra free",
     "Linux usa la RAM que sobra como caché de disco para no volver a leer lo que ya leyó. Esa memoria no figura como libre, y mirada de apuro parece que falta RAM.",
     "En `free -h`, available estima cuánto se le puede dar a un programa sin ir a swap, contando la caché que se puede soltar. Es la columna que importa; free bajo es normal en un servidor que lleva días encendido.",
     "El monitoreo de un cliente alerta \"memoria al 95 %\" en el servidor de video. `free -h` muestra available en 5 GB: la alerta mira free, no available, y no hace falta comprar RAM."),
   C("Carga y núcleos",
     "Un número de carga suelto no dice nada: 4 es poco en un equipo de 16 núcleos y saturación en uno de 2. Hace falta compararlo con la capacidad.",
     "uptime da la carga promedio de 1, 5 y 15 minutos; nproc dice cuántos núcleos hay. Una carga sostenida por encima de nproc es saturación. top con Shift+P ordena por CPU y con Shift+M por memoria.",
     "Un gateway Linux anda lento en horario pico. uptime marca 3,9 con nproc 4: está al límite, y top muestra qué proceso se lleva la CPU."),
   C("Señales: SIGTERM, SIGKILL y SIGHUP",
     "Hace falta una forma de avisarle algo a un proceso desde afuera: que termine, que relea su configuración. Las señales son ese aviso, identificado con un número.",
     "`kill PID` manda SIGTERM (15), un pedido que el programa atrapa para cerrar prolijo. `kill -9` manda SIGKILL, que no se puede atrapar: el kernel lo saca y lo que estaba escribiendo queda a medias. SIGHUP (1) se usa para pedir que relea la configuración. A un servicio, `systemctl restart`.",
     "Un proceso de exportación de video se colgó. `kill 4321` y a los segundos ya no está, con el archivo cerrado; solo si sigue ahí, `kill -9 4321`.")],
  """
### Un poco de historia

Las señales son de los mecanismos más viejos de Unix: una forma de avisarle algo a un proceso desde afuera, con un número. Los números quedaron fijos y por eso se usan igual en cualquier Linux: 15 es SIGTERM, 9 es SIGKILL y 1 es SIGHUP. La Debian Reference las lista junto con top y lsof como las herramientas básicas para mirar procesos.

Con la memoria pasó otra cosa. Durante años, free mostraba una cifra libre bajísima y muchos técnicos concluían que faltaba RAM. En 2014, el kernel 3.14 sumó MemAvailable, una estimación de cuánta memoria se puede dar a un programa sin ir a swap, y free la muestra en la columna available. Aun así, linuxblog.io advierte que muchas herramientas de monitoreo siguen alertando por free y marcan problemas que no existen.

### Cómo funciona

Linux usa la RAM que sobra como caché de disco: guarda lo que leyó para no leerlo de nuevo. Esa memoria figura como buff/cache y no como free, pero se libera apenas un programa la pide. Por eso el Server B del ejemplo de linuxblog.io, con 153 días encendido, muestra free bajo y anda perfecto: available es la cifra que importa.

La carga de uptime son tres promedios, de 1, 5 y 15 minutos, de procesos corriendo o esperando turno. Se compara con nproc: una carga sostenida por encima de la cantidad de núcleos es saturación.

Cada proceso tiene un PID y un padre; en la raíz está systemd, el PID 1. Para terminar uno se le manda una señal. `kill PID` envía SIGTERM: un pedido. El programa puede atraparlo, cerrar sus archivos y salir prolijo. `kill -9` envía SIGKILL: el kernel lo saca sin avisarle, y lo que estaba escribiendo queda a medias. Por eso va como último recurso.

SIGHUP es el clásico pedido de releer la configuración: el reload del ssh.service de Debian manda `kill -HUP` al proceso principal. Y si el que consume es un servicio, `systemctl restart` es mejor que kill: systemd lo baja con su señal de parada, espera y lo vuelve a levantar, y queda registrado en el journal.
""",
  [{"file": "10-t1.svg", "after": "lo que estaba escribiendo queda a medias",
    "alt": "Animación en cuatro tiempos con dos carriles, el mismo proceso grabador 1502 escribiendo video.mp4. Arriba, kill 1502: 1: viaja la señal 15, SIGTERM. 2: el proceso la atrapa, pasa a cierra y guarda, y el archivo queda cerrado completo en verde. Abajo, kill -9 1502: 3: viaja la señal 9, SIGKILL, y el proceso aparece eliminado sin pasar por ningún cierre. 4: el archivo queda en rojo, cortado a la mitad.",
    "caption": "Con SIGTERM el programa cierra prolijo; con SIGKILL queda todo a medias."}],
  S("Memoria, carga y quién consume",
    "Muestra memoria con la columna available, la carga contra los núcleos y los cinco procesos que más memoria y CPU usan. Solo termina un proceso si cargás su PID, y siempre con SIGTERM.",
    [("PID", "", "PID a terminar con SIGTERM (vacío = no terminar nada)"), ("CANTIDAD", "5", "Procesos a listar")],
    r'''
# IES Training - Linux - Memoria, carga y quien consume
# Solo lee, salvo que cargues un PID: en ese caso manda SIGTERM, nunca -9.
ies_recursos() {
  local pid="{{PID}}"
  local cant="{{CANTIDAD}}"
  echo "== Memoria (mira la columna available) =="
  free -h
  echo "== Carga de 1, 5 y 15 minutos contra nucleos =="
  uptime
  echo "Nucleos: $(nproc)"
  echo "== Los $cant que mas memoria usan (%MEM) =="
  ps aux | sort -rnk 4 | head -n "$cant"
  echo "== Los $cant que mas CPU usan (%CPU) =="
  ps aux | sort -rnk 3 | head -n "$cant"
  if [ -n "$pid" ]; then
    if [ "$pid" -le 1 ] 2>/dev/null || [ "$pid" = "$$" ]; then
      echo "Ese PID no se toca."; return 1
    fi
    ps -p "$pid" -o pid,user,cmd || { echo "No existe el PID $pid"; return 1; }
    kill "$pid" && echo "SIGTERM enviado a $pid"
    sleep 5
    if ps -p "$pid" >/dev/null; then
      echo "Sigue vivo. Si es un servicio: systemctl restart. Ultimo recurso: kill -9 $pid"
    else
      echo "Termino prolijo."
    fi
  fi
  echo "Listo: revisado. Para mirar en vivo: top (Shift+M memoria, Shift+P CPU, q sale)"
}
ies_recursos
''',
    [PEGAR, "Para terminar procesos de otros usuarios hace falta sudo -i antes.",
     "Nunca manda kill -9: si el proceso no responde a SIGTERM, la decisión la tomás vos.",
     "Si el que consume es un servicio, mejor systemctl restart que kill."]))

# =====================================================================================  3
L("3",
  {"file": "3.svg", "alt": "Tres columnas. apt update baja la lista: pregunta al repositorio qué versiones hay y no instala nada, todos los días. apt upgrade, en verde, instala lo nuevo: actualiza paquetes sin quitar ninguno, con regularidad. apt full-upgrade, en ámbar, puede quitar paquetes: instala y quita lo que haga falta, para el salto de versión mayor, planificado y con backup. Abajo, en verde, la seguridad automática: unattended-upgrades aplica solo seguridad una vez por día, Ubuntu lo trae y en Debian 13 se verifica, con registro en /var/log/apt/history.log. En ámbar, el reinicio lo decidís vos: Automatic-Reboot viene en false; gateway o NVR desatendido, hora fija de madrugada; servidor con gente de día, ventana acordada.",
   "caption": "Tres comandos con tres riesgos distintos, y el reinicio como decisión aparte."},
  [{"file": "3-paso2.svg", "step": 2, "after": "Instalá (si falta) y activá las actualizaciones",
    "alt": "Terminal con apt install unattended-upgrades, dpkg-reconfigure -plow unattended-upgrades y cat del archivo 20auto-upgrades. Debajo, el archivo /etc/apt/apt.conf.d/20auto-upgrades con las dos líneas en verde: APT::Periodic::Update-Package-Lists \"1\", que baja las listas cada día, y APT::Periodic::Unattended-Upgrade \"1\", que instala la seguridad cada día. Notas: dpkg-reconfigure pregunta si se quieren activar y con Sí escribe este archivo, en Ubuntu ya viene así; si un valor está en \"0\", esa parte no corre y el equipo queda sin parches aunque el paquete esté instalado.",
    "caption": "Con los dos valores en \"1\", las listas y la seguridad se actualizan cada día."},
   {"file": "3-paso5.svg", "step": 5, "after": "Reinicio automático a hora fija",
    "alt": "El archivo /etc/apt/apt.conf.d/52reinicio-ies con Automatic-Reboot \"true\" y Automatic-Reboot-Time \"04:30\". Debajo, terminal de ejemplo: ls /var/run/reboot-required encuentra la marca y cat de reboot-required.pkgs muestra el paquete del kernel nuevo; si existe la marca, un paquete espera un reinicio para usarse. A la derecha, en verde, para gateway, NVR o equipo desatendido: Automatic-Reboot true a las 04:30, reinicia solo si hace falta, de madrugada. En ámbar, para accesos, central IP o gente de día: Automatic-Reboot false, se reinicia a mano en una ventana acordada mirando la marca.",
    "caption": "La marca reboot-required avisa; el archivo propio decide cuándo reiniciar."}],
  [C("update, upgrade y full-upgrade",
     "Instalar a mano cada versión nueva con sus dependencias era inmanejable. APT separa tres pasos para que cada uno tenga su riesgo a la vista.",
     "`apt update` baja las listas y no instala nada; `apt upgrade` instala lo nuevo sin quitar paquetes; `apt full-upgrade` puede quitar e instalar dependencias y se reserva para el salto de versión, planificado y con backup. En scripts se usa apt-get, que tiene interfaz estable. Todo queda en /var/log/apt/history.log.",
     "Un cliente dice que \"algo cambió solo\" en su servidor de accesos. `grep -A3 \"Start-Date\" /var/log/apt/history.log | tail -20` muestra qué se actualizó y cuándo."),
   C("unattended-upgrades",
     "Un gateway sin parches es el eslabón débil de la red, y nadie se acuerda de actualizarlo a mano todas las semanas. unattended-upgrades aplica la seguridad solo.",
     "Corre una vez por día con timers de systemd y aplica solo seguridad. 20auto-upgrades lo activa con dos valores en \"1\"; 50unattended-upgrades define orígenes, lista negra y reinicio. Un repositorio agregado a mano no entra si no sumás su origen.",
     "El Debian 13 que corre la VPN de un depósito tiene unattended-upgrades activo: el parche de OpenSSL de un viernes ya está instalado el sábado sin que nadie entre."),
   C("Reinicio pendiente",
     "Algunos paquetes, como el kernel, solo se usan después de reiniciar. Un reinicio automático a media tarde es tan malo como uno que nunca llega.",
     "Esos paquetes dejan la marca /var/run/reboot-required y la lista en reboot-required.pkgs. Automatic-Reboot viene en \"false\"; en un archivo propio se activa con una hora fija de madrugada, o se reinicia a mano en una ventana.",
     "En el NVR de un edificio de Pocitos, `Automatic-Reboot-Time \"04:30\"`. En el servidor de accesos de una empresa, false, y el reinicio se coordina con el cliente un sábado temprano.")],
  """
### Un poco de historia

Debian resolvió temprano un problema que en otros sistemas se arreglaba a mano: instalar software con todas sus dependencias desde un repositorio firmado. dpkg instala un paquete .deb suelto; APT, que nació en Debian a fines de los noventa, sumó lo que faltaba: bajar listas de repositorios, calcular dependencias y actualizar todo junto. `apt-get` quedó como la herramienta estable para scripts y `apt` como la cómoda para usar a mano.

Las actualizaciones automáticas llegaron con unattended-upgrades: Ubuntu lo instala por defecto y aplica solo seguridad una vez por día; en Debian 13 se verifica y, si falta, se instala. Ubuntu 26.04 trajo cambios que rompen guías viejas: apt-key ya no existe y las llaves de los repositorios van en /etc/apt/keyrings, referenciadas con Signed-By.

### Cómo funciona

Un repositorio publica listas de paquetes firmadas. `apt update` baja esas listas: no instala nada, solo actualiza lo que tu equipo sabe que existe. `apt upgrade` instala las versiones nuevas sin quitar ningún paquete. `apt full-upgrade` puede quitar e instalar dependencias para completar la actualización: es la que se usa para un salto de versión, y se planifica con backup.

Todo queda anotado en /var/log/apt/history.log: qué se instaló, cuándo y con qué comando. Es lo primero que se mira cuando algo cambió solo.

unattended-upgrades corre con dos timers de systemd: uno baja las listas y otro instala lo de seguridad. El archivo 20auto-upgrades lo activa con dos valores en "1"; 50unattended-upgrades define qué orígenes se aplican, qué paquetes se excluyen y qué hacer con el reinicio. Ubuntu considera más riesgoso no aplicar seguridad que aplicarla: si un paquete molesta, se bloquea ese paquete en vez de apagar todo.

Algunos paquetes, como el kernel, solo se usan después de reiniciar: dejan la marca /var/run/reboot-required y la lista en reboot-required.pkgs. Automatic-Reboot viene en "false": o lo activás con una hora fija de madrugada, o reiniciás vos en una ventana acordada.

En Debian conviene usar el nombre trixie en los repositorios y no stable: así, cuando salga la próxima versión, el equipo no salta solo.
""",
  [{"file": "3-t1.svg", "after": "corre con dos timers de systemd",
    "alt": "Animación en cuatro tiempos sobre una línea de 24 horas, con un punto que recorre el día. 1: apt-daily.timer baja las listas de paquetes. 2: más tarde, apt-daily-upgrade.timer corre unattended-upgrades e instala solo seguridad; aparece el registro en history.log con openssl y un kernel nuevo. 3: aparece en ámbar la marca /var/run/reboot-required. 4: el punto llega a las 04:30 y, con Automatic-Reboot en true, el equipo reinicia; con false, espera la ventana acordada. Las horas de los timers son de ejemplo.",
    "caption": "Listas, seguridad, marca de reinicio y reinicio a la hora que elegiste."}],
  S("Actualizaciones automáticas con reinicio a hora fija",
    "Actualiza las listas, muestra lo pendiente, instala unattended-upgrades si falta, deja los dos valores en \"1\" y escribe el archivo propio de reinicio. Muestra si hay un reinicio pendiente; no reinicia.",
    [("REINICIO_AUTO", "false", "true = reinicia solo a la hora fijada (equipo desatendido)"), ("HORA", "04:30", "Hora del reinicio automático")],
    r'''
# IES Training - Linux - Actualizaciones automaticas con reinicio a hora fija
# Probalo en una VM de laboratorio. Correlo como root (sudo -i).
ies_actualizaciones() {
  local auto="{{REINICIO_AUTO}}"
  local hora="{{HORA}}"
  if [ "$(id -u)" -ne 0 ]; then echo "Correlo como root: sudo -i"; return 1; fi
  apt-get update
  echo "== Pendiente (simulado, no instala) =="
  apt-get -s upgrade | grep ^Inst || echo "Nada pendiente"
  # Se instala solo si falta (si ya esta, apt no hace nada)
  apt-get install -y unattended-upgrades
  # Los dos valores en "1": listas y seguridad cada dia
  printf 'APT::Periodic::Update-Package-Lists "1";\nAPT::Periodic::Unattended-Upgrade "1";\n' > /etc/apt/apt.conf.d/20auto-upgrades
  # Reinicio en un archivo propio
  printf 'Unattended-Upgrade::Automatic-Reboot "%s";\nUnattended-Upgrade::Automatic-Reboot-Time "%s";\n' "$auto" "$hora" > /etc/apt/apt.conf.d/52reinicio-ies
  cat /etc/apt/apt.conf.d/20auto-upgrades /etc/apt/apt.conf.d/52reinicio-ies
  echo "== Reinicio pendiente =="
  if [ -e /var/run/reboot-required ]; then
    cat /var/run/reboot-required.pkgs 2>/dev/null
  else
    echo "No hay reinicio pendiente"
  fi
  echo "Listo: seguridad automatica activa, reinicio automatico = $auto ($hora). Revisa: less /var/log/unattended-upgrades/unattended-upgrades.log"
}
ies_actualizaciones
''',
    [ROOT, "Viene con REINICIO_AUTO en false: ponelo en true solo en equipos desatendidos (gateway, NVR).",
     "No corre full-upgrade ni reinicia: el salto de versión mayor se planifica con backup.",
     "Reescribe 20auto-upgrades con los dos valores en \"1\": si alguien lo había apagado a propósito, preguntá antes."]))

# =====================================================================================  6
L("6",
  {"file": "6.svg", "alt": "Una escalera de cinco escalones que suben de izquierda a derecha, cada uno con su comando. 1, interfaz con IP: ip -br addr e ip route; si falla, cable, DHCP o IP fija. 2, gateway: ping -c3 192.168.88.1; si falla, VLAN o gateway mal cargado. 3, IP pública: ping -c3 1.1.1.1; si falla, ruta o salida del router. 4, nombre DNS, resaltado: dig debian.org +short; si falla, revisar los nameservers. 5, puerto y servicio: ss -tlnp y curl -sI; si falla, servicio caído o filtrado. Nota: subir de abajo hacia arriba y anotar cada escalón; si la IP pública responde y el nombre no, es DNS.",
   "caption": "Cada escalón se prueba con un comando; el primero que falla es el problema."},
  [{"file": "6-paso1.svg", "step": 1, "after": "Subí la escalera y anotá el resultado",
    "alt": "Terminal de ejemplo: ip -br addr muestra lo UNKNOWN con 127.0.0.1/8 y ens18 UP con 192.168.88.50/24, con el nombre de la interfaz, el estado UP y la IP con máscara marcados; ip route muestra default via 192.168.88.1 dev ens18, marcado, y la red 192.168.88.0/24. Nota en verde: la línea default via dice por dónde sale todo lo que no es de la red local, y si falta no hay internet aunque la IP esté bien. Tabla de traducción de net-tools a iproute2: ifconfig a ip addr, route a ip route, arp a ip neigh y netstat a ss. Nota: usar el nombre que muestra ip -br addr, eth0 ya no es la norma.",
    "caption": "Interfaz arriba, IP con máscara y una ruta por defecto: el primer escalón."},
   {"file": "6-paso2.svg", "step": 2, "after": "IP fija en Ubuntu con netplan",
    "alt": "El archivo /etc/netplan/90-ies.yaml con la configuración de la lección: network, version 2, ethernets, ens18, dhcp4 false, addresses 192.168.88.50/24, routes to default via 192.168.88.1 y nameservers 192.168.88.1 y 1.1.1.1. Etiquetas: la interfaz es la de ip -br addr, la IP fija va con máscara, la ruta por defecto es el gateway y los nameservers son el escalón 4. A la derecha, chmod 600, netplan generate y netplan try; sin Enter en 120 segundos vuelve atrás solo. Nota en ámbar: dos espacios por nivel, nunca tabulaciones y espacio después de los dos puntos.",
    "caption": "YAML con dos espacios por nivel, permisos 600, generate para validar y try para aplicar."}],
  [C("Diagnóstico en escalera",
     "\"No anda internet\" puede ser un cable, un gateway, el ISP o el DNS. Sin método se prueba al azar; la escalera ordena las pruebas de la capa más baja a la más alta.",
     "Interfaz con IP y ruta (ip -br addr, ip route), gateway (ping), IP pública (ping 1.1.1.1), nombre (ping a un dominio, dig), y puerto o servicio (ss -tlnp, curl). Se sube sin saltear escalones y se anota cada resultado: el primero que falla es el problema.",
     "Un NVR en un local del Centro no sube las grabaciones a la nube. Ping al gateway y a 1.1.1.1 andan, pero `dig` no resuelve: tiene cargado un DNS viejo. Lo arreglás en la red del NVR sin tocar el router."),
   C("iproute2 en lugar de net-tools",
     "ifconfig, route y arp son de otra época y en muchos servidores ya no vienen instalados. iproute2 reúne todo en un solo comando, ip, y suma ss para los sockets.",
     "ip addr (o ip -br addr) para interfaces e IP, ip route para rutas, ip neigh para la tabla ARP, ss -tlnp para lo que escucha. Son comandos de lectura: no cambian nada mientras no uses add o del.",
     "Te pasan una guía vieja que dice ifconfig y el servidor contesta command not found. `ip -br addr` te da lo mismo, en una línea por interfaz."),
   C("netplan try",
     "Cambiar la IP de un equipo al que entrás por red es la forma clásica de quedarte afuera. netplan try aplica el cambio con red de seguridad.",
     "netplan lee YAML de /etc/netplan (con permisos 600). `netplan generate` valida la sintaxis; `netplan try` aplica y espera 120 segundos a que confirmes con Enter: si perdiste la conexión, vuelve solo a lo anterior. `netplan apply` no tiene esa vuelta. En Debian con ifupdown no hay try.",
     "Pasás un servidor de accesos de DHCP a IP fija por SSH. Con `netplan try`, si te equivocaste en el gateway, a los dos minutos vuelve solo y no hay que mandar a nadie a la consola.")],
  """
### Un poco de historia

Durante años, la red de Linux se manejó con net-tools: ifconfig, route, arp y netstat. A fines de los noventa apareció iproute2, que maneja interfaces, direcciones y rutas con un solo comando, `ip`, y los sockets con `ss`. La Debian Reference tiene una tabla de traducción y una lista de comandos seguros, que solo leen: ip addr show, ip route show, ip neigh, ss, dig, tracepath y mtr.

La configuración también cambió. Debian servidor sigue con ifupdown y /etc/network/interfaces. Ubuntu Server usa netplan desde 2017: archivos YAML en /etc/netplan que netplan traduce para systemd-networkd. Y los nombres de interfaz pasaron de eth0 a nombres predecibles como ens18 o enp0s31f6, que dicen dónde está conectada la placa: en es cableada, p0 el bus, s31 la ranura.

### Cómo funciona

La red se diagnostica en escalera, de abajo hacia arriba, y el primer escalón que falla es el problema. Primero, ¿la interfaz tiene IP? `ip -br addr` lo muestra en una línea por interfaz, y `ip route` dice si hay ruta por defecto. Segundo, ¿llego al gateway? Un ping a 192.168.88.1. Tercero, ¿salgo a internet? Un ping a una IP pública, como 1.1.1.1. Cuarto, ¿resuelvo nombres? Si la IP pública responde y debian.org no, es DNS: hay que revisar los nameservers. Quinto, ¿el servicio responde? `ss -tlnp` dice qué escucha y en qué dirección, y `curl` prueba un servicio real.

La resolución de nombres sigue el orden de /etc/nsswitch.conf: con `hosts: files dns`, primero se mira /etc/hosts y después el DNS de /etc/resolv.conf. Por eso una línea vieja en /etc/hosts puede ganarle al DNS.

Para una IP fija, netplan lee YAML: dos espacios de sangría, nunca tabulaciones, y el archivo con permisos 600, porque si no avisa que está demasiado abierto. `netplan generate` valida la sintaxis. `netplan try` aplica el cambio y espera 120 segundos a que confirmes con Enter: si el cambio te dejó sin conexión, no podés confirmar y vuelve solo a la configuración anterior. `netplan apply` no tiene esa vuelta.

En Debian con ifupdown no hay try: la IP fija va en /etc/network/interfaces, con auto para que levante al bootear, y cambiar la IP de un equipo remoto se hace con la consola de la VM o de Proxmox a mano.
""",
  [{"file": "6-t1.svg", "after": "Si la IP pública responde y debian.org no, es DNS",
    "alt": "Animación en cuatro tiempos con cuatro escalones que suben de izquierda a derecha. 1: interfaz, ip -br addr muestra ens18 UP con 192.168.88.50/24, en verde. 2: gateway, ping a 192.168.88.1 con 3 paquetes recibidos, en verde. 3: IP pública, ping a 1.1.1.1 con 3 recibidos, en verde. 4: nombre, ping a debian.org falla con Temporary failure in name resolution, en rojo, y un recuadro dice que si la IP pública responde y el nombre no, es DNS y hay que revisar los nameservers.",
    "caption": "Tres escalones en verde y el cuarto en rojo: el problema es el DNS."},
   {"file": "6-t2.svg", "after": "vuelve solo a la configuración anterior",
    "alt": "Animación en cuatro tiempos con dos líneas de tiempo de 0 a 120 segundos. Arriba, un cambio que anda: 1: netplan try aplica la IP nueva y empieza a contar. 2: el técnico sigue conectado, aprieta Enter y la IP nueva queda fija. Abajo, un cambio que deja afuera: 3: la sesión SSH se corta y no hay forma de apretar Enter. 4: el contador llega a 120 segundos y netplan vuelve solo a la configuración anterior, y se puede volver a entrar.",
    "caption": "Con Enter el cambio queda; sin Enter, a los 120 s vuelve solo."}],
  S("Escalera de red, de abajo hacia arriba",
    "Solo lee: muestra interfaces y ruta por defecto, prueba gateway, IP pública y nombre, y lista lo que escucha. Se detiene en el primer escalón que falla y te dice cuál es.",
    [("GATEWAY", "192.168.88.1", "Gateway de la red"), ("IP_PUBLICA", "1.1.1.1", "IP pública para probar salida"), ("NOMBRE", "debian.org", "Nombre para probar el DNS")],
    r'''
# IES Training - Linux - Escalera de red
# Solo lee: no cambia IP, rutas ni DNS. Se detiene en el primer escalon que falla.
ies_escalera() {
  local gw="{{GATEWAY}}"
  local ip="{{IP_PUBLICA}}"
  local nombre="{{NOMBRE}}"
  echo "== 1. Interfaces e IP =="
  ip -br addr
  echo "== 1. Ruta por defecto =="
  ip route | grep default || { echo "FALLA en el escalon 1: no hay ruta por defecto"; return 1; }
  echo "== 2. Gateway $gw =="
  ping -c3 "$gw" >/dev/null && echo "OK" || { echo "FALLA en el escalon 2: no llego al gateway"; return 1; }
  echo "== 3. IP publica $ip =="
  ping -c3 "$ip" >/dev/null && echo "OK" || { echo "FALLA en el escalon 3: no salgo a internet"; return 1; }
  echo "== 4. Nombre $nombre =="
  if ping -c3 "$nombre" >/dev/null 2>&1; then
    echo "OK"
    dig "$nombre" +short 2>/dev/null
  else
    echo "FALLA en el escalon 4: la IP publica responde y el nombre no. Es DNS: revisa los nameservers."
    return 1
  fi
  echo "== 5. Que escucha y en que direccion =="
  ss -tlnp
  echo "Listo: los cuatro primeros escalones andan. Para un servicio real: curl -sI deb.debian.org | head -3"
}
ies_escalera
''',
    [PEGAR, "No cambia la IP: para eso, el YAML de la lección y netplan try a mano.",
     "Si dig no está instalado, el escalón 4 se prueba igual con ping; en Debian viene en el paquete bind9-dnsutils.",
     "Sin sudo, ss no muestra el proceso: correlo con sudo -i para ver qué programa escucha."]))

# =====================================================================================  7
L("7",
  {"file": "7.svg", "alt": "A la izquierda, la notebook del técnico (tecnico@notebook-2026) con la llave privada ~/.ssh/id_ed25519 en rojo, permisos 600, que no se copia nunca, y la pública ~/.ssh/id_ed25519.pub en verde, que se puede copiar. Una flecha ssh-copy-id lleva la pública al servidor 192.168.88.50, al archivo ~/.ssh/authorized_keys del usuario tecnico, con permisos 600, dentro de ~/.ssh con 700. Abajo, el orden que no te deja afuera: ssh-keygen -t ed25519, ssh-copy-id a tu usuario, entrar con la llave sin pedir clave, apagar la clave en sshd_config.d y probar en otra terminal. Pie en rojo: la sesión que funciona no se cierra hasta que una nueva entra con la llave.",
   "caption": "La pública viaja al servidor; la privada se queda en tu notebook."},
  [{"file": "7-paso3.svg", "step": 3, "after": "En el servidor, con esta sesión abierta",
    "alt": "El archivo /etc/ssh/sshd_config.d/10-ies-acceso.conf con PasswordAuthentication no, KbdInteractiveAuthentication no y PermitRootLogin no. Debajo, en la terminal de la sesión abierta, sshd -t && systemctl reload ssh, y sshd -T con grep, que muestra permitrootlogin no y passwordauthentication no en verde. A la derecha, qué hace cada línea: nadie entra con contraseña, se cierra la otra puerta de clave y root no entra por SSH. Nota: sshd -T muestra el valor en uso; si dice yes, otro snippet con número más bajo lo fija antes.",
    "caption": "Tres líneas en un archivo propio, validadas y comprobadas con sshd -T."},
   {"file": "7-paso4.svg", "step": 4, "after": "Desde OTRA terminal, probá que",
    "alt": "Dos terminales. La A, la que funciona, sigue conectada a tecnico@192.168.88.50 y queda abierta como salida de emergencia. En la B, nueva, ssh -o PubkeyAuthentication=no responde Permission denied (publickey), y ssh normal entra sin pedir la clave del servidor. Recuadro verde: las dos cosas que querés ver, sin llave rechazado y con llave adentro. Recuadro rojo: si B no entra con la llave, desde A se borra el snippet, sshd -t y reload; si ya se cerró A, la salida es la consola de la VM o del hipervisor.",
    "caption": "Sin llave, rechazado; con llave, adentro; y la primera sesión, siempre abierta."}],
  [C("Llave ed25519",
     "Las contraseñas se comparten, se anotan y se adivinan: un servidor con SSH abierto recibe intentos de bots en minutos. Una llave reemplaza el secreto que viaja por uno que nunca sale de tu equipo.",
     "`ssh-keygen -t ed25519 -C \"tecnico@notebook-2026\"` crea dos archivos: la privada, que queda en tu notebook con 600 y una frase de paso, y la pública, que va al servidor. El comentario identifica la llave en authorized_keys. RSA solo para equipos viejos; DSA ya no existe en OpenSSH 10.",
     "Cada técnico de IES tiene su propia llave con su nombre en el comentario. Cuando alguien deja la empresa, se borra su línea de authorized_keys en los servidores y listo, sin cambiar la clave de nadie."),
   C("ssh-copy-id y authorized_keys",
     "Copiar la pública a mano es fácil de hacer mal: un salto de línea o un permiso abierto y la llave no anda. ssh-copy-id lo hace en un paso.",
     "`ssh-copy-id tecnico@192.168.88.50` agrega tu pública a ~/.ssh/authorized_keys del usuario en el servidor. SSH exige ~/.ssh en 700 y authorized_keys en 600. Si no entra, `sudo journalctl -fu ssh` en el servidor muestra el motivo mientras probás.",
     "En un LXC nuevo de Proxmox, `ssh-copy-id` con la clave inicial y la próxima vez entrás sin que te la pida. Recién ahí se apaga la contraseña."),
   C("Apagar la contraseña sin quedar afuera",
     "Apagar la contraseña antes de probar la llave es la forma más rápida de perder el acceso a un servidor remoto.",
     "Primero se entra con la llave; después, en un archivo de sshd_config.d, PasswordAuthentication no, KbdInteractiveAuthentication no y PermitRootLogin no; `sshd -t` y reload. Con la sesión abierta, se prueba desde otra terminal. fail2ban es opcional con solo llaves: OpenSSH ya trae PerSourcePenalties.",
     "En el gateway de un depósito, aplicás el snippet con una sesión abierta. Desde otra terminal, `ssh -o PubkeyAuthentication=no` da Permission denied y con la llave entrás: recién ahí cerrás la primera.")],
  """
### Un poco de historia

SSH nació en 1995: Tatu Ylönen, en la Universidad Tecnológica de Helsinki, lo escribió después de un ataque que capturaba contraseñas que viajaban en claro por la red, como pasaba con telnet. En 1999 el proyecto OpenBSD lanzó OpenSSH, la versión libre que hoy viene en Debian y Ubuntu.

Las llaves también cambiaron. DSA fue eliminado en OpenSSH 10.0, RSA quedó para compatibilidad con equipos viejos, y ed25519, de curva elíptica, es la que recomienda Ubuntu y la que ssh-keygen genera por defecto. Ubuntu 26.04 trae OpenSSH 10.2, con intercambio de claves post cuántico por defecto y PerSourcePenalties activo, que penaliza a las direcciones que fallan la autenticación.

### Cómo funciona

Una llave son dos archivos. La privada, `~/.ssh/id_ed25519`, queda en tu notebook con permisos 600. La pública, `id_ed25519.pub`, se copia al servidor, en `~/.ssh/authorized_keys` del usuario. `ssh-copy-id` hace esa copia.

Al conectarte, el cliente ofrece la pública. Si el servidor la encuentra en authorized_keys, le pide una prueba: el cliente firma datos de esa sesión con la privada y el servidor verifica la firma con la pública. La privada nunca viaja, y la frase de paso solo sirve para descifrarla en tu equipo. No hay contraseña que adivinar por fuerza bruta, y un servidor comprometido no expone tu credencial.

El orden es lo que te salva: primero copiás la llave y entrás con ella; recién después apagás la contraseña con `PasswordAuthentication no` y `KbdInteractiveAuthentication no` en un archivo de sshd_config.d, junto con `PermitRootLogin no`. El valor por defecto de OpenSSH para root es prohibit-password, root solo con llave; prohibit-password tiene sentido cuando un proceso automatizado, como un backup, entra como root con llave.

SSH es exigente con los permisos: `~/.ssh` en 700 y authorized_keys en 600; si están más abiertos, ignora la llave. Para ver por qué no entra, `sudo journalctl -fu ssh` en el servidor mientras probás.

fail2ban es opcional con solo llaves: PerSourcePenalties y un firewall que limite el origen cubren lo principal. Y la regla que no se negocia: la sesión que funciona no se cierra hasta que una nueva entra con la llave.
""",
  [{"file": "7-t1.svg", "after": "La privada nunca viaja, y la frase de paso",
    "alt": "Animación en cuatro tiempos con la notebook a la izquierda, con la llave privada id_ed25519 en rojo y la pública en verde, y el servidor a la derecha, con authorized_keys. 1: la llave pública viaja por la red hacia el servidor. 2: el servidor la encuentra en authorized_keys y devuelve un pedido de prueba. 3: en la notebook se resalta la privada y se arma la firma con la privada y los datos de la sesión; viaja solo la firma, con la leyenda la privada no viaja. 4: el servidor verifica la firma con la pública y registra Accepted publickey for tecnico, sin contraseña.",
    "caption": "Viajan la pública y la firma; la privada se queda en la notebook."}],
  S("Solo llaves en SSH, sin quedarte afuera",
    "Revisa que el usuario tenga al menos una llave en authorized_keys y permisos correctos. Solo si la tiene, escribe el snippet que apaga la contraseña y el login de root, valida con sshd -t y recarga.",
    [("USUARIO", "tecnico", "Usuario que entra con llave"), ("SNIPPET", "10-ies-acceso.conf", "Archivo en sshd_config.d")],
    r'''
# IES Training - Linux - Solo llaves en SSH
# Correlo como root (sudo -i) con tu sesion abierta, y proba desde OTRA terminal.
ies_solo_llaves() {
  local usuario="{{USUARIO}}"
  local snippet="/etc/ssh/sshd_config.d/{{SNIPPET}}"
  local home="/home/$usuario"
  if [ "$(id -u)" -ne 0 ]; then echo "Correlo como root: sudo -i"; return 1; fi
  id "$usuario" >/dev/null 2>&1 || { echo "No existe el usuario $usuario"; return 1; }
  # Sin llave cargada no se apaga nada: asi no te quedas afuera
  if ! grep -qE "^(ssh-ed25519|ssh-rsa|ecdsa-)" "$home/.ssh/authorized_keys" 2>/dev/null; then
    echo "$usuario no tiene llaves en $home/.ssh/authorized_keys. Primero: ssh-copy-id $usuario@<este-servidor>"
    return 1
  fi
  # Permisos que SSH exige
  chmod 700 "$home/.ssh"
  chmod 600 "$home/.ssh/authorized_keys"
  # Ojo: con PermitRootLogin no, hace falta otro usuario con sudo
  id "$usuario" | grep -qwE "sudo|wheel" || echo "Aviso: $usuario no esta en el grupo sudo."
  printf 'PasswordAuthentication no\nKbdInteractiveAuthentication no\nPermitRootLogin no\n' > "$snippet"
  if sshd -t; then
    systemctl reload ssh
    sshd -T | grep -Ei "passwordauth|permitroot"
    echo "Listo: solo llaves. Desde OTRA terminal: ssh -o PubkeyAuthentication=no $usuario@<este-servidor> tiene que dar Permission denied."
  else
    rm -f "$snippet"
    echo "sshd -t encontro un error: borre $snippet y SSH sigue como estaba."
  fi
}
ies_solo_llaves
''',
    [ROOT, "No cierres la sesión desde la que lo pegaste hasta entrar con la llave desde otra terminal.",
     "Si el aviso dice que el usuario no está en sudo, sumalo antes (usermod -aG sudo) o vas a quedar sin forma de administrar.",
     "Para volver atrás desde la sesión abierta: rm del snippet, sshd -t y systemctl reload ssh."]))

# =====================================================================================  8
L("8",
  {"file": "8.svg", "alt": "Un servidor, 192.168.88.50, en el centro. Desde la notebook de gestión, 10.10.10.25, una flecha verde de 22/tcp entra. Desde internet, 203.0.113.7, una flecha roja punteada de 22/tcp se corta con una cruz. Desde un cliente de la red local, una flecha verde con lo que el equipo sirve. A la derecha, una flecha verde saliente: permitido, para apt, DNS y NTP. Nota: entrante en deny, SSH primero y solo desde la red de gestión, después lo que el equipo sirve. Tabla: Ubuntu usa ufw, que viene apagado; Debian 13 usa nftables. Pie: antes de filtrar, que el servicio no escuche donde no hace falta; el firewall es la segunda capa.",
   "caption": "Entrante cerrado salvo SSH desde gestión y lo que el equipo sirve; saliente abierto."},
  [{"file": "8-paso1.svg", "step": 1, "after": "¿Qué escucha y dónde?",
    "alt": "Terminal de ejemplo con sudo ss -tlnp: sshd escucha en 0.0.0.0:22 y en [::]:22, marcados en ámbar, y postgres en 127.0.0.1:5432, marcado en verde. Tres tarjetas: 0.0.0.0 y [::] son todas las interfaces, IPv4 e IPv6, las ve la red y es lo que hay que filtrar; 127.0.0.1 es solo el propio equipo, desde la red no llega con o sin firewall; Process dice qué programa escucha, y si no se reconoce conviene averiguar antes de abrir.",
    "caption": "0.0.0.0 lo ve la red; 127.0.0.1 solo el propio equipo."},
   {"file": "8-paso4.svg", "step": 4, "after": "Verificá desde OTRA máquina",
    "alt": "Terminal de otra máquina de la red de gestión, con un ejemplo: nc -zv 192.168.88.50 22 responde succeeded; nmap -Pn -p 22,80,443 muestra 22/tcp open en verde y 80 y 443 filtered en rojo. Tres tarjetas: open, algo escucha y el firewall deja pasar desde ahí; closed, connection refused, llega pero nada escucha, pasa con el puerto permitido y sin servicio; filtered, no hay respuesta, timeout, un DROP del firewall lo descarta en silencio.",
    "caption": "open, closed y filtered dicen cosas distintas: servicio, nada escuchando o firewall."}],
  [C("Política deny por defecto",
     "Un firewall que permite todo y bloquea lo malo conocido siempre llega tarde. Con deny por defecto, solo pasa lo que alguien decidió abrir.",
     "Entrante en deny, saliente en allow, y se abre solo lo que el equipo sirve, con origen cuando se puede. SSH se permite antes de activar el firewall, idealmente solo desde la red de gestión. En ufw: default deny incoming, allow from la red al puerto 22 y recién ahí enable.",
     "Un servidor de video en una cadena de locales: entrante cerrado, 22 solo desde 10.10.10.0/24 (gestión de IES) y el puerto del cliente de video solo desde la red de las cajas."),
   C("Orden de reglas y estado de conexión",
     "Las reglas se leen de arriba abajo y gana la primera que coincide. Sin una regla para las conexiones ya establecidas, ni las respuestas de lo que el propio equipo pide podrían volver.",
     "En nftables, la cadena input arranca con `ct state established,related accept`, sigue con lo, con lo que el equipo sirve y con ICMP e ICMPv6; lo que no coincide cae en la política drop. Se valida con `nft -c -f` y se carga con `systemctl enable nftables`.",
     "En un Debian 13 que hace de gateway, `nft list ruleset` muestra la cadena input con policy drop; un apt update funciona porque su respuesta entra por la primera regla, la de established."),
   C("No escuchar es mejor que filtrar",
     "Un puerto filtrado sigue ahí: alcanza con un cambio en el firewall para que quede expuesto. Un servicio que no escucha en la red no se puede alcanzar desde ella.",
     "`ss -tlnp` muestra en qué dirección escucha cada servicio: 0.0.0.0 o [::] es toda la red, 127.0.0.1 es solo local. Lo que solo usa el propio equipo se configura para escuchar en 127.0.0.1. Y se verifica desde otra máquina, con nc o nmap.",
     "La base de datos del software de accesos escucha en 0.0.0.0:5432. Configurándola en 127.0.0.1 ya no se ve desde la red, aunque alguien deshabilite el firewall.")],
  """
### Un poco de historia

El filtrado de paquetes de Linux vive dentro del kernel, en netfilter. La herramienta para escribir reglas fue cambiando: iptables llegó con el kernel 2.4, en 2001, y nftables entró al kernel 3.13, en 2014, con una sintaxis única para IPv4 e IPv6. Debian usa nftables por defecto desde Buster, y el Debian Handbook aclara que los comandos iptables que quedan existen solo por compatibilidad.

ufw, Uncomplicated Firewall, nació en Ubuntu para que configurar un host simple no exigiera conocer la sintaxis completa. Ubuntu Server lo trae instalado pero deshabilitado. Por eso las dos distribuciones enseñan cosas distintas: ufw en Ubuntu, nftables directo en Debian.

### Cómo funciona

Cada paquete que llega pasa por ganchos del kernel. Los dirigidos al propio equipo pasan por la cadena input; los que lo atraviesan, como en un gateway, por forward; los que salen, por output. En cada cadena las reglas se leen de arriba abajo y la primera que coincide decide. Si ninguna coincide, se aplica la política: con policy drop, lo que no está permitido se descarta.

Por eso el orden del archivo de la lección importa. Primero `ct state established,related accept`: las respuestas de conexiones que ya existen, como tu propia sesión SSH o un apt update, pasan sin recorrer todo. Después la interfaz lo y lo que el equipo sirve, con su origen: `ip saddr 10.10.10.0/24 tcp dport 22 accept` deja SSH solo a la red de gestión. Al final, ICMP para el ping e ICMPv6, sin el cual IPv6 no funciona.

ufw escribe reglas equivalentes por vos: `ufw default deny incoming`, `ufw allow from 10.10.10.0/24 to any port 22 proto tcp` y `ufw enable`. Si activás antes de permitir SSH, te cortás. Lo que se hace con nft en vivo se pierde al reiniciar: en Debian las reglas van en /etc/nftables.conf, se validan con `nft -c -f` y se cargan con `systemctl enable nftables`.

El filtro es la segunda capa: el Debian Handbook prefiere que un servicio no escuche donde no hace falta antes que filtrarlo. La verificación se hace desde otra máquina: connection refused quiere decir que el paquete llega y nada escucha; un timeout, que un DROP lo descarta.
""",
  [{"file": "8-t1.svg", "after": "la primera que coincide decide",
    "alt": "Animación en cuatro tiempos sobre la cadena input con policy drop y cinco reglas en orden: ct state established,related accept; iif lo accept; ip saddr 10.10.10.0/24 tcp dport 22 accept; icmp type echo-request accept; meta l4proto ipv6-icmp accept; y abajo, en rojo, la política drop. 1: llega la respuesta de un apt update, coincide con la primera regla y pasa. 2: llega SSH desde 10.10.10.25, baja hasta la regla de la red de gestión y pasa. 3: llega SSH desde 203.0.113.7, no coincide con ninguna regla y cae en la política: descartado. 4: llega un ping, coincide con la regla de echo-request y pasa.",
    "caption": "Cada paquete baja por las reglas hasta la primera que coincide; si no hay, drop."}],
  S("ufw en deny con SSH solo desde gestión",
    "Pone entrante en deny y saliente en allow, permite SSH desde la red de gestión y muestra desde dónde están conectadas las sesiones SSH de ahora. Solo activa ufw si lo pedís con ACTIVAR.",
    [("RED_GESTION", "10.10.10.0/24", "Red desde la que se administra"), ("PUERTO_SSH", "22", "Puerto de SSH"), ("ACTIVAR", "no", "si = activar ufw después de revisar")],
    r'''
# IES Training - Linux - ufw en deny con SSH solo desde gestion
# Para Ubuntu con ufw. Correlo como root (sudo -i) y con la consola de la VM a mano.
ies_firewall() {
  local red="{{RED_GESTION}}"
  local puerto="{{PUERTO_SSH}}"
  local activar="{{ACTIVAR}}"
  if [ "$(id -u)" -ne 0 ]; then echo "Correlo como root: sudo -i"; return 1; fi
  ufw version >/dev/null 2>&1 || { echo "No hay ufw. En Debian 13 usa /etc/nftables.conf y nft -c -f"; return 1; }
  echo "== Que escucha y donde =="
  ss -tlnp
  # Primero la regla de SSH, despues las politicas (ufw no duplica reglas)
  ufw allow from "$red" to any port "$puerto" proto tcp
  ufw default deny incoming
  ufw default allow outgoing
  echo "== Desde donde estan conectadas las sesiones SSH ahora =="
  ss -tn state established "( sport = :$puerto )"
  # Si tu IP no esta dentro de $red, activar te corta: por eso va con ACTIVAR=si
  if [ "$activar" = "si" ]; then
    ufw --force enable
  else
    echo "ufw NO se activo. Si tu IP esta en $red, volve a correrlo con ACTIVAR=si"
  fi
  ufw status numbered
  echo "Listo: SSH permitido desde $red. Verifica desde OTRA maquina: nc -zv <ip-del-servidor> $puerto"
}
ies_firewall
''',
    [ROOT, "Viene con ACTIVAR en no: mirá la lista de sesiones SSH y confirmá que tu IP está dentro de la red de gestión antes de activarlo.",
     "Abrí después, a mano, solo lo que el equipo sirve (por ejemplo ufw allow 443/tcp).",
     "No toca nftables: en Debian 13 se usa el archivo /etc/nftables.conf de la lección."]))

# =====================================================================================  9
L("9",
  {"file": "9.svg", "alt": "A la izquierda, una terminal con df -h de ejemplo: /dev/sda2 de 31 GB al 97 % montado en /, en rojo, y /dev/sdb1 al 26 % en /srv/datos. Una flecha lleva a la terminal de du -xh -d1 /var ordenado, donde /var/log con 6,8 GB se destaca. Debajo, los sospechosos de siempre: /var/cache/apt, paquetes ya instalados, se vacía con apt-get clean; /var/log/journal, el journal sin tope, SystemMaxUse=500M; /var/log, logs de texto sin rotar, logrotate; /tmp, que en 26.04 vive en RAM, usar /var/tmp. Nota: con df -i, si los inodos están al 100 % sobran archivos chicos aunque haya espacio libre.",
   "caption": "df encuentra el sistema de archivos lleno; du, la carpeta que lo llenó."},
  [{"file": "9-paso2.svg", "step": 2, "after": "¿Qué lo llenó? (-x no cruza a otros discos)",
    "alt": "Dos terminales de ejemplo. Primer nivel: du -xh -d1 /var ordenado muestra /var/cache 180M, /var/lib 1,1G, /var/log 6,8G destacado y /var 8,2G. Segundo nivel: du sobre /var/log muestra /var/log/apt 40M, /var/log/installer 210M y /var/log/journal 6,5G en rojo. Tres tarjetas: -x no cruza a otros discos montados adentro, como /srv/datos; -d1 y sort -h muestran un nivel por vez con lo más grande al final; encontrado: el journal ocupa 6,5 GB y se le pone tope en journald.conf.d.",
    "caption": "Se baja de a un nivel por la carpeta más grande hasta encontrar al culpable."},
   {"file": "9-paso4.svg", "step": 4, "after": "Disco extra en fstab por UUID",
    "alt": "Terminal con lsblk -f, que muestra sdb1 ext4 con su UUID, que hay que anotar tal cual. Debajo, la línea de fstab de la lección con sus seis campos marcados: UUID=el-uuid-que-viste es qué disco, /srv/datos dónde se monta, ext4 el tipo, defaults,nofail,x-systemd.device-timeout=5 las opciones, 0 el dump y 2 el orden de chequeo. Tres tarjetas: en rojo, UUID y nunca /dev/sdb1, porque los nombres del kernel cambian según el orden en que aparecen los discos; en ámbar, nofail con timeout, si el disco falta arranca igual y sin el timeout systemd lo espera 90 segundos; en verde, findmnt -x valida fstab antes de reiniciar porque un error puede dejar el equipo en modo emergencia.",
    "caption": "UUID para identificar el disco, nofail con timeout y findmnt -x antes de reiniciar."}],
  [C("df contra du",
     "\"No space left on device\" no dice qué se llenó ni por qué. Hacen falta dos preguntas distintas, y por eso hay dos comandos.",
     "`df -h` mide los sistemas de archivos montados y dice cuál se llenó; `df -i` mira los inodos. `du -xh -d1` suma carpetas de a un nivel sin cruzar a otros discos; con `sort -h` lo más grande queda al final. Se baja por la carpeta más grande hasta el culpable.",
     "El servidor de video de un supermercado deja de grabar. df dice / al 97 %; du baja por /var hasta /var/log/journal con 6 GB. Se le pone tope y vuelve a grabar."),
   C("Tope al journal",
     "El journal guarda todo lo que dicen los servicios, y en un equipo con un servicio que repite errores crece hasta comerse el disco.",
     "`du -sh /var/log/journal` dice cuánto ocupa. Un archivo propio en /etc/systemd/journald.conf.d con `SystemMaxUse=500M` le pone tope permanente, y `systemctl restart systemd-journald` lo aplica. Para la caché de paquetes, `apt-get clean` libera sin riesgo.",
     "En un gateway con 16 GB de disco, `SystemMaxUse=500M` en `/etc/systemd/journald.conf.d/ies.conf` evita que un servicio que falla en loop lo deje sin espacio un fin de semana."),
   C("fstab con UUID y nofail",
     "Un disco que falta o un nombre que cambia en fstab pueden dejar un servidor sin arrancar, en modo emergencia y sin acceso remoto.",
     "Cada disco se identifica por UUID, que se ve con `lsblk -f`, nunca por /dev/sdX. `nofail` deja arrancar aunque el disco falte, y `x-systemd.device-timeout=5` evita esperarlo 90 segundos. Antes de reiniciar, `findmnt -x` valida el archivo y `mount -a` lo prueba.",
     "Un disco USB de backup en un NVR: con UUID y nofail, el día que alguien lo desenchufa el equipo arranca igual y sigue grabando.")],
  """
### Un poco de historia

df y du son de los comandos más viejos de Unix, y responden dos preguntas distintas: df mide los sistemas de archivos montados y du suma lo que ocupan las carpetas. /etc/fstab, la tabla de qué disco se monta en qué carpeta, viene de la misma tradición.

Lo que cambió es cómo se nombra cada disco. Los nombres del kernel, como /dev/sdb, se asignan en el orden en que los discos aparecen al arrancar y pueden cambiar de un arranque a otro, así que hoy se usa el UUID que muestra `lsblk -f`. systemd sumó opciones a fstab, como `x-systemd.device-timeout`. Y Ubuntu 26.04 movió /tmp a memoria, a un tmpfs con tope de la mitad de la RAM: 2 GB en un servidor de 4 GB.

### Cómo funciona

Un "no space left on device" se resuelve con dos preguntas. Primero, `df -h`: ¿qué sistema de archivos se llenó? A veces es / y a veces un disco de datos. `df -i` mira los inodos: cada archivo usa uno, y millones de archivos chicos los agotan antes que el espacio.

Después, `du -xh -d1`: ¿qué carpeta lo llenó? Suma un nivel por vez, y `-x` evita cruzar a otros discos montados adentro. Se baja de a un nivel, /var, después /var/log, hasta encontrar al culpable; `sort -h` ordena los tamaños y deja lo más grande al final.

Los sospechosos se repiten. /var/cache/apt/archives guarda cada paquete bajado: `apt-get clean` lo vacía sin riesgo. El journal crece hasta su límite: un archivo en journald.conf.d con `SystemMaxUse=500M` le pone tope. Los logs de texto que logrotate no rota. Y en 26.04, un dump grande en /tmp ocupa RAM: conviene /var/tmp.

Si df y du no coinciden, puede haber un archivo borrado que un proceso sigue teniendo abierto: el espacio no se libera hasta que el proceso lo cierra, y lsof ayuda a encontrarlo.

En fstab, cada línea tiene seis campos: qué disco (UUID=...), dónde se monta, tipo, opciones, dump y orden de chequeo. `nofail` hace que un disco ausente no frene el arranque; sin `x-systemd.device-timeout=5`, systemd lo espera 90 segundos. Un error en fstab puede dejar el equipo en modo emergencia: se valida con `findmnt -x` antes de reiniciar, con la consola a mano.
""",
  [{"file": "9-t1.svg", "after": "Se baja de a un nivel, /var, después /var/log",
    "alt": "Animación en cuatro tiempos con cuatro barras horizontales que aparecen una debajo de la otra. 1: df -h muestra el sistema de archivos / con 30 GB usados en rojo y 1 GB libre. 2: du sobre / reparte lo usado en /usr, /var, /home y otros, y /var, con 8,2 GB, queda destacada. 3: du sobre /var muestra /var/lib y /var/log, y /var/log, con 6,8 GB, se destaca. 4: du sobre /var/log muestra el journal con 6,5 GB, marcado en rojo, y aparece la solución: tope con SystemMaxUse=500M. Los tamaños son de ejemplo.",
    "caption": "De / a /var, de /var a /var/log, y ahí está el journal."}],
  S("Disco lleno: dónde, qué y tope al journal",
    "Muestra espacio e inodos, las carpetas más grandes de /var, vacía la caché de apt y deja un tope permanente al journal. Para fstab solo muestra los UUID y valida: no edita el archivo.",
    [("TOPE", "500M", "Tamaño máximo del journal"), ("CARPETA", "/var", "Carpeta donde empezar a buscar")],
    r'''
# IES Training - Linux - Disco lleno: donde, que y tope al journal
# Correlo como root (sudo -i). No edita /etc/fstab.
ies_disco() {
  local tope="{{TOPE}}"
  local carpeta="{{CARPETA}}"
  local conf=/etc/systemd/journald.conf.d/ies.conf
  if [ "$(id -u)" -ne 0 ]; then echo "Correlo como root: sudo -i"; return 1; fi
  echo "== Espacio por sistema de archivos =="
  df -h
  echo "== Inodos =="
  df -i
  echo "== Lo mas grande en $carpeta (sin cruzar a otros discos) =="
  du -xh -d1 "$carpeta" 2>/dev/null | sort -h | tail
  echo "== Limpieza segura: cache de apt =="
  apt-get clean
  echo "== Journal antes del tope =="
  du -sh /var/log/journal 2>/dev/null
  # Tope permanente en un archivo propio (solo si cambia)
  mkdir -p /etc/systemd/journald.conf.d
  if ! grep -qx "SystemMaxUse=$tope" "$conf" 2>/dev/null; then
    printf '[Journal]\nSystemMaxUse=%s\n' "$tope" > "$conf"
    systemctl restart systemd-journald
    echo "Tope del journal: $tope"
  fi
  du -sh /var/log/journal 2>/dev/null
  echo "== Discos y UUID (para fstab) =="
  lsblk -f
  echo "== Validacion de /etc/fstab =="
  findmnt -x
  echo "Listo: revisado y journal con tope $tope. Verifica con df -h"
}
ies_disco
''',
    [ROOT, "El tope del journal se aplica al reiniciar journald: si el journal ya era más grande, se achica solo hasta el tope.",
     "No toca /etc/fstab: la línea con UUID y nofail se agrega a mano, se valida con findmnt -x y se prueba con mount -a, con la consola a mano.",
     "No borra logs ni archivos a mano: si du marca otra carpeta, se decide qué hacer con ella."]))

# =====================================================================================  11
L("11",
  {"file": "11.svg", "alt": "Cuatro pasos en fila: 1, copiar, con tar czf para /etc, rsync para datos y dump para bases de datos; 2, a otro lugar, otro disco u otro servidor, para que la copia no viva con el original; 3, programar, con un timer a las 02:30 con Persistent=true o una línea de cron; 4, en verde, restaurar un archivo a /tmp y compararlo con diff. Una flecha verde punteada vuelve del cuarto al primero: si la restauración falla, el backup no existía y se corrige. Abajo, una terminal de ejemplo con ls -lh /srv/backup y dos archivos srv1-etc con fecha, y una nota: Falcot Corp, en el Debian Handbook, guarda el servidor de backup en otra sala por si hay un incendio.",
   "caption": "Copiar, llevar a otro lugar, programar y, sobre todo, restaurar para probar."},
  [{"file": "11-paso2.svg", "step": 2, "after": "Servicio y timer:",
    "alt": "Dos archivos lado a lado. backup-etc.service, con [Unit] Description=Backup de /etc y [Service] con Type=oneshot y ExecStart=/usr/local/bin/backup-etc.sh resaltados: qué hacer, corre una vez y termina. backup-etc.timer, con [Timer] OnCalendar=*-*-* 02:30:00, Persistent=true y RandomizedDelaySec=15min, e [Install] WantedBy=timers.target, resaltados. Debajo, qué significa cada línea: a las 02:30 todos los días; si estaba apagado, corre al arrancar; hasta 15 minutos de demora al azar; se engancha al habilitarlo. Recuadro verde: se habilita el timer con systemctl enable backup-etc.timer, se mira con list-timers y el log con journalctl -u backup-etc.service.",
    "caption": "El .service dice qué; el .timer dice cuándo; y se habilita el timer."},
   {"file": "11-paso3.svg", "step": 3, "after": "La prueba que importa, restaurar a /tmp",
    "alt": "Terminal de ejemplo: tar xzf del backup de /etc con -C /tmp extrae solo etc/hostname, y diff contra /etc/hostname con && echo responde restaurado OK. Debajo, el recorrido: el archivo tar.gz en /srv/backup, una flecha -C /tmp hacia /tmp/etc/hostname, lo restaurado aparte, y una flecha diff hacia /etc/hostname, el original sin tocar. Notas: listar con tar -tzvf no prueba que se pueda restaurar; restaurar sobre / sobrescribe lo actual y la prueba se hace siempre en otra carpeta.",
    "caption": "Se saca un archivo a /tmp y se compara con el original: así se prueba."}],
  [C("Backup que se prueba restaurando",
     "Un script que termina sin errores no garantiza nada: el archivo puede estar vacío, cortado o en el mismo disco que se rompió. La única prueba es sacar algo de la copia.",
     "Se restaura un archivo a otra carpeta con `tar xzf archivo -C /tmp etc/hostname` y se compara con `diff`. Listar el contenido no alcanza, y restaurar sobre / pisa lo actual. La prueba se repite cada tanto, no solo el día que se arma.",
     "En la entrega de un servidor de accesos, el acta de IES incluye la restauración de prueba: un archivo de /etc sacado del backup y comparado con diff, con la fecha."),
   C("tar, rsync y dump",
     "No todo se respalda igual: una configuración cambia poco, una carpeta de datos cambia todo el tiempo y una base de datos no se puede copiar en caliente.",
     "`tar czf` empaqueta /etc en un archivo con fecha, y un find borra los de más de 14 días. `rsync -av` copia solo lo distinto a otro equipo; con `-n` simula primero. Las bases de datos se exportan con un dump y se guarda ese archivo. La copia va siempre a otro lugar físico.",
     "En el servidor de un cliente: tar de /etc todas las noches, rsync de /srv/datos al NAS de la otra oficina, y el dump de la base del software de accesos antes del tar."),
   C("Timer de systemd con Persistent",
     "Con cron, si el equipo estaba apagado a la hora del backup, esa noche no hay copia y nadie se entera. Los timers recuperan lo perdido y dejan el resultado en el journal.",
     "Son dos archivos: el .service con Type=oneshot y el script, y el .timer con OnCalendar, Persistent=true y RandomizedDelaySec. `systemd-analyze calendar` valida la expresión, se habilita el timer y `systemctl list-timers` muestra la próxima ejecución. Para algo simple, una línea en /etc/cron.d alcanza.",
     "Un servidor en una obra se apaga de noche por cortes. Con Persistent=true, el backup de las 02:30 corre a las 07:10, cuando vuelve la luz, y queda en `journalctl -u backup-etc.service`.")],
  """
### Un poco de historia

tar es de los programas más viejos de Unix: su nombre viene de tape archive, porque nació para guardar archivos en cinta. rsync apareció en 1996, de la mano de Andrew Tridgell y Paul Mackerras, para sincronizar dos lugares copiando solo las diferencias. El Debian Handbook cuenta cómo Falcot Corp lo usa: copias diarias con enlaces duros, que parecen completas pero ocupan solo lo que cambió, en un servidor separado, en otra sala, por si hay un incendio.

Para programar, cron sigue siendo lo primero que enseña el Debian Handbook. Los timers de systemd llegaron después: trstringer los prefiere por el log y la sintaxis, y la Arch Wiki marca sus costos, dos archivos y ningún aviso por mail incorporado.

### Cómo funciona

Un backup tiene cuatro partes: qué copiar, adónde, cuándo y cómo se prueba. Para configuraciones, tar: `tar czf` arma un archivo comprimido con todo /etc, con el nombre del equipo y la fecha. Para datos que cambian, rsync, que compara origen y destino y copia solo lo distinto; con `-n` simula sin copiar. Las bases de datos no se copian en caliente: se exporta un dump.

La copia tiene que vivir en otro lugar físico: otro disco o, mejor, otro servidor. Un backup en el mismo disco se pierde con el disco.

Para programarlo, un timer de systemd son dos archivos: el .service dice qué correr, con Type=oneshot, y el .timer dice cuándo, con `OnCalendar=*-*-* 02:30:00`. Se habilita el timer, no el servicio. `Persistent=true` hace que, si el equipo estaba apagado a esa hora, el backup corra apenas arranca. `RandomizedDelaySec` reparte el arranque para que todo no corra junto. `systemd-analyze calendar` valida la expresión y `systemctl list-timers` muestra la próxima ejecución; el resultado queda en `journalctl -u backup-etc.service`. Con cron alcanza una línea en /etc/cron.d, pero la salida se pierde si no se redirige.

Y la prueba: listar el contenido no alcanza. Se restaura un archivo a /tmp con `-C` y se compara con `diff`. Restaurar sobre / sobrescribe lo actual: la prueba se hace siempre en otra carpeta.
""",
  [{"file": "11-t1.svg", "after": "si el equipo estaba apagado a esa hora",
    "alt": "Animación en cuatro tiempos sobre una línea de dos días, lunes y martes. 1: el lunes a las 02:30 el timer dispara el backup, marcado en verde. 2: el martes un corte deja el equipo apagado de la 01:00 a las 07:10, y el backup de las 02:30 queda sin correr, en rojo. 3: el equipo arranca a las 07:10 y, por Persistent=true, el backup corre en ese momento; el journal de backup-etc.service muestra Starting y Finished a las 07:10. 4: aparece la prueba que importa, restaurar etc/hostname a /tmp con tar y compararlo con diff: restaurado OK.",
    "caption": "La noche perdida se recupera al arrancar; y la prueba sigue siendo restaurar."}],
  S("Backup diario de /etc con timer y prueba de restauración",
    "Crea el script de backup con rotación, el servicio y el timer, lo habilita, fuerza una corrida y restaura etc/hostname a /tmp para compararlo con diff. Se puede correr varias veces.",
    [("DESTINO", "/srv/backup", "Carpeta destino (en producción, otro disco)"), ("HORA", "02:30", "Hora del backup diario"), ("DIAS", "14", "Días que se guardan las copias")],
    r'''
# IES Training - Linux - Backup diario de /etc con timer y prueba
# Correlo como root (sudo -i). En produccion, DESTINO es otro disco o servidor.
ies_backup() {
  local destino="{{DESTINO}}"
  if [ "$(id -u)" -ne 0 ]; then echo "Correlo como root: sudo -i"; return 1; fi
  mkdir -p "$destino"
  # 1. Script de backup (se reescribe igual cada vez)
  cat > /usr/local/bin/backup-etc.sh <<'FIN'
#!/bin/bash
set -e
destino={{DESTINO}}
archivo="$destino/$(hostname -s)-etc-$(date +%F).tar.gz"
tar czf "$archivo" /etc
find "$destino" -name "*-etc-*.tar.gz" -mtime +{{DIAS}} -delete
FIN
  chmod 750 /usr/local/bin/backup-etc.sh
  # 2. Servicio (que) y timer (cuando)
  printf '[Unit]\nDescription=Backup de /etc\n\n[Service]\nType=oneshot\nExecStart=/usr/local/bin/backup-etc.sh\n' > /etc/systemd/system/backup-etc.service
  printf '[Unit]\nDescription=Backup diario de /etc\n\n[Timer]\nOnCalendar=*-*-* {{HORA}}:00\nPersistent=true\nRandomizedDelaySec=15min\n\n[Install]\nWantedBy=timers.target\n' > /etc/systemd/system/backup-etc.timer
  systemd-analyze calendar "*-*-* {{HORA}}:00" || return 1
  systemctl daemon-reload
  systemctl enable backup-etc.timer
  systemctl start backup-etc.timer
  # 3. Una corrida ahora y su log
  systemctl start backup-etc.service
  journalctl -u backup-etc.service -n 5 --no-pager
  systemctl list-timers | grep backup
  # 4. La prueba que importa: restaurar a /tmp y comparar
  local ultimo
  ultimo=$(ls -t "$destino"/*-etc-*.tar.gz | head -1)
  mkdir -p /tmp/ies-restore
  tar xzf "$ultimo" -C /tmp/ies-restore etc/hostname
  if diff /tmp/ies-restore/etc/hostname /etc/hostname; then
    echo "Listo: backup en $ultimo y restaurado OK. Proxima corrida: systemctl list-timers | grep backup"
  else
    echo "La restauracion NO coincide: revisa el backup antes de confiar en el."
  fi
}
ies_backup
''',
    [ROOT, "El destino de ejemplo está en el mismo disco: sirve para practicar, no como backup real. En producción, otro disco o servidor.",
     "No respalda bases de datos: para eso va un dump antes del tar.",
     "Para datos que cambian, rsync a otro equipo, primero con -n para simular."]))

# =====================================================================================  12
L("12",
  {"file": "12.svg", "alt": "Arriba, las cuatro piezas de Docker: imagen, el software empaquetado, por ejemplo nginx; contenedor, la imagen corriendo, docker run -d; volumen, datos que sobreviven, en /var/lib/docker/volumes; red de Docker, cómo se hablan los contenedores sin publicar nada. Abajo, publicar un puerto en el host: en rojo, docker run -d -p 8080:80 nginx deja 0.0.0.0:8080, todas las interfaces, que Docker abre antes de las reglas de ufw y responde a la red aunque ufw diga deny; en verde, docker run -d -p 127.0.0.1:8081:80 nginx deja 127.0.0.1:8081, solo el propio host, y lo público va detrás de un proxy inverso en 80 y 443 o se filtra en la cadena DOCKER-USER. Nota: la prueba se hace desde otra máquina con nmap.",
   "caption": "Imagen, contenedor, volumen y red; y el puerto, en 127.0.0.1 salvo que haya un motivo."},
  [{"file": "12-paso3.svg", "step": 3, "after": "Desde la OTRA VM:",
    "alt": "A la izquierda, la terminal del servidor 192.168.88.50 con un ejemplo: docker run -p 8080:80 nginx, ss muestra 0.0.0.0:8080 con docker-proxy en rojo, y ufw status activo con solo 22/tcp permitido desde 10.10.10.0/24, sin nada del 8080. A la derecha, la otra VM de la misma red: nmap -Pn -p 8080,8081 muestra 8080 open en rojo y 8081 filtered. Nota: el 8081 todavía no existe. Abajo, en rojo, por qué pasa: Docker redirige el puerto publicado en la tabla nat antes de que el paquete llegue a la cadena input, donde ufw tiene sus reglas; para el kernel va por forward hacia el contenedor, por eso ufw status no lo menciona y se verifica desde otra máquina.",
    "caption": "ufw no lo menciona, pero desde la otra VM el 8080 está abierto."},
   {"file": "12-paso4.svg", "step": 4, "after": "Publicado solo para el host:",
    "alt": "Terminal del servidor con un ejemplo: docker run -p 127.0.0.1:8081:80 nginx, ss muestra 127.0.0.1:8081 con docker-proxy en verde y curl a 127.0.0.1:8081 responde HTTP/1.1 200 OK. A la derecha, el servidor 192.168.88.50 con nginx en 127.0.0.1:8081 y, desde la otra VM con nmap al 8081, una flecha roja cortada: 8081 no aparece abierto. Notas: para los datos, docker volume create datos-prueba y docker volume inspect muestra su Mountpoint; no poner iptables false en Docker porque rompe la red de los contenedores y deja sus puertos accesibles desde la red local.",
    "caption": "En 127.0.0.1 responde en el servidor y no desde la red."}],
  [C("Imagen, contenedor y volumen",
     "Instalar un software con todas sus dependencias en cada servidor era lento y frágil. Docker lo empaqueta en una imagen y lo corre aislado, sin una máquina virtual completa.",
     "La imagen es el software empaquetado; el contenedor, la imagen corriendo, que se borra y se recrea sin drama. Los datos que tienen que sobrevivir van en un volumen, que vive en /var/lib/docker/volumes. Entre contenedores alcanza con la red de Docker: no hace falta publicar puertos.",
     "Un panel de monitoreo de cámaras corre en un contenedor; su base de datos va en un volumen. Al actualizar la imagen, el contenedor se recrea y los datos siguen ahí."),
   C("Puertos publicados y ufw",
     "Docker necesita que los paquetes lleguen a la IP interna del contenedor, y para eso escribe sus propias reglas en netfilter. Esas reglas actúan antes que las de ufw.",
     "`-p 8080:80` crea una redirección en la tabla nat: el paquete va por forward hacia el contenedor y no pasa por input, donde ufw tiene sus reglas. Por eso `ufw status` dice cerrado y el puerto responde desde afuera. La verificación es con nmap o nc desde otra máquina.",
     "findstack cuenta el caso de un panel de n8n publicado con -p 5678 en un servidor con ufw en deny: quedó abierto a internet sin que nadie lo notara."),
   C("Publicar en 127.0.0.1",
     "La forma más simple de que un puerto de contenedor no quede expuesto es que no escuche en la red. Lo que tiene que ser público conviene que pase por un solo lugar controlado.",
     "`-p 127.0.0.1:8081:80` deja el servicio solo para el host; `ss -tlnp` lo confirma. Lo público va detrás de un proxy inverso en 80 y 443, o se filtra en la cadena DOCKER-USER. No se pone \"iptables\": false: según Docker, rompe la red de los contenedores y deja los puertos accesibles desde la red local.",
     "En el servidor de un cliente, todos los paneles en contenedores escuchan en 127.0.0.1 y un único proxy inverso con HTTPS publica lo que hace falta.")],
  """
### Un poco de historia

Docker apareció en 2013 y popularizó los contenedores: empaquetar un programa con todo lo que necesita y correrlo aislado sobre el kernel del propio host, sin una máquina virtual completa. Por debajo usa funciones del kernel Linux, los espacios de nombres y los cgroups, y para la red escribe solo sus reglas de netfilter. En Ubuntu, el paquete docker.io lo mantiene Canonical; en 24.04 y en 26.04 es la misma versión, la 29.1.3, y desde 26.04 se puede correr sin root.

El problema de los puertos expuestos no es teórico. findstack cuenta el caso de un panel de n8n publicado con ufw en deny que quedó abierto a internet, y cita un relevamiento de Intruder, de mayo de 2026, según el cual el 31 % de más de 5.200 servidores Ollama expuestos respondía sin credenciales.

### Cómo funciona

Cuatro piezas. La imagen es el software empaquetado, por ejemplo nginx. El contenedor es la imagen corriendo. El volumen guarda los datos que tienen que sobrevivir al contenedor, en /var/lib/docker/volumes. La red de Docker conecta contenedores entre sí sin publicar nada al host.

Publicar un puerto con `-p 8080:80` lo abre en todas las interfaces del host. Docker lo resuelve con una redirección en la tabla nat: el paquete se manda a la IP interna del contenedor antes de que el kernel decida si es para el propio equipo. Como ya no es para el host, no pasa por la cadena input, donde viven las reglas de ufw, sino por forward. Resultado: `ufw status` dice cerrado y el puerto responde desde afuera.

El arreglo preferido es publicar en 127.0.0.1: `-p 127.0.0.1:8081:80` deja el servicio solo para el propio host, y `ss -tlnp` lo confirma. Lo que tenga que ser público va detrás de un proxy inverso en 80 y 443, o se filtra en la cadena DOCKER-USER, que Docker deja para eso. Lo que no conviene es apagar la integración con `"iptables": false`: según la documentación de Docker, rompe la red de los contenedores y deja sus puertos accesibles desde la red local.

La verificación se hace desde otra máquina, con nmap o nc: cualquier chequeo en el propio servidor mira el camino equivocado.
""",
  [{"file": "12-t1.svg", "after": "sino por forward. Resultado",
    "alt": "Animación en cuatro tiempos. A la izquierda, la red; en el medio, la tabla nat; arriba, la cadena input con las reglas de ufw en deny y el host; abajo, la cadena forward con las reglas de Docker y el contenedor nginx con IP 172.17.0.2. 1: un paquete llega desde la otra VM al puerto 8080 del servidor. 2: en la tabla nat, Docker lo redirige con DNAT al puerto 80 del contenedor. 3: como ya no es para el host, el paquete va por forward y llega al contenedor; la cadena input, donde están las reglas de ufw, se apaga con la etiqueta ufw no lo ve, y el puerto responde abierto. 4: con -p 127.0.0.1:8081:80 el servicio escucha solo en el host y un paquete de la red al 8081 no tiene nada que alcanzar.",
    "caption": "La redirección de Docker manda el paquete por forward: las reglas de ufw no lo ven."}],
  S("Auditoría de puertos de Docker",
    "Solo lee: lista los contenedores, marca los puertos publicados en todas las interfaces (los que ufw no filtra) y los que quedan en 127.0.0.1, y muestra ufw y los volúmenes.",
    [("IP_SERVIDOR", "192.168.88.50", "IP del servidor, para el nmap desde otra máquina")],
    r'''
# IES Training - Linux - Auditoria de puertos de Docker
# Solo lee: no crea, borra ni reinicia contenedores. Correlo como root (sudo -i).
ies_docker_puertos() {
  local ip="{{IP_SERVIDOR}}"
  if [ "$(id -u)" -ne 0 ]; then echo "Correlo como root: sudo -i"; return 1; fi
  docker version >/dev/null 2>&1 || { echo "Docker no esta instalado o no esta corriendo"; return 1; }
  echo "== Contenedores (columna PORTS) =="
  docker ps
  echo "== Publicados en TODAS las interfaces (ufw no los filtra) =="
  if docker ps | grep -E "0\.0\.0\.0:|\[::\]:"; then
    echo "ARRIBA: esos puertos responden a la red aunque ufw diga deny. Publicalos en 127.0.0.1."
  else
    echo "Ninguno"
  fi
  echo "== Publicados solo para el host (127.0.0.1) =="
  docker ps | grep "127\.0\.0\.1:" || echo "Ninguno"
  echo "== Lo que escucha docker-proxy =="
  ss -tlnp | grep docker-proxy || echo "Sin docker-proxy (o userland-proxy apagado): mira la columna PORTS"
  echo "== ufw (no incluye los puertos de Docker) =="
  ufw status 2>/dev/null || echo "ufw no instalado"
  echo "== Volumenes =="
  docker volume ls
  echo "Listo: auditado. Verifica desde OTRA maquina: nmap -Pn -p <puertos> $ip"
}
ies_docker_puertos
''',
    [ROOT, "No cambia nada: para pasar un contenedor a 127.0.0.1 hay que recrearlo con -p 127.0.0.1:PUERTO:PUERTO (o cambiar el ports en su compose).",
     "No toques \"iptables\": false en la configuración de Docker: rompe la red de los contenedores.",
     "La prueba que vale es desde otra máquina: lo que ves en el propio servidor puede engañar."]))

# ------------------------------------------------------------------ salida y chequeos
import re
order = ["1", "2", "4", "5", "10", "3", "6", "7", "8", "9", "11", "12"]
out = "/home/claude/ies-training/ilustraciones/linux/manifest.json"
json.dump({k: M[k] for k in order}, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
s = json.dumps(M, ensure_ascii=False)
print("ok", out, len(M), "lecciones · guiones largos:", "—" in s or "–" in s)
for k in order:
    t = M[k]["teoria_md"]
    w = len(re.findall(r"\w+", t))
    bad = [f["after"] for f in M[k]["teoria_figs"] if t.count(f["after"]) != 1 or not (15 <= len(f["after"]) <= 60)]
    code = M[k]["script_rsc"]["codigo"]
    vars_used = set(re.findall(r"\{\{([A-Z0-9_]+)\}\}", code))
    vars_decl = {v["nombre"] for v in M[k]["script_rsc"]["variables"]}
    nl = code.count("\n") + 1
    nonascii = [ln for ln in code.split("\n") if any(ord(ch) > 127 for ch in ln)]
    print(k, "palabras", w, "conceptos", len(M[k]["concepts"]), "teoria_figs mal:" if bad else "", bad if bad else "",
          "" if "### Un poco de historia" in t and "### Cómo funciona" in t else "SIN SUBTITULOS",
          "| script", nl, "líneas", "" if vars_used == vars_decl else f"VARIABLES {vars_used ^ vars_decl}", "NO ASCII" if nonascii else "")
