#!/usr/bin/env python3
"""Lección 4 · Teoría · Cómo OmniAccess lee el horario de armado.
Sale de teoria_md (Cómo funciona): bloques por día (1 lunes a 7 domingo), 22:00 a 06:00 se guarda partido en
22:00 a 24:00 y 00:00 a 06:00 del día siguiente; OmniAccess lo lee (/ISAPI/Event/schedules/lineDetections/lineDetection-1),
junta los bloques partidos, lo describe (L–D 22:00–06:00), calcula con la hora del servidor si está armada (verde)
o no (ámbar) y guarda esa lectura cinco minutos."""
from _anim_omni import new, out, when, travel, seq, box, pill0

a = new(25, "HORARIO DE ARMADO", "Del horario partido de la cámara al punto verde")
a.steps([
    "OmniAccess pide a la cámara el horario de la regla de línea.",
    "Junta los bloques partidos por la medianoche y lo describe en palabras.",
    "Con la hora del servidor calcula el estado: a las 15:00, desarmada.",
    "Otra consulta antes de 5 minutos: contesta la memoria, sin pedir a la cámara.",
    "A las 23:00 la hora cae dentro del horario: armada, punto verde.",
], still=4)

# ---- cámara: documento de horario
CX, CY, CW = 48, 182, 360
a.add(a.box(CX, CY, CW, 274, a.WHITE, a.LINE, rx=14))
a.add(a.text(CX + 20, CY + 30, "Cámara · horario de la línea", 17, a.INK, a.SANS, 600))
a.add(a.text(CX + 20, CY + 54, "día   bloques", 15, a.GREY, a.MONO, 600))
for i in range(7):
    y = CY + 82 + i * 25
    a.add(a.text(CX + 26, y, str(i + 1), 15, a.INK, a.MONO, 600))
    a.add(a.text(CX + 74, y, "00:00–06:00", 15, a.TXT, a.MONO))
    a.add(a.text(CX + 204, y, "22:00–24:00", 15, a.TXT, a.MONO))
a.add(a.text(CX + 20, CY + 260, "1 es lunes, 7 es domingo", 15, a.GREY, a.SANS))
# resalta el par partido: 22-24 del día 1 y 00-06 del día 2
when(a, f'<rect x="{CX + 196}" y="{CY + 66}" width="120" height="22" rx="6" fill="none" stroke="{a.AMB}" stroke-width="2.5"/>'
     f'<rect x="{CX + 66}" y="{CY + 91}" width="120" height="22" rx="6" fill="none" stroke="{a.AMB}" stroke-width="2.5"/>', 20, 40, still=0)

# ---- OmniAccess
OX = 472
a.add(box(OX, 182, 280, 84, "OmniAccess", "hora del servidor", "server"))
seq(a, f"M{OX - 8} 214 H{CX + CW + 10}", 1, 19, a.BLUE, "GET …/lineDetection-1", (OX + CX + CW) / 2, 204, still=0)
travel(a, (OX - 20, 214), (CX + CW + 24, 214), 1, 8, dot=8)
seq(a, f"M{CX + CW + 10} 246 H{OX - 8}", 9, 19, a.CYAN, "bloques por día", (OX + CX + CW) / 2, 238, still=0)

# ---- tiempo 2: juntar
when(a, a.text(OX + 140, 300, "junta los bloques partidos", 15, a.AMB, a.MONO, 600, "middle"), 20, 40, still=0)
when(a, a.pill(OX + 70, 316, "22:00–24:00", a.AMB, a.AMBBG, 15, 30, "middle")
     + a.text(OX + 140, 337, "+", 18, a.AMB, a.MONO, 600, "middle")
     + a.pill(OX + 210, 316, "00:00–06:00", a.AMB, a.AMBBG, 15, 30, "middle"), 21, 40, still=0)
when(a, a.arrow(f"M{OX + 140} 352 V372", a.AMB, 3), 27, 40, still=0)
when(a, a.pill(OX + 140, 380, "22:00–06:00", a.WHITE, a.AMB, 16, 32, "middle"), 28, 40, still=0)

# ---- memoria 5 min
when(a, a.pill(OX + 140, 300, "lectura guardada 5 min", a.BLUE, a.WHITE, 15, 30, "middle"), 41, 100, still=1)

# ---- pantalla
PX, PY, PW = 800, 182, 352
a.add(a.box(PX, PY, PW, 262, a.INK, rx=14))
a.add(a.text(PX + 22, PY + 34, "Vista de pared · canal", 17, a.WHITE, a.SANS, 600))
a.add(a.text(PX + 22, PY + 66, "horario de la línea", 15, "#9FC3E3", a.MONO))
when(a, a.text(PX + 22, PY + 112, "L–D 22:00–06:00", 28, a.WHITE, a.MONO, 600), 32, 100, still=1)
seq(a, f"M{OX + 288} 400 H{PX - 10}", 32, 40, a.BLUE, "", None, None, still=0)
# estado
amber = f'<circle cx="{PX + 36}" cy="{PY + 172}" r="12" fill="#F2A33A"/>' + a.text(PX + 60, PY + 179, "desarmada ahora", 19, "#FFD28A", a.SANS, 600)
green = f'<circle cx="{PX + 36}" cy="{PY + 172}" r="12" fill="#2FCB86"/>' + a.text(PX + 60, PY + 179, "armada", 19, "#8EF0C0", a.SANS, 600)
when(a, amber, 41, 80, still=0)
when(a, green, 81, 100, still=1)
when(a, a.text(PX + 22, PY + 226, "avisa si hay cruce", 15, "#8EF0C0", a.MONO), 81, 100, still=1)
when(a, a.text(PX + 22, PY + 226, "fuera de horario: no avisa", 15, "#FFD28A", a.MONO), 41, 80, still=0)

# ---- tiempo 4: consulta desde la memoria
seq(a, f"M{PX - 6} 300 H{OX + 290}", 61, 80, a.GREY, "", None, None, still=0)
when(a, a.pill(OX + 140, 344, "otra consulta: contesta la memoria", a.INK, a.SLATE, 15, 30, "middle")
     + a.pill(OX + 140, 384, "sin pedido a la cámara", a.GREY, a.WHITE, 15, 30, "middle"), 62, 80, still=0)

# ---- línea de 24 h
LX0, LX1, LY = 100, 1100, 540
def hx(h):
    return LX0 + (LX1 - LX0) * h / 24
a.add(a.text(48, 492, "Hoy, según la hora del servidor", 17, a.INK, a.SANS, 600))
a.add(a.box(LX0, LY - 16, LX1 - LX0, 32, a.WHITE, a.LINE, rx=6))
a.add(a.box(hx(0), LY - 16, hx(6) - hx(0), 32, a.OKBG, a.OK, rx=6, sw=2))
a.add(a.box(hx(22), LY - 16, hx(24) - hx(22), 32, a.OKBG, a.OK, rx=6, sw=2))
a.add(a.text((hx(0) + hx(6)) / 2, LY + 6, "armada", 15, a.OK, a.MONO, 600, "middle"))
for h in (0, 6, 12, 18, 22, 24):
    a.add(a.text(hx(h), LY + 40, f"{h:02d}:00", 15, a.GREY, a.MONO, 600, "middle"))
needle = (f'<line x1="0" y1="-30" x2="0" y2="30" stroke="{a.INK}" stroke-width="3"/>'
          f'<circle cx="0" cy="-30" r="6" fill="{a.INK}"/>')
a.add(a.group(f'<g transform="translate({hx(15)} {LY})">{needle}</g>', a.show(41, 80, 0.4), still=0))
a.add(a.group(f'<g transform="translate({hx(23)} {LY})">{needle}</g>', a.show(84, 100, 0.4), still=1))
mv = a.move([(0, hx(15), LY), (80, hx(15), LY), (84, hx(23), LY), (100, hx(23), LY)])
a.add(a.group(needle, mv, a.show(80, 84, 0.3), still=0))
when(a, a.text(hx(15), LY - 40, "15:00", 16, a.AMB, a.MONO, 600, "middle"), 41, 80, still=0)
when(a, a.text(hx(23), LY - 40, "23:00", 16, a.OK, a.MONO, 600, "middle"), 84, 100, still=1)

a.add(a.text(48, 640, "El 22:00–06:00 no entra en un solo bloque: cruza la medianoche. La cámara lo parte; OmniAccess lo junta para mostrarlo.", 16, a.TXT, a.SANS, 600))

out(a, 4, 1, "Del horario partido al punto verde",
    "Animación en cinco tiempos. A la izquierda, el horario de la regla de línea en la cámara: siete días, del 1 (lunes) al 7 (domingo), "
    "cada uno con un bloque de 00:00 a 06:00 y otro de 22:00 a 24:00. En el centro, OmniAccess con la hora del servidor; a la derecha, la vista de pared del canal. "
    "Abajo, una línea de 24 horas con los tramos armados de 00:00 a 06:00 y de 22:00 a 24:00. "
    "Tiempo 1: OmniAccess pide el horario con GET a lineDetection-1 y la cámara devuelve los bloques por día. "
    "Tiempo 2: se resaltan el bloque de 22:00 a 24:00 de un día y el de 00:00 a 06:00 del siguiente; OmniAccess los junta en 22:00 a 06:00 y la pantalla muestra L–D 22:00–06:00. La lectura queda guardada 5 minutos. "
    "Tiempo 3: con la hora del servidor, a las 15:00, el punto es ámbar: desarmada ahora, fuera de horario no avisa. "
    "Tiempo 4: otra consulta de estado antes de 5 minutos la contesta la memoria, sin pedido a la cámara. "
    "Tiempo 5: a las 23:00 la hora cae dentro del horario: punto verde, armada, avisa si hay cruce.",
    [10, 34, 52, 72, 94])
