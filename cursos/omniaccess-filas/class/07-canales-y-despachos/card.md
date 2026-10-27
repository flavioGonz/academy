# Lección 7. Canales y despachos

**Escuchá:** canales-y-despachos.mp3 (2 min)

**La idea, en tres líneas**
- Notificaciones (dirección `/admin/notificaciones`) tiene las pestañas Canales, Destinatarios, Reglas, Horarios, Plantillas y Suscriptores; cada canal tiene "Enviar prueba".
- Las alertas de aforo mandan a cada destinatario activo; las Reglas suman criterios propios (métrica, operador, días, horario, canales). El "Clip animado en alertas" agrega 5 s antes y 3 s después del momento.
- Todo pasa por una cola con reintentos (5 intentos, espera exponencial) y queda a la vista en Despachos, con "Reintentar".

**Impacto:** ante un "no me llegó" mostrás qué salió, a quién y cuándo, y reintentás sin rearmar nada.

**Quién lo dice:** 3 de 4 fuentes explican Web Push con claves VAPID y service worker (RFC 8030, Pushpad, MDN); BullMQ documenta el backoff exponencial; la API de Telegram, la descarga por URL. Canales, pestañas y límites de esta versión salen del código.

**Laboratorio** · Admin · 20 min
Instalación de prueba con la alerta "Aforo Caja 1" de la lección 6. Un bot de Telegram de prueba y un grupo de prueba.
1. Abrí `/admin/notificaciones` → Canales → Telegram. Cargá Bot Token y Chat ID de prueba, activá el canal y tocá "Enviar prueba".
2. Pestaña Destinatarios: agregá uno con "Nuevo".
```text
Nombre:     Supervisor (prueba)
Canal:      Telegram
Dirección:  -100123456789   (chat id de ejemplo)
```
Activá "Clip animado en alertas".
3. Pestaña Reglas → "Nueva regla" (opcional): "Aforo crítico caja", Zona / canal Aforo, Métrica Aforo, Operador >=, Umbral 3, Desde 08:00, Hasta 20:00, Canales destino Telegram, Cooldown 60.
4. Forzá la alerta con tres personas en la zona.
5. Abrí Despachos. En "Cola de despachos" seguí el envío: Pendiente → Procesando → Enviado. A la derecha aparece la alerta con destinatario, canal y mensaje.
6. Si queda "Fallido", leé el error y tocá "Reintentar" después de corregir. Errores típicos:
```text
Faltan credenciales de Telegram     falta Bot Token o Chat ID
Telegram: ... (URL de la foto)      la dirección pública del servidor no responde desde internet
Canal no soportado: email           esta versión no envía correo desde la cola
```
7. Desde el servidor, el worker deja su registro:
```bash
pm2 logs dispatch-worker --lines 30
```

⚠️ El Bot Token y la API Key de OpenWA dan control del canal: no van en capturas, chats de obra ni documentos para el cliente.

**Regla para quedarse**
Un canal no está configurado hasta que llegó la prueba y vi el despacho en Enviado.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Reintentos con backoff exponencial (BullMQ): https://docs.bullmq.io/guide/retrying-failing-jobs
- sendPhoto y sendAnimation, y la descarga por URL (Telegram Bot API): https://core.telegram.org/bots/api
- Qué es VAPID y por qué hace falta (Pushpad): https://pushpad.xyz/blog/web-push-what-is-vapid/
- Web Push (RFC 8030): https://datatracker.ietf.org/doc/html/rfc8030
