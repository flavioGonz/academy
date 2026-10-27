#!/usr/bin/env python3
"""Lección 6 · Teoría · El reseteo de apertura, minuto a minuto.
Sale de teoria_md (Cómo funciona): cada minuto el cron llama a schedule/tick, que calcula la hora de Uruguay (UTC-3),
busca los horarios activos con reseteo cuyo día coincide y cuya apertura es exactamente esa hora, pone en cero los
acumulados y graba un evento con valor 0 en Aforo, Entrada y Salida; guarda la hora del último reseteo para no disparar
dos veces en el mismo minuto; el aforo vuelve al valor real con el próximo evento de la cámara."""
from _anim_omni import new, out, when, check

a = new(26, "HORARIOS", "El reseteo de apertura, minuto a minuto")
a.steps([
    "07:59: el cron llama a schedule/tick. Ningún horario abre a esa hora.",
    "08:00: Apertura Caja 1 abre ahora y tiene reseteo: todo a cero.",
    "Otra llamada en el mismo minuto: ya reseteó a las 08:00, no repite.",
    "Llega el próximo evento de la cámara: el aforo vuelve a su valor real.",
], still=1)

# ---- línea de llamadas del cron
a.add(a.text(48, 200, "cron · cada minuto → schedule/tick", 16, a.INK, a.MONO, 600))
CALLS = [(120, "07:59", 2), (330, "08:00", 26), (540, "08:00 otra vez", 51)]
a.add(f'<line x1="60" y1="244" x2="760" y2="244" stroke="{a.LINE}" stroke-width="3"/>')
for x, lab, t in CALLS:
    when(a, f'<circle cx="{x}" cy="244" r="9" fill="{a.BLUE}"/>' + a.text(x, 276, lab, 16, a.INK, a.MONO, 600, "middle"), t, 100, still=1 if t < 50 else 0)
when(a, f'<circle cx="700" cy="244" r="9" fill="{a.AMB}"/>' + a.text(700, 276, "evento", 16, a.AMB, a.MONO, 600, "middle"), 76, 100, still=0)

# ---- lógica de schedule/tick
LX, LY, LW = 48, 304, 700
a.add(a.box(LX, LY, LW, 270, a.WHITE, a.LINE, rx=14))
a.add(a.text(LX + 20, LY + 32, "schedule/tick", 18, a.INK, a.SANS, 600))
a.add(a.text(LX + 20, LY + 64, "hora de Uruguay (UTC-3)", 15, a.GREY, a.MONO))
a.add(a.box(LX + 16, LY + 80, LW - 32, 58, a.SLATE, rx=10))
a.add(a.text(LX + 34, LY + 104, "Apertura Caja 1 · activo · con reseteo", 16, a.INK, a.SANS, 600))
a.add(a.text(LX + 34, LY + 128, "días L a S · apertura 08:00", 15, a.TXT, a.MONO))
ROWS = ["¿el día coincide?", "¿la apertura es esta hora?", "¿ya reseteó en este minuto?"]
for i, r in enumerate(ROWS):
    a.add(a.text(LX + 34, LY + 176 + i * 32, r, 16, a.TXT, a.SANS))
CK = LX + LW - 60


def marks(t0, t1, res, still=0):
    """res: lista de (texto, color) o None por fila."""
    s = ""
    for i, r in enumerate(res):
        if r is None:
            continue
        txt, col = r
        s += a.text(CK + 20, LY + 176 + i * 32, txt, 16, col, a.MONO, 600, "end")
    when(a, s, t0, t1, still=still)


SI, NO = ("sí", a.OK), ("no", a.BAD)
marks(4, 25, [SI, NO, None])
marks(28, 50, [SI, SI, ("no", a.GREY)], still=1)
marks(53, 75, [SI, SI, ("sí", a.AMB)])
PX = LX + LW - 16
when(a, a.pill(PX, LY + 16, "nada que hacer", a.GREY, a.SLATE, 15, 28, "end"), 6, 25, still=0)
when(a, a.pill(PX, LY + 16, "resetea · último reseteo 08:00", a.WHITE, a.BLUE, 15, 28, "end"), 30, 50, still=1)
when(a, a.pill(PX, LY + 16, "ya lo hizo: no repite", a.AMB, a.AMBBG, 15, 28, "end"), 55, 75, still=0)

# ---- canales
RX, RW = 790, 362
a.add(a.box(RX, 182, RW, 392, a.WHITE, a.LINE, rx=14))
a.add(a.text(RX + 20, 214, "Fila Caja 1", 18, a.INK, a.SANS, 600))


def chan(y, name, vals):
    a.add(a.box(RX + 16, y, RW - 32, 92, a.SLATE, rx=10))
    a.add(a.text(RX + 34, y + 54, name, 18, a.INK, a.SANS, 600))
    for t0, t1, v, col, still in vals:
        a.add(a.group(a.text(RX + RW - 36, y + 62, v, 38, col, a.HEAD, 600, "end"), a.show(t0, t1, 0.4), still=still))


chan(234, "Aforo", [(0, 30, "3", a.INK, 0), (30, 80, "0", a.BLUE, 1), (80, 100, "4", a.AMB, 0)])
chan(338, "Entrada", [(0, 30, "128", a.INK, 0), (30, 100, "0", a.BLUE, 1)])
chan(442, "Salida", [(0, 30, "125", a.INK, 0), (30, 100, "0", a.BLUE, 1)])
when(a, a.text(RX + 34, 552, "evento con valor 0 en los tres", 15, a.BLUE, a.MONO, 600), 30, 75, still=1)
when(a, a.text(RX + 34, 552, "la ocupación la mide la cámara", 15, a.AMB, a.MONO, 600), 80, 100, still=0)

a.add(a.text(48, 640, "Todo contador acumulado necesita un punto de partida: en OmniAccess, la apertura del día.", 16, a.TXT, a.SANS, 600))

out(a, 6, 1, "El reseteo de apertura, minuto a minuto",
    "Animación en cuatro tiempos. Arriba, las llamadas del cron a schedule/tick, una por minuto. Abajo a la izquierda, la lógica de schedule/tick con la hora de Uruguay (UTC-3) "
    "y el horario Apertura Caja 1, activo, con reseteo, de lunes a sábado con apertura a las 08:00, y tres preguntas: si el día coincide, si la apertura es esta hora y si ya reseteó en este minuto. "
    "A la derecha, los canales de la Fila Caja 1. "
    "Tiempo 1: a las 07:59 el día coincide pero la apertura no es esa hora: nada que hacer. Aforo 3, Entrada 128, Salida 125. "
    "Tiempo 2: a las 08:00 el día coincide, la apertura es esa hora y todavía no reseteó: pone en cero los acumulados, graba un evento con valor 0 en Aforo, Entrada y Salida y guarda la hora del último reseteo, 08:00. "
    "Tiempo 3: otra llamada en el mismo minuto encuentra que ya reseteó a las 08:00 y no repite. "
    "Tiempo 4: llega el próximo evento de la cámara y el Aforo vuelve a su valor real, 4, porque la ocupación la mide la cámara. "
    "Al pie: todo contador acumulado necesita un punto de partida; en OmniAccess, la apertura del día.",
    [12, 40, 62, 90])
