"""Ayudantes propios de las ilustraciones Akuvox 29 a 41 (no tocan ilus.py).

Agrega: bloques de bornes genéricos, lámpara de banco, cables con codos, barras de capacidad,
tarjetas de paso numeradas, globos de texto y tablas con tildes.
"""
import sys
sys.path.insert(0, "/home/claude/ies-training/tools")
from ilus import *  # noqa
from ilus import text, wrap, e  # noqa

OUT = "/home/claude/ies-training/ilustraciones/akuvox"


def out(name):
    return f"{OUT}/{name}"


class Strip(Node):
    """Bloque de bornes genérico. terms = ['12V', 'GND', ...]. Los bornes quedan abajo (side='bottom') o arriba.
    hl = {'NO': CYAN}. Anclas: .port('NO')."""
    def __init__(self, x, y, title, terms, sub="", side="bottom", hl=None, tw=74, dark=True, w=None, h=150):
        ww = w or max(240, 28 + len(terms) * tw)
        super().__init__(x, y, ww, h)
        self.title, self.terms, self.sub, self.side, self.hl, self.tw, self.dark = title, list(terms), sub, side, hl or {}, tw, dark
        x0 = x + (ww - len(terms) * tw) / 2
        self.tx = []
        for i, t in enumerate(terms):
            cx = x0 + i * tw + tw / 2
            self.tx.append(cx)
            self.anchors[t] = (cx, y + h if side == "bottom" else y)

    def svg(self):
        x, y, w, h = self.x, self.y, self.w, self.h
        fill = DEEP if self.dark else WHITE
        tc = WHITE if self.dark else INK
        sc = "#9FC3E3" if self.dark else INK3
        out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="{fill}" stroke="{DEEP if self.dark else LINE2}" stroke-width="2"/>']
        if self.side == "bottom":
            out.append(text(x + 20, y + 34, self.title, 20, 600, tc, FD))
            if self.sub:
                out.append(text(x + 20, y + 56, self.sub, 15, 400, sc, FM))
            sy = y + h - 28
            ly = y + h - 60
        else:
            out.append(text(x + 20, y + h - 40, self.title, 20, 600, tc, FD))
            if self.sub:
                out.append(text(x + 20, y + h - 18, self.sub, 15, 400, sc, FM))
            sy = y + 30
            ly = y + 64
        for cx, t in zip(self.tx, self.terms):
            c = self.hl.get(t)
            out.append(f'<rect x="{cx - 26}" y="{sy - 17}" width="52" height="34" rx="6" fill="{c or ("#0B3A66" if self.dark else SOFT)}" stroke="{c or ("#4E7396" if self.dark else LINE2)}" stroke-width="2"/>')
            out.append(f'<circle cx="{cx}" cy="{sy}" r="8" fill="none" stroke="{WHITE if (c or self.dark) else INK3}" stroke-width="2"/><path d="M{cx - 5} {sy}h10" stroke="{WHITE if (c or self.dark) else INK3}" stroke-width="2"/>')
            out.append(text(cx, ly + 5, t, 15, 600, (CYAN if not c else WHITE) if self.dark else INK2, FM, anchor="middle") if self.side == "bottom" else text(cx, ly + 5, t, 15, 600, CYAN if self.dark else INK2, FM, anchor="middle"))
        return "".join(out)


class Lamp(Node):
    """Lámpara de banco de 12 V. Anclas 'a' (izquierda) y 'b' (derecha)."""
    def __init__(self, x, y, title="Lámpara 12 V", sub="de banco", on=True):
        super().__init__(x - 30, y - 30, 60, 60)
        self.cx, self.cy, self.title, self.sub, self.on = x, y, title, sub, on
        self.anchors["a"] = (x - 30, y)
        self.anchors["b"] = (x + 30, y)

    def svg(self):
        x, y = self.cx, self.cy
        glow = f'<circle cx="{x}" cy="{y}" r="44" fill="#FFE9A8" opacity=".55"/>' if self.on else ""
        return (glow + f'<circle cx="{x}" cy="{y}" r="30" fill="{"#FFF6D6" if self.on else WHITE}" stroke="{INK2}" stroke-width="2.5"/>'
                f'<path d="M{x - 21} {y - 21}L{x + 21} {y + 21}M{x + 21} {y - 21}L{x - 21} {y + 21}" stroke="{INK2}" stroke-width="2.5"/>'
                + text(x, y + 58, self.title, 16, 600, INK, FB, anchor="middle")
                + (text(x, y + 78, self.sub, 15, 400, INK3, FM, anchor="middle") if self.sub else ""))


class Wire:
    """Cable con codos por una lista de puntos. kind como Cable: data, power+, power-, relay, logical, ok, alert, flow."""
    STY = Cable.STY

    def __init__(self, pts, kind="relay", label=None, at=None, dy=-12, arrow=False, dots=True):
        self.pts, self.kind, self.label, self.at, self.dy, self.arrow, self.dots = pts, kind, label, at, dy, arrow, dots

    def svg(self):
        col, sw, dash = self.STY[self.kind]
        mk = {BLUE: "a-blue", CYAN: "a-cyan", INK3: "a-gray", OK: "a-ok", ALERT: "a-alert"}.get(col, "a-blue")
        d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in self.pts)
        out = [f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"'
               + (f' stroke-dasharray="{dash}"' if dash else "") + (f' marker-end="url(#{mk})"' if self.arrow else "") + "/>"]
        if self.dots and self.kind in ("data", "power+", "power-", "relay"):
            for (px, py) in (self.pts[0], self.pts[-1]):
                out.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="5" fill="{col}"/>')
        if self.label:
            if self.at is None:
                i = len(self.pts) // 2 - 1
                (x1, y1), (x2, y2) = self.pts[i], self.pts[i + 1]
                lx, ly = (x1 + x2) / 2, (y1 + y2) / 2 + self.dy
            else:
                lx, ly = self.at
            wpx = len(self.label) * 8.6 + 22
            out.append(f'<rect x="{lx - wpx / 2:.1f}" y="{ly - 19:.1f}" width="{wpx:.1f}" height="28" rx="14" fill="{WHITE}" stroke="{col}" stroke-width="1.5"/>')
            out.append(text(lx, ly, self.label, 14, 600, col if col != BLACK else INK, FM, anchor="middle"))
        return "".join(out)


def card(x, y, w, h, title, body=None, n=None, kind="info", title_size=19, body_size=16):
    """Tarjeta con número de paso opcional. kind: info | ok | warn | alert | dark."""
    bg, fg, tc, bc = {"info": (WHITE, LINE2, INK, INK2), "ok": (OK_BG, OK, INK, INK2), "warn": (WARN_BG, WARN, INK, INK2),
                      "alert": (ALERT_BG, ALERT, INK, INK2), "dark": (DEEP, DEEP, WHITE, "#C9DDF0")}[kind]
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{bg}" stroke="{fg}" stroke-width="2"/>']
    tx = x + 20
    if n is not None:
        out.append(f'<circle cx="{x + 34}" cy="{y + 34}" r="17" fill="{CYAN}" stroke="{WHITE}" stroke-width="3"/>' + text(x + 34, y + 40, n, 17, 700, WHITE, FD, anchor="middle"))
        tx = x + 62
    t_svg, th = wrap(tx, y + 40, title, x + w - tx - 16, title_size, 600, tc, FB, 1.25)
    out.append(t_svg)
    if body:
        b_svg, _ = wrap(x + 20, y + 40 + th + 8, body, w - 40, body_size, 400, bc, FB, 1.35)
        out.append(b_svg)
    return "".join(out)


def bubble(x, y, w, s, tail="left", size=16, kind="info"):
    """Globo de texto. (x, y) es la esquina superior izquierda; tail = left | down | none."""
    bg, fg = {"info": (WHITE, BLUE), "ok": (OK_BG, OK), "warn": (WARN_BG, WARN), "alert": (ALERT_BG, ALERT)}[kind]
    t_svg, th = wrap(x + 16, y + 26, s, w - 32, size, 500, INK, FB, 1.3)
    h = th + 22
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h:.0f}" rx="14" fill="{bg}" stroke="{fg}" stroke-width="2"/>']
    if tail == "left":
        out.append(f'<path d="M{x + 1} {y + 18} L{x - 16} {y + 30} L{x + 1} {y + 34}" fill="{bg}" stroke="{fg}" stroke-width="2" stroke-linejoin="round"/>'
                   f'<path d="M{x + 2} {y + 19} L{x + 2} {y + 33}" stroke="{bg}" stroke-width="3"/>')
    elif tail == "down":
        out.append(f'<path d="M{x + 30} {y + h - 1} L{x + 40} {y + h + 16} L{x + 50} {y + h - 1}" fill="{bg}" stroke="{fg}" stroke-width="2" stroke-linejoin="round"/>'
                   f'<path d="M{x + 31} {y + h - 2} L{x + 49} {y + h - 2}" stroke="{bg}" stroke-width="3"/>')
    out.append(t_svg)
    return "".join(out)


def hbar(x, y, w_max, val, vmax, label, value_txt, color=BLUE, h=34, lw=250):
    """Barra horizontal: etiqueta a la izquierda (ancho lw), barra proporcional y valor."""
    bw = w_max * val / vmax
    return (text(x, y + h / 2 + 6, label, 16, 600, INK, FB)
            + f'<rect x="{x + lw}" y="{y}" width="{w_max}" height="{h}" rx="8" fill="{SOFT}"/>'
            + f'<rect x="{x + lw}" y="{y}" width="{bw:.1f}" height="{h}" rx="8" fill="{color}"/>'
            + text(x + lw + bw + 12, y + h / 2 + 6, value_txt, 16, 600, INK, FM))


def check_table(x, y, head, rows, widths, row_h=46, first_mono=False):
    """Tabla con celdas que pueden ser texto, True (tilde verde) o False (cruz roja) o '-' (gris)."""
    W = sum(widths)
    out = [f'<rect x="{x}" y="{y}" width="{W}" height="{row_h * (len(rows) + 1)}" rx="12" fill="{WHITE}" stroke="{LINE2}" stroke-width="1.5"/>',
           f'<path d="M{x} {y + 12}a12 12 0 0 1 12 -12h{W - 24}a12 12 0 0 1 12 12v{row_h - 12}h-{W}z" fill="{SOFT}"/>']
    cx = x
    for hd, w in zip(head, widths):
        if cx == x:
            out.append(text(cx + 16, y + row_h / 2 + 5, hd.upper(), 14, 600, INK3, FM, ls=1.2))
        else:
            out.append(text(cx + w / 2, y + row_h / 2 + 5, hd.upper(), 14, 600, INK3, FM, anchor="middle", ls=1.0))
        cx += w
    for r, row in enumerate(rows):
        ry = y + row_h * (r + 1)
        if r:
            out.append(f'<path d="M{x + 12} {ry}H{x + W - 12}" stroke="{LINE}" stroke-width="1"/>')
        cx = x
        for i, (cell, w) in enumerate(zip(row, widths)):
            mid = cx + w / 2
            cy = ry + row_h / 2
            if cell is True:
                out.append(f'<circle cx="{mid}" cy="{cy}" r="13" fill="{OK_BG}" stroke="{OK}" stroke-width="2"/><path d="M{mid - 6} {cy}l4 4.5l8 -9" fill="none" stroke="{OK}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>')
            elif cell is False:
                out.append(f'<circle cx="{mid}" cy="{cy}" r="13" fill="{ALERT_BG}" stroke="{ALERT}" stroke-width="2"/><path d="M{mid - 5} {cy - 5}l10 10M{mid + 5} {cy - 5}l-10 10" fill="none" stroke="{ALERT}" stroke-width="2.6" stroke-linecap="round"/>')
            elif i == 0:
                out.append(text(cx + 16, cy + 6, cell, 17, 600, INK, FM if first_mono else FB))
            else:
                col = INK3 if cell in ("-", "sin dato") else INK2
                out.append(text(mid, cy + 6, cell, 16, 500, col, FM, anchor="middle"))
            cx += w
    return "".join(out)


def legend_ok_bad(x, y):
    return (Mark(x, y, True) + text(x + 28, y + 6, "lo trae", 15, 500, INK2)
            + Mark(x + 130, y, False) + text(x + 158, y + 6, "no lo trae", 15, 500, INK2))


def arrow_right(x, y, w=40, color=INK3):
    return f'<path d="M{x} {y}h{w}" stroke="{color}" stroke-width="3" marker-end="url(#a-gray)"/>'


def pill(x, y, s, kind="gray", mono=True, anchor="start"):
    return Chip(x, y, s, kind, mono, anchor).svg()


def chip_w(s, mono=True):
    return len(s) * (9.2 if mono else 8.4) + 26


def chips_row(x, y, items, kind="gray", mono=False, gap=10):
    """Fila de chips sin superposición. items: str o (str, kind). Devuelve svg."""
    outs, cx = [], x
    for it in items:
        s, k = (it, kind) if isinstance(it, str) else it
        outs.append(Chip(cx, y, s, k, mono).svg())
        cx += chip_w(s, mono) + gap
    return "".join(outs)


def contact(x, y, label="relé 1", sub=None, closed=False, w=150):
    """Símbolo de contacto de relé entre (x, y) y (x + w, y): dos bornes y una palanca. Devuelve svg."""
    a, b = x + 30, x + w - 30
    lever = f'<path d="M{a} {y}L{b - 4} {y - (0 if closed else 26)}" stroke="{CYAN}" stroke-width="4" stroke-linecap="round"/>'
    o = (f'<rect x="{x}" y="{y - 52}" width="{w}" height="86" rx="14" fill="{WHITE}" stroke="{LINE2}" stroke-width="2"/>'
         f'<path d="M{x} {y}H{a}M{b} {y}H{x + w}" stroke="{CYAN}" stroke-width="4"/>'
         f'<circle cx="{a}" cy="{y}" r="6" fill="{WHITE}" stroke="{CYAN}" stroke-width="3"/><circle cx="{b}" cy="{y}" r="6" fill="{WHITE}" stroke="{CYAN}" stroke-width="3"/>'
         + lever + text(x + w / 2, y + 26, label, 15, 600, INK, FM, anchor="middle"))
    if sub:
        o += text(x + w / 2, y - 60, sub, 15, 500, INK3, FM, anchor="middle")
    return o


def coil(x, y, label="bobina", sub=None, w=150):
    """Bobina de un relé auxiliar entre (x, y) y (x + w, y). Devuelve svg."""
    a, b = x + 34, x + w - 34
    loops = "".join(f'<path d="M{a + i * (b - a) / 4:.1f} {y}a{(b - a) / 8:.1f} 12 0 0 1 {(b - a) / 4:.1f} 0" fill="none" stroke="{CYAN}" stroke-width="3"/>' for i in range(4))
    o = (f'<rect x="{x}" y="{y - 52}" width="{w}" height="86" rx="14" fill="{WHITE}" stroke="{LINE2}" stroke-width="2"/>'
         f'<path d="M{x} {y}H{a}M{b} {y}H{x + w}" stroke="{CYAN}" stroke-width="4"/>' + loops
         + text(x + w / 2, y + 26, label, 15, 600, INK, FM, anchor="middle"))
    if sub:
        o += text(x + w / 2, y - 60, sub, 15, 500, INK3, FM, anchor="middle")
    return o
