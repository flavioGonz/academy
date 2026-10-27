#!/usr/bin/env python3
"""Lección 6 · teoría: qué hace el switch con cada trama según la etiqueta y el perfil del puerto."""
from _anim_unifi import *  # noqa

a = new(25, "Puertos con perfil", "¿Trae etiqueta? Lo que decide el switch", [
    "La cámara manda tramas sin etiqueta: caen en la nativa, VLAN 30.",
    "Una trama con etiqueta 10 en ese puerto: Block All la descarta.",
    "Puerto del AP: la gestión sin etiqueta, cada SSID con su etiqueta.",
    "Si cambian la cámara por una notebook, la notebook cae en la VLAN 30.",
    "Con MAC fija o Lock Port to UniFi Device, lo que enchufen no pasa.",
], still=4)

# switch
SX, SY, SW, SH = 360, 190, 520, 310
a.add(a.box(SX, SY, SW, SH, A.INK, None, rx=18))
a.add(a.text(SX + SW / 2, SY + 36, "Switch UniFi", 20, A.WHITE, A.HEAD, 600, "middle"))
LANES = {"gest": ("gestión", 268), "10": ("VLAN 10 · Staff", 324), "20": ("VLAN 20 · Invitados", 380), "30": ("VLAN 30 · CCTV", 436)}
LX0, LX1 = 500, 740
for k, (lab, y) in LANES.items():
    a.add(a.box(LX0, y - 20, LX1 - LX0, 40, A.NAVY2, rx=10) + a.text((LX0 + LX1) / 2, y + 6, lab, 15, SUB_DARK, A.MONO, 600, "middle"))
PY = 352
PL, PR = SX - 14, SX + SW - 14
for x in (PL, PR):
    a.add(a.box(x, PY - 22, 28, 44, A.WHITE, A.LINE, rx=6))
a.add(a.text(SX, SY + SH + 30, "Puerto de la cámara", 16, A.INK, A.SANS, 600))
a.add(a.text(SX, SY + SH + 54, "nativa: CCTV (VLAN 30)", 15, A.TXT, A.MONO))
a.add(a.text(SX, SY + SH + 76, "etiquetadas: Block All", 15, A.BAD, A.MONO, 600))
a.add(a.text(SX + SW, SY + SH + 30, "Puerto del AP", 16, A.INK, A.SANS, 600, "end"))
a.add(a.text(SX + SW, SY + SH + 54, "nativa: gestión", 15, A.TXT, A.MONO, anchor="end"))
a.add(a.text(SX + SW, SY + SH + 76, "etiquetadas: Allow All", 15, A.OK, A.MONO, 600, "end"))

# equipo de la izquierda (arriba) y AP (arriba a la derecha)
DX, DY, DW = 48, 196, 240
a.add(line(a, [(DX + 110, DY + 84), (DX + 110, PY), (PL, PY)], A.LINE, 3))
vis(a, node(a, DX, DY, DW, 84, "Cámara", "no sabe de VLAN", ssize=14), 0, 2)
vis(a, node(a, DX, DY, DW, 84, "Notebook", "en lugar de la cámara", ssize=14, stroke=A.AMB), 3, 4)
AX = 932
a.add(a.box(AX, DY, 220, 84, A.WHITE, A.LINE, rx=14) + ap_icon(a, AX + 38, DY + 42, 20) + a.text(AX + 70, DY + 36, "AP", 20, A.INK, A.HEAD, 600)
      + a.text(AX + 70, DY + 60, "trunk", 14, A.GREY, A.MONO))
a.add(line(a, [(AX + 110, DY + 84), (AX + 110, PY), (PR + 28, PY)], A.LINE, 3))


def lane_hi(key, color, t0, t1, still=0):
    y = LANES[key][1]
    at(a, a.box(LX0, y - 20, LX1 - LX0, 40, "none", color, rx=10, sw=3), t0, t1, still=still)


def left_in(s0, label, color, key=None, hold=None, still=0):
    """Trama desde el equipo de la izquierda; si key, entra a esa VLAN."""
    token(a, [(DX + 110, DY + 100), (DX + 110, PY), (PL - 60, PY)], s0, s0 + 4, label, bg=color,
          hold=(s0 + 4.2 if key else hold), still=(0 if key else still))
    if key:
        y = LANES[key][1]
        token(a, [(SX + 77, PY), (SX + 77, y)], s0 + 4.2, s0 + 6.5, label, bg=color, hold=s0 + 7)
        lane_hi(key, A.OK if color == A.GREY else color, s0 + 6.5, hold or s0 + 15, still)


# 1: sin etiqueta -> VLAN 30
s0, s1 = ph(a, 0)
left_in(s0 + 1, "sin etiqueta", A.GREY, "30", hold=s1 - 1)
vis(a, check(a, LX1 + 30, 436, 13), 0)

# 2: etiqueta 10 -> descartada
s0, s1 = ph(a, 1)
left_in(s0 + 1, "etiqueta 10", A.BLUE, hold=s1 - 1)
vis(a, xmark(a, PL + 14, PY, 15), 1)
vis(a, pill(a, PL - 10, PY + 34, "Block All: se descarta", "bad", anchor="end"), 1)

# 3: AP trunk
s0, s1 = ph(a, 2)
for k, (key, lab, col) in enumerate([("gest", "sin etiqueta", A.GREY), ("10", "etiqueta 10", A.BLUE), ("20", "etiqueta 20", A.CYAN)]):
    y = LANES[key][1]
    t = s0 + 1 + k * 4.5
    token(a, [(AX + 110, DY + 100), (AX + 110, PY), (PR + 90, PY)], t, t + 3, lab, bg=col, hold=t + 3.2)
    token(a, [(PR - 63, PY), (PR - 63, y)], t + 3.2, t + 5.5, lab, bg=col, hold=t + 6)
    lane_hi(key, col if col != A.GREY else "#C9D6E3", t + 5.5, s1 - 1)

# 4: notebook -> VLAN 30
s0, s1 = ph(a, 3)
left_in(s0 + 1, "sin etiqueta", A.AMB, "30", hold=s1 - 1)
vis(a, pill(a, (LX0 + LX1) / 2, 462, "entra a la red de cámaras", "amb", anchor="middle"), 3)

# 5: MAC fija / Lock Port
s0, s1 = ph(a, 4)
left_in(s0 + 1, "sin etiqueta", A.AMB, hold=s1 - 1, still=1)
vis(a, xmark(a, PL + 14, PY, 15), 4)
vis(a, pill(a, PL - 10, PY + 34, "MAC fija · Lock Port", "ok", anchor="end"), 4)

write(a, "6-t1.svg", "Qué hace el switch con cada trama", mid_pcts(a))
