#!/usr/bin/env python3
"""Lección 6 · teoría: cómo la UCM lleva un DID a su interna (DID Mode, patrón, By DID con Strip, horario)."""
from _anim_grandstream import G

g = G(T=26, fix=72, kicker="GRANDSTREAM · RUTAS ENTRANTES", title="Del número llamado a la interna que suena")
g.steps([
    "Entra el INVITE. Con DID Mode en Request-line, la UCM lee el número de la primera línea.",
    "Lo compara con las rutas entrantes del troncal: coincide con _0655441XXX.",
    "By DID con Strip 6: saca 065544 y lo que queda, 1007, es la interna.",
    "En horario de oficina, la ruta manda la llamada a la interna 1007.",
    "Fuera de horario, la misma ruta la manda al buzón.",
])

# INVITE
g.add(g.box(48, 184, 640, 96, "#03213C", None, rx=14))
g.add(g.text(68, 216, "INVITE sip:0655441007@203.0.113.10 SIP/2.0", 16, "#D9E9F8", g.MONO, 500))
g.add(g.text(68, 246, "To: <sip:0655441007@203.0.113.10>", 16, "#9FC3E3", g.MONO, 500))
g.add(g.text(68, 268, "…", 16, "#9FC3E3", g.MONO, 500))
g.appear(g.box(172, 198, 100, 26, "none", "#FFD28A", rx=6, sw=2.5), 3, 40)
g.add(g.pillc(890, 206, "DID Mode: Request-line", g.BLUE, g.WHITE))
g.add(g.text(890, 252, "o To-header, según el proveedor", 14, g.GREY, g.SANS, 400, "middle"))

# patrón
g.add(g.box(48, 300, 640, 64, g.WHITE, g.LINE, rx=14))
g.add(g.text(68, 338, "Ruta entrante", 17, g.INK, g.SANS, 600))
g.add(g.text(210, 338, "_0655441XXX · By DID · Strip 6", 17, g.INK, g.MONO, 600))
g.appear(g.box(48, 300, 640, 64, "none", g.OK, rx=14, sw=3) + g.mark(660, 332, True, 13), 22, 100)

# Strip, dígito a dígito
DY, DW = 392, 50
digits = "0655441007"
for i, d in enumerate(digits):
    x = 48 + i * (DW + 8)
    g.add(g.box(x, DY, DW, 58, g.WHITE, g.LINE, rx=8))
    col = g.INK
    g.appear(g.text(x + DW / 2, DY + 38, d, 24, col, g.MONO, 600, "middle"), 41, 100)
    if i < 6:
        t = 43 + i * 1.6
        g.appear(g.box(x, DY, DW, 58, g.SLATE, None, rx=8) + g.text(x + DW / 2, DY + 38, d, 24, g.GREY, g.MONO, 600, "middle")
                 + f'<path d="M{x + 8} {DY + 50} L{x + DW - 8} {DY + 8}" stroke="{g.BAD}" stroke-width="3" stroke-linecap="round"/>', t, 100)
    else:
        g.appear(g.box(x, DY, DW, 58, g.OKBG, g.OK, rx=8, sw=2) + g.text(x + DW / 2, DY + 38, d, 24, g.OK, g.MONO, 600, "middle"), 54, 100)
g.appear(g.text(48, DY + 86, "Strip 6 cuenta caracteres desde la izquierda", 15, g.TXT, g.SANS, 600), 42, 100)

# horario y destinos
RX, RW = 780, 372
g.add(g.box(RX, 300, RW, 64, g.WHITE, g.LINE, rx=14))
g.add(g.text(RX + 20, 338, "Office Time/Holiday", 17, g.INK, g.SANS, 600))
g.appear(g.pillc(RX + RW - 86, 318, "en horario", g.OK, g.OKBG), 0, 80)
g.appear(g.pillc(RX + RW - 100, 318, "fuera de horario", g.AMB, g.AMBBG), 80, 100)
g.add(g.node(RX, 392, RW, 64, "Interna 1007", anchor="start"))
g.add(g.node(RX, 486, RW, 64, "Buzón de voz", anchor="start"))
g.arrow([(640, 421), (RX - 6, 424)], 61, 65, g.OK, hold=80)
g.appear(g.pillc(RX + RW - 70, 410, "suena", g.OK, g.OKBG), 65, 80)
g.arrow([(640, 421), (700, 421), (700, 518), (RX - 6, 518)], 82, 87, g.AMB, hold=100)
g.appear(g.pillc(RX + RW - 80, 504, "mensaje", g.AMB, g.AMBBG), 87, 100)

g.add(g.note(48, 572, 1104, None, ["Si el número llega con otro formato (59829…, +598…), cambian el patrón y el Strip: mirá el número real en el CDR.",
                                     "Lista negra global de entrantes: acepta números y también Anonymous."], "info"))

g.finish(6, 1, "Del número llamado a la interna que suena",
         "Animación en cinco tiempos sobre una llamada entrante por un troncal SIP, con el ejemplo oficial de Grandstream. "
         "1: entra el INVITE sip:0655441007@203.0.113.10; con DID Mode en Request-line la UCM lee el número de la primera línea (la otra opción es el encabezado To). "
         "2: lo compara con las rutas entrantes del troncal y coincide con el patrón _0655441XXX, destino By DID, Strip 6. "
         "3: Strip 6 tacha los seis primeros caracteres, 065544, y lo que queda, 1007, es la interna. "
         "4: con la condición de horario Office Time/Holiday en horario, la llamada va a la interna 1007, que suena. "
         "5: fuera de horario, la misma ruta manda la llamada al buzón de voz. "
         "Nota: si el número llega en otro formato, como 59829… o +598…, cambian el patrón y el Strip, por eso se mira el número real en el CDR; la lista negra global de entrantes acepta números y también Anonymous.",
         [10, 30, 50, 72, 92])
