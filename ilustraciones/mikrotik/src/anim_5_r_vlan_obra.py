#!/usr/bin/env python3
"""Lección 5 (VLAN por sistema), Resumen: una cámara infectada en la VLAN 20 de un edificio. Su broadcast no sale
de la VLAN 20, el video con el NVR va directo por el switch, y para llegar a una PC de la VLAN 10 tiene que pasar
por el router, donde forward lo descarta. Una notebook enchufada en la boca de la cámara cae en la VLAN 20."""
from _anims_10_19 import Anim, en, ventanas, fijo, dev, viaje, linea, narr, escribir, pill_c, place, marca, LIGHT, GOLD, MINT, CORAL, GHOST

a = Anim(T=28, kicker="MIKROTIK · VLAN · EN LA RED", title="Cada sistema en su VLAN: la cámara no ve la oficina")
a.steps([
    "La cámara manda un broadcast: llega solo a la VLAN 20.",
    "El video con el NVR va directo por el switch, en la VLAN 20.",
    "Para llegar a la PC tiene que pasar por el router: drop.",
    "Una notebook en la boca de la cámara cae en la VLAN 20.",
], still=2)

V20, V10 = a.AMB, a.BLUE
a.add(a.box(420, 172, 340, 104, a.INK, rx=16) + a.text(440, 204, "MikroTik", 19, "#FFFFFF", a.SANS, 600)
      + a.text(440, 228, "bridge · vlan-filtering=yes", 15, LIGHT, a.MONO) + a.text(440, 252, "vlan10-datos · vlan20-cctv", 15, LIGHT, a.MONO))
RP = (790, 172, 362, 104)
a.add(a.box(*RP, a.WHITE, a.LINE, rx=14) + a.text(808, 196, "chain=forward", 15, a.INK, a.MONO, 700)
      + a.text(808, 218, "in-interface=vlan20-cctv", 15, a.TXT, a.MONO) + a.text(808, 240, "out-interface=vlan10-datos", 15, a.TXT, a.MONO)
      + a.text(808, 262, "action=drop", 15, a.BAD, a.MONO, 700))
en(a, a.box(*RP, "none", a.BAD, rx=14, sw=3), 60, 75, still=1)

# switch del piso
SX, SY, SW = 230, 328, 740
a.add(a.box(SX, SY, SW, 76, a.WHITE, "#C2D4E6", rx=14) + a.text(SX + 18, SY + 30, "Switch del piso", 17, a.INK, a.SANS, 600))
PORTS = [(350, "access 20", V20), (600, "access 20", V20), (850, "access 10", V10)]
for x, t, c in PORTS:
    a.add(a.box(x - 56, SY + 40, 112, 28, c, rx=8) + a.text(x, SY + 59, t, 14, "#FFFFFF", a.MONO, 700, "middle"))
a.add(a.box(560, SY + 4, 150, 28, a.INK, rx=8) + a.text(635, SY + 23, "trunk 10,20,99", 14, "#FFFFFF", a.MONO, 700, "middle"))
a.add(linea(590, 276, 590, SY + 4, a.LINE, 5))

DEV = [(240, "Cámara", "10.10.20.60", "camera"), (490, "NVR", "10.10.20.50", "server"), (740, "PC oficina", "10.10.10.25", "laptop")]
for i, (x, t, s, ic) in enumerate(DEV):
    if i == 0:
        en(a, dev(a, x, 468, 220, 84, t, s, ic, hl=a.BAD), 0, 75, still=1)
        en(a, dev(a, x, 468, 220, 84, "Notebook", "en esa boca", "laptop", hl=a.AMB), 75, 100)
    else:
        a.add(dev(a, x, 468, 220, 84, t, s, ic))
    a.add(linea(x + 110, 468, PORTS[i][0], SY + 68, a.LINE, 4))
en(a, a.text(350, 580, "infectada", 15, a.BAD, a.SANS, 700, "middle"), 0, 75, still=1)

# leyenda
for i, (t, c) in enumerate((("VLAN 20 · CCTV", V20), ("VLAN 10 · datos", V10), ("VLAN 99 · gestión", a.INK))):
    a.add(a.box(48, 180 + i * 40, 18, 18, c, rx=4) + a.text(76, 195 + i * 40, t, 15, a.INK, a.SANS, 600))

CAM, NVR, PC = (350, 468), (600, 468), (850, 468)
ARR = (350, 412)
# 1: broadcast
for t0, lbl in ((3, "broadcast"), (77, "broadcast")):
    viaje(a, lbl, [(350, 456), (350, 412)], t0, t0 + 4, bg=V20, size=14, hold=0.2)
    viaje(a, "20", [(350, 412), (600, 412), (600, 450)], t0 + 4.5, t0 + 9, bg=V20, size=14, hold=3)
    viaje(a, "20", [(590, 326), (590, 292)], t0 + 4.5, t0 + 9, bg=V20, size=14, hold=3)
    en(a, marca(a, 960, 468, ok=False) + a.text(850, 588, "no le llega", 15, a.BAD, a.SANS, 700, "middle"), t0 + 9, t0 + 21)
    en(a, a.text(600, 588, "le llega", 15, V20, a.SANS, 700, "middle"), t0 + 9, t0 + 21)
# 2: video
for t0 in (28, 38):
    viaje(a, "RTSP", [(600, 456), (600, 412), (350, 412), (350, 450)], t0, t0 + 5, bg=a.OK, size=14, hold=0.3)
    viaje(a, "video", [(350, 450), (350, 412), (600, 412), (600, 456)], t0 + 5.5, t0 + 10, bg=a.OK, size=14, hold=0.3)
en(a, a.text(470, 448, "no pasa por el router", 15, a.OK, a.SANS, 700, "middle"), 30, 50)
# 3: hacia la PC
viaje(a, "a 10.10.10.25", [(350, 456), (350, 412), (590, 412), (590, 300)], 52, 59, bg=V20, size=14, hold=0.5)
en(a, a.text(672, 306, "etiqueta 20", 15, V20, a.MONO, 700), 55, 75, still=1)
en(a, marca(a, 590, 276, ok=False), 60, 75, still=1)
fijo(a, place(pill_c(a, "a 10.10.10.25", "#FFFFFF", V20, 14), 590, 300))

narr(a, [
    (0, 25, "El broadcast queda en la VLAN 20: cámaras, NVR y el router por el trunk. La PC ni se entera.", a.TXT),
    (25, 50, "Dentro de la misma VLAN el switch entrega directo: el video no carga al router.", a.OK),
    (50, 75, "10.10.10.25 es otra red: va al gateway 10.10.20.1, y en forward la regla la descarta.", a.BAD),
    (75, 100, "La boca es access con PVID 20: quien se enchufe ahí ve cámaras, no la red de oficina.", a.AMB),
], y=640, still_idx=2)

escribir(a, "5-r1", "Cada sistema en su VLAN",
         "Animación en cuatro tiempos en un edificio. Arriba el MikroTik con un bridge y vlan-filtering=yes, con vlan10-datos y vlan20-cctv, y la regla chain=forward in-interface=vlan20-cctv "
         "out-interface=vlan10-datos action=drop. En el medio, el switch del piso con un trunk de las VLAN 10, 20 y 99 hacia el router y tres bocas access: "
         "la cámara 10.10.20.60 y el NVR 10.10.20.50 en la VLAN 20, y la PC de la oficina 10.10.10.25 en la VLAN 10. La cámara está infectada. "
         "1: la cámara manda un broadcast; llega al NVR y, etiquetado con 20, al router por el trunk, pero no a la PC. "
         "2: el video entre el NVR y la cámara va directo por el switch dentro de la VLAN 20, sin pasar por el router. "
         "3: la cámara intenta llegar a la PC 10.10.10.25; es otra red, así que va a su gateway por el trunk con etiqueta 20 y en forward la regla la descarta. "
         "4: si alguien enchufa una notebook en la boca de la cámara, cae en la VLAN 20 por el PVID: su broadcast llega a cámaras y NVR, no a la oficina.",
         [10, 33, 56, 64, 86, 95])
