# Lección 2. Adopción limpia

**Escuchá:** adopcion-limpia.mp3 (2 min)

**La idea, en tres líneas**
- Un equipo se adopta si está libre de otro controlador, tiene firmware compatible y llega al controlador (en L2: misma red, un solo DHCP).
- La falla más común, según LazyAdmin, es el desfase de firmware entre equipo y controlador.
- Para readoptar: borrar el equipo del controlador viejo, reset de fábrica, adoptar.

**Impacto:** la primera hora de obra deja de ser prueba y error.

**Quién lo dice:** 3 de 3 fuentes sobre adopción coinciden en el orden reset, red, firmware; nadie discrepa.

**Laboratorio** · Foco · 15 min
1. Reset de fábrica: con el AP encendido, botón de reset 10 segundos. Si ya entrás por SSH, el comando es `set-default`.
2. Conectá el AP al mismo switch y VLAN que el controlador. Verificá que haya un solo servidor DHCP en esa red.
3. Buscá la IP que tomó el AP (lista de leases del DHCP o WiFiman) y entrá por SSH con el usuario de fábrica de un equipo reseteado (ubnt / ubnt, según LazyAdmin):
```bash
ssh ubnt@192.168.88.20
info
```
Mirá Model, Version, IP Address y Status: ahí ves a qué URL de inform apunta y si está conectado.
4. En UniFi Network > Devices el AP aparece pendiente: Adopt (o Adopt and Upgrade si lo pide).
5. Si queda en "Pending Adoption (Update Required)" y no actualiza solo, bajá el firmware de tu modelo desde la página de descargas de Ubiquiti y, por SSH:
```bash
upgrade <url-del-firmware-para-tu-modelo>
```
6. Si "adopta y pasa a offline" con el controlador en una PC, revisá el firewall de esa PC.
⚠️ Un equipo que estaba adoptado en otro controlador se elimina primero ahí; si no, sigue buscando a su host viejo.

**Regla para quedarse**
Equipo que no adopta: reset, misma red que el controlador, firmware, y recién ahí sospecho del controlador.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Métodos para "Adoption Failed", con casos en comentarios: https://lazyadmin.nl/home-network/unifi-adoption-failed/
- Equipos en "Pending Adoption (Update Required)": https://www.hostifi.com/support/unifi-troubleshooting-unifi-cloud-adoption
