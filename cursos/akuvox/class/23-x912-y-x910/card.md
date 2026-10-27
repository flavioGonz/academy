# Lección 23. X912 y X910

**Escuchá:** x912-y-x910.mp3 (2 min)

**La idea, en tres líneas**
- X912 "antivandálico": acero, táctil, Linux, IP65 y Wiegand según la guía; versiones estándar y con teclado físico. PIN, tarjetas 13,56 y 125 kHz, rostro, Bluetooth y QR; relé 30 V 3 A; 12 V hasta 1 A por el relé con PoE+ o fuente de 12 V 2,5 A.
- X910: un botón con detección de paquetes, sin pantalla, Linux, IP66. Sin PIN ni rostro; tarjeta 13,56 MHz, Bluetooth y QR; relé 30 V 2 A; PoE 802.3af o 12 a 24 V, y su salida de 12 V (600 mA) pide PoE+ o fuente de 12 V 2 A.
- Acceso: X912 con el ícono de llave, `2396` y Dial; X910 manteniendo el botón 5 s, anuncia la IP.

**Impacto:** el técnico llega con la alimentación justa para que la cerradura funcione desde el portero.

**Quién lo dice:** 5 de 10 fuentes del catálogo coinciden en revisar la alimentación por modelo; la tabla de métodos de acceso fija las credenciales. Sin ficha propia leída de X912 ni X910.

**Laboratorio** · Campo · 10 min
1. X912: ícono de llave o teclado, `2396`, Dial; anotá la IP. X910: mantené el botón de llamada 5 s y anotá la IP que dice.
2. En la web de cada uno, `Status > Basic > Product Information`: el firmware empieza con `912.` o `2910.`.
3. Alimentá cada uno según la salida de 12 V que vas a usar:
```text
X912  12 V / 1 A por el relé   -> PoE+ 802.3at o fuente 12 V 2,5 A
X910  12 V / 600 mA por el relé -> PoE+ 802.3at o fuente 12 V 2 A (con PoE af no alcanza)
```
4. Conectá una cerradura de banco, abrí desde la web y medí la tensión con el tester durante la apertura.
⚠️ Medí con la carga conectada: en vacío la salida puede mostrar 12 V y caerse al abrir.

**Regla para quedarse**
La salida de 12 V se confirma con la cerradura conectada y la alimentación que pide la tabla.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Salida de 12 V por modelo: https://knowledge.akuvox.com/docs/devices-supporting-12v-power-output
- Cómo sacar la IP de cada modelo: https://knowledge.akuvox.com/docs/before-entering-device-web-interface
- Guía de selección de porteros: https://www.akuvox.com/productSelectionGuide?cid=3
