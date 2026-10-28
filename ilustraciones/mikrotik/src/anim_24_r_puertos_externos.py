#!/usr/bin/env python3
"""Lección 24 · Port forwarding · Resumen ("Cómo se ve en la red").
Una IP pública, un puerto de afuera por servicio: 18000 y 18554 al NVR1, 18001 al NVR2; fuera de la lista no entra.
"""
from _anim_mk_32_39 import *

a = Anim(T=24, kicker="MIKROTIK · PORT FORWARDING · CÓMO SE VE EN LA RED", title="Una IP pública, un puerto de afuera por servicio")
a.steps([
    "iVMS-4200 pide 203.0.113.10:18000. El dst-nat lo manda al NVR1, puerto 8000.",
    "VLC pide el 18554: mismo NVR1, pero al 554, el de RTSP.",
    "La app del NVR2 pide el 18001: otro equipo, el mismo 8000 de adentro.",
    "Un celular fuera de nvr-permitidos pide el 18000: ninguna regla coincide.",
], still=0, size=17)

ROWS = [262, 318, 374]
RX, RY, RW, RH = 360, 176, 480, 330
a.add(a.box(RX, RY, RW, RH, a.INK, rx=18))
a.add(a.text(RX + 20, RY + 30, "MikroTik · ether1 203.0.113.10", 17, a.WHITE, a.SANS, 600))
a.add(a.text(RX + 20, RY + 54, "dstnat · WAN · src-address-list=nvr-permitidos", 15, SKY, a.MONO))
RT = [("dst-port=18000", "192.168.88.50:8000"), ("dst-port=18554", "192.168.88.50:554"), ("dst-port=18001", "192.168.88.51:8000")]
for y, (p, d) in zip(ROWS, RT):
    a.add(a.box(RX + 20, y - 23, RW - 40, 46, a.NAVY2, rx=10))
    a.add(a.text(RX + 36, y + 6, p, 15, a.WHITE, a.MONO, 600))
    a.add(a.text(RX + 196, y + 6, "→ " + d, 15, GOLD, a.MONO, 600))
HL = [(0, 2, 12), (1, 27, 37), (2, 52, 62)]
for i, s_, e in HL:
    a.add(during(a, a.box(RX + 16, ROWS[i] - 27, RW - 32, 54, "none", MINT, rx=12, sw=3.5), s_ + 3, e))
# celular: ninguna coincide
a.add(during(a, a.box(RX + 16, ROWS[0] - 27, RW - 32, 54, "none", ROSE, rx=12, sw=3.5), 80, 86))
a.add(a.box(RX + 20, 424, RW - 40, 62, a.NAVY2, rx=10))
a.add(a.text(RX + 36, 450, "sin dst-nat: el paquete es para el router", 15, SOFTW, a.MONO))
a.add(a.text(RX + 36, 474, "input · defconf: drop", 15, ROSE, a.MONO, 600))
a.add(during(a, a.box(RX + 16, 420, RW - 32, 70, "none", ROSE, rx=12, sw=3.5), 86, 100))

# extremos
a.add(dev(a, 48, 230, 250, 168, "Oficina IES", "198.51.100.20", "laptop", sub2="en la lista"))
a.add(a.text(110, 334, "iVMS-4200", 15, a.TXT, a.SANS))
a.add(a.text(110, 356, "VLC · app", 15, a.TXT, a.SANS))
a.add(dev(a, 48, 418, 250, 92, "Celular", "198.51.100.77", "phone", sub2="fuera de la lista"))
a.add(dev(a, 930, 214, 222, 132, "NVR1", "192.168.88.50", "server", sub2="8000 SDK"))
a.add(a.text(992, 326, "554 RTSP", 15, a.GREY, a.MONO))
a.add(dev(a, 930, 352, 222, 92, "NVR2", "192.168.88.51", "server", sub2="8000 SDK"))
for y in ROWS:
    a.add(line(300, y, RX - 4, y, a.LINE, 3, "5 7"))
    a.add(line(RX + RW + 4, y, 928, y, a.LINE, 3, "5 7"))
a.add(line(300, 464, RX - 4, 464, a.LINE, 3, "5 7"))


def flow(t, y, out_lbl, in_lbl):
    a.add(travel(a, pkt(a, out_lbl), [(250, y), (RX - 56, y)], t, t + 4, hold=1.5))
    a.add(travel(a, pkt(a, in_lbl, a.OK), [(RX + RW + 64, y), (860, y)], t + 8, t + 13, hold=3))


flow(1, ROWS[0], "→ :18000", "→ .50:8000")
flow(26, ROWS[1], "→ :18554", "→ .50:554")
flow(51, ROWS[2], "→ :18001", "→ .51:8000")
a.add(wins(a, check(a, 1126, 240), [(15, 25)]))
a.add(wins(a, check(a, 1126, 300), [(40, 50)]))
a.add(wins(a, check(a, 1126, 378), [(65, 75)]))
a.add(travel(a, pkt(a, "→ :18000", a.BAD), [(250, 464), (RX - 56, 464)], 76, 80, hold=6))
a.add(during(a, xmark(a, 330, 464), 87, 100))
a.add(still_only(a, place(pkt(a, "→ .50:8000", a.OK), 878, ROWS[0]) + check(a, 1126, 240)))

# cabecera del paquete
PY = 526
a.add(a.box(48, PY, 1104, 84, a.WHITE, a.LINE, rx=14))
a.add(a.text(72, PY + 34, "llega a", 15, a.GREY, a.MONO))
a.add(a.text(600, PY + 34, "sale hacia", 15, a.GREY, a.MONO))
HDR = [
    (0, 25, "203.0.113.10:18000", "192.168.88.50:8000", a.OK, 1),
    (25, 50, "203.0.113.10:18554", "192.168.88.50:554", a.OK, 0),
    (50, 75, "203.0.113.10:18001", "192.168.88.51:8000", a.OK, 0),
    (75, 100, "203.0.113.10:18000", "no sale: drop en input", a.BAD, 0),
]
for s_, e, o, d, col, st in HDR:
    a.add(during(a, a.text(72, PY + 66, o, 20, a.INK, a.MONO, 600) + a.text(600, PY + 66, d, 20, col, a.MONO, 600), s_, e, still=st))
a.add(a.text(48, 646, "dst-port es el puerto de afuera; to-ports, el del NVR. La app se carga con la IP pública y el puerto de afuera.", 16, a.TXT, a.SANS, 600))

write(a, 24, "r1", "Una IP pública, un puerto de afuera por servicio",
      "Animación en cuatro tiempos con la oficina IES 198.51.100.20 (en la lista nvr-permitidos), un celular 198.51.100.77 fuera de la lista, el MikroTik con ether1 203.0.113.10 "
      "y dos NVR: NVR1 192.168.88.50 con 8000 SDK y 554 RTSP, y NVR2 192.168.88.51 con 8000. En el router hay tres reglas dstnat con in-interface-list=WAN y src-address-list=nvr-permitidos. "
      "1: iVMS-4200 pide 203.0.113.10:18000 y el dst-nat lo manda a 192.168.88.50:8000. "
      "2: VLC pide el 18554 y va al mismo NVR1, al 554 de RTSP. "
      "3: la app del NVR2 pide el 18001 y va a 192.168.88.51:8000: otro equipo con el mismo puerto de adentro. "
      "4: el celular, fuera de la lista, pide el 18000; ninguna regla coincide, el paquete queda dirigido al router y la regla de input de la configuración por defecto lo descarta. "
      "dst-port es el puerto de afuera y to-ports el del NVR.",
      [5, 12, 30, 40, 55, 65, 80, 92])
