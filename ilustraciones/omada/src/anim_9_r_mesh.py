#!/usr/bin/env python3
"""Lección 9 · Resumen, "Cómo se ve en la red": mesh. El Mesh AP se engancha a un uplink con señal entre -40 y -62 dBm;
cada salto vuelve a repartir el tiempo de aire (radio half-duplex); estrella mejor que cadena; Auto Failover elige otro uplink
si cae uno (apagado de fábrica y con el controlador corriendo)."""
from _anim_om_red import *

a = nueva(28, "ROAMING Y MESH", "Mesh: lleva señal donde no llega el cable, no suma capacidad")
F = a.steps([
    "El Root AP tiene cable. El Mesh AP se engancha a un uplink con señal entre -40 y -62 dBm.",
    "Un cliente del Mesh AP de 2 saltos: su tráfico cruza el aire dos veces antes del cable.",
    "La radio habla de a uno: cada salto reparte otra vez el tiempo de aire. Estrella, no cadena.",
    "Auto Failover: si cae el uplink de un Mesh AP, el controlador le elige otro.",
], still=1)

SWX, Y = 48, 300
a.add(dev(a, SWX, Y - 40, 190, 80, "Switch", "cable", icon="server"))
NODES = {"root": (360, Y, "Root AP", "con cable"), "m1": (640, Y, "Mesh AP", "1 salto"), "m2": (940, Y, "Mesh AP", "2 saltos"),
         "m3": (560, 446, "Mesh AP", "1 salto")}
a.add(line(238, Y, 330, Y, a.BLUE, 5))


def wl(p, q, color=a.CYAN, dash="7 7", w=3):
    (x1, y1), (x2, y2) = NODES[p][:2], NODES[q][:2]
    return line(x1, y1, x2, y2, color, w, dash)


# enlaces inalámbricos (debajo de los equipos)
a.add(wl("root", "m1"))
at(a, wl("m1", "m2"), 0, 76, still=1)
a.add(wl("root", "m3"))
at(a, line(940, Y, 560, 446, a.OK, 4, "8 6"), 82, 100)
for k, (x, y, t, s_) in NODES.items():
    a.add(eap(a, x, y, 30))
    a.add(a.text(x, y + 52, t, 16, a.INK, a.SANS, 600, "middle") + a.text(x, y + 74, s_, 15, a.GREY, a.MONO, 400, "middle"))
at(a, a.text(500, Y - 18, "-55 dBm", 15, a.CYAN, a.MONO, 600, "middle"), 4, 100, still=1)
at(a, chip(a, 500, Y - 70, "uplink: -40 a -62 dBm", a.CYAN, "#E6F6FB", anchor="middle", stroke=a.CYAN), 3, 25)
# 1: el mesh AP busca uplink
for r, t0 in ((40, 4), (70, 7), (100, 10)):
    at(a, f'<circle cx="640" cy="{Y}" r="{r}" fill="none" stroke="{a.CYAN}" stroke-width="2" stroke-dasharray="4 6"/>', t0, t0 + 5)

# 2: el cliente en el AP de 2 saltos
a.add(glyph(a, "phone", 1040, Y - 80, a.INK, 1.4))
a.add(line(1056, Y - 40, 960, Y - 20, a.LINE, 2, "4 4"))
travel(a, dot(a, a.AMB, 10), [(1056, Y - 44), (940, Y), (640, Y), (360, Y), (238, Y)], 28, 40, hold=1)
at(a, chip(a, 790, Y + 18, "aire, salto 2", a.AMB, a.AMBBG, anchor="middle", stroke=a.AMB), 30, 50)
at(a, chip(a, 500, Y + 18, "aire, salto 1", a.AMB, a.AMBBG, anchor="middle", stroke=a.AMB), 34, 50)

# 3: tiempo de aire repartido
BX, BY = 48, 582
a.add(a.text(BX, BY - 12, "Aire del Mesh AP de 1 salto (ilustrativo)", 15, a.GREY, a.SANS, 600))
a.add(a.box(BX, BY, 450, 34, a.SLATE, rx=8))
segs = [(0, 150, "clientes", a.CYAN), (150, 150, "uplink", a.BLUE), (300, 150, "downlink", a.NAVY2)]
for i, (x, w, lab, col) in enumerate(segs):
    at(a, a.box(BX + x, BY, w, 34, col, rx=8) + a.text(BX + x + w / 2, BY + 23, lab, 15, a.WHITE, a.MONO, 600, "middle"), 52 + i * 4, 76, still=1)
at(a, note(a, 720, 500, 432, 116, "Límites", ["Hasta 3 saltos y 4 downlinks por uplink.", "EAP225-Outdoor: 50 a 60 clientes", "en toda la red mesh."], "amb"), 52, 76, still=1)
at(a, note(a, 720, 500, 432, 116, "Cobertura, no capacidad", ["Con mucha gente, cable. Que la mayoría", "de los clientes quede en el Root AP", "o a 1 salto."], "info"), 0, 52)

# 4: Auto Failover
at(a, xmark(a, 640, Y, 20), 78, 100)
at(a, a.text(790, 400, "uplink nuevo", 15, a.OK, a.SANS, 600), 83, 100)
at(a, note(a, 720, 500, 432, 116, "Auto Failover", ["Viene apagado y necesita el controlador", "corriendo. Sin controlador, el mesh", "mantiene la cobertura básica."], "ok"), 76, 100)

write(a, 9, "r1", "Mesh: cada salto reparte el tiempo de aire",
      "Animación en cuatro tiempos con un switch, un Root AP con cable y tres Mesh AP: dos a un salto y uno a dos saltos, en cadena. "
      "1: el Mesh AP busca un uplink y se engancha al Root AP sin cable, con una señal recomendada entre -40 y -62 dBm. "
      "2: el tráfico de un celular conectado al Mesh AP de dos saltos cruza el aire dos veces, salto 2 y salto 1, antes de llegar al cable. "
      "3: la radio es half-duplex y habla de a uno: el tiempo de aire de un Mesh AP se reparte entre clientes, uplink y downlink, y cada salto resta rendimiento; "
      "por eso estrella mejor que cadena, hasta 3 saltos y 4 downlinks por uplink, y un EAP225-Outdoor recomienda 50 a 60 clientes para toda la red mesh. "
      "4: cae el Mesh AP que hacía de uplink y, con Auto Failover, el controlador le elige otro uplink al Mesh AP de dos saltos. "
      "Auto Failover viene apagado y necesita el controlador corriendo; sin controlador, el mesh mantiene la cobertura básica.",
      [8, 36, 62, 90])
