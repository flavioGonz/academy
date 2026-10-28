#!/usr/bin/env python3
"""Lección 21 · L2TP con IPsec · Laboratorio paso 6: diagnóstico por capas.
active-peers dice si IPsec armó; /ppp/active, si L2TP y PPP llegaron hasta el final; el log, dónde se cortó.
"""
from _anim_mk_32_39 import *

a = Anim(T=28, kicker="MIKROTIK · L2TP CON IPSEC · PASO 6", title="Dos comandos dicen en qué capa se cortó")
a.steps([
    "Clave IPsec mal o UDP 500/4500 cerrado: IPsec no arma y active-peers queda vacío.",
    "IPsec arma, pero PPP rechaza usuario o contraseña: hay peer y /ppp/active, vacío.",
    "Todo bien: el peer establecido y la sesión de encargado con su IP del pool.",
    "El log con topics ipsec y l2tp cuenta lo mismo con detalle: leelo de afuera hacia adentro.",
], still=2, size=17)

a.add(dev(a, 48, 182, 200, 84, "Notebook", "198.51.100.7", "laptop", tsize=17))
a.add(router(a, 360, 182, 200, 84, "MikroTik", "203.0.113.10"))
a.add(line(248, 224, 360, 224, a.LINE, 3, "5 7"))

BARS = [("IPsec", "UDP 500/4500, ESP", 300), ("L2TP", "UDP 1701", 364), ("PPP", "usuario, clave, IP", 428)]
BX0, BW = 48, 512
for name, sub, y in BARS:
    a.add(a.box(BX0, y, BW, 48, a.SLATE, a.LINE, rx=24))
    a.add(a.text(BX0 + 22, y + 30, name, 17, a.INK, a.SANS, 600))
    a.add(a.text(BX0 + 92, y + 30, sub, 15, a.GREY, a.MONO))


def state(y, col, bg, t0, t1, label, still=0):
    a.add(during(a, a.box(BX0, y, BW, 48, bg, col, rx=24, sw=2.5)
                 + a.text(BX0 + 22, y + 30, [n for n, s_, yy in BARS if yy == y][0], 17, col, a.SANS, 600)
                 + a.text(BX0 + BW - 20, y + 30, label, 15, col, a.MONO, 600, "end"), t0, t1, still=still))


def attempt(y, t0, t1, col):
    a.add(travel(a, dot(a, col, 9), [(BX0 + 150, y + 24), (BX0 + BW - 150, y + 24)], t0, t1, hold=0.5))


# caso 1: IPsec no arma
attempt(300, 2, 8, a.BAD)
state(300, a.BAD, a.BADBG, 9, 25, "no arma")
# caso 2: IPsec y L2TP arriba, PPP rechaza
attempt(300, 27, 30, a.OK)
state(300, a.OK, a.OKBG, 30, 50, "arriba")
attempt(364, 31, 34, a.OK)
state(364, a.OK, a.OKBG, 34, 50, "arriba")
attempt(428, 35, 38, a.BAD)
state(428, a.BAD, a.BADBG, 38, 50, "rechazado")
# caso 3: todo arriba
for k, y in enumerate((300, 364, 428)):
    attempt(y, 52 + k * 3, 55 + k * 3, a.OK)
    state(y, a.OK, a.OKBG, 55 + k * 3, 100, "arriba", still=1)
a.add(during(a, a.pill(304, 500, "conectado · 192.168.89.10", a.OK, a.OKBG, 15, 30, "middle"), 62, 100, still=1))
a.add(during(a, a.pill(304, 500, "no conecta", a.BAD, a.BADBG, 15, 30, "middle"), 9, 25))
a.add(during(a, a.pill(304, 500, "no conecta", a.BAD, a.BADBG, 15, 30, "middle"), 38, 50))

# terminales a la derecha
TX, TW = 600, 552


def tbox(y, cmd):
    a.add(a.box(TX, y, TW, 90, a.INK, rx=12))
    a.add(a.text(TX + 18, y + 32, cmd, 15, a.WHITE, a.MONO))


def out(y, txt, col, t0, t1, still=0):
    a.add(during(a, a.text(TX + 18, y + 66, txt, 15, col, a.MONO, 600), t0, t1, still=still))


tbox(182, "/ip/ipsec/active-peers/print")
tbox(286, "/ppp/active/print")
tbox(390, '/log/print where topics~"ipsec|l2tp"')
out(182, "(vacío)", ROSE, 9, 25)
out(182, "remote-address=198.51.100.7 state=established", MINT, 30, 50)
out(182, "remote-address=198.51.100.7 state=established", MINT, 55, 100, still=1)
out(286, "(vacío)", ROSE, 9, 25)
out(286, "(vacío)", ROSE, 38, 50)
out(286, "encargado  l2tp  192.168.89.10", MINT, 61, 100, still=1)
out(390, "# en qué capa se cortó y por qué", GOLD, 76, 100)
a.add(during(a, a.box(TX - 4, 386, TW + 8, 98, "none", GOLD, rx=14, sw=3.5), 76, 100))
a.add(during(a, a.box(TX - 4, 178, TW + 8, 98, "none", ROSE, rx=14, sw=3.5), 9, 25))
a.add(during(a, a.box(TX - 4, 282, TW + 8, 98, "none", ROSE, rx=14, sw=3.5), 38, 50))

# lectura
a.add(a.box(TX, 500, TW, 96, a.WHITE, a.LINE, rx=12))
VER = [
    (0, 25, "sin peer → IPsec: ipsec-secret, UDP 500/4500, NAT-T", a.BAD, 0),
    (25, 50, "peer sí, sesión no → UDP 1701 o el /ppp/secret", a.AMB, 0),
    (50, 75, "peer y sesión → conectado; si no llega a la LAN, forward", a.OK, 1),
    (75, 100, "orden: IPsec, después L2TP, al final PPP", a.INK, 0),
]
a.add(a.text(TX + 18, 530, "cómo se lee", 15, a.GREY, a.MONO))
for t0, t1, txt, col, st in VER:
    a.add(during(a, a.text(TX + 18, 566, txt, 16, col, a.SANS, 600), t0, t1, still=st))
narr(a, 48, 640, [
    (0, 50, "Cada comando mira una capa. Si una no armó, las de adentro tampoco.", a.TXT, 0),
    (50, 100, "Si Windows no conecta y el celular sí, mirá active-peers: casi siempre es NAT-T (paso 5).", a.TXT, 1),
])

write(a, 21, "l2", "Dos comandos dicen en qué capa se cortó",
      "Animación en cuatro tiempos con una notebook 198.51.100.7 que se conecta al MikroTik 203.0.113.10, tres barras de capas (IPsec por UDP 500 y 4500 con ESP, L2TP por UDP 1701 y PPP con usuario, clave e IP) "
      "y tres comandos: /ip/ipsec/active-peers/print, /ppp/active/print y /log/print where topics~\"ipsec|l2tp\". "
      "1: con la clave IPsec mal o los puertos 500 y 4500 cerrados, IPsec no arma; active-peers y /ppp/active quedan vacíos: hay que mirar ipsec-secret, puertos y NAT-T. "
      "2: IPsec y L2TP arman, pero PPP rechaza usuario o contraseña; active-peers muestra la notebook establecida y /ppp/active sigue vacío: mirar UDP 1701 o el /ppp/secret. "
      "3: todo arriba: el peer establecido y la sesión de encargado por l2tp con 192.168.89.10. "
      "4: el log con topics ipsec y l2tp cuenta lo mismo con el motivo; se lee de afuera hacia adentro: IPsec, después L2TP y al final PPP.",
      [5, 20, 33, 45, 58, 70, 88])
