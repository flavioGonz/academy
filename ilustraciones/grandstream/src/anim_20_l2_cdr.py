#!/usr/bin/env python3
"""IVR que solo anuncia · Laboratorio, paso 7: 20-l2.svg.
Medir en el CDR: en las dos llamadas de prueba se cuelga apenas suena la 1002, así el Call Time es casi
entero el tiempo en el IVR. Campos del CDR según el manual del UCM630xA (Status, Call From, Call To,
Action Type, Start Time, Call Time). Horas y segundos de ejemplo, con la misma cuenta que 20-r1.
"""
from _anim_gs_red import R

g = R(T=26, fix=92, kicker="GRANDSTREAM · IVR QUE SOLO ANUNCIA · PASO 7", title="El CDR antes y después del arreglo")
g.steps([
    "Prueba con el error: colgás apenas suena la 1002 y la llamada queda en el CDR.",
    "Call Time 00:00:56: casi todo es IVR, tres vueltas de bienvenida y aviso.",
    "Con la receta, la misma prueba: Call Time 00:00:15.",
    "Bienvenida, 2 s de silencio y el timbre: 41 s menos de espera.",
], size=17)

B, OK, BAD, GREY, INK = g.BLUE, g.OK, g.BAD, g.GREY, g.INK
# tabla tipo CDR
TX, TY = 48, 176
cols = [("Status", 150), ("Call From", 150), ("Call To", 130), ("Action Type", 170), ("Start Time", 220), ("Call Time", 170)]
W = sum(w for _, w in cols)
g.add(g.box(TX, TY, W, 148, g.WHITE, g.LINE, rx=12))
g.add(g.box(TX, TY, W, 44, g.SLATE, rx=12))
x = TX
for name, w in cols:
    g.add(g.text(x + 16, TY + 28, name.upper(), 13, GREY, g.MONO, 600))
    x += w
g.add(f'<line x1="{TX + 12}" y1="{TY + 96}" x2="{TX + W - 12}" y2="{TY + 96}" stroke="{g.LINE}" stroke-width="1"/>')
rows = [(0, ["Answered", "1001", "7000", "IVR", "2026-10-29 10:02:10", "00:00:56"], BAD, 4),
        (1, ["Answered", "1001", "7000", "IVR", "2026-10-29 10:09:40", "00:00:15"], OK, 51)]
for r, vals, col, t0 in rows:
    y = TY + 78 + r * 52
    x = TX
    for i, ((name, w), v) in enumerate(zip(cols, vals)):
        c = col if i == 5 else INK
        g.appear(g.text(x + 16, y, v, 16 if i == 5 else 15, c, g.MONO, 600 if i == 5 else 400), t0 + i * 0.8, 100)
        x += w
    g.appear(g.text(TX + W + 14, y, "antes" if r == 0 else "después", 15, col, g.SANS, 600), t0, 100)
g.appear(g.box(TX + W - 170 + 6, TY + 52, 150, 38, "none", BAD, rx=8, sw=2.5), 26, 50, still=0)
g.appear(g.box(TX + W - 170 + 6, TY + 104, 150, 38, "none", OK, rx=8, sw=2.5), 52, 75, still=0)

# barras: de qué está hecho el Call Time
X0, PX = 170, 980 / 60
def seg(y, s0, s1, t0, t1, color, label=None, lc=None):
    xx, w = X0 + s0 * PX, (s1 - s0) * PX - 3
    g.bar(xx, y, w, 36, t0, t1, color)
    if label:
        g.appear(g.text(xx + w / 2, y + 24, label, 13, lc or g.WHITE, g.SANS, 600, "middle"), t1, 100)

YA, YD = 372, 448
g.add(g.text(48, YA + 24, "Antes", 18, INK, g.HEAD, 600))
g.add(g.text(48, YD + 24, "Después", 18, INK, g.HEAD, 600))
g.add(g.box(X0, YA, 980, 36, g.SLATE, rx=6))
g.add(g.box(X0, YD, 980, 36, g.SLATE, rx=6))
t = 27
for k in range(3):
    s0 = 18 * k
    seg(YA, s0, s0 + 12, t, t + 3.5, B, "bienvenida"); t += 3.5
    seg(YA, s0 + 12, s0 + 15, t, t + 1.2, GREY, "3 s"); t += 1.2
    seg(YA, s0 + 15, s0 + 18, t, t + 1.2, BAD, "aviso"); t += 1.2
seg(YA, 54, 56, t, t + 1, OK, None)
g.appear(g.pill(X0 + 56 * PX + 8, YA + 4, "56 s", BAD, g.BADBG, 13, 28), 46, 100)
seg(YD, 0, 12, 77, 83, B, "bienvenida")
seg(YD, 12, 14, 83, 85, "#B9C6D3", "2 s", INK)
seg(YD, 14, 15, 85, 86, OK, None)
g.appear(g.pill(X0 + 15 * PX + 8, YD + 4, "15 s", OK, g.OKBG, 13, 28), 86, 100)
g.appear(g.pillc(X0 + 35 * PX, YD + 4, "41 s menos de espera", OK, g.WHITE, 14, 28), 88, 100)
for s in (0, 15, 30, 45, 60):
    xx = X0 + s * PX
    g.add(f'<line x1="{xx:.1f}" y1="{YD + 46}" x2="{xx:.1f}" y2="{YD + 54}" stroke="{GREY}" stroke-width="1.5"/>')
    g.add(g.text(xx, YD + 74, f"{s} s", 13, GREY, g.MONO, 400, "middle"))
g.add(g.text(48, YD + 74, "(ejemplo)", 13, GREY, g.SANS, 400))

# abajo
g.add(g.box(48, 552, 1104, 76, g.WHITE, g.LINE, rx=14))
g.add(g.text(72, 584, "Colgando apenas suena la 1002, el Call Time es casi entero el tiempo que pasó en el IVR.", 17, INK, g.SANS, 600))
g.add(g.text(72, 610, "CDR > CDR, filtrando por la 1001 · Action Type IVR · datos de ejemplo", 15, GREY, g.MONO, 400))

g.done(20, "l2", "El CDR antes y después del arreglo",
       "Animación en cuatro tiempos con dos registros del CDR de la UCM, con las columnas Status, Call From, Call To, Action Type, Start Time y Call Time, y debajo dos barras de 0 a 60 segundos de ejemplo. "
       "1: la llamada de prueba con el error, de la 1001 al IVR 7000, en la que se cuelga apenas suena la 1002, queda en el CDR como Answered, Action Type IVR. "
       "2: su Call Time es 00:00:56; la barra muestra de qué está hecho: tres vueltas de bienvenida de 12 segundos, 3 segundos de Digit Timeout y el aviso de inválido, y recién ahí suena el grupo. "
       "3: con la receta aplicada, la misma prueba queda con Call Time 00:00:15. "
       "4: la barra nueva es la bienvenida, 2 segundos de silencio por el Response Timeout y el timbre: 41 segundos menos de espera. "
       "Abajo: colgando apenas suena la 1002, el Call Time es casi entero el tiempo que pasó en el IVR; se busca en CDR > CDR filtrando por la 1001.",
       [8, 30, 44, 60, 80, 92])
