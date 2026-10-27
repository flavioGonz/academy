#!/usr/bin/env python3
"""Lección 17 · Elegir el canal. Teoría "Cómo funciona": el canal es solo una preferencia (qué lista consultar),
cambiarlo no instala nada, y si la lista ofrece una versión más vieja, instalarla es bajar de versión.
"""
from _anim_mikrotik_14_26 import Anim, out

a = Anim(T=24, kicker="MIKROTIK · CANALES", title="El canal solo elige qué lista mirar")
a.steps([
    "En long-term, Check for Updates consulta la lista de long-term.",
    "Pasás a stable: consulta otra lista y ve una versión más nueva.",
    "Volvés a long-term: no se instaló nada. Solo miraste.",
    "Otro equipo con stable pasa a long-term: Install lo baja de versión.",
], still=1)

# ---- equipo
RX, RY, RW, RH = 48, 178, 500, 262
a.add(a.box(RX, RY, RW, RH, a.INK, rx=18))
a.add(a.text(RX + 24, RY + 40, "Equipo", 20, a.WHITE, a.HEAD, 600))
a.add(a.text(RX + 110, RY + 40, "System > Packages > Check for Updates", 15, "#9FC3E3", a.MONO))
CMD = [("channel=long-term", 0, 25), ("channel=stable", 25, 50), ("channel=long-term", 50, 75), ("channel=long-term", 75, 100)]
for c, s_, e in CMD:
    a.add(a.group(a.text(RX + 24, RY + 82, "/system/package/update/set", 16, "#FFFFFF", a.MONO, 600)
                  + a.text(RX + 24, RY + 108, c, 16, "#FFD28A", a.MONO, 600), a.show(s_, e), still=1 if s_ == 25 else 0))
a.add(a.text(RX + 24, RY + 146, "/system/package/update/check-for-updates", 16, "#FFFFFF", a.MONO, 600))
ST = [
    ("latest-version = la instalada", "no hay nada nuevo en esta lista", "#9FC3E3", 0, 25),
    ("latest-version: más nueva", "la instalada no cambió", "#5BE0A5", 25, 50),
    ("latest-version = la instalada", "cambiar de canal no instaló nada", "#9FC3E3", 50, 75),
    ("latest-version: más vieja", "Install la instala igual: es bajar", "#FFD28A", 75, 100),
]
for t1, t2, col, s_, e in ST:
    a.add(a.group(a.text(RX + 24, RY + 196, t1, 18, col, a.MONO, 600) + a.text(RX + 24, RY + 226, t2, 16, "#C9DDF0", a.SANS, 600),
                  a.show(s_, e), still=1 if s_ == 25 else 0))

# ---- listas
LX0, LY0, LW, LH = 590, 178, 562, 262
a.add(a.text(LX0, LY0 + 18, "LISTAS DE VERSIONES (una por canal)", 15, a.GREY, a.MONO, 600))
LISTS = [("long-term", "sale poco · solo arreglos"), ("stable", "cada pocos meses"), ("testing", "cada pocas semanas"), ("development", "lo que viene")]
sel = {0: [(0, 25), (50, 100)], 1: [(25, 50)]}
for i, (n, r) in enumerate(LISTS):
    y = LY0 + 34 + i * 57
    a.add(a.box(LX0, y, LW, 48, a.WHITE, a.LINE, rx=12))
    a.add(a.text(LX0 + 20, y + 31, n, 17, a.INK, a.MONO, 600))
    a.add(a.text(LX0 + LW - 20, y + 31, r, 15, a.GREY, a.SANS, 400, "end"))
    for s_, e in sel.get(i, []):
        a.add(a.group(a.box(LX0, y, LW, 48, "none", a.BLUE, rx=12, sw=3.5) + a.text(LX0 + 200, y + 31, "◀ consulta", 15, a.BLUE, a.MONO, 600),
                      a.show(s_, e, 0.6), still=1 if s_ == 25 else 0))

# ---- eje de versiones
AY = 560
a.add(a.text(48, AY - 70, "VERSIONES", 15, a.GREY, a.MONO, 600))
a.add(a.arrow(f"M150 {AY} H1140", a.GREY, 2.5))
a.add(a.text(48, AY + 6, "más vieja", 15, a.GREY, a.MONO, 400))
a.add(a.text(1140, AY - 16, "más nueva", 15, a.GREY, a.MONO, 400, "end"))
TK = {"long-term": 300, "stable": 560, "testing": 800, "development": 1010}
for n, x in TK.items():
    a.add(f'<line x1="{x}" y1="{AY - 8}" x2="{x}" y2="{AY + 8}" stroke="{a.GREY}" stroke-width="2.5"/>')
    a.add(a.text(x, AY + 30, f"última de {n}" if n in ("long-term", "stable") else n, 15, a.TXT, a.MONO, 400, "middle"))


def latest(x, s_, e, color, still):
    w = 168
    inner = (a.box(x - w / 2, AY - 62, w, 32, color, rx=16) + a.text(x, AY - 40, "latest-version", 15, a.WHITE, a.MONO, 600, "middle")
             + f'<path d="M{x - 8} {AY - 30} L{x} {AY - 16} L{x + 8} {AY - 30} z" fill="{color}"/>')
    a.add(a.group(inner, a.show(s_, e, 0.8), still=still))


latest(TK["long-term"], 0, 25, a.BLUE, 0)
latest(TK["stable"], 25, 50, a.OK, 1)
latest(TK["long-term"], 50, 75, a.BLUE, 0)
latest(TK["long-term"], 75, 100, a.AMB, 0)


def installed(pts, on, off, still):
    inner = (f'<path d="M-9 0 L0 -14 L9 0 z" fill="{a.INK}"/>' + a.box(-52, 4, 104, 30, a.INK, rx=15)
             + a.text(0, 25, "instalada", 15, a.WHITE, a.MONO, 600, "middle"))
    a.add(a.group(inner, a.move(pts), a.show(on, off, 0.5), still=still))


installed([(0, TK["long-term"], AY + 60), (100, TK["long-term"], AY + 60)], 0, 75, 1)
installed([(0, TK["stable"], AY + 60), (88, TK["stable"], AY + 60), (93, TK["long-term"], AY + 60), (100, TK["long-term"], AY + 60)], 75, 100, 0)
a.add(a.group(a.text(TK["stable"] + 70, AY + 86, "Install: baja a long-term. Antes, backup.", 15, a.AMB, a.SANS, 600), a.show(93, 100), still=0))
a.add(a.group(a.text(TK["stable"] + 70, AY + 86, "otro equipo: tiene la de stable", 15, a.INK, a.SANS, 600), a.show(76, 92), still=0))

out(a, 17, 1, "El canal es una preferencia",
    "Animación en cuatro tiempos con un equipo, las cuatro listas de versiones (long-term, stable, testing, development) y un eje de versiones de más vieja a más nueva. "
    "1: con channel=long-term, Check for Updates consulta la lista de long-term y latest-version coincide con la instalada. "
    "2: con channel=stable consulta la lista de stable y latest-version es más nueva; la versión instalada no cambia. "
    "3: de vuelta en long-term, todo sigue igual: cambiar de canal no instaló nada. "
    "4: otro equipo que tiene la versión de stable pasa a long-term; latest-version es más vieja que la instalada e Install la instala igual, o sea baja de versión. Antes, backup.",
    [12, 37, 62, 85, 96])
