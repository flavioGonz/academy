#!/usr/bin/env python3
"""Ayudantes para las animaciones de teoría del curso UniFi (lecciones 1 a 12).

Se apoyan en tools/anim.py sin modificarla. Cada animación: N tiempos iguales con leyenda numerada,
cajas fijas, fichas que viajan por una polilínea y cosas que aparecen en ciertos tiempos.
El cuadro fijo (movimiento reducido) muestra el tiempo `still`.
La descripción (desc) sale del alt de teoria_figs en manifest-teoria-1-12.json.
"""
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, "/home/claude/ies-training/tools")
from anim import Anim  # noqa: E402

SITE = Path("/home/claude/ies-training/site2/ilustraciones/unifi")
PREV = Path("/home/claude/ies-training/ilustraciones/unifi")
MAN = PREV / "manifest-teoria-1-12.json"
A = Anim
SUB_DARK = "#9FC3E3"


def new(T, tema, title, caps, still):
    a = Anim(T=T, kicker=f"UNIFI · {tema.upper()}", title=title)
    a.spans = a.steps(caps, still=still)
    a.still_i = still
    return a


def ph(a, i, j=None):
    j = i if j is None else j
    return a.spans[i][0], a.spans[j][1]


def vis(a, inner, i, j=None, still=None, fade=1.0):
    """Visible durante los tiempos i..j (índices desde 0). Fijo: visible si el tiempo fijo cae en i..j."""
    j = i if j is None else j
    s0, s1 = ph(a, i, j)
    st = still if still is not None else (1 if i <= a.still_i <= j else 0)
    return a.add(a.group(inner, a.show(s0, s1, fade), still=st))


def at(a, inner, t0, t1=100, still=0, fade=0.8):
    """Visible entre t0 y t1 (porcentajes)."""
    return a.add(a.group(inner, a.show(t0, t1, fade), still=still))


def _len(p, q):
    return math.hypot(q[0] - p[0], q[1] - p[1])


def chip(a, label, fg=None, bg=None, size=14, h=28):
    """Ficha centrada en 0,0."""
    w = int(len(label) * size * 0.62 + 24)
    return (a.box(-w / 2, -h / 2, w, h, bg or A.CYAN, rx=h / 2)
            + a.text(0, h * 0.18 + 1, label, size, fg or A.WHITE, A.MONO, 600, "middle"))


def token(a, pts, t0, t1, label=None, inner=None, fg=None, bg=None, still=0, hold=None, size=14):
    """Ficha que viaja por la polilínea pts entre t0 y t1 (%), visible hasta hold."""
    inner = inner if inner is not None else chip(a, label, fg, bg, size)
    total = sum(_len(pts[i], pts[i + 1]) for i in range(len(pts) - 1)) or 1
    kf = [(0, pts[0][0], pts[0][1]), (t0, pts[0][0], pts[0][1])]
    acc = 0
    for i in range(len(pts) - 1):
        acc += _len(pts[i], pts[i + 1])
        kf.append((t0 + (t1 - t0) * acc / total, pts[i + 1][0], pts[i + 1][1]))
    kf.append((100, pts[-1][0], pts[-1][1]))
    end = hold if hold is not None else min(t1 + 0.8, 100)
    if still:  # en el cuadro fijo, la ficha queda en el último punto
        kf[0] = (0, pts[-1][0], pts[-1][1])
        kf.insert(1, (max(t0 - 0.01, 0.01), pts[0][0], pts[0][1]))
    a.add(a.group(inner, a.move(kf), a.show(t0, end, 0.4), still=still))


def node(a, x, y, w, h, title, sub=None, dark=False, stroke=None, fill=None, tsize=20, ssize=15, sub2=None):
    fill = fill or (A.INK if dark else A.WHITE)
    stroke = stroke if stroke is not None else (None if dark else A.LINE)
    tc = A.WHITE if dark else A.INK
    sc = SUB_DARK if dark else A.GREY
    s = a.box(x, y, w, h, fill, stroke, rx=14)
    if sub and sub2:
        s += a.text(x + 20, y + h / 2 - 16, title, tsize, tc, A.HEAD, 600)
        s += a.text(x + 20, y + h / 2 + 8, sub, ssize, sc, A.MONO)
        s += a.text(x + 20, y + h / 2 + 30, sub2, ssize, sc, A.MONO)
    elif sub:
        s += a.text(x + 20, y + h / 2 - 4, title, tsize, tc, A.HEAD, 600)
        s += a.text(x + 20, y + h / 2 + 20, sub, ssize, sc, A.MONO)
    else:
        s += a.text(x + 20, y + h / 2 + 7, title, tsize, tc, A.HEAD, 600)
    return s


def line(a, pts, color=None, width=2.5, dash="", arrow=False):
    d = "M" + " L".join(f"{x} {y}" for x, y in pts)
    if arrow:
        return a.arrow(d, color, width, dash)
    da = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<path d="{d}" fill="none" stroke="{color or A.LINE}" stroke-width="{width}"{da} stroke-linecap="round"/>'


def xmark(a, x, y, r=15, color=None):
    c = color or A.BAD
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="{A.WHITE}" stroke="{c}" stroke-width="2.5"/>'
            f'<path d="M{x - r * .45} {y - r * .45} L{x + r * .45} {y + r * .45} M{x + r * .45} {y - r * .45} L{x - r * .45} {y + r * .45}" stroke="{c}" stroke-width="3" stroke-linecap="round"/>')


def check(a, x, y, r=15, color=None):
    c = color or A.OK
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="{A.WHITE}" stroke="{c}" stroke-width="2.5"/>'
            f'<path d="M{x - r * .45} {y + r * .02} L{x - r * .1} {y + r * .38} L{x + r * .5} {y - r * .35}" fill="none" stroke="{c}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>')


def pill(a, x, y, label, kind="info", size=14, h=28, anchor="start"):
    fg, bg = {"info": (A.BLUE, "#E4EFFA"), "ok": (A.OK, A.OKBG), "bad": (A.BAD, A.BADBG),
              "amb": (A.AMB, A.AMBBG), "grey": (A.GREY, "#E6EDF4"), "dark": (A.WHITE, A.NAVY2)}[kind]
    return a.pill(x, y, label, fg, bg, size, h, anchor)


def note(a, x, y, w, text, kind="info", size=16, h=46):
    col = {"info": A.BLUE, "ok": A.OK, "bad": A.BAD, "amb": A.AMB}[kind]
    bg = {"info": A.WHITE, "ok": A.OKBG, "bad": A.BADBG, "amb": A.AMBBG}[kind]
    return (a.box(x, y, w, h, bg, A.LINE, rx=10, sw=1.5) + f'<rect x="{x}" y="{y}" width="5" height="{h}" rx="2" fill="{col}"/>'
            + a.text(x + 20, y + h / 2 + size * 0.35, text, size, A.INK, A.SANS, 600))


def arcs(a, cx, cy, radii, color, facing=0, spread=38, width=3):
    """Arcos de onda centrados en (cx,cy) mirando a 'facing' grados (0 = derecha)."""
    out = []
    for r in radii:
        a1, a2 = math.radians(facing - spread), math.radians(facing + spread)
        x1, y1 = cx + r * math.cos(a1), cy + r * math.sin(a1)
        x2, y2 = cx + r * math.cos(a2), cy + r * math.sin(a2)
        out.append(f'<path d="M{x1:.1f} {y1:.1f} A{r} {r} 0 0 1 {x2:.1f} {y2:.1f}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round"/>')
    return out


def ap_icon(a, cx, cy, r=24):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{A.WHITE}" stroke="{A.LINE}" stroke-width="2.5"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r * .55}" fill="none" stroke="{A.CYAN}" stroke-width="2.5"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r * .18}" fill="{A.CYAN}"/>')


def phone_icon(a, cx, cy, color=None):
    c = color or A.INK
    return (f'<rect x="{cx - 12}" y="{cy - 20}" width="24" height="40" rx="5" fill="{A.WHITE}" stroke="{c}" stroke-width="2.5"/>'
            f'<line x1="{cx - 4}" y1="{cy + 13}" x2="{cx + 4}" y2="{cy + 13}" stroke="{c}" stroke-width="2.5" stroke-linecap="round"/>')


def desc(fname):
    m = json.load(open(MAN, encoding="utf-8"))
    for v in m.values():
        for tf in v.get("teoria_figs", []):
            if tf["file"] == fname:
                return tf["alt"]
    raise SystemExit(f"sin alt para {fname} en {MAN.name}")


def write(a, fname, title, pcts):
    stem = fname.rsplit(".", 1)[0]
    return a.write(str(SITE / fname), title, desc(fname), preview=pcts, prefix=str(PREV / f"_t{stem}"))


def mid_pcts(a):
    """Un instante al 70 % de cada tiempo."""
    return [round(s0 + (s1 - s0) * 0.7, 1) for s0, s1 in a.spans]
