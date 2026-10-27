# Mapa de acuerdos: OmniAccess Filas

M cuenta las páginas de raw/web con notas en el subtema. El comportamiento del producto no sale de la web: sale del código (research/notes/codigo.md), y cada tema lo indica.

## TH01 Contá con la cámara, no con el servidor
- Sub-topic: T02 (also T05)
- Agree: 3 de 4. Notes: a:N1, a:N6, a:N7, a:N9. Urls: https://knowledge.keenfinity-group.com/video-systems/article/how-to-set-up-count-with-iva-pro-fw-9-40-and-get-the-data-from-the-camera, https://media.boschsecurity.com/fs/media/pb/media/partners_1/integration_tools_1/developer/Bosch-Metadata-and-IVA-Events.pdf, https://developer.axis.com/analytics/axis-object-analytics-counting-data
- Disagree: https://www.footfallcam.com/blog/2024/03/redefining-queue-analytics-a-big-data-modelling-approach/: el conteo individual nunca es perfecto y conviene modelar estadísticamente.
- Level: foundation
- Código: OmniAccess no analiza video; lee los eventos de la cámara (c:3, c:4).
- Best story: el límite del 50 % de oclusión de Bosch.

## TH02 Separá ocupación (cuántos hay) de cruces (cuántos pasaron)
- Sub-topic: T02
- Agree: 2 de 4. Notes: a:N1, a:N9. Urls: https://knowledge.keenfinity-group.com/video-systems/article/how-to-set-up-count-with-iva-pro-fw-9-40-and-get-the-data-from-the-camera, https://developer.axis.com/analytics/axis-object-analytics-counting-data
- Disagree: none found
- Level: foundation
- Código: canal de aforo = regla Occupancy; Entrada / Salida = Entering / Leaving field (c:4).

## TH03 Poné la cámara alta y lo más cenital posible
- Sub-topic: T03
- Agree: 1 de 2 (thin evidence). Notes: a:N10, a:N11. Urls: https://knowledge.keenfinity-group.com/video-systems/article/how-to-set-up-count-with-iva-pro-fw-9-40-and-get-the-data-from-the-camera
- Disagree: el manual de OmniAccess promete usar "las mismas cámaras del lugar"; en obra se reutiliza la cámara existente.
- Level: core

## TH04 Nombrá la tarea de ocupación como el sistema la espera ("Aforo")
- Sub-topic: T02 (also T06)
- Agree: 1 de 1 en web (el nombre de la regla viaja en el evento). Urls: https://media.boschsecurity.com/fs/media/pb/media/partners_1/integration_tools_1/developer/Bosch-Metadata-and-IVA-Events.pdf
- Código: espera estimada, reporte diario y reset usan el canal "Aforo" (c:4, c:29, c:32).
- Level: core

## TH05 ONVIF es el idioma común; Profile M es el de las analíticas
- Sub-topic: T04
- Agree: 4 de 5. Urls: https://www.onvif.org/profiles/profile-m/, https://www.onvif.org/?p=4937, https://en.wikipedia.org/wiki/ONVIF, https://docs.edgexfoundry.org/3.2/microservices/device/services/device-onvif-camera/supplementary-info/api-analytic-support/
- Disagree: Bosch exige pasos manuales (metadata en el perfil) para que la analítica aparezca por ONVIF: https://media.boschsecurity.com/fs/media/pb/media/partners_1/integration_tools_1/developer/Bosch-Metadata-and-IVA-Events.pdf
- Level: foundation

## TH06 Pull point: el servidor pregunta, la cámara contesta
- Sub-topic: T05
- Agree: 3 de 5. Notes: a:N19, a:N22, a:N24. Urls: https://www.onvif.org/specs/2606/ONVIF-Core-Spec-v2606.pdf, https://doc.milestonesys.com/latest/en-US/onvifdriver/events.htm, https://docs.edgexfoundry.org/3.2/microservices/device/services/device-onvif-camera/supplementary-info/api-event-handling/
- Disagree: none found
- Level: core
- Código: pull cada 5 s, suscripción de 300 s (c:3).

## TH07 Push: la cámara avisa sola, pero hay que renovar y que la cámara llegue al servidor
- Sub-topic: T05
- Agree: 2 de 5. Urls: https://www.onvif.org/specs/2606/ONVIF-Core-Spec-v2606.pdf, https://docs.edgexfoundry.org/3.2/microservices/device/services/device-onvif-camera/supplementary-info/api-event-handling/
- Level: advanced
- Código: push opcional con ONVIF_PUSH_URL; camino reducido (c:6).

## TH08 Contá cambios, no repeticiones (Initialized vs Changed)
- Sub-topic: T05
- Agree: 3 de 5. Urls: https://www.onvif.org/specs/2606/ONVIF-Core-Spec-v2606.pdf, https://doc.milestonesys.com/latest/en-US/onvifdriver/events.htm, https://forum.milestonesys.com/t/the-onvif-pull-point-event-is-raised-redundantly-by-the-onvif-driver/13473
- Disagree: el foro muestra servidores que repiten el valor sin PropertyOperation.
- Level: core
- Código: graba solo cuando el valor cambia (c:5).

## TH09 Suscribite a los tópicos correctos (tns1:IVA y tns1:RuleEngine)
- Sub-topic: T05 (also T16)
- Agree: 1 de 5 (thin evidence). Urls: https://knowledge.keenfinity-group.com/video-systems/article/tns1-iva-does-not-include-all-iva-rules-in-camera
- Level: advanced

## TH10 Pedí el segundo stream para el vivo
- Sub-topic: T07
- Agree: 2 de 3. Urls: https://knowledge.keenfinity-group.com/video-systems/article/how-is-rtsp-usage-supported-with-bosch-vip-devices, https://pkg.go.dev/github.com/AlexxIT/go2rtc
- Level: core
- Código: guía con inst=2 para el vivo (c:12).

## TH11 Un relevo de video en el medio (go2rtc) evita que cada navegador le pegue a la cámara
- Sub-topic: T07
- Agree: 1 de 3 (thin evidence). Urls: https://pkg.go.dev/github.com/AlexxIT/go2rtc
- Código: stream bosch_<ip>, MP4 por HTTP, anillo para clips (c:12, c:13, c:14).
- Level: core

## TH12 Calibrá con datos: rebote y ventana contra el parpadeo
- Sub-topic: T08
- Agree: 1 de 2 (thin evidence). Urls: https://knowledge.keenfinity-group.com/video-systems/article/how-to-set-up-count-with-iva-pro-fw-9-40-and-get-the-data-from-the-camera
- Código: Señal del aforo y editor Bosch con backups (c:15, c:16).
- Level: core

## TH13 Reseteá los acumulados con un horario
- Sub-topic: T09
- Agree: 2 de 2. Urls: https://knowledge.keenfinity-group.com/video-systems/article/how-to-set-up-count-with-iva-pro-fw-9-40-and-get-the-data-from-the-camera, https://developer.axis.com/analytics/axis-object-analytics-counting-data
- Código: Horarios de Filas y cron (c:21).
- Level: core

## TH14 Umbral con período de calma
- Sub-topic: T10
- Agree: código (c:17, c:18, c:19). En web, Bosch ofrece alarma por "critical value": https://knowledge.keenfinity-group.com/video-systems/article/how-to-set-up-count-with-iva-pro-fw-9-40-and-get-the-data-from-the-camera
- Level: core

## TH15 Encolá los avisos y reintentá
- Sub-topic: T11
- Agree: 1 de 4 en web. Urls: https://docs.bullmq.io/guide/retrying-failing-jobs
- Código: DispatchJob, 5 intentos, backoff exponencial (c:24).
- Level: core

## TH16 Telegram baja la foto de una URL pública
- Sub-topic: T11
- Agree: 1 de 4. Urls: https://core.telegram.org/bots/api
- Código: PUBLIC_BASE_URL (c:24).
- Level: advanced

## TH17 Web Push necesita claves VAPID y un service worker
- Sub-topic: T11
- Agree: 3 de 4. Urls: https://datatracker.ietf.org/doc/html/rfc8030, https://pushpad.xyz/blog/web-push-what-is-vapid/, https://developer.mozilla.org/en-US/docs/Web/API/Push_API
- Level: core

## TH18 La espera es largo de fila dividido por el ritmo de salida (Little)
- Sub-topic: T13
- Agree: 3 de 4. Urls: https://third-bit.com/2026/05/30/littles-law/, https://en.wikipedia.org/wiki/Little%27s_law, https://projectproduction.org/journal/reprint-littles-law-as-viewed-on-its-50th-anniversary/
- Disagree: https://www.footfallcam.com/blog/2024/03/redefining-queue-analytics-a-big-data-modelling-approach/: usa tiempo medio de servicio y largo medio.
- Código: aforo × 15 / salidas de 15 min (c:29).
- Level: core

## TH19 La estimación solo vale con la fila estable
- Sub-topic: T13
- Agree: 2 de 4. Urls: https://third-bit.com/2026/05/30/littles-law/, https://en.wikipedia.org/wiki/Little%27s_law
- Level: core

## TH20 Atendé la alerta mirando la imagen antes de reaccionar
- Sub-topic: T14
- Agree: código (c:20, c:7). Web: ningún contador es exacto: https://www.footfallcam.com/blog/2024/03/redefining-queue-analytics-a-big-data-modelling-approach/
- Level: core

## TH21 Los reportes miden picos, horas críticas y cortes
- Sub-topic: T15
- Agree: código (c:31, c:32). Web: Little en intervalos finitos: https://projectproduction.org/journal/reprint-littles-law-as-viewed-on-its-50th-anniversary/
- Level: core

## The big splits
- Cómo estimar la espera: Little con salidas (OmniAccess, third-bit) contra tiempo medio de servicio (FootfallCam). Gira en qué dato es más confiable en la obra.
- Ángulo de cámara: Bosch pide cenital; la venta promete reutilizar cámaras del lugar.
- Push o pull: la especificación ofrece los dos; OmniAccess usa pull como principal y push como complemento.

## Coverage gaps
- No hay documentación pública de OmniAccess: todo lo del producto sale del código.
- El manual IVA Pro completo y el white paper de conteo de Bosch no se pudieron descargar (enlaces caídos); se usó la nota técnica de Keenfinity.
- No hay fuente web sobre las alertas de sabotaje de Bosch por ONVIF (GlobalSceneChange, ImageTooBright, ImageTooDark).
