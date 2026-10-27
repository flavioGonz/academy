"""Ayudas propias para las ilustraciones de MikroTik 12 a 22 (no modifica ilus.py)."""
import sys
sys.path.insert(0, "/home/claude/ies-training/tools")
from ilus import *  # noqa: F401,F403
from ilus import e, text, wrap

OUT = "/home/claude/ies-training/ilustraciones/mikrotik/"


def panel(x, y, w, h, title=None, kind="info", sub=None):
    """Tarjeta con encabezado de color (info, ok, warn, alert, dark)."""
    bg, fg = {"info": (WHITE, BLUE), "ok": (OK_BG, OK), "warn": (WARN_BG, WARN), "alert": (ALERT_BG, ALERT),
              "dark": (DEEP, CYAN), "soft": (SOFT, BLUE)}[kind]
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{bg}" stroke="{LINE2 if kind in ("info", "soft") else fg}" stroke-width="{2 if kind in ("info", "soft") else 2}"/>']
    if title:
        out.append(text(x + 20, y + 34, title, 19, 600, WHITE if kind == "dark" else (INK if kind in ("info", "soft") else fg), FD))
    if sub:
        out.append(text(x + 20, y + 58, sub, 15, 400, "#9FC3E3" if kind == "dark" else INK3, FM))
    return "".join(out)


def para(x, y, s, w, size=16, color=INK2, weight=400, font=FB, lh=1.35, anchor="start"):
    return wrap(x, y, s, w, size, weight, color, font, lh, anchor)[0]


def mono(x, y, s, size=15, color=INK, weight=500, anchor="start"):
    return text(x, y, s, size, weight, color, FM, anchor)


def pill(x, y, w, h, s, fill=BLUE, fg=WHITE, size=15, font=FM, weight=600, stroke=None):
    st = f' stroke="{stroke}" stroke-width="2"' if stroke else ""
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{min(h / 2, 12)}" fill="{fill}"{st}/>'
            + text(x + w / 2, y + h / 2 + size * 0.36, s, size, weight, fg, font, anchor="middle"))


def sparkline(x, y, w, h, values, color=BLUE, fill=None, base=True):
    """Serie de tasas (0..1) dibujada como área."""
    n = len(values)
    pts = [(x + i * w / (n - 1), y + h - v * h) for i, v in enumerate(values)]
    d = "M" + " L".join(f"{px:.1f} {py:.1f}" for px, py in pts)
    out = []
    if base:
        out.append(f'<path d="M{x} {y + h}H{x + w}" stroke="{LINE2}" stroke-width="1.5"/>')
    area = d + f" L{x + w:.1f} {y + h:.1f} L{x:.1f} {y + h:.1f}Z"
    out.append(f'<path d="{area}" fill="{fill or color}" opacity=".16"/>')
    out.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="3" stroke-linejoin="round"/>')
    return "".join(out)


def file_icon(x, y, name, sub=None, color=BLUE, w=64, h=80):
    """Ícono de archivo con nombre debajo."""
    out = [f'<path d="M{x} {y + 8}a8 8 0 0 1 8 -8h{w - 26}l18 18v{h - 26}a8 8 0 0 1 -8 8h-{w - 16}a8 8 0 0 1 -8 -8z" fill="{WHITE}" stroke="{color}" stroke-width="2.5"/>',
           f'<path d="M{x + w - 18} {y}v18h18" fill="none" stroke="{color}" stroke-width="2.5"/>',
           text(x + w / 2, y + h + 26, name, 15, 600, INK, FM, anchor="middle")]
    if sub:
        out.append(text(x + w / 2, y + h + 48, sub, 14, 400, INK3, FM, anchor="middle"))
    return "".join(out)


def line(x1, y1, x2, y2, color=LINE2, sw=2, dash=None):
    ds = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<path d="M{x1} {y1}L{x2} {y2}" stroke="{color}" stroke-width="{sw}"{ds} fill="none"/>'


def pipe(x, y, w, h, color, label=None, label_color=None, fill_op=.10, size=15, dash=None):
    """Tubo horizontal (capa de túnel) con etiqueta a la izquierda adentro."""
    ds = f' stroke-dasharray="{dash}"' if dash else ""
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h / 2}" fill="{color}" fill-opacity="{fill_op}" stroke="{color}" stroke-width="2.5"{ds}/>']
    if label:
        out.append(text(x + h / 2 + 4, y + 22, label, size, 600, label_color or color, FM))
    return "".join(out)


def badge(x, y, n, color=CYAN):
    return Step(x, y, n, color).svg()


def mark(x, y, ok=True):
    return Mark(x, y, ok)


def save(c, name):
    return c.save(OUT + name)
