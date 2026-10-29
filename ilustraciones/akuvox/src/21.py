import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/akuvox/src")
from _cat import *

# ---------------------------------------------------------------- 21.svg: S535 por módulos, S532 por versiones
c = Canvas("Akuvox", "S535 se arma por módulos; S532 viene en versiones")
c.add(panel(48, 122, 640, 300, "S535 · Linux · 5\" · IP66", "info"))
c.add(portero(80, 168, "pantalla", 0.82, None, None))
mods = [("Huella", "key"), ("LTE", "wifi"), ("Lector QR", "card"), ("Lazo de inducción", "bell")]
for i, (m, ic) in enumerate(mods):
    y = 170 + i * 60
    c.add(box(330, y, 330, 48, m, None, "soft", None, 17))
    c.add(wire([(205, 290), (300, 290), (300, y + 24), (330, y + 24)], "logical", dots=False))
c.add(text(270, 284, "+", 26, 700, INK3, FD, anchor="middle"))
c.add(panel(712, 122, 440, 300, "S532 · 2,8\"", "info"))
c.add(portero(744, 168, "pantalla", 0.82, None, None))
for i, v in enumerate(["estándar", "IP", "lazo de inducción"]):
    c.add(Chip(900, 210 + i * 56, v, "gray", mono=False))
g, W, H = grid(48, 440, ["S535", "S532"], [
    ("Rostro y QR", [True, False]),
    ("Relé", ["30 V 2 A", "30 V 3 A"]),
    ("12 V para cerradura", [("hasta 1 A por el relé", "ok"), ("500 mA, solo con fuente", "warn")]),
], first_w=300, col_w=402, row_h=44)
c.add(g)
save(c, "21.svg")

# ---------------------------------------------------------------- 21-paso1: el pedido del S535
c = Canvas("Akuvox · Paso 1", "El pedido del S535 lleva cada módulo")
c.add(doc(48, 130, 520, 380, "Pedido · edificio con huella y LTE", [
    ("1 x S535 (frente)", "blue"), ("1 x módulo de huella", "blue"), ("1 x módulo LTE", "blue"),
    "Alimentación: PoE+ 802.3at en el switch,", "o fuente 12 V (hasta 4 A)",
    "Cerradura desde el portero:", ("hasta 12 V / 1 A por el relé", "ok")], "info"))
c.add(Step(48, 130, 1))
c.add(portero(660, 150, "pantalla", 0.9, "S535", "frente"))
c.add(box(860, 160, 292, 60, "Módulo de huella", None, "soft"))
c.add(box(860, 240, 292, 60, "Módulo LTE", None, "soft"))
c.add(wire([(795, 260), (830, 260), (830, 190), (860, 190)], "logical", dots=False))
c.add(wire([(830, 260), (860, 270)], "logical", dots=False))
c.add(Note(612, 470, 540, "Si el pedido dice solo \"S535\", llega el frente sin huella ni LTE.", kind="warn", size=16))
save(c, "21-paso1.svg")

# ---------------------------------------------------------------- 21-paso2: S532 y la salida de 12 V
c = Canvas("Akuvox · Paso 2", "S532 con cerradura: ¿alcanza el PoE?")
c.add(panel(48, 126, 540, 380, "Solo PoE+", "alert"))
c.add(Router(76, 186, "Switch PoE", "", ports=["1", "2", "3"], hl={"1": CYAN}))
c.add(portero(410, 186, "pantalla", 0.62, None, None))
c.add(wire([(133, 356), (133, 390), (380, 390), (380, 240), (410, 240)], "data"))
c.add(check(80, 456, False) + text(104, 462, "el portero anda, pero sin salida de 12 V", 16, 600, ALERT, FB))
c.add(panel(612, 126, 540, 380, "Fuente 12 V 2,5 A o más", "ok"))
c.add(PSU(640, 196, "Fuente", "12 V 2,5 A", w=200))
c.add(portero(880, 186, "pantalla", 0.62, None, None))
c.add(wire([(840, 238), (880, 238)], "power+"))
c.add(Lock(880, 346, "Cerradura", "500 mA máx.", w=230))
c.add(wire([(973, 330), (973, 346)], "relay"))
c.add(text(990, 342, "12 V", 15, 600, CYAN, FM))
c.add(check(640, 456, True) + text(664, 462, "salida de 12 V para una cerradura chica", 16, 600, OK, FB))
c.add(Note(48, 530, 1104, "Cerradura de más de 500 mA en el S532 (o de más de 1 A en el S535): fuente propia para la cerradura.", kind="warn", size=16))
save(c, "21-paso2.svg")

# ---------------------------------------------------------------- 21-paso3: cómo se entra a cada uno
c = Canvas("Akuvox · Paso 3", "Cada uno se abre con otro código")
c.add(text(48, 180, "S535", 22, 700, INK, FD))
c.add(screen_flow(160, 150, [("9999 + Dial", "9999"), ("3888 + OK", "3888"), ("System Info", "System Info")], w=250, h=120, gap=50))
c.add(text(48, 430, "S532", 22, 700, INK, FD))
c.add(screen_flow(160, 400, [("*2396#", "*2396#"), ("1", "1")], w=250, h=120, gap=50))
c.add(Note(860, 410, 292, "S532 se entra igual que el R28 y el R27.", kind="info", size=15))
save(c, "21-paso3.svg")
