# Plan de lecciones: UniFi Network, controlador y sitios multi-cliente

Nivel: inicial a intermedio. Versión de referencia: UniFi Network 10.6 y 11.0 (octubre 2026), UniFi OS 5.x/6.x, UniFi OS Server.
Corpus: 30 páginas en raw/ (25 web, 5 notas oficiales de versión de Ubiquiti). Agreement map: 35 temas.
Laboratorio de referencia: una VM con UniFi OS Server (gratis, Ubuntu 24.04, 2 GB RAM) o una consola de laboratorio (UCG, UDM, CloudKey), un switch UniFi administrable y un AP. Rangos de ejemplo: 10.10.10.0/24 para gestión, 192.168.88.0/24 para el sitio remoto, controlador en 10.10.10.5, nombre unifi.example.com.

## Arco 1. Quién manda (lecciones 1 a 4)
Por qué este arco: antes de tocar WiFi o VLANs, el técnico necesita saber dónde vive la configuración y cómo entra cada equipo al controlador, en el local y a distancia. Cierra con un sitio de laboratorio visible en Site Manager.

### Lección 1. Quién manda
- Agree: 3 de 4 (TH01) y 4 de 4 (TH03).
- Idea: cada sitio tiene un controlador (Cloud Gateway, CloudKey o UniFi OS Server) y cada equipo un solo host. Site Manager es la puerta, no el cerebro. Desde Network 11.0 el self-hosted es UniFi OS Server.
- Por qué importa: elegir mal el controlador obliga a migrar después; un UDM no se gestiona desde un servidor central.
- Historia: Network 11.0.97 elimina el Network Server y declara a UniFi OS Server "the official replacement". https://community.ui.com/releases/UniFi-Network-Application-11-0-97/15662d06-8122-44e2-a1ba-af5d71b8a045
- Laboratorio: Admin, 15 min. Instalar UniFi OS Server en una VM Ubuntu 24.04 o abrir una consola de laboratorio y anotar versión de UniFi OS y de Network.
- Regla: antes de vender, decidí quién es el host de cada equipo del sitio y escribilo.

### Lección 2. Adopción limpia
- Agree: 3 de 3 (TH08), 2 de 3 (TH09).
- Idea: un equipo se adopta si está libre de otro controlador, con firmware compatible y en la misma red L2. Para readoptar: borrar del controlador, reset, adoptar.
- Por qué importa: es la primera hora de cada obra.
- Historia: según LazyAdmin el caso más común es desfase de firmware; un lector tenía el firewall de Windows "rebotando" la adopción. https://lazyadmin.nl/home-network/unifi-adoption-failed/
- Laboratorio: Foco, 15 min. Reset de un AP, adopción en L2, SSH con info.
- Regla: equipo que no adopta: reset, misma VLAN que el controlador, firmware, y recién ahí sospechar del controlador.

### Lección 3. Inform remoto
- Agree: 2 de 4 prefieren option 43 o DNS; discrepa Tom Lawrence (set-inform le anda siempre).
- Idea: en L3 el equipo necesita saber la URL de inform. Option 43 o DNS "unifi" sobreviven reinicios; set-inform por SSH es el plan B; Inform Host con Override si el controlador está detrás de NAT.
- Historia: hilo del foro de Lawrence Systems con la respuesta de soporte de Ubiquiti. https://forums.lawrencesystems.com/t/unifi-l3-persistent-inform-url/20405
- Laboratorio: Foco, 20 min. DHCP option 43 en un MikroTik de laboratorio o set-inform por SSH.
- Regla: en sitios remotos, el inform lo entrega el DHCP o el DNS, no la memoria del equipo.

### Lección 4. Muchos sitios
- Agree: 3 de 4 (TH04); TH06 con evidencia fina (1 de 4, cita el artículo oficial); 2 de 4 (TH07).
- Idea: Site Manager junta todos los consolas y servidores; solo necesita salida TCP 443 y 8883, DNS y NTP. Fabrics, roles y Blueprints ordenan muchos clientes.
- Historia: según Ubiquiti citado por UniHosted, un gateway por sitio y un servidor central son "functionally and administratively equivalent". https://www.unihosted.com/blog/unifi-site-management
- Laboratorio: Admin, 10 min. Verificar Remote Management y ver la consola en unifi.ui.com.
- Regla: cada sitio de cliente entra a Site Manager con una cuenta de la empresa, nunca con la personal del técnico.

## Arco 2. Red y WiFi bien hechos (lecciones 5 a 8)
Por qué este arco: lo que se configura en cada obra. Segmentar, dejar los puertos en su lugar y armar un plan de RF que no dependa de la suerte. Cierra con un sitio de laboratorio con tres VLANs y un WiFi medido.

### Lección 5. VLAN por función
- Agree: 4 de 5 (TH15); discrepa The Hook Up (cámaras en la VLAN principal por carga del router).
- Idea: una red por función (staff, invitados, CCTV), cada una con su DHCP; en 2026 la separación se hace con zonas.
- Historia: Network 11.0 migra automáticamente todos los sitios a Zone-Based Firewall. https://community.ui.com/releases/UniFi-Network-Application-11-0-97/15662d06-8122-44e2-a1ba-af5d71b8a045
- Laboratorio: Foco, 15 min. Crear tres redes y mirar la Zone Matrix.
- Regla: cada VLAN nueva sale con nombre, DHCP propio y zona elegida.

### Lección 6. Puertos con perfil
- Agree: 3 de 4 (TH17), 2 de 4 (TH18).
- Idea: puerto de equipo final con VLAN nativa de su red y etiquetadas bloqueadas; uplinks y AP con todas.
- Historia: arrancar una cámara de la pared y enchufar una laptop, de The Hook Up. https://www.thesmarthomehookup.com/test_install/unifi-network-update-part-2-vlans-wifi-partitioning-and-advanced-features/
- Laboratorio: Foco, 10 min. Port Manager: puerto de cámara con Native VLAN CCTV y Block All.
- Regla: puerto que da a la calle, VLAN nativa sola y nada etiquetado.

### Lección 7. Canales angostos
- Agree: 4 de 5 (TH19, TH20); divisiones en DFS y en Auto contra manual.
- Idea: 2.4 GHz en 20 MHz con 1, 6 y 11; en 5 GHz, más denso, más angosto; medir antes; Channel AI con dos o más AP.
- Historia: oficina de unos 300 equipos y 10 AP que bajó a 20 MHz y pasó al canal DFS 64. https://std.rocks/improve-wifi-performance-guide.html
- Laboratorio: Foco, 20 min. Escaneo de entorno y Channel AI.
- Regla: el ancho de canal se elige por la cantidad de clientes, no por el número de la caja.

### Lección 8. Potencia baja
- Agree: 5 de 5 (TH24).
- Idea: potencia al máximo genera clientes pegajosos y lentos; con varios AP, 2.4 baja, 5 media.
- Historia: LazyAdmin la llama probablemente la causa número uno de problemas de WiFi. https://lazyadmin.nl/home-network/optimize-your-unifi-network/
- Laboratorio: Campo, 20 min. Bajar potencia y caminar con WiFiman midiendo.
- Regla: más AP con menos potencia antes que pocos AP a todo volumen.

## Arco 3. Sin sorpresas (lecciones 9 a 12)
Por qué este arco: lo que separa una instalación que anda de una que se sostiene en el tiempo. Roaming con cabeza, invitados de verdad aislados, actualizaciones que no rompen nada y un método para diagnosticar. Cierra con un procedimiento de soporte repetible.

### Lección 9. Roaming sin magia
- Agree: 4 de 6 (BSS Transition); Fast Roaming dividido (WunderTech a favor, LazyAdmin en contra, Purple condicionado).
- Idea: el roaming lo decide el cliente; BSS Transition siempre, Fast Roaming solo con equipos probados, mínimo RSSI al final; equipos viejos en SSID aparte.
- Historia: caso ilustrativo de Purple, lectores viejos sin conexión en 9 locales tras activar Fast Roaming en todos los SSID. https://www.purple.ai/en-us/guides/unifi-802-11k-802-11r-fast-roaming
- Laboratorio: Campo, 15 min. Activar Fast Roaming en un SSID de prueba y ver el historial de roaming.
- Regla: ninguna función de roaming se activa en producción sin probar cada tipo de equipo del cliente.

### Lección 10. Invitados aislados
- Agree: 3 de 4 (TH30, TH31).
- Idea: red en zona Hotspot, WiFi Standard o Hotspot según haga falta portal, revisar landing page y probar el aislamiento desde un celular.
- Historia: la landing page viene activada por defecto en la zona Hotspot. https://www.wundertech.net/how-to-set-up-a-guest-network-vlan-in-unifi/
- Laboratorio: Foco, 20 min. Red de invitados con vouchers y prueba desde el celular.
- Regla: no se entrega una red de invitados sin probar desde un celular que no llega a nada interno.

### Lección 11. Backup y etapas
- Agree: 3 de 3 (TH13), 4 de 5 (TH32).
- Idea: backup antes de cada cambio grande, dos copias afuera; actualizar Official, esperar, probar en un sitio, después el resto; leer notas de versión.
- Historia: HostiFi espera 2 a 3 semanas y saltó la 7.5.174. https://www.hostifi.com/support/hostifi-how-we-handle-unifi-updates
- Laboratorio: Admin, 15 min. Bajar backup, restaurar en la VM de laboratorio, leer la nota de versión.
- Regla: antes de actualizar, backup. Siempre.

### Lección 12. Mirar primero
- Agree: 4 de 4 (TH34), 4 de 5 (TH35).
- Idea: ante una queja, primero historial del cliente y Time Machine, después un cambio por vez; si se rompió, volver a lo último que se tocó.
- Historia: caso ilustrativo de Purple, hotel con 6 desconexiones en 10 minutos que pasó a cero roams limpios. https://www.purple.ai/en-us/guides/unifi-802-11k-802-11r-fast-roaming
- Laboratorio: Rápido, 10 min. Leer el historial de un cliente y Time Machine de una radio.
- Regla: primero el historial, después la teoría, y un cambio por vez.

## Divisiones
- Fast Roaming (802.11r). A favor: WunderTech, que cita a Ubiquiti. En contra: LazyAdmin. Condicionado: Purple, solo SSID Enterprise de voz. Cómo decidir: inventario de equipos del cliente y prueba con cada tipo; si alguno falla, SSID aparte sin Fast Roaming.
- Canales Auto o manuales. Auto con Channel AI: WunderTech, LazyAdmin. Manual tras escanear: HostiFi, std.rocks. Cómo decidir: con dos o más AP y un entorno cambiante, Auto con Channel AI y revisar con Time Machine; en sitios con un vecino fijo y fuerte, manual.
- DFS. Evitar: LazyAdmin. Usar: std.rocks. Cómo decidir: si los canales 36 a 48 están saturados y no hay eventos de radar en el registro, DFS; si aparecen cambios de canal por radar, volver a los bajos.
- Mínimo RSSI. A favor como regla: std.rocks con -70 dBm. Solo en alta densidad: WunderTech citando a Ubiquiti. Último paso y suave: Purple. Cómo decidir: solo con solape de cobertura comprobado caminando.
- Adopción L3. Option 43: soporte de Ubiquiti. set-inform: Tom Lawrence y la guía de Sikich. Cómo decidir: si el DHCP del sitio es tuyo, option 43 o DNS; si no, set-inform e Inform Host, y control después de cada actualización.
- Ancho en 5 GHz. 80 MHz para casas (Ubiquiti citado por WunderTech), 40 MHz para oficinas (HostiFi, LazyAdmin), 20 MHz para alta densidad (std.rocks). Cómo decidir: por clientes por AP y por vecinos en el escaneo.

## Huecos
- La documentación de help.ui.com respondió HTTP 403 al scraper; lo oficial entra por las notas de versión (feed RSS de community.ui.com) y por citas de practicantes. Conviene que el técnico lea help.ui.com en el navegador como complemento.
- Alarm Manager y roles de administrador en Site Manager tienen poca profundidad en el corpus.
- Crosstalk Solutions quedó afuera: el presupuesto de búsqueda se agotó antes de encontrar una página suya recuperable.
- El menú de UniFi cambia con casi cada versión; las rutas del laboratorio son de Network 10.6 y 11.0 y pueden moverse.

## Entrega
12 carpetas class/NN-handle con script.txt, card.md y quiz.json; course.json con la ficha. Audio lo renderiza el orquestador.
