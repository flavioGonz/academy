#!/usr/bin/env python3
"""Lección 7 · teoría: el botón de reset según cuánto tiempo lo mantenés (RouterBOOT de respaldo, reset, CAP, Netinstall)."""
from _anim_mikrotik_1_13 import *

a = Anim(T=24, kicker="MIKROTIK · LECCIÓN 7 · CÓMO FUNCIONA", title="El botón de reset: depende de cuándo lo soltás")
a.steps([
    "Botón apretado al dar energía: arranca con el RouterBOOT de respaldo.",
    "Unos 5 s, el LED titila: si soltás, se resetea la configuración.",
    "5 s más, LED fijo: si soltás, entra en modo CAP.",
    "5 s más, el LED se apaga: si soltás, busca un servidor Netinstall.",
], still=1)

# equipo
a.add(a.box(48, 186, 300, 196, a.INK))
a.add(a.text(68, 220, "RouterBOARD", 19, a.WHITE, a.SANS, 600))
a.add(a.text(68, 244, "RouterBOOT de respaldo:", 13, SKY, a.MONO))
a.add(a.text(68, 264, "nunca se actualiza", 13, SKY, a.MONO))
LEDX, LEDY = 92, 318
a.add(f'<circle cx="{LEDX}" cy="{LEDY}" r="14" fill="#2A4A6A"/>')
blink = a.keyframes([(0, 0), (25, 0)] + [(25 + k * 1.5, (k + 1) % 2) for k in range(1, 17)] + [(50, 1), (75, 1), (75.5, 0), (100, 0)])
a.add(a.group(f'<circle cx="{LEDX}" cy="{LEDY}" r="14" fill="{MINT}"/>', blink, still=1))
a.add(a.text(LEDX, LEDY + 38, "LED", 13, SKY, a.MONO, 400, "middle"))
a.add(f'<circle cx="190" cy="{LEDY}" r="13" fill="#0B3A66" stroke="{SKY}" stroke-width="2"/>')
a.add(a.text(190, LEDY + 38, "reset", 13, SKY, a.MONO, 400, "middle"))
a.add(a.group(f'<circle cx="190" cy="{LEDY}" r="8" fill="{GOLD}"/>', a.show(1, 97), still=1))
a.add(a.group(a.pill(230, LEDY - 14, "apretado", a.INK, GOLD, 13, 28), a.show(1, 97), still=1))

# línea de tiempo
X0, PX = 420, 38.0     # px por segundo
TY = 250


def xs(sec):
    return X0 + sec * PX


a.add(a.text(X0, 206, "tiempo con el botón apretado", 14, a.GREY, a.MONO))
a.add(line(X0, TY, xs(18.2), TY, a.LINE, 6))
for sec, lab in [(0, "energía"), (5, "5 s"), (10, "10 s"), (15, "15 s")]:
    a.add(line(xs(sec), TY - 12, xs(sec), TY + 12, a.GREY, 2))
    a.add(a.text(xs(sec), TY + 34, lab, 14, a.TXT, a.MONO, 600, "middle"))
cur = a.move([(0, xs(0), TY), (2, xs(0), TY), (75, xs(15), TY), (95, xs(17.5), TY), (100, xs(17.5), TY)])
a.add(a.group(f'<circle cx="0" cy="0" r="11" fill="{a.AMB}" stroke="{a.WHITE}" stroke-width="3"/>', cur, a.show(0, 100), still=0))
a.add(still_only(a, f'<circle cx="{xs(7.5)}" cy="{TY}" r="11" fill="{a.AMB}" stroke="{a.WHITE}" stroke-width="3"/>'))

# resultados por tramo
CARDS = [
    (0, "Al arrancar", ["usa el RouterBOOT", "de respaldo"], a.BLUE, "#E3EEF9", 0, 25),
    (5, "LED titila", ["soltás: reset de", "la configuración"], a.OK, a.OKBG, 25, 50),
    (10, "LED fijo", ["soltás: modo CAP"], a.AMB, a.AMBBG, 50, 75),
    (15, "LED apagado", ["soltás: busca un", "servidor Netinstall"], a.BAD, a.BADBG, 75, 100),
]
CY, CH = 314, 120
for sec, t, ls, fg, bg, t0, t1 in CARDS:
    x = xs(sec) + 4
    w = 5 * PX - 8 if sec < 15 else 1152 - x
    a.add(a.box(x, CY, w, CH, a.WHITE, a.LINE, rx=12))
    a.add(a.text(x + 14, CY + 30, t, 16, a.INK, a.SANS, 600))
    for k, l in enumerate(ls):
        a.add(a.text(x + 14, CY + 60 + k * 22, l, 14, a.TXT, a.SANS))
    hi = a.box(x, CY, w, CH, bg, fg, rx=12, sw=2.5) + a.text(x + 14, CY + 30, t, 16, fg, a.SANS, 600)
    for k, l in enumerate(ls):
        hi += a.text(x + 14, CY + 60 + k * 22, l, 14, a.INK, a.SANS, 600)
    a.add(a.group(hi, a.show(t0, t1, 0.8), still=1 if t0 == 25 else 0))

# Netinstall
a.add(a.box(48, 470, 1104, 120, a.WHITE, a.LINE))
a.add(f'<rect x="48" y="470" width="5" height="120" rx="2" fill="{a.BLUE}"/>')
a.add(a.text(70, 502, "Netinstall", 17, a.INK, a.SANS, 600))
a.add(a.text(70, 530, "Reinstala RouterOS por red desde una PC conectada por cable.", 15, a.TXT, a.SANS))
a.add(a.text(70, 554, "Es la salida cuando el sistema no arranca o se perdió la contraseña.", 15, a.TXT, a.SANS))
a.add(device(a, 760, 486, 170, 84, "PC", "Netinstall", ssize=13))
a.add(line(930, 528, 1010, 528, a.BLUE, 3))
a.add(a.text(970, 516, "cable", 13, a.BLUE, a.MONO, 400, "middle"))
a.add(a.box(1010, 492, 126, 72, a.INK, rx=12))
a.add(a.text(1026, 522, "Router", 15, a.WHITE, a.SANS, 600))
a.add(a.text(1026, 544, "sin sistema", 13, SKY, a.MONO))
a.add(during(a, a.box(756, 482, 384, 92, "none", a.BAD, rx=14, sw=2.5), 77, 98.5))

a.add(a.text(48, 632, "Los tiempos son aproximados: mirá el LED y soltá en el momento justo.", 16, a.TXT, a.SANS, 600))

p, pre = out(7, 1)
a.write(p, title="Botón de reset de un RouterBOARD",
        desc="Animación en cuatro tiempos sobre una línea de tiempo con el botón de reset apretado desde que se da energía. 1: al arrancar con el botón apretado, "
             "el equipo usa el RouterBOOT de respaldo, que nunca se actualiza. 2: a los 5 segundos aproximadamente el LED titila: si soltás, se resetea la configuración. "
             "3: 5 segundos más, con el LED fijo: si soltás, entra en modo CAP. 4: 5 segundos más, cuando el LED se apaga: si soltás, busca un servidor Netinstall, "
             "que reinstala RouterOS por red desde una PC conectada por cable.",
        preview=[12, 40, 62, 88], prefix=pre)
