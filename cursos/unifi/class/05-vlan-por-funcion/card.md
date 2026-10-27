# Lección 5. VLAN por función

**Escuchá:** vlan-por-funcion.mp3 (2 min)

**La idea, en tres líneas**
- Una red por función (staff, invitados, CCTV, IoT), cada una con su VLAN ID y su propio DHCP.
- Con el firewall clásico UniFi permitía tráfico entre VLANs por defecto; desde Network 11.0 todos los sitios pasan al firewall por zonas.
- Cada red va a una zona (Internal, Hotspot, DMZ o una propia) y la Zone Matrix muestra qué puede hablar con qué.

**Impacto:** un celular de invitado o una cámara comprometida no llegan a las PCs ni al NVR.

**Quién lo dice:** 4 de 5 fuentes enseñan una VLAN por función; The Hook Up deja las cámaras en la red principal para no cargar el router con el tráfico entre VLANs y lo compensa con reglas y MAC fija por puerto.

**Laboratorio** · Foco · 15 min
En la consola de laboratorio con gateway UniFi (UniFi Network 10.6 u 11.0):
1. Settings > Networks > Create New, tres veces:
```text
Nombre    VLAN  Subred            Zona
Staff     10    10.10.10.0/24     Internal
Invitados 20    192.168.20.0/24   Hotspot
CCTV      30    192.168.30.0/24   Internal o una zona propia "CCTV"
```
Dejá el DHCP del gateway activo en cada una.
2. Si el formulario no muestra el campo Zone, el sitio todavía está en el firewall clásico: buscá en Settings la opción de actualizar al firewall por zonas (Policy Engine).
3. Abrí la Zone Matrix (Settings > Policy Engine > Zones) y leé la fila de Hotspot y la de tu zona CCTV: qué dice hacia Internal y hacia el gateway.
4. Para CCTV en zona propia, creá una política que permita solo del NVR hacia las cámaras y bloquee el resto.
⚠️ Al actualizar un sitio viejo a Network 11, las reglas clásicas se migran a zonas: revisá la matriz el mismo día.

**Regla para quedarse**
Cada VLAN nueva sale con nombre claro, DHCP propio y zona elegida.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- VLAN tagging en UniFi, con el ejemplo staff, invitados y CCTV: https://www.unihosted.com/blog/everything-you-need-to-know-about-vlan-tagging-in-unifi
- Cómo era la segmentación con el firewall clásico: https://lazyadmin.nl/home-network/unifi-vlan-configuration/
- Notas de Network 11.0.97, migración a zonas: https://community.ui.com/releases/UniFi-Network-Application-11-0-97/15662d06-8122-44e2-a1ba-af5d71b8a045
