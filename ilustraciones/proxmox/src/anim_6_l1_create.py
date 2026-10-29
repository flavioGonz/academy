#!/usr/bin/env python3
"""Lección 6 · Laboratorio, paso 3: qué hace pct create con --unprivileged 1. Crea el rootfs en local-lvm
(vm-300-disk-0, 8 GB), desempaqueta la plantilla corriendo cada dueño (0 → 100000), escribe /etc/pve/lxc/300.conf
y, al arrancar, adentro los archivos son de root y en el host del usuario 100000.
Fuentes: guía de administración (pct create, rootfs, unprivileged), tarjeta de la lección (uid_map 0 100000 65536)."""
from _anim_pmx_red import *

a = new(24, "Contenedor sin privilegios", "pct create: los dueños se corren 100000", lab=True)
a.steps([
    "pct create arma el disco rootfs de 8 GB en local-lvm.",
    "Desempaqueta la plantilla: cada dueño 0 se escribe como 100000.",
    "Guarda la configuración en /etc/pve/lxc/300.conf.",
    "Adentro los archivos son de root; en el host, del usuario 100000.",
], still=1)

# plantilla
PX, PY, PW, PH = 48, 182, 340, 250
a.add(a.box(PX, PY, PW, PH, a.WHITE, a.LINE, rx=14))
a.add(glyph(a, "card", PX + 18, PY + 16))
a.add(a.text(PX + 60, PY + 36, "Plantilla en local", 17, a.INK, a.SANS, 600))
a.add(a.text(PX + 18, PY + 64, "vztmpl/debian-13-standard_", 15, a.GREY, a.MONO))
a.add(a.text(PX + 18, PY + 86, "..._amd64.tar.zst", 15, a.GREY, a.MONO))
FILES = ["/etc/passwd", "/usr/bin/bash", "/root/"]
for i, f in enumerate(FILES):
    y = PY + 124 + i * 38
    a.add(a.box(PX + 18, y, PW - 36, 30, a.SLATE, rx=6) + a.text(PX + 30, y + 21, f, 15, a.INK, a.MONO) + a.text(PX + PW - 30, y + 21, "0:0", 15, a.BLUE, a.MONO, 700, "end"))

# rootfs
RX, RY, RW, RH = 812, 182, 340, 250
a.add(during(a, a.box(RX, RY, RW, RH, a.WHITE, a.BLUE, rx=14, sw=2), 3, 100, still=1))
a.add(during(a, glyph(a, "server", RX + 18, RY + 16) + a.text(RX + 60, RY + 36, "rootfs del CT 300", 17, a.INK, a.SANS, 600)
             + a.text(RX + 18, RY + 64, "local-lvm:vm-300-disk-0", 15, a.GREY, a.MONO) + a.text(RX + 18, RY + 86, "8 GB · con formato", 15, a.GREY, a.MONO), 3, 100, still=1))
for i, f in enumerate(FILES):
    y = RY + 124 + i * 38
    a.add(during(a, a.box(RX + 18, y, RW - 36, 30, a.SLATE, rx=6) + a.text(RX + 30, y + 21, f, 15, a.INK, a.MONO)
                 + a.text(RX + RW - 30, y + 21, "100000:100000", 15, a.AMB, a.MONO, 700, "end"), 34 + i * 4, 100, still=1))
# traslado con +100000
MX = (PX + PW + RX) / 2
a.add(a.box(MX - 110, 252, 220, 110, a.INK, rx=14))
a.add(a.text(MX, 284, "corrimiento", 15, SKY, a.MONO, 400, "middle"))
a.add(a.text(MX, 316, "uid + 100000", 18, GOLD, a.MONO, 700, "middle"))
a.add(a.text(MX, 344, "gid + 100000", 15, GOLD, a.MONO, 600, "middle"))
for i, f in enumerate(FILES):
    y = PY + 139 + i * 38
    a.add(travel(a, a.pill(-36, -14, "0:0", a.BLUE, "#E5F0FB", 15, 28), [(PX + PW - 30, y), (MX - 110, y if y < 300 else 300)], 27 + i * 4, 29 + i * 4, hold=0.1, fade=0.3))
    a.add(travel(a, a.pill(-80, -14, "100000", a.AMB, a.AMBBG, 15, 28), [(MX + 110, 300), (RX + 120, y)], 30 + i * 4, 33 + i * 4, hold=0.3, fade=0.3))

# 300.conf
CX, CY, CW, CH = 48, 458, 520, 140
a.add(during(a, a.box(CX, CY, CW, CH, a.WHITE, a.LINE, rx=14) + a.text(CX + 18, CY + 30, "/etc/pve/lxc/300.conf", 15, a.GREY, a.MONO)
             + a.text(CX + 18, CY + 58, "hostname: ct-prueba", 15, a.TXT, a.MONO) + a.text(CX + 18, CY + 82, "memory: 512", 15, a.TXT, a.MONO)
             + a.text(CX + 18, CY + 106, "rootfs: local-lvm:vm-300-disk-0,size=8G", 15, a.TXT, a.MONO)
             + a.box(CX + 270, CY + 42, 232, 26, a.AMBBG, rx=6) + a.text(CX + 280, CY + 60, "unprivileged: 1", 15, a.AMB, a.MONO, 700), 52, 100, still=0))
a.add(during(a, a.box(CX, CY, CW, CH, a.WHITE, a.LINE, rx=14) + a.text(CX + 18, CY + 30, "# pct create 300 local:vztmpl/<plantilla>", 15, a.INK, a.MONO, 600)
             + a.text(CX + 18, CY + 58, "  --unprivileged 1 --memory 512", 15, a.TXT, a.MONO, extra='xml:space="preserve"')
             + a.text(CX + 18, CY + 82, "  --rootfs local-lvm:8 --net0 ...", 15, a.TXT, a.MONO, extra='xml:space="preserve"')
             + a.text(CX + 18, CY + 116, "el CT todavía no arrancó", 15, a.GREY, a.SANS), 0, 52, still=1))
# vista adentro y afuera
VX, VY, VW, VH = 600, 458, 552, 140
v = (a.box(VX, VY, VW, VH, a.INK, rx=14)
     + tline(a, VX + 18, VY + 30, "adentro: # ls -ln /etc/passwd", MINT)
     + tline(a, VX + 18, VY + 54, "-rw-r--r-- 1 0 0 ... /etc/passwd", a.WHITE)
     + tline(a, VX + 18, VY + 90, "host:    # ls -ln (rootfs montado)", MINT)
     + tline(a, VX + 18, VY + 114, "-rw-r--r-- 1 100000 100000 ... passwd", GOLD))
a.add(during(a, v, 76, 100))
a.add(during(a, note(a, VX, VY, VW, VH, "Por qué se corre", ["Así, adentro root es dueño de todo y el sistema", "funciona normal; pero en el host esos archivos", "son de un usuario sin poder."], "info"), 0, 76, still=1))

status(a, 636, [
    (0, 25, "El contenedor no tiene disco virtual con su propio sistema: tiene un rootfs con archivos.", a.INK, 0),
    (25, 50, "Con --unprivileged 1, los dueños se escriben corridos: 0 pasa a 100000, 1 a 100001.", a.AMB, 1),
    (50, 75, "unprivileged: 1 queda en la configuración: es lo que pct config 300 confirma.", a.BLUE, 0),
    (75, 100, "El mismo archivo: de root para el contenedor, del usuario 100000 para el host.", a.OK, 0),
])

write(a, 6, "l1", "pct create: los dueños se corren 100000",
      "Animación en cuatro tiempos con la plantilla Debian en local, el rootfs del contenedor 300 y el archivo /etc/pve/lxc/300.conf. "
      "1: pct create 300 local:vztmpl/<plantilla> --unprivileged 1 --memory 512 --rootfs local-lvm:8 arma el disco rootfs vm-300-disk-0 de 8 GB en local-lvm, con formato; el contenedor todavía no arrancó. "
      "2: desempaqueta la plantilla adentro; en la plantilla /etc/passwd, /usr/bin/bash y /root/ son del dueño 0:0, y en el rootfs se escriben con uid y gid más 100000: quedan de 100000:100000. "
      "3: guarda la configuración en /etc/pve/lxc/300.conf con hostname ct-prueba, memory 512, el rootfs y unprivileged: 1, que es lo que confirma pct config 300. "
      "4: adentro, ls -ln /etc/passwd muestra dueño 0, root; desde el host el mismo archivo es del usuario 100000, un usuario sin poder.",
      [8, 36, 46, 62, 90])
