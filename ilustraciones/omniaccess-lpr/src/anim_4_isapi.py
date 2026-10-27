"""Teoría de Alta guiada: la puesta a punto por ISAPI y el primer evento, que la cámara manda con su MAC."""
from _anim_lpr import *

caps = ["Hora del servidor y destino de los eventos: dos PUT por ISAPI.",
        "GET VCAResource: si no dice roadDetection, error. No se fuerza.",
        "Video H.264 en 101 y 102, video en vivo y carga de matrículas.",
        "Primer evento: llega con la IP del router, pero el XML trae la MAC."]
a = new(24, "Puesta a punto", "Crear y poner a punto: pedidos ISAPI y el primer evento", caps, still=3)

SX, CX = 250, 1000
a.add(card(a, 60, 172, 380, 62, "Servidor OmniAccess", "192.0.2.10", dark=True, tsize=18))
a.add(card(a, 790, 172, 362, 62, "P1 - Entrada (21)", "192.0.2.21 · Hikvision", tsize=18))
for x in (SX, CX):
    a.add(line(a, x, 234, x, 650, a.LINE, 2, "5 6", arrow=False))


def msg(y, label, step, back=False, color=None, sub=None, d0=0):
    c = color or a.BLUE
    x1, x2 = (CX - 8, SX + 8) if back else (SX + 8, CX - 8)
    s = line(a, x1, y, x2, y, c, 3) + a.text(SX + 24, y - 10, label, 15, a.INK, a.MONO, 600)
    if sub:
        s += a.text(SX + 24, y + 22, sub, 15, a.GREY, a.MONO)
    vis(a, s, step, 3, d0=d0)


def ok(y, label, step, fg=None, bg=None, d0=4):
    vis(a, a.pill(CX - 14, y - 14, label, fg or a.OK, bg or a.OKBG, size=14, anchor="end"), step, 3, d0=d0)


msg(282, "PUT /ISAPI/System/time", 0)
ok(282 + 24, "ok", 0, d0=3)
msg(334, "PUT /ISAPI/Event/notification/httpHosts/1", 0, sub="destino 192.0.2.10:10000/api/webhooks/hikvision", d0=6)
ok(334 + 24, "ok", 0, d0=9)
msg(404, "GET .../VCAResource", 1)
vis(a, line(a, CX - 8, 432, SX + 8, 432, a.OK, 2.5, "7 5") + a.pill(SX + 24, 418, "<type>roadDetection</type>", a.OK, a.OKBG, size=14), 1, 3, d0=5)
vis(a, a.text(SX + 24, 458, "si no lo dice: error, sin forzar (pide reiniciar)", 15, a.AMB, a.SANS, 600), 1, 3, d0=8)
msg(496, "PUT /ISAPI/Streaming/channels/101 y 102 · H.264", 2)
ok(496 + 24, "ok", 2, d0=3)
msg(546, "matrículas: carga incremental", 2, d0=7)
vis(a, a.text(SX - 14, 492, "registra el", 15, a.TXT, a.SANS, 600, "end") + a.text(SX - 14, 512, "video en vivo", 15, a.TXT, a.SANS, 600, "end"), 2, 3, d0=10)

# 4 · primer evento a través del NAT
s0, s1 = ph(a, 3)
vis(a, a.box(560, 590, 130, 44, a.SLATE, a.GREY, rx=10) + a.text(625, 618, "router NAT", 15, a.INK, a.MONO, 600, "middle"), 3)
vis(a, line(a, CX - 8, 612, 690, 612, a.CYAN, 3, arrow=False) + line(a, 560, 612, SX + 8, 612, a.CYAN, 3)
    + a.text(708, 600, "POST · XML con MAC", 15, a.INK, a.MONO, 600)
    + a.text(SX + 20, 640, "origen 198.51.100.7", 15, a.GREY, a.MONO), 3, d0=1)
token(a, "evento", [(s0 + 2, CX - 50, 612), (s0 + 9, 625, 612), (s0 + 12, 625, 612), (s0 + 18, SX + 60, 612), (s1, SX + 60, 612)], size=13)
vis(a, a.text(SX - 14, 596, "MAC 00:00:5E:00:53:21", 15, a.INK, a.MONO, 600, "end")
    + a.text(SX - 14, 618, "= P1 - Entrada (21)", 15, a.OK, a.SANS, 600, "end")
    + a.text(SX - 14, 640, "si no, por IP", 15, a.GREY, a.SANS, 400, "end"), 3, d0=16)
write(a, "4-t1.svg", "Puesta a punto por ISAPI", [12, 37, 62, 92])
