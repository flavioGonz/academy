# Lección 14. Cliente DHCP

**Escuchá:** cliente-dhcp.mp3 (2 min)

**La idea, en tres líneas**
- El cliente DHCP instala dirección, ruta por defecto, DNS (`use-peer-dns`) y NTP (`use-peer-ntp`); `print detail` muestra qué recibió y el estado tiene que ser `bound`.
- `default-route-distance` decide qué ruta por defecto gana: con dos WAN en distancia 1 el tráfico se reparte (ECMP); el respaldo va con distancia mayor.
- Si ether1 recibe una IP privada hay doble NAT: compará con `public-address` de IP Cloud antes de prometer acceso remoto.

**Impacto:** sabés qué ruta y qué DNS usa el sitio, y detectás el doble NAT antes de que te lo reclamen.

**Quién lo dice:** 2 de 3 fuentes coinciden (primera configuración y página del cliente DHCP); nadie discrepa. MKController (vende una plataforma de gestión) advierte que las rutas recursivas no sirven con gateway dinámico.

**Laboratorio** · Foco · 15 min
En un RouterBOARD con RouterOS 7, ether1 conectado a un módem o a otro router que entregue DHCP:
1. Mirá qué recibió el cliente:
```routeros
/ip/dhcp-client/print detail
/ip/route/print where dst-address=0.0.0.0/0
/ip/dns/print
```
Anotá `status`, `address`, `gateway`, `primary-dns` y `primary-ntp`.
2. Si este enlace va a ser el respaldo, subile la distancia y mirá la ruta:
```routeros
/ip/dhcp-client/set [find interface=ether1] default-route-distance=2
/ip/route/print where dst-address=0.0.0.0/0
```
3. Pedí un lease nuevo sin esperar:
```routeros
/ip/dhcp-client/renew [find interface=ether1]
```
4. Detectá doble NAT:
```routeros
/ip/cloud/print
```
`address` del cliente en 10.x, 172.16.x a 172.31.x o 192.168.x: hay otro NAT adelante (módem en modo router). En 100.64.0.0/10: CGNAT (lección 9).
5. (Avanzado) Para failover con gateway dinámico, mirá el script de lease de la documentación: crea o corrige una ruta con `$"gateway-address"` cuando `$bound=1` y la borra cuando el lease se pierde. Probalo primero en laboratorio.

⚠️ Si el servidor manda rutas por la opción 121, el gateway de la opción 3 se ignora: si te falta la ruta por defecto, probá `add-default-route=special-classless`.

**Regla para quedarse**
Lo que instala el DHCP, lo leo antes de irme: dirección, ruta, DNS y si hay otro NAT adelante.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Cliente DHCP en RouterOS 7.25, rutas, distancia y scripts: https://manual.mikrotik.com/docs/7.25/network-management/dhcp/client/
- Por qué las rutas recursivas piden gateway estable: https://mkcontroller.com/blog/tutorials/mikrotik/mikrotik-dual-wan-failover-isp-guide/
- public-address y NAT delante del router: https://manual.mikrotik.com/docs/7.25/network-management/cloud/
