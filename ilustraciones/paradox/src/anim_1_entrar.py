"""Teoría lección 1: dos formas de entrar a programación (SP/MG contra EVO)."""
from _apdx import *

a = new(20, "Dos familias, dos formas de entrar")
a.steps(["Entrar: ENTER en SP y MG; mantener el 0 en EVO.",
         "Código de instalador: 4 dígitos (0000) contra 6 (000000).",
         "Sección: tres dígitos en SP y MG, cuatro en EVO.",
         "Adentro de la sección: dato, ENTER para mirar, CLEAR para salir."], still=3)


def key(x, y, s, dark=False, w=None):
    w = w or len(s) * 13 + 34
    if dark:
        return a.box(x, y, w, 52, "#03213C", None, rx=10) + a.text(x + w / 2, y + 34, s, 20, "#D9E9F8", a.MONO, 600, "middle"), w
    return (a.box(x, y + 4, w, 52, a.LINE, None, rx=10) + a.box(x, y, w, 52, a.WHITE, "#C2D4E6", rx=10, sw=2)
            + a.text(x + w / 2, y + 34, s, 20, a.INK, a.MONO, 600, "middle")), w


lanes = [(210, "SP / SP+ · MG / MG+", [("ENTER", False, None), ("0000", True, None), ("710", False, "3 dígitos"), ("dato · CLEAR", True, None)]),
         (400, "EVO / EVOHD+", [("mantener 0", False, None), ("000000", True, None), ("4000", False, "4 dígitos"), ("dato · CLEAR", True, None)])]
for y, title, ks in lanes:
    a.add(a.box(48, y - 34, 1104, 150, a.WHITE, a.LINE, rx=16, sw=2))
    a.add(a.text(72, y - 4, title, 19, a.INK, a.HEAD, 600))
    x = 72
    for i, (s, dark, note) in enumerate(ks):
        k, w = key(x, y + 20, s, dark)
        extra = a.text(x + w / 2, y + 102, note, 15, a.BLUE, a.SANS, 600, "middle") if note else ""
        at(a, k + extra, i * 25, 100, 1)
        if i < 3:
            at(a, a.text(x + w + 22, y + 54, "→", 22, a.GREY, a.MONO, 600, "middle"), (i + 1) * 25, 100, 1)
        x += w + 46
caption(a, 600, [(0, 25, "La forma de entrar ya te dice la familia: si ENTER no hace nada, probá con la de EVO.", None),
                 (25, 50, "Los códigos de fábrica están en manuales públicos: se cambian el primer día.", a.AMB),
                 (50, 75, "Mismo número no es misma función: una sección de SP no existe en EVO.", None),
                 (75, 100, "Por eso se abre el manual de la familia correcta antes de tocar una sección.", a.OK)], still=3)
write(a, "1-t1.svg", "Dos familias, dos formas de entrar",
      "Animación en cuatro tiempos con dos filas, SP y MG arriba, EVO abajo. 1: en SP y MG se entra con ENTER; en EVO se mantiene el 0. "
      "2: aparece el código de instalador, 0000 en SP y MG, 000000 en EVO. 3: la sección tiene tres dígitos en SP y MG (ejemplo 710) y cuatro en EVO (ejemplo 4000). "
      "4: adentro se carga el dato o se mira con ENTER, y CLEAR sale. El cuadro fijo muestra las dos secuencias completas.")
