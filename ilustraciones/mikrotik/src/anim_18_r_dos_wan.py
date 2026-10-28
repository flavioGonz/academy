#!/usr/bin/env python3
"""Lección 18 (Cloud a fondo) · Resumen: con dos WAN, el aviso a la nube sale por la ruta activa y el nombre sigue a esa IP."""
from _anim_r20_31 import *

a, _ = nuevo(26, "MIKROTIK · CLOUD A FONDO · EN LA RED", "Con dos WAN, el nombre sigue a la ruta",
             ["El aviso a cloud2.mikrotik.com sale por la principal: la nube anota 203.0.113.10.",
              "Se cae el ISP A: la ruta por defecto pasa al ISP B.",
              "El aviso siguiente sale por el ISP B: la nube anota 198.51.100.40.",
              "Con TTL de 60 s, al minuto el técnico ya resuelve la IP nueva."], still=2)

dev(a, 48, 310, 240, 110, "MikroTik", "ether1 → ISP A", "ether2 → ISP B", kind="router", ssize=14)
dev(a, 420, 196, 260, 96, "ISP A · principal", "203.0.113.10", "distance=1", kind="isp", ssize=14)
dev(a, 420, 438, 260, 96, "ISP B · respaldo", "198.51.100.40", "distance=2", kind="isp", ssize=14)
dev(a, 870, 196, 282, 96, "cloud2.mikrotik.com", "UDP 15252", "anota el origen", kind="cloud", ssize=14)
dev(a, 870, 438, 282, 96, "Técnico", "resuelve el nombre", kind="pc", ssize=14)

A_WIRE = poly([(288, 345), (360, 345), (360, 244), (420, 244)], a.BLUE, 3)
B_WIRE = poly([(288, 385), (360, 385), (360, 486), (420, 486)], a.BLUE, 3)
a.add(B_WIRE)
en(a, A_WIRE, 0, 27, still=0)
en(a, poly([(288, 345), (360, 345), (360, 244), (420, 244)], a.LINE, 3, "6 6"), 27, 100, still=1)
a.add(wire(680, 244, 870, 244, a.LINE, 3, "6 6"))
a.add(poly([(680, 486), (760, 486), (760, 260), (870, 260)], a.LINE, 3, "6 6"))
a.add(wire(1011, 292, 1011, 438, a.LINE, 3, "6 6"))
en(a, mark(a, 550, 314, ok=False, r=18) + a.text(550, 352, "caído", 15, a.BAD, a.MONO, 600, "middle"), 27, 100, still=1)
flip(a, 48, 448, [(0, 30, "ruta activa: ISP A", a.OK), (30, 33, "", a.OK), (33, 100, "ruta activa: ISP B", a.OK)], size=14, still_idx=2)

def aviso(path, t0, c):
    go(a, "", path, t0, t0 + 7, hold=2, inner=pillc(a, "aviso", bg=c, size=13, h=26))

aviso([(288, 345), (360, 345), (360, 244), (420, 244), (680, 244), (860, 244)], 3, a.CYAN)
aviso([(288, 385), (360, 385), (360, 486), (420, 486), (680, 486), (760, 486), (760, 260), (860, 260)], 53, a.CYAN)

# lo que anota la nube
a.add(a.box(48, 556, 760, 40, a.INK, rx=10))
a.add(a.text(66, 582, "<serie>.sn.mynetname.net  →", 15, SKY, a.MONO))
flip(a, 360, 582, [(0, 61, "203.0.113.10", MINT), (61, 100, "198.51.100.40", MINT)], size=15, still_idx=1)
en(a, ring(a, 52, 559, 752, 34, MINT, rx=8, sw=2), 9, 24)
en(a, ring(a, 52, 559, 752, 34, MINT, rx=8, sw=2), 60, 75)
en(a, a.text(560, 582, "public-address cambió", 15, GOLD, a.SANS, 600), 62, 100, still=1)
# 4. el técnico resuelve
go(a, "", [(1011, 300), (1011, 430)], 80, 86, hold=12, inner=pillc(a, "198.51.100.40", bg=a.OK, size=13, h=26))
en(a, a.text(1030, 572, "TTL 60 s", 15, a.GREY, a.MONO, 600), 78, 100)

narr(a, [
    (0, 25, "La nube no confía en lo que dice el router: anota la IP desde la que le llega.", a.TXT),
    (25, 50, "Cuando la principal cae, la ruta de distance=2 queda activa.", a.BAD),
    (50, 75, "/ip/cloud/force-update lo manda en el acto, sin esperar.", a.TXT),
    (75, 100, "El nombre sirve para llegar al sitio por cualquiera de las dos WAN.", a.OK),
], y=636, still_idx=2)

escribir(a, "18-r1.svg", "DDNS con dos WAN",
         "Animación en cuatro tiempos con un MikroTik con dos WAN: ether1 al ISP A principal (203.0.113.10, distance=1) y ether2 al ISP B de respaldo (198.51.100.40, distance=2); "
         "a la derecha cloud2.mikrotik.com por UDP 15252 y un técnico que resuelve el nombre. Abajo, a qué IP apunta <serie>.sn.mynetname.net. "
         "1: el aviso a la nube sale por la ruta principal y la nube anota 203.0.113.10. 2: se cae el ISP A y la ruta por defecto pasa al ISP B. "
         "3: el aviso siguiente sale por el ISP B, la nube anota 198.51.100.40 y public-address cambia. 4: con TTL de 60 segundos, al minuto el técnico ya resuelve la IP nueva.",
         [8, 38, 58, 70, 94])
