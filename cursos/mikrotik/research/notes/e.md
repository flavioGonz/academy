# Notes: batch e (port forwarding de NVR, lección 24)
Pages read: 17 (5 nuevas de esta tanda y 12 ya en raw/). With notes: 17. Skipped: 0. No se pudieron guardar: la lista oficial de puertos de Hikvision en us-legacy.hikvision.com (el proxy no llega al sitio) ni el artículo de supportusa.hikvision.com (solo carga con JavaScript).

Páginas: manual.mikrotik.com 7.25 (NAT, Filter, First Time Configuration), help.mikrotik.com congelado (Building Advanced Firewall, Connection tracking), forum.mikrotik.com (Need help with port forwarding 159605, Noob NAT port 80 breaking outbound web 41994, Hairpin NAT using Local DNS 174370, SOLVED hairpin 97689, Trying to understand defconf 267442), Dahua (How to Setup Remote Access for NVR), videoexpertsgroup.com (Port 37777, Hikvision RTSP), learncctv.com (Default ports, Ports to forward, Hikvision port forwarding), netviewcctv.co.uk (Ports needed for remote access to Hikvision), modat.io (Internet-exposed RTSP), bleepingcomputer.com (80.000 Hikvision), thehackernews.com (14.500 Dahua), IETF (RFC 1631, RFC 3022, RFC 6598).

## T15 NAT y port forwarding (lección 24)
- e:N1. dst-nat cambia la dirección de destino de un paquete que va hacia la red con NAT; el uso típico es hacer accesible desde internet un equipo de la LAN. Ejemplo oficial: chain=dstnat action=dst-nat dst-address=<IP pública> dst-port=22 to-addresses=10.0.0.3.
  - Source: https://manual.mikrotik.com/docs/7.25/firewall-and-quality-of-service/firewall/nat  Quote: "It is most commonly used to make hosts on a private network accessible from the Internet"
  - Kind: definition
  - Level: foundation
- e:N2. Sumar src-address al dst-nat para permitir solo la PC de casa "también se considera más seguro".
  - Source: https://manual.mikrotik.com/docs/7.25/firewall-and-quality-of-service/firewall/nat  Quote: "It is also considered to be more secure!"
  - Kind: technique
  - Level: foundation
- e:N3. NAT solo mira el primer paquete de la conexión; después de cambiar reglas hay que limpiar el connection tracking o las reglas parecen no funcionar.
  - Source: https://manual.mikrotik.com/docs/7.25/firewall-and-quality-of-service/firewall/nat  Quote: "NAT rules may seem to be not functioning correctly until the connection entry expires"
  - Kind: technique
  - Level: core
- e:N4. El firewall por defecto descarta en forward lo nuevo que entra por WAN y no fue dst-nateado (connection-nat-state=!dstnat). Un veterano del foro: con la defconf alcanza con agregar el dst-nat en NAT, los filtros ya están bien.
  - Source: https://forum.mikrotik.com/t/trying-to-understand-defconf-firewall/267442  Quote: "they would only add a DSTNAT entry on the NAT page, and the filters are already OK"
  - Kind: technique
  - Level: foundation
  - Also: https://help.mikrotik.com/docs/spaces/ROS/pages/328513/Building+Advanced+Firewall (regla "drop all from WAN not DSTNATed")
- e:N5. Con un firewall propio estricto, el puerto publicado tiene que estar permitido en forward (lo dice el ejemplo de RDP de la primera configuración). En el foro: alcanza una sola regla en forward para permitir el port forwarding en general.
  - Source: https://manual.mikrotik.com/docs/7.25/getting-started/first-time-configuration  Quote: "must be allowed in the firewall filter forward chain"
  - Kind: technique
  - Level: core
  - Also: https://forum.mikrotik.com/t/need-help-with-port-forwarding/159605 ("You only need on rule in the forward chain to permit port forwarding in general")
- e:N6. El ejemplo de primera configuración publica RDP con solo protocol y dst-port, sin in-interface ni dst-address ni origen.
  - Source: https://manual.mikrotik.com/docs/7.25/getting-started/first-time-configuration  Quote: "chain=dstnat action=dst-nat protocol=tcp dst-port=3389"
  - Kind: technique
  - Level: foundation
- e:N7. Una regla dst-nat con solo dst-port=80 rompió la navegación de toda la LAN: agarraba cualquier conexión al puerto 80, de la LAN o de la WAN. Arreglo: dst-address con la IP pública o in-interface de la WAN si la IP es dinámica.
  - Source: https://forum.mikrotik.com/t/noob-sorry-nat-port-80-breaking-outbound-web/41994  Quote: "This includes all LAN and WAN traffic, hence why it broke your web browsing"
  - Kind: story
  - Level: foundation
- e:N8. En el foro, anav: con WAN fija, dst-address=<IP pública>; con WAN dinámica, in-interface de la WAN. Y address-lists para que el servidor no aparezca en escaneos; quien tenga IP dinámica puede dar un nombre DDNS y el router lo resuelve.
  - Source: https://forum.mikrotik.com/t/need-help-with-port-forwarding/159605  Quote: "it makes the server NOT visible on scans of your ports"
  - Kind: technique
  - Level: core
- e:N9. Caso: NVR Dahua detrás de un RB4011, la app y el cliente de PC hacen login desde internet (443 publicado) pero no muestran video ni grabaciones. Otro usuario: para un Dahua tuvo que publicar TCP 443, 554 y 37777 y UDP 37778.
  - Source: https://forum.mikrotik.com/t/need-help-with-port-forwarding/159605  Quote: "TCP 443,554,37777 UDP 37778"
  - Kind: story
  - Level: core
- e:N10. Hairpin: desde la misma red que el servidor, la respuesta va directo al cliente con otra IP de origen y el cliente la descarta. Arreglo: masquerade en srcnat desde la LAN hacia el servidor por la interfaz LAN.
  - Source: https://manual.mikrotik.com/docs/7.25/firewall-and-quality-of-service/firewall/nat  Quote: "it discards it because it expects a packet back from 172.16.16.1"
  - Kind: technique
  - Level: core
- e:N11. Hairpin que no anda porque el dst-nat tiene in-interface del PPPoE: desde la LAN nunca coincide. Cambiarlo por dst-address-type=local dst-address=!<IP LAN del router>.
  - Source: https://forum.mikrotik.com/t/solved-hairpin-nat-not-working/97689  Quote: "It won't match connections coming from LAN"
  - Kind: story
  - Level: core
- e:N12. Alternativa al hairpin: DNS dividido o entrada estática en /ip/dns/static que apunte el nombre a la IP LAN del servidor; así el servidor ve la IP real (el hairpin la oculta). Si el puerto externo es distinto del interno, el DNS solo no alcanza; otra opción es poner el servidor en su propia subred.
  - Source: https://forum.mikrotik.com/t/hairpin-nat-using-local-dns/174370  Quote: "If you want to see actual source IP addresses, then you must not use hairpin NAT"
  - Kind: technique
  - Level: advanced
- e:N13. CGNAT (RFC 6598, 100.64.0.0/10): todo lo que necesita conexiones entrantes queda roto; el port forwarding que antes se hacía en el router propio pasa a ser imposible.
  - Source: https://manual.mikrotik.com/docs/7.25/firewall-and-quality-of-service/firewall/nat  Quote: "CGNAT makes this impossible"
  - Kind: definition
  - Level: foundation
  - Also: https://datatracker.ietf.org/doc/html/rfc6598 (abril 2012)
- e:N14. Connection tracking marca dstnat=yes en las conexiones que pasaron por DST-NAT, "por ejemplo, port forwarding".
  - Source: https://help.mikrotik.com/docs/spaces/ROS/pages/130220087/Connection%2Btracking  Quote: "A connection has gone through DST-NAT (for example, port forwarding)"
  - Kind: definition
  - Level: core
- e:N15. RouterOS trae helpers de NAT, entre ellos uno de RTSP, en /ip/firewall/service-ports.
  - Source: https://manual.mikrotik.com/docs/7.25/firewall-and-quality-of-service/firewall/nat  Quote: "RTSP service helper"
  - Kind: definition
  - Level: advanced

## T16 Puertos de NVR por fabricante
- e:N16. Hikvision: 80 HTTP (navegador), 443 HTTPS, 554 RTSP (software de terceros), 8000 puerto de servidor para software (iVMS-4200). Se pueden cambiar desde la web del equipo o con SADP. Hikvision recomienda 10554 porque algunas operadoras móviles bloquean el 554 entrante.
  - Source: https://learncctv.com/default-ports-for-hikvision-dvr  Quote: "Hikvision recommends to use the port 10554"
  - Kind: number
  - Level: core
  - Also: https://learncctv.com/ports-to-forward-for-hikvision-dvrs/
- e:N17. Distribuidor de Hikvision: 80 web, 8000 servidor para iVMS-4200 y la app iVMS-4500, RTSP 10554 para el video, 443 HTTPS; si el RTSP quedó en 554 (equipos o firmware viejos), cambiarlo a 10554 o 1024 si hay problemas por 3G/4G.
  - Source: https://netviewcctv.co.uk/blog/post/ports  Quote: "Server port: 8000 Used to connect via iVMS-4200 software and iVMS-4500 Mobile App"
  - Kind: number
  - Level: core
- e:N18. Un practicante publica un DVR Hikvision con HTTP cambiado a 8082 más 554, 8000 y 443, y marca TCP y UDP en el router doméstico.
  - Source: https://learncctv.com/hikvision-port-forwarding  Quote: "the ports configured in the DVR are 8082, 554, 8000, and 443"
  - Kind: example
  - Level: foundation
- e:N19. Dahua (aviso oficial de 2018): puertos por defecto TCP 37777, UDP 37778, HTTP 80, RTSP 554, HTTPS 443; "normalmente" alcanza con publicar el HTTP y el TCP. Para comprobar, sugiere un servicio externo de chequeo de puertos (canyouseeme).
  - Source: https://www.dahuasecurity.com/about-dahua/news-events/notice/how-to-setup-remote-access-for-nvr  Quote: "Usually you will only need to forward the HTTP and the TCP port."
  - Kind: number
  - Level: core
- e:N20. Dahua 37777: login remoto, video en vivo, reproducción y gestión desde SmartPSS y DMSS; se puede cambiar en la configuración de red; recomiendan no exponerlo y usar VPN o reglas por IP de confianza.
  - Source: https://www.videoexpertsgroup.com/glossary/port-37777  Quote: "Avoid exposing port 37777 to the internet directly"
  - Kind: technique
  - Level: core
- e:N21. URL RTSP de Hikvision: rtsp://usuario:clave@ip:puerto/Streaming/Channels/101 (101 = principal del canal 1); prueba con VLC, Medio, Abrir ubicación de red.
  - Source: https://videoexpertsgroup.com/glossary/hikvision-rtsp  Quote: "commonly \"101\" for the main stream"
  - Kind: example
  - Level: foundation

## T05 Exposición y seguridad de NVR publicados
- e:N22. Modat contó 973.819 servicios RTSP respondiendo en internet en marzo de 2026, en 10.671 puertos distintos; el 554 concentra el 56 %, el 43,9 % está en otros puertos. 8.074 entregaron imagen sin autenticación.
  - Source: https://www.modat.io/post/exposed-rtsp  Quote: "427,872 endpoints (43.9% of the total) exist on other ports entirely"
  - Kind: number
  - Level: core
- e:N23. CVE-2021-36260 de Hikvision (inyección de comandos por el servidor web, parche de septiembre 2021): de 285.000 servidores web Hikvision expuestos, unos 80.000 seguían vulnerables en 2022; Moobot (basada en Mirai) la usó.
  - Source: https://www.bleepingcomputer.com/news/security/over-80-000-exploitable-hikvision-cameras-exposed-online/  Quote: "roughly 80,000 still vulnerable to exploitation"
  - Kind: number
  - Level: core
- e:N24. Campaña sobre más de 14.530 equipos Dahua entre junio y julio de 2026: ataques de credenciales, CVE-2021-33044 y CVE-2021-33045 (salteo de autenticación) y el relay P2P; cifras atribuidas a Hunt.io.
  - Source: https://thehackernews.com/2026/08/hackers-compromised-14500-dahua-devices.html  Quote: "compromised more than 14,530 Dahua devices"
  - Kind: number
  - Level: core

## T15 Historia
- e:N25. RFC 1631 (mayo de 1994, Egevang y Francis) propone NAT como solución de corto plazo al agotamiento de direcciones, con una tabla de pares de direcciones locales y globales.
  - Source: https://datatracker.ietf.org/doc/html/rfc1631  Quote: "place Network Address Translators (NAT) at the borders of stub domains"
  - Kind: history
  - Level: foundation
- e:N26. RFC 3022 (enero de 2001) reemplaza a la 1631, define NAPT (traducción de dirección y puerto) y dice que el modelo se extiende para permitir acceso entrante mapeando de forma estática un equipo local por cada puerto de servicio.
  - Source: https://datatracker.ietf.org/doc/html/rfc3022  Quote: "allow inbound access by statically mapping a local node per each service TU port"
  - Kind: history
  - Level: foundation

## Disagreements seen
- Cuántos puertos publicar en Dahua: el aviso oficial dice que normalmente alcanza con HTTP y TCP 37777; un integrador del foro tuvo que publicar 443, 554, 37777 y 37778 UDP para tener video.
- RTSP de Hikvision: 554 según la página de puertos por defecto y la de RTSP; 10554 recomendado por Hikvision según learncctv y el distribuidor británico, por bloqueos de operadoras móviles.
- Hairpin NAT o DNS local: la documentación resuelve con masquerade; en el foro se prefiere DNS dividido o subred propia para no ocultar la IP real del cliente.
- Ejemplo oficial sin filtro: la primera configuración publica sin in-interface ni origen; la página de NAT pide origen y el foro muestra lo que rompe una regla demasiado general.

## Best stories
- dst-nat con solo dst-port=80 que dejó a toda la LAN sin navegar (https://forum.mikrotik.com/t/noob-sorry-nat-port-80-breaking-outbound-web/41994).
- NVR Dahua: login desde internet sí, video no; faltaban los puertos de datos (https://forum.mikrotik.com/t/need-help-with-port-forwarding/159605).
- 973.819 RTSP expuestos, 43,9 % fuera del 554 (https://www.modat.io/post/exposed-rtsp).
