import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/paradox/src")
from _pdx import *

# ---------------------------------------------------------------- 7.svg: dos casas en una central
c = Canvas(K(), "Dos particiones: la casa y el taller, cada una con lo suyo")
c.add(NOLIG)
c.add(Zone(48, 140, 520, 236, "PARTICIÓN 1 · CASA", BLUE))
c.add(Zone(632, 140, 520, 236, "PARTICIÓN 2 · TALLER", OK))
for i, (z, t) in enumerate([("01 1", "zona 1 · puerta principal"), ("05 1", "zona 2 · PIR del living"), ("08 1", "zona 3 · ventanas"), ("16 1", "zona 4 · medidores")]):
    y = 176 + i * 50
    c.add(code(72, y, 100, z, 15, h=36))
    c.add(text(188, y + 24, t, 16, 500, INK2, FB))
for i, (z, t) in enumerate([("01 2", "zona 5 · puerta del taller"), ("08 2", "zona 6 · ventana del taller")]):
    y = 176 + i * 50
    c.add(code(656, y, 100, z, 15, h=36))
    c.add(text(772, y + 24, t, 16, 500, INK2, FB))
c.add(text(656, 312, "El tercer dígito de cada zona dice", 16, 600, INK, FB))
c.add(text(656, 336, "la partición: 1, 2, o 3 para ambas.", 16, 600, INK, FB))
c.add(Box(430, 404, 340, 84, "Maestro del sistema", "particiones 1 y 2", icon=ICON["user"]))
c.add(Box(812, 520, 340, 84, "Usuario 005 · taller", "solo partición 2", icon=ICON["user"]))
c.add(Arrow((470, 404), (330, 378), kind="ok"))
c.add(Arrow((730, 404), (870, 378), kind="ok"))
c.add(Arrow((1010, 520), (1010, 378), kind="ok"))
c.add(Note(48, 520, 720, "[700] opción 1. Si después se apaga, todo pasa a partición 1 y las zonas asignadas a la 2 dejan de funcionar.", title="El particionado se prende una vez", kind="warn"))
save(c, "7.svg")

# ---------------------------------------------------------------- 7-paso3: opciones del usuario 005
c = Canvas(K(3), "Usuario 005: SLEEP borra todo, [2] deja solo el taller")
c.add(NOLIG)
labs = ["part. 1", "part. 2", "anular", "Stay", "forzado", "solo arm.", "solo PGM", "coacción"]
rows = [("De fábrica", {1, 3, 4, 5}, None), ("Después de SLEEP", set(), None), ("Después de [2]", {2}, None)]
c.add(code(48, 124, 540, "[CLEAR] [405]  [SLEEP]  [2]  [ENTER]", 16, h=42))
c.add(Step(48, 124, 3))
for i, (t, on, _) in enumerate(rows):
    y = 200 + i * 116
    c.add(text(48, y + 30, t, 18, 600, INK, FB))
    c.add(opts(270, y, on, size=50, gap=18, labels=labs))
    if i < 2:
        c.add(Arrow((900, y + 40), (900, y + 100)))
        c.add(text(920, y + 78, "tecla SLEEP" if i == 0 else "tecla 2", 16, 600, BLUE, FM))
c.add(rect(48, 548, 1104, 70, OK_BG, OK, rx=14))
c.add(text(72, 590, "Arma y desarma el taller; no la casa. Sin anular, sin Stay, sin forzado.", 18, 600, OK, FB))
c.add(Note(852, 120, 300, "[404] a [432]: una sección por usuario. La 405 es la del usuario 005.", kind="info", size=15))
save(c, "7-paso3.svg")

# ---------------------------------------------------------------- 7-paso6: 4 o 6 dígitos
c = Canvas(K(6), "El largo del código se decide antes de cargar usuarios")
c.add(NOLIG)
c.add(Step(48, 140, 6))
c.add(text(80, 148, "[701] opción 1: códigos de 4 o de 6 dígitos", 19, 600, INK, FB))
def digits(x, y, ds, hl=()):
    for i, d in enumerate(ds):
        col = WARN if i in hl else BLUE
        c.add(rect(x + i * 62, y, 52, 70, WARN_BG if i in hl else SOFT, col, rx=10))
        c.add(mid(x + i * 62 + 26, y + 47, d, 30, 700, col, FM))
c.add(text(80, 232, "Antes · 4 dígitos", 16, 600, INK3, FB))
digits(80, 250, "1234")
c.add(Arrow((350, 285), (470, 285)))
c.add(text(380, 272, "pasás a 6", 15, 600, INK2, FB))
c.add(text(500, 232, "Después · 6 dígitos", 16, 600, INK3, FB))
digits(500, 250, "123412", hl=(4, 5))
c.add(text(752, 352, "la central repite los dos primeros", 16, 600, WARN, FB, anchor="middle"))
c.add(Note(48, 400, 540, "El usuario sigue tecleando 1234 y no anda: su código ahora es 123412. Si el cambio es inevitable, avisale a cada usuario su código nuevo.", title="El llamado del lunes", kind="warn"))
c.add(Note(612, 400, 540, "Con la central en servicio, cambiar el largo o el particionado afecta a todos: coordinalo con el cliente y con monitoreo.", title="En obra", kind="alert"))
save(c, "7-paso6.svg")
