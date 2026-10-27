#!/usr/bin/env python3
"""Lección 2 · Teoría · Tres tareas sobre el mismo polígono.
Sale de teoria_md (Cómo funciona): la tarea de ocupación mira un polígono (hasta 16 puntos) y cuenta cuántos objetos hay
adentro en cada momento; las tareas de entrada y salida de campo disparan un evento cada vez que un objeto cruza el borde
hacia adentro o hacia afuera; OmniAccess lee la ocupación como un número que sube y baja y convierte cada entrada o salida
en un acumulado propio (canales Entrada y Salida). Escribir una configuración IVA nueva reinicia los contadores."""
from _anim_omni import new, out, when, travel

a = new(24, "LA CÁMARA CUENTA", "Ocupación, entrada y salida sobre el mismo polígono")
a.steps([
    "Ocupación: la cámara cuenta cuántos hay dentro del polígono ahora.",
    "Alguien cruza el borde hacia adentro: evento de entrada. Entrada suma 1.",
    "Alguien sale por el borde: evento de salida. Salida suma 1 y el aforo baja.",
], still=1)


def top(c):  # persona vista desde arriba
    return (f'<circle cx="0" cy="0" r="17" fill="{c}" fill-opacity=".25" stroke="{c}" stroke-width="2.5"/>'
            f'<circle cx="0" cy="0" r="8" fill="{c}"/>')


FX, FY, FW, FH = 48, 182, 680, 400
a.add(a.box(FX, FY, FW, FH, "#E9EEF3", a.LINE, rx=10))
a.add(a.text(FX + 16, FY + 28, "vista cenital", 15, a.GREY, a.MONO, 600))
a.add(a.box(FX + 470, FY + 40, 180, 50, "#C9D6E3", rx=8) + a.text(FX + 560, FY + 72, "caja", 16, a.INK, a.MONO, 600, "middle"))
poly = [(FX + 140, FY + 120), (FX + 620, FY + 120), (FX + 620, FY + 330), (FX + 140, FY + 330)]
d = "M" + " L".join(f"{x} {y}" for x, y in poly) + " z"
a.add(f'<path d="{d}" fill="{a.CYAN}" fill-opacity=".10" stroke="{a.CYAN}" stroke-width="3" stroke-dasharray="10 7"/>')
a.add("".join(f'<circle cx="{x}" cy="{y}" r="6" fill="{a.CYAN}"/>' for x, y in poly))
a.add(a.text(FX + 150, FY + 352, "zona de la fila · polígono de hasta 16 puntos", 15, a.BLUE, a.MONO, 600))

# tres personas en la fila (quietas)
for x in (FX + 300, FX + 400, FX + 500):
    a.add(f'<g transform="translate({x} {FY + 225})">{top(a.BLUE)}</g>')
# entra una por la izquierda (tiempo 2) y queda
inn = [(0, FX + 40, FY + 225), (36, FX + 40, FY + 225), (46, FX + 200, FY + 225), (100, FX + 200, FY + 225)]
a.add(a.group(top(a.OK), a.move(inn), a.show(34, 100, 0.8), still=0))
a.add(a.group(f'<g transform="translate({FX + 200} {FY + 225})">{top(a.OK)}</g>', a.keyframes([(0, 0), (100, 0)]), still=1))
# sale una por arriba hacia la caja (tiempo 3)
outp = [(0, FX + 560, FY + 225), (68, FX + 560, FY + 225), (78, FX + 560, FY + 100), (100, FX + 560, FY + 100)]
a.add(a.group(top(a.AMB), a.move(outp), a.show(0, 100), still=0))
a.add(a.group(f'<g transform="translate({FX + 560} {FY + 225})">{top(a.AMB)}</g>', a.keyframes([(0, 0), (100, 0)]), still=1))
# marcas de cruce
when(a, a.pill(FX + 140, FY + 160, "entra", a.WHITE, a.OK, 15, 28, "middle"), 41, 66, still=1)
when(a, a.pill(FX + 560, FY + 132, "sale", a.WHITE, a.AMB, 15, 28, "middle"), 73, 100, still=0)
# ocupación en el tiempo 1
when(a, f'<rect x="{FX + 136}" y="{FY + 116}" width="488" height="218" rx="8" fill="none" stroke="{a.BLUE}" stroke-width="4"/>'
     + a.pill(FX + 380, FY + 290, "4 adentro", a.WHITE, a.BLUE, 16, 30, "middle"), 4, 32, still=0)

# ---- canales en OmniAccess
RX, RW = 760, 392
a.add(a.box(RX, FY, RW, FH, a.WHITE, a.LINE, rx=14))
a.add(a.text(RX + 20, FY + 34, "Canales en OmniAccess", 18, a.INK, a.SANS, 600))


def counter(y, name, sub, vals, color):
    """vals: [(desde%, hasta%, texto)]"""
    a.add(a.box(RX + 16, y, RW - 32, 96, a.SLATE, rx=10))
    a.add(a.text(RX + 34, y + 36, name, 18, a.INK, a.SANS, 600))
    a.add(a.text(RX + 34, y + 66, sub, 15, a.GREY, a.MONO))
    for t0, t1, v, still in vals:
        a.add(a.group(a.text(RX + RW - 40, y + 62, v, 40, color, a.HEAD, 600, "end"), a.show(t0, t1, 0.4), still=still))


counter(FY + 54, "Aforo", "ocupación: sube y baja", [(0, 45, "4", 0), (45, 77, "5", 1), (77, 100, "4", 0)], a.BLUE)
counter(FY + 164, "Entrada", "acumulado propio", [(0, 45, "0", 0), (45, 100, "1", 1)], a.OK)
counter(FY + 274, "Salida", "acumulado propio", [(0, 77, "0", 1), (77, 100, "1", 0)], a.AMB)
when(a, a.pill(RX + RW - 72, FY + 196, "+1", a.WHITE, a.OK, 15, 28, "end"), 45, 60, still=1)
when(a, a.pill(RX + RW - 72, FY + 306, "+1", a.WHITE, a.AMB, 15, 28, "end"), 77, 92, still=0)

a.add(a.text(48, 618, "Escribir una configuración IVA nueva reinicia los contadores de la cámara: los cambios grandes, con el local cerrado.", 16, a.TXT, a.SANS, 600))
a.add(a.text(48, 644, "La precisión depende sobre todo de la geometría: altura, ángulo, reflejos y espacio antes y después del borde.", 16, a.TXT, a.SANS, 600))

out(a, 2, 1, "Ocupación, entrada y salida",
    "Animación en tres tiempos. A la izquierda, una vista cenital con la caja arriba y la zona de la fila como polígono punteado de hasta 16 puntos; "
    "a la derecha, los canales de OmniAccess: Aforo (ocupación, sube y baja), Entrada y Salida (acumulados propios). "
    "Tiempo 1: hay cuatro personas dentro del polígono; la tarea de ocupación cuenta 4 y Aforo marca 4, Entrada 0 y Salida 0. "
    "Tiempo 2: una persona cruza el borde hacia adentro; es un evento de entrada, Entrada suma 1 y el Aforo pasa a 5. "
    "Tiempo 3: una persona sale por el borde hacia la caja; es un evento de salida, Salida suma 1 y el Aforo vuelve a 4. "
    "Al pie: escribir una configuración IVA nueva reinicia los contadores de la cámara, y la precisión depende sobre todo de la geometría.",
    [15, 55, 92])
