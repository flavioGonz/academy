#!/usr/bin/env python3
"""Lección 1 (Moverse sin miedo), Resumen: un solo árbol desde /. Una ruta del sistema se lee del disco raíz;
/srv/datos es un punto de montaje y lo que cuelga de ahí vive en el segundo disco; findmnt dice qué disco hay
detrás de cada carpeta. Fuentes: teoría de la lección (cada disco extra se monta en una carpeta, como /srv/datos)
y findmnt(8) (columnas TARGET, SOURCE, FSTYPE, OPTIONS)."""
from _anims_lnx_rl import *

a = nueva(24, "LINUX · ÁRBOL ÚNICO · POR DENTRO", "Un solo árbol: el segundo disco aparece como carpeta")
a.steps([
    "La ruta /etc/ssh/sshd_config se lee del disco del sistema.",
    "/srv/datos es un punto de montaje: ahí cuelga el segundo disco.",
    "/srv/datos/obra/plano.pdf cruza al otro disco sin que lo notes.",
    "findmnt dice qué disco hay detrás de cada carpeta.",
], still=2)

# ---- discos a la derecha
DA, DB = a.BLUE, a.CYAN
a.add(dev(a, 760, 176, 392, 112, "Disco del sistema", "/dev/sda2 · ext4", "server", sub2="montado en /", stroke=DA, sw=3))
a.add(dev(a, 760, 316, 392, 112, "Disco de datos", "/dev/sdb1 · ext4", "server", sub2="montado en /srv/datos", stroke=DB, sw=3))

# ---- árbol
NODES = {  # nombre: (x, y, disco)
    "/": (70, 186, "A"), "etc": (120, 232, "A"), "ssh": (170, 278, "A"), "sshd_config": (220, 324, "A"),
    "var": (120, 370, "A"), "srv": (120, 416, "A"), "datos": (170, 462, "B"), "obra": (220, 508, "B"), "plano.pdf": (270, 554, "B"),
}
PARENT = {"etc": "/", "ssh": "etc", "sshd_config": "ssh", "var": "/", "srv": "/", "datos": "srv", "obra": "datos", "plano.pdf": "obra"}


def nbox(name, color, fill=None, sw=2):
    x, y, _ = NODES[name]
    w = int(len(name) * 10 + 28)
    return a.box(x, y - 18, w, 34, fill or a.WHITE, color, rx=10, sw=sw) + a.text(x + 14, y + 5, name, 16, a.INK, a.MONO, 600)


for ch, p in PARENT.items():
    px, py, _ = NODES[p]
    cx, cy, d = NODES[ch]
    a.add(camino(f"M{px + 16} {py + 16} V{cy} H{cx}", DB if d == "B" and ch != "datos" else "#C2D4E6", 2.5))
for n, (x, y, d) in NODES.items():
    a.add(nbox(n, DA if d == "A" else DB))
a.add(a.text(410, 186, "cada caja: una carpeta o un archivo", 15, a.GREY, a.SANS, 500))
a.add(a.text(410, 210, "azul: vive en sda2 · celeste: vive en sdb1", 15, a.GREY, a.SANS, 500))

# punto de montaje (paso 2 en adelante)
dx, dy, _ = NODES["datos"]
en(a, a.box(dx - 6, dy - 24, 86, 46, "none", a.AMB, rx=13, sw=3), 25, 100, still=1)
en(a, a.pill(dx + 96, dy - 15, "punto de montaje", a.AMB, a.AMBBG, 15, 30), 25, 100, still=1)

# enlaces a los discos
en(a, camino("M360 324 C 540 324, 600 232, 760 232", DA, 3, "8 6"), 10, 100, still=1)
en(a, camino("M440 462 C 600 462, 620 372, 760 372", DB, 3, "8 6"), 30, 100, still=1)

# recorrido 1: / → etc → ssh → sshd_config
def ruta(names):
    pts = []
    for n in names:
        x, y, _ = NODES[n]
        pts.append((x - 16, y))
    return pts


viaje(a, "", ruta(["/", "etc", "ssh", "sshd_config"]), 3, 18, inner=f'<circle r="10" fill="{DA}" stroke="#FFFFFF" stroke-width="3"/>', hold=6)
en(a, a.text(410, 372, "/etc/ssh/sshd_config", 16, DA, a.MONO, 700) + a.text(410, 396, "se lee de sda2", 15, a.TXT, a.SANS, 500), 8, 50)

# recorrido 2: / → srv → datos → obra → plano.pdf
viaje(a, "", ruta(["/", "srv"]), 52, 58, inner=f'<circle r="10" fill="{DA}" stroke="#FFFFFF" stroke-width="3"/>', hold=0)
viaje(a, "", ruta(["srv", "datos", "obra", "plano.pdf"]), 58.5, 70, inner=f'<circle r="10" fill="{DB}" stroke="#FFFFFF" stroke-width="3"/>', hold=30)
en(a, a.text(410, 540, "/srv/datos/obra/plano.pdf", 16, DB, a.MONO, 700) + a.text(410, 564, "se lee de sdb1: la ruta no avisa", 15, a.TXT, a.SANS, 500), 62, 100, still=1)

px_, py_, _ = NODES["plano.pdf"]
fijo(a, f'<circle cx="{px_ - 16}" cy="{py_}" r="10" fill="{DB}" stroke="#FFFFFF" stroke-width="3"/>')
# terminal findmnt (paso 4)
T = tterm(a, 760, 452, 392, 150, "TERMINAL · SOLO LEE")
T += trow(a, 760, 504, "$ findmnt /srv/datos", 15)
T += trow(a, 760, 534, ("TARGET     SOURCE    FSTYPE", T_COM), 15)
T += trow(a, 760, 562, ("/srv/datos /dev/sdb1 ext4", T_OK), 15)
T += trow(a, 760, 588, ("(ejemplo: el disco de tu equipo varía)", T_COM), 14)
en(a, T, 76, 100)
fijo(a, a.box(760, 452, 392, 150, a.WHITE, a.LINE, rx=12) + a.text(780, 490, "No hay disco D:", 18, a.INK, a.HEAD, 600)
     + a.text(780, 518, "el segundo disco es una carpeta más.", 16, a.TXT, a.SANS, 500)
     + a.text(780, 548, "findmnt /srv/datos te dice cuál es.", 16, a.BLUE, a.SANS, 600))

narr(a, [
    (0, 25, "Todo arranca en /: no hay disco C ni D.", None),
    (25, 50, "Montar un disco es colgarlo de una carpeta vacía: /srv/datos.", a.AMB),
    (50, 75, "Para el usuario es la misma ruta; el kernel sabe que cambió de disco.", None),
    (75, 100, "Antes de borrar o llenar algo, findmnt o df -h te dicen en qué disco cae.", a.OK),
], still_idx=2)

escribir(a, "1-r1", "Un solo árbol: el segundo disco aparece como carpeta",
         "Animación en cuatro tiempos. A la izquierda, el árbol de carpetas desde la raíz: /, etc, ssh, sshd_config, var, srv, datos, obra y plano.pdf. "
         "Las cajas en azul viven en el disco del sistema, /dev/sda2 montado en /; las celestes, en el disco de datos, /dev/sdb1 montado en /srv/datos. "
         "1: un punto recorre /etc/ssh/sshd_config y una línea punteada lo une al disco del sistema. "
         "2: la carpeta datos se marca en ámbar como punto de montaje y una línea la une al disco de datos. "
         "3: el punto recorre /srv/datos/obra/plano.pdf y, al pasar por datos, cambia de color: el archivo se lee del segundo disco y la ruta no lo avisa. "
         "4: una terminal muestra findmnt /srv/datos con TARGET /srv/datos, SOURCE /dev/sdb1 y FSTYPE ext4, como ejemplo.",
         [8, 35, 66, 88])
