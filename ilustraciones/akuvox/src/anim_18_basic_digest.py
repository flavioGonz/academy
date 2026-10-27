#!/usr/bin/env python3
"""Lección 18 · teoría: Basic manda usuario:clave en Base64; Digest responde 401 con nonce y la clave no viaja."""
from _anim_akuvox_15_28 import *

a = new(24, "AKUVOX · LECCIÓN 18", "Basic y Digest: el mismo GET, otra forma de probar la clave")
a.steps([
    "Basic: usuario:clave va en Base64 dentro del encabezado, en un solo pedido.",
    "Quien captura el tráfico lo decodifica: la clave queda a la vista.",
    "Digest: el portero responde 401 con un desafío, un número aleatorio (nonce).",
    "El cliente manda un resumen de clave, ruta y nonce en un segundo pedido. La clave no viaja.",
], still=3, size=17)

for X, name, kind in ((48, "Basic", a.BAD), (612, "Digest", a.OK)):
    a.add(a.box(X, 172, 540, 476, a.WHITE, a.LINE, rx=18))
    a.add(a.text(X + 22, 204, name, 22, a.INK, a.HEAD, 600))
    a.add(lifeline(a, X + 110, 222, 600, "curl", "cliente"))
    a.add(lifeline(a, X + 430, 222, 600, "Portero", "192.168.88.21"))

# ---- Basic
L1, L2 = 48 + 110, 48 + 430
a.add(msg(a, L1, L2, 330, "GET /fcgi/OpenDoor…", 3, sub="Authorization: Basic", sub_color=a.TXT))
a.add(at(a, a.text((L1 + L2) / 2, 378, "Y3VybC1sYWI6RWplbXBsby1DdXJsLTIwMjY=", 15, a.BAD, a.MONO, 600, "middle"), 4))
a.add(at(a, mark(L2 + 52, 330, True) + a.text(L2 + 52, 372, "abre", 15, a.OK, a.MONO, 600, "middle"), 10))
cap = (a.box(72, 452, 492, 116, a.BADBG, a.BAD, rx=12, sw=1.5)
       + a.text(90, 480, "captura del tráfico · Base64 se decodifica:", 15, a.BAD, a.SANS, 600))
a.add(at(a, cap, 26))
a.add(at(a, a.text(90, 514, "Y3VybC1sYWI6RWplbXBsby1…", 15, a.TXT, a.MONO) + a.text(90, 548, "→ curl-lab:Ejemplo-Curl-2026", 17, a.BAD, a.MONO, 600), 31))
a.add(at(a, a.arrow(f"M{(L1 + L2) / 2} 388 V446", a.BAD, 2.5, "5 5"), 27))

# ---- Digest
R1, R2 = 612 + 110, 612 + 430
a.add(msg(a, R1, R2, 320, "GET /fcgi/OpenDoor…", 52))
a.add(msg(a, R2, R1, 384, "401 · desafío", 59, color=a.AMB, sub='nonce="número aleatorio"', sub_color=a.AMB))
a.add(at(a, a.box(R1 - 96, 424, 192, 56, a.AMBBG, a.AMB, rx=10, sw=1.5)
         + a.text(R1, 446, "calcula resumen", 15, a.AMB, a.MONO, 600, "middle")
         + a.text(R1, 468, "clave+ruta+nonce", 15, a.AMB, a.MONO, 500, "middle"), 70))
a.add(msg(a, R1, R2, 520, "GET /fcgi/OpenDoor…", 77, sub="Digest response=resumen", sub_color=a.OK))
a.add(at(a, mark(R2 + 52, 520, True) + a.text(R2 + 52, 562, "abre", 15, a.OK, a.MONO, 600, "middle"), 85))
a.add(at(a, a.pill((R1 + R2) / 2, 590, "la clave no viaja", a.OK, a.OKBG, 15, anchor="middle"), 88))

a.write(*out(18)[:1], title="Autenticación Basic contra Digest",
        desc=("Animación en cuatro tiempos con dos diagramas de secuencia entre curl y el portero 192.168.88.21. "
              "1: con Basic, el GET a /fcgi/OpenDoor lleva el encabezado Authorization: Basic con usuario:clave en Base64 (Y3VybC1sYWI6RWplbXBsby1DdXJsLTIwMjY=) y el portero abre en un solo pedido. "
              "2: quien captura el tráfico decodifica el Base64 y lee curl-lab:Ejemplo-Curl-2026. "
              "3: con Digest, el primer GET recibe un 401 con un desafío, un número aleatorio llamado nonce. "
              "4: el cliente calcula un resumen con la clave, la ruta y el nonce y lo manda en un segundo GET; el portero abre y la clave no viaja."),
        preview=[14, 40, 66, 92], prefix=out(18)[1])
