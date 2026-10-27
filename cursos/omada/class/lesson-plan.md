# Plan del curso: TP-Link Omada, controlador SDN de punta a punta

Público: técnicos instaladores y de soporte de IES, con base de redes. Nivel inicial a intermedio. Versión de referencia: Omada Controller 6.x (las guías leídas citan 6.2.10.17 y 6.3.0.111, vigentes a octubre de 2026). 27 páginas leídas: 18 de documentación oficial (support.omadanetworks.com, tp-link.com, omadanetworks.com) y 9 de practicantes.

Cada bloque: handle · N de M fuentes · idea · por qué importa · historia · laboratorio · regla.

## Arco 1. Elegir y levantar el controlador
Por qué este arco: antes de configurar una sola VLAN hay que decidir dónde vive el controlador, levantarlo bien y lograr que los equipos lo encuentren; es lo que más llamadas de soporte genera al principio. Termina con un controlador andando y un equipo adoptado, en la misma subred y desde otra.

### 01 Dónde vive
- Fuentes: 5 de 9 (TH01). Discrepa simeononsecurity sobre el modelo de precios de la nube.
- Idea: hay tres familias: on-premises (software u OC200/OC220/OC300/OC400), en la nube (Omada Central Essentials gratis, Standard con licencia por equipo) y gateways integrados (Fusion, ER7212PC). Cloud Access no es controlador en la nube.
- Por qué importa: define si la red se gestiona sin internet, quién mantiene el host y si hay costo de licencias.
- Historia: con licencia vencida en la nube, la red sigue andando pero se apagan Portal, Fast Roaming y Schedule (https://www.tp-link.com/us/support/faq/3365). Capacidad recomendada OC200 hasta 25 equipos, OC400 hasta 500 (https://support.omadanetworks.com/en/document/13150/).
- Laboratorio: Admin · 10 min. Llenar una tabla de decisión para tres obras tipo.
- Regla: el controlador se elige por dónde corre el servicio y por la cifra recomendada, no por la máxima.

### 02 Host dedicado
- Fuentes: 4 de 5 (TH08), con TH09 a TH11. El fabricante no da imagen Docker oficial.
- Idea: si lo autoalojás, equipo dedicado, cuenta local, Docker con red host, CPU con AVX para la versión 6, y tiempo de cierre para MongoDB.
- Por qué importa: un controlador que se duerme o no ve broadcasts deja equipos sin gestión.
- Historia: la PC de la mesa técnica que se dormía (https://whitkirkchurch.org.uk/tech-blog/2021/08/installing-an-omada-sdn-controller-on-a-raspberry-pi-using-docker/); la web anda pero los APs nunca aparecen en red bridge (https://computingforgeeks.com/omada-controller-docker/); Pi 4 sin AVX (https://lazyadmin.nl/home-network/omada-controller-docker/).
- Laboratorio: Foco · 20 min. Compose con red host en una VM Linux.
- Regla: controlador propio en host dedicado, red host, AVX y sesenta segundos para cerrar.

### 03 Adopción limpia
- Fuentes: 4 de 5 (TH06) y 3 de 4 (TH15).
- Idea: el equipo grita por UDP 29810 en su subred; el controlador responde. Equipo usado, reset de fábrica. Adopt Failed se lee: credenciales, sin respuesta, uplink mesh.
- Por qué importa: es el primer paso de cada obra y el error más común en soporte.
- Historia: el Adopt Failed que pide la clave puesta en la GUI local (https://www.hostifi.com/support/omada-how-to-adopt-a-gateway-to-the-controller); switch sin botón de reset: consola a 38400 y BootUtil (https://support.omadanetworks.com/document/13176/).
- Laboratorio: Campo · 15 min. Adoptar un EAP en la misma VLAN y forzar un Adopt Failed.
- Regla: si no aparece en Pending, primero la VLAN; si falla, leer el mensaje.

### 04 Tres caminos
- Fuentes: 6 de 7 (TH17) y 3 de 3 (TH12).
- Idea: para otra subred o sede, Discovery Utility, Inform URL u option 138; con NAT, reenviar 29810 a 29817 con puerto igual; en la 6, también 29817.
- Por qué importa: sucursales, cámaras en otra VLAN y controladores en la nube dependen de esto.
- Historia: dos controladores detrás de la misma IP pública, uno corrido a 29820 a 29827 (https://support.omadanetworks.com/document/13090/); sucursal por VPN con option 138 servida por un switch (https://support.omadanetworks.com/de/document/124358/).
- Laboratorio: Foco · 15 min. Option 138 en un DHCP y verificar Pending.
- Regla: otra subred, alguien le dice al equipo dónde está el controlador.

## Arco 2. Armar la red del cliente
Por qué este arco: con los equipos adoptados, el trabajo diario es ordenar sitios, crear VLANs, aislar lo que tiene que estar aislado y dejar el WiFi limpio. Termina con una red segmentada y un RF razonable.

### 05 Sitios y clientes
- Fuentes: 2 de 3 (TH19, TH20).
- Idea: un sitio admite un gateway; cada sede con gateway es un sitio. Para varios clientes, MSP en software controller o Cloud Standard, con roles.
- Por qué importa: el orden de sitios define roaming, VPN y quién ve qué.
- Historia: límite de clientes MSP 100 en v5 y 500 en v6 (https://www.tp-link.com/de/support/faq/4276); Essentials no tiene MSP (https://support.omadanetworks.com/en/document/13150/).
- Laboratorio: Admin · 10 min. Crear dos sitios y un rol Viewer.
- Regla: un sitio por sede con gateway, una cuenta por persona.

### 06 VLAN completa
- Fuentes: 3 de 4 (TH21). Evan McCann: la VLAN de gestión es engorrosa.
- Idea: interfaz y DHCP en el gateway, uplink tagueado, puerto de acceso con la VLAN nativa; los perfiles de puerto los crea el controlador al crear la red.
- Por qué importa: es la VLAN de CCTV o de control de acceso que "no da IP".
- Historia: la pregunta oficial de "por qué el cliente pierde red al pasarlo a una VLAN" (https://www.tp-link.com/us/support/faq/4084).
- Laboratorio: Foco · 15 min. VLAN 20 de cámaras en ER y switch JetStream.
- Regla: VLAN que no da IP, revisar las tres patas.

### 07 VLAN no aísla
- Fuentes: 3 de 3 (TH23).
- Idea: si el gateway rutea, las VLAN se ven; para cortar, ACL de switch o gateway, con el permit puntual arriba.
- Por qué importa: CCTV, invitados y control de acceso aislados de la oficina.
- Historia: el switch con IP de gestión alcanzable desde cualquier VLAN (https://forums.lawrencesystems.com/t/tp-link-omada-followup/17893); ACL top down (https://www.omadanetworks.com/eg/support/faq/4122/).
- Laboratorio: Foco · 15 min. VLAN de invitados que solo sale a internet.
- Regla: VLAN separa, ACL aísla; el permit más específico va arriba.

### 08 Menos potencia
- Fuentes: 2 de 3 (TH24), 1 de 3 (TH26).
- Idea: 2,4 GHz en 1, 6, 11 a 20 MHz; 5 GHz a 40 MHz de arranque; potencia baja si los AP están a menos de 12 m; WLAN Optimization corta servicio.
- Por qué importa: la mayoría de quejas de WiFi lento son interferencia propia.
- Historia: bajar de 28 a 25 dBm y probar (https://www.tp-link.com/us/support/faq/2511).
- Laboratorio: Campo · 15 min. Fijar canales y potencia en dos EAP y medir.
- Regla: primero canal y ancho, después potencia, y la optimización automática de madrugada.

## Arco 3. WiFi avanzado, sedes y mantenimiento
Por qué este arco: lo que distingue una instalación que se sostiene: roaming, portal, sedes unidas y un controlador que se puede actualizar o mudar sin perder nada. Termina con el procedimiento de backup y migración.

### 09 Roaming y mesh
- Fuentes: 1 de 1 (TH27, evidencia fina) y 1 de 2 (TH28, evidencia fina).
- Idea: roaming pide SSID idéntico y mismo sitio; 802.11k/v encendido; 802.11r solo si los clientes lo soportan. Mesh: hasta 3 saltos, uplink entre -40 y -62 dBm, para cobertura y no capacidad.
- Por qué importa: tablets de logística, lectores y teléfonos WiFi que se cortan al moverse.
- Historia: el cliente que roamea y se queda sin internet por 802.11r (https://support.omadanetworks.com/en/document/13229/); EAP225-Outdoor, 50 a 60 clientes en toda la red mesh (https://www.omadanetworks.com/cz/support/faq/2283/).
- Laboratorio: Campo · 15 min. Prueba de roaming caminando con ping continuo.
- Regla: mismo SSID, mismo sitio, k y v sí, r con prueba.

### 10 Portal cautivo
- Fuentes: 2 de 3 (TH29).
- Idea: Portal en Site Settings > Authentication > Portal; voucher para hotelería; Pre-Authentication Access; el controlador tiene que estar corriendo y el certificado ayuda.
- Por qué importa: hoteles, salas de espera y locales comerciales.
- Historia: portal que se rehízo a mano al pasar a 4.1.5 (https://www.omadanetworks.com/us/omada-sdn/controller-upgrade/); certificado en un único pfx (https://whitkirkchurch.org.uk/tech-blog/2021/08/installing-an-omada-sdn-controller-on-a-raspberry-pi-using-docker/).
- Laboratorio: Foco · 15 min. Portal con vouchers en un SSID de invitados.
- Regla: portal sin controlador no autentica.

### 11 Túnel entre sedes
- Fuentes: 2 de 3 (TH31). Evan McCann: sitio a sitio sí, VPN de usuarios mejor otro equipo.
- Idea: Auto IPsec con ambos gateways en el mismo controlador, sitios distintos, IP pública y LAN sin solapar; Manual IPsec si hay NAT, con UDP 500 y 4500.
- Por qué importa: CCTV y control de acceso centralizados entre sucursales.
- Historia: sucursal que se adopta por el túnel con option 138 (https://support.omadanetworks.com/de/document/124358/).
- Laboratorio: Foco · 20 min. Auto IPsec entre dos ER en laboratorio.
- Regla: antes del túnel, subredes distintas en cada sede.

### 12 Backup primero
- Fuentes: 4 de 7 (TH32), 2 de 8 (TH36).
- Idea: backup programado fuera del controlador; upgrade de a una versión mayor; downgrade es reinstalar; migración en orden con Forget al final.
- Por qué importa: un controlador muerto sin backup es rehacer toda la obra.
- Historia: saltear la importación deja los equipos sin adoptar (https://www.tp-link.com/us/support/faq/3589); el upgrade del OC tarda 6 a 8 minutos offline (https://tp-link.com/support/faq/3684).
- Laboratorio: Admin · 20 min. Backup programado, export y restore en un controlador nuevo.
- Regla: antes de actualizar, backup. Siempre.

## Divisiones (decisiones, no lecciones)
- Confiar o no en TP-Link para clientes de empresa: Lawrence Systems no lo usaría por historial de seguridad; Evan McCann lo recomienda para negocios con necesidades básicas. Cómo decidir: criticidad del cliente, exigencias de seguridad del contrato y si la gestión queda expuesta a internet.
- Gateway Omada o firewall de terceros: la documentación pone el gateway Omada en el centro; McCann prefiere switches y APs Omada detrás de otro firewall. Cómo decidir: si el cliente necesita VPN de usuarios con RADIUS, routing dinámico o logs de firewall, otro firewall; si no, el ER alcanza y suma VPN de sitio automática.
- Controlador en Docker comunitario, hardware o nube: Docker es gratis y flexible pero sin soporte oficial; OC y Cloud tienen soporte. Cómo decidir: quién mantiene el host a cinco años y si hay presupuesto de licencias.
- Capacidad del OC200: cifra oficial actual recomendada 25 equipos contra 100 que se citaba en 2022. Cómo decidir: dimensionar por la recomendada y prever crecimiento.
- Ritmo de firmware: usuarios ven pocas actualizaciones; TP-Link ofrece canales Beta/RC. Cómo decidir: producción en estable, Beta solo en laboratorio.

## Huecos
- Roaming y mesh se apoyan en una sola fuente oficial cada uno.
- Monitoreo (dashboard, alertas, mail, syslog, Network Check, Packet Capture) solo aparece en la tabla comparativa oficial: se menciona en la lección 12 sin profundizar.
- No se leyó guía de WireGuard ni de VPN de cliente; la lección 11 se limita a sitio a sitio.
- No se leyó guía específica de upgrade de firmware de EAP, switch y gateway en modo controlador.
- Sin fuente de practicante sobre OC300/OC400 ni Omada Central Standard con MSP en producción.

## Entrega
12 lecciones de unos 2 minutos (guion, tarjeta y quiz de 3 preguntas), ficha en class/course.json. El audio lo renderiza el orquestador.
