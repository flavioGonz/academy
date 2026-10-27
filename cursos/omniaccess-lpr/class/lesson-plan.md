# Plan de lecciones: OmniAccess LPR

Público: técnico de IES (instala y mantiene) y operador (guardia, portería, monitoreo, administrador del barrio). Nivel inicial a intermedio. Fuente de verdad: manuales del producto (versión 2026.09) y código vigente de octubre de 2026; la web aporta teoría, hardware y voces críticas. 12 lecciones en 4 arcos.

## Arco 1. Entender el sistema (lecciones 1 y 2)
Por qué: antes de tocar una cámara conviene saber qué viaja por la red, dónde se decide la barrera y qué significa cada color en la pantalla del guardia.

### 1. Recorrido de lectura · 3 de 3 fuentes
- Idea: la cámara lee a bordo, manda un XML por HTTP al servidor del predio (puerto 10000), el servidor decide, guarda foto y evento y lo empuja al monitor en 1 a 3 s. Todo local: sin internet sigue andando.
- Por qué importa: cada falla posterior se ubica en un tramo del recorrido.
- Historia: PSDB 1976, Dartford Tunnel 1979 (https://www.traffictechnologytoday.com/features/feature-who-invented-anpr-the-untold-british-story-behind-a-global-traffic-technology-revolution.html).
- Laboratorio: Rápido, 15 min, seguir una lectura de punta a punta en una instalación de prueba (Webhooks, Monitor LPR, ficha → Datos).
- Regla: cuando algo falla, primero ubico en qué tramo del recorrido se cortó.

### 2. Quién abre · producto + 2 de 2 web
- Idea: la barrera la puede abrir la lista de la propia cámara (relé) o la decisión del servidor (credencial PLATE y Modo LPR). Antirrebote de 5 y 20 s. Verde, ámbar, rojo.
- Historia: tolerancia de un carácter en accesos cerrados (https://en.wikipedia.org/wiki/Automatic_number-plate_recognition).
- Laboratorio: Foco, 15 min, mandar un evento de prueba con curl antes y después de dar de alta `SBA1234`.
- Regla: sé siempre quién abre en cada portón: la cámara, el servidor o los dos.

## Arco 2. Instalar y configurar (lecciones 3 a 6)
Por qué: es el trabajo del técnico en obra; termina con una cámara bien colocada, dada de alta, grabando con la hora correcta y calibrada para la noche.

### 3. Cámara bien parada · 4 de 4
- Idea: ángulo hasta 30°, patente de 100 a 300 px (Hikvision pide 130), 4 a 8 m, un carril por cámara, leer donde el auto va lento, poste firme.
- Historia: guía Hikvision con sus errores comunes (https://cdn.connectec.uk/Files/Products/CCTV/Camera/Hikvision_Trade/installation_guide_of_hikvision_lpr_camera.pdf).
- Laboratorio: Campo, 20 min, medir píxeles de patente con una captura y un auto quieto.
- Regla: la posición de la cámara no se arregla con software.

### 4. Alta guiada · producto + 2 de 2 web
- Idea: Dispositivos → Agregar → Cámara LPR; pasos Equipo, Conexión, Ubicación (sentido y grupo), Grabación y Puesta a punto (hora, HTTP host, modo ANPR, H.264, go2rtc, matrículas, grabación, retención). Verificar en Configuración → Sistema → Webhooks.
- Historia: cámaras detrás de NAT que no decían quién eran (https://ipcamtalk.com/threads/assistance-with-hikvision-ds-2cd7a26g0-p-izs-integration-using-http-listening.79674/post-897038).
- Laboratorio: Campo, 25 min.
- Regla: una cámara está dada de alta cuando la puesta a punto queda toda en verde y el primer evento aparece en Webhooks.

### 5. Grabación y hora · 4 de 4
- Idea: sin canal de NVR no hay video del evento; Detectar grabaciones, Calcular retención, Sincronizar hora (hora del servidor o NTP local). Alerta con más de 120 s.
- Historia: grabaciones sin hora confiable no sirven de prueba (https://mobatime.com/support/faq/why-is-time-important-for-cctv).
- Laboratorio: Admin, 15 min.
- Regla: misma hora en cámara, NVR y servidor, verificada en cada visita.

### 6. Calibrar de noche · split
- Idea: Calibrar ANPR: zona de lectura por carril, línea de captura, perfil barrio-noche (1/500, anti-brillo, WDR y HLC apagados, ganancia 40, IR auto, foco semiautomático) y Tasa de lectura por hora.
- Historia: "ajustada de día, esperá la noche" (Hikvision).
- Laboratorio: Foco, 25 min (de noche).
- Regla: la calibración se mide por hora y se prueba de noche.

## Arco 3. Operar (lecciones 7 a 10)
Por qué: el turno del guardia y del operador; termina con alguien que lee el monitor de lejos, investiga una matrícula y sabe qué hacer con un merodeo o una lista negra.

### 7. Monitor en vivo · producto
- Monitor LPR: tres columnas, foco central, barra (En casa, Hoy, permitidos, denegados), filtros, vigilancia, popup de anomalías, sonido; SIN LECTURA y Cargar matrícula.
- Laboratorio: práctica guiada, 15 min. Regla: verde pasa, ámbar se verifica, rojo es protocolo.

### 8. Investigar matrícula · producto
- Ficha del evento: Grabación, Similares, Clip, Exportar, Registrar, Lista negra; Perfil, Historial, Datos; Búsqueda inteligente modo Accesos.
- Historia: Roseville, 71 % de alertas equivocadas que nadie detuvo porque se verificaba (https://www.techspot.com/community/topics/one-california-town-found-flocks-license-plate-cameras-were-wrong-71-of-the-time.298313/).
- Laboratorio: práctica guiada, 20 min. Regla: antes de afirmar, miro el recorte y la grabación.

### 9. Permanencia y merodeo · producto
- Permanencia al salir; merodeo por defecto 3 pasadas en 30 min; anomalías de presencia en Plazas (4 y 21 días, no identificados adentro).
- Laboratorio: práctica guiada, 15 min. Regla: un patrón se confirma con el historial antes de escalarlo.

### 10. Lista de vigilancia · producto + 2 de 2 web
- Lista negra, VIP / Autorizado, En búsqueda; motivo; Avisa o En silencio; se carga en las lectoras.
- Laboratorio: práctica guiada, 15 min. Regla: nadie entra a la lista sin motivo escrito.

## Arco 4. Administrar y diagnosticar (lecciones 11 y 12)
Por qué: lo que sostiene la instalación en el tiempo: el padrón al día, los reportes de cierre de mes y el árbol de diagnóstico para la llamada de "dejaron de entrar matrículas".

### 11. Padrón y reportes · producto
- Unidad → usuario → credencial → grupo; Vehículos / Matrículas; Sincronizar matrículas a las cámaras (Incremental o Reemplazo total); invitados; Historial → Exportar (Excel / PDF).
- Historia: el residente con el auto del taller (https://gatesentry.com/blog/license-plate-recognition-hoa-gates/).
- Laboratorio: Admin, 20 min. Regla: cargo siempre la cadena completa.

### 12. Lecturas que faltan · producto + web
- Árbol: ¿llegan webhooks? ¿con chapa? ¿modo roadDetection? ANPR y AcuSearch excluyentes; alertas offline, disk, mem, drift, vca; tasa de lectura; checklist de entrega.
- Laboratorio: Campo, 20 min. Regla: diagnostico con el árbol, de la red a la cámara, y nunca agrego un canal LPR a la búsqueda por imagen del NVR.

## Divisiones
- Obturador de noche: 1/1000 para cortar faros (Hikvision) o 1/500 para tráfico lento de barrio (perfil OmniAccess). Decidir por la velocidad real y medir la tasa por hora.
- WDR de noche: probar con y sin (Omada) o apagado (OmniAccess). Arrancar con el perfil y cambiar solo si la tasa nocturna lo pide.
- LPR como credencial única: los críticos dicen que no (gatesentry, Roseville); los distribuidores abren barreras solo con la lista. Decidir dejando siempre un respaldo (guardia, tag, invitado).
- Píxeles mínimos: 100 px (DTK, Manual del Instalador) o 130 px (Hikvision). Apuntar a 150 a 200 px.

## Huecos
- No hay documentación pública de OmniAccess: lo del producto sale de manuales y código, y algunas pantallas dependen de la versión y de la configuración de cada barrio.
- Avicam figura en el README junto a Hikvision, pero en el código es un terminal facial; el curso trata LPR con Hikvision.
- Notificaciones con reglas: el manual las describe para LPR; en esta versión el menú aparece en modo Filas.
- Merodeo sin pantalla propia: se ajusta con claves de configuración.

## Entrega
Tarjeta, guion de dos voces (Lucía y Martín), examen de tres preguntas, ilustración principal y de pasos, conceptos y teoría por lección.
