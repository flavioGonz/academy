#!/usr/bin/env python3
"""Lección 15 · Laboratorio, paso 6: disable y enable del cliente PPPoE. Se cierra la sesión (PADT, RFC 2516),
vuelve el descubrimiento (PADI, PADO, PADR, PADS con un número de sesión nuevo), PPP autentica y IPCP asigna
la IP, que puede ser otra: por eso el acceso remoto va por DDNS o túnel. Direcciones de documentación."""
from _anim_red_1_9 import *

a = Anim(T=26, kicker="MIKROTIK · PPPOE CON ANTEL · LABORATORIO", title="Reconectar el PPPoE puede traer otra IP")
a.steps([
    "disable: el cliente cierra la sesión con PADT y pppoe-antel queda sin IP.",
    "enable: vuelve a buscar al concentrador, que le da un número de sesión nuevo.",
    "Dentro de la sesión, PPP autentica y asigna la IP por IPCP.",
    "local-address cambió: el acceso remoto va por DDNS o por un túnel.",
], still=3)

MT, AC = 230, 880
a.add(dev(a, 48, 176, 364, 78, "MikroTik · pppoe-antel", "sobre ether1", icon="server", dark=True))
a.add(dev(a, 700, 176, 360, 78, "Concentrador de Antel", "al otro lado del ONT", icon="cloud"))
for x in (MT, AC):
    a.add(lifeline(a, x, 254, 528))

msg(a, MT, AC, 294, "PADT · cierra la sesión", 4, color=a.BAD, lsize=15)
msg(a, MT, AC, 344, "PADI · broadcast", 27, lsize=15)
msg(a, AC, MT, 374, "PADO", 31, color=a.OK, lsize=15)
msg(a, MT, AC, 404, "PADR", 35, lsize=15)
msg(a, AC, MT, 434, "PADS · sesión nueva", 39, color=a.OK, lsize=15)
msg(a, MT, AC, 484, "LCP y autenticación", 53, lsize=15)
msg(a, AC, MT, 514, "IPCP: 198.51.100.140", 60, color=a.OK, lsize=15)
a.add(during(a, a.text(AC + 24, 352, "descubrimiento:", 15, a.GREY, a.SANS, 600) + a.text(AC + 24, 374, "como en la teoría", 15, a.GREY, a.SANS, 600), 27, 100, still=1))
a.add(during(a, a.text(AC + 24, 494, "PPP dentro", 15, a.GREY, a.SANS, 600) + a.text(AC + 24, 516, "de la sesión", 15, a.GREY, a.SANS, 600), 53, 100, still=1))

# monitor
PY = 548
a.add(a.box(48, PY, 1104, 92, a.INK, rx=14))
a.add(a.text(66, PY + 34, "/interface/pppoe-client/monitor pppoe-antel once", 15, SKY, a.MONO))
a.add(a.text(66, PY + 68, "local-address:", 16, a.WHITE, a.MONO))
for t0, t1, v, c, st in ((0, 8, "203.0.113.77", a.WHITE, 0), (8, 62, "sin sesión", "#FF9E8A", 0), (62, 100, "198.51.100.140", MINT, 1)):
    a.add(during(a, a.text(230, PY + 68, v, 16, c, a.MONO, 600), t0, t1, still=st))
a.add(during(a, a.text(500, PY + 68, "antes: 203.0.113.77", 16, SKY, a.MONO), 62, 100, still=1))
a.add(during(a, a.text(1134, PY + 68, "otra IP", 16, GOLD, a.MONO, 600, "end"), 64, 100, still=1))
a.add(during(a, a.text(1134, PY + 34, "disable", 15, GOLD, a.MONO, 600, "end"), 2, 25))
a.add(during(a, a.text(1134, PY + 34, "enable", 15, GOLD, a.MONO, 600, "end"), 25, 50))

a.add(a.text(48, 664, "Si la IP cambia en cada sesión, nadie puede apuntar a ella: DDNS o túnel (módulo Entrar de afuera).", 15, a.TXT, a.SANS, 600))

write(a, 15, "l2", "Reconexión PPPoE y cambio de IP",
      "Animación en cuatro tiempos entre el cliente pppoe-antel del MikroTik, sobre ether1, y el concentrador de Antel. "
      "1: /interface/pppoe-client/disable pppoe-antel: el cliente cierra la sesión con PADT y la interfaz queda sin dirección. "
      "2: enable: vuelve el descubrimiento, PADI por broadcast, PADO, PADR y PADS, que trae un número de sesión nuevo. "
      "3: dentro de la sesión se negocia LCP, se autentica y el concentrador asigna la IP por IPCP, en el ejemplo 198.51.100.140. "
      "4: el monitor muestra local-address 198.51.100.140 en vez de 203.0.113.77: la IP cambió, así que el acceso remoto se resuelve con DDNS o con un túnel.",
      [10, 40, 64, 92])
