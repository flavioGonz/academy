"""Ayudas para las animaciones de teoría del curso VMware (sobre tools/anim.py). Mismo esquema que Paradox."""
import sys
sys.path.insert(0, "/home/claude/ies-training/tools")
from anim import Anim  # noqa

SITE = "/home/claude/ies-training/site2/ilustraciones/vmware/"
PREV = "/home/claude/ies-training/ilustraciones/vmware/_anim-"
KICK = "VMWARE · TEORÍA"
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


def vmbox(a, x, y, w=150, h=60, title="VM", sub=None, fill=None, stroke=None, tcol=None):
    s = a.box(x, y, w, h, fill or a.WHITE, stroke or a.LINE, rx=12, sw=2)
    s += f'<rect x="{x + 14}" y="{y + 14}" width="24" height="18" rx="3" fill="none" stroke="{a.BLUE}" stroke-width="2"/>'
    if sub:
        s += a.text(x + 48, y + h / 2 - 2, title, 16, tcol or a.INK, a.SANS, 600) + a.text(x + 48, y + h / 2 + 17, sub, 14, a.GREY, a.MONO)
    else:
        s += a.text(x + 48, y + h / 2 + 6, title, 16, tcol or a.INK, a.SANS, 600)
    return s


def caption(a, y, items, still=0):
    """Texto de pie que cambia por tramo: items = [(desde, hasta, texto, color)]."""
    for i, (s, e, t, col) in enumerate(items):
        at(a, a.text(48, y, t, 18, col or a.INK, a.SANS, 600), s, e, still=1 if i == still else 0)


def write(a, name, title, desc, pcts=(12, 37, 62, 87)):
    r = a.write(SITE + name, title, desc, preview=list(pcts), prefix=PREV + name.replace(".svg", ""))
    montage(name)
    return r


def montage(name):
    """Une los cuadros de vista previa en una sola imagen para revisar (ilustraciones/vmware/_mont-<id>.png)."""
    from PIL import Image
    import glob
    base = PREV + name.replace(".svg", "")
    fs = sorted(glob.glob(base + "-*.png"), key=lambda f: (f.endswith("fijo.png"), int(f.rsplit("-", 1)[1][:-4]) if not f.endswith("fijo.png") else 0))
    W, H = 900, 506
    m = Image.new("RGB", (W * 2, H * 3), "white")
    for i, f in enumerate(fs[:6]):
        im = Image.open(f).convert("RGB").resize((W, H))
        m.paste(im, ((i % 2) * W, (i // 2) * H))
    out = "/home/claude/ies-training/ilustraciones/vmware/_mont-" + name.replace(".svg", ".png")
    m.save(out)
    print("montaje", out)
