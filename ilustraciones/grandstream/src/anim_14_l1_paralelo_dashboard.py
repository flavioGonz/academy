#!/usr/bin/env python3
"""Lección 14 (Troncal analógica) · Laboratorio, paso 5: descolgar el teléfono de prueba en paralelo con la línea 1 y
mirar el Dashboard. El teléfono cierra el lazo; la línea queda tomada para Antel; un FXO en uso sin ninguna llamada en
Active Calls es la pista de algo en paralelo, la referencia para Diagnóstico de línea. Fuentes: la lección (concepto
Estados del FXO: un FXO naranja sin llamadas en Active Calls es una pista de que algo tiene tomada la línea; anotar lo
que muestra como referencia) y Qué trae el par (al descolgar se cierra el lazo y cae la tensión)."""
from _anim_gs_red import R

g = R(T=24, fix=62, kicker="GRANDSTREAM · TRONCAL ANALÓGICA · LABORATORIO",
      title="Un teléfono descolgado en paralelo: qué ve la central")
g.steps([
    "Todo colgado: el FXO1 se ve libre y Active Calls no tiene llamadas.",
    "Descolgás el teléfono de prueba en paralelo con la línea 1: cierra el lazo.",
    "El FXO1 en uso y Active Calls vacío: la marca de algo tomando la línea.",
    "Colgás y vuelve a libre. Lo que viste es tu referencia para el diagnóstico.",
])

PAR = "#3B4D61"
def par(x1, y1, x2, y2):
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{PAR}" stroke-width="8" stroke-linecap="round"/>'
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#F7FAFD" stroke-width="2" stroke-linecap="round"/>')

PY = 330
g.add(g.dev(48, PY - 44, 220, 88, "Línea 1", "Antel", icon="antel", dark=True))
g.add(par(268, PY, 700, PY))
TX = 470
g.add(par(TX, PY, TX, 266))
g.add(g.dev(TX - 130, 190, 260, 76, "Teléfono de prueba", "en paralelo", icon="tel"))
g.appear(g.pillc(TX + 220, 215, "colgado", g.GREY, g.SLATE, 13, 26), 0, 25)
g.appear(g.pillc(TX + 220, 215, "descolgado", g.AMB, g.AMBBG, 13, 26), 25, 75)
g.appear(g.pillc(TX + 220, 215, "colgado", g.GREY, g.SLATE, 13, 26), 75, 100)
g.appear(g.box(268, PY - 5, TX - 268, 10, R.USO, None, rx=5) + g.box(TX - 5, 266, 10, PY - 266, R.USO, None, rx=5), 27, 75)
g.add(g.dev(700, PY - 44, 160, 88, "UCM", "FXO1", icon="ucm", dark=True))
g.appear(g.text(560, PY + 30, "tensión de reposo", 15, g.OK, g.MONO, 600, "middle"), 0, 25)
g.appear(g.text(560, PY + 30, "cae: lazo cerrado", 15, g.AMB, g.MONO, 600, "middle"), 27, 75)
g.appear(g.text(560, PY + 30, "tensión de reposo", 15, g.OK, g.MONO, 600, "middle"), 77, 100)

# Dashboard
DX, DY, DW = 900, 186, 252
g.add(g.box(DX, DY, DW, 236, g.WHITE, g.LINE, rx=14))
g.add(g.text(DX + 18, DY + 30, "Dashboard", 15, g.GREY, g.MONO))
g.add(g.text(DX + 18, DY + 56, "Interface Status", 14, g.GREY, g.MONO))
g.appear(g.port(DX + 16, DY + 70, "FXO1", "libre", w=DW - 32), 0, 40)
g.appear(g.port(DX + 16, DY + 70, "FXO1", "uso", w=DW - 32), 40, 76)
g.appear(g.port(DX + 16, DY + 70, "FXO1", "libre", w=DW - 32), 76, 100)
g.add(g.text(DX + 18, DY + 150, "Active Calls", 14, g.GREY, g.MONO))
g.add(g.text(DX + 18, DY + 180, "(sin llamadas)", 17, g.INK, g.MONO, 600))
g.appear(g.box(DX + 8, DY + 132, DW - 16, 64, "none", g.AMB, rx=10, sw=2.5), 52, 75)
g.appear(g.box(DX + 8, DY + 62, DW - 16, 60, "none", g.AMB, rx=10, sw=2.5), 52, 75)

g.appear(g.note(48, 462, 1104, None, ["Para la central de Antel, la línea 1 ya está ocupada: quien llame recibe ocupado aunque nadie esté hablando por la UCM."], "amb"), 25, 75)
g.appear(g.note(48, 462, 1104, None, ["Descolgá solo el teléfono de prueba, nada más: así sabés que lo que ves lo provoca un equipo en paralelo."], "info"), 0, 25)
g.appear(g.note(48, 462, 1104, None, ["Anotá cómo lo muestra tu central y en cuánto vuelve a libre: es la referencia de la lección Diagnóstico de línea."], "ok"), 75, 100)
g.add(g.term(48, 540, 1104, 62, None, [("Línea 1 · descolgado en paralelo: FXO1 ______   Active Calls ______   vuelve a libre: ___ s", g.MINT)], size=16))

g.status(640, [
    (0, 25, "La referencia se toma con la línea quieta.", g.INK),
    (25, 50, "El teléfono hace lo mismo que haría la UCM al atender: cierra el lazo.", g.AMB),
    (50, 75, "Puerto en uso sin llamada en la central: alguien más tiene la línea.", g.AMB),
    (75, 100, "Con eso, un FXO naranja sin llamadas deja de ser un misterio.", g.OK),
])

g.done(14, "l1", "Un teléfono descolgado en paralelo: qué ve la central",
       "Animación en cuatro tiempos con la línea 1 de Antel, un teléfono de prueba conectado en paralelo sobre el mismo par y el FXO1 de la UCM; a la derecha, el Dashboard con Interface Status y Active Calls, y abajo un renglón de la ficha para anotar. "
       "1: con todo colgado hay tensión de reposo, el FXO1 se ve libre y Active Calls no tiene llamadas. "
       "2: se descuelga el teléfono de prueba en paralelo; cierra el lazo, la tensión cae y para la central de Antel la línea 1 queda ocupada. "
       "3: el Dashboard muestra el FXO1 en uso mientras Active Calls sigue sin llamadas: esa combinación es la marca de algo en paralelo tomando la línea. "
       "4: al colgar vuelve la tensión de reposo y el FXO1 vuelve a libre. "
       "Se anota cómo lo muestra la central y en cuánto vuelve a libre: es la referencia para la lección Diagnóstico de línea.",
       [8, 36, 62, 90])
