# Lección 16. Relés de afuera

**Escuchá:** reles-de-afuera.mp3 (2 min)

**La idea, en tres líneas**
- Web Relay de terceros desde el portero (`Access Control > Web Relay`): solo Web Relay o ambos (manda el local), comando tipo `state.xml?relayState=2`, hasta 50 URLs completas con la IP en blanco; se dispara por DTMF, tarjeta o nube.
- SR01 adentro: por RS485 (`Security Relay B`) o por la salida de 12 V (`Security Relay A`); por HTTP, `DoorNum=SA` o `SB`. Si rompen el portero, la puerta no abre.
- En el monitor, MK485 o RSAC-C1-R8 (8 relés por RS485, `Device > External Relay`); WR01 como relé de borde con 2 relés, 2 entradas y API. `Trigger Delay` y `Hold Delay` fijan los tiempos.

**Impacto:** la cerradura principal deja de depender de un equipo que está en la calle, y cada carga se maneja desde el relé que le queda cerca.

**Quién lo dice:** 1 o 2 de 7 fuentes por tema: cada pieza tiene su artículo propio de Akuvox (Web Relay, SR01, relés externos) y la ficha del WR01; no se contradicen pero tampoco se repiten.

**Laboratorio** · Campo · 20 min
1. Cableá el SR01 al portero por RS485 y la cerradura de banco al SR01.
2. En el portero: `Access Control > Relay > Security Relay`, habilitá `Security Relay B` (su modo de servidor es RS485), `Trigger Delay 0`, `Hold Delay 5`.
3. `Device > RS485`: `Apply RS485 Setting To = Others`. `Submit`.
4. Desde la PC, con el usuario HTTP de la lección 13:
```bash
PORTERO=192.168.88.21
curl -s -u 'abre-lab:Ejemplo-Http-2026' "$PORTERO/fcgi/OpenDoor?action=OpenDoor&DoorNum=SB"
```
5. Sin SR01: misma prueba con `DoorNum=2` sobre el relé B y un portón o lámpara de banco.
6. Anotá en la ficha qué relé maneja cada carga y con qué tiempos.
⚠️ El E12 no tiene RS485 y su conexión especial con el SR01 es la que Akuvox no recomienda por seguridad: en ese caso, mejor otro portero.

**Regla para quedarse**
La cerradura importante se maneja desde adentro; el portero solo pide.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- SR01: cableado, modelos y firmware mínimo: https://knowledge.akuvox.com/docs/how-to-configure-sr01-security-relay-on-akuvox-door-phones
- Web Relay de terceros en el portero: https://knowledge.akuvox.com/docs/configure-web-relay-on-door-phone-web-interface
- Relés externos del monitor (MK485, RSAC-C1-R8): https://knowledge.akuvox.com/docs/configure-external-relays-connected-to-indoor-monitors
- Ficha del WR01: https://www.akuvox.com/productsDisp?pid=130
