"""Ayudas de dibujo propias del curso OmniAccess LPR. No modifica ilus.py: solo suma piezas.

Kicker sin número de lección ("OmniAccess LPR" o "OmniAccess LPR · Paso N") para que las imágenes
sigan siendo correctas si el curso se reordena por módulos. Todo es esquemático: nada de capturas
reales de la interfaz ni datos reales (IPs 192.0.2.x, matrículas de ejemplo).
"""
import sys
sys.path.insert(0, "/home/claude/ies-training/tools")
from ilus import *  # noqa
from ilus import text, wrap, e, Node  # noqa

OUT = "/home/claude/ies-training/ilustraciones/omniaccess-lpr/"
AMBER = "#D99A06"


def K(paso=None):
    return "OmniAccess LPR" + (f" · Paso {paso}" if paso else "")


def save(c, name):
    return c.save(OUT + name)


KC = {"info": (WHITE, BLUE), "ok": (OK_BG, OK), "warn": (WARN_BG, WARN), "alert": (ALERT_BG, ALERT),
      "gray": (WHITE, INK3), "cyan": (WHITE, CYAN), "soft": (SOFT, BLUE), "dark": (DEEP, CYAN)}


def panel(x, y, w, h, title=None, kind="info", sub=None, title_size=18):
    bg, fg = KC[kind]
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{bg}" stroke="{fg if kind != "info" else LINE2}" stroke-width="2"/>']
    if title:
        col = WHITE if kind == "dark" else (fg if kind not in ("info", "soft", "gray", "cyan") else INK)
        out.append(text(x + 20, y + 32, title, title_size, 600, col, FD))
    if sub:
        out.append(text(x + 20, y + 56, sub, 15, 400, "#9FC3E3" if kind == "dark" else INK3, FM))
    return "".join(out)


def pill(x, y, s, fg=BLUE, bg=WHITE, size=15, mono=True, anchor="middle", bold=600):
    w = len(s) * (size * (0.6 if mono else 0.53)) + 24
    x0 = x - w / 2 if anchor == "middle" else x
    return (f'<rect x="{x0:.1f}" y="{y - size - 5:.1f}" width="{w:.1f}" height="{size + 13}" rx="{(size + 13) / 2:.1f}" fill="{bg}" stroke="{fg}" stroke-width="1.5"/>'
            + text(x0 + w / 2, y, s, size, bold, fg, FM if mono else FB, anchor="middle"))


def code(x, y, w, s, size=15, color="#D9E9F8", h=40):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#03213C"/>' + text(x + 16, y + h / 2 + size * 0.35, s, size, 500, color, FM)


def codebox(x, y, w, lines, size=15, lh=26, title=None):
    top = 30 if title else 14
    h = top + len(lines) * lh + 10
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="#03213C"/>']
    if title:
        out.append(text(x + 16, y + 22, title, 13, 500, "#7FA6C9", FM, ls=1.5))
    for i, ln in enumerate(lines):
        s, col = (ln, "#D9E9F8") if isinstance(ln, str) else ln
        out.append(text(x + 16, y + top + 4 + (i + 0.6) * lh, s, size, 500, col, FM))
    return "".join(out), h


def wire(points, kind="flow", arrow=True, dash=None):
    col, sw, d0 = Cable.STY[kind]
    dash = dash or d0
    d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in points)
    mk = {BLUE: "a-blue", CYAN: "a-cyan", INK3: "a-gray", OK: "a-ok", ALERT: "a-alert"}.get(col, "a-blue")
    return f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round"' + (f' stroke-dasharray="{dash}"' if dash else "") + (f' marker-end="url(#{mk})"' if arrow else "") + "/>"


def icon(x, y, name, color=BLUE, scale=1.2, sw=1.8):
    return f'<g transform="translate({x} {y}) scale({scale})" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">{ICON[name]}</g>'


def plate(x, y, s="SBA 1234", w=170, size=26, stroke=INK):
    """Patente genérica (rectángulo blanco con franja superior), centrada en x. y = borde superior."""
    h = w * 0.33
    x0 = x - w / 2
    return (f'<rect x="{x0:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="6" fill="{WHITE}" stroke="{stroke}" stroke-width="2.5"/>'
            f'<rect x="{x0 + 2:.1f}" y="{y + 2:.1f}" width="{w - 4:.1f}" height="{h * 0.2:.1f}" rx="4" fill="{BLUE}"/>'
            + text(x, y + h * 0.82, s, size, 700, INK, FM, anchor="middle"))


def barrier(x, y, up=False, color=INK2):
    """Barrera vehicular vista de costado: gabinete + brazo. (x, y) = base del gabinete."""
    out = [f'<rect x="{x}" y="{y - 70}" width="34" height="70" rx="6" fill="{WHITE}" stroke="{color}" stroke-width="2.5"/>']
    if up:
        out.append(f'<path d="M{x + 17} {y - 60} L{x + 60} {y - 170}" stroke="{OK}" stroke-width="8" stroke-linecap="round"/>')
    else:
        out.append(f'<path d="M{x + 17} {y - 60} H{x + 190}" stroke="{ALERT}" stroke-width="8" stroke-linecap="round" stroke-dasharray="22 12"/>')
    return "".join(out)


def cam_icon(x, y, s=1.0, color=DEEP):
    """Cámara bullet de costado mirando a la derecha (x, y = punto de montaje)."""
    return (f'<g transform="translate({x} {y}) scale({s})">'
            f'<rect x="0" y="-14" width="74" height="30" rx="7" fill="{color}"/>'
            f'<rect x="70" y="-10" width="14" height="22" rx="3" fill="#0B3A66"/>'
            f'<path d="M-6 -20 H82" stroke="{color}" stroke-width="5" stroke-linecap="round"/>'
            f'<circle cx="62" cy="1" r="5" fill="{CYAN}"/></g>')


def car_side(x, y, w=230, color="#5B6F84", facing="left"):
    """Auto de costado, simple. (x, y) = esquina inferior izquierda de las ruedas."""
    h = w * 0.3
    body = f'<path d="M{x} {y - 22} q0 -{h * 0.45:.0f} {w * 0.12:.0f} -{h * 0.5:.0f} l{w * 0.16:.0f} -{h * 0.45:.0f} h{w * 0.42:.0f} l{w * 0.14:.0f} {h * 0.45:.0f} q{w * 0.16:.0f} 0 {w * 0.16:.0f} {h * 0.5:.0f} v{h * 0.15:.0f} z" fill="{color}"/>'
    win = f'<path d="M{x + w * 0.31:.0f} {y - 22 - h * 0.5:.0f} l{w * 0.06:.0f} -{h * 0.35:.0f} h{w * 0.33:.0f} l{w * 0.1:.0f} {h * 0.35:.0f} z" fill="#C2D4E6"/>'
    wh = f'<circle cx="{x + w * 0.2:.0f}" cy="{y - 10}" r="{w * 0.075:.0f}" fill="{INK}"/><circle cx="{x + w * 0.8:.0f}" cy="{y - 10}" r="{w * 0.075:.0f}" fill="{INK}"/>'
    g = body + win + wh
    if facing == "right":
        return f'<g transform="translate({2 * x + w} 0) scale(-1 1)">{g}</g>'
    return g


def bars(x, y, w, h, vals, labels=None, lo=85, hi=95, top=100, label_every=3):
    """Barras de porcentaje (0..top) coloreadas: verde >= hi, ámbar entre lo y hi, rojo < lo."""
    n = len(vals)
    bw = w / n
    out = [f'<path d="M{x} {y + h}H{x + w}" stroke="{INK3}" stroke-width="1.5"/>']
    for k, ref in ((lo, ALERT), (hi, OK)):
        yy = y + h - h * k / top
        out.append(f'<path d="M{x} {yy:.1f}H{x + w}" stroke="{ref}" stroke-width="1.2" stroke-dasharray="6 5" opacity=".8"/>')
    for i, v in enumerate(vals):
        col = OK if v >= hi else (AMBER if v >= lo else ALERT)
        bh = h * v / top
        out.append(f'<rect x="{x + i * bw + 2:.1f}" y="{y + h - bh:.1f}" width="{bw - 4:.1f}" height="{bh:.1f}" rx="2" fill="{col}"/>')
        if labels and i % label_every == 0:
            out.append(text(x + i * bw + bw / 2, y + h + 22, labels[i], 14, 500, INK3, FM, anchor="middle"))
    return "".join(out)


def tag(x, y, s, kind="ok", size=16, anchor="start"):
    """Chip de estado con texto (verde/ámbar/rojo/gris) sin depender solo del color."""
    bg, fg = {"ok": (OK_BG, OK), "warn": (WARN_BG, WARN), "alert": (ALERT_BG, ALERT), "gray": (SOFT, INK2), "blue": (SOFT, BLUE)}[kind]
    w = len(s) * size * 0.56 + 26
    x0 = x - w / 2 if anchor == "middle" else x
    return f'<rect x="{x0:.1f}" y="{y - size - 6:.1f}" width="{w:.1f}" height="{size + 14}" rx="{(size + 14) / 2:.1f}" fill="{bg}" stroke="{fg}" stroke-width="1.5"/>' + text(x0 + w / 2, y, s, size, 600, fg, FB, anchor="middle")


def card(x, y, w, h, status="ok", label="AUTORIZADO", pl="SBA 1234", sub=None):
    """Tarjeta esquemática de una lectura en el monitor (sin datos reales)."""
    fg = {"ok": OK, "warn": AMBER, "alert": ALERT, "gray": INK3, "yellow": "#B8860B"}[status]
    bg = {"ok": OK_BG, "warn": WARN_BG, "alert": ALERT_BG, "gray": SOFT, "yellow": "#FFF8D6"}[status]
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{bg}" stroke="{fg}" stroke-width="{3 if status == "alert" else 2}"/>',
           f'<rect x="{x + 12}" y="{y + 12}" width="{h - 24}" height="{h - 24}" rx="8" fill="#0B1A28"/>',
           text(x + h + 2, y + 34, pl, 19, 700, INK, FM),
           text(x + h + 2, y + 60, label, 15, 700, fg, FB, ls=0.5)]
    if sub:
        out.append(text(x + h + 2, y + 82, sub, 14, 400, INK2, FB))
    return "".join(out)
