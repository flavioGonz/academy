# Plan de lecciones: OmniAccess Face

Diez lecciones en cuatro arcos. Tramo técnico (lecciones 2 a 5) para quien instala; tramo de operación (6 a 8) para guardia, portería y administrador; cierre de administración y diagnóstico (9 y 10). La configuración del equipo en sí (IP, firmware, relé, Action URL en la web del portero, horarios dentro del terminal) se remite al curso **Porteros IP Akuvox: de la caja a la puerta abierta**, sin repetirla.

Fuente de verdad: código y manuales de OmniAccess (Infratec), octubre de 2026. Los manuales de Face (Operador y Administrador) tienen el índice armado y el contenido pendiente; todo lo de pantallas sale del código.

## Arco 1. Entender y montar
Por qué: antes de tocar el panel conviene saber quién abre la puerta y dónde va el terminal, porque los dos errores más caros (esperar que OmniAccess bloquee y montar el equipo a contraluz) salen de ahí.

### 1. Quién decide la puerta
- Quién lo dice: producto + 2 de 2 fuentes (Hikvision, CIE) ubican la decisión en el equipo.
- Idea: el terminal reconoce y abre solo; OmniAccess recibe el evento, lo clasifica con el Modo Face (Lista Blanca o Lista Negra), guarda la foto y lo muestra.
- Por qué importa: cambiar el Modo Face no traba ni libera la puerta; cambia el registro.
- Historia: la propia pantalla de Modo Face dice "La cámara controla la apertura física".
- Practicar: Rápido, 10 min. Configuración → Modos → Modo Face; leer las opciones; mirar cómo cambia el menú.
- Regla: la puerta la abre el terminal; OmniAccess la cuenta.

### 2. Terminal bien parado
- Quién lo dice: 4 de 4 fuentes de instalación dan una altura fija para un rango de estaturas; discrepan en el número (1,1 m ClockRite, 1,30 m Control iD, cámara a 1,48 m Synerion, personas de 1,4 a 1,9 m Hikvision). 5 de 5 piden evitar sol y contraluz.
- Idea: altura según la ficha del modelo, persona a unos 50 cm, de frente, sin sol ni ventana detrás, luz frontal pareja.
- Historia: Synerion pone la cámara a 148 cm y reconoce de 150 a 200 cm de estatura a 50 cm (https://help.synerion.com/agile/knowledge-base/gt-installation-guidelines).
- Practicar: Campo, 20 min. Medir, probar a contraluz, probar con la persona más baja y la más alta.
- Regla: el terminal se monta para la luz de la peor hora del día, no para la del momento de la obra.

## Arco 2. Conectar y sincronizar
Por qué: es el trabajo del técnico en el panel: que el terminal exista con su MAC, que avise, que abra a pedido y que tenga las caras correctas.

### 3. El terminal avisa
- Quién lo dice: producto + 2 de 2 (Wikipedia Webhook, CIE).
- Idea: alta en Dispositivos como Acceso Facial con MAC; Action URL copiada del configurador al puerto 10000; la foto no viaja en el aviso, el servidor la busca en el registro del equipo; el botón Relé abre a pedido.
- Historia: sin MAC que coincida, el servidor descarta el evento ("Event skipped").
- Practicar: Foco, 25 min. Alta, Webhooks (Action URL), prueba de cara, Configuración → Sistema → Webhooks, botón Relé.
- Regla: sin MAC cargada no hay evento; sin red de vuelta al terminal no hay foto.

### 4. Rostros al terminal
- Quién lo dice: 5 de 5 coinciden en la foto frontal con luz pareja; 4 de 4 piden JPG y discrepan en peso (70 KB Speco, 200 KB Hikvision y Akuvox).
- Idea: la ficha guarda la foto; "A qué equipos se manda → Terminales de rostro" la copia; Memoria Flash muestra lo que el equipo tiene de verdad.
- Historia: Hikvision ofrece "Verify by Device" para comprobar que el equipo reconoce la foto al cargarla (https://enpinfo.hikvision.com/unzip/20201102205526_84041_doc/GUID-981B3FAD-F5BA-4E59-8D03-58DB01122125.html).
- Practicar: Foco, 20 min. Nueva persona con foto, envío al terminal, Directorio en Memoria Flash, contador Faces.
- Regla: la persona está enrolada cuando aparece en la memoria del terminal, no cuando se guardó la ficha.

### 5. Grupos y horarios
- Quién lo dice: producto; Hikvision QSG recomienda combinar modos para más seguridad.
- Idea: Grupos de Acceso ordena personas y equipos; la copia al terminal sigue siendo "A qué equipos se manda"; el horario por persona se configura en el terminal (curso Akuvox, lección Usuarios y horarios), porque esta versión no tiene pantalla de horarios para Face.
- Historia: la ayuda de la ficha: "Los grupos dan el permiso; esto copia la credencial a la memoria del equipo".
- Practicar: Admin, 20 min. Crear un grupo, sumarle personas y equipos, poner el horario en el terminal y probarlo fuera de hora.
- Regla: el horario que se cumple es el que está en el terminal.

## Arco 3. Operar en portería
Por qué: es lo que hace el guardia y el administrador todos los días: mirar, entender un evento, enrolar a alguien y manejar visitas y bloqueos.

### 6. Monitor y evento
- Quién lo dice: producto; go2rtc (video) y MDN (push) para lo técnico de fondo.
- Idea: Monitor Facial con Entrada, Capturas Recientes y Salida; filtros Todos, Permitidos y Denegados; LIVE u OFFLINE; la ficha del evento con Registrar y Exportar.
- Historia: un "Desconocido" en ámbar no siempre es un intruso: puede ser alguien reconocido por el terminal sin ficha vinculada.
- Practicar: Rápido, 15 min. Práctica guiada en el Monitor Facial.
- Regla: antes de actuar sobre un Denegado, abrí la ficha y mirá la foto.

### 7. Enrolar en portería
- Quién lo dice: 5 de 5 sobre foto de calidad; 3 de 3 (IMPO art. 9, Dictamen URCDP 3/023, Synerion) sobre consentimiento informado.
- Idea: Registrar desde el evento lleva la foto a una ficha nueva; se revisa la calidad y se manda al terminal; antes, la persona sabe para qué se usa su cara y da su consentimiento.
- Historia: la Ley 18.331 define dato biométrico en el art. 4 literal Ñ, agregado por la Ley 19.924 de 2020 (https://www.impo.com.uy/bases/leyes/18331-2008/4).
- Practicar: Foco, 20 min. De un evento Denegado a una persona enrolada, con el texto de consentimiento.
- Regla: sin consentimiento informado no se saca la foto; sin alternativa (tarjeta o PIN) no se obliga a nadie.

### 8. Visitas y bloqueos
- Quién lo dice: producto; 2 de 2 sobre ciclo de vida de los datos (Dictamen 3/023, Synerion).
- Idea: una visita frecuente se enrola con rol de visita y se le saca la cara al terminar; bloquear a alguien en Face es sacar su cara de la memoria del terminal; borrar la ficha no la borra del equipo.
- Historia: en esta versión, Invitados (pases con QR o matrícula) solo aparece con el módulo LPR; el QR que lee un Akuvox llega como "Código QR Válido" sin cruzarse con las invitaciones.
- Practicar: Admin, 20 min. Alta de una visita, prueba, baja ordenada.
- Regla: la baja se hace primero en el terminal y después en la ficha.

## Arco 4. Administrar y diagnosticar
Por qué: el sistema se sostiene con reportes que respondan preguntas y con un método para las fallas de siempre, cuidando los datos biométricos.

### 9. Historial y reportes
- Quién lo dice: producto; 2 de 2 sobre retención automática (MinIO, Synerion); Dictamen 3/023 sobre ciclo de vida.
- Idea: Historial de Acceso con filtro Rostros, rango y exportación Excel o PDF; Auditoría Hardware para traer lo que el terminal registró sin avisar; retención del Bucket FACE con cuidado.
- Historia: la regla de retención del Bucket FACE se aplica a todo el bucket, también a las fotos de alta (código de Almacenamiento) (https://docs.min.io/community/minio-object-store/administration/object-management/create-lifecycle-management-expiration-rule.html).
- Practicar: Admin, 20 min. Reporte de denegados de una semana, auditoría de doorlog y revisión de la retención.
- Regla: un reporte empieza por la pregunta, y la retención por saber qué se borra.

### 10. Diagnóstico facial
- Quién lo dice: 3 de 3 sobre umbral (Hikvision, AWS, NIST FRTE); 2 de 2 sobre diferencias demográficas (NIST 2019, infodocket); 3 de 3 sobre antisuplantación no infalible.
- Idea: separar por capas: ¿llega el evento? (Push), ¿trae foto? (vuelta al terminal), ¿se vincula? (nombre y ficha), ¿reconoce? (luz, foto, umbral en el terminal).
- Historia: NIST evaluó 189 algoritmos de 99 desarrolladores y encontró diferencias demográficas en la mayoría (https://www.nist.gov/node/1603646).
- Practicar: Foco, 25 min. Recorrido de diagnóstico con cuatro fallas preparadas.
- Regla: de a una capa por vez, desde el cable hasta el umbral.

## Divisiones
- Altura de montaje (1,1 m, 1,30 m, 1,48 m de cámara): manda la ficha del modelo, probada con la persona más baja y la más alta del lugar.
- Peso de la foto (70 KB contra 200 KB): manda el equipo destino; para Akuvox, menos de 200 KB y al menos 640x480.
- Consentimiento como base suficiente: la Ley 18.331 lo pide como regla general; CSO (GDPR) advierte que en una relación laboral no es libre. Ofrecer alternativa sin castigo y consultar al responsable de la base.
- Eventos en la nube (Smart Access de Akuvox) o locales (Action URL): OmniAccess usa local.

## Huecos
- Los manuales de Face (Operador y Administrador) están sin redactar: no hay texto oficial de umbral recomendado, privacidad ni puesta en marcha.
- No hay pantalla de horarios para Face ni uso del modelo Schedule; tampoco se dispara la sincronización por grupos (syncToDevices sin llamadas).
- La ficha creada desde Usuarios no crea credencial de rostro: los eventos Akuvox pueden mostrar el nombre del terminal sin quedar vinculados a la persona.
- No hay notificaciones push ni reglas de notificación para eventos faciales en esta versión.
- La pantalla /admin/dashboard-face (listas negra y blanca, búsqueda por foto con motor externo) no está en el menú: depende de la instalación.
- ZKTeco, Intelbras, Dahua y otras marcas no tienen funciones faciales en el driver; solo Akuvox y Hikvision.

## Entrega
Tarjeta, guion para audio de dos voces (Lucía y Martín) y examen de tres preguntas por lección. Ilustraciones y teoría en ilustraciones/omniaccess-face/.
