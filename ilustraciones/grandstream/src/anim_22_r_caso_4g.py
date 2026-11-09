#!/usr/bin/env python3
"""Caso de estudio · Video de un lado · Resumen ("Cómo se ve en la red"): 22-r1.svg.
El caso: GXV3350 del depósito detrás de un 4G con poca subida; manda 720P a 2048 kbps (de fábrica) y la subida
no da: el video hacia recepción llega con pérdida y se ve negro o congelado; el video que va al depósito llega entero.
Arreglo (recomendado en el manual del GXV3350): H.264 Image Size VGA y Video Bit Rate 384 kbps. Datos de ejemplo.
"""
from _anim_gs_red import R

g = R(T=28, fix=94, kicker="GRANDSTREAM · CASO DE ESTUDIO · VIDEO DE UN LADO", title="El caso en la red: una subida que no da")
g.steps([
    "Recepción manda su video al depósito: baja entero por el 4G y él la ve bien.",
    "El GXV del depósito manda 720P a 2048 kbps por una subida de unos 768 kbps.",
    "En la subida se pierden paquetes: recepción ve negro o la imagen congelada.",
    "VGA a 384 kbps: el video entra por la subida y llega entero.",
], size=17)

B, OK, BAD, GREY, INK, AMB = g.BLUE, g.OK, g.BAD, g.GREY, g.INK, g.AMB
NY = 176
g.add(g.dev(48, NY, 230, 80, "GXV3350", "depósito", icon="camera"))
g.add(g.dev(318, NY, 200, 80, "Router 4G", "subida chica", icon="wifi"))
g.add(g.cloud(556, NY + 6, 150, 68, "internet"))
g.add(g.dev(744, NY, 160, 80, "UCM", "medio", icon="ucm", dark=True))
g.add(g.dev(942, NY, 210, 80, "GXV3480", "recepción", icon="user"))
for x1, x2 in ((278, 318), (518, 556), (706, 744), (904, 942)):
    g.add(g.wire(x1, NY + 40, x2, NY + 40, w=3))
YD, YU = NY + 104, NY + 134   # bajada (recepción → depósito) y subida
XL, XR, XP = 163, 1047, 418
# pantallas
def pantalla(x, y, estado):
    col = {"ok": "#2E6E9E", "negro": "#0B0F14", "cong": "#3A4A5C"}[estado]
    s = g.box(x, y, 200, 112, col, None, rx=10)
    if estado == "ok":
        s += f'<circle cx="{x + 100}" cy="{y + 46}" r="18" fill="#9FC3E3"/><path d="M{x + 64} {y + 102} a36 30 0 0 1 72 0z" fill="#9FC3E3"/>'
    elif estado == "cong":
        s += f'<rect x="{x + 30}" y="{y + 30}" width="80" height="40" fill="#6E88A1"/><rect x="{x + 110}" y="{y + 50}" width="60" height="40" fill="#556677"/>'
        s += g.text(x + 100, y + 104, "congelado", 13, "#D9E9F8", g.MONO, 600, "middle")
    else:
        s += g.text(x + 100, y + 64, "sin imagen", 14, "#9FC3E3", g.MONO, 600, "middle")
    return s
g.add(g.text(48, 380, "Pantalla del depósito", 15, GREY, g.SANS, 600))
g.appear(pantalla(48, 392, "ok"), 3, 100)
g.add(g.text(952, 380, "Pantalla de recepción", 15, GREY, g.SANS, 600))
g.appear(pantalla(952, 392, "ok"), 0, 25, still=0)
g.appear(pantalla(952, 392, "negro"), 25, 52, still=0)
g.appear(pantalla(952, 392, "cong"), 52, 78, still=0)
g.appear(pantalla(952, 392, "ok"), 82, 100)

# 1 · bajada entera
for t0 in (3, 9, 15):
    g.token([(XR, YD), (XL, YD)], t0, t0 + 8, g.chip("video", bg=OK, size=12, h=22))
# 2 y 3 · subida con pérdida
for t0 in (28, 32, 36, 40, 44, 48, 54, 58, 62, 66, 70):
    g.token([(XL, YU), (XP - 12, YU)], t0, t0 + 2.4, g.chip("video", bg=AMB, size=12, h=22), hold=t0 + 2.6)
for t0 in (31, 43, 57, 69):
    g.token([(XP - 12, YU), (XR, YU)], t0, t0 + 6, g.chip("video", bg=AMB, size=12, h=22))
g.appear(g.mark(XP + 30, YU, False, 13), 30, 78, still=0)
g.appear(g.pillc(XP + 30, YU + 18, "se pierde en la subida", BAD, g.BADBG, 13, 26), 30, 78, still=0)
# 4 · con VGA y 384 kbps
for t0 in (82, 87, 92):
    g.token([(XL, YU), (XR, YU)], t0, t0 + 6, g.chip("video", bg=OK, size=12, h=22))
g.fijo_only(f'<g transform="translate(680 {YU})">' + g.chip("video", bg=OK, size=12, h=22) + "</g>"
            + f'<g transform="translate(450 {YD})">' + g.chip("video", bg=OK, size=12, h=22) + "</g>")

# barra de la subida
BX, BY = 300, 404
g.add(g.text(BX, BY, "Subida del 4G: 768 kbps", 15, INK, g.SANS, 600))
g.add(g.box(BX, BY + 12, 600, 30, g.SLATE, rx=8))
g.add(f'<line x1="{BX + 192}" y1="{BY + 6}" x2="{BX + 192}" y2="{BY + 48}" stroke="{INK}" stroke-width="2" stroke-dasharray="5 4"/>')
g.appear(g.box(BX, BY + 12, 600, 30, BAD, rx=8) + g.text(BX + 16, BY + 33, "720P · 2048 kbps", 14, g.WHITE, g.MONO, 600), 25, 78, still=0)
g.appear(g.box(BX, BY + 12, 96, 30, OK, rx=8) + g.text(BX + 110, BY + 33, "VGA · 384 kbps", 14, OK, g.MONO, 600), 80, 100)
g.add(g.text(BX + 198, BY + 66, "lo que entra", 13, GREY, g.MONO))

g.add(g.box(48, 520, 1104, 106, g.WHITE, g.LINE, rx=14))
ROWS = [(0, 25, "El video que va al depósito baja entero", "por eso él ve bien: el problema no es la cámara de recepción", OK),
        (25, 52, "El GXV3350 sale de fábrica con 720P y 2048 kbps", "casi tres veces lo que entra por esa subida", BAD),
        (52, 78, "En la captura de la UCM: un solo flujo de video con pérdida", "se manda y llega roto: es el camino, no el decodificador", BAD),
        (78, 100, "Account > Codec Settings: H.264 Image Size VGA, Video Bit Rate 384 kbps", "lo que recomienda Grandstream cuando 720P es mucho para la red", OK)]
for t0, t1, a, b, col in ROWS:
    g.appear(g.text(72, 560, a, 17, INK, g.SANS, 600) + g.text(72, 596, b, 16, col, g.SANS, 600), t0, t1)

g.done(22, "r1", "El caso en la red: una subida que no da",
       "Animación en cuatro tiempos. De izquierda a derecha: el GXV3350 del depósito, un router 4G con poca subida, internet, la UCM y el GXV3480 de recepción; debajo, las pantallas de los dos lados y una barra con la subida del 4G, 768 kbps de ejemplo. "
       "1: el video de recepción baja entero por el 4G y el depósito la ve bien. "
       "2: el GXV3350 manda de fábrica 720P a 2048 kbps, casi tres veces lo que entra por la subida. "
       "3: en la subida se pierden paquetes: a recepción le llegan pocos, ve negro o la imagen congelada, y en la captura de la UCM aparece un solo flujo de video con pérdida: se manda y llega roto, es el camino. "
       "4: con H.264 Image Size en VGA y Video Bit Rate en 384 kbps, en Account > Codec Settings del GXV del depósito, el video entra por la subida y llega entero; es lo que recomienda Grandstream cuando 720P es mucho para la red.",
       [8, 20, 34, 46, 60, 72, 86, 95])
