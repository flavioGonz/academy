#!/usr/bin/env python3
"""Lección 30 (DNS en MikroTik) · Laboratorio paso 3: la consulta desde la WAN muere en input; sin esa regla el router sería un resolver abierto y serviría para amplificar."""
from _anim_r20_31 import *

a, _ = nuevo(26, "MIKROTIK · DNS EN MIKROTIK · PASO 3", "El 53 de la WAN tiene que dar timeout",
             ["Desde la red de ether1, nslookup le pregunta a la IP WAN del router.",
              "input la descarta con drop all not coming from LAN: timeout.",
              "Si nada lo frenara, el router contestaría a cualquiera: resolver abierto.",
              "Con el origen falso de una víctima, la respuesta grande le cae a ella."], still=1)

XA, XR, XV = 190, 610, 1010
en(a, dev(a, XA - 130, 180, 260, 70, "Notebook en ether1", "la red de tu casa", tsize=17, ssize=14, add=False), 0, 50, still=1)
en(a, dev(a, XA - 130, 180, 260, 70, "Atacante", "en internet", kind="bad", tsize=17, ssize=14, add=False), 50, 100)
head(a, XR, 180, "Router", "WAN 203.0.113.10", w=280, kind="router")
en(a, dev(a, XV - 130, 180, 260, 70, "Víctima", "198.51.100.99", kind="isp", tsize=17, ssize=14, add=False), 75, 100)
lifeline(a, XA, 250, 450)
lifeline(a, XR, 250, 450)
en(a, f'<line x1="{XV}" y1="250" x2="{XV}" y2="450" stroke="{a.LINE}" stroke-width="2.5" stroke-dasharray="6 6"/>', 75, 100)

# 1 y 2: llega y muere en input
msg(a, XA, XR, 300, "A? mikrotik.com → :53", 3, 50, still=1)
en(a, a.box(XR - 150, 330, 300, 74, a.BADBG, a.BAD, rx=12, sw=2) + a.text(XR, 360, "input · drop all not", 15, a.BAD, a.MONO, 600, "middle")
   + a.text(XR, 384, "coming from LAN", 15, a.BAD, a.MONO, 600, "middle"), 27, 50, still=1)
en(a, a.text(XA, 344, "sin respuesta", 15, a.BAD, a.MONO, 600, "middle"), 30, 50, still=1)

# 3: sin la regla
en(a, a.pill(XR, 262, "si nada frenara el 53", a.AMB, a.AMBBG, 14, 28, anchor="middle"), 50, 100)
msg(a, XA, XR, 316, "A? mikrotik.com", 52, 75)
msg(a, XR, XA, 360, "respuesta", 57, 75, a.AMB)
en(a, a.text(XR + 16, 410, "allow-remote-requests=yes contesta", 15, a.AMB, a.SANS, 600) + a.text(XR + 16, 432, "en todas las IP del router", 15, a.AMB, a.SANS, 600), 58, 75)

# 4: amplificación
msg(a, XA, XR, 316, "consulta chica · src 198.51.100.99", 78, 100, a.BAD)
msg(a, XR, XV, 380, "respuesta mucho más grande", 84, 100, a.BAD)
en(a, f'<rect x="{XR + 6}" y="390" width="{XV - XR - 14}" height="14" rx="7" fill="{a.BAD}" opacity=".25"/>', 86, 100)

# salida
TY = 486
en(a, term(a, 48, TY, 640, ["> nslookup mikrotik.com 203.0.113.10", "DNS request timed out.", "    timeout was 2 seconds."], size=15, colors={1: MINT, 2: MINT}), 30, 50, still=1)
en(a, term(a, 48, TY, 640, ["> nslookup mikrotik.com 203.0.113.10", "(esperando…)"], size=15, colors={1: SKY}), 0, 30)
en(a, note(a, 48, TY, 640, 96, "Por qué importa", ["Un resolver abierto contesta a cualquiera, y la respuesta es mucho", "más grande que la consulta: sirve para atacar a otro."], "bad"), 50, 100)
a.add(note(a, 716, TY, 436, 96, "Con firewall propio", ["dos drop desde la lista WAN, UDP y TCP 53,", "como en la documentación."], "info"))

narr(a, [
    (0, 25, "La notebook está del lado de afuera: para el router, esto llega por la WAN.", a.TXT),
    (25, 50, "Timeout es el resultado correcto: el router no le contesta a internet.", a.OK),
    (50, 75, "Así quedan los equipos sin el drop en input, y se usan sin que el dueño lo sepa.", a.AMB),
    (75, 100, "La víctima recibe el tráfico; el router y su enlace ponen el ancho de banda.", a.BAD),
], still_idx=1)

escribir(a, "30-l1.svg", "El 53 cerrado desde la WAN",
         "Animación en cuatro tiempos con tres líneas de vida: afuera (la notebook en la red de ether1 o un atacante en internet), el router con WAN 203.0.113.10 y una víctima en 198.51.100.99. "
         "1: desde la red de ether1, nslookup le pregunta por mikrotik.com a la IP WAN del router, al puerto 53. "
         "2: la regla de input drop all not coming from LAN la descarta y nslookup da DNS request timed out, que es el resultado correcto. "
         "3: si nada frenara el 53, el router contestaría a cualquiera, porque allow-remote-requests=yes atiende en todas sus direcciones: queda como resolver abierto. "
         "4: un atacante manda consultas chicas con el origen falso de la víctima y el router le manda a ella respuestas mucho más grandes.",
         [12, 38, 62, 70, 92])
