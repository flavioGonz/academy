#!/usr/bin/env python3
"""Lección 9 · Laboratorio, paso 6: el salto al EAP 2 con WPA2-Personal, sin y con 802.11r.
Sin r: autenticación, reasociación y el intercambio de 4 mensajes de claves antes de los datos.
Con r (Fast BSS Transition): las claves se derivan en la autenticación y la reasociación; no hay intercambio de 4 mensajes."""
from _anim_om_red import *

a = nueva(26, "ROAMING Y MESH", "El salto al EAP 2, sin y con 802.11r", "l")
F = a.steps([
    "Sin 802.11r: autenticación y reasociación con el EAP 2.",
    "Después, el intercambio de 4 mensajes de claves (EAPOL). Recién ahí, datos.",
    "Con 802.11r: las claves viajan en la autenticación y la reasociación. Datos enseguida.",
    "Un cliente viejo que no tolera 802.11r cambia de EAP y se queda sin internet: apagalo.",
], still=2)

L = (110, 520)
R = (690, 1100)
for (xn, xe), title, x0 in ((L, "Sin 802.11r", 48), (R, "Con 802.11r", 628)):
    a.add(a.box(x0, 176, 524, 418, a.WHITE, a.LINE, rx=16))
    a.add(a.text(x0 + 20, 206, title, 17, a.INK, a.SANS, 600))
    a.add(a.text(xn, 236, "notebook", 15, a.GREY, a.MONO, 600, "middle") + a.text(xe, 236, "EAP 2", 15, a.GREY, a.MONO, 600, "middle"))
    a.add(lifeline(a, xn, 246, 580) + lifeline(a, xe, 246, 580))

xn, xe = L
Y = 272
seqL = [(xn, xe, "Authentication", a.BLUE, 3), (xe, xn, "Authentication", a.BLUE, 6),
        (xn, xe, "Reassociation Request", a.BLUE, 10), (xe, xn, "Reassociation Response", a.BLUE, 14),
        (xe, xn, "EAPOL 1/4", a.AMB, 28), (xn, xe, "EAPOL 2/4", a.AMB, 32), (xe, xn, "EAPOL 3/4", a.AMB, 36), (xn, xe, "EAPOL 4/4", a.AMB, 40)]
for i, (x1, x2, lab, col, t) in enumerate(seqL):
    msg(a, x1, x2, Y + i * 36, lab, t, color=col, lsize=15, dur=2)
at(a, a.box(L[0] - 10, Y + 4 * 36 - 26, L[1] - L[0] + 20, 4 * 36 - 4, "none", a.AMB, rx=10, sw=2, extra='stroke-dasharray="6 5"'), 28, 100, still=1)
msg(a, xn, xe, Y + 8 * 36 + 8, "datos", 45, color=a.OK, lsize=15, dur=2)

xn, xe = R
seqR = [(xn, xe, "Authentication (FT)", a.CYAN, 53), (xe, xn, "Authentication (FT)", a.CYAN, 56),
        (xn, xe, "Reassociation (FT)", a.CYAN, 60), (xe, xn, "Reassociation (FT)", a.CYAN, 63)]
for i, (x1, x2, lab, col, t) in enumerate(seqR):
    msg(a, x1, x2, Y + i * 36, lab, t, color=col, lsize=15, dur=2)
msg(a, xn, xe, Y + 4 * 36 + 8, "datos", 67, color=a.OK, lsize=15, dur=2)
at(a, note(a, 648, Y + 5 * 36 + 10, 484, 112, "Sin los 4 mensajes", ["Las claves para el EAP nuevo ya estaban", "preparadas: el salto tarda menos y el ping", "corta menos."], "ok"), 68, 100, still=1)

# 4: cliente viejo
at(a, a.box(628, 176, 524, 418, a.WHITE, a.BAD, rx=16, sw=2.5), 76, 100)
at(a, a.text(648, 206, "Cliente viejo con 802.11r", 17, a.BAD, a.SANS, 600), 76, 100)
at(a, a.text(668, 262, "PS> ping -t 192.168.88.1", 15, a.INK, a.MONO)
   + a.text(668, 292, "Respuesta desde 192.168.88.1 ...", 15, a.OK, a.MONO)
   + a.text(668, 322, "Tiempo de espera agotado ...", 15, a.BAD, a.MONO, 600)
   + a.text(668, 352, "Tiempo de espera agotado ...", 15, a.BAD, a.MONO, 600)
   + a.text(668, 382, "Tiempo de espera agotado ...", 15, a.BAD, a.MONO, 600), 78, 100)
at(a, note(a, 648, 420, 484, 150, "Dejalo apagado en ese SSID", ["Edit SSID > Advanced Settings > 802.11r.", "Probá con un equipo de cada tipo del cliente;", "si alguno pierde internet al cambiar de EAP,", "va sin r o a un SSID aparte."], "bad"), 80, 100)

status(a, 628, [
    (0, 25, "WPA2-Personal: el cliente se autentica y se reasocia con el EAP nuevo.", a.INK, 0),
    (25, 50, "Sin r, el salto incluye el intercambio completo de claves con cada EAP.", a.INK, 0),
    (50, 75, "802.11r prepara las claves por adelantado: menos tiempo sin datos.", a.OK, 1),
    (75, 100, "802.11r se elige por SSID: si un equipo no lo tolera, ese SSID va sin r.", a.BAD, 0),
], x=48, anchor="start", size=16)

write(a, 9, "l2", "El salto al EAP 2 sin y con 802.11r",
      "Animación en cuatro tiempos con dos diagramas de mensajes entre la notebook y el EAP 2, con WPA2-Personal. "
      "1: sin 802.11r, la notebook hace Authentication y Reassociation Request y Response con el EAP 2. "
      "2: después viene el intercambio de 4 mensajes de claves, EAPOL 1/4 a 4/4, y recién ahí pasan los datos. "
      "3: con 802.11r, Fast BSS Transition, las claves viajan en la autenticación y la reasociación FT y los datos pasan enseguida, sin los 4 mensajes: el salto tarda menos y el ping corta menos. "
      "4: un cliente viejo que no tolera 802.11r cambia de EAP y se queda sin internet: el ping muestra Tiempo de espera agotado una y otra vez. "
      "Se deja 802.11r apagado en ese SSID, en Edit SSID, Advanced Settings, o esos equipos van a un SSID aparte.",
      [8, 40, 66, 92])
