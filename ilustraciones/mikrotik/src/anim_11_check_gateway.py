#!/usr/bin/env python3
"""Lección 11 · teoría: ruta recursiva al testigo, check-gateway=ping cada 10 s y conmutación tras dos fallas."""
from _anim_mikrotik_1_13 import *

a = Anim(T=28, kicker="MIKROTIK · CÓMO FUNCIONA", title="check-gateway mira hasta el testigo, no solo el módem")
a.steps([
    "La default apunta a 1.1.1.1. Para llegar, sirve la /32 con scope=10 (≤ 11).",
    "Cada 10 s el router hace ping al testigo, y el ping recorre todo el camino.",
    "Se corta internet detrás del módem: el módem vive, pero el ping no vuelve.",
    "Tras dos fallas la ruta queda inactiva y gana la de distancia 2: el ISP2.",
], still=3)

Y = 246
a.add(line(248, Y, 900, Y, a.LINE, 3))
# pings (antes que las cajas: se esconden al pasar por ellas)
OUT = [(250, Y - 14), (898, Y - 14)]
BACK = [(898, Y + 14), (250, Y + 14)]


def dot(col):
    return f'<circle cx="0" cy="0" r="9" fill="{col}"/>'


for t0 in (27, 39):
    a.add(travel(a, dot(a.BLUE), OUT, t0, t0 + 4, hold=0.2))
    a.add(travel(a, dot(a.OK), BACK, t0 + 4.4, t0 + 8.4, hold=0.2))
for t0 in (52, 62):
    a.add(travel(a, dot(a.BLUE), [(250, Y - 14), (600, Y - 14)], t0, t0 + 2.5, hold=1))
a.add(still_only(a, place(a, dot(a.BLUE), 290, Y - 14)))

a.add(device(a, 48, 196, 200, 100, "Router", "ether1", sub2="203.0.113.10", dark=True, ssize=13))
a.add(device(a, 330, 196, 200, 100, "Módem fibra", "gateway", sub2="203.0.113.9", ssize=13))
a.add(device(a, 612, 196, 200, 100, "Internet", "del ISP1", ssize=13))
a.add(device(a, 900, 196, 252, 100, "Testigo ISP1", "1.1.1.1", ssize=14))
a.add(during(a, xmark(a, 571, Y), 50, 100, still=1))
a.add(during(a, a.text(571, Y - 28, "corte", 13, a.BAD, a.MONO, 600, "middle"), 50, 100, still=1))
a.add(during(a, check(a, 504, 222, 12), 50, 100, still=1))

# contador
a.add(a.text(48, 330, "check-gateway=ping · cada 10 s · espera 1 s", 15, a.TXT, a.MONO))
for t0, t1, txt, col, st in [(27, 50, "respuestas: ok", a.OK, 0), (55, 65, "fallas: 1", a.AMB, 0), (65, 100, "fallas: 2", a.BAD, 1)]:
    a.add(during(a, a.text(1152, 330, txt, 15, col, a.MONO, 600, "end"), t0, t1, still=st))

# tabla de rutas
TX, TY, TW = 48, 352, 1104
a.add(a.box(TX, TY, TW, 230, a.INK))
a.add(a.text(TX + 20, TY + 30, "/ip/route", 14, SKY, a.MONO))
ROWS = [("1.1.1.1/32", "gateway=203.0.113.9 scope=10", "ruta al testigo"),
        ("0.0.0.0/0", "gateway=1.1.1.1 target-scope=11 distance=1", "por ISP1"),
        ("0.0.0.0/0", "gateway=8.8.8.8 target-scope=11 distance=2", "por ISP2")]
ry = []
for i, (d, g, n) in enumerate(ROWS):
    y = TY + 46 + i * 58
    ry.append(y)
    a.add(a.box(TX + 14, y, TW - 28, 48, "#0B3A66", rx=8))
    a.add(a.text(TX + 30, y + 30, d, 15, a.WHITE, a.MONO, 600))
    a.add(a.text(TX + 180, y + 30, g, 15, SKY, a.MONO))
    a.add(a.text(TX + 650, y + 30, n, 13, SKY, a.MONO))
END = TX + TW - 30


def st(i, t0, t1, lab, fg, bg, s=0):
    a.add(during(a, a.pill(END, ry[i] + 10, lab, fg, bg, 13, 28, "end"), t0, t1, still=s))


st(0, 0, 100, "activa", a.OK, a.OKBG, 1)
st(1, 0, 68, "activa", a.OK, a.OKBG)
st(1, 68, 100, "inactiva", a.BAD, a.BADBG, 1)
st(2, 0, 68, "en espera", a.GREY, "#E6EDF4")
st(2, 68, 100, "activa", a.OK, a.OKBG, 1)
# resolución recursiva (tiempo 1)
a.add(during(a, f'<path d="M{TX + 22} {ry[1] + 24} H{TX + 6} V{ry[0] + 24} H{TX + 12}" fill="none" stroke="{GOLD}" stroke-width="3" marker-end="url(#{a._marker(GOLD)})"/>'
              + a.box(TX + 180 + 16 * 9 - 5, ry[1] + 8, 15 * 9 + 10, 32, "none", GOLD, rx=6, sw=2) + a.box(TX + 180 + 20 * 9 - 5, ry[0] + 8, 8 * 9 + 10, 32, "none", GOLD, rx=6, sw=2), 2, 25))
a.add(during(a, a.text(1152, 330, "scope 10 ≤ target-scope 11: la /32 sirve", 15, a.AMB, a.MONO, 600, "end"), 4, 25))
a.add(during(a, a.box(TX + 10, ry[1] - 4, TW - 20, 56, "none", a.BAD, rx=10, sw=3), 68, 85))
a.add(during(a, a.box(TX + 10, ry[2] - 4, TW - 20, 56, "none", MINT, rx=10, sw=3), 70, 100, still=1))

a.add(a.text(48, 626, "Con el gateway directo, el ping llega al módem: con el módem vivo e internet caída, no conmutaría.", 16, a.TXT, a.SANS, 600))

p, pre = out(11, 1)
a.write(p, title="check-gateway con ruta recursiva",
        desc="Animación en cuatro tiempos. Arriba, el camino Router (ether1 203.0.113.10), módem de fibra (gateway 203.0.113.9), internet del ISP1 y el testigo 1.1.1.1. "
             "Abajo, la tabla de rutas: 1.1.1.1/32 por 203.0.113.9 con scope=10; 0.0.0.0/0 por 1.1.1.1 con target-scope=11 y distance=1; 0.0.0.0/0 por 8.8.8.8 con distance=2. "
             "1: para llegar a 1.1.1.1, la default busca rutas con scope menor o igual a 11 y le sirve la /32. 2: cada 10 segundos check-gateway hace ping al testigo y el ping "
             "recorre todo el camino. 3: se corta internet detrás del módem; el módem sigue vivo pero el ping no vuelve: una falla, dos fallas. 4: tras dos fallas la default del "
             "ISP1 queda inactiva y la de distancia 2, por el ISP2, pasa a activa.",
        preview=[12, 36, 62, 88], prefix=pre)
