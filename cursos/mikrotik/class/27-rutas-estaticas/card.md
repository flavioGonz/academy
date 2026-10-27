# Lección 27. Rutas estáticas

**Escuchá:** rutas-estaticas.mp3 (2 min)

**La idea, en tres líneas**
- Una ruta es destino más gateway. El router busca primero la ruta más específica (la de máscara más larga) y, entre rutas al mismo destino, gana la de menor `distance`: conectada 0, estática 1, OSPF 110. La ruta por defecto es `0.0.0.0/0` y se usa cuando nada más coincide.
- `check-gateway=ping` prueba el gateway cada 10 segundos; con dos respuestas perdidas lo marca inalcanzable y la ruta queda inactiva, así entra la de respaldo con distancia mayor. Mira solo el próximo salto, no internet entero (para eso, las rutas recursivas de la lección de dos WAN).
- Hacia una red remota por un túnel: `dst-address` la LAN de allá y `gateway` la interfaz del túnel, con la ruta de vuelta en el otro extremo. Si la ruta por defecto va por el túnel, la IP pública del servidor VPN necesita su propia ruta /32 por el ISP.

**Impacto:** sabés leer la tabla de rutas de un cliente, armar un respaldo que conmuta solo y unir sucursales sin que el túnel se coma su propio camino.

**Quién lo dice:** 3 de 3 fuentes coinciden en cómo se elige la ruta (documentación de Routing Decision 7.25, la página de IP Routing y una guía práctica no oficial); el foro agrega la parte que más se olvida: las rutas hacen falta en las dos puntas.

**Laboratorio** · Foco · 15 min
En un hAP o hEX de banco con RouterOS 7, configuración por defecto, internet por DHCP en ether1 y la notebook en ether2. Las direcciones 192.168.88.250 y .251 no existen a propósito: hacen de gateways muertos.
1. Leé la tabla y la ruta por defecto que instaló el cliente DHCP:
```routeros
/ip/route/print
/ip/route/print detail where dst-address=0.0.0.0/0
```
`A` activa, `D` dinámica, `c` conectada, `d` de DHCP, `s` estática. Mirá la columna de distancia y `immediate-gw`.
2. Ruta a una red remota por un equipo de la LAN que no existe:
```routeros
/ip/route/add dst-address=10.20.30.0/24 gateway=192.168.88.250 comment="lab principal"
/ip/route/print where dst-address=10.20.30.0/24
/ping 10.20.30.1 count=3
```
La ruta queda activa (el gateway está en una red conectada, así que cuenta como alcanzable) y el ping falla igual.
3. Que el router vigile el gateway:
```routeros
/ip/route/set [find comment="lab principal"] check-gateway=ping
```
Esperá 30 segundos y volvé a imprimir: la ruta pierde la `A`.
4. Un respaldo al mismo destino, con distancia mayor:
```routeros
/ip/route/add dst-address=10.20.30.0/24 gateway=192.168.88.251 distance=2 comment="lab respaldo"
/ip/route/print where dst-address=10.20.30.0/24
```
Como la principal está inactiva, la activa es la de distancia 2. Si la principal vuelve a contestar, recupera el lugar.
5. Para cuando tengas un túnel (lección siguiente), las dos rutas típicas, con datos de ejemplo:
```routeros
/ip/route/add dst-address=192.168.20.0/24 gateway=l2tp-central comment="LAN central por el tunel"
/ip/route/add dst-address=203.0.113.10/32 gateway=192.168.1.1 comment="IP publica del VPN por el ISP"
```
La segunda solo hace falta si la ruta por defecto va por el túnel y el cliente no la agrega solo.
6. Limpiá el banco:
```routeros
/ip/route/remove [find comment~"lab"]
```

⚠️ Tocar la ruta por defecto de un router remoto es la forma más rápida de quedarte afuera: export antes, Safe Mode y un cambio por vez.

**Regla para quedarse**
Gana la más específica, después la de menor distancia; y toda ruta hacia allá necesita su ruta de vuelta.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Routing Decision en RouterOS 7.25: rutas conectadas, distancia, ECMP y check-gateway: https://manual.mikrotik.com/docs/7.25/user-guides/routing-and-networking-protocols/routing-decision
- IP Routing: la ruta más específica y los tipos de ruta: https://help.mikrotik.com/docs/spaces/ROS/pages/328084/IP+Routing
- Guía práctica de rutas estáticas, blackhole y respaldo (no oficial): https://mikrotikdocs.fyi/ip/static-routes-basic/
- Foro: sucursales por L2TP que no se veían hasta rutear en las dos puntas: https://forum.mikrotik.com/t/static-routes-l2tp/181714
