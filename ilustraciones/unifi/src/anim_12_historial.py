#!/usr/bin/env python3
"""Lección 12 · teoría: cruzar el historial del cliente con el Time Machine de la radio y del puerto."""
from _anim_unifi import *  # noqa

a = new(22, "Mirar primero", "Misma hora, tres historiales: qué cambió", [
    "Historial del cliente: una desconexión y reconexión, no un roam.",
    "Time Machine de la radio: a esa misma hora, un cambio de canal.",
    "Time Machine del puerto: el uplink no se cayó. Se descarta.",
    "Se escribe en tres líneas y se prueba un solo cambio.",
], still=3)

TX0, TX1 = 330, 1150
LANES = [(186, "Cliente", "historial de conexión"), (276, "Radio del AP 2", "Time Machine"), (366, "Puerto del uplink", "Time Machine")]
for y, t, s in LANES:
    a.add(node(a, 48, y, 262, 70, t, s, ssize=14, tsize=18))
    a.add(a.box(TX0, y + 10, TX1 - TX0, 50, A.WHITE, A.LINE, rx=8, sw=1.5))
# eje
for k, lab in enumerate(["−3 h", "−2 h", "−1 h", "ahora"]):
    x = TX0 + k * (TX1 - TX0) / 3
    a.add(f'<line x1="{x}" y1="446" x2="{x}" y2="454" stroke="{A.GREY}" stroke-width="2"/>' + a.text(x, 474, lab, 14, A.GREY, A.MONO, anchor="middle" if 0 < k < 3 else ("start" if k == 0 else "end")))
a.add(line(a, [(TX0, 450), (TX1, 450)], A.GREY, 2))

GX0, GX1 = 720, 800
CX = (GX0 + GX1) / 2
# cursor que baja carril por carril
for i, yb in enumerate([252, 342, 432]):
    s0, s1 = ph(a, i)
    at(a, f'<line x1="{CX}" y1="{180}" x2="{CX}" y2="{yb}" stroke="{A.INK}" stroke-width="2" stroke-dasharray="5 5"/>', s0 + 2, s1 if i < 2 else 100, still=1 if i == 2 else 0)
at(a, f'<line x1="{CX}" y1="180" x2="{CX}" y2="432" stroke="{A.INK}" stroke-width="2" stroke-dasharray="5 5"/>', ph(a, 3)[0], 100, still=1)

# carril 1: cliente (siempre)
y = 196
a.add(a.box(TX0 + 4, y + 4, GX0 - TX0 - 6, 42, "#E4EFFA", rx=6) + a.text((TX0 + GX0) / 2, y + 31, "en AP 2", 15, A.BLUE, A.MONO, 600, "middle"))
a.add(a.box(GX1 + 2, y + 4, TX1 - GX1 - 6, 42, "#E4EFFA", rx=6) + a.text((GX1 + TX1) / 2, y + 31, "en AP 2", 15, A.BLUE, A.MONO, 600, "middle"))
a.add(a.box(GX0 + 2, y + 4, GX1 - GX0 - 4, 42, A.BADBG, A.BAD, rx=6, sw=1.5, extra='stroke-dasharray="5 4"') + a.text(CX, y + 31, "sin red", 14, A.BAD, A.MONO, 600, "middle"))
vis(a, a.box(GX0 - 4, y - 2, GX1 - GX0 + 8, 54, "none", A.BAD, rx=8, sw=3), 0)
vis(a, pill(a, GX1 + 14, y + 11, "desconexión y reconexión", "bad"), 0)

# carril 2: radio
y = 286
s0, s1 = ph(a, 1)
at(a, f'<path d="M{CX} {y + 12} L{CX + 13} {y + 25} L{CX} {y + 38} L{CX - 13} {y + 25} z" fill="{A.AMB}"/>'
   + pill(a, CX + 24, y + 11, "cambio de canal", "amb"), s0 + 3, 100, still=1)
at(a, a.text(TX0 + 20, y + 40, "cambios y eventos de las últimas 24 h", 14, A.GREY, A.MONO), s0 + 1, 100, still=1)

# carril 3: puerto
y = 376
s0, s1 = ph(a, 2)
at(a, a.box(TX0 + 4, y + 4, TX1 - TX0 - 8, 42, A.OKBG, rx=6) + a.text(TX0 + 24, y + 31, "uplink arriba todo el tiempo", 15, A.OK, A.MONO, 600), s0 + 3, 100, still=1)
at(a, pill(a, TX1 - 16, y + 11, "descartado", "grey", anchor="end"), s0 + 8, 100, still=1)

# 4: tres líneas
s0, s1 = ph(a, 3)
card = a.box(48, 500, 1104, 150, A.WHITE, A.LINE, rx=14) + f'<rect x="48" y="500" width="6" height="150" rx="3" fill="{A.BLUE}"/>'
card += a.text(76, 534, "En tres líneas", 18, A.INK, A.HEAD, 600)
for k, t in enumerate(["1. Qué pasó: el cliente se cayó a la hora del cambio de canal de la radio.",
                       "2. Qué se descarta: el uplink estuvo arriba todo el tiempo.",
                       "3. Un solo cambio, en esa radio; se prueba, y si empeora se vuelve atrás."]):
    card += a.text(76, 566 + k * 26, t, 16, A.TXT, A.SANS)
vis(a, card, 3)
vis(a, a.text(48, 530, "Ejemplo de lectura. Para la señal: -65 dBm o mejor, -70 dBm como mínimo (WunderTech).", 16, A.TXT, A.SANS, 600), 0, 2)

write(a, "12-t1.svg", "Cruzar historial del cliente y Time Machine", mid_pcts(a))
