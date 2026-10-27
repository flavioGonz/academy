import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/bosch-incendio/src")
from _bi import *

# ---------------------------------------------------------------- 14.svg: antes, durante, después
c = Canvas(K(), "Avisá y aislá antes; rehabilitá todo después")
ph = [("Antes", BLUE, ["Monitoreo avisado: empresa, hora, operador", "Responsable y ocupantes avisados", "Salidas deshabilitadas en el panel", "Extinción bloqueada por su empresa", "Zona en modo revisión"]),
      ("Durante", WARN, ["Se prueba lo planificado", "Nada que mueva algo puede activarse", "Cada prueba con hora y resultado"]),
      ("Después", OK, ["Zona fuera de modo revisión", "Todas las salidas rehabilitadas", "Panel en reposo, sin deshabilitados", "Monitoreo avisado del fin"])]
for i, (t, col, ls) in enumerate(ph):
    x = 48 + i * 376
    c.add(rect(x, 130, 352, 360, WHITE, col, rx=16, sw=2.5))
    c.add(rect(x, 130, 352, 54, col, col, rx=16, sw=0)); c.add(rect(x, 164, 352, 20, col, col, rx=0, sw=0))
    c.add(text(x + 22, 166, t, 21, 600, WHITE, FD))
    for j, s in enumerate(ls):
        c.add(rect(x + 22, 210 + j * 52, 22, 22, WHITE, col, rx=5, sw=2))
        c.add(wrap(x + 56, 227 + j * 52, s, 280, 15)[0])
    if i < 2:
        c.add(arrow((x + 354, 310), (x + 374, 310)))
c.add(rect(48, 516, 1104, 104, WARN_BG, WARN, rx=14, sw=2))
c.add(f'<circle cx="96" cy="568" r="14" fill="{WARN}"/>')
c.add(text(130, 558, "LED amarillo fijo en el panel: hay algo deshabilitado", 18, 600, WARN, FD))
c.add(text(130, 588, "Antes de irte, ese LED tiene que estar apagado: si no, el edificio quedó sin una función de seguridad.", 16, 400, INK2))
save(c, "14.svg")

# ---------------------------------------------------------------- 14-paso1: cómo se aísla cada salida
c = Canvas(K(1), "Cada salida real, con su forma de aislarla")
c.add(Table(48, 136, ["Salida", "Cómo se aísla", "Quién"], [
    ["Transmisión al monitoreo", "deshabilitar en el panel y avisar", "vos, con el operador"],
    ["Sirenas (si corresponde)", "deshabilitar en el panel", "vos"],
    ["Retención de puertas", "deshabilitar la salida", "vos"],
    ["Ventilación", "deshabilitar la salida", "vos"],
    ["Ascensores", "deshabilitar la salida", "vos"],
    ["Extinción por gas", "central de extinción bloqueada", "su empresa"]], [330, 440, 334], hl_row=5, row_h=52))
c.add(Note(48, 520, 540, "Con gas, la prueba se coordina con la empresa de extinción y con su central bloqueada: anotá nombre y hora en la hoja.", title="Extinción, siempre aparte", kind="alert"))
c.add(Note(612, 520, 540, "La lista sale de la obra real: si hay una salida que no sabés cómo aislar, eso se resuelve antes de probar.", title="Lista completa", kind="info"))
save(c, "14-paso1.svg")

# ---------------------------------------------------------------- 14-t2: después de un cambio de software (teoría, fija)
c = Canvas("Bosch Incendio · Pruebas", "Después de un cambio: 100 % de lo afectado y 10 % del resto")
for i, (n, prob, lab) in enumerate([(300, 30, "300 iniciadores no afectados"), (800, 50, "800 iniciadores no afectados")]):
    y = 160 + i * 190
    c.add(text(48, y - 10, lab, 18, 600, INK, FD))
    W = 600 * n / 800
    c.add(rect(48, y + 10, W, 50, SOFT, LINE2, rx=8, sw=1.5))
    c.add(rect(48, y + 10, W * prob / n, 50, BLUE, BLUE, rx=8, sw=0))
    c.add(text(48 + W + 20, y + 44, f"probás {prob}", 20, 700, BLUE, FM))
    c.add(text(48, y + 92, "10 % = 30" if n == 300 else "10 % = 80, pero el tope es 50", 16, 500, INK2))
c.add(rect(900, 150, 252, 300, OK_BG, OK, rx=16, sw=2))
c.add(text(920, 188, "Lo afectado", 19, 600, OK, FD))
c.add(text(920, 240, "100 %", 40, 700, OK, FM))
c.add(wrap(920, 290, "Todo lo que tocó el cambio de software se prueba completo.", 212, 16)[0])
c.add(Note(48, 540, 1104, "Regla de la guía de Minnesota basada en NFPA 72. Si el proyecto o la autoridad piden más, manda lo que pidan.", title="De dónde sale", kind="info"))
save(c, "14-t2.svg")
