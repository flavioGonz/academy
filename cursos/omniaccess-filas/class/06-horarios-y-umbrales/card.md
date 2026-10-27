# Lección 6. Horarios y umbrales

**Escuchá:** horarios-y-umbrales.mp3 (2 min)

**La idea, en tres líneas**
- Horarios de Filas pone los contadores en 0 a la hora de apertura (Reseteo automático); lo dispara una tarea programada que llama cada minuto, y "Reset ahora" lo hace a mano.
- Un umbral (Filas → Nuevo Umbral) avisa cuando el aforo llega o supera N personas y no repite hasta que pasa el cooldown. Estados: OK, Alto desde el 70 %, Lleno desde el 100 %.
- Si la fila sigue sobre el umbral 5 minutos, OmniAccess escala con un aviso por Telegram para el supervisor.

**Impacto:** cada día arranca en cero y las alertas suenan cuando hay cola, no cada vez que el número roza el límite.

**Quién lo dice:** 2 de 2 fuentes recomiendan resetear los acumulados (Keenfinity para Bosch, Axis con su reset a medianoche). Los umbrales, estados y el escalamiento salen del código de OmniAccess.

**Laboratorio** · Admin · 15 min
Instalación de prueba con la fila "Fila Caja 1" funcionando.
1. Abrí Horarios de Filas → "Nuevo horario". Cargá:
```text
Nombre:               Apertura Caja 1
Dispositivo:          Fila Caja 1   (o "Todas las filas")
Días de la semana:    L a S
Apertura / Cierre:    08:00 / 20:00
Reseteo automático:   activado ("Pone los contadores en 0 al abrir")
Horario activo:       activado
```
2. En el servidor, confirmá que existe la tarea que dispara el reseteo:
```bash
crontab -l | grep schedule/tick
# * * * * * wget -qO- 127.0.0.1:10001/api/queue/schedule/tick >/dev/null 2>&1
```
3. Tocá "Reset ahora" y mirá en Filas que Aforo, Entrada y Salida queden en 0.
4. En Filas tocá "Nuevo Umbral". En "Nueva alerta de aforo" cargá: Nombre "Aforo Caja 1", Dispositivo "Fila Caja 1", Canal "Aforo", Umbral 2, Cooldown 30. Tocá "Crear alerta".
5. Meté tres personas en la zona. Mirá el borde rojo, el número en rojo y el aviso con foto arriba a la derecha.
6. Dejalos 5 minutos: llega el aviso de escalamiento por Telegram (si el canal está configurado, lección 7).
7. Al terminar, subí el umbral al valor real que pidió el cliente y dejá una sola alerta por fila.

⚠️ El reseteo pone en 0 lo que muestra OmniAccess y los acumulados de entradas y salidas. El aforo vuelve a tomar el valor real con el próximo evento de la cámara.

**Regla para quedarse**
Una alerta por fila, con el umbral que firmó el cliente, y un horario que la pone en cero cada mañana.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Cuándo y cómo se resetean los contadores de Bosch (Keenfinity): https://knowledge.keenfinity-group.com/video-systems/article/how-to-set-up-count-with-iva-pro-fw-9-40-and-get-the-data-from-the-camera
- Acumulados que no se resetean solos (Axis): https://developer.axis.com/analytics/axis-object-analytics-counting-data
