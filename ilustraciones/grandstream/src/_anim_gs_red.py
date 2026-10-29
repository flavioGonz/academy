#!/usr/bin/env python3
"""Ayudantes para las animaciones de Resumen ("Cómo se ve en la red") y Laboratorio del curso Grandstream.

Suma piezas sobre _anim_grandstream.G (que se apoya en tools/anim.py) sin modificar ninguno de los dos:
  - dev(): caja de equipo con ícono (teléfono de escritorio, celular, UCM, router, notebook, nube, fax, alarma…)
  - status(): renglón de abajo que cambia con cada tiempo (qué mirar en ese momento)
  - term(): recuadro oscuro con texto de pantalla (menús de la UCM, líneas de SDP, Active Calls)
  - done(): guarda <id>-<r1|l1|l2>.svg en site2/ilustraciones/grandstream/ y deja la vista previa
    (_rev-<id>-<tipo>-<pct>.png y -fijo.png) en ilustraciones/grandstream/.

  from _anim_gs_red import R
  g = R(T=24, fix=60, kicker="GRANDSTREAM · … · CÓMO SE VE EN LA RED", title="…")
"""
import sys

sys.path.insert(0, "/home/claude/ies-training/ilustraciones/grandstream/src")
from _anim_grandstream import G, SITE, PREV  # noqa: E402
from _fxo import ICO as _ICO  # noqa: E402

ICO = dict(_ICO)
ICO["router"] = ('<rect x="3" y="12" width="18" height="7" rx="1.5"/><path d="M7 15.5h.01M10.5 15.5h.01"/>'
                 '<path d="M8 12 6 6M16 12l2-6"/>')
ICO["ucm"] = '<rect x="3" y="6" width="18" height="12" rx="2"/><path d="M6.5 10h5M6.5 14h3M15 10h.01M17.5 10h.01M15 14h.01M17.5 14h.01"/>'
ICO["antel"] = '<rect x="5" y="3" width="14" height="18" rx="2"/><path d="M8.5 7h7M8.5 11h7M8.5 15h4"/>'
ICO["file"] = '<path d="M6 3h8l4 4v14H6z"/><path d="M14 3v4h4M9 12h6M9 16h6"/>'
ICO["mail"] = '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3.5 6 8.5 7 8.5-7"/>'
ICO["clock"] = '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2"/>'
ICO["bug"] = '<circle cx="12" cy="13" r="6"/><path d="M12 7V4M7 9 4 7M17 9l3-2M6 13H3M18 13h3M7 17l-3 2M17 17l3 2"/>'


class R(G):
    SKY, GOLD, MINT = "#9FC3E3", "#F6C35B", "#5BE0A5"
    USO, LIBRE, GRISP = "#F29A1F", "#0A63B8", "#B9C6D3"

    def ico(self, x, y, name, color=None, scale=1.3, sw=1.8):
        return (f'<g transform="translate({x} {y}) scale({scale})" fill="none" stroke="{color or self.BLUE}" '
                f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">{ICO[name]}</g>')

    def dev(self, x, y, w, h, title, sub=None, icon=None, dark=False, hl=None, sub2=None, tsize=19, ssize=15):
        """Caja de equipo con ícono a la izquierda (si hay), título y una o dos líneas de detalle en mono."""
        fill = self.INK if dark else self.WHITE
        st = "" if dark and not hl else f' stroke="{hl or self.LINE}" stroke-width="{3 if hl else 2}"'
        s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{fill}"{st}/>'
        tx = x + 18
        if icon:
            s += self.ico(x + 16, y + h / 2 - 16, icon, self.CYAN if dark else self.BLUE, 1.35)
            tx = x + 62
        tc = self.WHITE if dark else self.INK
        sc = self.SKY if dark else self.GREY
        lines = [v for v in (sub, sub2) if v]
        y0 = y + h / 2 + 7 - 12 * len(lines)
        s += self.text(tx, y0, title, tsize, tc, self.HEAD, 600)
        for k, v in enumerate(lines):
            s += self.text(tx, y0 + 24 + k * 21, v, ssize, sc, self.MONO, 400)
        return s

    def cloud(self, x, y, w, h, label="internet"):
        return (self.box(x, y, w, h, "#EAF2FA", self.LINE, rx=min(h / 2, 34), sw=2, extra='stroke-dasharray="7 6"')
                + self.text(x + w / 2, y + h / 2 + 5, label, 15, self.GREY, self.MONO, 400, "middle"))

    def wire(self, x1, y1, x2, y2, color=None, w=4, dash=None):
        da = f' stroke-dasharray="{dash}"' if dash else ""
        return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color or self.LINE}" stroke-width="{w}" stroke-linecap="round"{da}/>'

    def term(self, x, y, w, h, title=None, lines=(), size=16, lh=26, color=None):
        """Recuadro oscuro (pantalla, captura, SDP). lines: [(texto, color)] o texto."""
        s = self.box(x, y, w, h, "#03213C", None, rx=14)
        yy = y + 30
        if title:
            s += self.text(x + 20, yy, title, 15, self.SKY, self.MONO)
            yy += lh + 4
        for ln in lines:
            t, c = (ln, None) if isinstance(ln, str) else ln
            s += self.text(x + 20, yy, t, size, c or "#D9E9F8", self.MONO, 600)
            yy += lh
        return s

    def dot(self, color, r=9):
        return f'<circle cx="0" cy="0" r="{r}" fill="{color}" stroke="#FFFFFF" stroke-width="2"/>'

    def status(self, y, items, size=17):
        """items: [(t0, t1, texto, color)] centrado abajo, uno por tiempo."""
        for t0, t1, s, c in items:
            self.appear(self.text(600, y, s, size, c or self.INK, self.SANS, 600, "middle"), t0, t1)

    def port(self, x, y, label, state="libre", w=150, h=44):
        """Puerto FXO con el color del Dashboard: libre (azul), uso (naranja), gris (sin línea / sin configurar)."""
        col = {"libre": self.LIBRE, "uso": self.USO, "gris": self.GRISP}[state]
        txt = {"libre": "libre", "uso": "en uso", "gris": "sin línea"}[state]
        pw = len(txt) * 13 * 0.62 + 18
        return (self.box(x, y, w, h, self.WHITE, col, rx=10, sw=2.5)
                + self.text(x + 16, y + h / 2 + 6, label, 17, self.INK, self.MONO, 600)
                + self.box(x + w - 12 - pw, y + h / 2 - 12, pw, 24, col, rx=12)
                + self.text(x + w - 12 - pw / 2, y + h / 2 + 5, txt, 13, self.WHITE, self.MONO, 600, "middle"))

    def done(self, lid, kind, title, desc, pcts):
        name = f"{lid}-{kind}.svg"
        out = SITE / name
        self.save(str(out), title, desc)
        for old in PREV.glob(f"_rev-{lid}-{kind}-*.png"):
            old.unlink()
        self._last = out
        self.preview(pcts, str(PREV / f"_rev-{lid}-{kind}"))
        kb = out.stat().st_size / 1024
        print(f"{name}: {kb:.0f} KB")
        assert kb < 120, "pesa más de 120 KB"
        assert len(desc) <= 1000, f"alt de {len(desc)} caracteres"
        return out
