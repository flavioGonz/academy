#!/usr/bin/env python3
"""Lección 5 · Resumen, "Cómo se ve en la red": la ruta internacional con PIN. La teoría muestra la llamada que se
frena en el privilegio; acá la extensión tiene el nivel y la central igual pide el PIN antes de cursarla.
Fuentes: la lección (privilegio igual o mayor; Password Settings con PIN Groups; al marcar un internacional la
central pide el PIN antes de cursar la llamada), manual UCM630x (PIN de al menos cuatro dígitos)."""
from _anim_gs_red import R

g = R(T=26, fix=70, kicker="GRANDSTREAM · PATRÓN Y PRIVILEGIO · CÓMO SE VE EN LA RED",
      title="La ruta internacional pide el PIN antes de salir")
g.steps([
    "La 1001, con privilegio International, marca 00 54 11…: coincide con _00X. y el nivel alcanza.",
    "Antes de cursarla, la central le pide el PIN por el audio de la llamada.",
    "La 1001 marca su PIN, que está en el PIN Group: recién ahí sale el INVITE al proveedor.",
    "Con un PIN que no está en el grupo, la central corta: al proveedor no llega nada.",
])

XA, XU, XP = 140, 450, 760
g.lane(XA, 176, 560, "1001", "International", w=200)
g.lane(XU, 176, 560, "UCM", "ruta internacional", w=220)
g.lane(XP, 176, 560, "Proveedor_Lab", "troncal", w=220)
g.msg(XA, XU, 262, "INVITE 005411…", g.BLUE, 3, 9, hold=75, tok="INVITE")
g.msg(XU, XA, 318, "«ingresá el PIN» (audio)", g.CYAN, 27, 33, hold=75, dashed=True)
g.msg(XA, XU, 374, "PIN · teclas RFC 4733", g.BLUE, 52, 57, hold=75, tok="PIN")
g.appear(g.mark(XU + 30, 404, True, 13) + g.text(XU + 52, 410, "en el PIN Group", 15, g.OK, g.MONO, 600), 58, 75)
g.msg(XU, XP, 450, "INVITE 005411…", g.OK, 62, 68, hold=75, tok="INVITE")
g.appear(g.pillc(XP, 478, "sale la llamada", g.OK, g.OKBG, 13, 26), 68, 75)
# 4 · PIN equivocado
g.msg(XA, XU, 262, "INVITE 005411…", g.BLUE, 77, 80)
g.msg(XU, XA, 318, "«ingresá el PIN» (audio)", g.CYAN, 80.5, 83, dashed=True)
g.msg(XA, XU, 374, "PIN que no está en el grupo", g.BAD, 84, 87)
g.msg(XU, XA, 430, "la central corta", g.BAD, 89, 92)
g.appear(g.mark(XP, 450, False, 15) + g.text(XP, 488, "no llega nada", 15, g.BAD, g.MONO, 600, "middle"), 92, 100)

PX, PW = 900, 252
g.add(g.box(PX, 186, PW, 236, g.WHITE, g.LINE, rx=14))
g.add(g.text(PX + 18, 216, "Outbound Route", 15, g.GREY, g.MONO))
for k, (n, v) in enumerate([("nombre", "internacional"), ("patrón", "_00X."), ("privilegio", "International"), ("contraseña", "PIN Groups")]):
    y = 248 + k * 44
    g.add(g.text(PX + 18, y, n, 14, g.GREY, g.MONO) + g.text(PX + 18, y + 20, v, 16, g.INK, g.MONO, 600))
g.appear(g.box(PX + 8, 278, PW - 16, 82, "none", g.BLUE, rx=8, sw=2.5), 4, 25)
g.appear(g.box(PX + 8, 366, PW - 16, 42, "none", g.CYAN, rx=8, sw=2.5), 25, 75)
g.appear(g.box(PX + 8, 366, PW - 16, 42, "none", g.BAD, rx=8, sw=2.5), 75, 100)
g.add(g.note(PX, 440, PW, None, ["El privilegio frena a la", "extensión equivocada; el PIN,", "a la correcta en otras manos."], "info", size=15, lh=21))

g.status(612, [
    (0, 25, "Patrón y nivel: la llamada todavía no salió de la central.", g.INK),
    (25, 50, "El PIN es algo que sabe la persona y la extensión no guarda.", g.INK),
    (50, 75, "Solo con el PIN correcto el número viaja al proveedor.", g.OK),
    (75, 100, "Una extensión robada con International igual se frena acá.", g.BAD),
])

g.done(5, "r1", "La ruta internacional pide el PIN antes de salir",
       "Animación en cuatro tiempos con tres líneas de vida: la interna 1001 con privilegio International, la UCM con la ruta internacional y el troncal Proveedor_Lab; a la derecha, la ruta: nombre internacional, patrón _00X., privilegio International y contraseña por PIN Groups. "
       "1: la 1001 marca 00 54 11 y el resto del número; coincide con _00X. y su nivel alcanza. "
       "2: antes de cursarla, la central le pide el PIN por el audio de la llamada. "
       "3: la 1001 marca su PIN, que viaja como teclas RFC 4733; está en el PIN Group y recién ahí sale el INVITE al proveedor. "
       "4: con un PIN que no está en el grupo la central corta la llamada y al proveedor no llega nada. "
       "Nota: el privilegio frena a la extensión equivocada; el PIN, a la correcta usada por otra persona.",
       [8, 36, 66, 96])
