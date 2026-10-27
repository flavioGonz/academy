#!/usr/bin/env python3
"""Lección 5 · teoría: REGISTER con desafío digest y la central que rutea la llamada a la 202."""
from _anim_akuvox import Anim, A, draw_arrow, token, chip, lane, note, appear, finish

a = Anim(T=25, kicker="AKUVOX · CUENTA SIP", title="Registrarse y después llamar por la central")
a.steps([
    "El portero manda REGISTER: «la 201 está en mi IP y puerto».",
    "La central contesta 401 Unauthorized con un desafío.",
    "El portero repite con un resumen de su clave (digest): 200 OK.",
    "Llaman: el portero manda el INVITE para la 202 a la central.",
    "La central busca dónde está registrada la 202 y la hace sonar.",
], still=4)

XP, XC, XM = 150, 470, 790
lane(a, XP, 176, 640, "Portero", "ext. 201")
lane(a, XC, 176, 640, "Central", "192.168.88.10:5060")
lane(a, XM, 176, 640, "Monitor", "ext. 202")


def msg(x1, x2, y, s, color, t0, t1, dashed=False, tok=None):
    draw_arrow(a, [(x1, y), (x2, y)], t0, t1, color, dashed=dashed)
    appear(a, a.text((x1 + x2) / 2, y - 12, s, 16, color, A.MONO, 600, "middle"), t1 - 0.5, 100, still=1)
    if tok:
        token(a, [(x1, y), (x2, y)], t0, t1, chip(a, tok, bg=color))


msg(XP, XC, 278, "REGISTER 201", A.BLUE, 3, 9, tok="REGISTER")
msg(XC, XP, 330, "401 · desafío", A.GREY, 22, 27, dashed=True)
msg(XP, XC, 382, "REGISTER + digest", A.BLUE, 41, 46, tok="digest")
msg(XC, XP, 434, "200 OK", A.OK, 50, 55)
msg(XP, XC, 504, "INVITE 202", A.BLUE, 62, 68, tok="INVITE")
msg(XC, XM, 556, "INVITE", A.BLUE, 84, 90, tok="INVITE")
appear(a, a.pill(XM, 580, "suena la 202", A.OK, A.OKBG, 15, 30, "middle"), 91, 100, still=1)
# separador registro / llamada
a.add(f'<line x1="40" y1="466" x2="900" y2="466" stroke="{A.LINE}" stroke-width="2"/>')
a.add(a.text(40, 458, "REGISTRO", 13, A.GREY, A.MONO, 600, extra='letter-spacing="2"'))
a.add(a.text(40, 486, "LLAMADA", 13, A.GREY, A.MONO, 600, extra='letter-spacing="2"'))

# tabla de registros de la central
TX, TY, TW = 922, 186, 230
a.add(a.box(TX, TY, TW, 230, A.WHITE, A.LINE, rx=14))
a.add(a.text(TX + 18, TY + 32, "Registros", 19, A.INK, A.HEAD, 600))
a.add(a.text(TX + 18, TY + 54, "en la central", 15, A.GREY, A.MONO))


def row(y, ext, sub, hl=None):
    s = a.box(TX + 12, y, TW - 24, 62, A.SLATE, None, rx=10)
    s += a.text(TX + 28, y + 27, ext, 18, A.INK, A.MONO, 600)
    s += a.text(TX + 28, y + 50, sub, 14, A.TXT, A.MONO)
    return s


a.add(row(TY + 74, "202", "IP:puerto monitor"))
appear(a, row(TY + 146, "201", "IP:puerto portero"), 55, 100, still=1)
appear(a, a.box(TX + 12, TY + 146, TW - 24, 62, "none", A.OK, rx=10, sw=3), 55, 62, still=0)
appear(a, a.box(TX + 12, TY + 74, TW - 24, 62, "none", A.AMB, rx=10, sw=3)
       + a.text(TX + TW - 22, TY + 98, "¿dónde?", 14, A.AMB, A.MONO, 600, "end"), 80, 92, still=0)

s, _ = note(a, TX, 440, TW, None, ["El registro vence y", "se renueva solo cada", "período de registro."], "info", size=15, lh=21)
a.add(s)
s, _ = note(a, TX, 548, TW, None, ["Marcá 202 a secas: con", "un prefijo de más, la", "central no halla destino."], "amb", size=15, lh=21)
a.add(s)

finish(a, "5-t1.svg", "Registro SIP y llamada por la central",
       "Animación en cinco tiempos con tres líneas de vida: portero extensión 201, central 192.168.88.10 puerto 5060 y monitor extensión 202. "
       "1: el portero manda REGISTER diciendo que la 201 está en su IP y puerto. 2: la central contesta 401 Unauthorized con un desafío. "
       "3: el portero repite el REGISTER con un resumen digest calculado con su clave y la central responde 200 OK; la tabla de registros suma la 201. "
       "4: al apretar el botón, el portero manda el INVITE para la 202 a la central. 5: la central busca en su tabla dónde está registrada la 202 y le manda el INVITE al monitor, que suena. "
       "Notas: el registro vence y se renueva cada período de registro; con un prefijo de más la central no encuentra destino.",
       [8, 28, 57, 72, 93])
