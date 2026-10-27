#!/usr/bin/env python3
"""Teoría lección 10 (Portal cautivo): qué deja pasar el EAP según el estado de cada cliente, las excepciones
y qué pasa sin controlador.
Salida: site2/ilustraciones/omada/10-t1.svg"""
import sys
sys.path.insert(0, "/home/claude/ies-training/ilustraciones/omada/src")
from _anim_omada import *  # noqa

a = nueva(30, "PORTAL CAUTIVO", "El EAP retiene hasta que el controlador valida")
F = a.steps([
    "Un cliente nuevo pide una web: no está autenticado, el EAP lo retiene y lo manda al portal.",
    "Ingresa el voucher. El controlador lo valida y habilita a ese cliente: navega.",
    "Pre-Authentication Access: la web del negocio pasa antes de autenticar.",
    "Authentication-Free Client: un equipo exceptuado por MAC o IP navega sin portal.",
    "Controlador apagado: nadie valida, y los clientes nuevos no entran.",
], still=1, size=17)
P = F

# clientes
CL = [("Huésped A", "Huespedes-Lab"), ("Huésped B", "Huespedes-Lab"), ("Equipo de prueba", "por MAC")]
RY = [214, 326, 438]
RH = 80
for (t, s), y in zip(CL, RY):
    a.add(nodo(a, 48, y, 220, RH, t, s, dark=False, tsize=18))
# EAP con la tabla de estado
EX, EW = 400, 340
a.add(a.box(EX, 172, EW, 360, a.INK, rx=16))
a.add(a.text(EX + 20, 200, "EAP · estado de cada cliente", 15, DARK_SUB, a.MONO))
for y in RY:
    a.add(a.box(EX + 14, y, EW - 28, RH, a.NAVY2, None, rx=12))
for y, t in zip(RY, ["A", "B", "Equipo de prueba"]):
    a.add(a.text(EX + 30, y + 30, t, 17, a.WHITE, a.HEAD, 600))


def estado(y, label, fg, bg):
    return chip(a, EX + 30, y + 40, label, fg, bg, stroke=fg)


# estado de A
en(a, estado(RY[0], "no autenticado", a.AMB, a.AMBBG), 0, P[1][0] + 10, still=0)
en(a, estado(RY[0], "autenticado", a.OK, a.OKBG), P[1][0] + 10, 100, still=1)
# estado de B
a.add(estado(RY[1], "no autenticado", a.AMB, a.AMBBG))
# equipo exceptuado
a.add(estado(RY[2], "Authentication-Free", "#5BE0A5", a.NAVY2))

# controlador e internet
CX, CW = 900, 252
a.add(nodo(a, CX, 196, CW, 96, "Controlador", "portal :8088 / :8843"))
a.add(nodo(a, CX, 430, CW, 80, "Internet", dark=False))
caido = a.box(CX - 4, 192, CW + 8, 104, "none", a.BAD, rx=18, sw=3) + chip(a, CX + CW - 12, 206, "apagado", a.BAD, a.BADBG, anchor="end")
fase(a, caido, F, 4)

L1, L2, R1, R2 = 272, EX - 6, EX + EW + 6, CX - 8  # bordes de los tramos
cy = [y + RH / 2 for y in RY]


def ida(label, y, t0, dur=3, color=None, hold=1.0):
    viaje(a, paquete(a, label, color or a.CYAN), L1 + 60, y, L2 - 60, y, t0, t0 + dur, hold=hold)


def sale(label, y0, y1, t0, dur=3, color=None, hold=1.0):
    viaje(a, paquete(a, label, color or a.CYAN), R1 + 60, y0, R2 - 60, y1, t0, t0 + dur, hold=hold)


s = [f[0] for f in F]
# 1: A pide una web, queda retenido y vuelve al portal
ida("web", cy[0], s[0] + 1, 3, hold=3)
en(a, bad(a, L2 - 14, cy[0] - 44, 12) + a.text(L2 - 32, cy[0] - 38, "retenido", 15, a.AMB, a.MONO, 600, "end"), s[0] + 4, s[0] + 12)
viaje(a, paquete(a, "portal", a.BLUE), L2 - 60, cy[0], L1 + 60, cy[0], s[0] + 9, s[0] + 12, hold=6)
# 2: voucher al controlador, validación, navega
ida("voucher", cy[0], s[1] + 1, 2.5, a.BLUE, hold=0.2)
sale("voucher", cy[0], 244, s[1] + 4, 2.5, a.BLUE, hold=1)
en(a, ok(a, CX + CW - 26, 270, 13), s[1] + 7, s[1] + 20, still=1)
ida("web", cy[0], s[1] + 11, 2.5, hold=0.2)
sale("web", cy[0], 470, s[1] + 14, 3, hold=1.5)
solo_fijo(a, f'<g transform="translate(816 362)">{paquete(a, "web", a.CYAN)}</g>')
# 3: B, la web del negocio pasa
ida("web del negocio", cy[1], s[2] + 1, 3, hold=0.3)
en(a, a.text(EX + EW - 24, cy[1] - 14, "Pre-Auth Access", 15, "#5BE0A5", a.MONO, 600, "end"), s[2] + 3, s[3])
sale("negocio", cy[1], 470, s[2] + 5, 3.5, hold=2)
ida("otra web", cy[1], s[2] + 11, 3, hold=3)
en(a, bad(a, L2 - 14, cy[1] - 44, 12) + a.text(L2 - 32, cy[1] - 38, "retenido", 15, a.AMB, a.MONO, 600, "end"), s[2] + 14, s[3])
# 4: equipo exceptuado
ida("web", cy[2], s[3] + 1, 3, hold=0.3)
sale("web", cy[2], 470, s[3] + 5, 3.5, hold=4)
# 5: controlador apagado, el voucher de B no se valida
ida("voucher", cy[1], s[4] + 1, 2.5, a.BLUE, hold=0.2)
sale("voucher", cy[1], 244, s[4] + 4, 3, a.BLUE, hold=6)
en(a, bad(a, R2 - 14, 214, 13), s[4] + 7, 100)
en(a, a.text(EX + EW - 24, cy[1] - 14, "sigue sin entrar", 15, "#FFB4A3", a.MONO, 600, "end"), s[4] + 8, 100)

pie(a, F, [
    "El EAP retiene el tráfico; la página la sirve el controlador.",
    "Navega hasta que vence el código o el tiempo de autenticación.",
    "Las excepciones se configuran en Access Control del portal.",
    "Sirve para los equipos que tienen que navegar sin pasar por el portal.",
    "Sin controlador no hay validación. En Omada Central, una licencia vencida apaga el portal.",
], y=640, still=1, colores=[a.INK, a.OK, a.INK, a.INK, a.BAD], size=16)

salida(a, 10, 1, "El EAP retiene hasta que el controlador valida",
       "Animación en cinco tiempos con tres clientes del SSID Huespedes-Lab, el EAP con el estado de cada cliente, el controlador que sirve "
       "el portal por 8088 o 8843 e internet. 1: el huésped A pide una web, no está autenticado, el EAP lo retiene y lo manda al portal. "
       "2: A ingresa el voucher, el controlador lo valida, A pasa a autenticado y navega hasta que vence el código. 3: el huésped B, sin "
       "autenticar, llega a la web del negocio porque está en Pre-Authentication Access, pero cualquier otra web queda retenida. 4: el "
       "equipo de prueba, exceptuado por MAC en Authentication-Free Client, navega sin portal. 5: con el controlador apagado el voucher de "
       "B no se valida y B sigue sin entrar.",
       [12, 33, 52, 72, 92])
