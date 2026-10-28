#!/usr/bin/env python3
"""Lección 4 (Input y forward) · Laboratorio paso 2: cuatro pings y qué contador passthrough suma cada uno."""
from _anim_r20_31 import *

a, _ = nuevo(24, "MIKROTIK · INPUT Y FORWARD · PASO 2", "Cuatro pings, tres contadores",
             ["Ping de la notebook a 192.168.88.1: es una IP del router, suma input.",
              "Ping a la IP de ether1: también es del router, también input.",
              "Ping a 1.1.1.1: el router solo lo reenvía, suma forward.",
              "/ping 1.1.1.1 desde la terminal: lo genera el router, suma output."], still=2)

dev(a, 48, 318, 190, 104, "Notebook", "ether2", "192.168.88.10", ssize=14)
dev(a, 962, 318, 190, 104, "Internet", "1.1.1.1", kind="isp", ssize=14)
# router
a.add(a.box(330, 186, 500, 390, a.INK, rx=18))
a.add(a.text(352, 220, "Router de banco", 19, a.WHITE, a.HEAD, 600))
a.add(a.box(480, 238, 200, 66, a.NAVY2, rx=12))
a.add(a.text(580, 268, "el propio router", 16, a.WHITE, a.SANS, 600, "middle"))
a.add(a.text(580, 290, "procesos, terminal", 14, SKY, a.MONO, 400, "middle"))
a.add(wire(238, 370, 330, 370, a.BLUE, 3))
a.add(wire(830, 370, 962, 370, a.BLUE, 3))
a.add(a.text(342, 402, "192.168.88.1", 14, SKY, a.MONO))
a.add(a.text(818, 402, "IP de ether1", 14, SKY, a.MONO, 400, "end"))
# carriles
a.add(poly([(330, 370), (400, 370), (400, 271), (480, 271)], "#2C4A6B", 3, "6 6"))
a.add(poly([(330, 370), (830, 370)], "#2C4A6B", 3, "6 6"))
a.add(poly([(680, 271), (760, 271), (760, 370), (830, 370)], "#2C4A6B", 3, "6 6"))

# contadores
ROWS = [("lab: cuenta input", [(0, 9, "0"), (9, 34, "1"), (34, 100, "2")]),
        ("lab: cuenta forward", [(0, 61, "0"), (61, 100, "1")]),
        ("lab: cuenta output", [(0, 86, "0"), (86, 100, "1")])]
a.add(a.text(352, 448, "/ip/firewall/filter/print stats", 14, SKY, a.MONO))
for i, (name, vals) in enumerate(ROWS):
    y = 462 + i * 36
    a.add(a.box(348, y, 464, 30, a.NAVY2, rx=8))
    a.add(a.text(364, y + 21, name, 15, a.WHITE, a.MONO, 600))
    for k, (t0, t1, v) in enumerate(vals):
        still = 1 if (t0 <= 62 < t1) else 0
        en(a, a.text(796, y + 21, v, 16, MINT if v != "0" else SKY, a.MONO, 600, "end"), t0, t1, still)
def hl(i, t0, t1, still=0):
    en(a, ring(a, 345, 459 + i * 36, 470, 36, MINT, rx=10, sw=2.5), t0, t1, still)
hl(0, 9, 25); hl(0, 34, 50); hl(1, 61, 75, still=1); hl(2, 86, 100)

# 1 y 2: input
go(a, "a 192.168.88.1", [(238, 340), (408, 340), (408, 250)], 2, 9, hold=10, bg=a.CYAN, size=13)
go(a, "a IP de ether1", [(238, 340), (408, 340), (408, 250)], 27, 34, hold=10, bg=a.CYAN, size=13)
en(a, a.text(580, 334, "las dos son IP del router", 15, MINT, a.SANS, 600, "middle"), 30, 50)
# 3: forward
go(a, "a 1.1.1.1", [(250, 370), (896, 370)], 52, 61, hold=10, bg=a.BLUE, size=14)
fijo(a, at(pillc(a, "a 1.1.1.1", bg=a.BLUE, size=14), 600, 370))
en(a, a.text(580, 418, "atraviesa: ni entra ni sale del router", 15, MINT, a.SANS, 600, "middle"), 58, 75, still=1)
# 4: output
go(a, "/ping", [(690, 271), (760, 271), (760, 370), (896, 370)], 79, 86, hold=8, bg=a.AMB, size=14)
en(a, a.text(580, 334, "nace en el router", 15, GOLD, a.SANS, 600, "middle"), 80, 100)

narr(a, [
    (0, 25, "passthrough suma al contador y deja seguir: no cambia nada del tráfico.", a.TXT),
    (25, 50, "input es todo lo que va a una IP del router, de la LAN o de la WAN.", a.TXT),
    (50, 75, "forward es lo que pasa a través, hacia otra red.", a.OK),
    (75, 100, "output es lo que genera el propio router.", a.AMB),
], still_idx=2)

escribir(a, "4-l1.svg", "Input, forward y output con contadores",
         "Animación en cuatro tiempos con la notebook en ether2 (192.168.88.10), el router de banco y 1.1.1.1 en internet. Adentro del router, el propio router y "
         "tres contadores passthrough: lab: cuenta input, lab: cuenta forward y lab: cuenta output. 1: el ping de la notebook a 192.168.88.1 va al router y el contador de input pasa a 1. "
         "2: el ping a la IP de ether1 también es para el router y input pasa a 2. 3: el ping a 1.1.1.1 atraviesa el router y suma en forward. "
         "4: el /ping 1.1.1.1 desde la terminal del router lo genera el propio router y suma en output.",
         [10, 38, 62, 70, 92])
