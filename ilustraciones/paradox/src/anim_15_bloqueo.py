"""Teoría lección 15: bloqueo de teclado por códigos inválidos."""
from _apdx import *

a = new(22, "Bloqueo de teclado: el que prueba códigos, se queda afuera")
a.steps(["Alguien prueba códigos al azar: cada uno inválido suma uno.",
         "Llega a [717] = 5 intentos inválidos.",
         "Los teclados se bloquean [716] = 10 minutos y la central lo reporta.",
         "Pasado el bloqueo, el teclado vuelve; el código correcto desarma."], still=2)
a.add(a.box(48, 190, 300, 320, "#F1F4F7", "#C2D4E6", rx=20, sw=2))
a.add(a.box(72, 214, 252, 80, "#0B3A66", None, rx=8))
for s, e, t, still in [(0, 50, "código: ****", 0), (50, 75, "BLOQUEADO", 1), (75, 100, "listo", 0)]:
    at(a, a.text(90, 264, t, 24, "#FFD28A" if t == "BLOQUEADO" else "#9FE3F7", a.MONO, 700), s, e, still)
for r in range(3):
    for k in range(3):
        a.add(a.box(82 + k * 82, 316 + r * 60, 68, 46, a.WHITE, "#C2D4E6", rx=8))
a.add(a.text(420, 210, "INTENTOS INVÁLIDOS", 14, a.GREY, a.MONO, 600, extra='letter-spacing="2"'))
for i in range(5):
    x = 420 + i * 92
    a.add(a.box(x, 228, 76, 76, a.WHITE, a.LINE, rx=12) + a.text(x + 38, 276, str(i + 1), 26, a.GREY, a.MONO, 700, "middle"))
    at(a, a.box(x, 228, 76, 76, a.BADBG, a.BAD, rx=12, sw=3) + a.text(x + 38, 276, str(i + 1), 26, a.BAD, a.MONO, 700, "middle"), 4 + i * 8 if i < 4 else 25, 75, 1)
at(a, a.box(420, 340, 444, 80, a.INK, None, rx=14) + a.text(444, 374, "teclados bloqueados", 19, "#fff", a.HEAD, 600) + a.text(444, 402, "10 min · [716]", 16, "#FFD28A", a.MONO, 700), 50, 75, 1)
a.add(card(a, 920, 190, 232, 150, "Monitoreo", None))
at(a, a.text(944, 280, "nada", 17, a.GREY, a.SANS, 600), 0, 50, 0)
at(a, a.text(944, 280, "bloqueo de teclado", 17, a.BAD, a.SANS, 700) + a.text(944, 306, "abonado 1A01", 15, a.INK, a.MONO, 600), 50, 100, 1)
at(a, a.arrow("M864 380C900 380 900 330 1000 344", a.BAD, 3), 52, 75, 1)
at(a, chip(a, 420, 450, "fin del bloqueo: el código correcto desarma", "ok"), 75, 100, 0)
caption(a, 600, [(0, 25, "000 en [717] deja el bloqueo apagado, como viene de fábrica.", None),
                 (25, 50, "Valores de ejemplo: se acuerdan con el cliente.", None),
                 (50, 75, "El reporte avisa a monitoreo que alguien estuvo probando.", a.BAD),
                 (75, 100, "Protege el teclado; las llaves de fábrica igual se cambian todas.", a.OK)], still=2)
write(a, "15-t1.svg", "Bloqueo de teclado: el que prueba códigos, se queda afuera",
      "Animación en cuatro tiempos con un teclado, un contador de intentos y monitoreo. 1: alguien prueba códigos y cada inválido suma uno. "
      "2: llega a los 5 intentos de la sección 717. 3: los teclados se bloquean 10 minutos, sección 716, y la central reporta el bloqueo a monitoreo. "
      "4: termina el bloqueo y el código correcto desarma.")
