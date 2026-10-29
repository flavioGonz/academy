#!/usr/bin/env python3
"""Lección 8 (Grupo o cola) · Laboratorio, paso 5: dos llamadas a la cola 6500 con un agente ocupado. Least Recent
entrega cada llamada al agente libre que hace más tiempo que no atiende; con la fila llena (Max Queue Length 5),
la que sobra va al Failover Destination, Ring Group 6000. Fuentes: la lección (Least Recent; Max Queue Length; la
sexta llamada en espera va al Failover Destination) y la configuración del laboratorio."""
from _anim_gs_red import R

g = R(T=26, fix=40, kicker="GRANDSTREAM · GRUPO O COLA · LABORATORIO",
      title="Least Recent: a quién le toca cada llamada")
g.steps([
    "Entra la llamada 1: la 1001 está ocupada y, de las libres, la 1003 hace más que no atiende.",
    "Entra la 2 a la vez: ahora la que hace más que no atiende es la 1002.",
    "Con los tres agentes hablando, las que siguen esperan en la fila: hasta 5.",
    "La sexta en espera ya no entra: va al Failover Destination, el Ring Group 6000.",
])

AX, AW = 856, 296
AG = [(1001, 186), (1002, 270), (1003, 354)]
for n, y in AG:
    g.add(g.dev(AX, y, AW, 72, str(n), icon="tel", tsize=19))
# estado de cada agente
g.add(g.pillc(AX + 206, 186 + 23, "en otra llamada", g.BAD, g.BADBG, 13, 26))
g.appear(g.pillc(AX + 206, 270 + 23, "atendió hace 2 min", g.GREY, g.SLATE, 13, 26), 0, 37)
g.appear(g.pillc(AX + 206, 354 + 23, "atendió hace 15 min", g.GREY, g.SLATE, 13, 26), 0, 12)
g.appear(g.pillc(AX + 206, 354 + 23, "hablando · 1", g.OK, g.OKBG, 13, 26), 12, 100)
g.appear(g.pillc(AX + 206, 270 + 23, "hablando · 2", g.OK, g.OKBG, 13, 26), 37, 100)
g.appear(g.box(AX, 354, AW, 72, "none", g.OK, rx=14, sw=3.5), 6, 25)
g.appear(g.box(AX, 270, AW, 72, "none", g.OK, rx=14, sw=3.5), 30, 50)

# cola
QX, QY, QW = 300, 186, 500
g.add(g.box(QX, QY, QW, 240, g.WHITE, g.LINE, rx=16))
g.add(g.text(QX + 20, QY + 34, "Call Queue 6500 · Least Recent", 18, g.INK, g.HEAD, 600))
g.add(g.text(QX + 20, QY + 62, "Max Queue Length: 5", 15, g.TXT, g.MONO))
g.add(g.text(QX + 20, QY + 100, "fila", 15, g.GREY, g.MONO))
SL = [QX + 20 + k * 94 for k in range(5)]
for x in SL:
    g.add(g.box(x, QY + 114, 82, 44, g.SLATE, None, rx=10))
g.add(g.text(QX + 20, QY + 196, "Agent Ring Time 30 · Retry 5 · Rest 10", 15, g.GREY, g.MONO))

chip = lambda s, c=None: g.chip(s, bg=c or g.CYAN, size=14, h=28)
g.token([(120, 230), (QX + QW / 2, QY + 136), (AX - 50, 390)], 2, 10, chip("1"), hold=100)
g.token([(120, 290), (QX + QW / 2, QY + 136), (AX - 50, 306)], 27, 35, chip("2"), hold=100)
for k in range(5):
    t = 53 + k * 3.6
    g.token([(120, 350), (SL[k] + 41, QY + 136)], t, t + 3, chip(str(k + 3), g.AMB), hold=100)
g.appear(g.box(QX, 486, QW, 60, g.AMBBG, g.AMB, rx=12, sw=2) + g.text(QX + 20, 522, "Failover Destination: Ring Group 6000", 17, g.AMB, g.SANS, 600), 76, 100)
g.token([(120, 350), (QX + QW / 2, QY + 260), (QX + QW - 40, 516)], 78, 86, chip("8", g.BAD), hold=100)
g.add(g.text(48, 200, "entran", 15, g.GREY, g.MONO))
g.appear(g.pillc(QX + QW / 2, QY + 220, "fila llena", g.BAD, g.BADBG, 13, 24), 72, 100)
g.fijo_only(f'<g transform="translate({AX - 50} 390)">' + chip("1") + '</g>'
            + f'<g transform="translate({AX - 50} 306)">' + chip("2") + '</g>')

g.appear(g.note(48, 566, 1104, None, ["Least Recent mira cuánto hace que cada agente libre atendió su última llamada, no cuántas atendió (eso es Fewest Calls)."], "info"), 0, 75)
g.appear(g.note(48, 566, 1104, None, ["Max Queue Length viene en 0, sin límite: con 5, la sexta en espera escucha ocupado y va al desborde."], "amb"), 75, 100)

g.done(8, "l1", "Least Recent: a quién le toca cada llamada",
       "Animación en cuatro tiempos con la cola 6500 en Least Recent y Max Queue Length 5, su fila de cinco lugares, y tres agentes: la 1001 en otra llamada, la 1002 que atendió hace 2 minutos y la 1003 que atendió hace 15. "
       "1: entra la llamada 1; la 1001 está ocupada y, de las libres, la 1003 es la que hace más tiempo que no atiende: le toca a ella. "
       "2: entra la 2 a la vez y ahora la que hace más que no atiende es la 1002, que la recibe. "
       "3: con los tres agentes hablando, las llamadas 3 a 7 esperan en la fila hasta llenarla. "
       "4: la llamada 8, sexta en espera, ya no entra y va al Failover Destination, el Ring Group 6000. "
       "Least Recent mira cuánto hace que cada agente libre atendió, no cuántas llamadas atendió (eso es Fewest Calls). Max Queue Length viene en 0, sin límite.",
       [8, 34, 66, 92])
