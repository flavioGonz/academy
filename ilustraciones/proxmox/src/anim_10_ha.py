"""Teoría lección 10: HA con fencing por watchdog."""
from _apmx import *

a = new(24, "Fencing: primero se apaga el nodo, después se mueve la VM")
a.steps(["Todo sano: la VM 100 corre en pve1 y escribe en el storage.",
         "pve1 pierde la red del clúster: sin quórum, no renueva el watchdog.",
         "A los 60 segundos el watchdog reinicia pve1: deja de escribir.",
         "Con pve1 fuera, la HA arranca la VM 100 en pve2."], still=3)
NX = [48, 432, 816]
NAMES = ["pve1", "pve2", "pve3"]
for i, x in enumerate(NX):
    if i == 0:
        continue
    a.add(card(a, x, 170, 336, 150, NAMES[i], "con quórum", dark=True))
at(a, card(a, NX[0], 170, 336, 150, "pve1", "con quórum", dark=True), 0, 25, 0)
at(a, card(a, NX[0], 170, 336, 150, "pve1", "aislado · sin quórum", fill=a.AMBBG, stroke=a.AMB), 25, 50, 0)
at(a, card(a, NX[0], 170, 336, 150, "pve1", "reiniciándose", fill=a.BADBG, stroke=a.BAD), 50, 75, 0)
at(a, card(a, NX[0], 170, 336, 150, "pve1", "fuera del clúster", fill=a.SLATE, stroke=a.LINE), 75, 100, 1)
# red del clúster
at(a, line(a, "M768 214 H816", a.BLUE, 4), 0, 100, 1)
at(a, line(a, "M384 214 H432", a.BLUE, 4), 0, 25, 0)
# storage compartido
a.add(a.box(300, 470, 600, 80, a.WHITE, a.LINE, rx=14, sw=2) + a.text(600, 506, "Almacenamiento compartido", 19, a.INK, a.HEAD, 600, "middle")
      + a.text(600, 532, "disco de la VM 100", 15, a.GREY, a.MONO, 500, "middle"))
# VM 100
vm = lambda x, kind: a.box(x + 24, 240, 288, 56, {"ok": a.OKBG, "amb": a.AMBBG, "bad": a.BADBG}[kind], {"ok": a.OK, "amb": a.AMB, "bad": a.BAD}[kind], rx=10, sw=2) + a.text(x + 168, 275, "VM 100", 18, {"ok": a.OK, "amb": a.AMB, "bad": a.BAD}[kind], a.MONO, 700, "middle")
at(a, vm(NX[0], "ok") + line(a, "M300 296 C 300 400, 420 430, 420 466", a.OK, 3), 0, 25, 0)
at(a, vm(NX[0], "amb") + line(a, "M300 296 C 300 400, 420 430, 420 466", a.AMB, 3) + chip(a, 60, 340, "sigue escribiendo", "amb"), 25, 50, 0)
at(a, chip(a, 60, 340, "watchdog: 60 s y reinicio", "bad"), 50, 75, 0)
at(a, vm(NX[1], "ok") + line(a, "M600 296 V466", a.OK, 3) + chip(a, 444, 340, "recuperada por la HA", "ok"), 75, 100, 1)
# contador del watchdog
for s, e, t, col, st in [(0, 25, "watchdog renovado", a.OK, 0), (25, 50, "watchdog sin renovar", a.AMB, 0), (50, 75, "60 s: reset", a.BAD, 0)]:
    at(a, a.text(72, 313, t, 15, col if col != a.OK else "#7FE0B0", a.MONO, 700), s, e, st)
at(a, a.text(1000, 446, "si no esperara: dos VMs", 15, a.BAD, a.SANS, 700, "middle") + a.text(1000, 466, "escribiendo el mismo disco", 15, a.BAD, a.SANS, 700, "middle"), 25, 75, 0)
caption(a, 616, [(0, 25, "Cada nodo con servicios en HA renueva su watchdog mientras tiene quórum.", None),
                 (25, 50, "Aislado, pve1 puede seguir escribiendo en el storage: arrancar la VM en otro lado ahora la rompería.", a.AMB),
                 (50, 75, "El watchdog vence y reinicia el nodo: así se garantiza que la VM vieja ya no escribe.", a.BAD),
                 (75, 100, "Recién entonces la HA la arranca en otro nodo. Por eso exige quórum, storage compartido y fencing.", a.OK)], still=3)
write(a, "10-t2.svg", "Fencing: primero se apaga el nodo, después se mueve la VM",
      "Animación en cuatro tiempos de un clúster de tres nodos con alta disponibilidad y almacenamiento compartido. "
      "1: la VM 100 corre en pve1, escribe en el storage y pve1 renueva su watchdog porque tiene quórum. "
      "2: pve1 pierde la red del clúster y queda sin quórum; no puede renovar el watchdog y la VM sigue escribiendo, así que arrancarla en otro nodo la rompería. "
      "3: a los 60 segundos el watchdog reinicia pve1 y la VM vieja deja de escribir. "
      "4: con pve1 fuera, la HA arranca la VM 100 en pve2 sobre el mismo disco compartido.", pcts=(12, 37, 62, 90))
