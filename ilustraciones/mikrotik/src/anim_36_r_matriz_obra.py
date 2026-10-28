#!/usr/bin/env python3
"""Lección 36 (Zonas con listas) · Resumen: el edificio de ejemplo, con paquetes entre zonas y el casillero de la matriz que decide cada uno."""
from _anim_r20_31 import *

a, _ = nuevo(26, "MIKROTIK · ZONAS CON LISTAS · EN LA RED", "Cada paquete entre zonas busca su casillero",
             ["ADMIN al NVR por 443: casillero ámbar, solo el NVR. Pasa.",
              "Una cámara sale a NTP y pasa; si quiere una web, drop final.",
              "INVITADOS a la red de cámaras: no hay casillero. Drop y log.",
              "Tu notebook en GESTION llega a todas las zonas."], still=2)

ZONES = {"ADMIN": (48, 196, "vlan10-admin"), "GESTION": (48, 336, "bridge"), "INVITADOS": (48, 476, "ether5"),
         "CCTV": (468, 196, "ether3 · NVR .20.50"), "WAN": (468, 476, "ether1")}
ZW, ZH = 178, 78
CX, CY = 348, 375
cen = {}
for z, (x, y, sub) in ZONES.items():
    ex = x + ZW if x < 300 else x
    cen[z] = (ex, y + ZH / 2)
    a.add(wire(ex, y + ZH / 2, CX, CY, a.LINE, 3))
for z, (x, y, sub) in ZONES.items():
    dev(a, x, y, ZW, ZH, z, sub, kind="isp" if z == "WAN" else "pc", ssize=14, tsize=18)
a.add(f'<circle cx="{CX}" cy="{CY}" r="54" fill="{a.INK}"/>')
a.add(a.text(CX, CY - 4, "router", 16, a.WHITE, a.HEAD, 600, "middle"))
a.add(a.text(CX, CY + 18, "forward", 14, SKY, a.MONO, 400, "middle"))

def dot(c):
    return f'<circle cx="0" cy="0" r="11" fill="{c}" stroke="#FFFFFF" stroke-width="3"/>'

def viaje(o, d, t0, c, corta=False, hold=4):
    p0, p1 = cen[o], cen[d]
    if corta:
        import math
        d = math.dist(p0, (CX, CY)); k = (d - 74) / d
        stop = (p0[0] + (CX - p0[0]) * k, p0[1] + (CY - p0[1]) * k)
        go(a, "", [p0, stop], t0, t0 + 4, hold=hold, inner=dot(c))
        en(a, mark(a, CX + 40, CY - 40, ok=False, r=15), t0 + 4, t0 + 4 + hold + 6)
    else:
        go(a, "", [p0, (CX, CY), p1], t0, t0 + 8, hold=hold, inner=dot(c))

# matriz
MX, MY0, HW, CW, RH = 680, 186, 150, 80, 50
COLS = ["WAN", "ADMIN", "CCTV", "INVIT."]
ROWS = ["GESTION", "ADMIN", "CCTV", "INVITADOS"]
CELLS = [["sí", "sí", "sí", "sí"],
         ["sí", ".", "NVR", "no"],
         ["NTP", "no", ".", "no"],
         ["sí", "no", "no", "."]]
a.add(a.text(MX, MY0 - 6, "de \\ a", 14, a.GREY, a.MONO))
for j, c in enumerate(COLS):
    a.add(a.text(MX + HW + j * CW + CW / 2, MY0 + 30, c, 14, a.INK, a.MONO, 600, "middle"))
def cell_xy(i, j):
    return MX + HW + j * CW, MY0 + 44 + i * RH
for i, r in enumerate(ROWS):
    y = MY0 + 44 + i * RH
    a.add(a.text(MX, y + 31, r, 15, a.INK, a.MONO, 600))
    for j, v in enumerate(CELLS[i]):
        x, _y = cell_xy(i, j)
        fg, bg = {"sí": (a.OK, a.OKBG), "no": (a.BAD, a.BADBG), ".": (a.GREY, a.SLATE)}.get(v, (a.AMB, a.AMBBG))
        a.add(a.box(x + 3, y + 3, CW - 6, RH - 6, bg, rx=8))
        a.add(a.text(x + CW / 2, y + 31, v, 15, fg, a.MONO, 600, "middle"))

def celda(i, j, t0, t1, c, still=0):
    x, y = cell_xy(i, j)
    en(a, ring(a, x, y, CW, RH, c, rx=10, sw=3.5), t0, t1, still)

# 1. ADMIN al NVR
viaje("ADMIN", "CCTV", 2, a.AMB, hold=8)
celda(1, 2, 6, 25, a.AMB)
# 2. cámara: NTP pasa, web no
viaje("CCTV", "WAN", 27, a.AMB, hold=6)
celda(2, 0, 30, 50, a.AMB)
viaje("CCTV", "WAN", 40, a.BAD, corta=True, hold=3)
en(a, a.text(CX, 462, "web: no está en NTP", 15, a.BAD, a.MONO, 600, "middle"), 45, 50)
en(a, a.text(CX, 462, "NTP: udp 123", 15, a.AMB, a.MONO, 600, "middle"), 31, 44)
# 3. INVITADOS a CCTV
viaje("INVITADOS", "CCTV", 52, a.BAD, corta=True, hold=12)
celda(3, 2, 56, 75, a.BAD, still=1)
fijo(a, at(dot(a.BAD), 288, 429))
# 4. GESTION a todas
viaje("GESTION", "CCTV", 77, a.OK, hold=12)
viaje("GESTION", "WAN", 79, a.OK, hold=10)
viaje("GESTION", "ADMIN", 81, a.OK, hold=8)
en(a, ring(a, MX + HW, MY0 + 44, 4 * CW, RH, a.OK, rx=10, sw=3.5), 78, 100)

# log
a.add(a.box(680, 460, 472, 140, a.INK, rx=12))
a.add(a.text(698, 488, '/log/print where message~"ZONA-DROP"', 14, SKY, a.MONO))
en(a, a.text(698, 516, "ZONA-DROP forward: in:ether3 out:ether1,", 14, ROSE, a.MONO, 600) + a.text(698, 538, "  … 10.10.20.21:51234->203.0.113.80:443", 14, ROSE, a.MONO), 45, 100, still=1)
en(a, a.text(698, 562, "ZONA-DROP forward: in:ether5 out:ether3,", 14, ROSE, a.MONO, 600) + a.text(698, 584, "  … proto ICMP, 10.10.40.10->10.10.20.50", 14, ROSE, a.MONO), 60, 100, still=1)
en(a, a.text(698, 520, "(vacío)", 14, SKY, a.MONO), 0, 45)

narr(a, [
    (0, 25, "in-interface-list dice de qué zona viene; out-interface-list, a cuál va.", a.TXT),
    (25, 50, "Un casillero ámbar es una regla con algo más: un puerto o una IP.", a.AMB),
    (50, 75, "Los casilleros rojos no se escriben: lo que no coincide baja al drop final.", a.BAD),
    (75, 100, "Una VLAN nueva entra a su lista y hereda su fila de la matriz.", a.OK),
], still_idx=2)

escribir(a, "36-r1.svg", "Paquetes entre zonas y la matriz",
         "Animación en cuatro tiempos. A la izquierda, el router con cinco zonas: ADMIN (vlan10-admin), GESTION (bridge), INVITADOS (ether5), CCTV (ether3, con el NVR en 10.10.20.50) y WAN (ether1). "
         "A la derecha, la matriz de zonas: GESTION llega a todas; ADMIN sale a WAN y llega solo al NVR; CCTV sale a WAN solo por NTP; INVITADOS solo sale a WAN. Abajo, el log con el prefijo ZONA-DROP. "
         "1: un paquete de ADMIN al NVR por 443 coincide con el casillero ámbar y pasa. 2: una cámara sale a NTP y pasa; cuando pide una web, no coincide con nada y la corta el drop final, que deja una línea en el log. "
         "3: un paquete de INVITADOS hacia la red de cámaras no tiene casillero: drop final y otra línea ZONA-DROP. 4: la notebook en GESTION llega a CCTV, WAN y ADMIN.",
         [10, 38, 47, 62, 90])
