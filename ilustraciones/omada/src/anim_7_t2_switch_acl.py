#!/usr/bin/env python3
"""Lección 7 · Teoría extra: la Switch ACL funciona como lista negra, con permiso por defecto.
"Solo interno" = permit a las subredes internas arriba y deny a todo abajo (guía oficial de ACL de switch)."""
from _anim_om_red import *

a = nueva(26, "VLAN NO AÍSLA", "Switch ACL: todo pasa, salvo lo que cortás", "t")
F = a.steps([
    "Sin reglas, la Switch ACL deja pasar todo: es una lista negra, con permiso por defecto.",
    "Solo una deny de la red de cámaras a todo: corta internet, pero también el NVR.",
    "Permit a las subredes internas arriba, deny a todo abajo: la primera que coincide decide.",
    "Resultado: las cámaras llegan al NVR y no salen a internet. Solo interno.",
], still=2)

a.add(dev(a, 48, 300, 260, 92, "Cámaras", "VLAN 20", icon="camera", sub2="10.10.20.0/24"))
a.add(dev(a, 892, 210, 260, 92, "NVR", "192.168.88.20", icon="server", sub2="red interna"))
a.add(dev(a, 892, 392, 260, 92, "Internet", "1.1.1.1", icon="globe"))
# switch con la lista
SX, SY, SW, SH = 360, 196, 480, 300
a.add(a.box(SX, SY, SW, SH, a.INK, rx=16))
a.add(glyph(a, "server", SX + 20, SY + 18, a.CYAN) + a.text(SX + 64, SY + 42, "Switch · Switch ACL", 19, a.WHITE, a.SANS, 600))
a.add(a.text(SX + 24, SY + 82, "de arriba hacia abajo:", 15, SKY, a.MONO))
a.add(line(308, 346, SX, 346, a.BLUE, 4))
a.add(line(SX + SW, 256, 892, 256, a.BLUE, 4) + line(SX + SW, 438, 892, 438, a.BLUE, 4))


def regla(y, n, txt, col, t0, t1, still):
    at(a, a.box(SX + 20, y, SW - 40, 44, "#0B3A66", rx=10)
       + a.text(SX + 40, y + 28, n, 16, SKY, a.MONO, 600)
       + a.text(SX + 70, y + 28, txt, 16, col, a.MONO, 600), t0, t1, still=still)


at(a, a.text(SX + 24, SY + 130, "(sin reglas)", 17, SKY, a.SANS, 600), 0, 25)
regla(SY + 104, "1", "Deny  VLAN 20 → cualquiera", "#FF9C87", 25, 50, 0)
regla(SY + 104, "1", "Permit VLAN 20 → Redes-Internas", MINT, 50, 100, 1)
regla(SY + 158, "2", "Deny   VLAN 20 → cualquiera", "#FF9C87", 50, 100, 1)
at(a, a.text(SX + 24, SY + 270, "y si nada coincide: permit", 15, SKY, a.MONO), 0, 100, still=1)


def viaje(t0, dest, ok_, label):
    yd = 256 if dest == "nvr" else 438
    travel(a, pkt(a, label, a.BLUE), [(250, 346), (SX + 10, 346)], t0, t0 + 2.5, hold=0.2)
    if ok_:
        travel(a, pkt(a, label, a.BLUE), [(SX + SW - 10, yd), (870, yd)], t0 + 4, t0 + 7, hold=0.8)
    else:
        at(a, xmark(a, SX + SW + 26, yd, 14), t0 + 4, t0 + 16)


# 1: todo pasa
viaje(3, "nvr", True, "→ NVR")
viaje(12, "inet", True, "→ 1.1.1.1")
at(a, check(a, 1128, 256, 12) + check(a, 1128, 438, 12), 19, 25)
# 2: deny sola corta todo
viaje(28, "nvr", False, "→ NVR")
viaje(36, "inet", False, "→ 1.1.1.1")
at(a, a.text(SX + SW + 26, 330, "el NVR también", 15, a.BAD, a.SANS, 600, "middle"), 32, 50)
# 3 y 4: permit interno + deny a todo
viaje(53, "nvr", True, "→ NVR")
at(a, a.box(SX + 16, SY + 100, SW - 32, 52, "none", MINT, rx=12, sw=2.5), 54, 60, still=1)
viaje(62, "inet", False, "→ 1.1.1.1")
at(a, a.box(SX + 16, SY + 154, SW - 32, 52, "none", "#FF9C87", rx=12, sw=2.5), 63, 70)
at(a, check(a, 1128, 256, 12), 60, 100, still=1)
at(a, xmark(a, SX + SW + 26, 438, 14), 66, 100, still=1)
at(a, chip(a, 600, 520, "solo interno", a.OK, a.OKBG, anchor="middle", stroke=a.OK), 78, 100)

status(a, 610, [
    (0, 25, "A diferencia de un firewall que corta lo no permitido, acá pasa lo no prohibido.", a.INK, 0),
    (25, 50, "Una deny a todo, sola, deja a las cámaras sin NVR.", a.BAD, 0),
    (50, 75, "El permit puntual va arriba; la deny general, abajo.", a.INK, 1),
    (75, 100, "Con IP Group, Redes-Internas agrupa todas las subredes internas en una regla.", a.OK, 0),
], x=48, anchor="start", size=16)

write(a, 7, "t2", "La Switch ACL como lista negra: solo interno",
      "Animación en cuatro tiempos con la red de cámaras en la VLAN 20 (10.10.20.0/24), un switch con su Switch ACL evaluada de arriba hacia abajo, "
      "un NVR en la red interna (192.168.88.20) e internet (1.1.1.1). "
      "1: sin reglas, todo pasa: la Switch ACL es una lista negra, con permiso por defecto, y lo que no coincide con nada se permite. "
      "2: con una sola regla Deny de la VLAN 20 a cualquiera, se corta internet pero también el NVR. "
      "3: con la regla 1 Permit de la VLAN 20 hacia el IP Group Redes-Internas y la regla 2 Deny de la VLAN 20 a cualquiera, el paquete al NVR coincide con la 1 y pasa; "
      "el paquete a 1.1.1.1 no coincide con la 1, cae en la 2 y se corta. "
      "4: resultado, solo interno: las cámaras llegan al NVR y no salen a internet.",
      [8, 36, 62, 90])
