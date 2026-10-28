#!/usr/bin/env python3
"""Lección 13 · Laboratorio, paso 3: verificar por capas desde el router. Ping al gateway (vecino en el /29),
ping a 1.1.1.1 (ruta por defecto) y :resolve mikrotik.com (DNS a 1.1.1.1 por UDP 53). Cada falla señala una capa."""
from _anim_red_1_9 import *

a = Anim(T=26, kicker="MIKROTIK · IP FIJA · LABORATORIO", title="Tres pruebas en orden: vecino, mundo, nombres")
a.steps([
    "/ping 203.0.113.9: el gateway, que es tu vecino en el /29, contesta.",
    "/ping 1.1.1.1: sale por la ruta por defecto, cruza el gateway y vuelve.",
    ":resolve mikrotik.com: el router pregunta a su DNS y recibe la dirección.",
    "Si el gateway contesta y 1.1.1.1 no, el problema es la ruta o el proveedor.",
], still=2)

MT, GW, NT = 200, 600, 1000
a.add(dev(a, 48, 176, 304, 78, "MikroTik", "ether1 203.0.113.10/29", icon="server", dark=True))
a.add(dev(a, 448, 176, 304, 78, "Gateway proveedor", "203.0.113.9", icon="server"))
a.add(dev(a, 848, 176, 304, 78, "1.1.1.1", "internet y DNS", icon="cloud"))
for x in (MT, GW, NT):
    a.add(lifeline(a, x, 254, 482))

msg(a, MT, GW, 292, "echo", 3, end=76, still=1)
msg(a, GW, MT, 324, "reply", 9, color=a.OK, end=76, still=1)
msg(a, MT, NT, 370, "echo · por 0.0.0.0/0 vía .9", 28, end=76, still=1)
msg(a, NT, MT, 402, "reply", 37, color=a.OK, end=76, still=1)
msg(a, MT, NT, 448, "DNS · UDP 53 · ¿mikrotik.com?", 53, end=76, still=1)
msg(a, NT, MT, 480, "respuesta con la dirección", 62, color=a.OK, end=76, still=1)
# 4 · ejemplo de falla
msg(a, MT, GW, 292, "echo", 77, end=100, still=0)
msg(a, GW, MT, 324, "reply", 80, color=a.OK, end=100, still=0)
msg(a, MT, NT, 370, "echo a 1.1.1.1", 84, end=100, still=0, color=a.BAD, dash="8 6")
a.add(during(a, xmark(a, NT - 34, 370) + a.text(NT - 34, 406, "no vuelve", 15, a.BAD, a.MONO, 600, "middle"), 88, 100))

# checklist
CW = 352
CH = [("1 · gateway", "si falla: cable, máscara o VLAN"), ("2 · IP de internet", "si falla: ruta o proveedor"), ("3 · nombre", "si falla: DNS")]
for i, (t, s) in enumerate(CH):
    x = 48 + i * (CW + 24)
    y = 506
    a.add(a.box(x, y, CW, 96, a.WHITE, a.LINE, rx=14))
    a.add(a.text(x + 20, y + 36, t, 18, a.INK, a.SANS, 600))
    a.add(a.text(x + 20, y + 68, s, 15, a.TXT, a.SANS))
    on = [12, 40, 66][i]
    a.add(during(a, check(a, x + CW - 30, y + 30), on, 76, still=1))
    a.add(during(a, a.box(x, y, CW, 96, "none", a.OK, rx=14, sw=2.5), on, 76, still=1))
a.add(during(a, check(a, 48 + CW - 30, 536) + a.box(48, 506, CW, 96, "none", a.OK, rx=14, sw=2.5), 82, 100))
a.add(during(a, xmark(a, 48 + CW + 24 + CW - 30, 536) + a.box(48 + CW + 24, 506, CW, 96, "none", a.BAD, rx=14, sw=3), 90, 100))
a.add(during(a, a.text(48 + 2 * (CW + 24) + CW - 30, 542, "—", 20, a.GREY, a.MONO, 600, "middle"), 90, 100))

a.add(a.text(48, 640, "Cerrás con /ip/route/print where dst-address=0.0.0.0/0: la ruta por defecto tiene que estar activa.", 16, a.TXT, a.SANS, 600))

write(a, 13, "l1", "Verificación por capas con IP fija",
      "Animación en cuatro tiempos con tres líneas de vida: el MikroTik (ether1 203.0.113.10/29), el gateway del proveedor (203.0.113.9) y 1.1.1.1, que es un destino de internet y también el DNS del router. "
      "1: /ping 203.0.113.9: el gateway, vecino en el /29, contesta; queda probada la capa de cable, máscara y VLAN. "
      "2: /ping 1.1.1.1 sale por la ruta por defecto 0.0.0.0/0 vía .9 y vuelve: ruta y proveedor bien. "
      "3: :resolve mikrotik.com manda una consulta DNS por UDP 53 a 1.1.1.1 y recibe la dirección: DNS bien. "
      "4: el ejemplo de falla: el gateway contesta pero el ping a 1.1.1.1 no vuelve; el problema es la ruta por defecto o el proveedor, y el DNS ni se llega a probar. "
      "Se cierra mirando que la ruta por defecto esté activa.",
      [10, 36, 62, 92])
