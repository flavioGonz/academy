#!/usr/bin/env python3
"""Lección 12 · teoría: Torch mira antes del firewall; el log de una regla de drop dice qué se descarta."""
from _anim_mikrotik_1_13 import *

a = Anim(T=24, kicker="MIKROTIK · LECCIÓN 12 · CÓMO FUNCIONA", title="Torch mira la interfaz; el log dice qué descarta el firewall")
a.steps([
    "Torch lee lo que entra por la interfaz y lo agrupa en flujos, con su tasa.",
    "Lo ve antes del firewall: también lo que después se descarta.",
    "Torch no sabe qué hizo el firewall: el drop con log=yes escribe cada paquete.",
    "Mientras Torch corre, FastTrack se apaga y la CPU trabaja más.",
], still=2)

Y = 296


def dot(col):
    return f'<circle cx="0" cy="0" r="9" fill="{col}"/>'


a.add(a.box(300, 186, 852, 214, a.SLATE, a.LINE))
a.add(a.text(318, 214, "Router", 16, a.INK, a.SANS, 600))
a.add(line(238, Y, 1130, Y, a.LINE, 3))
# paquetes que pasan (antes que las cajas)
for t0 in (2, 8, 14, 27, 33, 52, 77, 83):
    a.add(travel(a, dot(a.BLUE), [(240, Y), (1120, Y)], t0, t0 + 7, hold=0.2))
# paquetes que el firewall descarta
for t0 in (29, 37, 54, 62):
    a.add(travel(a, dot(a.BAD), [(240, Y + 22), (640, Y + 22)], t0, t0 + 4, hold=0.6))
a.add(still_only(a, place(a, dot(a.BLUE), 280, Y) + place(a, dot(a.BAD), 520, Y + 22) + place(a, dot(a.BLUE), 860, Y)))

a.add(device(a, 48, 246, 190, 100, "Cámara", "192.168.88.50", ssize=13))
a.add(a.box(320, 236, 160, 120, a.WHITE, a.BLUE, sw=2.5))
a.add(a.text(338, 264, "bridge", 16, a.INK, a.MONO, 600))
a.add(a.text(338, 288, "interfaz", 13, a.GREY, a.MONO))
a.add(a.pill(338, 312, "Torch mira acá", a.BLUE, "#E3EEF9", 12, 26))
a.add(a.box(570, 236, 270, 120, a.WHITE, a.LINE))
a.add(a.text(588, 264, "firewall · forward", 16, a.INK, a.SANS, 600))
a.add(a.text(588, 292, "drop invalid", 14, a.TXT, a.MONO))
a.add(a.text(588, 314, "log=yes log-prefix=", 13, a.TXT, a.MONO))
a.add(a.text(588, 334, '"DROP-INV"', 13, a.TXT, a.MONO))
a.add(during(a, a.box(566, 232, 278, 128, "none", a.BAD, rx=16, sw=3), 52, 75, still=1))
a.add(a.box(930, 236, 200, 120, a.WHITE, a.LINE))
a.add(a.text(948, 264, "sale", 16, a.INK, a.SANS, 600))
a.add(a.text(948, 288, "a internet", 13, a.GREY, a.MONO))
a.add(during(a, xmark(a, 555, Y + 22, 12), 29, 75, still=1))

# Torch
a.add(a.box(48, 420, 540, 176, a.INK))
a.add(a.text(66, 448, "/tool/torch bridge src-address=192.168.88.50/32", 13, SKY, a.MONO))
a.add(a.text(66, 476, "origen", 13, SKY, a.MONO))
a.add(a.text(250, 476, "destino", 13, SKY, a.MONO))
a.add(a.text(570, 476, "tasa", 13, SKY, a.MONO, 400, "end"))
f1 = a.text(66, 506, "192.168.88.50", 15, a.WHITE, a.MONO, 600) + a.text(250, 506, "internet", 15, a.WHITE, a.MONO)
a.add(a.group(f1, a.show(4, 100), still=1))
for t0, t1, v, st in [(4, 12, "0.8 Mbps", 0), (12, 50, "1.1 Mbps", 0), (50, 100, "1.1 Mbps", 1)]:
    a.add(during(a, a.text(570, 506, v, 15, MINT, a.MONO, 600, "end"), t0, t1, still=st, fade=0.3))
f2 = a.text(66, 536, "192.168.88.50", 15, a.WHITE, a.MONO, 600) + a.text(250, 536, "otro flujo", 15, a.WHITE, a.MONO)
a.add(a.group(f2 + a.text(570, 536, "lo ve igual", 14, GOLD, a.MONO, 600, "end"), a.show(30, 100), still=1))
a.add(during(a, a.text(66, 576, "FastTrack apagado mientras corre: más CPU", 14, GOLD, a.MONO, 600), 76, 100))

# log
a.add(a.box(612, 420, 540, 176, a.INK))
a.add(a.text(630, 448, '/log/print follow where message~"DROP-INV"', 13, SKY, a.MONO))
for k, t0 in enumerate((55, 63)):
    a.add(during(a, a.text(630, 482 + k * 30, "DROP-INV forward: in:bridge out:ether1,", 14, a.WHITE, a.MONO)
                 , t0, 100, still=1))
a.add(during(a, a.text(630, 556, "una línea por cada paquete descartado", 14, GOLD, a.MONO, 600), 56, 100, still=1))

a.add(a.text(48, 636, "En producción: Torch un rato y apagarlo; log=yes solo mientras buscás, y después log=no.", 16, a.TXT, a.SANS, 600))

p, pre = out(12, 1)
a.write(p, title="Torch antes del firewall y el log del drop",
        desc="Animación en cuatro tiempos. Una cámara 192.168.88.50 manda tráfico que entra al router por la interfaz bridge, pasa por el firewall en forward "
             "(regla drop invalid con log=yes y log-prefix DROP-INV) y sale a internet. 1: Torch, en el bridge, agrupa lo que entra en flujos con su tasa. 2: Torch ve "
             "los paquetes antes del firewall, así que muestra también el flujo que después se descarta. 3: Torch no sabe qué hizo el firewall; la regla de drop con log=yes "
             "escribe una línea DROP-INV por cada paquete descartado. 4: mientras Torch corre, FastTrack se apaga y la CPU trabaja más.",
        preview=[10, 36, 62, 88], prefix=pre)
