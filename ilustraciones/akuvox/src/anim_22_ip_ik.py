#!/usr/bin/env python3
"""Lección 22 · teoría: cómo se leen los códigos IP (IEC 60529) e IK (IEC 62262)."""
from _anim_akuvox_15_28 import *

a = new(24, "AKUVOX", "IP65, IP66, IK06, IK10: qué dice cada número")
a.steps([
    "IP, primer dígito: sólidos. 6 es hermético al polvo, en IP65 y en IP66.",
    "Segundo dígito: agua. 5 resiste chorros de agua.",
    "6 resiste chorros potentes. De IP65 a IP66 cambia la fuerza del agua.",
    "IK mide impacto, de 00 a 10: IK06 es 1 joule; IK10, 20 joules.",
], still=3)

# ---------- IP
a.add(a.box(48, 176, 540, 456, a.WHITE, a.LINE, rx=18))
a.add(a.text(70, 210, "Código IP", 22, a.INK, a.HEAD, 600) + a.text(186, 210, "IEC 60529", 15, a.GREY, a.MONO))
a.add(a.text(70, 300, "IP", 56, a.INK, a.HEAD, 600))
for x in (160, 244):
    a.add(a.box(x, 238, 72, 82, a.SLATE, I.LINE2, rx=12))
a.add(a.text(196, 300, "6", 56, a.INK, a.MONO, 600, "middle"))
a.add(at(a, a.text(280, 300, "5", 56, a.INK, a.MONO, 600, "middle"), 0, 52, still=0))
a.add(at(a, a.text(280, 300, "6", 56, a.BLUE, a.MONO, 600, "middle"), 52, 100, still=1))
a.add(a.text(196, 344, "sólidos", 15, a.GREY, a.MONO, 600, "middle") + a.text(280, 344, "agua", 15, a.GREY, a.MONO, 600, "middle"))
a.add(at(a, a.box(156, 234, 80, 90, "none", a.CYAN, rx=14, sw=3), 1, 25, still=0))
a.add(at(a, a.box(240, 234, 80, 90, "none", a.CYAN, rx=14, sw=3), 26, 75, still=0))
# explicaciones
EXP = [("6", "hermético al polvo", 1, 25), ("5", "resiste chorros de agua", 26, 50), ("6", "resiste chorros potentes", 51, 75)]
for i, (d, t, t0, t1) in enumerate(EXP):
    y = 252 + i * 34
    a.add(at(a, a.box(342, y - 22, 236, 30, I.SOFT, a.CYAN, rx=8, sw=1.5), t0, t1, still=0))
    a.add(a.text(352, y, d, 17, a.INK, a.MONO, 600) + a.text(374, y, "· " + t, 16, a.TXT, a.SANS, 500))

# gabinete con polvo y agua
GX, GY, GW, GH = 230, 430, 150, 150
a.add(a.box(GX, GY, GW, GH, "#26323F", a.INK, rx=16))
a.add(f'<circle cx="{GX + 75}" cy="{GY + 34}" r="11" fill="#0B1A28" stroke="#5B6F84" stroke-width="2"/>')
a.add(a.box(GX + 30, GY + 62, 90, 50, "#3A4A5C", rx=8))
a.add(a.text(GX + 75, GY + GH + 32, "frente del portero", 15, a.GREY, a.SANS, 500, "middle"))
# polvo (paso 1)
import random
random.seed(4)
for i in range(14):
    y = GY + 10 + random.random() * (GH - 20)
    x0 = 70 + random.random() * 60
    t = 2 + random.random() * 8
    dot = f'<circle cx="0" cy="0" r="{3 + random.random() * 2:.1f}" fill="{a.AMB}"/>'
    a.add(a.group(dot, a.move([(0, x0, y), (t, x0, y), (t + 9, GX - 8, y), (100, GX - 8, y)]), a.show(t, 25, 1), still=0))
a.add(at(a, a.text(80, GY - 14, "polvo: no entra", 15, a.AMB, a.SANS, 600), 3, 25, still=0))
# agua (pasos 2 y 3)
a.add(a.box(500, GY + 50, 60, 40, I.LINE2, rx=8) + a.text(530, GY + 120, "chorro", 15, a.GREY, a.MONO, 600, "middle"))
for k, (t0, t1, w, n, lab) in enumerate(((27, 50, 3, 4, "chorros de agua"), (52, 75, 7, 6, "chorros potentes"))):
    flow = a.keyframes([(0, 0), (100, 240 if k == 0 else 480)], "stroke-dashoffset")
    for j in range(n):
        y = GY + 56 + (j - (n - 1) / 2) * (8 if k == 0 else 7) + 14
        a.add(a.group(f'<path d="M496 {y:.0f} H{GX + GW + 6}" stroke="{a.CYAN}" stroke-width="{w}" stroke-linecap="round" stroke-dasharray="14 12"/>',
                      flow, a.show(t0, t1), still=0))
    a.add(at(a, a.text(440, GY - 14, lab, 15, a.BLUE, a.SANS, 600, "middle"), t0, t1, still=0))

# ---------- IK
a.add(a.box(612, 176, 540, 456, a.WHITE, a.LINE, rx=18))
a.add(a.text(634, 210, "Código IK", 22, a.INK, a.HEAD, 600) + a.text(752, 210, "IEC 62262 · impacto", 15, a.GREY, a.MONO))
SX, SY, ST = 650, 300, 46
a.add(f'<path d="M{SX} {SY} H{SX + 10 * ST}" stroke="{I.LINE2}" stroke-width="6" stroke-linecap="round"/>')
for i in range(11):
    x = SX + i * ST
    a.add(f'<path d="M{x} {SY - 10} V{SY + 10}" stroke="{a.GREY}" stroke-width="2"/>')
    a.add(a.text(x, SY + 34, f"{i:02d}", 15, a.GREY, a.MONO, 500, "middle"))
x06, x10 = SX + 6 * ST, SX + 10 * ST
a.add(at(a, a.pill(x06, SY - 52, "IK06 · 1 J", a.WHITE, a.BLUE, 15, anchor="middle") + f'<circle cx="{x06}" cy="{SY}" r="9" fill="{a.BLUE}"/>', 76, 100, still=1))
a.add(at(a, a.pill(x10 - 44, SY - 52, "IK10 · 20 J", a.WHITE, a.INK, 15, anchor="middle") + f'<circle cx="{x10}" cy="{SY}" r="9" fill="{a.INK}"/>', 86, 100, still=1))
a.add(a.text(SX, SY + 66, "más alto, más energía de impacto que soporta", 15, a.TXT, a.SANS, 500))

# ensayo de impacto (paso 4)
FY = 560
a.add(f'<path d="M660 {FY} H1120" stroke="{a.INK}" stroke-width="5" stroke-linecap="round"/>')
for (cx, r, t0, lab, sub) in ((790, 14, 77, "1 J · IK06", "R29"), (990, 26, 87, "20 J · IK10", "X915 V2.0")):
    ball = f'<circle cx="0" cy="0" r="{r}" fill="{a.GREY}" stroke="{a.INK}" stroke-width="2"/>'
    a.add(a.group(ball, a.move([(0, cx, 440), (t0, cx, 440), (t0 + 4, cx, FY - r - 3), (100, cx, FY - r - 3)]), a.show(t0 - 1, t0 + 4.5, 0.5), still=0))
    a.add(at(a, f'<circle cx="{cx}" cy="{FY - r - 3}" r="{r}" fill="{a.GREY}" stroke="{a.INK}" stroke-width="2"/>', t0 + 4, 100, still=1))
    a.add(at(a, f'<path d="M{cx - 30} {FY - 6} L{cx - 44} {FY - 22} M{cx + 30} {FY - 6} L{cx + 44} {FY - 22}" stroke="{a.AMB}" stroke-width="3" stroke-linecap="round"/>', t0 + 4, t0 + 9, still=0))
    a.add(at(a, a.text(cx, FY + 32, lab, 16, a.INK, a.MONO, 600, "middle") + a.text(cx, FY + 54, sub, 15, a.GREY, a.MONO, 500, "middle"), t0 + 4, 100, still=1))
a.add(at(a, a.text(634, 400, "Mismo panel, distinto golpe", 16, a.TXT, a.SANS, 600), 76, 100, still=1))

a.write(*out(22)[:1], title="Cómo se leen los códigos IP e IK",
        desc=("Animación en cuatro tiempos. A la izquierda, el código IP según IEC 60529; a la derecha, el código IK según IEC 62262. "
              "1: el primer dígito del IP es sólidos; 6 es hermético al polvo y vale igual para IP65 e IP66: el polvo no entra al frente del portero. "
              "2: el segundo dígito es agua; 5 resiste chorros de agua. 3: 6 resiste chorros potentes; entre IP65 e IP66 cambia la fuerza del agua que soportan. "
              "4: el IK va de 00 a 10 y mide la energía de impacto que soporta el gabinete; IK06 son 1 joule (lo que publica el R29) e IK10 son 20 joules (el X915 V2.0), el valor más alto."),
        preview=[12, 40, 64, 84, 96], prefix=out(22)[1])
