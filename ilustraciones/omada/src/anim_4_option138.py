#!/usr/bin/env python3
"""Teoría lección 4 (Tres caminos): el broadcast no cruza el router; la option 138 viaja en la respuesta DHCP
y el EAP llama directo al controlador. Llega con cada concesión nueva.
Salida: site2/ilustraciones/omada/4-t1.svg"""
import sys
sys.path.insert(0, "/home/claude/ies-training/ilustraciones/omada/src")
from _anim_omada import *  # noqa

a = nueva(22, "OPTION 138", "Option 138: la dirección llega con la IP")
F = a.steps([
    "El EAP está en otra subred: su broadcast al UDP 29810 muere en el router.",
    "El EAP pide IP. La respuesta DHCP trae la option 138 con la IP del controlador.",
    "El EAP llama directo a 192.168.88.10: el router lo rutea y aparece en Pending.",
    "La 138 llega con cada concesión nueva: un EAP que ya tenía IP espera a renovar.",
], still=2)

L = {"eap": 190, "rt": 600, "ctl": 1000}
HEAD = [("eap", "EAP", "VLAN 20 · 10.10.10.x", False), ("rt", "Router", "DHCP de la VLAN 20", False),
        ("ctl", "Controlador", "192.168.88.10", True)]
for k, t, s, dark in HEAD:
    x = L[k]
    a.add(nodo(a, x - 130, 176, 260, 66, t, s, dark=dark, tsize=19))
    a.add(linea(a, x, 242, x, 530, a.LINE, 2, "4 6"))


def msg(x1, x2, y, label, color, t0, t1=100, still=0, dash="", lab_x=None, anchor="middle"):
    d = f"M{x1} {y} H{x2 - (8 if x2 > x1 else -8)}"
    lx = lab_x if lab_x is not None else (x1 + x2) / 2
    inner = a.arrow(d, color, 3, dash) + a.text(lx, y - 12, label, 16, color, a.MONO, 600, anchor)
    en(a, inner, t0, t1, still)
    # punto que viaja por la flecha
    viaje(a, f'<circle r="7" fill="{color}"/>', x1, y, x2 - (10 if x2 > x1 else -10), y, t0, t0 + 3, hold=0.3)


s1, s2, s3, s4 = (f[0] for f in F)
# 1: broadcast que muere en el router
msg(L["eap"], L["rt"] - 18, 290, "broadcast UDP 29810", a.BAD, s1 + 2, 100, 1, "7 6")
en(a, bad(a, L["rt"], 290, 15), s1 + 6, 100, still=1)
en(a, a.text(L["rt"] + 26, 296, "no cruza routers", 16, a.BAD, a.SANS, 600), s1 + 6, 100, still=1)
# 2: DHCP con option 138
msg(L["eap"], L["rt"], 350, "pide IP (DHCP)", a.BLUE, s2 + 2, 100, 1)
msg(L["rt"], L["eap"], 404, "IP 10.10.10.x + option 138", a.OK, s2 + 9, 100, 1)
en(a, chip(a, L["rt"] + 24, 386, "0xC0A8580A = 192.168.88.10", a.OK, a.OKBG, stroke=a.OK), s2 + 11, 100, still=1)
# 3: llamada directa al controlador
msg(L["eap"], L["ctl"], 466, "directo a 192.168.88.10", a.BLUE, s3 + 2, 100, 1, lab_x=L["eap"] + 30, anchor="start")
en(a, ok(a, L["rt"], 466, 13), s3 + 4, 100, still=1)
en(a, chip(a, L["ctl"], 488, "Pending", a.AMB, a.AMBBG, anchor="middle", stroke=a.AMB), s3 + 7, 100, still=1)
en(a, a.text(L["rt"] + 22, 500, "unicast: el router lo rutea", 15, a.GREY, a.MONO), s3 + 4, 100, still=1)

# 4: la concesión
hl = a.box(L["eap"] - 150, 312, L["rt"] - L["eap"] + 520, 116, "none", a.AMB, rx=14, sw=3, extra='stroke-dasharray="8 6"')
fase(a, hl, F, 3)
band = (a.box(48, 548, 1104, 56, a.AMBBG, a.AMB, rx=14, sw=1.5)
        + a.text(72, 583, "Ya tenía IP: no pide nada y no se entera. Desconectalo y reconectalo para que renueve.", 17, a.AMB, a.SANS, 600))
fase(a, band, F, 3)

pie(a, F, [
    "El descubrimiento por broadcast solo sirve dentro de la misma subred.",
    "En RouterOS el valor es la IP en hexadecimal, un byte por octeto, sin nada más.",
    "Desde acá, el EAP sigue el camino normal de adopción.",
    "",
], y=640, still=2)

salida(a, 4, 1, "Option 138: la dirección del controlador llega con la IP",
       "Diagrama de mensajes animado entre el EAP en la VLAN 20 (10.10.10.x), el router que da DHCP en esa VLAN y el controlador en "
       "192.168.88.10. 1: el broadcast del EAP al UDP 29810 muere en el router, que no lo deja cruzar. 2: el EAP pide IP por DHCP y la "
       "respuesta trae la option 138, 0xC0A8580A, que es 192.168.88.10 en hexadecimal. 3: el EAP llama directo al controlador por unicast, "
       "el router lo rutea y el equipo aparece en Pending. 4: la opción llega con cada concesión nueva; un EAP que ya tenía IP no pide nada "
       "y no se entera hasta renovar, por ejemplo desconectándolo y reconectándolo.",
       [12, 37, 62, 88])
