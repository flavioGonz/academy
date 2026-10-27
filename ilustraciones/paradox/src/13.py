import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/paradox/src")
from _pdx import *

# ---------------------------------------------------------------- 13.svg: TBL, grupos de fallas
c = Canvas(K(), "TBL: cada número encendido es un grupo de fallas")
c.add(NOLIG)
c.add(keypad(48, 140, "Teclado", "TBL encendida", lcd=True, hl_keys=("2", "3", "8"), screen=["TBL", "2  3  8"]))
groups = [("1", "batería baja de inalámbricos", None), ("2", "energía", "2.1 batería · 2.2 AC · 2.3 sobrecarga AUX"), ("3", "campana", None),
          ("4", "comunicación", None), ("5", "tamper y cableado de zona", None), ("6", "tamper de módulo", None),
          ("7", "lazo de fuego", None), ("8", "pérdida de reloj", None), ("9", "supervisión de inalámbricos", None),
          ("10", "supervisión de módulos del bus", "se limpia en [955]")]
for i, (n, t, s) in enumerate(groups):
    col, row = divmod(i, 5)
    x, y = 280 + col * 440, 132 + row * 92
    lit = n in ("2", "3", "8")
    c.add(rect(x, y, 420, 80, SOFT if lit else WHITE, CYAN if lit else LINE2, rx=12, sw=2.5 if lit else 1.5))
    c.add(badge(x + 34, y + 40, n, CYAN if lit else INK3, 20, 17))
    c.add(text(x + 66, y + (36 if s else 46), t, 17, 600, INK, FB))
    if s:
        c.add(text(x + 66, y + 60, s, 14, 500, INK3, FM))
c.add(text(48, 640, "Cada número abre su submenú: tocalo para ver el detalle. En un K32LCD+ la falla aparece en texto.", 16, 500, INK2, FB))
save(c, "13.svg")

# ---------------------------------------------------------------- 13-paso2: [955] y el reset
c = Canvas(K(2), "La falla de un módulo quitado no se va con un reset")
c.add(NOLIG)
c.add(Step(48, 140, 2))
cols = [("Sacás el ZX8 del bus", "TBL 10 · supervisión de módulo", "warn"), ("Reset", "la falla sigue ahí", "alert"), ("[955]", "falla de módulos del bus borrada", "ok")]
for i, (t, s, kd) in enumerate(cols):
    x = 80 + i * 360
    c.add(panel(x, 140, 320, 150, t, kd))
    svg, _ = wrap(x + 20, 214, s, 280, 17, 600, INK)
    c.add(svg)
    if i < 2:
        c.add(Arrow((x + 324, 215), (x + 356, 215)))
sv, _ = keys(80, 330, ["[ENTER]", "+", "0000", "+", "[955]"], 18, hl=(4,))
c.add(sv)
c.add(text(470, 356, "solo si el módulo sale para siempre", 16, 600, INK2, FB))
c.add(Note(48, 420, 540, "La falla de AC se ve en TBL apenas se corta la red, pero se reporta a monitoreo recién después del retardo de [839]: 15 min de fábrica.", title="AC: se ve ya, se reporta después", kind="info"))
c.add(Note(612, 420, 540, "Pérdida de reloj (grupo 8): cargá fecha y hora desde el menú rápido o desde BabyWare (paso 1).", title="Reloj", kind="ok"))
save(c, "13-paso2.svg")

# ---------------------------------------------------------------- 13-paso3: LED de estado de la placa
c = Canvas(K(3), "El LED de estado de la placa también habla")
c.add(NOLIG)
c.add(Step(48, 140, 3))
c.add(text(380, 150, "cada cuadrito = un cuarto de segundo (4 s en total)", 15, 500, INK3, FB))
pats = [("Un destello por segundo", "normal", [1, 0, 0, 0] * 4, OK),
        ("Un segundo sí, uno no", "hay alguna falla: mirá TBL", [1, 1, 1, 1, 0, 0, 0, 0] * 2, WARN),
        ("Encendido fijo", "la central está usando la línea telefónica", [1] * 16, BLUE),
        ("Rápido, 6 s al energizar", "bloqueo de instalador activo", [1, 0] * 8, CYAN)]
for i, (t, s, p, col) in enumerate(pats):
    y = 180 + i * 96
    c.add(rect(48, y - 16, 1104, 82, WHITE, LINE2, rx=14))
    c.add(ledrow(72, y + 6, p, t, s, col, cell=24))
c.add(text(48, 580, "Según la guía SP+. Anotá en cada prueba del laboratorio cuándo pasa del primer patrón al segundo.", 16, 500, INK2, FB))
save(c, "13-paso3.svg")
