"""Ayudantes propios para las animaciones de Teoría de los cursos OmniAccess Intrusión y Filas.
No tocan anim.py ni ilus.py: se apoyan en ellas.

new()      -> Anim con kicker del curso
out()      -> guarda en site2/ilustraciones/<slug>/<id>-t<N>.svg y deja PNG en ilustraciones/<slug>/_t<id>-t<N>-*.png
box()      -> caja de ilus.py (título, subtítulo, ícono) como fragmento SVG
when()     -> fragmento visible entre dos instantes
travel()   -> píldora o punto que viaja de un punto a otro entre dos instantes
seq()      -> flecha que aparece en un instante y queda hasta otro
card()     -> tarjeta de nota con barra de color y varias líneas
check()    -> tilde o cruz en círculo
lane()     -> cabecera oscura con línea de vida (diagrama de secuencia)
"""
import sys
from pathlib import Path

sys.path.insert(0, "/home/claude/ies-training/tools")
from anim import Anim  # noqa: E402
import ilus  # noqa: E402

SLUG = Path(__file__).resolve().parent.parent.name
SITE = Path(f"/home/claude/ies-training/site2/ilustraciones/{SLUG}")
PREV = Path(f"/home/claude/ies-training/ilustraciones/{SLUG}")
KICK = {"omniaccess-intrusion": "OMNIACCESS INTRUSIÓN", "omniaccess-filas": "OMNIACCESS FILAS"}[SLUG]


def new(T, tema, title):
    return Anim(T=T, kicker=f"{KICK} · {tema}", title=title)


def out(a, lid, n, title, desc, pcts):
    for old in PREV.glob(f"_t{lid}-t{n}-*.png"):
        old.unlink()
    p = a.write(str(SITE / f"{lid}-t{n}.svg"), title, desc, preview=pcts, prefix=str(PREV / f"_t{lid}-t{n}"))
    kb = Path(p).stat().st_size / 1024
    assert kb < 120, f"{p} pesa {kb:.0f} KB"
    for stray in SITE.glob("*.png"):
        if stray.name.startswith(f"{lid}-t"):
            stray.unlink()
    return p


def box(x, y, w, h, title, sub="", icon=None, dark=False, hl=None):
    return ilus.Box(x, y, w, h, title, sub, dark=dark, icon=ilus.ICON[icon] if icon else None, hl=hl).svg()


def when(a, inner, t0, t1=100, still=0, fade=1.2):
    return a.add(a.group(inner, a.show(t0, t1, fade), still=still))


def pill0(a, label, fg, bg, size=15, h=30):
    """Píldora centrada en (0,0), para mover con translate."""
    w = int(len(label) * size * 0.62 + 26)
    return (a.box(-w / 2, -h / 2, w, h, bg, rx=h / 2)
            + a.text(0, h * 0.18 + 1, label, size, fg, a.MONO, 600, "middle"))


def travel(a, p1, p2, t0, t1, label=None, fg="#FFFFFF", bg=None, dot=None, hold=1.0, still=0, size=15, inner=None):
    bg = bg or a.CYAN
    if inner is None:
        inner = pill0(a, label, fg, bg, size) if label else f'<circle cx="0" cy="0" r="{dot or 9}" fill="{bg}"/>'
    mv = a.move([(0, *p1), (t0, *p1), (t1, *p2), (100, *p2)])
    return a.add(a.group(inner, mv, a.show(t0, min(t1 + hold, 100), 0.5), still=still))


def seq(a, d, t, until=100, color=None, label=None, lx=None, ly=None, still=1, dash="", lcolor=None, lsize=15, anchor="middle", width=3):
    inner = a.arrow(d, color or a.BLUE, width, dash)
    if label:
        inner += a.text(lx, ly, label, lsize, lcolor or color or a.BLUE, a.MONO, 600, anchor)
    return a.add(a.group(inner, a.show(t, until), still=still))


def card(a, x, y, w, lines, kind="info", title=None, size=16, lh=23):
    col = {"info": a.BLUE, "ok": a.OK, "bad": a.BAD, "amb": a.AMB}[kind]
    bg = {"info": a.WHITE, "ok": a.OKBG, "bad": a.BADBG, "amb": a.AMBBG}[kind]
    h = 20 + (26 if title else 0) + lh * len(lines)
    s = a.box(x, y, w, h, bg, a.LINE if kind == "info" else None, rx=10)
    s += f'<rect x="{x}" y="{y}" width="5" height="{h}" rx="2" fill="{col}"/>'
    yy = y + 29
    if title:
        s += a.text(x + 20, yy, title, 17, a.INK, a.SANS, 600)
        yy += 26
    for ln in lines:
        s += a.text(x + 20, yy, ln, size, a.TXT, a.SANS, 400)
        yy += lh
    return s


def check(a, cx, cy, ok=True, r=16):
    c = a.OK if ok else a.BAD
    bg = a.OKBG if ok else a.BADBG
    p = (f'<path d="M{cx - 7} {cy} l5 5 l9 -10" fill="none" stroke="{c}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>' if ok
         else f'<path d="M{cx - 6} {cy - 6} l12 12 M{cx + 6} {cy - 6} l-12 12" stroke="{c}" stroke-width="3" stroke-linecap="round"/>')
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{bg}" stroke="{c}" stroke-width="2"/>' + p


def lane(a, x, ytop, ybot, title, sub=None, w=220):
    h = 62 if sub else 48
    s = a.box(x - w / 2, ytop, w, h, a.INK, rx=12)
    if sub:
        s += a.text(x, ytop + 27, title, 18, a.WHITE, a.HEAD, 600, "middle")
        s += a.text(x, ytop + 49, sub, 15, "#9FC3E3", a.MONO, 400, "middle")
    else:
        s += a.text(x, ytop + 31, title, 18, a.WHITE, a.HEAD, 600, "middle")
    s += f'<line x1="{x}" y1="{ytop + h}" x2="{x}" y2="{ybot}" stroke="{a.GREY}" stroke-width="1.5" stroke-dasharray="4 6"/>'
    return a.add(s)


def person(a, cx, cy, color=None, s=1.0):
    """Persona vista de arriba o de frente, muy simple, centrada en (cx, cy)."""
    c = color or a.BLUE
    return (f'<circle cx="{cx}" cy="{cy - 14 * s}" r="{8 * s}" fill="{c}"/>'
            f'<path d="M{cx - 12 * s} {cy + 16 * s} Q{cx - 12 * s} {cy - 4 * s} {cx} {cy - 4 * s} Q{cx + 12 * s} {cy - 4 * s} {cx + 12 * s} {cy + 16 * s} z" fill="{c}"/>')
