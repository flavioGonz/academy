#!/usr/bin/env python3
"""Lección 19 · teoría: el primer bloque del firmware es el código del modelo; la planilla se completa desde la web."""
from _anim_akuvox_15_28 import *

a = new(24, "AKUVOX · LECCIÓN 19", "El firmware dice qué modelo tenés enfrente")
a.steps([
    "En la web del equipo, el firmware empieza con el código del modelo: 29 es R29.",
    "915 es X915. El primer bloque alcanza para ubicarlo en la planilla.",
    "320 es el R20 en su versión 5.",
    "La planilla se completa mirando la web del equipo, no solo la etiqueta.",
], still=3)

# web del equipo
a.add(a.box(48, 190, 520, 236, a.WHITE, a.LINE, rx=16))
a.add(f'<path d="M48 204a14 14 0 0 1 14 -14h492a14 14 0 0 1 14 14v26h-520z" fill="{I.SOFT}"/>')
for i in range(3):
    a.add(f'<circle cx="{68 + i * 18}" cy="210" r="5" fill="{I.LINE2}"/>')
a.add(a.text(124, 216, "Web del equipo", 15, a.TXT, a.SANS, 600))
a.add(a.text(72, 262, "Firmware", 16, a.TXT, a.SANS, 600))

FW = [("29", ".x.y.z", "R29", "R"), ("915", ".x.y.z", "X915", "X"), ("320", ".x.y.z", "R20 v5", "R")]
SPANS = [(0, 25), (25, 50), (50, 75)]
for (blk, rest, mod, ser), (t0, t1) in zip(FW, SPANS):
    k = 38 * 0.6
    w = len(blk) * k
    g = (f'<rect x="66" y="278" width="{w + 12:.0f}" height="54" rx="8" fill="{a.AMBBG}" stroke="{a.AMB}" stroke-width="2"/>'
         + a.text(72, 318, blk, 38, a.AMB, a.MONO, 600) + a.text(round(72 + w, 1), 318, rest, 38, a.INK, a.MONO, 500)
         + a.arrow(f"M{72 + w / 2:.0f} 340 V372", a.AMB, 2.5)
         + a.text(72, 404, "código del modelo →", 17, a.AMB, a.SANS, 600)
         + a.pill(250, 382, mod, a.WHITE, a.BLUE, 17, h=32))
    a.add(at(a, g, t0 + 1, t1, still=0))
# cuadro fijo: los tres a la vez, chicos
fix = ""
for i, (blk, rest, mod, ser) in enumerate(FW):
    y = 300 + i * 40
    fix += a.text(72, y, blk, 24, a.AMB, a.MONO, 600) + a.text(72 + len(blk) * 14.4, y, rest, 24, a.INK, a.MONO, 500) + a.text(260, y, "→ " + mod, 20, a.BLUE, a.SANS, 600)
a.add(at(a, fix, 75, 100, still=1))

# planilla
TX, TY, TW = 620, 190, 532
cols = [("FIRMWARE", 0), ("BLOQUE", 160), ("MODELO", 280), ("SERIE", 420)]
a.add(a.box(TX, TY, TW, 236, a.WHITE, a.LINE, rx=14))
a.add(f'<path d="M{TX} {TY + 14}a14 14 0 0 1 14 -14h{TW - 28}a14 14 0 0 1 14 14v34h-{TW}z" fill="{I.SOFT}"/>')
a.add(a.text(TX + 18, TY - 14, "Planilla del catálogo", 16, a.TXT, a.SANS, 600))
for name, dx in cols:
    a.add(a.text(TX + 18 + dx, TY + 31, name, 15, a.GREY, a.MONO, 600))
for i, ((blk, rest, mod, ser), (t0, t1)) in enumerate(zip(FW, SPANS)):
    y = TY + 92 + i * 56
    if i:
        a.add(f'<path d="M{TX + 12} {y - 34}H{TX + TW - 12}" stroke="{a.LINE}"/>')
    row = (a.text(TX + 18, y, blk + rest, 17, a.INK, a.MONO, 500) + a.text(TX + 178, y, blk, 17, a.AMB, a.MONO, 600)
           + a.text(TX + 298, y, mod, 17, a.INK, a.SANS, 600) + a.text(TX + 438, y, ser, 17, a.TXT, a.MONO, 500))
    a.add(at(a, row, t0 + 12, 100, still=1))
    a.add(at(a, a.box(TX + 6, y - 30, TW - 12, 44, "none", a.CYAN, rx=8, sw=2), t0 + 12, t1, still=0))

# abajo: etiqueta contra web
a.add(a.box(48, 470, 1104, 150, a.WHITE, a.LINE, rx=16))
a.add(a.box(72, 494, 200, 102, a.SLATE, I.LINE2, rx=10, sw=1.5, extra='stroke-dasharray="6 5"'))
a.add(a.text(172, 530, "ETIQUETA", 15, a.GREY, a.MONO, 600, "middle"))
a.add(a.text(172, 562, "nombre comercial", 15, a.TXT, a.SANS, 500, "middle"))
a.add(a.text(300, 530, "La etiqueta da el nombre comercial.", 18, a.INK, a.SANS, 600))
a.add(a.text(300, 562, "El primer bloque del firmware, leído en la web del equipo, da el modelo.", 17, a.TXT, a.SANS, 500))
a.add(at(a, a.text(300, 594, "Con ese dato se completan alimentación, relé y 12 V desde las tablas de la Knowledge Base.", 17, a.BLUE, a.SANS, 600), 75, 100, still=1))

a.write(*out(19)[:1], title="El primer bloque del firmware identifica el modelo",
        desc=("Animación en cuatro tiempos. A la izquierda, la web del equipo muestra el firmware; a la derecha, la planilla del catálogo. "
              "1: el firmware 29.x.y.z empieza con 29, el código del R29, y la fila se completa: bloque 29, modelo R29, serie R. "
              "2: 915.x.y.z es el X915, serie X. 3: 320.x.y.z es el R20 versión 5, serie R. "
              "4: la planilla queda completa: la etiqueta da el nombre comercial y el primer bloque del firmware, leído en la web del equipo, da el modelo; "
              "con ese dato se completan alimentación, relé y 12 V desde las tablas de la Knowledge Base."),
        preview=[14, 40, 66, 92], prefix=out(19)[1])
