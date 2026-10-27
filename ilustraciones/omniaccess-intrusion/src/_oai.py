"""Ayudas de dibujo del curso OmniAccess Intrusión (copiadas de akuvox/src/_akv.py). No modifica ilus.py: solo suma piezas."""
import sys
sys.path.insert(0, "/home/claude/ies-training/tools")
from ilus import *  # noqa
from ilus import text, wrap, e  # noqa

OUT = "/home/claude/ies-training/ilustraciones/omniaccess-intrusion/"


def save(c, name):
    return c.save(OUT + name)


KC = {"info": (WHITE, BLUE), "ok": (OK_BG, OK), "warn": (WARN_BG, WARN), "alert": (ALERT_BG, ALERT),
      "gray": (WHITE, INK3), "cyan": (WHITE, CYAN), "soft": (SOFT, BLUE)}


def panel(x, y, w, h, title=None, kind="info", sub=None, title_size=18):
    """Tarjeta con borde de color y título arriba a la izquierda."""
    bg, fg = KC[kind]
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{bg}" stroke="{fg if kind != "info" else LINE2}" stroke-width="2"/>']
    if title:
        out.append(text(x + 20, y + 32, title, title_size, 600, fg if kind not in ("info", "soft") else INK, FD))
    if sub:
        out.append(text(x + 20, y + 56, sub, 15, 400, INK3, FM))
    return "".join(out)


def pill(x, y, s, fg=BLUE, bg=WHITE, size=15, mono=True, anchor="middle", bold=600):
    """Etiqueta con borde (como las de los cables)."""
    w = len(s) * (size * (0.6 if mono else 0.52)) + 24
    x0 = x - w / 2 if anchor == "middle" else x
    return (f'<rect x="{x0:.1f}" y="{y - size - 5:.1f}" width="{w:.1f}" height="{size + 13}" rx="{(size + 13) / 2:.1f}" fill="{bg}" stroke="{fg}" stroke-width="1.5"/>'
            + text(x0 + w / 2, y, s, size, bold, fg, FM if mono else FB, anchor="middle"))


def code(x, y, w, s, size=15, color="#D9E9F8", h=40):
    """Línea de código o URL sobre fondo oscuro."""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#03213C"/>' + text(x + 16, y + h / 2 + size * 0.35, s, size, 500, color, FM)


def code_parts(x, y, parts, size=16, h=44, pad=16):
    """URL en una línea con tramos de color: parts = [(texto, color), ...]. Devuelve (svg, lista de (x0, x1) por tramo)."""
    k = size * 0.6
    w = sum(len(p) for p, _ in parts) * k + 2 * pad
    out = [f'<rect x="{x}" y="{y}" width="{w:.0f}" height="{h}" rx="10" fill="#03213C"/>']
    cx, spans = x + pad, []
    for p, col in parts:
        out.append(text(cx, y + h / 2 + size * 0.35, p, size, 500, col, FM))
        spans.append((cx, cx + len(p) * k))
        cx += len(p) * k
    return "".join(out), spans


def terminal(x, y, label, color=BLUE, below=True, size=13, side=None, lcolor=INK2):
    """Borne (tornillo) con etiqueta. side='left'/'right' pone la etiqueta al costado."""
    if side == "right":
        lab = text(x + 15, y + size * 0.35, label, size, 700, lcolor, FM)
    elif side == "left":
        lab = text(x - 15, y + size * 0.35, label, size, 700, lcolor, FM, anchor="end")
    else:
        lab = text(x, y + 24 if below else y - 14, label, size, 600, lcolor, FM, anchor="middle")
    return (f'<circle cx="{x}" cy="{y}" r="9" fill="{SOFT}" stroke="{color}" stroke-width="2"/>'
            f'<path d="M{x - 5} {y + 5}L{x + 5} {y - 5}" stroke="{color}" stroke-width="1.6"/>' + lab)


def wire(points, kind="data", arrow=False, dash=None):
    """Cable poligonal (codos rectos) por una lista de puntos."""
    col, sw, d0 = Cable.STY[kind]
    dash = dash or d0
    d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in points)
    mk = {BLUE: "a-blue", CYAN: "a-cyan", INK3: "a-gray", OK: "a-ok", ALERT: "a-alert"}.get(col, "a-blue")
    s = f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round"' + (f' stroke-dasharray="{dash}"' if dash else "") + (f' marker-end="url(#{mk})"' if arrow else "") + "/>"
    if kind in ("data", "power+", "power-", "relay") and not arrow:
        (x1, y1), (x2, y2) = points[0], points[-1]
        s += f'<circle cx="{x1:.1f}" cy="{y1:.1f}" r="4.5" fill="{col}"/><circle cx="{x2:.1f}" cy="{y2:.1f}" r="4.5" fill="{col}"/>'
    return s


def diode_v(x, y, h=56, color=INK):
    """Diodo vertical centrado en (x, y): cátodo arriba (va al +), ánodo abajo (va al -)."""
    t = 12
    return (f'<path d="M{x} {y - h / 2}V{y - t}M{x} {y + t}V{y + h / 2}" stroke="{color}" stroke-width="2.5"/>'
            f'<path d="M{x - 12} {y + t}H{x + 12}L{x} {y - t + 2}z" fill="{color}"/>'
            f'<path d="M{x - 13} {y - t}H{x + 13}" stroke="{color}" stroke-width="3"/>')


def icon(x, y, name, color=BLUE, scale=1.2, sw=1.8):
    return f'<g transform="translate({x} {y}) scale({scale})" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">{ICON[name]}</g>'


def lifeline(x, y1, y2, title, sub=None):
    """Columna de un diagrama de secuencia."""
    out = [f'<rect x="{x - 95}" y="{y1}" width="190" height="{62 if sub else 48}" rx="12" fill="{DEEP}"/>',
           text(x, y1 + (27 if sub else 30), title, 17, 600, WHITE, FB, anchor="middle")]
    if sub:
        out.append(text(x, y1 + 49, sub, 14, 400, "#9FC3E3", FM, anchor="middle"))
    top = y1 + (62 if sub else 48)
    out.append(f'<path d="M{x} {top}V{y2}" stroke="{LINE2}" stroke-width="2" stroke-dasharray="6 6"/>')
    return "".join(out)


def msg(x1, x2, y, label, kind="flow", above=True, size=15, color=None):
    """Flecha horizontal de un diagrama de secuencia con texto encima."""
    col = color or {"flow": BLUE, "ok": OK, "alert": ALERT, "logical": INK3, "relay": CYAN}[kind]
    mk = {BLUE: "a-blue", OK: "a-ok", ALERT: "a-alert", INK3: "a-gray", CYAN: "a-cyan"}[col]
    dash = ' stroke-dasharray="8 6"' if kind == "logical" else ""
    xe = x2 - 6 if x2 > x1 else x2 + 6
    return (f'<path d="M{x1} {y}H{xe}" stroke="{col}" stroke-width="3"{dash} marker-end="url(#{mk})"/>'
            + text((x1 + x2) / 2, y - 10 if above else y + 22, label, size, 600, col, FM, anchor="middle"))


def bullet_list(x, y, items, w, size=16, gap=10, color=INK2):
    """Lista con viñetas cortas. items: str o (str, kind) con kind ok/alert/warn para el punto."""
    out, yy = [], y
    for it in items:
        s, kd = (it, "info") if isinstance(it, str) else it
        col = {"info": CYAN, "ok": OK, "alert": ALERT, "warn": WARN}[kd]
        out.append(f'<circle cx="{x + 5}" cy="{yy - size * 0.33:.1f}" r="4.5" fill="{col}"/>')
        svg, hh = wrap(x + 20, yy, s, w - 20, size, 400, color)
        out.append(svg)
        yy += hh + gap
    return "".join(out), yy


def frame(x, y, w, h, label=None, night=False):
    """Cuadro de cámara esquemático (escena): fondo oscuro, piso, cerco. Devuelve svg."""
    sky = "#0B1A28" if night else "#2C4A63"
    ground = "#1B2B1E" if night else "#3B5A3F"
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{sky}"/>',
           f'<path d="M{x} {y + h * 0.55}H{x + w}V{y + h - 14}a14 14 0 0 1 -14 14H{x + 14}a14 14 0 0 1 -14 -14z" fill="{ground}"/>']
    # cerco
    fy = y + h * 0.55
    out.append(f'<path d="M{x + 10} {fy - 34}H{x + w - 10}" stroke="#8FA3B5" stroke-width="3"/>')
    for i in range(int((w - 20) / 26) + 1):
        px = x + 10 + i * 26
        out.append(f'<path d="M{px} {fy - 40}V{fy}" stroke="#8FA3B5" stroke-width="2"/>')
    if label:
        out.append(f'<rect x="{x + 12}" y="{y + 12}" width="{len(label) * 8.6 + 22:.0f}" height="26" rx="13" fill="#000" opacity=".55"/>')
        out.append(text(x + 23, y + 30, label, 14, 600, WHITE, FM))
    return "".join(out)


def person(x, y, s=1.0, color="#F2F5F8"):
    """Silueta de persona (cabeza y cuerpo) con pie en (x, y)."""
    return (f'<circle cx="{x}" cy="{y - 58 * s}" r="{9 * s}" fill="{color}"/>'
            f'<path d="M{x - 11 * s} {y - 46 * s}h{22 * s}l{4 * s} {26 * s}h{-6 * s}l{-2 * s} {20 * s}h{-6 * s}l{-1 * s} {-16 * s}h{-2 * s}l{-1 * s} {16 * s}h{-6 * s}l{-2 * s} {-20 * s}h{-6 * s}z" fill="{color}"/>')


def dog(x, y, s=1.0, color="#C9B48A"):
    return (f'<ellipse cx="{x}" cy="{y - 14 * s}" rx="{20 * s}" ry="{9 * s}" fill="{color}"/>'
            f'<circle cx="{x + 22 * s}" cy="{y - 22 * s}" r="{7 * s}" fill="{color}"/>'
            f'<path d="M{x - 14 * s} {y - 8 * s}v{8 * s}M{x - 6 * s} {y - 8 * s}v{8 * s}M{x + 8 * s} {y - 8 * s}v{8 * s}M{x + 14 * s} {y - 8 * s}v{8 * s}" stroke="{color}" stroke-width="{3 * s}"/>')


def tag(x, y, s, kind="info", size=15, anchor="start"):
    """Pastilla de estado con colores KC (info, ok, warn, alert, gray, cyan)."""
    bg, fg = KC[kind]
    w = len(s) * size * 0.56 + 24
    x0 = x - w / 2 if anchor == "middle" else x
    return (f'<rect x="{x0:.1f}" y="{y - size - 6:.1f}" width="{w:.1f}" height="{size + 14}" rx="{(size + 14) / 2:.1f}" fill="{bg}" stroke="{fg}" stroke-width="1.5"/>'
            + text(x0 + w / 2, y, s, size, 600, fg, FB, anchor="middle"))


def button(x, y, w, s, kind="dark", size=15, h=40):
    """Botón de interfaz esquemático."""
    fill, fg = {"dark": (DEEP, WHITE), "red": (ALERT, WHITE), "ok": (OK, WHITE), "light": (SOFT, INK), "amber": (WARN_BG, WARN)}[kind]
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{fill}"/>' + text(x + w / 2, y + h / 2 + size * 0.36, s, size, 600, fg, FB, anchor="middle")
