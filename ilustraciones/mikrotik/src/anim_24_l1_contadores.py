#!/usr/bin/env python3
"""Lección 24 · Port forwarding · Laboratorio paso 6: leer el contador del NAT mientras probás.
Tres casos: sube y conecta; no sube (el SYN no llega o el origen no está en la lista); sube y no conecta (gateway del NVR).
"""
from _anim_mk_32_39 import *

a = Anim(T=28, kicker="MIKROTIK · PORT FORWARDING · PASO 6", title="El contador del NAT dice dónde buscar")
a.steps([
    "Sube y conecta: el SYN llega, el dst-nat cuenta 1 y el SYN-ACK vuelve por el MikroTik.",
    "No sube: el SYN muere antes (doble NAT, CGNAT) o el origen no está en la lista.",
    "Sube y no conecta: el NVR tiene otro gateway y el SYN-ACK se va por otro router.",
    "Regla: sin contador, buscá antes del MikroTik; con contador, en el NVR o en forward.",
], still=3, size=17)

Y = [214, 330, 446]
H = 80
SP = [(0, 25), (25, 50), (50, 75)]
for (s_, e), yc in zip(SP, Y):
    a.add(during(a, a.box(36, yc - H / 2 - 6, 1128, H + 12, a.WHITE, a.LINE, rx=16), s_, e))
for yc in Y:
    a.add(line(232, yc, 470, yc, a.LINE, 3, "5 7"))
    a.add(line(720, yc, 790, yc, a.LINE, 3, "5 7"))
    a.add(dev(a, 48, yc - H / 2, 184, H, "App", "198.51.100.20", "laptop", tsize=17))
    a.add(router(a, 470, yc - H / 2, 250, H, "MikroTik", "203.0.113.10"))
    a.add(dev(a, 790, yc - H / 2, 190, H, "NVR", "192.168.88.50", "server", tsize=17))
# obstáculo del caso B
a.add(a.box(250, Y[1] - 34, 180, 68, a.AMBBG, a.AMB, rx=12))
a.add(a.text(340, Y[1] - 6, "módem o CGNAT", 15, a.AMB, a.SANS, 600, "middle"))
a.add(a.text(340, Y[1] + 18, "sin reenvío", 15, a.AMB, a.MONO, 400, "middle"))
# gateway equivocado del caso C
a.add(a.box(1004, Y[2] - 34, 148, 68, a.BADBG, a.BAD, rx=12))
a.add(a.text(1078, Y[2] - 6, "otro router", 15, a.BAD, a.SANS, 600, "middle"))
a.add(a.text(1078, Y[2] + 18, "192.168.88.254", 14, a.BAD, a.MONO, 400, "middle"))
a.add(a.text(885, Y[2] + 58, "gateway del NVR: .254", 15, a.BAD, a.MONO, 600, "middle"))


def counter(yc, t_up):
    x, y = 708, yc - 34
    if t_up is None:
        a.add(a.pill(x, y, "contador 0", ROSE, "#14496F", 14, 26, "end"))
        return
    a.add(during(a, a.pill(x, y, "contador 0", SOFTW, "#14496F", 14, 26, "end"), 0, t_up, still=0))
    a.add(during(a, a.pill(x, y, "contador 1", a.INK, GOLD, 14, 26, "end"), t_up, 100, still=1))


counter(Y[0], 7)
counter(Y[1], None)
counter(Y[2], 57)

# caso A
a.add(travel(a, pkt(a, "SYN :18000"), [(170, Y[0]), (420, Y[0])], 1, 6, hold=1))
a.add(travel(a, pkt(a, "SYN :8000", a.OK), [(700, Y[0] + 26), (840, Y[0] + 26)], 8, 11, hold=1))
a.add(travel(a, pkt(a, "SYN-ACK", a.OK), [(840, Y[0] + 26), (700, Y[0] + 26)], 13, 16, hold=0.5))
a.add(travel(a, pkt(a, "SYN-ACK", a.OK), [(420, Y[0]), (170, Y[0])], 17, 22, hold=1))
a.add(during(a, check(a, 1012, Y[0]) + a.text(1038, Y[0] + 6, "conecta", 17, a.OK, a.SANS, 600), 22, 100, still=1))
# caso B
a.add(travel(a, pkt(a, "SYN :18000"), [(190, Y[1]), (236, Y[1])], 27, 31, hold=3))
a.add(during(a, xmark(a, 250, Y[1] - 34), 33, 100, still=1))
a.add(during(a, a.text(1000, Y[1] - 4, "no llega al", 16, a.AMB, a.SANS, 600) + a.text(1000, Y[1] + 18, "MikroTik", 16, a.AMB, a.SANS, 600), 34, 100, still=1))
a.add(during(a, a.text(600, Y[1] + 60, "o llega con un origen fuera de nvr-permitidos", 15, a.AMB, a.SANS, 600, "middle"), 38, 50))
# caso C
a.add(travel(a, pkt(a, "SYN :18000"), [(170, Y[2]), (420, Y[2])], 51, 56, hold=1))
a.add(travel(a, pkt(a, "SYN :8000", a.OK), [(700, Y[2] + 26), (840, Y[2] + 26)], 58, 61, hold=1))
a.add(travel(a, pkt(a, "SYN-ACK", a.BAD), [(950, Y[2]), (985, Y[2])], 64, 69, hold=3))
a.add(during(a, xmark(a, 1004, Y[2] - 34), 70, 100, still=1))
a.add(during(a, a.text(232, Y[2] + 58, "la respuesta no pasa por el MikroTik: nadie deshace el cambio", 15, a.BAD, a.SANS, 600), 66, 75))

# terminal
a.add(term(a, 48, 536, 1104, [
    '/ip/firewall/nat/print stats where comment~"NVR"',
    '/ip/firewall/connection/print where dst-address~":18000"',
], title="MIENTRAS PROBÁS"))

write(a, 24, "l1", "El contador del NAT dice dónde buscar",
      "Animación en cuatro tiempos con tres casos de una app 198.51.100.20 que llama a 203.0.113.10:18000, el MikroTik con el contador de la regla dstnat y el NVR 192.168.88.50. "
      "1: sube y conecta: el SYN llega al MikroTik, el contador pasa de 0 a 1, el dst-nat lo manda al NVR al 8000 y el SYN-ACK vuelve por el MikroTik a la app. "
      "2: no sube: el SYN se pierde antes de llegar, en un módem sin reenvío (doble NAT) o en el CGNAT del proveedor, o llega con un origen que no está en nvr-permitidos; el contador queda en 0. "
      "3: sube y no conecta: el SYN llega al NVR, pero el gateway del NVR es otro router, 192.168.88.254; el SYN-ACK sale por ahí, no pasa por el MikroTik y nadie deshace el cambio. "
      "4: la regla: si el contador no sube, buscá antes del MikroTik; si sube y no conecta, mirá el NVR o el forward. "
      "Abajo, los comandos /ip/firewall/nat/print stats where comment~\"NVR\" y /ip/firewall/connection/print where dst-address~\":18000\".",
      [4, 15, 20, 30, 40, 55, 66, 88])
