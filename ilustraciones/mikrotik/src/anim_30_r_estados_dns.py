#!/usr/bin/env python3
"""Lección 30 (DNS en MikroTik) · Resumen: NOERROR, NXDOMAIN y SERVFAIL vistos en el cable, y qué te dice cada uno."""
from _anim_r20_31 import *

a, _ = nuevo(26, "MIKROTIK · DNS EN MIKROTIK · EN LA RED", "NOERROR, NXDOMAIN, SERVFAIL: quién falló",
             ["mikrotik.com: el router pregunta arriba y vuelve la dirección. NOERROR.",
              "mikrotk.com, mal escrito: arriba contestan que no existe. NXDOMAIN.",
              "Se corta el enlace: arriba nadie contesta y el router responde SERVFAIL.",
              "NXDOMAIN es el nombre; SERVFAIL, el camino hacia arriba."], still=2)

XN, XR, XU = 190, 600, 1010
head(a, XN, 180, "Notebook", "192.168.88.10", w=250)
head(a, XR, 180, "Router · resolver", "192.168.88.1 · caché", w=290, kind="router")
head(a, XU, 180, "Servidores de arriba", "1.1.1.1, 9.9.9.9", w=280, kind="isp")
for x in (XN, XR, XU):
    lifeline(a, x, 250, 470)

Q1, Q2, R2, R1 = 290, 340, 390, 440
S = [(0, 25), (25, 50), (50, 75)]
# 1. NOERROR
msg(a, XN, XR, Q1, "A? mikrotik.com", 2, 25)
en(a, a.text(XR + 14, Q1 + 26, "no está en caché", 14, a.GREY, a.SANS, 400), 5, 25)
msg(a, XR, XU, Q2, "A? mikrotik.com", 7, 25)
msg(a, XU, XR, R2, "NOERROR · dirección", 12, 25, a.OK)
msg(a, XR, XN, R1, "NOERROR · dirección", 17, 25, a.OK)
# 2. NXDOMAIN
msg(a, XN, XR, Q1, "A? mikrotk.com", 27, 50)
msg(a, XR, XU, Q2, "A? mikrotk.com", 31, 50)
msg(a, XU, XR, R2, "NXDOMAIN", 36, 50, a.AMB)
msg(a, XR, XN, R1, "NXDOMAIN", 41, 50, a.AMB)
# 3. SERVFAIL
msg(a, XN, XR, Q1, "A? ies.com.uy", 52, 75, still=1)
msg(a, XR, XU, Q2, "a servers", 56, 75, a.GREY, lost=True, still=1)
msg(a, XR, XU, R2, "a dynamic-servers", 60, 75, a.GREY, lost=True, still=1)
msg(a, XR, XN, R1, "SERVFAIL", 66, 75, a.BAD, still=1)
en(a, a.box(XU - 140, 270, 280, 150, a.BADBG, a.BAD, rx=14, sw=2) + a.text(XU, 334, "enlace caído", 17, a.BAD, a.HEAD, 600, "middle")
   + a.text(XU, 360, "nadie contesta", 15, a.TXT, a.SANS, 400, "middle"), 54, 75, still=1)
# 4. resumen
en(a, note(a, 48, 264, 540, 196, "", [""], "info"), 76, 100)
en(a, a.text(70, 300, "Lo que te dice cada respuesta", 18, a.INK, a.HEAD, 600)
   + a.text(70, 340, "NOERROR", 16, a.OK, a.MONO, 600) + a.text(200, 340, "el nombre existe y hay dirección", 15, a.TXT, a.SANS)
   + a.text(70, 378, "NXDOMAIN", 16, a.AMB, a.MONO, 600) + a.text(200, 378, "no existe: mal escrito o bloqueado", 15, a.TXT, a.SANS)
   + a.text(70, 416, "SERVFAIL", 16, a.BAD, a.MONO, 600) + a.text(200, 416, "el router no consiguió respuesta", 15, a.TXT, a.SANS)
   + a.text(200, 438, "de arriba: mirá el enlace", 15, a.TXT, a.SANS), 76, 100)

# salida de nslookup
TY = 490
flip_items = [
    (0, 25, ["> nslookup mikrotik.com 192.168.88.1", "Name:    mikrotik.com", "Address: (la dirección)"], {1: MINT, 2: MINT}),
    (25, 50, ["> nslookup mikrotk.com 192.168.88.1", "*** 192.168.88.1 can't find mikrotk.com:", "    Non-existent domain"], {1: GOLD, 2: GOLD}),
    (50, 100, ["> nslookup ies.com.uy 192.168.88.1", "*** 192.168.88.1 can't find ies.com.uy:", "    Server failed"], {1: ROSE, 2: ROSE}),
]
for i, (t0, t1, lines, cols) in enumerate(flip_items):
    en(a, term(a, 48, TY, 640, lines, size=15, lh=24, colors=cols), t0, t1, still=1 if i == 2 else 0)
a.add(a.text(716, TY + 30, "nslookup en la notebook", 15, a.GREY, a.SANS, 600))
narr(a, [
    (0, 25, "Si no está en caché ni en estáticas, el router pregunta a sus servidores.", a.TXT),
    (25, 50, "La respuesta llegó: el problema es el nombre, no la red.", a.AMB),
    (50, 75, "La notebook no puede saber qué pasó arriba: solo ve el SERVFAIL.", a.BAD),
    (75, 100, "Leer el estado te dice si mirar el nombre o el enlace.", a.TXT),
], still_idx=2)

escribir(a, "30-r1.svg", "Estados de respuesta DNS",
         "Animación en cuatro tiempos con tres líneas de vida: la notebook (192.168.88.10), el router como resolver con caché (192.168.88.1) y los servidores de arriba (1.1.1.1 y 9.9.9.9). "
         "Abajo, la salida de nslookup en la notebook. 1: la notebook pregunta por mikrotik.com, el router no lo tiene en caché, pregunta arriba y vuelve NOERROR con la dirección. "
         "2: pregunta por mikrotk.com, mal escrito; arriba contestan NXDOMAIN y nslookup dice Non-existent domain. "
         "3: con el enlace caído, el router pregunta a servers y a dynamic-servers, nadie contesta, y le responde SERVFAIL a la notebook: Server failed. "
         "4: resumen: NOERROR, el nombre existe; NXDOMAIN, no existe o está bloqueado; SERVFAIL, el router no consiguió respuesta de arriba.",
         [12, 22, 46, 70, 90])
