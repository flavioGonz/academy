# Lección 7. VLAN no aísla

**Escuchá:** vlan-no-aisla.mp3 (2 min)

**La idea, en tres líneas**
- Las VLAN separan broadcast, pero si el gateway rutea entre ellas, se ven: para aislar hacen falta ACL (gateway, switch o EAP) o firewall.
- Las ACL se evalúan de arriba hacia abajo: el permit más específico va arriba del deny general.
- La ACL de switch funciona como lista negra: "solo interno" se arma con un permit a las subredes internas y después un deny a todo.

**Impacto:** CCTV, control de acceso e invitados quedan realmente aislados de la oficina, y se puede demostrar con una prueba.

**Quién lo dice:** 3 de 3 fuentes sobre segmentación coinciden; un practicante en el foro de Lawrence Systems desconfía de la seguridad de TP-Link para clientes de empresa y relata una IP de gestión alcanzable desde cualquier VLAN.

**Laboratorio** · Foco · 15 min
Red principal 192.168.88.0/24 (VLAN 1), invitados 10.10.30.0/24 (VLAN 30):
1. **Network Config > Network Settings > LAN > Add**: red `Invitados`, VLAN 30, 10.10.30.1/24 con DHCP.
2. **Site Settings > Profile > Groups > Create New Group**, tipo IP Group, nombre `Redes-Internas`:
```text
192.168.88.0/24
10.10.20.0/24
```
3. **Network Security > ACL > Gateway ACL > Create New Rule**:
```text
Name: Invitados-sin-interna
Policy: Deny
Protocols: All
Source: red Invitados
Destination: IP Group Redes-Internas
```
4. Asociá un SSID `Invitados-Lab` a la VLAN 30, conectá una notebook y probá:
```powershell
ping 10.10.30.1        # puede responder: es su gateway
ping 192.168.88.1      # no tiene que responder
ping 1.1.1.1           # tiene que responder
```
5. Si el ping a 192.168.88.1 responde, revisá el orden de las reglas: la de deny tiene que quedar arriba de cualquier permit general.
⚠️ Una ACL mal ordenada en producción puede cortar el acceso de las cámaras o del propio controlador: probá primero en laboratorio y aplicá en horario de baja actividad.

**Regla para quedarse**
VLAN separa, ACL aísla, y el permit más específico va arriba.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- ACL recomendadas en switches Omada para casos comunes: https://www.omadanetworks.com/eg/support/faq/4122/
- Por qué dos VLAN pueden comunicarse igual (guía de VLAN): https://www.tp-link.com/us/support/faq/4084
- Una voz escéptica sobre la seguridad de TP-Link: https://forums.lawrencesystems.com/t/tp-link-omada-followup/17893
