# Subtemas: OmniAccess Filas (control de filas y aforo)

Fuente de verdad del producto: código de OmniAccess (Infratec), rama de desarrollo de octubre de 2026, y los manuales filas-operador / filas-administrador (todavía en estructura, con secciones pendientes). Las fuentes web cubren el hardware (Bosch IVA Pro), los estándares (ONVIF, RTSP, Web Push) y la teoría (ley de Little).

- T01 Qué resuelve el control de filas y aforo: modo Cola (MODULE_QUEUE), qué pantallas aparecen, flujo cámara → evento → monitor → alerta.
- T02 Analíticas de video en la cámara: IVA / IVA Pro de Bosch, tareas Occupancy y Counter, Entering/Leaving field, limitaciones (oclusión, altura, ángulo).
- T03 Planificar la cámara de conteo: vista cenital, altura, reflejos, cantidad de personas, pasillos rectos.
- T04 ONVIF: historia, perfiles S/T/M, Profile M para analíticas y conteo.
- T05 Eventos ONVIF: PullPoint (CreatePullPointSubscription, PullMessages, Renew), Basic Notification (Subscribe/Notify), PropertyOperation Initialized/Changed/Deleted, tópicos.
- T06 Alta del contador en OmniAccess: Dispositivos Conteo, tipo QUEUE_COUNTER, Bosch, verificación con Analíticas ONVIF (reglas VCA, tópicos, descubrimiento).
- T07 Video en vivo: RTSP de Bosch (inst, line, rtsp_tunnel), go2rtc (go2rtc.yaml, puertos 1984/8554, stream.mp4), proxy y respaldo por captura.
- T08 Calibración del aforo: ruido del conteo, rebote (debounce), ventana anti doble conteo, aforo crítico, backups de configuración.
- T09 Horarios y reseteo de contadores: Horarios de Filas, Reset ahora, tick por cron, zona horaria.
- T10 Umbrales y alertas de aforo: QueueAlert (umbral, cooldown), estados OK/Alto/Lleno, escalamiento al supervisor, alertas de salud de cámara.
- T11 Canales y despachos: Telegram, WhatsApp (OpenWA), Web Push (VAPID), reglas de notificación, cola con reintentos (BullMQ), Despachos, clip animado.
- T12 Monitor de filas y lectura en sala: Monitor en Vivo, Filas, Flujo de Filas, Pantalla / Kiosko, PWA de filas.
- T13 Tiempo de espera: ley de Little, cómo lo estima OmniAccess, límites de la estimación.
- T14 Atender una alerta: aviso en pantalla, push, escalamiento, cortes de cámara, cámara tapada o a oscuras.
- T15 Reportes: afluencia por intervalo, día, semana y mes; exportación Excel/PDF; reportes programados; cortes en el período.
- T16 Diagnóstico: estado del polling, push vs pull, procesos, go2rtc, cola de despachos.
