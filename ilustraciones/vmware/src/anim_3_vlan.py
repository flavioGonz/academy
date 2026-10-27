"""Teoría lección 3: el port group etiqueta, el troncal transporta, el segundo uplink sostiene."""
from _avmw import *

a = new(24, "La etiqueta la pone el port group, no la VM")
a.steps(["La VM manda una trama común; el port group le pone la etiqueta 20.",
         "Por el troncal viaja etiquetada y el switch la entrega en la VLAN 20.",
         "Gestión va en VLAN 0: la trama sale sin etiqueta, a la VLAN nativa.",
         "Se suelta vmnic3: el vSwitch sigue por vmnic2 y la VM ni se entera."], still=1)

# host
a.add(card(a, 48, 170, 640, 420, "Host ESXi", None, dark=True))
a.add(vmbox(a, 80, 220, 200, 60, "VM video", "VM-VLAN20"))
a.add(a.box(80, 300, 200, 50, a.NAVY2, a.CYAN, rx=10) + a.text(96, 331, "PG VLAN 20", 16, "#FFFFFF", a.MONO, 600))
a.add(a.box(360, 220, 280, 60, a.NAVY2, "#4E7396", rx=12) + a.text(378, 246, "vmk0 · gestión", 16, "#FFFFFF", a.SANS, 600) + a.text(378, 268, "Management Network", 13, "#9FC3E3", a.MONO))
a.add(a.box(360, 300, 280, 50, a.NAVY2, a.CYAN, rx=10) + a.text(376, 331, "PG VLAN 0", 16, "#FFFFFF", a.MONO, 600))
a.add(a.box(80, 390, 560, 50, "#0E4A80", a.CYAN, rx=10) + a.text(360, 422, "vSwitch", 17, "#FFFFFF", a.MONO, 700, "middle"))
a.add(line(a, "M180 280V300M180 350V390M500 280V300M500 350V390", a.CYAN, 3))
for x, n in [(150, "vmnic2"), (430, "vmnic3")]:
    a.add(a.box(x, 480, 120, 44, "#0B3A66", "#4E7396", rx=8) + a.text(x + 60, 508, n, 15, "#FFFFFF", a.MONO, 600, "middle"))
    a.add(line(a, f"M{x + 60} 440V480", a.CYAN, 3))
# cables al switch
a.add(line(a, "M210 524V560 Q210 580 230 580H760", a.BLUE, 4))
c2 = line(a, "M490 524V548 Q490 568 510 568H760", a.BLUE, 4)
a.add(a.group(c2, a.show(0, 75), still=1))
at(a, line(a, "M490 524V536", a.BAD, 4) + chip(a, 560, 530, "vmnic3 sin link", "bad"), 75, 100, 0)
# switch físico
a.add(card(a, 760, 470, 392, 130, "Switch físico", "bocas en troncal"))
a.add(card(a, 790, 200, 340, 70, "Gateway VLAN 20", "192.0.2.1 (ej.)"))
a.add(card(a, 790, 300, 340, 70, "Red nativa", "sin etiqueta"))

FR = '<rect x="-34" y="-15" width="68" height="30" rx="8" fill="#FFB020" stroke="#fff" stroke-width="2"/>'
TAG = '<rect x="-34" y="-15" width="68" height="30" rx="8" fill="#FFB020" stroke="#fff" stroke-width="2"/><rect x="18" y="-22" width="32" height="22" rx="6" fill="#0A63B8"/><text x="34" y="-6" font-family="JetBrains Mono" font-size="14" font-weight="700" fill="#fff" text-anchor="middle">20</text>'
# 1: trama sin etiqueta de la VM al port group, aparece la etiqueta
a.add(a.group(FR, a.move([(0, 180, 250), (4, 180, 250), (12, 180, 325), (25, 180, 325), (100, 180, 325)]), a.keyframes([(0, 0), (3, 0), (4, 1), (13, 1), (14, 0), (100, 0)]), still=0))
a.add(a.group(TAG, a.move([(0, 180, 325), (14, 180, 325), (20, 180, 415), (26, 210, 560), (36, 760, 580), (44, 960, 535), (49, 960, 240), (100, 960, 240)]), a.keyframes([(0, 0), (13, 0), (14, 1), (49, 1), (50, 0), (100, 0)]), still=0))
at(a, chip(a, 790, 404, "etiqueta 802.1Q con VLAN 20", "info"), 8, 50, 0)
# 3: gestión sin etiqueta
a.add(a.group(FR, a.move([(0, 500, 250), (52, 500, 250), (56, 500, 325), (60, 500, 415), (64, 490, 560), (68, 760, 568), (71, 960, 535), (74, 960, 335), (100, 960, 335)]), a.keyframes([(0, 0), (51, 0), (52, 1), (74, 1), (75, 0), (100, 0)]), still=0))
at(a, chip(a, 790, 404, "VLAN 0 = sin etiqueta", "grey"), 52, 75, 0)
# 4: failover por vmnic2
a.add(a.group(TAG, a.move([(0, 180, 325), (77, 180, 325), (81, 180, 415), (85, 210, 560), (91, 760, 580), (95, 960, 535), (98, 960, 240), (100, 960, 240)]), a.keyframes([(0, 0), (76, 0), (77, 1), (98, 1), (99, 0), (100, 0)]), still=0))
at(a, chip(a, 790, 404, "el ping sigue", "ok"), 85, 100, 0)
# cuadro fijo: la trama etiquetada viajando por el troncal
a.add(a.group(TAG.replace('x="-34" y="-15"', 'x="566" y="565"').replace('x="18" y="-22"', 'x="618" y="558"').replace('x="34" y="-6"', 'x="634" y="574"'), a.keyframes([(0, 0), (100, 0)]), still=1))
caption(a, 640, [(0, 25, "La VM no sabe de VLAN: la etiqueta se la pone el vSwitch según el port group.", None),
                 (25, 50, "El puerto del switch tiene que estar en troncal con la VLAN 20 permitida.", None),
                 (50, 75, "Si cambiás la VLAN de gestión y el switch no la tiene, el host queda sin acceso.", a.AMB),
                 (75, 100, "Dos uplinks en el vSwitch: un cable suelto no corta el servicio.", a.OK)], still=1)
write(a, "3-t1.svg", "La etiqueta la pone el port group, no la VM",
      "Animación en cuatro tiempos de un host ESXi con un vSwitch, dos port groups (VLAN 20 para la VM de video y VLAN 0 para la gestión, vmk0) y dos uplinks, vmnic2 y vmnic3, hacia un switch físico en troncal. "
      "1: la VM manda una trama sin etiqueta y al pasar por el port group recibe la etiqueta 802.1Q con VLAN 20. "
      "2: la trama etiquetada viaja por el troncal y el switch la entrega al gateway de la VLAN 20. "
      "3: la trama de gestión, en VLAN 0, sale sin etiqueta y el switch la pone en la red nativa; si se cambia esa VLAN sin que el switch la tenga, el host queda sin acceso. "
      "4: se suelta el cable de vmnic3 y el tráfico sigue por vmnic2: el ping no se corta.")
