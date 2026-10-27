#!/usr/bin/env python3
"""Teoría lección 5 (Sitios y clientes): las capas de Omada y hasta dónde llega cada rol.
Salida: site2/ilustraciones/omada/5-t1.svg"""
import sys
sys.path.insert(0, "/home/claude/ies-training/ilustraciones/omada/src")
from _anim_omada import *  # noqa

a = nueva(22, "SITIOS Y ROLES", "Cada usuario llega hasta donde le da su rol")
F = a.steps([
    "Capas: MSP (opcional), cliente, un sitio por sede y los equipos de esa sede.",
    "Main Administrator: accede a todo en su vista.",
    "Administrator: casi todo, con algunas cosas reservadas.",
    "Viewer limitado a Sucursal: mira estado y ajustes, sin cambiar nada.",
], still=3)

# --- árbol
MX, MY, MW, MH = 214, 182, 320, 58
a.add(a.box(MX, MY, MW, MH, a.WHITE, a.GREY, rx=14, sw=2, extra='stroke-dasharray="6 6"'))
a.add(a.text(MX + 20, MY + 36, "MSP", 19, a.INK, a.HEAD, 600) + a.text(MX + 76, MY + 36, "opcional, del integrador", 15, a.GREY, a.MONO))
CY_ = 278
a.add(nodo(a, MX, CY_, MW, 62, "Cliente", "su vista Global", tsize=19))
SITES = [("Sitio Central", 60), ("Sitio Sucursal", 388)]
SY, SW, SH = 392, 300, 150
a.add(linea(a, MX + MW / 2, MY + MH, MX + MW / 2, CY_, a.GREY, 2, "4 5"))
a.add(f'<path d="M{MX + MW / 2} {CY_ + 62} V{CY_ + 88} H{60 + SW / 2} V{SY} M{MX + MW / 2} {CY_ + 88} H{388 + SW / 2} V{SY}" fill="none" stroke="{a.GREY}" stroke-width="2"/>')
for t, x in SITES:
    a.add(a.box(x, SY, SW, SH, "#EAF2FB", a.BLUE, rx=14, sw=2))
    a.add(a.text(x + 20, SY + 34, t, 19, a.INK, a.HEAD, 600))
    a.add(a.text(x + 20, SY + 60, "un solo gateway", 15, a.GREY, a.MONO))
    cx = x + 20
    for lab in ("ER", "SW", "EAP"):
        a.add(chip(a, cx, SY + 92, lab, a.WHITE, a.BLUE))
        cx += chipw(lab) + 10

# fase 1: las capas se marcan de arriba hacia abajo
s0 = F[0][0]
for i, (x, y, w, h) in enumerate([(MX, MY, MW, MH), (MX, CY_, MW, 62), (60, SY, 628, SH)]):
    en(a, a.box(x - 6, y - 6, w + 12, h + 12, "none", a.CYAN, rx=18, sw=3), s0 + 1 + i * 6, F[0][1])

# alcance de cada rol
alc_todo = a.box(44, CY_ - 12, 660, SY + SH - CY_ + 24, a.OK, a.OK, rx=20, sw=3, extra='fill-opacity=".07"')
fase(a, alc_todo, F, 1)
fase(a, alc_todo.replace(a.OK, a.BLUE), F, 2)
fase(a, a.box(380, SY - 10, SW + 16, SH + 20, a.OK, a.OK, rx=20, sw=3, extra='fill-opacity=".07"')
     + a.box(56, SY - 4, SW + 8, SH + 8, a.BG, None, rx=16, extra='fill-opacity=".93"')
     + a.text(60 + SW / 2, SY + SH / 2 + 6, "no lo ve", 19, a.GREY, a.HEAD, 600, "middle"), F, 3, still=1)

# --- tarjeta del usuario
RX, RY, RW, RH = 744, 182, 408, 360
a.add(a.box(RX, RY, RW, RH, a.WHITE, a.LINE))


def tarjeta(usuario, rol, rol_c, rol_bg, si, no):
    s = a.text(RX + 24, RY + 40, usuario, 21, a.INK, a.HEAD, 600)
    s += chip(a, RX + 24, RY + 58, rol, rol_c, rol_bg, stroke=rol_c)
    y = RY + 130
    for t in si:
        s += ok(a, RX + 38, y - 6, 11) + a.text(RX + 60, y, t, 17, a.TXT, a.SANS)
        y += 36
    for t in no:
        s += bad(a, RX + 38, y - 6, 11) + a.text(RX + 60, y, t, 17, a.TXT, a.SANS)
        y += 36
    return s


fase(a, a.text(RX + 24, RY + 40, "Regla de diseño", 21, a.INK, a.HEAD, 600)
     + "".join(a.text(RX + 24, RY + 86 + i * 32, t, 17, a.TXT, a.SANS) for i, t in enumerate([
         "Un sitio adopta un solo gateway:",
         "si una sede tiene su propio ER,",
         "es un sitio nuevo.",
         "",
         "Roaming: solo entre EAP del",
         "mismo sitio.",
         "Auto IPsec: une sitios distintos",
         "del mismo controlador."])), F, 0)
fase(a, tarjeta("la empresa", "Main Administrator", a.OK, a.OKBG,
                ["Todo en su vista", "Backups automáticos", "Licencias"], []), F, 1)
fase(a, tarjeta("un técnico", "Administrator", a.BLUE, "#EAF2FB",
                ["Sitios, redes y equipos"], ["No migra clientes", "No hace backups automáticos", "Licencias: solo lectura"]), F, 2)
fase(a, tarjeta("viewer-sucursal", "Viewer", a.AMB, a.AMBBG,
                ["Ve solo el sitio Sucursal", "Mira estado y ajustes"], ["No cambia nada", "Central no aparece"]), F, 3, still=1)

pie(a, F, [
    "Con MSP, cada usuario lleva dos roles: uno MSP y uno Customer.",
    "Main Administrator es para la empresa, no para cada técnico.",
    "Un usuario por persona: se sabe quién cambió qué.",
    "Sacarle el acceso a alguien no obliga a cambiarle la clave a todos.",
], y=640, still=3)

salida(a, 5, 1, "Cada usuario llega hasta donde le da su rol",
       "Animación en cuatro tiempos sobre el árbol de Omada: MSP opcional, cliente con su vista Global y dos sitios, Central y Sucursal, "
       "cada uno con un solo gateway más switch y EAP. 1: se marcan las capas; un sitio adopta un solo gateway, el roaming es dentro del "
       "sitio y Auto IPsec une sitios. 2: Main Administrator alcanza todo en su vista. 3: Administrator alcanza sitios, redes y equipos, "
       "pero no migra clientes, no hace backups automáticos y ve las licencias solo para lectura. 4: el usuario viewer-sucursal con rol "
       "Viewer ve solo el sitio Sucursal, mira estado y ajustes y no cambia nada; Central no le aparece.",
       [12, 37, 62, 88])
