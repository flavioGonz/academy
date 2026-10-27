import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/windows/src")
from _win import *

# ---------------------------------------------------------------- 10.svg: tres números y el antivirus
c = Canvas(K(), "El disco que graba se mide con tres números")
c.add(NOLIG)
cards = [("Latencia", "Avg. Disk sec/Transfer", "cuánto tarda cada operación", "más de 25 ms sostenidos: no da abasto", "alert"),
         ("IOPS", "Disk Transfers/sec", "operaciones por segundo", "se compara contra lo que da ese disco", "info"),
         ("Cola", "Avg. Disk Queue Length", "cuántas esperan su turno", "un disco solo: no más de 2", "warn")]
for i, (t, ctr, s, th, kd) in enumerate(cards):
    x = 48 + i * 372
    c.add(panel(x, 128, 352, 230, None, "info"))
    c.add(text(x + 22, 170, t, 24, 600, INK, FD))
    c.add(code(x + 20, 188, 312, ctr, 14, h=36))
    c.add(text(x + 22, 256, s, 16, 400, INK2, FB))
    c.add(rect(x + 20, 280, 312, 56, {"alert": ALERT_BG, "info": SOFT, "warn": WARN_BG}[kd], {"alert": ALERT, "info": LINE2, "warn": WARN}[kd], rx=10, sw=1.5))
    svg, _ = wrap(x + 34, 313, th, 290, 15, 600, {"alert": ALERT, "info": INK2, "warn": WARN}[kd])
    c.add(svg)
c.add(text(48, 392, "Umbrales según woshub; para grabación manda la guía del fabricante del VMS.", 15, 400, INK3, FB))
c.add(panel(48, 414, 1104, 170, "Y el antivirus no escanea la base de grabación", "alert"))
c.add(text(72, 486, "Ejemplo de Milestone:", 16, 600, INK2, FB))
c.add(tag(270, 486, "C:\\mediadatabase", "gray", anchor="start"))
for i, ext in enumerate([".blk", ".idx", ".pic"]):
    c.add(tag(500 + i * 96, 486, ext, "gray", anchor="start"))
svg, _ = wrap(72, 534, "El escaneo consume recursos y puede bloquear archivos: corta la grabación o corrompe la base. Se excluye solo lo que pide el fabricante, nunca un disco entero.", 1050, 16, 400, INK2)
c.add(svg)
save(c, "10.svg")

# ---------------------------------------------------------------- 10-paso3: leer los contadores
c = Canvas(K(3), "Avg. Disk sec/Transfer viene en segundos")
c.add(NOLIG)
c.add(Step(65, 141, 3))
c.add(text(94, 147, "Get-Counter en reposo y copiando un archivo grande (valores de ejemplo)", 17, 600, INK2, FB))
c.add(rect(48, 176, 1104, 92, SOFT, CYAN, rx=14))
c.add(text(80, 234, "0,025 s", 30, 700, BLUE, FM))
c.add(text(260, 234, "×  1000  =", 22, 600, INK3, FM))
c.add(text(470, 234, "25 ms", 30, 700, ALERT, FM))
c.add(text(640, 230, "el umbral de woshub para", 16, 500, INK2, FB))
c.add(text(640, 254, "latencia sostenida", 16, 500, INK2, FB))
for i, (t, kd, lat, latv, iops, q, qv) in enumerate([("En reposo", "ok", "0,002 s", 0.08, "40", "0,1", 0.05), ("Copiando un archivo grande", "alert", "0,031 s", 1.0, "110", "3,4", 1.0)]):
    x = 48 + i * 564
    c.add(panel(x, 296, 540, 300, t, kd if kd == "ok" else "alert"))
    c.add(gauge(x + 24, 370, 490, "Latencia", lat, "", latv, "ok" if kd == "ok" else "alert", mark=0.81, mark_label="25 ms"))
    c.add(text(x + 24, 466, "IOPS", 17, 600, INK, FB))
    c.add(text(x + 514, 466, iops, 17, 600, INK2, FM, anchor="end"))
    c.add(gauge(x + 24, 504, 490, "Cola", q, "", qv, "ok" if kd == "ok" else "alert", mark=0.59, mark_label="2"))
save(c, "10-paso3.svg")

# ---------------------------------------------------------------- 10-paso4: exclusiones de Defender
c = Canvas(K(4), "Excluí solo lo que pide el fabricante del VMS")
c.add(NOLIG)
c.add(Step(65, 141, 4))
c.add(text(94, 147, "Microsoft Defender, PowerShell como administrador", 17, 600, INK2, FB))
sv, h = console(48, 172, 1104, [
    ">(Get-MpPreference).ExclusionPath",
    ">Add-MpPreference -ExclusionPath 'D:\\LabGrabacion'",
    ">Add-MpPreference -ExclusionExtension '.blk','.idx','.pic'",
])
c.add(sv)
c.add(panel(48, 340, 540, 150, None, "ok"))
c.add(Mark(86, 380, ok=True))
c.add(text(118, 387, "La carpeta de grabación", 19, 600, OK, FD))
svg, _ = wrap(72, 426, "Las carpetas, extensiones y procesos que indique el fabricante del VMS instalado, anotados en el informe.", 490, 16, 400, INK2)
c.add(svg)
c.add(panel(612, 340, 540, 150, None, "alert"))
c.add(Mark(650, 380, ok=False))
c.add(text(682, 387, "Un disco entero \"por las dudas\"", 19, 600, ALERT, FD))
svg, _ = wrap(636, 426, "Excluir reduce la protección: lo que no se escanea, no se revisa. Solo lo que pide el fabricante.", 490, 16, 400, INK2)
c.add(svg)
c.add(Note(48, 516, 1104, "Al terminar el laboratorio, Remove-MpPreference con los mismos parámetros deja todo como estaba.", kind="info"))
save(c, "10-paso4.svg")
