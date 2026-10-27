# Lección 31. DNS transparente

**Escuchá:** dns-transparente.mp3 (2 min)

**La idea, en tres líneas**
- Las estáticas y los bloqueos del router valen solo para los equipos que le preguntan al router. Un celular, una tele o un DVR con el DNS clavado (8.8.8.8, el de fábrica) los saltea.
- Dos reglas de NAT, UDP y TCP 53, desde la lista LAN y hacia cualquier destino que no sea el router (`dst-address-type=!local`), con `action=redirect`: el equipo cree que le contesta 8.8.8.8 y le contesta el MikroTik. Con `dst-nat` se manda a otro servidor (un Pi-hole).
- Excepciones en una lista (el propio servidor DNS, un controlador de dominio). DoH viaja cifrado por el 443 y no se redirige: hay paliativos (dominio canario de Firefox, cortar DoT en el 853), no un candado.

**Impacto:** la LAN entera usa el DNS que configuraste, los nombres locales y los bloqueos llegan a todos los equipos, y sabés explicarle al cliente qué queda afuera.

**Quién lo dice:** 4 de 5 fuentes coinciden en redirigir UDP y TCP 53 al router o a un servidor propio (documentación de DNS 7.25 y tres hilos del foro); sobre DoH discrepan: una parte del foro arma listas de servidores DoH para bloquearlos, un veterano dice que es un blanco móvil y hay que convivir con eso, y otros lo ven como espiar a los usuarios.

**Laboratorio** · Foco · 15 min
En un RouterBOARD de banco con RouterOS 7 y la configuración por defecto (la lista `LAN` contiene al `bridge`), notebook en `ether2`.
1. Comprobá que el router sirve DNS a la LAN y creá un nombre de prueba que solo él conoce:
```routeros
/ip/dns/print
/ip/dns/static/add name=prueba-dns.lan address=192.168.88.77 comment="prueba DNS transparente"
```
`allow-remote-requests` tiene que estar en `yes`; si no, la redirección deja a la LAN sin respuestas.
2. Antes de las reglas, desde la notebook preguntale a Google por ese nombre:
```powershell
nslookup prueba-dns.lan 8.8.8.8
```
Google no lo conoce: "Non-existent domain".
3. La lista de excepciones (en el ejemplo, un servidor con DNS propio en 192.168.88.10):
```routeros
/ip/firewall/address-list/add list=dns-libre address=192.168.88.10 comment="servidor con DNS propio (ejemplo)"
```
4. Las dos reglas de redirección:
```routeros
/ip/firewall/nat/add chain=dstnat in-interface-list=LAN src-address-list=!dns-libre dst-address-type=!local protocol=udp dst-port=53 action=redirect to-ports=53 comment="DNS transparente udp"
/ip/firewall/nat/add chain=dstnat in-interface-list=LAN src-address-list=!dns-libre dst-address-type=!local protocol=tcp dst-port=53 action=redirect to-ports=53 comment="DNS transparente tcp"
```
Para mandarlo a un Pi-hole en vez del router, la acción es `action=dst-nat to-addresses=<IP del Pi-hole> to-ports=53`, con el Pi-hole en `dns-libre`. Si el Pi-hole está en la misma subred que los clientes, además hace falta el src-nat del hairpin (lección del NVR con criterio).
5. Repetí la prueba del paso 2 y mirá los contadores:
```powershell
nslookup prueba-dns.lan 8.8.8.8
```
```routeros
/ip/firewall/nat/print stats where comment~"DNS transparente"
```
Ahora contesta 192.168.88.77: respondió el MikroTik aunque la notebook le preguntó a 8.8.8.8, y los paquetes de la regla udp suben.
6. Paliativos para DoH. El dominio canario de Firefox, para que no prenda DoH por su cuenta, y cortar DNS sobre TLS (puerto 853) para que los equipos vuelvan al 53:
```routeros
/ip/dns/static/add name=use-application-dns.net type=NXDOMAIN comment="Firefox: no activar DoH solo"
/ip/firewall/filter/add chain=forward in-interface-list=LAN protocol=tcp dst-port=853 action=reject reject-with=icmp-admin-prohibited comment="sin DoT"
```
Para ver si alguien igual usa DoH: `/tool/torch bridge src-address=192.168.88.254/32 ip-protocol=tcp port=443` y buscá destinos como 8.8.8.8 o 1.1.1.1 en el 443.

⚠️ Si en la red hay un DNS propio en otra VLAN (un controlador de dominio, un Pi-hole), sumalo a `dns-libre` antes de crear las reglas: sin la excepción, sus consultas también van al router y los nombres del dominio dejan de resolver.

**Regla para quedarse**
UDP y TCP 53 de la LAN van al DNS que yo elijo, con una lista de excepciones, y sé que DoH queda afuera.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Por qué estáticas y adlists no alcanzan a los equipos con otro DNS (RouterOS 7.25): https://manual.mikrotik.com/docs/7.25/network-management/dns
- Foro: redirect o dst-nat para el DNS, explicado: https://forum.mikrotik.com/t/dns-redirect-action-redirect-vs-dst-nat/138046
- Foro: las dos reglas, la excepción y el DoH que se escapa al 443: https://forum.mikrotik.com/t/force-dns-request/180041
- Foro: bloquear DoH con listas y el dominio canario de Firefox: https://forum.mikrotik.com/t/redirecting-or-blocking-doh-dns-over-https-requests-made-by-clients/147912
- Foro: por qué DoH no se redirige, y el caso del hotel: https://forum.mikrotik.com/t/help-redirecting-doh-requests-to-internal-dns/157195
