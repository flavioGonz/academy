#!/usr/bin/env python3
"""Caso de estudio · Audio en un sentido · Resumen ("Cómo se ve en la red"): 21-r1.svg.
El caso: troncal de Antel en modo Dual; se suman remotos con External Host 192.0.2.10 y Local Network Address
queda sin las redes de Antel. La UCM anuncia c=192.0.2.10 a Antel; el RTP de la oficina llega, el de Antel
se pierde: la oficina no oye al de afuera. Arreglo: las redes de Antel en Local Network Address. Datos de ejemplo.
"""
from _anim_gs_red import R

g = R(T=28, fix=94, kicker="GRANDSTREAM · CASO DE ESTUDIO · AUDIO EN UN SENTIDO", title="El caso en la red: la c= que manda la central")
g.steps([
    "Se suman remotos: External Host 192.0.2.10. Los remotos se oyen bien.",
    "Entra una llamada por Antel; la UCM contesta 200 OK con c=192.0.2.10.",
    "El audio de la oficina llega a Antel; el de Antel va a 192.0.2.10 y se pierde.",
    "Redes de Antel en Local Network Address: c=198.51.100.2 y audio de ida y vuelta.",
], size=17)

B, OK, BAD, GREY, INK, CY = g.BLUE, g.OK, g.BAD, g.GREY, g.INK, g.CYAN
NY = 190
g.add(g.box(36, NY - 26, 300, 132, "none", CY, rx=16, sw=2, extra='stroke-dasharray="7 6"'))
g.add(g.text(56, NY - 6, "red privada de Antel", 14, CY, g.MONO))
g.add(g.dev(56, NY + 10, 260, 78, "Antel", "198.51.100.1", icon="antel"))
g.add(g.dev(430, NY, 340, 98, "UCM6300 · Dual", "LAN1 198.51.100.2", icon="ucm", dark=True, sub2="ExtHost 192.0.2.10"))
g.add(g.dev(882, NY + 10, 270, 78, "Router del cliente", "remotos e internet", icon="router"))
g.add(g.wire(316, NY + 49, 430, NY + 49, w=4))
g.add(g.wire(770, NY + 49, 882, NY + 49, w=4))
g.add(g.text(373, NY + 38, "LAN1", 13, B, g.MONO, 600, "middle"))
g.add(g.text(826, NY + 38, "LAN2", 13, B, g.MONO, 600, "middle"))

# 1 · los remotos, bien
for t0 in (6, 13):
    g.token([(770, NY + 49), (882, NY + 49)], t0, t0 + 3, g.chip("RTP", bg=OK, size=12, h=22))
    g.token([(882, NY + 63), (770, NY + 63)], t0 + 1.5, t0 + 4.5, g.chip("RTP", bg=OK, size=12, h=22))
g.appear(g.pillc(1017, NY + 112, "remotos: audio de ida y vuelta", OK, g.OKBG, 13, 26), 5, 25, still=0)

# 2 · 200 OK con la c= equivocada
SY = 398
g.token([(430, NY + 49), (316, NY + 49)], 29, 35, g.chip("200 OK", bg=B, size=13, h=24))
g.appear(g.term(48, SY, 520, 92, "SDP del 200 OK que sale por LAN1", [("c=IN IP4 192.0.2.10", "#FFB4A8")]), 33, 76, still=0)
g.appear(g.term(48, SY, 520, 92, "SDP del 200 OK que sale por LAN1", [("c=IN IP4 198.51.100.2", "#9BE7C4")]), 78, 100)

# 3 · el audio: uno llega, el otro no
AY = NY + 120
for t0 in (52, 60, 67):
    g.token([(430, AY), (316, AY)], t0, t0 + 3, g.chip("RTP", bg=OK, size=12, h=22), hold=t0 + 3.6)
    g.token([(316, AY + 34), (392, AY + 34)], t0 + 1, t0 + 3.5, g.chip("RTP", bg=BAD, size=12, h=22), hold=t0 + 4)
g.appear(g.mark(412, AY + 34, False, 13), 54, 76, still=0)
g.appear(g.text(600, AY + 12, "la oficina → Antel: llega", 15, OK, g.SANS, 600, "middle"), 52, 76, still=0)
g.appear(g.text(600, AY + 40, "Antel → 192.0.2.10: se pierde", 15, BAD, g.SANS, 600, "middle"), 54, 76, still=0)

# 4 · arreglo
for t0 in (84, 90):
    g.token([(430, AY), (316, AY)], t0, t0 + 3, g.chip("RTP", bg=OK, size=12, h=22))
    g.token([(316, AY + 22), (430, AY + 22)], t0 + 1.5, t0 + 4.5, g.chip("RTP", bg=OK, size=12, h=22))
g.appear(g.text(600, AY + 26, "audio de ida y vuelta por LAN1", 15, OK, g.SANS, 600, "middle"), 80, 100)
g.fijo_only(f'<g transform="translate(373 {AY})">' + g.chip("RTP", bg=OK, size=12, h=22) + "</g>"
            + f'<g transform="translate(373 {AY + 22})">' + g.chip("RTP", bg=OK, size=12, h=22) + "</g>")

# panel derecho: Local Network Address
PX = 612
g.add(g.box(PX, SY, 540, 112, g.WHITE, g.LINE, rx=14))
g.add(g.text(PX + 20, SY + 30, "PBX Settings > SIP Settings > NAT", 14, B, g.MONO, 600))
g.add(g.text(PX + 20, SY + 60, "Local Network Address: 192.168.88.0/24", 16, INK, g.MONO, 600))
g.appear(g.text(PX + 20, SY + 90, "+ 198.51.100.0/30 · 203.0.113.0/24", 16, OK, g.MONO, 600), 78, 100)
g.appear(g.text(PX + 20, SY + 90, "sin las redes de Antel", 16, BAD, g.SANS, 600), 0, 76, still=0)

# abajo
PY = 540
g.add(g.box(48, PY, 1104, 88, g.WHITE, g.LINE, rx=14))
ROWS = [(0, 25, "Interno remoto: fuera de Local Network Address, External Host está bien", "el router reenvía 5060 y 10000 a 20000 hacia la central", OK),
        (25, 50, "Antel tampoco está en la lista: la UCM le anuncia la IP pública", "200 OK con c=IN IP4 192.0.2.10", BAD),
        (50, 76, "El de afuera oye a la oficina; la oficina no lo oye", "el audio de Antel va a una IP que desde su red no existe", BAD),
        (76, 100, "Sumar las redes de Antel a Local Network Address", "c=IN IP4 198.51.100.2 y dos flujos en RTP Streams", OK)]
for t0, t1, a, b, col in ROWS:
    g.appear(g.text(72, PY + 36, a, 17, INK, g.SANS, 600) + g.text(72, PY + 66, b, 16, col, g.MONO, 600), t0, t1)

g.done(21, "r1", "El caso en la red: la c= que manda la central",
       "Animación en cuatro tiempos. A la izquierda, en la red privada de Antel, Antel en 198.51.100.1; al medio la UCM6300 en modo Dual con LAN1 198.51.100.2 y External Host 192.0.2.10; "
       "a la derecha, por LAN2, el router del cliente hacia los remotos e internet. "
       "1: se suman internos remotos con External Host 192.0.2.10 y su audio va y viene bien, porque están fuera de Local Network Address. "
       "2: entra una llamada por la troncal de Antel y la UCM contesta 200 OK con c=IN IP4 192.0.2.10, porque Local Network Address tiene solo 192.168.88.0/24. "
       "3: el audio de la oficina llega a Antel por LAN1, pero el de Antel va a 192.0.2.10, que desde su red no existe, y se pierde: el de afuera oye a la oficina y la oficina no lo oye. "
       "4: con 198.51.100.0/30 y 203.0.113.0/24 sumadas a Local Network Address en PBX Settings > SIP Settings > NAT, el 200 OK lleva c=IN IP4 198.51.100.2 y el audio va y viene por LAN1. Datos de ejemplo.",
       [8, 20, 33, 46, 58, 70, 86, 94])
