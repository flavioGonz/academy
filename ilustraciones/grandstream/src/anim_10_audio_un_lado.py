#!/usr/bin/env python3
"""Lección 10 · teoría: señalización y audio son dos conversaciones; una IP privada en el SDP da audio de un lado."""
from _anim_grandstream import G

g = G(T=28, fix=90, kicker="GRANDSTREAM · AUDIO DE UN LADO", title="Dos conversaciones: SIP arregla, RTP lleva la voz")
g.steps([
    "El INVITE lleva el SDP: c= dice a qué IP mandar el audio y m= a qué puerto.",
    "El 200 OK trae el SDP del otro lado y el ACK cierra el saludo.",
    "Cada lado manda RTP a lo que anunció el otro: unos 50 paquetes por segundo.",
    "Si la UCM anuncia su IP privada hacia afuera, el otro manda el audio ahí.",
    "Audio de un lado: el remoto escucha a la oficina, la oficina no lo escucha.",
])

XU, XR = 190, 690
g.lane(XU, 176, 630, "UCM", "192.168.88.20", w=240)
g.lane(XR, 176, 630, "Otro extremo", "remoto 198.51.100.7", w=260)
g.msg(XU, XR, 274, "INVITE + SDP", g.BLUE, 2, 10, tok="INVITE")
g.msg(XR, XU, 322, "200 OK + SDP", g.OK, 22, 30, tok="200 OK")
g.msg(XU, XR, 368, "ACK", g.BLUE, 33, 38, tok="ACK")
g.add(g.text(XU + 250, 404, "señalización SIP · arriba   |   audio RTP · abajo", 13, g.GREY, g.MONO, 400, "middle"))
g.add(f'<line x1="{XU - 120}" y1="414" x2="{XR + 130}" y2="414" stroke="{g.LINE}" stroke-width="1.5"/>')

Y1, Y2 = 460, 540   # RTP remoto → UCM, UCM → remoto
g.add(g.text(XU + 14, Y1 - 22, "remoto → UCM", 14, g.GREY, g.MONO, 400))
g.add(g.text(XU + 14, Y2 - 22, "UCM → remoto", 14, g.GREY, g.MONO, 400))
# tiempo 3: todo bien
for k in range(4):
    t = 41 + k * 4
    g.token([(XR, Y1), (XU, Y1)], t, t + 6, g.chip("RTP", bg=g.OK, size=13, h=24), hold=t + 6.3)
    g.token([(XU, Y2), (XR, Y2)], t + 1.5, t + 7.5, g.chip("RTP", bg=g.OK, size=13, h=24), hold=t + 7.8)
# tiempos 4 y 5: IP privada
for k in range(7):
    t = 62 + k * 5
    g.token([(XR, Y1), (440, Y1)], t, t + 4, g.chip("RTP", bg=g.BAD, size=13, h=24), hold=t + 4.3)
    g.token([(XU, Y2), (XR, Y2)], t + 1.5, t + 7.5, g.chip("RTP", bg=g.OK, size=13, h=24), hold=min(t + 7.8, 100))
g.appear(g.mark(420, Y1, False, 15) + g.text(400, Y1 + 34, "va a 192.168.88.20 por internet: no llega", 14, g.BAD, g.MONO, 600, "middle"), 64, 100)
g.appear(g.pillc(XU, 600, "no escucha al remoto", g.BAD, g.BADBG), 82, 100)
g.appear(g.pillc(XR, 600, "escucha a la oficina", g.OK, g.OKBG), 82, 100)
g.fijo_only(f'<g transform="translate(560 {Y1})">' + g.chip("RTP", bg=g.BAD, size=13, h=24) + "</g>"
            + f'<g transform="translate(440 {Y2})">' + g.chip("RTP", bg=g.OK, size=13, h=24) + "</g>")

# SDP de la UCM
PX, PW = 860, 292
g.add(g.box(PX, 186, PW, 172, "#03213C", None, rx=14))
g.add(g.text(PX + 18, 214, "SDP que manda la UCM", 14, "#9FC3E3", g.MONO))
g.appear(g.text(PX + 18, 252, "c=IN IP4 203.0.113.10", 16, "#5BE0A5", g.MONO, 600)
         + g.text(PX + 18, 280, "m=audio 10044", 16, "#D9E9F8", g.MONO, 600)
         + g.text(PX + 18, 302, "  RTP/AVP 8 0", 16, "#D9E9F8", g.MONO, 600)
         + g.text(PX + 18, 336, "IP pública: bien", 15, "#5BE0A5", g.SANS, 600), 4, 60)
g.appear(g.text(PX + 18, 252, "c=IN IP4 192.168.88.20", 16, "#FF9A85", g.MONO, 600)
         + g.text(PX + 18, 280, "m=audio 10044", 16, "#D9E9F8", g.MONO, 600)
         + g.text(PX + 18, 302, "  RTP/AVP 8 0", 16, "#D9E9F8", g.MONO, 600)
         + g.text(PX + 18, 336, "IP privada hacia afuera", 15, "#FF9A85", g.SANS, 600), 60, 100)
g.add(g.note(PX, 380, PW, None, ["8 y 0: PCMA y PCMU.", "G.711 a 20 ms: unos 50", "paquetes por segundo."], "info"))
g.appear(g.note(PX, 482, PW, "Por qué pasa", ["Falta External Host, o un", "SIP ALG reescribió el SDP.", "Un puerto RTP sin reenviar", "da el mismo síntoma."], "bad"), 62, 100)

g.finish(10, 1, "Dos conversaciones: SIP arregla, RTP lleva la voz",
         "Animación en cinco tiempos con dos líneas de vida, la UCM en 192.168.88.20 y un remoto en 198.51.100.7; arriba la señalización SIP y abajo el audio RTP en los dos sentidos. "
         "1: la UCM manda INVITE con SDP; c=IN IP4 203.0.113.10 dice a qué IP mandar el audio y m=audio 10044 RTP/AVP 8 0 a qué puerto, con PCMA o PCMU. "
         "2: el remoto responde 200 OK con su SDP y la UCM cierra con ACK. "
         "3: cada lado manda RTP a lo que anunció el otro, unos 50 paquetes por segundo con G.711 a 20 ms, y el audio va y viene. "
         "4: si la UCM anuncia su IP privada, c=IN IP4 192.168.88.20, el remoto manda el audio a esa dirección por internet y no llega; el audio de la UCM al remoto sí llega. "
         "5: audio de un lado: el remoto escucha a la oficina y la oficina no escucha al remoto. "
         "Causas: falta External Host o un SIP ALG reescribió el SDP; un puerto RTP sin reenviar da el mismo síntoma.",
         [8, 30, 50, 70, 90])
