# Lección 10. Asistencia y hora

**Escuchá:** asistencia-y-hora.mp3 (2 min)

**La idea, en tres líneas**
- Orden: controladora y personas, puntos de marca (entrada, salida o ambos), regla general, plantilla de turno (Normal o Man-Hour), turno, asignación a personas.
- Man-Hour es flexible: no exige ventana de entrada y salida; el cálculo más usado es primera entrada y última salida.
- La plataforma calcula con la hora del servidor y no maneja múltiples zonas horarias: controladoras y SYS en la misma zona.

**Impacto:** reportes de asistencia que cierran el primer mes y pasadas que aparecen en tiempo real.

**Quién lo dice:** 1 de 2 fuentes para la receta (artículo del soporte de Hikvision USA) y 1 de 3 para la zona horaria (FAQ V2.5.500); ambas de Hikvision, evidencia fina. No se encontró quien discrepe.

**Laboratorio** · Admin · 20 min
1. Revisá hora y zona del SYS y de la controladora de laboratorio:
```powershell
Get-TimeZone
w32tm /query /status
```
En la controladora, desde su web local: Configuración > Hora, misma zona que el servidor y NTP apuntando a 192.168.88.10 o al NTP del cliente.
2. Web Client > Attendance > Basic Settings > Attendance Checkpoint > Add: Puerta Lab como entrada y salida.
3. General Rule: fin de semana sábado y domingo; ausente si no hay marca.
4. Shift Settings > Template > Add:
```text
Tipo:              Man-Hour Shift
Horario:           08:00 a 17:00
Cálculo:           primera entrada y última salida
```
5. Shift > Add: repetir por semana, lunes a viernes con la plantilla anterior.
6. Assign Shift Schedule to Person: "Prueba Lab", desde hoy hasta fin de mes. Marcá entrada y salida con la tarjeta.
7. Al día siguiente: Attendance Records, Last 7 Days.

**Regla para quedarse**
Primero la hora, después los turnos.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Receta paso a paso de asistencia en HikCentral (soporte de Hikvision USA): https://supportusa.hikvision.com/support/solutions/articles/17000120924-time-and-attendance-setup-on-hikcentral
- Zona horaria de controladoras y turnos con hora del servidor (FAQ V2.5.500): https://pinfo.hikvision.com/hkwsen/unzip/20240603152919_44907_doc/UD38113B_HikCentral%20Professional%20V2.5.500_FAQ_V2.5.500_20240603.pdf
