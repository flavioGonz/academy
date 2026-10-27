"""Teoría lección 10: migración en vivo (copia de RAM en pasadas, páginas sucias)."""
from _apmx import *

a = new(24, "Migración en vivo: la RAM viaja mientras la VM corre")
a.steps(["En pve2 arranca un QEMU vacío, en pausa, esperando datos.",
         "Primera pasada: se copia toda la RAM. La VM sigue escribiendo.",
         "Otra pasada: solo las páginas que cambiaron. Cada vez menos.",
         "Pausa de milisegundos, va el resto y la VM sigue en pve2."], still=2)
# hosts
a.add(card(a, 48, 180, 420, 370, "pve1 · origen", None, dark=True))
a.add(card(a, 732, 180, 420, 370, "pve2 · destino", None, dark=True))
GX = [(48 + 24, 732 + 24)]
N = 12  # páginas de RAM en grilla 4x3
cell, gap = 80, 12


def grid(x0, kinds, y0=240):
    out = ""
    st = {"ram": ("#E5F0FB", a.BLUE), "dirty": (a.AMBBG, a.AMB), "empty": ("#0B3A66", "#4E7396"), "ok": (a.OKBG, a.OK)}
    for i, k in enumerate(kinds):
        r, cc = divmod(i, 4)
        f, s = st[k]
        out += a.box(x0 + 24 + cc * (cell + gap), y0 + r * (cell - 14 + gap), cell, cell - 14, f, s, rx=8, sw=2)
    return out


# origen: RAM de la VM
at(a, grid(48, ["ram"] * 12) + a.text(72, 526, "VM 100 corriendo", 16, "#7FE0B0", a.SANS, 700), 0, 25, 0)
dirty1 = [2, 5, 6, 9]
dirty2 = [6]
at(a, grid(48, ["dirty" if i in dirty1 else "ram" for i in range(12)]) + a.text(72, 526, "4 páginas sucias", 16, "#FFD38A", a.SANS, 700), 25, 50, 0)
at(a, grid(48, ["dirty" if i in dirty2 else "ram" for i in range(12)]) + a.text(72, 526, "1 página sucia", 16, "#FFD38A", a.SANS, 700), 50, 75, 1)
at(a, grid(48, ["empty"] * 12) + a.text(72, 526, "proceso terminado", 16, "#9FC3E3", a.SANS, 700), 75, 100, 0)
# destino
at(a, grid(732, ["empty"] * 12) + a.text(756, 526, "QEMU en pausa (incoming)", 16, "#9FC3E3", a.SANS, 700), 0, 25, 0)
at(a, grid(732, ["dirty" if i in dirty1 else "ram" for i in range(12)]) + a.text(756, 526, "4 páginas ya viejas", 16, "#9FC3E3", a.SANS, 700), 25, 50, 0)
at(a, grid(732, ["dirty" if i in dirty2 else "ram" for i in range(12)]) + a.text(756, 526, "falta 1 página", 16, "#9FC3E3", a.SANS, 700), 50, 75, 1)
at(a, grid(732, ["ok"] * 12) + a.text(756, 526, "VM 100 corriendo acá", 16, "#7FE0B0", a.SANS, 700), 75, 100, 0)
# flechas de copia
for s, e, lab, k, stl in [(25, 50, "12 páginas", "info", 0), (50, 75, "4 páginas", "amb", 1), (75, 100, "1 página + estado", "ok", 0)]:
    at(a, a.arrow("M480 360 H720", a.CYAN, 5) + chip(a, 600, 314, lab, k, anchor="middle"), s, e, stl)
at(a, chip(a, 600, 400, "pausa < 1 s", "bad", anchor="middle"), 78, 92, 0)
caption(a, 618, [(0, 25, "Con disco compartido, el disco no se mueve: solo falta la memoria y el estado de los dispositivos.", None),
                 (25, 50, "Mientras se copia, la VM sigue trabajando: lo que escribe se marca como sucio.", a.AMB),
                 (50, 75, "Cada pasada manda solo lo sucio. Se repite hasta que lo que falta se manda en milisegundos.", a.AMB),
                 (75, 100, "Se pausa el origen, va lo último y arranca el destino: los usuarios no notan el corte.", a.OK)], still=2)
write(a, "10-t1.svg", "Migración en vivo: la RAM viaja mientras la VM corre",
      "Animación en cuatro tiempos de una migración en vivo de la VM 100 de pve1 a pve2, con la RAM dibujada como doce páginas. "
      "1: en pve2 arranca un proceso QEMU en pausa que espera los datos; el disco está en almacenamiento compartido y no viaja. "
      "2: primera pasada: se copian las doce páginas mientras la VM sigue escribiendo, y cuatro quedan marcadas como sucias. "
      "3: la segunda pasada manda solo esas cuatro y queda una sucia; cada pasada es más chica. "
      "4: el origen se pausa menos de un segundo, se manda la última página y el estado de los dispositivos, y la VM sigue corriendo en pve2.")
