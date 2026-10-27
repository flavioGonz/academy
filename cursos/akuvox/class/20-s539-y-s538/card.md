# Lección 20. S539 y S538

**Escuchá:** s539-y-s538.mp3 (2 min)

**La idea, en tres líneas**
- Android de la serie S para el acceso principal: S539 de 10", IP66, Wiegand y apps de terceros según la guía de selección; S538 "Tri-Vision". Ambos con PIN, tarjeta 13,56 MHz y 125 kHz, rostro, Bluetooth y QR, y relé de 30 V 3 A.
- Alimentación: S539 PoE+ 802.3at o 12 V 3 A / 24 V 1,5 A; S538 PoE 802.3at o 24 V 2 A. La versión para frío del S538 va solo con fuente de 24 V 2 A o más.
- 12 V para cerradura: S539 hasta 1 A por el relé, solo con fuente de 24 V 2,5 A o más; S538 con borne propio de 500 mA.

**Impacto:** la fuente y el puerto PoE se eligen antes de ir a la obra y la cerradura no deja al portero sin energía.

**Quién lo dice:** 5 de 10 fuentes del catálogo coinciden en verificar la alimentación por modelo (tablas de alimentación y 12 V, guía de selección, fichas); ninguna discrepa. No hay ficha propia leída del S539 ni del S538.

**Laboratorio** · Campo · 15 min
1. Sacá la IP: en la pantalla, `9999` + Dial, `3888` + OK, `System Info` (en el S539, además `Network`).
2. Web: `Status > Basic > Product Information`. El firmware empieza con `539.` o `538.`; anotá el tercer bloque (10 o más es alta seguridad).
3. Revisá el puerto del switch:
```text
Equipo  PoE requerido        Fuente alternativa
S539    802.3at (PoE+)       12 V 3 A  o  24 V 1,5 A
S538    802.3at              24 V 2 A (versión para frío: solo fuente, 24 V 2 A o más)
```
4. Si la cerradura se alimenta desde el portero: S539 solo con fuente de 24 V 2,5 A o más; S538 por su borne de 12 V, 500 mA máximo.
5. Anotá en la planilla de la lección 19.
⚠️ Una cerradura que pide más de lo que da la salida de 12 V va con fuente propia.

**Regla para quedarse**
En la serie S Android, la fuente se decide antes que el soporte.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Guía de selección de porteros: https://www.akuvox.com/productSelectionGuide?cid=3
- Alimentación y PoE por modelo: https://knowledge.akuvox.com/docs/power-supply-for-intercom-devices
- Salida de 12 V por modelo: https://knowledge.akuvox.com/docs/devices-supporting-12v-power-output
