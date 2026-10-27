"""Teoría lección 4: corte de red, batería y umbrales en SP+."""
from _apdx import *

a = new(20, "Corte de luz: qué pasa con la batería, volt a volt")
a.steps(["Con red: el transformador alimenta y carga la batería.",
         "Se corta la red: la batería sostiene todo. TBL 2.2, falla de AC.",
         "La batería baja a 10,5 V: falla de batería, TBL 2.1.",
         "9,1 V: desconexión de protección. A 8,5 V la central se apaga."], still=1)
a.add(card(a, 48, 190, 300, 90, "Transformador", "16,5 Vac · 40 VA"))
a.add(card(a, 48, 330, 300, 90, "Batería", "12 V · 7 Ah"))
a.add(card(a, 440, 200, 260, 220, "Central", "SP+", dark=True))
at(a, line(a, "M348 235H440", "#D2492F", 5) + line(a, "M440 330H348", a.OK, 4, "8 6") + a.text(394, 365, "carga", 14, a.OK, a.MONO, 600, "middle"), 0, 25, 0)
at(a, line(a, "M348 235H440", a.GREY, 4, "4 8") + a.text(394, 222, "sin red", 14, a.BAD, a.MONO, 700, "middle"), 25, 100, 1)
at(a, line(a, "M348 375H440", "#D2492F", 5), 25, 100, 1)
at(a, a.box(460, 300, 220, 34, a.BAD, None, rx=17) + a.text(570, 323, "TBL 2.2 · AC", 15, "#fff", a.MONO, 700, "middle"), 25, 100, 1)
at(a, a.box(460, 346, 220, 34, a.AMB, None, rx=17) + a.text(570, 369, "TBL 2.1 · batería", 15, "#fff", a.MONO, 700, "middle"), 50, 100, 0)
# voltímetro
VX, VY = 760, 180
a.add(card(a, VX, VY, 392, 330, "Tensión de batería", None))
scale = [(13.0, ""), (10.5, "10,5 V falla"), (9.1, "9,1 V protección"), (8.5, "8,5 V apagado")]
Y = lambda v: VY + 70 + (13.4 - v) / (13.4 - 8.0) * 230
a.add(a.box(VX + 40, VY + 70, 60, 230, a.SLATE, a.LINE, rx=8))
for v, lab in scale[1:]:
    a.add(line(a, f"M{VX + 30} {Y(v):.0f}H{VX + 110}", a.BAD if v == 8.5 else a.AMB, 2, "6 4"))
    a.add(a.text(VX + 124, Y(v) + 5, lab, 16, a.BAD if v == 8.5 else a.AMB, a.SANS, 600))
for (s, e, v, col, still) in [(0, 25, 13.0, a.OK, 0), (25, 50, 11.8, a.OK, 1), (50, 75, 10.4, a.AMB, 0), (75, 100, 8.6, a.BAD, 0)]:
    top = Y(v)
    at(a, a.box(VX + 44, top, 52, VY + 296 - top, col, None, rx=6), s, e, still)
caption(a, 600, [(0, 25, "En la SP+ la batería admitida es de 12 V y 7 Ah, o de 4 Ah.", None),
                 (25, 50, "La falla de AC se ve enseguida, pero se reporta después del retardo de [839].", None),
                 (50, 75, "Cuantos más mA cuelgan del AUX, antes llega este momento.", a.AMB),
                 (75, 100, "Sin red y sin batería, la central se apaga y no hay alarma: por eso se calcula la autonomía.", a.BAD)], still=1)
write(a, "4-t1.svg", "Corte de luz: qué pasa con la batería, volt a volt",
      "Animación en cuatro tiempos con transformador, batería, central y un voltímetro de batería. 1: con red, el transformador alimenta y carga la batería. "
      "2: se corta la red, la batería sostiene la central y aparece TBL 2.2, falla de AC. 3: la batería baja a 10,5 V y aparece TBL 2.1, falla de batería. "
      "4: a 9,1 V hay desconexión de protección y a 8,5 V la central se apaga.")
