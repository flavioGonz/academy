"""Teoría de Zona de energía: reposo, alarma y margen de la batería."""
from _anim_bi import *

caps = ["Con red: la fuente alimenta el panel y carga las baterías.",
        "Sin red: las baterías toman el reposo (24 h; RPS trae 30 h).",
        "Al final, la alarma: 5 min según NFPA o 15 min según la IT-11.",
        "Lo que sobra es el margen del factor: 1,20 o 1,25."]
a = new(24, "Baterías", "Primero horas de reposo, después minutos de alarma", caps, still=3)

# línea de tiempo
X0, X1 = 80, 1120
seg = [(80, 300, "con red", a.BLUE), (300, 820, "reposo sin red: 24 h o 30 h", a.CYAN), (820, 960, "alarma", a.BAD), (960, 1120, "margen", a.OK)]
for x0, x1, t, col in seg:
    a.add(a.box(x0, 220, x1 - x0 - 4, 54, col, rx=8, extra='fill-opacity=".85"'))
    a.add(a.text((x0 + x1) / 2, 254, t, 16, a.WHITE, a.SANS, 600, "middle"))
s0, s1 = ph(a, 0)
_, e1 = ph(a, 3)
mk = a.add(a.group(f'<path d="M0 -14 L10 0 L-10 0 Z" fill="{a.INK}"/><rect x="-2" y="0" width="4" height="70" fill="{a.INK}"/>',
                   a.move([(0, 100, 290), (ph(a, 0)[1], 290, 290), (ph(a, 1)[1], 815, 290), (ph(a, 2)[1], 955, 290), (100, 1110, 290)]), still=0))
# batería
a.add(a.box(470, 400, 260, 150, a.WHITE, a.INK, rx=12, sw=3))
a.add(a.box(500, 386, 40, 14, a.INK, rx=3)); a.add(a.box(660, 386, 40, 14, a.BAD, rx=3))
levels = [(0, 5, a.OK), (1, 3, a.CYAN), (2, 1, a.BAD), (3, 1, a.OK)]
for i, n, col in levels:
    vis(a, "".join(a.box(490 + k * 46, 420, 38, 110, col, rx=6) for k in range(n)), i)
vis(a, a.text(760, 480, "cargando", 17, a.BLUE, a.SANS, 600), 0)
vis(a, a.text(760, 480, "baja despacio", 17, a.CYAN, a.SANS, 600), 1)
vis(a, a.text(760, 480, "baja rápido", 17, a.BAD, a.SANS, 600), 2)
vis(a, a.text(760, 480, "queda el margen", 17, a.OK, a.SANS, 600), 3)
a.add(a.text(48, 604, "C = (I reposo x horas + I alarma x tiempo de alarma) x factor", 18, a.INK, a.MONO, 600))
a.add(a.text(48, 640, "Escala ilustrativa: en Ah, la alarma pesa poco, pero es lo que tiene que funcionar al final.", 16, a.TXT))
write(a, "8-t1.svg", "Reposo, alarma y margen", [12, 37, 62, 90])
