#!/usr/bin/env python3
"""Lección 31 · Teoría · Por qué la tabla habla de carga resistiva: el arco al abrir.
Sale de teoria_md (Cómo funciona): al abrir con corriente se forma un arco; con carga resistiva es corto,
con carga inductiva la energía del campo se descarga ahí y el arco es mayor; el contacto se gasta o se pega;
protección: margen, diodo en electroimanes de continua (lección 4) o relé auxiliar."""
from _anim_akuvox_29_42 import new, out, when

a = new(24, "RELÉ DEL MONITOR · CARGAS", "Al abrir el contacto: arco chico o arco grande")
a.steps([
    "Contacto cerrado: la corriente circula por las dos cargas.",
    "El contacto abre: arco corto con la lámpara, arco mayor con el electroimán.",
    "Con el uso, el contacto de la carga inductiva se gasta más rápido o se pega.",
    "Protección: diodo en el electroimán de continua (lección 4) o relé auxiliar.",
], still=1)

RED, BLK, Y = "#D2492F", "#2B2B2B", "#E0A100"
CY = 340       # línea del contacto
BY = 470       # retorno


def spark(cx, cy, big):
    r = 40 if big else 14
    z = (f'M{cx - 4} {cy - 26} l10 12 l-10 6 l12 12 l-8 4 l10 14' if big else f'M{cx - 2} {cy - 10} l5 6 l-5 3 l6 7')
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#FFD28A" opacity=".75"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r * .55}" fill="#FFF1C9"/>'
            f'<path d="{z}" fill="none" stroke="{RED}" stroke-width="{3 if big else 2.5}" stroke-linejoin="round"/>')


def flash(t, dur=5):
    return a.keyframes([(0, 0), (t, 0), (t + .4, 1), (t + 1.5, .5), (t + 2.2, 1), (t + dur, 1), (t + dur + .6, 0), (100, 0)])


def panel(x0, title, sub, inductive):
    w = 540
    a.add(a.box(x0, 172, w, 330, a.WHITE, a.LINE, rx=18))
    a.add(a.text(x0 + 24, 210, title, 20, a.INK, a.HEAD, 600))
    a.add(a.text(x0 + 24, 234, sub, 15, a.GREY, a.MONO))
    px, fx = x0 + 120, x0 + 230          # pivote y contacto fijo
    # circuito
    a.add(a.pill(x0 + 24, CY - 14, "+12 V", RED, a.BADBG, 15, 28))
    a.add(f'<path d="M{x0 + 104} {CY} H{px}" stroke="{RED}" stroke-width="4"/>')
    a.add(f'<path d="M{fx + 10} {CY} H{x0 + 330}" stroke="{a.CYAN}" stroke-width="4"/>')
    lx = x0 + 380
    if not inductive:
        a.add(f'<circle cx="{lx}" cy="{CY}" r="28" fill="{a.WHITE}" stroke="{a.INK}" stroke-width="3"/>'
              f'<path d="M{lx - 19} {CY - 19} L{lx + 19} {CY + 19} M{lx + 19} {CY - 19} L{lx - 19} {CY + 19}" stroke="{a.INK}" stroke-width="3"/>')
        a.add(a.text(lx, CY + 54, "lámpara", 15, a.INK, a.MONO, 600, "middle"))
        a.add(f'<path d="M{x0 + 330} {CY} H{lx - 28} M{lx + 28} {CY} H{x0 + 470} V{BY} H{x0 + 104}" fill="none" stroke="{a.CYAN}" stroke-width="4"/>')
    else:
        a.add(f'<rect x="{lx - 40}" y="{CY - 26}" width="80" height="52" rx="8" fill="{a.SLATE}" stroke="{a.INK}" stroke-width="2.5"/>')
        a.add("".join(f'<path d="M{lx - 30 + k * 12} {CY + 14} q6 -30 12 0" fill="none" stroke="#B26A00" stroke-width="3"/>' for k in range(5)))
        a.add(a.text(lx, CY + 54, "electroimán", 15, a.INK, a.MONO, 600, "middle"))
        a.add(f'<path d="M{x0 + 330} {CY} H{lx - 40} M{lx + 40} {CY} H{x0 + 470} V{BY} H{x0 + 104}" fill="none" stroke="{a.CYAN}" stroke-width="4"/>')
    a.add(f'<path d="M{x0 + 104} {BY} H{x0 + 92}" stroke="{BLK}" stroke-width="4"/>')
    a.add(a.pill(x0 + 24, BY - 14, "−", BLK, "#E6EDF4", 16, 28))
    # contacto: pivote + pastilla fija
    a.add(f'<rect x="{fx - 6}" y="{CY - 4}" width="16" height="22" rx="3" fill="{Y}" stroke="{a.INK}" stroke-width="2"/>')
    a.add(f'<circle cx="{px}" cy="{CY}" r="8" fill="{a.WHITE}" stroke="{a.INK}" stroke-width="3"/>')
    a.add(a.text((px + fx) / 2, CY + 46, "contacto del relé", 15, a.GREY, a.MONO, 600, "middle"))
    closed = f'<line x1="{px}" y1="{CY}" x2="{fx - 6}" y2="{CY - 4}" stroke="{a.INK}" stroke-width="7" stroke-linecap="round"/>'
    opened = f'<line x1="{px}" y1="{CY}" x2="{fx - 14}" y2="{CY - 44}" stroke="{a.INK}" stroke-width="7" stroke-linecap="round"/>'
    # cerrado en 0-26 y 75-81; abierto el resto
    a.add(a.group(closed, a.keyframes([(0, 1), (26, 1), (26.3, 0), (75, 0), (75.3, 1), (81, 1), (81.3, 0), (100, 0)]), still=0))
    a.add(a.group(opened, a.keyframes([(0, 0), (26, 0), (26.3, 1), (75, 1), (75.3, 0), (81, 0), (81.3, 1), (100, 1)]), still=1))
    # corriente (flechas) mientras está cerrado
    cur = "".join(a.arrow(f"M{x} {BY - 22} h-34", a.CYAN, 3) for x in (x0 + 300, x0 + 420))
    when(a, cur + a.text(x0 + 290, BY - 32, "corriente", 15, a.CYAN, a.MONO, 600, "middle"), 0, 26, still=0)
    when(a, cur + a.text(x0 + 290, BY - 32, "corriente", 15, a.CYAN, a.MONO, 600, "middle"), 75.3, 81, still=0)
    # arco al abrir (t2)
    sx, sy = fx - 10, CY - 22
    a.add(a.group(spark(sx, sy, inductive), flash(26.3), still=1))
    return px, fx, sx, sy


panel(48, "Carga resistiva", "lámpara · no genera picos", False)
px, fx, sx, sy = panel(612, "Carga inductiva", "bobina, motor, electroimán", True)

# etiquetas del arco
when(a, a.pill(48 + 270, 252, "arco corto", a.OK, a.OKBG, 15, 28), 27, 50, still=1)
when(a, a.pill(612 + 266, 252, "arco mayor", a.BAD, a.BADBG, 15, 28), 27, 50, still=1)
# t3: desgaste
pits = "".join(f'<circle cx="{fx - 2 + dx}" cy="{CY + dy}" r="3" fill="{BLK}"/>' for dx, dy in ((-2, 2), (3, 8), (0, 13), (4, -1)))
when(a, pits + a.pill(612 + 266, 252, "se gasta o se pega", a.BAD, a.BADBG, 15, 28), 51, 75)
when(a, a.pill(48 + 270, 252, "contacto sano", a.OK, a.OKBG, 15, 28), 51, 75)
# t4: diodo en paralelo con el electroimán + arco chico
lx = 612 + 380
diode = (f'<path d="M{lx - 52} {CY} V{CY - 64} H{lx - 14}" fill="none" stroke="{a.OK}" stroke-width="3"/>'
         f'<path d="M{lx + 52} {CY} V{CY - 64} H{lx + 14}" fill="none" stroke="{a.OK}" stroke-width="3"/>'
         f'<path d="M{lx + 12} {CY - 78} L{lx - 12} {CY - 64} L{lx + 12} {CY - 50} Z" fill="{a.OK}"/>'
         f'<line x1="{lx - 13}" y1="{CY - 78}" x2="{lx - 13}" y2="{CY - 50}" stroke="{a.OK}" stroke-width="3"/>'
         + a.pill(lx + 64, CY - 78, "diodo", a.OK, a.OKBG, 15, 28))
when(a, diode, 76, 100)
for xx in (sx, 48 + 220):
    a.add(a.group(f'<circle cx="{xx}" cy="{sy}" r="14" fill="#FFD28A" opacity=".75"/>', flash(81.3, 4), still=0))
when(a, a.pill(612 + 24, 252, "arco chico otra vez", a.OK, a.OKBG, 15, 28), 82, 100)

a.add(a.text(48, 548, "La tabla de Akuvox da un techo pensado para carga resistiva.", 18, a.INK, a.SANS, 600))
a.add(a.text(48, 576, "C319: 24 V 1 A · C313: 30 V 2 A. El tamaño de la pantalla no dice nada del relé.", 17, a.TXT, a.SANS, 600))
a.add(a.text(48, 604, "Con carga inductiva: margen y protección. Si pasa el valor, el relé del monitor", 17, a.TXT, a.SANS, 600))
a.add(a.text(48, 628, "solo maneja la bobina de un relé auxiliar.", 17, a.TXT, a.SANS, 600))

out(a, 31, 1, "Al abrir el contacto: arco chico o arco grande",
    "Animación con dos circuitos iguales, uno con una lámpara (carga resistiva) y otro con un electroimán (carga inductiva), cada uno manejado por un contacto de relé. "
    "Tiempo 1: los contactos están cerrados y la corriente circula por las dos cargas. "
    "Tiempo 2: los contactos abren; con la lámpara aparece un arco corto, con el electroimán un arco mayor porque se descarga la energía del campo magnético. "
    "Tiempo 3: con el uso, el contacto de la carga inductiva se gasta más rápido o se pega, mientras el de la lámpara sigue sano. "
    "Tiempo 4: con un diodo en paralelo con el electroimán de continua, el arco vuelve a ser chico; la otra opción es un relé auxiliar. "
    "Abajo: la tabla de Akuvox es un techo para carga resistiva, por ejemplo C319 24 V 1 A y C313 30 V 2 A.",
    [12, 30, 62, 90])
