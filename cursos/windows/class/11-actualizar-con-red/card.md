# Lección 11. Actualizar con red

**Escuchá:** actualizar-con-red.mp3 (2 min)

**La idea, en tres líneas**
- Se actualiza siempre, con un ciclo definido y validado con el fabricante del VMS (Bosch pide como máximo 6 meses).
- En servidores, Microsoft sugiere que Windows avise antes de instalar y de reiniciar; un equipo sin sesión activa se reinicia cuando le toca.
- Antes de un cambio grande, un backup que sepas restaurar: es la única marcha atrás real.

**Impacto:** reinicios planificados en vez de sorpresas, y una salida real si una actualización rompe algo.

**Quién lo dice:** 3 de 6 fuentes coinciden en controlar el momento (Microsoft, woshub, Windows Latest); TechTarget discrepa y pide actualizaciones automáticas; Bosch, como fabricante de VMS, pide un ciclo máximo de 6 meses.

**Laboratorio** · Admin · 20 min
1. En Windows 11: Configuración > Windows Update > Opciones avanzadas > Horas activas. Ajustalas al horario de operación del cliente.
2. Últimas actualizaciones instaladas y quién reinició por ellas:
```powershell
Get-HotFix | Sort-Object InstalledOn -Descending | Select-Object -First 10
Get-WinEvent -FilterHashtable @{LogName='System'; Id=1074} -MaxEvents 5 |
  Select-Object TimeCreated, Message
```
3. En un Windows Server 2025 de prueba con un segundo disco (E: en este ejemplo), instalá la característica de backup:
```powershell
Install-WindowsFeature Windows-Server-Backup
```
4. Backup de los volúmenes críticos para restaurar el sistema:
```text
wbadmin start backup -backupTarget:E: -allCritical -quiet
wbadmin get versions -backupTarget:E:
```
5. Anotá el identificador de versión y la fecha en la planilla del servidor.
6. Si tenés tiempo, restaurá un archivo de prueba con `wbadmin start recovery` a otra carpeta (`-recoveryTarget`) para confirmar que el backup sirve.

⚠️ Antes de actualizar, backup. Siempre. Y `-recreateDisks` en una restauración borra datos: solo si sabés lo que hace.

**Regla para quedarse**
Antes de actualizar, backup. Siempre.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Server 2022 actualizado solo a 2025 por un error de clasificación: https://windowslatest.com/2024/11/06/windows-server-2022-auto-upgraded-to-windows-server-2025-due-to-api-error
- Cómo maneja Windows los reinicios tras actualizar: https://learn.microsoft.com/en-us/windows/deployment/update/waas-restart
- Recomendación de Bosch para el ciclo de actualizaciones del VMS: https://knowledge.keenfinity-group.com/video-systems/article/what-is-the-recommendation-regarding-the-windows-u
- Referencia de wbadmin: https://ss64.com/nt/wbadmin.html
