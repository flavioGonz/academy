#!/usr/bin/env python3
"""Lección 3 · Laboratorio, paso 2: lvs en un LVM-thin. El disco de una VM mide lo asignado (LSize) pero ocupa lo
escrito (Data%); el pool data reserva bloques recién cuando la VM escribe. La suma de lo asignado puede pasar el
tamaño del pool (sobreasignación) y, si todas las VM escriben, el pool llega al 100 %.
Fuentes: guía de administración (LVM-thin, thin pool data / local-lvm), tarjeta de la lección (lvs, sobreasignar)."""
from _anim_pmx_red import *

a = new(24, "Disco con criterio", "lvs: lo asignado y lo escrito", lab=True)
a.steps([
    "El disco de la VM 100 mide 32 GB, pero tiene 3 GB escritos.",
    "La VM escribe 5 GB: recién ahí el pool reserva esos bloques.",
    "Un disco nuevo de 120 GB: lo asignado ya pasa el tamaño del pool.",
    "Si todas escriben, el pool llega al 100 % y no queda dónde escribir.",
], still=1)

K = 2.2  # px por GB
PX, PY = 48, 214
# pool
a.add(a.text(PX, PY - 14, "thin pool data (local-lvm) · 200 GB", 16, a.INK, a.SANS, 600))
a.add(a.box(PX, PY, 200 * K, 34, "#E6EDF4", a.LINE, rx=8))
fills = [(0, 25, 23), (25, 75, 28), (75, 100, 200)]
for t0, t1, gb in fills:
    col = a.BAD if gb >= 200 else a.BLUE
    a.add(during(a, a.box(PX, PY, gb * K, 34, col, rx=8), t0, t1, still=1 if t0 == 25 else 0))
for t0, t1, txt, col, st in [(0, 25, "11,5 % usado", a.BLUE, 0), (25, 75, "14 % usado", a.BLUE, 1), (75, 100, "100 % · lleno", a.BAD, 0)]:
    a.add(during(a, a.text(PX + 200 * K + 14, PY + 24, txt, 16, col, a.MONO, 600), t0, t1, still=st))

# discos (ancho = LSize, relleno = escrito)
DY = [348, 414, 480]
disks = [("vm-100-disk-0", 32, [(0, 25, 3), (25, 75, 8), (75, 100, 32)], 0),
         ("vm-101-disk-0", 100, [(0, 75, 20), (75, 100, 100)], 0),
         ("vm-102-disk-0", 120, [(50, 75, 0), (75, 100, 68)], 50)]
for (name, size, ws, t_in), y in zip(disks, DY):
    body = a.text(PX, y - 10, f"{name} · {size} GB asignados", 15, a.TXT, a.MONO, 600)
    body += a.box(PX, y, size * K, 30, a.WHITE, a.GREY, rx=6, sw=2, extra='stroke-dasharray="6 4"')
    a.add(during(a, body, t_in, 100, still=1 if t_in == 0 else 0))
    for t0, t1, gb in ws:
        if gb:
            a.add(during(a, a.box(PX, y, gb * K, 30, a.BAD if t0 >= 75 else a.CYAN, rx=6), t0, t1, still=1 if (t0 <= 25 < t1) else 0))
# VM 100 escribe: bloques que bajan al disco y al pool
for i in range(5):
    a.add(travel(a, a.box(-4, -6, 8, 12, a.CYAN, rx=2), [(PX + (3 + i) * K + 4, DY[0] - 34), (PX + (3 + i) * K + 4, DY[0] + 15)], 29 + i * 1.6, 31 + i * 1.6, hold=0.5))
at(a, chip(a, PX + 32 * K + 16, DY[0] + 1, "+5 GB escritos", "info"), 30, 50)
# sobreasignación
SUM = (32 + 100 + 120) * K
asg = ""
x = PX
for gb, col in ((32, a.CYAN), (100, a.BLUE), (120, a.AMB)):
    asg += a.box(x, PY + 46, gb * K - 2, 16, col, rx=4)
    x += gb * K
asg += line(PX + 200 * K, PY - 6, PX + 200 * K, PY + 70, a.BAD, 2.5, "5 4")
asg += a.text(PX, PY + 86, "asignado: 252 GB, más que el pool", 15, a.AMB, a.MONO, 600)
a.add(during(a, asg, 50, 100))
a.add(during(a, note(a, PX, 524, 560, 70, "Asignado 252 GB en un pool de 200 GB", ["Anda mientras lo escrito no pase lo que hay."], "amb"), 50, 75))
a.add(during(a, note(a, PX, 524, 560, 70, "Pool lleno: las VM ya no pueden escribir", ["Se vigila el Data% del pool, no solo el de cada disco."], "bad"), 75, 100))
a.add(during(a, note(a, PX, 524, 560, 70, "Thin: ocupa lo que se escribe", ["Un bloque se reserva cuando la VM lo escribe."], "info"), 0, 50, still=1))

# terminal lvs
TX, TY, TW, TH = 690, 178, 462, 300
a.add(a.box(TX, TY, TW, TH, a.INK, rx=14))
a.add(tline(a, TX + 20, TY + 32, "# lvs", MINT))
a.add(tline(a, TX + 20, TY + 58, "(las columnas que importan)", SKY))
a.add(tline(a, TX + 20, TY + 96, "LV             LSize   Data%", SKY))
R = [TY + 128 + i * 32 for i in range(4)]
rows = [
    ("data           200.00g ", [(0, 25, "11.50", None), (25, 75, "14.00", None), (75, 100, "100.00", CORAL)], 0),
    ("vm-100-disk-0   32.00g ", [(0, 25, " 9.38", None), (25, 75, "25.00", MINT), (75, 100, "100.00", CORAL)], 0),
    ("vm-101-disk-0  100.00g ", [(0, 75, "20.00", None), (75, 100, "100.00", CORAL)], 0),
    ("vm-102-disk-0  120.00g ", [(50, 75, " 0.00", GOLD), (75, 100, "56.67", CORAL)], 50),
]
for (lab, vals, t_in), y in zip(rows, R):
    a.add(during(a, tline(a, TX + 20, y, lab), t_in, 100, still=1 if t_in == 0 else 0))
    for t0, t1, v, col in vals:
        a.add(during(a, tline(a, TX + 20 + 23 * 9.0, y, v, col or a.WHITE), t0, t1, still=1 if (t0 <= 25 < t1) else 0))
at(a, tline(a, TX + 20, TY + 272, "Data% del pool: la cuenta que manda", GOLD), 75, 100)
at(a, tline(a, TX + 20, TY + 272, "LSize mide lo asignado, Data% lo escrito", SKY), 0, 75, still=1)

status(a, 640, [
    (0, 25, "Un disco de 32 GB con 3 GB escritos ocupa 3 GB del pool.", a.INK, 0),
    (25, 50, "Data% sube en el disco y en el pool a medida que la VM escribe.", a.BLUE, 1),
    (50, 75, "Sobreasignar está permitido: es una apuesta a que no se llenen todos juntos.", a.AMB, 0),
    (75, 100, "Con el pool en 100 %, ninguna VM de ese pool puede escribir más.", a.BAD, 0),
])

write(a, 3, "l1", "lvs: lo asignado y lo escrito",
      "Animación en cuatro tiempos con el thin pool data de 200 GB (local-lvm), los discos de tres VM dibujados con su tamaño asignado y lo escrito, y la salida de lvs con las columnas LV, LSize y Data%. "
      "1: vm-100-disk-0 mide 32 GB pero tiene 3 GB escritos, Data% 9.38; con vm-101-disk-0 de 100 GB al 20 %, el pool está en 11.50 %. "
      "2: la VM 100 escribe 5 GB; recién ahí el pool reserva esos bloques: el disco pasa a 25.00 % y el pool a 14.00 %. "
      "3: se suma vm-102-disk-0 de 120 GB, vacío; lo asignado suma 252 GB en un pool de 200 GB: está sobreasignado y anda mientras lo escrito no pase lo que hay. "
      "4: si todas las VM escriben, el pool llega al 100 % y ninguna VM de ese pool puede escribir más; por eso se vigila el Data% del pool, no solo el de cada disco.",
      [8, 34, 46, 62, 90])
