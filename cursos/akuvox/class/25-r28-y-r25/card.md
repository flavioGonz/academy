# Lección 25. R28 y R25

**Escuchá:** r28-y-r25.mp3 (2 min)

**La idea, en tres líneas**
- R28: 4,3" no táctil, aluminio, Linux, IP65, Wiegand (guía de selección); versiones estándar y con lazo de inducción. PIN y tarjetas 13,56 y 125 kHz; relé 30 V 3 A; borne propio de 12 V 400 mA con PoE o fuente. Dos versiones de hardware.
- R25A (un botón) y R25K: Linux, IP65, Wiegand; la tabla de métodos marca la serie R25 sin PIN, solo tarjetas. Relé 30 V 2 A.
- Alimentación: R28A y R25 PoE 802.3af o 12 V 1 A. La salida de 12 V del R25 (400 mA por el relé) con PoE pide firmware 25.30.10.11 o más y depende del volumen del equipo.

**Impacto:** no se promete PIN en un R25 y se elige el R28 cuando hace falta 12 V propios sin tocar el relé.

**Quién lo dice:** 5 de 10 fuentes del catálogo coinciden en revisar alimentación por modelo; la tabla de 12 V es la única que explica la relación con el volumen. Sin ficha propia leída de R28 ni R25.

**Laboratorio** · Rápido · 10 min
1. IP: R28 con `*2396#` y luego `1`; R25A manteniendo el botón 5 s; R25K con `*3258*`.
2. Firmware en la web: `28.` (o `228.` en la versión 2 del R28) y `25.`.
3. R25 con PoE: conectá una carga de banco a la salida de 12 V por el relé, abrí desde la web y medí con volumen bajo y alto:
```text
Volumen bajo : ____ V durante la apertura
Volumen alto : ____ V durante la apertura
```
4. Si la caída afecta a la cerradura, fuente de 12 V 1 A para el portero o fuente propia para la cerradura.
⚠️ En obra, la cerradura no debería depender del volumen del portero: con PoE en un R25, fuente aparte para la cerradura.

**Regla para quedarse**
Del R25 no prometo PIN y de su salida de 12 V con PoE no dependo.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Salida de 12 V y la relación con el volumen: https://knowledge.akuvox.com/docs/devices-supporting-12v-power-output
- Métodos de acceso por modelo: https://knowledge.akuvox.com/docs/access-methods-supported-by-door-phones
- Guía de selección de porteros: https://www.akuvox.com/productSelectionGuide?cid=3
