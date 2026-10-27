# Lección 4. Horario de armado

**Escuchá:** horario-de-armado.mp3 (2 min)

**La idea, en tres líneas**
- Cada regla (línea y zona) tiene su horario de armado **en la cámara**. Dentro del horario avisa; fuera, la cámara sigue grabando en el NVR pero no manda ni cruce, ni zona, ni foto. No es el horario de grabación.
- OmniAccess lee ese horario y lo muestra en palabras en la vista de pared Intrusión y en la ficha de cada cámara: `línea L–D 22:00–06:00`, con punto verde (armada ahora) o ámbar (desarmada ahora). Se relee cada 5 minutos.
- En esta versión el horario se cambia en la web de la cámara (o del NVR). El **Mapa** tiene otro horario, propio de cada línea dibujada: solo calla el mapa, no la cámara, y la detección queda igual en el historial.

**Impacto:** el perímetro avisa de noche, que es cuando importa, y lo podés demostrar en pantalla.

**Quién lo dice:** 4 de 4 fuentes coinciden en que sin horario de armado la regla no avisa; Hikvision y un foro de instaladores separan horario de armado y de grabación (2 de 4).

**Laboratorio** · Admin · 15 min
1. **Monitores → Intrusión → Abrir**. En cada canal leé la línea de armado: punto verde o ámbar, y el texto de línea y zona. "armado: sin dato" quiere decir que la cámara no contestó la lectura.
2. Tocá un canal: en la **Ficha de la cámara**, el bloque **Armado** repite el horario regla por regla. Anotá tres cámaras.
3. En la web de "Perímetro Sur 07" (192.0.2.22) armá la línea de noche:
```text
Configuración > Evento > Evento inteligente > Detección de cruce de línea
> Programación de armado (Arming Schedule)
Lunes a domingo: 22:00 a 24:00 y 00:00 a 06:00   (copiar a todos los días)
Guardar
```
4. Volvé a la vista de pared. Hasta 5 minutos después debería decir `línea L–D 22:00–06:00`. Si es de día, el punto queda ámbar: desarmada ahora.
5. Si la cámara tiene zona, repetí con **Detección de intrusión**: cada regla tiene su horario.
6. Para el mapa: **Mapa → Editar mapa → Cruces de línea**, en la cámara tocá **Horario** y después **Quitar** ("Sin horario = siempre armada"), así el mapa no calla lo que la cámara avisa.

⚠️ Antes de entregar, verificá el armado de noche en cada cámara: un hueco en el horario es un perímetro ciego.

**Regla para quedarse**
El horario de armado se mira en cada cámara, de noche, antes de entregar.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Por qué importa el horario de armado (Hikvision): https://supportusa.hikvision.com/support/solutions/articles/17000129443-why-is-the-arming-schedule-important-
- Horario de armado frente a horario de grabación (Hikvision): https://supportusa.hikvision.com/support/solutions/articles/17000133598-what-is-the-difference-between-arming-schedule-recording-schedule-
- El caso de un instalador que mezclaba los dos horarios: https://www.ipcamtalk.com/threads/difference-between-arming-schedule-and-recording-schedule.7096
