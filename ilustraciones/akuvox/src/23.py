import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/akuvox/src")
from _cat import *

# ---------------------------------------------------------------- 23.svg: X912 y X910
c = Canvas("Akuvox · Lección 23", "X912 y X910: pantalla antivandálica o un botón")
c.add(portero(60, 150, "pantalla", 0.86, "X912", "acero · táctil"))
c.add(portero(240, 150, "boton", 0.86, "X910", "un botón"))
c.add(text(181, 450, "X912 también en versión", 15, 400, INK3, FB, anchor="middle"))
c.add(text(181, 470, "con teclado físico", 15, 400, INK3, FB, anchor="middle"))
c.add(text(181, 504, "X910: detección de paquetes", 15, 400, INK3, FB, anchor="middle"))
g, W, H = grid(452, 126, ["X912", "X910"], [
    ("PIN", [True, False]),
    ("Tarjeta", ["13,56 y 125 kHz", "solo 13,56 MHz"]),
    ("Rostro", [True, False]),
    ("Bluetooth y QR", [True, True]),
    ("Relé", ["30 V 3 A", "30 V 2 A"]),
    ("PoE", ["PoE+ 802.3at", "802.3af o 12-24 V"]),
    ("12 V por el relé", ["1 A", "600 mA"]),
    ("12 V pide", [("PoE+ o 12 V 2,5 A", "warn"), ("PoE+ o 12 V 2 A", "warn")]),
], first_w=230, col_w=235, row_h=44)
c.add(g)
c.add(Note(452, 126 + H + 18, W, "X910 con PoE af anda, pero su salida de 12 V no alcanza: pide PoE+ o fuente.", kind="warn", size=15))
save(c, "23.svg")

# ---------------------------------------------------------------- 23-paso1: sacar la IP
c = Canvas("Akuvox · Lección 23 · Paso 1", "Cómo te dice la IP cada uno")
c.add(text(48, 168, "X912", 22, 700, INK, FD))
c.add(screen_flow(160, 130, [("ícono de llave", "🔑" if False else "llave"), ("2396", "2396"), ("Dial", "IP")], w=250, h=120, gap=50))
c.add(text(48, 420, "X910", 22, 700, INK, FD))
c.add(portero(170, 340, "boton", 0.62))
c.add(f'<circle cx="{170 + 75 * 0.62:.1f}" cy="{340 + 214 * 0.62:.1f}" r="26" fill="none" stroke="{WARN}" stroke-width="3" stroke-dasharray="5 5"/>')
c.add(pill(330, 486, "mantené 5 s", BLUE, WHITE, 16, False))
c.add(arrow((290, 440), (440, 440), "flow", bend="straight"))
c.add(f'<path d="M460 400h380a16 16 0 0 1 16 16v48a16 16 0 0 1 -16 16h-340l-30 22v-22h-10a16 16 0 0 1 -16 -16v-48a16 16 0 0 1 16 -16z" fill="{WHITE}" stroke="{BLUE}" stroke-width="2"/>')
c.add(text(658, 448, "anuncia la IP en voz alta", 18, 600, INK, FB, anchor="middle"))
c.add(Note(900, 380, 252, "Paso 2: en la web, el firmware empieza con 912. o 2910.", kind="info", size=15))
save(c, "23-paso1.svg")

# ---------------------------------------------------------------- 23-paso4: medir con la carga
c = Canvas("Akuvox · Lección 23 · Paso 4", "Medí los 12 V con la cerradura conectada")
c.add(panel(48, 126, 540, 430, "En vacío", "warn"))
c.add(portero(80, 186, "pantalla", 0.72))
c.add(tester(330, 170, "12 V", None, None))
c.add(wire([(188, 260), (260, 260), (260, 420), (368, 420), (368, 334)], "power+", dots=False))
c.add(wire([(188, 290), (240, 290), (240, 450), (422, 450), (422, 334)], "power-", dots=False))
c.add(text(80, 520, "Puede marcar 12 V y engañarte.", 17, 600, WARN, FB))
c.add(panel(612, 126, 540, 430, "Con la cerradura, al abrir", "ok"))
c.add(portero(644, 186, "pantalla", 0.72))
c.add(tester(850, 160, "__ V", True, None))
c.add(Lock(800, 410, "Cerradura de banco", None, w=260))
c.add(wire([(888, 324), (888, 410)], "power+", dots=True))
c.add(wire([(942, 324), (942, 410)], "power-", dots=True))
c.add(wire([(752, 260), (780, 260), (780, 432), (800, 432)], "power+", dots=False))
c.add(wire([(752, 290), (766, 290), (766, 474), (800, 474)], "power-", dots=False))
c.add(text(1000, 250, "tester en", 15, 500, INK2, FB))
c.add(text(1000, 270, "paralelo con", 15, 500, INK2, FB))
c.add(text(1000, 290, "la cerradura", 15, 500, INK2, FB))
c.add(text(644, 530, "Abrí desde la web y leé el tester ahí.", 17, 600, OK, FB))
c.add(Note(48, 574, 1104, "Si cae: X912 con PoE+ o fuente 12 V 2,5 A; X910 con PoE+ o fuente 12 V 2 A (con PoE af no alcanza).", kind="info", size=16))
save(c, "23-paso4.svg")
