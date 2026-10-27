import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/paradox/src")
from _pdx import *

# ---------------------------------------------------------------- 2.svg: bus de 4 hilos, de a grupos
c = Canvas(K(), "El bus: cuatro hilos que alimentan y comunican")
b = Box(48, 210, 260, 120, "Central", "SP+ o MG", dark=True, icon=ICON["shield"])
c.add(b)
devs = [("Teclado", "K32LCD+", "Grupo 1"), ("Expansor", "ZX8", "Grupo 2"), ("Teclado", "K35", "Grupo 3")]
for i, (t, s, g) in enumerate(devs):
    y = 128 + i * 106
    d = c.add(Box(470, y, 240, 84, t, s, icon=ICON["card"] if i != 1 else ICON["server"]))
    c.add(Cable(b.right(), d.left(), kind="data"))
    c.add(tag(780, y + 50, g, "info" if i == 0 else "gray", 15))
    c.add(text(848, y + 50, "→ TBL", 15, 600, INK2, FM))
c.add(pill(384, 262, "bus 4 hilos", BLUE, WHITE, 14))
c.add(panel(940, 124, 212, 300, "Límites", "info"))
c.add(lines(960, 192, [("SP+", INK), "hasta 15 módulos", "76 m por módulo", "230 m en total", "", ("EVOHD+", INK), "hasta 254 módulos", "914 m en total"], 16, 24))
c.add(Note(48, 470, 540, "Rojo (+) y negro (−) llevan la alimentación del auxiliar; los otros dos hilos, los datos. Cada módulo suma consumo al AUX.", title="Alimenta y comunica", kind="info"))
c.add(Note(612, 470, 540, "Sin energía, se suma un grupo chico; se energiza y se mira TBL. Una falla nueva es del grupo que acabás de sumar.", title="De a grupos", kind="ok"))
c.add(text(48, 640, "Cifras de las guías SP+ y EVOHD+. En EVO, la sección [4000] lista los módulos que la central ve.", 15, 500, INK3, FB))
save(c, "2.svg")

# ---------------------------------------------------------------- 2-paso2: teclado a los cuatro bornes
c = Canvas(K(2), "Cada hilo del bus, al borne del mismo nombre")
c.add(NOLIG)
labs = ["+", "−", "datos", "datos"]
sv, a1 = strip(120, 130, labs, pitch=96, title="CENTRAL · BORNES DEL BUS", hl={"+": RED, "−": BLACK})
c.add(sv)
sv, a2 = strip(560, 430, labs, pitch=96, hl={"+": RED, "−": BLACK}, above=False)
c.add(sv)
c.add(text(560, 544, "TECLADO · BORNES DEL BUS", 15, 600, INK2, FM, ls=1))
kinds = ["power+", "power-", "data", "relay"]
for i in range(4):
    (x1, y1), (x2, y2) = a1[i], a2[i]
    ym = 300 + i * 22
    c.add(wire([(x1, y1), (x1, ym), (x2, ym), (x2, y2)], kinds[i]))
c.add(Step(104, 220, 2))
c.add(Note(48, 400, 470, "Rojo es + y negro es −: es la alimentación que sale del auxiliar. Los dos hilos de datos van borne a borne con el mismo nombre que dice la serigrafía.", title="Respetá la serigrafía", kind="info"))
c.add(Note(48, 556, 470, "Los nombres de los bornes de datos cambian según el modelo: el dibujo es genérico. Conectás sin energía y recién después energizás.", kind="warn", size=15))
c.add(text(890, 160, "Red 16,5 Vac y", 16, 600, INK2, FB))
c.add(text(890, 184, "batería: afuera", 16, 600, ALERT, FB))
c.add(text(890, 208, "mientras cableás", 16, 600, INK2, FB))
save(c, "2-paso2.svg")

# ---------------------------------------------------------------- 2-paso4: sumar el ZX8 y mirar TBL
c = Canvas(K(4), "Sumá un módulo y mirá qué falla aparece")
seq = [("1", "Desenergizá", "red y batería afuera"), ("2", "Sumá el ZX8", "al bus, borne a borne"), ("3", "Energizá", "red y batería"), ("4", "TBL", "¿hay una falla nueva?")]
for i, (n, t, s) in enumerate(seq):
    x = 48 + i * 282
    c.add(panel(x, 128, 258, 112, None, "info"))
    c.add(badge(x + 34, 166, n, CYAN))
    c.add(text(x + 62, 172, t, 20, 600, INK, FD))
    c.add(text(x + 24, 214, s, 16, 400, INK2, FB))
    if i < 3:
        c.add(Arrow((x + 262, 184), (x + 280, 184)))
c.add(Step(48, 128, 4))
c.add(panel(48, 272, 540, 230, "Lo esperable en una central nueva", "ok"))
c.add(tag(110, 344, "8", "ok", 18)); c.add(text(150, 344, "pérdida de reloj", 18, 600, INK, FB))
c.add(tag(110, 400, "3", "ok", 18)); c.add(text(150, 400, "campana, si no hay sirena", 18, 600, INK, FB))
c.add(text(72, 460, "Se resuelven con fecha y hora, y con sirena o 1 kΩ en BELL.", 16, 400, INK2, FB))
c.add(panel(612, 272, 540, 230, "Cualquier otra falla nueva", "warn"))
svg, _ = wrap(636, 336, "Es del ZX8 o de su cableado: lo que acabás de sumar. Revisá esos cuatro hilos antes de seguir con el próximo grupo.", 490, 18, 500, INK)
c.add(svg)
c.add(Note(48, 528, 1104, "En obra con el sistema en servicio, avisá a monitoreo antes de desenergizar: la central puede reportar falla de AC o tamper.", kind="alert", size=16))
save(c, "2-paso4.svg")

# ---------------------------------------------------------------- 2-paso5: zona de teclado
c = Canvas(K(5), "La entrada de zona del teclado, como zona 05")
c.add(NOLIG)
c.add(keypad(60, 130, "Teclado", "K32+ o K32LCD+", lcd=True))
sv, an = strip(290, 150, ["zona", "−"], pitch=96, title="ENTRADA DE ZONA DEL TECLADO")
c.add(sv)
c.add(rect(560, 140, 200, 120, WHITE, LINE2, rx=14))
c.add(text(580, 170, "Contacto", 17, 600, INK))
c.add(contact(600, 220, True, None, 90))
zx, zy = an["zona"]; mx, my = an["−"]
c.add(wire([(zx, zy), (zx, 320), (600, 320), (600, 220)], "data"))
c.add(wire([(mx, my), (mx, 296), (684, 296), (684, 220)], "data"))
c.add(text(290, 360, "Dibujo genérico: mirá los bornes en la guía de tu teclado.", 15, 400, INK3, FB))
c.add(Step(274, 200, 5))
sv, _ = keys(48, 462, ["[ENTER]", "+", "0000", "+", ("mantener 3 s la tecla de acción",), "+", "05", "+", "[ENTER]"], 17)
c.add(sv)
c.add(text(48, 530, "05 = número de zona, dos dígitos. ENTER guarda y sale.", 16, 500, INK2, FB))
c.add(Note(800, 128, 352, "Si después aprendés un inalámbrico en la zona 05, pisa a la de teclado. Y una de teclado pisa a una cableada con el mismo número.", title="El mismo número se pisa", kind="warn"))
c.add(Note(48, 560, 1104, "En EVO la zona de teclado admite un solo detector, aun con ATZ, no reconoce tamper y sigue la definición de EOL de la central.", kind="info", size=16))
save(c, "2-paso5.svg")
