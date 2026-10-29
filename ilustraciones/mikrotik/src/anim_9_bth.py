#!/usr/bin/env python3
"""Lección 9 · teoría: detrás de CGNAT solo funciona lo que abre el router; Back To Home usa un relay que no puede leer el tráfico."""
from _anim_mikrotik_1_13 import *

a = Anim(T=24, kicker="MIKROTIK · BACK TO HOME", title="Detrás de CGNAT, el router es el que llama")
a.steps([
    "Una conexión entrante no llega: el NAT del proveedor no reenvía nada.",
    "El router abre una conexión hacia el relay de MikroTik más cercano.",
    "El celular se conecta a ese relay, que une las dos puntas.",
    "Las claves WireGuard están solo en el router y en el celular: el relay no lee.",
], still=3)

RY = 380
# líneas de base
a.add(line(268, RY, 420, RY, a.BLUE, 3))
a.add(line(700, RY, 880, RY, a.LINE, 3, "6 6"))
a.add(a.text(800, RY - 14, "internet", 13, a.GREY, a.MONO, 400, "middle"))
# conexión saliente persistente router → relay (desde el tiempo 2)
path_out = f"M270 {RY - 20} H560 V250 H860"
a.add(a.group(f'<path d="{path_out}" fill="none" stroke="{a.OK}" stroke-width="4" stroke-dasharray="10 6"/>', a.show(30, 100), still=1))
a.add(a.group(f'<path d="M1000 290 V452" fill="none" stroke="{a.OK}" stroke-width="4" stroke-dasharray="10 6"/>', a.show(55, 100), still=1))

# 1. intento entrante
a.add(travel(a, pkt(a, "entrante", a.BAD, size=14), [(880, RY + 30), (812, RY + 30)], 3, 10, hold=12))
a.add(during(a, xmark(a, 740, RY + 30), 10, 25))
a.add(during(a, a.text(560, RY + 110, "el CGNAT no sabe a cuál de sus clientes mandarlo", 15, a.BAD, a.MONO, 600, "middle"), 10, 25))
# 2. el router abre hacia el relay
a.add(travel(a, pkt(a, "saliente", a.OK, size=14), [(330, RY - 20), (560, RY - 20), (560, 250), (800, 250)], 27, 37, hold=2))
a.add(during(a, a.text(415, 238, "la abre el router", 14, a.OK, a.MONO, 600, "middle"), 30, 100, still=1))
# 3. el celular al relay
a.add(travel(a, pkt(a, "celular", a.OK, size=14), [(1000, 476), (1000, 312)], 52, 58, hold=14))
# 4. tráfico cifrado de punta a punta
for t0 in (77, 85):
    a.add(travel(a, pkt(a, "cifrado", a.INK, size=14), [(1000, 476), (1000, 312), (1000, 250), (860, 250), (560, 250), (560, RY - 20), (330, RY - 20)], t0, t0 + 9, hold=0.5))
a.add(still_only(a, place(a, pkt(a, "cifrado", a.INK, size=14), 700, 250)))

# cajas encima de las líneas
a.add(device(a, 48, 326, 220, 108, "MikroTik", "WAN 100.64.12.34", sub2="claves WireGuard", dark=True, ssize=13))
a.add(device(a, 420, 326, 280, 108, "CGNAT del proveedor", "100.64.0.0/10", sub2="una IP pública, muchos clientes", tsize=17, ssize=13))
a.add(device(a, 860, 186, 292, 104, "Relay de MikroTik", "el más cercano", sub2="pasa paquetes sin leerlos", tsize=17, ssize=13))
a.add(device(a, 900, 452, 252, 100, "Celular", "app Back To Home", sub2="claves WireGuard", ssize=13))
a.add(during(a, a.box(856, 182, 300, 112, "none", a.AMB, rx=16, sw=3), 77, 100, still=1))

a.add(a.text(48, 600, "Detrás de CGNAT solo funcionan las conexiones que abre el propio router hacia afuera.", 16, a.INK, a.SANS, 600))
a.add(a.text(48, 630, "Back To Home se apoya en eso: nadie tiene que abrir un puerto.", 16, a.TXT, a.SANS))

p, pre = out(9, 2)
a.write(p, title="Back To Home detrás de CGNAT",
        desc="Animación en cuatro tiempos con un MikroTik con WAN 100.64.12.34 detrás del CGNAT del proveedor (100.64.0.0/10), el relay de MikroTik más cercano y un "
             "celular con la app Back To Home. 1: una conexión entrante desde internet no llega: el CGNAT no sabe a cuál de sus clientes mandarla. 2: el router abre una "
             "conexión saliente hacia el relay y la mantiene. 3: el celular se conecta al mismo relay, que une las dos puntas. 4: el tráfico viaja cifrado del celular al "
             "router pasando por el relay; las claves WireGuard están solo en el router y en el celular, así que el relay no puede leerlo.",
        preview=[12, 36, 60, 80], prefix=pre)
