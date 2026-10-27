#!/usr/bin/env python3
"""Lección 18 · IP Cloud a fondo. Teoría "Cómo funciona": la nube anota la IP de origen (public-address),
detrás de NAT el router avisa cada minuto, y el TTL de 60 s hace que los demás vean la IP nueva enseguida.
"""
from _anim_mikrotik_14_26 import Anim, node, packet, out

a = Anim(T=28, kicker="MIKROTIK · IP CLOUD", title="La nube anota la IP desde la que le llega el aviso")
a.steps([
    "El router manda su aviso a cloud2.mikrotik.com. El NAT cambia el origen.",
    "La nube anota la IP desde la que llegó: esa es la public-address.",
    "Un técnico resuelve el nombre. La respuesta vale 60 segundos.",
    "El NAT sale con otra IP. El aviso de cada minuto la lleva a la nube.",
    "Vence el TTL: el técnico pregunta de nuevo y ve la IP nueva.",
], still=1)

Y = 178
a.add(node(a, 48, Y, 250, 84, "MikroTik", "ether1 192.168.1.2"))
a.add(a.box(440, Y, 290, 84, a.WHITE, a.LINE, rx=16))
a.add(a.text(585, Y + 36, "NAT del módem", 20, a.INK, a.HEAD, 600, "middle"))
a.add(a.group(a.text(585, Y + 62, "sale como 203.0.113.10", 15, a.GREY, a.MONO, 400, "middle"), a.show(0, 61), still=1))
a.add(a.group(a.text(585, Y + 62, "sale como 203.0.113.25", 15, a.BAD, a.MONO, 600, "middle"), a.show(61, 100), still=0))
a.add(node(a, 872, Y, 280, 84, "cloud2.mikrotik.com", "UDP 15252", dark=True))

LANE = 300
a.add(f'<line x1="173" y1="{LANE}" x2="1012" y2="{LANE}" stroke="{a.LINE}" stroke-width="2" stroke-dasharray="4 6"/>')
a.add(a.text(48, LANE + 6, "AVISO", 15, a.GREY, a.MONO, 600))


def aviso(t, ip_in, ip_out):
    packet(a, "origen 192.168.1.2", [(0, 250, LANE), (t, 250, LANE), (t + 4, 470, LANE), (100, 470, LANE)], t, t + 4.4, a.CYAN)
    packet(a, f"origen {ip_out}", [(0, 700, LANE), (t + 4.4, 700, LANE), (t + 9, 930, LANE), (100, 930, LANE)], t + 4.4, t + 9.4, a.BLUE)


aviso(2, "192.168.1.2", "203.0.113.10")
aviso(64, "192.168.1.2", "203.0.113.25")

# solo en el cuadro fijo: el aviso ya pasó por el NAT
_off = a.keyframes([(0, 0), (100, 0)])
a.add(a.group(a.pill(330, LANE - 17, "origen 192.168.1.2", a.WHITE, a.CYAN, 15, 34, "middle")
              + a.pill(820, LANE - 17, "origen 203.0.113.10", a.WHITE, a.BLUE, 15, 34, "middle"), _off, still=1))

# registro en la nube
CX, CY, CW, CH = 712, 338, 440, 132
a.add(a.box(CX, CY, CW, CH, a.WHITE, a.LINE, rx=16))
a.add(a.text(CX + 22, CY + 34, "<serie>.sn.mynetname.net", 17, a.INK, a.MONO, 600))
a.add(a.text(CX + 22, CY + 62, "public-address", 15, a.GREY, a.MONO))
a.add(a.group(a.text(CX + 22, CY + 92, "203.0.113.10", 22, a.INK, a.MONO, 600), a.show(12, 74), still=1))
a.add(a.group(a.text(CX + 22, CY + 92, "203.0.113.25", 22, a.BAD, a.MONO, 600), a.show(74, 100), still=0))
a.add(a.group(a.text(CX + 22, CY + 92, "esperando aviso…", 18, a.GREY, a.MONO), a.show(0, 12), still=0))
a.add(a.text(CX + CW - 22, CY + 92, "TTL 60 s", 16, a.BLUE, a.MONO, 600, "end"))
a.add(a.group(a.box(CX, CY, CW, CH, "none", a.AMB, rx=16, sw=3.5), a.show(20, 40), still=1))
a.add(a.group(a.box(CX, CY, CW, CH, "none", a.AMB, rx=16, sw=3.5), a.show(73, 80), still=0))

# técnico con su cache
TX, TY, TW, TH = 48, 338, 400, 132
a.add(a.box(TX, TY, TW, TH, a.WHITE, a.LINE, rx=16))
a.add(a.text(TX + 22, TY + 34, "Técnico", 20, a.INK, a.HEAD, 600))
a.add(a.text(TX + 120, TY + 34, "resuelve el nombre", 15, a.GREY, a.MONO))
a.add(a.text(TX + 22, TY + 66, "en cache", 15, a.GREY, a.MONO))
a.add(a.group(a.text(TX + 22, TY + 98, "—", 20, a.GREY, a.MONO), a.show(0, 47), still=1))
a.add(a.group(a.text(TX + 22, TY + 98, "203.0.113.10", 22, a.INK, a.MONO, 600), a.show(47, 87), still=0))
a.add(a.group(a.text(TX + 22, TY + 98, "203.0.113.25", 22, a.OK, a.MONO, 600), a.show(87, 100), still=0))
BX, BY, BW = TX + 210, TY + 88, 166
a.add(a.text(BX, TY + 66, "le queda", 15, a.GREY, a.MONO))
a.add(a.box(BX, BY, BW, 14, "#E6EDF4", rx=7))
k = a.keyframes([(0, 0), (47, 0), (48, 1), (84, 0.03), (87, 0.03), (88, 1), (100, 0.7)], "transform", "scaleX({})")
a.add(a.group(a.group(a.box(BX, BY, BW, 14, a.BLUE, rx=7), k, still=None, origin=f"{BX}px {BY}px"), a.show(47, 100), still=0))

# consulta y respuesta DNS
q1 = a.group(a.arrow(f"M{TX + TW + 8} {TY + 40} H{CX - 10}", a.BLUE, 3) + a.text((TX + TW + CX) / 2, TY + 30, "¿IP del nombre?", 15, a.BLUE, a.MONO, 600, "middle"),
             a.show(42, 47), still=0)
r1 = a.group(a.arrow(f"M{CX - 8} {TY + 96} H{TX + TW + 10}", a.OK, 3) + a.text((TX + TW + CX) / 2, TY + 86, "203.0.113.10", 15, a.OK, a.MONO, 600, "middle"),
             a.show(45, 52), still=0)
q2 = a.group(a.arrow(f"M{TX + TW + 8} {TY + 40} H{CX - 10}", a.BLUE, 3) + a.text((TX + TW + CX) / 2, TY + 30, "¿IP del nombre?", 15, a.BLUE, a.MONO, 600, "middle"),
             a.show(84, 88), still=0)
r2 = a.group(a.arrow(f"M{CX - 8} {TY + 96} H{TX + TW + 10}", a.OK, 3) + a.text((TX + TW + CX) / 2, TY + 86, "203.0.113.25", 15, a.OK, a.MONO, 600, "middle"),
             a.show(86, 96), still=0)
for g in (q1, r1, q2, r2):
    a.add(g)

# notas por tiempo
NY = 572
NOTES = [
    (0, 20, a.TXT, "La IP de ether1 es privada. La nube no confía en lo que el router dice:", "mira el origen del paquete, que el NAT ya cambió."),
    (20, 40, a.TXT, "public-address es la IP del equipo que hace el NAT, no la de ether1.", "/ip/cloud/print la muestra."),
    (40, 60, a.TXT, "Mientras dure el TTL, el técnico usa la respuesta que guardó.", "Con 60 segundos, nunca queda vieja mucho tiempo."),
    (60, 80, a.BAD, "Detrás de NAT el router no ve el cambio: manda un aviso por minuto.", "/ip/cloud/force-update lo manda en el acto."),
    (80, 100, a.OK, "El nombre siguió a la IP. Llegar a un servicio, en cambio,", "depende del firewall y de que la IP sea realmente del router."),
]
for s_, e, col, l1, l2 in NOTES:
    a.add(a.group(a.box(48, NY - 34, 1104, 100, a.WHITE, a.LINE, rx=16)
                  + a.text(72, NY, l1, 17, col, a.SANS, 600) + a.text(72, NY + 32, l2, 17, a.TXT, a.SANS, 400),
                  a.show(s_, e), still=1 if s_ == 20 else 0))

out(a, 18, 1, "IP Cloud: la nube anota la IP de origen",
    "Animación en cinco tiempos. 1: el MikroTik, con ether1 192.168.1.2 detrás del NAT de un módem, manda su aviso a cloud2.mikrotik.com por UDP 15252; el NAT cambia el origen a 203.0.113.10. "
    "2: la nube anota la IP desde la que llegó el paquete: public-address es 203.0.113.10, la del equipo que hace NAT, no la de ether1. "
    "3: un técnico resuelve el nombre <serie>.sn.mynetname.net y recibe 203.0.113.10 con TTL de 60 segundos, que guarda en cache. "
    "4: el NAT pasa a salir como 203.0.113.25; detrás de NAT el router no ve el cambio y manda un aviso por minuto, que lleva la IP nueva a la nube (force-update lo manda en el acto). "
    "5: vence el TTL, el técnico pregunta de nuevo y recibe 203.0.113.25. El nombre sigue a la IP, pero llegar a un servicio depende del firewall.",
    [8, 30, 55, 72, 92])
