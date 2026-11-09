#!/usr/bin/env python3
"""Caso de estudio · Audio en un sentido · teoría: qué IP pone la UCM en la c= según el destino (21-t1.svg).
Con External Host y Use IP address in SDP, la UCM mira si el destino está en Local Network Address:
si está, anuncia la IP de su interfaz; si no, External Host. Sin las redes de Antel en la lista, a Antel
también le anuncia la IP pública. Campos del manual del UCM630x (PBX Settings > SIP Settings > NAT).
Datos de ejemplo: External Host 192.0.2.10, LAN1 198.51.100.2/30, Antel 198.51.100.1 y 203.0.113.0/24.
"""
from _anim_gs_red import R

g = R(T=26, fix=92, kicker="GRANDSTREAM · CASO DE ESTUDIO · AUDIO EN UN SENTIDO", title="Qué IP anuncia la central en la c=")
g.steps([
    "Hacia un remoto por internet: no está en la lista, va External Host. Bien.",
    "Hacia Antel: tampoco está en la lista, y le anuncia la IP pública. Mal.",
    "Se suman las redes de Antel a Local Network Address.",
    "Hacia Antel ahora va la IP de LAN1; el remoto sigue con External Host.",
], size=17)

B, OK, BAD, GREY, INK, CY = g.BLUE, g.OK, g.BAD, g.GREY, g.INK, g.CYAN
# equipos
DY = 172
g.add(g.dev(48, DY, 270, 78, "Antel", "198.51.100.1", icon="antel"))
g.add(g.dev(465, DY - 10, 270, 98, "UCM6300", "LAN1 198.51.100.2", icon="ucm", dark=True, sub2="ExtHost 192.0.2.10"))
g.add(g.dev(882, DY, 270, 78, "Interno remoto", "por internet", icon="phone"))
WY = DY + 39
g.add(g.wire(318, WY, 465, WY, w=4))
g.add(g.wire(735, WY, 882, WY, w=4))

# la pregunta que se hace la UCM
QY = 352
g.add(g.box(300, QY, 600, 52, g.WHITE, g.LINE, rx=12))
g.add(g.text(600, QY + 33, "¿El destino está en Local Network Address?", 18, INK, g.SANS, 600, "middle"))

# la lista
LX, LY = 300, 418
g.add(g.box(LX, LY, 600, 108, g.SLATE, rx=12))
g.add(g.text(LX + 20, LY + 28, "Local Network Address", 15, GREY, g.MONO))
g.add(g.text(LX + 20, LY + 58, "192.168.88.0/24", 17, INK, g.MONO, 600))
g.appear(g.text(LX + 20, LY + 88, "198.51.100.0/30", 17, OK, g.MONO, 600), 52, 100)
g.appear(g.text(LX + 220, LY + 88, "203.0.113.0/24", 17, OK, g.MONO, 600), 54, 100)
g.appear(g.pill(LX + 430, LY + 66, "+ redes de Antel", OK, g.OKBG, 14, 28), 52, 100)

def sdp(cx, ip, col):
    return (g.box(cx - 120, 268, 240, 40, "#03213C", rx=10)
            + g.text(cx, 294, f"c={ip}", 15, col, g.MONO, 600, "middle"))

INV = g.chip("INVITE", bg=B, size=13, h=24)
# 1 · hacia el remoto
g.token([(735, WY), (882, WY)], 4, 10, INV)
g.appear(sdp(1017, "192.0.2.10", "#9BE7C4"), 10, 100)
g.appear(g.pill(1017, 316, "no está → External Host", GREY, g.SLATE, 13, 26, "middle"), 10, 100)
g.appear(g.mark(860, 288, True, 14), 12, 100)
# 2 · hacia Antel, sin la red en la lista
g.token([(465, WY), (318, WY)], 29, 35, INV)
g.appear(sdp(183, "192.0.2.10", "#FFB4A8"), 35, 50, still=0)
g.appear(g.pill(183, 316, "no está → External Host", BAD, g.BADBG, 13, 26, "middle"), 35, 50, still=0)
g.appear(g.mark(340, 288, False, 14), 37, 50, still=0)
# 3 · se suma la red
g.appear(g.box(LX - 6, LY - 6, 612, 120, "none", OK, rx=14, sw=3), 52, 75, still=0)
# 4 · hacia Antel, con la red en la lista
g.token([(465, WY), (318, WY)], 78, 84, INV)
g.appear(sdp(183, "198.51.100.2", "#9BE7C4"), 84, 100)
g.appear(g.pill(183, 316, "está → IP de LAN1", OK, g.OKBG, 13, 26, "middle"), 84, 100)
g.appear(g.mark(340, 288, True, 14), 86, 100)

# abajo
g.add(g.box(48, 546, 1104, 80, g.WHITE, g.LINE, rx=14))
ROWS = [(0, 25, "Use IP address in SDP: Sí · el remoto recibe c=192.0.2.10 y su audio vuelve por el router", OK),
        (25, 50, "Antel recibe c=192.0.2.10: manda el audio a una IP que en su red no existe", BAD),
        (50, 75, "PBX Settings > SIP Settings > NAT · Local Network Address", INK),
        (75, 100, "Cada destino recibe la IP por la que la central lo alcanza", OK)]
for t0, t1, s, col in ROWS:
    g.appear(g.text(72, 594, s, 17, col, g.SANS, 600), t0, t1)

g.done(21, "t1", "Qué IP anuncia la central en la c=",
       "Animación en cuatro tiempos. A la izquierda Antel en 198.51.100.1, al medio la UCM con LAN1 198.51.100.2 y External Host 192.0.2.10, "
       "a la derecha un interno remoto por internet; abajo la pregunta que se hace la central, si el destino está en Local Network Address, y la lista, que tiene 192.168.88.0/24. "
       "1: hacia el remoto, el destino no está en la lista y la UCM pone External Host en la c=, 192.0.2.10: está bien, el audio del remoto vuelve por el router. "
       "2: hacia Antel tampoco está en la lista y le anuncia la misma IP pública: Antel manda su audio a una IP que en su red no existe. "
       "3: se suman a Local Network Address las redes de Antel, 198.51.100.0/30 y 203.0.113.0/24, en PBX Settings > SIP Settings > NAT. "
       "4: hacia Antel ahora la c= lleva 198.51.100.2, la IP de LAN1, y el remoto sigue recibiendo External Host: cada destino recibe la IP por la que la central lo alcanza. Datos de ejemplo.",
       [6, 16, 30, 42, 58, 80, 90, 97])
