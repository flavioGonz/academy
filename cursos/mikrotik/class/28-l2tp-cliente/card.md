# Lección 28. L2TP saliente

**Escuchá:** l2tp-cliente.mp3 (2 min)

**La idea, en tres líneas**
- El MikroTik del sitio llama a un servidor L2TP/IPsec (la central, un concentrador CHR o el servidor de otra empresa) con `/interface/l2tp-client`: `connect-to`, `user`, `password`, `use-ipsec=yes` y el `ipsec-secret`. Como la conexión sale del sitio, anda aunque el sitio esté detrás de CGNAT o de un módem que no podés tocar.
- `add-default-route=no` (el valor por defecto) para unir redes: solo las LAN de la otra punta van por el túnel, con una ruta cuyo gateway es la interfaz L2TP. `yes` solo si todo el tráfico del sitio tiene que salir por la central.
- La vuelta: o el otro extremo tiene una ruta hacia tu LAN por la IP del túnel, o hacés `masquerade` hacia la interfaz del túnel y del otro lado todo llega como la IP del túnel (sirve cuando no podés tocar el otro extremo, pero desde allá no pueden iniciar conexiones a tus equipos).

**Impacto:** una sucursal o un sitio con CGNAT queda unido a la central sin abrir puertos, y sabés por qué una PC no llega cuando el router sí.

**Quién lo dice:** 3 de 4 fuentes coinciden en el cliente con IPsec y las rutas en las dos puntas (documentación de L2TP y referencia del cliente en 7.25, y dos hilos del foro); un veterano del foro agrega la alternativa del src-nat cuando no se puede rutear del otro lado. La referencia avisa que varios clientes L2TP/IPsec detrás del mismo NAT no funcionan con `use-ipsec`.

**Laboratorio** · Foco · 20 min
Hace falta un servidor L2TP/IPsec como el de la lección de L2TP con IPsec (otro router de banco o un CHR), con IP pública de ejemplo 203.0.113.10 y LAN 10.10.1.0/24. El cliente es un hAP de banco con su LAN por defecto 192.168.88.0/24. Las dos LAN tienen que ser distintas.
1. En el servidor, un usuario para la sucursal con direcciones de túnel fijas, y la ruta hacia la LAN de la sucursal:
```routeros
/ppp/secret/add name=sucursal1 password="Clave-Sucursal-Ejemplo-1" service=l2tp local-address=10.255.1.1 remote-address=10.255.1.2
/ip/route/add dst-address=192.168.88.0/24 gateway=10.255.1.2 comment="LAN sucursal1"
```
2. En el cliente, la interfaz L2TP con IPsec y sin ruta por defecto:
```routeros
/interface/l2tp-client/add name=l2tp-central connect-to=203.0.113.10 user=sucursal1 password="Clave-Sucursal-Ejemplo-1" use-ipsec=yes ipsec-secret="Secreto-IPsec-Largo-De-Ejemplo-2026" add-default-route=no disabled=no
```
3. Verificá que levantó:
```routeros
/interface/l2tp-client/monitor l2tp-central
/ip/ipsec/active-peers/print
/ip/address/print where interface=l2tp-central
```
La interfaz recibe 10.255.1.2 y el peer IPsec aparece establecido.
4. La ruta hacia la LAN central, y la prueba desde una PC de la LAN del cliente:
```routeros
/ip/route/add dst-address=10.10.1.0/24 gateway=l2tp-central comment="LAN central por el tunel"
```
Desde la PC: `ping 10.10.1.1`. Si el router llega y la PC no, falta la ruta de vuelta del paso 1, o el MikroTik no es el gateway de los equipos de allá.
5. Si no podés tocar el otro extremo, la alternativa es NAT hacia el túnel:
```routeros
/ip/firewall/nat/add chain=srcnat out-interface=l2tp-central action=masquerade comment="NAT por el tunel"
```
6. El firewall. El cliente no abre puertos en input: la conexión sale de él. Para entrar por WinBox desde la central, una regla arriba del drop. Y si el otro extremo no es tuyo, sumá el túnel a la lista WAN: la configuración por defecto corta lo que entra desde allá sin pedirlo, y su masquerade pasa a cubrir también el túnel (el mismo efecto que el paso 5):
```routeros
/ip/firewall/filter/add chain=input in-interface=l2tp-central protocol=tcp dst-port=8291 action=accept comment="winbox desde la central" place-before=[find comment="defconf: drop all not coming from LAN"]
/interface/list/member/add list=WAN interface=l2tp-central
```
7. (Opcional) Con `add-default-route=yes` todo sale por la central. Mirá la tabla: aparece una ruta /32 hacia 203.0.113.10 por el gateway del ISP, para que el túnel no intente salir por sí mismo. Para que la LAN navegue así, hace falta el NAT del paso 5 o que la central lo haga. Después volvé a `no`.

Diagnóstico: `/log/print where topics~"l2tp|ipsec"`.

⚠️ L2TP sin IPsec no cifra nada: `use-ipsec=yes` siempre que el túnel cruce internet. Y si la sucursal tenía otro túnel viejo hacia la misma central, deshabilitalo antes: dos túneles hacia las mismas redes se pisan.

**Regla para quedarse**
El sitio llama a la central con IPsec, sin ruta por defecto, y cada LAN tiene su ruta de ida y su ruta de vuelta.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- L2TP en RouterOS 7.25: cliente, servidor y por qué L2TP solo no cifra: https://manual.mikrotik.com/docs/7.25/virtual-private-networks/l2tp/
- Referencia del cliente L2TP: use-ipsec, add-default-route, default-route-distance: https://manual.mikrotik.com/docs/7.25/cli-reference/interface/l2tp-client/
- Foro: la sucursal por 4G que llegaba desde el router y no desde las PC: https://forum.mikrotik.com/t/site-to-site-l2tp-vpn/135121
- Foro: mandar todo por el túnel, dos rutas por defecto y la ruta /32 al servidor: https://forum.mikrotik.com/t/send-all-traffic-through-l2tp-vpn/141695
- RFC 3193 (2001), L2TP protegido con IPsec: https://datatracker.ietf.org/doc/html/rfc3193
