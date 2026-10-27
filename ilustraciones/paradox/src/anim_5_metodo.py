"""Teoría lección 5: espera de sección, visualización y salida sin guardar."""
from _apdx import *

a = new(20, "Adentro de programación: mirar antes de escribir")
a.steps(["ENTER + código de instalador: la central espera una sección.",
         "Tecleás 710: entrás a la sección del retardo de entrada 1.",
         "ENTER antes de cargar: muestra el valor, dígito por dígito.",
         "CLEAR: volvés a la espera de sección sin guardar nada."], still=2)
# pantalla del teclado
a.add(a.box(48, 190, 520, 300, "#F1F4F7", "#C2D4E6", rx=20, sw=2))
a.add(a.box(78, 220, 460, 130, "#0B3A66", None, rx=10))
for s, e, txt, sub, still in [(0, 25, "sección: _ _ _", "ARM y STAY titilan", 0), (25, 50, "sección 710", "esperando el dato", 0),
                              (50, 75, "710 = 0 4 5", "45 s · sin cambios", 1), (75, 100, "sección: _ _ _", "nada se guardó", 0)]:
    at(a, a.text(100, 282, txt, 32, "#9FE3F7", a.MONO, 700) + a.text(100, 326, sub, 17, "#9FC3E3", a.SANS, 600), s, e, still)
keys = [("ENTER", 0), ("7", 25), ("1", 27), ("0", 29), ("ENTER", 50), ("CLEAR", 75)]
for i, (k, t) in enumerate([("ENTER", 0), ("710", 25), ("ENTER", 50), ("CLEAR", 75)]):
    x = 78 + i * 116
    a.add(a.box(x, 384, 100, 56, a.WHITE, "#C2D4E6", rx=10, sw=2) + a.text(x + 50, 419, k, 18, a.INK, a.MONO, 600, "middle"))
    a.add(a.group(a.box(x, 384, 100, 56, a.CYAN, None, rx=10) + a.text(x + 50, 419, k, 18, "#fff", a.MONO, 700, "middle"), a.show(t, t + 25), still=1 if i == 2 else 0))
# panel derecho
a.add(card(a, 612, 190, 540, 300, "Tres tipos de dato", None))
rows = [("Decimal", "000 a 255", "tiempos: 045 = 45 s"), ("Hexadecimal", "0 vale A", "ID, abonado, claves"), ("Opciones", "1 a 8", "prender y apagar")]
for i, (t, v, d) in enumerate(rows):
    y = 260 + i * 72
    a.add(a.text(636, y, t, 18, a.INK, a.SANS, 600))
    a.add(a.text(800, y, v, 17, a.BLUE, a.MONO, 600))
    a.add(a.text(636, y + 26, d, 15, a.GREY, a.SANS, 400))
caption(a, 600, [(0, 25, "Para entrar, las particiones desarmadas y StayD apagado.", None),
                 (25, 50, "Si ahora tecleás un número, lo estás escribiendo.", a.AMB),
                 (50, 75, "Primero ENTER: así ves lo que había antes de tocar.", a.OK),
                 (75, 100, "CLEAR sale de la sección sin guardar lo que tecleaste.", None)], still=2)
write(a, "5-t1.svg", "Adentro de programación: mirar antes de escribir",
      "Animación en cuatro tiempos de la pantalla de un teclado. 1: con ENTER y el código de instalador la central espera una sección, con ARM y STAY titilando. "
      "2: se teclea 710 y se entra a la sección del retardo de entrada 1. 3: ENTER antes de cargar muestra el valor 045, 45 segundos, sin cambiarlo. "
      "4: CLEAR vuelve a la espera de sección sin guardar nada. Al costado, los tres tipos de dato: decimal de 000 a 255, hexadecimal con el 0 como A y opciones de 1 a 8.")
