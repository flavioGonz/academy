#!/usr/bin/env python3
"""Lección 2 · teoría: REGISTER con Digest (401, cálculo, 200 OK) y por qué importa la contraseña aleatoria."""
from _anim_grandstream import G

g = G(T=25, fix=70, kicker="GRANDSTREAM · REGISTRO SIP", title="Digest: el teléfono prueba la clave sin mandarla")
g.steps([
    "El teléfono manda REGISTER con su número, sin credenciales.",
    "La central responde 401: un desafío con un número a resolver (nonce).",
    "El teléfono calcula con su contraseña y ese número, y repite el REGISTER.",
    "La central hace la misma cuenta con la clave que guarda: coincide, 200 OK.",
    "Un barrido prueba claves una tras otra: con la aleatoria, todas fallan.",
])

XT, XU = 160, 620
g.lane(XT, 176, 630, "Teléfono", "extensión 1001", w=220)
g.lane(XU, 176, 630, "UCM", "192.168.88.20", w=220)

g.msg(XT, XU, 280, "REGISTER 1001", g.BLUE, 2, 9, tok="REGISTER")
g.msg(XU, XT, 336, "401 · desafío con nonce", g.GREY, 22, 28, dashed=True)
g.appear(g.box(XT - 105, 360, 210, 52, g.AMBBG, g.AMB, rx=10, sw=1.5)
         + g.text(XT, 382, "cálculo(contraseña,", 14, g.AMB, g.MONO, 600, "middle")
         + g.text(XT, 401, "nonce, pedido)", 14, g.AMB, g.MONO, 600, "middle"), 42, 100)
g.msg(XT, XU, 452, "REGISTER + resultado", g.BLUE, 46, 53, tok="resultado")
g.appear(g.box(XU - 105, 470, 210, 52, g.OKBG, g.OK, rx=10, sw=1.5)
         + g.text(XU, 492, "misma cuenta con", 14, g.OK, g.MONO, 600, "middle")
         + g.text(XU, 511, "la clave guardada", 14, g.OK, g.MONO, 600, "middle"), 62, 100)
g.appear(g.mark(XU + 130, 496, True, 14), 64, 100)
g.msg(XU, XT, 568, "200 OK · registrado", g.OK, 66, 72)
g.appear(g.pillc(XT, 590, "registrado", g.OK, g.OKBG), 72, 100)

# panel derecho
PX, PW = 790, 362
g.add(g.note(PX, 186, PW, "Lo que viaja por la red", ["El número 1001, el nonce y el", "resultado del cálculo.", "La contraseña, nunca."], "ok"))
g.add(g.note(PX, 318, PW, "Concurrent Registrations", ["Cuántos equipos pueden tener", "esa cuenta registrada a la vez:", "3 de fábrica, hasta 10."], "info"))

# tiempo 5: el barrido
g.appear(g.box(PX, 450, PW, 182, g.BADBG, None, rx=12) + g.text(PX + 20, 480, "Barrido desde internet", 17, g.BAD, g.SANS, 600), 80, 100)
for i, (clave, t) in enumerate([("1001", 82), ("1234", 86), ("123456", 90)]):
    y = 512 + i * 30
    g.appear(g.text(PX + 20, y, f"REGISTER 1001 · clave {clave}", 15, g.INK, g.MONO, 600), t, 100)
    g.appear(g.text(PX + PW - 20, y, "falla", 15, g.BAD, g.MONO, 600, "end"), t + 1.5, 100)
g.appear(g.text(PX + 20, 616, "Aleatoria de 10+ caracteres: no se adivina.", 15, g.BAD, g.SANS, 600), 93, 100)

g.finish(2, 1, "Digest: el teléfono prueba la clave sin mandarla",
         "Animación en cinco tiempos con dos líneas de vida, el teléfono de la extensión 1001 y la UCM en 192.168.88.20. "
         "1: el teléfono manda REGISTER 1001 sin credenciales. 2: la central responde 401 con un desafío que trae un número a resolver, el nonce. "
         "3: el teléfono hace un cálculo con su contraseña, el nonce y el pedido, y repite el REGISTER con el resultado. "
         "4: la central hace la misma cuenta con la clave que tiene guardada; coincide y responde 200 OK: el teléfono queda registrado. "
         "5: un barrido desde internet prueba claves una tras otra contra la 1001 (1001, 1234, 123456) y todas fallan, porque la contraseña aleatoria de 10 caracteres o más no se adivina. "
         "Al costado: por la red viajan el número, el nonce y el resultado, nunca la contraseña; Concurrent Registrations limita cuántos equipos pueden tener la cuenta registrada a la vez, 3 de fábrica y hasta 10.",
         [6, 26, 48, 70, 96])
