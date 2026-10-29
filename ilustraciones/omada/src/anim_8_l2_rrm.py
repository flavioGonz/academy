#!/usr/bin/env python3
"""Lección 8 · Laboratorio, paso 6: WLAN Optimization programada a las 3:30, separada del reinicio programado.
Mientras escanea los clientes se quedan sin internet varios minutos; los AP tienen que estar conectados."""
from _anim_om_red import *

a = nueva(26, "MENOS POTENCIA", "WLAN Optimization de madrugada, lejos del reinicio", "l")
F = a.steps([
    "Ejemplo: 3:00, reinicio programado de los AP. Vuelven y quedan Connected.",
    "3:30, WLAN Optimization: los AP escanean fuera de servicio y los clientes quedan sin internet.",
    "El controlador decide canal, ancho y potencia y los aplica; queda en Optimization Record.",
    "Si coincide con el reinicio, los AP no están conectados: separalos 10 minutos o más.",
], still=1)

# línea de tiempo
X0, X1, Y = 100, 1100, 250
a.add(a.box(48, 182, 1104, 120, a.WHITE, a.LINE, rx=16))
a.add(line(X0, Y, X1, Y, a.LINE, 8))
def tx(h):
    return X0 + (X1 - X0) * h / 6
for h in range(7):
    a.add(line(tx(h), Y - 10, tx(h), Y + 10, a.GREY, 2) + a.text(tx(h), Y + 34, f"{h}:00", 15, a.GREY, a.MONO, 400, "middle"))
at(a, a.box(tx(3) - 6, Y - 22, 12, 44, a.BLUE, rx=4) + a.text(tx(3), Y - 30, "reinicio", 15, a.BLUE, a.SANS, 600, "middle"), 0, 75, still=1)
at(a, a.box(tx(3.5) - 6, Y - 22, 40, 44, a.AMB, rx=4) + a.text(tx(3.5) + 14, Y - 30, "optimización", 15, a.AMB, a.SANS, 600, "start"), 0, 75, still=1)
at(a, a.box(tx(3) - 6, Y - 22, 46, 44, a.BAD, rx=4) + a.text(tx(3), Y - 30, "reinicio + optimización a la vez", 15, a.BAD, a.SANS, 600, "middle"), 75, 100)
# reloj que avanza
mv = a.move([(0, tx(2.8), Y), (20, tx(3.1), Y), (25, tx(3.45), Y), (48, tx(3.6), Y), (73, tx(3.75), Y), (76, tx(2.95), Y), (100, tx(3.1), Y)])
a.add(a.group(f'<circle r="11" fill="{a.WHITE}" stroke="{a.INK}" stroke-width="3"/>', mv, a.keyframes([(0, 1), (100, 1)]), still=0))

# equipos
EX = [160, 340, 520]
for i, x in enumerate(EX):
    a.add(eap(a, x, 390, 26) + a.text(x, 436, f"EAP {i + 1}", 15, a.INK, a.MONO, 600, "middle"))
ST = [  # (t0, t1, etiqueta, fg, bg)
    (0, 6, "Connected", a.OK, a.OKBG), (6, 14, "reiniciando", a.BLUE, "#E6F0FA"), (14, 28, "Connected", a.OK, a.OKBG),
    (28, 50, "escaneando", a.AMB, a.AMBBG), (50, 76, "Connected", a.OK, a.OKBG),
    (76, 100, "reiniciando", a.BAD, a.BADBG),
]
for t0, t1, lab, fg, bg in ST:
    for x in EX:
        at(a, chip(a, x, 450, lab, fg, bg, anchor="middle", stroke=fg), t0, t1, still=1 if t0 == 28 else 0)
# cliente
a.add(dev(a, 48, 500, 560, 70, "Clientes del local", "", icon="phone"))
at(a, a.text(292, 543, "navegan", 17, a.OK, a.SANS, 600), 0, 6)
at(a, a.text(292, 543, "corte corto por el reinicio", 17, a.BLUE, a.SANS, 600), 6, 14)
at(a, a.text(292, 543, "navegan", 17, a.OK, a.SANS, 600), 14, 28)
at(a, a.text(292, 543, "sin internet varios minutos", 17, a.BAD, a.SANS, 600), 28, 50, still=1)
at(a, a.text(292, 543, "navegan con lo nuevo", 17, a.OK, a.SANS, 600), 50, 76)
at(a, a.text(292, 543, "corte y optimización a medias", 17, a.BAD, a.SANS, 600), 76, 100)

# panel controlador
PX, PW = 650, 502
a.add(dev(a, PX, 330, PW, 70, "Controlador", "Network Config > Network Settings > WLAN", icon="server", dark=True, ssize=15))
at(a, note(a, PX, 418, PW, 152, "Mientras escanea", ["Cada AP mira el aire de su alrededor fuera de", "servicio. Por eso de madrugada, y nunca en", "horario de trabajo."], "amb"), 26, 50, still=1)
at(a, note(a, PX, 418, PW, 152, "Optimization Record", ["Canal, ancho y potencia nuevos por AP.", "Si el resultado no convence: Optimization", "Record Detail > Apply Previous Settings."], "ok"), 50, 76)
at(a, note(a, PX, 418, PW, 152, "Los AP tienen que estar conectados", ["Si se reinician mientras optimiza, el análisis", "queda incompleto. Separá las dos tareas al", "menos 10 minutos."], "bad"), 76, 100)
at(a, note(a, PX, 418, PW, 152, "Antes del paso 6", ["Fijate la hora del reinicio programado de", "los AP y elegí la de la optimización lejos."], "info"), 0, 26)
for t0 in (52, 58):
    for x in EX:
        travel(a, dot(a, a.OK, 7), [(PX, 365), (x + 30, 380)], t0, t0 + 3, hold=0.2)

write(a, 8, "l2", "WLAN Optimization de madrugada, separada del reinicio programado",
      "Animación en cuatro tiempos con una línea de tiempo de 0 a 6 de la mañana, tres EAP, los clientes del local y el controlador. "
      "1: como ejemplo, a las 3:00 corre el reinicio programado; los AP se reinician, vuelven y quedan Connected, con un corte corto para los clientes. "
      "2: a las 3:30 corre WLAN Optimization: los AP escanean fuera de servicio y los clientes se quedan sin internet varios minutos; por eso va de madrugada. "
      "3: el controlador decide canal, ancho y potencia, los aplica a cada AP y lo deja en Optimization Record; si no convence, Apply Previous Settings vuelve atrás. "
      "4: si la optimización coincide con el reinicio, los AP no están conectados mientras optimiza y el análisis queda a medias: hay que separar las dos tareas al menos 10 minutos.",
      [8, 36, 62, 90])
