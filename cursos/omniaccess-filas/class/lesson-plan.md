# Plan: OmniAccess Filas, del conteo en la cámara a la alerta y el reporte

Público: técnicos de IES que instalan y mantienen OmniAccess Filas, y operadores o supervisores que miran las filas todos los días. Nivel inicial a intermedio. 10 lecciones en 3 arcos (4, 3 y 3).

Fuente de verdad: el código de OmniAccess (rama de desarrollo de octubre de 2026). Los manuales "OmniAccess Filas" del operador y del administrador están en estructura, con las secciones pendientes; donde dicen otra cosa que el código (menús, Profile M, Hikvision por ISAPI), manda el código y la tarjeta lo dice. Fuentes web: 26 páginas en raw/web (Bosch y Keenfinity para IVA Pro y RTSP, ONVIF para eventos y Profile M, go2rtc, ley de Little, BullMQ, Telegram, Web Push).

Cómo leer "N de M": M son las páginas web que tocan el subtema, N las que sostienen la idea. Muchas ideas son del producto y no tienen fuente web: la tarjeta lo aclara ("sale del código").

## Arco 1. La fila entra al sistema
Por qué este arco: antes de configurar avisos, la cámara tiene que contar bien, OmniAccess tiene que recibir sus eventos y el video tiene que verse. Cierra con una cámara de fila dada de alta, con aforo, entradas y salidas llegando y el vivo funcionando.

### Lección 1. Qué cuenta Filas
- Quién lo dice: 3 de 4 (TH01). El resto sale del código.
- Idea: OmniAccess no analiza video; la cámara Bosch con IVA Pro cuenta y OmniAccess lee sus eventos por ONVIF, los guarda, los muestra y avisa. Modo Cola exclusivo.
- Por qué importa: si el número está mal, casi siempre es la cámara; si no llega, es el camino.
- Historia: ONVIF nombró la gestión de filas como caso de uso de Profile M. https://www.onvif.org/?p=4937
- Laboratorio: Admin, 15 min. Activar Modo Cola en una demo y recorrer el menú.
- Regla: el número nace en la cámara; OmniAccess lo transporta y lo muestra.

### Lección 2. La cámara cuenta
- Quién lo dice: 1 de 2 (TH03), 2 de 4 (TH02).
- Idea: vista lo más cenital posible, más de 3 m; una zona de fila con tarea Occupancy llamada "Aforo" y tareas Entering field y Leaving field; ONVIF habilitado.
- Historia: el límite de oclusión del 50 % y la lista de Bosch. https://knowledge.keenfinity-group.com/video-systems/article/how-to-set-up-count-with-iva-pro-fw-9-40-and-get-the-data-from-the-camera
- Laboratorio: Campo, 25 min. Configuration Manager: tareas y nombres.
- Regla: la tarea de ocupación se llama Aforo.

### Lección 3. Alta del contador
- Quién lo dice: 3 de 5 (TH06), 3 de 5 (TH08).
- Idea: alta como Contador de Filas Bosch; OmniAccess hace pull point cada 5 s; verificar con Analíticas ONVIF y con el estado del sondeo; push es complemento.
- Historia: el driver de Milestone también pregunta cada 5 s y solo cuenta los Changed. https://doc.milestonesys.com/latest/en-US/onvifdriver/events.htm
- Laboratorio: Foco, 20 min. Alta y verificación con /api/queue/poll?info=1.
- Regla: no doy por instalada una fila hasta ver un cambio de aforo llegar.

### Lección 4. Video en vivo
- Quién lo dice: 2 de 3 (TH10), 1 de 3 (TH11).
- Idea: go2rtc toma el RTSP de la cámara (stream bosch_<ip>) y lo entrega como MP4 por HTTP; sin ese stream no hay vivo ni clip.
- Historia: los parámetros inst y rtsp_tunnel de Bosch. https://knowledge.keenfinity-group.com/video-systems/article/how-is-rtsp-usage-supported-with-bosch-vip-devices
- Laboratorio: Foco, 20 min. Agregar el stream y probarlo.
- Regla: el nombre del stream es bosch_ y la IP con guiones bajos.

## Arco 2. Que avise bien
Por qué este arco: un aforo que parpadea genera alertas falsas y un aviso que no sale no sirve. Cierra con la fila calibrada, reseteada a la apertura, con umbral y con al menos un canal probado.

### Lección 5. Calibrar el aforo
- Quién lo dice: 1 de 2 (TH12). Sale casi todo del código.
- Idea: Señal del aforo mide el parpadeo y sugiere rebote; el editor escribe zona, rebote, ventana anti doble conteo y aforo crítico en la cámara, con backup.
- Laboratorio: Foco, 20 min.
- Regla: primero medir, después tocar, y siempre con backup.

### Lección 6. Horarios y umbrales
- Quién lo dice: 2 de 2 (TH13); umbrales del código.
- Idea: reseteo a la apertura con Horarios de Filas; umbral con cooldown; estados OK, Alto y Lleno; escalamiento a los 5 minutos.
- Historia: Axis no resetea los cruces si nadie lo programa. https://developer.axis.com/analytics/axis-object-analytics-counting-data
- Laboratorio: Admin, 15 min.
- Regla: una alerta por fila, con el umbral que el cliente firmó.

### Lección 7. Canales y despachos
- Quién lo dice: 1 de 4 (TH15), 3 de 4 (TH17).
- Idea: canales en Notificaciones, destinatarios, reglas; todo pasa por una cola con reintentos y se ve en Despachos.
- Historia: el backoff exponencial de BullMQ. https://docs.bullmq.io/guide/retrying-failing-jobs
- Laboratorio: Admin, 20 min.
- Regla: un canal no está configurado hasta que llegó la prueba.

## Arco 3. Operar la fila
Por qué este arco: el operador vive en el monitor, en la alerta y en el reporte del día. Cierra con un turno simulado: leer la fila, atender una alerta y mandar el reporte.

### Lección 8. Monitor y espera
- Quién lo dice: 3 de 4 (TH18), 2 de 4 (TH19).
- Idea: Monitor en Vivo, Filas, Flujo y Kiosko; la espera estimada es aforo dividido por el ritmo de salida de los últimos 15 minutos (Little).
- Historia: Little probó la ley en 1961. https://en.wikipedia.org/wiki/Little%27s_law
- Laboratorio: Rápido, 15 min.
- Regla: la espera estimada es un promedio, no una promesa.

### Lección 9. Atender la alerta
- Quién lo dice: código; 1 web (TH20).
- Idea: aviso con foto, sonido, push y escalamiento; primero mirar la imagen, después actuar; cámara tapada y cortes.
- Laboratorio: Foco, 15 min. Práctica guiada.
- Regla: miro la foto antes de llamar al supervisor.

### Lección 10. Reportes programados
- Quién lo dice: código; 1 web (TH21).
- Idea: Reportes de Afluencia con exportación y reportes programados por Telegram; los cortes de cámara explican huecos.
- Historia: Little a los 50 años, intervalos finitos. https://projectproduction.org/journal/reprint-littles-law-as-viewed-on-its-50th-anniversary/
- Laboratorio: Admin, 15 min.
- Regla: un reporte sin la lista de cortes cuenta media historia.

## Divisiones
- Espera estimada: Little con salidas (OmniAccess) o tiempo medio de servicio (FootfallCam). Decidir: con salidas bien contadas, Little; si la zona de salida es mala, mirar la espera como tendencia.
- Ángulo: cenital (Bosch) o cámara existente (venta). Decidir: si la cámara existente no ve la fila de arriba, cotizar una dedicada.
- Push o pull: pull por defecto; push solo si la cámara llega al servidor y se probó con varias cámaras.

## Huecos
- Manuales del producto pendientes; menús y nombres salen del código.
- Manual IVA Pro y white paper de conteo de Bosch: enlaces caídos.
- Hikvision por ISAPI: el manual lo menciona, el código de Filas solo sondea cámaras Bosch.
