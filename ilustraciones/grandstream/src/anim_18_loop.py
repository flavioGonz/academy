#!/usr/bin/env python3
"""Lección 18 · teoría: hipótesis del caso real, el FXO2 que se ocupa y se libera cada unos 10 s."""
from _anim_grandstream import G

g = G(T=24, fix=88, kicker="GRANDSTREAM · DIAGNÓSTICO · HIPÓTESIS", title="El loop de 10 s: toma, espera, suelta y vuelve")
g.steps([
    "En el FXO2 aparece algo que la UCM toma por timbre: un timbre real, ruido o una inversión.",
    "La UCM toma la llamada: el puerto se pone naranja y la llamada queda en s, sin destino.",
    "No vuelve a sonar: pasado el Ring Timeout de 8000 ms, la UCM la da por cortada.",
    "El puerto se libera un instante y, si el disparo se repite, el ciclo vuelve a empezar.",
])
USO, LIBRE = "#F29A1F", "#0A63B8"

# puerto FXO2 grande
g.add(g.text(48, 204, "Interface Status · FXO2", 17, g.INK, g.SANS, 600))
g.add(g.box(48, 220, 150, 120, g.WHITE, g.LINE, rx=16))
g.appear(g.box(48, 220, 150, 120, LIBRE, rx=16) + g.text(123, 292, "libre", 20, g.WHITE, g.SANS, 700, "middle"), 0, 8)
g.appear(g.box(48, 220, 150, 120, USO, rx=16) + g.text(123, 292, "en uso", 20, g.WHITE, g.SANS, 700, "middle"), 8, 70)
g.appear(g.box(48, 220, 150, 120, LIBRE, rx=16) + g.text(123, 292, "libre", 20, g.WHITE, g.SANS, 700, "middle"), 70, 100)
# disparo
g.appear(g.pillc(410, 214, "¿timbre? ¿ruido? ¿inversión?", g.AMB, g.AMBBG, size=15, h=30), 2, 25)
g.arrow([(300, 260), (206, 260)], 3, 8, g.AMB, hold=25)
g.appear(g.pillc(410, 214, "se repite el disparo", g.AMB, g.AMBBG, size=15, h=30), 88, 100)
g.arrow([(300, 260), (206, 260)], 89, 94, g.AMB, hold=100)
# Active Calls
g.add(g.box(320, 264, 420, 76, g.WHITE, g.LINE, rx=14))
g.add(g.text(340, 290, "Active Calls", 15, g.BLUE, g.MONO, 600))
for k, t0 in enumerate((26, 32, 38, 44, 50, 56, 62)):
    g.appear(g.text(340, 322, f"DAHDI/o2 · Antel_Linea2 → s · 00:00:0{k + 2}", 16, g.INK, g.MONO, 600), t0, t0 + 6)
g.appear(g.text(340, 322, "sin llamadas", 16, g.GREY, g.MONO, 500), 68, 100)
g.appear(g.text(340, 322, "sin llamadas", 16, g.GREY, g.MONO, 500), 0, 26)
# reloj del Ring Timeout
g.add(g.box(780, 220, 372, 120, g.WHITE, g.LINE, rx=16))
g.add(g.text(800, 252, "Ring Timeout: 8000 ms", 17, g.INK, g.MONO, 600))
g.add(g.box(800, 276, 332, 22, g.SLATE, rx=6))
g.bar(800, 276, 332, 22, 26, 56, USO, hold=70)
g.appear(g.text(966, 326, "esperando otro timbre…", 15, g.GREY, g.SANS, 500, "middle"), 26, 56)
g.appear(g.text(966, 326, "no sonó: la da por cortada", 15, g.BAD, g.SANS, 600, "middle"), 56, 76)

# línea de tiempo de 30 s
TX, TW, TY = 120, 1000, 420
g.add(g.text(48, TY - 18, "Lo que se ve en el Dashboard durante 30 segundos", 17, g.INK, g.SANS, 600))
for cyc in range(3):
    x0 = TX + cyc * TW / 3
    w_uso = TW / 3 * 0.85
    g.add(g.box(x0, TY, w_uso, 40, USO, rx=6))
    g.add(g.box(x0 + w_uso, TY, TW / 3 - w_uso, 40, LIBRE, rx=6))
for s in range(0, 31, 5):
    g.add(g.text(TX + s * TW / 30, TY + 66, f"{s} s", 15, g.GREY, g.MONO, 500, "middle"))
g.add(g.text(TX + TW / 6, TY + 26, "en uso, unos 8,5 s", 15, g.WHITE, g.SANS, 600, "middle"))
g.add(g.group(f'<path d="M0 {TY - 8}V{TY + 48}" stroke="{g.INK}" stroke-width="3"/>',
              g.move([(0, TX, 0), (8, TX, 0), (70, TX + TW / 3 * 0.85, 0), (100, TX + TW / 3, 0)]), still=0))

g.add(g.note(48, 520, 1104, None, ["Es una hipótesis que encaja con lo visto, no un diagnóstico: se confirma midiendo el par, cambiando el par de puerto",
                                     "y grabando el FXO2 con Analog Record Trace durante dos o tres ciclos."], "amb", lh=24))

g.finish(18, 1, "El loop de 10 s: toma, espera, suelta y vuelve",
         "Animación en cuatro tiempos que muestra una hipótesis del caso real: un FXO2 que se ocupa y se libera cada unos 10 segundos. Arriba, el estado del FXO2, lo que muestra Active Calls y una barra del Ring Timeout de 8000 ms; abajo, una línea de tiempo de 30 segundos con tres ciclos naranja y azul. "
         "1: en el FXO2 aparece algo que la UCM toma por timbre, que puede ser un timbre real, ruido o una inversión de polaridad. "
         "2: la UCM toma la llamada, el puerto pasa a en uso y Active Calls muestra DAHDI/o2 por Antel_Linea2 hacia s, sin destino, mientras corre el tiempo. "
         "3: no vuelve a sonar y, pasado el Ring Timeout de 8000 ms, la UCM la da por cortada. "
         "4: el puerto se libera un instante y, si el disparo se repite, el ciclo vuelve a empezar, lo que en el Dashboard se ve como unos 8,5 segundos en uso y un instante libre cada 10 segundos. "
         "Nota: es una hipótesis que encaja con lo visto, no un diagnóstico; se confirma midiendo el par, cambiando el par de puerto y grabando el FXO2 con Analog Record Trace.",
         [12, 37, 62, 88])
