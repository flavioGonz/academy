#!/usr/bin/env python3
"""Caso de estudio · Cuelga y no corta · Laboratorio, paso 4: 23-l2.svg.
El teléfono que desaparece: se desenchufa la 1002 en plena llamada con la 1001. Sin RTP Timeout (de fábrica en la UCM)
la llamada sigue en Active Calls hasta que alguien cuelga; con RTP Timeout 60 (PBX Settings > SIP Settings > ToS)
la UCM corta a los 60 s sin audio de la 1002 y libera a la 1001. Valores de ejemplo.
"""
from _anim_gs_red import R

g = R(T=28, fix=94, kicker="GRANDSTREAM · CASO DE ESTUDIO · PASO 4", title="El teléfono que desaparece y la red que corta")
g.steps([
    "Llamada de la 1001 a la 1002: el audio va y viene por la UCM.",
    "Se desenchufa la 1002: deja de llegar su RTP. La 1001 queda en silencio.",
    "Sin RTP Timeout, Active Calls la sigue mostrando: nadie la corta.",
    "Con RTP Timeout 60, a los 60 s sin audio la UCM corta y libera a la 1001.",
], size=17)

B, OK, BAD, GREY, INK, AMB = g.BLUE, g.OK, g.BAD, g.GREY, g.INK, g.AMB
g.add(g.dev(48, 172, 250, 76, "1001", "recepción", icon="tel"))
g.add(g.dev(475, 172, 250, 76, "UCM", "PBX Settings > ToS", icon="ucm", dark=True))
g.add(g.dev(902, 172, 250, 76, "1002", "10.10.10.32", icon="phone"))
g.add(g.wire(298, 210, 475, 210, w=3))
g.add(g.wire(725, 210, 902, 210, w=3))
g.appear(g.box(890, 160, 274, 100, "none", BAD, rx=16, sw=2.5, extra='stroke-dasharray="7 6"'), 26, 100)
# 1 · audio de ida y vuelta
for t0 in (3, 9, 15):
    g.token([(298, 196), (475, 196)], t0, t0 + 3, g.chip("RTP", bg=OK, size=12, h=22))
    g.token([(902, 224), (725, 224)], t0 + 1, t0 + 4, g.chip("RTP", bg=OK, size=12, h=22))
# 2 · deja de llegar RTP de la 1002
for t0 in (28, 34, 40):
    g.token([(298, 196), (475, 196)], t0, t0 + 3, g.chip("RTP", bg=OK, size=12, h=22))
g.appear(g.mark(812, 224, False, 13), 28, 100)
g.appear(g.pillc(813, 262, "no llega RTP de la 1002", BAD, g.BADBG, 13, 26), 28, 100)
g.appear(g.pillc(173, 262, "en silencio", AMB, g.AMBBG, 13, 26), 30, 86, still=0)
g.appear(g.pillc(173, 262, "libre: la UCM cortó", OK, g.OKBG, 13, 26), 88, 100)
g.msg(475, 298, 300, "BYE", B, 86, 90, size=14)

# Active Calls
PX, PY = 48, 336
g.add(g.box(PX, PY, 540, 140, g.WHITE, g.LINE, rx=14))
g.add(g.text(PX + 20, PY + 30, "System Status > Active Calls", 15, B, g.MONO, 600))
g.appear(g.box(PX + 16, PY + 48, 508, 40, g.SLATE, rx=8) + g.text(PX + 32, PY + 74, "1001 y 1002", 16, INK, g.MONO, 600), 0, 88, still=0)
g.appear(g.text(PX + 380, PY + 74, "en curso", 15, GREY, g.MONO), 0, 50, still=0)
g.appear(g.text(PX + 380, PY + 74, "sigue…", 15, AMB, g.MONO, 600), 50, 75, still=0)
g.appear(g.text(PX + 380, PY + 74, "cortada", 15, OK, g.MONO, 600), 88, 100)
g.appear(g.text(PX + 32, PY + 116, "sin llamadas activas", 15, OK, g.SANS, 600), 89, 100)
g.appear(g.text(PX + 32, PY + 116, "sin RTP Timeout: hasta que alguien cuelga", 15, BAD, g.SANS, 600), 52, 75, still=0)

# reloj de RTP Timeout
TX = 612
g.add(g.box(TX, PY, 540, 140, g.WHITE, g.LINE, rx=14))
g.add(g.text(TX + 20, PY + 30, "RTP Timeout · segundos sin audio de la 1002", 15, INK, g.SANS, 600))
g.add(g.box(TX + 20, PY + 52, 500, 26, g.SLATE, rx=6))
g.bar(TX + 20, PY + 52, 500, 26, 28, 74, BAD, hold=76, still=0)
g.appear(g.text(TX + 20, PY + 108, "sin configurar: no cuenta", 15, BAD, g.SANS, 600), 52, 75, still=0)
g.bar(TX + 20, PY + 52, 500, 26, 76, 86, AMB)
g.appear(g.text(TX + 20, PY + 108, "RTP Timeout: 60 · a los 60 s corta", 15, OK, g.MONO, 600), 86, 100)
g.add(g.text(TX + 520, PY + 108, "60 s", 14, GREY, g.MONO, 400, "end"))

g.add(g.box(48, 500, 1104, 126, g.WHITE, g.LINE, rx=14))
ROWS = [(0, 25, "Con Direct Media apagado, el audio de los dos pasa por la UCM", "por eso la central nota cuando un lado deja de mandar", INK),
        (25, 50, "Un cable desenchufado no manda BYE: la llamada queda viva", "la 1001 escucha silencio y la línea queda ocupada", AMB),
        (50, 75, "RTP Timeout viene sin timeout de fábrica", "Session Timer solo actúa si el otro lado lo negoció: 1800 s", BAD),
        (75, 100, "RTP Timeout 60 y RTP Hold Timeout 300 en PBX Settings > SIP Settings > ToS", "probalo con los equipos del cliente: en mute algunos dejan de mandar audio", OK)]
for t0, t1, a, b, col in ROWS:
    g.appear(g.text(72, 548, a, 17, INK, g.SANS, 600) + g.text(72, 590, b, 16, col, g.SANS, 600), t0, t1)

g.done(23, "l2", "El teléfono que desaparece y la red que corta",
       "Animación en cuatro tiempos con la 1001 de recepción, la UCM y la 1002, que se desenchufa; abajo, Active Calls y un reloj con los segundos sin audio de la 1002. "
       "1: llamada de la 1001 a la 1002, con el audio de ida y vuelta pasando por la UCM. "
       "2: se desenchufa la 1002: deja de llegar su RTP, no manda BYE y la 1001 queda en silencio. "
       "3: sin RTP Timeout, que viene sin timeout de fábrica, la llamada sigue en Active Calls hasta que alguien cuelga; Session Timer solo actúa si el otro lado lo negoció. "
       "4: con RTP Timeout en 60 y RTP Hold Timeout en 300, en PBX Settings > SIP Settings > ToS, a los 60 segundos sin audio la UCM corta, le manda BYE a la 1001 y la libera. Conviene probarlo con los equipos del cliente, porque en mute algunos dejan de mandar audio.",
       [8, 20, 34, 46, 60, 70, 86, 95])
