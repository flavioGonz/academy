#!/usr/bin/env python3
"""Lección 36, teoría "Cómo funciona": cuándo pregunta la regla por la lista de entrada y por la de salida, y qué no ve."""
from _anim_mt2739 import escribir, Anim, SITE, PREV, en, ventanas, fijo, paquete, nodo, marca, narr, pill_c, LIGHT, GOLD, MINT

a = Anim(T=28, kicker="MIKROTIK · ZONAS", title="Zonas: la regla pregunta por la entrada y por la salida")
a.steps([
    "El NVR manda NTP a internet: entra por ether3.",
    "Decisión de ruteo: recién ahora se sabe la salida, ether1.",
    "En forward, la regla pregunta las dos listas: pasa.",
    "Para el router mismo (input) no hay salida: solo la entrada.",
    "Dos cámaras de la misma red se hablan sin pasar por el router.",
], still=2)

# ---- listas
LI = [("CCTV", "ether3"), ("SISTEMAS", "include=CCTV,ACCESOS"), ("WAN", "ether1")]
LX = [48, 336, 852]
LW = [260, 488, 300]
for (n, s), x, w in zip(LI, LX, LW):
    a.add(a.box(x, 170, w, 54, a.WHITE, a.LINE, rx=14))
    a.add(a.text(x + 18, 203, n, 17, a.BLUE, a.MONO, 600))
    a.add(a.text(x + 18 + len(n) * 11 + 18, 203, s, 15, a.TXT, a.MONO))
def lhl(i, wins, still=0):
    ventanas(a, f'<rect x="{LX[i] - 2}" y="168" width="{LW[i] + 4}" height="58" rx="15" fill="none" stroke="{a.CYAN}" stroke-width="3"/>', wins, still)
lhl(0, [(2, 20), (61, 80)])
lhl(1, [(4, 20), (41, 60)], still=1)
lhl(2, [(22, 40), (41, 60)], still=1)

# ---- camino del paquete
BY, BH = 262, 92
BOX = [("Entrada", 48, 250), ("Decisión de ruteo", 330, 250), ("chain=forward", 612, 250), ("Salida", 894, 258)]
for n, x, w in BOX:
    a.add(a.box(x, BY, w, BH, a.WHITE, a.LINE, rx=14))
    a.add(a.text(x + 18, BY + 32, n, 18, a.INK, a.HEAD, 600))
for x in (298, 580, 862):
    a.add(a.arrow(f"M{x + 2} {BY + BH / 2} H{x + 28}", a.GREY, 3))
a.add(a.text(66, BY + 62, "in-interface=ether3", 15, a.TXT, a.MONO))
a.add(a.text(348, BY + 62, "elige por dónde sale", 15, a.TXT, a.MONO))
a.add(a.text(630, BY + 62, "ve entrada y salida", 15, a.TXT, a.MONO))
en(a, a.text(912, BY + 62, "out-interface: ?", 15, a.GREY, a.MONO), 0, 23)
en(a, a.text(912, BY + 62, "out-interface=ether1", 15, a.INK, a.MONO, 600), 23, 60, still=1)
en(a, a.text(912, BY + 62, "out-interface: ?", 15, a.GREY, a.MONO), 60, 100)
en(a, a.text(66, BY + 82, "en CCTV y SISTEMAS", 15, a.BLUE, a.MONO, 600), 4, 60, still=1)
def bhl(i, wins, color=None, still=0):
    n, x, w = BOX[i]
    ventanas(a, f'<rect x="{x - 2}" y="{BY - 2}" width="{w + 4}" height="{BH + 4}" rx="15" fill="none" stroke="{color or a.CYAN}" stroke-width="3"/>', wins, still)
bhl(0, [(1, 20), (61, 70)])
bhl(1, [(21, 40), (66, 74)])
bhl(3, [(23, 40)])
bhl(2, [(41, 60)], a.OK, still=1)

# input
IX, IY = 330, 392
a.add(a.box(IX, IY, 250, 80, a.INK, rx=14))
a.add(a.text(IX + 18, IY + 32, "chain=input", 18, "#FFFFFF", a.HEAD, 600))
a.add(a.text(IX + 18, IY + 58, "para el router: no sale", 15, LIGHT, a.MONO))
a.add(a.arrow(f"M455 {BY + BH + 2} V{IY - 4}", a.GREY, 3, "5 5"))
ventanas(a, f'<rect x="{IX - 3}" y="{IY - 3}" width="256" height="86" rx="16" fill="none" stroke="{a.OK}" stroke-width="3"/>', [(72, 80)])

LANE = BY - 18
paquete(a, "NTP · udp 123", [(1, 173, LANE), (19, 173, LANE), (24, 455, LANE), (39, 455, LANE), (43, 737, LANE), (55, 737, LANE), (58, 1023, LANE), (59.5, 1023, LANE)], 1, 59.5)
paquete(a, "DNS al router · :53", [(61, 173, LANE), (66, 455, LANE), (70, 455, IY - 22), (79.5, 455, IY - 22)], 61, 79.5, bg=a.BLUE)
en(a, marca(a, 834, BY + 26, ok=True), 45, 60, still=1)

# ---- la regla
RX, RY, RW, RH = 612, 392, 540, 208
a.add(a.box(RX, RY, RW, RH, a.INK, rx=16))
a.add(a.text(RX + 22, RY + 32, "la regla", 15, LIGHT, a.MONO, 400, extra='letter-spacing="1.5"'))
def lines(t0, t1, ls, still=0):
    g = "".join(a.text(RX + 22, RY + 66 + i * 28, s, 16, c, a.MONO, 600 if c != LIGHT else 400) for i, (s, c) in enumerate(ls))
    en(a, g, t0, t1, still)
lines(0, 20, [("¿entró por una interfaz", "#FFFFFF"), ("de SISTEMAS?", "#FFFFFF"), ("ether3 está en CCTV,", LIGHT), ("y CCTV está incluida: sí", MINT)])
lines(20, 40, [("out-interface-list pregunta", "#FFFFFF"), ("por la salida, que se conoce", "#FFFFFF"), ("después del ruteo:", LIGHT), ("ether1, en WAN", MINT)])
lines(40, 60, [("chain=forward", "#FFFFFF"), ("in-interface-list=SISTEMAS", MINT), ("out-interface-list=WAN", MINT), ("protocol=udp dst-port=123", LIGHT), ("action=accept", MINT)], still=1)
lines(60, 80, [("chain=input", "#FFFFFF"), ("in-interface-list=CCTV", MINT), ("protocol=udp dst-port=53", LIGHT), ("action=accept", MINT), ("en input no hay salida", GOLD)])
lines(80, 100, [("ninguna regla lo ve:", "#FFB4A3"), ("la zona separa redes,", "#FFFFFF"), ("no equipos", "#FFFFFF"), ("VLAN primero, zonas después", GOLD)])

# ---- dos cámaras en el mismo bridge
CY = 512
a.add(a.box(48, 496, 540, 104, a.WHITE, a.LINE, rx=16))
a.add(a.text(66, 520, "misma red, mismo bridge", 15, a.GREY, a.MONO))
for x, n in ((66, "cam1 .20.51"), (418, "cam2 .20.52")):
    a.add(a.box(x, 538, 152, 48, a.SLATE, rx=12) + a.text(x + 76, 568, n, 15, a.INK, a.MONO, 600, "middle"))
a.add(f'<line x1="218" y1="562" x2="418" y2="562" stroke="{a.LINE}" stroke-width="3"/>')
a.add(a.box(268, 546, 100, 32, a.WHITE, a.LINE, rx=10) + a.text(318, 567, "switch", 15, a.TXT, a.MONO, 400, "middle"))
paquete(a, "video", [(82, 250, 530), (90, 390, 530), (92, 390, 530), (99, 250, 530)], 82, 99.5, bg=a.AMB)
ventanas(a, f'<rect x="46" y="494" width="544" height="108" rx="17" fill="none" stroke="{a.AMB}" stroke-width="3"/>', [(81, 100)])

narr(a, [
    (0, 20, "in-interface-list pregunta si la interfaz de entrada está en la lista.", a.TXT),
    (20, 40, "Por eso out-interface-list tiene sentido en forward y no en input.", a.TXT),
    (40, 60, "Un casillero de la matriz: de SISTEMAS a WAN, solo NTP.", a.OK),
    (60, 80, "En input se escribe qué servicios del router ve cada zona.", a.BLUE),
    (80, 100, "Para separar equipos, primero cada sistema en su VLAN.", a.AMB),
], y=636, still_idx=2)

escribir(a, f"{SITE}/36-t1.svg", "Zonas: entrada, salida y lo que no se ve",
         "Animación en cinco tiempos. Listas: CCTV con ether3, SISTEMAS con include de CCTV y ACCESOS, WAN con ether1. "
         "1: el NVR manda NTP a internet y el paquete entra por ether3, que está en CCTV y, por include, en SISTEMAS. "
         "2: en la decisión de ruteo se conoce la salida, ether1, que está en WAN; antes no se podía preguntar por la lista de salida. "
         "3: en forward la regla in-interface-list=SISTEMAS out-interface-list=WAN, udp 123, accept, coincide y el paquete pasa. "
         "4: un paquete para el router mismo va a input, donde no hay interfaz de salida; la regla solo usa in-interface-list=CCTV, udp 53. "
         "5: dos cámaras de la misma red del bridge se hablan por el switch sin pasar por el router y ninguna regla las ve: la zona separa redes, no equipos.",
         [10, 32, 52, 76, 92], f"{PREV}/_t36")
