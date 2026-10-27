"""Teoría lección 4: el vmkping grande con -d atraviesa cada salto; uno en 1500 lo descarta."""
from _avmw import *

a = new(20, "MTU 9000 de punta a punta, o nada")
a.steps(["vmkping -d -s 8972: sale un paquete de 9000 bytes que no se puede partir.",
         "vmk1 y vSwitch1 en 9000: pasa.",
         "El switch físico quedó en 1500: el paquete grande se descarta.",
         "Con el switch en 9000, el NAS responde: jumbo frames de punta a punta."], still=2)

HOPS = [(48, "vmk1", "10.10.10.21"), (338, "vSwitch1", "uplinks"), (628, "Switch físico", "bocas del NAS"), (918, "NAS", "10.10.10.50")]
for i, (x, t, s) in enumerate(HOPS):
    a.add(card(a, x, 230, 234, 120, t, s))
    if i < 3:
        a.add(line(a, f"M{x + 234} 290H{x + 290}", a.BLUE, 4))
for x in (48, 338, 918):
    a.add(chip(a, x + 20, 312, "MTU 9000", "ok"))
at(a, chip(a, 648, 312, "MTU 1500", "bad") + a.box(628, 230, 234, 120, "none", a.BAD, rx=14, sw=3), 0, 75, 1)
at(a, chip(a, 648, 312, "MTU 9000", "ok"), 75, 100, 0)

PK = '<rect x="-46" y="-22" width="92" height="44" rx="10" fill="#FFB020" stroke="#fff" stroke-width="2"/><text x="0" y="6" font-family="JetBrains Mono" font-size="15" font-weight="700" fill="#04223D" text-anchor="middle">9000</text>'
# intento fallido
a.add(a.group(PK, a.move([(0, 165, 400), (3, 165, 400), (20, 165, 400), (35, 455, 400), (48, 700, 400), (55, 700, 400), (100, 700, 400)]),
              a.keyframes([(0, 0), (2, 0), (3, 1), (52, 1), (56, 0), (100, 0)]), still=0))
at(a, a.text(764, 408, "descartado", 18, a.BAD, a.MONO, 700), 50, 75, 1)
# intento con todo en 9000
a.add(a.group(PK, a.move([(0, 165, 400), (76, 165, 400), (82, 455, 400), (88, 745, 400), (93, 1035, 400), (100, 1035, 400)]),
              a.keyframes([(0, 0), (75, 0), (76, 1), (99, 1), (100, 0)]), still=0))
at(a, chip(a, 918, 440, "respuesta: ok", "ok"), 93, 100, 0)
# cuadro fijo
a.add(a.group(PK.replace('x="-46" y="-22"', 'x="654" y="378"').replace('x="0" y="6"', 'x="700" y="406"'), a.keyframes([(0, 0), (100, 0)]), still=1))
a.add(a.box(48, 480, 1104, 92, a.WHITE, a.LINE, rx=14))
a.add(a.text(72, 516, "vmkping -I vmk1 -d -s 8972 10.10.10.50", 18, a.INK, a.MONO, 600))
a.add(a.text(72, 548, "8972 de datos + 8 de ICMP + 20 de IP = 9000 bytes", 16, a.GREY, a.MONO))
caption(a, 620, [(0, 25, "-d: no fragmentar. Si algo en el camino tiene MTU menor, no pasa.", None),
                 (25, 50, "Dentro del host el MTU se fija en el vmk y en el vSwitch.", None),
                 (50, 75, "El ping normal anda igual: por eso el problema parece intermitente.", a.BAD),
                 (75, 100, "Mismo MTU en vmk, vSwitch, switch y NAS: recién ahí se usa jumbo.", a.OK)], still=2)
write(a, "4-t1.svg", "MTU 9000 de punta a punta, o nada",
      "Animación en cuatro tiempos con cuatro saltos en fila: vmk1, vSwitch1, switch físico y NAS. "
      "1: vmkping con -d y -s 8972 arma un paquete de 9000 bytes que no se puede fragmentar. "
      "2: atraviesa vmk1 y vSwitch1, que están en MTU 9000. "
      "3: el switch físico está en MTU 1500 y el paquete se descarta; el ping normal seguiría andando. "
      "4: con el switch en 9000, el paquete llega al NAS y vuelve la respuesta. Abajo, la cuenta: 8972 de datos más 8 de ICMP más 20 de IP son 9000 bytes.")
