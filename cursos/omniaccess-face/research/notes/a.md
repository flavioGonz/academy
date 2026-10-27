# Notas a: el producto (código y manuales de OmniAccess, octubre de 2026)

Fuente: copia de solo lectura del código. No se cita por URL en las tarjetas; se nombra el manual o la pantalla. Cuando manual y código difieren, manda el código.

## T01 / T02 Arquitectura y modos
- Módulos en `Setting`: MODULE_LPR, MODULE_FACE, MODULE_QUEUE, MODULE_GUARD (src/lib/module-definitions.ts). MODULE_FACE se llama "OmniAccess Face: Reconocimiento facial y control de acceso".
- Configuración → Modos → "Modos (LPR / Face / Cola)": pestañas Modo LPR, Modo Face, Modo Cola. Banner "Activar este modo": "Cambiar de modo recarga la aplicación con la interfaz del nuevo modo."
- Modo Face (Setting MODE_FACE): opciones "Lista Negra" (las capturas identificadas serán DENEGADAS), "Lista Blanca" (las identificadas serán PERMITIDAS), "Aprendizaje" (deshabilitado, "Modo en desarrollo"). Textos de ayuda: "La cámara controla la apertura física" / "La cámara aún controla la apertura física". Por defecto el servidor asume WHITELIST si no hay valor.
- Con MODULE_FACE el menú cambia: "Monitor en Vivo" apunta a /admin/monitor-face; aparece la sección "Face" con "Dispositivos Faciales" (/admin/devices?type=FACE_TERMINAL); "Invitados" solo aparece con MODULE_LPR; "Tags RFID" y "Grupos de Acceso" están en cualquier modo que no sea Filas. La pantalla de inicio en modo Face es /admin/monitor-face.
- Servidor de eventos: server.js escucha en el puerto 10000 (WEBHOOK_PORT). El panel corre aparte (en la documentación, puerto 10001). La ruta Next.js /api/webhooks/akuvox está marcada DEPRECATED: responde OK pero no procesa; la URL debe ir al 10000.
- Drivers con función facial real: AkuvoxDriver (IFaceDriver, IRfidDriver, ILogDriver, IStatsDriver) y HikvisionDriver. ZKTeco, Intelbras, Dahua, Uniview, UniFi, Milesight tienen triggerRelay y upsertCredential vacíos. El README de door-control dice "Hikvision (Futuro)" para apertura, pero el código ya implementa triggerRelay para Hikvision: manda el código.

## T04 Alta del terminal
- Gestión → Dispositivos (en modo Face, entrada "Dispositivos Faciales"). Formulario "Configuración técnica del nodo de acceso": Nombre de Identificación, Tipo (Cámara LPR, Cámara de intrusión, NVR / Grabador, Acceso Facial, Contador de Filas), Fabricante (Akuvox, Avicam, Bosch, Dahua, Hikvision, Intelbras, Milesight, Ubiquiti UniFi, Uniview, ZKTeco), Modelo Hardware, Host / IP, Hardware ID (MAC), Usuario Manager, API Password, Sentido del Flujo (ENTRADA (Ingreso) / SALIDA (Egreso)), Ubicación Física. authType BASIC por defecto (NONE, BASIC, DIGEST).
- Ayuda del formulario para Akuvox: "Intercom > Relay > HTTP Notification" y "Activar el envio de eventos por HTTP POST". El código del servidor lee los parámetros de la URL (query string) y el configurador de la lista de dispositivos usa Action URL con GET: diferencia manual/código, manda el código (Action URL con parámetros en la URL).
- Fila del equipo: chip con marca y modelo, botón "Relé" (tooltip "tocar para accionar el relé"), contadores Faces y Tags (getDeviceStats: /api/user/get y /api/rfkey/get en Akuvox; actualiza lastOnlinePull), íconos Pull (verde, consulta exitosa en los últimos 5 min) y Push (azul, "Push (eventos)": último webhook), columna Hora / NTP con desfase.
- Menú ⋯ → Gestión: "Memoria Flash" (solo FACE_TERMINAL), "Webhooks (Action URL)" (solo Akuvox), "Editar Configuración".
- El dispositivo se identifica en los eventos por MAC; sin MAC cargada el evento puede quedar sin equipo.

## T05 / T06 Eventos
- Configurador de Action URLs (diálogo "Configurador de Action URLs", "Akuvox Universal Webhook Logic", pie "Servidor Webhook listo en puerto 10000"): base `http://<servidor>:10000/api/webhooks/akuvox`. Eventos recomendados: Valid Face (`event=face_valid&mac=$mac&user=$user_name&userid=$userid&FaceUrl=$FaceUrl&PicUrl=$pic_url&time=$time`), Invalid Face, Valid Card, Invalid Card, Valid PIN, QR Code, Relay Output (`event=relay_open`), Sensor Input, Call Events, System Boot. Botón "Copiar URL".
- handleAkuvoxWebhook (server.js): exige `mac` (sin MAC responde 400). Normaliza la MAC (sin dos puntos ni guiones, mayúsculas) y busca el equipo; si no coincide (por ejemplo llegó `$mac` sin reemplazar) prueba por IP de origen y, si hay un solo Akuvox, lo asume. Si no encuentra equipo, NO guarda el evento ("Event skipped"). Actualiza lastOnlinePush.
- Normalización: relay/relay_open → door_open (doorStatus OPEN), relay_close → door_close; face&type=invalid → face_invalid; card, code, qr, call_start → calling, hangup → call_end, boot.
- face_valid: valor = `user` o `name` (si empieza con `$`, "No Identificado"); details "Rostro: <nombre>, Similitud: <similarity o 100>%". face_invalid → DENY "Rostro: Desconocido".
- Foto: "Akuvox Action URLs do NOT send images" (src/lib/akuvox-models.ts). El servidor la va a buscar al terminal: primero la ruta que vino en FaceUrl/PicUrl, después recorre los últimos 10 registros de doorlog/searchlog/accesslog (puertos 80 y 8080) buscando coincidencia por userid, tarjeta o nombre, y como última opción la foto del perfil del usuario en el equipo. La sube al bucket "face" (MinIO/S3) y la anota como FaceImage en details.
- Vinculación con la ficha: intenta por `userid` (no coincide con los ids internos, que son cuid) y luego por credencial tipo FACE con valor igual al nombre recibido. Si la encuentra aplica MODE_FACE (Lista Negra → DENY, Lista Blanca → GRANT). Si no la encuentra en face_valid: Lista Negra → GRANT, Lista Blanca → DENY. La ficha subida desde la persona no crea credencial FACE (solo guarda `cara`); la crean el registro rápido (registerFace, valor DNI o id) y la importación desde equipo. Consecuencia: el evento muestra el nombre que mandó el terminal ("Rostro") aunque no quede vinculado a una ficha.
- Hikvision: llega al puerto 10000 (ruta raíz con POST o que contenga "hikvision"), multipart con JSON. Si no trae nombre de candidato (no identificado), el evento se ignora ("Only Store Matches"). Busca el usuario por nombre exacto. Lista Negra → DENY, si no GRANT. Guarda foto completa y recorte del rostro en el bucket "face".
- Evento persistido en AccessEvent (accessType FACE, decision GRANT/DENY, direction del equipo, snapshotPath, details) y emitido por WebSocket `access_event`.
- Debug: Configuración → Sistema → Webhooks (WebhookDebugPage): fuentes Akuvox, Facial, LPR Hik, TAG / RFID, con datos RAW.

## T07 Apertura
- El terminal abre por su cuenta al reconocer (decisión local). OmniAccess no manda abrir en eventos faciales; el texto de Modo Face lo dice: "La cámara controla la apertura física".
- Apertura remota: botón "Relé" en Dispositivos → triggerDeviceRelay. Akuvox: POST /api/relay/trig con num 1, mode 0, level 0, delay 5; si falla, GET /fcgi/do?action=OpenDoor (formato viejo) y /fcgi/OpenDoor (alta seguridad) con usuario de relé. Hikvision: ISAPI. Otras marcas: "Marca no compatible con disparo remoto". door-control.md describe POST /api/devices/{id}/open y monitor en /admin/dashboard: no existe en el código revisado (no hay ruta open en api/devices/[deviceId]), manda el código.
- Estado de puerta: door_open / door_close por Action URL Relay Output actualizan doorStatus (OPEN/CLOSED) y el color del botón Relé.

## T08 / T09 Alta y sincronización
- Gestión → Usuarios & Residentes → "Nueva persona" (cajón "Quién es, dónde vive, con qué entra y a qué equipos se manda"). Foto: "Subir foto" / "Cambiar", ayuda "Sirve para los terminales faciales." Sección "A qué equipos se manda": ayuda "Los grupos dan el permiso; esto copia la credencial a la memoria del equipo. Son cosas distintas: sin la copia, el equipo tiene el permiso pero no sabe a quién reconocer." Bloques "Cámaras LPR" y "Terminales de rostro" (bloqueo "Subí una foto arriba para poder mandarla."), "Mandar por área".
- Al guardar, pasos visibles: "Crear la ficha" / "Guardar los cambios", "Subir la foto", "Enviar el rostro a <terminal>" (error "El terminal no aceptó el rostro."). Si algo falla el cajón queda abierto.
- AkuvoxDriver.syncUserWithFace: ID numérico de 9 dígitos derivado del id (FNV-1a), /api/user/add (o /set si existe) con Name, CardCode (tags), PrivatePIN, ScheduleRelay "1001-1;" y Schedule "1:1001", DoorNum 1, imagen en base64; después /api/face/add (o /set). Hikvision: UserInfo/Record, CardInfo/Record y Face/Record por ISAPI.
- Memoria Flash (DeviceMemoryDialog): pestañas Directorio, Doorlog, Call Log (Akuvox). Directorio = "Identidades en memoria física"; modo "Inyección de Rostros" ("Sincroniza usuarios hacia el equipo", "Inyectar Usuarios"). "Volcar Base de Datos a Equipo" (Modo Sobrescritura, "Advertencia de Sobrescritura", "Iniciar Volcado"): manda todas las personas con foto o tag. "Descargar Equipo a App" (Modo Importación Inteligente, "Asignar a Residencia / Lote", "Iniciar Importación"). Botón "Refrescar Memoria".
- HardwareMirror: espejo de lo leído en el equipo (syncStatus ONLY_HARDWARE si solo está en el equipo, IN_SYNC tras importarlo).
- Requisitos de foto según docs/help/akuvox-api.md: JPG, menos de 200 KB, mínimo 640x480, fondo claro, frontal, sin lentes oscuros. Límites: 3.000 a 10.000 rostros según modelo; retcode -10 = memoria llena.
- Borrar una persona en OmniAccess (deleteUser) solo borra la ficha: no borra la cara del terminal ni la foto del bucket. Para el equipo: Memoria Flash → Directorio → eliminar ("Rostro eliminado correctamente").

## T10 Grupos y horarios
- Grupos de Acceso (/admin/groups, "Niveles de permisos y jerarquías del recinto"): nombre, Personas, Equipos. Ayuda: «Residentes», «Proveedores con horario», «Personal Club House».
- El modelo Schedule (días, hora inicio, hora fin por grupo) existe en la base pero ninguna pantalla ni lógica lo usa en esta versión. syncToDevices (copiar credencial a los equipos de los grupos) existe pero nadie lo llama. El usuario se manda al Akuvox con horario 1001 (el horario siempre válido del equipo). Los horarios por usuario se configuran en el terminal (curso Akuvox, lección de usuarios y horarios) o se resuelven con alta y baja de la cara.

## T11 / T12 Operación
- Monitor Facial (/admin/monitor-face): encabezado "Monitor Facial · Reconocimiento en tiempo real", indicador LIVE / OFFLINE (conexión del navegador al servidor por WebSocket), filtros Todos / Permitidos / Denegados, botón recargar. Tres columnas: Entrada, centro (destacado del último evento + "Capturas Recientes"), Salida. Muestra eventos FACE de las últimas 24 h (80 al cargar, hasta 100). Cada columna puede tener video EN VIVO del terminal si existe el stream `face_<id>` en go2rtc; si no, foto cada 5 s o "Sin señal". Tarjeta: foto (FaceImage, si no la del perfil, si no la captura), "Autorizado"/"Denegado" (rojo pulsante), Entrada/Salida, nombre o "Desconocido" en ámbar, unidad, hace cuánto, equipo. Sello "PERMITIDO"/"DENEGADO" sobre el video y "% match".
- Ficha del evento (EventDetailsDialog): Persona, Similitud, Rostro, "No registrado"/"Autorizado", acciones "Registrar" (abre Usuarios con action=create y la foto del evento), "Exportar" (ZIP con foto, datos y clip de 30 s si la cámara tiene canal NVR), "Ver grabación del NVR en este instante".
- PWA "Control Facial" (/pwa/face): eventos 24 h, Reconocidos, Denegados, botón "Registrar rostro" ("Tomá o subí una foto del rostro y asigná un nombre."), activar notificaciones push. registerFace crea persona con rol VISITOR, foto y credencial FACE; no la manda a ningún terminal. En el código revisado el servidor no envía push por eventos faciales (sendWebPushToAll solo se usa en Filas/ONVIF).
- Pantalla adicional /admin/dashboard-face ("Monitor en Vivo Face", Lista Negra, Lista Blanca, Cargar Rostro, Buscador Inteligente) con motor de comparación externo (CompreFace) y umbral COMPAREFACE_MIN_SIM (85 % por defecto en pantalla). No está en el menú principal: depende de la instalación.

## T13 Visitas y bloqueos
- Roles: RESIDENT, VISITOR, STAFF, ADMIN, PROVIDER, TEMPORARY_VISITOR, BLACKLISTED, WHITELISTED, SECURITY, OPERATOR.
- Invitaciones (Invitation/Guest/GuestEntry) validan por LPR, QR, búsqueda o manual; el menú Invitados solo aparece con MODULE_LPR. Los QR que lee un Akuvox llegan como "Código QR Válido" (qr_valid) y no se cruzan con las invitaciones.
- Lista negra en la ficha de la persona es de matrículas (LPR). En facial: rol BLACKLISTED (toggleBlacklist guarda rolAnterior) y pantalla de Lista Negra de dashboard-face; syncAllBlacklistAction sincroniza solo a Hikvision. Para que un Akuvox deje de abrir, hay que sacar la cara de su memoria.

## T14 Historial y auditoría
- Historial de Acceso: filtros Rostros / RFID, Todos / Permitidos / Denegados, Ambos / Entrada / Salida, rango de fecha y hora, búsqueda "Buscar matrícula, persona, lote o cámara…". Botones "Exportar (Excel / PDF)" y "Exportar JSON reimportable". En modo solo Face arranca con filtro Rostros.
- Auditoría Hardware (Configuración → Avanzado): "Sincronización de Memoria", "Memoria Física", "Pendientes de Sincr.", "Inspector de Eventos", "Ver logs en DB". syncHardwareLogs trae los últimos 100 registros del doorlog Akuvox y crea eventos "SINCRO_HW" que no estén ya (ventana de 2 s).

## T16 Diagnóstico
- Online si respondió el sondeo o hubo Pull o Push en los últimos 10 min.
- Reloj: columna Hora / NTP con desfase; "Sincronizar hora" solo en el menú de LPR.
- Errores del API Akuvox (docs/help/akuvox-api.md): 401 credenciales, timeout red, retcode -10 memoria llena.

## T17 Privacidad (producto)
- Fotos de alta y capturas van al mismo bucket "face" (S3_BUCKET_FACE). Configuración → Sistema → Almacenamiento: "Bucket FACE", "Días de retención antes de borrar. (0 = nunca)". La regla de vencimiento (updateBucketLifecycle) se aplica a todo el bucket (prefijo vacío): también borra las fotos de alta más viejas que ese plazo.
- face-administrador.md tiene la sección "Privacidad y retención" pendiente de redactar.
