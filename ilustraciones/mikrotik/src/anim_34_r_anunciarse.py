#!/usr/bin/env python3
"""Lección 34 (Descubrir vecinos), Resumen: anunciarse es mostrarse. Sin la lista propia el router anuncia por todos
los puertos, también hacia la red ajena de ether1, que ve su identidad, versión e IP. Con discover-interface-list=descubrir
solo habla y escucha por ether2 y ether3; la entrada de afuera vence y el switch sigue en /ip/neighbor."""
from _anims_10_19 import Anim, en, ventanas, fijo, dev, viaje, linea, narr, escribir, pill_c, place, marca, LIGHT, GOLD, MINT, CORAL, GHOST

a = Anim(T=28, kicker="MIKROTIK · VECINOS · EN LA RED", title="Anunciarse es mostrarse, también hacia afuera")
a.steps([
    "Lista static: el router se anuncia por todos los puertos.",
    "Del lado de ether1, la red ajena ve nombre, versión e IP.",
    "Lista descubrir: solo ether2 y ether3 se anuncian.",
    "Por ether1 ni habla ni escucha; adentro, el switch sigue.",
], still=2)

# ---- router
RX, RY, RW, RH = 420, 184, 336, 286
a.add(a.box(RX, RY, RW, RH, a.INK, rx=18) + a.text(RX + 20, RY + 34, "hAP del local", 19, "#FFFFFF", a.SANS, 600)
      + a.text(RX + 20, RY + 58, "identity hap-local", 15, LIGHT, a.MONO))
PORTS = {"ether1": (RX + 12, 336, "L"), "ether2": (RX + RW - 108, 232, "R"), "ether3": (RX + RW - 108, 320, "R"), "ether5": (RX + RW - 108, 408, "R")}
for p, (x, y, side) in PORTS.items():
    a.add(a.box(x, y - 16, 96, 32, a.NAVY2, "#4E7396", rx=8, sw=1.5) + a.text(x + 48, y + 6, p, 15, "#FFFFFF", a.MONO, 600, "middle"))
en(a, a.text(RX + 20, RY + 262, "discover-interface-list=static", 15, GOLD, a.MONO, 600), 0, 50)
en(a, a.text(RX + 20, RY + 262, "discover-interface-list=descubrir", 15, MINT, a.MONO, 600), 50, 100, still=1)

a.add(dev(a, 48, 296, 252, 80, "Red ajena", "proveedor o shopping", "globe"))
a.add(dev(a, 852, 192, 300, 80, "Notebook", "WinBox · ether2", "laptop"))
a.add(dev(a, 852, 280, 300, 80, "Switch del rack", "sw-rack · LLDP", "server"))
a.add(dev(a, 852, 368, 300, 80, "Cámara", "ether5", "camera"))
a.add(linea(300, 336, RX + 12, 336, a.LINE, 4))
for p, yy in (("ether2", 232), ("ether3", 320), ("ether5", 408)):
    a.add(linea(RX + RW - 12, yy, 852, yy, a.LINE, 4))
en(a, linea(300, 336, RX + 12, 336, a.BAD, 4, "4 9"), 50, 100, still=1)
en(a, linea(RX + RW - 12, 408, 852, 408, "#C2D4E6", 4, "4 9"), 50, 100, still=1)

# anuncios del router (cada 30 s en la realidad)
OUTL = [(RX + 2, 336), (330, 336)]
OUTR = {"ether2": [(RX + RW + 6, 232), (820, 232)], "ether3": [(RX + RW + 6, 320), (820, 320)], "ether5": [(RX + RW + 6, 408), (820, 408)]}
for t0 in (3, 28):
    viaje(a, "anuncio", OUTL, t0, t0 + 5, bg=a.CYAN, size=14, hold=0.5)
    for p in OUTR:
        viaje(a, "anuncio", OUTR[p], t0, t0 + 5, bg=a.CYAN, size=14, hold=0.5)
for t0 in (53, 78):
    for p in ("ether2", "ether3"):
        viaje(a, "anuncio", OUTR[p], t0, t0 + 5, bg=a.CYAN, size=14, hold=0.5)
# anuncios que llegan del switch y del proveedor
for t0 in (14, 40, 64, 88):
    viaje(a, "LLDP", [(820, 320), (RX + RW + 6, 320)], t0, t0 + 4, bg=a.NAVY2, size=14, hold=0.4)
for t0 in (16, 40):
    viaje(a, "LLDP", [(330, 336), (RX + 2, 336)], t0, t0 + 4, bg=a.NAVY2, size=14, hold=0.4)
viaje(a, "LLDP", [(300, 336), (352, 336)], 86, 89, bg=a.NAVY2, size=14, hold=3)
en(a, marca(a, RX - 12, 336, ok=False), 89, 100)
fijo(a, place(pill_c(a, "anuncio", "#FFFFFF", a.CYAN, 14), 800, 232) + place(pill_c(a, "anuncio", "#FFFFFF", a.CYAN, 14), 800, 320))

# ---- lo que ve cada uno
BY = 490
a.add(a.box(48, BY, 540, 114, a.WHITE, a.LINE, rx=16) + a.text(68, BY + 30, "Lo que ve la red ajena (Neighbors)", 16, a.INK, a.HEAD, 600))
fila_af = a.text(68, BY + 64, "hap-local · MikroTik · 7.x · 203.0.113.10", 16, a.INK, a.MONO, 600)
en(a, fila_af + a.pill(68, BY + 74, "te ve", a.BAD, a.BADBG, 14, 26), 8, 50)
en(a, a.text(68, BY + 64, "hap-local · MikroTik · 7.x · 203.0.113.10", 16, a.GREY, a.MONO) + a.pill(68, BY + 74, "todavía figura: vence sola", a.AMB, a.AMBBG, 14, 26), 50, 76, still=1)
en(a, a.text(68, BY + 64, "nada del router", 16, a.OK, a.MONO, 600) + a.pill(68, BY + 74, "ya no figura", a.OK, a.OKBG, 14, 26), 76, 100)
en(a, a.text(68, BY + 64, "(todavía nada)", 16, a.GREY, a.MONO), 0, 8)

a.add(a.box(612, BY, 540, 114, a.WHITE, a.LINE, rx=16) + a.text(632, BY + 30, "/ip/neighbor del router", 16, a.INK, a.HEAD, 600))
en(a, a.text(632, BY + 64, "ether3,bridge  sw-rack  lldp", 16, a.INK, a.MONO, 600), 18, 100, still=1)
en(a, a.text(632, BY + 92, "ether1  router del proveedor  lldp", 16, a.BAD, a.MONO, 600), 20, 76, still=1)
en(a, a.text(632, BY + 92, "ether1: ya no escucha", 16, a.GREY, a.MONO), 76, 100)

narr(a, [
    (0, 25, "Cada 30 s sale un anuncio por cada interfaz de la lista: sin configuración por defecto, entra ether1.", a.TXT),
    (25, 50, "Nombre, modelo, versión e IP: lo justo para elegir a quién atacar.", a.BAD),
    (50, 75, "Los puertos van sueltos en la lista; con el bridge entrarían todos sus puertos.", a.OK),
    (75, 100, "Sacar un puerto de la lista corta el anuncio y la escucha en ese puerto.", a.AMB),
], y=640, still_idx=2)

escribir(a, "34-r1", "Anunciarse es mostrarse",
         "Animación en cuatro tiempos. En el centro el hAP del local, identity hap-local, con ether1 hacia una red ajena del proveedor o del shopping, ether2 a la notebook con WinBox, "
         "ether3 al switch del rack, que habla LLDP, y ether5 a una cámara. Abajo, lo que ve la red ajena en Neighbors y la tabla /ip/neighbor del router. "
         "1: con discover-interface-list=static el router manda anuncios por todos los puertos, también por ether1, y escucha los que llegan: el del switch y el del router del proveedor. "
         "2: la red ajena ve hap-local, MikroTik, la versión y la IP 203.0.113.10; el router ve al switch en ether3,bridge y al router del proveedor en ether1. "
         "3: con discover-interface-list=descubrir, que tiene solo ether2 y ether3, los anuncios salen solo por esos dos; afuera, la entrada todavía figura hasta que vence sola. "
         "4: por ether1 el router ya no habla ni escucha: el anuncio del proveedor se ignora y la red ajena deja de verlo; adentro, el switch sigue en /ip/neighbor. La versión 7.x es un ejemplo.",
         [6, 32, 44, 58, 90, 96])
