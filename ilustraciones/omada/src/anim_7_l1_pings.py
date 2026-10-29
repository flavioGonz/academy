#!/usr/bin/env python3
"""Lección 7 · Laboratorio, paso 4: los tres pings desde la notebook en Invitados-Lab.
Su gateway responde, la red interna no (la Gateway ACL descarta el pedido), internet sí."""
from _anim_om_red import *

a = nueva(26, "VLAN NO AÍSLA", "Tres pings que prueban el aislamiento", "l")
F = a.steps([
    "ping 10.10.30.1: es su propio gateway, en su VLAN. Responde.",
    "ping 192.168.88.1: el pedido coincide con la deny y se descarta. No responde.",
    "ping 1.1.1.1: no coincide con la deny, pasa a internet y vuelve.",
    "Si 192.168.88.1 respondiera, la deny quedó debajo de un permit general: subila.",
], still=1)

# terminal
TX, TY, TW, TH = 48, 186, 560, 380
a.add(a.box(TX, TY, TW, TH, a.INK, rx=14))
a.add(a.text(TX + 20, TY + 32, "notebook en Invitados-Lab · 10.10.30.x", 15, SKY, a.MONO))
LINES = [
    (2, "PS> ping 10.10.30.1", a.WHITE, 0),
    (9, "Respuesta desde 10.10.30.1: bytes=32", MINT, 0),
    (27, "PS> ping 192.168.88.1", a.WHITE, 0),
    (36, "Tiempo de espera agotado para", GOLD, 0),
    (36, "esta solicitud.", GOLD, 0),
    (52, "PS> ping 1.1.1.1", a.WHITE, 0),
    (60, "Respuesta desde 1.1.1.1: bytes=32", MINT, 0),
]
for i, (t0, txt, col, _) in enumerate(LINES):
    at(a, a.text(TX + 20, TY + 72 + i * 30, txt, 15, col, a.MONO, 600 if col != a.WHITE else 400), t0, 100, still=1 if t0 < 50 else 0)

# camino
NX = 700
a.add(dev(a, NX, 186, 452, 70, "Notebook", "10.10.30.x · VLAN 30", icon="laptop"))
a.add(dev(a, NX, 300, 452, 100, "Gateway ER", "10.10.30.1 · 192.168.88.1", icon="server", dark=True))
at(a, chip(a, NX + 62, 364, "Gateway ACL: Deny → Redes-Internas", a.BAD, a.BADBG, stroke=a.BAD), 0, 75, still=1)
a.add(dev(a, NX, 446, 210, 70, "Oficina", "192.168.88.0/24", icon="server"))
a.add(dev(a, NX + 242, 446, 210, 70, "Internet", "1.1.1.1", icon="globe"))
a.add(line(NX + 60, 256, NX + 60, 300, a.AMB, 4))
a.add(line(NX + 105, 400, NX + 105, 446, a.BLUE, 3) + line(NX + 347, 400, NX + 347, 446, a.BLUE, 3))

# 1
travel(a, dot(a, a.BLUE), [(NX + 40, 256), (NX + 40, 318)], 4, 7, hold=0.3)
travel(a, dot(a, a.OK), [(NX + 80, 318), (NX + 80, 256)], 7.5, 10, hold=0.3)
at(a, check(a, NX + 160, 278, 13), 9, 25)
# 2
travel(a, dot(a, a.BLUE), [(NX + 40, 256), (NX + 40, 318)], 29, 32, hold=0.3)
at(a, xmark(a, NX + 105, 424, 14) + a.text(NX + 130, 430, "descartado", 15, a.BAD, a.SANS, 600), 32, 50, still=1)
# 3
travel(a, dot(a, a.BLUE), [(NX + 40, 256), (NX + 40, 350), (NX + 347, 400), (NX + 347, 446)], 54, 58, hold=0.3)
travel(a, dot(a, a.OK), [(NX + 347, 446), (NX + 347, 400), (NX + 80, 350), (NX + 80, 256)], 58.5, 62, hold=0.3)
at(a, check(a, NX + 420, 430, 13), 61, 75)
# 4: orden mal
BADO = (a.box(NX, 534, 452, 96, a.BADBG, a.BAD, rx=12, sw=1.5)
        + a.text(NX + 18, 560, "1  Permit · todo", 15, a.INK, a.MONO, 600)
        + a.text(NX + 18, 586, "2  Deny · Invitados → Redes-Internas", 15, a.BAD, a.MONO, 600)
        + a.text(NX + 18, 614, "Orden al revés: la deny nunca llega a actuar.", 15, a.BAD, a.SANS, 600))
at(a, BADO, 77, 100)
travel(a, dot(a, a.BLUE), [(NX + 40, 256), (NX + 40, 350), (NX + 105, 400), (NX + 105, 446)], 80, 84, hold=0.4)
travel(a, dot(a, a.BAD), [(NX + 105, 446), (NX + 105, 400), (NX + 80, 350), (NX + 80, 256)], 85, 88, hold=0.4)
at(a, a.box(TX + 14, TY + 72 + 3 * 30 - 20, TW - 28, 56, a.INK, rx=4), 86, 100)
at(a, a.text(TX + 20, TY + 72 + 3 * 30, "Respuesta desde 192.168.88.1: bytes=32", 15, a.BAD, a.MONO, 600), 86, 100)

status(a, 630, [
    (0, 25, "Que el propio gateway responda es normal.", a.INK, 0),
    (25, 50, "Cada Tiempo de espera agotado es la deny haciendo su trabajo.", a.OK, 1),
    (50, 75, "Gateway propio sí, red interna no, internet sí: eso es aislamiento.", a.OK, 0),
    (75, 100, "", a.INK, 0),
], x=48, anchor="start", size=16)

write(a, 7, "l1", "Los tres pings que prueban el aislamiento de invitados",
      "Animación en cuatro tiempos con la terminal de una notebook conectada a Invitados-Lab (10.10.30.x) y el camino por el gateway ER, que tiene la Gateway ACL Deny hacia Redes-Internas, "
      "hasta la oficina (192.168.88.0/24) o internet (1.1.1.1). "
      "1: ping 10.10.30.1 llega a su propio gateway en su VLAN y responde, lo que es normal. "
      "2: ping 192.168.88.1 coincide con la deny, el pedido se descarta en el gateway y la terminal muestra Tiempo de espera agotado para esta solicitud. "
      "3: ping 1.1.1.1 no coincide con la deny, sale a internet y vuelve con respuesta. "
      "4: si la lista tuviera un permit general arriba de la deny, el ping a 192.168.88.1 respondería porque la deny nunca llega a actuar; hay que subir la deny.",
      [8, 36, 62, 92])
