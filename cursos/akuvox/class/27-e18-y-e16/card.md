# Lección 27. E18 y E16

**Escuchá:** e18-y-e16.mp3 (2 min)

**La idea, en tres líneas**
- Rostro en plástico, Linux, IP65 y Wiegand (guía de selección). E18 (Akuvox lo presenta con 7", estándar o LTE): PIN, tarjetas 13,56 y 125 kHz, rostro, Bluetooth, QR. E16 (5" táctil): PIN, 13,56 MHz, rostro, Bluetooth, QR; E16P con palma.
- PoE 802.3af; fuente 12 V 1 A (E16C), 1,5 A (E18C) o 2,5 A (E18 con LTE). Relé 30 V 2 A y sin salida de 12 V: la cerradura va con fuente propia.
- PIN de sistema: `admin` hasta 216.30.10.121 (E16) y 18.30.10.211 (E18), `Admin321` después. E16 con tres hardware (`116.`, `216.`, `416.`); E18 con acciones HTTP extra desde 18.30.11.27.

**Impacto:** no se pierde tiempo con un PIN de sistema equivocado ni se cablea una cerradura esperando 12 V que el equipo no da.

**Quién lo dice:** 2 de 10 fuentes coinciden en sacar la IP con el método de la familia y leer el firmware; las tablas de alimentación, 12 V y métodos de acceso fijan el resto. Sin ficha propia leída del E18 ni del E16.

**Laboratorio** · Foco · 15 min
1. Mantené la pantalla 5 s e ingresá el PIN de sistema según firmware (`admin` o `Admin321`); anotá la IP.
2. Web, `Status > Basic > Product Information`: firmware `18.`, `116.`, `216.` o `416.`.
3. Elegí la fuente:
```text
E16C           PoE 802.3af o 12 V 1 A
E18C           PoE 802.3af o 12 V 1,5 A
E18 con LTE    PoE 802.3af o 12 V 2,5 A
Cerradura      fuente propia (sin salida de 12 V en E16C ni E18C)
```
4. En un E18 con 18.30.11.27 o más, probá el estado de la puerta:
```bash
curl -s -u 'abre-lab:Ejemplo-Http-2026' "192.168.88.23/fcgi/OpenDoor?action=DoorStatus&DoorNum=1"
```
5. Cambiá el PIN de sistema por uno propio y anotalo en la ficha.
⚠️ El PIN de sistema da acceso al menú del equipo en la calle: no se deja el de fábrica.

**Regla para quedarse**
En la serie E de rostro, la cerradura siempre lleva fuente propia y el PIN de sistema se cambia el primer día.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- PIN de sistema y acceso al menú de E16 y E18: https://knowledge.akuvox.com/docs/before-entering-device-web-interface
- Acciones HTTP del E18: https://knowledge.akuvox.com/docs/trigger-door-actions-via-http-api-e18
- Métodos de acceso (E16P con palma): https://knowledge.akuvox.com/docs/access-methods-supported-by-door-phones
