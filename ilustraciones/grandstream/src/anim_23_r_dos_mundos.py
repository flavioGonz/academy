#!/usr/bin/env python3
"""Caso de estudio · Cuelga y no corta · Resumen ("Cómo se ve en la red"): 23-r1.svg.
El caso con sus dos mundos: arriba, FXO (el celular cuelga, la línea de Antel manda ocupado de 425 Hz, la UCM con
tonos de fábrica no lo reconoce y la troncal queda tomada; con los tonos de Uruguay lo detecta y libera); abajo, SIP
(recepción cuelga, el BYE de la UCM no pasa el router del vendedor porque el NAT venció, el teléfono sigue hasta su RTP
timeout de 30 s en un GXV3350; con Enable Keep-alive el camino queda abierto y el BYE llega). Datos de ejemplo.
"""
from _anim_gs_red import R

g = R(T=28, fix=94, kicker="GRANDSTREAM · CASO DE ESTUDIO · CUELGA Y NO CORTA", title="El caso en la red: dos mundos, el mismo síntoma")
g.steps([
    "FXO: el cliente cuelga; Antel manda ocupado y la UCM no lo reconoce.",
    "La troncal queda tomada y la interna, con el tu tu tu. Arreglo: Tonos y corte.",
    "SIP: recepción cuelga; el BYE no pasa el router del vendedor: el NAT venció.",
    "Con Keep-alive el camino sigue abierto: el BYE llega y el teléfono corta.",
], size=17)

B, OK, BAD, GREY, INK, AMB = g.BLUE, g.OK, g.BAD, g.GREY, g.INK, g.AMB
# fila FXO
Y1 = 180
g.add(g.text(48, Y1 - 8, "FXO · línea de Antel", 15, AMB, g.SANS, 600))
g.add(g.dev(48, Y1, 220, 72, "Celular", "colgó", icon="phone"))
g.add(g.dev(330, Y1, 220, 72, "Línea Antel", "FXO1", icon="antel"))
g.add(g.dev(612, Y1, 220, 72, "UCM", "Busy Detection", icon="ucm", dark=True))
g.add(g.dev(894, Y1, 258, 72, "Interna 1001", "recepción", icon="tel"))
for x1, x2 in ((268, 330), (550, 612), (832, 894)):
    g.add(g.wire(x1, Y1 + 36, x2, Y1 + 36, w=3))
for t0 in (4, 9, 14, 19):
    g.token([(550, Y1 + 36), (612, Y1 + 36)], t0, t0 + 2.5, g.chip("425 Hz", bg=AMB, size=12, h=22), hold=t0 + 3)
g.appear(g.pillc(722, Y1 + 84, "tonos de fábrica: no reconoce el ocupado", BAD, g.BADBG, 13, 26), 6, 50, still=0)
g.appear(g.pillc(1023, Y1 + 84, "tu tu tu · troncal tomada", BAD, g.BADBG, 13, 26), 27, 50, still=0)
g.appear(g.pillc(722, Y1 + 84, "tonos de Uruguay: detecta y libera", OK, g.OKBG, 13, 26), 52, 100)
g.appear(g.pillc(1023, Y1 + 84, "la interna queda libre", OK, g.OKBG, 13, 26), 54, 100)

# fila SIP
Y2 = 352
g.add(g.text(48, Y2 - 8, "SIP · vendedor en la casa", 15, BAD, g.SANS, 600))
g.add(g.dev(48, Y2, 220, 72, "Recepción", "colgó", icon="tel"))
g.add(g.dev(330, Y2, 220, 72, "UCM", "manda el BYE", icon="ucm", dark=True))
g.add(g.dev(612, Y2, 220, 72, "Router casa", "NAT del puerto SIP", icon="router"))
g.add(g.dev(894, Y2, 258, 72, "Teléfono", "del vendedor", icon="phone"))
for x1, x2 in ((268, 330), (550, 612), (832, 894)):
    g.add(g.wire(x1, Y2 + 36, x2, Y2 + 36, w=3))
for t0 in (54, 58, 62):
    g.token([(550, Y2 + 36), (612, Y2 + 36)], t0, t0 + 2.5, g.chip("BYE", bg=B, size=12, h=22), hold=t0 + 2.8)
g.appear(g.mark(722, Y2 + 96, False, 13), 55, 76, still=0)
g.appear(g.pillc(1023, Y2 + 84, "sigue en llamada: corta a los 30 s", BAD, g.BADBG, 13, 26), 57, 76, still=0)
for t0 in (78, 82):
    g.token([(560, Y2 - 16), (884, Y2 - 16)], t0, t0 + 3, g.chip("OPTIONS", bg=GREY, size=12, h=22))
g.token([(560, Y2 - 16), (884, Y2 - 16)], 88, 92, g.chip("BYE", bg=OK, size=12, h=22), hold=100, still=0)
g.appear(g.pillc(722, Y2 + 84, "Keep-alive: el camino sigue abierto", OK, g.OKBG, 13, 26), 78, 100)
g.appear(g.pillc(1023, Y2 + 84 + 0, "corta al instante", OK, g.OKBG, 13, 26), 92, 100)
g.fijo_only(f'<g transform="translate(860 {Y2 - 16})">' + g.chip("BYE", bg=OK, size=12, h=22) + "</g>")

g.add(g.box(48, 514, 1104, 112, g.WHITE, g.LINE, rx=14))
ROWS = [(0, 25, "En cobre no hay mensaje de corte: la UCM lo tiene que detectar", "ocupado de 425 Hz, polaridad o corriente: PSTN Detection lo mide", INK),
        (25, 50, "Firma FXO: troncal analógica en Active Calls y la interna con el ocupado", "red de seguridad: Maximum Call Duration y Max Message Length del buzón", AMB),
        (50, 76, "Firma SIP: BYE repetido sin 200 OK en la captura", "el teléfono corta solo cuando vence su propio RTP timeout", BAD),
        (76, 100, "Enable Keep-alive cada 20 s y NAT en la extensión del vendedor", "en la UCM, RTP Timeout y Session Timer como red de seguridad", OK)]
for t0, t1, a, b, col in ROWS:
    g.appear(g.text(72, 554, a, 17, INK, g.SANS, 600) + g.text(72, 590, b, 16, col, g.SANS, 600), t0, t1)

g.done(23, "r1", "El caso en la red: dos mundos, el mismo síntoma",
       "Animación en cuatro tiempos con dos filas. Arriba, FXO: el celular del cliente, la línea de Antel por el FXO1, la UCM con Busy Detection y la interna 1001. Abajo, SIP: recepción, la UCM, el router de la casa del vendedor y su teléfono. "
       "1: el cliente cuelga y la línea manda ocupado de 425 hercios; con los tonos de fábrica la UCM no lo reconoce. "
       "2: la troncal analógica queda tomada y la interna sigue con el tu tu tu; con los tonos de Uruguay, la UCM detecta el corte y libera la línea, lo de la lección Tonos y corte. "
       "3: recepción cuelga una llamada con el vendedor y la UCM manda el BYE, pero el router de la casa ya cerró el puerto SIP: el BYE se repite sin 200 OK y el teléfono sigue en llamada hasta su propio RTP timeout, 30 segundos en un GXV3350. "
       "4: con Enable Keep-alive cada 20 segundos en la extensión, los OPTIONS de la UCM mantienen abierto el camino, el BYE llega y el teléfono corta al instante; RTP Timeout y Session Timer quedan como red de seguridad. Datos de ejemplo.",
       [8, 20, 34, 46, 60, 70, 86, 95])
