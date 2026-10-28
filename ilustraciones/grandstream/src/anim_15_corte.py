#!/usr/bin/env python3
"""Lección 15 · teoría: el otro cuelga, Antel manda ocupado; con tonos de Uruguay la UCM corta, con los de fábrica no."""
from _anim_grandstream import G

g = G(T=26, fix=90, kicker="GRANDSTREAM · DETECCIÓN DE CORTE", title="El otro cuelga: ¿la UCM se entera?")
g.steps([
    "Dos UCM iguales con una llamada en curso por el FXO1; solo cambian los tonos.",
    "El otro cuelga: en analógico no hay mensaje; llega el tono de ocupado.",
    "Con los tonos de Uruguay cargados, la UCM cuenta 4 tonos (Busy Tone Count) y cuelga.",
    "Con los de fábrica (480 y 620 Hz) no lo reconoce: el FXO queda tomado.",
])
K = [0, 25, 50, 75, 100]
USO, LIBRE = "#F29A1F", "#0A63B8"

filas = [(196, "Tone Country: Custom · 425 Hz 500/500", True), (392, "Tone Country: de fábrica · 480+620 Hz", False)]
for y, lab, ok in filas:
    g.add(g.box(48, y, 1104, 168, g.WHITE, g.LINE, rx=16))
    g.add(g.text(72, y + 34, lab, 17, g.INK, g.MONO, 600))
    g.add(g.node(72, y + 58, 200, 84, "Antel", "la línea", dark=True))
    g.add(g.node(880, y + 58, 248, 84, "UCM · FXO1", None, dark=True))
    # tren de tonos de ocupado entre Antel y la UCM
    for k in range(6):
        x = 320 + k * 90
        burst = "".join(f"M{x + j * 4:.1f} {y + 84}V{y + 116}" for j in range(11))
        t0 = 26 + k * 4
        g.appear(f'<path d="{burst}" stroke="{g.AMB}" stroke-width="2"/>', t0, 100 if not ok else min(100, t0 + 30))
    g.appear(g.text(560, y + 140, "conversación", 15, g.GREY, g.SANS, 500, "middle"), 0, 25)
    g.appear(g.text(560, y + 140, "ocupado: 425 Hz, 0,5 s y 0,5 s", 15, g.AMB, g.SANS, 600, "middle"), 25, 100)
    g.appear(f'<path d="M272 {y + 100}H880" stroke="{g.OK}" stroke-width="4"/>', 0, 25)
    if ok:
        for n in range(4):
            g.appear(g.pillc(700 + n * 40, y + 30, str(n + 1), g.WHITE, g.BLUE, size=15, h=26), 52 + n * 4, 72)
        g.appear(g.pillc(1004, y + 38, "en uso", g.WHITE, USO, size=15, h=28), 0, 70)
        g.appear(g.pillc(1004, y + 38, "libre", g.WHITE, LIBRE, size=15, h=28), 70, 100)
        g.appear(g.mark(936, y + 38, True, 14) + g.text(912, y + 44, "cortó", 15, g.OK, g.SANS, 600, "end"), 70, 100)
    else:
        g.appear(g.pillc(1004, y + 38, "en uso", g.WHITE, USO, size=15, h=28), 0, 100)
        g.appear(g.mark(936, y + 38, False, 14) + g.text(912, y + 44, "sigue tomado", 15, g.BAD, g.SANS, 600, "end"), 78, 100)

g.appear(g.note(48, 584, 1104, None, ["Busy Tone Count 2 de fábrica; el manual sugiere 4, 6 u 8. Más alto corta más tarde, y muy alto puede no cortar nunca."], "info"), 0, 75)
g.appear(g.note(48, 584, 1104, None, ["Con la línea tomada, el próximo que llama da ocupado y el buzón puede grabar dos minutos de tono."], "bad"), 75, 100)

g.finish(15, 1, "El otro cuelga: ¿la UCM se entera?",
         "Animación en cuatro tiempos con dos filas iguales: Antel conectada al FXO1 de una UCM. Arriba, la troncal con Tone Country en Custom y el ocupado de Uruguay, 425 Hz 500/500; abajo, con los tonos de fábrica de Estados Unidos, 480 y 620 Hz. "
         "1: hay una llamada en curso en las dos y el FXO1 figura en uso. "
         "2: el que llamó cuelga; en analógico no hay un mensaje de corte y, en una línea que corta por tono como muchas de Sudamérica, llega el ocupado de 425 Hz, medio segundo sí y medio no. "
         "3: arriba, la UCM reconoce el tono, cuenta cuatro (Busy Tone Count) y cuelga: el FXO1 pasa a libre. "
         "4: abajo, con los tonos de fábrica no lo reconoce y el FXO1 queda tomado; el próximo que llama da ocupado y el buzón puede grabar el tono. "
         "Nota: Busy Tone Count viene en 2 y el manual sugiere 4, 6 u 8; más alto corta más tarde y muy alto puede no cortar nunca.",
         [12, 37, 62, 90])
