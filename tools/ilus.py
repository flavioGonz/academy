"""ilus.py · biblioteca de ilustraciones de IES Training (SVG 1200x675, estilo IES).

Uso típico (un script por lección):

    import sys; sys.path.insert(0, "/home/claude/ies-training/tools")
    from ilus import *
    c = Canvas("MikroTik · Lección 1", "Conectá la notebook a ether2")
    r = c.add(Router(470, 210, ports=["ether1", "ether2", "ether3", "ether4", "ether5"], hl={"ether2": CYAN}, sub="hAP ax²"))
    n = c.add(Laptop(120, 420, "Notebook", "WinBox"))
    c.add(Cable(n.top(), r.port("ether2"), kind="data", label="cable de red"))
    c.add(Step(r.port("ether2")[0] + 18, r.port("ether2")[1] + 30, 1))
    c.add(Note(820, 430, 330, "ether1 queda para internet: el firewall por defecto la trata como WAN."))
    c.save("/home/claude/ies-training/ilustraciones/mikrotik/1-paso1.svg")

Después: python3 /home/claude/ies-training/tools/render_svg.py <svg> y mirá el .png con Read.

Reglas de estilo (no las cambies por ilustración):
- Lienzo 1200x675, fondo claro con grilla tenue, encabezado arriba a la izquierda (kicker + título).
- Colores: NAVY, DEEP, BLUE, CYAN para la marca; OK / WARN / ALERT solo con significado (bien, atención, peligro) y con texto.
- Texto mínimo 15 px. Familjen Grotesk para títulos, Instrument Sans para etiquetas, JetBrains Mono para comandos, IPs, puertos y menús.
- Cables: data = azul sólido, power = rojo/negro (positivo y negativo), relay = cian, wifi = punteado, logical = punteado gris (túnel, sesión, flujo lógico).
- Dibujos genéricos: nada de logos ni copias de fotos de producto. El modelo va escrito como texto.
"""
from html import escape
import math, textwrap

NAVY, DEEP, BLUE, CYAN = "#002F58", "#011E38", "#0A63B8", "#17A8D4"
INK, INK2, INK3 = "#04223D", "#41627F", "#6E88A1"
LINE, LINE2, SOFT, GROUND, WHITE = "#DDE8F2", "#C2D4E6", "#E5F0FB", "#F7FAFD", "#FFFFFF"
OK, OK_BG, WARN, WARN_BG, ALERT, ALERT_BG = "#0E8F5E", "#E3F5EC", "#B45309", "#FFF4DE", "#D2492F", "#FCEAE6"
RED, BLACK = "#D2492F", "#2B2B2B"
FD, FB, FM = "Familjen Grotesk", "Instrument Sans", "JetBrains Mono"


def e(s):
    return escape(str(s), quote=True)


def text(x, y, s, size=17, weight=400, color=INK2, font=FB, anchor="start", ls=0):
    extra = f' letter-spacing="{ls}"' if ls else ""
    return f'<text x="{x:.1f}" y="{y:.1f}" font-family="{font}" font-size="{size}" font-weight="{weight}" fill="{color}" text-anchor="{anchor}"{extra}>{e(s)}</text>'


def wrap(x, y, s, width_px, size=17, weight=400, color=INK2, font=FB, lh=1.35, anchor="start"):
    """Texto en varias líneas. width_px aproximado (0.52*size por carácter en Instrument Sans)."""
    k = 0.6 if font == FM else 0.52
    chars = max(8, int(width_px / (size * k)))
    lines = []
    for par in str(s).split("\n"):
        lines += textwrap.wrap(par, chars) or [""]
    out = [f'<text x="{x:.1f}" y="{y:.1f}" font-family="{font}" font-size="{size}" font-weight="{weight}" fill="{color}" text-anchor="{anchor}">']
    for i, ln in enumerate(lines):
        out.append(f'<tspan x="{x:.1f}" dy="{0 if i == 0 else size * lh:.1f}">{e(ln)}</tspan>')
    out.append("</text>")
    return "".join(out), len(lines) * size * lh


class Node:
    def __init__(self, x, y, w, h):
        self.x, self.y, self.w, self.h = x, y, w, h
        self.anchors = {}

    def left(self, dy=0): return (self.x, self.y + self.h / 2 + dy)
    def right(self, dy=0): return (self.x + self.w, self.y + self.h / 2 + dy)
    def top(self, dx=0): return (self.x + self.w / 2 + dx, self.y)
    def bottom(self, dx=0): return (self.x + self.w / 2 + dx, self.y + self.h)
    def center(self): return (self.x + self.w / 2, self.y + self.h / 2)
    def port(self, name): return self.anchors[name]
    def svg(self): return ""


class Canvas:
    def __init__(self, kicker, title, bg=GROUND, grid=True):
        self.items, self.kicker, self.title, self.bg, self.grid = [], kicker, title, bg, grid

    def add(self, item):
        self.items.append(item)
        return item

    def render(self):
        head = [
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 675" width="1200" height="675" role="img">',
            f"<title>{e(self.title)}</title>",
            "<defs>"
            f'<marker id="a-blue" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="{BLUE}"/></marker>'
            f'<marker id="a-cyan" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="{CYAN}"/></marker>'
            f'<marker id="a-gray" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="{INK3}"/></marker>'
            f'<marker id="a-ok" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="{OK}"/></marker>'
            f'<marker id="a-alert" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="{ALERT}"/></marker>'
            f'<pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" fill="none" stroke="#E6EEF6" stroke-width="1"/></pattern>'
            "</defs>",
            f'<rect width="1200" height="675" fill="{self.bg}"/>',
        ]
        if self.grid:
            head.append('<rect width="1200" height="675" fill="url(#grid)" opacity=".7"/>')
        if self.kicker:
            head.append(text(48, 56, self.kicker.upper(), 14, 500, CYAN, FM, ls=2.2))
        if self.title:
            head.append(text(48, 94, self.title, 32, 600, INK, FD))
        body = [i if isinstance(i, str) else i.svg() for i in self.items]
        return "\n".join(head + body + ["</svg>"])

    def save(self, path):
        from pathlib import Path
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        Path(path).write_text(self.render(), encoding="utf-8")
        return path


# ---------------------------------------------------------------- equipos
class Box(Node):
    """Caja genérica: título + subtítulo, clara u oscura, con ícono opcional (svg path de 24x24)."""
    def __init__(self, x, y, w, h, title, sub="", dark=False, icon=None, hl=None):
        super().__init__(x, y, w, h)
        self.title, self.sub, self.dark, self.icon, self.hl = title, sub, dark, icon, hl

    def svg(self):
        fill = DEEP if self.dark else WHITE
        stroke = self.hl or (DEEP if self.dark else LINE2)
        sw = 3 if self.hl else 2
        tx = self.x + (64 if self.icon else 20)
        out = [f'<rect x="{self.x}" y="{self.y}" width="{self.w}" height="{self.h}" rx="16" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>']
        if self.icon:
            out.append(f'<g transform="translate({self.x + 20} {self.y + self.h / 2 - 16}) scale(1.35)" fill="none" stroke="{CYAN if self.dark else BLUE}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{self.icon}</g>')
        ty = self.y + self.h / 2 + (-4 if self.sub else 6)
        out.append(text(tx, ty, self.title, 19, 600, WHITE if self.dark else INK))
        if self.sub:
            out.append(text(tx, ty + 23, self.sub, 15, 400, "#9FC3E3" if self.dark else INK3, FM))
        return "".join(out)


ICON = {
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c-3 3-3 15 0 18M12 3c3 3 3 15 0 18"/>',
    "laptop": '<rect x="4" y="5" width="16" height="11" rx="1.5"/><path d="M2 19h20"/>',
    "phone": '<rect x="7" y="2.5" width="10" height="19" rx="2"/><path d="M11 18h2"/>',
    "server": '<rect x="4" y="3" width="16" height="7" rx="1.5"/><rect x="4" y="14" width="16" height="7" rx="1.5"/><path d="M7.5 6.5h.01M7.5 17.5h.01"/>',
    "camera": '<path d="M3 8.5 15 5l2 5-12 3.5z"/><path d="m17 10 3.5 1.5M9 13l1 4M6 17h8"/>',
    "lock": '<rect x="5" y="10" width="14" height="11" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/>',
    "bolt": '<path d="M13 2 4 14h7l-1 8 9-12h-7z"/>',
    "cloud": '<path d="M7 18h10a4 4 0 0 0 .5-8A6 6 0 0 0 6 9.5 4.3 4.3 0 0 0 7 18z"/>',
    "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
    "door": '<rect x="6" y="2.5" width="12" height="19" rx="2"/><circle cx="15" cy="12" r="1"/>',
    "bell": '<path d="M6 16V11a6 6 0 0 1 12 0v5l2 2H4z"/><path d="M10 21h4"/>',
    "shield": '<path d="M12 3 4.5 6v5.5c0 4.6 3.2 8.4 7.5 9.5 4.3-1.1 7.5-4.9 7.5-9.5V6z"/>',
    "key": '<circle cx="8" cy="15" r="4"/><path d="m11 12 8.5-8.5M16 7l2.5 2.5"/>',
    "card": '<rect x="3" y="6" width="18" height="12" rx="2"/><path d="M3 10h18"/>',
    "elevator": '<rect x="5" y="2.5" width="14" height="19" rx="2"/><path d="m9 8 3-3 3 3M9 16l3 3 3-3"/>',
    "flame": '<path d="M12 21c-3.9 0-6.5-2.6-6.5-6.2 0-3.2 2.2-5.3 3.6-7.6.4 1.6 1.3 2.7 2.4 3.3.1-2.8 1.3-5.2 3.4-7.5.3 3 1.7 4.6 3 6.4.9 1.3 1.6 2.8 1.6 4.9 0 3.9-3 6.7-7.5 6.7z"/>',
    "wifi": '<path d="M5 12.5a10 10 0 0 1 14 0M8 15.5a5.5 5.5 0 0 1 8 0M2 9.5a14.5 14.5 0 0 1 20 0"/><circle cx="12" cy="19" r="1"/>',
    "tunnel": '<path d="M3 18V11a9 9 0 0 1 18 0v7"/><path d="M7 18v-6a5 5 0 0 1 10 0v6"/>',
    "check": '<path d="m5 12.5 4.5 4.5L19 7.5"/>',
    "x": '<path d="M6 6l12 12M18 6 6 18"/>',
    "warn": '<path d="M12 3 2 20h20z"/><path d="M12 9v5M12 17h.01"/>',
}


class Router(Node):
    """Router/switch con puertos etiquetados. ports=['ether1',...]. hl={'ether2': CYAN} resalta puertos.
    Anclas: .port('ether2') = punto debajo del puerto. Ancho automático."""
    def __init__(self, x, y, name="Router", sub="", ports=("ether1", "ether2", "ether3", "ether4", "ether5"), hl=None, dark=True, extra=None):
        pw, gap = 74, 10
        w = max(300, 40 + len(ports) * (pw + gap) - gap)
        super().__init__(x, y, w, 170)
        self.name, self.sub, self.ports, self.hl, self.dark, self.extra = name, sub, list(ports), hl or {}, dark, extra
        self.pw, self.gap = pw, gap
        for i, p in enumerate(self.ports):
            px = x + 20 + i * (pw + gap)
            self.anchors[p] = (px + pw / 2, y + self.h)

    def svg(self):
        x, y, w, h = self.x, self.y, self.w, self.h
        fill = DEEP if self.dark else WHITE
        out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="20" fill="{fill}" stroke="{DEEP if self.dark else LINE2}" stroke-width="2"/>',
               text(x + 20, y + 38, self.name, 21, 600, WHITE if self.dark else INK, FD)]
        if self.sub:
            out.append(text(x + 20, y + 62, self.sub, 15, 400, "#9FC3E3" if self.dark else INK3, FM))
        if self.extra:
            out.append(text(x + w - 20, y + 38, self.extra, 15, 500, CYAN, FM, anchor="end"))
        for i, p in enumerate(self.ports):
            px = x + 20 + i * (self.pw + self.gap)
            c = self.hl.get(p)
            out.append(f'<rect x="{px}" y="{y + 92}" width="{self.pw}" height="54" rx="8" fill="{c or ("#0B3A66" if self.dark else SOFT)}" stroke="{c or ("#4E7396" if self.dark else LINE2)}" stroke-width="2"/>')
            out.append(f'<rect x="{px + 20}" y="{y + 102}" width="{self.pw - 40}" height="18" rx="2" fill="none" stroke="{WHITE if (c or self.dark) else INK3}" stroke-width="1.5" opacity=".8"/>')
            lbl = p if len(p) <= 9 else p[:8] + "…"
            out.append(text(px + self.pw / 2, y + 138, lbl, 13 if len(lbl) > 6 else 14, 600 if c else 500, WHITE if (c or self.dark) else INK2, FM, anchor="middle"))
        return "".join(out)


def _dev(x, y, w, h, title, sub, icon, hl=None, dark=False):
    return Box(x, y, w, h, title, sub, dark=dark, icon=ICON[icon], hl=hl)


def Laptop(x, y, title="Notebook", sub="", hl=None, w=230): return _dev(x, y, w, 84, title, sub, "laptop", hl)
def Phone(x, y, title="Celular", sub="", hl=None, w=210): return _dev(x, y, w, 84, title, sub, "phone", hl)
def Server(x, y, title="Servidor", sub="", hl=None, w=230): return _dev(x, y, w, 84, title, sub, "server", hl)
def Camera(x, y, title="Cámara IP", sub="", hl=None, w=220): return _dev(x, y, w, 84, title, sub, "camera", hl)
def Internet(x, y, title="Internet", sub="", hl=None, w=210): return _dev(x, y, w, 84, title, sub, "globe", hl)
def CloudBox(x, y, title="Nube", sub="", hl=None, w=220): return _dev(x, y, w, 84, title, sub, "cloud", hl)
def Person(x, y, title="Usuario", sub="", hl=None, w=210): return _dev(x, y, w, 84, title, sub, "user", hl)
def Lock(x, y, title="Cerradura", sub="", hl=None, w=220): return _dev(x, y, w, 84, title, sub, "lock", hl)
def PSU(x, y, title="Fuente 12 V", sub="", hl=None, w=220): return _dev(x, y, w, 84, title, sub, "bolt", hl)
def Generic(x, y, title, sub="", icon="server", hl=None, w=230, dark=False): return _dev(x, y, w, 84, title, sub, icon, hl, dark)


class Intercom(Node):
    """Portero de calle genérico (frente vertical: cámara, pantalla o teclado, botón). Anclas: 'relayA', 'relayB', 'eth', 'power' a la derecha."""
    def __init__(self, x, y, title="Portero", sub="", keypad=False, screen=False, hl=None):
        super().__init__(x, y, 150, 260)
        self.title, self.sub, self.keypad, self.screen, self.hl = title, sub, keypad, screen, hl or {}
        for i, a in enumerate(["eth", "power", "relayA", "relayB"]):
            self.anchors[a] = (x + 150, y + 70 + i * 42)

    def svg(self):
        x, y = self.x, self.y
        out = [f'<rect x="{x}" y="{y}" width="150" height="260" rx="20" fill="#26323F" stroke="{DEEP}" stroke-width="2"/>',
               f'<circle cx="{x + 75}" cy="{y + 34}" r="13" fill="#0B1A28" stroke="#5B6F84" stroke-width="2"/><circle cx="{x + 75}" cy="{y + 34}" r="5" fill="{CYAN}"/>']
        if self.screen:
            out.append(f'<rect x="{x + 22}" y="{y + 62}" width="106" height="92" rx="8" fill="#0B1A28" stroke="#5B6F84"/>')
        elif self.keypad:
            for r in range(4):
                for k in range(3):
                    out.append(f'<rect x="{x + 33 + k * 30}" y="{y + 66 + r * 26}" width="24" height="20" rx="4" fill="#3A4A5C"/>')
        else:
            out.append(f'<rect x="{x + 30}" y="{y + 72}" width="90" height="60" rx="8" fill="#3A4A5C"/>')
        out.append(f'<circle cx="{x + 75}" cy="{y + 196}" r="22" fill="#3A4A5C" stroke="{CYAN}" stroke-width="2"/>')
        out.append(text(x + 75, y + 290, self.title, 18, 600, INK, FB, anchor="middle"))
        if self.sub:
            out.append(text(x + 75, y + 312, self.sub, 15, 400, INK3, FM, anchor="middle"))
        return "".join(out)


class Monitor(Node):
    """Monitor interior genérico (pantalla horizontal). Anclas a la izquierda: 'eth', 'power', 'relay'."""
    def __init__(self, x, y, title="Monitor interior", sub="", hl=None):
        super().__init__(x, y, 240, 160)
        self.title, self.sub, self.hl = title, sub, hl
        for i, a in enumerate(["eth", "power", "relay"]):
            self.anchors[a] = (x, y + 40 + i * 40)

    def svg(self):
        x, y = self.x, self.y
        return (f'<rect x="{x}" y="{y}" width="240" height="160" rx="18" fill="#F1F4F7" stroke="{self.hl or LINE2}" stroke-width="{3 if self.hl else 2}"/>'
                f'<rect x="{x + 16}" y="{y + 16}" width="208" height="112" rx="8" fill="#0B1A28"/>'
                f'<circle cx="{x + 120}" cy="{y + 144}" r="6" fill="{INK3}"/>'
                + text(x + 120, y + 188, self.title, 18, 600, INK, FB, anchor="middle")
                + (text(x + 120, y + 210, self.sub, 15, 400, INK3, FM, anchor="middle") if self.sub else ""))


class Relay(Node):
    """Relé con bornes COM / NO / NC. Anclas: 'COM', 'NO', 'NC' abajo; 'in' arriba."""
    def __init__(self, x, y, title="Relé A", sub="", hl=None):
        super().__init__(x, y, 200, 110)
        self.title, self.sub, self.hl = title, sub, hl
        for i, a in enumerate(["COM", "NO", "NC"]):
            self.anchors[a] = (x + 40 + i * 60, y + 110)
        self.anchors["in"] = (x + 100, y)

    def svg(self):
        x, y = self.x, self.y
        out = [f'<rect x="{x}" y="{y}" width="200" height="110" rx="14" fill="{WHITE}" stroke="{self.hl or LINE2}" stroke-width="{3 if self.hl else 2}"/>',
               text(x + 16, y + 30, self.title, 17, 600, INK), text(x + 16, y + 50, self.sub, 14, 400, INK3, FM) if self.sub else ""]
        for i, a in enumerate(["COM", "NO", "NC"]):
            cx = x + 40 + i * 60
            out.append(f'<circle cx="{cx}" cy="{y + 80}" r="9" fill="{SOFT}" stroke="{BLUE}" stroke-width="2"/>')
            out.append(text(cx, y + 104, a, 13, 600, INK2, FM, anchor="middle"))
        return "".join(out)


class Window(Node):
    """Ventana de programa o interfaz web genérica. rows = [(etiqueta, valor), ...]; hl = índice de fila resaltada."""
    def __init__(self, x, y, w, h, title, rows=(), hl=None, path=None):
        super().__init__(x, y, w, h)
        self.title, self.rows, self.hl, self.path = title, list(rows), hl, path

    def svg(self):
        x, y, w, h = self.x, self.y, self.w, self.h
        out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{WHITE}" stroke="{LINE2}" stroke-width="2"/>',
               f'<path d="M{x} {y + 14}a14 14 0 0 1 14 -14h{w - 28}a14 14 0 0 1 14 14v26h-{w}z" fill="{SOFT}"/>',
               f'<circle cx="{x + 20}" cy="{y + 20}" r="5" fill="{LINE2}"/><circle cx="{x + 38}" cy="{y + 20}" r="5" fill="{LINE2}"/><circle cx="{x + 56}" cy="{y + 20}" r="5" fill="{LINE2}"/>',
               text(x + 76, y + 26, self.title, 15, 600, INK2, FB)]
        yy = y + 52
        if self.path:
            out.append(text(x + 18, yy + 14, self.path, 15, 500, BLUE, FM))
            yy += 30
        for i, (k, v) in enumerate(self.rows):
            if i == self.hl:
                out.append(f'<rect x="{x + 10}" y="{yy - 4}" width="{w - 20}" height="34" rx="8" fill="{SOFT}" stroke="{CYAN}" stroke-width="2"/>')
            out.append(text(x + 20, yy + 18, k, 15, 500, INK2))
            out.append(text(x + w - 20, yy + 18, v, 15, 500, INK, FM, anchor="end"))
            yy += 38
        return "".join(out)


class Terminal(Node):
    """Terminal con líneas de comando. lines: str o (str, color)."""
    def __init__(self, x, y, w, lines, title="Terminal"):
        super().__init__(x, y, w, 52 + 26 * len(lines))
        self.lines, self.title = lines, title

    def svg(self):
        x, y, w, h = self.x, self.y, self.w, self.h
        out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="#03213C"/>',
               text(x + 18, y + 26, self.title, 13, 500, "#7FA6C9", FM, ls=1.5)]
        for i, ln in enumerate(self.lines):
            s, c = (ln, "#D9E9F8") if isinstance(ln, str) else ln
            out.append(text(x + 18, y + 56 + i * 26, s, 15, 400, c, FM))
        return "".join(out)


# ---------------------------------------------------------------- conexiones y anotaciones
class Cable:
    """kind: data | power+ | power- | relay | wifi | logical | flow (flecha). arrow=True agrega punta."""
    STY = {"data": (BLUE, 4, None), "power+": (RED, 4, None), "power-": (BLACK, 4, None), "relay": (CYAN, 4, None),
           "wifi": (BLUE, 3, "2 9"), "logical": (INK3, 3, "8 8"), "flow": (BLUE, 3, None), "ok": (OK, 3, None), "alert": (ALERT, 3, "8 6")}

    def __init__(self, a, b, kind="data", label=None, arrow=None, bend="auto", label_at=0.5, label_dy=-12):
        self.a, self.b, self.kind, self.label, self.bend, self.label_at, self.label_dy = a, b, kind, label, bend, label_at, label_dy
        self.arrow = arrow if arrow is not None else kind in ("flow", "logical", "ok", "alert")

    def svg(self):
        (x1, y1), (x2, y2) = self.a, self.b
        col, sw, dash = self.STY[self.kind]
        mk = {BLUE: "a-blue", CYAN: "a-cyan", INK3: "a-gray", OK: "a-ok", ALERT: "a-alert"}.get(col, "a-blue")
        if self.bend == "straight":
            d = f"M{x1:.1f} {y1:.1f}L{x2:.1f} {y2:.1f}"
        elif self.bend == "elbow":
            my = (y1 + y2) / 2
            d = f"M{x1:.1f} {y1:.1f}V{my:.1f}H{x2:.1f}V{y2:.1f}"
        else:
            dx, dy = x2 - x1, y2 - y1
            if abs(dy) > abs(dx):
                d = f"M{x1:.1f} {y1:.1f}C{x1:.1f} {y1 + dy * .55:.1f},{x2:.1f} {y2 - dy * .55:.1f},{x2:.1f} {y2:.1f}"
            else:
                d = f"M{x1:.1f} {y1:.1f}C{x1 + dx * .5:.1f} {y1:.1f},{x2 - dx * .5:.1f} {y2:.1f},{x2:.1f} {y2:.1f}"
        out = [f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{sw}" stroke-linecap="round"' + (f' stroke-dasharray="{dash}"' if dash else "") + (f' marker-end="url(#{mk})"' if self.arrow else "") + "/>"]
        if self.kind in ("data", "power+", "power-", "relay"):
            out.append(f'<circle cx="{x1:.1f}" cy="{y1:.1f}" r="5" fill="{col}"/><circle cx="{x2:.1f}" cy="{y2:.1f}" r="5" fill="{col}"/>')
        if self.label:
            t = self.label_at
            lx, ly = x1 + (x2 - x1) * t, y1 + (y2 - y1) * t + self.label_dy
            wpx = len(self.label) * 8.6 + 22
            out.append(f'<rect x="{lx - wpx / 2:.1f}" y="{ly - 19:.1f}" width="{wpx:.1f}" height="28" rx="14" fill="{WHITE}" stroke="{col}" stroke-width="1.5"/>')
            out.append(text(lx, ly, self.label, 14, 600, col if col not in (BLACK,) else INK, FM, anchor="middle"))
        return "".join(out)


def Arrow(a, b, label=None, kind="flow", **kw):
    return Cable(a, b, kind=kind, label=label, arrow=True, **kw)


class Step:
    """Número de paso en círculo (coincide con el número del paso del laboratorio)."""
    def __init__(self, x, y, n, color=CYAN):
        self.x, self.y, self.n, self.color = x, y, n, color

    def svg(self):
        return f'<circle cx="{self.x}" cy="{self.y}" r="17" fill="{self.color}" stroke="{WHITE}" stroke-width="3"/>' + text(self.x, self.y + 6, self.n, 17, 700, WHITE, FD, anchor="middle")


class Note:
    """Nota o explicación en tarjeta. kind: info | ok | warn | alert. title opcional."""
    def __init__(self, x, y, w, body, title=None, kind="info", size=16):
        self.x, self.y, self.w, self.body, self.title, self.kind, self.size = x, y, w, body, title, kind, size

    def svg(self):
        bg, fg = {"info": (WHITE, BLUE), "ok": (OK_BG, OK), "warn": (WARN_BG, WARN), "alert": (ALERT_BG, ALERT)}[self.kind]
        pad = 18
        t_svg, th = ("", 0)
        if self.title:
            t_svg, th = wrap(self.x + pad + 8, self.y + pad + 16, self.title, self.w - 2 * pad - 8, 17, 600, INK)
            th += 4
        b_svg, bh = wrap(self.x + pad + 8, self.y + pad + 16 + th, self.body, self.w - 2 * pad - 8, self.size, 400, INK2)
        h = pad * 2 + th + bh - 4
        return (f'<rect x="{self.x}" y="{self.y}" width="{self.w}" height="{h:.0f}" rx="14" fill="{bg}" stroke="{LINE if self.kind == "info" else bg}" stroke-width="1.5"/>'
                f'<rect x="{self.x}" y="{self.y + 12}" width="5" height="{h - 24:.0f}" rx="2.5" fill="{fg}"/>' + t_svg + b_svg)


class Chip:
    """Etiqueta corta (IP, puerto, estado). kind: blue | cyan | ok | warn | alert | gray."""
    def __init__(self, x, y, s, kind="blue", mono=True, anchor="start"):
        self.x, self.y, self.s, self.kind, self.mono, self.anchor = x, y, s, kind, mono, anchor

    def svg(self):
        bg, fg = {"blue": (BLUE, WHITE), "cyan": (CYAN, WHITE), "ok": (OK_BG, OK), "warn": (WARN_BG, WARN), "alert": (ALERT_BG, ALERT), "gray": (SOFT, INK2), "dark": (DEEP, WHITE)}[self.kind]
        w = len(self.s) * (9.2 if self.mono else 8.4) + 26
        x = self.x - (w / 2 if self.anchor == "middle" else 0)
        return f'<rect x="{x:.1f}" y="{self.y - 21}" width="{w:.1f}" height="30" rx="15" fill="{bg}"/>' + text(x + w / 2, self.y, self.s, 15, 600, fg, FM if self.mono else FB, anchor="middle")


class Table:
    """Tabla simple. head = [..], rows = [[..]], widths = [px..]. hl_row resalta una fila."""
    def __init__(self, x, y, head, rows, widths, hl_row=None, row_h=38, mono_cols=()):
        self.x, self.y, self.head, self.rows, self.widths, self.hl, self.rh, self.mono = x, y, head, rows, widths, hl_row, row_h, set(mono_cols)

    def svg(self):
        x, y, W = self.x, self.y, sum(self.widths)
        out = [f'<rect x="{x}" y="{y}" width="{W}" height="{self.rh * (len(self.rows) + 1)}" rx="12" fill="{WHITE}" stroke="{LINE2}" stroke-width="1.5"/>',
               f'<path d="M{x} {y + 12}a12 12 0 0 1 12 -12h{W - 24}a12 12 0 0 1 12 12v{self.rh - 12}h-{W}z" fill="{SOFT}"/>']
        cx = x
        for i, (hd, w) in enumerate(zip(self.head, self.widths)):
            out.append(text(cx + 14, y + self.rh / 2 + 5, hd.upper(), 13, 600, INK3, FM, ls=1.2))
            cx += w
        for r, row in enumerate(self.rows):
            ry = y + self.rh * (r + 1)
            if r == self.hl:
                out.append(f'<rect x="{x + 4}" y="{ry + 3}" width="{W - 8}" height="{self.rh - 6}" rx="8" fill="{SOFT}" stroke="{CYAN}" stroke-width="1.5"/>')
            elif r:
                out.append(f'<path d="M{x + 12} {ry}H{x + W - 12}" stroke="{LINE}" stroke-width="1"/>')
            cx = x
            for i, (cell, w) in enumerate(zip(row, self.widths)):
                out.append(text(cx + 14, ry + self.rh / 2 + 5, cell, 15, 600 if i == 0 else 400, INK if i == 0 else INK2, FM if i in self.mono else FB))
                cx += w
        return "".join(out)


def Label(x, y, s, size=17, weight=500, color=INK2, font=FB, anchor="start"):
    return text(x, y, s, size, weight, color, font, anchor)


def Mark(x, y, ok=True):
    """Tilde verde o cruz roja en círculo (siempre acompañar con texto)."""
    col, bg, ic = (OK, OK_BG, ICON["check"]) if ok else (ALERT, ALERT_BG, ICON["x"])
    return f'<circle cx="{x}" cy="{y}" r="18" fill="{bg}" stroke="{col}" stroke-width="2"/><g transform="translate({x - 12} {y - 12})" fill="none" stroke="{col}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round">{ic}</g>'


def Zone(x, y, w, h, label, color=LINE2):
    """Zona punteada (red, VLAN, edificio, sitio)."""
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="22" fill="none" stroke="{color}" stroke-width="2" stroke-dasharray="7 7"/>'
            + f'<rect x="{x + 18}" y="{y - 14}" width="{len(label) * 8.8 + 24:.0f}" height="28" rx="14" fill="{GROUND}"/>' + text(x + 30, y + 6, label, 14, 600, color if color != LINE2 else INK3, FM))
