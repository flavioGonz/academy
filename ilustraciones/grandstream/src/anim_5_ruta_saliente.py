#!/usr/bin/env python3
"""Lección 5 · teoría: qué hace la central cuando una extensión marca (patrón, privilegio, PIN, Strip, troncal)."""
from _anim_grandstream import G

g = G(T=28, fix=74, kicker="GRANDSTREAM · RUTAS SALIENTES", title="Cinco controles entre el teclado y el troncal")
g.steps([
    "La 1001 marca 929001007: coincide con _9NXXXXXXX, la ruta nacional.",
    "Privilegio: la 1001 es National y la ruta pide National. Pasa.",
    "La nacional no pide PIN. Strip 1 saca el 9: al proveedor va 29001007.",
    "El principal contesta 503: la central prueba el troncal de failover.",
    "La 1002, en Local, marca 00…: coincide con _00X. y el nivel no alcanza.",
])

W, GAP, Y0, H = 208, 16, 186, 150
CX = [48 + W / 2 + i * (W + GAP) for i in range(5)]
names = ["1 · Patrón", "2 · Privilegio", "3 · PIN", "4 · Strip", "5 · Troncal"]
for i, n in enumerate(names):
    x = 48 + i * (W + GAP)
    g.add(g.box(x, Y0, W, H, g.WHITE, g.LINE, rx=14))
    g.add(g.text(x + 18, Y0 + 32, n, 18, g.INK, g.HEAD, 600))


def stage(i, lines, t0, t1, col=None, frame=None):
    x = 48 + i * (W + GAP)
    s = ""
    if frame:
        s += g.box(x, Y0, W, H, "none", frame, rx=14, sw=3)
    for k, ln in enumerate(lines):
        s += g.text(x + 18, Y0 + 66 + k * 24, ln, 15, col if (k == len(lines) - 1 and col) else g.INK, g.MONO, 600)
    g.appear(s, t0, t1)


# escenario A: 1001 nacional
stage(0, ["_9NXXXXXXX", "ruta nacional"], 3, 80, g.OK, g.OK)
stage(1, ["1001: National", "ruta: National", "pasa"], 23, 80, g.OK, g.OK)
stage(2, ["la ruta", "no pide PIN"], 43, 80, g.GREY, g.LINE)
stage(3, ["Strip 1", "saca el 9", "→ 29001007"], 48, 80, g.OK, g.OK)
stage(4, ["principal: 503", "→ failover", "sale"], 65, 80, g.OK, g.OK)
# escenario B: 1002 local
stage(0, ["_00X.", "ruta internacional"], 82, 100, g.OK, g.OK)
stage(1, ["1002: Local", "ruta:", "International", "rechaza"], 87, 100, g.BAD, g.BAD)
for i in (2, 3, 4):
    stage(i, ["no llega"], 89, 100, g.GREY)

# ficha que recorre las etapas
LY = 372
g.add(f'<line x1="48" y1="{LY}" x2="1152" y2="{LY}" stroke="{g.LINE}" stroke-width="2" stroke-dasharray="4 6"/>')


def ride(label, bg, kf, t0, t1):
    g.add(g.group(g.chip(label, bg=bg, size=14, h=30), g.move(kf), g.show(t0, t1, 0.6), still=g.st(t0, t1)))


ride("929001007", g.CYAN, [(0, CX[0], LY), (21, CX[0], LY), (24, CX[1], LY), (42, CX[1], LY), (45, CX[2], LY), (46, CX[2], LY), (49, CX[3], LY), (100, CX[3], LY)], 1, 51)
ride("29001007", g.CYAN, [(0, CX[3], LY), (61, CX[3], LY), (64, CX[4], LY), (100, CX[4], LY)], 51, 80)
ride("00…", g.CYAN, [(0, CX[0], LY), (85, CX[0], LY), (88, CX[1], LY), (100, CX[1], LY)], 81, 100)
g.appear(g.mark(CX[1] + 60, LY, False, 15), 89, 100)

# tablas de abajo
TY = 420
g.add(g.box(48, TY, 640, 150, g.WHITE, g.LINE, rx=14))
g.add(g.text(68, TY + 32, "Rutas salientes", 18, g.INK, g.HEAD, 600))
for k, (h, xx) in enumerate([("patrón", 68), ("privilegio", 270), ("PIN", 450), ("Strip", 560)]):
    g.add(g.text(xx, TY + 60, h, 13, g.GREY, g.MONO))
rows = [("_9NXXXXXXX", "National", "no", "1"), ("_00X.", "International", "sí", "no")]
for r, row in enumerate(rows):
    y = TY + 92 + r * 34
    for v, xx in zip(row, (68, 270, 450, 560)):
        g.add(g.text(xx, y, v, 16, g.INK, g.MONO, 600))
g.appear(g.box(56, TY + 70, 624, 32, "none", g.OK, rx=8, sw=2), 0, 80)
g.appear(g.box(56, TY + 104, 624, 32, "none", g.BAD, rx=8, sw=2), 81, 100)

g.add(g.box(712, TY, 440, 150, g.WHITE, g.LINE, rx=14))
g.add(g.text(732, TY + 32, "Troncales de la ruta nacional", 18, g.INK, g.HEAD, 600))
g.add(g.text(732, TY + 66, "principal", 16, g.INK, g.MONO, 600))
g.add(g.text(732, TY + 100, "failover", 16, g.INK, g.MONO, 600))
g.appear(g.pillc(1060, TY + 46, "503", g.BAD, g.BADBG), 65, 80)
g.appear(g.pillc(1060, TY + 80, "toma la llamada", g.OK, g.OKBG), 68, 80)
g.add(g.note(48, 588, 1104, None, ["Failover: sin respuesta en 32 segundos, o respuesta 403, 407, 408, 503 o 603 del principal."], "info"))

g.finish(5, 1, "Cinco controles entre el teclado y el troncal",
         "Animación en cinco tiempos con cinco etapas en fila: patrón, privilegio, PIN, Strip y troncal, y un número que las recorre. "
         "1: la interna 1001 marca 929001007 y coincide con el patrón _9NXXXXXXX de la ruta nacional. "
         "2: la 1001 tiene privilegio National y la ruta pide National: pasa. "
         "3: la ruta nacional no pide PIN; Strip 1 saca el 9 y al proveedor va 29001007. "
         "4: el troncal principal contesta 503 y la central prueba el troncal de failover, que toma la llamada. "
         "5: la interna 1002, con privilegio Local, marca 00 y un número del exterior; coincide con _00X. de la ruta internacional, que pide International y PIN; el nivel no alcanza y la central rechaza la llamada, que no llega al PIN, al Strip ni al troncal. "
         "Abajo, la tabla de rutas y la regla de failover: sin respuesta en 32 segundos, o respuesta 403, 407, 408, 503 o 603 del principal.",
         [10, 30, 52, 74, 95])
