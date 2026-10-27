# Notes: batch b
Pages read: 16. With notes: 16. Skipped: 0. (Yeastar, Grandstream, 3CX, FreePBX community, Asterisk docs, Claroty Team82, CISA.)

## T06 Cuentas SIP en una central
- b:N1. Yeastar documenta el alta manual de un Akuvox E16C V2.0: crear la extensión en la central, anotar número, nombre de registro y contraseña; en el portero, Account > Basic: Account Enabled, Register Name, Username (número de extensión), Password, y en Preferred SIP Server la IP o dominio de la central. Resultado verificable en la central como extensión en línea.
  - Source: https://help.yeastar.com/en/p-series-appliance-edition/integrations/akuvox/manually-register-akuvox-intercom-device-with-yeastar-p-series-pbx-system.html  Quote: "This topic uses Akuvox E16C V2.0 as an example"
  - Kind: technique
  - Level: core
  - Bias: documentación de un fabricante de centrales (vende la central)
- b:N2. Yeastar pide resetear el portero si estaba usado antes y tener el IP Scanner de Akuvox en la misma subred antes de empezar.
  - Source: https://help.yeastar.com/en/p-series-appliance-edition/integrations/akuvox/manually-register-akuvox-intercom-device-with-yeastar-p-series-pbx-system.html  Quote: "RESET the intercom device if it is previously used."
  - Kind: rule of thumb
  - Level: foundation
  - Also: T02
- b:N3. Autoprovisión según la red: misma subred por PnP; otra subred por DHCP opción 66 con el link de provisión; red remota por Provision Link. Con DHCP, un solo servidor DHCP en esa subred o el portero no toma IP. Requiere firmware mínimo (E16C V2 216.30.10.85, R20A 320.30.11.112, X915S 2915.30.110.371, S562W 562.30.14.48, según Yeastar).
  - Source: https://help.yeastar.com/en/p-series-appliance-edition/integrations/akuvox/auto-provision-akuvox-intercom-device-with-yeastar-p-series-pbx-system.html  Quote: "Configure DHCP option 66 on DHCP server"
  - Kind: technique
  - Level: advanced
  - Also: T03, T04
- b:N4. Caso real en FreePBX: un R20A no registraba. El log mostraba "Failed to authenticate"; la causa más simple, según un moderador, es la contraseña equivocada. Resuelto eso, la llamada al portero fallaba porque marcaban asterisco 110 en vez de 110.
  - Source: https://community.freepbx.org/t/solved-sip-registration-failed-on-doorphone-akuvox-r20a/85457  Quote: "The simplest cause of this is a wrong password."
  - Kind: story
  - Level: core
  - Also: T15
- b:N5. En el mismo hilo, el portero registraba pero cambiaba de puerto en cada refresco; la sugerencia es desactivar SIP ALG en el router y activar el logger de pjsip para ver qué pasa.
  - Source: https://community.freepbx.org/t/solved-sip-registration-failed-on-doorphone-akuvox-r20a/85457  Quote: "you need to disable SIP ALG in the router"
  - Kind: technique
  - Level: core
  - Also: T03, T15
- b:N7. 3CX trata el portero como una extensión más: el visitante aprieta el botón, suena la extensión o el cliente web, se ve el video, se atiende y se abre; los desvíos y colas de la central se aplican igual.
  - Source: https://www.3cx.com/blog/voip-howto/door-phone/  Quote: "visitors or personnel can use the new door phone as an added 3CX extension"
  - Kind: definition
  - Level: foundation
  - Bias: blog de un fabricante de centrales
- b:N8. En Asterisk detrás de NAT, lo clave son local_net, external_media_address, external_signaling_address y direct_media; el ejemplo usa reenvío de 5060 y UDP 10000 a 20000 para RTP.
  - Source: https://docs.asterisk.org/Configuration/Channel-Drivers/SIP/Configuring-res_pjsip/Configuring-res_pjsip-to-work-through-NAT/  Quote: "The key is to make sure you have those three options set appropriately."
  - Kind: technique
  - Level: advanced
  - Also: T03, T13

## T07 DTMF
- b:N9. 3CX: el DTMF inband depende de la calidad del audio y los paquetes perdidos lo afectan; fuera de banda va por SIP INFO o RFC 2833. 3CX no recomienda SIP INFO porque no viaja sincronizado con el audio y muchos servicios públicos no lo soportan.
  - Source: https://www.3cx.com/blog/voip-howto/dtmf-rfc2833/  Quote: "SIP-INFO is not recommended for DTMF delivery"
  - Kind: rule of thumb
  - Level: core
  - Bias: central 3CX, texto de 2010
- b:N10. 3CX: si llega DTMF por SIP INFO, se reenvía como SIP INFO; el otro extremo tiene que soportar ese mecanismo. Es decir, la central no siempre traduce: el tipo tiene que coincidir punta a punta.
  - Source: https://www.3cx.com/blog/voip-howto/dtmf-rfc2833/  Quote: "if DTMF is received with SIP-INFO, it is forwarded also as SIP-INFO"
  - Kind: mistake
  - Level: core
- b:N11. Grandstream WP8x6 abre puertas Akuvox por DTMF: en el teléfono, External Service > Door System, tipo Others, cuenta, número del portero y código. En el Akuvox E12S: IP anunciada al mantener el botón de llamada, cuenta SIP en la misma central, Intercom > Basic para marcar al teléfono y Access Control > Relay para longitud y código DTMF.
  - Source: https://documentation.grandstream.com/knowledge-base/wp8x6-access-control-systems-configuration-guide/  Quote: "Press and hold the Call Button on the E12S panel to retrieve the IP address"
  - Kind: technique
  - Level: core
  - Also: T02, T06
- b:N12. Yeastar Linkus: durante la llamada, el usuario abre marcando el código DTMF 0 (el que viene en el portero); se cambia en Access Control > Relay > Relay del Akuvox.
  - Source: https://help.yeastar.com/en/p-series-appliance-edition/integrations/akuvox/control-door-access-via-linkus-clients.html  Quote: "open the door by dialing a DTMF code 0 via the Linkus clients"
  - Kind: technique
  - Level: core

## T08 Relés y cerraduras
- b:N13. Grandstream explica fail-safe y fail-secure con el cableado: NC con COM abre la cerradura al cortarse la energía (fail safe); NO con COM la deja trabada (fail secure). Un relé que solo tiene NO limita la elección.
  - Source: https://documentation.grandstream.com/knowledge-base/gds3710-two-doors-control-configuration-guide/  Quote: "when connecting NC2 and COM2 (Fail Safe) then strike will open when power is lost"
  - Kind: rule of thumb
  - Level: foundation
  - Bias: otro fabricante, el principio es general

## T10 Varias puertas
- b:N14. Grandstream: para abrir las dos puertas a la vez desde un teléfono con un solo código, las dos tienen que tener exactamente el mismo código DTMF; con códigos distintos se abre cada una por separado.
  - Source: https://documentation.grandstream.com/knowledge-base/gds3710-two-doors-control-configuration-guide/  Quote: "both Door1 and Doo2 has to be configured with exactly SAME password or PIN as DTMF open door"
  - Kind: technique
  - Level: core
- b:N15. FreePBX: un integrador con dos porteros (portón y puerta de oficina) resolvió abrir las dos con un solo botón mandando dos comandos HTTP desde la central (curl a cada portero); primero lo hizo con una extensión que cortaba la llamada, después con una tecla URL del teléfono para no perder al visitante. Él mismo advierte que así como está puede tener problemas de seguridad.
  - Source: https://community.freepbx.org/t/how-can-i-manage-double-doorphone-doorlock/97459  Quote: "Of course, as-is, it could have security issue"
  - Kind: story
  - Level: advanced
  - Also: T14

## T13 Video a través de la central
- b:N16. Asterisk no transcodifica video: los dos extremos tienen que soportar el mismo formato, y H.264 no viene habilitado por defecto.
  - Source: https://docs.asterisk.org/Configuration/Core-Configuration/Video-Telephony/  Quote: "There's no video transcoding so you have to make sure that both ends support the same video format."
  - Kind: rule of thumb
  - Level: core
- b:N17. Caso real: con un R20 llamando por IP directa a un videoteléfono Grandstream, la vista previa (early media) andaba; a través de FreePBX no. La causa fue la opción "r" de Dial en Asterisk, que fuerza tono de llamada e ignora el early media; "R" lo permite. En grupos de timbrado no lo lograron.
  - Source: https://community.freepbx.org/t/early-media-doorphone-video-preview/99698  Quote: "The issue was the r option in Asterisk Dial Options"
  - Kind: story
  - Level: advanced
  - Also: T05
- b:N18. Yeastar ofrece vista previa del video del portero antes de atender (Door Phone Application > Video Preview y Auto Preview) en su plan Ultimate.
  - Source: https://help.yeastar.com/en/p-series-appliance-edition/integrations/akuvox/control-door-access-via-linkus-clients.html
  - Kind: technique
  - Level: advanced
  - Bias: función paga del fabricante de la central

## T14 Seguridad
- b:N19. Claroty Team82 encontró 13 vulnerabilidades en el Akuvox E11 (publicadas en marzo de 2023): ejecución remota de código en la LAN, activar cámara y micrófono sin autenticación, y fotos de aperturas subidas a un FTP externo con un solo usuario para todos los equipos. Intentaron avisar al fabricante desde enero de 2022 sin respuesta; tras la publicación, Akuvox confirmó y prometió firmware antes del 20 de marzo de 2023.
  - Source: https://claroty.com/team82/research/akuvox-smart-intercom-vulnerabilities-leave-privacy-ajar  Quote: "uncovered 13 vulnerabilities"
  - Kind: story
  - Level: core
  - Bias: empresa de ciberseguridad (vende productos de seguridad OT)
- b:N20. Recomendaciones de Claroty: no exponer el equipo a internet (aunque se pierda la app), segmentarlo en su propia red con comunicación limitada a pocos equipos, abrir solo los puertos necesarios, bloquear UDP 8500 de entrada (descubrimiento) y cambiar la contraseña web por defecto.
  - Source: https://claroty.com/team82/research/akuvox-smart-intercom-vulnerabilities-leave-privacy-ajar  Quote: "we also recommend disabling UDP port 8500 for incoming traffic"
  - Kind: technique
  - Level: core
- b:N21. Claroty contó unos 5.000 equipos expuestos a internet con Censys (su cifra) y que la contraseña web descifrada era admin/admin.
  - Source: https://claroty.com/team82/research/the-silent-spy-among-us-modern-attacks-against-smart-intercoms  Quote: "we found about 5,000 of these devices exposed to the internet"
  - Kind: number
  - Level: core
- b:N22. CISA (ICSA-23-068-01) puntúa el peor caso en CVSS 9,8, describe SSH habilitado por defecto con usuario root y contraseña fija, llamadas SIP directas sin control de acceso, y recomienda desconectar los E11 de internet hasta que haya parche.
  - Source: https://www.cisa.gov/news-events/ics-advisories/icsa-23-068-01  Quote: "CISA recommends users disconnect Akuvox E11 devices from the internet"
  - Kind: number
  - Level: core
- b:N23. Grandstream UCM: contraseña de admin de fábrica aleatoria impresa en la etiqueta (desde 2017), cambio obligado recomendado, 10 a 30 caracteres, lista blanca de IP para la web, MFA, contraseñas SIP aleatorias, SRTP opcional o forzado por extensión, TLS para la señalización, Fail2ban.
  - Source: https://documentation.grandstream.com/knowledge-base/ucm6xxx-security-manual/  Quote: "the default random password can be found on the sticker at the back of the unit"
  - Kind: technique
  - Level: core
  - Also: T06
## Disagreements seen
- SIP INFO: 3CX no lo recomienda (https://www.3cx.com/blog/voip-howto/dtmf-rfc2833/); Akuvox lo ofrece como opción confiable (https://knowledge.akuvox.com/docs/door-unlock-configuration-8).
- Nube vs. aislamiento: Claroty y CISA piden sacar el equipo de internet (https://claroty.com/team82/research/akuvox-smart-intercom-vulnerabilities-leave-privacy-ajar, https://www.cisa.gov/news-events/ics-advisories/icsa-23-068-01); Yeastar y Akuvox documentan registro remoto por FQDN y nube (https://help.yeastar.com/en/p-series-appliance-edition/integrations/akuvox/manually-register-akuvox-intercom-device-with-yeastar-p-series-pbx-system.html).
- Dos puertas: Grandstream propone el mismo código DTMF en ambas (https://documentation.grandstream.com/knowledge-base/gds3710-two-doors-control-configuration-guide/); el integrador de FreePBX lo resolvió con comandos HTTP desde la central (https://community.freepbx.org/t/how-can-i-manage-double-doorphone-doorlock/97459).
- IP directa vs. central para video: el caso de FreePBX muestra que la vista previa anda por IP directa y se rompe por la central (https://community.freepbx.org/t/early-media-doorphone-video-preview/99698).

## Best stories
- 13 vulnerabilidades del E11, un año de mails sin respuesta, y fotos de aperturas en un FTP compartido. https://claroty.com/team82/research/akuvox-smart-intercom-vulnerabilities-leave-privacy-ajar
- El R20A que no registraba: contraseña mal y después asterisco de más. https://community.freepbx.org/t/solved-sip-registration-failed-on-doorphone-akuvox-r20a/85457
- La vista previa que se rompía por una letra: "r" contra "R" en el Dial de Asterisk. https://community.freepbx.org/t/early-media-doorphone-video-preview/99698
- Dos porteros, un botón: dos curl desde la central. https://community.freepbx.org/t/how-can-i-manage-double-doorphone-doorlock/97459
