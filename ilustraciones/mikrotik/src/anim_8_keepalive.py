#!/usr/bin/env python3
"""Lección 8 · teoría: el NAT del medio olvida la asociación y PersistentKeepalive = 25 la mantiene."""
from _anim_mikrotik_1_13 import *

a = Anim(T=24, kicker="MIKROTIK · LECCIÓN 8 · KEEPALIVE", title="PersistentKeepalive: que el NAT no se olvide del túnel")
a.steps([
    "La notebook manda al router: el NAT del medio anota la asociación.",
    "WireGuard no manda nada si no hay tráfico. A los minutos, el NAT la olvida.",
    "Lo que manda el router desde afuera ya no encuentra camino: se pierde.",
    "Con PersistentKeepalive = 25, un paquete chico cada 25 s la mantiene viva.",
], still=3)

Y = 290
a.add(device(a, 48, 236, 220, 108, "Notebook", "app WireGuard", sub2="detrás de un NAT"))
a.add(device(a, 932, 236, 220, 108, "Router del cliente", "203.0.113.10", sub2="UDP 13231", ssize=13, dark=True))
a.add(line(268, Y, 420, Y, a.LINE, 3, "6 6"))
a.add(line(760, Y, 932, Y, a.LINE, 3, "6 6"))
a.add(a.text(846, Y - 18, "internet", 13, a.GREY, a.MONO, 400, "middle"))

# 1. la notebook manda
a.add(travel(a, pkt(a, "datos", a.BLUE, size=14), [(300, Y + 30), (870, Y + 30)], 2, 12, hold=2))
# 2. silencio
a.add(during(a, a.text(600, 420, "sin tráfico: WireGuard no manda nada", 16, a.GREY, a.SANS, 600, "middle"), 27, 50))
a.add(during(a, a.text(600, 452, "pasan unos minutos…", 16, a.AMB, a.MONO, 600, "middle"), 30, 50))
# 3. el router manda y se pierde
a.add(travel(a, pkt(a, "datos", a.OK, size=14), [(900, Y - 30), (812, Y - 30)], 52, 58, hold=1))
a.add(during(a, xmark(a, 784, Y - 30), 58, 75))
a.add(during(a, a.text(600, 420, "el NAT ya no sabe a quién entregarlo", 16, a.BAD, a.SANS, 600, "middle"), 58, 75))
# 4. keepalive
for t0 in (77, 85, 93):
    a.add(travel(a, pkt(a, "keepalive", a.CYAN, size=13, h=28), [(300, Y + 30), (860, Y + 30)], t0, t0 + 5, hold=0.3))
a.add(travel(a, pkt(a, "datos", a.OK, size=14), [(900, Y - 30), (300, Y - 30)], 87, 95, hold=3))
a.add(still_only(a, place(a, pkt(a, "keepalive", a.CYAN, size=13, h=28), 344, Y + 30) + place(a, pkt(a, "datos", a.OK, size=14), 846, Y - 30)))
a.add(during(a, a.text(600, 420, "cada 25 s pasa algo: la asociación no vence", 16, a.OK, a.SANS, 600, "middle"), 79, 100, still=1))

a.add(a.box(420, 206, 340, 168, a.WHITE, a.LINE))
a.add(a.text(440, 238, "Módem de tu casa o 4G", 17, a.INK, a.SANS, 600))
a.add(a.text(440, 262, "NAT · asociaciones UDP", 14, a.GREY, a.MONO))
a.add(a.box(436, 280, 308, 74, a.SLATE, rx=10))
a.add(a.text(452, 306, "notebook ↔ 203.0.113.10:13231", 14, a.INK, a.MONO, 600))
for t0, t1, lab, fg, bg, st in [(7, 40, "abierta", a.OK, a.OKBG, 0), (40, 79, "olvidada", a.BAD, a.BADBG, 0), (79, 100, "abierta", a.OK, a.OKBG, 1)]:
    a.add(during(a, a.pill(452, 318, lab, fg, bg, 13, 26), t0, t1, still=st))

a.add(term(a, 48, 488, 520, ["[Peer]", "Endpoint = 203.0.113.10:13231", "PersistentKeepalive = 25"], title="NOTEBOOK · WIREGUARD", size=15))
a.add(a.box(54, 574, 508, 28, "none", MINT, rx=6, sw=2))
a.add(note(a, 612, 488, 540, 124, "Por qué hace falta", ["WireGuard no mantiene una conexión abierta.", "El NAT del medio olvida la asociación a los", "pocos minutos sin tráfico."], "amb"))

p, pre = out(8, 2)
a.write(p, title="PersistentKeepalive y el NAT del medio",
        desc="Animación en cuatro tiempos con una notebook detrás del NAT de un módem o de un 4G y el router del cliente en 203.0.113.10, UDP 13231. "
             "1: la notebook manda datos al router y el NAT anota la asociación como abierta. 2: sin tráfico, WireGuard no manda nada y a los pocos minutos el NAT "
             "olvida la asociación. 3: lo que manda el router desde afuera llega al NAT, que ya no sabe a quién entregarlo, y se pierde. 4: con PersistentKeepalive = 25, "
             "la notebook manda un paquete chico cada 25 segundos, la asociación sigue abierta y lo que manda el router llega.",
        preview=[10, 40, 64, 90], prefix=pre)
