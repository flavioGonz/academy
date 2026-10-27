"""Teoría lección 1: por núcleo, con mínimo de 16 por CPU (ejemplo de la KB 313548 citado por Introserv)."""
from _avmw import *

a = new(20, "Por núcleo, con un mínimo de 16 por CPU")
a.steps(["Tres hosts, una CPU de 8 núcleos cada uno: 24 núcleos reales.",
         "Cada CPU se cobra como mínimo 16: se suman 8 por CPU.",
         "Resultado: 48 núcleos licenciables para 24 reales.",
         "Con CPUs de 16 núcleos o más, la cuenta es 1 a 1."], still=2)

HX = [48, 418, 788]
for i, x in enumerate(HX):
    a.add(card(a, x, 190, 350, 230, f"Host {i + 1}", "1 CPU"))
    a.add(a.box(x + 20, 266, 310, 132, a.SLATE, a.LINE, rx=10))
    for k in range(8):
        r, q = divmod(k, 8)
        a.add(a.box(x + 34 + q * 37, 284, 28, 22, a.BLUE, rx=4))
    # núcleos que se pagan sin existir
    pad = "".join(a.box(x + 34 + q * 37, 318, 28, 22, "none", a.AMB, rx=4, sw=2, extra='stroke-dasharray="4 3"') for q in range(8))
    at(a, pad, 25, 75, 1)
    at(a, a.text(x + 34, 380, "8 reales", 17, a.BLUE, a.MONO, 600), 0, 25, 0)
    at(a, a.text(x + 34, 380, "8 reales + 8 sin existir", 17, a.AMB, a.MONO, 600), 25, 75, 1)

# totales
at(a, a.box(48, 450, 1110, 80, a.WHITE, a.LINE, rx=14) + a.text(80, 500, "24 núcleos físicos", 24, a.BLUE, a.MONO, 700), 0, 50, 0)
at(a, a.box(48, 450, 1110, 80, a.AMBBG, a.AMB, rx=14) + a.text(80, 500, "24 físicos", 24, a.BLUE, a.MONO, 700)
   + a.text(1126, 500, "48 licenciables: el doble", 24, a.AMB, a.MONO, 700, "end"), 50, 75, 1)
# caso 1 a 1
cover = a.box(40, 180, 1130, 360, a.BG, None, rx=0)
caso = cover
for i, x in enumerate([48, 603]):
    caso += card(a, x, 190, 540, 230, f"Host {i + 1}", "1 CPU de 24 núcleos")
    caso += a.box(x + 20, 266, 500, 132, a.SLATE, a.LINE, rx=10)
    for k in range(24):
        r, q = divmod(k, 12)
        caso += a.box(x + 34 + q * 40, 284 + r * 34, 30, 22, a.BLUE, rx=4)
caso += a.box(48, 450, 1110, 80, a.OKBG, a.OK, rx=14) + a.text(80, 500, "48 físicos", 24, a.BLUE, a.MONO, 700) + a.text(1126, 500, "48 licenciables: 1 a 1", 24, a.OK, a.MONO, 700, "end")
at(a, caso, 75, 100, 0)
caption(a, 590, [(0, 25, "Se cuentan núcleos físicos, no hilos ni sockets.", None),
                 (25, 50, "Los núcleos deshabilitados en BIOS no bajan la cuenta salvo acuerdo por escrito.", None),
                 (50, 75, "Así pegó el cambio en los clientes chicos: pagan núcleos que no tienen.", a.AMB),
                 (75, 100, "Con CPUs grandes el modelo no castiga: por eso la decisión es por cliente.", a.OK)], still=2)
write(a, "1-t1.svg", "Por núcleo, con un mínimo de 16 por CPU",
      "Animación en cuatro tiempos. 1: tres hosts con una CPU de 8 núcleos cada uno suman 24 núcleos físicos. "
      "2: cada CPU se cobra como mínimo 16, así que a cada una se le suman 8 núcleos que no existen, marcados en ámbar. "
      "3: el total queda en 24 físicos y 48 licenciables, el doble. "
      "4: en cambio, dos hosts con una CPU de 24 núcleos suman 48 físicos y 48 licenciables, una relación 1 a 1.")
