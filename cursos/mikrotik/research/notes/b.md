# Notes: batch b (practicantes, foro oficial y prensa de seguridad)
Pages read: 13. With notes: 12. Skipped: 1 (wirelessnetware.ca: solo presenta un video y vende curso, una idea útil apenas).

Páginas: forum.mikrotik.com (VLAN guide, defconf firewall, hairpin NAT), mkcontroller.com (dual WAN, gestión por VPS), admiralplatform.com (packet sniffer), wirelessnetware.ca (torch y traceroute), xtremeownage.com (backup a git), cloudzy.com (L2TP/IPsec, en alemán), csoonline.com, securityweek.com, securityaffairs.com y gendigital.com (Mēris y TrickBot).

## T01 Acceso inicial y herramientas de gestión
- b:N1. La "detección de internet" (detect-internet) puede cambiar en silencio las interface lists LAN y WAN y romper reglas de firewall que dependen de ellas; varios veteranos del foro recomiendan apagarla.
  - Source: https://forum.mikrotik.com/t/trying-to-understand-defconf-firewall/267442  Quote: "disable that “detect internet” misfeature"
  - Kind: mistake
  - Level: core
  - Also: T05

## T03 Usuarios, grupos y contraseñas
- b:N2. Para backups automáticos por SSH, un usuario dedicado con grupo mínimo (policy=read,ssh,api,test) y clave pública, no el admin.
  - Source: https://xtremeownage.com/blog/2025/mikrotik-backup-script/  Quote: "Create backup group with minimal read permissions"
  - Kind: template
  - Level: advanced
  - Also: T13

## T04 Servicios IP y superficie de ataque
- b:N3. Eclypsium encontró con Shodan más de 2 millones de MikroTik con alguna interfaz de gestión expuesta (SSH, WinBox o API) y estimó unos 300.000 vulnerables (su cifra).
  - Source: https://www.csoonline.com/article/3644469/researchers-warn-about-continuous-abuse-of-unpatched-mikrotik-routers.html  Quote: "over 2 million MikroTik routers that have one of their management interfaces exposed"
  - Kind: number
  - Level: foundation
- b:N4. CVE-2018-14847: recorrido de directorios por el servicio WinBox (RouterOS 6.42 y anteriores) sin autenticación, que permitía leer credenciales. CISA lo tiene en su catálogo de vulnerabilidades explotadas.
  - Source: https://www.csoonline.com/article/3644469/researchers-warn-about-continuous-abuse-of-unpatched-mikrotik-routers.html  Quote: "can be exploited through the RouterOS (version 6.42 and lower) WinBox management interface without authentication"
  - Kind: definition
  - Level: core
  - Also: T14
- b:N5. Honeypot de Gen Digital: un router virtual con versión vulnerable expuesto a internet fue comprometido a los 15 minutos, aunque el investigador había puesto usuario y contraseña fuertes (entraron por la falla de WinBox). El script del atacante dejaba abiertos solo SSH y WinBox y activaba SOCKS en el puerto 5678.
  - Source: https://www.gendigital.com/blog/insights/research/meris-and-trickbot-standing-on-the-shoulders-of-giants  Quote: "Exactly 15 minutes after deploying the honeypot"
  - Kind: story
  - Level: foundation
  - Also: T14
- b:N6. Un panel de control de la botnet mostraba cerca de 230.000 MikroTik conectados (su observación); parecía botnet como servicio usada por varias campañas.
  - Source: https://www.gendigital.com/blog/insights/research/meris-and-trickbot-standing-on-the-shoulders-of-giants  Quote: "close to 230K of devices"
  - Kind: number
  - Level: core
- b:N7. Mēris llegó a 21,8 millones de pedidos por segundo contra Yandex y se estimó en más de 200.000 equipos, la mayoría MikroTik (cifras de Yandex y Qrator).
  - Source: https://securityaffairs.com/122218/malware/meris-bot-mikrotik-routers.html  Quote: "peaked at the unprecedented rate of 21.8 million requests per second"
  - Kind: number
  - Level: foundation
- b:N8. MikroTik, citado por SecurityWeek: por defecto no debería haber reglas en el Scheduler y SOCKS debería estar apagado; deshabilitar todo lo que no se reconozca. Los equipos que actualizaron y además cambiaron contraseña quedaron protegidos.
  - Source: https://www.securityweek.com/mikrotik-confirms-meris-botnet-targets-routers-compromised-years-ago/  Quote: "By default, there should be no Scheduler rules, and SOCKS should be off"
  - Kind: test
  - Level: core
- b:N9. Equipos no expuestos también se atacan desde adentro: el troyano Glupteba atacaba MikroTik desde PCs de la LAN.
  - Source: https://www.csoonline.com/article/3644469/researchers-warn-about-continuous-abuse-of-unpatched-mikrotik-routers.html  Quote: "attacking MikroTik routers from inside local networks"
  - Kind: story
  - Level: core

## T05 Interfaces, bridge e interface lists
- b:N10. El bridge tiene "dos personalidades", switch e interfaz; entender eso evita la mayoría de las confusiones con PVID y VLAN de gestión (mkx en la guía de VLAN).
  - Source: https://forum.mikrotik.com/t/using-routeros-to-vlan-your-network/126489  Quote: "bridge is actually two personnalities"
  - Kind: definition
  - Level: core
  - Also: T09

## T07 NAT
- b:N11. Caso real: un dst-nat para una cámara funcionaba desde afuera pero no desde la LAN usando la IP pública. El dst-nat tenía in-interface=pppoe y por eso nunca coincidía para tráfico de la LAN. La solución fue cambiar el match a dst-address-type=local (excluyendo la IP LAN del router) y sumar un masquerade de hairpin.
  - Source: https://forum.mikrotik.com/t/solved-hairpin-nat-not-working/97689  Quote: "It won’t match connections coming from LAN"
  - Kind: story
  - Level: advanced
  - Also: T16
- b:N12. No se puede probar desde adentro qué está abierto hacia internet: para saber qué ve el mundo, probar desde afuera.
  - Source: https://forum.mikrotik.com/t/solved-hairpin-nat-not-working/97689  Quote: "if you want to reliably test what’s available from outside, you need to do it from outside"
  - Kind: rule of thumb
  - Level: core
  - Also: T15

## T08 Firewall filter
- b:N13. Input es lo que va al router mismo (dst-address es una IP del router, también la de LAN); forward es lo que pasa a través. "drop all not coming from LAN" protege al router; "drop all from WAN not DSTNATed" protege a la LAN.
  - Source: https://forum.mikrotik.com/t/trying-to-understand-defconf-firewall/267442  Quote: "input chain only applies to packets that have dst-address=self"
  - Kind: definition
  - Level: foundation
- b:N14. Dos escuelas en el foro: una sostiene que el firewall por defecto está bien diseñado y solo hay que abrir agujeros puntuales; la otra reemplaza la última regla por un "drop all else" explícito y agrega antes solo lo permitido.
  - Source: https://forum.mikrotik.com/t/trying-to-understand-defconf-firewall/267442  Quote: "There are mainly two schools of thought on Mikrotik forum about firewall rules"
  - Kind: rule of thumb
  - Level: core
- b:N15. Plantilla mínima "drop por defecto": input acepta established/related/untracked, descarta invalid, acepta ICMP, descarta el resto; forward acepta established/related/untracked, descarta invalid, descarta el resto. Las aceptaciones necesarias van antes del drop final.
  - Source: https://forum.mikrotik.com/t/trying-to-understand-defconf-firewall/267442  Quote: "Required accept rules need to be added before"
  - Kind: template
  - Level: core
- b:N16. El orden importa: una regla accept o drop que coincide corta el procesamiento de esa cadena. Por eso "accept ICMP" va arriba del drop de input.
  - Source: https://forum.mikrotik.com/t/trying-to-understand-defconf-firewall/267442  Quote: "that’s why the order of the rules within the same chain is so important"
  - Kind: rule of thumb
  - Level: foundation
- b:N17. Bloquear ICMP no es una medida de seguridad: rompe Path MTU Discovery y en IPv6 es vital. Si no querés que conteste ping, filtrá solo echo.
  - Source: https://forum.mikrotik.com/t/trying-to-understand-defconf-firewall/267442  Quote: "Blocking ICMP is not a security measure!"
  - Kind: mistake
  - Level: core

## T09 VLANs con bridge vlan-filtering
- b:N18. Guía de referencia del foro para integradores: puertos access (entra sin etiqueta, se etiqueta), trunk (entra y sale etiquetado), híbridos (teléfono con PC atrás). Usa una VLAN base de gestión 99 y evita la VLAN 1 por incompatibilidades con otros fabricantes.
  - Source: https://forum.mikrotik.com/t/using-routeros-to-vlan-your-network/126489  Quote: "it is simpler to use VLAN 2 and higher"
  - Kind: definition
  - Level: foundation
- b:N19. En access, descartar siempre lo que entra etiquetado; en trunk, descartar siempre lo que entra sin etiqueta. Los trunks necesitan seguridad física.
  - Source: https://forum.mikrotik.com/t/using-routeros-to-vlan-your-network/126489  Quote: "always drop ingress packets that do have tags"
  - Kind: rule of thumb
  - Level: core
- b:N20. Una VLAN por área (departamento, piso, edificio) aunque hoy no se filtre: cuando hay un brote de virus en un piso, se puede cortar ese piso solo. Las cámaras IP y los IoT son candidatos típicos a VLAN propia.
  - Source: https://forum.mikrotik.com/t/using-routeros-to-vlan-your-network/126489  Quote: "If you have IoT devices, IP cameras, guests who need to use your WiFi"
  - Kind: story
  - Level: core
- b:N21. El autor de la guía pide que con vlan-filtering=yes los access y trunk se comporten seguros por defecto; hoy hay que agregar ingress-filtering y frame-types a mano.
  - Source: https://forum.mikrotik.com/t/using-routeros-to-vlan-your-network/126489  Quote: "Secure should be the default"
  - Kind: rule of thumb
  - Level: advanced

## T10 Multi-WAN y failover
- b:N22. check-gateway desactiva la ruta tras dos chequeos fallidos y chequea cada 10 s aproximadamente: el cambio real tarda 20 a 30 s y no reacciona a pérdida intermitente, solo a gateway muerto (su resumen de la documentación).
  - Source: https://mkcontroller.com/blog/tutorials/mikrotik/mikrotik-dual-wan-failover-isp-guide/  Quote: "real switch-over lands around 20 to 30 seconds"
  - Kind: number
  - Level: advanced
  - Bias: vende una plataforma de gestión centralizada (MKController).
- b:N23. Rutas recursivas funcionan con gateways IP estables; con PPPoE o DHCP donde el gateway cambia, hay que adaptar (o usar Netwatch).
  - Source: https://mkcontroller.com/blog/tutorials/mikrotik/mikrotik-dual-wan-failover-isp-guide/  Quote: "recursive routing only works with stable IP gateways"
  - Kind: rule of thumb
  - Level: advanced
  - Bias: vende plataforma de gestión.
- b:N24. Netwatch en v7 tiene tipos icmp, tcp-conn, http-get, https-get e intervalos propios, con scripts up/down: más rápido y flexible que check-gateway, a costa de scripts. Muchos combinan ambos.
  - Source: https://mkcontroller.com/blog/tutorials/mikrotik/mikrotik-dual-wan-failover-isp-guide/  Quote: "Many operators combine the two"
  - Kind: technique
  - Level: advanced
- b:N25. Probar el failover desconectando el cable del primario y cronometrando, y alertar cuando un sitio queda días en el enlace de respaldo: un failover que nadie nota es un costo, no un ahorro.
  - Source: https://mkcontroller.com/blog/tutorials/mikrotik/mikrotik-dual-wan-failover-isp-guide/  Quote: "pull the primary’s connector and time the real switch-over"
  - Kind: test
  - Level: core
- b:N26. El testigo del enlace de respaldo tiene que alcanzarse por ese enlace, no por el primario; si no, la prueba no dice nada.
  - Source: https://mkcontroller.com/blog/tutorials/mikrotik/mikrotik-dual-wan-failover-isp-guide/  Quote: "or your test is meaningless"
  - Kind: mistake
  - Level: advanced
- b:N27. Los dst-nat atados a la IP del primario dejan de funcionar cuando cae ese enlace; por eso el acceso saliente (túnel) escala mejor que el port forwarding.
  - Source: https://mkcontroller.com/blog/tutorials/mikrotik/mikrotik-dual-wan-failover-isp-guide/  Quote: "outbound-anchored access scales better than port-forwarding"
  - Kind: rule of thumb
  - Level: core
  - Also: T16
  - Bias: vende acceso por túnel saliente.

## T11 VPN para gestión remota
- b:N28. Con el sitio detrás de NAT doble o CGNAT, el MikroTik abre un túnel saliente a un VPS con IP fija y se entra por ahí (el ejemplo usa OpenVPN; menciona WireGuard y SSTP como variantes). Cada MikroTik con su propio certificado o clave.
  - Source: https://mkcontroller.com/blog/remote_access/mikrotik/remote_mikrotik_management_via_vps  Quote: "it never accepts inbound connections, so NAT and CGNAT on the customer side don’t matter"
  - Kind: technique
  - Level: advanced
  - Bias: vende alternativa administrada (NATCloud).
- b:N29. L2TP/IPsec: L2TP no cifra, IPsec sí. Puertos en input: UDP 500, 4500, 1701 y protocolo ESP. use-ipsec=required, secreto largo, profile con pool. Ventaja: cliente nativo en Windows, macOS, iOS y Android sin instalar nada.
  - Source: https://cloudzy.com/de/blog/mikrotik-l2tp-vpn/  Quote: "UDP-Port 500 akzeptieren"
  - Kind: template
  - Level: core
  - Bias: vende VPS MikroTik.
- b:N30. L2TP/IPsec y FastTrack: hace falta una regla accept con ipsec-policy=in,ipsec arriba de fasttrack, y en el perfil change-tcp-mss=yes para evitar cortes por MTU.
  - Source: https://cloudzy.com/de/blog/mikrotik-l2tp-vpn/  Quote: "Change TCP MSS auf yes"
  - Kind: mistake
  - Level: advanced
- b:N31. Evitar PPTP por sus fallas conocidas; L2TP/IPsec es la alternativa nativa.
  - Source: https://cloudzy.com/de/blog/mikrotik-l2tp-vpn/  Quote: "Setzen Sie PPTP niemals in einem Unternehmensnetzwerk ein"
  - Kind: rule of thumb
  - Level: foundation

## T12 IP Cloud y DDNS
- b:N32. Un caso del foro usa IP Cloud como DNS apuntando al router de borde y publica cámaras y servidores por puertos; el problema que pregunta es el hairpin desde adentro.
  - Source: https://forum.mikrotik.com/t/solved-hairpin-nat-not-working/97689  Quote: "I have my DNS setup on the IP/Cloud feature"
  - Kind: story
  - Level: core
  - Also: T16

## T13 Backups, export y gestión de cambios
- b:N33. Backup a git: un script en Linux entra por SSH, corre /export show-sensitive terse verbose, quita la línea de fecha y hace commit solo si hubo cambios. Así quedó registrado sin intervención un cambio de credenciales PPPoE del ISP.
  - Source: https://xtremeownage.com/blog/2025/mikrotik-backup-script/  Quote: "I only wanted a commit performed, when there were changes"
  - Kind: story
  - Level: advanced
- b:N34. El export con show-sensitive incluye secretos: el archivo resultante pasa a ser sensible y se guarda como tal.
  - Source: https://xtremeownage.com/blog/2025/mikrotik-backup-script/  Quote: "/export show-sensitive terse verbose"
  - Kind: rule of thumb
  - Level: core

## T14 Actualización de RouterOS y RouterBOOT
- b:N35. El problema de los equipos embebidos no es que el fabricante no saque parches: es que los usuarios actualizan routers mucho menos que una PC. MikroTik responde bien a las fallas según CSO.
  - Source: https://www.csoonline.com/article/3644469/researchers-warn-about-continuous-abuse-of-unpatched-mikrotik-routers.html  Quote: "users are not as likely to update their firmware"
  - Kind: rule of thumb
  - Level: foundation

## T15 Troubleshooting
- b:N36. Packet sniffer en WinBox (Tools, Packet Sniffer): darle memoria (1 MB si hay RAM), nombre de archivo .pcap con fecha y router, filtro por IP o MAC del equipo y la interfaz (bridge). Un archivo de 24 bytes significa que no capturó nada.
  - Source: https://admiralplatform.com/tips4tiks-packet-capture-with-mikrotik/  Quote: "the file will start at 24B"
  - Kind: technique
  - Level: core
- b:N37. Caso: un portal cautivo mostraba página en blanco; con la captura en Wireshark, filtrando DNS, aparecieron unos 20 dominios que había que permitir y que la documentación del proveedor no listaba.
  - Source: https://admiralplatform.com/tips4tiks-packet-capture-with-mikrotik/  Quote: "a whopping 20 different domains"
  - Kind: story
  - Level: core
- b:N38. Comparar dos capturas lado a lado, una de un entorno que funciona y otra del que falla, acelera encontrar la diferencia. Ojo: una captura llena el disco rápido.
  - Source: https://admiralplatform.com/tips4tiks-packet-capture-with-mikrotik/  Quote: "Packet captures can fill up a disk VERY quickly"
  - Kind: technique
  - Level: advanced
- b:N39. Ping y traceroute generan tráfico; Torch no genera nada, observa lo que pasa. Se usan juntos: traceroute dice hasta dónde llega, Torch muestra si el paquete pasa por una interfaz.
  - Source: https://www.wirelessnetware.ca/blog/traceroute-torch-powerful-troubleshooting-duo/  Quote: "Torch does not generate, send or receive packets"
  - Kind: definition
  - Level: foundation
  - Bias: vende cursos MTCNA.

## T16 Port forwarding para NVR y cámaras
- b:N40. En el mismo hilo la cámara estaba publicada en el puerto 80 de la IP pública. La regla corregida usa dst-address-type=local pero excluye la IP LAN del router (dst-address=!192.168.88.1) para no secuestrar el acceso al propio router desde adentro. Más abajo otro usuario lista que tiene "servidores y cámaras" publicados por puertos con el nombre de IP Cloud.
  - Source: https://forum.mikrotik.com/t/solved-hairpin-nat-not-working/97689  Quote: "dst-address-type=local dst-address=!192.168.88.1"
  - Kind: story
  - Level: core
- b:N41. Si se publica algo, solo los puertos activamente necesarios, con HTTPS y autenticación, restringidos a IPs de administradores cuando se pueda.
  - Source: https://mkcontroller.com/blog/remote_access/mikrotik/remote_mikrotik_management_via_vps  Quote: "Expose only the ports you actively need"
  - Kind: rule of thumb
  - Level: core

## Disagreements seen
- Firewall: https://forum.mikrotik.com/t/trying-to-understand-defconf-firewall/267442 recoge dos escuelas (dejar la defconf y abrir agujeros, contra reescribir con drop final explícito); la documentación https://manual.mikrotik.com/docs/7.25/getting-started/first-time-configuration dice no tocar las reglas existentes.
- Failover: https://help.mikrotik.com/docs/spaces/ROS/pages/26476608/Failover+WAN+Backup enseña rutas recursivas con check-gateway; https://mkcontroller.com/blog/tutorials/mikrotik/mikrotik-dual-wan-failover-isp-guide/ las considera lentas (20 a 30 s) y suma Netwatch.
- Acceso remoto: securing-your-router propone WireGuard; https://cloudzy.com/de/blog/mikrotik-l2tp-vpn/ defiende L2TP/IPsec por compatibilidad nativa; https://mkcontroller.com/blog/remote_access/mikrotik/remote_mikrotik_management_via_vps propone túnel saliente a un VPS para sitios con CGNAT.
- Contraseña fuerte: la documentación la pone primero; el honeypot de https://www.gendigital.com/blog/insights/research/meris-and-trickbot-standing-on-the-shoulders-of-giants muestra que una contraseña fuerte no sirvió con una versión vulnerable expuesta.
- Port forwarding: el foro de hairpin trata publicar cámaras como normal; MikroTik y CSO empujan a no exponer.

## Best stories
- Honeypot comprometido en 15 minutos pese a contraseña fuerte, por versión vieja de WinBox expuesta. https://www.gendigital.com/blog/insights/research/meris-and-trickbot-standing-on-the-shoulders-of-giants
- Más de 2 millones de MikroTik con gestión expuesta, unos 300.000 vulnerables (Eclypsium). https://www.csoonline.com/article/3644469/researchers-warn-about-continuous-abuse-of-unpatched-mikrotik-routers.html
- La cámara que andaba desde afuera y no desde adentro, por un in-interface de más. https://forum.mikrotik.com/t/solved-hairpin-nat-not-working/97689
- Portal cautivo en blanco resuelto con una captura: 20 dominios ocultos. https://admiralplatform.com/tips4tiks-packet-capture-with-mikrotik/
- El script de backup que registró solo el cambio de credenciales PPPoE del ISP. https://xtremeownage.com/blog/2025/mikrotik-backup-script/
