#!/usr/bin/env python3
"""Lección 23 · Safe Mode. Teoría "Cómo funciona": cada cambio se aplica ya y queda marcado F; lo que se vigila es
la sesión; si muere de forma anormal, RouterOS deshace todo lo marcado, también lo de otras sesiones.
"""
from _anim_mikrotik_14_26 import Anim, out

a = Anim(T=26, kicker="MIKROTIK · SAFE MODE", title="Safe Mode vigila tu sesión, no un reloj")
a.steps([
    "Entrás en Safe Mode. Cada cambio se aplica ya y queda marcado con F.",
    "Mientras tanto, otra sesión cambia algo: también se deshace si caés.",
    "Un cambio te corta. No hay temporizador: el router espera a que la conexión muera.",
    "La conexión murió: RouterOS deshace todo lo marcado, de las dos sesiones.",
], still=3)

# sesiones
SX, SW = 48, 340


def session(y, name, sub):
    a.add(a.box(SX, y, SW, 104, a.WHITE, a.LINE, rx=16))
    a.add(a.text(SX + 22, y + 36, name, 19, a.INK, a.HEAD, 600))
    a.add(a.text(SX + 22, y + 60, sub, 15, a.GREY, a.MONO))


session(182, "Tu sesión", "WinBox · tomó el Safe Mode")
session(306, "Otra sesión", "terminal de otro técnico")
a.add(a.group(a.pill(SX + 22, 182 + 68, "Safe Mode activo", a.OK, a.OKBG, 15, 28), a.show(2, 62), still=0))
a.add(a.group(a.pill(SX + 22, 182 + 68, "sin respuesta…", a.AMB, a.AMBBG, 15, 28), a.show(62, 76), still=0))
a.add(a.group(a.pill(SX + 22, 182 + 68, "conexión muerta", a.BAD, a.BADBG, 15, 28), a.show(76, 100), still=1))
a.add(a.group(a.pill(SX + 22, 306 + 68, "un cambio suyo", a.INK, a.SLATE, 15, 28), a.show(28, 100), still=1))

# historial
HX, HY, HW = 424, 182, 728
a.add(a.box(HX, HY, HW, 296, a.INK, rx=18))
a.add(a.text(HX + 24, HY + 38, "/system/history", 18, a.WHITE, a.MONO, 600))
ROWS = [  # texto, quién, aparece
    ("bridge port agregado", "tu sesión", 8),
    ("regla de NAT agregada", "otra sesión", 30),
    ("ether2 deshabilitada", "tu sesión", 54),
]
for i, (t, who, on) in enumerate(ROWS):
    y = HY + 62 + i * 70
    inner = (a.box(HX + 16, y, HW - 32, 58, a.NAVY2, rx=10)
             + a.text(HX + 38, y + 36, "F", 18, "#FFD28A", a.MONO, 600)
             + a.text(HX + 72, y + 36, t, 17, a.WHITE, a.MONO, 600)
             + a.text(HX + HW - 36, y + 36, who, 15, "#9FC3E3", a.MONO, 400, "end"))
    a.add(a.group(inner, a.show(on, 100), still=1))
    a.add(a.group(f'<line x1="{HX + 70}" y1="{y + 30}" x2="{HX + 72 + len(t) * 10.4}" y2="{y + 30}" stroke="#FF8A73" stroke-width="3"/>'
                  + a.pill(HX + HW - 150, y + 15, "deshecho", "#FF8A73", "#3A1A1A", 15, 28, "end"),
                  a.show(80 + i * 3, 100), still=1))
a.add(a.group(a.text(HX + 24, HY + 280, "los cambios ya están aplicados: un cambio malo corta igual", 15, "#C9DDF0", a.SANS, 600), a.show(0, 76), still=0))

# línea de tiempo
TY = 560
a.add(a.text(48, TY - 34, "TIEMPO", 15, a.GREY, a.MONO, 600))
a.add(a.arrow(f"M48 {TY} H1150", a.GREY, 2.5))
MARKS = [(110, "entrás", a.OK), (380, "cambios con F", a.INK), (620, "corte", a.BAD), (1010, "deshace", a.BAD)]
for x, t, c in MARKS:
    a.add(f'<line x1="{x}" y1="{TY - 8}" x2="{x}" y2="{TY + 8}" stroke="{c}" stroke-width="3"/>')
    a.add(a.text(x, TY + 32, t, 15, c, a.MONO, 600, "middle"))
a.add(f'<rect x="632" y="{TY - 6}" width="366" height="12" rx="6" fill="{a.AMB}" opacity=".35"/>')
a.add(a.text(815, TY + 62, "esperando que muera la conexión: de segundos a unos 9 min", 15, a.AMB, a.SANS, 600, "middle"))
cur = a.move([(0, 60, TY), (2, 110, TY), (50, 500, TY), (58, 620, TY), (76, 1010, TY), (100, 1060, TY)])
a.add(a.group(a.group(f'<circle cx="0" cy="0" r="10" fill="{a.BLUE}" stroke="{a.WHITE}" stroke-width="3"/>', cur, still=None), a.show(0, 100), still=0))

# cuadro fijo: cursor en "deshace"
_off = a.keyframes([(0, 0), (100, 0)])
a.add(a.group(f'<circle cx="1010" cy="{TY}" r="10" fill="{a.BLUE}" stroke="{a.WHITE}" stroke-width="3"/>', _off, still=1))

out(a, 23, 1, "Safe Mode: lo que vigila es la sesión",
    "Animación en cuatro tiempos con dos sesiones, el historial /system/history y una línea de tiempo. "
    "1: entrás en Safe Mode desde WinBox; agregás un bridge port, el cambio se aplica en el acto y queda marcado con F. "
    "2: mientras tanto, desde otra sesión, otro técnico agrega una regla de NAT; también queda marcada. "
    "3: deshabilitás ether2 y tu sesión se corta; no hay temporizador propio: el router espera a que la conexión muera, de segundos a unos 9 minutos según el caso. "
    "4: la conexión murió de forma anormal y RouterOS deshace todo lo marcado con F, tus cambios y el de la otra sesión.",
    [10, 40, 66, 92])
