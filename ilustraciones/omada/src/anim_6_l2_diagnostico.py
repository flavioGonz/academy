#!/usr/bin/env python3
"""Lección 6 · Laboratorio, paso 5: si no agarra IP, dónde muere el Discover. Sin red en el gateway nadie responde;
con el uplink sin la 20 muere en el switch; con el puerto en la red por defecto toma una IP de otra red."""
from _anim_om_red import *

a = nueva(26, "VLAN COMPLETA", "No agarra IP: seguí el Discover hasta donde muere", "l")
F = a.steps([
    "Gateway sin la red CCTV: el Discover llega con la 20 y nadie le responde.",
    "Uplink con un perfil sin la VLAN 20: el Discover muere en el switch.",
    "Puerto 5 con la red por defecto: toma IP, pero 192.168.88.x, de otra red.",
    "Revisalo en ese orden: red y DHCP en el gateway, perfil del uplink, perfil del puerto.",
], still=1)

Y, H = 196, 96
YL = Y + H / 2
a.add(dev(a, 48, Y, 230, H, "Notebook", "puerto 5", icon="laptop"))
a.add(dev(a, 360, Y, 290, H, "Switch", "puerto 5 → uplink", icon="server"))
a.add(dev(a, 732, Y, 420, H, "Gateway ER", "interfaz y DHCP por red", icon="server", dark=True))
a.add(line(278, YL, 360, YL, a.BLUE, 4) + line(650, YL, 732, YL, a.BLUE, 4))
a.add(a.text(319, YL - 14, "acceso", 15, a.GREY, a.MONO, 400, "middle") + a.text(691, YL - 14, "uplink", 15, a.GREY, a.MONO, 400, "middle"))

# panel de diagnóstico
PX, PY, PW = 48, 352, 1104
LANE = Y + H + 30
a.add(a.box(PX, PY, PW, 222, a.WHITE, a.LINE, rx=16))
ROWS = ["Red CCTV, VLAN 20, con DHCP en el gateway", "Uplink del switch con el perfil All", "Puerto 5 con el perfil CCTV"]
WHERE = ["Network Config > Network Settings > LAN", "Devices > (switch) > Ports, puerto 1", "Devices > (switch) > Ports, puerto 5"]
for i, (r, w) in enumerate(zip(ROWS, WHERE)):
    y = PY + 26 + i * 66
    a.add(a.box(PX + 20, y, 36, 36, a.SLATE, rx=18) + a.text(PX + 38, y + 24, str(i + 1), 16, a.INK, a.MONO, 600, "middle"))
    a.add(a.text(PX + 72, y + 16, r, 17, a.INK, a.SANS, 600) + a.text(PX + 72, y + 40, w, 15, a.GREY, a.MONO))
    # resaltado de la fila en su fase
    at(a, a.box(PX + 10, y - 8, PW - 20, 60, "none", a.BAD, rx=12, sw=2.5), F[i][0] + 6, F[i][1], still=1 if i == 1 else 0)
    at(a, xmark(a, PX + PW - 50, y + 18, 14), F[i][0] + 6, F[i][1], still=1 if i == 1 else 0)
    at(a, check(a, PX + PW - 50, y + 18, 14), F[3][0] + 2 + i * 4, 100)

# 1: llega con la 20 y nadie responde
travel(a, pkt(a, "Discover", a.AMB), [(200, LANE), (360, LANE)], 3, 6, hold=0.2)
travel(a, pkt(a, "Discover · 20", a.AMB), [(520, LANE), (820, LANE)], 7, 11, hold=6)
at(a, a.text(942, Y - 12, "no hay interfaz en la 20: silencio", 15, a.BAD, a.SANS, 600, "middle"), 11, 25)
# 2: muere en el switch
travel(a, pkt(a, "Discover", a.AMB), [(200, LANE), (360, LANE)], 28, 31, hold=0.2)
travel(a, pkt(a, "Discover · 20", a.AMB), [(420, LANE), (600, LANE)], 32, 35, hold=1)
at(a, xmark(a, 650, YL, 15) + a.text(650, Y - 12, "el uplink no lleva la 20", 15, a.BAD, a.SANS, 600, "middle"), 36, 50, still=1)
# 3: toma IP de otra red
travel(a, pkt(a, "Discover", a.AMB), [(200, LANE), (360, LANE)], 53, 56, hold=0.2)
travel(a, pkt(a, "Discover", a.BLUE), [(520, LANE), (820, LANE)], 57, 61, hold=0.4)
travel(a, pkt(a, "Offer 192.168.88.x", a.BAD), [(820, LANE), (520, LANE)], 63, 67, hold=0.2)
travel(a, pkt(a, "192.168.88.x", a.BAD), [(360, LANE), (200, LANE)], 68, 70, hold=4)
at(a, a.text(505, Y - 12, "sin etiqueta: entra a la red por defecto", 15, a.BAD, a.SANS, 600, "middle"), 56, 75)
at(a, chip(a, 163, Y - 40, "IPv4: 192.168.88.x", a.BAD, a.BADBG, anchor="middle", stroke=a.BAD), 70, 75)
# 4: todo bien
at(a, chip(a, 163, Y - 40, "IPv4: 10.10.20.x", a.OK, a.OKBG, anchor="middle", stroke=a.OK), 88, 100)

status(a, 616, [
    (0, 25, "Si no hay red, no hay DHCP: es lo primero que se mira.", a.INK, 0),
    (25, 50, "El perfil All lleva todas las redes; un perfil armado a mano puede no llevar la 20.", a.INK, 1),
    (50, 75, "Una IP de otra red es peor que ninguna: parece que anda.", a.BAD, 0),
    (75, 100, "Y no toques el perfil del puerto por el que el switch habla con el controlador.", a.AMB, 0),
], x=48, anchor="start", size=16)

write(a, 6, "l2", "Si la cámara no agarra IP: dónde muere el pedido DHCP",
      "Animación en cuatro tiempos con la notebook en el puerto 5, el switch y el gateway ER, y abajo las tres patas de la VLAN para revisar en orden. "
      "1: el gateway no tiene la red CCTV: el Discover llega con la etiqueta 20 y nadie responde, porque no hay interfaz ni DHCP en esa VLAN. "
      "2: el uplink del switch tiene un perfil que no lleva la VLAN 20: el Discover muere en el switch y no llega al gateway. "
      "3: el puerto 5 quedó con la red por defecto: el Discover entra sin etiqueta a esa red y la notebook recibe una IP 192.168.88.x, de otra red, que parece que anda. "
      "4: el orden para revisar es red y DHCP en el gateway (Network Config > Network Settings > LAN), perfil del uplink (All) y perfil del puerto 5 (CCTV); "
      "con las tres bien la notebook toma 10.10.20.x. No conviene tocar el perfil del puerto por el que el switch habla con el controlador.",
      [8, 36, 66, 92])
