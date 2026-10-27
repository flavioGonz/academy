"""Ayudas de dibujo propias del curso Paradox. No modifica ilus.py: solo suma piezas.

Kicker sin número de lección ("Paradox" o "Paradox · Paso N") para que las imágenes
sigan siendo correctas si el curso se reordena por módulos.
"""
import sys
sys.path.insert(0, "/home/claude/ies-training/tools")
from ilus import *  # noqa
from ilus import text, wrap, e, Node  # noqa

OUT = "/home/claude/ies-training/ilustraciones/paradox/"


def K(paso=None):
    return "Paradox" + (f" · Paso {paso}" if paso else "")


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


# ---------------------------------------------------------------- piezas Paradox
NOLIG = "<style>text{font-variant-ligatures:none;font-feature-settings:'calt' 0,'liga' 0}</style>"
WIRE_COL = {"+": RED, "-": BLACK, "d": BLUE, "z": BLUE, "c": INK3, "r": CYAN, "y": "#C79A00", "g": OK}


def keycap(x, y, s, size=16, w=None, hl=None):
    """Tecla de teclado (x,y = esquina sup. izq.). Devuelve (svg, ancho)."""
    w = w or max(46, len(s) * size * 0.62 + 24)
    h = size + 22
    st = hl or LINE2
    svg = (f'<rect x="{x}" y="{y + 3}" width="{w:.1f}" height="{h}" rx="9" fill="{LINE2}"/>'
           f'<rect x="{x}" y="{y}" width="{w:.1f}" height="{h}" rx="9" fill="{WHITE}" stroke="{st}" stroke-width="{2.5 if hl else 1.5}"/>'
           + text(x + w / 2, y + h / 2 + size * 0.36, s, size, 600, INK, FM, anchor="middle"))
    return svg, w


def keys(x, y, items, size=16, gap=10, hl=()):
    """Secuencia de teclado. items: '[ENTER]' = tecla; '+' = signo; 'texto' = valor tipeado (chip oscuro);
    ('nota', 'n') = texto gris chico. Devuelve (svg, x_final)."""
    out, xx = [], x
    h = size + 22
    for i, it in enumerate(items):
        if isinstance(it, tuple):
            out.append(text(xx, y + h / 2 + 5, it[0], 15, 500, INK3, FB))
            xx += len(it[0]) * 15 * 0.52 + gap + 8
        elif it == "+":
            out.append(text(xx + 4, y + h / 2 + 6, "+", size + 2, 600, INK3, FM))
            xx += 18 + gap
        elif it.startswith("["):
            s, w = keycap(xx, y, it[1:-1], size, hl=CYAN if i in hl else None)
            out.append(s)
            xx += w + gap
        else:
            w = len(it) * size * 0.62 + 24
            out.append(f'<rect x="{xx}" y="{y}" width="{w:.1f}" height="{h}" rx="9" fill="#03213C"/>'
                       + text(xx + w / 2, y + h / 2 + size * 0.36, it, size, 600, "#D9E9F8", FM, anchor="middle"))
            xx += w + gap
    return "".join(out), xx


def strip(x, y, labels, pitch=62, title=None, hl=None, sub=None, dark=False, above=True):
    """Bornera: fila de tornillos con rótulo abajo. Devuelve (svg, anchors{label: (cx, cy)}).
    hl: {label: color} para resaltar rótulos. El ancla es el centro del tornillo."""
    hl = hl or {}
    w = pitch * len(labels) + 16
    top = 30 if title else 0
    out = []
    if title:
        out.append(text(x, y + 18, title, 15, 600, INK2 if not dark else INK, FM, ls=1))
    out.append(f'<rect x="{x}" y="{y + top}" width="{w}" height="{82 if above else 78}" rx="10" fill="#E9EEF3" stroke="{LINE2}" stroke-width="2"/>')
    an = {}
    for i, lb in enumerate(labels):
        cx = x + 8 + pitch * i + pitch / 2
        cy = y + top + (52 if above else 26)
        out.append(f'<rect x="{cx - pitch / 2 + 4}" y="{cy - 20}" width="{pitch - 8}" height="40" rx="6" fill="{WHITE}" stroke="{LINE2}" stroke-width="1.5"/>')
        out.append(f'<circle cx="{cx}" cy="{cy}" r="11" fill="#CBD5DF" stroke="{INK3}" stroke-width="1.5"/><path d="M{cx - 7} {cy}H{cx + 7}" stroke="{INK3}" stroke-width="2"/>')
        col = hl.get(lb, INK)
        out.append(text(cx, y + top + (20 if above else 68), lb, 14 if len(lb) > 5 else 15, 700 if lb in hl else 600, col, FM, anchor="middle"))
        an[lb] = (cx, cy)
        an[i] = (cx, cy)
    if sub:
        out.append(text(x, y + top + 100, sub, 15, 400, INK3, FB))
    return "".join(out), an


def resistor(x1, y, x2, label, color=INK, lab_dy=-16, body=60, vertical=False, lab_side="right"):
    """Resistencia (cuerpo rectangular, norma IEC) entre x1 y x2 sobre la línea y (o vertical: x fija, y1..y2)."""
    if vertical:
        x, y1, y2 = x1, y, x2
        my = (y1 + y2) / 2
        s = (f'<path d="M{x} {y1}V{my - body / 2}M{x} {my + body / 2}V{y2}" stroke="{color}" stroke-width="3"/>'
             f'<rect x="{x - 13}" y="{my - body / 2}" width="26" height="{body}" rx="4" fill="#FFF7E0" stroke="{WARN}" stroke-width="2.5"/>')
        tx = x + 24 if lab_side == "right" else x - 24
        return s + text(tx, my + 6, label, 16, 700, WARN, FM, anchor="start" if lab_side == "right" else "end")
    mx = (x1 + x2) / 2
    s = (f'<path d="M{x1} {y}H{mx - body / 2}M{mx + body / 2} {y}H{x2}" stroke="{color}" stroke-width="3"/>'
         f'<rect x="{mx - body / 2}" y="{y - 13}" width="{body}" height="26" rx="4" fill="#FFF7E0" stroke="{WARN}" stroke-width="2.5"/>')
    return s + text(mx, y + lab_dy - (0 if lab_dy > 0 else 4), label, 16, 700, WARN, FM, anchor="middle")


def contact(x, y, closed=True, label=None, w=70, color=INK, vertical=False):
    """Contacto (llave) entre (x,y) y (x+w,y). closed=True dibuja la lámina apoyada."""
    if vertical:
        x2, y2 = x, y + w
        tip = (x2 - (0 if closed else 22), y2 - 6)
        s = (f'<circle cx="{x}" cy="{y + 6}" r="5" fill="{WHITE}" stroke="{color}" stroke-width="2.5"/>'
             f'<circle cx="{x2}" cy="{y2 - 6}" r="5" fill="{WHITE}" stroke="{color}" stroke-width="2.5"/>'
             f'<path d="M{x} {y + 11}L{tip[0]} {tip[1] - (8 if closed else 4)}" stroke="{color}" stroke-width="3" stroke-linecap="round"/>')
        if label:
            s += text(x + 18, y + w / 2 + 5, label, 15, 600, INK2, FM)
        return s
    x2 = x + w
    s = (f'<circle cx="{x + 6}" cy="{y}" r="5" fill="{WHITE}" stroke="{color}" stroke-width="2.5"/>'
         f'<circle cx="{x2 - 6}" cy="{y}" r="5" fill="{WHITE}" stroke="{color}" stroke-width="2.5"/>'
         f'<path d="M{x + 11} {y}L{x2 - 8} {y - (5 if closed else 24)}" stroke="{color}" stroke-width="3" stroke-linecap="round"/>')
    if label:
        s += text(x + w / 2, y + 26, label, 15, 600, INK2, FM, anchor="middle")
    return s


def keypad(x, y, title="Teclado", sub="", lcd=True, w=170, hl_keys=(), screen=None):
    """Teclado genérico de alarma (frente). screen: lista de líneas cortas para la pantalla."""
    h = 250
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="#F1F4F7" stroke="{LINE2}" stroke-width="2"/>']
    if lcd:
        out.append(f'<rect x="{x + 16}" y="{y + 16}" width="{w - 32}" height="58" rx="6" fill="#0B3A66"/>')
        for i, s in enumerate(screen or []):
            out.append(text(x + 26, y + 40 + i * 22, s, 15, 600, "#9FE3F7", FM))
    kw = (w - 32 - 2 * 8) / 3
    labels = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "CLR", "0", "ENT"]
    for i, k in enumerate(labels):
        r, cidx = divmod(i, 3)
        kx, ky = x + 16 + cidx * (kw + 8), y + 88 + r * 38
        hl = k in hl_keys
        out.append(f'<rect x="{kx:.1f}" y="{ky}" width="{kw:.1f}" height="30" rx="6" fill="{CYAN if hl else WHITE}" stroke="{CYAN if hl else LINE2}" stroke-width="1.5"/>')
        out.append(text(kx + kw / 2, ky + 21, k, 13 if len(k) > 1 else 15, 600, WHITE if hl else INK2, FM, anchor="middle"))
    out.append(text(x + w / 2, y + h + 26, title, 17, 600, INK, FB, anchor="middle"))
    if sub:
        out.append(text(x + w / 2, y + h + 48, sub, 15, 400, INK3, FM, anchor="middle"))
    return "".join(out)


def opts(x, y, on, size=40, gap=8, labels=None, hl=()):
    """Fila de opciones 1 a 8 (encendida = cian). on: conjunto de números encendidos."""
    out = []
    for i in range(1, 9):
        xx = x + (i - 1) * (size + gap)
        is_on = i in on
        st = WARN if i in hl else (CYAN if is_on else LINE2)
        out.append(f'<rect x="{xx}" y="{y}" width="{size}" height="{size}" rx="8" fill="{CYAN if is_on else WHITE}" stroke="{st}" stroke-width="{3 if i in hl else 1.5}"/>')
        out.append(text(xx + size / 2, y + size / 2 + 6, str(i), 17, 700, WHITE if is_on else INK3, FM, anchor="middle"))
        if labels:
            out.append(text(xx + size / 2, y + size + 20, labels[i - 1], 13, 500, INK3, FB, anchor="middle"))
    return "".join(out)


def ledrow(x, y, pattern, label, sub=None, color=OK, cell=22, n=8):
    """Línea de tiempo de un LED: pattern = lista de 0/1 por medio segundo."""
    out = [text(x, y + 16, label, 17, 600, INK, FB)]
    if sub:
        out.append(text(x, y + 40, sub, 15, 400, INK3, FB))
    bx = x + 330
    for i, v in enumerate(pattern):
        out.append(f'<rect x="{bx + i * (cell + 4)}" y="{y}" width="{cell}" height="{cell}" rx="5" fill="{color if v else WHITE}" stroke="{color if v else LINE2}" stroke-width="1.5"/>')
    return "".join(out)


def board(x, y, w, h, title, sub=None):
    """Placa de la central, genérica (sin copiar el diseño real)."""
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{DEEP}" stroke="{DEEP}" stroke-width="2"/>',
           text(x + 20, y + 36, title, 20, 600, WHITE, FD)]
    if sub:
        out.append(text(x + 20, y + 60, sub, 15, 400, "#9FC3E3", FM))
    return "".join(out)


def vline(x, y1, y2, color=LINE, sw=1.5, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<path d="M{x} {y1}V{y2}" stroke="{color}" stroke-width="{sw}"{d}/>'
