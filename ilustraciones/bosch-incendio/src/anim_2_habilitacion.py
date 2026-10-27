"""Teoría de Quién manda: el recorrido de una habilitación según el Decreto 372/023."""
from _anim_bi import *

caps = ["El técnico registrado firma el proyecto e ingresa el trámite.",
        "La empresa registrada instala y pone en marcha según el proyecto.",
        "Una diferencia en obra vuelve al técnico registrado, por escrito.",
        "Habilitado: el propietario mantiene con una empresa registrada."]
a = new(24, "Normativa", "Cada decisión vuelve a quien firma", caps, still=3)

a.add(card(a, 60, 190, 300, 90, "Técnico registrado", "firma el proyecto", dark=True))
a.add(card(a, 840, 190, 300, 90, "Bomberos (DNB)", "trámite y verificación"))
a.add(card(a, 450, 330, 300, 100, "Obra", "sistema de detección"))
a.add(card(a, 60, 480, 300, 90, "Empresa registrada", "instala y mantiene"))
a.add(card(a, 840, 480, 300, 90, "Propietario", "responde por mantener"))
# flechas fijas numeradas
a.add(line(a, 362, 225, 836, 225, a.BLUE)); a.add(a.pill(600, 194, "1 proyecto + declaración jurada", a.BLUE, a.WHITE, anchor="middle"))
a.add(line(a, 300, 478, 470, 432, a.OK)); a.add(a.pill(250, 440, "2 instala", a.OK, a.WHITE, anchor="middle"))
a.add(line(a, 470, 330, 330, 284, a.AMB, dash="7 6")); a.add(a.pill(372, 300, "3 consulta", a.AMB, a.WHITE, anchor="middle"))
a.add(line(a, 838, 520, 362, 520, a.GREY, dash="7 6")); a.add(a.pill(600, 532, "4 contrata mantenimiento", a.GREY, a.WHITE, anchor="middle"))
# fichas
s0, s1 = ph(a, 0)
token(a, "proyecto firmado", [(s0 + 2, 300, 250), (s0 + 18, 900, 250), (s1 - 1, 900, 250)], bg=a.BLUE)
s0, s1 = ph(a, 1)
token(a, "instalación", [(s0 + 2, 300, 500), (s0 + 16, 560, 420), (s1 - 1, 560, 420)], bg=a.OK)
s0, s1 = ph(a, 2)
token(a, "diferencia", [(s0 + 1, 560, 350), (s0 + 10, 250, 300), (s0 + 14, 250, 300)], bg=a.AMB)
token(a, "decide por escrito", [(s0 + 15, 250, 300), (s0 + 23, 600, 360), (s1 - 1, 600, 360)], bg=a.INK)
s0, s1 = ph(a, 3)
vis(a, a.pill(600, 446, "habilitado", a.OK, a.OKBG, anchor="middle"), 3)
token(a, "mantenimiento", [(s0 + 2, 900, 466), (s0 + 14, 440, 466), (s1 - 1, 440, 466)], bg=a.GREY)
a.add(a.text(48, 630, "El manual de Bosch también lo dice: mandan las reglas de la autoridad local.", 17, a.TXT))
write(a, "2-t1.svg", "Cada decisión vuelve a quien firma", [12, 37, 62, 90])
