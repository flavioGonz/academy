# Lección 10. Reportes programados

**Escuchá:** reportes-programados.mp3 (2 min)

**La idea, en tres líneas**
- Reportes (Reportes de Afluencia) da el aforo por hora (intervalos de 5, 15, 30, 45 min o 1 h), por día, por semana y por mes, exporta a Excel o PDF con la marca del cliente y lista los cortes de conexión de cámara del período.
- Los reportes programados (Notificaciones → Horarios) mandan a la hora elegida un resumen: pico con su hora, promedio, alertas, lecturas, cortes y horas críticas. "Reporte diario" y "Reporte semanal" en Despachos lo mandan en el momento.
- En esta versión el resumen sale por el Telegram configurado sea cual sea el canal elegido, cuenta solo el canal "Aforo" y la hora se compara con el reloj del servidor.

**Impacto:** el cliente recibe cada mañana la historia de su fila, con los huecos explicados.

**Quién lo dice:** el contenido de los reportes sale del código de OmniAccess. De la web, Little (1 de 1 sobre intervalos finitos) defiende medir en una ventana cerrada como un día de tienda; evidencia fina.

**Laboratorio** · Admin · 15 min
Instalación de prueba con datos de al menos un día.
1. Abrí Reportes → "Por Hora". Elegí la fecha de hoy, la fila "Fila Caja 1" e intervalo de 15 min.
2. Leé las columnas: Intervalo, Aforo exacto (última lectura del intervalo), Máximo, Promedio, Lecturas. Bajá hasta "Cortes de conexión de cámara".
3. Exportá en PDF y en Excel. Si el PDF sale sin logo, cargalo en Configuración → Branding → Reportes Exportables.
4. Abrí `/admin/notificaciones` → pestaña Horarios → "Nuevo":
```text
Nombre:      Resumen diario
Frecuencia:  Diario
Hora:        21:30
Canal:       Telegram
```
5. En el servidor, revisá la zona horaria y la tarea que dispara los reportes:
```bash
timedatectl | grep "Time zone"        # conviene America/Montevideo
crontab -l | grep report/tick
```
6. Abrí Despachos y tocá "Reporte diario". Seguí el despacho hasta Enviado y leé el mensaje en Telegram: pico, promedio, alertas, lecturas, cortes y horas críticas.
7. Compará "Alertas emitidas" con la lista de alertas de Despachos: en esta versión ese número sale de un registro de canales anterior y puede quedar en 0 aunque haya habido alertas. Para contarlas, Despachos.

⚠️ Si el servidor está en hora universal (UTC), un reporte programado a las 22:00 sale a las 19:00 de Uruguay. Antes de cambiar la zona horaria de un servidor en producción, coordiná: afecta a todos los servicios de esa máquina.

**Regla para quedarse**
Un reporte sin la lista de cortes cuenta media historia.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- La ley de Little en intervalos finitos, por su autor (2011): https://projectproduction.org/journal/reprint-littles-law-as-viewed-on-its-50th-anniversary/
- Por qué los acumulados necesitan un punto de reinicio (Axis): https://developer.axis.com/analytics/axis-object-analytics-counting-data
