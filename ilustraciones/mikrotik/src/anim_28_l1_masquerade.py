#!/usr/bin/env python3
"""Lección 28 · L2TP saliente · Laboratorio paso 5: masquerade hacia el túnel cuando no podés tocar el otro extremo.
El origen pasa a ser 10.255.1.2, la central contesta a esa IP y el hAP deshace el cambio; la contra: desde allá no se puede iniciar.
"""
from _anim_mk_32_39 import *

a = Anim(T=26, kicker="MIKROTIK · L2TP SALIENTE · PASO 5", title="Masquerade al túnel: la central ve solo 10.255.1.2")
a.steps([
    "La PC hace ping a 10.10.1.1. Sale por l2tp-central y el masquerade pone 10.255.1.2.",
    "La central lo entrega con origen 10.255.1.2: la otra punta del túnel, que ya conoce.",
    "La respuesta vuelve a 10.255.1.2 por el túnel; el hAP deshace el cambio y llega a la PC.",
    "La contra: desde la central nadie puede abrir una conexión a 192.168.88.50.",
], still=2, size=17)

Y, H = 236, 104
CY = Y + H / 2
LANE = 362
a.add(a.box(540, CY - 20, 230, 40, a.OK, a.OK, rx=20, sw=2, extra='fill-opacity=".14"'))
a.add(a.text(655, CY - 30, "túnel L2TP/IPsec", 15, a.OK, a.MONO, 600, "middle"))
a.add(line(238, CY, 290, CY, a.LINE, 3, "5 7"))
a.add(line(960, CY, 1000, CY, a.LINE, 3, "5 7"))
a.add(dev(a, 48, Y, 190, H, "PC", "192.168.88.20", "laptop", sub2="sucursal", tsize=17))
a.add(router(a, 290, Y, 250, H, "hAP sucursal", "l2tp-central", "10.255.1.2"))
a.add(router(a, 770, Y, 190, H, "Central", "10.255.1.1", "no la tocás"))
a.add(dev(a, 1000, Y, 152, H, "Servidor", "10.10.1.1", "server", tsize=17))

# regla de NAT
a.add(term(a, 290, 388, 470, ["/ip/firewall/nat/add chain=srcnat", "out-interface=l2tp-central", "action=masquerade"], size=15, lh=22))
a.add(during(a, a.box(286, 384, 478, 94, "none", GOLD, rx=14, sw=3), 6, 14))
a.add(during(a, a.box(286, 384, 478, 94, "none", GOLD, rx=14, sw=3), 50, 58))
# la central sin ruta
a.add(a.box(800, 388, 352, 90, a.WHITE, a.LINE, rx=12))
a.add(a.text(818, 416, "tabla de la central", 15, a.GREY, a.MONO))
a.add(a.text(818, 442, "10.255.1.2/32 · el túnel", 15, a.OK, a.MONO, 600))
a.add(a.text(818, 466, "192.168.88.0/24 · no hay", 15, a.BAD, a.MONO, 600))
a.add(during(a, a.box(796, 384, 360, 98, "none", a.OK, rx=14, sw=3), 26, 40))
a.add(during(a, a.box(796, 384, 360, 98, "none", a.BAD, rx=14, sw=3), 80, 100))

# paquetes
a.add(travel(a, pkt(a, "ping", a.CYAN, size=14, h=28), [(200, LANE), (330, LANE)], 1, 5, hold=1))
a.add(travel(a, pkt(a, "ping", a.CYAN, size=14, h=28), [(560, CY), (750, CY)], 9, 15, hold=1))
a.add(travel(a, pkt(a, "ping", a.CYAN, size=14, h=28), [(960, LANE), (1076, LANE)], 27, 31, hold=3))
a.add(travel(a, pkt(a, "eco", a.OK, size=14, h=28), [(1076, LANE), (960, LANE)], 51, 54, hold=0.5))
a.add(travel(a, pkt(a, "eco", a.OK, size=14, h=28), [(750, CY), (560, CY)], 55, 61, hold=1))
a.add(travel(a, pkt(a, "eco", a.OK, size=14, h=28), [(330, LANE), (200, LANE)], 64, 68, hold=4))
a.add(during(a, check(a, 214, Y + 22), 69, 100, still=1))
a.add(still_only(a, place(pkt(a, "eco", a.OK, size=14, h=28), 655, CY)))
# la contra
a.add(travel(a, pkt(a, "→ 192.168.88.50", a.BAD, size=14, h=28), [(1076, LANE), (990, LANE)], 77, 81, hold=8))
a.add(during(a, xmark(a, 880, LANE), 82, 100))

# cabecera
PY = 494
a.add(a.box(48, PY, 1104, 88, a.WHITE, a.LINE, rx=14))
a.add(a.text(72, PY + 30, "tramo", 15, a.GREY, a.MONO))
a.add(a.text(420, PY + 30, "origen", 15, a.GREY, a.MONO))
a.add(a.text(760, PY + 30, "destino", 15, a.GREY, a.MONO))
HDR = [
    (0, 8, "PC → hAP", "192.168.88.20", "10.10.1.1", a.INK, 0),
    (8, 25, "por el túnel", "10.255.1.2", "10.10.1.1", a.AMB, 0),
    (25, 50, "central → servidor", "10.255.1.2", "10.10.1.1", a.AMB, 0),
    (50, 63, "vuelta por el túnel", "10.10.1.1", "10.255.1.2", a.OK, 0),
    (63, 75, "hAP → PC", "10.10.1.1", "192.168.88.20", a.OK, 1),
    (75, 100, "desde la central", "10.10.1.1", "192.168.88.50 · sin ruta", a.BAD, 0),
]
for s_, e, tr, o, d, col, st in HDR:
    a.add(during(a, a.text(72, PY + 66, tr, 18, a.INK, a.SANS, 600) + a.text(420, PY + 66, o, 19, col, a.MONO, 600)
                 + a.text(760, PY + 66, d, 19, col, a.MONO, 600), s_, e, still=st))
narr(a, 48, 628, [
    (0, 50, "Para la central, todo lo de la sucursal es una sola IP: 10.255.1.2.", a.TXT, 0),
    (50, 75, "Sirve cuando no podés agregar la ruta de vuelta en el otro extremo.", a.OK, 1),
    (75, 100, "Para entrar desde allá hace falta la ruta del paso 1 en la central.", a.BAD, 0),
])

write(a, 28, "l1", "Masquerade al túnel: la central ve solo 10.255.1.2",
      "Animación en cuatro tiempos con una PC 192.168.88.20 de la sucursal, el hAP con la interfaz l2tp-central 10.255.1.2, el túnel L2TP/IPsec, la central 10.255.1.1 que no podés tocar y un servidor 10.10.1.1. "
      "En el hAP está la regla /ip/firewall/nat/add chain=srcnat out-interface=l2tp-central action=masquerade. "
      "1: la PC hace ping a 10.10.1.1; el hAP lo manda por l2tp-central y el masquerade cambia el origen a 10.255.1.2. "
      "2: la central lo entrega al servidor con origen 10.255.1.2, una dirección que conoce porque es la otra punta del túnel. "
      "3: la respuesta vuelve a 10.255.1.2 por el túnel, el hAP deshace el cambio y el eco llega a la PC. "
      "4: la contra: desde la central nadie puede abrir una conexión a 192.168.88.50, porque la central no tiene ruta a 192.168.88.0/24; para eso hace falta la ruta del paso 1.",
      [4, 12, 30, 58, 66, 88])
