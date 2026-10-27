"""Ayudantes para las animaciones de teoría de MikroTik 27 a 39 (sobre tools/anim.py, sin tocarlo)."""
import sys
sys.path.insert(0, "/home/claude/ies-training/tools")
from anim import Anim  # noqa: E402

SITE = "/home/claude/ies-training/site2/ilustraciones/mikrotik"
PREV = "/home/claude/ies-training/ilustraciones/mikrotik"
LIGHT = "#9FC3E3"   # texto secundario sobre fondo oscuro
GOLD = "#FFD28A"    # resaltado sobre fondo oscuro
MINT = "#5BE0A5"    # ok sobre fondo oscuro


def vis(a, wins, fade=0.8):
    """Opacidad 1 dentro de cada ventana (inicio, fin) del ciclo, 0 fuera."""
    pts = [(0, 0)]
    end_on = False
    for s, e in wins:
        if s <= 0:
            pts += [(0, 1)]
        else:
            pts += [(s, 0), (s + fade, 1)]
        if e >= 100:
            pts += [(100, 1)]
            end_on = True
        else:
            pts += [(e - fade, 1), (e, 0)]
    if not end_on:
        pts.append((100, 0))
    return a.keyframes(pts)


def en(a, inner, t0, t1=100, still=0):
    """Agrega inner visible entre t0 y t1."""
    return a.add(a.group(inner, vis(a, [(t0, t1)]), still=still))


def ventanas(a, inner, wins, still=0):
    return a.add(a.group(inner, vis(a, wins), still=still))


def fijo(a, inner):
    """Solo en el cuadro fijo (movimiento reducido)."""
    return a.add(a.group(inner, a.keyframes([(0, 0), (100, 0)]), still=1))


def pill_c(a, label, fg, bg, size=15, h=30, stroke=None):
    """Píldora centrada en (0,0), para mover con transform."""
    w = int(len(label) * size * 0.62 + 28)
    st = f' stroke="{stroke}" stroke-width="2"' if stroke else ""
    return (f'<rect x="{-w / 2}" y="{-h / 2}" width="{w}" height="{h}" rx="{h / 2}" fill="{bg}"{st}/>'
            + a.text(0, size * 0.36, label, size, fg, a.MONO, 600, "middle"))


def paquete(a, label, pts, t0, t1, fg="#FFFFFF", bg=None, size=15, still=0, stroke=None):
    """Píldora que viaja por pts [(pct, x, y)] y se ve entre t0 y t1."""
    bg = bg or a.CYAN
    full = [(0, pts[0][1], pts[0][2])] + [p for p in pts if p[0] > 0] + [(100, pts[-1][1], pts[-1][2])]
    return a.add(a.group(pill_c(a, label, fg, bg, size, stroke=stroke), a.move(full), vis(a, [(t0, t1)], 0.6), still=still))


def pill_at(a, x, y, label, fg, bg, size=15, h=30, anchor="start"):
    return a.pill(x, y, label, fg, bg, size, h, anchor)


def nodo(a, x, y, w, h, titulo, sub="", dark=True, sub2="", size=20):
    fill = a.INK if dark else a.WHITE
    s = a.box(x, y, w, h, fill, None if dark else a.LINE, rx=16)
    s += a.text(x + 20, y + 33, titulo, size, a.WHITE if dark else a.INK, a.HEAD, 600)
    if sub:
        s += a.text(x + 20, y + 58, sub, 15, LIGHT if dark else a.GREY, a.MONO)
    if sub2:
        s += a.text(x + 20, y + 80, sub2, 15, LIGHT if dark else a.GREY, a.MONO)
    return a.add(s)


def marca(a, cx, cy, ok=True, r=16):
    c = a.OK if ok else a.BAD
    if ok:
        p = f'M{cx - 7} {cy} L{cx - 2} {cy + 6} L{cx + 8} {cy - 6}'
    else:
        p = f'M{cx - 6} {cy - 6} L{cx + 6} {cy + 6} M{cx + 6} {cy - 6} L{cx - 6} {cy + 6}'
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#FFFFFF" stroke="{c}" stroke-width="2.5"/>'
            f'<path d="{p}" fill="none" stroke="{c}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>')


def narr(a, items, x=48, y=630, size=17, still_idx=None):
    """items: [(t0, t1, texto, color)]. Una línea de narración abajo."""
    for i, (t0, t1, s, c) in enumerate(items):
        en(a, a.text(x, y, s, size, c, a.SANS, 600), t0, t1, still=1 if i == still_idx else 0)


def path_arrow(a, d, color, width=3, dash=""):
    return a.arrow(d, color, width, dash)


def escribir(a, path, title, desc, pcts, prefix, wait=450):
    """save + vista previa con espera larga (la de anim.py a veces deja fantasmas de opacidad en la captura)."""
    from pathlib import Path
    from playwright.sync_api import sync_playwright
    p = a.save(path, title, desc)
    outs = []
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={"width": 1200, "height": 675})
        pg.goto("file://" + str(p)); pg.wait_for_timeout(300)
        # en tiempo real: pausar y saltar deja capas fantasma en Chromium sin ventana
        pg.goto("file://" + str(p))
        for pct in sorted(pcts):
            ms = a.T * 1000 * pct / 100
            pg.wait_for_function(f"document.getAnimations().length && document.getAnimations()[0].currentTime >= {ms}", timeout=a.T * 1000 + 15000, polling=16)
            o = f"{prefix}-{pct}.png"; pg.screenshot(path=o); outs.append(o)
        ctx = b.new_context(viewport={"width": 1200, "height": 675}, reduced_motion="reduce")
        pg2 = ctx.new_page(); pg2.goto("file://" + str(p)); pg2.wait_for_timeout(300)
        o = f"{prefix}-fijo.png"; pg2.screenshot(path=o); outs.append(o)
        b.close()
    print("ok", Path(p).name, Path(p).stat().st_size // 1024, "KB ·", len(outs), "cuadros")
    return p
