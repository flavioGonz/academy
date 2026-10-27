#!/usr/bin/env python3
"""Lección 7 · teoría: de los dos tonos del Touch-Tone al evento RFC 4733 que lee el IVR."""
import math
from _anim_grandstream import G

g = G(T=24, fix=88, kicker="GRANDSTREAM · DTMF", title="La tecla que entiende el IVR: de dos tonos a un evento")
g.steps([
    "Touch-Tone (1963): cada tecla suena como la mezcla de dos tonos.",
    "Una máquina reconoce el par de tonos y sabe qué tecla fue: así nace el IVR.",
    "En la UCM, la tecla viaja como evento RFC 4733 dentro del RTP, junto a la voz.",
    "El IVR lee el evento: qué tecla fue y cuánto duró.",
])

# teclado
keys = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "*", "0", "#"]
KX, KY, KW, KH, KG = 60, 200, 64, 52, 12
g.add(g.box(KX - 16, KY - 16, 3 * KW + 2 * KG + 32, 4 * KH + 3 * KG + 32, g.WHITE, g.LINE, rx=18))
for i, k in enumerate(keys):
    x, y = KX + (i % 3) * (KW + KG), KY + (i // 3) * (KH + KG)
    g.add(g.box(x, y, KW, KH, g.SLATE, None, rx=10) + g.text(x + KW / 2, y + 34, k, 22, g.INK, g.MONO, 600, "middle"))
g.appear(g.box(KX - 6, KY - 6, 3 * KW + 2 * KG + 12, KH + 12, "none", g.AMB, rx=12, sw=2.5), 3, 50)
g.appear(g.box(KX - 6, KY - 6, KW + 12, 4 * KH + 3 * KG + 12, "none", g.CYAN, rx=12, sw=2.5), 5, 50)
g.appear(g.box(KX, KY, KW, KH, g.INK, None, rx=10) + g.text(KX + KW / 2, KY + 34, "1", 22, g.WHITE, g.MONO, 600, "middle"), 2, 100)
g.add(g.text(KX - 16, KY + 4 * KH + 3 * KG + 46, "teclado de quien llama", 14, g.GREY, g.MONO))


def wave(x0, x1, yc, amp, fs, col, w=2.5):
    pts = []
    for i in range(0, 241):
        x = x0 + (x1 - x0) * i / 240
        t = i / 240
        y = yc - amp * sum(math.sin(2 * math.pi * f * t) for f in fs) / len(fs)
        pts.append(f"{x:.1f} {y:.1f}")
    return f'<path d="M{" L".join(pts)}" fill="none" stroke="{col}" stroke-width="{w}"/>'


WX0, WX1 = 360, 800
g.appear(g.text(WX0, 208, "tono de la fila", 15, g.AMB, g.MONO, 600) + wave(WX0, WX1, 240, 18, [7], g.AMB), 4, 50)
g.appear(g.text(WX0, 290, "tono de la columna", 15, g.CYAN, g.MONO, 600) + wave(WX0, WX1, 322, 18, [12], g.CYAN), 7, 50)
g.appear(g.text(WX0, 376, "por la línea viaja la suma", 15, g.INK, g.MONO, 600) + wave(WX0, WX1, 420, 30, [7, 12], g.INK, 3), 12, 50)

# IVR
g.add(g.node(900, 196, 252, 96, "IVR 7000", "espera una tecla", dark=True, tsize=22))
g.arrow([(WX1 + 10, 420), (1026, 420), (1026, 300)], 27, 32, g.BLUE, hold=50)
g.appear(g.pillc(1026, 330, "reconoce el par: tecla 1", g.BLUE, g.WHITE, 13, 26), 32, 50)

# RTP en la UCM
LY = 560
g.add(g.text(48, LY + 44, "RTP entre el teléfono y la UCM", 15, g.GREY, g.MONO, 400, extra='letter-spacing="1"'))
g.add(f'<line x1="48" y1="{LY}" x2="1060" y2="{LY}" stroke="{g.LINE}" stroke-width="2" stroke-dasharray="4 6"/>')
for k in range(9):
    t0 = 51 + k * 4.4
    if k == 3:
        g.token([(110, LY), (1000, LY)], t0, t0 + 12, g.chip("RFC 4733 · tecla 1", bg=g.AMB, size=14, h=30), hold=t0 + 12.4)
    else:
        g.token([(70, LY), (1000, LY)], t0, t0 + 12, g.chip("voz", bg=g.BLUE, size=13, h=26), hold=t0 + 12.4)
g.fijo_only(f'<g transform="translate(260 {LY})">' + g.chip("voz", bg=g.BLUE, size=13, h=26) + "</g>"
            + f'<g transform="translate(470 {LY})">' + g.chip("RFC 4733 · tecla 1", bg=g.AMB, size=14, h=30) + "</g>"
            + f'<g transform="translate(690 {LY})">' + g.chip("voz", bg=g.BLUE, size=13, h=26) + "</g>")
g.arrow([(1040, LY), (1100, LY), (1100, 300)], 76, 80, g.AMB, hold=100)
g.appear(g.box(900, 300, 252, 0, "none") + g.pillc(1026, 330, "evento: tecla 1", g.AMB, g.AMBBG, 14, 28), 80, 100)
g.appear(g.pillc(1026, 372, "y cuánto duró", g.AMB, g.AMBBG, 14, 28), 82, 100)

g.appear(g.note(WX0, 200, 470, "Evento RFC 4733", ["Un paquete RTP especial dice qué tecla", "fue y cuánto duró, y viaja por el mismo", "camino que la voz."], "amb"), 52, 100)
g.appear(g.note(WX0, 352, 470, None, ["RFC 2833 (2000) lo definió; la RFC 4733", "(2006) la reemplazó. Por eso la UCM", "muestra RFC4733."], "info"), 56, 100)

g.finish(7, 2, "La tecla que entiende el IVR: de dos tonos a un evento",
         "Animación en cuatro tiempos. 1: en un teclado Touch-Tone, de 1963, se aprieta la tecla 1; se resaltan su fila y su columna, y cada una aporta un tono: por la línea viaja la suma de los dos. "
         "2: una máquina reconoce el par de tonos y sabe que fue la tecla 1; así nace el IVR. "
         "3: en la UCM la tecla ya no viaja como sonido: por el RTP entre el teléfono y la central pasan paquetes de voz y, entre ellos, un evento RFC 4733 que dice tecla 1. "
         "4: el IVR 7000 lee el evento: qué tecla fue y cuánto duró. "
         "Notas: el evento RFC 4733 es un paquete RTP especial que viaja por el mismo camino que la voz; la RFC 2833, de 2000, lo definió y la RFC 4733, de 2006, la reemplazó, por eso la UCM muestra RFC4733.",
         [14, 38, 62, 88])
