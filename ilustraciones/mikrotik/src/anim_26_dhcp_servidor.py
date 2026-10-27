#!/usr/bin/env python3
"""Lección 26 · Asignar IP. Teoría "Cómo funciona", DHCP en cuatro mensajes visto desde el servidor del router:
antes del Offer prueba la dirección con ARP y ping; con authoritative=yes contesta NAK enseguida a quien pide
una dirección que no le corresponde.
"""
from _anim_mikrotik_14_26 import Anim, node, lifeline, msg, out

a = Anim(T=28, kicker="MIKROTIK · SERVIDOR DHCP", title="El servidor prueba antes de ofrecer, y corta rápido")
a.steps([
    "Una cámara nueva grita un Discover por broadcast.",
    "Antes del Offer, RouterOS prueba la dirección con ARP y ping.",
    "Offer, Request y Ack: la cámara queda con 10.10.20.100.",
    "Llega un equipo que pide una dirección de otra red: NAK enseguida.",
    "Con el NAK empieza de nuevo con un Discover, sin esperar.",
], still=2)

LX, RX_, OX = 170, 600, 1010
a.add(a.group(node(a, 48, 176, 244, 68, "Cámara nueva", "ether5"), a.show(0, 60), still=1))
a.add(a.group(node(a, 48, 176, 244, 68, "Notebook", "venía de otra red"), a.show(60, 100), still=0))
a.add(node(a, 478, 176, 244, 68, "MikroTik", "dhcp-cctv · ether5", dark=True))
a.add(node(a, 888, 176, 244, 68, "Otros equipos", "en ether5"))
for x in (LX, RX_, OX):
    a.add(lifeline(a, x, 244, 584))

# fase A
msg(a, LX, RX_, 296, "Discover", 3, end=60, sub="broadcast", still=1)
msg(a, RX_, OX, 356, "ARP y ping a 10.10.20.100", 22, end=60, color=a.AMB, still=1)
a.add(a.group(a.text((RX_ + OX) / 2, 392, "nadie contesta: está libre", 15, a.AMB, a.SANS, 600, "middle"), a.show(28, 60), still=1))
msg(a, RX_, LX, 432, "Offer · 10.10.20.100", 42, end=60, still=1)
msg(a, LX, RX_, 486, "Request", 47, end=60, still=1)
msg(a, RX_, LX, 540, "Ack · lease", 52, end=60, color=a.OK, still=1)
a.add(a.group(a.pill(LX, 556, "10.10.20.100", a.OK, a.OKBG, 15, 28, "middle"), a.show(54, 60), still=1))

# fase B
msg(a, LX, RX_, 296, "Request · 192.168.1.50", 63, still=0, sub="la que tenía en otra red")
msg(a, RX_, LX, 380, "NAK", 69, color=a.BAD, still=0, sub="authoritative=yes: no te corresponde")
msg(a, LX, RX_, 466, "Discover", 82, still=0, sub="empieza de nuevo")
msg(a, RX_, LX, 548, "Offer · 10.10.20.101", 90, still=0)

# nota
NY = 626
NOTES = [(0, 40, "La cámara no tiene dirección todavía: por eso grita a todos."),
         (40, 60, "Pool pool-cctv: del .100 al .199. La IP del router queda afuera."),
         (60, 80, "Sin authoritative=yes, el equipo esperaría antes de rendirse."),
         (80, 100, "Discover, Offer, Request y Ack otra vez, ahora con una dirección de esta red.")]
for s_, e, t in NOTES:
    a.add(a.group(a.text(48, NY, t, 17, a.INK, a.SANS, 600), a.show(s_, e), still=1 if s_ == 40 else 0))

out(a, 26, 2, "Servidor DHCP: prueba, Offer y NAK",
    "Animación en cinco tiempos con tres líneas de vida: un equipo en ether5, el MikroTik con el servidor dhcp-cctv y los otros equipos de ether5. "
    "1: una cámara nueva manda Discover por broadcast. "
    "2: antes del Offer, RouterOS prueba la dirección 10.10.20.100 con ARP y ping; nadie contesta, está libre. "
    "3: el servidor manda Offer con 10.10.20.100, la cámara pide con Request y el servidor confirma con Ack y el lease; queda con 10.10.20.100. "
    "4: llega una notebook que pide 192.168.1.50, la dirección que tenía en otra red; con authoritative=yes el servidor contesta NAK enseguida. "
    "5: la notebook empieza de nuevo con un Discover, sin esperar, y recibe un Offer de esta red.",
    [8, 30, 56, 74, 94])
