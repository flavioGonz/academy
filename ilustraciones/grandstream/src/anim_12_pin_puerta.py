#!/usr/bin/env python3
"""Lección 12 · teoría: timbre al grupo, PIN por DTMF que el GDS compara, y OpenDoor por mensaje SIP."""
from _anim_grandstream import G

g = G(T=28, fix=50, kicker="GRANDSTREAM · PORTERO", title="El portero compara el PIN y recién ahí abre")
g.steps([
    "Tocan el timbre: el GDS3710 llama al 6000 y la UCM hace sonar a todo el grupo.",
    "Atiende recepción y marca 4829#: cada tecla viaja como evento RFC 4733.",
    "El GDS compara con su Remote PIN: coincide y activa la salida en Open Door.",
    "Con un PIN equivocado no coincide: la salida no se mueve.",
    "Sin atender: la tecla OpenDoor del GRP manda un mensaje SIP con el PIN, y abre.",
])

# teléfonos y central
g.add(g.node(48, 196, 230, 76, "GRP recepción", "miembro del 6000"))
g.add(g.node(48, 300, 230, 76, "GRP seguridad", "miembro del 6000"))
g.add(g.node(400, 236, 200, 100, "UCM", "grupo 6000", dark=True, tsize=22))
g.add(f'<path d="M278 234 H340 V270 H400 M278 338 H340 V300 H400 M600 286 H700" fill="none" stroke="{g.LINE}" stroke-width="3"/>')
R1 = [(278, 234), (340, 234), (340, 270), (400, 270)]
R2 = [(278, 338), (340, 338), (340, 300), (400, 300)]
U2G = [(600, 286), (700, 286)]

# GDS
GX, GY, GW = 700, 186, 452
g.add(g.box(GX, GY, GW, 300, g.WHITE, g.LINE, rx=16))
g.add(g.text(GX + 22, GY + 34, "GDS3710 · extensión 8001", 18, g.INK, g.HEAD, 600))
g.add(g.text(GX + 22, GY + 62, "Remote PIN to Open the Door: 4829", 15, g.GREY, g.MONO))
SX = [GX + 22 + i * 58 for i in range(5)]
SY = GY + 84
for x in SX:
    g.add(g.box(x, SY, 50, 56, g.SLATE, None, rx=8))
g.add(g.text(GX + 330, SY + 36, "lo que llega", 14, g.GREY, g.MONO))


def slots(chars, t0s, t1, col):
    for x, c, t in zip(SX, chars, t0s):
        g.appear(g.text(x + 25, SY + 38, c, 24, col, g.MONO, 600, "middle"), t, t1)


CY = GY + 184
g.add(g.text(GX + 22, CY, "Compara", 16, g.GREY, g.SANS, 600))
g.appear(g.text(GX + 120, CY, "4829 = 4829 · coincide", 17, g.OK, g.MONO, 600), 41, 60)
g.appear(g.text(GX + 120, CY, "1234 ≠ 4829 · no abre", 17, g.BAD, g.MONO, 600), 73, 80)
g.appear(g.text(GX + 120, CY, "MESSAGE con el PIN · coincide", 17, g.OK, g.MONO, 600), 89, 100)
OY = GY + 236
g.add(g.text(GX + 22, OY + 18, "Salida Open Door", 16, g.GREY, g.SANS, 600))
g.appear(g.pillc(GX + 300, OY, "reposo", g.GREY, g.SLATE), 0, 43)
g.appear(g.pillc(GX + 300, OY, "activa", g.OK, g.OKBG), 43, 60)
g.appear(g.pillc(GX + 300, OY, "reposo", g.GREY, g.SLATE), 60, 90)
g.appear(g.pillc(GX + 300, OY, "activa", g.OK, g.OKBG), 90, 100)

# cerradura
LY = 512
g.add(g.box(GX, LY, GW, 76, g.WHITE, g.LINE, rx=14))
g.add(f'<line x1="{GX + GW / 2}" y1="{GY + 300}" x2="{GX + GW / 2}" y2="{LY}" stroke="{g.CYAN}" stroke-width="3"/>')
g.add(g.text(GX + 22, LY + 46, "Cerradura", 18, g.INK, g.HEAD, 600))
for a, b, txt, fg, bg in [(0, 45, "trabada", g.INK, g.SLATE), (45, 60, "liberada", g.OK, g.OKBG), (60, 91, "trabada", g.INK, g.SLATE), (91, 100, "liberada", g.OK, g.OKBG)]:
    g.appear(g.pillc(GX + 300, LY + 24, txt, fg, bg, 16, 32), a, b)

# 1: timbre
g.token(list(reversed(U2G)), 2, 6, g.chip("INVITE a 6000", bg=g.BLUE, size=13, h=24))
g.token(list(reversed(R1)), 7, 11, g.chip("suena", bg=g.BLUE, size=13, h=24))
g.token(list(reversed(R2)), 7, 11, g.chip("suena", bg=g.BLUE, size=13, h=24))
g.appear(g.pillc(163, 164, "atiende", g.OK, g.OKBG, 13, 24), 15, 40)
# 2: dígitos 4829#
for k, c in enumerate("4829#"):
    t = 21 + k * 3.6
    g.token(R1, t, t + 1.6, g.chip(c, bg=g.AMB, size=14, h=26), hold=t + 1.7)
    g.token(U2G, t + 1.8, t + 3.2, g.chip(c, bg=g.AMB, size=14, h=26), hold=t + 3.3)
slots("4829#", [21 + k * 3.6 + 3.2 for k in range(5)], 60, g.INK)
# 4: PIN equivocado
for k, c in enumerate("1234#"):
    t = 61 + k * 2.2
    g.token(U2G, t, t + 1.5, g.chip(c, bg=g.BAD, size=14, h=26), hold=t + 1.6)
slots("1234#", [61 + k * 2.2 + 1.5 for k in range(5)], 80, g.BAD)
# 5: OpenDoor
g.token(R1, 81, 84.5, g.chip("MESSAGE", bg=g.CYAN, size=13, h=24), hold=84.6)
g.token(U2G, 84.8, 88, g.chip("MESSAGE", bg=g.CYAN, size=13, h=24), hold=88.2)
g.appear(g.box(SX[0], SY, 5 * 58 - 8, 56, g.WHITE, g.CYAN, rx=8, sw=2) + g.text(SX[0] + 141, SY + 34, "sin teclas: PIN en el mensaje", 15, g.TXT, g.SANS, 600, "middle"), 86, 100)
g.appear(g.pillc(163, 164, "tecla OpenDoor", g.CYAN, g.WHITE, 13, 24), 80, 100)

g.add(g.note(48, 420, 610, None, ["En el GRP, el servicio GDS guarda el número del", "portero (8001) y el mismo PIN para OpenDoor."], "info"))
g.add(g.note(48, 528, 610, None, ["Probalo con la puerta abierta o con alguien del lado", "de adentro: un relé mal configurado traba o deja abierto."], "amb"))

g.finish(12, 1, "El portero compara el PIN y recién ahí abre",
         "Animación en cinco tiempos con dos teléfonos GRP del grupo 6000 (recepción y seguridad), la UCM, el portero GDS3710 registrado como extensión 8001 y la cerradura conectada a su salida. "
         "1: tocan el timbre; el GDS3710 manda un INVITE al 6000 y la UCM hace sonar a los dos teléfonos del grupo; atiende recepción. "
         "2: recepción marca 4829# y cada tecla viaja como evento RFC 4733 hasta el portero. "
         "3: el GDS compara con su Remote PIN, 4829; coincide, activa la salida configurada en Open Door y la cerradura se libera. "
         "4: con un PIN equivocado, 1234#, no coincide: la salida queda en reposo y la cerradura trabada. "
         "5: sin atender, la tecla OpenDoor del GRP manda un mensaje SIP (MESSAGE) con el PIN; el portero lo compara, coincide y abre. "
         "Notas: en el GRP, el servicio GDS guarda el número del portero, 8001, y el mismo PIN para OpenDoor; conviene probar con la puerta abierta o con alguien del lado de adentro.",
         [8, 33, 50, 74, 94])
