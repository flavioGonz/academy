#!/usr/bin/env python3
"""Lección 8 · Teoría · Decidir por cámara, corregir de a una y la retención.
Sale de teoria_md (Cómo funciona): Historial y Evidencia son vistas de la misma tabla; las acciones del canal deciden por
cámara (todo lo pendiente de 6 horas); la corrección desde la ficha de la detección cambia solo esa; las fotos viven en el
bucket de intrusión y la retención es una regla de vencimiento: pasados los días configurados se borran solas; las
detecciones siguen en la base, sin su imagen."""
from _anim_omni import new, out, when, person

a = new(24, "REGISTRO", "Por cámara, de a una, y lo que queda con los días")
a.steps([
    "En Evidencia, cuatro detecciones de la misma cámara, todas pendientes.",
    "Acción del canal, Falsa alarma: decide por cámara, todo lo pendiente de 6 h.",
    "Corrección desde la ficha, Era real: cambia solo esa detección.",
    "Pasan los días de retención: las fotos se borran; las detecciones quedan.",
], still=2)

HORAS = ["22:41:05", "23:05:12", "01:12:40", "03:30:18"]
CW, CH, GAP = 258, 262, 24
X0, Y0 = 48, 186
for i, h in enumerate(HORAS):
    x = X0 + i * (CW + GAP)
    a.add(a.box(x, Y0, CW, CH, a.WHITE, a.LINE, rx=14))
    # foto (se borra en el tiempo 4)
    photo = (a.box(x + 12, Y0 + 12, CW - 24, 140, "#1B3A57", rx=10)
             + f'<path d="M{x + 12} {Y0 + 120} L{x + CW - 12} {Y0 + 104}" stroke="#355A7C" stroke-width="3"/>'
             + person(a, x + 70 + i * 30, Y0 + 92, "#9FC3E3", 1.1))
    a.add(a.group(photo, a.keyframes([(0, 1), (77, 1), (80, 0), (99, 0), (100, 1)]), still=1))
    gone = (a.box(x + 12, Y0 + 12, CW - 24, 140, "#F3F6F9", a.LINE, rx=10, extra='stroke-dasharray="6 6"')
            + a.text(x + CW / 2, Y0 + 88, "sin imagen", 16, a.GREY, a.MONO, 600, "middle"))
    a.add(a.group(gone, a.keyframes([(0, 0), (78, 0), (80, 1), (99, 1), (100, 0)]), still=0))
    a.add(a.text(x + 16, Y0 + 182, h, 16, a.INK, a.MONO, 600))
    a.add(a.text(x + 16, Y0 + 206, "Perímetro Norte 12", 15, a.TXT, a.SANS))
    py = Y0 + 220
    pend = a.pill(x + 16, py, "Pendiente", a.AMB, a.AMBBG, 15, 28)
    fals = a.pill(x + 16, py, "Falsa", a.TXT, a.SLATE, 15, 28)
    real = a.pill(x + 16, py, "Real", a.WHITE, a.BAD, 15, 28)
    a.add(a.group(pend, a.keyframes([(0, 1), (28, 1), (29, 0), (99, 0), (100, 1)]), still=0))
    if i == 2:
        a.add(a.group(fals, a.keyframes([(0, 0), (28, 0), (29, 1), (55, 1), (56, 0), (100, 0)]), still=0))
        a.add(a.group(real, a.keyframes([(0, 0), (55, 0), (56, 1), (99, 1), (100, 0)]), still=1))
    else:
        a.add(a.group(fals, a.keyframes([(0, 0), (28, 0), (29, 1), (99, 1), (100, 0)]), still=1))

# tiempo 2: acción del canal
when(a, f'<rect x="{X0 - 8}" y="{Y0 - 8}" width="{4 * CW + 3 * GAP + 16}" height="{CH + 16}" rx="18" fill="none" stroke="{a.BLUE}" stroke-width="3" stroke-dasharray="10 7"/>', 26, 49, still=0)
when(a, a.pill(48, 470, "acción del canal: Falsa alarma → las 4 pendientes de la cámara", a.BLUE, a.WHITE, 16, 34), 26, 50, still=0)
# tiempo 3: corrección de una
x3 = X0 + 2 * (CW + GAP)
when(a, f'<rect x="{x3 - 6}" y="{Y0 - 6}" width="{CW + 12}" height="{CH + 12}" rx="17" fill="none" stroke="{a.BAD}" stroke-width="3.5"/>', 51, 75, still=1)
when(a, a.pill(x3 + CW / 2, 470, "ficha: Era real → solo esta", a.BAD, a.BADBG, 16, 34, "middle"), 51, 75, still=1)
# tiempo 4: retención
when(a, a.box(48, 466, 1104, 96, a.WHITE, a.LINE, rx=12)
     + a.text(70, 498, "bucket intrusion · regla de vencimiento", 17, a.INK, a.SANS, 600)
     + a.text(70, 528, "Pasados los días configurados, las fotos se borran solas.", 16, a.TXT, a.SANS)
     + a.text(70, 552, "Las detecciones siguen en la base: hora, cámara, tipo y decisión, sin imagen.", 16, a.TXT, a.SANS), 77, 100, still=0)

a.add(a.text(48, 640, "Historial y Evidencia muestran la misma tabla: lo que cambiás en una se ve en la otra.", 16, a.TXT, a.SANS, 600))

out(a, 8, 1, "Por cámara, de a una, y la retención",
    "Animación en cuatro tiempos con cuatro tarjetas de Evidencia de la cámara Perímetro Norte 12, con foto y hora: 22:41:05, 23:05:12, 01:12:40 y 03:30:18. "
    "Tiempo 1: las cuatro están Pendientes. "
    "Tiempo 2: la acción del canal Falsa alarma decide por cámara y las cuatro pendientes pasan a Falsa. "
    "Tiempo 3: desde la ficha de la detección de las 01:12:40 se corrige con Era real y solo esa pasa a Real; las otras siguen Falsas. "
    "Tiempo 4: pasan los días de retención; la regla de vencimiento del bucket intrusion borra las fotos y cada tarjeta muestra sin imagen, "
    "pero las detecciones siguen en la base con hora, cámara, tipo y decisión. "
    "Al pie: Historial y Evidencia muestran la misma tabla.",
    [12, 38, 62, 92])
