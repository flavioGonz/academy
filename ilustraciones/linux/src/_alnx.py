"""Ayudas para las animaciones de teoría del curso Linux (sobre tools/anim.py)."""
import sys
sys.path.insert(0, "/home/claude/ies-training/tools")
from anim import Anim  # noqa

SITE = "/home/claude/ies-training/site2/ilustraciones/linux/"
PREV = "/home/claude/ies-training/ilustraciones/linux/_anim-"
KICK = "LINUX · TEORÍA"
NOLIG = "<style>text{font-variant-ligatures:none;font-feature-settings:'calt' 0,'liga' 0}</style>"


def new(T, title):
    a = Anim(T=T, kicker=KICK, title=title)
    a.add(NOLIG)
    return a


def at(a, svg, start=0, end=100, still=1):
    """Agrega svg visible entre start% y end%."""
    a.add(a.group(svg, a.show(start, end), still=still))


def card(a, x, y, w, h, title=None, sub=None, fill=None, stroke=None, tsize=19, dark=False):
    fill = fill or (a.INK if dark else a.WHITE)
    stroke = stroke or (a.INK if dark else a.LINE)
    s = a.box(x, y, w, h, fill, stroke, rx=14, sw=2)
    if title:
        s += a.text(x + 20, y + 34, title, tsize, a.WHITE if dark else a.INK, a.HEAD, 600)
    if sub:
        s += a.text(x + 20, y + 58, sub, 15, "#9FC3E3" if dark else a.GREY, a.MONO, 400)
    return s


def chip(a, x, y, label, kind="info", size=15, anchor="start", h=30):
    fg, bg = {"info": (a.BLUE, "#E5F0FB"), "ok": (a.OK, a.OKBG), "bad": (a.BAD, a.BADBG), "amb": (a.AMB, a.AMBBG),
              "grey": (a.GREY, a.SLATE), "dark": ("#FFFFFF", a.NAVY2), "cyan": ("#FFFFFF", a.CYAN)}[kind]
    return a.pill(x, y, label, fg, bg, size, h, anchor)


def line(a, d, color=None, w=4, dash=""):
    da = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<path d="{d}" fill="none" stroke="{color or a.BLUE}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"{da}/>'


def dot(a, x, y, r=10, color=None):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color or a.CYAN}"/>'


def caption(a, y, items, still=0):
    """Texto de pie que cambia por tramo: items = [(desde, hasta, texto, color)]."""
    for i, (s, e, t, col) in enumerate(items):
        at(a, a.text(48, y, t, 18, col or a.INK, a.SANS, 600), s, e, still=1 if i == still else 0)


def write(a, name, title, desc, pcts=(12, 37, 62, 87)):
    r = a.write(SITE + name, title, desc, preview=list(pcts), prefix=PREV + name.replace(".svg", ""))
    montage(name)
    return r


def montage(name):
    """Une los cuadros de vista previa en una sola imagen para revisar (ilustraciones/linux/_mont-<id>.png)."""
    from PIL import Image
    import glob
    base = PREV + name.replace(".svg", "")
    fs = sorted(glob.glob(base + "-*.png"), key=lambda f: (f.endswith("fijo.png"), int(f.rsplit("-", 1)[1][:-4]) if not f.endswith("fijo.png") else 0))
    W, H = 900, 506
    m = Image.new("RGB", (W * 2, H * 3), "white")
    for i, f in enumerate(fs[:6]):
        im = Image.open(f).convert("RGB").resize((W, H))
        m.paste(im, ((i % 2) * W, (i // 2) * H))
    out = "/home/claude/ies-training/ilustraciones/linux/_mont-" + name.replace(".svg", ".png")
    m.save(out)
    print("montaje", out)


# ---------------------------------------------------------------- piezas Linux para animaciones
T_CMD, T_OUT, T_PR, T_OK, T_ERR, T_COM, T_WARN = "#FFFFFF", "#9FC3E3", "#5FD3F3", "#5BD69B", "#FF8A73", "#7FA6C9", "#FFC861"


def nb(s):
    s = " " * (len(s) - len(s.lstrip(" "))) + s.lstrip(" ")
    return s.replace("  ", "  ")


def term(a, x, y, w, rows, title=None, size=15, lh=25, h=None):
    """Terminal oscura. rows: '$ comando' o (texto, color). Devuelve svg."""
    top = 32 if title else 14
    hh = h or (top + len(rows) * lh + 12)
    out = [a.box(x, y, w, hh, "#03213C", None, rx=12)]
    if title:
        out.append(a.text(x + 16, y + 22, title, 13, "#7FA6C9", a.MONO, 500, extra='letter-spacing="1.5"'))
    for i, r in enumerate(rows):
        yy = y + top + 4 + (i + 0.6) * lh
        out.append(trow(a, x, yy, r, size))
    return "".join(out)


def trow(a, x, yy, r, size=15):
    if isinstance(r, str) and r.startswith("$ "):
        return a.text(x + 16, yy, "$", size, T_PR, a.MONO, 600) + a.text(x + 16 + size * 1.2, yy, nb(r[2:]), size, T_CMD, a.MONO, 500)
    s, col = (r, T_OUT) if isinstance(r, str) else r
    return a.text(x + 16, yy, nb(s), size, col, a.MONO, 500)


def mono(a, x, y, s, size=16, color=None, weight=600, anchor="start"):
    return a.text(x, y, nb(s), size, color or a.INK, a.MONO, weight, anchor)


def pkt(a, label, color=None, w=None):
    """Paquete (rectángulo redondeado con texto) centrado en 0,0 para mover con a.move."""
    w = w or int(len(label) * 9.5 + 26)
    c = color or a.BLUE
    return a.box(-w / 2, -16, w, 32, c, "#FFFFFF", rx=16, sw=2) + a.text(0, 6, label, 15, "#FFFFFF", a.MONO, 700, "middle")
