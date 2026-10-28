#!/usr/bin/env python3
"""Lección 26 · Laboratorio, paso 3: por qué ether5 va a la lista LAN. Sin eso, la consulta DNS de la cámara al
router (UDP 53 a 10.10.20.1) muere en "drop all not coming from LAN"; con ether5 en LAN, el DNS del router
(allow-remote-requests=yes en la defconf) contesta. Reglas de input de la defconf de RouterOS 7."""
from _anim_red_1_9 import *

a = Anim(T=26, kicker="MIKROTIK · ASIGNAR IP · LABORATORIO", title="Por qué ether5 va a la lista LAN")
a.steps([
    "La cámara en ether5 le pregunta un nombre al router: DNS a 10.10.20.1.",
    "En input no es ICMP ni respuesta: cae en drop all not coming from LAN.",
    "/interface/list/member/add list=LAN interface=ether5: ether5 pasa a ser LAN.",
    "La misma consulta pasa el drop y el DNS del router contesta.",
], still=3)

CM, RT = 170, 560
a.add(dev(a, 48, 178, 250, 82, "Cámara", "10.10.20.100", icon="camera"))
a.add(dev(a, 420, 178, 290, 82, "Router", "ether5 10.10.20.1/24", icon="server", dark=True))
a.add(lifeline(a, CM, 260, 570))
a.add(lifeline(a, RT, 260, 570))

msg(a, CM, RT, 318, "DNS · UDP 53", 4, end=50, still=0, sub="¿dirección de un nombre?")
a.add(during(a, xmark(a, RT + 28, 318), 30, 50))
a.add(during(a, a.text(CM - 100, 384, "sin respuesta: la cámara no resuelve", 15, a.BAD, a.MONO, 600), 32, 50))
# lista
LX, LY = 48, 410
lst = (a.box(LX, LY, 662, 92, a.INK, rx=14)
       + a.text(LX + 18, LY + 34, "/interface/list/member/add list=LAN interface=ether5", 15, a.WHITE, a.MONO)
       + a.text(LX + 18, LY + 66, "lista LAN: bridge, ether5", 15, MINT, a.MONO, 600))
a.add(during(a, lst, 52, 100, still=1))
msg(a, CM, RT, 540, "DNS · UDP 53", 78)
msg(a, RT, CM, 578, "respuesta DNS", 87, color=a.OK)

# cadena input
CX, CY, CW = 752, 178, 400
a.add(a.box(CX, CY, CW, 412, a.WHITE, a.LINE, rx=16))
a.add(a.text(CX + 20, CY + 32, "/ip/firewall/filter · input", 16, a.INK, a.MONO, 600))
R = ["accept established,related", "drop invalid", "accept ICMP", "accept to local loopback", "drop all not coming from LAN"]
RH = 52
for i, r in enumerate(R):
    y = CY + 50 + i * (RH + 8)
    a.add(a.box(CX + 16, y, CW - 32, RH, a.SLATE, rx=8))
    a.add(a.text(CX + 32, y + 32, f"{i + 1}  {r}", 15, a.INK, a.MONO, 600))


def scan(t0, upto, final_col, final_end, still_last):
    for i in range(upto + 1):
        y = CY + 50 + i * (RH + 8)
        last = i == upto
        col = final_col if last else a.GREY
        end = final_end if last else t0 + (i + 1) * 1.6
        a.add(during(a, a.box(CX + 14, y - 2, CW - 28, RH + 4, "none", col, rx=9, sw=3 if last else 2), t0 + i * 1.6, end, still=1 if (last and still_last) else 0))


scan(18, 4, a.BAD, 50, False)
scan(80, 4, a.OK, 100, True)
a.add(during(a, a.text(CX + 20, CY + 360, "in-interface-list=!LAN: ether5 coincide", 15, a.BAD, a.SANS, 600)
             + a.text(CX + 20, CY + 384, "y se descarta", 15, a.BAD, a.SANS, 600), 26, 50))
a.add(during(a, a.text(CX + 20, CY + 360, "ether5 ya es LAN: no coincide, sigue", 15, a.OK, a.SANS, 600)
             + a.text(CX + 20, CY + 384, "y el DNS del router contesta", 15, a.OK, a.SANS, 600), 88, 100, still=1))

a.add(a.text(48, 640, "Lo mismo vale para WinBox y para cualquier servicio del router que la red de cámaras tenga que usar.", 16, a.TXT, a.SANS, 600))

write(a, 26, "l1", "La red de cámaras y la lista LAN",
      "Animación en cuatro tiempos entre una cámara en ether5 (10.10.20.100) y el router (10.10.20.1/24 en ether5), con las reglas de input de la configuración por defecto. "
      "1: la cámara manda una consulta DNS por UDP 53 a 10.10.20.1. "
      "2: en input no coincide con accept established,related, drop invalid, accept ICMP ni accept to local loopback, y cae en la 5, drop all not coming from LAN, "
      "porque ether5 no está en la lista LAN: la cámara no resuelve. "
      "3: /interface/list/member/add list=LAN interface=ether5 suma ether5 a la lista LAN, junto al bridge. "
      "4: la misma consulta ya no coincide con el drop y el DNS del router, que en la configuración por defecto acepta pedidos remotos, contesta. "
      "Lo mismo vale para WinBox y otros servicios del router.",
      [10, 36, 62, 92])
