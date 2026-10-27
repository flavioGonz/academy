# Lección 7. Que se levante

**Escuchá:** que-se-levante.mp3 (2 min)

**La idea, en tres líneas**
- El servicio del VMS va en automático (o automático retrasado si depende de red o base de datos) y con recuperación: reiniciar ante falla.
- Valores de partida de una plantilla: reiniciar a los 3 minutos en cada falla y resetear el contador cada 24 horas.
- Lo que no es servicio va como tarea programada al inicio, sin sesión iniciada, con privilegios altos y carpeta de inicio definida.

**Impacto:** una caída del servicio a la madrugada se resuelve sola en minutos, no el lunes.

**Quién lo dice:** 2 de 2 fuentes coinciden en recuperación de servicios (evidencia fina): la referencia de SS64 y la plantilla de Octopus; para tareas, una sola fuente (LazyAdmin); nadie discrepa.

**Laboratorio** · Foco · 15 min
En una VM, PowerShell como administrador. Usá un servicio de prueba que se pueda reiniciar sin riesgo, por ejemplo Spooler (cola de impresión):
1. Tipo de inicio y recuperación actual:
```powershell
Get-Service Spooler | Select-Object Name, Status, StartType
sc.exe qc Spooler
sc.exe qfailure Spooler
```
2. Automático retrasado y recuperación (espacio después de cada igual):
```powershell
sc.exe config Spooler start= delayed-auto
sc.exe failure Spooler reset= 86400 actions= restart/180000/restart/180000/restart/180000
sc.exe failureflag Spooler 1
```
3. Simular la caída y mirar cómo vuelve en unos 3 minutos:
```powershell
Stop-Process -Name spoolsv -Force
Get-Service Spooler
```
4. Tarea al inicio, como SYSTEM, sin sesión:
```powershell
New-Item -ItemType Directory C:\Lab -Force
Set-Content C:\Lab\arranque.ps1 'Add-Content C:\Lab\arranque.log (Get-Date)'
$a = New-ScheduledTaskAction -Execute 'powershell.exe' `
  -Argument '-NoProfile -ExecutionPolicy Bypass -File C:\Lab\arranque.ps1' -WorkingDirectory 'C:\Lab'
$t = New-ScheduledTaskTrigger -AtStartup
Register-ScheduledTask -TaskName 'Lab arranque' -TaskPath '\Lab\' -Action $a -Trigger $t `
  -User 'NT AUTHORITY\SYSTEM' -RunLevel Highest
```
5. Reiniciá la VM sin iniciar sesión, esperá un minuto, entrá y mirá `C:\Lab\arranque.log`.
6. Al terminar, volvé el servicio a como estaba (`start= auto`) y borrá la tarea con `Unregister-ScheduledTask -TaskName 'Lab arranque' -Confirm:$false`.

⚠️ No practiques matando el servicio del VMS en producción: el corte de grabación es real.

**Regla para quedarse**
Todo servicio crítico tiene recuperación configurada y probada.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Referencia de sc.exe (config, failure, qfailure): https://ss64.com/nt/sc.html
- Plantilla de recuperación ante fallas: https://octopus.com/integrations/windows/windows-service-set-recovery-on-failure-actions
- Tareas programadas con PowerShell: https://lazyadmin.nl/powershell/how-to-create-a-powershell-scheduled-task/
