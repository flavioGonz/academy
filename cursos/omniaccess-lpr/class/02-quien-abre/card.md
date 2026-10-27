# Lección 2. Quién abre

**Escuchá:** quien-abre.mp3 (2 min)

**La idea, en tres líneas**
- La barrera la puede abrir la propia cámara: tiene una lista blanca cargada desde OmniAccess y, al leer una patente de esa lista, cierra su relé (el semáforo verde). La lista negra va a la lista de bloqueo de la cámara.
- El servidor decide en este orden: si la cámara informó su lista, manda la cámara; si no, busca la matrícula como credencial de tipo matrícula (sin espacios ni guiones). Con Modo LPR en Lista Blanca, registrada es Autorizado; sin credencial, Denegado.
- Antirrebote: la misma matrícula no se registra dos veces en 5 segundos, ni dos veces por la misma cámara en 20. Una lectura sin chapa (NO_LEIDA) nunca se agrupa.

**Impacto:** cuando un residente dice "no me abrió", sabés si mirar la lista de la cámara, el padrón del servidor o el modo, y no culpás al auto.

**Quién lo dice:** 2 de 2 fuentes web (Syscom y Epcom) muestran la lista y la salida de alarma en la cámara Hikvision; el orden de decisión, los modos y el antirrebote salen del código de OmniAccess (el Manual del Administrador agrega el horario del grupo, que esta versión del receptor no evalúa).

**Laboratorio** · Foco · 15 min
Solo en una instalación de prueba: cada envío crea un evento real.
1. Configuración → Modos → Modos (LPR / Face / Cola) → Modo LPR: mirá cuál opción está activa (Lista Blanca, Lista Negra o Aprendizaje). No la cambies.
2. Desde una PC de la red, mandá una lectura simulada de la cámara `192.0.2.21` con una matrícula que no está en el padrón:
```bash
curl -s -X POST 192.0.2.10:10000/api/webhooks/hikvision \
  -H "Content-Type: application/xml" \
  --data '<EventNotificationAlert><ipAddress>192.0.2.21</ipAddress><eventType>ANPR</eventType><ANPR><licensePlate>SBA1234</licensePlate></ANPR></EventNotificationAlert>'
```
3. La respuesta trae `"decision":"DENY"` y en Monitor LPR aparece Denegado (ámbar).
4. Repetí el mismo comando enseguida: la respuesta dice `Debounced`, el antirrebote la descartó.
5. En el foco central tocá Registrar: nombre "Prueba IES", unidad de prueba, matrícula `SBA1234` ya cargada. Guardá.
6. Esperá 25 segundos y volvé a mandar el comando: ahora `"decision":"GRANT"` y la tarjeta en verde.
7. Al terminar, suspendé o borrá el usuario de prueba.
⚠️ En producción no se cambia el Modo LPR ni se mandan lecturas simuladas: alteran el historial y lo que ve el guardia.

**Regla para quedarse**
En cada portón sé quién abre: la cámara con su lista, el servidor con el padrón, o los dos.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Listas blancas y negras en cámaras ANPR Hikvision y acciones al leer: https://syscom.mx/blog/hikvision-anpr-reconocimiento-de-placas
- Salida de alarma de la cámara para la barrera: https://blog.epcom.net/?p=128
- La tolerancia de un carácter en accesos cerrados: https://en.wikipedia.org/wiki/Automatic_number-plate_recognition
