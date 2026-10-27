#!/usr/bin/env python3
"""Lección 27, teoría "Ida y vuelta": la sucursal llega a la central, pero la respuesta necesita su ruta de vuelta.
Cinco tiempos (24 s). Cuadro fijo: tiempo 5, con la ruta de vuelta puesta.
"""
from _anim_mt2739 import escribir, Anim, SITE, PREV, en, ventanas, fijo, paquete, nodo, marca, narr, LIGHT

a = Anim(T=24, kicker="MIKROTIK · RUTAS", title="Ida y vuelta: cada router decide solo por su tabla")
a.steps([
    "La PC de la sucursal le escribe al servidor de la central.",
    "La sucursal tiene ruta: el paquete entra al túnel y llega.",
    "El servidor contesta, pero la central no conoce 192.168.88.0/24.",
    "Agregás en la central la ruta de vuelta por el túnel.",
    "Ahora la respuesta vuelve por el túnel: ida y vuelta.",
], still=4)

# ---- nodos
NY, NH = 176, 82
nodo(a, 48, NY, 190, NH, "PC sucursal", "192.168.88.254", dark=False)
nodo(a, 280, NY, 220, NH, "Sucursal", "LAN 192.168.88.0/24")
nodo(a, 680, NY, 220, NH, "Central", "LAN 192.168.20.0/24")
nodo(a, 962, NY, 190, NH, "Servidor", "192.168.20.15", dark=False)
a.add(a.text(590, 222, "túnel L2TP", 16, a.BLUE, a.MONO, 600, "middle"))

# ---- carril
LY = 304
for cx in (143, 390, 790, 1057):
    a.add(f'<line x1="{cx}" y1="{NY + NH}" x2="{cx}" y2="{LY}" stroke="{a.LINE}" stroke-width="3"/>')
a.add(f'<line x1="143" y1="{LY}" x2="1057" y2="{LY}" stroke="{a.LINE}" stroke-width="3"/>')
a.add(a.box(500, LY - 22, 180, 44, "#E4F3FA", a.CYAN, rx=22, sw=2))

# ---- ISP
a.add(a.box(500, 486, 180, 70, a.WHITE, a.LINE, rx=16))
a.add(a.text(590, 517, "ISP · internet", 17, a.INK, a.HEAD, 600, "middle"))
a.add(a.text(590, 541, "ruta por defecto", 15, a.GREY, a.MONO, 400, "middle"))

# ---- tablas
TY, TW, RH = 352, 422, 46
def tabla(x, nombre):
    a.add(a.box(x, TY, TW, 226, a.WHITE, a.LINE, rx=16))
    a.add(a.text(x + 20, TY + 30, nombre, 18, a.INK, a.HEAD, 600))
    a.add(a.text(x + TW - 20, TY + 30, "/ip/route", 15, a.GREY, a.MONO, 400, "end"))

def fila(x, i, dst, gw, fill=None, col=None):
    y = TY + 46 + i * RH
    return (a.box(x + 12, y, TW - 24, 38, fill or a.SLATE, rx=10)
            + a.text(x + 26, y + 25, dst, 16, col or a.INK, a.MONO, 600)
            + a.text(x + 196, y + 25, gw, 16, col or a.TXT, a.MONO))

SX, CX = 48, 730
tabla(SX, "Sucursal")
tabla(CX, "Central")
for i, (d, g) in enumerate([("0.0.0.0/0", "ISP"), ("192.168.88.0/24", "bridge"), ("192.168.20.0/24", "l2tp-central")]):
    a.add(fila(SX, i, d, g))
for i, (d, g) in enumerate([("0.0.0.0/0", "ISP"), ("192.168.20.0/24", "bridge")]):
    a.add(fila(CX, i, d, g))

# fila que falta en la central (tiempos 1 a 3) y la que se agrega (4 y 5)
y3 = TY + 46 + 2 * RH
en(a, f'<rect x="{CX + 12}" y="{y3}" width="{TW - 24}" height="38" rx="10" fill="none" stroke="{a.GREY}" stroke-width="2" stroke-dasharray="6 5"/>'
      + a.text(CX + 26, y3 + 25, "sin ruta a 192.168.88.0/24", 16, a.GREY, a.MONO), 0, 61)
en(a, fila(CX, 2, "192.168.88.0/24", "l2tp-sucursal", a.OKBG, a.OK), 61, 100, still=1)

# resaltados de filas
def borde(x, i, color):
    y = TY + 46 + i * RH
    return f'<rect x="{x + 10}" y="{y - 2}" width="{TW - 20}" height="42" rx="11" fill="none" stroke="{color}" stroke-width="3"/>'
en(a, borde(SX, 2, a.CYAN), 8, 22)
en(a, borde(CX, 1, a.CYAN), 30, 39)
en(a, borde(CX, 0, a.BAD), 46, 59)
en(a, borde(CX, 2, a.OK), 62, 79)
en(a, borde(CX, 2, a.OK), 84, 92)
en(a, borde(SX, 1, a.OK), 92, 99)

# ---- paquetes
IDA = "→ 192.168.20.15"
VUE = "→ 192.168.88.254"
paquete(a, IDA, [(1, 143, LY), (7, 390, LY), (21, 390, LY), (28, 790, LY), (33, 1057, LY), (39, 1057, LY)], 1, 39)
paquete(a, VUE, [(41, 1057, LY), (46, 790, LY), (48.5, 790, LY), (50.5, 700, LY), (54, 590, 408), (59, 590, 408)], 41, 58, bg=a.BAD)
paquete(a, VUE, [(81, 1057, LY), (85, 790, LY), (91, 390, LY), (95, 143, LY), (99.5, 143, LY)], 81, 99.5, bg=a.OK)

en(a, a.arrow("M712 330 L652 382", a.BAD, 3, "7 6"), 49, 59)
en(a, marca(a, 590, 452, ok=False), 54, 60)
en(a, marca(a, 256, LY, ok=True), 95, 100, still=1)
en(a, marca(a, 940, LY, ok=True), 33, 40)

# cuadro fijo: la respuesta ya llegó a la PC
from _anim_mt2739 import pill_c
fijo(a, f'<g transform="translate(143 {LY})">' + pill_c(a, VUE, "#FFFFFF", a.OK) + "</g>")

narr(a, [
    (0, 20, "La sucursal busca 192.168.20.15 en su tabla: la /24 por l2tp-central.", a.TXT),
    (20, 40, "La central entrega al servidor por su red conectada.", a.TXT),
    (40, 60, "Sin ruta a la sucursal, la respuesta sale por la ruta por defecto y no vuelve.", a.BAD),
    (60, 80, "En la central: 192.168.88.0/24 con gateway la interfaz del túnel.", a.OK),
    (80, 100, "Cada ruta hacia allá necesita su ruta de vuelta en la otra punta.", a.OK),
], still_idx=4)

escribir(a, f"{SITE}/27-t1.svg", "Ida y vuelta por un túnel",
        "Animación en cinco tiempos. 1: la PC de la sucursal, 192.168.88.254, manda un paquete al servidor 192.168.20.15 de la central; "
        "la sucursal lo encuentra en su tabla, ruta 192.168.20.0/24 por l2tp-central. 2: el paquete cruza el túnel L2TP y la central lo entrega al servidor por su red conectada. "
        "3: el servidor contesta a 192.168.88.254, pero la central no tiene ruta a 192.168.88.0/24; la respuesta sale por la ruta por defecto hacia el ISP y no vuelve. "
        "4: se agrega en la central la ruta 192.168.88.0/24 con gateway la interfaz del túnel, l2tp-sucursal. 5: la respuesta vuelve por el túnel y llega a la PC. "
        "Cada router decide solo por su tabla: cada ruta hacia allá necesita su ruta de vuelta.",
        [10, 30, 52, 57, 70, 90], f"{PREV}/_t27")
