"""Ayudas de dibujo del curso Linux (copiadas del esquema de Paradox). No modifica ilus.py: solo suma piezas.

Kicker sin número de lección ("Linux" o "Linux · Paso N") para que las imágenes
sigan siendo correctas si el curso se reordena por módulos.
"""
import sys
sys.path.insert(0, "/home/claude/ies-training/tools")
from ilus import *  # noqa
from ilus import text, wrap, e, Node  # noqa

OUT = "/home/claude/ies-training/ilustraciones/linux/"


def K(paso=None):
    return "Linux" + (f" · Paso {paso}" if paso else "")


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


# ---------------------------------------------------------------- piezas Linux
NOLIG = "<style>text{font-variant-ligatures:none;font-feature-settings:'calt' 0,'liga' 0}</style>"
# colores de terminal (sobre fondo #03213C)
T_CMD, T_OUT, T_PR, T_OK, T_ERR, T_COM, T_WARN = "#FFFFFF", "#9FC3E3", "#5FD3F3", "#5BD69B", "#FF8A73", "#7FA6C9", "#FFC861"


def new(paso=None, title=""):
    c = Canvas(K(paso), title)
    c.add(NOLIG)
    return c


def term(x, y, w, rows, title=None, size=15, lh=25, h=None):
    """Terminal. rows: str (comando, con prompt $), ('texto', color) o ('#coment', T_COM).
    Un str que empieza con '$ ' dibuja el prompt en cian y el comando en blanco. Devuelve (svg, alto)."""
    top = 32 if title else 14
    hh = h or (top + len(rows) * lh + 12)
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{hh}" rx="12" fill="#03213C"/>']
    if title:
        out.append(text(x + 16, y + 22, title, 13, 500, "#7FA6C9", FM, ls=1.5))
    for i, r in enumerate(rows):
        yy = y + top + 4 + (i + 0.6) * lh
        if isinstance(r, str) and r.startswith("$ "):
            out.append(text(x + 16, yy, "$", size, 600, T_PR, FM))
            s = r[2:].replace("  ", "\u00a0\u00a0")
            out.append(text(x + 16 + size * 1.2, yy, s, size, 500, T_CMD, FM))
        else:
            s, col = (r, T_OUT) if isinstance(r, str) else r
            s = "\u00a0" * (len(s) - len(s.lstrip(" "))) + s.lstrip(" ")
            s = s.replace("  ", "\u00a0\u00a0")
            out.append(text(x + 16, yy, s, size, 500, col, FM))
    return "".join(out), hh


def fileb(x, y, w, path, rows, size=15, lh=25, hl=(), hl_col=None, note=None):
    """Archivo de texto (fondo blanco, ruta arriba). rows: str o (str, color). hl: índices de filas resaltadas."""
    hh = 44 + len(rows) * lh + 14
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{hh}" rx="12" fill="{WHITE}" stroke="{LINE2}" stroke-width="2"/>',
           f'<path d="M{x} {y + 12}a12 12 0 0 1 12 -12h{w - 24}a12 12 0 0 1 12 12v24h-{w}z" fill="{SOFT}"/>',
           text(x + 16, y + 25, path, 15, 600, BLUE, FM)]
    for i, r in enumerate(rows):
        s, col = (r, INK) if isinstance(r, str) else r
        yy = y + 44 + (i + 0.72) * lh
        if i in hl:
            out.append(f'<rect x="{x + 6}" y="{yy - lh * 0.72 + 1}" width="{w - 12}" height="{lh - 2}" rx="6" fill="{hl_col or SOFT}"/>')
        s = "\u00a0" * (len(s) - len(s.lstrip(" "))) + s.lstrip(" ")
        s = s.replace("  ", "\u00a0\u00a0")
        out.append(text(x + 16, yy, s, size, 500, col, FM))
    return "".join(out), hh


def callout(x, y, tx, ty, s, kind="info", size=15, anchor="start", w=None):
    """Etiqueta en (tx,ty) con línea fina hacia el punto (x,y)."""
    col = {"info": BLUE, "ok": OK, "warn": WARN, "alert": ALERT, "gray": INK3, "cyan": CYAN}[kind]
    out = [f'<path d="M{x} {y}L{tx} {ty}" stroke="{col}" stroke-width="1.6" fill="none"/>', f'<circle cx="{x}" cy="{y}" r="4" fill="{col}"/>']
    if w:
        svg, _ = wrap(tx + (6 if anchor == "start" else -6), ty + 5, s, w, size, 600, col, FB, anchor=anchor)
        out.append(svg)
    else:
        out.append(text(tx + (6 if anchor == "start" else -6), ty + 5, s, size, 600, col, FB, anchor=anchor))
    return "".join(out)


def brace(x, y1, y2, s, color=CYAN, size=15, side="right"):
    """Llave vertical con texto al costado."""
    d = 10 if side == "right" else -10
    m = (y1 + y2) / 2
    p = f'<path d="M{x} {y1}q{d} 0 {d} 10V{m - 8}q0 8 {d} 8q-{d} 0 -{d} 8V{y2 - 10}q0 10 -{d} 10" fill="none" stroke="{color}" stroke-width="2"/>'
    return p + text(x + d * 2.4, m + 5, s, size, 600, color, FB, anchor="start" if side == "right" else "end")


def flow(x, y, items, w=170, h=70, gap=46, kinds=None, size=16, sub=None):
    """Fila de cajas unidas por flechas. items: títulos; sub: subtítulos mono; kinds: info/ok/warn/alert/dark."""
    out, xs = [], []
    for i, t in enumerate(items):
        xx = x + i * (w + gap)
        k = (kinds or ["info"] * len(items))[i]
        bg, fg = {"info": (WHITE, LINE2), "ok": (OK_BG, OK), "warn": (WARN_BG, WARN), "alert": (ALERT_BG, ALERT), "dark": (DEEP, DEEP), "soft": (SOFT, CYAN)}[k]
        out.append(rect(xx, y, w, h, bg, fg, rx=14))
        tc = WHITE if k == "dark" else (fg if k in ("ok", "warn", "alert") else INK)
        if sub and sub[i]:
            out.append(mid(xx + w / 2, y + h / 2 - 3, t, size, 600, tc, FB))
            out.append(mid(xx + w / 2, y + h / 2 + 20, sub[i], 15, 500, "#9FC3E3" if k == "dark" else INK3, FM))
        else:
            out.append(mid(xx + w / 2, y + h / 2 + 6, t, size, 600, tc, FB))
        if i < len(items) - 1:
            out.append(f'<path d="M{xx + w + 6} {y + h / 2}H{xx + w + gap - 8}" stroke="{BLUE}" stroke-width="3" marker-end="url(#a-blue)"/>')
        xs.append(xx)
    return "".join(out), xs


def vline(x, y1, y2, color=LINE, sw=1.5, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<path d="M{x} {y1}V{y2}" stroke="{color}" stroke-width="{sw}"{d}/>'
