#!/usr/bin/env python3
"""Lección 2 · Laboratorio, paso 2: primero probás tu usuario en una sesión nueva y recién después deshabilitás admin.
Una contraseña perdida no se recupera (reset o Netinstall): mientras admin siga habilitado, tenés por dónde volver."""
from _anim_red_1_9 import *

a = Anim(T=24, kicker="MIKROTIK · USUARIOS PROPIOS · LABORATORIO", title="Primero entra tu usuario, después se apaga admin")
a.steps([
    "Creaste lucia.tecnico. Cerrás WinBox: admin sigue habilitado.",
    "Entrás con lucia.tecnico: el router la acepta y el log la anota.",
    "Recién ahí, /user/disable admin: en /user/print aparece con X.",
    "Si lucia.tecnico no entraba, volvías con admin y corregías la clave.",
], still=2)

# ---------- ventana de login de WinBox
WX, WY, WW, WH = 48, 180, 420, 236
a.add(a.box(WX, WY, WW, WH, a.WHITE, a.LINE, rx=16))
a.add(glyph(a, "laptop", WX + 18, WY + 16, a.BLUE))
a.add(a.text(WX + 62, WY + 38, "WinBox · sesión nueva", 18, a.INK, a.SANS, 600))
for k, (lab, y) in enumerate((("Connect To", 70), ("Login", 122), ("Password", 174))):
    a.add(a.text(WX + 20, WY + y + 6, lab, 15, a.GREY, a.SANS))
    a.add(a.box(WX + 130, WY + y - 18, WW - 150, 36, a.SLATE, rx=8))
a.add(a.text(WX + 144, WY + 77, "192.168.88.1", 15, a.INK, a.MONO, 600))
a.add(during(a, a.text(WX + 144, WY + 129, "lucia.tecnico", 15, a.INK, a.MONO, 600), 22, 70, still=1))
a.add(during(a, a.text(WX + 144, WY + 181, "••••••••••••••••", 15, a.INK, a.MONO, 600), 24, 70, still=1))
a.add(during(a, a.text(WX + 144, WY + 129, "lucia.tecnico", 15, a.BAD, a.MONO, 600), 76, 86))
a.add(during(a, a.text(WX + 144, WY + 181, "••••••••••••", 15, a.BAD, a.MONO, 600), 76, 86))
a.add(during(a, a.text(WX + 144, WY + 129, "admin", 15, a.OK, a.MONO, 600), 87, 100))
a.add(during(a, a.text(WX + 144, WY + 181, "••••••••", 15, a.OK, a.MONO, 600), 87, 100))
a.add(during(a, a.text(WX + 20, WY + WH - 18, "sin sesión abierta", 15, a.GREY, a.MONO), 2, 22))
a.add(during(a, check(a, WX + WW - 28, WY + 30), 33, 70, still=1))
a.add(during(a, xmark(a, WX + WW - 28, WY + 30), 80, 87))
a.add(during(a, check(a, WX + WW - 28, WY + 30), 92, 100))

# ---------- router
RX, RY = 512, 230
a.add(a.box(RX, RY, 150, 120, a.INK, rx=16))
a.add(glyph(a, "server", RX + 59, RY + 18, a.CYAN))
a.add(a.text(RX + 75, RY + 82, "Router", 18, a.WHITE, a.SANS, 600, "middle"))
a.add(a.text(RX + 75, RY + 104, "de banco", 15, SKY, a.MONO, 400, "middle"))
a.add(line(WX + WW, 290, RX, 290, a.LINE, 3))
dot = lambda c: f'<circle cx="0" cy="0" r="9" fill="{c}" stroke="{a.WHITE}" stroke-width="2"/>'
a.add(travel(a, dot(a.BLUE), [(WX + WW + 10, 290), (RX - 10, 290)], 28, 32, hold=0.3))
a.add(travel(a, dot(a.OK), [(RX - 10, 290), (WX + WW + 10, 290)], 32.5, 36, hold=0.3))
a.add(travel(a, dot(a.BLUE), [(WX + WW + 10, 290), (RX - 10, 290)], 77, 80, hold=0.3))
a.add(travel(a, dot(a.BAD), [(RX - 10, 290), (WX + WW + 10, 290)], 80.5, 83, hold=0.3))
a.add(travel(a, dot(a.BLUE), [(WX + WW + 10, 290), (RX - 10, 290)], 88, 91, hold=0.3))
a.add(travel(a, dot(a.OK), [(RX - 10, 290), (WX + WW + 10, 290)], 91.5, 94, hold=0.3))

# ---------- /user/print
UX, UY, UW = 700, 180, 452
a.add(a.box(UX, UY, UW, 236, a.WHITE, a.LINE, rx=16))
a.add(a.text(UX + 20, UY + 32, "/user/print", 16, a.INK, a.MONO, 600))
a.add(a.text(UX + UW - 20, UY + 32, "X = deshabilitado", 15, a.GREY, a.MONO, 400, "end"))
US = [("admin", "full"), ("lucia.tecnico", "full"), ("mesa.ayuda", "monitoreo")]
for i, (n, g) in enumerate(US):
    y = UY + 52 + i * 56
    a.add(a.box(UX + 16, y, UW - 32, 46, a.SLATE, rx=8))
    a.add(a.text(UX + 60, y + 29, n, 15, a.INK, a.MONO, 600))
    a.add(a.text(UX + UW - 36, y + 29, g, 15, a.TXT, a.MONO, 400, "end"))
xa = (a.box(UX + 16, UY + 52, UW - 32, 46, a.BADBG, a.BAD, rx=8, sw=2)
      + a.text(UX + 32, UY + 81, "X", 16, a.BAD, a.MONO, 600)
      + a.text(UX + 60, UY + 81, "admin", 15, a.BAD, a.MONO, 600)
      + a.text(UX + UW - 36, UY + 81, "full", 15, a.BAD, a.MONO, 400, "end"))
a.add(during(a, xa, 56, 74, still=1))
a.add(during(a, a.text(UX + 20, UY + 222, "admin sigue habilitado: es tu vuelta", 15, a.OK, a.SANS, 600), 0, 52))
a.add(during(a, a.text(UX + 20, UY + 222, "admin ya no puede entrar", 15, a.BAD, a.SANS, 600), 56, 74, still=1))
a.add(during(a, a.text(UX + 20, UY + 222, "admin todavía habilitado: volvés y corregís", 15, a.OK, a.SANS, 600), 76, 100))

# ---------- terminal / log
TY = 440
a.add(a.box(48, TY, 1104, 120, a.INK, rx=16))
TL = [
    (0, 25, ['/user/add name=lucia.tecnico group=full password="Ejemplo-Lab-2026!x"', "y cerrás WinBox"], 0),
    (25, 50, ["user lucia.tecnico logged in from 192.168.88.10 via winbox", "tu usuario funciona en una sesión nueva"], 0),
    (50, 75, ["/user/disable admin", "/user/print"], 1),
    (75, 100, ["login failure for user lucia.tecnico from 192.168.88.10 via winbox", "con admin habilitado, entrás y revisás la clave (ojo con el $: \\$)"], 0),
]
for t0, t1, (l1, l2), st in TL:
    c1 = "#FF9E8A" if l1.startswith("login failure") else (MINT if l1.startswith("user ") else a.WHITE)
    a.add(during(a, a.text(70, TY + 50, l1, 16, c1, a.MONO, 600) + a.text(70, TY + 88, l2, 16, SKY, a.SANS, 600), t0, t1, still=st))

a.add(a.text(48, 606, "Al revés, si deshabilitás admin y tu clave no entra, quedás afuera: la única salida es reset o Netinstall.", 16, a.BAD, a.SANS, 600))

write(a, 2, "l1", "El orden para deshabilitar admin",
      "Animación en cuatro tiempos con la ventana de login de WinBox, el router de banco, /user/print y la terminal. "
      "1: se crea lucia.tecnico en el grupo full y se cierra WinBox; admin sigue habilitado. "
      "2: en una sesión nueva entrás con lucia.tecnico; el router acepta y el log anota user lucia.tecnico logged in from 192.168.88.10 via winbox. "
      "3: recién ahí, /user/disable admin; en /user/print admin aparece con la X de deshabilitado. "
      "4: el otro caso: si lucia.tecnico no entraba, el log dice login failure, y como admin seguía habilitado volvías a entrar con admin y corregías la clave. "
      "Al revés, deshabilitar admin sin probar te puede dejar afuera, con reset o Netinstall como única salida.",
      [10, 36, 62, 90])
