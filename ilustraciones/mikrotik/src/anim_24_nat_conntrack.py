#!/usr/bin/env python3
"""Lección 24 · Port forwarding. Teoría "Cómo funciona": dstnat antes de la ruta, forward con la marca dstnat,
connection tracking guarda la traducción y deshace el cambio en la respuesta; solo el primer paquete recorre el NAT.
"""
from _anim_mikrotik_14_26 import Anim, node, out

a = Anim(T=28, kicker="MIKROTIK · PORT FORWARDING", title="Ida, vuelta y lo que guarda connection tracking")
a.steps([
    "Llega el primer paquete a 203.0.113.10:18000. dstnat cambia el destino.",
    "Recién ahí la ruta: ya no es para el router, va por forward y pasa.",
    "Connection tracking guarda la traducción de esta conexión.",
    "El NVR contesta. El router hace el cambio inverso.",
    "El resto de la conexión usa lo guardado: el contador del NAT no sube.",
], still=4)

Y, H = 222, 84
a.add(node(a, 48, Y, 200, H, "App o iVMS", "198.51.100.20"))
a.add(node(a, 952, Y, 200, H, "NVR", "192.168.88.50:8000"))
RX, RY, RW, RH = 276, 176, 648, 330
a.add(a.box(RX, RY, RW, RH, a.INK, rx=18))
a.add(a.text(RX + 20, RY + 30, "MikroTik · ether1 203.0.113.10", 16, "#9FC3E3", a.MONO, 600))
STG = [("dstnat", "antes de la ruta", 296), ("ruteo", "¿para quién es?", 504), ("forward", "filtro", 712)]
for n, sub, x in STG:
    a.add(a.box(x, Y, 192, H, a.NAVY2, rx=12))
    a.add(a.text(x + 96, Y + 32, n, 19, a.WHITE, a.MONO, 600, "middle"))
    a.add(a.text(x + 96, Y + 55, sub, 15, "#9FC3E3", a.SANS, 400, "middle"))
HL = [(296, 2, 20), (504, 21, 30), (712, 30, 40)]
for x, s_, e in HL:
    a.add(a.group(a.box(x, Y, 192, H, "none", "#FFD28A", rx=12, sw=3.5), a.show(s_, e, 0.6), still=0))
# contador del NAT
a.add(a.group(a.text(392, Y + 77, "contador: 0", 15, "#C9DDF0", a.MONO, 400, "middle"), a.show(0, 9), still=0))
a.add(a.group(a.text(392, Y + 77, "contador: 1", 15, "#FFD28A", a.MONO, 600, "middle"), a.show(9, 100), still=1))

# connection tracking
CX, CY, CW, CH = 296, 320, 608, 172
a.add(a.box(CX, CY, CW, CH, a.NAVY2, rx=12))
a.add(a.text(CX + 18, CY + 30, "connection tracking", 17, a.WHITE, a.MONO, 600))
row = (a.text(CX + 18, CY + 70, "198.51.100.20  →  203.0.113.10:18000", 16, "#C9DDF0", a.MONO, 400)
       + a.text(CX + 18, CY + 100, "se traduce a       192.168.88.50:8000", 16, "#5BE0A5", a.MONO, 600)
       + a.text(CX + 18, CY + 140, "la respuesta se deshace al revés", 15, "#9FC3E3", a.SANS, 600))
a.add(a.group(row, a.show(41, 100), still=1))
a.add(a.group(a.box(CX, CY, CW, CH, "none", "#5BE0A5", rx=12, sw=3.5), a.show(41, 52), still=0))
a.add(a.group(a.box(CX, CY, CW, CH, "none", "#FFD28A", rx=12, sw=3.5), a.show(66, 72), still=0))
a.add(a.group(a.box(CX, CY, CW, CH, "none", "#FFD28A", rx=12, sw=3.5), a.show(81, 100), still=1))

a.add(a.group(a.pill(760, CY + 62, "connection-nat-state=dstnat: pasa", a.OK, a.OKBG, 15, 28, "middle"), a.show(31, 42), still=0))
a.add(a.group(a.pill(600, CY + 62, "ya no es para el router", a.AMB, a.AMBBG, 15, 28, "middle"), a.show(22, 31), still=0))

# punto que viaja (por el centro de las cajas)
LY = Y + H / 2
xs = {"app": 148, "dst": 392, "rt": 600, "fw": 808, "nvr": 1052}


def dot(pts, on, off, col):
    mv = a.move([(p, xs[k] if isinstance(k, str) else k, LY if y is None else y) for p, k, y in pts])
    a.add(a.group(a.group(f'<circle r="11" fill="{col}" stroke="#FFFFFF" stroke-width="3"/>', mv, still=None), a.show(on, off, 0.4), still=0))


dot([(0, "app", None), (2, "app", None), (8, "dst", None), (21, "dst", None), (25, "rt", None), (30, "rt", None), (34, "fw", None), (37, "fw", None), (40, "nvr", None), (100, "nvr", None)], 2, 40.5, a.CYAN)
dot([(0, "nvr", None), (61, "nvr", None), (66, 600, CY + 120), (72, 600, CY + 120), (79, "app", None), (100, "app", None)], 61, 79.5, a.OK)
for t in (82, 88, 94):
    dot([(0, "app", None), (t, "app", None), (t + 2, 600, CY + 120), (t + 4, "nvr", None), (100, "nvr", None)], t, t + 4.3, a.CYAN)

# cabecera del paquete
PY = 532
a.add(a.box(48, PY, 1104, 104, a.WHITE, a.LINE, rx=16))
a.add(a.text(72, PY + 40, "origen", 15, a.GREY, a.MONO))
a.add(a.text(560, PY + 40, "destino", 15, a.GREY, a.MONO))
HDR = [
    (0, 10, "198.51.100.20", "203.0.113.10:18000", "llega de afuera", a.INK),
    (10, 60, "198.51.100.20", "192.168.88.50:8000", "después de dstnat", a.BLUE),
    (60, 68, "192.168.88.50:8000", "198.51.100.20", "contesta el NVR", a.INK),
    (68, 80, "203.0.113.10:18000", "198.51.100.20", "cambio inverso: la app ve a quien llamó", a.OK),
    (80, 100, "198.51.100.20", "192.168.88.50:8000", "paquetes siguientes: sin pasar por las reglas", a.BLUE),
]
for s_, e, o, d, note, col in HDR:
    a.add(a.group(a.text(72, PY + 76, o, 22, col, a.MONO, 600) + a.text(560, PY + 76, d, 22, col, a.MONO, 600)
                  + a.text(1128, PY + 40, note, 15, col, a.SANS, 600, "end"), a.show(s_, e, 0.6), still=1 if s_ == 80 else 0))

out(a, 24, 1, "Port forwarding: ida, vuelta y connection tracking",
    "Animación en cinco tiempos entre la app (198.51.100.20), el MikroTik (ether1 203.0.113.10) y el NVR 192.168.88.50. "
    "1: llega el primer paquete a 203.0.113.10:18000; en la cadena dstnat, antes de la ruta, el destino pasa a 192.168.88.50:8000 y el contador de la regla sube a 1. "
    "2: recién ahí el ruteo decide: ya no es para el router, va por forward, que lo deja pasar por la marca connection-nat-state=dstnat, y llega al NVR. "
    "3: connection tracking guarda la traducción de esa conexión. "
    "4: el NVR contesta desde 192.168.88.50:8000; el router hace el cambio inverso y la app ve que le contesta 203.0.113.10:18000. "
    "5: el resto de los paquetes de la conexión se traducen con lo guardado, sin recorrer las reglas de NAT: el contador sigue en 1.",
    [5, 26, 50, 75, 90])
