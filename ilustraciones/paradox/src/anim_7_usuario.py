"""Teoría lección 7: un código, sus opciones y las particiones que puede armar."""
from _apdx import *

a = new(20, "Un código, sus opciones, sus particiones")
a.steps(["El usuario 005 teclea su código en el teclado.",
         "La central busca sus opciones en [405]: solo partición 2.",
         "Se arma el taller. La casa sigue desarmada.",
         "El maestro, con particiones 1 y 2, arma las dos."], still=2)
a.add(card(a, 48, 190, 260, 300, "Teclado", None))
for r in range(3):
    for k in range(3):
        a.add(a.box(78 + k * 70, 260 + r * 56, 56, 42, a.WHITE, a.LINE, rx=8))
at(a, a.text(178, 470, "código del 005", 16, a.BLUE, a.MONO, 700, "middle"), 0, 75, 1)
at(a, a.text(178, 470, "código maestro", 16, a.BLUE, a.MONO, 700, "middle"), 75, 100, 0)
# opciones
a.add(card(a, 360, 190, 330, 300, "Opciones del usuario", None))
labs = ["1 part. 1", "2 part. 2", "3 anular", "4 Stay"]
for i, l in enumerate(labs):
    y = 240 + i * 56
    a.add(a.box(384, y, 282, 44, a.WHITE, a.LINE, rx=10) + a.text(404, y + 29, l, 17, a.INK, a.MONO, 600))
at(a, a.box(384, 296, 282, 44, a.CYAN, None, rx=10) + a.text(404, 325, "2 part. 2", 17, "#fff", a.MONO, 700), 25, 75, 1)
at(a, a.box(384, 240, 282, 44, a.CYAN, None, rx=10) + a.text(404, 269, "1 part. 1", 17, "#fff", a.MONO, 700)
   + a.box(384, 296, 282, 44, a.CYAN, None, rx=10) + a.text(404, 325, "2 part. 2", 17, "#fff", a.MONO, 700), 75, 100, 0)
at(a, a.text(384, 474, "[405] usuario 005", 15, a.GREY, a.MONO, 600), 0, 75, 1)
at(a, a.text(384, 474, "maestro del sistema", 15, a.GREY, a.MONO, 600), 75, 100, 0)
# particiones
for i, (t, y) in enumerate([("Partición 1 · casa", 190), ("Partición 2 · taller", 350)]):
    a.add(card(a, 740, y, 412, 140, t, None))
    a.add(a.group(chip(a, 764, y + 70, "desarmada", "grey"), a.show(0, 50 if i == 1 else 75), still=0))
at(a, chip(a, 764, 420, "armada", "ok"), 50, 100, 1)
at(a, chip(a, 764, 260, "desarmada", "grey"), 50, 75, 1)
at(a, chip(a, 764, 260, "armada", "ok"), 75, 100, 0)
at(a, line(a, "M690 330H740", a.OK, 4), 50, 100, 1)
caption(a, 600, [(0, 25, "El código no dice qué arma: lo dicen las opciones de ese usuario.", None),
                 (25, 50, "Opciones mínimas: sin anular, sin Stay, sin forzado si no los necesita.", None),
                 (50, 75, "Cada partición se arma y desarma por su lado.", a.OK),
                 (75, 100, "Una zona asignada a las dos (3) se arma cuando las dos están armadas.", None)], still=2)
write(a, "7-t1.svg", "Un código, sus opciones, sus particiones",
      "Animación en cuatro tiempos con un teclado, las opciones de usuario y las dos particiones. 1: el usuario 005 teclea su código. "
      "2: la central lee sus opciones en la sección 405: solo la opción 2, partición 2, está encendida. 3: se arma el taller, partición 2, y la casa sigue desarmada. "
      "4: el maestro, con particiones 1 y 2, arma las dos.")
