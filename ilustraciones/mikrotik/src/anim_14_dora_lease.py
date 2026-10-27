#!/usr/bin/env python3
"""Lección 14 · Cliente DHCP. Teoría "Cómo funciona": los cuatro mensajes, lo que viene en el Ack y la renovación.
  1. Discover por broadcast.  2. Offer.  3. Request y Ack: bound.
  4. Se instala lo del Ack (dirección, ruta, DNS, NTP).  5. A mitad del lease, renueva; si vence, se borra.
"""
from _anim_mikrotik_14_26 import Anim, node, lifeline, msg, bar, out

a = Anim(T=24, kicker="MIKROTIK · CLIENTE DHCP", title="Cuatro mensajes, y lo que instala el Ack")
a.steps([
    "Discover: el cliente grita por broadcast buscando un servidor.",
    "Offer: el servidor contesta con una dirección para ofrecer.",
    "Request y Ack: el cliente pide esa oferta y el servidor confirma.",
    "Con el Ack se instalan dirección, ruta por defecto, DNS y NTP.",
    "A mitad del lease pide renovar. Si vence sin renovar, se borran dirección y rutas.",
], still=3)

CX, SX = 160, 600
a.add(node(a, 48, 178, 224, 72, "MikroTik", "dhcp-client · ether1"))
a.add(node(a, 488, 178, 224, 72, "Módem u otro router", "servidor DHCP"))
a.add(lifeline(a, CX, 250, 520))
a.add(lifeline(a, SX, 250, 520))

msg(a, CX, SX, 300, "Discover", 3, sub="broadcast: ¿hay algún servidor?")
msg(a, SX, CX, 368, "Offer", 23, sub="te ofrezco una dirección")
msg(a, CX, SX, 436, "Request", 43, sub="quiero esa")
msg(a, SX, CX, 500, "Ack", 51, color=a.OK)

# estado del cliente
a.add(a.text(48, 556, "estado", 15, a.GREY, a.MONO))
a.add(a.group(a.pill(118, 536, "sin dirección", a.GREY, "#E6EDF4", 15), a.show(0, 53), still=0))
a.add(a.group(a.pill(118, 536, "bound", a.OK, a.OKBG, 15), a.show(53, 100), still=1))

# panel: lo que viene en el Ack
PX, PY, PW = 752, 178, 400
a.add(a.box(PX, PY, PW, 396, a.WHITE, a.LINE, rx=18))
a.add(a.text(PX + 24, PY + 38, "Lo que viene en el Ack", 20, a.INK, a.HEAD, 600))
rows = [
    ("dirección y máscara", "dinámica en ether1"),
    ("gateway · opción 3", "ruta 0.0.0.0/0 · distancia 1"),
    ("DNS · opción 6", "si use-peer-dns=yes"),
    ("NTP · opción 42", "si use-peer-ntp=yes"),
    ("tiempo de lease", "cuánto dura el préstamo"),
]
for i, (k, v) in enumerate(rows):
    y = PY + 62 + i * 64
    a.add(a.box(PX + 16, y, PW - 32, 54, a.SLATE, rx=10))
    a.add(a.text(PX + 32, y + 23, k, 16, a.INK, a.MONO, 600))
    a.add(a.text(PX + 32, y + 44, v, 15, a.TXT))
    on = 61 + i * 2.5
    a.add(a.group(a.box(PX + 16, y, PW - 32, 54, "none", a.OK, rx=10, sw=2.5)
                  + a.text(PX + PW - 30, y + 23, "instalado", 15, a.OK, a.MONO, 600, "end"),
                  a.show(on, 80), still=1 if i < 4 else 0))

# barra del lease (paso 5), abajo a la izquierda
LX, LY, LW = 330, 548, 382
a.add(a.text(LX, LY - 12, "lease", 15, a.GREY, a.MONO))
a.add(a.text(LX + LW / 2, LY - 12, "mitad: renew", 15, a.BLUE, a.MONO, 600, "middle"))
a.add(a.text(LX + LW, LY - 12, "vence", 15, a.BAD, a.MONO, 600, "end"))
a.add(a.box(LX, LY, LW, 14, "#E6EDF4", rx=7))
k = a.keyframes([(0, 0), (80, 0), (90, 0.5), (91.5, 0.5), (92.5, 0.02), (100, 0.02)], "transform", "scaleX({})")
a.add(a.group(a.group(a.box(LX, LY, LW, 14, a.BLUE, rx=7), k, still=None, origin=f"{LX}px {LY}px"), a.show(80, 100), still=0))
a.add(f'<line x1="{LX + LW / 2}" y1="{LY - 4}" x2="{LX + LW / 2}" y2="{LY + 18}" stroke="{a.BLUE}" stroke-width="2.5"/>')

BY = 636
a.add(a.group(a.text(48, BY, "Todo lo que llega en el Ack queda como dinámico: print detail muestra qué recibió el cliente.", 16, a.TXT, a.SANS, 600),
              a.show(0, 80), still=1))
a.add(a.group(a.text(48, BY, "Pasa el tiempo: a mitad del lease, el cliente pide renovar al mismo servidor y el lease vuelve a empezar.", 16, a.INK, a.SANS, 600),
              a.show(80, 91), still=0))
a.add(a.group(a.text(48, BY, "Si nadie contesta, más adelante prueba con cualquiera. Si el lease vence, se borran la dirección y las rutas dinámicas.", 16, a.BAD, a.SANS, 600),
              a.show(91, 100), still=0))

out(a, 14, 1, "DHCP: Discover, Offer, Request y Ack",
    "Animación en cinco tiempos entre el cliente DHCP del MikroTik en ether1 y el servidor del módem. "
    "1: el cliente manda Discover por broadcast. 2: el servidor contesta Offer con una dirección. "
    "3: el cliente pide esa oferta con Request y el servidor confirma con Ack; el estado pasa a bound. "
    "4: se instala lo que vino en el Ack: dirección y máscara dinámicas en ether1, ruta por defecto por el gateway de la opción 3 con distancia 1, "
    "DNS de la opción 6 si use-peer-dns=yes, NTP de la opción 42 si use-peer-ntp=yes, y el tiempo de lease. "
    "5: a mitad del lease el cliente pide renovar al mismo servidor; si nadie contesta y el lease vence, se borran la dirección y las rutas dinámicas.",
    [8, 30, 55, 72, 86, 95])
