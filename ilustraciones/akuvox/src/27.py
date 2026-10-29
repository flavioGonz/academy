import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/akuvox/src")
from _cat import *

# ---------------------------------------------------------------- 27.svg: E18 y E16
c = Canvas("Akuvox", "E18 y E16: rostro en plástico, cerradura aparte")
c.add(portero(60, 150, "pantalla", 0.86, "E18", "estándar o LTE"))
c.add(portero(240, 150, "pantalla", 0.86, "E16", "5\" táctil"))
c.add(text(212, 460, "Linux · IP65 · Wiegand", 15, 400, INK3, FB, anchor="middle"))
g, W, H = grid(452, 126, ["E18", "E16"], [
    ("PIN · rostro", [True, True]),
    ("Tarjeta", ["13,56 y 125 kHz", "solo 13,56 MHz"]),
    ("Bluetooth y QR", [True, True]),
    ("Palma", [None, "E16P"]),
    ("Relé", ["30 V 2 A", "30 V 2 A"]),
    ("PoE", ["802.3af", "802.3af"]),
    ("Fuente", ["E18C 12 V 1,5 A", "E16C 12 V 1 A"]),
    ("Salida de 12 V", [("no tiene", "alert"), ("no tiene", "alert")]),
], first_w=230, col_w=235, row_h=44)
c.add(g)
c.add(text(452 + 230 + 117, 126 + H + 26, "E18 con LTE: 12 V 2,5 A", 15, 500, INK3, FM, anchor="middle"))
c.add(Note(452, 126 + H + 44, W, "Sin salida de 12 V en E18C ni E16C: la cerradura va siempre con fuente propia.", kind="warn", size=15))
save(c, "27.svg")

# ---------------------------------------------------------------- 27-paso1: PIN de sistema por firmware
c = Canvas("Akuvox · Paso 1", "¿admin o Admin321? Depende del firmware")
c.add(portero(80, 140, "pantalla", 0.72))
c.add(f'<circle cx="134" cy="230" r="34" fill="none" stroke="{WARN}" stroke-width="3" stroke-dasharray="6 5"/>')
c.add(pill(150, 382, "mantené la pantalla 5 s", BLUE, WHITE, 15, False))
for i, (m, cut) in enumerate([("E16", "216.30.10.121"), ("E18", "18.30.10.211")]):
    y = 160 + i * 130
    c.add(text(300, y + 20, m, 22, 700, INK, FD))
    c.add(f'<rect x="380" y="{y - 10}" width="360" height="56" rx="12" fill="{SOFT}" stroke="{LINE2}"/>')
    c.add(text(400, y + 14, f"hasta {cut}", 15, 500, INK2, FM))
    c.add(text(400, y + 36, "PIN: admin", 17, 700, INK, FM))
    c.add(f'<rect x="752" y="{y - 10}" width="400" height="56" rx="12" fill="{OK_BG}" stroke="{OK}"/>')
    c.add(text(772, y + 14, "después", 15, 500, INK2, FM))
    c.add(text(772, y + 36, "PIN: Admin321", 17, 700, OK, FM))
c.add(Note(300, 430, 852, "Paso 2: el firmware empieza con 18. (E18) o 116. / 216. / 416. (los tres hardware del E16). Paso 5: cambiá el PIN de sistema por uno propio el primer día.", kind="info", size=15))
save(c, "27-paso1.svg")

# ---------------------------------------------------------------- 27-paso3: cableado con fuente propia
c = Canvas("Akuvox · Paso 3", "Sin salida de 12 V: la cerradura lleva su fuente")
c.add(portero(60, 150, "pantalla", 0.86, "E16C / E18C", "PoE o fuente propia"))
r = c.add(Relay(330, 160, "Relé A del portero", "30 V 2 A"))
c.add(wire([(189, 230), (330, 215)], "relay"))
c.add(PSU(330, 400, "Fuente de la cerradura", "12 V", w=270))
c.add(Lock(760, 400, "Cerradura", "fail-secure (NO)", w=250))
c.add(wire([r.port("COM"), (370, 340), (420, 340), (420, 400)], "power+"))
c.add(wire([r.port("NO"), (430, 310), (840, 310), (840, 400)], "power+"))
c.add(wire([(600, 455), (760, 455)], "power-"))
c.add(text(660, 300, "NO → + cerradura", 15, 600, RED, FM))
c.add(text(240, 364, "+ fuente → COM", 15, 600, RED, FM))
c.add(text(680, 484, "− a −", 15, 600, INK, FM, anchor="middle"))
c.add(check(760, 196, False) + text(784, 202, "no hay borne de 12 V en estos modelos", 16, 600, ALERT, FB))
c.add(Note(48, 560, 1104, "Cableado de la lección 4: para fail-safe, NC en lugar de NO. Electroimán: diodo en antiparalelo.", kind="info", size=16))
save(c, "27-paso3.svg")
