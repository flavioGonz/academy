#!/usr/bin/env python3
"""Lección 8 · Laboratorio, paso 4: repetir la caminata en los mismos tres puntos y comparar con la línea de base.
En B el celular cambia de AP; en C ya está en el AP 2 con -65 dBm o mejor. Los valores son de ejemplo; los umbrales
(-70 mínimo, -65 recomendado) son los de la lección, según WunderTech. Fuentes: lab.md (pasos 1 a 5) de la lección."""
from _anim_red_unifi import *  # noqa

a = new(24, "Potencia baja", "La caminata de después: mismos puntos, otro resultado", [
    "La línea de base del paso 1: señal y AP en A, B y C.",
    "Con la potencia nueva, repetís la caminata en los mismos puntos.",
    "En B el celular cambia de AP: esa es la zona de traspaso.",
    "En C ya está en el AP 2 con -65 dBm o mejor: la meta del paso.",
], still=3, paso=4)

Y = 250
a.add(wire(150, Y, 1050, Y, a.LINE, 3, "8 8"))
a.add(ap_icon(a, 110, Y, 24) + a.text(110, Y - 38, "AP 1", 16, a.INK, a.SANS, 600, "middle"))
a.add(ap_icon(a, 1090, Y, 24) + a.text(1090, Y - 38, "AP 2", 16, a.INK, a.SANS, 600, "middle"))
PX = {"A": 300, "B": 600, "C": 900}
for k, x in PX.items():
    a.add(f'<circle cx="{x}" cy="{Y}" r="16" fill="{a.WHITE}" stroke="{a.INK}" stroke-width="2"/>' + a.text(x, Y + 6, k, 16, a.INK, a.MONO, 600, "middle"))

# celular caminando en el tiempo 2 y 3
s0, _ = ph(a, 1)
_, s3 = ph(a, 2)
kf = [(0, PX["A"], Y + 50), (27, PX["A"], Y + 50), (48, PX["A"], Y + 50), (56, PX["B"], Y + 50), (73, PX["B"], Y + 50),
      (81, PX["C"], Y + 50), (100, PX["C"], Y + 50)]
ph_icon = phone_icon(a, 0, 0)
a.add(a.group(ph_icon, a.move(kf), a.show(s0 + 1, 100, 0.5), still=0))
still_only(a, phone_icon(a, PX["C"], Y + 50))
# enlace al AP actual
vis(a, poly([(PX["A"], Y + 28), (134, Y + 10)], a.OK, 2.5, "5 5"), 1)
vis(a, poly([(PX["B"], Y + 28), (1066, Y + 10)], a.OK, 2.5, "5 5"), 2)
vis(a, poly([(PX["C"], Y + 28), (1066, Y + 10)], a.OK, 2.5, "5 5"), 3)
vis(a, pill(a, PX["B"], Y + 86, "AP 1 → AP 2", "info", anchor="middle"), 2)

# tabla
TX, TY = 48, 370
a.add(a.box(TX, TY, 700, 210, a.WHITE, a.LINE, rx=14))
for i, h in enumerate(("Punto", "Antes (paso 1)", "Después (paso 4)")):
    a.add(a.text(TX + 24 + i * 210, TY + 34, h, 16, a.GREY, a.SANS, 600))
a.add(wire(TX + 20, TY + 50, TX + 680, TY + 50, a.LINE, 2))
BEFORE = [("A", "AP 1 · -55", a.OK), ("B", "AP 1 · -62", a.OK), ("C", "AP 1 · -72", a.BAD)]
AFTER = [("AP 1 · -58", a.OK, 1), ("AP 2 · -66", a.AMB, 2), ("AP 2 · -60", a.OK, 3)]
for j, ((p, v, c), (v2, c2, when)) in enumerate(zip(BEFORE, AFTER)):
    y = TY + 88 + j * 44
    a.add(a.text(TX + 24, y, p, 18, a.INK, a.MONO, 600))
    vis(a, a.text(TX + 234, y, v + " dBm", 16, c, a.MONO, 600), 0, 3)
    vis(a, a.text(TX + 444, y, v2 + " dBm", 16, c2, a.MONO, 600), when if when < 3 else 3, 3)
a.add(a.text(TX + 24, TY + 200, "valores de ejemplo", 15, a.GREY, a.SANS))

# escala
SX, SY, SH = 800, 370, 210
a.add(a.box(SX, SY, 352, SH, a.WHITE, a.LINE, rx=14))
a.add(a.text(SX + 20, SY + 34, "Señal en el celular", 16, a.INK, a.SANS, 600))
ZONES = [("-50 a -65", "recomendado", a.OK, a.OKBG), ("-65 a -70", "hasta el mínimo", a.AMB, a.AMBBG), ("peor que -70", "candidato a otro AP", a.BAD, a.BADBG)]
for i, (r, t, c, bg) in enumerate(ZONES):
    y = SY + 52 + i * 50
    a.add(a.box(SX + 20, y, 312, 40, bg, None, rx=8) + a.text(SX + 34, y + 26, r, 15, c, a.MONO, 600) + a.text(SX + 318, y + 26, t, 15, a.INK, a.SANS, 400, "end"))
vis(a, a.box(SX + 18, SY + 50, 316, 44, "none", a.OK, rx=9, sw=3), 3)

status(a, 628, [
    (0, 25, "Sin línea de base no hay comparación: mismos puntos, mismo celular.", a.INK, 0),
    (25, 50, "Esperá un par de minutos después de Apply Changes antes de caminar.", a.INK, 0),
    (50, 75, "Un traspaso en el medio es lo esperado, no una falla.", a.OK, 0),
    (75, 100, "Si algún punto queda peor que -70 dBm, anotalo para un AP más.", a.AMB, 1),
])

write(a, 8, "l1", "La caminata de después",
      "Animación en cuatro tiempos del paso 4 con el AP 1 y el AP 2 en los extremos de un pasillo, los puntos A, B y C, una tabla antes y después con valores de ejemplo y la escala de señal. "
      "1: la línea de base del paso 1: en A AP 1 con -55 dBm, en B AP 1 con -62 y en C todavía AP 1 con -72, peor que el mínimo. "
      "2: con la potencia nueva y un par de minutos de espera se repite la caminata; en A sigue en el AP 1 con -58. "
      "3: en B el celular pasa del AP 1 al AP 2, con -66: es la zona de traspaso. "
      "4: en C ya está en el AP 2 con -60 dBm, dentro de lo recomendado de -65 o mejor. "
      "Escala: de -50 a -65 recomendado, de -65 a -70 hasta el mínimo, peor que -70 candidato a otro AP.",
      [12, 37, 64, 92])
