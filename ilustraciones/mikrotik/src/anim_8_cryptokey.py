#!/usr/bin/env python3
"""Lección 8 · teoría: ruteo por clave en WireGuard (allowed-address de ida y de vuelta) y el silencio ante lo desconocido."""
from _anim_mikrotik_1_13 import *

a = Anim(T=30, kicker="MIKROTIK · LECCIÓN 8 · CÓMO FUNCIONA", title="WireGuard: cada clave queda atada a su dirección")
a.steps([
    "Llega un paquete cifrado al UDP 13231: la clave es la de notebook-lucia.",
    "Adentro viene de 10.10.10.2: es el allowed-address de ese peer. Se acepta.",
    "La respuesta a 10.10.10.2 sale por ese mismo peer, cifrada con su clave.",
    "Si adentro viniera de 10.10.10.3, no es de ese peer: se descarta.",
    "Un escáner sin clave conocida: se descarta sin respuesta.",
], still=1)

# notebook y escáner
a.add(device(a, 48, 190, 250, 116, "Notebook de Lucía", "túnel 10.10.10.2/32", sub2="su clave privada"))
a.add(device(a, 48, 420, 250, 96, "Escáner", "sin clave conocida"))
NY, SY = 248, 468
a.add(line(298, NY, 690, NY, a.LINE, 3, "6 6"))
a.add(line(298, SY, 690, SY, a.LINE, 3, "6 6"))
a.add(a.text(494, NY - 30, "internet", 13, a.GREY, a.MONO, 400, "middle"))

# router
RX, RY, RW, RH = 690, 186, 462, 350
a.add(a.box(RX, RY, RW, RH, a.INK))
a.add(a.text(RX + 20, RY + 32, "Router · wg-gestion", 18, a.WHITE, a.SANS, 600))
a.add(a.text(RX + 20, RY + 56, "UDP 13231 · 10.10.10.1/24", 14, SKY, a.MONO))
a.add(a.text(RX + 20, RY + 92, "peer", 13, SKY, a.MONO))
a.add(a.text(RX + 250, RY + 92, "allowed-address", 13, SKY, a.MONO))
PR = [(RY + 104, "notebook-lucia", "10.10.10.2/32"), (RY + 152, "notebook-pablo", "10.10.10.3/32")]
for y, n, ip in PR:
    a.add(a.box(RX + 14, y, RW - 28, 40, "#0B3A66", rx=8))
    a.add(a.text(RX + 28, y + 26, n, 15, a.WHITE, a.MONO, 600))
    a.add(a.text(RX + 250, y + 26, ip, 15, a.WHITE, a.MONO))
ly = PR[0][0]
DY = RY + 232   # zona de decisión


def ring_peer(t0, t1, col, still=0):
    a.add(during(a, a.box(RX + 10, ly - 4, RW - 20, 48, "none", col, rx=10, sw=3), t0, t1, still=still))


def dline(t0, t1, l1, l2, col, still=0):
    a.add(during(a, a.text(RX + 20, DY + 26, l1, 15, col, a.MONO, 600) + a.text(RX + 20, DY + 52, l2, 15, SKY, a.MONO), t0, t1, still=still))


# 1. llega cifrado y se abre con la clave del peer
a.add(travel(a, pkt(a, "cifrado · UDP 13231", a.BLUE, size=14), [(400, NY), (590, NY)], 2, 9, hold=1))
ring_peer(9, 20, GOLD)
dline(9, 20, "cifrado con una clave conocida:", "la del peer notebook-lucia", GOLD)
# 2. adentro: origen 10.10.10.2 coincide
ring_peer(20, 40, MINT, still=1)
dline(20, 40, "adentro: origen 10.10.10.2", "coincide con su allowed-address: acepta", MINT, still=1)
# 3. respuesta por el mismo peer
ring_peer(42, 60, MINT)
dline(42, 60, "respuesta a 10.10.10.2", "peer con esa dirección: notebook-lucia", MINT)
a.add(travel(a, pkt(a, "cifrado para Lucía", a.OK, size=14), [(590, NY + 44), (400, NY + 44)], 46, 54, hold=4))
# 4. origen que no corresponde
a.add(travel(a, pkt(a, "cifrado · UDP 13231", a.BLUE, size=14), [(400, NY), (590, NY)], 61, 67, hold=1))
ring_peer(67, 80, a.BAD)
dline(67, 80, "adentro: origen 10.10.10.3", "no es el allowed-address de este peer: drop", "#FF9B85")
# 5. escáner
a.add(travel(a, pkt(a, "UDP 13231 · sin clave", a.BAD, size=14), [(410, SY), (600, SY)], 81, 87, hold=1))
a.add(during(a, xmark(a, RX - 26, SY), 87, 98.5))
dline(87, 98.5, "ninguna clave conocida lo abre", "se descarta sin contestar", "#FF9B85")
a.add(during(a, a.text(66, SY + 36, "no recibe nada", 15, a.OK, a.MONO, 600), 89, 98.5))

a.add(a.text(48, 590, "No hay usuario ni contraseña: la clave dice quién es, y allowed-address qué IP puede usar.", 16, a.INK, a.SANS, 600))
a.add(a.text(48, 620, "En la notebook, AllowedIPs hace lo mismo al revés: decide qué destinos van por el túnel.", 16, a.TXT, a.SANS))

p, pre = out(8, 1)
a.write(p, title="Ruteo por clave en WireGuard",
        desc="Animación en cinco tiempos. A la derecha, el router con la interfaz wg-gestion (UDP 13231, 10.10.10.1/24) y dos peers: notebook-lucia con "
             "allowed-address 10.10.10.2/32 y notebook-pablo con 10.10.10.3/32. 1: llega un paquete cifrado al UDP 13231 cifrado con la clave del peer notebook-lucia. "
             "2: adentro, el origen es 10.10.10.2, el allowed-address de ese peer: se acepta. 3: la respuesta a 10.10.10.2 sale por el peer que tiene esa dirección, "
             "cifrada para Lucía. 4: si por ese mismo peer llegara un paquete con origen 10.10.10.3, no corresponde y se descarta. 5: un escáner sin clave conocida "
             "manda al UDP 13231 y el router lo descarta sin contestar.",
        preview=[12, 30, 50, 72, 92], prefix=pre)
