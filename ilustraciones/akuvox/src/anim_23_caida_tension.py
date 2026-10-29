#!/usr/bin/env python3
"""Lección 23 · teoría: con alimentación justa, la tensión cae cuando la cerradura pide corriente; se mide con carga."""
from _anim_akuvox_15_28 import *

a = new(20, "AKUVOX", "Medí con la cerradura conectada, durante la apertura")
a.steps([
    "En reposo no circula corriente: el tester marca 12 V y cualquier fuente parece buena.",
    "Al abrir, la cerradura pide corriente, que sale de la alimentación del portero.",
    "Si esa alimentación es justa, la tensión cae: X910 con PoE af, la salida no alcanza.",
    "Con PoE+ o fuente de 12 V 2 A, la tensión se sostiene durante la apertura.",
], still=2)

# ---- circuito
a.add(a.box(48, 176, 560, 452, a.WHITE, a.LINE, rx=18))
a.add(I.Generic(72, 200, "X910", "12 V por el relé", icon="bell", w=230).svg())
# alimentación
a.add(a.text(340, 222, "Alimentación del portero", 15, a.GREY, a.SANS, 600))
a.add(at(a, a.pill(340, 232, "PoE af", a.AMB, a.AMBBG, 16, h=32), 0, 75, still=1))
a.add(at(a, a.pill(340, 232, "PoE+ o 12 V 2 A", a.OK, a.OKBG, 16, h=32), 75, 100, still=0))
a.add(f'<path d="M336 248 H302" stroke="{a.BLUE}" stroke-width="4"/>')
# cables a la cerradura
a.add(f'<path d="M150 284 V470 H300" fill="none" stroke="{a.BAD}" stroke-width="4"/>')
a.add(f'<path d="M210 284 V520 H300" fill="none" stroke="#2B2B2B" stroke-width="4"/>')
flow = a.keyframes([(0, 0), (100, -600)], "stroke-dashoffset")
a.add(a.group(f'<path d="M150 284 V470 H300" fill="none" stroke="#FFD28A" stroke-width="4" stroke-dasharray="10 14"/>', flow, a.show(27, 72), still=1))
a.add(a.group(f'<path d="M150 284 V470 H300" fill="none" stroke="#FFD28A" stroke-width="4" stroke-dasharray="10 14"/>', flow, a.show(78, 97), still=0))
a.add(a.text(96, 404, "+", 22, a.BAD, a.MONO, 600) + a.text(222, 404, "−", 22, a.INK, a.MONO, 600))
a.add(I.Lock(300, 452, "Cerradura", "carga real", w=200).svg())
# tester en paralelo
TX, TY = 400, 300
a.add(f'<path d="M262 470 V420 H{TX + 40} V{TY + 96}" fill="none" stroke="{a.BAD}" stroke-width="2.5" stroke-dasharray="5 4"/>')
a.add(f'<path d="M262 520 V540 H560 V{TY + 40} H{TX + 160}" fill="none" stroke="#2B2B2B" stroke-width="2.5" stroke-dasharray="5 4"/>')
a.add(a.box(TX, TY, 160, 96, "#F4C430", a.INK, rx=14, sw=2))
a.add(a.box(TX + 14, TY + 14, 132, 46, "#E8F0D8", a.INK, rx=6, sw=1.5))
a.add(a.text(TX + 80, TY + 84, "tester", 15, a.INK, a.MONO, 600, "middle"))
a.add(at(a, a.text(TX + 80, TY + 46, "12 V", 26, a.INK, a.MONO, 600, "middle"), 0, 52, still=0))
a.add(at(a, a.text(TX + 80, TY + 46, "cae", 26, a.BAD, a.MONO, 600, "middle"), 52, 75, still=1))
a.add(at(a, a.text(TX + 80, TY + 46, "12 V", 26, a.OK, a.MONO, 600, "middle"), 75, 100, still=0))
a.add(at(a, a.text(320, 600, "sin corriente: no prueba nada", 16, a.TXT, a.SANS, 600), 0, 25, still=0))
a.add(at(a, a.text(320, 600, "circula corriente", 16, "#B26A00", a.SANS, 600), 27, 100, still=1))

# ---- gráfico
GX, GY, GW, GH = 640, 176, 512, 452
a.add(a.box(GX, GY, GW, GH, a.WHITE, a.LINE, rx=18))
a.add(a.text(GX + 22, GY + 36, "Tensión en la cerradura", 17, a.INK, a.SANS, 600))
AX0, AX1, AY0, AY1 = GX + 60, GX + GW - 30, GY + 90, GY + GH - 70
a.add(f'<path d="M{AX0} {AY0 - 10} V{AY1} H{AX1}" fill="none" stroke="{a.GREY}" stroke-width="2"/>')
a.add(a.text(AX1, AY1 + 30, "tiempo", 15, a.GREY, a.MONO, 400, "end"))
L12 = AY0 + 50
a.add(a.text(AX0 - 10, L12 + 5, "12 V", 15, a.INK, a.MONO, 600, "end"))
a.add(f'<path d="M{AX0} {L12} H{AX1}" stroke="{a.LINE}" stroke-width="2" stroke-dasharray="4 5"/>')
XA, XB = AX0 + 130, AX0 + 330
a.add(a.box(XA, AY0 - 10, XB - XA, AY1 - AY0 + 10, I.SOFT, rx=0))
a.add(a.text((XA + XB) / 2, AY1 - 14, "apertura", 15, a.BLUE, a.MONO, 600, "middle"))
# curvas
sag = f"M{AX0} {L12} H{XA} L{XA + 20} {L12 + 120} H{XB - 10} L{XB + 10} {L12} H{AX1}"
ok = f"M{AX0} {L12} H{XA} L{XA + 20} {L12 + 10} H{XB - 10} L{XB + 10} {L12} H{AX1}"
draw = lambda t0, t1: a.keyframes([(0, 900), (t0, 900), (t1, 0), (100, 0)], "stroke-dashoffset")
a.add(a.group(f'<path d="{sag}" fill="none" stroke="{a.BAD}" stroke-width="4" stroke-dasharray="900"/>', draw(27, 70), a.show(27, 75), still=1))
a.add(at(a, a.text(XA + 30, L12 + 150, "alimentación justa: cae", 16, a.BAD, a.SANS, 600), 50, 75, still=1))
a.add(a.group(f'<path d="{ok}" fill="none" stroke="{a.OK}" stroke-width="4" stroke-dasharray="900"/>', draw(76, 96), a.show(76, 100), still=0))
a.add(at(a, a.text(XA + 30, L12 + 46, "se sostiene", 16, a.OK, a.SANS, 600), 88, 100, still=0))
a.add(a.text(GX + 22, GY + GH - 22, "esquema: la caída real depende de la cerradura y la fuente", 15, a.GREY, a.SANS, 500))

a.write(*out(23)[:1], title="Caída de tensión con la cerradura conectada",
        desc=("Animación en cuatro tiempos. A la izquierda, un X910 que da 12 V por el relé a una cerradura, con un tester en paralelo; a la derecha, la tensión en la cerradura en el tiempo. "
              "1: en reposo no circula corriente y el tester marca 12 V: en vacío cualquier fuente parece buena. "
              "2: al abrir, la cerradura pide corriente, que sale de la alimentación del portero. "
              "3: si la alimentación es justa, como un X910 con PoE af, la tensión cae durante la apertura y la salida no alcanza. "
              "4: con PoE+ o fuente de 12 V 2 A la tensión se sostiene durante la apertura. El gráfico es un esquema sin valores de caída."),
        preview=[12, 40, 66, 94], prefix=out(23)[1])
