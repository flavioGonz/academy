#!/usr/bin/env python3
"""Lección 14 · teoría: el intercambio Digest de la HTTP API, contra Basic y Allowlist."""
from _anim_akuvox import Anim, A, draw_arrow, token, chip, lane, note, appear, mark, finish

a = Anim(T=25, kicker="AKUVOX · QUIÉN PUEDE ABRIR", title="Digest: probar la clave sin mandarla")
a.steps([
    "El cliente pide el recurso sin credencial.",
    "El portero responde 401 con un desafío que incluye un nonce.",
    "El cliente calcula el hash de usuario, clave, nonce y pedido, y repite.",
    "El portero hace la misma cuenta con la clave que guarda: coincide.",
    "Con una clave mala el resumen no coincide: error de autenticación.",
], still=3)

XC, XP = 170, 640
lane(a, XC, 176, 640, "Cliente", "pylocal-akuvox", w=220)
lane(a, XP, 176, 640, "Portero", "HTTP API · Digest", w=220)


def msg(x1, x2, y, s, color, t0, t1, dashed=False, tok=None, hold=100, still=1):
    draw_arrow(a, [(x1, y), (x2, y)], t0, t1, color, dashed=dashed, hold=hold, still=still)
    appear(a, a.text((x1 + x2) / 2, y - 11, s, 15, color, A.MONO, 600, "middle"), t1 - 0.5, hold, still=still)
    if tok:
        token(a, [(x1, y), (x2, y)], t0, t1, chip(a, tok, bg=color, size=13, h=24))


msg(XC, XP, 276, "pedido · sin credencial", A.BLUE, 3, 9, tok="pedido")
msg(XP, XC, 326, "401 · desafío con nonce", A.GREY, 22, 27, dashed=True)
appear(a, a.box(XC - 100, 352, 200, 50, A.AMBBG, A.AMB, rx=10, sw=1.5)
       + a.text(XC, 373, "hash(usuario, clave,", 14, A.AMB, A.MONO, 600, "middle")
       + a.text(XC, 393, "nonce, pedido)", 14, A.AMB, A.MONO, 600, "middle"), 41, 100, still=1)
msg(XC, XP, 432, "pedido + resumen (api-lab)", A.BLUE, 46, 52, tok="resumen")
appear(a, a.box(XP - 100, 446, 200, 50, A.OKBG, A.OK, rx=10, sw=1.5)
       + a.text(XP, 467, "misma cuenta con", 14, A.OK, A.MONO, 600, "middle")
       + a.text(XP, 487, "la clave guardada", 14, A.OK, A.MONO, 600, "middle"), 62, 100, still=1)
msg(XP, XC, 530, "200 · modelo y firmware", A.OK, 66, 72)
appear(a, mark(a, XP + 126, 471, True, 14), 64, 80, still=1)

# 5: clave mala
appear(a, a.box(XC - 110, 556, XP - XC + 220, 76, A.BADBG, None, rx=12), 81, 100, still=0)
msg(XC, XP, 582, "pedido + resumen con clave mala", A.BAD, 82, 87, hold=100, still=0)
msg(XP, XC, 618, "rechazo · error de autenticación", A.BAD, 90, 94, dashed=True, hold=100, still=0)

# panel lateral: los otros modos
PX, PW = 800, 352
s, _ = note(a, PX, 186, PW, "Digest", ["La clave nunca viaja tal cual:", "viaja una prueba de que", "el cliente la conoce."], "ok")
a.add(s)
s, h = note(a, PX, 312, PW, "Basic", ["Manda usuario:clave en Base64", "en cada pedido. No es cifrado:", "", ""], "bad")
a.add(s)
a.add(a.text(PX + 20, 312 + 30 + 26 + 44, "YXBpLWxhYjpFamVtcGxvLUFwaS0yMDI2", 14, A.BAD, A.MONO, 600))
a.add(a.text(PX + 20, 312 + 30 + 26 + 66, "= api-lab:Ejemplo-Api-2026", 14, A.BAD, A.MONO, 600))
s, _ = note(a, PX, 470, PW, "Allowlist", ["Sin usuario: el portero mira la", "IP de origen del paquete y la", "compara con su lista."], "info")
a.add(s)

finish(a, "14-t1.svg", "Digest: probar la clave sin mandarla",
       "Animación en cinco tiempos con dos líneas de vida: el cliente, un script con pylocal-akuvox, y el portero con la HTTP API en modo Digest. "
       "1: el cliente pide el recurso sin credencial. 2: el portero responde 401 con un desafío que incluye un nonce. "
       "3: el cliente calcula el hash de usuario, clave, nonce y pedido y repite el pedido con ese resumen, con el usuario api-lab. "
       "4: el portero hace la misma cuenta con la clave que tiene guardada; coincide y responde con modelo y firmware. "
       "5: con una clave mala el resumen no coincide y el portero rechaza el pedido: error de autenticación. "
       "Al costado, los otros modos: con Digest la clave nunca viaja tal cual; Basic manda usuario:clave en Base64 en cada pedido, y YXBpLWxhYjpFamVtcGxvLUFwaS0yMDI2 se decodifica como api-lab:Ejemplo-Api-2026; "
       "con Allowlist no hay usuario y el portero compara la IP de origen con su lista.",
       [8, 28, 50, 72, 95])
