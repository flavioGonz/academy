#!/usr/bin/env python3
"""Lección 19 · Troncal SIP de Antel · Resumen ("Cómo se ve en la red"): 19-r1.svg.
Dos caminos en la misma central: lo de Antel por LAN1 con la ruta estática, lo de internet por LAN2.
Qué pasa cuando falta la ruta estática: el INVITE sale por el router del cliente a internet y nadie contesta.
Datos de ejemplo: LAN1 198.51.100.2/30, gateway de Antel 198.51.100.1, redes de Antel 203.0.113.0/24,
servidor 203.0.113.10, LAN2 192.168.88.20 con gateway 192.168.88.1.
"""
from _anim_grandstream import G, SITE, PREV

g = G(T=26, fix=40, kicker="GRANDSTREAM · TRONCAL SIP DE ANTEL · CÓMO SE VE EN LA RED", title="Dos caminos en la misma central")
g.steps([
    "Antel manda OPTIONS al puerto de la troncal y la UCM contesta por el mismo puerto.",
    "Una saliente va a 203.0.113.10: la ruta estática la manda por LAN1 a Antel.",
    "Sin la ruta estática, el INVITE sigue la ruta por defecto: router, internet, nadie.",
    "Web, GDMS y actualizaciones salen por LAN2: la troncal no toca internet.",
], size=17)

B, OK, BAD, CY, GREY, INK = g.BLUE, g.OK, g.BAD, g.CYAN, g.GREY, g.INK
Y = 404                      # línea de los cables
# Antel
g.add(g.box(40, 176, 268, 306, "none", CY, rx=20, sw=2, extra='stroke-dasharray="7 7"'))
g.add(g.box(58, 162, 196, 28, g.BG, rx=14) + g.text(72, 182, "red privada de Antel", 14, CY, g.MONO, 600))
g.add(g.node(62, 214, 224, 80, "Servidor SIP", "203.0.113.10"))
g.add(g.node(62, 362, 224, 84, "Gateway Antel", "198.51.100.1"))
g.add(f'<path d="M174 294 V362" stroke="{GREY}" stroke-width="3" stroke-dasharray="8 8"/>')

# UCM
g.add(g.box(396, 176, 408, 306, INK, rx=20))
g.add(g.text(418, 210, "UCM6300 · modo Dual", 20, g.WHITE, g.HEAD, 600))
g.add(g.text(418, 240, "tabla de rutas", 14, "#9FC3E3", g.MONO))
g.add(g.box(416, 252, 368, 44, g.NAVY2, rx=10))
g.add(g.text(430, 280, "203.0.113.0/24 → 198.51.100.1 · LAN", 15, g.WHITE, g.MONO, 600))
g.add(g.box(416, 304, 368, 44, g.NAVY2, rx=10))
g.add(g.text(430, 332, "default → 192.168.88.1 · LAN2", 15, g.WHITE, g.MONO, 600))
# puertos
g.add(g.box(396, Y - 22, 74, 44, CY, rx=8) + g.text(433, Y + 6, "LAN1", 14, g.WHITE, g.MONO, 600, "middle"))
g.add(g.box(730, Y - 22, 74, 44, B, rx=8) + g.text(767, Y + 6, "LAN2", 14, g.WHITE, g.MONO, 600, "middle"))
g.add(g.text(416, Y + 54, "198.51.100.2/30", 15, "#BFF0FF", g.MONO, 600))
g.add(g.text(784, Y + 54, "192.168.88.20", 15, "#C9DDF2", g.MONO, 600, "end"))

# cliente
g.add(g.node(890, 362, 262, 84, "Router del cliente", "192.168.88.1"))
g.add(g.node(890, 196, 262, 84, "Internet", "web, GDMS, updates"))
g.add(f'<path d="M286 {Y} H396" stroke="{g.LINE}" stroke-width="5"/>')
g.add(f'<path d="M804 {Y} H890" stroke="{g.LINE}" stroke-width="5"/>')
g.add(f'<path d="M1021 362 V280" stroke="{g.LINE}" stroke-width="5"/>')

def hl_row(row, color, t0, t1, still=None):
    y = 252 if row == 1 else 304
    g.appear(g.box(412, y - 4, 376, 52, "none", color, rx=12, sw=3.5), t0, t1, still=still)

# 1 · OPTIONS de Antel y 200 OK por el mismo puerto
g.token([(286, Y), (396, Y)], 3, 9, g.chip("OPTIONS", bg=B, size=13, h=24))
g.token([(396, Y), (286, Y)], 13, 19, g.chip("200 OK", bg=OK, size=13, h=24))
g.appear(g.pill(341, Y + 34, "mismo puerto", OK, g.OKBG, 13, 26, "middle"), 13, 25)
# 2 · saliente con la ruta estática
hl_row(1, "#3DDC97", 28, 49)
g.token([(433, Y), (286, Y)], 31, 38, g.chip("INVITE", bg=B, size=13, h=24))
g.token([(286, Y), (396, Y)], 41, 47, g.chip("100 Trying", bg=OK, size=13, h=24), hold=49)
g.appear(g.mark(255, 254, True, 15), 38, 50)
# 3 · sin la ruta estática
g.appear(g.box(412, 248, 376, 52, g.INK, rx=12) + g.text(600, 280, "sin ruta estática", 15, "#F4A99A", g.MONO, 600, "middle"), 52, 75)
hl_row(2, "#F4A99A", 54, 75)
g.token([(730, Y), (804, Y), (890, Y)], 56, 61, g.chip("INVITE", bg=BAD, size=13, h=24))
g.token([(1021, 362), (1021, 280)], 62, 66, g.chip("INVITE", bg=BAD, size=13, h=24))
g.appear(g.mark(1128, 238, False, 15), 66, 75)
g.appear(g.pill(1021, 300, "408 · nadie contesta", BAD, g.BADBG, 13, 26, "middle"), 67, 75)
# 4 · internet por LAN2
hl_row(2, "#3DDC97", 78, 100)
g.token([(730, Y), (804, Y), (890, Y)], 80, 85, g.chip("GDMS", bg=B, size=13, h=24))
g.token([(1021, 362), (1021, 280)], 86, 90, g.chip("GDMS", bg=B, size=13, h=24), hold=100)
g.appear(g.mark(1128, 238, True, 15), 90, 100)

# cuadro fijo: el INVITE del paso 2 sobre el cable de la troncal
g.fijo_only(f'<g transform="translate(341 {Y})">' + g.chip("INVITE", bg=B, size=13, h=24) + '</g>')

# lo que pasa (abajo)
PY = 522
g.add(g.box(48, PY, 1104, 104, g.WHITE, g.LINE, rx=14))
ROWS = [
    (0, 25, "OPTIONS de 203.0.113.10 a 198.51.100.2:5060", "llega por LAN1 y el 200 OK vuelve por LAN1", OK),
    (25, 50, "INVITE de 198.51.100.2 a 203.0.113.10:5060", "la ruta 203.0.113.0/24 lo saca por LAN1 hacia 198.51.100.1", OK),
    (50, 75, "INVITE a 203.0.113.10 sin ruta estática", "sale por default a 192.168.88.1: internet no llega a la red de Antel", BAD),
    (75, 100, "web, GDMS, actualizaciones, internos remotos", "salen por LAN2 con el gateway del cliente", OK),
]
for t0, t1, a, b, col in ROWS:
    g.appear(g.text(72, PY + 40, a, 17, INK, g.MONO, 600) + g.text(72, PY + 74, b, 17, col, g.SANS, 600), t0, t1)
g.add(g.text(1128, PY + 40, "lo que pasa", 15, GREY, g.SANS, 400, "end"))
g.add(g.text(1128, PY + 64, "en la UCM", 15, GREY, g.SANS, 400, "end"))

PCTS = [6, 16, 34, 45, 58, 68, 84, 95]
name = "19-r1.svg"
out = SITE / name
g.save(str(out), "Dos caminos en la misma central",
       "Animación en cuatro tiempos. A la izquierda, la red privada de Antel con el servidor SIP 203.0.113.10 y el gateway 198.51.100.1; al medio, la UCM6300 en modo Dual con el puerto LAN1 198.51.100.2 hacia Antel, el puerto LAN2 192.168.88.20 hacia la red del cliente y su tabla de rutas: 203.0.113.0/24 por 198.51.100.1 y LAN, y la ruta por defecto por 192.168.88.1 y LAN2; a la derecha, el router del cliente e internet. "
       "1: Antel manda un OPTIONS al puerto LAN1 y la UCM contesta 200 OK por el mismo puerto. "
       "2: una saliente va al servidor 203.0.113.10; la ruta estática 203.0.113.0/24 la manda por LAN1 a Antel, que contesta 100 Trying. "
       "3: sin la ruta estática, el mismo INVITE sigue la ruta por defecto, sale por LAN2 al router del cliente y a internet, que no llega a la red privada de Antel: nadie contesta y la llamada termina en 408. "
       "4: lo que sí va a internet, como la web, GDMS, las actualizaciones y los internos remotos, sale por LAN2 con el gateway del cliente; la troncal nunca toca internet. Datos de ejemplo.")
for old in PREV.glob("_rev-19-r1-*.png"):
    old.unlink()
g._last = out
g.preview(PCTS, str(PREV / "_rev-19-r1"))
kb = out.stat().st_size / 1024
print(f"{name}: {kb:.0f} KB")
assert kb < 120
