"""Ayudantes para las animaciones de Resumen y Laboratorio del curso MikroTik, lecciones de orden 20 a 31
(ids 3, 4, 36, 33, 30, 31, 32, 9, 18, 8, 19, 20). Se apoyan en tools/anim.py sin modificarlo.

Convenciones:
- Tiempos en porcentaje del ciclo (0 a 100).
- Los paquetes se dibujan centrados en (0, 0) y viajan con go().
- fijo(): solo en el cuadro fijo (movimiento reducido).
- escribir(): guarda en site2 y saca la vista previa confiable con tools/anim_preview.py.
"""
import math
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, "/home/claude/ies-training/tools")
from anim import Anim  # noqa: E402

SITE = Path("/home/claude/ies-training/site2/ilustraciones/mikrotik")
PREV = Path("/home/claude/ies-training/ilustraciones/mikrotik")
SKY = "#9FC3E3"     # texto secundario sobre fondo oscuro
GOLD = "#FFD28A"    # atención sobre fondo oscuro
MINT = "#5BE0A5"    # correcto sobre fondo oscuro
ROSE = "#FFB4A3"    # error sobre fondo oscuro


def nuevo(T, kicker, title, pasos, still):
    a = Anim(T=T, kicker=kicker, title=title)
    tramos = a.steps(pasos, still=still)
    return a, tramos


# ---------- visibilidad
def vis(a, wins, fade=0.8):
    """Opacidad 1 dentro de cada ventana (inicio, fin), 0 fuera."""
    pts = [(0, 0)]
    end_on = False
    for s, e in wins:
        if s <= 0:
            pts += [(0, 1)]
        else:
            pts += [(s, 0), (s + fade, 1)]
        if e >= 100:
            pts += [(100, 1)]
            end_on = True
        else:
            pts += [(e - fade, 1), (e, 0)]
    if not end_on:
        pts.append((100, 0))
    return a.keyframes(pts)


def en(a, inner, t0, t1=100, still=0):
    return a.add(a.group(inner, vis(a, [(t0, t1)]), still=still))


def ventanas(a, inner, wins, still=0):
    return a.add(a.group(inner, vis(a, wins), still=still))


def fijo(a, inner):
    return a.add(a.group(inner, a.keyframes([(0, 0), (100, 0)]), still=1))


def narr(a, items, x=48, y=632, size=17, still_idx=None):
    """items: [(t0, t1, texto, color)] una línea de narración abajo."""
    for i, (t0, t1, s, c) in enumerate(items):
        en(a, a.text(x, y, s, size, c, a.SANS, 600), t0, t1, still=1 if i == still_idx else 0)


# ---------- piezas
def dev(a, x, y, w, h, title, sub="", sub2="", kind="pc", tsize=19, ssize=15, sub3="", add=True):
    """Equipo. kind: router (oscuro), pc, isp (gris), bad (atacante), cloud (borde punteado)."""
    if kind == "router":
        s = a.box(x, y, w, h, a.INK, rx=16)
        tc, sc = a.WHITE, SKY
    elif kind == "isp":
        s = a.box(x, y, w, h, a.SLATE, a.LINE, rx=16)
        tc, sc = a.INK, a.GREY
    elif kind == "bad":
        s = a.box(x, y, w, h, a.BADBG, a.BAD, rx=16, sw=2)
        tc, sc = a.BAD, a.TXT
    elif kind == "cloud":
        s = a.box(x, y, w, h, a.WHITE, a.CYAN, rx=22, sw=2.5, extra='stroke-dasharray="8 6"')
        tc, sc = a.INK, a.GREY
    else:
        s = a.box(x, y, w, h, a.WHITE, a.LINE, rx=16)
        tc, sc = a.INK, a.GREY
    s += a.text(x + 18, y + 32, title, tsize, tc, a.HEAD, 600)
    yy = y + 57
    for sb in (sub, sub2, sub3):
        if sb:
            s += a.text(x + 18, yy, sb, ssize, sc, a.MONO)
            yy += 22
    return a.add(s) if add else s


def pillc(a, label, fg=None, bg=None, size=15, h=32, stroke=None):
    """Píldora centrada en (0,0)."""
    w = int(len(label) * size * 0.62 + 28)
    st = f' stroke="{stroke}" stroke-width="2"' if stroke else ""
    return (f'<rect x="{-w / 2}" y="{-h / 2}" width="{w}" height="{h}" rx="{h / 2}" fill="{bg or a.CYAN}"{st}/>'
            + a.text(0, size * 0.36, label, size, fg or a.WHITE, a.MONO, 600, "middle"))


def at(inner, x, y):
    return f'<g transform="translate({x},{y})">{inner}</g>'


def go(a, label, pts, t0, t1, hold=2.0, fg=None, bg=None, size=15, still=0, inner=None):
    """Paquete que recorre la polilínea pts [(x,y)] a velocidad pareja entre t0 y t1, se queda 'hold' y se apaga."""
    inner = inner or pillc(a, label, fg, bg, size)
    segs = [math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
    tot = sum(segs) or 1
    kf = [(0, *pts[0]), (t0, *pts[0])]
    acc = 0
    for i, sl in enumerate(segs):
        acc += sl
        kf.append((t0 + (t1 - t0) * acc / tot, *pts[i + 1]))
    kf.append((100, *pts[-1]))
    mv = a.move([(p, x, y) for p, x, y in kf])
    op = vis(a, [(t0, min(t1 + hold, 100))], 0.5)
    return a.add(a.group(inner, mv, op, still=still))


def mark(a, cx, cy, ok=True, r=16):
    c = a.OK if ok else a.BAD
    if ok:
        p = f'M{cx - 7} {cy} L{cx - 2} {cy + 6} L{cx + 8} {cy - 6}'
    else:
        p = f'M{cx - 6} {cy - 6} L{cx + 6} {cy + 6} M{cx + 6} {cy - 6} L{cx - 6} {cy + 6}'
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#FFFFFF" stroke="{c}" stroke-width="2.5"/>'
            f'<path d="{p}" fill="none" stroke="{c}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>')


def wire(x1, y1, x2, y2, color="#DDE8F2", w=3, dash=""):
    da = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{w}"{da} stroke-linecap="round"/>'


def poly(pts, color, w=3, dash=""):
    da = f' stroke-dasharray="{dash}"' if dash else ""
    d = "M" + " L".join(f"{x} {y}" for x, y in pts)
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{w}"{da} stroke-linecap="round" stroke-linejoin="round"/>'


def term(a, x, y, w, lines, title="", size=15, lh=24, colors=None):
    """Terminal oscura. colors: {índice: color}."""
    h = 22 + (24 if title else 0) + lh * len(lines)
    s = a.box(x, y, w, h, a.INK, rx=12)
    yy = y + 30
    if title:
        s += a.text(x + 18, yy, title, 13, SKY, a.MONO, 400, extra='letter-spacing="1.8"')
        yy += 26
    for i, ln in enumerate(lines):
        s += a.text(x + 18, yy, ln, size, (colors or {}).get(i, a.WHITE), a.MONO)
        yy += lh
    return s


def note(a, x, y, w, h, title, lines, kind="info", tsize=17, lsize=15):
    col, bg = {"ok": (a.OK, a.OKBG), "bad": (a.BAD, a.BADBG), "amb": (a.AMB, a.AMBBG), "info": (a.BLUE, a.WHITE)}[kind]
    s = a.box(x, y, w, h, bg, a.LINE if kind == "info" else None, rx=10, sw=1.5)
    s += f'<rect x="{x}" y="{y}" width="5" height="{h}" rx="2" fill="{col}"/>'
    yy = y + 27
    if title:
        s += a.text(x + 20, yy, title, tsize, col if kind != "info" else a.INK, a.SANS, 600)
        yy += 24
    for ln in lines:
        s += a.text(x + 20, yy, ln, lsize, a.INK if kind != "info" else a.TXT, a.SANS)
        yy += 21
    return s


def mono_box(a, x, y, w, lines, title="", kind="amb", size=15, lh=23, colors=None):
    """Recuadro claro con barra de color y líneas en mono (comandos)."""
    col, bg = {"ok": (a.OK, a.OKBG), "bad": (a.BAD, a.BADBG), "amb": (a.AMB, a.AMBBG), "info": (a.BLUE, a.WHITE)}[kind]
    h = 20 + (28 if title else 0) + lh * len(lines)
    s = a.box(x, y, w, h, bg, a.LINE if kind == "info" else None, rx=10, sw=1.5)
    s += f'<rect x="{x}" y="{y}" width="5" height="{h}" rx="2" fill="{col}"/>'
    yy = y + 28
    if title:
        s += a.text(x + 20, yy, title, 17, col if kind != "info" else a.INK, a.SANS, 600)
        yy += 28
    for i, ln in enumerate(lines):
        s += a.text(x + 20, yy, ln, size, (colors or {}).get(i, a.INK), a.MONO)
        yy += lh
    return s


def ring(a, x, y, w, h, color, rx=16, sw=3.5):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="none" stroke="{color}" stroke-width="{sw}"/>'


def flip(a, x, y, items, size=15, fam=None, weight=600, anchor="start", still_idx=None):
    """Valor que cambia en el mismo lugar: items [(t0, t1, texto, color)]."""
    for i, (t0, t1, s, c) in enumerate(items):
        en(a, a.text(x, y, s, size, c, fam or a.MONO, weight, anchor), t0, t1, still=1 if i == still_idx else 0)


def flash_arrow(a, d, color, t0, t1=100, still=0, width=3, dash=""):
    return en(a, a.arrow(d, color, width, dash), t0, t1, still)


# ---------- salida
def escribir(a, name, title, desc, pcts):
    """Guarda site2/ilustraciones/mikrotik/<name> y deja la vista previa en ilustraciones/mikrotik/_rev-<stem>-<pct>.png."""
    p = a.save(SITE / name, title, desc)
    subprocess.run([sys.executable, "/home/claude/ies-training/tools/anim_preview.py", str(p), "--pct",
                    ",".join(str(x) for x in pcts)], check=True)
    kb = p.stat().st_size / 1024
    if kb > 120:
        print(f"AVISO: {name} pesa {kb:.0f} KB (más de 120)")
    return p


# ---------- diagramas de secuencia
def lifeline(a, x, y1, y2):
    return a.add(f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" stroke="{a.LINE}" stroke-width="2.5" stroke-dasharray="6 6"/>')


def msg(a, x1, x2, y, label, t, end, color=None, still=0, travel=2.5, lsize=15, dash="", sub=None, subcolor=None, lost=False, frac=0.55):
    """Mensaje de x1 a x2 en la altura y: sale en t% (un punto viaja) y queda dibujado hasta end%.
    lost=True: la flecha llega hasta la mitad y termina en una cruz (no hay respuesta)."""
    c = color or a.BLUE
    xm = (x1 + x2) / 2
    if lost:
        xe = x1 + (x2 - x1) * frac
        body = a.arrow(f"M{x1} {y} H{xe}", c, 3, dash or "6 5") + mark(a, xe + (14 if x2 > x1 else -14), y, ok=False, r=12)
        dest = xe
    else:
        tip = x2 - 2 if x2 > x1 else x2 + 2
        body = a.arrow(f"M{x1} {y} H{tip}", c, 3, dash)
        dest = x2
    lx = (x1 + dest) / 2 if lost else xm
    body += a.text(lx, y - 10, label, lsize, c, a.MONO, 600, "middle")
    if sub:
        body += a.text(xm, y + 22, sub, 14, subcolor or a.TXT, a.SANS, 400, "middle")
    en(a, body, t + travel * 0.7, end, still)
    mv = a.move([(0, x1, y), (t, x1, y), (t + travel, dest, y), (100, dest, y)])
    a.add(a.group(f'<circle cx="0" cy="0" r="8" fill="{c}"/>', mv, vis(a, [(t, t + travel + 0.3)], 0.3), still=0))


def head(a, x, y, title, sub="", w=220, kind="pc"):
    """Cabecera de una línea de vida, centrada en x."""
    dev(a, x - w / 2, y, w, 70 if sub else 50, title, sub, kind=kind, tsize=17, ssize=14)
