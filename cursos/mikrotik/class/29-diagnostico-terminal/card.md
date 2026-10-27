# Lección 29. Diagnóstico por terminal

**Escuchá:** diagnostico-terminal.mp3 (2 min)

**La idea, en tres líneas**
- Escalera de adentro hacia afuera: un equipo de la LAN, el gateway del proveedor, una IP de internet, un nombre. El primer escalón que falla dice dónde está el problema (LAN, WAN, ISP o DNS).
- Traceroute de RouterOS 7 repite rondas como mtr: la pérdida real empieza en un salto y sigue en todos los siguientes. Un salto intermedio que pierde mientras el destino contesta es un router que limita ICMP, no una falla.
- `src-address` prueba el camino del tráfico de la LAN (masquerade, túneles entre LAN) y `do-not-fragment` con `size` encuentra la MTU del camino. En RouterOS `size` es el paquete IP entero: 1500 equivale a 1472 de datos en Windows.

**Impacto:** en cinco minutos de terminal sabés si el problema es tuyo, del proveedor o del DNS, y el ticket sale con evidencia en lugar de "no anda internet".

**Quién lo dice:** 5 de 6 fuentes coinciden en el método (documentación de Ping y Traceroute de RouterOS 7.25, dos hilos del foro, Wikipedia y un comentario en el blog de APNIC); en el hilo del foro, quien lo abrió leía la pérdida del salto 2 como un corte del proveedor hasta que los veteranos se lo explicaron.

**Laboratorio** · Campo · 20 min
En un hAP o cualquier RouterBOARD de banco con RouterOS 7 y la configuración por defecto: `ether1` con internet, notebook en `ether2`. Anotá la IP que recibió la notebook (en el ejemplo, 192.168.88.254) y el gateway de la ruta por defecto (en el ejemplo, 203.0.113.1):
```routeros
/ip/dhcp-server/lease/print
/ip/route/print where dst-address=0.0.0.0/0
```
1. La escalera, de adentro hacia afuera, con tres pings por escalón:
```routeros
/ping 192.168.88.254 count=3
/ping 203.0.113.1 count=3
/ping 1.1.1.1 count=3
/ping mikrotik.com count=3
```
```text
Falla el 1 (LAN)          -> cable, puerto, bridge, o el equipo bloquea ping (paso 2)
Anda el 1, falla el 2     -> WAN: cable al módem, IP o VLAN del proveedor, PPPoE caído
Anda el 2, falla el 3     -> ruta por defecto, o el proveedor después de su gateway
Anda el 3, falla el 4     -> DNS ("resolve failed"): mirá /ip/dns
```
2. Si la notebook no contestó (el firewall de Windows suele bloquear el ping), probá con ARP, que en la misma red siempre contesta:
```routeros
/ping 192.168.88.254 arp-ping=yes interface=bridge count=2
```
Si aparece una MAC, el equipo está vivo y el ping lo frena su firewall. Buscá esa MAC en los leases del DHCP.
3. Traceroute a internet, tres rondas, y leé la tabla con estas reglas:
```routeros
/tool/traceroute 1.1.1.1 count=3
```
```text
Un salto con pérdida y los siguientes en 0%     -> ese router limita ICMP: no es falla
Desde un salto en adelante, todo timeout         -> falla después del último que contesta
Dos direcciones que se alternan                  -> lazo de ruteo
Tiempo que sube en un salto y sigue alto         -> enlace lento antes de ese salto
```
4. Probá el camino de la LAN con `src-address`. Primero normal, después desde la IP de la LAN:
```routeros
/ping 1.1.1.1 count=3
/ping 1.1.1.1 src-address=192.168.88.1 count=3
```
Ahora apagá el masquerade a propósito, repetí los dos pings y volvé a prenderlo:
```routeros
/ip/firewall/nat/disable [find comment="defconf: masquerade"]
/ping 1.1.1.1 count=3
/ping 1.1.1.1 src-address=192.168.88.1 count=3
/ip/firewall/nat/enable [find comment="defconf: masquerade"]
```
El ping normal sigue andando y el de la LAN no: así se ve un masquerade roto, aunque el router "tenga internet". Con un túnel entre dos LAN pasa lo mismo: se prueba desde la IP de la LAN.
5. MTU del camino, con el paquete sin fragmentar, bajando hasta que conteste:
```routeros
/ping 1.1.1.1 size=1500 do-not-fragment count=2
/ping 1.1.1.1 size=1492 do-not-fragment count=2
/ping 1.1.1.1 size=1400 do-not-fragment count=2
```
El tamaño más grande que contesta es la MTU del camino (1500 en Ethernet directo, 1492 típico con PPPoE). Desde Windows, la prueba equivalente a 1500 es:
```powershell
ping -f -l 1472 1.1.1.1
```
"fragmentation needed and DF set" con SIZE 576 es el tamaño del mensaje de error, no la MTU. Para ver qué salto tiene la MTU chica: `/tool/traceroute 1.1.1.1 size=1500 do-not-fragment count=1`.

⚠️ Apagar el masquerade corta internet a toda la LAN mientras dura: hacelo solo en el router de banco, nunca en un cliente.

**Regla para quedarse**
Pruebo de adentro hacia afuera, y una pérdida que no sigue en los saltos siguientes no es una falla.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Ping en RouterOS 7.25: estados, MTU, src-address y ARP ping: https://manual.mikrotik.com/docs/7.25/diagnostics-monitoring-and-troubleshooting/ping
- Traceroute en RouterOS 7.25: cómo leer pérdida, lazos y tiempos: https://manual.mikrotik.com/docs/7.25/diagnostics-monitoring-and-troubleshooting/traceroute
- Foro: 100% de pérdida en el salto 2 que no era un corte: https://forum.mikrotik.com/t/traceroute-output/157966
- Foro: por qué RouterOS manda 1500 con DF y Linux solo 1472: https://forum.mikrotik.com/t/ping-from-routeros-relationship-with-mtu/80144
- Origen de traceroute (Van Jacobson, 1987): https://en.wikipedia.org/wiki/Traceroute
