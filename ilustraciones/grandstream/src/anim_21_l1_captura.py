#!/usr/bin/env python3
"""Caso de estudio · Audio en un sentido · Laboratorio, paso 5: 21-l1.svg.
La captura en LAN1 con la falla provocada: el INVITE de la UCM con c=IN IP4 192.0.2.10, RTP Streams con un solo
flujo (198.51.100.2 → 198.51.100.1) que Ctrl+R marca como flujo sin vuelta; con el arreglo, c=198.51.100.2 y dos flujos.
Wireshark: Telephony > RTP > RTP Streams, Ctrl+R = select all single streams. Puertos y cantidades de ejemplo.
"""
from _anim_gs_red import R

g = R(T=26, fix=94, kicker="GRANDSTREAM · CASO DE ESTUDIO · PASO 5", title="La captura que confirma H1")
g.steps([
    "Filtro sip || sdp: el INVITE que la UCM manda a Antel por LAN1.",
    "En su SDP, c=IN IP4 192.0.2.10: la IP pública. H1 confirmada.",
    "RTP Streams: un solo flujo, de la UCM a Antel. Ctrl+R lo marca: sin vuelta.",
    "Con el arreglo: c=IN IP4 198.51.100.2 y dos flujos, uno por sentido.",
], size=17)

B, OK, BAD, GREY, INK = g.BLUE, g.OK, g.BAD, g.GREY, g.INK
# paquetes
g.add(g.box(48, 170, 1104, 150, g.WHITE, g.LINE, rx=14))
g.add(g.text(68, 198, "Wireshark · filtro: sip || sdp", 15, B, g.MONO, 600))
hdr = ["Origen", "Destino", "Info"]
xs = [68, 290, 512]
for x, h in zip(xs, hdr):
    g.add(g.text(x, 226, h, 14, GREY, g.MONO, 600))
pk = [("198.51.100.2", "198.51.100.1", "INVITE sip:2001@198.51.100.1 · SDP"),
      ("198.51.100.1", "198.51.100.2", "200 OK · SDP"),
      ("198.51.100.2", "198.51.100.1", "ACK")]
for i, (a, b_, info) in enumerate(pk):
    y = 254 + i * 26
    g.add(g.text(xs[0], y, a, 15, INK, g.MONO) + g.text(xs[1], y, b_, 15, INK, g.MONO) + g.text(xs[2], y, info, 15, INK, g.MONO))
g.appear(g.box(58, 236, 1084, 26, "none", B, rx=6, sw=2.5), 4, 50, still=0)

# SDP del INVITE
g.add(g.box(48, 336, 520, 132, "#03213C", rx=14))
g.add(g.text(68, 364, "SDP del INVITE", 15, g.SKY, g.MONO))
g.add(g.text(68, 422, "m=audio 10044 RTP/AVP 8 0", 16, "#D9E9F8", g.MONO, 600))
g.appear(g.text(68, 394, "c=IN IP4 192.0.2.10", 17, "#FFB4A8", g.MONO, 600), 25, 76, still=0)
g.appear(g.text(68, 394, "c=IN IP4 198.51.100.2", 17, "#9BE7C4", g.MONO, 600), 76, 100)
g.appear(g.text(68, 452, "IP pública: Antel no llega", 15, "#FFB4A8", g.SANS, 600), 28, 76, still=0)
g.appear(g.text(68, 452, "la IP de LAN1: Antel llega", 15, "#9BE7C4", g.SANS, 600), 78, 100)

# RTP Streams
PX = 600
g.add(g.box(PX, 336, 552, 196, g.WHITE, g.LINE, rx=14))
g.add(g.text(PX + 20, 364, "Telephony > RTP > RTP Streams", 15, B, g.MONO, 600))
for x, h in zip((PX + 20, PX + 250, PX + 460), ("Origen", "Destino", "Paquetes")):
    g.add(g.text(x, 392, h, 14, GREY, g.MONO, 600))
row1 = g.text(PX + 20, 422, "198.51.100.2:10044", 15, INK, g.MONO) + g.text(PX + 250, 422, "198.51.100.1:10500", 15, INK, g.MONO) + g.text(PX + 460, 422, "1000", 15, INK, g.MONO)
row2 = g.text(PX + 20, 452, "198.51.100.1:10500", 15, INK, g.MONO) + g.text(PX + 250, 452, "198.51.100.2:10044", 15, INK, g.MONO) + g.text(PX + 460, 452, "1000", 15, INK, g.MONO)
g.appear(row1, 50, 100)
g.appear(g.text(PX + 20, 452, "(ningún flujo de vuelta)", 15, BAD, g.SANS, 600), 52, 76, still=0)
g.appear(g.box(PX + 10, 404, 532, 28, g.BADBG, rx=6), 62, 76, still=0)
g.appear(row1, 62, 76, still=0)
g.appear(g.pill(PX + 20, 480, "Ctrl+R: flujo sin vuelta", BAD, g.BADBG, 14, 28), 63, 76, still=0)
g.appear(row2, 80, 100)
g.appear(g.pill(PX + 20, 480, "dos flujos: audio de ida y vuelta", OK, g.OKBG, 14, 28), 82, 100)

# abajo
g.add(g.box(48, 552, 1104, 76, g.WHITE, g.LINE, rx=14))
ROWS = [(0, 25, "Captura en LAN1, la interfaz de la troncal: ahí están la señalización y el audio con Antel", INK),
        (25, 50, "La UCM le dice a Antel que mande el audio a 192.0.2.10", BAD),
        (50, 76, "Lo que se ve en el cable confirma el síntoma: la oficina no oye al de afuera", BAD),
        (76, 100, "La misma prueba que encontró la falla verifica el arreglo", OK)]
for t0, t1, s_, col in ROWS:
    g.appear(g.text(72, 598, s_, 17, col, g.SANS, 600), t0, t1)

g.done(21, "l1", "La captura que confirma H1",
       "Animación en cuatro tiempos con la captura en LAN1 abierta en Wireshark: arriba la lista de paquetes con el filtro sip || sdp, abajo a la izquierda el SDP del INVITE y a la derecha la ventana Telephony > RTP > RTP Streams. "
       "1: el INVITE que la UCM, 198.51.100.2, manda a Antel, 198.51.100.1, seguido del 200 OK y el ACK. "
       "2: en el SDP del INVITE, la línea c=IN IP4 192.0.2.10: la IP pública, que Antel no alcanza; la línea m=audio 10044 RTP/AVP 8 0 da el puerto. H1 confirmada. "
       "3: RTP Streams muestra un solo flujo, de 198.51.100.2:10044 a 198.51.100.1:10500, con unos 1000 paquetes, y ningún flujo de vuelta; Ctrl+R lo marca como flujo sin vuelta: la oficina no oye al de afuera. "
       "4: con las redes de Antel en Local Network Address, el SDP lleva c=IN IP4 198.51.100.2 y aparecen dos flujos, uno por sentido. Puertos y cantidades de ejemplo.",
       [8, 20, 34, 46, 58, 68, 86, 95])
