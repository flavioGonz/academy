# Lección 4. Copiá y validá

**Escuchá:** copia-y-valida.mp3 (2 min)

**La idea, en tres líneas**
- Antes de editar, copia del original; tu cambio va en un archivo propio dentro del directorio `.d` del servicio.
- Cada servicio trae su validador: `sshd -t`, `netplan generate`, `findmnt -x`, `visudo -c`, `nginx -t`. Se valida antes de reiniciar.
- En OpenSSH vale el primer valor leído, y `/etc/ssh/sshd_config.d/*.conf` se incluye al principio: tu snippet gana sobre el archivo principal.

**Impacto:** cambiás la configuración de un equipo remoto sin quedarte afuera ni pedir que alguien vaya a la consola.

**Quién lo dice:** 4 de 5 fuentes sobre editar configuración coinciden (documentación de Ubuntu Server, Debian Handbook, linuxconfig, Arch Wiki); ninguna discrepa.

**Laboratorio** · Foco · 15 min
En una VM con openssh-server (Debian 13 o Ubuntu), con la consola de la VM abierta por si acaso:
1. Copia de seguridad protegida contra escritura:
```bash
sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.original
sudo chmod a-w /etc/ssh/sshd_config.original
```
2. Mirá qué snippets ya existen (pueden estar pisando valores):
```bash
ls -l /etc/ssh/sshd_config.d/
```
3. Tu cambio en un archivo propio y validación:
```bash
echo "Banner /etc/issue.net" | sudo tee /etc/ssh/sshd_config.d/10-ies.conf
sudo sshd -t && echo "config OK"
```
4. Error a propósito, para ver cómo lo marca:
```bash
echo "PasswordAuthentication yess" | sudo tee -a /etc/ssh/sshd_config.d/10-ies.conf
sudo sshd -t        # indica archivo y número de línea
sudo sed -i '/yess/d' /etc/ssh/sshd_config.d/10-ies.conf
sudo sshd -t && sudo systemctl reload ssh
```
5. Editores, lo mínimo:
```text
nano:  Ctrl+O guarda · Ctrl+X sale
vim:   i escribe · Esc vuelve · :wq guarda y sale · :q! sale sin guardar
```
⚠️ En un servidor remoto, recargá SSH con otra sesión abierta y probá entrar desde una nueva antes de cerrar la que funciona.

**Regla para quedarse**
Copia, cambio en un archivo `.d`, validación, y recién ahí restart.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Configuración de OpenSSH en Ubuntu, snippets y sshd -t: https://documentation.ubuntu.com/server/how-to/security/openssh-server/
- Directorios .d y por qué no editar archivos de otros paquetes: https://debian-handbook.info/browse/stable/sect.apt-get.html
- Validar netplan antes de aplicar: https://linuxconfig.org/netplan-configuration-guide-on-ubuntu-26-04
