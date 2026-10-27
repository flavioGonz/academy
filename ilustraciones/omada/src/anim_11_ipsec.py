#!/usr/bin/env python3
"""Teoría lección 11 (Túnel entre sedes): IKE por UDP 500, NAT Traversal a UDP 4500, ESP cifrado
y la decisión del gateway por destino.
Salida: site2/ilustraciones/omada/11-t1.svg"""
import sys
sys.path.insert(0, "/home/claude/ies-training/ilustraciones/omada/src")
from _anim_omada import *  # noqa

a = nueva(26, "IPSEC SITIO A SITIO", "Primero IKE, después ESP por el túnel")
F = a.steps([
    "IKE por UDP 500: los gateways se autentican y acuerdan cómo cifrar.",
    "Si detectan un NAT en el medio, pasan a UDP 4500: NAT Traversal.",
    "ESP: el tráfico entre las dos LAN viaja cifrado por el túnel.",
    "Para cada destino, el gateway decide: su LAN, local; la subred remota, al túnel.",
], still=2)
(a0, a1), (b0, b1), (c0, c1), (d0, d1) = F

GY, GH = 196, 80
a.add(nodo(a, 48, GY, 260, GH, "ER Central", "WAN 203.0.113.10"))
a.add(nodo(a, 892, GY, 260, GH, "ER Sucursal", "WAN 203.0.113.20"))
a.add(nodo(a, 520, GY + 6, 160, 68, "Internet", dark=False, tsize=18))
# LAN de cada sede
LY = 440
a.add(nodo(a, 48, LY, 260, 80, "LAN 10.10.10.0/24", "PC de monitoreo", dark=False, tsize=18))
a.add(nodo(a, 892, LY, 260, 80, "LAN 10.10.20.0/24", "cámaras", dark=False, tsize=18))
a.add(linea(a, 178, GY + GH, 178, LY, a.BLUE, 3) + linea(a, 1022, GY + GH, 1022, LY, a.BLUE, 3))

# NAT (fase 2)
fase(a, a.box(712, GY + 6, 160, 68, a.AMBBG, a.AMB, rx=14, sw=2, extra='stroke-dasharray="6 5"')
     + a.text(792, GY + 36, "NAT", 18, a.AMB, a.HEAD, 600, "middle") + a.text(792, GY + 58, "en el medio", 15, a.AMB, a.MONO, 400, "middle"), F, 1)

MY = 330  # carril de mensajes
X1, X2 = 318, 882


def mensaje(label, t0, derecha=True, color=None, dur=2.6, still=0):
    xa, xb = (X1, X2) if derecha else (X2, X1)
    c = color or a.BLUE
    inner = a.arrow(f"M{xa} {MY} H{xb + (-8 if derecha else 8)}", c, 3) + a.text(600, MY - 14, label, 16, c, a.MONO, 600, "middle")
    en(a, inner, t0, t0 + dur + 1.5, still)
    viaje(a, f'<circle r="8" fill="{c}"/>', xa, MY, xb + (-12 if derecha else 12), MY, t0, t0 + dur, hold=0.3)


# 1: IKE por 500
for i in range(4):
    mensaje("IKE · UDP 500 · clave o certificado", a0 + 1 + i * 5.6, derecha=(i % 2 == 0))
# 2: NAT detectado, 4500
mensaje("IKE · UDP 500", b0 + 1, True)
en(a, chip(a, 600, MY + 22, "NAT detectado", a.AMB, a.AMBBG, anchor="middle", stroke=a.AMB), b0 + 5, b1)
mensaje("IKE · UDP 4500", b0 + 11, False, a.AMB)
mensaje("IKE · UDP 4500", b0 + 17, True, a.AMB)

# 3: túnel y ESP
tunel = (f'<rect x="{X1 - 8}" y="{MY - 26}" width="{X2 - X1 + 16}" height="52" rx="26" fill="{a.OK}" fill-opacity=".1" stroke="{a.OK}" stroke-width="2.5"/>'
         + a.text(600, MY + 52, "túnel IPsec · ESP cifrado (dentro de UDP 4500 si hay NAT)", 15, a.OK, a.MONO, 600, "middle"))
en(a, tunel, c0, 100, still=1)
# paquete: PC Central → ER Central → túnel → ER Sucursal → cámaras
pk = paquete(a, "→ 10.10.20.1", a.CYAN)
viaje(a, pk, 178, LY - 40, 178, GY + GH + 30, c0 + 1, c0 + 4, hold=0.2)
viaje(a, f'<rect x="-46" y="-15" width="92" height="30" rx="15" fill="{a.OK}"/>' + a.text(0, 5, "ESP", 15, a.WHITE, a.MONO, 600, "middle"),
      X1 + 40, MY, X2 - 40, MY, c0 + 5, c0 + 13, hold=0.2)
viaje(a, pk, 1022, GY + GH + 30, 1022, LY - 40, c0 + 14, c0 + 17, hold=3)
solo_fijo(a, f'<g transform="translate(600 {MY})"><rect x="-46" y="-15" width="92" height="30" rx="15" fill="{a.OK}"/>{a.text(0, 5, "ESP", 15, a.WHITE, a.MONO, 600, "middle")}</g>')

# 4: decisión por destino
DX, DYY, DW = 352, 420, 496
dec = (a.box(DX, DYY, DW, 168, a.WHITE, a.LINE)
       + a.text(DX + 20, DYY + 32, "ER Central, para cada destino", 17, a.INK, a.HEAD, 600)
       + a.box(DX + 16, DYY + 48, DW - 32, 44, a.SLATE, None, rx=10)
       + a.text(DX + 30, DYY + 76, "10.10.10.x · su LAN", 16, a.INK, a.MONO, 600) + a.text(DX + DW - 30, DYY + 76, "entrega local", 16, a.BLUE, a.SANS, 600, "end")
       + a.box(DX + 16, DYY + 102, DW - 32, 44, a.SLATE, None, rx=10)
       + a.text(DX + 30, DYY + 130, "10.10.20.x · remota", 16, a.INK, a.MONO, 600) + a.text(DX + DW - 30, DYY + 130, "al túnel", 16, a.OK, a.SANS, 600, "end"))
fase(a, dec, F, 3)
en(a, a.box(DX + 12, DYY + 44, DW - 24, 52, "none", a.BLUE, rx=12, sw=3), d0 + 3, d0 + 12)
en(a, a.box(DX + 12, DYY + 98, DW - 24, 52, "none", a.OK, rx=12, sw=3), d0 + 12, d1)

pie(a, F, [
    "Con una clave precompartida o con certificados.",
    "Por eso, con NAT adelante, se abren UDP 500 y 4500 hacia el ER.",
    "Verificación: entradas en VPN Status > IPsec y un ping de una LAN a la otra.",
    "Si las dos sedes usaran 192.168.0.0/24, nada iría nunca al túnel.",
], y=640, still=2, colores=[a.INK, a.AMB, a.INK, a.BAD])

salida(a, 11, 1, "Primero IKE, después ESP por el túnel",
       "Animación en cuatro tiempos entre ER Central (WAN 203.0.113.10, LAN 10.10.10.0/24) y ER Sucursal (WAN 203.0.113.20, LAN "
       "10.10.20.0/24). 1: los gateways intercambian IKE por UDP 500, se autentican con clave o certificado y acuerdan cómo cifrar. 2: si "
       "detectan un NAT en el medio pasan a UDP 4500, NAT Traversal. 3: se arma el túnel y un paquete de la PC de la Central a 10.10.20.1 "
       "viaja cifrado como ESP, dentro de UDP 4500 si hay NAT, hasta la LAN de la Sucursal. 4: el ER Central decide por destino: lo de su "
       "LAN 10.10.10.x lo entrega local y lo de la subred remota 10.10.20.x lo mete en el túnel; si las dos LAN fueran iguales nada iría al túnel.",
       [14, 38, 62, 90])
