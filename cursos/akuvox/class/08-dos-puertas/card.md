# Lección 8. Dos puertas

**Escuchá:** dos-puertas.mp3 (2 min)

**La idea, en tres líneas**
- Un portero con dos relés: un código DTMF por relé y una tecla por puerta en el monitor; el mismo código en los dos abre ambas a la vez.
- Dos porteros distintos: el DTMF solo llega al que está en llamada, así que la otra puerta se abre por comando HTTP.
- El HTTP lleva usuario y clave propios, distintos del admin, y en lo posible solo se acepta desde IPs conocidas.

**Impacto:** el pedido "portón y hall desde el monitor" se resuelve el mismo día y sin dejar una puerta abrible por cualquiera.

**Quién lo dice:** 3 de 4 fuentes coinciden en un código por relé (Akuvox, Grandstream); el caso de FreePBX resuelve dos porteros por HTTP y su propio autor advierte el riesgo de seguridad.

**Laboratorio** · Foco · 20 min
1. Portero de dos relés, `Access Control > Relay`:
```text
Relay A (portón)  DTMF 731
Relay B (hall)    DTMF 732
```
2. Monitor, `Device > Relay > SoftKey In Talking Page`: tecla "Portón" = Remote Relay DTMF 731, tecla "Hall" = 732.
3. Llamá y probá cada tecla.
4. Comando HTTP en cualquier portero: `Access Control > Relay > Open Relay Via HTTP`, usuario `abre-lab`, clave `Ejemplo-Http-2026`.
5. Desde la PC de laboratorio:
```bash
PORTERO=192.168.88.21
# sin esquema, curl usa HTTP por defecto
curl -u 'abre-lab:Ejemplo-Http-2026' "$PORTERO/fcgi/OpenDoor?action=OpenDoor&DoorNum=1"
```
6. Si el equipo no está en la rama de alta seguridad y el formato nuevo no responde, revisá en su manual el formato de URL que corresponde a su firmware.
⚠️ Una URL de apertura con clave viaja en texto claro por HTTP: solo dentro de la red de porteros, nunca expuesta a internet.

**Regla para quedarse**
Cada puerta tiene su código y cada comando HTTP su propio usuario; ninguno es el admin.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Dos puertas y el mismo código DTMF, en Grandstream: https://documentation.grandstream.com/knowledge-base/gds3710-two-doors-control-configuration-guide/
- Dos porteros abiertos con un botón desde FreePBX: https://community.freepbx.org/t/how-can-i-manage-double-doorphone-doorlock/97459
- Elegir relé A, B o C y botón de apertura en el monitor: https://knowledge.akuvox.com/docs/how-to-open-the-door-via-dtmf-on-the-indoor-monitor
