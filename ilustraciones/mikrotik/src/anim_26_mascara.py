#!/usr/bin/env python3
"""Lección 26 · Asignar IP. Teoría "Cómo funciona": la máscara, el AND entre dirección y máscara, la ruta conectada
y la decisión: destino dentro de la red, directo por ARP; fuera, a un gateway.
"""
from _anim_mikrotik_14_26 import Anim, out

a = Anim(T=26, kicker="MIKROTIK · DIRECCIONES", title="La máscara decide qué es red y qué es host")
a.steps([
    "/24: los primeros 24 bits son la red. Los 8 que quedan, hosts.",
    "Dirección AND máscara: la red es 10.10.20.0. La última, .255, es el broadcast.",
    "Con solo cargar la IP aparece una ruta conectada DAc, distancia 0.",
    "Destino 10.10.20.50: cae en la red. El router lo busca directo por ARP.",
    "Destino 10.10.30.5: no cae en la red. Va a un gateway.",
], still=1)

a.add(a.text(48, 196, "/ip/address/add address=10.10.20.1/24 interface=ether5", 17, a.INK, a.MONO, 600))

PX, PY, PW, PH = 48, 216, 720, 216
a.add(a.box(PX, PY, PW, PH, a.WHITE, a.LINE, rx=16))
BX = PX + 168
CW = 10.2  # ancho de carácter mono 17


def bits(octs):
    return ".".join(f"{o:08b}" for o in octs)


# bandas red / host
a.add(a.group(a.box(BX - 6, PY + 14, 26 * CW + 3, PH - 28, a.BLUE, rx=8, extra='fill-opacity=".08"')
              + a.box(BX + 27 * CW - 4, PY + 14, 8 * CW + 8, PH - 28, a.AMB, rx=8, extra='fill-opacity=".12"')
              + a.text(BX + 13 * CW, PY + PH + 24, "red: 24 bits", 15, a.BLUE, a.MONO, 600, "middle")
              + a.text(BX + 31 * CW, PY + PH + 24, "hosts: 8", 15, a.AMB, a.MONO, 600, "middle"),
              a.show(1, 100), still=1))
ROWS = [("dirección", (10, 10, 20, 1), "10.10.20.1", a.INK, 0),
        ("máscara /24", (255, 255, 255, 0), "255.255.255.0", a.GREY, 0),
        ("AND = red", (10, 10, 20, 0), "10.10.20.0", a.BLUE, 22)]
for i, (lab, o, dec, col, on) in enumerate(ROWS):
    y = PY + 52 + i * 62
    a.add(a.text(PX + 20, y, lab, 15, a.GREY, a.MONO))
    inner = a.text(BX, y, bits(o), 17, col, a.MONO, 600) + a.text(PX + PW - 20, y, dec, 17, col, a.MONO, 600, "end")
    if on:
        a.add(f'<line x1="{PX + 16}" y1="{y - 34}" x2="{PX + PW - 16}" y2="{y - 34}" stroke="{a.LINE}" stroke-width="2"/>')
        a.add(a.group(inner, a.show(on, 100), still=1))
    else:
        a.add(inner)

# lo que calcula
RX, RY, RW = 800, 180, 352
a.add(a.box(RX, RY, RW, 252, a.INK, rx=16))
a.add(a.text(RX + 20, RY + 34, "Lo que sale de ahí", 18, a.WHITE, a.HEAD, 600))
CAL = [("red", "10.10.20.0", 24), ("hosts", ".1 a .254", 27), ("broadcast", "10.10.20.255", 30)]
for i, (k, v, on) in enumerate(CAL):
    y = RY + 72 + i * 34
    a.add(a.group(a.text(RX + 20, y, k, 15, "#9FC3E3", a.MONO) + a.text(RX + RW - 20, y, v, 16, a.WHITE, a.MONO, 600, "end"), a.show(on, 100), still=1))
a.add(a.group(a.box(RX + 14, RY + 172, RW - 28, 64, a.NAVY2, rx=10)
              + a.text(RX + 28, RY + 198, "DAc 10.10.20.0/24 ether5", 16, "#5BE0A5", a.MONO, 600)
              + a.text(RX + 28, RY + 222, "ruta conectada · distancia 0", 15, "#C9DDF0", a.MONO), a.show(41, 100), still=0))
a.add(a.group(a.box(RX + 14, RY + 172, RW - 28, 64, "none", "#5BE0A5", rx=10, sw=3), a.show(41, 52), still=0))

# decisión
DY = 486
a.add(a.box(48, DY, 1104, 150, a.WHITE, a.LINE, rx=16))
a.add(a.text(72, DY + 36, "¿El destino cae en 10.10.20.0/24?", 18, a.INK, a.HEAD, 600))
a.add(a.group(a.text(72, DY + 36, "", 1), a.show(0, 60), still=0))
DEC = [
    (60, 80, "10.10.20.50", "AND /24 = 10.10.20.0", "sí: está en la red", "directo: ARP, ¿quién tiene 10.10.20.50?", a.OK),
    (80, 100, "10.10.30.5", "AND /24 = 10.10.30.0", "no: es otra red", "lo manda a un gateway", a.BAD),
]
for s_, e, ip, andv, verdict, act, col in DEC:
    a.add(a.group(a.pill(72, DY + 58, "→ " + ip, a.WHITE, a.CYAN, 17, 36)
                  + a.text(300, DY + 83, andv, 17, a.INK, a.MONO, 600)
                  + a.text(620, DY + 83, verdict, 17, col, a.SANS, 600)
                  + a.text(72, DY + 128, act, 18, col, a.MONO, 600), a.show(s_, e), still=0))
a.add(a.group(a.text(72, DY + 90, "Cada IP de una interfaz habilitada define una red conectada.", 17, a.TXT, a.SANS, 600)
              + a.text(72, DY + 122, "Adentro de esa red, el router llega directo. Afuera, necesita un gateway.", 17, a.TXT, a.SANS, 600),
              a.show(0, 60), still=1))

out(a, 26, 1, "Máscara, red y decisión de envío",
    "Animación en cinco tiempos sobre la dirección 10.10.20.1/24 en ether5. "
    "1: la máscara /24 marca los primeros 24 bits como red y los 8 restantes como hosts. "
    "2: la dirección (00001010.00001010.00010100.00000001) AND la máscara (255.255.255.0) da la red 10.10.20.0; los hosts van de .1 a .254 y 10.10.20.255 es el broadcast. "
    "3: con solo cargar la IP aparece la ruta conectada DAc 10.10.20.0/24 por ether5 con distancia 0. "
    "4: un destino 10.10.20.50 AND /24 da 10.10.20.0, cae en la red y el router lo busca directo por ARP. "
    "5: un destino 10.10.30.5 AND /24 da 10.10.30.0, es otra red y el router lo manda a un gateway.",
    [10, 32, 48, 70, 90])
