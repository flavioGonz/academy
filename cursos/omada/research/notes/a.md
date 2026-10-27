# Notes: batch a
Pages read: 18. With notes: 18. Skipped: 0. (Todas documentación oficial de TP-Link / Omada; la página de upgrade a 4.1.5 es vieja y se usa solo por su procedimiento y por los cambios de función entre versiones.)

## T01 Arquitectura SDN
- a:N1. Una vez adoptado, el equipo toma las credenciales de dispositivo definidas en el controlador; cambiar entre standalone y controlador en switches pide reset de fábrica.
  - Source: https://support.omadanetworks.com/document/13176/  Quote: "go to Settings > Site > Device Account of the Controller that has adopted the device"
  - Kind: rule of thumb
  - Level: foundation
  - Also: T05
  - Bias: none
- a:N2. Si se configuró un equipo por su web standalone o CLI, la gestión por controlador en la nube queda deshabilitada y el equipo queda en "Preconfigured" hasta habilitarla o resetear.
  - Source: https://www.tp-link.com/us/support/faq/3365  Quote: "will disable the Omada Cloud-Based management and prevent it from connecting to the TP-Link cloud"
  - Kind: mistake
  - Level: foundation
  - Also: T06
  - Bias: none
- a:N3. Un EAP que fue gestionado por su web local tiene el mesh deshabilitado hasta un reset; por eso conviene resetear el AP antes de usarlo como mesh.
  - Source: https://www.omadanetworks.com/cz/support/faq/2283/  Quote: "its Mesh feature will be disabled forever until reset"
  - Kind: mistake
  - Level: core
  - Also: T12
  - Bias: none

## T02 Tipos de controlador
- a:N4. Tres categorías: on-premises (hardware o software), basados en la nube (Omada Cloud Standard con licencia por dispositivo, Omada Cloud Essentials gratis) y gateways integrados (Fusion, ER7212PC).
  - Source: https://support.omadanetworks.com/en/document/13150/  Quote: "grouped into three categories: On-Premises Controllers, Omada Cloud-Based Controllers, and Integrated Gateways"
  - Kind: definition
  - Level: foundation
  - Bias: fabricante, guía de selección de sus propios productos
- a:N5. Capacidad recomendada de hardware: OC200 hasta 25 equipos, OC220 hasta 40, OC300 hasta 160, OC400 hasta 500; software "ilimitado" con recomendación de 10.000 (su afirmación).
  - Source: https://support.omadanetworks.com/en/document/13150/  Quote: "OC200: Recommend≤ 25 Devices"
  - Kind: number
  - Level: foundation
  - Bias: fabricante
- a:N6. Cloud Access y controlador en la nube son cosas distintas: con Cloud Access el controlador sigue corriendo en tu hardware; en Cloud Standard/Essentials el servicio vive en la nube de Omada.
  - Source: https://support.omadanetworks.com/en/document/13150/  Quote: "Cloud Access and a Cloud-Based Controller are different concepts"
  - Kind: definition
  - Level: foundation
- a:N7. On-premises sigue gestionando la red local sin internet; el controlador en la nube depende de internet para gestionar.
  - Source: https://support.omadanetworks.com/en/document/13150/  Quote: "Most controller-based deployments can continue local management when internet access is unavailable"
  - Kind: rule of thumb
  - Level: foundation
- a:N8. Modo MSP: soportado en Software Controller y Cloud Standard; no en Cloud Essentials ni en controladores hardware (tabla comparativa).
  - Source: https://support.omadanetworks.com/en/document/13150/  Quote: "Cloud Essentials provides free, simplified management for less complex environments and does not support MSP Mode"
  - Kind: rule of thumb
  - Level: core
  - Also: T07
- a:N9. Fusion Gateways gestionan solo su propio sistema local, sin multi-sitio; ER7212PC V2 gestiona hasta 22 switches y EAP y dos gateways en total.
  - Source: https://support.omadanetworks.com/en/document/13150/  Quote: "does not support multi-site management"
  - Kind: number
  - Level: core
- a:N10. En el controlador en la nube cada equipo necesita una licencia activa; prueba gratis de 10 licencias por 30 días por TP-Link ID.
  - Source: https://www.tp-link.com/us/support/faq/3365  Quote: "each device should be bound with an activated license"
  - Kind: number
  - Level: foundation
  - Bias: fabricante
- a:N11. Si la licencia vence, el equipo sigue andando con la última configuración, pero se pierden gestión, monitoreo y funciones que dependen del controlador: Portal, Fast Roaming, Schedule.
  - Source: https://www.tp-link.com/us/support/faq/3365  Quote: "some features that depend on the Controller will be disabled, such as Portal, Fast Roaming, Schedule"
  - Kind: rule of thumb
  - Level: core
  - Also: T16
- a:N12. La licencia corre desde que se activa, esté o no asignada a un equipo; la cantidad de desvinculaciones es limitada; aviso por mail 30 días antes.
  - Source: https://www.tp-link.com/us/support/faq/3365  Quote: "The number of times a license can be unbound is limited"
  - Kind: mistake
  - Level: core
- a:N13. No todos los modelos entran al controlador en la nube (ejemplos: EAP610 V3.0, EAP225 V3.20, TL-SG3428MP V3.0); hay lista de compatibilidad.
  - Source: https://www.tp-link.com/us/support/faq/3365  Quote: "not all Omada products support the Omada CBC"
  - Kind: mistake
  - Level: core
- a:N14. Servidores de la nube Omada en AWS: Irlanda, Singapur y Estados Unidos, según dónde se registró el TP-Link ID.
  - Source: https://www.tp-link.com/us/support/faq/3365  Quote: "there are three server nodes"
  - Kind: number
  - Level: core

## T04 Puertos
- a:N15. Puertos por defecto (controlador 5.0.15 en adelante): 8043 HTTPS gestión software, 8088 HTTP, 8843 portal HTTPS, UDP 29810 descubrimiento, TCP 29811/29812 equipos con firmware v4, 29813 upgrade v4, 29814 gestión v5, 29815 info y capturas, 29816 terminal remota, UDP 27001 descubrimiento por la app, 27217 MongoDB.
  - Source: https://support.omadanetworks.com/document/13090/  Quote: "UDP 29810 ... Omada Controller and Omada Discovery Utility discover Omada devices"
  - Kind: template
  - Level: foundation
- a:N16. Puerto nuevo en 6.0: TCP 29817 para datos de monitoreo; tiene que estar abierto.
  - Source: https://support.omadanetworks.com/document/13090/  Quote: "New port in 6.0 TCP 29817 (device monitoring data)"
  - Kind: number
  - Level: foundation
  - Also: T15
- a:N17. Con NAT en el medio, los puertos 29810 a 29817 se reenvían con puerto origen y destino iguales; desde 5.9 los puertos web pueden remapearse.
  - Source: https://support.omadanetworks.com/document/13090/  Quote: "the source and destination ports of the Port Forwarding rules should be all the same"
  - Kind: rule of thumb
  - Level: core
  - Also: T06
- a:N18. En Linux evitar el puerto 443 para el controlador: un usuario no root no puede usarlo y el servicio no arranca. Los puertos de gestión se cambian en omada.properties (/opt/tplink/EAPController/properties).
  - Source: https://support.omadanetworks.com/document/13090/  Quote: "avoid using port 443"
  - Kind: mistake
  - Level: core
  - Also: T03
- a:N19. Historia: dos controladores detrás de la misma IP pública; a uno se le pasan los puertos 29810 a 29817 a 29820 a 29827 y el web a 18043, y se usa Discovery Utility con el puerto en la Inform URL.
  - Source: https://support.omadanetworks.com/document/13090/  Quote: "change ports 29810-29817 to 29820-29827"
  - Kind: story
  - Level: advanced

## T05 Adopción L2
- a:N20. El EAP no sabe dónde está el controlador: manda un broadcast al UDP 29810 en la LAN, el controlador lo escucha y responde.
  - Source: https://support.omadanetworks.com/document/13090/  Quote: "broadcasts a self-introductory message to UDP port 29810 in the LAN"
  - Kind: definition
  - Level: foundation
- a:N21. Adopt Failed por usuario o contraseña: probar las credenciales de la web standalone; si está "Managed by Others", buscarlas en el controlador anterior; si no, reset de fábrica (switch sin botón: consola a 38400 y BootUtil).
  - Source: https://support.omadanetworks.com/document/13176/  Quote: "Choose 38400 as speed and enter BootUtil to reset the device"
  - Kind: technique
  - Level: foundation
- a:N22. "Device does not respond to adopt commands": revisar tags de VLAN en todos los puertos entre equipo y DHCP, loops, ping desde el controlador, y firewall o antivirus en la PC del controlador software.
  - Source: https://support.omadanetworks.com/document/13176/  Quote: "configured with the correct VLAN tags and no other problems like network loops"
  - Kind: test
  - Level: core
  - Also: T16
- a:N23. "Failed to link to uplink AP" en mesh: acortar distancia o sacar obstáculos entre root y mesh AP, o adoptar por otro uplink.
  - Source: https://support.omadanetworks.com/document/13176/  Quote: "Failed to link to uplink AP"
  - Kind: technique
  - Level: core
  - Also: T12

## T06 Adopción L3 y remota
- a:N24. Tres métodos para que un equipo en otra subred o detrás de internet encuentre el controlador: Omada Discovery Utility (Batch Setting), Inform URL en la web standalone, DHCP option 138 con la IP del controlador.
  - Source: https://support.omadanetworks.com/de/document/124358/  Quote: "Three methods for Omada Controller to discover the Omada devices"
  - Kind: technique
  - Level: foundation
- a:N25. Option 138 solo se aplica cuando el cliente renueva DHCP: desconectar y reconectar el switch y el EAP es una forma.
  - Source: https://support.omadanetworks.com/de/document/124358/  Quote: "you need to renew DHCP parameters for the DHCP clients"
  - Kind: mistake
  - Level: core
- a:N26. Escenario VPN: con túnel IPsec entre sedes no hace falta port forwarding; un switch en la sucursal da DHCP con option 138 apuntando a la IP privada del controlador.
  - Source: https://support.omadanetworks.com/de/document/124358/  Quote: "the DHCP Server will tell the EAPs where the Omada Controller is"
  - Kind: story
  - Level: advanced
  - Also: T14
- a:N27. Un sitio solo puede adoptar un gateway: si el gateway de la sucursal se adopta, va en un sitio nuevo.
  - Source: https://support.omadanetworks.com/de/document/124358/  Quote: "one site can only adopt one gateway"
  - Kind: rule of thumb
  - Level: foundation
  - Also: T07
- a:N28. Omada Central: copiar el Site URL desde Global View > Dashboard y pegarlo en System Tools > Controller Settings del equipo (habilitando Cloud-based Controller Management) o en Discovery Utility; aparece en Pending.
  - Source: https://www.omadanetworks.com/ph/support/faq/4580/  Quote: "paste the Site URL copied from the controller into the Inform URL/IP Address field"
  - Kind: technique
  - Level: foundation
- a:N29. En el controlador en la nube, un equipo de fábrica con internet se conecta solo a la nube (ZTP) y queda adoptado; "Preconfigured" significa que todavía no habló con el controlador.
  - Source: https://www.tp-link.com/us/support/faq/3365  Quote: "it will automatically connect to the TP-Link Cloud"
  - Kind: definition
  - Level: core

## T07 Sitios y MSP
- a:N30. MSP se activa en Global Settings > Controller Settings; agrega clientes (nuevo, copiar existente, importar) y dos niveles de roles: MSP y Customer, con Main Administrator, Administrator y Viewer.
  - Source: https://www.tp-link.com/de/support/faq/4276  Quote: "The system provides two levels of roles"
  - Kind: technique
  - Level: core
- a:N31. Límite de clientes MSP: 100 en v5, 500 en v6, ajustable con customer.limit en omada.properties; subirlo no sube la escala de equipos.
  - Source: https://www.tp-link.com/de/support/faq/4276  Quote: "For Omada controller v6, the upper limitation of MSP Customer is 500"
  - Kind: number
  - Level: advanced
- a:N32. Un Administrator común no puede migrar clientes ni hacer backups automáticos; eso queda para el Main Administrator.
  - Source: https://www.tp-link.com/de/support/faq/4276  Quote: "they do not have permission to perform customer migrations or automatic data backups"
  - Kind: rule of thumb
  - Level: core
  - Also: T16

## T08 LAN/VLAN y perfiles
- a:N33. VLAN para switches con router de terceros: crear la red en Network Config > Network Settings > LAN con DHCP Server Device en None, marcar los puertos de acceso; los puertos no marcados que siguen en trunk llevan la VLAN tagueada.
  - Source: https://www.tp-link.com/us/support/faq/4084  Quote: "Any unselected port that remains in Trunk mode will automatically carry the VLAN as tagged traffic"
  - Kind: technique
  - Level: foundation
- a:N34. Configurar la VLAN solo en el switch no le da IP al cliente: hace falta interfaz VLAN y DHCP en el router, el uplink tagueado y el puerto de acceso con la VLAN como nativa.
  - Source: https://www.tp-link.com/us/support/faq/4084  Quote: "Configuring the VLAN only on the switch does not provide the client with an IP address"
  - Kind: mistake
  - Level: foundation
- a:N35. Legal DHCP Servers en la red: el gateway y los switches Omada aceptan solo los DHCP indicados (protección contra DHCP truchos).
  - Source: https://www.tp-link.com/us/support/faq/4084  Quote: "clients get IP addresses only from the DHCP servers specified here"
  - Kind: technique
  - Level: core
- a:N36. Puertos LAN del gateway: todos tienen como nativa la red por defecto (PVID 1); al agregar un puerto a otra red, la lleva tagueada. Se recomienda usar la red por defecto como VLAN de gestión.
  - Source: https://www.omadanetworks.com/lk/support/faq/3157/  Quote: "it is recommended that you can use the default network as the management VLAN"
  - Kind: rule of thumb
  - Level: foundation
- a:N37. Al crear una interfaz VLAN el controlador crea solo el perfil de puerto de esa red; se bindean perfiles a puertos desde Devices > switch > Ports.
  - Source: https://www.omadanetworks.com/eg/support/faq/4122/  Quote: "the controller will automatically create a profile for the corresponding network"
  - Kind: technique
  - Level: core

## T09 ACL
- a:N38. VLAN separa capa 2, pero si el gateway rutea entre VLAN se ven igual: para aislar hacen falta ACL o reglas de firewall.
  - Source: https://www.tp-link.com/us/support/faq/4084  Quote: "devices in VLAN 10 and VLAN 20 may still communicate"
  - Kind: mistake
  - Level: foundation
- a:N39. Las ACL de switch se evalúan de arriba hacia abajo: el permit al servidor puntual va arriba del deny entre redes. La ACL de switch funciona por lista negra, así que "solo interno" se arma con un permit a las subredes y un deny any.
  - Source: https://www.omadanetworks.com/eg/support/faq/4122/  Quote: "ACLs take effect based on a top-down priority"
  - Kind: technique
  - Level: core

## T10 RF
- a:N40. 2,4 GHz: solo 1, 6 y 11 no se solapan, a 20 MHz. 5 GHz: 40 MHz como valor empírico general; 20 MHz con mucha interferencia, 80 o más con poca.
  - Source: https://www.tp-link.com/us/support/faq/2511  Quote: "A generally good empirical value is 40 MHz"
  - Kind: rule of thumb
  - Level: foundation
- a:N41. Más potencia no es mejor: con APs a menos de 12 m bajar potencia; ejemplo de 28 dBm a 25 dBm y probar. EAP de techo al centro, 10 a 12 m entre ellos.
  - Source: https://www.tp-link.com/us/support/faq/2511  Quote: "A larger Tx power is not always better"
  - Kind: number
  - Level: foundation
- a:N42. WLAN Optimization (RRM) en Network Config > Network Settings > WLAN: corta internet varios minutos mientras escanea; programar en horario bajo y separado al menos 10 minutos del reboot programado; historial con "Apply Previous Settings" para volver atrás.
  - Source: https://www.tp-link.com/us/support/faq/2511  Quote: "Your internet connection will be unavailable for several minutes during scanning and optimization"
  - Kind: mistake
  - Level: core

## T11 Roaming
- a:N43. Roaming falla si el SSID no es idéntico (nombre, seguridad, cifrado, clave) o si los APs están en sitios distintos: los perfiles de roaming son por sitio.
  - Source: https://support.omadanetworks.com/en/document/13229/  Quote: "roaming profiles are strictly site-bound"
  - Kind: rule of thumb
  - Level: foundation
- a:N44. Fast Roaming (802.11k/v) en Site Settings > Wireless Features; 802.11r se desactiva por SSID si hay clientes viejos que pierden internet tras roamear.
  - Source: https://support.omadanetworks.com/en/document/13229/  Quote: "disable the 802.11r protocol on that SSID"
  - Kind: test
  - Level: core
- a:N45. Controlador 6.2 agrega Non-Stick Roaming, Ping-Pong Roaming Suppression (solo desde el controlador, no la app), AI Roaming y Band Steering.
  - Source: https://support.omadanetworks.com/en/document/13229/  Quote: "Omada Controller v6.2 introduces specific automated tuning mechanisms"
  - Kind: technique
  - Level: advanced
- a:N46. APs muy juntos: el cliente nunca baja del umbral para roamear; bajar potencia. "Lock to AP" en un cliente anula el roaming.
  - Source: https://support.omadanetworks.com/en/document/13229/  Quote: "a moving client may never drop below the necessary threshold"
  - Kind: mistake
  - Level: core
  - Also: T10

## T12 Mesh
- a:N47. Mesh: máximo 3 saltos, máximo 4 downlink por uplink AP, señal recomendada del uplink entre -40 y -62 dBm, hasta 180 m en exterior en campo abierto.
  - Source: https://www.omadanetworks.com/cz/support/faq/2283/  Quote: "The Maximum Hop number is 3"
  - Kind: number
  - Level: core
- a:N48. Mesh es para extender cobertura, no capacidad; ejemplo EAP225-Outdoor: 50 a 60 clientes para toda la red mesh. Alta densidad, cableado. Topología estrella mejor que cadena.
  - Source: https://www.omadanetworks.com/cz/support/faq/2283/  Quote: "not aim to expand the wireless client capacity"
  - Kind: rule of thumb
  - Level: core
- a:N49. Sin controlador corriendo, mesh mantiene la cobertura básica pero sin Auto Failover ni Fast Roaming; Auto Failover viene apagado por defecto.
  - Source: https://www.omadanetworks.com/cz/support/faq/2283/  Quote: "This feature is off by default"
  - Kind: rule of thumb
  - Level: core
  - Also: T02

## T13 Portal
- a:N50. Portal en Site Settings > Authentication > Portal (controlador 5.9 a 6): No Authentication, Simple Password, Hotspot (Voucher, Local User, SMS, RADIUS, Form Auth), RADIUS Server (incorporado desde 5.12), LDAP externo, portal externo.
  - Source: https://support.omadanetworks.com/en/document/13285/  Quote: "Omada Controller includes a built-in RADIUS Server from version 5.12 onwards"
  - Kind: definition
  - Level: core
- a:N51. Para que el portal funcione el controlador tiene que estar corriendo; Pre-Authentication Access deja pasar URLs o subredes antes de autenticar; Authentication-Free Client exime IPs o MACs.
  - Source: https://support.omadanetworks.com/en/document/13285/  Quote: "When using the Portal, make sure your Omada Controller is running"
  - Kind: rule of thumb
  - Level: core
  - Also: T02
- a:N52. Upgrades que rompen configuración: al pasar al controlador SDN 4.1.5, Portal y Access Control no se migraban solos y había que reconfigurarlos a mano.
  - Source: https://www.omadanetworks.com/us/omada-sdn/controller-upgrade/  Quote: "If you want to restore Portal configuration, go to Settings > Authentication and configure Portal manually"
  - Kind: story
  - Level: advanced
  - Also: T15

## T14 VPN de sitio
- a:N53. Auto IPsec: los dos gateways en sitios distintos del mismo controlador, ambos con IP pública en la WAN (sin NAT), y LAN que no se solapen.
  - Source: https://www.omadanetworks.com/us/support/faq/4699/  Quote: "the LAN networks of the remote site and current site shall not overlap"
  - Kind: rule of thumb
  - Level: core
- a:N54. Manual IPsec detrás de NAT: abrir UDP 500 y 4500 y usar Local ID / Remote ID tipo Name; con un extremo standalone, IKEv1 y una sola red local.
  - Source: https://support.omadanetworks.com/de/document/124358/  Quote: "make sure that UDP port 500 and UDP port 4500 are open on the NAT device"
  - Kind: technique
  - Level: advanced
- a:N55. Verificar el túnel en Network Config > VPN Status > Site-to-Site VPN > IPsec; en ER605 standalone, VPN > IPsec > IPsec SA.
  - Source: https://support.omadanetworks.com/de/document/124358/  Quote: "When corresponding entries are displayed in the tables, the VPN tunnel is successfully established"
  - Kind: test
  - Level: core

## T15 Firmware
- a:N56. Controlador hardware: upgrade local o por nube en Global View > System Settings; tarda 6 a 8 minutos y el controlador queda offline. Downgrade solo local y manual.
  - Source: https://tp-link.com/support/faq/3684  Quote: "It will take about 6-8 minutes to finish the firmware upgrade process"
  - Kind: number
  - Level: core
- a:N57. Downgrade de controlador software: desinstalar sin guardar datos e instalar la versión vieja; un backup de versión más nueva no se restaura en una más vieja. Guardar un backup por cada versión.
  - Source: https://tp-link.com/support/faq/3684  Quote: "it is still highly recommended keeping a backup file for every firmware version"
  - Kind: rule of thumb
  - Level: core
  - Also: T16
- a:N58. Canales Beta y Release Candidate (Early Access) disponibles; usarlos con cuidado.
  - Source: https://tp-link.com/support/faq/3684  Quote: "Please use these firmwares with caution since it may be unstable"
  - Kind: rule of thumb
  - Level: core
- a:N59. Antes de subir de versión de controlador, revisar lista de compatibilidad: el controlador solo gestiona equipos con firmware soportado.
  - Source: https://www.omadanetworks.com/us/omada-sdn/controller-upgrade/  Quote: "can configure and manage only the devices with supported firmware"
  - Kind: rule of thumb
  - Level: foundation

## T16 Backup, migración, troubleshooting
- a:N60. Migration (controlador 6.2.10 en adelante): Site Migration y Controller Migration, en tres pasos: exportar, importar en el destino, migrar equipos con la IP o Inform URL del destino; "Forget Devices" en el viejo solo cuando todos estén Connected en el nuevo.
  - Source: https://www.tp-link.com/us/support/faq/3589  Quote: "click Forget Devices on the previous Controller to finish the migration process"
  - Kind: technique
  - Level: core
- a:N61. Desde 5.13.11.41 la migración solo importa archivos de la misma versión Major.Minor.Patch; destino igual o mayor.
  - Source: https://www.tp-link.com/us/support/faq/3589  Quote: "only when importing a configuration file from a controller with the same Major. Minor. Patch version number"
  - Kind: mistake
  - Level: core
- a:N62. Desde 5.15.24, saltear la importación y pasar directo a migrar equipos hace que el destino no los adopte solo. El orden importa.
  - Source: https://www.tp-link.com/us/support/faq/3589  Quote: "the target controller will fail to adopt the devices automatically"
  - Kind: mistake
  - Level: core
- a:N63. ER7212PC: su backup solo vuelve a otro ER7212PC; no se cruza con software, hardware ni Central. Migrar de on-premises a nube deja equipos "Unactivated" hasta asignar licencia.
  - Source: https://www.tp-link.com/us/support/faq/3589  Quote: "Its backup file cannot be imported into other controllers"
  - Kind: mistake
  - Level: advanced
  - Also: T02
- a:N64. Procedimiento clásico de upgrade entre equipos: backup en Backup & Restore eligiendo días de datos retenidos, instalar el nuevo, restaurar, y después actualizar firmware de equipos uno por uno o en lote.
  - Source: https://www.omadanetworks.com/us/omada-sdn/controller-upgrade/  Quote: "Back up your current controller"
  - Kind: template
  - Level: foundation
  - Also: T15

## Disagreements seen
- Capacidad de hardware: la comparación oficial actual recomienda OC200 hasta 25 equipos (https://support.omadanetworks.com/en/document/13150/); un practicante de 2022 citaba OC200 hasta 100 y OC300 hasta 500 (https://evanmccann.net/blog/2022/3/tp-link-omada-overview). Recomendado vs máximo, y cambió con los años.
- Cloud gratis: la guía oficial dice que Cloud Essentials es gratis y Standard paga por licencia (https://support.omadanetworks.com/en/document/13150/); una comparativa dice "gratis para 1 sitio, niveles pagos" (https://simeononsecurity.com/articles/ubiquiti-unifi-vs-tp-link-omada/), dato que no coincide con la documentación.

## Best stories
- Dos controladores detrás de la misma IP pública, uno corrido a 29820 a 29827: https://support.omadanetworks.com/document/13090/
- La sucursal por VPN donde un switch reparte option 138 con la IP privada del controlador: https://support.omadanetworks.com/de/document/124358/
- WLAN Optimization que corta internet varios minutos y choca con el reboot programado: https://www.tp-link.com/us/support/faq/2511
- La licencia vencida: la red sigue andando pero el portal y el fast roaming se apagan: https://www.tp-link.com/us/support/faq/3365
- El portal que hubo que reconfigurar a mano al pasar a 4.1.5: https://www.omadanetworks.com/us/omada-sdn/controller-upgrade/
