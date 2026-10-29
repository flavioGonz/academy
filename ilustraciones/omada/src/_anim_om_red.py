"""Ayudantes para las animaciones "Cómo se ve en la red" (Resumen, <id>-r1.svg), de Laboratorio (<id>-l1/-l2.svg)
y de teoría extra del curso Omada. Se apoyan en tools/anim.py (no lo modifican) y en los glifos de ilus.py.

Convenciones: tiempos en porcentaje del ciclo; un "paquete" se dibuja centrado en (0, 0) y se mueve con travel();
still = opacidad en el cuadro fijo (movimiento reducido). Texto de 15 px como mínimo.
"""
import math
import subprocess
import sys

sys.path.insert(0, "/home/claude/ies-training/tools")
from anim import Anim  # noqa: E402,F401
from ilus import ICON  # noqa: E402

SITE = "/home/claude/ies-training/site2/ilustraciones/omada"
TOOLS = "/home/claude/ies-training/tools"
SKY = "#9FC3E3"     # texto secundario sobre fondo oscuro
GOLD = "#FFD28A"    # atención sobre fondo oscuro
MINT = "#5BE0A5"    # correcto sobre fondo oscuro


def nueva(T, tema, titulo, kind="r"):
    k = {"r": "CÓMO SE VE EN LA RED", "l": "LABORATORIO", "t": "TEORÍA"}[kind]
    return Anim(T=T, kicker=f"OMADA · {tema} · {k}", title=titulo)


# ---------- piezas fijas
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
        s += glyph(a, icon, x + 18, y + (h - 32) / 2 if h < 70 else y + 18, a.CYAN if dark else a.BLUE)
    ty = y + (h / 2 + 7 if not sub else (34 if h >= 70 else h / 2 - 3))
    s += a.text(tx, ty, title, tsize, a.WHITE if dark else a.INK, a.SANS, 600)
    if sub:
        s += a.text(tx, ty + 24, sub, ssize, SKY if dark else a.GREY, a.MONO)
    if sub2:
        s += a.text(tx, ty + 46, sub2, ssize, SKY if dark else a.GREY, a.MONO)
    return s


def eap(a, cx, cy, r=26, color=None):
    """EAP visto desde abajo: disco con anillo y LED."""
    c = color or a.CYAN
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{a.WHITE}" stroke="{a.LINE}" stroke-width="2"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r * 0.62:.1f}" fill="none" stroke="{c}" stroke-width="2.5"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r * 0.18:.1f}" fill="{c}"/>')


def line(x1, y1, x2, y2, color, w=3, dash=""):
    da = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{w}"{da} stroke-linecap="round"/>'


def pkt(a, label, fill=None, fg=None, size=15, h=32):
    """Píldora de paquete centrada en (0,0)."""
    size = max(size, 15)
    w = int(len(label) * size * 0.62 + 28)
    return (a.box(-w / 2, -h / 2, w, h, fill or a.CYAN, rx=h / 2)
            + a.text(0, size * 0.36, label, size, fg or a.WHITE, a.MONO, 600, "middle"))


def dot(a, c, r=9):
    return f'<circle cx="0" cy="0" r="{r}" fill="{c}" stroke="{a.WHITE}" stroke-width="2"/>'


def chip(a, x, y, label, fg=None, bg=None, size=15, h=30, anchor="start", stroke=None):
    size, h = max(size, 15), max(h, 30)
    w = int(len(label) * size * 0.62 + 26)
    x0 = x - w if anchor == "end" else (x - w / 2 if anchor == "middle" else x)
    st = f' stroke="{stroke}" stroke-width="1.5"' if stroke else ""
    return (f'<rect x="{x0:.1f}" y="{y}" width="{w}" height="{h}" rx="{h / 2}" fill="{bg or a.SLATE}"{st}/>'
            + a.text(x0 + w / 2, y + h * 0.68, label, size, fg or a.INK, a.MONO, 600, "middle"))


def xmark(a, x, y, r=15):
    d = r * 0.42
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="{a.WHITE}" stroke="{a.BAD}" stroke-width="2.5"/>'
            f'<path d="M{x - d:.1f} {y - d:.1f} L{x + d:.1f} {y + d:.1f} M{x + d:.1f} {y - d:.1f} L{x - d:.1f} {y + d:.1f}" stroke="{a.BAD}" stroke-width="3" stroke-linecap="round"/>')


def check(a, x, y, r=15):
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="{a.WHITE}" stroke="{a.OK}" stroke-width="2.5"/>'
            f'<path d="M{x - r * .45:.1f} {y + r * .02:.1f} L{x - r * .1:.1f} {y + r * .38:.1f} L{x + r * .48:.1f} {y - r * .35:.1f}" fill="none" stroke="{a.OK}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>')


def note(a, x, y, w, h, title, lines, kind="info", tsize=16, lsize=15, lh=21):
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
        yy += lh
    return s


def term(a, x, y, w, lines, title="", size=15, lh=24, colors=None, h=None):
    """Terminal o ventana oscura con líneas mono. colors = {índice: color}."""
    hh = h or (22 + (26 if title else 0) + lh * len(lines))
    s = a.box(x, y, w, hh, a.INK, rx=12)
    yy = y + 30
    if title:
        s += a.text(x + 18, yy, title, 15, SKY, a.MONO, 400)
        yy += 28
    for i, ln in enumerate(lines):
        c = (colors or {}).get(i, a.WHITE)
        s += a.text(x + 18, yy, ln, size, c, a.MONO)
        yy += lh
    return s


def tline(a, x, y, s, color=None, size=15, weight=400):
    """Una línea mono (para escribir dentro de un term() en momentos distintos)."""
    return a.text(x, y, s, size, color or a.WHITE, a.MONO, weight)


def lifeline(a, x, y1, y2):
    return f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" stroke="{a.LINE}" stroke-width="2.5" stroke-dasharray="6 6"/>'


# ---------- tiempo
def during(a, inner, t0, t1=100, still=0, fade=1.0):
    return a.group(inner, a.show(t0, t1, fade), still=still)


def at(a, inner, t0, t1=100, still=0, fade=1.0):
    """during() y lo agrega."""
    return a.add(during(a, inner, t0, t1, still, fade))


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
    mv = a.move([(round(p, 2), x, y) for p, x, y in kf])
    op = a.show(t0, min(t1 + hold, 100), fade)
    return a.add(a.group(inner, mv, op, still=still))


def msg(a, x1, x2, y, label, t, end=100, color=None, still=1, dur=2.5, lsize=16, dash="", lab_x=None, anchor="middle", sub=None):
    """Mensaje horizontal de x1 a x2: un punto viaja desde t% y la flecha queda dibujada hasta end%."""
    c = color or a.BLUE
    tip = x2 - 2 if x2 > x1 else x2 + 2
    body = a.arrow(f"M{x1} {y} H{tip}", c, 3, dash)
    lx = lab_x if lab_x is not None else (x1 + x2) / 2
    body += a.text(lx, y - 11, label, lsize, c, a.MONO, 600, anchor)
    if sub:
        body += a.text(lx, y + 23, sub, 15, a.TXT, a.SANS, 400, anchor)
    a.add(a.group(body, a.show(t + dur * 0.6, end), still=still))
    mv = a.move([(0, x1, y), (t, x1, y), (t + dur, x2, y), (100, x2, y)])
    a.add(a.group(f'<circle cx="0" cy="0" r="9" fill="{c}"/>', mv, a.show(t, t + dur + 0.4, 0.3), still=0))


def status(a, y, items, x=600, anchor="middle", size=17):
    """Frases que se alternan en una línea: items = [(t0, t1, texto, color, still)]."""
    for t0, t1, txt, col, st in items:
        a.add(a.group(a.text(x, y, txt, size, col, a.SANS, 600, anchor), a.show(t0, t1, 0.8), still=st))


def solo_fijo(a, inner):
    return a.add(a.group(inner, a.keyframes([(0, 0), (100, 0)]), still=1))


def write(a, lid, kind, title, desc, pcts):
    """Guarda site2/ilustraciones/omada/<lid>-<kind>.svg y deja la revisión ilustraciones/omada/_rev-<lid>-<kind>-<pct>.png."""
    path = a.save(f"{SITE}/{lid}-{kind}.svg", title, desc)
    subprocess.run([sys.executable, f"{TOOLS}/anim_preview.py", str(path), "--pct", ",".join(str(p) for p in pcts)], check=True)
    return path
