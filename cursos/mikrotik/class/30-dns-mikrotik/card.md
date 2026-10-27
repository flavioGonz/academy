# Lección 30. DNS en MikroTik

**Escuchá:** dns-mikrotik.mp3 (2 min)

**La idea, en tres líneas**
- RouterOS trae un resolver con caché (`/ip/dns`). Con la configuración por defecto ya es el DNS de la LAN: `allow-remote-requests=yes` y el DHCP entrega 192.168.88.1. Los servidores del proveedor aparecen como `dynamic-servers`; los de `servers` se prueban primero.
- `allow-remote-requests=yes` contesta en UDP y TCP 53 en todas las direcciones del router, también la pública. Sin las reglas de input que lo frenan desde la WAN, el router es un resolver abierto, útil para ataques de amplificación.
- Estáticas para nombres locales (`nvr.lan`), caché que se mira y se vacía, y DoH (`use-doh-server`) para preguntar cifrado. Con DoH no hay respaldo: si el servidor DoH no responde, la LAN recibe SERVFAIL.

**Impacto:** el DNS del cliente deja de ser una caja negra: sabés a quién pregunta, lo probás con un comando y no le prestás tu router a un ataque.

**Quién lo dice:** las 4 fuentes que tratan el tema coinciden en cerrar el puerto 53 hacia internet (documentación de DNS 7.25, foro de 2013, CSIRT de LACNIC y guía de Quad9); en DoH discrepan: un practicante deja los servidores comunes de respaldo y la documentación 7.25 dice que con DoH activo no se usan.

**Laboratorio** · Foco · 20 min
En un RouterBOARD de banco con RouterOS 7 y la configuración por defecto: `ether1` hacia internet (puede ser detrás del router de tu casa), notebook en `ether2`.
1. Mirá a quién le pregunta el router y qué le da el DHCP a la LAN:
```routeros
/ip/dns/print
/ip/dhcp-server/network/print
```
Anotá `servers`, `dynamic-servers`, `allow-remote-requests`, `cache-size` y `cache-used`, y el `dns-server` de la red DHCP.
2. Poné servidores propios y probá desde el router y desde la notebook:
```routeros
/ip/dns/set servers=1.1.1.1,9.9.9.9
:put [:resolve mikrotik.com]
```
```powershell
nslookup mikrotik.com 192.168.88.1
```
Respuesta con dirección: NOERROR. "Non-existent domain": NXDOMAIN. "Server failed": SERVFAIL, el router no consiguió respuesta de arriba.
3. Comprobá que el 53 está cerrado hacia afuera. Con la configuración por defecto lo frena la regla de input `defconf: drop all not coming from LAN`:
```routeros
/ip/firewall/filter/print where chain=input
/ip/address/print where interface=ether1
```
Conectá la notebook a la red del lado de `ether1` (la de tu casa) y preguntale a la IP WAN del router (en el ejemplo, 203.0.113.10). Tiene que dar timeout:
```powershell
nslookup mikrotik.com 203.0.113.10
```
Si el router tiene un firewall propio, sin la configuración por defecto, estas son las dos reglas de la documentación:
```routeros
/ip/firewall/filter/add chain=input in-interface-list=WAN protocol=udp dst-port=53 action=drop comment="drop DNS from WAN"
/ip/firewall/filter/add chain=input in-interface-list=WAN protocol=tcp dst-port=53 action=drop comment="drop DNS from WAN"
```
4. Un nombre local para el NVR, la caché y cómo vaciarla:
```routeros
/ip/dns/static/add name=nvr.lan address=192.168.88.50 comment="NVR de ejemplo"
/ip/dns/cache/print where name~"mikrotik"
/ip/dns/cache/flush
```
Desde la notebook, `nslookup nvr.lan 192.168.88.1` devuelve 192.168.88.50.
5. DoH, con el log abierto en otra terminal:
```routeros
/log/print follow where topics~"dns"
```
```routeros
/ip/dns/set use-doh-server=<URL-DoH> verify-doh-cert=yes
:put [:resolve mikrotik.com]
```
`<URL-DoH>` es la dirección del servicio con `https://` adelante: para Cloudflare, `cloudflare-dns.com/dns-query`. Dejá `servers` cargado, porque el router resuelve con ellos el nombre del servidor DoH. Si el log muestra un error de conexión o de certificado, volvé atrás:
```routeros
/ip/dns/set use-doh-server="" verify-doh-cert=no
```

⚠️ Con DoH activo, todas las consultas van a ese servidor y no hay respaldo: si se cae, toda la LAN se queda sin nombres. Algunos servicios (Quad9, por ejemplo) piden HTTP/2, que en RouterOS 7.25 solo tienen los equipos ARM64 y x86; Cloudflare, Google, NextDNS y OpenDNS andan en todos.

**Regla para quedarse**
El DNS del router contesta a la LAN y a nadie más, y lo pruebo con nslookup desde adentro y desde afuera.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- DNS en RouterOS 7.25: servidores, estáticas, caché, DoH y adlist: https://manual.mikrotik.com/docs/7.25/network-management/dns
- CSIRT de LACNIC: qué es un resolver abierto y por qué importa en la región: https://csirt.lacnic.net/en/dns-open-resolvers-on-ipv4
- Foro, 2013: ataques de amplificación contra routers con DNS abierto: https://forum.mikrotik.com/t/dns-amplification-attack/68310
- Guía de Quad9 para DoH en MikroTik, con la verificación por sniffer: https://docs.quad9.net/Setup_Guides/Open-Source_Routers/MikroTik_RouterOS_(Encrypted)/
- Un practicante arma DoH con respaldo y después lo endurece: https://medo64.com/posts/dns-over-https-for-mikrotik
