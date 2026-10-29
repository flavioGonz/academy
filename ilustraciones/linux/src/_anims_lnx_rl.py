"""Ayudantes para las animaciones de Resumen ("Cómo se ve en la red") y de Laboratorio del curso Linux
(las 12 lecciones). Se apoyan en tools/anim.py, en los íconos de tools/ilus.py y en las piezas de _alnx.py
(terminal, chip, mono), sin tocarlos.

Convenciones (las mismas de las animaciones nuevas de MikroTik):
- Tiempos en porcentaje del ciclo (0 a 100).
- en(): visible entre t0 y t1; fijo(): solo en el cuadro fijo (movimiento reducido).
- viaje(): una píldora que recorre una polilínea entre t0 y t1, a velocidad pareja.
- msg(): mensaje de diagrama de secuencia (punto que viaja y flecha que queda).
- escribir(): guarda en site2/ilustraciones/linux/<nombre>.svg y saca la vista previa con tools/anim_preview.py
  (PNG en ilustraciones/linux/_rev-<nombre>-<pct>.png y -fijo.png).
"""
import math
import subprocess
import sys

sys.path.insert(0, "/home/claude/ies-training/tools")
sys.path.insert(0, "/home/claude/ies-training/ilustraciones/linux/src")
from anim import Anim  # noqa: E402,F401
from ilus import ICON  # noqa: E402
from _alnx import NOLIG, term, trow, mono, chip, nb, T_CMD, T_OUT, T_PR, T_OK, T_ERR, T_COM, T_WARN  # noqa: E402,F401

SITE = "/home/claude/ies-training/site2/ilustraciones/linux"
LIGHT = "#9FC3E3"   # texto secundario sobre fondo oscuro
GOLD = "#FFD28A"    # atención sobre fondo oscuro
MINT = "#5BE0A5"    # correcto sobre fondo oscuro
CORAL = "#FFB4A3"   # error sobre fondo oscuro
GHOST = "#E6EDF4"   # píldora gris clara


def nueva(T, kicker, title):
    a = Anim(T=T, kicker=kicker, title=title)
    a.add(NOLIG)
    return a


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


def glyph(a, name, x, y, color=None, scale=1.35, sw=1.8):
    return (f'<g transform="translate({x} {y}) scale({scale})" fill="none" stroke="{color or a.BLUE}" '
            f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">{ICON[name]}</g>')


def dev(a, x, y, w, h, title, sub="", icon=None, dark=False, sub2="", tsize=19, ssize=15, stroke=None, sw=2):
    """Equipo: caja con ícono a la izquierda, título y una o dos líneas mono."""
    fill = a.INK if dark else a.WHITE
    st = stroke or (None if dark else "#C2D4E6")
    s = a.box(x, y, w, h, fill, st, rx=16, sw=sw)
    tx = x + (62 if icon else 20)
    if icon:
        s += glyph(a, icon, x + 18, y + h / 2 - 16, a.CYAN if dark else a.BLUE)
    nl = 1 + bool(sub) + bool(sub2)
    ty = y + h / 2 - (nl - 1) * 11 + 6
    s += a.text(tx, ty, title, tsize, a.WHITE if dark else a.INK, a.SANS, 600)
    if sub:
        s += a.text(tx, ty + 23, sub, ssize, LIGHT if dark else a.GREY, a.MONO)
    if sub2:
        s += a.text(tx, ty + 45, sub2, ssize, LIGHT if dark else a.GREY, a.MONO)
    return s


def pill_c(a, label, fg, bg, size=15, h=30, stroke=None):
    """Píldora centrada en (0,0)."""
    w = int(len(label) * size * 0.62 + 28)
    st = f' stroke="{stroke}" stroke-width="2"' if stroke else ""
    return (f'<rect x="{-w / 2}" y="{-h / 2}" width="{w}" height="{h}" rx="{h / 2}" fill="{bg}"{st}/>'
            + a.text(0, size * 0.36, label, size, fg, a.MONO, 600, "middle"))


def place(inner, x, y):
    return f'<g transform="translate({x},{y})">{inner}</g>'


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


def linea(x1, y1, x2, y2, color, w=3, dash=""):
    da = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{w}"{da} stroke-linecap="round"/>'


def camino(d, color, w=3, dash=""):
    da = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{w}"{da} stroke-linecap="round" stroke-linejoin="round"/>'


def marca(a, cx, cy, ok=True, r=15):
    c = a.OK if ok else a.BAD
    if ok:
        p = f'M{cx - 7} {cy} L{cx - 2} {cy + 6} L{cx + 8} {cy - 6}'
    else:
        p = f'M{cx - 6} {cy - 6} L{cx + 6} {cy + 6} M{cx + 6} {cy - 6} L{cx - 6} {cy + 6}'
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#FFFFFF" stroke="{c}" stroke-width="2.5"/>'
            f'<path d="{p}" fill="none" stroke="{c}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>')


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


def narr(a, items, x=48, y=640, size=17, still_idx=None):
    """items: [(t0, t1, texto, color)]: una línea de narración abajo."""
    for i, (t0, t1, s, c) in enumerate(items):
        en(a, a.text(x, y, s, size, c or a.INK, a.SANS, 600), t0, t1, still=1 if i == still_idx else 0)


def nota(a, x, y, w, h, title, lines, kind="info", tsize=17, lsize=15):
    fg, bg = {"info": (a.BLUE, "#E5F0FB"), "ok": (a.OK, a.OKBG), "bad": (a.BAD, a.BADBG), "amb": (a.AMB, a.AMBBG)}[kind]
    s = a.box(x, y, w, h, bg, fg, rx=12, sw=2) + a.text(x + 18, y + 28, title, tsize, fg, a.SANS, 700)
    for i, ln in enumerate(lines):
        s += a.text(x + 18, y + 54 + i * 22, ln, lsize, a.INK, a.SANS, 500)
    return s


def tterm(a, x, y, w, h, title=None):
    """Caja de terminal vacía (fondo oscuro), con título opcional. Las filas se agregan con trow_at."""
    s = a.box(x, y, w, h, "#03213C", None, rx=12)
    if title:
        s += a.text(x + 16, y + 24, title, 13, "#7FA6C9", a.MONO, 500, extra='letter-spacing="1.5"')
    return s


def trow_at(a, x, y, r, size=15):
    return trow(a, x, y, r, size)


def escribir(a, nombre, title, desc, pcts):
    """Guarda <SITE>/<nombre>.svg y saca la vista previa confiable (anim_preview.py)."""
    p = a.save(f"{SITE}/{nombre}.svg", title, desc)
    subprocess.run([sys.executable, "/home/claude/ies-training/tools/anim_preview.py", str(p),
                    "--pct", ",".join(str(x) for x in pcts)], check=True)
    return p
