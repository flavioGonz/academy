#!/usr/bin/env python3
"""Lección 14 · Resumen, "Cómo se ve en la red": el módem en modo router le da una IP privada a ether1;
la salida pasa por dos NAT; IP Cloud muestra otra public-address; el acceso remoto desde el celular no llega."""
from _anim_red_1_9 import *

a = Anim(T=26, kicker="MIKROTIK · CLIENTE DHCP · CÓMO SE VE EN LA RED", title="Doble NAT: el acceso remoto no llega al MikroTik")
a.steps([
    "El módem, en modo router, le da por DHCP 192.168.1.10 a ether1: el cliente queda bound.",
    "Al salir, cada paquete pasa por dos NAT: el del MikroTik y el del módem.",
    "IP Cloud ve 203.0.113.45, pero ether1 tiene 192.168.1.10: hay otro NAT adelante.",
    "El celular llama a 203.0.113.45: el módem no sabe a quién pasarlo y se pierde.",
], still=2)

Y0, H = 190, 96
a.add(dev(a, 48, Y0, 212, H, "NVR", "192.168.88.20", icon="camera"))
a.add(dev(a, 312, Y0, 200, H, "MikroTik", "ether1", icon="server", dark=True))
a.add(dev(a, 564, Y0, 222, H, "Módem", "modo router", icon="server", sub2="WAN 203.0.113.45"))
a.add(dev(a, 970, Y0, 182, H, "Celular", "en la calle", icon="phone"))
a.add(a.box(810, Y0 + 10, 136, 76, "#EAF2FA", a.LINE, rx=30, sw=2, extra='stroke-dasharray="7 6"'))
a.add(a.text(878, Y0 + 36, "internet", 15, a.GREY, a.MONO, 400, "middle"))
YL = Y0 + H / 2
a.add(line(260, YL, 312, YL, a.BLUE, 4))
a.add(line(512, YL, 564, YL, a.BLUE, 4))
a.add(line(786, YL, 810, YL, a.BLUE, 4))
a.add(line(946, YL, 970, YL, a.BLUE, 4))
# ether1 recibe la dirección
a.add(during(a, a.text(374, Y0 + 80, "192.168.1.10", 15, GOLD, a.MONO, 600), 12, 100, still=1))
pill_at(a, 312 + 200 - 12, Y0 - 14, "bound", a.OK, a.OKBG, 12, 100, still=1, anchor="end")

dot = lambda c: f'<circle cx="0" cy="0" r="9" fill="{c}" stroke="{a.WHITE}" stroke-width="2"/>'
# 1 · DHCP del módem al MikroTik
a.add(travel(a, dot(a.OK), [(556, YL), (520, YL)], 4, 8, hold=0.5))
a.add(during(a, a.text(538, YL + 76, "DHCP Ack", 15, a.OK, a.MONO, 600, "middle"), 3, 25))
# 2 · la salida y sus dos NAT
a.add(travel(a, dot(a.BLUE), [(266, YL), (306, YL)], 28, 31, hold=0.3))
a.add(travel(a, dot(a.BLUE), [(518, YL), (558, YL)], 33, 36, hold=0.3))
a.add(travel(a, dot(a.BLUE), [(796, YL + 18), (940, YL + 18)], 38, 42, hold=0.3))
CY, CW = 316, 352
CELLS = [("sale del NVR", "src 192.168.88.20", a.WHITE, 28),
         ("NAT 1 · MikroTik", "src 192.168.1.10", GOLD, 33),
         ("NAT 2 · módem", "src 203.0.113.45", MINT, 38)]
for i, (t, v, c, t0) in enumerate(CELLS):
    x = 48 + i * (CW + 24)
    a.add(during(a, a.box(x, CY, CW, 78, a.INK, rx=12)
                 + a.text(x + 18, CY + 30, t, 15, SKY, a.MONO)
                 + a.text(x + 18, CY + 58, v, 17, c, a.MONO, 600), t0, 100, still=1))
# 3 · IP Cloud
PY = 418
cloud = (a.box(48, PY, 640, 168, a.WHITE, a.LINE, rx=16)
         + a.text(68, PY + 34, "/ip/dhcp-client/print detail", 15, a.GREY, a.MONO)
         + a.text(68, PY + 60, "address=192.168.1.10/24", 16, a.INK, a.MONO, 600)
         + a.text(68, PY + 98, "/ip/cloud/print", 15, a.GREY, a.MONO)
         + a.text(68, PY + 124, "public-address: 203.0.113.45", 16, a.INK, a.MONO, 600))
a.add(during(a, cloud, 50, 100, still=1))
a.add(during(a, note(a, 712, PY, 440, 168, "No coinciden: doble NAT", ["192.168.1.10 es privada: alguien más hace", "NAT adelante. Si fuera 100.64.0.0/10,", "sería CGNAT del proveedor."], "amb"), 54, 76, still=1))
# 4 · el celular no llega
a.add(travel(a, dot(a.BAD), [(962, YL + 18), (800, YL + 18)], 79, 84, hold=0.5))
a.add(during(a, xmark(a, 834, YL + 18), 84, 100))
a.add(during(a, note(a, 712, PY, 440, 168, "Antes de prometer acceso remoto", ["El pedido muere en el módem: nunca", "llega a ether1. Salidas: Back To Home", "o un túnel a un concentrador."], "bad"), 78, 100))

status(a, 628, [
    (0, 25, "address de ether1: 192.168.1.10, una dirección privada que dio el módem.", a.INK, 0),
    (25, 50, "Para internet, el sitio es 203.0.113.45: la dirección del módem, no la de tu MikroTik.", a.INK, 0),
    (50, 75, "Compará address con public-address: si son distintas, hay otro NAT adelante.", a.AMB, 1),
    (75, 100, "Abrir puertos en el MikroTik no alcanza: la conexión de afuera no pasa del módem.", a.BAD, 0),
])

write(a, 14, "r1", "Doble NAT con el módem en modo router",
      "Animación en cuatro tiempos con la cadena NVR (192.168.88.20), MikroTik, módem del proveedor en modo router (WAN 203.0.113.45), internet y el celular del cliente. "
      "1: el módem entrega por DHCP 192.168.1.10 a ether1 y el cliente DHCP queda bound. "
      "2: un paquete del NVR sale con src 192.168.88.20, el NAT del MikroTik lo cambia a 192.168.1.10 y el NAT del módem a 203.0.113.45. "
      "3: /ip/dhcp-client/print detail muestra address=192.168.1.10/24 y /ip/cloud/print muestra public-address 203.0.113.45: no coinciden, hay doble NAT; "
      "si la address estuviera en 100.64.0.0/10 sería CGNAT. "
      "4: el celular intenta llegar a 203.0.113.45 y el pedido muere en el módem, que no sabe a quién pasarlo; nunca llega a ether1. "
      "Las salidas son Back To Home o un túnel a un concentrador.",
      [6, 40, 62, 90])
