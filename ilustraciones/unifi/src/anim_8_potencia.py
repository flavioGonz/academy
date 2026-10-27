#!/usr/bin/env python3
"""Lección 8 · teoría: asimetría de potencia AP / celular, reintentos y tiempo de aire."""
import math
from _anim_unifi import *  # noqa

a = new(24, "Potencia", "El AP habla fuerte; el celular le contesta bajito", [
    "AP 1 a potencia alta: el celular lo escucha bien de lejos y se queda.",
    "El celular transmite con menos potencia: al AP 1 le llega débil y reintenta.",
    "La velocidad baja: la misma trama ocupa más aire y los demás esperan.",
    "Con potencia más baja, el celular se pasa al AP 2: tramas cortas, aire libre.",
], still=3)

Y = 300
A1, PH, A2 = 150, 700, 1060


def wave(cx, radii, facing, color, t0, t1, step=1.2, width=3.5, still=0):
    for i, r in enumerate(radii):
        sp = min(40, math.degrees(math.asin(min(1, 80 / r))))
        at(a, "".join(arcs(a, cx, Y, [r], color, facing, sp, width)), t0 + i * step, t1, still=still)


# ondas (debajo de las cajas)
s0, s1 = ph(a, 0)
wave(A1 + 60, [110, 220, 330, 440, 520], 0, A.BLUE, s0 + 1, s1 - 1)
s0, s1 = ph(a, 1)
for i, r in enumerate([30, 65, 100]):
    at(a, "".join(arcs(a, PH - 65, Y, [r], A.BAD, 180, 40, 3)), s0 + 2 + i * 1.5, s1 - 1)
s0, s1 = ph(a, 3)
wave(A1 + 60, [120, 220], 0, A.BLUE, s0 + 1, 100, still=1)
wave(A2 - 95, [40, 80], 180, A.OK, s0 + 3, 100, still=1)
wave(PH + 65, [40, 80], 0, A.OK, s0 + 5, 100, still=1)

# equipos
a.add(a.box(A1 - 90, Y - 50, 180, 100, A.WHITE, A.LINE, rx=14) + ap_icon(a, A1 - 46, Y - 6, 22) + a.text(A1 - 12, Y, "AP 1", 20, A.INK, A.HEAD, 600))
vis(a, a.text(A1 - 70, Y + 34, "potencia alta", 14, A.BAD, A.MONO, 600), 0, 2)
vis(a, a.text(A1 - 70, Y + 34, "potencia baja", 14, A.OK, A.MONO, 600), 3)
a.add(a.box(PH - 60, Y - 50, 120, 100, A.WHITE, A.LINE, rx=14) + phone_icon(a, PH, Y - 8) + a.text(PH, Y + 36, "celular", 14, A.GREY, A.MONO, anchor="middle"))
vis(a, a.box(A2 - 90, Y - 50, 180, 100, A.WHITE, A.LINE, rx=14, extra='opacity=".45"') + a.text(A2, Y + 6, "AP 2", 20, A.GREY, A.HEAD, 600, "middle"), 0, 2)
vis(a, a.box(A2 - 90, Y - 50, 180, 100, A.WHITE, A.OK, rx=14, sw=2.5) + ap_icon(a, A2 - 46, Y - 6, 22) + a.text(A2 - 12, Y, "AP 2", 20, A.INK, A.HEAD, 600)
    + a.text(A2 - 70, Y + 34, "cerca", 14, A.OK, A.MONO, 600), 3)

# asociación
vis(a, line(a, [(A1 + 90, Y - 100), (PH - 60, Y - 100)], A.AMB, 2.5, "7 6") + a.text((A1 + PH) / 2, Y - 110, "asociado a AP 1", 15, A.AMB, A.MONO, 600, "middle"), 0, 2)
vis(a, line(a, [(PH + 60, Y - 100), (A2 - 90, Y - 100)], A.OK, 2.5, "7 6") + a.text((PH + A2) / 2, Y - 110, "asociado a AP 2", 15, A.OK, A.MONO, 600, "middle"), 3)

vis(a, pill(a, PH, Y + 92, "se ve aceptable: no busca otro", "amb", anchor="middle"), 0)
s0, s1 = ph(a, 1)
token(a, [(PH - 100, Y + 2), (A1 + 300, Y + 2)], s0 + 4, s0 + 12, "trama", bg=A.CYAN, hold=s0 + 12.5)
at(a, pill(a, A1 + 120, Y + 92, "llega débil", "bad"), s0 + 12, s1 - 1)
at(a, pill(a, PH, Y + 92, "reintento", "bad", anchor="middle"), s0 + 14, s0 + 18)
at(a, pill(a, PH, Y + 92, "reintento otra vez", "bad", anchor="middle"), s0 + 18, s1 - 1)

# aire del canal
TX0, TX1, TY = 160, 1140, 470
a.add(a.text(TX0, TY - 14, "AIRE DEL CANAL", 14, A.GREY, A.MONO, extra='letter-spacing="1.5"'))
a.add(a.box(TX0, TY, TX1 - TX0, 54, A.WHITE, A.LINE, rx=6, sw=1.5))


def block(t0, t1, w0, w1, col, lab, hide, still=0):
    k = (TX1 - TX0) / (w1 - w0)
    x = TX0 + (t0 - w0) * k
    w = (t1 - t0) * k - 3
    inner = a.box(x, TY + 3, w, 48, col, rx=5) + (a.text(x + w / 2, TY + 32, lab, 15, A.WHITE, A.MONO, 600, "middle") if lab else "")
    sc = a.keyframes([(0, 0), (t0, 0), (t1, 1), (100, 1)], "transform", "scaleX({})")
    a.add(a.group(inner, sc, a.show(t0, hide, 0.3), still=still, origin=f"{x}px {TY}px"))


s0, s1 = ph(a, 2)
block(s0 + 1, s0 + 13, s0, s1, A.AMB, "celular lejano, lento", s1 - 0.5)
block(s0 + 13.3, s0 + 20, s0, s1, A.BAD, "reintento", s1 - 0.5)
block(s0 + 20.3, s0 + 24, s0, s1, A.BLUE, "otros", s1 - 0.5)
vis(a, note(a, 48, 560, 1104, "Un cliente lento ocupa el canal más tiempo para mandar lo mismo: todos los del AP lo pagan.", "amb"), 2)
s0, s1 = ph(a, 3)
for i, t in enumerate(range(1, 24, 3)):
    block(s0 + t, s0 + t + 2.6, s0, s1, A.OK if i % 2 == 0 else A.BLUE, "cel" if i % 2 == 0 else "otro", 100, still=1)
vis(a, note(a, 48, 560, 1104, "Si un punto queda débil, la respuesta es un AP más, no subirle a todos.", "ok"), 3)

write(a, "8-t1.svg", "Potencia alta, reintentos y tiempo de aire", mid_pcts(a))
