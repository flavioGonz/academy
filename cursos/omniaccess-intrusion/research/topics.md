# Mapa del tema: OmniAccess Intrusión

Nivel: inicial a intermedio. Público: técnico instalador de IES y operador (guardia, puesto de monitoreo).
Fuente principal: el código de OmniAccess (octubre de 2026). Fuentes web: fabricantes (Hikvision, Dahua y OEM, Milesight, Uniview, Ajax, Bosch, Axis), estándares (ONVIF, RTSP, Web Push), herramientas (go2rtc, MinIO, Telegram) y practicantes (foros, centrales de monitoreo).

- T01 Qué es una analítica de intrusión: cruce de línea, intrusión de zona, entrada y salida de región; diferencia con detección de movimiento.
- T02 Cómo llega el evento: push HTTP de la cámara (servidor de alarma / HTTP host / "notificar al centro de vigilancia") frente a suscripción (stream de eventos, eventManager de Dahua, PullPoint de ONVIF).
- T03 Configurar la regla en la cámara: dibujar línea o zona, sentido A→B, sensibilidad, umbral de tiempo, porcentaje, tamaño de objeto.
- T04 Clasificación de objetivo (persona, vehículo) y filtros de falsa alarma (AcuSense y equivalentes).
- T05 Horario de armado: qué es, diferencia con el horario de grabación, fallas típicas.
- T06 Alta del equipo en el sistema: cámara, NVR, mapeo de canales, credenciales, hora.
- T07 Probar la cadena: test del servidor de alarma, heartbeat, respuesta 200, estado de conexión.
- T08 Causas de falsas alarmas y cómo bajarlas: instalación, configuración, tecnología, proceso.
- T09 Verificación de alarmas por video y atención: confirmar, falsa alarma, despacho, hechos.
- T10 Video en vivo y reproducción: RTSP, go2rtc, flujo principal y secundario, NVR.
- T11 Evidencia y registro: fotos, clips, retención, auditoría.
- T12 Avisos: sonido en el puesto, pantallas de pared, Telegram, Web Push, WhatsApp.
- T13 Correlación: varias cámaras en poco tiempo (recorrido), ráfagas, ritmo habitual, cruce de zonas.
- T14 Mapa y ubicación del evento en el predio.
- T15 Guardia en el terreno: coordinación con el puesto, posición en el mapa.
- T16 Diagnóstico: el evento no llega, no hay foto, no hay grabación, la cámara no responde.
