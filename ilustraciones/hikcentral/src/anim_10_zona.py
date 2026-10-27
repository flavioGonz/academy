"""Teoría de Asistencia y hora: el registro viaja con la hora de la controladora."""
from _anim_hc import *

caps = ["Marca a las 10:00 en la controladora A, en la misma zona que el SYS.",
        "El SYS la cruza con el turno y la pasada aparece en vivo.",
        "Otra marca en la controladora B, configurada en otra zona horaria.",
        "Esa pasada no aparece en vivo: queda solo en el histórico."]
a = new(26, "Asistencia", "La pasada viaja con la hora de la controladora", caps, still=3)

a.add(card(a, 48, 200, 320, 92, "Controladora A", "UTC-3 · NTP 192.168.88.10"))
a.add(card(a, 48, 392, 320, 92, "Controladora B", "otra zona horaria", stroke=a.BAD, sw=3))
a.add(card(a, 440, 296, 300, 92, "SYS", "UTC-3 · calcula con su hora", dark=True))
a.add(a.box(800, 186, 352, 150, a.WHITE, a.LINE, rx=16))
a.add(a.text(820, 218, "Control Client · pasadas en vivo", 15, a.TXT, a.SANS, 600))
a.add(a.box(800, 360, 352, 150, a.WHITE, a.LINE, rx=16))
a.add(a.text(820, 392, "Histórico de registros", 15, a.TXT, a.SANS, 600))
a.add(line(a, 368, 246, 440, 330, a.LINE, 3, arrow=False))
a.add(line(a, 368, 438, 440, 356, a.LINE, 3, arrow=False))
a.add(line(a, 740, 330, 800, 262, a.LINE, 3, arrow=False))
a.add(line(a, 740, 356, 800, 436, a.LINE, 3, arrow=False))

s0, s1 = ph(a, 0)
token(a, "10:00 · Prueba Lab", [(s0 + 3, 208, 316), (s0 + 14, 590, 280)], bg=a.CYAN)
s0, s1 = ph(a, 1)
token(a, "en turno", [(s0 + 2, 590, 280), (s0 + 10, 976, 262)], bg=a.OK)
row_a = a.box(820, 238, 312, 40, a.OKBG, rx=8) + a.text(836, 264, "10:00 · Prueba Lab · Puerta A", 14, a.OK, a.MONO, 600)
a.add(a.group(row_a, a.show(s0 + 10, 100), still=1))
row_ah = a.box(820, 412, 312, 40, a.SLATE, rx=8) + a.text(836, 438, "10:00 · Prueba Lab · Puerta A", 14, a.TXT, a.MONO)
a.add(a.group(row_ah, a.show(s0 + 10, 100), still=1))
s0, s1 = ph(a, 2)
token(a, "otra hora · B", [(s0 + 3, 208, 508), (s0 + 14, 590, 412)], bg=a.AMB)
s0, s1 = ph(a, 3)
token(a, "solo histórico", [(s0 + 2, 590, 412), (s0 + 10, 976, 478)], bg=a.AMB)
row_bh = a.box(820, 460, 312, 40, a.AMBBG, rx=8) + a.text(836, 486, "Puerta B · hora de otra zona", 14, a.AMB, a.MONO, 600)
a.add(a.group(row_bh, a.show(s0 + 10, s1), still=1))
a.add(a.group(a.pill(976, 306, "Puerta B: no aparece", a.BAD, a.BADBG, anchor="middle"), a.show(s0 + 10, s1), still=1))

a.add(a.text(48, 574, "La plataforma no maneja múltiples zonas horarias: SYS y controladoras en la misma zona,", 17, a.TXT))
a.add(a.text(48, 602, "con la misma fuente de hora (NTP al SYS o al del cliente). Primero la hora, después los turnos.", 17, a.TXT))
write(a, "10-t1.svg", "La pasada viaja con la hora de la controladora", [10, 38, 62, 94])
