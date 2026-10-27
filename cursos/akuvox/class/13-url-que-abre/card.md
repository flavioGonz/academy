# Lección 13. La URL que abre

**Escuchá:** url-que-abre.mp3 (2 min)

**La idea, en tres líneas**
- `Open Relay via HTTP` (R29: `Intercom > Relay`; E18: `Access Control > Relay`) se habilita con usuario y clave propios y `Session Check` apagado.
- Tercer número del firmware 10 o más es la rama de alta seguridad: con el modo encendido solo vale `/fcgi/OpenDoor`; apagado, también la vieja `/fcgi/do`.
- `DoorNum=1` dispara el relé A y `DoorNum=2` el relé B.

**Impacto:** el "no abre por HTTP" después de una actualización se resuelve en dos minutos, mirando el firmware en vez de probar URLs al azar.

**Quién lo dice:** 2 de 3 fuentes coinciden (las dos guías de Akuvox, que recomiendan el formato nuevo); el foro LogicMachine discrepa: apaga la alta seguridad para seguir con la URL vieja.

**Laboratorio** · Rápido · 10 min
1. `Status > Basic > Product Information`: anotá el firmware. Si el tercer bloque es 10 o más (por ejemplo `29.30.10.x`), el equipo está en la rama de alta seguridad.
2. Mirá el interruptor: `Security > Basic > High Security Mode` (en el E18, `System > Security > High Security Mode`, encendido de fábrica).
3. Habilitá `Open Relay via HTTP` con usuario `abre-lab` y clave `Ejemplo-Http-2026`; `Session Check` apagado; `Submit`.
4. Desde la PC de laboratorio:
```bash
PORTERO=192.168.88.21
# formato nuevo (usuario:clave@IP); -u manda lo mismo y curl sin esquema usa HTTP
curl -s -u 'abre-lab:Ejemplo-Http-2026' "$PORTERO/fcgi/OpenDoor?action=OpenDoor&DoorNum=1"
# formato viejo: solo firmware sin alta seguridad o con el modo apagado
curl -s "$PORTERO/fcgi/do?action=OpenDoor&UserName=abre-lab&Password=Ejemplo-Http-2026&DoorNum=1"
```
5. Anotá en la ficha qué formato abrió el relé y con qué firmware.
⚠️ Probalo con una lámpara o una cerradura de banco, no con la puerta de un cliente en uso.

**Regla para quedarse**
Primero leo el firmware y el modo de alta seguridad; después elijo la URL.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Los tres formatos de URL y las teclas del monitor: https://knowledge.akuvox.com/docs/open-door-via-http-command
- Formato recomendado y acciones extra en E18 y R20V5: https://knowledge.akuvox.com/docs/trigger-door-actions-via-http-api-e18
- El integrador que apaga la alta seguridad: https://forum.logicmachine.net/showthread.php?tid=6156
