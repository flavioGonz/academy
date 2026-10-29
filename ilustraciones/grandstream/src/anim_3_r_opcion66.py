#!/usr/bin/env python3
"""Lección 3 · Resumen, "Cómo se ve en la red": el camino por DHCP opción 66 (la teoría muestra el de SUBSCRIBE).
El GRP reseteado pide IP, la UCM en Route le contesta con la URL de aprovisionamiento en la opción 66, el teléfono
baja su XML por HTTPS y registra la cuenta 1. Fuentes: guía Zero Config de Grandstream (DHCP OPTION 66: Route,
DISCOVER y OFFER con https://192.168.2.1:8089/zccgi/; TFTP/HTTP/HTTPS; SUBSCRIBE a multicast); RFC 2131 y 2132."""
from _anim_gs_red import R

g = R(T=26, fix=72, kicker="GRANDSTREAM · ZERO CONFIG · CÓMO SE VE EN LA RED",
      title="Opción 66: la dirección llega junto con la IP")
g.steps([
    "El GRP reseteado pide IP; la UCM en Route le contesta con la opción 66.",
    "El teléfono va a esa URL y baja su XML por HTTPS: cuenta, idioma y hora.",
    "Aplica el XML y registra la cuenta 1, la 1001: queda andando sin tocarlo.",
    "Si la UCM no es el DHCP (modo Switch), no hay opción 66: queda el SUBSCRIBE.",
])

XT, XU = 150, 600
g.lane(XT, 176, 612, "GRP26xx", "reseteado de fábrica", w=230)
g.lane(XU, 176, 612, "UCM en Route", "LAN 192.168.2.1", w=230)

g.msg(XT, XU, 270, "DHCP Discover", g.BLUE, 2, 8, tok="Discover")
g.msg(XU, XT, 318, "Offer · opción 66", g.OK, 10, 16, tok="Offer")
g.appear(g.text(375, 346, "(después Request y Ack)", 14, g.GREY, g.SANS, 400, "middle"), 17, 100)
g.msg(XT, XU, 396, "GET /zccgi/ (HTTPS)", g.BLUE, 28, 35, tok="HTTPS")
g.msg(XU, XT, 444, "XML del teléfono", g.OK, 38, 45, tok="XML")
g.msg(XT, XU, 520, "REGISTER 1001 (Digest)", g.BLUE, 53, 60, tok="REGISTER")
g.msg(XU, XT, 568, "200 OK", g.OK, 63, 69)
g.appear(g.pillc(XT, 590, "1001 registrada", g.OK, g.OKBG, 14, 28), 69, 100)

PX, PW = 790, 362
g.appear(g.term(PX, 186, PW, 168, "Offer de la UCM", [
    ("IP de 192.168.2.0/24", None),
    ("opción 66:", "#9FC3E3"),
    ("https://192.168.2.1:8089/zccgi/", "#F6C35B"),
], size=15, lh=28), 12, 100)
g.appear(g.note(PX, 372, PW, "El XML trae", ["cuenta 1: extensión 1001", "Global Policy: español,", "hora de Montevideo"], "ok"), 40, 100)
g.appear(g.note(PX, 186, PW, "Antes de la IP", ["El teléfono recién reseteado", "no sabe dónde está su central:", "lo pregunta al pedir dirección."], "info"), 0, 12)
g.appear(g.box(PX, 506, PW, 116, g.AMBBG, None, rx=10)
         + f'<rect x="{PX}" y="506" width="5" height="116" rx="2" fill="{g.AMB}"/>'
         + g.text(PX + 20, 536, "UCM en Switch", 17, g.AMB, g.SANS, 600)
         + g.text(PX + 20, 562, "El DHCP es el router de la oficina:", 16, g.TXT)
         + g.text(PX + 20, 584, "no trae opción 66. El teléfono la", 16, g.TXT)
         + g.text(PX + 20, 606, "encuentra por SIP SUBSCRIBE.", 16, g.TXT), 75, 100)

g.done(3, "r1", "Opción 66: la dirección llega junto con la IP",
       "Animación en cuatro tiempos con dos líneas de vida, un GRP26xx reseteado de fábrica y la UCM en modo Route con su LAN en 192.168.2.1, y un panel a la derecha. "
       "1: el teléfono manda DHCP Discover y la UCM contesta Offer con una IP de 192.168.2.0/24 y la opción 66 con la URL https://192.168.2.1:8089/zccgi/; después siguen Request y Ack. "
       "2: el teléfono va a esa URL por HTTPS y recibe su XML: cuenta 1 con la extensión 1001 y la Global Policy con español y hora de Montevideo. "
       "3: aplica el XML, manda REGISTER 1001 con Digest y la UCM responde 200 OK: la 1001 queda registrada sin tocar el teléfono. "
       "4: si la UCM está en Switch, el DHCP es el router de la oficina y la respuesta no trae opción 66; el teléfono encuentra a la central por SIP SUBSCRIBE.",
       [8, 40, 66, 90])
