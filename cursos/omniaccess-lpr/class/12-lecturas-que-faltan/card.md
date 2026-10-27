# Lección 12. Lecturas que faltan

**Escuchá:** lecturas-que-faltan.mp3 (2 min)

**La idea, en tres líneas**
- "Dejaron de entrar matrículas" se diagnostica con un árbol: ¿llegan eventos a Webhooks? Si no llega nada, red o receptor caído. Si llegan sin matrícula, la cámara no está haciendo ANPR. Si es una sola cámara: estado, ping, HTTP host (se pierde con un reset) y tasa de lectura, porque leer mal no es lo mismo que no leer.
- En las cámaras con analítica propia, ANPR y la búsqueda por imagen del NVR son excluyentes: si alguien agrega el canal LPR a esa búsqueda, el recurso inteligente pasa de `roadDetection` a `smart` y la cámara deja de leer en silencio. Se revierte en orden: sacar el canal de la búsqueda del NVR, volver a `roadDetection`, reiniciar y esperar unos 80 segundos.
- La salud se vigila sola: alertas de sin respuesta (dos sondeos), disco del NVR, memoria arriba de 95 %, reloj con más de 120 segundos y ANPR apagado (modo VCA), con historial de 14 días y aviso por Telegram para cámaras LPR y NVR.

**Impacto:** la llamada de urgencia se resuelve en minutos y por orden, y la falla silenciosa (cámara con imagen que no lee) aparece como alerta antes de que falte una evidencia.

**Quién lo dice:** el Manual del Instalador, el README y el código coinciden en el árbol y en la exclusión ANPR/búsqueda por imagen. En IPCamTalk un integrador cuenta que al cambiar el modo de detección de la cámara dejó de recibir los POST: la misma familia de falla. La web discrepa en cuánto confiar: los fabricantes hablan de 95 a 99 %, las fuentes críticas recuerdan que eso es sobre patentes legibles.

**Laboratorio** · Campo · 20 min
En una cámara ANPR Hikvision de prueba (`192.0.2.21`) dada de alta y un NVR de prueba.
1. Dispositivos: leé Estado, Latencia y Hora / NTP de la cámara. Abrí su historial y alertas.
2. Configuración → Sistema → Webhooks: pasá un auto. ¿Llega el evento? ¿Con matrícula?
3. Preguntale a la cámara en qué modo está el recurso inteligente (te pide la contraseña del usuario integrador):
```bash
curl -s --digest -u integrador 192.0.2.21/ISAPI/System/Video/inputs/channels/1/VCAResource
```
Tiene que decir `<type>roadDetection</type>`.
4. Confirmá que el motor de patentes está habilitado:
```bash
curl -s --digest -u integrador 192.0.2.21/ISAPI/Traffic/channels/1/vehicleDetect | grep -i enabled
```
5. En el NVR, revisá que el canal de esa cámara no esté en la configuración de búsqueda por imagen.
6. Desconectá la cámara de prueba unos 3 minutos: aparece la alerta de sin respuesta. Reconectala y mirá que se normalice.
7. Tasa de lectura de esa cámara por hora: anotá la franja peor.
8. Recorré la lista de entrega: lee de día y de noche, tasa arriba de 90 %, grabación desde un evento de cada cámara, relojes, reinicio del servidor con todo volviendo solo, retención, avisos probados, padrón cargado y claves de fábrica cambiadas.
⚠️ Nunca agregues un canal LPR a la búsqueda por imagen del NVR: si el cliente quiere las dos cosas en un acceso, va una segunda cámara de contexto.

**Regla para quedarse**
Diagnostico con el árbol, de la red a la cámara, y la cámara de patentes no se comparte con la búsqueda por imagen del NVR.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Cuando cambiar el modo de la cámara corta los envíos: https://ipcamtalk.com/threads/assistance-with-hikvision-ds-2cd7a26g0-p-izs-integration-using-http-listening.79674/post-897038
- Sondear la salud de equipos Hikvision por ISAPI: https://hertzbeat.incubator.apache.org/docs/help/hikvision_isapi
- Cómo medir la exactitud de un sistema LPR sin engañarse: https://perceptics.com/measuring-license-plate-recognition-accuracy/
