"""Teoría lección 10: cola, IOPS y latencia del disco que graba (ley de Little)."""
from _awin import *

a = new(24, "Por qué la cola y la latencia suben juntas")
a.steps(["Pocas cámaras: cada pedido se atiende al llegar.",
         "Más cámaras: llegan pedidos más rápido de lo que salen.",
         "La cola crece y cada pedido espera más: sube la latencia.",
         "Sostenido arriba de 25 ms: el disco no da abasto."], still=3)
a.add(card(a, 48, 200, 230, 110, "Cámaras", "escriben video"))
a.add(card(a, 930, 186, 222, 300, "Disco", "atiende de a uno", dark=True))
a.add(a.text(600, 186, "cola de pedidos", 16, a.GREY, a.MONO, 600, "middle"))
N, X0, SW = 8, 330, 66
for i in range(N):
    a.add(a.box(X0 + i * SW, 210, 56, 80, a.WHITE, a.LINE, rx=10, sw=2))
fill = [(0, 25, 1, a.OK), (25, 50, 3, a.AMB), (50, 75, 6, a.AMB), (75, 100, 8, a.BAD)]
for s, e, n, col in fill:
    for i in range(n):
        at(a, a.box(X0 + (N - 1 - i) * SW + 4, 214, 48, 72, col, None, rx=8), s, e, 1 if s == 75 else 0)
# pedidos que entran (flujo)
for k in range(10):
    t0 = k * 10
    mv = a.move([(0, 280, 250), (t0, 280, 250), (t0 + 4, 322, 250), (100, 322, 250)])
    op = a.keyframes([(0, 0), (t0, 0), (t0 + 0.3, 1), (t0 + 4, 1), (t0 + 4.3, 0), (100, 0)])
    a.add(a.group(f'<circle cx="0" cy="0" r="8" fill="{a.BLUE}"/>', mv, op, still=0))
# medidores
labels = [("2 ms", "0,1", a.OK), ("9 ms", "1,5", a.AMB), ("18 ms", "3", a.AMB), ("31 ms", "5", a.BAD)]
a.add(a.text(330, 352, "Latencia (ejemplo)", 17, a.INK, a.SANS, 600) + a.text(330, 430, "Cola (ejemplo)", 17, a.INK, a.SANS, 600))
a.add(a.box(330, 366, 520, 18, a.SLATE, None, rx=9) + a.box(330, 444, 520, 18, a.SLATE, None, rx=9))
a.add(line(a, "M751 356V394", a.BAD, 3) + a.text(751, 412, "25 ms", 15, a.BAD, a.MONO, 600, "middle"))
for i, ((s, e, _, _), (lat, q, col), lw, qw) in enumerate(zip(fill, labels, (34, 150, 300, 500), (26, 160, 300, 500))):
    st = 1 if i == 3 else 0
    at(a, a.box(330, 366, lw, 18, col, None, rx=9) + a.text(870, 382, lat, 17, col, a.MONO, 700), s, e, st)
    at(a, a.box(330, 444, qw, 18, col, None, rx=9) + a.text(870, 460, q, 17, col, a.MONO, 700), s, e, st)
a.add(a.box(48, 500, 1104, 56, "#E5F0FB", None, rx=14) + a.text(72, 535, "cola ≈ IOPS × latencia", 19, a.BLUE, a.MONO, 700)
      + a.text(400, 535, "por eso se miran los tres números juntos, no uno solo", 17, a.TXT, a.SANS, 500))
caption(a, 610, [(0, 25, "Con poca carga, la latencia es casi solo lo que tarda el disco en sí.", a.OK),
                 (25, 50, "Si entran más pedidos por segundo de los que el disco atiende, se acumulan.", a.AMB),
                 (50, 75, "Cada pedido espera a los de adelante: la demora crece con la fila.", a.AMB),
                 (75, 100, "Ahí se pierden cuadros: el disco no da abasto para esa carga.", a.BAD)], still=3)
write(a, "10-t1.svg", "Por qué la cola y la latencia suben juntas",
      "Animación en cuatro tiempos: las cámaras mandan pedidos de escritura a una cola de ocho lugares frente al disco, con dos barras debajo, latencia y cola, con valores de ejemplo. "
      "1: con pocas cámaras la cola casi no tiene pedidos y la latencia es de unos 2 ms. 2: con más cámaras entran pedidos más rápido de lo que salen y la cola empieza a llenarse. "
      "3: la cola crece y la latencia sube porque cada pedido espera a los de adelante. 4: la cola está llena, la latencia pasa la marca de 25 ms y se marca en rojo: el disco no da abasto. "
      "Abajo, la relación cola aproximadamente igual a IOPS por latencia.", pcts=(12, 37, 62, 90))
