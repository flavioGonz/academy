#!/usr/bin/env python3
"""Lección 1 · Laboratorio, paso 5: con el backup guardado, recién ahí actualizar. Lo que viaja en cada paso:
el .tar de la central a la notebook, el firmware de la notebook a la central (que se reinicia) y, si algo sale mal,
el .tar de vuelta con Restore. Fuentes: manual UCM630x (Maintenance > Upgrade, Backup/Restore; restauración en .tar o
.tgz, menos de 100 MB, sin caracteres especiales en el nombre)."""
from _anim_gs_red import R

g = R(T=26, fix=62, kicker="GRANDSTREAM · PRIMER ARRANQUE · LABORATORIO",
      title="Backup afuera, después el firmware")
g.steps([
    "Maintenance > Upgrade: anotás la versión que tiene la central antes de tocar nada.",
    "Backup/Restore > Backup: la central arma el .tar y lo bajás a tu notebook.",
    "Recién ahí subís el firmware: la central lo instala y se reinicia.",
    "Si algo no quedó como estaba, Restore con el .tar de la notebook.",
])

Y, H = 196, 96
YL = Y + H / 2
g.add(g.dev(48, Y, 262, H, "Notebook", "del técnico", icon="laptop"))
g.add(g.dev(470, Y, 300, H, "UCM6300", "192.168.88.20", icon="ucm", dark=True))
g.add(g.dev(900, Y, 252, H, "Teléfonos", "1001 · 1002 · 1003", icon="tel"))
g.add(g.wire(310, YL, 470, YL, g.BLUE))
g.add(g.wire(770, YL, 900, YL, g.BLUE))

# estado de la central y de los teléfonos
g.appear(g.pillc(620, Y + H + 12, "en servicio", g.OK, g.OKBG, 13, 26), 0, 54)
g.appear(g.pillc(620, Y + H + 12, "instalando y reiniciando…", g.AMB, g.AMBBG, 13, 26), 54, 72)
g.appear(g.pillc(620, Y + H + 12, "en servicio", g.OK, g.OKBG, 13, 26), 72, 100)
g.appear(g.pillc(1026, Y + H + 12, "registrados", g.OK, g.OKBG, 13, 26), 0, 56)
g.appear(g.pillc(1026, Y + H + 12, "sin central", g.BAD, g.BADBG, 13, 26), 56, 72)
g.appear(g.pillc(1026, Y + H + 12, "registrados", g.OK, g.OKBG, 13, 26), 72, 100)

# lo que viaja
LANE = Y - 20
tar = g.chip("backup.tar", bg=g.BLUE, size=13, h=26)
g.token([(620, LANE), (180, LANE)], 30, 42, tar, hold=44)
g.appear(g.pillc(179, Y + H + 12, "backup.tar guardado", g.BLUE, "#E6F0FA", 13, 26), 42, 100)
fw = g.chip("firmware nuevo", bg=g.CYAN, size=13, h=26)
g.token([(180, LANE), (620, LANE)], 52, 60, fw, hold=62)
tar2 = g.chip("backup.tar", bg=g.OK, size=13, h=26)
g.token([(180, LANE), (620, LANE)], 80, 88, tar2, hold=90)

# pantalla
PY = 352
g.appear(g.term(48, PY, 700, 160, "En la web de la UCM", [
    ("Maintenance > Upgrade", "#5BE0A5"),
    ("versión actual: anotala en la ficha", None),
    ("botón Detect: hay versión nueva?", None),
], size=17, lh=30), 0, 25)
g.appear(g.term(48, PY, 700, 160, "En la web de la UCM", [
    ("Maintenance > Backup > Backup/Restore", "#5BE0A5"),
    ("Backup: configuración completa", None),
    ("el .tar queda fuera de la central", "#F6C35B"),
], size=17, lh=30), 25, 50)
g.appear(g.term(48, PY, 700, 160, "En la web de la UCM", [
    ("Maintenance > Upgrade", "#5BE0A5"),
    ("subís el firmware: instala y reinicia", None),
    ("mientras reinicia: sin web y sin teléfonos", "#F6C35B"),
], size=17, lh=30), 50, 75)
g.appear(g.term(48, PY, 700, 160, "En la web de la UCM", [
    ("Maintenance > Backup > Backup/Restore", "#5BE0A5"),
    ("Restore: elegís el .tar de la notebook", None),
    ("la configuración vuelve a como estaba", "#5BE0A5"),
], size=17, lh=30), 75, 100)

NX, NW = 776, 376
g.appear(g.note(NX, PY, NW, "Por qué en este orden", ["Sin el .tar afuera, una", "actualización que sale mal se", "reconfigura de memoria."], "amb"), 0, 75)
g.appear(g.note(NX, PY, NW, "Para restaurar", [".tar o .tgz, menos de 100 MB", "y sin caracteres especiales", "en el nombre del archivo."], "ok"), 75, 100)

g.status(612, [
    (0, 25, "La versión anotada te dice a qué volver si algo cambia después.", g.INK),
    (25, 50, "El backup viaja de la central a la notebook: queda afuera.", g.BLUE),
    (50, 75, "Durante el reinicio la central no atiende: hacelo en ventana de mantenimiento.", g.AMB),
    (75, 100, "Con el .tar en la notebook, la vuelta atrás es un Restore, no una tarde entera.", g.OK),
])

g.done(1, "l1", "Backup afuera, después el firmware",
       "Animación en cuatro tiempos con la notebook del técnico, la UCM6300 en 192.168.88.20 y los teléfonos 1001, 1002 y 1003, con un recuadro de la web de la UCM. "
       "1: en Maintenance > Upgrade se anota la versión actual y con Detect se ve si hay una nueva. "
       "2: en Maintenance > Backup > Backup/Restore la central arma el backup completo y el archivo backup.tar viaja a la notebook: queda fuera de la central. "
       "3: recién ahí se sube el firmware nuevo; la central lo instala y se reinicia, y mientras tanto no hay web y los teléfonos se quedan sin central, por eso se hace en ventana de mantenimiento. "
       "4: si algo no quedó como estaba, Restore con el .tar de la notebook y la configuración vuelve a como estaba; el archivo de restauración va en .tar o .tgz, menos de 100 MB y sin caracteres especiales en el nombre.",
       [10, 38, 58, 66, 88])
