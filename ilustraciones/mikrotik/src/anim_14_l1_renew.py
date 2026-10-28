#!/usr/bin/env python3
"""Lección 14 · Laboratorio, paso 3: /ip/dhcp-client/renew. Con el lease vigente, el cliente pide renovar al mismo
servidor (Request) y el Ack reinicia el lease. Si la renovación no sale, el cliente reinicia el pedido como si no
tuviera dirección. Fuentes: DHCP de RouterOS (renew, status) y RFC 2131 (renovación con Request al servidor)."""
from _anim_red_1_9 import *

a = Anim(T=24, kicker="MIKROTIK · CLIENTE DHCP · LABORATORIO", title="renew: pedir otra vez sin esperar a la mitad")
a.steps([
    "El cliente está bound: tiene 192.168.1.10 y el lease va corriendo.",
    "renew: le pide al mismo servidor que le renueve esa dirección.",
    "El servidor contesta Ack: el lease vuelve a empezar, con la misma dirección.",
    "Si nadie contesta, el cliente arranca de cero, como si no tuviera dirección.",
], still=2)

CL, SV = 230, 760
a.add(dev(a, 48, 178, 364, 78, "MikroTik · dhcp-client", "ether1", icon="server", dark=True))
a.add(dev(a, 600, 178, 320, 78, "Módem", "servidor DHCP · 192.168.1.1", icon="server"))
a.add(lifeline(a, CL, 256, 520))
a.add(lifeline(a, SV, 256, 520))

msg(a, CL, SV, 330, "Request", 28, end=75, still=1, sub="renovar 192.168.1.10")
msg(a, SV, CL, 390, "Ack", 52, color=a.OK, end=75, still=1, sub="lease nuevo")
msg(a, CL, SV, 330, "Request", 77, end=100, still=0, dash="8 6", color=a.AMB)
a.add(during(a, xmark(a, SV - 30, 330), 81, 100))
msg(a, CL, SV, 450, "Discover · broadcast", 88, end=100, still=0)

# estado
SX = 960
a.add(a.text(SX, 210, "status", 15, a.GREY, a.MONO))
pill_at(a, SX, 222, "bound", a.OK, a.OKBG, 0, 77, still=1)
pill_at(a, SX, 222, "renovando…", a.AMB, a.AMBBG, 77, 86)
pill_at(a, SX, 222, "searching...", a.BAD, a.BADBG, 86, 100)
a.add(during(a, a.text(SX, 290, "address", 15, a.GREY, a.MONO) + a.text(SX, 314, "192.168.1.10/24", 16, a.INK, a.MONO, 600), 0, 86, still=1))

# barra del lease
LX, LY, LW = 48, 548, 872
a.add(a.text(LX, LY - 12, "lease", 15, a.GREY, a.MONO))
a.add(a.text(LX + LW / 2, LY - 12, "mitad", 15, a.BLUE, a.MONO, 600, "middle"))
a.add(a.text(LX + LW, LY - 12, "vence", 15, a.BAD, a.MONO, 600, "end"))
a.add(a.box(LX, LY, LW, 16, "#E6EDF4", rx=8))
k = a.keyframes([(0, 0.18), (54, 0.36), (55.5, 0.01), (77, 0.12), (100, 0.2)], "transform", "scaleX({})")
a.add(a.group(a.group(a.box(LX, LY, LW, 16, a.BLUE, rx=8), k, still=None, origin=f"{LX}px {LY}px"), a.show(0, 100), still=0))
a.add(still_only(a, a.box(LX, LY, LW * 0.03, 16, a.BLUE, rx=8)))
a.add(f'<line x1="{LX + LW / 2}" y1="{LY - 4}" x2="{LX + LW / 2}" y2="{LY + 20}" stroke="{a.BLUE}" stroke-width="2.5"/>')
a.add(during(a, a.text(LX, LY + 46, "sin renew, el cliente renueva solo al llegar a la mitad", 15, a.TXT, a.SANS, 600), 0, 52))
a.add(during(a, a.text(LX, LY + 46, "con el Ack, el lease arranca de nuevo", 15, a.OK, a.SANS, 600), 56, 77, still=1))
a.add(during(a, a.text(LX, LY + 46, "si el lease vence, se borran la dirección y la ruta dinámica", 15, a.BAD, a.SANS, 600), 86, 100))

# terminal
TX, TY, TW = 960, 380, 192
a.add(a.box(TX - 10, TY, TW + 10, 118, a.INK, rx=14))
a.add(a.text(TX + 6, TY + 34, "/ip/dhcp-client/", 15, a.WHITE, a.MONO))
a.add(a.text(TX + 6, TY + 60, "renew [find", 15, a.WHITE, a.MONO))
a.add(a.text(TX + 6, TY + 86, "interface=ether1]", 15, a.WHITE, a.MONO))
a.add(during(a, a.box(TX - 12, TY - 2, TW + 14, 122, "none", GOLD, rx=15, sw=3), 24, 36))

write(a, 14, "l1", "Qué hace renew en el cliente DHCP",
      "Animación en cuatro tiempos entre el cliente DHCP del MikroTik en ether1 y el servidor DHCP del módem (192.168.1.1), con el estado del cliente y una barra del lease. "
      "1: el cliente está bound con 192.168.1.10/24 y el lease va corriendo; sin renew, renueva solo al llegar a la mitad. "
      "2: /ip/dhcp-client/renew [find interface=ether1] hace que pida al mismo servidor, con un Request, renovar esa dirección. "
      "3: el servidor contesta Ack y el lease vuelve a empezar con la misma dirección. "
      "4: si la renovación no sale, el cliente arranca el pedido de cero con un Discover por broadcast, como si no tuviera dirección, y el estado pasa a searching; "
      "si el lease vence, se borran la dirección y la ruta dinámica.",
      [10, 36, 62, 92])
