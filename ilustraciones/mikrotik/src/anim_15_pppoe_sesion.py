#!/usr/bin/env python3
"""Lección 15 · PPPoE con Antel. Teoría "Cómo funciona": descubrimiento (PADI, PADO, PADR, PADS) y después PPP
(LCP, autenticación, IPCP). La IP queda en pppoe-antel, no en ether1.
"""
from _anim_mikrotik_14_26 import Anim, node, lifeline, msg, out

a = Anim(T=26, kicker="MIKROTIK · PPPOE", title="PPPoE: primero se busca al concentrador, después PPP")
a.steps([
    "PADI por broadcast. El concentrador contesta PADO con su ac-name.",
    "PADR y PADS: queda una sesión con su número.",
    "Dentro de la sesión, PPP: LCP negocia el enlace.",
    "Usuario y contraseña. Después IPCP asigna la IP.",
    "La IP queda en pppoe-antel, no en ether1.",
], still=4)

CX, SX = 170, 640
a.add(node(a, 48, 176, 244, 66, "MikroTik", "cliente PPPoE · ether1"))
a.add(node(a, 518, 176, 244, 66, "Concentrador", "del proveedor"))
a.add(lifeline(a, CX, 242, 656))
a.add(lifeline(a, SX, 242, 656))

# franjas de fase
a.add(a.box(200, 252, 410, 226, a.CYAN, rx=12, extra='fill-opacity=".07"'))
a.add(a.text(208, 272, "DESCUBRIMIENTO PPPoE", 15, a.CYAN, a.MONO, 600))
a.add(a.box(200, 488, 410, 170, a.OK, rx=12, extra='fill-opacity=".07"'))
a.add(a.text(208, 508, "PPP DENTRO DE LA SESIÓN", 15, a.OK, a.MONO, 600))

msg(a, CX, SX, 302, "PADI", 2, sub="broadcast: ¿hay un concentrador?")
msg(a, SX, CX, 366, "PADO", 9, sub="ac-name: lo que ves en scan")
msg(a, CX, SX, 422, "PADR", 22)
msg(a, SX, CX, 464, "PADS · sesión n.º", 29)
msg(a, CX, SX, 540, "LCP  ⇄  enlace", 42, color=a.OK)
msg(a, CX, SX, 588, "usuario y contraseña", 62, color=a.OK)
msg(a, SX, CX, 636, "IPCP: tu IP", 70, color=a.OK)

# panel de interfaces
PX, PY, PW = 812, 176, 340
a.add(a.box(PX, PY, PW, 472, a.WHITE, a.LINE, rx=18))
a.add(a.text(PX + 24, PY + 38, "Interfaces del MikroTik", 20, a.INK, a.HEAD, 600))

# pppoe-antel (lógica), aparece con la sesión
yP = PY + 70
a.add(a.group(a.box(PX + 18, yP, PW - 36, 150, a.OKBG, a.OK, rx=12, sw=2)
              + a.text(PX + 34, yP + 32, "pppoe-antel", 19, a.INK, a.MONO, 600)
              + a.text(PX + 34, yP + 56, "interfaz lógica", 15, a.TXT),
              a.show(30, 100), still=1))
a.add(a.group(a.pill(PX + 34, yP + 74, "IP de IPCP", a.OK, a.WHITE, 15)
              + a.text(PX + 34, yP + 132, "masquerade y lista WAN acá", 15, a.OK, a.SANS, 600),
              a.show(72, 100), still=1))
a.add(a.group(a.text(PX + 34, yP + 96, "esperando PPP…", 15, a.GREY, a.MONO), a.show(30, 72), still=0))

# ether1 (física)
yE = PY + 250
a.add(a.box(PX + 18, yE, PW - 36, 104, a.SLATE, rx=12))
a.add(a.text(PX + 34, yE + 32, "ether1", 19, a.INK, a.MONO, 600))
a.add(a.text(PX + 34, yE + 56, "puerto físico", 15, a.TXT))
a.add(a.text(PX + 34, yE + 84, "sin IP · solo lleva las tramas", 15, a.GREY, a.MONO))
a.add(a.group(a.text(PX + PW / 2, yE - 12, "▲ la sesión viaja sobre ether1", 15, a.CYAN, a.MONO, 600, "middle"), a.show(30, 100), still=1))

# nota inferior
a.add(a.group(a.text(PX + 18, PY + 410, "Si scan no muestra ningún ac-name,", 15, a.BAD, a.SANS, 600)
              + a.text(PX + 18, PY + 432, "nadie contestó el PADI: una causa", 15, a.BAD, a.SANS, 600)
              + a.text(PX + 18, PY + 454, "posible es que el servicio lleve VLAN.", 15, a.BAD, a.SANS, 600),
              a.show(0, 30), still=0))
a.add(a.group(a.text(PX + 18, PY + 410, "Cada sesión nueva puede traer otra IP:", 15, a.TXT, a.SANS, 600)
              + a.text(PX + 18, PY + 432, "el acceso remoto va con DDNS", 15, a.TXT, a.SANS, 600)
              + a.text(PX + 18, PY + 454, "o con un túnel.", 15, a.TXT, a.SANS, 600),
              a.show(80, 100), still=1))

out(a, 15, 1, "PPPoE: descubrimiento y sesión PPP",
    "Animación en cinco tiempos entre el MikroTik (cliente PPPoE en ether1) y el concentrador del proveedor. "
    "1: el cliente manda PADI por broadcast y el concentrador contesta PADO con su ac-name, el que muestra scan; si no aparece ningún ac-name, nadie contestó y una causa posible es una VLAN. "
    "2: el cliente pide con PADR y el concentrador confirma con PADS y un número de sesión; aparece la interfaz lógica pppoe-antel sobre ether1. "
    "3: dentro de la sesión, PPP negocia el enlace con LCP. 4: el cliente se autentica con usuario y contraseña y el concentrador asigna la IP por IPCP. "
    "5: la IP queda en pppoe-antel, no en ether1, que es solo el puerto físico; por eso masquerade y la lista WAN apuntan a pppoe-antel. Cada sesión nueva puede traer otra IP.",
    [10, 30, 50, 75, 92])
