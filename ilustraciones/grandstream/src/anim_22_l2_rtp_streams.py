#!/usr/bin/env python3
"""Caso de estudio · Video de un lado · Laboratorio, paso 5: 22-l2.svg.
RTP Streams en la captura de la UCM con la cola del MikroTik puesta: cuatro flujos (audio y video en los dos
sentidos); el de video de la 1004 (10.10.10.31) llega con pérdida alta; el de la UCM hacia la 1004, sin pérdida.
Los tres lugares: se manda (hay flujo), llega roto (Lost, calculado con los números de secuencia), no es el
decodificador. Con VGA y 384 kbps: Lost cerca de 0. Puertos, cantidades y porcentajes de ejemplo.
"""
from _anim_gs_red import R

g = R(T=26, fix=94, kicker="GRANDSTREAM · CASO DE ESTUDIO · PASO 5", title="RTP Streams: cuál de los cuatro flujos llega roto")
g.steps([
    "¿Se manda? Hay flujo de video de 10.10.10.31, la 1004, hacia la UCM.",
    "¿Llega entero? Ese flujo tiene Lost alto; el que va hacia la 1004, no.",
    "Se manda y llega roto, en la subida del depósito: es el enlace.",
    "Con VGA y 384 kbps, el mismo flujo llega sin pérdida.",
], size=17)

B, OK, BAD, GREY, INK, AMB = g.BLUE, g.OK, g.BAD, g.GREY, g.INK, g.AMB
TX, TY = 48, 172
g.add(g.box(TX, TY, 1104, 260, g.WHITE, g.LINE, rx=14))
g.add(g.text(TX + 20, TY + 30, "Telephony > RTP > RTP Streams · la pata del depósito (1004)", 15, B, g.MONO, 600))
cols = [TX + 20, TX + 260, TX + 500, TX + 700, TX + 860, TX + 980]
for x, h in zip(cols, ("Origen", "Destino", "Payload", "Paquetes", "Lost", "")):
    g.add(g.text(x, TY + 62, h, 14, GREY, g.MONO, 600))
rows = [("10.10.10.31:50040", "192.168.88.20:10044", "PCMA", "1000", "0,4 %"),
        ("192.168.88.20:10044", "10.10.10.31:50040", "PCMA", "1000", "0 %"),
        ("192.168.88.20:10046", "10.10.10.31:50042", "H.264 (99)", "3400", "0 %"),
        ("10.10.10.31:50042", "192.168.88.20:10046", "H.264 (99)", "1900", "35 %")]
for i, r in enumerate(rows):
    y = TY + 98 + i * 40
    s = "".join(g.text(x, y, v, 15, INK, g.MONO) for x, v in zip(cols[:4], r[:4]))
    g.add(s)
    if i < 3:
        g.add(g.text(cols[4], y, r[4], 15, OK, g.MONO, 600))
YR = TY + 98 + 3 * 40
g.appear(g.box(TX + 10, YR - 26, 1084, 36, "none", B, rx=8, sw=2.5), 4, 25, still=0)
g.appear(g.text(cols[4], YR, "35 %", 15, BAD, g.MONO, 600), 25, 76, still=0)
g.appear(g.box(TX + 10, YR - 26, 1084, 36, g.BADBG, rx=8) + "".join(g.text(x, YR, v, 15, INK, g.MONO) for x, v in zip(cols[:4], rows[3][:4]))
         + g.text(cols[4], YR, "35 %", 15, BAD, g.MONO, 600), 27, 76, still=0)
g.appear(g.mark(cols[5] + 40, YR - 6, False, 13), 27, 76, still=0)
g.appear(g.box(TX + 10, YR - 66, 1084, 36, "none", OK, rx=8, sw=2), 32, 50, still=0)
g.appear(g.text(cols[4], YR, "0,2 %", 15, OK, g.MONO, 600) + g.mark(cols[5] + 40, YR - 6, True, 13), 78, 100)
g.add(g.text(TX + 20, TY + 244, "Lost se calcula con los números de secuencia del RTP", 14, GREY, g.SANS, 400))

# los tres lugares
PY = 452
places = [("1 · ¿Se manda?", "sí: hay flujo de 10.10.10.31", 0, OK),
          ("2 · ¿Llega entero?", "no: 35 % perdido en un sentido", 25, BAD),
          ("3 · ¿Se decodifica?", "no hace falta mirarlo todavía", 50, GREY)]
for i, (t, d, t0, col) in enumerate(places):
    x = 48 + i * 372
    g.add(g.box(x, PY, 352, 80, g.WHITE, g.LINE, rx=12))
    g.add(g.text(x + 18, PY + 30, t, 17, INK, g.SANS, 600))
    if i == 1:
        g.appear(g.text(x + 18, PY + 60, d, 15, col, g.SANS, 600), t0 + 2, 77, still=0)
        g.appear(g.text(x + 18, PY + 60, "sí: 0,2 % con el arreglo", 15, OK, g.SANS, 600), 78, 100)
    else:
        g.appear(g.text(x + 18, PY + 60, d, 15, col, g.SANS, 600), t0 + 2, 100)
g.add(g.box(48, 548, 1104, 76, g.WHITE, g.LINE, rx=14))
ROWS = [(0, 25, "La pata de la 1004: audio y video, cada uno en los dos sentidos", INK),
        (25, 50, "El video que baja a la 1004 llega entero: la cámara de recepción está bien", OK),
        (50, 76, "Se manda y llega roto: la subida del depósito no da para 720P a 2048 kbps", BAD),
        (76, 100, "GXV3350: H.264 Image Size VGA y Video Bit Rate 384 kbps; misma captura para verificar", OK)]
for t0, t1, s_, col in ROWS:
    g.appear(g.text(72, 594, s_, 17, col, g.SANS, 600), t0, t1)

g.done(22, "l2", "RTP Streams: cuál de los cuatro flujos llega roto",
       "Animación en cuatro tiempos con la ventana Telephony > RTP > RTP Streams de la captura en la UCM: los cuatro flujos de la pata de la 1004, audio PCMA y video H.264 con payload 99, cada uno en los dos sentidos, con su origen, destino, paquetes y pérdida. Debajo, tres casillas para los tres lugares del método. "
       "1: se manda: hay un flujo de video desde 10.10.10.31, la 1004 del depósito, hacia la UCM. "
       "2: ese flujo tiene Lost de 35 por ciento, calculado con los números de secuencia, y el de video de la UCM hacia la 1004 llega sin pérdida: la cámara de recepción está bien. "
       "3: se manda y llega roto, en la subida del depósito: es el enlace, que no da para 720P a 2048 kbps; el decodificador no hace falta mirarlo todavía. "
       "4: con H.264 Image Size en VGA y Video Bit Rate en 384 kbps en el GXV3350, el mismo flujo llega con pérdida cercana a cero. Puertos, cantidades y porcentajes de ejemplo.",
       [8, 20, 34, 46, 60, 70, 86, 95])
