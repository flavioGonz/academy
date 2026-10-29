#!/usr/bin/env python3
"""Lección 13 · teoría: la máscara /29 define el vecindario y la ruta por defecto lleva todo lo demás al gateway."""
from _anim_mikrotik_1_13 import *

a = Anim(T=28, kicker="MIKROTIK · CÓMO FUNCIONA", title="La máscara arma el vecindario; la default, el resto")
a.steps([
    "203.0.113.10/29: 29 bits de red. Quedan 3 bits: 8 direcciones.",
    "De .8 a .15: .8 es la red, .15 el broadcast, de .9 a .14 se usan.",
    "El gateway .9 está en el vecindario: el router lo alcanza directo.",
    "Para 1.1.1.1 no hay ruta más específica: 0.0.0.0/0 lo manda al .9.",
    "Sin la ruta por defecto, llega al vecino pero no a internet.",
], still=3)

# bits del último octeto
a.add(a.text(48, 222, "203.0.113.", 24, a.INK, a.MONO, 600))
BX = 208
for i, b in enumerate("00001010"):
    x = BX + i * 50
    net = i < 5
    a.add(a.box(x, 190, 44, 46, "#E3EEF9" if net else a.AMBBG, a.BLUE if net else a.AMB, rx=8, sw=2))
    a.add(a.text(x + 22, 222, b, 22, a.BLUE if net else a.AMB, a.MONO, 600, "middle"))
a.add(a.text(BX + 120, 260, "5 bits de red: 24 + 5 = /29", 14, a.BLUE, a.MONO, 600, "middle"))
a.add(a.text(BX + 322, 260, "3 bits: 8", 14, a.AMB, a.MONO, 600, "middle"))
a.add(a.text(620, 222, "= .10", 22, a.INK, a.MONO, 600))
a.add(during(a, a.box(BX - 6, 184, 254, 58, "none", a.BLUE, rx=12, sw=2.5) + a.box(BX + 244, 184, 156, 58, "none", a.AMB, rx=12, sw=2.5), 1, 20))

# vecindario
CELLS = [(".8", "red", a.GREY), (".9", "gateway", a.OK), (".10", "MikroTik", a.BLUE), (".11", "libre", a.TXT),
         (".12", "libre", a.TXT), (".13", "libre", a.TXT), (".14", "libre", a.TXT), (".15", "broadcast", a.GREY)]
CY, CW = 290, 132
for i, (n, lab, col) in enumerate(CELLS):
    x = 48 + i * 138
    a.add(a.box(x, CY, CW, 70, a.WHITE, a.LINE, rx=10))
    a.add(a.text(x + 16, CY + 32, n, 20, a.INK, a.MONO, 600))
    a.add(a.group(a.text(x + 16, CY + 56, lab, 14, col, a.MONO, 600), a.show(21, 100), still=1))
a.add(during(a, a.box(44, CY - 4, 1112, 78, "none", a.AMB, rx=14, sw=2.5) + a.text(1152, CY - 12, "vecindario 203.0.113.8/29", 14, a.AMB, a.MONO, 600, "end"), 21, 40))
a.add(during(a, a.box(48 + 138 - 4, CY - 4, CW + 8, 78, "none", a.OK, rx=12, sw=3) + a.box(48 + 276 - 4, CY - 4, CW + 8, 78, "none", a.BLUE, rx=12, sw=3), 41, 60))
a.add(during(a, f'<path d="M{48 + 276 + 30} {CY + 74} q -40 34 -80 0" fill="none" stroke="{a.OK}" stroke-width="3" marker-end="url(#{a._marker(a.OK)})"/>'
              + a.text(48 + 207 + 34, CY + 112, "directo por ether1", 14, a.OK, a.MONO, 600, "middle"), 43, 60))

# rutas y decisión
TX, TY = 48, 432
a.add(a.box(TX, TY, 620, 170, a.INK))
a.add(a.text(TX + 20, TY + 30, "/ip/route", 14, SKY, a.MONO))
a.add(a.text(TX + 20, TY + 68, "203.0.113.8/29", 16, a.WHITE, a.MONO, 600))
a.add(a.text(TX + 250, TY + 68, "ether1 · conectada", 15, SKY, a.MONO))
dflt = a.text(TX + 20, TY + 106, "0.0.0.0/0", 16, a.WHITE, a.MONO, 600) + a.text(TX + 250, TY + 106, "gateway=203.0.113.9", 15, SKY, a.MONO)
a.add(a.group(dflt, a.show(0, 79), still=1))
a.add(during(a, a.text(TX + 20, TY + 106, "0.0.0.0/0", 16, "#6E88A1", a.MONO, 600) + a.text(TX + 250, TY + 106, "no está", 15, "#FF9B85", a.MONO, 600)
              + line(TX + 18, TY + 101, TX + 112, TY + 101, "#FF9B85", 2), 80, 98.5))
a.add(during(a, a.box(TX + 10, TY + 44, 600, 36, "none", MINT, rx=8, sw=2.5), 41, 60))
a.add(during(a, a.box(TX + 10, TY + 82, 600, 36, "none", GOLD, rx=8, sw=2.5), 61, 79, still=1))
a.add(a.text(TX + 20, TY + 148, "coincide con todo: es el plan B de cada paquete", 13, SKY, a.MONO))

PX, PW = 700, 452
a.add(a.box(PX, TY, PW, 170, a.WHITE, a.LINE))
a.add(a.text(PX + 20, TY + 30, "paquete del router a…", 14, a.GREY, a.MONO))
for t0, t1, l1, l2, col, st in [
        (41, 60, "203.0.113.9", "vecino: sale directo por ether1", a.OK, 0),
        (61, 79, "1.1.1.1", "fuera del /29: va al gateway .9", a.OK, 1),
        (80, 100, "1.1.1.1", "sin ruta: no sale", a.BAD, 0)]:
    a.add(during(a, a.text(PX + 20, TY + 76, l1, 24, a.INK, a.MONO, 600) + a.text(PX + 20, TY + 112, l2, 16, col, a.SANS, 600), t0, t1, still=st))
a.add(during(a, check(a, PX + PW - 34, TY + 68), 41, 79, still=1))
a.add(during(a, xmark(a, PX + PW - 34, TY + 68), 80, 98.5))

a.add(a.text(48, 642, "Por eso se verifica en orden: vecino (gateway), mundo (1.1.1.1) y nombres (:resolve).", 16, a.TXT, a.SANS, 600))

p, pre = out(13, 1)
a.write(p, title="Máscara /29 y ruta por defecto",
        desc="Animación en cinco tiempos. 1: en 203.0.113.10/29 el último octeto es 00001010; los primeros 5 bits completan los 29 de red y quedan 3 bits, o sea 8 "
             "direcciones. 2: el vecindario va de 203.0.113.8 a 203.0.113.15: .8 es la red, .15 el broadcast y de .9 a .14 son usables (.9 gateway, .10 el MikroTik). "
             "3: el gateway .9 está en el mismo vecindario, por la ruta conectada 203.0.113.8/29, y el router lo alcanza directo por ether1. 4: para 1.1.1.1 no hay ruta más "
             "específica y la 0.0.0.0/0 lo manda al gateway 203.0.113.9. 5: sin la ruta por defecto, el router llega al vecino pero no a internet.",
        preview=[10, 30, 50, 70, 90], prefix=pre)
