#!/usr/bin/env python3
"""IVR que solo anuncia · Teoría: 20-t1.svg. Cómo un ruido se vuelve un 5 en el FXO.
La tecla 5 es 770 Hz + 1336 Hz (UIT-T Q.23). En la línea analógica el FXO busca ese par en el audio y lo filtra
por duración, espacio entre dígitos, desvío de frecuencia y twist; la voz suele fallar algún filtro (talk-off
cuando no falla), y el eco o el ruido a veces pasan todos. Por SIP la tecla viaja como evento RFC 4733 y no
hay que adivinar nada.
"""
from _anim_grandstream import G

g = G(T=24, fix=62, kicker="GRANDSTREAM · IVR QUE SOLO ANUNCIA · TEORÍA", title="Cómo un ruido se vuelve un 5 en el FXO")
g.steps([
    "Tecla 5 de verdad: 770 Hz y 1336 Hz a la vez. El FXO la reconoce y avisa al IVR.",
    "Voz o música: casi siempre falla un filtro, por ejemplo dura poco. No hay dígito.",
    "Eco o ruido que pasa todos los filtros: un 5 que nadie marcó (talk-off, falsing).",
    "Por SIP la tecla llega como evento RFC 4733: no hay nada que adivinar.",
], size=17)

B, OK, BAD, AMB, GREY, INK, CY = g.BLUE, g.OK, g.BAD, g.AMB, g.GREY, g.INK, g.CYAN
# teclado DTMF
KX, KY, CW, CH = 128, 214, 72, 54
cols, rows = ["1209", "1336", "1477"], ["697", "770", "852", "941"]
keys = [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"], ["*", "0", "#"]]
g.add(g.text(48, 188, "Hz", 14, GREY, g.MONO, 600))
for j, c in enumerate(cols):
    g.add(g.text(KX + j * CW + CW / 2 - 3, 188, c, 14, GREY, g.MONO, 600, "middle"))
for i, r in enumerate(rows):
    g.add(g.text(48, KY + i * CH + 33, r, 14, GREY, g.MONO, 600))
    for j in range(3):
        g.add(g.box(KX + j * CW, KY + i * CH, CW - 6, CH - 6, g.WHITE, g.LINE, rx=10))
        g.add(g.text(KX + j * CW + CW / 2 - 3, KY + i * CH + 33, keys[i][j], 19, INK, g.HEAD, 600, "middle"))
g.add(g.text(48, KY + 4 * CH + 22, "A a D usan 1633 Hz", 14, GREY, g.SANS, 400))
# resaltes: fila 770 y columna 1336
def row_col(t0, t1, col_on=True, color=CY):
    g.appear(g.box(KX - 6, KY + CH - 4, 3 * CW + 4, CH + 2, "none", color, rx=12, sw=3), t0, t1)
    if col_on:
        g.appear(g.box(KX + CW - 4, KY - 4, CW + 2, 4 * CH + 2, "none", color, rx=12, sw=3), t0, t1)
        g.appear(g.box(KX + CW, KY + CH, CW - 6, CH - 6, color, None, rx=10)
                 + g.text(KX + CW + CW / 2 - 3, KY + CH + 33, "5", 19, g.WHITE, g.HEAD, 600, "middle"), t0, t1)
row_col(2, 25)
row_col(27, 50, col_on=False, color=GREY)
row_col(52, 75, color=AMB)

# lo que entra por la línea
IX, IY, IW = 400, 170, 420
g.add(g.text(IX, IY + 4, "lo que entra", 14, GREY, g.SANS, 400))
INS = [(0, 25, "tecla 5 · 770 + 1336 Hz", B), (25, 50, "voz o música", GREY), (50, 75, "eco o ruido parecido", AMB), (75, 100, "SIP · evento RFC 4733: 5", B)]
for t0, t1, s, c in INS:
    g.appear(g.pill(IX, IY + 14, s, c, g.WHITE, 15, 30), t0, t1)
# detector
DX, DY, DW, DH = 400, 236, 420, 256
g.add(g.box(DX, DY, DW, DH, g.INK, None, rx=16))
g.add(g.text(DX + 22, DY + 36, "Detector DTMF del FXO", 19, g.WHITE, g.HEAD, 600))
checks = ["un tono de cada grupo", "dura lo suficiente", "niveles parecidos (twist)"]
for k, s in enumerate(checks):
    g.add(g.text(DX + 66, DY + 92 + k * 52, s, 17, "#D9E9F8", g.SANS, 600))
# estado de cada filtro por tiempo: ok / bad / na
STATE = [(0, 25, ["ok", "ok", "ok"]), (25, 50, ["ok", "bad", "ok"]), (50, 75, ["ok", "ok", "ok"]), (75, 100, ["na", "na", "na"])]
for t0, t1, st in STATE:
    for k, s in enumerate(st):
        cy = DY + 86 + k * 52
        if s == "na":
            g.appear(g.text(DX + 38, cy + 6, "·", 22, GREY, g.MONO, 600, "middle"), t0, t1)
        else:
            g.appear(g.mark(DX + 38, cy, s == "ok", 13), t0, t1)
g.appear(g.pillc(DX + DW / 2, DY + DH - 42, "sin detector: el evento ya dice qué tecla", CY, g.INK, 14, 28), 75, 100)
# salida al IVR
OX, OY, OW = 900, 290, 252
g.add(g.parrow(f"M{DX + DW + 6} {OY + 50} H{OX - 8}", g.GREY, 2.5))
g.add(g.box(OX, OY, OW, 100, g.WHITE, g.LINE, rx=14))
g.add(g.text(OX + 20, OY + 30, "al IVR 7000", 15, GREY, g.SANS, 400))
OUT = [(0, 25, "5", B, g.WHITE), (25, 50, "nada", GREY, g.SLATE), (50, 75, "5 falso", AMB, g.AMBBG), (75, 100, "5", B, g.WHITE)]
for t0, t1, s, c, bg in OUT:
    g.appear(g.pill(OX + 20, OY + 48, s, c, bg, 18, 36), t0, t1)
g.token([(IX + 120, IY + 44), (IX + 120, DY)], 3, 7, g.chip("audio", bg=B, size=13, h=24))
g.token([(IX + 120, IY + 44), (IX + 120, DY)], 53, 57, g.chip("audio", bg=AMB, size=13, h=24))

# abajo
g.add(g.box(48, 520, 1104, 104, g.WHITE, g.LINE, rx=14))
BOT = [(0, 75, "Según la norma, el detector filtra por duración mínima, espacio entre dígitos,", "desvío de frecuencia y twist. Si el ruido pasa los filtros, el IVR recibe un dígito.", INK),
       (75, 100, "En la línea analógica no hay eventos: el FXO decide con el audio.", "Por SIP, el teléfono manda la tecla como evento RFC 4733 dentro del RTP.", OK)]
for t0, t1, a, b, c in BOT:
    g.appear(g.text(72, 560, a, 17, INK, g.SANS, 600) + g.text(72, 592, b, 17, c, g.SANS, 600), t0, t1)

g.finish(20, 1, "Cómo un ruido se vuelve un 5 en el FXO",
         "Animación en cuatro tiempos. A la izquierda, el teclado DTMF con las frecuencias de cada fila, 697, 770, 852 y 941 hercios, y de cada columna, 1209, 1336 y 1477; al medio, el detector DTMF del FXO con tres filtros: un tono de cada grupo, que dure lo suficiente y niveles parecidos, el twist; a la derecha, lo que le pasa al IVR 7000. "
         "1: entra la tecla 5 de verdad, 770 y 1336 hercios a la vez; pasa los tres filtros y el IVR recibe un 5. "
         "2: entra voz o música; tiene algo de 770 pero dura poco y falla un filtro: no hay dígito. "
         "3: entra eco o ruido parecido al par de la tecla 5 y pasa todos los filtros: el IVR recibe un 5 que nadie marcó; eso es falsing, y talk-off cuando es la voz. "
         "4: por SIP, la tecla llega como evento RFC 4733 dentro del RTP y no pasa por ningún detector: el evento ya dice qué tecla fue. En la línea analógica no hay eventos y el FXO decide con el audio.",
         [5, 15, 38, 62, 70, 88])
