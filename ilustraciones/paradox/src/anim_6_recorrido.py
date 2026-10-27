"""Teoría lección 6: armado, demora de salida, retardo de entrada y seguimiento."""
from _apdx import *

a = new(24, "Armado, salida y entrada: los tiempos que evitan la falsa alarma")
a.steps(["Arma y sale: corre la demora de salida, 60 s de fábrica ([745]).",
         "Termina la demora: la casa queda armada.",
         "Vuelve: abre la puerta (01) y arranca el retardo de entrada, 45 s ([710]).",
         "Pasa frente al PIR (05): espera. Desarma a tiempo: no hay alarma."], still=3)
X0, X1, Y = 80, 1120, 300
a.add(line(a, f"M{X0} {Y}H{X1}", a.LINE, 10))
segs = [(80, 320, "salida 60 s", a.AMB, 0, 25), (320, 640, "armada", a.OK, 25, 50), (640, 920, "entrada 45 s", a.AMB, 50, 100)]
for x1, x2, lab, col, s, e in segs:
    at(a, line(a, f"M{x1} {Y}H{x2}", col, 10) + a.text((x1 + x2) / 2, Y - 22, lab, 16, col, a.MONO, 700, "middle"), s, 100, 1)
marks = [(80, "arma"), (320, "armada"), (640, "abre la puerta"), (790, "pasa el PIR"), (900, "desarma")]
for x, lab in marks:
    a.add(f'<circle cx="{x}" cy="{Y}" r="8" fill="#fff" stroke="{a.INK}" stroke-width="3"/>')
    a.add(a.text(x, Y + 36, lab, 15, a.INK, a.SANS, 600, "middle"))
# marcador de tiempo
mv = a.move([(0, 80, Y), (25, 320, Y), (50, 640, Y), (75, 790, Y), (88, 900, Y), (100, 900, Y)])
a.add(a.group(f'<circle cx="0" cy="0" r="14" fill="{a.CYAN}" stroke="#fff" stroke-width="3"/>', mv, a.keyframes([(0, 1), (100, 1)]), still=0))
# zonas
zs = [(80, "01", "puerta", "retardo de entrada"), (380, "05", "PIR del living", "seguimiento"), (680, "08", "ventanas", "instantánea")]
for x, c_, t, d in zs:
    a.add(card(a, x, 400, 280, 110, None, None))
    a.add(a.text(x + 20, 440, c_, 22, a.BLUE, a.MONO, 700))
    a.add(a.text(x + 66, 440, t, 18, a.INK, a.SANS, 600))
    a.add(a.text(x + 20, 476, d, 16, a.GREY, a.SANS, 600))
at(a, a.box(80, 400, 280, 110, "none", a.CYAN, rx=14, sw=4), 50, 75, 0)
at(a, a.box(380, 400, 280, 110, "none", a.CYAN, rx=14, sw=4), 75, 100, 1)
at(a, chip(a, 400, 484, "espera: antes abrió la puerta", "ok"), 75, 100, 1)
a.add(card(a, 980, 400, 172, 110, None, None))
at(a, a.text(1066, 466, "armando", 20, a.AMB, a.SANS, 700, "middle"), 0, 25, 0)
at(a, a.text(1066, 466, "armada", 20, a.OK, a.SANS, 700, "middle"), 25, 88, 0)
at(a, a.text(1066, 466, "desarmada", 20, a.OK, a.SANS, 700, "middle"), 88, 100, 1)
caption(a, 600, [(0, 25, "La demora de salida deja salir por la puerta sin que la zona 01 dispare.", None),
                 (25, 50, "Armada: una ventana (08) dispararía al instante, sin esperar.", None),
                 (50, 75, "El retardo de entrada da tiempo de llegar al teclado.", a.AMB),
                 (75, 100, "Si el PIR se activa sin que antes se abra la puerta, ahí sí dispara al instante.", a.OK)], still=3)
write(a, "6-t1.svg", "Armado, salida y entrada: los tiempos que evitan la falsa alarma",
      "Animación en cuatro tiempos sobre una línea de tiempo. 1: el cliente arma y corre la demora de salida de 60 segundos, sección 745. "
      "2: termina la demora y la casa queda armada; una ventana instantánea dispararía al momento. 3: vuelve, abre la puerta de la zona 01 y arranca el retardo de entrada de 45 segundos, sección 710. "
      "4: pasa frente al PIR de seguimiento, zona 05, que espera porque antes se abrió la puerta, y desarma a tiempo: no hay alarma.", pcts=(12, 37, 62, 92))
