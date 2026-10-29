#!/usr/bin/env python3
"""Lección 6 · Resumen, "Cómo se ve en la red": un uplink, tres redes. La notebook de la oficina va sin etiqueta
(red por defecto nativa), la cámara entra sin etiqueta y sale con la 20, el SSID de invitados del EAP llega con la 30.
Cada VLAN es su propio broadcast: el de la notebook no llega a la cámara."""
from _anim_om_red import *

a = nueva(28, "VLAN COMPLETA", "Un cable al gateway, tres redes separadas por etiqueta")
F = a.steps([
    "Notebook en el puerto 3 (red por defecto): la trama viaja sin etiqueta todo el camino.",
    "Cámara en el puerto 5 (perfil CCTV): entra sin etiqueta y el switch la sube con la 20.",
    "EAP en el puerto 4 (perfil All): el SSID Invitados ya llega con la etiqueta 30.",
    "Cada VLAN es su broadcast: el de la notebook no llega a la cámara ni a la VLAN 30.",
], still=1)

# gateway
GX, GY = 820, 180
a.add(dev(a, GX, GY, 332, 150, "Gateway ER", "una interfaz por red", icon="server", dark=True))
IFS = [("192.168.88.1", "por defecto", a.WHITE), ("10.10.20.1", "VLAN 20", "#7FD6F0"), ("10.10.30.1", "VLAN 30", GOLD)]
for i, (ip, v, c) in enumerate(IFS):
    a.add(a.text(GX + 22, GY + 92 + i * 20, f"{ip}", 15, c, a.MONO, 600) + a.text(GX + 190, GY + 92 + i * 20, v, 15, SKY, a.MONO))
# switch
SX, SY, SW, SH = 360, 352, 440, 78
a.add(a.box(SX, SY, SW, SH, a.WHITE, a.LINE, rx=14, sw=2))
a.add(glyph(a, "server", SX + 18, SY + 22) + a.text(SX + 62, SY + 46, "Switch JetStream", 18, a.INK, a.SANS, 600))
PORTS = {1: 760, 3: 410, 4: 585, 5: 760}
for p, x in PORTS.items():
    yy = SY - 14 if p == 1 else SY + SH - 14
    a.add(a.box(x - 16, yy, 32, 28, a.INK, rx=5) + a.text(x, yy + 20, str(p), 15, a.WHITE, a.MONO, 600, "middle"))
# uplink
a.add(line(760, SY - 14, 760, 255, a.BLUE, 5) + line(760, 255, GX, 255, a.BLUE, 5))
a.add(a.text(700, 300, "uplink · All", 15, a.GREY, a.MONO, 400, "end"))
# equipos abajo
a.add(line(410, SY + SH + 14, 410, 500, a.BLUE, 3) + line(585, SY + SH + 14, 585, 500, a.BLUE, 3) + line(760, SY + SH + 14, 760, 500, a.BLUE, 3))
a.add(dev(a, 330, 500, 160, 70, "Notebook", "oficina", icon="laptop"))
a.add(a.box(505, 500, 160, 70, a.WHITE, a.LINE, rx=14, sw=2) + eap(a, 536, 535, 18) + a.text(564, 530, "EAP", 18, a.INK, a.SANS, 600) + a.text(564, 552, "Invitados", 15, a.GREY, a.MONO))
a.add(dev(a, 680, 500, 160, 70, "Cámara", "CCTV", icon="camera"))
a.add(a.text(410, 596, "red por defecto", 15, a.GREY, a.MONO, 400, "middle") + a.text(585, 596, "perfil All", 15, a.GREY, a.MONO, 400, "middle") + a.text(760, 596, "perfil CCTV", 15, a.GREY, a.MONO, 400, "middle"))

# panel: la trama en el uplink
PX, PY = 48, 180
a.add(a.box(PX, PY, 280, 300, a.WHITE, a.LINE, rx=16))
a.add(a.text(PX + 20, PY + 32, "La trama en el uplink", 16, a.INK, a.SANS, 600))


def trama(y, tag, col, t0, t1, still):
    s = a.box(PX + 20, y, 240, 40, a.SLATE, rx=8)
    s += a.text(PX + 34, y + 26, "Ethernet", 15, a.GREY, a.MONO)
    if tag:
        s += a.box(PX + 118, y + 5, 72, 30, col, rx=6) + a.text(PX + 154, y + 26, tag, 15, a.WHITE, a.MONO, 600, "middle")
    else:
        s += a.text(PX + 118, y + 26, "sin etiqueta", 15, a.INK, a.MONO, 600)
    s += a.text(PX + 250, y + 26, "IP", 15, a.GREY, a.MONO, 400, "end")
    at(a, s, t0, t1, still=still)


trama(PY + 52, "", None, 6, 100, 1)
trama(PY + 110, "20", a.CYAN, 33, 100, 1)
trama(PY + 168, "30", a.AMB, 58, 100, 0)
at(a, a.text(PX + 20, PY + 240, "Mismo cable, cada trama", 15, a.TXT, a.SANS) + a.text(PX + 20, PY + 262, "con el número de su red.", 15, a.TXT, a.SANS), 62, 100)

UP = [(760, SY - 14), (760, 255), (GX, 255)]
# 1: notebook sin etiqueta todo el camino
travel(a, pkt(a, "sin tag", a.BLUE), [(410, 500), (410, SY + SH)], 3, 6, hold=0.3)
travel(a, pkt(a, "sin tag", a.BLUE), UP, 8, 13, hold=1)
at(a, a.box(GX - 4, GY + 74, 340, 24, "none", a.WHITE, rx=6, sw=2), 13, 25)
# 2: cámara: entra sin etiqueta, sale con 20
travel(a, pkt(a, "sin tag", a.BLUE), [(760, 500), (760, SY + SH)], 28, 31, hold=0.3)
travel(a, pkt(a, "tag 20", a.CYAN), UP, 33, 38, hold=1)
at(a, a.box(GX - 4, GY + 94, 340, 24, "none", "#7FD6F0", rx=6, sw=2), 38, 50, still=1)
at(a, a.text(774, 476, "el switch le pone la 20", 15, a.CYAN, a.SANS, 600), 30, 50, still=1)
# 3: EAP con tag 30
travel(a, pkt(a, "tag 30", a.AMB), [(585, 500), (585, SY + SH)], 53, 56, hold=0.3)
travel(a, pkt(a, "tag 30", a.AMB), UP, 58, 63, hold=1)
at(a, a.box(GX - 4, GY + 114, 340, 24, "none", GOLD, rx=6, sw=2), 63, 75)
at(a, a.text(599, 476, "ya viene con la 30", 15, a.AMB, a.SANS, 600), 55, 75)
# 4: broadcast de la notebook
travel(a, dot(a, a.BLUE, 9), [(410, 500), (410, SY + SH)], 78, 80, hold=0.2)
travel(a, dot(a, a.BLUE, 9), UP, 81, 85, hold=0.6)
travel(a, dot(a, a.BLUE, 9), [(585, SY + SH), (585, 486)], 81, 83, hold=0.6)
at(a, xmark(a, 760, 468, 14), 82, 100)
at(a, a.text(424, 476, "solo red por defecto", 15, a.BLUE, a.SANS, 600), 82, 100)

status(a, 640, [
    (0, 25, "La red por defecto es la nativa del uplink: va sin etiqueta y es la de gestión.", a.INK, 0),
    (25, 50, "Puerto de acceso: la VLAN como nativa. Uplink: tagueada. Gateway: interfaz y DHCP.", a.INK, 1),
    (50, 75, "Un EAP con varios SSID en VLAN distintas necesita su puerto en All, como el uplink.", a.INK, 0),
    (75, 100, "Separadas en capa 2; si el gateway rutea entre ellas, se ven: eso es la lección 7.", a.AMB, 0),
], x=48, anchor="start", size=16)

write(a, 6, "r1", "Un uplink, tres redes separadas por etiqueta 802.1Q",
      "Animación en cuatro tiempos con un gateway ER que tiene una interfaz por red (192.168.88.1 por defecto, 10.10.20.1 en la VLAN 20 y 10.10.30.1 en la VLAN 30), "
      "un switch JetStream con el uplink en el puerto 1 (perfil All) y tres equipos: una notebook de oficina en el puerto 3 (red por defecto), un EAP con el SSID Invitados en el puerto 4 (perfil All) "
      "y una cámara en el puerto 5 (perfil CCTV, VLAN 20 nativa). "
      "1: la trama de la notebook viaja sin etiqueta todo el camino y llega a la interfaz 192.168.88.1; la red por defecto es la nativa del uplink. "
      "2: la trama de la cámara entra sin etiqueta al puerto 5 y el switch la sube por el uplink con la etiqueta 20 hasta 10.10.20.1. "
      "3: el EAP manda el tráfico del SSID Invitados ya etiquetado con la 30 y sigue así por el uplink hasta 10.10.30.1. "
      "4: un broadcast de la notebook queda en la red por defecto: no llega a la cámara ni a la VLAN 30. Si el gateway rutea entre las VLAN, igual se ven; eso se corta con ACL.",
      [8, 36, 62, 84, 95])
