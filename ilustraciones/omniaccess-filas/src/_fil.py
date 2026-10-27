"""Ayudas de dibujo del curso OmniAccess Filas. No modifica ilus.py: solo suma piezas."""
import sys
sys.path.insert(0, "/home/claude/ies-training/tools")
from ilus import *  # noqa
from ilus import text, wrap, e  # noqa

OUT = "/home/claude/ies-training/ilustraciones/omniaccess-filas/"


def save(c, name):
    return c.save(OUT + name)


KC = {"info": (WHITE, BLUE), "ok": (OK_BG, OK), "warn": (WARN_BG, WARN), "alert": (ALERT_BG, ALERT),
      "gray": (WHITE, INK3), "cyan": (WHITE, CYAN), "soft": (SOFT, BLUE), "dark": (DEEP, CYAN)}


def panel(x, y, w, h, title=None, kind="info", sub=None, title_size=18):
    bg, fg = KC[kind]
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{bg}" stroke="{fg if kind not in ("info",) else LINE2}" stroke-width="2"/>']
    if title:
        col = WHITE if kind == "dark" else (fg if kind not in ("info", "soft") else INK)
        out.append(text(x + 20, y + 32, title, title_size, 600, col, FD))
    if sub:
        out.append(text(x + 20, y + 56, sub, 15, 400, "#9FC3E3" if kind == "dark" else INK3, FM))
    return "".join(out)


def pill(x, y, s, fg=BLUE, bg=WHITE, size=15, mono=True, anchor="middle", bold=600):
    w = len(s) * (size * (0.6 if mono else 0.52)) + 24
    x0 = x - w / 2 if anchor == "middle" else x
    return (f'<rect x="{x0:.1f}" y="{y - size - 5:.1f}" width="{w:.1f}" height="{size + 13}" rx="{(size + 13) / 2:.1f}" fill="{bg}" stroke="{fg}" stroke-width="1.5"/>'
            + text(x0 + w / 2, y, s, size, bold, fg, FM if mono else FB, anchor="middle"))


def code(x, y, w, s, size=15, color="#D9E9F8", h=40):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#03213C"/>' + text(x + 16, y + h / 2 + size * 0.35, s, size, 500, color, FM)


def person(cx, cy, col=BLUE, r=13):
    """Persona vista desde arriba o de frente, muy simple: cabeza y hombros."""
    return (f'<circle cx="{cx}" cy="{cy - r * 1.1:.1f}" r="{r * 0.62:.1f}" fill="{col}"/>'
            f'<path d="M{cx - r} {cy + r * 0.9:.1f}a{r} {r} 0 0 1 {2 * r} 0z" fill="{col}"/>')


def head_top(cx, cy, col=BLUE, r=12):
    """Persona vista desde arriba: hombros (elipse) y cabeza (círculo)."""
    return (f'<ellipse cx="{cx}" cy="{cy}" rx="{r * 1.5:.1f}" ry="{r * 0.8:.1f}" fill="{col}" opacity=".35"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r * 0.62:.1f}" fill="{col}"/>')


def poly(points, stroke=BLUE, fill="none", sw=3, dash=None, opacity=1):
    d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in points)
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round"' + (f' stroke-dasharray="{dash}"' if dash else "") + f' opacity="{opacity}"/>'


def rect(x, y, w, h, fill=WHITE, stroke=LINE2, sw=2, rx=12, dash=None, opacity=1):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"' + (f' stroke-dasharray="{dash}"' if dash else "") + f' opacity="{opacity}"/>'


def line(x1, y1, x2, y2, col=LINE2, sw=2, dash=None, arrow=None):
    mk = {BLUE: "a-blue", CYAN: "a-cyan", INK3: "a-gray", OK: "a-ok", ALERT: "a-alert"}.get(col, "a-blue")
    return f'<path d="M{x1:.1f} {y1:.1f}L{x2:.1f} {y2:.1f}" stroke="{col}" stroke-width="{sw}" fill="none"' + (f' stroke-dasharray="{dash}"' if dash else "") + (f' marker-end="url(#{mk})"' if arrow else "") + "/>"
