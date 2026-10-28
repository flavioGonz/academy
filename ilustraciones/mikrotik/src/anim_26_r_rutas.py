#!/usr/bin/env python3
"""Lección 26 · Resumen, "Cómo se ve en la red": la notebook de la LAN llega a una cámara de la red nueva de
ether5. Dos IP en el router, dos rutas conectadas (DAc); ARP en ether5 antes de entregar.
La defconf no corta LAN -> ether5 en forward (solo lo nuevo que entra por WAN sin dst-nat)."""
from _anim_red_1_9 import *

a = Anim(T=24, kicker="MIKROTIK · ASIGNAR IP · CÓMO SE VE EN LA RED", title="De la LAN a las cámaras: dos rutas conectadas")
a.steps([
    "La notebook quiere ver la cámara: 10.10.20.100 no es de su red, va al gateway.",
    "El router mira /ip/route: 10.10.20.0/24 es una ruta conectada por ether5.",
    "La red está al lado: pregunta por ARP en ether5 quién tiene 10.10.20.100.",
    "Entrega el paquete en ether5; la respuesta vuelve por el mismo camino.",
], still=3)

NXc, RXc, CXc = 160, 600, 1040
a.add(dev(a, 48, 178, 224, 78, "Notebook", "192.168.88.254/24", icon="laptop"))
a.add(dev(a, 440, 178, 320, 78, "MikroTik", "bridge .88.1 · ether5 .20.1", icon="server", dark=True))
a.add(dev(a, 928, 178, 224, 78, "Cámara", "10.10.20.100/24", icon="camera"))
for x in (NXc, RXc, CXc):
    a.add(lifeline(a, x, 256, 590))
a.add(a.text(NXc, 280, "bridge · LAN", 15, a.GREY, a.MONO, 400, "middle"))
a.add(a.text(CXc, 280, "ether5 · cámaras", 15, a.GREY, a.MONO, 400, "middle"))

# 1 · al gateway
msg(a, NXc, RXc, 318, "a 10.10.20.100", 4, sub="no es de 192.168.88.0/24: al gateway .1")
# 2 · tabla de rutas
TX, TW, TY = 420, 360, 362
tab = (a.box(TX, TY, TW, 104, a.WHITE, a.LINE, rx=14)
       + a.text(TX + 18, TY + 28, "/ip/route · conectadas", 15, a.GREY, a.MONO)
       + a.text(TX + 18, TY + 56, "DAc 192.168.88.0/24  bridge", 15, a.INK, a.MONO, 600)
       + a.box(TX + 10, TY + 66, TW - 20, 30, a.OKBG, rx=6)
       + a.text(TX + 18, TY + 87, "DAc 10.10.20.0/24    ether5", 15, a.OK, a.MONO, 600))
a.add(during(a, tab, 26, 100, still=1))
# 3 · ARP
msg(a, RXc, CXc, 500, "ARP ¿quién tiene 10.10.20.100?", 54, color=a.AMB, dash="8 6", end=76, still=0)
msg(a, CXc, RXc, 544, "ARP: 10.10.20.100 es mi MAC", 63, color=a.OK, end=76, still=0)
# 4 · entrega y vuelta, en las mismas filas
msg(a, RXc, CXc, 500, "a 10.10.20.100", 78)
msg(a, CXc, RXc, 544, "respuesta", 84, color=a.OK)
msg(a, RXc, NXc, 544, "respuesta", 89, color=a.OK)

status(a, 636, [
    (0, 25, "La notebook no conoce la red de las cámaras: le manda el paquete a su gateway, el router.", a.INK, 0),
    (25, 50, "No hizo falta agregar ninguna ruta: cada IP cargada en una interfaz crea su ruta conectada.", a.INK, 0),
    (50, 75, "Antes de entregar en una red conectada, el router averigua la MAC del destino por ARP.", a.AMB, 0),
    (75, 100, "El router enruta entre sus dos redes: ninguna regla de la defconf corta de la LAN a ether5.", a.OK, 1),
], size=17)

write(a, 26, "r1", "Notebook y cámara en dos redes del mismo router",
      "Animación en cuatro tiempos con tres líneas de vida: la notebook (192.168.88.254/24 en la LAN del bridge), el MikroTik (192.168.88.1 en bridge y 10.10.20.1 en ether5) "
      "y una cámara (10.10.20.100/24 en ether5). "
      "1: la notebook ve que 10.10.20.100 no es de 192.168.88.0/24 y manda el paquete a su gateway, el router. "
      "2: el router mira sus rutas conectadas, DAc 192.168.88.0/24 por bridge y DAc 10.10.20.0/24 por ether5, y usa la segunda; no hizo falta agregar ninguna ruta. "
      "3: como la red está conectada, pregunta por ARP en ether5 quién tiene 10.10.20.100 y la cámara contesta con su MAC. "
      "4: el router entrega el paquete en ether5, la cámara contesta y la respuesta vuelve a la notebook. "
      "Ninguna regla de la configuración por defecto corta el tráfico de la LAN a ether5.",
      [8, 36, 58, 68, 92])
