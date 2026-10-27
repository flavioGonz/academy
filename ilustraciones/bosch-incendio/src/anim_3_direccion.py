"""Teoría de Lazo LSN: dirección automática por orden de cable, manual por perillas y T-tap."""
from _anim_bi import *

caps = ["El panel lanza la autodetección desde LSN1.",
        "Perillas en 000: cada uno recibe el número de su lugar en el cable.",
        "Perillas manuales: cada uno responde con la suya, sin importar el orden.",
        "Una derivación T-tap: solo con manual y T-tap marcado en RPS."]
a = new(24, "Direcciones", "Automático numera por cable; manual, por perillas", caps, still=3)

a.add(a.box(60, 190, 240, 90, a.INK, a.INK, rx=14))
a.add(a.text(80, 228, "Módulo LSN", 19, a.WHITE, a.SANS, 600))
a.add(a.text(100, 266, "LSN1", 14, "#9FC3E3", a.MONO, 600, "middle")); a.add(a.text(260, 266, "LSN2", 14, "#9FC3E3", a.MONO, 600, "middle"))
loop = "M100 280 V400 H1100 V320 H260 V280"
a.add(f'<path d="{loop}" fill="none" stroke="{a.BLUE}" stroke-width="4" stroke-linejoin="round"/>')
D = [(420, 400), (680, 400), (940, 400)]
for x, y in D:
    a.add(a.box(x - 36, y - 36, 72, 72, a.BG, rx=10))
    a.add(det(a, x, y, 30))
s0, s1 = ph(a, 0)
token(a, "autodetección", [(s0 + 2, 100, 340), (s0 + 8, 100, 400), (s0 + 20, 1000, 400), (s1 - 1, 1000, 400)], bg=a.CYAN)
for (x, y), n in zip(D, ("1", "2", "3")):
    vis(a, a.pill(x, y + 46, n, a.WHITE, a.BLUE, size=17, anchor="middle"), 1)
for (x, y), n in zip(D, ("17", "4", "9")):
    vis(a, a.pill(x, y + 46, n, a.WHITE, a.OK, size=17, anchor="middle"), 2, 3)
vis(a, a.text(300, 520, "1, 2, 3: el orden del cable", 17, a.BLUE, a.SANS, 600), 1)
vis(a, a.text(300, 520, "17, 4, 9: lo que dicen las perillas", 17, a.OK, a.SANS, 600), 2, 3)
# T-tap
vis(a, f'<path d="M810 400 V560 H880" fill="none" stroke="{a.BLUE}" stroke-width="4"/>', 3)
vis(a, a.box(880, 524, 72, 72, a.BG, rx=10) + det(a, 916, 560, 30), 3)
vis(a, a.pill(960, 548, "21", a.WHITE, a.OK, size=17), 3)
vis(a, a.pill(1150, 506, "T-tap marcado en RPS", a.OK, a.OKBG, anchor="end"), 3)
a.add(a.text(48, 640, "En un mismo lazo, o todos automáticos o todos manuales del 1 al 254.", 17, a.TXT))
write(a, "3-t1.svg", "Automático o manual", [12, 37, 62, 90])
