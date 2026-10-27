"""Teoría lección 2: una trama recorre VM, bridge VLAN-aware y trunk, ida y vuelta."""
from _apmx import *

a = new(20, "Cómo viaja una trama por un bridge VLAN-aware")
a.steps(["La VM 100 manda una trama común, sin etiqueta.",
         "En vmbr0, su puerto tap100i0 la mete en la VLAN 10.",
         "Sale por bond0 al trunk del switch con el tag 10.",
         "Una trama con tag 20 solo llega a la VM 101, sin tag."], still=1)
# VMs
a.add(card(a, 48, 254, 230, 92, "VM 100", "net0 · tag 10"))
a.add(card(a, 48, 434, 230, 92, "VM 101", "net0 · tag 20"))
# bridge
a.add(a.box(380, 176, 400, 384, a.INK, None, rx=18))
a.add(a.text(404, 212, "vmbr0 · VLAN aware", 20, "#FFFFFF", a.HEAD, 600))
a.add(a.text(404, 236, "el switch virtual del host", 15, "#9FC3E3", a.MONO, 400))
a.add(a.text(846, 342, "bond0", 15, a.INK, a.MONO, 700, "middle") + a.text(846, 364, "2-4094", 15, a.GREY, a.MONO, 600, "middle"))
for y, lab, ly in [(300, "tap100i0 · PVID 10", 272), (480, "tap101i0 · PVID 20", 530)]:
    a.add(a.box(368, y - 18, 24, 36, a.CYAN, None, rx=6))
    a.add(a.text(404, ly, lab, 15, "#D9E9F8", a.MONO, 600))
a.add(a.box(768, 372, 24, 36, a.CYAN, None, rx=6))
a.add(line(a, "M278 300H368", a.BLUE, 4))
a.add(line(a, "M278 480H368", a.BLUE, 4))
a.add(line(a, "M392 300 C 580 300, 600 390, 768 390", "#4E7396", 3, "6 6"))
a.add(line(a, "M392 480 C 580 480, 600 390, 768 390", "#4E7396", 3, "6 6"))
a.add(line(a, "M792 390H900", a.BLUE, 4))
# switch
a.add(card(a, 900, 300, 252, 200, "Switch", "puerto trunk"))
a.add(a.text(920, 384, "VLAN 10 y 20", 15, a.GREY, a.MONO, 600))


def frame(lbl, kind):
    fg, bg = {"plain": (a.INK, "#FFFFFF"), "10": ("#FFFFFF", a.OK), "20": ("#FFFFFF", a.AMB)}[kind]
    return a.box(-58, -18, 116, 36, bg, a.INK if kind == "plain" else None, rx=10, sw=2) + a.text(0, 6, lbl, 15, fg, a.MONO, 700, "middle")


# tiempo 1: trama sin tag de la VM al puerto
a.add(a.group(frame("sin tag", "plain"), a.move([(0, 220, 300), (4, 220, 300), (22, 330, 300), (25, 330, 300)]), a.show(0, 25), still=0))
# tiempo 2: en el bridge, con tag 10
a.add(a.group(frame("VLAN 10", "10"), a.move([(25, 480, 300), (29, 480, 300), (47, 690, 385), (50, 690, 385)]), a.show(25, 50), still=1))
# tiempo 3: sale al switch
a.add(a.group(frame("tag 10", "10"), a.move([(50, 720, 390), (54, 720, 390), (72, 1026, 450), (75, 1026, 450)]), a.show(50, 75), still=0))
# tiempo 4: entra tag 20 y va solo a la VM 101
a.add(a.group(frame("tag 20", "20"), a.move([(75, 1026, 450), (78, 1026, 450), (86, 690, 395), (88, 690, 395)]), a.show(75, 88), still=0))
a.add(a.group(frame("sin tag", "plain"), a.move([(88, 330, 480), (90, 330, 480), (98, 200, 562), (100, 200, 562)]), a.show(88, 100), still=0))
at(a, chip(a, 48, 356, "no la ve: es VLAN 20", "bad"), 80, 100, still=0)
caption(a, 600, [(0, 25, "La VM no sabe de VLAN: arma tramas comunes. El tag lo pone Proxmox, no el sistema invitado.", None),
                 (25, 50, "El puerto de la VM tiene PVID 10: todo lo que entra por ahí queda en la VLAN 10.", a.OK),
                 (50, 75, "bond0 lleva 2 a 4094 etiquetadas: el switch recibe la trama con tag 10 en el trunk.", a.OK),
                 (75, 100, "Al volver, el bridge entrega cada VLAN solo a sus puertos y saca la etiqueta.", a.AMB)], still=1)
write(a, "2-t1.svg", "Cómo viaja una trama por un bridge VLAN-aware",
      "Animación en cuatro tiempos sobre un bridge vmbr0 VLAN aware con dos VM. 1: la VM 100 manda una trama común, sin etiqueta, hacia su puerto tap100i0. "
      "2: ese puerto tiene PVID 10, así que dentro del bridge la trama queda en la VLAN 10. 3: sale por bond0, que lleva las VLAN 2 a 4094 etiquetadas, hacia el puerto trunk del switch con el tag 10. "
      "4: una trama con tag 20 que vuelve del switch solo se entrega por tap101i0 a la VM 101, ya sin etiqueta; la VM 100 no la ve.")
