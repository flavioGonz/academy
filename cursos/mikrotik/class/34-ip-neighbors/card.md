# Lección 34. Descubrir vecinos

**Escuchá:** ip-neighbors.mp3 (2 min)

**La idea, en tres líneas**
- `/ip/neighbor` muestra cada equipo que se anuncia por MNDP (MikroTik), CDP (Cisco) o LLDP (IEEE 802.1AB, multimarca): identidad, plataforma, versión, IP, MAC y el puerto físico donde lo ve, aunque esté en el bridge.
- Anunciarse es mostrarse: nombre, modelo, versión e IP salen por cada interfaz de `discover-interface-list`. La WAN y los puertos que van a redes ajenas quedan fuera.
- Sacar una interfaz de la lista corta las dos direcciones: ni descubre ni es descubierto por ahí. Si no hay equipos Cisco, `protocol=lldp,mndp` evita vecinos repetidos.

**Impacto:** encontrás en qué puerto está cada switch o equipo sin seguir cables, y el router deja de contarle su versión a quien mira del otro lado.

**Quién lo dice:** 5 de 6 fuentes coinciden en usarlo dentro de la LAN y apagarlo hacia afuera; un practicante del foro propone filtrar UDP 5678 (MNDP) en el firewall, y otro usuario no logra ocultar el router así: la documentación lo resuelve sacando la interfaz de la lista.

**Laboratorio** · Rápido · 15 min
Router de banco con RouterOS 7 y configuración por defecto; un switch administrable con LLDP (o un segundo MikroTik) en `ether3`; notebook de administración en `ether2`; otra notebook del lado de `ether1` (WAN).
1. Mirá los vecinos y en qué puerto aparece cada uno:
```routeros
/ip/neighbor/print
/ip/neighbor/print detail
```
La columna INTERFACE muestra el puerto real y el bridge (por ejemplo `ether3,bridge`). En `detail` mirá identity, platform, version, board, system-caps y discovered-by.
2. Solo lo que llega por LLDP (switches de otras marcas, teléfonos IP y, según modelo y firmware, cámaras o NVR):
```routeros
/ip/neighbor/lldp/print
```
3. Revisá por dónde y cómo se anuncia el router:
```routeros
/ip/neighbor/discovery-settings/print
```
Con configuración por defecto, `discover-interface-list=LAN`. Sin ella, el valor de fábrica es `static`, que incluye `ether1`. De fábrica también: `protocol=cdp,lldp,mndp`, `mode=tx-and-rx`, `discover-interval=30s`.
4. Anunciate solo donde hace falta: el puerto de la notebook (para verlo en Neighbors de WinBox) y el del switch del rack. Cámaras, WAN y redes ajenas, fuera:
```routeros
/interface/list/add name=descubrir comment="puertos con descubrimiento"
/interface/list/member/add list=descubrir interface=ether2
/interface/list/member/add list=descubrir interface=ether3
/ip/neighbor/discovery-settings/set discover-interface-list=descubrir protocol=lldp,mndp
```
Los puertos van sueltos, sin el `bridge`: si ponés el bridge en la lista, participan todos sus puertos.
5. Verificá desde afuera: en la notebook del lado de `ether1`, abrí WinBox y mirá la pestaña Neighbors. El router no aparece (si ya figuraba, la entrada vence sola en un par de minutos). En el router, `/ip/neighbor/print` sigue mostrando el switch de `ether3`.

⚠️ Si sacás de la lista el puerto donde está tu notebook, el router deja de aparecer en Neighbors de WinBox desde ahí. Hacé el cambio con la notebook en un puerto que quede en la lista.

**Regla para quedarse**
El router se presenta solo en los puertos que son míos; la WAN y las redes ajenas no lo ven.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Neighbor discovery en RouterOS 7.25, con LLDP-MED para teléfonos: https://manual.mikrotik.com/docs/7.25/system-information-and-utilities/neighbor-discovery
- El LLDP que salía por el puerto de internet: https://forum.mikrotik.com/t/controlling-where-lldp-is-sent/115188
- Qué viaja en una trama LLDP: https://en.wikipedia.org/wiki/Link_Layer_Discovery_Protocol
