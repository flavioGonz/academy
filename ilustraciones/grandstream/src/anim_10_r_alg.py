#!/usr/bin/env python3
"""Lección 10 (Audio de un lado) · Resumen, "Cómo se ve en la red": el antes y después del SIP ALG. La UCM manda bien
c=IN IP4 203.0.113.10, el router con ALG lo reescribe y el remoto manda el audio a una IP privada; con el ALG
apagado y el router reiniciado, el SDP llega como salió. Fuentes: la lección (un ALG reescribe lo que la central
mandó bien; se apaga, se reinicia el router y se vuelve a capturar; RFC 4787 REQ-10 pide que vengan apagados)."""
from _anim_gs_red import R

g = R(T=26, fix=62, kicker="GRANDSTREAM · AUDIO DE UN LADO · CÓMO SE VE EN LA RED",
      title="El ALG reescribe lo que la central mandó bien")
g.steps([
    "La UCM atiende y manda el 200 OK con su SDP: c=IN IP4 203.0.113.10, correcto.",
    "El router con SIP ALG activo cambia esa línea: al remoto le llega 192.168.88.20.",
    "El remoto manda su audio a 192.168.88.20 por internet y se pierde: audio de un lado.",
    "ALG apagado y router reiniciado: el SDP llega como salió y el audio va y viene.",
])

Y, H = 190, 96
YL = Y + H / 2
g.add(g.dev(48, Y, 240, H, "UCM", "192.168.88.20", icon="ucm", dark=True, sub2="External Host .10"))
g.add(g.dev(352, Y, 286, H, "Router oficina", "203.0.113.10", icon="router", sub2=" "))
g.add(g.cloud(684, Y + 14, 120, 68))
g.add(g.dev(850, Y, 302, H, "Remoto", "198.51.100.7", icon="tel"))
g.add(g.wire(288, YL, 352, YL, g.BLUE))
g.add(g.wire(638, YL, 684, YL, g.BLUE))
g.add(g.wire(804, YL, 850, YL, g.BLUE))
g.appear(g.text(414, Y + 76, "SIP ALG: activo", 15, g.BAD, g.MONO, 600), 0, 75)
g.appear(g.text(414, Y + 76, "SIP ALG: apagado", 15, g.OK, g.MONO, 600), 75, 100)

LANE = Y - 20
g.token([(168, LANE), (495, LANE)], 2, 10, g.chip("200 OK · c=203.0.113.10", bg=g.OK, size=13, h=26), hold=12)
g.token([(495, LANE), (1001, LANE)], 28, 38, g.chip("200 OK · c=192.168.88.20", bg=g.BAD, size=13, h=26), hold=48)
for k in range(3):
    t = 52 + k * 6
    g.token([(1001, LANE), (800, LANE)], t, t + 5, g.chip("RTP → 192.168.88.20", bg=g.BAD, size=13, h=24), hold=t + 5.3)
    g.token([(168, Y + H + 18), (1001, Y + H + 18)], t + 1, t + 6, g.chip("RTP", bg=g.OK, size=13, h=24), hold=t + 6.3)
g.appear(g.mark(690, LANE, False, 14), 54, 75)
g.token([(168, LANE), (1001, LANE)], 77, 85, g.chip("200 OK · c=203.0.113.10", bg=g.OK, size=13, h=26), hold=87)
for k in range(2):
    t = 88 + k * 5
    g.token([(1001, LANE), (168, LANE)], t, t + 5, g.chip("RTP", bg=g.OK, size=13, h=24), hold=t + 5.3)
g.fijo_only(f'<g transform="translate(900 {LANE})">' + g.chip("RTP → 192.168.88.20", bg=g.BAD, size=13, h=24) + '</g>')

PY = 350
g.add(g.box(48, PY, 540, 170, "#03213C", None, rx=14))
g.add(g.text(68, PY + 32, "SDP que salió de la UCM", 15, g.SKY, g.MONO))
g.add(g.text(68, PY + 76, "c=IN IP4 203.0.113.10", 20, g.MINT, g.MONO, 600))
g.add(g.text(68, PY + 112, "m=audio 10044 RTP/AVP 8 0", 18, "#D9E9F8", g.MONO, 600))
g.add(g.text(68, PY + 148, "lo que la central escribió: bien", 15, g.MINT, g.SANS, 600))

g.add(g.box(612, PY, 540, 170, "#03213C", None, rx=14))
g.add(g.text(632, PY + 32, "SDP que le llegó al remoto", 15, g.SKY, g.MONO))
g.appear(g.text(632, PY + 76, "(todavía en camino)", 17, g.SKY, g.SANS), 0, 38)
g.appear(g.text(632, PY + 76, "c=IN IP4 192.168.88.20", 20, "#FF9C86", g.MONO, 600)
         + g.text(632, PY + 148, "reescrito en el router: IP privada", 15, "#FF9C86", g.SANS, 600), 38, 75)
g.appear(g.text(632, PY + 76, "c=IN IP4 203.0.113.10", 20, g.MINT, g.MONO, 600)
         + g.text(632, PY + 148, "igual a lo que salió", 15, g.MINT, g.SANS, 600), 85, 100)
g.appear(g.text(632, PY + 112, "m=audio 10044 RTP/AVP 8 0", 18, "#D9E9F8", g.MONO, 600), 38, 75)
g.appear(g.text(632, PY + 112, "m=audio 10044 RTP/AVP 8 0", 18, "#D9E9F8", g.MONO, 600), 85, 100)

g.status(560, [
    (0, 25, "La configuración de la UCM está bien: External Host y Local Network Address.", g.OK),
    (25, 50, "El ALG intenta arreglar un NAT que ya estaba resuelto, y lo rompe.", g.BAD),
    (50, 75, "El remoto escucha a la oficina; la oficina no escucha al remoto.", g.BAD),
    (75, 100, "Se confirma con otra captura: lo que sale y lo que llega tienen que coincidir.", g.OK),
])
g.appear(g.note(48, 584, 1104, None, ["El mismo ALG puede romper el ACK y cortar la llamada a los 32 s. La RFC 4787 pide que estos ALG vengan apagados."], "amb"), 0, 100)

g.done(10, "r1", "El ALG reescribe lo que la central mandó bien",
       "Animación en cuatro tiempos con la UCM en 192.168.88.20 con External Host 203.0.113.10, el router de la oficina con SIP ALG activo, internet y un remoto en 198.51.100.7; abajo, el SDP que salió de la UCM y el que le llegó al remoto. "
       "1: la UCM atiende y manda el 200 OK con c=IN IP4 203.0.113.10 y m=audio 10044 RTP/AVP 8 0: lo que escribió está bien. "
       "2: el router con SIP ALG cambia la línea c= y al remoto le llega c=IN IP4 192.168.88.20, una IP privada. "
       "3: el remoto manda su audio a 192.168.88.20 por internet y se pierde, mientras el audio de la UCM al remoto sí llega: el remoto escucha a la oficina y la oficina no lo escucha. "
       "4: con el SIP ALG apagado y el router reiniciado, el SDP llega como salió y el audio va y viene; se confirma con otra captura. "
       "Nota: el mismo ALG puede romper el ACK y cortar la llamada a los 32 segundos; la RFC 4787 pide que estos ALG vengan apagados.",
       [8, 40, 62, 92])
