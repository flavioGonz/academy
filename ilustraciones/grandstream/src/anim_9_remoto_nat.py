#!/usr/bin/env python3
"""Lección 9 · teoría: el interno remoto registra y habla a través del router de la oficina."""
from _anim_grandstream import G

g = G(T=26, fix=88, kicker="GRANDSTREAM · INTERNO REMOTO", title="Cómo cruza el NAT un interno que está afuera")
g.steps([
    "El remoto manda REGISTER a 203.0.113.10:5060; el router lo reenvía a la UCM.",
    "Con NAT activo en la extensión, la UCM contesta a la IP y el puerto de origen.",
    "En la llamada, la UCM anuncia en el SDP su External Host: 203.0.113.10.",
    "El remoto manda el RTP ahí, a un puerto de 10000 a 20000, y el router lo reenvía.",
])

LY = 270
g.add(g.node(48, 230, 210, 80, "Interno remoto", "afuera, por internet"))
g.add(g.node(870, 230, 282, 80, "UCM", "192.168.88.20", dark=True, tsize=22))
# router
RX, RW = 440, 360
g.add(g.box(RX, 196, RW, 232, g.WHITE, g.LINE, rx=16))
g.add(g.text(RX + 20, 226, "Router de la oficina", 18, g.INK, g.HEAD, 600))
g.add(g.text(RX + RW - 20, 226, "203.0.113.10", 16, g.BLUE, g.MONO, 600, "end"))
rules = ["UDP 5060 → 192.168.88.20", "UDP 10000-20000 → .20", "SIP ALG: apagado"]
for k, r in enumerate(rules):
    y = 318 + k * 36
    g.add(g.box(RX + 16, y, RW - 32, 30, g.SLATE, None, rx=8) + g.text(RX + 30, y + 21, r, 15, g.INK, g.MONO, 600))
g.appear(g.box(RX + 16, 318, RW - 32, 30, "none", g.BLUE, rx=8, sw=2.5), 5, 50)
g.appear(g.box(RX + 16, 354, RW - 32, 30, "none", g.OK, rx=8, sw=2.5), 76, 100)
g.add(f'<line x1="258" y1="{LY}" x2="870" y2="{LY}" stroke="{g.LINE}" stroke-width="3"/>')
g.add(g.text(350, LY + 28, "internet", 14, g.GREY, g.MONO, 400, "middle"))
g.add(g.text(835, LY + 28, "LAN", 14, g.GREY, g.MONO, 400, "middle"))

A, B = (258, LY), (870, LY)
g.token([A, B], 3, 16, g.chip("REGISTER → :5060", bg=g.BLUE, size=13, h=26), hold=17)
g.token([B, A], 27, 40, g.chip("200 OK", bg=g.OK, size=13, h=26), hold=41)
g.appear(g.pillc(1011, 334, "responde al origen real", g.OK, g.OKBG, 13, 26), 26, 50)
g.token([B, A], 52, 64, g.chip("INVITE + SDP", bg=g.CYAN, size=13, h=26), hold=65)
for k in range(4):
    g.token([A, B], 76 + k * 5, 84 + k * 5, g.chip("RTP", bg=g.OK, size=13, h=24), hold=84.4 + k * 5)
    g.token([B, A], 78.5 + k * 5, 86.5 + k * 5, g.chip("RTP", bg=g.OK, size=13, h=24), hold=86.9 + k * 5)
g.fijo_only(f'<g transform="translate(340 {LY})">' + g.chip("RTP", bg=g.OK, size=13, h=24) + "</g>"
            + f'<g transform="translate(830 {LY})">' + g.chip("RTP", bg=g.OK, size=13, h=24) + "</g>")

# ajustes de la UCM
g.add(g.box(870, 380, 282, 104, g.WHITE, g.LINE, rx=14))
for k, (n, v) in enumerate([("External Host", "203.0.113.10"), ("Local Network", "192.168.88.0/24"), ("NAT extensión", "sí")]):
    g.add(g.text(888, 410 + k * 28, n, 14, g.GREY, g.MONO) + g.text(1136, 410 + k * 28, v, 14, g.INK, g.MONO, 600, "end"))
g.appear(g.box(878, 392, 266, 26, "none", g.CYAN, rx=6, sw=2), 52, 100)

# SDP
SX, SY = 48, 460
g.add(g.box(SX, SY, 780, 150, "#03213C", None, rx=14))
g.add(g.text(SX + 20, SY + 30, "SDP que la UCM manda al remoto", 15, "#9FC3E3", g.MONO))
g.appear(g.text(SX + 20, SY + 70, "c=IN IP4 203.0.113.10", 20, "#5BE0A5", g.MONO, 600)
         + g.text(SX + 330, SY + 70, "← mandame el audio acá", 16, "#D9E9F8", g.SANS, 600)
         + g.text(SX + 20, SY + 108, "m=audio 10044 RTP/AVP 8 0", 20, "#D9E9F8", g.MONO, 600)
         + g.text(SX + 380, SY + 108, "← a este puerto", 16, "#D9E9F8", g.SANS, 600), 56, 100)
g.appear(g.text(SX + 20, SY + 76, "(todavía no hay llamada)", 16, "#9FC3E3", g.SANS), 0, 56)
g.appear(g.text(SX + 20, SY + 136, "A un interno de 192.168.88.0/24 le anunciaría 192.168.88.20.", 15, "#9FC3E3", g.SANS), 60, 100)

g.finish(9, 1, "Cómo cruza el NAT un interno que está afuera",
         "Animación en cuatro tiempos con el interno remoto en internet, el router de la oficina con IP pública 203.0.113.10 y la UCM en 192.168.88.20 dentro de la LAN. "
         "El router reenvía UDP 5060 y UDP 10000 a 20000 a la UCM y tiene el SIP ALG apagado. "
         "1: el remoto manda REGISTER a 203.0.113.10 puerto 5060 y el router lo reenvía a la UCM. "
         "2: con NAT activo en la extensión, la UCM responde 200 OK a la IP y el puerto de origen real del paquete. "
         "3: en la llamada, la UCM manda un INVITE con SDP que anuncia su External Host: c=IN IP4 203.0.113.10 y m=audio 10044 RTP/AVP 8 0; a un interno de 192.168.88.0/24 le anunciaría 192.168.88.20. "
         "4: el remoto manda el RTP a 203.0.113.10, a un puerto entre 10000 y 20000, el router lo reenvía a la UCM, y el audio viaja en los dos sentidos.",
         [10, 34, 62, 88])
