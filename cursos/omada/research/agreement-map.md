# Agreement map: TP-Link Omada SDN Controller

M por subtema (páginas distintas con al menos una nota en ese subtema, contando Also): T01 5 · T02 9 · T03 5 · T04 3 · T05 4 · T06 7 · T07 3 · T08 4 · T09 3 · T10 3 · T11 1 · T12 2 · T13 3 · T14 3 · T15 7 · T16 8.

## TH01 Elegí el tipo de controlador por dónde vive el servicio, no por la marca del menú
- Sub-topic: T02
- Agree: 5 of 9. Notes: a:N4, a:N6, a:N7, b:N6, b:N7. Urls: https://support.omadanetworks.com/en/document/13150/, https://evanmccann.net/blog/2022/3/tp-link-omada-overview, https://lazyadmin.nl/home-network/omada-controller-docker/, https://www.tp-link.com/us/support/faq/3365, https://whitkirkchurch.org.uk/tech-blog/2021/08/installing-an-omada-sdn-controller-on-a-raspberry-pi-using-docker/
- Disagree: https://simeononsecurity.com/articles/ubiquiti-unifi-vs-tp-link-omada/: describe la nube como "gratis para 1 sitio", que no coincide con Essentials gratis y Standard por licencia.
- Level: foundation
- Best story: la PC de la mesa técnica que se dormía y dejaba la red sin controlador, https://whitkirkchurch.org.uk/tech-blog/2021/08/installing-an-omada-sdn-controller-on-a-raspberry-pi-using-docker/

## TH02 Dimensioná el controlador hardware por la cifra recomendada, no por la máxima
- Sub-topic: T02
- Agree: 1 of 9. Notes: a:N5. Urls: https://support.omadanetworks.com/en/document/13150/
- Disagree: https://evanmccann.net/blog/2022/3/tp-link-omada-overview: en 2022 citaba OC200 hasta 100 y OC300 hasta 500.
- Level: foundation
- Best story: none

## TH03 Cloud Access no es controlador en la nube
- Sub-topic: T02
- Agree: 2 of 9. Notes: a:N6, b:N6. Urls: https://support.omadanetworks.com/en/document/13150/, https://evanmccann.net/blog/2022/3/tp-link-omada-overview
- Disagree: none found
- Level: foundation
- Best story: el autor que verificó que el controlador no salía a la nube hasta vincular el TP-Link ID, https://evanmccann.net/blog/2022/3/tp-link-omada-overview

## TH04 Con controlador en la nube, la licencia es parte del diseño: si vence, la red sigue pero pierde portal, fast roaming y schedules
- Sub-topic: T02 (also T16)
- Agree: 2 of 9. Notes: a:N10, a:N11, a:N12, a:N63. Urls: https://www.tp-link.com/us/support/faq/3365, https://www.tp-link.com/us/support/faq/3589
- Disagree: none found
- Level: core
- Best story: la licencia vencida que apaga el portal, https://www.tp-link.com/us/support/faq/3365

## TH05 Verificá compatibilidad del modelo y versión de hardware antes de prometer el tipo de controlador
- Sub-topic: T02 (also T15)
- Agree: 2 of 9. Notes: a:N13, a:N59. Urls: https://www.tp-link.com/us/support/faq/3365, https://www.omadanetworks.com/us/omada-sdn/controller-upgrade/
- Disagree: none found
- Level: core
- Best story: none

## TH06 Al adoptar, el equipo pasa a obedecer al controlador: la GUI local deja de servir y las credenciales son las del sitio
- Sub-topic: T01
- Agree: 4 of 5. Notes: a:N1, b:N2, b:N3, a:N2. Urls: https://support.omadanetworks.com/document/13176/, https://evanmccann.net/blog/2022/3/tp-link-omada-overview, https://www.hostifi.com/support/omada-how-to-adopt-a-new-access-point, https://www.tp-link.com/us/support/faq/3365
- Disagree: none found
- Level: foundation
- Best story: none

## TH07 Antes de adoptar un equipo usado, reseteo de fábrica
- Sub-topic: T01 (also T05, T12)
- Agree: 3 of 5. Notes: a:N2, a:N3, a:N21, b:N2. Urls: https://www.tp-link.com/us/support/faq/3365, https://www.omadanetworks.com/cz/support/faq/2283/, https://support.omadanetworks.com/document/13176/
- Disagree: none found
- Level: foundation
- Best story: el EAP que pasó por la web local y quedó con el mesh deshabilitado hasta el reset, https://www.omadanetworks.com/cz/support/faq/2283/

## TH08 Para autoalojar, corré el controlador en un equipo dedicado, con cuenta local
- Sub-topic: T03
- Agree: 4 of 5. Notes: b:N5, b:N7, b:N9, b:N12. Urls: https://whitkirkchurch.org.uk/tech-blog/2021/08/installing-an-omada-sdn-controller-on-a-raspberry-pi-using-docker/, https://lazyadmin.nl/home-network/omada-controller-docker/, https://computingforgeeks.com/omada-controller-docker/, https://mariushosting.com/how-to-install-tp-link-omada-controller-on-your-synology-nas/
- Disagree: https://support.omadanetworks.com/en/document/13150/: el fabricante empuja hardware o nube para no mantener host propio (no hay imagen Docker oficial).
- Level: foundation
- Best story: la PC que se dormía, https://whitkirkchurch.org.uk/tech-blog/2021/08/installing-an-omada-sdn-controller-on-a-raspberry-pi-using-docker/

## TH09 En Docker, red host; si no se puede, Inform URL
- Sub-topic: T03 (also T05, T06)
- Agree: 3 of 5. Notes: b:N10, b:N15, b:N24. Urls: https://computingforgeeks.com/omada-controller-docker/, https://lazyadmin.nl/home-network/omada-controller-docker/, https://mariushosting.com/how-to-install-tp-link-omada-controller-on-your-synology-nas/
- Disagree: none found
- Level: core
- Best story: la web anda y los APs nunca aparecen, https://computingforgeeks.com/omada-controller-docker/

## TH10 Controlador 6.x pide CPU con AVX: Raspberry Pi 4 y NAS viejos quedan afuera
- Sub-topic: T03
- Agree: 2 of 5. Notes: b:N13, b:N14. Urls: https://lazyadmin.nl/home-network/omada-controller-docker/, https://mariushosting.com/how-to-install-tp-link-omada-controller-on-your-synology-nas/
- Disagree: none found
- Level: core
- Best story: la Pi 4 donde MongoDB se cae al arrancar, https://lazyadmin.nl/home-network/omada-controller-docker/

## TH11 Dale a MongoDB tiempo para cerrar y al controlador tiempo para arrancar
- Sub-topic: T03 (also T16)
- Agree: 2 of 5. Notes: b:N11, b:N12, b:N37. Urls: https://lazyadmin.nl/home-network/omada-controller-docker/, https://computingforgeeks.com/omada-controller-docker/
- Disagree: none found
- Level: core
- Best story: none

## TH12 Sabé de memoria los puertos: 29810 UDP descubre, 29811 a 29817 TCP gestionan, 8043 web, 8843 portal
- Sub-topic: T04
- Agree: 3 of 3. Notes: a:N15, a:N16, b:N19. Urls: https://support.omadanetworks.com/document/13090/, https://computingforgeeks.com/omada-controller-docker/, https://lazyadmin.nl/home-network/omada-controller-docker/
- Disagree: none found
- Level: foundation
- Best story: none

## TH13 En controlador 6, abrí también el TCP 29817
- Sub-topic: T04 (also T15)
- Agree: 2 of 3. Notes: a:N16, b:N19. Urls: https://support.omadanetworks.com/document/13090/, https://computingforgeeks.com/omada-controller-docker/
- Disagree: none found
- Level: foundation
- Best story: none

## TH14 Con NAT en el medio, reenviá 29810 a 29817 con el mismo puerto de origen y destino
- Sub-topic: T04 (also T06)
- Agree: 2 of 3. Notes: a:N17, a:N19, a:N24. Urls: https://support.omadanetworks.com/document/13090/, https://support.omadanetworks.com/de/document/124358/
- Disagree: none found
- Level: core
- Best story: dos controladores tras la misma IP pública, uno movido a 29820 a 29827, https://support.omadanetworks.com/document/13090/

## TH15 Si un equipo no aparece en Pending, primero mirá si está en la misma VLAN que el controlador
- Sub-topic: T05
- Agree: 3 of 4. Notes: a:N20, a:N22, b:N20. Urls: https://support.omadanetworks.com/document/13090/, https://support.omadanetworks.com/document/13176/, https://computingforgeeks.com/omada-controller-docker/
- Disagree: none found
- Level: foundation
- Best story: none

## TH16 Leé el mensaje de Adopt Failed: credenciales, sin respuesta, uplink mesh
- Sub-topic: T05 (also T16)
- Agree: 2 of 4. Notes: a:N21, a:N22, a:N23, b:N21. Urls: https://support.omadanetworks.com/document/13176/, https://www.hostifi.com/support/omada-how-to-adopt-a-gateway-to-the-controller
- Disagree: none found
- Level: foundation
- Best story: el Adopt Failed que pide la clave de la GUI local, https://www.hostifi.com/support/omada-how-to-adopt-a-gateway-to-the-controller

## TH17 Para otra subred o sede: Discovery Utility, Inform URL u option 138
- Sub-topic: T06
- Agree: 6 of 7. Notes: a:N24, a:N28, b:N22, b:N23, b:N24, b:N15. Urls: https://support.omadanetworks.com/de/document/124358/, https://www.omadanetworks.com/ph/support/faq/4580/, https://www.hostifi.com/support/omada-how-to-adopt-a-gateway-to-the-controller, https://www.hostifi.com/support/omada-how-to-adopt-a-new-access-point, https://lazyadmin.nl/home-network/omada-controller-docker/, https://support.omadanetworks.com/document/13090/
- Disagree: none found
- Level: foundation
- Best story: la sucursal por VPN con option 138 servida por un switch, https://support.omadanetworks.com/de/document/124358/

## TH18 Option 138 recién actúa cuando el equipo renueva DHCP
- Sub-topic: T06
- Agree: 1 of 7. Notes: a:N25. Urls: https://support.omadanetworks.com/de/document/124358/
- Disagree: none found
- Level: core
- Best story: none

## TH19 Un sitio, un gateway: cada sede con su gateway es un sitio
- Sub-topic: T07 (also T14)
- Agree: 2 of 3. Notes: a:N27, a:N53. Urls: https://support.omadanetworks.com/de/document/124358/, https://www.omadanetworks.com/us/support/faq/4699/
- Disagree: none found
- Level: foundation
- Best story: none

## TH20 Para varios clientes, MSP en software controller o Cloud Standard, con roles separados
- Sub-topic: T07
- Agree: 2 of 3. Notes: a:N8, a:N30, a:N31, a:N32. Urls: https://support.omadanetworks.com/en/document/13150/, https://www.tp-link.com/de/support/faq/4276
- Disagree: none found
- Level: core
- Best story: none

## TH21 Una VLAN necesita tres cosas: interfaz y DHCP en el gateway, uplink tagueado, puerto de acceso con la VLAN nativa
- Sub-topic: T08
- Agree: 3 of 4. Notes: a:N33, a:N34, a:N36, a:N37. Urls: https://www.tp-link.com/us/support/faq/4084, https://www.omadanetworks.com/lk/support/faq/3157/, https://www.omadanetworks.com/eg/support/faq/4122/
- Disagree: https://evanmccann.net/blog/2022/3/tp-link-omada-overview: la VLAN de gestión es más difícil de lo que debería.
- Level: foundation
- Best story: none

## TH22 Dejá la red por defecto como VLAN de gestión de los equipos Omada
- Sub-topic: T08
- Agree: 1 of 4. Notes: a:N36. Urls: https://www.omadanetworks.com/lk/support/faq/3157/
- Disagree: https://evanmccann.net/blog/2022/3/tp-link-omada-overview: mover la gestión a otra VLAN es posible pero engorroso.
- Level: core
- Best story: none

## TH23 VLAN no es aislamiento: para cortar tráfico entre redes, ACL, y el orden importa
- Sub-topic: T09
- Agree: 3 of 3. Notes: a:N38, a:N39, b:N27. Urls: https://www.tp-link.com/us/support/faq/4084, https://www.omadanetworks.com/eg/support/faq/4122/, https://forums.lawrencesystems.com/t/tp-link-omada-followup/17893
- Disagree: none found
- Level: core
- Best story: el switch con la IP de gestión alcanzable desde cualquier VLAN, https://forums.lawrencesystems.com/t/tp-link-omada-followup/17893

## TH24 En 2,4 GHz 1, 6 y 11 a 20 MHz; en 5 GHz, 40 MHz de arranque; y bajá potencia cuando los AP están cerca
- Sub-topic: T10 (also T11)
- Agree: 2 of 3. Notes: a:N40, a:N41, a:N46. Urls: https://www.tp-link.com/us/support/faq/2511, https://support.omadanetworks.com/en/document/13229/
- Disagree: none found
- Level: foundation
- Best story: none

## TH25 La región del controlador manda sobre canales y potencia legales
- Sub-topic: T10
- Agree: 1 of 3. Notes: b:N16. Urls: https://computingforgeeks.com/omada-controller-docker/
- Disagree: none found
- Level: foundation
- Best story: none

## TH26 WLAN Optimization corta el servicio: programala de madrugada y lejos del reboot
- Sub-topic: T10
- Agree: 1 of 3. Notes: a:N42. Urls: https://www.tp-link.com/us/support/faq/2511
- Disagree: none found
- Level: core
- Best story: el escaneo que deja sin internet varios minutos, https://www.tp-link.com/us/support/faq/2511

## TH27 Roaming: mismo SSID idéntico, mismo sitio, 802.11k/v encendido, 802.11r solo si los clientes lo bancan
- Sub-topic: T11
- Agree: 1 of 1 (thin evidence). Notes: a:N43, a:N44, a:N45, a:N46. Urls: https://support.omadanetworks.com/en/document/13229/
- Disagree: none found
- Level: core
- Best story: none

## TH28 Mesh extiende cobertura, no capacidad: pocos saltos, buena señal de uplink, estrella
- Sub-topic: T12
- Agree: 1 of 2 (thin evidence). Notes: a:N47, a:N48, a:N49. Urls: https://www.omadanetworks.com/cz/support/faq/2283/
- Disagree: none found
- Level: core
- Best story: none

## TH29 El portal depende del controlador corriendo y del certificado
- Sub-topic: T13 (also T02)
- Agree: 2 of 3. Notes: a:N50, a:N51, b:N17. Urls: https://support.omadanetworks.com/en/document/13285/, https://whitkirkchurch.org.uk/tech-blog/2021/08/installing-an-omada-sdn-controller-on-a-raspberry-pi-using-docker/
- Disagree: none found
- Level: core
- Best story: none

## TH30 Revisá el portal después de cada upgrade grande de controlador
- Sub-topic: T13 (also T15)
- Agree: 1 of 3. Notes: a:N52. Urls: https://www.omadanetworks.com/us/omada-sdn/controller-upgrade/
- Disagree: none found
- Level: advanced
- Best story: la migración a 4.1.5 que obligó a rehacer el portal, https://www.omadanetworks.com/us/omada-sdn/controller-upgrade/

## TH31 VPN de sitio: Auto IPsec cuando ambos gateways tienen IP pública y están en el mismo controlador; Manual IPsec si hay NAT
- Sub-topic: T14
- Agree: 2 of 3. Notes: a:N53, a:N54, a:N55. Urls: https://www.omadanetworks.com/us/support/faq/4699/, https://support.omadanetworks.com/de/document/124358/
- Disagree: https://evanmccann.net/blog/2022/3/tp-link-omada-overview: sirve para sitio a sitio, no para acceso remoto de usuarios; routing y VPN avanzados, mejor otro firewall.
- Level: core
- Best story: none

## TH32 Antes de actualizar, backup. Siempre. Y de a una versión mayor por vez
- Sub-topic: T15 (also T16)
- Agree: 4 of 7. Notes: a:N57, a:N64, b:N31, b:N32. Urls: https://tp-link.com/support/faq/3684, https://www.omadanetworks.com/us/omada-sdn/controller-upgrade/, https://lazyadmin.nl/home-network/omada-controller-docker/, https://computingforgeeks.com/omada-controller-docker/
- Disagree: none found
- Level: foundation
- Best story: none

## TH33 El downgrade del controlador es una reinstalación: guardá un backup por versión
- Sub-topic: T15
- Agree: 1 of 7. Notes: a:N56, a:N57. Urls: https://tp-link.com/support/faq/3684
- Disagree: none found
- Level: core
- Best story: none

## TH34 Firmware Beta y RC solo en laboratorio; el ritmo de releases de TP-Link es discutido
- Sub-topic: T15
- Agree: 1 of 7. Notes: a:N58. Urls: https://tp-link.com/support/faq/3684
- Disagree: https://forums.lawrencesystems.com/t/tp-link-omada-followup/17893: un año con una sola actualización de switch; https://simeononsecurity.com/articles/ubiquiti-unifi-vs-tp-link-omada/: trimestral contra mensual en UniFi.
- Level: core
- Best story: un año, un firmware, https://forums.lawrencesystems.com/t/tp-link-omada-followup/17893

## TH35 Backup automático programado y guardado fuera del controlador
- Sub-topic: T16
- Agree: 2 of 8. Notes: b:N33, b:N36. Urls: https://lazyadmin.nl/home-network/omada-controller-docker/, https://computingforgeeks.com/omada-controller-docker/
- Disagree: none found
- Level: foundation
- Best story: none

## TH36 Migrá con el asistente en orden: exportar, importar, migrar equipos, y recién después Forget
- Sub-topic: T16
- Agree: 2 of 8. Notes: a:N60, a:N61, a:N62, a:N64. Urls: https://www.tp-link.com/us/support/faq/3589, https://www.omadanetworks.com/us/omada-sdn/controller-upgrade/
- Disagree: none found
- Level: core
- Best story: la migración donde saltear la importación deja los equipos sin adoptar, https://www.tp-link.com/us/support/faq/3589

## The big splits
- Confianza y seguridad de TP-Link para clientes de empresa: no lo usaría (https://forums.lawrencesystems.com/t/tp-link-omada-followup/17893) frente a recomendable para negocios con necesidades básicas (https://evanmccann.net/blog/2022/3/tp-link-omada-overview). Gira en torno al historial de seguridad y al riesgo que acepta cada integrador.
- Gateway Omada o firewall de terceros: la documentación pone al gateway Omada en el centro (https://support.omadanetworks.com/en/document/13150/); un practicante prefiere switches y APs Omada detrás de otro firewall (https://evanmccann.net/blog/2022/3/tp-link-omada-overview). Gira en torno a cuánto routing, firewall y VPN de usuarios necesita el cliente.
- Dónde vive el controlador: hardware o nube oficiales (https://support.omadanetworks.com/en/document/13150/) frente a Docker comunitario en servidor propio (https://lazyadmin.nl/home-network/omada-controller-docker/, https://computingforgeeks.com/omada-controller-docker/). Gira en torno a soporte oficial, costo de licencias y quién mantiene el host.
- Capacidad del controlador hardware: cifras oficiales actuales "recomendadas" bajas (https://support.omadanetworks.com/en/document/13150/) frente a cifras de 2022 más altas (https://evanmccann.net/blog/2022/3/tp-link-omada-overview).
- Ritmo de firmware: escaso según usuarios (https://forums.lawrencesystems.com/t/tp-link-omada-followup/17893, https://simeononsecurity.com/articles/ubiquiti-unifi-vs-tp-link-omada/) frente a canales Beta/RC y push en la nube (https://tp-link.com/support/faq/3684).

## Coverage gaps
- T11 roaming y T12 mesh: una sola fuente oficial cada uno (thin evidence); faltan practicantes midiendo roaming real.
- Portal: no se leyó la guía específica de vouchers v6.2 ni de portal externo; se cubre con la guía 5.9 a 6.
- VPN: no se leyó guía de WireGuard ni de VPN de cliente en gateways Omada; la lección se limita a sitio a sitio.
- Monitoreo: dashboard, alertas, notificaciones por mail, syslog y Network Check/Packet Capture aparecen solo en la tabla comparativa oficial; no hay fuente práctica leída.
- Firmware de dispositivos: la guía específica de upgrade de EAP/switch/gateway en modo controlador no se leyó; se cubre con la página del controlador y la de upgrade 4.1.5.
- No se encontró fuente de practicante sobre OC300/OC400 en obra ni sobre Omada Central Standard con MSP real.
