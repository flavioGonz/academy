#!/usr/bin/env python3
"""Lección 8 · Resumen, "Cómo se ve en la red": un ransomware en el host. pve1 sube los backups a PBS con un token
que tiene DatastoreBackup; si el host cae en manos de un atacante, ese token no puede borrar ni modificar backups
existentes. Un sync job lleva la copia a otro PBS fuera del sitio, y se restaura desde los backups de antes.
Fuentes: documentación de PBS (Ransomware: no reescribe bloques existentes, Datastore.Backup no borra, sync jobs
fuera del sitio sin borrar lo que desaparece del origen), tarjeta de la lección (regla 3-2-1)."""
from _anim_pmx_red import *

a = new(24, "PBS sin sorpresas", "El token que sube backups pero no los puede borrar")
a.steps([
    "Cada noche pve1 sube los trozos nuevos con el token backup@pbs!pve.",
    "Un ransomware toma pve1: cifra las VM y pide borrar backups. PBS dice que no.",
    "El sync job copia el datastore al PBS de IES, en otra ciudad.",
    "Se reinstala el host y se restaura desde el backup de antes del ataque.",
], still=1)

# pve1
HX, HY, HW, HH = 48, 186, 270, 170
at(a, dev(a, HX, HY, HW, HH, "pve1", "token backup@pbs!pve", icon="server", sub2="rol: DatastoreBackup", tsize=19), 0, 25)
at(a, dev(a, HX, HY, HW, HH, "pve1", "token backup@pbs!pve", icon="server", sub2="rol: DatastoreBackup", tsize=19), 50, 75)
at(a, dev(a, HX, HY, HW, HH, "pve1 · comprometido", "VM cifradas", icon="warn", sub2="token backup@pbs!pve", tsize=19, stroke=a.BAD, sw=3, fill=a.BADBG), 25, 50, still=1)
at(a, dev(a, HX, HY, HW, HH, "pve1 · reinstalado", "limpio, desde cero", icon="server", sub2="restaura desde PBS", tsize=19, stroke=a.OK, sw=2.5), 75, 100)
for i, vm in enumerate(["VM 100", "VM 101"]):
    x = HX + 20 + i * 122
    at(a, a.box(x, HY + 112, 110, 40, a.SLATE, rx=8) + a.text(x + 55, HY + 138, vm, 15, a.INK, a.MONO, 600, "middle"), 0, 25)
    at(a, a.box(x, HY + 112, 110, 40, a.BAD, rx=8) + a.text(x + 55, HY + 138, vm + " ✗", 15, a.WHITE, a.MONO, 700, "middle"), 25, 50, still=1)
    at(a, a.box(x, HY + 112, 110, 40, a.SLATE, rx=8) + a.text(x + 55, HY + 138, vm, 15, a.INK, a.MONO, 600, "middle"), 50, 75)
    at(a, a.box(x, HY + 112, 110, 40, a.OKBG, a.OK, rx=8) + a.text(x + 55, HY + 138, vm + " ✓", 15, a.OK, a.MONO, 700, "middle"), 86, 100)

# PBS main
MX, MY, MW, MH = 470, 186, 300, 330
a.add(a.box(MX, MY, MW, MH, a.INK, rx=16))
a.add(glyph(a, "shield", MX + 18, MY + 16, a.CYAN))
a.add(a.text(MX + 60, MY + 36, "PBS · datastore main", 18, a.WHITE, a.SANS, 600))
a.add(a.text(MX + 60, MY + 60, "en la sala del cliente", 15, SKY, a.MONO))
SNAP = ["vm/100 · lunes", "vm/100 · martes", "vm/101 · martes", "vm/100 · miércoles"]
for i, s in enumerate(SNAP):
    y = MY + 84 + i * 50
    t_in = 0 if i < 3 else 6
    a.add(during(a, a.box(MX + 18, y, MW - 36, 40, a.NAVY2, rx=8) + a.text(MX + 34, y + 26, s, 15, a.WHITE, a.MONO, 600), t_in, 100, still=1))
    a.add(during(a, glyph(a, "lock", MX + MW - 52, y + 8, MINT, 1.0), 30, 50, still=1))
a.add(a.text(MX + 18, MY + 304, "no reescribe trozos existentes", 15, MINT, a.SANS, 600))
# subida nocturna
for i in range(4):
    a.add(travel(a, a.box(-12, -9, 24, 18, a.CYAN, rx=4), [(HX + HW, HY + 60), (MX, MY + 250)], 2 + i * 1.5, 7 + i * 1.5, hold=0.1, fade=0.3))
at(a, chip(a, (HX + HW + MX) / 2, HY + 194, "solo lo nuevo", "info", anchor="middle"), 3, 25)
# ataque: pedido de borrado
go(a, "borrar", [(HX + HW, HY + 60), (MX + 30, HY + 60)], 31, 35, a.BAD, hold=1)
go(a, "sin permiso", [(MX + 30, HY + 96), (HX + HW - 10, HY + 96)], 37, 41, a.OK, hold=6)
go(a, "sobrescribir", [(HX + HW, HY + 130), (MX + 30, HY + 130)], 41, 44, a.BAD, hold=1)
at(a, xmark(a, MX + 10, HY + 130, 13), 44, 50)

# PBS remoto
RX, RY, RW, RH = 812, 186, 340, 330
a.add(a.box(RX, RY, RW, RH, a.WHITE, a.LINE, rx=16))
a.add(glyph(a, "shield", RX + 18, RY + 16))
a.add(a.text(RX + 60, RY + 36, "PBS de IES", 18, a.INK, a.SANS, 600))
a.add(a.text(RX + 60, RY + 60, "otra ciudad · fuera del sitio", 15, a.GREY, a.MONO))
for i, s in enumerate(SNAP):
    y = RY + 84 + i * 50
    a.add(during(a, a.box(RX + 18, y, RW - 36, 40, a.OKBG, a.OK, rx=8, sw=1.5) + a.text(RX + 34, y + 26, s, 15, a.OK, a.MONO, 600), 56 + i * 3, 100, still=0))
at(a, a.text(RX + 18, RY + 298, "sync job: no borra lo que", 15, a.TXT, a.SANS, 600) + a.text(RX + 18, RY + 320, "desaparece del origen", 15, a.TXT, a.SANS, 600), 54, 100)
for i in range(4):
    a.add(travel(a, a.box(-12, -9, 24, 18, a.OK, rx=4), [(MX + MW, MY + 120 + i * 50), (RX, RY + 104 + i * 50)], 54 + i * 3, 57 + i * 3, hold=0.1, fade=0.3))
at(a, chip(a, (MX + MW + RX) / 2, MY + MH + 12, "sync job", "ok", anchor="middle"), 53, 75)
# restore
for i in range(4):
    a.add(travel(a, a.box(-12, -9, 24, 18, a.OK, rx=4), [(MX, MY + 110), (HX + HW, HY + 120)], 80 + i * 1.5, 84 + i * 1.5, hold=0.1, fade=0.3))
at(a, chip(a, (HX + HW + MX) / 2, HY + 194, "restore", "ok", anchor="middle"), 80, 100)

# pie de la izquierda
at(a, note(a, HX, 386, HW, 130, "Lo que el token puede", ["Crear backups y leerlos.", "No puede borrarlos ni", "modificarlos."], "info"), 0, 25)
at(a, note(a, HX, 386, HW, 130, "El intento falla", ["Con DatastoreBackup no hay", "permiso para borrar. Y lo ya", "guardado no se reescribe."], "ok"), 25, 50, still=1)
at(a, note(a, HX, 386, HW, 130, "3-2-1", ["Tres copias, dos medios,", "una fuera del sitio: si se", "pierde el edificio, quedan."], "info"), 50, 75)
at(a, note(a, HX, 386, HW, 130, "Primero, host limpio", ["Se reinstala y se restaura", "desde un backup anterior", "al ataque."], "ok"), 75, 100)

status(a, 600, [
    (0, 25, "El host sube backups con un token propio, con el permiso justo para eso.", a.INK, 0),
    (25, 50, "Quien tome el host hereda ese token: por eso el token no puede borrar.", a.BAD, 1),
    (50, 75, "La copia de afuera no depende de la red del cliente ni de su edificio.", a.OK, 0),
    (75, 100, "Los backups de antes del ataque están intactos: de ahí sale la restauración.", a.OK, 0),
])
at(a, a.text(600, 632, "La retención y el borrado los hace el propio PBS, con prune jobs.", 16, a.GREY, a.SANS, 400, "middle"), 0, 100, still=1)

write(a, 8, "r1", "El token que sube backups pero no los puede borrar",
      "Animación en cuatro tiempos con el host pve1, que guarda en Proxmox Backup Server con el token backup@pbs!pve y el rol DatastoreBackup, el PBS del cliente con el datastore main y un PBS de IES en otra ciudad. "
      "1: cada noche pve1 sube solo los trozos nuevos a main, que guarda los backups vm/100 del lunes, martes y miércoles y vm/101 del martes; el token puede crear backups y leerlos, no borrarlos ni modificarlos. "
      "2: un ransomware toma pve1 y cifra las VM 100 y 101; con el mismo token pide borrar vm/100 y PBS lo rechaza por falta de permiso; tampoco puede sobrescribir, porque PBS no reescribe trozos existentes. "
      "3: un sync job copia el datastore al PBS de IES, fuera del sitio, configurado para no borrar lo que desaparece del origen: es la copia de la regla 3-2-1. "
      "4: el host se reinstala limpio y se restaura desde el backup del martes, anterior al ataque. La retención y el borrado los hace el propio PBS con prune jobs.",
      [8, 36, 46, 62, 90])
