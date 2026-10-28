#!/usr/bin/env python3
"""Lección 10 · NVR con criterio · Laboratorio paso 4: la prueba desde el celular con datos móviles.
Fuera de la lista el SYN se descarta y se reintenta sin respuesta; con la IP en nvr-permitidos, el contador sube y conecta.
"""
from _anim_mk_32_39 import *

a = Anim(T=24, kicker="MIKROTIK · NVR CON CRITERIO · PASO 4", title="La prueba del celular: primero no, después sí")
a.steps([
    "El celular manda un SYN al 8000. No está en la lista: no hay dst-nat, input lo tira.",
    "El celular reintenta el SYN. Nunca vuelve un SYN-ACK: la app dice que no conecta.",
    "Agregás la IP pública del celular a nvr-permitidos.",
    "Nuevo intento: la regla coincide, el contador sube a 1 y el NVR contesta.",
], still=3, size=17)

LY = 420
RX, RY, RW, RH = 360, 176, 480, 300
a.add(a.box(RX, RY, RW, RH, a.INK, rx=18))
a.add(a.text(RX + 20, RY + 30, "MikroTik · 203.0.113.10", 17, a.WHITE, a.SANS, 600))
# address-list
a.add(a.box(RX + 20, 214, RW - 40, 88, a.NAVY2, rx=12))
a.add(a.text(RX + 38, 240, "address-list nvr-permitidos", 15, SKY, a.MONO))
a.add(a.text(RX + 38, 266, "203.0.113.25   central", 15, a.WHITE, a.MONO))
a.add(during(a, a.text(RX + 38, 290, "198.51.100.77  celular", 15, MINT, a.MONO, 600), 56, 100, still=1))
a.add(during(a, a.box(RX + 16, 210, RW - 32, 96, "none", MINT, rx=14, sw=3.5), 56, 72))
# regla
a.add(a.box(RX + 20, 314, RW - 40, 64, a.NAVY2, rx=12))
a.add(a.text(RX + 38, 340, "dstnat · dst-port=8000", 15, a.WHITE, a.MONO))
a.add(a.text(RX + 38, 364, "src-address-list=nvr-permitidos", 15, GOLD, a.MONO, 600))
a.add(during(a, a.pill(RX + RW - 30, 324, "contador 0", SOFTW, "#14496F", 14, 26, "end"), 0, 80))
a.add(during(a, a.pill(RX + RW - 30, 324, "contador 1", a.INK, GOLD, 14, 26, "end"), 80, 100, still=1))
a.add(wins(a, a.box(RX + 16, 310, RW - 32, 72, "none", ROSE, rx=14, sw=3.5), [(6, 12), (30, 34), (40, 44)]))
a.add(during(a, a.box(RX + 16, 310, RW - 32, 72, "none", MINT, rx=14, sw=3.5), 79, 85))
# carril
a.add(line(298, LY, 930, LY, "#2E5C86", 3, "5 7"))
a.add(dev(a, 48, 370, 250, 100, "Celular", "198.51.100.77", "phone", sub2="datos móviles"))
a.add(dev(a, 930, 370, 222, 100, "NVR", "192.168.88.50", "server", sub2="TCP 8000"))

# 1. SYN descartado
a.add(travel(a, pkt(a, "SYN :8000", a.BAD), [(330, LY), (560, LY)], 2, 7, hold=5))
a.add(during(a, xmark(a, 640, LY) + a.pill(664, LY - 14, "input: drop", a.BAD, a.BADBG, 14, 28), 8, 24))
# 2. reintentos
for t in (27, 37):
    a.add(travel(a, pkt(a, "SYN otra vez", a.BAD), [(330, LY), (560, LY)], t, t + 4, hold=3))
    a.add(during(a, xmark(a, 640, LY) + a.pill(664, LY - 14, "input: drop", a.BAD, a.BADBG, 14, 28), t + 4, t + 8))
a.add(during(a, a.pill(173, 330, "no conecta", a.BAD, a.BADBG, 15, 30, "middle"), 30, 75))
# 4. con la IP en la lista
a.add(travel(a, pkt(a, "SYN :8000"), [(330, LY), (600, LY)], 76, 80, hold=3))
a.add(travel(a, pkt(a, "SYN :8000", a.OK), [(600, LY), (870, LY)], 83, 87, hold=1))
a.add(travel(a, pkt(a, "SYN-ACK", a.OK), [(870, LY), (330, LY)], 89, 95, hold=5))
a.add(during(a, a.pill(173, 330, "conecta", a.OK, a.OKBG, 15, 30, "middle"), 96, 100, still=1))
a.add(still_only(a, place(pkt(a, "SYN-ACK", a.OK), 600, LY)))

# terminal
a.add(term(a, 48, 500, 1104, [
    '/ip/firewall/nat/print stats where comment="NVR central"',
    "",
    "",
], title="TERMINAL DEL TÉCNICO"))
a.add(during(a, a.text(66, 580, '/ip/firewall/address-list/add list=nvr-permitidos address=198.51.100.77', 15, MINT, a.MONO, 600), 52, 100, still=1))
a.add(during(a, a.text(66, 604, 'comment="celular de prueba, borrar despues"', 15, MINT, a.MONO, 600), 52, 100, still=1))
narr(a, 48, 652, [
    (0, 50, "El SYN sigue dirigido al router: no hay nada publicado para esa IP.", a.BAD, 0),
    (50, 75, "Mientras la IP no esté en la lista, el contador de la regla no se mueve.", a.TXT, 0),
    (75, 100, "Solo el primer paquete de la conexión pasa por la regla: el contador cuenta conexiones.", a.OK, 1),
])

write(a, 10, "l1", "La prueba del celular: primero no, después sí",
      "Animación en cuatro tiempos con un celular con datos móviles que sale con la IP 198.51.100.77, el MikroTik 203.0.113.10 y el NVR 192.168.88.50 en TCP 8000. "
      "1: el celular manda un SYN a 203.0.113.10:8000; su IP no está en la address-list nvr-permitidos, la regla dstnat no se aplica, el paquete sigue dirigido al router e input lo descarta. El contador de la regla queda en 0. "
      "2: el celular reintenta el SYN y nunca recibe un SYN-ACK; la app dice que no conecta. "
      "3: el técnico agrega 198.51.100.77 a nvr-permitidos con /ip/firewall/address-list/add. "
      "4: en el nuevo intento la regla coincide, el contador sube a 1, el SYN llega al NVR y vuelve el SYN-ACK: conecta. "
      "El contador se mira con /ip/firewall/nat/print stats where comment=\"NVR central\" y cuenta conexiones, porque solo el primer paquete pasa por la regla.",
      [5, 20, 40, 62, 82, 93])
