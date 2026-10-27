# Lección 1. Camino del evento

**Escuchá:** camino-del-evento.mp3 (2 min)

**La idea, en tres líneas**
- La cámara (o el NVR Dahua) es la que detecta: cruce de línea o intrusión de zona. OmniAccess recibe el aviso, lo guarda como detección, le pide la foto a la cámara y lo muestra al instante en el Monitor Intrusión.
- Dos vías según la marca: una cámara Hikvision empuja el evento al servidor de alarma de OmniAccess (proceso de webhooks, puerto 10000); con un NVR Dahua, OmniAccess se suscribe al NVR y escucha sus eventos.
- El movimiento simple (VMD) se descarta al llegar y, en esta versión, no entra nada por ONVIF. Lo que cuenta es la analítica: cruce de línea, intrusión, entra a zona, sale de zona.

**Impacto:** cuando algo no llega, ya sabés en qué tramo buscar: cámara, red, servidor o pantalla.

**Quién lo dice:** 5 de 5 fuentes separan cruce de línea, intrusión y movimiento como eventos distintos; 4 de 6 describen el push de la cámara y la suscripción como las dos vías. Lo de OmniAccess sale del código de octubre de 2026.

**Laboratorio** · Rápido · 10 min
En la instalación de demo, con usuario de panel:
1. Abrí el menú lateral y fijate que aparezca **Monitor Intrusión**. Si no está, el sistema no tiene el módulo LPR o está en modo Filas: según cómo esté configurado tu sistema.
2. Entrá a **Dispositivos** y elegí la vista **Intrusión**. Anotá en una hoja, por cámara: nombre, IP, NVR y canal.
3. Para cada cámara, anotá quién detecta y por dónde avisa:
```text
Cámara Hikvision (directa o en NVR Hikvision)  -> push al servidor de alarma (puerto 10000)
Cámara de cualquier marca en NVR Dahua        -> suscripción al NVR (eventManager)
Cámara Dahua en NVR Hikvision                 -> sin vía: se configura en la cámara o se pasa a un NVR Dahua
```
4. Abrí **Monitor Intrusión** y dejá el filtro en **Intrusión**. Mirá la franja **Detecciones** de la derecha: cada tarjeta dice el tipo (Cruce de línea, Intrusión, Entra a zona, Sale de zona).
5. Dibujá en la hoja el camino completo de una detección: cámara, red, servidor 192.0.2.10:10000, base de datos, foto en el bucket de intrusión, pantalla.

**Regla para quedarse**
Antes de tocar nada, sabé quién detecta y por dónde avisa.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Eventos de Hikvision y "notificar al centro de vigilancia" (integración de Home Assistant): https://www.home-assistant.io/integrations/hikvision
- Reglas LineDetector y FieldDetector del estándar ONVIF: https://www.onvif.org/specs/2206/Analytics.html
- Códigos de evento de Dahua y suscripción con eventManager: https://community.home-assistant.io/t/dahua-ipc-to-mqtt-app/93327?page=5
