import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/paradox/src")
from _pdx import *

# ---------------------------------------------------------------- 1.svg: cuatro familias, cuatro formas de entrar
c = Canvas(K(), "¿Qué central tenés adelante? Así se entra")
c.add(NOLIG)
fams = [
    ("SP / SP+", "Spectra", "SP5500+ · SP6000+ · SP7000+", ["[ENTER]", "+", "0000"], "3 dígitos", "0000"),
    ("MG / MG+", "Magellan", "MG5050", ["[ENTER]", "+", "0000"], "3 dígitos", "0000"),
    ("EVO / EVOHD+", "Digiplex EVO", "EVO192 · EVOHD+", [("mantener",), "[0]", "+", "000000"], "4 dígitos", "000000"),
    ("M25", "Línea M", "M25 · M25 LTE", None, "no aplica", "no aplica"),
]
for i, (t, s, m, seq, sec, fab) in enumerate(fams):
    x = 48 + i * 280
    kd = "dark" if i == 3 else "info"
    c.add(panel(x, 124, 264, 330, None, "info"))
    c.add(text(x + 20, 162, t, 22, 600, INK, FD))
    c.add(text(x + 20, 188, s, 15, 500, INK3, FB))
    c.add(text(x + 20, 214, m, 14, 500, BLUE, FM))
    c.add(hline(x + 16, x + 248, 232))
    c.add(text(x + 20, 262, "ENTRAR", 13, 600, INK3, FM, ls=1.5))
    if seq:
        sv, _ = keys(x + 20, 276, seq, 15, gap=6)
        c.add(sv)
    else:
        c.add(text(x + 20, 296, "App BlueEye o", 16, 600, INK, FB))
        c.add(text(x + 20, 318, "software web", 16, 600, INK, FB))
    c.add(text(x + 20, 360, "SECCIONES", 13, 600, INK3, FM, ls=1.5))
    c.add(text(x + 20, 384, sec, 17, 600, INK, FB))
    c.add(text(x + 20, 418, "INSTALADOR DE FÁBRICA", 13, 600, INK3, FM, ls=1.5))
    c.add(text(x + 20, 442, fab, 17, 600, ALERT if fab[0] == "0" else INK3, FM))
c.add(Note(48, 478, 540, "Spectra SP y Magellan MG usan el mismo mapa de secciones: un instructivo sirve para las dos.", title="SP y MG, mismo mapa", kind="info"))
c.add(Note(612, 478, 540, "Si el código no es el de fábrica, no pruebes al azar: los teclados se pueden bloquear y avisar a monitoreo.", title="Código desconocido", kind="warn"))
save(c, "1.svg")

# ---------------------------------------------------------------- 1-paso3: versión en la 980
c = Canvas(K(3), "Leé la versión de la central en la sección [980]")
c.add(NOLIG)
c.add(Step(48, 140, 3))
c.add(text(80, 146, "SP o MG, desarmada y con StayD apagado", 17, 600, INK2, FB))
sv, xe = keys(80, 170, ["[ENTER]", "+", "0000", ("código de instalador",), "+", "[980]"], 18, hl=(5,))
c.add(sv)
y0 = 270
c.add(text(48, y0, "La central muestra la versión de a un dígito:", 18, 600, INK, FB))
steps = [("1.er dígito", "2 pitidos"), ("2.º dígito", "2 pitidos"), ("3.er dígito", "2 pitidos"), ("…", "")]
x = 48
for i, (d, b) in enumerate(steps):
    c.add(rect(x, y0 + 24, 170, 92, SOFT if d != "…" else WHITE, CYAN if d != "…" else LINE2, rx=14))
    c.add(mid(x + 85, y0 + 64, d, 18, 600, INK, FB))
    if b:
        c.add(mid(x + 85, y0 + 92, b, 15, 500, INK3, FM))
    if i < 3:
        s, _ = keycap(x + 182, y0 + 52, "ENTER", 14)
        c.add(s)
    x += 270
c.add(rect(48, y0 + 150, 520, 80, OK_BG, OK, rx=14))
c.add(text(72, y0 + 184, "Tres pitidos: terminó la versión", 18, 600, OK, FB))
c.add(text(72, y0 + 210, "Anotala completa en la ficha.", 16, 400, INK2, FB))
s, _ = keycap(612, y0 + 168, "CLEAR", 16)
c.add(s)
c.add(text(700, y0 + 194, "sale de programación", 17, 500, INK2, FB))
c.add(Note(48, 540, 1104, "En EVO la entrada es otra (mantener 0 y secciones de cuatro dígitos): buscá la sección de versión en su propia guía.", kind="info"))
save(c, "1-paso3.svg")

# ---------------------------------------------------------------- 1-paso4: ficha de la obra
c = Canvas(K(4), "La ficha de la obra, antes de tocar una sección")
c.add(rect(48, 124, 640, 420, WHITE, LINE2, rx=18))
c.add(text(72, 160, "FICHA DE LA OBRA", 14, 600, INK3, FM, ls=2))
rows = [("Modelo (placa)", "SP6000+"), ("Versión ([980])", "_ _ _ _"), ("Teclados", "K32LCD+ × 1"),
        ("Comunicación", "IP150 · IP180 · PCS"), ("StayD", "sí / no")]
for i, (k, v) in enumerate(rows):
    y = 200 + i * 62
    c.add(text(72, y + 22, k, 18, 600, INK, FB))
    c.add(rect(330, y, 330, 38, GROUND, LINE2, rx=8))
    c.add(text(346, y + 25, v, 16, 500, INK2, FM))
c.add(text(72, 524, "Valores de ejemplo: completá con lo que ves en la obra.", 15, 400, INK3, FB))
c.add(Step(48, 124, 4))
c.add(panel(720, 124, 432, 200, None, "alert"))
c.add(badge(756, 166, "5", ALERT))
c.add(text(788, 172, "¿SP4000 o SP65?", 20, 600, ALERT, FD))
svg, _ = wrap(744, 212, "Marcala en rojo en la ficha. Su reseteo es distinto al del resto de SP y MG: se ve en la lección de llaves de la central.", 384, 16, 400, INK2)
c.add(svg)
c.add(Note(720, 352, 432, "El modelo y la versión de [980] te dicen qué manual abrir. Con StayD activo no se entra a programación, y los módulos definen cómo reporta.", title="Por qué anotar todo esto", kind="info"))
save(c, "1-paso4.svg")
