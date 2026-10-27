#!/usr/bin/env python3
"""Lección 25 · Bridges. Teoría "Cómo funciona": el bridge anota la MAC de origen de cada trama y el puerto;
a una MAC conocida la manda solo por su puerto; si no la conoce o es broadcast, inunda. Lo que es para el router
sube por el bridge.
"""
from _anim_mikrotik_14_26 import Anim, out

a = Anim(T=26, kicker="MIKROTIK · BRIDGE", title="El bridge aprende de dónde viene cada MAC")
a.steps([
    "A le manda a B. El bridge anota la MAC de A en ether2. No conoce a B: inunda.",
    "B contesta. El bridge anota B en ether4 y ya conoce A: sale solo por ether2.",
    "A vuelve a mandarle a B: ahora sale solo por ether4.",
    "Un broadcast va a todos los puertos y sube al router por el bridge.",
], still=2)

# router (CPU) y bridge
a.add(a.box(250, 180, 600, 60, a.WHITE, a.LINE, rx=14))
a.add(a.text(550, 208, "Router: IP, servidor DHCP, DNS", 18, a.INK, a.HEAD, 600, "middle"))
a.add(a.text(550, 230, "lo que es para él sube por el bridge", 15, a.GREY, a.SANS, 400, "middle"))
a.add(f'<line x1="550" y1="240" x2="550" y2="268" stroke="{a.LINE}" stroke-width="3"/>')
BX, BY, BW, BH = 250, 268, 600, 62
a.add(a.box(BX, BY, BW, BH, a.INK, rx=14))
a.add(a.text(550, BY + 38, "bridge · interfaz maestra", 18, a.WHITE, a.MONO, 600, "middle"))
PORTS = [("ether2", "A", 330), ("ether3", "C", 470), ("ether4", "B", 630), ("ether5", "D", 770)]
PY, DY = 352, 452
for p, d, x in PORTS:
    a.add(f'<line x1="{x}" y1="{BY + BH}" x2="{x}" y2="{DY}" stroke="{a.LINE}" stroke-width="3"/>')
    a.add(a.pill(x, PY, p, a.INK, a.SLATE, 15, 30, "middle"))
    a.add(a.box(x - 62, DY, 124, 72, a.WHITE, a.LINE, rx=14))
    a.add(a.text(x, DY + 32, f"Equipo {d}", 17, a.INK, a.HEAD, 600, "middle"))
    a.add(a.text(x, DY + 56, f"MAC {d}", 15, a.GREY, a.MONO, 400, "middle"))

# tabla de hosts
TX, TY, TW = 900, 180, 252
a.add(a.box(TX, TY, TW, 344, a.WHITE, a.LINE, rx=16))
a.add(a.text(TX + 18, TY + 34, "tabla de hosts", 18, a.INK, a.HEAD, 600))
a.add(a.text(TX + 18, TY + 58, "/interface/bridge/host", 15, a.GREY, a.MONO))
a.add(a.text(TX + 18, TY + 92, "MAC", 15, a.GREY, a.MONO))
a.add(a.text(TX + TW - 18, TY + 92, "puerto", 15, a.GREY, a.MONO, 400, "end"))


def hrow(i, mac, port, on):
    y = TY + 106 + i * 56
    a.add(a.group(a.box(TX + 12, y, TW - 24, 46, a.SLATE, rx=10) + a.text(TX + 26, y + 29, mac, 17, a.INK, a.MONO, 600)
                  + a.text(TX + TW - 26, y + 29, port, 17, a.BLUE, a.MONO, 600, "end"), a.show(on, 100), still=1 if on < 50 else 0))
    a.add(a.group(a.box(TX + 12, y, TW - 24, 46, "none", a.OK, rx=10, sw=3), a.show(on, on + 6), still=0))


hrow(0, "MAC A", "ether2", 7)
hrow(1, "MAC B", "ether4", 33)
hrow(2, "MAC C", "ether3", 82)
a.add(a.group(a.text(TX + 18, TY + 320, "la arma sola, sin configurar", 15, a.TXT, a.SANS, 600), a.show(0, 100), still=1))

XC = 550
YB = BY + BH / 2
X = {d: x for _, d, x in PORTS}
YD = DY + 6


def frame(src, dsts, t, col, up=False, label=""):
    """Trama de src al bridge (t..t+5) y del bridge a dsts (t+6..t+11)."""
    xs = X[src]
    mv = a.move([(0, xs, YD), (t, xs, YD), (t + 2.5, xs, YB), (t + 5, XC, YB), (100, XC, YB)])
    a.add(a.group(a.group(f'<circle r="11" fill="{col}" stroke="#FFFFFF" stroke-width="3"/>', mv, still=None), a.show(t, t + 5.4, 0.3), still=0))
    for d in dsts:
        xd = X[d]
        mv = a.move([(0, XC, YB), (t + 6, XC, YB), (t + 8.5, xd, YB), (t + 11, xd, YD), (100, xd, YD)])
        a.add(a.group(a.group(f'<circle r="11" fill="{col}" stroke="#FFFFFF" stroke-width="3"/>', mv, still=None), a.show(t + 6, t + 11.4, 0.3), still=0))
    if up:
        mv = a.move([(0, XC, YB), (t + 6, XC, YB), (t + 10, XC, 210), (100, XC, 210)])
        a.add(a.group(a.group(f'<circle r="11" fill="{col}" stroke="#FFFFFF" stroke-width="3"/>', mv, still=None), a.show(t + 6, t + 10.4, 0.3), still=0))


frame("A", ["C", "B", "D"], 2, a.CYAN)
frame("B", ["A"], 28, a.OK)
frame("A", ["B"], 53, a.CYAN)
frame("C", ["A", "B", "D"], 77, a.AMB, up=True)

# etiqueta por tiempo
NY = 590
NOTES = [
    (0, 25, a.CYAN, "trama de A para B", "MAC B desconocida: sale por todos los puertos menos ether2."),
    (25, 50, a.OK, "trama de B para A", "MAC A está en la tabla: sale solo por ether2."),
    (50, 75, a.CYAN, "trama de A para B", "Las dos MAC son conocidas: C y D no se enteran."),
    (75, 100, a.AMB, "broadcast de C", "Por ejemplo un pedido DHCP: va a todos y el router lo atiende en el bridge."),
]
for s_, e, col, t1, t2 in NOTES:
    a.add(a.group(a.box(48, NY - 30, 1104, 74, a.WHITE, a.LINE, rx=14)
                  + f'<circle cx="80" cy="{NY + 7}" r="11" fill="{col}"/>'
                  + a.text(104, NY + 13, t1, 17, a.INK, a.MONO, 600)
                  + a.text(360, NY + 13, t2, 17, a.TXT, a.SANS, 600), a.show(s_, e), still=1 if s_ == 50 else 0))

# cuadro fijo: la trama de A va solo a B
_off = a.keyframes([(0, 0), (100, 0)])
a.add(a.group(a.arrow(f"M{X['A']} {DY - 4} V{BY + BH - 12} H{X['B'] - 16} ", a.CYAN, 3.5)
              + a.arrow(f"M{X['B']} {BY + BH - 4} V{DY - 6}", a.CYAN, 3.5), _off, still=1))

out(a, 25, 1, "El bridge aprende las MAC",
    "Animación en cuatro tiempos con un bridge, sus puertos ether2 a ether5 y un equipo en cada uno (A, C, B y D), más la tabla de hosts. "
    "1: A le manda una trama a B; el bridge anota MAC A en ether2 y, como no conoce MAC B, la inunda por todos los demás puertos. "
    "2: B contesta; el bridge anota MAC B en ether4 y, como conoce MAC A, manda la trama solo por ether2. "
    "3: A vuelve a mandarle a B y la trama sale solo por ether4; C y D no se enteran. "
    "4: C manda un broadcast, por ejemplo un pedido DHCP; el bridge anota MAC C en ether3, lo manda a todos los puertos y también sube al router, que atiende en el bridge.",
    [8, 37, 62, 88])
