# Lección 6. Monitor y evento

**Escuchá:** monitor-y-evento.mp3 (2 min)

**La idea, en tres líneas**
- El Monitor Facial muestra los eventos de rostro de las últimas 24 horas en tres columnas: Entrada, el centro con el último evento grande y las Capturas Recientes, y Salida.
- Arriba están el indicador LIVE u OFFLINE (si tu pantalla está conectada al servidor), los filtros Todos, Permitidos y Denegados, y el botón para recargar.
- Cada foto abre la ficha del evento: persona o "Desconocido", similitud, Autorizado o No registrado, y las acciones Registrar, Exportar y ver la grabación si la cámara tiene canal en el NVR.

**Impacto:** el guardia distingue en segundos un desconocido de un vecino que el terminal dejó pasar pero el sistema no vinculó, y deja evidencia exportada cuando la piden.

**Quién lo dice:** el código del Monitor Facial y de la ficha del evento; para lo técnico de fondo, go2rtc (video en vivo y fotos por API) y MDN (notificaciones push con permiso del usuario). No hay fuentes externas que discrepen: es la pantalla del producto.

**Laboratorio** · Rápido · 15 min
Práctica guiada en una instalación de demo con al menos un terminal enviando eventos:
1. Abrí el monitor:
```text
Menú → Monitor en Vivo   (en modo Face abre el Monitor Facial)
```
2. Mirá el indicador de arriba a la derecha. LIVE en verde: tu pantalla recibe eventos al instante. OFFLINE en rojo: recargá la página y revisá la red del puesto.
3. Pasá una cara enrolada por el terminal de Entrada. Fijate dónde aparece: la columna Entrada se ilumina, el centro muestra el evento grande con nombre, unidad y equipo, y abajo queda en Capturas Recientes.
4. Tocá Denegados. Elegí un evento con borde rojo y abrilo. Respondé:
```text
¿Tiene nombre o dice "Desconocido"?
¿Qué similitud figura?
¿Dice Autorizado o No registrado?
¿La foto es la captura de la puerta o la del alta?
```
5. Si el evento muestra el nombre de un residente conocido pero figura Denegado y No registrado, y la puerta se abrió, anotalo para el técnico: el terminal lo reconoció y abrió, pero OmniAccess no lo vinculó con su ficha (se ve en la lección 10). "Desconocido" en ámbar, en cambio, es una cara que el terminal no reconoció.
6. En la ficha del evento tocá Exportar: baja un ZIP con la foto y los datos (y un clip de 30 s si la cámara tiene canal en el NVR).
7. Opcional: abrí la app Control Facial en el celular del puesto (dirección /pwa/face de tu sistema) y compará los contadores Reconocidos y Denegados con el monitor.

⚠️ Si la columna muestra "Sin señal" en lugar del video, el monitor sigue registrando eventos: lo que falta es el video en vivo del terminal, que se configura aparte en el servidor de video.

**Regla para quedarse**
Antes de actuar sobre un Denegado, abrí la ficha y mirá la foto.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Cómo un servidor de video entrega MJPEG y fotos por API (go2rtc): https://raw.githubusercontent.com/AlexxIT/go2rtc/HEAD/internal/mjpeg/README.md
- Notificaciones push en aplicaciones web (MDN): https://developer.mozilla.org/en-US/docs/Web/API/Push_API
