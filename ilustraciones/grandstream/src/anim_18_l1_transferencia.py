#!/usr/bin/env python3
"""Lección 18 (Diagnóstico de línea) · Laboratorio, paso 3: el teléfono de prueba en la línea 2. El tono normal es
425 Hz continuo; con la transferencia temporal de Antel activa se escucha un tono distinto y las entrantes se desvían
en la central de Antel, así que la línea no suena. Fuentes: la lección (con la transferencia de Antel activa se escucha
un tono distinto), página de Antel de Transferencia temporal incondicional (todas las entrantes se transfieren a otro
número; con la facilidad activa se escucha un tono de libre distinto del normal; verificación *#21*NNNNNNNN# sin cargo,
cancelación #21# con un cómputo), ITU E.180 (invitación a marcar de Uruguay 425 Hz continuo)."""
from _anim_gs_red import R

g = R(T=26, fix=70, kicker="GRANDSTREAM · DIAGNÓSTICO DE LÍNEA · LABORATORIO",
      title="El tono de la línea 2: normal o con un servicio activo")
g.steps([
    "Descolgás el teléfono de prueba en el par 2: el tono normal es 425 Hz continuo.",
    "Si suena distinto, hay una facilidad activa: con la transferencia, otro tono de libre.",
    "Con la transferencia activa, Antel desvía las entrantes: la línea 2 no suena.",
    "Se anota y se habla con el cliente: *#21*número# la verifica; #21# la cancela.",
])

PAR = "#3B4D61"
def par(x1, y1, x2, y2):
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{PAR}" stroke-width="8" stroke-linecap="round"/>'
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#F7FAFD" stroke-width="2"/>')

Y = 240
g.add(g.dev(48, Y, 250, 96, "Teléfono de prueba", "en el par 2", icon="tel"))
g.add(par(298, Y + 48, 460, Y + 48))
g.add(g.dev(460, Y, 260, 96, "Central de Antel", "línea 2", icon="antel", dark=True))
g.add(g.dev(900, 186, 252, 84, "Cliente", "llama a la línea 2", icon="phone"))
g.add(g.dev(900, 300, 252, 84, "Otro número", "destino del desvío", icon="phone"))
g.add(g.wire(720, Y + 30, 900, 228, g.LINE, 3, "6 6"))
g.add(g.wire(720, Y + 66, 900, 342, g.LINE, 3, "6 6"))

# lo que escucha
SX, SY = 48, 372
g.add(g.box(SX, SY, 672, 132, "#03213C", None, rx=14))
g.add(g.text(SX + 20, SY + 30, "lo que se escucha al descolgar", 14, g.SKY, g.MONO))
BASE = SY + 84
g.appear(f'<rect x="{SX + 20}" y="{BASE - 22}" width="420" height="44" rx="6" fill="{g.MINT}" opacity=".85"/>'
         + g.text(SX + 460, BASE + 7, "425 Hz continuo", 18, g.MINT, g.MONO, 600), 2, 25)
tono2 = "".join(f'<rect x="{SX + 20 + k * 84}" y="{BASE - 22}" width="{50 if k % 2 == 0 else 24}" height="44" rx="6" fill="{g.GOLD}" opacity=".85"/>' for k in range(5))
g.appear(tono2 + g.text(SX + 460, BASE + 7, "un tono distinto", 18, g.GOLD, g.MONO, 600), 27, 100)
g.appear(g.text(SX + 20, SY + 124, "dibujo esquemático: Antel describe el tono solo como distinto del normal", 13, g.SKY, g.SANS), 27, 100)
g.appear(g.pillc(173, Y - 14, "tono normal", g.OK, g.OKBG, 13, 26), 4, 25)
g.appear(g.pillc(173, Y - 14, "tono distinto: anotalo", g.AMB, g.AMBBG, 13, 26), 27, 100)

# 3 · desvío
g.token([(1026, 270), (820, 270), (720, Y + 30)], 52, 58, g.chip("llamada", bg=g.CYAN, size=13, h=24), hold=59)
g.token([(720, Y + 66), (846, 328)], 59, 66, g.chip("desviada", bg=g.AMB, size=13, h=24), hold=75)
g.appear(g.mark(380, Y + 48, False, 14) + g.text(380, Y + 86, "no suena", 15, g.BAD, g.MONO, 600, "middle"), 60, 100)
g.appear(g.pillc(1026, 394, "suena acá", g.AMB, g.AMBBG, 13, 26), 66, 100)
g.fijo_only(f'<g transform="translate(846 328)">' + g.chip("desviada", bg=g.AMB, size=13, h=24) + '</g>')

g.add(g.box(744, 446, 408, 150, g.WHITE, g.LINE, rx=14))
g.add(g.text(764, 476, "Transferencia temporal (Antel)", 15, g.INK, g.SANS, 600))
g.add(g.text(764, 506, "verificar: *#21*NNNNNNNN#", 15, g.TXT, g.MONO) + g.text(1132, 506, "sin cargo", 13, g.OK, g.SANS, 600, "end"))
g.add(g.text(764, 534, "cancelar: #21#", 15, g.TXT, g.MONO) + g.text(1132, 534, "un cómputo", 13, g.AMB, g.SANS, 600, "end"))
g.add(g.text(764, 566, "NNNNNNNN: el número de destino", 13, g.GREY, g.SANS))
g.appear(g.box(744, 446, 408, 150, "none", g.BLUE, rx=14, sw=3), 77, 100)

g.status(628, [
    (0, 25, "Con el tono normal, la línea está como tiene que estar para salir.", g.OK),
    (25, 50, "Un tono raro no es la UCM: es algo que tiene programado la línea.", g.AMB),
    (50, 75, "Puede explicar el día que la línea 2 no recibía: las llamadas iban a otro lado.", g.AMB),
    (75, 100, "Cancelarla es decisión del cliente: se anota y se consulta antes.", g.INK),
])

g.done(18, "l1", "El tono de la línea 2: normal o con un servicio activo",
       "Animación en cuatro tiempos con el teléfono de prueba conectado al par 2, la central de Antel, un cliente que llama a la línea 2 y el otro número de una transferencia; abajo, lo que se escucha al descolgar y los códigos de la transferencia temporal de Antel. "
       "1: al descolgar el teléfono de prueba se escucha el tono normal de invitación a marcar, 425 Hz continuo. "
       "2: si suena distinto, la línea tiene una facilidad activa; con la transferencia temporal, Antel dice que se escucha un tono de libre distinto del normal; el dibujo del tono es esquemático. "
       "3: con la transferencia activa, la central de Antel desvía las entrantes al otro número: la línea 2 no suena y la UCM no ve nada, lo que puede explicar el día en que la línea 2 no recibía. "
       "4: se anota y se habla con el cliente: *#21* seguido del número y # la verifica sin cargo, y #21# la cancela con un cómputo.",
       [8, 36, 62, 90])
