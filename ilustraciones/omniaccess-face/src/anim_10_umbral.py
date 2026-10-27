"""Teoría de Diagnóstico facial: la mejor similitud contra el umbral; FMR y FNMR según dónde se pone; mejores imágenes separan las curvas."""
import math
from _anim_face import *

caps = ["Cada pasada se compara con cada plantilla; manda la mejor contra el umbral.",
        "Umbral bajo: casi no hay rechazos legítimos, pero pasan más ajenos (FMR).",
        "Umbral alto: casi ningún ajeno pasa, pero suben los rechazos legítimos (FNMR).",
        "Mejor luz y mejor foto separan las curvas: bajan los dos errores."]
a = new(24, "Umbral", "El umbral reparte el error; la imagen lo achica", caps, still=2, size=17)
S = [sp[0] for sp in a.spans]

CX, CY, CW, CH = 48, 176, 720, 360
a.add(a.box(CX, CY, CW, CH, a.WHITE, a.LINE))
gx0, gx1, base, top = CX + 30, CX + CW - 30, CY + CH - 56, CY + 40
sx = lambda v: gx0 + v / 100 * (gx1 - gx0)
a.add(f'<line x1="{gx0}" y1="{base}" x2="{gx1}" y2="{base}" stroke="{a.GREY}" stroke-width="2"/>')
for v in (0, 25, 50, 75, 100):
    a.add(a.text(sx(v), base + 24, str(v), 14, a.GREY, a.MONO, 600, "middle"))
a.add(a.text((gx0 + gx1) / 2, base + 46, "similitud con la plantilla", 15, a.GREY, a.MONO, 600, "middle"))


def curve(mu, sd, h=230):
    pts = []
    for i in range(0, 101):
        v = i
        y = base - h * math.exp(-((v - mu) ** 2) / (2 * sd * sd))
        pts.append((sx(v), y))
    return pts


def poly(pts, color, w=3.5):
    return f'<polyline points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="none" stroke="{color}" stroke-width="{w}"/>'


def area(pts, thr, side, color):
    sel = [(x, y) for x, y in pts if (x >= sx(thr) if side == "right" else x <= sx(thr))]
    if not sel:
        return ""
    p = [(sel[0][0], base)] + sel + [(sel[-1][0], base)]
    return f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in p)}" fill="{color}" opacity=".45"/>'


def thr_line(t, label=True):
    s = f'<line x1="{sx(t)}" y1="{top - 10}" x2="{sx(t)}" y2="{base}" stroke="{a.INK}" stroke-width="3" stroke-dasharray="8 5"/>'
    if label:
        s += a.pill(sx(t), top - 26, "umbral", a.WHITE, a.INK, size=13, anchor="middle")
    return s


imp, gen = curve(32, 9), curve(70, 9)
imp2, gen2 = curve(24, 7), curve(80, 7)
legend = (a.text(sx(14), top + 30, "personas ajenas", 15, a.BAD, a.SANS, 600, "middle")
          + a.text(sx(86), top + 30, "la persona correcta", 15, a.BLUE, a.SANS, 600, "middle"))
# 1 · una pasada
vis(a, thr_line(55) + f'<circle cx="{sx(86)}" cy="{base}" r="11" fill="{a.OK}"/>' + a.text(sx(86), base - 22, "esta pasada: 86", 15, a.OK, a.SANS, 600, "middle")
    + a.text(sx(30), top + 90, "Cada pasada es un punto en este eje:", 16, a.TXT, a.SANS, 400, "middle")
    + a.text(sx(30), top + 114, "la mejor similitud de la memoria.", 16, a.TXT, a.SANS, 400, "middle"), 0)
for st, t in ((1, 44), (2, 62)):
    vis(a, area(imp, t, "right", "#F2A493") + area(gen, t, "left", "#F5C77A") + poly(imp, a.BAD) + poly(gen, a.BLUE) + thr_line(t) + legend, st)
vis(a, area(imp2, 52, "right", "#F2A493") + area(gen2, 52, "left", "#F5C77A") + poly(imp2, a.BAD) + poly(gen2, a.BLUE) + thr_line(52) + legend, 3)

# panel derecho
RX, RW = 792, 360
a.add(a.box(RX, CY, RW, CH, a.WHITE, a.LINE))
temps = [("Bruno Ejemplo", 31), ("Ana Ejemplo", 86), ("Carla Ejemplo", 24), ("Dario Ejemplo", 40)]
inner = a.text(RX + 20, CY + 34, "Contra cada plantilla", 18, a.INK, a.SANS, 600)
for k, (n, v) in enumerate(temps):
    y = CY + 70 + k * 52
    best = v == 86
    inner += a.text(RX + 20, y + 4, n, 15, a.INK if best else a.TXT, a.SANS, 600 if best else 400)
    inner += a.box(RX + 20, y + 14, 260, 14, a.SLATE, rx=7) + a.box(RX + 20, y + 14, 260 * v / 100, 14, a.OK if best else "#A9BED2", rx=7)
    inner += a.text(RX + 292, y + 27, str(v), 15, a.OK if best else a.GREY, a.MONO, 600)
inner += f'<line x1="{RX + 20 + 260 * .55}" y1="{CY + 70}" x2="{RX + 20 + 260 * .55}" y2="{CY + 70 + 4 * 52}" stroke="{a.INK}" stroke-width="2.5" stroke-dasharray="6 4"/>'
inner += a.text(RX + 20, CY + 312, "La mejor, 86, supera el umbral:", 16, a.OK, a.SANS, 600) + a.text(RX + 20, CY + 336, "identifica y abre.", 16, a.OK, a.SANS, 600)
vis(a, inner, 0)


def stats(fmr, fnmr, note):
    s = a.text(RX + 20, CY + 34, "Con este umbral", 18, a.INK, a.SANS, 600)
    s += a.box(RX + 20, CY + 60, RW - 40, 70, "#FCE3DD", None, rx=10) + a.text(RX + 36, CY + 90, "FMR · aceptar a un ajeno", 15, a.BAD, a.SANS, 600) + a.text(RX + 36, CY + 116, fmr, 17, a.BAD, a.MONO, 600)
    s += a.box(RX + 20, CY + 142, RW - 40, 70, "#FDEFD5", None, rx=10) + a.text(RX + 36, CY + 172, "FNMR · rechazar al correcto", 15, a.AMB, a.SANS, 600) + a.text(RX + 36, CY + 198, fnmr, 17, a.AMB, a.MONO, 600)
    for k, l in enumerate(note):
        s += a.text(RX + 20, CY + 260 + k * 26, l, 16, a.TXT)
    return s


vis(a, stats("sube", "casi nada", ["Más amable con los vecinos,", "más permisivo con parecidos."]), 1)
vis(a, stats("casi nada", "sube", ["Más seguro, pero el vecino", "a contraluz queda afuera."]), 2)
vis(a, stats("baja", "baja", ["Mover el umbral solo cambia", "el error de lado; esto lo achica."]), 3)

a.add(a.text(48, 580, "Primero el aviso, la foto y el vínculo con la ficha; después la luz y la foto de alta; el umbral, al final.", 17, a.INK, a.SANS, 600))
a.add(a.text(48, 612, "Y se prueba con varias personas distintas: NIST encontró diferencias demográficas en la mayoría de los algoritmos.", 16, a.TXT))
write(a, "10-t1.svg", "Umbral, FMR y FNMR", [12, 37, 62, 90])
