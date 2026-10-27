"""Teoría de Modo del detector: con el óptico en baja, el DOTC necesita humo más CO o calor."""
from _anim_bi import *

caps = ["Vapor de una ducha: sube la señal de humo; CO y temperatura, no.",
        "Con el óptico en baja, el DOTC espera: no hay alarma.",
        "Fuego latente: suben juntos el humo y el CO.",
        "Humo más CO: alarma."]
a = new(24, "Modo del detector", "El vapor no trae CO: el DOTC en baja no se apura", caps, still=3)

a.add(a.box(60, 200, 300, 300, a.WHITE, a.LINE, rx=150, sw=3))
a.add(a.text(210, 340, "FAP-425-DOTC-R", 17, a.INK, a.MONO, 600, "middle"))
a.add(a.text(210, 368, "óptico en baja", 16, a.GREY, a.SANS, 400, "middle"))
vis(a, a.box(60, 200, 300, 300, "none", a.BAD, rx=150, sw=6), 3)
# barras
B = [(470, "Humo", a.BLUE), (650, "CO", a.OK), (830, "Temperatura", a.AMB)]
base, top = 520, 220
for x, t, col in B:
    a.add(a.box(x, top, 110, base - top, a.SLATE, a.LINE, rx=10, sw=2))
    a.add(a.text(x + 55, base + 30, t, 17, a.INK, a.SANS, 600, "middle"))
lvl = {0: (220, 20, 20), 1: (220, 20, 20), 2: (210, 190, 40), 3: (240, 220, 50)}
for i, (h1, h2, h3) in lvl.items():
    inner = "".join(a.box(x + 8, base - h - 8, 94, h, col, rx=6) for (x, _, col), h in zip(B, (h1, h2, h3)))
    vis(a, inner, i)
a.add(f'<path d="M455 330 H955" stroke="{a.INK}" stroke-width="2" stroke-dasharray="6 6"/>')
a.add(a.text(960, 335, "umbral", 15, a.INK, a.MONO))
vis(a, a.pill(210, 540, "vapor", a.GREY, a.SLATE, anchor="middle"), 0, 1)
vis(a, a.pill(210, 540, "espera, sin alarma", a.AMB, a.AMBBG, anchor="middle"), 1)
vis(a, a.pill(210, 540, "fuego latente", a.BAD, a.BADBG, anchor="middle"), 2)
vis(a, a.pill(210, 540, "ALARMA", a.WHITE, a.BAD, size=18, anchor="middle"), 3)
a.add(a.box(980, 380, 172, 120, a.WHITE, a.LINE, rx=12))
a.add(a.text(996, 410, "Regla de la", 15, a.TXT)); a.add(a.text(996, 432, "guía Bosch:", 15, a.TXT))
a.add(a.text(996, 460, "humo + CO", 16, a.INK, a.MONO, 600)); a.add(a.text(996, 484, "o humo + calor", 16, a.INK, a.MONO, 600))
a.add(a.text(48, 630, "Esa espera es la que rechaza el vapor; es también el costo frente a un fuego real.", 17, a.TXT))
write(a, "11-t1.svg", "El DOTC en baja espera", [12, 37, 62, 90])
