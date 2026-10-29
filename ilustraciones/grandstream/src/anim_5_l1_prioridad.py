#!/usr/bin/env python3
"""Lección 5 · Laboratorio, paso 5: botón Outgoing Routing Priority. Cuando un número coincide con dos rutas,
List Sorting Priority usa la primera de la lista y Accuracy First el patrón más parecido. Con una ruta amplia (_X.)
arriba de la internacional, el internacional sale sin PIN. Fuente: manual UCM630x (Outgoing Routing Priority:
List Sorting Priority y Accuracy First)."""
from _anim_gs_red import R

g = R(T=26, fix=40, kicker="GRANDSTREAM · PATRÓN Y PRIVILEGIO · LABORATORIO",
      title="Dos rutas coinciden: cuál gana")
g.steps([
    "La 1001 marca 005411…: coincide con la ruta general (_X.) y con la internacional (_00X.).",
    "List Sorting Priority: gana la primera de la lista, la general, y sale sin pedir PIN.",
    "Accuracy First: gana el patrón más parecido, _00X.: privilegio International y PIN.",
    "Por eso se mira el botón y se prueba: un internacional tiene que pedir PIN.",
])

g.add(g.text(48, 206, "marcado por la 1001", 15, g.GREY, g.MONO))
g.add(g.box(48, 218, 330, 56, g.INK, rx=12) + g.text(68, 254, "005411…", 24, g.GOLD, g.MONO, 600))

TX, TY, TW = 48, 302, 700
g.add(g.box(TX, TY, TW, 186, g.WHITE, g.LINE, rx=14))
g.add(g.text(TX + 20, TY + 32, "Outbound Routes (en este orden)", 16, g.INK, g.SANS, 600))
hdr = [("#", 20), ("nombre", 56), ("patrón", 230), ("privilegio", 340), ("PIN", 500)]
for t, dx in hdr:
    g.add(g.text(TX + dx, TY + 64, t, 14, g.GREY, g.MONO))
R1, R2 = TY + 82, TY + 130
for y, vals in ((R1, ("1", "general", "_X.", "National", "no")), (R2, ("2", "internacional", "_00X.", "International", "sí"))):
    g.add(g.box(TX + 10, y, TW - 20, 40, g.SLATE, None, rx=8))
    for (t, dx), v in zip(hdr, vals):
        g.add(g.text(TX + dx, y + 26, v, 16, g.INK, g.MONO, 600))
# coincidencias
g.appear(g.pillc(TX + TW - 60, R1 + 7, "coincide", g.BLUE, "#E6F0FA", 13, 26), 8, 25)
g.appear(g.pillc(TX + TW - 60, R2 + 7, "coincide", g.BLUE, "#E6F0FA", 13, 26), 12, 25)
g.appear(g.box(TX + 10, R1, TW - 20, 40, "none", g.BAD, rx=8, sw=3) + g.pillc(TX + TW - 60, R1 + 7, "gana", g.WHITE, g.BAD, 13, 26), 27, 50)
g.appear(g.box(TX + 10, R2, TW - 20, 40, "none", g.OK, rx=8, sw=3) + g.pillc(TX + TW - 60, R2 + 7, "gana", g.WHITE, g.OK, 13, 26), 52, 100)

# ajuste
SX, SW = 780, 372
g.add(g.box(SX, 186, SW, 134, g.WHITE, g.LINE, rx=14))
g.add(g.text(SX + 20, 216, "Outgoing Routing Priority", 15, g.GREY, g.MONO))
g.appear(g.text(SX + 20, 252, "(dos políticas posibles)", 17, g.GREY, g.SANS), 0, 25)
g.appear(g.text(SX + 20, 252, "List Sorting Priority", 19, g.BAD, g.MONO, 600)
         + g.text(SX + 20, 284, "la primera que coincida", 15, g.TXT), 25, 50)
g.appear(g.text(SX + 20, 252, "Accuracy First", 19, g.OK, g.MONO, 600)
         + g.text(SX + 20, 284, "el patrón más parecido", 15, g.TXT), 50, 100)

# resultado
g.appear(g.note(SX, 340, SW, "Resultado", ["Las dos rutas sirven para este número:", "decide la política."], "info"), 0, 25)
g.appear(g.note(SX, 340, SW, "Sale sin PIN", ["La ruta general no pide PIN ni", "International: el internacional", "sale como uno nacional."], "bad"), 25, 50)
g.appear(g.note(SX, 340, SW, "Pide PIN", ["Va por la internacional: privilegio", "International y PIN Group, como", "se diseñó."], "ok"), 50, 75)
g.appear(g.note(SX, 340, SW, "Prueba", ["Marcá un internacional de prueba", "desde una interna con PIN Group:", "tiene que pedir el PIN."], "ok"), 75, 100)

g.add(g.note(48, 512, 1104, None, ["La ruta general es un ejemplo de un patrón amplio. Con List Sorting, una ruta así arriba de la lista le gana a todas las de abajo."], "amb"))

g.status(628, [
    (0, 25, "Un número puede coincidir con más de un patrón.", g.INK),
    (25, 50, "El orden de la lista manda: el patrón amplio de arriba se lleva la llamada.", g.BAD),
    (50, 75, "La precisión manda: _00X. dice más que _X. para un número que empieza con 00.", g.OK),
    (75, 100, "Botón Outgoing Routing Priority, en la página de Outbound Routes.", g.INK),
])

g.done(5, "l1", "Dos rutas coinciden: cuál gana",
       "Animación en cuatro tiempos con el número 005411… marcado por la interna 1001, la tabla de Outbound Routes en orden (1, general, patrón _X., privilegio National, sin PIN; 2, internacional, patrón _00X., privilegio International, con PIN) y el ajuste Outgoing Routing Priority. "
       "1: el número coincide con las dos rutas. "
       "2: con List Sorting Priority gana la primera de la lista, la general, y el internacional sale sin PIN ni privilegio International. "
       "3: con Accuracy First gana el patrón más parecido, _00X., y la llamada va por la internacional, con privilegio International y PIN Group. "
       "4: por eso se revisa el botón Outgoing Routing Priority en la página de Outbound Routes y se prueba que un internacional pida el PIN. "
       "Nota: la ruta general es un ejemplo de patrón amplio; con List Sorting, una ruta así arriba de la lista les gana a todas las de abajo.",
       [10, 40, 62, 90])
