#!/usr/bin/env python3
"""Caso de estudio · Audio en un sentido · Laboratorio, paso 8: 21-l2.svg.
La otra firma de la troncal (H2): el SDP de Antel trae en la c= una red de audio que no está en Static Routes
(ejemplo 198.51.100.70, red 198.51.100.64/26). La UCM busca ruta, cae en la de por defecto y manda su RTP por LAN2
al router del cliente: el de afuera no oye a la oficina. Se ve capturando en LAN2. Arreglo: ruta estática por LAN1.
Datos de ejemplo (señalización de Antel 203.0.113.0/24, ruta estática de la lección Troncal SIP de Antel).
"""
from _anim_gs_red import R

g = R(T=26, fix=94, kicker="GRANDSTREAM · CASO DE ESTUDIO · PASO 8", title="Cuando el audio de la central sale por otra boca")
g.steps([
    "El SDP de Antel pide el audio en 198.51.100.70, otra red que la de señalización.",
    "La UCM busca ruta: esa red no está en Static Routes y va la de por defecto, LAN2.",
    "Su RTP sale por el router del cliente y no llega: el de afuera no oye. Se ve en LAN2.",
    "Ruta estática a 198.51.100.64/26 por LAN1: el audio sale por la troncal.",
], size=17)

B, OK, BAD, GREY, INK, CY = g.BLUE, g.OK, g.BAD, g.GREY, g.INK, g.CYAN
NY = 182
g.add(g.box(36, NY - 16, 300, 196, "none", CY, rx=16, sw=2, extra='stroke-dasharray="7 6"'))
g.add(g.text(56, NY + 4, "red privada de Antel", 14, CY, g.MONO))
g.add(g.dev(56, NY + 18, 260, 66, "Servidor SIP", "203.0.113.10", icon="antel"))
g.add(g.dev(56, NY + 100, 260, 66, "Audio de Antel", "198.51.100.70", icon="antel", hl=g.AMB))
g.add(g.box(430, NY, 340, 200, g.INK, rx=16))
g.add(g.text(450, NY + 32, "UCM6300 · tabla de rutas", 19, g.WHITE, g.HEAD, 600))
g.add(g.text(450, NY + 70, "203.0.113.0/24 → LAN1", 15, "#D9E9F8", g.MONO, 600))
g.add(g.text(450, NY + 100, "default → 192.168.88.1 · LAN2", 15, "#D9E9F8", g.MONO, 600))
g.appear(g.text(450, NY + 130, "198.51.100.64/26 → LAN1", 15, "#9BE7C4", g.MONO, 600), 78, 100)
g.appear(g.box(440, NY + 80, 320, 30, "none", BAD, rx=8, sw=2.5), 28, 76, still=0)
g.appear(g.box(440, NY + 110, 320, 30, "none", OK, rx=8, sw=2.5), 78, 100)
g.add(g.text(450, NY + 182, "LAN1", 14, CY, g.MONO, 600) + g.text(750, NY + 182, "LAN2", 14, CY, g.MONO, 600, "end"))
g.add(g.dev(882, NY + 60, 270, 78, "Router del cliente", "192.168.88.1", icon="router"))
g.add(g.wire(316, NY + 133, 430, NY + 133, w=4))
g.add(g.wire(770, NY + 99, 882, NY + 99, w=4))

# 1 · SDP de Antel
g.appear(g.term(48, 408, 520, 84, "SDP de Antel (200 OK)", [("c=IN IP4 198.51.100.70", "#F6C35B")]), 3, 100)
g.token([(316, NY + 133), (430, NY + 133)], 4, 11, g.chip("200 OK", bg=B, size=13, h=24))
# 3 · el RTP de la UCM sale por LAN2
for t0 in (54, 61, 68):
    g.token([(770, NY + 99), (882, NY + 99)], t0, t0 + 3, g.chip("RTP", bg=BAD, size=12, h=22), hold=t0 + 3.5)
g.appear(g.mark(1017, NY + 166, False, 14), 56, 76, still=0)
g.appear(g.text(1017, NY + 200, "por internet no llega", 15, BAD, g.SANS, 600, "middle"), 56, 76, still=0)
g.appear(g.term(612, 408, 540, 84, "Ethernet Capture · LAN2 · udp portrange 10000-20000", [("RTP 192.168.88.20 → 198.51.100.70", "#FFB4A8")]), 58, 76, still=0)
# 4 · con la ruta
for t0 in (84, 90):
    g.token([(430, NY + 133), (316, NY + 133)], t0, t0 + 3, g.chip("RTP", bg=OK, size=12, h=22))
g.appear(g.term(612, 408, 540, 84, "Static Routes · Add IPv4 Static Route", [("198.51.100.64/26 gw 198.51.100.1 · LAN1", "#9BE7C4")]), 78, 100)
g.fijo_only(f'<g transform="translate(373 {NY + 133})">' + g.chip("RTP", bg=OK, size=12, h=22) + "</g>")

g.add(g.box(48, 516, 1104, 110, g.WHITE, g.LINE, rx=14))
ROWS = [(0, 25, "La c= de Antel dice adónde mandarle el audio: puede no ser la red del servidor SIP", "pedile a Antel todas sus redes de señalización y de audio", INK),
        (25, 50, "Sin ruta estática para esa red, la UCM usa la de por defecto", "default → 192.168.88.1 por LAN2, el router del cliente", BAD),
        (50, 76, "La oficina oye al de afuera; el de afuera no oye a la oficina", "es el sentido contrario al caso de la c= de la UCM", BAD),
        (76, 100, "Esa red a Static Routes por LAN1 y a Local Network Address", "verificá con la captura en LAN1: dos flujos", OK)]
for t0, t1, a, b, col in ROWS:
    g.appear(g.text(72, 556, a, 17, INK, g.SANS, 600) + g.text(72, 592, b, 16, col, g.SANS, 600), t0, t1)

g.done(21, "l2", "Cuando el audio de la central sale por otra boca",
       "Animación en cuatro tiempos. A la izquierda, en la red privada de Antel, el servidor SIP 203.0.113.10 y el audio de Antel en 198.51.100.70; al medio la tabla de rutas de la UCM, con 203.0.113.0/24 por LAN1 y la ruta por defecto a 192.168.88.1 por LAN2; a la derecha el router del cliente. "
       "1: el 200 OK de Antel trae en su SDP c=IN IP4 198.51.100.70, una red distinta de la de señalización. "
       "2: la UCM busca ruta para esa dirección, no la encuentra en Static Routes y usa la de por defecto, por LAN2. "
       "3: su RTP sale por el router del cliente hacia internet y no llega a Antel: la oficina oye al de afuera y el de afuera no oye a la oficina, el sentido contrario al caso de la c= de la UCM; capturando en LAN2 con udp portrange 10000-20000 se ve el RTP de 192.168.88.20 a 198.51.100.70. "
       "4: con una ruta estática a 198.51.100.64/26 por el gateway 198.51.100.1 y LAN1, y esa red en Local Network Address, el audio sale por la troncal. Datos de ejemplo.",
       [8, 20, 34, 46, 60, 70, 86, 95])
