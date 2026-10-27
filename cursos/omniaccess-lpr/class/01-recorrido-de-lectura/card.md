# Lección 1. Recorrido de lectura

**Escuchá:** recorrido-de-lectura.mp3 (2 min)

**La idea, en tres líneas**
- La cámara ANPR lee la patente a bordo y manda el evento (XML más fotos) por HTTP al servidor OmniAccess del predio, al puerto de webhooks `10000`.
- El servidor decide Autorizado o Denegado, guarda la foto en el almacenamiento (bucket `lpr`) y el evento en la base, y lo empuja al Monitor LPR en 1 a 3 segundos.
- Todo corre adentro del barrio: sin internet se sigue leyendo, decidiendo y grabando; solo se demoran los avisos externos.

**Impacto:** cuando algo falla, sabés en qué tramo buscar (cámara, red, servidor, NVR o pantalla) en vez de reiniciar todo a ciegas.

**Quién lo dice:** 3 de 3 fuentes web describen el mismo pipeline (capturar, leer, enviar, validar); el recorrido propio de OmniAccess sale del Manual del Instalador ("Qué se instala") y del código. Nadie discrepa en la forma, sí en cuánto se puede confiar en la lectura (lo vemos al cierre del curso).

**Laboratorio** · Rápido · 15 min
Hacelo en una instalación de prueba o de demo, con el servidor en `192.0.2.10` y una cámara `P1 - Entrada (21)` en `192.0.2.21`.
1. Desde la PC del puesto, abrí la ruta de salud del receptor de eventos: tiene que contestar `OK`.
```text
192.0.2.10:10000/health
```
2. En el panel, entrá a Configuración → Sistema → Webhooks y dejala abierta en una pestaña.
3. Pasá un vehículo frente a la cámara de prueba, a paso de hombre, y mirá que aparezca el evento con la matrícula en Webhooks.
4. En otra pestaña abrí Monitor LPR: la captura aparece en la columna Entradas y en el foco central. Cronometrá cuánto tardó desde que el auto cruzó la línea.
5. Clic en la captura → Investigar → pestaña Datos: anotá dispositivo, canal del NVR y los metadatos que mandó la cámara.
6. En una hoja dibujá los cinco tramos (cámara, red, servidor, almacenamiento y base, monitor) y escribí al lado el tiempo medido.
⚠️ Si tarda más de 10 segundos de forma habitual, algo está degradado (red, cámara o servidor): es el primer dato para el diagnóstico.

**Regla para quedarse**
Cuando algo falla, primero ubico en qué tramo del recorrido se cortó la lectura.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Cómo funciona ANPR por dentro, de la imagen al OCR: https://en.wikipedia.org/wiki/Automatic_number-plate_recognition
- El XML que manda una cámara Hikvision por HTTP Listening: https://ipcamtalk.com/threads/get-passed-license-plate-numbers-using-isapi.79032/post-888496
- La historia de ANPR desde 1976: https://www.traffictechnologytoday.com/features/feature-who-invented-anpr-the-untold-british-story-behind-a-global-traffic-technology-revolution.html
