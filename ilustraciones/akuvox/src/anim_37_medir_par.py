#!/usr/bin/env python3
"""Lección 37 · Teoría · Antes de reutilizar el par: continuidad y aislación.
Sale de teoria_md (Cómo funciona): continuidad (cada conductor entero de punta a punta), aislación (sin fuga
entre los dos conductores ni hacia tierra o la cañería); un par en mal estado da fallas intermitentes que
ningún equipo corrige. Porteros de 2 hilos sin PoE: R20A-2 y R20K-2 a 48 V DC 1,25 A."""
from _anim_akuvox_29_42 import new, out, box, travel, when, check

a = new(24, "DOS HILOS · EL PAR EXISTENTE", "Antes de reutilizar el par: continuidad y aislación")
a.steps([
    "Continuidad: cada conductor tiene que llegar entero de punta a punta.",
    "Aislación entre los dos conductores: no tiene que haber fuga.",
    "Aislación hacia tierra o la cañería: tampoco tiene que haber fuga.",
    "Un par dañado (corte o fuga) da fallas intermitentes que ningún equipo corrige.",
], still=2)

YA, YB = 300, 350
X0, X1 = 250, 950
# cañería
a.add(f'<rect x="{X0 + 30}" y="266" width="{X1 - X0 - 60}" height="118" rx="20" fill="#E9EEF3" stroke="{a.GREY}" stroke-width="2"/>')
a.add(a.text(X0 + 50, 404 + 0, "cañería", 15, a.GREY, a.MONO, 600))
a.add(f'<line x1="{X0 + 30}" y1="440" x2="{X1 - 30}" y2="440" stroke="#8A6D3B" stroke-width="3" stroke-dasharray="10 6"/>')
a.add(a.text(X1 - 30, 466, "tierra", 15, "#8A6D3B", a.MONO, 600, "end"))
# extremos
a.add(box(48, 283, 200, 84, "Portero", "calle", "bell"))
a.add(box(952, 283, 200, 84, "Apto 301", "monitor", "laptop"))
# conductores
for y, n in ((YA, "conductor 1"), (YB, "conductor 2")):
    a.add(f'<line x1="{X0}" y1="{y}" x2="{X1}" y2="{y}" stroke="{a.BLUE}" stroke-width="5"/>')
a.add(a.text(600, YA - 12, "conductor 1", 15, a.BLUE, a.MONO, 600, "middle"))
a.add(a.text(600, YB + 26, "conductor 2", 15, a.BLUE, a.MONO, 600, "middle"))

# t1: continuidad (pulso por cada conductor)
travel(a, (X0 + 10, YA), (X1 - 10, YA), 3, 11, None, bg=a.CYAN, dot=10, hold=.5)
travel(a, (X0 + 10, YB), (X1 - 10, YB), 12, 20, None, bg=a.CYAN, dot=10, hold=.5)
when(a, check(a, 1020, 230, True, 15) + a.text(1042, 236, "entero", 15, a.OK, a.MONO, 600), 11.5, 75, still=1)
when(a, check(a, 1020, 400, True, 15) + a.text(1042, 406, "entero", 15, a.OK, a.MONO, 600), 20.5, 75, still=1)


def tester(x, y1, y2, label, ok, t0, t1, still):
    c = a.OK if ok else a.BAD
    g = (f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" stroke="{c}" stroke-width="2.5" stroke-dasharray="4 4"/>'
         f'<circle cx="{x}" cy="{y1}" r="6" fill="{c}"/><circle cx="{x}" cy="{y2}" r="6" fill="{c}"/>')
    return when(a, g + a.pill(x + 14, (y1 + y2) / 2 - 14, label, c, a.OKBG if ok else a.BADBG, 15, 28), t0, t1, still=still)


# t2: entre conductores
tester(430, YA, YB, "entre 1 y 2: sin fuga", True, 27, 75, 1)
# t3: hacia tierra / cañería
tester(770, YB, 440, "a tierra: sin fuga", True, 52, 75, 1)

# t4: par dañado
when(a, f'<rect x="360" y="{YA - 8}" width="40" height="16" fill="#E9EEF3"/>'
     f'<path d="M360 {YA - 10} l-6 20 M400 {YA - 10} l6 20" stroke="{a.BAD}" stroke-width="3"/>'
     + a.pill(338, 222, "corte", a.BAD, a.BADBG, 15, 28), 77, 100)
travel(a, (X0 + 10, YA), (348, YA), 78, 84, None, bg=a.BAD, dot=10, hold=12)
when(a, f'<path d="M820 {YB} l6 10 l-8 6 l8 10 l-6 8" fill="none" stroke="{a.BAD}" stroke-width="3"/>'
     + a.pill(760, 394, "fuga a la cañería", a.BAD, a.BADBG, 15, 28), 80, 100)
when(a, a.pill(940, 200, "falla intermitente", a.BAD, a.BADBG, 15, 28), 86, 100)

a.add(a.box(48, 500, 1104, 128, a.WHITE, a.LINE, rx=16))
a.add(a.text(72, 534, "Con el par sano, el par lleva la comunicación entre los equipos, como el UTP y el switch en IP.", 18, a.INK, a.SANS, 600))
a.add(a.text(72, 564, "La energía va aparte: los porteros de 2 hilos no tienen PoE.", 17, a.TXT, a.SANS, 600))
a.add(a.text(72, 592, "R20A-2 y R20K-2 piden 48 V DC 1,25 A; el C313-2 se alimenta del NS-2 o de 48 V.", 17, a.TXT, a.SANS, 600))

out(a, 37, 1, "Antes de reutilizar el par: continuidad y aislación",
    "Animación de un par existente que va del portero de calle al apartamento 301 dentro de una cañería, con la tierra debajo. "
    "Tiempo 1: continuidad; una señal recorre el conductor 1 y después el conductor 2 de punta a punta y los dos llegan enteros. "
    "Tiempo 2: aislación entre los dos conductores; no hay fuga. "
    "Tiempo 3: aislación hacia tierra o la cañería; no hay fuga. "
    "Tiempo 4: un par dañado; el conductor 1 tiene un corte donde la señal se detiene y el conductor 2 tiene una fuga a la cañería: eso da fallas intermitentes que ningún equipo corrige. "
    "Abajo: con el par sano, el par lleva la comunicación; la energía va aparte, a 48 V DC para R20A-2 y R20K-2.",
    [10, 40, 62, 92])
