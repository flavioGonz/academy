#!/usr/bin/env python3
"""Lección 10 · Teoría · Cómo arma Reportes de Afluencia cada intervalo.
Sale de teoria_md (Cómo funciona): toma los eventos de aforo del período elegido, en hora de Uruguay, y los agrupa en
intervalos; en cada uno calcula el máximo, el promedio, la cantidad de lecturas y el aforo exacto, que es la última
lectura del intervalo; debajo agrega los cortes de conexión de cámara con inicio, fin y duración, incluidos los abiertos."""
from _anim_omni import new, out, when

a = new(26, "REPORTES", "De lecturas sueltas a una fila del reporte")
a.steps([
    "Toma las lecturas del canal Aforo del período, en hora de Uruguay.",
    "Las agrupa en intervalos: acá, de una hora.",
    "Por intervalo: máximo, promedio, lecturas y aforo exacto (la última).",
    "Debajo, los cortes de cámara: inicio, fin y duración, también los abiertos.",
], still=2)

READ = {9: [(2, 3), (8, 4), (15, 5), (21, 4), (30, 6), (37, 5), (44, 7), (52, 6)],
        10: [(3, 8), (10, 9), (18, 7), (26, 8), (33, 6), (41, 5), (49, 4), (56, 5)],
        11: [(4, 4), (11, 3), (18, 4), (42, 2), (47, 3)]}
CX0, CX1, CY0, UY = 130, 1120, 356, 16
PXM = (CX1 - CX0) / 180


def X(h, m):
    return CX0 + ((h - 9) * 60 + m) * PXM


def Y(v):
    return CY0 - v * UY


a.add(a.box(48, 180, 1104, 210, a.WHITE, a.LINE, rx=14))
a.add(a.text(68, 206, "Fila Caja 1 · canal Aforo", 15, a.GREY, a.MONO, 600))
a.add(f'<line x1="{CX0}" y1="{CY0}" x2="{CX1}" y2="{CY0}" stroke="{a.LINE}" stroke-width="2"/>')
for h in (9, 10, 11, 12):
    a.add(a.text(X(h, 0), CY0 + 24, f"{h:02d}:00", 15, a.GREY, a.MONO, 600, "middle"))
# cortes (gris rayado)
for (h0, m0), (h1, m1) in (((11, 20), (11, 40)), ((11, 50), (12, 0))):
    a.add(a.box(X(h0, m0), 222, X(h1, m1) - X(h0, m0), CY0 - 222, a.BADBG, rx=4))
a.add(a.text((X(11, 20) + X(11, 40)) / 2, 240, "corte", 15, a.BAD, a.MONO, 600, "middle"))
a.add(a.text((X(11, 50) + X(12, 0)) / 2, 240, "corte", 15, a.BAD, a.MONO, 600, "middle"))
# lecturas
k = 0
for h, rs in READ.items():
    for m, v in rs:
        when(a, f'<circle cx="{X(h, m):.0f}" cy="{Y(v):.0f}" r="7" fill="{a.BLUE}"/>', 1 + k * 0.6, 100, still=1, fade=0.5)
        k += 1
# intervalos
for h in (10, 11):
    when(a, f'<line x1="{X(h, 0):.0f}" y1="214" x2="{X(h, 0):.0f}" y2="{CY0 + 6}" stroke="{a.INK}" stroke-width="2.5" stroke-dasharray="6 5"/>', 26, 100, still=1)
for i, h in enumerate((9, 10, 11)):
    when(a, f'<rect x="{X(h, 0) + 3:.0f}" y="214" width="{X(h + 1, 0) - X(h, 0) - 6:.0f}" height="{CY0 - 210}" rx="8" fill="{a.BLUE}" fill-opacity=".06"/>', 28 + i * 3, 100, still=1)
# última lectura de cada intervalo (exacto)
for h, rs in READ.items():
    m, v = rs[-1]
    when(a, f'<circle cx="{X(h, m):.0f}" cy="{Y(v):.0f}" r="12" fill="none" stroke="{a.AMB}" stroke-width="3"/>', 56, 100, still=1)

# ---- tabla del reporte
TX, TY = 48, 410
COLS = [("intervalo", 20), ("máximo", 260), ("promedio", 440), ("lecturas", 640), ("aforo exacto", 840)]
a.add(a.box(TX, TY, 1104, 150, a.WHITE, a.LINE, rx=14))
for name, x in COLS:
    a.add(a.text(TX + x, TY + 28, name, 15, a.GREY, a.MONO, 600))


def fmt(x):
    return f"{x:.1f}".replace(".", ",")


for i, (h, rs) in enumerate(READ.items()):
    vals = [v for _, v in rs]
    y = TY + 58 + i * 32
    when(a, a.text(TX + 20, y, f"{h:02d}:00 a {h + 1:02d}:00", 16, a.INK, a.MONO, 600), 28 + i * 3, 100, still=1)
    when(a, a.text(TX + 260, y, str(max(vals)), 16, a.INK, a.MONO, 600) + a.text(TX + 440, y, fmt(sum(vals) / len(vals)), 16, a.INK, a.MONO, 600)
         + a.text(TX + 640, y, str(len(vals)), 16, a.INK, a.MONO, 600) + a.text(TX + 840, y, str(vals[-1]), 16, a.AMB, a.MONO, 600), 52 + i * 2, 100, still=1)

# ---- cortes
when(a, a.box(48, 574, 1104, 46, a.BADBG, rx=10)
     + a.text(68, 603, "Cortes de cámara:  11:20 a 11:40 · 20 min   |   desde 11:50 · sigue abierto", 16, a.BAD, a.MONO, 600), 76, 100, still=0)
a.add(a.text(48, 646, "El aforo exacto es la última lectura del intervalo, no el promedio: por eso puede ser más bajo que el máximo.", 16, a.TXT, a.SANS, 600))

out(a, 10, 1, "De lecturas a una fila del reporte",
    "Animación en cuatro tiempos. Arriba, las lecturas del canal Aforo de la Fila Caja 1 entre las 09:00 y las 12:00, con dos cortes de cámara marcados entre las 11:20 y las 11:40 y desde las 11:50. "
    "Abajo, la tabla del reporte con intervalo, máximo, promedio, lecturas y aforo exacto. "
    "Tiempo 1: aparecen las lecturas como puntos, en hora de Uruguay. "
    "Tiempo 2: líneas punteadas las agrupan en intervalos de una hora: 09:00 a 10:00, 10:00 a 11:00 y 11:00 a 12:00. "
    "Tiempo 3: se marca la última lectura de cada intervalo y se completa la tabla: de 09:00 a 10:00, máximo 7, promedio 5,0, 8 lecturas, exacto 6; "
    "de 10:00 a 11:00, máximo 9, promedio 6,5, 8 lecturas, exacto 5; de 11:00 a 12:00, máximo 4, promedio 3,2, 5 lecturas, exacto 3. "
    "Tiempo 4: debajo aparecen los cortes de cámara: de 11:20 a 11:40, 20 minutos, y desde las 11:50, que sigue abierto. "
    "Al pie: el aforo exacto es la última lectura del intervalo, no el promedio.",
    [12, 36, 62, 92])
