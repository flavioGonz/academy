#!/usr/bin/env python3
"""Lección 19 · Troncal SIP de Antel · Laboratorio, paso 8: 19-l2.svg.
La saliente y el caller ID: con el número de la interna en el From, Antel la rechaza (en la captura, 403);
con Keep Trunk CID sale con el número de la troncal; con DOD, cada interna con su número directo.
El orden de prioridad es el del manual del UCM630x. Datos de ejemplo: interna 1003, celular 099 000 001,
números de la troncal 2900 1001 a 2900 1008, servidor 203.0.113.10.
"""
from _anim_grandstream import G, SITE, PREV

g = G(T=26, fix=60, kicker="GRANDSTREAM · TRONCAL SIP DE ANTEL · PASO 8", title="La saliente sale con un número de la troncal")
g.steps([
    "La 1003 llama a un celular y sale con su número de interna: Antel la rechaza.",
    "Con Keep Trunk CID, el From lleva 29001001: Antel la acepta y el celular suena.",
    "Con DOD por interna y Keep Trunk CID en No, la 1003 sale con su número directo.",
], size=17)

B, OK, BAD, GREY, INK, CY = g.BLUE, g.OK, g.BAD, g.GREY, g.INK, g.CYAN
XI, XU, XA = 150, 450, 760
g.lane(XI, 170, 520, "Interna 1003", "GRP2614", w=200)
g.lane(XU, 170, 520, "UCM", "198.51.100.2", w=200)
g.lane(XA, 170, 520, "Antel", "203.0.113.10", w=200)

# 1 · rechazo
g.msg(XI, XU, 254, "INVITE 099000001", B, 3, 7, hold=33, still=0)
g.msg(XU, XA, 294, "From: 1003", BAD, 8, 13, hold=33, tok="INVITE", still=0)
g.msg(XA, XU, 334, "403 Forbidden", BAD, 15, 20, hold=33, tok="403", still=0)
g.msg(XU, XI, 374, "rechazada", BAD, 21, 25, hold=33, still=0)
# 2 · Keep Trunk CID
g.msg(XI, XU, 254, "INVITE 099000001", B, 36, 40, hold=66, still=1)
g.msg(XU, XA, 294, "From: 29001001", OK, 41, 46, hold=66, tok="INVITE", still=1)
g.msg(XA, XU, 334, "180 Ringing · 200 OK", OK, 48, 53, hold=66, tok="200 OK", still=1)
g.appear(g.pillc((XU + XA) / 2, 362, "el celular ve 2900 1001", OK, g.OKBG, 14, 28), 54, 66)
# 3 · DOD
g.msg(XI, XU, 254, "INVITE 099000001", B, 69, 73, still=0)
g.msg(XU, XA, 294, "From: 29001003", OK, 74, 79, tok="INVITE", still=0)
g.msg(XA, XU, 334, "180 Ringing · 200 OK", OK, 81, 86, tok="200 OK", still=0)
g.appear(g.pillc((XU + XA) / 2, 362, "el celular ve 2900 1003", OK, g.OKBG, 14, 28), 87, 100, still=0)

# prioridad del caller ID (manual del UCM630x)
PX, PW = 900, 252
g.add(g.box(PX, 170, PW, 350, g.WHITE, g.LINE, rx=14))
g.add(g.text(PX + 18, 200, "Quién pone el número", 17, INK, g.SANS, 600))
g.add(g.text(PX + 18, 222, "de más a menos prioridad", 14, GREY, g.SANS))
ITEMS = ["Keep Original CID", "Troncal · Keep Trunk CID", "DOD de la interna", "CallerID de la interna", "Troncal sin Keep Trunk", "Global Outbound CID"]
for i, s in enumerate(ITEMS):
    y = 246 + i * 44
    g.add(g.box(PX + 14, y, PW - 28, 36, g.SLATE, rx=8))
    g.add(g.text(PX + 28, y + 24, f"{i + 1}. {s}", 15, g.TXT, g.SANS, 500))
def hl(i, color, bg, t0, t1, still=None):
    y = 246 + i * 44
    g.appear(g.box(PX + 14, y, PW - 28, 36, bg, color, rx=8, sw=2.5) + g.text(PX + 28, y + 24, f"{i + 1}. {ITEMS[i]}", 15, color, g.SANS, 600), t0, t1, still=still)
hl(3, BAD, g.BADBG, 8, 33)
hl(1, OK, g.OKBG, 41, 66)
hl(2, OK, g.OKBG, 74, 100)

# lo que muestra la captura (abajo)
PY = 540
g.add(g.box(48, PY, 1104, 96, g.WHITE, g.LINE, rx=14))
ROWS = [
    (0, 33, "From: <sip:1003@198.51.100.2>   →   SIP/2.0 403 Forbidden", "1003 no es un número de la troncal: Antel rechaza o saca el número por defecto", BAD, 0),
    (33, 66, "From: <sip:29001001@198.51.100.2>   →   180 Ringing, 200 OK", "Keep Trunk CID en Sí: todas las salientes con el número principal", OK, 1),
    (66, 100, "From: <sip:29001003@198.51.100.2>   →   180 Ringing, 200 OK", "DOD de la 1003 y Keep Trunk CID en No: cada interna con su número", OK, 0),
]
for t0, t1, a, b, col, st in ROWS:
    g.appear(g.text(72, PY + 38, a, 15, INK, g.MONO, 600) + g.text(72, PY + 72, b, 17, col, g.SANS, 600), t0, t1, still=st)

PCTS = [5, 12, 22, 44, 55, 76, 92]
name = "19-l2.svg"
out = SITE / name
g.save(str(out), "La saliente sale con un número de la troncal",
       "Animación en tres tiempos con tres columnas: la interna 1003, la UCM y Antel con el servidor 203.0.113.10; a la derecha, el orden en que la UCM elige el caller ID según su manual: Keep Original CID, el número del troncal con Keep Trunk CID, el DOD de la interna, el CallerID de la interna, el número del troncal sin Keep Trunk CID y el Global Outbound CID; abajo, el From que se ve en la captura. "
       "1: la 1003 llama al celular 099 000 001 de ejemplo; la UCM manda el INVITE con From 1003, el CallerID de la interna, y Antel lo rechaza: en la captura se ve un 403 Forbidden. Antel también puede sacarla con el número por defecto del servicio. "
       "2: con Keep Trunk CID en Sí, el From lleva 29001001, el número de la troncal; Antel contesta 180 Ringing y 200 OK, y el celular ve 2900 1001. "
       "3: con DOD asignado a la 1003 y Keep Trunk CID en No, el From lleva 29001003 y el celular ve el número directo de la interna. Todos los números son de ejemplo.")
for old in PREV.glob("_rev-19-l2-*.png"):
    old.unlink()
g._last = out
g.preview(PCTS, str(PREV / "_rev-19-l2"))
kb = out.stat().st_size / 1024
print(f"{name}: {kb:.0f} KB")
assert kb < 120
