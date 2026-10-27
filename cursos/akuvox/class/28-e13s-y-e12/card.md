# Lección 28. E13S y E12

**Escuchá:** e13s-y-e12.mp3 (2 min)

**La idea, en tres líneas**
- Un botón y plástico: E13S (portero SIP de un botón) y E12 (compacto); Linux y Wiegand según la guía (IP65 en la fila del E13S; la fila del E12 viene desalineada). Tarjeta 13,56 MHz, sin PIN ni rostro; el E12 suma Bluetooth y la guía le marca Wi-Fi (la tabla de métodos separa E12S y E12W).
- E12: PoE 802.3af o 12 V 1 A, relé 30 V 2 A, sin salida de 12 V y sin RS485 (su conexión al SR01 es la que Akuvox no recomienda). Dos versiones de hardware: firmware `12.` o `312.`.
- E13: relé 30 V 2 A; la tabla de alimentación no lo lista, la guía solo marca PoE. IP por voz manteniendo el botón 5 s.

**Impacto:** se elige bien entre un E12 y un portero con RS485 cuando la cerradura tiene que quedar protegida.

**Quién lo dice:** 2 de 10 fuentes coinciden en sacar la IP por el método de la familia y leer el firmware; las tablas de métodos, alimentación y 12 V completan. Sin ficha propia leída de E13S ni E12.

**Laboratorio** · Rápido · 10 min
1. Mantené el botón de llamada 5 s y anotá la IP que anuncia.
2. Web: firmware `12.`, `312.` o `13.` en `Status > Basic > Product Information`; cambiá la clave web de fábrica.
3. Mirá la etiqueta: E12S o E12W.
4. Dejá escrito en la ficha:
```text
Equipo        : E12_ / E13S
Cerradura     : fuente propia (sin salida de 12 V)
SR01          : no recomendado en E12 (sin RS485)
Clave perdida : SmartPlus, PC Manager en la LAN o llave del equipo a soporte
```
⚠️ Si la cerradura tiene que resistir que rompan el portero, en vez de un E12 conviene un portero con RS485 y SR01.

**Regla para quedarse**
En los de un botón, la cerradura lleva fuente propia y la clave web se cambia el primer día.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Métodos de acceso por modelo: https://knowledge.akuvox.com/docs/access-methods-supported-by-door-phones
- SR01 y la excepción del E12: https://knowledge.akuvox.com/docs/how-to-configure-sr01-security-relay-on-akuvox-door-phones
- Recuperar la clave web en porteros de un botón: https://ticket.akuvox.com/support/solutions/articles/48001156051-how-to-reset-the-web-password-for-single-button-series-door-phone-
