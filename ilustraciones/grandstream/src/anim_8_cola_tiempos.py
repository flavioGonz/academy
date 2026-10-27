#!/usr/bin/env python3
"""Lección 8 · teoría: los tiempos de la cola (Agent Ring Time, Retry Time, Agent Rest Time) en una línea de tiempo."""
from _anim_grandstream import G

g = G(T=26, fix=96, kicker="GRANDSTREAM · COLA DE LLAMADAS", title="Los tiempos de una cola, segundo a segundo")
g.steps([
    "Entra una llamada: espera con música y suena el 1001 durante 30 s.",
    "No atendió: la central espera 5 s y prueba con el siguiente, el 1002, que atiende.",
    "El 1002 habla con quien llamó; la llamada ya salió de la fila.",
    "Al cortar, el 1002 descansa 10 s antes de que la cola le pase otra.",
])

# tiempo simulado (s) → porcentaje del ciclo, por tramos
MAP = [(0, 2), (30, 24), (45, 48), (80, 72), (90, 92), (100, 97)]


def P(s):
    for (s0, p0), (s1, p1) in zip(MAP, MAP[1:]):
        if s0 <= s <= s1:
            return p0 + (p1 - p0) * (s - s0) / (s1 - s0)
    return MAP[-1][1]


X0, X1, SMAX = 270, 1130, 100
def X(s):
    return X0 + (X1 - X0) * s / SMAX


ROWS = {"cola": 214, "1001": 300, "1002": 386}
RH = 48
for name, y in [("Llamada en la cola", ROWS["cola"]), ("Agente 1001", ROWS["1001"]), ("Agente 1002", ROWS["1002"])]:
    g.add(g.box(48, y, 200, RH, g.WHITE, g.LINE, rx=12) + g.text(66, y + 30, name, 17, g.INK, g.SANS, 600))
    g.add(f'<line x1="{X0}" y1="{y + RH / 2}" x2="{X1}" y2="{y + RH / 2}" stroke="{g.LINE}" stroke-width="2" stroke-dasharray="3 6"/>')

# eje
AY = 470
g.add(f'<line x1="{X0}" y1="{AY}" x2="{X1}" y2="{AY}" stroke="{g.GREY}" stroke-width="1.5"/>')
for s in range(0, 101, 10):
    g.add(f'<line x1="{X(s)}" y1="{AY}" x2="{X(s)}" y2="{AY + 8}" stroke="{g.GREY}" stroke-width="1.5"/>')
    g.add(g.text(X(s), AY + 28, f"{s} s" if s in (0, 100) else str(s), 14, g.GREY, g.MONO, 400, "middle"))


def seg(row, s0, s1, col, label=None, lcol=g.WHITE, hold=100):
    y = ROWS[row] + 6
    g.bar(X(s0), y, X(s1) - X(s0), RH - 12, P(s0), P(s1), col, hold=hold)
    if label:
        g.appear(g.text((X(s0) + X(s1)) / 2, y + 24, label, 14, lcol, g.MONO, 600, "middle"), P(s1) - 1, hold)


seg("cola", 0, 30, "#BFE6F4")
seg("cola", 30, 45, "#BFE6F4")
g.appear(g.text((X(0) + X(45)) / 2, ROWS["cola"] + 30, "espera con música", 14, g.INK, g.MONO, 600, "middle"), P(20), 100)
seg("1001", 0, 30, g.AMB, "suena 30 s")
g.appear(g.mark(X(30) + 22, ROWS["1001"] + RH / 2, False, 14) + g.text(X(30) + 44, ROWS["1001"] + 30, "no atiende", 15, g.BAD, g.SANS, 600), P(30), 100)
seg("1002", 30, 35, g.GREY)
g.appear(g.text(X(32.5), ROWS["1002"] - 8, "espera 5 s", 13, g.GREY, g.MONO, 600, "middle"), P(35) - 1, 100)
seg("1002", 35, 45, g.AMB, "suena")
seg("1002", 45, 80, g.OK, "atiende y habla")
seg("1002", 80, 90, g.GREY, "descansa")
g.appear(g.pillc(X(95), ROWS["1002"] + 10, "libre", g.OK, g.OKBG), P(90), 100)
g.appear(g.text(X(45) + 8, ROWS["cola"] + 30, "sale de la fila", 14, g.OK, g.MONO, 600), P(46), 100)

# cabezal
kf = [(0, X(0), 0)] + [(p, X(s), 0) for s, p in MAP] + [(100, X(100), 0)]
g.add(g.group(f'<line x1="0" y1="200" x2="0" y2="{AY}" stroke="{g.BLUE}" stroke-width="2.5"/>'
              f'<circle cx="0" cy="{AY}" r="6" fill="{g.BLUE}"/>', g.move(kf), still=0))

# valores
g.add(g.box(48, 530, 700, 104, g.WHITE, g.LINE, rx=14))
for k, (n, v) in enumerate([("Agent Ring Time", "30 s sonando"), ("Retry Time", "5 s y pasa al siguiente"), ("Agent Rest Time", "10 s después de cortar")]):
    y = 562 + k * 28
    g.add(g.text(68, y, n, 16, g.INK, g.MONO, 600) + g.text(300, y, v, 16, g.TXT, g.SANS))
g.add(g.note(770, 530, 382, "Y si se llena", ["Pasado Max Queue Length, o sin", "agentes, va al Failover Destination."], "amb"))

g.finish(8, 1, "Los tiempos de una cola, segundo a segundo",
         "Animación en cuatro tiempos con una línea de tiempo de 0 a 100 segundos y tres filas: la llamada en la cola, el agente 1001 y el agente 1002, con los valores de fábrica. "
         "1: entra una llamada, espera con música y suena el 1001 durante 30 segundos (Agent Ring Time); no atiende. "
         "2: la central espera 5 segundos (Retry Time) y prueba con el siguiente, el 1002, que suena y atiende a los 45 segundos; la llamada sale de la fila. "
         "3: el 1002 habla con quien llamó. "
         "4: al cortar, el 1002 descansa 10 segundos (Agent Rest Time) y recién después queda libre para otra llamada. "
         "Nota: pasado Max Queue Length, o si la cola queda sin agentes, la llamada va al Failover Destination.",
         [14, 40, 62, 86, 99])
