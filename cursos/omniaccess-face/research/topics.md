# OmniAccess Face: mapa del tema

Público: técnico de IES (instala y configura) y operador (guardia, portería, administrador del barrio o edificio). Nivel inicial a intermedio. Fuente de verdad: código y manuales de OmniAccess (Infratec), rama de octubre de 2026. Las fuentes web cubren hardware, teoría de reconocimiento y marco legal.

Cómo se suele enseñar: los fabricantes de terminales faciales (Hikvision, Control iD, Synerion, ClockRite) separan instalación física, enrolamiento con foto de calidad y parámetros de reconocimiento; las plataformas (HikCentral, Akuvox Smart Access) agregan alta de personas, sincronización a equipos, eventos y reportes. Los reguladores (URCDP, GDPR) agregan consentimiento, finalidad y retención.

- T01 Qué resuelve OmniAccess Face y quién decide la apertura (terminal contra plataforma)
- T02 Modos del sistema: MODULE_FACE, Modo Face (Lista Blanca, Lista Negra, Aprendizaje deshabilitado)
- T03 Colocación del terminal: altura, distancia, luz, contraluz, sol, WDR, limpieza
- T04 Alta del terminal en Dispositivos: Acceso Facial, fabricante, modelo, IP, MAC, credenciales, sentido
- T05 Eventos por Action URL o HTTP: puerto 10000, variables, MAC, normalización de eventos
- T06 La foto del evento: doorlog del terminal, bucket FACE, ficha del evento
- T07 Apertura: decisión local del terminal, botón Relé, relay/trig, estado de puerta
- T08 Alta de rostros: ficha de la persona, foto, calidad de la imagen
- T09 Sincronización: Terminales de rostro, Memoria Flash (Directorio, Inyectar, Volcar, Descargar), HardwareMirror, ID numérico
- T10 Grupos de Acceso y horarios: qué guarda OmniAccess y qué decide el terminal
- T11 Monitor Facial: columnas Entrada y Salida, filtros, LIVE/OFFLINE, video por go2rtc
- T12 Ficha del evento y alta rápida desde el evento (Registrar)
- T13 Visitas, lista negra facial y bajas: sacar la cara del terminal
- T14 Historial, exportación y Auditoría Hardware
- T15 Umbral de coincidencia, falsos positivos y negativos, antisuplantación
- T16 Diagnóstico: Pull y Push, webhooks, reloj, credenciales, red
- T17 Datos biométricos: Ley 18.331 (art. 4 literal Ñ, 9, 18, 18 bis), consentimiento, retención y borrado
