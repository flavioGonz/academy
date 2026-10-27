# Lección 15. Botón del monitor

**Escuchá:** boton-del-monitor.mp3 (2 min)

**La idea, en tres líneas**
- En el monitor, `Remote Relay By HTTP or HTTPS` (C313: `Phone > Relay`) apunta al portero por IP o número SIP, con el formato de URL que corresponde a su alta seguridad y sus credenciales.
- Las teclas se crean en `Key Setting`: pantalla de llamada, de monitoreo y de vista previa, con tipo `Remote Relay By HTTP or HTTPS` y una etiqueta con el nombre de la puerta.
- Para un segundo portero, la tecla de monitoreo abre sin que nadie llame; monitoreo y vista previa piden el video del portero ya configurado.

**Impacto:** el pedido "portón y hall desde el monitor" se resuelve en el monitor, sin tocar la central ni depender de una llamada.

**Quién lo dice:** 1 de 7 fuentes sobre relés remotos lo documenta (la guía oficial de Akuvox, con R29 y C313); evidencia de una sola página, así que conviene probarlo en el modelo real.

**Laboratorio** · Foco · 15 min
1. En el segundo portero (portón): habilitá `Open Relay via HTTP` con usuario `monitor-porton` y clave `Ejemplo-Mon-2026` (lección 13).
2. En el monitor: `Phone > Relay > Remote Relay By HTTP or HTTPS` (en otros modelos, buscá `Relay` en `Device`):
```text
IP / número SIP : 192.168.88.22
Formato         : el nuevo (/fcgi/OpenDoor) si el portero tiene alta seguridad
Usuario / clave : monitor-porton / Ejemplo-Mon-2026
DoorNum         : 1 (relé A del portero del portón)
```
3. `+Add` para guardar.
4. `Phone > Relay > Key Setting > Softkey In Monitor Page`: habilitá una tecla, tipo `Remote Relay By HTTP or HTTPS`, etiqueta `Portón`.
5. Verificá que el monitor ya vea el video del portón; abrí monitoreo y tocá `Portón`.
6. Repetí en `Softkey in Talking Page` si querés la misma tecla durante una llamada.
⚠️ Una tecla que abre sin llamada es una llave más: el monitor va en un lugar de la casa que el cliente controla, no en un pasillo común.

**Regla para quedarse**
Cada tecla HTTP lleva el nombre de la puerta y un usuario propio del monitor.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Remote Relay By HTTP y las tres pantallas de teclas: https://knowledge.akuvox.com/docs/open-door-via-http-command
- El caso de dos porteros que no se resuelve por DTMF: https://community.freepbx.org/t/how-can-i-manage-double-doorphone-doorlock/97459
