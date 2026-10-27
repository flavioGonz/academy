"""Teoría lección 8: trozos deduplicados en PBS, prune y garbage collection."""
from _apmx import *

a = new(20, "PBS: trozos compartidos, prune y garbage collection")
a.steps(["Primer backup: el disco se parte en trozos y se guardan todos.",
         "Segundo backup: solo sube lo nuevo; lo repetido se reutiliza.",
         "Prune borra el índice del lunes: los trozos siguen ahí.",
         "GC borra lo que nadie usa, pasado el día de gracia."], still=1)
CX = {k: 420 + i * 150 for i, k in enumerate("abcde")}
CY = 470


def chunk(k, kind):
    fill, st, col = {"ok": (a.OKBG, a.OK, a.OK), "data": ("#E5F0FB", a.BLUE, a.INK), "amb": (a.AMBBG, a.AMB, a.AMB), "bad": (a.BADBG, a.BAD, a.BAD)}[kind]
    x = CX[k] - 50
    return a.box(x, CY, 100, 76, fill, st, rx=12, sw=2.5) + a.text(CX[k], CY + 48, k, 26, col, a.MONO, 700, "middle")


def index(y, name, ks, color, cross=False):
    g = a.box(48, y, 250, 64, "#FFFFFF", color, rx=12, sw=2) + a.text(68, y + 28, name, 18, a.INK, a.SANS, 600) + a.text(68, y + 50, "índice: " + " ".join(ks), 15, a.GREY, a.MONO, 600)
    for k in ks:
        g += line(a, f"M298 {y + 32} C 360 {y + 32}, {CX[k]} {CY - 120}, {CX[k]} {CY - 4}", color, 2.5, "6 5")
    if cross:
        g = a.box(48, y, 250, 64, a.BADBG, a.BAD, rx=12, sw=2, extra='stroke-dasharray="6 5"') + a.text(68, y + 28, name, 18, a.BAD, a.SANS, 600) + a.text(68, y + 50, "borrado por prune", 15, a.BAD, a.MONO, 600)
    return g


a.add(a.text(48, CY + 34, "Datastore", 18, a.INK, a.SANS, 600) + a.text(48, CY + 58, ".chunks", 15, a.GREY, a.MONO, 600))
# índices
at(a, index(190, "Backup lunes", "abcd", a.BLUE), 0, 50, 1)
at(a, index(190, "Backup lunes", "abcd", a.BAD, cross=True), 50, 100, 0)
at(a, index(300, "Backup martes", "abce", a.OK), 25, 100, 1)
# trozos
for k in "abc":
    at(a, chunk(k, "data"), 0, 100, 1)
at(a, chunk("d", "data"), 0, 50, 1)
at(a, chunk("d", "amb") + a.text(CX["d"], CY + 104, "sin dueño", 15, a.AMB, a.SANS, 700, "middle"), 50, 80, 0)
at(a, chunk("d", "bad") + a.text(CX["d"], CY + 104, "liberado", 15, a.BAD, a.SANS, 700, "middle"), 80, 92, 0)
at(a, chunk("e", "ok") + a.text(CX["e"], CY + 104, "lo único nuevo", 15, a.OK, a.SANS, 700, "middle"), 25, 50, 1)
at(a, chunk("e", "ok"), 50, 100, 0)
at(a, chip(a, 760, 200, "4 trozos escritos", "info"), 0, 25, 0)
at(a, chip(a, 760, 200, "martes: 1 trozo nuevo, 3 reutilizados", "ok"), 25, 50, 1)
at(a, chip(a, 760, 200, "prune no libera espacio", "amb"), 50, 75, 0)
at(a, chip(a, 760, 200, "GC: 24 h y 5 min de gracia", "bad"), 75, 100, 0)
caption(a, 628, [(0, 25, "PBS guarda cada backup como un índice que apunta a trozos del datastore.", None),
                 (25, 50, "Deduplicación: el martes el índice reutiliza a, b y c. Por eso 30 backups no ocupan 30 veces el disco.", a.OK),
                 (50, 75, "Prune borra solo el índice. El trozo d queda en disco hasta que pase la garbage collection.", a.AMB),
                 (75, 100, "GC revisa qué trozos ya no usa ningún índice y los borra pasado el plazo de gracia.", a.BAD)], still=1)
write(a, "8-t1.svg", "PBS: trozos compartidos, prune y garbage collection",
      "Animación en cuatro tiempos de un datastore de Proxmox Backup Server. 1: el backup del lunes parte el disco en los trozos a, b, c y d y los guarda; su índice apunta a los cuatro. "
      "2: el backup del martes solo sube el trozo e, que es nuevo, y reutiliza a, b y c: eso es la deduplicación. "
      "3: prune borra el índice del lunes, pero los trozos siguen en disco y d queda sin dueño. "
      "4: la garbage collection, pasado el plazo de gracia de 24 horas y 5 minutos, borra d, que ya no usa ningún índice, y recién ahí se libera espacio.")
