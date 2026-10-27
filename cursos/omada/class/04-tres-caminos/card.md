# Lección 4. Tres caminos

**Escuchá:** tres-caminos.mp3 (2 min)

**La idea, en tres líneas**
- En otra subred o sede, alguien le dice al equipo dónde está el controlador: Omada Discovery Utility, Inform URL en su web (System Tools > Controller Settings) o DHCP option 138.
- Option 138 recién actúa cuando el equipo renueva DHCP; para Omada Central se usa la Site URL del dashboard.
- Con NAT, reenviá TCP/UDP 29810 a 29817 con el mismo puerto de origen y destino; en controlador 6 se sumó el TCP 29817.

**Impacto:** sucursales, VLAN de cámaras y controladores en la nube se adoptan sin viajar.

**Quién lo dice:** 6 de 7 fuentes sobre adopción remota coinciden en los tres métodos; no se encontró discrepancia. La guía de Docker agrega que en Docker Desktop (Windows/macOS) el único camino práctico es la Inform URL.

**Laboratorio** · Foco · 15 min
Con un controlador en 192.168.88.0/24 (ej. 192.168.88.10) y un EAP en otra subred (ej. VLAN 20, 10.10.10.0/24):
1. Si el DHCP de la VLAN 20 lo da un gateway Omada: **Network Config > LAN**, editá la red, **Advanced DHCP Options**, **Option 138** = `192.168.88.10`. Guardá.
   Si lo da un MikroTik de laboratorio:
```routeros
/ip dhcp-server option add name=omada138 code=138 value=0xC0A8580A
/ip dhcp-server network set [find address="10.10.10.0/24"] dhcp-option=omada138
```
   La IP del controlador va en hexadecimal, un byte por octeto: 192.168.88.10 queda `0xC0A8580A`.
2. Desconectá y reconectá el EAP para que renueve DHCP.
3. Verificá que haya ruta entre las dos subredes (ping del EAP al controlador o desde **Tools** del controlador).
4. Mirá **Devices**: el EAP tiene que aparecer en **Pending**. Adoptalo.
5. Si hay NAT entre sede y controlador, la regla de port forwarding en la central queda así:
```text
TCP+UDP  29810-29817  ->  192.168.88.10  29810-29817   (mismo puerto origen y destino)
```
⚠️ Exponer los puertos de gestión a internet abre el controlador al mundo; si podés, preferí un túnel VPN entre sedes (Lección 11).

**Regla para quedarse**
Otra subred, otro método: Discovery Utility, Inform URL u option 138, y renovar DHCP.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Adopción entre subredes por internet y por VPN (Controller v6): https://support.omadanetworks.com/de/document/124358/
- Puertos del controlador y ejemplo de dos controladores tras la misma IP: https://support.omadanetworks.com/document/13090/
- Adopción en Omada Central con la Site URL: https://www.omadanetworks.com/ph/support/faq/4580/
