#!/usr/bin/env python3
"""Lección 20 (Concentrador CHR) · Laboratorio paso 1: el orden del endurecimiento en un CHR recién instalado en una IP pública."""
from _anim_r20_31 import *

a, _ = nuevo(26, "MIKROTIK · CONCENTRADOR CHR · PASO 1", "CHR nuevo en IP pública: tu usuario primero",
             ["El CHR arranca con admin sin contraseña en 198.51.100.20: cualquiera puede probar.",
              "Desde tu sesión creás tecnico-lucia, con su clave.",
              "Abrís otra sesión con tecnico-lucia y entra. Recién ahí, /user/disable admin.",
              "Un bot prueba admin: no entra. Y WinBox y SSH solo atienden a la oficina y al túnel."], still=2)

XT, XC, XB = 180, 600, 1020
head(a, XT, 176, "Tu notebook", "oficina · 203.0.113.50", w=270)
head(a, XC, 176, "CHR", "198.51.100.20", w=250, kind="router")
dev(a, XB - 132, 176, 264, 70, "Escáneres", "de internet", kind="bad", tsize=17, ssize=14)
for x in (XT, XC, XB):
    lifeline(a, x, 246, 456)

# usuarios del CHR
a.add(a.box(48, 478, 520, 110, a.INK, rx=14))
a.add(a.text(66, 506, "/user/print", 14, SKY, a.MONO))
a.add(a.text(66, 538, "admin", 15, a.WHITE, a.MONO, 600))
flip(a, 220, 538, [(0, 62, "full · sin contraseña", ROSE), (62, 100, "deshabilitado", SKY)], size=15, still_idx=1)
a.add(a.text(66, 568, "tecnico-lucia", 15, a.WHITE, a.MONO, 600))
flip(a, 220, 568, [(0, 32, "(no existe)", SKY), (32, 100, "full · clave propia", MINT)], size=15, still_idx=1)

# 1. riesgo
msg(a, XB, XC, 290, "login admin, sin clave", 4, 25, a.BAD)
en(a, a.text(XC + 20, 330, "si llega antes que vos, entra", 15, a.BAD, a.SANS, 600), 8, 25)
# 2. crear usuario
msg(a, XT, XC, 290, "/user/add name=tecnico-lucia", 28, 75, a.BLUE, still=1, lsize=14)
# 3. probar y deshabilitar
msg(a, XT, XC, 340, "otra sesión: tecnico-lucia", 52, 75, a.OK, still=1, lsize=14)
msg(a, XC, XT, 380, "entra", 56, 75, a.OK, still=1)
msg(a, XT, XC, 420, "/user/disable admin", 61, 75, a.INK, still=1, lsize=14)
# 4. bot falla
msg(a, XB, XC, 300, "login admin", 78, 100, a.BAD, lost=True, frac=0.86)
en(a, a.text(XC + 20, 340, "admin deshabilitado", 15, a.OK, a.SANS, 600), 82, 100)
en(a, term(a, 600, 478, 552, ["/ip/service/set winbox,ssh", "  available-from=203.0.113.50/32,10.10.10.0/24", "/ip/service/disable telnet,ftp,www,api,api-ssl"], size=14, lh=24), 84, 100)
en(a, note(a, 600, 478, 552, 110, "El orden importa", ["Si deshabilitás admin antes de probar el usuario", "nuevo, te podés quedar afuera de un equipo que", "está en otro país."], "amb"), 0, 84, still=1)

narr(a, [
    (0, 25, "Una IP pública recibe escaneos todo el tiempo: el endurecimiento va primero.", a.BAD),
    (25, 50, "Tu usuario, con clave larga y grupo full.", a.TXT),
    (50, 75, "La sesión de admin sigue abierta hasta comprobar que el usuario nuevo entra.", a.OK),
    (75, 100, "Después: servicios apagados, MAC server y discovery en none, DNS remoto apagado.", a.TXT),
], still_idx=2)

escribir(a, "20-l1.svg", "Endurecer el CHR en orden",
         "Animación en cuatro tiempos con tu notebook en la oficina (203.0.113.50), el CHR recién instalado en 198.51.100.20 y escáneres de internet. Abajo, los usuarios del CHR. "
         "1: el CHR arranca con admin sin contraseña en una IP pública: si un escáner llega antes que vos, entra. 2: desde tu sesión creás el usuario tecnico-lucia con su clave. "
         "3: abrís otra sesión con tecnico-lucia, comprobás que entra y recién ahí deshabilitás admin; si lo hacés al revés, te podés quedar afuera. "
         "4: un escáner prueba admin y no entra porque está deshabilitado; además, WinBox y SSH quedan con available-from para la oficina y el túnel, y se apagan telnet, ftp, www, api y api-ssl.",
         [12, 40, 66, 74, 94])
