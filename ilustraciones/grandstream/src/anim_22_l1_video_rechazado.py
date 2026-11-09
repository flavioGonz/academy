#!/usr/bin/env python3
"""Caso de estudio · Video de un lado · Laboratorio, paso 3: 22-l1.svg.
Falla de negociación provocada: la 1004 sin H.264 en Codec Preference. La 1003 ofrece audio y video; la UCM no
ofrece video en la pata de la 1004 (su extensión no tiene H.264); la respuesta a la 1003 lleva m=video 0 (RFC 3264:
puerto 0, flujo rechazado). Nadie ve video: no es "de un lado". Lo de la pata de la 1004 sin video es lo esperable
según la oferta y respuesta; cómo arma la UCM cada pata depende del firmware (probalo con la captura).
"""
from _anim_gs_red import R

g = R(T=26, fix=94, kicker="GRANDSTREAM · CASO DE ESTUDIO · PASO 3", title="Sin H.264 en una extensión: m=video 0")
g.steps([
    "La 1003 llama con video: su INVITE ofrece m=audio y m=video 99 (H.264).",
    "La extensión 1004 no tiene H.264: la UCM la llama solo con audio.",
    "La UCM le contesta a la 1003 con m=video 0: video rechazado.",
    "Nadie ve video. No es de un lado: es negociación. Volvé a poner H.264.",
], size=17)

B, OK, BAD, GREY, INK = g.BLUE, g.OK, g.BAD, g.GREY, g.INK
X3, XU, X4 = 170, 520, 870
g.lane(X3, 168, 470, "1003", "GXV3480 · H.264", w=230)
g.lane(XU, 168, 470, "UCM", "relay de media", w=230)
g.lane(X4, 168, 470, "1004", "sin H.264", w=230)
g.msg(X3, XU, 266, "INVITE · audio + video", B, 3, 10, tok="INVITE")
g.msg(XU, X4, 316, "INVITE · solo audio", B, 28, 35, tok="INVITE")
g.msg(X4, XU, 356, "200 OK · audio", OK, 38, 44)
g.msg(XU, X3, 406, "200 OK · m=video 0", BAD, 53, 60, tok="200 OK")
g.msg(X3, XU, 446, "ACK", GREY, 63, 67)

# SDP
g.appear(g.term(48, 488, 540, 104, "SDP de la oferta de la 1003", [("m=audio 50040 RTP/AVP 8 0", None), ("m=video 50042 RTP/AVP 99", "#9BE7C4")]), 4, 100)
g.appear(g.term(612, 488, 540, 104, "Codec Preference · 1004", [("PCMA, PCMU   (H.264 fuera)", "#FFB4A8")]), 26, 50, still=0)
g.appear(g.term(612, 488, 540, 104, "SDP de la respuesta a la 1003", [("m=audio 10044 RTP/AVP 8", None), ("m=video 0 RTP/AVP 99", "#FFB4A8")]), 52, 100)
g.appear(g.pillc(1075, 250, "nadie ve video", BAD, g.BADBG, 14, 28), 76, 100)
g.appear(g.pillc(1075, 300, "no es de un lado", BAD, g.BADBG, 14, 28), 78, 100)
g.appear(g.pillc(1075, 350, "volvé a poner H.264", OK, g.OKBG, 14, 28), 82, 100)

g.done(22, "l1", "Sin H.264 en una extensión: m=video 0",
       "Animación en cuatro tiempos, diagrama de secuencia con la 1003, un GXV3480 con H.264, la UCM que hace de relay de media y la 1004, a la que se le sacó H.264 de Codec Preference; abajo, los SDP. "
       "1: la 1003 llama con video y su INVITE ofrece m=audio 50040 RTP/AVP 8 0 y m=video 50042 RTP/AVP 99, H.264. "
       "2: la extensión 1004 tiene solo PCMA y PCMU, así que la UCM la llama solo con audio y la 1004 contesta 200 OK con audio. "
       "3: la UCM le contesta a la 1003 con m=video 0: según la RFC 3264, un puerto 0 rechaza el flujo. "
       "4: nadie ve video: no es un problema de un lado, es negociación; se vuelve a poner H.264 en la extensión. Puertos de ejemplo; cómo arma la UCM cada pata se confirma con la captura.",
       [8, 20, 34, 46, 60, 70, 86, 95])
