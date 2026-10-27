import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/windows/src")
from _win import *

# ---------------------------------------------------------------- 7.svg: inicio, recuperación y tarea al inicio
c = Canvas(K(), "Que el servicio arranque solo y vuelva si se cae")
c.add(NOLIG)
c.add(panel(48, 128, 352, 330, "Tipo de inicio", "info"))
types = [("auto", "Automático", "arranca con Windows", "info"),
         ("delayed-auto", "Automático retrasado", "si depende de red o base", "ok"),
         ("demand", "Manual", "solo si alguien lo inicia", "gray"),
         ("disabled", "Deshabilitado", "no arranca", "gray")]
for i, (k, t, s, kd) in enumerate(types):
    y = 194 + i * 58
    c.add(text(72, y, t, 17, 600, OK if kd == "ok" else INK, FB))
    c.add(text(72, y + 24, f"start= {k}", 14, 500, INK3, FM))
c.add(text(72, 424, "Retrasado: si depende de la red", 15, 400, INK2, FB))
c.add(text(72, 446, "o de la base de datos.", 15, 400, INK2, FB))
c.add(panel(424, 128, 728, 330, "Recuperación ante fallas", "info"))
falls = [("1.ª falla", "reiniciar"), ("2.ª falla", "reiniciar"), ("siguientes", "reiniciar")]
for i, (f, act) in enumerate(falls):
    x = 448 + i * 232
    c.add(rect(x, 182, 210, 110, SOFT, CYAN, rx=14))
    c.add(text(x + 18, 216, f, 17, 600, INK, FD))
    c.add(text(x + 18, 246, act, 16, 600, OK, FM))
    c.add(text(x + 18, 274, "a los 3 minutos", 15, 400, INK2, FB))
c.add(rect(448, 316, 680, 56, WHITE, LINE2, rx=12))
c.add(text(468, 350, "Contador a cero después de 24 h sin fallas", 17, 600, INK, FB))
c.add(text(468, 412, "Valores de partida de una plantilla; con failureflag 1 también", 15, 400, INK3, FB))
c.add(text(468, 436, "actúa si el servicio se detiene con error.", 15, 400, INK3, FB))
c.add(panel(48, 482, 1104, 150, "Lo que no es servicio: tarea programada al inicio", "soft"))
for i, s in enumerate(["AtStartup", "NT AUTHORITY\\SYSTEM", "sin sesión iniciada", "RunLevel Highest", "WorkingDirectory"]):
    c.add(tag(72 + [0, 150, 404, 620, 822][i], 572, s, "info", size=14, anchor="start"))
c.add(text(72, 614, "Corre al encender aunque nadie entre al equipo, con privilegios altos y su propia carpeta.", 15, 400, INK2, FB))
save(c, "7.svg")

# ---------------------------------------------------------------- 7-paso2: sintaxis de sc.exe
c = Canvas(K(2), "sc.exe: espacio después del igual y dos unidades")
c.add(NOLIG)
c.add(Step(65, 141, 2))
c.add(text(94, 147, "Recuperación del servicio de prueba Spooler", 17, 600, INK2, FB))
c.add(code(48, 180, 1104, "sc.exe failure Spooler reset= 86400 actions= restart/180000/restart/180000/restart/180000", 16, h=50))
c.add(arrow((420, 236), (420, 300), "flow"))
c.add(arrow((790, 236), (790, 300), "flow"))
c.add(panel(250, 304, 340, 120, None, "info"))
c.add(text(272, 340, "reset= 86400", 18, 600, BLUE, FM))
c.add(text(272, 370, "en segundos: 24 horas", 16, 400, INK2, FB))
c.add(text(272, 398, "sin fallas, el contador vuelve a 0", 15, 400, INK3, FB))
c.add(panel(620, 304, 532, 120, None, "info"))
c.add(text(642, 340, "restart/180000", 18, 600, BLUE, FM))
c.add(text(642, 370, "en milisegundos: 3 minutos", 16, 400, INK2, FB))
c.add(text(642, 398, "una acción por falla: 1.ª, 2.ª y siguientes", 15, 400, INK3, FB))
c.add(Note(48, 452, 540, "reset= 86400 funciona; reset=86400 da error. Lo mismo con start= delayed-auto.", title="El espacio es obligatorio", kind="warn"))
c.add(Note(612, 452, 540, "En PowerShell, sc a secas es Set-Content: escribí siempre sc.exe.", title="sc no es sc.exe", kind="warn"))
save(c, "7-paso2.svg")

# ---------------------------------------------------------------- 7-paso4: la tarea al inicio
c = Canvas(K(4), "Una tarea que corre al arrancar, sin nadie conectado")
c.add(NOLIG)
c.add(Step(65, 141, 4))
c.add(text(94, 147, "Register-ScheduledTask -TaskName 'Lab arranque' -TaskPath '\\Lab\\'", 17, 600, INK2, FM))
parts = [("Acción", "powershell.exe -File C:\\Lab\\arranque.ps1", "con -NoProfile y -ExecutionPolicy Bypass"),
         ("Carpeta", "-WorkingDirectory 'C:\\Lab'", "sin esto, escribe en System32"),
         ("Disparador", "New-ScheduledTaskTrigger -AtStartup", "al encender, sin esperar sesión"),
         ("Cuenta", "-User 'NT AUTHORITY\\SYSTEM' -RunLevel Highest", "como SYSTEM, con privilegios altos")]
for i, (t, cmd, s) in enumerate(parts):
    y = 178 + i * 92
    c.add(text(48, y + 34, t, 18, 600, INK, FD))
    c.add(code(190, y + 6, 560, cmd, 14, h=40))
    c.add(text(774, y + 32, s, 16, 500 if i == 1 else 400, WARN if i == 1 else INK2, FB))
c.add(Note(48, 550, 1104, "Para probar: reiniciá la VM sin iniciar sesión, esperá un minuto, entrá y mirá C:\\Lab\\arranque.log. Al terminar, Unregister-ScheduledTask.", kind="info"))
save(c, "7-paso4.svg")
