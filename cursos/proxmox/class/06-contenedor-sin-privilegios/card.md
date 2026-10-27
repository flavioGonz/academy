# Lección 6. Contenedor sin privilegios

**Escuchá:** contenedor-sin-privilegios.mp3 (2 min)

**La idea, en tres líneas**
- Un contenedor LXC comparte el kernel del host: arranca rápido y gasta poco, pero aísla menos que una VM.
- **No privilegiado** (el default): el root de adentro es un usuario sin poder afuera. **Privilegiado**: solo en entornos de confianza.
- **Docker** va en una VM; Docker directo en el host no se recomienda, y las imágenes OCI en LXC son tecnología en preview.

**Impacto:** servicios Linux livianos con menos RAM, sin abrir un agujero en el host.

**Quién lo dice:** 3 de 5 fuentes recomiendan Docker en VM (guía oficial, WunderTech, hhf); el foro oficial muestra que muchos lo corren en LXC para ahorrar recursos, a costa de aislamiento.

**Laboratorio** · Rápido · 10 min
1. Actualizá la lista de plantillas y buscá la de Debian:
```bash
pveam update
pveam available --section system | grep debian
```
2. Bajala al almacenamiento `local` (copiá el nombre exacto que mostró el paso anterior):
```bash
pveam download local <nombre-de-la-plantilla>
```
3. Creá un contenedor no privilegiado (la contraseña es de ejemplo, cambiala):
```bash
pct create 300 local:vztmpl/<nombre-de-la-plantilla> --hostname ct-prueba --unprivileged 1 --memory 512 --rootfs local-lvm:8 --net0 name=eth0,bridge=vmbr0,ip=dhcp --password 'Ejemplo.Cambiar.2026'
pct start 300
```
4. Entrá y mirá el mapeo de usuarios:
```bash
pct enter 300
cat /proc/self/uid_map
exit
```
Vas a ver algo como `0 100000 65536`: el root (0) de adentro es el usuario 100000 del host.
5. Confirmá en el host: `pct config 300 | grep unprivileged`.

**Regla para quedarse**
Servicios Linux livianos en LXC no privilegiado; Docker y todo lo expuesto, en VM.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Guía oficial, contenedores privilegiados y no privilegiados: https://pve.proxmox.com/pve-docs/pve-admin-guide.html
- Docker en VM, con la explicación de por qué: https://www.wundertech.net/how-to-run-docker-in-proxmox-on-a-vm/
- Hilo del foro con pros y contras de LXC contra VM: https://forum.proxmox.com/threads/proxmox-7-1-and-docker-lxc-vs-vm.105140/
