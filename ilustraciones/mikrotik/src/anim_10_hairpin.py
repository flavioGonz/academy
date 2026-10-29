#!/usr/bin/env python3
"""Lección 10 · teoría: hairpin NAT, direcciones de origen y destino en cada tramo, sin y con masquerade."""
from _anim_mikrotik_1_13 import *

a = Anim(T=30, kicker="MIKROTIK · HAIRPIN", title="Hairpin: por qué hace falta el masquerade de adentro")
a.steps([
    "Una PC de la LAN pide a la IP pública: 203.0.113.10:8000.",
    "El dst-nat cambia el destino al NVR, 192.168.88.50.",
    "Sin hairpin: el NVR contesta directo. La PC esperaba otra IP y lo descarta.",
    "Con masquerade: el origen pasa a ser el router, y el NVR le contesta a él.",
    "El router deshace las dos traducciones y le devuelve la respuesta a la PC.",
], still=4)

R = (600, 236)   # centro inferior del router
PC = (158, 452)
NV = (1042, 452)
RL, RR = (540, 280), (660, 280)
PCt, NVt = (158, 448), (1042, 448)
LY = 500   # tramo directo por la LAN

# líneas
a.add(f'<path d="M{PCt[0]} {PCt[1]} L{RL[0]} {RL[1]}" stroke="{a.LINE}" stroke-width="3" fill="none"/>')
a.add(f'<path d="M{RR[0]} {RR[1]} L{NVt[0]} {NVt[1]}" stroke="{a.LINE}" stroke-width="3" fill="none"/>')
a.add(line(268, LY, 932, LY, a.LINE, 3, "6 6"))
a.add(a.text(600, LY + 26, "misma LAN · bridge", 13, a.GREY, a.MONO, 400, "middle"))


def dot(col):
    return f'<circle cx="0" cy="0" r="11" fill="{col}"/>'


def hdr(x, y, src, dst, col=None, hi=None, w=300):
    """Cabecera del paquete: origen y destino."""
    s = a.box(x, y, w, 64, a.WHITE, col or a.LINE, rx=10, sw=2)
    for k, (lab, val) in enumerate((("de", src), ("a", dst))):
        c = (hi or {}).get(k, a.INK)
        s += a.text(x + 14, y + 26 + k * 24, lab, 13, a.GREY, a.MONO)
        s += a.text(x + 44, y + 26 + k * 24, val, 15, c, a.MONO, 600)
    return s


up_l = [(PCt[0] + 10, PCt[1] - 10), (RL[0] - 10, RL[1] + 8)]
dn_l = list(reversed(up_l))
dn_r = [(RR[0] + 10, RR[1] + 8), (NVt[0] - 10, NVt[1] - 10)]
up_r = list(reversed(dn_r))
SL, SR = (48, 186), (852, 186)

# 1. PC → router
a.add(travel(a, dot(a.BLUE), up_l, 2, 10, hold=2))
a.add(during(a, hdr(*SL, "192.168.88.20", "203.0.113.10:8000"), 2, 20))
# 2. router → NVR con dst cambiado
a.add(travel(a, dot(a.BLUE), dn_r, 22, 30, hold=2))
a.add(during(a, hdr(*SR, "192.168.88.20", "192.168.88.50:8000", hi={1: a.AMB}), 22, 40))
a.add(during(a, a.pill(600, 300, "dst-nat", a.AMB, a.AMBBG, 14, 28, "middle"), 21, 40))
# 3. NVR contesta directo a la PC
a.add(travel(a, dot(a.BAD), [(920, LY), (290, LY)], 42, 52, hold=1))
a.add(during(a, hdr(450, 540, "192.168.88.50", "192.168.88.20", a.BAD), 42, 60))
a.add(during(a, xmark(a, 292, 468), 53, 60))
a.add(during(a, a.text(48, 566, "esperaba de 203.0.113.10", 14, a.BAD, a.MONO, 600), 53, 60))
# 4. con masquerade: router → NVR con src del router, NVR → router
a.add(travel(a, dot(a.BLUE), up_l, 61, 65, hold=0.5))
a.add(travel(a, dot(a.BLUE), dn_r, 66, 71, hold=0.5))
a.add(during(a, hdr(*SR, "192.168.88.1", "192.168.88.50:8000", hi={0: a.OK, 1: a.AMB}), 66, 73))
a.add(travel(a, dot(a.OK), up_r, 73, 78, hold=1))
a.add(during(a, hdr(*SR, "192.168.88.50", "192.168.88.1", a.OK), 73, 80))
a.add(during(a, a.pill(600, 300, "dst-nat + masquerade", a.OK, a.OKBG, 14, 28, "middle"), 61, 80))
# 5. router → PC
a.add(travel(a, dot(a.OK), dn_l, 82, 90, hold=8))
a.add(during(a, hdr(*SL, "203.0.113.10:8000", "192.168.88.20", a.OK, hi={0: a.OK}), 82, 100, still=1))
a.add(during(a, check(a, 252, 440), 90, 100, still=1))
a.add(during(a, a.pill(600, 300, "deshace las dos", a.OK, a.OKBG, 14, 28, "middle"), 81, 100, still=1))

# cajas
a.add(a.box(470, 186, 260, 94, a.INK))
a.add(a.text(490, 218, "Router", 18, a.WHITE, a.SANS, 600))
a.add(a.text(490, 242, "pública 203.0.113.10", 13, SKY, a.MONO))
a.add(a.text(490, 262, "LAN 192.168.88.1", 13, SKY, a.MONO))
a.add(device(a, 48, 448, 220, 92, "PC", "192.168.88.20", ssize=13))
a.add(device(a, 932, 448, 220, 92, "NVR", "192.168.88.50:8000", ssize=13))
a.add(a.text(48, 640, "masquerade de la LAN hacia el NVR: srcnat src-address=192.168.88.0/24 dst-address=192.168.88.50", 15, a.TXT, a.MONO))

p, pre = out(10, 2)
a.write(p, title="Hairpin NAT paso a paso",
        desc="Animación en cinco tiempos con una PC 192.168.88.20 y un NVR 192.168.88.50 en la misma LAN, y el router con IP pública 203.0.113.10 y LAN 192.168.88.1. "
             "1: la PC manda a 203.0.113.10:8000. 2: el dst-nat cambia el destino a 192.168.88.50:8000 y el paquete llega al NVR con origen 192.168.88.20. "
             "3: sin hairpin, el NVR contesta directo a la PC desde 192.168.88.50; la PC esperaba la respuesta de 203.0.113.10 y la descarta. "
             "4: con un masquerade desde la LAN hacia el NVR, el router pone su IP 192.168.88.1 como origen y el NVR le contesta al router. "
             "5: el router deshace las dos traducciones y la PC recibe la respuesta de 203.0.113.10:8000.",
        preview=[8, 30, 55, 70, 76, 94], prefix=pre)
