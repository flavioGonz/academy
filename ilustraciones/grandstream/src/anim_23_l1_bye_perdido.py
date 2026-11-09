#!/usr/bin/env python3
"""Caso de estudio · Cuelga y no corta · Laboratorio, paso 2: 23-l1.svg.
El BYE que no llega: con la regla del MikroTik que tira la señalización de la UCM hacia la 1002 (10.10.10.32:5060),
la UCM manda el BYE y lo repite (RFC 3261, transacción no INVITE por UDP: Timer E desde T1 = 500 ms, se duplica hasta
T2 = 4 s, y se rinde a los 64 × T1 = 32 s, Timer F). La 1002 sigue en llamada, sin RTP, hasta su propio RTP timeout
(30 s de fábrica en un GXV3350). Datos de ejemplo.
"""
from _anim_gs_red import R

g = R(T=28, fix=94, kicker="GRANDSTREAM · CASO DE ESTUDIO · PASO 2", title="El BYE que no llega, en la captura")
g.steps([
    "La 1001 cuelga: la UCM le manda BYE a la 1002 por 10.10.10.32:5060.",
    "La regla del MikroTik lo tira: no hay 200 OK y la UCM lo repite.",
    "Repite cada vez más espaciado; a los 32 s se rinde. La 1002, en silencio.",
    "La 1002 corta sola a los 30 s: su RTP timeout. Se saca la regla.",
], size=17)

B, OK, BAD, GREY, INK, AMB = g.BLUE, g.OK, g.BAD, g.GREY, g.INK, g.AMB
g.add(g.dev(48, 172, 230, 76, "UCM", "192.168.88.20", icon="ucm", dark=True))
g.add(g.dev(486, 172, 230, 76, "MikroTik", "regla ies-lab-bye", icon="router", hl=BAD))
g.add(g.dev(922, 172, 230, 76, "1002", "10.10.10.32", icon="phone"))
g.add(g.wire(278, 210, 486, 210, w=3))
g.add(g.wire(716, 210, 922, 210, w=3))
g.appear(g.pillc(601, 262, "drop · udp 5060 hacia 10.10.10.32", BAD, g.BADBG, 13, 26), 0, 82, still=0)
g.appear(g.pillc(601, 262, "regla quitada", OK, g.OKBG, 13, 26), 84, 100)
g.appear(g.pillc(1037, 262, "en llamada, en silencio", AMB, g.AMBBG, 13, 26), 8, 74, still=0)
g.appear(g.pillc(1037, 262, "cortó: RTP Timeout Timer", OK, g.OKBG, 13, 26), 76, 100)

# línea de tiempo de las retransmisiones
X0, PX, TY = 120, 1000 / 34, 356
g.add(g.text(48, TY - 46, "Retransmisiones del BYE (segundos desde que colgó la 1001)", 16, INK, g.SANS, 600))
g.add(g.box(X0, TY, 1000, 4, g.LINE, rx=2))
for s_ in (0, 8, 16, 24, 32):
    x = X0 + s_ * PX
    g.add(f'<line x1="{x:.0f}" y1="{TY - 6}" x2="{x:.0f}" y2="{TY + 10}" stroke="{GREY}" stroke-width="1.5"/>')
    g.add(g.text(x, TY + 30, f"{s_}", 14, GREY, g.MONO, 400, "middle"))
sends = [0, 0.5, 1.5, 3.5, 7.5, 11.5, 15.5, 19.5, 23.5, 27.5, 31.5]
for k, s_ in enumerate(sends):
    t0 = 6 + s_ * 1.9
    x = X0 + s_ * PX
    g.appear(f'<rect x="{x - 4:.0f}" y="{TY - 30}" width="8" height="24" rx="3" fill="{B}"/>', t0, 100 if k else 100)
    g.token([(278, 196), (486, 196)], t0, t0 + 2, g.chip("BYE", bg=B, size=12, h=22), hold=t0 + 2.3)
g.appear(g.text(X0 + 32 * PX + 16, TY - 14, "Timer F", 14, BAD, g.MONO, 600), 68, 100)
g.appear(g.mark(458, 196, False, 12), 8, 82, still=0)
# RTP timeout del teléfono
g.add(g.text(48, TY + 70, "1002: segundos sin RTP (misma escala)", 16, INK, g.SANS, 600))
g.add(g.box(X0, TY + 84, 30 * PX, 24, g.SLATE, rx=6))
g.bar(X0, TY + 84, 30 * PX, 24, 8, 66, AMB)
g.appear(g.text(X0 + 12 + 30 * PX, TY + 102, "30 s: corta", 15, OK, g.MONO, 600), 66, 100)

g.add(g.box(48, 490, 1104, 136, g.WHITE, g.LINE, rx=14))
ROWS = [(0, 25, "Ethernet Capture en la UCM: el BYE sale hacia el Contact de la 1002", "10.10.10.32:5060, la dirección que la 1002 dio al llamar", INK),
        (25, 50, "Sin 200 OK, la UCM repite el BYE: 0,5 s, 1 s, 2 s y después cada 4 s", "RFC 3261 por UDP: Timer E desde T1 hasta T2, Timer F a los 32 s", BAD),
        (50, 74, "La 1002 no se entera: queda en llamada con nadie del otro lado", "lo mismo que hace el router de la casa cuando se olvida del puerto", AMB),
        (74, 100, "Lo que la corta es su propio RTP timeout: 30 s en un GXV3350", "si siempre corta al mismo tiempo, es un timer y no el BYE", OK)]
for t0, t1, a, b, col in ROWS:
    g.appear(g.text(72, 538, a, 17, INK, g.SANS, 600) + g.text(72, 580, b, 16, col, g.SANS, 600), t0, t1)

g.done(23, "l1", "El BYE que no llega, en la captura",
       "Animación en cuatro tiempos con la UCM 192.168.88.20, el MikroTik del banco con la regla ies-lab-bye y la 1002 en 10.10.10.32; abajo, una línea de tiempo de 0 a 32 segundos con cada envío del BYE y una barra con los segundos sin RTP de la 1002. "
       "1: la 1001 cuelga y la UCM manda BYE a la 1002, a 10.10.10.32 puerto 5060, el Contact que la 1002 dio al llamar. "
       "2: la regla del MikroTik descarta el UDP 5060 hacia la 1002: no hay 200 OK y la UCM repite el BYE. "
       "3: lo repite a los 0,5, 1,5 y 3,5 segundos y después cada 4, como dice la RFC 3261 para una transacción por UDP, y a los 32 segundos se rinde, Timer F; mientras tanto la 1002 queda en llamada, en silencio. "
       "4: la 1002 corta sola cuando vence su RTP timeout, 30 segundos de fábrica en un GXV3350; si lo colgado corta siempre al mismo tiempo, es un timer y no el BYE. Después se quita la regla. Datos de ejemplo.",
       [6, 12, 30, 46, 60, 70, 80, 94])
