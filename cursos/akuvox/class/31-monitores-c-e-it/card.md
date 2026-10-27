# Lección 31. Monitores C e IT

**Escuchá:** monitores-c-e-it.mp3 (2 min)

**La idea, en tres líneas**
- C313 7" Linux, C316 7" Android, C319 10" Android, IT88 10" Android en aluminio (guía de selección, todos con PoE). C313 y C316: 1 RS485, 1 relé, 1 timbre; C319S e IT88S: 1 RS485, 2 relés, 1 timbre.
- Carga del relé: IT88 y C313 30 V 2 A; C319 24 V 1 A; el C316 no figura en la tabla de carga, así que no se afirma.
- IP: C313 en `More > Status > Network`; C316, C319 e IT88 en `Settings > System Info > Network`. Relés externos por RS485 desde un firmware mínimo (C316 316.30.13.102, C319 119.30.12.902, IT88 88.30.12.904).

**Impacto:** cada relé del monitor maneja una carga que puede aguantar, y el C319 no termina con un portón de 30 V colgado.

**Quién lo dice:** 4 de 7 fuentes coinciden en elegir el monitor por sistema, relés e interfaces; ninguna discrepa, pero la tabla de carga no incluye al C316.

**Laboratorio** · Foco · 15 min
1. IP del monitor por su ruta de menú; web con tu clave.
2. Firmware: `113.`, `213.` o `313.` (C313 según versión), `316.`, `119.` (C319) u `88.` (IT88).
3. En un C319 o IT88, ubicá los dos relés y probalos con una carga de banco:
```text
C319  relé 1 y 2  -> máximo 24 V 1 A
IT88  relé 1 y 2  -> máximo 30 V 2 A (valor de la tabla)
C316  relé        -> sin dato en la tabla: confirmar antes de cargar
```
4. Si vas a sumar MK485 o RSAC-C1-R8, compará el firmware con el mínimo del modelo.
5. Poné a cada relé el nombre de lo que maneja.
⚠️ La tabla da un solo valor de carga por modelo; si un relé maneja algo crítico, confirmalo con el distribuidor.

**Regla para quedarse**
En los monitores C, el número de relés y su carga se leen antes de prometer qué abren.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Interfaces por modelo: https://knowledge.akuvox.com/docs/interface-differences-of-akuvox-indoor-monitors
- Carga del relé por modelo: https://knowledge.akuvox.com/docs/relay-output-of-indoor-monitors
- Firmware mínimo para relés externos: https://knowledge.akuvox.com/docs/configure-external-relays-connected-to-indoor-monitors
