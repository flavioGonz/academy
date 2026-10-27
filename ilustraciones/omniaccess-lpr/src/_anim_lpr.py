"""Ayudas para las animaciones de teoría del curso OmniAccess LPR (sobre tools/anim.py, sin modificarla).

Cada animación: N tiempos iguales con leyenda numerada (a.steps), cajas fijas y fichas que viajan.
El cuadro fijo (movimiento reducido) muestra el tiempo `still`: lo que tenga still=1 tiene que entenderse solo.
La descripción (desc) sale del alt de teoria_figs (teoria_figs_lpr.py), así dice lo mismo que el manifest.
"""
import sys
sys.path.insert(0, "/home/claude/ies-training/tools")
sys.path.insert(0, "/home/claude/ies-training/ilustraciones/omniaccess-lpr/src")
from anim import Anim  # noqa
from teoria_figs_lpr import FIGS  # noqa

SITE = "/home/claude/ies-training/site2/ilustraciones/omniaccess-lpr/"
PREV = "/home/claude/ies-training/ilustraciones/omniaccess-lpr/"
DARK_SUB = "#9FC3E3"


def new(T, tema, title, caps, still, size=18):
    a = Anim(T=T, kicker=f"OMNIACCESS LPR · {tema.upper()}", title=title)
    spans = a.steps(caps, still=still, size=size)
    a.still_i = still
    a.spans = spans
    return a


def ph(a, i, j=None):
    """(inicio, fin) en % del tiempo i (o de i a j inclusive)."""
    j = i if j is None else j
    return a.spans[i][0], a.spans[j][1]


def vis(a, inner, i, j=None, still=None, fade=1.2, d0=0):
    """Visible durante los tiempos i..j (d0: demora en % desde el inicio del tiempo i).
    still: si no se indica, visible en el cuadro fijo cuando el tiempo fijo cae en i..j."""
    j = i if j is None else j
    s0, s1 = ph(a, i, j)
    st = still if still is not None else (1 if i <= a.still_i <= j else 0)
    return a.add(a.group(inner, a.show(s0 + d0, s1, fade), still=st))


def card(a, x, y, w, h, title, sub=None, dark=False, stroke=None, sw=2, tsize=19, fill=None):
    f = fill or (a.INK if dark else a.WHITE)
    s = a.box(x, y, w, h, f, stroke or (a.INK if dark else a.LINE), rx=14, sw=sw)
    ty = y + h / 2 + (-4 if sub else 7)
    s += a.text(x + 20, ty, title, tsize, a.WHITE if dark else a.INK, a.SANS, 600)
    if sub:
        s += a.text(x + 20, ty + 24, sub, 15, DARK_SUB if dark else a.GREY, a.MONO)
    return s


def token(a, label, pts, fg=None, bg=None, size=14, still=0):
    """Ficha con texto que viaja. pts: [(pct, x, y)] (centro de la ficha). Visible solo entre el primer y el último punto."""
    inner = a.pill(0, -14, label, fg or a.WHITE, bg or a.CYAN, size=size, anchor="middle")
    p0, p1 = pts[0][0], pts[-1][0]
    full = [(0, pts[0][1], pts[0][2])] + list(pts) + [(100, pts[-1][1], pts[-1][2])]
    mv = a.move(full)
    op = a.show(p0, p1, 0.8)
    return a.add(a.group(inner, mv, op, still=still))


def mover(a, inner, pts, still=0):
    """Cualquier dibujo (con origen en 0,0) que viaja por pts [(pct, x, y)], visible entre el primero y el último."""
    p0, p1 = pts[0][0], pts[-1][0]
    full = [(0, pts[0][1], pts[0][2])] + list(pts) + [(100, pts[-1][1], pts[-1][2])]
    return a.add(a.group(inner, a.move(full), a.show(p0, p1, 0.8), still=still))


def line(a, x1, y1, x2, y2, color=None, width=3, dash="", arrow=True):
    d = f"M{x1} {y1} L{x2} {y2}"
    if arrow:
        return a.arrow(d, color, width, dash)
    da = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<path d="{d}" fill="none" stroke="{color or a.BLUE}" stroke-width="{width}"{da}/>'


def plate(a, cx, cy, txt, w=190, h=58, size=28, stroke=None, extra=""):
    """Patente esquemática centrada en (cx, cy): borde, franja azul arriba, texto en mono."""
    x, y = cx - w / 2, cy - h / 2
    return (f'<g {extra}>' + a.box(x, y, w, h, a.WHITE, stroke or a.INK, rx=8, sw=2.5)
            + f'<rect x="{x + 2}" y="{y + 2}" width="{w - 4}" height="{h * 0.18:.1f}" rx="5" fill="{a.BLUE}"/>'
            + a.text(cx, cy + h * 0.32, txt, size, a.INK, a.MONO, 600, "middle") + '</g>')


def chip(a, x, y, label, fg, bg, size=14, anchor="start"):
    return a.pill(x, y, label, fg, bg, size=size, anchor=anchor)


def desc(fname):
    for figs in FIGS.values():
        for tf in figs:
            if tf["file"] == fname:
                return tf["alt"]
    raise SystemExit(f"sin alt para {fname} en teoria_figs_lpr.py")


def write(a, fname, title, pcts):
    stem = fname.rsplit(".", 1)[0]
    return a.write(SITE + fname, title, desc(fname), preview=pcts, prefix=PREV + "_t" + stem)
