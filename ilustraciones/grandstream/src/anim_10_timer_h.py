#!/usr/bin/env python3
"""Lección 10 · teoría: ACK perdido, retransmisiones del 200 OK y corte por Timer H a los 32 s."""
from _anim_grandstream import G

g = G(T=26, fix=93, kicker="GRANDSTREAM · CORTE A LOS 32 SEGUNDOS", title="El ACK que no llega corta la llamada a los 32 s")
g.steps([
    "La UCM atiende con 200 OK. El otro lado manda ACK, pero un ALG lo rompe.",
    "Sin ACK, la UCM repite el 200 OK y sigue esperando.",
    "Mientras tanto la llamada anda: se habla sin problema.",
    "Timer H: 64 × T1 (500 ms) = 32 s sin ACK. La UCM corta.",
])

MAP = [(0, 3), (0.3, 25), (3.6, 50), (28, 75), (32, 88), (35, 97)]


def P(s):
    for (s0, p0), (s1, p1) in zip(MAP, MAP[1:]):
        if s0 <= s <= s1:
            return p0 + (p1 - p0) * (s - s0) / (s1 - s0)
    return MAP[-1][1]


# arriba: quién manda qué
LY = 238
g.add(g.node(48, 200, 240, 76, "Otro extremo", "atendido por la UCM"))
g.add(g.box(480, 200, 240, 76, g.WHITE, g.AMB, rx=14, sw=2) + g.text(600, 232, "Router", 20, g.INK, g.HEAD, 600, "middle")
      + g.text(600, 256, "SIP ALG activo", 15, g.AMB, g.MONO, 600, "middle"))
g.add(g.node(912, 200, 240, 76, "UCM", "manda el 200 OK", dark=True, tsize=22))
g.add(f'<line x1="288" y1="{LY}" x2="480" y2="{LY}" stroke="{g.LINE}" stroke-width="3"/><line x1="720" y1="{LY}" x2="912" y2="{LY}" stroke="{g.LINE}" stroke-width="3"/>')
TICKS = [0, 0.5, 1.5, 3.5, 7.5, 11.5, 15.5, 19.5, 23.5, 27.5, 31.5]
for s in TICKS:
    p = P(s)
    g.token([(912, LY), (288, LY)], p, p + 2.5, g.chip("200 OK", bg=g.OK, size=13, h=24), hold=p + 2.8)
    g.token([(288, LY), (480, LY)], p + 3, p + 4.2, g.chip("ACK", bg=g.BLUE, size=13, h=24), hold=p + 4.5)
g.appear(g.mark(456, LY - 34, False, 14) + g.text(600, 306, "el ACK no pasa", 15, g.BAD, g.SANS, 600, "middle"), 7, 100)

# abajo: línea de tiempo
X0, X1, SMAX = 200, 1120, 35
def X(s):
    return X0 + (X1 - X0) * s / SMAX


R = {"ok": 380, "ack": 440, "audio": 500}
for k, lab in [("ok", "200 OK"), ("ack", "ACK"), ("audio", "audio")]:
    g.add(g.text(48, R[k] + 6, lab, 16, g.INK, g.MONO, 600))
    g.add(f'<line x1="{X0}" y1="{R[k]}" x2="{X1}" y2="{R[k]}" stroke="{g.LINE}" stroke-width="2" stroke-dasharray="3 6"/>')
for s in TICKS:
    g.appear(f'<rect x="{X(s) - 3}" y="{R["ok"] - 16}" width="6" height="32" rx="3" fill="{g.OK}"/>', P(s), 100)
g.appear(g.text(X0 + 10, R["ack"] + 6, "nunca llega a la UCM", 15, g.BAD, g.MONO, 600), 8, 100)
for (s0, p0), (s1, p1) in zip(MAP[:4], MAP[1:5]):
    g.bar(X(s0), R["audio"] - 12, X(s1) - X(s0), 24, p0, p1, "#9FD9BE")
g.appear(g.text(X(14), R["audio"] + 6, "se habla", 15, g.OK, g.MONO, 600, "middle"), 52, 100)
# eje
AY = 548
g.add(f'<line x1="{X0}" y1="{AY}" x2="{X1}" y2="{AY}" stroke="{g.GREY}" stroke-width="1.5"/>')
for s in (0, 10, 20):
    g.add(f'<line x1="{X(s)}" y1="{AY}" x2="{X(s)}" y2="{AY + 8}" stroke="{g.GREY}" stroke-width="1.5"/>' + g.text(X(s), AY + 28, f"{s} s", 14, g.GREY, g.MONO, 400, "middle"))
g.add(f'<line x1="{X(32)}" y1="{R["ok"] - 30}" x2="{X(32)}" y2="{AY + 8}" stroke="{g.BAD}" stroke-width="2" stroke-dasharray="5 5"/>')
g.add(g.text(X(32), AY + 28, "32 s", 14, g.BAD, g.MONO, 600, "middle"))
g.appear(g.pillc(X(32) + 44, R["audio"] - 14, "corta", g.BAD, g.BADBG, 14, 28), 88, 100)
# cabezal
kf = [(p, X(s), 0) for s, p in MAP] + [(100, X(35), 0)]
kf = [(0, X(0), 0)] + kf
g.add(g.group(f'<line x1="0" y1="{R["ok"] - 30}" x2="0" y2="{AY}" stroke="{g.BLUE}" stroke-width="2"/>', g.move(kf), still=0))

g.add(g.note(48, 596, 1104, None, ["Corte fijo cerca del medio minuto: en la captura buscá el 200 OK repetido y el ACK que falta."], "amb"))

g.finish(10, 2, "El ACK que no llega corta la llamada a los 32 s",
         "Animación en cuatro tiempos. Arriba, el otro extremo, un router con SIP ALG activo y la UCM; abajo, una línea de tiempo de 0 a 35 segundos con tres filas: 200 OK, ACK y audio. "
         "1: la UCM atiende y manda 200 OK; el otro lado responde ACK, pero el ALG lo rompe y no pasa el router. "
         "2: sin ACK, la UCM repite el 200 OK y sigue esperando; cada ACK que vuelve se pierde igual. "
         "3: mientras tanto la llamada anda y se habla sin problema. "
         "4: a los 32 segundos, el Timer H, 64 veces T1 de 500 ms, vence sin ACK y la UCM corta la llamada. "
         "Nota: un corte fijo cerca del medio minuto se confirma en la captura buscando el 200 OK repetido y el ACK que falta.",
         [12, 38, 64, 93])
