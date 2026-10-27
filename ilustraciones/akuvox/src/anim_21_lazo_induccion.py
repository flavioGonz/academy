#!/usr/bin/env python3
"""Lección 21 · teoría: el lazo de inducción lleva la voz directo al audífono (telebobina), sin el ruido de la calle."""
import math
from _anim_akuvox_15_28 import *

a = new(20, "AKUVOX · LECCIÓN 21", "Lazo de inducción: la voz directo al audífono")
a.steps([
    "El portero recibe la voz de la llamada y la saca por el parlante.",
    "En la vereda, esa voz llega al audífono mezclada con el ruido de la calle.",
    "El lazo de inducción manda la misma voz como campo magnético.",
    "La telebobina del audífono la toma directo: llega la voz, sin el ruido.",
], still=3)

# campo del lazo (pasos 3 y 4)
a.add('<clipPath id="cl21"><rect x="40" y="176" width="1112" height="350"/></clipPath>')
for i, r in enumerate((100, 190, 290, 400, 530)):
    k = a.keyframes([(0, 0), (52 + i * 2, 0), (54 + i * 2, .9), (100, .9)])
    a.add('<g clip-path="url(#cl21)">' + a.group(f'<ellipse cx="175" cy="300" rx="{r}" ry="{r * .42:.0f}" fill="none" stroke="{a.CYAN}" stroke-width="3" stroke-dasharray="10 8"/>', k, still=.9) + '</g>')
# portero
a.add(a.box(60, 456, 230, 56, a.BG, rx=8))
a.add(I.Intercom(100, 188, "S535 o S532", "con lazo de inducción", screen=True).svg())
# persona con audífono
PX, PY = 820, 286
a.add(f'<circle cx="{PX}" cy="{PY}" r="42" fill="{I.SOFT}" stroke="{a.INK}" stroke-width="2.5"/>')
a.add(f'<path d="M{PX - 70} 446 C{PX - 70} 296 {PX + 70} 296 {PX + 70} 446" fill="{I.SOFT}" stroke="{a.INK}" stroke-width="2.5"/>')
a.add(f'<rect x="{PX - 56}" y="{PY - 16}" width="16" height="30" rx="7" fill="{a.BLUE}"/>')
a.add(a.text(PX, 476, "visitante con audífono", 17, a.INK, a.SANS, 600, "middle"))
a.add(a.text(PX, 498, "con telebobina", 15, a.GREY, a.MONO, 400, "middle"))

# ruido de calle
a.add(a.text(1150, 218, "ruido de calle", 16, a.GREY, a.SANS, 600, "end"))
def arc(cx, cy, r, color, w=3, left=True, dash=""):
    s = -1 if left else 1
    x1, y1 = cx + s * r * math.cos(math.radians(40)), cy - r * math.sin(math.radians(40))
    x2, y2 = cx + s * r * math.cos(math.radians(40)), cy + r * math.sin(math.radians(40))
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<path d="M{x1:.1f} {y1:.1f} A{r} {r} 0 0 {0 if left else 1} {x2:.1f} {y2:.1f}" fill="none" stroke="{color}" stroke-width="{w}" stroke-linecap="round"{d}/>'

# ondas de voz por el aire (pasos 1 a 2) y ruido (paso 2)
for i in range(3):
    d = i * 3
    a.add(a.group(arc(0, 0, 26, a.BLUE, 4, left=False), a.move([(0, 270, 300), (4 + d, 270, 300), (22 + d, 730, 270), (100, 730, 270)]),
                  a.show(4 + d, 22 + d, 1), still=0))
    a.add(a.group(arc(0, 0, 26, a.BLUE, 4, left=False), a.move([(0, 270, 300), (27 + d, 270, 300), (45 + d, 730, 270), (100, 730, 270)]),
                  a.show(27 + d, 45 + d, 1), still=0))
    a.add(a.group(arc(0, 0, 30, a.GREY, 4, left=True), a.move([(0, 1130, 300 + i * 30), (26 + d * 1.5, 1130, 300 + i * 30), (46 + d, 900, 268), (100, 900, 268)]),
                  a.show(26 + d * 1.5, 46 + d, 1), still=0))
a.add(at(a, a.text(500, 250, "voz por el aire", 16, a.BLUE, a.SANS, 600, "middle"), 3, 50, still=0))

a.add(at(a, a.pill(500, 404, "campo magnético del lazo", a.CYAN, a.WHITE, 15, anchor="middle"), 52, 100, still=1))
a.add(at(a, a.box(PX - 62, PY - 22, 28, 42, "none", a.OK, rx=10, sw=3) + a.box(PX - 214, PY - 54, 136, 28, a.BG, rx=6) + a.text(PX - 84, PY - 34, "toma el campo", 15, a.OK, a.MONO, 600, "end"), 78, 100, still=1))

# lo que llega
def wave(x, y, w, clean=True):
    pts = []
    for j in range(0, w + 1, 4):
        t = j / w * 8 * math.pi
        v = math.sin(t) * 16 * math.sin(j / w * math.pi)
        if not clean:
            v += math.sin(j * 1.7) * 9 + math.sin(j * .53 + 1) * 7
        pts.append(f"{x + j:.0f} {y + v:.1f}")
    return "M" + " L".join(pts)

a.add(a.box(48, 540, 540, 100, a.WHITE, a.LINE, rx=14))
a.add(a.text(66, 568, "Por el aire: voz y ruido", 17, a.INK, a.SANS, 600))
a.add(f'<path d="{wave(330, 600, 230, False)}" fill="none" stroke="{a.GREY}" stroke-width="2.5"/>')
a.add(a.text(66, 600, "lo que entra con la vereda", 15, a.GREY, a.SANS))
a.add(at(a, a.box(48, 540, 540, 100, "none", a.BAD, rx=14, sw=2.5), 27, 50, still=0))
a.add(a.box(612, 540, 540, 100, a.WHITE, a.LINE, rx=14))
a.add(a.text(630, 568, "Por el lazo: solo la voz", 17, a.INK, a.SANS, 600))
a.add(a.text(630, 600, "directo a la telebobina", 15, a.GREY, a.SANS))
a.add(at(a, f'<path d="{wave(900, 600, 230, True)}" fill="none" stroke="{a.OK}" stroke-width="3"/>' + a.box(612, 540, 540, 100, "none", a.OK, rx=14, sw=2.5), 77, 100, still=1))

a.write(*out(21)[:1], title="Lazo de inducción en un portero",
        desc=("Animación en cuatro tiempos. 1: el portero S535 o S532 con lazo de inducción recibe la voz de la llamada y la saca por el parlante. "
              "2: en la vereda, esa voz llega al visitante con audífono mezclada con el ruido de la calle. "
              "3: el lazo de inducción manda la misma voz como campo magnético alrededor del portero. "
              "4: la telebobina del audífono toma el campo directo; por el aire llegan voz y ruido, por el lazo llega solo la voz."),
        preview=[12, 38, 62, 90], prefix=out(21)[1])
