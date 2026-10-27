"""Ayudantes de animación propios del curso Omada (teoría). No modifica anim.py: solo suma piezas.

Uso: from _anim_omada import *  →  a = nueva(T, "TEMA", "Título") y las piezas de abajo.
Tiempos en porcentaje del ciclo. `fases` es la lista que devuelve a.steps(...).
"""
import sys
sys.path.insert(0, "/home/claude/ies-training/tools")
from anim import Anim  # noqa

SITE = "/home/claude/ies-training/site2/ilustraciones/omada/"
PREV = "/home/claude/ies-training/ilustraciones/omada/"
DARK_SUB = "#9FC3E3"


def nueva(T, tema, titulo):
    return Anim(T=T, kicker=f"OMADA · {tema}", title=titulo)


def salida(a, lid, n, title, desc, pcts):
    """Guarda <id>-t<n>.svg en site2 y deja las vistas previas en ilustraciones/omada/_t<id>-<n>-*.png."""
    return a.write(f"{SITE}{lid}-t{n}.svg", title=title, desc=desc, preview=pcts, prefix=f"{PREV}_t{lid}-{n}")


# ---------- piezas fijas
def nodo(a, x, y, w, h, titulo, sub=None, dark=True, stroke=None, tsize=20, ssize=14):
    """Equipo o servicio: caja oscura (o blanca) con título y subtítulo en mono."""
    fill = a.INK if dark else a.WHITE
    st = stroke or (None if dark else a.LINE)
    s = a.box(x, y, w, h, fill, st, rx=14)
    ty = y + (h / 2 + 7 if not sub else h / 2 - 3)
    s += a.text(x + 20, ty, titulo, tsize, a.WHITE if dark else a.INK, a.HEAD, 600)
    if sub:
        s += a.text(x + 20, ty + 23, sub, ssize, DARK_SUB if dark else a.GREY, a.MONO)
    return s


def eap(a, cx, cy, r=26, color=None):
    """EAP visto desde abajo: disco con anillo y LED."""
    c = color or a.CYAN
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{a.WHITE}" stroke="{a.LINE}" stroke-width="2"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r * 0.62:.1f}" fill="none" stroke="{c}" stroke-width="2.5"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r * 0.18:.1f}" fill="{c}"/>')


def ok(a, cx, cy, r=14):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{a.OKBG}" stroke="{a.OK}" stroke-width="2"/>'
            f'<path d="M{cx - r * .45:.1f} {cy + r * .02:.1f} L{cx - r * .1:.1f} {cy + r * .38:.1f} L{cx + r * .5:.1f} {cy - r * .35:.1f}" fill="none" stroke="{a.OK}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>')


def bad(a, cx, cy, r=14):
    d = r * 0.38
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{a.BADBG}" stroke="{a.BAD}" stroke-width="2"/>'
            f'<path d="M{cx - d:.1f} {cy - d:.1f} L{cx + d:.1f} {cy + d:.1f} M{cx + d:.1f} {cy - d:.1f} L{cx - d:.1f} {cy + d:.1f}" stroke="{a.BAD}" stroke-width="2.6" stroke-linecap="round"/>')


def linea(a, x1, y1, x2, y2, color=None, w=3, dash=""):
    da = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color or a.BLUE}" stroke-width="{w}"{da} stroke-linecap="round"/>'


def chip(a, x, y, label, fg=None, bg=None, size=15, h=30, anchor="start", stroke=None):
    """Píldora con borde opcional. (x, y) = esquina superior (o centro/extremo según anchor). Texto de 15 px como mínimo."""
    fg = fg or a.INK
    size, h = max(size, 15), max(h, 30)
    w = int(len(label) * size * 0.62 + 26)
    x0 = x - w if anchor == "end" else (x - w / 2 if anchor == "middle" else x)
    st = f' stroke="{stroke}" stroke-width="1.5"' if stroke else ""
    return (f'<rect x="{x0:.1f}" y="{y}" width="{w}" height="{h}" rx="{h / 2}" fill="{bg or a.SLATE}"{st}/>'
            + a.text(x0 + w / 2, y + h * 0.68, label, size, fg, a.MONO, 600, "middle"))


def chipw(label, size=15):
    size = max(size, 15)
    return int(len(label) * size * 0.62 + 26)


# ---------- tiempo
def en(a, inner, t0, t1=100, still=0, fade=1.0):
    """inner visible entre t0 y t1 (porcentajes)."""
    return a.add(a.group(inner, a.show(t0, t1, fade), still=still))


def fase(a, inner, fases, i, j=None, still=0):
    """inner visible desde el inicio de la fase i hasta el final de la fase j (por defecto, la misma)."""
    j = i if j is None else j
    return en(a, inner, fases[i][0], fases[j][1], still)


def viaje(a, inner, x0, y0, x1, y1, t0, t1, hold=2.5, still=0):
    """inner dibujado alrededor de (0,0) viaja de (x0,y0) a (x1,y1) entre t0 y t1, se ve desde t0 hasta t1+hold."""
    mv = a.move([(0, x0, y0), (t0, x0, y0), (t1, x1, y1), (100, x1, y1)])
    op = a.show(t0, min(t1 + hold, 100), 0.6)
    return a.add(a.group(inner, mv, op, still=still))


def paquete(a, label, color=None, size=15, h=34, fg=None):
    """Píldora de paquete centrada en (0,0)."""
    size = max(size, 15)
    w = int(len(label) * size * 0.62 + 28)
    return (f'<rect x="{-w / 2}" y="{-h / 2}" width="{w}" height="{h}" rx="{h / 2}" fill="{color or a.CYAN}"/>'
            + a.text(0, size * 0.36, label, size, fg or a.WHITE, a.MONO, 600, "middle"))


def pie(a, fases, textos, y=640, still=0, colores=None, x=48, size=17):
    """Una línea de explicación abajo, distinta en cada fase."""
    for i, t in enumerate(textos):
        if not t:
            continue
        col = (colores or [a.INK] * len(textos))[i]
        fase(a, a.text(x, y, t, size, col, a.SANS, 600), fases, i, still=1 if i == still else 0)


def solo_fijo(a, inner):
    """Se ve solo en el cuadro fijo (movimiento reducido); mientras corre queda oculto."""
    return a.add(a.group(inner, a.keyframes([(0, 0), (100, 0)]), still=1))
