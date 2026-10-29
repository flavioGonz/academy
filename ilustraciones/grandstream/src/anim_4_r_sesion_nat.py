#!/usr/bin/env python3
"""Lección 4 · Resumen, "Cómo se ve en la red": por qué el troncal registrado no pide reenvío de puertos.
La UCM inicia el REGISTER, el router del cliente arma una sesión de NAT y por ella vuelven las respuestas y entran
las llamadas mientras el registro se renueva. Fuentes: la lección (la UCM inicia la conversación y las respuestas
vuelven por la sesión; Simtex: en el 99,9 % de los casos no hace falta reenviar puertos); RFC 3261 (REGISTER, 401,
INVITE a la dirección registrada); RFC 4787 (sesiones UDP del NAT)."""
from _anim_gs_red import R

g = R(T=26, fix=62, kicker="GRANDSTREAM · TRONCAL REGISTRADO · CÓMO SE VE EN LA RED",
      title="La sesión que abre el REGISTER: sin reenviar puertos")
g.steps([
    "La UCM sale a registrarse: el router cambia el origen y anota la sesión.",
    "El 401 y el 200 OK vuelven a esa dirección: el router los pasa a la UCM.",
    "Entra una llamada: el proveedor manda el INVITE a donde se registró la UCM.",
    "La UCM renueva el registro antes de que venza: la sesión sigue abierta.",
])

Y, H = 190, 96
YL = Y + H / 2
g.add(g.dev(48, Y, 240, H, "UCM", "192.168.88.20", icon="ucm", dark=True))
g.add(g.dev(352, Y, 270, H, "Router cliente", "NAT", icon="router", sub2="WAN 203.0.113.10"))
g.add(g.cloud(668, Y + 14, 120, 68))
g.add(g.dev(834, Y, 318, H, "Proveedor", "sip.proveedor.example", icon="antel"))
g.add(g.wire(288, YL, 352, YL, g.BLUE))
g.add(g.wire(622, YL, 668, YL, g.BLUE))
g.add(g.wire(788, YL, 834, YL, g.BLUE))

LANE = Y - 20
A, B = 168, 993
mid = 487
g.token([(A, LANE), (B, LANE)], 3, 14, g.chip("REGISTER", bg=g.BLUE, size=13, h=26), hold=15)
g.token([(B, LANE), (A, LANE)], 28, 36, g.chip("401", bg=g.GREY, size=13, h=26), hold=37)
g.token([(A, LANE), (B, LANE)], 37, 42, g.chip("REGISTER + clave", bg=g.BLUE, size=13, h=26), hold=43)
g.token([(B, LANE), (A, LANE)], 42, 49, g.chip("200 OK", bg=g.OK, size=13, h=26), hold=50)
g.token([(B, LANE), (A, LANE)], 53, 68, g.chip("INVITE · llamada entrante", bg=g.CYAN, size=13, h=26), hold=72)
g.token([(A, LANE), (B, LANE)], 78, 86, g.chip("REGISTER (renovación)", bg=g.BLUE, size=13, h=26), hold=87)
g.token([(B, LANE), (A, LANE)], 88, 95, g.chip("200 OK", bg=g.OK, size=13, h=26), hold=96)
g.appear(g.pillc(168, Y + H + 12, "registrado", g.OK, g.OKBG, 13, 26), 49, 100)
g.appear(g.pillc(168, Y + H + 12, "suena la entrante", g.CYAN, "#E3F4FA", 13, 26), 68, 76)

# tabla de NAT del router
PY = 346
g.add(g.box(48, PY, 640, 210, g.WHITE, g.LINE, rx=16))
g.add(g.text(68, PY + 34, "Sesión UDP que anotó el router", 17, g.INK, g.SANS, 600))
rows = [("adentro", "192.168.88.20:5060"), ("afuera", "203.0.113.10:40112"), ("del otro lado", "sip.proveedor.example:5060")]
for k, (n, v) in enumerate(rows):
    yy = PY + 76 + k * 34
    g.appear(g.text(68, yy, n, 15, g.GREY, g.MONO) + g.text(260, yy, v, 17, g.INK, g.MONO, 600), 8, 100)
g.appear(g.text(68, PY + 76, "(todavía vacía: nadie salió)", 16, g.GREY, g.SANS), 0, 8)
g.appear(g.pillc(560, PY + 186, "abierta", g.OK, g.OKBG, 14, 28), 8, 100)
g.appear(g.box(250, PY + 88, 420, 32, "none", g.BLUE, rx=8, sw=2.5), 28, 50)
g.appear(g.box(250, PY + 88, 420, 32, "none", g.CYAN, rx=8, sw=2.5), 53, 75)
g.appear(g.text(68, PY + 190, "se renueva con cada REGISTER", 15, g.OK, g.SANS, 600), 78, 100)

NX, NW = 714, 438
g.appear(g.note(NX, PY, NW, "La UCM empieza la charla", ["El router reemplaza el origen privado por", "203.0.113.10 y un puerto suyo, y se lo anota."], "info"), 0, 25)
g.appear(g.note(NX, PY, NW, "Las respuestas vuelven solas", ["Llegan a 203.0.113.10:40112: el router", "busca la sesión y las entrega a la UCM."], "ok"), 25, 50)
g.appear(g.note(NX, PY, NW, "La entrante usa el mismo camino", ["El proveedor manda el INVITE a la", "dirección del registro, y entra por la sesión."], "ok"), 50, 75)
g.appear(g.note(NX, PY, NW, "Ningún puerto abierto hacia la UCM", ["Simtex: en el 99,9 % de los casos no hace", "falta reenviar puertos para el troncal."], "ok"), 75, 100)

g.status(612, [
    (0, 25, "El puerto 40112 es un ejemplo: lo elige el router.", g.GREY),
    (25, 50, "Rejected sale de acá si la UCM no llega al proveedor o la clave no coincide.", g.AMB),
    (50, 75, "Sin reenvío de puertos, la llamada entra igual.", g.OK),
    (75, 100, "Registro vigente, sesión abierta: el troncal recibe llamadas.", g.OK),
])

g.done(4, "r1", "La sesión que abre el REGISTER",
       "Animación en cuatro tiempos con la UCM en 192.168.88.20, el router del cliente con NAT y WAN 203.0.113.10, internet y el proveedor sip.proveedor.example; abajo, la sesión UDP que anota el router. "
       "1: la UCM manda REGISTER al proveedor; el router reemplaza el origen privado 192.168.88.20:5060 por 203.0.113.10 y un puerto propio, por ejemplo 40112, y anota la sesión. "
       "2: el 401 y, después del REGISTER con la clave, el 200 OK vuelven a 203.0.113.10:40112; el router encuentra la sesión y los entrega a la UCM, que queda registrada. "
       "3: entra una llamada: el proveedor manda el INVITE a la dirección del registro y entra por la misma sesión. "
       "4: la UCM renueva el registro antes de que venza y la sesión sigue abierta. "
       "Por eso, como dice Simtex, en el 99,9 % de los casos el troncal registrado no necesita reenvío de puertos.",
       [8, 40, 62, 90])
