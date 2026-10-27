# Notes: batch c
Pages read: 15. With notes: 15. Skipped: 0. (Relés por HTTP: 8 artículos de la Knowledge Base de Akuvox, la página del WR01 en akuvox.com, la librería pylocal-akuvox, un hilo del foro LogicMachine, el ejemplo de ComfortClick, Home Assistant, MikroTik y Asterisk.)

## T16 API HTTP de apertura
- c:N1. Apertura por HTTP en el portero: menú Intercom > Relay > Open Relay via HTTP (ejemplo R29), tildar Enabled y poner usuario y clave propios; se pueden dejar en blanco para no autenticar. Akuvox dice que todos sus equipos de intercom lo soportan.
  - Source: https://knowledge.akuvox.com/docs/open-door-via-http-command  Quote: "All Akuvox intercom devices support this feature."
  - Kind: technique
  - Level: core
- c:N2. Session Check queda desactivado: Akuvox advierte que activarlo puede hacer fallar la apertura.
  - Source: https://knowledge.akuvox.com/docs/open-door-via-http-command  Quote: "Enabling it may lead to door-opening failure."
  - Kind: mistake
  - Level: core
- c:N3. Formato viejo (firmware sin alta seguridad): http://{IP}/fcgi/do?action=OpenDoor&UserName={usuario}&Password={clave}&DoorNum=1. Con alta seguridad activa solo valen los nuevos: http://{usuario}:{clave}@{IP}/fcgi/OpenDoor?action=OpenDoor&DoorNum=1 o, sin credenciales configuradas, http://{IP}/fcgi/OpenDoor?action=OpenDoor&DoorNum=1. Con alta seguridad apagada valen los tres.
  - Source: https://knowledge.akuvox.com/docs/open-door-via-http-command  Quote: "the device only supports the following two formats"
  - Kind: template
  - Level: core
- c:N4. Cómo saber si hay alta seguridad: Status > Basic > Product Information, si el tercer bloque del firmware es 10 o más el equipo tiene la rama de alta seguridad; el interruptor está en Security > Basic > High Security Mode (en el E18, System > Security > High Security Mode, encendido por defecto).
  - Source: https://knowledge.akuvox.com/docs/open-door-via-http-command  Quote: "third section of the version number is or bigger than 10"
  - Kind: test
  - Level: core
  - Also: T17
- c:N5. DoorNum elige el relé: 1 es el relé A, 2 el relé B; para el relé de seguridad SR01, DoorNum=SA o SB.
  - Source: https://knowledge.akuvox.com/docs/open-door-via-http-command  Quote: "Relay A: DoorNum = 1"
  - Kind: definition
  - Level: core
  - Also: T18
- c:N6. En E18 (18.30.11.27 o más) y R20V5 (320.30.12.28 o más) el mismo endpoint acepta más acciones: OpenDoor, CloseDoor, OpenDoorForever (dejar abierta), DoorStatus (consultar estado) y RefuseOpenDoorWrongCardID. Menú en E18: Access Control > Relay > Open Relay via HTTP. Recomienda clave única y fuerte, distinta de admin.
  - Source: https://knowledge.akuvox.com/docs/trigger-door-actions-via-http-api-e18  Quote: "Avoid using the default admin credentials."
  - Kind: technique
  - Level: advanced
- c:N7. El mismo artículo del E18 llama "recomendado" al formato nuevo y muestra que con el interruptor de alta seguridad apagado conviven el viejo y el nuevo.
  - Source: https://knowledge.akuvox.com/docs/trigger-door-actions-via-http-api-e18  Quote: "New URL Format(Recommended)"
  - Kind: rule of thumb
  - Level: core

## T17 Autenticación y seguridad del HTTP
- c:N8. HTTP API (Setting > HTTP API, ejemplo R29, todos los porteros): modos de autorización None (solo pruebas o demo), Allowlist (solo IPs listadas, para LAN), Basic (usuario y clave en Base64, viaja en claro), Digest (protege la credencial con MD5) y Normal (reservado a desarrollo interno de Akuvox).
  - Source: https://knowledge.akuvox.com/docs/configure-http-api  Quote: "Data is transmitted in clear text."
  - Kind: definition
  - Level: core
- c:N9. La librería pylocal-akuvox, pensada para Home Assistant, distingue dos caminos: los porteros con API JSON reciben /api/relay/trig con la autenticación de la HTTP API (None, AllowList, Basic o Digest); los equipos clase IT83 usan en cambio Open Relay Via HTTP con sus propias credenciales.
  - Source: https://pylocal-akuvox.readthedocs.io/en/latest/quickstart.html  Quote: "sends /api/relay/trig with the connection's AuthConfig"
  - Kind: technique
  - Level: advanced
  - Also: T16, T20
  - Bias: librería de código abierto de un tercero, no oficial
- c:N10. La misma librería advierte que el endpoint OpenDoor lleva la clave en la query de la URL, así que puede quedar en logs de proxies o del equipo; interpreta 0 como éxito y -1 como falla de credencial en firmwares que devuelven ese marcador.
  - Source: https://pylocal-akuvox.readthedocs.io/en/latest/quickstart.html  Quote: "it can appear in proxy or device access logs"
  - Kind: mistake
  - Level: advanced
- c:N11. HTTPS con equipos viejos: según pylocal-akuvox, algunos equipos como el monitor S562 traen parámetros Diffie-Hellman de 1024 bits que OpenSSL rechaza con "dh key too small"; la librería solo relaja la seguridad si se desactiva la verificación, y lo limita a LAN de confianza.
  - Source: https://pylocal-akuvox.readthedocs.io/en/latest/quickstart.html  Quote: "intended for trusted LAN use only"
  - Kind: mistake
  - Level: advanced
- c:N12. Un integrador en el foro de LogicMachine abre Akuvox con la URL vieja y credenciales de admin desde un script Lua, y aconseja apagar el modo de alta seguridad para que funcione. Es la práctica que el fabricante desaconseja.
  - Source: https://forum.logicmachine.net/showthread.php?tid=6156  Quote: "you need to disable it"
  - Kind: story
  - Level: core
  - Bias: foro de un fabricante de controladores domóticos

## T18 Relés remotos y externos
- c:N13. En el monitor, Phone > Relay > Remote Relay By HTTP or HTTPS: se carga la IP o el número SIP del portero, el formato de URL según alta seguridad y las credenciales. Después, en Key Setting, se crean teclas del tipo Remote Relay By HTTP or HTTPS en la pantalla de llamada, de monitoreo y de vista previa. Ejemplo oficial con R29 y C313.
  - Source: https://knowledge.akuvox.com/docs/open-door-via-http-command  Quote: "Softkey In Monitor Page"
  - Kind: technique
  - Level: core
- c:N14. Web Relay en el portero (Access Control > Web Relay): relé de terceros con servidor web, tipo Only Web Relay o Both (el relé local tiene prioridad), comando de ejemplo state.xml?relayState=2; dejando la IP en blanco se cargan URLs completas, hasta 50 comandos. Se dispara por DTMF (Web Relay Key igual al código DTMF), tarjeta (Action ID por usuario) o nube.
  - Source: https://knowledge.akuvox.com/docs/configure-web-relay-on-door-phone-web-interface  Quote: "You can configure up to 50 commands."
  - Kind: technique
  - Level: advanced
- c:N15. Solo los porteros Android (S539, S538, X916, X915V2 y R29) disparan el Web Relay desde la app SmartPlus, según Akuvox.
  - Source: https://knowledge.akuvox.com/docs/configure-web-relay-on-door-phone-web-interface  Quote: "ONLY Android door phones"
  - Kind: rule of thumb
  - Level: advanced
- c:N16. SR01 relé de seguridad: va del lado de adentro y maneja la cerradura, así que romper el portero no abre la puerta. Se conecta por la salida de 12 V del portero (Security Relay A) o por RS485 (Security Relay B, Device > RS485 en "Others"). Trigger Delay y Hold Delay configurables; el E18 no tiene Hold Delay. Lista de modelos y firmwares mínimos.
  - Source: https://knowledge.akuvox.com/docs/how-to-configure-sr01-security-relay-on-akuvox-door-phones  Quote: "even if the door phone is destroyed, the door cannot be opened"
  - Kind: technique
  - Level: core
  - Also: T23
- c:N17. El E12 se conecta al SR01 de una forma especial porque no tiene RS485, y Akuvox no recomienda esa conexión por seguridad.
  - Source: https://knowledge.akuvox.com/docs/how-to-configure-sr01-security-relay-on-akuvox-door-phones  Quote: "It is NOT recommended to use such a connection due to security."
  - Kind: mistake
  - Level: advanced
- c:N18. Relés externos del monitor: MK485 (8 salidas, por RS485; C y B normal abierto, C y A normal cerrado) o RSAC-C1-R8 (8 relés, 8 salidas, 8 entradas, hasta 3 por monitor, dirección por DIP). Menú Device > External Relay, Hold Delay, "Never" deja activado. Firmwares mínimos por modelo (S567, S562, S563, S565, X933, X937, C316, C319, IT88).
  - Source: https://knowledge.akuvox.com/docs/configure-external-relays-connected-to-indoor-monitors  Quote: "It has 8 relay output ports"
  - Kind: technique
  - Level: advanced
  - Also: T22, T24
- c:N19. Para el RSAC-C1-R8, sin el DIP 1 encendido el monitor no lo detecta.
  - Source: https://knowledge.akuvox.com/docs/configure-external-relays-connected-to-indoor-monitors  Quote: "Otherwise, the indoor monitor will not detect the device."
  - Kind: mistake
  - Level: advanced
- c:N20. WR01 es un controlador de relé web de borde: 2 relés y 2 entradas, 20.000 usuarios y 100.000 registros, alimentación AC o DC de 12 a 24 V o PoE, salida de 12 V hasta 0,5 A, BLE, montaje en pared o riel DIN; WR01-L suma LTE. Se controla por web y API abierta.
  - Source: https://www.akuvox.com/productsDisp?pid=130  Quote: "2 Relays & 2 Inputs"
  - Kind: definition
  - Level: core
  - Also: T23
- c:N21. En un monitor viejo (C315S) un integrador abre el relé del propio monitor con la URL vieja y DoorNum=0.
  - Source: https://www.comfortclick.com/Support/ExampleDetails/Akuvox  Quote: "DoorNum=0) for this type of indoor monitors"
  - Kind: story
  - Level: advanced
  - Also: T24
  - Bias: ejemplo de un fabricante de software domótico

## T19 HTTP saliente ante eventos
- c:N22. Action URL (Device Management > Setting > Action URL, ejemplo R20A 320.30.11.47): el portero o terminal manda un HTTP a un servidor cuando pasa algo (abrir puerta, llamar). Usuario y clave para servidores con digest; si la URL trae credenciales, mandan esas.
  - Source: https://knowledge.akuvox.com/docs/set-up-action-url  Quote: "the authentication in the URL takes precedence"
  - Kind: technique
  - Level: core
- c:N23. Variables que el equipo reemplaza: $relay1status (1 abierto, 0 cerrado), $input1status, $code, $card_sn, $unlocktype, $remote, $mac, $ip, $model, $firmware. Eventos en X915V2: llamada, corte, relé A/B/C disparado y cerrado, entradas, código válido e inválido, tarjeta, rostro, QR, alarma de intrusión y arranque.
  - Source: https://knowledge.akuvox.com/docs/set-up-action-url  Quote: "Variables that the device will automatically replace"
  - Kind: template
  - Level: core
- c:N24. El evento de arranque (Setup Completed) no depende del interruptor de Action URL: si no se usa, el campo queda vacío.
  - Source: https://knowledge.akuvox.com/docs/set-up-action-url  Quote: "This URL is not controlled by the Action URL Enable switch."
  - Kind: mistake
  - Level: advanced
- c:N25. ComfortClick integra un E11R escuchando HTTP del portero (timbre, botón de salida, movimiento) y abriendo relés por HTTP: el mismo patrón ida y vuelta.
  - Source: https://www.comfortclick.com/Support/ExampleDetails/Akuvox  Quote: "Two relays can be activated via HTTP command"
  - Kind: story
  - Level: advanced
  - Also: T20

## T20 Clientes HTTP
- c:N26. Home Assistant rest_command expone un pedido HTTP como acción; soporta método, usuario, clave, autenticación basic (por defecto) o digest, timeout (10 s por defecto) y verify_ssl. Se define en configuration.yaml y se reinicia.
  - Source: https://www.home-assistant.io/integrations/rest_command  Quote: "Either basic or digest."
  - Kind: technique
  - Level: core
- c:N27. MikroTik /tool fetch hace pedidos HTTP desde consola o script: user y password, Basic por defecto, http-auth-scheme=digest para digest; sin check-certificate no valida TLS; output=none descarta la respuesta; :onerror atrapa fallas. Documentación de RouterOS 7.
  - Source: https://manual.mikrotik.com/docs/system-information-and-utilities/fetch/  Quote: "set http-auth-scheme=digest for digest authentication"
  - Kind: technique
  - Level: core
- c:N28. Asterisk CURL(url) hace un GET desde el dialplan (POST si se pasa post-data), disponible desde Asterisk 10.
  - Source: https://docs.asterisk.org/Latest_API/API_Documentation/Dialplan_Functions/CURL/  Quote: "a 'HTTP GET' (by default) will be used"
  - Kind: technique
  - Level: advanced
- c:N29. Cámaras LPR abren por la HTTP API del portero: Setting > HTTP API en Allowlist con la IP de la cámara, patente cargada en el usuario (hasta 5) y la cámara manda un POST. Probadas Milesight, March Networks, Aibase, Hikvision (alarm server con /api/lpr/hik, solo X912 912.30.12.114 y R29 29.30.10.745 o más) y Dahua.
  - Source: https://knowledge.akuvox.com/docs/integration-with-milesight-lpr-camera-for-door-opening  Quote: "This integration works with cameras that support the POST method."
  - Kind: technique
  - Level: advanced
  - Also: T17
- c:N30. EC33 se integra por HTTP: en el EC33, Device > Relay > Open Relay via HTTP con usuario y clave; en el terminal, Device > Lift Control apuntando a la IP del EC33 con esas credenciales.
  - Source: https://knowledge.akuvox.com/docs/configure-lift-control-1  Quote: "enable Open Relay via HTTP"
  - Kind: technique
  - Level: advanced
  - Also: T23

## Disagreements seen
- Alta seguridad: Akuvox recomienda el formato nuevo y deja el modo de alta seguridad encendido por defecto (https://knowledge.akuvox.com/docs/trigger-door-actions-via-http-api-e18); un integrador de LogicMachine aconseja apagarlo para usar la URL vieja con admin (https://forum.logicmachine.net/showthread.php?tid=6156).
- Sin credenciales: la guía de apertura permite dejar usuario y clave en blanco (https://knowledge.akuvox.com/docs/open-door-via-http-command); la guía de la HTTP API reserva "None" para pruebas (https://knowledge.akuvox.com/docs/configure-http-api).
- Clave en la URL: Akuvox publica ejemplos con usuario y clave dentro de la URL (https://knowledge.akuvox.com/docs/trigger-door-actions-via-http-api-e18); pylocal-akuvox advierte que así queda en logs (https://pylocal-akuvox.readthedocs.io/en/latest/quickstart.html).

## Best stories
- El foro LogicMachine: funciona, pero apagando la alta seguridad y con admin en la URL (https://forum.logicmachine.net/showthread.php?tid=6156).
- El SR01: rompen el portero y la puerta sigue cerrada (https://knowledge.akuvox.com/docs/how-to-configure-sr01-security-relay-on-akuvox-door-phones).
- La cámara Hikvision que abre el portón leyendo la patente (https://knowledge.akuvox.com/docs/integration-with-milesight-lpr-camera-for-door-opening).
- Hasta 50 comandos de Web Relay con la IP en blanco (https://knowledge.akuvox.com/docs/configure-web-relay-on-door-phone-web-interface).
