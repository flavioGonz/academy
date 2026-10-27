"""Genera /home/claude/ies-training/ilustraciones/linux/estructura.json."""
import json

E = {
 "curso": {
  "objetivo": "Al terminar el curso vas a poder recorrer un servidor Debian o Ubuntu sin romper nada, dar permisos por grupos, cambiar configuraciones con copia y validación, diagnosticar servicios, procesos y red con método, dejar SSH solo con llaves detrás de un firewall que entendés, y resolver disco lleno, backups que se prueban y contenedores Docker sin puertos expuestos.",
  "recorrido": "Arrancás leyendo el sistema: el árbol de archivos, quién puede tocar qué y cómo se cambia una configuración sin quedarte afuera. Después mirás el sistema por dentro: cómo arranca con systemd, cómo se leen sus logs, cómo se reparten memoria y procesos, y cómo se mantiene al día con apt. Con eso, salís a la red: la escalera de diagnóstico, el acceso remoto con llaves y el firewall de host. Cerrás con lo que más se repite en soporte: disco lleno, backups que se prueban restaurando y contenedores Docker publicados sin sorpresas."
 },
 "modulos": [
  {"title": "Moverse sin romper",
   "why": "Antes de administrar, hay que saber leer un equipo desconocido, entender quién puede tocar cada archivo y cambiar una configuración sin quedar afuera. Va de solo mirar a hacer el primer cambio con red de seguridad. Termina con un snippet de SSH validado y recargado.",
   "objetivos": [
    "Al terminar el módulo vas a poder recorrer un equipo con pwd, ls, less, find, grep y tuberías sin modificar nada.",
    "Al terminar el módulo vas a poder dar acceso compartido con grupos y setgid, sin 777.",
    "Al terminar el módulo vas a poder cambiar una configuración en un archivo .d con copia, validación y recarga."
   ],
   "lessons": ["1", "2", "4"]},
  {"title": "El sistema por dentro: servicios, procesos y paquetes",
   "why": "Con el equipo bajo control, toca entender qué corre adentro: cómo arranca con systemd y dónde deja sus logs, cómo se leen memoria, carga y procesos, y cómo se mantiene al día sin reinicios sorpresa. Termina con un servidor que sabés diagnosticar y que se parchea solo.",
   "objetivos": [
    "Al terminar el módulo vas a poder explicar el arranque con systemd y diagnosticar un servicio con systemctl status y journalctl.",
    "Al terminar el módulo vas a poder leer free, la carga y top, y terminar un proceso con la señal correcta.",
    "Al terminar el módulo vas a poder dejar las actualizaciones de seguridad automáticas con un reinicio planificado."
   ],
   "lessons": ["5", "10", "3"]},
  {"title": "Red y acceso remoto",
   "why": "La red es donde más se pierde el tiempo y donde más se arriesga el acceso. Va del diagnóstico en escalera a SSH con llaves y a un firewall de host con deny por defecto, siempre sin cortarte la sesión. Termina con un servidor accesible solo con llave y solo desde la red de gestión.",
   "objetivos": [
    "Al terminar el módulo vas a poder diagnosticar la red en escalera con iproute2 y cambiar una IP con netplan try.",
    "Al terminar el módulo vas a poder dejar SSH solo con llaves ed25519 sin quedarte afuera.",
    "Al terminar el módulo vas a poder armar un firewall de host con ufw o nftables y verificarlo desde otra máquina."
   ],
   "lessons": ["6", "7", "8"]},
  {"title": "Mantenimiento y troubleshooting",
   "why": "Los llamados que más se repiten: disco lleno, un backup que nadie probó y un contenedor que quedó expuesto. Cada lección usa lo de los módulos anteriores: journal, timers, firewall y verificación desde afuera. Termina con un método para cada uno.",
   "objetivos": [
    "Al terminar el módulo vas a poder resolver un disco lleno con df y du y agregar un disco a fstab por UUID.",
    "Al terminar el módulo vas a poder programar un backup con un timer de systemd y probarlo restaurando.",
    "Al terminar el módulo vas a poder publicar contenedores Docker en 127.0.0.1 y comprobar que ufw no quedó salteado."
   ],
   "lessons": ["9", "11", "12"]}
 ],
 "lecciones": {
  "1": {"objetivos": [
         "Al terminar vas a poder ubicarte en el árbol de archivos y distinguir /, /etc, /var y /root.",
         "Al terminar vas a poder buscar archivos con find y texto con grep -rn, sin modificar nada.",
         "Al terminar vas a poder encadenar comandos con la tubería y descartar errores con 2>/dev/null."],
        "sigue": "Ya sabés leer el equipo. La próxima explica quién puede leer y escribir cada archivo, y cómo dar acceso sin 777.",
        "requisitos": []},
  "2": {"objetivos": [
         "Al terminar vas a poder leer y escribir permisos en números (755, 644, 600, 2770).",
         "Al terminar vas a poder dar acceso compartido con un grupo y usermod -aG.",
         "Al terminar vas a poder armar una carpeta compartida con setgid y aplicar permisos recursivos por tipo."],
        "conecta": "En Moverse sin miedo leíste los permisos que muestra ls -la. Acá aprendés a cambiarlos.",
        "sigue": "Con los permisos claros, la próxima hace el primer cambio de configuración de verdad: con copia, archivo .d y validación.",
        "requisitos": ["1"]},
  "4": {"objetivos": [
         "Al terminar vas a poder guardar una copia protegida antes de editar un archivo de configuración.",
         "Al terminar vas a poder poner tu cambio en un archivo propio del directorio .d y saber cuál valor gana en SSH.",
         "Al terminar vas a poder validar con sshd -t (y sus equivalentes) antes de recargar un servicio."],
        "conecta": "En Nunca 777 viste quién puede escribir en /etc. Acá escribís ahí, con copia y validación.",
        "sigue": "Tu primer cambio quedó validado. El próximo módulo mira cómo arranca el sistema y qué hacer cuando un servicio no levanta.",
        "requisitos": ["2"]},
  "5": {"objetivos": [
         "Al terminar vas a poder describir el arranque, del firmware a systemd y sus targets.",
         "Al terminar vas a poder diagnosticar un servicio caído con systemctl status y journalctl -u.",
         "Al terminar vas a poder distinguir start de enable y leer el arranque anterior con journalctl -b -1."],
        "conecta": "En Copiá y validá recargaste SSH después de validar. Acá ves qué pasa cuando un servicio no levanta y dónde está el error.",
        "sigue": "Con el servicio arriba, la próxima mira cuánta memoria y CPU usa cada proceso, y cómo terminar uno sin romper nada.",
        "requisitos": ["4"]},
  "10": {"objetivos": [
          "Al terminar vas a poder leer free -h por la columna available y no por free.",
          "Al terminar vas a poder comparar la carga con nproc y encontrar con top quién consume.",
          "Al terminar vas a poder terminar un proceso con SIGTERM y dejar kill -9 como último recurso."],
         "conecta": "En Status y journal systemd arrancaba los servicios. Acá ves esos procesos corriendo y cómo se terminan.",
         "sigue": "Ya sabés qué corre y cuánto consume. La próxima mantiene todo eso actualizado sin reinicios sorpresa.",
         "requisitos": ["5"]},
  "3": {"objetivos": [
         "Al terminar vas a poder distinguir apt update, upgrade y full-upgrade, y leer history.log.",
         "Al terminar vas a poder activar unattended-upgrades y verificar 20auto-upgrades.",
         "Al terminar vas a poder fijar el reinicio automático a una hora o dejarlo para una ventana acordada."],
        "conecta": "En Copiá y validá aprendiste a cambiar configuración en un archivo .d. Acá el reinicio automático va en un archivo propio de apt.conf.d, y lo corren timers de systemd como los de Status y journal.",
        "sigue": "El servidor quedó al día. El próximo módulo sale a la red, empezando por diagnosticarla en escalera.",
        "requisitos": ["4", "5"]},
  "6": {"objetivos": [
         "Al terminar vas a poder diagnosticar la red en escalera: interfaz, gateway, IP pública, DNS y puerto.",
         "Al terminar vas a poder usar ip y ss en lugar de ifconfig, route y netstat.",
         "Al terminar vas a poder fijar una IP con netplan y aplicarla con netplan try."],
        "conecta": "En Moverse sin miedo usaste grep y tuberías; acá los usás para leer la salida de ip, ss y dig.",
        "sigue": "Con la red andando, la próxima asegura el acceso remoto: SSH con llaves y sin contraseña.",
        "requisitos": ["1"]},
  "7": {"objetivos": [
         "Al terminar vas a poder generar una llave ed25519 y copiarla con ssh-copy-id.",
         "Al terminar vas a poder apagar la contraseña y el login de root en un archivo de sshd_config.d.",
         "Al terminar vas a poder probar el cambio desde otra terminal sin cerrar la sesión que funciona."],
        "conecta": "En Copiá y validá armaste un snippet de SSH con sshd -t. Acá ese mismo método apaga la contraseña.",
        "sigue": "SSH ya es solo con llave. La próxima cierra todo lo demás con un firewall de host, empezando por permitir SSH.",
        "requisitos": ["4", "6"]},
  "8": {"objetivos": [
         "Al terminar vas a poder leer con ss -tlnp qué escucha y en qué dirección.",
         "Al terminar vas a poder dejar entrante en deny con SSH permitido solo desde la red de gestión, con ufw o nftables.",
         "Al terminar vas a poder verificar el firewall desde otra máquina y distinguir open, closed y filtered."],
        "conecta": "En Llave, no contraseña aseguraste SSH. Acá decidís desde dónde se puede llegar a SSH y a todo lo demás.",
        "sigue": "El servidor quedó accesible y protegido. El último módulo resuelve los llamados de siempre, empezando por el disco lleno.",
        "requisitos": ["7", "5"]},
  "9": {"objetivos": [
         "Al terminar vas a poder encontrar qué sistema de archivos se llenó con df y qué carpeta lo llenó con du.",
         "Al terminar vas a poder liberar la caché de apt y ponerle tope al journal.",
         "Al terminar vas a poder agregar un disco a fstab por UUID con nofail y validarlo con findmnt -x."],
        "conecta": "En Status y journal viste cuánto ocupa el journal; en Actualizar con método, la caché de apt. Acá esos son los primeros sospechosos.",
        "sigue": "Con espacio en disco, la próxima lo usa bien: un backup programado que se prueba restaurando.",
        "requisitos": ["5", "3"]},
  "11": {"objetivos": [
          "Al terminar vas a poder armar un backup de /etc con tar y rotación, y llevar datos a otro equipo con rsync.",
          "Al terminar vas a poder programarlo con un timer de systemd con Persistent=true.",
          "Al terminar vas a poder probar el backup restaurando un archivo a /tmp y comparándolo con diff."],
         "conecta": "En Status y journal usaste systemctl y journalctl con servicios. Acá escribís tu propio servicio y su timer.",
         "sigue": "La última lección suma contenedores Docker, y vuelve sobre el firewall para que no queden puertos expuestos.",
         "requisitos": ["5", "9"]},
  "12": {"objetivos": [
          "Al terminar vas a poder explicar imagen, contenedor, volumen y red de Docker.",
          "Al terminar vas a poder mostrar por qué un puerto publicado se saltea ufw y verificarlo con nmap.",
          "Al terminar vas a poder publicar un contenedor en 127.0.0.1 y guardar sus datos en un volumen."],
         "conecta": "En Deny por defecto dejaste ufw en deny y verificaste desde otra máquina. Acá ves por qué Docker pasa por al lado.",
         "cierre": "Terminaste el recorrido: sabés leer, cambiar, diagnosticar y proteger un servidor Linux de obra. Para repasar, los scripts de cada lección dejan armado lo aprendido en una VM de laboratorio.",
         "requisitos": ["8"]}
 },
 "avisos": [
  {"id": "12", "texto": "ufw activo en deny (lección 8)", "sugerencia": "ufw activo en deny (lección Deny por defecto)"},
  {"id": "8", "texto": "La lección doce vuelve sobre esto con Docker", "sugerencia": "La última lección del curso vuelve sobre esto con Docker"}
 ]
}

out = "/home/claude/ies-training/ilustraciones/linux/estructura.json"
json.dump(E, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
ids = [l for m in E["modulos"] for l in m["lessons"]]
print("ok", out, "módulos", len(E["modulos"]), "lecciones", len(ids), sorted(ids, key=int) == [str(i) for i in range(1, 13)])
pos = {l: i for i, l in enumerate(ids)}
for l, x in E["lecciones"].items():
    for r in x.get("requisitos", []):
        if pos[r] >= pos[l]:
            print("REQUISITO DESPUÉS", l, r)
s = json.dumps(E, ensure_ascii=False)
print("guiones largos:", "—" in s or "–" in s)
