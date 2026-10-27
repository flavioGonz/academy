"""Teoría lección 2: el bus alimenta y comunica; la central supervisa cada módulo."""
from _apdx import *

a = new(20, "El bus: energía para todos, diálogo con cada uno")
a.steps(["Rojo y negro: la alimentación del auxiliar llega a cada módulo.",
         "Los dos hilos de datos: la central habla con cada módulo.",
         "Sumás un módulo sin energía: al energizar, la central lo ve.",
         "Un módulo deja de responder: TBL grupo 10, supervisión de módulo."], still=1)
a.add(card(a, 48, 250, 210, 170, "Central", "SP+ o MG", dark=True))
cols = [("#D2492F", 0), ("#2B2B2B", 1), (a.BLUE, 2), (a.CYAN, 3)]
Y0 = 300
for col, i in cols:
    a.add(line(a, f"M258 {Y0 + i * 18}H1110", col, 4))
mods = [(340, "Teclado", "K32LCD+"), (570, "Expansor", "ZX8"), (800, "Teclado", "K35")]
for x, t, s in mods:
    for col, i in cols:
        a.add(line(a, f"M{x + 40 + i * 14} {Y0 + i * 18}V430", col, 3))
        a.add(dot(a, x + 40 + i * 14, Y0 + i * 18, 4, col))
    a.add(card(a, x - 20, 430, 200, 90, t, s))
# módulo nuevo
for col, i in cols:
        at(a, line(a, f"M{1040 + i * 14} {Y0 + i * 18}V430", col, 3), 50, 100, 0)
at(a, card(a, 1010, 430, 142, 90, "Nuevo", "ZX8"), 50, 100, 0)
# energía: brillo
at(a, line(a, f"M258 {Y0}H1110", "#FF8A73", 9) + line(a, f"M258 {Y0 + 18}H1110", "#7A7A7A", 9), 0, 25, 0)
at(a, a.text(560, 270, "+ y − del auxiliar", 16, "#D2492F", a.MONO, 700, "middle"), 0, 25, 0)
# datos: paquete que va y vuelve
for k, (x, _, _) in enumerate(mods):
    t0 = 25 + k * 8
    mv = a.move([(0, 270, Y0 + 36), (t0, 270, Y0 + 36), (t0 + 3, x + 68, Y0 + 36), (t0 + 5, x + 68, Y0 + 54), (t0 + 8, 270, Y0 + 54), (100, 270, Y0 + 54)])
    op = a.keyframes([(0, 0), (t0, 0), (t0 + 0.5, 1), (t0 + 7.5, 1), (t0 + 8, 0), (100, 0)])
    a.add(a.group('<circle cx="0" cy="0" r="9" fill="#FFB020" stroke="#fff" stroke-width="2"/>', mv, op, still=0))
at(a, a.text(560, 270, "datos: pregunta y respuesta", 16, a.BLUE, a.MONO, 700, "middle"), 25, 50, 1)
at(a, chip(a, 1081, 536, "reconocido", "ok", anchor="middle"), 56, 75, 0)
# falla
at(a, a.box(550, 430, 200, 90, a.BADBG, a.BAD, rx=14, sw=3) + a.text(570, 464, "Expansor", 19, a.BAD, a.HEAD, 600)
   + a.text(570, 490, "no responde", 15, a.BAD, a.MONO, 600), 75, 100, 0)
at(a, a.box(70, 380, 166, 30, a.BAD, None, rx=15) + a.text(153, 401, "TBL 10", 16, "#fff", a.MONO, 700, "middle"), 77, 100, 0)
caption(a, 600, [(0, 25, "Cada módulo suma consumo: por eso el bus entra en la cuenta del AUX.", None),
                 (25, 50, "La central habla con cada módulo por los hilos de datos y sabe quién está.", None),
                 (50, 75, "Por eso se suma de a uno: si aparece una falla, es del último que conectaste.", a.OK),
                 (75, 100, "Si sacás un módulo a propósito, la falla queda hasta borrarla en [955].", a.BAD)], still=1)
write(a, "2-t1.svg", "El bus: energía para todos, diálogo con cada uno",
      "Animación en cuatro tiempos de una central con cuatro hilos de bus y tres módulos colgados. 1: los hilos rojo y negro llevan la alimentación del auxiliar a todos. "
      "2: por los dos hilos de datos un mensaje va de la central a cada módulo y vuelve. 3: se suma un cuarto módulo y la central lo reconoce. "
      "4: el expansor deja de responder, se marca en rojo y la central muestra TBL grupo 10, supervisión de módulo, que se borra en la sección 955 si el módulo sale para siempre.")
