#!/usr/bin/env python3
"""Lección 5 · Teoría · Cómo llega la detección a cada pantalla.
Sale de teoria_md (Cómo funciona): cada detección se emite por un socket a todas las pantallas abiertas; el Monitor
Intrusión pinta el canal de rojo y lo sube arriba; el Mapa, si la línea está dibujada y dentro de su horario, la hace
titilar, pita y dice "Persona en" y el nombre de la cámara; las pantallas de pared leen el estado cada pocos segundos
y suenan según el ajuste de Monitores; el navegador bloquea el audio hasta un toque (o Chrome en kiosco con autoplay)."""
from _anim_omni import new, out, when, travel, box

a = new(24, "AVISOS", "Una detección, tres pantallas, dos caminos")
a.steps([
    "Llega una detección: el servidor la emite por socket a las pantallas abiertas.",
    "Monitor Intrusión: el canal se pone rojo y sube arriba.",
    "Mapa: si la línea está dibujada y en su horario, titila, pita y habla.",
    "Pared: lee el estado cada pocos segundos y suena según Monitores.",
], still=2)


def speaker(x, y, c):
    return (f'<path d="M{x} {y - 7} h8 l10 -9 v32 l-10 -9 h-8 z" fill="{c}"/>'
            f'<path d="M{x + 24} {y - 6} q7 7 0 14 M{x + 30} {y - 12} q13 13 0 26" fill="none" stroke="{c}" stroke-width="2.5" stroke-linecap="round"/>')


a.add(box(48, 352, 270, 84, "Servidor", "detección nueva", "server"))
PX = 560

# ---- Monitor Intrusión
MY = 176
a.add(a.box(PX, MY, 592, 158, a.WHITE, a.LINE, rx=14))
a.add(a.text(PX + 20, MY + 30, "Monitor Intrusión", 18, a.INK, a.SANS, 600))
a.add(a.text(PX + 572, MY + 30, "socket", 15, a.BAD, a.MONO, 600, "end"))
rows = ["Perímetro Sur 07", "Acceso Principal", "Perímetro Norte 12"]
RY0, RH = MY + 46, 36
for i, name in enumerate(rows):
    y = RY0 + i * RH
    if i < 2:   # bajan un lugar cuando sube el Norte
        inner = a.box(PX + 16, 0, 560, RH - 6, a.SLATE, rx=8) + a.text(PX + 34, 21, name, 16, a.INK, a.SANS, 600)
        mv = a.move([(0, 0, y), (30, 0, y), (36, 0, y + RH), (100, 0, y + RH)])
        a.add(a.group(inner, mv, still=0))
        a.add(a.group(f'<g transform="translate(0 {y + RH})">{inner}</g>', a.keyframes([(0, 0), (100, 0)]), still=1))
    else:
        grey = a.box(PX + 16, 0, 560, RH - 6, a.SLATE, rx=8) + a.text(PX + 34, 21, name, 16, a.INK, a.SANS, 600)
        red = (a.box(PX + 16, 0, 560, RH - 6, a.BAD, rx=8) + a.text(PX + 34, 21, name, 16, a.WHITE, a.SANS, 600)
               + a.text(PX + 560, 21, "Cruce de línea", 15, a.WHITE, a.MONO, 600, "end"))
        mv = a.move([(0, 0, y), (30, 0, y), (36, 0, RY0), (100, 0, RY0)])
        a.add(a.group(f'<g>{grey}</g>', mv, a.keyframes([(0, 1), (26, 1), (27, 0), (99, 0), (100, 1)]), still=0))
        a.add(a.group(red, mv, a.keyframes([(0, 0), (26, 0), (27, 1), (99, 1), (100, 0)]), still=0))
# cuadro fijo: estado final
a.add(a.group(a.box(PX + 16, RY0, 560, RH - 6, a.BAD, rx=8) + a.text(PX + 34, RY0 + 21, rows[2], 16, a.WHITE, a.SANS, 600)
              + a.text(PX + 560, RY0 + 21, "Cruce de línea", 15, a.WHITE, a.MONO, 600, "end"), a.keyframes([(0, 0), (100, 0)]), still=1))

# ---- Mapa
MapY = 352
a.add(a.box(PX, MapY, 592, 128, a.WHITE, a.LINE, rx=14))
a.add(a.text(PX + 20, MapY + 30, "Mapa", 18, a.INK, a.SANS, 600))
a.add(a.text(PX + 572, MapY + 30, "socket", 15, a.BAD, a.MONO, 600, "end"))
a.add(f'<path d="M{PX + 24} {MapY + 92} h200" stroke="{a.LINE}" stroke-width="8" stroke-linecap="round"/>')
a.add(f'<path d="M{PX + 44} {MapY + 92} h150" stroke="{a.BLUE}" stroke-width="5" stroke-linecap="round"/>')
blink = a.keyframes([(0, 0), (52, 0), (53, 1), (56, 0), (59, 1), (62, 0), (65, 1), (68, 0), (71, 1), (75, 0), (100, 0)])
a.add(a.group(f'<path d="M{PX + 44} {MapY + 92} h150" stroke="{a.BAD}" stroke-width="7" stroke-linecap="round"/>', blink, still=1))
a.add(a.text(PX + 24, MapY + 66, "línea Perímetro Norte 12", 15, a.GREY, a.MONO))
when(a, speaker(PX + 270, MapY + 76, a.BAD) + a.text(PX + 318, MapY + 70, "pitido (otro tono si es persona)", 15, a.BAD, a.MONO, 600)
     + a.text(PX + 318, MapY + 98, "voz: “Persona en Perímetro Norte 12”", 15, a.INK, a.SANS, 600), 54, 75, still=1)
when(a, a.text(PX + 270, MapY + 84, "solo si la línea está dibujada y en su horario", 15, a.GREY, a.SANS), 0, 53, still=0)
when(a, a.text(PX + 270, MapY + 84, "solo si la línea está dibujada y en su horario", 15, a.GREY, a.SANS), 76, 100, still=0)

# ---- Pared
WY = 498
a.add(a.box(PX, WY, 592, 128, a.INK, rx=14))
a.add(a.text(PX + 20, WY + 30, "Pantalla de pared · Rotación", 18, a.WHITE, a.SANS, 600))
a.add(a.text(PX + 572, WY + 30, "consulta", 15, "#9FC3E3", a.MONO, 600, "end"))
when(a, speaker(PX + 24, WY + 78, "#FFD28A") + a.text(PX + 72, WY + 76, "suena según Monitores: sin sonido, un tono", 15, "#FFD28A", a.MONO, 600)
     + a.text(PX + 72, WY + 100, "o repetir hasta que se acepte", 15, "#FFD28A", a.MONO, 600), 86, 100, still=0)
when(a, a.text(PX + 24, WY + 76, "el audio necesita un toque en la página", 16, "#9FC3E3", a.SANS, 600)
     + a.text(PX + 24, WY + 100, "o Chrome en kiosco con autoplay", 16, "#9FC3E3", a.SANS, 600), 0, 85, still=1)

# ---- flechas: socket (empuja) y consulta (la pared pregunta)
a.add(a.arrow(f"M318 382 C440 382 440 {MY + 80} {PX - 10} {MY + 80}", a.BAD, 3))
a.add(a.arrow(f"M318 400 H{PX - 10}", a.BAD, 3))
a.add(a.arrow(f"M{PX - 10} {WY + 64} L326 424", a.GREY, 2.5, "6 6"))
a.add(a.text(400, WY + 60, "cada pocos segundos", 15, a.GREY, a.MONO, 600, "middle"))
travel(a, (318, 382), (PX - 14, MY + 80), 3, 12, dot=9, bg=a.BAD, hold=2)
travel(a, (318, 400), (PX - 14, 400), 3, 12, dot=9, bg=a.BAD, hold=2)
for t in (77, 82, 87, 92):
    travel(a, (PX - 14, WY + 62), (334, 427), t, t + 3, dot=7, bg=a.GREY, hold=0.4)
when(a, a.pill(48, 460, "socket: llega al instante", a.BAD, a.BADBG, 15, 30), 3, 100, still=1)
when(a, a.pill(48, 500, "pared: pregunta", a.GREY, a.SLATE, 15, 30), 76, 100, still=0)

out(a, 5, 1, "Una detección, tres pantallas",
    "Animación en cuatro tiempos. A la izquierda, el servidor con una detección nueva; a la derecha, tres pantallas: Monitor Intrusión, Mapa y Pantalla de pared o Rotación. "
    "Tiempo 1: el servidor emite la detección por socket y llega al instante al Monitor y al Mapa. "
    "Tiempo 2: en el Monitor Intrusión el canal Perímetro Norte 12 se pone rojo con Cruce de línea y sube al primer lugar de la lista. "
    "Tiempo 3: en el Mapa la línea dibujada titila, suena un pitido (con otro tono si es persona) y una voz dice Persona en Perímetro Norte 12; solo pasa si la línea está dibujada y en su horario. "
    "Tiempo 4: la pantalla de pared no recibe el socket: pregunta el estado cada pocos segundos y suena según el ajuste de Monitores (sin sonido, un tono o repetir hasta que se acepte). "
    "El audio del navegador necesita un toque en la página o Chrome en kiosco con autoplay.",
    [8, 40, 62, 94])
