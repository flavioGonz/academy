import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/akuvox/src")
from _cat import *

# ---------------------------------------------------------------- 22.svg: X916 y X915
c = Canvas("Akuvox", "X916 y X915: los Android de acero")
c.add(portero(60, 140, "pantalla_grande", 0.92, "X916", "13\" · Starlight"))
c.add(portero(240, 160, "pantalla", 0.84, "X915", "8\""))
c.add(pill(212, 480, "edificio de categoría", BLUE, SOFT, 15, False))
g, W, H = grid(452, 126, ["X916", "X915"], [
    ("Versiones", ["estándar · LTE", "estándar · HID · palma"]),
    ("Relé", [("30 V 5 A", "ok"), "30 V 3 A"]),
    ("PoE", ["PoE+", "PoE+"]),
    ("Fuente", ["12 V 4 A o 24 V 2 A", "24 V 2 A"]),
    ("12 V para cerradura", ["500 mA", "1 A"]),
    ("12 V pide", [("fuente 24 V 2,5 A", "warn"), ("fuente 24 V 2,5 A *", "warn")]),
], first_w=230, col_w=235, row_h=46)
c.add(g)
c.add(text(452, 126 + H + 30, "* salvo X915 V2 con cierto hardware y firmware (paso 4).", 15, 400, INK3, FB))
c.add(Note(452, 126 + H + 52, W, "El X916 tiene el relé más fuerte de la línea: 30 V 5 A.", kind="ok", size=15))
save(c, "22.svg")

# ---------------------------------------------------------------- 22-paso3: IP65 o IP66
c = Canvas("Akuvox · Paso 3", "¿IP65 o IP66? Vale la ficha de la versión")
c.add(doc(48, 140, 330, 230, "Guía de selección", ["Porteros · todos los modelos", "X915", ("IP65", "warn")], "warn", None))
c.add(doc(430, 140, 330, 230, "Ficha X915 V2.0", ["acero inoxidable · 8\"", "PoE+ · Android", ("IP66 · IK10", "ok")], "ok", None))
c.add(arrow((760, 255), (830, 255), "ok", bend="straight"))
c.add(panel(840, 140, 312, 230, "Planilla / pliego", "info"))
c.add(text(860, 210, "X915 V2.0", 17, 600, INK, FM))
c.add(text(860, 244, "IP66 · IK10", 17, 700, OK, FM))
c.add(text(860, 278, "fuente: ficha X915 V2.0", 15, 500, INK2, FM))
c.add(check(213, 405, False) + text(237, 411, "general", 16, 600, ALERT, FB))
c.add(check(595, 405, True) + text(619, 411, "versión exacta", 16, 600, OK, FB))
c.add(Note(48, 460, 1104, "Dos páginas del mismo fabricante, dos números. En una propuesta se cita la ficha de la versión que se compra, con su nombre, no la guía general.", kind="info", size=16))
save(c, "22-paso3.svg")

# ---------------------------------------------------------------- 22-paso4: alimentación
c = Canvas("Akuvox · Paso 4", "¿Cerradura desde el portero? Decidí la fuente")
c.add(box(410, 130, 380, 64, "¿Cerradura desde el portero?", None, "dark", None, 19, center=True))
c.add(arrow((470, 194), (250, 270), "flow", "no", label_dy=-6))
c.add(arrow((730, 194), (950, 270), "flow", "sí", label_dy=-6))
c.add(box(70, 272, 360, 80, "PoE+ 802.3at", "alcanza", "ok", None, 20, center=True))
c.add(box(770, 272, 360, 80, "Fuente 24 V 2,5 A o más", "para X916 y X915", "warn", None, 19, center=True))
c.add(arrow((950, 352), (950, 420), "flow", "excepción", label_dy=0))
c.add(panel(612, 424, 540, 150, "Excepción X915 V2", "ok"))
c.add(text(632, 488, "hardware 2915.1.0.8 a 2915.1.0.13", 16, 500, INK2, FM))
c.add(text(632, 516, "y firmware 2915.30.10.228 o más", 16, 500, INK2, FM))
c.add(text(632, 550, "→ la salida de 12 V anda también con PoE", 16, 600, OK, FB))
c.add(Note(48, 424, 520, "La versión de hardware se lee en Status > Basic > Product Information (paso 2). El X915 tiene dos.", kind="info", size=16))
save(c, "22-paso4.svg")
