#!/usr/bin/env python3
"""Lección 13 · teoría: qué pasa en el par de cobre (reposo, timbre, atender, colgar, tono para marcar)."""
from _anim_grandstream import G

g = G(T=26, fix=96, kicker="GRANDSTREAM · LÍNEA ANALÓGICA", title="Qué pasa en el par de cobre")
g.steps([
    "En reposo, la central de Antel mantiene tensión continua en el par.",
    "Entra una llamada: la central suma el timbre, una alterna de unos 70 V.",
    "La UCM atiende por el FXO: cierra el lazo, circula corriente y la tensión cae.",
    "Cuelga: el lazo se abre y la tensión vuelve a la de reposo.",
    "Para salir, el FXO descuelga y la central manda el tono de 425 Hz.",
])
K = [0, 20, 40, 60, 80, 100]   # límites de cada tiempo

# equipos y par
g.add(g.node(48, 190, 250, 90, "Central de Antel", "hace de FXS", dark=True, tsize=21))
g.add(g.node(902, 190, 250, 90, "UCM · FXO1", "hace de teléfono", dark=True, tsize=21))
for dy in (-6, 6):
    g.add(f'<path d="M298 {235 + dy}H902" stroke="#3B4D61" stroke-width="3"/>')
# estado del par (en el medio)
CX = 600
est = [("reposo · tensión continua", g.BLUE, g.WHITE), ("timbre · alterna de unos 70 V", g.AMB, g.AMBBG),
       ("atendido · lazo cerrado, corriente", g.OK, g.OKBG), ("colgado · vuelve la tensión", g.BLUE, g.WHITE),
       ("descolgado · tono de invitación de 425 Hz", g.OK, g.OKBG)]
for i, (s, fg, bg) in enumerate(est):
    g.appear(g.pillc(CX, 266, s, fg, bg, size=15, h=30), K[i], K[i + 1])
# corriente que circula con el lazo cerrado
for t0 in (41, 47, 53):
    g.token([(310, 229), (890, 229)], t0, t0 + 6, g.chip("corriente", bg=g.OK, size=14, h=24))
for t0 in (81, 88, 94):
    g.token([(310, 229), (890, 229)], t0, t0 + 6, g.chip("corriente", bg=g.OK, size=14, h=24))
# tono hacia la UCM al descolgar para salir

# osciloscopio: tensión en el tiempo
OX, OY, OW, OH = 48, 320, 1104, 230
g.add(g.box(OX, OY, OW, OH, g.WHITE, g.LINE, rx=14))
g.add(g.text(OX + 20, OY + 32, "Tensión en el par, en el tiempo", 17, g.INK, g.SANS, 600))
HI, LO = OY + 92, OY + 182          # nivel de reposo y de descolgado
g.add(g.text(OX + 20, HI + 5, "reposo", 15, g.GREY, g.SANS, 500))
g.add(g.text(OX + 20, LO + 5, "descolgado", 15, g.GREY, g.SANS, 500))
X0, W = OX + 130, (OW - 160) / 5
g.add(f'<path d="M{X0} {OY + 205}H{X0 + 5 * W}" stroke="{g.LINE}" stroke-width="2"/>')
import math
segs = []
segs.append(f"M{X0:.1f} {HI}H{X0 + W:.1f}")
pts = []
for j in range(0, 121):
    x = X0 + W + W * j / 120
    on = (j % 60) < 40 and j < 120
    pts.append(f"{x:.1f} {HI - (34 * math.sin(j * 0.9) if on else 0):.1f}")
segs.append("M" + " L".join(pts))
segs.append(f"M{X0 + 2 * W:.1f} {HI}V{LO}H{X0 + 3 * W:.1f}")
segs.append(f"M{X0 + 3 * W:.1f} {LO}V{HI}H{X0 + 4 * W:.1f}")
pts = [f"{X0 + 4 * W:.1f} {HI}", f"{X0 + 4 * W:.1f} {LO}"]
for j in range(0, 121):
    x = X0 + 4 * W + W * j / 120
    pts.append(f"{x:.1f} {LO - 6 * math.sin(j * 1.6):.1f}")
segs.append("M" + " L".join(pts))
cols = [g.BLUE, g.AMB, g.OK, g.BLUE, g.OK]
for i, d in enumerate(segs):
    g.appear(f'<path d="{d}" fill="none" stroke="{cols[i]}" stroke-width="3" stroke-linejoin="round"/>', K[i] + 1, 100)
labs = ["continua", "timbre", "corriente", "reposo", "425 Hz"]
for i, s in enumerate(labs):
    g.appear(g.text(X0 + i * W + W / 2, OY + 222, s, 15, cols[i], g.MONO, 600, "middle"), K[i] + 1, 100)
# cursor
g.add(g.group(f'<path d="M0 {OY + 50}V{OY + 200}" stroke="{g.INK}" stroke-width="2" stroke-dasharray="4 4"/>',
              g.move([(0, X0, 0), (100, X0 + 5 * W, 0)]), still=0))

g.add(g.note(48, 572, 1104, None, ["Antel no publica sus valores: innovaphone habla de 24 a 70 V en reposo y Sandman de 4 a 18 V descolgado. Medí tu línea."], "amb"))

g.finish(13, 1, "Qué pasa en el par de cobre",
         "Animación en cinco tiempos con la central de Antel, que hace de FXS, unida por el par de cobre al FXO1 de la UCM, que hace de teléfono. Abajo, un gráfico de la tensión en el par que se va dibujando. "
         "1: en reposo, la central mantiene tensión continua en el par. "
         "2: entra una llamada y la central suma el timbre, una alterna de unos 70 V que se ve como ráfagas. "
         "3: la UCM atiende por el FXO, cierra el lazo, circula corriente y la tensión cae al nivel de descolgado. "
         "4: al colgar, el lazo se abre y la tensión vuelve a la de reposo. "
         "5: para hacer una llamada, el FXO descuelga, la tensión vuelve a caer y la central manda el tono de invitación a marcar de 425 Hz. "
         "Nota: Antel no publica sus valores; innovaphone habla de 24 a 70 V en reposo y Sandman de 4 a 18 V descolgado, por eso conviene medir la línea.",
         [10, 30, 50, 70, 92])
