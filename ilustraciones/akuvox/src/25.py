import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/akuvox/src")
from _cat import *

# ---------------------------------------------------------------- 25.svg: R28 y R25
c = Canvas("Akuvox", "R28 y R25: ¿PIN y 12 V para la cerradura?")
c.add(portero(60, 150, "pantalla_teclado", 0.8, "R28", "4,3\" no táctil"))
c.add(portero(210, 150, "boton", 0.8, "R25A", "un botón"))
c.add(portero(340, 150, "teclado", 0.8, "R25K", None))
g, W, H = grid(500, 126, ["R28", "R25A / R25K"], [
    ("PIN", [True, (("la tabla: sin PIN"), "alert")]),
    ("Tarjeta 13,56 y 125 kHz", [True, True]),
    ("Relé", ["30 V 3 A", "30 V 2 A"]),
    ("Alimentación", ["PoE af o 12 V 1 A", "PoE af o 12 V 1 A"]),
    ("Salida de 12 V", [("400 mA, borne propio", "ok"), ("400 mA por el relé", "warn")]),
    ("12 V con PoE", [("sí", "ok"), ("depende del volumen", "warn")]),
], first_w=230, col_w=211, row_h=46)
c.add(g)
c.add(Note(500, 126 + H + 18, W, "R25 con PoE: la salida de 12 V pide firmware 25.30.10.11 o más y cambia con el volumen del equipo.", kind="warn", size=15))
c.add(Note(48, 500, 420, "El R28 da 12 V por un borne propio, sin ocupar el relé.", kind="ok", size=15))
save(c, "25.svg")

# ---------------------------------------------------------------- 25-paso1: cómo te dan la IP
c = Canvas("Akuvox · Paso 1", "Tres modelos, tres formas de pedir la IP")
items = [("R28", "pantalla_teclado", ["*2396#", "después 1"]),
         ("R25A", "boton", ["mantené el botón", "5 s"]),
         ("R25K", "teclado", ["*3258*", "(como el R20K)"])]
for i, (m, k, how) in enumerate(items):
    x = 48 + i * 376
    c.add(panel(x, 126, 352, 420, m, "info"))
    c.add(portero(x + 108, 170, k, 0.88))
    c.add(text(x + 176, 470, how[0], 20, 700, BLUE, FM, anchor="middle"))
    c.add(text(x + 176, 502, how[1], 17, 500, INK2, FB, anchor="middle"))
c.add(Note(48, 566, 1104, "Paso 2: el firmware en la web empieza con 28. (o 228. en la versión 2 del R28) y 25. en los R25.", kind="info", size=16))
save(c, "25-paso1.svg")

# ---------------------------------------------------------------- 25-paso3: medir con volumen bajo y alto
c = Canvas("Akuvox · Paso 3", "R25 con PoE: medí con volumen bajo y alto")
c.add(Router(48, 150, "Switch PoE", "802.3af", ports=["1", "2", "3"], hl={"1": CYAN}))
c.add(portero(420, 150, "boton", 0.8, "R25A", "PoE"))
c.add(wire([(105, 320), (105, 360), (390, 360), (390, 210), (420, 210)], "data"))
c.add(Lock(640, 300, "Carga de banco", "12 V por el relé", w=240))
c.add(wire([(540, 260), (600, 260), (600, 330), (640, 330)], "power+", dots=False))
c.add(wire([(540, 290), (585, 290), (585, 360), (640, 360)], "power-", dots=False))
c.add(tester(960, 140, "__ V", None, None))
c.add(wire([(998, 304), (998, 320), (880, 320)], "power+", dots=False))
c.add(wire([(1052, 304), (1052, 350), (880, 350)], "power-", dots=False))
c.add(panel(612, 430, 540, 140, "Durante la apertura", "info"))
c.add(text(632, 498, "Volumen bajo : ____ V", 18, 600, INK, FM))
c.add(text(632, 534, "Volumen alto : ____ V", 18, 600, INK, FM))
c.add(Note(48, 430, 540, "Akuvox avisa que con PoE la salida de 12 V del R25 se ve afectada por el ajuste de volumen. Medilo vos.", kind="warn", size=15))
save(c, "25-paso3.svg")

# ---------------------------------------------------------------- 25-paso4: si la caída afecta
c = Canvas("Akuvox · Paso 4", "Si la tensión cae, separá la cerradura")
c.add(panel(48, 126, 540, 470, "Opción 1: fuente para el portero", "info"))
c.add(PSU(78, 196, "Fuente", "12 V 1 A", w=200))
c.add(portero(380, 186, "boton", 0.72, "R25", None))
c.add(wire([(278, 238), (380, 238)], "power+"))
c.add(Lock(78, 390, "Cerradura", "por el relé", w=220))
c.add(wire([(380, 300), (340, 300), (340, 432), (298, 432)], "relay"))
c.add(text(78, 560, "Sirve en banco y en obras chicas.", 16, 500, INK2, FB))
c.add(panel(612, 126, 540, 470, "Opción 2: fuente propia para la cerradura", "ok"))
c.add(portero(644, 186, "boton", 0.72, "R25", "PoE"))
c.add(Relay(820, 196, "Relé del portero", "contacto seco"))
c.add(wire([(752, 250), (820, 250)], "relay"))
c.add(PSU(650, 440, "Fuente", "de la cerradura", w=210))
c.add(Lock(900, 410, "Cerradura", None, w=230))
c.add(wire([(860, 306), (860, 400), (800, 400), (800, 440)], "power+"))
c.add(wire([(920, 306), (920, 360), (1015, 360), (1015, 410)], "power+"))
c.add(wire([(1015, 494), (1015, 540), (750, 540), (750, 524)], "power-"))
c.add(text(870, 386, "+ a COM", 15, 600, RED, FM))
c.add(text(930, 350, "NO a +", 15, 600, RED, FM))
c.add(check(644, 574, True) + text(668, 580, "En obra: la cerradura no depende del volumen.", 16, 600, OK, FB))
c.add(Note(48, 612, 1104, "Cableado en NO (fail-secure) como en la lección 4; para fail-safe, NC.", kind="info", size=15) if False else "")
save(c, "25-paso4.svg")
