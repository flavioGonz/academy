#!/usr/bin/env python3
"""Lección 4 (Input y forward) · Resumen: el NVR publicado por el 18000. La regla en input queda en 0 porque el dst-nat cambia el destino antes de decidir el camino."""
from _anim_r20_31 import *

a, _ = nuevo(24, "MIKROTIK · INPUT Y FORWARD · EN LA RED", "Por qué la regla en input del NVR queda en 0",
             ["Desde el celular, alguien entra a la IP pública del router por el 18000.",
              "En prerouting, el dst-nat cambia el destino al NVR antes de decidir.",
              "La decisión ve una IP de la LAN: el paquete va a forward, no a input.",
              "La regla de forward con la IP y el puerto del NVR es la que suma."], still=3)

# encabezado del paquete
a.add(a.box(48, 176, 1104, 50, a.WHITE, a.LINE, rx=12))
a.add(a.text(68, 208, "encabezado", 15, a.GREY, a.MONO))
a.add(a.text(190, 208, "src 198.51.100.7", 16, a.INK, a.MONO, 600))
a.add(a.text(392, 208, "→ dst", 16, a.GREY, a.MONO, 600))
flip(a, 462, 208, [(0, 31, "203.0.113.10 : 18000", a.INK), (31, 100, "192.168.88.50 : 8000", a.OK)], size=16, still_idx=1)
en(a, a.pill(1132, 189, "cambiado por dst-nat", a.OK, a.OKBG, 14, 26, anchor="end"), 31, 100, still=1)

# camino
MY, IY = 400, 284
a.add(wire(180, MY, 1030, MY, a.LINE, 3))
a.add(poly([(500, MY - 40), (500, IY), (600, IY)], a.LINE, 3))
dev(a, 48, MY - 50, 132, 100, "Internet", "celular", "4G", kind="isp", ssize=14)
def etapa(x, y, w, h, t, s1, s2=""):
    s = a.box(x, y, w, h, a.WHITE, a.LINE, rx=14, sw=2)
    s += a.text(x + w / 2, y + 30, t, 17, a.INK, a.HEAD, 600, "middle")
    s += a.text(x + w / 2, y + 54, s1, 14, a.GREY, a.MONO, 400, "middle")
    if s2:
        s += a.text(x + w / 2, y + 74, s2, 14, a.GREY, a.MONO, 400, "middle")
    return a.add(s)
etapa(250, MY - 46, 170, 92, "prerouting", "conntrack", "dst-nat")
a.add(f'<path d="M500 {MY - 40} L540 {MY} L500 {MY + 40} L460 {MY} Z" fill="{a.INK}"/>')
a.add(a.text(500, MY + 64, "decisión", 15, a.GREY, a.MONO, 600, "middle"))
a.add(a.text(500, MY + 84, "de ruteo", 15, a.GREY, a.MONO, 600, "middle"))
etapa(600, IY - 40, 160, 80, "input", "para el router")
a.add(a.text(784, IY + 6, "WinBox, DNS, el propio router", 15, a.GREY, a.SANS))
etapa(600, MY - 40, 160, 80, "forward", "pasa a través")
etapa(830, MY - 40, 140, 80, "postrouting", "src-nat")
dev(a, 1030, MY - 50, 122, 100, "NVR", "192.168.88.50", ":8000", ssize=13)
en(a, ring(a, 246, MY - 50, 178, 100, a.OK, rx=16), 25, 50)
en(a, ring(a, 596, MY - 44, 168, 88, a.OK, rx=16), 50, 100, still=1)
en(a, ring(a, 596, IY - 44, 168, 88, a.BAD, rx=16), 52, 75)
en(a, mark(a, 760, IY - 44, ok=False, r=14), 52, 75)
en(a, a.text(320, IY - 6, "¿el destino es una IP", 15, a.INK, a.SANS, 600, "middle") + a.text(320, IY + 16, "del propio router?", 15, a.INK, a.SANS, 600, "middle"), 50, 75)

# paquete (un punto que se detiene entre etapas)
def dot(c):
    return f'<circle cx="0" cy="0" r="12" fill="{c}" stroke="#FFFFFF" stroke-width="3"/>'
go(a, "", [(150, MY), (215, MY)], 3, 9, hold=18, inner=dot(a.BLUE))
go(a, "", [(215, MY), (335, MY)], 27, 31, hold=0, inner=dot(a.BLUE))
go(a, "", [(335, MY), (440, MY)], 31, 35, hold=16, inner=dot(a.OK))
go(a, "", [(440, MY), (570, MY)], 52, 57, hold=19, inner=dot(a.OK))
go(a, "", [(570, MY), (795, MY), (1000, MY)], 77, 87, hold=13, inner=dot(a.OK))
fijo(a, at(dot(a.OK), 795, MY))

# contadores
a.add(a.box(48, 488, 1104, 110, a.WHITE, a.LINE, rx=14))
a.add(a.text(68, 518, "/ip/firewall/filter/print stats", 15, a.GREY, a.MONO))
a.add(a.text(68, 552, "chain=input   dst-port=18000", 15, a.INK, a.MONO, 600))
a.add(a.text(68, 582, "chain=forward dst-address=192.168.88.50 dst-port=8000", 15, a.INK, a.MONO, 600))
a.add(a.text(1000, 518, "PACKETS", 14, a.GREY, a.MONO, 600, "end"))
flip(a, 1000, 552, [(0, 100, "0", a.BAD)], size=16, anchor="end", still_idx=0)
flip(a, 1000, 582, [(0, 80, "0", a.GREY), (80, 88, "1", a.OK), (88, 94, "2", a.OK), (94, 100, "3", a.OK)], size=16, anchor="end", still_idx=3)
en(a, a.text(1030, 552, "nunca coincide", 15, a.BAD, a.SANS, 600), 52, 100, still=1)
en(a, a.text(1030, 582, "esta suma", 15, a.OK, a.SANS, 600), 80, 100, still=1)

narr(a, [
    (0, 25, "El técnico puso chain=input dst-port=18000 para limitar orígenes.", a.TXT),
    (25, 50, "El dst-nat trabaja antes del filter: cuando llega el filter, el destino ya es el NVR.", a.TXT),
    (50, 75, "Lo publicado nunca pasa por input: el router no es el destino.", a.BAD),
    (75, 100, "La regla va en forward, con la IP y el puerto del NVR.", a.OK),
], y=642, still_idx=3)

escribir(a, "4-r1.svg", "El NVR publicado cae en forward",
         "Animación en cuatro tiempos con el camino del paquete en el router: internet, prerouting con conntrack y dst-nat, la decisión de ruteo, input (para el router) "
         "o forward (a través), postrouting con src-nat y el NVR en 192.168.88.50 puerto 8000. Arriba, el encabezado del paquete; abajo, los contadores de dos reglas. "
         "1: desde un celular llega un paquete de 198.51.100.7 a 203.0.113.10 puerto 18000. 2: en prerouting, el dst-nat cambia el destino a 192.168.88.50 puerto 8000. "
         "3: la decisión de ruteo ve que el destino no es del router y lo manda a forward; la regla chain=input dst-port=18000 nunca coincide y queda en 0. "
         "4: el paquete sigue por forward y postrouting hasta el NVR, y la regla chain=forward dst-address=192.168.88.50 dst-port=8000 es la que suma.",
         [10, 38, 62, 85, 95])
