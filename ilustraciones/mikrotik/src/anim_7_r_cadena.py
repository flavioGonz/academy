#!/usr/bin/env python3
"""Lección 7 · Actualizar en orden · Resumen ("Cómo se ve en la red").
Una actualización completa vista desde afuera: el backup que baja a la notebook, la consulta por HTTPS al servidor de
MikroTik, la instalación con reinicio, RouterBOOT con el segundo reinicio y los campos que cambian en cada momento.
"""
from _anim_mk_32_39 import *

a = Anim(T=30, kicker="MIKROTIK · ACTUALIZAR EN ORDEN · CÓMO SE VE EN LA RED", title="Una actualización completa, de punta a punta")
a.steps([
    "Backup: el .backup y el export quedan en Files y los bajás a la notebook.",
    "check-for-updates: el router consulta por HTTPS (TCP 443) qué hay en su canal.",
    "install: baja los paquetes, reinicia y los instala. current-firmware sigue viejo.",
    "/system/routerboard/upgrade graba RouterBOOT; el segundo reinicio lo activa.",
    "current igual a upgrade. Revisás el log y anotás todo en el legajo del cliente.",
], still=2, size=17)

S = [(0, 20), (20, 40), (40, 60), (60, 80), (80, 100)]
# ---- equipos
a.add(line(800, 232, 916, 232, a.LINE, 3, "5 7"))
a.add(line(284, 232, 400, 232, a.LINE, 3, "5 7"))
a.add(dev(a, 48, 186, 236, 92, "Notebook", "WinBox · técnico", "laptop"))
a.add(dev(a, 916, 186, 236, 92, "Servidor MikroTik", "canal long-term", "cloud", tsize=17))
RX, RY, RW, RH = 400, 186, 400, 254
a.add(a.box(RX, RY, RW, RH, a.INK, rx=18))
a.add(a.text(RX + 20, RY + 32, "RouterBOARD del cliente", 18, a.WHITE, a.SANS, 600))
FIELDS = [("RouterOS", 46, 100), ("upgrade-firmware", 46, 100), ("current-firmware", 78, 100)]
for i, (f, t_new, _) in enumerate(FIELDS):
    y = RY + 70 + i * 52
    a.add(a.box(RX + 18, y, RW - 36, 42, a.NAVY2, rx=10))
    a.add(a.text(RX + 34, y + 27, f, 15, SKY, a.MONO))
    a.add(during(a, a.text(RX + RW - 34, y + 27, "vieja", 16, SOFTW, a.MONO, 600, "end"), 0, t_new, still=1 if i == 2 else 0))
    a.add(during(a, a.text(RX + RW - 34, y + 27, "nueva", 16, MINT, a.MONO, 600, "end"), t_new, 100, still=1 if i < 2 else 0))
    a.add(during(a, a.box(RX + 14, y - 4, RW - 28, 50, "none", GOLD, rx=12, sw=3), t_new, t_new + 6))
a.add(during(a, a.pill(RX + RW / 2, RY + 228, "current ≠ upgrade: falta RouterBOOT", a.INK, GOLD, 14, 26, "middle"), 48, 61, still=1))
a.add(during(a, a.pill(RX + RW / 2, RY + 228, "current = upgrade", a.OK, a.OKBG, 14, 26, "middle"), 80, 100))
# reinicios
for t0 in (42, 72):
    a.add(during(a, a.box(RX, RY, RW, RH, a.INK, rx=18, extra='opacity=".82"') + a.text(RX + RW / 2, RY + 140, "reiniciando…", 20, GOLD, a.SANS, 600, "middle"), t0, t0 + 5))

# ---- archivos del backup
a.add(during(a, a.pill(48, 296, "pre-upgrade.backup", a.INK, a.SLATE, 14, 28) + a.pill(48, 332, "pre-upgrade.rsc", a.INK, a.SLATE, 14, 28), 12, 100, still=1))
a.add(travel(a, pkt(a, ".backup", a.CYAN, size=14, h=26), [(RX - 6, 226), (300, 226)], 4, 10, hold=1))
a.add(travel(a, pkt(a, ".rsc", a.CYAN, size=14, h=26), [(RX - 6, 250), (300, 250)], 7, 12, hold=1))
# ---- consulta y descarga
a.add(travel(a, pkt(a, "HTTPS", a.BLUE, size=14, h=26), [(810, 218), (900, 218)], 22, 27, hold=1))
a.add(during(a, a.text(858, 306, "TCP 443", 15, a.BLUE, a.MONO, 600, "middle") + a.text(858, 328, "desde 7.23", 15, a.BLUE, a.MONO, 400, "middle"), 22, 40))
a.add(travel(a, pkt(a, "latest", a.OK, size=14, h=26), [(900, 252), (810, 252)], 30, 35, hold=4))
a.add(during(a, a.text(1034, 306, "latest-version: nueva", 15, a.OK, a.MONO, 600, "middle"), 31, 40))
a.add(travel(a, pkt(a, ".npk", a.CYAN, size=14, h=26), [(900, 236), (810, 236)], 37, 41, hold=0.5))
a.add(during(a, a.text(1034, 336, "si el 443 está cortado,", 15, a.BAD, a.SANS, 600, "middle") + a.text(1034, 358, "no ve versiones", 15, a.BAD, a.SANS, 600, "middle"), 22, 40))
a.add(during(a, a.pill(RX + RW / 2, RY + 228, "/system/routerboard/upgrade", a.INK, GOLD, 14, 26, "middle"), 62, 72))

# ---- la secuencia
SEQ = ["backup", "RouterOS", "reinicio", "RouterBOOT", "reinicio", "verificar"]
WIN = [(0, 20), (20, 42), (42, 47), (60, 72), (72, 77), (80, 100)]
BY, BW, GAP = 470, 168, 19
for i, (lab, (t0, t1)) in enumerate(zip(SEQ, WIN)):
    x = 48 + i * (BW + GAP)
    a.add(a.box(x, BY, BW, 52, a.WHITE, a.LINE, rx=12))
    a.add(a.text(x + BW / 2, BY + 33, lab, 16, a.INK, a.SANS, 600, "middle"))
    a.add(during(a, a.box(x, BY, BW, 52, a.BLUE, a.BLUE, rx=12) + a.text(x + BW / 2, BY + 33, lab, 16, a.WHITE, a.SANS, 600, "middle"), t0, t1, still=1 if i == 2 else 0))
    if t1 < 100:
        a.add(during(a, check(a, x + BW - 6, BY + 4, 11), t1, 100, still=1 if i < 2 else 0))
    if i < len(SEQ) - 1:
        a.add(a.arrow(f"M{x + BW + 2} {BY + 26} H{x + BW + GAP - 3}", a.GREY, 2))
a.add(during(a, a.box(48, 548, 1104, 50, a.OKBG, a.OK, rx=12) + a.text(68, 579, "legajo: versión de RouterOS, de RouterBOOT, canal y fecha", 16, a.OK, a.SANS, 600), 84, 100))
a.add(during(a, a.text(48, 580, "No cortes la energía mientras instala ni mientras graba RouterBOOT.", 16, a.AMB, a.SANS, 600), 40, 80))
a.add(a.text(48, 640, "/system/package/update/install  ·  /system/routerboard/upgrade  ·  /system/reboot", 16, a.TXT, a.MONO))

write(a, 7, "r1", "Una actualización completa, de punta a punta",
      "Animación en cinco tiempos con la notebook del técnico, el RouterBOARD del cliente con tres campos (RouterOS, upgrade-firmware y current-firmware) y el servidor de actualizaciones de MikroTik, "
      "y abajo la secuencia backup, RouterOS, reinicio, RouterBOOT, reinicio y verificar. "
      "1: backup: el .backup y el export quedan en Files y se bajan a la notebook. "
      "2: check-for-updates: el router consulta al servidor por HTTPS, TCP 443, qué hay en su canal y vuelve latest-version; si la salida al 443 está cortada, no ve versiones. "
      "3: install: baja los paquetes, reinicia y los instala; RouterOS y upgrade-firmware pasan a la versión nueva, pero current-firmware sigue vieja: falta RouterBOOT. "
      "4: /system/routerboard/upgrade graba RouterBOOT y el segundo reinicio lo activa. "
      "5: current-firmware es igual a upgrade-firmware; se revisa el log y se anota en el legajo la versión de RouterOS, la de RouterBOOT, el canal y la fecha. No se corta la energía durante la instalación.",
      [6, 26, 33, 44, 52, 66, 74, 92])
