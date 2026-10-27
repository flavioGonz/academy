#!/usr/bin/env python3
"""Teoría lección 7 (La VLAN no aísla): la Gateway ACL evalúa de arriba hacia abajo y la primera que coincide decide.
Salida: site2/ilustraciones/omada/7-t1.svg"""
import sys
sys.path.insert(0, "/home/claude/ies-training/ilustraciones/omada/src")
from _anim_omada import *  # noqa

a = nueva(24, "GATEWAY ACL", "La primera regla que coincide decide")
F = a.steps([
    "Un paquete de Invitados a 192.168.88.1 llega al gateway. Se lee la regla 1.",
    "Coincide con la deny: se descarta. La regla 2 ni se mira.",
    "Un paquete a 1.1.1.1 no coincide con la 1: sigue a la 2 y sale a internet.",
    "Orden al revés: el permit general atrapa primero y la deny nunca actúa.",
], still=1)

# origen
a.add(nodo(a, 48, 340, 250, 72, "Notebook", "Invitados · 10.10.30.x", dark=False, tsize=19))
# panel de reglas
PX, PY, PW, PH = 380, 186, 460, 250
a.add(a.box(PX, PY, PW, PH, a.WHITE, a.LINE))
a.add(a.text(PX + 22, PY + 34, "Gateway ACL", 19, a.INK, a.HEAD, 600) + a.text(PX + PW - 22, PY + 34, "de arriba hacia abajo", 15, a.GREY, a.MONO, 400, "end"))
R1, R2, RH = PY + 56, PY + 124, 56


def fila(y, n, pol, txt):
    fg, bg = (a.BAD, a.BADBG) if pol == "Deny" else (a.OK, a.OKBG)
    return (a.box(PX + 16, y, PW - 32, RH, a.SLATE, None, rx=12)
            + f'<circle cx="{PX + 44}" cy="{y + RH / 2}" r="15" fill="{a.WHITE}"/>' + a.text(PX + 44, y + RH / 2 + 6, str(n), 15, a.INK, a.MONO, 600, "middle")
            + chip(a, PX + 70, y + 13, pol, fg, bg, stroke=fg)
            + a.text(PX + 70 + chipw(pol) + 14, y + RH / 2 + 6, txt, 16, a.INK, a.SANS, 600))


a.add(fila(R1, 1, "Deny", "Invitados → Redes-Internas"))
a.add(fila(R2, 2, "Permit", "general"))
# lista al revés (fase 4), tapa la normal
fase(a, fila(R1, 1, "Permit", "general") + fila(R2, 2, "Deny", "Invitados → Redes-Internas"), F, 3)
a.add(a.text(PX + 22, PY + PH - 24, "Redes-Internas: 192.168.88.0/24 · 10.10.20.0/24", 15, a.TXT, a.MONO))

# destinos
DX, DW = 900, 252
a.add(nodo(a, DX, 186, DW, 72, "Oficina · VLAN 1", "192.168.88.0/24", dark=False, tsize=19))
a.add(nodo(a, DX, 380, DW, 72, "Internet", "1.1.1.1", dark=False, tsize=19))

(a0, a1), (b0, b1), (c0, c1), (d0, d1) = F
WX = 300  # donde espera el paquete, a la izquierda del panel
pA = paquete(a, "192.168.88.1", a.CYAN)
pB = paquete(a, "1.1.1.1", a.CYAN)
yr1, yr2 = R1 + RH / 2, R2 + RH / 2

# fase 1 y 2: paquete a la oficina
viaje(a, pA, 173, 334, WX, yr1, a0 + 2, a0 + 9, hold=b1 - a0 - 10)
en(a, a.box(PX + 10, R1 - 6, PW - 20, RH + 12, "none", a.AMB, rx=14, sw=3, extra='stroke-dasharray="7 5"'), a0 + 10, a1)
en(a, a.box(PX + 10, R1 - 6, PW - 20, RH + 12, "none", a.BAD, rx=14, sw=3) + bad(a, WX + 76, yr1 - 26, 13), b0, b1, still=1)
en(a, a.box(PX + 16, R2, PW - 32, RH, a.WHITE, None, rx=12, extra='fill-opacity=".7"') + a.text(PX + PW - 30, R2 + RH / 2 + 6, "no se mira", 15, a.GREY, a.MONO, 400, "end"), b0 + 2, b1, still=1)
en(a, chip(a, DX + DW, 268, "no llega", a.OK, a.OKBG, anchor="end", stroke=a.OK), b0 + 3, b1, still=1)
solo_fijo(a, f'<g transform="translate({WX} {yr1})">{pA}</g>')

# fase 3: paquete a internet
viaje(a, pB, 173, 334, WX, yr1, c0 + 1, c0 + 5, hold=3)
en(a, a.box(PX + 10, R1 - 6, PW - 20, RH + 12, "none", a.GREY, rx=14, sw=2.5, extra='stroke-dasharray="7 5"') + a.text(WX, yr1 - 26, "no coincide", 15, a.GREY, a.MONO, 600, "middle"), c0 + 5, c1)
viaje(a, pB, WX, yr1, WX, yr2, c0 + 8, c0 + 10, hold=3)
en(a, a.box(PX + 10, R2 - 6, PW - 20, RH + 12, "none", a.OK, rx=14, sw=3), c0 + 10, c1)
DOT = '<circle r="9" fill="#17A8D4"/>'
viaje(a, DOT, PX + PW + 6, yr2, DX - 14, 416, c0 + 14, c0 + 19, hold=c1 - c0 - 20)
en(a, ok(a, DX + DW - 28, 416, 13), c0 + 19, c1)

# fase 4: orden al revés
viaje(a, pA, 173, 334, WX, yr1, d0 + 1, d0 + 6, hold=4)
en(a, a.box(PX + 10, R1 - 6, PW - 20, RH + 12, "none", a.OK, rx=14, sw=3), d0 + 7, d1)
viaje(a, DOT, PX + PW + 6, yr1, DX - 14, 222, d0 + 11, d0 + 16, hold=d1 - d0 - 17)
en(a, a.box(DX - 4, 182, DW + 8, 80, "none", a.BAD, rx=16, sw=3) + chip(a, DX + DW, 268, "llega: mal", a.BAD, a.BADBG, anchor="end", stroke=a.BAD), d0 + 16, d1)

# prueba de verificación
VY = 486
a.add(a.box(48, VY, 1104, 104, a.WHITE, a.LINE))
a.add(a.text(72, VY + 32, "Verificación desde un cliente invitado", 17, a.INK, a.HEAD, 600))
for i, (cmd, res, good) in enumerate([("ping 10.10.30.1", "responde", True), ("ping 192.168.88.1", "no responde", True), ("ping 1.1.1.1", "responde", True)]):
    x = 72 + i * 360
    a.add(a.box(x, VY + 48, 196, 36, a.INK, rx=8) + a.text(x + 14, VY + 72, cmd, 15, "#D9E9F8", a.MONO))
    a.add(a.text(x + 210, VY + 72, res, 16, a.OK, a.SANS, 600))
fase(a, a.box(48, VY, 1104, 104, a.BADBG, a.BAD, rx=14, sw=2)
     + a.text(72, VY + 40, "Si el ping a 192.168.88.1 responde, casi siempre es el orden:", 17, a.BAD, a.SANS, 600)
     + a.text(72, VY + 72, "la deny tiene que quedar arriba de cualquier permit general.", 17, a.BAD, a.SANS, 600), F, 3)

pie(a, F, [
    "Sin ACL, el gateway rutea entre VLAN y las redes se ven.",
    "Un IP Group corta Invitados hacia todas las redes internas con una sola regla.",
    "Ninguna regla de corte coincide: el paquete sigue su camino.",
    "",
], y=640, still=1)

salida(a, 7, 1, "La primera regla que coincide decide",
       "Animación en cuatro tiempos de una Gateway ACL con dos reglas: 1 Deny de Invitados a Redes-Internas (192.168.88.0/24 y "
       "10.10.20.0/24) y 2 Permit general. 1: un paquete de una notebook invitada (10.10.30.x) a 192.168.88.1 llega al gateway y se "
       "compara con la regla 1. 2: coincide con la deny, se descarta, la regla 2 ni se mira y no llega a la oficina. 3: un paquete a "
       "1.1.1.1 no coincide con la regla 1, pasa a la 2, permit, y sale a internet. 4: con el orden al revés, el permit general atrapa "
       "primero al paquete a 192.168.88.1, que llega a la oficina, y la deny nunca actúa. Abajo, la verificación: ping al propio gateway "
       "responde, a 192.168.88.1 no responde y a 1.1.1.1 responde.",
       [14, 40, 66, 90])
