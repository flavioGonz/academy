"""Genera /home/claude/ies-training/ilustraciones/hikcentral/estructura.json.

Orden nuevo: 1 2 3 4 | 5 6 7 | 11 8 | 9 10 12.
Roles y cuentas (11) pasa antes de Alarmas con criterio (8): la regla 2 de alarmas manda la alarma al
"usuario guardia", que se crea en Roles y cuentas, y el rol Guardia usa el área Depósito de Áreas primero.
"""
import json

E = {
 "curso": {
  "objetivo": "Al terminar el curso vas a poder dimensionar, instalar, licenciar y respaldar un servidor HikCentral Professional, dar de alta equipos por IP, ISUP o Hik-Connect y ordenarlos en áreas, decidir dónde graba cada cámara, armar usuarios con roles mínimos y alarmas que alguien atiende, configurar niveles de acceso y asistencia, y diagnosticar equipos offline con un método y la Communication Matrix.",
  "recorrido": "Arrancás por el servidor: qué capa hace qué, cómo se dimensiona e instala, cómo se licencia y qué hacer antes de tocarlo. Con la plataforma en pie, das de alta los equipos, los ordenás en áreas y decidís dónde graba cada cámara. Después definís quién opera y qué le avisa el sistema: roles a medida y alarmas con criterio, que llegan al usuario que acabás de crear. Cerrás con las puertas y el reloj, niveles de acceso y asistencia, y con el diagnóstico de abajo arriba que usa todo lo anterior."
 },
 "modulos": [
  {"title": "El servidor bien parado",
   "why": "Antes de agregar una sola cámara, la plataforma tiene que estar dimensionada, instalada, licenciada y con un plan para cuando haya que tocar el servidor. Va del mapa de capas a la instalación, de la instalación a la licencia y de la licencia al procedimiento de cambio. Termina con un servidor de laboratorio activado y respaldado.",
   "objetivos": [
    "Al terminar el módulo vas a poder ubicar una falla en su capa: equipo, SYS, streaming o cliente.",
    "Al terminar el módulo vas a poder dimensionar e instalar el SYS con la guía oficial y resolver un puerto en rojo en Service Manager.",
    "Al terminar el módulo vas a poder activar la licencia online u offline y cambiar el hardware del servidor sin perder licencia ni configuración."
   ],
   "lessons": ["1", "2", "3", "4"]},
  {"title": "Equipos, áreas y grabación",
   "why": "Es lo que se hace en cada obra: dar de alta los equipos con el método que corresponde, ubicarlos en un árbol de áreas y decidir, cámara por cámara, dónde queda el video. El orden importa: sin alta no hay canales, y sin área los canales no tienen vivo ni grabación útil. Termina con un sitio de laboratorio ordenado y grabando.",
   "objetivos": [
    "Al terminar el módulo vas a poder elegir entre alta por IP, ISUP o Hik-Connect y registrar una cámara por ISUP sin abrir puertos en el sitio.",
    "Al terminar el módulo vas a poder diseñar el árbol de áreas, importar los canales y armar vistas y mapas.",
    "Al terminar el módulo vas a poder decidir por cámara si graba en el sitio o en el centro, respetando los límites de cada opción."
   ],
   "lessons": ["5", "6", "7"]},
  {"title": "Quién opera y qué le avisa",
   "why": "Con las cámaras en sus áreas, se define quién las mira y qué le salta en pantalla. Primero los roles, porque se apoyan en las áreas y crean al usuario guardia; después las alarmas, que tienen a ese guardia como destinatario. Termina con un operador que ve solo lo suyo y recibe solo lo que tiene que atender.",
   "objetivos": [
    "Al terminar el módulo vas a poder crear roles a medida con vigencia, horario y áreas visibles, y endurecer contraseñas y HTTPS.",
    "Al terminar el módulo vas a poder separar eventos de alarmas y bajar el ruido con Ignore Repetitive Events y Delay Alarm.",
    "Al terminar el módulo vas a poder configurar una alarma con grabación pre y post evento, bloqueo del clip y destinatario."
   ],
   "lessons": ["11", "8"]},
  {"title": "Puertas, asistencia y diagnóstico",
   "why": "Acceso y asistencia concentran las llamadas de soporte, y las dos dependen de aplicar a los equipos y de la hora. El curso cierra con el diagnóstico de abajo arriba, que usa todo lo anterior: capas, puertos de alta, streaming y controladoras. Termina con una puerta que abre en horario, una marca que aparece en el reporte y un método para el próximo offline.",
   "objetivos": [
    "Al terminar el módulo vas a poder armar persona, nivel de acceso y asignación, y aplicarlos sin dejar puertas offline en horario.",
    "Al terminar el módulo vas a poder configurar asistencia con puntos de marca, regla general y turnos, con SYS y controladoras en la misma hora.",
    "Al terminar el módulo vas a poder diagnosticar un equipo offline de abajo arriba y validar cada puerto contra la Communication Matrix."
   ],
   "lessons": ["9", "10", "12"]}
 ],
 "lecciones": {
  "1": {
   "objetivos": [
    "Al terminar vas a poder explicar qué hacen el SYS, el Streaming Gateway, el Streaming Server y cada cliente.",
    "Al terminar vas a poder leer Service Manager y anotar servicio, estado y puerto sin tocar nada.",
    "Al terminar vas a poder reconocer un VSM217 por la versión del Control Client."
   ],
   "sigue": "Con el mapa en la cabeza, la próxima dimensiona e instala el SYS en un servidor de laboratorio.",
   "requisitos": []
  },
  "2": {
   "objetivos": [
    "Al terminar vas a poder elegir el perfil de hardware del SYS con la guía de requisitos.",
    "Al terminar vas a poder verificar el MD5 del instalador e instalar en modo típico como administrador.",
    "Al terminar vas a poder encontrar con netstat y tasklist quién ocupa un puerto en rojo y resolverlo."
   ],
   "conecta": "En Mapa de capas abriste Service Manager solo para mirar. Acá instalás el SYS y lo usás para resolver un conflicto de puertos.",
   "sigue": "El servidor quedó instalado con una licencia temporal. La próxima lo activa, online u offline.",
   "requisitos": ["1"]
  },
  "3": {
   "objetivos": [
    "Al terminar vas a poder activar primero la licencia base y después las expansiones.",
    "Al terminar vas a poder hacer una activación offline con pedido y respuesta dentro de las 24 horas.",
    "Al terminar vas a poder interpretar los errores 1103, 1105, 1108, 1113, 1114 y 1116."
   ],
   "conecta": "En Servidor a medida dejaste el SYS instalado. Acá se activa, con la hora del servidor en hora.",
   "sigue": "Con la licencia atada al servidor, la próxima arma el procedimiento para tocarlo sin perderla.",
   "requisitos": ["2"]
  },
  "4": {
   "objetivos": [
    "Al terminar vas a poder programar el backup del sistema y copiarlo fuera del SYS.",
    "Al terminar vas a poder explicar por qué un cambio de hardware o una migración de VM rompe la licencia.",
    "Al terminar vas a poder seguir un checklist de cambio: backup, copia, desactivar, cambiar y reactivar."
   ],
   "conecta": "En Licencia sin sorpresas viste que la licencia queda atada a la instalación. Acá se planifica cómo liberarla antes de tocar el servidor.",
   "sigue": "El servidor quedó bien parado. El próximo módulo empieza a cargarle equipos.",
   "requisitos": ["3"]
  },
  "5": {
   "objetivos": [
    "Al terminar vas a poder elegir entre alta por IP, ISUP o Hik-Connect según la conexión del sitio.",
    "Al terminar vas a poder registrar una cámara por ISUP con Device ID y clave en los dos lados.",
    "Al terminar vas a poder probar el puerto 7660 con Test-NetConnection y separar red de configuración."
   ],
   "conecta": "En el módulo anterior dejaste el SYS activado y respaldado. Acá recibe sus primeros equipos.",
   "sigue": "Los equipos quedaron online. La próxima los ubica en un árbol de áreas, sin el cual no hay vivo ni reproducción.",
   "requisitos": ["4"]
  },
  "6": {
   "objetivos": [
    "Al terminar vas a poder diseñar el árbol de áreas antes del alta e importar los canales a cada área.",
    "Al terminar vas a poder explicar por qué las cámaras de un área hija no aparecen en la madre.",
    "Al terminar vas a poder armar una vista pública y elegir entre E-map y GIS."
   ],
   "conecta": "En Tres formas de alta activaste Add Resource to Area. Acá se ve por qué: sin área, la cámara existe pero nadie la puede usar.",
   "sigue": "Las cámaras ya están donde el operador las busca. La próxima decide dónde queda su video.",
   "requisitos": ["5"]
  },
  "7": {
   "objetivos": [
    "Al terminar vas a poder armar la tabla de grabación por cámara con su motivo.",
    "Al terminar vas a poder chequear cada fila contra los límites de pStor, Hybrid SAN y Cloud Storage.",
    "Al terminar vas a poder tomar el calendario del NVR y buscar las cámaras que no graban."
   ],
   "conecta": "En Tres formas de alta elegiste cómo entra cada equipo; acá ves que esa elección limita dónde puede grabar.",
   "sigue": "El sitio quedó ordenado y grabando. El próximo módulo define quién lo opera, empezando por los roles.",
   "requisitos": ["5", "6"]
  },
  "11": {
   "objetivos": [
    "Al terminar vas a poder crear un rol a medida con vigencia, horario de permisos y áreas visibles.",
    "Al terminar vas a poder crear un usuario por persona y subir la fuerza mínima de contraseña a Strong.",
    "Al terminar vas a poder armar el .pem del certificado HTTPS y saber dónde se sube."
   ],
   "conecta": "En Áreas primero armaste el árbol con Depósito y sus naves. Acá ese árbol decide qué ve cada usuario.",
   "sigue": "Ya existe el usuario guardia. La próxima le arma alarmas que valga la pena atender.",
   "requisitos": ["6"]
  },
  "8": {
   "objetivos": [
    "Al terminar vas a poder distinguir un evento de una alarma y decidir cuál corresponde.",
    "Al terminar vas a poder bajar el ruido con Ignore Repetitive Events y Delay Alarm.",
    "Al terminar vas a poder configurar grabación pre y post evento con bloqueo y un destinatario."
   ],
   "conecta": "En Roles y cuentas creaste al usuario guardia: acá es el destinatario de la alarma. Y la cámara necesita el calendario de grabación de Dónde graba.",
   "sigue": "El video quedó resuelto. El último módulo pasa a las puertas, empezando por los niveles de acceso.",
   "requisitos": ["7", "11"]
  },
  "9": {
   "objetivos": [
    "Al terminar vas a poder dar de alta una persona con credencial y asignarle un nivel de acceso con horario.",
    "Al terminar vas a poder aplicar cambios a los dispositivos sin marcar Apply (Initial).",
    "Al terminar vas a poder probar el nivel con una pasada dentro y otra fuera del horario."
   ],
   "conecta": "En Tres formas de alta diste de alta equipos; acá la controladora es la que recibe los permisos. Y como en Roles y cuentas, los horarios mandan.",
   "sigue": "Las mismas lectoras pueden hacer de reloj. La próxima arma la asistencia, empezando por la hora.",
   "requisitos": ["5"]
  },
  "10": {
   "objetivos": [
    "Al terminar vas a poder dejar SYS y controladoras en la misma zona y con la misma fuente de hora.",
    "Al terminar vas a poder configurar puntos de marca, regla general, plantilla y turno.",
    "Al terminar vas a poder elegir entre turno Normal y Man-Hour y leer los registros del día siguiente."
   ],
   "conecta": "En Niveles de acceso diste de alta a Prueba Lab con su tarjeta y la Puerta Lab. Acá esa misma puerta marca entrada y salida.",
   "sigue": "Queda el ticket de todos los días: el equipo que aparece offline. La última lección arma el método.",
   "requisitos": ["9"]
  },
  "12": {
   "objetivos": [
    "Al terminar vas a poder diagnosticar un equipo offline en orden: físico, IP, DNS, servicio y puertos.",
    "Al terminar vas a poder validar cada puerto contra la Communication Matrix con Test-NetConnection.",
    "Al terminar vas a poder distinguir un tope de conexiones del NVR de un problema de ancho de banda."
   ],
   "conecta": "Usa todo lo anterior: las capas de Mapa de capas, el 7660 de Tres formas de alta y el 559 del Streaming Gateway.",
   "cierre": "Con esto recorriste HikCentral Professional completo: del servidor bien parado a la puerta que abre y el reporte que cierra. La ficha de licencia, el checklist de cambio, la tabla de grabación y la escalera de diagnóstico son tu kit para la próxima obra.",
   "requisitos": ["1", "5"]
  }
 },
 "avisos": [
  {"id": "8,9,10,11", "archivo": "card.md",
   "texto": "Con el orden nuevo cambian los títulos de cuatro tarjetas: \"# Lección 11. Roles y cuentas\", \"# Lección 8. Alarmas con criterio\", \"# Lección 9. Niveles de acceso\" y \"# Lección 10. Asistencia y hora\".",
   "sugerencia": "Pasan a \"# Lección 8. Roles y cuentas\", \"# Lección 9. Alarmas con criterio\", \"# Lección 10. Niveles de acceso\" y \"# Lección 11. Asistencia y hora\". Las lecciones 1 a 7 y la 12 conservan su número. La aplicación de la charla cambia sola \"Lección diez.\" por \"Lección once.\"."},
  {"id": "4", "archivo": "script.txt",
   "texto": "A: Lección cuatro, cierre del primer arco. Antes de tocar.",
   "sugerencia": "A: Lección cuatro, cierre del primer módulo. Antes de tocar."},
  {"id": "5", "archivo": "script.txt",
   "texto": "A: Segundo arco, operación diaria. Lección cinco: tres formas de dar de alta un equipo.",
   "sugerencia": "A: Arranca el segundo módulo: equipos, áreas y grabación. Lección cinco: tres formas de dar de alta un equipo."},
  {"id": "11", "archivo": "script.txt",
   "texto": "A: Lección once. Roles y cuentas.",
   "sugerencia": "A: Arranca el tercer módulo. Lección ocho. Roles y cuentas."},
  {"id": "8", "archivo": "script.txt",
   "texto": "A: Lección ocho, cierre del segundo arco. Alarmas con criterio.",
   "sugerencia": "A: Lección nueve, cierre del tercer módulo. Alarmas con criterio."},
  {"id": "9", "archivo": "script.txt",
   "texto": "A: Tercer arco: acceso, gestión y troubleshooting. Lección nueve, niveles de acceso.",
   "sugerencia": "A: Arranca el último módulo: puertas, asistencia y diagnóstico. Lección diez, niveles de acceso."}
 ]
}
out = "/home/claude/ies-training/ilustraciones/hikcentral/estructura.json"
json.dump(E, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
s = json.dumps(E, ensure_ascii=False)
ids = [i for m in E["modulos"] for i in m["lessons"]]
assert sorted(ids, key=int) == [str(i) for i in range(1, 13)], ids
assert set(E["lecciones"]) == set(ids)
for lid, x in E["lecciones"].items():
    for r in x.get("requisitos", []):
        assert ids.index(r) < ids.index(lid), (lid, r)
print("ok", out, "orden:", ids, "dashes:", "—" in s or "–" in s)
