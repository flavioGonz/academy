#!/usr/bin/env python3
"""Lección 10 · NVR con criterio · Resumen ("Cómo se ve en la red").
La central de la lista llega al NVR; un escáner de internet prueba el 8000 y los puertos del router y no recibe nada.
"""
from _anim_mk_32_39 import *

a = Anim(T=24, kicker="MIKROTIK · NVR CON CRITERIO · CÓMO SE VE EN LA RED", title="Quién llega al NVR y quién no")
a.steps([
    "La central (en nvr-permitidos) manda un SYN al 8000: el dst-nat lo lleva al NVR.",
    "El NVR contesta y el router deshace el cambio: la central ve a 203.0.113.10.",
    "Un escáner prueba el 8000. No está en la lista: la regla no se aplica e input lo tira.",
    "Prueba 8291 y 80, puertos del router: nada publicado, drop y sin respuesta.",
], still=0, size=17)

L1, L2 = 352, 500   # carriles: central y escáner
RX, RY, RW, RH = 360, 176, 480, 372

# router (abajo de los paquetes)
a.add(a.box(RX, RY, RW, RH, a.INK, rx=18))
a.add(a.text(RX + 20, RY + 30, "MikroTik · ether1 203.0.113.10", 17, a.WHITE, a.SANS, 600))
a.add(a.box(RX + 20, 218, RW - 40, 104, a.NAVY2, rx=12))
a.add(a.text(RX + 38, 244, "/ip/firewall/nat · dstnat", 15, SKY, a.MONO))
a.add(a.text(RX + 38, 268, "in-interface-list=WAN dst-port=8000", 15, a.WHITE, a.MONO))
a.add(a.text(RX + 38, 290, "src-address-list=nvr-permitidos", 15, GOLD, a.MONO, 600))
a.add(a.text(RX + 38, 312, "→ to-addresses=192.168.88.50", 15, a.WHITE, a.MONO))
a.add(a.box(RX + 20, 386, RW - 40, 82, a.NAVY2, rx=12))
a.add(a.text(RX + 38, 412, "/ip/firewall/filter · input", 15, SKY, a.MONO))
a.add(a.text(RX + 38, 438, "defconf: drop all not coming", 15, a.WHITE, a.MONO))
a.add(a.text(RX + 38, 460, "from LAN", 15, a.WHITE, a.MONO))
# carriles
a.add(line(298, L1, 930, L1, "#2E5C86", 3, "5 7"))
a.add(line(298, L2, RX, L2, a.LINE, 3, "5 7"))
a.add(line(RX, L2, 600, L2, "#2E5C86", 3, "5 7"))

# extremos
a.add(dev(a, 48, 300, 250, 100, "Central", "203.0.113.25", "server", sub2="en la lista"))
a.add(dev(a, 48, 450, 250, 100, "Escáner", "198.51.100.66", "globe", sub2="fuera de la lista"))
a.add(dev(a, 930, 300, 222, 100, "NVR", "192.168.88.50", "server", sub2="TCP 8000"))
a.add(a.pill(940, 420, "80, 443, 8291: del router,", a.BAD, a.BADBG, 14, 28))
a.add(a.pill(940, 454, "nunca se publican", a.BAD, a.BADBG, 14, 28))

# resaltados
a.add(during(a, a.box(RX + 16, 214, RW - 32, 112, "none", MINT, rx=14, sw=3.5), 6, 14))
a.add(during(a, a.pill(RX + RW - 28, 226, "coincide", a.OK, a.OKBG, 14, 26, "end"), 6, 25))
a.add(during(a, a.box(RX + 16, 214, RW - 32, 112, "none", ROSE, rx=14, sw=3.5), 55, 62))
a.add(during(a, a.pill(RX + RW - 28, 226, "no coincide", a.BAD, a.BADBG, 14, 26, "end"), 55, 75, still=0))
a.add(wins(a, a.box(RX + 16, 382, RW - 32, 90, "none", ROSE, rx=14, sw=3.5), [(61, 75), (80, 99)]))

# 1. SYN de la central hasta el NVR
a.add(travel(a, pkt(a, "SYN :8000"), [(330, L1), (600, L1)], 1, 7, hold=6))
a.add(travel(a, pkt(a, "SYN :8000", a.OK), [(600, L1), (870, L1)], 13, 20, hold=4))
a.add(during(a, check(a, 1126, 326), 20, 50))
# 2. SYN-ACK de vuelta
a.add(travel(a, pkt(a, "SYN-ACK", a.OK), [(870, L1), (330, L1)], 27, 40, hold=3))
a.add(during(a, check(a, 272, 326), 41, 100, still=1))
# 3. escáner al 8000
a.add(travel(a, pkt(a, "SYN :8000", a.BAD), [(330, L2), (550, L2)], 51, 59, hold=4))
a.add(during(a, xmark(a, 640, L2), 62, 75))
# 4. escáner a los puertos del router
a.add(travel(a, pkt(a, "SYN :8291", a.BAD), [(330, L2), (550, L2)], 77, 82, hold=2))
a.add(travel(a, pkt(a, "SYN :80", a.BAD), [(330, L2), (550, L2)], 87, 92, hold=3))
a.add(wins(a, xmark(a, 640, L2), [(82, 86), (93, 100)]))
a.add(still_only(a, place(pkt(a, "SYN :8000", a.BAD), 480, L2) + xmark(a, 640, L2) + place(pkt(a, "SYN :8000", a.OK), 800, L1)))

# cabecera del paquete (abajo)
PY = 568
a.add(a.box(48, PY, 1104, 76, a.WHITE, a.LINE, rx=14))
HDR = [
    (0, 25, "de 203.0.113.25  a 203.0.113.10:8000", "dst-nat → a 192.168.88.50:8000", a.OK, 1),
    (25, 50, "de 192.168.88.50:8000  a 203.0.113.25", "sale como 203.0.113.10:8000", a.OK, 0),
    (50, 75, "de 198.51.100.66  a 203.0.113.10:8000", "sigue siendo para el router → drop", a.BAD, 0),
    (75, 100, "de 198.51.100.66  a 203.0.113.10:8291 y :80", "drop: no recibe ni un rechazo", a.BAD, 0),
]
for s_, e, o, d, col, st in HDR:
    a.add(during(a, a.text(72, PY + 33, o, 17, a.INK, a.MONO, 600) + a.text(72, PY + 60, d, 17, col, a.MONO, 600), s_, e, still=st))
a.add(a.text(1128, PY + 33, "lo que lleva", 15, a.GREY, a.SANS, 400, "end"))
a.add(a.text(1128, PY + 56, "el paquete", 15, a.GREY, a.SANS, 400, "end"))

write(a, 10, "r1", "Quién llega al NVR y quién no",
      "Animación en cuatro tiempos con la central de monitoreo 203.0.113.25, que está en la address-list nvr-permitidos, un escáner de internet 198.51.100.66, "
      "el MikroTik con ether1 203.0.113.10 y el NVR 192.168.88.50 en TCP 8000. "
      "1: la central manda un SYN a 203.0.113.10:8000; la regla dstnat (in-interface-list=WAN, dst-port=8000, src-address-list=nvr-permitidos) coincide y el destino pasa a 192.168.88.50:8000. "
      "2: el NVR contesta con SYN-ACK y el router deshace el cambio: la central ve que le contesta 203.0.113.10:8000. "
      "3: el escáner prueba el 8000; no está en la lista, la regla no se aplica, el paquete sigue dirigido al router y la regla de input defconf: drop all not coming from LAN lo descarta. "
      "4: prueba el 8291 y el 80 del router; no hay nada publicado, input los descarta y no recibe respuesta. Los puertos 80, 443 y 8291 del router nunca se publican.",
      [5, 16, 35, 58, 66, 84, 95])
