#!/usr/bin/env python3
"""Lección 10 · teoría: la llamada a la app pasa por la nube; con el WAN cortado, lo local sigue andando."""
from _anim_akuvox import Anim, A, draw_arrow, token, chip, lane, appear, mark, finish

a = Anim(T=25, kicker="AKUVOX · SMARTPLUS Y PLAN B", title="La app depende de la nube; lo local, no")
a.steps([
    "Aprietan el botón: el portero llama al número SIP de SmartPlus (cuenta 1).",
    "La nube busca los dispositivos del residente y notifica al celular.",
    "La app se despierta, se conecta y la llamada pasa a través de la nube.",
    "Se corta el WAN del edificio: el paso 1 ya falla y la app no suena.",
    "Lo local sigue: la llamada al monitor, el PIN, la tarjeta y el relé.",
], still=4)

XM, XP, XN, XA, XW = 130, 380, 760, 1040, 570
lane(a, XM, 176, 640, "Monitor", "red del edificio", w=196)
lane(a, XP, 176, 640, "Portero", "SIP 1: SmartPlus", w=196)
lane(a, XN, 176, 640, "Nube", "SmartPlus", w=196)
lane(a, XA, 176, 640, "App celular", "del residente", w=196)
a.add(a.text(XW, 262, "WAN", 14, A.GREY, A.MONO, 600, "middle"))
a.add(f'<line x1="{XW}" y1="270" x2="{XW}" y2="640" stroke="{A.LINE}" stroke-width="2"/>')


def msg(x1, x2, y, s, color, t0, t1, hold=100, still=1, tok=None, dashed=False):
    draw_arrow(a, [(x1, y), (x2, y)], t0, t1, color, hold=hold, still=still, dashed=dashed)
    appear(a, a.text((x1 + x2) / 2, y - 11, s, 15, color, A.MONO, 600, "middle"), t1 - 0.5, hold, still=still)
    if tok:
        token(a, [(x1, y), (x2, y)], t0, t1, chip(a, tok, bg=color, size=13, h=24))


# 1 a 3: el camino por la nube (se borra cuando cae el WAN)
msg(XP, XN, 300, "llamada SIP al número del depto", A.BLUE, 3, 10, hold=60, still=0, tok="llamada")
msg(XN, XA, 350, "notificación", A.AMB, 22, 27, hold=60, still=0, tok="aviso")
msg(XA, XN, 400, "la app se conecta", A.BLUE, 42, 46, hold=60, still=0)
appear(a, a.box(XP, 428, XA - XP, 38, "#E4F5FB", None, rx=8)
       + a.text((XP + XA) / 2, 453, "audio y video a través de la nube", 15, A.CYAN, A.MONO, 600, "middle"), 47, 60, still=0)
pk = '<rect x="-13" y="-6" width="26" height="12" rx="4" fill="#17A8D4"/>'
for i in range(3):
    t0 = 47.5 + i * 3.5
    token(a, [(XP + 20, 422), (XA - 20, 422)], t0, t0 + 6, pk, hold=t0 + 6.2)
    token(a, [(XA - 20, 472), (XP + 20, 472)], t0 + 2.5, t0 + 8.5, pk, hold=min(t0 + 8.7, 60))

# 4: cae el WAN
cut = (f'<line x1="{XW}" y1="270" x2="{XW}" y2="640" stroke="{A.BAD}" stroke-width="4" stroke-dasharray="10 7"/>'
       + a.pill(XW, 276, "WAN cortado", A.BAD, A.BADBG, 14, 28, "middle"))
appear(a, cut, 61, 100, still=1)
draw_arrow(a, [(XP, 340), (XW - 14, 340)], 63, 68, A.BLUE, still=1)
appear(a, a.text((XP + XW) / 2 - 10, 329, "llamada a SmartPlus", 15, A.BLUE, A.MONO, 600, "middle"), 63, 100, still=1)
appear(a, mark(a, XW, 340, False, 15), 68.5, 100, still=1)
appear(a, a.text(XA, 340, "no suena", 16, A.BAD, A.SANS, 600, "middle")
       + a.text(XA, 392, "llave temporal nueva:", 15, A.BAD, A.SANS, 600, "middle")
       + a.text(XA, 414, "necesita la nube", 15, A.BAD, A.SANS, 600, "middle"), 69, 100, still=1)

# 5: lo local
msg(XP, XM, 470, "llamada local", A.OK, 82, 86, tok="llamada")
appear(a, a.pill(XM, 496, "atiende y abre", A.OK, A.OKBG, 14, 28, "middle"), 87, 100, still=1)
appear(a, a.box(XP - 110, 540, 220, 76, A.OKBG, A.OK, rx=12, sw=2)
       + a.text(XP, 568, "PIN y tarjeta: valida", 15, A.OK, A.SANS, 600, "middle")
       + a.text(XP, 590, "el portero, y dispara el relé", 15, A.OK, A.SANS, 600, "middle"), 89, 100, still=1)

finish(a, "10-t1.svg", "La app depende de la nube y lo local no",
       "Animación en cinco tiempos con cuatro líneas de vida: monitor, portero, nube SmartPlus y app del celular; entre el portero y la nube pasa el WAN del edificio. "
       "1: el visitante aprieta y el portero, con la cuenta SIP 1 tomada por SmartPlus, llama al número SIP del departamento en la nube. "
       "2: la nube busca los dispositivos del residente y manda una notificación al celular. "
       "3: la app se despierta, se conecta a la nube y el audio y el video viajan a través de ella. "
       "4: se corta el WAN; la llamada a SmartPlus falla en el primer paso, la app no suena y tampoco se pueden generar llaves temporales nuevas. "
       "5: lo local sigue andando: el portero llama al monitor dentro del edificio, el residente atiende y abre, y el PIN y la tarjeta se validan en el propio portero, que dispara el relé.",
       [8, 28, 52, 75, 95])
