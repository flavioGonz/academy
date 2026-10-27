#!/usr/bin/env python3
"""Lección 7 · teoría: el IVR como máquina de estados (bienvenida, espera, decide; Timeout e Invalid)."""
from _anim_grandstream import G

g = G(T=30, fix=36, kicker="GRANDSTREAM · IVR", title="El IVR espera, decide y nunca deja a nadie colgado")
g.steps([
    "Entra la llamada al IVR 7000: suena el prompt y la central espera una tecla.",
    "Tecla 1 en horario de oficina: la condición manda a Ring Group ventas.",
    "La misma tecla 1 fuera de horario: va al buzón de la 1001.",
    "No marca nada: espera 10 s, repite 3 veces y va al destino de Timeout.",
    "Marca una tecla sin evento: va al destino de Invalid.",
])

# estados
g.add(g.node(48, 186, 250, 64, "Bienvenida", "prompt del IVR 7000"))
g.add(g.box(48, 290, 250, 104, g.WHITE, g.LINE, rx=14))
g.add(g.text(173, 322, "Espera una tecla", 20, g.INK, g.HEAD, 600, "middle"))
g.add(g.text(173, 346, "Response Timeout 10 s", 15, g.GREY, g.MONO, 400, "middle"))
g.add(g.box(390, 290, 190, 104, g.INK, None, rx=14))
g.add(g.text(485, 334, "Decide", 20, g.WHITE, g.HEAD, 600, "middle"))
g.add(g.text(485, 358, "evento + horario", 15, "#9FC3E3", g.MONO, 400, "middle"))
g.add(g.parrow("M173 250 V284", g.GREY, 2.5))
g.add(g.parrow("M298 342 H384", g.GREY, 2.5))

DX, DW = 690, 462
dests = [("Ring Group ventas", "tecla 1 · Office Time"), ("Voicemail 1001", "tecla 1 · Out of Office Time"),
         ("Extension 1002", "tecla 2 · All Time"), ("Ring Group recepción", "destino de Timeout e Invalid")]
DY = [186, 268, 350, 432]
for (t, sub), y in zip(dests, DY):
    g.add(g.box(DX, y, DW, 64, g.WHITE, g.LINE, rx=14))
    g.add(g.text(DX + 20, y + 28, t, 18, g.INK, g.HEAD, 600))
    g.add(g.text(DX + 20, y + 50, sub, 14, g.GREY, g.MONO))
    g.add(f'<path d="M580 342 H630 V{y + 32} H{DX}" fill="none" stroke="{g.LINE}" stroke-width="2"/>')


def route(i, t0, t1, hold, col):
    y = DY[i] + 32
    g.arrow([(580, 342), (630, 342), (630, y), (DX - 4, y)], t0, t1, col, hold=hold)
    g.appear(g.box(DX, DY[i], DW, 64, "none", col, rx=14, sw=3), t1, hold)


def ride(pts, t0, t1, hold=None):
    g.token(pts, t0, t1, g.chip("llamada", bg=g.CYAN, size=13, h=24), hold=hold)


# 1: bienvenida
def hl(x, y, w, h, t0, t1, col=None, dark=False):
    g.appear(g.box(x - 4, y - 4, w + 8, h + 8, "none", col or g.CYAN, rx=17, sw=3), t0, t1)

hl(48, 186, 250, 64, 2, 10)
g.appear(g.pillc(410, 206, "suena el prompt", g.BLUE, g.WHITE, 13, 24), 3, 10)
hl(48, 290, 250, 104, 10, 20)
# 2: tecla 1 en horario
hl(390, 290, 190, 104, 24, 31)
route(0, 28, 31, 40, g.OK)
# 3: tecla 1 fuera de horario
hl(390, 290, 190, 104, 44, 51)
route(1, 48, 51, 60, g.AMB)
# 4: timeout, tres vueltas
for k, (a, b) in enumerate([(61, 65), (65.5, 69.5), (70, 74)]):
    g.add(g.box(68, 362, 210, 14, g.SLATE, None, rx=7)) if k == 0 else None
    g.bar(68, 362, 210, 14, a, b, g.AMB, hold=b + 0.3)
    g.appear(g.text(173, 412, f"repite el prompt {k + 1} de 3", 14, g.AMB, g.MONO, 600, "middle"), a, b + 0.3)
hl(390, 290, 190, 104, 74.5, 79.5)
route(3, 77, 79.5, 80, g.BLUE)
g.appear(g.pillc(DX + DW - 80, DY[3] + 18, "Timeout", g.BLUE, g.WHITE, 13, 24), 79, 80)
# 5: inválida
hl(390, 290, 190, 104, 84, 91)
route(3, 88, 91, 100, g.BLUE)
g.appear(g.pillc(DX + DW - 80, DY[3] + 18, "Invalid", g.BLUE, g.WHITE, 13, 24), 91, 100)

# panel inferior: qué marca quien llama y la hora
g.add(g.box(48, 524, 532, 108, g.WHITE, g.LINE, rx=14))
g.add(g.text(68, 556, "Quien llama marca", 16, g.GREY, g.SANS, 600))
g.add(g.text(68, 610, "Hora de la UCM", 16, g.GREY, g.SANS, 600))
for a, b, s, col in [(0, 20, "todavía nada", g.GREY), (21, 40, "1", g.INK), (41, 60, "1", g.INK), (60, 80, "nada", g.AMB), (81, 100, "9 · no tiene evento", g.BAD)]:
    g.appear(g.text(260, 557, s, 20 if len(s) < 3 else 17, col, g.MONO, 600), a, b)
g.appear(g.pillc(330, 592, "en horario", g.OK, g.OKBG), 0, 40)
g.appear(g.pillc(330, 592, "fuera de horario", g.AMB, g.AMBBG), 40, 60)
g.appear(g.pillc(330, 592, "no se evalúa", g.GREY, g.SLATE), 60, 100)
g.add(g.note(600, 524, 552, "Sin destino, corta", ["Si Timeout o Invalid quedan vacíos, al terminar", "las repeticiones la central cuelga."], "bad"))

g.finish(7, 1, "El IVR espera, decide y nunca deja a nadie colgado",
         "Animación en cinco tiempos del IVR 7000 como máquina de estados: bienvenida, espera de una tecla con Response Timeout de 10 segundos y decisión por evento y horario, con cuatro destinos a la derecha. "
         "1: entra la llamada, suena el prompt y la central espera una tecla. "
         "2: quien llama marca 1 en horario de oficina y la condición Office Time manda la llamada a Ring Group ventas. "
         "3: marca la misma tecla 1 fuera de horario y la llamada va al buzón de la 1001 (Voicemail 1001). "
         "4: no marca nada; la central espera 10 segundos, repite el prompt 3 veces y manda la llamada al destino de Timeout, Ring Group recepción. "
         "5: marca 9, una tecla sin evento, y la llamada va al destino de Invalid, también Ring Group recepción. "
         "La tecla 2 va siempre a la Extension 1002. Nota: si Timeout o Invalid quedan vacíos, al terminar las repeticiones la central cuelga.",
         [8, 33, 55, 68, 94])
