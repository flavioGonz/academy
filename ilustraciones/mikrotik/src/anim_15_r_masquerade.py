#!/usr/bin/env python3
"""Lección 15 · Resumen, "Cómo se ve en la red": con PPPoE la WAN es pppoe-antel. Si el masquerade quedó con
out-interface=ether1, el router navega pero la LAN no: sus paquetes salen con origen privado y nadie contesta.
Con out-interface-list=WAN y pppoe-antel en la lista, vuelve todo (concepto de la lección)."""
from _anim_red_1_9 import *

a = Anim(T=26, kicker="MIKROTIK · PPPOE CON ANTEL · CÓMO SE VE EN LA RED", title="Con PPPoE, el masquerade tiene que mirar a pppoe-antel")
a.steps([
    "El PPPoE marcó: la IP pública quedó en pppoe-antel, no en ether1.",
    "El router navega: sus propios paquetes salen con la IP de pppoe-antel.",
    "La LAN no: el masquerade dice out-interface=ether1 y el paquete sale por pppoe-antel.",
    "Con out-interface-list=WAN y pppoe-antel en la lista, el origen cambia y vuelve.",
], still=3)

Y0, H = 186, 104
a.add(dev(a, 48, Y0, 196, H, "PC de la LAN", "192.168.88.10", icon="laptop"))
RX, RW = 300, 380
a.add(a.box(RX, Y0, RW, H, a.INK, rx=16))
a.add(glyph(a, "server", RX + 18, Y0 + 14, a.CYAN))
a.add(a.text(RX + 62, Y0 + 32, "MikroTik", 19, a.WHITE, a.SANS, 600))
a.add(a.box(RX + 16, Y0 + 46, RW - 32, 24, a.NAVY2, rx=6))
a.add(a.text(RX + 28, Y0 + 63, "pppoe-antel", 15, MINT, a.MONO, 600))
a.add(during(a, a.text(RX + RW - 28, Y0 + 63, "203.0.113.77", 15, MINT, a.MONO, 600, "end"), 4, 100, still=1))
a.add(a.box(RX + 16, Y0 + 74, RW - 32, 24, "#12385C", rx=6))
a.add(a.text(RX + 28, Y0 + 91, "ether1", 15, SKY, a.MONO))
a.add(a.text(RX + RW - 28, Y0 + 91, "solo el puerto físico", 15, SKY, a.MONO, 400, "end"))
a.add(dev(a, 742, Y0, 184, H, "ONT", "modo puente", icon="server"))
a.add(dev(a, 986, Y0, 166, H, "Antel", "internet", icon="cloud"))
YL = Y0 + H / 2
a.add(line(244, YL, RX, YL, a.BLUE, 4))
a.add(line(RX + RW, YL, 742, YL, a.BLUE, 4))
a.add(line(926, YL, 986, YL, a.BLUE, 4))

dot = lambda c: f'<circle cx="0" cy="0" r="9" fill="{c}" stroke="{a.WHITE}" stroke-width="2"/>'
OUTP = [(RX + RW + 8, YL), (978, YL)]
BACK = [(978, YL + 0.1), (RX + RW + 8, YL + 0.1)]
# 2 · el router navega
a.add(travel(a, dot(a.OK), OUTP, 28, 34, hold=0.3))
a.add(travel(a, dot(a.OK), BACK, 36, 42, hold=0.3))
# 3 · la PC no
a.add(travel(a, dot(a.BLUE), [(252, YL), (292, YL)], 52, 54, hold=0.2))
a.add(travel(a, dot(a.BAD), OUTP, 58, 64, hold=10))
a.add(during(a, xmark(a, 956, YL - 36), 64, 76))
# 4 · arreglado
a.add(travel(a, dot(a.BLUE), [(252, YL), (292, YL)], 78, 80, hold=0.2))
a.add(travel(a, dot(a.OK), OUTP, 83, 88, hold=0.3))
a.add(travel(a, dot(a.OK), BACK, 89, 94, hold=0.3))
a.add(travel(a, dot(a.OK), [(292, YL), (252, YL)], 95, 97, hold=2))

# ---------- paquete al salir
PY, PW = 320, 528
a.add(a.box(48, PY, PW, 168, a.WHITE, a.LINE, rx=16))
a.add(a.text(68, PY + 32, "Paquete que sale por pppoe-antel", 17, a.INK, a.SANS, 600))
CARDS = [
    (0, 25, [("PPPoE conectado", a.INK), ("local-address=203.0.113.77", a.OK)], 0),
    (25, 50, [("del router: /ping 1.1.1.1", a.INK), ("src 203.0.113.77 · contesta", a.OK)], 0),
    (50, 75, [("de la PC: src 192.168.88.10", a.INK), ("sale igual, con origen privado", a.BAD), ("del otro lado nadie le contesta", a.BAD)], 0),
    (75, 100, [("de la PC: src 192.168.88.10", a.INK), ("masquerade: src 203.0.113.77", a.OK), ("la respuesta vuelve a la PC", a.OK)], 1),
]
for t0, t1, ls, st in CARDS:
    body = "".join(a.text(68, PY + 70 + j * 32, t, 16, c, a.MONO, 600) for j, (t, c) in enumerate(ls))
    a.add(during(a, body, t0, t1, still=st))

# ---------- regla de NAT
NX, NW = 600, 552
a.add(a.box(NX, PY, NW, 168, a.INK, rx=16))
a.add(a.text(NX + 20, PY + 32, "/ip/firewall/nat", 16, SKY, a.MONO, 600))
a.add(a.text(NX + 20, PY + 66, "chain=srcnat action=masquerade", 16, a.WHITE, a.MONO))
a.add(during(a, a.text(NX + 20, PY + 96, "out-interface=ether1", 16, GOLD, a.MONO, 600), 0, 76))
a.add(during(a, a.text(NX + 20, PY + 130, "el paquete sale por pppoe-antel: no coincide", 15, "#FF9E8A", a.SANS, 600), 54, 76))
a.add(during(a, a.text(NX + 20, PY + 96, "out-interface-list=WAN", 16, MINT, a.MONO, 600)
             + a.text(NX + 20, PY + 132, "/interface/list/member/add list=WAN", 15, SKY, a.MONO)
             + a.text(NX + 52, PY + 154, "interface=pppoe-antel", 15, SKY, a.MONO), 76, 100, still=1))

status(a, 528, [
    (0, 25, "ether1 queda como el cable: la sesión PPPoE y la IP viven en la interfaz lógica.", a.INK, 0),
    (25, 50, "Por eso el router parece andar bien: sus paquetes ya salen con la IP pública.", a.OK, 0),
    (50, 75, "La regla no mira la interfaz por donde sale de verdad: no hay NAT para la LAN.", a.BAD, 0),
    (75, 100, "Masquerade, lista WAN y reglas de firewall apuntan a pppoe-antel por la lista.", a.OK, 1),
], size=17)
a.add(note(a, 48, 556, 1104, 64, "", ["En la defconf el masquerade ya usa out-interface-list=WAN: alcanza con sumar pppoe-antel a la lista WAN."], "info"))

write(a, 15, "r1", "Masquerade con PPPoE",
      "Animación en cuatro tiempos con la cadena PC de la LAN (192.168.88.10), MikroTik, ONT en modo puente y Antel. Dentro del MikroTik, pppoe-antel con 203.0.113.77 y ether1 como puerto físico. "
      "1: el PPPoE marcó y la IP pública, local-address 203.0.113.77, quedó en pppoe-antel, no en ether1. "
      "2: el propio router hace ping a 1.1.1.1: sale con origen 203.0.113.77 y le contestan. "
      "3: un paquete de la PC sale por pppoe-antel, pero la regla de masquerade dice out-interface=ether1 y no coincide; "
      "el paquete sale con origen privado 192.168.88.10 y nadie le contesta. "
      "4: con la regla en out-interface-list=WAN y /interface/list/member/add list=WAN interface=pppoe-antel, el origen pasa a 203.0.113.77 y la respuesta vuelve a la PC. "
      "En la configuración por defecto el masquerade ya usa la lista WAN: alcanza con sumar pppoe-antel a la lista.",
      [8, 36, 62, 70, 92])
