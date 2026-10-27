"""Teoría lección 3: snapshot copy-on-write en LVM-thin o ZFS."""
from _apmx import *

a = new(20, "Snapshot copy-on-write: congelar sin copiar")
a.steps(["El disco de la VM: solo ocupan los bloques escritos.",
         "Snapshot: anota qué bloques hay. No copia nada.",
         "La VM cambia B: lo nuevo va a otro bloque, B queda.",
         "Rollback: el disco vuelve a A B C D. B2 se descarta."], still=2)
BX, BY, S, G = 300, 290, 92, 16
SY, VY, SH = 184, 452, 46  # fila del snapshot (arriba) y del disco (abajo)
cx = [BX + i * (S + G) + S / 2 for i in range(7)]


def blk(i, lab, kind, y=BY):
    fill, st, col = {"data": ("#E5F0FB", a.BLUE, a.INK), "new": (a.OKBG, a.OK, a.OK), "free": ("#FFFFFF", a.LINE, a.GREY),
                     "bad": (a.BADBG, a.BAD, a.BAD)}[kind]
    x = BX + i * (S + G)
    dash = 'stroke-dasharray="6 5"' if kind == "free" else ""
    return a.box(x, y, S, S, fill, st, rx=12, sw=2.5, extra=dash) + (a.text(x + S / 2, y + S / 2 + 9, lab, 26, col, a.MONO, 700, "middle") if lab else "")


def row(y, targets, color, bg):
    """Fila de punteros: casillero i apunta al bloque targets[i]."""
    g = ""
    for i, t in enumerate(targets):
        x = BX + i * (S + G)
        y1, y2 = (y + SH, BY) if y < BY else (y, BY + S)
        g += line(a, f"M{cx[i]} {y1}L{cx[t]} {y2 + (-4 if y < BY else 4)}", color, 3, "5 5")
        g += a.box(x, y, S, SH, bg, color, rx=10, sw=2) + a.text(x + S / 2, y + 30, "AB2CD"[0] if False else ["A", "B", "C", "D", "B2"][t], 18, color, a.MONO, 700, "middle")
    return g


a.add(a.text(48, BY + 44, "Bloques", 18, a.INK, a.SANS, 600))
a.add(a.text(48, BY + 66, "en el pool", 15, a.GREY, a.SANS, 400))
a.add(a.text(48, SY + 30, "Snapshot", 18, a.AMB, a.SANS, 600))
a.add(a.text(48, VY + 30, "Disco de la VM", 18, a.BLUE, a.SANS, 600))
for i, l in enumerate("ABCD"):
    a.add(blk(i, l, "data"))
for i in range(4, 7):
    a.add(blk(i, "", "free"))
a.add(a.text(cx[5] + 54, BY - 14, "libres: no ocupan", 15, a.GREY, a.SANS, 600, "middle"))
at(a, blk(4, "B2", "new"), 50, 75, still=1)
at(a, blk(4, "B2", "bad") + a.text(cx[4], BY - 14, "descartado", 15, a.BAD, a.SANS, 700, "middle"), 75, 92, still=0)
# disco
at(a, row(VY, [0, 1, 2, 3], a.BLUE, "#FFFFFF"), 0, 50, 0)
at(a, row(VY, [0, 4, 2, 3], a.BLUE, "#FFFFFF"), 50, 75, 1)
at(a, row(VY, [0, 1, 2, 3], a.BLUE, "#FFFFFF"), 75, 100, 0)
# snapshot
at(a, a.text(BX, SY + 30, "todavía no hay", 17, a.GREY, a.SANS, 500), 0, 25, 0)
at(a, row(SY, [0, 1, 2, 3], a.AMB, a.AMBBG), 25, 100, 1)
for s_, e_, t_, k_, st_ in [(25, 50, "instantáneo: 0 bytes copiados", "amb", 0), (50, 75, "conserva B", "amb", 1), (75, 100, "el disco vuelve a esto", "ok", 0)]:
    at(a, chip(a, 740, SY + 8, t_, k_), s_, e_, st_)
caption(a, 620, [(0, 25, "En LVM-thin y ZFS el disco ocupa lo escrito: 32 GB asignados con 3 GB de datos ocupan 3 GB.", None),
                 (25, 50, "El snapshot es una marca: los bloques que ya estaban quedan protegidos, sin copiarlos.", a.AMB),
                 (50, 75, "Copy-on-write: el cambio se escribe aparte. El snapshot ocupa solo lo que cambió desde entonces.", a.OK),
                 (75, 100, "Todo vive en el mismo pool: si ese disco muere, el snapshot se va con él. No es un backup.", a.BAD)], still=2)
write(a, "3-t1.svg", "Snapshot copy-on-write: congelar sin copiar",
      "Animación en cuatro tiempos de un snapshot copy-on-write. 1: el disco de la VM usa los bloques A, B, C y D del pool; los bloques libres no ocupan espacio. "
      "2: al sacar el snapshot no se copia nada: solo se anota que A, B, C y D pertenecen al snapshot. "
      "3: la VM modifica B; el dato nuevo se escribe en un bloque aparte, B2, y el disco pasa a ver A, B2, C y D, mientras el snapshot conserva B. "
      "4: con un rollback el disco vuelve a A, B, C y D y B2 se descarta. Como todo vive en el mismo pool, un snapshot no reemplaza a un backup.")
