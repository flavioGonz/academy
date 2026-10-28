#!/usr/bin/env python3
"""Lección 39 (Dos WAN: IP fija + DHCP), Laboratorio paso 5: /ip/cloud/force-update antes y durante el failover.
El router le pregunta a cloud2.mikrotik.com por UDP 15252 y la nube contesta con la dirección desde la que recibió
el pedido: public-address y el nombre .sn.mynetname.net siguen a la WAN por la que sale el router."""
from _anims_10_19 import Anim, en, ventanas, fijo, dev, viaje, linea, narr, escribir, pill_c, place, marca, LIGHT, GOLD, MINT, CORAL, GHOST

a = Anim(T=24, kicker="MIKROTIK · LABORATORIO · PASO 5", title="La nube contesta con la IP desde la que le hablaste")
a.steps([
    "force-update con la fija activa: el pedido sale por ether1.",
    "La nube contesta: te vi desde 203.0.113.10.",
    "Corte simulado: el router sale por el 4G y pregunta de nuevo.",
    "public-address cambia y el nombre la sigue (TTL 60 s).",
], still=3)

a.add(a.box(48, 196, 230, 112, a.INK, a.INK, rx=16) + a.text(68, 232, "Router", 19, "#FFFFFF", a.SANS, 600)
      + a.text(68, 256, "/ip/cloud", 15, LIGHT, a.MONO) + a.text(68, 278, "force-update", 15, LIGHT, a.MONO))
a.add(dev(a, 380, 178, 300, 80, "ether1 · IP fija", "203.0.113.10", "server"))
a.add(dev(a, 380, 290, 300, 80, "ether2 · 4G", "sale como 198.51.100.77", "wifi"))
a.add(dev(a, 900, 226, 252, 96, "cloud2.mikrotik.com", "UDP 15252", "cloud"))
a.add(linea(278, 232, 380, 218, a.LINE, 4) + linea(278, 274, 380, 330, a.LINE, 4))
a.add(linea(680, 218, 900, 260, a.LINE, 4) + linea(680, 330, 900, 290, a.LINE, 4))
en(a, linea(278, 232, 380, 218, a.OK, 4) + linea(680, 218, 900, 260, a.OK, 4), 0, 50)
en(a, linea(278, 274, 380, 330, a.AMB, 4) + linea(680, 330, 900, 290, a.AMB, 4), 50, 100, still=1)
en(a, a.text(800, 206, "rutas de la fija inactivas", 15, a.GREY, a.MONO, 600, "middle"), 50, 100, still=1)

UP1 = [(700, 222), (860, 252)]
UP2 = [(700, 326), (860, 296)]
viaje(a, "¿qué IP ves?", UP1, 4, 12, bg=a.BLUE, size=14, hold=1)
viaje(a, "te vi: 203.0.113.10", [(860, 252), (790, 239)], 27, 33, bg=a.OK, size=14, hold=8)
viaje(a, "¿qué IP ves?", UP2, 54, 62, bg=a.BLUE, size=14, hold=1)
viaje(a, "te vi: 198.51.100.77", [(860, 296), (790, 309)], 77, 83, bg=a.AMB, size=14, hold=10)
fijo(a, place(pill_c(a, "te vi: 198.51.100.77", "#FFFFFF", a.AMB, 14), 790, 309))

# ---- terminal
TX, TY, TW = 48, 430, 660
a.add(a.box(TX, TY, TW, 170, a.INK, rx=16))
a.add(a.text(TX + 22, TY + 34, "> /ip/cloud/force-update", 15, LIGHT, a.MONO))
a.add(a.text(TX + 22, TY + 60, "> /ip/cloud/print", 15, LIGHT, a.MONO))
a.add(a.text(TX + 22, TY + 98, "public-address:", 16, LIGHT, a.MONO))
a.add(a.text(TX + 22, TY + 130, "dns-name:", 16, LIGHT, a.MONO))
a.add(a.text(TX + 196, TY + 130, "<serie>.sn.mynetname.net", 16, "#FFFFFF", a.MONO, 600))
en(a, a.text(TX + 196, TY + 98, "203.0.113.10", 17, MINT, a.MONO, 700), 36, 86)
en(a, a.text(TX + 196, TY + 98, "198.51.100.77", 17, GOLD, a.MONO, 700), 86, 100, still=1)
en(a, a.text(TX + 196, TY + 98, "…", 17, LIGHT, a.MONO, 700), 0, 36)

# ---- DNS
DX, DW = 736, 416
a.add(a.box(DX, TY, DW, 170, a.WHITE, a.LINE, rx=16) + a.text(DX + 22, TY + 34, "El nombre en el DNS", 16, a.INK, a.HEAD, 600))
a.add(a.text(DX + 22, TY + 70, "<serie>.sn.mynetname.net", 16, a.INK, a.MONO, 600))
en(a, a.pill(DX + 22, TY + 88, "A 203.0.113.10", a.OK, a.OKBG, 15, 30), 38, 88)
en(a, a.pill(DX + 22, TY + 88, "A 198.51.100.77", a.AMB, a.AMBBG, 15, 30), 88, 100, still=1)
a.add(a.text(DX + 22, TY + 148, "TTL 60 s: los clientes lo vuelven a pedir pronto", 15, a.GREY, a.SANS))

narr(a, [
    (0, 25, "El pedido sigue la ruta activa hacia cloud2.mikrotik.com, como cualquier paquete del router.", a.TXT),
    (25, 50, "La nube no adivina: anota la dirección de origen que le llegó y te la devuelve.", a.OK),
    (50, 75, "Con las recursivas de la fija caídas, el mismo pedido sale por ether2.", a.AMB),
    (75, 100, "Esa IP es del 4G: sirve para salir, no para que la central entre.", a.AMB),
], y=640, still_idx=3)

escribir(a, "39-l1", "La nube contesta con la IP desde la que le hablaste",
         "Animación en cuatro tiempos del paso 5. El router con /ip/cloud, sus dos salidas, ether1 con la IP fija 203.0.113.10 y ether2 por el 4G, "
         "y el servidor cloud2.mikrotik.com, al que el router le pregunta por UDP 15252. Abajo, la salida de /ip/cloud/print y el nombre <serie>.sn.mynetname.net en el DNS. "
         "1: con la fija activa, /ip/cloud/force-update manda el pedido por ether1. "
         "2: la nube contesta con la dirección desde la que lo recibió, 203.0.113.10: public-address queda en 203.0.113.10 y el nombre apunta ahí. "
         "3: con el corte simulado las recursivas de la fija caen y el mismo pedido sale por ether2, por el 4G. "
         "4: la nube lo ve llegar desde 198.51.100.77, una IP de ejemplo del 4G; public-address cambia y el nombre la sigue con TTL de 60 segundos. "
         "Esa IP sirve para salir, no para que la central de monitoreo entre.",
         [8, 33, 58, 82, 95])
