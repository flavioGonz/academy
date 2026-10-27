# Lección 33. Terminales A0x

**Escuchá:** terminales-a0x.mp3 (2 min)

**La idea, en tres líneas**
- Por credencial: A01S solo tarjeta (13,56 y 125 kHz); A02S suma PIN; A03S suma Bluetooth; A05C rostro, PIN, 13,56 MHz, Bluetooth y QR; A08S PIN, tarjetas, Bluetooth y QR.
- A08 (ficha): aluminio, teclado táctil, lector QR, 13,56 y 125 kHz más NFC, BLE 5.0, PoE o fuente, pared o embutido, IP65 e IK09; A08K con teclado y sin QR. Relé: A01 a A03 30 V 3 A; A05 y A08 30 V 2 A.
- 12 V por el relé: 500 mA en A01, A02, A03 y A08 (A08 con PoE desde hardware 108.2.0.0.0); el A05 no da. IP: A01, A02, A03 y A08 anuncian la IP al apretar Reset; el A05 se busca con IP Scanner.

**Impacto:** cada puerta interna lleva el terminal con la credencial justa y la cerradura alimentada como corresponde.

**Quién lo dice:** 8 de 11 fuentes de control de acceso coinciden en el reparto terminal, controladora, relé de borde y ascensor (menú, fichas de A08, EC33 y WR01, tablas de métodos, alimentación y 12 V, guía de ascensores); ninguna discrepa.

**Laboratorio** · Campo · 15 min
1. Probá en la mesa: apretá Reset en el A08 y anotá la IP que anuncia.
2. Web: firmware `108.` en `Status > Basic > Product Information`; cambiá la clave de fábrica.
3. Creá un usuario con PIN y tarjeta, relé A y horario (como en la lección 7).
4. Alimentación de la cerradura:
```text
A08 con fuente 12 V 1 A o más        -> 12 V 500 mA por el relé
A08 con PoE, hardware 108.2.0.0.0+   -> también 12 V 500 mA
A05                                  -> sin salida: fuente propia
```
5. Abrí con PIN y con tarjeta y verificá el registro de accesos.
⚠️ Probá el botón Reset en la mesa antes de usarlo en obra, y no lo mantengas apretado más de lo necesario.

**Regla para quedarse**
El terminal se elige por la credencial de la puerta y la cerradura por la salida de 12 V que tenga.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Ficha del A08 (IP65 e IK09): https://www.akuvox.com/productsDisp?pid=92
- Métodos de acceso de la serie A: https://knowledge.akuvox.com/docs/access-methods-supported-by-door-phones
- Cómo sacar la IP de los terminales: https://knowledge.akuvox.com/docs/before-entering-device-web-interface
