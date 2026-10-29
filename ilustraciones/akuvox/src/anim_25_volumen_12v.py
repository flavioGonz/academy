#!/usr/bin/env python3
"""Lección 25 · teoría: en el R25 con PoE, la salida de 12 V por el relé queda afectada por el volumen; en obra, fuente propia."""
import math
from _anim_akuvox_15_28 import *

a = new(24, "AKUVOX", "R25 con PoE: la cerradura no debería depender del volumen")
a.steps([
    "R25 con PoE: 12 V por el relé, hasta 400 mA, con firmware 25.30.10.11 o más.",
    "Akuvox avisa que esa salida queda afectada por el ajuste de volumen.",
    "Por eso se mide con volumen bajo y alto, con la carga conectada, al abrir.",
    "En obra: fuente propia para la cerradura y el relé como contacto seco.",
], still=3)

# R25
a.add(I.Generic(60, 196, "R25 con PoE", "fw 25.30.10.11 o más", icon="bell", w=270).svg())
a.add(at(a, a.box(56, 192, 278, 92, "none", a.CYAN, rx=18, sw=3), 2, 24, still=0))
# volumen
a.add(a.box(60, 312, 270, 100, a.WHITE, a.LINE, rx=14))
a.add(a.text(80, 340, "Volumen del equipo", 15, a.TXT, a.SANS, 600))
a.add(f'<path d="M92 374 H298" stroke="{I.LINE2}" stroke-width="6" stroke-linecap="round"/>')
a.add(a.text(92, 400, "bajo", 15, a.GREY, a.MONO, 500, "middle") + a.text(298, 400, "alto", 15, a.GREY, a.MONO, 500, "middle"))
LO, HI = 92, 298
vol = [(0, LO), (28, LO), (38, HI), (46, HI), (50, LO), (60, LO), (63, HI), (73, HI), (76, LO), (82, LO), (88, HI), (94, HI), (98, LO), (100, LO)]
knob = f'<circle cx="0" cy="0" r="13" fill="{a.BLUE}" stroke="{a.WHITE}" stroke-width="3"/>'
a.add(a.group(knob, a.move([(p, x, 374) for p, x in vol]), a.show(0, 100), still=0))
a.add(only_still(a, f'<g transform="translate({HI} 374)">{knob}</g>'))

# cerradura y cableado A (12 V por el relé)
a.add(I.Lock(500, 232, "Cerradura", "carga de banco", w=230).svg())
wA = f'<path d="M330 252 H500" stroke="{a.BAD}" stroke-width="4"/><path d="M330 268 H500" stroke="#2B2B2B" stroke-width="4"/>'
a.add(at(a, wA + a.text(415, 300, "12 V por el relé", 15, a.BAD, a.MONO, 600, "middle") + a.text(415, 322, "400 mA máx.", 15, a.GREY, a.MONO, 500, "middle"), 0, 76, still=0))
# cableado B (paso 4)
wB = (I.PSU(500, 436, "Fuente propia", "para la cerradura", w=230).svg()
      + f'<path d="M560 436 V316" stroke="{a.BAD}" stroke-width="4"/><path d="M670 436 V316" stroke="#2B2B2B" stroke-width="4"/>'
      + f'<path d="M330 260 H430 V376 H560" fill="none" stroke="{a.CYAN}" stroke-width="4" stroke-dasharray="2 0"/>'
      + a.pill(445, 344, "relé: contacto seco", a.CYAN, a.WHITE, 15, anchor="middle"))
a.add(at(a, wB, 76, 100, still=1))

# medidor
CX, CY, R = 950, 420, 140
a.add(a.box(790, 196, 362, 330, a.WHITE, a.LINE, rx=18))
a.add(a.text(810, 228, "Tensión en la cerradura", 17, a.INK, a.SANS, 600))
a.add(f'<path d="M{CX - R} {CY} A{R} {R} 0 0 1 {CX + R} {CY}" fill="none" stroke="{I.LINE2}" stroke-width="10" stroke-linecap="round"/>')
for i in range(9):
    ang = math.radians(180 - i * 22.5)
    x1, y1 = CX + (R - 20) * math.cos(ang), CY - (R - 20) * math.sin(ang)
    x2, y2 = CX + (R - 6) * math.cos(ang), CY - (R - 6) * math.sin(ang)
    a.add(f'<path d="M{x1:.1f} {y1:.1f} L{x2:.1f} {y2:.1f}" stroke="{a.GREY}" stroke-width="2"/>')
needle = f'<path d="M{CX} {CY} L{CX} {CY - R + 26}" stroke="{a.INK}" stroke-width="5" stroke-linecap="round"/><circle cx="{CX}" cy="{CY}" r="10" fill="{a.INK}"/>'
ang = lambda x: 20 if x == HI else 0
pts = [(p, ang(x) if p < 76 else 0) for p, x in vol]
nd = a.keyframes([(p, d) for p, d in pts], "transform", "rotate({}deg)")
a.add(a.group(needle, nd, a.show(0, 100), still=0, origin=f"{CX}px {CY}px"))
a.add(only_still(a, needle))
a.add(at(a, a.text(CX, CY + 40, "puede cambiar con el volumen", 16, a.BAD, a.SANS, 600, "middle"), 26, 76, still=0))
a.add(at(a, a.text(CX, CY + 40, "no depende del volumen", 16, a.OK, a.SANS, 600, "middle"), 78, 100, still=1))
a.add(a.text(CX, CY + 74, "esquema sin valores: medí y anotá", 15, a.GREY, a.SANS, 500, "middle"))

# planilla de medición (paso 3)
a.add(at(a, a.box(60, 548, 670, 84, a.WHITE, a.LINE, rx=14)
         + a.text(80, 580, "Durante la apertura", 15, a.TXT, a.SANS, 600)
         + a.text(80, 612, "Volumen bajo : ____ V", 17, a.INK, a.MONO, 600)
         + a.text(400, 612, "Volumen alto : ____ V", 17, a.INK, a.MONO, 600), 51, 76, still=0))
a.add(at(a, a.box(60, 548, 1092, 84, a.OKBG, a.OK, rx=14, sw=1.5)
         + a.text(80, 582, "Las dos salidas: fuente de 12 V 1 A para el portero, o fuente propia para la cerradura.", 17, a.INK, a.SANS, 600)
         + a.text(80, 612, "La segunda es la estable en obra: la cerradura no depende del volumen.", 17, a.OK, a.SANS, 600), 77, 100, still=1))

a.write(*out(25)[:1], title="R25 con PoE: 12 V y volumen",
        desc=("Animación en cuatro tiempos. 1: un R25 alimentado por PoE da 12 V por el relé a una cerradura de banco, hasta 400 mA, con firmware 25.30.10.11 o más. "
              "2: Akuvox avisa que esa salida queda afectada por el ajuste de volumen: al mover el volumen, la aguja que muestra la tensión en la cerradura se mueve. "
              "3: por eso se mide con la carga conectada, durante la apertura, con volumen bajo y con volumen alto, y se anotan las dos lecturas. "
              "4: en obra, la cerradura va con fuente propia y el relé del portero queda como contacto seco; al mover el volumen la aguja no cambia. "
              "La otra salida es una fuente de 12 V 1 A para el portero. El medidor es un esquema sin valores."),
        preview=[12, 40, 66, 92], prefix=out(25)[1])
