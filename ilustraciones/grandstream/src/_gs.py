"""Ayudas de dibujo propias del curso Grandstream. No modifica ilus.py: solo suma piezas.

Kicker sin número de lección ("Grandstream" o "Grandstream · Paso N") para que las imágenes
sigan siendo correctas si el curso se reordena por módulos.
"""
import sys
sys.path.insert(0, "/home/claude/ies-training/tools")
from ilus import *  # noqa
from ilus import text, wrap, e, Node  # noqa

OUT = "/home/claude/ies-training/ilustraciones/grandstream/"


def K(paso=None):
    return "Grandstream" + (f" · Paso {paso}" if paso else "")


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


class DeskPhone(Node):
    """Teléfono IP de escritorio genérico (GRP, GXP). Anclas: top/bottom/left/right."""
    def __init__(self, x, y, title="Teléfono", sub="", hl=None, w=170):
        super().__init__(x, y, w, 120)
        self.title, self.sub, self.hl = title, sub, hl

    def svg(self):
        x, y, w = self.x, self.y, self.w
        st = self.hl or LINE2
        out = [f'<rect x="{x}" y="{y + 10}" width="{w}" height="110" rx="16" fill="#F1F4F7" stroke="{st}" stroke-width="{3 if self.hl else 2}"/>',
               f'<rect x="{x + 12}" y="{y}" width="34" height="112" rx="14" fill="#3A4A5C"/>',
               f'<rect x="{x + 60}" y="{y + 24}" width="{w - 74}" height="40" rx="6" fill="#0B1A28"/>']
        for r in range(3):
            for k in range(4):
                kx = x + 62 + k * ((w - 78) / 4)
                out.append(f'<rect x="{kx:.1f}" y="{y + 74 + r * 13}" width="{(w - 78) / 4 - 6:.1f}" height="8" rx="2" fill="#B9C9D8"/>')
        out.append(text(x + w / 2, y + 146, self.title, 17, 600, INK, FB, anchor="middle"))
        if self.sub:
            out.append(text(x + w / 2, y + 168, self.sub, 15, 400, INK3, FM, anchor="middle"))
        return "".join(out)


def ucm(x, y, sub="192.168.88.20", ports=("WAN", "LAN"), hl=None, name="UCM6300", extra=None):
    """La central: Router oscuro con los puertos del UCM630x (WAN y LAN)."""
    return Router(x, y, name, sub, ports=list(ports), hl=hl or {}, extra=extra)


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


class UCMBox(Node):
    """Central UCM dibujada a mano: nombre, subtítulo, LCD opcional y puertos abajo.
    ports = ['WAN', 'LAN']; hl = {'WAN': CYAN}. Anclas: .port('WAN') debajo del puerto."""
    def __init__(self, x, y, w=420, name="UCM6300", sub="", ports=("WAN", "LAN"), hl=None, lcd=None, h=150):
        super().__init__(x, y, w, h)
        self.name, self.sub, self.ports, self.hl, self.lcd = name, sub, list(ports), hl or {}, lcd
        self.pw = 86
        for i, p in enumerate(self.ports):
            px = x + 20 + i * (self.pw + 12)
            self.anchors[p] = (px + self.pw / 2, y + h)

    def svg(self):
        x, y, w, h = self.x, self.y, self.w, self.h
        out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="{DEEP}" stroke="{DEEP}" stroke-width="2"/>',
               text(x + 20, y + 36, self.name, 21, 600, WHITE, FD)]
        if self.sub:
            out.append(text(x + 20, y + 60, self.sub, 15, 400, "#9FC3E3", FM))
        if self.lcd:
            lw = len(self.lcd) * 9.4 + 28
            out.append(f'<rect x="{x + w - lw - 18}" y="{y + 18}" width="{lw:.0f}" height="46" rx="6" fill="#123B5E" stroke="{CYAN}" stroke-width="2"/>')
            out.append(text(x + w - 18 - lw / 2, y + 47, self.lcd, 15, 600, "#BFF0FF", FM, anchor="middle"))
            out.append(text(x + w - 18 - lw / 2, y + 84, "LCD", 13, 500, "#7FA6C9", FM, anchor="middle"))
        for i, p in enumerate(self.ports):
            px = x + 20 + i * (self.pw + 12)
            c = self.hl.get(p)
            out.append(f'<rect x="{px}" y="{y + h - 56}" width="{self.pw}" height="44" rx="8" fill="{c or "#0B3A66"}" stroke="{c or "#4E7396"}" stroke-width="2"/>')
            out.append(f'<rect x="{px + 26}" y="{y + h - 50}" width="{self.pw - 52}" height="14" rx="2" fill="none" stroke="{WHITE}" stroke-width="1.5" opacity=".8"/>')
            out.append(text(px + self.pw / 2, y + h - 20, p, 14, 600, WHITE, FM, anchor="middle"))
        return "".join(out)
