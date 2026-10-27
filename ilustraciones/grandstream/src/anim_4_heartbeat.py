#!/usr/bin/env python3
"""Lección 4 · teoría: heartbeat con OPTIONS cada 60 s y paso al troncal de failover."""
from _anim_grandstream import G

g = G(T=26, fix=90, kicker="GRANDSTREAM · TRONCAL SIP", title="Heartbeat: la central pregunta si el troncal vive")
g.steps([
    "Con heartbeat activo, la UCM manda OPTIONS cada 60 s y el proveedor contesta.",
    "Las llamadas salen por el troncal principal mientras contesta.",
    "El proveedor deja de contestar: los OPTIONS quedan sin respuesta.",
    "La UCM da el troncal por caído y la ruta usa el troncal de failover.",
])

# equipos
g.add(g.node(48, 322, 190, 76, "Interna 1001", "marca afuera"))
g.add(g.node(400, 300, 230, 120, "UCM", "heartbeat activo", dark=True, tsize=22))
g.add(g.node(870, 196, 282, 80, "Proveedor_Lab", "troncal principal"))
g.add(g.node(870, 456, 282, 80, "Segundo troncal", "failover de la ruta"))

P1, P2 = (630, 336), (870, 236)       # UCM → principal
F1, F2 = (630, 386), (870, 496)       # UCM → failover
g.add(f'<path d="M238 360 H400" stroke="{g.LINE}" stroke-width="4"/>')
g.add(f'<path d="M{P1[0]} {P1[1]} L{P2[0]} {P2[1]}" stroke="{g.LINE}" stroke-width="4"/>')
g.add(f'<path d="M{F1[0]} {F1[1]} L{F2[0]} {F2[1]}" stroke="{g.LINE}" stroke-width="4" stroke-dasharray="8 8"/>')
# tramo en uso
g.appear(f'<path d="M238 360 H400" stroke="{g.OK}" stroke-width="5"/><path d="M{P1[0]} {P1[1]} L{P2[0]} {P2[1]}" stroke="{g.OK}" stroke-width="5"/>', 27, 50)
g.appear(f'<path d="M238 360 H400" stroke="{g.OK}" stroke-width="5"/><path d="M{F1[0]} {F1[1]} L{F2[0]} {F2[1]}" stroke="{g.OK}" stroke-width="5"/>', 80, 100)

def opt(t, answered=True):
    g.token([P1, P2], t, t + 4.5, g.chip("OPTIONS", bg=g.BLUE, size=13, h=24))
    if answered:
        g.token([P2, P1], t + 5.5, t + 9.5, g.chip("200 OK", bg=g.OK, size=13, h=24))
    else:
        g.appear(g.mark(P2[0] - 30, P2[1] + 30, False, 15), t + 4.5, t + 11)

opt(2); opt(13); opt(38)
opt(52, False); opt(63, False)

# llamadas
g.token([(238, 360), (400, 360)], 27, 30, g.chip("llamada", bg=g.CYAN, size=13, h=24))
g.token([P1, P2], 31, 36, g.chip("llamada", bg=g.CYAN, size=13, h=24))
g.token([(238, 360), (400, 360)], 79, 82, g.chip("llamada", bg=g.CYAN, size=13, h=24))
g.token([F1, F2], 83, 88, g.chip("llamada", bg=g.CYAN, size=13, h=24))

# estados del principal
PX = 1011
g.appear(g.pillc(PX, 290, "registrado · contesta", g.OK, g.OKBG), 0, 51)
g.appear(g.pillc(PX, 290, "sin respuesta", g.AMB, g.AMBBG), 51, 76)
g.appear(g.pillc(PX, 290, "caído", g.BAD, g.BADBG), 76, 100)
g.appear(g.pillc(1011, 550, "en uso", g.OK, g.OKBG), 80, 100)
g.appear(g.pillc(1011, 550, "en espera", g.GREY, g.SLATE), 0, 80)

# notas
g.add(g.note(48, 470, 520, "Advanced Settings del troncal", [
    "Enable Heartbeat Detection: Sí", "Heartbeat Frequency: 60 (segundos)"], "info"))
g.appear(g.note(48, 580, 760, None, ["Sin respuesta al OPTIONS, la UCM considera el troncal caído."], "amb"), 52, 76)
g.appear(g.note(48, 580, 760, None, ["Las salientes siguen por el troncal de failover de la ruta."], "ok"), 78, 100)
g.appear(g.note(48, 580, 760, None, ["OPTIONS pregunta qué soporta el otro equipo y, de paso, si está vivo."], "info"), 0, 50)

g.finish(4, 1, "Heartbeat: la central pregunta si el troncal vive",
         "Animación en cuatro tiempos con la interna 1001, la UCM con heartbeat activo, el troncal principal Proveedor_Lab y un segundo troncal configurado como failover de la ruta. "
         "1: la UCM manda OPTIONS al proveedor cada 60 segundos y el proveedor contesta 200 OK; el troncal figura registrado. "
         "2: una llamada de la 1001 sale por el troncal principal. "
         "3: el proveedor deja de contestar y los OPTIONS quedan sin respuesta. "
         "4: la UCM da el troncal principal por caído y la siguiente llamada sale por el troncal de failover. "
         "Notas: en Advanced Settings del troncal, Enable Heartbeat Detection en Sí y Heartbeat Frequency en 60; OPTIONS sirve para preguntar qué soporta el otro equipo y, de paso, si está vivo.",
         [8, 34, 58, 90])
