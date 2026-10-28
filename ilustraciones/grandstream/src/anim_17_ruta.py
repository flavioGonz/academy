#!/usr/bin/env python3
"""Lección 17 · teoría: la llamada entra por el FXO, arranca en s y la ruta entrante de la troncal la lleva al destino."""
from _anim_grandstream import G

g = G(T=26, fix=72, kicker="GRANDSTREAM · RUTA ENTRANTE ANALÓGICA", title="De la línea al grupo: la ruta es por troncal")
g.steps([
    "Suena la línea 2 y la UCM atiende por el FXO2: la llamada es de la troncal Antel_Linea2.",
    "No llega número llamado: la llamada arranca en la extensión s.",
    "La ruta entrante de Antel_Linea2 (patrón _.) le da destino: el grupo 6000.",
    "Suenan las internas del grupo; en Active Calls el destino es 6000.",
    "Una línea cuya troncal no tiene ruta entrante se queda en s, sin destino.",
])
K = [0, 20, 40, 60, 80, 100]

Y = 236
g.add(g.node(48, Y, 170, 84, "Línea 2", "Antel", dark=True))
g.add(g.node(262, Y, 200, 84, "FXO2", "Antel_Linea2"))
g.add(g.node(506, Y, 120, 84, "s", "arranque"))
g.add(g.node(670, Y, 220, 84, "Ruta entrante", "_. → 6000"))
g.add(g.node(940, Y - 52, 212, 64, "1001", anchor="start"))
g.add(g.node(940, Y + 20, 212, 64, "1002", anchor="start"))
g.add(g.text(1046, Y + 116, "Grupo 6000 · internas", 17, g.OK, g.SANS, 600, "middle"))
for x1, x2 in ((218, 262), (462, 506), (626, 670)):
    g.add(f'<path d="M{x1} {Y + 42}H{x2}" stroke="{g.LINE}" stroke-width="4"/>')
g.add(f'<path d="M890 {Y + 42}L940 {Y - 20}M890 {Y + 42}L940 {Y + 52}" stroke="{g.LINE}" stroke-width="3"/>')
chip = g.chip("llamada", bg=g.CYAN, size=15, h=26)
g.token([(130, Y - 18), (362, Y - 18)], 3, 12, chip, hold=20)
g.token([(362, Y - 18), (566, Y - 18)], 22, 30, chip, hold=40)
g.token([(566, Y - 18), (780, Y - 18)], 42, 50, chip, hold=60)
g.appear(g.box(506, Y, 120, 84, "none", g.BLUE, rx=14, sw=3), 22, 42)
g.appear(g.box(670, Y, 220, 84, "none", g.OK, rx=14, sw=3), 42, 80)
g.arrow([(890, Y + 42), (938, Y - 18)], 61, 64, g.OK, hold=80)
g.arrow([(890, Y + 42), (938, Y + 50)], 61, 64, g.OK, hold=80)
g.appear(g.pillc(1100, Y - 40, "suena", g.OK, g.OKBG, size=15, h=28) + g.pillc(1100, Y + 32, "suena", g.OK, g.OKBG, size=15, h=28), 64, 80)

# Active Calls
AY = 402
g.add(g.box(48, AY, 640, 96, g.WHITE, g.LINE, rx=14))
g.add(g.text(68, AY + 32, "System Status > Active Calls", 16, g.BLUE, g.MONO, 600))
g.appear(g.text(68, AY + 70, "DAHDI · Antel_Linea2 → s", 18, g.INK, g.MONO, 600), 22, 42)
g.appear(g.text(68, AY + 70, "DAHDI · Antel_Linea2 → 6000", 18, g.OK, g.MONO, 600), 42, 80)
g.appear(g.text(68, AY + 70, "DAHDI · Antel_Linea3 → s", 18, g.BAD, g.MONO, 600), 80, 100)

# línea sin ruta
g.appear(g.node(730, AY, 422, 96, "Antel_Linea3 sin ruta", "se queda en s, sin destino") + g.mark(1124, AY + 22, False, 14), 80, 100)
g.appear(g.note(48, 530, 1104, None, ["Toda llamada analógica entra a la extensión s (Asterisk). El destino lo pone la ruta entrante de su troncal."], "info"), 0, 80)
g.appear(g.note(48, 530, 1104, None, ["Si una llamada queda en s, lo más probable es que su troncal no tenga ruta entrante o que el patrón no coincida."], "bad"), 80, 100)

g.finish(17, 1, "De la línea al grupo: la ruta es por troncal",
         "Animación en cinco tiempos con la línea 2 de Antel, el FXO2 de la troncal Antel_Linea2, la extensión s, la ruta entrante con patrón _. y destino 6000, y las internas 1001 y 1002 del grupo 6000. Abajo, una caja con lo que muestra Active Calls. "
         "1: suena la línea 2 y la UCM atiende por el FXO2. "
         "2: por la línea analógica no llega número llamado y la llamada arranca en la extensión s; Active Calls muestra Antel_Linea2 hacia s. "
         "3: la ruta entrante de Antel_Linea2 le da destino, el grupo 6000; Active Calls muestra 6000. "
         "4: suenan las internas 1001 y 1002 del grupo. "
         "5: una línea cuya troncal, Antel_Linea3, no tiene ruta entrante se queda en s, sin destino. "
         "Nota: toda llamada analógica entra a la extensión s, como dice la documentación de Asterisk; si queda ahí, lo más probable es que falte la ruta o que el patrón no coincida.",
         [10, 30, 50, 72, 92])
