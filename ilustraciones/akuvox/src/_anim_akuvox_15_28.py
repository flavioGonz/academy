"""Ayudantes de animación para la teoría de Akuvox, lecciones 15 a 28.
No toca anim.py ni ilus.py: reusa sus piezas (equipos de ilus.py dibujados dentro de un Anim)."""
import sys
sys.path.insert(0, "/home/claude/ies-training/tools")
from anim import Anim  # noqa
import ilus as I  # noqa

SITE = "/home/claude/ies-training/site2/ilustraciones/akuvox/"
PREV = "/home/claude/ies-training/ilustraciones/akuvox/"


def out(lid, n=1):
    return f"{SITE}{lid}-t{n}.svg", f"{PREV}_t{lid}-t{n}"


def new(T, kicker, title):
    return Anim(T=T, kicker=kicker, title=title)


def packet(a, label, p0, p1, t0, t1, color=None, fg=None, hide=None, size=15, still=0, via=()):
    """Pastilla que viaja de p0 a p1 entre t0% y t1%, visible desde t0 hasta hide% (por defecto t1+4)."""
    color = color or a.CYAN
    hide = hide if hide is not None else min(t1 + 4, 100)
    w = int(len(label) * size * 0.62 + 26)
    inner = (a.box(-w / 2, -15, w, 30, color, rx=15)
             + a.text(0, 6, label, size, fg or a.WHITE, a.MONO, 600, "middle"))
    mv = a.move([(0, *p0), (t0, *p0), *via, (t1, *p1), (100, *p1)])
    op = a.show(t0, hide, 0.8)
    return a.group(inner, mv, op, still=still)


def at(a, inner, t0, t1=100, still=1):
    """Grupo visible entre t0% y t1%."""
    return a.group(inner, a.show(t0, t1), still=still)


def mark(x, y, ok=True):
    return I.Mark(x, y, ok)


def tap(a, x, y, t, dur=10, still=0):
    """Toque de dedo: círculo que late alrededor de t%."""
    k = a.keyframes([(0, 0), (t, 0), (t + 1, 1), (t + dur - 1, 1), (t + dur, 0), (100, 0)])
    inner = (f'<circle cx="{x}" cy="{y}" r="26" fill="{a.CYAN}" opacity=".25"/>'
             f'<circle cx="{x}" cy="{y}" r="12" fill="{a.CYAN}" opacity=".7"/>')
    return a.group(inner, k, still=still)


def code(a, x, y, parts, size=16, h=44, pad=16, bg="#03213C"):
    """Línea de código con tramos de color: parts=[(texto, color)]. Devuelve svg y lista de (x0, x1)."""
    k = size * 0.6
    w = sum(len(p) for p, _ in parts) * k + 2 * pad
    s = [f'<rect x="{x}" y="{y}" width="{w:.0f}" height="{h}" rx="10" fill="{bg}"/>']
    cx, spans = x + pad, []
    for p, col in parts:
        s.append(a.text(round(cx, 1), y + h / 2 + size * 0.35, p, size, col, a.MONO, 500))
        spans.append((cx, cx + len(p) * k))
        cx += len(p) * k
    return "".join(s), spans


def arrow(a, x1, y1, x2, y2, color=None, width=3, dash=""):
    return a.arrow(f"M{x1} {y1} L{x2} {y2}", color, width, dash)


def msg(a, x1, x2, y, label, t0, t1=100, color=None, still=1, size=15, sub=None, sub_color=None, dash=""):
    """Mensaje de diagrama de secuencia: flecha de x1 a x2 en y que aparece en t0%, con un punto que la recorre."""
    color = color or a.BLUE
    mid = (x1 + x2) / 2
    inner = a.arrow(f"M{x1} {y} L{x2 - (8 if x2 > x1 else -8)} {y}", color, 3, dash)
    inner += a.text(mid, y - 10, label, size, color, a.MONO, 600, "middle")
    if sub:
        inner += a.text(mid, y + 24, sub, size, sub_color or a.TXT, a.MONO, 500, "middle")
    s = a.group(inner, a.show(t0, t1), still=still)
    dot = f'<circle cx="0" cy="0" r="7" fill="{color}"/>'
    d = a.group(dot, a.move([(0, x1, y), (t0, x1, y), (t0 + 5, x2, y), (100, x2, y)]), a.show(t0, t0 + 6, 0.5), still=0)
    return s + d


def lifeline(a, x, y1, y2, title, sub=None, w=170):
    s = a.box(x - w / 2, y1, w, 50 if not sub else 62, a.WHITE, a.LINE, rx=12)
    s += a.text(x, y1 + 30, title, 17, a.INK, a.SANS, 600, "middle")
    if sub:
        s += a.text(x, y1 + 50, sub, 15, a.GREY, a.MONO, 400, "middle")
    top = y1 + (50 if not sub else 62)
    s += f'<path d="M{x} {top} V{y2}" stroke="{a.LINE}" stroke-width="2.5" stroke-dasharray="6 6"/>'
    return s


def zone(x, y, w, h, label, color=None):
    """Zona punteada como ilus.Zone, con la etiqueta en 15 px."""
    color = color or I.LINE2
    tc = color if color != I.LINE2 else I.INK3
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="22" fill="none" stroke="{color}" stroke-width="2" stroke-dasharray="7 7"/>'
            + f'<rect x="{x + 18}" y="{y - 14}" width="{len(label) * 9.4 + 24:.0f}" height="28" rx="14" fill="{I.GROUND}"/>'
            + I.text(x + 30, y + 6, label, 15, 600, tc, I.FM))


def only_still(a, inner):
    """Visible solo en el cuadro fijo (movimiento reducido); oculto durante la animación."""
    return a.group(inner, a.keyframes([(0, 0), (100, 0)]), still=1)
