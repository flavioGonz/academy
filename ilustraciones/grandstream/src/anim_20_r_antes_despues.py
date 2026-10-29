#!/usr/bin/env python3
"""IVR que solo anuncia · Resumen ("Cómo se ve en la red"): 20-r1.svg.
El recorrido de la llamada antes y después del arreglo, en una línea de tiempo de ejemplo:
antes, con marcar internos prendido, un 5 falso de la línea dispara el aviso de inválido y con
repeticiones en 3 el grupo suena recién a los 54 s; después, bienvenida, 2 s de silencio y grupo a los 14 s.
Bienvenida de 12 s y Digit Timeout de 3 s (de fábrica, según el manual); los segundos son de ejemplo.
"""
from _anim_gs_red import R

g = R(T=28, fix=95, kicker="GRANDSTREAM · IVR QUE SOLO ANUNCIA · CÓMO SE VE EN LA RED", title="Antes y después: cuánto tarda en sonar el grupo")
g.steps([
    "Antes: suena la bienvenida y la línea mete un 5 que nadie marcó.",
    "El IVR espera más dígitos, busca el interno 5, no existe: aviso de inválido.",
    "Repeticiones en 3: saludo y aviso otra vez; el grupo suena recién a los 54 s.",
    "Después: sin marcar internos y repeticiones en 1, el grupo suena a los 14 s.",
], size=17)

B, OK, BAD, AMB, GREY, INK = g.BLUE, g.OK, g.BAD, g.AMB, g.GREY, g.INK
NY = 176
g.add(g.dev(48, NY, 290, 72, "Línea de Antel", "FXO1 · ruido y eco", icon="antel"))
g.add(g.dev(455, NY, 290, 72, "IVR 7000", "bienvenida", icon="ucm", dark=True))
g.add(g.dev(862, NY, 290, 72, "Ring Group 6000", "1001 · 1002", icon="tel"))
g.add(g.wire(338, NY + 36, 455, NY + 36, w=4))
g.add(g.wire(745, NY + 36, 862, NY + 36, w=4))

# dígitos falsos que entran por la línea
for t0 in (7, 53, 62):
    g.token([(338, NY + 36), (455, NY + 36)], t0, t0 + 3.5, g.chip("5 falso", bg=AMB, size=13, h=24))
# qué hace el IVR
g.appear(g.pillc(600, 262, "busca el interno 5: no existe", BAD, g.BADBG, 14, 28), 26, 31, still=0)
g.appear(g.pillc(600, 262, "«Lo siento, no lo entiendo»", BAD, g.BADBG, 14, 28), 31, 50, still=0)
g.appear(g.pillc(600, 262, "vuelta 2 de 3", BAD, g.BADBG, 14, 28), 51, 60, still=0)
g.appear(g.pillc(600, 262, "vuelta 3 de 3 · después, Invalid", BAD, g.BADBG, 14, 28), 60, 75, still=0)
g.appear(g.pillc(600, 262, "Response Timeout · Ring Group 6000", OK, g.OKBG, 14, 28), 84, 100)
g.token([(745, NY + 36), (836, NY + 36)], 69, 72, g.chip("al grupo", bg=BAD, size=13, h=24), hold=75)
g.token([(745, NY + 36), (836, NY + 36)], 86, 89, g.chip("al grupo", bg=OK, size=13, h=24), hold=100)

# líneas de tiempo
X0, PX = 170, 980 / 60          # 0 a 60 s
def seg(y, s0, s1, t0, t1, color, label=None, lc=None):
    x, w = X0 + s0 * PX, (s1 - s0) * PX - 3
    g.bar(x, y, w, 36, t0, t1, color)
    if label:
        g.appear(g.text(x + w / 2, y + 24, label, 13, lc or g.WHITE, g.SANS, 600, "middle"), t1, 100)

YA, YD = 336, 424
g.add(g.text(48, YA + 24, "Antes", 18, INK, g.HEAD, 600))
g.add(g.text(48, YD + 24, "Después", 18, INK, g.HEAD, 600))
g.add(g.box(X0, YA, 980, 36, g.SLATE, rx=6))
g.add(g.box(X0, YD, 980, 36, g.SLATE, rx=6))
cyc = [((2, 13), (26, 29), (31, 35)), ((51, 55), (55, 56.5), (56.5, 58)), ((60, 64), (64, 65.5), (65.5, 67))]
for k, (w_, d_, a_) in enumerate(cyc):
    s0 = 18 * k
    seg(YA, s0, s0 + 12, *w_, B, "bienvenida")
    seg(YA, s0 + 12, s0 + 15, *d_, GREY, "3 s")
    seg(YA, s0 + 15, s0 + 18, *a_, BAD, "aviso")
seg(YA, 54, 60, 69, 72, OK, "grupo")
g.appear(g.pill(X0 + 54 * PX - 6, YA - 34, "suena a los 54 s", BAD, g.BADBG, 13, 26, "end"), 70, 100)
seg(YD, 0, 12, 76, 84, B, "bienvenida")
seg(YD, 12, 14, 84, 86, "#B9C6D3", "2 s", INK)
seg(YD, 14, 20, 86, 89, OK, "grupo")
g.appear(g.pill(X0 + 20 * PX + 10, YD + 4, "suena a los 14 s", OK, g.OKBG, 13, 28), 88, 100)
# eje
for s in (0, 15, 30, 45, 60):
    x = X0 + s * PX
    g.add(f'<line x1="{x:.1f}" y1="{YD + 46}" x2="{x:.1f}" y2="{YD + 54}" stroke="{GREY}" stroke-width="1.5"/>')
    g.add(g.text(x, YD + 74, f"{s} s", 13, GREY, g.MONO, 400, "middle"))
g.add(g.text(48, YD + 74, "(ejemplo)", 13, GREY, g.SANS, 400))

# lo que pasa (abajo)
PY = 528
g.add(g.box(48, PY, 1104, 104, g.WHITE, g.LINE, rx=14))
ROWS = [
    (0, 25, "Dial Other Extensions: Extension, Ring Group · ninguna tecla", "el detector del FXO toma ruido o eco por un 5", AMB),
    (25, 50, "Digit Timeout 3 s · interno 5: no existe", "Invalid Input Prompt: «Lo siento, no lo entiendo»", BAD),
    (50, 75, "Invalid Input Prompt Repeats: 3", "tres vueltas y recién ahí el destino Invalid: Ring Group 6000", BAD),
    (75, 100, "Dial Other Extensions: nada · Response Timeout 2 s · Repeats 1", "bienvenida, silencio y Ring Group 6000 por el destino de Timeout", OK),
]
for t0, t1, a, b, col in ROWS:
    g.appear(g.text(72, PY + 40, a, 16, INK, g.MONO, 600) + g.text(72, PY + 74, b, 17, col, g.SANS, 600), t0, t1)

g.done(20, "r1", "Antes y después: cuánto tarda en sonar el grupo",
       "Animación en cuatro tiempos. Arriba, la línea de Antel por el FXO1, el IVR 7000 y el Ring Group 6000 con las internas 1001 y 1002; "
       "abajo, dos líneas de tiempo de 0 a 60 segundos de ejemplo, antes y después del arreglo. "
       "1: antes, con Dial Other Extensions en Extension y Ring Group y ninguna tecla, suena la bienvenida de 12 segundos y el FXO toma ruido o eco de la línea por un 5. "
       "2: el IVR espera más dígitos durante el Digit Timeout de 3 segundos, busca el interno 5, no existe y suena el aviso de opción inválida, Lo siento, no lo entiendo. "
       "3: con Invalid Input Prompt Repeats en 3, saludo y aviso vuelven dos veces más y el grupo suena recién a los 54 segundos, por el destino Invalid. "
       "4: después, con marcar internos apagado, Response Timeout de 2 segundos y repeticiones en 1, suena la bienvenida, 2 segundos de silencio y el grupo a los 14 segundos, por el destino de Timeout.",
       [6, 9, 20, 30, 42, 58, 72, 86, 95])
