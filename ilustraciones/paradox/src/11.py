import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/paradox/src")
from _pdx import *

# ---------------------------------------------------------------- 11.svg: del evento al operador
c = Canvas(K(), "Del evento al operador, con nombre y apellido")
c.add(NOLIG)
ce = c.add(Box(48, 170, 250, 110, "Central", "abonado 1A01", dark=True, icon=ICON["shield"]))
md = c.add(Box(350, 170, 230, 110, "Módulo IP", "IP150+ o IP180", icon=ICON["server"]))
rc = c.add(Box(640, 170, 250, 110, "Receptora", "IPR512 o IPC10", icon=ICON["server"]))
op = c.add(Box(942, 170, 210, 110, "Monitoreo", "operador", icon=ICON["user"]))
c.add(Cable(ce.right(), md.left(), kind="data", label="serie"))
c.add(Arrow(md.right(), rc.left(), label="Contact ID", kind="flow"))
c.add(Arrow(rc.right(), op.left(), kind="flow"))
c.add(text(48, 330, "Qué viaja en cada evento", 18, 600, INK, FD))
for i, (k, v, col) in enumerate([("abonado", "1A01", BLUE), ("evento", "alarma de robo", ALERT), ("partición", "1", OK), ("zona", "003", CYAN)]):
    x = 48 + i * 200
    c.add(rect(x, 348, 184, 74, WHITE, LINE2, rx=12))
    c.add(text(x + 16, 376, k, 15, 600, INK3, FB))
    c.add(text(x + 16, 406, v, 18, 700, col, FM))
c.add(panel(860, 330, 292, 110, "Supervisión", "info"))
c.add(text(880, 392, "el módulo se reporta cada", 15, 400, INK2, FB))
c.add(text(880, 416, "tanto: si calla, avisa", 15, 400, INK2, FB))
c.add(Note(48, 462, 540, "Formato en [810]: 4 = Contact ID, 5 = SIA. Por IP o GPRS, SIA no va: IP180 e IP150M reportan solo Contact ID.", title="Contact ID por IP", kind="info"))
c.add(Note(612, 462, 540, "La receptora te da abonado, IP y puerto, contraseña (solo legado) y perfil de supervisión. Pediles los reales.", title="Lo que da la receptora", kind="ok"))
save(c, "11.svg")

# ---------------------------------------------------------------- 11-paso1: el abonado en cada partición y canal
c = Canvas(K(1), "El abonado va en cada partición y en cada canal")
c.add(NOLIG)
c.add(Step(48, 140, 1))
c.add(code(80, 124, 520, "[810] 44   Contact ID en los dos teléfonos", 16, h=42))
c.add(text(380, 222, "Teléfono", 18, 600, INK, FB, anchor="middle"))
c.add(text(760, 222, "IP", 18, 600, INK, FB, anchor="middle"))
grid = [("Partición 1", "[811]", "[918]"), ("Partición 2", "[812]", "[919]")]
for i, (p, a, b) in enumerate(grid):
    y = 244 + i * 110
    c.add(text(60, y + 56, p, 18, 600, INK, FB))
    for j, sec in enumerate((a, b)):
        x = 230 + j * 380
        c.add(rect(x, y, 300, 90, SOFT, CYAN, rx=14))
        c.add(text(x + 20, y + 54, sec, 20, 700, BLUE, FM))
        c.add(text(x + 280, y + 54, "1A01", 22, 700, INK, FM, anchor="end"))
c.add(Note(48, 486, 540, "[812] y [919] se cargan aunque la central no esté particionada. Sin abonado, la central no tiene con qué firmar los eventos de ese canal.", title="Las cuatro, siempre", kind="warn"))
c.add(Note(612, 486, 540, "1A01 es de ejemplo. Un abonado de otra obra hace que el evento llegue al cliente equivocado.", title="Abonado real", kind="alert"))
save(c, "11-paso1.svg")

# ---------------------------------------------------------------- 11-paso2: receptor IP 1
c = Canvas(K(2), "Receptor IP 1: IP de a tres dígitos, perfil y registro")
c.add(NOLIG)
c.add(Step(48, 140, 2))
c.add(code(80, 124, 470, "[929]  203 000 113 010", 20, h=48))
c.add(Arrow((560, 148), (640, 148)))
c.add(text(660, 156, "203.0.113.10", 24, 700, INK, FM))
c.add(text(80, 200, "Cada número de la IP con tres dígitos: 0 se escribe 000 y 10 se escribe 010.", 16, 500, INK2, FB))
rows = [("[930]", "puerto", "el que indique la receptora"), ("[933]", "contraseña", "solo IPR512; el IPC10 no la usa"), ("[934]", "perfil", "supervisión, ej. 02"), ("[935]", "ARM", "registra el módulo y muestra el estado")]
for i, (s_, k, d) in enumerate(rows):
    y = 232 + i * 64
    c.add(rect(48, y, 620, 54, WHITE, LINE2, rx=12))
    c.add(text(68, y + 34, s_, 18, 700, BLUE, FM))
    c.add(text(160, y + 34, k, 17, 600, INK, FB))
    c.add(text(290, y + 34, d, 15, 500, INK2, FB))
c.add(Table(712, 232, ["Perfil IPC10", "Supervisión"], [["01", "1200 s"], ["02", "600 s"], ["03", "300 s"], ["04", "90 s"]], [220, 220], hl_row=1, row_h=46, mono_cols=(0, 1)))
c.add(Note(48, 506, 1104, "Menos segundos = la receptora se entera antes si el módulo se cae, con más tráfico. En el IPR512 los perfiles los define la receptora; en el IPC10 son fijos.", kind="info", size=16))
save(c, "11-paso2.svg")
