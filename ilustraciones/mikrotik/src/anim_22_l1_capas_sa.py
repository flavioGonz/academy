#!/usr/bin/env python3
"""Lección 22 · IPsec entre marcas · Laboratorio paso 5: diagnóstico por capas.
active-peers (fase 1), ph2-state en la policy (fase 2) y los contadores de las dos SA de installed-sa con tráfico real.
"""
from _anim_mk_32_39 import *

a = Anim(T=28, kicker="MIKROTIK · IPSEC ENTRE MARCAS · PASO 5", title="Mirá por capas: peer, fase 2 y los contadores")
a.steps([
    "Fase 1: active-peers muestra a 198.51.100.20 establecido.",
    "Fase 2: la policy pasa a ph2-state=established y aparecen dos SA, una por sentido.",
    "Ping a 10.10.10.5: suben los bytes de la SA de ida y, con la respuesta, los de vuelta.",
    "Si sube solo la de ida, la falla está del otro lado: firewall, bypass o gateway en B.",
], still=2, size=17)

a.add(router(a, 48, 172, 250, 120, "Sitio A", "203.0.113.10", "LAN 192.168.88.0/24"))
a.add(router(a, 902, 172, 250, 120, "Sitio B", "198.51.100.20", "LAN 10.10.10.0/24"))
# fase 1
a.add(line(298, 232, 902, 232, a.LINE, 3, "5 7"))
a.add(during(a, a.box(310, 190, 580, 84, a.AMBBG, a.AMB, rx=14, sw=2, extra='fill-opacity=".6"'), 6, 100, still=1))
a.add(during(a, a.text(600, 212, "fase 1 · canal seguro", 15, a.AMB, a.MONO, 600, "middle"), 6, 100, still=1))
a.add(travel(a, dot(a, a.AMB, 9), [(310, 232), (890, 232)], 1, 5, hold=0.3))
a.add(travel(a, dot(a, a.AMB, 9), [(890, 232), (310, 232)], 5, 9, hold=0.3))
# dos SA
a.add(during(a, a.arrow("M330 240 H870", a.BLUE, 3) + a.text(600, 236, "SA de ida", 14, a.BLUE, a.MONO, 600, "middle"), 30, 100, still=1))
a.add(during(a, a.arrow("M870 262 H330", a.OK, 3) + a.text(600, 258, "SA de vuelta", 14, a.OK, a.MONO, 600, "middle"), 32, 100, still=1))
# ping
for t in (52, 58, 64):
    a.add(travel(a, pkt(a, "ESP", a.BLUE, size=13, h=22), [(340, 240), (860, 240)], t, t + 3, hold=0.2))
    a.add(travel(a, pkt(a, "ESP", a.OK, size=13, h=22), [(860, 262), (340, 262)], t + 3, t + 6, hold=0.2))
for t in (78, 84, 90):
    a.add(travel(a, pkt(a, "ESP", a.BLUE, size=13, h=22), [(340, 240), (860, 240)], t, t + 3, hold=0.2))
a.add(during(a, xmark(a, 940, 314) + a.text(964, 320, "la respuesta no sale", 15, a.BAD, a.SANS, 600), 82, 100))

# terminal
PX, PY, PW = 48, 334, 1104
a.add(a.box(PX, PY, PW, 270, a.INK, rx=14))
a.add(a.text(PX + 18, PY + 30, "EN EL SITIO A", 13, SKY, a.MONO, 400, extra='letter-spacing="1.6"'))
C1, C2 = PX + 18, PX + 470
a.add(a.text(C1, PY + 66, "/ip/ipsec/active-peers/print", 15, a.WHITE, a.MONO))
a.add(during(a, a.text(C2, PY + 66, "198.51.100.20  state=established", 15, MINT, a.MONO, 600), 9, 100, still=1))
a.add(during(a, a.text(C2, PY + 66, "(vacío)", 15, SKY, a.MONO), 0, 9))
a.add(a.text(C1, PY + 112, "/ip/ipsec/policy/print detail", 15, a.WHITE, a.MONO))
a.add(during(a, a.text(C2, PY + 112, "ph2-state=no-phase2", 15, GOLD, a.MONO, 600), 0, 30))
a.add(during(a, a.text(C2, PY + 112, "ph2-state=established", 15, MINT, a.MONO, 600), 30, 100, still=1))
a.add(a.text(C1, PY + 158, "/ip/ipsec/installed-sa/print", 15, a.WHITE, a.MONO))
a.add(during(a, a.text(C2, PY + 158, "ida     203.0.113.10 → 198.51.100.20", 15, SOFTW, a.MONO), 30, 100, still=1))
a.add(during(a, a.text(C2, PY + 222, "vuelta  198.51.100.20 → 203.0.113.10", 15, SOFTW, a.MONO), 32, 100, still=1))
a.add(during(a, a.text(C1, PY + 190, "current-bytes", 15, SKY, a.MONO) + a.text(C1, PY + 254, "current-bytes", 15, SKY, a.MONO), 30, 100, still=1))


def bar(y, col, pts, still=0.45):
    x, w, h = C2, 560, 14
    a.add(during(a, a.box(x, y, w, h, "#14496F", rx=7), 30, 100, still=1))
    k = a.keyframes(pts, "transform", "scaleX({})")
    a.add(during(a, a.group(a.box(x, y, w, h, col, rx=7), k, still=1, origin=f"{x}px {y}px"), 30, 100, still=0))
    a.add(still_only(a, f'<g transform="translate({x} {y}) scale({still} 1) translate({-x} {-y})">' + a.box(x, y, w, h, col, rx=7) + "</g>"))


bar(PY + 176, a.CYAN, [(0, 0.02), (52, 0.02), (70, 0.45), (78, 0.45), (95, 0.85), (100, 0.85)])
bar(PY + 240, MINT, [(0, 0.02), (55, 0.02), (73, 0.45), (100, 0.45)])
a.add(during(a, a.box(C2 - 6, PY + 228, 572, 38, "none", ROSE, rx=10, sw=3) + a.pill(C2 + 566, PY + 198, "no sube", a.BAD, a.BADBG, 14, 26, "end"), 86, 100))

narr(a, 48, 640, [
    (0, 25, "Empezá por la fase 1: sin peer establecido, lo demás no importa.", a.TXT, 0),
    (25, 50, "Dos SA por router, de un solo sentido: una de ida y una de vuelta.", a.TXT, 0),
    (50, 75, "Las dos suben: el tráfico entra y sale cifrado. Túnel sano.", a.OK, 1),
    (75, 100, "Solo sube la de ida: B recibe y descifra, pero su respuesta no vuelve por el túnel.", a.BAD, 0),
])

write(a, 22, "l1", "Mirá por capas: peer, fase 2 y los contadores",
      "Animación en cuatro tiempos entre el sitio A (MikroTik 203.0.113.10, LAN 192.168.88.0/24) y el sitio B (198.51.100.20, LAN 10.10.10.0/24), con lo que muestran en A tres comandos. "
      "1: fase 1: los dos peers arman el canal seguro y /ip/ipsec/active-peers/print muestra a 198.51.100.20 con state=established. "
      "2: fase 2: en /ip/ipsec/policy/print detail la policy pasa de ph2-state=no-phase2 a ph2-state=established, y /ip/ipsec/installed-sa/print muestra dos SA: la de ida, de 203.0.113.10 a 198.51.100.20, y la de vuelta, al revés. "
      "3: con un ping de la LAN de A a 10.10.10.5, sube current-bytes en la SA de ida y, con las respuestas, en la de vuelta: túnel sano. "
      "4: si solo sube la de ida, B recibe y descifra pero su respuesta no vuelve por el túnel: la falla está del otro lado, en el firewall, el bypass de NAT o el gateway de los equipos de B.",
      [5, 20, 40, 60, 70, 92])
