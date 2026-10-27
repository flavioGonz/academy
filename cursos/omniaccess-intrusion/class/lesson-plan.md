# Plan: OmniAccess Intrusión

Público: técnicos de IES (instalación y soporte) y operadores (guardia, puesto de monitoreo, administrador del barrio). Nivel inicial a intermedio. 10 lecciones en 4 arcos.

Fuente de verdad: el código de OmniAccess de octubre de 2026 (rama de desarrollo más reciente). El módulo no tiene manual propio: los nombres de pantallas, botones, estados y tiempos salen del código (research/notes/b.md). Las 30 páginas de raw/web cubren la teoría y el hardware: documentación de fabricantes (Hikvision, Milesight, Uniview, Ajax, Bosch, Trassir), estándares (ONVIF Analytics, RTSP 2.0, Web Push), herramientas (go2rtc, MinIO, Telegram Bot API), practicantes (Home Assistant, ipcamtalk, cctvcamerapros, alarmserver) y centrales de monitoreo (SDM, Security Sales, SecurityInfoWatch, Davantis).

Cómo leer "N de M": M son las páginas que tocan el subtema, N las que sostienen la idea. Lo que hace OmniAccess no se cuenta: es el producto.

Datos de ejemplo en todo el curso: servidor OmniAccess 192.0.2.10 (webhooks en el puerto 10000), NVR 192.0.2.50, cámaras 192.0.2.21 a 192.0.2.29, "Barrio Ejemplo", cámaras "Perímetro Norte 12" y "Perímetro Sur 07".

## Arco 1. Entender el sistema
Por qué este arco: antes de tocar una cámara hay que saber quién detecta (la cámara o el NVR), por dónde llega el aviso y qué hace OmniAccess con él. Cierra con el recorrido completo de una detección dibujado en una hoja.

### Lección 1. Camino del evento
- Quién lo dice: 5 de 5 (TH01), 4 de 6 (TH02).
- Idea: la cámara o el NVR detectan; OmniAccess recibe, guarda, pide la foto y avisa. Hikvision empuja el evento al servidor de alarma (puerto 10000); con Dahua OmniAccess se suscribe al NVR. El movimiento simple se descarta. Por ONVIF no entra nada en esta versión.
- Por qué importa: la mitad de los "no anda" se explican sabiendo de qué lado está la falla.
- Historia: el movimiento simple se dejó afuera porque generaba miles de eventos e imágenes (b:N2). Home Assistant: solo se ven los eventos marcados para notificar al centro (https://www.home-assistant.io/integrations/hikvision).
- Laboratorio: Rápido, 10 min. Recorrer Dispositivos → Intrusión y el Monitor Intrusión de la demo, anotar marca, NVR y vía de cada cámara.
- Regla: primero sabé quién detecta y por dónde avisa; después tocá.

## Arco 2. Instalar y configurar
Por qué este arco: es el trabajo del técnico en obra: la regla en la cámara, el alta con el aviso a OmniAccess, el horario en que avisa y dónde suena. Cierra con una cámara de perímetro que dispara, llega al monitor y suena en la pared.

### Lección 2. Regla en cámara
- Quién lo dice: 4 de 5 (TH05), 4 de 4 (TH08), 2 de 5 (TH06).
- Idea: la línea o la zona viven en la cámara (o en el NVR Dahua). El calibrador de OmniAccess dibuja línea y zona sobre un cuadro real, cambia sentido, sensibilidad (40, 60, 80) y objetivo, y escribe en la cámara. Auto-perfil: 60, personas y vehículos, aviso a OmniAccess.
- Por qué importa: una línea mal puesta genera ruido o, peor, no ve al que pasa.
- Historia: la recomendación de Ajax de no pegar la línea al borde ni a árboles y probar siempre (https://ajax.systems/support/posts/line-crossing-detection-in-ajax-video-surveillance/).
- Laboratorio: Foco, 20 min. Calibrar "Perímetro Norte 12": línea a lo largo del cerco con sentido A→B, sensibilidad 60, objetivo personas, y caminar la escena.
- Regla: la línea corta todo el camino, lejos del borde, y se prueba caminando.

### Lección 3. Alta y aviso
- Quién lo dice: 2 de 2 (TH03), 2 de 2 (TH12), 2 de 2 (TH11).
- Idea: Dispositivos → Agregar → Cámara de intrusión, o importar desde el NVR clasificando cada canal. Después, Servidor de alarma: "Configurar OmniAccess como alarma" y "Probar reporte"; con Dahua, "Verificar suscripción". En la cámara Hikvision, la vinculación del evento con "Notificar al centro de vigilancia".
- Por qué importa: sin aviso, la cámara detecta y nadie se entera.
- Historia: el test de la notificación HTTP manda un POST vacío y espera un 200 (https://videos.cctvcamerapros.com/developer/docs/getting-started/http-post-setup).
- Laboratorio: Campo, 25 min. Importar canales del NVR de demo como intrusión, configurar el servidor de alarma de una cámara Hikvision, probar y cruzar la línea.
- Regla: una cámara de intrusión no está dada de alta hasta que cruzaste su línea y la viste llegar.

### Lección 4. Horario de armado
- Quién lo dice: 4 de 4 (TH09), 2 de 4 (TH10).
- Idea: cada regla tiene su horario en la cámara; fuera de él la cámara graba pero no avisa. OmniAccess lo lee y lo muestra ("L–D 22:00–06:00", punto verde o ámbar). En esta versión se cambia en la web de la cámara. El Mapa tiene su propio horario de aviso, que solo silencia el mapa.
- Por qué importa: un perímetro "activo" que de noche no avisa es la falla más cara.
- Historia: Hikvision cuenta que el error común es armado de día y apagado de noche (https://supportusa.hikvision.com/support/solutions/articles/17000129443-why-is-the-arming-schedule-important-).
- Laboratorio: Admin, 15 min. Leer el armado de tres cámaras en la vista de pared, poner una en 22:00 a 06:00 desde su web y verificar el cambio.
- Regla: el horario de armado se mira en cada cámara, de noche, antes de entregar.

### Lección 5. Avisos y pantallas
- Quién lo dice: 2 de 4 (TH22), 2 de 2 (TH23).
- Idea: en esta versión la intrusión avisa en pantallas: el canal rojo del Monitor Intrusión, el Mapa (pitido y voz) y las pantallas de pared con sonido configurable. Telegram avisa la salud de los equipos. No hay regla de intrusión por Telegram, WhatsApp ni push.
- Por qué importa: el cliente pregunta "¿me llega al celular?" y la respuesta honesta evita un reclamo.
- Historia: Davantis insiste en que la alarma llegue calificada y con el video a un clic (https://www.davantis.com/wp-content/uploads/perimeter-security-false-alarms-guide.pdf).
- Laboratorio: Admin, 20 min. Crear un enlace de pantalla de Intrusión, sonido "Repetir hasta que se acepte", abrirlo en kiosco; dibujar la línea de una cámara en el Mapa.
- Regla: decile al cliente dónde suena la alarma y dónde no, por escrito.

## Arco 3. Operar
Por qué este arco: es el turno del operador: decidir si es real, mirar en vivo y la grabación, dejar registro y coordinar al guardia. Cierra con una alarma de prueba atendida de punta a punta.

### Lección 6. Atender la alarma
- Quién lo dice: 4 de 4 (TH17), 1 de 2 (TH18), 1 de 2 (TH19).
- Idea: canal rojo, "Aceptar alarma", la ficha con la foto; el análisis y el mapa del cruce están en la ficha de la detección de la vista de pared Intrusión; Confirmar real (A) o Falsa alarma (F); real queda "En atención" hasta Resolver. La decisión vale para lo pendiente de esa cámara en 6 horas.
- Por qué importa: decidir rápido y bien, con datos, es lo que el sistema le pide al operador.
- Historia: "Stick to the facts" (https://www.sdmmag.com/articles/89047-video-monitoring-best-practices); la central que despacha una vez por zona por hora (https://www.securitysales.com/insights/central-stations-assess-actual-alarms/147248/).
- Laboratorio: Foco, 15 min. Atender una alarma de prueba con el teclado, leer los indicios, resolverla.
- Regla: decidí con la foto, el análisis y el vivo, y dejá la cámara resuelta.

### Lección 7. Vivo y grabación
- Quién lo dice: 2 de 3 (TH20).
- Idea: Ver en vivo con pestañas Vivo, Grabación y Evidencia; SD o HD; PTZ si el nombre dice PTZ; seguimiento visual entre cámaras; grabación del NVR con línea de tiempo y velocidad; descargar o mandar el clip por WhatsApp.
- Por qué importa: la foto dice que pasó algo; el video dice qué y hacia dónde fue.
- Historia: go2rtc adapta el RTSP al navegador y transcodifica solo si hace falta (https://pkg.go.dev/github.com/AlexxIT/go2rtc).
- Laboratorio: Foco, 20 min. Armar el seguimiento visual entre dos cámaras vecinas y bajar un clip de un evento.
- Regla: antes de decir "no hay nada", mirá los 10 segundos de antes en la grabación.

### Lección 8. Registro y guardia
- Quién lo dice: 2 de 2 (TH21), 2 de 4 (TH24).
- Idea: Historial y Evidencia con filtros (tipo, cámara, estado, fechas), corrección de una detección ("Era falsa alarma", "Fue real"), retención del bucket de intrusión. La tablet del guardia no recibe la alarma: el puesto lo ve en el Mapa y lo manda por radio.
- Por qué importa: el registro es lo que queda para el administrador y para un reclamo.
- Historia: grabar lo que vio el operador ayuda a que sirva como evidencia (https://www.sdmmag.com/articles/89047-video-monitoring-best-practices).
- Laboratorio: Admin, 15 min. Buscar las pendientes de anoche de una cámara, corregir una y ubicar al guardia más cercano en el Mapa.
- Regla: ninguna detección termina el turno como pendiente.

## Arco 4. Afinar y diagnosticar
Por qué este arco: con el sistema andando, el trabajo es que avise solo cuando importa y saber dónde mirar cuando no avisa. Cierra con un plan de ajuste mensual y una lista de diagnóstico.

### Lección 9. Menos falsas alarmas
- Quién lo dice: 4 de 5 (TH14), 2 de 5 (TH15), 1 de 5 (TH16).
- Idea: en orden: posición y limpieza, regla (sentido, zona, sensibilidad), objetivo persona o vehículo, y medir. El Análisis de OmniAccess da los números: ráfaga, ritmo contra 7 días, porcentaje de falsas de las últimas 50 revisadas.
- Por qué importa: un operador saturado deja pasar la alarma verdadera.
- Historia: la alarma 501 (https://www.davantis.com/wp-content/uploads/perimeter-security-false-alarms-guide.pdf); gatos y pájaros con porcentaje al 90 % (https://ipcamtalk.com/threads/intrusion-detection-settings-does-not-work.24107).
- Laboratorio: Admin, 20 min. Elegir la cámara con más falsas de la semana, leer su análisis, aplicar un cambio y medir.
- Regla: un cambio por vez, y se mide una semana.

### Lección 10. Cuando no llega
- Quién lo dice: 2 de 2 (TH12), 1 de 2 (TH13), 2 de 3 (TH04).
- Idea: de la cámara al monitor: armado, vinculación "Notificar al centro", servidor de alarma y prueba, host de eventos y puerto 10000, cámara dada de alta con su IP o MAC, credenciales para la foto, NVR y canal para la grabación, hora; con Dahua, NVR alcanzable.
- Por qué importa: el diagnóstico ordenado ahorra visitas.
- Historia: el usuario necesita el permiso de notificar al centro y autenticación digest (https://www.home-assistant.io/integrations/hikvision).
- Laboratorio: Campo, 25 min. Romper a propósito tres eslabones en la demo y encontrarlos con la lista.
- Regla: diagnosticá de la cámara hacia el monitor, un eslabón por vez.

## Divisiones
- Push o suscripción: cctvcamerapros y la propia Hikvision empujan el evento al servidor; alarmserver y el script de Dahua se suscriben. OmniAccess usa push con Hikvision y suscripción al NVR con Dahua. Decidir: lo decide la marca del equipo que analiza.
- Sensibilidad o clasificación: Trassir y Milesight ponen la sensibilidad como perilla principal; ipcamtalk muestra que sin clasificación no alcanza. Decidir: con cámara AcuSense, primero objetivo persona; sin clasificación, reubicar y achicar la zona antes de tocar la sensibilidad.
- Filtrar en el sitio o verificar con una persona: Davantis prefiere decidir en el sitio con análisis continuo; las centrales verifican con video y con el cliente. Decidir: OmniAccess pone la decisión en el operador con la foto y los indicios; el ajuste en la cámara baja el ruido antes.

## Huecos
- La documentación oficial de Hikvision sobre cruce de línea e intrusión no se pudo leer (403); se usan distribuidores y otros fabricantes con la misma lógica.
- No hay fuente pública de OmniAccess: lo del producto sale del código y se nombra por pantalla.
- Funciones del código a medio hacer que el curso no enseña como terminadas: el editor de horario de armado desde OmniAccess, la alerta global en el panel, la verificación omni-vision y los avisos de intrusión por Telegram, WhatsApp o push.

## Entrega
10 lecciones con guion (dos voces), tarjeta y quiz de 3 preguntas; ilustraciones y teoría por lección en ilustraciones/omniaccess-intrusion. Sin audio: lo renderiza el orquestador.
