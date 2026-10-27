# Mapa de acuerdos: UniFi Network

Notas: research/notes/a.md (82 notas, 28 páginas con notas). Conteo N de M por páginas, no por notas. M = páginas con al menos una nota en el subtema del tema (incluidas las líneas Also). Versión compacta: 30 temas.

## TH01 Pensá cada sitio como un controlador propio; Site Manager solo es la puerta
- Sub-topic: T01 (also T03)
- Agree: 3 of 4. Notes: a:N1, a:N3, a:N11, a:N14. Urls: https://www.unihosted.com/blog/unifi-site-management, https://www.unihosted.com/blog/unifi-os-server, https://community.ui.com/releases/UniFi-Network-Application-11-0-97/15662d06-8122-44e2-a1ba-af5d71b8a045
- Disagree: none found
- Level: foundation
- Best story: si cae internet, el sitio se sigue gestionando en local; si cae el controlador, la red sigue andando sin cambios posibles. https://www.unihosted.com/blog/unifi-os-server

## TH02 Un dispositivo, un solo host
- Sub-topic: T01 (also T02)
- Agree: 2 of 4. Notes: a:N2, a:N8. Urls: https://www.unihosted.com/blog/unifi-os-server
- Disagree: none found
- Level: foundation
- Best story: un UDM no puede ser gestionado por un UniFi OS Server externo. https://www.unihosted.com/blog/unifi-os-server

## TH03 Para self-hosted en 2026, UniFi OS Server; el Network Server queda en 10.6
- Sub-topic: T02
- Agree: 4 of 4. Notes: a:N4, a:N5, a:N6. Urls: https://community.ui.com/releases/UniFi-Network-Application-11-0-97/15662d06-8122-44e2-a1ba-af5d71b8a045, https://community.ui.com/releases/UniFi-Network-Application-11-0-83/d6940379-cd5a-4e61-8596-7e22d647a4ea, https://community.ui.com/releases/UniFi-Network-Application-10-6-101/05283624-0980-4dd7-b8d6-9fa5c4e28da4, https://www.unihosted.com/blog/unifi-os-server
- Disagree: none found
- Level: foundation
- Best story: 11.0 elimina el Network Server y lo reemplaza oficialmente por UniFi OS Server. https://community.ui.com/releases/UniFi-Network-Application-11-0-97/15662d06-8122-44e2-a1ba-af5d71b8a045

## TH04 Cloud Gateway por sitio o controlador central: decidí por costo, actualizaciones y quién mantiene
- Sub-topic: T02 (also T03)
- Agree: 3 of 4. Notes: a:N5, a:N8, a:N11. Urls: https://community.ui.com/releases/UniFi-Network-Application-11-0-83/d6940379-cd5a-4e61-8596-7e22d647a4ea, https://www.unihosted.com/blog/unifi-os-server, https://www.unihosted.com/blog/unifi-site-management
- Disagree: none found (las fuentes de hosting tienen sesgo hacia el controlador central)
- Level: core
- Best story: Ubiquiti dice que ambos modelos son "functionally and administratively equivalent" en Site Manager. https://www.unihosted.com/blog/unifi-site-management

## TH05 No clones la VM del controlador
- Sub-topic: T02
- Agree: 1 of 4 (thin evidence). Notes: a:N7. Urls: https://www.unihosted.com/blog/unifi-os-server
- Disagree: none found
- Level: core
- Best story: los clones comparten tokens de acceso remoto. https://www.unihosted.com/blog/unifi-os-server

## TH06 Si un sitio no aparece en Site Manager, revisá salida 443/8883, DNS, NTP y Remote Management
- Sub-topic: T03
- Agree: 1 of 4 (thin evidence; la fuente cita el artículo oficial de Ubiquiti). Notes: a:N10. Urls: https://www.unihosted.com/blog/unifi-site-management
- Disagree: none found
- Level: core
- Best story: no hace falta abrir ningún puerto de entrada. https://www.unihosted.com/blog/unifi-site-management

## TH07 Para muchos clientes, usá Fabrics, roles y plantillas (Blueprints con Drift Inspector)
- Sub-topic: T03
- Agree: 2 of 4. Notes: a:N12, a:N13. Urls: https://www.unihosted.com/blog/unifi-site-management, https://community.ui.com/releases/UniFi-Network-Application-10-6-101/05283624-0980-4dd7-b8d6-9fa5c4e28da4
- Disagree: none found
- Level: advanced
- Best story: Drift Inspector muestra qué sitio se apartó de la plantilla. https://community.ui.com/releases/UniFi-Network-Application-10-6-101/05283624-0980-4dd7-b8d6-9fa5c4e28da4

## TH08 Antes de adoptar: equipo libre de otro controlador, firmware compatible, misma red L2
- Sub-topic: T04
- Agree: 3 of 3. Notes: a:N16, a:N17, a:N18, a:N21. Urls: https://lazyadmin.nl/home-network/unifi-adoption-failed/, https://www.hostifi.com/support/unifi-troubleshooting-unifi-cloud-adoption, https://www.sikich.com/insight/migrate-ubiquiti-unifi-controller-to-a-new-server/
- Disagree: none found
- Level: foundation
- Best story: el caso más común es desfase de firmware entre AP y controlador. https://lazyadmin.nl/home-network/unifi-adoption-failed/

## TH09 Para readoptar, primero borrá el equipo del controlador y reseteá
- Sub-topic: T04
- Agree: 2 of 3. Notes: a:N17, a:N19. Urls: https://lazyadmin.nl/home-network/unifi-adoption-failed/, https://www.hostifi.com/support/unifi-troubleshooting-unifi-cloud-adoption
- Disagree: none found
- Level: core
- Best story: tres equipos tras un corte de luz que no volvían hasta eliminarlos del controlador. https://lazyadmin.nl/home-network/unifi-adoption-failed/

## TH10 Para adopción L3, preferí DHCP option 43 o DNS; set-inform por SSH es el plan B
- Sub-topic: T05
- Agree: 2 of 4. Notes: a:N23, a:N22. Urls: https://forums.lawrencesystems.com/t/unifi-l3-persistent-inform-url/20405, https://www.hostifi.com/support/unifi-troubleshooting-unifi-cloud-adoption
- Disagree: https://forums.lawrencesystems.com/t/unifi-l3-persistent-inform-url/20405: Tom Lawrence usa set-inform para todos sus clientes sin problemas. https://www.sikich.com/insight/migrate-ubiquiti-unifi-controller-to-a-new-server/: indica set-inform como el método de migración.
- Level: core
- Best story: equipos que vuelven a unifi:8080/inform tras un reinicio. https://forums.lawrencesystems.com/t/unifi-l3-persistent-inform-url/20405

## TH11 El inform es http, puerto 8080, barra inform; mejor con nombre DNS que con IP
- Sub-topic: T05
- Agree: 3 of 4. Notes: a:N22, a:N26, a:N25. Urls: https://www.hostifi.com/support/unifi-troubleshooting-unifi-cloud-adoption, https://www.sikich.com/insight/migrate-ubiquiti-unifi-controller-to-a-new-server/, https://lazyadmin.nl/home-network/unifi-adoption-failed/
- Disagree: none found
- Level: foundation
- Best story: un lector con https y el puerto equivocado que dejó los AP "en el limbo". https://lazyadmin.nl/home-network/unifi-adoption-failed/

## TH12 Con controlador en contenedor o detrás de NAT, configurá Inform Host con Override
- Sub-topic: T05
- Agree: 2 of 4. Notes: a:N25. Urls: https://lazyadmin.nl/home-network/unifi-adoption-failed/, https://forums.lawrencesystems.com/t/unifi-l3-persistent-inform-url/20405
- Disagree: none found
- Level: core
- Best story: "Click OVERRIDE!!" https://lazyadmin.nl/home-network/unifi-adoption-failed/

## TH13 Backup antes de cada actualización o cambio grande, y al menos dos copias fuera del equipo
- Sub-topic: T06 (also T14)
- Agree: 3 of 3. Notes: a:N28, a:N29, a:N31. Urls: https://deluisio.com/networking/unifi/2025/08/05/how-to-restore-unifi-from-backup/, https://ubiquiti-networks-forum.de/board/thread/13809-final-unifi-network-application-10-x-x/, https://www.sikich.com/insight/migrate-ubiquiti-unifi-controller-to-a-new-server/
- Disagree: none found
- Level: foundation
- Best story: el backup no lleva video de Protect ni logs locales. https://deluisio.com/networking/unifi/2025/08/05/how-to-restore-unifi-from-backup/

## TH14 Al restaurar, misma versión o superior, y después verificá y re-apuntá los equipos
- Sub-topic: T06
- Agree: 3 of 4. Notes: a:N30, a:N26, a:N28, a:N32. Urls: https://www.sikich.com/insight/migrate-ubiquiti-unifi-controller-to-a-new-server/, https://deluisio.com/networking/unifi/2025/08/05/how-to-restore-unifi-from-backup/, https://community.ui.com/releases/UniFi-Network-Application-10-6-101/05283624-0980-4dd7-b8d6-9fa5c4e28da4
- Disagree: none found
- Level: core
- Best story: una versión perdía MC-LAG al restaurar. https://community.ui.com/releases/UniFi-Network-Application-10-6-101/05283624-0980-4dd7-b8d6-9fa5c4e28da4

## TH15 Una VLAN por función, con su DHCP, y bloqueá lo que no tiene que hablar entre sí
- Sub-topic: T07
- Agree: 4 of 5. Notes: a:N33, a:N34, a:N36, a:N35. Urls: https://www.unihosted.com/blog/everything-you-need-to-know-about-vlan-tagging-in-unifi, https://lazyadmin.nl/home-network/unifi-vlan-configuration/, https://community.ui.com/releases/UniFi-Network-Application-11-0-97/15662d06-8122-44e2-a1ba-af5d71b8a045, https://www.wundertech.net/how-to-set-up-a-guest-network-vlan-in-unifi/
- Disagree: https://www.thesmarthomehookup.com/test_install/unifi-network-update-part-2-vlans-wifi-partitioning-and-advanced-features/: deja cámaras en la VLAN principal por carga del router y compensa con reglas y MAC por puerto.
- Level: foundation
- Best story: plan staff 10, invitados 20, CCTV 30 con trunk al AP. https://www.unihosted.com/blog/everything-you-need-to-know-about-vlan-tagging-in-unifi

## TH16 En 2026 la segmentación se hace con zonas (Zone-Based Firewall)
- Sub-topic: T07 (also T13)
- Agree: 3 of 5. Notes: a:N35, a:N64. Urls: https://community.ui.com/releases/UniFi-Network-Application-11-0-97/15662d06-8122-44e2-a1ba-af5d71b8a045, https://www.wundertech.net/how-to-set-up-a-guest-network-vlan-in-unifi/, https://lazyadmin.nl/home-network/unifi-vlan-configuration/
- Disagree: none found
- Level: core
- Best story: 11.0 migra todos los sitios a zonas automáticamente. https://community.ui.com/releases/UniFi-Network-Application-11-0-97/15662d06-8122-44e2-a1ba-af5d71b8a045

## TH17 Puerto de equipo final: VLAN nativa de su red y etiquetadas bloqueadas; uplinks y AP con todo
- Sub-topic: T08
- Agree: 3 of 4. Notes: a:N39, a:N36, a:N40. Urls: https://lazyadmin.nl/home-network/unifi-vlan-configuration/, https://www.unihosted.com/blog/everything-you-need-to-know-about-vlan-tagging-in-unifi, https://lazyadmin.nl/home-network/unifi-adoption-failed/
- Disagree: none found
- Level: foundation
- Best story: switch de terceros que necesitaba la VLAN del AP sin etiquetar. https://lazyadmin.nl/home-network/unifi-adoption-failed/

## TH18 Atá los puertos expuestos (cámaras en exterior) al equipo que corresponde
- Sub-topic: T08
- Agree: 2 of 4. Notes: a:N41, a:N42. Urls: https://www.thesmarthomehookup.com/test_install/unifi-network-update-part-2-vlans-wifi-partitioning-and-advanced-features/, https://community.ui.com/releases/UniFi-Network-Application-10-6-101/05283624-0980-4dd7-b8d6-9fa5c4e28da4
- Disagree: none found
- Level: core
- Best story: arrancar una cámara de la pared y enchufar una laptop. https://www.thesmarthomehookup.com/test_install/unifi-network-update-part-2-vlans-wifi-partitioning-and-advanced-features/

## TH19 2.4 GHz en 20 MHz y solo canales 1, 6 y 11
- Sub-topic: T09
- Agree: 4 of 5. Notes: a:N43. Urls: https://lazyadmin.nl/home-network/optimize-your-unifi-network/, https://www.hostifi.com/support/unifi-wireless-best-practices, https://www.wundertech.net/how-to-optimize-a-unifi-wi-fi-network/, https://std.rocks/improve-wifi-performance-guide.html
- Disagree: none found
- Level: foundation
- Best story: Zigbee en el canal 11 y WiFi en 6 y 11 para darle aire. https://lazyadmin.nl/home-network/optimize-your-unifi-network/

## TH20 En 5 GHz, cuanto más denso, más angosto (40 MHz oficina, 80 MHz casa, 20 MHz alta densidad)
- Sub-topic: T09
- Agree: 4 of 5. Notes: a:N44, a:N45. Urls: https://www.wundertech.net/how-to-optimize-a-unifi-wi-fi-network/, https://www.hostifi.com/support/unifi-wireless-best-practices, https://lazyadmin.nl/home-network/optimize-your-unifi-network/, https://std.rocks/improve-wifi-performance-guide.html
- Disagree: none found sobre el principio; difieren en el valor por defecto.
- Level: core
- Best story: oficina de 300 equipos que bajó a 20 MHz. https://std.rocks/improve-wifi-performance-guide.html

## TH21 Medí el espectro antes de elegir canales, en horario tranquilo
- Sub-topic: T09
- Agree: 4 of 5. Notes: a:N45, a:N49. Urls: https://www.hostifi.com/support/unifi-wireless-best-practices, https://www.wundertech.net/how-to-optimize-a-unifi-wi-fi-network/, https://std.rocks/improve-wifi-performance-guide.html, https://lazyadmin.nl/home-network/optimize-your-unifi-network/
- Disagree: none found
- Level: core
- Best story: el escaneo deja la radio fuera de servicio de 5 a 10 minutos. https://www.hostifi.com/support/unifi-wireless-best-practices

## TH22 Dejá los canales en Auto y usá Channel AI con dos o más AP
- Sub-topic: T09
- Agree: 3 of 5. Notes: a:N47, a:N81. Urls: https://www.wundertech.net/how-to-optimize-a-unifi-wi-fi-network/, https://lazyadmin.nl/home-network/optimize-your-unifi-network/, https://community.ui.com/releases/UniFi-Network-Application-10-6-101/05283624-0980-4dd7-b8d6-9fa5c4e28da4
- Disagree: https://www.hostifi.com/support/unifi-wireless-best-practices: en sus pruebas Auto nunca funcionó como debía. https://std.rocks/improve-wifi-performance-guide.html: elige el canal a mano.
- Level: core
- Best story: optimización nocturna con elección de radios desde 10.6. https://community.ui.com/releases/UniFi-Network-Application-10-6-101/05283624-0980-4dd7-b8d6-9fa5c4e28da4

## TH23 DFS: usalos si están limpios y no hay radar cerca; evitalos si ves caídas
- Sub-topic: T09
- Agree: 1 of 2 por lado (thin evidence). Notes: a:N45, a:N46. Urls: https://std.rocks/improve-wifi-performance-guide.html, https://lazyadmin.nl/home-network/optimize-your-unifi-network/
- Disagree: https://lazyadmin.nl/home-network/optimize-your-unifi-network/ evitarlos; https://std.rocks/improve-wifi-performance-guide.html usarlos.
- Level: core
- Best story: canal 64 limpio contra 36 a 48 saturados. https://std.rocks/improve-wifi-performance-guide.html

## TH24 Bajá la potencia: celdas chicas y más AP rinden más que pocos AP al máximo
- Sub-topic: T10
- Agree: 5 of 5. Notes: a:N50, a:N51, a:N52. Urls: https://lazyadmin.nl/home-network/optimize-your-unifi-network/, https://www.wundertech.net/how-to-optimize-a-unifi-wi-fi-network/, https://std.rocks/improve-wifi-performance-guide.html, https://www.hostifi.com/support/unifi-wireless-best-practices, https://www.purple.ai/en-us/guides/unifi-802-11k-802-11r-fast-roaming
- Disagree: none found (WunderTech nota que la guía residencial de Ubiquiti dice alta salvo AP muy juntos; un solo AP va en alta)
- Level: foundation
- Best story: "probably the number one reason for wireless network issues". https://lazyadmin.nl/home-network/optimize-your-unifi-network/

## TH25 El roaming lo decide el cliente; el AP solo sugiere
- Sub-topic: T11
- Agree: 3 of 6. Notes: a:N53. Urls: https://www.purple.ai/en-us/guides/unifi-802-11k-802-11r-fast-roaming, https://www.wundertech.net/how-to-optimize-a-unifi-wi-fi-network/, https://lazyadmin.nl/home-network/optimize-your-unifi-network/
- Disagree: https://deluisio.com/networking/unifi/2024/08/19/optimizing-wi-fi-roaming-a-guide-to-bss-transition-in-unifi-networks/: describe BSS Transition como si el AP coordinara la decisión con el cliente.
- Level: foundation
- Best story: ninguna

## TH26 BSS Transition siempre activado
- Sub-topic: T11
- Agree: 4 of 6. Notes: a:N55. Urls: https://lazyadmin.nl/home-network/optimize-your-unifi-network/, https://www.wundertech.net/how-to-optimize-a-unifi-wi-fi-network/, https://www.purple.ai/en-us/guides/unifi-802-11k-802-11r-fast-roaming, https://deluisio.com/networking/unifi/2024/08/19/optimizing-wi-fi-roaming-a-guide-to-bss-transition-in-unifi-networks/
- Disagree: none found (WunderTech: apagar si un equipo muy viejo empieza a caerse)
- Level: core
- Best story: ninguna

## TH27 Fast Roaming solo donde lo probaste con todos los tipos de equipo
- Sub-topic: T11 (also T12)
- Agree: 3 of 6 con matices. Notes: a:N56, a:N57. Urls: https://www.wundertech.net/how-to-optimize-a-unifi-wi-fi-network/, https://www.purple.ai/en-us/guides/unifi-802-11k-802-11r-fast-roaming, https://lazyadmin.nl/home-network/optimize-your-unifi-network/
- Disagree: https://lazyadmin.nl/home-network/optimize-your-unifi-network/: suele hacer más mal que bien; https://www.wundertech.net/how-to-optimize-a-unifi-wi-fi-network/ y Ubiquiti (citado): recomendado; https://deluisio.com/networking/unifi/2024/08/13/optimizing-your-unifi-network-a-guide-to-advanced-wi-fi-settings/: activarlo en redes con varios AP.
- Level: core
- Best story: lectores viejos sin conexión en 9 locales. https://www.purple.ai/en-us/guides/unifi-802-11k-802-11r-fast-roaming

## TH28 Mínimo RSSI al final, suave, y solo con solape de cobertura probado
- Sub-topic: T11 (also T16)
- Agree: 2 of 6. Notes: a:N59, a:N60. Urls: https://www.purple.ai/en-us/guides/unifi-802-11k-802-11r-fast-roaming, https://www.wundertech.net/how-to-optimize-a-unifi-wi-fi-network/
- Disagree: https://std.rocks/improve-wifi-performance-guide.html: -70 dBm como regla general en oficina.
- Level: advanced
- Best story: un cliente expulsado repetidas veces termina rechazando el AP. https://www.wundertech.net/how-to-optimize-a-unifi-wi-fi-network/

## TH29 WPA3 y MLO dejan afuera equipos viejos: SSID aparte para legado
- Sub-topic: T12
- Agree: 2 of 3. Notes: a:N61, a:N62. Urls: https://www.purple.ai/en-us/guides/unifi-802-11k-802-11r-fast-roaming, https://www.wundertech.net/how-to-optimize-a-unifi-wi-fi-network/
- Disagree: none found
- Level: core
- Best story: PMF obligatorio en WPA3. https://www.purple.ai/en-us/guides/unifi-802-11k-802-11r-fast-roaming

## TH30 Invitados: zona Hotspot, revisar landing page y comprobar el aislamiento desde un celular
- Sub-topic: T13
- Agree: 3 of 4. Notes: a:N64, a:N65, a:N66, a:N68. Urls: https://www.wundertech.net/how-to-set-up-a-guest-network-vlan-in-unifi/, https://help.cloudunifi.com/unifi/setting-up-hotspot/, https://help.ironwifi.com/configuration-guides/ubiquiti/unifi-hotspot
- Disagree: none found
- Level: core
- Best story: la landing page activada por defecto que nadie pidió. https://www.wundertech.net/how-to-set-up-a-guest-network-vlan-in-unifi/

## TH31 Vouchers y portal: pre-autorización para el portal, post-autorización bloquea privadas
- Sub-topic: T13
- Agree: 3 of 4. Notes: a:N66, a:N67, a:N69. Urls: https://help.cloudunifi.com/unifi/setting-up-hotspot/, https://help.ironwifi.com/configuration-guides/ubiquiti/unifi-hotspot, https://www.wundertech.net/how-to-set-up-a-guest-network-vlan-in-unifi/
- Disagree: none found
- Level: core
- Best story: ninguna

## TH32 Actualizá con demora y por etapas: Official, esperar, probar, desplegar
- Sub-topic: T14
- Agree: 4 of 5. Notes: a:N71, a:N72, a:N74, a:N75. Urls: https://www.hostifi.com/support/hostifi-how-we-handle-unifi-updates, https://forums.lawrencesystems.com/t/unifi-10-5-made-changes-safer-troubleshooting-clients-a-lot-easier-youtube-release/26907, https://community.ui.com/releases/UniFi-Network-Application-10-6-101/05283624-0980-4dd7-b8d6-9fa5c4e28da4, https://community.ui.com/releases/UniFi-Network-Application-11-0-97/15662d06-8122-44e2-a1ba-af5d71b8a045
- Disagree: none found
- Level: core
- Best story: HostiFi saltó la 7.5.174. https://www.hostifi.com/support/hostifi-how-we-handle-unifi-updates

## TH33 Leé las notas de versión antes de un salto mayor
- Sub-topic: T14
- Agree: 3 of 5. Notes: a:N75, a:N31. Urls: https://community.ui.com/releases/UniFi-Network-Application-11-0-97/15662d06-8122-44e2-a1ba-af5d71b8a045, https://ubiquiti-networks-forum.de/board/thread/13809-final-unifi-network-application-10-x-x/, https://community.ui.com/releases/UniFi-Network-Application-11-0-83/d6940379-cd5a-4e61-8596-7e22d647a4ea
- Disagree: none found
- Level: core
- Best story: 11.0 borra el historial de estadísticas y quita USG. https://community.ui.com/releases/UniFi-Network-Application-11-0-97/15662d06-8122-44e2-a1ba-af5d71b8a045

## TH34 Usá Time Machine e historial de cliente antes de tocar nada
- Sub-topic: T15 (also T16)
- Agree: 4 of 4. Notes: a:N76, a:N77, a:N78, a:N79. Urls: https://community.ui.com/releases/UniFi-Network-Application-10-6-101/05283624-0980-4dd7-b8d6-9fa5c4e28da4, https://community.ui.com/releases/UniFi-Network-Application-11-0-97/15662d06-8122-44e2-a1ba-af5d71b8a045, https://forums.lawrencesystems.com/t/unifi-10-5-made-changes-safer-troubleshooting-clients-a-lot-easier-youtube-release/26907, https://www.purple.ai/en-us/guides/unifi-802-11k-802-11r-fast-roaming
- Disagree: none found
- Level: core
- Best story: filtro de clientes que "flapean" en Port Manager. https://community.ui.com/releases/UniFi-Network-Application-10-6-101/05283624-0980-4dd7-b8d6-9fa5c4e28da4

## TH35 Un cambio por vez, probá, y si falla volvé a los valores por defecto
- Sub-topic: T16
- Agree: 4 of 5. Notes: a:N80, a:N81, a:N82. Urls: https://www.wundertech.net/how-to-optimize-a-unifi-wi-fi-network/, https://lazyadmin.nl/home-network/optimize-your-unifi-network/, https://std.rocks/improve-wifi-performance-guide.html, https://www.purple.ai/en-us/guides/unifi-802-11k-802-11r-fast-roaming
- Disagree: none found
- Level: foundation
- Best story: piloto en un local antes de desplegar a la cadena. https://www.purple.ai/en-us/guides/unifi-802-11k-802-11r-fast-roaming

## The big splits
- Fast Roaming (802.11r): a favor https://www.wundertech.net/how-to-optimize-a-unifi-wi-fi-network/ (y Ubiquiti citado), https://deluisio.com/networking/unifi/2024/08/13/optimizing-your-unifi-network-a-guide-to-advanced-wi-fi-settings/; en contra https://lazyadmin.nl/home-network/optimize-your-unifi-network/; condicionado https://www.purple.ai/en-us/guides/unifi-802-11k-802-11r-fast-roaming. Gira en la mezcla de equipos del sitio.
- Canales en Auto o a mano: Auto más Channel AI https://www.wundertech.net/how-to-optimize-a-unifi-wi-fi-network/, https://lazyadmin.nl/home-network/optimize-your-unifi-network/; a mano tras escanear https://www.hostifi.com/support/unifi-wireless-best-practices, https://std.rocks/improve-wifi-performance-guide.html. Gira en cuánto cambia el entorno y cuánto tiempo hay para mirarlo.
- DFS: https://lazyadmin.nl/home-network/optimize-your-unifi-network/ contra https://std.rocks/improve-wifi-performance-guide.html. Gira en si hay radar cerca y en la saturación de los canales bajos.
- Mínimo RSSI: https://std.rocks/improve-wifi-performance-guide.html contra https://www.wundertech.net/how-to-optimize-a-unifi-wi-fi-network/ y https://www.purple.ai/en-us/guides/unifi-802-11k-802-11r-fast-roaming. Gira en la densidad de AP y el solape probado.
- Adopción L3: option 43 (soporte Ubiquiti en https://forums.lawrencesystems.com/t/unifi-l3-persistent-inform-url/20405) contra set-inform (Tom Lawrence en https://forums.lawrencesystems.com/t/unifi-l3-persistent-inform-url/20405, https://www.sikich.com/insight/migrate-ubiquiti-unifi-controller-to-a-new-server/). Gira en si controlás el DHCP del sitio.
- Ancho en 5 GHz: 80 MHz (https://www.wundertech.net/how-to-optimize-a-unifi-wi-fi-network/ citando a Ubiquiti para casas) contra 40 MHz (https://www.hostifi.com/support/unifi-wireless-best-practices, https://lazyadmin.nl/home-network/optimize-your-unifi-network/ urbano) contra 20 MHz (https://std.rocks/improve-wifi-performance-guide.html alta densidad).

## Coverage gaps
- La documentación oficial de help.ui.com no se pudo descargar (HTTP 403 a scripts); entra solo citada por practicantes y por las notas de versión.
- Alarm Manager: solo menciones en notas de versión, sin guía paso a paso.
- Roles y permisos de administradores en Site Manager: poca profundidad.
- DNS "unifi" como método de adopción: mencionado, sin guía de configuración en un DHCP/DNS de terceros.
- Crosstalk Solutions no quedó en el corpus (sin página recuperable en la búsqueda).
