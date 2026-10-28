#!/usr/bin/env python3
"""Lección 32 (Bloqueo por DNS) · Laboratorio paso 4: la estática FWD saca un nombre de la adlist; la pausa apaga todas las adlists un rato."""
from _anim_r20_31 import *

a, _ = nuevo(26, "MIKROTIK · BLOQUEO POR DNS · PASO 4", "Una excepción y una pausa",
             ["Antes: example.net está en la adlist y el router contesta 0.0.0.0.",
              "Con una estática type=FWD para example.net, la consulta sigue hacia arriba.",
              "adlist/pause duration=10m: mientras dura, ninguna adlist bloquea.",
              "Cuando vence la pausa, las adlists vuelven solas: ads.example.net, 0.0.0.0."], still=1)

XN, XR, XU = 180, 590, 1010
head(a, XN, 178, "Notebook", "192.168.88.254", w=260)
head(a, XR, 178, "Router", "adlist + estáticas", w=260, kind="router")
head(a, XU, 178, "Servidores de arriba", "servers", w=270, kind="isp")
for x in (XN, XR, XU):
    lifeline(a, x, 248, 440)

def nota(t0, t1, txt, col, still=0):
    en(a, a.text(XR - 14, 324, txt, 14, col, a.MONO, 600, "end"), t0, t1, still)

# 1. bloqueado
msg(a, XN, XR, 290, "A? example.net", 2, 25)
nota(6, 25, "en la adlist", a.BAD)
msg(a, XR, XN, 360, "0.0.0.0", 9, 25, a.BAD)
# 2. FWD
msg(a, XN, XR, 290, "A? example.net", 27, 50, still=1)
nota(31, 50, "estática FWD: sigue", a.OK, still=1)
msg(a, XR, XU, 330, "A? example.net", 33, 50, still=1)
msg(a, XU, XR, 370, "dirección real", 38, 50, a.OK, still=1)
msg(a, XR, XN, 370, "dirección real", 43, 50, a.OK, still=1)
# 3. pausa
msg(a, XN, XR, 290, "A? ads.example.net", 54, 75)
nota(58, 75, "adlists en pausa", a.AMB)
msg(a, XR, XU, 330, "A? ads.example.net", 60, 75)
msg(a, XU, XR, 370, "dirección real", 64, 75, a.AMB)
msg(a, XR, XN, 370, "dirección real", 68, 75, a.AMB)
# 4. vuelve
msg(a, XN, XR, 290, "A? ads.example.net", 79, 100)
nota(83, 100, "adlist activa otra vez", a.BAD)
msg(a, XR, XN, 360, "0.0.0.0", 86, 100, a.BAD)

# barra de la pausa
a.add(a.box(48, 462, 1104, 128, a.WHITE, a.LINE, rx=14))
a.add(a.text(66, 492, "/ip/dns/static/add name=example.net type=FWD", 15, a.INK, a.MONO, 600))
a.add(a.text(66, 520, "/ip/dns/adlist/pause duration=10m", 15, a.INK, a.MONO, 600))
en(a, ring(a, 56, 472, 640, 28, a.OK, rx=8, sw=2), 27, 50, still=1)
en(a, ring(a, 56, 500, 640, 28, a.AMB, rx=8, sw=2), 52, 75)
a.add(a.text(66, 566, "pausa", 14, a.GREY, a.MONO, 600))
a.add(a.box(130, 552, 800, 20, "#E6EDF4", rx=10))
k = a.keyframes([(0, 0), (52, 0), (52.5, 1), (75, 0.0), (100, 0)], "transform", "scaleX({})")
a.add(a.group(a.box(130, 552, 800, 20, a.AMB, rx=10), k, still=0, origin="130px 552px"))
flip(a, 950, 568, [(0, 52, "sin pausa", a.GREY), (52, 75, "10 min corriendo", a.AMB), (75, 100, "vencida", a.BAD)], size=14, still_idx=0)
a.add(a.text(730, 506, "la excepción es permanente;", 14, a.GREY, a.SANS, 600))
a.add(a.text(730, 526, "la pausa, por un rato", 14, a.GREY, a.SANS, 600))

narr(a, [
    (0, 25, "La adlist contesta desde el router: la consulta no sale.", a.TXT),
    (25, 50, "FWD es lo contrario de bloquear: deja pasar ese nombre aunque esté en la lista.", a.OK),
    (50, 75, "La pausa sirve para probar si un problema es del bloqueo.", a.AMB),
    (75, 100, "No hay que acordarse de volverla atrás: vence sola.", a.TXT),
], still_idx=1)

escribir(a, "32-l1.svg", "Excepción FWD y pausa de adlist",
         "Animación en cuatro tiempos con la notebook (192.168.88.254), el router con la adlist y sus estáticas, y los servidores de arriba. Abajo, los dos comandos del paso 4 y una barra de pausa. "
         "1: example.net está en la adlist y el router contesta 0.0.0.0. 2: con /ip/dns/static/add name=example.net type=FWD, la consulta por example.net sigue hacia arriba y vuelve la dirección real. "
         "3: con /ip/dns/adlist/pause duration=10m, ninguna adlist bloquea mientras corre la pausa: ads.example.net también resuelve. "
         "4: cuando la pausa vence, las adlists vuelven solas y ads.example.net vuelve a dar 0.0.0.0.",
         [12, 40, 48, 66, 92])
