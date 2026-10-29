#!/usr/bin/env python3
"""Lección 10 · Laboratorio, paso 2: HTTPS Redirection. Apagado, el cliente va al portal por HTTP en el 8088 y el voucher
viaja sin cifrar; activado, va al 8843 por HTTPS. Con un certificado propio (.pfx) y el nombre del controlador igual al del
certificado, la página se ve limpia."""
from _anim_om_red import *

a = nueva(26, "PORTAL CAUTIVO", "HTTPS Redirection: a qué puerto va el huésped", "l")
F = a.steps([
    "HTTPS Redirection apagado: el portal va por HTTP en el 8088 y el voucher viaja sin cifrar.",
    "Activado: el EAP redirige a la página segura del portal, en el 8843.",
    "Con el certificado que trae el controlador, el celular puede avisar que no es de confianza.",
    "Certificado propio en .pfx y el nombre del controlador igual al del certificado: limpio.",
], still=3)

# celular
PX, PY, PW, PH = 70, 180, 300, 400
a.add(a.box(PX, PY, PW, PH, a.INK, rx=34))
a.add(a.box(PX + 14, PY + 40, PW - 28, PH - 70, a.WHITE, rx=12))
a.add(a.box(PX + 110, PY + 16, 80, 10, "#24507A", rx=5))
URLS = [("http://controlador:8088", a.GREY, 0, 25), ("controlador:8843", a.INK, 25, 75), ("portal.example.com:8843", a.INK, 75, 100)]
for u, col, t0, t1 in URLS:
    at(a, a.box(PX + 26, PY + 52, PW - 52, 34, a.SLATE, rx=17) + a.text(PX + (40 if t0 == 0 else 62), PY + 75, u, 15, col, a.MONO), t0, t1, still=1 if t0 == 75 else 0)
at(a, a.text(PX + PW / 2, PY + 92 + 40, "Bienvenido", 20, a.INK, a.HEAD, 600, "middle")
   + a.box(PX + 40, PY + 170, PW - 80, 40, a.WHITE, a.LINE, rx=8) + a.text(PX + 56, PY + 196, "voucher", 15, a.GREY, a.MONO)
   + a.box(PX + 40, PY + 222, PW - 80, 40, a.BLUE, rx=8) + a.text(PX + PW / 2, PY + 248, "Conectar", 16, a.WHITE, a.SANS, 600, "middle"), 0, 50, still=0)
at(a, a.text(PX + PW / 2, PY + 92 + 40, "Bienvenido", 20, a.INK, a.HEAD, 600, "middle")
   + a.box(PX + 40, PY + 170, PW - 80, 40, a.WHITE, a.LINE, rx=8) + a.text(PX + 56, PY + 196, "voucher", 15, a.GREY, a.MONO)
   + a.box(PX + 40, PY + 222, PW - 80, 40, a.BLUE, rx=8) + a.text(PX + PW / 2, PY + 248, "Conectar", 16, a.WHITE, a.SANS, 600, "middle"), 75, 100, still=1)
# aviso de certificado
WARN = (a.box(PX + 26, PY + 110, PW - 52, 200, a.BADBG, a.BAD, rx=12, sw=2)
        + glyph(a, "warn", PX + 44, PY + 126, a.BAD)
        + a.text(PX + 84, PY + 148, "Conexión no", 17, a.BAD, a.SANS, 600)
        + a.text(PX + 84, PY + 170, "privada", 17, a.BAD, a.SANS, 600)
        + a.text(PX + 44, PY + 212, "El certificado no es", 15, a.INK, a.SANS)
        + a.text(PX + 44, PY + 234, "de confianza para", 15, a.INK, a.SANS)
        + a.text(PX + 44, PY + 256, "este nombre.", 15, a.INK, a.SANS))
at(a, WARN, 52, 75)
# candados
at(a, glyph(a, "lock", PX + 36, PY + 58, a.AMB, 0.9), 25, 75)
at(a, glyph(a, "lock", PX + 36, PY + 58, a.OK, 0.9), 75, 100, still=1)
at(a, a.text(PX + PW / 2, PY + 320, "voucher a la vista", 15, a.BAD, a.SANS, 600, "middle"), 6, 25)

# flujo a la derecha
FX = 430
a.add(dev(a, FX, 186, 260, 70, "EAP", "retiene y redirige", icon="wifi"))
a.add(dev(a, FX + 300, 186, 422, 70, "Controlador", "sirve el portal", icon="server", dark=True))
a.add(line(FX + 260, 221, FX + 300, 221, a.BLUE, 3))
ROWS = [
    (0, 25, "HTTP · 8088", "sin cifrar: cualquiera en el aire puede leerlo", a.BAD, a.BADBG),
    (25, 50, "HTTPS · 8843", "cifrado con TLS", a.OK, a.OKBG),
    (50, 75, "HTTPS · 8843", "cifrado, pero con un certificado que el celular no reconoce", a.AMB, a.AMBBG),
    (75, 100, "HTTPS · 8843", "cifrado y con certificado propio: candado limpio", a.OK, a.OKBG),
]
for t0, t1, port, txt, fg, bg in ROWS:
    at(a, chip(a, FX, 282, port, fg, bg, stroke=fg) + a.text(FX + 160, 302, txt, 15, fg, a.SANS, 600), t0, t1, still=1 if t0 == 75 else 0)
for t0 in (4, 29, 54, 79):
    travel(a, dot(a, a.BLUE), [(FX + 10, 360), (FX + 700, 360)], t0, t0 + 5, hold=0.4)
a.add(line(FX, 360, FX + 722, 360, a.LINE, 2, "4 6"))
a.add(a.text(FX, 392, "celular → página del portal en el controlador", 15, a.GREY, a.MONO))

at(a, note(a, FX, 420, 722, 150, "Cómo se carga el certificado propio", ["El controlador lo acepta en un único archivo .pfx, con certificado y clave juntos.",
   "Fijá el nombre del controlador (Controller Hostname/IP) igual al del certificado.", "Ejemplo: portal.example.com, con su DNS apuntando al controlador."], "ok"), 75, 100, still=1)
at(a, note(a, FX, 420, 722, 150, "En el formulario del paso 2", ["HTTPS Redirection: activado.", "Landing Page: la URL original que pidió el cliente.", "Se aplica a todos los tipos de autenticación."], "info"), 0, 75)

write(a, 10, "l1", "HTTPS Redirection y el certificado del portal",
      "Animación en cuatro tiempos con la pantalla del celular de un huésped y el camino hasta la página del portal que sirve el controlador. "
      "1: con HTTPS Redirection apagado, el portal se abre por HTTP en el puerto 8088 y el voucher viaja sin cifrar. "
      "2: con HTTPS Redirection activado, el EAP redirige a la página segura del portal en el 8843, cifrada con TLS. "
      "3: con el certificado que trae el controlador, el celular puede mostrar un aviso de conexión no privada, porque no reconoce el certificado para ese nombre. "
      "4: con un certificado propio cargado como un único archivo .pfx con certificado y clave, y el nombre del controlador igual al del certificado, por ejemplo portal.example.com, la página se ve limpia con candado.",
      [8, 36, 62, 90])
