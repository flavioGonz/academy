"""Ayudas para las animaciones de teoría del curso HikCentral (sobre tools/anim.py, sin modificarla).

Cada animación: N tiempos iguales con leyenda numerada (a.steps), cajas fijas y fichas que viajan.
El cuadro fijo (movimiento reducido) muestra el tiempo `still`: lo que tenga still=1 tiene que entenderse solo.
La descripción (desc) sale del alt de teoria_figs en manifest.json, para que diga lo mismo.
"""
import json, sys
sys.path.insert(0, "/home/claude/ies-training/tools")
from anim import Anim  # noqa

SITE = "/home/claude/ies-training/site2/ilustraciones/hikcentral/"
PREV = "/home/claude/ies-training/ilustraciones/hikcentral/"
MAN = "/home/claude/ies-training/ilustraciones/hikcentral/manifest.json"
DARK_SUB = "#9FC3E3"


def new(T, tema, title, caps, still):
    a = Anim(T=T, kicker=f"HIKCENTRAL · {tema.upper()}", title=title)
    spans = a.steps(caps, still=still)
    a.still_i = still
    a.spans = spans
    return a


def ph(a, i, j=None):
    """(inicio, fin) en % del tiempo i (o de i a j inclusive)."""
    j = i if j is None else j
    return a.spans[i][0], a.spans[j][1]


def vis(a, inner, i, j=None, still=None, fade=1.2):
    """Visible durante los tiempos i..j. still: si no se indica, visible en el cuadro fijo cuando lo incluye."""
    j = i if j is None else j
    s0, s1 = ph(a, i, j)
    st = still if still is not None else (1 if i <= a.still_i <= j else 0)
    return a.add(a.group(inner, a.show(s0, s1, fade), still=st))


def card(a, x, y, w, h, title, sub=None, dark=False, stroke=None, sw=2, tsize=19):
    fill = a.INK if dark else a.WHITE
    s = a.box(x, y, w, h, fill, stroke or (a.INK if dark else a.LINE), rx=14, sw=sw)
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


def desc(fname):
    m = json.load(open(MAN, encoding="utf-8"))
    for v in m.values():
        for tf in v.get("teoria_figs", []):
            if tf["file"] == fname:
                return tf["alt"]
    raise SystemExit(f"sin alt para {fname} en el manifest")


def write(a, fname, title, pcts):
    stem = fname.rsplit(".", 1)[0]
    return a.write(SITE + fname, title, desc(fname), preview=pcts, prefix=PREV + "_anim-" + stem)


def stream(a, x1, y1, x2, y2, s0, s1, color=None, tt=5, gap=3.5, r=7):
    """Puntos que corren de (x1,y1) a (x2,y2) entre s0% y s1%: un flujo de video o de datos."""
    t = s0
    while t + tt <= s1:
        mv = a.move([(0, x1, y1), (t, x1, y1), (t + tt, x2, y2), (100, x2, y2)])
        op = a.keyframes([(0, 0), (max(t - 0.01, 0), 0), (t, 1), (t + tt, 1), (min(t + tt + 0.01, 100), 0), (100, 0)])
        a.add(a.group(f'<circle cx="0" cy="0" r="{r}" fill="{color or a.CYAN}"/>', mv, op, still=0))
        t += gap


def line(a, x1, y1, x2, y2, color=None, width=3, dash="", arrow=True):
    d = f"M{x1} {y1} L{x2} {y2}"
    if arrow:
        return a.arrow(d, color, width, dash)
    da = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<path d="{d}" fill="none" stroke="{color or a.BLUE}" stroke-width="{width}"{da}/>'
