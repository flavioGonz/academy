#!/usr/bin/env python3
"""Lección 6 · Laboratorio, paso 3: Power Cycle del puerto PoE de la cámara. La cámara reinicia y pide IP sin etiqueta;
el puerto (Native VLAN CCTV 30, Tagged VLAN Management Block All) la pone en la VLAN 30; por el uplink viaja con
etiqueta 30; el DHCP del gateway en la VLAN 30 contesta y el switch saca la etiqueta antes de entregarla.
Fuentes: lab.md (pasos 1 a 3) y theory_md de la lección (nativa y etiquetadas, IEEE 802.1Q); RFC 2131 (DHCP)."""
from _anim_red_unifi import *  # noqa

a = new(24, "Puertos con perfil", "Power Cycle: la cámara pide IP y cae en su VLAN", [
    "Power Cycle: el switch corta el PoE del puerto y la cámara se reinicia.",
    "La cámara pide IP sin etiqueta; el puerto la pone en la VLAN 30, su nativa.",
    "El DHCP de la VLAN 30 contesta; el switch saca la etiqueta antes de entregarla.",
    "La cámara queda en 192.168.30.11 sin saber nada de VLAN.",
], still=3, paso=3)

Y, H = 200, 100
YL = Y + 50
CAM = a.box(48, Y, 250, H, a.WHITE, a.LINE, rx=14) + glyph(a, "camera", 66, Y + 18) + a.text(110, Y + 34, "Cámara", 19, a.INK, a.SANS, 600)
a.add(CAM)
vis(a, a.text(110, Y + 58, "reiniciando", 15, a.AMB, a.MONO, 600), 0)
vis(a, a.text(110, Y + 58, "sin IP", 15, a.GREY, a.MONO), 1, 2)
vis(a, a.text(110, Y + 58, "192.168.30.11", 15, a.OK, a.MONO, 600), 3)

a.add(a.box(420, Y, 340, H, a.WHITE, a.LINE, rx=14) + glyph(a, "server", 438, Y + 18)
      + a.text(482, Y + 34, "Switch · puerto 5", 19, a.INK, a.SANS, 600)
      + a.text(482, Y + 58, "Native: CCTV (VLAN 30)", 15, a.GREY, a.MONO)
      + a.text(482, Y + 80, "Tagged: Block All", 15, a.GREY, a.MONO))
a.add(dev(a, 880, Y, 272, H, "Gateway UniFi", "DHCP de la VLAN 30", icon="server", dark=True, sub2="192.168.30.1/24"))
a.add(wire(298, YL, 420, YL, a.BLUE, 4))
a.add(wire(760, YL, 880, YL, a.BLUE, 4))
a.add(a.text(359, Y + H + 26, "sin etiqueta", 15, a.GREY, a.MONO, 400, "middle"))
a.add(a.text(820, Y + H + 26, "VID 30", 15, a.CYAN, a.MONO, 600, "middle"))
a.add(a.text(359, Y + H + 48, "acceso", 15, a.GREY, a.SANS, 400, "middle"))
a.add(a.text(820, Y + H + 48, "uplink", 15, a.GREY, a.SANS, 400, "middle"))

LN = 392
a.add(wire(173, LN, 1016, LN, a.LINE, 2, "3 7"))
for cx in (173, 590, 1016):
    a.add(wire(cx, Y + H, cx, LN, a.LINE, 2, "3 7"))

# 1 · PoE
s0, s1 = ph(a, 0)
bolt_on = glyph(a, "bolt", 344, Y + 4, a.AMB, 1.2)
during(a, bolt_on, 0, s0 + 6)
during(a, bolt_on.replace(a.AMB, a.LINE) + a.text(359, Y - 4, "PoE cortado", 15, a.BAD, a.MONO, 600, "middle"), s0 + 6, s0 + 14)
during(a, bolt_on + a.text(359, Y - 4, "PoE vuelve", 15, a.OK, a.MONO, 600, "middle"), s0 + 14, s1)
during(a, a.box(48, Y, 250, H, "#FFFFFF", None, rx=14, extra='opacity=".55"'), s0 + 6, s0 + 14)

# 2 · Discover sin etiqueta → VLAN 30
s0, s1 = ph(a, 1)
go(a, [(173, LN), (590, LN)], s0 + 2, s0 + 7, "Discover", a.GREY, hold=s0 + 7)
during(a, pill(a, 590, Y + H + 14, "sin etiqueta → nativa VLAN 30", "info", anchor="middle"), s0 + 6, s1)
go(a, [(590, LN), (1016, LN)], s0 + 10, s0 + 15, "Discover · 30", a.CYAN, hold=s0 + 16)

# 3 · Offer/Ack vuelve
s0, s1 = ph(a, 2)
go(a, [(1016, LN), (590, LN)], s0 + 2, s0 + 7, "Offer · 30", a.CYAN, hold=s0 + 8)
during(a, pill(a, 590, Y + H + 14, "saca la etiqueta 30", "info", anchor="middle"), s0 + 7, s1)
go(a, [(590, LN), (173, LN)], s0 + 10, s0 + 15, "Offer", a.OK, hold=s0 + 16)
during(a, a.text(600, 450, "Lo mismo con Request y Ack: el puerto agrega y saca la etiqueta en cada trama.", 16, a.INK, a.SANS, 600, "middle"),
       s0 + 4, s1)

# 4 · resultado
s0, s1 = ph(a, 3)
during(a, check(a, 285, Y, 15), s0 + 1, 100, still=1)
during(a, nbox(a, 48, 464, 520, 120, "Verificá en el controlador", ["La cámara aparece con una IP de", "192.168.30.0/24. Si toma otra, revisá la", "Native VLAN del puerto."], "ok"),
       s0 + 2, 100, still=1)
during(a, nbox(a, 600, 464, 552, 120, "Block All", ["Si la cámara (o lo que enchufen) manda una", "trama con etiqueta de otra VLAN, el puerto", "la descarta."], "info"),
       s0 + 4, 100, still=1)

status(a, 628, [
    (0, 25, "Power Cycle reinicia lo que se alimenta por ese puerto.", a.INK, 0),
    (25, 50, "La cámara manda tramas comunes: la VLAN la decide el puerto.", a.INK, 0),
    (50, 75, "Etiqueta solo en el uplink: al equipo final le llega sin etiqueta.", a.INK, 0),
    (75, 100, "Nativa CCTV y Block All: la cámara anda igual y no pide otra VLAN.", a.OK, 1),
])

write(a, 6, "l1", "Power Cycle y DHCP en la VLAN de la cámara",
      "Animación en cuatro tiempos del paso 3 con la cámara, el puerto 5 del switch (Native VLAN CCTV 30, Tagged VLAN Management Block All) y el gateway UniFi con el DHCP de la VLAN 30 (192.168.30.1/24). "
      "1: Power Cycle corta el PoE del puerto y lo devuelve; la cámara se reinicia. "
      "2: la cámara pide IP con un DHCP Discover sin etiqueta; el puerto lo pone en la VLAN 30, su nativa, y por el uplink viaja con la etiqueta 30. "
      "3: el DHCP de la VLAN 30 contesta con el Offer etiquetado 30 y el switch saca la etiqueta antes de entregarlo; lo mismo pasa con Request y Ack. "
      "4: la cámara queda en 192.168.30.11 sin saber nada de VLAN; se verifica en el controlador que tome una IP de 192.168.30.0/24, "
      "y con Block All una trama que llegue con etiqueta de otra VLAN se descarta.",
      [12, 40, 64, 90])
