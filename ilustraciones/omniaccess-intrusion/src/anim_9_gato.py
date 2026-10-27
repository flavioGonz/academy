#!/usr/bin/env python3
"""Lección 9 · Teoría · Sin clasificación, la geometría manda.
Sale de teoria_md (Cómo funciona): con clasificación la cámara descarta lo que no es persona o vehículo; sin clasificación,
como contó un usuario en un foro, ni el porcentaje ni la sensibilidad frenan a un gato que entra en la zona: la solución
pasa por achicar la zona o mover la línea; un cambio por vez y una semana de datos para saber si sirvió."""
from _anim_omni import new, out, when, person, check

a = new(24, "FALSAS ALARMAS", "Un gato, una cámara que no clasifica y una zona")
a.steps([
    "Cámara sin clasificación: un gato entra a la zona y dispara.",
    "Bajás la sensibilidad: el gato sigue entrando y sigue disparando.",
    "Achicás la zona a donde importa: el gato pasa por afuera.",
    "Una persona entra a la zona chica: dispara. Lo que importa se sigue viendo.",
], still=2)


def cat(c="#4A3A2A"):
    return (f'<ellipse cx="0" cy="0" rx="26" ry="13" fill="{c}"/>'
            f'<circle cx="26" cy="-12" r="11" fill="{c}"/>'
            f'<path d="M19 -20 l3 -12 l6 9 z M29 -21 l5 -11 l3 11 z" fill="{c}"/>'
            f'<path d="M-24 -4 q-18 -6 -14 -26" fill="none" stroke="{c}" stroke-width="5" stroke-linecap="round"/>'
            f'<path d="M-14 10 v12 M-4 10 v12 M10 10 v12 M18 10 v12" stroke="{c}" stroke-width="4" stroke-linecap="round"/>')


FX, FY, FW, FH = 48, 182, 700, 392
a.add(a.box(FX, FY, FW, FH, "#DCE9D6", a.LINE, rx=10))
a.add(a.box(FX, FY, FW, 92, "#C9D6E3", rx=10))
a.add(f'<path d="M{FX} {FY + 92} H{FX + FW}" stroke="{a.GREY}" stroke-width="4"/>')
for x in range(FX + 20, FX + FW, 40):
    a.add(f'<path d="M{x} {FY + 92} v-34" stroke="{a.GREY}" stroke-width="3"/>')
a.add(a.text(FX + FW - 14, FY + 26, "cerco", 15, a.TXT, a.MONO, 600, "end"))
a.add(a.box(FX + 300, FY + 50, 90, 42, "#B8C7D6", rx=4) + a.text(FX + 345, FY + 77, "portón", 15, a.INK, a.MONO, 600, "middle"))

# zona grande (tiempos 1 y 2) y zona chica (3 y 4)
big = f"M{FX + 40} {FY + 120} L{FX + FW - 40} {FY + 120} L{FX + FW - 30} {FY + FH - 20} L{FX + 30} {FY + FH - 20} z"
small = f"M{FX + 270} {FY + 100} L{FX + 420} {FY + 100} L{FX + 430} {FY + 190} L{FX + 260} {FY + 190} z"
when(a, f'<path d="{big}" fill="{a.BAD}" fill-opacity=".10" stroke="{a.BAD}" stroke-width="3" stroke-dasharray="10 7"/>'
     + a.text(FX + 60, FY + 146, "zona", 16, a.BAD, a.MONO, 600), 0, 50, still=0)
when(a, f'<path d="{small}" fill="{a.BAD}" fill-opacity=".12" stroke="{a.BAD}" stroke-width="3" stroke-dasharray="10 7"/>'
     + a.text(FX + 440, FY + 130, "zona chica", 16, a.BAD, a.MONO, 600), 51, 100, still=1)

# gato: cruza el césped en los tiempos 1, 2 y 3
CY = FY + 300
for t0 in (2, 27, 52):
    a.add(a.group(cat(), a.move([(0, FX + 90, CY), (t0, FX + 90, CY), (t0 + 18, FX + FW - 110, CY), (100, FX + FW - 110, CY)]),
                  a.show(t0, t0 + 19, 0.6), still=1 if t0 == 52 else 0))
# disparos del gato
for t in (9, 34):
    when(a, a.pill(FX + FW / 2, FY + 250, "¡evento!", a.WHITE, a.BAD, 16, 32, "middle"), t, t + 12, still=0)
when(a, a.pill(FX + FW / 2, FY + 250, "sin evento: está fuera de la zona", a.OK, a.OKBG, 16, 32, "middle"), 60, 75, still=1)
# persona en el tiempo 4
a.add(a.group(person(a, 0, 0, a.INK, 1.4), a.move([(0, FX + 345, FY + FH - 30), (76, FX + 345, FY + FH - 30), (86, FX + 345, FY + 160), (100, FX + 345, FY + 160)]),
              a.show(76, 100, 0.6), still=0))
when(a, a.pill(FX + 520, FY + 172, "¡evento!", a.WHITE, a.BAD, 16, 32, "middle"), 86, 100, still=0)

# ---- panel de ajustes y registro
RX, RW = 780, 372
a.add(a.box(RX, FY, RW, 176, a.WHITE, a.LINE, rx=14))
a.add(a.text(RX + 20, FY + 32, "Ajustes de la regla", 17, a.INK, a.SANS, 600))
a.add(a.text(RX + 20, FY + 66, "clasificación", 15, a.GREY, a.MONO) + a.text(RX + 200, FY + 66, "no tiene", 16, a.BAD, a.MONO, 600))
a.add(a.text(RX + 20, FY + 100, "sensibilidad", 15, a.GREY, a.MONO))
a.add(a.group(a.text(RX + 200, FY + 100, "80", 16, a.INK, a.MONO, 600), a.keyframes([(0, 1), (26, 1), (27, 0), (99, 0), (100, 1)]), still=0))
a.add(a.group(a.text(RX + 200, FY + 100, "40", 16, a.AMB, a.MONO, 600), a.keyframes([(0, 0), (26, 0), (27, 1), (99, 1), (100, 0)]), still=1))
a.add(a.text(RX + 20, FY + 134, "zona", 15, a.GREY, a.MONO))
a.add(a.group(a.text(RX + 200, FY + 134, "grande", 16, a.INK, a.MONO, 600), a.keyframes([(0, 1), (50, 1), (51, 0), (99, 0), (100, 1)]), still=0))
a.add(a.group(a.text(RX + 200, FY + 134, "chica", 16, a.AMB, a.MONO, 600), a.keyframes([(0, 0), (50, 0), (51, 1), (99, 1), (100, 0)]), still=1))
a.add(a.text(RX + 20, FY + 160, "un cambio por vez", 15, a.GREY, a.SANS))

LY = FY + 196
a.add(a.box(RX, LY, RW, 196, a.WHITE, a.LINE, rx=14))
a.add(a.text(RX + 20, LY + 32, "Detecciones", 17, a.INK, a.SANS, 600))
LOG = [(10, "gato", False), (35, "gato", False), (86, "persona", True)]
for i, (t, who, ok) in enumerate(LOG):
    y = LY + 52 + i * 44
    when(a, a.box(RX + 14, y, RW - 28, 36, a.SLATE, rx=8) + a.text(RX + 30, y + 24, f"zona · {who}", 16, a.INK, a.MONO, 600)
         + check(a, RX + RW - 40, y + 18, ok, 13) + a.text(RX + RW - 62, y + 24, "real" if ok else "falsa", 15, a.OK if ok else a.BAD, a.MONO, 600, "end"),
         t, 100, still=1 if i < 2 else 0)

a.add(a.text(48, 618, "Con clasificación, la cámara descarta lo que no es persona o vehículo. Sin ella, decide la geometría.", 16, a.TXT, a.SANS, 600))
a.add(a.text(48, 644, "Después, una semana de datos: el Análisis muestra si bajó el porcentaje de falsas de la cámara.", 16, a.TXT, a.SANS, 600))

out(a, 9, 1, "Sin clasificación, la geometría manda",
    "Animación en cuatro tiempos sobre el cuadro de una cámara que no clasifica objetos: un cerco con un portón arriba y césped abajo. A la derecha, los ajustes de la regla y la lista de detecciones. "
    "Tiempo 1: con una zona grande sobre todo el césped y sensibilidad 80, un gato cruza y dispara un evento, que queda como falsa. "
    "Tiempo 2: con la sensibilidad bajada a 40, el gato vuelve a cruzar y vuelve a disparar. "
    "Tiempo 3: la zona se achica a la entrada del portón; el gato cruza el césped por afuera y no hay evento. "
    "Tiempo 4: una persona camina hacia el portón, entra a la zona chica y dispara un evento real. "
    "Al pie: con clasificación la cámara descarta lo que no es persona o vehículo; sin ella decide la geometría. Después, una semana de datos para ver en el Análisis si bajó el porcentaje de falsas.",
    [12, 40, 66, 95])
