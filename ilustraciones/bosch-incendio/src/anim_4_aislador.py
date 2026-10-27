"""Teoría de Lazo cerrado: alimentación alternada y aisladores ante un corto."""
from _anim_bi import *

caps = ["El módulo alimenta el lazo desde LSN1.",
        "Diez segundos después, desde LSN2: el sentido se alterna.",
        "Corto entre el 2 y el 3: se abren sus aisladores.",
        "Dos ramales, uno por extremo: todos detectan, con avería."]
a = new(24, "Aisladores", "El lazo encierra el corto y sigue detectando", caps, still=3)

a.add(a.box(480, 160, 240, 70, a.INK, a.INK, rx=14))
a.add(a.text(600, 192, "Módulo LSN", 18, a.WHITE, a.SANS, 600, "middle"))
a.add(a.text(510, 222, "LSN1", 13, "#9FC3E3", a.MONO, 600, "middle")); a.add(a.text(690, 222, "LSN2", 13, "#9FC3E3", a.MONO, 600, "middle"))
full = "M510 230 V300 H120 V520 H1080 V300 H690 V230"
a.add(f'<path d="{full}" fill="none" stroke="#C2D4E6" stroke-width="5" stroke-linejoin="round"/>')
flow(a, full, a.OK, 0)
flow(a, "M690 230 V300 H1080 V520 H120 V300 H510 V230", a.CYAN, 1)
flow(a, "M510 230 V300 H120 V520 H330", a.OK, 3)
flow(a, "M690 230 V300 H1080 V520 H670", a.CYAN, 3)
E = [(120, 410, "1"), (360, 520, "2"), (640, 520, "3"), (920, 520, "4"), (1080, 410, "5")]
for x, y, n in E:
    a.add(a.box(x - 36, y - 36, 72, 72, a.BG, rx=10))
    a.add(det(a, x, y, 28, a.OK))
    lx, ly = (x - 52, y + 6) if n == "1" else ((x + 52, y + 6) if n == "5" else (x, y + 56))
    a.add(a.text(lx, ly, n, 16, a.GREY, a.MONO, 600, "middle"))
# corto
vis(a, f'<path d="M478 498 l20 18 l-12 4 l22 22" fill="none" stroke="{a.BAD}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>', 2, 3)
vis(a, a.pill(500, 560, "corto", a.BAD, a.BADBG, anchor="middle"), 2, 3)
for x in (360, 640):
    vis(a, a.box(x - 26, 460, 52, 26, a.BADBG, a.BAD, rx=6, sw=1.5) + a.text(x, 479, "abre", 13, a.BAD, a.MONO, 600, "middle"), 2, 3)
vis(a, a.pill(300, 270, "desde LSN1", a.OK, a.OKBG, anchor="middle"), 0)
vis(a, a.pill(900, 270, "desde LSN2", a.CYAN, a.WHITE, anchor="middle"), 1)
vis(a, a.pill(300, 270, "1 y 2 por LSN1", a.OK, a.OKBG, anchor="middle"), 3)
vis(a, a.pill(900, 270, "3, 4 y 5 por LSN2", a.CYAN, a.WHITE, anchor="middle"), 3)
vis(a, a.pill(200, 584, "panel: avería del lazo", a.AMB, a.AMBBG, anchor="middle"), 3)
a.add(a.text(48, 645, "Según el manual, en operación normal el sentido de la corriente cambia cada 10 segundos.", 16, a.TXT))
write(a, "4-t1.svg", "El lazo encierra el corto", [12, 37, 62, 90])
