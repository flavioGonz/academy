#!/usr/bin/env python3
"""Lección 20 · Concentrador CHR. Teoría "Cómo funciona": el túnel saliente atraviesa el CGNAT porque el NAT anota
la conexión que abrió el sitio; esa anotación vence sin tráfico, y persistent-keepalive=25s la mantiene viva.
"""
from _anim_mikrotik_14_26 import Anim, node, packet, out

a = Anim(T=28, kicker="MIKROTIK · CONCENTRADOR CHR", title="El sitio abre el camino y el keepalive lo mantiene")
a.steps([
    "El sitio manda un paquete al CHR. El NAT del proveedor anota la conexión.",
    "El CHR contesta por el mismo camino y el NAT lo deja pasar.",
    "Sin tráfico la anotación vence. El hub ya no puede llegar al sitio.",
    "Con persistent-keepalive=25s el sitio manda un paquete chico cada 25 s.",
    "La anotación sigue viva: el hub llega al sitio cuando quieras entrar.",
], still=4)

Y = 178
a.add(node(a, 48, Y, 260, 84, "Router del sitio", "wg-central · 10.10.10.2"))
a.add(node(a, 470, Y, 260, 84, "NAT o CGNAT", "del proveedor"))
a.add(node(a, 892, Y, 260, 84, "CHR", "wg-hub · 198.51.100.20", dark=True))
LANE = 312
SX, NX, HX = 178, 600, 1022
a.add(f'<line x1="{SX}" y1="{LANE}" x2="{HX}" y2="{LANE}" stroke="{a.LINE}" stroke-width="2.5" stroke-dasharray="5 7"/>')
for x in (SX, NX, HX):
    a.add(f'<line x1="{x}" y1="{Y + 84}" x2="{x}" y2="{LANE}" stroke="{a.LINE}" stroke-width="2.5"/>')

# tabla de anotaciones del NAT
TX, TY, TW, TH = 330, 362, 540, 150
a.add(a.box(TX, TY, TW, TH, a.WHITE, a.LINE, rx=16))
a.add(a.text(TX + 22, TY + 34, "Lo que anotó el NAT", 19, a.INK, a.HEAD, 600))
a.add(a.group(a.box(TX + 16, TY + 52, TW - 32, 52, a.SLATE, rx=10)
              + a.text(TX + 32, TY + 84, "IP interna · puerto · IP externa", 16, a.INK, a.MONO, 600)
              + a.text(TX + TW - 32, TY + 84, "→ CHR :13231", 16, a.BLUE, a.MONO, 600, "end"),
              a.show(6, 50), still=1))
a.add(a.group(a.box(TX + 16, TY + 52, TW - 32, 52, a.SLATE, rx=10)
              + a.text(TX + 32, TY + 84, "IP interna · puerto · IP externa", 16, a.INK, a.MONO, 600)
              + a.text(TX + TW - 32, TY + 84, "→ CHR :13231", 16, a.BLUE, a.MONO, 600, "end"),
              a.show(62, 100), still=0))
a.add(a.group(a.box(TX + 16, TY + 52, TW - 32, 52, a.BADBG, rx=10)
              + a.text(TX + TW / 2, TY + 84, "vencida: no queda nada anotado", 16, a.BAD, a.MONO, 600, "middle"),
              a.show(50, 62), still=0))
a.add(a.group(a.text(TX + TW / 2, TY + 84, "vacía", 16, a.GREY, a.MONO, 400, "middle"), a.show(0, 6), still=0))
# vida de la anotación
BX, BY, BW = TX + 140, TY + 122, TW - 172
a.add(a.text(TX + 22, TY + 134, "vida", 15, a.GREY, a.MONO))
a.add(a.box(BX, BY, BW, 14, "#E6EDF4", rx=7))
life = [(0, 0), (6, 0), (6.5, 1), (26, 0.45), (26.5, 1), (50, 0), (62, 0), (62.5, 1), (70, 0.75), (70.5, 1), (78, 0.75), (78.5, 1),
        (86, 0.75), (86.5, 1), (94, 0.75), (94.5, 1), (99.5, 0.85), (100, 0)]
k = a.keyframes(life, "transform", "scaleX({})")
a.add(a.group(a.box(BX, BY, BW, 14, a.OK, rx=7), k, still=None, origin=f"{BX}px {BY}px"))

# 1: el sitio abre
packet(a, "sitio → CHR", [(0, SX + 90, LANE), (2, SX + 90, LANE), (6, NX, LANE), (10, HX - 90, LANE), (100, HX - 90, LANE)], 2, 10.5, a.BLUE)
# 2: el CHR contesta
packet(a, "respuesta", [(0, HX - 90, LANE), (22, HX - 90, LANE), (26, NX, LANE), (30, SX + 90, LANE), (100, SX + 90, LANE)], 22, 30.5, a.OK)
# 3: el hub intenta y el NAT descarta
packet(a, "hub → sitio", [(0, HX - 90, LANE), (52, HX - 90, LANE), (55.5, NX + 80, LANE), (100, NX + 80, LANE)], 52, 59.5, a.BAD)
a.add(a.group(a.text(NX, LANE - 30, "✕ sin anotación: se descarta", 16, a.BAD, a.MONO, 600, "middle"), a.show(55, 61), still=0))
# 4: keepalive
for t in (62, 70, 78, 86, 94):
    packet(a, "keepalive", [(0, SX + 70, LANE), (t, SX + 70, LANE), (t + 3.5, HX - 70, LANE), (100, HX - 70, LANE)], t, t + 3.8, a.CYAN, size=15, h=30)
a.add(a.group(a.text(SX, LANE + 40, "cada 25 s", 16, a.CYAN, a.MONO, 600, "middle"), a.show(61, 88), still=0))
# 5: el hub llega
packet(a, "WinBox a 10.10.10.2", [(0, HX - 120, LANE), (80, HX - 120, LANE), (83, NX, LANE), (88, SX + 120, LANE), (100, SX + 120, LANE)], 80, 89, a.OK)
a.add(a.group(a.text(SX, LANE + 40, "llega", 16, a.OK, a.MONO, 600, "middle"), a.show(88, 99), still=0))

# cuadro fijo
_off = a.keyframes([(0, 0), (100, 0)])
a.add(a.group(a.pill(780, LANE - 17, "WinBox a 10.10.10.2", a.WHITE, a.OK, 15, 34, "middle")
              + a.pill(380, LANE - 15, "keepalive", a.WHITE, a.CYAN, 15, 30, "middle")
              + a.text(SX, LANE + 40, "cada 25 s", 16, a.CYAN, a.MONO, 600, "middle"), _off, still=1))

# notas
NY = 584
NOTES = [
    (0, 40, a.TXT, "El CHR no inicia nada: responde a una conexión que el sitio abrió.", "Por eso el CGNAT del cliente deja de importar."),
    (40, 60, a.BAD, "Las anotaciones del NAT vencen si no pasa tráfico por un rato.", "Sin keepalive, el hub espera a que el sitio vuelva a hablar."),
    (60, 100, a.OK, "El sitio lleva endpoint y keepalive porque es el que llama.", "El hub no lleva endpoint: aprende de dónde viene cada peer."),
]
for s_, e, col, l1, l2 in NOTES:
    a.add(a.group(a.box(48, NY - 34, 1104, 100, a.WHITE, a.LINE, rx=16)
                  + a.text(72, NY, l1, 17, col, a.SANS, 600) + a.text(72, NY + 32, l2, 17, a.TXT, a.SANS, 400),
                  a.show(s_, e), still=1 if s_ == 60 else 0))

out(a, 20, 1, "CGNAT y keepalive hacia el CHR",
    "Animación en cinco tiempos con el router del sitio (wg-central 10.10.10.2), el NAT o CGNAT del proveedor y el CHR (wg-hub 198.51.100.20, puerto 13231). "
    "1: el sitio manda un paquete al CHR y el NAT anota la conexión: IP interna, puerto e IP externa. "
    "2: el CHR contesta por el mismo camino y el NAT lo deja pasar; el CHR no inicia nada. "
    "3: sin tráfico, la anotación vence; el hub intenta llegar al sitio y el NAT descarta el paquete. "
    "4: con persistent-keepalive=25s el sitio manda un paquete chico cada 25 segundos y la anotación se renueva. "
    "5: con la anotación viva, el hub llega al sitio: WinBox a 10.10.10.2 entra por el camino abierto. El sitio lleva endpoint y keepalive; el hub no lleva endpoint.",
    [8, 27, 56, 72, 86])
