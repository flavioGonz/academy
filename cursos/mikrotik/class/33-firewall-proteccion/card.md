# Lección 33. Reglas de protección

**Escuchá:** firewall-proteccion.mp3 (2 min)

**La idea, en tres líneas**
- `input` protege al router: aceptar `established,related,untracked`, descartar `invalid`, aceptar ICMP (con límite desde WAN, si querés), los admins por address-list y, al final, drop de todo lo que no viene de LAN.
- `forward` protege a la LAN: FastTrack de lo establecido, drop de `invalid` y drop de lo nuevo que entra por WAN sin dst-nat (`connection-nat-state=!dstnat`).
- Las listas contra fuerza bruta y el drop del puerto 53 desde WAN son capas extra: la primera defensa es no exponer gestión ni DNS a internet.

**Impacto:** sabés qué hace cada regla del firewall, detectás un DNS abierto antes de que llame el proveedor y, si un SSH tiene que quedar expuesto, lo blindás sin dejarte afuera.

**Quién lo dice:** 6 de 7 fuentes coinciden en la estructura input/forward con drop final y en no exponer DNS ni gestión; en las listas de fuerza bruta, la documentación las propone como capa extra y un veterano del foro las considera casi inútiles; limitar ICMP es opcional según el propio MikroTik, porque el kernel ya lo limita a 100 paquetes por segundo.

**Laboratorio** · Foco · 20 min
Router de banco con RouterOS 7 y configuración por defecto: `ether1` en la lista WAN (toma IP por DHCP de la red de la oficina), notebook de administración en `ether2` (192.168.88.10) y otra notebook del lado de `ether1` para probar "desde internet" (en el ejemplo, 192.0.2.50). Antes de tocar: export (lección de backup) y Safe Mode.
1. Mirá el firewall por defecto y ubicá cada regla:
```routeros
/ip/firewall/filter/print where chain=input
/ip/firewall/filter/print where chain=forward
```
En input: `defconf: accept established,related,untracked`, `defconf: drop invalid`, `defconf: accept ICMP`, `defconf: drop all not coming from LAN`. En forward: `defconf: fasttrack`, `defconf: accept established,related, untracked`, `defconf: drop invalid`, `defconf: drop all from WAN not DSTNATed`.
2. Ping desde WAN con límite (opcional), arriba del accept ICMP de fábrica:
```routeros
/ip/firewall/filter/add chain=input in-interface-list=WAN protocol=icmp icmp-options=8:0 limit=5,10:packet action=accept comment="ping WAN limitado" place-before=[find comment="defconf: accept ICMP"]
/ip/firewall/filter/add chain=input in-interface-list=WAN protocol=icmp icmp-options=8:0 action=drop comment="ping WAN excedido" place-before=[find comment="defconf: accept ICMP"]
```
Los demás tipos de ICMP (destino inalcanzable, tiempo excedido, fragmentación necesaria) siguen entrando por la regla de fábrica: los necesitan traceroute y el ajuste de MTU.
3. DNS: mirá si el router responde consultas y cerrá el 53 desde WAN arriba de todo:
```routeros
/ip/dns/print
/ip/firewall/filter/add chain=input in-interface-list=WAN protocol=udp dst-port=53 action=drop comment="DNS no desde WAN" place-before=[find chain=input comment="defconf: accept established,related,untracked"]
/ip/firewall/filter/add chain=input in-interface-list=WAN protocol=tcp dst-port=53 action=drop comment="DNS TCP no desde WAN" place-before=[find chain=input comment="defconf: accept established,related,untracked"]
```
Desde la notebook WAN: `nslookup mikrotik.com <IP WAN del router>` no recibe respuesta. Con la defconf, el drop final ya lo cubría; estas dos reglas lo dejan explícito aunque alguien agregue después un accept amplio desde WAN. Si la LAN no usa al router como DNS, además `allow-remote-requests=no`.
4. Solo si SSH tiene que quedar abierto a WAN (lo exige un proveedor, no hay VPN): admins exceptuados y las listas por etapas de la documentación, todas arriba del drop final:
```routeros
/ip/firewall/address-list/add list=admins address=198.51.100.7 comment="oficina ejemplo"
/ip/firewall/filter
add chain=input protocol=tcp dst-port=22 in-interface-list=WAN src-address-list=admins action=accept comment="SSH admins" place-before=[find comment="defconf: drop all not coming from LAN"]
add chain=input protocol=tcp dst-port=22 connection-state=new in-interface-list=WAN src-address-list=connection3 action=add-src-to-address-list address-list=bruteforce_blacklist address-list-timeout=1d comment="SSH fb: lista negra" place-before=[find comment="defconf: drop all not coming from LAN"]
add chain=input protocol=tcp dst-port=22 connection-state=new in-interface-list=WAN src-address-list=connection2 action=add-src-to-address-list address-list=connection3 address-list-timeout=1h comment="SSH fb: tercera" place-before=[find comment="defconf: drop all not coming from LAN"]
add chain=input protocol=tcp dst-port=22 connection-state=new in-interface-list=WAN src-address-list=connection1 action=add-src-to-address-list address-list=connection2 address-list-timeout=15m comment="SSH fb: segunda" place-before=[find comment="defconf: drop all not coming from LAN"]
add chain=input protocol=tcp dst-port=22 connection-state=new in-interface-list=WAN action=add-src-to-address-list address-list=connection1 address-list-timeout=5m comment="SSH fb: primera" place-before=[find comment="defconf: drop all not coming from LAN"]
add chain=input protocol=tcp dst-port=22 in-interface-list=WAN src-address-list=!bruteforce_blacklist action=accept comment="SSH fb: aceptar" place-before=[find comment="defconf: drop all not coming from LAN"]
add chain=input protocol=tcp dst-port=22 in-interface-list=WAN action=drop comment="SSH fb: drop lista negra" place-before=[find comment="defconf: drop all not coming from LAN"]
```
Las reglas de lista no frenan el paquete: lo anotan y sigue. Por eso van en orden inverso (cada conexión sube un escalón) y por eso hace falta el drop del final. Si en la lección de cerrar puertas limitaste SSH con `available-from`, para esta prueba de banco sumale la red de la notebook WAN.
5. Probalo: desde la notebook WAN abrí y cerrá `ssh admin@<IP WAN del router>` cuatro veces en menos de cinco minutos, y mirá:
```routeros
/ip/firewall/address-list/print where list~"^connection|^bruteforce"
/ip/firewall/filter/print stats where comment~"SSH"
/log/print where message~"login failure"
```
Para desbloquear la notebook de prueba:
```routeros
/ip/firewall/address-list/remove [find list~"^connection|^bruteforce" address=192.0.2.50]
```

⚠️ Las listas cuentan conexiones nuevas, no logins fallidos: un login exitoso también suma, y un script o un backup que abre otra sesión te puede dejar afuera un día. La lista `admins` va siempre primero. En sitios con dos WAN y ruteo asimétrico, `drop invalid` puede cortar conexiones legítimas (lo advierte la documentación de connection tracking).

**Regla para quedarse**
Input cuida al router, forward cuida a la LAN, y lo que no permití a propósito termina en un drop.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Receta oficial contra fuerza bruta por SSH, con sus números: https://manual.mikrotik.com/docs/7.25/firewall-and-quality-of-service/user-guides/bruteforce-prevention
- Los 409 GB de subida por un DNS abierto: https://forum.mikrotik.com/t/large-bandwidth-usage-upstream-on-idle/94237
- Por qué un veterano del foro desconfía de las listas por etapas: https://forum.mikrotik.com/t/bruteforce-prevention-issue/123058
