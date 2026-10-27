#!/usr/bin/env python3
"""Lección 4 · teoría: FastTrack saltea firewall, connection tracking y colas; el contador de forward queda quieto."""
from _anim_mikrotik_1_13 import *

a = Anim(T=24, kicker="MIKROTIK · LECCIÓN 4 · FASTTRACK", title="FastTrack: un atajo para las conexiones establecidas")
a.steps([
    "Los primeros paquetes de una conexión pasan por conntrack, filter y colas.",
    "La regla fasttrack-connection marca la conexión, ya establecida.",
    "Los que siguen van por el camino rápido: el contador de forward se queda quieto.",
    "Al lado de fasttrack va un accept igual, para lo que siga por el camino normal.",
], still=2)

# camino normal
BY, BH = 186, 112
a.add(device(a, 48, BY, 150, BH, "LAN", "192.168.88.10"))
a.add(device(a, 1002, BY, 150, BH, "WAN", "internet"))
a.add(a.box(250, BY, 200, BH, a.WHITE, a.LINE))
a.add(a.text(268, BY + 32, "connection", 17, a.INK, a.SANS, 600))
a.add(a.text(268, BY + 54, "tracking", 17, a.INK, a.SANS, 600))
a.add(during(a, a.pill(268, BY + 70, "fasttrack", a.AMB, a.AMBBG, 14), 33, 100, still=1))
a.add(a.box(480, BY, 300, BH, a.WHITE, a.LINE))
a.add(a.text(498, BY + 32, "filter · forward", 17, a.INK, a.SANS, 600))
a.add(a.text(498, BY + 64, "fasttrack-connection", 14, a.TXT, a.MONO))
a.add(a.text(498, BY + 90, "accept established…", 14, a.TXT, a.MONO))
a.add(during(a, a.box(488, BY + 44, 284, 30, "none", a.AMB, rx=8, sw=2.5), 27, 50))
a.add(during(a, a.box(488, BY + 70, 284, 30, "none", a.OK, rx=8, sw=2.5), 77, 98.5))
a.add(a.box(810, BY, 162, BH, a.WHITE, a.LINE))
a.add(a.text(828, BY + 32, "colas", 17, a.INK, a.SANS, 600))
a.add(a.text(828, BY + 56, "queues", 14, a.GREY, a.MONO))

PY = BY + BH + 30
a.add(line(198, PY, 1002, PY, a.LINE, 3, "4 6"))
a.add(a.text(600, PY + 36, "camino normal", 14, a.GREY, a.MONO, 400, "middle"))

FY = 452
a.add(f'<path d="M123 {BY + BH} V{FY} H1077 V{BY + BH}" fill="none" stroke="{a.AMB}" stroke-width="3" stroke-dasharray="10 6"/>')
a.add(a.text(600, FY - 16, "camino rápido: saltea firewall, connection tracking y colas", 15, a.AMB, a.MONO, 600, "middle"))


def dot(col):
    return f'<circle cx="0" cy="0" r="10" fill="{col}"/>'


# 1 y 2: paquetes por el camino normal
for t0 in (2, 10, 27):
    a.add(travel(a, dot(a.BLUE), [(198, PY), (1002, PY)], t0, t0 + 8, hold=0.5))
# 3: corriente por el camino rápido
for i in range(6):
    t0 = 51 + i * 3.5
    a.add(travel(a, dot(a.AMB), [(123, BY + BH + 8), (123, FY), (1077, FY), (1077, BY + BH + 8)], t0, t0 + 9, hold=0.3))
a.add(still_only(a, place(a, dot(a.AMB), 420, FY) + place(a, dot(a.AMB), 640, FY) + place(a, dot(a.AMB), 860, FY)))
# 4: un paquete que sigue por el camino normal
a.add(travel(a, dot(a.BLUE), [(198, PY), (1002, PY)], 79, 88, hold=0.5))

# contadores
CY = 492
a.add(a.box(48, CY, 1104, 112, a.INK, rx=12))
a.add(a.text(66, CY + 28, "/IP/FIREWALL/FILTER/PRINT STATS WHERE CHAIN=FORWARD", 12, SKY, a.MONO, 400, extra='letter-spacing="1.6"'))
a.add(a.text(66, CY + 60, "special dummy rule to show fasttrack counters", 15, a.WHITE, a.MONO))
a.add(a.text(66, CY + 90, "reglas de forward (camino normal)", 15, a.WHITE, a.MONO))


def counter(x, y, vals, col):
    for t0, t1, v, st in vals:
        a.add(a.group(a.text(x, y, v, 17, col, a.MONO, 600, "end"), a.show(t0, t1, 0.3), still=st))


counter(1130, CY + 60, [(0, 54, "0", 0), (54, 58, "40", 0), (58, 62, "120", 0), (62, 66, "210", 1), (66, 70, "300", 0), (70, 100, "380", 0)], GOLD)
counter(1130, CY + 90, [(0, 10, "0", 0), (10, 18, "1", 0), (18, 35, "2", 0), (35, 87, "3", 1), (87, 100, "4", 0)], MINT)
a.add(during(a, a.text(1096, CY + 90, "quieto", 15, GOLD, a.MONO, 600, "end"), 55, 76, still=1))

a.add(a.text(48, 640, "Por eso un contador de forward puede quedar quieto aunque haya tráfico: lo cuenta la fila de fasttrack.", 16, a.TXT, a.SANS, 600))

p, pre = out(4, 2)
a.write(p, title="FastTrack en RouterOS",
        desc="Animación en cuatro tiempos. Arriba, el camino normal de un paquete de la LAN a la WAN: connection tracking, filter forward (con las reglas "
             "fasttrack-connection y accept established) y colas. Abajo, el camino rápido. 1: los primeros paquetes de la conexión pasan por el camino normal y "
             "el contador de forward sube. 2: la regla fasttrack-connection marca la conexión establecida. 3: los paquetes que siguen van por el camino rápido, "
             "que saltea firewall, connection tracking y colas: el contador de forward se queda quieto y sube la fila special dummy rule to show fasttrack counters. "
             "4: al lado de la regla fasttrack va un accept igual, para lo que siga por el camino normal.",
        preview=[12, 40, 63, 85], prefix=pre)
