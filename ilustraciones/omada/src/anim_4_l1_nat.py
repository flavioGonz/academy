#!/usr/bin/env python3
"""Lección 4 · Laboratorio, paso 5: port forwarding en la central. El router cambia el destino
203.0.113.10 por 192.168.88.10 con el mismo puerto; en el controlador 6 tiene que estar también el TCP 29817."""
from _anim_om_red import *

a = nueva(26, "TRES CAMINOS", "Port forwarding: cambia la IP, el puerto queda igual", "l")
F = a.steps([
    "El EAP de la sucursal llama a la IP pública de la central: UDP 29810 a 203.0.113.10.",
    "El router de la central cambia el destino a 192.168.88.10 con el mismo puerto: Pending.",
    "Adoptado, la gestión va por TCP 29814 y los datos de monitoreo del 6 por TCP 29817.",
    "Falla típica: una regla vieja hasta el 29816 deja afuera el 29817 del controlador 6.",
], still=1)

Y, H = 190, 96
a.add(dev(a, 48, Y, 230, H, "EAP sucursal", "Inform URL:", icon="wifi", sub2="203.0.113.10"))
a.add(a.box(310, Y + 10, 170, 76, "#EAF2FA", a.LINE, rx=30, sw=2, extra='stroke-dasharray="7 6"'))
a.add(a.text(395, Y + 54, "internet", 15, a.GREY, a.MONO, 400, "middle"))
a.add(dev(a, 512, Y, 300, H, "Router de la central", "WAN 203.0.113.10", icon="server"))
a.add(dev(a, 844, Y, 308, H, "Controlador", "192.168.88.10", icon="server", dark=True))
YL = Y + H / 2
a.add(line(278, YL, 310, YL, a.BLUE, 4) + line(480, YL, 512, YL, a.BLUE, 4) + line(812, YL, 844, YL, a.BLUE, 4))

# regla
RX, RY = 48, 318
a.add(a.box(RX, RY, 560, 132, a.WHITE, a.LINE, rx=14))
a.add(a.text(RX + 20, RY + 32, "Virtual server en el router de la central", 16, a.INK, a.SANS, 600))
a.add(a.text(RX + 20, RY + 64, "Protocolo  TCP + UDP", 16, a.TXT, a.MONO))
at(a, a.text(RX + 20, RY + 92, "Externo    29810-29817", 16, a.INK, a.MONO, 600)
   + a.text(RX + 20, RY + 118, "Interno    192.168.88.10  29810-29817", 16, a.INK, a.MONO, 600), 0, 75, still=1)
at(a, a.text(RX + 20, RY + 92, "Externo    29810-29816", 16, a.BAD, a.MONO, 600)
   + a.text(RX + 20, RY + 118, "Interno    192.168.88.10  29810-29816", 16, a.BAD, a.MONO, 600), 75, 100)

# encabezado antes y después
HX, HY, HW = 640, 318, 512
a.add(a.box(HX, HY, HW, 132, a.WHITE, a.LINE, rx=14))
a.add(a.text(HX + 20, HY + 32, "El paquete, antes y después del router", 16, a.INK, a.SANS, 600))
a.add(a.text(HX + 20, HY + 66, "llega", 15, a.GREY, a.SANS))
a.add(a.text(HX + 20, HY + 104, "sale", 15, a.GREY, a.SANS))
for (t0, t1, port, st) in ((0, 50, "UDP 29810", 1), (50, 64, "TCP 29814", 0), (64, 75, "TCP 29817", 0), (75, 100, "TCP 29817", 0)):
    s_ = a.text(HX + 80, HY + 66, f"dst 203.0.113.10  {port}", 16, a.INK, a.MONO, 600)
    if t0 < 75:
        s_ += a.text(HX + 80, HY + 104, f"dst 192.168.88.10  {port}", 16, a.OK, a.MONO, 600)
    at(a, s_, t0, t1, still=st)
at(a, a.text(HX + 80, HY + 104, "no hay regla: se descarta", 16, a.BAD, a.MONO, 600), 75, 100)

# viajes
def ida(t0, label, color, until=None):
    pts = [(200, YL), (310, YL), (480, YL), (600, YL)]
    travel(a, pkt(a, label, color), pts, t0, t0 + 6, hold=0.6)
    if until is None:
        travel(a, pkt(a, label, color), [(700, YL), (812, YL), (930, YL)], t0 + 7, t0 + 10, hold=0.8)


ida(4, "UDP 29810", a.AMB)
at(a, chip(a, 1140, Y + 10, "Pending", a.AMB, a.AMBBG, anchor="end", stroke=a.AMB), 32, 50, still=1)
at(a, a.box(512, Y, 300, H, "none", a.BLUE, rx=14, sw=3), 26, 48)
ida(54, "TCP 29814", a.BLUE)
ida(64, "TCP 29817", a.NAVY2)
at(a, chip(a, 1140, Y + 10, "Connected", a.OK, a.OKBG, anchor="end", stroke=a.OK), 58, 75)
ida(79, "TCP 29817", a.NAVY2, until=True)
at(a, xmark(a, 662, YL - 62, 15), 86, 100)

at(a, note(a, 48, 474, 1104, 96, "Mismo puerto de los dos lados", ["Descubrimiento, adopción y gestión no admiten otro puerto de origen; desde la 5.9 solo web y portal.", "La regla manda todo al controlador: los equipos de la sucursal llaman a esos puertos."], "info"), 0, 50, still=1)
at(a, note(a, 48, 474, 1104, 96, "TCP 29817, nuevo en el controlador 6", ["Lleva los datos de monitoreo de los equipos y tiene que estar abierto.", "Antes del 6 los puertos llegaban al 29816: una regla vieja puede no incluirlo."], "info"), 50, 75)
at(a, note(a, 48, 474, 1104, 96, "El 29817 muere en el router de la central", ["Corregí la regla: TCP y UDP del 29810 al 29817.", "Mejor todavía: un túnel VPN entre sedes y la option 138 con la IP privada, sin puertos abiertos a internet."], "bad"), 75, 100)

status(a, 618, [
    (0, 50, "El EAP no sabe que hay NAT: llama a la IP pública y el router hace el resto.", a.INK, 1),
    (50, 75, "Cada conexión nueva del equipo pasa por la misma regla.", a.INK, 0),
    (75, 100, "Exponer la gestión a internet abre el controlador al mundo: si podés, VPN.", a.AMB, 0),
], x=48, anchor="start", size=16)

write(a, 4, "l1", "Port forwarding de los puertos de Omada en la central",
      "Animación en cuatro tiempos con el EAP de una sucursal (Inform URL 203.0.113.10), internet, el router de la central (WAN 203.0.113.10) y el controlador 192.168.88.10, "
      "con la regla de virtual server y el encabezado del paquete antes y después del router. "
      "1: el EAP manda UDP 29810 a la IP pública de la central. "
      "2: la regla TCP y UDP 29810 a 29817 cambia el destino a 192.168.88.10 con el mismo puerto y el equipo aparece en Pending; descubrimiento, adopción y gestión no admiten otro puerto de origen. "
      "3: ya adoptado, la gestión va por TCP 29814 y los datos de monitoreo del controlador 6 por TCP 29817, por la misma regla, y el equipo queda Connected. "
      "4: falla típica, una regla vieja que termina en 29816: el TCP 29817 no tiene regla y muere en el router; se corrige con TCP y UDP del 29810 al 29817, "
      "y lo más prolijo es un túnel VPN entre sedes con la option 138 apuntando a la IP privada del controlador.",
      [8, 38, 62, 92])
