# Lección 1. Moverse sin miedo

**Escuchá:** moverse-sin-miedo.mp3 (2 min)

**La idea, en tres líneas**
- Todo cuelga de un único árbol que arranca en `/`; `/root` es solo la carpeta personal del administrador.
- Con `pwd`, `ls -la`, `cd`, `less`, `find` y `grep` leés cualquier equipo sin modificar nada.
- La tubería `|` encadena comandos: la salida de uno es la entrada del siguiente.

**Impacto:** en un appliance, una VM o un LXC desconocido encontrás la configuración en minutos y sin riesgo de romper nada.

**Quién lo dice:** 2 de 2 fuentes que cubren navegación coinciden (evidencia fina); ninguna discrepa. La Debian Reference propone practicar como usuario sin privilegios.

**Laboratorio** · Rápido · 10 min
En una VM con Debian 13 o Ubuntu 24.04/26.04 (con openssh-server instalado), como usuario común, sin sudo:
1. Ubicate y listá:
```bash
pwd
ls -la /etc | less      # en less: / busca, n repite, q sale
```
2. Encontrá los archivos de configuración del servidor SSH:
```bash
find /etc -name "*sshd*" 2>/dev/null
```
3. Buscá una palabra dentro de los archivos, con número de línea:
```bash
grep -rn "Port" /etc/ssh 2>/dev/null
```
4. Leé el archivo entero sin editarlo:
```bash
less /etc/ssh/sshd_config
```
5. Bonus: listá los procesos de SSH sin que grep se encuentre a sí mismo:
```bash
ps aux | grep "[s]shd"
```

**Regla para quedarse**
En un equipo nuevo, primero leo con less y grep; recién después edito.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Tutorial de comandos básicos y tuberías de la Debian Reference: https://www.debian.org/doc/manuals/debian-reference/ch01.en.html
- find aplicado a auditar permisos (SUID, archivos escribibles por todos): https://linuxblog.io/linux-file-permissions-explained-chmod-chown-and-umask-in-practice/
