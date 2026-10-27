#!/usr/bin/env python3
"""Lección 32 · Teoría · PoE: el switch pregunta antes de dar energía.
Sale de teoria_md (Cómo funciona): detección por resistencia de firma, lectura de la clase, recién
entonces unos 48 V; en un puerto 802.3af el X937 puede no encender o quedar inestable; presupuesto total.
Historia: 802.3af hasta 15,4 W y 802.3at (PoE+) hasta 30 W por puerto."""
from _anim_akuvox_29_42 import new, out, box, travel, when
import ilus

a = new(24, "MONITORES SERIE X · POE", "PoE: el switch pregunta antes de dar energía")
a.steps([
    "Detección: el switch mide la resistencia de firma en el par.",
    "Clase: el equipo indica cuánta potencia va a pedir.",
    "Recién entonces aplica unos 48 V: el X937 enciende.",
    "En un puerto 802.3af no alcanza: puede no encender o quedar inestable.",
], still=2)

RED = "#D2492F"
# switch
a.add(a.box(48, 196, 330, 170, a.INK, rx=18))
a.add(a.text(72, 232, "Switch PoE", 21, a.WHITE, a.HEAD, 600))
a.add(a.text(72, 256, "puerto del X937", 15, "#9FC3E3", a.MONO))
a.add(a.box(250, 270, 100, 64, a.NAVY2, a.CYAN, rx=10))
a.add(a.text(300, 308, "puerto", 15, a.WHITE, a.MONO, 600, "middle"))
when(a, a.pill(72, 290, "802.3at", a.WHITE, a.BLUE, 15, 30) + a.text(72, 346, "PoE+ · hasta 30 W", 15, "#9FC3E3", a.MONO, 600), 0, 75, still=1)
when(a, a.pill(72, 290, "802.3af", a.INK, "#FFD28A", 15, 30) + a.text(72, 346, "hasta 15,4 W", 15, "#FFD28A", a.MONO, 600), 75.5, 100)

# cable
CY = 302
a.add(f'<path d="M350 {CY} H860" stroke="{a.BLUE}" stroke-width="5"/>')
a.add(a.text(605, CY + 36, "un UTP: datos y energía", 15, a.GREY, a.MONO, 600, "middle"))
# energía (rayas que corren) desde t3
dash = a.keyframes([(0, 0), (100, -600)], "stroke-dashoffset")
a.add(a.group(f'<path d="M350 {CY - 12} H860" stroke="{RED}" stroke-width="4" stroke-dasharray="14 10"/>'
              + a.pill(560, CY - 52, "≈ 48 V", RED, a.BADBG, 15, 28), a.show(52, 100), dash, still=1))

# monitor X937
mon = ilus.Monitor(860, 210, "X937", "15,6\" · Android 14")
a.add(mon.svg())
screen_on = f'<rect x="876" y="226" width="208" height="112" rx="8" fill="#1F6FB8"/><rect x="896" y="246" width="90" height="12" rx="6" fill="#9FC3E3"/><rect x="896" y="268" width="150" height="10" rx="5" fill="#5D9CD3"/><rect x="896" y="288" width="120" height="10" rx="5" fill="#5D9CD3"/>'
a.add(a.group(screen_on, a.keyframes([(0, 0), (54, 0), (55, 1), (75, 1), (76, 0), (80, 0), (80.5, 1), (83, 1), (83.5, 0), (86, 0), (86.5, 1), (88, 1), (88.5, 0), (93, 0), (93.5, 1), (95, 1), (95.5, 0), (100, 0)]), still=1))

# t1: sonda de firma
travel(a, (420, CY), (820, CY), 3, 11, "¿firma PoE?", a.INK, "#E6EDF4", hold=1.5)
travel(a, (820, CY), (420, CY), 14, 21, "firma OK", a.OK, a.OKBG, hold=3)
# t2: clase
travel(a, (820, CY), (420, CY), 29, 40, "clase: cuánto va a pedir", a.WHITE, a.BLUE, hold=6)
when(a, a.pill(72, 140 + 236, "sabe cuánto pide", a.OK, a.OKBG, 15, 28), 42, 75, still=1)
# t4: aviso
when(a, a.pill(870, 434, "inestable o no enciende", a.BAD, a.BADBG, 15, 30), 77, 100)
when(a, a.pill(870, 434, "encendido", a.OK, a.OKBG, 15, 30), 55, 75, still=1)

a.add(a.box(48, 470, 1104, 150, a.WHITE, a.LINE, rx=16))
a.add(a.text(72, 506, "Qué pide cada uno (tabla de alimentación de Akuvox)", 18, a.INK, a.SANS, 600))
a.add(a.text(72, 536, "X937: PoE+ 802.3at o fuente de 12 V 2 A.   X933: PoE o fuente de 12 V 1 A.", 17, a.TXT, a.SANS, 600))
a.add(a.text(72, 570, "Y el presupuesto total: 8 puertos PoE+ no siempre dan 30 W en todos a la vez.", 17, a.TXT, a.SANS, 600))
a.add(a.text(72, 598, "Sumá los consumos y comparalos con la potencia total en la ficha del switch.", 17, a.TXT, a.SANS, 600))

out(a, 32, 1, "PoE: el switch pregunta antes de dar energía",
    "Animación de un switch PoE conectado por un UTP a un monitor X937. "
    "Tiempo 1: el switch manda una prueba por el par y mide la resistencia de firma; la firma vuelve bien. "
    "Tiempo 2: el monitor indica su clase, es decir cuánta potencia va a pedir. "
    "Tiempo 3: recién entonces el switch aplica unos 48 V y el X937 enciende. "
    "Tiempo 4: el puerto pasa a ser 802.3af, hasta 15,4 W; el X937, que pide PoE+ 802.3at, parpadea y queda inestable o no enciende. "
    "Abajo: el X937 pide PoE+ 802.3at o fuente de 12 V 2 A, el X933 PoE o fuente de 12 V 1 A, y hay que sumar consumos contra la potencia total del switch.",
    [8, 17, 36, 62, 87])
