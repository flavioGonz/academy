from _akx2941 import *

K = "Akuvox"

# ---------------------------------------------------------------- figura principal
c = Canvas(K, "Una controladora en el tablero, cuatro puertas")
c.add(Zone(40, 150, 430, 470, "tablero", INK3))
ctl = c.add(Generic(75, 300, "A094 o A095", "controladora 4 puertas", icon="server", w=360, dark=True))
c.add(Chip(75, 440, "relé 30 V 2 A en las dos", "gray", mono=False))
c.add(Chip(75, 488, "A094: 220 V · sin PoE", "warn", mono=False))
c.add(Chip(75, 536, "A095: PoE+ o 12 V 5 A", "gray", mono=False))
for i in range(4):
    y = 140 + i * 125
    d = c.add(Generic(600, y, f"Puerta {i + 1}", "lector + cerradura", icon="door", w=290))
    c.add(Cable(ctl.right(-24 + i * 16), d.left(), kind="relay"))
c.add(Note(920, 150, 240, "A095 sí. A094 no se integra.", title="Ascensor EC33", kind="info"))
c.add(Note(920, 360, 240, "Cada salida de 12 V tiene su propio límite (paso 2).", title="Energía", kind="warn"))
c.save(out("35.svg"))

# ---------------------------------------------------------------- paso 2
c = Canvas(K + " · Paso 2", "¿Cuánta corriente da cada salida de 12 V?")
x0, lw, wm, vmax = 60, 380, 560, 800
rows = [
    ("A094 · 4 salidas", 800, "800 mA", BLUE),
    ("A095 con fuente 12 V 5 A", 500, "500 mA", BLUE),
    ("A095 PoE+ · 4 lectores o menos", None, "0,2 a 0,4 A", CYAN),
    ("A095 PoE+ · 8 lectores", 200, "0,2 A", WARN),
]
for i, (lbl, v, vt, col) in enumerate(rows):
    y = 160 + i * 74
    if v is None:
        c.add(text(x0, y + 23, lbl, 16, 600, INK, FB))
        c.add(f'<rect x="{x0 + lw}" y="{y}" width="{wm}" height="34" rx="8" fill="{SOFT}"/>')
        c.add(f'<rect x="{x0 + lw}" y="{y}" width="{wm * 400 / vmax:.1f}" height="34" rx="8" fill="{CYAN}" opacity=".35"/>')
        c.add(f'<rect x="{x0 + lw}" y="{y}" width="{wm * 200 / vmax:.1f}" height="34" rx="8" fill="{CYAN}"/>')
        c.add(text(x0 + lw + wm * 400 / vmax + 12, y + 23, vt, 16, 600, INK, FM))
    else:
        c.add(hbar(x0, y, wm, v, vmax, lbl, vt, col, lw=lw))
c.add(Label(x0 + lw, 470, "corriente máxima por salida de 12 V", 15, 500, INK3, FM))
c.add(Note(60, 500, 540, "Por puerta: consumo del lector + consumo de la cerradura. Si pasa el valor de su salida, la cerradura va con fuente propia (paso 3).", title="Cómo se usa", kind="info"))
c.add(Note(640, 500, 500, "A094: su entrada de 100 a 240 VAC 1,5 A alimenta las 4 salidas a la vez.", title="Ojo", kind="warn"))
c.save(out("35-paso2.svg"))

# ---------------------------------------------------------------- paso 3
c = Canvas(K + " · Paso 3", "Si la puerta no entra, la cerradura va aparte")
c.add(Label(60, 160, "El lector sigue en la salida de 12 V de la controladora", 18, 600, INK))
y1 = 240
c.add(Chip(60, y1 + 6, "salida 12 V", "blue"))
c.add(Wire([(200, y1), (560, y1)], kind="power+"))
c.add(Generic(560, y1 - 42, "Lector", "puerta 1", icon="card", w=260))
c.add(Label(60, 360, "La cerradura toma energía de su propia fuente", 18, 600, INK))
y2 = 470
c.add(Chip(60, y2 + 6, "+ fuente propia", "alert"))
c.add(Wire([(232, y2), (330, y2)], kind="power+"))
c.add(contact(330, y2, "relé puerta 1", sub="controladora", closed=False, w=180))
c.add(Wire([(510, y2), (600, y2)], kind="relay"))
c.add(Lock(600, y2 - 42, "Cerradura", "puerta 1", w=230))
c.add(Wire([(830, y2), (930, y2)], kind="power-"))
c.add(Chip(940, y2 + 6, "− fuente propia", "dark"))
c.add(Step(520, 354, 3))
c.add(Note(60, 560, 1080, "El relé de la controladora solo abre y cierra el circuito: la corriente de la cerradura sale de su fuente.", kind="ok"))
c.save(out("35-paso3.svg"))
