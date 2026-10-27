# Lección 9. Qué cambió

**Escuchá:** que-cambio.mp3 (2 min)

**La idea, en tres líneas**
- Ante "ayer andaba", empezá por el Monitor de confiabilidad (`perfmon /rel`): cruza fallas con instalaciones y actualizaciones por día.
- En el Visor de eventos, filtrá con Get-WinEvent -FilterHashtable (log, ID, fecha), que es mucho más rápido que Where-Object.
- 1074 en System dice quién o qué pidió el reinicio; 6008 marca un apagado inesperado (corte o pantallazo azul).

**Impacto:** respondés "por qué se reinició" con fecha, hora y culpable, en vez de suposiciones.

**Quién lo dice:** 2 de 3 fuentes coinciden en filtrar con FilterHashtable (TheITBros y woshub); el Monitor de confiabilidad lo trae TechTarget y los IDs de reinicio woshub; nadie discrepa.

**Laboratorio** · Rápido · 10 min
En tu notebook o una VM, PowerShell como administrador:
1. Abrí el Monitor de confiabilidad (Win+R, `perfmon /rel`), pasá a vista por semanas y buscá el día con el índice más bajo. Anotá qué se instaló ese día.
2. Quién reinició y cuándo:
```powershell
Get-WinEvent -FilterHashtable @{LogName='System'; Id=1074} -MaxEvents 5 |
  Format-List TimeCreated, Message
```
3. Apagados inesperados:
```powershell
Get-WinEvent -FilterHashtable @{LogName='System'; Id=6008} -MaxEvents 5 -ErrorAction SilentlyContinue |
  Select-Object TimeCreated, Message
```
4. Errores y críticos del log Sistema en las últimas 24 horas:
```powershell
Get-WinEvent -FilterHashtable @{LogName='System'; Level=1,2; StartTime=(Get-Date).AddHours(-24)} |
  Select-Object TimeCreated, Id, ProviderName, Message | Format-Table -Wrap
```
5. Tamaño máximo actual del log Sistema, para saber cuánto historial guarda:
```powershell
Get-WinEvent -ListLog System | Select-Object LogName, MaximumSizeInBytes, RecordCount
```
6. Exportá el historial de confiabilidad desde el propio monitor (Guardar historial de confiabilidad) y adjuntalo al informe.

**Regla para quedarse**
Ante una falla, primero pregunto qué cambió y lo busco en Confiabilidad.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Monitor de confiabilidad en servidores: https://www.techtarget.com/it-infrastructure/tip/How-to-use-Reliability-Monitor-to-manage-servers
- Quién reinició un servidor (eventos 1074 y 6008): https://woshub.com/check-shutdown-reboot-logs-windows/
- Filtrar eventos con Get-WinEvent: https://theitbros.com/get-windows-event-logs-powershell/
