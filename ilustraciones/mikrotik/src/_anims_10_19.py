"""Ayudantes para las animaciones de Resumen y Laboratorio del curso MikroTik, lecciones de orden 10 a 19
(ids 27, 11, 37, 38, 39, 29, 35, 34, 12, 5). Se apoyan en tools/anim.py y en los íconos de tools/ilus.py, sin tocarlos.

Convenciones:
- Tiempos en porcentaje del ciclo (0 a 100).
- en(): visible entre t0 y t1; fijo(): solo en el cuadro fijo (movimiento reducido).
- viaje(): una píldora que recorre una polilínea entre t0 y t1, a velocidad pareja.
- escribir(): guarda en site2/ilustraciones/mikrotik/<nombre>.svg y saca la vista previa con tools/anim_preview.py
  (PNG en ilustraciones/mikrotik/_rev-<nombre>-<pct>.png y -fijo.png).
"""
import math
import subprocess
import sys

sys.path.insert(0, "/home/claude/ies-training/tools")
from anim import Anim  # noqa: E402,F401
from ilus import ICON  # noqa: E402

SITE = "/home/claude/ies-training/site2/ilustraciones/mikrotik"
LIGHT = "#9FC3E3"   # texto secundario sobre fondo oscuro
GOLD = "#FFD28A"    # atención sobre fondo oscuro
MINT = "#5BE0A5"    # correcto sobre fondo oscuro
CORAL = "#FFB4A3"   # error sobre fondo oscuro
GHOST = "#E6EDF4"   # píldora gris clara


def vis(a, wins, fade=0.8):
    """Opacidad 1 dentro de cada ventana (inicio, fin), 0 fuera."""
    pts = [(0, 0)]
    end_on = False
    for s, e in wins:
        if s <= 0:
            pts.append((0, 1))
        else:
            pts += [(s, 0), (min(s + fade, 100), 1)]
        if e >= 100:
            pts.append((100, 1))
            end_on = True
        else:
            pts += [(max(e - fade, s + fade), 1), (e, 0)]
    if not end_on:
        pts.append((100, 0))
    return a.keyframes(pts)


def en(a, inner, t0, t1=100, still=0):
    return a.add(a.group(inner, vis(a, [(t0, t1)]), still=still))


def ventanas(a, inner, wins, still=0):
    return a.add(a.group(inner, vis(a, wins), still=still))


def fijo(a, inner):
    """Solo en el cuadro fijo."""
    return a.add(a.group(inner, a.keyframes([(0, 0), (100, 0)]), still=1))


def dev(a, x, y, w, h, title, sub="", icon=None, dark=False, hl=None, sub2="", tsize=19):
    """Equipo con ícono (los mismos de ilus.py), título y subtítulo en mono."""
    fill = a.INK if dark else a.WHITE
    stroke = hl or (a.INK if dark else "#C2D4E6")
    s = a.box(x, y, w, h, fill, stroke, rx=16, sw=3 if hl else 2)
    tx = x + (62 if icon else 20)
    if icon:
        iy = y + h / 2 - 16
        s += (f'<g transform="translate({x + 18} {iy}) scale(1.35)" fill="none" stroke="{a.CYAN if dark else a.BLUE}" '
              f'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{ICON[icon]}</g>')
    nl = 1 + bool(sub) + bool(sub2)
    ty = y + h / 2 - (nl - 1) * 11 + 6
    s += a.text(tx, ty, title, tsize, a.WHITE if dark else a.INK, a.SANS, 600)
    if sub:
        s += a.text(tx, ty + 23, sub, 15, LIGHT if dark else a.GREY, a.MONO)
    if sub2:
        s += a.text(tx, ty + 44, sub2, 15, LIGHT if dark else a.GREY, a.MONO)
    return s


def pill_c(a, label, fg, bg, size=15, h=30, stroke=None):
    """Píldora centrada en (0,0)."""
    w = int(len(label) * size * 0.62 + 28)
    st = f' stroke="{stroke}" stroke-width="2"' if stroke else ""
    return (f'<rect x="{-w / 2}" y="{-h / 2}" width="{w}" height="{h}" rx="{h / 2}" fill="{bg}"{st}/>'
            + a.text(0, size * 0.36, label, size, fg, a.MONO, 600, "middle"))


def viaje(a, label, pts, t0, t1, fg="#FFFFFF", bg=None, hold=1.5, still=0, size=15, stroke=None, inner=None):
    """Píldora (o inner, dibujado en 0,0) que recorre pts [(x, y)] entre t0 y t1 y queda 'hold' al final."""
    bg = bg or a.CYAN
    segs = [math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
    tot = sum(segs) or 1
    kf = [(0, *pts[0]), (t0, *pts[0])]
    acc = 0
    for i, sl in enumerate(segs):
        acc += sl
        kf.append((t0 + (t1 - t0) * acc / tot, *pts[i + 1]))
    kf.append((100, *pts[-1]))
    mv = a.move(kf)
    body = inner if inner is not None else pill_c(a, label, fg, bg, size, stroke=stroke)
    return a.add(a.group(body, mv, vis(a, [(t0, min(t1 + hold, 100))], 0.5), still=still))


def place(inner, x, y):
    return f'<g transform="translate({x},{y})">{inner}</g>'


def linea(x1, y1, x2, y2, color, w=3, dash=""):
    da = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{w}"{da} stroke-linecap="round"/>'


def marca(a, cx, cy, ok=True, r=15):
    c = a.OK if ok else a.BAD
    if ok:
        p = f'M{cx - 7} {cy} L{cx - 2} {cy + 6} L{cx + 8} {cy - 6}'
    else:
        p = f'M{cx - 6} {cy - 6} L{cx + 6} {cy + 6} M{cx + 6} {cy - 6} L{cx - 6} {cy + 6}'
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#FFFFFF" stroke="{c}" stroke-width="2.5"/>'
            f'<path d="{p}" fill="none" stroke="{c}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>')


def narr(a, items, x=48, y=640, size=17, still_idx=None):
    """items: [(t0, t1, texto, color)]: una línea de narración abajo."""
    for i, (t0, t1, s, c) in enumerate(items):
        en(a, a.text(x, y, s, size, c, a.SANS, 600), t0, t1, still=1 if i == still_idx else 0)


def panel(a, x, y, w, h, title, sub="", dark=True):
    s = a.box(x, y, w, h, a.INK if dark else a.WHITE, None if dark else a.LINE, rx=18)
    s += a.text(x + 22, y + 34, title, 18, "#FFFFFF" if dark else a.INK, a.HEAD, 600)
    if sub:
        s += a.text(x + w - 22, y + 34, sub, 15, LIGHT if dark else a.GREY, a.MONO, 400, "end")
    return a.add(s)


def escribir(a, nombre, title, desc, pcts):
    """Guarda <SITE>/<nombre>.svg y saca la vista previa confiable (anim_preview.py)."""
    p = a.save(f"{SITE}/{nombre}.svg", title, desc)
    subprocess.run([sys.executable, "/home/claude/ies-training/tools/anim_preview.py", str(p),
                    "--pct", ",".join(str(x) for x in pcts)], check=True)
    return p
