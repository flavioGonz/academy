# Lección 21. S535 y S532

**Escuchá:** s535-y-s532.mp3 (2 min)

**La idea, en tres líneas**
- S535: Linux, 5", aluminio, IP66 y Wiegand según la guía de selección; se arma con módulos de huella, LTE, lector QR o lazo de inducción. PIN, tarjetas 13,56 y 125 kHz, rostro, Bluetooth, QR y huella opcional; relé 30 V 2 A.
- S532: 2,8", versiones estándar, IP y lazo de inducción; PIN, tarjetas y Bluetooth, sin rostro ni QR; relé 30 V 3 A. No figura en la guía de selección.
- Alimentación: S535 PoE+ o 12 V hasta 4 A (12 V de salida hasta 1 A con PoE+ o fuente de 12 V 2 A); S532 PoE+ o 12 V 2 A, pero su salida de 12 V (500 mA) pide fuente de 12 V 2,5 A.

**Impacto:** el S535 se cotiza completo con sus módulos, y el S532 no queda sin energía para la cerradura por haberlo dejado solo con PoE.

**Quién lo dice:** 5 de 10 fuentes del catálogo coinciden en verificar la alimentación por modelo; la tabla de métodos de acceso es la única que fija las credenciales. Sin ficha propia leída de ninguno de los dos.

**Laboratorio** · Admin · 10 min
1. Armá el pedido de un S535 para un edificio con huella y LTE de respaldo:
```text
1 x S535 (frente)
1 x módulo de huella
1 x módulo LTE
Alimentación: PoE+ 802.3at en el switch, o fuente 12 V (hasta 4 A)
Cerradura desde el portero: hasta 12 V / 1 A por el relé
```
2. Para un S532 con cerradura alimentada desde el portero:
```text
Fuente 12 V 2,5 A o más (con PoE solo no hay salida de 12 V)
Cerradura <= 500 mA
```
3. Anotá cómo se entra a cada uno: S535 con `9999` y `3888`; S532 con `*2396#` y luego `1`.
⚠️ Si la cerradura pide más de 500 mA en el S532 o de 1 A en el S535, va con fuente propia.

**Regla para quedarse**
El S535 se cotiza por módulos y el S532 con cerradura lleva fuente.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Menú de productos con los módulos del S535: https://www.akuvox.com/products
- Métodos de acceso por modelo: https://knowledge.akuvox.com/docs/access-methods-supported-by-door-phones
- Salida de 12 V por modelo: https://knowledge.akuvox.com/docs/devices-supporting-12v-power-output
