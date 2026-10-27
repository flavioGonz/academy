from _akx2941 import *

K = "Akuvox"

# ---------------------------------------------------------------- figura principal
c = Canvas(K, "Contá los relés y leé la carga antes de prometer")
mons = [
    ("C313", "7\" · Linux", ["1 relé", ("30 V 2 A", "gray")]),
    ("C316", "7\" · Android", ["1 relé", ("carga sin dato", "warn")]),
    ("C319", "10\" · Android", ["2 relés", ("24 V 1 A", "warn")]),
    ("IT88", "10\" · aluminio", ["2 relés", ("30 V 2 A", "gray")]),
]
for i, (name, sub, chips) in enumerate(mons):
    x = 60 + i * 280
    c.add(Monitor(x, 140, name, sub))
    c.add(Chip(x + 120, 412, chips[0], "blue", mono=False, anchor="middle"))
    s, k = chips[1]
    c.add(Chip(x + 120, 456, s, k, mono=True, anchor="middle"))
c.add(Note(60, 510, 1080, "La tabla de carga trae un solo valor por modelo. En el C319 y el IT88 aplicalo a cada uno de los dos relés, y si uno maneja algo crítico, confirmalo con el distribuidor. Del C316 no hay dato: no le cuelgues una carga sin confirmar.", title="Un valor por modelo", kind="info"))
c.save(out("31.svg"))

# ---------------------------------------------------------------- paso 3
c = Canvas(K + " · Paso 3", "Probá los dos relés del C319, cada uno con su lámpara")
for i, (lbl, y) in enumerate([("relé 1", 230), ("relé 2", 410)]):
    c.add(Chip(60, y + 6, "+12 V fuente", "alert", mono=True))
    c.add(Wire([(214, y), (330, y)], kind="power+"))
    c.add(contact(330, y, lbl, closed=(i == 0)))
    c.add(Wire([(480, y), (640, y)], kind="relay"))
    lp = Lamp(670, y, "Lámpara 12 V", None, on=(i == 0))
    c.add(lp)
    c.add(Wire([(700, y), (820, y)], kind="power-"))
    c.add(Chip(830, y + 6, "− fuente", "dark", mono=True))
c.add(Step(405, 150, 3))
c.add(Label(950, 236, "cerrado: prende", 16, 600, OK))
c.add(Label(950, 416, "abierto: apagada", 16, 600, INK3))
c.add(chips_row(60, 560, [("C319: máx. 24 V 1 A por relé", "warn"), ("IT88: máx. 30 V 2 A (tabla)", "gray"), ("C316: sin dato, confirmar", "warn")], mono=False))
c.add(Label(60, 620, "Activá cada relé por separado: tiene que prender solo su lámpara.", 17, 500, INK2))
c.save(out("31-paso3.svg"))

# ---------------------------------------------------------------- paso 4
c = Canvas(K + " · Paso 4", "¿Tu firmware llega al mínimo para RS485?")
def blocks(y, vals, title, hl=None, kind="gray"):
    o = [text(60, y + 6, title, 17, 600, INK)]
    for j, v in enumerate(vals):
        x = 300 + j * 150
        col = CYAN if hl and j in hl else LINE2
        o.append(f'<rect x="{x}" y="{y - 30}" width="120" height="56" rx="12" fill="{WHITE}" stroke="{col}" stroke-width="{3 if hl and j in hl else 2}"/>')
        o.append(text(x + 60, y + 7, v, 22, 600, INK, FM, anchor="middle"))
        if j < 3:
            o.append(text(x + 135, y + 10, ".", 26, 700, INK3, FM, anchor="middle"))
    return "".join(o)
c.add(blocks(190, ["119", "30", "12", "902"], "Mínimo del C319"))
c.add(blocks(290, ["119", "30", "C", "D"], "Lo que leés en Status", hl={2, 3}))
for j, s in enumerate(["A · modelo", "B · OEM", "C · rama", "D · número"]):
    c.add(Label(360 + j * 150, 352, s, 15, 500, INK3, FM, "middle"))
c.add(Note(60, 400, 520, "Mismo A (modelo) y mismo B. Si C es igual, D tiene que ser igual o mayor que el mínimo. Si C es otro, preguntá antes de cablear.", title="Cómo comparar", kind="info"))
c.add(Table(640, 400, ["Modelo", "Mínimo RS485"], [["C316", "316.30.13.102"], ["C319", "119.30.12.902"], ["IT88", "88.30.12.904"]], [150, 300], row_h=44, mono_cols=(1,)))
c.save(out("31-paso4.svg"))
