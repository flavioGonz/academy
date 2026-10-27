# Lección 6. Puertos con perfil

**Escuchá:** puertos-con-perfil.mp3 (2 min)

**La idea, en tres líneas**
- Por defecto un puerto de switch UniFi acepta todas las VLANs etiquetadas: sirve para uplinks y AP, no para equipos finales.
- Puerto de cámara o IoT: Native VLAN = la red del equipo y Tagged VLAN Management = Block All.
- En puertos expuestos (exterior, estacionamiento), sumá MAC fija o "Lock Port to UniFi Device" (Network 10.6.101, switch con firmware 7.6 o superior).

**Impacto:** quien desenchufa una cámara y conecta una notebook cae en la VLAN de cámaras y nada más.

**Quién lo dice:** 3 de 4 fuentes enseñan nativa más bloqueo de etiquetadas en puertos de equipo final; nadie discrepa, y The Hook Up agrega la MAC fija como capa extra.

**Laboratorio** · Foco · 10 min
1. UniFi Network > Port Manager > elegí el switch y el puerto de la cámara.
2. Configurá:
```text
Native VLAN / Network:     CCTV (VLAN 30)
Tagged VLAN Management:    Block All
```
3. Hacé Power Cycle del puerto (PoE) para que la cámara renueve IP y verificá que tome una de 192.168.30.0/24.
4. Puerto del AP y uplink:
```text
Native VLAN / Network:     Staff o la red de gestión
Tagged VLAN Management:    Allow All
```
5. Si entre el gateway y el AP hay un switch de terceros, dejá la VLAN de gestión del AP sin etiquetar en ese switch y las de los SSID etiquetadas.
6. Prueba: enchufá una notebook en el puerto de la cámara. Tiene que recibir IP de la VLAN 30 y no llegar a la red Staff.
⚠️ Cambiar la VLAN nativa del puerto de un AP o de un uplink puede dejar sin gestión todo lo que cuelga de ahí. Hacelo en el puerto de un equipo final primero.

**Regla para quedarse**
Puerto que da a la calle: VLAN nativa de su red y nada etiquetado.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Native VLAN y Block All en Port Manager: https://lazyadmin.nl/home-network/unifi-vlan-configuration/
- Seguridad de puerto con MAC fija, el caso de la cámara arrancada: https://www.thesmarthomehookup.com/test_install/unifi-network-update-part-2-vlans-wifi-partitioning-and-advanced-features/
- Lock Port to UniFi Device en las notas de 10.6.101: https://community.ui.com/releases/UniFi-Network-Application-10-6-101/05283624-0980-4dd7-b8d6-9fa5c4e28da4
