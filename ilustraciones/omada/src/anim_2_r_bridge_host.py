#!/usr/bin/env python3
"""Lección 2 · Resumen, "Cómo se ve en la red": controlador en Docker con red bridge contra red host.
La web en el 8043 abre igual; el broadcast de descubrimiento al UDP 29810 no cruza el NAT de la red bridge."""
from _anim_om_red import *

a = nueva(26, "HOST DEDICADO", "Docker en bridge: la web abre, el EAP nunca aparece")
F = a.steps([
    "Red bridge: la notebook abre https://192.168.88.10:8043 y la web anda. Todo parece bien.",
    "El EAP de fábrica anuncia por broadcast al UDP 29810: llega a la VM y no cruza el NAT.",
    "Se recrea el contenedor con network_mode: host: usa la red de la VM sin NAT.",
    "El broadcast llega al 29810 del controlador, que le responde: el EAP aparece en Pending.",
], still=1)

# equipos de la LAN
a.add(dev(a, 48, 208, 262, 92, "EAP de fábrica", "busca controlador", icon="wifi"))
a.add(dev(a, 48, 432, 262, 92, "Notebook", "navegador", icon="laptop"))
a.add(dev(a, 352, 322, 176, 92, "Switch", "misma LAN", icon="server"))
a.add(line(310, 254, 380, 254, a.BLUE, 3) + line(380, 254, 380, 322, a.BLUE, 3))
a.add(line(310, 478, 380, 478, a.BLUE, 3) + line(380, 478, 380, 414, a.BLUE, 3))
a.add(line(528, 368, 600, 368, a.BLUE, 4))

# VM
a.add(a.box(600, 186, 552, 376, a.WHITE, a.LINE, rx=18, sw=2))
a.add(a.text(624, 220, "VM Linux · 192.168.88.10", 17, a.INK, a.SANS, 600))
a.add(a.box(586, 340, 64, 56, a.INK, rx=10) + a.text(618, 374, "eth0", 15, a.WHITE, a.MONO, 600, "middle"))

# bridge (fases 1 y 2)
BR = (a.box(690, 246, 438, 292, "#EAF2FA", a.LINE, rx=16, sw=2, extra='stroke-dasharray="7 6"')
      + a.text(712, 276, "red bridge de Docker", 16, a.GREY, a.MONO)
      + a.box(668, 330, 120, 76, a.AMBBG, a.AMB, rx=12, sw=2)
      + a.text(728, 362, "NAT", 17, a.AMB, a.SANS, 600, "middle")
      + a.text(728, 386, "publica 8043", 15, a.AMB, a.MONO, 400, "middle")
      + dev(a, 830, 318, 278, 100, "omada-controller", "contenedor", icon="server", dark=True)
      + line(650, 368, 668, 368, a.BLUE, 3) + line(788, 368, 830, 368, a.BLUE, 3))
at(a, BR, 0, 52, still=1)
# host (fases 3 y 4)
HO = (dev(a, 690, 300, 438, 136, "omada-controller", "network_mode: host", icon="server", dark=True, sub2="escucha 8043 y 29810 en la VM")
      + line(650, 368, 690, 368, a.BLUE, 4))
at(a, HO, 52, 100)
at(a, chip(a, 690, 462, "docker compose up -d", a.INK, a.SLATE), 54, 76)

# 1: la web anda
travel(a, dot(a, a.CYAN), [(310, 478), (380, 478), (380, 368), (528, 368), (600, 368), (728, 368), (830, 368)], 3, 11, hold=0.5)
travel(a, dot(a, a.OK), [(830, 368), (728, 368), (600, 368), (528, 368), (380, 368), (380, 478), (310, 478)], 12, 19, hold=0.5)
at(a, a.text(316, 502, "TCP 8043", 15, a.CYAN, a.MONO, 600), 2, 25)
at(a, chip(a, 179, 540, "la web abre", a.OK, a.OKBG, anchor="middle", stroke=a.OK), 18, 50, still=1)
# 2: el broadcast se queda en la VM
for t0 in (28, 36):
    travel(a, dot(a, a.AMB, 10), [(310, 254), (380, 254), (380, 368), (528, 368), (606, 368), (650, 368)], t0, t0 + 5, hold=1.2)
    travel(a, dot(a, a.AMB, 7), [(380, 300), (380, 414), (380, 432)], t0 + 2, t0 + 3.5, hold=0.6)
at(a, xmark(a, 659, 368, 12), 33, 52, still=1)
at(a, a.text(712, 470, "el broadcast se queda en eth0:", 16, a.BAD, a.SANS, 600)
   + a.text(712, 494, "no cruza el NAT de la red bridge", 16, a.BAD, a.SANS, 600), 33, 52, still=1)
at(a, a.text(318, 238, "broadcast UDP 29810", 15, a.AMB, a.MONO, 600), 26, 52, still=1)
at(a, chip(a, 179, 176, "Devices: no aparece nada", a.BAD, a.BADBG, anchor="middle", stroke=a.BAD), 40, 52, still=1)
# 4: con host, llega y responde
travel(a, dot(a, a.AMB, 10), [(310, 254), (380, 254), (380, 368), (528, 368), (606, 368), (720, 368)], 77, 82, hold=0.6)
travel(a, dot(a, a.OK, 10), [(720, 368), (606, 368), (528, 368), (380, 368), (380, 254), (310, 254)], 84, 89, hold=0.6)
at(a, a.text(318, 238, "UDP 29810 y respuesta", 15, a.OK, a.MONO, 600), 76, 100)
at(a, chip(a, 179, 176, "Pending", a.AMB, a.AMBBG, anchor="middle", stroke=a.AMB), 89, 100)
at(a, check(a, 760, 470, 15) + a.text(784, 476, "el 29810 que escucha es el de la VM", 15, a.OK, a.SANS, 600), 82, 100)

status(a, 610, [
    (0, 25, "Un pedido dirigido al 8043 cruza el NAT porque el puerto está publicado.", a.INK, 0),
    (25, 52, "El NAT solo pasa lo dirigido a un puerto publicado: el broadcast de la LAN no lo cruza.", a.BAD, 1),
    (52, 75, "Con red host no hay NAT en el medio: el contenedor comparte la red de la VM.", a.INK, 0),
    (75, 100, "En Docker Desktop de Windows o macOS la red host no funciona: ahí, Inform URL.", a.AMB, 0),
], x=48, anchor="start")

write(a, 2, "r1", "Controlador en Docker: red bridge contra red host",
      "Animación en cuatro tiempos con un EAP de fábrica, la notebook del técnico, un switch y una VM Linux 192.168.88.10 que corre el contenedor omada-controller. "
      "1: con red bridge, la notebook abre https://192.168.88.10:8043; el pedido cruza el NAT de Docker porque el puerto está publicado y la web anda. "
      "2: el EAP anuncia por broadcast al UDP 29810; el broadcast llega a toda la LAN y a eth0 de la VM, pero no cruza el NAT de la red bridge y en Devices no aparece nada. "
      "3: se recrea el contenedor con network_mode: host y queda usando la red de la VM, escuchando 8043 y 29810 sin NAT en el medio. "
      "4: el broadcast llega al 29810 del controlador, que le responde por el mismo puerto, y el EAP aparece en Pending. "
      "En Docker Desktop de Windows o macOS la red host no funciona y los equipos llegan con Inform URL.",
      [8, 34, 44, 62, 86, 95])
