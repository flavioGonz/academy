#!/usr/bin/env python3
"""Lección 4 · teoría: por qué el electroimán lleva diodo en antiparalelo (la bobina y el arco en el contacto)."""
from _anim_akuvox import Anim, A, token, appear, finish

a = Anim(T=24, kicker="AKUVOX · RELÉ Y CERRADURA", title="La bobina, el arco y el diodo")
P = a.steps([
    "Con el contacto cerrado, la corriente pasa por la bobina del electroimán.",
    "Sin diodo: el contacto abre, la tensión de la bobina salta y hay arco.",
    "Con diodo (cátodo al +): la corriente sigue por el diodo y se apaga sin arco.",
], still=2)

RED, CY = A.BAD, A.CYAN
TOP, BOT, XC, XD = 270, 490, 560, 690
C1, C2 = 300, 380            # bornes del contacto


def wire(pts, color=A.INK, w=4):
    d = "M" + " L".join(f"{x} {y}" for x, y in pts)
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{w}" stroke-linejoin="round" stroke-linecap="round"/>'


# fuente
a.add(a.box(60, 240, 150, 100, A.SLATE, None, rx=12))
a.add(a.text(78, 280, "Fuente 12 V", 17, A.INK, A.SANS, 600))
a.add(a.text(78, 306, "aparte", 14, A.GREY, A.MONO))
a.add(a.text(222, TOP - 10, "+", 18, RED, A.MONO, 600))
a.add(a.text(150, 366, "−", 18, A.INK, A.MONO, 600))
# cables
a.add(wire([(210, TOP), (C1, TOP)], RED))
a.add(wire([(C2, TOP), (XC, TOP), (XC, 320)], RED))
a.add(wire([(XC, 440), (XC, BOT), (135, BOT), (135, 340)]))
a.add(f'<circle cx="{C1}" cy="{TOP}" r="7" fill="{A.WHITE}" stroke="{A.INK}" stroke-width="2.5"/>')
a.add(f'<circle cx="{C2}" cy="{TOP}" r="7" fill="{A.WHITE}" stroke="{A.INK}" stroke-width="2.5"/>')
a.add(a.text((C1 + C2) / 2, TOP + 36, "contacto del relé", 14, A.GREY, A.MONO, 400, "middle"))
# bobina (símbolo de inductor)
coil = f"M{XC} 320 " + " ".join(f"a 13 10 0 1 1 0 20" for _ in range(6))
a.add(f'<path d="{coil}" fill="none" stroke="{A.INK}" stroke-width="4"/>')
a.add(a.text(XC - 30, 372, "bobina del", 15, A.INK, A.SANS, 600, "end"))
a.add(a.text(XC - 30, 394, "electroimán", 15, A.INK, A.SANS, 600, "end"))
# hojas del contacto: cerrada / abierta
closed = f'<line x1="{C1}" y1="{TOP}" x2="{C2 - 7}" y2="{TOP}" stroke="{A.INK}" stroke-width="5" stroke-linecap="round"/>'
opened = f'<line x1="{C1}" y1="{TOP}" x2="{C2 - 10}" y2="{TOP - 34}" stroke="{A.INK}" stroke-width="5" stroke-linecap="round"/>'
a.add(a.group(closed, a.keyframes([(0, 1), (36, 1), (36.5, 0), (66, 0), (66.5, 1), (76, 1), (76.5, 0), (100, 0)]), still=0))
a.add(a.group(opened, a.keyframes([(0, 0), (36, 0), (36.5, 1), (66, 1), (66.5, 0), (76, 0), (76.5, 1), (100, 1)]), still=1))

# diodo en antiparalelo (solo en el tiempo 3)
diode = (wire([(XC, TOP), (XD, TOP), (XD, 350)]) + wire([(XD, 410), (XD, BOT), (XC, BOT)])
         + f'<path d="M{XD - 18} 410 L{XD + 18} 410 L{XD} 372 z" fill="{A.OK}"/>'
         + f'<line x1="{XD - 20}" y1="370" x2="{XD + 20}" y2="370" stroke="{A.OK}" stroke-width="5"/>'
         + f'<line x1="{XD}" y1="350" x2="{XD}" y2="370" stroke="{A.INK}" stroke-width="4"/>'
         + a.text(XD + 30, 376, "diodo", 16, A.OK, A.SANS, 600)
         + a.text(XD + 30, 398, "cátodo al +", 14, A.OK, A.MONO, 600))
appear(a, diode, 66, 100, still=1)
appear(a, f'<rect x="{XD - 52}" y="350" width="104" height="60" rx="8" fill="none" stroke="{A.GREY}" stroke-width="1.5" stroke-dasharray="5 5"/>' + a.text(XD, 386, "sin diodo", 14, A.GREY, A.MONO, 600, "middle"), 34, 66, still=0)

# corriente: puntos que giran por el circuito
dot = f'<circle r="7" fill="{CY}"/>'
loop = [(210, TOP), (XC, TOP), (XC, BOT), (135, BOT), (135, 340)]
for k in range(4):
    t0 = 1 + k * 7
    token(a, loop, t0, t0 + 9, dot, hold=t0 + 9.2)
for k in range(2):
    t0 = 66 + k * 4
    token(a, loop, t0, t0 + 9, dot, hold=min(t0 + 9.2, 76))
spin = [(XC, 330), (XC, BOT), (XD, BOT), (XD, TOP), (XC, TOP), (XC, 330)]
for k in range(3):
    t0 = 77 + k * 5
    token(a, spin, t0, t0 + 7, f'<circle r="{7 - k * 1.5}" fill="{A.OK}"/>', hold=t0 + 7.2)
appear(a, a.text(60, 548, "la corriente gira por la bobina y el diodo hasta apagarse", 16, A.OK, A.SANS, 600), 77, 100, still=1)
appear(a, a.text(60, 548, "corriente: fuente → contacto → bobina → fuente", 16, CY, A.SANS, 600), 1, 33, still=0)

# arco en el contacto
spark = (f'<path d="M{C2 - 22} {TOP - 30} l10 12 l-8 4 l14 16 l-4 -14 l9 -2 l-12 -16 z" fill="#FFB020" stroke="{RED}" stroke-width="2"/>'
         + a.text(C2 + 18, TOP - 28, "arco", 16, RED, A.SANS, 600))
a.add(a.group(spark, a.keyframes([(0, 0), (36.5, 0), (37, 1), (38.5, .2), (39.5, 1), (41, .3), (42, 1), (46, 1), (47, 0), (100, 0)]), still=0))
appear(a, a.text(60, 548, "salto de tensión: la corriente busca camino por el aire", 16, RED, A.SANS, 600), 37, 66, still=0)

# gráfico de tensión en la bobina
GX, GY, GW, GH = 840, 180, 312, 360
a.add(a.box(GX, GY, GW, GH, A.WHITE, A.LINE, rx=16))
a.add(a.text(GX + 20, GY + 34, "Tensión en la bobina", 18, A.INK, A.HEAD, 600))
Y12, Y0, X0, XCUT, X1 = GY + 110, GY + 210, GX + 64, GX + 150, GX + GW - 20
a.add(a.text(X0 - 10, Y12 + 5, "12 V", 14, A.GREY, A.MONO, 400, "end"))
a.add(a.text(X0 - 10, Y0 + 5, "0", 14, A.GREY, A.MONO, 400, "end"))
a.add(f'<line x1="{X0}" y1="{Y0}" x2="{X1}" y2="{Y0}" stroke="{A.LINE}" stroke-width="2"/>')
a.add(f'<line x1="{XCUT}" y1="{GY + 60}" x2="{XCUT}" y2="{GY + GH - 50}" stroke="{A.GREY}" stroke-width="1.5" stroke-dasharray="4 5"/>')
a.add(a.text(XCUT, GY + GH - 26, "abre el contacto", 14, A.GREY, A.MONO, 400, "middle"))
a.add(wire([(X0, Y12), (XCUT, Y12)], A.INK, 3))
appear(a, wire([(XCUT, Y12), (XCUT, GY + GH - 56), (XCUT + 16, Y0), (X1, Y0)], RED, 3)
       + a.text(XCUT + 22, GY + GH - 64, "sin diodo: salto", 15, RED, A.SANS, 600), 37, 100, still=1)
appear(a, wire([(XCUT, Y12), (XCUT + 3, Y0 + 12), (XCUT + 70, Y0), (X1, Y0)], A.OK, 3)
       + a.text(XCUT + 22, Y0 - 16, "con diodo", 15, A.OK, A.SANS, 600), 77, 100, still=1)

finish(a, "4-t2.svg", "Por qué el electroimán lleva diodo",
       "Animación en tres tiempos de un circuito con fuente de 12 V aparte, el contacto del relé y la bobina de un electroimán, con un gráfico de la tensión en la bobina. "
       "1: con el contacto cerrado la corriente circula de la fuente al contacto, a la bobina y vuelve a la fuente. "
       "2: sin diodo, el contacto se abre; como la corriente de la bobina no puede cortarse de golpe, la tensión en sus bornes salta y aparece un arco en el contacto; en el gráfico se ve el salto. "
       "3: con un diodo en antiparalelo sobre la bobina, con el cátodo al positivo, al abrir el contacto la corriente sigue girando por la bobina y el diodo hasta apagarse, sin arco; en el gráfico la tensión baja a cero sin salto.",
       [15, 42, 88])
