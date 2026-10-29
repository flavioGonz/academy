#!/usr/bin/env python3
"""Lección 4 · teoría: cómo se lee una cadena (deciden / anotan), jump que vuelve y cadena vacía = accept."""
from _anim_mikrotik_1_13 import *

a = Anim(T=28, kicker="MIKROTIK · CÓMO FUNCIONA", title="Las reglas se leen en orden hasta que una decide")
a.steps([
    "WinBox desde la oficina (admins): jump a gestion-wan y accept decide.",
    "WinBox desde otra IP: en gestion-wan nadie decide y vuelve a input.",
    "De vuelta en input, sigue abajo: el drop de la defconf decide.",
    "Ping del router: passthrough anota y sigue; al final de la cadena, pasa.",
], still=1)

ACT = {"accept": (a.OK, a.OKBG), "drop": (a.BAD, a.BADBG), "jump": (a.BLUE, "#E3EEF9"), "passthrough": (a.GREY, "#E6EDF4")}


def panel(x, y, w, title, rows, end_txt):
    h = 50 + len(rows) * 62 + 56
    s = a.box(x, y, w, h, a.WHITE, a.LINE)
    s += a.text(x + 18, y + 32, title, 16, a.INK, a.MONO, 600)
    ys = []
    for i, (act, txt) in enumerate(rows):
        ry = y + 50 + i * 62
        fg, bg = ACT[act]
        s += a.box(x + 12, ry, w - 24, 50, a.SLATE, rx=10)
        pw = int(len(act) * 14 * 0.62 + 26)
        s += a.box(x + 22, ry + 11, pw, 28, bg, rx=14) + a.text(x + 22 + pw / 2, ry + 30, act, 14, fg, a.MONO, 600, "middle")
        s += a.text(x + 34 + pw, ry + 30, txt, 14, a.INK, a.MONO)
        ys.append(ry)
    ey = y + 50 + len(rows) * 62
    s += a.box(x + 12, ey, w - 24, 44, "none", a.GREY, rx=10, sw=1.5, extra='stroke-dasharray="6 5"')
    s += a.text(x + 26, ey + 28, end_txt, 14, a.GREY, a.MONO)
    ys.append(ey)
    return s, ys, h


IX, IY, IW = 48, 182, 600
s, iy, ih = panel(IX, IY, IW, "chain=input (resumida)", [
    ("accept", "established,related,untracked"),
    ("jump", "→ gestion-wan · WAN tcp 22,8291"),
    ("drop", "all not coming from LAN"),
], "fin de la cadena: el paquete pasa")
a.add(s)
GX, GY, GW = 700, 182, 452
s, gy, gh = panel(GX, GY, GW, "chain=gestion-wan", [("accept", "src-address-list=admins")], "fin: vuelve a input")
a.add(s)
OX, OY = 700, GY + gh + 20
s, oy, oh = panel(OX, OY, GW, "chain=output", [("passthrough", "lab: cuenta output")], "fin de la cadena: pasa")
a.add(s)


def ring(x, w, y, h, col, t0, t1, label="", still=0):
    inner = a.box(x, y - 3, w, h + 6, "none", col, rx=12, sw=3)
    if label:
        inner += a.text(x + w - 14, y + h / 2 + 5, label, 14, col, a.MONO, 600, "end")
    a.add(during(a, inner, t0, t1, still=still, fade=0.5))


RI = (IX + 6, IW - 12)
RG = (GX + 6, GW - 12)
# 1. admins
ring(*RI, iy[0], 50, a.AMB, 2, 6, "no: es new")
ring(*RI, iy[1], 50, a.BLUE, 6, 25, "coincide")
ring(*RG, gy[0], 50, a.OK, 10, 25, "decide")
# 2 y 3. otra IP
ring(*RI, iy[0], 50, a.AMB, 27, 31, "no: es new", still=0)
ring(*RI, iy[1], 50, a.BLUE, 31, 75, "coincide", still=1)
ring(*RG, gy[0], 50, a.AMB, 36, 50, "no coincide", still=1)
ring(*RG, gy[1], 44, a.BLUE, 40, 75, "", still=1)
ring(*RI, iy[2], 50, a.BAD, 53, 75, "decide", still=0)
# 4. output
ring(OX + 6, GW - 12, oy[0], 50, a.GREY, 77, 98.5, "suma y sigue")
ring(OX + 6, GW - 12, oy[1], 44, a.OK, 83, 98.5, "")

# flechas jump y vuelta
jy = iy[1] + 18
a.add(a.group(a.arrow(f"M{IX + IW} {jy} H{IX + IW + 18} V{gy[0] + 25} H{GX - 4}", a.BLUE, 3), a.show(7, 25, 0.5), still=0))
a.add(a.group(a.arrow(f"M{IX + IW} {jy} H{IX + IW + 18} V{gy[0] + 25} H{GX - 4}", a.BLUE, 3), a.show(32, 50, 0.5), still=1))
ry = gy[1] + 30
a.add(a.group(a.arrow(f"M{GX} {ry} H{IX + IW + 34} V{iy[2] + 25} H{IX + IW + 4}", a.BLUE, 3, "6 5"), a.show(41, 75, 0.5), still=1))

# paquete en evaluación y resultado
PY = 592
pk = [(0, 25, "TCP 8291 · new · desde 203.0.113.25 (admins)", "ACEPTADO", a.OK, a.OKBG, 0),
      (25, 50, "TCP 8291 · new · desde otra IP de internet", "sigue…", a.BLUE, "#E3EEF9", 1),
      (50, 75, "TCP 8291 · new · desde otra IP de internet", "DESCARTADO", a.BAD, a.BADBG, 0),
      (75, 100, "ping 1.1.1.1 · lo genera el router", "SALE", a.OK, a.OKBG, 0)]
a.add(a.text(48, PY, "PAQUETE", 13, a.GREY, a.MONO, extra='letter-spacing="2"'))
for t0, t1, txt, res, fg, bg, st in pk:
    inner = a.text(140, PY, txt, 17, a.INK, a.MONO, 600)
    inner += a.pill(1152, PY - 20, res, fg, bg, 15, 30, "end")
    a.add(during(a, inner, t0, t1, still=st, fade=0.6))
a.add(a.text(48, 636, "accept, drop, reject y jump deciden. passthrough y log anotan y dejan seguir.", 16, a.TXT, a.SANS, 600))

p, pre = out(4, 1)
a.write(p, title="Cómo se lee una cadena del firewall",
        desc="Animación en cuatro tiempos sobre tres cadenas: input resumida (accept established,related,untracked; jump a gestion-wan para WAN tcp 22 y 8291; "
             "drop all not coming from LAN), gestion-wan (accept src-address-list=admins) y output (un passthrough de laboratorio). 1: un WinBox nuevo desde "
             "203.0.113.25, que está en admins, no coincide con established, coincide con el jump y en gestion-wan el accept decide. 2: un WinBox desde otra IP "
             "salta a gestion-wan, ahí ninguna regla decide y vuelve a input, justo debajo del jump. 3: sigue bajando y el drop de la defconf lo descarta. "
             "4: un ping que genera el router pasa por output: el passthrough suma y deja seguir, nadie decide y al final de la cadena el paquete pasa.",
        preview=[12, 45, 64, 90], prefix=pre)
