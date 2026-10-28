#!/usr/bin/env python3
"""Lección 28 · L2TP saliente · Laboratorio paso 7: add-default-route=yes.
La ruta por defecto pasa al túnel y RouterOS agrega una /32 hacia el servidor por el ISP: la navegación entra al túnel
y los paquetes del propio túnel salen por el ISP porque la /32 gana por máscara más larga.
"""
from _anim_mk_32_39 import *

a = Anim(T=24, kicker="MIKROTIK · L2TP SALIENTE · PASO 7", title="Todo por la central, menos el túnel mismo")
a.steps([
    "Con add-default-route=yes aparecen 0.0.0.0/0 por l2tp-central y una /32 al servidor.",
    "La PC va a 198.51.100.80: gana 0.0.0.0/0 y viaja por adentro del túnel.",
    "El túnel mismo va a 203.0.113.10: la /32 gana por máscara más larga y sale por el ISP.",
    "La /32 evita que el túnel se meta en sí mismo. Después de probar, volvé a no.",
], still=2, size=17)

# ---- tabla de rutas
TX, TY, TW = 48, 172, 1104
a.add(a.box(TX, TY, TW, 262, a.INK, rx=16))
a.add(a.text(TX + 20, TY + 30, "/ip/route/print · sucursal", 15, SKY, a.MONO))
a.add(a.text(TX + 300, TY + 30, "dst-address", 15, SKY, a.MONO))
a.add(a.text(TX + 560, TY + 30, "gateway", 15, SKY, a.MONO))
ROWS = [
    ("0.0.0.0/0", "l2tp-central", "del túnel", 4),
    ("203.0.113.10/32", "192.168.1.1 (ISP)", "la agrega RouterOS", 8),
    ("10.255.1.1/32", "l2tp-central", "otra punta", 0),
    ("192.168.88.0/24", "bridge", "LAN", 0),
]


def ry(i):
    return TY + 46 + i * 52


for i, (d, g, n, t) in enumerate(ROWS):
    row = (a.box(TX + 14, ry(i), TW - 28, 44, a.NAVY2, rx=10) + a.text(TX + 300, ry(i) + 28, d, 17, a.WHITE, a.MONO, 600)
           + a.text(TX + 560, ry(i) + 28, g, 17, GOLD if i < 2 else a.WHITE, a.MONO, 600) + a.text(TX + TW - 30, ry(i) + 28, n, 15, SKY, a.SANS, 400, "end"))
    a.add(during(a, row, t, 100, still=1) if t else row)
    if t:
        a.add(during(a, a.pill(TX + 30, ry(i) + 9, "dinámica", a.INK, MINT, 13, 26), t, 100, still=1))


def hl(i, t0, t1, col, still=0):
    a.add(during(a, a.box(TX + 10, ry(i) - 4, TW - 20, 52, "none", col, rx=12, sw=3.5), t0, t1, still=still))


hl(0, 28, 50, MINT)
hl(1, 53, 75, GOLD, still=1)
a.add(during(a, a.pill(TX + 720, 436, "/32 es más larga que /0: gana", a.INK, GOLD, 14, 24), 55, 75, still=1))

# ---- el camino
DY, DH = 462, 84
DC = DY + DH / 2
a.add(line(300, DC, 760, DC, a.LINE, 3, "5 7"))
a.add(line(960, DC, 1000, DC, a.LINE, 3, "5 7"))
a.add(a.box(300, DC - 18, 460, 36, a.OK, a.OK, rx=18, sw=2, extra='fill-opacity=".12"'))
a.add(a.text(650, DC + 40, "túnel (dentro de IPsec)", 15, a.OK, a.MONO, 600, "middle"))
a.add(router(a, 48, DY, 252, DH, "hAP sucursal", "PC 192.168.88.20 detrás"))
a.add(dev(a, 360, DY, 190, DH, "ISP", "192.168.1.1", "globe", tsize=17))
a.add(router(a, 760, DY, 200, DH, "Central", "203.0.113.10"))
a.add(dev(a, 1000, DY, 152, DH, "Web", "198.51.100.80", None, tsize=17))

# 2. navegación por el túnel
a.add(travel(a, pkt(a, "→ 198.51.100.80", a.OK, size=14, h=26), [(330, DC), (650, DC)], 30, 40, hold=1))
a.add(travel(a, dot(a, a.OK, 9), [(960, DC), (1000, DC)], 43, 46, hold=3))
# 3. paquetes del túnel por el ISP
a.add(travel(a, pkt(a, "UDP 4500 → 203.0.113.10", a.BLUE, size=14, h=26), [(310, DC - 32), (460, DC - 32), (640, DC - 32)], 56, 68, hold=4))
a.add(still_only(a, place(pkt(a, "UDP 4500 → 203.0.113.10", a.BLUE, size=14, h=26), 520, DC - 32)))

narr(a, 48, 598, [
    (0, 25, "La ruta por defecto ahora apunta al túnel. La del ISP queda solo para la central.", a.TXT, 0),
    (25, 50, "Para que la LAN navegue así, hace falta el NAT del paso 5 o que la central lo haga.", a.OK, 0),
    (50, 75, "El túnel viaja por el ISP como cualquier conexión hacia 203.0.113.10.", a.BLUE, 1),
    (75, 100, "Si el túnel entrara en el túnel, no llegaría nunca a la central.", a.AMB, 0),
])
a.add(a.text(48, 640, "/interface/l2tp-client/set l2tp-central add-default-route=no   (al terminar la prueba)", 16, a.TXT, a.MONO))

write(a, 28, "l2", "Todo por la central, menos el túnel mismo",
      "Animación en cuatro tiempos con la tabla de rutas de la sucursal y el camino hAP, ISP 192.168.1.1, central 203.0.113.10 y una web 198.51.100.80. "
      "1: con add-default-route=yes aparecen dos rutas dinámicas: 0.0.0.0/0 por l2tp-central y 203.0.113.10/32 por 192.168.1.1, el gateway del ISP; siguen 10.255.1.1/32 por l2tp-central y 192.168.88.0/24 en el bridge. "
      "2: la PC 192.168.88.20 va a 198.51.100.80; gana 0.0.0.0/0, el paquete viaja por adentro del túnel y sale a internet desde la central, para lo que hace falta el NAT del paso 5 o que la central lo haga. "
      "3: los paquetes del propio túnel, UDP 4500 hacia 203.0.113.10, coinciden con la /32, que gana por máscara más larga, y salen por el ISP. "
      "4: esa /32 la agrega RouterOS para que el túnel no se meta en sí mismo; después de probar se vuelve a add-default-route=no.",
      [6, 30, 44, 60, 66, 88])
