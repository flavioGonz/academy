# Lección 3. Red del host

**Escuchá:** red-del-host.mp3 (2 min)

**La idea, en tres líneas**
- El vSwitch estándar une uplinks físicos (vmnic) con port groups, donde se conectan VMs y adaptadores del host.
- Cada port group lleva un VLAN ID; 0 es sin etiqueta (VLAN nativa). El puerto del switch físico va en troncal con esas VLAN permitidas.
- Dos uplinks por vSwitch, a bocas distintas, y la red de gestión se toca solo con consola fuera de banda (iLO, iDRAC o pantalla).

**Impacto:** cero hosts inaccesibles por un cambio de VLAN y servidores que siguen grabando aunque se suelte un cable.

**Quién lo dice:** 2 de 2 fuentes de redes estándar coinciden (KB de Broadcom y phoenixNAP); evidencia escasa en cantidad, sin discrepancias.

**Laboratorio** · Foco · 15 min
En un ESXi de laboratorio con al menos dos NICs libres (acá vmnic2 y vmnic3), por SSH:
```bash
# ver lo que hay
esxcfg-vswitch -l
esxcli network nic list

# vSwitch nuevo con dos uplinks
esxcli network vswitch standard add -v vSwitch1
esxcli network vswitch standard uplink add -u vmnic2 -v vSwitch1
esxcli network vswitch standard uplink add -u vmnic3 -v vSwitch1

# port group para la VLAN 20
esxcli network vswitch standard portgroup add -p VM-VLAN20 -v vSwitch1
esxcli network vswitch standard portgroup set -p VM-VLAN20 -v 20

# verificar uplinks activos y VLAN
esxcli network vswitch standard policy failover get -v vSwitch1
esxcfg-vswitch -l
```
Configurá los dos puertos del switch físico en troncal con la VLAN 20 permitida, conectá una VM al port group y probá ping a su gateway. Después desenchufá un cable y repetí.

⚠️ No cambies la VLAN del port group "Management Network" por SSH ni desde el cliente web sin tener abierta la consola remota (iLO, iDRAC) o física.

**Regla para quedarse**
La red de gestión se toca solo con la consola fuera de banda abierta.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Cambiar VLAN en un port group, por UI y por CLI (KB de Broadcom): https://knowledge.broadcom.com/external/article/311057/configuring-vlan-on-a-vswitch-standard.html
- vSwitch, NIC teaming y port groups en una instalación nueva: https://phoenixnap.com/kb/vmware-esxi
