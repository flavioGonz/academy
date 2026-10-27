# Lección 26. Los R20

**Escuchá:** los-r20.mp3 (2 min)

**La idea, en tres líneas**
- R20A (un botón, tarjetas 13,56 y 125 kHz, QR desde 320.30.12.19), R20K (teclado: PIN y tarjetas), R20K-L (LTE, PIN y 13,56 MHz) y R20B (botones, tarjetas): Linux, aluminio, sin pantalla, IP65, Wiegand. PoE 802.3af o 12 V 1 A; relé 30 V 2 A.
- Tres versiones de hardware: R20K V3.0, R20A V5.0 y R20B V2.0 dan 12 V 500 mA por el relé (con PoE desde 320.30.11.42 y afectada por el volumen); las versiones viejas no tienen salida.
- La etiqueta engaña: R20A V3.0 es hardware 2 y V5.0 es hardware 3. En la web, `20.`, `220.` o `320.` al comienzo del hardware. MD06 y MD12 son módulos de nombres, sin ficha leída.

**Impacto:** la cerradura y el firmware se eligen por la versión de hardware real, no por la etiqueta.

**Quién lo dice:** 2 de 10 fuentes coinciden en sacar la IP con el método de la familia y leer el firmware (guías de Akuvox de acceso web y de actualización); la tabla de 12 V es la única que detalla la salida por versión.

**Laboratorio** · Rápido · 10 min
1. IP: R20A manteniendo el botón 5 s; R20K o R25K con `*3258*`; R20B manteniendo el primer botón 5 s.
2. Web, `Status > Basic > Product Information`, `Hardware Version`:
```text
20.x   -> hardware 1
220.x  -> hardware 2   (un R20A con etiqueta V3.0 cae acá)
320.x  -> hardware 3   (R20A V5.0, R20K V3.0)
```
3. Decidí la cerradura:
```text
hardware 3 (o R20B V2.0) + fuente 12 V 1,2 A o más     -> 12 V 500 mA por el relé
hardware 3 + PoE + firmware 320.30.11.42 o más          -> 12 V 500 mA, afectada por el volumen
hardware viejo                                          -> fuente propia para la cerradura
```
4. Anotá hardware, firmware y decisión en la planilla.
⚠️ Cada versión de hardware lleva su propio archivo de firmware: se baja el de la versión real, no el de la etiqueta.

**Regla para quedarse**
En un R20, primero la versión de hardware real; después la cerradura y el firmware.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Versiones de hardware y códigos de firmware: https://knowledge.akuvox.com/docs/upgrade-devices
- Salida de 12 V por versión: https://knowledge.akuvox.com/docs/devices-supporting-12v-power-output
- Métodos de acceso por modelo: https://knowledge.akuvox.com/docs/access-methods-supported-by-door-phones
