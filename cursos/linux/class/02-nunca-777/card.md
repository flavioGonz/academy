# Lección 2. Nunca 777

**Escuchá:** nunca-777.mp3 (2 min)

**La idea, en tres líneas**
- Permisos para dueño, grupo y resto (u, g, o) con r=4, w=2, x=1: 755 directorios, 644 archivos, 600 secretos.
- El acceso compartido se da con un grupo (`usermod -aG`) y no con 777 ni trabajando como root.
- En un directorio, setgid (el 2 de 2770) hace que lo nuevo herede el grupo de la carpeta.

**Impacto:** el software (NVR, gestor de accesos, scripts) escribe donde corresponde sin dejar carpetas abiertas a cualquier usuario del equipo.

**Quién lo dice:** 3 de 5 fuentes coinciden (Debian Handbook, Debian Reference, linuxblog.io); ninguna discrepa. La Debian Reference agrega que dar sudo sin contraseña (NOPASSWD) solo tiene sentido en una estación de un único usuario.

**Laboratorio** · Foco · 15 min
En una VM de prueba con Debian 13 o Ubuntu 24.04/26.04:
1. Creá el grupo y dos usuarios de prueba:
```bash
sudo groupadd tecnicos
sudo adduser tec1
sudo adduser tec2
sudo usermod -aG tecnicos tec1
sudo usermod -aG tecnicos tec2
id tec1
```
2. Carpeta compartida con setgid:
```bash
sudo mkdir -p /srv/obra
sudo chown root:tecnicos /srv/obra
sudo chmod 2770 /srv/obra
ls -ld /srv/obra        # drwxrws y el grupo tecnicos
```
3. Probá con cada usuario y mirá el grupo del archivo creado:
```bash
sudo -u tec1 touch /srv/obra/plano.txt
ls -l /srv/obra         # el grupo es tecnicos aunque lo creó tec1
sudo -u nobody ls /srv/obra   # Permission denied: el resto no entra
```
4. Permisos recursivos sin volver ejecutable todo:
```bash
sudo find /srv/obra -type d -exec chmod 2770 {} \;
sudo find /srv/obra -type f -exec chmod 660 {} \;
```
Nota de versión: en Ubuntu 26.04 `sudo` es sudo-rs; `sudo -E` se ignora con un aviso. Para pasar una variable se usa la opción preserve-env con el nombre de la variable.

**Regla para quedarse**
Si pienso en 777, lo que falta es arreglar dueño y grupo.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Permisos, setgid, sticky bit y ACL en el Debian Handbook: https://debian-handbook.info/browse/stable/sect.rights-management.html
- chmod, chown y umask con casos reales (web, llaves SSH, carpetas compartidas): https://linuxblog.io/linux-file-permissions-explained-chmod-chown-and-umask-in-practice/
- Cambios de sudo-rs en Ubuntu 26.04: https://computingforgeeks.com/ubuntu-2604-lts-features/
