#!/usr/bin/env python3
"""Lección 13 (Qué trae el par) · Resumen, "Cómo se ve en la red": un panel de alarma en paralelo con el FXO2 toma la
línea para reportar; para Antel la línea queda ocupada y el cliente que llama recibe ocupado; cuando la alarma
corta, la próxima llamada suena en la UCM. Fuentes: la lección (todo lo que cuelga del mismo par puede descolgar y
la línea queda ocupada para la central de Antel; ejemplo de la alarma que reporta por la línea 2; al descolgar la
tensión cae a pocos voltios; tensión de reposo de unos 48 V según las fuentes)."""
from _anim_gs_red import R

g = R(T=26, fix=62, kicker="GRANDSTREAM · QUÉ TRAE EL PAR · CÓMO SE VE EN LA RED",
      title="Una línea, varios equipos: la alarma toma el par")
g.steps([
    "En reposo, el par tiene tensión y todo lo que cuelga de él la ve: la línea está libre.",
    "La alarma reporta: descuelga, cierra el lazo y la tensión cae. La línea está tomada.",
    "Un cliente llama a esa línea: Antel le da ocupado y el FXO2 nunca ve el timbre.",
    "La alarma corta: vuelve la tensión de reposo y la próxima llamada suena en el FXO2.",
])

PAR = "#3B4D61"
def par(x1, y1, x2, y2):
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{PAR}" stroke-width="8" stroke-linecap="round"/>'
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#F7FAFD" stroke-width="2" stroke-linecap="round"/>')

PY = 340
g.add(g.dev(48, PY - 48, 240, 96, "Central de Antel", "da tensión y timbre", icon="antel", dark=True))
g.add(par(288, PY, 1000, PY))
g.add(g.text(560, PY + 30, "par de cobre · línea 2", 15, g.GREY, g.MONO, 400, "middle"))
g.add(g.dev(1000, PY - 48, 152, 96, "UCM", "FXO2", icon="ucm", dark=True))
# alarma en paralelo
AX = 700
g.add(par(AX, PY, AX, 256))
g.add(g.dev(AX - 130, 178, 260, 78, "Panel de alarma", "en paralelo", icon="alarma"))
# cliente
g.add(g.dev(48, 500, 240, 84, "Cliente", "llama a la línea 2", icon="phone"))
g.add(g.wire(168, 500, 168, PY + 48, g.LINE, 3, "6 6"))

# tensión
VX, VY = 330, 470
g.add(g.box(VX, VY, 420, 120, "#03213C", None, rx=14))
g.add(g.text(VX + 20, VY + 30, "tensión en el par (continua)", 14, g.SKY, g.MONO))
g.appear(g.text(VX + 20, VY + 82, "reposo · unos 48 V", 26, g.MINT, g.MONO, 600), 0, 27)
g.appear(g.text(VX + 20, VY + 82, "cae a pocos voltios", 26, g.GOLD, g.MONO, 600), 27, 78)
g.appear(g.text(VX + 20, VY + 82, "reposo otra vez", 26, g.MINT, g.MONO, 600), 78, 100)
g.appear(g.text(VX + 20, VY + 108, "alguien cerró el lazo", 14, g.GOLD, g.SANS, 600), 30, 78)

# estado de la alarma y de la línea
g.appear(g.pillc(AX + 230, 204, "colgada", g.GREY, g.SLATE, 13, 26), 0, 27)
g.appear(g.pillc(AX + 230, 204, "descolgada: reporta", g.AMB, g.AMBBG, 13, 26), 27, 78)
g.appear(g.pillc(AX + 230, 204, "colgada", g.GREY, g.SLATE, 13, 26), 78, 100)
g.appear(g.box(288, PY - 6, AX - 288, 12, "#F29A1F", None, rx=6), 27, 78)
g.appear(g.pillc(1076, PY + 62, "ve la línea tomada", g.AMB, g.AMBBG, 13, 26), 30, 78)
g.appear(g.pillc(1076, PY + 62, "libre", g.BLUE, "#E6F0FA", 13, 26), 0, 27)
# 2 · el reporte
for k in range(2):
    t = 30 + k * 7
    g.token([(AX, 266), (AX, PY - 4), (330, PY - 4)], t, t + 6, g.chip("reporte", bg=g.AMB, size=13, h=24), hold=t + 6.3)
# 3 · el cliente recibe ocupado
g.token([(168, 500), (168, PY + 60)], 52, 57, g.chip("llamada", bg=g.CYAN, size=13, h=26), hold=58)
g.token([(168, PY + 60), (168, 500)], 59, 64, g.chip("ocupado", bg=g.BAD, size=13, h=26), hold=75)
g.appear(g.mark(960, PY - 40, False, 14) + g.text(940, PY - 34, "sin timbre", 15, g.BAD, g.MONO, 600, "end"), 58, 75)
# 4 · ahora sí
g.token([(168, 500), (168, PY + 60), (980, PY + 60)], 82, 92, g.chip("timbre", bg=g.OK, size=13, h=26), hold=95)
g.appear(g.pillc(1076, PY + 62, "suena", g.OK, g.OKBG, 13, 26), 92, 100)
g.fijo_only(f'<g transform="translate(168 {PY + 100})">' + g.chip("ocupado", bg=g.BAD, size=13, h=26) + '</g>')

g.appear(g.note(790, 470, 362, "Antes de conectar", ["Se recorre el par y se anota todo", "lo que cuelga: alarma, posnet,", "fax, teléfonos sueltos."], "info"), 0, 50)
g.appear(g.note(790, 470, 362, "Para probar", ["Una línea con un solo equipo:", "el resto se desconecta mientras", "dura la prueba."], "ok"), 50, 100)

g.done(13, "r1", "Una línea, varios equipos: la alarma toma el par",
       "Animación en cuatro tiempos con la central de Antel, el par de cobre de la línea 2 que llega al FXO2 de la UCM y un panel de alarma conectado en paralelo; abajo, un cliente que llama y la tensión en el par. "
       "1: en reposo, el par tiene tensión continua, unos 48 V en muchas líneas, y todos los equipos la ven: la línea está libre. "
       "2: la alarma reporta a la empresa de monitoreo: descuelga, cierra el lazo y la tensión cae a pocos voltios; el FXO2 ve la línea tomada. "
       "3: un cliente llama a la línea 2; para Antel está ocupada, le da ocupado y el FXO2 nunca ve el timbre. "
       "4: la alarma corta, vuelve la tensión de reposo y la próxima llamada suena en el FXO2. "
       "Antes de conectar se recorre el par y se anota todo lo que cuelga; para probar, una línea con un solo equipo.",
       [8, 36, 62, 92])
