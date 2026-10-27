# Mapa de acuerdos: Telefonía IP Grandstream

M por subtema = páginas distintas con al menos una nota (o línea Also) en ese subtema. Notas en research/notes/a.md.
Abreviaturas solo para leer rápido; las urls van completas en cada tema.

## TH01 Cambiá la contraseña de admin al primer ingreso y no confíes en "admin/admin"
- Sub-topic: T01 (also T13)
- Agree: 3 of 4. Notes: a:N3, a:N8, a:N53. Urls: https://documentation.grandstream.com/knowledge-base/ucm6xxx-security-manual/ https://www.simtex.com.au/support/kb/pbx-setup-guides/grandstream-ucm-sip-trunk-configuration https://documentation.grandstream.com/knowledge-base/ucm630x-series-user-manual/
- Disagree: https://support.telnyx.com/en/articles/5748258-grandstream-configuring-sip-trunks-on-your-grandstream-ucm6xxx-series: indica admin/admin como login de fábrica (desactualizado para equipos desde 2017).
- Level: foundation
- Best story: Simtex: dejar admin/admin es de las causas más comunes de centrales comprometidas (https://www.simtex.com.au/support/kb/pbx-setup-guides/grandstream-ucm-sip-trunk-configuration)

## TH02 Elegí el modo de red (Switch, Route, Dual) antes de configurar nada
- Sub-topic: T01 (also T03, T13)
- Agree: 2 of 4. Notes: a:N1, a:N12, a:N55. Urls: https://documentation.grandstream.com/knowledge-base/ucm630x-series-user-manual/ https://documentation.grandstream.com/knowledge-base/zero-config-guide/
- Disagree: none found
- Level: foundation
- Best story: DHCP opción 66 y Dynamic Defense solo funcionan en Route (https://documentation.grandstream.com/knowledge-base/zero-config-guide/)

## TH03 Entrá por HTTPS 8089 y usá el asistente inicial
- Sub-topic: T01
- Agree: 2 of 4. Notes: a:N2, a:N4. Urls: https://documentation.grandstream.com/knowledge-base/ucm630x-series-user-manual/ https://support.telnyx.com/en/articles/5748258-grandstream-configuring-sip-trunks-on-your-grandstream-ucm6xxx-series
- Disagree: none found
- Level: foundation
- Best story: none

## TH04 Antes de actualizar firmware, backup; y programá backups fuera de la central
- Sub-topic: T01 (also T13)
- Agree: 4 of 4. Notes: a:N5, a:N58, a:N7, a:N8. Urls: https://documentation.grandstream.com/knowledge-base/ucm630x-series-user-manual/ https://www.tenable.com/cve/CVE-2025-28172 https://www.simtex.com.au/support/kb/pbx-setup-guides/grandstream-ucm-sip-trunk-configuration https://support.telnyx.com/en/articles/5748258-grandstream-configuring-sip-trunks-on-your-grandstream-ucm6xxx-series
- Disagree: none found
- Level: foundation
- Best story: CVE-2025-28172, UCM6510 hasta 1.0.20.52 sin límite de intentos de login (https://www.tenable.com/cve/CVE-2025-28172)

## TH05 Extensión con contraseña aleatoria y registros concurrentes acotados
- Sub-topic: T02 (also T13)
- Agree: 2 of 2 (thin evidence). Notes: a:N9, a:N10, a:N54. Urls: https://documentation.grandstream.com/knowledge-base/ucm630x-series-user-manual/ https://documentation.grandstream.com/knowledge-base/ucm6xxx-security-manual/
- Disagree: none found
- Level: foundation
- Best story: none

## TH06 Dejá NAT activado y Direct Media apagado en la extensión salvo que sepas por qué
- Sub-topic: T02 (also T16)
- Agree: 2 of 2 (thin evidence). Notes: a:N11, a:N67. Urls: https://documentation.grandstream.com/knowledge-base/ucm630x-series-user-manual/ https://documentation.grandstream.com/knowledge-base/ucm-remote-extensions-guide/
- Disagree: none found
- Level: core
- Best story: none

## TH07 Provisioná con Zero Config en lugar de cargar teléfono por teléfono
- Sub-topic: T03
- Agree: 2 of 2 (thin evidence). Notes: a:N12, a:N13, a:N15, a:N16. Urls: https://documentation.grandstream.com/knowledge-base/zero-config-guide/ https://documentation.grandstream.com/knowledge-base/ucm630x-series-user-manual/
- Disagree: none found
- Level: core
- Best story: escaneo por "SIP Message" a la dirección de broadcast cuando faltan equipos (https://documentation.grandstream.com/knowledge-base/zero-config-guide/)

## TH08 No toques la web del teléfono si lo vas a provisionar: lo manual le gana a la plantilla
- Sub-topic: T03
- Agree: 1 of 2 (thin evidence). Notes: a:N14. Urls: https://documentation.grandstream.com/knowledge-base/zero-config-guide/
- Disagree: none found
- Level: core
- Best story: none

## TH09 Para varios sitios, centralizá en GDMS y apagá el SSH remoto cuando no lo uses
- Sub-topic: T04 (also T13)
- Agree: 2 of 2 (thin evidence). Notes: a:N17, a:N18. Urls: https://blog.grandstream.com/company/news/blog/gdms-is-a-game-changer https://documentation.grandstream.com/knowledge-base/ucm630x-series-user-manual/
- Disagree: none found
- Level: core
- Best story: none

## TH10 Troncal con proveedor: Register Trunk y verificá en el Dashboard
- Sub-topic: T05
- Agree: 3 of 3. Notes: a:N19, a:N20, a:N22. Urls: https://documentation.grandstream.com/knowledge-base/sip-trunks-guide/ https://www.simtex.com.au/support/kb/pbx-setup-guides/grandstream-ucm-sip-trunk-configuration https://support.telnyx.com/en/articles/5748258-grandstream-configuring-sip-trunks-on-your-grandstream-ucm6xxx-series
- Disagree: none found
- Level: foundation
- Best story: "Rejected" en el Dashboard es credencial o alcance (https://documentation.grandstream.com/knowledge-base/sip-trunks-guide/)

## TH11 Para el troncal registrado no abras puertos
- Sub-topic: T05 (also T14)
- Agree: 2 of 3. Notes: a:N24, a:N59. Urls: https://www.simtex.com.au/support/kb/pbx-setup-guides/grandstream-ucm-sip-trunk-configuration https://community.freepbx.org/t/vpn-or-tls/91126
- Disagree: none found
- Level: core
- Best story: "en el 99,9 % de los casos no hace falta reenviar puertos" (afirmación de Simtex)

## TH12 Recortá los codecs del troncal a los que usa el proveedor
- Sub-topic: T05 (also T16)
- Agree: 1 of 3 (thin evidence). Notes: a:N23. Urls: https://www.simtex.com.au/support/kb/pbx-setup-guides/grandstream-ucm-sip-trunk-configuration
- Disagree: none found
- Level: core
- Best story: none

## TH13 Revisá DID Mode cuando las entrantes no matchean
- Sub-topic: T05 (also T07)
- Agree: 1 of 3 (thin evidence). Notes: a:N21. Urls: https://documentation.grandstream.com/knowledge-base/sip-trunks-guide/
- Disagree: none found
- Level: core
- Best story: none

## TH14 Escribí patrones salientes con _ y usá Strip para sacar el prefijo
- Sub-topic: T06
- Agree: 3 of 5. Notes: a:N26, a:N27, a:N30. Urls: https://documentation.grandstream.com/knowledge-base/ucm630x-series-user-manual/ https://support.telnyx.com/en/articles/5748258-grandstream-configuring-sip-trunks-on-your-grandstream-ucm6xxx-series https://www.simtex.com.au/support/kb/pbx-setup-guides/grandstream-ucm-sip-trunk-configuration
- Disagree: Simtex dice que gana la primera ruta de arriba; el manual dice que la prioridad se configura por orden o por precisión de patrón.
- Level: foundation
- Best story: _9NXXXXXXXXX con Strip 1 (https://support.telnyx.com/en/articles/5748258-grandstream-configuring-sip-trunks-on-your-grandstream-ucm6xxx-series)

## TH15 Poné privilegio por ruta y PIN en las caras
- Sub-topic: T06 (also T13)
- Agree: 4 of 5. Notes: a:N28, a:N54, a:N59. Urls: https://documentation.grandstream.com/knowledge-base/ucm6xxx-security-manual/ https://documentation.grandstream.com/knowledge-base/ucm630x-series-user-manual/ https://community.freepbx.org/t/vpn-or-tls/91126 https://community.freepbx.org/t/fail2ban-securing-pbx-behind-router-with-port-forwarding/70943
- Disagree: none found
- Level: core
- Best story: separar ruta local de internacional y ponerle contraseña a la internacional (https://community.freepbx.org/t/fail2ban-securing-pbx-behind-router-with-port-forwarding/70943)

## TH16 Configurá un troncal de failover y heartbeat
- Sub-topic: T06 (also T05)
- Agree: 2 of 5. Notes: a:N29, a:N22. Urls: https://support.telnyx.com/en/articles/5748258-grandstream-configuring-sip-trunks-on-your-grandstream-ucm6xxx-series https://www.simtex.com.au/support/kb/pbx-setup-guides/grandstream-ucm-sip-trunk-configuration
- Disagree: none found
- Level: core
- Best story: failover a los 32 segundos sin respuesta o ante 403, 407, 408, 503, 603 (afirmación de Telnyx)

## TH17 Usá ByDID con Strip para llevar cada DID a su interna
- Sub-topic: T07
- Agree: 2 of 2 (thin evidence). Notes: a:N32, a:N33. Urls: https://documentation.grandstream.com/knowledge-base/sip-trunks-guide/ https://documentation.grandstream.com/knowledge-base/ucm630x-series-user-manual/
- Disagree: none found
- Level: core
- Best story: 0655441007 con Strip 6 llega a la 1007 (https://documentation.grandstream.com/knowledge-base/sip-trunks-guide/)

## TH18 Armá el IVR con horario por tecla y un destino para silencio o tecla inválida
- Sub-topic: T08
- Agree: 2 of 2 (thin evidence). Notes: a:N35, a:N36, a:N37. Urls: https://documentation.grandstream.com/knowledge-base/ucm630x-series-user-manual/ https://blog.grandstream.com/company/news/blog/how-to-use-the-ucm-ip-pbxs-call-center-features
- Disagree: el blog habla de hasta 5 niveles; el manual actual, 64 IVR anidados.
- Level: core
- Best story: none

## TH19 Grupo para "que suene en todos"; cola cuando hay espera, agentes y desborde
- Sub-topic: T09
- Agree: 2 of 2 (thin evidence). Notes: a:N38, a:N39, a:N40. Urls: https://documentation.grandstream.com/knowledge-base/ucm630x-series-user-manual/ https://blog.grandstream.com/company/news/blog/how-to-use-the-ucm-ip-pbxs-call-center-features
- Disagree: none found
- Level: core
- Best story: devolución de llamada sin perder el lugar en la cola (https://blog.grandstream.com/company/news/blog/how-to-use-the-ucm-ip-pbxs-call-center-features)

## TH20 Buzón con PIN no trivial, a correo y con salida a operador
- Sub-topic: T10
- Agree: 1 of 1 (thin evidence). Notes: a:N41, a:N42. Urls: https://documentation.grandstream.com/knowledge-base/ucm630x-series-user-manual/
- Disagree: none found
- Level: foundation
- Best story: none

## TH21 Interna remota: External Host, Local Network Address y puertos 5060 más 10000 a 20000
- Sub-topic: T11
- Agree: 3 of 3. Notes: a:N43, a:N72, a:N46. Urls: https://documentation.grandstream.com/knowledge-base/ucm-remote-extensions-guide/ https://documentation.grandstream.com/knowledge-base/ucm630x-series-user-manual/ https://community.freepbx.org/t/fail2ban-securing-pbx-behind-router-with-port-forwarding/70943
- Disagree: none found
- Level: core
- Best story: sin Local Network Address la IP externa no se arma bien (https://documentation.grandstream.com/knowledge-base/ucm-remote-extensions-guide/)

## TH22 Del lado del teléfono, STUN; si el NAT es simétrico, keep alive y puertos
- Sub-topic: T11
- Agree: 2 of 3. Notes: a:N44, a:N72. Urls: https://documentation.grandstream.com/knowledge-base/ucm-remote-extensions-guide/ https://documentation.grandstream.com/knowledge-base/ucm630x-series-user-manual/
- Disagree: none found
- Level: core
- Best story: none

## TH23 Si cambiás el puerto SIP, cambialo en la central, no solo en el router
- Sub-topic: T11 (also T13)
- Agree: 1 of 3 (thin evidence). Notes: a:N46. Urls: https://community.freepbx.org/t/fail2ban-securing-pbx-behind-router-with-port-forwarding/70943
- Disagree: none found
- Level: core
- Best story: 5555 afuera hacia 5060 adentro no funciona porque SIP lleva el puerto en los encabezados

## TH24 Apagá SIP ALG en el router del cliente y reiniciá
- Sub-topic: T12 (also T11, T16)
- Agree: 5 of 5. Notes: a:N43, a:N47, a:N48, a:N50, a:N51. Urls: https://documentation.grandstream.com/knowledge-base/ucm-remote-extensions-guide/ https://didlogic.com/learn/sip-alg-explained/ https://surevoip.co.uk/support/wiki/troubleshooting/sip_alg/start.html https://teleprojectuk.helpdocs.io/article/k6xq10vkqm-what-is-sip-alg-and-when-should-it-be-disabled https://www.plexatalk.co.uk/?p=17613
- Disagree: https://www.plexatalk.co.uk/?p=17613 y https://surevoip.co.uk/support/wiki/troubleshooting/sip_alg/start.html: hay casos raros (servidores viejos sin manejo de NAT) donde ayuda.
- Level: core
- Best story: corte a los 32 segundos, Timer H de 64 por 500 ms esperando un ACK (https://didlogic.com/learn/sip-alg-explained/)

## TH25 Fail2ban activo, con tus IPs en la Allowlist
- Sub-topic: T13
- Agree: 3 of 7. Notes: a:N52, a:N57, a:N59. Urls: https://documentation.grandstream.com/knowledge-base/ucm6xxx-security-manual/ https://wazo-platform.discourse.group/t/fail2ban-guide-for-servers-on-the-internet/399 https://community.freepbx.org/t/vpn-or-tls/91126
- Disagree: none found
- Level: core
- Best story: varios INVITE maliciosos por segundo y más de 50 IPs al primer baneo (https://wazo-platform.discourse.group/t/fail2ban-guide-for-servers-on-the-internet/399)

## TH26 Cerrá la administración: lista blanca de IPs, nada de 80 ni 443, SSH y AMI apagados
- Sub-topic: T13
- Agree: 4 of 7. Notes: a:N53, a:N56, a:N18, a:N59. Urls: https://documentation.grandstream.com/knowledge-base/ucm6xxx-security-manual/ https://documentation.grandstream.com/knowledge-base/ucm630x-series-user-manual/ https://www.simtex.com.au/support/kb/pbx-setup-guides/grandstream-ucm-sip-trunk-configuration https://community.freepbx.org/t/fail2ban-securing-pbx-behind-router-with-port-forwarding/70943
- Disagree: none found
- Level: core
- Best story: none

## TH27 Capas de defensa: estática, Geo-IP, dinámica, Fail2Ban
- Sub-topic: T13
- Agree: 2 of 7. Notes: a:N55. Urls: https://documentation.grandstream.com/knowledge-base/ucm630x-series-user-manual/ https://documentation.grandstream.com/knowledge-base/ucm6xxx-security-manual/
- Disagree: none found
- Level: advanced
- Best story: none

## TH28 Para remotos, VPN si la podés sostener; si no, listas blancas por IP o puertos con defensas
- Sub-topic: T14
- Agree: 3 of 5. Notes: a:N59, a:N61, a:N62. Urls: https://community.freepbx.org/t/vpn-or-tls/91126 https://community.freepbx.org/t/cloud-hosted-pbx-direct-sip-or-vpn/47641 https://community.freepbx.org/t/fail2ban-securing-pbx-behind-router-with-port-forwarding/70943
- Disagree: https://community.freepbx.org/t/fail2ban-securing-pbx-behind-router-with-port-forwarding/70943: su VPN se caía varias veces al día y perdía llamadas.
- Level: advanced
- Best story: VPN caída 2 a 4 veces por año, casi siempre por certificados (https://community.freepbx.org/t/vpn-or-tls/91126)

## TH29 Registrá el portero como una extensión y abrí con PIN por DTMF o tecla OpenDoor
- Sub-topic: T15
- Agree: 3 of 3. Notes: a:N63, a:N64, a:N66. Urls: https://blog.grandstream.com/company/news/blog/get-more-gds3710-integrating-it-your-grandstream-solution https://documentation.grandstream.com/knowledge-base/connecting-gds37xx-with-grp26xxx/ https://documentation.grandstream.com/knowledge-base/ucm630x-series-user-manual/
- Disagree: none found
- Level: core
- Best story: GRP2601 a 2604 solo audio; 2614 en adelante con imagen JPEG (https://documentation.grandstream.com/knowledge-base/connecting-gds37xx-with-grp26xxx/)

## TH30 Audio de un solo lado: primero NAT y puertos, después ALG, después captura
- Sub-topic: T16 (also T11, T12)
- Agree: 6 of 7. Notes: a:N67, a:N69, a:N70, a:N71, a:N43, a:N47. Urls: https://documentation.grandstream.com/knowledge-base/ucm630x-series-user-manual/ https://documentation.grandstream.com/knowledge-base/sip-trunks-guide/ https://documentation.grandstream.com/knowledge-base/ucm-remote-extensions-guide/ https://didlogic.com/learn/sip-alg-explained/ https://forum.netgate.com/post/897197 https://www.3cx.com/community/threads/grandstream-phone-receiver-cant-hear-me.116955/
- Disagree: https://www.3cx.com/community/threads/grandstream-phone-receiver-cant-hear-me.116955/: el caso no era el ALG ni el firewall local; mostró que el problema podía estar del lado del servidor.
- Level: core
- Best story: GXP1625 que oía pero no era oído solo contra un servidor (https://www.3cx.com/community/threads/grandstream-phone-receiver-cant-hear-me.116955/)

## TH31 Capturá en la UCM con Ethernet Capture y leé el SDP; syslog solo lo necesario
- Sub-topic: T16
- Agree: 2 of 7. Notes: a:N68, a:N69. Urls: https://documentation.grandstream.com/knowledge-base/ucm630x-series-user-manual/ https://didlogic.com/learn/sip-alg-explained/
- Disagree: none found
- Level: advanced
- Best story: comparar lo que salió con lo que llegó para ver si alguien reescribió el SDP (https://didlogic.com/learn/sip-alg-explained/)

## The big splits
- VPN o puertos abiertos para internos remotos: https://community.freepbx.org/t/vpn-or-tls/91126 (VPN primero) contra https://community.freepbx.org/t/cloud-hosted-pbx-direct-sip-or-vpn/47641 (lista blanca por IP para sedes fijas) y https://community.freepbx.org/t/fail2ban-securing-pbx-behind-router-with-port-forwarding/70943 (VPN poco confiable en su caso). Gira en torno a cuántos remotos hay, si tienen IP fija y quién mantiene la VPN.
- SIP ALG siempre apagado o "depende": la mayoría lo apaga sin excepción; https://www.plexatalk.co.uk/?p=17613 y https://surevoip.co.uk/support/wiki/troubleshooting/sip_alg/start.html admiten casos raros. Gira en torno a si la central y los teléfonos ya manejan NAT (los Grandstream sí).
- Login de fábrica: admin/admin en guías de proveedores contra contraseña aleatoria en la etiqueta en el manual oficial. Gira en torno a la antigüedad del equipo.
- Orden de rutas salientes: primera que matchea contra prioridad por precisión de patrón, según cómo esté "Outgoing Routing Priority".

## Coverage gaps
- T02, T03, T04, T07, T08, T09 y T10 se apoyan casi solo en documentación oficial (evidencia delgada en cantidad de páginas, fuerte en calidad).
- GDMS: no se pudo leer una guía técnica de GDMS (las páginas del producto cargan con JavaScript); solo un post del fabricante y el manual del UCM.
- Porteros GSC (GSC3570, GSC35xx): ninguna página leída los cubre en detalle; solo menciones.
- WP8xx (teléfonos WiFi): ninguna página propia; se tratan como cualquier terminal SIP aprovisionable.
- Calidad de voz (jitter, QoS, VLAN de voz): casi sin cobertura en lo leído.
- Foro oficial de Grandstream: no fue accesible desde el entorno (certificado); los casos de foro vienen de 3CX, FreePBX, Netgate y Wazo.
