#!/usr/bin/env python3
"""Caso de estudio · Cuelga y no corta · teoría: qué corta una llamada cuando el BYE no llega (23-t1.svg).
RFC 4028: Session-Expires y Min-SE en el INVITE; el refresher manda re-INVITE o UPDATE a mitad del intervalo;
sin refresco, la sesión se da por terminada. UCM630x: Session Expiration 1800 s y Min SE 90 s de fábrica;
RTP Timeout (sin timeout de fábrica) corta si no llega RTP. Valores de ejemplo: RTP Timeout 60 s.
"""
from _anim_gs_red import R

g = R(T=28, fix=92, kicker="GRANDSTREAM · CASO DE ESTUDIO · CUELGA Y NO CORTA", title="Qué corta la llamada cuando el BYE no llega")
g.steps([
    "INVITE con Session-Expires: 1800 y Min-SE: 90; el 200 OK acepta el intervalo.",
    "A mitad del intervalo, el refresher manda UPDATE y la sesión sigue viva.",
    "El teléfono desaparece: no llega más RTP. Con RTP Timeout 60, la UCM corta.",
    "Sin RTP Timeout: corta Session Expiration, si no hubo refresco a tiempo.",
], size=17)

B, OK, BAD, GREY, INK, AMB = g.BLUE, g.OK, g.BAD, g.GREY, g.INK, g.AMB
XT, XU = 200, 700
g.lane(XT, 170, 470, "Teléfono", "interno remoto", w=230)
g.lane(XU, 170, 470, "UCM", "Session Timer", w=230)
g.msg(XT, XU, 262, "INVITE · Session-Expires: 1800 · Min-SE: 90", B, 3, 10, size=14)
g.msg(XU, XT, 300, "200 OK · Session-Expires: 1800;refresher=uac", OK, 12, 18, size=14)
g.msg(XT, XU, 348, "UPDATE (a los 900 s)", B, 28, 34, tok="UPDATE", size=14)
g.msg(XU, XT, 382, "200 OK", OK, 36, 42, size=14)
# RTP que deja de llegar
for t0 in (52, 55, 58):
    g.token([(XT, 420), (XT + 140, 420)], t0, t0 + 2.4, g.chip("RTP", bg=GREY, size=12, h=22), hold=t0 + 2.6)
g.appear(g.mark(XT + 170, 420, False, 13), 53, 75, still=0)
g.appear(g.text(XT + 196, 426, "no llega más RTP", 15, BAD, g.SANS, 600), 53, 75, still=0)
g.msg(XU, XT, 452, "BYE · RTP Timeout", BAD, 66, 71, hold=75, still=0, size=14)
g.msg(XU, XT, 452, "BYE · Session Expiration vencida", BAD, 90, 95, size=14)

# relojes a la derecha
PX = 860
g.add(g.box(PX, 176, 292, 290, g.WHITE, g.LINE, rx=14))
g.add(g.text(PX + 20, 206, "Relojes de la UCM", 17, INK, g.SANS, 600))
g.add(g.text(PX + 20, 244, "Session Expiration", 14, GREY, g.MONO))
g.add(g.box(PX + 20, 254, 252, 20, g.SLATE, rx=6))
g.bar(PX + 20, 254, 126, 20, 14, 30, B, hold=34, still=0)
g.appear(g.text(PX + 20, 296, "se reinicia con cada refresco", 14, OK, g.SANS, 600), 34, 50, still=0)
g.bar(PX + 20, 254, 252, 20, 78, 92, BAD)
g.appear(g.text(PX + 20, 296, "1800 s sin refresco: corta", 14, BAD, g.SANS, 600), 90, 100)
g.add(g.text(PX + 20, 340, "RTP Timeout", 14, GREY, g.MONO))
g.add(g.box(PX + 20, 350, 252, 20, g.SLATE, rx=6))
g.bar(PX + 20, 350, 252, 20, 56, 66, AMB, hold=75, still=0)
g.appear(g.text(PX + 20, 392, "60 s sin audio: corta", 14, BAD, g.SANS, 600), 66, 75, still=0)
g.appear(g.text(PX + 20, 392, "sin configurar", 14, GREY, g.SANS, 600), 76, 100)
g.add(g.text(PX + 20, 440, "PBX Settings > SIP Settings", 13, B, g.MONO, 600))

g.add(g.box(48, 500, 1104, 126, g.WHITE, g.LINE, rx=14))
ROWS = [(0, 25, "RFC 4028: la sesión tiene un vencimiento que se negocia", ["Min-SE es el mínimo que acepta la UCM: 90 s de fábrica; Session Expiration, 1800 s"], INK),
        (25, 50, "El refresco va a mitad del intervalo, con re-INVITE o UPDATE", ["si un lado se fue, el refresco falla y la sesión se da por terminada"], OK),
        (50, 75, "RTP Timeout corta cuando no llega audio en ese tiempo", ["sin timeout de fábrica: si no se configura, la llamada queda viva en silencio"], BAD),
        (75, 100, "Session Timer solo actúa si los dos lados lo negocian", ["Timer viene prendido; Force Timer lo exige y puede rechazar llamadas"], AMB)]
for t0, t1, h, ls, col in ROWS:
    inner = g.text(72, 538, h, 18, col, g.SANS, 600)
    for k, l in enumerate(ls):
        inner += g.text(72, 576 + k * 28, l, 16, g.TXT, g.SANS, 400)
    g.appear(inner, t0, t1)

g.done(23, "t1", "Qué corta la llamada cuando el BYE no llega",
       "Animación en cuatro tiempos, diagrama de secuencia entre un teléfono remoto y la UCM, con los relojes de la UCM a la derecha: Session Expiration y RTP Timeout. "
       "1: el INVITE lleva Session-Expires: 1800 y Min-SE: 90, y el 200 OK acepta el intervalo con refresher=uac; según la RFC 4028 la sesión tiene un vencimiento negociado, y en la UCM Min SE es 90 y Session Expiration 1800 de fábrica. "
       "2: a mitad del intervalo, a los 900 segundos, el teléfono manda UPDATE, la UCM contesta 200 OK y el reloj de la sesión se reinicia. "
       "3: el teléfono desaparece y no llega más RTP; con RTP Timeout en 60 segundos, la UCM corta y manda BYE. RTP Timeout viene sin timeout de fábrica. "
       "4: sin RTP Timeout, corta Session Expiration cuando pasa el intervalo sin refresco; solo actúa si los dos lados lo negociaron. Valores de ejemplo.",
       [6, 16, 32, 44, 60, 70, 88, 97])
