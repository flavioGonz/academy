# Notes: batch a
Pages read: 30. With notes: 27. Skipped: 3 (Axis cross line detection: es la API de instalación de una ACAP, no suma a este curso; ONVIF Profile Feature Overview y página de Profile S: solo tablas de perfiles, una nota de contexto).

Fuente principal aparte: el código de OmniAccess (octubre de 2026), leído en `src/app/admin/monitor-intrusion`, `src/components/intrusion/*`, `src/lib/intrusion/analisis.ts`, `server.js`, `dahua-events.js`, `lib-intrusion-capture.js`, `src/lib/isapi-*.ts`, `src/app/actions/detections.ts`, `prisma/schema.prisma`, `docs/manual/*.md`. Esas notas van en `b.md`.

## T01 Qué es una analítica de intrusión
- a:N1. Hikvision expone como eventos separados Motion, Line Crossing y Field Detection (intrusión de zona); el integrador de Home Assistant crea un sensor por cada evento configurado para "Notify the surveillance center".
  - Source: https://www.home-assistant.io/integrations/hikvision  Quote: "configured within the camera/nvr interface to “Notify the surveillance center”"
  - Kind: definition
  - Level: foundation
  - Also: T02
  - Bias: none
- a:N2. ONVIF define dos reglas de analítica estándar: LineDetector (una polilínea; si un objeto la cruza en el sentido indicado manda el evento Crossed) y FieldDetector (un polígono; informa si cada objeto está adentro o afuera, ObjectsInside).
  - Source: https://www.onvif.org/specs/2206/Analytics.html  Quote: "If an object crosses the polyline in the specified direction, the rule engine sends a Crossed event"
  - Kind: definition
  - Level: foundation
  - Bias: none
- a:N3. Dahua nombra el cruce de línea "CrossLineDetection: tripwire event" y la intrusión "CrossRegionDetection: intrusion event", con VideoMotion aparte para movimiento.
  - Source: https://community.home-assistant.io/t/dahua-ipc-to-mqtt-app/93327?page=5  Quote: "CrossLineDetection: tripwire event"
  - Kind: definition
  - Level: foundation
  - Also: T02
  - Bias: none
- a:N4. Milesight describe la intrusión como protección de un área: alarma tanto si el objeto entra desde afuera como si aparece de golpe adentro; el cruce de línea dispara cada vez que un objeto atraviesa la línea virtual.
  - Source: https://www.milesight.com/support/download/document-center/ipc-series/ndaa/en/user-manual/intrusion-detection.html  Quote: "Whether it is an intrusion from outside the region or a sudden appearance within the region"
  - Kind: definition
  - Level: foundation
  - Also: T03
  - Bias: fabricante
- a:N5. Trassir presenta el detector de cruce como herramienta de perímetro: cuando una persona, vehículo u objeto cruza, avisa al operador, graba o activa otras acciones.
  - Source: https://storage.trassir.com/manual/en/setup-line-crossing.html  Quote: "sends a notification to the operator, starts video recording"
  - Kind: definition
  - Level: foundation
  - Bias: fabricante de VMS

## T02 Cómo llega el evento
- a:N6. Una cámara puede mandar eventos de dos formas: empujándolos a un servidor (Actively Push, HTTP POST a IP, puerto y ruta) o dejando que una plataforma se suscriba (Push by Subscription, la plataforma se conecta a la cámara).
  - Source: https://videos.cctvcamerapros.com/developer/docs/getting-started/http-post-setup  Quote: "Actively Push makes the camera connect out to the servers in the table"
  - Kind: definition
  - Level: core
  - Bias: vende cámaras y un SDK
- a:N7. El evento puede salir directo de la cámara o reenviado por el NVR; la cámara directa necesita estar en la red (no detrás de los puertos PoE del NVR).
  - Source: https://videos.cctvcamerapros.com/developer/docs/getting-started/http-post-setup  Quote: "Requires the camera to be on your local network via a PoE switch"
  - Kind: rule of thumb
  - Level: core
  - Also: T06
  - Bias: vende cámaras
- a:N8. Un servidor de alarmas genérico se suscribe a Hikvision por HTTP streaming y a Dahua conectándose a cada cámara con usuario y clave; para Hisilicon escucha en un puerto.
  - Source: https://hub.docker.com/r/toxuin/alarmserver  Quote: "Alarm Server uses HTTP streaming to connect to each camera individually and subscribe to all the events."
  - Kind: technique
  - Level: core
  - Bias: none (software libre)
- a:N9. En Dahua la suscripción se abre con `eventManager.cgi?action=attach&codes=[...]` y queda abierta recibiendo eventos; un foro lo recomienda con wget para diagnosticar.
  - Source: https://community.home-assistant.io/t/dahua-ipc-to-mqtt-app/93327?page=5  Quote: "A great way to troubleshot is use the command that makes a log"
  - Kind: test
  - Level: advanced
  - Also: T16
  - Bias: none
- a:N10. Bosch: por ONVIF, el cruce de línea llega por el tópico tns1:RuleEngine y no por tns1:IVA; un cliente suscripto solo a IVA no recibe los cruces.
  - Source: https://knowledge.keenfinity-group.com/video-systems/article/tns1-iva-does-not-include-all-iva-rules-in-camera  Quote: "ONVIF client only receives motion events and no Line Crossing information"
  - Kind: mistake
  - Level: advanced
  - Also: T16
  - Bias: fabricante
- a:N11. Ajax: si la cámara está integrada por ONVIF, los cruces también se transmiten por ONVIF; si está habilitado el envío a central, también van a la central.
  - Source: https://ajax.systems/support/posts/line-crossing-detection-in-ajax-video-surveillance/  Quote: "line crossing events are also transmitted via ONVIF"
  - Kind: definition
  - Level: core
  - Bias: fabricante

## T03 Configurar la regla en la cámara
- a:N12. En un NVR Hikvision V5: Menú, Cámara, Smart Event, elegir cámara, Line Crossing Detection, Enable, Draw Area, sentido A→B, B→A o ambos, sensibilidad, objetivo; después pestaña Schedule y en Linkage Action tildar Notify Surveillance Center.
  - Source: https://www.securitywholesalers.com.au/faqs/how-to-configure-acusense-using-hikvision-nvr-v5-0-firmware/  Quote: "In Linkage Action, tick: Trigger Recording Notify Surveillance Center"
  - Kind: template
  - Level: core
  - Also: T05
  - Bias: distribuidor
- a:N13. Sentido: A→B dispara solo si el objeto pasa del lado A al B; B→A al revés; A↔B en los dos sentidos. Se pueden tener hasta cuatro líneas.
  - Source: https://www.milesight.com/support/download/document-center/ipc-series/ai/en/user-manual/line-crossing.html  Quote: "“A ↔ B” means that the alarm will be triggered when objects cross line from either side."
  - Kind: definition
  - Level: core
  - Bias: fabricante
- a:N14. En intrusión de zona se ajustan umbral de tiempo (lo mínimo que el intruso queda adentro), sensibilidad y porcentaje (tamaño mínimo del intruso respecto del área).
  - Source: https://global.uniview.com/res/201905/30/20190530_1728629_How-to-set-Intrusion-Detection_850805_168459_0.pdf  Quote: "The minimum length of time that the intruder stays in the detection area before an alarm will be reported."
  - Kind: definition
  - Level: core
  - Also: T08
  - Bias: fabricante
- a:N15. Recomendaciones para dibujar la línea: no pegada al borde del cuadro, no sobre árboles, postes o autos estacionados, larga para cortar todos los caminos, y siempre probar después de dibujarla.
  - Source: https://ajax.systems/support/posts/line-crossing-detection-in-ajax-video-surveillance/  Quote: "after adding a line, always perform a test"
  - Kind: rule of thumb
  - Level: core
  - Also: T08
  - Bias: fabricante
- a:N16. Trassir: si hay falsas alarmas, bajar la sensibilidad; modo de escena interior o exterior; filtro de tiempo.
  - Source: https://storage.trassir.com/manual/en/setup-line-crossing.html  Quote: "If false alarms occur, the sensitivity value should be reduced."
  - Kind: rule of thumb
  - Level: core
  - Also: T08
  - Bias: fabricante
- a:N17. Milesight: tamaño mínimo y máximo de objeto y modo de disparo "Bottom" (cuando la base del objeto entra) para que el cuerpo que se asoma no dispare.
  - Source: https://www.milesight.com/support/download/document-center/ipc-series/ndaa/en/user-manual/intrusion-detection.html  Quote: "the alarm will be triggered as soon as the bottom of the object enters the detection area"
  - Kind: technique
  - Level: advanced
  - Bias: fabricante

## T04 Clasificación de objetivo
- a:N18. Los algoritmos actuales clasifican humano, vehículo motor y no motor, e ignoran animales, hojas y lluvia; Uniview lo llama Smart Intrusion Prevention.
  - Source: https://www.uniview.com/News/Blog/202605/1100575_169683_0.htm  Quote: "classify moving objects into specific categories such as human, motor vehicle, and non-motor vehicle"
  - Kind: definition
  - Level: core
  - Also: T08
  - Bias: fabricante, artículo con productos
- a:N19. Milesight y Ajax permiten elegir el objeto que dispara (persona, vehículo, en Ajax también mascota) por línea.
  - Source: https://www.milesight.com/support/download/document-center/ipc-series/ai/en/user-manual/line-crossing.html  Quote: "Check Human or Vehicle attribute"
  - Kind: technique
  - Level: core
  - Bias: fabricante

## T05 Horario de armado
- a:N20. Hikvision: el evento solo funciona cuando el horario de armado está activo; si falta o tiene un hueco, no dispara. Problema común: armado de día y apagado de noche. Ruta: Configuration, Event, el evento, Arming Schedule.
  - Source: https://supportusa.hikvision.com/support/solutions/articles/17000129443-why-is-the-arming-schedule-important-  Quote: "if it is missing or there is a gap the event will not trigger"
  - Kind: mistake
  - Level: foundation
  - Bias: fabricante
- a:N21. Hikvision distingue horario de grabación (cuándo graba: continuo o por movimiento) de horario de armado (cuándo el evento está habilitado).
  - Source: https://supportusa.hikvision.com/support/solutions/articles/17000133598-what-is-the-difference-between-arming-schedule-recording-schedule-  Quote: "Arming schedule is when an event, like motion, is enabled on camera."
  - Kind: definition
  - Level: foundation
  - Bias: fabricante
- a:N22. Un instalador quería intrusión de noche (por los faros de los autos) y movimiento de día; mezclaba horario de grabación y de armado y no le cerraba lo que pasaba.
  - Source: https://www.ipcamtalk.com/threads/difference-between-arming-schedule-and-recording-schedule.7096  Quote: "all night i want smart event ( intrusion detection ) due to headlight intrusions"
  - Kind: story
  - Level: foundation
  - Bias: none
- a:N23. Milesight: el horario de detección se arma por día y se puede copiar a todos los días con "All".
  - Source: https://www.milesight.com/support/download/document-center/ipc-series/ndaa/en/user-manual/intrusion-detection.html  Quote: "The "All" button is handy to copy the today’s schedule to all"
  - Kind: technique
  - Level: core
  - Bias: fabricante

## T07 Probar la cadena
- a:N24. El botón Test de la notificación HTTP manda un POST vacío; si el servidor contesta 200, la cámara muestra "Test successful". El heartbeat es otra cosa: un keepalive periódico.
  - Source: https://videos.cctvcamerapros.com/developer/docs/getting-started/http-post-setup  Quote: "If the server answers HTTP 200, the camera shows Test successful."
  - Kind: test
  - Level: core
  - Also: T16
  - Bias: vende cámaras
- a:N25. El servidor tiene que contestar cada POST al instante, incluidos los keepalive vacíos; si no, la cámara muestra la conexión Offline y la corta.
  - Source: https://videos.cctvcamerapros.com/developer/docs/getting-started/http-post-setup  Quote: "Acknowledge every POST immediately."
  - Kind: rule of thumb
  - Level: advanced
  - Also: T16
  - Bias: vende cámaras
- a:N26. Para que Home Assistant reciba eventos de Hikvision el usuario necesita el permiso "Remote: Notify Surveillance Center/Trigger Alarm Output" y la autenticación web en digest/basic, en cada cámara si hay NVR.
  - Source: https://www.home-assistant.io/integrations/hikvision  Quote: "the hikvision user must have the ‘Remote: Notify Surveillance Center/Trigger Alarm Output’ permission"
  - Kind: mistake
  - Level: advanced
  - Also: T16
  - Bias: none

## T08 Falsas alarmas
- a:N27. Davantis: más del 76 % de las alarmas que recibe una central son falsas con detección de movimiento convencional (su afirmación); las causas se agrupan en instalación, ambiente, biológicas y del sistema.
  - Source: https://www.davantis.com/wp-content/uploads/perimeter-security-false-alarms-guide.pdf  Quote: "more than 76% of the signals reaching a CMS are false"
  - Kind: number
  - Level: foundation
  - Bias: vende analítica DFUSION
- a:N28. Davantis propone cuatro niveles en orden: instalación (30 a 40 % se elimina reubicando, su afirmación), configuración (zonas de exclusión, umbrales por hora), tecnología (clasificación de objetos, hasta 95 %, su afirmación) y proceso (auditar falsas por zona cada mes).
  - Source: https://www.davantis.com/wp-content/uploads/perimeter-security-false-alarms-guide.pdf  Quote: "The four levels are applied in order: first resolve installation issues"
  - Kind: template
  - Level: core
  - Bias: vende analítica
- a:N29. El otro error es el falso negativo: bajar falsas alarmas a costa de perder detecciones empeora el problema real; un operador que vio 500 falsas responde peor a la 501.
  - Source: https://www.davantis.com/wp-content/uploads/perimeter-security-false-alarms-guide.pdf  Quote: "An operator who has processed 500 consecutive false alarms has reduced responsiveness to alarm 501."
  - Kind: story
  - Level: core
  - Also: T09
  - Bias: vende analítica
- a:N30. Uniview: arañas que hacen tela frente al domo reflejan el IR; una superficie metálica brillante puede causar cientos de alarmas; limpiar el vidrio y sacar el horizonte del cuadro.
  - Source: https://www.uniview.com/News/Blog/202605/1100575_169683_0.htm  Quote: "spiders building webs directly over the camera housing reflect infrared light"
  - Kind: mistake
  - Level: core
  - Bias: fabricante
- a:N31. Un usuario en Argentina se quejaba de que en un DVR Hikvision ni el porcentaje ni la sensibilidad frenaban gatos y pájaros en la intrusión de zona (detección sin clasificación).
  - Source: https://ipcamtalk.com/threads/intrusion-detection-settings-does-not-work.24107  Quote: "I get the event triggered with a cat, or even a bird walking around the area"
  - Kind: story
  - Level: core
  - Also: T04
  - Bias: none

## T09 Verificación y atención
- a:N32. Al despachar, decir "delito en curso" y atenerse a los hechos: no decir que alguien tiene un arma si no se ve.
  - Source: https://www.sdmmag.com/articles/89047-video-monitoring-best-practices  Quote: "“Stick to the facts,” Hertel adds."
  - Kind: rule of thumb
  - Level: core
  - Bias: none
- a:N33. Grabar la pantalla exacta que vio el operador aumenta la chance de que sirva como evidencia; los operadores de video reciben 10 a 60 días de formación (según las centrales consultadas).
  - Source: https://www.sdmmag.com/articles/89047-video-monitoring-best-practices  Quote: "recording the exact screen views that the central station operator sees"
  - Kind: technique
  - Level: core
  - Also: T11
  - Bias: none
- a:N34. Si la misma zona dispara varias veces en una hora, una central despacha una sola vez; la verificación por video con un clip corto ayuda al operador a decidir.
  - Source: https://www.securitysales.com/insights/central-stations-assess-actual-alarms/147248/  Quote: "If the same zone trips multiple times within an hour, we only dispatch once"
  - Kind: rule of thumb
  - Level: core
  - Also: T13
  - Bias: centrales mayoristas promocionan servicios
- a:N35. Cross-zoning: dos señales de zonas vecinas en poco tiempo confirman un intruso mejor que una sola; la verificación por video manda cuadros de antes y después del evento.
  - Source: https://www.securityinfowatch.com/home/article/10537347/seeing-is-believing  Quote: "A second alarm signal, received in an adjacent zone in close time proximity"
  - Kind: technique
  - Level: core
  - Also: T13
  - Bias: none
- a:N36. Davantis: la alarma tiene que llegar al operador ya calificada (persona o vehículo, zona, prioridad) y con el video a un clic; si hay que cambiar de interfaz, se atiende fuera del protocolo.
  - Source: https://www.davantis.com/wp-content/uploads/perimeter-security-false-alarms-guide.pdf  Quote: "Qualified events, not raw signals"
  - Kind: rule of thumb
  - Level: core
  - Bias: vende analítica

## T10 Video en vivo y reproducción
- a:N37. go2rtc toma video de decenas de formatos y protocolos y lo entrega en los formatos populares, con transcodificación por FFmpeg solo si hace falta y latencia mínima.
  - Source: https://pkg.go.dev/github.com/AlexxIT/go2rtc  Quote: "on-the-fly transcoding only if necessary via FFmpeg"
  - Kind: definition
  - Level: core
  - Bias: none
- a:N38. RTSP 2.0 (RFC 7826) reemplaza al 1.0 (RFC 2326) y es el protocolo de capa de aplicación para establecer y controlar la entrega de audio y video en tiempo real.
  - Source: https://datatracker.ietf.org/doc/html/rfc7826  Quote: "RTSP is an application-layer protocol for the setup and control of the delivery of data with real-time properties."
  - Kind: definition
  - Level: core
  - Bias: none
- a:N39. Perfil ONVIF S: cámara o codificador que manda video por IP a un cliente que lo configura y controla; en proceso de deprecación (último envío de conformidad 31 de marzo de 2027).
  - Source: https://www.onvif.org/profiles/profile-s/  Quote: "Profile deprecation in process; last date of product conformance submissions is March 31, 2027."
  - Kind: definition
  - Level: core
  - Bias: none

## T11 Evidencia y registro
- a:N40. MinIO borra objetos automáticamente por reglas de vencimiento (expiry) compatibles con el ciclo de vida de S3.
  - Source: https://min.io/docs/minio/linux/administration/object-management/object-lifecycle-management.html  Quote: "For object expiry, MinIO AIStor automatically deletes the object."
  - Kind: definition
  - Level: core
  - Bias: fabricante

## T12 Avisos
- a:N41. Un bot de Telegram se crea y administra con @BotFather, que entrega el token; con ese token el servidor manda mensajes y fotos por la Bot API (sendMessage, sendPhoto).
  - Source: https://core.telegram.org/bots/features  Quote: "BotFather, creating and managing bots"
  - Kind: definition
  - Level: core
  - Bias: none
- a:N42. Web Push (RFC 8030) es el protocolo para entregar eventos en tiempo real a un navegador o app a través de un servicio de push.
  - Source: https://datatracker.ietf.org/doc/html/rfc8030  Quote: "a simple protocol for the delivery of real-time events to user agents"
  - Kind: definition
  - Level: core
  - Bias: none

## Disagreements seen
- Dónde filtrar la falsa alarma: Davantis defiende filtrar en el sitio con análisis a 25 cuadros por segundo; las centrales de securitysales.com confían en la verificación humana por video y en contactar al cliente. https://www.davantis.com/wp-content/uploads/perimeter-security-false-alarms-guide.pdf frente a https://www.securitysales.com/insights/central-stations-assess-actual-alarms/147248/
- Sensibilidad: Trassir y Milesight tratan la sensibilidad como la perilla principal; el foro de ipcamtalk muestra que sin clasificación de objeto ni sensibilidad ni porcentaje frenan gatos y pájaros. https://storage.trassir.com/manual/en/setup-line-crossing.html frente a https://ipcamtalk.com/threads/intrusion-detection-settings-does-not-work.24107
- Push o suscripción: cctvcamerapros enseña el push de la cámara al servidor; alarmserver y el script de Dahua se suscriben a la cámara. https://videos.cctvcamerapros.com/developer/docs/getting-started/http-post-setup frente a https://hub.docker.com/r/toxuin/alarmserver

## Best stories
- El operador que vio 500 falsas alarmas y responde peor a la 501: https://www.davantis.com/wp-content/uploads/perimeter-security-false-alarms-guide.pdf
- La central que despacha una sola vez si la misma zona dispara varias veces en una hora: https://www.securitysales.com/insights/central-stations-assess-actual-alarms/147248/
- El usuario argentino con gatos y pájaros que disparan la intrusión con porcentaje al 90 %: https://ipcamtalk.com/threads/intrusion-detection-settings-does-not-work.24107
- Armado de día y apagado de noche, el error común según Hikvision: https://supportusa.hikvision.com/support/solutions/articles/17000129443-why-is-the-arming-schedule-important-
- "Stick to the facts" al despachar: https://www.sdmmag.com/articles/89047-video-monitoring-best-practices
