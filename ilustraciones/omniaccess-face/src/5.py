import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/omniaccess-face/src")
from _face import *

# ---------------------------------------------------------------- 5.svg: grupo, copia y horario
c = Canvas("OmniAccess Face · Lección 5", "Tres cosas distintas: grupo, copia y horario")
cols = [(48, "1 · Grupo de Acceso", "en OmniAccess", "Personas × equipos = quién pasa por dónde. Documenta el permiso y se ve en la ficha.", "info", "Gestión → Grupos de Acceso"),
        (436, "2 · La copia", "en OmniAccess → terminal", "\"A qué equipos se manda\" copia la cara a la memoria del terminal. Sin copia no reconoce.", "ok", "Ficha → Terminales de rostro"),
        (824, "3 · El horario", "en el terminal", "OmniAccess manda a cada persona con el horario \"siempre\". El horario por persona se pone en el equipo.", "warn", "Web del terminal (curso Akuvox)")]
for x, t_, s_, body, kind, path in cols:
    c.add(card(x, 130, 328, 330))
    c.add(text(x + 20, 168, t_, 20, 600, INK, FD))
    c.add(text(x + 20, 194, s_, 15, 500, INK3, FM))
    c.add(Note(x + 16, 214, 296, body, kind=kind, size=16))
    c.add(text(x + 20, 440, path, 15, 600, BLUE, FM))
c.add(Arrow((378, 300), (434, 300), kind="flow"))
c.add(Arrow((766, 300), (822, 300), kind="flow"))
c.add(Note(48, 490, 1104, "En esta versión el grupo no copia nada solo y no hay pantalla de horarios para Face. Si reenviás la ficha, revisá que el horario siga en el terminal.", title="Lo que hace y lo que no hace OmniAccess", kind="info", size=16))
save(c, "5.svg")

# ---------------------------------------------------------------- 5-paso5: el reenvío puede pisar el horario
c = Canvas("OmniAccess Face · Lección 5 · Paso 5", "Reenviá la ficha y mirá si el horario sigue")
steps_ = [("Horario manual en el terminal", "Ana · L a V 8:00 a 17:00", "ok"),
          ("Cambio en la ficha y reenvío", "OmniAccess actualiza a Ana en el equipo", "info"),
          ("Horario después del reenvío", "puede volver a \"siempre\" (1001)", "alert")]
for i, (t_, s_, k) in enumerate(steps_):
    x = 48 + i * 380
    col = {"ok": OK, "info": BLUE, "alert": ALERT}[k]
    c.add(card(x, 150, 340, 120, stroke=col, sw=2.5))
    c.add(text(x + 20, 196, t_, 18, 600, INK, FB))
    c.add(text(x + 20, 228, s_, 15, 500, INK2, FM if i != 1 else FB))
    if i < 2:
        c.add(Arrow((x + 344, 210), (x + 376, 210), kind="flow"))
c.add(Step(48, 150, 5))
c.add(Note(48, 310, 540, "Después de cada reenvío, abrí la web del terminal y confirmá el horario de esa persona.", title="Qué hacer", kind="ok", size=16))
c.add(Note(612, 310, 540, "Anotá en la ficha de la obra quién tiene horario en el terminal y quién lo cargó.", title="Para el que viene después", kind="info", size=16))
save(c, "5-paso5.svg")
