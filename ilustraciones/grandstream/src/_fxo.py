"""Piezas para las ilustraciones del módulo de líneas analógicas por FXO (lecciones 13 a 18).

Se apoya en _gs.py (que a su vez usa ilus.py) sin modificarlos:
- UCMAnalog: frente genérico del UCM6304A con FXS 1-4, FXO 1-4 (RJ11) y LAN/WAN. Anclas 'FXO1'..'FXO4', 'FXS1'..
  debajo de cada puerto. state={'FXO1': 'libre'|'uso'|'gris'} colorea el puerto con el código del Dashboard.
- Jack: roseta de pared con RJ11. Ancla .port('par') a la izquierda y 'rj' abajo.
- Meter: multímetro genérico con lectura y puntas (rojo y negro, como los cables de alimentación de la biblioteca).
- par(): el par telefónico (dos hilos) dibujado como línea doble gris oscuro, con etiqueta.
- ico(): íconos propios (fax, alarma, posnet) en el mismo trazo que ilus.ICON.
"""
import sys
sys.path.insert(0, "/home/claude/ies-training/ilustraciones/grandstream/src")
from _gs import *  # noqa
from _gs import text, wrap, Node  # noqa

PAR = "#3B4D61"          # color del par telefónico (no es un cable de datos)
LIBRE, USO, GRIS = BLUE, "#F29A1F", "#B9C6D3"   # colores del Dashboard: libre (azul en firmware actual), en uso, sin línea

ICO = {
    "fax": '<rect x="6" y="3" width="12" height="6" rx="1"/><rect x="3" y="9" width="18" height="9" rx="2"/><path d="M7 18v3h10v-3M7 13h4"/>',
    "alarma": '<path d="M12 3 4.5 6v5.5c0 4.6 3.2 8.4 7.5 9.5 4.3-1.1 7.5-4.9 7.5-9.5V6z"/><path d="M12 8v5M12 16h.01"/>',
    "posnet": '<rect x="6" y="2.5" width="12" height="19" rx="2"/><rect x="8.5" y="5" width="7" height="4" rx=".5"/><path d="M9 13h.01M12 13h.01M15 13h.01M9 16h.01M12 16h.01M15 16h.01"/>',
    "tel": '<path d="M5 9c0-3 3.5-5 7-5s7 2 7 5l-2.5 1.5L14 9V7.5h-4V9l-2.5 1.5z"/><rect x="5" y="12" width="14" height="8" rx="2"/><path d="M9 15h.01M12 15h.01M15 15h.01M9 17.5h.01M12 17.5h.01M15 17.5h.01"/>',
    "central": '<rect x="4" y="3" width="16" height="18" rx="2"/><path d="M8 7h8M8 11h8M8 15h5"/>',
}

ICO.update({k: v for k, v in ICON.items() if k not in ICO})   # también los de ilus.py (phone, server, bell...)


def ico(x, y, name, color=BLUE, scale=1.3, sw=1.8):
    return f'<g transform="translate({x} {y}) scale({scale})" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">{ICO[name]}</g>'


def dev(x, y, title, sub="", icon="tel", w=230, hl=None, dark=False, h=84):
    """Caja de equipo con ícono propio (mismo estilo que Generic de ilus.py)."""
    bg, fg, st = (DEEP, WHITE, DEEP) if dark else (WHITE, INK, hl or LINE2)
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{bg}" stroke="{st}" stroke-width="{3 if hl else 2}"/>',
           ico(x + 18, y + h / 2 - 16, icon, CYAN if dark else (hl or BLUE), 1.35),
           text(x + 64, y + (h / 2 - 2 if sub else h / 2 + 6), title, 18, 600, fg, FB)]
    if sub:
        out.append(text(x + 64, y + h / 2 + 20, sub, 15, 400, "#9FC3E3" if dark else INK3, FM))
    return "".join(out)


def par(points, label=None, at=0.5, dy=-12, color=PAR, dash=None, w=3):
    """Par telefónico: línea doble (dos hilos) por la polilínea points, con puntos en las puntas."""
    d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in points)
    ds = f' stroke-dasharray="{dash}"' if dash else ""
    s = (f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{w + 4}" stroke-linejoin="round" stroke-linecap="round"{ds}/>'
         f'<path d="{d}" fill="none" stroke="{GROUND}" stroke-width="{max(1, w - 1.5)}" stroke-linejoin="round" stroke-linecap="round"{ds}/>')
    (x1, y1), (x2, y2) = points[0], points[-1]
    s += f'<circle cx="{x1:.1f}" cy="{y1:.1f}" r="5" fill="{color}"/><circle cx="{x2:.1f}" cy="{y2:.1f}" r="5" fill="{color}"/>'
    if label:
        # etiqueta sobre el tramo más largo
        segs = list(zip(points[:-1], points[1:]))
        (ax, ay), (bx, by) = max(segs, key=lambda sg: abs(sg[1][0] - sg[0][0]) + abs(sg[1][1] - sg[0][1]))
        lx, ly = ax + (bx - ax) * at, ay + (by - ay) * at
        s += pill(lx, ly + dy, label, color, WHITE, size=14, mono=False)
    return s


class UCMAnalog(Node):
    """Frente del UCM6304A (genérico): FXS 1-4 y FXO 1-4 en RJ11 y los puertos de red."""
    def __init__(self, x, y, w=600, name="UCM6304A", sub="4 FXS · 4 FXO", state=None, hl=None, net=True, h=170, top=False):
        super().__init__(x, y, w, h)
        self.name, self.sub, self.state, self.hl, self.net, self.top = name, sub, state or {}, hl or {}, net, top
        self.pw, self.gap = 44, 10
        gx = x + 24
        self.groups = []
        for g in ("FXS", "FXO"):
            self.groups.append((g, gx))
            for i in range(4):
                px = gx + i * (self.pw + self.gap)
                self.anchors[f"{g}{i + 1}"] = (px + self.pw / 2, y if top else y + h)
            gx += 4 * (self.pw + self.gap) + 26

    def svg(self):
        x, y, w, h = self.x, self.y, self.w, self.h
        out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="{DEEP}"/>']
        ty = y + h - 50 if self.top else y + 38
        out.append(text(x + 24, ty, self.name, 21, 600, WHITE, FD))
        if self.sub:
            out.append(text(x + 24, ty + 24, self.sub, 15, 400, "#9FC3E3", FM))
        py = y + 14 if self.top else y + h - 52
        for g, gx in self.groups:
            out.append(text(gx, py + 58 if self.top else y + h - 66, g, 15, 600, "#9FC3E3", FM))
            for i in range(4):
                name = f"{g}{i + 1}"
                px = gx + i * (self.pw + self.gap)
                st = self.state.get(name)
                fill = {"libre": LIBRE, "uso": USO, "gris": "#2C4A66"}.get(st, "#0B3A66")
                stroke = self.hl.get(name) or {"libre": LIBRE, "uso": USO}.get(st, "#4E7396")
                sw = 3 if self.hl.get(name) else 2
                out.append(f'<rect x="{px}" y="{py}" width="{self.pw}" height="38" rx="7" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
                out.append(f'<rect x="{px + 12}" y="{py + 6}" width="{self.pw - 24}" height="10" rx="2" fill="none" stroke="{WHITE}" stroke-width="1.4" opacity=".75"/>')
                out.append(text(px + self.pw / 2, py + 32, str(i + 1), 15, 600, WHITE, FM, anchor="middle"))
        if self.net:
            nx = x + w - 120
            y = (y - 10) if self.top else y
            for i, p in enumerate(("LAN", "WAN")):
                out.append(f'<rect x="{nx + i * 52}" y="{y + 24}" width="44" height="34" rx="6" fill="#0B3A66" stroke="#4E7396" stroke-width="2"/>')
                out.append(text(nx + i * 52 + 22, y + 78, p, 15, 600, "#7FA6C9", FM, anchor="middle"))
        return "".join(out)


class Jack(Node):
    """Roseta de pared con RJ11. Anclas: 'par' (entrada del par, a la izquierda) y 'rj' (abajo, donde va el cable)."""
    def __init__(self, x, y, title="Roseta", sub="", w=150, h=120, hl=None):
        super().__init__(x, y, w, h)
        self.title, self.sub, self.hl = title, sub, hl
        self.anchors["par"] = (x, y + 50)
        self.anchors["rj"] = (x + w / 2, y + h)
        self.anchors["top"] = (x + w / 2, y)

    def svg(self):
        x, y, w, h = self.x, self.y, self.w, self.h
        st = self.hl or LINE2
        out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{WHITE}" stroke="{st}" stroke-width="{3 if self.hl else 2}"/>',
               f'<rect x="{x + w / 2 - 22}" y="{y + 30}" width="44" height="34" rx="5" fill="#0B1A28"/>',
               f'<rect x="{x + w / 2 - 8}" y="{y + 62}" width="16" height="6" fill="#0B1A28"/>',
               f'<path d="M{x + w / 2 - 6} {y + 34}v10M{x + w / 2 + 6} {y + 34}v10" stroke="#E7C66A" stroke-width="2.5"/>',
               text(x + w / 2, y + 92, self.title, 16, 600, INK, FB, anchor="middle")]
        if self.sub:
            out.append(text(x + w / 2, y + 111, self.sub, 14, 400, INK3, FM, anchor="middle"))
        return "".join(out)


class Meter(Node):
    """Multímetro genérico. reading: texto del display; mode: texto chico debajo. Anclas 'rojo' y 'negro' arriba."""
    def __init__(self, x, y, reading="__ V", mode="V CC", w=170, h=210, title=None):
        super().__init__(x, y, w, h)
        self.reading, self.mode, self.title = reading, mode, title
        self.anchors["rojo"] = (x + w * 0.32, y)
        self.anchors["negro"] = (x + w * 0.68, y)

    def svg(self):
        x, y, w, h = self.x, self.y, self.w, self.h
        out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="20" fill="#F2B233" stroke="#B57F12" stroke-width="2"/>',
               f'<rect x="{x + 14}" y="{y + 16}" width="{w - 28}" height="62" rx="8" fill="#DCE8D2" stroke="#7A8F6B" stroke-width="2"/>',
               text(x + w / 2, y + 58, self.reading, 26, 700, "#1E2B16", FM, anchor="middle"),
               f'<circle cx="{x + w / 2}" cy="{y + 132}" r="32" fill="#2B2B2B"/>',
               f'<path d="M{x + w / 2} {y + 132}l18 -20" stroke="#F2B233" stroke-width="5" stroke-linecap="round"/>',
               text(x + w / 2, y + 190, self.mode, 15, 700, "#2B2B2B", FM, anchor="middle")]
        if self.title:
            out.append(text(x + w / 2, y + h + 26, self.title, 16, 600, INK, FB, anchor="middle"))
        return "".join(out)


def probe(a, b, color):
    """Punta del multímetro: cable de a (multímetro) a b (contacto)."""
    (x1, y1), (x2, y2) = a, b
    my = (y1 + y2) / 2
    return (f'<path d="M{x1} {y1} C{x1} {my} {x2} {my} {x2} {y2}" fill="none" stroke="{color}" stroke-width="4" stroke-linecap="round"/>'
            f'<circle cx="{x2}" cy="{y2}" r="6" fill="{color}"/>')


def legend_state(x, y, items, size=15):
    """Leyenda de estados del Dashboard: items = [(color, texto)]."""
    out, yy = [], y
    for col, s in items:
        out.append(f'<rect x="{x}" y="{yy - 15}" width="30" height="22" rx="5" fill="{col}"/>')
        out.append(text(x + 42, yy, s, size, 500, INK2, FB))
        yy += 34
    return "".join(out)
