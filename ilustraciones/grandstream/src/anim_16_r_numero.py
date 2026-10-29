#!/usr/bin/env python3
"""Lección 16 (Identificador y audio) · Resumen, "Cómo se ve en la red": por qué no aparece el número en una entrante
analógica. Sin el servicio de Antel no viaja nada; con el servicio y otro esquema, la UCM recibe algo que no
decodifica; con el esquema correcto, el número aparece en el CDR y en el teléfono. Fuentes: la lección (Identificación
de número llamante se contrata aparte; Antel no publica el esquema; "Failed to decode CallerID" en Asterisk; orden:
teléfono con pantalla, Auto-Detect, esquemas de a uno; CDR > CDR)."""
from _anim_gs_red import R

g = R(T=26, fix=88, kicker="GRANDSTREAM · IDENTIFICADOR Y AUDIO · CÓMO SE VE EN LA RED",
      title="El número que no aparece: tres causas, un orden")
g.steps([
    "Sin el servicio de Antel no viaja ningún número: ni el teléfono con pantalla lo muestra.",
    "Con el servicio, pero otro esquema en la troncal: llega algo que la UCM no decodifica.",
    "Auto-Detect y, si no alcanza, un esquema por vez, mirando el CDR en cada prueba.",
    "Con el esquema de la línea, el número aparece en el CDR y en el teléfono que atiende.",
])

# línea de tiempo de la entrante
TX, TY, TW = 48, 196, 1104
g.add(g.box(TX, TY - 10, TW, 150, "#03213C", None, rx=14))
g.add(g.text(TX + 20, TY + 20, "lo que llega por el FXO1 en una entrante", 14, g.SKY, g.MONO))
BASE = TY + 84
def burst(x, w=150):
    return "".join(f'<line x1="{x + i * 6}" y1="{BASE - 34}" x2="{x + i * 6 + 3}" y2="{BASE + 34}" stroke="{g.GOLD}" stroke-width="2"/>' for i in range(int(w / 6)))
g.add(burst(TX + 40) + g.text(TX + 115, BASE + 52, "timbre", 14, g.GOLD, g.MONO, 600, "middle"))
g.add(burst(TX + 700) + g.text(TX + 775, BASE + 52, "timbre", 14, g.GOLD, g.MONO, 600, "middle"))
g.add(f'<line x1="{TX + 200}" y1="{BASE}" x2="{TX + 690}" y2="{BASE}" stroke="#2A4B6A" stroke-width="2" stroke-dasharray="4 6"/>')
g.appear(g.text(TX + 445, BASE + 6, "nada: la línea no tiene el servicio", 16, "#FF9C86", g.MONO, 600, "middle"), 0, 25)
g.appear(g.box(TX + 250, BASE - 22, 390, 44, g.CYAN, None, rx=8) + g.text(TX + 445, BASE + 6, "datos del número", 16, "#03213C", g.MONO, 600, "middle"), 25, 100)
g.add(g.text(TX + TW - 20, TY + 20, "el momento y la forma los pone el esquema", 13, g.SKY, g.MONO, 400, "end"))

# UCM y teléfono
Y2 = 372
g.add(g.box(48, Y2, 520, 170, g.WHITE, g.LINE, rx=14))
g.add(g.text(68, Y2 + 32, "Antel_Linea1 · Caller ID Scheme", 15, g.GREY, g.MONO))
g.appear(g.text(68, Y2 + 70, "Bellcore/Telcordia (de fábrica)", 18, g.INK, g.MONO, 600), 0, 50)
g.appear(g.text(68, Y2 + 70, "Auto-Detect → uno por vez", 18, g.BLUE, g.MONO, 600), 50, 75)
g.appear(g.text(68, Y2 + 70, "el esquema de esta línea", 18, g.OK, g.MONO, 600), 75, 100)
g.add(g.text(68, Y2 + 112, "CDR > CDR · número", 15, g.GREY, g.MONO))
g.appear(g.text(68, Y2 + 144, "(vacío)", 18, g.BAD, g.MONO, 600), 0, 25)
g.appear(g.text(68, Y2 + 144, "no se decodifica", 18, g.BAD, g.MONO, 600) + g.text(300, Y2 + 144, "Failed to decode CallerID", 14, g.GREY, g.MONO), 25, 50)
g.appear(g.text(68, Y2 + 144, "prueba 1, prueba 2…", 18, g.AMB, g.MONO, 600), 50, 75)
g.appear(g.text(68, Y2 + 144, "2900 1007", 20, g.OK, g.MONO, 600), 75, 100)

g.add(g.box(592, Y2, 280, 170, "#03213C", None, rx=14))
g.add(g.text(612, Y2 + 32, "teléfono con pantalla", 14, g.SKY, g.MONO))
g.appear(g.text(612, Y2 + 90, "sin número", 20, "#FF9C86", g.MONO, 600), 0, 25)
g.appear(g.text(612, Y2 + 90, "2900 1007", 22, g.MINT, g.MONO, 600) + g.text(612, Y2 + 124, "el servicio está", 15, g.SKY, g.SANS), 25, 100)

g.add(g.box(896, Y2, 256, 170, g.WHITE, g.LINE, rx=14))
g.add(g.text(916, Y2 + 32, "qué hacer", 15, g.GREY, g.MONO))
g.appear(g.text(916, Y2 + 72, "pedir el servicio", 17, g.INK, g.SANS, 600) + g.text(916, Y2 + 98, "a Antel", 17, g.INK, g.SANS, 600), 0, 25)
g.appear(g.text(916, Y2 + 72, "cambiar el esquema", 17, g.INK, g.SANS, 600) + g.text(916, Y2 + 98, "de la troncal", 17, g.INK, g.SANS, 600), 25, 75)
g.appear(g.text(916, Y2 + 72, "dejarlo fijo y", 17, g.OK, g.SANS, 600) + g.text(916, Y2 + 98, "anotarlo en la ficha", 17, g.OK, g.SANS, 600), 75, 100)

g.add(g.note(48, 564, 1104, None, ["El número es un ejemplo. Antel no publica qué esquema usa: el que funciona en una línea se anota en su ficha."], "info"))

g.done(16, "r1", "El número que no aparece: tres causas, un orden",
       "Animación en cuatro tiempos con lo que llega por el FXO1 en una entrante, dos timbres y lo que viaja entre ellos, y abajo el Caller ID Scheme de la troncal Antel_Linea1 con el número del CDR, un teléfono con pantalla conectado al par y qué hacer. "
       "1: sin el servicio de identificación de Antel entre los timbres no viaja nada; el CDR queda vacío y el teléfono con pantalla tampoco muestra número: se pide el servicio a Antel. "
       "2: con el servicio llegan los datos del número y el teléfono con pantalla muestra 2900 1007, pero con otro esquema en la troncal la UCM no los decodifica, como el Failed to decode CallerID de Asterisk. "
       "3: se prueba Auto-Detect y, si no alcanza, un esquema por vez, mirando el CDR en cada prueba. "
       "4: con el esquema de la línea el número 2900 1007 aparece en el CDR y en el teléfono que atiende; se deja fijo y se anota en la ficha. "
       "El número es un ejemplo y Antel no publica qué esquema usa.",
       [10, 36, 62, 90])
