"""Ayudantes propios para las ilustraciones MikroTik 1-11 (encima de tools/ilus.py, sin modificarla)."""
import sys
sys.path.insert(0, "/home/claude/ies-training/tools")
from ilus import *  # noqa
from ilus import e, text, wrap

OUT = "/home/claude/ies-training/ilustraciones/mikrotik/"


def rect(x, y, w, h, fill=WHITE, stroke=LINE2, sw=2, rx=16, dash=None, opacity=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    o = f' opacity="{opacity}"' if opacity is not None else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}{o}/>'


def line(x1, y1, x2, y2, color=LINE2, sw=2, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<path d="M{x1} {y1}L{x2} {y2}" stroke="{color}" stroke-width="{sw}" fill="none" stroke-linecap="round"{d}/>'


def note_h(w, body, title=None, size=16):
    pad = 18
    th = 0
    if title:
        _, th = wrap(0, 0, title, w - 2 * pad - 8, 17, 600, INK)
        th += 4
    _, bh = wrap(0, 0, body, w - 2 * pad - 8, size, 400, INK2)
    return pad * 2 + th + bh - 4


KIND = {"ok": (OK_BG, OK), "alert": (ALERT_BG, ALERT), "warn": (WARN_BG, WARN), "plain": (WHITE, INK2),
        "hl": (SOFT, BLUE), "dim": (GROUND, INK3)}


def rows(x, y, w, items, h=34, gap=6, size=15, font=FM):
    """Filas de código/reglas coloreadas (como 4.svg). items = [(texto, kind)], kind en KIND."""
    out = []
    for i, (s, k) in enumerate(items):
        bg, fg = KIND[k]
        yy = y + i * (h + gap)
        out.append(rect(x, yy, w, h, bg, LINE if k == "plain" else (CYAN if k == "hl" else bg), 1.5, 8))
        out.append(text(x + 16, yy + h / 2 + 5.5, s, size, 500 if k != "dim" else 400, fg, font))
    return "".join(out)


def caption(x, y, s, color=INK3):
    """Rótulo chico en mayúsculas (estilo kicker)."""
    return text(x, y, s.upper(), 14, 600, color, FM, ls=1.6)


def card(x, y, w, h, title, body=None, kind="info", icon=None, title_size=19, body_size=16, mono_title=False):
    """Tarjeta con título y cuerpo envuelto. kind: info | ok | alert | warn | dark."""
    if kind == "dark":
        bg, st, tc, bc = DEEP, DEEP, WHITE, "#9FC3E3"
    else:
        bg, st = {"info": (WHITE, LINE2), "ok": (OK_BG, OK), "alert": (ALERT_BG, ALERT), "warn": (WARN_BG, WARN)}[kind]
        tc, bc = INK, INK2
    out = [rect(x, y, w, h, bg, st, 2, 16)]
    tx = x + 20
    if icon:
        col = CYAN if kind == "dark" else {"ok": OK, "alert": ALERT, "warn": WARN}.get(kind, BLUE)
        out.append(f'<g transform="translate({x + 18} {y + 16}) scale(1.15)" fill="none" stroke="{col}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{ICON[icon]}</g>')
        tx = x + 58
    out.append(text(tx, y + 38, title, title_size, 600, tc, FM if mono_title else FD))
    if body:
        b, _ = wrap(x + 20, y + 70, body, w - 40, body_size, 400, bc)
        out.append(b)
    return "".join(out)


def mini(x, y, w, h, title, sub="", dark=False, hl=None, icon=None, title_size=18):
    """Caja compacta centrada (equipo chico, archivo, servicio)."""
    fill = DEEP if dark else WHITE
    st = hl or (DEEP if dark else LINE2)
    out = [rect(x, y, w, h, fill, st, 3 if hl else 2, 14)]
    cx = x + w / 2
    if icon:
        out.append(f'<g transform="translate({x + 16} {y + h / 2 - 14}) scale(1.15)" fill="none" stroke="{CYAN if dark else BLUE}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{ICON[icon]}</g>')
        cx = x + 48 + (w - 48) / 2
    ty = y + h / 2 + (-3 if sub else 6)
    out.append(text(cx, ty, title, title_size, 600, WHITE if dark else INK, FB, anchor="middle"))
    if sub:
        out.append(text(cx, ty + 22, sub, 15, 400, "#9FC3E3" if dark else INK3, FM, anchor="middle"))
    return "".join(out)


def pill(x, y, s, kind="blue", anchor="middle", mono=True):
    return Chip(x, y, s, kind, mono=mono, anchor=anchor).svg()


def arrow(a, b, kind="flow", label=None, **kw):
    return Arrow(a, b, label=label, kind=kind, **kw).svg()


def mark(x, y, ok=True):
    return Mark(x, y, ok)


def icon(x, y, name, color=BLUE, scale=1.2, sw=2):
    return f'<g transform="translate({x} {y}) scale({scale})" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">{ICON[name]}</g>'


def code(x, y, w, lines, title="TERMINAL", lh=28, size=15):
    """Terminal oscura. lines: str o (str, color). Devuelve (svg, alto)."""
    h = 50 + lh * len(lines)
    out = [rect(x, y, w, h, "#03213C", "#03213C", 0, 14), text(x + 18, y + 27, title, 13, 500, "#7FA6C9", FM, ls=1.5)]
    for i, ln in enumerate(lines):
        s, c = (ln, "#D9E9F8") if isinstance(ln, str) else ln
        out.append(text(x + 18, y + 56 + i * lh, s, size, 400, c, FM))
    return "".join(out), h


GREEN_T, RED_T, CYAN_T, GRAY_T, AMBER_T = "#6EE7B7", "#FCA5A5", "#7DD3FC", "#7FA6C9", "#FCD34D"


def port_router(x, y, ports, colors=None, name="", sub="", pw=64, gap=8, labels=None):
    """Router compacto con puertos chicos. colors={'ether1': WARN}. Devuelve (svg, dict de anclas abajo, ancho)."""
    colors = colors or {}
    w = 40 + len(ports) * (pw + gap) - gap
    h = 130 if name else 90
    out = [rect(x, y, w, h, DEEP, DEEP, 2, 18)]
    py = y + (h - 64)
    if name:
        out.append(text(x + 20, y + 34, name, 19, 600, WHITE, FD))
        if sub:
            out.append(text(x + w - 20, y + 34, sub, 14, 500, CYAN, FM, anchor="end"))
    anchors = {}
    for i, p in enumerate(ports):
        px = x + 20 + i * (pw + gap)
        c = colors.get(p)
        out.append(rect(px, py, pw, 46, c or "#0B3A66", c or "#4E7396", 2, 8))
        lbl = (labels or {}).get(p, p)
        out.append(text(px + pw / 2, py + 29, lbl, 13, 600, WHITE, FM, anchor="middle"))
        anchors[p] = (px + pw / 2, py + 46 + (h - (py - y) - 46))
    return "".join(out), anchors, w


def save(c, name):
    p = c.save(OUT + name)
    print("guardado", p)
    return p


def pills(x, y, items, kind="ok", gap=8):
    """Fila de chips seguidos, con separación pareja."""
    out = []
    for s in items:
        out.append(pill(x, y, s, kind, anchor="start"))
        x += len(s) * 9.2 + 26 + gap
    return "".join(out)


def ctable(x, y, head, rows_, widths, row_h=44, col_colors=None, col_fonts=None, size=15, head_bg=SOFT, zebra=False):
    """Tabla con color y fuente por columna. Celdas pueden ser (texto, color) o (texto, 'pill:kind')."""
    col_colors = col_colors or [INK] + [INK2] * (len(widths) - 1)
    col_fonts = col_fonts or [FM] + [FB] * (len(widths) - 1)
    W = sum(widths)
    H = row_h * (len(rows_) + 1)
    out = [rect(x, y, W, H, WHITE, LINE2, 1.5, 12),
           f'<path d="M{x} {y + 12}a12 12 0 0 1 12 -12h{W - 24}a12 12 0 0 1 12 12v{row_h - 12}h-{W}z" fill="{head_bg}"/>']
    cx = x
    for hd, w in zip(head, widths):
        out.append(text(cx + 16, y + row_h / 2 + 5, hd.upper(), 13, 600, INK3, FM, ls=1.2))
        cx += w
    for r, row in enumerate(rows_):
        ry = y + row_h * (r + 1)
        if r:
            out.append(f'<path d="M{x + 12} {ry}H{x + W - 12}" stroke="{LINE}" stroke-width="1"/>')
        cx = x
        for i, (cell, w) in enumerate(zip(row, widths)):
            col, s = col_colors[i], cell
            if isinstance(cell, tuple):
                s, col = cell
            if isinstance(col, str) and col.startswith("pill:"):
                out.append(pill(cx + 14, ry + row_h / 2 + 5, s, col[5:], anchor="start"))
            else:
                out.append(text(cx + 16, ry + row_h / 2 + 5, s, size, 500 if i == 0 else 400, col, col_fonts[i]))
            cx += w
    return "".join(out), H


def fileicon(x, y, name, kind="text", w=64, h=80):
    """Ícono de archivo (hoja con esquina doblada). kind: text | bin | secret."""
    col = {"text": BLUE, "bin": NAVY, "secret": WARN}[kind]
    f = 18
    out = [f'<path d="M{x} {y + 8}a8 8 0 0 1 8 -8h{w - f - 8}l{f} {f}v{h - f - 8}a8 8 0 0 1 -8 8h-{w - 16}a8 8 0 0 1 -8 -8z" fill="{WHITE}" stroke="{col}" stroke-width="2.5"/>',
           f'<path d="M{x + w - f} {y}v{f}h{f}" fill="none" stroke="{col}" stroke-width="2.5"/>']
    if kind == "bin":
        out.append(text(x + w / 2, y + 52, "0101", 13, 600, col, FM, anchor="middle"))
    else:
        for i in range(3):
            out.append(line(x + 12, y + 32 + i * 12, x + w - 14 - (i == 2) * 14, y + 32 + i * 12, col, 2))
    if kind == "secret":
        out.append(f'<g transform="translate({x + w - 22} {y + h - 26}) scale(.9)" fill="{WARN_BG}" stroke="{col}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">{ICON["lock"]}</g>')
    if name:
        out.append(text(x + w / 2, y + h + 24, name, 15, 600, INK, FM, anchor="middle"))
    return "".join(out)


def bullets(x, y, items, w, size=16, color=INK2, gap=10, dot=BLUE):
    """Lista con viñetas; items str o (str, color). Devuelve (svg, alto)."""
    out, yy = [], y
    for it in items:
        s, col = (it, dot) if isinstance(it, str) else it
        out.append(f'<circle cx="{x + 5}" cy="{yy - 5}" r="4" fill="{col}"/>')
        t, h = wrap(x + 20, yy, s, w - 20, size, 400, color)
        out.append(t)
        yy += h + gap
    return "".join(out), yy - y


def tube(x1, y, x2, h=56, label=None, color=CYAN):
    """Túnel horizontal (banda redondeada con borde) entre x1 y x2, centrado en y."""
    out = [rect(x1, y - h / 2, x2 - x1, h, "#E2F5FB", color, 2.5, h / 2)]
    if label:
        out.append(icon(x1 + 24, y - 14, "lock", color, 1.15, 2.2))
        out.append(text(x1 + 60, y + 6, label, 15, 600, "#0B7FA6", FM))
    return "".join(out)
