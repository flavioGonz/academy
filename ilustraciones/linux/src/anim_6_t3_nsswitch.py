#!/usr/bin/env python3
"""Lección 6, Teoría (figura extra): el orden de /etc/nsswitch.conf. ping resuelve con la biblioteca del sistema,
que sigue hosts: files dns, y una línea vieja de /etc/hosts le gana al DNS; dig le pregunta directo al servidor
DNS de /etc/resolv.conf y no mira /etc/hosts. getent hosts muestra lo que ve el sistema.
Fuentes: teoría de la lección (orden de nsswitch.conf, /etc/hosts antes que el DNS), nsswitch.conf(5), dig(1),
getent(1). Nombre y direcciones de ejemplo."""
from _anims_lnx_rl import *

a = nueva(26, "LINUX · NOMBRES · TEORÍA", "ping y dig no preguntan al mismo lugar")
a.steps([
    "ping pide el nombre al sistema, que sigue hosts: files dns.",
    "files va primero: una línea vieja de /etc/hosts gana. Responde .88.40.",
    "dig no pasa por nsswitch: le pregunta al DNS de resolv.conf. Dice .88.45.",
    "Dos respuestas distintas: la línea vieja de /etc/hosts es el problema.",
], still=3)

# clientes
a.add(dev(a, 48, 186, 230, 76, "ping", "app.obra.lan", None, dark=True))
a.add(dev(a, 48, 400, 230, 76, "dig", "app.obra.lan", None, dark=True))
# nsswitch
a.add(a.box(340, 176, 290, 96, a.WHITE, "#C2D4E6", rx=14) + a.text(360, 206, "/etc/nsswitch.conf", 16, a.INK, a.MONO, 700)
      + mono(a, 360, 238, "hosts: files dns", 17, a.BLUE, 700) + a.text(360, 262, "por ejemplo", 14, a.GREY, a.SANS, 500))
# /etc/hosts
a.add(a.box(700, 166, 452, 116, a.WHITE, "#C2D4E6", rx=14) + a.text(720, 196, "/etc/hosts  (files)", 16, a.INK, a.MONO, 700)
      + mono(a, 720, 228, "127.0.0.1      localhost", 15, a.GREY, 500) + mono(a, 720, 256, "192.168.88.40  app.obra.lan", 15, a.AMB, 700))
en(a, a.text(1132, 256, "línea vieja", 14, a.AMB, a.SANS, 700, "end"), 30, 100, still=1)
# DNS
a.add(dev(a, 700, 380, 452, 116, "Servidor DNS", "nameserver de /etc/resolv.conf", "globe", sub2="app.obra.lan  A  192.168.88.45"))
a.add(camino("M278 224 H340", "#C2D4E6", 4) + camino("M630 224 H700", "#C2D4E6", 4) + camino("M630 252 C 670 252, 650 420, 700 420", "#C2D4E6", 3, "6 6")
      + camino("M278 438 H700", "#C2D4E6", 4))
a.add(a.text(632, 330, "dns: solo si files", 15, a.GREY, a.SANS, 600, "end") + a.text(632, 352, "no lo encuentra", 15, a.GREY, a.SANS, 600, "end"))

viaje(a, "app.obra.lan?", [(300, 224), (330, 224)], 3, 7, bg=a.BLUE, size=13, hold=1)
en(a, a.box(336, 172, 298, 104, "none", a.BLUE, rx=16, sw=3), 6, 25)
viaje(a, "1 files", [(640, 224), (690, 224)], 27, 31, bg=a.BLUE, size=13, hold=1)
en(a, a.box(712, 236, 428, 30, "none", a.AMB, rx=8, sw=3), 31, 100, still=1)
viaje(a, ".88.40", [(690, 286), (330, 286)], 36, 43, bg=a.AMB, size=14, hold=1)
en(a, mono(a, 48, 304, "PING app.obra.lan (192.168.88.40)", 15, a.AMB, 700), 44, 100, still=1)
# dig
viaje(a, "A? · UDP 53", [(300, 438), (690, 438)], 52, 59, bg=a.CYAN, size=13, hold=1)
viaje(a, ".88.45", [(690, 452), (300, 452)], 61, 68, bg=a.OK, size=14, hold=1)
en(a, mono(a, 48, 510, "$ dig app.obra.lan +short", 15, a.INK, 600) + mono(a, 48, 536, "192.168.88.45", 15, a.OK, 700), 68, 100, still=1)
en(a, a.text(300, 418, "no mira /etc/hosts", 15, a.CYAN, a.SANS, 700), 52, 100, still=1)

# paso 4
en(a, nota(a, 520, 520, 632, 84, "La misma pregunta, dos respuestas", ["Sacá o corregí la línea vieja de /etc/hosts.", "getent hosts app.obra.lan muestra lo que ve ping."], "amb"), 76, 100, still=1)

narr(a, [
    (0, 25, "Casi todos los programas resuelven nombres con la biblioteca del sistema.", None),
    (25, 50, "Si /etc/hosts tiene el nombre, el DNS ni se consulta.", a.AMB),
    (50, 75, "dig es una herramienta de DNS: sirve para ver qué dice el servidor.", a.OK),
    (75, 100, "Cuando ping y dig no coinciden, mirá /etc/hosts antes que el DNS.", a.AMB),
], y=640, still_idx=3)

escribir(a, "6-t3", "ping y dig no preguntan al mismo lugar",
         "Animación en cuatro tiempos con dos clientes a la izquierda, ping y dig, que buscan el nombre de ejemplo app.obra.lan. En el medio, /etc/nsswitch.conf con hosts: files dns; a la derecha, /etc/hosts y el servidor DNS de /etc/resolv.conf, que tiene app.obra.lan en 192.168.88.45. "
         "1: ping le pide el nombre al sistema, que sigue el orden de nsswitch.conf. "
         "2: files va primero: /etc/hosts tiene una línea vieja, 192.168.88.40 app.obra.lan, que gana; el DNS solo se consultaría si files no lo encontrara, y ping muestra PING app.obra.lan (192.168.88.40). "
         "3: dig no mira /etc/hosts: le pregunta al DNS por UDP 53 y recibe 192.168.88.45. "
         "4: la misma pregunta da dos respuestas: hay que sacar o corregir la línea vieja de /etc/hosts, y getent hosts app.obra.lan muestra lo que ve ping.",
         [10, 40, 64, 90])
