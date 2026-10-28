#!/usr/bin/env python3
"""Lección 32 (Bloqueo por DNS) · Resumen: la adlist bloquea el nombre exacto; la estática NXDOMAIN con match-subdomain cubre también lo de abajo."""
from _anim_r20_31 import *

a, _ = nuevo(26, "MIKROTIK · BLOQUEO POR DNS · EN LA RED", "Adlist: el nombre exacto. NXDOMAIN: todo lo de abajo",
             ["example.net está en la adlist: el router contesta 0.0.0.0 sin preguntar arriba.",
              "www.example.net no está en la lista: pregunta arriba y vuelve la dirección real.",
              "example.com tiene una estática NXDOMAIN: el router dice que no existe.",
              "Con match-subdomain=yes, www.example.com también da NXDOMAIN."], still=1)

XN, XR, XU = 180, 590, 1010
head(a, XN, 178, "Notebook", "usa el DNS del router", w=260)
head(a, XR, 178, "Router", "adlist + estáticas", w=260, kind="router")
head(a, XU, 178, "Servidores de arriba", "servers", w=270, kind="isp")
for x in (XN, XR, XU):
    lifeline(a, x, 248, 452)

def res(t0, t1, txt, col, bg, still=0):
    en(a, a.pill(XN, 420, txt, col, bg, 14, 28, anchor="middle"), t0, t1, still)

# 1. adlist
msg(a, XN, XR, 290, "A? example.net", 2, 25)
en(a, a.text(XR - 14, 324, "está en la adlist", 14, a.BAD, a.MONO, 600, "end"), 6, 25)
msg(a, XR, XN, 360, "0.0.0.0 · TTL 2 s", 9, 25, a.BAD)
res(13, 25, "el navegador no llega a ningún lado", a.BAD, a.BADBG)
# 2. www no está
msg(a, XN, XR, 290, "A? www.example.net", 27, 50, still=1)
en(a, a.text(XR - 14, 324, "no está: solo el nombre exacto", 14, a.AMB, a.MONO, 600, "end"), 31, 50, still=1)
msg(a, XR, XU, 340, "A? www.example.net", 33, 50, still=1)
msg(a, XU, XR, 380, "dirección real", 38, 50, a.OK, still=1)
msg(a, XR, XN, 380, "dirección real", 43, 50, a.OK, still=1)
res(45, 50, "abre: no está bloqueado", a.AMB, a.AMBBG, still=1)
# 3. NXDOMAIN example.com
msg(a, XN, XR, 290, "A? example.com", 52, 75)
en(a, a.text(XR - 14, 324, "estática type=NXDOMAIN", 14, a.BAD, a.MONO, 600, "end"), 56, 75)
msg(a, XR, XN, 360, "NXDOMAIN", 59, 75, a.BAD)
res(63, 75, "no existe", a.BAD, a.BADBG)
# 4. www.example.com
msg(a, XN, XR, 290, "A? www.example.com", 77, 100)
en(a, a.text(XR - 14, 324, "match-subdomain=yes: también", 14, a.BAD, a.MONO, 600, "end"), 81, 100)
msg(a, XR, XN, 360, "NXDOMAIN", 84, 100, a.BAD)
res(88, 100, "no existe", a.BAD, a.BADBG)

# configuración
a.add(a.box(48, 478, 1104, 112, a.INK, rx=12))
a.add(a.text(66, 506, "/ip/dns/adlist", 14, SKY, a.MONO))
a.add(a.text(300, 506, "file=adlist-prueba.txt  →  example.net, ads.example.net", 15, a.WHITE, a.MONO, 600))
a.add(a.text(66, 540, "/ip/dns/static", 14, SKY, a.MONO))
a.add(a.text(300, 540, "name=example.com type=NXDOMAIN match-subdomain=yes", 15, a.WHITE, a.MONO, 600))
a.add(a.text(66, 574, "cada nombre de la adlist ocupa unos 75 bytes de caché: primero se sube cache-size", 14, SKY, a.SANS))
en(a, ring(a, 56, 486, 1088, 30, MINT, rx=8, sw=2), 0, 50, still=1)
en(a, ring(a, 56, 520, 1088, 30, MINT, rx=8, sw=2), 50, 100)

narr(a, [
    (0, 25, "El bloqueo vive en la caché DNS del router: la consulta no sale.", a.TXT),
    (25, 50, "La adlist no tiene comodines: cada nombre se bloquea por separado.", a.AMB),
    (50, 75, "Para un sitio puntual, una estática NXDOMAIN.", a.TXT),
    (75, 100, "match-subdomain=yes cubre el dominio y todo lo que está debajo.", a.OK),
], still_idx=1)

escribir(a, "32-r1.svg", "Bloqueo por nombre exacto o por dominio",
         "Animación en cuatro tiempos con la notebook que usa el DNS del router, el router con una adlist y una estática, y los servidores de arriba. Abajo, la configuración: "
         "la adlist del archivo adlist-prueba.txt con example.net y ads.example.net, y la estática example.com type=NXDOMAIN match-subdomain=yes. "
         "1: la notebook pregunta por example.net, que está en la adlist; el router contesta 0.0.0.0 con TTL de 2 segundos sin preguntar arriba, y el navegador no llega a ningún lado. "
         "2: pregunta por www.example.net, que no está en la lista; el router pregunta arriba y vuelve la dirección real: la adlist bloquea solo el nombre exacto. "
         "3: pregunta por example.com y el router contesta NXDOMAIN por la estática. 4: con match-subdomain=yes, www.example.com también da NXDOMAIN.",
         [12, 40, 48, 66, 92])
