# Mapa de acuerdos: OmniAccess Intrusión

Cómo leer N de M: M son las páginas web con notas en ese subtema; N las que sostienen la idea. Lo que dice el producto sale de `notes/b.md` (código) y no entra en la cuenta: es la regla de la casa.

## TH01 Separá cruce de línea, intrusión de zona y movimiento: son tres eventos distintos
- Sub-topic: T01
- Agree: 5 de 5. Notes: a:N1, a:N2, a:N3, a:N4, a:N5. Urls: https://www.home-assistant.io/integrations/hikvision https://www.onvif.org/specs/2206/Analytics.html https://community.home-assistant.io/t/dahua-ipc-to-mqtt-app/93327?page=5 https://www.milesight.com/support/download/document-center/ipc-series/ndaa/en/user-manual/intrusion-detection.html https://storage.trassir.com/manual/en/setup-line-crossing.html
- Disagree: none found
- Level: foundation
- Best story: OmniAccess descarta el movimiento simple porque saturaba el sistema (b:N2)

## TH02 Elegí la vía del evento según la marca: push de la cámara o suscripción al equipo
- Sub-topic: T02
- Agree: 4 de 6. Notes: a:N6, a:N7, a:N8, a:N9. Urls: https://videos.cctvcamerapros.com/developer/docs/getting-started/http-post-setup https://hub.docker.com/r/toxuin/alarmserver https://community.home-assistant.io/t/dahua-ipc-to-mqtt-app/93327?page=5
- Disagree: https://hub.docker.com/r/toxuin/alarmserver: también se suscribe a Hikvision por streaming en vez de esperar el push.
- Level: core

## TH03 Tildá "Notificar al centro de vigilancia" en la vinculación del evento
- Sub-topic: T02 (also T03)
- Agree: 2 de 2. Notes: a:N1, a:N12. Urls: https://www.home-assistant.io/integrations/hikvision https://www.securitywholesalers.com.au/faqs/how-to-configure-acusense-using-hikvision-nvr-v5-0-firmware/
- Disagree: none found. Thin evidence.
- Level: core

## TH04 Por ONVIF, suscribite a los tópicos correctos o se pierden los cruces
- Sub-topic: T02 (also T16)
- Agree: 2 de 3. Notes: a:N10, a:N11. Urls: https://knowledge.keenfinity-group.com/video-systems/article/tns1-iva-does-not-include-all-iva-rules-in-camera https://ajax.systems/support/posts/line-crossing-detection-in-ajax-video-surveillance/
- Disagree: none found. Thin evidence.
- Level: advanced

## TH05 Dibujá la línea larga, lejos del borde y de lo que tapa, y elegí el sentido
- Sub-topic: T03
- Agree: 4 de 5. Notes: a:N12, a:N13, a:N15, a:N16. Urls: https://www.securitywholesalers.com.au/faqs/how-to-configure-acusense-using-hikvision-nvr-v5-0-firmware/ https://www.milesight.com/support/download/document-center/ipc-series/ai/en/user-manual/line-crossing.html https://ajax.systems/support/posts/line-crossing-detection-in-ajax-video-surveillance/ https://storage.trassir.com/manual/en/setup-line-crossing.html
- Disagree: none found
- Level: core

## TH06 En zona, ajustá tiempo mínimo adentro y tamaño del objeto, no solo sensibilidad
- Sub-topic: T03 (also T08)
- Agree: 2 de 5. Notes: a:N14, a:N17. Urls: https://global.uniview.com/res/201905/30/20190530_1728629_How-to-set-Intrusion-Detection_850805_168459_0.pdf https://www.milesight.com/support/download/document-center/ipc-series/ndaa/en/user-manual/intrusion-detection.html
- Disagree: https://ipcamtalk.com/threads/intrusion-detection-settings-does-not-work.24107: en un DVR sin clasificación ni porcentaje ni umbral sirvieron.
- Level: core

## TH07 Probá cada regla después de dibujarla, caminando la escena
- Sub-topic: T03
- Agree: 2 de 5. Notes: a:N15, a:N24. Urls: https://ajax.systems/support/posts/line-crossing-detection-in-ajax-video-surveillance/ https://videos.cctvcamerapros.com/developer/docs/getting-started/http-post-setup
- Disagree: none found
- Level: core

## TH08 Filtrá por objetivo (persona o vehículo) donde la cámara lo permita
- Sub-topic: T04 (also T08)
- Agree: 4 de 4. Notes: a:N18, a:N19, a:N31, a:N28. Urls: https://www.uniview.com/News/Blog/202605/1100575_169683_0.htm https://www.milesight.com/support/download/document-center/ipc-series/ai/en/user-manual/line-crossing.html https://ipcamtalk.com/threads/intrusion-detection-settings-does-not-work.24107 https://www.davantis.com/wp-content/uploads/perimeter-security-false-alarms-guide.pdf
- Disagree: https://www.davantis.com/wp-content/uploads/perimeter-security-false-alarms-guide.pdf: la clasificación sola falla con objetos chicos o lejanos de noche; pide apariencia más movimiento.
- Level: core

## TH09 Revisá el horario de armado: sin horario, la regla no avisa
- Sub-topic: T05
- Agree: 4 de 4. Notes: a:N20, a:N21, a:N22, a:N23. Urls: https://supportusa.hikvision.com/support/solutions/articles/17000129443-why-is-the-arming-schedule-important- https://supportusa.hikvision.com/support/solutions/articles/17000133598-what-is-the-difference-between-arming-schedule-recording-schedule- https://www.ipcamtalk.com/threads/difference-between-arming-schedule-and-recording-schedule.7096 https://www.milesight.com/support/download/document-center/ipc-series/ndaa/en/user-manual/intrusion-detection.html
- Disagree: none found
- Level: foundation
- Best story: armado de día, apagado de noche (a:N20)

## TH10 No confundas horario de grabación con horario de armado
- Sub-topic: T05
- Agree: 2 de 4. Notes: a:N21, a:N22. Urls: https://supportusa.hikvision.com/support/solutions/articles/17000133598-what-is-the-difference-between-arming-schedule-recording-schedule- https://www.ipcamtalk.com/threads/difference-between-arming-schedule-and-recording-schedule.7096
- Disagree: none found
- Level: foundation

## TH11 Cámara directa en la red, o el NVR reenvía: decidí quién avisa
- Sub-topic: T06 (also T02)
- Agree: 2 de 2. Notes: a:N7, a:N8. Urls: https://videos.cctvcamerapros.com/developer/docs/getting-started/http-post-setup https://hub.docker.com/r/toxuin/alarmserver
- Disagree: none found. Thin evidence.
- Level: core

## TH12 Probá el camino con el test y mirá el estado de conexión
- Sub-topic: T07 (also T16)
- Agree: 2 de 2. Notes: a:N24, a:N25, a:N26. Urls: https://videos.cctvcamerapros.com/developer/docs/getting-started/http-post-setup https://www.home-assistant.io/integrations/hikvision
- Disagree: none found. Thin evidence.
- Level: core

## TH13 El usuario de la cámara necesita permiso de notificar y autenticación digest
- Sub-topic: T07 (also T16)
- Agree: 1 de 2. Notes: a:N26. Urls: https://www.home-assistant.io/integrations/hikvision
- Disagree: none found. Thin evidence.
- Level: advanced

## TH14 Atacá las falsas alarmas en orden: instalación, configuración, tecnología, proceso
- Sub-topic: T08
- Agree: 4 de 5. Notes: a:N28, a:N30, a:N16, a:N15. Urls: https://www.davantis.com/wp-content/uploads/perimeter-security-false-alarms-guide.pdf https://www.uniview.com/News/Blog/202605/1100575_169683_0.htm https://storage.trassir.com/manual/en/setup-line-crossing.html https://ajax.systems/support/posts/line-crossing-detection-in-ajax-video-surveillance/
- Disagree: none found
- Level: core

## TH15 Medí las falsas por cámara y revisalas cada mes
- Sub-topic: T08 (also T13)
- Agree: 2 de 5. Notes: a:N28, a:N34. Urls: https://www.davantis.com/wp-content/uploads/perimeter-security-false-alarms-guide.pdf https://www.securitysales.com/insights/central-stations-assess-actual-alarms/147248/
- Disagree: none found
- Level: core

## TH16 No bajes falsas alarmas a costa de perder detecciones reales
- Sub-topic: T08 (also T09)
- Agree: 1 de 5. Notes: a:N29. Urls: https://www.davantis.com/wp-content/uploads/perimeter-security-false-alarms-guide.pdf
- Disagree: none found. Fuente con interés comercial.
- Level: core
- Best story: el operador de la alarma 501 (a:N29)

## TH17 Verificá con video antes de despachar y contá solo hechos
- Sub-topic: T09
- Agree: 4 de 4. Notes: a:N32, a:N34, a:N35, a:N36. Urls: https://www.sdmmag.com/articles/89047-video-monitoring-best-practices https://www.securitysales.com/insights/central-stations-assess-actual-alarms/147248/ https://www.securityinfowatch.com/home/article/10537347/seeing-is-believing https://www.davantis.com/wp-content/uploads/perimeter-security-false-alarms-guide.pdf
- Disagree: https://www.securitysales.com/insights/central-stations-assess-actual-alarms/147248/: varias centrales confían más en el contacto con el cliente (SMS, llamadas) que en el video.
- Level: core
- Best story: "Stick to the facts" (a:N32)

## TH18 Tratá varias detecciones seguidas de la misma zona como un solo episodio
- Sub-topic: T13
- Agree: 1 de 2. Notes: a:N34. Urls: https://www.securitysales.com/insights/central-stations-assess-actual-alarms/147248/
- Disagree: none found. Thin evidence.
- Level: core

## TH19 Dos zonas vecinas en poco tiempo pesan más que una: buscá el recorrido
- Sub-topic: T13
- Agree: 1 de 2. Notes: a:N35. Urls: https://www.securityinfowatch.com/home/article/10537347/seeing-is-believing
- Disagree: none found. Thin evidence.
- Level: core

## TH20 El video en vivo pasa por un servidor que adapta el RTSP al navegador
- Sub-topic: T10
- Agree: 2 de 3. Notes: a:N37, a:N38. Urls: https://pkg.go.dev/github.com/AlexxIT/go2rtc https://datatracker.ietf.org/doc/html/rfc7826
- Disagree: none found
- Level: core

## TH21 Guardá la evidencia de lo que vio el operador, con retención definida
- Sub-topic: T11
- Agree: 2 de 2. Notes: a:N33, a:N40. Urls: https://www.sdmmag.com/articles/89047-video-monitoring-best-practices https://min.io/docs/minio/linux/administration/object-management/object-lifecycle-management.html
- Disagree: none found. Thin evidence.
- Level: core

## TH22 La alarma tiene que llegar calificada y con el video a un clic
- Sub-topic: T09 (also T12)
- Agree: 2 de 4. Notes: a:N36, a:N34. Urls: https://www.davantis.com/wp-content/uploads/perimeter-security-false-alarms-guide.pdf https://www.securitysales.com/insights/central-stations-assess-actual-alarms/147248/
- Disagree: none found
- Level: core

## TH23 Avisos fuera del puesto: bot de Telegram y push del navegador
- Sub-topic: T12
- Agree: 2 de 2. Notes: a:N41, a:N42. Urls: https://core.telegram.org/bots/features https://datatracker.ietf.org/doc/html/rfc8030
- Disagree: none found. Thin evidence (definiciones).
- Level: core

## TH24 La fatiga del operador es un riesgo: menos ruido, turnos y pausas
- Sub-topic: T09 (also T15)
- Agree: 2 de 4. Notes: a:N29, a:N33. Urls: https://www.davantis.com/wp-content/uploads/perimeter-security-false-alarms-guide.pdf https://www.sdmmag.com/articles/89047-video-monitoring-best-practices
- Disagree: none found
- Level: core

## The big splits
- Filtrar en el sitio o verificar después: Davantis pide decidir en el sitio con análisis continuo; las centrales de securitysales.com confían en verificar con video y con el cliente. Depende de si hay alguien mirando en tiempo real.
- Sensibilidad o clasificación: Trassir y Milesight ponen la sensibilidad como perilla principal; el foro de ipcamtalk muestra que sin clasificación ninguna perilla alcanza. Depende de si la cámara clasifica personas y vehículos.
- Push o suscripción: cctvcamerapros enseña el push; alarmserver y el script de Dahua se suscriben. Depende de la marca: OmniAccess usa push con Hikvision y suscripción con Dahua.

## Coverage gaps
- No se consiguió en texto la documentación oficial de Hikvision sobre cruce de línea e intrusión (el centro de documentación respondió 403) ni la guía AcuSense en PDF. Se cubre con distribuidores, otros fabricantes y el código.
- No hay fuente pública sobre OmniAccess: todo lo del producto sale del código.
- Atención de alarmas en barrios privados uruguayos: sin fuente local; se usan prácticas de centrales de EE. UU.
