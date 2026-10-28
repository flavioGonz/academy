#!/usr/bin/env python3
"""Lección 13 · Resumen, "Cómo se ve en la red": el primer ping de una PC de la LAN a internet con la WAN en IP fija.
Ruta por defecto al gateway 203.0.113.9 (vecino en el /29), ARP en ether1, masquerade de la defconf
(out-interface-list=WAN) que cambia el origen a 203.0.113.10, y la vuelta."""
from _anim_red_1_9 import *

a = Anim(T=26, kicker="MIKROTIK · IP FIJA · CÓMO SE VE EN LA RED", title="IP fija: el primer paquete a internet, paso a paso")
a.steps([
    "Una PC de la LAN hace ping a 1.1.1.1 y se lo manda a su gateway, el MikroTik.",
    "No hay ruta más específica: 0.0.0.0/0 lo manda a 203.0.113.9, vecino en ether1.",
    "Para entregárselo al gateway, el router pregunta por ARP su MAC en ether1.",
    "Sale con origen 203.0.113.10 por el masquerade, y la respuesta vuelve a la PC.",
], still=3)

PC, MT, GW, NET = 140, 452, 800, 1074
a.add(dev(a, 48, 178, 200, 78, "PC de la LAN", "192.168.88.10", icon="laptop"))
a.add(dev(a, 300, 178, 304, 78, "MikroTik", "ether1 203.0.113.10/29", icon="server", dark=True))
a.add(dev(a, 668, 178, 264, 78, "Gateway proveedor", "203.0.113.9", icon="server"))
a.add(dev(a, 984, 178, 168, 78, "Internet", "1.1.1.1", icon="cloud"))
for x in (PC, MT, GW, NET):
    a.add(lifeline(a, x, 256, 572))

# 1
msg(a, PC, MT, 304, "a 1.1.1.1", 4, sub="src 192.168.88.10")
# 2 · decisión de ruta
TX, TW, TY = 300, 304, 340
tab = (a.box(TX, TY, TW, 96, a.WHITE, a.LINE, rx=14)
       + a.text(TX + 16, TY + 26, "/ip/route", 15, a.GREY, a.MONO)
       + a.text(TX + 16, TY + 52, "DAc 203.0.113.8/29 ether1", 15, a.INK, a.MONO, 600)
       + a.box(TX + 8, TY + 60, TW - 16, 28, a.OKBG, rx=6)
       + a.text(TX + 16, TY + 80, "0.0.0.0/0 gw 203.0.113.9", 15, a.OK, a.MONO, 600))
a.add(during(a, tab, 26, 100, still=1))
a.add(during(a, a.text(GW + 20, TY + 40, "el .9 está dentro del /29:", 15, a.TXT, a.SANS, 600)
             + a.text(GW + 20, TY + 62, "se alcanza directo por ether1", 15, a.TXT, a.SANS, 600), 30, 50))
# 3 · ARP
msg(a, MT, GW, 476, "ARP ¿quién tiene 203.0.113.9?", 52, color=a.AMB, dash="8 6", end=76, still=0)
msg(a, GW, MT, 520, "ARP: 203.0.113.9 es mi MAC", 61, color=a.OK, end=76, still=0)
# 4 · salida con masquerade y vuelta
msg(a, MT, GW, 476, "src 203.0.113.10", 78)
msg(a, GW, NET, 476, "a 1.1.1.1", 81)
msg(a, NET, GW, 520, "respuesta", 85, color=a.OK)
msg(a, GW, MT, 520, "a 203.0.113.10", 88, color=a.OK)
msg(a, MT, PC, 560, "a 192.168.88.10", 91, color=a.OK)
a.add(during(a, a.pill(MT - 14, 462, "masquerade", a.BLUE, "#E3EEF9", 15, 28, "end"), 78, 100, still=1))

status(a, 628, [
    (0, 25, "1.1.1.1 no es de la LAN: la PC usa su gateway, 192.168.88.1.", a.INK, 0),
    (25, 50, "Por eso la máscara importa: con el gateway fuera del /29, no habría a quién mandarlo.", a.INK, 0),
    (50, 75, "Sin respuesta al ARP, ni el ping al gateway funciona: cable, máscara o VLAN.", a.AMB, 0),
    (75, 100, "El masquerade de la defconf sale por la lista WAN; conntrack devuelve la respuesta a la PC.", a.OK, 1),
], size=17)

write(a, 13, "r1", "El primer paquete con IP fija",
      "Animación en cuatro tiempos con cuatro líneas de vida: una PC de la LAN (192.168.88.10), el MikroTik (ether1 203.0.113.10/29), el gateway del proveedor (203.0.113.9) e internet (1.1.1.1). "
      "1: la PC hace ping a 1.1.1.1 y se lo manda a su gateway, el MikroTik. "
      "2: el router busca en /ip/route: no hay ruta más específica y 0.0.0.0/0 apunta a 203.0.113.9, que está dentro de la ruta conectada 203.0.113.8/29 de ether1. "
      "3: antes de entregarlo, pregunta por ARP en ether1 quién tiene 203.0.113.9 y el gateway contesta con su MAC; si no contesta, el problema es de cable, máscara o VLAN. "
      "4: el paquete sale con origen 203.0.113.10 por el masquerade de la configuración por defecto, llega a 1.1.1.1, la respuesta vuelve a 203.0.113.10 "
      "y el router se la devuelve a 192.168.88.10.",
      [8, 36, 60, 70, 95])
