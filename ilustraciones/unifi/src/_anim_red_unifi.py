#!/usr/bin/env python3
"""Ayudantes para las animaciones "Cómo se ve en la red" (Resumen) y de Laboratorio del curso UniFi (lecciones 1 a 12).

Se apoyan en tools/anim.py (no la modifican) y en las piezas de las animaciones de teoría del curso (_anim_unifi:
token, chip, ap_icon, phone_icon, arcs, check, xmark…). Suman equipos con icono (los glifos de ilus.py), mensajes
de diagrama de secuencia, terminal, recuadros de nota de varias líneas y la salida a site2 con revisión por
tools/anim_preview.py (PNG en ilustraciones/unifi/_rev-<id>-<r1|l1|l2>-<pct>.png).
Tiempos en porcentaje del ciclo. `still` es la opacidad en el cuadro fijo (movimiento reducido).
"""
import math
import subprocess
import sys

sys.path.insert(0, "/home/claude/ies-training/tools")
sys.path.insert(0, "/home/claude/ies-training/ilustraciones/unifi/src")
from anim import Anim  # noqa: E402,F401
from ilus import ICON  # noqa: E402
from _anim_unifi import (A, SUB_DARK, chip, token, xmark, check, arcs, ap_icon, phone_icon)  # noqa: E402,F401

SITE = "/home/claude/ies-training/site2/ilustraciones/unifi"
TOOLS = "/home/claude/ies-training/tools"
SKY = SUB_DARK      # texto secundario sobre fondo oscuro
GOLD = "#FFD28A"    # atención sobre fondo oscuro
MINT = "#5BE0A5"    # correcto sobre fondo oscuro


def new(T, tema, title, caps, still, paso=None):
    """Lienzo con kicker, título y leyenda numerada. paso=None → Resumen; paso=N → Laboratorio, paso N."""
    tail = "CÓMO SE VE EN LA RED" if paso is None else f"LABORATORIO · PASO {paso}"
    a = Anim(T=T, kicker=f"UNIFI · {tema.upper()} · {tail}", title=title)
    a.spans = a.steps(caps, still=still)
    a.still_i = still
    return a


def ph(a, i, j=None):
    j = i if j is None else j
    return a.spans[i][0], a.spans[j][1]


def during(a, inner, t0, t1=100, still=0, fade=0.8):
    """Visible entre t0 y t1 (%)."""
    return a.add(a.group(inner, a.show(t0, t1, fade), still=still))


def vis(a, inner, i, j=None, still=None, fade=0.8):
    """Visible durante los tiempos i..j (desde 0). En el cuadro fijo, visible si el tiempo fijo cae en i..j."""
    j = i if j is None else j
    s0, s1 = ph(a, i, j)
    st = still if still is not None else (1 if i <= a.still_i <= j else 0)
    return a.add(a.group(inner, a.show(s0, s1, fade), still=st))


def still_only(a, inner):
    return a.add(a.group(inner, a.keyframes([(0, 0), (100, 0)]), still=1))


def glyph(a, name, x, y, color=None, scale=1.35, sw=1.8):
    """Icono de ilus.py (24x24) con la esquina superior izquierda en (x, y)."""
    return (f'<g transform="translate({x} {y}) scale({scale})" fill="none" stroke="{color or a.BLUE}" '
            f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">{ICON[name]}</g>')


def dev(a, x, y, w, h, title, sub="", icon=None, dark=False, sub2="", tsize=19, ssize=15, stroke=None, sw=2, ap=False):
    """Equipo: caja con icono a la izquierda (ap=True dibuja el AP redondo del curso), título y una o dos líneas mono."""
    fill = a.INK if dark else a.WHITE
    st = stroke or (None if dark else a.LINE)
    s = a.box(x, y, w, h, fill, st, rx=14, sw=sw)
    tx = x + (62 if (icon or ap) else 18)
    if ap:
        s += ap_icon(a, x + 34, y + 34, 18)
    elif icon:
        s += glyph(a, icon, x + 18, y + 18, a.CYAN if dark else a.BLUE)
    s += a.text(tx, y + 34, title, tsize, a.WHITE if dark else a.INK, a.SANS, 600)
    if sub:
        s += a.text(tx, y + 58, sub, ssize, SKY if dark else a.GREY, a.MONO)
    if sub2:
        s += a.text(tx, y + 80, sub2, ssize, SKY if dark else a.GREY, a.MONO)
    return s


def wire(x1, y1, x2, y2, color=None, w=3, dash=""):
    da = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color or A.LINE}" stroke-width="{w}"{da} stroke-linecap="round"/>'


def poly(pts, color=None, w=3, dash=""):
    d = "M" + " L".join(f"{x} {y}" for x, y in pts)
    da = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<path d="{d}" fill="none" stroke="{color or A.LINE}" stroke-width="{w}"{da} stroke-linecap="round" stroke-linejoin="round"/>'


def lifeline(a, x, y1, y2):
    return a.add(f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" stroke="{a.LINE}" stroke-width="2.5" stroke-dasharray="6 6"/>')


def msg(a, x1, x2, y, label, t, end=100, color=None, still=1, sub=None, dur=2.5, lsize=16, dash="", subcolor=None):
    """Mensaje horizontal de x1 a x2: un punto viaja desde t% y la flecha queda dibujada hasta end%."""
    c = color or a.BLUE
    tip = x2 - 2 if x2 > x1 else x2 + 2
    body = a.arrow(f"M{x1} {y} H{tip}", c, 3, dash)
    body += a.text((x1 + x2) / 2, y - 11, label, lsize, c, a.MONO, 600, "middle")
    if sub:
        body += a.text((x1 + x2) / 2, y + 24, sub, 15, subcolor or a.TXT, a.SANS, 400, "middle")
    a.add(a.group(body, a.show(t + dur * 0.6, end), still=still))
    mv = a.move([(0, x1, y), (t, x1, y), (t + dur, x2, y), (100, x2, y)])
    a.add(a.group(f'<circle cx="0" cy="0" r="9" fill="{c}"/>', mv, a.show(t, t + dur + 0.4, 0.3), still=0))


def status(a, y, items, x=600, anchor="middle", size=17):
    """Frases que se alternan en una línea: items = [(t0, t1, texto, color, still)]."""
    for t0, t1, txt, col, st in items:
        a.add(a.group(a.text(x, y, txt, size, col, a.SANS, 600, anchor), a.show(t0, t1, 0.8), still=st))


def pill(a, x, y, label, kind="info", size=15, h=28, anchor="start"):
    fg, bg = {"info": (a.BLUE, "#E4EFFA"), "ok": (a.OK, a.OKBG), "bad": (a.BAD, a.BADBG), "amb": (a.AMB, a.AMBBG),
              "grey": (a.GREY, "#E6EDF4"), "dark": (a.WHITE, a.NAVY2)}[kind]
    return a.pill(x, y, label, fg, bg, size, h, anchor)


def pill_at(a, x, y, label, kind, t0, t1=100, still=0, size=15, h=28, anchor="start"):
    during(a, pill(a, x, y, label, kind, size, h, anchor), t0, t1, still)


def nbox(a, x, y, w, h, title, lines, kind="info", tsize=17, lsize=15, lh=22):
    """Recuadro con barra de color a la izquierda, título y líneas."""
    col, bg = {"ok": (a.OK, a.OKBG), "bad": (a.BAD, a.BADBG), "amb": (a.AMB, a.AMBBG), "info": (a.BLUE, a.WHITE)}[kind]
    s = a.box(x, y, w, h, bg, a.LINE if kind == "info" else None, rx=10, sw=1.5)
    s += f'<rect x="{x}" y="{y}" width="5" height="{h}" rx="2" fill="{col}"/>'
    yy = y + 28
    if title:
        s += a.text(x + 20, yy, title, tsize, col if kind != "info" else a.INK, a.SANS, 600)
        yy += 25
    for ln in lines:
        s += a.text(x + 20, yy, ln, lsize, a.INK if kind != "info" else a.TXT, a.SANS)
        yy += lh
    return s


def term(a, x, y, w, lines, title="", size=15, lh=24, colors=None, h=None):
    """Terminal oscura con líneas mono. colors = {índice: color}."""
    hh = h or (24 + (26 if title else 0) + lh * len(lines))
    s = a.box(x, y, w, hh, a.INK, rx=12)
    yy = y + 32
    if title:
        s += a.text(x + 18, yy, title, 15, SKY, a.MONO, 400)
        yy += 28
    for i, ln in enumerate(lines):
        c = (colors or {}).get(i, a.WHITE)
        s += a.text(x + 18, yy, ln, size, c, a.MONO)
        yy += lh
    return s


def dot(a, color, r=9):
    return f'<circle cx="0" cy="0" r="{r}" fill="{color}" stroke="{a.WHITE}" stroke-width="2"/>'


def tag(a, label, bg, fg=None, size=15, h=28):
    """Ficha centrada en 0,0 (para token)."""
    return chip(a, label, fg or a.WHITE, bg, size, h)


def go(a, pts, t0, t1, label=None, bg=None, inner=None, still=0, hold=None, size=15):
    """Ficha que viaja por pts entre t0 y t1; en el cuadro fijo queda en el último punto si still=1."""
    token(a, pts, t0, t1, label=label, inner=inner, bg=bg, still=still, hold=hold, size=size)


def write(a, lid, kind, title, desc, pcts):
    """Guarda site2/ilustraciones/unifi/<lid>-<kind>.svg y deja la revisión _rev-<lid>-<kind>-<pct>.png."""
    path = a.save(f"{SITE}/{lid}-{kind}.svg", title, desc)
    subprocess.run([sys.executable, f"{TOOLS}/anim_preview.py", str(path), "--pct", ",".join(str(p) for p in pcts)], check=True)
    return path


def mid(a, f=0.7):
    """Un instante al f de cada tiempo, para la revisión."""
    return [round(s0 + (s1 - s0) * f, 1) for s0, s1 in a.spans]
