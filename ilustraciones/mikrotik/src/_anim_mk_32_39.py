"""Ayudantes para las animaciones de Resumen y Laboratorio del curso MikroTik, lecciones de orden 32 a 39
(ids 10, 24, 21, 28, 22, 7, 16, 17). Se apoyan en tools/anim.py sin modificarlo.

Convenciones:
- Tiempos en porcentaje del ciclo (0 a 100).
- Un paquete se dibuja centrado en (0, 0) y se mueve con travel().
- still=1 marca lo que se ve en el cuadro fijo (movimiento reducido).
- Salida: site2/ilustraciones/mikrotik/<id>-r1.svg, <id>-l1.svg, <id>-l2.svg.
  Revisión: ilustraciones/mikrotik/_rev-<id>-<tipo>-<pct>.png (con tools/anim_preview.py).
"""
import math
import subprocess
import sys

sys.path.insert(0, "/home/claude/ies-training/tools")
from anim import Anim  # noqa: E402
from ilus import ICON  # noqa: E402  (mismos íconos que las ilustraciones fijas)

SITE = "/home/claude/ies-training/site2/ilustraciones/mikrotik"
SKY = "#9FC3E3"     # texto secundario sobre fondo oscuro
GOLD = "#FFD28A"    # atención sobre fondo oscuro
MINT = "#5BE0A5"    # correcto sobre fondo oscuro
ROSE = "#FF9C8A"    # bloqueado sobre fondo oscuro
SOFTW = "#C9DDF0"   # texto común sobre fondo oscuro


# ---------------------------------------------------------------- equipos
def dev(a, x, y, w, h, title, sub="", icon=None, dark=False, sub2="", hl=None, tsize=19):
    """Equipo: caja con ícono (de ilus.ICON), título y una o dos líneas mono."""
    fill = a.INK if dark else a.WHITE
    stroke = hl or (None if dark else a.LINE)
    s = a.box(x, y, w, h, fill, stroke, rx=16, sw=3 if hl else 2)
    tx = x + (62 if icon else 20)
    if icon:
        s += (f'<g transform="translate({x + 18} {y + 18}) scale(1.35)" fill="none" stroke="{a.CYAN if dark else a.BLUE}" '
              f'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{ICON[icon]}</g>')
    s += a.text(tx, y + 36, title, tsize, a.WHITE if dark else a.INK, a.SANS, 600)
    if sub:
        s += a.text(tx, y + 60, sub, 15, SKY if dark else a.GREY, a.MONO)
    if sub2:
        s += a.text(tx, y + 82, sub2, 15, SKY if dark else a.GREY, a.MONO)
    return s


def router(a, x, y, w, h, title="MikroTik", sub="", sub2=""):
    """Router: caja oscura (como en las animaciones de teoría)."""
    return dev(a, x, y, w, h, title, sub, None, True, sub2)


# ---------------------------------------------------------------- tiempo
def during(a, inner, t0, t1=100, still=0, fade=0.8):
    return a.group(inner, a.show(t0, t1, fade), still=still)


def still_only(a, inner):
    return a.group(inner, a.keyframes([(0, 0), (100, 0)]), still=1)


def wins(a, inner, ws, still=0, fade=0.8):
    """Visible en varias ventanas [(t0, t1), ...]."""
    pts = [(0, 0)]
    for s, e in ws:
        pts += [(s, 0), (s + fade, 1), (e - fade, 1), (e, 0)]
    pts.append((100, 0))
    d = {}
    for p, v in pts:
        d[round(p, 2)] = v
    return a.group(inner, a.keyframes(sorted(d.items())), still=still)


def travel(a, inner, pts, t0, t1, hold=1.5, still=0, fade=0.5):
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


def place(inner, x, y):
    return f'<g transform="translate({x},{y})">{inner}</g>'


# ---------------------------------------------------------------- piezas
def pkt(a, label, fill=None, fg=None, size=15, h=32, stroke=None):
    """Píldora centrada en (0,0)."""
    w = int(len(label) * size * 0.62 + 28)
    st = f' stroke="{stroke}" stroke-width="2"' if stroke else ""
    return (f'<rect x="{-w / 2}" y="{-h / 2}" width="{w}" height="{h}" rx="{h / 2}" fill="{fill or a.CYAN}"{st}/>'
            + a.text(0, size * 0.36, label, size, fg or a.WHITE, a.MONO, 600, "middle"))


def dot(a, col, r=11):
    return f'<circle cx="0" cy="0" r="{r}" fill="{col}" stroke="#FFFFFF" stroke-width="3"/>'


def check(a, x, y, r=15):
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="{a.WHITE}" stroke="{a.OK}" stroke-width="2.5"/>'
            f'<path d="M{x - r * .45} {y + r * .02} L{x - r * .1} {y + r * .38} L{x + r * .48} {y - r * .35}" fill="none" stroke="{a.OK}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>')


def xmark(a, x, y, r=15):
    d = r * 0.42
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="{a.WHITE}" stroke="{a.BAD}" stroke-width="2.5"/>'
            f'<path d="M{x - d} {y - d} L{x + d} {y + d} M{x + d} {y - d} L{x - d} {y + d}" stroke="{a.BAD}" stroke-width="3" stroke-linecap="round"/>')


def line(x1, y1, x2, y2, color, w=3, dash=""):
    da = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{w}"{da} stroke-linecap="round"/>'


def poly(pts, color, w=3, dash=""):
    da = f' stroke-dasharray="{dash}"' if dash else ""
    d = "M" + " L".join(f"{x} {y}" for x, y in pts)
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{w}"{da} stroke-linejoin="round" stroke-linecap="round"/>'


def term(a, x, y, w, lines, title="", size=15, lh=24, colors=None):
    """Terminal oscura con líneas mono. colors: {índice: color}."""
    h = 20 + (26 if title else 0) + lh * len(lines)
    s = a.box(x, y, w, h, a.INK, rx=12)
    yy = y + 30
    if title:
        s += a.text(x + 18, yy, title, 13, SKY, a.MONO, 400, extra='letter-spacing="1.6"')
        yy += 26
    for i, ln in enumerate(lines):
        s += a.text(x + 18, yy, ln, size, (colors or {}).get(i, a.WHITE), a.MONO)
        yy += lh
    return s


def note(a, x, y, w, h, title, lines, kind="info", tsize=16, lsize=15):
    """Recuadro con barra de color a la izquierda."""
    col, bg = {"ok": (a.OK, a.OKBG), "bad": (a.BAD, a.BADBG), "amb": (a.AMB, a.AMBBG), "info": (a.BLUE, a.WHITE)}[kind]
    s = a.box(x, y, w, h, bg, a.LINE if kind == "info" else None, rx=10, sw=1.5)
    s += f'<rect x="{x}" y="{y}" width="5" height="{h}" rx="2" fill="{col}"/>'
    yy = y + 26
    if title:
        s += a.text(x + 20, yy, title, tsize, col if kind != "info" else a.INK, a.SANS, 600)
        yy += 23
    for ln in lines:
        s += a.text(x + 20, yy, ln, lsize, a.INK if kind != "info" else a.TXT, a.SANS)
        yy += 21
    return s


def narr(a, x, y, items, size=17, anchor="start"):
    """items: [(t0, t1, texto, color, still)] frases que se alternan en el mismo lugar."""
    for t0, t1, txt, col, st in items:
        a.add(during(a, a.text(x, y, txt, size, col, a.SANS, 600, anchor), t0, t1, still=st))


# ---------------------------------------------------------------- salida
def write(a, lid, kind, title, desc, pcts):
    """Guarda <lid>-<kind>.svg en el sitio y deja los PNG de revisión en ilustraciones/mikrotik/."""
    path = a.save(f"{SITE}/{lid}-{kind}.svg", title, desc)
    subprocess.run([sys.executable, "/home/claude/ies-training/tools/anim_preview.py", str(path),
                    "--pct", ",".join(str(p) for p in pcts)], check=True)
    return path
