# Mapa del tema: Porteros IP Akuvox (nivel inicial a intermedio, técnicos instaladores)

Cómo se enseña: Akuvox organiza su formación por la Knowledge Base (knowledge.akuvox.com), con guías de administrador por modelo (E16, E12, R20, C316, C319...) divididas en capítulos fijos: acceso al equipo, red, llamadas, relé, apertura de puerta, monitoreo, seguridad, firmware, backup. Los fabricantes de centrales (Yeastar, Grandstream, 3CX, FreePBX/Asterisk) enseñan la integración como "registrar el portero como una extensión más" y abrir por DTMF. Los investigadores de seguridad (Claroty Team82, CISA) enseñan el tema desde la exposición a internet y las credenciales por defecto. Este mapa sigue ese orden: equipo, red, llamada, puerta, credenciales, integración, nube, video, seguridad, soporte.

- T01 Familias y modelos: porteros de calle (series E, R, X, S) y monitores interiores (C, S, X, IT), versiones de hardware.
- T02 Primer acceso: encontrar la IP (pantalla, anuncio por voz, IP Scanner, DHCP), credenciales por defecto, entrar a la web.
- T03 Red y puertos: DHCP o IP fija, puerto SIP 5060, rango RTP, descubrimiento, VLAN y subredes.
- T04 Firmware: leer el número de versión, versión de hardware, dónde bajar, cómo actualizar, modo de alta seguridad.
- T05 Llamadas IP directas: portero a monitor sin servidor, misma red, puerto, limitaciones.
- T06 Cuentas SIP en una central: registrar el portero y el monitor en UCM, Asterisk/FreePBX, Yeastar o 3CX; errores típicos de registro.
- T07 DTMF para abrir: inband, RFC 2833, SIP INFO; el mismo tipo y el mismo código en ambos extremos; lista blanca DTMF.
- T08 Relés, cerraduras y botón de salida: NO/NC, fail-safe y fail-secure, alimentación separada, entradas, alarma de puerta abierta.
- T09 Credenciales y horarios: PIN público y privado, tarjetas RF/Mifare, rostro, QR, autenticación doble, horarios por usuario.
- T10 Varios porteros y varias puertas: abrir dos puertas desde un monitor o un teléfono, relé remoto, web relay, comandos HTTP.
- T11 SmartPlus y app: nube de Akuvox, alta de equipos, app del residente, límites y quejas.
- T12 Video hacia NVR/VMS: RTSP del portero, ONVIF, MJPEG, credenciales del stream, monitor viendo cámaras.
- T13 Video y audio a través de la central: H.264, early media y vista previa, codecs, NAT.
- T14 Seguridad: contraseña por defecto, exposición a internet, vulnerabilidades publicadas (E11), red separada, API HTTP, SRTP y TLS.
- T15 Soporte y troubleshooting: logs, captura PCAP, exportar configuración, reseteo de contraseña, qué mandar al fabricante.

## Ampliación (octubre de 2026): relés por HTTP y catálogo por tipo de dispositivo

Cómo se enseña: la Knowledge Base de Akuvox trata la apertura por HTTP, la HTTP API, el Action URL, el Web Relay, el relé de seguridad SR01 y los relés externos del monitor como artículos sueltos por función, y el catálogo como tablas transversales (alimentación, carga de relé, métodos de acceso, salidas de 12 V, interfaces de monitores) más la página de productos y la guía de selección de akuvox.com. Los integradores (LogicMachine, ComfortClick, la librería pylocal-akuvox) y las plataformas que mandan el pedido (Home Assistant, MikroTik, Asterisk, cámaras LPR) enseñan el lado cliente. El catálogo se arma por tipo de equipo, igual que el menú de productos del fabricante.

- T16 API HTTP de apertura: Open Relay via HTTP, formatos de URL viejo (/fcgi/do) y nuevo (/fcgi/OpenDoor), modo de alta seguridad, DoorNum y acciones.
- T17 Autenticación y seguridad del HTTP: HTTP API (None, Allowlist, Basic, Digest), usuario dedicado, clave en la URL, HTTPS, VLAN, nada expuesto.
- T18 Relés remotos y externos: botones del monitor por HTTP, Web Relay de terceros, SR01, MK485 y RSAC-C1-R8, WR01, tiempos de disparo y retención.
- T19 HTTP saliente ante eventos: Action URL, variables, eventos por modelo.
- T20 Clientes HTTP: navegador y curl, Home Assistant, MikroTik /tool fetch, Asterisk CURL, cámaras LPR, plataformas domóticas.
- T21 Catálogo de porteros de calle: series S, X, R, E y equipos de emergencia, datos clave y acceso al equipo.
- T22 Catálogo de monitores interiores: series S, C, IT y X, Linux o Android, interfaces y relé.
- T23 Control de acceso, ascensores y 2 hilos: serie A, WR01, controladoras A094 y A095, EC33, sistema de 2 hilos.
- T24 Teléfonos, accesorios, software y parque instalado: R49G, teléfonos IP, accesorios y módulos, software de PC y apps, modelos que salieron del catálogo.
