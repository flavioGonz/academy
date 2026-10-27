# Lección 3. Inform remoto

**Escuchá:** inform-remoto.mp3 (2 min)

**La idea, en tres líneas**
- En capa 3 el equipo necesita saber la URL de inform: arranca en http, sigue el nombre del controlador y termina en :8080/inform.
- DHCP option 43 o un nombre DNS "unifi" sobreviven a reinicios y actualizaciones; set-inform por SSH es el plan B.
- Con el controlador detrás de NAT o en contenedor, configurá Inform Host con Override para que los equipos reciban la dirección correcta.

**Impacto:** los equipos remotos vuelven solos al controlador después de un reinicio o un corte.

**Quién lo dice:** 2 de 4 fuentes prefieren option 43 o DNS (el soporte de Ubiquiti, citado en el foro, lo recomienda); Tom Lawrence usa set-inform con todos sus clientes sin problemas, y Sikich lo usa para migrar.

**Laboratorio** · Foco · 20 min
Controlador en 10.10.10.5 (nombre unifi.example.com), sitio remoto en 192.168.88.0/24 con un MikroTik de laboratorio y ruta entre ambos.
1. Opción A, DHCP option 43 en RouterOS 7. El valor es 01 (subopción) 04 (largo) y la IP en hexadecimal (10.10.10.5 = 0A0A0A05):
```routeros
/ip dhcp-server option add name=unifi-inform code=43 value=0x01040A0A0A05
/ip dhcp-server network set [find address=192.168.88.0/24] dhcp-option=unifi-inform
```
Con un gateway UniFi en el sitio, el mismo dato va en la red, campo "Option 43 Application Host Address".
2. Opción B, DNS. Que el nombre `unifi` resuelva al controlador para los clientes de ese DHCP:
```routeros
/ip dns static add name=unifi address=10.10.10.5
```
3. Reset de fábrica del AP en la red 192.168.88.0/24 y esperá que aparezca pendiente en el controlador. Adoptá.
4. Opción C, plan B por SSH (equipo reseteado, usuario de fábrica):
```bash
ssh ubnt@192.168.88.20
set-inform http://<controlador>:8080/inform
info
```
Donde `<controlador>` es el nombre DNS del controlador (en este laboratorio, unifi.example.com).
Si queda pendiente, adoptalo en el controlador y repetí `set-inform` una vez más.
5. Controlador en VM con NAT o en contenedor: en UniFi Network, Settings > System > Advanced, Inform Host, marcá Override y poné el nombre o IP alcanzable.
⚠️ El puerto 8080 del controlador tiene que ser alcanzable desde el sitio remoto. Exponelo solo hacia las IP de tus sitios o por VPN, nunca abierto a todo internet.

**Regla para quedarse**
En sitios remotos, el inform lo entrega el DHCP o el DNS, no la memoria del equipo.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Hilo sobre inform que vuelve al valor de fábrica, con la respuesta de Ubiquiti: https://forums.lawrencesystems.com/t/unifi-l3-persistent-inform-url/20405
- Formato correcto de la URL de inform: https://www.hostifi.com/support/unifi-troubleshooting-unifi-cloud-adoption
- Inform Host con Override en los comentarios: https://lazyadmin.nl/home-network/unifi-adoption-failed/
