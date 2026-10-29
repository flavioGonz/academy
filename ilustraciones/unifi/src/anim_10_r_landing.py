#!/usr/bin/env python3
"""Lección 10 · Resumen, "Cómo se ve en la red": el WiFi de invitados solo con contraseña (Standard) en una red de zona
Hotspot. Con Show Landing Page activa aparece un portal que nadie pidió; al desmarcarla el celular navega directo; y la
zona sigue aislando: la impresora de Staff no responde. Fuentes: idea_md, theory_md y lab.md de la lección (WunderTech,
ayuda de Ubiquiti citada; Hotspot hacia Internal es Allow Return)."""
from _anim_red_unifi import *  # noqa

a = new(26, "Invitados aislados", "Solo contraseña en zona Hotspot: el portal que nadie pidió", [
    "WiFi Standard con contraseña, red en zona Hotspot: el celular entra y toma IP.",
    "Abre el navegador: con Show Landing Page activa, el gateway lo manda al portal.",
    "Desmarcás Show Landing Page: la misma página sale directo a internet.",
    "Sin portal, la zona sigue aislando: la impresora 10.10.10.50 no responde.",
], still=3)

a.add(dev(a, 48, 196, 260, 96, "Celular", "SSID Invitados", icon="phone", sub2="192.168.20.31"))
a.add(dev(a, 450, 186, 320, 116, "Gateway UniFi", "red Invitados", icon="server", dark=True, sub2="zona Hotspot"))
a.add(dev(a, 892, 186, 260, 90, "Internet", "203.0.113.80", icon="globe"))
a.add(dev(a, 892, 312, 260, 90, "Impresora", "10.10.10.50 · Staff", icon="server"))
a.add(pill(a, 1152, 414, "zona Internal", "ok", anchor="end"))
a.add(wire(308, 244, 450, 244, a.BLUE, 4))
a.add(wire(770, 231, 892, 231, a.BLUE, 4))
a.add(poly([(770, 286), (830, 286), (830, 357), (892, 357)], a.BLUE, 4))

# ajuste del Hotspot Portal
HX, HY = 450, 330
a.add(a.box(HX, HY, 320, 96, a.WHITE, a.LINE, rx=14))
a.add(a.text(HX + 20, HY + 32, "Hotspot Portal", 17, a.INK, a.SANS, 600))
box_on = (a.box(HX + 20, HY + 52, 22, 22, a.BLUE, None, rx=5)
          + f'<path d="M{HX + 25} {HY + 63} L{HX + 30} {HY + 69} L{HX + 38} {HY + 57}" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round"/>')
box_off = a.box(HX + 20, HY + 52, 22, 22, a.WHITE, a.GREY, rx=5, sw=2)
vis(a, box_on, 0, 1)
vis(a, box_off, 2, 3)
a.add(a.text(HX + 54, HY + 69, "Show Landing Page", 16, a.INK, a.MONO, 600))

# pantalla del celular
SX, SY, SW, SH = 48, 330, 360, 250
a.add(a.box(SX, SY, SW, SH, a.WHITE, a.LINE, rx=18))
a.add(a.box(SX, SY, SW, 40, a.SLATE, None, rx=18))
a.add(a.box(SX, SY + 20, SW, 20, a.SLATE, None, rx=0))
a.add(a.text(SX + 20, SY + 27, "navegador del celular", 15, a.GREY, a.MONO))
vis(a, a.text(SX + 24, SY + 90, "conectado a Invitados", 17, a.INK, a.SANS, 600) + a.text(SX + 24, SY + 118, "clave del WiFi aceptada", 15, a.TXT, a.SANS), 0)
vis(a, a.box(SX + 24, SY + 64, SW - 48, 150, a.AMBBG, None, rx=12) + a.text(SX + SW / 2, SY + 110, "Portal de invitados", 18, a.AMB, a.SANS, 600, "middle")
    + a.text(SX + SW / 2, SY + 140, "¿Aceptás las condiciones?", 15, a.INK, a.SANS, 400, "middle")
    + a.text(SX + SW / 2, SY + 186, "el cliente no lo pidió", 15, a.BAD, a.SANS, 600, "middle"), 1)
vis(a, a.box(SX + 24, SY + 64, SW - 48, 150, a.OKBG, None, rx=12) + a.text(SX + SW / 2, SY + 128, "la página pedida", 18, a.OK, a.SANS, 600, "middle")
    + a.text(SX + SW / 2, SY + 158, "navega directo", 15, a.INK, a.SANS, 400, "middle"), 2)
vis(a, a.box(SX + 24, SY + 64, SW - 48, 70, a.OKBG, None, rx=12) + a.text(SX + SW / 2, SY + 106, "internet: sí", 17, a.OK, a.SANS, 600, "middle")
    + a.box(SX + 24, SY + 146, SW - 48, 70, a.BADBG, None, rx=12) + a.text(SX + SW / 2, SY + 188, "10.10.10.50: se vence el tiempo", 16, a.BAD, a.SANS, 600, "middle"), 3)

# 1 · asociación
s0, s1 = ph(a, 0)
go(a, [(450, 260), (308, 260)], s0 + 6, s0 + 12, "IP 192.168.20.31", a.GREY, hold=s0 + 13)
during(a, pill(a, 60, 168, "WiFi tipo Standard", "info"), s0 + 2, s1)

# 2 · redirección al portal
s0, s1 = ph(a, 1)
go(a, [(308, 232), (450, 232)], s0 + 2, s0 + 6, "GET", a.BLUE, hold=s0 + 7)
go(a, [(450, 262), (308, 262)], s0 + 9, s0 + 14, "→ portal", a.AMB, hold=s0 + 15)
during(a, xmark(a, 830, 231, 15), s0 + 6, s1)

# 3 · directo
s0, s1 = ph(a, 2)
go(a, [(308, 232), (450, 232)], s0 + 2, s0 + 5, "GET", a.BLUE, hold=s0 + 5.5)
go(a, [(770, 231), (884, 231)], s0 + 6, s0 + 9, "GET", a.BLUE, hold=s0 + 9.5)
go(a, [(884, 252), (770, 252)], s0 + 11, s0 + 14, "200", a.OK, hold=s0 + 14.5)
go(a, [(450, 262), (308, 262)], s0 + 15, s0 + 18, "página", a.OK, hold=s0 + 19)

# 4 · impresora
s0, s1 = ph(a, 3)
go(a, [(308, 232), (379, 232)], s0 + 2, s0 + 5, "→ impresora", a.BLUE, hold=s1 - 0.5, still=1)
during(a, xmark(a, 800, 286, 16), s0 + 7, 100, still=1)
during(a, nbox(a, 450, 456, 702, 104, "Allow Return", ["Hotspot hacia Internal solo contesta conexiones que empezaron", "adentro: el invitado no inicia. Probalo siempre desde un celular."], "ok"),
       s0 + 7, 100, still=1)

status(a, 628, [
    (0, 25, "El aislamiento lo da la zona Hotspot; el tipo de WiFi decide si hay portal.", a.INK, 0),
    (25, 50, "La zona Hotspot trae la landing page activada de fábrica.", a.AMB, 0),
    (50, 75, "Show Landing Page desmarcada: solo contraseña, como se pidió.", a.OK, 0),
    (75, 100, "Sin portal no se pierde aislamiento: la zona sigue bloqueando.", a.OK, 1),
])

write(a, 10, "r1", "El portal que nadie pidió",
      "Animación en cuatro tiempos con un celular en el SSID Invitados, el gateway UniFi con la red Invitados en la zona Hotspot, internet (203.0.113.80) "
      "y una impresora de Staff en 10.10.10.50, zona Internal; abajo, el ajuste Show Landing Page del Hotspot Portal y la pantalla del celular. "
      "1: el WiFi es tipo Standard, solo contraseña; el celular entra y toma 192.168.20.31. "
      "2: abre el navegador y, como la zona Hotspot trae la landing page activada, el gateway lo redirige al portal de invitados, que el cliente no pidió. "
      "3: con Show Landing Page desmarcada, la misma página sale directo a internet y vuelve. "
      "4: sin portal la zona sigue aislando: el celular intenta abrir 10.10.10.50 puerto 80 y el gateway lo bloquea, "
      "porque Hotspot hacia Internal es Allow Return y el invitado no puede iniciar; en el celular se vence el tiempo. Se prueba siempre desde un celular.",
      [12, 40, 64, 90])
