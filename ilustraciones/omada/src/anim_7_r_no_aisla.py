#!/usr/bin/env python3
"""Lección 7 · Resumen, "Cómo se ve en la red": la VLAN de invitados llega a la web del NVR porque el gateway rutea.
El broadcast queda en la VLAN 30; el paquete ruteado pasa. La Gateway ACL lo corta y la salida a internet sigue."""
from _anim_om_red import *

a = nueva(26, "VLAN NO AÍSLA", "El invitado llega al NVR: la VLAN no alcanzaba")
F = a.steps([
    "La notebook invitada busca su gateway por ARP: ese broadcast no sale de la VLAN 30.",
    "Pide la web del NVR, 192.168.88.20: el gateway tiene una pata en cada VLAN y la rutea.",
    "Con la Gateway ACL Invitados-sin-interna, el mismo paquete se descarta en el gateway.",
    "Hacia 1.1.1.1 no coincide con la deny: sale a internet. Aislada, pero con salida.",
], still=2)

# zonas
a.add(a.box(48, 250, 330, 300, "#FFF7E8", a.AMB, rx=18, sw=2))
a.add(a.text(68, 282, "VLAN 30 · Invitados", 17, a.AMB, a.SANS, 600))
a.add(a.text(68, 306, "10.10.30.0/24", 15, a.GREY, a.MONO))
a.add(a.box(822, 250, 330, 300, "#EAF4FC", a.BLUE, rx=18, sw=2))
a.add(a.text(842, 282, "Red por defecto · oficina", 17, a.BLUE, a.SANS, 600))
a.add(a.text(842, 306, "192.168.88.0/24", 15, a.GREY, a.MONO))
for r, t0 in ((40, 4), (72, 7), (104, 10)):
    at(a, f'<circle cx="213" cy="400" r="{r}" fill="none" stroke="{a.AMB}" stroke-width="2.5" stroke-dasharray="6 6"/>', t0, t0 + 6)
at(a, a.text(213, 534, "ARP: ¿quién tiene 10.10.30.1?", 15, a.AMB, a.MONO, 600, "middle"), 3, 25)
a.add(dev(a, 78, 420, 270, 86, "Notebook invitada", "10.10.30.50", icon="laptop"))
a.add(dev(a, 852, 420, 270, 86, "NVR", "192.168.88.20 · web", icon="camera"))
# gateway
GX, GY, GW, GH = 452, 360, 296, 150
a.add(dev(a, GX, GY, GW, GH, "Gateway ER", "rutea entre redes", icon="server", dark=True))
a.add(a.text(GX + 18, GY + 112, "10.10.30.1", 15, GOLD, a.MONO, 600) + a.text(GX + GW - 18, GY + 112, "192.168.88.1", 15, "#7FD6F0", a.MONO, 600, "end"))
a.add(line(348, 463, 452, 463, a.AMB, 4) + line(748, 463, 852, 463, a.BLUE, 4))
# internet
a.add(a.box(500, 186, 200, 70, "#EAF2FA", a.LINE, rx=30, sw=2, extra='stroke-dasharray="7 6"'))
a.add(a.text(600, 218, "internet", 16, a.GREY, a.MONO, 400, "middle") + a.text(600, 240, "1.1.1.1", 15, a.GREY, a.MONO, 400, "middle"))
a.add(line(600, 256, 600, 360, a.GREY, 3))
# ACL
at(a, chip(a, GX + GW / 2, 520, "Deny: Invitados → Redes-Internas", a.BAD, a.BADBG, anchor="middle", stroke=a.BAD), 52, 100, still=1)

# carril del paquete (vista de camino)
a.add(line(213, 506, 213, 590, a.LINE, 2, "4 5") + line(987, 506, 987, 590, a.LINE, 2, "4 5") + line(213, 590, 987, 590, a.LINE, 2, "4 5"))
a.add(line(600, 552, 600, 590, a.LINE, 2, "4 5"))
# 1: ARP en la VLAN 30
at(a, a.text(987, 538, "acá no llega", 15, a.GREY, a.SANS, 600, "middle"), 12, 25)
# 2: el paquete ruteado pasa
travel(a, pkt(a, "→ 192.168.88.20", a.BLUE), [(213, 590), (600, 590)], 28, 32, hold=0.3)
travel(a, pkt(a, "→ 192.168.88.20", a.BLUE), [(600, 590), (987, 590)], 33, 37, hold=0.5)
travel(a, pkt(a, "respuesta", a.OK), [(987, 590), (213, 590)], 39, 45, hold=1)
at(a, check(a, 987, 400, 15) + a.text(1010, 406, "la web abre", 15, a.BAD, a.SANS, 600), 37, 50)
at(a, a.text(600, 334, "pasa: la VLAN separó el broadcast, no el ruteo", 15, a.BAD, a.SANS, 600, "middle"), 30, 50)
# 3: la ACL lo descarta
travel(a, pkt(a, "→ 192.168.88.20", a.BLUE), [(213, 590), (560, 590)], 56, 61, hold=8)
at(a, xmark(a, 680, 590, 16) + a.text(706, 596, "descartado en el gateway", 15, a.BAD, a.SANS, 600), 62, 75, still=1)
# 4: internet sigue
travel(a, pkt(a, "→ 1.1.1.1", a.BLUE), [(213, 590), (600, 590)], 78, 82, hold=0.2)
travel(a, dot(a, a.BLUE, 10), [(600, 574), (600, 262)], 83, 86, hold=0.5)
travel(a, dot(a, a.OK, 10), [(600, 262), (600, 360)], 88, 91, hold=0.3)
at(a, check(a, 728, 222, 15), 86, 100)

status(a, 640, [
    (0, 25, "El broadcast es por VLAN: cada red tiene el suyo.", a.INK, 0),
    (25, 50, "Si el gateway rutea entre VLAN, los equipos de una llegan a la otra por capa 3.", a.BAD, 0),
    (50, 75, "La deny va en la Gateway ACL, arriba de cualquier permit general.", a.INK, 1),
    (75, 100, "Probalo con ping: red interna no responde, internet sí.", a.OK, 0),
], x=48, anchor="start", size=16)

write(a, 7, "r1", "La VLAN de invitados llega al NVR hasta que entra la ACL",
      "Animación en cuatro tiempos con la VLAN 30 de invitados (10.10.30.0/24) y una notebook invitada 10.10.30.50, el gateway ER con una interfaz en cada red (10.10.30.1 y 192.168.88.1), "
      "internet y la red de la oficina con un NVR en 192.168.88.20. "
      "1: la notebook busca su gateway con un ARP; ese broadcast queda dentro de la VLAN 30 y no llega a la red de la oficina. "
      "2: la notebook pide la web del NVR; como no está en su red, el paquete va al gateway, que lo rutea a la otra VLAN, y la web abre: la VLAN separó el broadcast, no el ruteo. "
      "3: con la Gateway ACL Invitados-sin-interna, Deny desde Invitados hacia el grupo Redes-Internas, el mismo paquete se descarta en el gateway. "
      "4: un paquete a 1.1.1.1 no coincide con la deny y sale a internet: la red de invitados queda aislada de la interna pero con salida. Se verifica con ping.",
      [8, 36, 64, 90])
