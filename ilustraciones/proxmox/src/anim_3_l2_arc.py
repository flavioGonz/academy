#!/usr/bin/env python3
"""Lección 3 · Laboratorio, paso 3: el ARC de ZFS y su límite. La primera lectura va al disco y queda en el ARC; la
segunda sale de la RAM; el ARC crece con lo leído hasta zfs_arc_max, que se lee en bytes en
/sys/module/zfs/parameters/zfs_arc_max y se fija en /etc/modprobe.d/zfs.conf. Regla oficial: 2 GiB + 1 GiB por TiB.
Fuentes: guía de administración (ZFS, ARC, límite del instalador y regla de tamaño), tarjeta de la lección."""
from _anim_pmx_red import *

a = new(24, "Disco con criterio", "El ARC: la caché de ZFS en la RAM del host", lab=True)
a.steps([
    "Primera lectura: el dato no está en el ARC y ZFS va al disco.",
    "Segunda lectura: sale de la RAM; el disco ni se entera.",
    "Con cada dato nuevo el ARC crece, hasta el tope zfs_arc_max.",
    "El tope se lee y se fija en bytes: 6 GiB para un pool de 4 TiB.",
], still=2)

# VM y disco
a.add(dev(a, 48, 182, 250, 76, "VM 100", "lee la base de datos", icon="server", tsize=18))
a.add(dev(a, 48, 500, 250, 80, "Pool ZFS · 4 TiB", "discos: lento", icon="server", tsize=18))
# RAM del host
RX, RY, RW = 340, 300, 560
K = RW / 64
a.add(a.text(RX, RY - 12, "RAM del host · 64 GiB", 16, a.INK, a.SANS, 600))
a.add(a.box(RX, RY, RW, 56, "#E6EDF4", a.LINE, rx=10))
a.add(a.box(RX, RY, 16 * K, 56, a.NAVY2, rx=10) + a.text(RX + 8 * K, RY + 34, "VM 100 · 16", 15, a.WHITE, a.MONO, 600, "middle"))
a.add(a.box(RX + 16 * K + 2, RY, 24 * K, 56, a.NAVY2, rx=10) + a.text(RX + 28 * K, RY + 34, "VM 101 · 24", 15, a.WHITE, a.MONO, 600, "middle"))
AX = RX + 40 * K + 4
for t0, t1, gib, st in [(0, 12, 0.3, 0), (12, 50, 1.2, 0), (50, 62, 3.5, 0), (62, 100, 6, 1)]:
    lab = "ARC" if gib >= 3 else ""
    a.add(during(a, a.box(AX, RY, gib * K, 56, a.CYAN, rx=10) + (a.text(AX + gib * K / 2, RY + 34, lab, 15, a.WHITE, a.MONO, 700, "middle") if lab else ""), t0, t1, still=st))
CAP = AX + 6 * K
a.add(line(CAP, RY - 8, CAP, RY + 70, a.AMB, 3, "6 4"))
a.add(a.text(CAP + 8, RY + 86, "zfs_arc_max", 15, a.AMB, a.MONO, 700))
at(a, a.text(RX + RW - 12, RY + 34, "libre", 15, a.GREY, a.MONO, 400, "end"), 0, 100, still=1)
at(a, chip(a, CAP + 8, RY - 46, "tope: 6 GiB", "amb"), 50, 100, still=1)

# caminos
VM = (173, 258)
ARC = (AX + 8, RY)
DISK = (173, 500)
a.add(path(f"M{VM[0]} {VM[1]} V262 H{AX + 8} V{RY}", a.LINE, 2.5))
a.add(path(f"M{AX + 8} {RY + 56} V440 H{DISK[0]} V{DISK[1]}", a.LINE, 2.5))
# 1 · miss: VM → ARC → disco → ARC → VM
go(a, "leer", [VM, (VM[0], 262), (AX + 8, 262), ARC], 2, 5, a.BLUE, hold=0.2)
at(a, chip(a, AX + 46, 214, "no está", "bad"), 5, 12)
go(a, "leer", [(AX + 8, RY + 56), (AX + 8, 440), (DISK[0], 440), DISK], 6, 10, a.BLUE, hold=0.2)
go(a, "dato", [DISK, (DISK[0], 440), (AX + 8, 440), (AX + 8, RY + 56)], 11, 17, a.GREY, hold=0.2)
go(a, "dato", [ARC, (AX + 8, 262), (VM[0], 262), VM], 18, 22, a.GREY, hold=1.5)
at(a, a.text(318, 474, "lento: va al disco", 15, a.BAD, a.SANS, 600), 8, 25)
# 2 · hit
go(a, "leer", [VM, (VM[0], 262), (AX + 8, 262), ARC], 28, 31, a.BLUE, hold=0.2)
at(a, chip(a, AX + 46, 214, "está en el ARC", "ok"), 31, 44)
go(a, "dato", [ARC, (AX + 8, 262), (VM[0], 262), VM], 32, 35, a.OK, hold=2)
at(a, a.text(318, 474, "rápido: el disco ni se entera", 15, a.OK, a.SANS, 600), 32, 50)
# 3 · crece
for i in range(4):
    go(a, "dato", [(AX + 8, 440), (AX + 8, RY + 56)], 52 + i * 2.5, 54 + i * 2.5, a.GREY, hold=0.2)
at(a, a.text(318, 474, "cada lectura nueva suma al ARC", 15, a.BLUE, a.SANS, 600), 52, 62)
at(a, a.text(318, 474, "llegó al tope: no crece más", 15, a.AMB, a.SANS, 600), 62, 75, still=1)

# terminal
TX, TY, TW, TH = 930, 182, 222, 400
a.add(a.box(TX, TY, TW, TH, a.INK, rx=14))
a.add(a.text(TX + 16, TY + 28, "TERMINAL", 13, SKY, a.MONO, 400, extra='letter-spacing="1.8"'))
at(a, tline(a, TX + 16, TY + 60, "Cada lectura:", SKY) + tline(a, TX + 16, TY + 86, "¿está en el ARC?", SKY), 0, 75, still=1)
at(a, tline(a, TX + 16, TY + 140, "no: al disco", CORAL), 8, 25)
at(a, tline(a, TX + 16, TY + 140, "sí: de la RAM", MINT), 32, 50)
at(a, tline(a, TX + 16, TY + 140, "sí: de la RAM", MINT), 52, 75, still=1)
p4 = (tline(a, TX + 16, TY + 60, "# cat /sys/module/", MINT) + tline(a, TX + 16, TY + 82, "zfs/parameters/", MINT)
      + tline(a, TX + 16, TY + 104, "zfs_arc_max", MINT) + tline(a, TX + 16, TY + 132, "6442450944", GOLD)
      + tline(a, TX + 16, TY + 172, "# cat /etc/", MINT) + tline(a, TX + 16, TY + 194, "modprobe.d/zfs.conf", MINT)
      + tline(a, TX + 16, TY + 222, "options zfs", GOLD) + tline(a, TX + 16, TY + 244, "zfs_arc_max=", GOLD) + tline(a, TX + 16, TY + 266, "6442450944", GOLD)
      + tline(a, TX + 16, TY + 310, "2 GiB + 1 GiB × 4", SKY) + tline(a, TX + 16, TY + 332, "= 6 GiB", SKY)
      + tline(a, TX + 16, TY + 354, "= 6442450944 bytes", SKY))
a.add(during(a, p4, 75, 100))

status(a, 628, [
    (0, 25, "Lo que no está en la caché sale del disco, que es lo más lento del servidor.", a.INK, 0),
    (25, 50, "Cuanto más se repiten las lecturas, más trabajo le ahorra el ARC al disco.", a.OK, 0),
    (50, 75, "Esa memoria compite con las VM: por eso el ARC tiene un tope.", a.AMB, 1),
    (75, 100, "La regla oficial: 2 GiB de base más 1 GiB por TiB de pool, escrito en bytes.", a.BLUE, 0),
])

write(a, 3, "l2", "El ARC: la caché de ZFS en la RAM del host",
      "Animación en cuatro tiempos con la VM 100, la RAM del host de 64 GiB (16 GiB para la VM 100, 24 GiB para la VM 101 y el ARC de ZFS), un pool ZFS de 4 TiB y la terminal. "
      "1: primera lectura: el dato no está en el ARC, ZFS va al disco, que es lento, y el dato queda guardado en el ARC al volver a la VM. "
      "2: la segunda lectura del mismo dato sale de la RAM y el disco ni se entera. "
      "3: con cada dato nuevo el ARC crece hasta el tope zfs_arc_max, de 6 GiB, y ahí deja de crecer; esa memoria compite con las VM. "
      "4: el tope se lee en bytes con cat /sys/module/zfs/parameters/zfs_arc_max, que muestra 6442450944, y queda fijo en /etc/modprobe.d/zfs.conf con options zfs zfs_arc_max=6442450944; "
      "es la regla oficial de 2 GiB de base más 1 GiB por TiB de pool: con 4 TiB, 6 GiB.",
      [8, 33, 56, 68, 90])
