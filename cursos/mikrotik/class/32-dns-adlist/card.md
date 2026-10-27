# Lección 32. Bloqueo por DNS

**Escuchá:** dns-adlist.mp3 (2 min)

**La idea, en tres líneas**
- Adlist (RouterOS 7.15 en adelante): una lista de dominios, por URL o archivo, que el router contesta con `0.0.0.0` (y `::` en IPv6). Vive en la caché DNS: unos 75 bytes por nombre, así que primero se sube `cache-size`. Bloquea solo el nombre exacto, no los de abajo.
- Para un sitio entero con sus subdominios, una estática `type=NXDOMAIN match-subdomain=yes`. Para sacar un nombre de la adlist, una estática `type=FWD` con ese nombre.
- Para cortar en el firewall, una estática FWD con `address-list` carga las direcciones que el router les contestó a los equipos. Una address-list con el nombre la resuelve el router por su cuenta y, con CDN, puede no coincidir. Todo esto vale para quien usa el DNS del router: DoH y VPN pasan igual.

**Impacto:** bloqueás publicidad y sitios puntuales en toda la red sin software extra, y le explicás al cliente qué cubre y qué no antes de que te lo reclame.

**Quién lo dice:** 4 de 5 fuentes coinciden en que el bloqueo por DNS es el camino en el router y en sus límites (documentación de DNS y de address lists 7.25, el hilo de 7.15 del foro, un hilo sobre bloqueo por firewall); antes de adlist, un veterano del foro recomendaba un DNS externo que filtre para no cargar el router, y un practicante bloqueaba con estáticas hacia una IP muerta y `reject` en el firewall.

**Laboratorio** · Foco · 20 min
En un RouterBOARD de banco con RouterOS 7.15 o más y la configuración por defecto, notebook en `ether2` usando el router como DNS (o con el DNS transparente de la lección anterior). Los dominios son los reservados para ejemplos.
1. Mirá versión, arquitectura y memoria, y el estado de la caché:
```routeros
/system/resource/print
/ip/dns/print
```
Anotá `version`, `architecture-name`, `free-memory`, `free-hdd-space`, `cache-size` y `cache-used`. MikroTik recomienda adlist en equipos ARM64; en un equipo chico, listas chicas.
2. Subí la caché y cargá una adlist de prueba desde un archivo del router:
```routeros
/ip/dns/set cache-size=16384
/file/add name=adlist-prueba.txt contents="0.0.0.0 example.net\nads.example.net\n"
/ip/dns/adlist/add file=adlist-prueba.txt
/ip/dns/adlist/print
```
Desde la notebook:
```powershell
nslookup example.net 192.168.88.1
nslookup www.example.net 192.168.88.1
```
`example.net` devuelve 0.0.0.0 y `www.example.net` su dirección real: la adlist bloquea solo el nombre exacto. En `/ip/dns/adlist/print`, `match-count` sube. Para una lista pública en formato hosts se usa `url=` en vez de `file=`, y si no entra en la caché el log dice `adlist read: max cache size reached`.
3. Un sitio entero, con todo lo de abajo:
```routeros
/ip/dns/static/add name=example.com type=NXDOMAIN match-subdomain=yes comment="bloqueo sitio ejemplo"
```
`nslookup example.com 192.168.88.1` y `nslookup www.example.com 192.168.88.1` dan "Non-existent domain".
4. Una excepción y una pausa. La entrada FWD saca el nombre de la adlist; la pausa apaga todas las adlists un rato:
```routeros
/ip/dns/static/add name=example.net type=FWD comment="excepcion adlist"
/ip/dns/adlist/pause duration=10m
```
Repetí `nslookup example.net 192.168.88.1`: ya no da 0.0.0.0.
5. Cortar en el firewall con lo que contesta el DNS. La lista se llena cuando un equipo pregunta por el nombre:
```routeros
/ip/dns/static/add name=example.org type=FWD address-list=bloqueo-ejemplo match-subdomain=yes comment="bloqueo por firewall ejemplo"
/ip/firewall/filter/add chain=forward in-interface-list=LAN dst-address-list=bloqueo-ejemplo action=reject reject-with=icmp-admin-prohibited comment="bloqueo por dominio"
```
Desde la notebook, `ping example.org`; después, en el router:
```routeros
/ip/firewall/address-list/print where list=bloqueo-ejemplo
```
Aparecen las direcciones que el router le contestó, y el ping recibe el rechazo. Con `reject` el navegador corta enseguida; con `drop` se queda esperando.
6. Limpieza del laboratorio:
```routeros
/ip/dns/static/remove [find comment~"ejemplo"]
/ip/dns/static/remove [find comment="excepcion adlist"]
/ip/dns/adlist/remove [find file=adlist-prueba.txt]
/ip/firewall/filter/remove [find comment="bloqueo por dominio"]
```

⚠️ Con CDN, varias marcas comparten direcciones: un bloqueo por address-list puede cortar servicios que nadie quería cortar, y un permiso puede abrir otros. Para sitios, preferí el bloqueo por nombre (adlist o NXDOMAIN) y usá el firewall solo para casos puntuales y probados.

**Regla para quedarse**
Bloqueo por nombre en el DNS del router, con caché a medida y DNS transparente, y le digo al cliente que DoH y VPN quedan afuera.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Adlist, estáticas NXDOMAIN y FWD, y address-list desde el DNS (RouterOS 7.25): https://manual.mikrotik.com/docs/7.25/network-management/dns
- Address lists con nombres de dominio y el problema de las CDN: https://manual.mikrotik.com/docs/7.25/firewall-and-quality-of-service/firewall/address-lists
- Foro: llegada de adlist en 7.15 y la recomendación de ARM64: https://forum.mikrotik.com/t/v7-15rc-testing-is-released/175351
- Foro, 2017: 5000 estáticas en un RB951 y la CPU al 80%: https://forum.mikrotik.com/t/ad-blocking-by-static-dns-just-dont-do-it/111280
- Foro: bloquear sitios por firewall con HTTPS y CDN: https://forum.mikrotik.com/t/blocked-allowed-websites-by-firewall-filter-rules/158566
- Foro: adlist contra Pi-hole y las consultas HTTPS RR que se escapan: https://forum.mikrotik.com/t/adlist-and-dns-server/182097
