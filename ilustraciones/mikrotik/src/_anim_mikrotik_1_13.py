"""Ayudantes para las animaciones de teoría de MikroTik, lecciones 1 a 13.

Se apoyan en tools/anim.py (no la modifican). Convenciones:
- Un "paquete" se dibuja centrado en (0, 0) y se mueve con travel().
- still_only(): visible solo en el cuadro fijo (movimiento reducido).
- Tiempos en porcentaje del ciclo.
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, "/home/claude/ies-training/tools")
from anim import Anim  # noqa: E402

SITE = Path("/home/claude/ies-training/site2/ilustraciones/mikrotik")
PREV = Path("/home/claude/ies-training/ilustraciones/mikrotik")

SKY = "#9FC3E3"     # texto secundario sobre fondo oscuro
GOLD = "#FFD28A"    # atención sobre fondo oscuro
MINT = "#5BE0A5"    # correcto sobre fondo oscuro


def out(lid, n):
    return SITE / f"{lid}-t{n}.svg", str(PREV / f"_t{lid}-t{n}")


def still_only(a, inner):
    """Visible solo en el cuadro fijo."""
    return a.group(inner, a.keyframes([(0, 0), (100, 0)]), still=1)


def during(a, inner, t0, t1=100, still=0, fade=1.0):
    """Visible entre t0 y t1."""
    return a.group(inner, a.show(t0, t1, fade), still=still)


def device(a, x, y, w, h, title, sub="", dark=False, stroke=None, tsize=19, ssize=14, sub2=""):
    fill = a.INK if dark else a.WHITE
    st = None if dark else (stroke or a.LINE)
    s = a.box(x, y, w, h, fill, st, rx=14, sw=2)
    s += a.text(x + 18, y + 32, title, tsize, a.WHITE if dark else a.INK, a.SANS, 600)
    if sub:
        s += a.text(x + 18, y + 56, sub, ssize, SKY if dark else a.GREY, a.MONO)
    if sub2:
        s += a.text(x + 18, y + 78, sub2, ssize, SKY if dark else a.GREY, a.MONO)
    return s


def pkt(a, label, fill=None, fg=None, size=15, h=34):
    """Píldora centrada en (0,0)."""
    w = int(len(label) * size * 0.62 + 30)
    return (a.box(-w / 2, -h / 2, w, h, fill or a.CYAN, rx=h / 2)
            + a.text(0, h * 0.2 + 1, label, size, fg or a.WHITE, a.MONO, 600, "middle"))


def travel(a, inner, pts, t0, t1, hold=2.0, still=0, fade=0.5):
    """Mueve inner (dibujado en 0,0) por la polilínea pts entre t0 y t1; queda quieto 'hold' y se apaga."""
    segs = [math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
    tot = sum(segs) or 1
    kf = [(0, *pts[0]), (t0, *pts[0])]
    acc = 0
    for i, sl in enumerate(segs):
        acc += sl
        kf.append((t0 + (t1 - t0) * acc / tot, *pts[i + 1]))
    kf.append((100, *pts[-1]))
    mv = a.move([(p, x, y) for p, x, y in kf])
    op = a.show(t0, min(t1 + hold, 100), fade)
    return a.group(inner, mv, op, still=still)


def place(a, inner, x, y):
    return f'<g transform="translate({x},{y})">{inner}</g>'


def xmark(a, x, y, r=15):
    d = r * 0.42
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="{a.WHITE}" stroke="{a.BAD}" stroke-width="2.5"/>'
            f'<path d="M{x - d} {y - d} L{x + d} {y + d} M{x + d} {y - d} L{x - d} {y + d}" stroke="{a.BAD}" stroke-width="3" stroke-linecap="round"/>')


def check(a, x, y, r=15):
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="{a.WHITE}" stroke="{a.OK}" stroke-width="2.5"/>'
            f'<path d="M{x - r * .45} {y + r * .02} L{x - r * .1} {y + r * .38} L{x + r * .48} {y - r * .35}" fill="none" stroke="{a.OK}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>')


def note(a, x, y, w, h, title, lines, kind="info", tsize=16, lsize=15):
    """Recuadro con barra de color a la izquierda."""
    col, bg = {"ok": (a.OK, a.OKBG), "bad": (a.BAD, a.BADBG), "amb": (a.AMB, a.AMBBG), "info": (a.BLUE, a.WHITE)}[kind]
    s = a.box(x, y, w, h, bg, a.LINE if kind == "info" else None, rx=10, sw=1.5)
    s += f'<rect x="{x}" y="{y}" width="5" height="{h}" rx="2" fill="{col}"/>'
    yy = y + 26
    if title:
        s += a.text(x + 20, yy, title, tsize, col if kind != "info" else a.INK, a.SANS, 600)
        yy += 24
    for ln in lines:
        s += a.text(x + 20, yy, ln, lsize, a.INK if kind != "info" else a.TXT, a.SANS)
        yy += 21
    return s


def term(a, x, y, w, lines, title="", size=15, lh=24, colors=None):
    """Terminal oscura con líneas de texto mono."""
    h = 22 + (24 if title else 0) + lh * len(lines)
    s = a.box(x, y, w, h, a.INK, rx=12)
    yy = y + 30
    if title:
        s += a.text(x + 18, yy, title, 12, SKY, a.MONO, 400, extra='letter-spacing="1.8"')
        yy += 26
    for i, ln in enumerate(lines):
        c = (colors or {}).get(i, a.WHITE)
        s += a.text(x + 18, yy, ln, size, c, a.MONO)
        yy += lh
    return s


def line(x1, y1, x2, y2, color, w=3, dash=""):
    da = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{w}"{da} stroke-linecap="round"/>'


def caption_line(a, x, y, items, size=17):
    """items: [(t0, t1, texto, color, still)] frases que se alternan en el mismo lugar."""
    s = ""
    for t0, t1, txt, col, st in items:
        s += a.group(a.text(x, y, txt, size, col, a.SANS, 600), a.show(t0, t1, 0.8), still=st)
    return s
