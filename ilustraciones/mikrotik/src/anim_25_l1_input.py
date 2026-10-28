#!/usr/bin/env python3
"""Lección 25 · Laboratorio, paso 3: ether5 fuera del bridge con 10.10.50.1/24 y la notebook en 10.10.50.2/24.
ARP resuelve, el ping entra por "accept ICMP" (antes del drop) y el SYN de WinBox muere en
"drop all not coming from LAN" porque ether5 no está en la lista LAN. Reglas de input de la defconf (RouterOS 7)."""
from _anim_red_1_9 import *

a = Anim(T=26, kicker="MIKROTIK · UN SOLO BRIDGE · LABORATORIO", title="ether5 fuera del bridge: el ping entra, WinBox no")
a.steps([
    "La notebook (10.10.50.2) averigua por ARP la MAC de 10.10.50.1.",
    "ping 10.10.50.1: en input, la regla accept ICMP lo deja pasar. Contesta.",
    "WinBox: el SYN al 8291 sigue de largo hasta drop all not coming from LAN.",
    "ether5 no está en la lista LAN. Hasta que la sumes, WinBox no entra por ahí.",
], still=2)

NB, RT = 170, 560
a.add(dev(a, 48, 178, 250, 82, "Notebook", "10.10.50.2/24", icon="laptop"))
a.add(dev(a, 420, 178, 290, 82, "Router", "ether5 10.10.50.1/24", icon="server", dark=True))
a.add(lifeline(a, NB, 260, 568))
a.add(lifeline(a, RT, 260, 568))
a.add(a.text(RT, 284, "fuera del bridge", 15, a.GREY, a.MONO, 400, "middle"))

msg(a, NB, RT, 320, "ARP ¿quién tiene .50.1?", 3, color=a.AMB, dash="8 6", end=25, still=0)
msg(a, RT, NB, 358, "ARP: .50.1 es mi MAC", 10, color=a.OK, end=25, still=0)
msg(a, NB, RT, 410, "ICMP echo", 28, end=100)
msg(a, RT, NB, 448, "echo reply", 41, color=a.OK, end=100)
msg(a, NB, RT, 500, "TCP SYN :8291", 53, color=a.BLUE, end=100)
msg(a, NB, RT, 538, "SYN de nuevo", 66, color=a.BLUE, end=100, dash="8 6")
for y, t0 in ((500, 60), (538, 70)):
    a.add(during(a, xmark(a, RT + 28, y), t0, 100, still=1))
a.add(during(a, a.text(NB - 100, 590, "sin SYN-ACK: WinBox no conecta", 15, a.BAD, a.MONO, 600), 72, 100, still=1))

# cadena input
CX, CY, CW = 752, 178, 400
a.add(a.box(CX, CY, CW, 390, a.WHITE, a.LINE, rx=16))
a.add(a.text(CX + 20, CY + 32, "/ip/firewall/filter · input", 16, a.INK, a.MONO, 600))
R = ["accept established,related", "drop invalid", "accept ICMP", "accept to local loopback", "drop all not coming from LAN"]
RH = 52
for i, r in enumerate(R):
    y = CY + 50 + i * (RH + 8)
    a.add(a.box(CX + 16, y, CW - 32, RH, a.SLATE, rx=8))
    a.add(a.text(CX + 32, y + 32, f"{i + 1}  {r}", 15, a.INK, a.MONO, 600))


def scan(t0, upto, ok):
    for i in range(upto + 1):
        y = CY + 50 + i * (RH + 8)
        last = i == upto
        col = (a.OK if ok else a.BAD) if last else a.GREY
        dur_end = 76 if last else t0 + (i + 1) * 1.6
        a.add(during(a, a.box(CX + 14, y - 2, CW - 28, RH + 4, "none", col, rx=9, sw=3 if last else 2), t0 + i * 1.6, dur_end, still=1 if (last and not ok) else 0))


scan(31, 2, True)
scan(56, 4, False)
a.add(during(a, a.text(CX + 20, CY + 360, "ICMP coincide en la 3: aceptado", 15, a.OK, a.SANS, 600), 36, 52))
a.add(during(a, a.text(CX + 20, CY + 360, "in-interface-list=!LAN: ether5 coincide", 15, a.BAD, a.SANS, 600), 63, 100, still=1))

a.add(note(a, 48, 610, 1104, 48, "", ["Para WinBox por ether5: /interface/list/member/add list=LAN interface=ether5 (como en la lección Asignar IP)."], "info", lsize=15))

write(a, 25, "l1", "Ping sí, WinBox no, en un puerto fuera del bridge",
      "Animación en cuatro tiempos entre la notebook (10.10.50.2/24) y el router con ether5 fuera del bridge (10.10.50.1/24), con las reglas de input de la configuración por defecto a la derecha. "
      "1: la notebook pregunta por ARP la MAC de 10.10.50.1 y el router contesta. "
      "2: el ping llega a input, pasa por accept established,related y drop invalid sin coincidir y lo acepta la regla 3, accept ICMP; el router contesta. "
      "3: WinBox manda un SYN al puerto 8291; recorre las reglas y coincide con la 5, drop all not coming from LAN, porque ether5 no está en la lista LAN; "
      "el SYN se repite y no hay SYN-ACK. "
      "4: hasta sumar ether5 a la lista LAN con /interface/list/member/add list=LAN interface=ether5, WinBox no entra por ese puerto.",
      [12, 40, 66, 90])
