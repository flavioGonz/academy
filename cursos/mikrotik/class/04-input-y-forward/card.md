# Lección 4. Input y forward

**Escuchá:** input-y-forward.mp3 (2 min)

**La idea, en tres líneas**
- `input` es lo que va al router (cualquier IP del router, también la de LAN); `forward` es lo que pasa a través de él.
- Las reglas se evalúan de arriba abajo y la primera que coincide manda: lo que permitís va arriba del drop, con `place-before`.
- Agrupá direcciones en address-lists e interfaces en interface lists, y que las reglas apunten a las listas.

**Impacto:** resolvés en minutos el "puse la regla y no anda", y las reglas sobreviven a un cambio de IP.

**Quién lo dice:** 3 de 4 fuentes coinciden en el reparto input/forward y en la importancia del orden; en el foro conviven dos escuelas (dejar la configuración por defecto y abrir agujeros, o reescribir con un drop final explícito).

**Laboratorio** · Foco · 15 min
En un router de laboratorio con configuración por defecto de RouterOS 7:
1. Mirá el firewall por defecto y ubicá la regla que protege al router:
```routeros
/ip/firewall/filter/print
```
Buscá `defconf: drop all not coming from LAN` (input) y `defconf: drop all from WAN not DSTNATed` (forward).
2. Creá la lista de administradores (direcciones de ejemplo):
```routeros
/ip/firewall/address-list/add list=admins address=192.168.88.10 comment="notebook lab"
/ip/firewall/address-list/add list=admins address=203.0.113.25 comment="oficina ejemplo"
```
3. Agregá la regla arriba del drop, no al final:
```routeros
/ip/firewall/filter/add chain=input protocol=tcp dst-port=8291 src-address-list=admins action=accept comment="winbox solo admins" place-before=[find comment="defconf: drop all not coming from LAN"]
```
4. Conectate por WinBox y mirá el contador de la regla:
```routeros
/ip/firewall/filter/print stats where comment="winbox solo admins"
```
5. Probá el error a propósito: agregá una copia sin `place-before`, mirá que queda al final y que su contador no sube. Después borrala.

⚠️ Un error de orden en input puede cortarte WinBox: hacelo en Safe Mode (lección 1).

**Regla para quedarse**
Antes de agregar una regla, sé en qué cadena va y qué tiene arriba.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Qué hace cada regla del firewall por defecto, explicado en el foro: https://forum.mikrotik.com/t/trying-to-understand-defconf-firewall/267442
- Firewall base de MikroTik con address-lists: https://help.mikrotik.com/docs/spaces/ROS/pages/328513/Building+Advanced+Firewall
- Por qué una regla agregada al final no coincide: https://manual.mikrotik.com/docs/7.25/getting-started/securing-your-router
