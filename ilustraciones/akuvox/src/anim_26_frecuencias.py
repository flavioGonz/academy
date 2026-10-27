#!/usr/bin/env python3
"""Lección 26 · teoría: tarjetas de 125 kHz y de 13,56 MHz, y qué frecuencia lee cada R20."""
from _anim_akuvox_15_28 import *

a = new(20, "AKUVOX · LECCIÓN 26", "125 kHz o 13,56 MHz: qué tarjeta lee cada R20")
a.steps([
    "125 kHz (tipo EM o HID Prox): la generación vieja, simple y fácil de copiar.",
    "13,56 MHz (ISO 14443, como MIFARE): permite cifrado y más datos.",
    "El R20A lee las dos frecuencias: con cualquiera de las dos tarjetas, abre.",
    "El R20K-L lee solo 13,56 MHz: la tarjeta de 125 kHz no la lee.",
], still=3)


def card(x, y, w, h, kind):
    s = a.box(x, y, w, h, a.WHITE, a.INK, rx=12, sw=2)
    if kind == "125":
        for i in range(3):
            s += f'<rect x="{x + 16 + i * 8}" y="{y + 16 + i * 8}" width="{w - 32 - i * 16}" height="{h - 32 - i * 16}" rx="8" fill="none" stroke="{a.AMB}" stroke-width="2"/>'
    else:
        s += f'<rect x="{x + 18}" y="{y + h / 2 - 16}" width="36" height="30" rx="5" fill="#E9C46A" stroke="{a.AMB}" stroke-width="1.5"/>'
        s += f'<path d="M{x + 18} {y + h / 2 - 1} H{x + 54} M{x + 36} {y + h / 2 - 16} V{y + h / 2 + 14}" stroke="{a.AMB}" stroke-width="1.2"/>'
    return s


# tarjetas
a.add(card(60, 196, 210, 132, "125"))
a.add(a.text(290, 230, "125 kHz", 22, a.INK, a.HEAD, 600))
a.add(a.text(290, 258, "tipo EM o HID Prox", 16, a.TXT, a.MONO))
a.add(a.text(290, 286, "simple, fácil de copiar", 16, a.BAD, a.SANS, 600))
a.add(card(60, 360, 210, 132, "1356"))
a.add(a.text(290, 394, "13,56 MHz", 22, a.INK, a.HEAD, 600))
a.add(a.text(290, 422, "ISO 14443, como MIFARE", 16, a.TXT, a.MONO))
a.add(a.text(290, 450, "cifrado y más datos", 16, a.OK, a.SANS, 600))
a.add(at(a, a.box(52, 188, 226, 148, "none", a.CYAN, rx=16, sw=3), 1, 25, still=0))
a.add(at(a, a.box(52, 352, 226, 148, "none", a.CYAN, rx=16, sw=3), 26, 50, still=0))
# copia (paso 1)
ghost = card(0, 0, 150, 94, "125")
a.add(a.group(ghost, a.move([(0, 500, 196), (5, 500, 196), (11, 520, 196), (100, 520, 196)]), a.show(5, 25, 1.5), still=0))
a.add(at(a, a.text(595, 318, "una copia", 16, a.BAD, a.SANS, 600, "middle"), 14, 25, still=0))
# cifrado (paso 2)
a.add(at(a, a.pill(170, 470, "cifrado", a.OK, a.OKBG, 15, anchor="middle"), 28, 100, still=1))

# lectores
RA, RK = 760, 990
a.add(I.Intercom(RA - 75, 196, "R20A", "lee las dos", keypad=False).svg())
a.add(I.Intercom(RK - 75, 196, "R20K-L", "solo 13,56 MHz", keypad=True).svg())


def token(lab):
    return a.box(-48, -28, 96, 56, a.WHITE, a.INK, rx=8, sw=2) + a.text(0, 7, lab, 16, a.INK, a.MONO, 600, "middle")


def tap(lab, x0, y0, xr, t0, ok, t_end):
    a.add(a.group(token(lab), a.move([(0, x0, y0), (t0, x0, y0), (t0 + 1.5, x0, 344), (t0 + 3.5, xr - 120, 344), (t0 + 5, xr, 300), (t0 + 8, xr, 300), (100, xr, 300)]),
                  a.show(t0, t0 + 9, 0.8), still=0))
    waves = "".join(f'<path d="M{xr - 30 - i * 12} {230 - i * 10} Q{xr} {205 - i * 14} {xr + 30 + i * 12} {230 - i * 10}" fill="none" stroke="{a.OK if ok else a.BAD}" stroke-width="3" stroke-linecap="round"/>' for i in range(2))
    a.add(at(a, waves, t0 + 5, t0 + 9, still=0))


tap("125", 165, 262, RA, 51, True, 75)
tap("13,56", 165, 426, RA, 62, True, 75)
tap("125", 165, 262, RK, 76, False, 100)
tap("13,56", 165, 426, RK, 87, True, 100)

# resultados
for x, rows in ((RA, [("125 kHz", True, 56), ("13,56 MHz", True, 67)]), (RK, [("125 kHz", False, 81), ("13,56 MHz", True, 92)])):
    for j, (lab, ok, t) in enumerate(rows):
        y = 552 + j * 40
        a.add(a.text(x - 105, y + 6, lab, 16, a.TXT, a.MONO, 500))
        a.add(at(a, mark(x + 20, y, ok) + a.text(x + 44, y + 6, "abre" if ok else "no lee", 15, a.OK if ok else a.BAD, a.MONO, 600), t, 100, still=1))

a.write(*out(26)[:1], title="Tarjetas de 125 kHz y 13,56 MHz en los R20",
        desc=("Animación en cuatro tiempos. 1: la tarjeta de 125 kHz, tipo EM o HID Prox, es la generación vieja de proximidad, simple y fácil de copiar: una copia abre igual. "
              "2: la de 13,56 MHz, ISO 14443 como MIFARE, permite cifrado y más datos. "
              "3: el R20A lee las dos frecuencias y abre con cualquiera de las dos tarjetas. "
              "4: el R20K-L lee solo 13,56 MHz: con la tarjeta de 125 kHz no lee, con la de 13,56 MHz abre."),
        preview=[12, 40, 66, 96], prefix=out(26)[1])
