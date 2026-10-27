# Lección 1. Repos en orden

**Escuchá:** repos-en-orden.mp3 (2 min)

**La idea, en tres líneas**
- Proxmox VE 9.2 (mayo 2026, Debian 13) es la rama actual; la 8.4 tuvo parches de seguridad solo hasta agosto de 2026.
- Antes del primer update se elige un repositorio: enterprise (con suscripción, para producción) o no-subscription (gratis, que Proxmox indica para pruebas y uso no productivo).
- Se actualiza con `apt full-upgrade`, nunca con `apt upgrade` a secas.

**Impacto:** se terminan los "401 Unauthorized" del primer update y los hosts con paquetes a medio actualizar.

**Quién lo dice:** 6 de 7 fuentes coinciden en que la rama actual es la 9.x y 3 de 7 tratan el repositorio; techdirectarchive usa no-subscription como rutina, mientras la wiki oficial no lo recomienda para producción.

**Laboratorio** · Rápido · 10 min
1. En la web del nodo: **Node → Updates → Repositories**. Mirá qué repositorios hay y cuáles marcan advertencia.
2. Por consola, revisá versión y archivos de repositorio:
```bash
pveversion -v | head -3
ls /etc/apt/sources.list.d/
cat /etc/apt/sources.list.d/*.sources
```
3. Si no hay suscripción: en **Repositories** seleccioná `pve-enterprise` y tocá **Disable**; después **Add → No-Subscription**. Por consola queda un archivo `/etc/apt/sources.list.d/proxmox.sources` con `Components: pve-no-subscription` y `Suites: trixie`.
4. Si quedan archivos `.list` viejos, migralos y actualizá:
```bash
apt modernize-sources
apt update
apt full-upgrade
```
5. Verificá que `apt update` no muestre errores y que solo quede un repositorio de Proxmox habilitado.

⚠️ En un cliente con suscripción, mantené enterprise. Decidir no-subscription para producción es una decisión del cliente, con backups probados.

**Regla para quedarse**
Un host, un repositorio de Proxmox elegido a conciencia, y siempre `apt full-upgrade`.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Repositorios oficiales de Proxmox VE 9 (formato deb822): https://pve.proxmox.com/wiki/Package_Repositories
- Anuncio de PVE 9.0 y fin de soporte de 8.4: https://lists.proxmox.com/pipermail/pve-user/2025-August/017639.html
- Update menor a 9.2.3 paso a paso: https://techdirectarchive.com/2026/06/13/how-to-update-proxmox-ve-from-to-the-latest-version-9-2-3-today/
