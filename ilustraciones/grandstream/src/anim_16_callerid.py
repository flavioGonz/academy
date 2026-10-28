#!/usr/bin/env python3
"""Lección 16 · teoría: el número viaja en FSK entre el primer y el segundo timbre (Bellcore) o en DTMF antes del timbre."""
from _anim_grandstream import G

g = G(T=26, fix=92, kicker="GRANDSTREAM · IDENTIFICADOR", title="El número viaja entre timbres, o antes")
g.steps([
    "Bellcore, el de fábrica de la UCM: suena el primer timbre.",
    "Entre el primer y el segundo timbre, el número viaja en FSK y la UCM lo lee.",
    "Si la UCM atiende antes del segundo timbre, el número no llega: Undetected.",
    "ETSI-DTMF antes del timbre: el número llega como tonos de teclado y después suena.",
])
NUM = "2900 1007"
X0, X1 = 230, 1120

def fila(y, titulo, sub):
    g.add(g.box(48, y, 1104, 150, g.WHITE, g.LINE, rx=16))
    g.add(g.text(72, y + 34, titulo, 18, g.INK, g.SANS, 600))
    g.add(g.text(72, y + 58, sub, 15, g.GREY, g.SANS, 400))
    g.add(f'<path d="M{X0} {y + 104}H{X1}" stroke="{g.LINE}" stroke-width="2"/>')

def ring(x, w, y, t0, t1, lab):
    d = "".join(f"M{x + j * 5:.1f} {y + 86}V{y + 122}" for j in range(int(w / 5)))
    g.appear(f'<path d="{d}" stroke="{g.GREY}" stroke-width="2"/>' + g.text(x + w / 2, y + 78, lab, 15, g.GREY, g.SANS, 600, "middle"), t0, t1)

# fila Bellcore
Y1 = 176
fila(Y1, "Bellcore/Telcordia", "FSK entre el 1.er y el 2.º timbre")
ring(330, 150, Y1, 2, 100, "timbre 1")
g.appear(g.box(560, Y1 + 88, 240, 32, g.BLUE, rx=6) + g.text(680, Y1 + 110, "FSK · " + NUM, 15, g.WHITE, g.MONO, 700, "middle"), 27, 50)
g.appear(g.box(560, Y1 + 88, 240, 32, g.BLUE, rx=6) + g.text(680, Y1 + 110, "FSK · " + NUM, 15, g.WHITE, g.MONO, 700, "middle"), 75, 100)
ring(880, 150, Y1, 40, 50, "timbre 2")
ring(880, 150, Y1, 75, 100, "timbre 2")
# atender antes (tiempo 3)
g.appear(g.box(500, Y1 + 84, 6, 40, g.BAD, rx=2) + g.text(503, Y1 + 142, "atiende", 15, g.BAD, g.SANS, 600, "middle"), 52, 75)
# pantalla de la UCM con el número
g.add(g.box(880, Y1 + 14, 248, 52, g.INK, rx=10))
g.appear(g.text(1004, Y1 + 47, "sin número todavía", 15, "#9FC3E3", g.SANS, 500, "middle"), 0, 30)
g.appear(g.text(1004, Y1 + 48, NUM, 20, "#BFF0FF", g.MONO, 700, "middle"), 30, 52)
g.appear(g.text(1004, Y1 + 48, "Undetected", 18, "#FFB4A6", g.MONO, 700, "middle"), 52, 75)
g.appear(g.text(1004, Y1 + 48, NUM, 20, "#BFF0FF", g.MONO, 700, "middle"), 75, 100)

# fila DTMF antes del timbre
Y2 = 352
fila(Y2, "ETSI-DTMF Prior to Ringing", "tonos de teclado y después el timbre")
g.add(g.box(880, Y2 + 14, 248, 52, g.INK, rx=10))
g.appear(g.text(1004, Y2 + 47, "esperando", 15, "#9FC3E3", g.SANS, 500, "middle"), 0, 84)
digits = NUM.replace(" ", "")
for i, d in enumerate(digits):
    x = 330 + i * 34
    g.appear(g.box(x, Y2 + 90, 28, 28, g.CYAN, rx=5) + g.text(x + 14, Y2 + 110, d, 15, g.WHITE, g.MONO, 700, "middle"), 76 + i * 0.9, 100)
ring(680, 150, Y2, 86, 100, "timbre 1")
g.appear(g.text(1004, Y2 + 48, NUM, 20, "#BFF0FF", g.MONO, 700, "middle"), 84, 100)

g.add(g.note(48, 526, 1104, None, ["Antel no publica qué esquema usa su identificador: se prueba Auto-Detect y después uno por uno."], "amb"))
g.add(g.note(48, 590, 1104, None, ["El número de la animación es un ejemplo de documentación."], "info"))

g.finish(16, 1, "El número viaja entre timbres, o antes",
         "Animación en cuatro tiempos con dos filas, cada una con una línea de tiempo y la pantalla de la UCM a la derecha. "
         "1: con Bellcore, el esquema de fábrica de la UCM, suena el primer timbre y la pantalla dice sin número todavía. "
         "2: entre el primer y el segundo timbre el número viaja en FSK y la UCM lo muestra, 2900 1007, antes del segundo timbre. "
         "3: si la UCM atiende antes del segundo timbre, el FSK no llega y la pantalla muestra Undetected. "
         "4: en la fila de abajo, con ETSI-DTMF antes del timbre, el número llega como tonos de teclado, la UCM lo muestra y después suena el primer timbre. "
         "Notas: Antel no publica qué esquema usa, por eso se prueba Auto-Detect y después cada esquema; el número es un ejemplo de documentación.",
         [12, 37, 62, 92])
