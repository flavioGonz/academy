#!/usr/bin/env python3
"""Lección 5 · teoría: la etiqueta 802.1Q que se pone en el access, viaja por el trunk, sube al CPU por el bridge y se filtra en el ingreso."""
from _anim_mikrotik_1_13 import *

a = Anim(T=26, kicker="MIKROTIK · LECCIÓN 5 · CÓMO FUNCIONA", title="La etiqueta de VLAN: dónde se pone y dónde se saca")
a.steps([
    "La cámara manda sin etiqueta. ether2, access con PVID 20, le asigna la VLAN 20.",
    "Por el trunk viaja etiquetada; en el access del otro switch sale sin etiqueta.",
    "Hacia el router, bridge es un puerto más: tagged en la 20, vlan20-cctv la recibe.",
    "Llega una trama etiquetada a un access: ingress-filtering la descarta.",
], still=1)


def frame(tag=False, bad=False):
    s = f'<rect x="-24" y="-13" width="48" height="26" rx="5" fill="{a.WHITE}" stroke="{a.BAD if bad else a.INK}" stroke-width="2"/>'
    if tag:
        s += f'<rect x="-46" y="-13" width="26" height="26" rx="5" fill="{a.CYAN}"/>' + a.text(-33, 6, "20", 13, a.WHITE, a.MONO, 600, "middle")
    return s


# leyenda 802.1Q
a.add(a.box(48, 186, 226, 214, a.WHITE, a.LINE))
a.add(a.text(64, 214, "802.1Q", 17, a.INK, a.SANS, 600))
a.add(place(a, frame(), 106, 246))
a.add(a.text(142, 251, "sin etiqueta", 14, a.TXT, a.MONO))
a.add(place(a, frame(True), 106, 288))
a.add(a.text(142, 293, "VLAN 20", 14, a.TXT, a.MONO))
a.add(a.text(64, 334, "4 bytes extra", 14, a.TXT, a.MONO))
a.add(a.text(64, 358, "VLAN ID de 12 bits", 14, a.TXT, a.MONO))
a.add(a.text(64, 382, "4094 posibles", 14, a.TXT, a.MONO))

# cámara
a.add(device(a, 48, 440, 168, 72, "Cámara", "manda sin etiqueta", ssize=13))
# router / bridge
RX, RY, RW, RH = 290, 186, 560, 344
a.add(a.box(RX, RY, RW, RH, a.SLATE, a.LINE))
a.add(a.text(RX + 18, RY + 30, "MikroTik · bridge con vlan-filtering", 16, a.INK, a.SANS, 600))
a.add(a.box(RX + 120, RY + 46, 320, 54, a.INK, rx=10))
a.add(a.text(RX + 140, RY + 79, "vlan20-cctv · 10.10.20.1/24", 15, a.WHITE, a.MONO, 600))
a.add(a.box(RX + 180, RY + 146, 200, 50, a.WHITE, a.LINE, rx=10))
a.add(a.text(RX + 196, RY + 168, "bridge", 15, a.INK, a.MONO, 600))
a.add(a.text(RX + 196, RY + 188, "puerto hacia el CPU", 13, a.GREY, a.MONO))
a.add(line(RX + 280, RY + 100, RX + 280, RY + 146, a.GREY, 2))
BUS = RY + 230
a.add(line(RX + 105, BUS, RX + 455, BUS, a.GREY, 2))
a.add(line(RX + 280, RY + 196, RX + 280, BUS, a.GREY, 2))
P2 = (RX + 30, RY + 262, 150, 56)
P4 = (RX + 380, RY + 262, 150, 56)
for (x, y, w, h), n, d in [(P2, "ether2", "access · PVID 20"), (P4, "ether4", "trunk")]:
    a.add(a.box(x, y, w, h, a.WHITE, a.LINE, rx=10))
    a.add(a.text(x + 14, y + 24, n, 15, a.INK, a.MONO, 600))
    a.add(a.text(x + 14, y + 44, d, 13, a.GREY, a.MONO))
    a.add(line(x + 75, y, x + 75, BUS, a.GREY, 2))
# enlaces externos
LY = 476
a.add(line(216, LY, RX + 30, LY, a.BLUE, 3))
a.add(line(RX + 530, LY, 930, LY, a.BLUE, 5))
a.add(a.text(890, LY + 34, "trunk", 13, a.BLUE, a.MONO, 600, "middle"))
# switch y equipo
a.add(device(a, 930, 430, 222, 92, "Switch del piso", "access VLAN 20", ssize=13))
a.add(device(a, 930, 220, 222, 80, "Equipo VLAN 20", "recibe sin etiqueta", ssize=13))
a.add(line(1041, 300, 1041, 430, a.BLUE, 3))

# 1. sin etiqueta hasta ether2; se le asigna la 20
a.add(travel(a, frame(), [(238, LY - 28), (300, LY - 28)], 2, 9, hold=3))
a.add(during(a, a.pill(RX + 30, RY + 226, "+ VLAN 20", a.CYAN, "#E1F5FB", 13, 26), 10, 25))
# 2. por el trunk con etiqueta; sale sin etiqueta
x2 = P2[0] + 75
x4 = P4[0] + 75
a.add(travel(a, frame(True), [(x2 + 10, BUS - 22), (x4 - 30, BUS - 22), (x4 + 70, LY - 28), (900, LY - 28)], 27, 37, hold=2))
a.add(travel(a, frame(), [(1080, 400), (1080, 330)], 40, 45, hold=4))
# 3. al CPU por el puerto bridge
a.add(travel(a, frame(True), [(x2 + 10, BUS - 22), (RX + 250, BUS - 22), (RX + 250, RY + 128)], 52, 60, hold=14))
a.add(during(a, check(a, RX + 466, RY + 73), 60, 75))
a.add(during(a, a.box(RX + 176, RY + 142, 208, 58, "none", a.OK, rx=12, sw=3), 55, 75))
# 4. etiquetada en un access: se descarta
a.add(travel(a, frame(True, bad=True), [(244, LY - 28), (266, LY - 28)], 77, 83, hold=15.5))
a.add(during(a, xmark(a, RX + 16, LY - 28, 13), 83, 98.5))
a.add(during(a, a.text(RX + 30, RY + 250, "frame-types + ingress-filtering", 13, a.BAD, a.MONO, 600), 83, 98.5))

# cuadro fijo: el recorrido completo
a.add(still_only(a, place(a, frame(), 262, LY - 28) + place(a, frame(True), 890, LY - 28) + place(a, frame(), 1080, 365)
                 + place(a, frame(True), RX + 250, RY + 128)))

# tabla VLAN
a.add(term(a, 48, 560, 1104, ["/interface/bridge/vlan/add bridge=bridge tagged=bridge,ether4 untagged=ether2,ether3 vlan-ids=20"], size=14))
CMD = "/interface/bridge/vlan/add bridge=bridge tagged=bridge,ether4 untagged=ether2,ether3 vlan-ids=20"
cx = 66 + CMD.index("tagged=bridge") * 14 * 0.6
a.add(during(a, a.box(cx - 4, 572, len("tagged=bridge") * 8.4 + 8, 28, "none", MINT, rx=6, sw=2.5), 52, 75))

p, pre = out(5, 1)
a.write(p, title="Recorrido de una trama con VLAN",
        desc="Animación en cuatro tiempos sobre un MikroTik con bridge y vlan-filtering: ether2 access con PVID 20, ether4 trunk hacia un switch del piso, "
             "el puerto bridge hacia el CPU y la interfaz vlan20-cctv con 10.10.20.1/24. 1: la cámara manda una trama sin etiqueta y ether2 le asigna la VLAN 20. "
             "2: la trama viaja etiquetada con 20 por el trunk y sale sin etiqueta por el puerto access del otro switch hacia el equipo de la VLAN 20. "
             "3: hacia el router, la trama sube por el puerto bridge, que está como tagged en la VLAN 20, y la recibe vlan20-cctv. "
             "4: una trama etiquetada que llega a un puerto access se descarta por frame-types e ingress-filtering. Abajo, la entrada de la tabla: "
             "tagged=bridge,ether4 untagged=ether2,ether3 vlan-ids=20.",
        preview=[12, 34, 64, 92], prefix=pre)
