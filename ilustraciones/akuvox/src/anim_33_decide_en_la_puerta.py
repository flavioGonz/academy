#!/usr/bin/env python3
"""Lección 33 · Teoría · El A08 decide en la puerta.
Sale de teoria_md (Cómo funciona): lector y controlador en el mismo equipo: lee la credencial, la busca en su
lista de usuarios, revisa el horario y, si corresponde, activa su relé. Todo pasa en la puerta, sin servidor.
Credenciales del A08 según la tarjeta: PIN, tarjetas, Bluetooth y QR."""
from _anim_akuvox_29_42 import new, out, box, travel, when, check

a = new(24, "TERMINALES A0X", "El A08 decide en la puerta, sin servidor")
a.steps([
    "Llega la credencial: tarjeta, PIN, QR o Bluetooth. El A08 la lee.",
    "La busca en su lista de usuarios: existe y tiene permiso al relé A.",
    "Revisa el horario: está dentro. Activa el relé A y la cerradura se libera.",
    "La misma tarjeta fuera de horario: no abre. Todo pasó en la puerta.",
], still=2)

# credenciales
a.add(a.text(48, 214, "credenciales", 15, a.GREY, a.MONO, 600))
for i, c in enumerate(["tarjeta", "PIN", "QR", "Bluetooth"]):
    a.add(a.pill(48, 230 + i * 44, c, a.INK, a.WHITE if i else "#D7ECF8", 15, 32))

# A08
a.add(a.box(230, 180, 690, 274, a.WHITE, a.LINE, rx=20))
a.add(a.text(254, 214, "A08", 21, a.INK, a.HEAD, 600))
a.add(a.text(306, 214, "lector y controlador en el mismo equipo", 15, a.GREY, a.MONO))
ST = [(250, "lee", "la credencial"), (412, "lista", "de usuarios"), (574, "horario", "del usuario"), (736, "relé A", "de la puerta")]
SW, SY, SH = 150, 270, 96
for x, t, s in ST:
    a.add(a.box(x, SY, SW, SH, a.SLATE, None, rx=14))
    a.add(a.text(x + SW / 2, SY + 42, t, 19, a.INK, a.SANS, 600, "middle"))
    a.add(a.text(x + SW / 2, SY + 66, s, 15, a.GREY, a.MONO, 400, "middle"))
for i in range(3):
    x = ST[i][0] + SW
    a.add(a.arrow(f"M{x + 2} {SY + SH / 2} H{x + 10}", a.GREY, 2.5))

# cerradura
a.add(f'<path d="M886 {SY + SH / 2} H960" stroke="{a.CYAN}" stroke-width="4"/>')
a.add(box(960, 276, 192, 84, "Cerradura", "", "lock"))
when(a, a.text(1024, 347, "trabada", 15, a.GREY, a.MONO, 600), 0, 62)
when(a, a.text(1024, 347, "liberada", 15, a.OK, a.MONO, 600), 62, 74, still=1)
when(a, a.text(1024, 347, "trabada", 15, a.GREY, a.MONO, 600), 74, 100)
when(a, f'<rect x="958" y="274" width="196" height="88" rx="17" fill="none" stroke="{a.OK}" stroke-width="3"/>', 62, 74, still=1)

# recorrido de la credencial (pasada 1: entra)
cx = [x + SW / 2 for x, _, _ in ST]
TY = SY - 22
travel(a, (130, 246), (cx[0], TY), 3, 12, "tarjeta", a.WHITE, a.BLUE, hold=14)
travel(a, (cx[0], TY), (cx[1], TY), 27, 33, "tarjeta", a.WHITE, a.BLUE, hold=19)
travel(a, (cx[1], TY), (cx[2], TY), 52, 56, "tarjeta", a.WHITE, a.BLUE, hold=2)
travel(a, (cx[2], TY), (cx[3], TY), 58, 61, "tarjeta", a.WHITE, a.BLUE, hold=12, still=1)
when(a, check(a, cx[0], SY + SH + 26), 13, 75, still=1)
when(a, check(a, cx[1], SY + SH + 26), 34, 75, still=1)
when(a, check(a, cx[2], SY + SH + 26), 57, 75, still=1)
when(a, check(a, cx[3], SY + SH + 26), 61, 75, still=1)
when(a, f'<rect x="{ST[3][0]}" y="{SY}" width="{SW}" height="{SH}" rx="14" fill="none" stroke="{a.OK}" stroke-width="3"/>', 61, 74, still=1)
when(a, a.pill(ST[2][0] + SW / 2, SY + SH + 48, "dentro del horario", a.OK, a.OKBG, 15, 28, "middle"), 57, 75, still=1)

# pasada 2: fuera de horario
travel(a, (130, 246), (cx[0], TY), 77, 80, "tarjeta", a.WHITE, a.BLUE, hold=1)
travel(a, (cx[0], TY), (cx[1], TY), 81, 83, "tarjeta", a.WHITE, a.BLUE, hold=1)
travel(a, (cx[1], TY), (cx[2], TY), 84, 86, "tarjeta", a.WHITE, a.BAD, hold=14)
when(a, check(a, cx[0], SY + SH + 26), 80, 100)
when(a, check(a, cx[1], SY + SH + 26), 83, 100)
when(a, check(a, cx[2], SY + SH + 26, ok=False), 86, 100)
when(a, a.pill(ST[2][0] + SW / 2, SY + SH + 48, "fuera del horario", a.BAD, a.BADBG, 15, 28, "middle"), 86, 100)
when(a, a.pill(ST[3][0] + SW / 2, SY + SH + 48, "no se activa", a.GREY, "#E6EDF4", 15, 28, "middle"), 87, 100)

# sin servidor
a.add(a.box(48, 470, 1104, 150, a.WHITE, a.LINE, rx=16))
a.add(a.text(72, 506, "Sin servidor de por medio", 18, a.INK, a.SANS, 600))
a.add(a.text(72, 536, "La lista de usuarios, los horarios y el relé viven en el A08: la decisión se toma en la puerta.", 17, a.TXT, a.SANS, 600))
a.add(a.text(72, 568, "PIN, tarjeta, QR o Bluetooth recorren el mismo camino. Lo que cambia es cuán fácil es copiar", 17, a.TXT, a.SANS, 600))
a.add(a.text(72, 594, "o prestar cada credencial: por eso el PIN suele ir junto con la tarjeta.", 17, a.TXT, a.SANS, 600))

out(a, 33, 1, "El A08 decide en la puerta",
    "Animación de un terminal A08 por dentro, en cuatro etapas: lee la credencial, la busca en la lista de usuarios, revisa el horario y activa el relé A, que maneja una cerradura. "
    "Tiempo 1: llega una tarjeta (también podría ser PIN, QR o Bluetooth) y el A08 la lee. "
    "Tiempo 2: la busca en su lista de usuarios; existe y tiene permiso al relé A. "
    "Tiempo 3: está dentro del horario; el relé A se activa y la cerradura se libera. "
    "Tiempo 4: la misma tarjeta pasa fuera de horario; la lectura y la lista dan bien pero el horario no, el relé no se activa y la cerradura queda trabada. "
    "Todo ocurre en el equipo de la puerta, sin servidor.",
    [8, 40, 66, 92])
