# Lección 11. Acceso blindado

**Escuchá:** acceso-blindado.mp3 (2 min)

**La idea, en tres líneas**
- Un usuario por persona en el realm `pve`, con el rol justo: `PVEAuditor` para mirar, `PVEVMUser` para operar VMs. Root solo para el administrador.
- 2FA con TOTP o WebAuthn, más de un factor y **claves de recuperación** guardadas.
- El firewall se habilita con una **sesión SSH abierta** y el **IPSet `management`** cargado con las IPs de administración.

**Impacto:** sabés quién hizo cada cambio y no quedás afuera de tu propio servidor al prender el firewall.

**Quién lo dice:** en firewall 2 de 4 fuentes coinciden (guía oficial y el caso de Diego Carrasco); usuarios y 2FA vienen solo de la guía oficial (evidencia fina).

**Laboratorio** · Admin · 15 min
1. Usuario de solo lectura (contraseña de ejemplo, la pide el comando):
```bash
pveum user add tecnico@pve --comment "Técnico de soporte"
pveum passwd tecnico@pve
pveum acl modify / --user tecnico@pve --role PVEAuditor
pveum user permissions tecnico@pve
```
2. 2FA: entrá como `tecnico@pve`, **Datacenter → Permissions → Two Factor → Add → TOTP**, escaneá con la app. Después **Add → Recovery Keys** y guardalas en el gestor de contraseñas.
3. Firewall, en este orden:
   - Abrí una sesión SSH al nodo y dejala abierta.
   - **Datacenter → Firewall → IPSet → Create** con nombre `management`, y agregá tu IP (por ejemplo 10.10.10.50).
   - **Datacenter → Firewall → Options → Firewall: Yes**.
4. Desde la sesión SSH, revisá que compile sin errores:
```bash
pve-firewall status
```
5. Probá entrar a la web desde una IP que no esté en `management`. Si quedaste afuera, desde la sesión SSH: `pve-firewall stop`.

⚠️ En un servidor remoto sin consola fuera de banda, un firewall mal configurado te deja sin acceso. Sesión SSH abierta y IPSet `management` antes de habilitarlo. Siempre.

**Regla para quedarse**
Nunca habilito el firewall sin una sesión SSH abierta y el IPSet management cargado.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Guía oficial: usuarios, roles, 2FA y firewall: https://pve.proxmox.com/pve-docs/pve-admin-guide.html
- Cómo volvió a entrar después de bloquearse con el firewall: https://diegocarrasco.com/regain-access-proxmox-firewall-misconfiguration/
