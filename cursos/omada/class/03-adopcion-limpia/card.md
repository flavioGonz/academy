# Lección 3. Adopción limpia

**Escuchá:** adopcion-limpia.mp3 (2 min)

**La idea, en tres líneas**
- El equipo busca al controlador con un broadcast al UDP 29810 en su subred; si no aparece en Pending, lo primero es mirar si está en la misma VLAN.
- "Adopt Failed" se lee: credenciales (usá las de la web local o las de Device Account del controlador anterior), sin respuesta (VLAN, loops, firewall) o uplink mesh.
- Equipo usado: reset de fábrica antes de adoptar. Adoptado, la GUI local deja de servir y manda el controlador.

**Impacto:** la adopción deja de ser prueba y error y se resuelve leyendo un mensaje.

**Quién lo dice:** 3 de 4 fuentes sobre adopción coinciden en empezar por la VLAN; 4 de 5 coinciden en que, adoptado, el equipo obedece al controlador. No se encontró discrepancia.

**Laboratorio** · Campo · 15 min
Con un controlador (Lección 2 o un OC) y un EAP en la misma VLAN:
1. Conectá el EAP de fábrica y buscá su IP en el DHCP. En el controlador: **Devices**, debería estar en **Pending**. Adoptalo.
2. Forzá un fallo: en el controlador, **Forget** del EAP. Reseteá el EAP, entrá a su web local (`http://<IP-del-EAP>`, usuario inicial `admin`/`admin`) y poné una clave nueva de ejemplo (`Lab-Omada-2026`).
3. Volvé al controlador e intentá adoptarlo: va a aparecer **Adopt Failed**. Usá **Retry** con el usuario y la clave de la web local.
4. Anotá el mensaje exacto que viste y en qué paso se resolvió.
```text
Mensaje -> Qué revisar
"username or password is incorrect" -> clave de la web local o Settings > Site > Device Account del otro controlador
"does not respond to adopt commands" -> VLAN tags hasta el DHCP, loops, ping desde el controlador, firewall/antivirus
"Failed to link to uplink AP"       -> distancia/obstáculos entre root y mesh AP, otro uplink
Switch sin botón de reset            -> consola a 38400 baudios, BootUtil
```

**Regla para quedarse**
Si no aparece en Pending, primero la VLAN; si falla la adopción, leer el mensaje antes de resetear.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Guía oficial de adopción fallida (Controller v5): https://support.omadanetworks.com/document/13176/
- Cómo descubre un EAP al controlador y qué puertos usa: https://support.omadanetworks.com/document/13090/
- Adoptar un gateway nuevo y el Adopt Failed con la clave local: https://www.hostifi.com/support/omada-how-to-adopt-a-gateway-to-the-controller
