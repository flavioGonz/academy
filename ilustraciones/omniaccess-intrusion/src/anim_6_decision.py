#!/usr/bin/env python3
"""Lección 6 · Teoría · Pendiente, decisión por cámara y En atención.
Sale de teoria_md (Cómo funciona): cada detección nace pendiente (acknowledged = false); las pendientes de las últimas
6 horas se reconstruyen al recargar; la decisión marca todas las pendientes de esa cámara en esa ventana como reales o
falsas y guarda la hora de la decisión (sirve para medir el tiempo de reacción); si es real, la cámara entra en la lista
"en atención" hasta que alguien la resuelve."""
from _anim_omni import new, out, when, card

a = new(24, "ATENDER", "Una decisión por cámara, con hora")
a.steps([
    "Cada detección nace pendiente: acknowledged = false.",
    "Recargás la página: las pendientes de las últimas 6 horas vuelven.",
    "Confirmás real: se marcan todas las pendientes de la cámara y se guarda la hora.",
    "La cámara queda En atención hasta que alguien la resuelve.",
], still=2)

LX, LY, LW = 48, 182, 620
a.add(a.box(LX, LY, LW, 380, a.WHITE, a.LINE, rx=14))
a.add(a.text(LX + 20, LY + 34, "Monitor Intrusión · Perímetro Norte 12", 18, a.INK, a.SANS, 600))
a.add(a.text(LX + 20, LY + 62, "detecciones de la cámara", 15, a.GREY, a.MONO))
HORAS = ["02:11:40", "02:12:05", "02:12:30"]
RY0, RH = LY + 82, 52
# filas: visibles salvo durante la recarga
rows_on = a.keyframes([(0, 0), (1, 0), (2.5, 1), (26, 1), (27, 0), (33, 0), (35, 1), (100, 1)])
rows = ""
for i, h in enumerate(HORAS):
    y = RY0 + i * RH
    rows += a.box(LX + 16, y, LW - 32, RH - 10, a.SLATE, rx=8)
    rows += a.text(LX + 34, y + 27, h, 16, a.INK, a.MONO, 600) + a.text(LX + 150, y + 27, "Cruce de línea", 16, a.TXT, a.SANS, 600)
a.add(a.group(rows, rows_on, still=1))
for i in range(3):
    y = RY0 + i * RH + 7
    pend = a.pill(LX + LW - 32, y, "pendiente", a.AMB, a.AMBBG, 15, 28, "end")
    real = a.pill(LX + LW - 32, y, "real", a.WHITE, a.BAD, 15, 28, "end")
    a.add(a.group(pend, a.keyframes([(0, 0), (1, 0), (2.5, 1), (26, 1), (27, 0), (33, 0), (35, 1), (55, 1), (56, 0), (100, 0)]), still=0))
    a.add(a.group(real, a.keyframes([(0, 0), (55, 0), (56, 1), (99, 1), (100, 0)]), still=1))

# recarga
when(a, a.box(LX + 16, RY0, LW - 32, 3 * RH - 10, "#F3F6F9", rx=8)
     + f'<path d="M{LX + 300} {RY0 + 56} a22 22 0 1 1 -6 15" fill="none" stroke="{a.BLUE}" stroke-width="4" stroke-linecap="round"/>'
     + f'<path d="M{LX + 286} {RY0 + 66} l8 8 l6 -11" fill="none" stroke="{a.BLUE}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>'
     + a.text(LX + 290, RY0 + 120, "recargando…", 16, a.BLUE, a.MONO, 600, "middle"), 27, 34, still=0)
when(a, a.pill(LX + 20, RY0 + 3 * RH + 4, "vuelven las pendientes de las últimas 6 h", a.BLUE, a.WHITE, 15, 30), 35, 50, still=0)

# botones
BY = LY + 300
a.add(a.box(LX + 20, BY, 200, 44, a.WHITE, a.BAD, rx=10) + a.text(LX + 120, BY + 28, "Confirmar real", 16, a.BAD, a.SANS, 600, "middle"))
a.add(a.box(LX + 236, BY, 180, 44, a.WHITE, a.LINE, rx=10) + a.text(LX + 326, BY + 28, "Falsa alarma", 16, a.TXT, a.SANS, 600, "middle"))
when(a, a.box(LX + 20, BY, 200, 44, a.BAD, rx=10) + a.text(LX + 120, BY + 28, "Confirmar real", 16, a.WHITE, a.SANS, 600, "middle"), 52, 58, still=0)
when(a, a.text(LX + 440, BY + 28, "vale para las 3", 15, a.BAD, a.MONO, 600), 55, 100, still=1)

# ---- derecha: hora de la decisión y tiempo de reacción
RX, RW = 700, 452
when(a, a.box(RX, LY, RW, 176, a.WHITE, a.LINE, rx=14)
     + a.text(RX + 20, LY + 34, "se guarda la hora de la decisión", 17, a.INK, a.SANS, 600)
     + a.text(RX + 20, LY + 72, "detección", 15, a.GREY, a.MONO) + a.text(RX + 200, LY + 72, "02:11:40", 16, a.INK, a.MONO, 600)
     + a.text(RX + 20, LY + 102, "decisión", 15, a.GREY, a.MONO) + a.text(RX + 200, LY + 102, "02:14:10", 16, a.BAD, a.MONO, 600)
     + f'<line x1="{RX + 20}" y1="{LY + 118}" x2="{RX + RW - 20}" y2="{LY + 118}" stroke="{a.LINE}" stroke-width="2"/>'
     + a.text(RX + 20, LY + 150, "tiempo de reacción", 15, a.GREY, a.MONO) + a.text(RX + 200, LY + 150, "2 min 30 s", 18, a.INK, a.MONO, 600), 57, 100, still=1)

# ---- En atención
EY = LY + 200
a.add(a.box(RX, EY, RW, 180, a.WHITE, a.LINE, rx=14))
a.add(a.text(RX + 20, EY + 34, "En atención", 18, a.AMB, a.SANS, 600))
a.add(a.text(RX + 20, EY + 62, "reales sin resolver", 15, a.GREY, a.MONO))
when(a, a.box(RX + 16, EY + 80, RW - 32, 44, a.AMBBG, rx=8) + a.text(RX + 34, EY + 108, "Perímetro Norte 12", 16, a.INK, a.SANS, 600)
     + a.box(RX + RW - 142, EY + 86, 112, 32, a.WHITE, a.OK, rx=8) + a.text(RX + RW - 86, EY + 108, "Resolver", 15, a.OK, a.SANS, 600, "middle"), 60, 88, still=1)
when(a, a.box(RX + RW - 142, EY + 86, 112, 32, a.OK, rx=8) + a.text(RX + RW - 86, EY + 108, "Resolver", 15, a.WHITE, a.SANS, 600, "middle"), 84, 88, still=0)
when(a, a.text(RX + 20, EY + 108, "vacía", 16, a.GREY, a.SANS, 600), 0, 59, still=0)
when(a, a.pill(RX + 20, EY + 88, "Perímetro Norte 12 · resuelta", a.OK, a.OKBG, 15, 30), 89, 100, still=0)
a.add(a.text(RX + 20, EY + 156, "Era falsa alarma: además corrige el registro.", 15, a.TXT, a.SANS))

a.add(a.text(48, 640, "Cerrar el navegador no pierde la alarma: lo pendiente está guardado en la base, no en la pantalla.", 16, a.TXT, a.SANS, 600))

out(a, 6, 1, "Una decisión por cámara, con hora",
    "Animación en cuatro tiempos. A la izquierda, el Monitor Intrusión de la cámara Perímetro Norte 12 con tres cruces de línea a las 02:11:40, 02:12:05 y 02:12:30, y los botones Confirmar real y Falsa alarma. "
    "Tiempo 1: cada detección nace pendiente, con acknowledged igual a false. "
    "Tiempo 2: la página se recarga, la lista se vacía un instante y vuelven las pendientes de las últimas 6 horas. "
    "Tiempo 3: se toca Confirmar real y las tres pasan a real; a la derecha se guarda la hora de la decisión, 02:14:10, y con la detección de las 02:11:40 da un tiempo de reacción de 2 min 30 s. "
    "Tiempo 4: la cámara aparece en la lista En atención; al tocar Resolver sale de la lista y queda resuelta. Era falsa alarma, además, corrige el registro. "
    "Al pie: cerrar el navegador no pierde la alarma, porque lo pendiente está guardado en la base.",
    [12, 31, 42, 66, 95])
