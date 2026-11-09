#!/usr/bin/env python3
"""Caso de estudio · Video de un lado · teoría: el video en la oferta y la respuesta (22-t1.svg).
RFC 3264: cada m= es un flujo; sendrecv, recvonly, sendonly; un puerto 0 en la respuesta rechaza el flujo.
RFC 4585 y 5104: con el flujo andando, si se pierde un cuadro completo, el receptor pide refresco (PLI o FIR;
RFC 5168 por SIP INFO) y el que manda responde con un cuadro completo (I-frame). Datos de ejemplo.
"""
from _anim_gs_red import R

g = R(T=28, fix=92, kicker="GRANDSTREAM · CASO DE ESTUDIO · VIDEO DE UN LADO", title="El video en la oferta y la respuesta")
g.steps([
    "Oferta y respuesta con a=sendrecv: hay video en los dos sentidos.",
    "La respuesta dice a=recvonly (sin cámara): el video va en un solo sentido.",
    "La respuesta trae m=video 0: el flujo se rechaza y no hay video para nadie.",
    "Con video andando, se pierde un cuadro: PLI o FIR, y llega un cuadro completo.",
], size=17)

B, OK, BAD, GREY, INK, AMB = g.BLUE, g.OK, g.BAD, g.GREY, g.INK, g.AMB
XA, XB = 230, 970
g.add(g.dev(48, 172, 364, 76, "Recepción · ofrece", "GXV3480", icon="user"))
g.add(g.dev(788, 172, 364, 76, "Depósito · responde", "GXV3350", icon="camera"))

def sdp(x, lines):
    return g.term(x, 266, 364, 112, None, lines, size=15, lh=28)

g.add(sdp(48, [("m=audio 5004 RTP/AVP 8 0", None), ("m=video 5006 RTP/AVP 99", None), ("a=sendrecv", "#9BE7C4")]))
ANS = [(0, 25, [("m=audio 5004 RTP/AVP 8", None), ("m=video 5006 RTP/AVP 99", None), ("a=sendrecv", "#9BE7C4")]),
       (25, 50, [("m=audio 5004 RTP/AVP 8", None), ("m=video 5006 RTP/AVP 99", None), ("a=recvonly", "#F6C35B")]),
       (50, 75, [("m=audio 5004 RTP/AVP 8", None), ("m=video 0 RTP/AVP 99", "#FFB4A8"), ("", None)]),
       (75, 100, [("m=audio 5004 RTP/AVP 8", None), ("m=video 5006 RTP/AVP 99", None), ("a=sendrecv", "#9BE7C4")])]
for t0, t1, ls in ANS:
    g.appear(sdp(788, ls), t0, t1)

# flujos de video entre las dos columnas
YF, YB = 300, 344
g.add(g.text(600, 268, "flujos de video", 15, GREY, g.SANS, 600, "middle"))
def flujo(y, x1, x2, t0, t1, col, label):
    for k in range(3):
        a = t0 + 2 + k * 6
        g.token([(x1, y), (x2, y)], a, a + 4, g.chip(label, bg=col, size=12, h=22), hold=a + 4.5)
flujo(YF, 460, 740, 0, 25, OK, "video")
flujo(YB, 740, 460, 0, 25, OK, "video")
flujo(YF, 460, 740, 25, 50, OK, "video")
g.appear(g.text(600, YB + 6, "no manda: no hay flujo de vuelta", 15, AMB, g.SANS, 600, "middle"), 28, 50, still=0)
g.appear(g.text(600, YF + 6, "puerto 0: sin video", 15, BAD, g.SANS, 600, "middle"), 53, 75, still=0)
g.appear(g.text(600, YB + 6, "en ningún sentido", 15, BAD, g.SANS, 600, "middle"), 53, 75, still=0)

# 4 · PLI / FIR
g.token([(740, YB), (500, YB)], 77, 80, g.chip("P", bg=OK, size=12, h=22), hold=80.5)
g.token([(740, YB), (600, YB)], 80, 82, g.chip("P", bg=BAD, size=12, h=22), hold=82.5)
g.appear(g.mark(600, YB, False, 12), 82, 86, still=0)
g.token([(460, YF), (740, YF)], 84, 88, g.chip("PLI / FIR", bg=AMB, size=12, h=22), hold=88.5)
g.token([(740, YB), (460, YB)], 89, 94, g.chip("I-frame", bg=B, size=12, h=22), hold=100, still=0)
g.fijo_only(f'<g transform="translate(540 {YB})">' + g.chip("I-frame", bg=B, size=12, h=22) + "</g>")
g.appear(g.text(600, YB + 34, "pide un cuadro completo", 14, AMB, g.SANS, 600, "middle"), 84, 100)

g.add(g.box(48, 404, 1104, 170, g.WHITE, g.LINE, rx=14))
ROWS = [(0, 25, "sendrecv en las dos puntas", ["cada lado manda y recibe: cuatro flujos con el audio", "RTP Streams los muestra con su origen y destino"], OK),
        (25, 50, "recvonly en la respuesta", ["el depósito solo recibe: recepción no lo ve", "pasa con un equipo sin cámara o sin permiso, o un portero al revés"], AMB),
        (50, 75, "puerto 0 en la respuesta", ["el video se rechaza para los dos: no es un problema de un lado", "suele ser H.264 fuera de Codec Preference de una extensión"], BAD),
        (75, 100, "PLI y FIR (RFC 4585 y 5104), o RFC 5168 por SIP INFO", ["sin cuadro completo, la imagen queda negra o congelada", "el que manda contesta con un I-frame y la imagen vuelve"], B)]
for t0, t1, h, ls, col in ROWS:
    inner = g.text(72, 444, h, 18, col, g.SANS, 600)
    for k, l in enumerate(ls):
        inner += g.text(72, 484 + k * 32, l, 17, g.TXT, g.SANS, 400)
    g.appear(inner, t0, t1)

g.done(22, "t1", "El video en la oferta y la respuesta",
       "Animación en cuatro tiempos. A la izquierda recepción con un GXV3480, que ofrece; a la derecha el depósito con un GXV3350, que responde; debajo de cada uno su SDP con m=audio y m=video y, entre los dos, los flujos de video. "
       "1: oferta y respuesta con a=sendrecv: hay video en los dos sentidos. "
       "2: la respuesta dice a=recvonly, como un equipo sin cámara o sin permiso: el depósito solo recibe, el video va en un solo sentido y recepción no lo ve. "
       "3: la respuesta trae m=video 0: un puerto 0 rechaza el flujo y no hay video para nadie; no es un problema de un lado y suele ser H.264 fuera de Codec Preference de una extensión. "
       "4: con el video andando se pierde un paquete; el receptor pide un cuadro completo con PLI o FIR, de las RFC 4585 y 5104, o con RFC 5168 por SIP INFO, y el que manda contesta con un I-frame; sin ese cuadro la imagen queda negra o congelada.",
       [6, 16, 32, 44, 60, 80, 90, 97])
