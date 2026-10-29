#!/usr/bin/env python3
"""Lección 7 · Resumen, "Cómo se ve en la red": el día que hace falta. vzdump manda cada noche el archivo completo a
otro almacenamiento (NFS); el snapshot queda en el mismo pool. Si el pool se pierde, el disco y el snapshot se van
juntos; el backup sigue en el NFS, qmrestore arma la VM otra vez y arranca con sus datos.
Fuentes: guía de administración (vzdump, almacenamientos NFS/CIFS/PBS, qmrestore), tarjeta de la lección
(snapshot no es backup, restore de prueba)."""
from _anim_pmx_red import *

a = new(24, "Backup que restaura", "El snapshot se va con el disco; el backup no")
a.steps([
    "Cada noche, vzdump manda la VM 100 completa al NFS.",
    "Falla el RAID del host: el disco y el snapshot se pierden juntos.",
    "qmrestore lee el archivo del NFS y arma los discos otra vez.",
    "La VM arranca con los datos de anoche, en el tiempo que ya mediste.",
], still=2)

# host
HX, HY, HW, HH = 48, 180, 560, 300
a.add(a.box(HX, HY, HW, HH, a.WHITE, a.LINE, rx=18))
a.add(glyph(a, "server", HX + 18, HY + 16))
a.add(a.text(HX + 60, HY + 36, "pve1", 19, a.INK, a.SANS, 600))
a.add(a.text(HX + 112, HY + 36, "VM 100 · servidor de archivos", 15, a.GREY, a.MONO))
PX, PY, PW, PH = HX + 20, HY + 64, HW - 40, 210


def pool(state, t0, t1, still=0):
    if state == "ok":
        s = a.box(PX, PY, PW, PH, a.SLATE, a.LINE, rx=14)
        s += a.text(PX + 18, PY + 30, "local-lvm · sobre el RAID del host", 16, a.INK, a.SANS, 600)
        s += a.box(PX + 18, PY + 50, PW - 36, 56, a.WHITE, a.BLUE, rx=10, sw=2) + a.text(PX + 34, PY + 84, "vm-100-disk-0 · el disco de la VM", 15, a.BLUE, a.MONO, 600)
        s += a.box(PX + 18, PY + 120, PW - 36, 56, a.WHITE, a.AMB, rx=10, sw=2) + a.text(PX + 34, PY + 154, "snapshot antes-upgrade", 15, a.AMB, a.MONO, 600)
    elif state == "bad":
        s = a.box(PX, PY, PW, PH, a.BADBG, a.BAD, rx=14, sw=2.5, extra='stroke-dasharray="10 7"')
        s += a.text(PX + 18, PY + 30, "local-lvm · el RAID falló", 16, a.BAD, a.SANS, 600)
        s += a.box(PX + 18, PY + 50, PW - 36, 56, "none", a.BAD, rx=10, sw=1.5, extra='stroke-dasharray="6 6"') + a.text(PX + 34, PY + 84, "vm-100-disk-0 · perdido", 15, a.BAD, a.MONO, 600)
        s += a.box(PX + 18, PY + 120, PW - 36, 56, "none", a.BAD, rx=10, sw=1.5, extra='stroke-dasharray="6 6"') + a.text(PX + 34, PY + 154, "snapshot antes-upgrade · perdido", 15, a.BAD, a.MONO, 600)
    else:
        s = a.box(PX, PY, PW, PH, a.OKBG, a.OK, rx=14, sw=2)
        s += a.text(PX + 18, PY + 30, "local-lvm · discos nuevos", 16, a.OK, a.SANS, 600)
        s += a.box(PX + 18, PY + 50, PW - 36, 56, a.WHITE, a.OK, rx=10, sw=2) + a.text(PX + 34, PY + 84, "vm-100-disk-0 · restaurado", 15, a.OK, a.MONO, 600)
        s += a.text(PX + 34, PY + 150, "los snapshots no vuelven: vivían en el pool", 15, a.GREY, a.SANS)
    at(a, s, t0, t1, still)


pool("ok", 0, 27)
pool("bad", 27, 52)
pool("new", 52, 100, still=1)
at(a, xmark(a, PX + PW - 26, PY + 26, 16), 29, 52)

# NFS
NX, NY, NW, NH = 812, 180, 340, 190
a.add(dev(a, NX, NY, NW, NH, "NFS · backups", "otro equipo, otro disco", icon="server", tsize=18))
at(a, a.box(NX + 18, NY + 92, NW - 36, 76, a.OKBG, a.OK, rx=10, sw=2) + a.text(NX + 34, NY + 122, "vzdump-qemu-100-", 15, a.OK, a.MONO, 700)
   + a.text(NX + 34, NY + 146, "<fecha>.vma.zst", 15, a.OK, a.MONO, 700), 14, 100, still=1)
at(a, a.text(NX + NW - 18, NY + 34, "intacto", 15, a.OK, a.MONO, 700, "end"), 30, 52)
a.add(path(f"M{HX + HW} {HY + 150} H{NX}", a.LINE, 3))
for i in range(5):
    a.add(travel(a, a.box(-14, -10, 28, 20, a.BLUE, rx=4), [(HX + HW - 10, HY + 150), (NX + 10, HY + 150)], 4 + i * 1.6, 9 + i * 1.6, hold=0.1, fade=0.3))
at(a, chip(a, (HX + HW + NX) / 2, HY + 110, "configuración + discos", "info", anchor="middle"), 4, 25)
for i in range(5):
    a.add(travel(a, a.box(-14, -10, 28, 20, a.OK, rx=4), [(NX + 10, HY + 150), (HX + HW - 10, HY + 150)], 54 + i * 1.6, 59 + i * 1.6, hold=0.1, fade=0.3))
at(a, chip(a, (HX + HW + NX) / 2, HY + 110, "qmrestore", "ok", anchor="middle"), 54, 75)

# la VM vuelve
at(a, dev(a, NX, 392, NW, 88, "VM 100 · running", "datos de anoche", icon="server", tsize=18, stroke=a.OK, sw=2.5), 78, 100)
at(a, check(a, NX + NW - 26, 420), 80, 100)

# terminal
TX, TY, TW, TH = 48, 500, 1104, 96
a.add(a.box(TX, TY, TW, TH, a.INK, rx=12))
at(a, tline(a, TX + 18, TY + 36, "# vzdump 100 --mode snapshot --compress zstd --storage nfs-backups", MINT)
   + tline(a, TX + 18, TY + 66, "archivo completo: configuración y todos los discos, en otro almacenamiento", SKY), 0, 25)
at(a, tline(a, TX + 18, TY + 36, "el pool del host no responde: VM 100 sin disco", CORAL)
   + tline(a, TX + 18, TY + 66, "qm rollback antes-upgrade no sirve: el snapshot estaba en el mismo pool", CORAL), 27, 50)
at(a, tline(a, TX + 18, TY + 36, "# qmrestore /mnt/pve/nfs-backups/dump/vzdump-qemu-100-<fecha>.vma.zst 100 --storage local-lvm", MINT)
   + tline(a, TX + 18, TY + 66, "la VM 100 ya no existe; si existiera, la prueba va a un ID nuevo", SKY), 50, 75, still=1)
at(a, tline(a, TX + 18, TY + 36, "# qm start 100", MINT)
   + tline(a, TX + 18, TY + 66, "el restore de prueba del mes ya te dijo cuánto tarda: eso le contestás al cliente", SKY), 75, 100)

status(a, 634, [
    (0, 25, "El backup sale del host: va a otro equipo, con todo lo necesario para rearmar la VM.", a.BLUE, 0),
    (25, 50, "Un snapshot sirve para deshacer un cambio, no para sobrevivir a la pérdida del disco.", a.BAD, 0),
    (50, 75, "El archivo de vzdump alcanza para reconstruir la VM en cualquier nodo.", a.OK, 1),
    (75, 100, "Un backup cuenta cuando ya lo restauraste: la prueba mensual es la que te da esta tranquilidad.", a.OK, 0),
], size=17)

write(a, 7, "r1", "El snapshot se va con el disco; el backup no",
      "Animación en cuatro tiempos con el host pve1 y la VM 100, servidor de archivos, cuyo disco vm-100-disk-0 y un snapshot llamado antes-upgrade viven en local-lvm, sobre el RAID del host, y un NFS de backups en otro equipo. "
      "1: cada noche vzdump 100 --mode snapshot --compress zstd --storage nfs-backups manda la configuración y todos los discos, en un archivo completo vzdump-qemu-100-<fecha>.vma.zst, al NFS. "
      "2: falla el RAID del host; el disco de la VM y el snapshot se pierden juntos, porque el snapshot estaba en el mismo pool y un rollback no sirve; el archivo en el NFS sigue intacto. "
      "3: qmrestore con el archivo del NFS arma otra vez la VM 100 en local-lvm, con discos nuevos; como la VM 100 ya no existe se restaura con su ID, y en una prueba se usa un ID nuevo. Los snapshots no vuelven. "
      "4: qm start 100 y la VM arranca con los datos de anoche; el restore de prueba mensual ya dijo cuánto tarda.",
      [8, 36, 62, 70, 92])
