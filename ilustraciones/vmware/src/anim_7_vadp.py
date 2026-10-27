"""Teoría lección 7: el ciclo de un job de backup con VADP y CBT, y la restauración aislada."""
from _avmw import *

a = new(24, "Un job de backup por dentro: snapshot, copia, borrado")
a.steps(["El producto de backup pide por la API un snapshot de la VM.",
         "CBT dice qué bloques cambiaron: se copian solo esos al repositorio.",
         "Terminada la copia, el job borra el snapshot.",
         "La prueba: restaurar con otro nombre en una red aislada."], still=1)

a.add(card(a, 48, 180, 520, 330, "Host ESXi", None, dark=True))
a.add(vmbox(a, 76, 236, 220, 60, "srv-video", "VM en producción"))
# disco con bloques
a.add(a.box(76, 330, 460, 150, "#0B3A66", "#4E7396", rx=12) + a.text(96, 360, "disco de srv-video", 16, "#FFFFFF", a.SANS, 600))
CH = {1, 4, 7}
for k in range(10):
    a.add(a.box(96 + k * 43, 384, 34, 44, "#E5F0FB", a.BLUE, rx=5, sw=1.5))
for k in CH:
    at(a, a.box(96 + k * 43, 384, 34, 44, "#FFB020", a.AMB, rx=5, sw=2), 25, 50, 1)
at(a, a.text(96, 458, "CBT: 3 bloques cambiaron desde el último backup", 14, "#FFD27A", a.MONO, 600), 25, 50, 1)
# snapshot
snap = a.box(330, 236, 206, 60, a.AMBBG, a.AMB, rx=12, sw=2) + a.text(348, 262, "snapshot del job", 15, a.AMB, a.SANS, 600) + a.text(348, 283, "base congelado", 13, a.AMB, a.MONO)
at(a, snap, 4, 50, 1)
at(a, chip(a, 330, 196, "borrado", "ok"), 52, 75, 0)
# servidor de backup
a.add(card(a, 700, 180, 452, 130, "Producto de backup", "Veeam, Nakivo, Altaro u otro"))
a.add(card(a, 700, 340, 452, 170, "Repositorio", "copias anteriores + incremental"))
for k in range(3):
    a.add(a.box(724 + k * 50, 420, 40, 60, "#E5F0FB", a.BLUE, rx=5, sw=1.5))
# pedido de snapshot
at(a, a.arrow("M700 240 C620 240 600 260 540 262", a.BLUE, 3) + a.text(590, 226, "VADP", 15, a.BLUE, a.MONO, 700), 0, 25, 0)
# bloques que viajan
for i, k in enumerate(sorted(CH)):
    t0 = 28 + i * 5
    mv = a.move([(0, 113 + k * 43, 406), (t0, 113 + k * 43, 406), (t0 + 6, 900 + i * 50, 450), (100, 900 + i * 50, 450)])
    a.add(a.group('<rect x="-17" y="-22" width="34" height="44" rx="5" fill="#FFB020" stroke="#B26A00" stroke-width="2"/>', mv,
                  a.keyframes([(0, 0), (t0 - 1, 0), (t0, 1), (t0 + 6, 1), (99, 1), (100, 0)]), still=0))
at(a, chip(a, 700, 520, "NBD, HotAdd o SAN", "grey"), 25, 50, 1)
# fijo: bloques ya en el repositorio
a.add(a.group("".join(f'<rect x="{883 + i * 50}" y="428" width="34" height="44" rx="5" fill="#FFB020" stroke="#B26A00" stroke-width="2"/>' for i in range(3)), a.keyframes([(0, 0), (100, 0)]), still=1))
# restauración aislada
rest = a.box(48, 530, 520, 70, a.OKBG, a.OK, rx=12, sw=2.5) + a.text(70, 562, "srv-prueba-restore", 17, a.OK, a.MONO, 700) + a.text(70, 586, "port group Restore-Aislado, sin uplinks", 14, a.OK, a.MONO)
at(a, rest, 78, 100, 0)
at(a, a.arrow("M760 512 C720 560 640 566 572 566", a.OK, 3), 78, 100, 0)
caption(a, 640, [(0, 25, "El snapshot congela el disco para copiar algo coherente mientras la VM sigue andando.", None),
                 (25, 50, "Con CBT el incremental copia lo cambiado, no el disco entero.", None),
                 (50, 75, "Si el job falla antes de este paso, el snapshot queda colgado: por eso se revisa.", a.AMB),
                 (75, 100, "Un backup cuenta cuando arrancó, se verificó y sabés cuánto tardó.", a.OK)], still=1)
write(a, "7-t1.svg", "Un job de backup por dentro: snapshot, copia, borrado",
      "Animación en cuatro tiempos con un host ESXi que tiene la VM srv-video y su disco, y a la derecha el producto de backup y el repositorio. "
      "1: el producto de backup pide por la API de vSphere (VADP) un snapshot de la VM, que congela el disco base. "
      "2: Changed Block Tracking marca los tres bloques que cambiaron desde el último backup y solo esos viajan al repositorio, por NBD, HotAdd o SAN. "
      "3: terminada la copia, el job borra el snapshot; si el job fallara antes, el snapshot quedaría colgado. "
      "4: la prueba: la VM se restaura como srv-prueba-restore en el port group Restore-Aislado, sin uplinks.")
