"""Ayudantes para las animaciones "Cómo se ve en la red" (Resumen) y de Laboratorio del curso MikroTik,
lecciones de orden 1 a 9 (ids 1, 23, 6, 2, 25, 26, 14, 13, 15).

Se apoyan en tools/anim.py (no lo modifican) y reusan las piezas de las animaciones de teoría
(_anim_mikrotik_1_13: device, travel, pkt, during…). Agrega equipos con icono (los mismos glifos de ilus.py),
mensajes de diagrama de secuencia y la salida a site2 con revisión por tools/anim_preview.py.
"""
import subprocess
import sys

sys.path.insert(0, "/home/claude/ies-training/tools")
from anim import Anim  # noqa: E402,F401
from ilus import ICON  # noqa: E402
from _anim_mikrotik_1_13 import (SKY, GOLD, MINT, still_only, during, pkt, travel, place, xmark, check,  # noqa: F401
                                 note, term, line, caption_line)

SITE = "/home/claude/ies-training/site2/ilustraciones/mikrotik"
TOOLS = "/home/claude/ies-training/tools"


def glyph(a, name, x, y, color=None, scale=1.35, sw=1.8):
    """Icono de ilus.py (24x24) con la esquina superior izquierda en (x, y)."""
    return (f'<g transform="translate({x} {y}) scale({scale})" fill="none" stroke="{color or a.BLUE}" '
            f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">{ICON[name]}</g>')


def dev(a, x, y, w, h, title, sub="", icon=None, dark=False, sub2="", tsize=19, ssize=15, stroke=None, sw=2):
    """Equipo: caja con icono a la izquierda, título y una o dos líneas mono."""
    fill = a.INK if dark else a.WHITE
    st = stroke or (None if dark else a.LINE)
    s = a.box(x, y, w, h, fill, st, rx=14, sw=sw)
    tx = x + (62 if icon else 18)
    if icon:
        s += glyph(a, icon, x + 18, y + 18, a.CYAN if dark else a.BLUE)
    s += a.text(tx, y + 34, title, tsize, a.WHITE if dark else a.INK, a.SANS, 600)
    if sub:
        s += a.text(tx, y + 58, sub, ssize, SKY if dark else a.GREY, a.MONO)
    if sub2:
        s += a.text(tx, y + 80, sub2, ssize, SKY if dark else a.GREY, a.MONO)
    return s


def lifeline(a, x, y1, y2):
    return f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" stroke="{a.LINE}" stroke-width="2.5" stroke-dasharray="6 6"/>'


def msg(a, x1, x2, y, label, t, end=100, color=None, still=1, sub=None, dur=2.5, lsize=16, dash="", subcolor=None):
    """Mensaje horizontal de x1 a x2: un punto viaja desde t% y la flecha queda dibujada hasta end%."""
    c = color or a.BLUE
    tip = x2 - 2 if x2 > x1 else x2 + 2
    body = a.arrow(f"M{x1} {y} H{tip}", c, 3, dash)
    body += a.text((x1 + x2) / 2, y - 11, label, lsize, c, a.MONO, 600, "middle")
    if sub:
        body += a.text((x1 + x2) / 2, y + 24, sub, 15, subcolor or a.TXT, a.SANS, 400, "middle")
    a.add(a.group(body, a.show(t + dur * 0.6, end), still=still))
    mv = a.move([(0, x1, y), (t, x1, y), (t + dur, x2, y), (100, x2, y)])
    a.add(a.group(f'<circle cx="0" cy="0" r="9" fill="{c}"/>', mv, a.show(t, t + dur + 0.4, 0.3), still=0))


def status(a, y, items, x=600, anchor="middle", size=17):
    """Frases que se alternan en una línea: items = [(t0, t1, texto, color, still)]."""
    for t0, t1, txt, col, st in items:
        a.add(a.group(a.text(x, y, txt, size, col, a.SANS, 600, anchor), a.show(t0, t1, 0.8), still=st))


def pill_at(a, x, y, label, fg, bg, t0, t1=100, still=0, size=15, h=28, anchor="start"):
    a.add(a.group(a.pill(x, y, label, fg, bg, size, h, anchor), a.show(t0, t1, 0.8), still=still))


def write(a, lid, kind, title, desc, pcts):
    """Guarda site2/ilustraciones/mikrotik/<lid>-<kind>.svg y deja la revisión _rev-<lid>-<kind>-<pct>.png."""
    path = a.save(f"{SITE}/{lid}-{kind}.svg", title, desc)
    subprocess.run([sys.executable, f"{TOOLS}/anim_preview.py", str(path), "--pct", ",".join(str(p) for p in pcts)], check=True)
    return path
