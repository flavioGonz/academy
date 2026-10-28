#!/usr/bin/env python3
"""Lección 23 · Resumen, "Cómo se ve en la red": desde la oficina cambiás el gateway de la ruta por defecto
del router de un depósito y te equivocás; las respuestas ya no salen, la sesión muere y Safe Mode deshace.
Fuente: Configuration Management (Safe Mode, F floating-undo, timeout TCP de 9 minutos)."""
from _anim_red_1_9 import *

a = Anim(T=26, kicker="MIKROTIK · SAFE MODE · CÓMO SE VE EN LA RED", title="Un gateway mal escrito, y el router vuelve solo")
a.steps([
    "Desde la oficina entrás al depósito y tomás Safe Mode con Ctrl+X.",
    "Cambiás el gateway de la ruta por defecto y escribís .99 en vez de .9.",
    "El router ya no tiene ruta para contestarte: WinBox se congela.",
    "La sesión muere y RouterOS deshace lo marcado con F: vuelve la ruta y reconectás.",
], still=3)

Y = 254
a.add(dev(a, 48, 186, 290, 104, "Oficina IES", "198.51.100.20", icon="laptop", sub2="WinBox"))
a.add(a.box(430, 186, 340, 104, "#EAF2FA", a.LINE, rx=40, sw=2, extra='stroke-dasharray="7 6"'))
a.add(glyph(a, "cloud", 548, 192, a.BLUE, 1.1))
a.add(a.text(582, 212, "Internet", 16, a.INK, a.SANS, 600))
a.add(dev(a, 862, 186, 290, 104, "Router del depósito", "ether1 203.0.113.10/29", icon="server", dark=True, sub2="a 40 km"))
a.add(line(338, Y, 430, Y, a.BLUE, 4))
a.add(line(770, Y, 862, Y, a.BLUE, 4))

# idas y vueltas de la sesión WinBox
IN = [(400, Y - 22), (800, Y - 22)]
OUT = [(800, Y + 22), (400, Y + 22)]
for t0 in (3, 13, 29):
    a.add(travel(a, pkt(a, "WinBox", a.BLUE, size=15), IN, t0, t0 + 4, hold=0.5))
    a.add(travel(a, pkt(a, "respuesta", a.OK, size=15), OUT, t0 + 4.5, t0 + 8.5, hold=0.5))
# paso 3: llegan pedidos, las respuestas no salen
for t0 in (52, 62):
    a.add(travel(a, pkt(a, "WinBox", a.BLUE, size=15), IN, t0, t0 + 4, hold=0.5))
a.add(during(a, xmark(a, 816, Y + 22) + a.text(816, Y + 64, "sin ruta", 15, a.BAD, a.MONO, 600, "middle"), 56, 76))
# paso 4: reconecta
a.add(travel(a, pkt(a, "WinBox", a.BLUE, size=15), IN, 86, 90, hold=0.5))
a.add(travel(a, pkt(a, "respuesta", a.OK, size=15), OUT, 90.5, 94.5, hold=4))
a.add(still_only(a, place(a, pkt(a, "respuesta", a.OK, size=15), 600, Y + 22)))

# estado de la sesión
SX = 48
status(a, 322, [
    (0, 50, "sesión viva", a.OK, 0),
    (50, 64, "sesión congelada", a.AMB, 0),
    (64, 78, "sin respuesta: el router espera que muera (hasta unos 9 min)", a.BAD, 0),
    (78, 100, "reconectado: la ruta buena volvió sola", a.OK, 1),
], x=SX, anchor="start", size=17)

# terminal de la oficina
TX, TY0, TW = 48, 346, 540
lines = ["[tecnico@deposito] > Ctrl+X", "[Safe Mode taken]", "[tecnico@deposito] <SAFE> /ip/route/set", "  [find dst-address=0.0.0.0/0] gateway=203.0.113.99"]
a.add(a.box(TX, TY0, TW, 196, a.INK, rx=14))
a.add(a.text(TX + 18, TY0 + 30, "TERMINAL · OFICINA", 13, SKY, a.MONO, 400, extra='letter-spacing="1.8"'))
for i, (ln, t0) in enumerate(zip(lines, (2, 8, 27, 27))):
    col = GOLD if i == 1 else (a.WHITE if i < 2 else ("#FF9E8A" if i == 3 else a.WHITE))
    a.add(a.group(a.text(TX + 18, TY0 + 62 + i * 30, ln, 15, col, a.MONO), a.show(t0, 100), still=1))
a.add(during(a, a.text(TX + 18, TY0 + 180, "… no contesta", 15, "#FF9E8A", a.MONO, 600), 52, 78))
a.add(during(a, a.text(TX + 18, TY0 + 180, "reconectado · el gateway vuelve a ser .9", 15, MINT, a.MONO, 600), 86, 100, still=1))

# tabla de rutas y historial del router
RX, RW = 612, 540
a.add(a.box(RX, TY0, RW, 196, a.WHITE, a.LINE, rx=14))
a.add(a.text(RX + 20, TY0 + 32, "/ip/route · ruta por defecto", 17, a.INK, a.SANS, 600))
a.add(a.box(RX + 16, TY0 + 48, RW - 32, 44, a.SLATE, rx=8))
a.add(a.text(RX + 32, TY0 + 76, "0.0.0.0/0", 15, a.INK, a.MONO, 600))
gw_ok = a.text(RX + 170, TY0 + 76, "203.0.113.9", 15, a.INK, a.MONO, 600) + a.pill(RX + RW - 32, TY0 + 56, "activa", a.OK, a.OKBG, 15, 28, "end")
gw_bad = a.text(RX + 170, TY0 + 76, "203.0.113.99", 15, a.BAD, a.MONO, 600) + a.pill(RX + RW - 32, TY0 + 56, "inactiva", a.BAD, a.BADBG, 15, 28, "end")
a.add(a.group(gw_ok, a.show(0, 31), still=0))
a.add(during(a, gw_bad, 31, 80))
a.add(during(a, gw_ok, 80, 100, still=1))
a.add(during(a, a.text(RX + 20, TY0 + 122, ".99 no está en 203.0.113.8/29: no hay ruta a internet.", 15, a.BAD, a.SANS, 600), 33, 80))
a.add(a.box(RX + 16, TY0 + 140, RW - 32, 40, a.INK, rx=8))
a.add(a.text(RX + 32, TY0 + 166, "/system/history", 15, SKY, a.MONO))
a.add(during(a, a.text(RX + 190, TY0 + 166, "F  route changed", 15, GOLD, a.MONO, 600), 31, 80))
a.add(during(a, a.text(RX + 190, TY0 + 166, "deshecho al caer la sesión", 15, "#FF9E8A", a.MONO, 600), 80, 100, still=1))

a.add(note(a, 48, 566, 1104, 62, "", ["Sin Safe Mode, ese error es un viaje de 40 km. Con Safe Mode, esperás unos minutos y volvés a entrar."], "ok"))

write(a, 23, "r1", "Safe Mode en un router remoto",
      "Animación en cuatro tiempos entre la notebook de la oficina (198.51.100.20), internet y el router de un depósito a 40 km (ether1 203.0.113.10/29). "
      "1: la sesión WinBox va y vuelve; en la terminal, Ctrl+X muestra Safe Mode taken y el prompt pasa a SAFE. "
      "2: con /ip/route/set se cambia el gateway de la ruta por defecto 0.0.0.0/0 a 203.0.113.99 en vez de 203.0.113.9; el cambio se aplica en el acto, "
      "queda marcado con F en /system/history y la ruta queda inactiva porque .99 no está en la red 203.0.113.8/29. "
      "3: los pedidos de WinBox siguen llegando, pero las respuestas no tienen ruta: la sesión se congela y el router espera a que muera, hasta unos 9 minutos. "
      "4: la sesión murió y RouterOS deshace el cambio marcado con F; la ruta por defecto vuelve a 203.0.113.9 y la oficina reconecta. "
      "Sin Safe Mode, el error obligaba a viajar al depósito.",
      [8, 32, 58, 70, 92])
