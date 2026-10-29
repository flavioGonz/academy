#!/usr/bin/env python3
"""Lección 5 · Laboratorio, paso 3: entrar con viewer-sucursal. Ve solo su sitio, mira sin cambiar nada;
el cambio de un Administrator sí viaja al EAP, y cada cambio queda a nombre de quien lo hizo."""
from _anim_om_red import *

a = nueva(24, "SITIOS Y CLIENTES", "Entrá como viewer-sucursal: mirar sí, cambiar no", "l")
F = a.steps([
    "viewer-sucursal inicia sesión: el controlador arma su vista con rol Viewer y un solo sitio.",
    "Pide el estado de Sucursal y lo ve. Central no aparece en su lista de sitios.",
    "Intenta cambiar un ajuste: como Viewer, no se aplica y nada viaja al EAP.",
    "Tu usuario Administrator hace el cambio: el controlador lo empuja al EAP de Sucursal.",
], still=2)

XV, XA, XC, XE = 160, 420, 740, 1040
a.add(dev(a, 48, 172, 240, 58, "viewer-sucursal", icon="user"))
a.add(dev(a, 306, 172, 232, 58, "Tu usuario", icon="laptop"))
a.add(dev(a, 620, 172, 240, 58, "Controlador", icon="server", dark=True))
a.add(dev(a, 920, 172, 232, 58, "EAP Sucursal", icon="wifi"))
for x in (XV, XA, XC, XE):
    a.add(lifeline(a, x, 230, 572))
at(a, chip(a, XV, 240, "Viewer · Sucursal", a.INK, a.SLATE, anchor="middle"), 0, 100, still=1)
at(a, chip(a, XA, 240, "Administrator", a.INK, a.SLATE, anchor="middle"), 0, 100, still=1)

msg(a, XV, XC, 300, "inicio de sesión", 3, color=a.BLUE)
msg(a, XC, XV, 340, "vista: rol Viewer, sitio Sucursal", 10, color=a.OK)
msg(a, XV, XC, 392, "estado de Sucursal", 28, color=a.BLUE)
msg(a, XC, XV, 428, "clientes, equipos, ajustes", 33, color=a.OK)
at(a, a.box(XC + 30, 380, 370, 60, a.WHITE, a.LINE, rx=10)
   + a.text(XC + 46, 404, "Sitios de viewer-sucursal", 15, a.GREY, a.SANS, 600)
   + a.text(XC + 46, 428, "Sucursal", 16, a.INK, a.MONO, 600)
   + a.text(XC + 160, 428, "(Central no figura)", 15, a.GREY, a.SANS), 38, 52)
msg(a, XV, XC, 486, "cambiar el SSID", 54, color=a.BAD, end=75, still=1)
at(a, xmark(a, XC, 486, 14) + a.text(XC + 24, 492, "no se aplica: rol Viewer", 15, a.BAD, a.SANS, 600), 57, 75, still=1)
at(a, a.text((XC + XE) / 2, 528, "nada viaja al EAP", 15, a.GREY, a.SANS, 600, "middle"), 59, 75, still=1)
msg(a, XA, XC, 486, "cambiar el SSID", 78, color=a.BLUE, still=0)
msg(a, XC, XE, 528, "configuración nueva", 83, color=a.OK, still=0)
at(a, check(a, XE - 22, 528, 12), 86, 100)
at(a, chip(a, XC, 552, "a nombre de tu usuario", a.INK, a.SLATE, anchor="middle"), 86, 100)

status(a, 622, [
    (0, 25, "Cerrá sesión con tu usuario y entrá con viewer-sucursal y Visor-Lab-2026.", a.INK, 0),
    (25, 50, "El cliente mira el estado de su local sin ver los demás.", a.INK, 0),
    (50, 75, "Si viewer-sucursal pudiera cambiar algo, el rol quedó mal: revisalo.", a.BAD, 1),
    (75, 100, "Un usuario por persona: cada cambio queda a nombre de quien lo hizo.", a.OK, 0),
], x=48, anchor="start", size=16)

write(a, 5, "l1", "Lo que puede y no puede hacer un usuario Viewer",
      "Diagrama de mensajes animado entre el usuario viewer-sucursal (rol Viewer, solo el sitio Sucursal), tu usuario Administrator, el controlador y el EAP de Sucursal. "
      "1: viewer-sucursal inicia sesión y el controlador arma su vista con rol Viewer y un solo sitio. "
      "2: pide el estado de Sucursal y ve clientes, equipos y ajustes; en su lista de sitios figura solo Sucursal y Central no aparece. "
      "3: intenta cambiar el SSID; como es Viewer el cambio no se aplica y nada viaja al EAP; si pudiera cambiar algo, el rol quedó mal. "
      "4: tu usuario Administrator hace el mismo cambio y el controlador empuja la configuración nueva al EAP de Sucursal; con un usuario por persona, cada cambio queda a nombre de quien lo hizo.",
      [8, 40, 64, 92])
