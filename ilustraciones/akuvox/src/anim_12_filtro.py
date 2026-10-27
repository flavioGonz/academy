#!/usr/bin/env python3
"""Lección 12 · teoría: el filtro de Wireshark deja solo el registro SIP y se lee el segundo rechazo."""
from _anim_akuvox import Anim, A, note, appear, finish, cls

a = Anim(T=24, kicker="AKUVOX · DIAGNÓSTICO", title="Encontrar la falla de registro en la captura")
a.steps([
    "La PCAP trae todo lo que pasó: el registro se pierde entre el resto.",
    "Con el filtro de la lección quedan solo REGISTER, 401 y 403.",
    "El primer 401 es normal: la central manda el nonce y pide credencial.",
    "Tras el REGISTER con resumen llega otro rechazo: la clave está mal.",
], still=3)

LX, LW = 48, 660
a.add(a.box(LX, 176, LW, 446, A.WHITE, A.LINE))
a.add(a.box(LX, 176, LW, 44, "#E6EEF6", None, rx=14))
a.add(a.text(LX + 18, 204, "captura.pcap · filtro:", 14, A.GREY, A.MONO))
FIL = 'sip.Method == "REGISTER" || sip.Status-Code == 401 || sip.Status-Code == 403'
appear(a, a.box(LX + 8, 226, LW - 16, 54, A.OKBG, A.OK, rx=8, sw=1.5) + a.text(LX + 18, 248, 'sip.Method == "REGISTER"', 15, A.OK, A.MONO, 600)
       + a.text(LX + 18, 270, '|| sip.Status-Code == 401 || sip.Status-Code == 403', 15, A.OK, A.MONO, 600), 26, 100, still=1)
appear(a, a.box(LX + 8, 226, LW - 16, 54, A.SLATE, None, rx=8) + a.text(LX + 18, 259, "(sin filtro)", 15, A.GREY, A.MONO), 0, 26, still=0)
a.add(a.text(LX + 18, 302, "N°", 13, A.GREY, A.MONO))
a.add(a.text(LX + 70, 302, "PROTOCOLO", 13, A.GREY, A.MONO))
a.add(a.text(LX + 190, 302, "INFO", 13, A.GREY, A.MONO))

rows = [
    ("ARP", "¿Quién tiene 10.10.10.1?", None),
    ("DNS", "consulta", None),
    ("SIP", "REGISTER · portero → central", "reg1"),
    ("ARP", "¿Quién tiene 10.10.10.1?", None),
    ("SIP", "401 Unauthorized · nonce", "401"),
    ("DNS", "respuesta", None),
    ("SIP", "REGISTER con resumen", "reg2"),
    ("ARP", "¿Quién tiene 10.10.20.10?", None),
    ("SIP", "403 Forbidden", "403"),
    ("DNS", "consulta", None),
]
Y0, H = 312, 30
k = 0
for i, (proto, info, tag) in enumerate(rows):
    y_full = Y0 + i * H
    inner = (a.box(LX + 8, 0, LW - 16, H - 4, A.SLATE if tag else "#F4F7FA", None, rx=6)
             + a.text(LX + 18, 19, str(i + 1), 14, A.GREY, A.MONO)
             + a.text(LX + 70, 19, proto, 14, A.BLUE if tag else A.GREY, A.MONO, 600)
             + a.text(LX + 190, 19, info, 14, A.INK if tag else A.GREY, A.MONO, 600 if tag else 400))
    if tag:
        y_f = Y0 + k * 42
        k += 1
        mv = a.move([(0, 0, y_full), (26, 0, y_full), (30, 0, y_f), (98.5, 0, y_f), (100, 0, y_full)])
        c = cls(a, f"opacity:1;transform-box:view-box;transform:translate(0px,{y_f}px);", mv)
        a.add(f'<g class="{c}">{inner}</g>')
    else:
        a.add(a.group(f'<g transform="translate(0 {y_full})">{inner}</g>', a.show(0, 26, 1.5), still=0))

# resaltados (posiciones filtradas)
y401, y403 = Y0 + 1 * 42, Y0 + 3 * 42
appear(a, a.box(LX + 6, y401 - 3, LW - 12, H + 2, "none", A.AMB, rx=8, sw=3)
       + a.pill(LX + LW - 16, y401 + 1, "normal", A.AMB, A.AMBBG, 13, 24, "end"), 52, 100, still=1)
appear(a, a.box(LX + 6, y403 - 3, LW - 12, H + 2, "none", A.BAD, rx=8, sw=3)
       + a.pill(LX + LW - 16, y403 + 1, "la falla", A.BAD, A.BADBG, 13, 24, "end"), 77, 100, still=1)
appear(a, a.text(LX + 18, Y0 + 4 * 42 + 34, "4 de 10 paquetes · el resto era tráfico de fondo", 15, A.GREY, A.SANS, 600), 31, 100, still=1)

PX, PW = 740, 412
panels = [
    ("La captura guarda todo", ["Buffer de 1 MB en el portero:", "el REGISTER pesa poco y", "queda entre ARP, DNS y el", "resto del tráfico."], "info"),
    ("El filtro de la lección", ["Deja solo los REGISTER y", "las respuestas 401 y 403."], "info"),
    ("401: la central desafía", ["Manda un nonce. El portero", "repite con un resumen de", "usuario, clave y nonce."], "amb"),
    ("Segundo rechazo: la falla", ["Con la clave mal llega otro", "401 o un 403. En la central,", "pjsip set logger on muestra", "Failed to authenticate."], "bad"),
]
for i, (t, ls, kk) in enumerate(panels):
    s, h = note(a, PX, 186, PW, t, ls, kk)
    appear(a, s, i * 25 + 1, (i + 1) * 25, still=1 if i == 3 else 0, fade=0.8)
s, _ = note(a, PX, 430, PW, "Registro sano", ["El 200 OK no entra en este filtro:", "después del REGISTER con resumen", "no aparece ningún rechazo."], "ok", size=15, lh=21)
a.add(s)

finish(a, "12-t1.svg", "El filtro de Wireshark que encuentra la falla de registro",
       "Animación en cuatro tiempos sobre la lista de paquetes de captura.pcap. "
       "1: sin filtro, la captura muestra diez paquetes mezclados, ARP, DNS y SIP, y el registro se pierde entre el tráfico de fondo. "
       "2: se aplica el filtro sip.Method == \"REGISTER\" || sip.Status-Code == 401 || sip.Status-Code == 403 y quedan cuatro: REGISTER, 401 Unauthorized con nonce, REGISTER con resumen y 403 Forbidden. "
       "3: el primer 401 es normal: la central manda el nonce y pide credencial. "
       "4: después del REGISTER con resumen llega otro rechazo, la falla: la clave está mal y la central registra Failed to authenticate. "
       "Nota: en un registro sano el 200 OK no entra en este filtro, así que después del REGISTER con resumen no aparece ningún rechazo.",
       [12, 40, 65, 92])
