#!/usr/bin/env python3
"""Lección 8 · Teoría · La prueba por áreas de la ley de Little, y cómo la usa OmniAccess.
Sale de teoria_md (Cómo funciona): L = λW; si cada persona es una barra horizontal desde que llega hasta que se va, el
área total es a la vez la suma de los tiempos de espera y la suma, momento a momento, de cuántas personas había.
OmniAccess usa W = L / λ: L es el aforo actual y λ el ritmo de salida de los últimos 15 minutos; el kiosko muestra ~N min,
"<1" si es menos de un minuto o un guion si no hubo salidas."""
from _anim_omni import new, out, when

a = new(26, "ESPERA ESTIMADA", "La ley de Little, dibujada")
a.steps([
    "Cada persona es una barra: desde que llega a la fila hasta que se va.",
    "Sumando el largo de las barras: el total de minutos de espera.",
    "Contando cuántas había en cada momento: la misma área, por columnas.",
    "Por eso L = λW. OmniAccess despeja la espera: W = L / λ.",
], still=2)

BARS = [(0, 6), (2, 10), (3, 9), (5, 14), (8, 15), (11, 18), (12, 20), (16, 25)]
TMAX = 26
X0, X1 = 120, 840
PX = (X1 - X0) / TMAX
BY0, BH = 192, 25


def X(t):
    return X0 + t * PX


# eje de tiempo
a.add(a.text(48, BY0 + 40, "personas", 15, a.GREY, a.MONO, 600))
for t in range(0, TMAX + 1, 5):
    a.add(f'<line x1="{X(t):.0f}" y1="{BY0 - 4}" x2="{X(t):.0f}" y2="560" stroke="{a.LINE}" stroke-width="1"/>')
    a.add(a.text(X(t), 584, f"{t} min", 15, a.GREY, a.MONO, 600, "middle"))

# barras (tiempo 1: aparecen una a una)
total = 0
for i, (s, e) in enumerate(BARS):
    y = BY0 + i * BH
    total += e - s
    when(a, a.box(X(s), y, (e - s) * PX, BH - 6, a.CYAN, rx=5), 1 + i * 2.5, 100, still=1, fade=0.8)
    # largo (tiempo 2)
    when(a, a.text(X(e) + 8, y + 15, f"{e - s}", 15, a.INK, a.MONO, 600), 26 + i * 2.4, 100, still=1, fade=0.5)
assert total == 60

# L(t) por columnas, abajo
LY1 = 560
UH = 22


def L(t):
    return sum(1 for s, e in BARS if s <= t < e)


cols = ""
for t in range(TMAX):
    n = L(t + 0.5)
    if n:
        cols += a.box(X(t) + 1, LY1 - n * UH, PX - 2, n * UH, a.BLUE, rx=2, extra='fill-opacity=".85"')
a.add(a.text(48, LY1 - 66, "cuántas", 15, a.GREY, a.MONO, 600))
a.add(a.text(48, LY1 - 46, "había", 15, a.GREY, a.MONO, 600))
# revelado por barrido (tiempo 3)
reveal = a.keyframes([(0, 0), (51, 0), (70, 1), (100, 1)], "transform", "scaleX({})")
a.n += 1
c = f"c{a.n}"
a.css.append(f".{c}{{transform-box:view-box;transform-origin:{X0}px 0;transform:scaleX(1);animation:{reveal} {a.T}s linear infinite}}")
a.add(f'<defs><clipPath id="sweep"><rect class="{c}" x="{X0}" y="400" width="{X1 - X0}" height="170"/></clipPath></defs>')
when(a, f'<g clip-path="url(#sweep)">{cols}</g>', 51, 100, still=1)
sweep = a.move([(0, X0, 0), (51, X0, 0), (70, X(TMAX), 0), (100, X(TMAX), 0)])
a.add(a.group(f'<line x1="0" y1="{BY0 - 8}" x2="0" y2="{LY1}" stroke="{a.BAD}" stroke-width="3"/>', sweep, a.show(51, 72, 0.5), still=0))

# ---- panel derecho
RX, RW = 878, 274
a.add(a.box(RX, 182, RW, 400, a.WHITE, a.LINE, rx=14))
when(a, a.text(RX + 20, 214, "suma de esperas", 15, a.GREY, a.MONO, 600)
     + a.text(RX + 20, 252, "60 persona·min", 22, a.CYAN, a.MONO, 600), 40, 100, still=1)
when(a, a.text(RX + 20, 296, "suma por columnas", 15, a.GREY, a.MONO, 600)
     + a.text(RX + 20, 334, "60 persona·min", 22, a.BLUE, a.MONO, 600)
     + a.text(RX + 20, 364, "la misma área", 16, a.OK, a.SANS, 600), 70, 100, still=1)
when(a, f'<line x1="{RX + 20}" y1="384" x2="{RX + RW - 20}" y2="384" stroke="{a.LINE}" stroke-width="2"/>'
     + a.text(RX + 20, 420, "L = λ · W", 24, a.INK, a.HEAD, 600)
     + a.text(RX + 20, 456, "W = L / λ", 24, a.BAD, a.HEAD, 600)
     + a.text(RX + 20, 490, "L: aforo actual", 15, a.TXT, a.SANS)
     + a.text(RX + 20, 514, "λ: salidas de 15 min / 15", 15, a.TXT, a.SANS)
     + a.text(RX + 20, 548, "kiosko: ~N min, <1 o un guion", 15, a.TXT, a.SANS), 76, 100, still=1)

a.add(a.text(48, 636, "Vale con la fila estable: a la larga sale tanta gente como entra. Si llega mucha de golpe, el número se queda corto.", 16, a.TXT, a.SANS, 600))

out(a, 8, 1, "La ley de Little, dibujada",
    "Animación en cuatro tiempos sobre un eje de 0 a 26 minutos. Arriba, ocho personas como barras horizontales desde que llegan a la fila hasta que se van; abajo, columnas con cuántas personas había en cada minuto. "
    "Tiempo 1: aparecen las barras, una por persona. "
    "Tiempo 2: al lado de cada barra se lee su largo en minutos (6, 8, 6, 9, 7, 7, 8 y 9); sumados dan 60 persona por minuto. "
    "Tiempo 3: una línea roja barre el tiempo y deja debajo las columnas de cuántas había en cada momento; sumadas dan también 60 persona por minuto: la misma área. "
    "Tiempo 4: por eso L es igual a lambda por W, y OmniAccess despeja la espera, W igual a L sobre lambda, con L el aforo actual y lambda las salidas de los últimos 15 minutos divididas 15; el kiosko muestra ~N min, menos de 1 o un guion. "
    "Al pie: vale con la fila estable; si llega mucha gente de golpe, el número se queda corto.",
    [10, 40, 62, 92])
