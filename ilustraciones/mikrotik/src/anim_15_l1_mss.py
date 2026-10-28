#!/usr/bin/env python3
"""Lección 15 · Laboratorio, paso 5: MSS en PPPoE. El SYN anuncia MSS 1460 (para 1500); con MTU 1492 un segmento
lleno no entra y, si nadie avisa por ICMP, se pierde. change-mss con clamp-to-pmtu deja el SYN en 1452
(1492 - 40 de cabeceras IP y TCP) y los segmentos del servidor pasan. Valores de la teoría de la lección."""
from _anim_red_1_9 import *

a = Anim(T=26, kicker="MIKROTIK · PPPOE CON ANTEL · LABORATORIO", title="El MSS del SYN decide si la página carga entera")
a.steps([
    "La PC abre una conexión: su SYN anuncia MSS=1460, pensado para 1500 bytes.",
    "El servidor manda segmentos de 1460: 1500 bytes no entran en 1492 y se pierden.",
    "Con change-mss, el SYN sale por pppoe-antel con MSS=1452.",
    "Ahora los segmentos son de 1452: el paquete mide 1492 y pasa.",
], still=3)

PC, MT, SV = 150, 520, 1040
a.add(dev(a, 48, 176, 220, 78, "PC de la LAN", "MTU 1500", icon="laptop"))
a.add(dev(a, 380, 176, 290, 78, "MikroTik", "pppoe-antel · 1492", icon="server", dark=True))
a.add(dev(a, 920, 176, 232, 78, "Servidor web", "en internet", icon="cloud"))
for x in (PC, MT, SV):
    a.add(lifeline(a, x, 254, 520))
# tramo PPPoE
BX = 600
a.add(f'<rect x="{BX}" y="262" width="96" height="258" rx="10" fill="{a.AMBBG}" opacity=".8"/>')
a.add(a.text(BX + 48, 282, "PPPoE", 15, a.AMB, a.MONO, 600, "middle"))
a.add(a.text(BX + 48, 302, "1492", 15, a.AMB, a.MONO, 600, "middle"))

msg(a, PC, MT, 336, "SYN MSS=1460", 3, end=50, still=0)
msg(a, MT, SV, 336, "SYN MSS=1460", 8, end=50, still=0, sub="sin regla: pasa igual")
msg(a, SV, BX + 96, 396, "1460 + 40 = 1500 bytes", 28, color=a.BAD, end=50, still=0, dash="8 6")
a.add(during(a, xmark(a, BX + 48, 396) + a.text(BX + 48, 432, "no entra", 15, a.BAD, a.MONO, 600, "middle"), 33, 50))
a.add(during(a, a.text(PC - 100, 470, "sin aviso por ICMP: la página carga a medias", 15, a.BAD, a.SANS, 600), 36, 50))

msg(a, PC, MT, 336, "SYN MSS=1460", 53, end=100, still=1)
msg(a, MT, SV, 336, "SYN MSS=1452", 58, color=a.OK, end=100, still=1, sub="change-mss: clamp-to-pmtu")
msg(a, SV, MT, 420, "1452 + 40 = 1492 bytes", 78, color=a.OK, end=100, still=1)
msg(a, MT, PC, 470, "datos", 85, color=a.OK, end=100, still=1)
a.add(during(a, check(a, BX + 48, 420), 82, 100, still=1))

TY = 540
a.add(a.box(48, TY, 1104, 96, a.INK, rx=14))
a.add(a.text(66, TY + 36, "/ip/firewall/mangle/add chain=forward out-interface=pppoe-antel protocol=tcp", 15, a.WHITE, a.MONO))
a.add(a.text(66, TY + 64, "  tcp-flags=syn action=change-mss new-mss=clamp-to-pmtu passthrough=yes comment=\"MSS PPPoE\"", 15, a.WHITE, a.MONO))
a.add(during(a, a.box(46, TY - 2, 1108, 100, "none", GOLD, rx=15, sw=3), 52, 64))
a.add(a.text(48, 660, "Antes, fijate si el perfil PPP ya lo hace: /ppp/profile/print detail where name=default (change-tcp-mss).", 15, a.TXT, a.SANS, 600))

write(a, 15, "l1", "Ajuste de MSS con PPPoE",
      "Animación en cuatro tiempos entre una PC de la LAN (MTU 1500), el MikroTik con pppoe-antel (MTU 1492) y un servidor web, con el tramo PPPoE marcado en 1492. "
      "1: la PC abre una conexión y su SYN anuncia MSS=1460, pensado para 1500 bytes; sin regla, el SYN pasa igual. "
      "2: el servidor manda segmentos de 1460 más 40 de cabeceras, 1500 bytes, que no entran en el tramo de 1492; si nadie avisa por ICMP, se pierden y la página carga a medias. "
      "3: con la regla de mangle change-mss new-mss=clamp-to-pmtu para los SYN que salen por pppoe-antel, el SYN sale con MSS=1452. "
      "4: el servidor manda segmentos de 1452 más 40, 1492 bytes, que pasan, y los datos llegan a la PC. "
      "Antes de agregar la regla conviene ver si el perfil PPP ya trae change-tcp-mss.",
      [10, 36, 62, 92])
