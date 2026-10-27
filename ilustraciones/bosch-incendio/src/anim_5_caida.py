"""Teoría de Quince voltios: la tensión cae por el cable y por los elementos."""
from _anim_bi import *

caps = ["El módulo entrega 30 V en sus bornes.",
        "La corriente va y vuelve por el cable: cada metro resta.",
        "Con 0,5 mA por elemento, al final quedan unos 26,2 V.",
        "Con 2 mA (sirenas, módulos), unos 20,5 V: el margen se achica."]
a = new(24, "Tensión", "La tensión cae en el camino: tiene que llegar 15 V", caps, still=3)

a.add(card(a, 48, 220, 230, 120, "Módulo LSN", "30 V en bornes", dark=True))
a.add(a.box(910, 190, 250, 180, "#E5F0FB", a.CYAN, rx=16, sw=2))
a.add(a.text(930, 222, "60 elementos al final", 16, a.BLUE, a.SANS, 600))
for k in range(4):
    for j in range(2):
        a.add(det(a, 960 + k * 56, 268 + j * 62, 22))
a.add(f'<path d="M280 250 H908" stroke="{a.BLUE}" stroke-width="4"/><path d="M280 310 H908" stroke="{a.INK}" stroke-width="3"/>')
a.add(a.text(594, 290, "600 m de ida y 600 m de vuelta", 15, a.GREY, a.MONO, 400, "middle"))
flow(a, "M280 250 H908", a.OK, 1, 3, width=6)
flow(a, "M908 310 H280", a.OK, 1, 3, width=6)
vis(a, a.pill(163, 360, "30 V", a.OK, a.OKBG, size=18, anchor="middle"), 0, 3)
# barras de tensión al final
X0, Y0, H = 360, 600, 6.0  # px por voltio
a.add(a.text(360, 410, "TENSIÓN AL ÚLTIMO ELEMENTO", 14, a.GREY, a.MONO, 600))
a.add(f'<path d="M330 {Y0} H880" stroke="{a.LINE}" stroke-width="2"/>')
for i, (v, lab, col) in enumerate([(26.2, "0,5 mA: 26,2 V", a.OK), (20.5, "2 mA: 20,5 V", a.AMB)]):
    x = 400 + i * 240
    vis(a, a.box(x, Y0 - v * H, 140, v * H, col, rx=6) + a.text(x + 70, Y0 - v * H - 10, lab, 16, col, a.MONO, 600, "middle"), 2 + i, 3)
a.add(f'<path d="M330 {Y0 - 15 * H} H880" stroke="{a.BAD}" stroke-width="2.5" stroke-dasharray="8 6"/>')
a.add(a.text(886, Y0 - 15 * H + 5, "15 V mínimo", 15, a.BAD, a.SANS, 600))
vis(a, a.text(48, 470, "Cada elemento suma", 16, a.TXT), 1, 3)
vis(a, a.text(48, 494, "0,35 ohm y su consumo", 16, a.TXT), 1, 3)
a.add(a.text(48, 645, "Con 2 mA y más cable, cerca de los 1100 m la tensión baja de 15 V: avería. Cuenta de banco; la de obra va en SSD.", 15, a.TXT))
write(a, "5-t1.svg", "La tensión cae en el camino", [12, 37, 62, 90])
