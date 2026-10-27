"""Teoría de Zonas y reglas: de la causa al efecto con reglas y contadores."""
from _anim_bi import *

caps = ["El detector 3.4 entra en alarma: evento del grupo 3.",
        "La regla por evento del grupo 3 activa las sirenas del piso.",
        "Llega un segundo, el 3.7: el contador marca 2 y actúa su regla.",
        "Panel y BMS muestran la misma dirección lógica, con ubicación."]
a = new(24, "Reglas", "Del evento al efecto: reglas y contadores", caps, still=3)

for (y, n) in ((230, "3.4"), (380, "3.7")):
    a.add(a.box(48, y - 50, 230, 100, a.WHITE, a.LINE, rx=14, sw=2))
    a.add(det(a, 100, y, 28))
    a.add(a.text(150, y + 8, n, 24, a.INK, a.MONO, 600))
vis(a, led(a, 100, 230, a.BAD, 6), 0, 3)
vis(a, led(a, 100, 380, a.BAD, 6), 2, 3)
a.add(card(a, 420, 180, 330, 100, "Regla por evento", "alarma del grupo 3"))
a.add(card(a, 420, 330, 330, 100, "Contador grupo 3", "dos equipos en alarma"))
a.add(card(a, 880, 180, 270, 100, "Sirenas piso 3", "efecto"))
a.add(card(a, 880, 330, 270, 100, "Efecto de 2 equipos", "según la matriz"))
a.add(line(a, 280, 230, 416, 230, a.LINE, 3)); a.add(line(a, 280, 380, 416, 380, a.LINE, 3)); a.add(line(a, 280, 250, 416, 360, a.LINE, 2))
a.add(line(a, 752, 230, 876, 230, a.LINE, 3)); a.add(line(a, 752, 380, 876, 380, a.LINE, 3))
s0, s1 = ph(a, 0)
token(a, "evento 3.4", [(s0 + 2, 290, 200), (s0 + 14, 345, 200), (s1 - 1, 345, 200)], bg=a.BAD)
vis(a, a.box(420, 180, 330, 100, "none", a.BLUE, rx=14, sw=4), 1, 3)
vis(a, a.box(880, 180, 270, 100, "none", a.BAD, rx=14, sw=4) + a.pill(1146, 196, "activas", a.BAD, a.BADBG, anchor="end"), 1, 3)
vis(a, a.pill(744, 346, "2", a.WHITE, a.BLUE, size=17, anchor="end"), 2, 3)
vis(a, a.pill(744, 346, "1", a.WHITE, a.GREY, size=17, anchor="end"), 0, 1)
vis(a, a.box(880, 330, 270, 100, "none", a.BAD, rx=14, sw=4), 2, 3)
# mensaje
a.add(a.box(48, 480, 1104, 110, a.INK, rx=16))
a.add(a.text(72, 516, "MENSAJE DEL PANEL Y DEL BMS", 14, "#9FC3E3", a.MONO, 600))
vis(a, a.text(72, 560, "Alarma · detector óptico · sala de reuniones piso 3 · 3.4", 22, a.WHITE, a.MONO, 600), 3)
vis(a, a.text(72, 560, "esperando eventos...", 20, "#9FC3E3", a.MONO), 0, 2, still=0)
a.add(a.text(48, 632, "Cada regla lleva un nombre que se rastrea hasta su cruce en la matriz firmada.", 17, a.TXT))
write(a, "10-t1.svg", "Del evento al efecto", [12, 37, 62, 90])
