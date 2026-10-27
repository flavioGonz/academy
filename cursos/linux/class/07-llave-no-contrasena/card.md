# Lección 7. Llave, no contraseña

**Escuchá:** llave-no-contrasena.mp3 (2 min)

**La idea, en tres líneas**
- Llave ed25519: la privada no sale de tu equipo, la frase de paso no viaja, y no hay contraseña que adivinar por fuerza bruta.
- Orden seguro: `ssh-copy-id`, entrar con la llave, y recién ahí `PasswordAuthentication no` y `PermitRootLogin no` en un archivo de `sshd_config.d`.
- fail2ban es opcional con solo llaves; OpenSSH ya trae PerSourcePenalties y el firewall puede limitar por origen.

**Impacto:** el acceso remoto a servidores, gateways y LXC deja de depender de contraseñas que se comparten, se anotan o se adivinan.

**Quién lo dice:** 4 de 7 fuentes sobre SSH coinciden en llaves ed25519 (documentación de Ubuntu Server, Arch Wiki, linuxblog.io, computingforgeeks). Sobre fail2ban hay discrepancia: en el hilo de Akamai uno lo ve como ruido con solo llaves y otro lo defiende porque sirve para cualquier log.

**Laboratorio** · Foco · 20 min
Desde tu notebook hacia una VM de prueba (ejemplo 192.168.88.50, usuario tecnico):
1. Generá la llave con comentario que la identifique:
```bash
ssh-keygen -t ed25519 -C "tecnico@notebook-2026"
```
2. Copiala y entrá con ella:
```bash
ssh-copy-id tecnico@192.168.88.50
ssh tecnico@192.168.88.50       # no tendría que pedir la contraseña del servidor
```
3. En el servidor, con esta sesión abierta, un archivo propio:
```text
# /etc/ssh/sshd_config.d/10-ies-acceso.conf
PasswordAuthentication no
KbdInteractiveAuthentication no
PermitRootLogin no
```
```bash
sudo sshd -t && sudo systemctl reload ssh
sudo sshd -T | grep -Ei "passwordauth|permitroot"
```
4. Desde OTRA terminal, probá que la contraseña ya no entra:
```bash
ssh -o PubkeyAuthentication=no tecnico@192.168.88.50    # Permission denied
```
5. Permisos que SSH exige:
```bash
chmod 700 ~/.ssh && chmod 600 ~/.ssh/authorized_keys
```
⚠️ Nunca cierres la sesión que funciona hasta confirmar que una nueva entra con la llave. Si quedaste afuera, la salida es la consola de la VM o del hipervisor.

Nota de versión: Ubuntu 26.04 trae OpenSSH 10.2 (intercambio de claves post cuántico por defecto, DSA eliminado, PerSourcePenalties activo); `sshd.service` es alias de `ssh.service`.

**Regla para quedarse**
Primero entro con la llave, después apago la contraseña, y nunca cierro la sesión que funciona hasta probar una nueva.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- OpenSSH en Ubuntu Server: llaves, snippets y logs: https://documentation.ubuntu.com/server/how-to/security/openssh-server/
- Llaves SSH, tipos y cómo copiarlas: https://wiki.archlinux.org/title/SSH_keys
- La discusión sobre fail2ban con solo llaves: https://www.akamai.com/community/questions/10861/how-important-is-fail2ban
