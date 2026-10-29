#!/usr/bin/env python3
"""Lección 10 (Audio de un lado) · Laboratorio, paso 2: llamada de 20 segundos con Ethernet Capture corriendo.
La UCM guarda una copia de lo que entra y sale por la interfaz elegida: la señalización y unos 50 paquetes RTP por
segundo en cada sentido; después se detiene y se descarga para Wireshark. Fuentes: la lección (Maintenance >
Network Troubleshooting > Ethernet Capture; llamada de 20 s; G.711 a 20 ms, unos 50 paquetes por segundo;
RTP Streams con unos 1000 paquetes por sentido; capturar en el propio equipo)."""
from _anim_gs_red import R

g = R(T=26, fix=62, kicker="GRANDSTREAM · AUDIO DE UN LADO · LABORATORIO",
      title="Lo que guarda la captura durante la llamada")
g.steps([
    "Start: desde ahora la UCM guarda una copia de cada paquete de esa interfaz.",
    "Llamada de 20 s: INVITE, 200 OK, ACK y el audio, unos 50 paquetes por segundo por sentido.",
    "Cortás, Stop y descarga: el archivo va a tu notebook para abrirlo en Wireshark.",
    "Ahí se ve qué IP anunció cada lado y cuántos paquetes de audio hubo en cada sentido.",
])

Y, H = 190, 96
YL = Y + H / 2
g.add(g.dev(48, Y, 236, H, "1001", "192.168.88.30", icon="tel"))
g.add(g.box(392, Y, 416, H, g.INK, rx=14))
g.add(g.ico(408, Y + 16, "ucm", g.CYAN, 1.35))
g.add(g.text(454, Y + 40, "UCM · 192.168.88.20", 19, g.WHITE, g.HEAD, 600))
g.add(g.text(454, Y + 66, "Ethernet Capture", 15, g.SKY, g.MONO))
g.add(g.dev(916, Y, 236, H, "Remoto", "198.51.100.7", icon="tel"))
g.add(g.wire(284, YL, 392, YL, g.BLUE))
g.add(g.wire(808, YL, 916, YL, g.BLUE))
g.appear(g.pillc(600, Y + H + 12, "● grabando", g.BAD, g.BADBG, 13, 26), 3, 50)
g.appear(g.pillc(600, Y + H + 12, "detenida · descargada", g.OK, g.OKBG, 13, 26), 52, 100)

LANE = Y - 20
g.token([(166, LANE), (1034, LANE)], 27, 31, g.chip("INVITE", bg=g.BLUE, size=13, h=26), hold=31.3)
g.token([(1034, LANE), (166, LANE)], 32, 35, g.chip("200 OK", bg=g.OK, size=13, h=26), hold=35.3)
g.token([(166, LANE), (1034, LANE)], 35.5, 38, g.chip("ACK", bg=g.BLUE, size=13, h=26), hold=38.3)
for k in range(4):
    t = 39 + k * 2.6
    g.token([(166, LANE), (1034, LANE)], t, t + 3, g.chip("RTP", bg=g.OK, size=13, h=24), hold=t + 3.2)
    g.token([(1034, LANE + 0.1), (166, LANE + 0.1)], t + 1, t + 4, g.chip("RTP", bg=g.OK, size=13, h=24), hold=t + 4.2)

# archivo de captura
FX, FY, FW = 48, 344, 760
g.add(g.box(FX, FY, FW, 180, g.WHITE, g.LINE, rx=14))
g.add(g.ico(FX + 18, FY + 16, "file", g.BLUE, 1.3))
g.add(g.text(FX + 62, FY + 40, "archivo de captura", 17, g.INK, g.SANS, 600))
rows = [("SIP", "INVITE · 200 OK · ACK · BYE"), ("RTP UCM → remoto", ""), ("RTP remoto → UCM", "")]
for k, (n, v) in enumerate(rows):
    y = FY + 82 + k * 32
    g.add(g.text(FX + 20, y, n, 15, g.GREY, g.MONO))
g.appear(g.text(FX + 260, FY + 82, "INVITE · 200 OK · ACK", 16, g.INK, g.MONO, 600), 33, 46)
g.appear(g.text(FX + 260, FY + 82, "INVITE · 200 OK · ACK · BYE", 16, g.INK, g.MONO, 600), 46, 100)
for k in range(2):
    y = FY + 114 + k * 32
    g.appear(g.text(FX + 260, y, "0 paquetes", 16, g.GREY, g.MONO, 600), 0, 40)
    g.appear(g.text(FX + 260, y, "≈ 500 paquetes…", 16, g.INK, g.MONO, 600), 40, 44)
    g.appear(g.text(FX + 260, y, "≈ 1000 paquetes en 20 s", 16, g.OK, g.MONO, 600), 44, 100)
g.appear(g.box(FX + 10, FY + 96, FW - 20, 76, "none", g.OK, rx=8, sw=2.5), 77, 100)

# notebook
g.add(g.dev(852, FY, 300, 96, "Tu notebook", "Wireshark", icon="laptop"))
g.token([(600, FY - 4), (1002, FY - 4)], 54, 62, g.chip("captura", bg=g.BLUE, size=13, h=26), hold=63)
g.appear(g.term(852, FY + 112, 300, 68, None, [("sip || sdp", g.MINT)], size=17), 64, 100)

g.appear(g.note(48, 548, 1104, None, ["Maintenance > Network Troubleshooting > Ethernet Capture: interfaz de los teléfonos y Start, antes de llamar."], "info"), 0, 50)
g.appear(g.note(48, 548, 1104, None, ["Solo queda lo que pasa por la interfaz de la UCM: por eso se captura en el equipo que está en el camino del audio."], "info"), 50, 75)
g.appear(g.note(48, 548, 1104, None, ["Un sentido con 1000 paquetes y el otro en 0 es audio de un lado. La captura tiene audio real: no sale del soporte."], "amb"), 75, 100)

g.done(10, "l1", "Lo que guarda la captura durante la llamada",
       "Animación en cuatro tiempos con la interna 1001 (192.168.88.30), la UCM en 192.168.88.20 con Ethernet Capture y un remoto en 198.51.100.7; abajo, el archivo de captura y la notebook del técnico. "
       "1: con Start en Maintenance > Network Troubleshooting > Ethernet Capture, la UCM empieza a guardar una copia de cada paquete de la interfaz elegida. "
       "2: en la llamada de 20 segundos pasan INVITE, 200 OK y ACK, y el audio, unos 50 paquetes RTP por segundo en cada sentido: alrededor de 1000 por sentido; al cortar, el BYE. "
       "3: Stop y descarga: el archivo va a la notebook para abrirlo en Wireshark con el filtro sip || sdp; solo queda lo que pasó por la interfaz de la UCM, por eso se captura en el equipo que está en el camino. "
       "4: ahí se ve qué IP anunció cada lado y cuántos paquetes de audio hubo en cada sentido; un sentido con 1000 y el otro en 0 es audio de un lado. La captura tiene audio real y no sale del soporte.",
       [8, 42, 62, 90])
