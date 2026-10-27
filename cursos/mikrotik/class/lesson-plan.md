# Plan: MikroTik RouterOS para integradores

Nivel inicial a intermedio. RouterOS 7 (la documentación leída es la de la versión 7.25, octubre 2026). 24 lecciones de unos 2 minutos: 3 arcos de 4 (lecciones 1 a 12), una ampliación de 3 partes (lecciones 13 a 22) y la lección 23 (Safe Mode), que se presenta en el arco 1 después de la lección 1, y la lección 24 (Port forwarding), que se presenta en el arco 3 después de la lección 10. Fuentes: 55 páginas en raw/web (19 de MikroTik más 3 sumadas para la lección 23, 3 del foro oficial más 4 de la lección 23, 2 guías de practicantes sobre Safe Mode, 3 de Antel, 3 de foros y soporte uruguayos, 1 de Microsoft, 17 de practicantes y prensa de seguridad). Mapa de acuerdos: research/agreement-map.md (TH01 a TH35 del curso original, TH36 a TH63 de la ampliación, TH64 a TH66 de la lección 23, TH67 a TH70 de la lección 24; las páginas de la lección 24 están en research/notes/e.md).

Criterio de orden: primero lo que evita quedar afuera del equipo o dejarlo expuesto (alto acuerdo, se practica en 10 minutos), después lo que se hace todas las semanas en obra y soporte, y al final lo que tiene más variantes y discusión entre fuentes.

## Arco 1. Entrar y blindar (lecciones 1 a 4)
Por qué este arco: un MikroTik recién sacado de la caja se puede dejar abierto o se puede perder el acceso en cinco minutos; estas cuatro lecciones dejan un equipo al que entrás vos y nadie más.

### 1. Entrar sin romper
- 3 de 3 fuentes coinciden (TH01); para la defconf, 3 de 4 (TH02), la guía de VLAN del foro arranca de cero.
- Idea: entrar por WinBox con la MAC desde un puerto LAN (ether1 es WAN por defecto) y hacer cada cambio riesgoso en Safe Mode. La configuración por defecto se conserva salvo que vayas a reconstruir todo a conciencia; los CCR vienen sin ella.
- Por qué importa: el primer error típico es cortarse el acceso a uno mismo en un sitio remoto.
- Historia: Safe Mode deshace todo si la sesión se corta, pero si pasás de 100 cambios sale solo y no deshace nada (https://help.mikrotik.com/docs/spaces/ROS/pages/328155/Configuration+Management).
- Laboratorio: Rápido, 10 min. Conectarse por MAC, mirar firewall y listas por defecto, export inicial, probar Safe Mode con Ctrl+X y Ctrl+D.
- Regla: cambio que puede cortarme, en Safe Mode y en pasos chicos.

### 23. Safe Mode
- Ubicación: se escribió como lección 23 (octubre 2026); en la presentación final va en este arco, justo después de la lección 1, que solo lo presenta al pasar.
- 5 de 6 fuentes coinciden en cómo se entra, se confirma y se deshace (TH64); 3 de 4 en el tope de 100 acciones y los pasos chicos (TH65); lo que no cubre tiene poco acuerdo (TH66).
- Idea: Safe Mode marca un punto de vuelta y deshace todo lo marcado con F en /system/history si la sesión dueña termina mal. Botón en WinBox y WebFig, Ctrl+X o F4 en la CLI; Ctrl+X otra vez o soltar el botón confirma, Ctrl+D descarta, /quit confirma. Tope de 100 acciones; otro usuario puede tomar el modo con u, r o d. Usarlo en firewall, bridge y VLAN, IP de gestión y ruta por defecto, y siempre en remoto, con export antes.
- Por qué importa: es la diferencia entre un error en remoto y un viaje al sitio.
- Historia: con Safe Mode en WebFig, un drop en input te bloquea y al minuto reconecta sin la regla (https://forum.mikrotik.com/t/safe-mode-in-webfig/92508); quitar una IP en Safe Mode y cortar la energía dejó el cambio aplicado en 6.40.4 (https://forum.mikrotik.com/t/safe-mode-powercycle-useless/105625). Mecánica, timeout y toma por otro usuario (https://manual.mikrotik.com/docs/7.25/getting-started/configuration-management/).
- Laboratorio: Foco, 15 min. Export, Safe Mode, deshabilitar a propósito el puerto por donde se entra, esperar la reversión, cambio bueno confirmado con Ctrl+X, salida con Ctrl+D que descarta.
- Regla: antes de un cambio que me puede cortar: export, Safe Mode, un cambio, verifico y confirmo.

### 2. Usuarios propios
- 3 de 3 fuentes coinciden (TH04), sin discrepancias.
- Idea: un usuario por técnico con contraseña larga, probarlo, y recién ahí deshabilitar admin. Grupos propios con las políticas justas y, si se puede, limitados por dirección de origen.
- Por qué importa: con usuarios nominales sabés quién cambió qué, y das de baja a alguien sin cambiarle la clave a todos.
- Historia: según la documentación, el grupo read de fábrica puede reiniciar el router y ver configuración sensible; y un signo pesos sin escapar acorta la contraseña sin avisar (https://manual.mikrotik.com/docs/7.25/getting-started/securing-your-router).
- Laboratorio: Admin, 10 min. Crear usuario full, probarlo, deshabilitar admin, crear grupo de monitoreo sin reboot ni write y probar que no puede reiniciar.
- Regla: nadie entra como admin; cada técnico, su usuario.

### 3. Cerrar puertas
- 7 de 7 fuentes coinciden en no exponer gestión a internet (TH05); la propia guía de MikroTik documenta cómo abrirla cuando es inevitable, filtrada por origen.
- Idea: WinBox, SSH y API nunca hacia internet; apagar telnet, ftp, www y api; MAC server y descubrimiento solo hacia LAN. Actualizar no alcanza si la contraseña ya se filtró: cambiarla y auditar scheduler, SOCKS y reglas raras.
- Por qué importa: los routers expuestos se escanean y se comprometen solos, sin que nadie los elija.
- Historia: el honeypot de Gen Digital con versión vieja y contraseña fuerte cayó a los 15 minutos por la falla de WinBox (https://www.gendigital.com/blog/insights/research/meris-and-trickbot-standing-on-the-shoulders-of-giants); MikroTik sobre Mēris: si te robaron la contraseña en 2018, actualizar solo no ayuda (https://mikrotik.com/supportsec/meris-botnet).
- Laboratorio: Foco, 15 min. Auditar servicios, restringir available-from, MAC server a LAN, revisar scheduler, SOCKS, proxy y clientes L2TP.
- Regla: la gestión no mira a internet; si hace falta entrar de afuera, VPN.

### 4. Input y forward
- 3 de 4 fuentes coinciden (TH14, TH15); el foro discute dos escuelas de firewall (TH18).
- Idea: input es lo que va al router, forward lo que pasa por él. Las reglas se leen de arriba abajo y la primera que coincide manda: lo que permitís va arriba del drop. Address-lists e interface lists para que las reglas no dependan de IPs ni nombres de puertos.
- Por qué importa: la mitad de los "no anda" de soporte es una regla bien escrita en el lugar equivocado.
- Historia: la documentación avisa que en un router con defconf, un add pone tu regla debajo del drop y nunca coincide; hay que usar place-before (https://manual.mikrotik.com/docs/7.25/getting-started/securing-your-router).
- Laboratorio: Foco, 15 min. Address-list admins, regla que limita WinBox a esa lista ubicada con place-before, mirar contadores.
- Regla: antes de agregar una regla, sé en qué cadena va y qué tiene arriba.

## Arco 2. Operación diaria (lecciones 5 a 8)
Por qué este arco: es lo que un integrador hace todas las semanas: separar sistemas en VLANs, guardar la configuración, actualizar y entrar a distancia.

### 5. VLAN por sistema
- 2 de 3 fuentes coinciden (TH19, TH20, TH21), sin discrepancias de fondo.
- Idea: cámaras, control de acceso y datos en VLANs separadas con bridge vlan-filtering. Access sin etiqueta, trunk solo etiquetado, ingress-filtering en todos, gestión por una VLAN propia, y vlan-filtering se activa al final.
- Por qué importa: si un equipo de CCTV se infecta o satura, no se lleva puesta la red de la oficina.
- Historia: poner varias VLAN en una entrada con puertos access deja pasar las dos VLAN por ambos puertos; y con PVID 1 en trunk y bridge queda una puerta sin etiqueta al router (https://manual.mikrotik.com/docs/7.25/bridging-and-switching/user-guides/bridge-vlan-table). La guía del foro propone una VLAN por área para poder cortar un piso solo (https://forum.mikrotik.com/t/using-routeros-to-vlan-your-network/126489).
- Laboratorio: Foco, 20 min. Puerto de rescate fuera del bridge, VLAN 20 de CCTV, tabla VLAN, frame-types, activar filtering y verificar con Torch.
- Regla: vlan-filtering es lo último que se toca, con un camino de rescate abierto.

### 6. Backup primero
- 3 de 3 fuentes coinciden (TH29).
- Idea: export en texto para leer, comparar y migrar; backup binario para restaurar el mismo equipo. El export no lleva contraseñas de usuarios; con show-sensitive lleva claves y pasa a ser un archivo sensible.
- Por qué importa: con un export antes y otro después, cualquier "quién tocó esto" se contesta con un diff.
- Historia: un practicante versiona sus exports en git y solo hace commit cuando cambia algo; así quedó registrado un cambio de credenciales PPPoE del ISP (https://xtremeownage.com/blog/2025/mikrotik-backup-script/).
- Laboratorio: Admin, 10 min. Export, export show-sensitive, backup con contraseña, bajar archivos y comparar dos exports.
- Regla: antes de tocar, export; después de tocar, export.

### 7. Actualizar en orden
- 4 de 6 fuentes coinciden (TH30); sobre stable o long-term no hay ganador.
- Idea: canal stable o long-term, nunca testing en producción. Backup antes, RouterOS primero, RouterBOOT después con reinicio. Desde v6 se pasa por una versión intermedia.
- Por qué importa: la mayoría de los MikroTik comprometidos tenían parche disponible hace años.
- Historia: Eclypsium contó más de 2 millones de MikroTik con gestión expuesta y estimó unos 300.000 vulnerables (https://www.csoonline.com/article/3644469/researchers-warn-about-continuous-abuse-of-unpatched-mikrotik-routers.html).
- Laboratorio: Admin, 15 min. Ver canal, actualizar, comparar current-firmware y upgrade-firmware, actualizar RouterBOOT.
- Regla: RouterOS y RouterBOOT se actualizan juntos, con backup antes.

### 8. Túnel de gestión
- 4 de 7 fuentes coinciden en VPN con WireGuard primero (TH25); una guía defiende L2TP/IPsec por el cliente nativo y el aviso de Mēris nombra IPsec.
- Idea: WireGuard con un peer por técnico, allowed-address /32 y solo el puerto UDP del túnel abierto en input. L2TP/IPsec queda para cuando del otro lado no se puede instalar nada; PPTP nunca.
- Por qué importa: entrás a cualquier cliente sin dejar WinBox mirando a internet.
- Historia: la documentación avisa que el firewall por defecto bloquea el túnel hasta que se acepta su puerto en input (https://help.mikrotik.com/docs/spaces/ROS/pages/69664792/WireGuard).
- Laboratorio: Foco, 20 min. Interfaz wg-gestion, peer de la notebook, reglas de input, cliente con allowed IPs acotadas, probar WinBox por el túnel.
- Regla: a un cliente se entra por túnel, nunca por un puerto abierto.

## Arco 3. Avanzado y diagnóstico (lecciones 9 a 12)
Por qué este arco: casos donde las fuentes dan más de un camino; cada lección deja un criterio para decidir en el sitio.

### 9. Nombre, no puerta
- 2 de 3 fuentes coinciden (TH28); usuarios del foro publican cámaras por puerto detrás del nombre de IP Cloud como algo normal.
- Idea: DDNS de IP Cloud da un nombre que sigue la IP pública; no abre nada. Comparar public-address con la IP del WAN dice si hay NAT doble o CGNAT, y con CGNAT no hay port forwarding posible.
- Por qué importa: te ahorra una tarde peleando con un port forwarding que nunca va a andar.
- Historia: la documentación lo dice literal: el nombre solo hace más fácil encontrar el router y no abre ningún acceso (https://manual.mikrotik.com/docs/7.25/network-management/cloud/); detrás de CGNAT no se puede publicar nada (https://manual.mikrotik.com/docs/7.25/firewall-and-quality-of-service/firewall/nat).
- Laboratorio: Rápido, 10 min. Activar DDNS, leer public-address, comparar con el WAN, decidir el camino.
- Regla: antes de prometer acceso remoto, comparo public-address con la IP del WAN.

### 10. NVR con criterio
- 4 de 6 fuentes coinciden (TH34); el ejemplo oficial de primera configuración publica un puerto sin filtrar el origen.
- Idea: la primera opción es VPN. Si igual hay que publicar un NVR: solo el puerto que usa la app, entrada por la lista WAN, origen limitado con address-list, nunca un puerto del router. Hairpin solo si desde adentro se entra por la IP pública.
- Por qué importa: un NVR publicado a todo internet es el próximo equipo en aparecer en un escaneo.
- Historia: en el foro una cámara andaba desde afuera y no desde adentro porque el dst-nat tenía in-interface del PPPoE (https://forum.mikrotik.com/t/solved-hairpin-nat-not-working/97689); la documentación llama "más seguro" a sumar src-address al dst-nat (https://manual.mikrotik.com/docs/7.25/firewall-and-quality-of-service/firewall/nat).
- Laboratorio: Campo, 15 min. Address-list de la central, dst-nat filtrado, limpiar conexiones, probar desde 4G con y sin permiso.
- Regla: si publico algo, publico un puerto, para una lista de orígenes, con fecha de revisión.

### 24. Port forwarding
- Ubicación: se escribió como lección 24 (octubre 2026); en la presentación final va en este arco, justo después de la lección 10, que deja el criterio de si publicar o no. Esta es la práctica concreta del dst-nat.
- 5 de 6 fuentes coinciden en atar el dst-nat a la WAN o a la IP pública y filtrar el origen (TH67); 4 de 4 en que el firewall por defecto ya deja pasar lo dst-nateado (TH68); 6 de 7 en los puertos de fábrica de Hikvision y Dahua, con diferencias en cuántos alcanzan (TH69); hairpin con masquerade o DNS local (TH70).
- Idea: `chain=dstnat action=dst-nat` con `to-addresses` y `to-ports` (afuera 18000, adentro 8000), `in-interface-list=WAN` o la IP pública, `src-address-list`; la regla `drop all from WAN not DSTNATed` ya lo permite en forward y con firewall estricto alcanza un accept con `connection-nat-state=dstnat`. Puertos: Hikvision 8000, 554 o 10554, 80 y 443; Dahua 37777 TCP, 37778 UDP, 554, 80 y 443. Varios NVR con puertos externos distintos. Hairpin con dst-nat para la LAN y masquerade, o DNS local si el puerto es el mismo. WAN privada es doble NAT; WAN en 100.64.0.0/10, CGNAT sin forwarding. Probar desde afuera y mirar contadores.
- Por qué importa: es el pedido más frecuente en CCTV y el que más tardes se pierde cuando no se sabe si el paquete llega al router.
- Historia: una regla con solo dst-port=80 dejó a toda la LAN sin navegar (https://forum.mikrotik.com/t/noob-sorry-nat-port-80-breaking-outbound-web/41994); un NVR Dahua hacía login desde internet pero no mostraba video hasta publicar los puertos de datos (https://forum.mikrotik.com/t/need-help-with-port-forwarding/159605); Modat contó 973.819 servicios RTSP expuestos en marzo de 2026, el 43,9 % fuera del 554 (https://www.modat.io/post/exposed-rtsp). Puertos: https://learncctv.com/default-ports-for-hikvision-dvr, https://netviewcctv.co.uk/blog/post/ports, https://www.dahuasecurity.com/about-dahua/news-events/notice/how-to-setup-remote-access-for-nvr.
- Laboratorio: Campo, 20 min. Chequeo de WAN, address-list, dst-nat 18000 a 8000 y 18554 a 554, forward, limpiar conexiones, pruebas desde la oficina, VLC y celular, contadores, hairpin y DNS local.
- Regla: un puerto por servicio, entrando por la WAN, para una lista de orígenes; lo pruebo desde afuera y miro el contador.

### 11. Dos WAN
- 2 de 3 fuentes coinciden en rutas recursivas (TH23); un practicante las considera lentas y suma Netwatch.
- Idea: rutas /32 a hosts testigo por cada ISP, y defaults recursivas con check-gateway=ping y distancias 1 y 2; así se detecta la caída aguas arriba del módem. Las dos salidas en la lista WAN para el masquerade.
- Por qué importa: el módem prendido con internet caída es el caso más común, y un failover que solo mira el módem no lo ve.
- Historia: según MKController, check-gateway tarda de 20 a 30 segundos en conmutar y no ve pérdidas parciales (https://mkcontroller.com/blog/tutorials/mikrotik/mikrotik-dual-wan-failover-isp-guide/); la documentación suma un segundo testigo por enlace (https://help.mikrotik.com/docs/spaces/ROS/pages/26476608/Failover+WAN+Backup).
- Laboratorio: Foco, 20 min. Rutas testigo, defaults recursivas, segunda WAN en la lista, ping continuo y cortar el ISP1 aguas arriba.
- Regla: un failover que no probé desenchufando no existe.

### 12. Torch y sniffer
- 2 de 6 fuentes de troubleshooting coinciden en el uso combinado (TH31, TH32), sin discrepancias.
- Idea: ping y traceroute preguntan, Torch mira lo que pasa por una interfaz en vivo, el sniffer guarda paquetes para Wireshark, y el log con log=yes en una regla dice qué se descarta. Torch en la interfaz LAN, no en la WAN.
- Por qué importa: pasás de "no anda" a "el paquete llega y nadie contesta" en cinco minutos.
- Historia: un portal cautivo mostraba página en blanco; con una captura aparecieron unos 20 dominios que había que permitir y que el proveedor no documentaba (https://admiralplatform.com/tips4tiks-packet-capture-with-mikrotik/). Torch sube la CPU porque apaga FastTrack mientras corre (https://manual.mikrotik.com/docs/7.25/diagnostics-monitoring-and-troubleshooting/torch).
- Laboratorio: Campo, 15 min. Ping y traceroute, Torch filtrado por una cámara, captura a .pcap, log temporal en un drop.
- Regla: no adivino; miro con Torch, y si no alcanza, capturo.

## Arco 4. Conexión a internet (lecciones 13 a 15)
Por qué este arco: antes de VLANs, firewall o VPN, el router tiene que salir a internet; estas tres lecciones cubren las tres formas que aparecen en obra en Uruguay, de la más simple a la que más consultas genera.

### 13. IP fija
- 3 de 5 fuentes coinciden (TH36); la documentación de NAT agrega el matiz masquerade o src-nat (TH37). Sin discrepancias.
- Idea: dirección, ruta por defecto y DNS a mano; antes, deshabilitar el cliente DHCP de la defconf en ether1; verificar por capas (gateway, IP de internet, nombre).
- Por qué importa: es la WAN que se configura en cinco minutos y se rompe en uno si un dato está mal escrito; con gateway fijo el sitio queda listo para rutas recursivas.
- Historia: Antel Internet corporativo entrega hasta 29 IPs fijas en un /27 sobre RJ45, con un router que instala y administra Antel (https://antel.com.uy/empresas/internet-y-fija/planes/internet-corporativo); Internet pyme trae 1 IP fija (https://antel.com.uy/empresas/internet-y-fija/planes/internet-pyme).
- Laboratorio: Rápido, 15 min. Deshabilitar DHCP cliente, cargar IP de ejemplo 203.0.113.10/29, ruta y DNS, tres pruebas, comparar con public-address.
- Regla: IP fija: dirección, ruta y DNS a mano, y tres pings antes de irme.

### 14. Cliente DHCP
- 2 de 3 fuentes coinciden (TH39, TH40); un practicante con producto propio advierte el límite de las recursivas con gateway dinámico (TH38).
- Idea: leer lo que instala el cliente (dirección, ruta, DNS, NTP, estado bound); default-route-distance para principal y respaldo; detectar doble NAT comparando con public-address.
- Por qué importa: el DHCP "anda solo" y por eso nadie mira el doble NAT ni las dos rutas en distancia 1 que reparten tráfico sin querer.
- Historia: con la opción 121 el gateway de la opción 3 se ignora y la ruta por defecto puede faltar; el script de lease de la documentación mantiene una ruta al día cuando cambia el gateway (https://manual.mikrotik.com/docs/7.25/network-management/dhcp/client/).
- Laboratorio: Foco, 15 min. print detail, distancia 2, renew, comparar con public-address.
- Regla: lo que instala el DHCP, lo leo antes de irme.

### 15. PPPoE con Antel
- 3 de 8 fuentes coinciden en que el ONT de Antel se pasa a puente a pedido y el router propio marca PPPoE (TH45); 2 de 8 detallan MTU y MSS (TH42); en contra, usuarios uruguayos con cortes en 2017 que volvieron a modo router.
- Idea: ONT en puente pedido a Antel; cliente PPPoE con las credenciales del servicio, add-default-route y use-peer-dns; la WAN pasa a ser la interfaz PPPoE; MTU y MRU 1492 y MSS. VLAN: no confirmada por ninguna fuente, se prueba sin VLAN con el escáner y se confirma con Antel.
- Por qué importa: es la consulta más frecuente de los clientes de fibra y donde más se pierde tiempo por datos sin confirmar.
- Historia: "en fibra lo hacen ellos": el cambio de modo lo hace el proveedor de forma remota (https://www.macacos.com.uy/foros/viewtopic.php?id=17622); Antel ofrece modo puente o router WiFi por MiAntel o el 121 (https://antel.com.uy/personas/preguntas-frecuentes/internet); PPPoE limita MTU y MRU a 1492 (https://manual.mikrotik.com/docs/7.25/virtual-private-networks/pppoe/).
- Laboratorio: Campo, 20 min. Scan, cliente PPPoE, lista WAN, monitor, MSS, reconectar y ver si cambia la IP.
- Regla: con Antel, confirmo modo puente y VLAN antes de ir, y anoto lo que me dijeron y quién.

## Arco 5. Software al día (lecciones 16 y 17)
Por qué este arco: la lección 7 dejó el orden; estas dos dan las herramientas para actualizar sitios sin internet, deshacer una versión y elegir con criterio qué versión vive en cada cliente.

### 16. Paquetes al día
- 2 de 3 fuentes coinciden (TH47, TH48, TH49), sin discrepancias.
- Idea: Check for Updates, Download o Download&Install; paquetes extra que se habilitan y se aplican con reinicio; .npk de la arquitectura correcta en la raíz de Files cuando no hay internet; downgrade con los .npk viejos; RouterBOOT al final.
- Por qué importa: las redes de cámaras aisladas no tienen salida a internet, y una versión que rompe algo se deshace en minutos si sabés cómo.
- Historia: desde 7.13 los drivers de radio son paquetes aparte y wireless y wifi-qcom no pueden estar activos a la vez (https://manual.mikrotik.com/docs/7.25/getting-started/installation-and-upgrade/packages/); el paquete subido dentro de una carpeta no se instala (https://help.mikrotik.com/docs/spaces/ROS/pages/328142/Upgrading+and+installation).
- Laboratorio: Admin, 20 min. Backup, arquitectura, habilitar y desinstalar un extra, .npk a mano, downgrade, RouterBOOT.
- Regla: changelog, backup, paquetes de la misma arquitectura y versión, y RouterBOOT al final.

### 17. Elegir el canal
- 2 de 3 fuentes coinciden (TH50); la documentación describe sin elegir y ofrece actualización automática por script.
- Idea: long-term en sitios de clientes, stable solo para una función nueva probada en el banco, testing y development nunca en producción; el cambio de canal también sirve para bajar.
- Por qué importa: el canal decide cuántas sorpresas trae cada actualización en un sitio que se visita poco.
- Historia: un distribuidor recuerda que una versión candidata puede dejar el equipo recuperable solo por Netinstall (https://blog.linitx.com/mikrotik-routeros-package-channel-bugfix-only-current-release-candidate-legacy/).
- Laboratorio: Admin, 10 min. Comparar installed-version y latest-version en long-term y stable, elegir y anotar.
- Regla: long-term en clientes; lo nuevo, primero en mi banco.

## Arco 6. Acceso remoto y VPN (lecciones 18 a 22)
Por qué este arco: la lección 8 dejó WireGuard como primera opción; estas cinco cubren lo que aparece cuando el sitio no tiene IP pública, cuando del otro lado solo hay un cliente nativo y cuando el otro extremo es un firewall de otra marca.

### 18. Cloud a fondo
- 2 de 5 fuentes coinciden (TH46, TH41); en el foro, un veterano pide apagar detect-internet y otro usuario lo usa para registrar caídas.
- Idea: DDNS con TTL de 60 s y actualización por minuto detrás de NAT, force-update, public-address de la WAN por donde sale la ruta a la nube, hora por NTP y no por la nube; el nombre no es un camino.
- Por qué importa: con PPPoE la IP cambia, y con dos WAN el nombre puede seguir al enlace de respaldo.
- Historia: la documentación dice que la hora de la nube es aproximada y que con NTP activo no se usa (https://manual.mikrotik.com/docs/7.25/network-management/cloud/); el debate sobre detect-internet (https://forum.mikrotik.com/t/trying-to-understand-defconf-firewall/267442).
- Laboratorio: Rápido, 15 min. DDNS, force-update, resolver el nombre, NTP, revisar detect-internet.
- Regla: el nombre sigue a la IP, el NTP pone la hora, y para entrar uso un túnel.

### 19. Back To Home
- 2 de 3 fuentes coinciden (TH51, TH52, TH53), sin discrepancias.
- Idea: WireGuard gestionado por la nube de MikroTik, directo o por relay; solo ARM, ARM64 o TILE con 7.12 o más; un usuario por dispositivo, allow-lan solo a quien lo necesita, expires para accesos temporales.
- Por qué importa: es el acceso remoto más rápido para un sitio con CGNAT si el equipo lo soporta.
- Historia: los RouterBOARD MIPS quedan afuera (https://www.wirelessnetware.ca/blog/back-to-home-with-mikrotik/); revocar borra todos los usuarios y claves (https://manual.mikrotik.com/docs/7.25/network-management/cloud/back-to-home/).
- Laboratorio: Foco, 20 min. Activar, usuario con LAN y vencimiento, QR en el celular por datos móviles, usuario de solo internet, lista LAN.
- Regla: un usuario por equipo, la LAN solo a quien la necesita, y nunca revoco para dar una baja.

### 20. Concentrador CHR
- 2 de 5 fuentes describen el patrón del concentrador (TH54); la documentación de licencias (TH55) y la guía de Hetzner (TH56) completan; MKController ofrece su nube como alternativa (sesgo comercial).
- Interpretación: el pedido "manejo de VPS" se interpreta como MikroTik CHR en un VPS como concentrador de VPN para sitios detrás de CGNAT o sin IP pública; la tarjeta lo dice.
- Idea: instalar con dd desde el modo rescate, endurecer el día uno, elegir licencia según tráfico (Free 1 Mbps, P1, P10, P-Unlimited, prueba de 60 días), un peer WireGuard por sitio que llama al hub con keepalive.
- Por qué importa: es el camino para sitios con CGNAT y equipos sin Back To Home, y el hub es el equipo más expuesto de la empresa.
- Historia: el CHR arranca con admin sin contraseña en una IP pública (https://community.hetzner.com/tutorials/mikrotik-chr-basic-setup); las copias no reinician la prueba y IP Cloud pide licencia paga (https://manual.mikrotik.com/docs/7.25/getting-started/routeros-licensing/chr/chr-licensing/).
- Laboratorio: Foco, 20 min. Endurecer, firewall de input, licencia, hub WireGuard, sitio de laboratorio detrás de NAT.
- Regla: el hub se endurece el día uno y se licencia según lo que transporta.

### 21. L2TP con IPsec
- 2 de 3 fuentes coinciden (TH57); Microsoft documenta la clave de NAT-T (TH58); la documentación de IPsec aconseja evitar la clave compartida (TH62).
- Idea: servidor con use-ipsec=required, pool, perfil y un secret por persona; input UDP 500, 4500, 1701 y ESP; IPsec fuera de FastTrack; la clave de registro de Windows cuando hay NAT.
- Por qué importa: es la única opción cuando el equipo del otro lado no admite instalar nada.
- Historia: Android conecta y Windows no: AssumeUDPEncapsulationContextOnSendRule en 2 (https://learn.microsoft.com/en-us/troubleshoot/windows-server/networking/configure-l2tp-ipsec-server-behind-nat-t-device).
- Laboratorio: Foco, 20 min. Servidor, usuario, reglas, bypass, cliente nativo de Windows, diagnóstico.
- Regla: L2TP siempre con IPsec obligatorio, un usuario por persona y cuatro puertos claros en input.

### 22. IPsec entre marcas
- 3 de 6 fuentes coinciden en acordar parámetros y diagnosticar por capas (TH59, TH61); 4 de 6 en el bypass de NAT y FastTrack (TH60). Discrepan en PSK o certificados y en NAT-T.
- Idea: profile, peer, identity, proposal y policy con una tabla acordada; active-peers, ph2-state, installed-sa y log ipsec; bypass de NAT y FastTrack; NTP y subredes distintas antes de empezar.
- Por qué importa: es el túnel que más visitas cuesta cuando se arma sin tabla con el técnico de la otra marca.
- Historia: el túnel lento que "se arregla" al prender Torch es FastTrack (https://manual.mikrotik.com/docs/7.25/virtual-private-networks/ipsec/); en MikroTik la fase 1 está en Active Peers y la fase 2 en Policies (https://getlabsdone.com/setup-ipsec-site-to-site-vpn-tunnel-between-pfsense-and-mikrotik/).
- Laboratorio: Foco, 20 min. Tabla, cinco piezas, puertos desde el otro extremo, bypass, diagnóstico y tabla de síntomas.
- Regla: primero la tabla firmada por las dos puntas, después el túnel, y el log para no adivinar.

## Divisiones (decisiones, no lecciones)
- Firewall por defecto o drop explícito. Un lado: no tocar la defconf y abrir agujeros puntuales (documentación y una escuela del foro). Otro: reescribir con un drop final y permitir solo lo explícito (otra escuela del foro, https://forum.mikrotik.com/t/trying-to-understand-defconf-firewall/267442). Cómo decidir: si el equipo lo van a tocar varios técnicos con nivel distinto, defconf; si tenés una plantilla propia probada y documentada, drop explícito.
- Rutas recursivas o Netwatch. Recursivas: sin scripts, de 20 a 30 segundos según un practicante. Netwatch: más rápido y flexible, con scripts que mantener (https://mkcontroller.com/blog/tutorials/mikrotik/mikrotik-dual-wan-failover-isp-guide/). Cómo decidir: si el sitio tolera medio minuto, recursivas; si hay voz o cobros, Netwatch con plantilla única para toda la flota.
- WireGuard, L2TP/IPsec o túnel saliente. WireGuard si podés instalar el cliente; L2TP/IPsec si el que se conecta solo tiene el cliente nativo del sistema (https://cloudzy.com/de/blog/mikrotik-l2tp-vpn/); túnel saliente a un VPS o Back To Home si el sitio está detrás de CGNAT (https://mkcontroller.com/blog/remote_access/mikrotik/remote_mikrotik_management_via_vps).
- Publicar cámaras o no. Una parte del foro lo trata como rutina; MikroTik y la prensa de seguridad empujan a no exponer nada. Cómo decidir: si quien mira tiene IP fija (una central de monitoreo), dst-nat filtrado por origen; si son celulares con IP cambiante, VPN o la nube del fabricante del NVR.
- Defconf o configuración desde cero. La documentación recomienda conservarla a principiantes; la guía de VLAN del foro arranca limpio. Cómo decidir: desde cero solo con plantilla probada y acceso de rescate.
- Stable o long-term. La documentación describe ambos sin elegir. Cómo decidir: long-term en sitios que se visitan poco; stable cuando necesitás una función nueva.

- (Ampliación) ONT de Antel en puente o en router. Puente: el MikroTik es el router del cliente, sin doble NAT (Antel ofrece el modo, https://antel.com.uy/personas/preguntas-frecuentes/internet). Router: usuarios de un foro uruguayo volvieron a ese modo por cortes en 2017 (https://www.macacos.com.uy/foros/viewtopic.php?id=17622). Cómo decidir: si vas a dar acceso remoto, VPN o publicar algo, puente; si el cliente solo navega y el sitio tuvo cortes en puente, router de Antel con el MikroTik por DHCP detrás, sabiendo que hay doble NAT.
- (Ampliación) Canal de producción. La documentación describe sin elegir y ofrece actualización automática; un distribuidor recomienda la rama de solo arreglos (https://blog.linitx.com/mikrotik-routeros-package-channel-bugfix-only-current-release-candidate-legacy/). Cómo decidir: long-term en clientes; stable solo si la función nueva hace falta y se probó.
- (Ampliación) Back To Home, CHR propio o servicio de terceros para CGNAT. Back To Home: gratis, solo ARM, pasa por relays de MikroTik. CHR propio: control total, cuesta licencia y mantenimiento. Servicio de terceros: menos trabajo, dependencia de un proveedor (MKController lo ofrece, sesgo comercial). Cómo decidir: pocos sitios ARM, Back To Home; flota mixta o con MIPS, concentrador CHR.
- (Ampliación) Clave compartida o certificados en IPsec. La documentación aconseja evitar la clave compartida (https://manual.mikrotik.com/docs/7.25/virtual-private-networks/ipsec/); los ejemplos prácticos la usan. Cómo decidir: clave larga y única por túnel para pocos sitios; certificados cuando crece la cantidad de túneles o el otro extremo lo soporta.
- (Ampliación) NAT-T encendido o apagado. Apagado con IPs públicas en las dos puntas (https://getlabsdone.com/setup-ipsec-site-to-site-vpn-tunnel-between-pfsense-and-mikrotik/); encendido si alguien puede estar detrás de NAT (https://cloudzy.com/de/blog/mikrotik-l2tp-vpn/). Cómo decidir: encendido salvo que el otro extremo pida lo contrario y no haya NAT en el camino.

- (Lección 23) Quedarse en Safe Mode todo el trabajo o alternarlo por paso. Todo el trabajo: lo propone una guía universitaria de laboratorio (https://cyberlab.pacific.edu/courses/comp177/resources/routeros-overview). Por paso: la documentación pide pasos chicos por el tope de 100 acciones (https://manual.mikrotik.com/docs/7.25/getting-started/configuration-management/) y un veterano del foro aconseja alternarlo entre pasos. Cómo decidir: en equipos de clientes, por paso; confirmar cada cambio verificado evita que un error tardío se lleve todo lo bueno.
- (Lección 23) Safe Mode o restauración programada. Safe Mode cubre el error que corta la sesión; cuando el cambio corta la sesión a propósito (mover la VPN de gestión), se deshace igual. Un veterano propone backup y scheduler que restaura a los 5 minutos (https://forum.mikrotik.com/t/how-to-execute-risky-mikrotik-commands-safely/165189). Cómo decidir: Safe Mode por defecto; restauración programada solo para cambios que te van a desconectar sí o sí.

- (Lección 24) Hairpin con masquerade o DNS local. La documentación enseña el masquerade (https://manual.mikrotik.com/docs/7.25/firewall-and-quality-of-service/firewall/nat); en el foro prefieren DNS dividido o una subred propia para que el servidor vea la IP real del cliente (https://forum.mikrotik.com/t/hairpin-nat-using-local-dns/174370). Cómo decidir: si el puerto externo es igual al interno y en la oficina usan un nombre, DNS local; si el puerto cambia o usan la IP pública escrita, hairpin; si el NVR ya está en su VLAN, alcanza con que el dst-nat coincida desde la LAN.
- (Lección 24) Cuántos puertos publicar en Dahua. El aviso oficial dice que suele alcanzar con HTTP y 37777 (https://www.dahuasecurity.com/about-dahua/news-events/notice/how-to-setup-remote-access-for-nvr); un integrador del foro sumó 443, 554 y 37778 UDP para ver video (https://forum.mikrotik.com/t/need-help-with-port-forwarding/159605). Cómo decidir: empezar por el puerto de la app y sumar de a uno mirando contadores, nunca rangos por las dudas.

## Huecos
- DHCP con reservas para cámaras y NVR, opciones DHCP y DNS estático: ninguna fuente leída lo cubre en detalle; el curso lo menciona solo dentro de la lección de VLAN.
- Logs remotos (syslog) y /system logging: sin página dedicada; la lección 12 usa solo log=yes en una regla.
- Puertos específicos de NVR por fabricante: la lección 10 usa puertos de ejemplo; la lección 24 los toma del aviso de Dahua y de practicantes de Hikvision. La lista oficial de puertos de Hikvision (us-legacy.hikvision.com) no se pudo guardar en raw/, así que la tabla de Hikvision se apoya en learncctv.com y en un distribuidor británico.
- Netwatch y L2TP/IPsec: solo cubiertos por practicantes con producto propio; las lecciones lo dicen.
- WebFig y SSH como herramientas de trabajo: cubiertos solo en la parte de seguridad.

- (Ampliación) Antel: ninguna página leída de antel.com.uy publica VLAN, MTU ni formato de usuario PPPoE para router propio; los hilos de GameOver Uruguay sobre el tema no se pudieron leer (protección anti bots). La lección 15 dice qué está confirmado y qué hay que preguntar a Antel.
- (Ampliación) IPsec con Fortinet, Cisco y Ubiquiti: solo se leyó una guía con pfSense; la lección 22 da la tabla genérica.
- (Ampliación) Instalación de CHR: la guía leída es de Hetzner y usa una imagen 6.49; las guías oficiales por proveedor existen pero no se agregaron por el tope de páginas oficiales.
- (Ampliación) Límite de downgrade a la versión de fábrica: la página oficial no está en raw/; la lección 16 no lo afirma.

- (Lección 23) Corte de energía en Safe Mode: la página de la CLI dice que la configuración se escribe en disco al salir del modo seguro; usuarios del foro vieron el cambio confirmado tras un corte de energía en 6.40.4. No se encontró confirmación para RouterOS 7; la lección dice que el corte de energía no es una forma de deshacer.
- (Lección 23) Timeout de la reversión: la documentación da 9 minutos de timeout TCP; el foro reporta segundos o un minuto; una guía no oficial lo llama configurable, sin respaldo en la documentación. La lección da el rango.
- (Lección 23) Qué pasa al cerrar WinBox con el botón Safe Mode apretado: ninguna fuente leída lo documenta; la lección enseña a soltar el botón antes de desconectar.

## Entrega
Cada lección: script.txt (diálogo Lucía y Martín, 260 a 360 palabras), card.md y quiz.json de 3 preguntas. En el portal no hay audio: script.txt se muestra como texto opcional ("La charla"). Ficha del curso en class/course.json.

## Lecciones agregadas (pedido de Nico, octubre 2026)

### 25. Un solo bridge
- 4 de 5 fuentes coinciden en un bridge por equipo con la IP en el bridge (https://manual.mikrotik.com/docs/7.25/bridging-and-switching/, https://manual.mikrotik.com/docs/7.25/bridging-and-switching/user-guides/layer2-misconfiguration, https://manual.mikrotik.com/docs/7.25/getting-started/manual-network-setup); un hilo del foro matiza: en routers sin switch chip da casi igual y en equipos con dos chips hay un bridge con offload por chip (https://forum.mikrotik.com/t/one-or-more-bridges/146916).
- Idea: los puertos del bridge son esclavos; la marca H dice que conmuta el switch chip; fuera de CRS1xx/2xx solo un bridge por chip tiene offload; separar con VLAN. Las configuraciones por defecto: AP Router deja ether1 afuera como WAN, Switch mete todos los puertos (https://manual.mikrotik.com/docs/7.25/getting-started/configuration-management/default-configurations).
- Por qué importa: un segundo bridge para cámaras manda el tráfico a la CPU sin que nadie lo note.
- Historia: el router que "murió" al sacar ether2 del bridge porque el bridge usaba la MAC de ese puerto (https://forum.mikrotik.com/t/remove-port-from-the-default-brige/125811).
- Laboratorio: Foco, 15 min. Leer bridge y puertos, admin-mac, sacar ether5 con red propia, ether1 como WAN si estaba adentro, volver.
- Regla: un bridge por equipo, la IP en el bridge, y lo que hay que separar va por VLAN.

### 26. Asignar IP
- 4 de 4 fuentes oficiales coinciden (https://help.mikrotik.com/docs/spaces/ROS/pages/328247/IP+Addressing, https://manual.mikrotik.com/docs/7.25/getting-started/networking-fundamentals/, https://manual.mikrotik.com/docs/7.25/network-management/dhcp/server, https://manual.mikrotik.com/docs/7.25/getting-started/manual-network-setup).
- Idea: dirección con máscara e interfaz, ruta conectada automática, varias IP por interfaz, IP en bridge o VLAN y nunca en un puerto esclavo; servidor DHCP en cuatro piezas (IP, pool sin la IP del router, network, servidor) o con setup.
- Por qué importa: es la base de cada red del sitio y de cada "la cámara no toma IP".
- Historia: la documentación avisa que el servidor DHCP no anda en un bridge vacío y que prueba cada dirección con ARP y ping antes de ofrecerla.
- Laboratorio: Rápido, 15 min. Leer direcciones y rutas conectadas, segunda IP temporal, red de cámaras en ether5 con su DHCP y una reserva.
- Regla: la IP va en el bridge o en la VLAN; el pool, sin la IP del router y con lugar para las fijas.

### 27. Rutas estáticas
- 3 de 3 fuentes coinciden en la selección: más específica primero, después menor distancia (https://manual.mikrotik.com/docs/7.25/user-guides/routing-and-networking-protocols/routing-decision, https://help.mikrotik.com/docs/spaces/ROS/pages/328084/IP+Routing, https://mikrotikdocs.fyi/ip/static-routes-basic/, esta última no oficial).
- Idea: ruta por defecto, gateway, distance, check-gateway (cada 10 s, dos fallas), rutas a redes remotas por el túnel, ruta /32 a la IP pública del VPN cuando la default va por el túnel.
- Por qué importa: un respaldo mal armado o una ruta de vuelta olvidada son las fallas más comunes al unir sitios.
- Historia: tres MikroTik con L2TP; las sucursales no se veían hasta rutear en las dos puntas (https://forum.mikrotik.com/t/static-routes-l2tp/181714).
- Laboratorio: Foco, 15 min. Leer la tabla, ruta por un gateway muerto, check-gateway, respaldo con distancia 2, las dos rutas del túnel.
- Regla: gana la más específica, después la de menor distancia; y toda ruta hacia allá necesita su ruta de vuelta.

### 28. L2TP saliente
- 3 de 4 fuentes coinciden en el cliente con IPsec y las rutas en las dos puntas (https://manual.mikrotik.com/docs/7.25/virtual-private-networks/l2tp/, https://manual.mikrotik.com/docs/7.25/cli-reference/interface/l2tp-client/, https://forum.mikrotik.com/t/static-routes-l2tp/181714); un veterano agrega el src-nat cuando no se puede rutear del otro lado (https://forum.mikrotik.com/t/site-to-site-l2tp-vpn/135121).
- Idea: el sitio llama a la central con /interface/l2tp-client, use-ipsec=yes, add-default-route=no; ruta a la LAN central por la interfaz; ruta de vuelta en el servidor o masquerade hacia el túnel; el túnel en la lista WAN si el otro extremo no es tuyo.
- Por qué importa: es la forma de unir un sitio con CGNAT a la central sin abrir puertos.
- Historia: la sucursal por 4G que llegaba desde el router y no desde las PC; un IPsec viejo seguía intentando por detrás (https://forum.mikrotik.com/t/site-to-site-l2tp-vpn/135121). Con add-default-route, la ruta /32 al servidor aparece sola (https://forum.mikrotik.com/t/send-all-traffic-through-l2tp-vpn/141695).
- Laboratorio: Foco, 20 min. Usuario en el servidor, cliente con IPsec, verificación, rutas, NAT por el túnel, firewall, prueba opcional de add-default-route.
- Regla: el sitio llama a la central con IPsec, sin ruta por defecto, y cada LAN tiene su ruta de ida y su ruta de vuelta.

### 29. Diagnóstico por terminal
- 5 de 6 fuentes coinciden en ir de adentro hacia afuera y en leer la pérdida por salto (https://manual.mikrotik.com/docs/7.25/diagnostics-monitoring-and-troubleshooting/ping, https://manual.mikrotik.com/docs/7.25/diagnostics-monitoring-and-troubleshooting/traceroute, https://forum.mikrotik.com/t/traceroute-output/157966, https://en.wikipedia.org/wiki/Traceroute); en el hilo del foro, quien lo abrió leía la pérdida del salto 2 como un corte del proveedor.
- Idea: escalera de pings (LAN, gateway, IP de internet, nombre); ARP ping para equipos que bloquean ICMP; traceroute con rondas como mtr, donde la pérdida real sigue en todos los saltos siguientes; src-address para probar masquerade y túneles; do-not-fragment con size para la MTU (size es el paquete entero).
- Por qué importa: cada ticket de "no anda internet" sale con el lugar de la falla y evidencia.
- Historia: 100% de pérdida en el salto 2 que no era una caída (https://forum.mikrotik.com/t/traceroute-output/157966); RouterOS manda 1500 con DF y Linux solo 1472 de datos (https://forum.mikrotik.com/t/ping-from-routeros-relationship-with-mtu/80144).
- Laboratorio: Campo, 20 min. Escalera de cuatro pings, ARP ping, traceroute con tabla de lectura, src-address con el masquerade apagado y prendido, MTU.
- Regla: pruebo de adentro hacia afuera, y una pérdida que no sigue en los saltos siguientes no es una falla.

### 30. DNS en MikroTik
- 4 de 4 fuentes coinciden en cerrar el 53 hacia internet (https://manual.mikrotik.com/docs/7.25/network-management/dns, https://forum.mikrotik.com/t/dns-amplification-attack/68310, https://csirt.lacnic.net/en/dns-open-resolvers-on-ipv4, https://docs.quad9.net/Setup_Guides/Open-Source_Routers/MikroTik_RouterOS_(Encrypted)/); en DoH, un practicante deja respaldo (https://medo64.com/posts/dns-over-https-for-mikrotik) y la documentación 7.25 dice que no hay.
- Idea: resolver con caché, servers y dynamic-servers, allow-remote-requests y el riesgo de resolver abierto, drop UDP y TCP 53 desde la WAN, estáticas, caché, DoH sin respaldo y con HTTP/2 solo en ARM64 y x86.
- Por qué importa: un resolver abierto presta el router a ataques de amplificación, y un DNS mal entendido parece "internet caída".
- Historia: routers con la CPU al 100% por amplificación DNS en 2013 (https://forum.mikrotik.com/t/dns-amplification-attack/68310); el CSIRT de LACNIC rastrea resolvers abiertos en la región.
- Laboratorio: Foco, 20 min. Estado, servidores, prueba del 53 desde la red de la WAN, estática para el NVR, caché, DoH con el log abierto.
- Regla: el DNS del router contesta a la LAN y a nadie más, y lo pruebo con nslookup desde adentro y desde afuera.

### 31. DNS transparente
- 4 de 5 fuentes coinciden en redirigir UDP y TCP 53 (https://manual.mikrotik.com/docs/7.25/network-management/dns, https://forum.mikrotik.com/t/dns-redirect-action-redirect-vs-dst-nat/138046, https://forum.mikrotik.com/t/force-dns-request/180041, https://forum.mikrotik.com/t/help-redirecting-doh-requests-to-internal-dns/157195); discrepan sobre DoH: listas de bloqueo (https://forum.mikrotik.com/t/redirecting-or-blocking-doh-dns-over-https-requests-made-by-clients/147912) o convivir con eso.
- Idea: estáticas y adlists solo alcanzan a quien le pregunta al router; dos reglas dstnat redirect desde LAN con dst-address-type=!local; dst-nat para un Pi-hole; lista de excepciones; DoH no se redirige: dominio canario de Firefox y cortar DoT 853 como paliativos.
- Por qué importa: los bloqueos y nombres locales llegan a todos los equipos, incluidos los que traen el DNS clavado.
- Historia: Torch muestra 8.8.8.8:443 y el AdGuard queda salteado (https://forum.mikrotik.com/t/force-dns-request/180041).
- Laboratorio: Foco, 15 min. Estática de prueba, nslookup a 8.8.8.8 antes y después, excepción, contadores, canario y DoT.
- Regla: UDP y TCP 53 de la LAN van al DNS que yo elijo, con una lista de excepciones, y sé que DoH queda afuera.

### 32. Bloqueo por DNS
- 4 de 5 fuentes coinciden en bloquear por nombre en el DNS del router y en sus límites (https://manual.mikrotik.com/docs/7.25/network-management/dns, https://manual.mikrotik.com/docs/7.25/firewall-and-quality-of-service/firewall/address-lists, https://forum.mikrotik.com/t/v7-15rc-testing-is-released/175351, https://forum.mikrotik.com/t/blocked-allowed-websites-by-firewall-filter-rules/158566); antes de adlist, un veterano recomendaba un DNS externo filtrante (https://forum.mikrotik.com/t/ad-blocking-by-static-dns-just-dont-do-it/111280).
- Idea: adlist desde 7.15 (0.0.0.0, caché de unos 75 bytes por nombre, solo el nombre exacto, ARM64 recomendado), NXDOMAIN con match-subdomain para un sitio, FWD como excepción, FWD con address-list para el firewall, límites de CDN, DoH y VPN.
- Por qué importa: el pedido de "sacar publicidad y bloquear tal sitio" se resuelve en el router y con expectativas claras.
- Historia: 5000 estáticas en un RB951 y la CPU al 80% (https://forum.mikrotik.com/t/ad-blocking-by-static-dns-just-dont-do-it/111280); adlist llega en 7.15 con la recomendación de ARM64 (https://forum.mikrotik.com/t/v7-15rc-testing-is-released/175351).
- Laboratorio: Foco, 20 min. Versión y memoria, adlist por archivo, NXDOMAIN, excepción y pausa, FWD con address-list y reject en forward, limpieza.
- Regla: bloqueo por nombre en el DNS del router, con caché a medida y DNS transparente, y le digo al cliente que DoH y VPN quedan afuera.

- (Lecciones 29 a 32, divisiones) DoH en el router con o sin respaldo: un practicante deja los servidores comunes de respaldo; la documentación 7.25 dice que con DoH activo no se usan y que, si el servidor no responde, la LAN recibe SERVFAIL. Cómo decidir: en clientes, DoH solo con un servicio confiable y monitoreado; si el sitio no tolera quedarse sin nombres, DNS común. Bloquear DoH de los clientes o convivir: listas de servidores DoH (blanco móvil, pueden romper apps) o aceptar el límite y explicarlo. Cómo decidir: listas solo en redes donde el filtro es un requisito (escuela, hotel con contrato); en el resto, DNS transparente y expectativas claras.
- (Lecciones 29 a 32, huecos) La página de Mozilla sobre el dominio canario no se pudo guardar (solo JavaScript): la lección 31 lo cita a través del hilo del foro que lo enlaza. El repositorio de listas StevenBlack en GitHub no se pudo guardar: la lección 32 usa una adlist por archivo y menciona `url=` sin dirección. El artículo de APNIC sobre leer traceroute solo guardó un comentario de lector.

### 33. Reglas de protección
- 6 de 7 fuentes coinciden en la estructura input/forward con drop final y en no exponer DNS ni gestión (https://help.mikrotik.com/docs/spaces/ROS/pages/328513/Building+Advanced+Firewall, https://manual.mikrotik.com/docs/7.25/firewall-and-quality-of-service/firewall/filter, https://forum.mikrotik.com/t/trying-to-understand-defconf-firewall/267442, https://manual.mikrotik.com/docs/7.25/getting-started/securing-your-router); en fuerza bruta, la documentación propone listas por etapas como capa extra (https://manual.mikrotik.com/docs/7.25/firewall-and-quality-of-service/user-guides/bruteforce-prevention) y un veterano del foro las considera casi inútiles (https://forum.mikrotik.com/t/bruteforce-prevention-issue/123058).
- Idea: input con established/related, invalid, ICMP (límite opcional desde WAN), admins por address-list y drop final; forward con FastTrack, invalid y drop de WAN sin dst-nat; drop de UDP y TCP 53 desde WAN; listas por etapas de SSH con la lista admins exceptuada arriba.
- Por qué importa: es el firewall que el técnico hereda o escribe en cada cliente, y un DNS abierto o un SSH expuesto se descubren cuando ya hay daño.
- Historia: 409 GB de subida en una semana por un DNS abierto (https://forum.mikrotik.com/t/large-bandwidth-usage-upstream-on-idle/94237); 27 intentos y bloqueo de un día, o 2.600 por día para el atacante paciente (https://manual.mikrotik.com/docs/7.25/firewall-and-quality-of-service/user-guides/bruteforce-prevention).
- Laboratorio: Foco, 20 min. Leer la defconf, ping limitado, drop del 53 desde WAN, listas por etapas con admins exceptuados, prueba con cuatro SSH y desbloqueo.
- Regla: input cuida al router, forward cuida a la LAN, y lo que no permití a propósito termina en un drop.

### 34. Descubrir vecinos
- 5 de 6 fuentes coinciden en usar el descubrimiento dentro de la LAN y apagarlo hacia afuera (https://manual.mikrotik.com/docs/7.25/system-information-and-utilities/neighbor-discovery, https://manual.mikrotik.com/docs/7.25/cli-reference/ip/neighbor/discovery-settings, https://forum.mikrotik.com/t/controlling-where-lldp-is-sent/115188); un practicante propone filtrar UDP 5678 y otro usuario no logra ocultar el router así (https://forum.mikrotik.com/t/ip-neighbor-discovery/125004). Historia de los protocolos: https://en.wikipedia.org/wiki/Link_Layer_Discovery_Protocol, https://en.wikipedia.org/wiki/Cisco_Discovery_Protocol.
- Idea: /ip/neighbor y /ip/neighbor/lldp para encontrar switches, teléfonos y otros MikroTik con su puerto físico; discover-interface-list solo con puertos propios (de fábrica es static, con defconf LAN); protocol=lldp,mndp si no hay Cisco.
- Por qué importa: ahorra seguir cables en racks heredados y evita que el router anuncie nombre, versión e IP hacia la WAN o redes ajenas.
- Historia: el usuario que vio salir su propio LLDP por el puerto de internet con el sniffer (https://forum.mikrotik.com/t/controlling-where-lldp-is-sent/115188).
- Laboratorio: Rápido, 15 min. Vecinos y puerto, tabla LLDP, discovery-settings, lista propia con puertos sueltos, verificación desde la WAN.
- Regla: el router se presenta solo en los puertos que son míos.

### 35. Vigilar con Netwatch
- 4 de 5 fuentes coinciden en el uso de sondas y scripts al caer y volver (https://manual.mikrotik.com/docs/7.25/diagnostics-monitoring-and-troubleshooting/netwatch, https://manual.mikrotik.com/docs/7.25/cli-reference/tool/netwatch, https://manual.mikrotik.com/docs/7.25/system-information-and-utilities/e-mail, https://forum.mikrotik.com/t/advanced-netwatch/158909); discrepan en failover (https://mkcontroller.com/blog/tutorials/mikrotik/mikrotik-dual-wan-failover-isp-guide/) y en reinicio de PoE por script o por power-cycle-ping (https://manual.mikrotik.com/docs/7.25/hardware/poe-out).
- Idea: sondas simple, icmp, tcp-conn, http-get, https-get y dns; tcp-conn al servicio del NVR; icmp con umbral contra falsas alarmas; avisos por e-mail y por Telegram con fetch output=none; reinicio de PoE; startup-delay de 5 minutos; el router no avisa su propia caída.
- Por qué importa: el integrador se entera antes que el cliente y algunas fallas se arreglan solas.
- Historia: los avisos a Telegram que se cortaron con 7.13 hasta agregar output=none (https://forum.mikrotik.com/t/netwatch-with-fetch-stopped-working-after-7-13/172865); el ping suelto que disparaba falsas alarmas (https://forum.mikrotik.com/t/advanced-netwatch/158909); el router que no puede avisar si está caído (https://forum.mikrotik.com/t/telegram-bot-message-when-internet-is-down/160188).
- Laboratorio: Foco, 20 min. Sonda tcp-conn al NVR con log, prueba desenchufando, mail, Telegram, reinicio de PoE.
- Regla: cada equipo crítico tiene su sonda y su aviso, probado desenchufando después de cada actualización.

- (Lecciones 33 a 35, divisiones) Listas de fuerza bruta: la documentación las da como capa extra; un veterano del foro las ve casi inútiles. Cómo decidir: solo si SSH tiene que quedar abierto a WAN, con la lista de admins arriba; lo primero es VPN y claves. Limitar ICMP o dejarlo al kernel (100 pps según MikroTik): opcional; si se limita, solo echo desde WAN. Reinicio de PoE por script de Netwatch o por power-cycle-ping: el vigilante del puerto no depende de scripts; Netwatch permite además avisar. Una sola de las dos por puerto. Ocultar el descubrimiento filtrando UDP 5678 o sacando la interfaz de la lista: la lista.
- (Lecciones 33 a 35, huecos) Ninguna fuente leída confirma qué modelos de cámaras o NVR anuncian LLDP: la lección 34 dice "según modelo y firmware". La documentación 7.26 (aún no estable a la fecha) dice que la sonda simple tiene intervalo de 60 s por defecto y la referencia 7.25 dice 10 s: la lección 35 fija interval en cada comando. No se guardó la API de Telegram (página enorme): el formato sendMessage sale de los hilos del foro.
