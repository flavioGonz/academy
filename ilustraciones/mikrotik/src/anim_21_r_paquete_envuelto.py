#!/usr/bin/env python3
"""Lección 21 · L2TP con IPsec · Resumen ("Cómo se ve en la red").
El paquete del encargado desde su casa: cómo se envuelve (PPP, L2TP, ESP, UDP 4500), qué cambia el NAT de la casa
y cómo lo desenvuelve el MikroTik hasta que el paquete original llega al NVR.
"""
from _anim_mk_32_39 import *

a = Anim(T=25, kicker="MIKROTIK · L2TP CON IPSEC · CÓMO SE VE EN LA RED", title="Un paquete del encargado, envuelto y desenvuelto")
a.steps([
    "Adentro va lo que importa: de 192.168.89.10, la IP del túnel, al NVR 192.168.88.50.",
    "La notebook lo envuelve: PPP, L2TP (UDP 1701), cifrado ESP y, por el NAT, UDP 4500.",
    "El router de la casa cambia el origen de afuera. Lo cifrado no lo toca ni lo lee.",
    "El MikroTik acepta el UDP 4500 en input, descifra y saca L2TP y PPP.",
    "Queda el paquete original: va por forward al NVR. La respuesta hace el camino inverso.",
], still=2, size=17)

# ---- fila de equipos
TY, TH = 178, 84
CY = TY + TH / 2
a.add(line(250, CY, 1000, CY, a.LINE, 3, "5 7"))
a.add(a.text(610, CY - 12, "internet", 15, a.GREY, a.MONO, 400, "middle"))
a.add(dev(a, 48, TY, 200, TH, "Notebook", "192.168.1.34", "laptop", tsize=17))
a.add(dev(a, 290, TY, 230, TH, "Router casa · NAT", "198.51.100.7", "wifi", tsize=17))
a.add(router(a, 700, TY, 230, TH, "MikroTik", "203.0.113.10"))
a.add(dev(a, 962, TY, 190, TH, "NVR", "192.168.88.50", "server", tsize=17))
a.add(during(a, a.box(696, TY - 4, 238, TH + 8, "none", GOLD, rx=18, sw=3.5), 61, 80))
a.add(during(a, a.box(286, TY - 4, 238, TH + 8, "none", a.AMB, rx=18, sw=3.5), 45, 58))

# paquete que viaja (carril debajo de los equipos)
LY = 288
a.add(line(148, LY, 1056, LY, a.LINE, 2, "2 8"))
a.add(travel(a, pkt(a, "paquete", a.CYAN, size=14, h=28), [(148, LY), (405, LY)], 42, 47, hold=3))
a.add(travel(a, pkt(a, "paquete", a.AMB, size=14, h=28), [(405, LY), (815, LY)], 51, 59, hold=1))
a.add(travel(a, pkt(a, "paquete", a.OK, size=14, h=28), [(815, LY), (1056, LY)], 82, 88, hold=8))
a.add(still_only(a, place(pkt(a, "paquete", a.AMB, size=14, h=28), 405, LY)))

# ---- anatomía del paquete
SY, SH = 396, 92
a.add(a.text(48, 330, "EL PAQUETE POR DENTRO", 15, a.GREY, a.MONO, 600, extra='letter-spacing="2"'))


def seg(x, w, lines, col, t_in, t_out, still=1, fg=None, dark=False):
    fill = col if dark else a.WHITE
    s = a.box(x, SY, w, SH, fill, col, rx=10, sw=2.5)
    for i, (t, size, wt) in enumerate(lines):
        s += a.text(x + w / 2, SY + 30 + i * 24, t, size, fg or (a.WHITE if dark else col), a.MONO, wt, "middle")
    a.add(during(a, s, t_in, t_out, still=still))


# ESP: envuelve lo de adentro
a.add(during(a, a.box(426, 344, 726, 158, a.BLUE, a.BLUE, rx=14, sw=2.5, extra='fill-opacity=".08"')
             + a.text(442, 370, "ESP · cifrado: de afuera no se lee", 15, a.BLUE, a.MONO, 600), 30, 66, still=1))
seg(48, 250, [("IP de afuera", 15, 600), ("de 192.168.1.34", 15, 400), ("a 203.0.113.10", 15, 400)], a.INK, 34, 47, still=0)
seg(48, 250, [("IP de afuera", 15, 600), ("de 198.51.100.7", 15, 600), ("a 203.0.113.10", 15, 400)], a.AMB, 47, 66, still=1)
seg(306, 112, [("UDP", 15, 600), ("4500", 17, 600), ("NAT-T", 15, 400)], a.INK, 34, 66)
seg(442, 104, [("UDP", 15, 600), ("1701", 17, 600)], a.CYAN, 22, 72)
seg(554, 88, [("L2TP", 15, 600), ("túnel", 15, 400)], a.CYAN, 22, 72)
seg(650, 80, [("PPP", 15, 600), ("sesión", 15, 400)], a.OK, 22, 72)
seg(738, 270, [("IP de adentro", 15, 600), ("de 192.168.89.10", 15, 400), ("a 192.168.88.50", 15, 400)], a.OK, 0, 100)
seg(1016, 120, [("datos", 15, 600), ("TCP 8000", 15, 400)], a.GREY, 0, 100)
a.add(during(a, a.box(734, SY - 4, 278, SH + 8, "none", MINT, rx=12, sw=3.5), 2, 18))
a.add(during(a, a.box(734, SY - 4, 278, SH + 8, "none", MINT, rx=12, sw=3.5), 74, 98))
a.add(during(a, a.box(44, SY - 4, 258, SH + 8, "none", GOLD, rx=12, sw=3.5), 47, 58))

# ---- narración
narr(a, 48, 548, [
    (0, 20, "Es el pedido de la app al NVR, como si la notebook estuviera en la oficina.", a.TXT, 0),
    (20, 40, "Cada capa agrega su encabezado por fuera. UDP 4500 porque IPsec detectó el NAT de la casa.", a.TXT, 0),
    (40, 60, "El NAT solo cambia lo de afuera: IP y UDP 4500. Lo demás viaja cifrado.", a.AMB, 1),
    (60, 80, "Después de descifrar, el UDP 1701 vuelve a pasar por input: también tiene que estar aceptado.", a.BLUE, 0),
    (80, 100, "Llega desde la interfaz del túnel: la LAN ve a 192.168.89.10, no a la casa.", a.OK, 0),
])
a.add(a.text(48, 640, "Input del MikroTik: UDP 500 y 4500 (IKE y NAT-T), ESP cuando no hay NAT, y UDP 1701.", 16, a.TXT, a.SANS, 600))

write(a, 21, "r1", "Un paquete del encargado, envuelto y desenvuelto",
      "Animación en cinco tiempos con la notebook del encargado en su casa (192.168.1.34), el router de la casa que hace NAT y sale con 198.51.100.7, el MikroTik 203.0.113.10 y el NVR 192.168.88.50. "
      "Abajo se ve el paquete por dentro. 1: adentro va el pedido de la app: IP de 192.168.89.10, la IP del túnel, a 192.168.88.50, con datos TCP 8000. "
      "2: la notebook lo envuelve: PPP, L2TP por UDP 1701, todo eso cifrado en ESP y, como IPsec detectó un NAT, dentro de UDP 4500, con una IP de afuera de 192.168.1.34 a 203.0.113.10. "
      "3: el router de la casa cambia solo el origen de afuera a 198.51.100.7; lo cifrado no lo toca ni lo lee. "
      "4: el MikroTik acepta el UDP 4500 en input, descifra el ESP, el UDP 1701 vuelve a pasar por input y saca L2TP y PPP. "
      "5: queda el paquete original, que entra desde la interfaz del túnel y va por forward al NVR; la respuesta hace el camino inverso.",
      [8, 28, 38, 52, 68, 76, 90])
