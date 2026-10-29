#!/usr/bin/env python3
"""Lección 11 · Resumen, "Cómo se ve en la red": la sucursal con el router del proveedor adelante. Auto IPsec no aplica;
con UDP 500 y 4500 abiertos hacia el ER, Manual IPsec arma el túnel (NAT Traversal en 4500). Con el túnel arriba,
el EAP de la sucursal recibe la option 138 con la IP privada del controlador y se adopta por adentro del túnel."""
from _anim_om_red import *

a = nueva(28, "TÚNEL ENTRE SEDES", "Sucursal detrás del router del proveedor: túnel y adopción")
F = a.steps([
    "El ER de la sucursal tiene IP privada en la WAN: el IKE de la central muere en el router del proveedor.",
    "El proveedor abre UDP 500 y 4500 hacia el ER: Manual IPsec, NAT detectado, todo por UDP 4500.",
    "Un EAP nuevo en la sucursal pide IP: la option 138 trae 10.10.10.10, la IP privada del controlador.",
    "El EAP llama a 10.10.10.10 por adentro del túnel y aparece en Pending: sin puertos abiertos.",
], still=3, size=17)

Y, H = 196, 92
YL = Y + H / 2
# túnel (fases 2 a 4), detrás de los equipos
at(a, f'<rect x="250" y="{YL - 22}" width="640" height="44" rx="22" fill="{a.CYAN}" fill-opacity=".18" stroke="{a.CYAN}" stroke-width="2"/>', 40, 100, still=1)
a.add(dev(a, 48, Y, 252, H, "ER Central", "WAN 203.0.113.10", icon="server", dark=True))
a.add(a.box(336, Y + 14, 150, 64, "#EAF2FA", a.LINE, rx=28, sw=2, extra='stroke-dasharray="7 6"') + a.text(411, Y + 52, "internet", 15, a.GREY, a.MONO, 400, "middle"))
a.add(dev(a, 522, Y, 250, H, "Router proveedor", "NAT · 203.0.113.20", icon="server", stroke=a.AMB))
a.add(dev(a, 808, Y, 344, H, "ER Sucursal", "WAN privada 192.168.1.2", icon="server", dark=True))
a.add(line(300, YL, 336, YL, a.BLUE, 4) + line(486, YL, 522, YL, a.BLUE, 4) + line(772, YL, 808, YL, a.BLUE, 4))
# LAN
a.add(dev(a, 48, 420, 252, 92, "Controlador", "10.10.10.10", icon="server", sub2="LAN 10.10.10.0/24"))
a.add(dev(a, 900, 420, 252, 92, "EAP nuevo", "LAN 10.10.20.0/24", icon="wifi"))
a.add(line(174, Y + H, 174, 420, a.BLUE, 3) + line(1026, Y + H, 1026, 420, a.BLUE, 3))

# 1: IKE muere en el proveedor
travel(a, dot(a, a.BLUE, 10), [(240, YL), (560, YL)], 3, 9, hold=0.3)
at(a, a.text(411, Y - 12, "IKE · UDP 500", 15, a.BLUE, a.MONO, 600, "middle"), 2, 25)
at(a, xmark(a, 647, Y + H + 26, 15) + a.text(672, Y + H + 32, "sin regla: no sabe a quién pasarlo", 15, a.BAD, a.SANS, 600), 10, 25)
# 2: con 500 y 4500 abiertos
at(a, chip(a, 647, Y + H + 12, "UDP 500 y 4500 → ER", a.AMB, a.AMBBG, anchor="middle", stroke=a.AMB), 26, 100, still=1)
travel(a, dot(a, a.BLUE, 10), [(240, YL), (900, YL)], 28, 34, hold=0.3)
travel(a, dot(a, a.CYAN, 10), [(900, YL), (240, YL)], 35, 40, hold=0.3)
at(a, a.text(411, Y - 12, "IKE: 500 → 4500 (NAT detectado)", 15, a.CYAN, a.MONO, 600, "middle"), 27, 50)
# 3: option 138
travel(a, pkt(a, "pide IP", a.BLUE), [(1000, 420), (1000, Y + H + 4)], 53, 56, hold=0.2)
travel(a, pkt(a, "option 138: 10.10.10.10", a.OK), [(1052, Y + H + 4), (1052, 420)], 58, 62, hold=1)
at(a, chip(a, 1026, 530, "controlador: 10.10.10.10", a.OK, a.OKBG, anchor="middle", stroke=a.OK), 62, 100, still=1)
# 4: por el túnel
travel(a, pkt(a, "→ 10.10.10.10", a.BLUE), [(1000, 420), (1000, YL + 20)], 77, 79, hold=0.1)
travel(a, dot(a, a.CYAN, 10), [(880, YL), (260, YL)], 80, 86, hold=0.2)
at(a, a.text(411, Y - 12, "ESP en UDP 4500 · cifrado", 15, a.CYAN, a.MONO, 600, "middle"), 77, 100, still=1)
travel(a, pkt(a, "→ 10.10.10.10", a.BLUE), [(174, YL + 30), (174, 420)], 87, 89, hold=0.5)
at(a, chip(a, 174, 530, "Pending", a.AMB, a.AMBBG, anchor="middle", stroke=a.AMB), 89, 100, still=1)

# notas
NX, NY, NW, NH = 336, 420, 528, 120
at(a, note(a, NX, NY, NW, NH, "Auto IPsec pide IP pública en la WAN", ["Con NAT adelante, el ER no recibe lo que llega a", "203.0.113.20 hasta que el router se lo pase."], "bad"), 0, 25)
at(a, note(a, NX, NY, NW, NH, "Manual IPsec", ["Gateway remoto, subredes, clave precompartida y", "Local ID / Remote ID de tipo Name en los dos lados."], "info"), 25, 50)
at(a, note(a, NX, NY, NW, NH, "El DHCP de la sucursal", ["Option 138 con la IP privada del controlador:", "la que solo se alcanza por adentro del túnel."], "ok"), 50, 75)
at(a, note(a, NX, NY, NW, NH, "Sin puertos de gestión en internet", ["Del 29810 al 29817 viajan cifrados por el túnel.", "Verificá en VPN Status > Site-to-Site VPN > IPsec."], "ok"), 75, 100, still=1)

write(a, 11, "r1", "La sucursal detrás del router del proveedor: túnel y adopción por adentro",
      "Animación en cuatro tiempos con el ER Central (WAN 203.0.113.10) y su controlador 10.10.10.10, internet, el router del proveedor que hace NAT (203.0.113.20) "
      "y el ER de la sucursal con IP privada en la WAN (192.168.1.2) y un EAP nuevo en la LAN 10.10.20.0/24. "
      "1: Auto IPsec pide IP pública en la WAN; el IKE por UDP 500 que manda la central muere en el router del proveedor, que no sabe a quién pasarlo. "
      "2: el proveedor abre UDP 500 y 4500 hacia el ER y se arma Manual IPsec con Local ID y Remote ID de tipo Name; los gateways detectan el NAT, pasan a UDP 4500 y el túnel queda arriba. "
      "3: el EAP nuevo pide IP y el DHCP de la sucursal le manda la option 138 con 10.10.10.10, la IP privada del controlador, que solo se alcanza por el túnel. "
      "4: el EAP llama a 10.10.10.10; el paquete viaja cifrado como ESP dentro de UDP 4500 por el túnel y el EAP aparece en Pending, sin puertos de gestión abiertos a internet. "
      "Se verifica en VPN Status, Site-to-Site VPN, IPsec.",
      [8, 36, 60, 84, 95])
