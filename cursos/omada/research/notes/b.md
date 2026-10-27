# Notes: batch b
Pages read: 9. With notes: 9. Skipped: 0. (Practicantes: guías de Docker, una reseña larga, un hilo de foro escéptico, guías de un hosting de controladores y una comparativa con cifras dudosas.)

## T01 Arquitectura SDN
- b:N1. Omada es el único de su grupo (frente a UniFi e Instant On) donde cada equipo puede funcionar solo, con su web o CLI; algunas funciones L2+/L3 de switches JetStream solo están en standalone.
  - Source: https://evanmccann.net/blog/2022/3/tp-link-omada-overview  Quote: "Omada is the only of the three which allow all individual devices to operate on their own"
  - Kind: definition
  - Level: foundation
  - Bias: TP-Link le dio el equipo al autor
- b:N2. Todo cambio entre modo controlador y standalone en switches pide reset de fábrica.
  - Source: https://evanmccann.net/blog/2022/3/tp-link-omada-overview  Quote: "Every change between controller and standalone mode requires a factory reset"
  - Kind: rule of thumb
  - Level: foundation
- b:N3. Al adoptarse, la GUI local del AP o del gateway deja de servir y el equipo usa las credenciales que define Omada.
  - Source: https://www.hostifi.com/support/omada-how-to-adopt-a-new-access-point  Quote: "Once the AP is adopted into Omada, the local GUI becomes non-functional"
  - Kind: rule of thumb
  - Level: foundation
  - Bias: empresa que vende hosting de controladores

## T02 Tipos de controlador
- b:N4. En 2022 un practicante listaba OC200 hasta 100 equipos, OC300 hasta 500, software hasta 1.500 según el hardware (su afirmación; la cifra oficial actual es menor como "recomendado").
  - Source: https://evanmccann.net/blog/2022/3/tp-link-omada-overview  Quote: "OC200 - up to 100 devices"
  - Kind: number
  - Level: foundation
- b:N5. Historia: una iglesia corría el controlador en la PC de la mesa técnica; se dormía o se reiniciaba por actualizaciones y los equipos quedaban desconectados hasta que alguien lo levantaba. Lo pasaron a un equipo dedicado.
  - Source: https://whitkirkchurch.org.uk/tech-blog/2021/08/installing-an-omada-sdn-controller-on-a-raspberry-pi-using-docker/  Quote: "the system going to sleep or restarting to install updates"
  - Kind: story
  - Level: foundation
  - Also: T03
- b:N6. La cloud integration es opcional: el controlador no habló con la nube hasta que el autor vinculó un TP-Link ID; quien no confía en la nube puede autoalojar detrás de su firewall.
  - Source: https://evanmccann.net/blog/2022/3/tp-link-omada-overview  Quote: "It didn't reach out to any cloud services until I chose to link my TP-Link ID"
  - Kind: rule of thumb
  - Level: core
- b:N7. Para autoalojar, elegir "Create a Local Account" en el wizard: el controlador no depende de la nube de TP-Link.
  - Source: https://lazyadmin.nl/home-network/omada-controller-docker/  Quote: "pick Create a Local Account"
  - Kind: technique
  - Level: foundation
  - Also: T03
- b:N8. Comparativa afirma que Omada Cloud es "gratis para 1 sitio" y que el controlador en la nube gestiona hasta 100 sitios (cifras que no coinciden con la documentación oficial actual).
  - Source: https://simeononsecurity.com/articles/ubiquiti-unifi-vs-tp-link-omada/  Quote: "Free for up to 1 site, paid tiers available"
  - Kind: number
  - Level: foundation
  - Bias: comparativa genérica, cifras sin fuente

## T03 Instalar el controlador software
- b:N9. TP-Link no publica imagen Docker oficial; la que se usa es la comunitaria mbentley/omada-controller, que trae Java y MongoDB adentro.
  - Source: https://computingforgeeks.com/omada-controller-docker/  Quote: "TP-Link does not publish an official Docker image"
  - Kind: definition
  - Level: core
  - Also: T05
- b:N10. Probado en julio de 2026 con 6.2.10.17: con red bridge y puertos publicados la web anda pero los APs nunca aparecen; la solución es network_mode host porque el broadcast de descubrimiento no cruza el bridge.
  - Source: https://computingforgeeks.com/omada-controller-docker/  Quote: "Skip this and adoption silently breaks"
  - Kind: mistake
  - Level: core
  - Also: T05
- b:N11. stop_grace_period de 60 segundos para que MongoDB cierre limpio; sin eso, riesgo de base corrupta.
  - Source: https://lazyadmin.nl/home-network/omada-controller-docker/  Quote: "MongoDB needs a clean shutdown"
  - Kind: technique
  - Level: core
  - Also: T16
- b:N12. El controlador usa unos 1,9 GB de RAM al arrancar (su medición); conviene 4 GB libres. El arranque tarda 1 a 2 minutos: no reiniciar por impaciencia.
  - Source: https://lazyadmin.nl/home-network/omada-controller-docker/  Quote: "The Omada Controller uses around 1.9 GB of RAM after startup"
  - Kind: number
  - Level: core
- b:N13. Controlador 6.x usa un MongoDB que pide AVX: no corre en Raspberry Pi 4 (usar tag 5 o una mini PC con Intel de 6ª generación o más).
  - Source: https://lazyadmin.nl/home-network/omada-controller-docker/  Quote: "requires the AVX instruction set"
  - Kind: mistake
  - Level: core
- b:N14. La misma advertencia de AVX en NAS Synology: si el NAS no tiene AVX, usar la imagen de la rama 5. Guía probada con 6.3.0.111.
  - Source: https://mariushosting.com/how-to-install-tp-link-omada-controller-on-your-synology-nas/  Quote: "If your NAS does NOT support AVX"
  - Kind: mistake
  - Level: core
- b:N15. Host networking no sirve en Docker Desktop de Windows o macOS: ahí, Inform URL.
  - Source: https://lazyadmin.nl/home-network/omada-controller-docker/  Quote: "Host networking does not work on Docker Desktop for Windows or macOS"
  - Kind: mistake
  - Level: core
  - Also: T06
- b:N16. La región en el wizard define canales legales y potencia: elegir el país real.
  - Source: https://computingforgeeks.com/omada-controller-docker/  Quote: "it sets the legal wireless channels and transmit power for your country"
  - Kind: rule of thumb
  - Level: foundation
  - Also: T10
- b:N17. El certificado propio se sube como un único .pfx (cert más clave con openssl pkcs12) y se fija el Controller Hostname/IP al nombre; importa para el portal cautivo.
  - Source: https://whitkirkchurch.org.uk/tech-blog/2021/08/installing-an-omada-sdn-controller-on-a-raspberry-pi-using-docker/  Quote: "The Omada controller only supports uploading one file"
  - Kind: technique
  - Level: advanced
  - Also: T13
- b:N18. Muchas variables del contenedor se usan solo en el primer arranque y después quedan en la base; para cambiar puertos hace falta WEB_CONFIG_OVERRIDE=true.
  - Source: https://lazyadmin.nl/home-network/omada-controller-docker/  Quote: "the controller stores port configuration in its database after the first run"
  - Kind: mistake
  - Level: advanced
  - Also: T04

## T04 Puertos
- b:N19. Puertos a abrir en el host: 8043/tcp, 29811 a 29817/tcp, 29810/udp, 27001/udp; 8843 para portal.
  - Source: https://computingforgeeks.com/omada-controller-docker/  Quote: "29810/udp, 29811 to 29817, and 27001/udp"
  - Kind: template
  - Level: foundation

## T05 Adopción L2
- b:N20. Si no aparece nada para adoptar, casi siempre el equipo está en otra VLAN o subred que el controlador.
  - Source: https://computingforgeeks.com/omada-controller-docker/  Quote: "the device is almost always on a different VLAN or subnet from the controller"
  - Kind: test
  - Level: foundation
- b:N21. Al adoptar puede saltar "Adopt Failed" pidiendo usuario y clave: son los que se pusieron en la GUI local del equipo.
  - Source: https://www.hostifi.com/support/omada-how-to-adopt-a-gateway-to-the-controller  Quote: "Simply enter in the username and password you used to setup the gateway"
  - Kind: technique
  - Level: foundation

## T06 Adopción L3 y remota
- b:N22. Gateway ER605: sale con WAN en DHCP y LAN 192.168.0.1/24; se configura internet en la GUI, se pega la Inform URL en System Tools > Controller Settings (habilitando cloud-based controller management) y se adopta desde Pending.
  - Source: https://www.hostifi.com/support/omada-how-to-adopt-a-gateway-to-the-controller  Quote: "paste in your inform URL from earlier"
  - Kind: technique
  - Level: foundation
- b:N23. La Inform URL se toma de Settings > Controller > Access Config del controlador.
  - Source: https://www.hostifi.com/support/omada-how-to-adopt-a-new-access-point  Quote: "Scroll down to the section 'Access Config'"
  - Kind: technique
  - Level: foundation
- b:N24. Para equipos nuevos sin acceso a su web, Inform URL o DHCP option 138; host networking es lo más simple si todo está en la misma subred.
  - Source: https://lazyadmin.nl/home-network/omada-controller-docker/  Quote: "via DHCP Option 138"
  - Kind: rule of thumb
  - Level: core

## T08 LAN/VLAN
- b:N25. Configurar VLAN de gestión es más difícil de lo que debería (opinión del autor).
  - Source: https://evanmccann.net/blog/2022/3/tp-link-omada-overview  Quote: "Configuring management VLANs is harder than it should be"
  - Kind: mistake
  - Level: core
- b:N26. Esquema de nombres JetStream: TL-S + velocidad (G gigabit, X 10G) + gestión (2 smart, 3 o 5 full managed) + uplinks + puertos + sufijos PoE (P, MP, HP, HPP). En modo controlador, smart y full managed exponen las mismas funciones.
  - Source: https://evanmccann.net/blog/2022/3/tp-link-omada-overview  Quote: "In controller mode, the features on smart and fully managed switches are the same"
  - Kind: template
  - Level: foundation

## T09 ACL y seguridad
- b:N27. Escepticismo de seguridad: un practicante cuenta un switch TP-Link cuya IP de gestión era alcanzable desde cualquier VLAN; otro no confía en TP-Link para clientes de empresa.
  - Source: https://forums.lawrencesystems.com/t/tp-link-omada-followup/17893  Quote: "I don't trust the security of TP-Link for any business that we would support"
  - Kind: story
  - Level: core
  - Also: T15

## T14 VPN
- b:N28. Los gateways Omada cubren VPN de sitio a sitio "OK", pero para acceso remoto de usuarios se quedan cortos (2022: sin RADIUS para VPN, logs limitados). Recomendación: switches y APs Omada detrás de otro firewall si se necesita routing o VPN avanzada.
  - Source: https://evanmccann.net/blog/2022/3/tp-link-omada-overview  Quote: "As a solution for site-to-site VPNs, it's OK"
  - Kind: rule of thumb
  - Level: core
  - Also: T02

## T15 Firmware
- b:N29. Un usuario en un año vio una sola actualización de firmware en un switch; menos frecuente que Ubiquiti (su experiencia, 2023).
  - Source: https://forums.lawrencesystems.com/t/tp-link-omada-followup/17893  Quote: "TP-Links firmware updates are few and far between"
  - Kind: story
  - Level: core
- b:N30. Comparativa: actualizaciones de Omada típicamente trimestrales contra mensuales en UniFi (su afirmación).
  - Source: https://simeononsecurity.com/articles/ubiquiti-unifi-vs-tp-link-omada/  Quote: "typically quarterly vs monthly"
  - Kind: number
  - Level: core
- b:N31. Para saltos de versión mayor del controlador (5.x a 6.x), no saltear versiones: de a una, verificando que arranque limpio, con backup antes.
  - Source: https://lazyadmin.nl/home-network/omada-controller-docker/  Quote: "don't skip versions"
  - Kind: rule of thumb
  - Level: core
- b:N32. Lo mismo de otro practicante: backup primero y no saltar varias versiones mayores de una.
  - Source: https://computingforgeeks.com/omada-controller-docker/  Quote: "do not jump multiple major versions in one hop"
  - Kind: rule of thumb
  - Level: core

## T16 Backup y troubleshooting
- b:N33. Backup automático en Settings > Maintenance > Backup Schedule; semanal alcanza en redes chicas; mejor guardarlo en un servidor de archivos (SFTP) para que sobreviva si muere el host.
  - Source: https://lazyadmin.nl/home-network/omada-controller-docker/  Quote: "switch to Save to File Server"
  - Kind: technique
  - Level: foundation
- b:N34. Restore en instalación nueva: crear cuenta local en el paso 1 del wizard y en el paso 2 "Restore from Backup File" con el .cfg; la cuenta creada se pisa con la del backup.
  - Source: https://lazyadmin.nl/home-network/omada-controller-docker/  Quote: "the local account you created in step 1 gets overwritten by the backup"
  - Kind: technique
  - Level: core
- b:N35. Nunca "docker compose down -v" al actualizar: borra los volúmenes y toda la configuración.
  - Source: https://lazyadmin.nl/home-network/omada-controller-docker/  Quote: "Never use docker compose down -v during an update"
  - Kind: mistake
  - Level: core
- b:N36. Además del export del controlador, tar del volumen de datos: ese tar más el compose reconstruyen el controlador en otro host.
  - Source: https://computingforgeeks.com/omada-controller-docker/  Quote: "That tarball plus the Compose file is everything you need"
  - Kind: technique
  - Level: core
- b:N37. Contenedor que arranca y se cae: memoria o puertos; JAVA_MAX_HEAP_SIZE=1024m en hosts chicos.
  - Source: https://lazyadmin.nl/home-network/omada-controller-docker/  Quote: "JAVA_MAX_HEAP_SIZE=1024m"
  - Kind: technique
  - Level: advanced

## Disagreements seen
- Confianza en TP-Link: https://forums.lawrencesystems.com/t/tp-link-omada-followup/17893 (no lo usaría en empresas por historial de seguridad) frente a https://evanmccann.net/blog/2022/3/tp-link-omada-overview (lo recomienda para negocios con necesidades básicas, ideal detrás de otro firewall).
- Router Omada sí o no: https://evanmccann.net/blog/2022/3/tp-link-omada-overview sugiere firewall de terceros para routing y VPN avanzada; la documentación oficial empuja el gateway Omada como centro (https://support.omadanetworks.com/en/document/13150/).
- Dónde correr el controlador: Docker comunitario (https://lazyadmin.nl/home-network/omada-controller-docker/, https://computingforgeeks.com/omada-controller-docker/) frente a hardware o nube oficiales (https://support.omadanetworks.com/en/document/13150/), sin soporte oficial para la imagen.
- Frecuencia de firmware: pocas actualizaciones para un usuario (https://forums.lawrencesystems.com/t/tp-link-omada-followup/17893) frente a la documentación que muestra canales Beta/RC y push en la nube (https://tp-link.com/support/faq/3684).

## Best stories
- La PC de la mesa técnica que se dormía y dejaba la red sin controlador: https://whitkirkchurch.org.uk/tech-blog/2021/08/installing-an-omada-sdn-controller-on-a-raspberry-pi-using-docker/
- Docker en bridge: la web anda, los APs nunca aparecen: https://computingforgeeks.com/omada-controller-docker/
- La Raspberry Pi 4 que no arranca el controlador 6 por falta de AVX: https://lazyadmin.nl/home-network/omada-controller-docker/
- El "Adopt Failed" que pide la clave de la GUI local: https://www.hostifi.com/support/omada-how-to-adopt-a-gateway-to-the-controller
- El switch con la IP de gestión alcanzable desde cualquier VLAN: https://forums.lawrencesystems.com/t/tp-link-omada-followup/17893
