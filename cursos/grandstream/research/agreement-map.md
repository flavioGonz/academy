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

# Módulo Líneas analógicas por FXO (lecciones 13 a 18, notas b:)
Páginas con notas en este módulo: 25 (24 nuevas y el manual del UCM630x). Antel no publica parámetros eléctricos ni el esquema de identificador: todo lo de la línea en sí queda como "medilo en la instalación".

## TH32 El FXS da tensión y timbre; el FXO se comporta como un teléfono
- Sub-topic: T17
- Agree: 4 of 4. Notes: b:N1, b:N3, b:N9, b:N55. Urls: https://www.patton.com/technotes/what-are-fxs-and-fxo/ https://wiki.innovaphone.com/?i=11277 https://documentation.grandstream.com/knowledge-base/ucm630x-audio-series-user-manual/ https://documentation.grandstream.com/wp-content/uploads/2026/10/HT80x-V2-–-Administration-Guide.pdf
- Disagree: none found
- Level: foundation
- Best story: FXS con FXS o FXO con FXO "is a senseless connection" (https://wiki.innovaphone.com/?i=11277)

## TH33 Medí la línea antes de enchufarla: tensión en reposo, al descolgar y quién más está en el par
- Sub-topic: T17 (also T22)
- Agree: 4 of 5. Notes: b:N2, b:N3, b:N4, b:N5, b:N11. Urls: https://www.patton.com/technotes/what-are-fxs-and-fxo/ https://wiki.innovaphone.com/?i=11277 https://www.sandman.com/firealarm-bul.html https://community.asterisk.org/t/functioning-pstn-line-with-red-alarm/65892
- Disagree: los valores cambian según la fuente (50 V, 24 a 70 V, 48 V); ninguna fuente da los de Antel.
- Level: foundation
- Best story: panel de alarma que entra en falla cada vez que alguien descuelga en la línea compartida (https://www.sandman.com/firealarm-bul.html)

## TH34 Una troncal por línea para rutear por número; varias FXO en una troncal para salir por la primera libre
- Sub-topic: T18 (also T21)
- Agree: 3 of 3. Notes: b:N12, b:N13, b:N16, b:N42. Urls: https://documentation.grandstream.com/knowledge-base/ucm630x-series-user-manual/ https://documentation.grandstream.com/knowledge-base/manage-analog-lines/ https://community.asterisk.org/t/receiving-calls-from-pstn-s-extension-or-dialed-number/40772
- Disagree: none found (la decisión es de diseño; ninguna fuente impone una forma)
- Level: core
- Best story: Ascend toma siempre el puerto 1 si está libre (https://documentation.grandstream.com/knowledge-base/manage-analog-lines/)

## TH35 Leé el estado de cada FXO en el Dashboard antes de tocar la configuración
- Sub-topic: T18 (also T22)
- Agree: 2 of 2. Notes: b:N10, b:N14. Urls: https://documentation.grandstream.com/knowledge-base/manage-analog-lines/ https://documentation.grandstream.com/knowledge-base/ucm630x-audio-series-user-manual/
- Disagree: la guía dice verde para listo; en el firmware actual se ve azul (observación del caso, no fuente)
- Level: foundation
- Best story: gris es "conectado pero no configurado" (https://documentation.grandstream.com/knowledge-base/manage-analog-lines/)

## TH36 Ajustá país de la línea y códec: FXO Opermode, ACIM y PCMA fuera de Norteamérica
- Sub-topic: T18 (also T20)
- Agree: 3 of 3. Notes: b:N17, b:N18, b:N38, b:N35. Urls: https://documentation.grandstream.com/knowledge-base/ucm630x-series-user-manual/ https://documentation.grandstream.com/knowledge-base/manage-analog-lines/ https://techdocs.audiocodes.com/multi-service-business-routers/mediant-500-msbr/user-manual/version-720/Content/UM/Debugging%20a%20Caller%20ID%20Detection%20on%20FXO.htm
- Disagree: none found
- Level: core
- Best story: PCMA "unless already known" para todo lo que no es Norteamérica (https://documentation.grandstream.com/knowledge-base/ucm630x-series-user-manual/)

## TH37 Cargá los tonos de Uruguay: todo es 425 Hz y lo que cambia es la cadencia
- Sub-topic: T19
- Agree: 2 of 2. Notes: b:N19, b:N20, b:N22. Urls: https://www.itu.int/dms_pub/itu-t/opb/sp/T-SP-E.180-2010-PDF-S.pdf https://www.3amsystems.com/World_Tone_Database?q=Uruguay
- Disagree: none found (thin evidence: la lista UIT es de 2010 y nadie confirma la red actual de Antel)
- Level: core
- Best story: ocupado 425 Hz 0,5/0,5 y llamada 425 Hz 1/4 (https://www.itu.int/dms_pub/itu-t/opb/sp/T-SP-E.180-2010-PDF-S.pdf)

## TH38 Elegí el método de corte que usa tu línea, y medilo en vez de adivinarlo
- Sub-topic: T19
- Agree: 5 of 7. Notes: b:N21, b:N23, b:N25, b:N26, b:N27, b:N30, b:N8. Urls: https://documentation.grandstream.com/knowledge-base/ucm630x-series-user-manual/ https://documentation.grandstream.com/knowledge-base/manage-analog-lines/ https://en.wikipedia.org/wiki/Answer_supervision https://help.yeastar.com/en/p-series/administrator-guide/analog-fxo-trunk-settings.html https://wiki.innovaphone.com/?i=11277
- Disagree: https://community.asterisk.org/t/asterisk-hangsup-when-busydetect-yes/44836: busy detection cortó llamadas buenas; https://lists.digium.com/pipermail/asterisk-users/2010-July/251933.html: el patrón explícito empeoró la detección.
- Level: core
- Best story: PSTN Detection con una llamada real de un minuto (https://documentation.grandstream.com/knowledge-base/manage-analog-lines/)

## TH39 Pedí el identificador a Antel y después probá esquemas hasta que el número aparezca
- Sub-topic: T20
- Agree: 5 of 6. Notes: b:N31, b:N32, b:N33, b:N34, b:N35, b:N36. Urls: https://antel.com.uy/personas/servicios/telefonia-fija/identificacion-de-numero-llamante https://documentation.grandstream.com/knowledge-base/ucm630x-series-user-manual/ https://en.wikipedia.org/wiki/Caller_ID https://techdocs.audiocodes.com/multi-service-business-routers/mediant-500-msbr/user-manual/version-720/Content/UM/Debugging%20a%20Caller%20ID%20Detection%20on%20FXO.htm https://help.yeastar.com/en/p-series/administrator-guide/analog-fxo-trunk-settings.html
- Disagree: ninguna fuente dice qué esquema usa Antel; Wikipedia no lista a Uruguay.
- Level: core
- Best story: "Failed to decode CallerID" mientras el teléfono con display sí lo mostraba (https://lists.digium.com/pipermail/asterisk-users/2010-July/251933.html)

## TH40 Eco, ruido o volumen: primero impedancia (ACIM), después ganancias
- Sub-topic: T20
- Agree: 2 of 3. Notes: b:N38, b:N39, b:N35. Urls: https://documentation.grandstream.com/knowledge-base/manage-analog-lines/ https://documentation.grandstream.com/knowledge-base/ucm630x-series-user-manual/
- Disagree: none found (thin evidence)
- Level: core
- Best story: none

## TH41 En analógico no hay DID: la ruta entrante es por troncal y siempre con destino
- Sub-topic: T21 (also T22)
- Agree: 4 of 4. Notes: b:N41, b:N42, b:N43, b:N44. Urls: https://docs.asterisk.org/Configuration/Dialplan/Special-Dialplan-Extensions/ https://community.asterisk.org/t/receiving-calls-from-pstn-s-extension-or-dialed-number/40772 https://documentation.grandstream.com/knowledge-base/manage-analog-lines/ https://documentation.grandstream.com/knowledge-base/ucm630x-series-user-manual/
- Disagree: none found
- Level: core
- Best story: "When an analog call comes into Asterisk, the call is sent to the s extension" (https://docs.asterisk.org/Configuration/Dialplan/Special-Dialplan-Extensions/)

## TH42 Salida por varias líneas: patrón de Uruguay, orden de puertos y failover; el número que se ve es el de la línea
- Sub-topic: T21
- Agree: 3 of 3. Notes: b:N13, b:N45, b:N46, b:N47. Urls: https://documentation.grandstream.com/knowledge-base/manage-analog-lines/ https://documentation.grandstream.com/knowledge-base/ucm630x-series-user-manual/ https://en.wikipedia.org/wiki/Telephone_numbers_in_Uruguay
- Disagree: none found
- Level: core
- Best story: Outbound Route CID "does not apply to analog trunks" (https://documentation.grandstream.com/knowledge-base/ucm630x-series-user-manual/)

## TH43 Revisá los servicios de Antel de la línea: desvíos, correo de voz y llamada en espera
- Sub-topic: T21 (also T22)
- Agree: 3 of 3. Notes: b:N48, b:N49, b:N50. Urls: https://antel.com.uy/personas/servicios/telefonia-fija/transferencia-temporal-incondicional https://antel.com.uy/personas/servicios/telefonia-fija/correo-de-voz https://antel.com.uy/personas/servicios/telefonia-fija/llamada-en-espera
- Disagree: none found (thin evidence: solo el proveedor)
- Level: core
- Best story: con la transferencia activa se escucha "un tono de libre distinto del normal" (https://antel.com.uy/personas/servicios/telefonia-fija/transferencia-temporal-incondicional)

## TH44 Diagnosticá de la ficha a la configuración, y cambiá el par de puerto para separar línea de equipo
- Sub-topic: T22
- Agree: 6 of 8. Notes: b:N11, b:N35, b:N51, b:N52, b:N53, b:N5, b:N24. Urls: https://community.asterisk.org/t/functioning-pstn-line-with-red-alarm/65892 https://techdocs.audiocodes.com/multi-service-business-routers/mediant-500-msbr/user-manual/version-720/Content/UM/Debugging%20a%20Caller%20ID%20Detection%20on%20FXO.htm https://documentation.grandstream.com/knowledge-base/ucm630x-audio-series-user-manual/ https://documentation.grandstream.com/knowledge-base/ucm630x-series-user-manual/ https://community.freepbx.org/t/polarity-switch-causing-false-call-backs/35199 https://www.sandman.com/firealarm-bul.html
- Disagree: none found
- Level: advanced
- Best story: entrantes fantasma por la inversión de polaridad al colgar (https://community.freepbx.org/t/polarity-switch-causing-false-call-backs/35199)

## TH45 Para reclamar a Antel, llevá datos: número, síntoma, horario y lo que mediste
- Sub-topic: T22
- Agree: 1 of 1. Notes: b:N54. Urls: https://antel.com.uy/atencion-telefonica
- Disagree: none found (thin evidence)
- Level: foundation
- Best story: none

## Divisiones del módulo
- Busy Tone Count alto o bajo: Grandstream lo sube para evitar cortes al azar; Yeastar avisa que muy alto no detecta; Asterisk muestra falsos positivos. Se decide con PSTN Detection y probando colgar del otro lado.
- Patrón de ocupado explícito o no: Grandstream y Yeastar lo usan; un caso de Asterisk detectó mejor sin él. Se decide midiendo el tono real con Analog Record Trace.
- Inversión de polaridad para cortar: útil donde la red la manda; en DAHDI generó cortes al atender y entrantes fantasma. Se activa solo si PSTN Detection la encuentra.

## Huecos del módulo
- Antel no publica tensión de la línea, frecuencia de timbre, esquema de identificador ni método de corte: todo eso queda para medir y probar en la instalación.
- La lista de tonos de la UIT es de 2010; no hay confirmación de que la red actual de Antel (incluidas las líneas que entrega desde equipos en la casa del cliente) use los mismos.
- URSEC: no se encontró una norma técnica pública de la interfaz de línea analógica.
- El foro oficial de Grandstream y la base de conocimiento de Yeastar (Cloudflare) no se pudieron leer; los casos de foro son de Asterisk, FreePBX y listas de Digium.

## Lección agregada en octubre de 2026: Troncal SIP de Antel (TH46 a TH52)
Base: research/notes/c.md (16 páginas con notas). Evidencia sobre Antel delgada: la página oficial no publica datos técnicos; lo técnico sale de un integrador y de dos foros, coherentes entre sí entre 2017 y 2022.

## TH46 La troncal de Antel es por IP: sin usuario ni contraseña, con OPTIONS de Antel
- Sub-topic: T23 (also T24)
- Agree: 3 of 3. Notes: c:N5, c:N7, c:N17. Urls: https://www.simpletech.uy/en/troncal-sip-empresarial-antel-uruguay/ https://www.3cx.com/community/threads/troncal-sip-antel-and-3cx.50040/ https://community.freepbx.org/t/antel-sip-trunk-only-options/84614
- Disagree: none found. La página de Antel no lo dice ni lo contradice.
- Level: foundation
- Best story: el FreePBX que contestaba 401 a cada OPTIONS (https://community.freepbx.org/t/antel-sip-trunk-only-options/84614)

## TH47 Antel entrega un puerto RJ45 con IP de cliente, gateway, máscara, servidor SIP, números y canales
- Sub-topic: T23
- Agree: 2 of 2. Notes: c:N4, c:N7. Urls: https://www.simpletech.uy/en/troncal-sip-empresarial-antel-uruguay/ https://www.3cx.com/community/threads/troncal-sip-antel-and-3cx.50040/
- Disagree: none found (thin evidence). No se confirmó si en FTTH llega como un puerto del ONT, una VLAN o un equipo aparte.
- Level: foundation
- Best story: máscara /30 y una IP de prueba para ping (https://www.3cx.com/community/threads/troncal-sip-antel-and-3cx.50040/)

## TH48 Planes por llamadas simultáneas sobre FTTH y fibra dedicada, con caller ID y número de salida a elección
- Sub-topic: T23
- Agree: 1 of 1. Notes: c:N1, c:N2. Urls: https://antel.com.uy/empresas/internet-y-fija/planes/troncal-sip
- Disagree: Simpletech (2018) también nombra el cobre como medio de acceso; la página actual de Antel habla solo de FTTH y fibra dedicada.
- Level: foundation
- Best story: none

## TH49 Conectá la troncal directo a la central y separala de la red del cliente; con NAT en el medio, el contenido SIP no se traduce
- Sub-topic: T24 (also T12)
- Agree: 3 of 3. Notes: c:N10, c:N11, c:N12, c:N15. Urls: https://www.simpletech.uy/en/troncal-sip-empresarial-antel-uruguay/ https://documentation.grandstream.com/knowledge-base/ucm630x-series-user-manual/ https://didlogic.com/learn/sip-alg-explained/
- Disagree: Simpletech recomienda un E-SBC si la troncal se mezcla con otras redes; para una pyme con una sola UCM, la conexión directa alcanza.
- Level: core
- Best story: el técnico de 3CX que tuvo ping recién al agregar rutas (https://www.3cx.com/community/threads/troncal-sip-antel-and-3cx.50040/)

## TH50 La saliente lleva un número de la troncal como caller ID, o Antel la rechaza o la saca con el número por defecto
- Sub-topic: T25
- Agree: 2 of 2. Notes: c:N24, c:N14, c:N1. Urls: https://www.simpletech.uy/en/troncal-sip-empresarial-antel-uruguay/ https://documentation.grandstream.com/knowledge-base/ucm630x-series-user-manual/
- Disagree: none found. Ninguna fuente dice qué código de respuesta usa Antel para el rechazo.
- Level: core
- Best story: none

## TH51 El plan de numeración de Uruguay arma la ruta saliente; el número entrante se mira en la primera llamada
- Sub-topic: T25
- Agree: 2 of 2 en el plan. Notes: c:N22, c:N23, c:N24. Urls: https://www.itu.int/dms_pub/itu-t/oth/02/02/T02020000E00001PDFS.pdf https://en.wikipedia.org/wiki/Telephone_numbers_in_Uruguay
- Disagree: ninguna fuente da el formato en que Antel entrega el número llamado ni si acepta 09 o 598 en las salientes.
- Level: core
- Best story: 911 es la excepción al formato 1XY (https://www.itu.int/dms_pub/itu-t/oth/02/02/T02020000E00001PDFS.pdf)

## TH52 Diagnóstico de la troncal: captura primero, leer la respuesta SIP, y reclamar con el número de servicio
- Sub-topic: T26
- Agree: 3 of 3. Notes: c:N25, c:N26, c:N27, c:N8. Urls: https://en.wikipedia.org/wiki/List_of_SIP_response_codes https://www.simpletech.uy/en/troncal-sip-empresarial-antel-uruguay/ https://www.3cx.com/community/threads/troncal-sip-antel-and-3cx.50040/
- Disagree: none found
- Level: core
- Best story: el número de servicio P más cinco dígitos (https://www.simpletech.uy/en/troncal-sip-empresarial-antel-uruguay/)

## Huecos de la lección
- Antel no publica servidor, puertos, codecs, formato de numeración ni la forma física de entrega en FTTH. Tampoco si su servidor contesta los OPTIONS de la central ni desde cuántas IP manda señalización y audio.
- La guía técnica más completa es de 2018 (actualizada en 2025) y la escribió un integrador; los foros son de 2017 y 2022.
