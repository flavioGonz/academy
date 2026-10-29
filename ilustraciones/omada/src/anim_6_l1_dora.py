#!/usr/bin/env python3
"""Lección 6 · Laboratorio, paso 4: ipconfig /renew en el puerto 5. El DHCP de la VLAN 20 (Discover, Offer, Request, Ack)
viaja sin etiqueta entre la notebook y el puerto 5, y con la etiqueta 20 por el uplink."""
from _anim_om_red import *

a = nueva(24, "VLAN COMPLETA", "ipconfig /renew en el puerto 5: el DHCP de la VLAN 20", "l")
F = a.steps([
    "Discover: sale sin etiqueta del puerto 5 y el switch lo sube por el uplink con la 20.",
    "Offer: el DHCP de 10.10.20.1 ofrece 10.10.20.100; en el puerto 5 llega sin etiqueta.",
    "Request y Ack: la notebook pide esa dirección y el gateway la confirma.",
    "ipconfig | findstr IPv4 muestra 10.10.20.x: las tres patas de la VLAN andan.",
], still=3)

XN, XS, XG = 170, 560, 990
a.add(dev(a, 48, 172, 244, 58, "Notebook", icon="laptop"))
a.add(dev(a, 438, 172, 244, 58, "Switch", icon="server"))
a.add(dev(a, 828, 172, 324, 58, "Gateway · 10.10.20.1", icon="server", dark=True))
a.add(lifeline(a, XN, 230, 470) + lifeline(a, XS, 230, 470) + lifeline(a, XG, 230, 470))
a.add(a.text((XN + XS) / 2, 254, "puerto 5 · CCTV · sin etiqueta", 15, a.GREY, a.MONO, 400, "middle"))
a.add(a.text((XS + XG) / 2, 254, "uplink · All · etiqueta 20", 15, a.CYAN, a.MONO, 600, "middle"))


def par(y, label, t, color, back=False, still=1):
    if not back:
        msg(a, XN, XS, y, label, t, color=color, still=still, dur=2)
        msg(a, XS, XG, y, f"{label} · 20", t + 2.5, color=color, still=still, dur=2)
    else:
        msg(a, XG, XS, y, f"{label} · 20", t, color=color, still=still, dur=2)
        msg(a, XS, XN, y, label, t + 2.5, color=color, still=still, dur=2)


par(300, "Discover", 4, a.AMB)
par(350, "Offer 10.10.20.100", 28, a.OK, back=True)
par(400, "Request", 54, a.BLUE)
par(450, "Ack", 62, a.OK, back=True)

# terminal
TX, TY = 48, 486
a.add(a.box(TX, TY, 640, 96, a.INK, rx=14))
a.add(a.text(TX + 20, TY + 32, "PS> ipconfig /renew", 15, a.WHITE, a.MONO))
a.add(a.text(TX + 20, TY + 56, "PS> ipconfig | findstr IPv4", 15, a.WHITE, a.MONO))
at(a, a.text(TX + 20, TY + 80, "Dirección IPv4. . . . . . : 10.10.20.100", 15, MINT, a.MONO, 600), 76, 100, still=1)

at(a, note(a, 720, TY, 432, 96, "Si no hay respuesta", ["El Discover llegó hasta donde está la", "falla: revisá gateway, uplink y puerto."], "info"), 0, 50)
at(a, note(a, 720, TY, 432, 96, "La etiqueta la pone y la saca el switch", ["La notebook nunca ve el número de VLAN:", "para ella es una red común."], "ok"), 50, 100, still=1)

write(a, 6, "l1", "El DHCP de la VLAN 20, sin etiqueta y con etiqueta",
      "Diagrama de mensajes animado entre la notebook conectada al puerto 5 (perfil CCTV), el switch y el gateway con la interfaz 10.10.20.1 de la VLAN 20. "
      "Entre la notebook y el puerto 5 los mensajes van sin etiqueta; por el uplink, con perfil All, van con la etiqueta 20. "
      "1: ipconfig /renew dispara el Discover, que sale sin etiqueta y el switch sube por el uplink con la 20. "
      "2: el DHCP de 10.10.20.1 responde con el Offer de 10.10.20.100, que vuelve con la 20 por el uplink y sin etiqueta en el puerto 5. "
      "3: la notebook manda el Request por esa dirección y el gateway la confirma con el Ack. "
      "4: ipconfig | findstr IPv4 muestra 10.10.20.100: la interfaz y el DHCP del gateway, el uplink y el puerto de acceso andan. "
      "La etiqueta la pone y la saca el switch; la notebook nunca ve el número de VLAN.",
      [10, 36, 62, 90])
