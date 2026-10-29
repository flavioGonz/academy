#!/usr/bin/env python3
"""Lección 8 · Laboratorio, paso 5: medir después desde los mismos tres puntos. Si un punto queda por debajo de -70 dBm,
se sube un escalón la potencia solo del EAP que lo cubre y se vuelve a medir. Valores de ejemplo."""
from _anim_om_red import *

a = nueva(26, "MENOS POTENCIA", "Medí desde los mismos puntos y corregí solo un AP", "l")
F = a.steps([
    "Con el celular y la app de análisis WiFi, medí la señal en los mismos tres puntos.",
    "A y B quedan mejor que -70 dBm. C, en la punta, queda en -74: le falta señal.",
    "C lo cubre el EAP 2: subí un escalón solo su potencia, de Medium a High.",
    "Volvé a medir C: ahora -67 dBm. El EAP 1 queda como estaba.",
], still=1)

# planta
PX, PY, PW, PH = 48, 186, 600, 384
a.add(a.box(PX, PY, PW, PH, a.WHITE, a.LINE, rx=16))
a.add(a.text(PX + 20, PY + 30, "Planta · valores de ejemplo", 15, a.GREY, a.MONO))
E1, E2 = (210, 400), (470, 400)
# celdas
a.add(f'<circle cx="{E1[0]}" cy="{E1[1]}" r="130" fill="{a.BLUE}" fill-opacity=".07" stroke="{a.BLUE}" stroke-width="2" stroke-dasharray="6 6"/>')
at(a, f'<circle cx="{E2[0]}" cy="{E2[1]}" r="130" fill="{a.CYAN}" fill-opacity=".08" stroke="{a.CYAN}" stroke-width="2" stroke-dasharray="6 6"/>', 0, 54, still=1)
at(a, f'<circle cx="{E2[0]}" cy="{E2[1]}" r="160" fill="{a.CYAN}" fill-opacity=".08" stroke="{a.CYAN}" stroke-width="2.5" stroke-dasharray="6 6"/>', 54, 100)
a.add(eap(a, *E1, 24) + a.text(E1[0], E1[1] + 46, "EAP 1 · Medium", 15, a.BLUE, a.MONO, 600, "middle"))
a.add(eap(a, *E2, 24))
at(a, a.text(E2[0], E2[1] + 46, "EAP 2 · Medium", 15, a.CYAN, a.MONO, 600, "middle"), 0, 54, still=1)
at(a, a.text(E2[0], E2[1] + 46, "EAP 2 · High", 15, a.AMB, a.MONO, 600, "middle"), 54, 100)
PTS = {"A": (150, 300), "B": (330, 360), "C": (598, 488)}
for k, (x, y) in PTS.items():
    a.add(f'<circle cx="{x}" cy="{y}" r="16" fill="{a.WHITE}" stroke="{a.INK}" stroke-width="2"/>' + a.text(x, y + 6, k, 16, a.INK, a.MONO, 600, "middle"))
# el celular recorre los puntos
PH_ = f'<rect x="-11" y="-18" width="22" height="36" rx="5" fill="{a.INK}"/><rect x="-7" y="-13" width="14" height="22" rx="2" fill="{a.CYAN}"/>'
mv = a.move([(0, 150, 266), (6, 150, 266), (12, 330, 326), (20, 598, 454), (100, 598, 454)])
a.add(a.group(PH_, mv, a.keyframes([(0, 1), (100, 1)]), still=0))
solo_fijo(a, f'<g transform="translate(598,454)">{PH_}</g>')

# planilla
TX, TY, TW = 680, 186, 472
a.add(a.box(TX, TY, TW, 270, a.WHITE, a.LINE, rx=16))
a.add(a.text(TX + 20, TY + 32, "Planilla del paso 5", 16, a.INK, a.SANS, 600))
a.add(a.text(TX + 20, TY + 66, "Punto", 15, a.GREY, a.SANS, 600) + a.text(TX + 120, TY + 66, "AP", 15, a.GREY, a.SANS, 600) + a.text(TX + 220, TY + 66, "Después", 15, a.GREY, a.SANS, 600) + a.text(TX + 340, TY + 66, "Ajuste", 15, a.GREY, a.SANS, 600))
ROWS = [("A", "EAP 1", "-58 dBm", 7, a.OK), ("B", "EAP 1", "-63 dBm", 13, a.OK), ("C", "EAP 2", "-74 dBm", 21, a.BAD)]
for i, (p, ap, v, t0, col) in enumerate(ROWS):
    y = TY + 104 + i * 40
    a.add(a.text(TX + 20, y, p, 16, a.INK, a.MONO, 600) + a.text(TX + 120, y, ap, 15, a.TXT, a.MONO))
    if p != "C":
        at(a, a.text(TX + 220, y, v, 16, col, a.MONO, 600), t0, 100, still=1)
    else:
        at(a, a.text(TX + 220, y, v, 16, col, a.MONO, 600), t0, 78, still=1)
        at(a, a.text(TX + 220, y, "-67 dBm", 16, a.OK, a.MONO, 600), 78, 100)
        at(a, a.text(TX + 340, y, "+1 escalón", 15, a.AMB, a.MONO, 600), 54, 100)
at(a, a.box(TX + 10, TY + 104 + 2 * 40 - 26, TW - 20, 38, "none", a.BAD, rx=8, sw=2), 26, 52, still=1)
# escala
SY = TY + 236
a.add(a.text(TX + 20, SY, "mejor que -70: alcanza", 15, a.OK, a.SANS, 600) + a.text(TX + TW - 20, SY, "peor: un escalón", 15, a.AMB, a.SANS, 600, "end"))

at(a, note(a, TX, 476, TW, 94, "Solo el AP que cubre ese punto", ["Subir todos a High trae de vuelta la interferencia", "y el cliente pegado al AP lejano."], "amb"), 50, 100)
at(a, note(a, TX, 476, TW, 94, "Mismos puntos que en el paso 1", ["Así el antes y el después se pueden comparar.", "Anotá canal, ancho y dBm del AP asociado."], "info"), 0, 50, still=1)

status(a, 622, [
    (0, 25, "El celular mide la señal del AP al que quedó asociado en cada punto.", a.INK, 0),
    (25, 50, "Por debajo de -70 dBm en un lugar de trabajo, falta señal ahí.", a.BAD, 1),
    (50, 75, "Devices > (EAP 2) > Config > Radios: un escalón más de potencia.", a.INK, 0),
    (75, 100, "Medir, ajustar uno y volver a medir: el ciclo termina cuando todos alcanzan.", a.OK, 0),
], x=48, anchor="start", size=16)

write(a, 8, "l1", "Medir después y corregir la potencia de un solo AP",
      "Animación en cuatro tiempos con la planta de un local, el EAP 1 y el EAP 2 en potencia Medium con sus celdas, tres puntos de medición A, B y C y la planilla del paso 5, con valores de ejemplo. "
      "1: con el celular y una app de análisis WiFi se mide la señal del AP asociado en los mismos tres puntos del paso 1. "
      "2: A da -58 dBm y B -63 dBm con el EAP 1, mejor que -70; C, en la punta, da -74 dBm con el EAP 2: le falta señal. "
      "3: como C lo cubre el EAP 2, se sube un escalón solo su potencia, de Medium a High, en Devices, EAP 2, Config, Radios, y su celda crece. "
      "4: se vuelve a medir C y da -67 dBm; el EAP 1 queda como estaba. Subir todos a High traería de vuelta la interferencia y el cliente pegado al AP lejano.",
      [8, 36, 62, 90])
