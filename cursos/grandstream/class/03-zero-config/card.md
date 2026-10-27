# Lección 3. Zero Config

**Escuchá:** zero-config.mp3 (2 min)

**La idea, en tres líneas**
- La UCM descubre los teléfonos por SIP multicast al arrancar, o por DHCP opción 66 si está en modo Route, y les sirve la configuración por TFTP, HTTP o HTTPS.
- Plantillas por prioridad: Global Policy < Global Template < Model Template.
- Lo que se configuró a mano en la web del teléfono no lo pisa ninguna plantilla.

**Impacto:** un edificio de decenas de teléfonos queda configurado igual, en minutos, y se reprovisiona desde la central.

**Quién lo dice:** 2 de 2 fuentes oficiales coinciden (guía de Zero Config y manual del UCM630x); sin discrepancias. Para varios sitios, Grandstream propone GDMS en la nube.

**Laboratorio** · Foco · 20 min
1. Verificá que Zero Config esté activo.
```text
Device Management > Zero Config > Zero Config Settings > Enable Zero Config: Sí
```
2. Conectá un GRP26xx de laboratorio reseteado de fábrica a la misma red y esperá que aparezca. Si no aparece, escaneá:
```text
Device Management > Zero Config > Auto Discover
Scan Method: SIP Message
Scan IP: 192.168.88.255
```
3. Si el modelo no figura en las plantillas, bajalo:
```text
Device Management > Zero Config > Model Update > (modelo) > Download
```
4. En Global Policy, poné idioma español y zona horaria de Montevideo.
5. Editá el teléfono descubierto, asignale la extensión 1001 en la cuenta 1, guardá y tocá el botón de sincronizar.
6. Comprobá en el teléfono que la cuenta registró y que la hora es la correcta.
⚠️ Activar Auto Assign Extension en una red con teléfonos de otro cliente o de otra central puede tomar equipos ajenos: usalo solo en una red de voz separada.

**Regla para quedarse**
El teléfono que se aprovisiona desde la central no se toca a mano; si quedó distinto, reset de fábrica y que lo tome Zero Config.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Guía oficial de Zero Config: https://documentation.grandstream.com/knowledge-base/zero-config-guide/
- GDMS, gestión en la nube según Grandstream: https://blog.grandstream.com/company/news/blog/gdms-is-a-game-changer
