# Lección 10. Lista de vigilancia

**Escuchá:** lista-de-vigilancia.mp3 (2 min)

**La idea, en tres líneas**
- Tres categorías: Lista negra (rojo con sonido; toda lectura queda Denegada y la matrícula pasa a la lista de bloqueo de las lectoras), VIP / Autorizado (verde, se destaca) y En búsqueda (ámbar: avisa cuando aparece, sin bloquear).
- Se carga desde el escudo Lista de vigilancia del Monitor LPR o con el botón Lista negra de la ficha. La matrícula va como la lee la cámara, sin espacios ni guiones, y En búsqueda pide un motivo: es lo que el guardia ve en la captura.
- Avisa manda Telegram cuando la detecta; En silencio la muestra solo en el monitor. Un usuario con rol de bloqueado arrastra todas sus matrículas, y la lista negra le gana a cualquier pase de invitado.

**Impacto:** la alerta roja aparece solo para lo que importa, con el porqué escrito, y el guardia sabe qué hacer sin llamar a nadie para preguntar.

**Quién lo dice:** el Manual del Administrador y el código describen las categorías, el aviso y la carga en las lectoras. La web pone el límite: en Roseville el 71 % de las alertas de vehículo buscado eran lecturas equivocadas, y gatesentry documenta cámaras que "inventan" patentes a partir de carteles. Nadie discrepa en verificar el recorte antes de actuar.

**Laboratorio** · Foco · 15 min
En una instalación de prueba (los pasos 3 y 5 crean eventos reales).
1. Monitor LPR → ícono del escudo, Lista de vigilancia.
2. Agregá la matrícula `SAB2024` (sin espacio), categoría En búsqueda, motivo "Prueba IES: camioneta reportada por la administración", con Avisa.
3. Mandá una lectura simulada de esa matrícula (o pasá el auto de prueba):
```bash
curl -s -X POST 192.0.2.10:10000/api/webhooks/hikvision -H "Content-Type: application/xml" \
  --data '<EventNotificationAlert><ipAddress>192.0.2.21</ipAddress><eventType>ANPR</eventType><ANPR><licensePlate>SAB2024</licensePlate></ANPR></EventNotificationAlert>'
```
4. Mirá la tarjeta ámbar con el motivo. Compará el recorte con la matrícula leída.
5. Volvé a la lista y pasala a Lista negra (el sistema pregunta "¿Pasarla a...?": Sí, cambiarla). Leé el resumen de las lectoras. Mandá otra lectura pasados 25 segundos: rojo, con sonido y Denegada.
6. Dala de baja al terminar y verificá que el contador del escudo baje.
⚠️ Antes de activar un protocolo por lista negra o búsqueda, el guardia confirma a ojo que el recorte dice esa patente: un 8 leído como 9 es una persona inocente frenada en el portón.

**Regla para quedarse**
Nadie entra a la lista sin motivo escrito, y ninguna alerta se actúa sin mirar el recorte.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Roseville: alertas de vehículo buscado y lecturas equivocadas: https://www.techspot.com/community/topics/one-california-town-found-flocks-license-plate-cameras-were-wrong-71-of-the-time.298313/
- Falsos positivos y patentes "inventadas" desde carteles: https://gatesentry.com/blog/license-plate-recognition-hoa-gates/
- Listas blancas y negras dentro de la cámara: https://syscom.mx/blog/hikvision-anpr-reconocimiento-de-placas
