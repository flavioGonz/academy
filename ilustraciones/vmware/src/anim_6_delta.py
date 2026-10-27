"""Teoría lección 6: el snapshot congela el disco base y manda lo escrito a un delta; borrar es consolidar."""
from _avmw import *

a = new(20, "Qué pasa con el disco cuando sacás un snapshot")
a.steps(["Sin snapshot: la VM escribe directo en su disco base.",
         "Sacás el snapshot: el base queda congelado y nace el delta.",
         "Cada bloque que cambia va al delta, que crece mientras exista.",
         "Lo borrás: el delta se consolida en el base y desaparece."], still=2)

a.add(vmbox(a, 470, 184, 260, 66, "vm-prueba", "encendida"))
BX, BY = 120, 330
a.add(card(a, BX, BY, 400, 150, "vm-prueba-flat.vmdk", "disco base"))
# bloques del base
for k in range(10):
    a.add(a.box(BX + 20 + k * 37, BY + 84, 30, 40, "#E5F0FB", a.BLUE, rx=5, sw=1.5))
# candado (congelado) visible desde 25 a 75
lock = (f'<g transform="translate({BX + 340} {BY + 16})" fill="none" stroke="{a.GREY}" stroke-width="2.4">'
        '<rect x="0" y="12" width="28" height="22" rx="4"/><path d="M5 12V7a9 9 0 0 1 18 0v5"/></g>')
at(a, lock + chip(a, BX, BY + 166, "solo lectura", "grey"), 25, 75, 1)
# delta
DX = 680
delta = card(a, DX, BY, 400, 150, "vm-prueba-000001.vmdk", "delta", fill=a.AMBBG, stroke=a.AMB)
at(a, delta, 25, 88, 1)
# bloques que van al delta (crecen)
for k in range(5):
    t0 = 52 + k * 4
    blk = a.box(DX + 20 + k * 37, BY + 84, 30, 40, "#FFB020", a.AMB, rx=5, sw=1.5)
    a.add(a.group(blk, a.keyframes([(0, 0), (t0, 0), (t0 + 1, 1), (82, 1), (88, 0), (100, 0)]), still=1 if k < 3 else 0))
# escritura 1: al base
a.add(a.group('<circle r="11" fill="#FFB020" stroke="#fff" stroke-width="3"/>', a.move([(0, 600, 250), (4, 600, 250), (18, 340, BY + 104), (100, 340, BY + 104)]),
              a.keyframes([(0, 0), (3, 0), (4, 1), (19, 1), (21, 0), (100, 0)]), still=0))
# escrituras al delta
for k in range(3):
    t0 = 50 + k * 6
    a.add(a.group('<circle r="11" fill="#FFB020" stroke="#fff" stroke-width="3"/>', a.move([(0, 600, 250), (t0, 600, 250), (t0 + 4, DX + 35 + k * 37, BY + 104), (100, DX + 35 + k * 37, BY + 104)]),
                  a.keyframes([(0, 0), (t0 - 1, 0), (t0, 1), (t0 + 4, 1), (t0 + 5, 0), (100, 0)]), still=0))
at(a, a.arrow(f"M600 252 L{DX + 120} {BY - 6}", a.AMB, 3, "8 6") + a.text(DX + 150, 290, "lo escrito va al delta", 16, a.AMB, a.MONO, 600), 25, 75, 1)
# consolidación: el delta viaja al base
mv = a.move([(0, 0, 0), (76, 0, 0), (88, -560, 0), (100, -560, 0)])
cons = "".join(a.box(DX + 20 + k * 37, BY + 84, 30, 40, "#FFB020", a.AMB, rx=5, sw=1.5) for k in range(5))
a.add(a.group(cons, mv, a.keyframes([(0, 0), (75, 0), (76, 1), (88, 1), (90, 0), (100, 0)]), still=0))
at(a, chip(a, BX, BY + 166, "consolidado: un solo disco otra vez", "ok"), 88, 100, 0)
for k in range(5):
    at(a, a.box(BX + 20 + k * 37, BY + 84, 30, 40, "#FFE3A3", a.BLUE, rx=5, sw=1.5), 88, 100, 0)
caption(a, 590, [(0, 25, "Un disco, una escritura: nada que vigilar.", None),
                 (25, 50, "El base ya no se toca: sin él, el delta no sirve para nada.", None),
                 (50, 75, "Más horas = delta más grande = más lenta la VM y más largo el borrado.", a.AMB),
                 (75, 100, "Durante la consolidación no se cancela nada: se espera.", a.OK)], still=2)
write(a, "6-t1.svg", "Qué pasa con el disco cuando sacás un snapshot",
      "Animación en cuatro tiempos con una VM encima de su disco base, vm-prueba-flat.vmdk. 1: sin snapshot, una escritura de la VM va directo al disco base. "
      "2: al sacar el snapshot, el base queda congelado, en solo lectura, y aparece el delta vm-prueba-000001.vmdk. "
      "3: cada bloque que cambia se escribe en el delta, que crece mientras el snapshot exista. "
      "4: al borrar el snapshot, los bloques del delta se consolidan en el disco base, el delta desaparece y queda un solo disco otra vez.")
