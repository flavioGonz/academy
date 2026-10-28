#!/usr/bin/env python3
"""Lección 9 (Nombre, no puerta) · Laboratorio paso 3: public-address contra la IP de la WAN, y hasta dónde llega un paquete de afuera en cada caso."""
from _anim_r20_31 import *

a, _ = nuevo(27, "MIKROTIK · NOMBRE, NO PUERTA · PASO 3", "Dos IP comparadas: hasta dónde llega el paquete",
             ["Iguales: el router tiene la IP pública y el paquete llega hasta él.",
              "WAN privada y otra public-address: el módem hace NAT y el paquete muere ahí.",
              "WAN en 100.64.0.0/10: CGNAT. El NAT del proveedor no sabe a quién darlo.",
              "Detrás de CGNAT, el camino lo abre el router hacia afuera."], still=3)

COLS = [("IP pública directa", 48), ("NAT del módem", 424), ("CGNAT del proveedor", 800)]
W = 352
for t, x in COLS:
    a.add(a.box(x, 176, W, 300, a.WHITE, a.LINE, rx=16))
    a.add(a.text(x + W / 2, 206, t, 18, a.INK, a.HEAD, 600, "middle"))
    a.add(a.pill(x + W / 2, 222, "internet", a.GREY, a.SLATE, 13, 26, anchor="middle"))

def caja(x, y, t, s, kind="pc"):
    dev(a, x + 26, y, W - 52, 64, t, s, kind=kind, tsize=16, ssize=14)

# columna 1
caja(48, 270, "MikroTik", "WAN 203.0.113.10", "router")
a.add(a.text(48 + 26, 368, "public-address 203.0.113.10", 14, a.TXT, a.MONO))
a.add(a.text(48 + 26, 390, "= IP de la WAN", 14, a.OK, a.MONO, 600))
# columna 2
caja(424, 270, "Módem del proveedor", "203.0.113.20 · hace NAT", "isp")
caja(424, 350, "MikroTik", "WAN 192.168.1.2", "router")
a.add(a.text(424 + 26, 436, "public-address 203.0.113.20", 14, a.TXT, a.MONO))
a.add(a.text(424 + 26, 458, "≠ WAN privada", 14, a.AMB, a.MONO, 600))
# columna 3
caja(800, 270, "CGNAT", "una IP para muchos clientes", "isp")
caja(800, 350, "MikroTik", "WAN 100.64.12.34", "router")
a.add(a.text(800 + 26, 436, "WAN en 100.64.0.0/10", 14, a.TXT, a.MONO))
a.add(a.text(800 + 26, 458, "= CGNAT", 14, a.BAD, a.MONO, 600))

def dot(c):
    return f'<circle cx="0" cy="0" r="10" fill="{c}" stroke="#FFFFFF" stroke-width="2.5"/>'

cx = [x + W / 2 for _, x in COLS]
# 1
go(a, "", [(cx[0], 236), (cx[0], 270)], 3, 7, hold=17, inner=dot(a.BLUE))
en(a, ring(a, 48 + 23, 267, W - 46, 70, a.OK, rx=16), 7, 25)
# 2
go(a, "", [(cx[1], 236), (cx[1], 270)], 28, 32, hold=17, inner=dot(a.BLUE))
en(a, mark(a, cx[1] + 120, 302, ok=False), 32, 50)
# 3
go(a, "", [(cx[2], 236), (cx[2], 270)], 53, 57, hold=17, inner=dot(a.BLUE))
en(a, mark(a, cx[2] + 120, 302, ok=False), 57, 75)

# resultados (se suman)
RES = [("Se puede publicar con cuidado:", "un dst-nat del MikroTik alcanza.", a.OK, a.OKBG, 9),
       ("Modo bridge en el módem, o el", "reenvío también en el módem.", a.AMB, a.AMBBG, 34),
       ("Sin port forwarding posible:", "túnel saliente o Back To Home.", a.BAD, a.BADBG, 59)]
for i, (l1, l2, c, bg, t) in enumerate(RES):
    x = COLS[i][1]
    en(a, a.box(x, 492, W, 84, bg, rx=14) + a.text(x + 20, 524, l1, 15, c, a.SANS, 600) + a.text(x + 20, 548, l2, 15, a.INK, a.SANS), t, 100, still=1)

# 4. el router abre hacia afuera
en(a, a.arrow("M1139 370 V240", a.OK, 3.5, "8 6"), 78, 100, still=1)
en(a, a.text(1128, 248, "saliente", 14, a.OK, a.MONO, 600, "end"), 80, 100, still=1)
en(a, ring(a, 797, 173, W + 6, 306, a.OK, rx=18, sw=3), 78, 100, still=1)

narr(a, [
    (0, 25, "Si public-address es la IP de la WAN, no hay nada traduciendo antes.", a.OK),
    (25, 50, "Un reenvío en el MikroTik no alcanza si el módem no reenvía también.", a.AMB),
    (50, 75, "Al proveedor no se le puede pedir que reenvíe un puerto de su CGNAT.", a.BAD),
    (75, 100, "Lo que abre el router sí vuelve: en eso se apoyan el túnel y Back To Home.", a.OK),
], still_idx=3)

escribir(a, "9-l1.svg", "public-address contra la WAN",
         "Animación en cuatro tiempos con tres columnas. IP pública directa: el MikroTik tiene WAN 203.0.113.10 y public-address es la misma. NAT del módem: el módem del proveedor tiene 203.0.113.20 "
         "y hace NAT; la WAN del MikroTik es 192.168.1.2. CGNAT: la WAN del MikroTik es 100.64.12.34, dentro de 100.64.0.0/10. 1: en la primera, un paquete de afuera llega hasta el router: "
         "se puede publicar con cuidado y un dst-nat alcanza. 2: en la segunda, el paquete muere en el módem: hace falta modo bridge o el reenvío también en el módem. "
         "3: en la tercera, muere en el CGNAT, que no sabe a cuál de sus clientes darlo: no hay port forwarding posible. "
         "4: detrás de CGNAT, el camino lo abre el router hacia afuera, con un túnel saliente o Back To Home.",
         [12, 40, 62, 70, 92])
