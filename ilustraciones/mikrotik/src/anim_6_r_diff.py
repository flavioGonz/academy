#!/usr/bin/env python3
"""Lección 6 · Resumen, "Cómo se ve en la red": export y backup antes, el cambio, export después,
los .rsc bajan a la notebook y diff muestra qué cambió; el .backup vuelve atrás el mismo equipo."""
from _anim_red_1_9 import *

a = Anim(T=26, kicker="MIKROTIK · BACKUP PRIMERO · CÓMO SE VE EN LA RED", title="Antes, después y un diff: la intervención queda escrita")
a.steps([
    "Antes de tocar: export en texto y backup en binario, con contraseña.",
    "Hacés el cambio y sacás la foto de después.",
    "Los .rsc bajan a la notebook: diff marca con > lo que cambió.",
    "Para volver atrás en este mismo equipo, el .backup lo deja como estaba.",
], still=2)

# ---------- router y sus archivos
RX, RY, RW, RH = 48, 186, 430, 272
a.add(a.box(RX, RY, RW, RH, a.INK, rx=18))
a.add(glyph(a, "server", RX + 20, RY + 18, a.CYAN))
a.add(a.text(RX + 64, RY + 36, "Router del cliente", 20, a.WHITE, a.HEAD, 600))
a.add(a.text(RX + 64, RY + 60, "identity:", 15, SKY, a.MONO))
for t0, t1, name, col, st in ((0, 30, "MikroTik", a.WHITE, 0), (30, 88, "LAB-MT01", GOLD, 1), (88, 100, "MikroTik", MINT, 0)):
    a.add(during(a, a.text(RX + 160, RY + 60, name, 15, col, a.MONO, 600), t0, t1, still=st))
a.add(a.text(RX + 20, RY + 98, "FILES", 13, SKY, a.MONO, 400, extra='letter-spacing="1.8"'))
FILES = [("antes.rsc", "texto · se lee", 6), ("antes.backup", "binario · con contraseña", 12), ("despues.rsc", "texto · se lee", 34)]
for i, (n, k, t0) in enumerate(FILES):
    y = RY + 110 + i * 48
    a.add(during(a, a.box(RX + 16, y, RW - 32, 40, a.NAVY2, rx=8)
                 + a.text(RX + 32, y + 26, n, 15, a.WHITE, a.MONO, 600)
                 + a.text(RX + RW - 32, y + 26, k, 15, SKY, a.MONO, 400, "end"), t0, 100, still=1))
a.add(during(a, a.box(RX + 16, RY + 158, RW - 32, 40, "none", GOLD, rx=8, sw=2.5), 78, 100))

# ---------- cable y notebook
CY = 318
a.add(line(RX + RW, CY, 700, CY, a.BLUE, 4))
a.add(a.text(589, CY - 16, "WinBox · Files", 15, a.GREY, a.MONO, 400, "middle"))
NX, NW = 700, 452
a.add(a.box(NX, RY, NW, RH, a.WHITE, a.LINE, rx=18))
a.add(glyph(a, "laptop", NX + 20, RY + 18, a.BLUE))
a.add(a.text(NX + 64, RY + 36, "Notebook · legajo del cliente", 20, a.INK, a.HEAD, 600))
a.add(during(a, a.text(NX + 64, RY + 60, "antes.rsc  despues.rsc", 15, a.GREY, a.MONO), 58, 100, still=1))
for t0, n in ((52, "antes.rsc"), (55, "despues.rsc")):
    a.add(travel(a, pkt(a, n, a.CYAN, size=15), [(RX + RW + 70, CY + 30), (NX - 70, CY + 30)], t0, t0 + 3.5, hold=0.6))
# diff
D = [("$ diff antes.rsc despues.rsc", a.INK, ""),
     ("< # <fecha 10:02> by RouterOS 7.x", a.AMB, "fecha"),
     ("> # <fecha 10:31> by RouterOS 7.x", a.AMB, "fecha"),
     ("> /system identity", a.OK, "tu cambio"),
     ("> set name=LAB-MT01", a.OK, "tu cambio")]
for i, (ln, col, tag) in enumerate(D):
    y = RY + 80 + i * 32
    on = 59 + i * 1.6
    bg = {a.AMB: a.AMBBG, a.OK: a.OKBG}.get(col, a.SLATE)
    a.add(during(a, a.box(NX + 16, y, NW - 32, 30, bg, rx=6) + a.text(NX + 28, y + 21, ln, 15, col, a.MONO, 600), on, 100, still=1))
a.add(during(a, a.text(NX + 24, RY + 258, "La línea de fecha cambia siempre: no cuenta.", 15, a.AMB, a.SANS, 600), 64, 100, still=1))
# paso 4: el backup vuelve al router
a.add(during(a, a.arrow(f"M{RX + RW - 30} {RY + 200} C {RX + RW + 40} {RY + 230}, {RX + RW + 40} {RY + 60}, {RX + RW - 6} {RY + 54}", GOLD, 3), 80, 100))

# ---------- terminal (cambia con el paso)
TY = 480
a.add(a.box(48, TY, 1104, 146, a.INK, rx=14))
a.add(a.text(66, TY + 30, "TERMINAL", 13, SKY, a.MONO, 400, extra='letter-spacing="1.8"'))
T = [
    (0, 25, ["/export file=antes", '/system/backup/save name=antes password="Backup-Lab-Ejemplo-1"'], 0),
    (25, 50, ["/system/identity/set name=LAB-MT01", "/export file=despues"], 0),
    (50, 75, ["# en la notebook", "diff antes.rsc despues.rsc      (en Windows: fc antes.rsc despues.rsc)"], 1),
    (75, 100, ['/system/backup/load name=antes.backup password="Backup-Lab-Ejemplo-1"', "# pide confirmar, reinicia y el equipo queda como al guardar"], 0),
]
for t0, t1, ls, st in T:
    body = "".join(a.text(66, TY + 66 + j * 30, ln, 16, a.WHITE if not ln.startswith("#") else SKY, a.MONO) for j, ln in enumerate(ls))
    a.add(during(a, body, t0, t1, still=st))
a.add(during(a, a.text(66, TY + 128, "En otro modelo, el .backup puede no encajar: para migrar, export e import revisado.", 15, GOLD, a.SANS, 600), 80, 100))

write(a, 6, "r1", "Export, backup y diff en una intervención",
      "Animación en cuatro tiempos con el router del cliente (sus archivos en Files) y la notebook del técnico. "
      "1: antes de tocar, /export file=antes deja antes.rsc, de texto, y /system/backup/save name=antes con contraseña deja antes.backup, binario. "
      "2: el cambio, /system/identity/set name=LAB-MT01, y la foto de después con /export file=despues, que deja despues.rsc. "
      "3: los dos .rsc bajan a la notebook por WinBox, Files; diff antes.rsc despues.rsc muestra la línea de fecha que siempre cambia, marcada con < y >, "
      "y el cambio real marcado con >: /system identity y set name=LAB-MT01. "
      "4: para volver atrás en el mismo equipo, /system/backup/load name=antes.backup con su contraseña pide confirmar, reinicia y el identity vuelve a MikroTik. "
      "En otro modelo el .backup puede no encajar: para migrar se usa el export con un import revisado.",
      [10, 38, 62, 70, 90])
