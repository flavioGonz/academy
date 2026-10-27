# Lección 6. VLAN completa

**Escuchá:** vlan-completa.mp3 (2 min)

**La idea, en tres líneas**
- Una VLAN tiene tres patas: interfaz y DHCP en el gateway, uplink tagueado entre gateway y switch, y puerto de acceso con la VLAN como nativa (untagged).
- En el controlador: Network Config > Network Settings > LAN > Add; al crear la red, el controlador crea su perfil de puerto, y los puertos en trunk la llevan tagueada.
- La red por defecto queda como VLAN de gestión de los equipos Omada; con router de terceros, la red se crea con DHCP Server Device en None.

**Impacto:** "la cámara no agarra IP" se resuelve con una lista de tres puntos y no con prueba y error.

**Quién lo dice:** 3 de 4 fuentes sobre VLAN coinciden; un practicante (Evan McCann) señala que mover la VLAN de gestión es más engorroso de lo que debería.

**Laboratorio** · Foco · 15 min
Con un gateway ER y un switch JetStream adoptados en el mismo sitio:
1. **Network Config > Network Settings > LAN > Add**:
```text
Name: CCTV
VLAN: 20
Gateway/Subnet: 10.10.20.1/24
DHCP Server: activado, rango 10.10.20.100 - 10.10.20.200
```
2. Verificá que el puerto del switch que va al gateway esté con el perfil **All** (trunk): lleva la VLAN 20 tagueada.
3. **Devices > (switch) > Ports**: editá el puerto 5 y asignale el perfil `CCTV` (VLAN 20 nativa, untagged).
4. Enchufá una notebook en el puerto 5 y verificá:
```powershell
ipconfig /renew
ipconfig | findstr IPv4
```
   Tiene que mostrar 10.10.20.x.
5. Si no agarra IP, revisá en orden: red y DHCP en el gateway, perfil del uplink, perfil del puerto.
⚠️ No cambies el perfil del puerto por el que el switch habla con el controlador: podés dejarlo sin gestión.

**Regla para quedarse**
VLAN que no da IP: revisar gateway, uplink y puerto, en ese orden.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- VLAN 802.1Q en switches Omada en modo controlador (v6): https://www.tp-link.com/us/support/faq/4084
- VLAN de los puertos LAN del gateway y red de gestión: https://www.omadanetworks.com/lk/support/faq/3157/
- Perfiles de puerto creados por el controlador (ejemplo completo): https://www.omadanetworks.com/eg/support/faq/4122/
