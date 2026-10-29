#!/usr/bin/env python3
"""Lección 3 · Resumen, "Cómo se ve en la red" (dentro del host): por qué ZFS quiere ver los discos. En un mirror
sobre HBA, ZFS lee un bloque, compara el checksum, detecta que el disco A devolvió un dato dañado, lee la copia del
disco B, entrega el dato bueno y reescribe A. Detrás de una RAID por hardware ve un solo disco: detecta el error
pero no tiene otra copia para corregirlo.
Fuentes: guía de administración (ZFS: checksums, RAID por software, no usar sobre RAID por hardware), tarjeta."""
from _anim_pmx_red import *

a = new(24, "Disco con criterio", "ZFS ve los dos discos y se cura solo")
a.steps([
    "La VM lee un bloque: ZFS lo pide al disco A y verifica el checksum.",
    "El checksum no coincide: el dato de A está dañado. ZFS lee la copia de B.",
    "La VM recibe el dato bueno y ZFS reescribe el bloque en A.",
    "Detrás de una RAID por hardware, ZFS ve un solo disco: no tiene la otra copia.",
], still=2)

# ---------- columna izquierda: VM, ZFS, discos
a.add(dev(a, 48, 182, 300, 76, "VM 100", "lee un archivo", icon="server", tsize=18))
ZX, ZY, ZW, ZH = 48, 296, 640, 96
a.add(a.box(ZX, ZY, ZW, ZH, a.INK, rx=16))
a.add(a.text(ZX + 22, ZY + 36, "ZFS · rpool · mirror", 19, a.WHITE, a.SANS, 600))
a.add(a.text(ZX + 22, ZY + 64, "cada bloque guarda su checksum", 15, SKY, a.MONO))
DA, DB = (78, 452), (388, 452)
for (x, y), n, s in ((DA, "disco A", "sda · por HBA"), (DB, "disco B", "sdb · por HBA")):
    a.add(a.box(x, y, 270, 120, a.WHITE, a.LINE, rx=14))
    a.add(a.text(x + 20, y + 32, n, 18, a.INK, a.SANS, 600))
    a.add(a.text(x + 20, y + 56, s, 15, a.GREY, a.MONO))
# bloques en cada disco
BAx, BBx, BYy = DA[0] + 20, DB[0] + 20, DA[1] + 70
a.add(during(a, a.box(BAx, BYy, 120, 36, a.SLATE, a.LINE, rx=8) + a.text(BAx + 60, BYy + 24, "bloque 7", 15, a.INK, a.MONO, 600, "middle"), 0, 31.5))
a.add(during(a, a.box(BAx, BYy, 120, 36, a.BADBG, a.BAD, rx=8) + a.text(BAx + 60, BYy + 24, "bloque 7 ✗", 15, a.BAD, a.MONO, 600, "middle"), 30, 62))
a.add(during(a, a.box(BAx, BYy, 120, 36, a.OKBG, a.OK, rx=8) + a.text(BAx + 60, BYy + 24, "bloque 7 ✓", 15, a.OK, a.MONO, 600, "middle"), 62, 100, still=1))
a.add(a.box(BBx, BYy, 120, 36, a.OKBG, a.OK, rx=8) + a.text(BBx + 60, BYy + 24, "bloque 7 ✓", 15, a.OK, a.MONO, 600, "middle"))
for x in (DA[0], DB[0]):
    a.add(line(x + 135, ZY + ZH, x + 135, DA[1], a.BLUE, 3))
a.add(line(198, 258, 198, ZY, a.BLUE, 3))

PA_UP, PA_DN = (DA[0] + 135, DA[1] - 10), (DA[0] + 135, ZY + ZH + 14)
PB_UP, PB_DN = (DB[0] + 135, DB[1] - 10), (DB[0] + 135, ZY + ZH + 14)
VM_DN, VM_UP = (198, ZY - 14), (198, 268)
# 1 · pedido a A, dato llega, checksum
go(a, "leer 7", [VM_UP, VM_DN], 2, 5, a.BLUE, hold=0.3)
go(a, "leer 7", [PA_DN, PA_UP], 6, 10, a.BLUE, hold=0.3)
at(a, chip(a, ZX + ZW - 20, ZY + 22, "checksum: verificando", "grey", anchor="end"), 10, 26)
# 2 · vuelve dañado, no coincide; leer B
go(a, "dato 7", [PA_UP, PA_DN], 26, 31, a.BAD, hold=1.5)
at(a, chip(a, ZX + ZW - 20, ZY + 22, "checksum: no coincide", "bad", anchor="end"), 31, 50)
go(a, "leer 7", [PB_DN, PB_UP], 38, 42, a.BLUE, hold=0.3)
go(a, "dato 7", [PB_UP, PB_DN], 43, 47, a.OK, hold=2)
# 3 · dato bueno a la VM, reescribe A
at(a, chip(a, ZX + ZW - 20, ZY + 22, "checksum: OK (copia de B)", "ok", anchor="end"), 50, 75, still=1)
go(a, "dato 7 ✓", [VM_DN, VM_UP], 52, 56, a.OK, hold=3)
go(a, "reescribe 7", [PA_DN, PA_UP], 57, 61, a.OK, hold=0.8)
at(a, check(a, 330, 200), 56, 100, still=1)

# ---------- panel derecho: zpool status (pasos 1 a 3)
RX, RY, RW, RH = 720, 182, 432, 390
tz = (a.box(RX, RY, RW, RH, a.INK, rx=14)
      + a.text(RX + 20, RY + 30, "# zpool status", 15, MINT, a.MONO))
rows = [("NAME", "STATE", "CKSUM"), ("rpool", "ONLINE", "0"), ("  mirror-0", "ONLINE", "0"), ("    sda", "ONLINE", None), ("    sdb", "ONLINE", "0")]
for i, (n, st, ck) in enumerate(rows):
    y = RY + 100 + i * 30
    col = SKY if i == 0 else a.WHITE
    tz += tline(a, RX + 20, y, n, col) + tline(a, RX + 210, y, st, col) + (tline(a, RX + 340, y, ck, col) if ck else "")
a.add(during(a, tz, 0, 75, still=1))
y_sda = RY + 100 + 3 * 30
at(a, tline(a, RX + 340, y_sda, "0"), 0, 31)
at(a, tline(a, RX + 340, y_sda, "1", GOLD), 31, 75, still=1)
at(a, tline(a, RX + 20, RY + 268, "status: ... An attempt was made", SKY) + tline(a, RX + 20, RY + 294, "to correct the error. Applications", SKY) +
   tline(a, RX + 20, RY + 320, "are unaffected.", MINT), 62, 75, still=1)
at(a, tline(a, RX + 20, RY + 268, "lectura en curso...", SKY), 6, 31)
at(a, tline(a, RX + 20, RY + 268, "sda devolvió un dato que no", GOLD) + tline(a, RX + 20, RY + 294, "coincide con su checksum", GOLD), 31, 50)
at(a, tline(a, RX + 20, RY + 352, "la cuenta queda: mirá CKSUM", SKY), 64, 75, still=1)

# ---------- paso 4: ZFS sobre RAID por hardware
p4 = a.box(RX, RY, RW, RH, a.WHITE, a.BAD, rx=14, sw=2)
p4 += a.text(RX + 20, RY + 34, "ZFS sobre RAID por hardware", 18, a.BAD, a.SANS, 600)
p4 += a.box(RX + 20, RY + 54, RW - 40, 58, a.INK, rx=10) + a.text(RX + 38, RY + 88, "ZFS ve 1 disco: sda", 15, a.WHITE, a.MONO, 600)
p4 += a.box(RX + 20, RY + 128, RW - 40, 112, a.SLATE, a.LINE, rx=10)
p4 += a.text(RX + 38, RY + 156, "Controladora RAID · caché", 15, a.INK, a.MONO, 600)
p4 += blocks(a, RX + 38, RY + 172, ["A", "B"], w=80, h=48)
p4 += a.text(RX + 230, RY + 200, "los discos reales", 15, a.GREY, a.SANS)
p4 += a.text(RX + 230, RY + 220, "quedan escondidos", 15, a.GREY, a.SANS)
p4 += a.text(RX + 20, RY + 280, "ZFS detecta el dato dañado, pero no", 15, a.INK, a.SANS)
p4 += a.text(RX + 20, RY + 302, "tiene otra copia para corregirlo.", 15, a.INK, a.SANS)
p4 += a.text(RX + 20, RY + 336, "Con RAID por hardware: LVM-thin.", 15, a.BAD, a.SANS, 600)
p4 += a.text(RX + 20, RY + 358, "Con ZFS: HBA o modo IT.", 15, a.OK, a.SANS, 600)
a.add(during(a, p4, 75, 100))
# en el paso 4 la columna izquierda se apaga un poco
a.add(during(a, a.box(40, 170, 660, 412, a.BG, rx=0, extra='opacity=".55"'), 76, 100))

status(a, 626, [
    (0, 25, "ZFS no confía en lo que devuelve el disco: compara cada bloque con su checksum.", a.INK, 0),
    (25, 50, "Un disco que devuelve basura sin avisar es justo lo que una RAID común no detecta.", a.BAD, 0),
    (50, 75, "Con dos copias, ZFS corrige solo y deja la cuenta en zpool status.", a.OK, 1),
    (75, 100, "Por eso ZFS nunca va encima de una controladora RAID con caché.", a.BAD, 0),
])

write(a, 3, "r1", "ZFS ve los dos discos y se cura solo",
      "Animación en cuatro tiempos con la VM 100, el pool ZFS rpool en mirror y dos discos conectados por HBA, sda y sdb, más la salida de zpool status. "
      "1: la VM lee un archivo; ZFS pide el bloque 7 al disco A y lo verifica contra el checksum que guarda de cada bloque. "
      "2: el disco A devolvió un dato dañado y el checksum no coincide; ZFS lee la copia del bloque 7 en el disco B, que está bien, y en zpool status la columna CKSUM de sda pasa a 1. "
      "3: la VM recibe el dato bueno, ZFS reescribe el bloque 7 en el disco A y zpool status avisa que se intentó corregir el error y que las aplicaciones no se vieron afectadas. "
      "4: si ZFS está encima de una controladora RAID por hardware con caché, ve un solo disco; detecta el dato dañado pero no tiene otra copia para corregirlo. "
      "Con RAID por hardware conviene LVM-thin; ZFS va con HBA o controladora en modo IT.",
      [8, 30, 44, 66, 90])
