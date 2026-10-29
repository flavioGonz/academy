#!/usr/bin/env python3
"""Lección 8 · Resumen, "Cómo se ve en la red": la banda de 2.4 GHz vista en frecuencia. Canales cada 5 MHz y
transmisiones de unos 20 MHz: solo 1, 6 y 11 no se pisan. Dos EAP en 3 y 9 se pisan con los vecinos; a 40 MHz, también
entre ellos. En 1 y 6 a 20 MHz, no."""
from _anim_om_red import *

a = nueva(28, "MENOS POTENCIA", "2.4 GHz por dentro: por qué 1, 6 y 11")
F = a.steps([
    "Los canales están cada 5 MHz, pero cada transmisión ocupa unos 20: los vecinos se pisan.",
    "El consultorio: EAP 1 en canal 3 y EAP 2 en 9, a 20 MHz. Cada uno pisa a dos redes vecinas.",
    "Como estaban, a 40 MHz: ocupan el doble y se pisan también entre ellos.",
    "EAP 1 en 1 y EAP 2 en 6, a 20 MHz: entre ellos no se pisan y con los vecinos se turnan.",
], still=1)

X0, X1, F0, F1 = 110, 1090, 2400, 2484
BASE = 462


def fx(f):
    return X0 + (f - F0) * (X1 - X0) / (F1 - F0)


def ch(n):
    return 2407 + 5 * n


def hump(f0, f1, h, fill, stroke, op=0.55, dash=""):
    x0, x1 = fx(f0), fx(f1)
    s = 0.12 * (x1 - x0)
    da = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<path d="M{x0:.1f} {BASE} L{x0 + s:.1f} {BASE - h} L{x1 - s:.1f} {BASE - h} L{x1:.1f} {BASE} Z" '
            f'fill="{fill}" fill-opacity="{op}" stroke="{stroke}" stroke-width="2.5"{da}/>')


# eje
a.add(a.box(48, 180, 1104, 340, a.WHITE, a.LINE, rx=16))
a.add(line(X0, BASE, X1, BASE, a.INK, 2))
for n in range(1, 14):
    x = fx(ch(n))
    big = n in (1, 6, 11)
    a.add(line(x, BASE, x, BASE + 10, a.INK if big else a.GREY, 2))
    a.add(a.text(x, BASE + 32, str(n), 16 if big else 15, a.INK if big else a.GREY, a.MONO, 600 if big else 400, "middle"))
a.add(a.text(X1, BASE + 50, "canal · 2.4 GHz", 15, a.GREY, a.MONO, 400, "end"))
a.add(a.text(X0, 210, "espectro ocupado", 15, a.GREY, a.MONO))

# 1: las tres libres
for n in (1, 6, 11):
    at(a, hump(ch(n) - 10, ch(n) + 10, 150, a.OKBG, a.OK, 0.7), 3 + n * 0.6, 25)
at(a, hump(ch(3) - 10, ch(3) + 10, 120, a.AMBBG, a.AMB, 0.6, "6 5"), 12, 25)
at(a, a.text(fx(ch(3)), BASE - 128, "canal 3 pisa a 1 y a 6", 15, a.AMB, a.SANS, 600, "middle"), 13, 25)

# vecinos del edificio (fases 2 a 4)
for n in (1, 6, 11):
    at(a, hump(ch(n) - 10, ch(n) + 10, 80, a.SLATE, a.GREY, 0.9, "5 5"), 25, 100, still=1)
at(a, a.text(fx(ch(11)) + 60, BASE - 88, "redes vecinas", 15, a.GREY, a.SANS, 600, "middle"), 25, 100, still=1)
# 2: EAP en 3 y 9 a 20
at(a, hump(ch(3) - 10, ch(3) + 10, 150, "#CFE3F7", a.BLUE, 0.75), 27, 50, still=1)
at(a, hump(ch(9) - 10, ch(9) + 10, 150, "#CDEFF8", a.CYAN, 0.75), 29, 50, still=1)
at(a, a.text(fx(ch(3)), BASE - 160, "EAP 1 · canal 3", 15, a.BLUE, a.MONO, 600, "middle")
   + a.text(fx(ch(9)), BASE - 160, "EAP 2 · canal 9", 15, a.CYAN, a.MONO, 600, "middle"), 29, 50, still=1)
# 3: a 40 MHz
at(a, hump(ch(3) - 10, ch(3) + 30, 150, "#CFE3F7", a.BLUE, 0.6), 52, 75)
at(a, hump(ch(9) - 30, ch(9) + 10, 150, "#CDEFF8", a.CYAN, 0.6), 54, 75)
at(a, f'<rect x="{fx(ch(9) - 30):.1f}" y="{BASE - 150}" width="{fx(ch(3) + 30) - fx(ch(9) - 30):.1f}" height="150" fill="{a.BAD}" fill-opacity=".22"/>', 56, 75)
at(a, a.text(fx(ch(6)), BASE - 160, "se pisan entre ellos", 15, a.BAD, a.SANS, 600, "middle")
   + a.text(fx(ch(1)) - 20, BASE - 160, "EAP 1 · 40 MHz", 15, a.BLUE, a.MONO, 600, "start")
   + a.text(fx(ch(11)) + 20, BASE - 160, "EAP 2 · 40 MHz", 15, a.CYAN, a.MONO, 600, "end"), 56, 75)
# 4: 1 y 6 a 20
at(a, hump(ch(1) - 10, ch(1) + 10, 150, "#CFE3F7", a.BLUE, 0.75), 78, 100)
at(a, hump(ch(6) - 10, ch(6) + 10, 150, "#CDEFF8", a.CYAN, 0.75), 80, 100)
at(a, a.text(fx(ch(1)), BASE - 160, "EAP 1 · canal 1", 15, a.BLUE, a.MONO, 600, "middle")
   + a.text(fx(ch(6)), BASE - 160, "EAP 2 · canal 6", 15, a.CYAN, a.MONO, 600, "middle"), 80, 100)
at(a, check(a, fx(ch(6)) + 170, BASE - 166, 14) + a.text(fx(ch(6)) + 192, BASE - 160, "no se pisan", 15, a.OK, a.SANS, 600), 82, 100)

status(a, 568, [
    (0, 25, "14 canales en teoría, según el país; solo tres que no se superponen.", a.INK, 0),
    (25, 50, "Un canal entre medio pisa a medias a dos redes: lo peor de los dos mundos.", a.BAD, 1),
    (50, 75, "En 2.4 GHz, siempre 20 MHz: con 40 no queda lugar.", a.BAD, 0),
    (75, 100, "Antes de elegir, una app de análisis WiFi muestra qué usan los vecinos.", a.OK, 0),
], x=48, anchor="start", size=17)
status(a, 604, [
    (0, 100, "La región Uruguay en el sitio define qué canales y qué potencia son legales.", a.GREY, 1),
], x=48, anchor="start", size=16)

write(a, 8, "r1", "La banda de 2.4 GHz por dentro: por qué 1, 6 y 11",
      "Animación en cuatro tiempos con la banda de 2.4 GHz dibujada en frecuencia, canales del 1 al 13 y el espectro que ocupa cada transmisión. "
      "1: los canales están separados 5 MHz pero cada transmisión ocupa unos 20 MHz; solo 1, 6 y 11 no se superponen, y un canal intermedio como el 3 pisa al 1 y al 6. "
      "2: en un consultorio con redes vecinas en 1, 6 y 11, el EAP 1 en el canal 3 y el EAP 2 en el 9, a 20 MHz, pisan a medias a dos redes vecinas cada uno. "
      "3: como estaban configurados, a 40 MHz, cada uno ocupa el doble y además se pisan entre ellos. "
      "4: con el EAP 1 en el canal 1 y el EAP 2 en el 6, a 20 MHz, entre ellos no se pisan y con los vecinos comparten un canal entero, turnándose. "
      "Una app de análisis WiFi muestra qué canales usan los vecinos, y la región Uruguay en el sitio define canales y potencia legales.",
      [8, 36, 62, 90])
