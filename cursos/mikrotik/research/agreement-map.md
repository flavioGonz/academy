# Agreement map: MikroTik RouterOS 7 para integradores

Fuentes: 26 páginas (13 oficiales de MikroTik, 3 del foro oficial, 10 de practicantes y prensa de seguridad). Notas: research/notes/a.md (61) y b.md (41).
M por subtema = páginas distintas con al menos una nota en ese subtema (incluye líneas Also):
T01 3 · T02 4 · T03 3 · T04 7 · T05 4 · T06 2 · T07 4 · T08 4 · T09 3 · T10 3 · T11 7 · T12 3 · T13 3 · T14 6 · T15 6 · T16 6.

## TH01 Arrancá por Winbox con MAC desde un puerto LAN y trabajá en Safe Mode
- Sub-topic: T01 (also T13)
- Agree: 3 of 3. Notes: a:N1, a:N3, a:N4, b:N1. Urls: https://manual.mikrotik.com/docs/7.25/getting-started/first-time-configuration, https://help.mikrotik.com/docs/spaces/ROS/pages/328155/Configuration+Management, https://forum.mikrotik.com/t/trying-to-understand-defconf-firewall/267442
- Disagree: none found
- Level: foundation
- Best story: Safe Mode deshace todo si se corta la sesión, salvo que pases de 100 acciones (https://help.mikrotik.com/docs/spaces/ROS/pages/328155/Configuration+Management)

## TH02 Conservá la configuración por defecto salvo que vayas a reconstruir todo a conciencia
- Sub-topic: T02 (also T08)
- Agree: 3 of 4. Notes: a:N5, a:N36, a:N2. Urls: https://manual.mikrotik.com/docs/7.25/getting-started/first-time-configuration, https://help.mikrotik.com/docs/spaces/ROS/pages/328155/Configuration+Management, https://forum.mikrotik.com/t/trying-to-understand-defconf-firewall/267442
- Disagree: https://forum.mikrotik.com/t/using-routeros-to-vlan-your-network/126489: arma todo desde cero con su propia VLAN de gestión; en el foro de defconf una escuela reemplaza el final del firewall por un drop explícito.
- Level: foundation
- Best story: los CCR vienen sin defconf, así que la decisión existe igual (https://manual.mikrotik.com/docs/7.25/getting-started/first-time-configuration)

## TH03 Conocé las salidas de emergencia: reset con criterio, botón y Netinstall
- Sub-topic: T02 (also T14)
- Agree: 3 of 4. Notes: a:N6, a:N7, a:N8, a:N9. Urls: https://help.mikrotik.com/docs/spaces/ROS/pages/328155/Configuration+Management, https://help.mikrotik.com/docs/display/ROS/RouterBOOT, https://help.mikrotik.com/docs/spaces/ROS/pages/328142/Upgrading+and+installation
- Disagree: none found
- Level: core
- Best story: el botón tiene tres tiempos: 5 s reset, 10 s CAP, 15 s Netinstall (https://help.mikrotik.com/docs/display/ROS/RouterBOOT)

## TH04 Un usuario por técnico, admin deshabilitado, grupos mínimos
- Sub-topic: T03
- Agree: 3 of 3. Notes: a:N10, a:N11, a:N12, a:N13, b:N2. Urls: https://manual.mikrotik.com/docs/7.25/getting-started/first-time-configuration, https://manual.mikrotik.com/docs/7.25/getting-started/securing-your-router, https://xtremeownage.com/blog/2025/mikrotik-backup-script/
- Disagree: none found
- Level: foundation
- Best story: el grupo read de fábrica puede reiniciar y ver configuración sensible (https://manual.mikrotik.com/docs/7.25/getting-started/securing-your-router)

## TH05 Nunca expongas WinBox, SSH ni API a internet
- Sub-topic: T04 (also T11)
- Agree: 7 of 7. Notes: a:N14, a:N19, b:N3, b:N4, b:N5, b:N7, a:N47. Urls: https://manual.mikrotik.com/docs/7.25/getting-started/securing-your-router, https://manual.mikrotik.com/docs/7.25/getting-started/first-time-configuration, https://mikrotik.com/supportsec/meris-botnet, https://www.csoonline.com/article/3644469/researchers-warn-about-continuous-abuse-of-unpatched-mikrotik-routers.html, https://www.gendigital.com/blog/insights/research/meris-and-trickbot-standing-on-the-shoulders-of-giants, https://securityaffairs.com/122218/malware/meris-bot-mikrotik-routers.html, https://www.securityweek.com/mikrotik-confirms-meris-botnet-targets-routers-compromised-years-ago/
- Disagree: securing-your-router documenta cómo abrir gestión desde WAN "cuando es inevitable" (ISP), restringido por origen.
- Level: foundation
- Best story: honeypot comprometido en 15 minutos pese a contraseña fuerte (https://www.gendigital.com/blog/insights/research/meris-and-trickbot-standing-on-the-shoulders-of-giants)

## TH06 Apagá los servicios que no usás y restringí los que quedan
- Sub-topic: T04
- Agree: 3 of 7. Notes: a:N15, a:N16, a:N18, a:N23, a:N50, b:N8. Urls: https://manual.mikrotik.com/docs/7.25/getting-started/securing-your-router, https://manual.mikrotik.com/docs/7.25/getting-started/first-time-configuration, https://www.securityweek.com/mikrotik-confirms-meris-botnet-targets-routers-compromised-years-ago/
- Disagree: available-from en /ip service vs firewall: la propia documentación prefiere el firewall porque corta antes.
- Level: foundation
- Best story: SOCKS en 5678 era la marca de los routers de Mēris (https://www.gendigital.com/blog/insights/research/meris-and-trickbot-standing-on-the-shoulders-of-giants)

## TH07 Actualizar no alcanza si ya te robaron la contraseña: cambiala y auditá scheduler, SOCKS y firewall
- Sub-topic: T04 (also T14)
- Agree: 5 of 7. Notes: a:N19, a:N20, b:N8, b:N9. Urls: https://mikrotik.com/supportsec/meris-botnet, https://www.securityweek.com/mikrotik-confirms-meris-botnet-targets-routers-compromised-years-ago/, https://securityaffairs.com/122218/malware/meris-bot-mikrotik-routers.html, https://www.csoonline.com/article/3644469/researchers-warn-about-continuous-abuse-of-unpatched-mikrotik-routers.html, https://www.gendigital.com/blog/insights/research/meris-and-trickbot-standing-on-the-shoulders-of-giants
- Disagree: none found
- Level: core
- Best story: Mēris: routers parchados en 2018 pero con la contraseña ya robada (https://mikrotik.com/supportsec/meris-botnet)

## TH08 No confíes en la LAN: el ataque también viene de adentro
- Sub-topic: T04
- Agree: 2 of 7. Notes: a:N20, b:N9. Urls: https://mikrotik.com/supportsec/meris-botnet, https://www.csoonline.com/article/3644469/researchers-warn-about-continuous-abuse-of-unpatched-mikrotik-routers.html
- Disagree: none found
- Level: core
- Best story: Glupteba atacaba el router desde PCs Windows de la LAN (https://www.csoonline.com/article/3644469/researchers-warn-about-continuous-abuse-of-unpatched-mikrotik-routers.html)

## TH09 Trabajá con interface lists LAN y WAN, no con nombres de puerto
- Sub-topic: T05 (also T07)
- Agree: 3 of 4. Notes: a:N21, a:N22, b:N1, b:N10. Urls: https://manual.mikrotik.com/docs/7.25/getting-started/first-time-configuration, https://help.mikrotik.com/docs/spaces/ROS/pages/328513/Building+Advanced+Firewall, https://forum.mikrotik.com/t/trying-to-understand-defconf-firewall/267442
- Disagree: none found
- Level: foundation
- Best story: detect-internet que reescribe las listas sin avisar (https://forum.mikrotik.com/t/trying-to-understand-defconf-firewall/267442)

## TH10 Verificá en dos pasos: IP primero, nombre después
- Sub-topic: T06 (also T15)
- Agree: 1 of 2. Thin evidence. Notes: a:N24, a:N25. Urls: https://manual.mikrotik.com/docs/7.25/getting-started/first-time-configuration
- Disagree: none found
- Level: foundation
- Best story: none

## TH11 Una VLAN, un rango, un DHCP
- Sub-topic: T06 (also T09)
- Agree: 2 of 2. Thin evidence. Notes: a:N26, b:N18. Urls: https://manual.mikrotik.com/docs/7.25/bridging-and-switching/user-guides/bridge-vlan-table, https://forum.mikrotik.com/t/using-routeros-to-vlan-your-network/126489
- Disagree: none found
- Level: core
- Best story: none

## TH12 Masquerade para WAN dinámica, src-nat para IP fija, y uno por cada salida
- Sub-topic: T07 (also T10)
- Agree: 3 of 4. Notes: a:N28, a:N44, b:N27. Urls: https://manual.mikrotik.com/docs/7.25/firewall-and-quality-of-service/firewall/nat, https://help.mikrotik.com/docs/spaces/ROS/pages/26476608/Failover+WAN+Backup, https://mkcontroller.com/blog/tutorials/mikrotik/mikrotik-dual-wan-failover-isp-guide/
- Disagree: none found
- Level: core
- Best story: none

## TH13 Después de tocar NAT, limpiá las conexiones antes de decir que no anda
- Sub-topic: T07
- Agree: 1 of 4. Thin evidence. Notes: a:N27. Urls: https://manual.mikrotik.com/docs/7.25/firewall-and-quality-of-service/firewall/nat
- Disagree: none found
- Level: core
- Best story: none

## TH14 Input protege al router, forward protege a la LAN
- Sub-topic: T08
- Agree: 3 of 4. Notes: a:N33, b:N13, b:N16. Urls: https://help.mikrotik.com/docs/spaces/ROS/pages/328513/Building+Advanced+Firewall, https://forum.mikrotik.com/t/trying-to-understand-defconf-firewall/267442, https://manual.mikrotik.com/docs/7.25/getting-started/first-time-configuration
- Disagree: none found
- Level: foundation
- Best story: regla 7 "drop all from WAN not DSTNATed" frena a vecinos del ISP que inyectan paquetes a tu LAN (https://forum.mikrotik.com/t/trying-to-understand-defconf-firewall/267442)

## TH15 El orden de las reglas es la regla: lo permitido va arriba del drop
- Sub-topic: T08 (also T04)
- Agree: 3 of 4. Notes: b:N15, b:N16, a:N17. Urls: https://forum.mikrotik.com/t/trying-to-understand-defconf-firewall/267442, https://manual.mikrotik.com/docs/7.25/getting-started/securing-your-router, https://help.mikrotik.com/docs/spaces/ROS/pages/328513/Building+Advanced+Firewall
- Disagree: none found
- Level: foundation
- Best story: las reglas de WAN agregadas al final con add nunca coinciden porque el drop de defconf las tapa (https://manual.mikrotik.com/docs/7.25/getting-started/securing-your-router)

## TH16 Agrupá direcciones en address-lists y referí las reglas a la lista
- Sub-topic: T08 (also T16)
- Agree: 2 of 4. Notes: a:N34, b:N41. Urls: https://help.mikrotik.com/docs/spaces/ROS/pages/328513/Building+Advanced+Firewall, https://mkcontroller.com/blog/remote_access/mikrotik/remote_mikrotik_management_via_vps
- Disagree: none found
- Level: core
- Best story: none

## TH17 No bloquees ICMP entero
- Sub-topic: T08
- Agree: 2 of 4. Notes: b:N17, a:N33. Urls: https://forum.mikrotik.com/t/trying-to-understand-defconf-firewall/267442, https://help.mikrotik.com/docs/spaces/ROS/pages/328513/Building+Advanced+Firewall
- Disagree: none found
- Level: core
- Best story: none

## TH18 Defconf o drop explícito: elegí una escuela de firewall
- Sub-topic: T08
- Agree: 2 of 4 (cada escuela). Notes: b:N14, b:N15, a:N36. Urls: https://forum.mikrotik.com/t/trying-to-understand-defconf-firewall/267442, https://manual.mikrotik.com/docs/7.25/getting-started/first-time-configuration
- Disagree: es en sí la división (ver splits).
- Level: advanced
- Best story: none

## TH19 Activá vlan-filtering al final, con la gestión ya resuelta
- Sub-topic: T09
- Agree: 2 of 3. Notes: a:N37, b:N21. Urls: https://manual.mikrotik.com/docs/7.25/bridging-and-switching/user-guides/bridge-vlan-table, https://forum.mikrotik.com/t/using-routeros-to-vlan-your-network/126489
- Disagree: none found
- Level: core
- Best story: la advertencia oficial de quedar afuera, y la sugerencia de usar un puerto fuera del bridge (https://manual.mikrotik.com/docs/7.25/bridging-and-switching/user-guides/bridge-vlan-table)

## TH20 Access sin etiqueta, trunk solo etiquetado, ingress-filtering en todos
- Sub-topic: T09
- Agree: 2 of 3. Notes: a:N38, a:N40, b:N19. Urls: https://manual.mikrotik.com/docs/7.25/bridging-and-switching/user-guides/bridge-vlan-table, https://forum.mikrotik.com/t/using-routeros-to-vlan-your-network/126489
- Disagree: none found
- Level: core
- Best story: varias VLAN en una entrada access filtran tráfico entre VLANs (https://manual.mikrotik.com/docs/7.25/bridging-and-switching/user-guides/bridge-vlan-table)

## TH21 Gestión por una VLAN dedicada, nunca por la 1 ni sin etiqueta
- Sub-topic: T09 (also T05)
- Agree: 2 of 3. Notes: a:N39, a:N41, b:N18, b:N10. Urls: https://manual.mikrotik.com/docs/7.25/bridging-and-switching/user-guides/bridge-vlan-table, https://forum.mikrotik.com/t/using-routeros-to-vlan-your-network/126489
- Disagree: mkx en el hilo prefiere no tener VLAN nativa en absoluto; es matiz, no oposición.
- Level: core
- Best story: PVID 1 en trunk y bridge deja una puerta sin etiqueta al router (https://manual.mikrotik.com/docs/7.25/bridging-and-switching/user-guides/bridge-vlan-table)

## TH22 Verificá la VLAN con Torch en el puerto padre
- Sub-topic: T09 (also T15)
- Agree: 1 of 3. Thin evidence. Notes: a:N60. Urls: https://manual.mikrotik.com/docs/7.25/diagnostics-monitoring-and-troubleshooting/torch
- Disagree: none found
- Level: advanced
- Best story: none

## TH23 Failover con rutas recursivas a hosts testigo, no al gateway del módem
- Sub-topic: T10
- Agree: 2 of 3. Notes: a:N42, a:N43, b:N22, b:N26. Urls: https://help.mikrotik.com/docs/spaces/ROS/pages/26476608/Failover+WAN+Backup, https://mkcontroller.com/blog/tutorials/mikrotik/mikrotik-dual-wan-failover-isp-guide/
- Disagree: https://mkcontroller.com/blog/tutorials/mikrotik/mikrotik-dual-wan-failover-isp-guide/: check-gateway tarda 20 a 30 s y no ve pérdida parcial; suma Netwatch.
- Level: advanced
- Best story: un solo testigo es frágil, dos por enlace (https://help.mikrotik.com/docs/spaces/ROS/pages/26476608/Failover+WAN+Backup)

## TH24 Probá el failover tirando del cable y avisate cuando quedás en el respaldo
- Sub-topic: T10
- Agree: 1 of 3. Thin evidence. Notes: b:N25. Urls: https://mkcontroller.com/blog/tutorials/mikrotik/mikrotik-dual-wan-failover-isp-guide/
- Disagree: none found
- Level: core
- Best story: "un failover que nadie nota es un costo" (https://mkcontroller.com/blog/tutorials/mikrotik/mikrotik-dual-wan-failover-isp-guide/)

## TH25 Para gestión remota, VPN; WireGuard como primera opción
- Sub-topic: T11 (also T04)
- Agree: 4 of 7. Notes: a:N14, a:N45, a:N46, a:N49. Urls: https://manual.mikrotik.com/docs/7.25/getting-started/securing-your-router, https://help.mikrotik.com/docs/spaces/ROS/pages/69664792/WireGuard, https://manual.mikrotik.com/docs/7.25/network-management/cloud/, https://mikrotik.com/supportsec/meris-botnet
- Disagree: https://cloudzy.com/de/blog/mikrotik-l2tp-vpn/: L2TP/IPsec por cliente nativo sin instalar nada; el aviso de Mēris nombra IPsec.
- Level: core
- Best story: none

## TH26 L2TP/IPsec cuando el cliente no puede instalar nada: puertos, required y FastTrack
- Sub-topic: T11
- Agree: 2 of 7. Notes: b:N29, b:N30, b:N31, a:N35. Urls: https://cloudzy.com/de/blog/mikrotik-l2tp-vpn/, https://help.mikrotik.com/docs/spaces/ROS/pages/328513/Building+Advanced+Firewall
- Disagree: none found
- Level: advanced
- Best story: none

## TH27 Sitio con CGNAT: túnel saliente o Back To Home, porque el port forwarding no existe
- Sub-topic: T11 (also T16)
- Agree: 3 of 7. Notes: a:N31, a:N49, b:N28. Urls: https://manual.mikrotik.com/docs/7.25/firewall-and-quality-of-service/firewall/nat, https://manual.mikrotik.com/docs/7.25/network-management/cloud/, https://mkcontroller.com/blog/remote_access/mikrotik/remote_mikrotik_management_via_vps
- Disagree: none found
- Level: advanced
- Best story: none

## TH28 DDNS de IP Cloud es un nombre, no una puerta
- Sub-topic: T12
- Agree: 2 of 3. Notes: a:N48, a:N49, a:N50. Urls: https://manual.mikrotik.com/docs/7.25/network-management/cloud/, https://manual.mikrotik.com/docs/7.25/getting-started/securing-your-router
- Disagree: https://forum.mikrotik.com/t/solved-hairpin-nat-not-working/97689: usuarios que publican cámaras por puerto detrás del nombre de IP Cloud como práctica normal.
- Level: core
- Best story: none

## TH29 Export en texto para leer y comparar, backup binario para el mismo equipo
- Sub-topic: T13
- Agree: 3 of 3. Notes: a:N51, a:N52, a:N53, b:N33, b:N34. Urls: https://help.mikrotik.com/docs/spaces/ROS/pages/328155/Configuration+Management, https://manual.mikrotik.com/docs/7.25/getting-started/first-time-configuration, https://xtremeownage.com/blog/2025/mikrotik-backup-script/
- Disagree: none found
- Level: core
- Best story: el commit automático que capturó el cambio de credenciales PPPoE (https://xtremeownage.com/blog/2025/mikrotik-backup-script/)

## TH30 Actualizá RouterOS en canal stable o long-term, y después RouterBOOT
- Sub-topic: T14
- Agree: 4 of 6. Notes: a:N54, a:N55, a:N56, a:N57, b:N35. Urls: https://help.mikrotik.com/docs/spaces/ROS/pages/328142/Upgrading+and+installation, https://help.mikrotik.com/docs/display/ROS/RouterBOOT, https://manual.mikrotik.com/docs/7.25/getting-started/securing-your-router, https://www.csoonline.com/article/3644469/researchers-warn-about-continuous-abuse-of-unpatched-mikrotik-routers.html
- Disagree: stable vs long-term no tiene un ganador en las fuentes; la documentación describe ambos.
- Level: core
- Best story: 300.000 equipos vulnerables por no actualizar (https://www.csoonline.com/article/3644469/researchers-warn-about-continuous-abuse-of-unpatched-mikrotik-routers.html)

## TH31 Torch para ver quién usa qué, en la interfaz LAN
- Sub-topic: T15
- Agree: 2 of 6. Notes: a:N58, a:N59, b:N39. Urls: https://manual.mikrotik.com/docs/7.25/diagnostics-monitoring-and-troubleshooting/torch, https://www.wirelessnetware.ca/blog/traceroute-torch-powerful-troubleshooting-duo/
- Disagree: none found
- Level: core
- Best story: none

## TH32 Packet sniffer a .pcap y Wireshark cuando necesitás ver el contenido
- Sub-topic: T15
- Agree: 2 of 6. Notes: b:N36, b:N37, b:N38, a:N58. Urls: https://admiralplatform.com/tips4tiks-packet-capture-with-mikrotik/, https://manual.mikrotik.com/docs/7.25/diagnostics-monitoring-and-troubleshooting/torch
- Disagree: none found
- Level: core
- Best story: portal cautivo en blanco y 20 dominios ocultos (https://admiralplatform.com/tips4tiks-packet-capture-with-mikrotik/)

## TH33 Lo que se ve desde afuera se prueba desde afuera
- Sub-topic: T15 (also T16)
- Agree: 1 of 6. Thin evidence. Notes: b:N12. Urls: https://forum.mikrotik.com/t/solved-hairpin-nat-not-working/97689
- Disagree: none found
- Level: core
- Best story: none

## TH34 Si publicás un NVR, restringí el origen, mínimos puertos y nunca el puerto del router
- Sub-topic: T16 (also T07)
- Agree: 4 of 6. Notes: a:N30, a:N32, b:N40, b:N41, a:N34. Urls: https://manual.mikrotik.com/docs/7.25/firewall-and-quality-of-service/firewall/nat, https://manual.mikrotik.com/docs/7.25/getting-started/first-time-configuration, https://forum.mikrotik.com/t/solved-hairpin-nat-not-working/97689, https://mkcontroller.com/blog/remote_access/mikrotik/remote_mikrotik_management_via_vps
- Disagree: el ejemplo de first-time-configuration publica RDP sin filtrar origen.
- Level: core
- Best story: la cámara que andaba desde afuera y no desde adentro (https://forum.mikrotik.com/t/solved-hairpin-nat-not-working/97689)

## TH35 Hairpin NAT para entrar por la IP pública desde la propia LAN
- Sub-topic: T16 (also T07)
- Agree: 2 of 6. Notes: a:N29, b:N11. Urls: https://manual.mikrotik.com/docs/7.25/firewall-and-quality-of-service/firewall/nat, https://forum.mikrotik.com/t/solved-hairpin-nat-not-working/97689
- Disagree: none found
- Level: advanced
- Best story: el servidor que contesta directo y el cliente que tira la respuesta (https://manual.mikrotik.com/docs/7.25/firewall-and-quality-of-service/firewall/nat)

Totales por nivel: foundation 10, core 19, advanced 6.

## The big splits
- Firewall por defecto vs drop explícito: la documentación (https://manual.mikrotik.com/docs/7.25/getting-started/first-time-configuration) y una escuela del foro dicen no tocar la defconf y abrir agujeros; la otra escuela (https://forum.mikrotik.com/t/trying-to-understand-defconf-firewall/267442) reescribe con un drop final y permisos explícitos. Gira en torno a legibilidad vs riesgo de romper algo.
- Detección de caída de WAN: rutas recursivas con check-gateway (https://help.mikrotik.com/docs/spaces/ROS/pages/26476608/Failover+WAN+Backup) contra Netwatch con scripts (https://mkcontroller.com/blog/tutorials/mikrotik/mikrotik-dual-wan-failover-isp-guide/). Gira en torno a velocidad de detección vs simplicidad y cero scripts.
- VPN de gestión: WireGuard (https://manual.mikrotik.com/docs/7.25/getting-started/securing-your-router) vs L2TP/IPsec nativo (https://cloudzy.com/de/blog/mikrotik-l2tp-vpn/) vs túnel saliente a VPS (https://mkcontroller.com/blog/remote_access/mikrotik/remote_mikrotik_management_via_vps). Gira en torno a qué cliente hay del otro lado y si el sitio tiene IP pública.
- Publicar cámaras por puerto: práctica corriente en el foro (https://forum.mikrotik.com/t/solved-hairpin-nat-not-working/97689) vs no exponer nada y entrar por VPN (https://mikrotik.com/supportsec/meris-botnet). Gira en torno a quién necesita ver las cámaras y desde qué app.
- Desde cero vs defconf: la guía de VLAN del foro (https://forum.mikrotik.com/t/using-routeros-to-vlan-your-network/126489) arranca limpio; la documentación recomienda defconf a principiantes.

## Coverage gaps
- T06 DHCP y DNS: solo 2 páginas; nada sobre reservas estáticas (leases), opciones DHCP ni DNS estático, que un integrador usa para NVR y cámaras.
- Logs: ninguna página dedicada a /system logging ni a enviar logs a un syslog remoto; solo menciones.
- WebFig y SSH como herramientas: casi sin cobertura propia más allá de securing-your-router.
- Port forwarding específico de NVR (puertos de Hikvision o Dahua, RTSP 554): no hay página leída que liste puertos de fabricantes; el curso usa puertos de ejemplo.
- L2TP/IPsec: la única guía práctica es de un proveedor de VPS (sesgo comercial) y en alemán.
- Netwatch: solo descrito por un practicante con producto propio; sin página oficial leída.

# Ampliación (octubre 2026): conexión a internet, software y acceso remoto

Fuentes nuevas: 20 páginas (6 de manual.mikrotik.com 7.25, 3 de antel.com.uy, 2 del foro uruguayo macacos, 1 de soporte de Montevideo COMM, 1 de Microsoft Learn, 7 de practicantes). Notas: research/notes/c.md (60), que también relee páginas del lote original.
M por subtema nuevo: T17 5 · T18 3 · T19 8 · T20 3 · T21 5 · T22 3 · T23 6 · T24 3. T12 sube a 5 con las notas nuevas.

## TH36 Con IP fija, cargá a mano dirección, ruta por defecto y DNS, y verificá cada uno
- Sub-topic: T17
- Agree: 3 of 5. Notes: c:N2, c:N17, c:N18. Urls: https://manual.mikrotik.com/docs/7.25/getting-started/first-time-configuration, https://antel.com.uy/empresas/internet-y-fija/planes/internet-pyme, https://antel.com.uy/empresas/internet-y-fija/planes/internet-corporativo
- Disagree: none found
- Level: foundation
- Best story: Antel Internet corporativo entrega hasta 29 IPs fijas en un /27 sobre un RJ45, con un router que administra Antel (https://antel.com.uy/empresas/internet-y-fija/planes/internet-corporativo)

## TH37 Masquerade para IP dinámica; con IP fija, src-nat es una opción con cuidado en multi WAN
- Sub-topic: T17 (also T10)
- Agree: 1 of 5. Notes: c:N3. Urls: https://manual.mikrotik.com/docs/7.25/firewall-and-quality-of-service/firewall/nat
- Disagree: none found
- Level: core
- Best story: con src-nat y dos enlaces, al volver el principal se pueden filtrar IPs privadas a internet (https://manual.mikrotik.com/docs/7.25/firewall-and-quality-of-service/firewall/nat)

## TH38 Rutas recursivas solo con gateway estable; con DHCP o PPPoE, script de lease o Netwatch
- Sub-topic: T17 (also T18, T10)
- Agree: 2 of 5. Notes: c:N8, c:N7. Urls: https://mkcontroller.com/blog/tutorials/mikrotik/mikrotik-dual-wan-failover-isp-guide/, https://manual.mikrotik.com/docs/7.25/network-management/dhcp/client/
- Disagree: none found
- Level: core
- Best story: none

## TH39 Con DHCP cliente, leé qué instaló: dirección, ruta, DNS y NTP, y que el estado sea bound
- Sub-topic: T18
- Agree: 2 of 3. Notes: c:N1, c:N4, c:N5. Urls: https://manual.mikrotik.com/docs/7.25/getting-started/first-time-configuration, https://manual.mikrotik.com/docs/7.25/network-management/dhcp/client/
- Disagree: none found
- Level: foundation
- Best story: si el servidor manda la opción 121, el gateway de la opción 3 se ignora y la ruta por defecto puede no aparecer (https://manual.mikrotik.com/docs/7.25/network-management/dhcp/client/)

## TH40 Elegí qué ruta por defecto gana con default-route-distance; distancias iguales reparten tráfico
- Sub-topic: T18 (also T10)
- Agree: 2 of 3. Notes: c:N6, c:N8. Urls: https://manual.mikrotik.com/docs/7.25/network-management/dhcp/client/, https://mkcontroller.com/blog/tutorials/mikrotik/mikrotik-dual-wan-failover-isp-guide/
- Disagree: none found
- Level: core
- Best story: none

## TH41 Si la WAN por DHCP tiene IP privada, hay otro NAT adelante: comparalo con public-address
- Sub-topic: T18 (also T12)
- Agree: 1 of 3 en este lote. Notes: c:N30. Urls: https://manual.mikrotik.com/docs/7.25/network-management/cloud/ (se apoya en TH28 del mapa original, 2 de 3)
- Disagree: none found
- Level: core
- Best story: none

## TH42 En PPPoE, MTU y MRU hasta 1492 y MSS ajustado
- Sub-topic: T19
- Agree: 2 of 8. Notes: c:N9, c:N12. Urls: https://manual.mikrotik.com/docs/7.25/virtual-private-networks/pppoe/, https://getlabsdone.com/how-to-configure-pppoe-in-mikrotik-router/
- Disagree: none found (las páginas de Antel no publican MTU)
- Level: core
- Best story: páginas que cargan a medias con PPPoE hasta que se activa Change TCP MSS (https://getlabsdone.com/how-to-configure-pppoe-in-mikrotik-router/)

## TH43 Con PPPoE la WAN pasa a ser pppoe-out1: NAT, listas y reglas apuntan ahí
- Sub-topic: T19
- Agree: 2 of 8. Notes: c:N11, c:N12. Urls: https://manual.mikrotik.com/docs/7.25/getting-started/first-time-configuration, https://getlabsdone.com/how-to-configure-pppoe-in-mikrotik-router/
- Disagree: none found
- Level: foundation
- Best story: conectado al proveedor pero la LAN sin internet porque el masquerade seguía por ether1 (https://getlabsdone.com/how-to-configure-pppoe-in-mikrotik-router/)

## TH44 VLAN en la WAN solo si el proveedor la indica; el PPPoE va sobre la interfaz VLAN
- Sub-topic: T19
- Agree: 1 of 8. Notes: c:N12. Urls: https://getlabsdone.com/how-to-configure-pppoe-in-mikrotik-router/
- Disagree: none found. Para Antel ninguna página leída confirma ni descarta una VLAN con el ONT en modo puente.
- Level: core
- Best story: none

## TH45 Con Antel, el ONT en modo puente se pide a Antel y el MikroTik hace el PPPoE con las credenciales del servicio
- Sub-topic: T19
- Agree: 3 of 8. Notes: c:N13, c:N15, c:N16. Urls: https://antel.com.uy/personas/preguntas-frecuentes/internet, https://www.macacos.com.uy/foros/viewtopic.php?id=17924, https://foros.montevideocomm.uy/forum/accesorios-wifi-15/question/configuracion-de-router-tp-link-wr941hp-523
- Disagree: https://www.macacos.com.uy/foros/viewtopic.php?id=17622: en 2017 varios usuarios tuvieron cortes con el ONT en puente y volvieron a modo router con su equipo por DHCP detrás (doble NAT).
- Level: core
- Best story: "en fibra lo hacen ellos": el cambio de modo lo hace el proveedor de forma remota (https://www.macacos.com.uy/foros/viewtopic.php?id=17622)

## TH46 La IP de PPPoE o DHCP cambia al reconectar: masquerade en la WAN y DDNS para seguirla
- Sub-topic: T12 (also T19)
- Agree: 2 of 5. Notes: c:N3, c:N29. Urls: https://manual.mikrotik.com/docs/7.25/firewall-and-quality-of-service/firewall/nat, https://manual.mikrotik.com/docs/7.25/network-management/cloud/
- Disagree: none found
- Level: core
- Best story: none

## TH47 Paquetes: routeros trae casi todo; los extras se habilitan, se aplican con reinicio y se confirman en el log
- Sub-topic: T20
- Agree: 2 of 3. Notes: c:N20, c:N21, c:N22, c:N23. Urls: https://manual.mikrotik.com/docs/7.25/getting-started/installation-and-upgrade/packages/, https://help.mikrotik.com/docs/spaces/ROS/pages/328142/Upgrading+and+installation
- Disagree: none found
- Level: core
- Best story: desde 7.13 wireless y wifi-qcom no pueden estar activos a la vez (https://manual.mikrotik.com/docs/7.25/getting-started/installation-and-upgrade/packages/)

## TH48 Sin internet en el router: .npk de la arquitectura correcta en la raíz de Files y reinicio
- Sub-topic: T20 (also T14)
- Agree: 2 of 3. Notes: c:N23, c:N20, c:N25. Urls: https://help.mikrotik.com/docs/spaces/ROS/pages/328142/Upgrading+and+installation, https://manual.mikrotik.com/docs/7.25/getting-started/installation-and-upgrade/packages/
- Disagree: none found
- Level: core
- Best story: el paquete subido dentro de una carpeta (por ejemplo la de hotspot) no se instala (https://help.mikrotik.com/docs/spaces/ROS/pages/328142/Upgrading+and+installation)

## TH49 Para volver atrás: .npk de la versión anterior y /system/package/downgrade, o un canal con versión más vieja
- Sub-topic: T20 (also T14)
- Agree: 2 of 3. Notes: c:N24. Urls: https://manual.mikrotik.com/docs/7.25/getting-started/installation-and-upgrade/packages/, https://help.mikrotik.com/docs/spaces/ROS/pages/328142/Upgrading+and+installation
- Disagree: none found
- Level: core
- Best story: none

## TH50 Sitios de clientes en long-term; stable solo si necesitás una función; testing y development nunca
- Sub-topic: T20 (also T14)
- Agree: 2 of 3. Notes: c:N26, c:N27. Urls: https://help.mikrotik.com/docs/spaces/ROS/pages/328142/Upgrading+and+installation, https://blog.linitx.com/mikrotik-routeros-package-channel-bugfix-only-current-release-candidate-legacy/
- Disagree: la documentación describe los canales sin recomendar uno y ofrece un script de actualización automática (c:N28); el distribuidor recomienda la rama de solo arreglos para producción.
- Level: foundation
- Best story: una versión candidata puede dejar el equipo recuperable solo por Netinstall (https://blog.linitx.com/mikrotik-routeros-package-channel-bugfix-only-current-release-candidate-legacy/)

## TH51 Back To Home para sitios sin IP pública con equipos ARM: un usuario por dispositivo y LAN solo a quien la necesita
- Sub-topic: T24
- Agree: 2 of 3. Notes: c:N33, c:N34, c:N38, c:N60. Urls: https://manual.mikrotik.com/docs/7.25/network-management/cloud/back-to-home/, https://www.wirelessnetware.ca/blog/back-to-home-with-mikrotik/, https://manual.mikrotik.com/docs/7.25/network-management/cloud/
- Disagree: none found
- Level: core
- Best story: los RouterBOARD MIPS quedan afuera de Back To Home (https://www.wirelessnetware.ca/blog/back-to-home-with-mikrotik/)

## TH52 Back To Home depende de la lista LAN y revocarlo borra todos los usuarios y claves
- Sub-topic: T24
- Agree: 1 of 3. Notes: c:N35, c:N36. Urls: https://manual.mikrotik.com/docs/7.25/network-management/cloud/back-to-home/
- Disagree: none found
- Level: core
- Best story: none

## TH53 Back To Home para lo simple; WireGuard a mano cuando necesitás control fino
- Sub-topic: T24 (also T11)
- Agree: 1 of 3. Notes: c:N37. Urls: https://manual.mikrotik.com/docs/7.25/network-management/cloud/back-to-home/
- Disagree: none found
- Level: core
- Best story: none

## TH54 Un CHR en un VPS como punto de encuentro: los sitios llaman al hub, el CGNAT deja de importar
- Sub-topic: T21 (also T11)
- Agree: 2 of 5. Notes: c:N42, c:N43. Urls: https://mkcontroller.com/blog/remote_access/mikrotik/remote_mikrotik_management_via_vps, https://mikrotikdocs.fyi/virtual-private-networks/home-cottage-wireguard/
- Disagree: MKController empuja su servicio en la nube como alternativa al VPS propio (sesgo comercial).
- Level: core
- Best story: none

## TH55 Licencia CHR sin trampas: Free sirve para laboratorio, P1 para un hub con tráfico, prueba de 60 días con cuenta
- Sub-topic: T21
- Agree: 1 of 5 (fuente primaria). Notes: c:N39, c:N40. Urls: https://manual.mikrotik.com/docs/7.25/getting-started/routeros-licensing/chr/chr-licensing/
- Disagree: none found
- Level: core
- Best story: las copias de un CHR no reinician la prueba; IP Cloud requiere licencia paga (https://manual.mikrotik.com/docs/7.25/getting-started/routeros-licensing/chr/chr-licensing/)

## TH56 Endurecé el CHR antes que nada: arranca con admin sin contraseña en una IP pública
- Sub-topic: T21 (also T03, T04)
- Agree: 2 of 5. Notes: c:N41, c:N42. Urls: https://community.hetzner.com/tutorials/mikrotik-chr-basic-setup, https://mkcontroller.com/blog/remote_access/mikrotik/remote_mikrotik_management_via_vps
- Disagree: none found
- Level: foundation
- Best story: instalación con dd desde el sistema de rescate del VPS (https://community.hetzner.com/tutorials/mikrotik-chr-basic-setup)

## TH57 L2TP siempre con IPsec obligatorio, y en input UDP 500, 4500, 1701 y ESP
- Sub-topic: T22
- Agree: 2 of 3. Notes: c:N45, c:N46, c:N47. Urls: https://manual.mikrotik.com/docs/7.25/virtual-private-networks/ipsec/, https://cloudzy.com/de/blog/mikrotik-l2tp-vpn/
- Disagree: none found
- Level: core
- Best story: none

## TH58 Si Windows no conecta y el celular sí, mirá la clave de registro de NAT-T
- Sub-topic: T22
- Agree: 2 of 3. Notes: c:N48, c:N47. Urls: https://learn.microsoft.com/en-us/troubleshoot/windows-server/networking/configure-l2tp-ipsec-server-behind-nat-t-device, https://cloudzy.com/de/blog/mikrotik-l2tp-vpn/
- Disagree: none found
- Level: core
- Best story: valor 2 cuando servidor y cliente están detrás de NAT (https://learn.microsoft.com/en-us/troubleshoot/windows-server/networking/configure-l2tp-ipsec-server-behind-nat-t-device)

## TH59 Antes de un IPsec con otra marca, acordá por escrito los parámetros de fase 1 y fase 2
- Sub-topic: T23
- Agree: 3 of 6. Notes: c:N50, c:N57, c:N58. Urls: https://manual.mikrotik.com/docs/7.25/virtual-private-networks/ipsec/, https://mkcontroller.com/blog/remote_access/mikrotik/mikrotik-ipsec-site-to-site-vpn/, https://getlabsdone.com/setup-ipsec-site-to-site-vpn-tunnel-between-pfsense-and-mikrotik/
- Disagree: none found
- Level: core
- Best story: none

## TH60 Sacá el tráfico del túnel del masquerade y de FastTrack
- Sub-topic: T23
- Agree: 4 of 6. Notes: c:N52, c:N55, c:N56, c:N57. Urls: https://manual.mikrotik.com/docs/7.25/virtual-private-networks/ipsec/, https://help.mikrotik.com/docs/spaces/ROS/pages/328513/Building+Advanced+Firewall, https://manual.mikrotik.com/docs/7.25/getting-started/first-time-configuration, https://mkcontroller.com/blog/remote_access/mikrotik/mikrotik-ipsec-site-to-site-vpn/
- Disagree: el método varía: regla srcnat accept arriba de todo (documentación de IPsec, MKController) o ipsec-policy=out,none en el masquerade (primera configuración).
- Level: core
- Best story: el túnel lento que se arregla al prender Torch (https://manual.mikrotik.com/docs/7.25/virtual-private-networks/ipsec/)

## TH61 Diagnosticá por capas: active-peers para fase 1, ph2-state para fase 2, installed-sa y el log ipsec
- Sub-topic: T23 (also T15)
- Agree: 3 of 6. Notes: c:N51, c:N54, c:N57, c:N58, c:N53, c:N59. Urls: https://manual.mikrotik.com/docs/7.25/virtual-private-networks/ipsec/, https://mkcontroller.com/blog/remote_access/mikrotik/mikrotik-ipsec-site-to-site-vpn/, https://getlabsdone.com/setup-ipsec-site-to-site-vpn-tunnel-between-pfsense-and-mikrotik/
- Disagree: none found
- Level: advanced
- Best story: el log muestra cada algoritmo rechazado como local:remoto (https://manual.mikrotik.com/docs/7.25/virtual-private-networks/ipsec/)

## TH62 Preferí IKEv2 y, si se puede, certificados en vez de clave compartida
- Sub-topic: T23 (also T22)
- Agree: 2 of 6. Notes: c:N49, c:N57. Urls: https://manual.mikrotik.com/docs/7.25/virtual-private-networks/ipsec/, https://mkcontroller.com/blog/remote_access/mikrotik/mikrotik-ipsec-site-to-site-vpn/
- Disagree: los ejemplos prácticos (incluido el de L2TP de la propia documentación y la guía de pfSense) usan clave compartida.
- Level: advanced
- Best story: none

## TH63 Antes del túnel: relojes por NTP y subredes que no se pisen
- Sub-topic: T23 (also T21, T12)
- Agree: 2 of 6. Notes: c:N32, c:N44, c:N31. Urls: https://mkcontroller.com/blog/remote_access/mikrotik/mikrotik-ipsec-site-to-site-vpn/, https://manual.mikrotik.com/docs/7.25/network-management/cloud/
- Disagree: none found
- Level: core
- Best story: dos sitios con 192.168.88.0/24 no se pueden unir sin renumerar (https://mkcontroller.com/blog/remote_access/mikrotik/mikrotik-ipsec-site-to-site-vpn/)

Totales de la ampliación por nivel: foundation 5, core 21, advanced 2.

## The big splits (ampliación)
- Canal de producción: la documentación (https://help.mikrotik.com/docs/spaces/ROS/pages/328142/Upgrading+and+installation) no elige y ofrece actualizar solo por script; un distribuidor (https://blog.linitx.com/mikrotik-routeros-package-channel-bugfix-only-current-release-candidate-legacy/) recomienda la rama de solo arreglos. Gira en torno a estabilidad contra funciones nuevas y a cuánto se visita el sitio.
- ONT de Antel en puente o en router: Antel ofrece el puente (https://antel.com.uy/personas/preguntas-frecuentes/internet); usuarios del foro macacos volvieron a modo router con doble NAT por cortes (https://www.macacos.com.uy/foros/viewtopic.php?id=17622). Gira en torno a control y acceso remoto contra simplicidad de soporte.
- Clave compartida o certificados en IPsec: la documentación aconseja evitar PSK; los ejemplos prácticos la usan. Gira en torno a cantidad de túneles y a qué soporta el otro extremo.
- NAT-T encendido o apagado: la guía de pfSense lo apaga con IPs públicas; la de L2TP lo pide encendido si puede haber NAT. Gira en torno a si hay NAT en el camino.
- Back To Home, CHR propio o servicio de terceros para sitios con CGNAT: Back To Home es gratis pero solo ARM y pasa por relays de MikroTik; un CHR propio da control y cuesta licencia y mantenimiento; MKController ofrece su nube (sesgo comercial).

## Coverage gaps (ampliación)
- Antel: ninguna página leída de antel.com.uy publica parámetros para router propio (VLAN, MTU, formato de usuario PPPoE). El único usuario y clave visto es genérico de ADSL en un instructivo de un proveedor de 2020. Los hilos de GameOver Uruguay que tratan el tema no se pudieron leer (protección anti bots). Lo que la lección 15 dice de Antel se limita a lo confirmado; el resto se marca como "a confirmar con Antel".
- IPsec con Fortinet, Cisco y Ubiquiti: solo se leyó una guía con pfSense; un hilo del foro sobre FortiGate quedó fuera por el límite de 3 páginas por sitio. La lección 22 da la tabla de parámetros genérica.
- Instalación de CHR: la guía leída es de Hetzner con una imagen 6.49; las guías oficiales por proveedor existen pero no se agregaron.
- Downgrade: la página oficial que limita el downgrade a la versión de fábrica del equipo no está en raw/ (se llegó al tope de 6 páginas oficiales nuevas); la lección 16 enseña el comando sin afirmar ese límite.
- Netwatch y script de lease para failover con DHCP: solo el ejemplo oficial del script de lease.

## Lección 23 (Safe Mode, octubre 2026)

## TH64 Safe Mode deshace solo si la sesión dueña se corta; Ctrl+X o soltar el botón confirma, Ctrl+D descarta
- Sub-topic: T13 (also T01)
- Agree: 5 of 6. Notes: d:N2, d:N3, d:N5, d:N6, d:N14, d:N16. Urls: https://manual.mikrotik.com/docs/7.25/getting-started/configuration-management/, https://cyberlab.pacific.edu/courses/comp177/resources/routeros-overview, https://forum.mikrotik.com/t/safe-mode-in-webfig/92508, https://mikrotikdocs.fyi/management-tools/winbox-webfig/, https://help.mikrotik.com/docs/spaces/ROS/pages/328134/Command+Line+Interface
- Disagree: mikrotikdocs.fyi describe los cambios como "pendientes" y el timeout como configurable; la documentación no dice eso.
- Level: foundation
- Best story: drop en input en WebFig con Safe Mode, reconecta al minuto sin la regla (https://forum.mikrotik.com/t/safe-mode-in-webfig/92508)

## TH65 Tope de 100 acciones: pasos chicos y alternar Safe Mode entre pasos
- Sub-topic: T13
- Agree: 3 of 4. Notes: d:N8, d:N9, d:N12. Urls: https://manual.mikrotik.com/docs/7.25/getting-started/configuration-management/, https://manual.mikrotik.com/docs/7.25/management-tools/winbox, https://forum.mikrotik.com/t/safe-mode-powercycle-useless/105625
- Disagree: la guía universitaria propone quedarse en Safe Mode todo el laboratorio (https://cyberlab.pacific.edu/courses/comp177/resources/routeros-overview).
- Level: core
- Best story: none

## TH66 Lo que Safe Mode no cubre: corte de energía, cambios que cortan la sesión a propósito, sesiones de otro
- Sub-topic: T13
- Agree: 2 of 4. Notes: d:N10, d:N11, d:N12, d:N13. Urls: https://forum.mikrotik.com/t/safe-mode-powercycle-useless/105625, https://forum.mikrotik.com/t/how-to-execute-risky-mikrotik-commands-safely/165189
- Disagree: la página de CLI dice que en Safe Mode la configuración se escribe en disco al salir (https://help.mikrotik.com/docs/spaces/ROS/pages/328134/Command+Line+Interface), lo que contradice lo que vieron usuarios en 6.40.4 al cortar la energía. Sin confirmación para RouterOS 7.
- Level: advanced
- Best story: quitar la IP en Safe Mode y cortar la energía dejó el cambio aplicado (https://forum.mikrotik.com/t/safe-mode-powercycle-useless/105625)

## Lección 24 (Port forwarding, octubre 2026)

## TH67 dst-nat atado a la entrada (WAN o IP pública) y filtrado por origen
- Sub-topic: T15 (also T05)
- Agree: 5 of 6. Notes: e:N1, e:N2, e:N7, e:N8, e:N11. Urls: https://manual.mikrotik.com/docs/7.25/firewall-and-quality-of-service/firewall/nat, https://forum.mikrotik.com/t/noob-sorry-nat-port-80-breaking-outbound-web/41994, https://forum.mikrotik.com/t/need-help-with-port-forwarding/159605, https://forum.mikrotik.com/t/solved-hairpin-nat-not-working/97689
- Disagree: el ejemplo de primera configuración publica con solo protocolo y puerto (https://manual.mikrotik.com/docs/7.25/getting-started/first-time-configuration).
- Level: foundation
- Best story: la regla con solo dst-port=80 que rompió la navegación de la LAN (https://forum.mikrotik.com/t/noob-sorry-nat-port-80-breaking-outbound-web/41994)

## TH68 El firewall por defecto ya deja pasar lo dst-nateado; con firewall estricto, una regla en forward
- Sub-topic: T15
- Agree: 4 of 4. Notes: e:N4, e:N5, e:N14. Urls: https://forum.mikrotik.com/t/trying-to-understand-defconf-firewall/267442, https://help.mikrotik.com/docs/spaces/ROS/pages/328513/Building+Advanced+Firewall, https://manual.mikrotik.com/docs/7.25/getting-started/first-time-configuration, https://help.mikrotik.com/docs/spaces/ROS/pages/130220087/Connection%2Btracking
- Disagree: none
- Level: core
- Best story: none

## TH69 Puertos de NVR: Hikvision 8000, 554 o 10554, 80 y 443; Dahua 37777 TCP, 37778 UDP, 554, 80 y 443; todos cambiables
- Sub-topic: T16
- Agree: 6 of 7. Notes: e:N16, e:N17, e:N18, e:N19, e:N20, e:N9. Urls: https://learncctv.com/default-ports-for-hikvision-dvr, https://netviewcctv.co.uk/blog/post/ports, https://www.dahuasecurity.com/about-dahua/news-events/notice/how-to-setup-remote-access-for-nvr, https://www.videoexpertsgroup.com/glossary/port-37777, https://forum.mikrotik.com/t/need-help-with-port-forwarding/159605
- Disagree: cuántos puertos alcanzan en Dahua (aviso oficial: HTTP y TCP; integrador del foro: 443, 554, 37777 y 37778 UDP); RTSP de Hikvision en 554 o 10554. La lista oficial de Hikvision no se pudo guardar.
- Level: core
- Best story: login sí, video no, en un NVR Dahua (https://forum.mikrotik.com/t/need-help-with-port-forwarding/159605)

## TH70 Hairpin con masquerade o DNS local; cambiar el puerto no esconde el servicio
- Sub-topic: T15 (also T05)
- Agree: 3 of 4 en hairpin (e:N10, e:N11, e:N12); 2 of 2 en que el puerto no estándar no esconde (e:N22, e:N20 lo propone como medida adicional). Urls: https://manual.mikrotik.com/docs/7.25/firewall-and-quality-of-service/firewall/nat, https://forum.mikrotik.com/t/solved-hairpin-nat-not-working/97689, https://forum.mikrotik.com/t/hairpin-nat-using-local-dns/174370, https://www.modat.io/post/exposed-rtsp
- Disagree: el foro prefiere DNS dividido o subred propia para que el NVR vea la IP real; la documentación enseña el masquerade.
- Level: advanced
- Best story: 973.819 servicios RTSP expuestos en marzo de 2026, 43,9 % fuera del 554 (https://www.modat.io/post/exposed-rtsp)
