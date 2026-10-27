#!/usr/bin/env python3
"""Ayudantes para las animaciones de teoría del curso Akuvox (lecciones 1 a 14).

Se apoyan en tools/anim.py sin modificarla: flechas que se dibujan solas (stroke-dashoffset con
pathLength=100), fichas que viajan por una polilínea, cajas de equipo y notas.
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, "/home/claude/ies-training/tools")
from anim import Anim  # noqa: E402

SITE = Path("/home/claude/ies-training/site2/ilustraciones/akuvox")
PREV = Path("/home/claude/ies-training/ilustraciones/akuvox")

A = Anim  # atajo para la paleta


def cls(a, base, *names):
    """Clase CSS con estilo base (cuadro fijo) y una o varias animaciones."""
    a.n += 1
    c = f"c{a.n}"
    anims = ",".join(f"{n} {a.T}s linear infinite" for n in names)
    a.css.append(f".{c}{{{base}animation:{anims}}}")
    return c


def appear(a, inner, t0, t1=100, still=1, fade=1.2):
    """inner visible entre t0 y t1 (porcentaje)."""
    return a.add(a.group(inner, a.show(t0, t1, fade), still=still))


def _seg_len(p, q):
    return math.hypot(q[0] - p[0], q[1] - p[1])


def _head(p, q, color, size=13):
    ang = math.atan2(q[1] - p[1], q[0] - p[0])
    x, y = q
    l, w = size, size * 0.55
    bx, by = x - l * math.cos(ang), y - l * math.sin(ang)
    px, py = -math.sin(ang) * w, math.cos(ang) * w
    return f'<path d="M{x:.1f} {y:.1f} L{bx + px:.1f} {by + py:.1f} L{bx - px:.1f} {by - py:.1f} z" fill="{color}"/>'


def draw_arrow(a, pts, t0, t1, color=None, width=3, hold=100, still=1, dashed=False, head=True, extra=""):
    """Flecha por la polilínea pts que se dibuja entre t0 y t1 y queda hasta hold.
    Con dashed=True no se 'dibuja': aparece con fundido (no se puede combinar trazo y punteado)."""
    color = color or A.BLUE
    d = "M" + " L".join(f"{x} {y}" for x, y in pts)
    # cortar el trazo antes de la punta para que no asome
    if head:
        p, q = pts[-2], pts[-1]
        L = _seg_len(p, q)
        k = max(0, (L - 8) / L) if L else 1
        qq = (p[0] + (q[0] - p[0]) * k, p[1] + (q[1] - p[1]) * k)
        d = "M" + " L".join(f"{x} {y}" for x, y in pts[:-1]) + f" L{qq[0]:.1f} {qq[1]:.1f}"
    vis = a.show(t0, hold, 0.8)
    if dashed:
        line = f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" stroke-dasharray="9 7" stroke-linecap="round" {extra}/>'
        a.add(a.group(line + (_head(pts[-2], pts[-1], color) if head else ""), vis, still=still))
        return
    dash = a.keyframes([(0, 100), (t0, 100), (t1, 0), (100, 0)], prop="stroke-dashoffset")
    c = cls(a, "stroke-dashoffset:0;", dash)
    line = f'<path class="{c}" d="{d}" pathLength="100" stroke-dasharray="100 100" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round" {extra}/>'
    a.add(a.group(line, vis, still=still))
    if head:
        a.add(a.group(_head(pts[-2], pts[-1], color), a.show(t1, hold, 0.5), still=still))


def token(a, pts, t0, t1, inner, still=0, hold=None):
    """Mueve inner (dibujado alrededor de 0,0) por la polilínea pts entre t0 y t1.
    Se ve desde t0 hasta hold (por defecto t1 + 0.6)."""
    total = sum(_seg_len(pts[i], pts[i + 1]) for i in range(len(pts) - 1)) or 1
    kf = [(0, pts[0][0], pts[0][1]), (t0, pts[0][0], pts[0][1])]
    acc = 0
    for i in range(len(pts) - 1):
        acc += _seg_len(pts[i], pts[i + 1])
        kf.append((t0 + (t1 - t0) * acc / total, pts[i + 1][0], pts[i + 1][1]))
    kf.append((100, pts[-1][0], pts[-1][1]))
    end = hold if hold is not None else min(t1 + 0.6, 100)
    a.add(a.group(inner, a.move(kf), a.show(t0, end, 0.4), still=still))


def chip(a, label, fg=None, bg=None, size=14, h=28):
    """Ficha centrada en 0,0 (para token)."""
    w = int(len(label) * size * 0.62 + 24)
    return (a.box(-w / 2, -h / 2, w, h, bg or A.CYAN, rx=h / 2)
            + a.text(0, h * 0.18 + 1, label, size, fg or A.WHITE, A.MONO, 600, "middle"))


def node(a, x, y, w, h, title, sub=None, dark=False, stroke=None, fill=None, tsize=20, ssize=15, anchor="start"):
    fill = fill or (A.INK if dark else A.WHITE)
    stroke = stroke if stroke is not None else (None if dark else A.LINE)
    tc = A.WHITE if dark else A.INK
    sc = "#9FC3E3" if dark else A.GREY
    s = a.box(x, y, w, h, fill, stroke, rx=14)
    if anchor == "middle":
        tx = x + w / 2
    else:
        tx = x + 20
    if sub:
        s += a.text(tx, y + h / 2 - 4, title, tsize, tc, A.HEAD, 600, anchor)
        s += a.text(tx, y + h / 2 + 20, sub, ssize, sc, A.MONO, 400, anchor)
    else:
        s += a.text(tx, y + h / 2 + 7, title, tsize, tc, A.HEAD, 600, anchor)
    return s


def lane(a, x, ytop, ybot, title, sub=None, w=210):
    """Cabecera oscura y línea de vida punteada (diagrama de secuencia)."""
    s = node(a, x - w / 2, ytop, w, 62 if sub else 50, title, sub, dark=True, anchor="middle", tsize=19)
    y0 = ytop + (62 if sub else 50)
    s += f'<line x1="{x}" y1="{y0}" x2="{x}" y2="{ybot}" stroke="{A.GREY}" stroke-width="1.5" stroke-dasharray="4 6"/>'
    return a.add(s)


def note(a, x, y, w, title, lines, kind="info", size=16, lh=22):
    col = {"info": A.BLUE, "ok": A.OK, "bad": A.BAD, "amb": A.AMB}[kind]
    bg = {"info": A.WHITE, "ok": A.OKBG, "bad": A.BADBG, "amb": A.AMBBG}[kind]
    h = 22 + (26 if title else 0) + lh * len(lines)
    s = a.box(x, y, w, h, bg, A.LINE if kind == "info" else None, rx=10)
    s += f'<rect x="{x}" y="{y}" width="5" height="{h}" rx="2" fill="{col}"/>'
    yy = y + 30
    if title:
        s += a.text(x + 20, yy, title, 17, A.INK, A.SANS, 600)
        yy += 26
    for ln in lines:
        s += a.text(x + 20, yy, ln, size, A.TXT, A.SANS, 400)
        yy += lh
    return s, h


def mark(a, cx, cy, ok=True, r=16):
    col = A.OK if ok else A.BAD
    bg = A.OKBG if ok else A.BADBG
    s = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{bg}" stroke="{col}" stroke-width="2.5"/>'
    if ok:
        s += f'<path d="M{cx - r * .45} {cy} L{cx - r * .1} {cy + r * .38} L{cx + r * .5} {cy - r * .35}" fill="none" stroke="{col}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>'
    else:
        d = r * .38
        s += f'<path d="M{cx - d} {cy - d} L{cx + d} {cy + d} M{cx + d} {cy - d} L{cx - d} {cy + d}" stroke="{col}" stroke-width="3" stroke-linecap="round"/>'
    return s


def pillc(a, cx, y, label, fg=None, bg=None, size=14, h=28):
    """Píldora centrada en cx."""
    return a.pill(cx, y, label, fg, bg, size, h, "middle")


def lock(a, x, y, open_=False, color=None, s=1.0):
    """Candado simple (x,y = esquina sup. izq. del cuerpo)."""
    c = color or A.INK
    w, h = 30 * s, 24 * s
    sh = (f'<path d="M{x + 7 * s} {y} V{y - 9 * s} a{8 * s} {8 * s} 0 0 1 {16 * s} 0 V{y - 3 * s if open_ else y}" '
          f'fill="none" stroke="{c}" stroke-width="{3 * s}" stroke-linecap="round" '
          + (f'transform="translate({10 * s} {-4 * s})"' if open_ else "") + "/>")
    return sh + f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{4 * s}" fill="{c}"/>'


def preview(svg_path, T, pcts, prefix):
    """Como Anim.preview, pero busca el instante con animation-delay negativo y pausa por CSS.
    (Con WAAPI pausado, Chromium a veces deja pintadas fichas con opacidad 0 en la captura.)"""
    from playwright.sync_api import sync_playwright
    outs = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1200, "height": 675})
        src = Path(svg_path).read_text(encoding="utf-8")
        tmp = Path("/tmp/claude-0/-home-claude/e7efb7ec-f4b7-5f80-a457-304e3488cc08/scratchpad/_pv.svg")
        for pct in pcts:
            # copia nueva por instante: carga limpia, sin restos de pintura del cuadro anterior
            rule = "*{animation-play-state:paused!important;animation-delay:-%ss!important}" % (T * pct / 100)
            tmp.write_text(src.replace("</style>", rule + "</style>", 1), encoding="utf-8")
            pg.goto("file://" + str(tmp)); pg.wait_for_timeout(150)
            o = f"{prefix}-{pct}.png"; pg.screenshot(path=o); outs.append(o)
        ctx = b.new_context(viewport={"width": 1200, "height": 675}, reduced_motion="reduce")
        pg2 = ctx.new_page(); pg2.goto("file://" + str(svg_path)); pg2.wait_for_timeout(200)
        o = f"{prefix}-fijo.png"; pg2.screenshot(path=o); outs.append(o)
        b.close()
    return outs


def finish(a, name, title, desc, pcts):
    out = SITE / name
    a.save(str(out), title, desc)
    prefix = str(PREV / ("_t" + name.replace(".svg", "")))
    for old in PREV.glob(f"_t{name.replace('.svg', '')}-*.png"):
        old.unlink()
    preview(out, a.T, pcts, prefix)
    kb = out.stat().st_size / 1024
    print(f"{name}: {kb:.0f} KB")
    assert kb < 120, "pesa más de 120 KB"
    return out
