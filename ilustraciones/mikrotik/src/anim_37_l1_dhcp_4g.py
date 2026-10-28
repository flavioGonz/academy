#!/usr/bin/env python3
"""Lección 37 (Dos WAN: PPPoE + DHCP), Laboratorio paso 3: el cliente DHCP de ether2 toma dirección del router 4G
y cada dato del ACK va a un lugar distinto: la dirección a ether2, el router (opción 3) a una ruta en distancia 2,
y el DNS (opción 6) queda afuera por use-peer-dns=no."""
from _anims_10_19 import Anim, en, ventanas, fijo, dev, viaje, linea, narr, escribir, pill_c, place, marca, LIGHT, GOLD, MINT, CORAL, GHOST

a = Anim(T=24, kicker="MIKROTIK · LABORATORIO · PASO 3", title="Lo que trae el DHCP del 4G y dónde va cada dato")
a.steps([
    "El cliente de ether2 pide dirección: DISCOVER y OFFER.",
    "REQUEST y ACK: el 4G confirma la dirección y sus datos.",
    "Cada dato a su lugar: la ruta espera en distancia 2.",
    "En el print: status=bound, y una IP privada detrás del 4G.",
], still=2)

a.add(dev(a, 48, 172, 270, 90, "Router", "ether2 · cliente DHCP", None, dark=True))
a.add(dev(a, 882, 172, 270, 90, "Router 4G", "servidor DHCP", "wifi", sub2="192.168.8.1"))
a.add(linea(318, 217, 882, 217, a.LINE, 4))
L, R = (420, 217), (780, 217)
viaje(a, "DISCOVER", [L, R], 2, 8, bg=a.BLUE, size=14, hold=0.5)
viaje(a, "OFFER", [R, L], 11, 17, bg=a.OK, size=14, hold=0.5)
viaje(a, "REQUEST", [L, R], 27, 33, bg=a.BLUE, size=14, hold=0.5)
viaje(a, "ACK", [R, L], 36, 42, bg=a.OK, size=14, hold=1)
en(a, a.text(600, 192, "broadcast en ether2", 15, a.GREY, a.MONO, 400, "middle"), 0, 25)
en(a, a.text(600, 192, "lease confirmado", 15, a.OK, a.MONO, 600, "middle"), 42, 100, still=1)

# ---- el ACK
CX, CY, CW = 48, 290, 560
ack = a.box(CX, CY, CW, 222, a.INK, rx=16) + a.text(CX + 22, CY + 32, "Lo que trae el ACK (ejemplo)", 16, "#FFFFFF", a.HEAD, 600)
FIELDS = [("dirección", "192.168.8.100/24"), ("opción 3 · router", "192.168.8.1"), ("opción 6 · DNS", "192.168.8.1"), ("opción 51 · lease", "tiempo de préstamo")]
FY = [CY + 76, CY + 116, CY + 156, CY + 196]
for (k, v), y in zip(FIELDS, FY):
    ack += a.text(CX + 22, y, k, 15, LIGHT, a.MONO) + a.text(CX + 230, y, v, 17, "#FFFFFF", a.MONO, 600)
en(a, ack, 42, 100, still=1)
en(a, a.box(CX, CY, CW, 222, "none", "#C2D4E6", rx=16, sw=2, extra='stroke-dasharray="7 6"')
   + a.text(CX + CW / 2, CY + 118, "esperando el ACK…", 17, a.GREY, a.SANS, 600, "middle"), 0, 42)

# ---- a dónde va cada dato
DX, DW = 664, 488
DST = [("/ip/address", "192.168.8.100/24 en ether2", a.OK, a.OKBG),
       ("/ip/route", "0.0.0.0/0 gw 192.168.8.1 distance=2", a.AMB, a.AMBBG),
       ("/ip/dns", "no lo suma: use-peer-dns=no", a.GREY, GHOST)]
DY = [290, 368, 446]
for i, ((t, s, c, bg), y) in enumerate(zip(DST, DY)):
    box = a.box(DX, y, DW, 66, bg, c, rx=14, sw=2) + a.text(DX + 20, y + 28, t, 16, a.INK, a.MONO, 700) + a.text(DX + 20, y + 52, s, 15, a.INK, a.MONO)
    t0 = 52 + i * 6
    en(a, box, t0, 100, still=1)
    fy = FY[i if i < 2 else 2] - 6
    en(a, a.arrow(f"M{CX + CW + 4} {fy} C {CX + CW + 30} {fy}, {DX - 30} {y + 33}, {DX - 6} {y + 33}", c, 2.5), t0, 75, still=1)
en(a, a.text(DX + DW - 18, DY[1] + 28, "espera", 15, a.AMB, a.SANS, 700, "end"), 58, 100, still=1)
en(a, a.text(DX + DW - 18, DY[2] + 28, "ignorado", 15, a.GREY, a.SANS, 700, "end"), 64, 100, still=1)

# ---- el print
TY = 532
en(a, a.box(48, TY, 1104, 70, a.INK, rx=14)
   + a.text(68, TY + 28, "> /ip/dhcp-client/print detail where interface=ether2", 15, LIGHT, a.MONO)
   + a.text(68, TY + 54, "status=bound  address=192.168.8.100/24  gateway=192.168.8.1", 16, "#FFFFFF", a.MONO, 600), 76, 100)
en(a, a.box(48, TY, 1104, 70, a.WHITE, a.LINE, rx=14)
   + a.text(68, TY + 42, "Mientras las recursivas del PPPoE estén activas, esta ruta no trabaja.", 16, a.TXT, a.SANS, 600), 52, 76, still=1)

narr(a, [
    (0, 25, "Todavía no tiene IP: el pedido sale por broadcast en ether2.", a.TXT),
    (25, 50, "El ACK trae la dirección, el gateway, los DNS del 4G y el tiempo del préstamo.", a.TXT),
    (50, 75, "add-default-route=yes con default-route-distance=2: la ruta existe pero espera.", a.AMB),
    (75, 100, "192.168.x es doble NAT; 100.64.x, CGNAT: por el 4G sale todo y no entra nada.", a.AMB),
], still_idx=2)

escribir(a, "37-l1", "Lo que trae el DHCP del 4G",
         "Animación en cuatro tiempos del paso 3. Arriba, el router con el cliente DHCP en ether2 y el router 4G, servidor DHCP en 192.168.8.1. "
         "1: el cliente todavía no tiene IP y pide por broadcast: DISCOVER, y el 4G contesta OFFER. "
         "2: REQUEST y ACK; el ACK trae, como ejemplo, la dirección 192.168.8.100/24, la opción 3 router 192.168.8.1, la opción 6 DNS 192.168.8.1 y la opción 51 con el tiempo del préstamo. "
         "3: cada dato va a un lugar: la dirección a /ip/address en ether2; el router a una ruta 0.0.0.0/0 por 192.168.8.1 con distance=2, que espera mientras las recursivas del PPPoE estén activas; "
         "y el DNS no se suma porque use-peer-dns=no. "
         "4: /ip/dhcp-client/print detail where interface=ether2 muestra status=bound, address=192.168.8.100/24 y gateway=192.168.8.1; "
         "una dirección 192.168.x es doble NAT y una 100.64.x es CGNAT: por el 4G sale todo, pero no entra nada de afuera.",
         [6, 14, 40, 60, 70, 90])
