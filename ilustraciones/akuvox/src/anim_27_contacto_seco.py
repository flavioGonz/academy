#!/usr/bin/env python3
"""Lección 27 · teoría: E16C y E18C sin salida de 12 V; el relé es un contacto seco. NO = fail-secure, NC = fail-safe."""
import math
from _anim_akuvox_15_28 import *

a = new(24, "AKUVOX · LECCIÓN 27", "Contacto seco: el relé une COM con NO o con NC")
a.steps([
    "El relé del E16C o E18C es un contacto seco: une o separa, no aporta energía.",
    "En reposo, COM toca NC. Con NO, la cerradura queda sin energía; con NC, el imán tiene.",
    "El relé actúa: COM pasa a NO. La fail-secure recibe energía; el imán la pierde. Liberan.",
    "Sin energía en la fuente: la fail-secure (NO) queda trabada; la fail-safe (NC) libera.",
], still=2, size=17)

ON_NO = [(53, 73)]          # relé activado
FLOW = a.keyframes([(0, 0), (100, -900)], "stroke-dashoffset")


def panel(X0, title, sub, use_no, lock_title, lock_sub):
    a.add(a.box(X0, 176, 540, 456, a.WHITE, a.LINE, rx=18))
    a.add(a.text(X0 + 22, 210, title, 21, a.INK, a.HEAD, 600) + a.text(X0 + 22, 234, sub, 15, a.GREY, a.MONO))
    # fuente
    a.add(I.PSU(X0 + 22, 256, "Fuente", "12 V", w=180).svg())
    a.add(a.text(X0 + 214, 270, "+", 20, a.BAD, a.MONO, 600) + a.text(X0 + 126, 364, "−", 20, a.INK, a.MONO, 600))
    # relé
    RX, RY = X0 + 250, 256
    a.add(a.box(RX, RY, 268, 172, a.WHITE, I.LINE2, rx=14))
    a.add(a.text(RX + 16, RY + 28, "Relé del portero", 16, a.INK, a.SANS, 600) + a.text(RX + 16, RY + 50, "no aporta energía", 15, a.GREY, a.MONO))
    cx, cy = RX + 50, RY + 112
    nx = RX + 170
    for lab, y, ly in (("NO", cy - 26, cy - 40), ("NC", cy + 26, cy + 52)):
        a.add(f'<circle cx="{nx}" cy="{y}" r="8" fill="{I.SOFT}" stroke="{a.BLUE}" stroke-width="2"/>' + a.text(nx, ly, lab, 15, a.INK, a.MONO, 600, "middle"))
    a.add(f'<circle cx="{cx}" cy="{cy}" r="8" fill="{I.SOFT}" stroke="{a.BLUE}" stroke-width="2"/>' + a.text(cx - 14, cy + 32, "COM", 15, a.INK, a.MONO, 600))
    ang = math.degrees(math.atan2(26, nx - cx - 8))
    lever = f'<path d="M{cx} {cy} L{nx - 8} {cy}" stroke="{a.INK}" stroke-width="5" stroke-linecap="round"/>'
    rot = a.keyframes([(0, ang), (52, ang), (54, -ang), (72, -ang), (74, ang), (100, ang)], "transform", "rotate({}deg)")
    a.add(a.group(lever, rot, a.show(0, 100), still=0, origin=f"{cx}px {cy}px"))
    a.add(only_still(a, f'<g transform="rotate({-ang:.2f} {cx} {cy})">{lever}</g>'))
    # cerradura
    LX, LY = X0 + 250, 486
    a.add(I.Lock(LX, LY, lock_title, " ", w=268).svg())
    # cables
    py = cy - 26 if use_no else cy + 26
    loop = (f"M{X0 + 202} 278 H{X0 + 232} V{cy} H{cx}"            # + a COM
            f" M{nx} {py} H{RX + 254} V{LY}"                       # NO/NC a cerradura
            f" M{LX} {LY + 60} H{X0 + 112} V340")                  # − de vuelta
    a.add(f'<path d="{loop}" fill="none" stroke="{a.BAD}" stroke-width="4"/>')
    unused = cy + 26 if use_no else cy - 26
    a.add(a.text(nx + 18, unused + 6, "libre", 15, a.GREY, a.MONO))
    return loop, (LX + 64, LY + 66), RX


# ----- panel NO (fail-secure)
loopL, (sxL, syL), _ = panel(48, "Fail-secure", "COM + NO", True, "Cerradura", "")
a.add(a.group(f'<path d="{loopL}" fill="none" stroke="#FFD28A" stroke-width="4" stroke-dasharray="12 12"/>', FLOW, a.show(53, 73), still=1))
a.add(at(a, a.text(sxL, syL, "trabada · sin energía", 15, a.GREY, a.MONO, 600), 0, 53, still=0))
a.add(at(a, a.text(sxL, syL, "libera", 15, a.OK, a.MONO, 600), 53, 74, still=1))
a.add(at(a, a.text(sxL, syL, "queda trabada", 15, a.BAD, a.MONO, 600), 76, 100, still=0))

# ----- panel NC (fail-safe)
loopR, (sxR, syR), RXR = panel(612, "Fail-safe", "COM + NC · electroimán", False, "Electroimán", "")
a.add(a.group(f'<path d="{loopR}" fill="none" stroke="#FFD28A" stroke-width="4" stroke-dasharray="12 12"/>', FLOW, a.show(0, 52), still=0))
a.add(at(a, a.text(sxR, syR, "trabado · con energía", 15, a.GREY, a.MONO, 600), 0, 53, still=0))
a.add(at(a, a.text(sxR, syR, "libera", 15, a.OK, a.MONO, 600), 53, 100, still=1))
# diodo en antiparalelo junto al electroimán
DX = 612 + 200
a.add(f'<path d="M{RXR + 254} 462 H{DX} V546" fill="none" stroke="{a.INK}" stroke-width="2.5"/>')
a.add(f'<path d="M{DX - 11} 496 H{DX + 11} M{DX - 11} 512 H{DX + 11} L{DX} 496 Z" fill="{a.INK}" stroke="{a.INK}" stroke-width="2" stroke-linejoin="round"/>')
a.add(a.text(DX - 18, 510, "diodo", 15, a.TXT, a.MONO, 600, "end"))

# paso 1: el relé no aporta energía
for X0 in (48, 612):
    a.add(at(a, a.box(X0 + 246, 252, 276, 180, "none", a.CYAN, rx=16, sw=3), 1, 25, still=0))
# paso 4: sin energía
for X0 in (48, 612):
    a.add(at(a, a.box(X0 + 22, 256, 180, 84, a.BADBG, a.BAD, rx=16, sw=2)
             + a.text(X0 + 112, 292, "Fuente", 19, a.INK, a.SANS, 600, "middle") + a.text(X0 + 112, 318, "sin energía", 15, a.BAD, a.MONO, 600, "middle"), 75, 100, still=0))

a.write(*out(27)[:1], title="Relé de contacto seco: NO y NC",
        desc=("Animación en cuatro tiempos con dos circuitos: a la izquierda una cerradura fail-secure cableada a COM y NO; a la derecha un electroimán fail-safe a COM y NC, con diodo en antiparalelo. "
              "En los dos, el positivo de la fuente de 12 V va a COM y el negativo de la cerradura vuelve a la fuente. "
              "1: el relé del E16C o E18C es un contacto seco: une o separa, no aporta energía. "
              "2: en reposo COM toca NC; con NO la cerradura queda sin energía y trabada, con NC el electroimán tiene energía y traba. "
              "3: el relé actúa y COM pasa a NO: la fail-secure recibe energía y libera, el electroimán la pierde y libera. "
              "4: sin energía en la fuente, la fail-secure queda trabada y la fail-safe libera."),
        preview=[12, 40, 62, 90], prefix=out(27)[1])
