#!/usr/bin/env python3
"""Lección 11 · Laboratorio, paso 2: cambiar la LAN por defecto del ER de 192.168.0.1/24 a 10.10.20.1/24.
Los clientes siguen con su IP vieja y sin salida hasta renovar; al renovar, el ER rechaza la dirección vieja (NAK)
y el cliente arranca de nuevo con Discover y recibe una 10.10.20.x (RFC 2131)."""
from _anim_om_red import *

a = nueva(26, "TÚNEL ENTRE SEDES", "Cambiás la LAN del ER: los clientes quedan en la vieja", "l")
F = a.steps([
    "El ER de la sucursal pasa de 192.168.0.1/24 a 10.10.20.1/24, como pide el plan.",
    "La PC sigue con 192.168.0.100 y su gateway 192.168.0.1 ya no existe: sin salida.",
    "Al renovar, pide su dirección vieja: el ER no la reconoce y responde NAK.",
    "Arranca de cero: Discover, Offer, Request, Ack. Ahora tiene 10.10.20.x.",
], still=3)

XP, XR = 200, 860
a.add(dev(a, 70, 172, 260, 62, "PC de la sucursal", icon="laptop"))
a.add(dev(a, 730, 172, 260, 62, "ER Sucursal", icon="server", dark=True))
a.add(lifeline(a, XP, 234, 580) + lifeline(a, XR, 234, 580))
# estado de la LAN del ER
at(a, chip(a, XR, 244, "LAN 192.168.0.1/24", a.GREY, a.SLATE, anchor="middle"), 0, 6)
at(a, chip(a, XR, 244, "LAN 10.10.20.1/24", a.OK, a.OKBG, anchor="middle", stroke=a.OK), 6, 100, still=1)
# estado de la PC
at(a, chip(a, XP, 244, "192.168.0.100", a.INK, a.SLATE, anchor="middle"), 0, 25)
at(a, chip(a, XP, 244, "192.168.0.100 · sin salida", a.BAD, a.BADBG, anchor="middle", stroke=a.BAD), 25, 76)
at(a, chip(a, XP, 244, "10.10.20.100", a.OK, a.OKBG, anchor="middle", stroke=a.OK), 88, 100, still=1)

# 2: el ping al gateway viejo
msg(a, XP, XR, 312, "ping 192.168.0.1", 28, color=a.BLUE, end=50, still=0)
at(a, xmark(a, XR - 24, 312, 12) + a.text(XR + 20, 318, "esa IP ya no está", 15, a.BAD, a.SANS, 600), 31, 50)
# 3: renueva y NAK
msg(a, XP, XR, 312, "Request 192.168.0.100", 53, color=a.BLUE)
msg(a, XR, XP, 356, "NAK: esa red no es la mía", 58, color=a.BAD)
# 4: DORA
msg(a, XP, XR, 410, "Discover", 76, color=a.AMB)
msg(a, XR, XP, 450, "Offer 10.10.20.100", 79, color=a.OK)
msg(a, XP, XR, 490, "Request 10.10.20.100", 82, color=a.BLUE)
msg(a, XR, XP, 530, "Ack", 85, color=a.OK)

# panel
NX, NW = 1010, 142
at(a, note(a, 48, 588, 1104, 50, "", ["Hacelo en ventana de mantenimiento: hasta que cada cliente renueva DHCP, queda sin red. Desconectar y reconectar acelera."], "amb"), 0, 100, still=1)

write(a, 11, "l1", "Cambiar la LAN del ER y la renovación DHCP de los clientes",
      "Diagrama de mensajes animado entre una PC de la sucursal y el ER Sucursal. "
      "1: la LAN por defecto del ER pasa de 192.168.0.1/24 a 10.10.20.1/24, según el plan de subredes que no se solapan. "
      "2: la PC sigue con 192.168.0.100 y su gateway 192.168.0.1 ya no existe: un ping no tiene respuesta y no hay salida. "
      "3: al renovar, la PC pide su dirección vieja y el ER responde NAK porque esa red ya no es la suya. "
      "4: la PC arranca de cero con Discover, Offer, Request y Ack y queda con 10.10.20.100. "
      "Como hasta que cada cliente renueva queda sin red, el cambio se hace en ventana de mantenimiento; desconectar y reconectar acelera la renovación.",
      [8, 36, 62, 92])
