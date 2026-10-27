# Lección 24. R29

**Escuchá:** r29.mp3 (2 min)

**La idea, en tres líneas**
- Android de 7" táctil, aluminio, superficie o embutido, IP65 e IK06 (ficha). Versiones: R29S una cámara; R29C doble cámara y Bluetooth; R29C-L con LTE; R29C-T con huella. Tarjetas 13,56 y 125 kHz en todas.
- Credenciales: R29C PIN, tarjeta, rostro, Bluetooth y QR; R29CT cambia QR por huella; R29S sin Bluetooth. Relé 30 V 3 A; la V1.1 da 12 V 500 mA por el relé.
- Alimentación (tabla de Akuvox): R29 PoE 802.3at o 12 V 2,5 A; R29CT 802.3af; R29S 802.3at sin fuente listada; el R29C-L con LTE no acepta PoE (12 V 1,5 A). Lee patentes Hikvision y Dahua desde 29.30.10.745.

**Impacto:** el R29 llega a obra con la versión, la fuente y la cubierta correctas, sin vueltas al depósito.

**Quién lo dice:** 4 de 10 fuentes coinciden en elegir por credenciales (ficha del R29, tabla de métodos, guía de selección, ficha del X915); la tabla de alimentación es la única que aclara el R29C-L sin PoE.

**Laboratorio** · Foco · 15 min
1. Identificá la versión por la etiqueta: R29S, R29C, R29C-L o R29C-T.
2. IP: `9999` + Dial, `3888` + OK, `System Info`. Web: firmware `29.x.y.z` en `Status > Basic > Product Information`.
3. Completá la lista de obra:
```text
Versión   Cámaras  Extra       Alimentación                Accesorios
R29S      1        -           PoE 802.3at (la tabla no lista fuente)  cubierta de lluvia + soporte
R29C      2        Bluetooth   PoE 802.3at o 12 V 2,5 A (fila "R29")   cubierta de lluvia + soporte
R29C-L    2        LTE         SOLO fuente 12 V 1,5 A      soporte de pared R29C-L
R29C-T    2        Huella, BT  PoE 802.3af o 12 V 1,5 A    cubierta de lluvia + soporte
```
4. Elegí cubierta de lluvia y soporte según montaje (pared o embutido) y color (negro o plata).
⚠️ IK06 es el grado que publica la ficha: en lugares con riesgo de golpe, comparalo con lo que pide el pliego.

**Regla para quedarse**
Antes de cotizar un R29, la versión exacta: de ella dependen la fuente y las credenciales.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Ficha del R29 con versiones y accesorios: https://www.akuvox.com/productsDisp?pid=17
- Alimentación por modelo (R29C-L sin PoE): https://knowledge.akuvox.com/docs/power-supply-for-intercom-devices
- Métodos de acceso por versión: https://knowledge.akuvox.com/docs/access-methods-supported-by-door-phones
