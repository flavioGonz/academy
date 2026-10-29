#!/usr/bin/env python3
"""Lección 7 · Laboratorio, paso 3: la VM restaurada con otro ID trae la configuración de la original (misma MAC, y
adentro la misma IP fija). Si arrancara conectada, la red vería dos equipos iguales. Con link_down=1 la placa está
desconectada: no sale nada y se verifica por consola.
Fuentes: guía de administración (qmrestore conserva la configuración; --unique asigna MAC nueva; link_down),
tarjeta de la lección (paso 3)."""
from _anim_pmx_red import *

a = new(24, "Backup que restaura", "La 900 es una copia exacta: por eso link_down", lab=True)
a.steps([
    "qmrestore ... 900: la copia trae la misma MAC y, adentro, la misma IP.",
    "Si arrancara conectada, la red vería dos equipos iguales.",
    "link_down=1: la placa de la 900 queda desconectada; no sale nada.",
    "qm start 900: arranca aislada y la revisás por la consola.",
], still=2)

HX, HY, HW, HH = 48, 180, 700, 330
a.add(a.box(HX, HY, HW, HH, a.WHITE, a.LINE, rx=18))
a.add(glyph(a, "server", HX + 18, HY + 16))
a.add(a.text(HX + 60, HY + 36, "pve1", 19, a.INK, a.SANS, 600))
BY = HY + 250
a.add(a.box(HX + 20, BY, HW - 40, 40, a.NAVY2, rx=10) + a.text(HX + 40, BY + 26, "vmbr0", 15, a.WHITE, a.MONO, 600))
# VM 100
a.add(dev(a, HX + 40, HY + 64, 280, 110, "VM 100 · producción", "MAC BC:24:11:AA:10:00", icon="server", sub2="IP 10.10.10.100", tsize=17))
a.add(line(HX + 180, HY + 174, HX + 180, BY, a.BLUE, 4))
# VM 900
V9 = HX + 380


def vm900(stroke, note_txt, col, t0, t1, still=0):
    s = dev(a, V9, HY + 64, 280, 110, "VM 900 · restaurada", "MAC BC:24:11:AA:10:00", icon="server", sub2="IP 10.10.10.100", tsize=17, stroke=stroke, sw=2.5)
    s += a.text(V9 + 154, HY + 206, note_txt, 15, col, a.SANS, 600)
    at(a, s, t0, t1, still)


vm900(a.AMB, "apagada · copia de la 100", a.AMB, 4, 25)
vm900(a.BAD, "conectada: choca con la 100", a.BAD, 25, 50)
vm900(a.OK, "link_down=1 · desconectada", a.OK, 50, 75, still=1)
vm900(a.OK, "running · aislada", a.OK, 75, 100)
go(a, "qmrestore", [(V9 + 140, 150), (V9 + 140, HY + 100)], 1, 4, a.BLUE, hold=0.3)
# cable de la 900
at(a, line(V9 + 140, HY + 174, V9 + 140, BY, a.BAD, 4), 25, 50)
at(a, line(V9 + 140, HY + 174, V9 + 140, HY + 206, a.GREY, 3, "6 6") + line(V9 + 140, HY + 226, V9 + 140, BY, a.GREY, 3, "6 6"), 50, 100, still=1)
at(a, xmark(a, V9 + 140, HY + 232, 13), 52, 100, still=1)
# switch y usuario
SX = 800
a.add(a.box(SX, BY - 30, 120, 100, a.INK, rx=14) + a.text(SX + 60, BY + 26, "Switch", 17, a.WHITE, a.SANS, 600, "middle"))
a.add(line(HX + HW - 20, BY + 20, SX, BY + 20, a.BLUE, 4))
a.add(dev(a, 960, BY - 40, 192, 120, "PC del cliente", "usa la VM 100", icon="laptop", tsize=17))
a.add(line(SX + 120, BY + 20, 960, BY + 20, a.BLUE, 3))
# paso 2: el choque
for t in (28, 36, 44):
    go(a, "¿.100?", [(960, BY + 20), (SX + 60, BY + 20)], t, t + 2, a.GREY, hold=0.2)
    go(a, "soy .100", [(HX + 180, HY + 174), (HX + 180, BY + 20), (SX, BY + 20)], t + 2.5, t + 5, a.BLUE, hold=0.2)
    go(a, "soy .100", [(V9 + 140, HY + 174), (V9 + 140, BY + 20), (SX, BY + 20)], t + 3, t + 5.5, a.BAD, hold=0.2)
at(a, note(a, SX, HY, 352, 160, "Dos equipos iguales", ["Misma MAC y misma IP: el bridge y el", "switch no saben a cuál mandar. La", "PC del cliente se corta con la 100,", "que está en producción."], "bad"), 30, 50)
at(a, note(a, SX, HY, 352, 160, "Qué viene en el backup", ["La configuración entera: placa, MAC,", "discos. Adentro, el sistema tiene su", "IP fija. qmrestore --unique daría", "otra MAC, pero no otra IP."], "info"), 0, 30, still=0)
at(a, note(a, SX, HY, 352, 160, "Placa desconectada", ["Para la 900 es como un cable", "desenchufado: no manda ni recibe.", "La 100 sigue atendiendo sola."], "ok"), 50, 75, still=1)
at(a, note(a, SX, HY, 352, 160, "Verificar sin red", ["Consola: el sistema arranca y los", "datos están. Anotás cuánto tardó el", "restore y después la borrás."], "ok"), 75, 100)
# paso 4: consola
go(a, "consola", [(V9 + 140, HY + 26), (V9 + 140, HY + 64)], 78, 81, a.CYAN, hold=6)

# terminal
TX, TY, TW, TH = 48, 530, 1104, 66
a.add(a.box(TX, TY, TW, TH, a.INK, rx=12))
for t0, t1, c, st in [(0, 25, "# qmrestore /var/lib/vz/dump/vzdump-qemu-100-<fecha>.vma.zst 900", 0),
                      (25, 50, "# qm start 900      ← sin el paso 3: no lo hagas", 0),
                      (50, 75, "# qm set 900 --net0 virtio,bridge=vmbr0,link_down=1", 1),
                      (75, 100, "# qm start 900      → consola · ... · qm stop 900 && qm destroy 900", 0)]:
    at(a, tline(a, TX + 18, TY + 41, c, CORAL if t0 == 25 else MINT), t0, t1, still=st)

status(a, 634, [
    (0, 25, "Restaurar con otro ID no cambia lo que hay adentro: es la misma máquina.", a.INK, 0),
    (25, 50, "Una prueba de restore no puede cortarle el servicio a la VM en producción.", a.BAD, 0),
    (50, 75, "Antes de arrancar, la placa desconectada: la prueba queda aislada.", a.OK, 1),
    (75, 100, "Restore probado: el archivo está sano, la VM arranca y sabés cuánto tarda.", a.OK, 0),
])

write(a, 7, "l1", "La 900 es una copia exacta: por eso link_down",
      "Animación en cuatro tiempos con el host pve1, el bridge vmbr0, la VM 100 en producción (MAC BC:24:11:AA:10:00, IP 10.10.10.100), la VM 900 restaurada, un switch y la PC de un usuario de la 100. "
      "1: qmrestore del archivo vzdump-qemu-100-<fecha>.vma.zst con el ID 900 crea una copia exacta: la configuración trae la misma placa y la misma MAC, y adentro el sistema tiene la misma IP fija; qmrestore --unique daría otra MAC, pero no otra IP. "
      "2: si la 900 arrancara conectada, la PC pregunta por 10.10.10.100 y contestan las dos VM; con dos equipos iguales el bridge y el switch no saben a cuál mandar y la PC se corta con la 100, que está en producción. "
      "3: qm set 900 --net0 virtio,bridge=vmbr0,link_down=1 deja la placa de la 900 desconectada, como un cable desenchufado; la 100 sigue atendiendo sola. "
      "4: qm start 900 arranca la VM aislada; por la consola se verifica que el sistema arranca y los datos están, se anota cuánto tardó el restore y después qm stop 900 y qm destroy 900 la borran.",
      [10, 40, 62, 82, 94])
