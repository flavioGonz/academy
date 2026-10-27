# Lección 10. Diagnóstico facial

**Escuchá:** diagnostico-facial.mp3 (2 min)

**La idea, en tres líneas**
- Una falla facial se separa en cuatro capas, de a una: ¿llega el aviso?, ¿trae foto?, ¿se vincula con la ficha?, ¿el terminal reconoce?
- Las tres primeras se ven en OmniAccess (íconos Push y Pull de Dispositivos, Configuración → Sistema → Webhooks, la ficha del evento); la cuarta vive en el terminal: luz, foto de alta y umbral.
- Bajar el umbral para que "reconozca más" sube las falsas aceptaciones; primero luz y foto.

**Impacto:** resolvés por teléfono o en una visita lo que antes eran tres visitas cambiando cosas al azar.

**Quién lo dice:** 3 de 3 fuentes sobre umbral (Hikvision, AWS, NIST FRTE) coinciden en que subirlo baja falsas aceptaciones y sube falsos rechazos, y ninguna da un valor universal; 3 de 3 (Synerion, Hikvision, Senstar) dicen que la antisuplantación ayuda pero no es infalible; NIST encontró diferencias demográficas en la mayoría de 189 algoritmos.

**Laboratorio** · Foco · 25 min
En una demo, pedile a un compañero que prepare una falla por vez sin decirte cuál. Para cada una, seguí las capas en orden:
1. Capa 1, ¿llega el aviso? Pasá una cara y mirá:
```text
Gestión → Dispositivos Faciales → ícono Push (azul = aviso en los últimos 5 min)
Configuración → Sistema → Webhooks → fuente Akuvox
```
Sin aviso: URL al puerto 10000, firewall, que el terminal llegue al servidor. Con "Dispositivo Desconocido": la MAC de la ficha del equipo no coincide.
2. Capa 2, ¿trae foto? Si el evento llega sin foto, mirá el ícono Pull (verde = OmniAccess pudo consultar el terminal) y los contadores Faces y Tags. Si no responden: usuario y clave de API en Editar Configuración, tipo de autenticación, red de vuelta al terminal. Mirá también la columna Hora / NTP: un reloj corrido complica buscar la foto en el registro del equipo.
3. Capa 3, ¿se vincula? Abrí la ficha del evento:
```text
Nombre correcto + "Autorizado"     → vinculado, todo bien
Nombre correcto + "No registrado"  → el terminal reconoció, OmniAccess no encontró la ficha
"Desconocido"                      → el terminal no reconoció (capa 4)
```
Con Akuvox, OmniAccess vincula buscando una credencial de rostro con el nombre que manda el terminal; en la versión revisada, las fichas creadas desde Usuarios & Residentes no la crean, y con Lista Blanca el evento queda Denegado aunque la puerta abrió. Verificá que el nombre sea idéntico en los dos lados y, si persiste, reportalo a soporte de Infratec con el evento.
4. Capa 4, ¿reconoce? Si el terminal no reconoce a alguien enrolado: revisá la luz a esa hora (lección 2), la foto de alta en Memoria Flash y recién después el umbral del terminal (en Hikvision, nivel de seguridad 1:N). Probá con varias personas distintas, no solo con vos.
5. Anotá cada falla con su capa, el síntoma y la solución en la ficha de la obra.

⚠️ No bajes el umbral del terminal para resolver un caso: abre la puerta a más parecidos para todos. Y la antisuplantación ayuda pero no es infalible: si el lugar pide más seguridad, combiná cara con tarjeta o PIN.

**Regla para quedarse**
De a una capa por vez: aviso, foto, vínculo, reconocimiento.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Nivel de seguridad 1:N y 1:1, liveness y WDR en un terminal Hikvision: https://enpinfo.hikvision.com/hkwsen/unzip/20251224164304_81809_doc/GUID-9F07C169-0B01-4F3E-8729-0BD5189C7613.html
- Umbral de similitud según el uso (AWS Rekognition): https://docs.aws.amazon.com/rekognition/latest/dg/thresholds-collections.html
- FMR y FNMR en la evaluación de NIST (FRTE 1:1): https://pages.nist.gov/frvt/html/frvt11.html
- Estudio de NIST sobre efectos demográficos (2019): https://www.nist.gov/node/1603646
