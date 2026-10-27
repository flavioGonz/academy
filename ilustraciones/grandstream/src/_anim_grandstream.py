#!/usr/bin/env python3
"""Ayudantes para las animaciones de teoría del curso Grandstream (lecciones 1 a 12).

Se apoyan en tools/anim.py sin modificarla. Idea central: cada animación fija un instante FIX
(porcentaje del ciclo) y todo lo que se ve en ese instante es lo que queda en el cuadro fijo
(reducir movimiento). Así el cuadro fijo es siempre un fotograma real y coherente.

  from _anim_grandstream import G
  g = G(T=24, fix=60, kicker="GRANDSTREAM · SIP", title="…")
  g.steps([...])                       # el paso que contiene FIX queda fijo
  g.appear(svg, 10, 40)                # visible entre 10 % y 40 %
  g.arrow([(x1, y1), (x2, y2)], 10, 14, color)   # flecha que se dibuja sola
  g.token([(x1, y1), (x2, y2)], 10, 14, g.chip("REGISTER"))
  g.finish(2, 1, "Título", "Descripción", [8, 30, 50, 70, 92])
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, "/home/claude/ies-training/tools")
from anim import Anim  # noqa: E402

SITE = Path("/home/claude/ies-training/site2/ilustraciones/grandstream")
PREV = Path("/home/claude/ies-training/ilustraciones/grandstream")


def _len(p, q):
    return math.hypot(q[0] - p[0], q[1] - p[1])


class G(Anim):
    def __init__(self, T=24, fix=50, kicker="", title=""):
        super().__init__(T=T, kicker=kicker, title=title)
        self.FIX = fix

    # ---------- visibilidad
    def st(self, t0, t1=100):
        """1 si el instante fijo cae dentro de [t0, t1)."""
        return 1 if t0 <= self.FIX < t1 else 0

    def steps(self, captions, **kw):
        k = len(captions)
        idx = min(int(self.FIX // (100 / k)), k - 1)
        return super().steps(captions, still=idx, **kw)

    def appear(self, inner, t0=0, t1=100, fade=1.0, still=None):
        if t0 <= 0 and t1 >= 100:
            return self.add(inner)
        s = self.st(t0, t1) if still is None else still
        return self.add(self.group(inner, self.show(t0, t1, fade), still=s))

    def fijo_only(self, inner):
        """Solo en el cuadro fijo (movimiento reducido): mientras corre, invisible."""
        return self.add(self.group(inner, self.keyframes([(0, 0), (100, 0)]), still=1))

    def _cls(self, base, *names):
        self.n += 1
        c = f"c{self.n}"
        anims = ",".join(f"{n} {self.T}s linear infinite" for n in names)
        self.css.append(f".{c}{{{base}animation:{anims}}}")
        return c

    # ---------- flechas y fichas
    def parrow(self, d, color=None, width=3, dash=""):
        """Flecha fija por un path d (la de anim.py)."""
        return Anim.arrow(self, d, color, width, dash)

    @staticmethod
    def head(p, q, color, size=13):
        ang = math.atan2(q[1] - p[1], q[0] - p[0])
        x, y = q
        l, w = size, size * 0.55
        bx, by = x - l * math.cos(ang), y - l * math.sin(ang)
        px, py = -math.sin(ang) * w, math.cos(ang) * w
        return f'<path d="M{x:.1f} {y:.1f} L{bx + px:.1f} {by + py:.1f} L{bx - px:.1f} {by - py:.1f} z" fill="{color}"/>'

    def arrow(self, pts, t0, t1, color=None, hold=100, width=3, dashed=False, head=True, still=None):
        """Flecha por la polilínea pts: se dibuja entre t0 y t1 y queda hasta hold."""
        color = color or self.BLUE
        s = self.st(t0, hold) if still is None else still
        p, q = pts[-2], pts[-1]
        L = _len(p, q)
        k = max(0, (L - 9) / L) if (L and head) else 1
        qq = (p[0] + (q[0] - p[0]) * k, p[1] + (q[1] - p[1]) * k)
        d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts[:-1]) + f" L{qq[0]:.1f} {qq[1]:.1f}"
        vis = self.show(t0, hold, 0.6)
        hd = self.head(p, q, color) if head else ""
        if dashed:
            line = f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" stroke-dasharray="9 7" stroke-linecap="round"/>'
            self.add(self.group(line + hd, vis, still=s))
            return
        dash = self.keyframes([(0, 100), (t0, 100), (t1, 0), (100, 0)], prop="stroke-dashoffset")
        c = self._cls("stroke-dashoffset:0;", dash)
        line = f'<path class="{c}" d="{d}" pathLength="100" stroke-dasharray="100 100" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round"/>'
        self.add(self.group(line, vis, still=s))
        if head:
            self.add(self.group(hd, self.show(t1, hold, 0.4), still=s))

    def token(self, pts, t0, t1, inner, hold=None, still=0):
        """Mueve inner (dibujado alrededor de 0,0) por pts entre t0 y t1."""
        total = sum(_len(pts[i], pts[i + 1]) for i in range(len(pts) - 1)) or 1
        kf = [(0, pts[0][0], pts[0][1]), (t0, pts[0][0], pts[0][1])]
        acc = 0
        for i in range(len(pts) - 1):
            acc += _len(pts[i], pts[i + 1])
            kf.append((t0 + (t1 - t0) * acc / total, pts[i + 1][0], pts[i + 1][1]))
        kf.append((100, pts[-1][0], pts[-1][1]))
        end = hold if hold is not None else min(t1 + 0.6, 100)
        self.add(self.group(inner, self.move(kf), self.show(t0, end, 0.4), still=still))

    def chip(self, label, bg=None, fg=None, size=14, h=28):
        w = int(len(label) * size * 0.62 + 24)
        return (self.box(-w / 2, -h / 2, w, h, bg or self.CYAN, rx=h / 2)
                + self.text(0, h * 0.18 + 1, label, size, fg or self.WHITE, self.MONO, 600, "middle"))

    def pillc(self, cx, y, label, fg=None, bg=None, size=14, h=28):
        return self.pill(cx, y, label, fg, bg, size, h, "middle")

    # ---------- piezas
    def node(self, x, y, w, h, title, sub=None, dark=False, stroke=None, fill=None, tsize=20, ssize=15, anchor="middle"):
        fill = fill or (self.INK if dark else self.WHITE)
        stroke = stroke if stroke is not None else (None if dark else self.LINE)
        tc = self.WHITE if dark else self.INK
        sc = "#9FC3E3" if dark else self.GREY
        s = self.box(x, y, w, h, fill, stroke, rx=14)
        tx = x + w / 2 if anchor == "middle" else x + 20
        if sub:
            s += self.text(tx, y + h / 2 - 4, title, tsize, tc, self.HEAD, 600, anchor)
            s += self.text(tx, y + h / 2 + 20, sub, ssize, sc, self.MONO, 400, anchor)
        else:
            s += self.text(tx, y + h / 2 + 7, title, tsize, tc, self.HEAD, 600, anchor)
        return s

    def lane(self, x, ytop, ybot, title, sub=None, w=210):
        """Cabecera oscura y línea de vida punteada (diagrama de secuencia)."""
        h = 62 if sub else 50
        s = self.node(x - w / 2, ytop, w, h, title, sub, dark=True, tsize=19)
        s += f'<line x1="{x}" y1="{ytop + h}" x2="{x}" y2="{ybot}" stroke="{self.GREY}" stroke-width="1.5" stroke-dasharray="4 6"/>'
        return self.add(s)

    def msg(self, x1, x2, y, label, color, t0, t1, hold=100, dashed=False, tok=None, still=None, size=15):
        """Mensaje de un diagrama de secuencia: flecha + rótulo (+ ficha que viaja)."""
        self.arrow([(x1, y), (x2, y)], t0, t1, color, hold=hold, dashed=dashed, still=still)
        s = self.st(t0, hold) if still is None else still
        self.appear(self.text((x1 + x2) / 2, y - 10, label, size, color, self.MONO, 600, "middle"), t1 - 0.5, hold, still=s)
        if tok:
            self.token([(x1, y), (x2, y)], t0, t1, self.chip(tok, bg=color, size=13, h=24))

    def note(self, x, y, w, title, lines, kind="info", size=16, lh=22):
        col = {"info": self.BLUE, "ok": self.OK, "bad": self.BAD, "amb": self.AMB}[kind]
        bg = {"info": self.WHITE, "ok": self.OKBG, "bad": self.BADBG, "amb": self.AMBBG}[kind]
        h = 20 + (26 if title else 0) + lh * len(lines)
        s = self.box(x, y, w, h, bg, self.LINE if kind == "info" else None, rx=10)
        s += f'<rect x="{x}" y="{y}" width="5" height="{h}" rx="2" fill="{col}"/>'
        yy = y + 30
        if title:
            s += self.text(x + 20, yy, title, 17, self.INK if kind == "info" else col, self.SANS, 600)
            yy += 26
        for ln in lines:
            s += self.text(x + 20, yy, ln, size, self.TXT, self.SANS, 400)
            yy += lh
        return s

    def mark(self, cx, cy, ok=True, r=16):
        col = self.OK if ok else self.BAD
        bg = self.OKBG if ok else self.BADBG
        s = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{bg}" stroke="{col}" stroke-width="2.5"/>'
        if ok:
            s += (f'<path d="M{cx - r * .45:.1f} {cy:.1f} L{cx - r * .1:.1f} {cy + r * .38:.1f} L{cx + r * .5:.1f} {cy - r * .35:.1f}" '
                  f'fill="none" stroke="{col}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>')
        else:
            d = r * .38
            s += f'<path d="M{cx - d:.1f} {cy - d:.1f} L{cx + d:.1f} {cy + d:.1f} M{cx + d:.1f} {cy - d:.1f} L{cx - d:.1f} {cy + d:.1f}" stroke="{col}" stroke-width="3" stroke-linecap="round"/>'
        return s

    def bar(self, x, y, w, h, t0, t1, color, hold=100, still=None):
        """Barra horizontal que crece de izquierda a derecha entre t0 y t1 (línea de tiempo)."""
        s = self.st(t0, hold) if still is None else still
        sc = self.keyframes([(0, 0), (t0, 0), (t1, 1), (100, 1)], "transform", "scaleX({})")
        vis = self.show(t0, hold, 0.4)
        c = self._cls(f"transform-box:fill-box;transform-origin:left center;transform:scaleX(1);", sc)
        return self.add(self.group(f'<rect class="{c}" x="{x}" y="{y}" width="{w}" height="{h}" rx="{min(h / 2, 6)}" fill="{color}"/>', vis, still=s))

    # ---------- salida
    def finish(self, lid, n, title, desc, pcts):
        name = f"{lid}-t{n}.svg"
        out = SITE / name
        self.save(str(out), title, desc)
        prefix = PREV / f"_t{lid}-t{n}"
        for old in PREV.glob(f"_t{lid}-t{n}-*.png"):
            old.unlink()
        self._last = out
        self.preview(pcts, str(prefix))
        kb = out.stat().st_size / 1024
        print(f"{name}: {kb:.0f} KB")
        assert kb < 120, "pesa más de 120 KB"
        return out
