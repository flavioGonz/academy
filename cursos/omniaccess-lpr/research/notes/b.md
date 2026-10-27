# Notes: batch b (producto: manuales OmniAccess LPR 2026.09 y código de octubre 2026)
Fuentes: Manual del Operador, Manual del Administrador, Manual del Instalador, Guía rápida, HIKVISION_SETUP, ANALISIS_PROBLEMAS_LPR, ANALISIS_OCR_PWA, OCR_CLIENT_SIDE_FINAL, README y código (server.js, handlers, src/app/admin, src/app/api, src/lib, prisma). Se citan por nombre, sin URL. Cuando manual y código difieren manda el código (lista al final).

## T02 Arquitectura
- b:N1. Piezas: servidor OmniAccess en el predio (contenedor o VM Linux), cámaras ANPR que leen a bordo y envían por HTTP, NVR que graba 24/7, PostgreSQL, MinIO (fotos y clips, buckets como `lpr`), go2rtc (RTSP al navegador), tablets. (Manual del Instalador, "Qué se instala")
- b:N2. Procesos: web y API en el puerto 10001; receptor de webhooks y Socket.io en el 10000; go2rtc en 1984; worker de despacho con Redis. Las cámaras Hikvision van al 10000, la ruta Next del 10001 solo responde que está deprecada. (README §2; código `src/app/api/webhooks/hikvision/route.ts`)
- b:N3. Modos exclusivos en Configuración → Modos → Modos (LPR / Face / Cola): MODULE_LPR, MODULE_FACE, MODULE_QUEUE; Guardia (MODULE_GUARD) se suma. Cambiar de modo recarga la interfaz. (código settings, layout)
- b:N4. Sin internet sigue leyendo, decidiendo y grabando; solo se demoran Telegram/WhatsApp y los logos de marca. (Manual del Instalador)
- b:N5. Requisitos: hasta 4 cámaras 4 núcleos, 8 GB, 250 GB SSD; 8 a 16 cámaras 8 núcleos, 16 GB, 500 GB SSD. 8 cámaras generan 3 a 4 GB/día de fotos. (Manual del Instalador)

## T03 Quién decide
- b:N6. Orden de decisión en server.js: 1) si la cámara informa su lista (whiteList → GRANT, blackList → DENY) manda la cámara; 2) si no, se busca la matrícula como credencial PLATE: con Modo LPR "Lista Blanca" (por defecto) GRANT, con "Lista Negra" DENY; 3) sin credencial, DENY. (código server.js)
- b:N7. La cámara tiene su propia lista: "Cargar matrículas" en la puesta a punto manda las habilitadas a la lista de la cámara, "son las que prenden el semáforo verde con el relé". La lista negra pasa a la blackList de todas las lectoras Hikvision. (código CajonDispositivo, lista-negra.ts)
- b:N8. Antirrebote: la misma matrícula no se registra dos veces en 5 s (servidor) ni dos veces por la misma cámara en 20 s según la hora del evento; NO_LEIDA nunca se agrupa. (código server.js)
- b:N9. Hora del evento: se usa la de la cámara solo si está a menos de 10 minutos de la del servidor; si no, la del servidor. (código server.js)
- b:N10. Tres estados para el operador: Autorizado (verde), Denegado (ámbar) y Lista negra (rojo con sonido). "Un Denegado no es una alarma." (Manual del Operador)
- b:N11. Invitados: pase con patente y vigencia; el match tolera uno o dos caracteres (según largo) y la lista negra siempre gana; avisa al anfitrión por WhatsApp. (código server.js matchInvitedPlate)

## T06 Alta en Dispositivos
- b:N12. Menú lateral → Dispositivos → Agregar: alta guiada. Primero el tipo (Cámara LPR, Cámara de intrusión o NVR / Grabador); para LPR los pasos son Equipo, Conexión, Ubicación, Grabación, Puesta a punto. (código CajonDispositivo)
- b:N13. Ubicación pide el Sentido: Entrada ("Lee a los que entran al barrio") o Salida ("Lee a los que salen; cierra visitas"), y el grupo de acceso; sin grupo aparece "Sin grupo de acceso la cámara no deja pasar a nadie por servidor". (código)
- b:N14. Puesta a punto LPR (Hikvision): Dar de alta la cámara, Poner la hora, Servidor de alarmas → OmniAccess (HTTP host), Modo ANPR (verifica roadDetection), Video H.264 (canales 101 y 102), Video en vivo (go2rtc), Cargar matrículas, Vincular la grabación, Calcular retención. Cada tarea queda en ok, error o salteado. (código provision.ts)
- b:N15. Convención de nombre del manual: `P1 - Entrada (204)`: acceso, sentido y último octeto de la IP. Aparece en reportes y alertas. (Manual del Instalador)
- b:N16. Configuración en la cámara si se hace a mano: destino IP del servidor, puerto de webhooks, ruta del driver, formato XML, sin autenticación (red privada). Ruta Hikvision `/api/webhooks/hikvision` en el puerto 10000. (Manual del Instalador, HIKVISION_SETUP)

## T07 Eventos que llegan
- b:N17. El receptor acepta POST multipart: separa XML/JSON de las imágenes; la foto más grande es la escena y la que se llama plate/licen es el recorte. Si llega sin imagen, pide un snapshot por ISAPI. (código)
- b:N18. Si la cámara manda ANPR sin chapa se guarda como `NO_LEIDA` con "ALERTA: Matrícula No Reconocida"; heartbeats solo actualizan "último contacto". (código)
- b:N19. La cámara se identifica por MAC, después por IP; si hay una sola Hikvision se asume esa. (código)
- b:N20. Monitor de webhooks para verificar: el manual dice Configuración → Avanzado → Monitor de webhooks; en el código está en Configuración → Sistema → Webhooks (y la página Debug Webhooks). (Manual del Instalador vs código)

## T08 NVR y hora
- b:N21. Sin canal de NVR no hay grabación asociada: el botón Grabación queda deshabilitado ("Cámara sin canal NVR mapeado") y el historial dice "sin NVR". (Manual del Operador, código)
- b:N22. En Dispositivos: botón "Detectar grabaciones" (busca la IP de cada cámara en los canales de todos los NVR), "Calcular retención" (la grabación más vieja del canal) y "Sincronizar hora" (muestra hora y desfase y pregunta antes de poner la hora del servidor). (código)
- b:N23. Sincronizar hora tiene dos modos: hora del servidor (Montevideo, manual, no necesita internet) o NTP (solo si el equipo alcanza ese servidor). (código sync-time)
- b:N24. Alerta "drift" con desfase mayor a 120 s; el manual dice "más de 2 minutos". (código, Manual del Instalador)
- b:N25. Retención en Configuración → Sistema → Almacenamiento; valores típicos 30 días fotos, 7 días clips; con 30 días y 8 cámaras hacen falta unos 120 GB. (Manual del Administrador)

## T09 Calibración
- b:N26. Dispositivos → (acción) Calibrar ANPR: video en vivo, "Zona de lectura de patente" con Carril 1 y Carril 2, "Línea de calibración", "Línea de captura ANPR", "Guardar línea de captura", reversible. Coordenadas Hikvision 0 a 1000 con origen abajo a la izquierda. (código CameraCalibrator, isapi-anpr)
- b:N27. Auto-calibración "Perfil ANPR barrio-noche" (barrio abierto / nocturno, tráfico de 20 a 30 km/h): obturador 1/500, anti-brillo de patente nivel 60, WDR apagado, HLC apagado, ganancia máx 40, filtro IR automático, iluminador IR auto, foco semiautomático. Solo Hikvision. (código isapi-camera)
- b:N28. Tasa de lectura: botón en Dispositivos (vista Cámaras LPR): leídas contra no leídas por cámara (peor primero) y por hora, rango por días. Interpretación: más de 95 % correcta, 85 a 95 % aceptable, menos de 85 % problema; mirar por hora. (código ReadRateDialog, Manual del Instalador)
- b:N29. Las cuatro reglas: ángulo hasta 30°, patente de 100 a 300 px (4 a 8 m), un carril por cámara, leer en el punto de detención; el 80 % de las fallas es de noche; probar de noche. (Manual del Instalador)

## T10 Monitor LPR
- b:N30. Menú: "Monitor LPR" (el manual dice "Monitor en Vivo"). Tres columnas: Entradas, foco central, Salidas; mosaico con la última captura de cada cámara y "Capturas recientes". (código monitor-lpr)
- b:N31. Barra superior en el código: buscador "Buscar matrícula e investigar...", En casa (adentro/total), Hoy, permitidos y denegados de hoy, filtro Todos / Permitidos / Denegados, Color y Tipo, y botones Lista de vigilancia, popup automático de anomalías, sonido, refrescar. El manual menciona LIVE, ADENTRO, En buffer y campana, que no están en esta versión. (código vs Manual del Operador)
- b:N32. Foco central: Patente con recorte, marca, tipo, color, cámara y hora, botones Investigar y Registrar; si la lectura es SIN LECTURA aparece "Cargar matrícula" y la consulta "Matrículas Requeridas" del Ministerio del Interior (el guardia resuelve el captcha). (código)
- b:N33. Cargar matrícula a mano re-evalúa el acceso (residente, decisión, vigilancia) en el servidor. (código PlateManualButton)
- b:N34. Alertas críticas abajo a la izquierda: merodeo y lista negra. (código)
- b:N35. 1 a 3 s desde la línea hasta el monitor; más de 10 s habitual es degradación. (Manual del Operador)

## T11 Investigar
- b:N36. Ficha del evento: acciones Grabación, Similares, Clip, Exportar, Registrar, Lista negra (o Desmarcar); pestañas Perfil (Frecuencia, Cámaras habituales, Horarios habituales), Historial, Datos. (código EventDetailsDialog)
- b:N37. Exportar: ZIP con `captura.jpg`, `recorte_matricula.jpg`, `clip_30s.mp4`, `evento.json` (por defecto 10 s antes, 30 s). Clip: ventana configurable en Configuración → Avanzado → Video del evento (por defecto 10 s antes y 10 s después), descargar o enviar por WhatsApp. (código export, DescargaClip)
- b:N38. Búsqueda inteligente: modo Accesos sobre la base propia (color, tipo, marca, matrícula, acceso P1 a P7, entradas/salidas, autorizados/denegados, franja, fechas relativas) con chips de lo entendido; modos Por texto e imagen consultan el NVR. El ítem del menú aparece solo con un NVR VPro dado de alta. (README, código)
- b:N39. Similares busca en cámaras de contexto, no en las LPR; 10 a 40 s. (Manual del Operador)
- b:N40. Historial de Acceso: buscador "Buscar matrícula, persona, lote o cámara…", filtros, columna Grabación, "Exportar (Excel / PDF)" y JSON. (código history)

## T12 Permanencia y merodeo
- b:N41. Permanencia: en una salida, tiempo desde la última entrada de la misma matrícula; aparece en la ficha. (código EventDetailsDialog)
- b:N42. Merodeo: por defecto activo, 3 pasadas de la misma matrícula en 30 minutos por cualquier acceso, 30 minutos de enfriamiento, excluye residentes autorizados; deja una entrada MERODEO en la bitácora y una alerta en el monitor. Se ajusta con claves de configuración (MERODEO_*), sin pantalla propia en esta versión. (código server.js)
- b:N43. Plazas de Parking → Anomalías de presencia: "Vehículo del barrio adentro hace mucho" (4 días por defecto), "Lotes sin movimiento (posible casa vacía)" (21 días), "Autos no identificados adentro". (código plazas)

## T13 Lista de vigilancia
- b:N44. Categorías: Lista negra (rojo), VIP / Autorizado (verde), En búsqueda (ámbar). En búsqueda exige motivo ("es lo que ve el guardia en la captura"). Avisa (Telegram y regla WATCHLIST) o En silencio (solo monitor). (código WatchlistDialog, watch-categories)
- b:N45. Al poner en lista negra: "Toda lectura se registra DENEGADA desde ahora" y se carga en las lectoras como blackList; si una lectora no responde, la barrera la deniega igual por servidor. (código lista-negra.ts; el server.js de esta copia todavía decide solo por cámara y credencial)
- b:N46. Un usuario con rol de bloqueado arrastra sus matrículas a la lista negra. (Manual del Administrador, código)

## T14 Padrón
- b:N47. Cadena: Unidad → Usuario → Credencial (matrícula, RFID, rostro) → Grupo de acceso. "El error más común es cargar matrículas sueltas sin usuario ni unidad." (Manual del Administrador)
- b:N48. La decisión del servidor busca la credencial tipo PLATE, normalizada sin espacios ni guiones; Vehículos / Matrículas es la vista centrada en el vehículo con la última detección. (código)
- b:N49. Sincronizar matrículas a las cámaras: Incremental (recomendado, solo diferencias, "Las cámaras nunca quedan sin lista") o Reemplazo total (borra y recarga, "Sólo para reparar"). (código SyncToDevicesDialog)
- b:N50. Estados: Activo, Suspendido, Eliminado; para baja temporal, suspendido. Alta con efecto inmediato. (Manual del Administrador)
- b:N51. Diferencia cámara 676 contra base 673: matrículas filtradas, normalización o importación tardía. (ANALISIS_PROBLEMAS_LPR)

## T15 Reportes y avisos
- b:N52. Reportes en LPR: Historial de Acceso → Exportar (Excel / PDF) eligiendo período, qué eventos y columnas; portada en Configuración → Branding → Reportes Exportables. (código)
- b:N53. Avisos que salen en LPR en esta versión: Telegram por vigilancia con aviso y por salud de cámaras LPR y NVR; WhatsApp al anfitrión de un invitado; push en la PWA Control LPR (`/pwa/lpr`). La pantalla Notificaciones con reglas aparece en el menú del modo Filas. (código; Manual del Administrador describe reglas para LPR)
- b:N54. PWA de guardia: OCR en el teléfono con Tesseract (solo letras y números, línea única, formato Mercosur ABC1234 o ABC1D23, confianza mínima 40 %). (OCR_CLIENT_SIDE_FINAL)

## T16 Diagnóstico y salud
- b:N55. Sondeo de cada equipo (UI: "sondeo activo cada 30s"; README: cron por minuto); alertas offline (dos sondeos), disk, mem (95 %), drift (120 s), vca (ANPR apagado); historial 14 días; Telegram para LPR y NVR. (código device-health)
- b:N56. ANPR y AcuSearch del NVR son excluyentes por cámara: si el canal LPR se agrega a la búsqueda por imagen del NVR, el recurso inteligente pasa de `roadDetection` a `smart` y la cámara deja de leer en silencio. Revertir en orden: sacar el canal de la búsqueda del NVR, poner roadDetection, reiniciar, esperar unos 80 s. (Manual del Instalador, README)
- b:N57. "Dejaron de entrar matrículas": mirar si llegan webhooks; si llegan sin chapa, revisar el modo; si no llega nada, red o servicio. Una sola cámara: estado, ping, notificación HTTP (se pierde con un reset), tasa. (Manual del Instalador)
- b:N58. Colores capturados solo blanco y plateado: lo manda así la cámara; habilitar atributos de vehículo en la cámara. (ANALISIS_PROBLEMAS_LPR)
- b:N59. Checklist de entrega: leer de día y de noche, tasa arriba de 90 %, grabación desde un evento de cada cámara, relojes, reinicio del servidor, retención, avisos probados, padrón, credenciales de fábrica cambiadas. (Manual del Instalador)

## Diferencias manual / código (manda el código)
- Menú "Monitor en Vivo" → en LPR se llama "Monitor LPR".
- "Dispositivos LPR" → "Dispositivos".
- Barra del monitor: LIVE, ADENTRO, En buffer y campana no están; hay En casa, Hoy, permitidos, denegados, vigilancia, popup de anomalías, sonido.
- Monitor de webhooks: Configuración → Sistema → Webhooks (no Avanzado).
- Decisión: el manual dice que contrasta horario; en server.js la decisión es lista de la cámara, credencial PLATE y Modo LPR, sin evaluar el horario del grupo.
- Merodeo: el manual dice "mismo acceso"; el código cuenta pasadas por cualquier acceso.
- Notificaciones/Despachos/Reportes como menú: en esta versión aparecen en modo Filas; en LPR el reporte sale del Historial.
- Avicam: en el código es un terminal facial, no una cámara LPR. El README lo menciona junto a Hikvision para LPR.
- Clip de la ficha: ventana 10 s + 10 s configurable (el manual dice 30 s); el ZIP sí trae `clip_30s.mp4`.
