#!/usr/bin/env python3
"""Lección 5 · Resumen, "Cómo se ve en la red": un sitio adopta un solo gateway. El ER de la sucursal no entra
en el sitio de la central; va en su propio sitio, y Auto IPsec une los dos sitios del mismo controlador."""
from _anim_om_red import *

a = nueva(26, "SITIOS Y CLIENTES", "Llega el segundo router: un sitio, un gateway")
F = a.steps([
    "En el sitio Central están el ER de la central, su switch y su EAP.",
    "El ER de la sucursal aparece en Pending: en Central ya hay un gateway y no tiene lugar.",
    "Se crea el sitio Sucursal, con región Uruguay y su zona horaria, y el ER se adopta ahí.",
    "Cada sitio con sus redes, SSID y roaming; Auto IPsec une los dos sitios del controlador.",
], still=3)

TOP, BOT = 186, 572
a.add(a.box(48, TOP, 252, BOT - TOP, a.WHITE, a.LINE, rx=16))
a.add(a.text(68, TOP + 32, "Devices · Pending", 16, a.GREY, a.SANS, 600))
a.add(a.box(330, TOP, 370, BOT - TOP, a.WHITE, a.LINE, rx=16, sw=2))
a.add(a.text(350, TOP + 32, "Sitio Central", 17, a.INK, a.SANS, 600))
a.add(dev(a, 350, 236, 330, 64, "ER central", "gateway del sitio", icon="server", dark=True))
a.add(dev(a, 350, 312, 330, 64, "Switch", icon="server"))
a.add(dev(a, 350, 388, 330, 64, "EAP", "SSID Oficina", icon="wifi"))
at(a, a.text(350, 490, "Sus redes, sus SSID y su ACL.", 15, a.TXT, a.SANS)
   + a.text(350, 514, "Roaming: entre sus EAP.", 15, a.TXT, a.SANS), 0, 26)
at(a, a.text(350, 490, "Sus redes, sus SSID y su ACL.", 15, a.TXT, a.SANS)
   + a.text(350, 514, "Roaming: entre sus EAP.", 15, a.TXT, a.SANS), 50, 100, still=1)

# sitio Sucursal: lugar vacío y después creado
at(a, a.box(790, TOP, 362, BOT - TOP, a.SLATE, a.LINE, rx=16, sw=2, extra='stroke-dasharray="7 6"')
   + a.text(971, 380, "todavía no hay", 17, a.GREY, a.SANS, 600, "middle")
   + a.text(971, 406, "otro sitio", 17, a.GREY, a.SANS, 600, "middle"), 0, 52)
at(a, a.box(790, TOP, 362, BOT - TOP, a.WHITE, a.OK, rx=16, sw=2)
   + a.text(810, TOP + 32, "Sitio Sucursal", 17, a.INK, a.SANS, 600)
   + chip(a, 810, TOP + 46, "Uruguay · America/Montevideo", a.OK, a.OKBG)
   + a.text(810, 490, "Su propio gateway, sus redes", 15, a.TXT, a.SANS)
   + a.text(810, 514, "y sus SSID.", 15, a.TXT, a.SANS), 52, 100, still=1)
at(a, dev(a, 810, 388, 322, 64, "EAP sucursal", "adoptado acá", icon="wifi"), 76, 100, still=1)

# el ER de la sucursal viaja
CARD = dev(a, 0, 0, 232, 64, "ER sucursal", "Pending", icon="server", stroke=a.AMB)
mv = a.move([(0, 58, 236), (27, 58, 236), (33, 360, 470), (40, 360, 470), (45, 58, 236), (55, 58, 236), (61, 810, 300), (100, 810, 300)])
a.add(a.group(CARD, mv, a.show(26, 62, 0.8), still=0))
at(a, dev(a, 810, 300, 322, 64, "ER sucursal", "gateway del sitio", icon="server", dark=True), 61.5, 100, still=1)
at(a, xmark(a, 624, 502, 16) + a.text(515, 556, "Central ya tiene gateway", 15, a.BAD, a.SANS, 600, "middle"), 33, 44)

# 4: Auto IPsec entre sitios
TUN = (f'<path d="M680 268 C 740 268, 760 332, 810 332" fill="none" stroke="{a.CYAN}" stroke-width="5" stroke-linecap="round"/>'
       + a.text(745, 392, "Auto", 15, a.CYAN, a.MONO, 600, "middle") + a.text(745, 412, "IPsec", 15, a.CYAN, a.MONO, 600, "middle"))
at(a, TUN, 78, 100, still=1)

status(a, 618, [
    (0, 25, "El sitio es la unidad de configuración: equipos, redes, SSID, ACL y reglas.", a.INK, 0),
    (25, 50, "Con todo en un solo sitio funciona hasta que llega el segundo gateway.", a.BAD, 0),
    (50, 75, "Cada sede con su router es un sitio. Región y zona horaria, al crearlo.", a.INK, 0),
    (75, 100, "Un SSID de un sitio no roamea al otro; el túnel une las LAN de los dos.", a.INK, 1),
], x=48, anchor="start", size=16)

write(a, 5, "r1", "Un sitio adopta un solo gateway",
      "Animación en cuatro tiempos con la lista de Pending del controlador, el sitio Central y el lugar para un segundo sitio. "
      "1: en el sitio Central están el ER de la central como gateway, su switch y su EAP con el SSID Oficina; el sitio tiene sus redes, SSID y ACL, y el roaming es entre sus EAP. "
      "2: el ER de la sucursal aparece en Pending; al querer llevarlo al sitio Central no hay lugar, porque Central ya tiene gateway. "
      "3: se crea el sitio Sucursal con región Uruguay y zona horaria America/Montevideo, y el ER de la sucursal se adopta ahí como su gateway. "
      "4: el EAP de la sucursal se adopta en ese sitio; cada sitio tiene sus redes, SSID y roaming, y Auto IPsec une los dos sitios del mismo controlador.",
      [8, 36, 62, 92])
