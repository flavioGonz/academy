"""Ayudas de dibujo propias del curso Proxmox. No modifica ilus.py: solo suma piezas.

Kicker sin número de lección ("Proxmox VE" o "Proxmox VE · Paso N") para que las imágenes
sigan siendo correctas si el curso se reordena por módulos.
"""
import sys
sys.path.insert(0, "/home/claude/ies-training/tools")
from ilus import *  # noqa
from ilus import text, wrap, e, Node  # noqa

OUT = "/home/claude/ies-training/ilustraciones/proxmox/"


def K(paso=None):
    return "Proxmox VE" + (f" · Paso {paso}" if paso else "")


def save(c, name):
    return c.save(OUT + name)


KC = {"info": (WHITE, BLUE), "ok": (OK_BG, OK), "warn": (WARN_BG, WARN), "alert": (ALERT_BG, ALERT),
      "gray": (WHITE, INK3), "cyan": (WHITE, CYAN), "soft": (SOFT, BLUE), "dark": (DEEP, CYAN)}


def panel(x, y, w, h, title=None, kind="info", sub=None, title_size=18):
    """Tarjeta con borde de color y título arriba a la izquierda."""
    bg, fg = KC[kind]
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{bg}" stroke="{fg if kind not in ("info",) else LINE2}" stroke-width="2"/>']
    if title:
        col = WHITE if kind == "dark" else (fg if kind not in ("info", "soft", "gray", "cyan") else INK)
        out.append(text(x + 20, y + 32, title, title_size, 600, col, FD))
    if sub:
        out.append(text(x + 20, y + 56, sub, 15, 400, "#9FC3E3" if kind == "dark" else INK3, FM))
    return "".join(out)


def pill(x, y, s, fg=BLUE, bg=WHITE, size=15, mono=True, anchor="middle", bold=600):
    """Etiqueta con borde (como las de los cables). y = línea base del texto."""
    w = len(s) * (size * (0.6 if mono else 0.52)) + 24
    x0 = x - w / 2 if anchor == "middle" else x
    return (f'<rect x="{x0:.1f}" y="{y - size - 5:.1f}" width="{w:.1f}" height="{size + 13}" rx="{(size + 13) / 2:.1f}" fill="{bg}" stroke="{fg}" stroke-width="1.5"/>'
            + text(x0 + w / 2, y, s, size, bold, fg, FM if mono else FB, anchor="middle"))


def code(x, y, w, s, size=15, color="#D9E9F8", h=40):
    """Línea de código o menú sobre fondo oscuro."""
    s = s.replace("  ", "\u00a0\u00a0")  # respeta espacios dobles en SVG
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#03213C"/>' + text(x + 16, y + h / 2 + size * 0.35, s, size, 500, color, FM)


def codebox(x, y, w, lines, size=15, lh=26, title=None):
    """Bloque de código de varias líneas. lines: str o (str, color)."""
    top = 30 if title else 14
    h = top + len(lines) * lh + 10
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="#03213C"/>']
    if title:
        out.append(text(x + 16, y + 22, title, 13, 500, "#7FA6C9", FM, ls=1.5))
    for i, ln in enumerate(lines):
        s, col = (ln, "#D9E9F8") if isinstance(ln, str) else ln
        s = "\u00a0" * (len(s) - len(s.lstrip(" "))) + s.lstrip(" ")  # sangría visible en SVG
        s = s.replace("  ", "\u00a0\u00a0")  # espacios dobles visibles (columnas)
        out.append(text(x + 16, y + top + 4 + (i + 0.6) * lh, s, size, 500, col, FM))
    return "".join(out), h


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


def icon(x, y, name, color=BLUE, scale=1.2, sw=1.8):
    return f'<g transform="translate({x} {y}) scale({scale})" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">{ICON[name]}</g>'


def lifeline(x, y1, y2, title, sub=None, w=190):
    """Columna de un diagrama de secuencia."""
    out = [f'<rect x="{x - w / 2}" y="{y1}" width="{w}" height="{62 if sub else 48}" rx="12" fill="{DEEP}"/>',
           text(x, y1 + (27 if sub else 30), title, 17, 600, WHITE, FB, anchor="middle")]
    if sub:
        out.append(text(x, y1 + 49, sub, 14, 400, "#9FC3E3", FM, anchor="middle"))
    top = y1 + (62 if sub else 48)
    out.append(f'<path d="M{x} {top}V{y2}" stroke="{LINE2}" stroke-width="2" stroke-dasharray="6 6"/>')
    return "".join(out)


def msg(x1, x2, y, label, kind="flow", above=True, size=15, color=None):
    """Flecha horizontal de un diagrama de secuencia con texto encima."""
    col = color or {"flow": BLUE, "ok": OK, "alert": ALERT, "logical": INK3, "relay": CYAN, "warn": WARN}[kind]
    mk = {BLUE: "a-blue", OK: "a-ok", ALERT: "a-alert", INK3: "a-gray", CYAN: "a-cyan", WARN: "a-gray"}[col]
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


def arrow(a, b, kind="flow", label=None, **kw):
    return Cable(a, b, kind=kind, label=label, arrow=True, **kw)


def box(x, y, w, h, title, lines=(), kind="info", title_size=18, size=15, mono=False, lh=None):
    """Tarjeta con título y líneas cortas debajo."""
    out = [panel(x, y, w, h, title, kind, title_size=title_size)]
    lh = lh or size * 1.45
    for i, s in enumerate(lines):
        if isinstance(s, tuple):
            s, col = s
        else:
            col = INK2 if kind != "dark" else "#D9E9F8"
        out.append(text(x + 20, y + 62 + i * lh, s, size, 500 if mono else 400, col, FM if mono else FB))
    return "".join(out)


def tag(x, y, s, kind="info", size=15, mono=True, anchor="middle"):
    """Chip de color con significado. kind: info|ok|warn|alert|gray|dark|cyan."""
    bg, fg = {"info": (SOFT, BLUE), "ok": (OK_BG, OK), "warn": (WARN_BG, WARN), "alert": (ALERT_BG, ALERT),
              "gray": (WHITE, INK3), "dark": (DEEP, WHITE), "cyan": (CYAN, WHITE)}[kind]
    w = len(s) * (size * (0.6 if mono else 0.53)) + 24
    x0 = x - w / 2 if anchor == "middle" else (x - w if anchor == "end" else x)
    return (f'<rect x="{x0:.1f}" y="{y - size - 6:.1f}" width="{w:.1f}" height="{size + 14}" rx="{(size + 14) / 2:.1f}" fill="{bg}" stroke="{fg}" stroke-width="1.5"/>'
            + text(x0 + w / 2, y, s, size, 600, fg, FM if mono else FB, anchor="middle"))


def hline(x1, x2, y, color=LINE, sw=1.5):
    return f'<path d="M{x1} {y}H{x2}" stroke="{color}" stroke-width="{sw}"/>'


def rect(x, y, w, h, fill=WHITE, stroke=LINE2, rx=12, sw=2, dash=None, op=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    o = f' fill-opacity="{op}"' if op is not None else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"{o} stroke="{stroke}" stroke-width="{sw}"{d}/>'


def mid(x, y, s, size=16, weight=500, color=INK2, font=FB):
    return text(x, y, s, size, weight, color, font, anchor="middle")


def badge(x, y, s, color=CYAN, r=18, size=17):
    """Círculo con una letra o número (para recorridos a, b, c o 1, 2, 3 dentro de una figura)."""
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}"/>' + text(x, y + size * 0.36, s, size, 700, WHITE, FD, anchor="middle")


def lines(x, y, items, size=16, lh=26, color=INK2, font=FB, weight=400):
    """Varias líneas sueltas, una debajo de otra. items: str o (str, color)."""
    out = []
    for i, s in enumerate(items):
        s, col = (s, color) if isinstance(s, str) else s
        out.append(text(x, y + i * lh, s, size, weight, col, font))
    return "".join(out)




# ---------------------------------------------------------------- piezas Proxmox
NOLIG = "<style>text{font-variant-ligatures:none;font-feature-settings:'calt' 0,'liga' 0}</style>"


def host(x, y, w, h, title, sub=None, dark=True):
    """Servidor o nodo Proxmox (caja grande, oscura por defecto) con ícono de servidor."""
    fill, st = (DEEP, DEEP) if dark else (WHITE, LINE2)
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="{fill}" stroke="{st}" stroke-width="2"/>',
           icon(x + 18, y + 16, "server", CYAN if dark else BLUE, 1.15),
           text(x + 56, y + 38, title, 20, 600, WHITE if dark else INK, FD)]
    if sub:
        out.append(text(x + 56, y + 60, sub, 15, 400, "#9FC3E3" if dark else INK3, FM))
    return "".join(out)


def vmcard(x, y, w, title, sub=None, kind="info", h=None, ic="laptop"):
    """Tarjeta chica de VM o contenedor. kind: info|ok|warn|alert|gray|dark."""
    h = h or (70 if sub else 52)
    bg, fg = {"info": (WHITE, BLUE), "ok": (OK_BG, OK), "warn": (WARN_BG, WARN), "alert": (ALERT_BG, ALERT),
              "gray": (GROUND, INK3), "dark": ("#0B3A66", CYAN), "soft": (SOFT, BLUE)}[kind]
    tc = WHITE if kind == "dark" else INK
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{bg}" stroke="{fg}" stroke-width="2"/>',
           icon(x + 12, y + h / 2 - 13, ic, fg, 1.05),
           text(x + 46, y + (h / 2 - 3 if sub else h / 2 + 6), title, 17, 600, tc, FB)]
    if sub:
        out.append(text(x + 46, y + h / 2 + 19, sub, 15, 400, "#9FC3E3" if kind == "dark" else INK3, FM))
    return "".join(out)


def layer(x, y, w, h, label, sub=None, fill=SOFT, stroke=LINE2, color=INK, size=18, mono=False):
    """Capa horizontal de una pila (hardware, kernel, hipervisor…)."""
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{fill}" stroke="{stroke}" stroke-width="2"/>',
           text(x + w / 2, y + h / 2 + (size * 0.35 if not sub else -2), label, size, 600, color, FM if mono else FB, anchor="middle")]
    if sub:
        out.append(text(x + w / 2, y + h / 2 + 20, sub, 15, 400, INK3 if fill in (SOFT, WHITE, GROUND) else "#9FC3E3", FM, anchor="middle"))
    return "".join(out)


def blocks(x, y, cells, size=54, gap=8, label_size=16):
    """Fila de bloques de disco. cells: lista de (texto, kind) con kind data|new|old|free|ref|alert."""
    st = {"data": (SOFT, BLUE, INK), "new": (OK_BG, OK, OK), "old": (WARN_BG, WARN, WARN), "free": (WHITE, LINE2, INK3),
          "ref": (WHITE, CYAN, CYAN), "alert": (ALERT_BG, ALERT, ALERT), "dark": (DEEP, DEEP, WHITE)}
    out = []
    for i, (s, k) in enumerate(cells):
        bg, fg, tc = st[k]
        xx = x + i * (size + gap)
        dash = ' stroke-dasharray="5 4"' if k == "free" else ""
        out.append(f'<rect x="{xx}" y="{y}" width="{size}" height="{size}" rx="8" fill="{bg}" stroke="{fg}" stroke-width="2"{dash}/>')
        if s:
            out.append(text(xx + size / 2, y + size / 2 + label_size * 0.36, s, label_size, 700, tc, FM, anchor="middle"))
    return "".join(out)


def check(x, y, s, ok=True, size=17, w=None, color=INK):
    """Tilde o cruz con texto al lado (y = centro del círculo)."""
    out = Mark(x, y, ok)
    if w:
        svg, _ = wrap(x + 30, y + 6, s, w, size, 500, color)
        return out + svg
    return out + text(x + 30, y + 6, s, size, 500, color, FB)


def arrowline(x1, y1, x2, y2, color=BLUE, sw=3, dash=None):
    mk = {BLUE: "a-blue", CYAN: "a-cyan", INK3: "a-gray", OK: "a-ok", ALERT: "a-alert"}.get(color, "a-blue")
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<path d="M{x1} {y1}L{x2} {y2}" stroke="{color}" stroke-width="{sw}"{d} fill="none" marker-end="url(#{mk})"/>'


def path(d, color=BLUE, sw=3, dash=None, arrow=False):
    mk = {BLUE: "a-blue", CYAN: "a-cyan", INK3: "a-gray", OK: "a-ok", ALERT: "a-alert"}.get(color, "a-blue")
    da = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<path d="{d}" stroke="{color}" stroke-width="{sw}"{da} fill="none" stroke-linejoin="round" stroke-linecap="round"' + (f' marker-end="url(#{mk})"' if arrow else "") + "/>"
