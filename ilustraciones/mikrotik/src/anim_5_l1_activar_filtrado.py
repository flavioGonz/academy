#!/usr/bin/env python3
"""Lección 5 (VLAN por sistema), Laboratorio paso 4: qué pasa al poner vlan-filtering=yes. Antes, el PVID no tiene
efecto y la notebook en ether2 llega a 192.168.88.1; después, lo que entra por ether2 es VLAN 20 y llega a vlan20-cctv,
no a la IP del bridge: esa sesión se corta. La de ether5, fuera del bridge, sigue."""
from _anims_10_19 import Anim, en, ventanas, fijo, dev, viaje, linea, narr, escribir, pill_c, place, marca, LIGHT, GOLD, MINT, CORAL, GHOST

a = Anim(T=24, kicker="MIKROTIK · LABORATORIO · PASO 4", title="vlan-filtering=yes: la tabla manda de golpe")
a.steps([
    "Antes: el PVID no tiene efecto y ether2 llega a 192.168.88.1.",
    "Activás vlan-filtering=yes: la tabla VLAN empieza a mandar.",
    "Lo de ether2 entra como VLAN 20: la sesión a .88.1 se corta.",
    "ether5 está fuera del bridge: la sesión de rescate sigue.",
], still=2)

V20 = a.AMB
a.add(a.box(300, 172, 600, 304, a.SLATE, "#C2D4E6", rx=18) + a.text(320, 200, "Router", 17, a.INK, a.HEAD, 600))
a.add(a.box(316, 212, 352, 188, a.WHITE, "#C2D4E6", rx=14, sw=2, extra='stroke-dasharray="7 6"') + a.text(332, 236, "bridge", 15, a.GREY, a.MONO, 600))
CH = {"ether2": 252, "ether3": 302, "ether4": 352}
for p, y in CH.items():
    a.add(a.box(332, y - 4, 104, 34, a.NAVY2, rx=8) + a.text(384, y + 18, p, 15, "#FFFFFF", a.MONO, 600, "middle"))
a.add(a.text(450, 270, "PVID 20", 15, V20, a.MONO, 700) + a.text(450, 320, "PVID 20", 15, V20, a.MONO, 700) + a.text(450, 370, "trunk", 15, a.GREY, a.MONO, 700))
a.add(a.box(332, 420, 104, 34, a.OK, rx=8) + a.text(384, 442, "ether5", 15, "#FFFFFF", a.MONO, 700, "middle")
      + a.text(450, 442, "fuera del bridge", 15, a.OK, a.SANS, 700))
# CPU
CX0 = 694
a.add(a.box(CX0, 212, 190, 242, a.INK, rx=14) + a.text(CX0 + 16, 238, "CPU del router", 15, LIGHT, a.MONO))
ENT = {"bridge": (262, "bridge · VLAN 1", "192.168.88.1"), "v20": (330, "vlan20-cctv", "10.10.20.1"), "e5": (398, "ether5", "10.255.255.1")}
for k, (y, t, ip) in ENT.items():
    a.add(a.box(CX0 + 12, y - 8, 166, 52, a.NAVY2, rx=10) + a.text(CX0 + 24, y + 12, t, 15, LIGHT, a.MONO) + a.text(CX0 + 24, y + 34, ip, 15, "#FFFFFF", a.MONO, 700))

a.add(dev(a, 48, 226, 222, 84, "Notebook", "en ether2", "laptop", sub2="WinBox a .88.1"))
a.add(dev(a, 48, 396, 222, 84, "Notebook rescate", "10.255.255.2/30", "laptop"))
a.add(linea(270, 268, 332, 265, a.LINE, 4) + linea(270, 438, 332, 437, a.LINE, 4))

# tráfico de la notebook de ether2
for t0 in (3, 14):
    viaje(a, "WinBox", [(600, 266), (CX0 - 4, 276)], t0, t0 + 5, bg=a.BLUE, size=14, hold=1.5)
en(a, marca(a, CX0 + 188, 254, ok=True), 9, 50)
for t0 in (54, 63):
    viaje(a, "WinBox · 20", [(590, 266), (CX0 - 52, 344)], t0, t0 + 5, bg=V20, size=14, hold=2)
en(a, marca(a, CX0 + 188, 254, ok=False) + a.text(CX0 + 95, 196, "llega por vlan20-cctv", 15, V20, a.SANS, 700, "middle"), 60, 100, still=1)
fijo(a, place(pill_c(a, "WinBox · 20", "#FFFFFF", V20, 14), CX0 - 52, 344))
# rescate
for t0 in (8, 34, 78, 88):
    viaje(a, "WinBox", [(620, 437), (CX0 - 4, 418)], t0, t0 + 4, bg=a.OK, size=14, hold=1)
en(a, marca(a, CX0 + 188, 390, ok=True), 10, 100, still=1)

# ---- abajo: el comando y las sesiones
BY = 496
a.add(a.box(48, BY, 1104, 104, a.INK, rx=16))
a.add(a.text(70, BY + 36, "> /interface/bridge/set bridge vlan-filtering=", 16, "#FFFFFF", a.MONO, 600))
en(a, a.text(538, BY + 36, "no", 16, LIGHT, a.MONO, 700), 0, 27)
en(a, a.text(538, BY + 36, "yes", 16, GOLD, a.MONO, 700), 27, 100, still=1)
a.add(a.text(70, BY + 78, "sesión por ether2", 15, LIGHT, a.MONO) + a.text(620, BY + 78, "sesión por ether5", 15, LIGHT, a.MONO))
for t0, t1, s, fg, bg, st in ((0, 60, "conectada", a.OK, a.OKBG, 0), (60, 100, "cortada", a.BAD, a.BADBG, 1)):
    en(a, a.pill(250, BY + 58, s, fg, bg, 14, 28), t0, t1, still=st)
en(a, a.pill(800, BY + 58, "conectada", a.OK, a.OKBG, 14, 28), 0, 100, still=1)

narr(a, [
    (0, 25, "Con vlan-filtering=no el bridge ignora la tabla: es un switch común.", a.TXT),
    (25, 50, "Desde ahora cada trama tiene VLAN: la de su etiqueta o el PVID del puerto.", a.AMB),
    (50, 75, "192.168.88.1 está en el bridge, VLAN 1; ether2 ya no es de esa VLAN.", a.BAD),
    (75, 100, "Por eso se activa al final y desde ether5 o la consola serial.", a.OK),
], y=640, still_idx=2)

escribir(a, "5-l1", "vlan-filtering=yes: la tabla manda de golpe",
         "Animación en cuatro tiempos del paso 4. El router por dentro: el bridge con ether2 y ether3 en PVID 20 y ether4 de trunk, ether5 fuera del bridge, "
         "y el CPU del router con tres puertas: el bridge en la VLAN 1 con 192.168.88.1, vlan20-cctv con 10.10.20.1 y ether5 con 10.255.255.1. "
         "A la izquierda, una notebook en ether2 con WinBox a 192.168.88.1 y la notebook de rescate en ether5 con 10.255.255.2/30. Abajo, el comando y el estado de las dos sesiones. "
         "1: con vlan-filtering=no el PVID no tiene efecto y la notebook de ether2 llega a 192.168.88.1. "
         "2: se ejecuta /interface/bridge/set bridge vlan-filtering=yes y la tabla VLAN empieza a mandar. "
         "3: lo que entra por ether2 recibe la VLAN 20 y llega al CPU por vlan20-cctv, no a la IP del bridge: la sesión por ether2 se corta. "
         "4: ether5 está fuera del bridge y la sesión de rescate sigue conectada; por eso se activa al final y desde ether5 o la consola serial.",
         [10, 35, 62, 70, 90])
