#!/usr/bin/env python3
"""Lección 31 (DNS transparente) · Laboratorio paso 5: nslookup prueba-dns.lan 8.8.8.8 antes y después del redirect, con el contador de la regla."""
from _anim_r20_31 import *

a, _ = nuevo(26, "MIKROTIK · DNS TRANSPARENTE · PASO 5", "Le preguntás a Google y te contesta el router",
             ["Antes de las reglas: 8.8.8.8 no conoce prueba-dns.lan. NXDOMAIN.",
              "Con las reglas, la consulta a 8.8.8.8:53 cae en el redirect: no sale.",
              "El resolver tiene la estática y contesta 192.168.88.77, con origen 8.8.8.8.",
              "nslookup muestra 192.168.88.77 y sube el contador de la regla udp."], still=3)

XN, XR, XG = 190, 600, 1010
head(a, XN, 178, "Notebook", "ether2 · 192.168.88.254", w=270)
head(a, XR, 178, "Router", "redirect + resolver", w=270, kind="router")
head(a, XG, 178, "8.8.8.8", "DNS de Google", w=250, kind="isp")
for x in (XN, XR, XG):
    lifeline(a, x, 248, 440)

# 1. antes
msg(a, XN, XG, 288, "A? prueba-dns.lan → 8.8.8.8:53", 3, 25, sub="pasa por el router sin cambios", subcolor=a.GREY)
msg(a, XG, XN, 350, "NXDOMAIN", 13, 25, a.AMB)
# 2. redirect
msg(a, XN, XR, 288, "A? prueba-dns.lan → 8.8.8.8:53", 28, 75)
en(a, a.box(XR - 120, 308, 240, 52, a.WHITE, a.OK, rx=12, sw=2) + a.text(XR, 332, "dstnat: redirect", 15, a.OK, a.MONO, 600, "middle")
   + a.text(XR, 351, "destino → el router :53", 14, a.TXT, a.MONO, 400, "middle"), 33, 100, still=1)
en(a, mark(a, XR + (XG - XR) * 0.5, 288, ok=False, r=14) + a.text(XR + (XG - XR) * 0.5, 322, "no sale a internet", 14, a.BAD, a.SANS, 600, "middle"), 36, 75)
# 3. respuesta del resolver
en(a, a.text(XR + 16, 388, "estática prueba-dns.lan → 192.168.88.77", 14, a.INK, a.MONO, 600), 52, 100, still=1)
msg(a, XR, XN, 410, "192.168.88.77 · src 8.8.8.8", 56, 100, a.OK, still=1)
# salida y contador
TY = 470
en(a, term(a, 48, TY, 560, ["> nslookup prueba-dns.lan 8.8.8.8", "*** can't find prueba-dns.lan:", "    Non-existent domain"], size=15, colors={1: GOLD, 2: GOLD}), 0, 25)
en(a, term(a, 48, TY, 560, ["> nslookup prueba-dns.lan 8.8.8.8", "(esperando…)"], size=15, colors={1: SKY}), 25, 76)
en(a, term(a, 48, TY, 560, ["> nslookup prueba-dns.lan 8.8.8.8", "Name:    prueba-dns.lan", "Address:  192.168.88.77"], size=15, colors={1: MINT, 2: MINT}), 76, 100, still=1)
a.add(a.box(632, TY, 520, 118, a.INK, rx=12))
a.add(a.text(650, TY + 28, "/ip/firewall/nat/print stats", 14, SKY, a.MONO))
a.add(a.text(650, TY + 62, "DNS transparente udp", 15, a.WHITE, a.MONO, 600))
a.add(a.text(650, TY + 94, "DNS transparente tcp", 15, a.WHITE, a.MONO, 600))
flip(a, 1132, TY + 62, [(0, 30, "0", SKY), (30, 100, "1", MINT)], size=16, anchor="end", still_idx=1)
a.add(a.text(1132, TY + 94, "0", 16, SKY, a.MONO, 600, "end"))
en(a, ring(a, 640, TY + 40, 504, 34, MINT, rx=8, sw=2.5), 78, 100, still=1)

narr(a, [
    (0, 25, "Google no puede conocer un nombre que solo existe en tu router.", a.AMB),
    (25, 50, "La regla agarra la consulta en dstnat, antes de que salga por la WAN.", a.OK),
    (50, 75, "A la vuelta, el router deshace el cambio: el origen vuelve a ser 8.8.8.8.", a.TXT),
    (75, 100, "Si aparece 192.168.88.77, contestó el router aunque preguntaste a Google.", a.OK),
], still_idx=3)

escribir(a, "31-l1.svg", "Prueba del DNS transparente",
         "Animación en cuatro tiempos con la notebook en ether2 (192.168.88.254), el router con el redirect y su resolver, y 8.8.8.8. Abajo, la salida de nslookup y los contadores "
         "de las reglas DNS transparente udp y tcp. 1: antes de las reglas, la consulta por prueba-dns.lan va a 8.8.8.8 y Google contesta NXDOMAIN. "
         "2: con las reglas, la misma consulta a 8.8.8.8:53 cae en el redirect del router, que cambia el destino por el propio router y no la deja salir a internet; el contador udp pasa a 1. "
         "3: el resolver tiene la estática y contesta 192.168.88.77; a la vuelta el origen vuelve a ser 8.8.8.8. "
         "4: nslookup muestra prueba-dns.lan con 192.168.88.77: contestó el router aunque la notebook le preguntó a Google.",
         [12, 40, 64, 70, 92])
