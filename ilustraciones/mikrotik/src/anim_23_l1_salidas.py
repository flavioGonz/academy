#!/usr/bin/env python3
"""Lección 23 · Laboratorio, pasos 5 y 6: un cambio hecho en Safe Mode y las salidas posibles.
Ctrl+X otra vez (o soltar el botón) y /quit lo conservan; Ctrl+D o la sesión cortada lo deshacen.
Fuente: Configuration Management (Ctrl+D deshace, /quit no; sesión que termina de forma anormal deshace)."""
from _anim_red_1_9 import *

a = Anim(T=24, kicker="MIKROTIK · SAFE MODE · LABORATORIO", title="Cómo salís de Safe Mode decide si el cambio queda")
a.steps([
    "En Safe Mode cambiás el nombre: se aplica ya y queda marcado con F.",
    "Ctrl+X otra vez, o soltar el botón: el prompt pierde <SAFE> y el cambio queda.",
    "/quit es una salida normal: el cambio también queda.",
    "Ctrl+D, o una sesión que se corta: RouterOS deshace todo lo de Safe Mode.",
], still=3)

TX, TY, TW = 48, 180, 520
a.add(a.box(TX, TY, TW, 330, a.INK, rx=16))
a.add(a.text(TX + 18, TY + 30, "NEW TERMINAL", 13, SKY, a.MONO, 400, extra='letter-spacing="1.8"'))
base = [("[admin@MikroTik] > Ctrl+X", a.WHITE), ("[Safe Mode taken]", GOLD),
        ("[admin@MikroTik] <SAFE> /system/identity/set", a.WHITE), ("name=LAB-SAFE", a.WHITE)]
for i, (t, c) in enumerate(base):
    a.add(during(a, a.text(TX + 18 + (36 if i == 3 else 0), TY + 66 + i * 34, t, 15, c, a.MONO, 600 if c != a.WHITE else 400), 2 + i * 2, 100, still=1))
VAR = [
    (25, 50, [("[admin@LAB-SAFE] <SAFE> Ctrl+X", a.WHITE), ("[admin@LAB-SAFE] >", a.WHITE), ("sin <SAFE>: confirmado", MINT)], 0),
    (50, 75, [("[admin@LAB-SAFE] <SAFE> /quit", a.WHITE), ("al volver a entrar:", SKY), ("[admin@LAB-SAFE] >", MINT)], 0),
    (75, 100, [("[admin@LAB-SAFE] <SAFE> Ctrl+D", a.WHITE), ("al volver a entrar:", SKY), ("[admin@MikroTik] >", "#FF9E8A")], 1),
]
for t0, t1, ls, st in VAR:
    body = "".join(a.text(TX + 18, TY + 66 + (4 + j) * 34 + 12, t, 15, c, a.MONO, 600 if c != a.WHITE else 400) for j, (t, c) in enumerate(ls))
    a.add(during(a, body, t0, t1, still=st))
a.add(during(a, a.text(TX + 18, TY + 66 + 4 * 34 + 12, "el prompt ya muestra el nombre nuevo", 15, SKY, a.MONO), 12, 25))

# historial
HY = TY + 350
a.add(a.box(TX, HY, TW, 88, a.WHITE, a.LINE, rx=14))
a.add(a.text(TX + 18, HY + 32, "/system/history", 16, a.INK, a.MONO, 600))
a.add(during(a, a.text(TX + 18, HY + 62, "F", 17, a.AMB, a.MONO, 600)
             + a.text(TX + 46, HY + 62, "el cambio de nombre, por admin", 15, a.INK, a.SANS, 600), 10, 100, still=1))
a.add(during(a, a.text(TX + TW - 18, HY + 62, "se deshace si caés", 15, a.AMB, a.MONO, 600, "end"), 10, 25))

# salidas
EX, EW = 600, 552
a.add(a.text(EX, TY + 24, "SALIDAS", 13, a.GREY, a.MONO, 600, extra='letter-spacing="1.8"'))
ROWS = [
    ("Ctrl+X otra vez", "o soltar el botón Safe Mode", "queda: LAB-SAFE", True, 25, 50),
    ("/quit", "salida normal", "queda: LAB-SAFE", True, 50, 75),
    ("Ctrl+D", "salís descartando", "se deshace: MikroTik", False, 75, 100),
    ("sesión cortada", "el router la da por muerta", "se deshace: MikroTik", False, 75, 100),
]
for i, (k, sub, res, ok, t0, t1) in enumerate(ROWS):
    y = TY + 40 + i * 100
    a.add(a.box(EX, y, EW, 90, a.WHITE, a.LINE, rx=14))
    a.add(a.text(EX + 20, y + 36, k, 18, a.INK, a.MONO, 600))
    a.add(a.text(EX + 20, y + 64, sub, 15, a.GREY, a.SANS))
    col, bg = (a.OK, a.OKBG) if ok else (a.BAD, a.BADBG)
    a.add(during(a, a.pill(EX + EW - 20, y + 31, res, col, bg, 15, 30, "end"), t0, 100, still=1))
    a.add(during(a, a.box(EX - 2, y - 2, EW + 4, 94, "none", col, rx=15, sw=3), t0, t1))

a.add(a.text(48, 646, "Confirmá después de cada cambio verificado: así un error posterior no se lleva lo que ya estaba bien.", 16, a.TXT, a.SANS, 600))

write(a, 23, "l1", "Las salidas de Safe Mode",
      "Animación en cuatro tiempos con la terminal, el historial y una tabla de salidas. "
      "1: con Ctrl+X aparece Safe Mode taken; /system/identity/set name=LAB-SAFE se aplica en el acto, el prompt ya muestra LAB-SAFE y el cambio queda marcado con F en /system/history. "
      "2: Ctrl+X otra vez, o soltar el botón Safe Mode de WinBox, confirma: el prompt pierde SAFE y el nombre queda LAB-SAFE. "
      "3: /quit es una salida normal y el cambio también queda. "
      "4: Ctrl+D sale descartando, y una sesión que se corta también deshace: al volver a entrar el nombre es otra vez MikroTik. "
      "Conviene confirmar después de cada cambio verificado.",
      [10, 36, 62, 90])
