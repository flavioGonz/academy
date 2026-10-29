#!/usr/bin/env python3
"""Lección 4 · Laboratorio, paso 2: Codec Preference PCMA, PCMU y DTMF RFC4733 en el troncal. Lo que viaja en el
SDP: la oferta del INVITE con solo PCMA (8) y PCMU (0) más telephone-event, la respuesta del proveedor con PCMA,
y el audio. Con la lista sin recortar, la respuesta puede elegir otro codec. Fuentes: la lección (los dos lados
intercambian en el SDP la lista de codecs; PCMA primero; RFC4733); RFC 3264 (oferta y respuesta), RFC 3551
(tipos 0 y 8), RFC 4733 (telephone-event)."""
from _anim_gs_red import R

g = R(T=26, fix=62, kicker="GRANDSTREAM · TRONCAL REGISTRADO · LABORATORIO",
      title="Codecs recortados: la negociación da siempre lo mismo")
g.steps([
    "El INVITE ofrece solo PCMA y PCMU, en ese orden, más el evento de teclas.",
    "El proveedor contesta con uno de los ofrecidos: PCMA, y el evento de teclas.",
    "El audio viaja en PCMA, un paquete cada 20 ms; las teclas, como eventos RFC 4733.",
    "Sin recortar la lista se ofrecen más codecs, y la respuesta puede elegir otro.",
])

XU, XP = 150, 560
g.lane(XU, 176, 612, "UCM", "troncal Proveedor_Lab", w=240)
g.lane(XP, 176, 612, "Proveedor", "sip.proveedor.example", w=240)
g.msg(XU, XP, 272, "INVITE + SDP (oferta)", g.BLUE, 2, 9, tok="INVITE")
g.msg(XP, XU, 330, "200 OK + SDP (respuesta)", g.OK, 26, 33, tok="200 OK")
g.msg(XU, XP, 382, "ACK", g.BLUE, 36, 40)
for k in range(4):
    t = 52 + k * 5
    g.token([(XU, 440), (XP, 440)], t, t + 4, g.chip("RTP · PCMA", bg=g.OK, size=13, h=24), hold=t + 4.3)
    g.token([(XP, 476), (XU, 476)], t + 2, t + 6, g.chip("RTP · PCMA", bg=g.OK, size=13, h=24), hold=t + 6.3)
g.appear(g.text(355, 516, "teclas: eventos telephone-event (101)", 15, g.OK, g.MONO, 600, "middle"), 54, 75)
g.fijo_only(f'<g transform="translate(300 440)">' + g.chip("RTP · PCMA", bg=g.OK, size=13, h=24) + '</g>'
            + f'<g transform="translate(420 476)">' + g.chip("RTP · PCMA", bg=g.OK, size=13, h=24) + '</g>')
g.msg(XU, XP, 560, "INVITE (lista sin recortar)", g.AMB, 77, 84)
g.msg(XP, XU, 596, "200 OK con otro codec", g.AMB, 88, 94)

PX, PW = 696, 456
g.appear(g.term(PX, 186, PW, 196, "SDP del INVITE (oferta)", [
    ("m=audio 10044 RTP/AVP 8 0 101", "#5BE0A5"),
    ("a=rtpmap:8 PCMA/8000", None),
    ("a=rtpmap:0 PCMU/8000", None),
    ("a=rtpmap:101 telephone-event/8000", None),
], size=15, lh=28), 6, 75)
g.appear(g.term(PX, 400, PW, 132, "SDP del 200 OK (respuesta)", [
    ("m=audio 30000 RTP/AVP 8 101", "#5BE0A5"),
    ("a=rtpmap:8 PCMA/8000", None),
], size=15, lh=28), 30, 75)
g.appear(g.note(PX, 186, PW, "Advanced Settings del troncal", ["Codec Preference: PCMA, PCMU", "(el resto afuera, PCMA primero)", "DTMF Mode: RFC4733"], "info"), 0, 6)
g.appear(g.term(PX, 186, PW, 196, "SDP del INVITE (sin recortar, ejemplo)", [
    ("m=audio 10044 RTP/AVP 0 8 9 18 101", "#F6C35B"),
    ("PCMU, PCMA, G.722, G.729…", None),
    ("la respuesta elige de lo ofrecido", None),
], size=15, lh=28), 75, 100)
g.appear(g.note(PX, 400, PW, "Lo que conviene", ["Solo los codecs que pide el proveedor:", "la llamada sale siempre en el mismo."], "amb"), 75, 100)

g.status(640, [
    (0, 25, "8 es PCMA y 0 es PCMU, las dos variantes de G.711; 101, el evento de teclas.", g.INK),
    (25, 50, "La respuesta solo puede elegir entre lo que se ofreció.", g.OK),
    (50, 75, "Mismo codec de los dos lados: la central no tiene que convertir nada.", g.OK),
    (75, 100, "Con más codecs en la lista, la negociación puede elegir mal o fallar.", g.AMB),
], size=16)

g.done(4, "l1", "Codecs recortados: la negociación da siempre lo mismo",
       "Animación en cuatro tiempos con dos líneas de vida, la UCM con el troncal Proveedor_Lab y el proveedor sip.proveedor.example, y a la derecha el SDP de cada mensaje. "
       "1: con Codec Preference en PCMA y PCMU, el INVITE ofrece m=audio 10044 RTP/AVP 8 0 101: PCMA (8) primero, PCMU (0) y el evento de teclas telephone-event (101) de RFC 4733. "
       "2: el proveedor contesta 200 OK con m=audio 30000 RTP/AVP 8 101: elige PCMA y el evento de teclas, entre lo que se le ofreció; la UCM confirma con ACK. "
       "3: el audio viaja en PCMA en los dos sentidos, un paquete cada 20 ms, y las teclas como eventos RFC 4733. "
       "4: con la lista sin recortar, el INVITE ofrece más codecs, por ejemplo PCMU, PCMA, G.722 y G.729, y la respuesta puede elegir otro; la negociación puede elegir mal o fallar. "
       "Por eso se dejan solo los que pide el proveedor.",
       [8, 36, 62, 90])
