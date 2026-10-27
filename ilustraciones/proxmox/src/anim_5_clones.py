"""Teoría lección 5: linked clone contra full clone."""
from _apmx import *

a = new(20, "Linked clone o full clone: de quién son los bloques")
a.steps(["Plantilla 9000: sus bloques quedan de solo lectura.",
         "Linked clone: instantáneo, apunta a la plantilla.",
         "Full clone: copia todo y queda independiente.",
         "Si la plantilla se borra: el linked se rompe."], still=2)
BX, S, G = 330, 80, 14
TY, LY, FY = 186, 330, 470
cx = [BX + i * (S + G) + S / 2 for i in range(6)]


def b(i, y, lab, fill, st, col, dash=False):
    x = BX + i * (S + G)
    d = 'stroke-dasharray="6 5"' if dash else ""
    return a.box(x, y, S, S, fill, st, rx=10, sw=2.5, extra=d) + a.text(x + S / 2, y + S / 2 + 8, lab, 22, col, a.MONO, 700, "middle")


a.add(a.text(48, TY + 36, "Plantilla 9000", 18, a.INK, a.SANS, 600) + a.text(48, TY + 60, "base de solo lectura", 15, a.GREY, a.SANS, 400))
a.add(a.text(48, LY + 36, "VM 201", 18, a.INK, a.SANS, 600) + a.text(48, LY + 60, "linked clone", 15, a.GREY, a.MONO, 600))
a.add(a.text(48, FY + 36, "VM 202", 18, a.INK, a.SANS, 600) + a.text(48, FY + 60, "full clone", 15, a.GREY, a.MONO, 600))
tpl = "".join(b(i, TY, l, a.NAVY2, a.NAVY2, "#FFFFFF") for i, l in enumerate("ABCD"))
at(a, tpl, 0, 75, 1)
at(a, "".join(b(i, TY, l, a.BADBG, a.BAD, a.BAD, True) for i, l in enumerate("ABCD")) + a.text(cx[4] + 10, TY + 48, "borrada", 18, a.BAD, a.SANS, 700), 75, 100, 0)
# linked: punteros a la plantilla y un bloque propio
lk = ""
for i in (0, 1, 3):
    lk += line(a, f"M{cx[i]} {LY}V{TY + S + 4}", a.CYAN, 3, "5 5")
    lk += b(i, LY, "↑", "#FFFFFF", a.CYAN, a.CYAN, True)
lk += b(2, LY, "C1", a.OKBG, a.OK, a.OK)
at(a, lk, 25, 75, 1)
at(a, chip(a, cx[4], LY + 26, "solo guarda lo que cambió", "cyan"), 25, 50, 0)
broken = ""
for i in (0, 1, 3):
    broken += line(a, f"M{cx[i]} {LY}V{TY + S + 4}", a.BAD, 3, "5 5") + b(i, LY, "?", a.BADBG, a.BAD, a.BAD, True)
broken += b(2, LY, "C1", a.OKBG, a.OK, a.OK)
at(a, broken + chip(a, cx[4], LY + 26, "roto: le faltan bloques", "bad"), 75, 100, 0)
# full: copia de a un bloque
for i, l in enumerate("ABCD"):
    at(a, b(i, FY, l, "#E5F0FB", a.BLUE, a.INK), 50 + i * 3, 100, 1)
at(a, chip(a, cx[4], FY + 26, "copia completa: tarda más", "info"), 50, 75, 1)
at(a, chip(a, cx[4], FY + 26, "sigue andando", "ok"), 75, 100, 0)
caption(a, 616, [(0, 25, "Al convertir la VM 9000 en plantilla, su disco pasa a ser una base que no se modifica.", None),
                 (25, 50, "Copy-on-write otra vez: el linked clone lee de la plantilla y escribe aparte lo suyo.", a.CYAN),
                 (50, 75, "El full clone copia todos los bloques: más lento y más disco, pero no depende de nadie.", None),
                 (75, 100, "Si la VM va a vivir más que la plantilla, full clone. Linked, para el laboratorio.", a.BAD)], still=2)
write(a, "5-t1.svg", "Linked clone o full clone: de quién son los bloques",
      "Animación en cuatro tiempos. 1: la plantilla 9000 tiene los bloques A, B, C y D, ahora de solo lectura. "
      "2: el linked clone, VM 201, se crea al instante: sus bloques A, B y D apuntan a la plantilla y solo guarda aparte lo que cambió, el bloque C1. "
      "3: el full clone, VM 202, copia los cuatro bloques uno por uno: tarda más pero queda independiente. "
      "4: si la plantilla se borra, al linked clone le faltan bloques y se rompe; el full clone sigue andando.")
