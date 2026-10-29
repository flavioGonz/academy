#!/usr/bin/env python3
"""Lección 14 (Troncal analógica) · Resumen, "Cómo se ve en la red": cada línea entra a un FXO, cada FXO es una
troncal con nombre, y el Dashboard lo muestra en colores mientras pasan las llamadas. Fuentes: la lección (troncal
por línea; las rutas trabajan con el nombre de la troncal; Dashboard: gris sin configurar o sin línea, azul libre en
el firmware actual, naranja en uso; Trunks: Available, Busy, Abnormal, Unmonitored; las llamadas analógicas
aparecen en Active Calls como canales DAHDI)."""
from _anim_gs_red import R

g = R(T=26, fix=62, kicker="GRANDSTREAM · TRONCAL ANALÓGICA · CÓMO SE VE EN LA RED",
      title="Del par a la ruta: cómo ve la UCM cada línea")
g.steps([
    "Con las troncales creadas, el FXO1 y el FXO2 se ven libres y las troncales, Available.",
    "Suena la línea 1: el FXO1 atiende y pasa a naranja; Antel_Linea1 queda Busy.",
    "La 1002 llama afuera: la ruta saliente usa Antel_Linea2 y el FXO2 toma la línea.",
    "Terminada esa llamada, se desconecta el cable del FXO2: pasa a gris, sin línea.",
])

PAR = "#3B4D61"
def par(x1, y1, x2, y2, dash=None):
    da = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{PAR}" stroke-width="8" stroke-linecap="round"{da}/>'
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#F7FAFD" stroke-width="2" stroke-linecap="round"{da}/>')

L1, L2 = 196, 300
for y, n in ((L1, "1"), (L2, "2")):
    g.add(g.dev(48, y, 190, 72, f"Línea {n}", "Antel", icon="antel"))
g.add(par(238, L1 + 36, 300, L1 + 36))
g.appear(par(238, L2 + 36, 300, L2 + 36), 0, 76)
g.appear(par(238, L2 + 36, 262, L2 + 36), 76, 100)
PX, PW = 300, 200
def port(y, label, state, t0, t1):
    g.appear(g.port(PX, y + 14, label, state, w=PW), t0, t1)
port(L1, "FXO1", "libre", 0, 27); port(L1, "FXO1", "uso", 27, 100)
port(L2, "FXO2", "libre", 0, 52); port(L2, "FXO2", "uso", 52, 76); port(L2, "FXO2", "gris", 76, 100)
TX, TW = 556, 300
for y, n in ((L1, "Antel_Linea1"), (L2, "Antel_Linea2")):
    g.add(g.box(TX, y, TW, 72, g.INK, rx=14) + g.text(TX + 18, y + 30, n, 18, g.WHITE, g.MONO, 600)
          + g.text(TX + 18, y + 56, "troncal analógica", 14, g.SKY, g.MONO))
    g.add(g.wire(PX + PW, y + 36, TX, y + 36, g.LINE, 3))
def tstate(y, label, fg, bg, t0, t1):
    g.appear(g.pill(TX + TW - 12, y + 10, label, fg, bg, 12, 22, "end"), t0, t1)
tstate(L1, "Available", g.BLUE, "#E6F0FA", 0, 27); tstate(L1, "Busy", g.WHITE, R.USO, 27, 100)
tstate(L2, "Available", g.BLUE, "#E6F0FA", 0, 52); tstate(L2, "Busy", g.WHITE, R.USO, 52, 76)

RX, RW = 890, 262
g.appear(g.dev(RX, L1, RW, 72, "Ruta entrante", "de Antel_Linea1"), 27, 100)
g.appear(g.dev(RX, L2, RW, 72, "Ruta saliente", "de la 1002"), 52, 76)
g.appear(g.wire(TX + TW, L1 + 36, RX, L1 + 36, g.OK, 4), 27, 100)
g.appear(g.wire(TX + TW, L2 + 36, RX, L2 + 36, g.OK, 4), 52, 76)
g.token([(120, L1 - 16), (690, L1 - 16)], 28, 38, g.chip("timbre → atiende", bg=g.CYAN, size=13, h=24), hold=40)
g.token([(1011, L2 + 88), (400, L2 + 88)], 53, 62, g.chip("1002 marca afuera", bg=g.BLUE, size=13, h=24), hold=64)
g.appear(g.mark(250, L2 + 36, False, 13) + g.text(160, L2 + 98, "cable desconectado", 15, g.BAD, g.MONO, 600, "middle"), 78, 100)

# Active Calls
AY = 420
g.add(g.box(48, AY, 772, 118, g.WHITE, g.LINE, rx=14))
g.add(g.text(68, AY + 30, "System Status > Active Calls", 15, g.BLUE, g.MONO, 600))
g.appear(g.text(68, AY + 66, "(sin llamadas)", 16, g.GREY, g.SANS), 0, 27)
g.appear(g.text(68, AY + 66, "DAHDI · Antel_Linea1 → entrante", 16, g.INK, g.MONO, 600), 27, 100)
g.appear(g.text(68, AY + 96, "1002 → DAHDI · Antel_Linea2", 16, g.INK, g.MONO, 600), 52, 76)
# leyenda de colores
g.add(g.box(844, AY, 308, 118, g.WHITE, g.LINE, rx=14))
g.add(g.text(864, AY + 30, "colores del Dashboard", 15, g.GREY, g.MONO))
for k, (c, t) in enumerate(((R.LIBRE, "libre"), (R.USO, "en uso"), (R.GRISP, "sin línea o sin configurar"))):
    y = AY + 56 + k * 24
    g.add(f'<circle cx="872" cy="{y - 5}" r="7" fill="{c}"/>' + g.text(888, y, t, 15, g.INK, g.SANS))

g.status(600, [
    (0, 25, "Las rutas hablan de troncales, no de puertos: por eso los nombres claros.", g.INK),
    (25, 50, "La llamada analógica aparece como canal DAHDI de su troncal.", g.INK),
    (50, 75, "Cada FXO en uso es una línea ocupada para Antel.", g.AMB),
    (75, 100, "Mirá el Dashboard antes y después de cada cambio: te dice qué ve la central.", g.INK),
])

g.done(14, "r1", "Del par a la ruta: cómo ve la UCM cada línea",
       "Animación en cuatro tiempos con las líneas 1 y 2 de Antel, los puertos FXO1 y FXO2 con los colores del Dashboard, las troncales analógicas Antel_Linea1 y Antel_Linea2 con su estado, las rutas que las usan y, abajo, Active Calls y la leyenda de colores: azul libre, naranja en uso, gris sin línea o sin configurar. "
       "1: con las troncales creadas, el FXO1 y el FXO2 se ven libres y las dos troncales, Available. "
       "2: suena la línea 1, el FXO1 atiende y pasa a naranja; Antel_Linea1 queda Busy, la llamada va a la ruta entrante de esa troncal y Active Calls la muestra como canal DAHDI de Antel_Linea1. "
       "3: la 1002 llama afuera, la ruta saliente usa Antel_Linea2, el FXO2 toma la línea y pasa a naranja. "
       "4: terminada esa llamada, se desconecta el cable del FXO2 y el puerto pasa a gris, sin línea. "
       "Las rutas trabajan con el nombre de la troncal; conviene mirar el Dashboard antes y después de cada cambio.",
       [8, 36, 62, 90])
