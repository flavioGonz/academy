#!/usr/bin/env python3
"""Lección 7 · Actualizar en orden · Laboratorio paso 4: qué pasa por dentro con /system/routerboard/upgrade y el reinicio.
RouterOS trae su RouterBOOT, upgrade lo graba en el principal, el reinicio lo activa y el de respaldo no se toca.
"""
from _anim_mk_32_39 import *

a = Anim(T=24, kicker="MIKROTIK · ACTUALIZAR EN ORDEN · PASO 4", title="RouterBOOT: se graba con upgrade, se activa al reiniciar")
a.steps([
    "Después de install: el RouterOS nuevo trae su RouterBOOT, pero arranca el viejo.",
    "/system/routerboard/upgrade lo graba en el RouterBOOT principal. Todavía corre el viejo.",
    "/system/reboot: arranca el RouterBOOT nuevo y después RouterOS. current = upgrade.",
    "El de respaldo no se toca: es la salida si algo falla (reset apretado al dar energía).",
], still=2, size=17)

# ---- RouterOS instalado (izquierda)
a.add(a.box(48, 180, 330, 150, a.INK, rx=16))
a.add(a.text(68, 210, "RouterOS instalado", 17, a.WHITE, a.SANS, 600))
a.add(a.text(68, 238, "versión nueva", 15, MINT, a.MONO, 600))
a.add(a.box(66, 254, 294, 56, a.NAVY2, rx=10))
a.add(a.text(82, 278, "trae RouterBOOT nueva", 15, a.WHITE, a.MONO))
a.add(a.text(82, 300, "= upgrade-firmware", 15, GOLD, a.MONO, 600))

# ---- memoria del equipo (centro)
MX, MY = 450, 180
a.add(a.box(MX, MY, 340, 268, a.WHITE, a.LINE, rx=16))
a.add(a.text(MX + 20, MY + 30, "Memoria del RouterBOARD", 17, a.INK, a.SANS, 600))
a.add(a.box(MX + 18, MY + 48, 304, 92, a.SLATE, a.LINE, rx=12))
a.add(a.text(MX + 34, MY + 76, "RouterBOOT principal", 16, a.INK, a.SANS, 600))
a.add(during(a, a.text(MX + 34, MY + 104, "versión vieja", 15, a.GREY, a.MONO, 600), 0, 30))
a.add(during(a, a.text(MX + 34, MY + 104, "versión nueva", 15, a.OK, a.MONO, 600), 30, 100, still=1))
a.add(during(a, a.text(MX + 34, MY + 126, "grabada, falta reiniciar", 15, a.AMB, a.SANS, 600), 32, 50))
a.add(during(a, a.box(MX + 14, MY + 44, 312, 100, "none", GOLD, rx=14, sw=3.5), 28, 40))
a.add(a.box(MX + 18, MY + 156, 304, 92, a.SLATE, a.LINE, rx=12))
a.add(a.text(MX + 34, MY + 184, "RouterBOOT de respaldo", 16, a.INK, a.SANS, 600))
a.add(a.text(MX + 34, MY + 212, "nunca se actualiza", 15, a.GREY, a.MONO, 600))
a.add(during(a, a.box(MX + 14, MY + 152, 312, 100, "none", a.OK, rx=14, sw=3.5), 76, 100))
# copia
a.add(during(a, a.arrow(f"M378 282 C410 282 420 {MY + 94} {MX + 14} {MY + 94}", GOLD, 3), 27, 40))
a.add(travel(a, dot(a, GOLD, 9), [(378, 282), (412, 250), (MX + 14, MY + 94)], 28, 33, hold=0.5))

# ---- arranque (derecha)
BX = 850
a.add(a.text(BX, 200, "Al dar energía arranca:", 16, a.INK, a.SANS, 600))
CH = [("energía", 0), ("RouterBOOT", 1), ("RouterOS", 2)]
for i, (t, _) in enumerate(CH):
    y = 222 + i * 74
    a.add(a.box(BX, y, 302, 52, a.WHITE, a.LINE, rx=12))
    a.add(a.text(BX + 18, y + 33, t, 16, a.INK, a.SANS, 600))
    if i < 2:
        a.add(a.arrow(f"M{BX + 151} {y + 54} V{y + 70}", a.GREY, 2))
a.add(during(a, a.text(BX + 284, 222 + 74 + 33, "vieja", 15, a.GREY, a.MONO, 600, "end"), 0, 55))
a.add(during(a, a.text(BX + 284, 222 + 74 + 33, "nueva", 15, a.OK, a.MONO, 600, "end"), 55, 100, still=1))
a.add(during(a, a.box(BX - 4, 218, 310, 204, "none", GOLD, rx=14, sw=3.5) + a.pill(BX + 151, 428, "reiniciando…", a.INK, GOLD, 14, 26, "middle"), 50, 56))
for k, t in enumerate((56, 58, 60)):
    a.add(during(a, a.box(BX, 222 + k * 74, 302, 52, "none", a.OK, rx=12, sw=3), t, 74))
a.add(during(a, a.text(BX, 478, "si el principal falla:", 15, a.OK, a.SANS, 600) + a.text(BX, 500, "reset apretado al dar energía", 15, a.OK, a.SANS, 600)
             + a.text(BX, 522, "arranca con el de respaldo", 15, a.OK, a.SANS, 600), 76, 100))

# ---- terminal
a.add(term(a, 48, 352, 330, ["/system/routerboard/print"], size=15))
TY = 420
a.add(a.box(48, TY, 330, 96, a.INK, rx=12))
a.add(a.text(66, TY + 36, "current-firmware", 15, SKY, a.MONO))
a.add(a.text(66, TY + 72, "upgrade-firmware", 15, SKY, a.MONO))
a.add(during(a, a.text(360, TY + 36, "vieja", 15, GOLD, a.MONO, 600, "end"), 0, 60))
a.add(during(a, a.text(360, TY + 36, "nueva", 15, MINT, a.MONO, 600, "end"), 60, 100, still=1))
a.add(a.text(360, TY + 72, "nueva", 15, MINT, a.MONO, 600, "end"))
a.add(during(a, a.box(44, TY - 4, 338, 104, "none", MINT, rx=14, sw=3), 60, 74, still=1))

narr(a, 48, 566, [
    (0, 25, "current-firmware y upgrade-firmware no coinciden: falta este paso.", a.AMB, 0),
    (25, 50, "upgrade solo graba. Lo que corre ahora no cambia hasta reiniciar.", a.AMB, 0),
    (50, 75, "Después del reinicio coinciden: recién ahí terminó la actualización.", a.OK, 1),
    (75, 100, "Por eso el respaldo nunca se actualiza: siempre queda uno que se sabe que arranca.", a.OK, 0),
])
a.add(a.text(48, 640, "/system/routerboard/upgrade  ·  /system/reboot  ·  /log/print where topics~\"system\"", 16, a.TXT, a.MONO))

write(a, 7, "l1", "RouterBOOT: se graba con upgrade, se activa al reiniciar",
      "Animación en cuatro tiempos con el RouterOS instalado, la memoria del RouterBOARD con el RouterBOOT principal y el de respaldo, la cadena de arranque energía, RouterBOOT, RouterOS, "
      "y lo que muestra /system/routerboard/print. "
      "1: después de install, el RouterOS nuevo trae su RouterBOOT, que figura como upgrade-firmware, pero el que arranca sigue siendo el viejo: current-firmware y upgrade-firmware no coinciden. "
      "2: /system/routerboard/upgrade graba esa versión en el RouterBOOT principal; lo que está corriendo no cambia. "
      "3: con /system/reboot arranca el RouterBOOT nuevo y después RouterOS; current-firmware pasa a ser igual a upgrade-firmware. "
      "4: el RouterBOOT de respaldo nunca se actualiza: si el principal falla, manteniendo el botón de reset al dar energía el equipo arranca con el de respaldo.",
      [5, 20, 32, 45, 53, 62, 88])
