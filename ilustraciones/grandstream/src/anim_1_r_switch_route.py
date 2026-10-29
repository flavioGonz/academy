#!/usr/bin/env python3
"""Lección 1 · Resumen, "Cómo se ve en la red": el modo de red decide quién le contesta el DHCP al teléfono
conectado al LAN de la UCM. En Switch el LAN es un puente y responde el router de la oficina (sin opción 66);
en Route la UCM es el DHCP de su red 192.168.2.0/24 y entrega la opción 66 con la URL de aprovisionamiento.
Fuentes: manual UCM630x (Network Settings, Method), guía Zero Config (DHCP OPTION 66, https://192.168.2.1:8089/zccgi/)."""
from _anim_gs_red import R

g = R(T=26, fix=73, kicker="GRANDSTREAM · PRIMER ARRANQUE · CÓMO SE VE EN LA RED",
      title="Switch o Route: quién le da la IP al teléfono")
g.steps([
    "Switch: el teléfono en el LAN pide IP por DHCP y el pedido cruza la UCM, como un switch.",
    "Contesta el router de la oficina: el teléfono queda en 192.168.88.0/24, sin opción 66.",
    "Route: el pedido llega a la UCM, que es el DHCP de su propia red, 192.168.2.0/24.",
    "La respuesta trae la opción 66 con la URL de aprovisionamiento: el teléfono va a la UCM.",
])

Y, H = 190, 96
YL = Y + H / 2
LANE = Y - 20
g.add(g.dev(48, Y, 262, H, "Router oficina", "192.168.88.1", icon="router", sub2="DHCP 192.168.88.0/24"))
g.add(g.box(430, Y, 340, H, g.INK, rx=14))
g.add(g.ico(446, Y + 16, "ucm", g.CYAN, 1.35))
g.add(g.text(492, Y + 40, "UCM6300", 19, g.WHITE, g.HEAD, 600))
g.add(g.text(442, Y + H - 16, "WAN", 14, g.SKY, g.MONO, 600))
g.add(g.text(758, Y + H - 16, "LAN", 14, g.SKY, g.MONO, 600, "end"))
g.add(g.dev(890, Y, 262, H, "Teléfono GRP", "en el puerto LAN", icon="tel"))
g.add(g.wire(310, YL, 430, YL, g.BLUE))
g.add(g.wire(770, YL, 890, YL, g.BLUE))
# modo
g.appear(g.pill(492, Y + 52, "Method: Switch", g.WHITE, "#0B4F8F", 14, 28), 0, 50)
g.appear(g.pill(492, Y + 52, "Method: Route", g.INK, g.GOLD, 14, 28), 50, 100)
g.appear(g.text(442, Y + H + 26, "WAN 192.168.88.20 · LAN puente", 15, g.GREY, g.MONO, 400), 0, 50)
g.appear(g.text(442, Y + H + 26, "WAN 192.168.88.20 · LAN 192.168.2.1 DHCP", 15, g.BLUE, g.MONO, 600), 50, 100)

# 1 · Discover en Switch: cruza la UCM
disc = g.chip("DHCP Discover", bg=g.BLUE, size=13, h=26)
g.token([(1000, LANE), (600, LANE), (180, LANE)], 3, 20, disc, hold=23)
# 2 · Offer del router
off = g.chip("Offer · Ack", bg=g.OK, size=13, h=26)
g.token([(180, LANE), (1000, LANE)], 28, 42, off, hold=48)
g.appear(g.pillc(1021, Y + H + 12, "IP 192.168.88.31", g.OK, g.OKBG, 13, 26), 42, 50)
# 3 · Discover en Route: se queda en la UCM
g.token([(1000, LANE), (700, LANE)], 53, 60, disc, hold=61)
g.appear(g.pillc(179, Y + H + 12, "no participa", g.GREY, g.SLATE, 13, 26), 56, 100)
off66 = g.chip("Offer + opción 66", bg=g.OK, size=13, h=26)
g.token([(700, LANE), (1000, LANE)], 63, 72, off66, hold=74)
g.appear(g.pillc(1021, Y + H + 12, "IP de 192.168.2.0/24", g.OK, g.OKBG, 13, 26), 72, 100)

# panel: lo que recibe el teléfono
PY = 348
g.appear(g.term(48, PY, 700, 196, "Respuesta DHCP que recibe el teléfono", [
    ("de: router 192.168.88.1", None),
    ("IP 192.168.88.31 · gateway 192.168.88.1", "#5BE0A5"),
    ("opción 66: no viene", "#F6C35B"),
    ("Zero Config: solo por SIP SUBSCRIBE", None),
], size=17, lh=30), 28, 50)
g.appear(g.term(48, PY, 700, 196, "Respuesta DHCP que recibe el teléfono", [
    ("de: UCM 192.168.2.1", None),
    ("IP de 192.168.2.0/24 · gateway 192.168.2.1", "#5BE0A5"),
    ("opción 66: https://192.168.2.1:8089/zccgi/", "#F6C35B"),
    ("el teléfono baja su configuración de ahí", None),
], size=17, lh=30), 63, 100)
g.appear(g.term(48, PY, 700, 196, "Respuesta DHCP que recibe el teléfono", [
    ("(esperando el pedido del teléfono…)", "#9FC3E3"),
], size=17, lh=30), 0, 28)
g.appear(g.term(48, PY, 700, 196, "Respuesta DHCP que recibe el teléfono", [
    ("(esperando el pedido del teléfono…)", "#9FC3E3"),
], size=17, lh=30), 50, 63)

# notas a la derecha
NX, NW = 776, 376
g.appear(g.note(NX, PY, NW, "Switch (de fábrica)", ["El LAN es un puente: la UCM no", "es el DHCP de esa red y no", "puede mandar la opción 66."], "info"), 0, 50)
g.appear(g.note(NX, PY, NW, "Route", ["La UCM tiene su red y su DHCP.", "Habilita la opción 66 y la", "defensa dinámica (Dynamic Defense)."], "ok"), 50, 100)

g.status(628, [
    (0, 25, "En Switch la UCM deja pasar el pedido: el DHCP de la oficina no la conoce.", g.INK),
    (25, 50, "Sin opción 66, el teléfono tiene que encontrar la UCM por SUBSCRIBE.", g.AMB),
    (50, 75, "En Route el pedido no sale del LAN: la UCM contesta.", g.INK),
    (75, 100, "Se decide con la central vacía: cambiarlo en producción corta la web y los teléfonos.", g.BAD),
])

g.done(1, "r1", "Switch o Route: quién le da la IP al teléfono",
       "Animación en cuatro tiempos con el router de la oficina (192.168.88.1, DHCP de 192.168.88.0/24), la UCM6300 con su WAN en 192.168.88.20 y un teléfono GRP conectado a su puerto LAN. "
       "1: con Method en Switch, el teléfono manda DHCP Discover y el pedido cruza la UCM, que hace de puente, hasta el router. "
       "2: contesta el router con Offer y Ack: el teléfono queda con 192.168.88.31 y gateway 192.168.88.1, y la opción 66 no viene; Zero Config solo puede encontrarlo por SIP SUBSCRIBE. "
       "3: con Method en Route, el LAN de la UCM es 192.168.2.1 con su propio DHCP; el Discover llega a la UCM y el router no participa. "
       "4: la UCM responde con una IP de 192.168.2.0/24 y la opción 66 https://192.168.2.1:8089/zccgi/, de donde el teléfono baja su configuración. "
       "Route también habilita Dynamic Defense. El modo se decide con la central vacía: cambiarlo en producción corta la web y los teléfonos.",
       [8, 36, 58, 68, 90])
