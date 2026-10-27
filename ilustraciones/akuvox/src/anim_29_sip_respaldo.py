#!/usr/bin/env python3
"""Lección 29 · Teoría · El botón de emergencia: una llamada, dos intentos (escalera SIP).
Sale de teoria_md (Cómo funciona): INVITE a la central, suena el interno 200, sin respuesta la central
cancela ese intento y abre otro hacia el respaldo; para el portero es una sola llamada."""
from _anim_akuvox_29_42 import new, out, box, seq, when

a = new(24, "PUNTO DE EMERGENCIA · SIP", "Una llamada, dos intentos: el E21 no se entera")
a.steps([
    "Apretás el botón: el E21 manda un INVITE a la central, destino 200.",
    "La central hace sonar el interno 200. Al E21 le llega 180: está sonando.",
    "Nadie atiende en 20 s: la central cancela ese intento y llama al respaldo.",
    "Atiende el respaldo: 200 OK. Para el E21 fue una sola llamada.",
], still=3, size=18)

X = {"e21": 170, "pbx": 470, "i200": 770, "resp": 1050}
Y0, Y1 = 236, 600
a.add(box(60, 172, 220, 64, "E21", "extensión 801", "bell"))
a.add(box(360, 172, 220, 64, "Central IP", "regla de desvío", "server", dark=True))
a.add(box(660, 172, 220, 64, "Interno 200", "guardia", "user"))
a.add(box(940, 172, 220, 64, "Respaldo", "cola o celular", "phone"))
for k, x in X.items():
    a.add(f'<line x1="{x}" y1="{Y0}" x2="{x}" y2="{Y1}" stroke="{a.LINE}" stroke-width="3" stroke-dasharray="6 6"/>')


def msg(y, src, dst, label, t, color=None, dash="", until=100):
    x1, x2 = X[src], X[dst]
    sgn = 1 if x2 > x1 else -1
    seq(a, f"M{x1 + sgn * 4} {y} H{x2 - sgn * 8}", t, until, color or a.BLUE, label, (x1 + x2) / 2, y - 9, dash=dash)


msg(276, "e21", "pbx", "INVITE · 200", 3)
msg(316, "pbx", "i200", "INVITE", 27)
msg(356, "i200", "pbx", "180 suena", 32, a.GREY)
msg(356, "pbx", "e21", "180", 35, a.GREY)
# suena el 200 (solo mientras suena)
when(a, a.pill(X["i200"] + 14, 300, "suena…", a.AMB, a.AMBBG, 15, 28), 33, 54)
when(a, a.text(X["i200"] + 14, 330, "deja de sonar", 15, a.GREY, a.SANS, 600), 56, 100, still=1)
# tiempo sin respuesta
when(a, a.pill(X["pbx"] + 14, 376, "20 s sin respuesta", a.AMB, a.AMBBG, 15, 28), 42, 100, still=1)
msg(430, "pbx", "i200", "CANCEL", 52, a.BAD, "8 6")
msg(470, "pbx", "resp", "INVITE · respaldo", 57)
msg(512, "resp", "pbx", "200 OK · atiende", 77, a.OK)
msg(552, "pbx", "e21", "200 OK", 80, a.OK)
# voz extremo a extremo
when(a, f'<line x1="{X["e21"]}" y1="590" x2="{X["resp"]}" y2="590" stroke="{a.OK}" stroke-width="6" stroke-linecap="round" opacity=".35"/>'
     + a.text(320, 582, "voz de punta a punta", 15, a.OK, a.MONO, 600, "middle"), 85, 100, still=1)
# llave de lo que ve el E21
when(a, a.text(48, 640, "El E21 solo vio INVITE, 180 y 200 OK: los intentos y el desvío los maneja la central.", 18, a.INK, a.SANS, 600), 82, 100, still=1)
when(a, a.text(48, 640, "La regla de respaldo vive en la central, no en el portero.", 18, a.TXT, a.SANS, 600), 0, 81)

out(a, 29, 1, "Una llamada, dos intentos",
    "Diagrama de escalera animado entre el E21 (extensión 801), la central IP, el interno 200 y el respaldo. "
    "Tiempo 1: al apretar el botón, el E21 manda un INVITE a la central con destino 200. "
    "Tiempo 2: la central manda INVITE al interno 200, que suena, y el E21 recibe 180. "
    "Tiempo 3: pasan 20 segundos sin respuesta; la central manda CANCEL al 200 y un INVITE nuevo al respaldo, una cola o un celular. "
    "Tiempo 4: el respaldo atiende con 200 OK, la central le pasa 200 OK al E21 y la voz queda establecida. "
    "El E21 solo vio INVITE, 180 y 200 OK: para él fue una sola llamada.",
    [12, 40, 65, 92])
