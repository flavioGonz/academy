#!/usr/bin/env python3
"""Lección 20 · teoría: el switch (PSE) detecta y clasifica al PD antes de dar energía; un puerto af no alcanza para un portero que pide at."""
from _anim_akuvox_15_28 import *

a = new(24, "AKUVOX", "PoE: primero detecta, después clasifica, recién ahí da energía")
a.steps([
    "El switch (PSE) primero detecta si del otro lado hay un equipo PoE (PD).",
    "Lee la clase de potencia que pide el portero. Recién ahí entrega energía.",
    "Puerto 802.3at (PoE+): hasta 25,5 W en el equipo. El S539 arranca y anda.",
    "Puerto solo af: unos 12,95 W. Al subir el consumo, puede no arrancar o reiniciarse.",
], still=3)

# switch
a.add(a.box(48, 196, 300, 168, a.INK, rx=20))
a.add(a.text(70, 234, "Switch PoE", 21, a.WHITE, a.HEAD, 600))
a.add(a.text(70, 258, "PSE · entrega energía", 15, "#9FC3E3", a.MONO))
a.add(a.box(240, 286, 84, 56, a.CYAN, rx=8))
a.add(at(a, a.text(70, 320, "puerto 802.3at", 16, "#7FE0FF", a.MONO, 600), 0, 75, still=0))
a.add(at(a, a.text(70, 320, "puerto solo af", 16, "#FFD28A", a.MONO, 600), 75, 100, still=1))

# portero
a.add(I.Intercom(930, 176, "S539", "PD · pide 802.3at", screen=True).svg())
a.add(at(a, f'<rect x="952" y="238" width="106" height="92" rx="8" fill="{a.CYAN}" opacity=".85"/>'
         + a.text(1005, 290, "anda", 17, a.WHITE, a.SANS, 600, "middle"), 53, 90, still=0))
a.add(at(a, a.text(1005, 290, "se reinicia", 15, "#FFB4A6", a.MONO, 600, "middle"), 90, 100, still=1))

# cable
a.add(f'<path d="M324 314 H930" stroke="{a.BLUE}" stroke-width="5"/>')
flow = a.keyframes([(0, 0), (100, -240)], "stroke-dashoffset")
a.add(a.group(f'<path d="M324 314 H930" stroke="{a.BAD}" stroke-width="5" stroke-dasharray="14 10"/>', flow, a.show(50, 92), still=0))
a.add(a.text(627, 346, "un solo cable: datos y energía", 15, a.GREY, a.SANS, 500, "middle"))

# negociación
a.add(msg(a, 360, 918, 222, "detección: ¿hay un PD?", 3, 50, still=0))
a.add(msg(a, 918, 360, 272, "firma de PD", 12, 50, color=a.OK, still=0))
a.add(at(a, a.box(470, 196, 320, 90, a.BG, rx=10), 25, 50, still=0))
a.add(msg(a, 360, 918, 222, "¿qué clase de potencia?", 28, 50, still=0))
a.add(msg(a, 918, 360, 272, "clase: PoE+ (802.3at)", 36, 75, color=a.OK, still=0))
a.add(at(a, a.pill(627, 382, "recién ahora: energía", a.BAD, a.BADBG, 15, anchor="middle"), 44, 56, still=0))

# barra de potencia (W en el equipo)
X0, PX = 110, 990 / 30
BY = 540
a.add(a.text(48, BY - 22, "Potencia disponible en el equipo", 17, a.INK, a.SANS, 600))
a.add(a.box(X0, BY, 990, 34, a.SLATE, rx=8))
xaf, xat = X0 + 12.95 * PX, X0 + 25.5 * PX
a.add(at(a, a.box(X0, BY, 25.5 * PX, 34, a.OKBG, a.OK, rx=8, sw=1.5), 50, 75, still=0))
a.add(at(a, a.box(X0, BY, 12.95 * PX, 34, a.AMBBG, a.AMB, rx=8, sw=1.5), 75, 100, still=1))
for x, lab in ((xaf, "802.3af · 12,95 W"), (xat, "802.3at · 25,5 W")):
    a.add(f'<path d="M{x:.0f} {BY - 8} V{BY + 78}" stroke="{a.INK}" stroke-width="2" stroke-dasharray="4 4"/>')
    a.add(a.text(round(x - 8), BY + 26, lab, 15, a.INK, a.MONO, 600, "end"))
a.add(a.text(X0 - 10, BY + 24, "0 W", 15, a.GREY, a.MONO, 400, "end"))
# consumo
CY = BY + 50
a.add(a.text(X0 + 4, CY + 50, "consumo al subir: pantalla, cámara, lectores (esquema, sin valores)", 15, a.GREY, a.SANS, 500))
grow_ok = a.keyframes([(0, 0), (54, 0), (64, 1), (100, 1)], "transform", "scaleX({})")
a.add(at(a, a.group(a.box(X0, CY, 18 * PX, 26, a.BLUE, rx=6), grow_ok, still=1, origin=f"{X0}px {CY}px")
         + "", 50, 75, still=0))
grow_bad = a.keyframes([(0, 0), (77, 0), (88, 1), (100, 1)], "transform", "scaleX({})")
a.add(at(a, a.group(a.box(X0, CY, 18 * PX, 26, a.BAD, rx=6), grow_bad, still=1, origin=f"{X0}px {CY}px"), 75, 100, still=1))
a.add(at(a, mark(X0 + 18 * PX + 30, CY + 13, True), 64, 75, still=0))
a.add(at(a, mark(X0 + 18 * PX + 30, CY + 13, False), 88, 100, still=1))

a.write(*out(20)[:1], title="Negociación PoE entre switch y portero",
        desc=("Animación en cuatro tiempos entre un switch PoE (PSE) y un portero S539 (PD) unidos por un solo cable. "
              "1: el switch detecta si del otro lado hay un equipo PoE y el portero responde con su firma de PD. "
              "2: el switch pregunta la clase de potencia, el portero pide PoE+ (802.3at) y recién entonces el switch entrega energía. "
              "3: con un puerto 802.3at hay hasta 25,5 W disponibles en el equipo; el consumo del portero entra y el S539 arranca y anda. "
              "4: con un puerto solo af hay unos 12,95 W; cuando sube el consumo (pantalla, cámara, lectores) pasa el límite y el portero no arranca o se reinicia. "
              "La barra de consumo es un esquema, sin valores."),
        preview=[8, 40, 66, 95], prefix=out(20)[1])
