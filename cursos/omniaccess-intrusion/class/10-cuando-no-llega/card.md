# Lección 10. Cuando no llega

**Escuchá:** cuando-no-llega.mp3 (2 min)

**La idea, en tres líneas**
- Se diagnostica de la cámara hacia el monitor, un eslabón por vez: ¿la regla detecta y está armada ahora? ¿La vinculación tiene **Notificar al centro de vigilancia**? ¿El servidor de alarma apunta a OmniAccess (campana verde, **Probar reporte**)? ¿El servidor recibe en el puerto 10000?
- Del lado de OmniAccess: la cámara tiene que estar dada de alta con la IP o la MAC que manda en el evento; si no, la detección entra sin cámara y no pinta ningún canal. Sin la clave propia de la cámara no hay foto; sin NVR y canal no hay grabación; con la hora corrida, el clip no coincide.
- Con Dahua: **Verificar suscripción** tiene que decir "Suscripción activa"; "NVR no accesible" es red o credenciales del NVR. La salud de cada equipo está en **Dispositivos** y en la pantalla **Salud del sistema**, y Telegram avisa cuando una cámara deja de responder.

**Impacto:** una visita de soporte se resuelve en minutos y sin cambiar nada a ciegas.

**Quién lo dice:** 2 de 2 fuentes usan el test y el estado de conexión para probar el camino; Home Assistant agrega el permiso de notificar al centro y la autenticación digest; Bosch documenta que por ONVIF los cruces van por otro tópico (2 de 3).

**Laboratorio** · Campo · 25 min
En la demo, un compañero rompe a propósito tres eslabones sin decirte cuáles (por ejemplo: destilda Notificar al centro de vigilancia, arma la línea solo de 08:00 a 09:00 y cambia la clave de la cámara). Vos diagnosticás:
1. Cruzá la línea. ¿Aparece algo en la franja **Detecciones**? Anotá sí o no.
2. Vista de pared: ¿la línea está **armada ahora** (punto verde)? Si no, revisá el horario en la cámara.
3. Campana del canal: ¿**OmniAccess presente**? Tocá **Probar reporte**.
4. Web de la cámara: regla de cruce, **Método de vinculación**, tilde de **Notificar al centro de vigilancia**.
5. Desde una PC en la red de cámaras, probá que el puerto de eventos del servidor responda:
```bash
curl -s -o /dev/null -w "%{http_code}\n" -X POST 192.0.2.10:10000/api/webhooks/hikvision
```
Cualquier código HTTP quiere decir que el puerto está abierto; un timeout es red o firewall.
6. Si llega la detección pero sin foto, revisá usuario y clave de la cámara en **Dispositivos → Editar**.
7. Si no hay grabación, revisá NVR y canal, y la hora en **Sincronizar hora**.
8. Anotá los tres eslabones rotos y cómo los encontraste.

⚠️ No resetees la cámara para "probar": se pierden la regla, el horario y el servidor de alarma.

**Regla para quedarse**
Diagnosticá de la cámara hacia el monitor, un eslabón por vez.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Estado Online u Offline, heartbeat y respuesta del servidor a cada envío: https://videos.cctvcamerapros.com/developer/docs/getting-started/http-post-setup
- Permiso de notificar al centro y autenticación digest en Hikvision (Home Assistant): https://www.home-assistant.io/integrations/hikvision
- Cruces por ONVIF en otro tópico (Bosch): https://knowledge.keenfinity-group.com/video-systems/article/tns1-iva-does-not-include-all-iva-rules-in-camera
