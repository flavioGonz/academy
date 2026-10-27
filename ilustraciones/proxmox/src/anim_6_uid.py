"""Teoría lección 6: contenedor no privilegiado contra privilegiado (mapeo de uid)."""
from _apmx import *

a = new(20, "Privilegiado o no: quién es root para el host")
a.steps(["Adentro del contenedor, un proceso corre como root.",
         "No privilegiado: el kernel lo traduce a uid 100000.",
         "Contra archivos del host, ese uid no tiene poder.",
         "Privilegiado: uid 0 es el root del host. Riesgo."], still=2)
# contenedor
a.add(card(a, 48, 190, 300, 290, "Contenedor 300", "LXC"))
a.add(a.text(68, 452, "root adentro: uid 0", 16, a.GREY, a.MONO, 600))
# kernel compartido
a.add(a.box(420, 190, 320, 290, a.INK, None, rx=16) + a.text(440, 226, "Kernel del host", 20, "#FFFFFF", a.HEAD, 600)
      + a.text(440, 250, "compartido por todos", 15, "#9FC3E3", a.MONO, 400))
for s, e, t, col, st in [(0, 25, "uid_map: 0 → 100000", "#9FC3E3", 0), (25, 75, "uid_map: 0 → 100000", "#7FE0B0", 1), (75, 100, "sin mapeo: 0 → 0", "#FFB4A6", 0)]:
    at(a, a.text(440, 450, t, 16, col, a.MONO, 700), s, e, st)
# archivos del host
a.add(card(a, 812, 190, 340, 290, "Archivos del host", "dueño: root (uid 0)"))
for j, f in enumerate(["/etc/pve", "/etc/shadow", "discos de otras VM"]):
    a.add(a.box(832, 270 + j * 52, 300, 40, a.SLATE, None, rx=8) + a.text(848, 296 + j * 52, f, 16, a.INK, a.MONO, 600))


def tok(lbl, kind):
    fg, bg = {"in": (a.INK, "#E5F0FB"), "ok": ("#FFFFFF", a.OK), "bad": ("#FFFFFF", a.BAD)}[kind]
    w = len(lbl) * 10 + 34
    return a.box(-w / 2, -20, w, 40, bg, a.BLUE if kind == "in" else None, rx=20, sw=2) + a.text(0, 7, lbl, 16, fg, a.MONO, 700, "middle")


a.add(a.group(tok("proceso · uid 0", "in"), a.move([(0, 198, 330), (25, 198, 330)]), a.show(0, 25), still=0))
a.add(a.group(tok("uid 100000", "ok"), a.move([(25, 198, 330), (30, 198, 330), (46, 580, 330), (50, 580, 330)]), a.show(25, 50), still=0))
a.add(a.group(tok("uid 100000", "ok"), a.move([(50, 580, 330), (54, 580, 330), (66, 760, 330), (75, 760, 330)]), a.show(50, 75), still=1))
at(a, chip(a, 812, 140 + 24, "permiso denegado", "ok") if False else a.box(812, 420, 340, 50, a.OKBG, a.OK, rx=12) + a.text(982, 452, "permiso denegado: host a salvo", 16, a.OK, a.SANS, 700, "middle"), 58, 75, 1)
a.add(a.group(tok("uid 0 = root", "bad"), a.move([(75, 198, 330), (79, 198, 330), (92, 760, 330), (100, 760, 330)]), a.show(75, 100), still=0))
at(a, a.box(812, 420, 340, 50, a.BADBG, a.BAD, rx=12) + a.text(982, 452, "si escapa, tiene todo", 16, a.BAD, a.SANS, 700, "middle"), 88, 100, 0)
caption(a, 600, [(0, 25, "Un contenedor comparte el kernel del host: no hay otro kernel en el medio, como en una VM.", None),
                 (25, 50, "No privilegiado: el root de adentro es, para el kernel, el usuario 100000 del host.", a.OK),
                 (50, 75, "Si un proceso se escapara, llega sin privilegios: no puede tocar lo del host.", a.OK),
                 (75, 100, "Privilegiado: el root de adentro es el root del host. Solo en entornos de confianza.", a.BAD)], still=2)
write(a, "6-t1.svg", "Privilegiado o no: quién es root para el host",
      "Animación en cuatro tiempos con un contenedor, el kernel del host compartido y los archivos del host, cuyo dueño es root. "
      "1: dentro del contenedor 300 un proceso corre como root, uid 0. "
      "2: en un contenedor no privilegiado, el kernel lo traduce con el uid_map a uid 100000. "
      "3: si ese proceso intentara tocar archivos del host como /etc/pve o discos de otras VM, recibe permiso denegado: el host queda a salvo. "
      "4: en un contenedor privilegiado no hay mapeo, el uid 0 de adentro es el root del host y, si el proceso escapara, tendría acceso a todo.")
