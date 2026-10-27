"""Teoría lección 14: registro IP en la receptora y supervisión."""
from _apdx import *

a = new(22, "Registro y supervisión: lo que muestra [935]")
a.steps(["ARM en [935]: el módulo pide registrarse. El grupo 1 titila.",
         "La receptora valida abonado, perfil, formato y la MAC del módulo.",
         "Registrado: el grupo 1 queda fijo.",
         "Supervisión: el módulo se reporta según el perfil. Si calla, avisa."], still=2)
a.add(card(a, 48, 190, 300, 320, "[935] estado", None))
for i, (g, t) in enumerate([("1", "registro"), ("2", "módulo"), ("3", "programación"), ("4", "registro (error)")]):
    y = 240 + i * 62
    a.add(a.box(72, y, 44, 44, a.WHITE, a.LINE, rx=10) + a.text(94, y + 29, g, 18, a.GREY, a.MONO, 700, "middle"))
    a.add(a.text(132, y + 29, t, 17, a.INK, a.SANS, 600))
blink = a.keyframes([(0, 0), (3, 0), (4, 1), (7, 1), (8, 0), (11, 0), (12, 1), (15, 1), (16, 0), (19, 0), (20, 1), (23, 1), (24, 0), (25, 0), (100, 0)])
a.add(a.group(a.box(72, 240, 44, 44, a.CYAN, None, rx=10) + a.text(94, 269, "1", 18, "#fff", a.MONO, 700, "middle"), blink, still=0))
at(a, a.box(72, 240, 44, 44, a.CYAN, None, rx=10) + a.text(94, 269, "1", 18, "#fff", a.MONO, 700, "middle"), 50, 100, 1)
a.add(card(a, 440, 220, 240, 110, "Módulo IP", "MAC del equipo"))
a.add(card(a, 840, 190, 312, 320, "Receptora", "IPR512 o IPC10"))
checks = ["abonado 1A01", "perfil 02", "formato Contact ID", "MAC conocida"]
for i, c_ in enumerate(checks):
    y = 270 + i * 50
    a.add(a.text(904, y + 6, c_, 17, a.INK, a.SANS, 600))
    at(a, f'<circle cx="880" cy="{y}" r="11" fill="{a.OK}"/>' + a.text(880, y + 5, "✓", 14, "#fff", a.SANS, 700, "middle"), 28 + i * 5, 100, 1)
at(a, a.arrow("M680 255H834", a.BLUE, 4) + a.text(757, 242, "registro", 14, a.BLUE, a.MONO, 700, "middle"), 0, 50, 1)
at(a, a.arrow("M836 300H686", a.OK, 4) + a.text(761, 322, "OK", 14, a.OK, a.MONO, 700, "middle"), 50, 75, 1)
# supervisión: latidos
for k in range(3):
    t0 = 76 + k * 7
    mv = a.move([(0, 690, 420), (t0, 690, 420), (t0 + 5, 830, 420), (100, 830, 420)])
    op = a.keyframes([(0, 0), (t0, 0), (t0 + 0.5, 1), (t0 + 5, 1), (t0 + 5.5, 0), (100, 0)])
    a.add(a.group(f'<circle cx="0" cy="0" r="9" fill="{a.CYAN}"/>', mv, op, still=0))
at(a, a.text(560, 460, "cada 600 s (perfil 02, IPC10)", 15, a.CYAN, a.MONO, 700, "middle"), 75, 100, 0)
caption(a, 600, [(0, 25, "Grupo 1: apagado sin registrar, titila registrando, fijo registrado.", None),
                 (25, 50, "Si algo no coincide, el error aparece en el grupo 4: por ejemplo, otra MAC.", a.AMB),
                 (50, 75, "Grupos 2 y 3 hablan de la casa: el módulo y la programación.", None),
                 (75, 100, "Menos segundos de perfil: la receptora se entera antes si el módulo cae.", a.OK)], still=2)
write(a, "14-t1.svg", "Registro y supervisión: lo que muestra [935]",
      "Animación en cuatro tiempos con la tabla de estado de la sección 935, el módulo IP y la receptora. 1: con ARM el módulo pide registrarse y el grupo 1 titila. "
      "2: la receptora valida abonado 1A01, perfil 02, formato Contact ID y la MAC del módulo. 3: registrado, el grupo 1 queda fijo. "
      "4: el módulo se reporta periódicamente según el perfil, cada 600 segundos con el perfil 02 del IPC10; si deja de hacerlo, la receptora avisa.")
