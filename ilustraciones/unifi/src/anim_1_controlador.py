#!/usr/bin/env python3
"""Lección 1 · teoría: qué vive en el controlador y qué pasa cuando falta internet o falta el controlador."""
from _anim_unifi import *  # noqa

a = new(25, "Quién manda", "Dónde vive la configuración, y qué sigue andando", [
    "El controlador guarda la configuración y la empuja a cada equipo.",
    "Cada equipo se reporta al controlador por su URL de inform.",
    "Desde afuera: Site Manager conecta al técnico con el controlador.",
    "Cae internet: desde afuera no se llega; en la LAN se sigue gestionando.",
    "Cae el controlador: el WiFi sigue con lo último, pero nadie cambia nada.",
], still=4)

# arriba: técnico y Site Manager
a.add(node(a, 48, 182, 290, 70, "Técnico", "fuera del sitio"))
a.add(node(a, 470, 182, 330, 70, "Site Manager", "unifi.ui.com · no guarda config"))
a.add(line(a, [(338, 217), (462, 217)], A.GREY, 2.5, "6 6", arrow=True))
a.add(line(a, [(635, 252), (635, 330)], A.GREY, 2.5, "6 6"))

# sitio
a.add(a.box(40, 288, 1120, 362, "none", A.GREY, rx=18, sw=1.5, extra='stroke-dasharray="6 6"'))
a.add(a.text(64, 316, "SITIO DEL CLIENTE", 14, A.GREY, A.MONO, extra='letter-spacing="2"'))
CX, CY, CW, CH = 465, 330, 340, 84
a.add(node(a, CX, CY, CW, CH, "Controlador", "redes · WiFi · puertos · firewall", dark=True, ssize=14))
DEV = [(150, "AP 1"), (480, "AP 2"), (810, "Switch")]
DY = 520
for x, n in DEV:
    a.add(line(a, [(635, CY + CH), (635, 468), (x + 120, 468), (x + 120, DY)], A.LINE, 2.5))
for x, n in DEV:
    a.add(node(a, x, DY, 240, 66, n, "WiFi al aire" if n != "Switch" else "puertos activos", ssize=14))

# notebook en la LAN (tiempos 4 y 5)
vis(a, node(a, 64, 336, 270, 70, "Notebook", "en la LAN del sitio", ssize=14) + line(a, [(334, 371), (CX - 6, 371)], A.OK, 3), 3, 4)

# 1: config hacia los equipos
s0, s1 = ph(a, 0)
for k, (x, n) in enumerate(DEV):
    token(a, [(635, CY + CH + 14), (635, 468), (x + 120, 468), (x + 120, DY - 14)], s0 + 2 + k * 3, s0 + 10 + k * 3,
          "config", bg=A.BLUE, hold=s1 - 1)

# 2: inform hacia el controlador
s0, s1 = ph(a, 1)
for k, (x, n) in enumerate(DEV):
    token(a, [(x + 120, DY - 14), (x + 120, 468), (635, 468), (635, CY + CH + 14)], s0 + 2 + k * 3, s0 + 10 + k * 3,
          "inform", bg=A.CYAN, hold=s1 - 1)

# 3: sesión del técnico por Site Manager
s0, s1 = ph(a, 2)
token(a, [(338, 217), (470, 217)], s0 + 1, s0 + 5, "sesión", bg=A.NAVY2, hold=s0 + 5.2)
token(a, [(635, 262), (635, 322)], s0 + 6, s0 + 11, "sesión", bg=A.NAVY2, hold=s1 - 1)
vis(a, pill(a, 816, 203, "conecta, no guarda", "info"), 2)

# 4: cae internet
vis(a, xmark(a, 635, 272) + pill(a, 662, 258, "sin internet", "bad"), 3)
vis(a, xmark(a, 400, 217), 3)
s0, s1 = ph(a, 3)
token(a, [(340, 371), (CX - 50, 371)], s0 + 3, s0 + 10, "cambio", bg=A.OK, hold=s1 - 1)
vis(a, check(a, CX - 50, 334, 13), 3)

# 5: cae el controlador
vis(a, a.box(CX, CY, CW, CH, A.SLATE, A.BAD, rx=14, sw=2.5)
    + a.text(CX + 20, CY + 38, "Controlador", 20, A.GREY, A.HEAD, 600)
    + a.text(CX + 20, CY + 62, "apagado", 15, A.BAD, A.MONO, 600), 4)
for x, n in DEV:
    vis(a, pill(a, x + 120, DY + 82, "sigue con lo último", "ok", size=14, anchor="middle"), 4)
s0, s1 = ph(a, 4)
token(a, [(340, 371), (CX - 84, 371)], s0 + 2, s0 + 8, "cambio", bg=A.GREY, hold=s1 - 1, still=1)
vis(a, xmark(a, CX - 24, 371, 13), 4)

write(a, "1-t1.svg", "Dónde vive la configuración en UniFi", mid_pcts(a))
