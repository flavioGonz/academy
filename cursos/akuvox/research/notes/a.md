# Notes: batch a
Pages read: 9. With notes: 9. Skipped: 0. (Akuvox Knowledge Base, Akuvox ticket portal, Akuvox SmartPlus en Google Play.)

## T01 Familias y modelos
- a:N1. Akuvox numera el firmware en cuatro partes A.B.C.D: A es el modelo (29 es R29, 915 es X915, 216 es E16 V2, 416 es E16 V3, 12 es E12, 316 es C316, 115 es C315), B el OEM (30 con logo Akuvox), C la rama (10 o más indica la rama con modo de alta seguridad) y D la versión dentro de la rama.
  - Source: https://knowledge.akuvox.com/docs/upgrade-devices  Quote: "We can divide the firmware version number into four parts: A, B, C, and D."
  - Kind: definition
  - Level: foundation
  - Also: T04
  - Bias: none (documentación del fabricante)
- a:N2. Varios modelos tienen más de una versión de hardware (E12, R28, X915 y C313 tienen dos; R20, E16 y E21 tienen tres) y cada una lleva un firmware distinto. Se ve en la etiqueta trasera o en Status > Basic > Product Information. Excepción: R20A con etiqueta V3.0 es hardware 2 y V5.0 es hardware 3.
  - Source: https://knowledge.akuvox.com/docs/upgrade-devices  Quote: "Different versions require different firmware files."
  - Kind: mistake
  - Level: foundation
  - Also: T04
  - Bias: none
- a:N3. La guía oficial de usuarios y credenciales toma como ejemplo modelos concretos: E12 y E16 solo leen tarjetas IC de 13,56 MHz; los modelos sin teclado numérico no aceptan PIN privado. Conviene confirmar el modelo antes de prometer un método de apertura.
  - Source: https://knowledge.akuvox.com/docs/door-unlock-configuration-8  Quote: "RF cards operating at 13.56 MHz frequency are compatible with the device"
  - Kind: rule of thumb
  - Level: foundation
  - Also: T09

## T02 Primer acceso
- a:N4. Cómo sacar la IP depende del modelo: en porteros sin teclado (R20A, R25A, E11, E12, E13, X910) se mantiene apretado el botón de llamada unos cinco segundos y el equipo la dice en voz alta; en R20K/R25K se marca asterisco 3258 asterisco; en E16/E18 se mantiene apretada la pantalla cinco segundos y se entra con el PIN de sistema; en R29/X915 se marca 9999, luego 3888 y System Info.
  - Source: https://knowledge.akuvox.com/docs/before-entering-device-web-interface  Quote: "Hold the Call button for about five seconds."
  - Kind: technique
  - Level: foundation
- a:N5. El PIN de sistema por defecto del E16 cambió con el firmware: hasta 216.30.10.121 es "admin"; en versiones posteriores es "Admin321". Lo mismo en E18 con su versión de corte.
  - Source: https://knowledge.akuvox.com/docs/before-entering-device-web-interface  Quote: "Firmware version 216.30.10.121 or earlier: admin All other versions: Admin321."
  - Kind: mistake
  - Level: foundation
- a:N6. En los monitores la IP está en pantalla: C315 More > System Info > Network; C316, C319, S567, S563, S562, X933 en Settings > System Info > Network.
  - Source: https://knowledge.akuvox.com/docs/before-entering-device-web-interface
  - Kind: technique
  - Level: foundation
- a:N7. La herramienta IP Scanner de Akuvox busca equipos en la red, permite reiniciar, resetear y cambiar red; pide Windows 7 de 64 bits o superior y apagar el firewall de la PC. Usuario y contraseña web por defecto: admin y admin.
  - Source: https://knowledge.akuvox.com/docs/before-entering-device-web-interface  Quote: "The defaults are both admin."
  - Kind: technique
  - Level: foundation
  - Also: T14

## T04 Firmware
- a:N8. Firmware oficial: Knowledge Base, sección Firmware & Tool, descarga desde Google Drive; .zip es para equipos Android y .rom para equipos Linux. Para versiones especiales o compatibles con terceros se pide a soporte.
  - Source: https://knowledge.akuvox.com/docs/upgrade-devices  Quote: ".zip is for the Android system, and .rom is for the Linux system."
  - Kind: rule of thumb
  - Level: foundation
- a:N9. Por web: System > Basic, Select File, Upgrade; no cerrar ni refrescar la ventana durante la actualización; luego verificar la versión. Por SmartPlus: el equipo tiene que estar en línea, vinculado a la nube y con red estable.
  - Source: https://knowledge.akuvox.com/docs/upgrade-devices  Quote: "When upgrading, do not close or refresh the upgrading window."
  - Kind: technique
  - Level: foundation
- a:N10. En el número de firmware, una rama (parte C) de 10 o más indica la rama con modo de alta seguridad, que cifra la comunicación, los comandos de apertura y el almacenamiento de contraseñas. Conviene saber en qué rama está el equipo antes de usar herramientas o comandos viejos.
  - Source: https://knowledge.akuvox.com/docs/upgrade-devices  Quote: "If the number is 10 or larger, the device is in the firmware version with high security mode"
  - Kind: definition
  - Level: core
  - Also: T14
- a:N11. Antes de abrir un ticket, el soporte de Akuvox pide actualizar al último firmware.
  - Source: https://ticket.akuvox.com/support/solutions/articles/48001200817-read-first-how-to-provide-information-to-effectively-resolve-a-technical-issue-on-akuvox-intercom-  Quote: "It is highly recommended to upgrade the latest firmware when you find some issues"
  - Kind: rule of thumb
  - Level: foundation
  - Also: T15

## T05 Llamadas IP directas
- a:N12. Una llamada IP directa es entre dos equipos por su IP, sin servidor ni central, y funciona cuando están en la misma red. Se configura en Intercom > Basic > Direct IP; puerto por defecto 5060, y si se cambia tiene que coincidir en el otro equipo.
  - Source: https://knowledge.akuvox.com/docs/intercom-call-configuration-8  Quote: "IP calls work when the devices are on the same network."
  - Kind: definition
  - Level: foundation

## T06 Cuentas SIP
- a:N13. Los equipos Akuvox admiten dos cuentas SIP en dos servidores distintos. La cuenta 1 es la principal y la que usa SmartPlus si está activado; si la 1 no registra, pasa a la 2. Campos: Register Name y Username iguales al usuario de la central, Password, Server Address, puerto y período de registro. Ruta: Account > Basic.
  - Source: https://knowledge.akuvox.com/docs/intercom-call-configuration-8  Quote: "Akuvox intercom devices support the configuration of two SIP accounts"
  - Kind: technique
  - Level: core
- a:N14. Transporte SIP: UDP por defecto, TCP, TLS (requiere subir certificados) o DNS-SRV. El rango de puertos RTP propio se fija en Network > Advanced > Local RTP.
  - Source: https://knowledge.akuvox.com/docs/intercom-call-configuration-8
  - Kind: technique
  - Level: core
  - Also: T03, T14
- a:N15. "Prevent SIP Hacking" (Account > Advanced > Call) hace que el equipo solo acepte llamadas de contactos en la lista blanca.
  - Source: https://knowledge.akuvox.com/docs/intercom-call-configuration-8  Quote: "only receive calls from contacts in the whitelist"
  - Kind: technique
  - Level: core
  - Also: T14

## T07 DTMF
- a:N16. Tres formas de mandar DTMF en SIP: inband (dentro del audio, simple pero se degrada con codecs comprimidos como G.729), RFC 2833 (eventos en paquetes RTP, fuera de banda, más confiable) y SIP INFO (mensajes de señalización, confiable pero menos soportado que RFC 2833). Akuvox ofrece también combinaciones Info+RFC2833 e Info+Inband+RFC2833.
  - Source: https://knowledge.akuvox.com/docs/how-to-open-the-door-via-dtmf-on-the-indoor-monitor  Quote: "not as widely supported as the RFC 2833 method"
  - Kind: definition
  - Level: core
- a:N17. Receta oficial: en el portero, Account > Advanced > DTMF elegir el tipo; Access Control > Relay elegir relé A/B/C, cantidad de dígitos y código (ejemplo 010). En el monitor, el mismo tipo en Account > Advanced > DTMF y el mismo código en Device > Relay > Relay Setting > Remote Relay. Botón de apertura en pantalla: Device > Relay > SoftKey In Talking Page, tipo Remote Relay DTMF.
  - Source: https://knowledge.akuvox.com/docs/how-to-open-the-door-via-dtmf-on-the-indoor-monitor  Quote: "Select the DTMF type as configured on the door phone."
  - Kind: technique
  - Level: core
  - Also: T10
- a:N18. Para abrir por DTMF, los dos equipos tienen que usar el mismo modo y el mismo código o la apertura falla. Payload por defecto acordado entre emisor y receptor (rango 96 a 127).
  - Source: https://knowledge.akuvox.com/docs/door-unlock-configuration-8  Quote: "must use the same mode and code. Otherwise, the DTMF unlock may fail."
  - Kind: rule of thumb
  - Level: core
- a:N19. Lista blanca DTMF (Access Control > Relay > Open Relay Via DTMF): None, Only Contacts List o All Numbers. Limitar a contactos evita que cualquier número que llame pueda abrir marcando el código.
  - Source: https://knowledge.akuvox.com/docs/door-unlock-configuration-8
  - Kind: technique
  - Level: core
  - Also: T14

## T08 Relés, cerraduras, botón de salida
- a:N20. El relé del portero se dispara por los métodos que se habiliten (PIN, tarjeta, rostro, DTMF, HTTP, botón de salida) y cada usuario lleva asignado qué relé abre. El tiempo de apertura y el modo del relé se ajustan en Access Control > Relay.
  - Source: https://knowledge.akuvox.com/docs/door-unlock-configuration-8
  - Kind: definition
  - Level: foundation

- a:N21. Botón de salida: se conecta a una entrada y se configura en Access Control > Input (Enabled, nivel de disparo, relé a ejecutar). La misma pantalla ofrece alarma de puerta abierta demasiado tiempo (Door Opened Timeout) y alarma de apertura forzada (Break-in Intrusion).
  - Source: https://knowledge.akuvox.com/docs/door-unlock-configuration-8  Quote: "Activate an alarm when the door is forcibly or illegally opened."
  - Kind: technique
  - Level: core
- a:N22. Apertura por HTTP: Access Control > Relay > Open Relay Via HTTP, con un usuario y una contraseña propios para las URL de apertura, distintos de los de la web. Sirve para que una central, un sistema de alarmas o un script abra sin estar en llamada.
  - Source: https://knowledge.akuvox.com/docs/door-unlock-configuration-8  Quote: "Set a username for authentication in HTTP command URLs."
  - Kind: technique
  - Level: core
  - Also: T10

## T09 Credenciales y horarios
- a:N23. PIN público (todos los vecinos): 4 a 8 dígitos, por defecto 33333333. PIN privado: uno por usuario, 2 a 8 caracteres. Modo APT#+Key solo con SmartPlus.
  - Source: https://knowledge.akuvox.com/docs/door-unlock-configuration-8  Quote: "The default is 33333333."
  - Kind: mistake
  - Level: foundation
  - Also: T14
- a:N24. Usuarios en Directory > User: hasta 20.000 usuarios en el E16, hasta 5 tarjetas por usuario, tarjetas de 13,56 MHz; cada usuario lleva relé, horario (Always, Never o uno propio), piso, web relay. Alta masiva exportando el .tgz, editando el .csv y reimportando.
  - Source: https://knowledge.akuvox.com/docs/door-unlock-configuration-8  Quote: "The device allows to add 20,000 users."
  - Kind: technique
  - Level: core
- a:N25. Reconocimiento facial: foto jpg/png/bmp hasta 2 MB; nivel de coincidencia y nivel antisuplantación ("Close" desactiva y deja pasar una foto); distancia de detección 1 a 3 metros; rechazo con barbijo opcional.
  - Source: https://knowledge.akuvox.com/docs/door-unlock-configuration-8  Quote: "Facial verification can be passed using non-living substitutes"
  - Kind: mistake
  - Level: core
  - Also: T14
- a:N26. Autenticación doble con orden fijo: Face+PIN, Face+RF Card, RF Card+PIN; Entry Restriction fija un intervalo mínimo entre aperturas del mismo usuario.
  - Source: https://knowledge.akuvox.com/docs/door-unlock-configuration-8
  - Kind: technique
  - Level: advanced
- a:N27. Tarjetas Mifare cifradas: el equipo lee sector y bloque con clave, no el UID; DESFire con App ID, File ID y AES/DES. Leer el UID solo es copiable; leer un sector cifrado no.
  - Source: https://knowledge.akuvox.com/docs/door-unlock-configuration-8  Quote: "it reads the data in the cards' designated sectors and blocks, not the UID"
  - Kind: technique
  - Level: advanced
  - Also: T14

## T11 SmartPlus y app
- a:N28. La app SmartPlus (100 mil descargas o más, 3,6 estrellas en Google Play, según la tienda) permite ver y hablar con visitas, abrir y dar llaves temporales. Reseñas visibles se quejan de pedidos de login, llamadas que fallan al azar y notificaciones que llegan tarde; Akuvox responde pidiendo actualizar la app y el sistema operativo.
  - Source: https://play.google.com/store/apps/details?id=com.akuvox.mobile.smartplus&hl=en&gl=US&pli=1  Quote: "Sometimes I can't make calls, call someone, receive calls"
  - Kind: story
  - Level: core
  - Bias: reseñas de usuarios, sin verificar
- a:N29. Con SmartPlus, la cuenta SIP 1 del equipo queda tomada por la nube y muestra el número SIP de SmartPlus; la cuenta 2 queda libre para una central local.
  - Source: https://knowledge.akuvox.com/docs/intercom-call-configuration-8  Quote: "it will be utilized when the Akuvox SmartPlus cloud service is activated"
  - Kind: rule of thumb
  - Level: core
  - Also: T06
- a:N30. Bluetooth con SmartPlus: apertura con la app en el bolsillo o en modo manos libres al acercarse; umbral RSSI e intervalo configurables. Requiere el equipo conectado a SmartPlus.
  - Source: https://knowledge.akuvox.com/docs/door-unlock-configuration-8
  - Kind: technique
  - Level: advanced

## T12 Video hacia NVR/VMS
- a:N31. RTSP del portero: rtsp://IP/live/ch00_0 (primer stream) y rtsp://IP/live/ch00_1 (segundo). Por defecto H.264, 25 fps, 2048 kbps el primero y 512 kbps el segundo. Autenticación Digest configurable en Surveillance > RTSP > RTSP Basic.
  - Source: https://knowledge.akuvox.com/docs/monitor-and-image-13  Quote: "rtsp://Device's IP/live/ch00_0"
  - Kind: technique
  - Level: core
- a:N32. ONVIF: Surveillance > ONVIF, Discoverable, usuario y contraseña admin por defecto; URL http://IP:80/onvif/device_service. Así lo agrega un NVR.
  - Source: https://knowledge.akuvox.com/docs/monitor-and-image-13  Quote: "It is admin by default."
  - Kind: technique
  - Level: core
  - Also: T14
- a:N33. MJPEG: http://IP:8080/video.cgi para video y /picture.jpg para captura; conviene activar MJPEG Authorization para que no sea abierto.
  - Source: https://knowledge.akuvox.com/docs/monitor-and-image-13
  - Kind: technique
  - Level: core
  - Also: T14

## T14 Seguridad
- a:N34. La contraseña web de fábrica es admin/admin en toda la familia, publicada en la documentación pública.
  - Source: https://knowledge.akuvox.com/docs/before-entering-device-web-interface
  - Kind: mistake
  - Level: foundation

## T15 Soporte
- a:N35. Qué pide soporte de Akuvox: descripción reproducible, topología de red, diagrama eléctrico si es de relé, versión de firmware (Status > Product Information), archivo de configuración exportado, log del sistema con nivel 7 reproduciendo la falla, y captura PCAP si es de red o llamadas (limitada a 1 MB, arrancarla justo antes de reproducir).
  - Source: https://ticket.akuvox.com/support/solutions/articles/48001200817-read-first-how-to-provide-information-to-effectively-resolve-a-technical-issue-on-akuvox-intercom-  Quote: "Adjust the log level as 7 then reproduce your issue."
  - Kind: template
  - Level: core
- a:N36. Reseteo de contraseña web en porteros de un botón (R20A, R20B, R20K, R26, E11, E12): por SmartPlus con un parámetro de autoprovisión, por PC Manager en la misma LAN, o exportando la llave del equipo desde la web y mandándola a soporte, que devuelve un unlock.bin.
  - Source: https://ticket.akuvox.com/support/solutions/articles/48001156051-how-to-reset-the-web-password-for-single-button-series-door-phone-  Quote: "we will decrypt it and send you the unlock.bin file"
  - Kind: technique
  - Level: core
  - Also: T14

## Disagreements seen
- DTMF SIP INFO: Akuvox lo presenta como confiable y separado del audio (https://knowledge.akuvox.com/docs/door-unlock-configuration-8); 3CX lo desaconseja porque no viaja sincronizado con el audio y muchos servicios no lo soportan (https://www.3cx.com/blog/voip-howto/dtmf-rfc2833/).
- Contraseña por defecto: la documentación oficial publica admin/admin como paso normal (https://knowledge.akuvox.com/docs/before-entering-device-web-interface); Claroty la señala como debilidad justamente por estar publicada (https://claroty.com/team82/research/akuvox-smart-intercom-vulnerabilities-leave-privacy-ajar).
- Nube SmartPlus: el fabricante la presenta como la forma moderna de gestionar (https://play.google.com/store/apps/details?id=com.akuvox.mobile.smartplus&hl=en&gl=US&pli=1), Claroty recomienda no exponer el equipo a internet aunque se pierda la app.

## Best stories
- El PIN de sistema del E16 cambió de "admin" a "Admin321" según firmware: el técnico que prueba el viejo se queda afuera. https://knowledge.akuvox.com/docs/before-entering-device-web-interface
- Soporte pide la PCAP arrancada justo antes de reproducir porque solo guarda 1 MB. https://ticket.akuvox.com/support/solutions/articles/48001200817-read-first-how-to-provide-information-to-effectively-resolve-a-technical-issue-on-akuvox-intercom-
- Reseña de SmartPlus: ve a la persona en pantalla pero no puede atender por un error al azar. https://play.google.com/store/apps/details?id=com.akuvox.mobile.smartplus&hl=en&gl=US&pli=1
