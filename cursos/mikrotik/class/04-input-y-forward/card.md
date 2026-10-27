# Lección 4. Input y forward

**Escuchá:** input-y-forward.mp3 (2 min)

**La idea, en tres líneas**
- Filter tiene tres cadenas: `input` (lo que va a cualquier IP del router, también la de LAN), `forward` (lo que pasa a través) y `output` (lo que sale del router). El dst-nat se hace antes de decidir el camino, así que un port forwarding cae en `forward`; el src-nat (masquerade) se hace después del filter.
- Cada cadena se lee de arriba abajo y manda la primera regla que decide (accept, drop, reject); si ninguna decide, el paquete pasa. Por eso arriba va `established,related` (el resto de las reglas solo ve el primer paquete de cada conexión) y abajo, el drop.
- Una regla se arma con matchers (`in-interface-list`, `src-address-list`, `protocol` y `dst-port`, `connection-state`, `time`, `limit`) y se comprueba con contadores, `log-prefix` y Torch: si el contador no sube, la regla no está coincidiendo.

**Impacto:** dejás de adivinar: sabés en qué cadena va cada regla, la ponés en su lugar y lo comprobás con un número antes de irte de la obra.

**Quién lo dice:** 7 de 7 fuentes coinciden en el reparto de cadenas y en que el orden manda (documentación de Filter, Packet flow, Connection tracking, matchers, address-lists, el firewall avanzado de MikroTik y el hilo de la defconf del foro). La discrepancia es de estilo: una escuela del foro respeta la configuración por defecto y abre agujeros puntuales; otra termina cada cadena con un drop explícito, como el ejemplo de Filter de la documentación.

**Laboratorio** · Foco · 30 min
Router de banco con RouterOS 7 y configuración por defecto: ether1 a la red de la oficina como si fuera internet (lista WAN), notebook en ether2 con 192.168.88.10. Todas las reglas del laboratorio llevan un comentario que empieza con `lab:` para borrarlas juntas al final.
En WinBox todo está en IP > Firewall > Filter Rules. Con `+` creás la regla: Chain, Protocol, Dst. Port, In. Interface List y Connection State en la pestaña General; Src. Address List y Dst. Address List en Advanced; Limit y Time en Extra; Action, Log, Log Prefix y Jump Target en Action. El botón Comment le pone el comentario. La regla nueva queda al final de la lista: la arrastrás a su lugar.

1. Safe Mode (Ctrl+X) y export, como en las lecciones de Safe Mode y backup. Leé el firewall con números y contadores:
```routeros
/export file=antes-firewall
/ip/firewall/filter/print stats
/ip/firewall/nat/print
```
En input ubicá `defconf: accept ICMP` y `defconf: drop all not coming from LAN`; en forward, `defconf: fasttrack` y `defconf: drop all from WAN not DSTNATed`. En nat está el masquerade hacia WAN: se aplica en postrouting, después del filter.

2. Mirá el camino del paquete con tres contadores. `passthrough` suma y deja seguir: no cambia nada. Las dos primeras van arriba de su cadena; output está vacía en la configuración por defecto, así que ahí alcanza con `add`:
```routeros
/ip/firewall/filter/add chain=input src-address=192.168.88.10 protocol=icmp action=passthrough comment="lab: cuenta input" place-before=[find comment="defconf: accept established,related,untracked"]
/ip/firewall/filter/add chain=forward src-address=192.168.88.10 protocol=icmp action=passthrough comment="lab: cuenta forward" place-before=[find comment="defconf: fasttrack"]
/ip/firewall/filter/add chain=output dst-address=1.1.1.1 protocol=icmp action=passthrough comment="lab: cuenta output"
```
Desde la notebook hacé ping a 192.168.88.1, a la IP de ether1 del router y a 1.1.1.1. Desde la terminal del router, `/ping 1.1.1.1 count=3`. Después:
```routeros
/ip/firewall/filter/print stats where comment~"^lab: cuenta"
```
El ping a 192.168.88.1 y el ping a la IP de ether1 suman en input: las dos son IP del router. El ping a 1.1.1.1 suma en forward y el del router, en output. Un dst-nat (lección de port forwarding) cambia el destino antes de esta decisión: lo publicado se cuenta en forward, nunca en input.

3. Estados y fasttrack. Abrí una página web desde la notebook y mirá:
```routeros
/ip/firewall/connection/print where src-address~"192.168.88.10"
/ip/firewall/filter/print stats where chain=forward
```
La primera fila de forward es dinámica, `special dummy rule to show fasttrack counters`: ahí suma lo que va por el camino rápido, que ya no pasa por las reglas de abajo. Arriba de todo está `accept established,related,untracked`, así que el resto de las reglas solo evalúa paquetes `new`. Por eso una regla nueva no corta una conexión que ya estaba abierta: para probar, cerrás la sesión o la borrás con `/ip/firewall/connection/remove`.

4. Ejemplo 1: WinBox y SSH desde WAN solo para la oficina de IES, y log del resto. Una cadena propia (`jump`) junta la gestión desde WAN en un solo lugar; si ninguna regla de esa cadena decide, el paquete vuelve a input donde quedó:
```routeros
/ip/firewall/address-list/add list=admins address=203.0.113.25 comment="lab: oficina IES ejemplo"
/ip/firewall/filter/add chain=input in-interface-list=WAN protocol=tcp dst-port=22,8291 action=jump jump-target=gestion-wan comment="lab: gestion desde WAN" place-before=[find comment="defconf: drop all not coming from LAN"]
/ip/firewall/filter/add chain=gestion-wan src-address-list=admins action=accept comment="lab: admins"
/ip/firewall/filter/add chain=gestion-wan action=drop log=yes log-prefix="GESTION-WAN" comment="lab: resto, log y drop"
```
Desde una PC de la red de la oficina (fuera de `admins`) probá WinBox a la IP de ether1 y mirá el log:
```routeros
/log/print where message~"GESTION-WAN"
```
Sumá la IP de esa PC a `admins` y probá de nuevo: entra. Si en la lección de cerrar puertas limitaste WinBox con `available-from`, la oficina también va ahí. Para entrar de afuera, la primera opción sigue siendo la VPN (lección del túnel de gestión).

5. Ejemplo 2: ping al router desde la LAN sí, con límite; desde WAN, no. Solo se toca el echo request (`8:0`): el resto del ICMP (inalcanzable, fragmentación) sigue por `defconf: accept ICMP`. Las dos van arriba de esa regla:
```routeros
/ip/firewall/filter/add chain=input in-interface-list=LAN protocol=icmp icmp-options=8:0 limit=5,10:packet action=accept comment="lab: ping desde LAN" place-before=[find comment="defconf: accept ICMP"]
/ip/firewall/filter/add chain=input protocol=icmp icmp-options=8:0 action=drop comment="lab: ping resto" place-before=[find comment="defconf: accept ICMP"]
```
Desde la PC de la oficina, el ping a ether1 deja de contestar; desde la notebook, sigue. La lección de reglas de protección muestra la otra opción: ping desde WAN con límite en vez de cortado.

6. Ejemplo 3: el NVR sale solo a NTP y a su nube; las cámaras, a ningún lado. Acá alcanza con `add` al final: lo nuevo que sale de la LAN no coincide con ninguna regla de forward de la configuración por defecto, llega al final y ahí se evalúa en el orden en que lo agregás. El nombre de la nube es de ejemplo: va el que publica el fabricante.
```routeros
/ip/firewall/address-list/add list=nube-nvr address=nube.fabricante.example comment="lab: nube del NVR, ejemplo"
/ip/firewall/address-list/add list=camaras address=192.168.88.101-192.168.88.150 comment="lab: camaras"
/ip/firewall/filter/add chain=forward src-address=192.168.88.50 out-interface-list=WAN protocol=udp dst-port=123 action=accept comment="lab: NVR a NTP"
/ip/firewall/filter/add chain=forward src-address=192.168.88.50 out-interface-list=WAN dst-address-list=nube-nvr action=accept comment="lab: NVR a su nube"
/ip/firewall/filter/add chain=forward src-address=192.168.88.50 out-interface-list=WAN action=reject reject-with=icmp-admin-prohibited comment="lab: NVR resto"
/ip/firewall/filter/add chain=forward src-address-list=camaras out-interface-list=WAN action=drop comment="lab: camaras sin internet"
```
Para probar, poné la notebook con 192.168.88.50: una página web falla enseguida (reject) y el contador de NTP sube si sincronizás la hora. Reject adentro: el equipo se entera al instante y no queda esperando. Drop hacia afuera: al que escanea no se le contesta nada. El DNS del NVR conviene que sea el router, que es input y ya está permitido desde la LAN. Cámaras y NVR en la misma red del bridge no pasan por forward entre ellos: se conmutan en capa 2. Para filtrar entre sistemas, cada uno en su VLAN (lección VLAN por sistema) y zonas (próxima lección).

7. Ejemplo 4: la PC de monitoreo ve solo el NVR. Con la PC en otra red (ether5 fuera del bridge con 10.10.50.1/24, como en la lección de bridges, y la PC en 10.10.50.10):
```routeros
/ip/firewall/filter/add chain=forward src-address=10.10.50.10 dst-address=192.168.88.50 protocol=tcp dst-port=80,443,554,8000 action=accept comment="lab: monitoreo al NVR"
/ip/firewall/filter/add chain=forward src-address=10.10.50.10 action=reject reject-with=icmp-admin-prohibited comment="lab: monitoreo resto"
```

8. Ejemplo 5: invitados con horario, de lunes a viernes de 8 a 20. El reloj y la zona horaria del router mandan, así que primero se miran:
```routeros
/system/clock/print
/ip/firewall/address-list/add list=invitados address=192.168.88.200-192.168.88.220 comment="lab: invitados"
/ip/firewall/filter/add chain=forward src-address-list=invitados out-interface-list=WAN time=8h-20h,mon,tue,wed,thu,fri action=accept comment="lab: invitados en horario"
/ip/firewall/filter/add chain=forward src-address-list=invitados out-interface-list=WAN action=drop comment="lab: invitados fuera de horario"
```
Lo que se abrió antes de las 20 sigue hasta que se cierra: lo acepta `established`.

9. Diagnóstico, en este orden: ¿llega el tráfico?, ¿qué regla lo agarra?, ¿qué pasa si la saco?
```routeros
/tool/torch bridge src-address=192.168.88.50/32 duration=20s
/ip/firewall/filter/reset-counters [find comment~"^lab:"]
/ip/firewall/filter/print stats where chain=forward
/ip/firewall/filter/disable [find comment="lab: camaras sin internet"]
/ip/firewall/filter/enable [find comment="lab: camaras sin internet"]
```
Probá el error de orden a propósito: subí el reject arriba del NTP y mirá cómo el contador de NTP queda quieto. Después volvé a ponerlo abajo:
```routeros
/ip/firewall/filter/move [find comment="lab: NVR resto"] destination=[find comment="lab: NVR a NTP"]
/ip/firewall/filter/move [find comment="lab: NVR a NTP"] destination=[find comment="lab: NVR resto"]
```
`move` deja la regla justo arriba de la de `destination`. Mientras Torch corre, FastTrack se apaga: los contadores de forward suben más que de costumbre.

10. Limpieza:
```routeros
/ip/firewall/filter/remove [find comment~"^lab:"]
/ip/firewall/address-list/remove [find comment~"^lab:"]
```

⚠️ Un drop mal ubicado en input te corta WinBox: todo el laboratorio en Safe Mode. En producción, `log=yes` en una regla muy transitada llena el log y suma CPU: se prende para mirar y se apaga.

**Regla para quedarse**
Primero la cadena, después el lugar, y al final el contador que lo confirma.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Las tres cadenas y los dos métodos de filtrado (RouterOS 7.25): https://manual.mikrotik.com/docs/7.25/firewall-and-quality-of-service/firewall/filter
- El camino del paquete: prerouting, dst-nat, ruteo, forward, src-nat: https://manual.mikrotik.com/docs/7.25/firewall-and-quality-of-service/packet-flow-in-routeros
- Estados de conexión y qué saltea FastTrack: https://help.mikrotik.com/docs/spaces/ROS/pages/130220087/Connection%2Btracking
- Matchers (time, limit, dst-address-type) y contadores con print stats: https://help.mikrotik.com/docs/spaces/ROS/pages/250708064/Common+Firewall+Matchers+and+Actions
- Acciones: accept, drop, reject, jump, return, passthrough: https://help.mikrotik.com/docs/spaces/ROS/pages/48660574/Filter
- La pregunta del foro: cómo un paquete dst-nateado esquiva input: https://forum.mikrotik.com/t/trying-to-understand-defconf-firewall/267442
- Por qué un add común queda debajo del drop: https://manual.mikrotik.com/docs/7.25/firewall-and-quality-of-service/firewall/address-lists
