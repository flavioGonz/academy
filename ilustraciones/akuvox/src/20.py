import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/akuvox/src")
from _cat import *

# ---------------------------------------------------------------- 20.svg: S539 y S538 comparados
c = Canvas("Akuvox", "S539 y S538: mismas credenciales, otra fuente")
c.add(portero(60, 150, "pantalla_grande", 0.9, "S539", "10\" · Android"))
c.add(portero(240, 150, "pantalla", 0.9, "S538", "Tri-Vision · Android"))
c.add(pill(212, 470, "acceso principal de edificio", BLUE, SOFT, 15, False))
g, W, H = grid(452, 126, ["S539", "S538"], [
    ("PIN", [True, True]),
    ("Tarjeta 13,56 y 125 kHz", [True, True]),
    ("Rostro · Bluetooth · QR", [True, True]),
    ("Relé", ["30 V 3 A", "30 V 3 A"]),
    ("PoE", ["802.3at (PoE+)", "802.3at"]),
    ("Fuente", ["12 V 3 A o 24 V 1,5 A", ("24 V 2 A", "blue")]),
    ("12 V para cerradura", [("1 A por el relé", "warn"), ("500 mA borne propio", "ok")]),
], first_w=270, col_w=215, row_h=44)
c.add(g)
c.add(Note(452, 126 + H + 20, W, "S539: la salida de 12 V solo con fuente de 24 V 2,5 A o más. S538 para frío: solo fuente de 24 V 2 A o más.", kind="warn", size=15))
save(c, "20.svg")

# ---------------------------------------------------------------- 20-paso1: sacar la IP
c = Canvas("Akuvox · Paso 1", "Sacá la IP desde la pantalla del portero")
c.add(screen_flow(48, 160, [("9999 + Dial", "9999"), ("3888 + OK", "3888"), ("System Info", "System Info"), ("Network (S539)", "IP: 192.168.88.x")], w=240, h=150, gap=48))
c.add(Note(48, 420, 540, "Después, en la web: Status > Basic > Product Information. El firmware empieza con 539. o 538.", title="Paso 2", kind="info", size=15))
c.add(Note(612, 420, 540, "Tercer bloque del firmware 10 o más: rama de alta seguridad (afecta la URL de apertura, lección 14).", kind="info", size=15))
c.add(text(48, 580, "Mismo camino en S539, S538, S535, X915, X916 y R29.", 17, 600, INK2, FB))
save(c, "20-paso1.svg")

# ---------------------------------------------------------------- 20-paso3: PoE o fuente
c = Canvas("Akuvox · Paso 3", "¿El puerto del switch da 802.3at?")
c.add(Router(48, 140, "Switch PoE", "puerto 802.3at (PoE+)", ports=["1", "2", "3", "4"], hl={"1": CYAN, "2": CYAN}))
c.add(portero(560, 150, "pantalla_grande", 0.72, "S539", None))
c.add(portero(860, 150, "pantalla", 0.72, "S538", None))
c.add(wire([(105, 310), (105, 360), (520, 360), (520, 230), (560, 230)], "data"))
c.add(wire([(189, 310), (189, 380), (820, 380), (820, 230), (860, 230)], "data"))
c.add(PSU(680, 170, "Fuente", "12 V 3 A o 24 V 1,5 A", w=170) if False else "")
c.add(panel(48, 440, 540, 170, "S539", "info"))
c.add(text(68, 500, "PoE+ 802.3at", 17, 600, BLUE, FM))
c.add(text(68, 530, "o fuente 12 V 3 A", 17, 500, INK2, FM))
c.add(text(68, 560, "o fuente 24 V 1,5 A", 17, 500, INK2, FM))
c.add(panel(612, 440, 540, 170, "S538", "info"))
c.add(text(632, 500, "PoE 802.3at", 17, 600, BLUE, FM))
c.add(text(632, 530, "o fuente 24 V 2 A", 17, 500, INK2, FM))
c.add(text(632, 570, "versión para frío: solo fuente 24 V 2 A+", 16, 600, WARN, FB))
c.add(Note(360, 140, 180, "Un puerto af no alcanza.", kind="warn", size=15) if False else "")
save(c, "20-paso3.svg")

# ---------------------------------------------------------------- 20-paso4: 12 V para la cerradura
c = Canvas("Akuvox · Paso 4", "¿De dónde saca 12 V la cerradura?")
c.add(panel(48, 126, 540, 420, "S539 · 12 V por el relé", "warn"))
c.add(portero(80, 186, "pantalla_grande", 0.7, None, None))
c.add(PSU(80, 400, "Fuente", "24 V 2,5 A o más", w=230))
c.add(wire([(185, 350), (185, 400)], "power+"))
c.add(Lock(350, 210, "Cerradura", "hasta 1 A", w=210))
c.add(wire([(185, 250), (350, 252)], "relay"))
c.add(text(268, 238, "salida 12 V", 15, 600, CYAN, FM, anchor="middle"))
c.add(check(370, 418, False) + text(394, 424, "con PoE solo:", 16, 600, ALERT, FB))
c.add(text(394, 448, "sin salida de 12 V", 16, 400, INK2, FB))
c.add(panel(612, 126, 540, 420, "S538 · borne de 12 V propio", "ok"))
c.add(portero(644, 186, "pantalla", 0.7, None, None))
c.add(Lock(914, 210, "Cerradura", "hasta 500 mA", w=210))
c.add(wire([(749, 290), (914, 252)], "power+"))
c.add(text(830, 300, "borne 12 V", 15, 600, RED, FM, anchor="middle"))
c.add(check(644, 418, True) + text(668, 424, "independiente del relé", 16, 600, OK, FB))
c.add(Note(48, 566, 1104, "Una cerradura que pide más de lo que da la salida de 12 V va con fuente propia (lección 4).", kind="warn", size=16))
save(c, "20-paso4.svg")
