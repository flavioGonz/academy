#!/usr/bin/env python3
"""Lección 5 · teoría: una red es VLAN + DHCP + zona (t1) y dónde va el NVR (t2)."""
from _anim_unifi import *  # noqa

# ---------------- t1: el viaje de un paquete de invitado
a = new(24, "VLAN por función", "Una red en UniFi: VLAN, DHCP y zona, juntas", [
    "El celular se asocia al SSID Invitados: el AP marca sus tramas con VLAN 20.",
    "El DHCP de la VLAN 20 le da una IP de 192.168.20.0/24: cada VLAN tiene el suyo.",
    "Intenta llegar a una PC de Staff: el gateway rutea y le pregunta a la zona.",
    "Hotspot hacia Internal es Allow Return: el invitado no puede iniciar.",
], still=3)

a.add(a.text(48, 214, "ZONA HOTSPOT", 14, A.AMB, A.MONO, 600, extra='letter-spacing="1.5"'))
a.add(a.box(40, 226, 440, 130, "none", A.AMB, rx=16, sw=1.5, extra='stroke-dasharray="6 6"'))
a.add(a.box(60, 250, 200, 84, A.WHITE, A.LINE, rx=14) + phone_icon(a, 92, 292)
      + a.text(118, 286, "Celular", 19, A.INK, A.HEAD, 600) + a.text(118, 310, "red Invitados", 14, A.GREY, A.MONO))
a.add(a.box(296, 250, 164, 84, A.WHITE, A.LINE, rx=14) + ap_icon(a, 330, 292, 20)
      + a.text(362, 286, "AP", 19, A.INK, A.HEAD, 600) + a.text(362, 310, "trunk", 14, A.GREY, A.MONO))
a.add(line(a, [(260, 292), (296, 292)], A.LINE, 2.5, "4 5"))
GX, GY, GW, GH = 560, 236, 220, 112
a.add(node(a, GX, GY, GW, GH, "Gateway UniFi", "rutea entre redes", dark=True, ssize=14, sub2="DHCP · zonas"))
a.add(line(a, [(460, 292), (GX, 292)], A.LINE, 3))

# redes de destino
a.add(a.text(930, 200, "ZONA INTERNAL", 14, A.BLUE, A.MONO, 600, extra='letter-spacing="1.5"'))
a.add(node(a, 930, 212, 222, 76, "PC de Staff", "VLAN 10 · 10.10.10.x", ssize=14))
a.add(node(a, 930, 306, 222, 76, "Cámaras", "VLAN 30 · CCTV", ssize=14))
a.add(line(a, [(GX + GW, 262), (930, 250)], A.LINE, 2.5))
a.add(line(a, [(GX + GW, 330), (930, 344)], A.LINE, 2.5))

# DHCP por red
a.add(a.text(GX, 400, "DHCP POR RED", 14, A.GREY, A.MONO, extra='letter-spacing="1.5"'))
NETS = [("VLAN 10", "10.10.10.0/24"), ("VLAN 20", "192.168.20.0/24"), ("VLAN 30", "192.168.30.0/24")]
for k, (v, n) in enumerate(NETS):
    a.add(a.box(GX, 414 + k * 40, 300, 32, A.WHITE, A.LINE, rx=8, sw=1.5) + a.text(GX + 14, 436 + k * 40, f"{v}  →  {n}", 15, A.TXT, A.MONO))
vis(a, a.box(GX, 454, 300, 32, A.OKBG, A.OK, rx=8, sw=2) + a.text(GX + 14, 476, "VLAN 20  →  192.168.20.0/24", 15, A.OK, A.MONO, 600), 1)

# matriz de zonas (mini)
MX, MY = 48, 422
a.add(a.text(MX, MY - 10, "ZONE MATRIX · fila origen, columna destino", 14, A.GREY, A.MONO))
a.add(a.box(MX, MY, 470, 110, A.WHITE, A.LINE, rx=10, sw=1.5))
a.add(a.text(MX + 200, MY + 30, "→ Internal", 15, A.GREY, A.MONO))
a.add(a.text(MX + 20, MY + 76, "Hotspot", 16, A.INK, A.MONO, 600))
a.add(a.box(MX + 190, MY + 52, 250, 38, A.SLATE, rx=8) + a.text(MX + 315, MY + 77, "Allow Return", 16, A.INK, A.MONO, 600, "middle"))
vis(a, a.box(MX + 190, MY + 52, 250, 38, A.AMBBG, A.AMB, rx=8, sw=2.5) + a.text(MX + 315, MY + 77, "Allow Return", 16, A.AMB, A.MONO, 600, "middle"), 2, 3)

# 1: trama con VLAN 20
s0, s1 = ph(a, 0)
token(a, [(160, 268), (380, 268)], s0 + 1, s0 + 7, "trama", bg=A.GREY, hold=s0 + 7.3)
token(a, [(380, 268), (GX - 50, 268)], s0 + 8, s0 + 15, "VLAN 20", bg=A.BLUE, hold=s0 + 18)

# 2: IP
s0, s1 = ph(a, 1)
token(a, [(GX - 10, 316), (500, 316), (500, 380), (170, 380)], s0 + 2, s0 + 12, "192.168.20.x", bg=A.OK, hold=s1 - 1)

# 3: hacia Staff
s0, s1 = ph(a, 2)
token(a, [(160, 268), (380, 268), (GX - 50, 268)], s0 + 1, s0 + 9, "a 10.10.10.x", bg=A.CYAN, hold=s0 + 9.3)
vis(a, pill(a, GX + GW / 2, 196, "¿Hotspot → Internal?", "amb", anchor="middle"), 2)

# 4: bloqueado
s0, s1 = ph(a, 3)
token(a, [(GX + GW - 40, 262), (836, 256)], s0 + 1, s0 + 6, "10.10.10.x", bg=A.CYAN, hold=s1 - 1, still=1)
vis(a, xmark(a, 904, 254, 13), 3)
vis(a, note(a, 48, 560, 1104, "El invitado solo puede contestar conexiones que empezó Internal; iniciar, nunca.", "bad", size=16), 3)

write(a, "5-t1.svg", "VLAN, DHCP y zona en UniFi", mid_pcts(a))

# ---------------- t2: dónde está el NVR
b = new(18, "VLAN por función", "¿El video pasa por el router? Depende del NVR", [
    "Cámaras y NVR en VLANs distintas: cada flujo sube al gateway y vuelve a bajar.",
    "Cámaras y NVR en la misma VLAN: el video va por el switch, sin pasar por el router.",
    "The Hook Up: cámaras en la red principal, con reglas y MAC fija por puerto.",
], still=1)
GX, GY = 470, 186
b.add(node(b, GX, GY, 260, 76, "Gateway UniFi", "rutea entre VLANs", dark=True, ssize=14))
SX, SY = 300, 330
b.add(node(b, SX, SY, 600, 64, "Switch", None))
b.add(line(b, [(600, GY + 76), (600, SY)], A.LINE, 4))
CAMS = [300, 470, 640]
for x in CAMS:
    b.add(node(b, x, 480, 150, 70, "Cámara", "4K", ssize=14))
    b.add(line(b, [(x + 75, 480), (x + 75, SY + 64)], A.LINE, 3))
NX = 900
b.add(node(b, NX, 480, 220, 70, "NVR", None))
b.add(line(b, [(NX + 110, 480), (NX + 110, 440), (850, 440), (850, SY + 64)], A.LINE, 3))

# recorrido resaltado
for x in CAMS:
    vis(b, line(b, [(x + 75, 480), (x + 75, SY + 64)], A.AMB, 4), 0)
    vis(b, line(b, [(x + 75, 480), (x + 75, SY + 64)], A.OK, 4), 1, 2)
vis(b, line(b, [(600, SY), (600, GY + 76)], A.AMB, 6) + line(b, [(NX + 110, 480), (NX + 110, 440), (850, 440), (850, SY + 64)], A.AMB, 4)
    + pill(b, 616, 280, "sube y baja por el mismo cable", "amb"), 0)
vis(b, line(b, [(NX + 110, 480), (NX + 110, 440), (850, 440), (850, SY + 64)], A.OK, 4), 1, 2)
# etiquetas de VLAN según el tiempo
for x in CAMS:
    vis(b, pill(b, x + 75, 566, "VLAN 30", "info", anchor="middle"), 0)
    vis(b, pill(b, x + 75, 566, "VLAN 30", "ok", anchor="middle"), 1)
    vis(b, pill(b, x + 75, 566, "red principal", "grey", anchor="middle"), 2)
    vis(b, pill(b, x + 75, 450, "MAC fija", "ok", anchor="middle"), 2)
vis(b, pill(b, NX + 110, 566, "VLAN 10", "amb", anchor="middle"), 0)
vis(b, pill(b, NX + 110, 566, "VLAN 30", "ok", anchor="middle"), 1)
vis(b, pill(b, NX + 110, 566, "red principal", "grey", anchor="middle"), 2)
vis(b, pill(b, GX + 280, GY + 24, "reglas", "ok"), 2)

def streams(s0, s1, via_gw):
    for k, x in enumerate(CAMS):
        t = s0 + 1 + k * 1.6
        while t + 7 <= s1 - 1:
            pts = [(x + 75, 480), (x + 75, SY + 40)]
            if via_gw:
                pts += [(593, SY + 20), (593, GY + 70), (607, GY + 70), (607, SY + 20)]
            pts += [(850, SY + 40), (850, 440), (NX + 110, 440), (NX + 110, 480)]
            token(b, pts, t, t + (9 if via_gw else 7), inner=f'<circle r="7" fill="{A.AMB if via_gw else A.OK}"/>', hold=t + (9 if via_gw else 7))
            t += 4.8

streams(*ph(b, 0), True)
streams(*ph(b, 1), False)
streams(*ph(b, 2), False)
vis(b, note(b, 48, 606, 1104, "Cada flujo cruza el router dos veces: con once cámaras 4K, es carga real.", "amb", size=16, h=44), 0)
vis(b, note(b, 48, 606, 1104, "Si el NVR está en la misma VLAN que las cámaras, el video no pasa por el router.", "ok", size=16, h=44), 1)
vis(b, note(b, 48, 606, 1104, "No es un atajo: es una decisión de carga y de dónde está el NVR.", "info", size=16, h=44), 2)
vis(b, line(b, [(600, SY + 72), (600, SY + 100)], A.GREY, 0) + b.text(616, 302, "el video no sube al gateway", 15, A.OK, A.MONO, 600), 1)
write(b, "5-t2.svg", "Dónde está el NVR y el router entre VLANs", mid_pcts(b))
