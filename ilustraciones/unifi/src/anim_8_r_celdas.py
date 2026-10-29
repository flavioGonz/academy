#!/usr/bin/env python3
"""Lección 8 · Resumen, "Cómo se ve en la red": tamaño de celda en un local con dos AP. Al máximo, las celdas se pisan
enteras y el celular en C sigue en el AP 1; con potencia baja hay solape en B y en C pasa al AP 2; queda un rincón D
por debajo de -70 dBm; la salida es un AP más, no subirle a todos. Los dBm son de ejemplo, con los umbrales de la
lección (-70 mínimo, -65 recomendado, según WunderTech). Fuentes: idea_md, theory_md y lab.md de la lección."""
from _anim_red_unifi import *  # noqa

a = new(26, "Potencia baja", "Celdas más chicas: cada celular en el AP que tiene cerca", [
    "Al máximo: dos celdas enormes que se pisan; en C el celular sigue en el AP 1.",
    "Potencia baja: celdas chicas con solape en B; en C el celular pasa al AP 2.",
    "Queda un rincón, D, por debajo de -70 dBm.",
    "Subirle a todos vuelve al paso 1: un AP 3 con potencia baja cubre D.",
], still=3)

PX, PY, PW, PH = 48, 186, 820, 410
a.add(f'<defs><clipPath id="plan8"><rect x="{PX}" y="{PY}" width="{PW}" height="{PH}" rx="16"/></clipPath></defs>')
a.add(a.box(PX, PY, PW, PH, a.WHITE, a.LINE, rx=16))
AP1, AP2, AP3 = (200, 330), (640, 330), (770, 520)
PTS = {"A": (250, 470), "B": (420, 470), "C": (600, 470), "D": (820, 566)}


def cell(c, r, color, op=0.14):
    return (f'<g clip-path="url(#plan8)"><circle cx="{c[0]}" cy="{c[1]}" r="{r}" fill="{color}" fill-opacity="{op}" '
            f'stroke="{color}" stroke-width="2.5" stroke-dasharray="8 6"/></g>')


vis(a, cell(AP1, 470, a.BLUE) + cell(AP2, 470, a.CYAN), 0)
vis(a, cell(AP1, 260, a.BLUE) + cell(AP2, 260, a.CYAN), 1, 3)
vis(a, cell(AP3, 140, a.OK, 0.18), 3)

for (x, y), lab in ((AP1, "AP 1"), (AP2, "AP 2")):
    a.add(ap_icon(a, x, y, 22) + a.text(x, y - 34, lab, 16, a.INK, a.SANS, 600, "middle"))
vis(a, ap_icon(a, AP3[0], AP3[1], 20) + a.text(AP3[0] - 40, AP3[1] + 6, "AP 3", 16, a.OK, a.SANS, 600, "end"), 3)

for k, (x, y) in PTS.items():
    if k == "D":
        continue
    a.add(f'<circle cx="{x}" cy="{y}" r="16" fill="{a.WHITE}" stroke="{a.INK}" stroke-width="2"/>' + a.text(x, y + 6, k, 16, a.INK, a.MONO, 600, "middle"))
DX, DY = PTS["D"]
vis(a, f'<circle cx="{DX}" cy="{DY}" r="16" fill="{a.BADBG}" stroke="{a.BAD}" stroke-width="2.5"/>' + a.text(DX, DY + 6, "D", 16, a.BAD, a.MONO, 600, "middle"), 2)
vis(a, f'<circle cx="{DX}" cy="{DY}" r="16" fill="{a.OKBG}" stroke="{a.OK}" stroke-width="2.5"/>' + a.text(DX, DY + 6, "D", 16, a.OK, a.MONO, 600, "middle"), 3)

# celular en C y su enlace
CX, CY = PTS["C"]
a.add(phone_icon(a, CX + 44, CY))
vis(a, poly([(CX + 44, CY - 22), AP1], a.BAD, 3, "6 6"), 0)
vis(a, poly([(CX + 44, CY - 22), AP2], a.OK, 3, "6 6"), 1, 3)

# panel de lecturas
RX = 892
a.add(a.box(RX, 186, 260, 410, a.WHITE, a.LINE, rx=16))
a.add(a.text(RX + 20, 218, "WiFiman (ejemplo)", 16, a.INK, a.SANS, 600))
ROWS = [
    (0, [("A", "AP 1", "-55", a.OK), ("B", "AP 1", "-62", a.OK), ("C", "AP 1", "-72", a.BAD)]),
    (1, [("A", "AP 1", "-58", a.OK), ("B", "traspaso", "-66", a.AMB), ("C", "AP 2", "-60", a.OK)]),
    (2, [("A", "AP 1", "-58", a.OK), ("C", "AP 2", "-60", a.OK), ("D", "AP 2", "-76", a.BAD)]),
    (3, [("A", "AP 1", "-58", a.OK), ("C", "AP 2", "-60", a.OK), ("D", "AP 3", "-62", a.OK)]),
]
for i, rows in ROWS:
    s = ""
    for j, (p, ap, dbm, c) in enumerate(rows):
        y = 262 + j * 56
        s += a.text(RX + 20, y, p, 18, a.INK, a.MONO, 600) + a.text(RX + 52, y, ap, 16, a.TXT, a.MONO) + a.text(RX + 240, y, f"{dbm} dBm", 16, c, a.MONO, 600, "end")
    vis(a, s, i)
a.add(wire(RX + 20, 420, RX + 240, 420, a.LINE, 2))
a.add(a.text(RX + 20, 450, "mínimo  -70 dBm", 15, a.AMB, a.MONO, 600))
a.add(a.text(RX + 20, 476, "objetivo -65 o mejor", 15, a.OK, a.MONO, 600))
vis(a, a.text(RX + 20, 520, "potencia: alta", 15, a.BAD, a.MONO, 600), 0)
vis(a, a.text(RX + 20, 520, "2.4 Low · 5 Medium", 15, a.INK, a.MONO, 600), 1, 3)
vis(a, a.text(RX + 20, 548, "+ AP 3 en Low", 15, a.OK, a.MONO, 600), 3)

status(a, 632, [
    (0, 25, "Si el lejano siempre parece aceptable, el celular no busca otro AP.", a.BAD, 0),
    (25, 50, "Celdas que se tocan en el borde: el traspaso pasa donde corresponde.", a.OK, 0),
    (50, 75, "Un punto por debajo de -70 dBm es candidato a un AP más.", a.AMB, 0),
    (75, 100, "Más AP con menos potencia, en vez de subirle a todos.", a.OK, 1),
])

write(a, 8, "r1", "Celdas más chicas con potencia baja",
      "Animación en cuatro tiempos sobre la planta de un local con el AP 1 y el AP 2, los puntos A, B y C de la caminata y un rincón D; a la derecha, lecturas de ejemplo en WiFiman. "
      "1: con potencia alta las dos celdas son enormes y se pisan; en el punto C el celular sigue en el AP 1 con -72 dBm, peor que el mínimo de -70. "
      "2: con 2.4 GHz en Low y 5 GHz en Medium las celdas son más chicas y se solapan en B, la zona de traspaso; en C el celular pasa al AP 2 con -60 dBm. "
      "3: queda el rincón D por debajo de -70 dBm, con -76. "
      "4: subirle la potencia a todos volvería al primer caso; un AP 3 con potencia baja cubre D con -62 dBm. "
      "La lección trata -70 dBm como mínimo y busca -65 o mejor.",
      [12, 40, 64, 90])
