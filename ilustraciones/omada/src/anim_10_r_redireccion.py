#!/usr/bin/env python3
"""Lección 10 · Resumen, "Cómo se ve en la red": el recorrido del portal cautivo. El EAP retiene la web del cliente
no autenticado y lo redirige a la página que sirve el controlador (8088 HTTP u 8843 HTTPS); el voucher se valida en el
controlador, que habilita al cliente; después navega directo, sin pasar por el controlador."""
from _anim_om_red import *

a = nueva(28, "PORTAL CAUTIVO", "Portal cautivo: la web que pediste, la que te muestran")
F = a.steps([
    "El huésped pide una web. No está autenticado: el EAP retiene el pedido y lo redirige.",
    "El celular abre la página del portal, que sirve el controlador (8843 con HTTPS Redirection).",
    "Ingresa el voucher. El controlador lo valida y habilita a ese cliente en el EAP.",
    "Navega directo, sin pasar por el controlador, hasta que vence el código.",
], still=2)

XP, XE, XC, XI = 140, 460, 790, 1070
HEAD = [(XP, "Celular", "huésped", "phone", False), (XE, "EAP", "Huespedes-Lab", "wifi", False),
        (XC, "Controlador", "sirve el portal", "server", True), (XI, "Internet", "la web pedida", "globe", False)]
for x, t, s_, ic, dk in HEAD:
    a.add(dev(a, x - 115, 172, 230, 66, t, s_, icon=ic, dark=dk))
    a.add(lifeline(a, x, 238, 586))
# estado del cliente en el EAP
at(a, chip(a, XE, 248, "no autenticado", a.AMB, a.AMBBG, anchor="middle", stroke=a.AMB), 0, 60)
at(a, chip(a, XE, 248, "autenticado", a.OK, a.OKBG, anchor="middle", stroke=a.OK), 60, 100, still=1)

msg(a, XP, XE, 306, "pide la web", 3, color=a.BLUE)
at(a, xmark(a, XE + 18, 306, 12) + a.text(XE + 38, 312, "retenido", 15, a.AMB, a.SANS, 600), 6, 76, still=1)
msg(a, XE, XP, 350, "redirección al portal", 9, color=a.AMB)
msg(a, XP, XC, 404, "página del portal · 8843", 29, color=a.BLUE, lab_x=XP + 40, anchor="start")
msg(a, XC, XP, 446, "logo, bienvenida, voucher", 35, color=a.OK, lab_x=XC - 40, anchor="end")
msg(a, XP, XC, 498, "voucher", 54, color=a.BLUE, lab_x=XP + 40, anchor="start")
at(a, check(a, XC + 20, 498, 12) + a.text(XC + 40, 504, "válido: 1 día", 15, a.OK, a.SANS, 600), 57, 100, still=1)
msg(a, XC, XE, 540, "habilita a ese cliente", 60, color=a.OK)
msg(a, XP, XI, 580, "la web pedida (Landing Page)", 78, color=a.BLUE, still=0, lab_x=XP + 40, anchor="start")
at(a, a.text(XC, 574, "no pasa por acá", 15, a.GREY, a.SANS, 600, "middle"), 80, 100)

status(a, 634, [
    (0, 25, "Hasta autenticar, el EAP solo deja pasar lo de Pre-Authentication Access.", a.INK, 0),
    (25, 50, "Con un certificado propio en .pfx, la página segura se ve limpia.", a.INK, 0),
    (50, 75, "Sin controlador corriendo no hay quién valide: los clientes nuevos no entran.", a.BAD, 1),
    (75, 100, "El portal no aísla: la VLAN de invitados con su ACL sigue haciendo falta.", a.AMB, 0),
], x=48, anchor="start", size=16)

write(a, 10, "r1", "El recorrido de un huésped por el portal cautivo",
      "Diagrama de mensajes animado entre el celular de un huésped, el EAP del SSID Huespedes-Lab, el controlador que sirve el portal e internet. "
      "1: el huésped pide una web; como no está autenticado, el EAP retiene el pedido y le responde con una redirección al portal. "
      "2: el celular abre la página del portal, que sirve el controlador por el 8843 con HTTPS Redirection (por el 8088 en HTTP), con el logo, la bienvenida y el campo del voucher. "
      "3: el huésped ingresa el voucher; el controlador lo valida, por ejemplo por un día, y habilita a ese cliente en el EAP, que pasa de no autenticado a autenticado; "
      "sin controlador corriendo no hay quién valide y los clientes nuevos no entran. "
      "4: el celular va a la web que había pedido, la Landing Page, y navega directo por el EAP, sin pasar por el controlador, hasta que vence el código. "
      "El portal no aísla: la VLAN de invitados con su ACL sigue haciendo falta.",
      [8, 36, 62, 90])
