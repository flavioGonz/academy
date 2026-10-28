#!/usr/bin/env python3
"""Lección 22 · IPsec entre marcas · Resumen ("Cómo se ve en la red").
La falla típica con fase 1 y 2 arriba: el masquerade cambia el origen antes de que se mire la policy, y FastTrack
saltea la policy en los paquetes siguientes. Con las reglas de bypass, el paquete entra cifrado.
"""
from _anim_mk_32_39 import *

a = Anim(T=28, kicker="MIKROTIK · IPSEC ENTRE MARCAS · CÓMO SE VE EN LA RED", title="Túnel arriba y no pasa nada: dónde se escapa")
a.steps([
    "Fases 1 y 2 arriba. La PC hace ping a 10.10.10.5: pasa forward y llega a srcnat.",
    "El masquerade pone 203.0.113.10. La policy ya no coincide: sale sin cifrar y se pierde.",
    "Con \"no NAT al tunel\" arriba de todo, el origen queda: coincide y sale cifrado en ESP.",
    "FastTrack saltea la policy en los paquetes que siguen. El accept en forward lo evita.",
], still=2, size=17)

PY = 394   # carril del paquete
RX, RY, RW, RH = 230, 172, 610, 252
a.add(a.box(RX, RY, RW, RH, a.INK, rx=18))
a.add(a.text(RX + 20, RY + 28, "Sitio A · MikroTik · 203.0.113.10", 16, a.WHITE, a.SANS, 600))
a.add(a.text(RX + RW - 20, RY + 28, "orden →", 15, SKY, a.MONO, 400, "end"))
ST = [(248, "forward"), (448, "srcnat"), (648, "policy")]
for x, n in ST:
    a.add(a.box(x, RY + 44, 176, 194, a.NAVY2, rx=12))
    a.add(a.text(x + 14, RY + 70, n, 17, a.WHITE, a.MONO, 600))
a.add(line(RX + 10, PY, RX + RW - 10, PY, "#2E5C86", 3, "5 7"))
# forward
a.add(during(a, a.text(262, RY + 100, "accept túnel", 15, MINT, a.MONO, 600), 86, 100))
a.add(a.text(262, RY + 128, "fasttrack-", 15, SOFTW, a.MONO))
a.add(a.text(262, RY + 150, "connection", 15, SOFTW, a.MONO))
# srcnat
a.add(during(a, a.text(462, RY + 100, "accept", 15, MINT, a.MONO, 600) + a.text(462, RY + 122, "no NAT al tunel", 15, MINT, a.MONO, 600), 52, 100, still=1))
a.add(a.text(462, RY + 150, "masquerade", 15, SOFTW, a.MONO))
# policy
a.add(a.text(662, RY + 100, "src 192.168.88.0/24", 14, SOFTW, a.MONO))
a.add(a.text(662, RY + 122, "dst 10.10.10.0/24", 14, SOFTW, a.MONO))
a.add(a.text(662, RY + 150, "→ encrypt", 15, GOLD, a.MONO, 600))
# resaltados
a.add(during(a, a.box(444, RY + 40, 184, 202, "none", ROSE, rx=14, sw=3.5), 27, 37))
a.add(during(a, a.box(644, RY + 40, 184, 202, "none", ROSE, rx=14, sw=3.5), 37, 45))
a.add(during(a, a.pill(736, RY + 172, "no coincide", a.BAD, a.BADBG, 14, 26, "middle"), 37, 50))
a.add(during(a, a.box(444, RY + 40, 184, 202, "none", MINT, rx=14, sw=3.5), 53, 61))
a.add(during(a, a.box(644, RY + 40, 184, 202, "none", MINT, rx=14, sw=3.5), 61, 72, still=1))
a.add(during(a, a.pill(736, RY + 172, "coincide", a.OK, a.OKBG, 14, 26, "middle"), 61, 75, still=1))
a.add(during(a, a.box(244, RY + 40, 184, 202, "none", ROSE, rx=14, sw=3.5), 76, 85))
a.add(during(a, a.box(244, RY + 40, 184, 202, "none", MINT, rx=14, sw=3.5), 86, 100))

# extremos
a.add(dev(a, 48, PY - 46, 168, 92, "PC", "192.168.88.20", "laptop", tsize=17))
a.add(router(a, 900, RY, 252, 120, "Sitio B", "198.51.100.20", "LAN 10.10.10.0/24"))
a.add(dev(a, 900, 352, 252, 82, "Servidor", "10.10.10.5", "server", tsize=17))
a.add(line(840, PY, 900, PY, a.LINE, 3, "5 7"))
# salida sin cifrar
a.add(poly([(820, PY), (860, 458)], a.BAD, 3, "6 6"))
a.add(a.text(890, 464, "internet sin cifrar:", 15, a.BAD, a.SANS, 600))
a.add(a.text(890, 486, "origen privado o equivocado", 15, a.BAD, a.SANS, 600))

# 1 y 2: sin bypass
a.add(travel(a, pkt(a, "ping", a.CYAN, size=14, h=28), [(200, PY), (440, PY)], 2, 12, hold=14))
a.add(travel(a, pkt(a, "ping", a.AMB, size=14, h=28), [(440, PY), (640, PY)], 28, 34, hold=3))
a.add(travel(a, pkt(a, "ping", a.BAD, size=14, h=28), [(640, PY), (820, PY), (860, 458)], 40, 46, hold=3))
a.add(during(a, xmark(a, 860, 458), 46, 50))
# 3: con bypass de NAT
a.add(travel(a, pkt(a, "ping", a.CYAN, size=14, h=28), [(200, PY), (640, PY)], 51, 59, hold=2))
a.add(travel(a, pkt(a, "ESP", a.BLUE, size=14, h=28), [(780, PY), (1030, PY)], 62, 68, hold=1))
a.add(during(a, check(a, 1126, 370), 68, 75, still=1))
a.add(still_only(a, place(pkt(a, "ESP", a.BLUE, size=14, h=28), 870, PY)))
# 4: FastTrack
for t in (76, 80):
    a.add(travel(a, pkt(a, "ping", a.BAD, size=14, h=28), [(200, PY), (300, PY), (300, 458), (820, 458), (860, 458)], t, t + 4, hold=0.5))
a.add(during(a, poly([(300, PY + 14), (300, 458), (840, 458)], a.BAD, 3, "6 6"), 76, 86))
a.add(during(a, a.text(560, 490, "atajo de FastTrack: no mira la policy", 15, a.BAD, a.SANS, 600, "middle"), 76, 86))
a.add(travel(a, pkt(a, "ping", a.CYAN, size=14, h=28), [(200, PY), (640, PY)], 88, 93, hold=0.5))
a.add(travel(a, pkt(a, "ESP", a.BLUE, size=14, h=28), [(780, PY), (1030, PY)], 94, 97, hold=3))

# cabecera
HY = 520
a.add(a.box(48, HY, 1104, 64, a.WHITE, a.LINE, rx=14))
HDR = [
    (0, 25, "de 192.168.88.20 a 10.10.10.5", "todavía sin tocar", a.INK, 0),
    (25, 50, "de 203.0.113.10 a 10.10.10.5", "masquerade: la policy pide 192.168.88.0/24", a.BAD, 0),
    (50, 75, "de 192.168.88.20 a 10.10.10.5", "coincide: viaja en ESP de 203.0.113.10 a 198.51.100.20", a.OK, 1),
    (75, 86, "de 192.168.88.20 a 10.10.10.5", "\"se arregla con Torch\": es FastTrack", a.AMB, 0),
    (86, 100, "de 192.168.88.20 a 10.10.10.5", "con el accept en forward, todos pasan por la policy", a.OK, 0),
]
for s_, e, h1, h2, col, st in HDR:
    a.add(during(a, a.text(72, HY + 40, h1, 18, a.INK, a.MONO, 600) + a.text(1128, HY + 40, h2, 16, col, a.SANS, 600, "end"), s_, e, still=st))
a.add(a.text(48, 626, 'srcnat accept "no NAT al tunel" place-before=0  ·  forward accept arriba de fasttrack-connection', 16, a.TXT, a.MONO))

write(a, 22, "r1", "Túnel arriba y no pasa nada: dónde se escapa",
      "Animación en cuatro tiempos dentro del MikroTik del sitio A (203.0.113.10), con tres etapas en orden: forward (con fasttrack-connection), srcnat (con masquerade) y la policy de IPsec "
      "(src 192.168.88.0/24, dst 10.10.10.0/24, encrypt), y el sitio B 198.51.100.20 con el servidor 10.10.10.5. "
      "1: con las fases 1 y 2 arriba, la PC 192.168.88.20 hace ping a 10.10.10.5; pasa forward y llega a srcnat. "
      "2: el masquerade cambia el origen a 203.0.113.10; cuando se mira la policy, ya no coincide con 192.168.88.0/24, el paquete sale sin cifrar a internet y se pierde. "
      "3: con la regla srcnat accept \"no NAT al tunel\" arriba de todo, el origen queda 192.168.88.20, la policy coincide y el paquete viaja cifrado en ESP de 203.0.113.10 a 198.51.100.20 hasta el servidor. "
      "4: con FastTrack sin bypass, los paquetes siguientes de la conexión toman el atajo y no miran la policy: se escapan sin cifrar; el síntoma es que se arregla con Torch. "
      "Una regla accept para el túnel en forward, arriba de fasttrack-connection, lo evita.",
      [6, 30, 42, 56, 66, 80, 95])
