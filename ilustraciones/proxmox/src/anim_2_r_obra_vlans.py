#!/usr/bin/env python3
"""Lección 2 · Resumen, "Cómo se ve en la red": la obra de punta a punta. La cámara (VLAN 10) y el teléfono IP
(VLAN 20) entran al switch por puertos access; un solo cable trunk lleva las dos VLAN etiquetadas hasta eno1 del
host; vmbr0 VLAN aware entrega cada trama sin etiqueta solo al puerto tap con esa VLAN.
Fuentes: guía de administración (Linux bridge VLAN aware, tag por placa, tap<VMID>i<N>), 802.1Q, tarjeta de la lección."""
from _anim_pmx_red import *

a = new(24, "Puente VLAN-aware", "Dos VLAN, un cable, un bridge")
a.steps([
    "La cámara manda video sin etiqueta; el switch la pone en la VLAN 10.",
    "Por el trunk viaja con tag 10; vmbr0 la entrega sin tag a la VM 100.",
    "El teléfono registra en la central: VLAN 20, mismo cable, VM 101.",
    "Comparten cable y bridge, pero ninguna VM ve la VLAN de la otra.",
], still=3)

# ---------- equipos de campo
a.add(dev(a, 48, 196, 226, 84, "Cámara IP", "VLAN 10", icon="camera"))
a.add(dev(a, 48, 440, 226, 84, "Teléfono IP", "VLAN 20", icon="phone"))
# switch
SWX, SWY, SWW, SWH = 340, 262, 190, 196
a.add(a.box(SWX, SWY, SWW, SWH, a.INK, rx=16))
a.add(a.text(SWX + SWW / 2, SWY + 34, "Switch", 19, a.WHITE, a.SANS, 600, "middle"))
a.add(a.box(SWX + 10, SWY + 56, 92, 30, a.NAVY2, rx=8) + a.text(SWX + 56, SWY + 77, "access 10", 15, MINT, a.MONO, 600, "middle"))
a.add(a.box(SWX + 10, SWY + 140, 92, 30, a.NAVY2, rx=8) + a.text(SWX + 56, SWY + 161, "access 20", 15, GOLD, a.MONO, 600, "middle"))
a.add(a.box(SWX + 112, SWY + 98, 70, 30, a.NAVY2, rx=8) + a.text(SWX + 147, SWY + 119, "trunk", 15, SKY, a.MONO, 600, "middle"))
# host
HX, HY, HW, HH = 590, 178, 562, 392
a.add(a.box(HX, HY, HW, HH, a.WHITE, a.LINE, rx=18))
a.add(glyph(a, "server", HX + 18, HY + 16))
a.add(a.text(HX + 60, HY + 36, "pve1", 19, a.INK, a.SANS, 600))
a.add(a.text(HX + 112, HY + 36, "vmbr0 · bridge-vlan-aware yes", 15, a.GREY, a.MONO))
EX, EY = HX + 22, HY + 170
a.add(a.box(EX, EY, 92, 46, a.SLATE, a.LINE, rx=10) + a.text(EX + 46, EY + 29, "eno1", 16, a.INK, a.MONO, 600, "middle"))
BX, BY, BW, BH = HX + 150, HY + 64, 132, 304
a.add(a.box(BX, BY, BW, BH, a.NAVY2, rx=14))
a.add(a.text(BX + BW / 2, BY + 30, "vmbr0", 17, a.WHITE, a.MONO, 600, "middle"))
a.add(a.text(BX + BW / 2, BY + BH - 16, "VLAN 2-4094", 15, SKY, a.MONO, 400, "middle"))
T1Y, T2Y = HY + 112, HY + 304
a.add(a.box(BX + BW - 8, T1Y - 2, 116, 30, a.OKBG, rx=8) + a.text(BX + BW + 50, T1Y + 18, "tap100i0", 15, a.OK, a.MONO, 600, "middle"))
a.add(a.text(BX + BW + 50, T1Y + 48, "PVID 10", 15, a.OK, a.MONO, 600, "middle"))
a.add(a.box(BX + BW - 8, T2Y - 2, 116, 30, a.AMBBG, rx=8) + a.text(BX + BW + 50, T2Y + 18, "tap101i0", 15, a.AMB, a.MONO, 600, "middle"))
a.add(a.text(BX + BW + 50, T2Y + 48, "PVID 20", 15, a.AMB, a.MONO, 600, "middle"))
VX, VW, VH = HX + 412, 132, 92
a.add(dev(a, VX, T1Y - 32, VW, VH, "VM 100", "VMS", tsize=18))
a.add(dev(a, VX, T2Y - 32, VW, VH, "VM 101", "central", tsize=18))

# ---------- cables
CAM = (274, 238)
PHO = (274, 482)
S10 = (SWX + 10, SWY + 71)
S20 = (SWX + 10, SWY + 155)
STR = (SWX + 182, SWY + 113)
ENO = (EX, EY + 23)
a.add(path(f"M{CAM[0]} {CAM[1]} C{CAM[0] + 40} {CAM[1]} {S10[0] - 40} {S10[1]} {S10[0]} {S10[1]}", a.BLUE, 3))
a.add(path(f"M{PHO[0]} {PHO[1]} C{PHO[0] + 40} {PHO[1]} {S20[0] - 40} {S20[1]} {S20[0]} {S20[1]}", a.BLUE, 3))
a.add(path(f"M{STR[0]} {STR[1]} C{STR[0] + 40} {STR[1]} {ENO[0] - 40} {ENO[1]} {ENO[0]} {ENO[1]}", a.BLUE, 5))
a.add(line(EX + 92, EY + 23, BX, EY + 23, a.BLUE, 4))
a.add(line(BX + BW + 108, T1Y + 13, VX, T1Y + 13, a.BLUE, 3))
a.add(line(BX + BW + 108, T2Y + 13, VX, T2Y + 13, a.BLUE, 3))
a.add(a.text((STR[0] + ENO[0]) / 2, ENO[1] - 34, "un cable", 15, a.GREY, a.SANS, 600, "middle"))

# recorridos
IN = (BX + BW / 2, EY + 23)
MID1 = (BX + BW / 2, T1Y + 13)
MID2 = (BX + BW / 2, T2Y + 13)
OUT1 = (VX - 4, T1Y + 13)
OUT2 = (VX - 4, T2Y + 13)


def recorrido(t, src, sp, lab, tagc, tag, mid, out):
    go(a, lab, [src, sp], t, t + 4, a.GREY, hold=0.4)
    go(a, f"{lab} · tag {tag}", [STR, ENO, IN], t + 5, t + 11, tagc, hold=0.4)
    go(a, lab, [IN, mid, out], t + 12, t + 17, a.GREY, hold=1.6)


recorrido(3, CAM, S10, "RTSP", a.OK, 10, MID1, OUT1)
recorrido(52, PHO, S20, "SIP", a.AMB, 20, MID2, OUT2)
# paso 4: las dos a la vez
recorrido(76, CAM, S10, "RTSP", a.OK, 10, MID1, OUT1)
recorrido(79, PHO, S20, "SIP", a.AMB, 20, MID2, OUT2)

# rótulos de etiqueta por tramo
at(a, chip(a, 300, 182, "sin tag", "grey"), 2, 25)
at(a, chip(a, (STR[0] + ENO[0]) / 2, ENO[1] + 18, "tag 10", "ok", anchor="middle"), 28, 50)
at(a, chip(a, VX + VW / 2, T1Y + 70, "sin tag", "grey", anchor="middle"), 37, 50)
at(a, chip(a, 300, 534, "sin tag", "grey"), 51, 75)
at(a, chip(a, (STR[0] + ENO[0]) / 2, ENO[1] + 18, "tag 20", "amb", anchor="middle"), 57, 75)
at(a, chip(a, (STR[0] + ENO[0]) / 2, ENO[1] + 18, "tag 10 · tag 20", "info", anchor="middle"), 80, 100, still=1)
at(a, xmark(a, VX + 10, HY + 195, 11) + a.text(VX + 28, HY + 200, "no ve la 20", 15, a.BAD, a.SANS, 600), 88, 100, still=1)
at(a, xmark(a, VX + 10, HY + 247, 11) + a.text(VX + 28, HY + 252, "no ve la 10", 15, a.BAD, a.SANS, 600), 88, 100, still=1)

status(a, 622, [
    (0, 25, "El puerto access del switch decide la VLAN: la cámara no sabe nada de etiquetas.", a.INK, 0),
    (25, 50, "El tag 10 viaja solo por el trunk; el bridge lo saca al entregar por tap100i0.", a.OK, 0),
    (50, 75, "Otra VLAN no pide otro bridge: es otro tag en la placa de la VM.", a.AMB, 0),
    (75, 100, "Un solo vmbr0 separa las dos redes del edificio, como lo haría un switch.", a.BLUE, 1),
])

write(a, 2, "r1", "Dos VLAN, un cable, un bridge",
      "Animación en cuatro tiempos con una obra completa: una cámara IP en la VLAN 10 y un teléfono IP en la VLAN 20 conectados a puertos access de un switch; "
      "un solo cable trunk va del switch a eno1 del host pve1, donde vmbr0 es VLAN aware con VLAN 2 a 4094; el puerto tap100i0 tiene PVID 10 y lleva a la VM 100 con el VMS, "
      "y tap101i0 tiene PVID 20 y lleva a la VM 101 con la central telefónica. "
      "1: la cámara manda video RTSP sin etiqueta y el puerto access 10 del switch la pone en la VLAN 10. "
      "2: por el trunk viaja con tag 10 hasta eno1; vmbr0 la entrega por tap100i0 sin tag a la VM 100. "
      "3: el teléfono manda su registro SIP; por el mismo cable viaja con tag 20 y vmbr0 lo entrega sin tag a la VM 101 por tap101i0. "
      "4: las dos VLAN viajan a la vez por el mismo cable y el mismo bridge, pero la VM 100 no ve la VLAN 20 y la VM 101 no ve la VLAN 10.",
      [8, 36, 46, 66, 90])
