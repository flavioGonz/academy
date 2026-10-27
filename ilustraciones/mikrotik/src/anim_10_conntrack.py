#!/usr/bin/env python3
"""Lección 10 · teoría: el dst-nat decide con el primer paquete y la conexión sigue lo guardado en la tabla."""
from _anim_mikrotik_1_13 import *

a = Anim(T=26, kicker="MIKROTIK · LECCIÓN 10 · CÓMO FUNCIONA", title="El NAT decide con el primer paquete de cada conexión")
a.steps([
    "El primer paquete de la central pasa por las reglas: el dst-nat le cambia el destino.",
    "Esa decisión queda guardada en la tabla de conexiones.",
    "Los paquetes que siguen no miran las reglas: usan lo guardado.",
    "Si cambiás la regla, la conexión abierta sigue igual hasta que la borrás.",
], still=2)

L1, L2 = 292, 428   # carriles: reglas y tabla
# carriles (debajo de todo)
for y in (L1, L2):
    a.add(line(204, y, 996, y, a.LINE, 2, "3 7"))


def dot(col):
    return f'<circle cx="0" cy="0" r="11" fill="{col}"/>'


# 1. primer paquete por las reglas
a.add(travel(a, dot(a.BLUE), [(214, L1), (986, L1)], 2, 14, hold=1))
# 3. siguientes por la tabla
for t0 in (52, 58, 64):
    a.add(travel(a, dot(a.BLUE), [(214, L2), (986, L2)], t0, t0 + 8, hold=0.5))
# 4. con la regla cambiada, siguen por la tabla
for t0 in (78, 86):
    a.add(travel(a, dot(a.BLUE), [(214, L2), (986, L2)], t0, t0 + 8, hold=0.5))
a.add(still_only(a, place(a, dot(a.BLUE), 266, L2) + place(a, dot(a.BLUE), 934, L2)))

# extremos
a.add(device(a, 48, 236, 156, 250, "Central", "203.0.113.25", ssize=13))
a.add(a.text(66, 340, "manda a", 13, a.GREY, a.MONO))
a.add(a.text(66, 360, "203.0.113.10", 14, a.INK, a.MONO, 600))
a.add(a.text(66, 380, ":8000", 14, a.INK, a.MONO, 600))
a.add(device(a, 996, 236, 156, 250, "NVR", "192.168.88.50", ssize=13))
a.add(a.text(1014, 340, "recibe en", 13, a.GREY, a.MONO))
a.add(a.text(1014, 360, ":8000", 14, a.INK, a.MONO, 600))
a.add(during(a, check(a, 1126, 264), 13, 100, still=1))

# router
RX, RW = 330, 540
a.add(a.box(RX, 186, RW, 334, a.INK))
a.add(a.text(RX + 20, 216, "Router · 203.0.113.10", 17, a.WHITE, a.SANS, 600))
# reglas
a.add(a.box(RX + 40, 236, RW - 80, 112, "#0B3A66", rx=12))
a.add(a.text(RX + 58, 262, "/ip/firewall/nat · dstnat", 13, SKY, a.MONO))
a.add(a.text(RX + 58, 288, "in-interface-list=WAN dst-port=8000", 14, a.WHITE, a.MONO))
a.add(a.text(RX + 58, 310, "src-address-list=nvr-permitidos", 14, a.WHITE, a.MONO))
a.add(a.text(RX + 58, 332, "→ to-addresses=192.168.88.50", 14, a.WHITE, a.MONO))
a.add(during(a, a.box(RX + 36, 232, RW - 72, 120, "none", GOLD, rx=14, sw=3), 4, 16))
a.add(a.group(a.box(RX + 40, 236, RW - 80, 112, a.INK, rx=12, extra='opacity=".55"'), a.show(50, 100, 0.8), still=1))
a.add(during(a, a.pill(RX + RW - 52, 244, "cambiada", a.INK, GOLD, 13, 26, "end"), 76, 100))
# tabla
a.add(a.box(RX + 40, 380, RW - 80, 96, "#0B3A66", rx=12))
a.add(a.text(RX + 58, 406, "/ip/firewall/connection", 13, SKY, a.MONO))
row = (a.text(RX + 58, 432, "203.0.113.25 → 203.0.113.10:8000", 14, a.WHITE, a.MONO, 600)
       + a.text(RX + 58, 456, "traducido a 192.168.88.50:8000", 14, MINT, a.MONO, 600))
a.add(a.group(row, a.show(26, 100), still=1))
a.add(during(a, a.box(RX + 36, 376, RW - 72, 104, "none", MINT, rx=14, sw=3), 26, 75, still=1))

# lectura del paquete
a.add(during(a, a.text(600, 552, "destino 203.0.113.10:8000  →  192.168.88.50:8000", 17, a.INK, a.MONO, 600, "middle"), 4, 25))
a.add(during(a, a.text(600, 552, "solo el primer paquete pasa por las reglas de NAT", 16, a.TXT, a.SANS, 600, "middle"), 25, 75, still=1))
a.add(term(a, 48, 572, 1104, ['/ip/firewall/connection/remove [find dst-address~":8000"]'], size=15))
a.add(during(a, a.text(1134, 608, "para que aplique la regla nueva", 14, GOLD, a.MONO, 600, "end"), 76, 100))
a.add(during(a, a.text(600, 552, "la conexión vieja sigue la decisión guardada", 16, a.AMB, a.SANS, 600, "middle"), 76, 100))

p, pre = out(10, 1)
a.write(p, title="El NAT y la tabla de conexiones",
        desc="Animación en cuatro tiempos. La central de monitoreo 203.0.113.25 manda al puerto 8000 de la IP pública del router, 203.0.113.10, y el NVR está en "
             "192.168.88.50. 1: el primer paquete pasa por la regla dstnat (in-interface-list=WAN, dst-port=8000, src-address-list=nvr-permitidos) y su destino cambia "
             "a 192.168.88.50:8000. 2: esa decisión queda guardada en la tabla de conexiones. 3: los paquetes siguientes de la misma conexión no pasan por las reglas: "
             "usan lo guardado. 4: si cambiás la regla, la conexión abierta sigue igual; para que aplique la regla nueva se borra con "
             "/ip/firewall/connection/remove [find dst-address~\":8000\"].",
        preview=[8, 36, 62, 88], prefix=pre)
