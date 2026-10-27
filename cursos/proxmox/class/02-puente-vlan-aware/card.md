# Lección 2. Puente VLAN-aware

**Escuchá:** puente-vlan-aware.mp3 (2 min)

**La idea, en tres líneas**
- La red de Proxmox se arma en capas: placas físicas, bond (si hay dos o más), y encima el bridge `vmbr0`, que es el switch virtual.
- Con el bridge marcado como **VLAN aware**, cada placa virtual lleva su tag; no hace falta un bridge por VLAN.
- Los cambios de la GUI quedan en `/etc/network/interfaces.new` hasta que tocás **Apply Configuration** (o `ifreload -a` si editaste a mano).

**Impacto:** menos tickets de "la VM no tiene red" y un solo bridge para todas las VLAN del cliente.

**Quién lo dice:** 3 de 4 fuentes de red coinciden en bond, bridge y VLAN-aware; opensourceisfun prefiere Open vSwitch para aislar clientes entre sí.

**Laboratorio** · Foco · 15 min
1. En la web: **Node → System → Network**, editá `vmbr0`, tildá **VLAN aware** y tocá **Apply Configuration**.
2. Revisá cómo quedó el archivo:
```bash
cat /etc/network/interfaces
```
Tiene que verse parecido a esto (rango de documentación):
```text
auto vmbr0
iface vmbr0 inet static
    address 10.10.10.2/24
    gateway 10.10.10.1
    bridge-ports eno1
    bridge-stp off
    bridge-fd 0
    bridge-vlan-aware yes
    bridge-vids 2-4094
```
3. Creá o editá una VM de prueba: **Hardware → Network Device → VLAN Tag: 10**.
4. Arrancá la VM y en el host mirá el tag en su puerto (`tap<VMID>i0`):
```bash
bridge vlan show
```
5. En el switch, el puerto del host va en trunk con la VLAN 10 permitida.

⚠️ Mover la IP de gestión a una VLAN tagueada desde una conexión remota te corta el acceso al aplicar. Hacelo con consola local o IPMI a mano.

**Regla para quedarse**
Placas, bond, bridge; VLAN aware en el bridge y el tag en la placa de la VM.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Guía oficial, capítulo de red (VLAN y bonds): https://pve.proxmox.com/pve-docs/pve-admin-guide.html
- Bond LACP con bridge y VLAN, paso a paso con switch Cisco: https://getlabsdone.com/steps-to-create-proxmox-bridge-with-multiple-ports-using-lacp-bonding/
- La alternativa con Open vSwitch: https://opensourceisfun.substack.com/p/proxmox-setup-part-2-network
