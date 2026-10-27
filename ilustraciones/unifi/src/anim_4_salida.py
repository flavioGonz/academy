#!/usr/bin/env python3
"""Lección 4 · teoría: la consola sale hacia afuera (DNS, NTP, TLS 443/8883); nadie entra."""
from _anim_unifi import *  # noqa

a = new(24, "Muchos sitios", "Todo sale desde la consola: nombre, hora y TLS", [
    "La consola busca nombres por DNS (UDP 53) y toma la hora por NTP (UDP 123).",
    "Con la hora bien valida el certificado y abre su salida: TCP 443 y 8883.",
    "El técnico entra a unifi.ui.com y llega por esa conexión que salió del sitio.",
    "Si NTP está bloqueado, la hora queda mal, TLS no valida y el sitio no aparece.",
], still=2)

# sitio
a.add(a.box(40, 182, 400, 400, "none", A.GREY, rx=18, sw=1.5, extra='stroke-dasharray="6 6"'))
a.add(a.text(62, 210, "SITIO DEL CLIENTE", 14, A.GREY, A.MONO, extra='letter-spacing="2"'))
KX, KY, KW, KH = 70, 340, 300, 96
a.add(node(a, KX, KY, KW, KH, "Consola", "UCG, CloudKey o Server", dark=True, ssize=14, sub2="Remote Management"))
a.add(a.text(60, 620, "Ningún puerto de entrada abierto: todo sale desde la consola.", 16, A.INK, A.SANS, 600))
# borde

# afuera
a.add(node(a, 640, 190, 240, 68, "DNS", "UDP 53", ssize=14))
a.add(node(a, 640, 278, 240, 68, "NTP", "UDP 123 · la hora", ssize=14))
SM = (640, 430, 290, 84)
a.add(node(a, *SM, "Site Manager", "unifi.ui.com · nube", ssize=14))
a.add(node(a, 980, 430, 172, 84, "Técnico", "navegador", ssize=14))
a.add(line(a, [(980, 472), (938, 472)], A.GREY, 2.5, arrow=True))

OUT = (KX + KW, KY + 30)
a.add(line(a, [(KX + KW, KY + 20), (632, 224)], A.LINE, 2))
a.add(line(a, [(KX + KW, KY + 40), (632, 312)], A.LINE, 2))
a.add(line(a, [(KX + KW, KY + 70), (632, 472)], A.LINE, 2))

# 1: DNS y NTP
s0, s1 = ph(a, 0)
token(a, [(KX + KW + 20, KY + 20), (600, 230)], s0 + 1, s0 + 7, "¿nombre?", bg=A.CYAN, hold=s0 + 7.3)
token(a, [(600, 236), (KX + KW + 40, KY + 24)], s0 + 8, s0 + 13, "IP", bg=A.BLUE, hold=s0 + 13.3)
token(a, [(KX + KW + 20, KY + 40), (600, 316)], s0 + 9, s0 + 15, "¿hora?", bg=A.CYAN, hold=s0 + 15.3)
token(a, [(600, 320), (KX + KW + 40, KY + 44)], s0 + 16, s0 + 22, "hora", bg=A.BLUE, hold=s0 + 22.6)
vis(a, pill(a, KX, KY + KH + 14, "hora correcta", "ok"), 0, 2)

# 2 y 3: conexión de salida establecida
s0, s1 = ph(a, 1)
at(a, line(a, [(KX + KW, KY + 70), (632, 472)], A.OK, 4, arrow=True), s0 + 8, ph(a, 2)[1], still=1)
at(a, pill(a, 540, 398, "TCP 443 · 8883", "ok", anchor="middle"), s0 + 8, ph(a, 2)[1], still=1)
token(a, [(KX + KW + 20, KY + 70), (620, 470)], s0 + 1, s0 + 8, "TLS", bg=A.OK, hold=s0 + 8.3)
vis(a, pill(a, KX, KY + KH + 50, "certificado válido", "ok"), 1, 2)

# 3: técnico
s0, s1 = ph(a, 2)
token(a, [(1066, 472), (930, 472)], s0 + 1, s0 + 5, "sesión", bg=A.NAVY2, hold=s0 + 5.2)
token(a, [(640, 472), (KX + KW + 40, KY + 72)], s0 + 6, s0 + 14, "sesión", bg=A.NAVY2, hold=s1 - 1, still=1)
vis(a, a.text(SM[0], SM[1] + SM[3] + 26, "arma la conexión, no guarda la config", 15, A.TXT, A.MONO), 2)

# 4: NTP bloqueado
s0, s1 = ph(a, 3)
token(a, [(KX + KW + 20, KY + 40), (428, 366)], s0 + 1, s0 + 5, "¿hora?", bg=A.CYAN, hold=s1 - 1)
vis(a, xmark(a, 490, 352), 3)
vis(a, pill(a, KX, KY + KH + 14, "hora mal", "bad"), 3)
vis(a, pill(a, KX, KY + KH + 50, "TLS no valida", "bad"), 3)
vis(a, xmark(a, 540, 434), 3)
vis(a, pill(a, SM[0], SM[1] + SM[3] + 10, "el sitio no aparece", "bad"), 3)
vis(a, a.text(640, 380, "Revisá: Remote Management, 443 y 8883, DNS y NTP, cuenta.", 15, A.BAD, A.SANS, 600), 3)

write(a, "4-t1.svg", "La consola UniFi sale hacia Site Manager", mid_pcts(a))
