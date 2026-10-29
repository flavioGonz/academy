#!/usr/bin/env python3
"""Lección 3 · Laboratorio, paso 3: Adopt Failed por clave y Retry con las credenciales de la web local."""
from _anim_om_red import *

a = nueva(24, "ADOPCIÓN LIMPIA", "Adopt Failed por clave: Retry con la de la web local", "l")
F = a.steps([
    "Adopt: el controlador intenta tomar el EAP, pero el EAP ya tiene una clave propia.",
    "El EAP no lo acepta y en Devices aparece Adopt Failed: username or password is incorrect.",
    "Retry con el usuario y la clave de la web local: admin y Lab-Omada-2026.",
    "Con esas credenciales el EAP acepta: queda Connected y pasa a la Device Account.",
], still=3)

XT, XC, XE = 170, 600, 1030
a.add(dev(a, 48, 172, 244, 58, "Técnico", icon="laptop"))
a.add(dev(a, 478, 172, 244, 58, "Controlador", icon="server", dark=True))
a.add(dev(a, 908, 172, 244, 58, "EAP", icon="wifi"))
a.add(lifeline(a, XT, 230, 560) + lifeline(a, XC, 230, 560) + lifeline(a, XE, 230, 560))
at(a, chip(a, XE, 240, "clave: Lab-Omada-2026", a.AMB, a.AMBBG, anchor="middle", stroke=a.AMB), 0, 87)
at(a, chip(a, XE, 240, "Device Account", a.OK, a.OKBG, anchor="middle", stroke=a.OK), 87, 100, still=1)

msg(a, XT, XC, 300, "Adopt", 3, color=a.BLUE)
msg(a, XC, XE, 300, "adopción", 7, color=a.BLUE)
msg(a, XE, XC, 350, "usuario o clave incorrectos", 28, color=a.BAD)
at(a, xmark(a, XE - 24, 350, 12), 28, 100, still=1)
# ventana de Devices con el error
at(a, a.box(48, 330, 470, 64, a.BADBG, a.BAD, rx=12, sw=1.5)
   + a.text(66, 356, "Adopt Failed", 17, a.BAD, a.SANS, 600)
   + a.text(66, 380, "username or password is incorrect", 15, a.BAD, a.MONO), 32, 100, still=1)
# Retry
at(a, a.box(48, 406, 470, 66, a.WHITE, a.BLUE, rx=12, sw=1.5)
   + a.text(66, 431, "Retry", 17, a.BLUE, a.SANS, 600)
   + a.text(66, 456, "admin / Lab-Omada-2026", 15, a.INK, a.MONO, 600), 52, 100, still=1)
msg(a, XT, XC, 512, "Retry + credenciales", 56, color=a.BLUE, lab_x=XT + 30, anchor="start")
msg(a, XC, XE, 512, "adopción", 61, color=a.BLUE)
msg(a, XE, XC, 556, "aceptado", 78, color=a.OK)
at(a, check(a, XE - 24, 556, 12), 78, 100, still=1)
at(a, chip(a, XC, 250, "Connected", a.OK, a.OKBG, anchor="middle", stroke=a.OK), 84, 100, still=1)

status(a, 622, [
    (0, 25, "El EAP pasó por su web local: ya no tiene la clave de fábrica.", a.INK, 0),
    (25, 50, "El aviso dice el motivo: es de credenciales, no de red. No hace falta resetear.", a.BAD, 0),
    (50, 75, "Si estaba en otro controlador: Settings > Site > Device Account de aquel.", a.INK, 0),
    (75, 100, "Adoptado, la web local deja de mandar: las credenciales son las del sitio.", a.OK, 1),
], x=48, anchor="start", size=16)

write(a, 3, "l1", "Adopt Failed por credenciales y Retry",
      "Diagrama de mensajes animado entre el técnico, el controlador y un EAP al que se le puso la clave Lab-Omada-2026 en su web local. "
      "1: el técnico toca Adopt y el controlador intenta adoptar el EAP, que ya no tiene la clave de fábrica. "
      "2: el EAP no lo acepta y en Devices aparece Adopt Failed con el mensaje username or password is incorrect: es un problema de credenciales, no de red, y no hace falta resetear. "
      "3: el técnico usa Retry con el usuario admin y la clave Lab-Omada-2026 de la web local; si el equipo venía de otro controlador, la clave sale de Settings, Site, Device Account de aquel. "
      "4: con esas credenciales el EAP acepta, queda Connected y sus credenciales pasan a ser la Device Account del sitio; la web local deja de mandar.",
      [8, 36, 62, 92])
