#!/usr/bin/env python3
"""Lección 1 · Resumen, "Cómo se ve en la red": Cloud Access no es controlador en la nube.
Hotel con OC300 en el rack y Cloud Access: se corta la fibra y en el lugar se sigue gestionando.
Con Omada Central el controlador vive en la nube: sin internet, nadie gestiona."""
from _anim_om_red import *

a = nueva(26, "DÓNDE VIVE", "Cloud Access o controlador en la nube: cortá la fibra")
F = a.steps([
    "OC300 en el rack y Cloud Access: la nube es solo la puerta para entrar de afuera.",
    "Se corta la fibra: de afuera no entrás, pero en el lugar el OC300 sigue mandando.",
    "Omada Central: el controlador corre en la nube y los equipos le hablan por internet.",
    "Se corta la fibra: la red sigue con lo último, pero nadie gestiona hasta que vuelva.",
], still=1)
A, B = 0, 50   # dos escenarios

# oficina de IES
a.add(dev(a, 48, 250, 220, 90, "Técnico IES", "en la oficina", icon="laptop"))
# nube
a.add(a.box(316, 236, 268, 118, "#EAF2FA", a.LINE, rx=40, sw=2, extra='stroke-dasharray="7 6"'))
at(a, a.text(450, 284, "Nube TP-Link", 19, a.INK, a.SANS, 600, "middle")
   + a.text(450, 312, "Cloud Access:", 15, a.GREY, a.MONO, 400, "middle")
   + a.text(450, 334, "solo la puerta", 15, a.GREY, a.MONO, 400, "middle"), 0, 50, still=1)
at(a, a.box(316, 236, 268, 118, a.INK, rx=40)
   + a.text(450, 284, "Omada Central", 19, a.WHITE, a.SANS, 600, "middle")
   + a.text(450, 312, "acá corre el", 15, SKY, a.MONO, 400, "middle")
   + a.text(450, 334, "controlador", 15, SKY, a.MONO, 400, "middle"), 50, 100)
a.add(line(268, 295, 316, 295, a.BLUE, 4))
# fibra
a.add(line(584, 295, 662, 295, a.BLUE, 4))
a.add(a.text(623, 268, "fibra", 15, a.GREY, a.MONO, 400, "middle"))
for t0 in (27, 77):
    at(a, line(584, 295, 662, 295, a.BAD, 5, "6 6") + xmark(a, 623, 295, 16), t0, t0 + 23 if t0 == 27 else 100, still=1 if t0 == 27 else 0)

# hotel
a.add(a.box(662, 186, 490, 368, a.WHITE, a.LINE, rx=18, sw=2))
a.add(a.text(686, 220, "Hotel en Colonia", 17, a.GREY, a.SANS, 600))
a.add(dev(a, 686, 244, 200, 82, "Gateway ER", "WAN: la fibra", icon="server"))
at(a, dev(a, 920, 244, 210, 82, "OC300", "en el rack", icon="server", dark=True), 0, 50, still=1)
at(a, a.box(920, 244, 210, 82, a.SLATE, a.LINE, rx=14, sw=2, extra='stroke-dasharray="6 5"')
   + a.text(1025, 280, "sin controlador", 16, a.GREY, a.SANS, 600, "middle")
   + a.text(1025, 304, "en el lugar", 16, a.GREY, a.SANS, 600, "middle"), 50, 100)
a.add(line(886, 285, 920, 285, a.BLUE, 3))
a.add(line(786, 326, 786, 360, a.BLUE, 3) + line(712, 360, 1110, 360, a.BLUE, 3))
for cx in (730, 830):
    a.add(line(cx, 360, cx, 384, a.BLUE, 3) + eap(a, cx, 410, 24))
a.add(a.text(780, 458, "EAP", 15, a.GREY, a.MONO, 400, "middle"))
a.add(line(1010, 360, 1010, 384, a.BLUE, 3))
a.add(dev(a, 918, 384, 212, 62, "Huésped", "celular", icon="phone"))
a.add(line(890, 360, 890, 476, a.BLUE, 3))
a.add(dev(a, 686, 476, 444, 62, "Técnico en el lugar", "notebook en la LAN", icon="laptop"))

# panel de estado
PX, PY = 48, 384
a.add(a.box(PX, PY, 560, 170, a.WHITE, a.LINE, rx=16))
ROWS = ["Desde la oficina", "En el lugar", "Portal del huésped"]
for i, r in enumerate(ROWS):
    a.add(a.text(PX + 22, PY + 42 + i * 48, r, 17, a.INK, a.SANS, 600))
EST = [  # (fase, fila, ok, texto)
    (0, 0, True, "entra por Cloud Access"), (0, 1, True, "gestiona el OC300"), (0, 2, True, "autentica"),
    (1, 0, False, "sin fibra no entra"), (1, 1, True, "el OC300 sigue mandando"), (1, 2, True, "sigue autenticando"),
    (2, 0, True, "gestiona en la nube"), (2, 1, True, "también por la nube"), (2, 2, True, "con licencia vigente"),
    (3, 0, False, "Central no llega a los equipos"), (3, 1, False, "no hay controlador acá"), (3, 2, False, "no autentica"),
]
for f, r, good, txt in EST:
    y = PY + 36 + r * 48
    mark = check(a, PX + 252, y, 13) if good else xmark(a, PX + 252, y, 13)
    col = a.OK if good else a.BAD
    at(a, mark + a.text(PX + 276, y + 6, txt, 16, col, a.SANS, 600), F[f][0] + 2, F[f][1], still=1 if f == 1 else 0)

# ---- escenario A
# 1: el técnico entra por Cloud Access hasta el OC300
travel(a, dot(a, a.CYAN), [(268, 295), (450, 295), (662, 295), (786, 300), (920, 300), (1025, 300)], 4, 13, hold=1)
travel(a, dot(a, a.OK), [(1025, 300), (920, 300), (786, 300), (662, 295), (450, 295), (268, 295)], 14, 22, hold=1)
# 2: la fibra cortada
travel(a, dot(a, a.CYAN), [(268, 295), (450, 295), (576, 295)], 29, 33, hold=4)
travel(a, dot(a, a.CYAN), [(890, 476), (890, 360), (1025, 360), (1025, 326)], 36, 40, hold=2)
travel(a, dot(a, a.OK), [(1060, 384), (1060, 326)], 42, 45, hold=2)

# ---- escenario B
# 3: los equipos hablan con la nube; el técnico gestiona desde la oficina
for i, t0 in enumerate((53, 57)):
    travel(a, dot(a, a.CYAN if i == 0 else a.OK), [(730, 384), (730, 360), (786, 360), (786, 326), (686, 300), (662, 295), (584, 295)], t0, t0 + 4, hold=0.5)
travel(a, dot(a, a.OK), [(268, 295), (316, 295)], 63, 66, hold=0.5)
# 4: corte: nadie gestiona
travel(a, dot(a, a.CYAN), [(890, 476), (890, 360), (980, 360), (980, 336)], 80, 84, hold=0.6)
at(a, xmark(a, 980, 340, 14), 84, 100)

# notas abajo
at(a, note(a, 48, 572, 1104, 44, "", ["Con controlador local o integrado, el servicio, la configuración y los logs quedan en el lugar."], "info"), 0, 25)
at(a, note(a, 48, 572, 1104, 44, "", ["Lo que depende del controlador corriendo, como el portal, sigue: el OC300 está ahí."], "ok"), 25, 50, still=1)
at(a, note(a, 48, 572, 1104, 44, "", ["No hay host que cuidar, pero la gestión depende de internet y, en Standard, de licencias vigentes."], "info"), 50, 75)
at(a, note(a, 48, 572, 1104, 44, "", ["La red no se cae: los equipos siguen con lo último. Cualquier cambio espera a que vuelva internet."], "amb"), 75, 100)

write(a, 1, "r1", "Cloud Access o controlador en la nube: qué pasa cuando se corta la fibra",
      "Animación en cuatro tiempos con el técnico de IES en la oficina, la nube de TP-Link, la fibra y un hotel en Colonia con gateway ER, "
      "dos EAP, el celular de un huésped y la notebook del técnico en la LAN. "
      "1: con un OC300 en el rack y Cloud Access, el técnico entra desde la oficina; la nube es solo la puerta y quien gestiona es el OC300. "
      "2: se corta la fibra; desde la oficina ya no se entra, pero en el lugar la notebook sigue gestionando el OC300 y el portal sigue autenticando al huésped. "
      "3: con Omada Central no hay controlador en el lugar; los equipos le hablan a la nube por internet y el técnico gestiona desde la nube; "
      "en Central Standard cada equipo lleva su licencia. "
      "4: se corta la fibra; los equipos siguen con la última configuración que recibieron, pero nadie puede cambiar nada, ni siquiera desde la notebook en el lugar, hasta que vuelva internet.",
      [8, 38, 46, 62, 88])
