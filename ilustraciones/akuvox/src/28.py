import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/akuvox/src")
from _cat import *

# ---------------------------------------------------------------- 28.svg: E13S y E12
c = Canvas("Akuvox · Lección 28", "E13S y E12: un botón, tarjeta y fuente aparte")
c.add(portero(60, 150, "boton", 0.86, "E13S", "un botón · IP65"))
c.add(portero(240, 150, "boton", 0.86, "E12", "E12S / E12W"))
c.add(pill(212, 470, "casa u oficina chica", BLUE, SOFT, 15, False))
g, W, H = grid(452, 126, ["E13S", "E12"], [
    ("Tarjeta 13,56 MHz", [True, True]),
    ("PIN · rostro", [False, False]),
    ("Bluetooth", [None, True]),
    ("Wi-Fi", [None, ("E12W (guía)", "blue")]),
    ("Relé", ["30 V 2 A", "30 V 2 A"]),
    ("Alimentación", ["PoE (guía)", "PoE af o 12 V 1 A"]),
    ("Salida de 12 V", [None, ("no tiene", "alert")]),
    ("RS485 para SR01", [None, ("no tiene", "alert")]),
], first_w=230, col_w=235, row_h=44)
c.add(g)
c.add(dash_mark(470, 126 + H + 24) + text(490, 126 + H + 30, "sin dato en las tablas leídas", 15, 400, INK3, FB))
c.add(Note(452, 126 + H + 48, W, "La cerradura va con fuente propia; si tiene que resistir que rompan el portero, otro modelo con RS485 y SR01.", kind="warn", size=15))
save(c, "28.svg")

# ---------------------------------------------------------------- 28-paso1: IP por voz y clave web
c = Canvas("Akuvox · Lección 28 · Pasos 1 y 2", "Pedile la IP al botón y cambiá la clave web")
c.add(portero(80, 150, "boton", 0.8))
c.add(f'<circle cx="140" cy="{150 + 214 * 0.8:.0f}" r="30" fill="none" stroke="{WARN}" stroke-width="3" stroke-dasharray="5 5"/>')
c.add(pill(140, 400, "mantené 5 s", BLUE, WHITE, 16, False))
c.add(Step(80, 150, 1))
c.add(f'<path d="M260 180h300a16 16 0 0 1 16 16v48a16 16 0 0 1 -16 16h-260l-30 22v-22h-10a16 16 0 0 1 -16 -16v-48a16 16 0 0 1 16 -16z" fill="{WHITE}" stroke="{BLUE}" stroke-width="2"/>')
c.add(text(410, 228, "dice la IP en voz alta", 18, 600, INK, FB, anchor="middle"))
c.add(Window(640, 140, 512, 180, "Portero · web", path="Status > Basic > Product Information",
             rows=[("Firmware", "12. / 312. / 13."), ("Clave web", "cambiarla hoy")], hl=1))
c.add(Step(640, 140, 2))
c.add(Note(48, 450, 1104, "12. y 312. son las dos versiones de hardware del E12; 13. es el E13. Mirá también la etiqueta: E12S o E12W (paso 3).", kind="info", size=16))
save(c, "28-paso1.svg")

# ---------------------------------------------------------------- 28-paso4: lo que queda en la ficha
c = Canvas("Akuvox · Lección 28 · Paso 4", "¿La cerradura tiene que resistir un ataque?")
c.add(panel(48, 126, 540, 360, "E12 con SR01", "alert"))
c.add(portero(80, 186, "boton", 0.66))
c.add(Generic(260, 200, "SR01", "conexión especial", "shield", w=290))
c.add(wire([(179, 260), (260, 242)], "alert", dash="8 6", dots=False))
c.add(check(80, 440, False) + text(104, 446, "sin RS485: Akuvox no la recomienda", 16, 600, ALERT, FB))
c.add(panel(612, 126, 540, 360, "Portero con RS485 + SR01", "ok"))
c.add(portero(644, 186, "pantalla", 0.66))
c.add(Generic(824, 200, "SR01", "adentro", "shield", w=290))
c.add(wire([(743, 260), (824, 242)], "data"))
c.add(pill(784, 236, "RS485", BLUE, WHITE, 15))
c.add(Lock(824, 320, "Cerradura", None, w=290))
c.add(wire([(969, 284), (969, 320)], "relay"))
c.add(check(644, 440, True) + text(668, 446, "rompen el portero y la puerta sigue cerrada", 16, 600, OK, FB))
c.add(text(48, 524, "Clave web perdida en un portero de un botón:", 17, 600, INK, FB))
for i, s_ in enumerate(["SmartPlus", "PC Manager en la misma LAN", "llave del equipo a soporte"]):
    c.add(Chip(48 + [0, 150, 440][i], 568, s_, "gray", mono=False))
save(c, "28-paso4.svg")
