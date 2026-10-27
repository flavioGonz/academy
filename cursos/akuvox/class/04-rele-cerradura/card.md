# Lección 4. Relé y cerradura

**Escuchá:** rele-cerradura.mp3 (2 min)

**La idea, en tres líneas**
- Primero se decide qué hace la puerta sin energía: fail-safe (queda libre) o fail-secure (queda trabada).
- NC con COM abre al cortarse la energía; NO con COM queda trabada. La cerradura va con su propia fuente, y el electroimán con diodo.
- En Akuvox, `Access Control > Relay` fija el tiempo de apertura y `Access Control > Input` el botón de salida y las alarmas de puerta.

**Impacto:** salidas de emergencia que no quedan trabadas en un corte y alarmas de puerta forzada que el cliente no sabía que tenía.

**Quién lo dice:** 2 de 2 fuentes coinciden (guía del E16 de Akuvox y guía de dos puertas de Grandstream); evidencia escasa, el principio eléctrico es general.

**Laboratorio** · Campo · 20 min
1. En el banco: fuente de 12 V CC aparte, cerradura de prueba o lámpara de 12 V, pulsador NA.
2. Cableado en NO (fail-secure):
```text
+12 V fuente ──> COM del relé
NO del relé  ──> + cerradura
- cerradura  ──> -12 V fuente
(electroimán: diodo en antiparalelo sobre la bobina)
```
3. En la web: `Access Control > Relay`, tiempo de apertura 5 s. Abrí desde la web y cronometrá.
4. Pasá el cable de NO a NC y repetí: anotá en qué estado queda la carga en reposo.
5. Conectá el pulsador a la entrada y en `Access Control > Input` habilitala, elegí el nivel de disparo y el relé a ejecutar.
6. Activá la alarma de puerta abierta (Door Opened Timeout) y probala dejando la entrada accionada.
7. Cortá la fuente y anotá qué hace la cerradura en NO y en NC.
⚠️ En obra, el electroimán de una salida de emergencia se cablea para liberar sin energía y se respeta la normativa de evacuación del edificio.

**Regla para quedarse**
Antes de elegir el borne decido qué pasa cuando se corta la luz, y la cerradura nunca se alimenta del portero.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Fail-safe y fail-secure explicados con el cableado: https://documentation.grandstream.com/knowledge-base/gds3710-two-doors-control-configuration-guide/
- Botón de salida, entradas y alarmas de puerta en Akuvox: https://knowledge.akuvox.com/docs/door-unlock-configuration-8
