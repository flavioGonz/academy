#!/usr/bin/env python3
"""Lección 11 · Laboratorio, paso 1: un usuario de solo lectura. pveum user add crea tecnico@pve sin permisos;
pveum acl modify / asigna PVEAuditor en la raíz; el rol se hereda hacia abajo (propagate) a nodos, VMs y
almacenamiento; pveum user permissions muestra lo que resulta.
Fuentes: guía de administración (árbol de permisos, propagación, roles PVEAuditor, privilegios .Audit), tarjeta."""
from _anim_pmx_red import *

a = new(24, "Acceso blindado", "Un rol en / y el árbol entero lo hereda", lab=True)
a.steps([
    "pveum user add tecnico@pve: el usuario existe, pero no ve nada.",
    "acl modify / --role PVEAuditor: el rol se asigna en la raíz.",
    "Se hereda hacia abajo: nodos, VMs y almacenamiento.",
    "user permissions muestra lo que resulta: mirar sí, tocar no.",
], still=2)

# árbol
R = (364, 214)
KIDS = [(150, 330, "/nodes"), (364, 330, "/vms"), (578, 330, "/storage")]
LEAF = [(150, 440, "/nodes/pve1"), (364, 440, "/vms/100"), (578, 440, "/storage/local-lvm")]
BW, BH = 196, 48


def node(x, y, lab, t_on=None, st=0):
    base = a.box(x - BW / 2, y - BH / 2, BW, BH, a.WHITE, a.LINE, rx=10, sw=2) + a.text(x, y + 6, lab, 15, a.INK, a.MONO, 600, "middle")
    a.add(base)
    if t_on is not None:
        at(a, a.box(x - BW / 2, y - BH / 2, BW, BH, a.OKBG, a.OK, rx=10, sw=2.5) + a.text(x, y + 6, lab, 15, a.OK, a.MONO, 700, "middle"), t_on, 100, still=st)


for (x, y, _) in KIDS:
    a.add(path(f"M{R[0]} {R[1] + BH / 2} V{(R[1] + y) / 2} H{x} V{y - BH / 2}", a.LINE, 3))
for (x, y, lab) in LEAF:
    px = 150 if lab.startswith("/nodes") else (364 if lab.startswith("/vms") else 578)
    a.add(path(f"M{px} {330 + BH / 2} V{y - BH / 2}", a.LINE, 3))
node(R[0], R[1], "/", 30, 1)
for i, (x, y, lab) in enumerate(KIDS):
    node(x, y, lab, 53 + i, 1)
for i, (x, y, lab) in enumerate(LEAF):
    node(x, y, lab, 58 + i, 1)
at(a, chip(a, R[0] + BW / 2 + 12, R[1] - 15, "PVEAuditor", "ok"), 30, 100, still=1)
# herencia: puntos que bajan
for (x, y, _) in KIDS:
    a.add(travel(a, f'<circle r="8" fill="{a.OK}"/>', [(R[0], R[1] + BH / 2), (R[0], (R[1] + y) / 2), (x, (R[1] + y) / 2), (x, y - BH / 2)], 51, 54, hold=0.2, fade=0.2))
for (x, y, lab) in LEAF:
    px = 150 if lab.startswith("/nodes") else (364 if lab.startswith("/vms") else 578)
    a.add(travel(a, f'<circle r="8" fill="{a.OK}"/>', [(px, 330 + BH / 2), (x, y - BH / 2)], 55, 58, hold=0.2, fade=0.2))
# usuario sin nada
at(a, dev(a, 48, 520, 320, 72, "tecnico@pve", "sin permisos: no ve nada", icon="user", tsize=17), 3, 26)
at(a, dev(a, 48, 520, 320, 72, "tecnico@pve", "rol PVEAuditor en /", icon="user", tsize=17, stroke=a.OK, sw=2), 26, 100, still=1)
at(a, a.text(400, 562, "propagate: el rol baja por todo el árbol", 15, a.OK, a.SANS, 600), 52, 100, still=1)

# terminal
TX, TY, TW, TH = 708, 182, 444, 410
a.add(a.box(TX, TY, TW, TH, a.INK, rx=14))
a.add(a.text(TX + 18, TY + 28, "TERMINAL DE PVE1", 13, SKY, a.MONO, 400, extra='letter-spacing="1.8"'))
L = [TY + 60 + i * 25 for i in range(14)]
at(a, tline(a, TX + 18, L[0], "# pveum user add tecnico@pve", MINT) + tline(a, TX + 18, L[1], "# pveum passwd tecnico@pve", MINT), 0, 100, still=1)
at(a, tline(a, TX + 18, L[3], "# pveum acl modify /", MINT) + tline(a, TX + 18, L[4], "  --user tecnico@pve", MINT) + tline(a, TX + 18, L[5], "  --role PVEAuditor", MINT), 26, 100, still=1)
p4 = (tline(a, TX + 18, L[7], "# pveum user permissions tecnico@pve", MINT)
      + tline(a, TX + 18, L[8], "/            Sys.Audit, ...", a.WHITE)
      + tline(a, TX + 18, L[9], "/nodes/pve1  Sys.Audit", a.WHITE)
      + tline(a, TX + 18, L[10], "/vms/100     VM.Audit", a.WHITE)
      + tline(a, TX + 18, L[11], "/storage/... Datastore.Audit", a.WHITE)
      + tline(a, TX + 18, L[13], "sin VM.PowerMgmt ni .Allocate", GOLD))
at(a, p4, 76, 100)
at(a, tline(a, TX + 18, L[12], "(salida resumida)", SKY), 76, 100)
at(a, tline(a, TX + 18, L[8], "lo asignado vale ahí y", SKY) + tline(a, TX + 18, L[9], "en todo lo que cuelga abajo", SKY), 52, 76, still=1)

status(a, 628, [
    (0, 25, "Un usuario por persona: así se sabe quién hizo cada cambio.", a.INK, 0),
    (25, 50, "El permiso es un par: un rol sobre una ruta del árbol.", a.BLUE, 0),
    (50, 75, "Asignado en /, alcanza todo; en /vms/100, solo esa VM.", a.OK, 1),
    (75, 100, "permissions es la prueba: confirmá que no tenga de más.", a.AMB, 0),
])

write(a, 11, "l1", "Un rol en / y el árbol entero lo hereda",
      "Animación en cuatro tiempos con el árbol de permisos de Proxmox (/, /nodes, /vms, /storage y debajo /nodes/pve1, /vms/100 y /storage/local-lvm), el usuario tecnico@pve y la terminal de pve1. "
      "1: pveum user add tecnico@pve y pveum passwd crean el usuario; existe, pero sin permisos no ve nada. "
      "2: pveum acl modify / --user tecnico@pve --role PVEAuditor asigna el rol en la raíz del árbol. "
      "3: con propagate, el rol se hereda hacia abajo y se pintan /nodes, /vms, /storage y cada nodo, VM y almacenamiento. "
      "4: pveum user permissions tecnico@pve muestra lo que resulta, en resumen: Sys.Audit, VM.Audit y Datastore.Audit en cada ruta, sin VM.PowerMgmt ni privilegios .Allocate: mirar sí, tocar no.",
      [8, 36, 62, 66, 92])
