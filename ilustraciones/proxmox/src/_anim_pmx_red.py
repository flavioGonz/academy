"""Ayudantes para las animaciones "Cómo se ve en la red" (Resumen, <id>-r1.svg) y de Laboratorio
(<id>-l1.svg, <id>-l2.svg) del curso Proxmox VE.

Se apoyan en tools/anim.py (no lo modifican) y siguen el estilo de las animaciones nuevas de MikroTik
(ilustraciones/mikrotik/src/_anim_red_1_9.py): equipos con icono, paquetes que viajan, mensajes de
diagrama de secuencia, terminal oscura, frases de estado que se alternan, y revisión con tools/anim_preview.py.
Tiempos en porcentaje del ciclo (0 a 100). `still` es la opacidad en el cuadro fijo (movimiento reducido).
"""
import glob
import math
import subprocess
import sys

sys.path.insert(0, "/home/claude/ies-training/tools")
from anim import Anim  # noqa: E402,F401
from ilus import ICON  # noqa: E402

SITE = "/home/claude/ies-training/site2/ilustraciones/proxmox"
REV = "/home/claude/ies-training/ilustraciones/proxmox"
TOOLS = "/home/claude/ies-training/tools"
NOLIG = "<style>text{font-variant-ligatures:none;font-feature-settings:'calt' 0,'liga' 0}</style>"

SKY = "#9FC3E3"     # texto secundario sobre fondo oscuro
GOLD = "#FFD28A"    # atención sobre fondo oscuro
MINT = "#5BE0A5"    # correcto sobre fondo oscuro
CORAL = "#FF9E8A"   # peligro sobre fondo oscuro


def new(T, tema, title, lab=False):
    k = "PROXMOX VE · " + tema.upper() + (" · LABORATORIO" if lab else " · CÓMO SE VE EN LA RED")
    a = Anim(T=T, kicker=k, title=title)
    a.add(NOLIG)
    return a


# ---------- tiempo
def still_only(a, inner):
    """Visible solo en el cuadro fijo."""
    return a.group(inner, a.keyframes([(0, 0), (100, 0)]), still=1)


def during(a, inner, t0, t1=100, still=0, fade=1.0):
    """Visible entre t0 y t1."""
    return a.group(inner, a.show(t0, t1, fade), still=still)


def at(a, inner, t0, t1=100, still=0):
    a.add(during(a, inner, t0, t1, still))


# ---------- piezas
def glyph(a, name, x, y, color=None, scale=1.35, sw=1.8):
    """Icono de ilus.py (24x24) con la esquina superior izquierda en (x, y)."""
    return (f'<g transform="translate({x} {y}) scale({scale})" fill="none" stroke="{color or a.BLUE}" '
            f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">{ICON[name]}</g>')


def dev(a, x, y, w, h, title, sub="", icon=None, dark=False, sub2="", tsize=19, ssize=15, stroke=None, sw=2, fill=None):
    """Equipo: caja con icono a la izquierda, título y una o dos líneas mono."""
    fill = fill or (a.INK if dark else a.WHITE)
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


def pkt(a, label, fill=None, fg=None, size=15, h=34):
    """Píldora centrada en (0,0), para mover con travel()."""
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


def go(a, label, pts, t0, t1, color=None, hold=2.0, fg=None, size=15):
    a.add(travel(a, pkt(a, label, color or a.CYAN, fg, size), pts, t0, t1, hold))


def place(a, inner, x, y):
    return f'<g transform="translate({x},{y})">{inner}</g>'


def xmark(a, x, y, r=15):
    d = r * 0.42
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="{a.WHITE}" stroke="{a.BAD}" stroke-width="2.5"/>'
            f'<path d="M{x - d} {y - d} L{x + d} {y + d} M{x + d} {y - d} L{x - d} {y + d}" stroke="{a.BAD}" stroke-width="3" stroke-linecap="round"/>')


def check(a, x, y, r=15):
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="{a.WHITE}" stroke="{a.OK}" stroke-width="2.5"/>'
            f'<path d="M{x - r * .45} {y + r * .02} L{x - r * .1} {y + r * .38} L{x + r * .48} {y - r * .35}" fill="none" stroke="{a.OK}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>')


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
    """Terminal oscura con líneas de texto mono. colors: {índice: color}."""
    h = h or (22 + (24 if title else 0) + lh * len(lines))
    s = a.box(x, y, w, h, a.INK, rx=12)
    yy = y + 30
    if title:
        s += a.text(x + 18, yy, title, 13, SKY, a.MONO, 400, extra='letter-spacing="1.8"')
        yy += 26
    for i, ln in enumerate(lines):
        c = (colors or {}).get(i, a.WHITE)
        s += a.text(x + 18, yy, ln, size, c, a.MONO, extra='xml:space="preserve"')
        yy += lh
    return s


def tline(a, x, y, s, color=None, size=15):
    """Una línea de terminal (para hacerla aparecer sola)."""
    return a.text(x, y, s, size, color or a.WHITE, a.MONO, extra='xml:space="preserve"')


def line(x1, y1, x2, y2, color, w=3, dash=""):
    da = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{w}"{da} stroke-linecap="round"/>'


def path(d, color, w=3, dash=""):
    da = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{w}"{da} stroke-linecap="round" stroke-linejoin="round"/>'


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


def chip(a, x, y, label, kind="info", size=15, anchor="start", h=30):
    fg, bg = {"info": (a.BLUE, "#E5F0FB"), "ok": (a.OK, a.OKBG), "bad": (a.BAD, a.BADBG), "amb": (a.AMB, a.AMBBG),
              "grey": (a.GREY, a.SLATE), "dark": ("#FFFFFF", a.NAVY2), "cyan": ("#FFFFFF", a.CYAN)}[kind]
    return a.pill(x, y, label, fg, bg, size, h, anchor)


def blocks(a, x, y, labels, w=54, h=44, gap=8, fill=None, fg=None, stroke=None, size=16):
    """Fila de bloques con letra (discos, trozos, páginas)."""
    s = ""
    for i, lb in enumerate(labels):
        bx = x + i * (w + gap)
        s += a.box(bx, y, w, h, fill or a.WHITE, stroke or a.LINE, rx=8, sw=2)
        if lb:
            s += a.text(bx + w / 2, y + h / 2 + 6, lb, size, fg or a.INK, a.MONO, 600, "middle")
    return s


def bar(a, x, y, w, h, frac, color, bg="#E6EDF4"):
    return a.box(x, y, w, h, bg, rx=h / 2) + (a.box(x, y, max(w * frac, h), h, color, rx=h / 2) if frac > 0 else "")


def write(a, lid, kind, title, desc, pcts):
    """Guarda site2/ilustraciones/proxmox/<lid>-<kind>.svg, deja _rev-<lid>-<kind>-<pct>.png y un montaje."""
    p = a.save(f"{SITE}/{lid}-{kind}.svg", title, desc)
    subprocess.run([sys.executable, f"{TOOLS}/anim_preview.py", str(p), "--pct", ",".join(str(x) for x in pcts)], check=True)
    montage(f"{lid}-{kind}", pcts)
    return p


def montage(stem, pcts):
    """Une los cuadros de revisión en una sola imagen (ilustraciones/proxmox/_mont-<stem>.png)."""
    from PIL import Image
    fs = [f"{REV}/_rev-{stem}-{int(p)}.png" for p in pcts] + [f"{REV}/_rev-{stem}-fijo.png"]
    W, H = 900, 506
    rows = (len(fs) + 1) // 2
    m = Image.new("RGB", (W * 2, H * rows), "white")
    for i, f in enumerate(fs):
        im = Image.open(f).convert("RGB").resize((W, H))
        m.paste(im, ((i % 2) * W, (i // 2) * H))
    out = f"{REV}/_mont-{stem}.png"
    m.save(out)
    print("montaje", out)
