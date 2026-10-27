# Notes: batch b (el producto: código de OmniAccess, octubre de 2026)
Fuente: copia de solo lectura del código vigente. No se cita por URL en las tarjetas: se nombra la pantalla. Los manuales del producto no tienen capítulo de intrusión; donde el manual del instalador o del administrador toca algo vecino, se anota.

## T01 Qué entra y qué no
- b:N1. Tipos de detección guardados (modelo Detection): LINECROSS "Cruce de línea", INTRUSION "Intrusión" (en la alerta global "Intrusión en zona"), REGION_ENTER "Entra a zona", REGION_EXIT "Sale de zona", MOTION "Movimiento", OTHER "Evento".
- b:N2. Hikvision (proceso webhooks, server.js): el XML de la cámara se clasifica por eventType: linedetection → LINECROSS, fielddetection → INTRUSION, regionentrance → REGION_ENTER, regionexiting → REGION_EXIT. vmd y motiondetection (movimiento simple) se descartan: no se guardan, no se emiten y no se captura foto, porque saturaban el sistema.
- b:N3. La cámara se identifica por la MAC o la IP que vienen en el XML. Si no está dada de alta, la detección queda sin cámara (deviceId vacío): no aparece en ningún canal ni arma alarma.
- b:N4. Clase del objeto: si la cámara AcuSense la manda (DetectionRegionList, detectionTarget), se guarda label human o vehicle y se muestra "Persona" o "Vehículo/Auto".
- b:N5. Dahua (dahua-events.js): no hay push por cámara. El proceso webhooks abre una suscripción permanente a cada NVR Dahua: `/cgi-bin/eventManager.cgi?action=attach&codes=[CrossLineDetection,CrossRegionDetection,IntrusionDetection]&heartbeat=20`. CrossLineDetection → LINECROSS; CrossRegionDetection e IntrusionDetection → INTRUSION. Repite el mismo canal y tipo como máximo cada 8 segundos. Si se corta, reintenta a los 5 s. Por Dahua no llega clase de objeto.
- b:N6. ONVIF: en esta versión no hay ingesta de eventos de intrusión por ONVIF (el sondeo ONVIF del código es para el conteo de Filas con Bosch). Una cámara de otra marca grabada en un NVR Dahua llega igual, porque el que analiza y avisa es el NVR.
- b:N7. Caso sin vía: cámara Dahua grabada por un NVR Hikvision. Mensaje del sistema: el NVR Hikvision no analiza canales de otra marca; los eventos se configuran en la propia cámara o se pasa la cámara a un NVR Dahua.
- b:N8. Al llegar una detección: se guarda, se emite por socket (general_detection) a todas las pantallas abiertas y, si no es movimiento, se pide la foto directo a la cámara (Hikvision `/ISAPI/Streaming/channels/101/picture`, Dahua `/cgi-bin/snapshot.cgi?channel=1`, puerto 80, credenciales de la cámara, 3,5 s de espera) y se sube al bucket "intrusion" de MinIO. Cuando llega la foto se emite detection_snapshot.
- b:N9. Sin foto propia, el panel muestra un cuadro de la grabación del NVR en ese instante (/api/nvr/cuadro): "Buscando el cuadro en la grabación…". Si tampoco: "Sin captura del evento".

## T02 El aviso de la cámara: Servidor de alarma
- b:N10. Hikvision: OmniAccess se agrega como servidor de alarma por ISAPI (`/ISAPI/Event/notification/httpHosts`), protocolo HTTP, formato XML, sin autenticación, a la IP, puerto y ruta del "host de eventos" (ajustes EVENT_HOST_IP, EVENT_HOST_PORT por defecto 10000, EVENT_HOST_PATH por defecto /api/webhooks/hikvision). Usa un lugar libre (0.0.0.0) o el siguiente; no borra los otros servidores.
- b:N11. Sin host de eventos cargado: "Falta configurar el host de eventos de OmniAccess (Settings EVENT_HOST_IP)". En esta versión no hay pantalla para cargarlo: se deja al instalar el servidor.
- b:N12. Diálogo "Servidor de alarma" (ícono campana del canal, o menú "Alertas"): lista "Servidores de alarma en el equipo", estado "OmniAccess presente" u "OmniAccess no configurado"; botones "Configurar OmniAccess como alarma", "Probar reporte", "Reescribir config". Resultado del test: "El equipo reporta OK a OmniAccess ✓" o "Test enviado; el equipo no confirmó explícitamente (revisá que lleguen eventos)". Varios NVR y cámaras no implementan el test activo.
- b:N13. Dahua en el mismo diálogo: "Recepción de eventos (Dahua)", "Suscripción activa" o "NVR no accesible", botón "Verificar suscripción"; no escribe nada en la cámara.
- b:N14. Ojo: el diálogo muestra un "Destino OmniAccess" fijo escrito en el código, no el host de eventos real. Es solo informativo y puede no coincidir con la instalación.
- b:N15. El ícono de campana queda verde ("Servidor de alarma activo (recibiendo OK)") según un registro de IPs con aviso confirmado (ALARM_CONFIGURED_IPS).

## T03 La regla: calibrador de intrusión
- b:N16. Calibrador ("Calibrar líneas y zonas", ícono regla y lápiz en el canal, o "Calibrar" en Dispositivos): controles Línea, Zona, Sentido, Sensibilidad, Objetivo, Servidor, Probar, y botón "Auto-perfil · Perímetro recomendado" (sensibilidad 60, objetivo personas y vehículos, aviso a OmniAccess; "Es reversible").
- b:N17. Línea: "tocá los 2 extremos, arrastrá para ajustar"; Zona: "tocá para agregar vértices, doble clic borra"; botones Limpiar, Revertir, Cerrar, Guardar. Sentido: A→B, Ambos, B→A (en la cámara left-right, any, right-left). La línea necesita 2 puntos y la zona al menos 3.
- b:N18. Sensibilidad rota entre 40, 60 y 80. Texto de ayuda: "En perímetro con vegetación, 40–60 suele ser el equilibrio". Objetivo: Persona, Vehículo, Ambos; solo en cámaras que lo soportan: "esta cámara no filtra por objetivo".
- b:N19. Todo se escribe EN LA CÁMARA por ISAPI (`/ISAPI/Smart/LineDetection/1` y `/ISAPI/Smart/FieldDetection/1`) leyendo el XML y cambiando solo lo necesario. Coordenadas de 0 a 1000 con origen abajo a la izquierda. Si la cámara no soporta: "Esta cámara no tiene cruce de línea ni zona de intrusión: sólo se puede configurar el aviso a OmniAccess."
- b:N20. Para canales detrás de un NVR Dahua la geometría se lee y escribe en el NVR (IVS por configManager). Sensibilidad y objetivo son de Hikvision.
- b:N21. Una sola regla de cada tipo por cámara: lineDetection-1 y fieldDetection-1 (canal 1).

## T05 Horario de armado
- b:N22. El horario vive en la cámara, por regla: `/ISAPI/Event/schedules/lineDetections/lineDetection-1` y `.../fieldDetections/fieldDetection-1`. Bloques por día (1 lunes a 7 domingo), "24:00" es fin de día; un rango que cruza medianoche se guarda como dos bloques.
- b:N23. OmniAccess lo lee y lo muestra en palabras: "Siempre", "Nunca (desarmada)", "L–D 22:00–06:00". Resumen en cada canal de la vista de pared: "línea ... zona ..." con punto verde (armada ahora) o ámbar (desarmada ahora), "armado: sin dato" si no hay lectura. Lectura con caché de 5 minutos.
- b:N24. Está escrito el editor "Horario de armado" (presets Siempre, Noche 22:00 a 06:00, Fuera de horario 18:00 a 08:00, Personalizado; mapa semanal; "Armar con este horario") pero en esta versión no está montado en ninguna pantalla y su ruta de guardado (/api/intrusion/horarios) no existe. A medio hacer: el horario se cambia en la web de la cámara o del NVR.
- b:N25. Texto del producto: "Fuera del horario la cámara sigue grabando en el NVR, pero no avisa nada: ni cruce, ni zona, ni foto."
- b:N26. Mapa del barrio: cada línea o zona dibujada en el mapa puede tener "Horario de armado" propio (De, a, "Alertar: todo / solo persona / solo auto"). "Sin horario = siempre armada. Fuera de la franja la geometría queda dormida (gris)." "Fuera de ese rango/clase, no suena ni parpadea (igual queda en el historial)." Solo afecta al mapa; no toca la cámara.

## T06 Alta del equipo
- b:N27. Dispositivos (menú lateral; el manual lo llama "Dispositivos LPR"): botón Agregar con alta guiada, primero se elige el tipo: "Cámara LPR", "Cámara de intrusión" ("Vigila el perímetro con cruce de línea o zona. Sus alarmas van al monitor de intrusión.") o "NVR / Grabador". Pasos de la cámara de intrusión: Equipo, Conexión, Grabación, Puesta a punto.
- b:N28. Puesta a punto de una cámara de intrusión: Dar de alta la cámara; Poner la hora; Servidor de alarmas → OmniAccess; Video en vivo (stream en go2rtc); Vincular la grabación (NVR y canal); Calcular retención.
- b:N29. NVR: "Importar cámaras (clasificar)": cada canal con miniatura, marca y protocolo; rol LPR, intrusión u omitir; las existentes solo se vinculan a su canal; el sistema sugiere LPR si el nombre habla de matrícula, patente, entrada, salida, acceso o barrera, y si no "cámara del perímetro". Las cámaras creadas así toman usuario y clave del NVR.
- b:N30. Vista Dispositivos → Intrusión (tabla de cámaras de intrusión): "N cámaras", "con analítica", "avisan a OmniAccess"; por fila NVR y canal, "Configurada" o "Sin analítica", "Avisa" o "Sin confirmar", "En línea" o "Sin respuesta"; botones Calibrar, Historial de salud, Editar, Quitar de OmniAccess ("la cámara y su grabación en el NVR no se tocan").
- b:N31. El menú "Monitor Intrusión" aparece cuando el sistema tiene el módulo LPR y no está en modo Filas. Permiso de rol "Monitor de intrusión".
- b:N32. Una cámara se trata como PTZ si su nombre contiene "PTZ".
- b:N33. Manual del instalador: "Grabación y NVR, Mapeo de canales" y "La hora": cámaras, NVR y servidor con la misma hora; Dispositivos → Sincronizar hora.

## T09 Atender
- b:N34. Monitor de Intrusión (panel, /admin/monitor-intrusion): encabezado "Cruce de línea, intrusión, zonas y movimiento · N canales", buscador "Buscar canal…", "En vivo", botones Historial y Evidencia, filtro Intrusión / Movimiento / Todo. Mosaico de canales con línea (celeste) y zona (rosada) dibujadas encima; fila fija "Actividad reciente" con los 3 primeros; a la derecha la franja "Detecciones".
- b:N35. Orden: canal con alarma sin aceptar siempre arriba; después detección en el último minuto; después los que tienen analítica.
- b:N36. Canal en alarma: se pone rojo y late, con "<tipo> detectada · hace N s" (hasta 3, "+N evento(s) más"); al pasar el mouse "Aceptar alarma" o "Aceptar N alarmas". Aceptar abre la ficha del evento (misma que la franja) con "Falsa alarma (F)" y "Confirmar real (A)". Teclas: flechas para recorrer eventos de la cámara, A o Enter real, F o R falsa, Esc cerrar.
- b:N37. Confirmar real: la cámara queda "En atención" (borde animado y botón "Resolver") hasta que alguien la resuelve. Falsa alarma: se archiva como falsa. La decisión aplica a TODAS las detecciones sin aceptar de esa cámara de las últimas 6 horas. Las alarmas sin aceptar se reconstruyen al recargar (últimas 6 horas).
- b:N38. Vista de pared Intrusión (/monitor/intrusion): "En foco" (hasta 12 cámaras), "El resto del perímetro", franja "Últimas detecciones" con filtros Todas, Sin confirmar, Con alguien, Reales, Falsas. Canal en alarma con rótulo "Intrusión detectada" o "Intrusión confirmada". Ficha de la cámara: "Falsa alarma" y "Es real: la atiendo"; confirmada: "Era falsa alarma" y "Resuelta". Ficha de la detección: "Era falsa alarma" / "Fue real" para corregir UNA. Las fichas se cierran solas al minuto.
- b:N39. Un enlace de pantalla es de solo lectura; decide solo quien entró al panel con permiso de intrusión.
- b:N40. "Era falsa alarma" sobre una confirmada reclasifica como falsas las aceptadas como reales de esa cámara en las últimas 6 horas.
- b:N41. Hay un modal viejo que confirmaba solo a los 20 s ("Confirmar alarma"); ya no se usa desde el 3/10 (openspec). El comentario de reclasificarComoFalsa todavía lo menciona.
- b:N42. La "alerta global" (ventana roja en toda la app, "Intrusión · requiere confirmación", "Intrusión real: la atiendo") está escrita para el panel pero en esta versión solo se monta en las pantallas de pared (Rotación, Resumen, Salud); en Control LPR e Intrusión no se muestra. En la pared se puede cerrar con la X y queda una píldora "N cámaras con intrusión sin resolver · Ver".

## T10 Video
- b:N43. "Ver en vivo (incluye grabación y evidencia)": pestañas Vivo, Grabación, Evidencia. Vivo por go2rtc (stream lpr_<id> sub, lpr_<id>_hd principal), botón SD/HD, "En vivo", "Conectando…", "Reconectando…". PTZ: arrastrar, rueda para zoom, flechas del teclado.
- b:N44. Seguimiento visual: "Editar seguimiento visual (enlaces entre cámaras)", "Agregar cámara", "Arrastrá cada ícono al punto de la escena por donde se pasa a esa cámara. Al verlo en vivo, tocá el ícono para seguir al intruso." El ícono rebota en rojo si esa cámara tiene eventos.
- b:N45. Grabación: línea de tiempo de 24 h con zoom, velocidad 1/2/4/8, eventos marcados; "Sin grabación en este horario". Requiere NVR y canal vinculados. "Descargar o enviar por WhatsApp" (10 s antes y 10 s después por defecto), con intro; por WhatsApp a destinatarios del Centro de Notificaciones o a un usuario, con un máximo de segundos.
- b:N46. Los NVR que graban en H.265 se reproducen transcodificando en el servidor (openspec, 3/10).

## T11 Registro
- b:N47. Historial ("Historial de intrusión"): filtros Intrusión+, Intrusión, Línea, Movim., Todo; columnas Evento, Cámara, NVR · Canal, Fecha; 40 por página.
- b:N48. Evidencia: grilla con filtros Buscar (cámara o NVR), Tipo de evento, Cámara, Estado (Todas, Pendientes, Revisadas), Rango de fechas (Desde, Hasta); estado de cada tarjeta Pendiente, Real o Falsa; al dejar el mouse 3 s reproduce el clip; Resumen con Total, Pend., Revis. y por tipo.
- b:N49. Bucket de fotos "intrusion" compartido en todos los modos; retención en Configuración → Almacenamiento ("Bucket Intrusión", políticas de retención). Manual del administrador: retención típica de fotos 30 días.

## T12 Avisos
- b:N50. Panel: el aviso es visual en el Monitor Intrusión (canal rojo) y en el Mapa. El Mapa suena (pitido distinto para persona) y habla ("Persona en <cámara>"), con "Silenciar alertas", "Feed de intrusiones" e indicador "INTRUSIÓN ACTIVA" o "SISTEMA ARMADO · N hoy". Tocar la línea o zona roja ("tocá para aceptar") abre la ficha con Real, Falsa alarma y ver grabación.
- b:N51. Pantallas de pared (menú Monitores): vista Intrusión con sonido "Sin sonido", "Un tono por alarma" o "Repetir hasta que se acepte"; Rotación "se queda en Intrusión hasta que se resuelva"; enlaces de pantalla con token; Chrome en modo kiosco para que suene sin primer toque; si no, "Tocá la pantalla para habilitar el sonido y la pantalla completa".
- b:N52. Telegram: el monitoreo de salud manda "ALERTA · <equipo>" y "NORMALIZADO · <equipo>" (sin respuesta, disco, memoria, reloj). Las reglas de Notificaciones y la cola de Despachos (NotificationRule, DispatchJob, dispatch-worker) en esta versión solo manejan Filas (aforo) y reportes: no hay regla de intrusión por Telegram, WhatsApp ni push. El texto del producto menciona "el bot" y avisos retenidos por omni-vision, pero eso no está en esta rama.
- b:N53. omni-vision (verificación por visión de la captura: "Confirmada", "Hay alguien", "Animal", "No se ve a nadie") está desactivado en esta versión: la función devuelve vacío ("sin omni-vision, sin GPU"). El filtro "Con alguien" de la pared queda en cero.

## T13 Análisis
- b:N54. Ficha → "Análisis" ("Mirando alrededor de esta detección…"): tres cifras (detecciones en el episodio, hoy en esta cámara, % de falsas en esta cámara o "pocas revisadas aún") e indicios con color: clase; ráfaga (±5 min, "es un mismo episodio, no N intrusiones"); "Fue de noche" (22 a 06); "Más movimiento que lo habitual" (3 o más y más de 3 veces el promedio de la misma hora de los 7 días previos); historial (de las últimas 50 revisadas, con 5 o más; 70 % o más falsas en verde, 30 % o menos en rojo); otras cámaras en ±3 min ("puede ser un recorrido"); lecturas LPR en ±3 min.
- b:N55. "No da un veredicto ... la decisión la tome alguien con la foto delante."
- b:N56. "Dónde fue el cruce": recuadro satelital con la cámara (azul), su línea o zona (rojo) y otras cámaras que detectaron (ámbar). Sale del Mapa del barrio: hace falta la cámara ubicada en el mapa y su línea o zona dibujada ahí.

## T14 Mapa
- b:N57. Mapa (menú lateral): capa "Cruces / Zonas"; en edición, "Cruces de línea" y "Zonas de intrusión" listan solo cámaras con analítica configurada; por cámara Dibujar o Redibujar, Sugerir (según la orientación de la cámara), Ver, borrar, sentido de la flecha, horario. Aviso "Desactualizada: la analítica cambió en la cámara, redibujá". Colores: zona ámbar, línea azul, gris punteado dormida, roja titilando en alarma.

## T15 Guardia
- b:N58. La consola del guardia (tablet) no recibe alarmas de intrusión en esta versión. Lo que sí: posición en el Mapa (cada 10 s con la app en pantalla, 30 s con la pantalla apagada en Android), botón de pánico (mantener 1,5 s), registro. El puesto ve a los guardias en el Mapa y los coordina por radio.

## T16 Diagnóstico
- b:N59. Salud: Dispositivos (estado, latencia, hora), vista de pared "Salud del sistema"; alertas DeviceAlert (sin respuesta tras dos sondeos, disco, memoria 95 %, reloj con más de 2 minutos) con Telegram.
- b:N60. Proceso de webhooks en el puerto 10000 (pm2 "omniaccess-webhooks"); el panel en otro proceso. Manual del instalador: "Configuración → Avanzado → Monitor de webhooks" para ver qué llega.
- b:N61. Manual del instalador, servicios: Aplicación web, Webhooks, Base de datos, Almacenamiento, Servidor de video, Cola de despacho; reiniciar el servidor una vez antes de entregar.
