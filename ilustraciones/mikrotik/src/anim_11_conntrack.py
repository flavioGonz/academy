#!/usr/bin/env python3
"""Lección 11 · teoría: al conmutar, conntrack conserva las conexiones con su traducción vieja."""
from _anim_mikrotik_1_13 import *

a = Anim(T=26, kicker="MIKROTIK · CONNTRACK", title="Al conmutar, las conexiones viejas quedan colgadas")
a.steps([
    "Una llamada sale por el ISP1: conntrack la guarda traducida a 203.0.113.10.",
    "Cae internet del ISP1, no la interfaz: las rutas pasan al ISP2.",
    "La llamada sigue con su traducción vieja: por el ISP2 no sirve.",
    "Las conexiones nuevas salen bien. La vieja queda hasta que vence o la borrás.",
], still=2)

# rutas de salida (debajo de las cajas)
Y1, Y2 = 236, 404
a.add(f'<path d="M548 300 V{Y1} H900" fill="none" stroke="{a.LINE}" stroke-width="3"/>')
a.add(f'<path d="M548 340 V{Y2} H900" fill="none" stroke="{a.LINE}" stroke-width="3"/>')
a.add(line(248, 320, 400, 320, a.LINE, 3))


def p(label, col):
    return pkt(a, label, col, size=13, h=28)


# 1. sale por ISP1 con src 203.0.113.10
a.add(travel(a, p("de 203.0.113.10", a.BLUE), [(560, Y1), (800, Y1)], 4, 12, hold=6))
# 3. después del cambio, misma llamada sale por ISP2 con la traducción vieja
a.add(travel(a, p("de 203.0.113.10", a.AMB), [(560, Y2), (776, Y2)], 54, 62, hold=12))
a.add(during(a, xmark(a, 878, Y2), 62, 75, still=1))
a.add(still_only(a, place(a, p("de 203.0.113.10", a.AMB), 776, Y2)))
# 4. conexión nueva bien traducida
a.add(travel(a, p("de 192.168.8.2", a.OK), [(560, Y2), (790, Y2)], 78, 86, hold=12))

# cajas
a.add(device(a, 48, 270, 200, 100, "Teléfono SIP", "192.168.88.30", ssize=13))
a.add(a.box(400, 270, 300, 100, a.INK))
a.add(a.text(420, 302, "Router", 18, a.WHITE, a.SANS, 600))
a.add(a.text(420, 326, "masquerade por las", 13, SKY, a.MONO))
a.add(a.text(420, 346, "dos salidas", 13, SKY, a.MONO))
a.add(device(a, 900, 186, 252, 100, "ISP1 · ether1", "203.0.113.10", ssize=13))
a.add(device(a, 900, 354, 252, 100, "ISP2 · router 4G", "ether2 192.168.8.2", ssize=13))
a.add(during(a, a.box(896, 182, 260, 108, "none", a.BAD, rx=16, sw=3), 26, 100, still=1))
a.add(during(a, a.pill(1140, 252, "internet caída", a.BAD, a.BADBG, 13, 26, "end"), 26, 100, still=1))
a.add(during(a, a.pill(1140, 420, "ruta activa", a.OK, a.OKBG, 13, 26, "end"), 28, 100, still=1))

# tabla de conexiones
CX, CY, CW = 48, 480, 1104
a.add(a.box(CX, CY, CW, 118, a.INK))
a.add(a.text(CX + 20, CY + 28, "/ip/firewall/connection", 13, SKY, a.MONO))
r1 = a.text(CX + 20, CY + 60, "udp 192.168.88.30 → proveedor SIP", 15, a.WHITE, a.MONO, 600)
a.add(a.group(r1, a.show(8, 100), still=1))
for t0, t1, txt, col, st in [(8, 50, "traducida a 203.0.113.10 · por ISP1", MINT, 0), (50, 100, "traducida a 203.0.113.10 · ya no sirve", GOLD, 1)]:
    a.add(during(a, a.text(CX + 560, CY + 60, txt, 15, col, a.MONO, 600), t0, t1, still=st))
r2 = a.text(CX + 20, CY + 92, "conexión nueva", 15, a.WHITE, a.MONO, 600) + a.text(CX + 560, CY + 92, "traducida a 192.168.8.2 · por ISP2", 15, MINT, a.MONO, 600)
a.add(during(a, r2, 80, 100))
a.add(a.text(48, 640, "Para soltar lo colgado: /ip/firewall/connection/remove [find protocol=udp] (corta las llamadas en curso).", 15, a.TXT, a.MONO))

p_, pre = out(11, 2)
a.write(p_, title="Conexiones viejas al conmutar de WAN",
        desc="Animación en cuatro tiempos con un teléfono SIP 192.168.88.30 detrás de un router con dos salidas y masquerade por las dos: ISP1 por ether1 con 203.0.113.10 "
             "e ISP2 por un router 4G, con ether2 en 192.168.8.2. 1: una llamada sale por el ISP1 y conntrack la guarda traducida a 203.0.113.10. 2: cae internet del ISP1 "
             "pero la interfaz no baja: las rutas pasan al ISP2. 3: la llamada sigue con su traducción vieja y sus paquetes salen por el ISP2 con origen 203.0.113.10: no sirven. "
             "4: las conexiones nuevas salen bien traducidas a 192.168.8.2; la vieja queda hasta que vence o se borra con /ip/firewall/connection/remove [find protocol=udp], "
             "que corta las llamadas en curso.",
        preview=[12, 36, 64, 90], prefix=pre)
