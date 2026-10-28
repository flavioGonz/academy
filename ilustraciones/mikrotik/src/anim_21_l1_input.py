#!/usr/bin/env python3
"""Lección 21 · L2TP con IPsec · Laboratorio paso 3: qué ve la cadena input cuando conecta un cliente.
UDP 500, UDP 4500 o ESP, y el UDP 1701 que vuelve a pasar por input después de descifrar; y qué pasa si las reglas quedan debajo del drop.
"""
from _anim_mk_32_39 import *

a = Anim(T=26, kicker="MIKROTIK · L2TP CON IPSEC · PASO 3", title="Lo que ve input cuando un cliente conecta")
a.steps([
    "Llega IKE por UDP 500. Es nuevo: baja por la lista hasta \"L2TP IPsec\" y pasa.",
    "Con NAT todo sigue en UDP 4500, misma regla. Sin NAT, los datos llegan en ESP.",
    "El router descifra y el L2TP (UDP 1701) vuelve a entrar a input: también pasa.",
    "Si las reglas quedan debajo del drop, nunca se miran: el cliente no conecta.",
], still=2, size=17)

LX, LW, RY0, RH = 300, 560, 232, 46
ROWS = [
    ("defconf: accept established,related,untracked", a.WHITE, None),
    ("defconf: drop invalid", a.WHITE, None),
    ("defconf: accept ICMP", a.WHITE, None),
    ("L2TP IPsec · udp 500,4500,1701 · accept", MINT, "nueva"),
    ("ESP · protocol=ipsec-esp · accept", MINT, "nueva"),
    ("defconf: drop all not coming from LAN", ROSE, None),
]


def ry(i):
    return RY0 + i * RH


a.add(a.box(LX - 20, RY0 - 40, LW + 40, RH * 6 + 74, a.INK, rx=18))
a.add(a.text(LX, RY0 + RH * 6 + 22, "/ip/firewall/filter · chain=input · de arriba hacia abajo", 15, SKY, a.MONO))
T_SWAP = 77
for i, (t, col, tag) in enumerate(ROWS):
    inner = a.box(LX, 2, LW, RH - 8, a.NAVY2, rx=10) + a.text(LX + 16, 29, t, 15, col, a.MONO, 600 if col != a.WHITE else 400)
    if tag:
        inner += a.pill(LX + LW - 12, 8, tag, a.OK, a.OKBG, 13, 24, "end")
    if i in (3, 4):      # en el tiempo 4 bajan debajo del drop
        mv = a.move([(0, 0, ry(i)), (T_SWAP, 0, ry(i)), (T_SWAP + 3, 0, ry(i + 1)), (98, 0, ry(i + 1)), (99.5, 0, ry(i)), (100, 0, ry(i))])
        a.add(a.group(inner, mv, still=1))
    elif i == 5:
        mv = a.move([(0, 0, ry(5)), (T_SWAP, 0, ry(5)), (T_SWAP + 3, 0, ry(3)), (98, 0, ry(3)), (99.5, 0, ry(5)), (100, 0, ry(5))])
        a.add(a.group(inner, mv, still=1))
    else:
        a.add(place(inner, 0, ry(i)))


def hl(i, t0, t1, col, still=0):
    a.add(during(a, a.box(LX - 4, ry(i) - 2, LW + 8, RH - 0, "none", col, rx=12, sw=3.5), t0, t1, still=still))


# derecha: el router por dentro
BX = 924
a.add(a.box(BX, 232, 228, 186, a.WHITE, a.LINE, rx=16))
a.add(a.text(BX + 18, 262, "El router por dentro", 16, a.INK, a.SANS, 600))
for k, t in enumerate(["IKE: UDP 500 / 4500", "descifra ESP", "L2TP: UDP 1701", "PPP: usuario y IP"]):
    a.add(a.text(BX + 18, 298 + k * 30, t, 15, a.TXT, a.MONO))
a.add(during(a, a.box(BX + 8, 278, 212, 56, "none", a.OK, rx=10, sw=2.5), 10, 50))
a.add(during(a, a.box(BX + 8, 338, 212, 56, "none", a.OK, rx=10, sw=2.5), 54, 74, still=1))

LANE = 262
a.add(line(LANE, 204, LANE, 510, a.LINE, 3, "4 7"))
a.add(a.text(LANE - 80, 216, "entra", 15, a.GREY, a.MONO, 400, "end"))


def descend(label, col, i, t0, t1, hold=2):
    a.add(travel(a, pkt(a, label, col, size=14, h=28), [(LANE - 50, 212), (LANE - 50, ry(i) + 19)], t0, t1, hold=hold))


# 1. IKE
descend("UDP 500", a.CYAN, 3, 2, 9)
hl(3, 9, 18, MINT)
a.add(travel(a, pkt(a, "UDP 500", a.OK, size=14, h=28), [(LX + LW + 20, ry(3) + 19), (BX + 60, 306)], 12, 17, hold=1))
# 2. UDP 4500 y ESP
descend("UDP 4500", a.CYAN, 3, 27, 34)
hl(3, 34, 40, MINT)
descend("ESP", a.BLUE, 4, 38, 46)
hl(4, 46, 50, MINT)
a.add(during(a, a.text(BX, 456, "ESP: solo si no hay", 15, a.BLUE, a.SANS, 600) + a.text(BX, 478, "NAT en el medio", 15, a.BLUE, a.SANS, 600), 38, 50))
# 3. UDP 1701 descifrado
a.add(travel(a, pkt(a, "UDP 1701", a.OK, size=14, h=28), [(LX + LW - 60, 212), (LANE - 50, 212), (LANE - 50, ry(3) + 19)], 52, 62, hold=2))
hl(3, 62, 74, MINT, still=1)
a.add(during(a, a.text(BX, 456, "descifrado, pero vuelve", 15, a.OK, a.SANS, 600) + a.text(BX, 478, "a pasar por input", 15, a.OK, a.SANS, 600), 54, 75, still=1))
a.add(still_only(a, place(pkt(a, "UDP 1701", a.OK, size=14, h=28), LANE - 50, ry(3) + 19)))
# 4. reglas debajo del drop
descend("UDP 500", a.CYAN, 3, 82, 88, hold=8)
hl(3, 88, 100, ROSE)
a.add(during(a, xmark(a, LANE, ry(3) + 19), 89, 100))
a.add(during(a, a.text(BX, 456, "el drop corta antes:", 15, a.BAD, a.SANS, 600) + a.text(BX, 478, "las nuevas no se miran", 15, a.BAD, a.SANS, 600), 80, 100))

a.add(term(a, 48, 556, 1104, [
    'chain=input protocol=udp dst-port=500,4500,1701 action=accept comment="L2TP IPsec"',
    'chain=input protocol=ipsec-esp action=accept comment="ESP"',
    'place-before=[find comment="defconf: drop all not coming from LAN"]',
], size=15, colors={2: GOLD}))

write(a, 21, "l1", "Lo que ve input cuando un cliente conecta",
      "Animación en cuatro tiempos sobre la cadena input del MikroTik, que se lee de arriba hacia abajo: accept established, related y untracked; drop invalid; accept ICMP; "
      "la regla nueva L2TP IPsec (UDP 500, 4500 y 1701, accept); la regla nueva ESP (protocol=ipsec-esp, accept) y, al final, defconf: drop all not coming from LAN. "
      "1: llega IKE por UDP 500; como es nuevo, baja por la lista hasta la regla L2TP IPsec, que lo acepta, y llega al proceso IKE del router. "
      "2: con NAT en el medio todo sigue por UDP 4500, que acepta la misma regla; sin NAT, los datos llegan en ESP y los acepta la regla ESP. "
      "3: el router descifra y el L2TP por UDP 1701 vuelve a entrar a input; la regla L2TP IPsec también lo acepta. "
      "4: si las dos reglas nuevas quedan debajo del drop, el UDP 500 llega primero al drop y se descarta: las reglas nuevas nunca se miran y el cliente no conecta. "
      "Por eso se agregan con place-before=[find comment=\"defconf: drop all not coming from LAN\"].",
      [6, 14, 32, 44, 58, 66, 84, 94])
