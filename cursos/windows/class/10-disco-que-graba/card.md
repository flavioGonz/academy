# Lección 10. Disco que graba

**Escuchá:** disco-que-graba.mp3 (2 min)

**La idea, en tres líneas**
- Al disco de grabación se lo mide con tres números: latencia (Avg. Disk sec/Transfer), IOPS (Disk Transfers/sec) y cola (Avg. Disk Queue Length).
- Según woshub, más de 25 ms de latencia sostenida es un disco que no da abasto, y la cola de un disco solo no debería pasar de 2.
- El antivirus no escanea la base de grabación: Milestone excluye C:\mediadatabase y los archivos .blk, .idx y .pic, porque el escaneo puede cortar la grabación o corromper la base.

**Impacto:** pérdida de cuadros explicada con números y sin bloqueos del antivirus sobre la grabación.

**Quién lo dice:** evidencia fina: los umbrales salen de una sola fuente (woshub) y las exclusiones de otra (documentación de Milestone); no se contradicen, y para grabación manda la guía de cada fabricante de VMS.

**Laboratorio** · Foco · 15 min
En una VM o PC de banco, PowerShell como administrador:
1. Vista rápida: Administrador de tareas (Ctrl+Shift+Esc) > Rendimiento > Disco, tiempo medio de respuesta. Después `resmon` > pestaña Disco > Almacenamiento, longitud de cola.
2. Un minuto de contadores en reposo (los nombres de contador están en inglés; en Windows en español pueden figurar traducidos):
```powershell
$c = '\PhysicalDisk(_Total)\Avg. Disk sec/Transfer',
     '\PhysicalDisk(_Total)\Disk Transfers/sec',
     '\PhysicalDisk(_Total)\Avg. Disk Queue Length'
Get-Counter -Counter $c -SampleInterval 5 -MaxSamples 12
```
3. Repetí el paso 2 mientras copiás un archivo grande a ese disco y compará. Avg. Disk sec/Transfer viene en segundos: 0,025 son 25 ms.
4. Exclusiones de Defender actuales y una de laboratorio:
```powershell
(Get-MpPreference).ExclusionPath
New-Item -ItemType Directory D:\LabGrabacion -Force
Add-MpPreference -ExclusionPath 'D:\LabGrabacion'
Add-MpPreference -ExclusionExtension '.blk','.idx','.pic'
```
5. En un servidor real, cargá las exclusiones de carpetas, extensiones y procesos que indique el fabricante del VMS instalado y dejalas anotadas en el informe.
6. Al terminar el laboratorio, quitá lo que agregaste con `Remove-MpPreference` y los mismos parámetros.

⚠️ Excluir carpetas reduce la protección: solo las que pide el fabricante, nunca un disco entero "por las dudas".

**Regla para quedarse**
El disco de grabación se mide y se excluye del antivirus según el fabricante.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Medir latencia, IOPS y cola de disco en Windows: https://woshub.com/how-to-measure-disk-iops-using-powershell/
- Exclusiones de antivirus en Milestone XProtect: https://doc.milestonesys.com/2025R1/en-US/standard_features/sf_mc/sf_considerationsrequirements/mc_virusscanningexclusionsexplained.htm
