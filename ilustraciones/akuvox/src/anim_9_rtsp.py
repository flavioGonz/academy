#!/usr/bin/env python3
"""Lección 9 · teoría: cómo un NVR pide el video del portero por RTSP con autorización Digest."""
from _anim_akuvox import Anim, A, draw_arrow, token, chip, lane, note, appear, finish

a = Anim(T=25, kicker="AKUVOX · RTSP AL NVR", title="El NVR le pide el video al portero")
a.steps([
    "El NVR abre TCP al 554 del portero y pide DESCRIBE del stream.",
    "Con la autorización activa, el portero responde 401 con un desafío Digest.",
    "El NVR repite con un resumen hecho con la clave: la clave no viaja.",
    "El portero describe el stream (H.264, 25 fps). El NVR pide SETUP y PLAY.",
    "El video llega en paquetes RTP: por UDP o dentro de la misma conexión TCP.",
], still=2)

XN, XP = 190, 690
lane(a, XN, 176, 630, "NVR", "graba la grilla")
lane(a, XP, 176, 630, "Portero", "192.168.88.21:554")


def msg(x1, x2, y, s, color, t0, t1, dashed=False, tok=None, size=15):
    draw_arrow(a, [(x1, y), (x2, y)], t0, t1, color, dashed=dashed)
    appear(a, a.text((x1 + x2) / 2, y - 11, s, size, color, A.MONO, 600, "middle"), t1 - 0.5, 100, still=1)
    if tok:
        token(a, [(x1, y), (x2, y)], t0, t1, chip(a, tok, bg=color, size=13, h=24))


msg(XN, XP, 276, "DESCRIBE rtsp://…/live/ch00_1", A.BLUE, 3, 9, tok="DESCRIBE")
msg(XP, XN, 326, "401 · desafío Digest", A.GREY, 22, 27, dashed=True)
msg(XN, XP, 376, "DESCRIBE + resumen Digest", A.BLUE, 42, 48, tok="resumen")
msg(XP, XN, 426, "200 OK · H.264 · 25 fps", A.OK, 62, 67)
msg(XN, XP, 470, "SETUP", A.BLUE, 69, 72)
msg(XN, XP, 512, "PLAY", A.BLUE, 74, 77)
appear(a, a.box(XN, 540, XP - XN, 52, "#E4F5FB", None, rx=8)
       + a.text((XN + XP) / 2, 574, "RTP · video", 16, A.CYAN, A.MONO, 600, "middle"), 81, 100, still=1)
frame = '<rect x="-16" y="-9" width="32" height="18" rx="4" fill="#17A8D4"/>'
for i in range(7):
    t0 = 82 + i * 2.4
    token(a, [(XP - 22, 552), (XN + 22, 552)], t0, min(t0 + 5, 99.6), frame, hold=min(t0 + 5.2, 99.8))

PX, PW = 822, 330
panels = [
    ("Qué stream pide", ["ch00_1: secundario, 512 kbps", "ch00_0: principal, 2048 kbps", "Para la grilla alcanza", "el secundario."], "info"),
    ("401 no es un error", ["Es el portero pidiendo", "credencial: RTSP", "Authorization en Digest."], "info"),
    ("La clave no viaja", ["El resumen se calcula con", "la clave de nvr-lab y el", "desafío. Quien mire la red", "no ve la clave."], "ok"),
    ("SETUP y PLAY", ["Con la descripción del", "stream, el NVR prepara la", "recepción y pide arrancar."], "info"),
    ("Llega el video", ["Paquetes RTP por UDP, o", "intercalados en la misma", "conexión TCP del 554."], "info"),
]
for i, (t, ls, k) in enumerate(panels):
    s, h = note(a, PX, 186, PW, t, ls, k)
    appear(a, s, i * 20 + 1, (i + 1) * 20, still=1 if i == 2 else 0, fade=0.8)
s, _ = note(a, PX, 428, PW, "ONVIF, un nivel arriba", ["El NVR consulta", "/onvif/device_service, ve", "los perfiles y obtiene las", "URL RTSP sin escribirlas."], "info", size=15, lh=21)
a.add(s)

finish(a, "9-t1.svg", "El NVR pide el video del portero por RTSP",
       "Animación en cinco tiempos con dos líneas de vida: el NVR y el portero 192.168.88.21 en el puerto 554. "
       "1: el NVR abre una conexión TCP al 554 y pide DESCRIBE rtsp://192.168.88.21/live/ch00_1, el stream secundario de 512 kbps. "
       "2: con la autorización RTSP activada, el portero responde 401 con un desafío Digest. "
       "3: el NVR repite el DESCRIBE con un resumen calculado con la clave de su usuario y el desafío; la clave no viaja. "
       "4: el portero responde 200 OK describiendo el stream, H.264 a 25 fps, y el NVR pide SETUP y PLAY. "
       "5: el video llega al NVR en paquetes RTP, por UDP o intercalados en la misma conexión TCP. "
       "Nota: con ONVIF el NVR consulta /onvif/device_service, ve los perfiles y obtiene las URL RTSP sin escribirlas.",
       [8, 28, 50, 72, 93])
