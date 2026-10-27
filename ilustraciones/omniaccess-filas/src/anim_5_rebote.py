#!/usr/bin/env python3
"""Lección 5 · Teoría · De los cambios por minuto al rebote sugerido.
Sale de teoria_md (Cómo funciona): la pestaña Señal del aforo toma las lecturas del canal Aforo de los últimos 10, 30 o
60 minutos, cuenta los cambios por minuto y sugiere un rebote: 1 segundo si son 4 o menos, y 1,5, 2, 2,5 o 3 segundos
cuando pasan de 4, 8, 15 o 30."""
import random
from _anim_omni import new, out, when

a = new(24, "CALIBRAR", "Cuántas veces cambia el aforo, y qué rebote sugiere")
a.steps([
    "La pestaña Señal toma las lecturas crudas del canal Aforo.",
    "Cuenta los cambios por minuto: cada salto de valor suma uno.",
    "Ubica la medida en la escala: 18 cambios por minuto, rebote de 2,5 s.",
    "Con la fila tranquila: 3 cambios por minuto, rebote de 1 s.",
], still=2)

CX0, CX1, CY0, CY1 = 120, 1100, 196, 372
a.add(a.box(48, 180, 1104, 210, a.WHITE, a.LINE, rx=14))
a.add(a.text(68, 206, "un minuto del canal Aforo", 15, a.GREY, a.MONO, 600))
for v in (2, 3, 4, 5):
    y = CY1 - (v - 1) * 36
    a.add(f'<line x1="{CX0}" y1="{y}" x2="{CX1}" y2="{y}" stroke="{a.LINE}" stroke-width="1"/>')
    a.add(a.text(CX0 - 14, y + 5, str(v), 15, a.GREY, a.MONO, 600, "end"))


def signal(vals):
    n = len(vals)
    pts, x = [], CX0
    step = (CX1 - CX0) / n
    for i, v in enumerate(vals):
        y = CY1 - (v - 1) * 36
        pts.append((x, y)); x += step; pts.append((x, y))
    d = "M" + " L".join(f"{px:.0f} {py:.0f}" for px, py in pts)
    changes = [(CX0 + step * i, vals[i - 1], vals[i]) for i in range(1, n) if vals[i] != vals[i - 1]]
    return d, changes


random.seed(7)
busy = [3]
while sum(1 for i in range(1, len(busy)) if busy[i] != busy[i - 1]) < 18:
    busy.append(random.choice([2, 3, 4]) if random.random() < 0.75 else busy[-1])
busy = busy[:60] if len(busy) > 60 else busy
calm = [3] * 12 + [4] * 16 + [3] * 14 + [4] * 6 + [4] * 12
d1, ch1 = signal(busy)
d2, ch2 = signal(calm)
assert len(ch1) == 18 and len(ch2) == 3, (len(ch1), len(ch2))
when(a, f'<path d="{d1}" fill="none" stroke="{a.AMB}" stroke-width="3"/>', 1, 74, still=1)
when(a, f'<path d="{d2}" fill="none" stroke="{a.BLUE}" stroke-width="3"/>', 76, 100, still=0)

# tiempo 2: marcas de cada cambio y contador
for i, (x, v0, v1) in enumerate(ch1):
    y = CY1 - (max(v0, v1) - 1) * 36 - 12
    when(a, f'<circle cx="{x:.0f}" cy="{y:.0f}" r="5" fill="{a.BAD}"/>', 26 + i * 1.1, 74, still=1, fade=0.4)
for i in range(18):
    t0 = 26 + i * 1.1
    t1 = 26 + (i + 1) * 1.1 if i < 17 else 74
    when(a, a.text(1132, 206, f"{i + 1} cambios", 16, a.BAD, a.MONO, 600, "end"), t0, t1, still=1 if i == 17 else 0, fade=0.2)
for i, (x, v0, v1) in enumerate(ch2):
    y = CY1 - (max(v0, v1) - 1) * 36 - 12
    when(a, f'<circle cx="{x:.0f}" cy="{y:.0f}" r="5" fill="{a.BAD}"/>', 80 + i * 2, 100, still=0, fade=0.4)
when(a, a.text(1132, 206, "3 cambios", 16, a.BAD, a.MONO, 600, "end"), 86, 100, still=0)

# ---- escala
SX0, SW, SY = 120, 196, 474
SEG = [("hasta 4", "1 s"), ("más de 4", "1,5 s"), ("más de 8", "2 s"), ("más de 15", "2,5 s"), ("más de 30", "3 s")]
a.add(a.text(48, 426, "cambios por minuto → rebote sugerido", 17, a.INK, a.SANS, 600))
for i, (lab, reb) in enumerate(SEG):
    x = SX0 + i * SW
    a.add(a.box(x + 2, SY, SW - 4, 40, a.SLATE, rx=8) + a.text(x + SW / 2, SY + 26, lab, 15, a.INK, a.MONO, 600, "middle"))
    a.add(a.text(x + SW / 2, SY + 72, reb, 18, a.BLUE, a.MONO, 600, "middle"))
a.add(a.text(SX0 - 14, SY + 72, "rebote", 15, a.GREY, a.MONO, 600, "end"))
# resaltes
seg4 = SX0 + 3 * SW
when(a, a.box(seg4 + 2, SY, SW - 4, 40, a.AMBBG, a.AMB, rx=8, sw=2.5) + a.text(seg4 + SW / 2, SY + 26, "más de 15", 15, a.AMB, a.MONO, 600, "middle")
     + a.pill(seg4 + SW / 2, SY + 92, "sugiere 2,5 s", a.WHITE, a.AMB, 16, 32, "middle"), 51, 74, still=1)
when(a, a.box(SX0 + 2, SY, SW - 4, 40, "#DCEBFA", a.BLUE, rx=8, sw=2.5) + a.text(SX0 + SW / 2, SY + 26, "hasta 4", 15, a.BLUE, a.MONO, 600, "middle")
     + a.pill(SX0 + SW / 2, SY + 92, "sugiere 1 s", a.WHITE, a.BLUE, 16, 32, "middle"), 88, 100, still=0)
# aguja
needle = f'<path d="M0 -14 L-9 -28 L9 -28 z" fill="{a.INK}"/>'
when(a, f'<g transform="translate({seg4 + (18 - 15) / 15 * SW:.0f} {SY})">{needle}</g>' + a.text(seg4 + (18 - 15) / 15 * SW + 14, SY - 22, "18", 15, a.INK, a.MONO, 600), 51, 74, still=1)
when(a, f'<g transform="translate({SX0 + 3 / 4 * SW:.0f} {SY})">{needle}</g>' + a.text(SX0 + 3 / 4 * SW + 14, SY - 22, "3", 15, a.INK, a.MONO, 600), 88, 100, still=0)

a.add(a.text(48, 640, "La ventana puede ser de 10, 30 o 60 minutos. Más de 8 cambios por minuto ya es parpadeo de más.", 16, a.TXT, a.SANS, 600))

out(a, 5, 1, "Cambios por minuto y rebote sugerido",
    "Animación en cuatro tiempos. Arriba, un minuto de lecturas crudas del canal Aforo, con valores entre 2 y 4; abajo, una escala de cambios por minuto con el rebote que sugiere: "
    "hasta 4, 1 s; más de 4, 1,5 s; más de 8, 2 s; más de 15, 2,5 s; más de 30, 3 s. "
    "Tiempo 1: la pestaña Señal toma las lecturas crudas del canal Aforo y aparece una señal que salta seguido. "
    "Tiempo 2: cada salto de valor se marca con un punto rojo y el contador llega a 18 cambios. "
    "Tiempo 3: 18 cambios por minuto caen en el tramo de más de 15 y la sugerencia es un rebote de 2,5 s. "
    "Tiempo 4: con la fila tranquila la señal cambia 3 veces en el minuto, cae en el tramo de hasta 4 y la sugerencia es 1 s. "
    "Al pie: la ventana puede ser de 10, 30 o 60 minutos; más de 8 cambios por minuto ya es parpadeo de más.",
    [12, 40, 62, 94])
