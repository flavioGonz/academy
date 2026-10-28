#!/usr/bin/env python3
"""Lección 17 · Elegir el canal · Laboratorio paso 2: comparar canales sin instalar nada, visto en el cable.
set channel no sale a la red; check-for-updates consulta la lista del canal; print muestra lo guardado y la versión instalada no cambia.
"""
from _anim_mk_32_39 import *

a = Anim(T=26, kicker="MIKROTIK · ELEGIR EL CANAL · PASO 2", title="Qué sale a la red y qué no, al comparar canales")
a.steps([
    "set channel=long-term cambia una preferencia en el router. No sale nada a la red.",
    "check-for-updates: ahora sí consulta la lista de long-term y guarda latest-version.",
    "set channel=stable y check-for-updates: consulta otra lista; latest-version cambia.",
    "print muestra lo guardado: installed-version no se movió. No se instaló nada.",
], still=2, size=17)

# ---- terminal
TX, TY, TW = 48, 176, 560
a.add(a.box(TX, TY, TW, 300, a.INK, rx=14))
CMDS = [
    ("/system/package/update/set channel=long-term", 1),
    ("/system/package/update/check-for-updates", 26),
    ("/system/package/update/print", 40),
    ("/system/package/update/set channel=stable", 52),
    ("/system/package/update/check-for-updates", 58),
    ("/system/package/update/print", 76),
]
for i, (c, t) in enumerate(CMDS):
    y = TY + 40 + i * 44
    a.add(a.text(TX + 18, y, c, 15, SOFTW, a.MONO))
    a.add(during(a, a.box(TX + 8, y - 26, TW - 16, 36, "none", GOLD, rx=8, sw=2.5), t, t + 7))

# ---- router y servidor
a.add(router(a, 660, 176, 200, 92, "Router", "RouterOS 7"))
a.add(dev(a, 1000, 176, 152, 92, "Servidor", "MikroTik", "cloud", tsize=17))
a.add(line(860, 222, 1000, 222, a.LINE, 3, "5 7"))
for t0, t1, txt in ((2, 24, "nada sale a la red"), (52, 57, "nada sale a la red"), (41, 50, "lee lo guardado"), (77, 100, "lee lo guardado")):
    a.add(during(a, a.pill(760, 286, txt, a.GREY, a.SLATE, 14, 26, "middle"), t0, t1))


def ask(t, ch):
    a.add(travel(a, dot(a, a.BLUE, 8), [(866, 210), (994, 210)], t, t + 4, hold=0.3))
    a.add(travel(a, dot(a, a.OK, 8), [(994, 236), (866, 236)], t + 5, t + 9, hold=0.5))
    a.add(during(a, a.text(1152, 302, f"pide la lista de {ch}", 15, a.BLUE, a.MONO, 600, "end")
                 + a.text(1152, 324, "HTTPS · TCP 443 (desde 7.23)", 15, a.BLUE, a.MONO, 400, "end"), t, t + 14))


ask(27, "long-term")
ask(59, "stable")

# ---- lo guardado
GX, GY, GW = 660, 352, 492
a.add(a.box(GX, GY, GW, 124, a.WHITE, a.LINE, rx=14))
a.add(a.text(GX + 18, GY + 30, "channel", 15, a.GREY, a.MONO))
a.add(a.text(GX + 18, GY + 64, "installed-version", 15, a.GREY, a.MONO))
a.add(a.text(GX + 18, GY + 98, "latest-version", 15, a.GREY, a.MONO))
a.add(during(a, a.text(GX + GW - 18, GY + 30, "long-term", 16, a.INK, a.MONO, 600, "end"), 0, 52))
a.add(during(a, a.text(GX + GW - 18, GY + 30, "stable", 16, a.AMB, a.MONO, 600, "end"), 52, 100, still=1))
a.add(a.text(GX + GW - 18, GY + 64, "la de hoy", 16, a.INK, a.MONO, 600, "end"))
a.add(during(a, a.text(GX + GW - 18, GY + 98, "sin consultar", 16, a.GREY, a.MONO, 400, "end"), 0, 36))
a.add(during(a, a.text(GX + GW - 18, GY + 98, "la última de long-term", 16, a.OK, a.MONO, 600, "end"), 36, 68))
a.add(during(a, a.text(GX + GW - 18, GY + 98, "la última de stable", 16, a.AMB, a.MONO, 600, "end"), 68, 100, still=1))
a.add(during(a, a.box(GX - 4, GY + 74, GW + 8, 40, "none", a.OK, rx=10, sw=3), 36, 44))
a.add(during(a, a.box(GX - 4, GY + 74, GW + 8, 40, "none", a.AMB, rx=10, sw=3), 68, 76, still=1))
a.add(during(a, a.box(GX - 4, GY + 40, GW + 8, 40, "none", a.OK, rx=10, sw=3), 78, 100))

narr(a, 48, 536, [
    (0, 25, "El canal es solo qué lista mirar. Cambiarlo no toca el equipo.", a.TXT, 0),
    (25, 50, "La consulta trae la lista del canal elegido; el router guarda la respuesta.", a.BLUE, 0),
    (50, 75, "Otro canal, otra lista: por eso latest-version cambia.", a.AMB, 1),
    (75, 100, "Para instalar haría falta install, y antes un backup. Este paso solo mira.", a.OK, 0),
])
a.add(a.text(48, 600, "Al terminar, dejá el canal elegido en el paso 3: en clientes, long-term.", 16, a.TXT, a.SANS, 600))

write(a, 17, "l1", "Qué sale a la red y qué no, al comparar canales",
      "Animación en cuatro tiempos con los comandos del paso 2, el router, el servidor de MikroTik y los valores que guarda /system/package/update: channel, installed-version y latest-version. "
      "1: /system/package/update/set channel=long-term cambia una preferencia en el router; no sale nada a la red. "
      "2: check-for-updates consulta al servidor la lista de long-term, desde 7.23 por HTTPS en TCP 443, y el router guarda latest-version: la última de long-term. "
      "3: set channel=stable y check-for-updates consultan otra lista; latest-version pasa a ser la última de stable. "
      "4: print muestra lo guardado; installed-version no se movió: no se instaló nada. Para instalar haría falta install, con backup antes.",
      [6, 30, 46, 62, 74, 90])
