#!/usr/bin/env python3
"""Lección 11 · Laboratorio, paso 5: ping 10.10.20.1 desde la PC de la central. El ER Central lo mete en el túnel
porque el destino es la subred remota: por fuera viaja ESP de 203.0.113.10 a 203.0.113.20; el ER Sucursal lo descifra."""
from _anim_om_red import *

a = nueva(26, "TÚNEL ENTRE SEDES", "ping 10.10.20.1: el mismo paquete, por dentro y por fuera", "l")
F = a.steps([
    "La PC manda el ping a 10.10.20.1: no es de su LAN, así que va a su gateway, el ER Central.",
    "10.10.20.0/24 es la subred remota: el ER Central lo cifra y lo mete en ESP.",
    "El ER Sucursal lo descifra y entrega el paquete original a 10.10.20.1.",
    "La respuesta vuelve igual, cifrada. En la terminal: Respuesta desde 10.10.20.1.",
], still=1)

Y, H = 190, 92
YL = Y + H / 2
a.add(dev(a, 48, Y, 220, H, "PC Central", "10.10.10.50", icon="laptop"))
a.add(dev(a, 300, Y, 250, H, "ER Central", "WAN 203.0.113.10", icon="server", dark=True, sub2="LAN 10.10.10.1"))
a.add(a.box(582, Y + 14, 120, 64, "#EAF2FA", a.LINE, rx=28, sw=2, extra='stroke-dasharray="7 6"') + a.text(642, Y + 52, "internet", 15, a.GREY, a.MONO, 400, "middle"))
a.add(dev(a, 734, Y, 250, H, "ER Sucursal", "WAN 203.0.113.20", icon="server", dark=True, sub2="LAN 10.10.20.1"))
a.add(line(268, YL, 300, YL, a.BLUE, 4) + line(550, YL, 582, YL, a.BLUE, 4) + line(702, YL, 734, YL, a.BLUE, 4))
at(a, f'<rect x="540" y="{YL - 18}" width="204" height="36" rx="18" fill="{a.CYAN}" fill-opacity=".2" stroke="{a.CYAN}" stroke-width="2"/>', 0, 100, still=1)
a.add(a.text(642, Y - 10, "túnel IPsec (Auto IPsec)", 15, a.CYAN, a.MONO, 600, "middle"))


def hdr(x, y, w, parts, enc=False):
    """parts: [(texto, color_fondo, color_texto, ancho)]"""
    s, xx = "", x
    for t, bg, fg, ww in parts:
        s += a.box(xx, y, ww, 40, bg, rx=6) + a.text(xx + ww / 2, y + 26, t, 15, fg, a.MONO, 600, "middle")
        xx += ww + 6
    return s


INNER = [("src 10.10.10.50", a.SLATE, a.INK, 190), ("dst 10.10.20.1", a.SLATE, a.INK, 180), ("ICMP", a.SLATE, a.INK, 80)]
OUTER = [("src 203.0.113.10", "#0B3A66", a.WHITE, 200), ("dst 203.0.113.20", "#0B3A66", a.WHITE, 200), ("ESP", a.CYAN, a.WHITE, 70)]
LX = 48
a.add(a.box(LX, 316, 1104, 250, a.WHITE, a.LINE, rx=16))
a.add(a.text(LX + 20, 346, "En el cable", 16, a.INK, a.SANS, 600))
# 1: paquete original en la LAN central
at(a, a.text(LX + 20, 384, "LAN central", 15, a.GREY, a.SANS, 600) + hdr(LX + 160, 360, 0, INNER), 3, 25)
travel(a, dot(a, a.BLUE, 10), [(268, YL), (300, YL)], 4, 8, hold=0.4)
# 2: encapsulado
at(a, a.text(LX + 20, 384, "LAN central", 15, a.GREY, a.SANS, 600) + hdr(LX + 160, 360, 0, INNER), 25, 50, still=1)
at(a, a.text(LX + 20, 440, "internet", 15, a.GREY, a.SANS, 600) + hdr(LX + 160, 416, 0, OUTER)
   + a.box(LX + 160 + 488, 416, 300, 40, a.INK, rx=6) + glyph(a, "lock", LX + 160 + 500, 424, a.CYAN, 1.0)
   + a.text(LX + 160 + 640, 442, "paquete original cifrado", 15, SKY, a.MONO, 400, "middle"), 30, 75, still=1)
at(a, a.text(LX + 20, 500, "El ER Central decide por destino: 10.10.10.x se queda en su LAN; 10.10.20.x va al túnel.", 16, a.INK, a.SANS, 600), 28, 50, still=1)
travel(a, dot(a, a.CYAN, 10), [(550, YL), (734, YL)], 32, 38, hold=0.5)
# 3: descifrado
at(a, a.text(LX + 20, 496, "LAN sucursal", 15, a.GREY, a.SANS, 600) + hdr(LX + 160, 472, 0, INNER), 55, 75)
at(a, check(a, 859, Y + H + 18, 14) + a.text(880, Y + H + 24, "llega a 10.10.20.1", 15, a.OK, a.SANS, 600), 58, 75)
# 4: respuesta
travel(a, dot(a, a.OK, 10), [(734, YL), (550, YL)], 79, 85, hold=0.3)
travel(a, dot(a, a.OK, 10), [(300, YL), (268, YL)], 86, 88, hold=0.5)
at(a, a.box(LX + 20, 370, 600, 76, a.INK, rx=10) + a.text(LX + 38, 400, "PS> ping 10.10.20.1", 15, a.WHITE, a.MONO)
   + a.text(LX + 38, 428, "Respuesta desde 10.10.20.1: bytes=32", 15, MINT, a.MONO, 600), 88, 100)
at(a, a.text(LX + 20, 500, "Si no responde: VPN Status > Site-to-Site VPN > IPsec, y que las LAN no se solapen.", 16, a.INK, a.SANS, 600), 80, 100)

status(a, 628, [
    (0, 25, "Para la PC es un ping común: no sabe que hay un túnel.", a.INK, 0),
    (25, 50, "Por internet solo se ven las IP públicas de los dos ER y un ESP cifrado.", a.INK, 1),
    (50, 75, "Del otro lado, el paquete sale igual que entró en la central.", a.OK, 0),
    (75, 100, "Con respuesta, el túnel anda en los dos sentidos.", a.OK, 0),
], x=48, anchor="start", size=16)

write(a, 11, "l2", "Un ping por el túnel IPsec, por dentro y por fuera",
      "Animación en cuatro tiempos con la PC Central (10.10.10.50), el ER Central (WAN 203.0.113.10, LAN 10.10.10.1), internet y el ER Sucursal (WAN 203.0.113.20, LAN 10.10.20.1) unidos por Auto IPsec, "
      "y un panel con los encabezados del paquete en el cable. "
      "1: la PC manda el ping a 10.10.20.1; como no es de su LAN, va a su gateway con src 10.10.10.50 y dst 10.10.20.1. "
      "2: el ER Central ve que 10.10.20.0/24 es la subred remota, cifra el paquete y lo mete en ESP; por internet viaja con src 203.0.113.10 y dst 203.0.113.20 y el original va cifrado adentro. "
      "3: el ER Sucursal lo descifra y entrega el paquete original, igual que salió, a 10.10.20.1. "
      "4: la respuesta vuelve por el mismo camino, cifrada, y la terminal muestra Respuesta desde 10.10.20.1. Si no responde, se revisa VPN Status, Site-to-Site VPN, IPsec, y que las LAN no se solapen.",
      [8, 36, 62, 92])
