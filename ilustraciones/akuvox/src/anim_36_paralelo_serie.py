#!/usr/bin/env python3
"""Lección 36 · Teoría (2) · El cableado define el resultado: paralelo o serie.
Sale de teoria_md (Cómo funciona): en paralelo con el botón, el relé lo aprieta por el usuario y el ascensor va
directo; en serie con el común o la línea de autorización, el relé habilita la botonera y el usuario elige entre
los pisos liberados."""
from _anim_akuvox_29_42 import new, out, when

a = new(24, "ASCENSOR EC33 · CABLEADO", "Paralelo o serie: el mismo relé, otro resultado")
a.steps([
    "Paralelo: el usuario pasa la tarjeta y el relé del piso 3 cierra.",
    "Es como apretar el botón: el ascensor va directo al piso 3.",
    "Serie: el relé habilita la botonera solo en los pisos liberados.",
    "El usuario elige entre los liberados y aprieta el 3: el ascensor va.",
], still=1)

FLOORS = ["4", "3", "2", "1", "PB"]
FH = 58


def contact(x, y, label, closed_t=None, still_closed=0):
    """contacto horizontal de x a x+90 en y; cerrado entre closed_t."""
    out_ = [f'<circle cx="{x}" cy="{y}" r="6" fill="{a.WHITE}" stroke="{a.CYAN}" stroke-width="3"/>',
            f'<circle cx="{x + 90}" cy="{y}" r="6" fill="{a.WHITE}" stroke="{a.CYAN}" stroke-width="3"/>',
            a.text(x + 45, y + 30, label, 15, a.INK, a.MONO, 600, "middle")]
    a.add("".join(out_))
    opened = f'<line x1="{x + 6}" y1="{y}" x2="{x + 82}" y2="{y - 26}" stroke="{a.CYAN}" stroke-width="4" stroke-linecap="round"/>'
    closed = f'<line x1="{x + 6}" y1="{y}" x2="{x + 84}" y2="{y}" stroke="{a.OK}" stroke-width="4" stroke-linecap="round"/>'
    if closed_t:
        t0, t1 = closed_t
        a.add(a.group(opened, a.keyframes([(0, 1), (t0, 1), (t0 + .3, 0), (t1, 0), (t1 + .3, 1), (100, 1)]), still=1 - still_closed))
        a.add(a.group(closed, a.keyframes([(0, 0), (t0, 0), (t0 + .3, 1), (t1, 1), (t1 + .3, 0), (100, 0)]), still=still_closed))
    else:
        a.add(opened)


def shaft(x, y0, move_t, still_floor):
    a.add(a.box(x, y0, 74, FH * 5, a.SLATE, a.LINE, rx=8))
    for i, f in enumerate(FLOORS):
        y = y0 + i * FH
        if i:
            a.add(f'<line x1="{x}" y1="{y}" x2="{x + 74}" y2="{y}" stroke="{a.LINE}" stroke-width="2"/>')
        a.add(a.text(x + 88, y + 36, f, 15, a.GREY, a.MONO, 600))
    yPB, y3 = y0 + 4 * FH + 6, y0 + 1 * FH + 6
    t0, t1, t2 = move_t
    mv = a.move([(0, 0, yPB), (t0, 0, yPB), (t1, 0, y3), (t2, 0, y3), (t2 + .5, 0, yPB), (100, 0, yPB)])
    cab = f'<rect x="{x + 10}" y="0" width="54" height="{FH - 12}" rx="6" fill="{a.BLUE}"/><rect x="{x + 18}" y="8" width="38" height="{FH - 28}" rx="3" fill="#9FC3E3"/>'
    a.add(a.group(cab, mv, a.show(0, 100), still=0 if still_floor == "3" else 1))
    if still_floor == "3":   # cuadro fijo: cabina en el 3 (se dibuja oculta salvo en movimiento reducido)
        a.css.append("@media (prefers-reduced-motion:reduce){.fix3{opacity:1!important}}")
        a.add(f'<g class="fix3" style="opacity:0"><rect x="{x + 10}" y="{y3}" width="54" height="{FH - 12}" rx="6" fill="{a.BLUE}"/><rect x="{x + 18}" y="{y3 + 8}" width="38" height="{FH - 28}" rx="3" fill="#9FC3E3"/></g>')


# ---------- paralelo
L = 48
a.add(a.box(L, 172, 540, 420, a.WHITE, a.LINE, rx=18))
a.add(a.text(L + 24, 206, "Paralelo · directo al piso", 20, a.INK, a.HEAD, 600))
# dos ramas en paralelo
a.add(f'<path d="M{L + 40} 300 V420 M{L + 40} 300 H{L + 90} M{L + 40} 420 H{L + 90} M{L + 186} 300 H{L + 236} M{L + 186} 420 H{L + 236} M{L + 236} 300 V420" fill="none" stroke="{a.CYAN}" stroke-width="3"/>')
contact(L + 96, 300, "botón del piso 3")
contact(L + 96, 420, "relé EC33 piso 3", (6, 46), 1)
a.add(a.text(L + 24, 500, "Cierra cualquiera de los dos:", 16, a.TXT, a.SANS, 600))
a.add(a.text(L + 24, 524, "el control ve el botón apretado.", 16, a.TXT, a.SANS, 600))
when(a, a.pill(L + 24, 240, "tarjeta válida", a.OK, a.OKBG, 15, 28), 3, 46, still=1)
shaft(L + 400, 230, (27, 42, 47), "3")
when(a, a.pill(L + 300, 548, "va directo al 3", a.OK, a.OKBG, 15, 28), 42, 50, still=1)

# ---------- serie
R = 612
a.add(a.box(R, 172, 540, 420, a.WHITE, a.LINE, rx=18))
a.add(a.text(R + 24, 206, "Serie · liberar botones", 20, a.INK, a.HEAD, 600))
a.add(f'<path d="M{R + 30} 300 H{R + 50} M{R + 146} 300 H{R + 190}" fill="none" stroke="{a.CYAN}" stroke-width="3"/>')
contact(R + 52, 300, "relé EC33", (52, 98))
a.add(a.text(R + 30, 290, "común", 15, a.GREY, a.MONO, 600, "middle"))
# botonera
BX = R + 200
a.add(a.box(BX, 222, 150, 300, a.SLATE, a.LINE, rx=14))
a.add(a.text(BX + 75, 246, "botonera", 15, a.GREY, a.MONO, 600, "middle"))
for i, f in enumerate(FLOORS):
    y = 276 + i * 50
    a.add(f'<circle cx="{BX + 40}" cy="{y}" r="18" fill="{a.WHITE}" stroke="{a.LINE}" stroke-width="2"/>' + a.text(BX + 40, y + 5, f, 15, a.GREY, a.MONO, 600, "middle"))
    lib = f in ("3", "2")
    when(a, a.text(BX + 66, y + 5, "libre" if lib else "no", 15, a.OK if lib else a.GREY, a.MONO, 600), 53, 98)
    if lib:
        when(a, f'<circle cx="{BX + 40}" cy="{y}" r="19" fill="{a.OKBG}" stroke="{a.OK}" stroke-width="3"/>' + a.text(BX + 40, y + 5, f, 15, a.OK, a.MONO, 700, "middle"), 53, 98)
a.add(f'<path d="M{R + 190} 300 H{BX}" stroke="{a.CYAN}" stroke-width="3"/>')
when(a, a.pill(R + 24, 240, "tarjeta válida", a.OK, a.OKBG, 15, 28), 52, 98)
# el usuario aprieta el 3
y3b = 276 + 50
when(a, f'<circle cx="{BX + 40}" cy="{y3b}" r="27" fill="none" stroke="{a.BLUE}" stroke-width="3"/>', 77, 84)
when(a, a.pill(R + 24, 548, "aprieta el 3 entre los libres", a.BLUE, "#E6F1FB", 15, 28), 77, 98)
shaft(R + 400, 230, (80, 94, 98), "")

out(a, 36, 2, "Paralelo o serie: el mismo relé, otro resultado",
    "Animación con dos paneles. A la izquierda, cableado en paralelo: el contacto del relé del EC33 para el piso 3 está en paralelo con el botón del piso 3, y al lado un hueco de ascensor con la cabina en planta baja. "
    "Tiempo 1: el usuario pasa una tarjeta válida y el relé del piso 3 cierra. "
    "Tiempo 2: para el control es como si apretaran el botón, y la cabina sube directo al piso 3. "
    "A la derecha, cableado en serie: el relé está en serie con el común de la botonera. "
    "Tiempo 3: con la tarjeta válida, el relé cierra y quedan libres solo los pisos permitidos, en el ejemplo el 2 y el 3. "
    "Tiempo 4: el usuario aprieta el 3 entre los pisos libres y la cabina sube al 3.",
    [12, 44, 66, 92])
