"""Ayudantes propios para las animaciones de Teoría de Akuvox 29 a 42 (no tocan anim.py ni ilus.py).

new()      -> Anim con kicker AKUVOX
out()      -> guarda en site2/ilustraciones/akuvox/<id>-t<N>.svg y deja PNG en ilustraciones/akuvox/_t<id>-t<N>-*.png
box()      -> caja de ilus.py (título, subtítulo, ícono) como fragmento SVG
travel()   -> una píldora que viaja de un punto a otro entre dos instantes
seq()      -> flecha que aparece en un instante y queda hasta otro (diagramas de escalera)
"""
import sys
sys.path.insert(0, "/home/claude/ies-training/tools")
from anim import Anim  # noqa: E402
import ilus  # noqa: E402

SITE = "/home/claude/ies-training/site2/ilustraciones/akuvox"
PREV = "/home/claude/ies-training/ilustraciones/akuvox"


def new(T, tema, title):
    return Anim(T=T, kicker=f"AKUVOX · {tema}", title=title)


def out(a, lid, n, title, desc, pcts):
    return a.write(f"{SITE}/{lid}-t{n}.svg", title, desc, preview=pcts, prefix=f"{PREV}/_t{lid}-t{n}")


def box(x, y, w, h, title, sub="", icon=None, dark=False, hl=None):
    return ilus.Box(x, y, w, h, title, sub, dark=dark, icon=ilus.ICON[icon] if icon else None, hl=hl).svg()


def pill_at0(a, label, fg, bg, size=15, h=30):
    """píldora centrada en (0,0) para mover con translate."""
    w = int(len(label) * size * 0.62 + 26)
    return (a.box(-w / 2, -h / 2, w, h, bg, rx=h / 2)
            + a.text(0, h * 0.18 + 1, label, size, fg, a.MONO, 600, "middle"))


def travel(a, p1, p2, t0, t1, label=None, fg="#FFFFFF", bg=None, dot=None, hold=1.0, still=0):
    """Píldora (o punto) que viaja de p1 a p2 entre t0 y t1 (porcentajes) y desaparece 'hold' después."""
    bg = bg or a.CYAN
    inner = pill_at0(a, label, fg, bg) if label else f'<circle cx="0" cy="0" r="{dot or 9}" fill="{bg}"/>'
    mv = a.move([(0, *p1), (t0, *p1), (t1, *p2), (100, *p2)])
    return a.add(a.group(inner, mv, a.show(t0, min(t1 + hold, 100), 0.5), still=still))


def seq(a, d, t, until=100, color=None, label=None, lx=None, ly=None, still=1, dash="", lcolor=None, lsize=15, anchor="middle", width=3):
    """Flecha (path d) que aparece en t y queda hasta 'until', con etiqueta opcional."""
    inner = a.arrow(d, color or a.BLUE, width, dash)
    if label:
        inner += a.text(lx, ly, label, lsize, lcolor or color or a.BLUE, a.MONO, 600, anchor)
    return a.add(a.group(inner, a.show(t, until), still=still))


def when(a, inner, t0, t1=100, still=0, fade=1.2):
    return a.add(a.group(inner, a.show(t0, t1, fade), still=still))


def note(a, x, y, s, size=17, fill=None, weight=600):
    return a.text(x, y, s, size, fill or a.INK, a.SANS, weight)


def check(a, cx, cy, ok=True, r=16):
    c = a.OK if ok else a.BAD
    bg = a.OKBG if ok else a.BADBG
    p = (f'<path d="M{cx - 7} {cy} l5 5 l9 -10" fill="none" stroke="{c}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>' if ok
         else f'<path d="M{cx - 6} {cy - 6} l12 12 M{cx + 6} {cy - 6} l-12 12" stroke="{c}" stroke-width="3" stroke-linecap="round"/>')
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{bg}" stroke="{c}" stroke-width="2"/>' + p
