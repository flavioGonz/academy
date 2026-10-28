# Mapa de acuerdos: Porteros IP Akuvox

M por subtema (páginas distintas con al menos una nota en ese subtema, contando Also): T01 2, T02 3, T03 4, T04 3, T05 2, T06 8, T07 5, T08 2, T09 1, T10 4, T11 3, T12 1, T13 4, T14 11, T15 3. Temas con M menor a 3 llevan "thin evidence".

## TH01 Identificá modelo, versión de hardware y rama de firmware antes de tocar nada
- Sub-topic: T01 (also T04)
- Agree: 2 of 2 (thin evidence en T01; en T04 2 of 3). Notes: a:N1, a:N2, a:N3, b:N3. Urls: https://knowledge.akuvox.com/docs/upgrade-devices, https://knowledge.akuvox.com/docs/door-unlock-configuration-8, https://help.yeastar.com/en/p-series-appliance-edition/integrations/akuvox/auto-provision-akuvox-intercom-device-with-yeastar-p-series-pbx-system.html
- Disagree: none found
- Level: foundation
- Best story: R20A con etiqueta V3.0 que en realidad es hardware 2, https://knowledge.akuvox.com/docs/upgrade-devices

## TH02 Sacá la IP con el método del modelo (voz, pantalla, IP Scanner) y no adivines
- Sub-topic: T02
- Agree: 3 of 3. Notes: a:N4, a:N6, a:N7, b:N2, b:N11. Urls: https://knowledge.akuvox.com/docs/before-entering-device-web-interface, https://help.yeastar.com/en/p-series-appliance-edition/integrations/akuvox/manually-register-akuvox-intercom-device-with-yeastar-p-series-pbx-system.html, https://documentation.grandstream.com/knowledge-base/wp8x6-access-control-systems-configuration-guide/
- Disagree: none found
- Level: foundation
- Best story: el E12S dice su IP en voz alta al mantener el botón, https://documentation.grandstream.com/knowledge-base/wp8x6-access-control-systems-configuration-guide/

## TH03 El PIN de sistema y la clave web por defecto dependen del firmware; cambiá la web el primer día
- Sub-topic: T02 (also T14)
- Agree: 2 of 3 en T02; en T14 4 of 11 lo dicen explícito. Notes: a:N5, a:N7, a:N34, b:N20, b:N21. Urls: https://knowledge.akuvox.com/docs/before-entering-device-web-interface, https://claroty.com/team82/research/akuvox-smart-intercom-vulnerabilities-leave-privacy-ajar, https://claroty.com/team82/research/the-silent-spy-among-us-modern-attacks-against-smart-intercoms
- Disagree: none found sobre cambiarla; el fabricante publica admin/admin como paso normal sin insistir en cambiarla.
- Level: foundation
- Best story: E16 con PIN "admin" hasta 216.30.10.121 y "Admin321" después, https://knowledge.akuvox.com/docs/before-entering-device-web-interface

## TH04 Reseteá el equipo usado antes de integrarlo
- Sub-topic: T06 (also T02)
- Agree: 2 of 8. Notes: b:N2, b:N3. Urls: https://help.yeastar.com/en/p-series-appliance-edition/integrations/akuvox/manually-register-akuvox-intercom-device-with-yeastar-p-series-pbx-system.html, https://help.yeastar.com/en/p-series-appliance-edition/integrations/akuvox/auto-provision-akuvox-intercom-device-with-yeastar-p-series-pbx-system.html
- Disagree: none found
- Level: foundation
- Best story: none

## TH05 Actualizá con el archivo exacto del modelo y la versión de hardware, sin cerrar la ventana
- Sub-topic: T04
- Agree: 2 of 3. Notes: a:N8, a:N9, a:N11. Urls: https://knowledge.akuvox.com/docs/upgrade-devices, https://ticket.akuvox.com/support/solutions/articles/48001200817-read-first-how-to-provide-information-to-effectively-resolve-a-technical-issue-on-akuvox-intercom-
- Disagree: none found
- Level: foundation
- Best story: .zip para Android, .rom para Linux, https://knowledge.akuvox.com/docs/upgrade-devices

## TH06 Sabé si el equipo está en la rama de alta seguridad (C de 10 o más)
- Sub-topic: T04 (also T14)
- Agree: 1 of 3. Notes: a:N10. Urls: https://knowledge.akuvox.com/docs/upgrade-devices
- Disagree: none found
- Level: core
- Best story: none

## TH07 Usá llamada IP directa para una casa simple en la misma red
- Sub-topic: T05
- Agree: 2 of 2 (thin evidence). Notes: a:N12, b:N17. Urls: https://knowledge.akuvox.com/docs/intercom-call-configuration-8, https://community.freepbx.org/t/early-media-doorphone-video-preview/99698
- Disagree: none found
- Level: foundation
- Best story: la vista previa anda por IP directa y se rompe por la central, https://community.freepbx.org/t/early-media-doorphone-video-preview/99698

## TH08 Con central, registrá portero y monitor como extensiones comunes
- Sub-topic: T06
- Agree: 6 of 8. Notes: a:N13, b:N1, b:N7, b:N11, b:N12, b:N4. Urls: https://knowledge.akuvox.com/docs/intercom-call-configuration-8, https://help.yeastar.com/en/p-series-appliance-edition/integrations/akuvox/manually-register-akuvox-intercom-device-with-yeastar-p-series-pbx-system.html, https://www.3cx.com/blog/voip-howto/door-phone/, https://documentation.grandstream.com/knowledge-base/wp8x6-access-control-systems-configuration-guide/, https://community.freepbx.org/t/solved-sip-registration-failed-on-doorphone-akuvox-r20a/85457, https://help.yeastar.com/en/p-series-appliance-edition/integrations/akuvox/control-door-access-via-linkus-clients.html
- Disagree: none found
- Level: core
- Best story: el R20A de FreePBX, https://community.freepbx.org/t/solved-sip-registration-failed-on-doorphone-akuvox-r20a/85457

## TH09 Si no registra, primero la contraseña; después SIP ALG y puertos
- Sub-topic: T06 (also T03, T15)
- Agree: 1 of 8 con el caso, 2 of 4 en T03 (FreePBX y Asterisk NAT). Notes: b:N4, b:N5, b:N8. Urls: https://community.freepbx.org/t/solved-sip-registration-failed-on-doorphone-akuvox-r20a/85457, https://docs.asterisk.org/Configuration/Channel-Drivers/SIP/Configuring-res_pjsip/Configuring-res_pjsip-to-work-through-NAT/
- Disagree: none found
- Level: core
- Best story: "Failed to authenticate" y después el asterisco de más, https://community.freepbx.org/t/solved-sip-registration-failed-on-doorphone-akuvox-r20a/85457

## TH10 Usá la cuenta SIP 2 para la central si la 1 la toma SmartPlus
- Sub-topic: T06 (also T11)
- Agree: 1 of 8. Notes: a:N13, a:N29. Urls: https://knowledge.akuvox.com/docs/intercom-call-configuration-8
- Disagree: none found
- Level: core
- Best story: el R20A con cuenta 1 en el router Fritzbox y cuenta 2 en FreePBX, https://community.freepbx.org/t/solved-sip-registration-failed-on-doorphone-akuvox-r20a/85457

## TH11 Autoprovisioná por PnP, DHCP opción 66 o link según dónde esté la central
- Sub-topic: T06 (also T03)
- Agree: 1 of 8. Notes: b:N3. Urls: https://help.yeastar.com/en/p-series-appliance-edition/integrations/akuvox/auto-provision-akuvox-intercom-device-with-yeastar-p-series-pbx-system.html
- Disagree: none found
- Level: advanced
- Best story: none

## TH12 Mismo tipo de DTMF y mismo código en los dos extremos
- Sub-topic: T07
- Agree: 5 of 5. Notes: a:N17, a:N18, b:N10, b:N11, b:N12. Urls: https://knowledge.akuvox.com/docs/how-to-open-the-door-via-dtmf-on-the-indoor-monitor, https://knowledge.akuvox.com/docs/door-unlock-configuration-8, https://www.3cx.com/blog/voip-howto/dtmf-rfc2833/, https://documentation.grandstream.com/knowledge-base/wp8x6-access-control-systems-configuration-guide/, https://help.yeastar.com/en/p-series-appliance-edition/integrations/akuvox/control-door-access-via-linkus-clients.html
- Disagree: none found
- Level: core
- Best story: Linkus abre con el 0 que trae el portero de fábrica, https://help.yeastar.com/en/p-series-appliance-edition/integrations/akuvox/control-door-access-via-linkus-clients.html

## TH13 Preferí RFC 2833; dejá inband para casos sin opción
- Sub-topic: T07
- Agree: 3 of 5. Notes: a:N16, b:N9. Urls: https://knowledge.akuvox.com/docs/how-to-open-the-door-via-dtmf-on-the-indoor-monitor, https://knowledge.akuvox.com/docs/door-unlock-configuration-8, https://www.3cx.com/blog/voip-howto/dtmf-rfc2833/
- Disagree: https://knowledge.akuvox.com/docs/door-unlock-configuration-8 presenta SIP INFO como igual de confiable; 3CX lo desaconseja.
- Level: core
- Best story: inband que falla con G.729, https://knowledge.akuvox.com/docs/door-unlock-configuration-8

## TH14 Limitá quién puede abrir por DTMF (lista blanca de contactos)
- Sub-topic: T07 (also T14)
- Agree: 1 of 5. Notes: a:N19, a:N15. Urls: https://knowledge.akuvox.com/docs/door-unlock-configuration-8, https://knowledge.akuvox.com/docs/intercom-call-configuration-8
- Disagree: none found
- Level: core
- Best story: CISA sobre llamadas SIP directas sin control de acceso, https://www.cisa.gov/news-events/ics-advisories/icsa-23-068-01

## TH15 Elegí cerradura y contacto (NO/NC) según fail-safe o fail-secure
- Sub-topic: T08
- Agree: 2 of 2 (thin evidence). Notes: b:N13, a:N20. Urls: https://documentation.grandstream.com/knowledge-base/gds3710-two-doors-control-configuration-guide/, https://knowledge.akuvox.com/docs/door-unlock-configuration-8
- Disagree: none found
- Level: foundation
- Best story: none

## TH16 Botón de salida por entrada, con alarma de puerta abierta y de apertura forzada
- Sub-topic: T08
- Agree: 1 of 2 (thin evidence). Notes: a:N21. Urls: https://knowledge.akuvox.com/docs/door-unlock-configuration-8
- Disagree: none found
- Level: core
- Best story: none

## TH17 Cargá usuarios con relé y horario; alta masiva por CSV dentro del tgz
- Sub-topic: T09
- Agree: 1 of 1 (thin evidence). Notes: a:N24, a:N3. Urls: https://knowledge.akuvox.com/docs/door-unlock-configuration-8
- Disagree: none found
- Level: core
- Best story: 20.000 usuarios y 5 tarjetas por usuario en el E16, https://knowledge.akuvox.com/docs/door-unlock-configuration-8

## TH18 Cambiá el PIN público de fábrica
- Sub-topic: T09 (also T14)
- Agree: 1 of 1 (thin evidence). Notes: a:N23. Urls: https://knowledge.akuvox.com/docs/door-unlock-configuration-8
- Disagree: none found
- Level: foundation
- Best story: 33333333 por defecto, https://knowledge.akuvox.com/docs/door-unlock-configuration-8

## TH19 Rostro: no dejes la antisuplantación en "Close"
- Sub-topic: T09 (also T14)
- Agree: 1 of 1 (thin evidence). Notes: a:N25. Urls: https://knowledge.akuvox.com/docs/door-unlock-configuration-8
- Disagree: none found
- Level: core
- Best story: con "Close" pasa una foto, https://knowledge.akuvox.com/docs/door-unlock-configuration-8

## TH20 Tarjetas: preferí Mifare cifrada a solo UID
- Sub-topic: T09 (also T14)
- Agree: 1 of 1 (thin evidence). Notes: a:N27. Urls: https://knowledge.akuvox.com/docs/door-unlock-configuration-8
- Disagree: none found
- Level: advanced
- Best story: none

## TH21 Dos puertas desde un monitor: un código DTMF por relé y una tecla por puerta
- Sub-topic: T10
- Agree: 3 of 4. Notes: a:N17, b:N14. Urls: https://knowledge.akuvox.com/docs/how-to-open-the-door-via-dtmf-on-the-indoor-monitor, https://knowledge.akuvox.com/docs/door-unlock-configuration-8, https://documentation.grandstream.com/knowledge-base/gds3710-two-doors-control-configuration-guide/
- Disagree: https://community.freepbx.org/t/how-can-i-manage-double-doorphone-doorlock/97459: lo resolvió con comandos HTTP desde la central en lugar de DTMF.
- Level: core
- Best story: el código igual en dos puertas abre las dos de una, https://documentation.grandstream.com/knowledge-base/gds3710-two-doors-control-configuration-guide/

## TH22 Abrí por HTTP con usuario propio y solo desde IPs conocidas
- Sub-topic: T10 (also T14)
- Agree: 2 of 4. Notes: a:N22, b:N15. Urls: https://knowledge.akuvox.com/docs/door-unlock-configuration-8, https://community.freepbx.org/t/how-can-i-manage-double-doorphone-doorlock/97459
- Disagree: none found
- Level: advanced
- Best story: dos curl desde FreePBX y la advertencia del propio autor, https://community.freepbx.org/t/how-can-i-manage-double-doorphone-doorlock/97459

## TH23 SmartPlus resuelve la app del residente, pero sumá un plan B local
- Sub-topic: T11
- Agree: 2 of 3. Notes: a:N28, a:N29, a:N30. Urls: https://play.google.com/store/apps/details?id=com.akuvox.mobile.smartplus&hl=en&gl=US&pli=1, https://knowledge.akuvox.com/docs/intercom-call-configuration-8
- Disagree: https://claroty.com/team82/research/akuvox-smart-intercom-vulnerabilities-leave-privacy-ajar: recomienda sacar el equipo de internet aunque se pierda la app.
- Level: core
- Best story: reseña que ve a la visita pero no puede atender, https://play.google.com/store/apps/details?id=com.akuvox.mobile.smartplus&hl=en&gl=US&pli=1

## TH24 Mandá el portero al NVR por RTSP ch00_0 o ONVIF, con credenciales propias
- Sub-topic: T12
- Agree: 1 of 1 (thin evidence). Notes: a:N31, a:N32, a:N33. Urls: https://knowledge.akuvox.com/docs/monitor-and-image-13
- Disagree: none found
- Level: core
- Best story: dos streams, 2048 y 512 kbps, https://knowledge.akuvox.com/docs/monitor-and-image-13

## TH25 Video por la central: mismo codec en las dos puntas y early media habilitado
- Sub-topic: T13
- Agree: 3 of 4. Notes: b:N16, b:N17, b:N18. Urls: https://docs.asterisk.org/Configuration/Core-Configuration/Video-Telephony/, https://community.freepbx.org/t/early-media-doorphone-video-preview/99698, https://help.yeastar.com/en/p-series-appliance-edition/integrations/akuvox/control-door-access-via-linkus-clients.html
- Disagree: none found
- Level: advanced
- Best story: la "r" contra la "R" en el Dial, https://community.freepbx.org/t/early-media-doorphone-video-preview/99698

## TH26 Detrás de NAT, la central necesita saber su red local y su IP pública
- Sub-topic: T13 (also T03)
- Agree: 1 of 4. Notes: b:N8. Urls: https://docs.asterisk.org/Configuration/Channel-Drivers/SIP/Configuring-res_pjsip/Configuring-res_pjsip-to-work-through-NAT/
- Disagree: none found
- Level: advanced
- Best story: none

## TH27 El portero no se publica a internet
- Sub-topic: T14
- Agree: 3 of 11. Notes: b:N19, b:N20, b:N21, b:N22. Urls: https://claroty.com/team82/research/akuvox-smart-intercom-vulnerabilities-leave-privacy-ajar, https://claroty.com/team82/research/the-silent-spy-among-us-modern-attacks-against-smart-intercoms, https://www.cisa.gov/news-events/ics-advisories/icsa-23-068-01
- Disagree: https://help.yeastar.com/en/p-series-appliance-edition/integrations/akuvox/manually-register-akuvox-intercom-device-with-yeastar-p-series-pbx-system.html documenta registro remoto con puertos reenviados; SmartPlus asume salida a internet.
- Level: core
- Best story: 13 vulnerabilidades y unos 5.000 equipos expuestos, https://claroty.com/team82/research/the-silent-spy-among-us-modern-attacks-against-smart-intercoms

## TH28 Red separada para los porteros, con tráfico limitado a la central, el NVR y la gestión
- Sub-topic: T14
- Agree: 2 of 11. Notes: b:N20. Urls: https://claroty.com/team82/research/akuvox-smart-intercom-vulnerabilities-leave-privacy-ajar, https://www.cisa.gov/news-events/ics-advisories/icsa-23-068-01
- Disagree: none found
- Level: core
- Best story: none

## TH29 Cerrá lo que no usás: ONVIF, MJPEG y RTSP con clave; lista blanca SIP
- Sub-topic: T14
- Agree: 3 of 11. Notes: a:N15, a:N32, a:N33, b:N20. Urls: https://knowledge.akuvox.com/docs/monitor-and-image-13, https://knowledge.akuvox.com/docs/intercom-call-configuration-8, https://claroty.com/team82/research/akuvox-smart-intercom-vulnerabilities-leave-privacy-ajar
- Disagree: none found
- Level: core
- Best story: UDP 8500 de descubrimiento, https://claroty.com/team82/research/akuvox-smart-intercom-vulnerabilities-leave-privacy-ajar

## TH30 La central también se asegura: clave fuerte, lista blanca, SRTP y TLS
- Sub-topic: T14 (also T06)
- Agree: 2 of 11. Notes: b:N23, a:N14. Urls: https://documentation.grandstream.com/knowledge-base/ucm6xxx-security-manual/, https://knowledge.akuvox.com/docs/intercom-call-configuration-8
- Disagree: none found
- Level: core
- Best story: UCM con clave aleatoria en la etiqueta desde 2017, https://documentation.grandstream.com/knowledge-base/ucm6xxx-security-manual/

## TH31 Para soporte: firmware, config, log nivel 7 y PCAP arrancada justo antes
- Sub-topic: T15
- Agree: 2 of 3. Notes: a:N35, b:N5. Urls: https://ticket.akuvox.com/support/solutions/articles/48001200817-read-first-how-to-provide-information-to-effectively-resolve-a-technical-issue-on-akuvox-intercom-, https://community.freepbx.org/t/solved-sip-registration-failed-on-doorphone-akuvox-r20a/85457
- Disagree: none found
- Level: core
- Best story: PCAP de 1 MB, https://ticket.akuvox.com/support/solutions/articles/48001200817-read-first-how-to-provide-information-to-effectively-resolve-a-technical-issue-on-akuvox-intercom-

## TH32 Contraseña perdida: SmartPlus, PC Manager o llave del equipo a soporte
- Sub-topic: T15 (also T14)
- Agree: 1 of 3. Notes: a:N36. Urls: https://ticket.akuvox.com/support/solutions/articles/48001156051-how-to-reset-the-web-password-for-single-button-series-door-phone-
- Disagree: none found
- Level: core
- Best story: unlock.bin que devuelve soporte, https://ticket.akuvox.com/support/solutions/articles/48001156051-how-to-reset-the-web-password-for-single-button-series-door-phone-

## The big splits
- DTMF por SIP INFO: Akuvox lo ofrece como confiable (https://knowledge.akuvox.com/docs/door-unlock-configuration-8); 3CX lo desaconseja por falta de sincronía y de soporte (https://www.3cx.com/blog/voip-howto/dtmf-rfc2833/). Gira en torno a si la central en el medio lo pasa o lo descarta.
- Nube y acceso remoto vs. aislamiento: Claroty y CISA piden no exponer (https://claroty.com/team82/research/akuvox-smart-intercom-vulnerabilities-leave-privacy-ajar, https://www.cisa.gov/news-events/ics-advisories/icsa-23-068-01); Yeastar documenta registro remoto con reenvío de puertos y SmartPlus necesita salida a internet (https://help.yeastar.com/en/p-series-appliance-edition/integrations/akuvox/manually-register-akuvox-intercom-device-with-yeastar-p-series-pbx-system.html). Gira en torno a salida saliente hacia una nube contra puertos entrantes abiertos.
- Dos puertas: DTMF con el mismo código (https://documentation.grandstream.com/knowledge-base/gds3710-two-doors-control-configuration-guide/) contra comandos HTTP desde la central (https://community.freepbx.org/t/how-can-i-manage-double-doorphone-doorlock/97459).
- IP directa vs. central: la central suma desvíos, colas y apps; la IP directa conserva funciones como la vista previa (https://community.freepbx.org/t/early-media-doorphone-video-preview/99698).

## Coverage gaps
- T09 credenciales y horarios, T12 RTSP hacia NVR y T08 cerraduras quedaron con una o dos páginas (thin evidence): todo viene de la guía del E16 y de un fabricante tercero. Falta un practicante que cuente una integración real con un NVR (Hikvision, Dahua, Uniview).
- Falta una fuente práctica sobre alimentación de cerraduras (fuente separada, diodo en cerraduras magnéticas): la página oficial de cableado no se pudo guardar con el límite por sitio.
- No hay fuente que mida la calidad de SmartPlus más allá de reseñas de la tienda.
- No hay fuente sobre Grandstream UCM como central de los porteros más allá de su manual de seguridad y de los teléfonos WP8x6.
- No hay fuentes en español.

# Ampliación octubre de 2026: relés por HTTP y catálogo (TH33 a TH68)

Fuentes nuevas: research/notes/c.md y d.md. M por subtema nuevo (páginas distintas con al menos una nota, contando Also): T16 3, T17 5, T18 7, T19 2, T20 7, T21 10, T22 7, T23 11, T24 7. T19 queda con "thin evidence".

## TH33 Elegí el formato de URL según la rama de alta seguridad: /fcgi/OpenDoor si está activa, /fcgi/do solo en firmware viejo
- Sub-topic: T16 (also T17)
- Agree: 2 of 3. Notes: c:N3, c:N4, c:N7. Urls: https://knowledge.akuvox.com/docs/open-door-via-http-command, https://knowledge.akuvox.com/docs/trigger-door-actions-via-http-api-e18
- Disagree: https://forum.logicmachine.net/showthread.php?tid=6156: apaga la alta seguridad para seguir usando /fcgi/do con admin.
- Level: core
- Best story: con alta seguridad apagada conviven los tres formatos, https://knowledge.akuvox.com/docs/open-door-via-http-command

## TH34 DoorNum elige el relé: 1 es A, 2 es B, SA y SB para el SR01
- Sub-topic: T16 (also T18)
- Agree: 2 of 3. Notes: c:N5, c:N6. Urls: https://knowledge.akuvox.com/docs/open-door-via-http-command, https://knowledge.akuvox.com/docs/trigger-door-actions-via-http-api-e18
- Disagree: none found
- Level: core
- Best story: none

## TH35 Dejá Session Check apagado en Open Relay via HTTP
- Sub-topic: T16
- Agree: 1 of 3. Notes: c:N2. Urls: https://knowledge.akuvox.com/docs/open-door-via-http-command
- Disagree: none found
- Level: core
- Best story: none

## TH36 Usá CloseDoor, OpenDoorForever y DoorStatus solo donde el firmware lo soporta
- Sub-topic: T16
- Agree: 1 of 3. Notes: c:N6. Urls: https://knowledge.akuvox.com/docs/trigger-door-actions-via-http-api-e18
- Disagree: none found
- Level: advanced
- Best story: E18 18.30.11.27 y R20V5 320.30.12.28 como mínimos, https://knowledge.akuvox.com/docs/trigger-door-actions-via-http-api-e18

## TH37 Credenciales propias para el HTTP, nunca las de admin ni en blanco
- Sub-topic: T17
- Agree: 3 of 5. Notes: c:N8, c:N9, c:N29. Urls: https://knowledge.akuvox.com/docs/configure-http-api, https://pylocal-akuvox.readthedocs.io/en/latest/quickstart.html, https://knowledge.akuvox.com/docs/integration-with-milesight-lpr-camera-for-door-opening
- Disagree: https://knowledge.akuvox.com/docs/open-door-via-http-command: permite dejar usuario y clave en blanco. https://forum.logicmachine.net/showthread.php?tid=6156: usa admin en la URL.
- Level: core
- Best story: el script Lua con admin en la URL, https://forum.logicmachine.net/showthread.php?tid=6156

## TH38 Preferí Digest o Allowlist a Basic: Basic viaja en claro
- Sub-topic: T17
- Agree: 3 of 5. Notes: c:N8, c:N9, c:N29. Urls: https://knowledge.akuvox.com/docs/configure-http-api, https://pylocal-akuvox.readthedocs.io/en/latest/quickstart.html, https://knowledge.akuvox.com/docs/integration-with-milesight-lpr-camera-for-door-opening
- Disagree: none found
- Level: core
- Best story: "None" recomendado solo para demo, https://knowledge.akuvox.com/docs/configure-http-api

## TH39 La clave dentro de la URL termina en logs: usuario dedicado y red cerrada
- Sub-topic: T17
- Agree: 1 of 5. Notes: c:N10. Urls: https://pylocal-akuvox.readthedocs.io/en/latest/quickstart.html
- Disagree: https://knowledge.akuvox.com/docs/trigger-door-actions-via-http-api-e18: publica ejemplos con usuario y clave en la URL como formato recomendado.
- Level: advanced
- Best story: none

## TH40 No apagues la alta seguridad para usar la URL vieja
- Sub-topic: T17 (also T16)
- Agree: 1 of 5. Notes: c:N4. Urls: https://knowledge.akuvox.com/docs/open-door-via-http-command
- Disagree: https://forum.logicmachine.net/showthread.php?tid=6156: la apaga.
- Level: core
- Best story: none

## TH41 HTTPS en equipos viejos puede fallar por Diffie-Hellman débil; verificá certificados en lo nuevo
- Sub-topic: T17
- Agree: 1 of 5. Notes: c:N11. Urls: https://pylocal-akuvox.readthedocs.io/en/latest/quickstart.html
- Disagree: none found
- Level: advanced
- Best story: el S562 y el "dh key too small", https://pylocal-akuvox.readthedocs.io/en/latest/quickstart.html

## TH42 Para abrir un segundo portero, tecla Remote Relay By HTTP en el monitor
- Sub-topic: T18
- Agree: 1 of 7. Notes: c:N13. Urls: https://knowledge.akuvox.com/docs/open-door-via-http-command
- Disagree: none found
- Level: core
- Best story: teclas en pantalla de llamada, monitoreo y vista previa, https://knowledge.akuvox.com/docs/open-door-via-http-command

## TH43 Relé crítico adentro: SR01 por RS485 o por 12 V, para que romper el portero no abra
- Sub-topic: T18 (also T23)
- Agree: 1 of 7. Notes: c:N16, c:N17. Urls: https://knowledge.akuvox.com/docs/how-to-configure-sr01-security-relay-on-akuvox-door-phones
- Disagree: none found
- Level: core
- Best story: el portero destruido que no abre la puerta, https://knowledge.akuvox.com/docs/how-to-configure-sr01-security-relay-on-akuvox-door-phones

## TH44 Web Relay de terceros desde el portero: tipo, Action ID y hasta 50 comandos
- Sub-topic: T18
- Agree: 1 of 7. Notes: c:N14, c:N15. Urls: https://knowledge.akuvox.com/docs/configure-web-relay-on-door-phone-web-interface
- Disagree: none found
- Level: advanced
- Best story: none

## TH45 Relés externos del monitor por RS485 (MK485, RSAC-C1-R8) con firmware mínimo
- Sub-topic: T18 (also T22, T24)
- Agree: 1 of 7. Notes: c:N18, c:N19. Urls: https://knowledge.akuvox.com/docs/configure-external-relays-connected-to-indoor-monitors
- Disagree: none found
- Level: advanced
- Best story: el DIP 1 apagado que esconde el RSAC-C1-R8, https://knowledge.akuvox.com/docs/configure-external-relays-connected-to-indoor-monitors

## TH46 Relé de borde WR01 cuando la carga queda lejos del portero
- Sub-topic: T18 (also T23)
- Agree: 1 of 7. Notes: c:N20. Urls: https://www.akuvox.com/productsDisp?pid=130
- Disagree: none found
- Level: core
- Best story: none

## TH47 Ajustá Trigger Delay y Hold Delay; "Never" deja el relé activado
- Sub-topic: T18
- Agree: 2 of 7. Notes: c:N16, c:N18. Urls: https://knowledge.akuvox.com/docs/how-to-configure-sr01-security-relay-on-akuvox-door-phones, https://knowledge.akuvox.com/docs/configure-external-relays-connected-to-indoor-monitors
- Disagree: none found
- Level: core
- Best story: el E18 sin Hold Delay en el SR01, https://knowledge.akuvox.com/docs/how-to-configure-sr01-security-relay-on-akuvox-door-phones

## TH48 Antes de colgar la cerradura del portero, mirá la salida de 12 V del modelo
- Sub-topic: T18 (also T21)
- Agree: 1 of 7. Notes: d:N8. Urls: https://knowledge.akuvox.com/docs/devices-supporting-12v-power-output
- Disagree: none found
- Level: core
- Best story: la salida de 12 V del R20 que depende del volumen con PoE, https://knowledge.akuvox.com/docs/devices-supporting-12v-power-output

## TH49 Usá Action URL para que el portero avise eventos a un servidor, con variables
- Sub-topic: T19 (also T20)
- Agree: 2 of 2 (thin evidence). Notes: c:N22, c:N23, c:N25. Urls: https://knowledge.akuvox.com/docs/set-up-action-url, https://www.comfortclick.com/Support/ExampleDetails/Akuvox
- Disagree: none found
- Level: core
- Best story: $relay1status que llega 1 al abrir y 0 al cerrar, https://knowledge.akuvox.com/docs/set-up-action-url

## TH50 Dejá vacío el evento de arranque si no lo usás: no lo apaga el interruptor
- Sub-topic: T19
- Agree: 1 of 2 (thin evidence). Notes: c:N24. Urls: https://knowledge.akuvox.com/docs/set-up-action-url
- Disagree: none found
- Level: advanced
- Best story: none

## TH51 Cualquier cliente HTTP abre: probá con navegador o curl y mudalo al sistema que ya está en la obra
- Sub-topic: T20
- Agree: 7 of 7. Notes: c:N9, c:N25, c:N26, c:N27, c:N28, c:N29, c:N30. Urls: https://pylocal-akuvox.readthedocs.io/en/latest/quickstart.html, https://www.comfortclick.com/Support/ExampleDetails/Akuvox, https://www.home-assistant.io/integrations/rest_command, https://manual.mikrotik.com/docs/system-information-and-utilities/fetch/, https://docs.asterisk.org/Latest_API/API_Documentation/Dialplan_Functions/CURL/, https://knowledge.akuvox.com/docs/integration-with-milesight-lpr-camera-for-door-opening, https://knowledge.akuvox.com/docs/configure-lift-control-1
- Disagree: none found
- Level: core
- Best story: la cámara de patentes que abre el portón, https://knowledge.akuvox.com/docs/integration-with-milesight-lpr-camera-for-door-opening

## TH52 Igualá la autenticación del cliente con la del equipo (basic o digest)
- Sub-topic: T20 (also T17)
- Agree: 3 of 7. Notes: c:N9, c:N26, c:N27. Urls: https://pylocal-akuvox.readthedocs.io/en/latest/quickstart.html, https://www.home-assistant.io/integrations/rest_command, https://manual.mikrotik.com/docs/system-information-and-utilities/fetch/
- Disagree: none found
- Level: core
- Best story: none

## TH53 Cámaras LPR abren por la HTTP API del portero, en Allowlist
- Sub-topic: T20
- Agree: 1 of 7. Notes: c:N29. Urls: https://knowledge.akuvox.com/docs/integration-with-milesight-lpr-camera-for-door-opening
- Disagree: none found
- Level: advanced
- Best story: Hikvision solo con X912 y R29 desde ciertos firmwares, https://knowledge.akuvox.com/docs/integration-with-milesight-lpr-camera-for-door-opening

## TH54 Con HTTPS, validá el certificado en el cliente
- Sub-topic: T20 (also T17)
- Agree: 3 of 7. Notes: c:N11, c:N26, c:N27. Urls: https://manual.mikrotik.com/docs/system-information-and-utilities/fetch/, https://www.home-assistant.io/integrations/rest_command, https://pylocal-akuvox.readthedocs.io/en/latest/quickstart.html
- Disagree: none found
- Level: advanced
- Best story: fetch no valida TLS si no se pide check-certificate, https://manual.mikrotik.com/docs/system-information-and-utilities/fetch/

## TH55 Elegí el portero por las credenciales que pide la obra, con la tabla de métodos de acceso
- Sub-topic: T21 (also T23)
- Agree: 4 of 10. Notes: d:N2, d:N3, d:N4, d:N5. Urls: https://knowledge.akuvox.com/docs/access-methods-supported-by-door-phones, https://www.akuvox.com/productSelectionGuide?cid=3, https://www.akuvox.com/productsDisp?pid=37, https://www.akuvox.com/productsDisp?pid=17
- Disagree: none found
- Level: foundation
- Best story: huella solo en R29CT y como módulo del S535, https://knowledge.akuvox.com/docs/access-methods-supported-by-door-phones

## TH56 Verificá la alimentación por modelo: 802.3af, 802.3at o PoE+, y los que no aceptan PoE
- Sub-topic: T21 (also T22, T23)
- Agree: 5 of 10. Notes: d:N2, d:N3, d:N4, d:N6, d:N8. Urls: https://knowledge.akuvox.com/docs/power-supply-for-intercom-devices, https://www.akuvox.com/productSelectionGuide?cid=3, https://www.akuvox.com/productsDisp?pid=37, https://www.akuvox.com/productsDisp?pid=17, https://knowledge.akuvox.com/docs/devices-supporting-12v-power-output
- Disagree: none found
- Level: core
- Best story: el R29C-L con LTE que no toma PoE, https://knowledge.akuvox.com/docs/power-supply-for-intercom-devices

## TH57 Mirá la carga del relé del modelo antes de conectar la cerradura
- Sub-topic: T21 (also T22, T23)
- Agree: 2 of 10. Notes: d:N7, d:N8. Urls: https://knowledge.akuvox.com/docs/relay-output-of-indoor-monitors, https://knowledge.akuvox.com/docs/devices-supporting-12v-power-output
- Disagree: none found
- Level: core
- Best story: X916 con 5 A, https://knowledge.akuvox.com/docs/relay-output-of-indoor-monitors

## TH58 Confirmá IP e IK en la ficha de la versión exacta, no en tablas generales
- Sub-topic: T21
- Agree: 3 of 10. Notes: d:N2, d:N3, d:N4. Urls: https://www.akuvox.com/productSelectionGuide?cid=3, https://www.akuvox.com/productsDisp?pid=37, https://www.akuvox.com/productsDisp?pid=17
- Disagree: https://www.akuvox.com/productSelectionGuide?cid=3: X915 IP65, contra IP66 e IK10 de la ficha V2.0.
- Level: core
- Best story: el X915 con dos grados de protección según la página, https://www.akuvox.com/productsDisp?pid=37

## TH59 Sacá la IP con el método de la familia y leé el código A del firmware
- Sub-topic: T21 (also T22, T23, T24)
- Agree: 2 of 10. Notes: d:N9, d:N10. Urls: https://knowledge.akuvox.com/docs/before-entering-device-web-interface, https://knowledge.akuvox.com/docs/upgrade-devices
- Disagree: none found
- Level: foundation
- Best story: none

## TH60 Monitor Linux para lo simple, Android para apps; contá relés e interfaces
- Sub-topic: T22
- Agree: 4 of 7. Notes: d:N12, d:N13, d:N14, d:N15. Urls: https://www.akuvox.com/productSelectionGuide?cid=4, https://knowledge.akuvox.com/docs/interface-differences-of-akuvox-indoor-monitors, https://knowledge.akuvox.com/docs/relay-output-of-indoor-monitors, https://knowledge.akuvox.com/docs/power-supply-for-intercom-devices
- Disagree: none found
- Level: core
- Best story: el S560 de auricular, sin relé ni RS485, https://knowledge.akuvox.com/docs/interface-differences-of-akuvox-indoor-monitors

## TH61 En control de acceso, terminal en la puerta, controladora en el tablero, WR01 de borde y EC33 en el ascensor
- Sub-topic: T23
- Agree: 8 of 11. Notes: d:N17, d:N18, d:N19, d:N20, d:N21, c:N20, d:N5, d:N6. Urls: https://www.akuvox.com/products, https://www.akuvox.com/productsDisp?pid=92, https://knowledge.akuvox.com/docs/devices-supporting-12v-power-output, https://www.akuvox.com/productsDisp?pid=83, https://knowledge.akuvox.com/docs/configure-lift-control-1, https://www.akuvox.com/productsDisp?pid=130, https://knowledge.akuvox.com/docs/access-methods-supported-by-door-phones, https://knowledge.akuvox.com/docs/power-supply-for-intercom-devices
- Disagree: none found
- Level: core
- Best story: none

## TH62 EC33: en paralelo para ir directo al piso, en serie para liberar botones
- Sub-topic: T23
- Agree: 1 of 11. Notes: d:N21. Urls: https://knowledge.akuvox.com/docs/configure-lift-control-1
- Disagree: none found
- Level: advanced
- Best story: dos EC33, uno desbloquea y otro llama, https://knowledge.akuvox.com/docs/configure-lift-control-1

## TH63 Dos hilos para reformas: 48 V, NS-2 y nada de PoE en el portero
- Sub-topic: T23
- Agree: 2 of 11. Notes: d:N22, d:N15. Urls: https://www.akuvox.com/products, https://knowledge.akuvox.com/docs/power-supply-for-intercom-devices
- Disagree: none found
- Level: core
- Best story: none

## TH64 Separá catálogo vigente de parque instalado: menú de productos contra tablas de la Knowledge Base
- Sub-topic: T24
- Agree: 3 of 7. Notes: d:N26, d:N27, d:N28. Urls: https://www.akuvox.com/products, https://knowledge.akuvox.com/docs/upgrade-devices, https://www.comfortclick.com/Support/ExampleDetails/Akuvox
- Disagree: none found
- Level: core
- Best story: la pareja E11R y C315S, https://www.comfortclick.com/Support/ExampleDetails/Akuvox

## TH65 Software: SDMC para comunidades locales, ACMS o ACMS Pro para acceso en PC, SmartPlus para nube
- Sub-topic: T24
- Agree: 1 of 7. Notes: d:N25. Urls: https://www.akuvox.com/productsSoftwareForIntercom
- Disagree: none found
- Level: core
- Best story: el Installer Kit Tool montado sobre un S563W, https://www.akuvox.com/productsSoftwareForIntercom

## TH66 Pedí el accesorio del modelo exacto: cubierta de lluvia, soporte y módulo
- Sub-topic: T24
- Agree: 2 of 7. Notes: d:N4, c:N18. Urls: https://www.akuvox.com/productsDisp?pid=17, https://knowledge.akuvox.com/docs/configure-external-relays-connected-to-indoor-monitors
- Disagree: none found
- Level: foundation
- Best story: none

## TH67 Teléfonos de video y equipos fuera del intercom: usá solo lo que dice su ficha
- Sub-topic: T24
- Agree: 2 of 7. Notes: d:N23, d:N24. Urls: https://www.akuvox.com/productsDisp?pid=48, https://www.akuvox.com/products
- Disagree: none found
- Level: core
- Best story: none

## TH68 Monitores viejos abren su propio relé por HTTP con otro DoorNum: probalo antes de prometerlo
- Sub-topic: T24 (also T18)
- Agree: 2 of 7. Notes: c:N21, c:N9. Urls: https://www.comfortclick.com/Support/ExampleDetails/Akuvox, https://pylocal-akuvox.readthedocs.io/en/latest/quickstart.html
- Disagree: none found
- Level: advanced
- Best story: DoorNum=0 en el C315S, https://www.comfortclick.com/Support/ExampleDetails/Akuvox

## TH69 Un botón con varios destinos: en orden (Sequence Call) o todos juntos (Group Call), y el rechazo decide si sigue
- Sub-topic: T28
- Agree: 9 of 9 páginas de llamadas y grupos de la Knowledge Base. Notes: g:N5, g:N6, g:N7, g:N8, g:N11, g:N12, g:N16. Urls: https://knowledge.akuvox.com/docs/call-settings-10, https://knowledge.akuvox.com/docs/configure-sequence-call, https://knowledge.akuvox.com/docs/configure-group-call, https://knowledge.akuvox.com/docs/call-settings-7, https://knowledge.akuvox.com/docs/calling-feature, https://knowledge.akuvox.com/docs/call-settings-4, https://knowledge.akuvox.com/docs/call-setting-9, https://knowledge.akuvox.com/docs/call-settings-1, https://knowledge.akuvox.com/docs/call-settings-15
- Disagree: la redacción de End This Call Only ("other numbers" contra "the next number", g:N13); el X915 pone el rechazo del grupo en "Only Group Call Allowed" (g:N12).
- Level: core
- Best story: R29 con Time Out de 10 segundos que corta y pasa al siguiente, https://knowledge.akuvox.com/docs/call-setting-9

## TH70 El menú depende de la familia: táctiles con grupos del directorio y prioridad; botón y teclado con Manager Dial
- Sub-topic: T28
- Agree: 5 of 5. Notes: g:N7, g:N8, g:N14, g:N15, g:N16, g:N22. Urls: https://knowledge.akuvox.com/docs/configure-sequence-call, https://knowledge.akuvox.com/docs/configure-group-call, https://knowledge.akuvox.com/docs/contact-list-configuration-4, https://knowledge.akuvox.com/docs/contacts-configuration-13, https://knowledge.akuvox.com/docs/calling-feature
- Disagree: none found
- Level: core
- Best story: el R20B con números distintos por pulsador y módulo de expansión, https://knowledge.akuvox.com/docs/calling-feature

## TH71 Dial Plan y Call Feature: un número corto para varios destinos y límites que no superen a la central
- Sub-topic: T28 (also T05)
- Agree: 6 of 6. Notes: g:N18, g:N19, g:N20, g:N21. Urls: https://knowledge.akuvox.com/docs/call-settings-10, https://knowledge.akuvox.com/docs/call-setting-9, https://knowledge.akuvox.com/docs/call-settings-4, https://knowledge.akuvox.com/docs/call-settings-1, https://knowledge.akuvox.com/docs/call-settings-15, https://knowledge.akuvox.com/docs/call-settings-7
- Disagree: none found
- Level: core
- Best story: hasta 5 números reemplazados por un prefijo y llamados a la vez, https://knowledge.akuvox.com/docs/call-settings-10

## Split (botones)
- Separador de varios números en la tecla de Recepción: la guía del E18 dice ";" (https://knowledge.akuvox.com/docs/call-settings-15); la captura de un E16C V2.0 en obra usa ","; la guía del E16 no lo dice (https://knowledge.akuvox.com/docs/call-settings-10).

## Coverage gaps (botones)
- Ninguna página dice si los varios números de la tecla de Recepción suenan juntos o en orden.
- Ninguna página aclara qué hace un táctil con un grupo sin prioridades cuando también hay Sequence Call configurado; se lee que el grupo con prioridades va en orden y el grupo sin prioridades suena junto.
- El hilo de 3CX sobre un monitor Akuvox en un grupo de timbrado no entró en raw (página delgada para el scraper).

## The big splits (ampliación)
- Alta seguridad encendida o apagada: Akuvox recomienda el formato nuevo con la alta seguridad activa (https://knowledge.akuvox.com/docs/trigger-door-actions-via-http-api-e18); un integrador la apaga para usar la URL vieja con admin (https://forum.logicmachine.net/showthread.php?tid=6156). Gira en torno a compatibilidad del cliente contra exposición de la credencial.
- Credenciales en la URL: el fabricante las publica así (https://knowledge.akuvox.com/docs/trigger-door-actions-via-http-api-e18); pylocal-akuvox advierte que quedan en logs (https://pylocal-akuvox.readthedocs.io/en/latest/quickstart.html). Gira en torno a dónde se registra la URL.
- Autenticación en blanco: permitida en Open Relay via HTTP (https://knowledge.akuvox.com/docs/open-door-via-http-command), "solo para demo" en la HTTP API (https://knowledge.akuvox.com/docs/configure-http-api).
- Grado de protección del X915: IP65 en la guía de selección, IP66 e IK10 en la ficha V2.0 (https://www.akuvox.com/productSelectionGuide?cid=3, https://www.akuvox.com/productsDisp?pid=37).

## Coverage gaps (ampliación)
- T19 Action URL descansa en una página oficial y un ejemplo de integrador.
- No se encontró en páginas leídas una acción HTTP saliente en HikCentral ni en NVR Hikvision; lo documentado es la cámara LPR Hikvision hablando con el portero. Grandstream UCM no tiene en páginas leídas una acción HTTP para abrir: su camino documentado sigue siendo DTMF (lecciones 5, 6 y 8).
- Faltan fichas propias leídas de S539, S538, S535, S532, X916, X912, X910, R28, R25, R20, E18, E16, E13S, E12, E21, E20S, de los monitores, de A15, A095, A094, A01 a A05, de los lectores, del SR01, del NS-2 y de la cámara VC50: sus datos salen de las tablas transversales y de la guía de selección, sin cámara en megapíxeles ni grado IK salvo X915, R29 y A08.
- Ninguna página leída publica una lista oficial de discontinuados; C317 no aparece en ninguna.
