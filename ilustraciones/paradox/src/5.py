import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/paradox/src")
from _pdx import *

# ---------------------------------------------------------------- 5.svg: anatomía de la programación SP/MG
c = Canvas(K(), "ENTER, código, sección y dato: tres formas de dato")
c.add(NOLIG)
sv, xe = keys(48, 130, ["[ENTER]", "+", "0000", "+", "[710]", "+", "045"], 20)
c.add(sv)
for x, y, lab in [(90, 200, "entrar"), (208, 222, "código de instalador"), (314, 200, "sección, 3 dígitos"), (413, 222, "dato")]:
    c.add(text(x, y, lab, 15, 500, INK3, FB, anchor="middle"))
cards = [("Decimal", "000 a 255", "Tiempos y cantidades. [710] = 045: retardo de entrada de 45 s.", None),
         ("Hexadecimal", "la tecla 0 vale A", "ID, abonados y contraseñas. B a F van con teclas de función.", None),
         ("Opciones 1 a 8", "cada tecla prende o apaga", "Opción encendida = tecla iluminada. ENTER guarda.", {1, 2, 3, 8})]
for i, (t, s, d, on) in enumerate(cards):
    x = 48 + i * 376
    c.add(panel(x, 236, 352, 236, t, "info"))
    c.add(text(x + 20, 292, s, 17, 600, BLUE, FM))
    svg, _ = wrap(x + 20, 328, d, 312, 16, 400, INK2)
    c.add(svg)
    if on:
        c.add(opts(x + 20, 410, on, size=32, gap=6))
c.add(panel(48, 494, 540, 112, None, "ok"))
s_, _ = keycap(72, 518, "ENTER", 16); c.add(s_)
c.add(text(170, 534, "apenas entrás a la sección,", 17, 600, INK, FB))
c.add(text(170, 560, "antes de cargar: muestra sin cambiar", 17, 600, OK, FB))
c.add(panel(612, 494, 540, 112, None, "warn"))
s_, _ = keycap(636, 518, "CLEAR", 16); c.add(s_)
c.add(text(734, 534, "sale de la sección", 17, 600, INK, FB))
c.add(text(734, 560, "sin guardar lo que tecleaste", 17, 600, WARN, FB))
save(c, "5.svg")

# ---------------------------------------------------------------- 5-paso1: modo visualización
c = Canvas(K(1), "Mirá la sección antes de escribirla")
c.add(NOLIG)
c.add(Step(48, 140, 1))
sv, _ = keys(80, 124, ["[ENTER]", "+", "0000", "+", "[710]"], 18)
c.add(sv)
c.add(text(470, 150, "retardo de entrada 1", 17, 500, INK3, FB))
seq = [("ENTER", "0", "1.er dígito"), ("ENTER", "4", "2.º dígito"), ("ENTER", "5", "3.er dígito")]
for i, (k, d, lab) in enumerate(seq):
    x = 80 + i * 300
    s_, w = keycap(x, 236, k, 17); c.add(s_)
    c.add(Arrow((x + w + 10, 256), (x + w + 50, 256)))
    c.add(rect(x + w + 60, 214, 90, 84, "#0B3A66", "#0B3A66", rx=12))
    c.add(mid(x + w + 105, 272, d, 36, 700, "#9FE3F7", FM))
    c.add(mid(x + w + 105, 326, lab, 15, 500, INK3, FB))
c.add(rect(80, 360, 760, 64, OK_BG, OK, rx=14))
c.add(text(104, 400, "045 = 45 segundos, el valor de fábrica. No cambiaste nada.", 18, 600, OK, FB))
s_, _ = keycap(880, 372, "CLEAR", 17); c.add(s_)
c.add(text(980, 398, "sale", 17, 600, INK2, FB))
c.add(Note(48, 456, 540, "Si seguís con ENTER, la central pasa a la sección siguiente: así se recorre la programación sin tocarla.", title="Sigue a la próxima", kind="info"))
c.add(Note(612, 456, 540, "Si tecleás un número antes del primer ENTER, estás escribiendo el dato. Primero ENTER, después mirás.", title="El orden importa", kind="warn"))
save(c, "5-paso1.svg")

# ---------------------------------------------------------------- 5-paso2: las llaves del primer día
c = Canvas(K(2), "Las tres llaves de la central, el primer día")
c.add(NOLIG)
cards = [("[397]", "Código de instalador", "0000", "uno propio de la obra", "4 o 6 dígitos. Ni 0000, ni 1234, ni una fecha.", "alert", 2),
         ("[399]", "Maestro del sistema", "1234", "uno propio del cliente", "No se puede borrar, solo cambiar.", "alert", 3),
         ("[398]", "Mantenimiento", "vacío", "solo si hace falta", "Programa casi todo, menos comunicación ([815] a [817], [910], [911], [918] a [949]) y códigos.", "gray", 4)]
for i, (sec, t, fab, new, d, kd, stp) in enumerate(cards):
    x = 48 + i * 376
    c.add(panel(x, 124, 352, 360, None, "info"))
    c.add(Step(x, 124, stp))
    c.add(text(x + 24, 168, sec, 22, 700, BLUE, FM))
    c.add(text(x + 24, 198, t, 19, 600, INK, FD))
    c.add(text(x + 24, 244, "FÁBRICA", 13, 600, INK3, FM, ls=1.5))
    c.add(tag(x + 24, 280, fab, kd, 18, anchor="start"))
    c.add(text(x + 24, 324, "QUEDA", 13, 600, INK3, FM, ls=1.5))
    c.add(text(x + 24, 352, new, 17, 600, OK if kd == "alert" else INK2, FB))
    svg, _ = wrap(x + 24, 394, d, 304, 15, 400, INK2)
    c.add(svg)
sv, _ = keys(48, 510, ["[ENTER]", "+", "0000", "+", "[397]", "+", ("código nuevo",)], 17)
c.add(sv)
c.add(Note(612, 504, 540, "Anotá los códigos en la ficha del sistema de gestión, nunca en el gabinete (paso 5).", kind="ok"))
save(c, "5-paso2.svg")
