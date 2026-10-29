#!/usr/bin/env python3
"""Lección 9 · teoría: cómo se actualiza el DDNS de IP Cloud y de dónde sale public-address."""
from _anim_mikrotik_1_13 import *

a = Anim(T=24, kicker="MIKROTIK · CÓMO FUNCIONA", title="IP Cloud: el servidor anota la IP desde la que le llegás")
a.steps([
    "Con ddns-enabled=yes, el router avisa a cloud2.mikrotik.com por UDP 15252.",
    "El servidor ve desde qué IP llega y actualiza el nombre, con TTL de 60 s.",
    "Esa IP vuelve como public-address. Si no es la de tu WAN, hay un NAT antes.",
    "Si el router no ve su IP pública en sus interfaces, avisa una vez por minuto.",
], still=2)

Y, LY = 250, 344
# paquetes primero: las cajas los tapan al pasar
seg1 = [(170, LY), (500, LY)]
seg2 = [(500, LY), (1030, LY)]


def update(t0, still=0):
    a.add(travel(a, pkt(a, "de 192.168.1.2", a.BLUE, size=14), seg1, t0, t0 + 4, hold=0.2, still=0))
    a.add(travel(a, pkt(a, "de 203.0.113.10", a.CYAN, size=14), seg2, t0 + 4.2, t0 + 9, hold=1.5, still=0))


a.add(line(170, LY, 1030, LY, a.LINE, 2, "3 7"))
a.add(a.text(48, LY + 5, "UDP", 13, a.GREY, a.MONO))
a.add(a.text(48, LY + 23, "15252", 13, a.GREY, a.MONO))
update(6)
update(77)
update(88)
a.add(still_only(a, place(a, pkt(a, "de 192.168.1.2", a.BLUE, size=14), 330, LY) + place(a, pkt(a, "de 203.0.113.10", a.CYAN, size=14), 760, LY)))
a.add(line(278, Y, 380, Y, a.BLUE, 3))
a.add(line(610, Y, 900, Y, a.LINE, 3, "6 6"))
a.add(a.text(755, Y - 16, "internet", 13, a.GREY, a.MONO, 400, "middle"))

a.add(device(a, 48, 196, 230, 110, "MikroTik", "WAN 192.168.1.2", sub2="ddns-enabled=yes", dark=True))
a.add(device(a, 380, 196, 230, 110, "Módem del proveedor", "NAT", sub2="sale con 203.0.113.10", tsize=17))
a.add(device(a, 900, 196, 252, 110, "cloud2.mikrotik.com", "servidor de IP Cloud", tsize=17))
a.add(during(a, a.text(500, LY + 44, "el NAT cambia el origen", 14, a.AMB, a.MONO, 600, "middle"), 9, 25))

# nombre DNS
a.add(a.box(712, 404, 440, 110, a.WHITE, a.LINE))
a.add(a.text(730, 434, "dns-name", 14, a.GREY, a.MONO))
a.add(a.text(730, 464, "<serie>.sn.mynetname.net", 17, a.INK, a.MONO, 600))
a.add(during(a, a.text(730, 494, "→ 203.0.113.10 · TTL 60 s", 16, a.OK, a.MONO, 600), 26, 100, still=1))
a.add(during(a, a.box(708, 400, 448, 118, "none", a.OK, rx=16, sw=2.5), 26, 50))

# lo que ve el router
a.add(a.box(48, 404, 610, 110, a.INK))
a.add(a.text(66, 436, "/ip/cloud/print", 14, SKY, a.MONO))
a.add(during(a, a.text(66, 466, "public-address: 203.0.113.10", 16, a.WHITE, a.MONO, 600), 51, 100, still=1))
a.add(a.text(66, 496, "IP de la WAN:   192.168.1.2", 16, a.WHITE, a.MONO, 600))
a.add(during(a, a.pill(640, 470, "distintas: hay un NAT antes", a.INK, GOLD, 14, 30, "end"), 54, 100, still=1))
a.add(during(a, a.text(600, 560, "una actualización por minuto mientras siga detrás de NAT", 16, a.AMB, a.SANS, 600, "middle"), 77, 98.5))

a.add(a.text(48, 630, "El nombre solo dice dónde está el router: no abre ningún puerto. El firewall sigue decidiendo.", 16, a.TXT, a.SANS, 600))

p, pre = out(9, 1)
a.write(p, title="Cómo se actualiza el DDNS de IP Cloud",
        desc="Animación en cuatro tiempos. Un MikroTik con WAN 192.168.1.2 detrás del NAT de un módem que sale con 203.0.113.10, y el servidor cloud2.mikrotik.com. "
             "1: con ddns-enabled=yes, el router manda una actualización por UDP 15252; al pasar por el módem el origen cambia a 203.0.113.10. 2: el servidor ve esa IP y "
             "actualiza <serie>.sn.mynetname.net a 203.0.113.10 con TTL de 60 segundos. 3: el router recibe esa IP como public-address; como no coincide con la IP de la "
             "WAN, hay un NAT antes. 4: como no ve su IP pública en sus interfaces, el router repite la actualización una vez por minuto. El nombre no abre ningún puerto.",
        preview=[6, 40, 62, 92], prefix=pre)
