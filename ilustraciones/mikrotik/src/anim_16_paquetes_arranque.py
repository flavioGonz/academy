#!/usr/bin/env python3
"""Lección 16 · Paquetes al día. Teoría "Cómo funciona": RouterOS no reemplaza paquetes en caliente;
los aplica en el arranque siguiente (después de RouterBOOT), toma los .npk de la raíz de Files y no baja
de versión salvo con /system/package/downgrade.
"""
from _anim_mikrotik_14_26 import Anim, out

a = Anim(T=24, kicker="MIKROTIK · PAQUETES", title="Los paquetes se aplican al arrancar, no en caliente")
a.steps([
    "Download deja la versión nueva preparada. El router sigue con la de siempre.",
    "Reinicio. Antes que RouterOS corre RouterBOOT, el cargador del equipo.",
    "Al arrancar, RouterOS aplica los .npk de la raíz de Files.",
    "Una versión más vieja no se instala sola: hace falta downgrade.",
], still=2)

# ---- línea de arranque (arriba)
ST = [("RouterOS", "en marcha"), ("reinicio", ""), ("RouterBOOT", "cargador"), ("RouterOS", "aplica .npk"), ("RouterOS", "en marcha")]
X0, Y0, W, H, GAP = 48, 182, 196, 84, 31
win = [(0, 25), (25, 33), (33, 42), (42, 50), (50, 75)]
for i, (t, sub) in enumerate(ST):
    x = X0 + i * (W + GAP)
    a.add(a.box(x, Y0, W, H, a.WHITE, a.LINE, rx=14))
    a.add(a.text(x + W / 2, Y0 + (38 if sub else 50), t, 19, a.INK, a.HEAD, 600, "middle"))
    if sub:
        a.add(a.text(x + W / 2, Y0 + 62, sub, 15, a.GREY, a.MONO, 400, "middle"))
    s, e = win[i]
    a.add(a.group(a.box(x, Y0, W, H, "none", a.BLUE, rx=14, sw=3.5), a.show(s, e, 0.6), still=1 if i == 3 else 0))
    if i == 3:
        a.add(a.group(a.box(x, Y0, W, H, "none", a.BLUE, rx=14, sw=3.5), a.show(76, 89, 0.6), still=0))
    if i == 4:
        a.add(a.group(a.box(x, Y0, W, H, "none", a.BLUE, rx=14, sw=3.5), a.show(89, 100, 0.6), still=0))
    if i < len(ST) - 1:
        a.add(a.arrow(f"M{x + W + 4} {Y0 + H / 2} H{x + W + GAP - 4}", a.GREY, 2.5))
# versión que corre
a.add(a.group(a.text(X0 + W / 2, Y0 + H + 26, "versión de siempre", 15, a.TXT, a.MONO, 600, "middle"), a.show(0, 100), still=1))
xl = X0 + 4 * (W + GAP)
a.add(a.group(a.text(xl + W / 2, Y0 + H + 26, "versión nueva", 15, a.OK, a.MONO, 600, "middle"), a.show(50, 75), still=1))
a.add(a.group(a.text(xl + W / 2, Y0 + H + 26, "sigue la de siempre", 15, a.BAD, a.MONO, 600, "middle"), a.show(75, 89), still=0))
a.add(a.group(a.text(xl + W / 2, Y0 + H + 26, "la versión anterior", 15, a.AMB, a.MONO, 600, "middle"), a.show(89, 100), still=0))

# ---- Files (abajo izquierda)
FX, FY, FW, FH = 48, 318, 560, 320
a.add(a.box(FX, FY, FW, FH, a.WHITE, a.LINE, rx=18))
a.add(a.text(FX + 24, FY + 38, "Files", 20, a.INK, a.HEAD, 600))
a.add(a.text(FX + 92, FY + 38, "lo que subiste o bajó Download", 15, a.GREY, a.MONO))


def frow(y, name, where, on, off, still):
    inner = (a.box(FX + 16, y, FW - 32, 50, a.SLATE, rx=10)
             + a.text(FX + 32, y + 31, name, 16, a.INK, a.MONO, 600)
             + a.text(FX + FW - 32, y + 31, where, 15, a.GREY, a.MONO, 400, "end"))
    a.add(a.group(inner, a.show(on, off), still=still))


frow(FY + 60, "routeros-…-arm64.npk", "raíz · nueva", 4, 75, 1)
frow(FY + 120, "hotspot/routeros-…-arm64.npk", "carpeta", 4, 75, 1)
frow(FY + 60, "routeros-…-arm64.npk", "raíz · más vieja", 75, 100, 0)
# marcas al aplicar
a.add(a.group(a.pill(FX + FW - 140, FY + 71, "se aplica", a.OK, a.OKBG, 15, anchor="end"), a.show(43, 75), still=1))
a.add(a.group(a.pill(FX + FW - 112, FY + 131, "se ignora", a.BAD, a.BADBG, 15, anchor="end"), a.show(45, 75), still=1))
a.add(a.group(a.pill(FX + FW - 196, FY + 71, "se ignora", a.BAD, a.BADBG, 15, anchor="end"), a.show(78, 88), still=0))
a.add(a.group(a.pill(FX + FW - 196, FY + 71, "se aplica", a.OK, a.OKBG, 15, anchor="end"), a.show(91, 100), still=0))
a.add(a.group(a.text(FX + 24, FY + 220, "Download: deja la versión lista y espera tu reinicio.", 15, a.TXT, a.SANS, 600)
              + a.text(FX + 24, FY + 246, "Download&Install: baja, instala y reinicia sola.", 15, a.TXT, a.SANS, 600),
              a.show(0, 42), still=0))
a.add(a.group(a.text(FX + 24, FY + 220, "Solo cuenta la raíz de Files. Dentro de una carpeta,", 15, a.TXT, a.SANS, 600)
              + a.text(FX + 24, FY + 246, "el .npk queda ahí y no se instala.", 15, a.TXT, a.SANS, 600),
              a.show(42, 75), still=1))
a.add(a.group(a.text(FX + 24, FY + 220, "Por defecto, al reiniciar no baja de versión.", 15, a.TXT, a.SANS, 600)
              + a.text(FX + 24, FY + 246, "Con downgrade usa los .npk anteriores que subiste.", 15, a.TXT, a.SANS, 600),
              a.show(75, 100), still=0))
a.add(a.text(FX + 24, FY + 294, "Si algo no se instaló, /log/print dice por qué.", 15, a.GREY, a.MONO))

# ---- terminal (abajo derecha)
TX, TY, TW, TH = 640, 318, 512, 320
a.add(a.box(TX, TY, TW, TH, a.INK, rx=18))
a.add(a.text(TX + 24, TY + 38, "Terminal", 18, a.WHITE, a.HEAD, 600))


def term(lines, on, off, still):
    s = ""
    for j, (txt, col) in enumerate(lines):
        s += a.text(TX + 24, TY + 84 + j * 34, txt, 16, col, a.MONO, 600 if j == 0 else 400)
    a.add(a.group(s, a.show(on, off), still=still))


W2, Y2, G2 = "#FFFFFF", "#FFD28A", "#9FC3E3"
term([("/system/package/update/download", W2), ("la versión queda preparada", G2), ("no se instala nada todavía", G2)], 0, 25, 0)
term([("/system/reboot", W2), ("primero corre RouterBOOT", G2), ("después arranca RouterOS", G2)], 25, 42, 0)
term([("/system/package/print", W2), ("routeros  versión nueva", "#5BE0A5"), ("instalada en este arranque", G2)], 42, 75, 1)
term([("/system/reboot", W2), ("hay un .npk más viejo en la raíz", G2), ("no lo instala: sigue la actual", Y2)], 75, 89, 0)
term([("/system/package/downgrade", W2), ("toma los .npk anteriores", G2), ("y reinicia: queda la versión anterior", Y2)], 89, 100, 0)

out(a, 16, 1, "Paquetes: se aplican en el arranque",
    "Animación en cuatro tiempos. 1: Download deja la versión nueva preparada en Files y el router sigue con la de siempre; Download&Install en cambio reinicia sola. "
    "2: al reiniciar, antes que RouterOS corre RouterBOOT, el cargador del equipo. "
    "3: al arrancar, RouterOS aplica el .npk que está en la raíz de Files; el que está dentro de una carpeta se ignora. El equipo queda con la versión nueva. "
    "4: si en la raíz hay un .npk más viejo, al reiniciar no se instala; /system/package/downgrade le indica que use los .npk anteriores y reinicia. "
    "Si algo no se instaló, /log/print dice por qué.",
    [12, 30, 60, 82, 95])
