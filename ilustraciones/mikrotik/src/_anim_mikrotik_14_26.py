#!/usr/bin/env python3
"""Ayudantes para las animaciones de teoría de MikroTik, lecciones 14 a 26.

No modifica tools/anim.py: solo arma piezas repetidas (equipos, líneas de vida, mensajes
que viajan, paquetes con texto, barras que se vacían) encima de la clase Anim.
"""
import sys

sys.path.insert(0, "/home/claude/ies-training/tools")
from anim import Anim  # noqa: E402

SITE = "/home/claude/ies-training/site2/ilustraciones/mikrotik"
PREV = "/home/claude/ies-training/ilustraciones/mikrotik"
NAVY_TXT = "#9FC3E3"


def node(a, x, y, w, h, title, sub=None, dark=False, tsize=20, ssize=15, fill=None, stroke=None):
    """Equipo: caja con título y, opcional, una línea mono debajo."""
    f = fill or (a.INK if dark else a.WHITE)
    s = a.box(x, y, w, h, f, stroke or (None if dark else a.LINE), rx=16)
    tc = a.WHITE if dark else a.INK
    if sub:
        s += a.text(x + w / 2, y + h / 2 - 3, title, tsize, tc, a.HEAD, 600, "middle")
        s += a.text(x + w / 2, y + h / 2 + 21, sub, ssize, NAVY_TXT if dark else a.GREY, a.MONO, 400, "middle")
    else:
        s += a.text(x + w / 2, y + h / 2 + 7, title, tsize, tc, a.HEAD, 600, "middle")
    return s


def lifeline(a, x, y1, y2):
    return f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" stroke="{a.LINE}" stroke-width="2.5" stroke-dasharray="6 6"/>'


def msg(a, x1, x2, y, label, t, end=100, color=None, still=1, sub=None, travel=2.5, lsize=16,
        dot=True, dash="", subcolor=None, width=3):
    """Mensaje horizontal de x1 a x2 que sale en t% (un punto viaja) y queda dibujado hasta end%."""
    c = color or a.BLUE
    tip = x2 - 2 if x2 > x1 else x2 + 2
    arrow = a.arrow(f"M{x1} {y} H{tip}", c, width, dash)
    lab = a.text((x1 + x2) / 2, y - 11, label, lsize, c, a.MONO, 600, "middle")
    if sub:
        lab += a.text((x1 + x2) / 2, y + 25, sub, 15, subcolor or a.TXT, a.SANS, 400, "middle")
    a.add(a.group(arrow + lab, a.show(t + travel * 0.6, end), still=still))
    if dot:
        mv = a.move([(0, x1, y), (t, x1, y), (t + travel, x2, y), (100, x2, y)])
        a.add(a.group(f'<circle cx="0" cy="0" r="9" fill="{c}"/>', mv, a.show(t, t + travel + 0.4, 0.3), still=0))


def tag(a, x, y, label, fg, bg, size=15, h=28, anchor="start"):
    """Pastilla sin animación (para envolver con group)."""
    return a.pill(x, y, label, fg, bg, size, h, anchor)


def packet(a, label, pts, on, off, fill=None, fg=None, size=15, h=34, still=0, w=None):
    """Paquete con texto, centrado en (0,0), que se mueve por pts [(pct,x,y)] y se ve entre on y off."""
    fill = fill or a.CYAN
    fg = fg or a.WHITE
    w = w or int(len(label) * size * 0.62 + 30)
    inner = (f'<rect x="{-w / 2}" y="{-h / 2}" width="{w}" height="{h}" rx="{h / 2}" fill="{fill}"/>'
             + a.text(0, size * 0.36, label, size, fg, a.MONO, 600, "middle"))
    a.add(a.group(inner, a.move(pts), a.show(on, off, 0.4), still=still))


def bar(a, x, y, w, h, pts, color=None, still=1, bg=None):
    """Barra que se llena o vacía: pts [(pct, fracción 0..1)]."""
    color = color or a.BLUE
    a.add(a.box(x, y, w, h, bg or "#E6EDF4", rx=h / 2))
    k = a.keyframes([(p, v) for p, v in pts], "transform", "scaleX({})")
    a.add(a.group(a.box(x, y, w, h, color, rx=h / 2), k, still=still, origin=f"{x}px {y}px"))


def preview(T, svg_path, pcts, prefix):
    """Como Anim.preview, pero sin pausar por JS (Chromium a veces pinta un cuadro viejo):
    para cada instante escribe una copia temporal con el tiempo fijado en el CSS
    (animation-delay negativo y pausa) y la abre en una página nueva."""
    import tempfile, os
    from pathlib import Path
    from playwright.sync_api import sync_playwright
    src = Path(svg_path).read_text(encoding="utf-8")
    tmpd = Path(tempfile.mkdtemp(prefix="anim-prev-", dir="/tmp/claude-0"))
    outs = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        for pct in pcts:
            d = T * pct / 100
            rule = f"*{{animation-delay:-{d:.3f}s!important;animation-play-state:paused!important}}"
            f = tmpd / f"f{pct}.svg"
            f.write_text(src.replace("@media (prefers-reduced-motion", rule + "@media (prefers-reduced-motion", 1), encoding="utf-8")
            pg = b.new_page(viewport={"width": 1200, "height": 675})
            pg.goto("file://" + str(f)); pg.wait_for_timeout(120)
            o = f"{prefix}-{pct}.png"; pg.screenshot(path=o); outs.append(o); pg.close()
        ctx = b.new_context(viewport={"width": 1200, "height": 675}, reduced_motion="reduce")
        pg2 = ctx.new_page(); pg2.goto("file://" + str(svg_path)); pg2.wait_for_timeout(200)
        o = f"{prefix}-fijo.png"; pg2.screenshot(path=o); outs.append(o)
        b.close()
    for f in tmpd.iterdir():
        os.unlink(f)
    tmpd.rmdir()
    return outs


def out(a, lid, n, title, desc, pcts):
    path = a.save(f"{SITE}/{lid}-t{n}.svg", title, desc)
    preview(a.T, path, pcts, f"{PREV}/_t{lid}-{n}")
    return path
