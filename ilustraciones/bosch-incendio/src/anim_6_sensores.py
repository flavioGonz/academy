"""Teoría de Elegir detector: qué mira cada sensor y cómo los combina el multisensor."""
from _anim_bi import *

caps = ["Humo: las partículas dispersan la luz del LED hacia el receptor.",
        "Calor: el térmico mira el máximo (54 o 69 °C) o el gradiente.",
        "CO: un fuego latente lo genera temprano; la celda química lo ve.",
        "El algoritmo combina las señales: el vapor solo mueve el óptico."]
a = new(24, "Sensores", "Cada sensor mira una huella distinta del fuego", caps, still=3)

a.add(a.box(430, 200, 340, 340, a.WHITE, a.LINE, rx=170, sw=3))
a.add(a.text(600, 380, "Multisensor", 20, a.INK, a.SANS, 600, "middle"))
a.add(a.text(600, 406, "FAP-425-DOTC-R", 15, a.GREY, a.MONO, 400, "middle"))
S = [(70, 210, "Óptico", "luz dispersada", a.BLUE), (70, 360, "Térmico", "máximo o gradiente", a.AMB), (70, 510, "Químico", "CO", a.OK)]
for x, y, t, s, col in S:
    a.add(a.box(x, y, 260, 90, a.WHITE, a.LINE, rx=14, sw=2))
    a.add(a.text(x + 20, y + 38, t, 19, a.INK, a.SANS, 600))
    a.add(a.text(x + 20, y + 66, s, 15, a.GREY, a.MONO))
    a.add(line(a, x + 262, y + 45, 440, 370, a.LINE, 2, arrow=False))
for i, (x, y, t, s, col) in enumerate(S):
    vis(a, a.box(x, y, 260, 90, "none", col, rx=14, sw=4), i, 3)
# estímulos
s0, s1 = ph(a, 0)
for k in range(6):
    t0 = s0 + 1 + k * 2.5
    mv = a.move([(0, 380 + k * 14, 190), (t0, 380 + k * 14, 190), (t0 + 10, 300 - k * 10, 255), (100, 300 - k * 10, 255)])
    op = a.keyframes([(0, 0), (t0, 0), (t0 + 0.5, 1), (s1 - 2, 1), (s1, 0), (100, 0)])
    a.add(a.group(f'<circle cx="0" cy="0" r="7" fill="{a.GREY}" fill-opacity=".7"/>', mv, op, still=0))
vis(a, a.pill(380, 166, "humo", a.GREY, a.SLATE), 0)
vis(a, f'<path d="M400 470 q15 -20 0 -40 q-15 -20 0 -40" fill="none" stroke="{a.AMB}" stroke-width="4"/>', 1)
vis(a, a.pill(420, 470, "calor", a.AMB, a.AMBBG), 1)
s0, s1 = ph(a, 2)
token(a, "CO", [(s0 + 2, 420, 620), (s0 + 14, 300, 560), (s1 - 1, 300, 560)], bg=a.OK)
# decisión
a.add(a.box(860, 300, 290, 140, a.INK, rx=16))
a.add(a.text(880, 338, "Algoritmo", 19, a.WHITE, a.SANS, 600))
a.add(line(a, 772, 370, 856, 370, a.BLUE))
vis(a, a.text(880, 376, "fuego: varias señales juntas", 15, "#9FC3E3", a.MONO), 3)
vis(a, a.text(880, 404, "vapor: solo el óptico", 15, "#9FC3E3", a.MONO), 3)
vis(a, a.pill(1005, 470, "alarma de fuego", a.WHITE, a.BAD, anchor="middle"), 3)
a.add(a.text(48, 650, "El CO también reacciona a hidrógeno y monóxido de nitrógeno, según la hoja de datos.", 15, a.TXT))
write(a, "6-t1.svg", "Qué mira cada sensor", [12, 37, 62, 90])
