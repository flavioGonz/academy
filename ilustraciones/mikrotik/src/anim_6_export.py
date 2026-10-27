#!/usr/bin/env python3
"""Lección 6 · teoría: qué escribe el export (cambios, por menú, cabecera) y qué deja afuera."""
from _anim_mikrotik_1_13 import *

a = Anim(T=24, kicker="MIKROTIK · LECCIÓN 6 · CÓMO FUNCIONA", title="Qué escribe el export y qué deja afuera")
a.steps([
    "El export recorre la configuración y escribe comandos, agrupados por menú.",
    "Lo que sigue igual que de fábrica no se escribe: por eso el archivo es corto.",
    "Contraseñas de usuarios, certificados y claves SSH: nunca.",
    "Claves de WiFi, PPPoE y VPN: solo si pedís show-sensitive.",
], still=3)

LX, LY0, LW = 48, 182, 560
a.add(a.box(LX, LY0, LW, 398, a.WHITE, a.LINE))
a.add(a.text(LX + 18, LY0 + 32, "Configuración del router", 17, a.INK, a.SANS, 600))
ROWS = [
    ("identity LAB-MT01", "cambiado: va", a.OK, a.OKBG, 4),
    ("IP 192.168.88.1/24 en bridge", "va", a.OK, a.OKBG, 9),
    ("servicio www en el puerto 80", "de fábrica: no va", a.GREY, "#E6EDF4", 27),
    ("contraseña de lucia.tecnico", "nunca", a.BAD, a.BADBG, 52),
    ("certificados y claves SSH", "nunca", a.BAD, a.BADBG, 56),
    ("usuario y clave del PPPoE", "con show-sensitive", a.AMB, a.AMBBG, 77),
]
ry = []
for i, (txt, st, fg, bg, t0) in enumerate(ROWS):
    y = LY0 + 50 + i * 56
    ry.append(y)
    a.add(a.box(LX + 12, y, LW - 24, 46, a.SLATE, rx=10))
    a.add(a.text(LX + 28, y + 29, txt, 15, a.INK, a.MONO))
    a.add(during(a, a.pill(LX + LW - 24, y + 9, st, fg, bg, 13, 28, "end"), t0, 100, still=1))

FX, FW = 660, 492
a.add(a.box(FX, LY0, FW, 398, a.INK))
a.add(a.text(FX + 20, LY0 + 32, "antes.rsc", 17, a.WHITE, a.SANS, 600))
a.add(a.text(FX + FW - 20, LY0 + 32, "/export file=antes", 14, SKY, a.MONO, 400, "end"))
FL = [
    ("# <fecha> by RouterOS 7.x", "#7C9AB8", 2),
    ("/ip address", SKY, 9),
    ("add address=192.168.88.1/24 interface=bridge", a.WHITE, 9),
    ("/system identity", SKY, 5),
    ("set name=LAB-MT01", a.WHITE, 5),
    ("/interface pppoe-client", SKY, 80),
    ("add name=pppoe-out1 user=… password=…", GOLD, 80),
]
# orden en el archivo: cabecera, /ip address, /system identity, /interface pppoe-client
order = [0, 1, 2, 3, 4, 5, 6]
fy = []
for k, i in enumerate(order):
    txt, col, t0 = FL[i]
    y = LY0 + 74 + k * 30 + (40 if i >= 5 else 0) + (8 if i >= 1 else 0)
    fy.append(y)
    a.add(during(a, a.text(FX + 20, y, txt, 14, col, a.MONO), t0, 100, still=1))
a.add(during(a, a.text(FX + 20, fy[5] - 22, "solo con /export show-sensitive", 13, GOLD, a.MONO), 80, 100, still=1))
a.add(during(a, a.box(FX + 10, fy[0] - 20, FW - 20, 30, "none", "#7C9AB8", rx=6, sw=2), 2, 24))
a.add(during(a, a.text(FX + 20, LY0 + 380, "la primera línea cambia siempre: aparece en todo diff", 13, "#7C9AB8", a.MONO), 2, 24))

# viajes de fila a archivo
for i, t0, tgt in [(0, 2, fy[4]), (1, 7, fy[2])]:
    a.add(travel(a, pkt(a, "→", a.OK, size=14, h=26), [(LX + LW - 40, ry[i] + 23), (FX + 30, tgt - 5)], t0, t0 + 3, hold=0.5))
a.add(travel(a, pkt(a, "→", a.AMB, size=14, h=26), [(LX + LW - 40, ry[5] + 23), (FX + 30, fy[6] - 5)], 77, 80, hold=0.5))
# lo que no va: tachado breve
for i, t0, col in [(2, 27, a.GREY), (3, 52, a.BAD), (4, 56, a.BAD)]:
    a.add(during(a, line(LX + 26, ry[i] + 24, LX + 30 + len(ROWS[i][0]) * 9, ry[i] + 24, col, 2.5), t0, 100, still=1))

a.add(a.text(48, 626, "El .backup sí guarda todo, usuarios y contraseñas incluidos: es binario y se guarda con password=.", 16, a.TXT, a.SANS, 600))

p, pre = out(6, 1)
a.write(p, title="Qué escribe el export de RouterOS",
        desc="Animación en cuatro tiempos. A la izquierda, partes de la configuración del router; a la derecha, el archivo antes.rsc que escribe /export file=antes. "
             "1: el export escribe comandos agrupados por menú (/ip address con 192.168.88.1/24 en bridge, /system identity con LAB-MT01) y una primera línea con fecha "
             "y versión, que por eso aparece en todo diff. 2: el servicio www en el puerto 80 sigue como de fábrica y no se escribe. 3: la contraseña del usuario, "
             "los certificados y las claves SSH no se exportan nunca. 4: el usuario y la clave del PPPoE solo aparecen con /export show-sensitive.",
        preview=[12, 36, 62, 90], prefix=pre)
