#!/usr/bin/env python3
"""Lección 19 · Troncal SIP de Antel · Laboratorio, paso 5: 19-l1.svg.
Los OPTIONS de Antel: 200 OK cuando vienen del Host Name del troncal; rechazo cuando vienen de una IP
que no está en ningún troncal (el caso publicado de FreePBX contestaba 401); el heartbeat de la UCM.
Datos de ejemplo: servidores 203.0.113.10 (Host Name) y 203.0.113.11, UCM 198.51.100.2.
"""
from _anim_grandstream import G, SITE, PREV

g = G(T=26, fix=95, kicker="GRANDSTREAM · TRONCAL SIP DE ANTEL · PASO 5", title="El OPTIONS de Antel: 200 OK o rechazo")
g.steps([
    "OPTIONS desde 203.0.113.10, el Host Name: la UCM lo reconoce y contesta 200 OK.",
    "Heartbeat de la UCM: su OPTIONS cada 60 s. Si Antel contesta, no queda Unreachable.",
    "OPTIONS desde 203.0.113.11, una IP que no está en ningún troncal: rechazo.",
    "Con esa IP en un troncal y en la Allowlist de Fail2ban, también recibe su 200 OK.",
], size=17)

B, OK, BAD, GREY, INK = g.BLUE, g.OK, g.BAD, g.GREY, g.INK
X10, XU, X11 = 150, 470, 790
g.lane(X10, 170, 530, "Antel", "203.0.113.10", w=200)
g.lane(XU, 170, 530, "UCM · LAN1", "198.51.100.2", w=200)
g.lane(X11, 170, 530, "Antel", "203.0.113.11", w=200)
R = [262, 302, 352, 392, 442, 482, 0, 0]

g.msg(X10, XU, R[0], "OPTIONS", B, 3, 9, tok="OPTIONS")
g.msg(XU, X10, R[1], "200 OK", OK, 11, 17, tok="200 OK")
g.msg(XU, X10, R[2], "OPTIONS · heartbeat", GREY, 28, 34, tok="OPTIONS")
g.msg(X10, XU, R[3], "200 OK", OK, 36, 42)
g.msg(X11, XU, R[4], "OPTIONS", B, 53, 59, tok="OPTIONS")
g.msg(XU, X11, R[5], "401 o 404 · no es un troncal", BAD, 61, 67, hold=75, tok="401", still=0)
g.appear(g.mark(XU - 32, R[4] + 2, False, 14), 60, 75, still=0)
g.msg(XU, X11, R[5], "200 OK", OK, 80, 86, still=1)
g.appear(g.mark(XU - 32, R[4] + 2, True, 14), 79, 100)

# troncales configurados (derecha)
PX, PW = 910, 242
g.add(g.box(PX, 176, PW, 290, g.WHITE, g.LINE, rx=14))
g.add(g.text(PX + 20, 208, "VoIP Trunks", 17, INK, g.SANS, 600))
g.add(g.text(PX + 20, 232, "Peer SIP Trunk", 14, GREY, g.MONO))
g.add(g.box(PX + 16, 246, PW - 32, 64, g.SLATE, rx=10))
g.add(g.text(PX + 30, 272, "Antel_Troncal", 16, INK, g.MONO, 600))
g.add(g.text(PX + 30, 296, "Host 203.0.113.10", 15, g.TXT, g.MONO))
g.appear(g.box(PX + 16, 320, PW - 32, 64, g.OKBG, rx=10) + g.text(PX + 30, 346, "Antel_2", 16, INK, g.MONO, 600)
         + g.text(PX + 30, 370, "Host 203.0.113.11", 15, g.TXT, g.MONO), 77, 100)
g.appear(g.box(PX + 16, 320, PW - 32, 64, g.BADBG, rx=10) + g.text(PX + 30, 346, "203.0.113.11", 16, BAD, g.MONO, 600)
         + g.text(PX + 30, 370, "en ningún troncal", 15, BAD, g.SANS, 600), 52, 76, still=0)
g.add(g.text(PX + 20, 414, "Dashboard · Trunks", 14, GREY, g.MONO))
g.appear(g.pill(PX + 20, 426, "Unmonitored", GREY, g.SLATE, 13, 26), 0, 27, still=0)
g.appear(g.pill(PX + 20, 426, "contesta: disponible", OK, g.OKBG, 13, 26), 42, 100)
g.appear(g.pill(PX + 20, 426, "esperando respuesta", g.AMB, g.AMBBG, 13, 26), 27, 42, still=0)

# lo que muestra la captura (abajo)
PY = 548
g.add(g.box(48, PY, 1104, 92, g.WHITE, g.LINE, rx=14))
ROWS = [
    (0, 25, "203.0.113.10 → 198.51.100.2  OPTIONS  ·  198.51.100.2 → 203.0.113.10  200 OK", "Antel ve la central viva: lo que pide la planilla", OK, 0),
    (25, 50, "198.51.100.2 → 203.0.113.10  OPTIONS  ·  203.0.113.10 → 198.51.100.2  200 OK", "si Antel no contesta y queda Unreachable, apagá el heartbeat", g.AMB, 0),
    (50, 75, "203.0.113.11 → 198.51.100.2  OPTIONS  ·  198.51.100.2 → 203.0.113.11  401", "IP que no es un Host Name: pedile a Antel todas sus IP", BAD, 0),
    (75, 100, "203.0.113.11 → 198.51.100.2  OPTIONS  ·  198.51.100.2 → 203.0.113.11  200 OK", "las dos IP de Antel contestadas: entrantes de cualquiera de las dos", OK, 1),
]
for t0, t1, a, b, col, st in ROWS:
    g.appear(g.text(72, PY + 36, a, 15, INK, g.MONO, 600) + g.text(72, PY + 68, b, 17, col, g.SANS, 600), t0, t1, still=st)

PCTS = [6, 16, 32, 40, 58, 66, 84, 96]
name = "19-l1.svg"
out = SITE / name
g.save(str(out), "El OPTIONS de Antel: 200 OK o rechazo",
       "Animación en cuatro tiempos con tres columnas: dos servidores de Antel de ejemplo, 203.0.113.10 y 203.0.113.11, y la UCM en LAN1 198.51.100.2. A la derecha, los troncales configurados y el estado en el Dashboard; abajo, lo que muestra la captura. "
       "1: Antel manda OPTIONS desde 203.0.113.10, que es el Host Name del Peer SIP Trunk Antel_Troncal, y la UCM contesta 200 OK. "
       "2: con Enable Heartbeat Detection, la UCM manda su propio OPTIONS cada 60 segundos; si Antel contesta, el troncal figura disponible; si no contesta y queda Unreachable aunque los OPTIONS de Antel tengan respuesta, se apaga el heartbeat. "
       "3: llega un OPTIONS desde 203.0.113.11, una IP que no está en ningún troncal; la UCM no sabe que es Antel y lo rechaza, por ejemplo con 401 o 404, como en un caso publicado de FreePBX que contestaba 401. "
       "4: con esa IP cargada en un segundo troncal, Antel_2, y la red de Antel en la Allowlist de Fail2ban, el OPTIONS de 203.0.113.11 también recibe 200 OK. Datos de ejemplo.")
for old in PREV.glob("_rev-19-l1-*.png"):
    old.unlink()
g._last = out
g.preview(PCTS, str(PREV / "_rev-19-l1"))
kb = out.stat().st_size / 1024
print(f"{name}: {kb:.0f} KB")
assert kb < 120
