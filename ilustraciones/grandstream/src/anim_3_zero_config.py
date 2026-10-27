#!/usr/bin/env python3
"""Lección 3 · teoría: Zero Config de punta a punta (descubrimiento, armado del XML, entrega, registro)."""
from _anim_grandstream import G

g = G(T=26, fix=94, kicker="GRANDSTREAM · ZERO CONFIG", title="Del teléfono reseteado a la extensión registrada")
g.steps([
    "Descubrimiento: SUBSCRIBE a multicast, y la UCM contesta NOTIFY con la URL.",
    "Armado: la UCM junta las plantillas por prioridad y la cuenta asignada.",
    "Entrega: el teléfono baja el XML por TFTP, HTTP o HTTPS y lo aplica.",
    "Registro: el teléfono registra su cuenta con lo que le llegó.",
])

XT, XU = 150, 600
g.lane(XT, 176, 636, "Teléfono", "GRP26xx de fábrica", w=230)
g.lane(XU, 176, 636, "UCM", "Zero Config", w=230)

# 1 descubrimiento
g.msg(XT, XU, 280, "SUBSCRIBE · multicast LAN", g.BLUE, 2, 9, tok="SUBSCRIBE")
g.msg(XU, XT, 330, "NOTIFY · URL del XML", g.CYAN, 13, 19, tok="NOTIFY")
g.appear(g.text(XT + 225, 362, "o la URL en DHCP opción 66 (UCM en Route)", 14, g.GREY, g.MONO, 400, "middle"), 17, 100)

# 3 entrega
g.msg(XT, XU, 422, "pide el XML · TFTP, HTTP o HTTPS", g.BLUE, 52, 58)
g.msg(XU, XT, 470, "XML", g.CYAN, 60, 66, tok="XML")
g.appear(g.pillc(XT, 498, "aplica", g.AMB, g.AMBBG), 68, 100)

# 4 registro
g.msg(XT, XU, 556, "REGISTER 1001", g.BLUE, 76, 80)
g.msg(XU, XT, 600, "200 OK", g.OK, 82, 86)
g.appear(g.mark(XT + 140, 626, True, 13) + g.text(XT + 160, 631, "1001 registrada", 15, g.OK, g.SANS, 600), 87, 100)

# 2 armado (panel derecho)
PX, PW = 770, 382
g.add(g.text(PX, 196, "Armado del XML en la UCM", 18, g.INK, g.HEAD, 600))
rows = [
    ("Model Template", "por modelo · gana si choca", g.BLUE, 27),
    ("Global Template", "para todos los equipos", g.BLUE, 30),
    ("Global Policy", "español · hora de Montevideo", g.BLUE, 33),
    ("Cuenta asignada", "cuenta 1 → extensión 1001", g.OK, 36),
]
for i, (t, sub, col, at) in enumerate(rows):
    y = 212 + i * 62
    g.add(g.box(PX, y, PW - 54, 52, g.WHITE, g.LINE, rx=12))
    g.add(g.text(PX + 18, y + 22, t, 17, g.INK, g.SANS, 600))
    g.add(g.text(PX + 18, y + 42, sub, 14, g.GREY, g.MONO))
    g.appear(g.box(PX, y, PW - 54, 52, "none", col, rx=12, sw=3), at, 50)
g.arrow([(PX + 164, 452), (PX + 164, 486)], 38, 42, g.BLUE)
# flecha de prioridad
g.add(g.parrow(f"M{PX + PW - 8} 386 V216", g.GREY, 2))
g.add(g.text(PX + PW + 4, 206, "más prioridad", 13, g.GREY, g.MONO, 400, "end"))
# XML resultante
g.add(g.box(PX, 488, PW - 54, 58, g.INK, None, rx=12))
g.add(g.text(PX + 18, 513, "XML del teléfono", 17, g.WHITE, g.SANS, 600))
g.appear(g.text(PX + 18, 535, "listo para servir", 14, "#9FC3E3", g.MONO), 44, 100)
g.appear(g.text(PX + 18, 535, "armándose…", 14, "#9FC3E3", g.MONO), 25, 44)
g.add(g.note(PX, 562, PW, None, ["Lo tocado a mano en el teléfono queda", "por encima de cualquier plantilla."], "amb"))

g.finish(3, 1, "Del teléfono reseteado a la extensión registrada",
         "Animación en cuatro tiempos con dos líneas de vida, un teléfono GRP26xx reseteado de fábrica y la UCM con Zero Config, y un panel con el armado del XML. "
         "1, descubrimiento: el teléfono manda SUBSCRIBE a una dirección multicast de la LAN y la UCM contesta NOTIFY con la URL del XML; con la UCM en Route la URL también puede llegar en la opción 66 del DHCP. "
         "2, armado: la UCM junta Model Template, Global Template y Global Policy (español y hora de Montevideo), de mayor a menor prioridad, y la cuenta asignada, cuenta 1 con la extensión 1001, en el XML del teléfono. "
         "3, entrega: el teléfono pide el XML por TFTP, HTTP o HTTPS, lo recibe y lo aplica. "
         "4, registro: el teléfono manda REGISTER 1001, la UCM responde 200 OK y la extensión queda registrada. "
         "Nota: lo que se configuró a mano en el teléfono queda por encima de cualquier plantilla.",
         [8, 36, 62, 94])
