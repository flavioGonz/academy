#!/usr/bin/env python3
"""Lección 17 (Hasta que suene) · Resumen, "Cómo se ve en la red": dos líneas, dos troncales, dos rutas entrantes. La
línea 1 va al IVR 7000 en horario y al grupo 6000 fuera de horario; la línea 2, la del fax, va directo a la extensión
del fax. Fuentes: la lección (laboratorio: Antel_Linea1, patrón _., Office Time → IVR 7000, fuera de horario → Ring
Group 6000; Antel_Linea2, patrón _., Extension del fax; toda llamada analógica arranca en s; en Active Calls el destino
nunca tiene que quedar en s)."""
from _anim_gs_red import R

g = R(T=26, fix=88, kicker="GRANDSTREAM · HASTA QUE SUENE · CÓMO SE VE EN LA RED",
      title="Dos líneas, dos rutas: cada una sabe a dónde va")
g.steps([
    "10:00, suena la línea 1: arranca en s y su ruta, en horario, la manda al IVR 7000.",
    "20:00, la misma línea: fuera de horario, la ruta la manda al Ring Group 6000.",
    "Suena la línea 2: su ruta, con patrón _., la manda directo a la extensión del fax.",
    "En Active Calls cada llamada tiene destino: IVR, grupo o fax, nunca s.",
])

R1, R2 = 196, 360
def fila(y, n):
    g.add(g.dev(48, y, 168, 76, f"Línea {n}", "Antel", icon="antel"))
    g.add(g.box(244, y + 16, 110, 44, g.WHITE, g.LINE, rx=10) + g.text(299, y + 45, f"FXO{n}", 17, g.INK, g.MONO, 600, "middle"))
    g.add(g.box(382, y + 16, 60, 44, g.SLATE, None, rx=10) + g.text(412, y + 45, "s", 20, g.INK, g.MONO, 600, "middle"))
    for x1, x2 in ((216, 244), (354, 382), (442, 470)):
        g.add(g.wire(x1, y + 38, x2, y + 38, g.LINE, 3))
fila(R1, 1)
fila(R2, 2)
CX, CW = 470, 330
g.add(g.box(CX, R1 - 10, CW, 132, g.WHITE, g.LINE, rx=14))
g.add(g.text(CX + 18, R1 + 18, "Inbound Route · Antel_Linea1", 15, g.INK, g.MONO, 600))
g.add(g.text(CX + 18, R1 + 46, "Pattern _.", 15, g.TXT, g.MONO))
g.add(g.text(CX + 18, R1 + 74, "Office Time → IVR 7000", 15, g.TXT, g.MONO))
g.add(g.text(CX + 18, R1 + 102, "fuera de horario → RG 6000", 15, g.TXT, g.MONO))
g.add(g.box(CX, R2 - 10, CW, 96, g.WHITE, g.LINE, rx=14))
g.add(g.text(CX + 18, R2 + 18, "Inbound Route · Antel_Linea2", 15, g.INK, g.MONO, 600))
g.add(g.text(CX + 18, R2 + 46, "Pattern _.", 15, g.TXT, g.MONO))
g.add(g.text(CX + 18, R2 + 74, "Default → Extensión del fax", 15, g.TXT, g.MONO))
g.appear(g.box(CX + 8, R1 + 54, CW - 16, 28, "none", g.OK, rx=6, sw=2.5), 4, 25)
g.appear(g.box(CX + 8, R1 + 82, CW - 16, 28, "none", g.OK, rx=6, sw=2.5), 29, 50)
g.appear(g.box(CX + 8, R2 + 54, CW - 16, 28, "none", g.OK, rx=6, sw=2.5), 54, 75)

DX, DW = 860, 292
dests = [("IVR 7000", "con horario", 186, "ucm"), ("Ring Group 6000", "1001 · 1002", 270, "tel"), ("Fax", "extensión del fax", 366, "fax")]
for n, s, y, ic in dests:
    g.add(g.dev(DX, y, DW, 70, n, s, icon=ic))
g.arrow([(CX + CW, R1 + 68), (DX, 221)], 8, 12, g.OK, hold=25)
g.arrow([(CX + CW, R1 + 96), (DX, 305)], 33, 37, g.OK, hold=50)
g.arrow([(CX + CW, R2 + 68), (DX, 401)], 58, 62, g.OK, hold=75)
g.appear(g.pillc(DX + DW - 56, 186 + 22, "atiende", g.OK, g.OKBG, 13, 24), 12, 25)
g.appear(g.pillc(DX + DW - 56, 270 + 22, "suena", g.OK, g.OKBG, 13, 24), 37, 50)
g.appear(g.pillc(DX + DW - 56, 366 + 22, "atiende", g.OK, g.OKBG, 13, 24), 62, 75)
g.appear(g.pillc(132, R1 - 30, "10:00", g.WHITE, g.BLUE, 13, 26), 2, 25)
g.appear(g.pillc(132, R1 - 30, "20:00", g.WHITE, g.INK, 13, 26), 27, 50)
g.token([(132, R1 + 38), (412, R1 + 38)], 2, 7, g.chip("llamada", bg=g.CYAN, size=13, h=24), hold=8)
g.token([(132, R1 + 38), (412, R1 + 38)], 27, 32, g.chip("llamada", bg=g.CYAN, size=13, h=24), hold=33)
g.token([(132, R2 + 38), (412, R2 + 38)], 52, 57, g.chip("llamada", bg=g.CYAN, size=13, h=24), hold=58)

AY = 476
g.add(g.box(48, AY, 1104, 128, g.WHITE, g.LINE, rx=14))
g.add(g.text(68, AY + 32, "System Status > Active Calls", 15, g.BLUE, g.MONO, 600))
g.appear(g.text(68, AY + 66, "DAHDI · Antel_Linea1 → 7000 (IVR)", 16, g.INK, g.MONO, 600), 8, 25)
g.appear(g.text(68, AY + 66, "DAHDI · Antel_Linea1 → 6000 (Ring Group)", 16, g.INK, g.MONO, 600), 33, 50)
g.appear(g.text(68, AY + 66, "DAHDI · Antel_Linea2 → fax", 16, g.INK, g.MONO, 600), 58, 75)
g.appear(g.text(68, AY + 66, "DAHDI · Antel_Linea1 → 7000 (IVR)", 16, g.OK, g.MONO, 600)
         + g.text(68, AY + 96, "DAHDI · Antel_Linea2 → fax", 16, g.OK, g.MONO, 600)
         + g.text(1132, AY + 66, "ninguna en s", 16, g.OK, g.SANS, 600, "end"), 77, 100)

g.status(640, [
    (0, 25, "Sin número llamado, la troncal por la que entró decide la ruta.", g.INK),
    (25, 50, "La misma ruta cambia de destino con la condición de horario.", g.INK),
    (50, 75, "La línea del fax no pasa por el IVR: su ruta va directo a la extensión.", g.OK),
    (75, 100, "Si alguna queda en s, a su troncal le falta ruta o el patrón no coincide.", g.AMB),
])

g.done(17, "r1", "Dos líneas, dos rutas: cada una sabe a dónde va",
       "Animación en cuatro tiempos con dos líneas de Antel, cada una con su FXO, la extensión s donde arranca la llamada y la ruta entrante de su troncal, y tres destinos: el IVR 7000 con horario, el Ring Group 6000 con la 1001 y la 1002, y la extensión del fax; abajo, Active Calls. "
       "1: a las 10:00 suena la línea 1; la llamada entra por el FXO1, arranca en s y la ruta de Antel_Linea1, con patrón _. y en Office Time, la manda al IVR 7000. "
       "2: a las 20:00, la misma línea: fuera de horario la ruta la manda al Ring Group 6000. "
       "3: suena la línea 2; su ruta, con patrón _., la manda directo a la extensión del fax. "
       "4: en Active Calls cada llamada tiene destino, IVR, grupo o fax, y ninguna queda en s; si alguna queda en s, a su troncal le falta ruta o el patrón no coincide.",
       [10, 36, 62, 90])
