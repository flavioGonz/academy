# Notes: batch a
Pages read: 26. With notes: 24. Skipped: 2 (MDN Push API y RFC 7826 solo aportan contexto de fechas y definiciones; se usan como referencia, sin notas propias de obra).

## T02 Analíticas de video en la cámara
- a:N1. IVA Pro ofrece dos tareas de conteo en la interfaz: Counter (objetos que cruzan una línea de hasta 16 nodos) y Occupancy (objetos dentro de un campo de hasta 16 nodos), con alarma opcional al llegar a un umbral.
  - Source: https://knowledge.keenfinity-group.com/video-systems/article/how-to-set-up-count-with-iva-pro-fw-9-40-and-get-the-data-from-the-camera  Quote: "Count all objects currently in a specified field"
  - Kind: definition
  - Level: foundation
- a:N2. Limitaciones declaradas por Bosch: no cuenta objetos ocultos más de un 50 %, los niños pueden no contarse bien, la vista cenital de personas solo con IVA Pro Buildings en FLEXIDOME panoramic 5100i.
  - Source: https://knowledge.keenfinity-group.com/video-systems/article/how-to-set-up-count-with-iva-pro-fw-9-40-and-get-the-data-from-the-camera  Quote: "Objects that are occluded by more than 50% will not be counted."
  - Kind: rule of thumb
  - Level: core
  - Also: T03
- a:N3. La tarea Occupancy con "Alarm on overcrowding" alarma cuando hay "critical value" objetos o más en el área.
  - Source: https://knowledge.keenfinity-group.com/video-systems/article/how-to-set-up-count-with-iva-pro-fw-9-40-and-get-the-data-from-the-camera
  - Kind: technique
  - Level: core
  - Also: T08
- a:N4. La configuración se hace en Configuration Manager 7.74 o superior: VCA → Main Operation (IVA Pro Buildings como tipo de análisis) y VCA → Tasks (borrar la tarea por defecto, agregar Counter u Occupancy, nombrarla).
  - Source: https://knowledge.keenfinity-group.com/video-systems/article/how-to-set-up-count-with-iva-pro-fw-9-40-and-get-the-data-from-the-camera
  - Kind: technique
  - Level: core
- a:N5. Los contadores de la cámara se reinician con el comando RCP+ CONF_IVA_COUNTER_VALUES, al escribir una configuración IVA nueva o al llegar a un valor configurado. Bosch recomienda resetear con regularidad.
  - Source: https://knowledge.keenfinity-group.com/video-systems/article/how-to-set-up-count-with-iva-pro-fw-9-40-and-get-the-data-from-the-camera  Quote: "It is best practice to reset the counter values regularly"
  - Kind: rule of thumb
  - Level: core
  - Also: T09
- a:N6. Por ONVIF llega un subconjunto de la metadata VCA (eventos y cajas de objetos); la metadata completa va en el formato propietario VCD por RCP+ o RTSP; MQTT también puede transportar eventos de conteo.
  - Source: https://knowledge.keenfinity-group.com/video-systems/article/how-to-set-up-count-with-iva-pro-fw-9-40-and-get-the-data-from-the-camera  Quote: "a reduced set of the VCA metadata including the events"
  - Kind: definition
  - Level: core
  - Also: T05
- a:N7. Bosch publica por ONVIF eventos de reglas IVA (Object in field, Crossing line, Entering field, Leaving field, Counter, Crowd detection, etc.); el mensaje lleva la fuente de video, el tipo de evento y el nombre de la regla. Desde FW 6.10.
  - Source: https://media.boschsecurity.com/fs/media/pb/media/partners_1/integration_tools_1/developer/Bosch-Metadata-and-IVA-Events.pdf  Quote: "ONVIF IVA event message contains the video source the event type and the rule name"
  - Kind: definition
  - Level: core
  - Also: T05
- a:N8. Si se crea una regla nueva en la cámara, el cliente ONVIF tiene que volver a pedir GetEventProperties; mover una línea no lo requiere. Por compatibilidad, los eventos IVA también salen como alarma de movimiento.
  - Source: https://media.boschsecurity.com/fs/media/pb/media/partners_1/integration_tools_1/developer/Bosch-Metadata-and-IVA-Events.pdf
  - Kind: mistake
  - Level: advanced
  - Also: T06
- a:N9. Axis separa igual los dos escenarios: Crossline counting (acumulado desde el último reset) y Occupancy in area (objetos presentes ahora); el acumulado de cruces no se resetea solo salvo que se active el reset a medianoche.
  - Source: https://developer.axis.com/analytics/axis-object-analytics-counting-data  Quote: "the accumulated number of counts will never reset"
  - Kind: rule of thumb
  - Level: core
  - Also: T09

## T03 Planificar la cámara de conteo
- a:N10. La vista cenital es la mejor; vista frontal o poco inclinada "no sirve para contar". Lista de Bosch: altura mayor a 3 m, sin superficies que reflejen, hasta 64 personas en escena, pasillos rectos, evitar gente que dobla y sale enseguida o que merodea sobre la línea.
  - Source: https://knowledge.keenfinity-group.com/video-systems/article/how-to-set-up-count-with-iva-pro-fw-9-40-and-get-the-data-from-the-camera  Quote: "Camera height >3m"
  - Kind: rule of thumb
  - Level: foundation
- a:N11. Dejar lugar antes y después de la línea o del borde del campo: si la línea queda pegada al borde de la imagen, la persona no se detecta a tiempo.
  - Source: https://knowledge.keenfinity-group.com/video-systems/article/how-to-set-up-count-with-iva-pro-fw-9-40-and-get-the-data-from-the-camera
  - Kind: mistake
  - Level: core
- a:N12. Ningún contador es 100 % exacto: un cliente que deja el carro y se va, o que se agacha, rompe el seguimiento. FootfallCam declara 99 % para su sensor estéreo (su afirmación).
  - Source: https://www.footfallcam.com/blog/2024/03/redefining-queue-analytics-a-big-data-modelling-approach/  Quote: "there is no people counter with perfect counting accuracy"
  - Kind: story
  - Level: core
  - Bias: vende contadores y analítica de filas.
  - Also: T13

## T04 ONVIF y Profile M
- a:N13. ONVIF se fundó en 2008 (Axis, Bosch y Sony); Core 1.0 en noviembre de 2008; Profile S en 2012; Profile M publicado en junio de 2021.
  - Source: https://en.wikipedia.org/wiki/ONVIF
  - Kind: definition
  - Level: foundation
- a:N14. El release candidate de Profile M se anunció el 29 de septiembre de 2020; nombra la gestión de filas por conteo de personas como caso de uso.
  - Source: https://www.onvif.org/?p=4937  Quote: "crowd control or queue management through people counting analytics"
  - Kind: story
  - Level: foundation
- a:N15. Profile M: metadata y eventos para analíticas; interfaces de eventos para contador de objetos; eventos por metadata, servicio de eventos ONVIF o MQTT; se combina con S y T para video.
  - Source: https://www.onvif.org/profiles/profile-m/
  - Kind: definition
  - Level: core
- a:N16. Bosch: la metadata ONVIF (MetadataConfig1) se agrega a mano al perfil ONVIF; el contador como evento va solo en el stream de metadata.
  - Source: https://media.boschsecurity.com/fs/media/pb/media/partners_1/integration_tools_1/developer/Bosch-Metadata-and-IVA-Events.pdf  Quote: "must be added manually to the ONVIF profile"
  - Kind: mistake
  - Level: advanced
- a:N17. Para que GetProfile devuelva la analítica de una Bosch hay que sumar "Video Analytic Configuration" al perfil (ONVIF Device Manager o script propio).
  - Source: https://knowledge.keenfinity-group.com/video-systems/article/how-can-you-add-the-analytics-of-bosch-cameras-to-the-onvif-getprofile
  - Kind: technique
  - Level: advanced
- a:N18. EdgeX gestiona módulos y reglas de analítica con Profile M (AnalyticsModules, SupportedAnalyticsModules, AnalyticsModuleOptions).
  - Source: https://docs.edgexfoundry.org/3.2/microservices/device/services/device-onvif-camera/supplementary-info/api-analytic-support/
  - Kind: definition
  - Level: advanced

## T05 Eventos ONVIF
- a:N19. Todo dispositivo ONVIF implementa el Real-time Pull-Point: el cliente pide un pull point (CreatePullPointSubscription), recibe una dirección y llama PullMessages; el cliente inicia toda la comunicación, por eso es "amigable con el firewall".
  - Source: https://www.onvif.org/specs/2606/ONVIF-Core-Spec-v2606.pdf  Quote: "firewall friendly notification interface"
  - Kind: definition
  - Level: core
- a:N20. Basic Notification (WS-BaseNotification): el cliente se suscribe, la cámara abre otra conexión y manda Notify; la suscripción vence en el TerminationTime salvo que el cliente la renueve.
  - Source: https://www.onvif.org/specs/2606/ONVIF-Core-Spec-v2606.pdf
  - Kind: definition
  - Level: core
- a:N21. Eventos de propiedad: PropertyOperation "Initialized" al crear la propiedad o al pedir un punto de sincronización, "Changed" cuando cambia, "Deleted" al desaparecer.
  - Source: https://www.onvif.org/specs/2606/ONVIF-Core-Spec-v2606.pdf  Quote: "The operation mode “Initialized” shall also be used when a synchronization point has been requested."
  - Kind: definition
  - Level: core
- a:N22. Milestone: el driver ONVIF hace PullMessages cada 5 s por defecto y solo considera los mensajes con PropertyOperation "Changed"; después de crear el pull point manda SetSynchronizationPoint para leer el estado actual.
  - Source: https://doc.milestonesys.com/latest/en-US/onvifdriver/events.htm  Quote: "every 5 seconds by default"
  - Kind: technique
  - Level: core
- a:N23. Un desarrollador de servidor ONVIF reporta eventos duplicados en cada pull al repetir el mismo valor sin PropertyOperation: el filtrado de cambios no es trivial y cada cliente lo resuelve distinto.
  - Source: https://forum.milestonesys.com/t/the-onvif-pull-point-event-is-raised-redundantly-by-the-onvif-driver/13473
  - Kind: story
  - Level: advanced
- a:N24. EdgeX resume las dos vías: PullPoint ("pull") y BaseNotification ("push" con Notify, Subscribe y Renew); su servicio renueva la suscripción push diez segundos antes de que venza y crea un pull point nuevo cuando expira.
  - Source: https://docs.edgexfoundry.org/3.2/microservices/device/services/device-onvif-camera/supplementary-info/api-event-handling/
  - Kind: technique
  - Level: core
- a:N25. Bosch (FW 7.84 RTOS, 8.50 CPP14, 8.45 Inteox en adelante): las reglas IVA salen bajo tns1:IVA salvo el cruce de línea, que sale bajo tns1:RuleEngine; conviene suscribirse a los dos tópicos.
  - Source: https://knowledge.keenfinity-group.com/video-systems/article/tns1-iva-does-not-include-all-iva-rules-in-camera
  - Kind: mistake
  - Level: advanced
  - Also: T16

## T07 Video en vivo
- a:N26. RTSP de Bosch: rtsp://IP abre el stream 1; ?inst=2 el segundo stream; ?line= elige la entrada en equipos multicanal; rtsp_tunnel no va en la query string; vcd habilita los datos VCA de Bosch.
  - Source: https://knowledge.keenfinity-group.com/video-systems/article/how-is-rtsp-usage-supported-with-bosch-vip-devices
  - Kind: technique
  - Level: core
- a:N27. go2rtc: un solo binario sin dependencias, configuración en go2rtc.yaml (streams: nombre: url), API y WebUI en el puerto 1984, servidor RTSP en 8554, WebRTC en 8555; transcodifica con FFmpeg solo si hace falta; ofrece api/stream.mp4.
  - Source: https://pkg.go.dev/github.com/AlexxIT/go2rtc
  - Kind: definition
  - Level: core
- a:N28. RTSP 2.0 es la RFC 7826 (diciembre de 2016) y reemplaza a la RFC 2326 de 1998.
  - Source: https://datatracker.ietf.org/doc/html/rfc7826
  - Kind: definition
  - Level: foundation

## T11 Canales y despachos
- a:N29. BullMQ reintenta con backoff exponencial: espera 2^(intento-1) × delay; con delay de 3 s, el séptimo intento llega 3,2 minutos después del anterior.
  - Source: https://docs.bullmq.io/guide/retrying-failing-jobs  Quote: "2 ^ (attempts - 1) * delay"
  - Kind: number
  - Level: core
- a:N30. Telegram: sendPhoto acepta una URL que descarga Telegram (fotos hasta 5 MB por URL) y sendAnimation manda GIF o video sin sonido; el archivo tiene que ser accesible desde internet si va por URL.
  - Source: https://core.telegram.org/bots/api  Quote: "Telegram will download and send the file. 5 MB max size for photos"
  - Kind: rule of thumb
  - Level: core
- a:N31. Web Push: el servidor de la aplicación manda el mensaje a un push service, que lo entrega al navegador aunque la página no esté abierta (RFC 8030, diciembre de 2016).
  - Source: https://datatracker.ietf.org/doc/html/rfc8030
  - Kind: definition
  - Level: core
- a:N32. VAPID (RFC 8292, noviembre de 2017): la suscripción queda atada a la clave pública del servidor y cada envío se firma con la privada; sin la privada no se puede usar la suscripción.
  - Source: https://pushpad.xyz/blog/web-push-what-is-vapid/
  - Kind: definition
  - Level: core
- a:N33. El Push API necesita un service worker activo y está disponible en los navegadores principales desde marzo de 2023.
  - Source: https://developer.mozilla.org/en-US/docs/Web/API/Push_API
  - Kind: definition
  - Level: foundation

## T13 Tiempo de espera
- a:N34. Ley de Little: L = λW; vale para cualquier distribución de llegadas y de servicio, cualquier cantidad de servidores y cualquier disciplina, si el sistema es estable. Sirve para despejar W = L/λ.
  - Source: https://third-bit.com/2026/05/30/littles-law/  Quote: "As long as the system is stable and stationary"
  - Kind: definition
  - Level: core
- a:N35. Si llegan más de los que se atienden, la fila crece sin límite: la ley "sigue valiendo", pero dice que el sistema está roto.
  - Source: https://third-bit.com/2026/05/30/littles-law/
  - Kind: rule of thumb
  - Level: core
- a:N36. Historia: usada sin prueba en 1954, Philip Morse desafió a encontrar un contraejemplo y John Little publicó la prueba en 1961.
  - Source: https://en.wikipedia.org/wiki/Little%27s_law
  - Kind: story
  - Level: foundation
- a:N37. Little, a los 50 años de su prueba: la ley también vale en intervalos finitos si se miden bien llegadas y salidas en [0, T]; el ejemplo es una tienda con su arribo por hora y su tiempo medio adentro.
  - Source: https://projectproduction.org/journal/reprint-littles-law-as-viewed-on-its-50th-anniversary/
  - Kind: story
  - Level: advanced
- a:N38. FootfallCam discrepa del seguimiento individual: propone estimar la espera con largo de fila y tiempo de servicio promedio, sin seguir a cada persona (su afirmación: 99,9 % frente a 99 %).
  - Source: https://www.footfallcam.com/blog/2024/03/redefining-queue-analytics-a-big-data-modelling-approach/
  - Kind: technique
  - Level: advanced
  - Bias: vende el producto que describe.

## Disagreements seen
- Cómo estimar la espera: FootfallCam usa largo de fila y tiempo de servicio (https://www.footfallcam.com/blog/2024/03/redefining-queue-analytics-a-big-data-modelling-approach/); la ley de Little en su forma general usa llegadas o salidas promedio en una ventana (https://third-bit.com/2026/05/30/littles-law/). OmniAccess hace lo segundo con salidas de 15 minutos.
- Qué cuenta como evento: Milestone ignora todo lo que no sea "Changed" (https://doc.milestonesys.com/latest/en-US/onvifdriver/events.htm); la especificación usa "Initialized" también al sincronizar (https://www.onvif.org/specs/2606/ONVIF-Core-Spec-v2606.pdf); el foro muestra servidores que repiten valores (https://forum.milestonesys.com/t/the-onvif-pull-point-event-is-raised-redundantly-by-the-onvif-driver/13473).
- Ángulo de la cámara: Bosch dice que la vista frontal no sirve para contar (https://knowledge.keenfinity-group.com/video-systems/article/how-to-set-up-count-with-iva-pro-fw-9-40-and-get-the-data-from-the-camera); en obra se suele reutilizar la cámara de seguridad existente, como sugiere el manual de OmniAccess ("usando las mismas cámaras del lugar").

## Best stories
- La ley de Little se usaba sin prueba hasta que Morse desafió a encontrar un contraejemplo y Little la probó en 1961: https://en.wikipedia.org/wiki/Little%27s_law
- ONVIF nombró la gestión de filas como caso de uso de Profile M en 2020: https://www.onvif.org/?p=4937
- Bosch: "objetos tapados más del 50 % no se cuentan" y la cámara a menos de 3 m deja pasar gente sin contar: https://knowledge.keenfinity-group.com/video-systems/article/how-to-set-up-count-with-iva-pro-fw-9-40-and-get-the-data-from-the-camera
- Un desarrollador ONVIF ve el mismo evento disparado en cada pull: https://forum.milestonesys.com/t/the-onvif-pull-point-event-is-raised-redundantly-by-the-onvif-driver/13473
