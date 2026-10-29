#!/usr/bin/env python3
"""Lección 9 (Interno remoto) · Laboratorio, paso 3: Media > NAT activado en la extensión del remoto. El REGISTER
lleva adentro la IP privada del teléfono; el router de su casa cambia el origen; con NAT la UCM contesta a la IP y
el puerto de donde vino el paquete, no a lo que dice el mensaje. Fuentes: manual UCM630x (NAT de la extensión),
la lección (la central contesta a la dirección real de origen), RFC 3581 (responder al origen real), RFC 3261 (Via)."""
from _anim_gs_red import R

g = R(T=26, fix=88, kicker="GRANDSTREAM · INTERNO REMOTO · LABORATORIO",
      title="NAT en la extensión: contestar a donde vino el paquete")
g.steps([
    "El remoto manda REGISTER; adentro del mensaje escribe su IP privada, 192.168.1.50.",
    "El router de su casa cambia el origen: a la UCM llega desde 198.51.100.7:40312.",
    "Con NAT apagado, la UCM contestaría a lo que dice el mensaje: 192.168.1.50, no llega.",
    "Con NAT activado contesta a 198.51.100.7:40312: el router de la casa lo pasa y registra.",
])

Y, H = 190, 96
YL = Y + H / 2
g.add(g.dev(48, Y, 246, H, "Remoto", "GRP en su casa", icon="tel", sub2="192.168.1.50"))
g.add(g.dev(360, Y, 270, H, "Router casa", "WAN 198.51.100.7", icon="router"))
g.add(g.cloud(676, Y + 14, 110, 68))
g.add(g.dev(832, Y, 320, H, "UCM", "por 203.0.113.10:5060", icon="ucm", dark=True))
g.add(g.wire(294, YL, 360, YL, g.BLUE))
g.add(g.wire(630, YL, 676, YL, g.BLUE))
g.add(g.wire(786, YL, 832, YL, g.BLUE))

LANE = Y - 20
g.token([(171, LANE), (495, LANE)], 3, 12, g.chip("REGISTER", bg=g.BLUE, size=13, h=26), hold=14)
g.token([(495, LANE), (992, LANE)], 27, 38, g.chip("REGISTER desde 198.51.100.7:40312", bg=g.BLUE, size=13, h=26), hold=40)
g.token([(992, LANE), (700, LANE)], 53, 62, g.chip("200 OK → 192.168.1.50", bg=g.BAD, size=13, h=26), hold=64)
g.appear(g.mark(650, LANE, False, 14), 62, 75)
g.token([(992, LANE), (495, LANE), (171, LANE)], 77, 90, g.chip("200 OK → 198.51.100.7:40312", bg=g.OK, size=13, h=26), hold=92)
g.appear(g.pillc(171, Y + H + 12, "registrado", g.OK, g.OKBG, 13, 26), 90, 100)
g.appear(g.pillc(495, Y + H + 12, "sesión 40312 ↔ 192.168.1.50", g.INK, g.SLATE, 13, 26), 24, 100)

# lo que dice el mensaje y lo que ve la UCM
PY = 352
g.add(g.box(48, PY, 560, 176, "#03213C", None, rx=14))
g.add(g.text(68, PY + 32, "lo que dice adentro del REGISTER", 15, g.SKY, g.MONO))
g.add(g.text(68, PY + 74, "Via: SIP/2.0/UDP 192.168.1.50:5060", 16, g.GOLD, g.MONO, 600))
g.add(g.text(68, PY + 108, "Contact: <sip:1002@192.168.1.50>", 16, g.GOLD, g.MONO, 600))
g.add(g.text(68, PY + 150, "NAT no cambia lo que va escrito adentro", 15, "#D9E9F8", g.SANS, 600))
g.appear(g.box(58, PY + 52, 540, 66, "none", g.GOLD, rx=8, sw=2.5), 2, 25)

g.add(g.box(632, PY, 520, 176, g.WHITE, g.LINE, rx=14))
g.add(g.text(652, PY + 32, "de dónde llegó, según la UCM", 15, g.GREY, g.MONO))
g.appear(g.text(652, PY + 74, "origen 198.51.100.7:40312", 18, g.INK, g.MONO, 600), 38, 100)
g.appear(g.text(652, PY + 74, "(esperando el paquete)", 16, g.GREY, g.SANS), 0, 38)
g.appear(g.text(652, PY + 116, "Media > NAT: apagado", 16, g.BAD, g.MONO, 600) + g.text(652, PY + 148, "contesta a 192.168.1.50: se pierde", 15, g.BAD, g.SANS, 600), 50, 75)
g.appear(g.text(652, PY + 116, "Media > NAT: activado", 16, g.OK, g.MONO, 600) + g.text(652, PY + 148, "contesta al origen real: llega", 15, g.OK, g.SANS, 600), 75, 100)

g.status(612, [
    (0, 25, "El teléfono solo conoce su IP de la casa, y esa es la que escribe.", g.INK),
    (25, 50, "El router de la casa anota la sesión: lo que vuelva a 40312 va al teléfono.", g.INK),
    (50, 75, "192.168.1.50 es privada: la respuesta muere en el camino y el teléfono no registra.", g.BAD),
    (75, 100, "NAT viene activado: se revisa que siga así en la extensión del remoto.", g.OK),
])

g.done(9, "l1", "NAT en la extensión: contestar a donde vino el paquete",
       "Animación en cuatro tiempos con el interno remoto, un GRP en una casa con IP privada 192.168.1.50, el router de esa casa con WAN 198.51.100.7, internet y la UCM, a la que llega por 203.0.113.10:5060; abajo, lo que dice adentro el REGISTER y de dónde lo ve llegar la UCM. "
       "1: el remoto manda REGISTER y adentro escribe su IP privada: Via SIP/2.0/UDP 192.168.1.50:5060 y Contact con 192.168.1.50; NAT no cambia lo que va escrito adentro. "
       "2: el router de la casa cambia el origen y anota la sesión; el paquete llega a la UCM desde 198.51.100.7:40312. "
       "3: con Media > NAT apagado, la UCM contestaría a lo que dice el mensaje, 192.168.1.50, una IP privada: la respuesta se pierde y el teléfono no registra. "
       "4: con NAT activado, la UCM contesta 200 OK a 198.51.100.7:40312, el origen real; el router de la casa lo pasa al teléfono y queda registrado.",
       [8, 36, 64, 92])
