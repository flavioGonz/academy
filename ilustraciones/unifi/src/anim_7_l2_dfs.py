#!/usr/bin/env python3
"""Lección 7 · Laboratorio, paso 5: Extended 5 GHz Spectrum (DFS). El AP usa un canal DFS limpio (64); aparece un
radar, el AP tiene que dejar el canal en el acto, los clientes se cortan y vuelve en otro canal; Time Machine anota el
evento. Fuentes: lab.md (pasos 5 y 6) y theory_md de la lección (802.11h, DFS); std.rocks ("if a priority signal is
detected, the access point must automatically vacate the channel"); Purple (el radar puede forzar el cambio y cortar
clientes). No se dibuja a qué canal salta ni cuánto tiempo queda vedado el 64: depende del equipo y la norma."""
from _anim_red_unifi import *  # noqa

a = new(24, "Canales angostos", "DFS: canales limpios, hasta que aparece un radar", [
    "Con Extended 5 GHz Spectrum (DFS), el AP usa el 64: limpio, sin vecinos.",
    "Aparece un radar meteorológico o militar en ese canal y el AP lo detecta.",
    "El AP tiene que dejar el canal en el acto: los clientes se cortan.",
    "Vuelve en otro canal y Time Machine anota el cambio por radar.",
], still=2, paso=5)

a.add(a.box(48, 186, 300, 100, a.WHITE, a.LINE, rx=14))
a.add(ap_icon(a, 88, 226, 20))
a.add(a.text(124, 222, "AP", 20, a.INK, a.HEAD, 600))
vis(a, a.text(124, 248, "canal 64 · DFS", 15, a.INK, a.MONO, 600), 0, 1)
vis(a, a.text(124, 248, "dejando el 64", 15, a.BAD, a.MONO, 600), 2)
vis(a, a.text(124, 248, "otro canal", 15, a.OK, a.MONO, 600), 3)
PH = [(108, 400), (198, 420), (288, 400)]
for x, y in PH:
    a.add(phone_icon(a, x, y))
for x, y in PH:
    vis(a, poly([(198, 286), (x, y - 24)], a.OK, 2.5, "5 5"), 0, 1)
    vis(a, poly([(198, 286), (x, y - 24)], a.OK, 2.5, "5 5"), 3)
    vis(a, xmark(a, x, y - 40, 12), 2)
vis(a, pill(a, 198, 460, "conectados", "ok", anchor="middle"), 0, 1)
vis(a, pill(a, 198, 460, "cortados", "bad", anchor="middle"), 2)
vis(a, pill(a, 198, 460, "reconectan", "ok", anchor="middle"), 3)

# radar
RX, RY = 1040, 250
a.add(a.box(930, 186, 222, 100, a.WHITE, a.LINE, rx=14) + glyph(a, "warn", 948, 204, a.AMB)
      + a.text(992, 222, "Radar", 19, a.INK, a.SANS, 600) + a.text(992, 246, "meteorológico", 15, a.GREY, a.MONO)
      + a.text(992, 268, "o militar", 15, a.GREY, a.MONO))
s0, s1 = ph(a, 1)
for k in range(4):
    t = s0 + 1 + k * 5
    during(a, "".join(arcs(a, 930, 236, [40, 70, 100], a.AMB, facing=180, spread=30, width=3)), t, t + 3.5, still=1 if k == 1 else 0)
during(a, pill(a, 640, 300, "radar en el canal 64", "amb", anchor="middle"), s0 + 6, ph(a, 2)[1], still=1)

# franja de canales de 5 GHz
SY = 520
a.add(a.text(420, SY - 74, "Canales de 5 GHz (según std.rocks)", 15, a.GREY, a.SANS, 600))
GROUPS = [("36 a 48", "sin DFS", 420, 200, a.LINE), ("52 a 64", "DFS", 640, 200, a.AMB), ("100 a 140", "DFS", 860, 292, a.AMB)]
for lab, sub, x, w, c in GROUPS:
    a.add(a.box(x, SY - 50, w, 50, a.WHITE, c, rx=10, sw=2.5))
    a.add(a.text(x + w / 2, SY - 20, lab, 16, a.INK, a.MONO, 600, "middle"))
    a.add(a.text(x + w / 2, SY + 24, sub, 15, a.GREY, a.SANS, 400, "middle"))
vis(a, a.box(640 + 150, SY - 50, 50, 50, a.OK, None, rx=10, extra='fill-opacity=".25"') + a.text(815, SY - 60, "64", 15, a.OK, a.MONO, 600, "middle"), 0, 1)
vis(a, a.box(640 + 150, SY - 50, 50, 50, a.BAD, None, rx=10, extra='fill-opacity=".35"') + a.text(815, SY - 60, "64", 15, a.BAD, a.MONO, 600, "middle"), 2, 3)

# 4 · Time Machine
s0, s1 = ph(a, 3)
during(a, a.box(420, 300, 732, 92, a.WHITE, a.LINE, rx=14) + a.text(440, 332, "AirView > Radios > Time Machine", 16, a.INK, a.SANS, 600)
       + a.pill(440, 348, "cambio de canal por radar", a.AMB, a.AMBBG, 15, 28), s0 + 4, 100)

status(a, 632, [
    (0, 25, "DFS suma canales, muchas veces más limpios que 36 a 48.", a.INK, 0),
    (25, 50, "Esos canales son de sistemas con prioridad: el WiFi los usa de prestado.", a.AMB, 0),
    (50, 75, "Dejar el canal no es opcional: es la regla para usar DFS.", a.BAD, 1),
    (75, 100, "Si Time Machine muestra cambios por radar seguido, volvé a los canales bajos.", a.INK, 0),
])

write(a, 7, "l2", "DFS y el radar",
      "Animación en cuatro tiempos del paso 5 con un AP y tres celulares, un radar y la franja de canales de 5 GHz según std.rocks: 36 a 48 sin DFS, 52 a 64 y 100 a 140 DFS. "
      "1: con Extended 5 GHz Spectrum (DFS) activado, el AP usa el canal 64, limpio, y los celulares están conectados. "
      "2: aparece un radar meteorológico o militar en el canal 64 y el AP lo detecta. "
      "3: el AP tiene que dejar el canal en el acto y los clientes se cortan. "
      "4: el AP vuelve en otro canal, los clientes reconectan y AirView > Radios > Time Machine anota el cambio de canal por radar. "
      "Si esos eventos se repiten, conviene volver a los canales bajos.",
      [12, 40, 64, 92])
