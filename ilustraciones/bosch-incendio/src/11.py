import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/bosch-incendio/src")
from _bi import *

LV = {"Alta": 3, "Media": 2, "Baja": 1, "-": 0}


def bars(x, y, lvl, col):
    out = []
    for k in range(3):
        on = k < LV[lvl]
        out.append(rect(x + k * 22, y - 18 + (2 - k) * 0, 16, 20, col if on else WHITE, col if on else LINE2, rx=3, sw=1.5))
    return "".join(out) + text(x + 74, y, lvl, 15, 500, INK2)


# ---------------------------------------------------------------- 11.svg: lugar de instalación = sensibilidad
c = Canvas(K(), "El lugar de instalación decide cómo pesa cada sensor")
c.add(text(48, 140, "FAP-425-DOTC-R · ALGUNOS LUGARES DE LA GUÍA DE OPERACIÓN", 13, 600, INK3, FM, ls=1.5))
rows = [("Oficina (fuera de horario)", "Alta", "Alta", "Alta", False), ("Oficina (fumadores) / sala de espera", "Alta", "Baja", "Baja", True),
        ("Oficina (modo día)", "Baja", "Media", "Alta", False), ("Garaje", "Alta", "Baja", "Baja", False), ("Cocina / restaurante en operación", "Baja", "Baja", "Baja", False)]
x0, y0, rh = 48, 156, 64
c.add(rect(x0, y0, 1104, rh * 6, WHITE, LINE2, rx=12))
for j, h in enumerate(["Térmico máx.", "Óptico", "Químico (CO)"]):
    c.add(text(560 + j * 200, y0 + 38, h, 15, 600, INK2))
for i, (lug, t, o, ch, dflt) in enumerate(rows):
    y = y0 + rh * (i + 1)
    if dflt:
        c.add(rect(x0 + 4, y + 4, 1096, rh - 8, SOFT, CYAN, rx=8, sw=1.5))
    else:
        c.add(hline(x0 + 12, x0 + 1092, y, LINE))
    c.add(text(x0 + 18, y + 38, lug, 16, 600, INK))
    if dflt:
        c.add(tag(470, y + 39, "de fábrica", "cyan", size=13, mono=False))
    for j, (lvl, col) in enumerate([(t, WARN), (o, BLUE), (ch, OK)]):
        c.add(bars(560 + j * 200, y + 42, lvl, col))
c.add(Note(48, 556, 1104, "Con el óptico en sensibilidad baja, el DOTC-R solo dispara si además del humo sube el CO o la temperatura. Por eso rechaza vapor, y por eso espera más.", title="Lo que cambia por dentro", kind="info"))
save(c, "11.svg")

# ---------------------------------------------------------------- 11-paso3: marcar los de fábrica
c = Canvas(K(3), "Marcá los que quedaron de fábrica sin que nadie decida")
c.add(Table(48, 140, ["Dir.", "Modelo", "Lugar (modo)", "¿Elegido?", "Ambiente real"], [
    ["3.1", "FAP-425-OT-R", "Oficina (modo día)", "de fábrica", "cocina de piso"],
    ["3.2", "FAP-425-DOTC-R", "Oficina (fumadores)", "de fábrica", "sala de espera"],
    ["3.3", "FAP-425-O-R", "sensibilidad media", "elegido", "oficina"],
], [90, 220, 260, 170, 364], hl_row=0, row_h=54, mono_cols=(0, 1)))
c.add(rect(1000, 196, 140, 40, ALERT_BG, ALERT, rx=10, sw=2))
c.add(mid(1070, 222, "no coincide", 15, 700, ALERT))
c.add(Note(48, 380, 540, "Que esté de fábrica no es un error en sí: el problema es que nadie lo decidió. Cuando el ambiente real no se parece al lugar programado, va a la lista.", title="Qué buscás", kind="info"))
c.add(Note(612, 380, 540, "Valores de fábrica según la guía: OT y DOT en oficina modo día, DOTC en oficina con fumadores, ópticos en sensibilidad media, térmico en A2R.", title="Cómo reconocerlos", kind="info"))
c.add(text(48, 600, "Filas 3.2 y 3.3 de ejemplo para practicar. Trabajá sobre una copia, nunca sobre la del panel en servicio.", 15, 400, INK3))
save(c, "11-paso3.svg")

# ---------------------------------------------------------------- 11-paso4: qué correspondería
c = Canvas(K(4), "Anotá qué modo correspondería según la guía")
c.add(box(48, 150, 470, 180, "Hoy: Oficina (modo día)", ["FAP-425-OT-R en la cocina del piso", "Térmico: baja (B) · Óptico: media", "el vapor y el humo de cocina", "le llegan al óptico"], kind="alert", size=16))
c.add(arrow((530, 240), (660, 240), kind="ok"))
c.add(box(682, 150, 470, 180, "Propuesta: Cocina en operación", ["Cocina/casino/restaurante en operación", "el OT queda solo con térmico máximo", "(B); el óptico no participa", "se acuerda con el proyecto"], kind="ok", size=16))
c.add(Note(48, 370, 1104, "Cambiar el modo cambia la respuesta al fuego: el OT en modo cocina deja de ver humo. Se acuerda con el proyecto, se deja escrito y se prueba después del cambio.", title="Es una propuesta, no un cambio", kind="warn"))
save(c, "11-paso4.svg")
