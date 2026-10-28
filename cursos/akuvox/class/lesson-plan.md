# Plan de lecciones: Porteros IP Akuvox, de la caja a la puerta abierta

Nivel: inicial a intermedio. Público: técnicos instaladores y de soporte con base de redes. 41 lecciones: los 3 arcos originales de fundamentos (lecciones 1 a 12, sin cambios porque hay técnicos con avance guardado), la parte Relés por HTTP (13 a 18) y el catálogo por tipo de dispositivo (19 a 41). Fuentes: 55 páginas en raw/web (20 de knowledge.akuvox.com, 10 de akuvox.com, 2 del portal de soporte de Akuvox, 1 de la app SmartPlus en Google Play, 3 de Yeastar, 3 de Grandstream, 2 de 3CX, 3 de la comunidad FreePBX, 3 de Asterisk, 2 de Claroty Team82, 1 de CISA, y una página cada uno de Home Assistant, MikroTik, pylocal-akuvox, el foro LogicMachine y ComfortClick). Los conteos "N de M" salen de research/agreement-map.md.

Nota de búsqueda: el presupuesto de búsquedas web del turno estaba agotado al empezar. Las páginas se encontraron navegando índices propios de los sitios (llms.txt de la Knowledge Base de Akuvox, sitemaps de Grandstream, 3CX, FreePBX, Asterisk y Claroty) y enlaces salientes de páginas abiertas. Ninguna url es inventada.

Nota de la ampliación (27 de octubre de 2026): las páginas nuevas de la Knowledge Base salieron de su llms.txt; las de akuvox.com, del menú de productos del propio sitio; las de terceros, de búsquedas web de ese día. Las 10 páginas de akuvox.com tienen todo el contenido dentro de un formulario ASP.NET que el scraper descarta (las guardaba con 0 palabras); se guardaron con un extractor mínimo que escribe el mismo encabezado que el scraper (título, url, palabras) y el texto visible de la página sin scripts. "Vigente" en este curso quiere decir "listado en el menú de productos de akuvox.com el 27 de octubre de 2026".

## Arco 1. De la caja a la red (lecciones 1 a 4)
Por qué este arco: antes de integrar nada, el técnico necesita entrar al equipo, saber exactamente qué tiene en la mano, hacer la primera llamada y que el relé mueva una cerradura de verdad. Termina con un portero y un monitor hablando y una puerta que abre.

### 1. Primer acceso
- 3 de 3 fuentes coinciden (TH02, TH03).
- Idea: cada familia muestra su IP de otra manera (voz, pantalla, código, IP Scanner); con la IP se entra por web con admin/admin y se cambia esa clave el primer día.
- Por qué importa: es la media hora que más se pierde en obra.
- Historia: el PIN de sistema del E16 es "admin" hasta 216.30.10.121 y "Admin321" después (https://knowledge.akuvox.com/docs/before-entering-device-web-interface). Grandstream usa el E12S que dice su IP en voz alta (https://documentation.grandstream.com/knowledge-base/wp8x6-access-control-systems-configuration-guide/).
- Laboratorio: Rápido, 10 min. Sacar la IP de un portero y de un monitor por dos caminos y entrar a la web.
- Regla: la IP se pide al equipo, no se adivina, y la clave de fábrica no pasa la primera visita.

### 2. Leer el firmware
- 2 de 3 fuentes coinciden (TH01, TH05, TH06).
- Idea: el número A.B.C.D dice modelo, OEM, rama y versión; además hay versiones de hardware con firmware distinto. Se actualiza con el archivo exacto y sin cerrar la ventana.
- Historia: un R20A con etiqueta V3.0 es en realidad hardware 2 (https://knowledge.akuvox.com/docs/upgrade-devices).
- Laboratorio: Admin, 15 min. Decodificar el firmware de dos equipos, bajar el archivo correcto, backup y actualizar uno.
- Regla: modelo, hardware y rama antes de bajar un firmware.

### 3. Llamada directa
- 2 de 2 fuentes coinciden (TH07, evidencia escasa).
- Idea: portero y monitor en la misma red se llaman por IP sin servidor; alcanza para una casa y conserva funciones que a veces se pierden por una central.
- Historia: la vista previa de video andaba por IP directa y no a través de FreePBX (https://community.freepbx.org/t/early-media-doorphone-video-preview/99698).
- Laboratorio: Rápido, 10 min. Llamada IP directa portero a monitor y apertura desde la pantalla.
- Regla: casa simple, IP directa; central solo cuando aporta algo.

### 4. Relé y cerradura
- 2 de 2 fuentes coinciden (TH15, TH16, evidencia escasa).
- Idea: elegir NO o NC según la cerradura sea fail-safe o fail-secure, alimentarla aparte y usar las entradas para botón de salida y alarma de puerta abierta.
- Historia: Grandstream explica que NC con COM abre al cortarse la luz (https://documentation.grandstream.com/knowledge-base/gds3710-two-doors-control-configuration-guide/).
- Laboratorio: Campo, 20 min. Cablear una cerradura de banco o una lámpara de 12 V, probar el tiempo de apertura y el botón de salida.
- Regla: primero decido qué pasa cuando se corta la luz; después elijo el borne.

## Arco 2. La puerta que abre (lecciones 5 a 8)
Por qué este arco: es el trabajo diario de una obra con central telefónica y varios accesos. Termina con portero y monitor registrados en la central, apertura por DTMF confiable, usuarios cargados y dos puertas que se abren desde un solo monitor.

### 5. Cuenta SIP
- 6 de 8 fuentes coinciden (TH08, TH10).
- Idea: el portero y el monitor se registran en la central como extensiones comunes, en Account > Basic; hay dos cuentas y la 1 la toma SmartPlus si está activo.
- Historia: el R20A de FreePBX que no registraba por la contraseña y después se llamaba con un asterisco de más (https://community.freepbx.org/t/solved-sip-registration-failed-on-doorphone-akuvox-r20a/85457).
- Laboratorio: Foco, 20 min. Crear dos extensiones en una central de laboratorio (UCM, FreePBX o Yeastar) y registrar portero y monitor.
- Regla: una extensión por equipo, anotada, y verificación en la central antes de irse.

### 6. DTMF que abre
- 5 de 5 coinciden en mismo tipo y mismo código (TH12); 3 de 5 en preferir RFC 2833 (TH13); discrepa Akuvox sobre SIP INFO frente a 3CX.
- Idea: el tipo de DTMF (RFC 2833, SIP INFO, inband) y el código tienen que coincidir en portero, central y monitor; la lista blanca DTMF limita quién abre.
- Historia: Yeastar abre con el 0 que trae el portero de fábrica (https://help.yeastar.com/en/p-series-appliance-edition/integrations/akuvox/control-door-access-via-linkus-clients.html); 3CX desaconseja SIP INFO (https://www.3cx.com/blog/voip-howto/dtmf-rfc2833/).
- Laboratorio: Foco, 15 min. Abrir por DTMF con RFC 2833, cambiar el monitor a SIP INFO para ver la falla y volver.
- Regla: RFC 2833 en las tres puntas y código distinto del de fábrica.

### 7. Usuarios y horarios
- 1 de 1 (TH17 a TH20, evidencia escasa, todo de la guía del E16).
- Idea: cada usuario lleva su PIN, tarjetas, rostro, relé y horario; el PIN público de fábrica se cambia; la carga masiva se hace con el CSV dentro del tgz.
- Historia: PIN público 33333333 por defecto y antisuplantación en "Close" que deja pasar una foto (https://knowledge.akuvox.com/docs/door-unlock-configuration-8).
- Laboratorio: Admin, 15 min. Crear un horario, dos usuarios, exportar, sumar tres por CSV e importar.
- Regla: nadie entra con "Always" si tiene un horario real.

### 8. Dos puertas
- 3 de 4 fuentes coinciden (TH21, TH22); discrepa el hilo de FreePBX que lo resuelve por HTTP.
- Idea: con un portero de dos relés, un código DTMF por relé y una tecla por puerta en el monitor; con dos porteros, el DTMF solo llega al que está en llamada, y para el otro se usa un comando HTTP con usuario propio.
- Historia: dos porteros abiertos con dos comandos desde la central (https://community.freepbx.org/t/how-can-i-manage-double-doorphone-doorlock/97459); el mismo código en dos puertas abre ambas (https://documentation.grandstream.com/knowledge-base/gds3710-two-doors-control-configuration-guide/).
- Laboratorio: Foco, 20 min. Dos teclas de apertura en el monitor y un comando HTTP probado con curl.
- Regla: cada puerta tiene su código y cada comando HTTP su usuario.

## Arco 3. Video, nube y seguridad (lecciones 9 a 12)
Por qué este arco: lo que separa una instalación que anda de una que se sostiene: video en el NVR, app para el residente sin depender de una sola cosa, el portero fuera de internet y un método para diagnosticar. Termina con un portero blindado y un kit de evidencia para soporte.

### 9. RTSP al NVR
- 1 de 1 (TH24, evidencia escasa).
- Idea: el portero entrega dos streams RTSP (ch00_0 y ch00_1) y ONVIF; se agrega al NVR con credenciales propias y el stream secundario para vista en grilla.
- Historia: valores por defecto 25 fps, 2048 y 512 kbps (https://knowledge.akuvox.com/docs/monitor-and-image-13).
- Laboratorio: Rápido, 10 min. Probar el RTSP con ffprobe o VLC y agregarlo al NVR.
- Regla: el NVR graba el ch00_1 si no necesita detalle, y nunca con admin/admin.

### 10. SmartPlus con plan B
- 2 de 3 fuentes coinciden (TH23, TH10); discrepa Claroty sobre exponer el equipo.
- Idea: SmartPlus da app, llaves temporales y Bluetooth, pero ocupa la cuenta SIP 1 y depende de internet; conviene dejar el monitor local funcionando igual.
- Historia: reseñas de la app con llamadas que fallan al azar y notificaciones tardías (https://play.google.com/store/apps/details?id=com.akuvox.mobile.smartplus&hl=en&gl=US&pli=1).
- Laboratorio: Admin, 15 min. Dibujar qué sigue andando si se cae internet y probarlo desconectando el WAN.
- Regla: si se corta internet, el monitor abre igual.

### 11. Portero blindado
- 3 de 11 fuentes coinciden en no exponer (TH27 a TH30); Yeastar y SmartPlus asumen salida a internet.
- Idea: red separada, nada de reenvío de puertos al portero, claves propias en web, RTSP, ONVIF y HTTP, lista blanca SIP, firmware al día; la central también se asegura.
- Historia: Claroty encontró 13 vulnerabilidades en el E11 y unos 5.000 equipos expuestos (https://claroty.com/team82/research/the-silent-spy-among-us-modern-attacks-against-smart-intercoms); CISA puntúa 9,8 (https://www.cisa.gov/news-events/ics-advisories/icsa-23-068-01).
- Laboratorio: Campo, 20 min. Escanear el portero desde la red de usuarios con nmap y cerrar lo que responda de más.
- Regla: el portero vive en su VLAN y solo habla con la central, el NVR y la gestión.

### 12. Diagnóstico con evidencia
- 2 de 3 fuentes coinciden (TH09, TH25, TH31, TH32).
- Idea: registro que falla, DTMF que no abre o video que no aparece se resuelven con log de la central, PCAP del portero y versión de firmware; soporte de Akuvox pide exactamente eso.
- Historia: la vista previa que se rompía por la "r" del Dial (https://community.freepbx.org/t/early-media-doorphone-video-preview/99698); PCAP de 1 MB arrancada justo antes de reproducir (https://ticket.akuvox.com/support/solutions/articles/48001200817-read-first-how-to-provide-information-to-effectively-resolve-a-technical-issue-on-akuvox-intercom-).
- Laboratorio: Foco, 20 min. Romper el registro a propósito, encontrarlo en el log y en la PCAP, y armar el paquete para soporte.
- Regla: sin firmware, config, log y captura no hay ticket.

## Parte 4. Relés por HTTP (lecciones 13 a 18)
Por qué esta parte: la apertura por DTMF solo llega al portero que está en llamada; el HTTP abre cualquier relé desde cualquier sistema de la obra, y por eso mismo es lo primero que hay que asegurar. Termina con un portero que abre por URL con usuario propio, avisa sus eventos y recibe órdenes de Home Assistant, MikroTik, Asterisk o una cámara.

### 13. La URL que abre
- 2 de 3 fuentes coinciden (TH33, TH34, TH35); discrepa el foro LogicMachine.
- Idea: Open Relay via HTTP con usuario propio; con la rama de alta seguridad (tercer número del firmware 10 o más, interruptor en Security) solo vale /fcgi/OpenDoor con credenciales en la URL; /fcgi/do queda para firmware viejo o con el interruptor apagado. DoorNum 1 es A, 2 es B.
- Por qué importa: la mitad de los "no abre" por HTTP son un formato que el firmware ya no acepta.
- Historia: los tres formatos y cuándo vale cada uno (https://knowledge.akuvox.com/docs/open-door-via-http-command); Session Check apagado.
- Laboratorio: Rápido, 10 min. Habilitar, probar el formato nuevo con curl, probar el viejo y ver el rechazo.
- Regla: primero leo el firmware, después elijo la URL.

### 14. Quién puede abrir
- 3 de 5 fuentes coinciden en credenciales propias y Digest o Allowlist (TH37, TH38, TH39, TH40); discrepan la guía que permite dejarlo en blanco y el foro LogicMachine.
- Idea: la HTTP API ofrece None, Allowlist, Basic y Digest; Basic viaja en claro; la clave en la URL termina en logs; usuario dedicado, VLAN de porteros, nada publicado a internet, HTTPS donde el equipo lo soporte.
- Historia: el integrador que apaga la alta seguridad y pone admin en la URL (https://forum.logicmachine.net/showthread.php?tid=6156); pylocal-akuvox advirtiendo los logs (https://pylocal-akuvox.readthedocs.io/en/latest/quickstart.html).
- Laboratorio: Admin, 15 min. HTTP API en Allowlist o Digest, curl desde una IP permitida y otra no, revisión de quién conoce la clave.
- Regla: un usuario por integración, nunca admin, y solo desde la VLAN.

### 15. Botón del monitor
- 1 de 7 (TH42); evidencia de una sola página oficial, con R29 y C313 de ejemplo.
- Idea: Remote Relay By HTTP or HTTPS en el monitor apunta al portero que no está en llamada; las teclas van en la pantalla de llamada, de monitoreo y de vista previa.
- Historia: el caso del portón con un portero y el hall con otro, que el DTMF no resuelve (lección 8) y el monitor sí por HTTP (https://knowledge.akuvox.com/docs/open-door-via-http-command).
- Laboratorio: Foco, 15 min. Tecla "Portón" en la pantalla de monitoreo de un monitor apuntando a un segundo portero.
- Regla: cada tecla HTTP lleva el nombre de la puerta y su propio usuario.

### 16. Relés de afuera
- 1 o 2 de 7 por tema (TH43 a TH48): cada pieza tiene su artículo propio y no se repiten entre sí.
- Idea: relé local A o B; Web Relay de terceros; SR01 adentro por RS485 o 12 V; MK485 o RSAC-C1-R8 en el monitor; WR01 como relé de borde. Trigger Delay y Hold Delay.
- Historia: el SR01 que mantiene la puerta cerrada aunque rompan el portero (https://knowledge.akuvox.com/docs/how-to-configure-sr01-security-relay-on-akuvox-door-phones).
- Laboratorio: Campo, 20 min. SR01 por RS485 en un portero de laboratorio, DoorNum=SB por HTTP; si no hay SR01, relé B con portón de banco.
- Regla: la cerradura importante se maneja desde adentro.

### 17. El portero avisa
- 2 de 2 (TH49, TH50, evidencia escasa).
- Idea: Action URL manda un GET a un servidor ante eventos (relé, entradas, códigos, tarjetas, llamadas) con variables como $relay1status y $mac.
- Historia: el integrador que escucha timbre y botón de salida por HTTP (https://www.comfortclick.com/Support/ExampleDetails/Akuvox).
- Laboratorio: Foco, 15 min. Servidor HTTP de una línea en la PC y ver llegar la apertura.
- Regla: lo que abre por HTTP también avisa por HTTP.

### 18. Abrir desde sistemas
- 7 de 7 coinciden en que cualquier cliente HTTP sirve (TH51); 3 de 7 en igualar basic o digest (TH52).
- Idea: Home Assistant rest_command, MikroTik /tool fetch, Asterisk CURL y cámaras LPR por la HTTP API; HikCentral y UCM sin acción HTTP documentada en las páginas leídas.
- Historia: la cámara Hikvision que abre el portón por patente (https://knowledge.akuvox.com/docs/integration-with-milesight-lpr-camera-for-door-opening).
- Laboratorio: Foco, 20 min. La misma apertura desde curl, MikroTik y Home Assistant, con digest donde corresponda.
- Regla: pruebo con curl, después lo muevo al sistema, y documento quién tiene la credencial.

## Parte 5. Porteros de calle (lecciones 19 a 29)
Por qué esta parte: el técnico se encuentra en obra con cualquier modelo de la línea, nuevo o viejo, y necesita saber en un minuto qué hace, cómo se alimenta, qué credenciales acepta y cómo se entra. Termina con una ficha por familia que sirve para cotizar, instalar y dar soporte.

### 19. Mapa del catálogo
- 3 de 7 (TH64) y 4 de 10 (TH55).
- Idea: el menú de productos de akuvox.com como fuente de lo vigente, las tablas de la Knowledge Base como fuente de datos transversales, y los sufijos de versión (S, C, W, A, P, K, L, -2).
- Historia: E16 y C316 siguen en el menú de octubre de 2026 (https://www.akuvox.com/products).
- Laboratorio: Admin, 15 min. Planilla de catálogo con tipo, serie, sistema, PoE y estado.
- Regla: vigente es lo que está en el menú del fabricante el día que cotizo.

### 20. S539 y S538
- 5 de 10 en alimentación (TH56), 4 de 10 en credenciales (TH55).
- Idea: los Android de la serie S: S539 de 10" con PoE+ e IP66 según la guía, y S538 "Tri-Vision"; rostro, Bluetooth y QR en los dos.
- Historia: el S538 resistente al frío que solo acepta fuente de 24 V 2 A (https://knowledge.akuvox.com/docs/devices-supporting-12v-power-output).
- Laboratorio: Campo, 15 min.
- Regla: Android grande, PoE+ o fuente de 24 V.

### 21. S535 y S532
- Idea: S535 Linux de 5" e IP66 con módulos (huella, LTE, QR, lazo de inducción); S532 de 2,8" en versiones estándar, IP y lazo de inducción, sin rostro ni QR.
- Historia: la tabla de PoE+ y fuente de 12 V del S532 (https://knowledge.akuvox.com/docs/power-supply-for-intercom-devices).
- Laboratorio: Admin, 10 min.
- Regla: el S535 se arma por módulos; el pedido lleva cada módulo.

### 22. X916 y X915
- 3 de 10 coinciden en confirmar IP e IK en la ficha (TH58); la guía y la ficha del X915 no coinciden.
- Idea: los Android de acero: X916 de 13" con cámara Starlight y relé de 5 A; X915 de 8" con versiones HID y palma, IP66 e IK10 en la ficha V2.0.
- Historia: el X915 IP65 en una página e IP66 en otra (https://www.akuvox.com/productsDisp?pid=37).
- Laboratorio: Foco, 15 min.
- Regla: el grado IP e IK sale de la ficha de la versión exacta.

### 23. X912 y X910
- Idea: X912 Linux antivandálico, versión estándar y con teclado físico; X910 de un botón, sin PIN, con detección de paquetes.
- Historia: X912 12 V 1 A por relé con PoE+ (https://knowledge.akuvox.com/docs/devices-supporting-12v-power-output).
- Laboratorio: Campo, 10 min.

### 24. R29
- 4 de 10 (TH55), con ficha propia leída.
- Idea: Android de 7", IP65 e IK06, cuatro versiones (S, C, C-L, C-T); C-L con LTE sin PoE.
- Historia: el R29C-L que no arranca por PoE (https://knowledge.akuvox.com/docs/power-supply-for-intercom-devices).
- Laboratorio: Foco, 15 min.

### 25. R28 y R25
- Idea: R28 de 4,3" sin táctil con borne de 12 V propio; R25A de un botón y R25K, que se consulta con el código del R20K; la tabla de métodos marca a la serie R25 sin PIN.
- Laboratorio: Rápido, 10 min.

### 26. Los R20
- Idea: R20A, R20K, R20K-L y R20B: Linux, IP65, sin pantalla, 802.3af, relé 30 V 2 A, tres versiones de hardware; MD06 y MD12 como módulos de nombres.
- Historia: la salida de 12 V del R20 que con PoE depende del volumen (https://knowledge.akuvox.com/docs/devices-supporting-12v-power-output).
- Laboratorio: Rápido, 10 min.

### 27. E18 y E16
- Idea: los de rostro en plástico: E18 táctil y E16 de 5", Linux, IP65, 802.3af, sin salida de 12 V; E16P con palma; PIN de sistema que cambió con el firmware.
- Laboratorio: Foco, 15 min.

### 28. E13S y E12
- Idea: un botón, plástico, 13,56 MHz, sin PIN; la guía marca Wi-Fi para el E12 y la tabla de métodos separa E12S y E12W; el E12 no tiene RS485 para el SR01.
- Laboratorio: Rápido, 10 min.

### 29. E21 y E20S
- Idea: intercomunicadores de emergencia: E21 de acero con cámara, sin PIN ni tarjeta, PoE 802.3af y relé de 3 A; E20S PoE sin fuente opcional.
- Laboratorio: Rápido, 10 min.

## Parte 6. Monitores interiores (lecciones 30 a 32)
Por qué esta parte: el monitor decide qué puede hacer el residente (abrir, ver cámaras, manejar relés) y es el equipo que más se cambia de lugar. Termina con un criterio para elegir Linux o Android y saber cuántos relés trae.

### 30. Monitores serie S
- 4 de 7 (TH60).
- Idea: S560 de auricular (sin relé ni RS485), S562 de 7" Linux con relé de 1 A, S563 de 8" Android, S567 de 10" Android y S565, que no figura en la guía de selección (ni tamaño ni sistema se afirman); RS485, relé y entrada de timbre en los cuatro de pantalla.
- Laboratorio: Foco, 15 min.

### 31. Monitores C e IT
- Idea: C313 de 7" Linux, C316 de 7" Android, C319 de 10" Android con dos relés de 24 V 1 A, IT88 de 10" en aluminio con dos relés.
- Laboratorio: Foco, 15 min.

### 32. Monitores serie X
- Idea: X933 de 7" Android con dos relés de 24 V 1 A y X937 de 15,6" con Android 14, PoE+ y dos RJ45 extra; AKClaw Panel como línea aparte, sin ficha leída.
- Laboratorio: Admin, 10 min.

## Parte 7. Control de acceso, ascensores y 2 hilos (lecciones 33 a 37)
Por qué esta parte: la misma obra que lleva porteros suele llevar puertas internas, ascensores y edificios viejos con dos hilos. Termina con cada pieza en su lugar: terminal en la puerta, controladora en el tablero, EC33 en la sala de máquinas.

### 33. Terminales A0x
- 8 de 11 (TH61).
- Idea: A01 tarjeta, A02 teclado, A03 Bluetooth, A05 rostro, A08 QR e IP65 IK09.
- Laboratorio: Campo, 15 min.

### 34. A15 y WR01
- Idea: A15 de rostro para marco de puerta; WR01 relé de borde con 2 relés y 2 entradas.
- Laboratorio: Foco, 15 min.

### 35. A094 y A095
- Idea: controladoras de 4 puertas; A094 en gabinete a 220 V con 4 salidas de 12 V; A095 PoE o 12 V 5 A con 8 salidas.
- Laboratorio: Admin, 15 min.

### 36. Ascensor EC33
- 1 de 11 en el cableado (TH62).
- Idea: 32 relés ampliables a 64; paralelo para ir directo al piso, serie para liberar botones; se habla por HTTP con el terminal.
- Historia: dos EC33, uno desbloquea y otro llama (https://knowledge.akuvox.com/docs/configure-lift-control-1).
- Laboratorio: Foco, 20 min.

### 37. Dos hilos
- 2 de 11 (TH63).
- Idea: R20A-2, R20K-2, E12S-2, S562W-2, C313W-2 con NS-2, NC-2 y NX-2; 48 V y nada de PoE en el portero.
- Laboratorio: Admin, 10 min.

## Parte 8. Teléfonos, accesorios, software y parque instalado (lecciones 38 a 41)
Por qué esta parte: completa el catálogo con lo que no es portero ni monitor y con lo que ya no se vende pero sigue en las paredes. Termina con la ficha completa del sistema y un criterio para el reemplazo.

### 38. Teléfonos y otros
- 2 de 7 (TH67).
- Idea: R49G de video Android, SP-R50P y HCP-R15P, cámara VC50B/VC50T, radares MR01 y MR03; solo el R49G tiene ficha leída.
- Laboratorio: Rápido, 10 min.

### 39. Accesorios y módulos
- 2 de 7 (TH66) y TH43, TH45.
- Idea: cubiertas de lluvia y soportes por modelo, SR01, MK485 y RSAC-C1-R8, lectores de escritorio, Bkey, KF, fuentes recomendadas.
- Laboratorio: Admin, 15 min.

### 40. Software y nube
- 1 de 7 (TH65), más lección 10.
- Idea: SmartPlus App y nube, My MobileKey, ACMS, ACMS Pro, SDMC e Installer Kit Tool.
- Laboratorio: Admin, 15 min.

### 42. Licencias Akuvox
- 5 de 8 fuentes sobre el cobro coinciden (TH25, notas e:N1 a e:N7): cobro por servicio con vencimiento; discrepan un distribuidor canadiense, un revendedor británico y un foro alemán de 2024.
- Idea: sin licencia en la LAN (SIP directo, IP, relés, RTSP, HTTP); se paga la nube por servicio (app maestra, PM App, familiares extra, Premium, cerraduras de terceros, Apple Wallet; en comercial por puerta) y el software de PC (ACMS Pro 1.0.0.4 prueba de 180 días, SDMC con licencia USB por encima de 500 equipos). Paga el distribuidor o el instalador habilitado; Auto Renew cada 30 días. Sin precios oficiales.
- Historia: el ejemplo de 120 unidades del generador de cotizaciones (https://knowledge.akuvox.com/docs/how-to-generate-project-quotations); ACMS Pro que deja afuera a todos a los 180 días (https://knowledge.akuvox.com/docs/akuvox-acms-pro-administrator-guide).
- División: renovación por servicio en la documentación oficial (https://knowledge.akuvox.com/docs/for-distributors) contra licencia única de por vida (https://pipl.systems/guides/akuvox-canada-distribution) y "con monitor no se paga" (https://firstfence.co.uk/akuvox-cloud-subscription). Cómo decidir: vale la cotización escrita del distribuidor de la región, con fecha y período.
- Laboratorio: Admin, 15 min. Leer cuenta y Connect Setting en el portero, armar la planilla de qué depende de la nube para un edificio y una casa, pasarla a un presupuesto de dos renglones y probar sin WAN.
- Regla: el equipo se cobra una vez, la nube se cotiza por servicio y por escrito, y la puerta abre igual sin licencia.
- Huecos: ningún precio oficial; ninguna página dice qué deja de andar en el equipo al vencer; no hay procedimiento publicado de traspaso entre instaladores; sin dato del licenciamiento de MySmart Local Server ni de ACMS.

### 41. Parque instalado
- 3 de 7 (TH64).
- Idea: E11, R27, R26, DB01, C315, C310, IT83, A092 y E20 siguen en la documentación sin estar en el menú; C317 no aparece en ninguna página leída.
- Historia: la pareja E11R y C315S del ejemplo de ComfortClick (https://www.comfortclick.com/Support/ExampleDetails/Akuvox).
- Laboratorio: Campo, 20 min.
- Regla: antes de cambiar un equipo viejo, leo su código de firmware y busco su par vigente.

## Divisiones (decisiones, no lecciones)
- DTMF por SIP INFO. Akuvox lo ofrece como confiable (https://knowledge.akuvox.com/docs/door-unlock-configuration-8); 3CX lo desaconseja (https://www.3cx.com/blog/voip-howto/dtmf-rfc2833/). Cómo decidir: si hay una central en el medio, RFC 2833 en todas las puntas; SIP INFO solo si un extremo no soporta otra cosa y se prueba con la central real.
- Nube contra aislamiento. Claroty y CISA piden no exponer (https://claroty.com/team82/research/akuvox-smart-intercom-vulnerabilities-leave-privacy-ajar); Yeastar documenta registro remoto con reenvío de puertos (https://help.yeastar.com/en/p-series-appliance-edition/integrations/akuvox/manually-register-akuvox-intercom-device-with-yeastar-p-series-pbx-system.html). Cómo decidir: tráfico saliente hacia una nube o una VPN sí; puertos entrantes reenviados al portero, no.
- Dos puertas por DTMF o por HTTP. Grandstream con el mismo código (https://documentation.grandstream.com/knowledge-base/gds3710-two-doors-control-configuration-guide/); FreePBX con comandos HTTP (https://community.freepbx.org/t/how-can-i-manage-double-doorphone-doorlock/97459). Cómo decidir: un portero con dos relés, DTMF; dos porteros distintos, HTTP con usuario propio y lista blanca.
- IP directa o central. La central suma desvíos, colas y apps (https://www.3cx.com/blog/voip-howto/door-phone/); la IP directa conserva la vista previa (https://community.freepbx.org/t/early-media-doorphone-video-preview/99698). Cómo decidir: si nadie fuera de la casa atiende el portero, IP directa.

- Alta seguridad encendida o apagada para el HTTP. Akuvox la deja encendida y recomienda /fcgi/OpenDoor (https://knowledge.akuvox.com/docs/trigger-door-actions-via-http-api-e18); un integrador la apaga para usar /fcgi/do con admin (https://forum.logicmachine.net/showthread.php?tid=6156). Cómo decidir: si el cliente HTTP acepta credenciales en la URL o digest, alta seguridad encendida; si no, se cambia el cliente o se pone un intermediario, no se apaga la seguridad.
- Credenciales en la URL. El fabricante las publica así (https://knowledge.akuvox.com/docs/trigger-door-actions-via-http-api-e18); pylocal-akuvox advierte que quedan en logs (https://pylocal-akuvox.readthedocs.io/en/latest/quickstart.html). Cómo decidir: usuario dedicado que solo abre, tráfico encerrado en la VLAN y, si el equipo lo soporta, HTTP API en Digest o Allowlist.
- Grado de protección del X915. IP65 en la guía de selección (https://www.akuvox.com/productSelectionGuide?cid=3), IP66 e IK10 en la ficha V2.0 (https://www.akuvox.com/productsDisp?pid=37). Cómo decidir: vale la ficha de la versión que se compra; con equipos viejos, la etiqueta.

## Huecos
- Credenciales, cerraduras y RTSP descansan en una o dos páginas (guía del E16 y Grandstream). Falta un caso de practicante con un NVR concreto.
- La alimentación de cerraduras (fuente separada, diodo en electroimanes) se enseña desde el principio general; la página oficial de cableado de Akuvox no entró por el límite de páginas por sitio.
- El formato nuevo de URL de apertura HTTP (/fcgi/OpenDoor) salía en la lección 8 de la guía del E16 leída pero no guardada en raw. Resuelto en la ampliación: la página oficial de apertura por HTTP ya está en raw y lo respalda (lección 13).
- No hay fuentes en español ni de foros de integradores de la región.
- Al cerrar la primera versión no se cubrían la serie A, los ascensores ni Home Assistant; la ampliación los suma (lecciones 18, 33 a 36). Control4 sigue sin cubrir.
- Relés por HTTP: no se encontró en páginas leídas una acción HTTP saliente de HikCentral ni de un NVR Hikvision; lo documentado es la cámara LPR Hikvision hablando con el portero. Grandstream UCM tampoco tiene acción HTTP documentada en las páginas leídas; la lección 18 lo dice y deriva al DTMF de las lecciones 5, 6 y 8 o a un Asterisk con CURL.
- El cuerpo JSON de /api/relay/trig no está en ninguna página leída (solo su existencia, en pylocal-akuvox); el curso no da un ejemplo de ese pedido.
- Catálogo: solo X915, R29, R49G, EC33, A08 y WR01 tienen ficha propia leída (límite de 10 páginas de akuvox.com). El resto sale de la guía de selección y de las tablas transversales de la Knowledge Base: no hay megapíxeles de cámara ni grado IK para esos modelos, y las lecciones no los inventan.
- La guía de selección de monitores trae las columnas de cámara y Wi-Fi desalineadas; se usan solo pantalla, carcasa y sistema operativo.
- No hay lista oficial de discontinuados en las páginas leídas. "Fuera de catálogo" quiere decir "en tablas de la Knowledge Base pero no en el menú de productos". El C317 no aparece en ninguna página leída y no se afirma nada de él.

## Entrega
41 carpetas class/NN-handle con script.txt (texto opcional "La charla", el audio quedó descartado), card.md y quiz.json, más class/course.json. Las lecciones 1 a 12 no se tocaron.

## Parte 9. Pantallas: monitor y portero (lecciones 43 y 44)
Por qué esta parte: el cliente juzga el sistema por lo que ve en la pantalla. Con los equipos ya elegidos y andando, falta dejar cada pantalla con los botones, el idioma y la imagen que corresponden a quien la usa. En la ruta lineal, la 43 va después de Dos hilos (cierre de Adentro: monitores y 2 hilos) y la 44 después de E18 y E16 (último de los porteros táctiles en La calle: series R y E). Notas: research/notes/f.md (f:N1 a f:N35).

### 43. Theme del monitor
- 10 de 10 páginas sobre pantallas de monitor (todas de la Knowledge Base de Akuvox) coinciden en el mecanismo; cambian los nombres por modelo; sin practicantes.
- Idea: pantalla de inicio en `Device > Display Setting > Theme` (Default o Call List: C319, S567, IT88, X933, S562) o en `Device > Key/Display > Home Page Mode` (Classic o Call List Simple: C313); los botones son el tipo de cada área (Arming, SOS, Unlock, Contacts...), con etiqueta e ícono de hasta 100x100; protector, fondo, logo de arranque, idioma y, en el S567, Theme Style y Festival Theme Auto-Switch.
- Por qué importa: el pedido "sacame el botón de alarma" se resuelve en dos minutos y se repite igual en todos los apartamentos.
- Historia: el fondo cambiado desde la nube por AutoP en un S562, que toma efecto al reiniciar (https://knowledge.akuvox.com/docs/configure-screensaver-on-indoor-monitors-using-autop-commands); la línea `Config.Settings.DISPLAYSTYLE.IdleStyle` que vale 4 o 5 en el S567 y 0 o 1 en el S562 (planillas AutoP oficiales, sin página en raw).
- Laboratorio: Foco, 20 min. Default y Call List, Arming cambiado por Unlock "Portón" con un Remote Relay HTTP de Botón del monitor, Settings Page Display, protector de 1280x800 con horario, pantalla en español, fondo por AutoP si hay SmartPlus.
- Regla: el botón que sobra no se esconde con el theme: se cambia el tipo del área, y lo que se cambia en un monitor queda anotado para todos.
- Fuentes: https://knowledge.akuvox.com/docs/screen-display-configuration-7, https://knowledge.akuvox.com/docs/screen-display-configuration-6, https://knowledge.akuvox.com/docs/screen-display-configuration-9, https://knowledge.akuvox.com/docs/screen-display-configuration-10, https://knowledge.akuvox.com/docs/screen-display-configuration-8, https://knowledge.akuvox.com/docs/screen-display-configuration-11, https://knowledge.akuvox.com/docs/screensaver-specifications, https://knowledge.akuvox.com/docs/configure-screensaver-on-indoor-monitors-using-autop-commands, https://knowledge.akuvox.com/docs/configure-temperature-display-on-indoor-monitors, https://knowledge.akuvox.com/docs/language-and-time-setting-15

### 44. Theme del portero
- 8 de 8 páginas (Knowledge Base de Akuvox) coinciden en elegir el theme en la web del equipo; difieren en la lista por fecha (R29 con 4 themes en la nota de junio y 5 con Parking Lot en su guía de septiembre de 2026); sin practicantes.
- Idea: tabla oficial de themes por modelo (Villa, Building, Office, Multi-factor Authentication, Alphanumeric, Speed Dial, QR Code, Directory, Customized Text, Gate Mode, Intercom, VMS, Default, Custom UI); ruta `Setting > Key/Display > Theme`, `Intercom > Key/Display > Theme` (X916) o `Device > LCD > Theme` (E18, E16); dentro del theme, página de inicio (íconos, directorio o teclado), nombres de tecla e idiomas en Building; protector y publicidad, fondo, logo.
- Por qué importa: la visita llama en dos o tres toques y el portero no queda en un theme que necesita la nube en una obra local.
- Historia: Gate Mode, que muestra edificios y apartamentos del proyecto de comunidad en SmartPlus y sin nube no tiene qué mostrar (https://knowledge.akuvox.com/docs/configure-theme-on-akuvox-door-phone).
- Laboratorio: Foco, 20 min. Villa y Building en un R29 o X915, página de inicio en directorio y en teclado, teclas en español, dos idiomas, protector de 800x1280 con Play Time, prueba de calle con alguien que no conoce el edificio.
- Regla: el theme se elige por quién llega a la puerta, y se prueba con alguien que no conoce el edificio.
- Fuentes: https://knowledge.akuvox.com/docs/configure-theme-on-akuvox-door-phone, https://knowledge.akuvox.com/docs/screen-display, https://knowledge.akuvox.com/docs/screen-display-configuration-1, https://knowledge.akuvox.com/docs/screen-display-configuration-3, https://knowledge.akuvox.com/docs/screen-display-configuration-4, https://knowledge.akuvox.com/docs/screensaver-specifications, https://knowledge.akuvox.com/docs/languages-supported-by-different-models, https://knowledge.akuvox.com/docs/language-and-time-setting-2

### División (pantallas)
- Lista de themes del R29: la nota de themes (https://knowledge.akuvox.com/docs/configure-theme-on-akuvox-door-phone) da Villa, Building, Office y Alphanumeric; la guía del R29 (https://knowledge.akuvox.com/docs/screen-display) suma Parking Lot. Cómo decidir: vale la lista que muestra la web del equipo con su firmware; los themes de nube solo si el portero está en un proyecto de SmartPlus.

### Huecos (pantallas)
- Ninguna página de practicante sobre themes de Akuvox: las dos lecciones descansan solo en el fabricante.
- No hay versión de firmware mínima publicada para cada theme (Parking Lot, Two Column Speed Dial del S535, Custom UI del E16) en las páginas leídas.
- Los comandos AutoP de theme (`IdleStyle`, `ThemeStyle`, `GENERAL.Theme`) salen de planillas .xlsx que el scraper no guarda; las tarjetas los dan como dato del fabricante sin url.
- No se encontró cómo elegir el theme del portero desde SmartPlus (solo Gate Mode y Parking Lot dependen de la nube); el theme del monitor tampoco tiene opción documentada en el portal, salvo AutoP.
- El S567 nombra un "Theme Style" que se aplica a todas las pantallas; los siete estilos (Default, Minimalist, Volumetric, Colorful, Dark, Natural, Luxury) salen de la planilla AutoP, no de la página.

## Parte 10. Configuración de porteros: botones y llamadas (lección 45)
Por qué esta parte: Nico pidió, dentro de porteros, la configuración de botones y todas las formas de llamada posibles. Con el theme elegido (lección 44), falta que cada botón llame a quien corresponde y que el portero haga lo esperado cuando nadie atiende o alguien rechaza. En la ruta lineal, la 45 va en el módulo nuevo "Configuración de porteros", después de Theme del portero (estructura-extra-modulos-config.json). Notas: research/notes/g.md (g:N1 a g:N25).

### 45. Configuración de botones
- 12 de 12 páginas de la Knowledge Base de Akuvox coinciden en el mecanismo (TH69, TH70, TH71); cambian el menú por familia y la redacción de End This Call Only. Practicante: hilo de FreePBX con dos terminales que suenan juntos a través de la central.
- Idea: el destino es una IP (`Intercom > Basic > Direct IP`; E12 en `Intercom > Call Feature > Direct IP`) o un número SIP por la cuenta; la tecla de Recepción (`Intercom > Basic > Key Setting` en E16 y E18), el Speed Dial (R29, X915, R20K) o el Manager Dial (E12, serie R20, E13) cargan el destino; Sequence Call (Call Timeout, When Refused Do Not Call Next o Call Next) contra Group Call (When Refused End This Call Only o End All Calls); en táctiles, grupo del directorio con Priority of Call; Dial Plan con prefijo y hasta 5 reemplazos; Call Feature con Auto Answer, Max Call Time, Max Dial Time y Hang Up After Open Door.
- Por qué importa: el reclamo "toqué y no sonó en la cocina" o "mi hijo rechazó y se cortó para todos" es un ajuste de When Refused, no una falla del equipo.
- Historia: el R29 con Time Out de 10 segundos que corta y pasa al siguiente (https://knowledge.akuvox.com/docs/call-setting-9); el R20B con números por pulsador y módulo de expansión (https://knowledge.akuvox.com/docs/calling-feature); la tecla de Recepción de un E16C V2.0 en obra con dos IP separadas por coma (captura de Nico, sin url), contra el ";" que documenta la guía del E18 (https://knowledge.akuvox.com/docs/call-settings-15).
- Laboratorio: Foco, 25 min. E16 y dos monitores por IP directa: Recepción con dos destinos, grupo en Groups Only, rechazo con End This Call Only y End All Calls, prioridad con Sequence Call de 20 s y Call Next o Do Not Call Next, Dial Plan con prefijo 100, tiempos de Call Feature, y el menú equivalente en E12, R20, R29 y X915.
- Regla: cada botón se prueba con un monitor que no atiende y otro que rechaza antes de irme de la obra.
- Fuentes: https://knowledge.akuvox.com/docs/call-settings-10, https://knowledge.akuvox.com/docs/configure-sequence-call, https://knowledge.akuvox.com/docs/configure-group-call, https://knowledge.akuvox.com/docs/contact-list-configuration-4, https://knowledge.akuvox.com/docs/contacts-configuration-13, https://knowledge.akuvox.com/docs/call-settings-7, https://knowledge.akuvox.com/docs/calling-feature, https://knowledge.akuvox.com/docs/call-settings-4, https://knowledge.akuvox.com/docs/call-setting-9, https://knowledge.akuvox.com/docs/call-settings-1, https://knowledge.akuvox.com/docs/call-settings-15, https://knowledge.akuvox.com/docs/intercom-call-configuration-10

### División (botones)
- Separador de varios números en la tecla de Recepción: la guía del E18 dice ";" (https://knowledge.akuvox.com/docs/call-settings-15); la captura de un E16C V2.0 en obra usa ","; la guía del E16 no lo dice (https://knowledge.akuvox.com/docs/call-settings-10). Cómo decidir: el separador que el firmware de ese equipo acepta al guardar y que hace sonar a los dos destinos en la prueba.

### Huecos (botones)
- Ninguna página dice si los números de la tecla de Recepción suenan juntos o en orden, ni si el When Refused de Group Call se aplica a esa tecla: el laboratorio lo hace anotar.
- No hay página que diga qué hace un táctil con un grupo sin prioridades cuando Sequence Call está configurado; lo leído es que el grupo con prioridades se llama en orden y el grupo de Group Call suena junto.
- El hilo de 3CX sobre un monitor Akuvox en un grupo de timbrado (la vista previa hace que la central dé la llamada por atendida) no entró en raw por ser una página delgada para el scraper; no se cita.
- Rangos válidos de Call Timeout, Max Call Time y Max Dial Time no figuran en las páginas leídas; la tarjeta no da valores salvo el 20 de la captura.
